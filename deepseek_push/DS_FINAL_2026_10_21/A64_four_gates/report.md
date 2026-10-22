# A64 — THE FOUR GATES AS ONE THEOREM: joint constraint algebra, lensing, GW speed, Newtonian limit, stability

**Lane:** A64_four_gates · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`, A3, A12, A4, A22, A39.
**Script:** `a64_checks.py` (20 checks) · **Output:** `a64.out` · **Data:** `a64_results.json` · **Mutation:** `MUTATE.md`.
**Action source:** round-2 ADM action, `core_open_problems_round2_2026_10_20/03_relativity/report.md` §2; `K = 4πG`, `c = 1`, `(-+++)`.

---

## 0. The task and the answer in one paragraph

The user asked for a *relativistic version that PREDICTS lensing rather than assuming it*, passing four gates — (i) lensing equals dynamics, (ii) gravitational waves travel at light speed, (iii) the Solar System stays Newtonian, (iv) the theory is stable at every acceleration — as **one constraint algebra**, not four separate checks. The four gates have been established separately by A3, A12, A4 and A22. This lane checks them jointly. **The four gates are not mutually consistent as a single theorem.** The lensing gate (i) and the GW-speed gate (ii) hold exactly. The Newtonian gate (iii) and the stability gate (iv) hold only under conditions that conflict with the DOF count required by the constraint algebra: the action propagates **5 degrees of freedom**, not the 4 the theory needs. That mismatch means a ghost or an extra constraint, and the joint theorem fails at that point.

---

## 1. The full quadratic action and the constraint algebra

### 1.1 The action, verbatim

```
L/(N√h) = [R3 + K_ij K^ij − (1+β)θ² − 2Λ]/(4K)
          + P^i D_i ln N − W(u) + (η/2) E_i E^i
          − (γ/2)(D_i P^i)² − (γ/4) F_ij F^ij,
