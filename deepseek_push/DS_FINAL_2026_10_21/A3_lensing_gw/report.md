# A3 — lensing equals dynamics, and gravitational waves at light speed

**Lane:** A3_lensing_gw · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`
**Script:** `a3_checks.py` (15/15 PASS, exit 0, 2.3 s) · **Output:** `a3.out` · **Data:** `a3_results.json`
**Action source (frozen, not re-derived):** `core_open_problems_round2_2026_10_20/03_relativity/report.md` §2.

---

## 0. Claim

**Gate “tensor c_GW = c”: CLOSED-DERIVED.** For the unchanged action, the quadratic action of a
transverse–traceless mode on the de Sitter background is exactly the Einstein one,
`a³(ḣ² − p²h²)/(16K)`, so `c_T² = 1` **exactly** — not to leading order, not only at P = 0, and not only
in the principal symbol. The proof is structural: no operator in the action contains two derivatives of
`h^TT`, and the constraint sectors are TT-blind. §3 lists the precise operator that would have to be
present to break it, and confirms it is absent.

**Gate “lensing equals dynamics”: CLOSED-DERIVED at first order, NOT an identity.** `Φ = Ψ` holds
*exactly* at the order at which the two potentials are defined, because the P-sector's traceless spatial
stress is second order in the field (`Π ≡ p_r − p_t = W'(u)u = u²/[K(1−u/a₀)] = O(P²)`). The framework's
central claim is therefore **true as a theorem at O(ε)** and **false as an identity**: the first nonzero
slip is `O(ε²)`, i.e. `(Φ−Ψ)/Φ = O(Ψ)`. For a Milky-Way-like solution that is
`|1 − Φ/Ψ| = |1 − M_dyn/M_lens| ≤ 2.63×10⁻⁷` — 5–6 orders of magnitude below any lensing slip
measurement, and therefore operationally indistinguishable from equality, but formally nonzero.

**Scalar sector: CONDITIONAL(γ ≤ η).** On the same background the scalar front speed is `c_s = √(γ/η)`
exactly, so `c_s ≤ c ⟺ γ ≤ η`; it **can** exceed `c` (any `γ > η`), and the phase speed exceeds `c` in an
infrared band `p² < x₊` around the de Sitter gap. The joint bound including the polarized static branch is
`γ/η + 4γa₀²/K ≤ 1`, whose second term is `1.19×10⁻¹⁸` for `L★ = 24 pc` — i.e. numerically the whole
condition is `γ ≤ η`.

---

## 1. Conventions (one discrepancy with the brief, resolved)

The action is used exactly as printed in the round-2 report:

```
L/(N√h) = [R3 + K_ij K^ij − (1+β)θ² − 2Λ]/(4K)
          + P^i D_i log N − W_full(u) + (η/2) E_i E^i
          − (γ/2)(D_i P^i)² − (γ/4) F_ij F^ij ,
W_full = (a₀²/K)[−u/a₀ − log(1−u/a₀)],   u = K√(h^{ij}P_iP_j),
E_i = (Ṗ_i − ℒ_N P_i)/N,   F_ij = ∂_iP_j − ∂_jP_i,   P₀ = N^iP_i .
```

`(R−2Λ)/(4K)` is the Einstein–Hilbert term `R/(16πG)`, so `4K = 16πG`, i.e. **`K = 4πG` for this
action**. The DS_FINAL brief writes `K = 8πG`; that is a different normalisation of the same symbol and
would halve the gravitational coupling of the printed action. Every formula here is kept in terms of the
action's own `K`; all numerics use `K = 4πG = 8.3872×10⁻¹⁰`. Lane A12 adopted `K = 4πG`
independently (`A12_slip_theorem/a12_results.json`), so the two lanes are on one convention.
`c = 1`, signature `(−+++)`, `[η] = [γ] = [K] = length²`, `β` dimensionless, `u < a₀`.

---

## 2. Static spherically symmetric sector

### 2.1 Exact reduction

`ds² = −N²dt² + f δ_ij dx^i dx^j`, `P_i = P(r)x_i/r`, `N^i = 0`, dust matter `L_m = −ρN`
(so `T^t_t = −ρ`, `T^i_j = 0`). With

