# X54_cold_de_exchange: FROZEN CRITERIA (committed alone, before any script or number)

**Question (owner's framing).** The owner calls the cold component "cold dark energy, paired with dark energy". Do the
CMB, DESI DR2 BAO and supernova data allow, or prefer, an energy exchange between cold dark energy (ρ_c, the gravitating
w ≈ 0 clumping field component; not matter, not a particle) and dark energy (ρ_DE)? If they do, does the a₀(z) implied
by the tracking law a₀(z) = κ c √(G ρ_DE(z)) (κ = ½ FITTED) match the record's native a₀(z) (CFG689)?

Standing: κ = ½ FITTED. No dark-matter particle. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Never "theory
closed"; nothing here may say the data favour the framework. ΛCDM is the name of the external rival only. A flat a₀ is
only the w = −1 case and is never used as a cap on the exchange (owner rule 10-06).

## 0. Record read before freezing (not blind)
- CFG253 README + criteria: its 3 % (F_made ≤ 0.03 of today's cold mass made after z = 1090) is a DECLARED convention
  (G1), not a likelihood. Its a₀ already tracks ρ_DE. The flat-a₀ piece is CFG131's 1 % line (max_{z≤5}|a₀(z)/a₀(0) − 1|
  < 0.01), which CFG253 reports as allowing only 0.5–1.6 % of the cold mass; that line is a flat-a₀ cap and is NOT used
  here. CFG253 numbers seen: Q = ξHρ_c at F_made 0.03 ⇔ ξ = 0.00435; Q = ξHρ_DE at 0.03 ⇔ ξ = 0.0344 (its declared
  Ω values).
- CFG131 (door 8): Q^μ = Q u_c^μ; a w = −1 vacuum cannot carry a density perturbation in the cold frame (dust theorem).
- CFG176/CFG195 (door 11: a Λ cannot flow; NEC column bound), CFG360 (PARTIAL, no mechanism), X24b (vacuum heating,
  ε ~ 1e-6), X34 (cold component must be dust-like by z ≈ 5e4; its patched-CLASS + C2-likelihood + Gauss–Newton refit
  machinery is the template here), X35 (a₀ tracking EDE), CFG689 summary (native √X(z) bands, 68 %).
- C7 ΛCDM refit (χ² 1003.475, plik 582.40 / lowTT 24.31 / lowEE 396.72) and the one-run CLASS timing (≈ 5 s, 0.28 GB)
  were seen. No exchange number has been computed.

## 1. Model family (standard interacting vacuum, geodesic cold dark energy)
Flat FRW, GR. Components: photons, massless neutrinos (N_eff 3.044, as C7), baryons, cold dark energy ρ_c (w = 0), dark
energy ρ_DE (w = −1 vacuum stress), exchange Q:
  dρ_c/dt + 3Hρ_c = +Q,   dρ_DE/dt = −Q.   **Sign: ξ > 0 means energy flows DE → cold.**
- **M-C (primary):** Q = ξ H ρ_c ⇒ ρ_c = ρ_c0 a^{−(3−ξ)}, ρ_DE = ρ_DE0 + ξρ_c0/(3−ξ) (a^{−(3−ξ)} − 1).
- **M-D (reported):** Q = ξ H ρ_DE ⇒ ρ_DE = ρ_DE0 a^{−ξ}, ρ_c = (ρ_c0 − B) a^{−3} + B a^{−ξ}, B = ξρ_DE0/(3−ξ).
- **Perturbations (both):** energy transfer along the cold 4-velocity, Q^μ = Q u_c^μ: **zero momentum transfer in the
  cold dark energy rest frame**; δQ = 0 on cold-comoving slices, so the vacuum carries no perturbation in that frame
  (δρ_DE = 0, CFG131's consistency condition for a w = −1 stress). In synchronous gauge (comoving with the geodesic cold
  component, θ_c = 0): δ_c' = −h'/2 − (aQ/ρ_c ℋ) ℋ δ_c, i.e. a dilution rate r = ξ (M-C) or ξρ_DE/ρ_c (M-D). Synchronous
  gauge only; a Newtonian-gauge run is refused by the patch.
- **Implementation:** a documented patch to the record's pristine CLASS v3.3.4 tree (as X34), built outside the repository,
  diff committed (`x54_exchange.patch`). ξ and the model are read from the environment; unset ⇒ binary identical to
  vanilla.

## 2. Data and likelihood (raw likelihoods, framework's own background)
- **CMB:** C2's plik-lite + low-ℓ TT + low-ℓ EE + A_planck prior, read-only exec of C2's likelihood block, as X34/Q6.
- **BAO:** DESI DR2 (6 anisotropic D_M/r_d, D_H/r_d with correlations + BGS D_V/r_d), the table verbatim from CFG689.
  D_M, H(z) and r_d come from the same CLASS run (CLASS's own drag sound horizon), not from an emulator.
- **SN:** DES-SN5YR (Dovekie, CFG684/CFG689 loader) **primary**; Pantheon+ (non-calibrators, zHD > 0.01) and Union3
  (nodes) reported; absolute magnitude marginalised analytically (CFG689's sn_chi2 form). Never pooled across SN sets.
- **Coordinator / owner rule (binding, 10-26): no ΛCDM-derived inputs.** No Planck best-fit Ω_c/Ω_b (5.364) and no
  ΛCDM background prior. The cold dark energy abundance ω_c, ξ and the CMB parameters (ω_b, 100θ_s, ln10¹⁰A_s, n_s, τ,
  A_planck) are fitted to the raw likelihoods on the exchange background. Anything still inherited is listed in
  ASSUMPTION_LEDGER.md. C7's ΛCDM refit parameters are used ONLY as start values for the optimiser; the ξ = 0 point is
  refitted on the same data and machinery as every other point.
- The cosmological fit contains no a₀; footings enter only the secondary a₀ verdict (absolute a₀ = footing × √X).

## 3. Statistic
**Profile likelihood in ξ** on a coarse grid with full refits (X34's Gauss–Newton/Broyden steering: plik + priors +
BAO + SN whitened residuals; graded χ² = plik + lowTT + lowEE + A-prior + BAO + SN). No MCMC.
- M-C grid: ξ ∈ {−0.012, −0.008, −0.004, −0.002, 0, +0.002, +0.004, +0.008, +0.012}; if Δχ² < 3.84 at an edge,
  extend that side by doubling (to |ξ| ≤ 0.1).
- M-D grid: ξ ∈ {−0.6, −0.4, −0.2, −0.1, 0, +0.1, +0.2, +0.4, +0.6}; same extension rule (to |ξ| ≤ 1.5).
- Pantheon+ / Union3 profiles may use the 5 inner + any needed outer points, started from the DES-SN5YR best fits.
- χ²_min(ξ) is interpolated by a cubic spline on the grid. **ξ̂** = argmin; **Δχ²₀** = χ²(ξ = 0) − χ²(ξ̂); the **95 %
  interval** = {ξ : χ²(ξ) − χ²(ξ̂) ≤ 3.84}.
- A grid point counts only if its refit converged (fall of the steered χ² < 0.05 on the last step, or ≤ 8 iterations
  with the graded χ² non-increasing).

## 4. Verdict classes (primary: M-C, DES-SN5YR; same rule printed for every model × SN set)
- **EXCHANGE PREFERRED (direction)** if Δχ²₀ ≥ 4.0 (ξ ≠ 0 at ≥ 2σ, 1 dof); direction = DE → cold if ξ̂ > 0, else cold → DE.
- Else, with the 95 % interval closed on the grid and containing 0:
  - **EXCHANGE ALLOWED (bound ξ ∈ [lo, hi])** if the interval permits a produced cold fraction F_made ≥ 0.03 (CFG253's
    declared tolerance) at either end, i.e. the data are looser than the record's convention;
  - **EXCHANGE EXCLUDED BEYOND [lo, hi]** if both ends give |F_made| < 0.03, i.e. the data are tighter than the record's
    convention.
- **UNDECIDED** if Step 0 fails, a required check fails, the interval is not closed within the extension limit, or a grid
  point inside the interval failed to converge.

F_made ≡ fraction of today's cold dark energy produced by exchange since z = 1090 = 1 − N(a_1090)/N(1), N = ρ_c a³
(negative = cold dark energy lost to DE).

## 5. Secondary verdict: a₀(z) against CFG689
√X(z) ≡ a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0) at ξ̂ and at both 95 % ends (footing-independent ratio; absolute a₀(2.33) printed for
both footings). Graded at z = 2.33 against CFG689's flat + θ* 68 % band for the matching SN set (DES-SN5YR: TD5F
[0.68, 1.04]; Pantheon+: TF [0.68, 1.05]; Union3: TU3F [0.69, 1.07]); the curvature-free bands (D5 [0.34, 1.21], primary
[0.32, 1.21], U3 [0.42, 1.26]) and CFG689's median 0.909 are reported.
- **CONSISTENT** if √X(2.33) at ξ̂ lies inside the band; **TENSION** otherwise (ρ_DE(2.33) ≤ 0 is TENSION).
- Reported: whether any ξ in the 95 % interval reaches CFG689's median 0.909 (the "a₀(2.33) ≈ 0.91–0.94 of local" shape).
- Caveat stated with the grade: CFG689's band was built assuming ρ_m ∝ (1+z)³ (CFG253 ±3 %, brackets B4m/B4p); with
  exchange that assumption is itself perturbed, so the comparison is a placement, not a joint fit.

## 6. Reports (not graded)
- F_made at ξ̂ and at the 95 % ends, against CFG253's 3 % convention and CFG131's flat-a₀ 1 % figure (the latter quoted,
  not used).
- w_eff(z): (i) intrinsic w_DE(z) = −1 + (Q/H)/(3ρ_DE); (ii) apparent w_app(z) of the "everything except ρ_c0 a⁻³ and
  baryons" fluid an uncoupled-fit observer would infer; a CPL (w0, wa) least-squares fit of ρ_app over 0 ≤ z ≤ 2.5;
  against DESI's w0wa chains (margestats, read only).
- S8 = σ₈ √(Ω_m/0.3) at ξ = 0, ξ̂ and the 95 % ends.

## 7. Step 0 (stop rule; any failure ⇒ UNDECIDED, no profile)
- S0-1 C7 ΛCDM χ² 1003.475 reproduced with the vanilla binary at C7's parameters (|Δ| ≤ 2, as X34).
- S0-2 CFG681's committed flat-ΛCDM BAO-only χ² 10.5515 (Ω_m 0.2970, scale profiled) and BAO + Pantheon+ 1400.143
  (Ω_m 0.3039) reproduced with this lane's BAO/SN code (|Δχ²| ≤ 0.02, |ΔΩ_m| ≤ 5e-4).
- S0-3 DESI chain numbers: the DES-SN5YR chain's mean w (−0.752) and wa (−0.86) recomputed from chain.*.txt (|Δw| ≤ 0.005,
  |Δwa| ≤ 0.03).

