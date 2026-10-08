# CFG450 FROZEN CRITERIA: at what radius does the CFG382 target audit read the X-COP gas mass, and do the definition-A deficits move?

Frozen before any CFG450 script exists. kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10, as in
CFG431) are reported separately, never pooled. No dark-matter particle; the cold fluid's mass is still required. Read-only on
CFG382, CFG431 and deepseek_push (T15, T16): no file there is edited.

## The question
`cfg382_target_audit.py` reads the X-COP gas mass as `exp(interp(0.0, log RADIUS, log MGAS))`, i.e. at RADIUS = 1 in the
file's own unit, while the hydrostatic mass is read at R500 (kpc). CFG431 (README, robustness row R2) states that this is
"M_gas at 1 Mpc" and re-reads the gas at `log(R500_kpc / 1000)`. Which reading is correct decides whether the cluster
deficits 0.413 (b = 0) / 0.905 (b = 0.3) that T15, T16 and CFG431 inherit are biased.

## Gates (decided only from the FITS headers and the profiles on disk, real_research/data/xcop/)
- **U1 (units).** For all 12 `*_fgas_profile.fits` files, extension FGAS: the RADIUS column unit (TUNIT1) is read.
  - If it is `R/R500` for all 12, and the header keyword R500 (kpc) is within 2% of `xcop_r500_ettori2019.json` for all 12,
    then `interp(0.0, log RADIUS, ...)` reads the gas at R500 (header normalisation) -> **NOT A BUG** branch.
  - If it is Mpc (or kpc) for any file used, -> **BUG** branch.
  - Anything else (missing unit, mixed units) -> **UNDETERMINED**, stop and report.
- **U2 (cross-check, must pass for the NOT A BUG verdict to stand).** For all 12: the NFW total mass in the fgas file at
  RADIUS = 1 agrees with the hydro file's M_NFW interpolated at the JSON R500 (kpc) to within 2%, and the gas fraction at
  RADIUS = 1 lies in [0.08, 0.20] (the usual f_gas,500 range). If U2 fails, the verdict is UNDETERMINED.

## Recompute (both branches)
Gas mass at the JSON R500 exactly: RADIUS = R500_json / R500_header in the R/R500 unit (or R500 in the file's length unit if
U1 says length). Hydrostatic mass, stellar mass, sample (the 7 clusters with stellar profiles), definition A, kernel nu_mono,
cosmic share 5.364 exactly as cfg382_target_audit.py. Reported: median and 16-84% for clusters and for the 20 Lovisari groups
(groups have no gas-radius issue; recomputed only to give T15/T16 both footings), for b = 0 and b = 0.3, at each footing.
- **Movement threshold (decision).** A cluster median moving by more than 0.02 (absolute, at either b, canonical footing)
  from 0.413 / 0.905 = **MOVES**; otherwise **UNCHANGED**.

## Propagation (reported, not re-verdicted)
- **T15.** Re-evaluate its cluster and group quantities with the new deficits, holding all its other conventions fixed
  (a0 = 1.2e-10 in the kernel supply S, f_law 0.286, lambda 0.028): C2 M_cold/M_b rows, C3 f_max and lambda_max, C4 f_res,
  C5 violation factor. A second, labelled row recomputes S at the matching footing's a0 (T15/T16 use 1.2e-10, neither
  footing; this is disclosed, not corrected in place).
- **T16.** Same substitution: the group and cluster lambda_max windows, the three-way intersection, the floor-vs-cluster gap.
- **CFG431.** (a) Primary cluster e_med and S at canonical with gas at R500 (must equal the primary if UNCHANGED);
  (b) R1-full: groups AND clusters at the alt footing too (CFG431's R1 moved only the galaxies); (c) the effective radius
  CFG431's R2 actually read, in units of R500, per cluster, and its e_med. If U1 gives R/R500, R2 read the gas OUTSIDE R500
  and is reported as invalid (its premise is wrong). CFG431's estimator (S_of, bootstrap NB 4000, seed 431) is copied verbatim.

## Controls
- **C1 (reproduction).** With the CFG382 read, canonical: clusters 0.413 / 0.905 and groups 0.787 / 1.760 (b = 0 / 0.3) to 0.002.
- **C2 (CFG431 R2 reproduction).** CFG431's R2 read gives its cluster e_med 0.225 to 0.002.
- **C3 (T15/T16 reproduction).** With the original inputs (0.41/0.91, 0.79/1.76), the copied T15/T16 formulas reproduce the
  committed t15_results.json rows/ceil/res/viol and t16_results.json others/windows/inter/gap to 1e-9.
- **MUTATE (CFG450_MUTATE=1).** Plant the wrong-unit read: treat RADIUS as Mpc (gas at RADIUS = R500_json in Mpc). The
  movement decision must flip to MOVES. Outputs go to *_MUTATE files.

A failed control is reported and kept, never silently fixed.
