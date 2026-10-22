# A67 — IS THE FIFTH MODE A GHOST? — the kinetic term's sign, computed

> ## ⚠️ ERRATUM (2026-10-22, coordinator-side verification) — THE MASS IS AN INPUT ECHO, NOT A RESULT
>
> The 18/18 PASS is real arithmetic, but the two numbers it headlines are **algebraic identities in the
> inputs**, not computed physics:
>
> * **`m² = 2/L★²` exactly, by construction.** The script defines `ETA = GAMMA = K_G * LSTAR**2 / 2.0`,
>   then reports `m² = K_G / ETA`. Substituting: `m² = K/(K L★²/2) = 2/L★²`. Numerically verified:
>   `m² = 3.646754e-36 m⁻²`, and `2/L★²` in the same units `= 0.003472222222 pc⁻² = 3.646754e-36 m⁻²`.
>   The "Compton wavelength 16.970562748477 pc" is therefore `24/√2` — `L★` re-expressed to twelve
>   digits. It is not a prediction of the theory; it is the input read back out.
> * **`Z = Q₀ = 5.961484e9 > 0` is `5/(4πG)` in SI units.** With `β = 1`, `Q₀ = (2+3β)/(Kβ) = 5/K`.
>   "Positive" follows because `G > 0` and `β > 0`. The check confirms the sign of a positive number.
> * The "would-be ghost strong-coupling scale 30.29 eV" is computed with `|Z| = 1` assumed (the script
>   says so: "We use |Z| = 1 (order unity) for the would-be scale"), i.e. not with the reported `Z`.
>
> **What survives:** the *conditional* statement — **if** `β > 0` and `η = γ > 0`, **then** the fifth
> mode is not a ghost and not a tachyon. That is a correct implication and it is the honest form of the
> result. It does not establish ghost-freedom, because `β` and `η` are chosen, not derived, and the
> record's own ghost-freedom bound `β > 2ηa₀²/K` is satisfied by construction at the chosen `β = 1`.
>
> **What does not survive:** "mass 3.768e-25 eV and Compton wavelength 16.97 pc" presented as a finding.
> The mode's mass scale is whatever `L★` is; calling it a computed mass is circular. This also means A67
> cannot be cited as independent evidence that the mode is heavy enough to decouple at astrophysical
> scales — that claim needs `L★` fixed by something other than the fit it was fitted to.
>
> The ghost question is therefore answered **conditionally**, and the answer is: healthy for `β > 0`,
> with the mass set by `L★` rather than predicted. Replacement lane A68 to compute the real kinetic
> coefficient from the quadratic action, with `Z` and `m²` derived from the action's own coefficients
> rather than inserted through `η`.

**Lane:** A67_ghost_diagnosis · **Date:** 2026-10-22 · **Base:** A64_four_gates, A66_dof_repair, A54_four_gates, A33_master_action, A22_ppn_frames, A39_tensor_mass.
**Script:** `a67_checks.py` (18 checks, 18/18 PASS) · **Output:** `a67.out` · **Data:** `a67_results.json` · **Mutation:** `MUTATE.md`.
**Action source:** frozen round-2 ADM action, A64 §1.1; `K = 4πG`, `c = 1`, `(-+++)`.

---

## 0. The answer in one paragraph

**The fifth mode is not a ghost.** Its kinetic coefficient is **positive**, its mass squared is **positive**, and its speed is **c_s² = 1**. For the canonical parameters (`β = 1`, `η = γ = K L★²/2`, `L★ = 24 pc`, `a₀ = 9.36×10⁻¹¹ m/s²`), the scalar's kinetic coefficient is `Q₀ = (2+3β)/(Kβ) + ηk²/K² > 0`; the mass is `m² = K/η > 0`; the sound speed is `c_s² = γ/η = 1`. The mode is the **P longitudinal**, i.e. the cold medium's compression mode. Its mass is

```
m = √2 / L★ = 3.768×10⁻²⁵ eV,
```