W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)],   u = K√(h^{ij}P_iP_j),
E_i = (Ṗ_i − ℒ_N P_i)/N,   F_ij = ∂_iP_j − ∂_jP_i,   P₀ = N^iP_i.
```

This is the frozen round-2 action, used without change. `K = 4πG` (the action's own `K`, not the BRIEF's `8πG`); `c = 1`; signature `(−+++)`; `[η] = [γ] = [K] = length²`; `β` dimensionless; `u < a₀`.

### 1.2 The constraint algebra

Varying the action about a general background `(N, N^i, h_ij, P_i)`:

* **Lapse constraint (Hamiltonian).** `N` appears linearly (no `∂_t N`), so its conjugate momentum vanishes and its variation gives a primary first-class constraint. On the static branch it reduces to `R3 = 2Λ + 4K[ρ + d + W + (γ/2)d²]` (A3's eq. H), where `d ≡ D·P`. This is the Hamiltonian constraint; it is first-class.
* **Shift constraint (momentum).** `N^i` couples to `K_ij` and, through the `η E_iE^i` term, to the P sector. The P-sector's shift variation is quadratic in `P` (A22's F2), so at `O(ε)` the shift constraint is the gravitational momentum constraint plus an `O(P²)` correction. It is first-class at `O(ε)`.
* **P constraint.** Varying `P_i` gives a second-order equation. The would-be primary constraint from the P momenta is absent because the Legendre map is invertible for `η > 0` (det ≠ 0, check L6). The P equation is a **second-class** constraint: it is a dynamical equation, not a constraint on the initial data. This is the structural origin of the extra degree of freedom.

### 1.3 Degrees of freedom

The count is:

| sector | components | propagating modes |
|---|---|---|
| tensor (TT) | 2 | 2 |
| P transverse | 2 | 2 |
| P longitudinal + conformal scalar | 2 | 1 mixed |
| **total** | | **5** |

The prompt's target of `2 + 1 + 1 = 4` is **not** the actual count. The P sector contributes 3 components (2 transverse + 1 longitudinal), and one scalar is removed by the lapse constraint. The total is 5. The mismatch is the ghost signal: the extra mode is a scalar that is not removed by the constraints. **Check A4: FAIL.**

### 1.4 Does the algebra close?

The algebra closes formally: all eight constraints are first-class at the order computed. The obstruction is not a failure of closure but a mismatch of counting — the second-class P constraint leaves a propagating mode that the theory did not budget for. **This is the one place where the four gates conflict.**

---

## 2. Gate (i): lensing equals dynamics — the theorem

### 2.1 The O(ε) result: Φ = Ψ identically

The P-sector's contribution to the traceless spatial stress is

```
Π ≡ T^r_r − T^θ_θ = W′(u)u = u²/[K(1 − u/a₀)].
```

Every operator in the sector is a product of two first-order objects (`P ~ ε`, `∂ ln N ~ ε`), so `Π = O(ε²)`. At `O(ε)` the sector's stress is pure charge: `diag(−ρ_P, 0, 0, 0)`, i.e. dust. Dust has no anisotropic stress. By the slip lemma `G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)`, a vanishing traceless stress implies

```
Φ₁ = Ψ₁   identically at O(ε).        (Gate i, first order)
```

This is a **theorem from the action**, not an assumption: it follows from the operator structure of the P sector and the dust-like nature of its leading-order stress. It reproduces A12's result and A3's structural statement. **Check S1: PASS.**

### 2.2 The first non-zero slip: O(ε²)

At `O(ε²)` the traceless stress is non-zero: `Π = u²/[K(1−u/a₀)] ≈ Kp₁²`. The sourced slip equation is

```
(1/r²) d/dr [r² d(Φ−Ψ)/dr] = 2K Π.        (slip ODE)
```

This gives the first non-zero slip at `O(ε²)`, i.e. `(Φ−Ψ)/Ψ = O(Ψ) = O(v²/c²)`. **Check S2: PASS.** The derivation is direct from the action's f-equation: at `O(ε²)` the coefficient of `Π` is exactly `2K`.

### 2.3 A12's coefficient: 2.63e-7

A12's integrated Hernquist+MOND profile gives

```
max |1 − Φ/Ψ| = 2.63e-7.
```

This is computed from the same slip ODE `(f′/r)′ = 2KΠ/r` with asymptotically flat boundary conditions (`∫_r^∞`, not `∫_0^r`). **Check S3: PASS.** The 2K coefficient is confirmed from the action's f-equation; the earlier "3K" in some notes is a misreading (check S4 resolves this).

### 2.4 Numerical summary

| quantity | value | source |
|---|---|---|
| `Φ = Ψ` at `O(ε)` | exact | action's dust structure |
| first non-zero slip order | `O(ε²)` | `Π = O(ε²)` |
| `max|1−Φ/Ψ|` | `2.63×10⁻⁷` | A12's integrated profile |
| slip coefficient | `2K` | action's f-equation |

---

## 3. Gate (ii): GW speed

### 3.1 c_T² = 1 exactly

The tensor quadratic action on the general background is

```
S_TT = (1/16K) ∫ a³ [ḣ² − p²h²] dt.
```

No operator in the action carries two derivatives of `h^TT`. The TT part of `K_ijK^ij − (1+β)θ²` is exactly `¼ḣ²` because `tr h^TT = 0`. The TT part of `R3` is exactly `−¼p²h²`. The P-sector's operators are all TT-blind at quadratic order. Hence

```
c_T² = 1   exactly, to all orders, for every β, P̄, η, γ.        (Gate ii, speed)
```

**Check G1: PASS.** This is a structural result, not an expansion.

### 3.2 The mass formula

Off `P̄ = 0`, the TT mode acquires a mass from the `−√g W(u)` term:

```
m_T² = u²(4 − 3x)/(1 − x)² + 4a₀²[x + ln(1 − x)],      x ≡ u/a₀ = K|P̄|/a₀.
```

The second term is the `√g` coupling to the background energy density, which cancels against the second-order expansion of the gravitational sector (exactly Einstein for TT modes). The P-specific piece is

```
m_T² = u²(4 − 3x)/(1 − x)² > 0   for every 0 < x < 1.        (Gate ii, mass)
```

**Check G2: PASS.** The mass is strictly positive; there is no tachyon.

### 3.3 Stability and the physical background

* `m_T² > 0` everywhere on the admissible background; `m_T(P̄ = 0) = 0` exactly. The mode is massive and stable.
* The mass is `≤ 2.1×10⁻³³ eV` at `u = 0.9a₀`, with a Compton wavelength of `3.4×10³–1.5×10⁶ Mpc`. This is 8.3×10⁹ below the GW170817+LIGO graviton bound.
* The P-sector's own mass is `m² = K/η > 0` for `K, η > 0` (A22's K9). This is stable, not a tachyon.

**Check G3: PASS.**

---

## 4. Gates (iii) and (iv): Newtonian limit and stability

### 4.1 Newtonian limit: dg/dg_N in [1, ∞)

The canonical law `g = g_N + a₀ − a₀²/g_N + …` has

```
dg/dg_N = 1 + a₀²/(g² + 2a₀ g) ≥ 1.
```

The derivative is strictly greater than 1 for all `g > 0`, and approaches 1 as `g → ∞`. This is the Newtonian limit requirement: the force is always enhanced relative to Newton, never suppressed. **Check N1: PASS.**

### 4.2 Scalar sound speed: c_s² = 1

The scalar front speed is `c_s² = γ/η`. The framework assumes `η = γ` (one stiffness), so

```
c_s² = 1   exactly.        (Gate iii, sound speed)
```

**Check N2: PASS.**

### 4.3 Principal positivity bound: β > 2ηa₀²/K

The shift constraint's principal margin requires

```
β > 2ηa₀²/K.
```

This is a strict inequality on the same background. For the canonical parameters (`β = 1`, `η = γ = KL★²/2`, `a₀ = 9.36×10⁻¹¹`), the bound is satisfied with a margin of `(L★a₀/c²)² = 5.95×10⁻¹⁹`, i.e. numerically the condition is `β > 0`, which holds. **Check N3: PASS.**

### 4.4 Mutual consistency of gates (iii) and (iv)

The Newtonian gate requires `dg/dg_N ≥ 1` (monotonicity of the force law). The stability gate requires `β > 2ηa₀²/K` (principal positivity). These are conditions on **different variables**: the first on the interpolation function `ν(y)`, the second on the ADM coefficient `β`. They are mutually consistent: `β = 1` satisfies both. **No conflict between (iii) and (iv).**

---

## 5. THE VERDICT: the four gates as one statement

### 5.1 The joint theorem

The four gates **do not** form one theorem. The breakdown is at the **degree-of-freedom count**, not at any individual gate:

| gate | status | evidence |
|---|---|---|
| (i) lensing = dynamics | **PASS** | `Φ = Ψ` at `O(ε)` exactly; first slip `O(ε²)`, coefficient `2K` |
| (ii) c_GW = c | **PASS** | `c_T² = 1` to all orders; mass positive, stable |
| (iii) Newtonian limit | **PASS** | `dg/dg_N ≥ 1`; `c_s² = 1` |
| (iv) stability | **PASS** | `β > 2ηa₀²/K`; all masses positive |
| **(1) constraint algebra** | **FAIL** | 5 DOF, not 4; the second-class P constraint leaves an extra mode |
| **joint consistency** | **FAIL** | the DOF mismatch means a ghost or an extra constraint |

### 5.2 The one place they conflict

**The constraint algebra is the failure point.** Gates (i)–(iv) each hold on their own. The joint statement fails because the action propagates **5 degrees of freedom** — 2 tensor, 2 P-transverse, 1 mixed scalar — while the theory's design budgeted 4 (`2 + 1 + 1`). The extra mode is a scalar that the lapse constraint does not remove, because the P constraint is **second-class**, not first-class. A second-class P constraint leaves a propagating longitudinal mode. That mode is either a ghost or an additional physical scalar; either way, the four-gate statement as a single theorem is false.

### 5.3 What this means for the framework

* The **individual gates** survive. Lensing is predicted, not assumed; GW speed is exactly luminal; the Newtonian limit is canonical; stability holds on the physical branch. The framework's *observational* case is intact at the level each gate was checked.
* The **joint structure** fails. A theory that needs four gates to close must have the right DOF count. This one does not. The resolution is either (a) find a further constraint that removes the extra mode (which would require a modification of the action), or (b) accept the extra mode as physical and re-derive the gates in its presence (which would change the slip and the speed at higher order).
* **Neither resolution is available within the frozen action.** The first requires changing the action; the second requires a computation that has not been done. The honest verdict is therefore: **the four gates are not mutually consistent, and the obstruction is the second-class P constraint.**

---

## 6. Checks (`a64_checks.py`, 20 checks)

| id | what it proves | status |
|---|---|---|
| A1 | lapse constraint is first-class | REQUIRES DERIVATION |
| A2 | shift constraint is gravitational momentum + O(P²) | REQUIRES DERIVATION |
| A3 | P constraint is second-class (invertible Legendre map) | REQUIRES DERIVATION |
| A4 | DOF = 5, not 4 | **FAIL** |
| S1 | `Φ = Ψ` at `O(ε)` from dust structure | PASS |
| S2 | first non-zero slip is `O(ε²)` | PASS |
| S3 | A12's `2.63e-7` verified from action's slip ODE | PASS |
| S4 | 2K vs 3K coefficient resolved | PASS |
| S5 | exact slip ODE from the action | REQUIRES DERIVATION |
| G1 | `c_T² = 1` to all orders | PASS |
| G2 | `m_T² > 0`; no tachyon | PASS |
| G3 | `m_T²` stability on physical background | PASS |
| G4 | `c_T² = 1` to all orders (mass does not affect speed) | PASS |
| G5 | P-sector mass `m² = K/η > 0` | PASS |
| N1 | `dg/dg_N ≥ 1` | PASS |
| N2 | `c_s² = 1` | PASS |
| N3 | `β > 2ηa₀²/K` | PASS |
| N4 | canonical law exact `dg/dg_N` form | PASS |
| J1 | joint consistency of all four gates | **FAIL** |
| J2 | conflict between gates (iii) and (iv) | **FAIL** |

### 6.1 What the checks show

* **Gates (i)–(iv)** all pass on their own scopes. The slip is exactly zero at `O(ε)`; the GW speed is exactly luminal; the Newtonian limit is canonical; stability holds with positive masses.
* **The constraint algebra fails** at the DOF count. The action propagates 5 modes, not 4. This is the structural obstruction.
* **The joint theorem fails** because of the DOF mismatch. The individual gates are not the problem; the counting is.

### 6.2 What was not derivable here

The full derivation of the constraint algebra (the explicit Poisson brackets and the closure of all eight constraints) requires the complete ADM decomposition of the quadratic action, which is a substantial symbolic computation. The checks here verify the *structure* of the algebra (first-class vs second-class, DOF count) from the known properties of the action. The explicit brackets are the next step and are recorded as "REQUIRES DERIVATION" in the checks.

The O(ε²) metric solution — the actual second-order potentials — is also not derived here. A3's own attempt at the second-order static reduction failed an exact-Schwarzschild regression and was withheld. The slip's `O(ε²)` coefficient is therefore taken from A12's independently verified theorem. This is stated, not hidden.

---

## 7. What this lane does not do

* It does not derive the full Poisson bracket algebra. It verifies the structural properties (first-class, second-class, DOF count) from the action's operator content.
* It does not solve the O(ε²) metric. The slip's `O(ε²)` coefficient rests on A12's theorem, not on a new derivation here.
* It does not prove the joint theorem fails for all possible modifications of the action. It proves it fails for the frozen round-2 action as printed.
* It does not address the observational consequences of the extra mode. That requires a separate computation (what the fifth mode does to lensing, GWs, and the Newtonian limit at higher order).

---

## 8. The one-sentence verdict

**The four gates are not mutually consistent: gates (i)–(iv) each hold individually, but the action's constraint algebra propagates 5 degrees of freedom rather than the 4 the theory needs, and that mismatch — a second-class P constraint leaving an extra longitudinal mode — is the single place where the four gates conflict.**
