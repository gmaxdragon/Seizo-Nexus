# Seizo Nexus: independent CAD recheck

Checked October 16, 2026, Pacific time. Owner: Vivaan Goel.

## Result

All four original STL files and all four matching STEP files are already published on main. This recheck examined the actual model geometry rather than relying only on the earlier README or a successful workflow badge. No original model was resized, repaired, fused or overwritten.

Source snapshot inspected: `27b627f1142888159ac3abc43f06a5b726c19a7c`.

- Every local STL and STEP used in this check matched its current GitHub Git blob hash.
- Each STL also matched the original conversation upload byte-for-byte.
- The repository screenshot matched the original uploaded PNG byte-for-byte.
- Reran `python tools/validate_release.py --record`: passed. Four STEP files reopened as 12 valid solids with 4,274 faces in total. The original bounds, volume and surface area passed the existing conversion tolerances. The 25 internal links in the packaged initial documentation were checked; the later BOM changes were not part of that local link-count check.
- Rendered and visually inspected all four STL exports individually. These views are inspection aids, not extra design files or photographs of printed objects.
- Checked component bounding boxes within each export. No pair has positive-volume bounding-box overlap above the 0.000001 mm comparison tolerance. Six component pairs in export (2) have face-plane contact at Z=7. This is a check of the exported layout, not clearance testing of an assembled, moving mechanism.

Verdict: valid geometry and faithful conversion; suitable to open and inspect in CAD/slicer software. Not certified as a complete, physically tested print-and-assemble kit.

## Findings that matter before printing

| File | Connected source components | Finding |
| --- | ---: | --- |
| `Seizo Nexus.stl` | 1 | Enclosure-shaped connected body, approximately 200.000 x 200.038 x 138.397 coordinate units. Confirm orientation/supports before printing. |
| `Seizo Nexus (1).stl` | 1 | Connected frame, approximately 261.000 x 263.400 x 17.000 units. Too wide for an axis-aligned 256 x 256 layout. It cannot be separated into smaller objects merely by splitting disconnected components, because it has only one. |
| `Seizo Nexus (2).stl` | 8 | The overall layout spans about 270.163 units in Y. The largest body is approximately 174.382 x 201.845 x 99.000. There is a separate 72.5 x 23 x 7 body plus six small detail bodies. Those details occupy Z=7..11 while the 7-unit-high body's bounding box ends at Z=7. Do not automatically separate and drop every mesh shell to the bed: raised details may need to stay registered to that body. Their intended bonding or multicolour treatment remains to be checked in the original design and slicer. |
| `Seizo Nexus (3).stl` | 2 | Largest body approximately 200.001 x 145.179 x 112.100 units; smaller body approximately 57 x 11.387 x 30. Their bounding boxes are separated by at least 0.613 units in the current layout. This is not a measured assembled fit clearance. |

All millimetre interpretations still assume one STL coordinate unit equals one millimetre. STEP is explicitly written in millimetres using that assumption. No physical unit measurement was supplied.

The smallest detail in export (2) is approximately 1.982 x 1.719 x 4 units. Check its layer preview and attachment carefully. Eight mesh components do not necessarily mean eight standalone prints; some are raised details of one intended item. This is why the original names and body placement were preserved rather than automatically splitting or joining everything.

An attempted exact nearest-surface-distance pass exceeded its aggregate 45-second inspection budget and was not used to certify clearance. Only the completed bounding-box comparison is claimed above. No inter-file assembled collision sweep, minimum-wall certification, print-orientation optimization or physical fit/load test was performed.

## Purchase intent

Vivaan confirmed he will buy PLA and already knows the supplier. No further supplier recommendation is needed. Exact quantity, spool specification and price were not provided, so those BOM values remain pending rather than guessed. This does not add paid printing or finished modules.

## Next physical check

Inspect the intended print layout in the actual printer's slicer at the preserved scale. In particular, keep export (2)'s small raised details aligned with their supporting body. Test a mating connector before printing the entire system. The original editable design or a measured fit test is needed before changing mating geometry confidently.

[STL downloads](../models/stl) | [STEP downloads](../models/step) | [Conversion report](geometry-validation.json) | [Build notes](BUILD_NOTES.md)
