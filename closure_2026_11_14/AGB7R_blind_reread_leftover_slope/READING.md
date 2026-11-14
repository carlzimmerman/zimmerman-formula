# AGB7R — blind re-grade of AGB7: reading of the frozen rules (written before any run)

2026-11-14. Second, independent implementation of lane AGB7 (CFG684 and CFG689 re-read with the age slope left in
the DES distances). The only file of the lane read is its `FROZEN_CRITERIA.md`. Read besides, as the criteria and
the brief allow: AGB1's harness `agb1_reread.py` (for the exact text substitutions) and template `agb1_template.py`;
the lane sources `cfg684_robust.py` and `cfg689_native_ruler.py` and `cfg684_results.json`; the key names and the
structure (not the numbers) of LGS1's `lgs1_cfg684_<sample>.json` and `lgs1_cfg689_<mode>_<sample>.json`; the
`curves` entries `full_sfr` and `des_only_sfr` of AGB3's `agb3_S.json`. AGB1's two A = 1 files are opened only by
the H2 and H3 check code. No AGB7 script, output, README or commit diff has been opened.

## What is run (as I read it)
- The lane sources are executed unchanged apart from exact text substitutions, each asserted to occur exactly once:
  the supernova mask becomes `(dz > 0) & sample`, the moduli become `dmu − A × T(zHD)` (applied to every supernova
  before the mask; the covariance is not touched), the output paths go to this folder, and (CFG684 only) the list of
  combinations becomes `BAO+DES5+CC`, `BAO+DES5`. Each combination is fitted on its own, so dropping the other five
  cannot change its numbers; H1 tests exactly that.
- Samples: `full` = every supernova the lanes keep (zHD > 0); `des_only` = IDSURVEY == 10 only.
- Templates: **T_S** is AGB1's `agb1_template.T(z, "S")`, imported unchanged (the criteria name AGB1's T_S, and H2
  needs the same code path to 1e-9). **T_H** is built from AGB3's curve for the sample (`full_sfr` for `full`,
  `des_only_sfr` for `des_only`): T_H(z) = 0.030 mag/Gyr × [age(z_1) − age(z)], with age(z) the bin mean host age
  linearly interpolated in zHD between bin redshifts and held constant beyond the first and last bins (z_1 is the
  first bin). Ambiguity resolved: the criteria give no interpolation and no zero point. The zero point cannot matter
  (both lanes profile a constant magnitude offset analytically); the interpolation is my choice and T_H is
  reported only, so no label rests on it.
- Runs at the frozen 60,000 steps and seeds (CFG689_NSTEP not set). CFG684: `full` and `des_only` at A = 0.23 and
  0.35 with T_S, 0.35 with T_H; `full` at A = 0 (H1) and A = 1 with T_S (H2). CFG689: modes D5 and TD5F, both
  samples, A = 0.23 and 0.35 with T_S; TD5F `des_only` at A = 1 with T_S (H3). CFG689 with `CFG689_PARALLEL=1`,
  at most three at once; CFG684 one after another; BLAS threads 2. Exit code 75 = NOT RUN, recorded, guard untouched.
- Extra, reported only: my own A = 1 runs for the sample/mode pairs the checks do not cover (CFG684 `des_only`;
  CFG689 D5 both samples and TD5F `full`), so that the "shift in units of the A = 1 shift" row can be filled without
  reading AGB1's other outputs (forbidden to me). They run last, at lower priority; one not run leaves its ratio blank.

## Labels (each run against LGS1's committed A = 0 run of the same sample and mode)
- Primary run A = 0.23 with T_S; bracket A = 0.35 with T_S. The second word of every label is ROBUST if the bracket
  gives the same first word, else FRAGILE. T_H runs get no label.
- **CFG684**, per sample and per combination (BAO+DES5, BAO+DES5+CC), from the run's own `cfg684` output:
  - A1: DEGENERACY BROKEN if `dchi2_max` ≥ 4, else NOT BROKEN (the run's own number, not a difference).
  - A2: ROBUST if |Ω_m(A) − Ω_m(0)| ≤ √(sd_A² + sd_0²) on `flat_a0_om` mean and sd, else AGE-DEPENDENT.
    Ambiguity resolved: "within the two sd added in quadrature" is read as one combined sd, i.e. the two sds (the
    run's and the A = 0 run's) added in quadrature, not twice it. The ratio |Δ| / √(sd_A² + sd_0²) is printed so
    the other reading can be read off.
  - A3: FLOOR HOLDS if `tracking[0]` at z* 2.33 is strictly above 0, else FLOOR LOST (the script stores
    √max(X_lo, 0), so a lost floor shows as exactly 0).
- **CFG689**, per mode (D5, TD5F) and sample, on the `BAO+SN` block:
  - B1 per z* in (1.0, 1.2, 1.5, 2.33): STABLE if the run's median `sqrtX_q[2]` lies in the A = 0 band
    [`sqrtX_q[1]`, `sqrtX_q[3]`] (the 16 and 84 percentiles) and the A = 0 median lies in the run's band (both
    inclusive), else SHIFTED.
  - B2: CLASS UNCHANGED if `P1_class` and `P0`'s `P0_class` both equal the A = 0 run's, else CLASS CHANGED.
    Ambiguity resolved: TD5F is flat (no curvature node), so the script writes no P0; there B2 compares P1 only
    (absent equals absent).
  - Gate: a label needs `K4.ok` true and `nstep` 60,000 in the run it grades and in the A = 0 reference; otherwise
    that mode and sample is NOT EVALUABLE. If only the bracket run fails the gate, the second word is NOT EVALUABLE.
  - Reported, no label: P2 class with Δχ², dof and σ-equivalent; `e_3sigma` at each z*; native H0 median and 68 %.

## Harness checks (judged before any label is read; tolerances read as absolute differences)
- **H1** `cfg684 full` A = 0 vs `cfg684_results.json`, both combinations: `dchi2_max`, `flat_a0_om` mean and sd,
  `tracking` and `rival` (both edges) at z* 1.0, 1.5, 2.33; every |difference| ≤ 1e-6.
- **H2** `cfg684 full` A = 1 T_S vs `agb1_cfg684_full_A1.json`, the same quantities, every |difference| ≤ 1e-9.
- **H3** `cfg689 TD5F des_only` A = 1 T_S vs `agb1_cfg689_TD5F_des_only_A1.json`: tracking √X quantiles at the four
  z*; read as all five stored quantiles (2.5, 16, 50, 84, 97.5), every |difference| ≤ 0.005. The worst difference
  on the 16/50/84 subset is printed too.
- CFG684's labels are NOT EVALUABLE if H1 or H2 fails; CFG689's if H3 fails.

## Reported only
- CFG684 at A = 0.35 with T_H, both samples, with the same quantities as the labelled runs.
- For each run, shift / (A = 1 shift) from my own A = 1 runs: CFG684 the flat-a0 Ω_m (it has no tracking median;
  the band edges at 2.33 are added); CFG689 the tracking medians at each z* (it has no flat-a0 Ω_m).

## Hygiene
- Every output is written into this folder; before and after each run the lane folders `CFG681`, `CFG684`, `CFG689`
  are checked for any file changed or added (mtime marker and `git status`).
- Logs drop interpreter warning lines that carry absolute paths, and the source line echoed after each.

kappa = 1/2 FITTED; not theory closed.
