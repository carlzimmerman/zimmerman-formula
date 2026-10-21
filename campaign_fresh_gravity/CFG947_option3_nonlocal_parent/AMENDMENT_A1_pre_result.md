# CFG947 AMENDMENT A1 (2026-10-20, PRE-RESULT)

Written after the criteria commit (9c683a634) and before any script was run or any number existed. It is committed alone.
It corrects one mis-stated falsification clause and pins down implementation details the criteria left open. No pass line,
candidate or class rule changes.

## A1.1 T-M: the falsification clause was the wrong quantity (correction)

The criteria (§4, T-M) state the right condition: a prescribed source is conservable only if D̈_s = −F_ms. They then name
the wrong falsifier ("falsified if F_ms = 0 for ε > 0").

Working the toy out on paper before coding shows why F_ms alone does not decide it. Write D_s = Σ_j s_j x_j, with the 𝒮
weight s_j carried by matter element j. Then

  D̈_s = Σ_j s_j ẍ_j + Σ_j (s̈_j x_j + 2 ṡ_j ẋ_j).

If each carrier falls freely in the total field, Σ_j s_j ẍ_j = Σ_j s_j g_m(x_j) + Σ_j s_j g_𝒮(x_j). The first sum is
−F_ms (Newton's third law between matter and 𝒮). The second sum is 𝒮's self-force, which is zero. So a nonzero F_ms is
consistent with conservation whenever the weights are constant: the matter's momentum change is carried by 𝒮's momentum
∫j_s = Ḋ_s. The whole obstruction is the relocation term

  R ≡ Σ_j (s̈_j x_j + 2 ṡ_j ẋ_j),

which is nonzero when the weights change, i.e. when the phantom grows and the draw moves, in a non-concentric domain.

**Corrected test.**
- Compute R symbolically for E8's draw on the declared toy (core plus a two-blob shell, dipole fraction ε) and for N3's
  switch-on.
- Evaluate R / (M_dom g_ref) for ε ∈ {0, 0.01, 0.1, 0.3}, with M_e/M_dom = ½ and a growth time equal to the dynamical time
  at the blob radius (both declared).
- Check numerically, with Plummer-softened blobs, that Σ_j s_j g_tot(x_j) = −F_ms to round-off when the weights are
  constant.

**Falsifiers.**
- T-M (as an obstruction to E8 verbatim) is falsified if R = 0 for ε > 0.
- d5 fails for a candidate whose declared relocation rule gives R ≠ 0 for ε > 0.

## A1.2 Implementation details fixed now (no result exists)

**Mu5 (q cap removed).** E7's edge makes q < 1 in the P-S configuration, so the cap never acts there. The tooth is therefore
applied to a starved catchment: NGC 3198's domain with shell cold mass × 0.5 (as CFG748's 0.5× mass-starved case), so that
q > 1.
- Uncapped: ρ_tot = (1 − q)ρ_c in the shell.
- Capped: e is scaled by 1/q, and the law deficit inside r_e is reported.

**N3's gate.**
- s(r) = clip((Δ_enc(r) − Δ_lo)/(Δ_ta − Δ_lo), 0, 1), with Δ_enc the mean enclosed particle overdensity. Inside r_ON it uses
  the P-S particle profile; outside it, M_ta plus the cosmic mean.
- Δ_lo = 2 is the primary value, graded for T-N3 and d3. Δ_lo = 1.1, a broad gate, is reported.
- The cold outside r_ON is at the cosmic mean (1 − f_b)ρ̄_m.

**d4 metrics.**
- **N2-E:** r_ON and the catchment particle mass under the largest-R rule (two equal point masses, each 2 × M_ta,thr, in
  ρ̄_m with Δ_ta(0) = 11.83), at d = d_c(1 ± 0.01).
- **N2-B:** the merger of the two minima of ψ for two Gaussian-smoothed (σ = L*) point masses (ψ ∝ −erf(r/(√2 σ))/r each).
  The merger separation d_c is computed numerically. The metric is the domain's retained baryons and edge r_e ∝ √M_b,ret at
  d_c(1 ± 0.01).
- **N1:** the same toys under rule β (labels latched before the approach).
- **N3:** the gate's outer radius and the gated charge at it.

**Cold profile in the shell (P-S).** ∝ r⁻² between r_e and r_ON, normalised to M_c,catch = (1 − f_b) M_ta[M⊙]. With f_b the
engine's FB = 0.02237/(0.02237 + 0.1200), M_ta[M⊙] = M_ta[M⊙/h]/0.674 (x_supply's own conversion).

**Units.**
- The engine-side formulas (M_ta, x_supply, fret_of) use the engine's own constants verbatim (6.674e-11, 1.989e30, 3.0857e22,
  0.674, 0.315 × 2.775e11).
- CFG847's systems use CFG938's constants (1.989e30, 3.0857e19).
- Everything else uses CFG4_common's constants.

**f1 bound.** Δa/g_host ≤ (g_ph(a)/g_host) × max(v²/c², g_host a/c²), where:
- g_ph(a) is the satellite's isolated phantom field at its Plummer radius;
- v = √(g_host R).

κ = ½ FITTED; footings never pooled; not theory closed.
