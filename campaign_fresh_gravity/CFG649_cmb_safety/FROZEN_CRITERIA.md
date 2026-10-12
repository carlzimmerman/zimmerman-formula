# CFG649 FROZEN CRITERIA: the CMB-SAFETY GATE (primary CMB switch-off + CMB lensing from the framework's own gravitating P(k, z))

- **Written:** 2026-10-12, committed ALONE before any CFG649 code or number.
- **Settings:** κ = ½ FITTED; footings never pooled (canonical only: P1 is the only finished RES 1024³ run; alt = P2 stays PENDING); "cold energy"; the cold energy's MASS is required; no particle species; not "theory closed". Nothing here says the data favour the framework.
- **Read only:** `CFG596_lean_pm_1024/cfg596_pm.py` (production freeze 6323b630f), the stored CFG596 outputs in `_external_data/cfg596_work/P0` (S0) and `P1` (candidate B, RES canonical) — JSON + 256³ block-mean meshes. Planck 2018 VIII MV band edges and fractional band errors are read from the committed `real_research/cross_thread_review_2026_09_26/XR26_cmb.py` (typed published table). Nothing is downloaded. The running 1024³ job (cfg636_pm.py), the cfg640 waiter and the cfg625 driver are not touched; this lane is 1 process, ≤ 2 GB, `nice -n 10`.
- **Yardsticks:** no ΛCDM fit, HMcode/halofit, CLASS/CAMB spectrum or standard-MOND curve enters any verdict. The comparison is framework (F) vs the same-pipeline S0 run, as in CFG596.

## Disclosures before freezing

- Read before this file (code reading, not measurement): cfg596_pm.py (forces / source / catchment / snapshot logic), CFG596 README (its published B(z = 0) at k 0.3–4: 1.186 / 1.252 / 1.206 / 1.103 / 1.035), CFG630 README (settling → dark energy ~1e-6 of ρ_DE since z = 1, ≤ 3.8e-6 in total), CFG324 / XR26 lensing code (Limber form, band averaging).
- PRINTED before this file: the scalar snapshot diagnostics of P0/P1 (σ8, σ8_grav, n_catch, e_sum, src_sum at z_i, 1, 0.7548, 0.5, 0.2562, 0). In particular: at z_i = 49 P1 has n_catch = 1 (background only), e_sum = 0, σ8_grav identical to P0; at z = 1 P1 already has n_catch = 786 and σ8_grav 0.5547 vs 0.5224. The k-bin grid (512 bins, first 0.0802 h/Mpc, 127 bins ≤ 8.04) was printed. NO P(k) ratio at any k other than CFG596's published z = 0 values was looked at.
- The 1024³ run stored NO diagnostics between z_i = 49 and z = 1 (snapshots only at z_i, 1, 0.7548, 0.5, 0.2562, 0), so the in-box switch-on epoch is NOT measured. This lane does not rerun the engine.

## Part A. Primary CMB (argument + check; no new physics)

Claim to be checked: at z ≈ 1100 candidate B's switch 1_B is off, cold energy is ordinary cold collisionless matter (Ω_c/Ω_b = 5.364, background as matter), a₀ and settling play no role, and settling energy handed to dark energy is ≲ 1e-6 of ρ_DE (CFG630).

The rules that must carry it (stated from the engine, the spec CFG518/524/527 and THEORY_v1):
- R-A1 the phantom source exists only on the catchments (union of turnaround balls around RESOLVED peaks: δ ≥ 3(τ − ε) and enclosed mean 1 + δ ≥ Δ_ta(z) on R ≥ r_min); with no catchment the engine returns src ≡ 0 and the potential is exactly S0's;
- R-A2 the source is zero-sum per catchment component (mass conserved; the background is untouched);
- R-A3 a₀ enters only through ν(y) inside switched cells (FLAT branch: a₀ constant; the DE-tracking branch would make a₀ smaller at high z, still gated);
- R-A4 the settling sink to dark energy (CFG542/630) is ∝ 1_B 1_C and so zero before turnaround.

