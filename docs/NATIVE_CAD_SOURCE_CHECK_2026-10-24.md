# Seizo Nexus: native editable CAD source check

**24 October 2026: THIS REQUIREMENT IS NOT PASSED.** The repository has four original STL files and four faceted STEP conversions. These STEP files can be imported and edited directly to a limited extent, but they are not the original Tinkercad editable model, Fusion .f3d/.f3z, or public Onshape source.

## Exact source needed

The owner's Half-Life checker asks for either a genuine Fusion .f3d/.f3z archive or an actual public Onshape source document URL placed in the Half-Life **description or demo URL**. A neutral STEP alone is insufficient. Do not put an Onshape URL in the GitHub repo URL field.

## Owner's shortest legitimate repair

1. Sign into the original Tinkercad account and open the genuine Seizo Nexus editable design, not the STL/STEP exports.
2. If Tinkercad offers Send to Fusion, transfer and open that original design in Autodesk Fusion. Verify component geometry and ability to edit. Export a **real Fusion Archive** (.f3d or .f3z as appropriate) from the actual application. Do not rename any STEP file.
3. Commit the genuine archive into models/native/ in this repository; keep the existing STL and STEP files. Download the archive back from GitHub and confirm that Fusion opens it.
4. Alternative: create a real Onshape document with the relevant geometry, make it public, and verify it is visible when logged out. Any imported mesh/faceted surfaces and newly made features must be disclosed. Enter the real Onshape link in Half-Life's project description or demo URL.
5. Rerun the Half-Life checker, confirm its CAD-source flag passes, and review attribution for any third-party geometry.

## Evidence boundary

Neither the main branch nor the earlier CAD release branch contains an actual source-format archive or public Onshape URL. The connected tools cannot log into the owner's original Tinkercad/Fusion/Onshape account. It would be inaccurate to claim the checker has been fixed by converting or renaming STL/STEP files.

Reference: https://cad.onshape.com/help/Content/Collaboration/share_documents.htm
