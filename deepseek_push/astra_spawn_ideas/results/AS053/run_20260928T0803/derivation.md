# AS053 — Dimensionless slope freedom in a single-scale action

**Run:** `run_20260928T0803` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent · **Status:** complete, unreviewed
**Task file:** `deepseek_push/astra_spawn_ideas/AS053_dimensionless_slope_freedom_in_a_single_scale_action.md`
**Task SHA-256:** `ab897a9af62fd2eb5ffa61e89b46c03970dec70dd8d811bb6d89b19b5987fb4b` (verified before execution)

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Named claim under test** (seed, Mathematics section):
> p_λ(Y) = λ·Y/(1+λ·Y), λ > 0, has p(0)=0, p(∞)=1 but p'(0) = λ.

**Framework consequence investigated:** the PD08 "particle-free derivation" of κ = 1/2 (PD08 STEP 3, "fraction identity": *a one-scale action forces the per-channel engagement's linear slope to be exactly 1, p'(0)=1, because no second scale exists to rescale it*), chained through the two-channel OR composition (PD01 A1–B4) to the deep spherical matching. If a *dimensionless* slope coupling λ survives the single-scale action class, the chain closes to κ = 1/(2λ) and κ = 1/2 is a normalization (λ = 1), not a derivation.

**Symbol dictionary** (SI unless noted):
| symbol | meaning | status |
|---|---|---|
| Y = g/s | dimensionless drive, g total radial acceleration, s the vacuum rate | — |
| s | c·sqrt(G·ρ_Λ): the vacuum's own rate; the action's one dimensional scale | framework input (PD08) |
| ρ_Λ | vacuum mass density | framework input (measured) |
| p_λ(Y) | per-channel engagement of the metric's static response | candidate family |
| μ_λ(Y) = 1 − (1−p_λ)² | response after OR composition over two equal channels | derived from p_λ |
| K_λ(Y) | static energy primitive, K_λ' = μ_λ | derived from μ_λ |
| λ | dimensionless coupling (slope of p at 0) | **free parameter of the family** |
| r_M = sqrt(G·M_b/a0) | MOND radius | framework input |
| v_flat⁴ = G·M_b·a0 | deep flat-speed law | framework input |
| κ = a0/s = 1/(2λ) | coefficient of the vacuum relation | output of the chain |
| G_N = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 | numerical conventions (only G_N used; G_bare, G_cosmo separate, unused) | inputs |

