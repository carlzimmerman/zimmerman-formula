# CFG417 FROZEN CRITERIA: the Tolman reading of the rational 4 against DESI DR2
(owner 2026-10-07: "keep going"; committed before any script)

**Reading (not a derivation).** The 4 in Gρ_Λ = 4a₀²/c² is (1+3w)², the square of the vacuum's Tolman active-mass factor (ρ + 3p/c² = (1+3w)ρ). That gives:

  a₀ = c√(Gρ_DE)/|1+3w|, so κ_eff = 1/|1+3w₀| today.

- It reduces to κ = ½ for w = −1.
- The record's CFG264 R3 ("Tolman 2 × virial 2") ranked this family and folded it into R1's no-go as a derivation. This lane only tests its CONSEQUENCE.

**Data.**
- DESI DR2 chains (../_external_data/desi_dr2_chains: CMB, +Pantheon+, +Union3, +DESY5): the weighted w₀ posterior, giving the posterior of κ_eff.
- The measured κ = 0.530 ± 0.037 (the record's combined SPARC estimate, k05 937cca01b). The per-footing values 0.465 ± 0.076 and 0.55 ± 0.17 are reported.

**Verdict per chain.** z = (κ_eff,median − 0.530)/√(0.037² + σ_κeff²).
- COMPATIBLE: |z| < 2.
- EXCLUDED: |z| ≥ 3.
- TENSION: in between.

**Lane reading.**
- If every SN chain is EXCLUDED, the Tolman reading and DESI's evolving w₀ cannot both hold. Either the reading is false, or galaxies prefer w₀ ≈ −1.
- The w = −1 point (κ = 0.5) is reported as the reference.

**MUTATE.** Set w₀ := −1 in every chain. All chains must become COMPATIBLE. Separate outputs.

**Scope.** A consequence test of a chosen reading. κ = ½ stays fitted.
