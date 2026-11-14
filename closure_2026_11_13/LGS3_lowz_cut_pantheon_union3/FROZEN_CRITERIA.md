# LGS3 — X54's Pantheon+ and Union3 profiles with the low-redshift supernovae cut (FROZEN, before any cut number)

2026-11-13. Owner-approved ("swing steps 1 and 3"), relayed by the coordinating session. A re-read of committed lanes. It
adopts nothing and edits no ledger.

## Why
LGS2 (`closure_2026_11_13/LGS2_legacy_sn_dropped_x54_rf5/`) found that X54's M-D lean (Q = ξHρ_DE, DE → cold, Δχ² 2.76 at
ξ = 0 with DES-SN5YR) disappears when Dovekie's 197 legacy low-redshift supernovae are dropped (Δχ² 0.001), and that a
size control keeps it. X54's committed Pantheon+ and Union3 M-D profiles lean the same way (Δχ² 1.94 and 1.86). Both
compilations carry their own low-redshift samples. One question: **does the lean with Pantheon+ and with Union3 also come
from their low-redshift supernovae?** It decides whether "a low-redshift supernova artefact" holds beyond one compilation.
Prompted by arXiv:2610.23657 (a legacy low-redshift offset in Dovekie); nothing here uses that paper's numbers.

Read before freezing (not blind): LGS2's results and X54's committed numbers. No cut number for X54 or CFG689 exists at
this commit. Counts below come from the data files, with no fit.

