# CFG689 — BAO with the framework's own ruler: does native pre-switch physics break the dark degeneracy? (FROZEN, before any script or number from this lane)

Block CFG680–689 (owner reserved 2026-10-12); CFG689 is its last id. Owner, 2026-10-19: "Yes: write and commit CFG689 frozen
criteria alone (native-ruler BAO), and queue the run behind NC1x with a waiter. Nothing runs while the 1024³ is live."

## 1. Why this lane exists
CFG681–683 treated the BAO ruler as a free nuisance, q = c/(H0 r_d). With q free, BAO + SN measure only the shape E(z) = H(z)/H0,
and Ω_m trades against the dark energy X(z) = ρ_DE(z)/ρ_DE(0): a0(2.33)/a0(0) = 1.93 / 1.14 / 0 at Ω_m 0.25 / 0.30 / 0.35
(CFG681), so the tracking law stayed degenerate (CFG682/683). Two of the framework's own results say the ruler is not free:
- **CFG654 principle (README, 2026-10-13).** Before the switch turns on, the universe is GR + photons + neutrinos + baryons + cold
  energy (as cold matter) + dark energy, with a0 irrelevant. Linear physics in that era (CAMB) is the framework's own physics.
  Addendum A1 primary input: ω_b 0.02236, ω_c 0.1202 (Planck 2018 VI Table 2, TT,TE,EE+lowE: physical densities set before
  recombination, not late-time fit results) → r_drag = 147.0667 Mpc (`cfg654_ics_results.json`, NATIVE_CMB, CAMB 1.6.6).
- **CFG253.** At most ~3% of today's cold mass can be made after recombination, so ρ_m(z) = ω_m (1 + z)³ in physical units to ≤ 3%.

With r_d fixed, each D_H/r_d is an absolute H(z) in km/s/Mpc, and ρ_DE(z) = ρ_tot(z) − ρ_m(z) − ρ_r(z) at each redshift. Ω_m, H0
and the shape are then no longer free, and the tracking law a0(z) = κ c √(G ρ_DE(z)) (owner rule) has a definite native band.

**Disclosed before freezing (hand arithmetic in the proposing chat, 2026-10-19; D_H only, no D_M, no correlations, no SN,
r_d 147.07 Mpc, ω_m 0.1432 including a 0.06-eV neutrino; the primary below has Σm_ν = 0 as A1 does):**
w(z) ≡ ρ_DE(z)/ρ_crit,100 ≈ 0.376 ± 0.034 (z 0.51), 0.387 ± 0.037 (0.71), 0.299 ± 0.029 (0.93), 0.276 ± 0.065 (1.32),
0.333 ± 0.20 (1.48), 0.284 ± 0.13 (2.33). Constant χ² ≈ 5.9 / 5. Expected from that: tracking √X ≈ 0.9–1.07 out to z 2.33,
rival E(z) 1.7–3.4, e_3σ ≈ 0.08 dex (z 1) to 0.15 dex (z 2.33). These are expectations, never predictions, and cannot be claimed
as confirmed by this lane.
**Also disclosed:** BAO + an early-universe (ω_b, ω_c) prior is standard cosmology in spirit (DESI runs BAO + early-universe CMB
priors). What is new here is only the mapping to the tracking a0(z) and the fact that the record's own CFG654/CFG253 license it.
A constant ρ_DE is ΛCDM's background, so **no outcome of this lane can favour the framework over ΛCDM.**

## 2. Data (verbatim from CFG681; nothing new downloaded)
- DESI DR2 BAO (arXiv 2503.14738v2 Table) exactly as in `CFG681_bao_raw_geometry/cfg681_bao.py` (ANISO six tracers with D_M/r_d,
  D_H/r_d and their correlation; BGS D_V/r_d at z 0.295). Tracers independent; 2×2 covariance per tracer.
- Pantheon+ STAT+SYS (`_external_data/pantheonplus_dr/`, sha256 abf806d9…, as CFG681): non-calibrators with zHD > 0.01; absolute
  magnitude M marginalised analytically (shape only).
- From the CMB, **only ω_b and ω_c** (A1 pair). No θ*, no R, no l_A, no CMB lensing, no late-time CMB fit result.

## 3. Native inputs (primary = CFG654 addendum A1, verbatim)
- ω_b = 0.02236 ± 0.00015, ω_c = 0.1202 ± 0.0014 (Gaussian prior χ² terms; correlation 0 primary; `cfg654_ics.py` PROVENANCE).
  N_eff 3.044, T_CMB 2.7255 K, Σm_ν = 0, flat.
- r_d(ω_b, ω_c): CAMB 1.6.6 `rdrag` with `cfg654_ics.camb_results` settings (nnu 3.044, mnu 0, AccuracyBoost 1.5, h 0.6777 —
  r_d does not depend on h, K2). Inside the sampler a power-law emulator r_d = r_d0 (ω_b/ω_b0)^(−b) (ω_c/ω_c0)^(−c), with b, c from
  CAMB central differences at ±2σ (K2 checks it).