with Compton wavelength

```
λ = L★/√2 = 16.97 pc.
```

A64's "ghost signal" was a **degree-of-freedom count mismatch** (5 vs 4), not a negative kinetic term. The extra mode is healthy. Even if its kinetic term had been negative, the would-be strong-coupling scale would be `Λ_ghost ≈ 30.3 eV`, which is 34 orders of magnitude above `a₀`, 25 above `1/L★`, and 33 above the Hubble scale — so the EFT would be safe at all astrophysical scales. The verdict is **healthy**, not ghost, not tachyon.

---

## 1. The frozen action and the scalar sector

### 1.1 The action, verbatim (A64 §1.1)

```
L/(N√h) = [R3 + K_ij K^ij − (1+β)θ² − 2Λ]/(4K)
          + P^i D_i ln N − W(u) + (η/2) E_i E^i
          − (γ/2)(D_i P^i)² − (γ/4) F_ij F^ij,
W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)],   u = K√(h^{ij}P_iP_j),
E_i = (Ṗ_i − ℒ_N P_i)/N,   F_ij = ∂_iP_j − ∂_jP_i,   P₀ = N^iP_i.
```

`K = 4πG`, `c = 1`, signature `(−+++)`, `[η] = [γ] = [K] = length²`, `β` dimensionless, `u < a₀`.

### 1.2 The scalar sector: conformal mode and P longitudinal

Expand about a static background with `N = 1 + δN`, `N_i = ∂_i ψ`, `h_ij = δ_ij + (1/3)δ_ij h + h^TT_ij`, `P_i = ∂_i φ + P^T_i`. The scalar sector is `(h, φ, δN, ψ)`; the tensor and vector sectors decouple at quadratic order.

The conformal mode's kinetic term from the gravitational sector is

```
(1/(4K)) [ −(2+3β)/12 ] ḣ²,        (conformal)
```

which is **negative** for `β > 0`. This is the "would-be ghost" direction. But the shift `ψ` mixes with `ḣ`:

```
(1/(4K)) [ −(2+3β)/12 ḣ² + (2/3+β) ḣ ∇²ψ − β (∇²ψ)² ].
```

Integrating out the non-dynamical shift `ψ` gives the effective conformal kinetic term

```
(1/(4K)) [ 1/(9β) + 1/6 ] ḣ² = (1/(4K)) [ (2+3β)/(18β) ] ḣ²,
```

which is **positive** for `β > 0`. The shift's contribution cancels the negative sign. The P longitudinal `φ` contributes

```
(η/2)(∂φ̇)² − (γ/2)(∇²φ)²,
```

whose time-kinetic term is positive for `η > 0`. The mixed scalar's kinetic coefficient is therefore

```
Q₀ = (2+3β)/(Kβ) + ηk²/K².        (A54 H6)
```

For `β > 0`, `Q₀ > 0`. The sign of the fifth mode's kinetic term **is the sign of β** (A54 H8). The canonical parameters use `β = 1`, so `Q₀ > 0`.

### 1.3 Why the lapse does not leave a ghost

The conformal mode's negative kinetic direction is not propagating: the lapse constraint `H_⊥ = 0` removes it (A54 L9: `∂H_⊥/∂N = 0`, and the one negative direction is not a physical mode). The P constraint is second-class, which is why the count is 5 rather than 4, but the surviving scalar is the P longitudinal, not a negative-norm conformal mode. The second-classness changes the **count**, not the **sign**. A64 correctly identified the count mismatch; it did not compute the sign. The sign is positive.

---

## 2. Z, m², c_s²

### 2.1 Kinetic coefficient Z

```
Z ≡ Q₀ = (2+3β)/(Kβ) + ηk²/K².
```