Checks (script `cfg649_cmb_safety.py`, part A):
- A1 (data, P1 vs P0 at z_i): n_catch ≤ 1, e_sum = 0 and max |P_grav,F/P_grav,S0 − 1| ≤ 1e-6 over all k bins → the switch is OFF at the start of the run.
- A2 (code): a static scan of cfg596_pm.py lists every place a₀ or the redshift enters, and confirms the source path is multiplied by the catchment mask (no high-z path outside the catchments). Reported as a list; a path that adds a source outside catchments is a LOOPHOLE.
- A3 (estimate, labelled ESTIMATE): with the engine's own linear spectrum (EH IC × D(a), matter + Λ background, no radiation — this OVERestimates high-z growth, the conservative direction), the expected number of linear peaks above the turnaround threshold δ_lin,ta (spherical collapse, 1.062 in EdS) at z = 1100 inside the whole last-scattering volume, for every Lagrangian scale R ∈ [1e-3, 10] Mpc/h: log10 N_max. PASS if N_max < 1e-10 (switch provably off at recombination). Also reported: the in-box (L = 100, r_min = 0.78125) switch-on redshift estimate z_on (N = 1), context only.
- A4 (context): CFG630's settling → dark energy fraction, copied from its JSON (no new computation).
- Primary-CMB verdict: SWITCH-OFF CONFIRMED if A1, A2 (no loophole) and A3 pass; otherwise LOOPHOLE (named). The primary-CMB physics in the switch-off era is GR-linear and INHERITED; the framework adopts it there. No primary-CMB spectrum is computed or fitted here.

## Part B. CMB lensing from the framework's own gravitating field

**Field.** The lens is the GRAVITATING field δ_grav (CFG555 definition, stored as P_grav), the same convention CFG596 used for shear. Context only: the same numbers on the particle field.

