# CFG902 FROZEN CRITERIA: CFG804 rerun with the mass convention its source (CFG416) declared (committed alone, before any script)

**Why.** CFG886 (README, section T5) found that CFG804 solves the catchment fixed point M_ta = M_b/(f_ret f_b) in Msun,
while CFG416 declared its f_ret(M_ta) ramp in **Msun/h** ("0.10 below 10^12.5 Msun/h", CFG416 FROZEN_CRITERIA.md line 8).
CFG886 estimated 13–28% more supply in bins 2–4 under the declared convention, and said CFG804 needs a rerun to see
whether its primary verdict or its all-radii shortfall changes. This lane is that rerun, fixed forward. CFG804's and
CFG416's files are not edited.

## What changes (and nothing else)

CFG804's committed script `CFG804_catchment_supply_derived/cfg804.py` (git blob b1749cb85e224d5a78927a061aa2832126b5b1ec,
commit 67774ce37) is read as text, checked against that blob hash, and executed in a fresh process with exactly these
string replacements, each asserted to occur exactly once:

- **R1, the convention (the only physics change).** In `N_of`, the line
  `lMta = logMb - math.log10(f * FB); fn = fret_of(lMta)` becomes
  `lMta = logMb - math.log10(f * FB) + SHIFT_DEX; fn = fret_of(lMta)`.
  With SHIFT_DEX = log10 h this is M_ta[Msun/h] = h M_b[Msun]/(f_ret f_b), the inverse of CFG416's own conversion
  `Mbn = fr * 0.157 * Mta / 0.674  # Msun` (cfg416_pm.py, x_supply, line 277; Mta in Msun/h).
- **R2, the same convention in CFG804's internal K1 target.** `abs(lk - 12.30) < 0.01` becomes
  `abs(lk - (12.30 + SHIFT_DEX)) < 0.01`. (The 12.30 is a log M_ta in Msun; in Msun/h the same fixed point sits at
  12.30 + log10 h. N = 10 is unchanged.)
- **R3, output redirection only.** The two output writes (`cfg804_results{sfx}.json`, `cfg804{sfx}.out` into CFG804's
  directory) are redirected into this lane's directory as `cfg902_results_{MODE}{sfx}.json` and `cfg902_{MODE}{sfx}.out`.
  Nothing is written into CFG804's directory (checked with `git status` after the runs).
- The script's `__file__` is set to CFG804's own path, so the KiDS data path `D` resolves exactly as in CFG804.
  `sys.argv` carries `alt` for the alt footing; `CFG804_MUTATE` is unset (CFG804's own f_ret = 1 mutate is not rerun).
  The final `sys.exit` is caught.

Everything else is CFG804 verbatim: fret_of, f_b = 1/(1 + 5.364), the fixed point, the edge rule, the profile grid,
the NGRID snapping (1, 2–10 in 0.25), the KiDS-1000 B21 Fig. 3 data and full covariance, the per-bin mass profiling
(grid 9.00–12.00 in 0.01, 3 sweeps from ZK), primary R ≤ 0.31 Mpc and all radii.

**h for the conversion: 0.674.** This is the value CFG416 itself used to convert its ramp's Msun/h masses to Msun
(cfg416_pm.py line 277 and line 279; cfg416_checks.py `H = 0.674`), and the value CFG886 used for this finding
(`H_REC = 0.674`). CFG804 uses no h at all. So the choice is not ambiguous and no 0.674/0.70 bracket is run.
SHIFT_DEX = log10(0.674) = −0.17134. (CFG416's PM cosmology uses h = 0.6736, i.e. log10 h = −0.17160, 0.0003 dex away;
reported only, at fixed masses, see R-h below.)

## Runs (single core, separate processes, both footings, never pooled)

| MODE | SHIFT_DEX | footings | role |
|---|---|---|---|
| `orig` | 0 | canonical (a0 9.3603e-11), alt (1.1312e-10) | K1 reproduction of CFG804 |
| `declared` | log10(0.674) = −0.17134 | canonical, alt | **the result** |
| `mutate` | 2 log10(0.674) = −0.34268 (deliberately wrong: h² instead of h) | canonical | MUTATE |

## Classes (CFG804's own, unchanged)

- Primary (R ≤ 0.31 Mpc): **DERIVED SUPPLY SUFFICES** if Δχ²(D_der − B) ≤ 4; **FALLS SHORT** otherwise.
- All radii: the same threshold, as CFG804's script prints it (CFG804: FALLS SHORT, +148.7 canonical / +172.2 alt).
- Reported per footing and per radius set: Δχ², the class, and **CLASS CHANGED yes/no** against CFG804's committed class.
  Also the derived N, log M_ta (Msun/h), f_ret and edge (r_M and kpc) per bin at the best-fit masses, and the change in
  the all-radii Δχ² (declared − orig).
- No new threshold is introduced. A smaller all-radii Δχ² that stays > 4 is reported as "shortfall reduced, class
  unchanged", not as a pass.

## Controls

- **K1 (binding): the original convention reproduces CFG804's committed numbers.** `orig` must reproduce every number in
  the committed `cfg804_results.json` (canonical) and `cfg804_results_alt.json` (alt): chi2_B, chi2_D, dchi2 and p_D for
  primary and all radii to |Δ| ≤ 1e-6 (p_D relative ≤ 1e-6), the best-fit logMb per bin to ≤ 1e-9, and K1, K2 and cls
  identical. Byte identity of the printed `.out` against `cfg804.out` / `cfg804_alt.out` is reported (not binding).
- **K2 (binding): the change touches only D.** chi2_B (primary and all radii, both footings) is identical between `orig`
  and `declared` to ≤ 1e-9, and CFG804's internal K1 (with the R2 target) and K2 lines print PASS in every non-mutate run.
- **K3 (binding): the fixed point in the declared convention.** At log M_b = 10.5 it gives N = 10.000 and
  log M_ta = 12.304 − 0.171 = 12.133 (± 0.01). At CFG804's committed canonical primary masses (10.38 / 10.78 / 10.91 /
  11.12) it reproduces CFG886's declared-convention N = 10.0 / 10.0 / 9.4 / 7.0 to ≤ 0.05.
- **MUTATE (binding, separate outputs `cfg902_*_mutate*`).** With the doubled shift (canonical):
  (a) at the `declared` run's best-fit masses, N_mutate ≥ N_declared in every bin (both radius sets) and strictly greater
  in at least one bin; and (b) the all-radii Δχ² responds: Δχ²_all(mutate) ≤ Δχ²_all(declared) − 1.0 (more supply
  moves D toward B). MUTATE **bites** if (a) and (b) hold; otherwise it is reported as NOT BITING and the rerun is
  reported as not shown to be sensitive.
- **R-h (reported only).** N at the `declared` best-fit masses with h = 0.6736 instead of 0.674, and whether the NGRID
  snapping (and so the D profile) changes in any bin.

## Limits (stated in advance)

- Compute: each process single-threaded (OMP_NUM_THREADS=1, nice 10), < 1 GB, < 15 min; if CFG804's code exceeds either,
  the lane stops and reports instead of running.
- This lane changes only the unit convention. It does not address CFG886's other T5 points (R from BAO + BBN, the
  census f_ret provenance: galaxy floor not traceable in repo, ramp UNDETERMINED), and it does not add the framework
  two-halo term CFG804 names as its next step.
- The census f_ret is an observational input carried in the record, not derived by the framework (CFG804 caveat; CFG806).

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native model; not theory closed.