## 8. Machinery checks (required outcome PASS in the normal run)
- K1 background identity, from CLASS's background table at ξ = +0.01 (M-C) and +0.3 (M-D): d ln(ρ_c a³)/d ln a equals the
  model's (Q/H)/ρ_c with the frozen sign, and d(ρ_c + ρ_DE)/d ln a = −3ρ_c (max relative error ≤ 2e-3 over 0 ≤ z ≤ 1e4).
- K2 patched binary with ξ = 0 equals vanilla (max |ΔC_ℓ/C_ℓ| ≤ 1e-4 for TT, EE, φφ; σ₈ ≤ 1e-5).
- K3 perturbation check: δ_cdm(k = 0.05 h/Mpc) growth from z = 10 to 0 in the patched CLASS at ξ = +0.05 (M-C) agrees with an
  independent Python integration of δ_c' = −h'/2 − rℋδ_c, δ_b' = −h'/2 − θ_b, θ_b' = −ℋθ_b, h'' + ℋh' = −3ℋ²Σ Ω_i δ_i
  (dust + vacuum with δρ_DE = 0; radiation neglected), started from CLASS's own z = 10 values, to ≤ 3e-3 relative, while
  the dilution term's own effect is ≥ 1 %.
- K4 the BAO/SN distances read from CLASS's table agree with this lane's analytic background (same parameters) to 1e-4.

## 9. MUTATE plan (env X54_MUTATE=1 → *_MUTATE outputs; profile skipped)
The binary's runtime bug switch flips the sign of the exchange in the background (energy flows the wrong way for the
stated ξ) AND drops the perturbation dilution term (δQ = Qδ_c: the vacuum would have to carry a cold-frame perturbation).
**K1 and K3 must FAIL**; Step 0 and K2 must still PASS (the bug is inert at ξ = 0). Exit 1 if any check misses its
required outcome.

## 10. Compute
Single thread (OMP_NUM_THREADS=1), nice -n 15, < 1 GB RSS, each CLASS run seconds; run files in a temp build dir outside
the repository, deleted per run where large. compute_queue/ untouched. No downloads.
