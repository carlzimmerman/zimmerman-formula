# Audit of the Codex mass-budget folder (2026-11-14)

Written 2026-11-14, 14:35 EST. This is an audit of `codex_mass_budget_2026_11_14/` (without `latest_sn_review/`), the three untracked WLJ1 items, and the root handoff `CLAUDE_HANDOFF_MASS_BUDGET_2026_11_14.txt`. Every claim in those files was treated as something to check. Nothing under those paths, the paper folder, CJ1, or any lane was edited, staged or committed. The checks were done independently, with this folder's own scripts. `calculation/reproduce.py` was not needed as a cross-check, because the independent numbers already matched exactly.

## Grades

- **A1** 10,272 cases and patch mass conserved to 6.67e-16: **CORRECT** (got 10,272 rows and 6.66e-16 on the FZS1 layouts).
- **A2** Retained-source counts at z 0, f 2 (172/240 canonical, 186/250 alt) and all-Bar counts (240/240, 250/250): **CORRECT**. All 32 retained cells of the calculation README and all 8 all-Bar f 2 cells were reproduced exactly. As they say, these are grid counts, not abundance-weighted counts.
- **A3** Denominators (X 5.41; grid ratio 5.364327224; Xsh 59.4861 / 59.5029 at z 0 and 55.7159 / 55.7313 at z >= 1; FB 0.157125799): **CORRECT**.
- **A4** `BUDGET_BOUND.md` criterion, R_budget, monotonicity proof: **CORRECT** (re-derived).
- **A5** `BUDGET_BOUND.md` example table: **CORRECT WITH LIMITS**. Six of the eight rows were reproduced exactly (z 0, 2.2 and 3; both footings). The two z 4.4 rows were not checked. The exact match needs the halo code's G = 4.30091e-9 Mpc (km/s)^2/Msun. With CODATA G and the record's MSUN = 1.98892e30 kg, every radius is 1.3e-4 larger (e.g. 430.333 rather than 430.277 kpc). No count changes. The number of interior crossings (76 of 128 rows) was not recounted.
- **B1** Static junction (t >= 0, no mass sheet, unchanged inner force, density-equality condition): **CORRECT**.
- **B2** Interface condition [J^r] - Rdot [J^t] = 0: **CORRECT**. It needs a continuous metric, which is stated.
- **B3** Reading of QX17 E3 and E2, and lambda_in = 0 in an exactly stationary interior: **CORRECT WITH LIMITS**. The interior must be static (n parallel to a hypersurface-orthogonal Killing vector) and the clock must be aligned, so that Q is invariant. P_in^t = 0 also needs adapted coordinates with no g_tr. These conditions are stated as "aligned with the Killing flow" and "adapted static coordinates".
- **B4** Advective reduction and its four consequences, the j_extra formula and the two rational examples: **CORRECT**.
- **B5** Kinematic interpolation and the bound |v| <= B/tau: **CORRECT**.
- **B6** "7,110 active snapshots; 3,706 require outer outflow": **CORRECT**. The recount gives 7,110 rows, 27 with zero outer density, 3,706 with ratio < 0.999, 3,373 with ratio > 1.001 and 4 near-equal.
- **B7** "Full polarization transport can change that conclusion" (handoff section 4, README): **OVERSTATED**, and I grade it **WRONG in the weak-field regime**. The non-advective flux is about v_c^2/c^2 ≈ 3e-7 to 5e-7 of the advective flux for a Milky-Way-mass system at 100 kpc (derivation below). Only a strong-field or effectively singular polarization layer could change the 3,706 count.
- **C** `test_wlj1_grade.py` gives 7/7 OK. All six outputs are byte-identical, in their harness and in my own copy run. The pooled-flag mutant fails 7/7. **CORRECT**.
- **D** `INDEPENDENT_REVIEW.md` and `verification/VERIFICATION.md`: **CORRECT WITH LIMITS**. The "independent" reviewer is a subagent of the same Codex session, so it is not independent of that session. It reran no numerical experiment. The "validated manifests" are hash and provenance checks, not correctness checks. Details are in item D.
- **E** Hygiene: 18 files contain home paths or the account name. Five files are over 5 MB outside `latest_sn_review/`, and two more are inside it. No tracked file is edited or overwritten. The per-path recommendation is in item E.

