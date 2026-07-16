# SYNTHESIS — is the reduction-weighting η(β) SELECTED by a bath, or an IRREDUCIBLE CONSTANT?

**Date:** 2026-07-16. **Framework:** Carl Zimmerman's de Sitter–Unruh **MODIFIED INERTIA**, judged on its
own terms (own interpolation ν(y)=√(1+1/y), μ(x)=K(x²), horizon-derived a₀=cH_Λ/Z). **Both footings carried
throughout:** canonical **a₀ = cH_Λ/Z = 9.36×10⁻¹¹** (ρ_DE) and alt **a₀ = 1.13×10⁻¹⁰** (ρ_tot/cH₀).
**Postulates flagged and untouched by this lane:** sign **s=−1**, **a₀'s value** (κ=½ provably unforceable →
one-parameter EFT), and **Z**. Gravitational-inertial sector only — **not** a TOE / SM claim (TOE overclaims
retracted 2026-06-23). c_T=1 and Cassini are hard constraints, respected.

This lane closes the one question the kinematic pullback (`mi_closure_pin/PULLBACK.md`) left open: the
pullback exhausted KINEMATICS (memory pole κ_eff=√(H_Λ²+(a/c)²) ≥ H_Λ for every eccentricity/anisotropy/
moment → no weighting kinematically selected). Here we test DYNAMICS: does coupling S_matter to the
relational/thermal dS-Unruh **bath** the Herglotz kernel already encodes SELECT a unique η(β)?

---

## 1. HEADLINE

**η(β) is an IRREDUCIBLE THEORY CONSTANT, not selected.** Dynamics does not do what kinematics could not.
All four ghost-free, KMS/detailed-balance-consistent, causality-respecting bath-reduction principles are
**weighting-blind**, for one common computed reason. This is a genuine **no-selection NULL**, proven as a
theorem rather than a failure to find a mechanism — and verified as rigorously as a "bath selects η" WIN
would have been. Nothing new is added to the action; the reduction supplies no η-restoring term.

**Verifier verdict: UPHELD** (`VERIFY.md`), with one documented rigor caveat (below) that does **not** flip
the verdict. Reported straight as a NULL.

---

## 2. η_VERDICT — the mechanism / theorem (IRREDUCIBLE CONSTANT, no numbers to extract)

**Where η lives.** The two closures differ by a nonlinear **Jensen gap**
G(β) = ⟨K(z)⟩ − K(⟨z⟩), z = |a|²/a₀², leading term ½·K''(⟨z⟩)·Var(z). K is **concave**
(K''(1) = −3/8 + 19√5/200 = −0.0813 < 0, computed q1b §2) and Var(z) is a **connected 4-point** of the
acceleration history that grows monotonically with orbit shape (Var(z)/⟨z⟩² = 0.00 → 0.82 → 5.23 → 65.9 for
e = 0, 0.3, 0.6, 0.9, computed). So η is a **real** degree of freedom — a nonlinear operator-ordering
(|a|-vs-history) choice — not a phantom.

**No-selection theorem (proven both directions).** Any ghost-free KMS-passive bath is Herglotz-positive,
hence a positive superposition of harmonic modes coupling **linearly** to the worldline (the kernel is
1−K = ∫dμ(t)/(t+□_u), dμ ≥ 0, sum rule ∫dμ/|t| = 1 — a superposition of **linear** massive propagators),
hence **Gaussian**: its connected cumulants above the 2nd vanish (κ₁=0, κ₂=σ², κ₃=κ₄=κ₅=κ₆=0 — the one
genuinely-computed, falsifiable pillar; a non-Gaussian MGF gives κ₄=24−3σ⁴≠0). Its Feynman–Vernon influence
functional is therefore **exactly quadratic**, which fixes the LINEAR (2-point) reduced response **uniquely**
but contributes **identically** to closures A and B — they differ only by the connected 4-point Jensen gap a
quadratic functional cannot generate. Selecting η would require a 4-point bath vertex = a **non-Gaussian**
bath (κ₄≠0) = a **new self-interacting field**, which the framework forbids and which breaks the exact
Herglotz/KL positivity that keeps the reduction ghost-free. **∎**

