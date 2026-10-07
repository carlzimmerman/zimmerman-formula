# T3 (P2 reframing, JKO): settling as a Wasserstein gradient flow whose minimiser is exactly rho_ph?

Lane: `deepseek_push/openai_math_cross_analysis_2026-10/t3_jko_settling/`.
Frozen criteria: `FROZEN_CRITERIA.md` (T3, C4, C5, T3-MUTATE). Working model:
`campaign_fresh_gravity/WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md`. κ = 1/2 is FITTED. No dark-matter
particle; the cold fluid's amount (5.36 M_b) is an input. Not "theory closed"; the data do not favour the framework.

Scripts: `t3_jko_settling.py` (nominal), `T3_MUTATE=1` (separate `*_MUTATE` outputs, rc 1).
Nominal: **8/8 checks PASS, rc 0.** MUTATE: **5/8 PASS with the declared flips (C0, C2, C7 FAIL), rc 1.**

---

## 1. The free energy and its unique minimiser

F[ρ] = ∫ ρ log(ρ/ρ_ph) dx (KL). Gibbs identity: ρ log(ρ/ρ_ph) = ρ_ph·h(ρ/ρ_ph) + (ρ − ρ_ph) with
h(x) = x log x − x + 1 ≥ 0, h(1) = 0, h″ = 1/x > 0 (sympy-verified). Hence F ≥ 0, F = 0 iff ρ = ρ_ph a.e.,
and by strict convexity the unique minimiser over the mass-1 simplex is exactly ρ_ph.
δF/δρ = log(ρ/ρ_ph) + 1, so δF/δρ = const ⇔ ρ = c·ρ_ph (sympy). **All stationary points of F (and of the
mass-constrained / quadratically penalised F_gen = KL + (β/2)(∫ρ − M)²) are rescalings of ρ_ph** — the
first variation of F_gen at ρ = c·ρ_ph is position-independent (sympy). The constrained minimiser is
ρ* = (M_supply/M_ph)·ρ_ph (Lagrange), with the penalty form approaching it as β → ∞ (numeric: c* → 1 on
the unit-mass toy).

**Physical caveat (supply limit).** For the MW-like point-mass host (M_b = 1e11 M_sun, r_in = 0.5 kpc,
r_out = 818 kpc), ρ_ph < 0 on the whole annulus (record kernel ν(y) = 1/(1−e^{−√y})), with
M_ph = M_b[(ν(y_in)−1) − (ν(y_out)−1)] = **−66.53 M_b (canonical), −73.19 M_b (alt)** vs the supply
+5.36 M_b: the unnormalised KL target does not match the supply in sign or magnitude — the supply limit binds.
Log ρ_ph is then not real; the declared positive proxy ρ̄_ph = |ρ_ph| is the only real target the KL admits,
and only **8.06% (canonical) / 7.32% (alt)** of its mass is realisable: ρ* = 0.0806·ρ̄_ph (canonical),
0.0732·ρ̄_ph (alt), ∫ρ* = M_supply to 2e-10 (C1, C2).

**Extra potential (frozen question: yes).** F = ∫ρ log ρ + ∫ρ V with **V(x) = −log ρ_ph(x)**: an external
field. The entire baryon-and-a0 content of the law sits in V, not in the fluid's self-interaction (C3).

## 2. JKO scheme and the PDE

JKO: ρ_{k+1} = argmin_ρ (1/(2τ)) W₂²(ρ, ρ_k) + F[ρ]. Euler–Lagrange in terms of the Kantorovich potential w_k
of the step: T_k = id − τ∇w_k with ∇w_k = ∇(δF/δρ)(ρ_{k+1}) = ∇log(ρ_{k+1}/ρ_ph), ρ_{k+1} = (T_k)#ρ_k
(first order in τ; the exact statement is the discrete Hamilton–Jacobi form w_k − (τ/2)|∇w_k|² = δF/δρ + const).

Overdamped convention ∂_tρ = div(ρ∇δF/δρ):

