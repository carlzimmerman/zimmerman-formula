# CFG556 FROZEN CRITERIA: is CFG555's gravitating-field excess intrinsic to the framework's halo profiles, or a PM artefact? A resolution-free halo model

Frozen 2026-10-10, before any script is written or any halo-model number is computed. This file is committed alone and never edited afterwards; later notes go in the README as dated disclosures.

Standing settings: κ = ½ is FITTED; footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s², scored separately, never pooled; flat a0; kernel ν(y) = 1/(1 − exp(−√y)). Candidate B: inside a bound system the total mass is baryons + settled cold energy (the law's round phantom of the retained baryons, up to the edge); the settled mass comes from the halo's own surroundings (drained shell). The cold energy's MASS is still required. Not "theory closed". No PM runs, no downloads; other lanes are read-only.

## 0. The question

CFG555: on the gravitating density, every 512³ PM growth run has max|P/P_S0 − 1| = 0.15–0.19 at k ≤ 1 h/Mpc (excess near k ≈ 0.3–0.4, mostly the source × particle cross term) and P 13–20% low at k ≈ 1. Is that what the framework's halo profiles predict (INTRINSIC), or PM bookkeeping (ARTEFACT)?

## 1. Inputs (declared)

- **Cosmology and linear spectrum:** the PM's own: h = 0.6736, ω_b = 0.02237, ω_c = 0.1200, Ω_m = (ω_b + ω_c)/h², f_b = ω_b/(ω_b + ω_c), n_s = 0.965, σ8 = 0.811, Eisenstein–Hu no-wiggle T(k) exactly as in `CFG361_pm_growth_T5_bookkeeping/cfg361_pm.py` lines 66–79 (copied verbatim; this is the spectrum the PM ICs are drawn from). z = 0, linear.
- **Halo mass variable:** M = M200m [Msun/h], grid 10^8–10^16, ≥ 300 log points.
- **Mass function:** Tinker et al. 2008, Δ = 200m, z = 0 (A = 0.186, a = 1.47, b = 2.57, c = 1.19). **Bias:** Tinker et al. 2010, Δ = 200. δ_c = 1.686. σ(M) from the linear spectrum with a top hat of radius (3M/4πρ̄_m)^{1/3}.
- **ΛCDM profile:** NFW, c200m(M) = 10.14 (M / 2e12 Msun/h)^−0.081 (Duffy et al. 2008, full sample, Δ = 200m, z = 0). Standard model (L-std): truncated at r200m, mass M.
- **Catchment:** turnaround radius r_ta = radius where the mean enclosed density of the NFW extended beyond r200m equals Δ_ta ρ̄_m, Δ_ta = 11.81 (the PM's own z = 0 value, CFG504/CFG555 shared_diag). M_ta = M_NFW,ext(< r_ta). L-ta profile = the NFW extended to r_ta.
- **Baryons (framework):** census retention f_ret = CFG416's `fret_of(log10 M_ta)` (copied verbatim from `CFG515_census_edge_resolution/cfg515_lib.py`); retained M_b,ret = f_ret f_b M_ta. Stars: Moster et al. 2013 z = 0 (M1 = 10^11.590 Msun, N = 0.0351, β = 1.376, γ = 0.608) on M200c [Msun] computed from the same NFW, capped at M_b,ret; Hernquist with half-mass radius 0.015 r200c. Gas = M_b,ret − M*: β-model ρ ∝ [1 + (r/r_c)²]^−1, r_c = 0.1 r200c. These shapes are declared, not fitted.

## 2. The framework halo (per halo, per footing)

- **Law inside the edge:** M_in(< r) = M_b(< r) ν(y), y = G M_b(< r)/(r² a0). Settled cold energy = M_in − M_b.
- **Edge variants:**
  - **E-cen (census, PRIMARY):** r_e = r_M / ln(1 + f_ret f_b/(1 − f_b)), r_M = √(G M_b,ret/a0) (THEORY_v1 R2); retained baryons truncated at r_e and renormalised to M_b,ret. Then the settled mass at r_e equals the catchment's whole cold supply (1 − f_b) M_ta.
  - **E-emg (emergent, CFG541 class-A exhaustion):** baryons untruncated (normalised to M_b,ret inside r_ta); r_e = smallest r with M_in(< r) − M_b(< r) = (1 − f_b) M_ta.
  - **E-s25 / E-s55 (CFG544 kinetic softening, 25% / 55% outward in r_99):** E-cen, with the settled cold part's ρr² tapered linearly from its E-cen value at r1 = 2 r_e − r2 to zero at r2 = 1.25 r_e / 1.55 r_e (settled mass conserved exactly).
  - If r_e ≥ r_ta: r_e := r_ta; the unsettled remainder M_ta − M_in(r_ta) (if positive) follows the L-ta shape over the ball. The number of such halos is reported.
- **Drained shell (R5):** for r_e < r ≤ r_ta, M_F(< r) = M_in(r_e) + [M_ta − M_in(r_e)] · [M_L(< r) − M_L(< r_e)] / [M_ta − M_L(< r_e)]; so M_F(< r_ta) = M_ta (mass conservation, same total as ΛCDM inside r_ta). The shell depletion q = 1 − [M_ta − M_in(r_e)]/[M_ta − M_L(< r_e)] is reported. Nothing outside r_ta in either case.
- **Retention variants:** census f_ret (PRIMARY); f_ret = 1 (the PM runs' value, PM-matched).

## 3. Halo-model spectra

- U(k|M) = Σ_i ΔM_i j0(k r_i) over each halo's cumulative mass profile on a log radial grid (≥ 1500 points to r_ta, or r200m for L-std).
- P_1h = ∫ dM n (U/ρ̄_m)²; P_2h = P_lin I(k)², I(k) = ∫ dM n b U/ρ̄_m + A_miss, A_miss = 1 − ∫ dM n b M/ρ̄_m (missing low-mass mass with U = M, the standard correction). For the r_ta-scoped models the 2-halo integral is divided by ∫ n b M_ta/ρ̄_m (so I → 1 at k → 0; the same normalisation for L-ta and F).
- **PRIMARY ratio:** R(k) = 1 + [P_F,ta(k) − P_L,ta(k)] / P_L,std(k), k = 0.05–3 h/Mpc.
- **Reported alternatives (not gating, but stated):** R_ratio(k) = P_F,ta/P_L,ta; and the "r200m scope" (catchment = the r200m ball, supply (1 − f_b) M200m, standard normalisation): R_200 = P_F,200/P_L,std.
- **σ8:** of the halo-model (nonlinear) density, σ8²_F = σ8²_L,std + ∫ ΔP W² k² dk/2π²; report σ8,F/σ8,L.

## 4. Comparison with the PM (read-only)

- PM gravitating ratio r_PM(k) = P_grav/P_S0 from CFG555's caches (`_external_data/cfg555_work/`) and the matched S0 JSONs: 512³ runs 425_R3_can_512, 439_A_alt_512, 439_B_DEcan_512, 460_can_512_s360, 518_DCcan_512; 256³ runs 424_TAcan, 424_TAalt. Numbers are re-read from CFG555, never retyped.
- **PM-matched halo model:** f_ret = 1, E-cen, framework profile only for halos with M_ta ≥ M_res and L-ta otherwise; M_res = 10^12.3 Msun/h at 512³ (CFG504's SO finder threshold) and 10^13.2 at 256³ (×8 particle mass).
- **Reproduction test (per PM run, matched footing):** REPRODUCED if at the PM's k_at (its max|P−1| bin) 0.5 ≤ (R_HM − 1)/(r_PM − 1) ≤ 2, AND the sign of R_HM − 1 at k = 1 matches r_PM − 1 there. Otherwise NOT REPRODUCED.
- **Validation of the ΛCDM halo model on our boxes:** P_L,std / P_S0 at the S0 bins in 0.1 ≤ k ≤ 1 (256³, `cfg359_S0_FLAT_canonical_N256`) and 0.1 ≤ k ≤ 2 (512³, `cfg411_S0_Rc3_MIXA_FLAT_canonical_N512`). Label GOOD if within ±20% in every such bin, else POOR. POOR does not change the verdict but is stated beside it (the ratio is a halo-model ratio; absolute agreement is not needed for it).

## 5. Verdict per footing (PRIMARY: census f_ret, E-cen, all halos)

Let E = max(R − 1) and D = min(R − 1) over 0.05 ≤ k ≤ 1.
- **INTRINSIC:** E > 0.10.
- **ARTEFACT:** max|R − 1| ≤ 0.10 over k ≤ 1 AND the PM-matched halo model does NOT reproduce the 512³ PM run(s) of that footing.
- **MIXED:** otherwise (|R − 1| ≤ 0.10 but the PM-matched model reproduces the PM; or E ≤ 0.10 while D < −0.10).
- The variants (E-emg, E-s25, E-s55, f_ret = 1, R_ratio, R_200) are reported with their own E/D; if any variant's class differs from the primary, the verdict carries the note "VARIANT-SENSITIVE" with the list.
- **Drivers:** the contribution of each mass decade to ΔP at k = 0.35 and k = 1; and M_F(< r)/M_L(< r) at r/r_ta = 0.1, 0.2, 0.3, 0.5, 1 for log M_ta = 12, 13, 14, 15.
- **Observational context only (no verdict input):** what R(k) and the σ8 ratio imply for weak-lensing S8 and small-scale power; KiDS-1000 / DES Y3 / Planck S8 values are recalled and PROVISIONAL.

## 6. Controls (default run; a failed control is reported and labels the lane NO LABEL)

- **C1** σ8 of P_lin = 0.811 to 1e-3.
- **C2** 2-halo normalisation: I(k = 1e-3) = 1 to 1e-3 for L-std, L-ta and F.
- **C3** mass conservation: |M_F(< r_ta) − M_ta|/M_ta ≤ 1e-6 for every halo (bare-law MUTATE excepted).
- **C4** the numerical U(k) of a truncated NFW matches the analytic truncated-NFW transform to 1e-3 (k = 0.05–3, three masses).
- **C5** (reported) P_lin vs the S0 z_i spectrum rescaled by D(z_i)², 0.05 ≤ k ≤ 0.5: the ratio is printed (cosmic variance and the lattice expected).

## 7. MUTATE (`CFG556_MUTATE=1`; separate `_MUTATE` outputs; all three must bite)

- **M1 framework profile := L-ta:** |R − 1| ≤ 1e-10 at every k.
- **M2 edge removed:** bare law to r_ta (phantom of the untruncated retained baryons out to r_ta, no supply cap, no shell drain): E must INCREASE relative to the primary (each footing).
- **M3 drained shell removed:** the shell keeps the L-ta mass (in-ball mass then exceeds M_ta): max over 0.3 ≤ k ≤ 1 of |R_M3 − R| ≥ 0.01 (each footing).

## 8. Outputs

`cfg556_halo_model.py`, `cfg556_halo_model.out` / `_MUTATE.out`, `cfg556_results.json` / `_MUTATE.json`, `README.md`. Lane folder only; committed with message starting "CFG556 results:"; not pushed. Compute: nice -n 10, ≤ 4 threads.
