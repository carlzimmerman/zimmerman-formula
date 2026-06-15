# FRONTIER 2 — the cross-sector coupling d²F/dYdQ via conformal anomaly / induced gravity: VERDICT (2026-06-15)

**Grade: UNFORCED — the cross-term is NOT generated, the separability F=J(Y)+K(Q) is NOT broken, and no
COMPUTED coefficient lands κ=½.** Both the conformal-anomaly angle and the Sakharov-induced-gravity angle fail,
each by a computed obstruction, not by assertion. The "one calc" identified by the Z run resolves AGAINST
closure. This converges with the 6 banked horizon routes + DSSYK; the quarantine holds. *Both ways: the genuine
structure (the anomaly really does make Λ dynamical) is credited; the manufactured-win paths are killed with
computed reasons; no high-priest dismissal.*

Companion script: `/tmp/anomaly_crossterm.py`, `/tmp/anomaly_step2.py`, `/tmp/anomaly_step3.py`,
`/tmp/anomaly_step4.py`, `/tmp/anomaly_step5_verify.py` (sympy, numbers reproduced inline).

---

## The target, precisely
AeST's free function is separable, F(Y,Q) = J(Y) + K(Q), with Y = q^{μν}∂φ∂φ the spatial/MOND slot (carries a₀
via J ~ (2/3)Y^{3/2}/a₀) and Q = A^μ∂φ the temporal slot (carries Λ via K ~ −2Λ+…). Separability sets
∂²F/∂Y∂Q = 0 identically — this is exactly what DECOUPLES a₀ from Λ. The cross-term ∂²F/∂Y∂Q is the ONLY object
inside AeST that could tie them. Deriving Z = √(32π/3) = 5.789 is deriving κ=½ (a₀ = κ·c√(Gρ_DE), Z = √(8π/3)/κ;
sympy: κ=½ ⇒ Z=5.78881). The frontier: does the conformal anomaly or induced gravity FORCE the cross-term with a
COMPUTED coefficient = ½?

## (i) Conformal / trace anomaly — KILLED, four computed obstructions
1. **WZ-closed basis is curvature-only.** The Wess-Zumino-consistent 4D trace anomaly is ⟨T⟩ = c·C² − a·E₄ + b·□R
   (Weyl², Gauss-Bonnet, □R). All three are curvature invariants — a functional of the background METRIC, not of
   the scalar profile. A field-monomial Y^{3/2}Q^m is NOT in the basis (it is not Weyl-covariant curvature).
2. **On de Sitter the anomaly is a constant.** Weyl²=0 (conformally flat), E₄=24H⁴ (const), □R=0 ⇒ ⟨T⟩ = −24a·H⁴,
   a pure number × H⁴. It has zero Y- or Q-dependence; it cannot BE a cross-derivative.
3. **The Riegert dilaton ≠ the AeST scalar.** The anomaly-induced (Riegert) action carries a dilaton σ that is the
   metric Weyl compensator (σ → σ+ω under g→e^{2ω}g). The AeST φ is k-essence shift-symmetric (φ→φ+const) and
   Weyl-inert in the deep-MOND sector. Identifying σ≡φ requires a posited mixing g_mix·σφ that gauges away the
   shift symmetry — an EXTRA input, not forced.
4. **Dimension + value.** Even allowing an induced Y^{3/2}Q^m: [Y^{3/2}Q^m]=mass^{6+2m}, so its coupling is
   DIMENSIONFUL (mass^{−(2+2m)}); the anomaly coefficient (a,c) is DIMENSIONLESS — it cannot be that prefactor, so
   the scale (H or a₀) re-enters as a separate input. And the anomaly's own dimensionless number is the central
   charge ratio a/c = **1/3** for a free scalar — the 1/3 family, never 1/2.

## (ii) Sakharov induced gravity — KILLED, two computed obstructions
- **Obstruction D (decisive, action-level proved).** The deep-MOND sector is scale/conformally invariant (SO(4,1),
  Singh 2026). sympy: ∫dⁿx |∇φ|^p is scale-invariant ⇔ p=n; n=3 ⇒ p=3 ⇒ |∇φ|³ = Y^{3/2}, the MARGINAL operator.
  a₀ is the dimensionful SO(4,1)-breaking spurion; a scale-invariant loop integral CANNOT deposit a dimensionful a₀
  multiplying a scale-free operator. a₀ is an input, not a loop output.
