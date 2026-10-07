# CFG413 FROZEN CRITERIA: how far out must the law be ON for KiDS-1000 (two-halo modelled), and how much growth excess lies beyond that radius?
(committed alone, before any script; light CPU, nice 15, one thread; no PM run; no downloads)

**Why.** CFG352 put the switch edge at 0.23 r_ta and found KiDS d chi2 +169 / +163. Its KiDS scorer
(FP1 `kfit(..., W0, Amax = 0.0)`) has the two-halo amplitude fixed at ZERO, so that number has no two-halo term.
CFG377 showed that the isolated-lens stack beyond ~0.3 Mpc/h is two-halo dominated and that a free R^-0.8 amplitude
moves chi2 from 325 / 261 to 9.7 / 11.9 (/15). CFG412: ~80% of T1's l3 < 0 ON mass lies inside resolved-host
turnaround spheres, so an ON-to-r_ta switch removes at most ~13-19%. This lane asks whether a smaller ON radius,
honestly tested against KiDS with a free two-halo term, opens room for growth.

## Grid (declared)
x in {0.23, 0.3, 0.4, 0.5, 0.7, 1.0}; r_on = x * r_ta, r_ta = cfg100_lib's r_ta_law(M_gal, a0, z_lens) (the record's
r_ta, Delta_ta(z) from the Lambda spherical-collapse table). Both footings a0 = 9.3603e-11 and 1.1312e-10, never
pooled. kappa = 1/2 is FITTED. The cold mass is still required; no particle species.

## (1) KiDS leg (script `cfg413_kids.py`)
- Data, stacking, grouping, covariance: exactly CFG377's primary stack (KiDS-1000 isolated lenses, 15 g_bar bins,
  per-lens sums `cfg110_perlens.npz`, 50-patch leave-one-out jackknife, Hartlap factor).
- Model per lens group: CFG377's BARE law (CFG100 v_law: M_d(r) = M_gal (nu_mono(y) - 1), shell projector
  `dsigma`, M_d frozen beyond the last radius), with the truncation radius r_e = x * r_ta instead of 0.4 r_ta
  (x = 0.4 reproduces CFG377's BARE exactly; check K1). Plus a FREE two-halo amplitude A times CFG377's pair-averaged
  (R / 1 Mpc)^-0.8 template, profiled analytically (unconstrained in sign, exactly as CFG377).
- chi2(x) per footing; Delta chi2(x) = chi2(x) - chi2(x = 1).
- x_min = the smallest grid x with Delta chi2 <= 4, per footing.
- Robustness: repeat with each one of the 15 bins dropped (covariance sub-matrix, Hartlap for 14 bins); report
  x_min per drop and the largest.
- Reported only (no verdict weight): the same with A >= 0 enforced; with no two-halo term (A = 0, CFG352-like);
  the strict-isolation f30 subset; the bins with mean R <= 0.3/h Mpc only (Brouwer+21's trusted range).
- "Cannot distinguish": if Delta chi2 <= 4 for every grid x on both footings, the README says the data cannot
  distinguish x, and states why (radial reach / two-halo degeneracy / errors), with the numbers.

## (2) Growth leg (script `cfg413_growth.py`)
- Input: CFG410 BASE z0 snapshots `../_external_data/cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_{canonical,alt}_N256_z0.npz`
  (read-only), re-deposited at 256^3 with CFG412's `cfg412_screen` functions (imported read-only).
- Fields as CFG412's PM leg: T1 switch fT1 = smear(l2), l3 sign, and the RES excess source exc = max(s_ph - s_c, 0).
- Peaks and turnaround radii: CFG412's turnaround-cover machinery (3x3x3 local maxima with delta >= 3(tau - eps);
  first-crossing ON radius r_ta,c of each peak). "Resolved" = r_ta,c >= 2 cells (1.56 Mpc/h), CFG412-D2's definition.
- For each x: IN(x) = union over resolved peaks of the balls |cell - c| <= x * r_ta,c (periodic); BEYOND = not IN.
- Gate quantity S(x) = sum(fT1 * exc * BEYOND) / sum(fT1 * exc): the share of the T1-weighted RES excess source
  lying beyond x * r_ta of every resolved peak.
- Also: S_fil(x) (same, restricted to l3 < 0 cells), Xhat(x) = X_CFG410 * S_fil(x) (CFG412's estimate of the
  removable share of the P(k = 1) excess; X_CFG410 = 0.89 / 0.86; labelled an ESTIMATE), and the T1-ON mass share
  beyond. Sensitivity (reported only): resolved threshold 1 cell and 3 cells.

## Checks (can fail)
- K1: at x = 0.4 the KiDS BARE chi2 with the profiled two-halo term reproduces CFG377's 9.7 / 11.9 (to 0.05).
- K2: CFG377's no-two-halo BARE chi2 325.49 / 261.19 reproduces at x = 0.4 with A = 0 (to 0.05).
- K3: at x = 1 the T1-ON, l3 < 0 MASS share inside resolved balls reproduces CFG412-D2's 0.805 / 0.811 (to 0.01).
- K4: S(x) and S_fil(x) are non-increasing in x (both footings).
- K5: the re-computed T1 agrees with the stored f (>= 0.995 of cells).

## MUTATE (CFG413_MUTATE=1, separate outputs `*_MUTATE.*`)
x = 0.05 (law almost entirely off) added against the x = 1 reference. KiDS must FAIL: Delta chi2 > 4 on both
footings with the free two-halo term. If it does not, MUTATE is NOT DETECTED and the KiDS leg cannot discriminate.

## Verdict (declared now; per footing, the lane verdict needs both)
- **DOOR OPEN**: some grid x has KiDS Delta chi2 <= 4 AND S(x) >= 0.60, on both footings, AND that x also passes
  Delta chi2 <= 4 in all 15 drop-one-bin variants. Then the README specifies (does NOT run) the confirming PM run:
  a CFG410-style RES + MIX-A run with the switch multiplied by IN(x) around peaks.
- **PARTIAL**: not OPEN, but some grid x has Delta chi2 <= 4 AND S(x) >= 0.30 on both footings (or the OPEN pair
  fails only the drop-one-bin robustness).
- **CLOSED**: otherwise.

## Caveats declared in advance
- KiDS lenses (log M_b ~ 10-11, r_ta ~ 1 Mpc) are below the 0.78 Mpc/h mesh; the growth leg's resolved peaks are
  group/cluster hosts. Unresolved galaxy hosts inside BEYOND cells would also need the law ON, so S(x) is an UPPER
  bound on the removable share at fixed x.
- The KiDS constraint is set on isolated galaxies; applying x to group-scale peaks assumes the ON fraction of r_ta
  is mass-independent.
- Xhat is a linear-response estimate, not a PM result; one 256^3 snapshot per footing at z = 0 (CFG411b: the excess
  grows with resolution).
- Never "theory closed"; never "the data favour the framework".