**Ratio.** R(k, z) = P_grav,F(k, z) / P_grav,S0(k, z) at the stored snapshots (z = 1, 0.7548, 0.5, 0.2562, 0; R ≡ 1 measured at z_i = 49 by A1). Between snapshots: linear in a. Box support: k ∈ [k_lo, k_hi] = [0.0802, 8.04] h/Mpc (CFG596's support; first bin to πN/(4L)).

**Declared extrapolation rules (bracket).**
- Redshift above z = 1: **Z-b (canonical)** R − 1 linear in a between the two measured anchors (a = 0.02: R ≡ 1; a = 0.5: R(k, 1)); **Z-a (low)** R = 1 for z > 1; **Z-c (high, unphysical upper bound)** R(k, z) = R(k, 1) held for all 1 < z ≤ 50.
- Large scales k < k_lo: **K-a (canonical)** R = 1 (a zero-sum, compensated source has δ_src ∝ k² as k → 0); **K-b (high)** R held at the mean of the three lowest box bins.
- Small scales k > k_hi: R held at its value at k_hi (both brackets).
- **S0 weighting baseline** (enters only as weights of the ratio): **base-1 (canonical)** the S0 PM P_grav(k, z) inside the box support at z ≤ 1 (linear in a between snapshots), and outside it the engine's own linear spectrum P_lin0(k) D(a)²; for 1 < z ≤ 50 inside the box support the linear spectrum times the z = 1 nonlinear factor N(k) = P_PM,S0(k, 1)/P_lin(k, 1), with N − 1 scaled by (D(z)/D(1))²; for k > k_hi a power-law continuation with the slope over [k_hi/2, k_hi]. **base-2** linear P_lin0 D² everywhere. Both are the run's own inherited ingredients (EH IC, flagged); neither is a fit.
- The verdict bracket is all 2 × 3 × 2 = 12 combinations of {base-1, base-2} × {Z-a, Z-b, Z-c} × {K-a, K-b}; canonical = (base-1, Z-b, K-a).

**Projection.** Limber, flat background of the engine (h = 0.6736, Ω_m = 0.3138, flat w = −1, no radiation; flagged inherited), χ_* at z_* = 1090, z ∈ [1e-3, 50]: C_L^φφ = 4/(L+½)⁴ ∫ dχ [1.5 Ω_m H0² (1+z) (χ_* − χ)/χ_*]² P(k = (L+½)/χ, z). Units cancel in every ratio.

**Statistics (frozen).**
- Primary: **ΔA_lens = A_F/A_S0 − 1** on Planck 2018 VIII MV bands 8–400 (9 bands): per band A_b = BP_F,b / BP_S0,b with BP = mean over integer L in the band of L²(L+1)² C_L^φφ; A = Σ w_b A_b / Σ w_b, w_b = 1/σ_A,b² (the record's XR26/CFG324 amplitude estimator with S0 in place of the fiducial). The FFP10 fiducial column is NOT used.
- Secondary (reported, same rule applied as a label): ΔA on Planck MV 8–2048 bands (14 bands); ΔA_ACT-range = uniform weight over L 40–763 (approximation: ACT DR6 bandpowers are not on disk).
- Secondary (reported, no verdict role): Δχ²_rel = Σ_b ((A_b − 1)/σ_A,b)² on 8–400 and 8–2048 — the χ² cost of F if S0 sat exactly on the data (bands treated independent).
- Coverage: f_cov = fraction of the S0 band-weighted Limber integrand (8–400 and 8–2048) from {z ≤ 1 and k_lo ≤ k ≤ k_hi}; also the fractions from z ≤ 1 (all k) and from the box k-range (all z).

**Data constraint.** The raw Planck PR4 and ACT DR6 lensing bandpowers / covariances are NOT on disk (checked 2026-10-12) and are not downloaded. The S0-relative constraint σ_A uses the published amplitude errors as LABELLED CONTEXT: Planck 2018 8–400 σ = 0.028 (typed in XR26; PR4 quotes 1.011 ± 0.028 context), ACT DR6 σ = 0.023 (1.013 ± 0.023, context). The published central values are NOT used (they are relative to a ΛCDM fiducial).

**Pass rule (primary, Planck 8–400, σ = 0.028, 2σ = 0.056).**
- **SAFE** if |ΔA| ≤ 0.056 for every one of the 12 bracket members;
- **CONDITIONAL** if the canonical |ΔA| ≤ 0.056 but some bracket member exceeds it;
- **UNSAFE** if the canonical |ΔA| > 0.056; **UNSAFE-ROBUST** if every bracket member exceeds it.
- Also reported (label only): the same rule at the ACT σ = 0.023 (2σ = 0.046) on the ACT-range statistic.
- A lane whose canonical ΔA is UNSAFE fails the CMB-safety gate; CONDITIONAL means the gate is not decided by this box and needs high-z / large-box coverage.

## MUTATE (`CFG649_MUTATE=1`, separate outputs)

- **M1** F ≡ S0 (P0 JSON passed as both): ΔA = 0 to ≤ 1e-12 in every bracket member and every statistic; Δχ²_rel = 0.
- **M2a** R ≡ 1.10 at all k, z: ΔA must equal 0.100 to ≤ 1e-9 (all statistics).
- **M2b** R = 1.10 on the covered region only (z ≤ 1, k_lo ≤ k ≤ k_hi), 1 elsewhere: ΔA must equal 0.10 × Σ_b w_b f_cov,b / Σ_b w_b to ≤ 1e-9 (independent computation of the per-band coverage).
- **M2c** inject CFG596's own measured boost B(k) = P_grav,P1/P_grav,P0 at z = 0, held for all z ≤ 1 (K-a, Z-a): ΔA must be > 0 and agree with an independent midpoint-in-χ quadrature of the same input to ≤ 1e-3 relative.
- MUTATE bites only if M1 returns exactly zero and M2a/M2b/M2c reproduce their computed amounts.

## Deliverable for other lanes

The README carries a **CMB-SAFETY CHECKLIST**: every settling-fix lane (CFG636 capped source, CFG640 two-phase, CFG644 neighbour edge, CFG646 gas expulsion, CFG647 per-host supply, CFG648 splashback) must (1) show the switch-off condition at its own z_i (A1) and that its new rule adds no source outside catchments (A2-type statement), and (2) run this script on its own PM output vs its same-realisation S0 and report ΔA (canonical + bracket) with the label above.

Commit rule: specific paths only; no push.