```
R3[fδ] = −2f″/f² + (3/2)f′²/f³ − 4f′/(r f²),      √h = f^{3/2},
d ≡ D_iP^i = f^{−3/2}(1/r²)(r² f^{1/2}P)′,        F_ij ≡ 0   (radial P is a gradient),
```

the angle-integrated Lagrangian is `L = 4πr²[N f^{3/2}(R3/(4K) − W − (γ/2)d²) + f^{1/2}P N′ − ρN]`.
Varying `N`, `f`, `P` gives three exact ODEs. The lapse one is the Hamiltonian constraint and is the
cleanest:

```
R3 = 2Λ + 4K [ ρ + d + W_full(u) + (γ/2)d² ] .                                    (H)
```

**(H) is verified three independent ways** (checks K0, K0b, K1): as an identity against the directly
varied action; the `R3` formula against a from-scratch 3D Christoffel/Riemann build; and the exact
isotropic Schwarzschild chart `N = (1−m/r)/(1+m/r)`, `f = (1+m/r)⁴`, `P = 0`, `ρ = 0`, `Λ = 0`
as a solution, at three interior points in **exact rational arithmetic** — no weak-field expansion
anywhere. Because the check is inhomogeneous-free it does not by itself fix the `ρ`-coupling; the
`P`-equation check K2 does: `EP(P=0) = √f N′ ≠ 0`, i.e. **`P = 0` is not a solution in a gravitational
field**. The sector is sourced by the acceleration, as it must be — this is what makes the theory
modified gravity rather than GR plus a decoupled field.

### 2.2 The anisotropic stress, exactly as a function of u

Only the traceless part of the spatial stress can produce a slip. For the sector's non-derivative
operator, `T^i_j = W′(u)u P^iP_j/|P|² − δ^i_j W`, hence

```
Π ≡ p_r − p_t = T^r_r − T^θ_θ = W′(u) u = u²/[K(1 − u/a₀)] .                       (Π)
```

**(Π) is exact in `u`, not an expansion** (check K3: `W′u − u²/[K(1−u/a₀)] = 0` identically). It is
strictly positive for every `u > 0` and diverges at the cap `u → a₀`. Expanding `u = εq` gives
`Π = ε²q²/K + O(ε³)` (check K4): the sector's traceless stress is **second order in the field**, because
every one of its operators is a product of two first-order objects.

### 2.3 Why `Φ = Ψ` at first order, and where it fails

The exact slip lemma is `G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)`; a slip requires a nonzero
`T^TF_ij`. From (Π): at `O(ε)` the sector's traceless stress vanishes, so `Φ₁ = Ψ₁` **identically** —
this is a theorem, not a coincidence of isotropy, and it reproduces the round-1 leading result
(`Δ(Φ−Ψ)=0 ⇒ Ψ=Φ` with decaying boundary conditions) from the same action. At `O(ε²)` the source is
nonzero, so

```
Φ − Ψ = O(ε²),        (Φ − Ψ)/Φ = O(Ψ) = O(v²/c²).                                (S)
```

**The framework's central claim is thus true at the order at which it was derived and false as an
identity.** This is the exact statement the round-1 “leading lensing equality” was reaching for.

### 2.4 Size on a Milky-Way-like solution

Rather than re-solve the profile (that is lane A12's independent theorem and numerical run, and the
coordinator has ruled it the cross-check), I quote A12's numbers as external inputs, labelled:

| quantity | value | source |
|---|---|---|
| `1 − Φ/Ψ` at 10 kpc | `−9.13×10⁻⁸` | A12 `a12_results.json` |
| `1 − Φ/Ψ` at 100 kpc | `−1.32×10⁻⁷` | A12 |
| `max |1 − Φ/Ψ|` over the model galaxy | `2.63×10⁻⁷` | A12 |
| same, at Saturn | `≈10⁻⁹` | A12 |

A12's theorem (same `K = 4πG`, same frozen action, its own 11/11 checks) states `Φ/Ψ = 1 + O(Ψ)` with
the identical structural reason — the sector is a *charge* sector at leading order, not a stress sector.
Two independent routes therefore agree on both the order and the coefficient scale. **Operationally
lensing mass = dynamical mass to `2.6×10⁻⁷`**, versus a current observational reach on the slip of order
`10⁻¹`; the claim survives every existing test by ~6 orders of magnitude. It is not, however, an identity,
and any future `10⁻⁷`-level slip measurement would see it.

---

