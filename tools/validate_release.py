"""Independently validate checked-in originals, STEP geometry, image and doc links.

Read-only for project files. The optional --record flag writes a release evidence
JSON in the repository root, without changing CAD files or their conversion report.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import unquote, urlsplit
import numpy as np
import trimesh
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / 'tools/source-manifest.json').read_text())
    report = json.loads((ROOT / 'docs/geometry-validation.json').read_text())
    assert len(manifest['files']) == len(report['files']) == 4
    assert {p.name for p in (ROOT/'models/stl').glob('*.stl')} == {x['name'] for x in manifest['files']}
    assert {p.stem for p in (ROOT/'models/step').glob('*.step')} == {Path(x['name']).stem for x in manifest['files']}
    results = []
    for item, record in zip(manifest['files'], report['files']):
        source = ROOT/'models/stl'/item['name']
        destination = ROOT/'models/step'/(source.stem+'.step')
        assert source.stat().st_size == item['bytes'] and sha(source) == item['sha256'] == record['source_sha256']
        assert record['stl'] == source.relative_to(ROOT).as_posix()
        assert record['step'] == destination.relative_to(ROOT).as_posix()
        assert sha(destination) == record['step_sha256']
        mesh = trimesh.load_mesh(source, process=False)
        mesh.merge_vertices(digits_vertex=12)
        components = mesh.split(only_watertight=False)
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert len(mesh.faces) == item['triangles'] and len(components) == item['components']
        shape = cq.importers.importStep(str(destination)).val()
        solids = shape.Solids()
        assert shape.isValid() and len(solids) == item['components']
        assert len(shape.Faces()) == item['triangles']
        box = shape.BoundingBox()
        imported_bounds = np.array([[box.xmin,box.ymin,box.zmin],[box.xmax,box.ymax,box.zmax]])
        assert float(np.max(abs(imported_bounds-mesh.bounds))) <= 1e-5
        volume = sum(abs(x.volume) for x in components)
        assert abs(sum(x.Volume() for x in solids)-volume)/max(volume,1.) <= 1e-8
        assert abs(shape.Area()-mesh.area)/max(mesh.area,1.) <= 1e-8
        results.append({'file':item['name'], 'solids':len(solids), 'faces':len(shape.Faces()), 'valid':True})
    image = manifest['screenshot']
    path = ROOT/image['path']
    assert sha(path) == image['sha256'] and path.stat().st_size == image['bytes']
    assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    checked_links = 0
    for relative in ('README.md','ATTRIBUTION.md','docs/BUILD_NOTES.md','docs/STEP_CONVERSION.md'):
        doc = ROOT/relative
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', doc.read_text(encoding='utf-8')):
            if target.startswith('#') or urlsplit(target).scheme:
                continue
            target = unquote(urlsplit(target).path)
            assert (doc.parent/target).resolve().is_relative_to(ROOT)
            assert (doc.parent/target).exists(), f'Broken internal link: {relative} -> {target}'
            checked_links += 1
    assert sum(x['solids'] for x in results) == 12
    assert sum(x['faces'] for x in results) == 4274
    result = {'schema':'seizo-nexus-package-check/v1', 'result':'pass', 'original_stl_files':4,
              'step_files':4, 'valid_step_solids':12, 'source_triangles':4274,
              'original_screenshot_verified':True, 'internal_links_checked':checked_links,
              'physical_fit_verified':False, 'parametric_history_recovered':False,
              'units':'1 STL coordinate unit = 1 mm is an assumption', 'checks':results,
              'files':{p.relative_to(ROOT).as_posix():sha(p) for directory in ('models','docs')
                       for p in sorted((ROOT/directory).rglob('*')) if p.is_file()}}
    if '--record' in sys.argv:
        (ROOT/'package-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
