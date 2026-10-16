"""Conservatively convert the supplied STL batch to faceted STEP solids.

No remeshing, scaling, recentering, filling, smoothing, or component fusion.
Run from any directory. Inputs and outputs are relative to this repository.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import numpy as np
import trimesh
import cadquery as cq
from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid,
)
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepLib import BRepLib
from OCP.TopoDS import TopoDS
from OCP.TopAbs import TopAbs_SHELL
from OCP.gp import gp_Pnt
from OCP.IFSelect import IFSelect_RetDone

ROOT = Path(__file__).resolve().parents[1]
SEW_TOLERANCE = 1e-7
BOUNDS_TOLERANCE = 1e-5
RELATIVE_TOLERANCE = 1e-8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounds(shape) -> list[list[float]]:
    box = shape.BoundingBox()
    return [[box.xmin, box.ymin, box.zmin], [box.xmax, box.ymax, box.zmax]]


def main() -> None:
    manifest = json.loads((ROOT / 'tools/source-manifest.json').read_text())
    records = []
    (ROOT / 'models/step').mkdir(parents=True, exist_ok=True)
    (ROOT / 'docs').mkdir(exist_ok=True)
    for item in manifest['files']:
        name = item['name']
        source = ROOT / 'models/stl' / name
        before = digest(source)
        if before != item['sha256'] or source.stat().st_size != item['bytes']:
            raise ValueError(f'{name}: source bytes differ from the supplied batch')
        mesh = trimesh.load_mesh(source, process=False)
        mesh.merge_vertices(digits_vertex=12)
        if (not np.isfinite(mesh.vertices).all() or not mesh.is_watertight
                or not mesh.is_winding_consistent):
            raise ValueError(f'{name}: expected a finite, closed, consistently wound mesh')
        if len(mesh.faces) != item['triangles'] or (mesh.area_faces <= 1e-14).any():
            raise ValueError(f'{name}: unexpected face count or degenerate triangles')
        components = sorted(mesh.split(only_watertight=False),
                            key=lambda c: (-abs(c.volume), tuple(c.bounds[0])))
        if len(components) != item['components']:
            raise ValueError(f'{name}: unexpected connected-component count')
        solids, details = [], []
        for index, component in enumerate(components, 1):
            sewer = BRepBuilderAPI_Sewing(SEW_TOLERANCE, True, True, True, False)
            for triangle in component.triangles:
                polygon = BRepBuilderAPI_MakePolygon()
                for point in triangle:
                    polygon.Add(gp_Pnt(*map(float, point)))
                polygon.Close()
                face = BRepBuilderAPI_MakeFace(polygon.Wire())
                if not face.IsDone():
                    raise ValueError(f'{name}: triangle construction failed')
                sewer.Add(face.Face())
            sewer.Perform()
            shell = sewer.SewedShape()
            if shell.ShapeType() != TopAbs_SHELL or not shell.Closed():
                raise ValueError(f'{name}, component {index}: not one closed shell')
            solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shell)).Solid()
            if not BRepLib.OrientClosedSolid_s(solid) or not BRepCheck_Analyzer(solid).IsValid():
                raise ValueError(f'{name}, component {index}: invalid solid')
            obj = cq.Shape.cast(solid)
            volume_error = abs(obj.Volume() - abs(component.volume)) / max(abs(component.volume), 1.)
            area_error = abs(obj.Area() - component.area) / max(component.area, 1.)
            bounds_error = float(np.max(np.abs(np.asarray(bounds(obj)) - component.bounds)))
            if (volume_error > RELATIVE_TOLERANCE or area_error > RELATIVE_TOLERANCE
                    or bounds_error > BOUNDS_TOLERANCE):
                raise ValueError(f'{name}, component {index}: geometry changed')
            solids.append(obj)
            details.append({
                'component': index, 'triangles': len(component.faces),
                'volume_mesh': float(component.volume), 'volume_step': float(obj.Volume()),
                'surface_area_mesh': float(component.area), 'area_step': float(obj.Area()),
                'valid': True, 'closed': True, 'bounds_mesh': component.bounds.tolist(),
            })
        compound = cq.Compound.makeCompound(solids)
        destination = ROOT / 'models/step' / (source.stem + '.step')
        status = compound.exportStep(str(destination), unit='MM', outputUnit='MM', write_pcurves=False)
        if status != IFSelect_RetDone:
            raise ValueError(f'{name}: STEP export failed')
        imported = cq.importers.importStep(str(destination)).val()
        final_solids = imported.Solids()
        bounds_error = float(np.max(np.abs(np.asarray(bounds(imported)) - mesh.bounds)))
        target_volume = sum(abs(c.volume) for c in components)
        volume_error = abs(sum(s.Volume() for s in final_solids) - target_volume) / max(target_volume, 1.)
        area_error = abs(imported.Area() - mesh.area) / max(mesh.area, 1.)
        if (not imported.isValid() or len(final_solids) != len(solids)
                or len(imported.Faces()) != len(mesh.faces)
                or bounds_error > BOUNDS_TOLERANCE
                or volume_error > RELATIVE_TOLERANCE or area_error > RELATIVE_TOLERANCE):
            raise ValueError(f'{name}: STEP reimport did not preserve valid geometry')
        if digest(source) != before:
            raise ValueError(f'{name}: source changed during conversion')
        records.append({
            'stl': 'models/stl/' + name, 'step': 'models/step/' + destination.name,
            'source_sha256': before, 'step_sha256': digest(destination),
            'source_bytes': source.stat().st_size, 'step_bytes': destination.stat().st_size,
            'source_triangles': len(mesh.faces), 'source_vertices': len(mesh.vertices),
            'mesh_watertight': bool(mesh.is_watertight),
            'mesh_winding_consistent': bool(mesh.is_winding_consistent),
            'source_bounds': mesh.bounds.tolist(), 'extents': mesh.extents.tolist(),
            'disconnected_components': len(components), 'step_solids': len(final_solids),
            'step_faces': len(imported.Faces()), 'step_valid': True,
            'roundtrip_max_bounds_difference_mm': bounds_error,
            'roundtrip_relative_volume_difference': volume_error,
            'roundtrip_relative_area_difference': area_error, 'component_checks': details,
        })
        print(f'PASS: {name}: {len(mesh.faces)} facets, {len(final_solids)} valid STEP solids', flush=True)
    report = {
        'schema': 'seizo-nexus-mesh-step-validation/v1',
        'source_batch_date': manifest['batch_date'],
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'units': manifest['unit_assumption'],
        'conversion': 'One planar face per source triangle, sewn into closed shells and oriented solids; components not fused',
        'source_files_byte_preserved': True, 'original_coordinates_preserved': True,
        'decimation': False, 'hole_filling': False, 'parametric_history_recovered': False,
        'sewing_tolerance_mm': SEW_TOLERANCE, 'bounds_check_tolerance_mm': BOUNDS_TOLERANCE,
        'relative_volume_area_tolerance': RELATIVE_TOLERANCE,
        'versions': {name: importlib.metadata.version(name) for name in
                     ('cadquery', 'cadquery-ocp', 'trimesh', 'numpy')},
        'not_checked': ['Physical fit, loads and strength', 'Print orientation, supports and wall suitability',
                        'Electrical safety and heat clearance', 'Inter-component interference and duplicates',
                        'Original design intent, units, part names and assembly completeness'],
        'files': records,
    }
    (ROOT / 'docs/geometry-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('All four source files preserved; four STEP files reopened and validated.', flush=True)


if __name__ == '__main__':
    main()