## 3. Tensor sector: `c_T² = 1` exactly

### 3.1 The quadratic action

Background `P̄ = 0`, `N = 1`, `h_ij = a²δ_ij`. Perturb `h_ij = a²(δ_ij + h^TT_ij)` with
`∂_ih^TT_ij = 0`, `h^TT_ii = 0`; one mode `h^TT = h cos(kz)·diag(1,−1,0)`, physical `p = k/a`.
The two contributions to the quadratic action are computed exactly:

* **gradient**: `R3^{(2)} = −(1/4)p²h²` (check K5, from a full 3D Christoffel/Riemann build of the
  perturbed 3-metric, mode-averaged; the coefficient is exactly `−1/4`, no `β`, no `P`);
* **kinetic**: `K_ijK^ij − (1+β)θ² = 3H² + ¼ḣ² − (1+β)(3H)²`, i.e. the TT part is exactly `¼ḣ²`
  (check K6). `θ = 3H` **exactly** for TT because `tr h^TT = 0`, so the whole `(1+β)θ²` operator —
  the only non-Einstein term in the gravitational sector — contributes nothing to the tensor mode.

Hence

```
S_TT^{(2)} = (1/16K) ∫ a³ [ ḣ² − p² h² ] dt ,        c_T² = 1   exactly.            (T)
```

### 3.2 Why no other operator can enter

The sector couples to the metric only through `u = K√(h^{ij}P_iP_j)`, `d = D_iP^i`, `F_ij`, `E_i`, and
`P^iD_i ln N`. On the TT mode, at quadratic order in perturbations:

| operator | TT matrix element | reason |
|---|---|---|
| `−W(u)` | `0` | `W` depends on `h^{ij}P_iP_j`; `P̄ = 0` ⇒ `δ²W = ½W″δP²`, no `∂h` |
| `P^iD_i ln N` | `0` | linear in `δP`, and `∂_i ln N = 0` on the background |
| `(η/2)E_iE^i` | `0` | `δE_i = ∂_tδP_i`; `h^{TT}` enters only at cubic order |
| `−(γ/2)(D_iP^i)²` | `0` | `δd|_{∂h} = −P̄_j∂_ih^TT_ij = 0` by transversality |
| `−(γ/4)F_ijF^ij` | `0` | `F` is built from `∂_{[i}P_{j]}`, no metric at linear order |
| `−2Λ`, `R3`, `K_ijK^ij` | Einstein | gives (T) |

**No-go / breaker inventory.** `c_T = 1` is destroyed by any operator that (i) carries two derivatives of
`h^TT`, or (ii) contracts the TT perturbation with a non-transverse background tensor. Concretely, the
three operators that would do it are

1. a non-Hodge stiffness `−(γ/2)|D_iP_j|²` instead of `−(γ/2)(D·P)² − (γ/4)F²` — this gives
   `c_T² = 1 + 2K|P̄|²` (round-1 adversarial control; reproduced as mutation `naive_stiffness`, which
   fails K7);
2. a `P`–curvature coupling `ξ P^iP^jR_ij` or `ξRP²`;
3. an explicit `n_in_j`/`h_ijP^iP^j` multiplier of `h^{TT}` (a condensate or Proca mass would do it).

**None of the three is present in the printed action**, and the check set verifies the two that are
expressible as coefficient identities. Gate closed.

---

## 4. Scalar sector on the same background

From the round-2 reduction (reused, not re-derived) the scalar mode has

```
Q(p) = B + ηp²,   V(p) = γp⁴ + 2BH²,   B = K(2+3β)/β,
ω²(p)/p² = (γp² + 2BH²/p²)/(B + ηp²) .                                             (S1)
```

* **Front (characteristic) speed:** `c_s² ≡ lim_{p→∞} ω²/p² = γ/η` (check K8). So
  `c_s ≤ c ⟺ γ ≤ η`: an exact inequality in the couplings, with `β` entering only through the IR scale.
* `γ > η` ⇒ `c_s > c` at short wavelengths: **the scalar sector of this action is superluminal unless
  `γ ≤ η`, and the printed action does not fix `γ/η`.** This is the honest answer to “can it exceed c”:
  yes, for any `γ > η`.