## Item A: enclosed masses (own SI calculation)

Script: `audit_a_masses.py`. It executes the FZS1 prefix read-only, which in turn loads FRZ1 and CFG556 read-only. It uses only their halo population, `rset_com` (the FLD1 R_set), `M_L`, `bar_cum` and `lay_S`. Everything else is recomputed here in SI:

- G = 6.67430e-11, with a0 canonical / alt = 9.3603e-11 / 1.1312e-10 m/s^2, constant in z.
- v* = a0/(10 q H0 E(z)) with q = 6.41, which gives 668.53 / 807.93 km/s at z 0.
- Active means v200c <= v*, with v200c from M200c and r200c in SI.
- Xsh is recomputed from the medians of PD1's `share_over_Mb` tables.
- C = [sqrt(b^2 + 4 b a0 r^2/G) - b]/2 is compared with Q = (1-FB) Mta/h.

The retained source b is (1-FB) Mta/(h Xsh) on galaxies and `bar_cum` on clusters. The all-Bar source b is Mb + (FB Mta - Mb) M_L/Mta on galaxies.

```
nice -n 19 python3 -I -B reviews/codex_mass_budget_audit_2026_11_14/audit_a_masses.py               > audit_a_masses.out
nice -n 19 python3 -I -B reviews/codex_mass_budget_audit_2026_11_14/audit_a_masses.py --msun-code   > audit_a_masses_codeG.out
```

Peak memory was 0.46 GB.

**Retained-source exceedances** (active haloes in brackets; canonical | alt), identical to the calculation README:

| z | f 1.25 | f 2 | f 3 | f 5 |
|---|---|---|---|---|
| 0 | 87 \| 101 | 172 \| 186 | 213 \| 228 | 240 \| 250 (240 \| 250) |
| 2.2 | 0 \| 0 | 0 \| 0 | 41 \| 52 | 96 \| 106 (151 \| 161) |
| 3 | 0 \| 0 | 0 \| 0 | 0 \| 0 | 57 \| 68 (129 \| 139) |
| 4.4 | 0 \| 0 | 0 \| 0 | 0 \| 0 | 0 \| 0 (98 \| 108) |

**All-Bar exceedances at f 2**, canonical | alt:

| z | canonical | alt |
|---|---|---|
| 0 | 240/240 | 250/250 |
| 2.2 | 81/151 | 91/161 |
| 3 | 30/129 | 44/139 |
| 4.4 | 0/98 | 0/108 |

All of these match. For the other f values, the all-Bar counts are in `audit_a_masses.out`; their files report only f 2.

**Budget table** (physical kpc, halo-code G; canonical | alt):

| row | retained R_budget | all-Bar R_budget | R_set at f 3 |
|---|---|---|---|
| z 0, 1e12 | 430.277 \| 391.457 | 194.190 \| 180.092 | 447.329 \| 447.229 |
| z 2.2, 1e11 | 159.783 \| 145.366 | 68.937 \| 63.977 | 75.816 \| 75.787 |
| z 3, 1e11 | 168.265 \| 153.083 | 70.095 \| 65.055 | 55.882 \| 55.855 |

These equal their table to the last digit. The rta values (1076.532, 221.070 and 185.827 kpc) also match.

The worked example also matches: canonical, z 0, 1e12, f 1.25. It gives Mb 3.45546e10 Msun, R_set 186.387 kpc, raw cold 5.932716e11 Msun/h and patch cold 1.384596e12 Msun/h. At f 3 the raw cold is 1.439923e12 Msun/h.

Constant convention: with CODATA G and MSUN 1.98892e30, every radius scales by sqrt(4.302021/4.30091) = 1.000129. Their "independent physical-unit check" reuses the halo code's G, so it does not test this convention. The size of the effect is 1.3e-4, and it changes no count.

Monotonicity proof (re-derived): from C^2 + bC = k b r^2 with k = a0/G,

- dC/db = (k r^2 - C)/(2C + b) = C^2/[b(2C + b)] >= 0;
- dC/dr = 2 k b r/(2C + b) > 0 for r, b > 0.

C <= Q is equivalent to F(C) <= F(Q) because F(x) = x(x+b) is increasing.

Not checked: the s-range table, the force-residual examples (+0.2372479 and -0.7591404), the eta / scope tables (run_003), and the figure.

