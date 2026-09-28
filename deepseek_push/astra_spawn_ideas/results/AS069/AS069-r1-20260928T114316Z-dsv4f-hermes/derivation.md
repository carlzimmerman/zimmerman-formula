# AS069 — Dimensionless kernel parameter versus vacuum energy (derivation)

**Run:** `AS069-r1-20260928T114316Z-dsv4f-hermes`
**Worker:** deepseek-v4-flash-0731 (OpenRouter) / Hermes subagent on macOS
**Task seed sha256:** `4e301e32aa04fc392d34aa5d28ff8035d1d61774a54e0801f05ae57e20e50bc3` (verified on disk before execution)
**Sources pinned and verified against SOURCE_MANIFEST.json (all ✓):**
- `deepseek_push/PD01_polarization_count.py` — `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d`
- `deepseek_push/PD08_particle_free_derivation.py` — `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb`
- `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` — `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c`

**Branch discipline.** Conclusions are drawn only for the MU_λ response family
(λ the dimensionless kernel parameter; symbolic λ > 0, channel counts at the
integers n ≥ 1 — instances n = 1..6 — and λ = 1/2 used as an algebraic
diagnostic that is *not* a channel count) inside the corpus A1-class local
action of k01/AS067:  `L ⊃ −α J(Y;λ) − K(Q) + 2α J^μ ∂_μ φ`,  α = 2 − K_B,
Y = g/s,  s = c√(G ρ_L),  κ = a0/s **= 1/2 adopted** (framework input; never
claimed derived here). Q, RAR, EXP, MONO are never imported. The generic
J-only-through-J′ zero-mode theorem of AS067 (kernel-independent) is used as an
established lemma; all new statements are re-derived within MU_λ. The affected
operative gate is requirement 13 (cosmological acceleration-scale relation) of
the amended thirteen-item target; criterion B and the remaining gates are
untouched.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Named claim (the seed's mathematics line).**

> For J(Y; λ), the derivative fixes forces while C(λ) changes vacuum energy
> independently if allowed.

Formalized: let `F` be the force observable (rotation-acceleration law
`μ_λ(g/s)·g = B` with `μ_λ = ∂J/∂Y`) and `V` the vacuum observable
(`ρ_vac = α·(J(0;λ)+C(λ))/(16πG c²)`, J(0;λ)=0 by convention, C the free
additive constant in units of a0²). Then the Jacobian of the observables with
respect to the pair (λ, C) is block lower-triangular,

```
∂(F, V)/∂(λ, C) = [ ∂F/∂λ   ∂F/∂C ]   with ∂F/∂C ≡ 0 (exact),
                  [ ∂V/∂λ   ∂V/∂C ]        ∂V/∂C = α/(64π) ≠ 0,
                                            ∂V/∂λ = (α/2)·∂J(0;λ)/∂λ (absorbable into C),
                                            ∂F/∂λ ≠ 0 on the deep and transition regions of MU_λ.
```

Its rank is 2 generically and drops to 1 **iff** `∂F/∂λ = 0`. Consequently:

- (S2) the observed vacuum density ρ_L is reproduced **exactly for every λ**
  by the shift `C = 64π a0²/α` (J(0)=0 convention): the vacuum datum selects a
  curve in (λ, C), never λ. Vacuum energy is λ-blind.
- (S3) the deep-slope identity `μ_λ ≈ λ·Y` fixes `a0 = s/λ`, i.e. `κ = 1/λ`:
  the dimensionless kernel parameter IS the inverse kappa; κ = 1/2 ⇔ λ = 2 is
  the adopted footing, never a consequence of the vacuum energy.
- (S4, negative control) setting C(λ) to produce κ = 1/2 is **calibration**,
  not derivation; the control is genuinely capable of failing (a principle of
  the action fixing C absolutely would flip it) and does not fail within the
  available action class.

**Symbol dictionary.** λ dimensionless kernel parameter (diagnostics 1/2, 1, 2,
3); n ≥ 1 MU_n channel count; `Y = g/s`; `s = c√(Gρ_L)` (m/s²); `μ_λ(Y) = 1 −
(1+Y)^{−λ}`; `B = g_N` baryonic acceleration; `a0 = κ s`, κ = 1/2 adopted;
`C` additive constant of the primitive (a0² units); `ρ_L` vacuum mass density
(kg/m³); α = 2 − K_B ∈ [7/4, 2]; G = 6.67430e-11, c = 299792458, M_sun =
1.98847e30, pc = 3.085677581491367e16 (SI). `G_N`, `G_bare`, `G_cosmo` are
**separate** symbols; only the framework-declared G is used here (no
renormalization map is invoked).

**Framework inputs (given, not derived):** `a0 = κ c√(Gρ_L)`, κ = 1/2;
`r_M = √(G M_b/a0)`; `v_flat⁴ = G M_b a0`. Footings: canonical
a0 = 9.3619e-11 m/s²; alternative a0 = 1.1279e-10 m/s² — reported under both
readings (fixed ρ_L ⇒ κ_eff; fixed κ ⇒ changed ρ_L), never simultaneously fixed.

**Boundary conditions / assumptions (stated, not derived):**
A1. Action class: corpus local action as in AS067 A1; J multiplies √−g only.
A2. Static sector: `μ_λ(g/s) g = B` with B prescribed (spherical baryonic
profile for the substitution check); no filter, no gate (this task never
touches MONO's heat filter).
A3. `μ_λ ∈ C¹((0,∞))`, positive, monotone increasing (response family).
A4. λ is a *parameter* of the action: it has no equation of motion in this
class (promotion to a field is an explicit extension, not used here).
A5. The zero-mode lemma (AS067 S1, K1/k01): the EL equations contain J only
through J′, ∂J/∂Y — kernel-independent, hence valid for every MU_λ member.

**Conclusions to be established:** S1 block-Jacobian and rank condition; S2
compensation surjectivity; S3 deep-slope identification κ = 1/λ; S4
calibration verdict; E1/E2 limiting regimes with leading neglected terms; F1/F2
independent-representation residuals; E3 ill-posedness of the absolute-zero
fixing.

## 2. The one-parameter primitive family and its primitives (step 2–3 of seed)

Response family `μ_λ(Y) = 1 − (1+Y)^{−λ}`. Primitives `J_λ(Y) = ∫₀^Y μ_λ(y)dy`
(closed forms, sympy-exact; each satisfies `J_λ′ = μ_λ` identically, and the
integration constant J_λ(0) is *absorbed into the free C(λ)* — the derivative
fixes the force, the constant is the remainder):

```
J_{1/2}(Y) = Y − 2√(1+Y) + 2          J_1(Y) = Y − ln(1+Y)
J_2(Y)     = Y − Y/(1+Y)              J_3(Y) = Y − (1/2)(1 − 1/(1+Y)²)
```
(`J(0)` of sympy's antiderivatives: −2, 0, 1, 1/2 for λ = 1/2, 1, 2, 3 — each
nonzero value is precisely the C(λ) that must be absorbed; no J(0)=0
normalization is imposed.)

**Force law:** `μ_λ(g/s)·g = B`; at λ = 2 the closed algebraic form is
`y·μ₂(y) = y²(y+2)/(1+y)²` with exact polynomial-inverse cubic
`y³ + (2−q)y² − 2qy − q = 0`, q = B/s (Lean-certified; used in F1).

**Deep and Newtonian limits (with leading neglected terms):**
- Deep, Y → 0: `μ_λ = λY − λ(λ+1)Y²/2 + O(Y³)` ⇒ `g = √(B·s/λ)·[1 +
  ((λ+1)/4)·√(B/(sλ)) + O(B/(sλ))]` — the deep law `g² = (s/λ)B` with the
  a0-line `a0 = s/λ`, κ = 1/λ; the leading neglected term has coefficient
  (λ+1)/4 (verified numerically: 0.7503 at q = 1e-6 vs predicted 0.75; the
  deep-window error scale err·√(q/2) ≤ 2.99e-4 over q ≤ 1e-3).
- Newtonian, Y → ∞: `g = B·[1 + (B/s)^{−λ} + O((B/s)^{−λ−1})]` — the end is
  λ-blind (every member collapses onto g = B); at λ = 2 the coefficient is 1
  (verified: median 0.9942 over B/s ∈ [10², 10⁵], predicted 1.0).

## 3. Jacobian of force and vacuum observables (S1)

Observable vector at fixed probes: F₁ = g at B/s = 0.01 (deep), F₂ = g at
B/s = 1 (transition), V = ρ_vac/ρ_L. Parameters (λ, C), C in a0² units.

Numeric finite differences (λ₀ = 2, δλ = 2e-5, δC = 2e-4):

```
∂F₁/∂C = 0.000e+00   ∂F₂/∂C = 0.000e+00   ∂V/∂C = 9.9472e-03 = α/(64π)  (exact, α = 2)
∂F/∂λ ≠ 0: singular values of ∂(F₁,F₂,V)/∂(λ,C): 1.965e-01, 9.947e-03  → rank 2
```

Rank-reduction condition: for the degenerate family `J(Y;λ) = J₀(Y) + λC₀`
(pure shift), ∂F/∂λ ≡ 0 and the Jacobian's singular values are (2.22e-02,
0.000e+00) → **rank 1**: λ is a pure label, the vacuum energy carries the only
λ-information and no datum selects λ. At the Newtonian end ∂F/∂λ → 0 (decay
~ln(q)/q; measured 0.000e+00 at B/s = 1e11 — below double-precision resolution
of the bisection, threshold 1e-6): the rank drop is a limit, absent at every
finite B.

**Physical identification of the condition (seed obligation).** Rank 2 means
(λ, C) are two genuinely independent observable directions: the measured deep
+ transition force fixes λ (a *fit*, excluded as proof — no observational
preference is used as mathematics), the measured vacuum density fixes the
combination C + J(0;λ) only. A *derivation* of κ that "removes a genuinely
independent freedom" would require the rank to drop by a *principle* — the
seed's claim is that C(λ) prevents the vacuum datum from doing so: the vacuum
energy is exactly independent of λ when C is allowed to adjust, and any choice
of λ is exactly realized. Lean-certified: `block_det`, `col_indep`, `col_dep`.

## 4. Vacuum-energy compensation surjectivity (S2) and the calibration control (S4)

With the J(0)=0 convention, `ρ_vac = α·C/(16πG c²)`. Demanding ρ_vac = ρ_L:

```
C_req = 16πG c² ρ_L/α = 64π a0²/α        (α = 2: C_req/a0² = 32π = 100.531;
                                           α = 7/4: C_req/a0² = 256π/7 = 114.893)
```

`ρ_vac/ρ_L = α·(64π/α)/(64π) = 1` — **exactly, for every λ ∈ {1/2, 1, 2, 3}
and every α ∈ {7/4, 2}** (Lean-certified: `calibr_ratio`, `calibr_dimens`).
The required shift is λ-*independent* in this normalization: the observed
vacuum energy is compatible with every member of the one-parameter family. The
identification step "κ = 1/2 ⇔ λ = 2 happens to match ρ_L" is bookkeeping:
a0 = s/2 and ρ_L = 4a0²/(Gc²) are the SAME statement as κ = 1/2 adopted.

**Negative control (must be capable of failing) — PASSED.**
- C is a zero mode of the static equations (AS067 S1, kernel-independent: EL
  contains only J′, J″): the action's equations cannot fix C, in the λ-family
  or outside it. The control could fail *only* if some principle pinned C
  absolutely; the only such principle available to this action class is the
  "empty Newtonian vacuum" fixing J(∞ + ...) = 0.
- That principle is **ill-posed** for MU_λ: the primitive span
  `I_n(Z) = 2∫₀^Z y μ_n(y) dy ~ Z²` diverges for every n (measured log-log
  slopes 2.0003, 2.0000, 2.0000 for n = 1, 2, 3 over Z ∈ [10³, 10⁶]) — there
  is no Newtonian-end anchor; and for the corpus's *saturating* carriers the
  same fixing gives ρ_vac < 0 (k01 K3, AS067 S6a) — the wrong sign. Hence no
  member of the family, and no available extension inside the action class,
  turns "set C to reproduce ρ_L at κ = 1/2" into a derivation. The control
  is genuine: it fails loudly the moment a positive, finite, absolute fixing
  of the primitive zero appears (that would be a derivation) — none exists in
  this class.

## 5. Independent representations (seed step 4) — actual residuals

- **F1.** λ = 2 force law solved two independent ways: 400-step bisection vs
  the exact cubic roots of `y³ + (2−q)y² − 2qy − q = 0` over q ∈ [10⁻⁴, 10²]
  (50 samples): `max |y_bis − y_cub| = 7.1e-14`; substitution residual
  `max |μ₂(y)y − q|/q = 2.8e-14` — the solved g satisfies the original
  equation to machine precision.
- **F2.** 200-point Hernquist-type profile (M = 10¹¹ M_sun, a_h = 3 kpc,
  r ∈ [0.1, 100] kpc): max relative substitution residual 2.2e-16.
- **E1/E2.** Deep and Newtonian asymptotes with the leading-order coefficients
  confirmed (0.7503 vs 3/4; 0.9994 vs 1, max |coeff−1| = 0.0198 over
  B/s ∈ [10², 10⁵]) — actual residuals, not booleans.
- **S0.** Symbolic (sympy): `J_λ′ − μ_λ = 0` exactly at λ = 1/2, 1, 2, 3
  (residual 0, closed forms in §2); deep slope `lim μ_λ/Y = λ` exactly
  (symbolic); Newtonian recovery `lim μ_λ = 1` exactly (symbolic); μ_n′(0) = n
  for n = 1..6 (symbolic).

## 6. Footings (both readings, separately)

s = c√(Gρ_L) = 1.872380e-10 m/s² (= 2 a0_canonical, fp-exact); ρ_L =
5.844412e-27 kg/m³.

- **Canonical** a0 = 9.3619e-11: κ = 1/2, λ = 2 — the adopted footing.
- **Alternative** a0 = 1.1279e-10, fixed ρ_L: κ_eff = 0.602388 ⇒ λ_eff =
  1.660059 — **not a channel count** (identification constraint only, mirroring
  PD01's exclusion of non-integer counts).
- **Alternative**, fixed κ = 1/2: ρ_L′ = 4 a0_alt²/(Gc²) = 8.483090e-27 kg/m³
  = 1.4515 ρ_L.
- The dimensionless statements S0–S4 never invoke a0's numerical value (they
  use only its role as the scale in Y = g/s): they apply to both footings
  unchanged (contract's "dimensionless theorem proved once").

## 7. Verdict and closure implication

**Strongest surviving statement.** Within the corpus A1-class local action, for
the MU_λ response family: the observables' Jacobian in (λ, C) is block
lower-triangular with ∂F/∂C = 0 exactly and ∂V/∂C = α/(64π) ≠ 0; rank 2 on the
family (∂F/∂λ ≠ 0 in deep/transition), rank 1 iff ∂F/∂λ = 0. The observed
vacuum energy reproduces exactly at every λ via the allowed C(λ): **the vacuum
energy datum is blind to the dimensionless kernel parameter; κ = a0/s = 1/λ is
fixed only by the deep-slope identity a0 = s/λ, i.e. by adoption at λ = 2
(κ = 1/2), never by the vacuum.** The "set C(λ) to produce κ = 1/2" control is
calibration, passed with a genuine capability to fail (any absolute,
positive, finite fixing of the primitive zero would flip it; the available
fixings are ill-posed for MU_λ and sign-wrong for the saturating carriers).

This is a scoped structural/negative result for the *derivation route* of
gate 13 (cosmological acceleration-scale relation): no equation of this
action class relates λ (hence κ) to ρ_L. The preserve-arm (κ = 1/2 adopted
input) is untouched and consistent — this does not falsify the framework.

**What this does NOT establish.** No statement about Q/RAR/EXP/MONO kernels
beyond the generic-J zero-mode lemma; no claim about the full thirteen-item
target (criterion B, DOF counts, PPN, lensing, stability — untouched); no
empirical test; λ_eff = 1.6601 at the alternative footing is an
identification constraint, not a fit; per-object force fitting is explicitly
not used as a mathematical proof.

## 8. First missing bridge (next unresolved implication)

To convert κ = 1/2 from adopted input to derived, a structure outside the
A1-class must (i) give C an equation (fixing the primitive's zero *absolutely*
with the correct sign and O(1) size at the canonical footing — the quantified
target of AS067 §9), AND (ii) additionally couple λ to ρ_L so that ∂V/∂λ ≠ 0
survives the C-compensation — the new statement of this task: a mechanism in
which the vacuum datum selects λ because the shift C is no longer free. The
rank-reduction theorem here shows the two requirements are one: any such
mechanism necessarily makes the action's observables rank-1 in (λ, C) with a
*determined* λ — the exact shape of the missing equation
`λ = λ(ρ_L, a0; action data)` is the open dependency.

## 9. Reproducibility

- `as069_audit.py` (sympy + numpy only) + `run_bounded.py` (bounds), raw
  stdout `as069_audit.out`, `/usr/bin/time -l` trace `as069_audit.time`,
  `as069_results.json` (17/17 checks PASS), `as069_observables.npz`.
- Bounds: RLIMIT_CPU = 120 s (enforced), threads = 1 (env OPENBLAS/OMP/MKL/
  VECLIB/NUMEXPR → 1), RLIMIT_AS = 512 MB **not enforceable on this macOS
  host** (kernel refuses finite RLIMIT_AS; measured instead): wall 0.354 s,
  max RSS 88.3 MB — both far inside the declared envelope.
- Lean certificate: `AS069_jacobian.lean` — 10 theorems, compiled
  `lake env lean` in `fable_independent_2026/lean_2026` (compile host only;
  nothing written there), zero `sorry`, axioms per theorem ⊆ {propext,
  Classical.choice, Quot.sound} (unfiltered `#print axioms`, see
  `AS069_axioms.out`). House-traps honored: `field_simp`-then-`ring` ordering,
  `deriv_sub` premises, `deriv_id`'s `id` pattern, `fun_prop` does not mark
  `HasDerivAt` in this mathlib (v4.34.0-rc2-class) — derivative value computed
  via `differentiableAt` premises + `deriv_id''`/`deriv_const_add_id`.