## Data and samples (counts before any fit)
**Pantheon+** (`PantheonPlusSH0ES.dat` + STAT+SYS covariance; X54's loader keeps non-calibrators with zHD > 0.01: 1,580 rows).
- `full`: the loader's own selection, 1,580. Harness check only.
- `zcut` (**primary**): also zHD > 0.0870, the top of the Dovekie legacy range. Removes 613; keeps 967.
- `legacy_surveys` (secondary): rows with IDSURVEY 5, 63, 64, 65, 66 or 150 (CSP, CfA3S, CfA3K, CfA4p1, CfA4p2,
  Foundation) dropped at any redshift. Removes 374 (372 at zHD ≤ 0.087, 2 above); keeps 1,206.
  - The code convention was checked in the data, not taken from memory. 191 of Dovekie's 197 legacy supernovae appear in
    Pantheon+ by name (CID), and 189 of them carry the same IDSURVEY. The other 2 are Dovekie 64 (CfA3K) against
    Pantheon+ 5 (CSP).
  - Over all 339 names shared by the two files, 337 agree.
  - Pantheon+ rows are light-curve entries. A supernova with a second row from another survey (CfA1, CfA2, LOSS, …)
    keeps that row.
- `rand` (size control, frozen for M-C and M-D): low redshift kept; 613 supernovae (as many as `zcut` removes) dropped at
  random from zHD > 0.0870, numpy `default_rng(20261114)`. Keeps 967: 613 at zHD ≤ 0.087 and 354 above. This removes
  63 % of the z > 0.087 set: it matches the count, not the information.
- Covariance: sub-block of the covariance, then inverted, as the loader does. The absolute magnitude stays marginalised.

**Union3** (22 spline nodes, z 0.05 … 2.26; the file gives node μ and their inverse covariance).
- `full`: all 22. Harness check only.
- `zcut` (**primary**): the one node at z ≤ 0.0870 (z = 0.05) marginalised out (invert the weight matrix, take the
  covariance sub-block, invert). The cut is approximate in supernova redshift: the spline node at z = 0.10 still carries
  supernovae from about 0.05 to 0.15.
- `node055` (control, frozen for M-C and M-D): the z = 0.55 node marginalised out instead.
  - Rule: of the nodes above the cut, the one whose M-marginalised conditional precision (the diagonal of the projected
    weight matrix, which measures the information unique to a node and is what marginalising it removes) is closest to
    the z = 0.05 node's: 1,744 against 1,877.
  - Marginal σ cannot discriminate: it is 0.089–0.098 for every node below z 0.8, dominated by the offset they share.
  - A random draw (`default_rng(20261114)`) would pick z = 1.39, a node with about a quarter of that precision. It is not
    used.

## Method
`lgs3_run.py` executes X54's committed script with exact text substitutions, each asserted to occur exactly once:
- **Selection.** The Pantheon+ row selection (`& LGS_SEL_PP(raw)`) and the Union3 node cut (after the loader's own line).
  Both are switched on only **after** X54's Step 0 and checks K1–K4, which read the full sets: S0-2 reproduces CFG681's
  BAO + Pantheon+ χ² on all of Pantheon+. The profile set is then reloaded and its size printed.
- **Outputs.** Paths into this folder (`lgs3_x54_<PP|U3>_<sample>.{out,json}`).
- **Directories.** Build: LGS2's rebuild at `../_external_data/x54_class_build_lgs2` (patch sha256 d66bbc98…, identical to
  X54's). Runs: `runs_lgs3_<comp>_<sample>` there.
- **Scope.**
  - Each run fits one compilation (M-C then M-D), through X54's own Pantheon+ / Union3 profile path: inner grid
    ±{0.002, 0.004} (M-C) or ±{0.1, 0.2} (M-D), started from the DES-SN5YR ξ = 0 refit, with X54's extension rule.
  - The DES-SN5YR profiles are not refitted. They are loaded from the committed results through X54's own REANALYSE path
    (LGS2 showed the live refit reproduces them exactly), so the start point is the committed one.
- Same likelihoods, grids, steering and stop rules. No MUTATE or S1 supplement.
The build is judged by X54's own Step 0 and K1–K4 (7/7 required in every run) and by the harness check.

## Part A — X54, per compilation (Pantheon+, Union3), per model (M-C, M-D)
- **Harness check** (as LGS2). `full` must reproduce the committed `x54_cold_de_exchange_results.json`:
  - the same converged grid points, each graded χ² within 0.1, and Δχ²(ξ = 0) within 0.1;
  - ξ̂ and both 95 % edges within 1e-4 (M-C) or 5e-3 (M-D);
  - the same class category and a0 grade.

  The committed values are M-C Pantheon+ −0.00133, 1.25, [−0.00363, +0.00102]; M-C Union3 −0.00141, 1.39,
  [−0.00370, +0.00095]; M-D Pantheon+ +0.099, 1.94, [−0.041, grid edge +0.20]; M-D Union3 +0.117, 1.86, [−0.052, grid
  edge +0.20]. Tolerances as justified in LGS2 (X54's 0.05 stop rule, the profiles' widths). A failing model is
  NOT EVALUABLE.
- **Label 1.** Class category (EXCHANGE PREFERRED (direction) / ALLOWED / EXCLUDED BEYOND / UNDECIDED) UNCHANGED or
  CHANGED. The a0 grade, X54's own (√X(2.33) at ξ̂ against CFG689's TF band [0.68, 1.05] for Pantheon+ and TU3F band
  [0.69, 1.07] for Union3), UNCHANGED or CHANGED on each footing, 9.3603e-11 and 1.1312e-10 m/s², never pooled. The
  footings carry the same label by construction (the grade reads √X); absolute a0(2.33) is printed for each.
- **Label 2.** STABLE or SHIFTED by mutual containment of the best fits, on X54's 95 % interval and on the 68 % interval
  (Δχ² ≤ 1, from the converged points with X54's spline).
- **Control rule.** For `zcut` against its control (`rand`; `node055`), per label and model: a change for `zcut` and none
  for the control comes "from the low-redshift cut"; a change in both is "not attributable to the low-redshift cut alone".
  `legacy_surveys` gets Labels 1 and 2 but no control reading (the control matches `zcut`'s count, not its).
- **The LEAN reading (frozen; the lane's question)**, per compilation, from M-D's Δχ²(ξ = 0) = χ²(0) − χ²(ξ̂):
  - **LEAN FROM LOW-Z** if Δχ² < 1.0 for `zcut` while Δχ² ≥ 1.0 for the control;
  - **LEAN NOT FROM LOW-Z** if Δχ² ≥ 1.0 for `zcut`;
  - **UNDECIDED** otherwise (both below 1.0).

  NOT EVALUABLE if M-D's harness check fails or a run is missing. For `legacy_surveys`, M-D's Δχ² is reported with no
  reading.
- Reported, no label: F_made, S8, the ξ = 0 refit's H0 and Ω_m, the CPL fit at ξ̂.

## Part B (optional, cheap) — CFG689 flat + acoustic-angle modes, TF (Pantheon+) and TU3F (Union3), `full` and `zcut`
`lgs3_run.py cfg689` applies the same selection to CFG689's loader (no CFG689 check in these modes reads the supernovae),
with the LGS1 pattern: frozen 60,000 steps, same seeds, outputs `lgs3_cfg689_<mode>_<sample>.{out,json}`.
- **Harness:** `full` reproduces the committed tracking √X quantiles at z* 1.0, 1.2, 1.5, 2.33 to 0.005.
- **B1 per z*:** STABLE if the `zcut` median of tracking √X lies inside the committed 68 % band and the committed median lies
  inside the `zcut` band; else SHIFTED.
- **B2:** CLASS UNCHANGED if the P1 and P0 classes are the committed ones.
- **B3:** the script's own constant-dark-energy class (P2) UNCHANGED or CHANGED; Δχ² and σ reported.
- The chain check K4 must be ok, or the mode is NOT EVALUABLE. A busy-machine exit (75) is NOT RUN.

## Compute and guards
`python3 -I -B`, `nice -n 10`, at most three CLASS children at once (one per X54 process). Another lane has priority on the
machine. `df -h /` and `memory_pressure` are checked before each heavy step; below 5 GB free the lane stops. No process this
lane did not start is signalled. Logs go to scratch and are copied here (as `.txt`) at commit time. After every run the
committed X54 and CFG689 folders must be untouched.

## Not in this lane
- X54's DES-SN5YR profiles (LGS2), MUTATE and S1.
- CFG689 for `legacy_surveys` or the controls, and its other modes.
- RF5 (not asked).
- No w0–wa fit beyond what the scripts print.

## What the result may and may not say
A re-read. LEAN FROM LOW-Z means the compilation's M-D lean goes away with its low-redshift supernovae (or node) while a
matched control keeps it. It does not say which supernovae are right, nor that the low-redshift samples are offset; it does
not test arXiv:2610.23657's offset. Nothing here measures H0 or a0, and nothing here grades the framework.

kappa = 1/2 FITTED; not theory closed.
