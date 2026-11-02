# VS3_second_tracer: FROZEN CRITERIA, committed alone before any script

Owner's go, 2026-11-02: "settle it then", after VS2 read UNDECIDED. **Not blind:** VS1 and VS2 results are known, and CFG492's README was opened far enough to show that NGC 3608 and 4564 are PN-only rows and the start of a PN value. kappa = 1/2 FITTED. Footings never pooled. Reinstates nothing; cold sector stays retired. Not theory closed. Nothing here says the data favour the framework.

## Question
Do slow rotators that are not group centrals show the outer excess in a second tracer (planetary nebulae), or does the excess go with being central?

## What this lane cannot do, stated first
**SETTLED needs at least 4 distinct slow non-centrals with an outer tracer and a JAM anchor. The disk holds at most 2: NGC 4374 and NGC 3608. So this lane cannot return SETTLED.** Its strongest label is a lean. The number 4 comes from about 0.08 dex galaxy scatter (VS1, VS2): 0.08/sqrt(4) = 0.04 dex, so a +0.12 dex excess is 3 sigma.

## Data, no download
Committed CFG492 per-galaxy offsets, code path unchanged, nu_mono, both footings: GC and PN offsets from `cfg492_gc_vs_pn_results.json`. Control from its `_MUTATE_results.json`. Rotator class: Emsellem+11 on disk. Central: VS2's rule and primary window, 500 kpc and 500 km/s, on 2MRS. Other windows reported, not graded. NGC 3608's JAM quality is 0, below the quality >= 1 used elsewhere: its row is kept, flagged, and reported with its mass moved by +-0.1 dex using the local slope of offset on mass as a rough estimate.

## Statistic
For tracer T in (PN, GC): reference = mean offset of fast non-centrals in T, error = larger of scatter/sqrt(N) and inverse-variance bootstrap error. Contrast for each slow non-central = its offset minus the reference, error = its bootstrap error combined with the reference error. Slow centrals and fast centrals against the same reference are reported.

## Labels, each footing, same on both or FOOTING-DEPENDENT
- **LEANS ROTATION:** PN rows of NGC 3608 and NGC 4374 both have contrast >= +0.10 dex, and their mean contrast is above 0 at > 2 sigma.
- **LEANS ENVIRONMENT:** both PN contrasts within 1 sigma of 0, and slow centrals' mean PN contrast >= +0.10 dex at > 2 sigma.
- **UNDECIDED** otherwise, including a window that removes either galaxy from the slow non-centrals at primary. The label is never SETTLED.

## Controls
MUTATE: the same statistic on CFG492's shuffled PN-galaxy pairing must not return LEANS ROTATION on both footings. If it does, the lane reads NO VERDICT. Outputs named by mode.

## Reported limits
Isotropic Jeans; beta = 0 for PNe, and PN samples in massive ellipticals are known to be anisotropy-sensitive. Two objects. A lean is not a detection, an offset is not a halo, and no mechanism is tested.
