# ZT4_zstar_outer_lensing: FROZEN CRITERIA (committed alone with the ledger, before any script or number)

Test: **Z-T4 (outer lensing)** of design Z★ = v3s-OC, exactly as frozen in
`rebuild_2026_10_22/Z1_successor_design/TEST_PLAN.md` §2 (commit 0d1959a4f5); design in `Z1_successor_design/DESIGN.md`.
κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), scored separately, never pooled.
No dark-matter particle: the cold sector is one pressureless medium ("cold energy", a field). Never "theory closed".
Nothing here may be read as "the data favour the framework". Ledger: `ASSUMPTION_LEDGER.md` (committed with this file).

## 0. The frozen line (verbatim from TEST_PLAN.md)

"The owner law truncated at r_s(f_own) plus a two-halo term from the linear dust power spectrum (unowned medium = dust;
C2 transfer). f_own bracket fixed here: {5.364, 50}. PASS: Δχ² (Z★ − zero-field v3) ≤ +4 on P2 at both bracket ends and
both footings. FAIL: ≥ +9 at both ends. Otherwise UNDECIDED."

Everything below is an implementation choice for that line, fixed now, before any Z★ number exists.

## 1. Inputs (read only; pinned)

| input | commit | sha256 (first 16) |
|---|---|---|
| `P2_spec_isolated_lensing/p2_spec_isolated_lensing.py` (data, estimator, covariance, zero-field v3 model) | 1ebfa54245 | 8420630a1cc5970e |
| `P2_spec_isolated_lensing/p2_spec_isolated_lensing_results.json` (committed profile, cov, models) | 1ebfa54245 | a77afd7e2990ccdc |
| `F2_outer_lensing/f2_aqual.py` (AQUAL solver/projector, imported by P2) | 7c8c3d5302 | 7420d7290e63132a |
| `F3_growth_audit/f3_growth_audit_results.json` key "K2" (backgrounds A, B) | 059766caa5 | 5e0df3b412ddcfeb |
| `Z1_successor_design/TEST_PLAN.md`, `DESIGN.md`, `z1_successor_design.py` (K5 closed form) | 0d1959a4f5 / f65f181cc1 | — |

P2 is never edited. Its source is read and executed in this lane's process up to (not including) its verdict loop
(`VER = {}; AMP = {}`, section 10), with argv = (KiDS reader cache, work dir, `--phase=B`). That rebuilds P2's samples
(same seeds), reads P2's measurement cache, and gives P2's own `stack`, `amps`, `town_per_lens`, `tnbr`, `point_part`,
`bin_avg`, `meff_lens`, `MEAS`, `PC/PJ/PD` etc. The work dir is a **copy** of P2's scratch caches in this session's
scratch space, so nothing outside this lane is written. P2's output-writing section is never reached.

## 2. Model Z★ (per footing, per f ∈ {5.364, 50}; the same f for every galaxy, lens and neighbour)

