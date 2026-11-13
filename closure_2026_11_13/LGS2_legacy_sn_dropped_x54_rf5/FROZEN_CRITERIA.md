# LGS2 — re-read X54 and RF5 with the legacy low-redshift supernovae dropped (FROZEN, before any `des_only` number)

2026-11-13. Owner: "swing em". The follow-on to LGS1 (`closure_2026_11_13/LGS1_legacy_sn_dropped/`), which re-read CFG684
and CFG689 and left X54 and RF5 open. A re-read of committed lanes. It adopts nothing and edits no ledger.

## Why
Nájera, Banik and Desmond (arXiv:2610.23657) report that the 197 legacy low-redshift supernovae in the DES-SN5YR Dovekie
Hubble diagram (z 0.025–0.087, IDSURVEY other than 10) sit about +0.065 mag off the DES sample. X54 and RF5 read that
file through the CFG684 loader, which keeps every supernova with z > 0. LGS1 found CFG684's flat-a0 Ω_m LEGACY-DEPENDENT
(no CMB) and CFG689's tracking bands STABLE. Nothing here depends on that paper's numbers. One question:
**do X54's and RF5's frozen results change when the legacy supernovae are dropped?**

Read before freezing (not blind): both lanes' READMEs, criteria, results files and scripts; LGS1's criteria and results.
No `des_only` or `rand197` number for X54 or RF5 exists at this commit. X54's patched CLASS was rebuilt before freezing
with X54's own `x54_make_patch.py` (run through `lgs2_run.py x54_build`, build dir `../_external_data/x54_class_build_lgs2`):
the regenerated patch has sha256 d66bbc98…, identical to the committed `x54_exchange.patch`; the binary's sha256 is
bebbd9c8… against the committed run's debac461… (CLASS compiles its own build path into the binary, so a rebuild in a new
directory cannot match by sha). The binary is judged by X54's own K2 check and by the harness check below.

