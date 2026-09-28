# AS073 — Coefficient selection by a variational principle: derivation and controls

**Run:** `AS073-r1-20260928T1121Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent
**Task SHA-256 (verified at start):** `f6c9ad296de3670399905dba2e1690e10377e9a51aa1589cd728cd82c7305bb7`
**Outcome:** counterexample (obstruction theorem with scoped positive content)

---

## 1. The claim under test and the symbol dictionary

**Named claim (AS073 principal test):** *"Candidate objective I[mu] with fixed endpoint
values has stationary equation δI/δμ = 0"* — i.e. an endpoint-fixed variational principle
over response functions selects the coefficient (the deep-MOND slope, hence κ).

**Symbols (all SI unless noted):**
`B = g_N = g_bar > 0` (baryonic Newtonian acceleration), `g` total radial acceleration,
`s = c·sqrt(G·ρ_L)` the vacuum rate (argument unit, `Y = g/s` dimensionless), `μ` the
response function, `μ_λ(Y) = 1 − (1+Y)^{−λ} = 1 − exp(−λ·log(1+Y))` the diagnostic family,
`λ` a positive finite dimensionless slope parameter, `q > 0` a kinetic exponent,
`F(μ, μ')` an autonomous density, `φ(μ) > 0` an engagement weight, `Φ' = φ`,
`V(μ) = μ²(1−μ)²` the double-well potential, `G_N` Newton coupling, `G_bare`, `G_cosmo`
kept separate (never identified), `n ≥ 1` symbolic channel count (MU_n family).

**Framework base (adopted inputs, not derived here):**
```
a0 = κ·c·sqrt(G·ρ_Lambda),   κ = 1/2 ADOPTED
s = c·sqrt(G·ρ_Lambda)  ⇒  a0 = κ·s = s/2 on the canonical footing
r_M = sqrt(G·M_b/a0),   v_flat^4 = G·M_b·a0
ρ_Lambda = 4·a0²/(G·c²)
```
**Admissible class under test:** `A = { μ : [0,∞) → [0,1], C¹, μ(0)=0, μ(∞)=1, μ'(0) exists }`.
The endpoint values μ(0)=0, μ(∞)=1 are exactly the corpus boundary structure (PD08 steps 1–2:
zero drive at the frozen vacuum, saturation at full drive).

**Branches:** this task's declared branch is the CORE coefficient with the conditional
MU_n statistical response; the diagnostic family μ_λ is the MU_λ completion class
(λ = 2 is the operative MU2 in s-units: `mu2(x) = 1−(1+x/2)^{−2} = 1−(1+Y)^{−2}`, Y = x/2 = g/s).
No conclusion is transferred to the operative filtered-MONO target (criterion B); Q, RAR,
EXP, MONO appear nowhere in the conclusions.

---

## 2. Step 1 — precise claim, boundary conditions, framework vs conclusion

**To be established:** does an endpoint-fixed objective I[μ], δI/δμ = 0, with the two
endpoint conditions, determine the deep slope μ'(0) — and through the L230 matching chain
(Sec. 4, T3) the coefficient κ = 1/μ'(0)?

**Framework inputs (listed, never silently promoted):** κ = 1/2; `s = c√(Gρ_L)`;
the vacuum-units normalization (argument in Y = g/s with unit linear per-channel response);
the L230 chain algebra (κ = 1/n); the double-well/-type potential class as the "physically
natural" selection density; the kinetic densities (μ')^q.

**Conclusion candidates:** nothing is assumed about existence/uniqueness of stationary
points, minimizers, or slope values. All three sources were inspected first:
- **PD01** (`37e39d1abb8…c74d`): the channel-count derivation — slope = OR-channel count; κ = 1/count after the L230 principle; count {1,2} from the metric's static response; data select 2. Its D1 premise is the OR identification; the full completion stays empirical.
- **PD08** (`83f6054cdfb1…f0cfb`): action `S_kin = (1/8πG)∫s²K(|gradΦ|/s)d³x`; μ = 1−(1−p)²; p'(0)=1 (fraction identity, ONE-scale action); spherical matching → a0 = s/2. Contains **no functional over response functions** whose EL is δI/δμ = 0 — the variational object of this task is *absent* from the source.
- **k01** (`8df5a3ab5a38…35b25c`): zero-mode theorem K1 (J enters static EL only through J′: additive constant of the primitive is invisible), K2 (Λ explicit and free ⇒ no equation relates a0 to Λ: outcome 3), K3/K4 (Λ-free repair fails on sign and size), K5 (QUMOND reading gives κ≈1 and is the forbidden branch).

**Consequence for Step 2 (per work order):** the functional read from the source does not
exist → construct clearly labelled examples and test whether argument rescaling leaves a
free slope. That is Sections 3–6; the minimizer is never retrofitted as a discovery —
the reverse-engineering control (Sec. 7) explicitly identifies how a target can be installed.

---

## 3. Step 2 — constructed objectives and the free-slope test

Four labelled constructions, all with the *same* fixed endpoints μ(0)=0, μ(∞)=1:

**(E1) q=1 (total-derivative) objective.** `I = ∫₀^∞ φ(μ)·μ' dY`. Since `φ(μ)μ' = d/dY[Φ(μ)]`
with `Φ' = φ`, by the fundamental theorem **I is the same constant `Φ(1) − Φ(0)` for every
μ ∈ A**. The EL vanishes identically (`φ'μ' − d/dY φ(μ) = 0`), so **every** admissible
function is stationary: the objective is boundary-controlled (a zero mode in the k01 K1
sense, transported into the response-functional language). No slope, no κ.

**(E2) kinetic objectives.** `I_q = ∫₀^∞ φ(μ)·(μ')^q dY`, q ≠ 1, φ > 0.
EL (Sec. 4, T2): scale-covariant; the argument-rescaling orbit of any stationary point is
stationary with rescaled slope; for q ≠ 1 the action is homogeneous along the orbit,
`I(T_λμ) = λ^{1−q}I(μ)`, so inf_I = 0 is unattained: **no global minimizer in A** for any
q ≠ 1, φ > 0. The pure kinetic member (φ ≡ 1, q = 2) evaluated on the diagnostic family
(Sec. 6) *ranks the target kernel worst*: `I_kin[μ_2] = 4/5 > I_kin[μ_1] = 1/3 >
I_kin[μ_{1/2}] = 1/8`, and the infimum 0 at n → 0⁺ is not attained (n²/(2n+1) → 0).
The "most natural" functional both rejects n = 2 and selects nothing.

**(E3) well-type objective.** `I = ∫₀^∞ [μ'²/2 + V(μ)] dY`, `V = μ²(1−μ)² ≥ 0`,
`V(0) = V(1) = 0`. First integral `E = μ'²/2 − V(μ)` is constant along EL solutions
(Sec. 4, T2(iii)); with finite action and μ(∞)=1, E = 0, forcing μ'(0)² = 2V(0) = 0;
IVP uniqueness at (0, 0, 0) gives μ ≡ 0 — contradicts μ(∞) = 1. **No admissible stationary
point exists on the half-line.** Numerically (Sec. 6): the (0,0) trajectory is identically
zero (max|μ| = 0 on [0,12]); any nonzero start c ≠ 0 has E = c²/2 > 0 and escapes through
μ = 1 in finite time (t_cross = 4.514 for c = 0.1, 1.010 for c = 1.0) — never an admissible
solution; energy drift along the pre-blow-up arc ≤ 2.4e-13 (integrator-quality invariant).

**(E4) reverse-engineered objective (control, Sec. 7).** `I_α[μ] = ½∫₀^∞ (μ − μ_α)² dY`:
δI_α/δμ = μ − μ_α — the target kernel sits *verbatim* inside the objective; its minimizer
is exactly the inserted μ_α (slope α, α ∈ {1/2, 1, 2}).

**Free-slope test answer:** yes — the seed's diagnostic counterexamples (λ = 1/2, 1, 2)
are three admissible kernels with identical endpoints and slopes {1/2, 1, 2}
(Sec. 6, S2a); and within the natural autonomous class, rescaling the argument of any
stationary point yields a stationary point with rescaled slope (T2). The slope is a free
parameter of the class; the endpoints carry zero slope information (Lean-certified, Sec. 8).

---

## 4. Step 3 — the algebra, with all scale factors and signs

**T1 (endpoint degeneracy).** For every λ > 0, `μ_λ(Y) = 1 − exp(−λ·log(1+Y)) = 1 − (1+Y)^{−λ}`
(equality for 1+Y > 0, all λ):
- endpoint: μ_λ(0) = 1 − e^0 = 0;  (lean `muLam_zero`)
- saturation: μ_λ(Y) → 1 as Y → ∞ (exp(−λ log(1+Y)) → 0; lean `muLam_tendsto_atTop`);
- range: 0 ≤ μ_λ(Y) ≤ 1 for 0 ≤ Y (log(1+Y) ≥ 0, λ > 0; lean `muLam_nonneg`, `muLam_le_one`);
- slope: `μ_λ'(0) = [d/dY (−λ·log(1+Y)) at 0]·exp(0) ·(−1)… = λ`:
  derivative of 1 − e^{−λ log(1+Y)} at Y = 0: chain rule gives `0 − e^{0}·(−λ · 1/(1+0)) = λ`
  (lean `muLam_hasDerivAt_zero`, `muLam_slope_half/one/two`).
  Series (sympy, exact): `μ_λ(Y) = λY − λ(λ+1)Y²/2 + λ(λ+1)(λ+2)Y³/6 + O(Y⁴)` (Y < 1),
  tail `1 − μ_λ(Y) = (1+Y)^{−λ}` **exactly** (all Y > 0).
  Leading neglected terms and domains: deep linearization error ~ −λ(λ+1)Y²/2 on Y < 1;
  saturation defect (1+Y)^{−λ} on all Y.

**T2 (variational class classification).** Let `F(μ,μ') = φ(μ)(μ')^q`, q > 0, φ > 0, C¹
(autonomous separable densities; the only local class with no second scale — Y is already
dimensionless in s-units, and an explicit Y-dependence would smuggle back an independent
scale). The EL operator `δI/δμ = ∂_μF − d/dY[∂_{μ'}F]` obeys, for `ν(Y) = μ(Y/λ)`:

```
δI/δμ[ν](Y) = λ^{−q} · (δI/δμ[μ])(Y/λ)          (exact symbolic identity, sympy ≡ 0)
```

Derivation: `∂_μF(ν,ν') = φ'(μ(Z))·(μ'(Z)/λ)^q = λ^{−q}φ'(μ(Z))μ'(Z)^q`, and
`d/dY[∂_{μ'}F(ν,ν')] = λ^{−q}·(d/dZ)[qφ(μ(Z))μ'(Z)^{q−1}]` with Z = Y/λ — the λ-powers
cancel to a single λ^{−q}.  Consequences:
- (i) if μ* is stationary, the **whole orbit** {μ*(Y/λ)} ⊂ A is stationary, with slopes
  μ*'(0)/λ = μ*'(0)·λ′: stationary slopes are never selected;
- (ii) `I[T_λ μ] = λ^{1−q}·I[μ]` (change of variable Z = Y/λ): for q ≠ 1 the action is an
  orbit-homogeneous function, `inf_A I = 0` is unattained (I > 0 on A since μ' ≢ 0 and
  φ > 0) — **no global minimizer exists** for any q ≠ 1;
- (iii) q = 1: total derivative, EL ≡ 0 identically (verified: sympy 0; and the generic
  reduction `d/dY Φ(μ) − φ(μ)μ' = (Φ′ − φ)·μ'`), action constant on A (E1);
- (iv) well-type `F = μ'²/2 + V(μ)`: first-integral identity
  `d/dY[μ'²/2 − V(μ)] + μ'·(δI/δμ) ≡ 0` (sympy 0), whence the (iii) no-go of Sec. 3.

**T3 (L230 matching chain — the coefficient link).** Deep-MOND spherical point source with
response slope λ: `(1/r²)d/dr[r²(λg/s)·g] = 4πGρ` ⇒ `λg²/s = GM/r²` ⇒
`g² = (s/λ)(GM/r²) = (s/λ)g_N`. Matching to the a0-line `g² = a0·g_N`:
`a0·g_N = (s/λ)·g_N` ⇒ `a0 = s/λ` (positivity of g_N for cancellation) ⇒
`κ = a0/s = 1/λ`.  **κ is the reciprocal of the deep slope** — exact algebra
(sympy: `κ = 1/n`, `a0 = s/n`; Lean: `deep_g_squared`, `deep_mond_point_mass`,
`a0_unique`, `kappa_eq_one_div_slope`).  Diagnostic map: λ ∈ {1/2, 1, 2} ⇒
κ ∈ {2, 1, 1/2}. The adopted κ = 1/2 is the λ = 2 member of the same continuum —
undistinguished by any endpoint-fixed variational principle in the tested class.

**Units/sign audit.** s has units of acceleration (m/s²) from
`s = c·√(G·[ρ_L])` = (m/s)·√((m³kg⁻¹s⁻²)(kg m⁻³)) = (m/s)·(m/s) = m/s² ✓. Y = g/s
dimensionless ✓. μ_λ dimensionless, sign: μ_λ ≥ 0 because the driving term is `−exp(…)`
with exp ∈ (0,1] ✓ (Lean range theorems). κ = a0/s = 1/λ dimensionless ✓. Footings in
Sec. 5.

---

## 5. Both footings (carried separately, never sharing fixed ρ_L and fixed κ)

| quantity | canonical a0 = 9.3619e-11 m/s² | alternative a0 = 1.1279e-10 m/s² |
|---|---|---|
| ρ_Lambda (kg/m³) | 5.844412e-27 | 8.483090e-27 (κ = 1/2 fixed) |
| s = c√(Gρ_L) (m/s²) | 1.872380e-10 | 2.255800e-10 |
| κ = a0/s | 1/2 exactly (adopted) | 0.602388 (ρ_L fixed at canonical) — effective κ |
| slope λ = 1/κ | 2 | 1.660059 |

The theorem content is dimensionless; it applies to both footings with the entries above.
Note the framework's rule is respected: the alternative footing is either (a) κ fixed at
1/2 with the density changed to 8.4831e-27, or (b) ρ_L fixed at 5.8444e-27 with effective
κ = 0.60239 — never both fixed.

---

## 6. Step 4 — independent checks (actual residuals, not booleans)

Prototype `compute_as073.py` (14/14 PASS, 0.67 s wall, 113 MB peak RSS, single thread,
alarm(120) enforced, mpmath dps = 50):

| check | measured | tolerance |
|---|---|---|
| S0 footings: s_can = 2·a0_can | 1.872380e-10, rel diff < 1e-15 | 1e-15 rel |
| S1a EL covariance, generic φ, μ, q (sympy) | exact 0 | ≡ 0 |
| S1a2 covariance, FD (φ=1+μ², μ=tanh, q=2, λ=0.7) | 1.735e-08 | < 1e-4 (fd) |
| S1b q=1 total derivative (sympy) | 0; EL[q=1] ≡ 0 | ≡ 0 |
| S1c well first integral + μ′·EL (sympy) | 0 | ≡ 0 |
| S1d kappa chain (sympy) | κ = 1/n | ≡ 1/n |
| S1e deep series | n·Y − n(n+1)Y²/2 + … | coeffs exact |
| S2a slopes μ_λ′(0) = λ, λ ∈ {1/2,1,2} (central FD, h=1e-6, 50 dps) | residuals 3.1e-13…8.0e-12 | < 1e-8 |
| S2a2 endpoints: μ_λ(0)=0; 1−μ_λ(1e8) = (1+1e8)^{−λ} | matches to 1e-45 | 1e-45 |
| S2b rescaling family vs OR family (O(1) differences 0.0001…0.0833) | rescaling exact for D_λ; OR class ≠ rescaling | > 0.05 differences |
| S2c q=1 action constant: I[μ_λ] = Φ(1)−Φ(0) = 1.5 for λ ∈ {1/2,1,2} | 1.5 to 1e-20 | 1e-20 |
| S2d kinetic I_kin = n²/(2n+1): {0.1250, 0.3333, 0.8000} | exact to 1e-13 tail | ranking + positivity |
| S2e well no-go (DOP853, rtol 1e-12): (0,0) → μ ≡ 0; c=0.1 → crosses 1 at t=4.514 then blows up; c=1.0 → crosses at t=1.010; energy drift (μ<1.5) ≤ 2.4e-13 | as listed | trivial-only + escape |
| S2f reverse engineering: I_α[μ_α] = 0 (grid); cross I_α[μ_β|β≠α] = {0.157, 0.736, 1.468} > 0; ε-growth ratio 4.0000 vs 4 | 4.0000 | < 1e-6 rel |

---

## 7. Step 5 — negative control (chosen to be capable of failing) and strongest statement

**NC1 — reverse engineering (the seed's designated control).** "Choose I specifically to
minimize at the target kernel and identify the reverse engineering." Executed: I_α with the
target verbatim; the identification is that the slope parameter α appears *inside* the
objective's coefficients (the integrand is built with μ_α). Measured: EL residual at the
inserted target = 0 on a 501-point grid; quadratic growth d²I/dε² = ∫ψ² (ratio 4.0000 when
ε doubles); cross-objectives strictly penalize every other diagnostic kernel. *Capable of
failing:* if the same I_α had selected the target *without* α inside, the control would have
failed (it did not).

**NC2 — the natural kinetic functional.** I_kin = ∫(μ′)²: if the variational route had real
selective power, a "natural" objective would at least not rank the target worst. Measured:
I_kin[μ_2] = 0.8 > 0.333 > 0.125, inf = 0 unattained — the natural functional *rejects*
n = 2 and selects nothing. *Capable of failing:* a ranking favoring n = 2 would have
contradicted this control.

**NC3 — well-type infeasibility (boundary case).** The vacuum-side endpoint μ(0)=0 coincides
with the potential's zero; the first integral forces μ′(0) = 0 ⇒ trivial solution only for
E = 0, while E > 0 escapes through μ = 1 in finite time (measured crossing/blow-up). No
admissible stationary point exists — the "physically motivated" selection problem is empty.
*Capable of failing:* a well-type solution with μ(∞)=1 would have falsified it.

**NC4 — endpoint degeneracy.** Three kernels, identical endpoints, slopes {1/2, 1, 2}
(measured residual < 8e-12 at 50 dps; Lean-certified). *Capable of failing:* if the
endpoint conditions pinned μ′(0), the three slopes could not coexist.

**Strongest surviving statement (scoped theorem, counterexample to the named claim):**

> **AS073-T (obstruction).** Let A be the endpoint-fixed response class (μ C¹,
> μ(0)=0, μ(∞)=1, [0,1]-valued) and let I[μ] = ∫₀^∞ F dY be any objective whose density
> is (a) autonomous separable, F = φ(μ)(μ′)^q, q > 0, φ > 0, or (b) well-type
> F = μ′²/2 + V(μ), V ≥ 0, V(0) = V(1) = 0. Then the variational principle δI/δμ = 0 with
> the two endpoint values **does not determine the deep slope μ′(0)**: the stationary set
> is either empty (case b), or consists of argument-rescaling orbits with freely rescaled
> slopes (case a, q ≠ 1), or is all of A with the action constant (case a, q = 1); no
> global minimizer with finite positive action exists for any q ≠ 1. Any objective whose
> minimizer is a prescribed kernel (e.g. μ_2, slope 2, κ = 1/2) contains that kernel's
> slope as an explicit coefficient (reverse engineering, NC1). Consequently, via the L230
> chain κ = 1/slope (T3, Lean-certified), **no endpoint-fixed variational principle in
> this class derives κ = 1/2**: κ remains the adopted framework input, exactly as
> PD01/PD08's fractional premise and k01's additive zero mode (outcome 3) already record.

**Domain:** half-line response functions with the stated endpoint structure; λ-scale orbits;
diagnostics at λ ∈ {1/2, 1, 2}; both a0 footings via s (Sec. 5). No operative-branch
(filtered MONO, criterion B) conclusion is drawn: the MU_λ family is used only as the
declared conditional statistical-response diagnostic.

---

## 8. Lean certificates

`AS073_variational_selection.lean` (13 theorems, in the run dir; compiled from
`fable_independent_2026/lean_2026` via `lake env lean <abs path>`, exit 0, zero warnings,
zero sorry):

- **Part A (T3):** `deep_g_squared`, `deep_mond_point_mass` (g² = (s/n)g_N),
  `a0_unique` (mul_left_cancel₀ on g_N), `kappa_eq_one_div_slope` ((s/n)/s = 1/n by
  field_simp) — the coefficient = 1/slope chain.
- **Part B (T1):** `muLam_zero`, `muLam_tendsto_atTop` (exp(−λ log(1+Y)) → 0 via
  hplus → log → λ-mult → neg → exp_atBot), `muLam_nonneg`, `muLam_le_one`,
  `muLam_hasDerivAt_zero` (chain rule: const_add, log, const_mul, exp, sub),
  `muLam_slope_half/one/two`, `slopes_distinct` (1/2 ≠ 1 ≠ 2 — the diagnostics).

**Unfiltered axiom ledger** (in compile output, 13/13): every theorem depends on exactly
`[propext, Classical.choice, Quot.sound]` — the allowed set; hard bar met.

---

## 9. Execution bounds (declared and enforced)

| bound | declared | enforced |
|---|---|---|
| wall | ≤ 120 s | signal.alarm(120); observed 0.67 s (prototype) + 3–9 s (Lean) |
| memory | ≤ 512 MB | RLIMIT_AS rejected on this macOS host (recorded honestly); observed peak RSS 112.6 MB |
| threads | 1 | single process, OMP_NUM_THREADS=1, serial scipy/mpmath; no subprocesses |
| grids | bounded | FD h = 1e-6 (50 dps), quad intervals ≤ 6, IVP ≤ 6000 steps, ≤ 501-diagnostic points |

---

## 10. Reading and first-principles statement

The seed asked whether a variational principle *removes a genuinely independent freedom*.
Answer, scoped to the natural endpoint-fixed response-functional class: **no** — the
freedom survives as (i) the argument-rescaling orbit (T2i), (ii) the unattained infimum
(T2ii), (iii) the infeasible well problem (T2iv), and (iv) the verbatim target inside any
engineering objective (NC1). The result is consistent with — and places in the
δI/δμ language — the corpus's own three anchors: k01 K1/K2 (additive zero mode: no
equation of the action relates a0 to Λ), PD08 step 3 (fraction identity p′(0) = 1 is a
**premise** of the one-scale action, not a variational output), and PD01 (the slope is the
OR-channel count of the metric's static response, selected by data at 0.5/1.2σ vs 7/10σ —
not by any action). |κ = 1/2 remains an adopted input; the route to derive it is the
channel algebra + data (PD01/PD08), not an endpoint-fixed variational principle.

**First-principles ledger for this run:** primitives: G, c, M_sun, pc, κ = 1/2 adopted,
a0 footings; measured calibrations: none fitted; derived here: T1 (endpoint/slope structure
of the diagnostic family, Lean), T2 (EL covariance + q=1 constancy + well no-go + no-minimizer),
T3 (κ = 1/slope, Lean), the reverse-engineering identification, the residual ledger.
Not derived: κ = 1/2; any operative-branch statement; any empirical claim.

---

## 11. Child proposal (ready, not dispatched)

**AS073.C01 — "Non-autonomous and constrained endpoint-fixed objectives: does any
explicit-scale or Lagrange-multiplier selection fix the slope?"** — Target: extend the
classification to densities F(Y, μ, μ′) with explicit Y-dependence (a smuggled scale) and
to constrained problems (fixed ∫μ, fixed action): claim — slope selection in these classes
is either reverse-engineered (the target's scale appears in F or in the multiplier's
value-equation) or absent; the discriminating control: any F whose EL admits slope-2 as the
unique stationary slope has μ_2 extractable from F's coefficients. Duplicate check:
AS053.C01 (second-order slope condition on the completion) and AS059 (general static
two-slot action) are different fingerprints — this child tests *selection functionals over
responses with explicit-scale/constraint structure*, which neither addresses; no live
equivalent in the child registry/FGF queue. Full spec: `branches/AS073/AS073.C01.md`.