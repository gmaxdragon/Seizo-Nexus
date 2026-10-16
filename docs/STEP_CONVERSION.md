# STL to STEP conversion and checks

## Inputs and output identity

The four source filenames and their byte hashes are fixed in [source-manifest.json](../tools/source-manifest.json). Original source STL files are retained unchanged under models/stl. Each output under models/step has the same filename stem with a .step extension.

The only unit assumption is **one source STL coordinate unit equals one millimetre**. Numeric coordinates and global placement are retained. STL inputs do not independently establish that physical unit choice.

## Method

The converter loads each mesh without automatic mesh repair. Coincident vertices are merged for topology analysis at 12 decimal digits. It rejects non-finite coordinates, degenerate triangles, open meshes, or inconsistent winding.

For each connected component, it creates one planar CAD face per original triangle and sews the faces with a 0.0000001 mm tolerance. It requires one closed shell, constructs an oriented solid, and checks the result with the Open CASCADE boundary-representation validator. Multiple components are collected in a compound. They are not Boolean-unioned.

No decimation, smoothing, hole filling, rescaling, recentering, assembly repositioning, or analytic curve fitting is performed. A negative orientation, if encountered, is corrected at solid orientation rather than by changing the geometric surface.

STEP files are exported with millimetre units and then independently reopened. The code checks validity, the number of solids and faces, all six bounding-box coordinates, surface area, and volume. Bounds must agree within 0.00001 mm; relative surface-area and volume differences must be at most 0.00000001. These numerical tolerances concern the digital conversion, not achievable printer accuracy.

The batch contains 1,046, 624, 1,854, and 750 triangles respectively. It converts to 1, 1, 8, and 2 solids. Detailed per-component evidence and output SHA256 hashes are in [geometry-validation.json](geometry-validation.json).

## What this does not recover

These are faceted B-rep STEP solids derived from tessellated STL surfaces. They do not recover native sketches, feature history, dimensions, constraints, assembly mates, part names, or exact smooth cylinders and arcs. The STEP format can carry CAD geometry, but converting a triangulated surface does not recreate the source author's modeling operations.

A valid CAD solid is not proof of printable clearances, absence of inter-component interference, adequate wall thickness, mechanical strength, or physical safety. Those checks are outside this conversion report.

## Reproduce

Use Python 3.13 in a virtual environment and install the pinned conversion dependencies:

```sh
python -m pip install -r tools/requirements-cad.txt
python tools/convert_stl_to_step.py
python tools/validate_release.py
```

Run these commands from the repository root. Conversion regenerates models/step and docs/geometry-validation.json but never edits source STLs. STEP header timestamps can change the byte checksum on regeneration even when geometry is unchanged; rerun the report and checks together. Validation alone reads the checked-in outputs without regenerating them.

The dependency versions and Open CASCADE checks are recorded in the report. The package workflow also verifies the original screenshot hash and every internal Markdown file/image link before publishing the candidate.

## References

- [CadQuery import and export documentation](https://cadquery.readthedocs.io/en/latest/importexport.html).
- [Open CASCADE sewing API](https://dev.opencascade.org/doc/refman/html/class_b_rep_builder_a_p_i___sewing.html).

These describe the libraries. The accompanying execution report establishes what was checked on these particular files.