**∂_tρ = Δρ − div(ρ ∇log ρ_ph)**; radial 1D against the C/r² target:
∂_tρ = ρ″ + (4/r)ρ′ + (2/r²)ρ (sympy; the +2/r² term is the phantom cusp's "potential").
Mass-reweighting μ = v²ρ (v = r/r_out) eliminates the drift exactly: ∂_tμ = μ″ on [v_in, 1], Neumann.

**Mass conservation (C4, frozen): PASS.** Sympy: d/dt∫ρ dV = 4π[r²J_r]_{r_in}^{r_out} by FTC with
J_r = ∂_rρ − ρ∂_r log ρ_ph; the boundary term is 0 under no-flux on the annulus (and vanishes at infinity
for ρ, ρ_ph = O(1/r²)). Numerically the radial flow on [r_in, r_out] with no-flux boundaries conserves mass
to **1.7e-13 relative** over 2×10⁴ CN steps (frozen threshold 1e-10), and the end state is c·ρ_ph
(c fixed by the initial mass, 4.6e-4 relative) — the mass constraint is enforced BY the flow, so the
supply-limited rescaling is automatic.

## 3. The effective force

v = −∇(δF/δρ) = **−∇log(ρ/ρ_ph)** — zero at the target; near ρ ≈ ρ_ph the drift velocity is
−∇log ρ + ∇log ρ_ph. Linearising about ρ_ph (η-variable; φ = η/ρ_ph reduces the operator to ∂²/∂v²,
Neumann) gives the spectrum on the annulus: 0 (ρ_ph itself) and −(kπ/L)², **κ₁ = 9.8718** numerically
(theory (π/(1−r_in/r_out))² = 9.8817, 1e-3 agreement; zero mode 7.6e-11). With the declared diffusion
scale D = r_out²/t_dyn (t_dyn = 1/√(G ρ_host) = 28.3 Gyr, ρ_host = 6.36 M_b/((4π/3)r_out³)):

**Γ_KJ·t_dyn = κ₁ = 9.87, i.e. Γ_KJ ≈ 0.35 Gyr⁻¹** — **×353 vs CFG382's λ = 0.028**, ×9.9 vs CFG378's g = 1
and ×99 vs g = 0.1. The untuned KL flow settles 1–2 orders of magnitude faster than the record's bracket,
and ~2.5 orders faster than CFG382's rate: the free-energy flow alone does NOT reproduce the settling rate;
the small λ = 0.028 (CFG382) is exactly the suppression that does (CFG382 PARTIAL: groups pass, clusters
at R500 and UFDs do not). The spectrum is geometry-only, hence footing-independent (C6).

## 4. G9 verdict (frozen C5): is −∇log ρ_ph gravitational?

**No — gravity-only FAILS as declared on both footings.** (i) Analytic: in the annulus ρ_b = 0 (point
baryon), so any c∇Φ_b is divergence-free and curl-free (harmonic), while ∇·(∇log|ρ_ph|) = s′ + 2s/r ≠ 0
(−2/r² in the deep-MOND part; measured −4.0 ≤ r²∇·s ≤ −2.0, C3): no multiple of a baryonic field can match.
(ii) Numeric grid: min_c max_r |grad log ρ_ph − c grad Φ_b| over c ∈ [0.1, 10]: best c hits the window edge
(0.1) and the residual is **4.2e9 / 4.7e9 of the field scale** (threshold to reopen: < 10%); s(r)/g_b(r)
spans −2.4e-11 (r_in) to +3.8e-9 (r_out) — wrong exponent (1/r vs 1/r²) AND a sign flip at ~3 kpc.

**Conclusion (G9): the settling force is NOT gravity-only.** It requires either the one fluid-time-field
(lapse) coupling λ of CFG382 — whose channel is **CONDITIONAL** in the record (PARTIAL: groups pass, R500
clusters and UFDs fail) — or the fluid's own superfluid pressure (FL1, CFG288 road W). CFG378 implements an
operational overdamped JKO step (ρ_new = ρ_c^(1−λ)ρ_t^λ via one linearised Monge–Ampère step, Γ = g/t_dyn)
but **declares the mechanism without deriving it**; this lane shows the analytic object beneath that step
is exactly the KL/JKO flow above, and that its force term −∇log ρ_ph (equivalently the external field
V = −log ρ_ph) is what the coupling must supply.

## MUTATE (T3_MUTATE=1): drop the targeting term

F = ∫ρ log ρ (no −∫ρ log ρ_ph): minimiser over the mass-1 simplex is the **uniform** density (sympy:
log ρ + 1 = const; numeric: F_H(ρ_ph) − F_H(uniform) = +0.91 on the annulus). **C0 FAIL, C2 FAIL, C7 FAIL
(heat-flow stationary solutions are constants, not c·ρ_ph) — the minimiser is not ρ_ph, as declared.**
Mass conservation survives (C4 PASS, drift 1.4e-11); C1/C3/C5/C6 unchanged. rc 1.

## Bottoms line

The settling CAN be written as the JKO flow of KL(ρ‖ρ̄_ph) — well posed, mass conserving
(1.7e-13 numerically; sympy IBP), with the unique minimiser ρ̄_ph rescaled by the supply — but the
effective force −∇log ρ_ph is neither gravitational nor a fluid self-interaction in the record's sense:
G9 forces the CFG382 lapse coupling (CONDITIONAL) or FL1 superfluid pressure. The free flow's rate
(κ₁ = 9.87/t_dyn ≈ 0.35 Gyr⁻¹) exceeds the record's Γ bracket by 1–2 orders; the record's λ = 0.028
supplies the needed suppression. Follow-up if any: an analytic derivation of λ = 0.028 from the lapse
coupling — none found in this lane (no scan performed; declared, not derived).