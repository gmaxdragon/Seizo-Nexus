# Build notes and validation boundary

This is a preparation guide for the current CAD batch, not a tested assembly manual.

## Preserve the intended dimensions

Use one STL unit as one millimetre only after checking that interpretation against the intended object dimensions. The STEP files encode that assumption explicitly. No conversion scaling was applied. Do not use a slicer's automatic shrink-to-fit without considering the resulting changes to dovetails, sliding interfaces, and hardware fit.

The file bounding boxes include original export placement and all disconnected components. Export 02 spans about 261 by 263.4 mm in XY; Export 03 spans about 270.163 mm in Y. Confirm printer capacity and orientation. Separating disconnected bodies is different from cutting a single connected body. Export 02 contains one connected component, not a ready-separated set of small parts.

## Inspect before committing to a full print

Identify the purpose of each body using the original CAD project. Preview every layer in the slicer. Check thin features, support removal, overhangs, small holes, flat bearing surfaces, disconnected islands, and any overlap between bodies. A watertight mesh can still contain geometry that is inconvenient or unsuitable to print.

Test one mating interface first, then verify drawer/cover travel and connection fit. The source journal notes that glue may be needed in some places, but no validated gluing procedure is supplied. Do not glue sliding, pivoting, or removable interfaces before understanding their role.

Material, nozzle size, layer height, perimeters, infill, supports, and clearances need to be selected and tested for the particular printer and load. No universal settings are claimed here.

## Provisional assembly order

After checking the original part identities, test the base connection, then the storage enclosure and its sliding parts. Check the scissor mechanism unloaded and away from fingers. Add holders, covers, labels, and logo elements only after the main connections fit. Load the workstation gradually while checking stability and flex. These are general checks, not evidence that an assembly has already passed them.

## Power-strip holder boundary

The compact holder is intended to hold an already enclosed commercial power strip. It is not a replacement mains enclosure. Do not open or rewire the strip, crush cables, conceal damaged cords, block required ventilation, or make the power switch inaccessible. Verify the holder fits without putting stress on sockets or plugged-in cables.

## Information not yet supplied

- A complete part-name and quantity map for every feature shown in the screenshot.
- Original native CAD or a designer-exported STEP assembly with semantic part names.
- Measured fit clearances and physical build results.
- Tested loads, material settings, assembly hardware, and a complete BOM.
- Exact attribution and licensing for reused source models.

The four converted STEP files and the original STLs remain useful without claiming these missing items are complete. Digital results are recorded separately in [geometry-validation.json](geometry-validation.json).
