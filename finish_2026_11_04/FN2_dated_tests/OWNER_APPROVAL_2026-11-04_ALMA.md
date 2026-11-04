# Owner approval, 2026-11-04: stream the two ALMA cubes after release and score them

Recorded at the owner's instruction, given in chat on 2026-11-04 in answer to: "Approve streaming the two ALMA cubes on release day to score them?" The owner chose "Approve ALMA download". The approval text named the files and sizes:

> Yes: after the 2026-11-06 02:42:31 UTC release, stream the two ALMA cubes for MOUS uid://A001/X3788/Xbfd2 (spw25, 34,749,031,680 bytes; spw23, 38,556,031,680 bytes), keep only the cutouts, and score them with the FN2 release-day runbook.

kappa = 1/2 FITTED. Not theory closed. One disc excludes no model.

## Approved
| file | source | bytes | kept |
|---|---|---|---|
| `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits` | `https://almascience.eso.org/dataPortal/` (or its NRAO or NAOJ mirror) | 34,749,031,680 | the +-4.5 arcsec cutout of U4_28473 only, 0.28-0.83 GB |
| `member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw23.cube.I.pbcor.fits` | same | 38,556,031,680 | the +-13 arcsec cutout of U4_27928 only, 2.55-7.62 GB |

Streamed through `rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_stream_cutout.py`; the full cubes are never stored. Scored and recorded by `RELEASE_DAY_RUNBOOK.md` steps 4-9.

## Not covered by this approval
- A file whose size differs from the listing above: it goes back to the owner as a new size first.
- The `.pb.fits.gz` files, the 193.5 GB product tar, and the archive's SODA cutout service.
- GS4_24110's files (2026-11-28): they need their own yes.
- Any deposit, including a PAPER66 v1.5 with the filled scorecard, and sending anything outside.
