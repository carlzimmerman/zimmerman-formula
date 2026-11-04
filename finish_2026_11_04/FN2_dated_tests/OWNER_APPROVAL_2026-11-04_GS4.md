# Owner approval, 2026-11-04: GS4_24110 [CI](2-1) cube after its 2026-11-28 release

Recorded at the owner's instruction. On 2026-11-04 the owner answered "yeah do all this" to a status that listed, among the downloads waiting on the owner, "the GS4 cube (7.0 GB, for November 28)". kappa = 1/2 FITTED. Not theory closed. One disc excludes no model.

Release: 2026-11-28 18:25:24 UTC (13:25:24 US Eastern). MOUS uid://A001/X3845/X3a, programme 2025.1.01377.L, target Pointing-F (0.42 arcsec from GS4_24110). Source: `https://almascience.eso.org/dataPortal/` (or its NRAO or NAOJ mirror).

| file | bytes | status |
|---|---|---|
| `member.uid___A001_X3845_X3a.Pointing-F_sci.spw31.cube.I.pbcor.fits` | 7,018,934,400 | APPROVED |
| `member.uid___A001_X3845_X3a.Pointing-F_sci.spw25_27_29_31.cont.I.pbcor.fits` | 14,777,280 | AWAITING OWNER |

The continuum image wasn't named in the owner's yes. The frozen harness (`campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_gs4.py --cube ... --cont ...`) needs it, so it is listed here for its own yes. `fn2_gs4_release_day.sh` downloads nothing until both rows read APPROVED.

## Known limit, from FN2 (`README.md`, part B)
The frozen MUTATE cannot run on this window: +2000 km/s and the clarified +1000 fallback both lie wholly outside spw31, so the harness exits 2 and the run has no MUTATE control (CFG809 addendum A section 2). A substitute control would need a dated owner addendum before 2026-11-28 18:25:24 UTC. Every n = 1 against n = 2 pair is at or below 0.51 sigma, so this release can't separate them.

## Not covered
A file whose size differs from the table (back to the owner first); any other product of this MOUS; any deposit; sending anything outside.
