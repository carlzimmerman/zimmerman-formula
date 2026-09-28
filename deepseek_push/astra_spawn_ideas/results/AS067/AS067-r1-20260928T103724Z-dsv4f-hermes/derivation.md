# AS067 — Additive vacuum zero mode in the local action (audit)

**Run:** `AS067-r1-20260928T103724Z-dsv4f-hermes`
**Worker:** deepseek-v4-flash-0731 (OpenRouter) / Hermes subagent on macOS (x86 Apple Silicon host)
**Task seed sha256:** `c7fd82f8402252ef2346ae8c49e30b4d8ff0f6183ed950aa354bb7f396d0a6a8` (verified on disk before execution)
**Sources pinned and verified against SOURCE_MANIFEST.json:**
- `deepseek_push/PD01_polarization_count.py` — `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d` ✓
- `deepseek_push/PD08_particle_free_derivation.py` — `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb` ✓
- `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` — `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c` ✓

**Branch discipline.** Conclusions are drawn only for the MU_n response family (symbolic n ≥ 1, operative n = 2) and for the generic-J zero-mode theorem, which is kernel-independent (it holds for any differentiable J, hence also for the operative filtered-MONO primitive — flagged explicitly as a generic statement, not as a MONO computation). Q, RAR, EXP, MONO are never imported to repair or extend any result here. The affected operative gate is **requirement 13 (cosmological acceleration-scale relation)** of the amended thirteen-item target; criterion B and requirement 1 are untouched.

---

## 1. Precise claim, symbols, boundary conditions, assumptions