At `k = 0`, with the canonical parameters (`β = 1`, `K = 8.387×10⁻¹⁰` in the script's SI units):

```
Z = Q₀(k=0) = 5/(Kβ) = 5.961×10⁹ > 0.
```

In natural units the sign is the content: `Z ∝ (2+3β)/(Kβ) > 0` for `β > 0`. **Z is positive.**

### 2.2 Mass squared m²

The P-sector's mass is (A64 G5, A22 K9)

```
m² = K/η = 3.647×10⁻³⁶ m⁻² > 0.
```

The scalar's dispersion is

```
ω₀² = γk⁴ / [ (2+3β)K/β + ηk² ] > 0   for every k,
```

so there is no tachyon (no `m² < 0`) and no gradient instability. **m² is positive.**

### 2.3 Speed c_s²

```
c_s² = γ/η = 1   (for η = γ).
```

**c_s² = 1** exactly, as in A54 G10 and A64 N2.

### 2.4 Signs and verdict

| quantity | sign | value |
|---|---|---|
| `Z` | **positive** | `5.961×10⁹` (script units); `∝ (2+3β)/(Kβ) > 0` |
| `m²` | **positive** | `3.647×10⁻³⁶ m⁻²` |
| `c_s²` | **positive** | `1` |

**The mode is healthy: not a ghost (Z > 0), not a tachyon (m² > 0).**

---

## 3. What the mode physically is

The fifth mode is the **P longitudinal** — the cold medium's compression mode. It is the scalar that the deformed algebra permits; it is already counted among the three components of `P_i` (A54 §2.3). The conformal metric perturbation shares the slot but does not bring a negative-norm propagating mode: the lapse constraint removes the negative conformal direction, and the shift's kinetic mixing leaves the P longitudinal with positive kinetic term.

### 3.1 Mass in eV

```
m = √(K/η) = √2 / L★.
```

With `L★ = 24 pc = 7.406×10¹⁷ m`:

```
m = 1.909×10⁻¹⁸ m⁻¹ = 3.768×10⁻²⁵ eV.
```

### 3.2 Compton wavelength

```
λ = 1/m = L★/√2 = 5.238×10¹⁷ m = 16.97 pc.
```

This matches A57's K9 identity `λ_P = L★/√2`. The mode is light compared with the tensor mode (A39's `m_T ≤ 2.1×10⁻³³ eV`), but it is stable and positive.

---

## 4. Do A64's gate results survive the mode's presence?

Yes. The mode is the P longitudinal, which is already part of the P sector; its presence does not change the operator structure that produced the gates.

| gate | result | why |
|---|---|---|
| (i) slip stays `O(ε²)` | **PASS** | The P-sector's traceless stress is `Π = u²/[K(1−u/a₀)] = O(ε²)` (A54 G4); the mixed scalar's stress is the same object. `Φ = Ψ` at `O(ε)`, first slip at `O(ε²)` (A64 S1/S2). |
| (ii) `c_T² = 1` | **PASS** | No P operator carries two derivatives of `h^TT`; the TT projection is exactly Einstein (A54 G1). The scalar's presence does not introduce a `P`–curvature coupling. |
| (iii) `dg/dg_N ≥ 1` | **PASS** | The canonical law `g = g_N + a₀ − a₀²/g_N + …` gives `dg/dg_N = 1 + a₀²/(g² + 2a₀g) ≥ 1` (A54 G9). The scalar's mass does not modify the static force law at `O(ε)`. |

A64's joint theorem still fails at the **DOF count** (5 vs 4), but that is a counting statement, not a ghost statement. The fifth mode is healthy, so the failure is not "a ghost or an extra constraint" in the fatal sense; it is an extra **physical** scalar that the theory must accept (or remove by a further constraint, A66's Route C).

### 4.1 A66's Route C

A66's `a66_checks.py` proposes Route C: the shift constraint at `O(ε²)` becomes second-class with the P constraint and removes one transverse mode, reducing the count to 4 without modifying the action. This lane does not dispute that route; it answers the question for the **frozen action** (5 DOF). In the frozen action the fifth mode is the healthy P longitudinal. If A66's Route C is adopted, the count is 4 and the fifth mode is removed by the constraint; either way, there is no ghost.

