# AS263 — Derive the time-dependent projector commutator [∂_τ, P_h]Z

- **Run:** `AS263-r1-20260928T232432Z-dsv4f-hermes`
- **Task sha256:** `50c6c923d292f191f7230db687f25eeb0929bfce9bedef3384904df4416f7b09` (verified at start)
- **Branch/action/gate:** CA5-GNC-R homogeneous candidate; operative target filtered `nu_mono`, causality criterion B (FINAL_ACTION.md pinned `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`, occupied/RESULT.md pinned `6091291f05fca5f1f4fdcc216f305bd31a476a7ea3d16c09131faca1158975d5`, transport/HOMOGENEOUS_FRW.md pinned `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d` — all match SOURCE_MANIFEST.json). Q, RAR, MU2, EXP are comparison branches only; nothing is transferred.
- **Framework cell:** `a0 = κ c √(G ρ_Λ)`, **κ = 1/2 ADOPTED** (mandated input). `r_M = √(G M_b/a0)`, deep `v_flat⁴ = G M_b a0`. Both footings computed **separately** (they cannot share fixed ρ_Λ and fixed κ): canonical `a0 = 9.3619e-11 m/s²`, alternative `a0 = 1.1279e-10 m/s²`. `G_N`, `G_bare`, `G_cosmo` kept separate: no coupling equality is set anywhere in this derivation (the identity is kinematic; only foliation data N, K, n, h enter).

---

## 0. The object to derive and the premises it starts from

**Adopted convention and definitions (all from the pinned action, FINAL_ACTION.md §1/§3 and occupied/RESULT.md):**

- Compact closed spacelike leaves `Σ_τ`, induced metric `h`, future unit normal `n`, lapse `N`, `X_τ = −g^{μν}τ_μτ_ν > 0`, `n_μ = −τ_μ/√X_τ`, `N = X_τ^{−1/2}`.
- **Varied intrinsic (volume) mean — NOT lapse-weighted:**

  ```
  ⟨A⟩_h = (∫_Σ √h A) / (∫_Σ √h).                                    (D1)
  ```

- **Mean-zero projector** (the operator denoted `P_h` in occupied/RESULT.md: "`∫√h P_h Z = 0`"):

  ```
  z = P_h Z := Z − ⟨Z⟩_h,     ⟨P_h Z⟩_h = 0,   P_h² = P_h.           (D2)
  ```

- **Normal convention (adopted):** the foliation time derivative is along the future unit normal flow with zero shift,

  ```
  ∂_τ = N n,      i.e.  N n(Z) = ∂_τ Z  for every leaf field Z.       (D3)
  ```

- **Volume-element transport** (standard identity for a leaf moving along `N n`; sign audited below):

  ```
  ∂_τ √h = N K √h,   K := h^{ij} K_{ij},  K_{ij} = h_i^ρ h_j^σ ∇_ρ n_σ .  (D4)
  ```

  Sign/consistency check: for `N = 1`, `h = a²δ` in 2D, `√h = a²`, `K = 2 ȧ/a`, so `∂_τ√h = 2aȧ = N K √h` ✓ (3D FRW: `√h = a³`, `K = 3H`). In the task's homogeneous sector `N = 1`, `K = 3H(τ)` leaf-constant.

The task's displayed object: **compute `[∂_τ, P_h] Z` from `d⟨Z⟩_h/dτ = ⟨N(nZ + Kz)⟩_h`, `z = P_h Z`, under the normal convention** — i.e. derive the commutator of the leaf-time derivative with the moving-geometry mean-zero projector, and identify the term a time-stepping auxiliary solver must include to preserve zero mean.

---

## 1. Step 1 — the mean-derivative identity by differentiating numerator and denominator

Write the mean as a quotient `⟨Z⟩_h = I₁/I₀` with

```
I₁ = ∫_Σ √h Z,    I₀ = ∫_Σ √h .
```

**Reynolds transport on the foliation** (normal convention D3, volume data D4): for any smooth `f`,

```
d/dτ ∫_Σ √h f  =  ∫_Σ [∂_τ f + N K f] √h .                         (D5)
```

`∂_τ f = N n(f)` by (D3); the `+NKf` term is the time derivative of the moving volume element (D4), sign as audited there. Then:

