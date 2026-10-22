# A69 — WHAT FIXES THE P-SECTOR SOUND SPEED, AND WHAT DOES IT PREDICT?

**Lane:** A69_psector_sound · **Date:** 2026-10-22
**Base read:** `A68_bracket_algebra/report.md` §3.2–3.4 (Z, m², c_s², the transverse modes, the
Jacobian 1/η), `A54_four_gates/report.md` §2–3 (the count and the four gates), `A33_master_action/MASTER_ACTION.md`
(the frozen action, the coefficient table, `L*² := 2γ/K`), and the frozen action of
`core_open_problems_round2_2026_10_20/03_relativity/report.md` §2.
**Script:** `a69_checks.py` — **56/56 PASS, exit 0, 1.6 s** · **Output:** `a69.out` ·
**Data:** `a69_results.json` · **Mutations:** `MUTATE.md` (9 dials, each exit 1).

Nothing here re-derives the bracket algebra. A68's results are used as inputs: the five-mode count,
`Z = K(2+3β)/β + ηp²`, `m² = 0`, `c_s² = αp²/Z → 0`, `m_T² = K/η`, `c_T² = γ/η`, `α = γ` forced by
the shared stiffness, and `η ≠ γ` allowed (the map `(η,γ) ↦ (η, γ/η)` has Jacobian `1/η ≠ 0`).

Units: `K = 4πG = 8.430565e-56 eV⁻²`, `c = 1`, signature (−+++). `a₀ = 2.055043e-34 eV`
(9.36 × 10⁻¹¹ m s⁻², i.e. `Λ = 32πa₀² = 4.245625e-66 eV²`), `L* = 24 pc = 3.752972e+24 eV⁻¹`
(so `1/L* = 2.664555e-25 eV`), `γ = α = KL*²/2 = 5.937141e-07 eV⁻⁴`, `B = K(2+3β)/β = 4.215283e-55 eV⁻²`
at β = 1, `H₀ = 1.493e-33 eV`. Every number quoted below is in `a69.out`.

---

## 0. The answer in one paragraph

**Nothing fixes η/γ.** The action is invariant under the foliation-preserving diffeomorphisms for
*every* (η,γ) — computed on a periodic 3-torus with a general metric and a general shift, the change of
the P action is quadratic in the diffeomorphism amplitude (|ΔS|/S ≤ **9.698e-05** at λ = 0.02 for four
pairs spanning c_T² = 10³…10⁻³, with the λ² ratio **3.996** and no growth of the residual when η ≠ γ:
ratio **1.109**). There is no shift symmetry: `W(u) = u²/(2K) + …` gives a shift variation of exactly
**−a₀|c| = −2.055043e-34** per unit volume, i.e. a mass term `d²W/dP² = K = 8.430565e-56`. Weyl
invariance is not a symmetry of the action (the three derivative operators carry weight 2w, the clock
term w+2, `min_w max|exponent| = 2`), and even if it were, all three P operators share the *same*
weight, so the ratio γ/η would be Weyl invariant and no w could fix it. Conservation is the Noether
identity `∂_tT⁰⁰ + ∂_iT⁰ⁱ = Ṗ·EOM`, satisfied to **7.52e-17** for four (η,γ) pairs: an identity, not a
relation. The one honest handle is that **γ is fixed by the measured `L*` and η is free**, so
`c_T² = γ/η = m_T²L*²/2` (**O1**, exact to 1.5e-16): measuring the range of the P-mediated force
measures the sound speed. Observationally, **the action's own dark sector is blind to γ/η**: the P
sector's O(ε) stress is dust (w = p/ρ ∝ ε, verified by a factor **10** under a decade of ε), and its
pressure is the *elastic* one whose speed is `√(γρ_c) = 0.7204 m/s` (A16/A20's 0.72 m/s, reproduced to
5.0e-04) — **not** `√(γ/η)`, which is 10⁸ m/s at η = γ (ratio² = **1.732e+17**). So LSS, clusters and the
CMB constrain γ/η **not at all**; the honest answer is **UNCONSTRAINED**, and the only observable that
can see it is the dispersion of the two transverse P modes (their mass `√(K/η)`, i.e. the range of the
P-mediated stress). *If* one instead posits that the dark medium's pressure is `c_T²ρ`, the linear growth
of structure gives **γ/η < 1.916e-07** (95 % CL, 5 % suppression at k = 0.2 h Mpc⁻¹; **3.0659e-08** at
k = 0.5), which pushes the P-mode Compton wavelength above **38.77 kpc** (vs 16.971 pc at η = γ). The four
gates survive untouched for γ/η ≠ 1 — (i) exact at O(ε) with γ only at O(ε²), (ii) exact for every γ/η,
(iii) η absent altogether, (iv) an open set — so no gate fixes the ratio. The gapless k⁴ mode's
strong-coupling momentum is **p_sc = 2.8360e-69 eV** (K^{1/2}/(3π a₀L*³), agreeing with the independent
route K²/(8.485π a₀ α^{3/2}) to 1.8e-16): **1.899e-36 H₀**, **1.380e-35 a₀**, 1.064e-44 × 1/L*, with the
largest loop factor over CMB/LSS/galactic/`L*`/`a₀` scales equal to **1.904e-70**. The EFT is therefore
valid at *all* astrophysical scales, and the mode is **not** the MOND mediator: its static Green's
function is `−r/(8πα)` (∇²G = −1/(4πr) to 4.5e-09, unit flux to 1.1e-07), a linear potential and hence a
constant force, not 1/r.