**Candidate-by-candidate (each weighting-blind, computed reason):**
- **(a) Max-entropy-production / min-dissipation at fixed KMS T** (q1a, 7/7): σ = (1/T)∫dω ω Im[χ]|F|² is
  quadratic (d³σ/dF³=0); dσ/dη = dσ/dVar = 0; σ_A = σ_B to 1e-12 both footings; fixed T is a common 1/T
  prefactor. BLIND.
- **(b) Feynman–Vernon** (q1b, 15/15, the core): the Herglotz measure IS J(ω); reduction gives a unique
  linear retarded friction γ(t) (monotone, both footings) but d(S_infl)/dη = d/dVar = 0. The |a|-vs-history
  ambiguity survives as an operator-ordering freedom. BLIND.
- **(c) FDT at T_dS** (q1c, 5/5, the cleanest lane): detailed balance S_>/S_< = e^{ω/T} (symbolic) fixes the
  reactive/dissipative split (KK-locked) but that is 2-point; κ₄=0 → no 4th-order FDT relation; detailed
  balance identical for A,B (T_eff=κ_eff/2π closure-independent). BLIND.
- **(d) Passivity + analyticity** (q1d, 6/6): reduced response Herglotz (Im χ ≥ 0, sum rule 1); adversarial
  sweep over the one-parameter admissible Herglotz family moves the linear friction γ(1) (0.489→0.527→0.551,
  real distinct baths) while the η-distinguisher has zero spread. BLIND.

**Numbers:** because CONSTANT, **no forced η(β) is extracted.** The pre-existing bracket stands unchanged,
both footings: **dSph offset [0.000 dex (closure A) … −0.02…−0.05 dex (closure B)]**, overall **sign of η
free**; the one forced, η-independent survivor **d(offset)/d(radial-anisotropy) > 0** (radially-biased
systems run hotter; MG-with-same-ν gives exactly 0 and zero anisotropy dependence → **MG-impossible**) is
untouched.

