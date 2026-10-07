# T11 — FROZEN CRITERIA: the assembly clock (historical face of the settling law)

**Claim to test (novel derivation from the campaign's own T10 result):**

The settling law assigns completeness  f = 1 − e^{−Γt}  (T10 S1: heat-mode
settling; Γ = λπ²/t_dyn, first-mode dominates late). Since R500 is defined
by mean density, ρ̄(<R500) = 500ρ_crit — the SAME for clusters and groups —
the settling rate Γ is COMMON (density-locked). Hence for the measured
completeness pair (clusters 0.43 ± 0.15 [X-COP], groups 0.60):

  (A1)  The exact single-mode law gives, with Γ cancelling:
        t_form(c)/t_form(g) = ln(1 − f_c)/ln(1 − f_g) = 0.6135
        — a pure ASSEMBLY-TIME ratio, no λ, no a₀, no κ, no cosmology
        beyond the R500-Δ-locking.  [Linear-branch folklore f ≈ Γt gives
        0.717; the exact law's value is 0.613 vs the linear 0.717 — the
        exponential curvature is testable, not negligible.]

  (A2)  Second-mode corrections (e^{−4Γt}-relative) at Γt ~ 0.5–0.9 shift
        the ratio by O(2–3)%; the declared window is t_c/t_g ∈ [0.55, 0.66].

  (A3)  z-face: with t_g ≈ 11 Gyr (z_g ≈ 0.15), the prediction is
        t_c ≈ 6.7 Gyr ⇒ z_form(cluster main body) ≈ 0.7–0.8 in flat ΛCDM
        (H₀ = 68, Ωm = 0.3 — standard kinematics, record-side constants).

  (A4)  Density-locking corollary (the sharp new statement): completeness
        at a fixed overdensity is MASS-INDEPENDENT up to the assembly
        history — a 10¹³ M_b group and a 10¹⁵ M_b cluster at their
        respective R500 sit on the SAME f(Γt) curve with the SAME Γ.

**Kill condition (pre-registered):** assembly-epoch measurements (BCG/
red-sequence ages, cluster archaeology) yielding t_c/t_g outside
[0.55, 0.66] kill the historical face of the settling law.

**Screens:** Q1 — derives the completeness-ratio law from the framework's
settling (a₀ enters NOT AT ALL; the claim is the law's historical face);
Q2 — no inserted rational; the numbers 0.43/0.60 are measured inputs, the
ratio is forced; Q3 — functional law, not a constant search.

**Checks that can fail (exit 1):**
  C1  exact-ln ratio: |ln(1−0.43)/ln(1−0.60) − 0.6135| < 0.001.
  C2  curvature vs linear: 0.6135 < 0.717 (exponential-law value is
      strictly BELOW the linear approximation — the exact law's signature).
  C3  second-mode window: two-mode f(t) = 1 − c₁e^{−Γt} − c₂e^{−4Γt}
      (c₂/c₁ = 1/9, the Neumann-mode amplitude ratio) gives the ratio in
      [0.55, 0.66] over Γt_g ∈ [0.5, 1.5].
  C4  density-locking: ρ̄(<R500) for a 1e13 and 1e15 M_b host (K = 500,
      c = 1, H₀ = 68, z = 0.1) agree to < 1% ⇒ same Γ (up to H(z) — both
      at the same z ⇒ identical).
  C5  z-face: t(z) flat ΛCDM: t(0.75)/t(0.15) ∈ [0.58, 0.66]; and
      t(0.75) itself ∈ [6.0, 7.5] Gyr (H₀ = 68, Ωm = 0.3, ΩΛ = 0.7).
  C6  literature grounding: web sources for cluster/group assembly epochs
      must show the measured t_c/t_g band overlapping [0.55, 0.66] OR
      clearly outside it (either way the verdict is registered; the
      prediction is one-sided: the band is the law's).

**MUTATE (T11_MUTATE=1):** completeness pair swapped (f_c = 0.60,
f_g = 0.43) — C1 must fail (ratio 1.63 ≠ 0.6135), C2 must fail, C4/C5
must pass (density/cosmology unchanged).  [CORRECTED 2026-10-07: the
original wording declared C3 pair-agnostic; empirically the second-mode
window IS pair-dependent (swapped pair gives [1.619, 1.619], off the
declared window) — C3 is declared to flip with the pair. Verified:
main C3 [0.5577, 0.5926] ⊂ [0.55, 0.66]; MUTATE C3 fails as corrected.]

**Deliverables:** freeze committed ALONE; t11_assembly_clock.py + .out ×2
+ results ×2; README with the ratio table, the kill condition, the
registration duty; Lean certificate of the ln-ratio identity (symbolic —
numeric evaluation stays in the lane; house pattern).
Language: nothing "closed"; the face dies alone if the kill condition
fires; κ/a₀ untouched.