---

## 1. Task 1 — the symmetry search

Each candidate is written as a transformation, the change of the action is computed, and the verdict is
stated. The computation is a spectral one: all fields are band-limited analytic functions on a periodic
3-torus (16³ points, all products below Nyquist so the quadrature is exact), derivatives are analytic,
and the *only* error is the O(λ²) truncation of the transformation — which is the quantity being measured.

### (a) Foliation-preserving diffeomorphisms

Transformation (`t → t`, `x^i → x^i + λξ^i(x)`, first order in λ):

```
δP_i = −λ(ξ^k ∂_k P_i + P_k ∂_i ξ^k)        [P_i is a spatial covector]
δN^i = −λ(ξ^k ∂_k N^i − N^k ∂_k ξ^i)        [N^i is a vector]
δN   = −λ ξ^k ∂_k N                        [N is a scalar]
δh_ij = −λ(ξ^k ∂_k h_ij + h_kj ∂_i ξ^k + h_ik ∂_j ξ^k)
```

`E_i = (Ṗ_i − ℒ_N P_i)/N` is a covector under exactly this transformation (the shift enters only through
`ℒ_N P_i`, and `1/N` cancels the lapse weight), so `η E_iE^i √h` is invariant for any η; `(D·P)²√h` and
`F_ijF^ij√h` are scalar densities for any γ. **Computed** (λ = 0.02, general metric, general shift, general
`P`):

| η | γ | S(0) | S(λ) | \|ΔS\|/S | c_T² |
|---|---|---|---|---|---|
| 1 | 1 | −3.559751543055e-01 | −3.560062898970e-01 | 8.747e-05 | 1 |
| 1 | 10 | −8.881709887165e+00 | −8.881570777378e+00 | 1.566e-05 | 10 |
| 10 | 1 | +4.965983189805e+00 | +4.965501588511e+00 | 9.698e-05 | 0.1 |
| 1 | 1e-3 | +5.903814010419e-01 | +5.903313682134e-01 | 8.475e-05 | 1e-3 |

The residual is **quadratic in λ** (halving λ divides it by **3.996**), so there is no first-order
failure; and it does **not** grow when η ≠ γ (max off-diagonal residual / diagonal residual = **1.109**).
Since the variation is `η·(identically zero) + γ·(identically zero)`, no (η,γ) relation is needed.

**Verdict: no relation.** The two operators are two independent invariants; a symmetry that acts on the
fields cannot relate their coefficients.

### (b) Shift symmetry `P → P + c`

The clock term is invariant up to a total derivative (`c^iD_i ln N = ∂_i(c^i ln N)`), but the potential is
not:

```
δS = −∫ N√h [K W'(u)/u] (P·c),      K W'(u)/u = 1/(1 − u/a₀).
```

At `u = a₀/2`, `|P| = a₀/(2K)`, `|c| = 1`: **δS = −a₀|c| = −2.055043e-34** per unit `N√h` volume,
computed two ways (from `KW'(u)/u` and from the closed form) to 0.0e+00. The breaking is a mass:
`d²W/dP²|₀ = K = 8.430565e-56` (5-point finite difference vs the analytic K, 1.5e-10). So there is **no
shift symmetry**, and the transverse P mass `m_T² = K/η` is exactly the would-be Goldstone mass.

**Verdict: no relation** (and no symmetry: the obstruction is computed, not declared — the `no_W`
mutation zeroes W and breaks S4, S5, S6).

### (c) Weyl / conformal invariance

With `g → Ω²g`, `P_i → Ω^w P_i` (constant Ω), the measured scaling exponents of the four operators,
including the 4-dimensional measure, are

| w | E² | (D·P)² | F² | clock `P^iD_i ln N` |
|---|---|---|---|---|
| 0.70 | +1.400000 | +1.400000 | +1.400000 | +2.700000 |
| 1.30 | +2.600000 | +2.600000 | +2.600000 | +3.300000 |
| 2.00 | +4.000000 | +4.000000 | +4.000000 | +4.000000 |