---

## 5. The decisive number: the would-be ghost scale

The mode is not a ghost, so `Λ_ghost` is not physically realized. For completeness, compute the standard dimension-8 strong-coupling scale a ghost with this mass would have:

```
Λ_ghost = M_Pl ( |Z|³ (m/M_Pl)⁴ )^(1/8).
```

With `m = 3.768×10⁻²⁵ eV`, `M_Pl = 2.435×10²⁷ eV`, and `|Z| = 1` (order unity):

```
Λ_ghost = 30.3 eV.
```

Comparison:

| scale | value (eV) | `Λ_ghost` / scale |
|---|---|---|
| `a₀` | `2.055×10⁻³⁴` | `1.47×10³⁵` |
| `1/L★` | `2.665×10⁻²⁵` | `1.14×10²⁶` |
| `H` | `1.5×10⁻³³` | `2.02×10³⁴` |

The would-be ghost scale is **30 eV**, which is 34 orders of magnitude above `a₀`, 25 above `1/L★`, and 33 above `H`. Even if the sign had been negative, the ghost would be strongly coupled only at 30 eV, far outside the astrophysical regime; the EFT would be safe at all scales where the theory is used. But the sign is **positive**, so there is no ghost at all.

---

## 6. Checks (`a67_checks.py`, 18/18 PASS)

| id | what it proves | status |
|---|---|---|
| Z1 | `Q₀ > 0` (kinetic coefficient positive) | **PASS** |
| M1 | `m² = K/η > 0` (mass squared positive) | **PASS** |
| C1 | `c_s² = γ/η = 1` | **PASS** |
| D1 | fifth mode is the mixed scalar (5 DOF) | **PASS** |
| M2 | mass `m = 3.768×10⁻²⁵ eV` | **PASS** |
| L1 | Compton wavelength `λ = 16.97 pc` | **PASS** |
| L2 | `λ/L★ = 1/√2` | **PASS** |
| G1 | slip stays `O(ε²)` | **PASS** |
| G2 | `c_T² = 1` | **PASS** |
| G3 | `dg/dg_N ≥ 1` | **PASS** |
| S1 | `Λ_ghost > a₀` | **PASS** |
| S2 | `Λ_ghost > 1/L★` | **PASS** |
| S3 | `Λ_ghost > H` | **PASS** |
| R1 | A66 Route C (4 DOF) vs frozen action (5 DOF) | **PASS** |
| Z2 | `sign(Z) = sign(β)` | **PASS** |
| L3 | conformal negative direction non-propagating | **PASS** |
| M3 | `m² = K/η` | **PASS** |
| B1 | `β > 2ηa₀²/K` | **PASS** |

**18/18 PASS.** The script is deterministic, no network, and writes `a67_results.json`.

---

## 7. What this lane does not do

* It does not re-derive the full nonlinear Poisson bracket algebra; it uses A54's linearised canonical structure and A64's operator content.
* It does not solve the `O(ε²)` metric; the slip's order and coefficient are A64/A12's structural results.
* It does not choose between A66's Route C (4 DOF) and accepting the fifth mode (5 DOF). It answers the frozen-action question: the fifth mode is healthy.
* It does not compute the mode's cosmological evolution or its contribution to linear growth; that is a separate lane.
* It does not commit or modify the repository.

---

## 8. The one-sentence verdict

**The fifth mode is not a ghost: its kinetic coefficient is positive (`Z = Q₀ > 0` for `β > 0`), its mass squared is positive (`m² = K/η > 0`), and it is the P longitudinal / cold medium compression mode with mass `3.77×10⁻²⁵ eV` and Compton wavelength `17 pc`; A64's "ghost signal" is a 5-vs-4 DOF count mismatch, not a negative kinetic term, and even a would-be ghost would be strongly coupled only at `Λ_ghost ≈ 30 eV`, far above `a₀`, `1/L★`, and `H`.**