- **Owner law inside r_s, owner frame (no EFE).** Each galaxy's baryons are P2's T_central inventory (M★, cold gas from
  B21's relation, hot CGM 0.5 M★ as a uniform 100 kpc sphere for the lens, a point for neighbours). Isolated AQUAL,
  μ = x/(1+x) (P2's case (a) profile, y_e = 0: R2 puts the owner in its own free-fall frame).
- **Truncation (R1 capacity).** Enclosed total mass M_Z(r) = min(M_iso(r), (1 + f) M_b), M_b = M★ + M_cold + M_hot.
  For a point mass M_iso(r_s) = (1+f) M_b exactly at r_s = r_M √(f(f+1)), r_M = √(G M_b / a₀) (Z1 K5), so the cap is the
  frozen "held phantom stops at the owned dust". Beyond r_s the projection uses a constant-mass tail.
- **T_own,Z:** P2's T_own table machinery (`meff_lens` with y_e = 0, then the cap, then `AQ.delta_sigma` and P2's
  12-point area-weighted `bin_avg`), on P2's native-M★ grid; per lens interpolated exactly as `town_per_lens`.
- **T_nbr,Z:** P2's neighbour machinery with every neighbour's dimensionless profile m(s) = min(M_iso(s), 1 + f)
  (s = r/r_M) in place of P2's node y_e = 0, i.e. P2's `ext_profile` / `mc_table` / `gtable` code re-run on that m
  (re-implemented line for line in this lane, constant tail), plus P2's exact point part. Pairs, distances, types and
  the linear sum are P2's.
- **Two-halo term (unowned medium = dust).** For lens centres only:
  ΔΣ_2h(R, z) = b · ρ̄_c0 (1+z)² ∫ k dk/(2π) P_lin(k, z) J₂(k R (1+z)), R physical (P2's bins), P_lin = CLASS linear
  matter power at the lens redshift (Mpc units), ρ̄_c0 = ω_cdm · 2.77537e11 M☉/Mpc³ (dust density of that background).
  - **Bias convention (frozen): b = 1**, the lens is an unbiased linear tracer of the dust field. POSITED (no native
    bias exists; no fitted constant introduced). Iso-randoms and randoms carry b = 0 (random points), so the term
    enters only through the lens stack.
  - Area-averaged over each bin with P2's `bin_avg`; tabulated on z = 0.00–0.55 (step 0.025), linear in z per lens.
  - CLASS settings = F3's `class_run` (N_ur 3.044, T_cmb 2.7255, P_k_max 60 h/Mpc), z_max_pk 0.6; k from 1e-5 to the
    CLASS maximum, power-law extrapolation (log-log slope of the last decade) to 1e3 /Mpc; 4·10⁵ log-spaced k points.
  - **Backgrounds:** A = C2 c2b g = 1 refit, B = CFG886 background with A's A_s, n_s, ω_b (F3 K2 parameters). Both are
    run; both enter the verdict (section 4).
- Per centre model: m_Z = T_own,Z (lens rows) + T_nbr,Z (every centre) + ΔΣ_2h (lens rows); stacked with P2's `stack`
  on S3 as Δ = L − I3, with P2's WW weighting and 36-patch jackknife.
- Zero-field v3 = P2's case (a) model, taken from the executed P2 code (checked against the committed JSON, K0).

## 3. Statistic

- Data vector and covariance: P2's primary S3 Δ = L − I3 and its 15 × 15 delete-one jackknife covariance (36 patches).
- **χ² on the outer range O1 ∪ O2 (bin centres 0.4 < R ≤ 3.0 Mpc, 7 bins)** with the 7 × 7 sub-block inverted and the
  Hartlap factor (36 − 7 − 2)/(36 − 1). Δχ² = χ²(Z★) − χ²(zero-field v3 (a)), per footing, per f end, per background.
- The model's own jackknife scatter is not added to the covariance (as in P2's profile covariance).

## 4. Verdict

Per footing: **PASS** if Δχ² ≤ +4 at both f ends on both backgrounds; **FAIL** if Δχ² ≥ +9 at both f ends on both
backgrounds; otherwise **UNDECIDED**. Lane: PASS iff both footings PASS; FAIL iff both footings FAIL; otherwise
UNDECIDED (a footing split is stated). No knob is scanned; no bracket value, bias, range or background is changed after
a number is seen. Post-result changes go in a dated `AMENDMENT_*.md`, never into this file.

## 5. Reported only (not verdict lines)

(r1) the full 15-bin χ² (Hartlap (36 − 15 − 2)/35) and the inner range (0.03–0.31 Mpc, 6 bins) Δχ²; (r2) diagonal-only
χ² on the outer range; (r3) Z★ without the two-halo term; (r4) Z★ with the two-halo term and without T_nbr (the
double-count bracket: catalogued neighbours' owned mass is also inside ξ_lin); (r5) the two-halo term with the
Sheth–Tormen bias of the owner's total mass (1+f) M_b on the native σ(M) (EXTERNALLY CALIBRATED); (r6) P2's amplitudes
A_O1, A_O2 for Z★; (r7) the S1 sample (L − I1), P2's secondary; (r8) r_s of the median S3 lens. F2 (secondary per
TEST_PLAN) is reported only if it can be done without a new pipeline; otherwise the README says why not.

## 6. Checks (`zt4_outer_lensing.py`; one `K* PASS/FAIL` line each; exit 0 iff all pass)

- **K0 P2 replay.** The executed P2 code reproduces the committed S3 profile d, σ, m_a, m_b (both footings) to ≤ 1e-9
  relative (max |Δ| / max |value|), P2's committed checks are all true, and the zero-field v3 outer χ² recomputed from
  the committed JSON (d, m_a, cov) equals this lane's to ≤ 1e-6 relative, per footing.
- **K1 untruncated limit.** At f = 1e7 and no two-halo term, the Z★ machinery reproduces P2's T_own (a) table to
  ≤ 1e-3 relative (max over mass × bin, relative to each bin's value) and the stacked S3 model m_a to ≤ 1e-3
  (max |Δ| / max |m_a|), per footing.
- **K2 cap identity.** Point mass: ν((r_M/r_s)²) = 1 + f to ≤ 1e-12 at f = 5.364 and 50; the capped extended tables
  satisfy M_Z ≤ (1+f) M_b everywhere and M_Z = M_iso wherever M_iso < (1+f) M_b.
- **K3 two-halo machinery.** (a) σ₈ from this lane's integral of CLASS P_lin(k, 0) vs CLASS `sigma8()` and vs F3 K2 σ₈,
  each ≤ 1e-3 relative, for A and B; (b) the J₂ Hankel integrator on P(k) = exp(−k²s²) (analytic
  ∫ k dk/(2π) e^{−k²s²} J₂(kR) = [1 − e^{−x}(1 + x)]/(πR²), x = R²/4s²) ≤ 1e-4 relative at R = 0.4, 1, 3 Mpc.
- **K4 statistic.** The 7 × 7 covariance sub-block is positive definite and every χ² is finite.
- **K5 resources.** Each phase's peak RSS < 1 GB.
- **`--mutate`:** the data use cross shear (WX) in place of tangential (WG) after P2's code has run. K0 must FAIL and
  the run exit 1. Outputs `zt4_outer_lensing_MUTATE.out` and `zt4_outer_lensing_results_MUTATE.json`.

## 7. Compute

`OMP_NUM_THREADS=1 nice -n 15 python3 zt4_outer_lensing.py <KiDS reader cache> <work dir copy> [--mutate]`, run as two
sequential processes (phase C: CLASS and the two-halo tables, K3; phase S: P2 replay, Z★ model, scoring), each < 1 GB
RSS, single thread, no multiprocessing, no downloads, no simulation. `vm_stat` checked before (free + inactive ≥ 12 GB).