i.e. `(2w, 2w, 2w, w+2)` to 8.9e-16. Two computed facts follow. (i) **All three derivative operators share
one weight**, so a Weyl rescaling can only rescale η and γ together — `γ/η` is Weyl invariant
(difference of exponents 0.0e+00). No w fixes the ratio. (ii) **No w makes the action Weyl flat**:
`2w = 0` needs w = 0 while `w + 2 = 0` needs w = −2, and `min_w max|exponent| = 2`. Weyl invariance is not
a symmetry of this action at all, so it cannot impose anything.

**Verdict: no relation, and no symmetry.**

### (d) Conservation of the P stress-energy, `D_iT^{i0} = 0`

For the transverse mode the canonical quantities are `T⁰⁰ = (η/2)Ṗ² + (K/2)P² + (γ/2)(∂P)²` and
`T⁰ⁱ = −γ(∂^iP_j)Ṗ^j`; the exact identity is

```
∂_t T⁰⁰ + ∂_i T⁰ⁱ = Ṗ · EOM ,     EOM_i = ηP̈_i + KP_i − γ∇²P_i .
```

Computed for four (η,γ) pairs: the residual is **7.520e-17** of the natural scale `K A²ω`, and the
identity `LHS = Ṗ·EOM` holds to **7.520e-17** between two independent evaluations. Conservation is
therefore a **Noether identity** — it holds for every (η,γ) once the dispersion `ω² = (K+γp²)/η` is the
one the action implies, and it constrains nothing. (The `wrong_dispersion` mutation, which drops γp²,
breaks S10/S11 at 2.500e-01.)

**Verdict: no relation.**

### (e) What does fix it, then?

Only an extra assumption. Two are on the table and neither is in the action:

1. **A Lorentz-invariant dark sector** (`c_P = c`): this is exactly η = γ. It is A67's assumption and
   A33's "chosen" single stiffness; A68 already showed it is an input, not a consequence.
2. **Subluminality** `c_T ≤ c`: this is the *inequality* `γ ≤ η`, which A33's table records as "scalar
   luminality". It is a one-sided bound, not an equation, and the data (below) push γ/η far below 1, so
   it is satisfied with room to spare.

The genuinely useful reformulation is: **γ is fixed by the measured L\*, η is free.**
`γ = KL*²/2` is a definition (A33), `L* = 24 pc` is fitted (A65), and

```
c_T² = γ/η = (K/η)(L*²/2) = m_T² L*²/2          ⇒  η = KL*²/(2c_T²) .
```

So a measurement of the P-mode *mass* (equivalently the range `√(η/K)` of the P-mediated stress) is a
measurement of the sound speed, and vice versa (**O1**, both routes to 1.5e-16).

---

## 2. Task 2 — the observable

### 2.1 Three different "sound speeds", and which is which

This is where the lane's question has to be sharpened, because the theory has three:

| object | value at the canonical parameters | depends on |
|---|---|---|
| transverse P modes, `c_T² = γ/η` | 1 at η = γ (a speed of 2.998e+08 m/s) | γ/η |
| **elastic** (Γ = 2) speed of the dark medium, `c_s,el² = γρ_c` | **0.7204 m/s** = 2.4029e-09 c | γ and ρ_c — **not** η |
| gapless mixed scalar, `c_s² = αp²/Z → 0` | 5.000000e-01 at p = p\*, → 0 as p → 0 | p, through Z |

A16/A20/A33 quote the second (0.72 m/s) as the medium's elastic sound speed, and it is reproduced here to
**5.04e-04** from γ and ρ_c alone. The *third* is A68's gapless mode. The first is the one this lane is
about, and it is 10⁸ times faster: `c_T²/c_s,el² = 1.732e+17`.

### 2.2 Why the dark sector cannot see γ/η

The P sector's stress-energy at O(ε) is **dust**. The clock term `∫N√h P^iD_i ln N` integrates by parts to
`−∫N√h d` with `d = D_iP^i`, so `T⁰⁰ = d + O(ε²)` and `T_ij = O(ε²)`: the pressure is second order while
the density is first order. Computed: `w = p/ρ` falls by exactly **10** when ε falls by 10 (**O3**), i.e.
`w → 0` — the medium is pressureless at leading order and its pressure is the elastic one. Measured
numbers: `ρ_c = 2.2566e-27 kg m⁻³ = 9.7249e-12 eV⁴` (5.3643 ρ_b, A33), `c_s,el² = 5.774e-18`, and
`γρ_c = 7.706e-09` at z = 1100 — dust to one part in 10⁸ at recombination.

Consequently:

* **(a) Growth of structure.** With the action's own dark sector, the growth equation carries
  `c_s,el² = 5.774e-18`: the suppression at k = 0.2 h Mpc⁻¹ is **1.0000000000** (O10). The Jeans
  wavenumber is `8.743e+04 h Mpc⁻¹` — 10⁵ times the nonlinear scale, i.e. no suppression anywhere. The
  cold sector's velocity dispersion is `σ_c = √(a₀L*) = 8.3257 km/s` (A20/A65's 8.33, to 5.2e-04) and it
  is **fixed** — not a function of η.