```
dI₁/dτ = ∫ [N n(Z) + N K Z] √h,       dI₀/dτ = ∫ N K √h .
```

**Quotient rule (every factor and sign shown):**

```
d⟨Z⟩_h/dτ = (dI₁/dτ · I₀ − I₁ · dI₀/dτ) / I₀²
          = ⟨N n(Z)⟩_h + ⟨N K Z⟩_h − ⟨Z⟩_h ⟨N K⟩_h
          = ⟨N n(Z)⟩_h + ⟨N K (Z − ⟨Z⟩_h)⟩_h                      (centering; ⟨Z⟩_h leaf-constant)
          = ⟨ N ( n(Z) + K P_h Z ) ⟩_h .
```

**Result (E1) — exactly the task's starting identity, now derived:**

```
d⟨Z⟩_h/dτ = ⟨ N ( n Z + K z ) ⟩_h ,     z = P_h Z .                (E1)
```

Every coefficient: the `+1` on `N K Z` (volume-element growth at expansion, D4), the `−⟨Z⟩⟨NK⟩` (quotient rule denominator derivative), the centering step (uses `⟨Z⟩_h` constant on the compact leaf), the normal-convention identification `N n(Z) = ∂_τZ`. Units: `[⟨Z⟩/τ] = [Z]/s · 1` — checked: `N` dimensionless, `n(Z)` = `[Z]/s`, `K z` = `[Z]/s` ✓.

---

## 2. Step 2 — the commutator in covariance form; terms surviving beyond homogeneity

By definition of the commutator on leaf fields,

```
[∂_τ, P_h] Z := ∂_τ(P_h Z) − P_h(∂_τ Z) .
```

The projector depends on time through the moving leaf `h(τ)` (through the mean `⟨·⟩_h`), so both terms must be computed with the time-dependent mean:

```
∂_τ(P_h Z) = ∂_τ Z − d⟨Z⟩_h/dτ
           = ∂_τ Z − [⟨N n(Z)⟩_h + ⟨N K z⟩_h]            (E1)
           = P_h(∂_τ Z) − ⟨N K z⟩_h · 1 ,

P_h(∂_τ Z) = ∂_τ Z − ⟨∂_τ Z⟩_h = ∂_τ Z − ⟨N n(Z)⟩_h  .
```

Subtracting:

```
[∂_τ, P_h] Z = − ⟨ N K z ⟩_h · 1                              (C1)
             = − [ ⟨N K Z⟩_h − ⟨N K⟩_h ⟨Z⟩_h ] · 1
             = − Cov_h(N K, Z) · 1 ,
```

where `Cov_h(NK,Z) := ⟨NKZ⟩_h − ⟨NK⟩_h⟨Z⟩_h` is the (uncentered) covariance with respect to the volume mean. **The commutator is a leaf-constant function** whose value is minus the weighted covariance of the lapse-weighted expansion `NK` with the field `Z`.

**Isolated terms surviving beyond exact homogeneity.** In the homogeneous sector `N = 1`, `K = 3H(τ)` (leaf-constant) so `⟨NKz⟩_h = 3H ⟨z⟩_h = 0` — the commutator vanishes for **every** field `Z` (not only constants). For one small inhomogeneous lapse/expansion perturbation `δN`, `δK` on the torus (`N = 1+δN`, `K = 3H+δK`):

```
Cov_h(NK, Z) = 3H · Cov_h(δN, Z) + Cov_h(δK, Z) + Cov_h(δN δK, Z) .   (D6)
```

All terms vanish in exact homogeneity; the surviving terms are exactly the covariances of the perturbed lapse and expansion against the field — first order: `[∂_τ,P_h]Z ≈ −[3H Cov_h(δN,Z) + Cov_h(δK,Z)]`.

**Controls on the identity (capable of failing):**

