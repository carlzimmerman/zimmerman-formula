# QC1_qcd_volume_ratio: FROZEN CRITERIA

Written before the script. **Disclosed first:** before freezing I did rough hand arithmetic on the proposal, and read CFG886.
Seen so far: (λ_π0/0.8409 fm)³ ≈ 5.255, not the proposal's 5.274; Γ/H of order 1e19 for a gapped scalar; R = 5.272 ± 0.218 on
the record. These tests are therefore a check of a claim with partly known answers, not a blind test.

**The claim under test (pasted proposal, 10-31).** Cold dark energy is a vacuum condensate displaced per baryon at the QCD
transition, T ≈ 155 MeV. Then R_nat = Ω_c/Ω_b = (ħ/m_π0 c / r_p)³ = 5.274, "to 0.07 %, zero free parameters". It claims zero
isocurvature, Γ/H = 0, closing X1, and closes G11 (core form "unique"), G12 (S fixed, R_net = 1), G14 (κ = ½ "exact geometry").

**Inputs.** Record: R = 5.272 ± 0.218, flat a0, DESI DR2 BAO + BBN; 6.12 ± 0.32 with SH0ES; 2.9–8.1 without flat a0 (CFG886).
Ω_m 0.2976016, h 0.6856427, ω_b 0.0223081. Particle values (m_π0, CODATA radii, f0(500) width, bag constant, gluon condensate) are
quoted from memory, marked PROVISIONAL, and not fetched. A verdict below that turns on one must hold across the stated range.

## Tests and rules
- **T1 arithmetic.** Recompute each number in the proposal. A number is WRONG if off by > 0.1 %. Dimensions are checked too.
- **T2 precision.** Compare the ratio, propagating r_p's error, with R's error. "0.07 %" stands only if R is known that well.
- **T3 look-elsewhere.** Pool: lengths ħ/m for 12 hadronic scales over 6 radii, plus ratios of those masses, exponents 1–4, 18
  simple prefactors (including 10/9, 4/3, π, 4π/3), offset 0 or ±1. Null: 200 log-uniform targets in 3–8, same relative windows.
  Windows: ±4.1 % (R's 1σ) and ±0.28 %. DISTINGUISHED needs target 5.272 in the top 5 % of null targets in both windows, on the
  full pool and on the bare subset (prefactor 1, offset 0). Otherwise CHANCE-LEVEL.
- **T4 energy.** A volume ratio is an energy ratio only if the density is equal in both volumes. R computed from: the proposal's own
  virial (E_bag = m_p/4), MIT B^¼ = 145 MeV, the trace-anomaly vacuum at ⟨αG²/π⟩ 0.005–0.02 GeV⁴. Also shell only (cloud minus core).
  PASS if the proposal's own virial gives R within 1σ of the record.
- **T5 baryon number.** A bag volume is even in B; Ω_c ∝ net baryons is odd. Thermal nucleons plus antinucleons at 155 MeV over net.
  PASS only if that ratio is < 10.
- **T6 lifetime.** Γ/H at 155 MeV for a gapped scalar shift, using f0(500) width 400–700 MeV and g* 17–62, plus the thermal factor
  e^(−m/T). PASS only if Γ/H < 1 at zero temperature, since a gap stops thermal absorption, not decay.
- **T7 delocalisation.** Fraction of space the 1.46 fm spheres fill at 155 MeV. PASS only if ≥ 1, which is what "delocalised" needs.
- **T8 Λ scales.** Compare the proposal's QCD combinations with ρ_Λ^¼ and a0. Match means within a factor 2.
- **T9 κ.** Does the identity fix κ, or restate it? Fixes only if some equation selects 4π for the a0 law, independent of κ = ½.
- **T10 core, response.** "Unique" fails on any other profile meeting the same stated conditions. G12 needs a calculation.

**Word rule.** X1 CLOSED needs T5, T6, T7 all pass. MECHANISM FAILS if any of them fails. Zero isocurvature from birth after inflation is
credited separately, as it holds for any post-inflation production. No grader is run, as no new profile or number enters one.
κ = ½ stays FITTED unless T9 says otherwise. Not "theory closed". No dark matter particle added.