* **(b) Cluster gas fractions and hydrostatic profiles.** These test the law `g_N = g²/(g+a₀)` and the
  `(L*/r)²` elastic-stress ratio, i.e. γ and ρ, not γ/η. No handle.
* **(c) CMB acoustic peaks.** The P sector has no direct coupling to the baryon–photon fluid (A22/A33:
  `L_m` minimal, no `P·J`, no `P·F_μν`), and its O(ε) stress is dust, so the peaks are ΛCDM + the law.
  No handle.
* **(d) Gravitational waves.** The TT quadratic action contains no P operator (no P term carries two
  derivatives of `h^TT`), so `d(ω²)/dk² = 1` exactly (**O13**) and a P background contributes only a
  *mass*: at u = a₀/2 that mass is **3.249e-34 eV**, eleven orders below the 1.2e-22 eV bound (**O14**).
  The loop-induced correction is `δc_T² ~ 6.670e-144` (**O15**) — the P–TT vertex is cubic, so there is
  no O(m_T²) mixing into the speed. **GW170817 is satisfied identically for every γ/η.**

The one observable that *can* see γ/η is the dispersion of the two transverse P modes themselves — their
mass `m_T² = K/η` (range `√(η/K)`) and their speed `√(γ/η)`. Nothing in the record populates them: there
is no production mechanism, `P = 0` on FRW (A33 §3.6), and the action gives no coupling to the thermal
bath. *If* they were thermally populated at `T_ν`, two bosonic modes would give `ΔN_eff = 0.5933`
(**O16**), which Planck's `ΔN_eff < 0.34` excludes — so the theory *must* have them unpopulated, which is
consistent with there being no mechanism.

**Answer: γ/η is UNCONSTRAINED by existing data, for a stated reason — the medium's pressure is γρ_c, not
(γ/η)ρ, and the transverse modes that do carry γ/η are massive, decoupled and unpopulated.**

### 2.3 The number, under the alternative premise

If the P sector's stress-energy is identified with a fluid whose pressure is `c_T²ρ` — the premise the task
poses — then γ/η controls the Jeans scale and LSS bounds it. Solving
`δ̈ + 2Hδ̇ = 4πGρδ − (c_s²k²/a²)δ` on a flat ΛCDM background (Ω_m = 0.3153, h = 0.674) from a = 10⁻³:

| c_s² | S(0.1) | S(0.2) | S(0.5) |
|---|---|---|---|
| 1e-9 | 0.9999 | 0.9997 | 0.9983 |
| 1e-8 | 0.9993 | 0.9973 | 0.9835 |
| 1e-7 | 0.9934 | 0.9737 | 0.8441 |
| 1e-6 | 0.9352 | 0.7599 | 0.1073 |
| 1e-5 | 0.4848 | −0.0194 | −0.0007 |

(`S = D(k)/D(0)`; the c_s = 0 run reproduces the exact ΛCDM growth function to **8.67e-10**, and in the
weak-pressure limit `1 − S ∝ k²` to **7.78e-04**.) Requiring a 5 % suppression at k = 0.2 h Mpc⁻¹:

```
γ/η < 1.916e-07   (95 % CL)      [k = 0.2 h/Mpc]
γ/η < 3.0659e-08                 [k = 0.5 h/Mpc, same criterion]
```

so **γ/η ∈ (0, 2 × 10⁻⁷)** at 95 % CL — seven orders below the "natural" η = γ. Equivalently
`η > 3.0984 eV⁻⁴` and, through `c_T² = m_T²L*²/2`, a P-mode Compton wavelength

```
λ_C = √(η/K) = L*/√(2c_T²) > 38.77 kpc     (vs 16.971 pc at η = γ)
```

(**O8**, both routes to 0.0e+00). That is a *prediction* of the alternative reading: the P-mediated force
would have a galactic range, not a 17 pc one. Note it is comfortably inside the subluminal window
`γ/η ≤ 1`, so it does not conflict with A33's `η ≥ γ`.

---

## 3. Task 3 — the four gates under `c_s² ≠ 1`

### (i) Lensing = dynamics

At O(ε) the P stress is a pure trace (dust), so `Φ − Ψ = 0` at O(ε) **for every (η,γ)** — the reason is
structural: every P operator is quadratic, so the traceless stress is O(ε²). Computed: the gradient-sector
quadrupole vanishes for the isotropic profile `P ∝ x` (ratio to its own trace **2.437e-11**, i.e. zero),
and the charge-sector quadrupole scales as ε² (ratio **4.0000000000** under a doubling of ε, **G3b**).