- **Obstruction E (wrong end of the RG).** Induced Λ ~ M⁴ (quartic), 1/G ~ M² (quadratic), but the a₀-coupling on
  the dim-6 Y^{3/2} operator ~ M^{−2} (IRRELEVANT, UV-suppressed). So a₀/√Λ is cutoff(M)-dependent — no fixed pure
  number. The framework ties a₀~√Λ at the IR scale H (ρ_DE); Sakharov deposits coefficients at the UV cutoff — the
  opposite end. No IR a₀↔Λ lock emerges.

## Both ways — what IS real (credited at full weight)
The 4D trace anomaly GENUINELY makes the cosmological vacuum energy dynamical (Antoniadis–Mazur–Mottola,
arXiv:0803.4000, 1006.3567): Λ becomes a horizon-boundary-condition condensate. So the anomaly really does touch
the Q/Λ sector — that is structure, not nothing. BUT (a) it acts on the metric conformal mode (Riegert dilaton),
not the Y^{3/2} term; (b) its IR behavior is a running Λ with a stable fixed point at Λ→0 (the condensate
dissolves) — it drives Λ toward zero, the opposite of depositing a fixed a₀~√Λ; (c) the induced action is
σΔ₄σ + σE₄ (dilaton×curvature), with NO Y–Q field cross-monomial. It modifies Λ's dynamics; it supplies no
a₀↔Λ lock, no cross-term, no κ=½.

## The d=3-lead bridge test — they do NOT meet (orthogonal)
The new lead (Z_d = 8√(π/(d(d−1))), Z₃=5.789 exactly) is a SPATIAL-dimension dof count. The conformal anomaly
VANISHES in odd SPACETIME dimensions including d=3 (no local curvature invariant of the right Weyl weight;
literature-confirmed), and on a d=4 spacetime it knows only the metric, not the spatial-d equipartition count the
Z_d formula uses. The "3" in Z_d is spatial marginality (p=n=3 ⇒ Y^{3/2}), the SAME 3 — but that is a spatial dof
statement, not an even-spacetime curvature anomaly. The two leads are orthogonal; the anomaly is the wrong tool to
make the d=3 spatial count force κ=½.

## Both-ways stress test for an independent ½
A scan of d-dependent geometric ratios: a/c(scalar)=1/3, Verlinde (d−3)/((d−2)(d−1))=1/6, 1/(d−1)=1/3 — none is ½.
The ONE hit is 1/(d−2)=½ at d=4 — but that is the scalar's canonical dimension (d−2)/2, i.e. the SAME
free-fall/equipartition ½ already flagged as the free posit; it RESTATES κ=½, it does not DERIVE it from the
anomaly's a or c. To reach ½ you must abandon the anomaly coefficient (1/3) and import the canonical dimension =
the posit itself. No independent, anomaly-COMPUTED ½ exists.

## Bottom line
Neither the conformal anomaly nor Sakharov induced gravity COMPUTES a forced cross-coupling d²F/dYdQ; both leave
the free O(1) intact (like the 6 banked horizon routes + DSSYK→∞). The separability F=J(Y)+K(Q) is not broken by
a deeper principle here, and there is no cost reduction: the anomaly route adds no a₀↔Λ lock, so it does not
collapse +2 to +1 either. Quarantine: a₀/Z never asserted derived. The empirical program stays Z-free (a₀(z),
wide-binary DR4 cancel Z), so the open coefficient touches no falsifiable test.

*Sources: Skordis–Złošnik 2021 (arXiv:2007.00082); Singh 2026 (arXiv:2601.04290); Deser–Schwimmer / Bonora–
Pasti–Bregola (4D WZ anomaly basis); Antoniadis–Mazur–Mottola (arXiv:0803.4000, 1006.3567, 0907.0823);
odd-d anomaly vanishing (standard). Banked: OPEN_PROBLEM_yphi32_KQ.md, DERIVE_Z_FRESH_RUN_VERDICT_2026-06-15.md,
ROUTE_AEST_JOINT_COEFFICIENT_2026-06-15.md, FORCING_THE_COEFFICIENT.md.*