## Data and samples
The Dovekie Hubble diagram and STAT+SYS inverse covariance in `../_external_data/cfg684_inputs/des5/` (as LGS1).
1,820 supernovae; 1,623 with IDSURVEY 10 (DES, z 0.0733–1.1442); 197 legacy (IDSURVEY 5, 63, 64, 65, 66, 150).
- `full`: all 1,820, the committed lanes' own selection. Harness check only.
- `des_only`: IDSURVEY 10 only (1,623). **The primary sample.**
- `rand197`: legacy kept, 197 randomly chosen DES supernovae dropped (numpy `default_rng(20261113)`, the same draw as
  LGS1's control). Size control, X54's primary model only.
A dropped supernova is removed from the covariance (invert the inverse covariance, take the sub-block, invert), as the
loader already does. No MUERR cut. The absolute magnitude stays marginalised analytically.

## Method
`lgs2_run.py` executes the committed sources with exact text substitutions, each asserted to occur exactly once:
- the selection mask in X54's `load_sn` (`ww = dz > 0` → `ww = (dz > 0) & LGS_SEL(rows)`); RF5 gets the same mask through
  the X54 BAO / SN block it executes (one added line after its own `blk.replace`, plus `LGS_SEL` in that namespace);
- every output path, into this folder (`lgs2_x54_<sample>.{out,json}`, `lgs2_rf5_<sample>.{out,json}`,
  `rf5_cells_<sample>/`);
- build, run and work directories, outside the repository: `../_external_data/x54_class_build_lgs2` (runs in
  `runs_<sample>`), `../_external_data/rf5_work_lgs2_<sample>`. RF5's binaries are its committed builds, read only;
- scope (stated here, not a change of method): X54 runs its DES-SN5YR profiles only (M-C and M-D; Pantheon+ and Union3
  contain no Dovekie supernova); the control runs M-C only. RF5's chain runs the eight cells the committed run finished
  (z_on 1e6, 3e5, 1e5, 5e4, 3e4, 2e4, 1.2e4, 7000); 4000 and below are not run and stay UNDETERMINED (not finished), as
  committed. Its grader is unchanged and still lists all fourteen cells.
Same likelihoods, grids, start points, steering, stop rules and seeds. No MUTATE, REANALYSE or supplement mode.
`lgs2_collect.py` applies the rules below. The harness, the collector and this file are committed alone, first.

## Part A — X54 (profile likelihood in the exchange ξ; CMB + DESI DR2 BAO + DES-SN5YR)
- **Harness check.** Each run must pass X54's Step 0 and K1–K4 with their required outcomes (7/7), or that run is NOT
  EVALUABLE. `full` must reproduce the committed `x54_cold_de_exchange_results.json`, per model (M-C, M-D): the same set
  of converged grid points; each point's graded χ² within 0.1; Δχ²(ξ = 0) within 0.1; ξ̂ and both 95 % edges within 1e-4
  (M-C) or 5e-3 (M-D); same class category and a0 grade. Tolerances: X54's refit stops when the steered χ² falls by less
  than 0.05, so each converged point is fixed to about 0.05 and a difference of two points to 0.1. On M-C's profile
  (95 % half-width 0.0023, σ ≈ 0.0012) an error of 0.1 in χ² moves ξ̂ and the edges by about 3e-5; 1e-4 is three times that
  and 5 % of the grid step. M-D's profile is about 50 times wider, hence 5e-3. A model whose harness check fails is
  NOT EVALUABLE.
- **Label 1 (X54's own frozen classes), primary = M-C, DES-SN5YR.** UNCHANGED or CHANGED for (a) the class category
  (EXCHANGE PREFERRED (direction) / EXCHANGE ALLOWED / EXCHANGE EXCLUDED BEYOND / UNDECIDED; the printed bounds are not part
  of the category, they are Label 2's business), and (b) the a0 grade (CONSISTENT / TENSION of √X(2.33) at ξ̂ against
  CFG689's TD5F band [0.68, 1.04]) on each footing, 9.3603e-11 and 1.1312e-10 m/s², never pooled. The grade reads the
  footing-independent ratio √X, so the two footings carry the same label by construction; absolute a0(2.33) is printed for
  each.
- **Label 2, STABLE or SHIFTED by mutual containment** on X54's own 95 % interval (Δχ² ≤ 3.84 on its spline): STABLE if
  the `des_only` ξ̂ lies inside the committed interval and the committed ξ̂ lies inside the `des_only` interval.
  **Label 2b**, the same rule on the 68 % interval (Δχ² ≤ 1), computed by the collector from the converged grid points with
  X54's own spline construction. 2b is the stricter one and is the analogue of LGS1's 68 % rule.
- **Matched-band reading (frozen, reported with its label).** X54's a0 grade uses CFG689's committed TD5F band, which was
  itself built with the legacy set. The `des_only` √X(2.33) at ξ̂ is also graded against LGS1's legacy-dropped TD5F band
  at z 2.33 (read from `lgs1_results.json`, 0.654–1.009).
- **Control.** Labels 1, 2 and 2b for `rand197` against the committed numbers. If `des_only` changes a label and `rand197`
  does not, the change comes from the legacy set; if both change, it is not attributable to the legacy set alone.
- **M-D (Q ∝ ρ_DE), reported with the same labels.** It is not X54's primary. Committed: UNDECIDED (upper side not
  closed on the frozen grid), a0 TENSION, Δχ²(ξ = 0) 2.76. Its 95 % "interval" ends at the grid edge 0.2; containment is
  applied to the interval as printed.
- Reported, no label: F_made at ξ̂ and the 95 % ends, S8, the ξ = 0 refit's H0, Ω_m and χ², the CPL fit at ξ̂.

## Part B — RF5 (turn-on epoch of the cold component; CMB + DESI DR2 BAO + DES-SN5YR steer; shear and forest graded)
Run order per sample: `chain` (cells 1e6 → 7000), then `khronon` (μ_K 0.03, 0.1), then `channel` per cell, then `grade`.
Channels follow the committed coverage: shear + forest at 1e6, 3e5, 1e5, 5e4, 3e4, 2e4; shear only at 1.2e4, 7000 and K0.1.
For `full` the forest is run at 1e6 only (the committed G0 cell), shear everywhere. The shear scale cut is re-derived by
RF5's own rule at each sample's 1e6 best fit (the lane's frozen procedure); whether it equals the committed kept set is
reported. RF5's machinery checks (`checks`, K1–K8) are run once, on `full`. K9 (preemption), MUTATE and the restart
check are not re-run.
- **Harness check.** `full` must reproduce the committed `rf5_results.json`: at each cell 1e6 … 2e4, every graded χ² part
  (plik, low-ℓ TT, low-ℓ EE, A prior, BAO, SN), the shear χ² and S − S_min within 0.2; at 1.2e4 and 7000 the same gate
  outcomes and plik within 1 %; the khronon rows' labels the same; the shear kept set identical; K1–K8 passing. Tolerance:
  twice RF5's own stop line (|Δχ²| < 0.1); RF5's different-start refit of 5e4 moved its χ² by 0.034, inside it. 1.2e4 and
  7000 fail G-CMB at p < 1e-28 and the lane says 7000 is its roughest fit, so only their gates are checked. Forest: the
  1e6 forest χ² within 2.0 and the same G0 outcome; if only this fails, the forest reading is NOT EVALUABLE and the rest
  stands. If any other part fails, Part B is NOT EVALUABLE and `des_only` is reported against the committed files only.
- **Label 1 (RF5's verdict, per footing).** UNCHANGED if the `des_only` verdict line is the committed one, "a window exists
  at z_on in [30000, 1000000] (forest NOT DIAGNOSTIC (G0); CMB = plik-lite; shear = DES Y3 xi+ linear-safe)", on each
  footing, and the khronon rows keep their labels (UNDETERMINED, UNDETERMINED); else CHANGED. The footings share one χ²
  surface (a0 is absent at linear order), so they carry the same label by construction.
- **Label 2 (RF5's headline quantity: the surface S − S_min, which sets the window's lower edge through the 25 line).**
  STABLE if, at every cell where the committed S is defined (1e6 … 1.2e4), |(S − S_min)_des_only − (S − S_min)_committed|
  ≤ 1.0; else SHIFTED, naming the cells. A cell whose `des_only` S is missing makes Label 2 NOT EVALUABLE, with the reason. 1.0 is RF5's own restart-check line and the Δχ² of a one-parameter 68 % interval. The margin of the
  edge cell 3e4 to the 25 line (committed 2.97) is reported with it.
- Reported, no label: per-cell w0, wa, Ω_m, h, σ8, √X, the SN χ² and its p, the shear χ² and A_shear, the forest χ² and
  G0, and the absolute-gates-only edge.

## Compute and guards
`python3 -I -B`, `nice -n 10`, at most three CLASS children at once across the lane (three X54 processes with one child
each, or one RF5 driver with its three). Logs go to a scratch path and are copied here at commit time. `df -h /` and
`memory_pressure` are checked before each heavy step; below 5 GB free the lane stops and reports. No process this lane did
not start is signalled. RF5's stop rule applies per sample: near 3 h of wall time, what is unfinished is UNDETERMINED.
An exit on any guard is NOT RUN, stated, not worked around. After every run, `git status --short` must show the
committed X54 and RF5 folders untouched.

## Not in this lane
X54's Pantheon+ and Union3 profiles (no Dovekie supernova; their start point is the DES-SN5YR ξ = 0 refit, so they would
move only through it), X54's post-hoc S1 supplement and MUTATE run. RF5's cells at z_on 4000 and below (unfinished in the
committed run), its forest at 1.2e4 and 7000 (not run there either), the `full` forest beyond 1e6, K9, MUTATE and the
restart check. No size control for RF5. No w0–wa fit beyond what the lanes print.

## What the result may and may not say
A re-read. UNCHANGED / STABLE means the committed results do not lean on the legacy supernovae. CHANGED / SHIFTED means
they do, and the lane then carries that as a stated dependence; it does not by itself say which sample is right. Nothing
here measures H0 or a0, and nothing here grades the framework.

kappa = 1/2 FITTED; not theory closed.