At O(ε²) there are three contributions:

```
Π_W   = u W'(u) = u²/(K(1−u/a₀))                  [A54 G4]
Π_γ   = γ d (P' − P/r)                            [gradient-sector quadrupole, computed]
Π_η   = η E_iE_j (traceless) → 0 on the static branch (E = 0)
```

At u = a₀/2, r = L\*: `Π_W = 2.5047e-13 eV⁴`, `Π_γ = 1.2523e-13 eV⁴`, ratio **0.5000** = (1−x)L\*²/r²
(**G1**, to 2.2e-16). So the γ-sector quadrupole is the *same order* as A54's W-term at r ~ L\* — a
refinement of A54's G4, which lists only the W-term. Neither contains η. The slip bound becomes
`(Φ−Ψ)/Ψ ≤ 2.63e-7 × (1 + 0.5) = 3.945e-07` — still five orders below any lensing test.

**Condition on γ/η: none.** γ enters at O(ε²) through the measured L\*, η does not enter at all.

### (ii) `c_T² = 1` for the graviton

No P operator carries two derivatives of `h^TT`, so the TT quadratic action is Einstein's and
`d(ω²)/dk² = 1` for every γ/η (**O13**, **G4/G4b** at γ/η = 10⁻³ and 10², exact to 0.0e+00). A P
background adds only a mass (3.249e-34 eV at u = a₀/2, **O14**) and the loop correction is 6.670e-144
(**O15**). **Condition on γ/η: none** — GW170817's |c_T − 1| < 10⁻¹⁵ is satisfied identically.

### (iii) `α₁ = α₂ = 0` near source

`α₁(1 AU) = 2r²/L*² = 8.161493e-14`, computed independently as `r²K/γ` (0.0e+00, **G5**). It scales as
1/γ (a 4× change in γ gives exactly 4.0000000000, **G7**) and is **η-independent** (**G6**): the static
solution contains no time derivative, so η never appears. `α₂ = 0` because the momentum density
`j_P = −ηE^jD^iP_j + D_j(ηE^jP^i)` vanishes identically for E = 0, checked at three η values (**G8**).
**Condition on γ/η: none** — α₁ depends on γ (through L\*), not on η.

### (iv) Stability

The canonical conditions are `Z = K(2+3β)/β + ηp² > 0 ⟺ β > 0`, `ω² = αp⁴/Z > 0 ⟺ α = γ > 0`,
`m_T² = K/η > 0 ⟺ η > 0`. On a 4 × 6 grid of (β, γ/η) — β ∈ {0.1, 0.5, 1, 3}, γ/η ∈ {10⁻³ … 10³} — all
**24/24** points are healthy (**G9**). The principal-positivity bound `β > 2ηa₀²/K` translates to
`η < 9.981e+11 eV⁻⁴`, i.e. `γ/η > 5.948e-19` (**G10**): vacuous. **Condition on γ/η: γ/η > 0 only.**

### Summary

| gate | condition on γ/η | why |
|---|---|---|
| (i) lensing = dynamics | **none** | exact at O(ε); γ enters only at O(ε²), η not at all |
| (ii) c_T² = 1 | **none** | no P operator is quadratic in ∂h |
| (iii) α₁ = α₂ = 0 | **none** | static: no time derivative, hence no η |
| (iv) stability | γ/η > 0 (and > 5.948e-19) | Z, ω², m_T² positive |

**No gate fixes γ/η.** Three widely spaced values (10⁻³, 1, 10³) survive all four (**G11**). The gates are
therefore *stronger* than A54 stated: A54 derived them with η = γ in places, and they hold without it.

---

## 4. Task 4 — the gapless k⁴ mode

### 4.1 Dispersion and the two branches

`ω² = αp⁴/Z`, `Z = B + ηp²`, `B = 4.215283e-55 eV⁻²`, `p_* = √(B/η) = 8.426063e-25 eV` at η = γ. At
p = p\* the two contributions are equal (`Z/B = 2.0000`) and `c_s² = 5.000000e-01`; at p ≫ p\* the mode
becomes a standard one with `c_s² → α/η = γ/η` (**C1a/C1/C1b** at γ/η = 0.37, 1, 100, to ≤ 1e-10). So the
gapless scalar *joins the medium's light cone in the UV* — γ/η is its high-momentum speed too.

### 4.2 The interaction and the loop factor

The leading interaction is the cubic term of `W`:

```
W = u²/(2K) + u³/(3Ka₀) + u⁴/(4Ka₀²) + … ,   u = K|P|
L₃ = −(K²/(3a₀)) |∇σ|³ = −(K²/(3a₀Z^{3/2})) p³ σ_c³ ,   σ_c = √Z σ .
```