## Item B: junction theorem, transport path, weak-field size

Algebra, re-derived by hand:

- The distributional divergence of J H(-F) + J_out H(F) leaves [J^mu] d_mu F delta(F), with d_t F = -Rdot.
- QX17 E3 is exactly the current n^m rho_Q - lambda P^m/Q, with rho_Q = J_P/Q + mu_K^2 (Q-1)/K.
- E2's normal part is lambda = (1 + gamma_L Pi_+) n.d ln N + gamma_L n.d Pi_+. This is zero when every field is invariant along n parallel to the Killing vector.
- Moving interface: lambda_out (P^r - Rdot P^t)/Q_out = rho_out (n^r - Rdot n^t)_out + Rdot n_in^t rho_in.
- Advective form: v_out = Rdot (1 - N_in/N_out).
- Consequences 1 to 4: verified.
- Sdot sign: verified.
- j_extra,out/N_out = Rdot (1 - N_in/N_out) - v_out: verified.
- Rational examples: t = 2/3 with ratio 3/2 and Rdot 2, v_out -1; t = 3/2 with ratio 2/3. Both verified.
- Transport path: C_t + v C_r = 0. Also 4 pi r^2 N v = -a_dot Delta, and |v| <= (1-a)|Delta|/[tau (1-a) C_R'] <= B/tau. The linear-schedule blow-up and the finite-time-arrival argument are also correct.

**Recount of 7,110 / 3,706** (`audit_b_junction_count.py`; `audit_b_junction_count.out`): this uses XJ1's library read-only, only for the population, R_set (`rsurf_com` on XJ1's shell runs) and the cluster layout. On the galaxy branch the one-sided slopes are analytic here:

- inside: d/dr[min(phantom, Mcold) + rem r/rta];
- outside: t Mcold M_L'/Mta.

That covers 6,904 of the 7,110 rows. On the 206 cluster rows I used finite differences. Totals: 7,110 rows; 27 degenerate (zero outer density, all z 0 k 2: 8 canonical and 19 alt); 3,706 below 0.999; 3,373 above 1.001; 4 near 1. Every group count equals run_007.

**Weak-field size of the non-advective flux** (`audit_b_weakfield.py`; `audit_b_weakfield.out`):

- Take lapse N ≈ 1 + Phi/c^2 and clock tilt n^r ≈ v/c. Then E2 gives lambda ≈ c^-3 (d_t Phi + v d_r Phi) = c^-3 (Phi_dot + v g). The gamma_L Pi_+ part is about 1.5e-15 at 1e-5 Msun/pc^3.
- D.P = N gives P^r = M_N(<r)/(4 pi r^2), so P/N = r/(dln M_N/dln r).
- Ratio: (lambda P/Q)/(N v/c) = (g r/c^2)/(dln M_N/dln r) + Phi_dot r/(c^2 v dln M_N/dln r). The steady part does not depend on v, and it equals v_c^2/c^2 for an isothermal profile.
- Milky-Way mass at 100 kpc: GM/(r c^2) is 2.9e-7 for 6e11 Msun and 4.8e-7 for 1e12 Msun. The deep-law v_flat^2/c^2 for M_b = 6e10 Msun is 3.0e-7 canonical and 3.3e-7 alt. The time-dependent part is about 3e-8.

The lead's estimate of order 1e-6 is confirmed; the steady part is a factor 2 to 3 below it.

A thin layer does not change this scaling. With no surface mass, Phi is C^1, so the n.d ln N part stays bounded at about Phi/c^2 whatever the layer width delta. Only the gamma_L n.d Pi_+ part grows as r/delta. Starting from about 1e-15, it needs r/delta of about 1e14 to 1e15 before it matters. Such a layer is effectively a surface layer, which brings back the excluded surface reservoir.

So in the weak field the non-advective channel cannot supply the O(1) flux, Rdot times the density jump, that the 3,706 cases need. The advective obstruction stands to relative order 1e-6, and the sentence in the handoff and README that full polarization transport "can change that conclusion" needs that qualifier. The JUNCTION_THEOREM text itself is careful: it says no smallness proof is supplied for a sharp layer, and this estimate supplies one. Not checked: COL1's own reduction file.

## Item C: WLJ1