**Boundary conditions and assumptions (framework inputs, PD08/PD01):**
1. One field (the metric's own potential), no particle: S_kin = (1/8πG)∫s²K(|∇Φ|/s)d³x − ∫ρ_bΦ; s fixed independently of a0. *(PD08, input)*
2. Static response presents exactly two independent Poisson channels (00 sector → Ψ; spatial-trace sector → Φ−Ψ); response is the OR over the two equal per-channel engagements: μ = 1 − (1−p)². *(PD01 B1–B3, input)*
3. p(0) = 0 (frozen vacuum), p(∞) = 1 (saturation), normalization μ(∞) = 1 (L230). *(PD08 STEP 1/2, input)*
4. Deep spherical matching of div(μ grad Φ) = 4πGρ with μ ≈ μ'(0)·g/s. *(PD08 STEP 5, input)*
5. **STATED PREMISE OF PD08 (the object attacked):** p'(0) = 1 — "engagement fraction = drive fraction, both measured in the one scale s; no second scale exists to rescale it" (STEP 3, L230; backed by the k01 zero-mode theorem, which rules out *dimensional* second scales).
6. κ = 1/2 adopted as input (framework contract); the task does not supply an independent derivation — this run tests whether the one-scale action *supplies* one.

**Conclusions to be established (not inputs):** whether λ is excluded by conditions 1–4 (it is not); whether κ = 1/(2λ) with λ free (it is); which PD08 premise would have to exclude the family (p'(0)=1, condition 5 — it is a normalization, not a theorem).

---

## 2. Varying the static energy primitive: λ is a dimensionless coupling, not a scale

The seed's Step 2 — "vary the corresponding static energy primitive and show whether λ adds a dimensional scale or a dimensionless coupling":

The static energy primitive (kinetic function) of μ_λ is the antiderivative normalized at K(0)=0:

    μ_λ(Y) = 1 − (1+λY)⁻²
    K_λ(Y) = ∫₀^Y μ_λ = λY²/(1+λY),   K_λ'(Y) = μ_λ(Y)   (exact; sympy + Lean)

Every term of p_λ, μ_λ, K_λ is a **pure dimensionless function of Y = g/s**: λ multiplies the dimensionless Y only. No power of a length, time or mass scale appears beyond the argument's own unit s. Therefore:

- **λ is a dimensionless coupling.** It is *not* a second dimensional scale, so the k01 zero-mode theorem (K1–K6: the static equations are invariant under J→J+C; with Λ explicit and free no equation of the action relates a0 to Λ; no *dimensional* coefficient survives) does not reach it. PD08 STEP 3's justification — "no second scale to rescale it" — is silent on dimensionless parameters, and AS053's family is precisely the gap: a one-parameter family inside the same one-scale action class, with the same boundaries and normalization, carrying a free dimensionless slope.
- **The premise in PD08 that would have to exclude this family is STEP 3's fraction identity p'(0)=1** (L230). It is an independent *normalization* of the engagement in the channel's own unit; nothing in the action forces λ = 1. This is exactly the seed's principle: "the adopted one-half normalization is not a derived result unless an independent argument removes its freedom."
- The family is not exotic: μ_λ(Y) = μ₂(λY), i.e. the corpus's own committed MU2-analytic family μ_n(Y) = 1−(1+Y)⁻ⁿ at n = 2 with the argument rescaled Y → λY. Equivalently μ_λ(Y) = μ₂(g/a0) with a0 = s/(2λ): **the response family is the operative MU2 branch; the freedom sits entirely in the vacuum relation κ = a0/s.** (Recorded as a comparison/identification — no branch translation of the operative MONO target is performed.)

---

## 3. Intermediate algebra: signs, scales, units, limiting regimes

**OR composition (two equal channels):**
    1 − p_λ = 1/(1+λY)  ⇒  μ_λ(Y) = 1 − (1+λY)⁻².
    μ_λ(0) = 0,  μ_λ(∞) = 1,  μ_λ'(Y) = 2λ(1+λY)⁻³,  μ_λ'(0) = 2λ.
    Completion-independence: for n channels, slope of 1−(1−p_λ)ⁿ at 0 = n·λ (n = 1,2,3 checked symbolically).

**Static energy primitive:**
    K_λ(Y) = λY²/(1+λY),  K_λ(0) = 0,  K_λ' = μ_λ.  (dimensionless in Y)

**Deep spherical matching** (div(μ grad Φ) = 4πGρ; point source; μ ≈ μ'(0) g/s = 2λg/s):
    (1/r²) d/dr [r² (2λ g/s) g] = 4πGρ  ⇒  r²(2λ g/s)g = G·M
    ⇒  g² = s·G·M/(2λ r²) = (s/(2λ))·g_N,   g_N = G·M/r².
    Matching to the a0-line g² = a0·g_N:  a0 = s/(2λ),  κ = a0/s = 1/(2λ).   **(exact, Lean-certified)**
    Diagnostic couplings: λ = 1/2 → κ = 1; λ = 1 → κ = 1/2; λ = 2 → κ = 1/4.

**Limiting regimes and leading neglected terms (domain statements):**
- *Deep (Y ≪ 1, r ≫ r_M):* μ_λ = 2λY − 3λ²Y² + O(λ³Y³); leading law g² = (s/2λ)g_N [1 + O(λY)]. Numerically at r = 10¹⁹ m, λ = 1: extracted κ_eff = g²/(s g_N) = 0.50004465 vs 1/(2λ) = 0.5 — deviation 4.5e-5 ≈ O(λY) with Y = g/s = 8.4e-5, **not a fit**.
- *Newtonian (Y ≫ 1, r ≪ r_M):* μ_λ = 1 − (λY)⁻² + O((λY)⁻³); leading neglected term (λY)⁻² with domain λY ≫ 1. Numerically g/g_N − 1 = 1.9903856e-12 (r=10¹²) and 1.9898297e-8 (r=10¹³), matching (λY)⁻² = 1.9903912e-12 / 1.9903912e-8 with relative agreement 2.8e-6 and 2.8e-4.

**Units:** all identities dimensionless; dimensional examples carry SI (Section 6, both footings).

---

## 4. Independent checks (actual residuals, 60-digit mpmath; Lean)

| check | what it verifies | actual value | gate |
|---|---|---|---|
| E1 | μ = 1−(1+λY)⁻² and K' = μ on Y ∈ {1e-7,1e-3,1,1e3,1e7}, λ ∈ {1/2,1,2} (Richardson central differences, O(h⁴)) | substitution ≤ 7.7788e-55; differentiation ≤ 2.33e-45 (relative) | < 1e-40 PASS |
| E2 | numeric slope extraction p'(0), μ'(0) (Richardson, h=1e-12) | p'(0) rel res ≤ 1.6e-50; μ'(0) rel res ≤ 1.2e-47 | < 1e-38 PASS |
| E3 | exact algebraic profile r²gμ_λ(g/s) = G_N·M_sun solved at 60 digits, r ∈ [10¹²,10¹⁹] m × 3 λ | max relative equation residual 1.314e-57 | < 1e-45 PASS |
| E4 | deep extraction κ_eff → 1/(2λ) at r=10¹⁹ m | 1.0000631, 0.5000447, 0.2500316 vs 1, 1/2, 1/4 (finite-Y deviation ~ λY, expected) | < 2e-4 PASS |
| E5 | Newtonian recovery with derived leading term | leading-term rel agreement 2.8e-6 / 2.8e-4 | < 1e-3 PASS |
| Lean | 10 theorems: boundaries, slopes, primitive, saturation limits, deep matching (κ = 1/(2λ)) | compiles exit 0, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound} | hard bar PASS |

Sympy exact checks (A1–A4, B1–B4, C1–C2, D1–D3): p(0)=0, p(∞)=1, p'(0)=λ, μ(0)=0, μ(∞)=1, μ'(0)=2λ, K'=μ, K(0)=0, n-channel slopes n·λ, κ = 1/(2λ), N1–N2 controls — 34/34 PASS, exit 0, wall 0.27 s.

---

## 5. Specified negative control and the strongest surviving statement

**Negative control (capable of failing):** *Strawman assertion — "one dimensional scale prohibits λ": a single-scale action forces p'(0)=1; the family is illegitimate.*
Test: structural audit of the explicit family at λ ∈ {1/2, 1, 2}: (i) uses only s (Y = g/s), no second dimensional parameter; (ii) p(0)=0, p(∞)=1; (iii) μ(0)=0, μ(∞)=1 (L230 normalization); (iv) μ monotone; (v) family = corpus MU2 family under argument rescaling. **All five hold for λ ≠ 1 with the same algebra as λ = 1. The control fired: the strawman assertion is REFUTED** — the one-scale condition does not exclude the family. (The control was genuinely capable of failing: had any boundary or normalization broken at λ ≠ 1, the strawman would have survived.) The asserted *consequence* — PD08 derives κ = 1/2 — is refuted: the chain closes only with the independent dimensionless premise λ = 1.

**Strongest surviving statement (domain: λ > 0, Y ≥ 0, single-scale static OR class of PD08):**
> In the single-scale action class {one scale s = c·sqrt(G ρ_Λ), two equal OR-composed static channels, boundaries p(0)=0, p(∞)=1, normalization μ(∞)=1}, the family p_λ(Y) = λY/(1+λY) with λ ∈ (0,∞) satisfies every structural condition; μ_λ'(0) = 2λ (Lean-certified); the deep spherical matching yields κ = a0/s = 1/(2λ) (Lean-certified). Hence κ = 1/2 is the adopted normalization λ = 1; the dimensionless slope freedom survives the single-scale action, and only an independent argument fixing λ = 1 (the L230 fraction identity as a *principle*, currently a premise) can remove it.

**First additional implication needed to transfer to the full theory:** a mechanism or theorem that fixes the dimensionless coupling λ = 1 from within the action (equivalently: derives the L230 fraction identity), or — failing that — the explicit admission that κ = 1/2 is an independent vacuum-normalization input. k01's K1–K2 zero-mode result shows no equation of the *current* action class relates the scales; this run shows dimensionless couplings are equally untouched. No branch repair is available from Q, RAR, MU2, EXP or MONO: the result *is* about the coefficient premise feeding those branches.

---

## 6. Both registered footings (dimensional examples carried separately)

Constants: G_N = 6.67430e-11 m³kg⁻¹s⁻², c = 299792458 m/s (exact), M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m. rho_Λ(canonical) = 4a0_can²/(G_N c²) = **5.844412454e-27 kg/m³**.

| footing | a0 | fixed inputs | outcome |
|---|---|---|---|
| canonical | 9.3619e-11 m/s² | ρ_Λ = 5.8444e-27 kg/m³, κ = 1/2 | λ = s/(2a0) = **1** (exactly, by adoption) |
| alternative (fixed ρ_Λ) | 1.1279e-10 m/s² | ρ_Λ = 5.8444e-27 kg/m³ (same s = 1.87238e-10 m/s) | κ = a0/s = **0.602388404063**, λ = 1/(2κ) = **0.830029257913** |
| alternative (fixed κ = 1/2) | 1.1279e-10 m/s² | κ = 1/2 (λ = 1) | ρ_Λ = 4a0²/(Gc²) = **8.483089619560e-27 kg/m³**; ρ_Λ,alt/ρ_Λ = (a0_alt/a0_can)² = **1.4514871574** |

The two footings cannot share both fixed vacuum density and fixed kappa — consistent with the framework contract, here with the identification λ = s/(2a0). Because the theorem is dimensionless (λ a pure number), it applies verbatim to both footings; the footing choice is the *adopted coupling value*, not a new freedom.

---

## 7. Branch discipline

No branch law was imported: Q, RAR, MU2, EXP-AQUAL and operative MONO are untouched and remain distinct; no branch translation was performed. The identification μ_λ(Y) = μ₂(g/a0) (Section 2) records that the family at its matched a0 *is* the MU2 analytic response — it is a comparison used to show the counterexample is the corpus's own family with a free vacuum relation, not evidence of a different gravity law. The operatity of filtered ν_mono with criterion B is unaffected: AS053 attacks the coefficient premise (κ), which precedes the spline/filter/gate construction.

---

## 8. What this does and does not establish

**Established:** (exact algebra, Lean-certified) the family's boundaries, slopes, primitive, saturation, and the matched κ = 1/(2λ) for every λ>0; (60-digit numerics) all identity/profile residuals ≤ 2.4e-45 with the two limiting regimes' leading neglected terms verified; (structure) the k01 zero-mode theorem does not constrain dimensionless couplings, so PD08's STEP 3 unit-slope premise is genuinely independent.

**Not established:** any mechanism fixing λ = 1; a derivation of κ = 1/2 from the single-scale action; any change to the operative MONO branch, its filter or its gates; any empirical statement (the footnote "observational preference is not a mathematical proof" is respected: zero observational data used).

**Limitations:** (1) counterexample is within the *static spherical* sector where the corpus's response lives; the radiative/PPN sector is untouched. (2) The OR identification over exactly two channels remains the corpus's own premise (PD01 D1) — the counterexample inherits it. (3) The family is one completion class; the *freedom* it demonstrates is the slope of the linear jet, and a different action (e.g., with derivative couplings, AS-series kappa lanes) could in principle constrain it — none is present in the reviewed class. (4) Memory bound: RLIMIT_AS could not be raised on this macOS host (OS refused, "current limit exceeds maximum"); actual peak RSS ~35 MB, single-threaded, wall 0.27 s ≪ 120 s, CPU limit enforced at 120 s. (5) Numerical agreement is finite evidence; all load-bearing statements are exact algebra + Lean.

## 9. Next unresolved implication and follow-up

**Next unresolved implication:** the fraction identity p'(0) = 1 is not derivable in the reviewed single-scale action class — neither as a dimensional consequence (k01) nor as a dimensionless one (this run). The first missing bridge to the full theory: **an independent principle that fixes λ = 1** (e.g., a second-order/stationarity condition on the static action whose Euler–Lagrange problem removes the linear jet's coupling), or the explicit demotion of κ = 1/2 to the status "vacuum-normalization input" in the coefficient gate.

**Suggested follow-up (child spec ready):** derive the first variation of the deep law with respect to the *completion* class — i.e., test whether a *second-order* slope condition (e.g., μ''(0) fixed by the primitive's convexity or by the k01 heat/filter structure) can remove the linear-jet freedom; the discriminating observable is the extracted κ_eff at finite Y (registered E4 procedure), which currently equals 1/(2λ) to the accuracy of the response itself.