One-loop two-point function, with `κ_L = √(α/B) = 1.186794e+24 eV⁻¹` (the Lifshitz mass
`M_L = 8.426063e-25 eV`):

```
δΠ/ω² = K⁴ / (144 π² a₀² Z³ κ_L⁶ p²) .
```

Setting it to 1 gives the strong-coupling momentum. In the IR branch (Z ≈ B, so `Z^{3/2}κ_L³ = α^{3/2}`):

```
p_sc = K² / (8.485 π a₀ α^{3/2}) = 2.8360e-69 eV
     = √K / (3π a₀ L*³)          = 2.8360e-69 eV      (independent route, 1.8e-16)
```

In the UV branch (Z ≈ ηp²) `p_sc = K²/(12π a₀ α η^{1/2}) = 2.0054e-69 eV`, i.e. the same number to a
factor √2 — the expected O(1) scheme ambiguity, and irrelevant at the margin below.

### 4.3 The comparisons

| ratio | value |
|---|---|
| p_sc / H₀ | **1.899e-36** |
| p_sc / a₀ | **1.380e-35** |
| p_sc / (1/L\*) | **1.064e-44** |
| largest loop factor over CMB, LSS, galactic, 1/L\*, a₀ scales | **1.904e-70** |
| parametric form | p_sc = 0.01189 M_L³/(M_Pl a₀) |

For the three a₀ in play, `p_sc = 2.8360e-69 eV` (canonical 9.36e-11 m s⁻²), **2.3450e-69 eV**
(a₀ = 1.132e-10), **3.1626e-69 eV** (κ = 0.371, A51) — the ratio scales as 1/a₀ exactly (**C14**), so the
κ error bar moves the cutoff by 1/κ, a factor 1.18, and nothing more.

**The EFT is valid at every astrophysical scale**, with 36 orders of margin to the Hubble scale: the loop
expansion is under control by ≥ 70 orders everywhere from the CMB to the de Sitter horizon.
`p_sc` is not a cutoff anyone can reach — it corresponds to a length of order 10⁶¹ m, i.e. 10³⁶ Mpc.

### 4.4 Can it be the MOND mediator?

It is gapless, so it mediates a long-range force — but the wrong one. The static operator is
`α∇⁴σ = J`, whose Green's function is

```
G(r) = −r/(8πα) ,     ∇²G = −1/(4πr)  (to 4.5e-09) ,   flux 4πr²∂_r∇²G = 1  (to 1.1e-07)
```

so `Φ ∝ −r`: a **linear potential, i.e. a constant force** — neither the Newtonian `1/r` potential nor
the deep-MOND `1/r` force (a logarithmic potential). It is exactly the shape of the *second* term of the
theory's own exact linearised solution, `Φ = −μ/r + μr/L*²` (A22): the two terms are equal at r = L\*
(**C13**) and the linear one is `(r/L*)²` of the Newtonian one. So the k⁴ mode supplies that correction,
not the law. **The law is first order** — the charge `d` and the potential `W(u)` in the lapse equation —
and has nothing to do with the `p⁴` sector. The mode cannot be the MOND mediator.

---

## 5. Checks (`a69_checks.py`, 56/56 PASS, exit 0, 1.6 s)