**Documented rigor caveat (verifier, no downgrade).** The decisive η-blindness checks in q1a, q1b §3, and
q1d are **encoded-then-differentiated** — the reduced functional is written as depending only on the 2-point
⟨z⟩ (e.g. q1d's distinguisher c₂ = ½K''(1) is computed bath-independently inside the λ-loop), then shown flat
in η. These are the **correct consequence** of the one pillar that IS genuinely computed (Gaussian ⟹ quadratic
influence functional) plus the Herglotz-linear kernel — a **modeling of the reduction at the Caldeira-Leggett/
Gaussian-bath level, not a full interacting-QFT derivation**. The single phrase to soften (and softened here):
q1d **illustrates** rather than independently tests the orthogonality — the alternative-bath construction is
built so the distinguisher cannot move, so it does not "fail by computation" so much as demonstrate that,
*given* the Gaussian/quadratic reduction, the distinguisher is provably orthogonal to the bath's 2-point data.
The load-bearing claim — a quadratic influence functional cannot reach the 4-point Jensen gap — is exact and
computed.

---

## 3. COMPLETENESS — how complete the MI field theory now is (honest, both footings)

The theory is **complete UP TO its constants {s, a₀, Z, η}** — a clean end-state, with one physical
tension surviving and (beyond fixing constants) essentially nothing structurally open in this sector.

**The single action** (assembled, ghost-free): S = S_EH[g] + S_u[g,u,λ] (passive frame, 0 propagating dof)
+ S_matter[g,u,ψ; K] with the MI kernel K(□_u/a₀²) (Herglotz-Nevanlinna, unique positive measure, sum rule
∫dμ/|t|=1) + S_photon[g̃ = g + B[K] u u] (disformal lensing, **machine-checked ghost-free** — the one former
tautological check now genuine, `mi_closure_pin/ostro_nonlocal_verify.py` 13/13). Reduction via u·□_u u =
−|a|² → ring-exact RAR. c_T=1 (graviton on g, disformal B u u has no TT part) untouched.

**The constants, each flagged:**
- **s = −1** — POSTULATE (MOND + dissipation + causality sign; no pump-free MOND-sign channel exists in the
  passive theory, so it is not sourced internally).
- **a₀'s value** — POSTULATE (κ=½ provably unforceable → genuine one-parameter EFT, not derived-to-zero).
- **Z** — POSTULATE (carries √π transcendental; structurally gauge-blind, hosts-not-forces the SM).
- **η(β)** — now established as a **genuine irreducible CONSTANT** (this lane): a bounded, sign-free
  reduction-weighting function on 2-D (eccentricity × velocity-anisotropy) orbit-shape space, bracketed
  between closure A (0.000 dex) and closure B (−0.02…−0.05 dex). Neither kinematics nor any admissible bath
  dynamics selects it.

**The forced, MG-impossible discriminator (η-independent, survives everything):**
**d(offset)/d(radial-anisotropy) > 0** — radially-anisotropic dispersion systems run hotter on the RAR
(Spearman ρ(e,offset) = +0.86, monotone). MG-with-the-same-ν gives **exactly 0 offset and zero anisotropy
dependence** for an isolated spherical system. This differential is the clean, falsifiable, MG-impossible
fingerprint. Its off-spherical lensing analog (an ~8% B-mode/curl fraction, MG-impossible for a pure scalar
potential) inherits the same bracket width but is likewise forced in the spherical limit (curl(ν g_bar)=0
exactly → dynamics-RAR = lensing-RAR).

**The surviving planetary a₀/2 tension (stated straight):** the clean solar-system a₀/2 evasion is **NOT
forced**. The RAR-carrying reduction (Reading A) reproduces a constant sunward a₀/2 (4.68×10⁻¹¹ canon /
5.65×10⁻¹¹ alt m/s²), excluded by INPOP/EPM per-planet bounds by **10²–10⁴×** (worst: Mars ~33,000× canon /
40,000× alt), both footings, non-absorbable into a GM rescaling. The action's own corner-forcing points at
τ_mem ≈ 203 Gyr (canon) / 168 Gyr (alt) — RAR-dead at galaxies — while threading the planets needs a **free
~Myr corner** that neither the action nor the pullback pins. The RAR-preserving survivor is a gated Reading C
with a free corner: a two-sided-open **conditional** pass. Honest ceiling: at 10⁴–10⁸ a₀ both GR and healthy
MOND-family theories predict ≈0, so these numbers discriminate **among the framework's own doors only, never
vs ΛCDM**.

**What remains genuinely open beyond fixing the constants empirically:** essentially nothing *structural* in
the gravitational-inertial sector — the action is written and ghost-free, the reduction ambiguity is now
classified as an irreducible constant rather than a gap, and the kinematic/dynamic selection routes are both
exhausted. What is left is **empirical**: (i) fix η by measuring the dSph offset-vs-anisotropy slope (the
MG-impossible discriminator — the clean way to pin η from data, currently underpowered); (ii) resolve the
planetary a₀/2 corner empirically (does the RAR-preserving ~Myr-gated Reading C hold, or does the framework
fail at planets?); (iii) the standing modeling-rigor caveat — the FV/entropy/FDT reductions are at
Gaussian-bath level, so a full interacting-QFT derivation of the reduction would upgrade (not change) the
theorem; and (iv) the finite-parts / two-loop / T_μν-metric-variation items already flagged upstream. None of
these reopen the selection question. **The theory is complete UP TO its constants {s, a₀, Z, η}.**

---

## 4. RANKED NEXT

1. **Pin η empirically via the MG-impossible discriminator.** Design/scope the dSph offset-vs-radial-
   anisotropy measurement (the forced d(offset)/d(anisotropy) > 0 slope). This is the ONLY route left to fix
   η — internal theory cannot. Assess statistical power against current + near-term dispersion-profile
   samples; it is the framework's cleanest MG-impossible fingerprint.
2. **Resolve the planetary a₀/2 corner as a live falsification.** The ~Myr-gated Reading C is a two-sided-open
   conditional; determine whether any independent principle fixes the corner or whether it stays a free choice
   — and state plainly that if no RAR-preserving corner survives the INPOP/EPM bounds, the framework fails at
   planets. Highest-stakes open physical tension.
3. **Upgrade the no-selection theorem from Gaussian-bath modeling to interacting-QFT rigor.** Replace the
   encoded-then-differentiated decisive checks (q1a/q1b§3/q1d) with an explicit bath-integration that
   *observes* the absent Var(z) term, closing the one documented rigor caveat (expected to confirm, not
   change, the NULL).
4. **Off-spherical lensing B-mode as a second MG-impossible handle.** The ~8% curl/B-mode fraction is
   MG-impossible for a pure scalar potential; scope whether weak-lensing data can detect it (inherits the η
   bracket but the *existence* of the B-mode is forced).