```
TMPDIR=<review>/scratch/tmp nice -n 19 python3 -I -B closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/test_wlj1_grade.py -v
  -> Ran 7 tests, OK
... test_wlj1_grade.py --grader-script .../codex_fix_2026_11_14/run_01/wlj1_grade_shared_flag_mutant.py
  -> FAILED (failures=7)
```

The mutant differs from the grader by exactly one added line, which pools the two C4 flags.

Own copy run: I copied the grader and its 14 inputs into `scratch/wlj1`, then ran `wlj1_grade.py` and `wlj1_grade.py --as-frozen`. `cmp` gives byte-identical results for `wlj1_grade.json/.out`, `wlj1_grade_MUTATE.json/.out` and `wlj1_grade_asfrozen.json/.out`. The `run_01/wlj1_grade_verified.py` copy equals the tracked grader, whose last commit is 6cce4d7328. The scratch folder was deleted after the comparison and is not committed.

## Item D: overstatements in the review and verification files

1. **"Independent review"** is used in the `INDEPENDENT_REVIEW.md` title, in VERIFICATION ("An independent reviewer also ran the seven tests"), in the handoff ("Independent review checked the theorem and its scope") and in BUDGET_BOUND.md ("independently checked by /root/independent_final_review"). The reviewer is a fresh subagent of the same Codex session, so it is not independent of that session's framing or code. Within that limit its algebra checks are right; this audit re-derived the same identities.
2. The reviewer "audited against authenticated outputs, not rerun" and "No numerical experiment was rerun". The rows "Reported mass tables ... match detailed CSV rows" and "All eight displayed example rows match the saved results" therefore show internal consistency, not reproduction. This audit supplies the reproduction for item A (six of eight rows) and for the junction count.
3. "Nine accepted computation manifests validate" uses a validator script outside the repository, under the home directory. By its own message it checks hashes and provenance ("mathematical interpretation requires review"), not correctness. I did not rerun it.
4. The "independent physical-unit check" uses the halo code's G and so does not test the 1.3e-4 constant convention.
5. The handoff and README sentence "Full polarization transport can change that conclusion" leaves open more than the weak-field equations allow (item B).

Nothing else in those two files claims more than was done. PAPER72 1584/1584 is a literal and provenance count, and it says so. The checkpoint commit e8bebc5f83 exists on branch `codex/mass-budget-2026-11-14`.

## Item E: hygiene and commit recommendation

**Home path or account name** (18 files):

- `codex_mass_budget_2026_11_14/latex_compile.json`
- `.../before_correction/PAPER72_audit.py`: a false positive; the string is the audit's own `"/Users/" not in TEX` check.
- `.../latest_review/REVIEW.md`, at line 181 (validator path)
- `.../latest_review/run_001/stderr.txt`, `run_002/stderr.txt`, `run_003/stderr.txt` and `run_004/stderr.txt` (tracebacks)
- `.../calculation/README.md`, at line 159 (validator path)
- `.../calculation/reproduce.py`, at line 11: the validator SKILL path is hard-coded to the home directory, so the script is not reproducible elsewhere.
- `.../calculation/run_005/stderr.txt`
- `.../verification/audit_results.json`, `audit_results_initial.json` and `cj1_audit_launch_failed.out`
- WLJ1 `CODEX_GRADER_VERIFICATION_2026_11_14.md` (3 hits)
- `codex_fix_2026_11_14/runner_command.json` (3 hits)
- `codex_fix_2026_11_14/run_01/comparison.json` (3 hits)
- `codex_fix_2026_11_14/run_01/regression_red.txt` (2 hits)
- root `CLAUDE_HANDOFF_MASS_BUDGET_2026_11_14.txt`, at line 3

Many manifests and notes also name a machine-local temporary venv, `/private/tmp/forj0332-fit-venv/bin/python`. That is not a home path, but it cannot be reproduced on another machine.

**Over 5 MB:**

- `calculation/run_001/representative_profiles.npz` (9.6 MB)
- `calculation/run_001/halo_masses.csv` (8.3 MB)
- `latest_review/run_005/junction_checks.json`, `run_006/junction_checks.json` and `run_007/junction_checks.json` (5.8 MB each; run_006 is byte-identical to run_007)

`latest_sn_review/inputs/` also holds 33 MB and 9.4 MB catalogue copies; that folder was not assessed.