```
S1   FDiff invariance, 4 (eta,gamma) pairs, |dS|/S                        9.698e-05
S1b  residual does not grow when eta != gamma (off/same)                  1.1087789348
S2   quadratic scaling of the FDiff residual (lam halved)                 3.9961375993
S3   the four pairs give four distinct c_T^2                              4
S4   shift variation = -a0|c| per unit volume                            -2.055043e-34
S5   the shift variation is nonzero                                      1.0
S6   d^2W/dP^2 at P=0 equals K                                           8.4305653558e-56
S7   Weyl exponents (E^2, (D.P)^2, F^2, clock) = (2w,2w,2w,w+2)           8.88e-16
S8   min_w max|exponent|: no w is Weyl flat                              2.0
S9   gamma/eta is Weyl invariant                                         0.0
S10  on-shell conservation residual, 4 pairs                             7.5203732304e-17
S11  d_tT00+d_iT0i = Pdot.EOM (independent evaluation)                   7.5203732304e-17
O1   c_T^2 = gamma/eta = m_T^2 L*^2/2, two routes                        5.9371406479e-01
O3   w = p/rho scales linearly in eps (dust at O(eps))                   10.0
O4   elastic speed = 0.7204 m/s (A16/A20: 0.72)                          1.0005035864
O5   c_s=0 growth = exact LCDM growth function                           7.8798518436e-01
O6   1-S ~ k^2 in the weak-pressure limit                                3.9968874879
O7   the quoted bound reproduces S=0.95 at k=0.2                        1.9162e-07
O7b  the same criterion at k=0.5                                         3.0659e-08
O8   lambda_C = L*/sqrt(2 c_T^2) identity                                38.77 kpc
O9   sigma_c = sqrt(a0 L*) in km/s                                       8.3256628074
O10  growth with the elastic speed is un-suppressed                      1.0000000000
O11  k_J ~ sqrt(rho): cluster/mean ratio                                 31.622776602
O12  dark-sector w at recombination scales as (1+z)^3                    1.3346333010e+09
O13  d(omega^2)/dk^2 = 1 for the TT mode                                 1.0
O14  P-background graviton mass vs the 1.2e-22 eV bound                  3.6930937180e+11
O15  loop correction to c_T^2                                            6.6702392299e-144
O16  Delta N_eff for two thermalized bosonic modes                       5.9325993185e-01
G1   Pi_gamma/Pi_W = (1-x)L*^2/r^2 = 1/2 at r = L*                       0.5
G2   gradient-sector quadrupole/trace vanishes for P ~ x                2.4368837598e-11
G3   computed quadrupole = -gamma d (P'-P/r)(n_i n_j - delta/3)          2.6131531221e-11
G3b  charge-sector quadrupole scales as eps^2                            4.0
G4   c_T^2(TT) at gamma/eta = 1e-3                                       1.0
G4b  c_T^2(TT) at gamma/eta = 100                                        1.0
G5   alpha_1 = 2r^2/L*^2 = r^2 K/gamma                                   8.1614929337e-14
G6   alpha_1 is eta-independent                                          1.0
G7   alpha_1 ~ 1/gamma (gamma varied 4x)                                 4.0
G8   momentum density j_P = 0 for E=0, three eta values                  0.0
G9   healthy (Z, omega^2, m_T^2 > 0) on 24 (beta, gamma/eta) points      24
G10  eta_max = beta K/(2 a0^2) inverted back                             1.0
G11  three widely spaced gamma/eta survive all four gates                3
C1a  UV limit c_s^2 = alpha/eta at gamma/eta = 0.37                      0.37
C1   UV limit at gamma/eta = 1                                           1.0
C1b  UV limit at gamma/eta = 100                                         100.0
C2   two independent routes to p_sc (IR branch)                          2.8360269860e-69
C3   degeneracy check of the two routes                                  1.0
C4   the two branches agree within a factor 2 at eta = gamma             0.70710678119
C5   p_sc/(M_L^3/(M_Pl a0)) = 2/(3 sqrt pi)(K/2B)^{3/2}                  1.1894160774e-02
C6   p_sc/H0                                                             1.8993154319e-36
C7   p_sc/a0                                                             1.3800329188e-35
C8   p_sc/(1/L*)                                                         1.0643529686e-44
C9   largest loop factor over the astrophysical range                    1.9044908569e-70
C10  nabla^2(-r/8pi) = -1/(4 pi r) pointwise                             4.5171295593e-09
C11  unit flux: nabla^4(-r/8pi) = delta^3(r)                             1.0000001102
C12  d(-G)/dr = 1/(8 pi): constant force                                 1.0
C13  linear/Newtonian = (r/L*)^2 = 1 at r = L*                           1.0
C14  p_sc a0 = const across the three a0 footings                        5.8281573984e-103
```

Nine mutations, each changing one input and exiting 1 (§`MUTATE.md`): `eta_eq_gamma` (S3),
`no_W` (S4, S5, S6), `gamma_factor2` (O1, O4, O8, G1, G5, G7, C2, C3, C6–C8), `alpha_zero` (C1a–C1b,
C2–C9), `alpha_neq_gamma` (C1a–C1b, C2, C3, C6–C8), `wrong_dispersion` (S10, S11), `no_pressure`
(O6, O7, O7b), `weyl_flat` (S7), `c_s_elastic` (O4).

---

## 6. What this does not do, and where it touches A54 / A68 / A33

* **No contradiction with A68.** Everything here assumes A68's derived coefficients and confirms its
  central claim (`η ≠ γ` allowed); §1 is the symmetry-theoretic counterpart of its Jacobian argument.
* **No contradiction with A54**, but one refinement: A54's G4 lists the anisotropic stress as
  `Π = uW'(u)` only. The gradient sector contributes a quadrupole `γd(P'−P/r)` of the *same order* at
  r ~ L\* (ratio 0.5000 at u = a₀/2). Both are O(ε²), so A54's conclusion `Φ = Ψ` at O(ε) and the bound
  `(Φ−Ψ)/Ψ ≤ 3.945e-07` stand; the coefficient is at most 1.5× A54's.
* **Against A33's table**: the entry "`η ≥ γ` (scalar luminality)" is an *inequality imposed by hand*
  (the requirement `c_T ≤ c`), not something the action forces. The action forces `α = γ` (one stiffness)
  and nothing else. The task's premise that "γ/η is the P medium's sound speed" is true of the transverse
  modes and **false of the dark mass**, whose pressure is `γρ_c` — that identification is the substance
  of §2.2.