* **Where the phase speed exceeds c:** `γp⁴ + 2BH² > Bp² + ηp⁴` ⟺ `(γ−η)x² − Bx + 2BH² > 0` with
  `x = p²`, which for `γ < η` holds exactly for `x < x₊ = [B + √(B² + 8BH²(η−γ))]/(2(η−γ))`
  (check K10). That band is `p ≲ √2 H` — the de Sitter gap, where `ω → √(2)H` is finite and `ω/p` is
  not a signal speed. It is not a causality violation, but it means “`c_s ≤ 1` everywhere” is false for
  every admissible `γ < η`; the correct statement is the front-speed one.
* **Joint bound with the polarized static branch** (round-2 §4): the worst non-tensor speed there is
  `(γ/η)(1 + 4ηu²/K)`, so full luminality of the non-tensor sector requires
  `γ/η + 4γa₀²/K ≤ 1` (check K11). With `γ = KL★²/2`, `L★ = 24 pc`, the second term is
  `2(L★a₀/c²)² = 1.19×10⁻¹⁸` (check K12), i.e. **numerically the condition is just `γ ≤ η`**, and the
  round-2 kinetic margin `β > 2ηa₀²/K` is a separate requirement on `β`.

---

## 5. Status

| gate | status | content |
|---|---|---|
| tensor `c_GW = c` | **DERIVED** | `c_T² = 1` exactly, eq. (T); breaker inventory in §3.2 |
| lensing = dynamics | **DERIVED** at `O(ε)`; **not an identity** | `Φ₁ = Ψ₁` from `Π = O(ε²)`, eq. (Π),(S); `O(ε²)` slip |
| numerical slip size | **NUMERICAL** (external, A12) | `≤2.63×10⁻⁷` relative, 10 kpc `−9.13×10⁻⁸` |
| scalar `c_s ≤ c` | **CONDITIONAL(γ ≤ η)** | eq. (S1); superluminal for `γ > η`; IR band is the gap |

Premises used, all explicit: (i) dust matter `L_m = −ρN` for the static source; (ii) the frozen printed
action with `K = 4πG`; (iii) staticity and the clock-aligned branch for §2; (iv) `P̄ = 0` de Sitter
background for §3–4. No fitted number was introduced. `a₀`, `G`, `L★` enter only in §2.4/§4 numerics.

## 6. Checks (`a3_checks.py`, 15/15 PASS, 2.3 s)

K0 lapse equation = Hamiltonian constraint (exact identity); K0b `R3[fδ]` from an independent 3D
Christoffel/Riemann build; K1 exact isotropic Schwarzschild solves it (rational arithmetic); K2 `P=0` is
not a solution; K3 `Π = W′u = u²/[K(1−u/a₀)]` exactly; K4 `Π = O(ε²)`; K5 TT gradient `= −p²h²/4`;
K6 TT kinetic `= ḣ²/4`; K7 `c_T²=1`; K8 `c_s²→γ/η`; K9 the causality quadratic; K10 the superluminal
band is `p² < x₊`; K11 static-branch bound; K12 the `a₀` term is `1.19×10⁻¹⁸`; K13 slip `= O(Ψ)`.

## 7. What this does not do

* It does not solve the static profile: the `O(ε²)` slip coefficient is taken from A12's independently
  verified theorem, not re-derived here. My own exact reduction produced the Hamiltonian constraint (H)
  and the exact anisotropic stress (Π), but my second metric equation failed an exact-Schwarzschild
  regression at `O(ε²)` and is therefore **withheld rather than published**; the `O(ε²)` coefficient in
  §2.4 rests on A12.
* It does not prove `γ ≤ η`; it proves that `γ ≤ η` is *equivalent* to scalar luminality.
* `c_T = 1` is a classical statement about the quadratic action on a `P̄ = 0` de Sitter background with
  TT perturbations: not a finite-frequency waveform, a loop statement, or a regularity proof.

## 8. Next

1. Fix the second-order static reduction (the failure is in the `f`-variation's Ostrogradski handling,
   not in the physics: the Hamiltonian constraint and (Π) are both verified) and confirm A12's `O(ε²)`
   coefficient from the action directly.
2. Fix `γ/η` from an independent premise (`η = γ` exactly, or `η > γ` from causality); until then the
   scalar sector is luminal only conditionally.
3. Propagate the `2.6×10⁻⁷` slip into a real lensing forecast: it is `~6` orders below current reach, so
   the honest forecast is “no discrimination”, which should be recorded rather than sold as a test.