**Overwrites:** none. No tracked file in CJ1, the paper folder, WLJ1, XJ1, FRZ1, FZS1 or JNT2 is modified. The only already-tracked Codex files are `before_correction/CJ1_SCORECARD_at_PAPER72_v1_4.md/.json` (9935bcc45e). The other four `before_correction` copies are byte-identical to git history at e0f529eca4. `test_wlj1_grade.py` is a new file inside a finished lane folder; it overwrites nothing.

**Recommendation, by path:**

- **COMMIT AS IS:**
  - `README.md`, `PLAN.md`, `INDEPENDENT_REVIEW.md` and `verification/VERIFICATION.md`, with this audit as the qualifying note.
  - `calculation/`: `BUDGET_BOUND.md`, all `.py` files except `reproduce.py`, and all `*contract*.json`.
  - `calculation/run_002`, `run_003`, `run_004` and `run_006` in full.
  - From `calculation/run_001`: `results.json`, `manifest.json`, `stdout.txt` and `stderr.txt`.
  - `latest_review/JUNCTION_THEOREM.md`, `TRANSPORT_PATH.md`, `check_junction.py`, `run_checks.py` and `contract.json`.
  - From `latest_review/run_007`: `manifest.json`, `stdout.txt` and `stderr.txt`.
  - `verification/`: `source_checkpoint.json`, `final_checkpoint_receipt.json`, `accepted_manifests.json`, `paper_audit.out`, `paper_mutation.out` and `cj1_audit.out`.
  - `before_correction/manifest.json`.
  - WLJ1: `test_wlj1_grade.py`, `codex_fix_2026_11_14/audit_grader.py` and `contract.json`. From `run_01`: everything except `comparison.json` and `regression_red.txt`.
- **COMMIT AFTER REDACTING** (replace the home prefix with a repository-relative path, or with `<validator>` for the plugin script):
  - `calculation/README.md`, line 159;
  - `calculation/reproduce.py`, line 11 (better: read the validator path from an environment variable);
  - `latest_review/REVIEW.md`, line 181;
  - `verification/audit_results.json`, `audit_results_initial.json` and `cj1_audit_launch_failed.out`;
  - WLJ1 `CODEX_GRADER_VERIFICATION_2026_11_14.md` (3 lines) and `codex_fix_2026_11_14/runner_command.json`;
  - `run_01/comparison.json` and `run_01/regression_red.txt`.

  Redacting README.md or reproduce.py will invalidate `calculation/SHA256SUMS`, so regenerate it or leave it untracked.
- **LEAVE UNTRACKED:**
  - `calculation/run_001/representative_profiles.npz` and `halo_masses.csv`: over 5 MB, regenerable with `reproduce.py --stage 1`, and their hashes are pinned in the manifest.
  - `calculation/run_005/`: a failed serialization run whose stderr has a home path.
  - `latest_review/run_001` to `run_006`: superseded diagnostics, with home paths in stderr and duplicated 5.8 MB files.
  - `latest_review/run_007/junction_checks.json`: 5.8 MB, regenerable in 9 s, hash pinned. Commit it only if the lead accepts a 5.8 MB file.
  - `before_correction/` copies of `COMPLETED_FORM.md`, `SCORECARD.md`, the TeX and `PAPER72_audit.py`: identical to git at e0f529eca4.
  - `latex_compile.json`: a tool response with a home path.
  - `calculation/SHA256SUMS`, if anything above is redacted.
  - Root `CLAUDE_HANDOFF_MASS_BUDGET_2026_11_14.txt`: like the other root handoffs, it has a home path at line 3, and its content repeats the README.
  - `latest_sn_review/`: not assessed; it belongs to another lane.

## Not checked

- The common-radius algebra and the paper TeX (already checked by the lead).
- The z 4.4 rows of the budget table.
- The 76 interior crossings.
- The s ranges and force-residual examples.
- The eta / scope tables (run_003) and the figure.
- COL1's reduction.
- The manifest validator.
- The PAPER72 and CJ1 audit counts.
- `latest_sn_review/`.

## Files

- `audit_a_masses.py`, `audit_a_masses.out` and `audit_a_masses_codeG.out`
- `audit_b_junction_count.py` and `audit_b_junction_count.out`
- `audit_b_weakfield.py` and `audit_b_weakfield.out`

JSON copies were written to `scratch/` and are not committed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