**Named claim (the seed's mathematics line).** In the corpus's local action (k01, g03t convention)

```
S = (1/16 pi G) ∫ d⁴x √-g [ R − 2Λ − α J(Y) − K(Q) + 2α J^μ ∂_μ φ ] + S_m,
α := 2 − K_B,   Y = q^μν ∂_μ φ ∂_ν φ,   J^μ the khronon/MOND coupling current,
```

the additive zero mode of the MOND primitive satisfies

```
J(Y) → J(Y) + C   ⟹   Λ_eff = Λ + (2−K_B) J(0)/2 + K(Q0)/2 ,
```

i.e., on the FLRW background (Y = 0, Q = Q0) the added constant enters only through the
effective cosmological constant with coefficient α/2 = (2−K_B)/2.

**Symbol dictionary.** `Λ` explicit cosmological constant (m⁻²; c=1 convention in the algebra, SI restored below); `α = 2−K_B ∈ [7/4, 2]` for K_B ∈ [0, 1/4] (corpus's audited range); `J` the MOND kinetic primitive (units of acceleration-squared, i.e. L²T⁻⁴ SI, L⁻² in c=1); `K` the coherence-kernel function, `Q0` its background value; `φ` the MOND scalar (velocity-squared potential), `Ψ` the metric potential; `ρ_b` baryonic density; `C` an arbitrary constant; `λ ∈ {1/2, 1, 2}` the diagnostic coefficient of the shift (seed-mandated); `s = c√(Gρ_L)` (m/s²), `Y = g/s` dimensionless, `a0 = κ s` with **κ = 1/2 adopted as framework input** (never claimed derived here); MU_n response `μ_n(Y) = 1 − (1+Y)^(−n)`.

**Framework inputs (given):** `a0 = κ c √(G ρ_L)`, κ = 1/2; `r_M = √(G M_b/a0)`; `v_flat⁴ = G M_b a0`; `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI). Footings: canonical `a0 = 9.3619e-11 m/s²` and alternative `a0 = 1.1279e-10 m/s²`, reported separately under both readings (fixed ρ_L ⇒ κ_eff; fixed κ ⇒ changed ρ_L). `G_N`, `G_bare`, `G_cosmo` remain **separate** symbols; this audit's sectors use only the single framework-declared G (the corpus's G-renormalization factors of k01 K4 are cited as recorded context, not used as an identification).

**Boundary conditions / assumptions (stated, not derived):**
A1. The action class is the corpus's local scalar-telegraphic action: `J` enters as `−α J(Y) √-g` and `Y` is metric-independent at the order kept (`q^μν` built from the fixed background structure). Excluded: actions where the shift C multiplies a metric-dependent function `f(g)J(Y)` (then Λ-compensation fails pointwise — see §7), and actions with derivative couplings of the constant sector to other fields.
A2. Static sector: weak-field two-potential metric convention of PD01 B1; the reduced static Lagrangian `L = −2(∇Ψ)² + 2α ∇Ψ·∇φ − α J(|∇φ|²) − ρ_b(Ψ+φ)` (overall 1/16πG dropped) of k01 K1.
A3. Background sector: FLRW with `φ̇ = 0` (Y = 0) and constant `Q = Q0` (k01 K2).
A4. The response-to-primitive dictionary: in the Δ(z)-parametrization, `s := g_N/a0 = z μ(z)`, `J(0) = −I a0²`, `I = 2 ∫ z μ(z) dz` (k01 K3 convention); the MU_n family is treated both truncated (μ = 0.99 end) and untruncated.

**Conclusions to be established (they are not inputs):** S1 static invariance; S2 background shift formula; S3 exact action symmetry under the compensated pair; S4 tightness (constants are the whole invariant subspace); S5 κ-non-derivability inside the action class; S6 repair audit (sign, convergence, size).

## 2. Static invariance, re-derived with coefficients retained (S1)

The reduced static Lagrangian with α retained:

```
L = −2 Ψ′² + 2α Ψ′φ′ − α J(φ′²) − ρ_b(Ψ + φ).          (1D reduction, x the radial/axial variable)
```

Euler–Lagrange (sympy `euler_equations`, generic J):

```
EL_φ :  2α [ 2φ′² φ″ J″(φ′²) + φ″ J′(φ′²) − Ψ″ ] + ρ_b = 0        (J enters ONLY as J′, J″)
EL_Ψ :  4 Ψ″ − 2α φ″ + ρ_b = 0                                     (no J at all)
```

Both equations contain J only through its derivatives. Hence for ANY constant C and any λ:

```
EL(J + λC) − EL(J) = 0   exactly (symbolic residual 0; λ = 1/2, 1, 2 and symbolic λ checked).
```

Physical reading: the additive constant is invisible to the static dynamics; it reappears only in the
energy density (uniform shift `+αC` of the Hamiltonian density), i.e. exactly as a vacuum-energy term.

**Independent representation (seed step 4).** The same statement was verified on the *discretized* action:
the central-difference gradient `∂S/∂φ_i` of the 1D lattice action with 401 nodes, Gaussian profiles,
was computed for `J(Y) = Y` and `J(Y) = Y + C`:

```
||∇S(J+C) − ∇S(J)||_∞ = 6.66e-10  (rel 7.3e-10; finite-difference noise floor, threshold 1e-9).
```

## 3. Homogeneous constant shift with all factors, signs, units (S2)

On FLRW (`Y ≡ 0`, `Q ≡ Q0`), the constant part of the minisuperspace Lagrangian density is

```
L_const = a³ [ −2 Λ − α J(0) − K(Q0) ]  / (16πG).
```

Matching this to the single effective cosmological term `a³ (−2 Λ_eff)/(16πG)`:

```
Λ_eff = Λ + (α/2) J(0) + (1/2) K(Q0)  =  Λ + (2−K_B) J(0)/2 + K(Q0)/2.        (S2)
```

Signs: all three bare terms are negative in the corpus's convention (R − 2Λ − αJ − K); the effective
combination is their half-sum. Units: in c = 1, J(0), K(Q0), Λ all have L⁻²; in SI the J(0) term is
acceleration-squared/c⁴ (m⁻²) and the resulting mass density is `ρ_vac = α J(0)/(16πG c²)` kg/m³.

Under `J → J + λC` the shift is exactly linear:

```
ΔΛ_eff = λ α C / 2.                                                       (S2′)
```

The map `(Λ, J(0), K(Q0)) ↦ Λ_eff` has Jacobian `(1, α/2, 1/2)` — rank 1 (SVD: single singular value
`1.4197`), i.e. **two independent null directions** `(δΛ = −α δJ₀/2)` and `(δΛ = −δK₀/2)`: the local
action carries a two-dimensional vacuum zero-mode degeneracy that collapses onto the single observable
`Λ_eff`. (The k01 K2 formula is reproduced exactly; this extends it with the rank statement.)

## 4. Exact gauge symmetry of the compensated pair (S3)

Apply the pair `J → J + λC` together with `Λ → Λ − λ α C / 2`. The change of the action density is

```
Δ(√-g · L_den) = √-g [ −2 ΔΛ − α ΔJ ] = √-g [ −2(−λαC/2) − α(λC) ] = 0   pointwise, identically.
```

So the compensated pair is an **exact symmetry of the full action** (not a limiting statement): every
observable — static force law, Friedmann evolution, everything derived from S — is unchanged while the
primitive's zero `J(0)` changes. Numeric check on nontrivial profiles (λ = 1/2, 1, 2; C = 0.37, 1.19):
`max |density_comp − density_base| = 2.2e-16 … 7.8e-16`.

**Consequence (S5).** Since `(Λ, J(0), K(Q0))` enter physics only through `Λ_eff`, the equations of the
action contain no relation between the vacuum density (`ρ_L ∝ Λ_eff`-sector) and the MOND scale `s`:
the ratio `κ = a0/s` is *not* fixed by any equation of this action class. `κ = 1/2` is exactly the
adopted input the framework contract declares. This is the corpus's k01 "outcome 3" (arbitrary additive
constant ⇒ no derivation possible), re-derived with coefficients retained and with the rank statement.

## 5. Tightness (S4) and the deep/Newtonian limits

**Tightness — the claim is not overbroad.** A *nonconstant* shift `J → J + λC·w(Y)`, `w(Y) = Y/(1+Y)`,
changes the equations (sympy residual for EL_φ):

```
EL(J + λCw) − EL(J) = 2Cαλ (3φ′² − 1) φ″ / (1 + φ′²)³  ≠ 0.
```

Symbolic residual nonzero; at the observable level this same perturbation changes the rotation
acceleration `g(r)` by 9.5% (λ=1/2), 18% (λ=1), 33% (λ=2) for n = 2 (8–28% for n = 3) — the probe is
capable of failing and does fail for nonconstant w. The invariant subspace of the shift is **exactly**
the constants: the additive vacuum zero mode is the whole story, and no field-dependent renormalization
masquerades as one.

**Limits (seed control).** Deep-MOND and Newtonian limits of the MU_n family (symbolic n ≥ 1, instances
n = 1..6):

```
μ_n(Y) = 1 − (1+Y)^(−n):   μ_n′(0) = n   (deep slope = the channel count),   μ_n(∞) = 1.
```

Both limits constrain only J′ (through μ) — never J(0): the zero mode survives both regimes. The
L230 chain closes for general n: deep matching `μ ≈ n g/s` with `μ g = g_N` gives `g² = (s/n) g_N`,
i.e. the a0-line with `a0 = s/n`, `κ_n = 1/n` (symbolic). Canonical footing: n = 2 ⇒ κ = 1/2 exactly
(`s = 2 a0_can = 1.872380e-10 m/s²`, `ρ_L = 5.844412e-27 kg/m³`). Alternative footing, stated under
both readings:
- fixed `ρ_L`: `κ_eff = a0_alt/s = 0.602388` ⇒ `n_eff = 1.660059` — **not a channel count** (mirrors
  PD01's structural exclusion of non-integer counts; not a prediction, an identification constraint);
- fixed κ = 1/2: `ρ_L′ = (2 a0_alt)²/(G c²) = 8.483090e-27 kg/m³` (= 1.4515 ρ_L), n = 2 unchanged.

A dimensionless theorem (S1–S4, S6-sign) is proved once and applies to both footings because the
zero-mode statements never invoke the numerical value of a0 (only its role as a scale in Y = g/s).

## 6. Repair audits (S6): can anything inside the action fix J(0)?

**(a) "Empty Newtonian vacuum" fixing — sign.** Fixing the primitive's zero by demanding `J = 0` at the
saturated/Newtonian end gives, for the MU_n family in the corpus's Δ-convention (`J(0) = −I_n a0²`,
`I_n(z_t) = 2 ∫_0^{z_t} z μ_n(z) dz`, closed forms for n = 1..6 computed symbolically):

```
μ_n > 0 on (0,∞)  ⟹  I_n > 0  ⟹  J(0) < 0  ⟹  ρ_vac = α J(0)/(16πG c²) < 0   for EVERY n ≥ 1 and
EVERY truncation z_t.  The sign is mathematically forced (primitive strictly increasing ⇒ descends
toward Y = 0); the "Lambda-free repair" fails on sign for the whole MU_n family, n-independent
(k01 K3 established this for the nu_RAR and exponential carriers).
```

**(b) Untruncated family — ill-posed fixing.** The MU_n family does **not** saturate (μ_n → 1 only at
Y → ∞), so the k01-style span `I_n(Z)` diverges like `Z²` for every n (numeric log-log slopes = 2.000
for n = 1..4 over Z = 10³..10⁶; `I_n(Z) = Z² + O(ln Z or const)`). The empty-Newtonian fixing is
therefore undefined without an arbitrary truncation — a *functional* freedom, part of the audit itself.

**(c) Size at an explicit truncation (μ = 0.99).** `|ρ_vac|/ρ_L = α I_n κ²/(16π)` with the truncation's
I_n, across n = 2..6 × K_B ∈ {0, 1/4} × both footings:

```
n = 2:  0.681 .. 1.129 ;   n = 3:  0.110 .. 0.183 ;   n = 4:  0.039 .. 0.064 ;
n = 5:  0.019 .. 0.031 ;   n = 6:  0.011 .. 0.018   (min 0.0109, max 1.1290).
```

SIGN is convention-independent (a); SIZE sweeps two orders of magnitude with n/κ²/truncation — it
carries no fixed meaning until a principle fixes the primitive's zero. (k01's K4 numbers, ratio ≈
0.01–0.03, belong to the *saturated* nu_RAR/exp carriers with their own I; the MU_n-family numbers here
are not in conflict with them — different kernels, same audit conclusion.)

## 7. Negative control (seed-mandated, capable of failing) — passed

**Control 1 (statics).** The observable rotation acceleration `g(r)` from `μ_n(g/s)·g = g_N(r)` for a
Hernquist baryon model (M = 10¹¹ M_sun, a_h = 3 kpc, r ∈ [0.1, 100] kpc, 200 log-spaced radii, 300-step
bisection) is exactly unchanged under `J → J + λC` (the equation itself is unchanged); the substituted
residual `max |μ(g)g − g_N|/g_N = 3.2e-15` (n = 2), 3.0e-15 (n = 3). The same observable changes by
9–33% under the nonconstant probe (§5) — the control discriminates.

**Control 2 (background).** Fixing Λ to compensate C — `Λ → Λ − λ α C/2` — restores identical
Friedmann evolution by the exact identity of §4 (compensated density residual 2.2e-16..7.8e-16).
Leaving the shift **uncompensated** changes `ρ_Λ` by `λ α C/(16πG c² ρ_L)` = **0.44% (λ = 1/2, K_B =
1/4) up to 1.99% (λ = 2, K_B = 0)** (ΔH/H = 0.22–0.99% at Ω_Λ = 1): the shift *is* observable unless Λ
is adjusted — the control is genuinely capable of failing and the numbers show it must be applied. This
is the seed's test in executable form: "fix Lambda to compensate C and show unchanged observables
despite a changed primitive zero" — PASS.

## 8. Verdict and closure implication

**Strongest surviving statement.** Within the corpus's local action class (A1–A4), the additive vacuum
zero mode is an **exact gauge degeneracy**: `(J, Λ, K) ↦ (J + λC, Λ − λαC/2, K)` is an exact symmetry;
statics see only J′; the background sees only `Λ_eff = Λ + αJ(0)/2 + K(Q0)/2` (rank-1, two null
directions, linear in λ); the invariant subspace is exactly the constants; and both natural repairs
(empty-Newtonian-vacuum fixing: wrong sign for every n; untruncated fixing: divergent; any size:
truncation-dependent) fail. Hence **no equation of the action derives κ = a0/s**: the half is an
adopted boundary condition (as the framework contract states), and the derive-arm of gate 13
(cosmological acceleration-scale relation) is closed within this action class — a scoped negative
result for the derivation route, not a falsification of the framework (the preserve-arm, κ = 1/2
input, is untouched and consistent).

**What this does NOT establish.** No statement about Q/RAR/EXP/MONO kernels beyond their participation
in the generic-J theorem; no claim about the full thirteen items (criterion B, DOF counts, PPN,
stability, lensing — untouched); no empirical test of the framework; the alternative-footing n_eff =
1.6601 statement is an identification constraint (non-channel-count), not a fit.

## 9. First missing bridge (next unresolved implication)

To convert κ = 1/2 from adopted input to derived, a principle must fix the primitive's zero `J(0)`
**absolutely** (removing the two-dimensional (J(0), K(Q0)) degeneracy with Λ) with the correct sign
(ρ_vac > 0) and magnitude (|ρ_vac|/ρ_L = O(1) at the canonical footing) — i.e., a structure outside
the local action's √-g·J(Y) coupling: a global/sequestering constraint (k02-type: corpus records a
miss by ~10⁵), a nonlocal completion, or a sign-flipping kinetic structure. The specific quantified
target: **find any extension of S (A1-class) such that (i) Λ_eff = Λ + αJ(0)/2 + K(Q0)/2 ceases to be
the only invariant, (ii) the new equation fixes J(0) = −κ²I a0² with κ = 1/2 and the positive-sign
requirement, while (iii) S1–S4 survive; or prove a no-go for the class.**

## 10. Reproducibility

Script `as067_audit.py` (sympy + numpy only), launcher `run_bounded.py`, raw stdout `as067_audit.out`,
`as067_observables.npz`, `as067_results.json` (16/16 checks PASS). Bounds: RLIMIT_CPU 120 s (enforced),
threads = 1 (enforced via env), RLIMIT_AS 512 MB (kernel-refused on this macOS host — recorded;
measured max RSS 97.3 MB, wall 1.58 s incl. interpreter start; script-internal wall 1.366 s).
Lean certificate: `AS067_zero_mode.lean` (see §11), compiled in `fable_independent_2026/lean_2026`
(compile-host only; no files written there).