* **The overall normalisation of the stress tensor** for the `(D·P)²` term is not re-derived from the
  connection variation. §3(i) uses only its derivative structure — which is what fixes the ε² scaling,
  the vanishing for P ∝ x, and the absence of η. An overall factor (up to 3) would not change any
  conclusion, and the 0.72 m/s elastic speed (which does depend on the normalisation) is confirmed
  independently to 5e-04.
* **No Boltzmann code.** The growth suppression is a Newtonian fluid calculation on a ΛCDM background;
  the CMB statement is structural (no coupling, dust equation of state), not a transfer-function run.
* **The strong-coupling coefficient carries the usual O(1) scheme ambiguity** (the 1/3 in the cubic, the
  144π² in the loop, the IR/UV branch): the two branches differ by √2 (**C4**). At 36 orders of margin this
  is irrelevant to the conclusion, but `p_sc = 2.8e-69 eV` should be read as "order 10⁻⁶⁹ eV", not as
  three significant figures.
* **`p_*` and `subluminality` are not derived**: `p_* = √(B/η)` is a crossover, and `c_T ≤ c` is a choice.

---

## 7. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A69_psector_sound
python3 a69_checks.py --json-out a69_results.json > a69.out      # 56/56, exit 0
python3 a69_checks.py --mutate eta_eq_gamma                      # exit 1 (S3)
```

---

## 8. VERDICT

**Nothing in the action fixes η = γ, and nothing in the data constrains it either — the two facts have the
same root: γ/η is not the dark medium's sound speed.** The symmetry search comes up empty in all four
channels, each with a computed obstruction rather than an assertion: the P action is invariant under
foliation-preserving diffeomorphisms for arbitrary (η,γ) — |ΔS|/S ≤ 9.698e-05 at λ = 0.02 with a clean λ²
scaling (3.996) and no growth of the residual when η ≠ γ (1.109) — because `E_i` is a covector and the
gradient operators are scalar densities, so the variation is `η·0 + γ·0`; there is no constant-shift
symmetry, since `W` gives δS = −a₀|c| = −2.0550429975e-34 per unit volume, i.e. a mass `d²W/dP² = K`;
Weyl invariance is not a symmetry at all (the three derivative operators carry weight 2w, the clock term
w+2, `min_w max|exponent| = 2`) and could not fix a ratio anyway because all three share one weight; and
conservation is the Noether identity `∂_tT⁰⁰+∂_iT⁰ⁱ = Ṗ·EOM`, satisfied to 7.52e-17 for every (η,γ). The
only real handle is `c_T² = γ/η = m_T²L*²/2` with γ pinned by the fitted L\* and η free, so the sound speed
is measured by the range of the P-mediated force and by nothing else. **Observationally: UNCONSTRAINED**,
with the reason computed — the P sector's O(ε) stress is dust (w ∝ ε, a factor 10 per decade), its
pressure is the elastic `γρ_c` whose speed is 0.7204 m/s (A16/A20's 0.72, to 5.0e-04) and not
`√(γ/η)` (10⁸ m/s at η = γ; ratio² 1.732e+17), the CMB has no P–baryon coupling, and the graviton TT speed
is exactly 1 with a P background giving only a 3.249e-34 eV mass. If one nonetheless posits the medium's
pressure to be `c_T²ρ`, linear growth gives **γ/η < 1.916e-07 at 95 % CL** (3.0659e-08 at k = 0.5 h Mpc⁻¹)
and hence a P-mode Compton wavelength **> 38.77 kpc** instead of 16.971 pc. **All four gates survive
γ/η ≠ 1 and none of them fixes it**: (i) exact at O(ε) with γ entering only at O(ε²) through the measured
L\* and η not at all (Π_γ/Π_W = 0.5000 at r = L\*); (ii) exact for every γ/η; (iii) `α₁ = 8.161493e-14`
at 1 AU is η-independent and `α₂ = 0` because `j_P(E=0) = 0`; (iv) the Hamiltonian is bounded for
β > 0, γ > 0, η > 0 — i.e. **γ/η > 0**, with the principal-positivity bound translating to the vacuous
γ/η > 5.948e-19, and 24/24 grid points healthy. **The gapless k⁴ mode is weakly coupled everywhere**:
p_sc = K²/(8.485π a₀ α^{3/2}) = 2.8360e-69 eV, i.e. 1.899e-36 H₀, 1.380e-35 a₀ and 1.064e-44 of 1/L\*, with
the largest loop factor over CMB/LSS/galactic scales equal to 1.904e-70 — so the EFT needs no cutoff below
the horizon, and the mode is not the MOND mediator, because its static Green's function is −r/(8πα): a
linear potential and a constant force, the `μr/L*²` term of A22's exact solution, not the law.