- *Control 1 (constant test field):* `Z = c` on the leaf ⇒ `z = 0`, `Cov = 0`, and `P_h c = 0` identically ⇒ commutator `= 0` exactly. Verified symbolically and numerically (C4, residual ≤ 4.4e-11).
- *Exact homogeneity:* verified for mean-zero **and** mean-nonzero fields (C5, residuals ≤ 1.7e-10, closed form ≤ 1.8e-15).
- *Negative control (perturbed leaf):* direct finite-difference commutation `∂_τ(P_hZ) − P_h(∂_τZ)` on the perturbed torus, compared with `−⟨NKz⟩_h` — the naive "frozen projection" claim (commutator = 0) fails with residual `2.010e-5 = |⟨NKz⟩_h|` (the observable obstruction), while the formula residual is `1.7e-8 → 1.8e-10 → 7.1e-11` as ε: 1e-3 → 1e-4 → 1e-5 — genuine FD convergence, control capable of failing and discriminating (C6).

---

## 3. Step 3 — the term a time-stepping auxiliary solver must include

For the centered variable `z`, the **projector equation** implied by (C1) is

```
∂_τ z = P_h(∂_τ Z) − ⟨ N K z ⟩_h · 1 .                            (D7)
```

A solver advancing the centered sector by the *frozen-projection* update `∂_τ z = P_h(∂_τ Z)` drifts the mean:

```
d⟨z⟩_h/dτ = ⟨∂_τ z⟩_h + ⟨N K z⟩_h = ⟨N K z⟩_h ≠ 0   (perturbed leaf).
```

The missing term is exactly **`−⟨NKz⟩_h`, the commutator remainder `[∂_τ,P_h]Z` itself**: with (D7),

```
d⟨z⟩_h/dτ = ⟨P_h(∂_τZ)⟩_h − ⟨NKz⟩_h + ⟨NKz⟩_h = 0   identically.
```

**Deliverable of step 3:** the time-stepping auxiliary solver must append the leaf-constant covariance term `−⟨NKz⟩_h` (= `−Cov_h(NK,Z)`) to its centered-variable update to preserve zero mean on a moving leaf; equivalently it must evolve `⟨Z⟩_h` by (E1) and update `z = Z − ⟨Z⟩_h` rather than freezing the projection. Demonstrated numerically (C8): 200-step explicit Euler on the perturbed torus — naive update loses the mean to `⟨z⟩ = −1.056e-5`, matching the accumulated drift `−∫⟨NKz⟩dτ = −1.062e-5` to 0.5% (Euler accuracy), while the corrected update keeps `|⟨z⟩| ≤ 6.0e-8` (residual of order `dτ·|⟨NKz⟩| ≈ 4e-8`, the Euler cross-leaf reweighting; exactly zero in the continuum).

---

## 4. Step 4 — the relation, its assumptions, and the downstream calculation

**Requested relation (C1), all assumptions explicit:**

> On a smooth family of compact closed leaves `(Σ_τ, h_τ)` of the CA5-GNC-R homogeneous-candidate foliation with lapse `N > 0`, future unit normal `n` (normal convention `∂_τ = N n`, zero shift), expansion trace `K`, and the varied intrinsic mean (D1):
> `[∂_τ, P_h] Z = −⟨N K (Z − ⟨Z⟩_h)⟩_h = −Cov_h(NK, Z)` — a leaf-constant function.
> Assumptions used: (A1) compact closed leaves, no boundary terms; (A2) `N > 0`; (A3) normal convention (D3); (A4) volume-element identity (D4) — standard hypersurface geometry under the action's own convention `K_{ij} = h∇n` with the future normal; (A5) `C²`-regular fields (C¹ suffices for the identity); (A6) mean not lapse-weighted (D1), per the action's explicit definition; (A7) `κ = 1/2`, `a0` both footings — adopted inputs, **not** derived here (the identity itself contains no `a0`; the footings enter only through the background `K = 3H(τ)` of the homogeneous branch).

**Downstream calculation enabled/blocked:** (C1) supplies the missing ingredient for moving-geometry transport of the **projected constraint source** of the action, eq. (7) of FINAL_ACTION.md: `2M_P² c_N div_N(DZ−a+DU) + ρ_d − ⟨N ρ_d⟩_h/N = 0`, whose source has *exactly zero `N√h` integral*. That zero-mean character must be preserved under evolution; (C1) now gives the projection drift term, enabling the concrete calculation `∂_τ[ρ_d − ⟨N ρ_d⟩_h/N]` along the coupled evolution and a mean-fidelity check for the centered auxiliary sector. Without (C1) that τ-propagation is simply undefined (frozen-projection error `⟨NKz⟩ ≠ 0` accumulates). Gate affected: **CA5-GNC-R coupled-evolution / constraint preservation** (one of the open gates of the amended thirteen-item target). This is a scoped ingredient, **not** gravity closure: `closure_candidate = null`.