- After recombination: ρ_m(z)/ρ_crit,100 = ω_m (1 + z)³ with ω_m = ω_b + ω_c (+ Σm_ν/93.14 eV in bracket B2). Radiation:
  ω_γ (1 + 0.2271 N_rel)(1 + z)⁴, ω_γ = 2.4728e-5 (record value, CFG642), N_rel = 3.044 (2.029 when one species is massive, B2;
  that species is counted in matter, a declared approximation, < 1e-3 of H² at z ≤ 2.33). ρ_crit,100 = 1.87847e-26 kg m⁻³.

## 4. Model
Flat, as CFG681. H(z)² / (100 km s⁻¹ Mpc⁻¹)² = ω_m (1 + z)³ + ω_r (1 + z)⁴ + w(z). Here w(z) ≡ ρ_DE(z)/ρ_crit,100 (the physical
dark-energy density), piecewise-linear in z on CFG681's nodes {0, 0.4, 0.7, 1.0, 1.5, 2.33}, with all **six** node values free
(w(0) is free too) and w constant beyond 2.33. w may go negative; the data decide, and the fraction of samples is reported.
Derived: h² = ω_m + ω_r + w(0); X(z) = w(z)/w(0); tracking a0(z)/a0(0) = √X (set to 0 where X ≤ 0); rival a0(z)/a0(0) = E(z) =
H(z)/H0. D_M = ∫ c dz/H, D_H = c/H, D_V = (z D_M² D_H)^(1/3), all in Mpc and divided by r_d(ω_b, ω_c).
SN: μ = 5 log10[(1 + z_hel) D_M(z_HD)] + const, with M marginalised (shape only).
Parameters: 6 w-nodes + ω_b + ω_c. Flat priors on the w-nodes over [−2, 3].

## 5. Inference
- **Best fit:** multi-start Nelder–Mead → Powell (CFG681 recipe). Starts: w ≡ 0.25 / 0.31 / 0.38, and two tilted (0.38 → 0.25,
  0.25 → 0.38), with ω_b, ω_c at their centres.
- **Posterior:** Metropolis–Hastings, 4 chains × 60 000 steps, seeds 6891–6894. Gaussian proposal = (2.38²/8) × inverse numerical
  Hessian at the best fit (falls back to diagonal if that is not positive-definite). Burn-in is the first 20%. All derived
  quantities come from the post-burn samples.
- **Safety:** every 5 000 steps the script checks for a live PM / 1024³ / chain process. If it finds one, it exits with code 75
  and writes no verdict. The waiter then re-gates and reruns that mode from the start.