---

## 5. Numerics: bounded prototype, controls, actual residuals

Prototype: 3-torus `T³`, 24³ grid (13 824 points), fully analytic leaf data,
`H₀ = 0.70`, evaluation `τ₀ = 0.37`, band-limited perturbations:
`δN ~ 0.02 cos(3x₁−x₂)sin(2x₃)+0.01 sin(4x₁+x₃)`,
`δK ~ 0.10 cos(2x₁)cos(x₂)sin(x₃)+0.05 sin(5x₂−x₁)`,
`√h(0) = 1 + 0.03 cos(2x₁+3x₂)sin(x₃)`,
`Z(τ,x) = cos(2x₁+0.3τ) + 0.4 sin(3x₂−0.1τ) cos(x₃+0.2τ) + 0.2 cos τ cos(4x₁−2x₃)`,
with the exact transport solution `√h(τ) = √h(0) e^{NKτ}` (`∂_τ√h = NK√h` to machine precision, C0: rel. 9.1e-11).

| check | statement | observed | pass |
|---|---|---|---|
| C0 | volume transport `∂_τ√h = NK√h` (FD vs exact) | 9.1e-11 rel (pert) | ✓ |
| C1 | identity (E1): FD of `⟨Z⟩` vs `<N(nZ+Kz)>` | 2.3e-11 / 2.1e-14 / 4.2e-12 (ε = 1e-3/1e-4/1e-5; roundoff floor ∝ 1/ε) | ✓ |
| C2 | quotient rule `(I₁′I₀−I₁I₀′)/I₀²` vs (E1) RHS | 4.24e-12 | ✓ |
| C3 | (C1): FD commutator vs `−⟨NKz⟩` | 1.74e-8 → 1.76e-10 → 7.1e-11 (linear, roundoff floor) | ✓ |
| C3b | commutator is leaf-constant (pert) | std/|value| = 4.5e-4 (FD noise) | ✓ |
| C3c | `⟨NKz⟩ = Cov(NK,Z)` algebra | 3.7e-17 | ✓ |
| C4 | **control 1:** `Z ≡ 7.3` ⇒ commutator 0 | ≤ 4.4e-11 (hom), 0.0 (pert) | ✓ |
| C5 | exact homogeneity (mean-zero AND mean-nonzero `Z`) | ≤ 1.7e-10 FD; closed form ≤ 1.8e-15 | ✓ |
| C6 | **negative control:** naive frozen-commutation residual | naive: 2.010e-5 = `|⟨NKz⟩|` (fails, as required); formula: 1.7e-8 → 7.1e-11 (passes) | ✓ |
| C7 | covariance decomposition (D6) | 1.1e-17 | ✓ |
| C8 | aux-solver mean preservation (200 Euler steps, dτ=2e-3) | corrected `|⟨z⟩| ≤ 6.0e-8`; naive drift −1.056e-5 ≈ ∫drift −1.062e-5 | ✓ |
| S1 | **symbolic (sympy, exact trig integration on the circle at τ=0):** (E1) residual | exactly `0` | ✓ |
| S2 | **symbolic:** (C1) residual | exactly `0`; closed form `⟨NKz⟩ = 9HeN/20 + 3eKeN/800 + 799eK/1600` | ✓ |

The negative control is genuinely capable of failing and discriminates: the naive zero-commutator claim errs by `2.010e-5` (the full obstruction `|⟨NKz⟩|`), while (C1) matches to `7.1e-11`; a sign error in (D4)/(E1) would have made the residuals O(1). Refinement: residuals scale linearly with the FD step and hit the double-precision `1/ε` floor, as expected for exact identities.

**Bounded execution (actually enforced):** wall `≤ 120 s` — `ulimit -t 118` (CPU) + in-script `signal.alarm(118)`; actual 2.27 s. Memory `≤ 512 MB` — **declared and enforced by RSS telemetry**: macOS refuses `RLIMIT_AS` (`setrlimit(RLIMIT_AS)` → "maximum limit 1", `ulimit -v` → "cannot modify limit"), so the cap is enforced by `/usr/bin/time -l` peak-footprint + in-process `getrusage` self-check; actual peak 107 152 104 B = **102.2 MiB**. Threads `1` — `OMP/OPENBLAS/MKL/VECLIB/NUMEXPR_NUM_THREADS=1`, single process.

---

## 6. Framework footings — both applied separately

| footing | a0 (m/s²) | ρ_Λ = 4a0²/(Gc²) (kg/m³) | κ_eff at fixed canonical ρ_Λ | r_M(10¹¹ M_⊙) (m) |
|---|---|---|---|---|
| canonical | 9.3619e-11 | 5.8444e-27 | (reference κ = 1/2) | 3.7651e20 |
| alternative | 1.1279e-10 | 8.4831e-27 | 0.6024 (= 1.2048 × κ) | 3.4303e20 |

The two footings do **not** share fixed ρ_Λ and fixed κ: at fixed canonical density the alternative a0 forces `κ_eff = 0.6024` (a factor `a0_alt/a0_can = 1.2048` on the adopted κ = 1/2); at fixed κ = 1/2 the density changes to 8.4831e-27 kg/m³. Constants mandated: `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI); `G_N/G_bare/G_cosmo` separate — no equality set. **Dimensionless-application clause (contract):** (C1) is a purely geometric/kinematic identity — it contains `N, K, n, h` only — so it is footing-independent and applies identically under both footings; the footings enter the physics only through the branch background expansion `K = 3H(τ)` (via `G_cosmo` in the branch's Friedmann equation, which is a separate symbol and not set equal to `G_N` or `G_bare` here).

---

## 7. Lean certificate

`AS263_projector_commutator.lean` (in this run dir) certifies the finite-mode algebraic/differential core of (E1) and (C1): weighted-volume mean `Avg`, mean-zero projector `Proj`, transport `w_i′ = c_i w_i` (`c = NK` sampled on the grid):

1. `covariance_centering` — `⟨c(z−⟨z⟩)⟩ = ⟨cz⟩ − ⟨z⟩⟨c⟩`;
2. `mean_deriv_value` — quotient-rule value identity;
3. `mean_deriv_quotient` — `d/dt⟨z⟩_h = ⟨dz/dt⟩ + ⟨cz⟩ − ⟨z⟩⟨c⟩` (via `HasDerivAt.sum/mul/div` on `Finset.univ.sum`, real calculus);
4. `projector_commutator` — **the commutator: `d/dt(Proj z)_i = (dz_i − ⟨dz⟩) − ⟨c(z−⟨z⟩)⟩`**;
5. `constant_field_commutator` — control 1: constant field ⇒ 0;
6. `homogeneous_sector` — `c` constant and `⟨z⟩ = 0` ⇒ `d/dt(Proj z) = P(dz)` (commutator vanishes in exact homogeneity).

Compiled: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS263_projector_commutator.lean` — **exit 0**, zero `sorry`; `#print axioms` for all six theorems = `{propext, Classical.choice, Quot.sound}` (hard bar met). Build quirks worked around (recorded for the campaign): this build's `∑` binder elaborator rejects annotated binders — all sums written as explicit `Finset.univ.sum (fun i : Fin n => ...)`; `HasDerivAt.sum` returns sum-of-functions requiring the `Finset.sum_apply` reshape; `convert` on `HasDerivAt` generates instance goals, avoided via `rw` of function-identity lemmas.

---

## 8. Files in this run dir

- `compute_as263.py` — bounded prototype (bounds enforced in-run; exit 0).
- `raw_output.json` — full output of the final bounded run; `raw_output.stderr` — `/usr/bin/time -l` record (peak memory footprint 107152104 B).
- `AS263_projector_commutator.lean` — Lean 4 certificate; `lean_compile.out` — compile + axiom audit (exit 0, axioms {propext, Classical.choice, Quot.sound}).
- `derivation.md`, `result.json` — this report and the schema-v2 record.
- `probe*.lean` — development probes preserved (see `failed_attempts` in result.json).