## 6. Primary statistics (BAO + Pantheon+ shape; BAO only reported beside it)
**P1: native bands and the fork target** at z* ∈ {1.0, 1.2, 1.5, 2.33} (CFG683's):
- Tracking √X(z*) and rival E(z*): median, 68% and 95% intervals.
- Separation, with CFG683's conservative closest-edge form on posterior quantiles:
  gap = log10 E₁₆ − log10 √X₈₄; σ_E = log10 E₅₀ − log10 E₁₆; σ_X = log10 √X₈₄ − log10 √X₅₀ (√X floored at 0.01);
  S(e) = gap / √(e² + σ_E² + σ_X²); e_3σ = largest e on CFG683's grid (0.01–1.0, 1000 points) with S ≥ 3.
- **Class** (compares the native tracking 68% width in √X with CFG683's CMB-free BAO+SN band width at z* 1.0 / 1.5 / 2.33 =
  0.853 / 1.596 / 2.183):
  - DEGENERACY BROKEN: native width ≤ ½ of CFG683's at all three;
  - PARTLY BROKEN: at one or two;
  - NOT BROKEN: at none.
- Record samples graded with CFG683 P3's (z*, e): KURVS-CDFS (1.5, 0.30); z~1.2 multi-tracer (1.2, 0.162); RC100/CRISTAL
  optimistic (2.33, 0.125) and realistic (2.33, 0.40). Grades: DECIDES (S ≥ 3), LEANS (2 ≤ S < 3), CANNOT (S < 2).

**P2: constant dark energy with the native ruler.**
- Δχ² = χ²(w ≡ const: 1 node + ω_b, ω_c) − χ²(6 nodes + ω_b, ω_c), taken as 5 dof, converted with CFG681's p → equivalent σ.
- Classes: CONSISTENT WITH CONSTANT (< 2σ), HINT (2–3σ), EVOLVING DE REQUIRED (≥ 3σ).
- Reading: EVOLVING would mean that the tracking law predicts an a0(z) that is not flat (the √X band is that prediction). A
  constant w is ΛCDM's background, so neither class favours the framework over ΛCDM.

**P3 (reported, no verdict):**
- native H0 = 100 h;
- the absolute tracking a0 at each node for κ = ½: a0 = ½ c √(G ρ_crit,100 w), labelled "κ fitted; not a footing change". The
  footings stay 9.36e-11 / 1.13e-10 unless the owner decides otherwise;
- P(w(z*) ≤ 0).

## 7. Brackets (reported with the same classes; the verdict is the primary's)
- **B1 BBN ω_b:** 0.02193 ± 0.00022 (cfg654 PRIMAT row) with ω_c 0.1202 ± 0.0014 (CFG654's declared mixed bracket).
- **B2 one massive neutrino:** Σm_ν = 0.06 eV; ω_ν counted in matter; r_d from CAMB with mnu 0.06.
- **B3 ω_b–ω_c correlation:** −0.5 and +0.5.
- **B4 cold mass not exactly conserved (CFG253 ≤ 3%):** ρ_m = (ω_b + ω_c (1 + f))(1 + z)³ for z ≤ 2.5, with r_d from the early
  ω_c, at f = −0.03 (drain) and +0.03 (made after recombination, all of it before z 2.33: the worst case here).
- **B5 CMB-free:** the ω_c prior is removed (ω_c flat in [0.05, 0.25]). ω_b comes from BBN (0.02193 ± 0.00022), and a Gaussian
  h prior is applied through h² = ω_m + ω_r + w(0) at h = 0.680, 0.700 and 0.7304, each with σ_h 0.0104. The 0.7304 ± 0.0104 row
  is SH0ES (Riess+22, record value in `cfg654_ics.py`); the other two are grid points, not measurements. This maps local H0 onto
  a0(z*). Reported only.
- **B6 node set:** 4 nodes {0, 0.7, 1.5, 2.33}.

If any bracket flips the primary's P1 or P2 class, the verdict line carries "BRACKET-SENSITIVE (B…)".

## 8. Checks (any failure is labelled in the output; no verdict until it is fixed and disclosed)
- **K1:** CAMB rdrag at the A1 pair = 147.0667 ± 0.02 Mpc; at the BBN pair = 147.5453 ± 0.02; at BBN + mnu 0.06 = 147.5381 ± 0.02
  (`cfg654_ics_results.json`).
- **K2:** the emulator matches direct CAMB to ≤ 2e-4 (relative) at four off-centre points (ω_b ± 2σ, ω_c ± 2σ). rdrag changes by
  < 1e-4 (relative) for h ± 0.05.
- **K3:** ruler-free reproduction of CFG681. Implemented in this script's own distance/χ² code, with r_d profiled analytically
  like CFG681's q, w constant, and ω_m + ω_r + w(0) = 0.68² (so Ω_r equals CFG681's):
  - BAO only: χ²_min = 10.5515 ± 0.01 at Ω_m 0.2970 ± 0.001 (CFG681 T1 X≡1);
  - BAO + SN: χ²_min = 1400.143 ± 0.02 at Ω_m 0.3039 ± 0.001 (CFG681 T2 X≡1).
- **K4:** Gelman–Rubin R̂ < 1.02 for the 8 parameters and the P1 derived quantities; acceptance between 0.1 and 0.5 in every chain.

## 9. MUTATE (separate outputs named by mode; each must recover or bite)
- **M1 constant truth.** DESI and Pantheon+ are replaced by the noiseless prediction of the primary's best-fit constant-w model
  (A1 centres) at the same errors. Pass: P2 Δχ² ≤ 0.1, and the tracking 68% bands at all four z* contain 1.
- **M2 vanishing dark energy.** Truth w = w_c × {1, 1, 1, 0.5, 0, 0} at the nodes (w_c is M1's constant). Pass: the best-fit
  nodes are within max(1σ, 0.03) of the truth at every node; P2 Δχ² ≥ 9; the tracking 68% band at z* 2.33 excludes 1.
- **M3 ruler bite.** Primary data with r_d × 1.02. Pass (the result rests on the ruler): the best-fit w(2.33) moves by ≥ 1
  primary posterior σ.

## 10. Verdict line (frozen form)
"P1 <class> (e_3σ at z* 1.0/1.2/1.5/2.33 = …; record samples …); P2 <class> (Δχ² …/5, …σ); native H0 …; brackets …;
MUTATE M1/M2/M3 …; K1–K4 …".
Standing wording: κ fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over
ΛCDM. Never cite the native a0 values as a derivation of κ or as a footing.

## 11. Run plan
Script `cfg689_native_ruler.py` (written after this file is committed). Modes are set by env CFG689_MODE ∈ {primary, M1, M2, M3,
B1, B2, B3m, B3p, B4m, B4p, B5a, B5b, B5c, B6}; outputs are `cfg689[_MODE].out/.json`. Single process, OMP_NUM_THREADS=2, nice 10,
RSS < 1 GB. Queued behind chain6 (NC1x + its scoring) by `_external_data/overnight_chain/cfg689_waiter.sh`. It starts only when
no chain, PM, 1024³ or scorer process is alive and free + inactive ≥ 44 GB, and it re-gates before every mode.
