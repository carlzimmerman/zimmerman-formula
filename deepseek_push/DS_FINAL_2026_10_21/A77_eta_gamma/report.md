# A77 — DOES THE MEDIUM'S OWN THERMODYNAMICS FIX ITS SOUND SPEED?

**Lane:** A77_eta_gamma · **Date:** 2026-10-22
**Base read:** `A69_psector_sound/report.md` (nothing in the action forces η = γ; `c_T² = γ/η = m_T²L*²/2`;
the P stress is dust at O(ε); the elastic pressure speed is `√(γρ_c) = 0.7204 m/s`, **not** `√(γ/η)`; the data
are UNCONSTRAINED; *if* the pressure were `c_T²ρ`, then `γ/η < 1.916e-07` at 95 % CL), `A68_bracket_algebra/report.md`
(`Z = K(2+3β)/β + ηp²`, `m_T² = K/η`, `c_T² = γ/η`, `α = γ` forced, the gapless `k⁴` mode), `A16_cutoffs_edge/report.md`
(the Γ = 2 polytrope: `c_s² = γρ_c`, `λ_J = √2πL*`, `M_J` at the switch, the 0.7204 m/s speed), `A63_saturating_medium/report.md`
(the Langmuir gate), and `A72_coefficient/` (the thermal footing `a₀ = cH_Λ/2π`).
**Script:** `a77_checks.py` — **40/40 PASS, exit 0, 1.3 s** · **Output:** `a77.out` · **Data:** `a77_results.json`
· **Mutations:** `MUTATE.md` (10 dials, each exit 1, each breaking a named check).

Units: `K = 4πG = 8.4305653545e-56 eV⁻²`, `c = 1`, signature (−+++). `a₀ = 9.36e-11 m/s² = 2.055043e-34 eV`,
`L* = 24 pc = 3.752972e+24 eV⁻¹`, `γ = α = KL*²/2 = 5.9371406479e-07 eV⁻⁴`, `ρ_c = 9.724900e-12 eV⁴`,
`H₀ = 67.4 km/s/Mpc` (so `H_Λ = 1.189667e-33 eV`), `T_dS = ħH_Λ/2πk_B = 1.893413e-34 eV = 2.1972e-30 K`.
Every number below is printed by `a77.out`; the external anchors taken from the record (A16's
`0.519081 m²/s²`, `0.720473 m/s`, `0.0212 M☉`; A69's `0.9737`; A51's `κ = 0.371 ± 0.119`; A29's and A18's
cluster scales) are inputs of the script and appear in its output.

---

## 0. The answer in one paragraph

**The closure is not forced, and in the form the task states it is not even consistent.** The first half of it
is a derivation: the transverse quadratic action gives `ω² = (K + γk²)/η`, so `c_T² = lim ω²/k² = γ/η`
exactly, with the gap `K/η` fixed by `W''(0) = 1/K` (K1–K5). But that is a **stiffness-over-inertia** ratio, not
`dP/dρ`: the medium's own thermodynamic speed comes from the Γ = 2 polytrope, `c_s,el² = dp/dρ = γρ_c =
5.773810e-18`, i.e. `0.720364 m/s` (A16's `0.720473`), and the two coincide **iff** `ηρ_c = 1` — the closure
needs `ηρ_c = 7.486283e-09`, a factor `1.335776e+08` away (K6–K11). The second half fails on its own arithmetic:
with `m_P = ħ/(cL*)` and `T_dS`, three-dimensional equipartition gives `3k_BT_dS/m_P = 2.764049 σ_c²`, i.e.
**13.8418 km/s, not 8.3257**; forcing it to equal `σ_c² = a0L*` would *predict* `a0 = 3cH_Λ/2π = 2.587150e-10 m/s²`,
i.e. `κ = 1.143542`, **6.49σ** from A51's `0.371 ± 0.119` (K12, K15, K16). What the numbers do satisfy is the
**per-dof** relation `k_BT_dS/m_P = 0.921350 σ_c²`, which is *exactly* the A72 thermal footing
`a0 = cH_Λ/2π = 8.623833e-11` (declared `8.620e-11`, K13, K14) — so the candidate's numerical success is a
known identity of the record, not a thermodynamic law. And the premise is thermodynamically impossible:
`m_P/T_dS = 1.407276e+09`, so the P field's equilibrium occupation `e^(−m_P/T_dS)` underflows to zero; equilibrium
would need `L* = 2π/H_Λ = 3.377462e+10 pc = 33.77 Gpc`, i.e. `1.407e+09 L*` (K17, K18). **Adopted anyway**, the
closure gives `γ/η = (σ_c/c)² = 7.712519e-10`, `η = 769.8057 eV⁻⁴`, `m_T = 1.046497e-29 eV`, `λ_C = 611.0801 kpc`,
which is **248.43×** below A69's bound and passes everything — growth `S(0.2) = 0.999795`, `S(0.5) = 0.998718`,
Jeans `1.232290 Mpc` / `3.266079e+10 M☉` at the cosmic mean, half-mode at `k = 11.1632 h/Mpc` — because passing a
*one-sided* bound by 2.4 decades is not evidence. `611.0801 kpc` matches no measured scale (ratios `0.4322`,
`0.5738`, `0.3624`, `0.5908` to A29's splashback, A29's `u = 1/2` crossing, A18's `r_v` and A29's `R_200c`), and
structurally it *cannot*: A69's static sector is η-independent, so the law has no Yukawa range to cut off. In the
other direction the medium's actual pressure is elastic — `ρσ²/p_el = 1.335776e+08`, `c_T/c_s,el = 1.1558e+04` — so
**0.7204 m/s governs structure formation and `γ/η` governs nothing**. Verdict **(b): still free**; the missing
principle is a matching condition for the kinetic coefficient η.

---

## 1. Task 1 — the equation of state

### 1.1 `c_T² = γ/η` from the action, symbolically

At quadratic order on flat space (`N = 1`, `N^i = 0`), and for a **transverse** configuration `D·P = 0`, the
`(α/2)(D·P)²` term vanishes and `F_ijF^ij = 2(∂P)²`, so the frozen action reduces to one component of

```
L_T = (η/2) Ṗ² − (γ/2)(∇P)² − (K/2) P²          [the mass term from W''(0) = 1/K]
```

The Euler–Lagrange equation computed by sympy from exactly this Lagrangian is
`K·P + η·P̈ − γ·P'' = 0`, and the plane-wave ansatz gives

```
ω²(k) = (K + γk²)/η        ⇒     c_T² ≡ lim_{k→∞} ω²/k² = γ/η ,      m_T² ≡ ω²(0) = K/η .
```

Four independent evaluations agree: the E-L equation against the closed form (K1, residual 0), the symbolic
limit against the ratio `γ/η` (K2), the gap against `K/η` with `d²W/dP²|₀ = K` from the `W` series (K3, K4,
residual 0), and a finite-difference slope of `ω²(k)` at `k = 50, 51` against `γ/η` (K5, `1.54e-15`). Nothing
here is new relative to A68 §3.2 — the point of re-deriving it is that the *identification* below can then be
separated from the *derivation*.

### 1.2 Why `c_T²` is not `dP/dρ`

`c_T² = γ/η` is the coefficient of `k²` in a massive dispersion: the high-`k` phase/group speed, i.e. the
light cone of the P sector, or equivalently the ratio of the gradient stiffness `γ` to the inertia `η`. It is
*not* a thermodynamic derivative. For a homogeneous P configuration the stress is

```
ρ = (η/2)Ṗ² + (K/2)P² ,      p = (η/2)Ṗ² − (K/2)P² ,
```

so `p/ρ` runs from −1 (at rest) to +1 (kinetic domination) and `dp/dρ` is not `γ/η` anywhere: the mass term
enters `p` and `ρ` with *opposite* signs, which is precisely what a gap does and what a `p = c_T²ρ` fluid does
not. `c_T²` is the transverse (shear) speed of an elastic medium with modulus `γ` and inertia `1/η`.

### 1.3 The medium's actual thermodynamic speed

The action's *longitudinal* gradient operator is the same `γ`, and through `D·P = δρ_c` it **is** an equation of
state (A16 §1). Sympy, from `e = (γ/2)(ρ_c − ρ̄_c)²` and `p = ρ de/dρ − e`:

```
p = (γ/2)(ρ² − ρ̄²) ,      c_s² = dp/dρ = γρ        (K6, exact)
```

At `ρ_c = 9.724900e-12 eV⁴`: `c_s,el² = 5.773810e-18` and `c_s,el = 0.720364 m/s`, against A16's published
`0.519081 m²/s²` and `0.720473 m/s` (K7 `3.02e-04`, K8 `1.51e-04` — the difference is the record's rounding of
`ρ_c`). **This is the medium's thermodynamic sound speed**, and it is `1.1558e+04` times smaller than `σ_c`.

### 1.4 What the `(η, γ)` pair corresponds to

The pair is the elastic-solid pair, `c_T² = μ/ρ_inertia` with `μ = γ` and `ρ_inertia = 1/η`. The comparison
with the three standard media is then immediate, and it is the answer to "which relation the action's pair
corresponds to":

| medium | `c_s²/σ²` at `σ² = 3k_BT/m` | `c_s` vs `T` | is `c_T = σ` an identity? |
|---|---|---|---|
| 3D ideal gas, adiabatic (5/3) | 5/9 = 0.555556 | `∝ √T` | no, off by 5/9 |
| 3D ideal gas, isothermal | 1/3 | `∝ √T` | no, off by 1/3 |
| collisionless (Jeans/Vlasov) | 1 | `∝ √T` | **yes** — but the pressure is `ρσ²`, no `η` anywhere |
| 3D harmonic solid (this medium) | no universal value; `σ/c_s ≈` Lindemann ≈ 0.1 at melting, and `c_s` is `T`-independent while `σ ∝ √T` | `T`-independent | **no, and not even a fixed number** |

So the action's `(η, γ)` corresponds to the **last row**: a solid, for which the wave speed and the thermal
dispersion are independent quantities whose ratio is set by the lattice (the Lindemann ratio), not by
thermodynamics. The proposed `c_T = σ_c` is the *third* row's relation — the collisionless one, where the
"sound speed" is just the velocity dispersion and the stiffness is `ρσ²`, not `γ`.

The two speeds are related by one dimensionless combination. Directly from the definitions,

```
c_T²/c_s,el² = (γ/η)/(γρ_c) = 1/(ηρ_c)        (K9, to 1.12e-16;  = 1.335776e+08 here)
```

and since `[η] = eV⁻⁴` while `[ρ] = eV⁴`, `ηρ_c` is the *only* dimensionless number available: the
hydrodynamic matching is `ηρ_c = 1` (the canonical momentum of `P` is the mass current), and it makes the two
speeds equal **exactly** (K10). That is the medium's own thermodynamics fixing its sound speed — at
`0.720364 m/s`. The closure instead needs `ηρ_c = 7.486283e-09` (K11), i.e. an inertia `1.335776e+08` times *smaller*
than the medium's density, with nothing in the action or the EOS to supply that.

### 1.5 The equipartition step

Three things are wrong with it, in increasing order of severity.

**(a) The coefficient.** With `m_P = ħ/(cL*) = 1/L* = 2.664555e-25 eV` and `k_BT_dS = 1.893413e-34 eV`,

```
3 k_B T_dS/m_P = 2.764049 σ_c²        ⇒  σ_th = 13.8418 km/s, not 8.3257
k_B T_dS/m_P   = 0.921350 σ_c²        ⇒  σ   = 7.9916 km/s
```

(K12 versus the closed form `3√(32π/3)/(2π) = 2.763953`, K13 versus `√(32π/3)/(2π) = 0.921318`). So the
task's stated relation `σ_c² = 3k_BT_dS/m_P` is **false by 2.764** with the record's own `a₀`, `L*`, `T_dS`.
The statement is not innocent: combined with the *definition* `σ_c² = a0L*` it is a **prediction for `a₀`**,

```
a₀ = 3cH_Λ/2π = 2.587150e-10 m/s²      ⇒   κ = a₀/(2.2624e-10) = 1.143542 ,
```

which is **6.49σ** from A51's `κ = 0.371 ± 0.119` (K15, K16). The 3-dof version of the closure is therefore not
"unforced" — it is **excluded**.

**(b) The identity behind the near-miss.** The per-dof row is not an accident: `a₀ = cH_Λ/2π` is the A72
thermal footing, and at that footing `k_BT_dS/m_P = a0L*` *identically* (both are `H_ΛL*/2π`). Computed:
`cH_Λ/2π = 8.623833e-11 m/s²` against the declared `8.620e-11` (K14, `4.45e-04`). So the candidate closure's
numerical agreement with `σ_c` **is** the A72 relation, with an 8.54 % offset from the canonical `a₀`; it is not
a statement about `η` at all, and it does not survive being written with the coefficient 3 that the task states.

**(c) The premise is impossible.** A particle of mass `m_P = 1/L*` in a bath at `T_dS = H_Λ/2π` sits at

```
m_P/T_dS = 2π/(H_ΛL*) = 1.407276e+09        ⇒   e^(−m_P/T_dS) = 0.000e+00  (underflow)
```

(K17). It is `1.407276e+09` times heavier than the de Sitter temperature; it has no thermal population, and
(there being no P–baryon or P–photon coupling, A69 §2.2) no channel to acquire one. Equilibrium at `T_dS` would
require `m_P ≲ T_dS`, i.e. `L* ≳ 2π/H_Λ = 3.377462e+10 pc = 33.77 Gpc` — the thermal wavelength at `T_dS`, and
`1.407e+09` times the fitted `L*` (K18). **The medium is not, and cannot be, in equilibrium at the de Sitter
temperature.** This is the same fact as A69's `ΔN_eff = 0.5933` for two thermalized bosonic modes, seen from the
other side: the modes must be unpopulated, and they are.

### 1.6 What is forced, what is identified

| statement | status | number |
|---|---|---|
| `ω² = (K + γk²)/η`, `c_T² = γ/η`, `m_T² = K/η` | **DERIVED** (E-L of the frozen action) | K1–K5 |
| `c_s,el² = dp/dρ = γρ_c` | **DERIVED** (Γ = 2 polytrope, A16) | `5.773810e-18`, `0.720364 m/s` |
| `c_T = c_s,el` | identity **iff** `ηρ_c = 1` — the hydrodynamic matching, dimensionally forced | K9, K10 |
| `c_T = σ_c` | **IDENTIFICATION**, no derivation; O(1) band `c_T²/σ² ∈ [1/3, 1]` | below |
| `σ_c² = 3k_BT_dS/m_P` | **FALSE** by 2.764; implies `a₀ = 2.587150e-10`, 6.49σ | K12, K15, K16 |
| `σ_c² = k_BT_dS/m_P` | true but **= the A72 footing**, not equipartition of a 3-component field | K13, K14 |
| the P medium in equilibrium at `T_dS` | **FALSE**: `m_P/T_dS = 1.407276e+09` | K17, K18 |

The O(1) band of the identification, computed:

```
c_T²/σ² = 1/3 :  c_T = 4.8068 km/s ,  γ/η = 2.570840e-10 ,  λ_C = 1058.4218 kpc
c_T²/σ² = 5/9 :  c_T = 6.2056 km/s ,  γ/η = 4.284733e-10 ,  λ_C =  819.8500 kpc
c_T²/σ² = 1   :  c_T = 8.3257 km/s ,  γ/η = 7.712519e-10 ,  λ_C =  611.0801 kpc
```

a span of `√3 = 1.732051` in `λ_C`. Note that **every** member of the band is on the cluster scale, so the
identification's O(1) ambiguity is not what decides the phenomenology — the identification itself does.

---

## 2. Task 2 — consistency with the data

### 2.1 The numbers

With `γ/η = (σ_c/c)² = 7.712519e-10` (from `a0L*`; `7.7206e-10` if one uses the rounded `8.33 km/s`, K19 at
`1.04e-03`),

```
η    = γ/c_T² = 769.8057 eV⁻⁴        (= K/m_T², K20)
m_T  = √(K/η) = 1.046497e-29 eV      (m_T/H₀ = 7278.85)
λ_C  = √(η/K) = 611.0801 kpc = 6.110801e+05 pc = 2.5462e+04 L*   (= L*/√2c_T, K21; the task's 612 kpc to 0.2 %, K22)
ηρ_c = 7.486283e-09
```

The P-mode Compton wavelength is `2.5462e+04` times `L*` and `7.4205` times the free-streaming length that A16 assigns
to `σ_c` (`82.35 kpc`, K33).

### 2.2 Growth of structure

The growth integration is the same as A69's (RK4 in `ln a`, `Ω_m = 0.3153`, `h = 0.674`, from `a = 10⁻³`); it is
validated three ways — `c_s = 0` reproduces the exact ΛCDM growth function to `8.67e-10` (K25), `c_s² = 1e-7`
reproduces A69's published `S(0.2) = 0.9737` to `4.35e-05` (K26), and the fixed-step result agrees with an
adaptive DOP853 integration to `1.78e-15` (K27). With `c_s² = 7.712519e-10`:

| k (h/Mpc) | 0.2 | 0.5 | 3 | 5 | 10 |
|---|---|---|---|---|---|
| `S = D(k)/D(0)` | **0.999795** | **0.998718** | 0.95463 | 0.87794 | 0.57902 |

`1−S ∝ k²` holds to `4.20e-04` (K28: `6.247` against `6.25`), and the half-mode is at
`k_1/2 = 11.1632 h/Mpc`, `λ_1/2 = 0.08958 h⁻¹ Mpc` (K29). For contrast, at `η = γ` (`c_T = c`) the same
solver gives `S(0.2) = 1.045e-35`: **the closure is what makes the P medium cold enough to be viable at all**,
which is worth stating because it is the one place where the candidate *improves* the theory's consistency.

Against A69's bound: `γ/η = 7.712519e-10 < 1.916e-07`, a margin of **248.43** in `c_T²` and the same 248.43 in
`η` (K24, two routes), i.e. the suppression at `k = 0.2` is `0.02 %` where the bound was defined by `5 %`.

**Is that "consistent"? Only in the weak sense.** The bound is one-sided and sits 2.4 decades above the
candidate, so it also admits `γ/η = 5.773810e-18` (the hydrodynamic value, §3) and every value in between: passing
it discriminates nothing. The genuinely sharp statement the closure makes is the half-mode at
`k = 11.2 h/Mpc` — a `50 %` suppression at `k = 11 h/Mpc` and `12 %` at `k = 5 h/Mpc` would be visible in the
Ly-α flux power, which is measured out to `k ≈ 20 h/Mpc`. That comparison needs a transfer-function run and is
**not** done here; the honest status is **testable, not tested**.

### 2.3 The cluster-scale Jeans mass

```
at ρ_c :      λ_J = 1.232290 Mpc ,   M_J = 3.266079e+10 M☉      (K30, K31)
at 200 ρ_c :  λ_J = 87.1361 kpc  ,   M_J = 2.309467e+09 M☉
```

So a `c_T = 8.33 km/s` P-medium is a warm-ish dark component: its power is un-suppressed on every linear scale
(`S(0.2) = 0.999795`, `S(0.5) = 0.998718`) and it turns over only at `k_1/2 = 11.1632 h/Mpc`, i.e. sub-galactic
scales. That is not excluded by the cluster data, and it is not selected by them either.

### 2.4 Does `611.0801 kpc` show up somewhere already measured?

No — and the census is worth stating because it is the only thing that could have turned the identification
into a measurement. Against the record's own scales:

| scale | value | `λ_C`/scale |
|---|---|---|
| A29 splashback of the cluster stack | 1.414 Mpc | **0.4322** |
| A29 `u = 1/2` crossing | 1.065 Mpc | **0.5738** |
| A18 `r_v` (cluster stack) | 1.6863 Mpc | **0.3624** |
| A29 `R_200c` (`r_sp/1.367`) | 1.0344 Mpc | **0.5908** |
| A16 free-streaming length at `σ_c` | 82.35 kpc | **7.4205** |

(K32: the minimum `|ratio−1|` is `0.4092`, i.e. no scale is within 30 %.) A search of the lane reports finds no
600-kpc number anywhere in the record.

But the stronger statement is structural, and it kills the hope of a measurement rather than merely reporting a
miss. `λ_C` is the range of the **transverse propagating** P modes. The **law** is mediated by the static
sector — the charge `d = D·P`, the potential `W(u)` and the lapse constraint — which contains no time
derivative; A69's G5/G6 compute exactly that: `α₁ = 2r²/L*²` at 1 AU is **η-independent**, and `α₂ = 0` because
`j_P(E = 0) = 0`. A constraint sector has no mass and no range: the anomaly is Coulomb-like for every `η`. So
`611.0801 kpc` is not "the range of the P-mediated force" in the sense that a cluster lensing profile could
measure; it is the range of two modes that have no source, no coupling, and (A69 O16) cannot be thermally
populated. **A 611 kpc Compton wavelength cannot show up in any existing measurement of the dark sector.**

---

## 3. Task 3 — the other direction: the pressure is elastic

### 3.1 The elastic Jeans scales

With `c_s,el² = γρ_c`, the dispersion `c_s²k² = 4πGρ_c` gives `k_J = √2/L*` — **density-free**, because both
`c_s²` and `4πGρ` carry one power of `ρ_c`. Two routes agree (`K34`, closed form against a Brent root, `1.67e-14`;
`K35` against `√2πL*`, `6.89e-05`), and the density-independence is verified at `ρ_c` and `200ρ_c` (`K37`,
ratio 1 exactly; the `c_T` version scales as `√200 = 1.4142135624e+01`, `K38`):

```
λ_J,el = √2πL* = 106.6218 pc
M_J,el(ρ_c) = 2.115564e-02 M☉          (A16's 0.0212, K36)
```

A16's own evaluation at the switch density (`4.9609 M☉/pc³`, flat-curve profile) gives `M_J = 5.565e8 M☉`
inside `R_TF = 53.31 pc` — the ultra-compact-dwarf class. Note the inversion: `M_J,el ∝ ρ_c` while `M_J(c_T) ∝ ρ_c^{−1/2}`, so at cluster
densities the two readings differ by five orders in the *opposite* direction from the mean-density comparison.

### 3.2 The fork: which velocity is the pressure?

```
ρ_c σ_c² / p_el = σ_c²/c_s,el² = 1.335776e+08        ⇒   c_T/c_s,el = 1.1558e+04        (K39)
```

A medium cannot have both. Either

* **(i) it is a solid**, the pressure is `p = (γ/2)(ρ² − ρ̄²)`, `c_s = 0.720364 m/s` governs the Jeans scale and
  the growth, and `σ_c = 8.33 km/s` is not a thermal dispersion at all — it is a *virial* velocity,
  `σ_c² = a0L*` being the circular speed squared at the MOND radius; or
* **(ii) it is collisionless**, the pressure is `ρσ²`, `8.33 km/s` governs, and the elastic EOS is `1.335776e+08` times
  subdominant, i.e. irrelevant.

The record's reading is (i): A69's O10 gives `S = 1.0000000000` for growth with `c_s,el`, and A16's Jeans chain
is built on (i). Under (ii) the same growth numbers as §2.2 appear — but the pressure is `ρσ²`, which contains
**no `η`**: `γ/η` does not enter the Euler equation in either reading. Even in the collisionless reading, where
`c_T = σ_c` numerically, the physics that governs structure formation is `σ_c`, not `γ/η`.

So: **the velocity that governs structure formation is `0.720364 m/s`** (the record's own reading), and
`8.3257 km/s` enters only through free-streaming (A16's `82.35 kpc`) and only if `σ_c` is a dispersion — which
is exactly the assumption the elastic EOS denies.

### 3.3 What, if anything, sees `γ/η`?

Only the dispersion of the two transverse P modes: their mass `m_T = 1.046497e-29 eV` and their speed
`√(γ/η)`. They are (a) unpopulated — `e^(−m_P/T_dS)` underflows, and A69's `ΔN_eff = 0.5933` for two
thermalized bosonic modes is excluded by Planck's `ΔN_eff < 0.34`; (b) uncoupled — no `P·J`, no `P·F_μν`
(A22/A33); and (c) unsourced — no production mechanism and `P = 0` on FRW. A quantity with no population, no
coupling and no source has no observable. That is the precise reason A69 found the data UNCONSTRAINED, and the
closure does not change it: fixing a number that nothing reads is not a prediction.

---

## 4. Task 4 — verdict

**(b) Still free.** Not (a): the thermodynamics does not fix `γ/η`, it fixes a *different* speed
(`c_s,el² = γρ_c = 5.773810e-18`, `0.720364 m/s`), and the only dimensionally natural matching of the inertia to
the medium (`ηρ_c = 1`) makes the two coincide *there*, not at `σ_c`. The identification `c_T = σ_c` has an O(1)
band `c_T²/σ² ∈ [1/3, 1]` (1058.4218 → 611.0801 kpc in `λ_C`) and no principle selects a member. The one
quantitative version the task states (`3k_BT/m_P`) is **excluded at 6.49σ** through its implied `a₀`, and its
premise (`m_P` in equilibrium at `T_dS`) is impossible by `1.407276e+09` in `m_P/T_dS`.

Not (c) either, strictly: (c) would require that the identification is *forced* and only its consequence
unobservable. It is not forced. What is true is the weaker pair of statements: `γ/η` **is** unobservable in the
dark sector (the static sector is η-independent and the transverse modes are empty), and *if* one adopts
`c_T = σ_c` the resulting `λ_C = 611.0801 kpc` still has no observable consequence.

**The missing principle, named exactly.** `η` is the coefficient of `(η/2)E_iE^i` — a *kinetic* coefficient, an
inertia. The medium's thermodynamics supplies only `ρ_c`, `p(ρ_c)`, `T_dS` and `m_P`; it says nothing about
`η`. What is required is a **matching condition (a Kubo/transport relation) for the P field's inertia**:

```
η⁻¹  =  lim_{ω→0} (1/ω) ∫dt ⟨[P_i(t), P_j(0)]⟩  —  or, in the hydrodynamic limit,  η = 1/ρ_c ,
```

i.e. an identification of the P field's canonical momentum with a physical mass current of the medium. A72's
thermal-wavelength argument fixes `a₀`, not `η`; equipartition fixes `σ` given `m_P` and `T`, not `γ/η`. Until
such a relation exists, `γ/η` is a free coefficient of the frozen action, exactly as A68's Jacobian argument
said, and the honest prediction for `λ_C` is the whole range `(0, ∞)` consistent with A69's one-sided bound —
with the hydrodynamic corner `η = 1/ρ_c` giving `γ/η = 5.773810e-18`, `λ_C = 7.06 Gpc` and `c_T = 0.7204 m/s`,
and the candidate corner giving `611.0801 kpc` and `8.33 km/s`.

---

## 5. Checks (`a77_checks.py`, 40/40 PASS, exit 0, 1.3 s)

```
K1   omega^2 from the E-L equation of the transverse action = (K+gamma k^2)/eta    1.8000017647
K2   c_T^2 = lim omega^2/k^2 = gamma/eta (symbolic limit vs ratio)                 2.5294117647e-01
K3   mass gap omega^2(0) = K/eta                                                   1.7058823529
K4   d^2W/dP^2|_0 = K from the W series (gap vs K)                                 2.9000000000
K5   c_T^2 from the finite-difference slope of omega^2(k) at k=50,51               2.5294117647e-01
K6   sympy: dp/drho = gamma rho for the Gamma = 2 polytrope                        1.0000000000
K7   gamma rho_c = 0.519081 m^2/s^2 (A16 K8)                                       5.1892415565e-01
K8   elastic sound speed = 0.720473 m/s (A16 K8)                                   7.203639e-01
K9   c_T^2/c_s,el^2 = 1/(eta rho_c)                                                1.335776e+08
K10  eta = 1/rho_c => c_T = c_s,el (the hydrodynamic matching)                     5.773810e-18
K11  the closure's eta*rho_c = c_s,el^2/c_T^2 = 7.48e-9 (not 1)                   7.486283e-09
K12  3 k_BT/(m_P sigma_c^2) = 3 sqrt(32pi/3)/(2pi) = 2.76395                        2.764049
K13  k_BT/(m_P sigma_c^2) = sqrt(32pi/3)/(2pi) = 0.92116 (per-dof)                 0.921350
K14  cH_L/2pi reproduces the declared thermal footing 8.620e-11                     8.623833e-11
K15  dof*cH_L/2pi = 2.587e-10 m/s^2 (dof = 3)                                      2.587150e-10
K16  the 3-dof version is 6.49 sigma from A51's kappa                              6.491952
K17  m_P/T_dS = 2pi/(H_L L*) = 1.408e9                                             1.407276e+09
K18  L* at which m_P = T_dS: 2pi/H_L = 3.377e10 pc = 33.77 Gpc                     3.377462e+10
K19  (sigma_c/c)^2 from a0L* vs 7.7206e-10 from 8.33 km/s                          7.712519e-10
K20  eta = gamma/c_T^2 = K/m_T^2 (two routes)                                      7.698057e+02
K21  lambda_C = sqrt(eta/K) = L*/(sqrt2 c_T)                                       6.110801e+02 kpc
K22  lambda_C = 611 kpc (the task's 612 kpc, 0.2 %)                                6.110801e+02
K24  the closure sits 248x below A69's bound, in c_T^2 and in eta                  2.4842727464e+02
K25  c_s = 0 growth = the exact LCDM growth function (ODE vs integral)             7.8798518436e-01
K26  S(k=0.2) at c_s^2 = 1e-7 reproduces A69's table (0.9737)                      9.736576e-01
K27  S(k=0.2) at c_T = sigma_c: RK4 vs adaptive DOP853                             9.997947e-01
K28  1-S ~ k^2: (1-S(0.5))/(1-S(0.2)) = 6.25                                       6.247374
K29  half-mode 1/k_1/2 = 0.090 h^-1 Mpc (k_1/2 = 11.2 h/Mpc)                       8.957968e-02
K30  lambda_J = 2pi c_T/sqrt(4pi G rho) = 1.2323 Mpc                               1.232290
K31  M_J = (4pi/3)rho(lambda/2)^3 = pi lambda^3 rho/6 = 3.266e10 Msun              3.266079e+10
K32  no measured cluster scale sits at lambda_C (min |ratio-1| >= 0.30)            4.092316e-01
K32b the closure is allowed by A69's bound (gamma/eta < 1.916e-07)                 7.712519e-10
K33  lambda_C / lambda_FS(sigma_c) = 7.42 (A16's 82.35 kpc)                        7.420505
K34  elastic k_J: closed form vs numerical root of the dispersion                  1.000000
K35  elastic lambda_J = sqrt2 pi L* = 106.62 pc (density-free)                     1.066218e+02
K36  elastic M_J at the cosmic mean = 0.0212 Msun (A16)                            2.115564e-02
K37  dln(lambda_J,el)/dln(rho) = 0: 200x in density, same length                    1.000000
K38  the c_T Jeans length does scale: 200x density -> sqrt(200)                     1.4142135624e+01
K39  rho sigma_c^2 / p_el = (sigma_c/c_s,el)^2 = 1.336e8                            1.335776e+08
K40  T implied by the elastic speed = 2.71e-9 T_dS (a cold solid)                  2.708448e-09
```

Ten mutations, each changing one input, each exit **1** (`MUTATE.md`): `ct_light` (K22, K27–K29, K32b, K33),
`a0_thermal` (K12, K13, K19, K22, K29, K33), `rho_c_x2` (K7, K8, K36), `lstar_25` (K7, K8, K19, K22, K29, K33,
K36), `gamma_x2` (K7, K8, K21, K22, K32, K33, K35, K36), `soft_equipartition` (K12, K16), `no_pressure` (K26,
K28, K29), `no_shear` (K1, K2, K5), `eos_half` (K6–K11, K35, K36), `hlam_x3` (K12–K16). 26 of the 40 checks are
broken by at least one dial; the other 14 are two-route identities (symbolic derivation against closed form,
root-find against analytic formula, scaling laws), listed one by one in `MUTATE.md` with the route each
guards — no input dial can split them because both routes move together.

---

## 6. What this does not do

* **It does not derive `η`.** That is the point — no matching condition exists in the record, and nothing here
  manufactures one. The dimensional argument `η = O(1)/ρ_c` is offered as the *natural* corner, not as a
  derivation, and its `O(1)` is left open (`λ_C ∝ 1/√O(1)`).
* **It does not run a transfer function.** The Ly-α remark in §2.2 is a scale comparison
  (`k_1/2 = 11.1632 h/Mpc` against a forest measured to `k ≈ 20 h/Mpc`), not a bound; the growth calculation is
  Newtonian, on a ΛCDM background, with a single fluid.
* **`T_dS` uses `H_Λ` from `H₀√Ω_Λ`** (67.4 km/s/Mpc, 0.6847), not from the record's `Λ = 32πa₀²` identity; the
  two differ by `3.47e-05` in the ratio `3k_BT/m_Pσ_c²` (K12), which is why that check carries a looser tolerance
  than the rest. No conclusion depends on it.
* **The `c_T = σ_c` identification is not tested against any *new* observable**, because §2.4/§3.3 argue there
  is none. If a P–matter coupling were added, `λ_C = 611.0801 kpc` would become a fifth-force range and a
  cluster-scale Yukawa test would apply — that is a different theory (it would violate A69's dust statement).
* **The "3-dof excluded at 6.49σ" verdict is conditional on `σ_c² = a0L*`**, which is a definition in the record
  (A16 §2, A20/A65). Relaxing it would make the 3-dof version merely unforced rather than excluded; the
  Boltzmann objection (K17) survives either way.
* **`L*` is fitted** (A65) and everything here scales with it: `λ_C ∝ L*`, `σ_c ∝ √L*`. Nothing here predicts
  `L*`.

---

## 7. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A77_eta_gamma
python3 a77_checks.py --json-out a77_results.json > a77.out        # 40/40, exit 0
A77_MUTATE=ct_light python3 a77_checks.py                          # exit 1 (K22, K27-K29, K32b, K33)
A77_MUTATE=eos_half python3 a77_checks.py                          # exit 1 (K6-K11, K35, K36)
```

---

## 8. VERDICT

**No: the medium's own thermodynamics does not fix `c_T = γ/η`, and the specific closure proposed here is
wrong twice over before the identification is even reached.** The derivation half is solid and is reproduced
from the frozen action: the transverse quadratic Lagrangian `(η/2)Ṗ² − (γ/2)(∇P)² − (K/2)P²` has
`ω² = (K + γk²)/η`, so `c_T² = γ/η` exactly, with `m_T² = K/η` fixed by `W''(0) = 1/K` (K1–K5). But `γ/η` is a
stiffness-over-inertia ratio, not a `dP/dρ`: the medium's thermodynamic speed is the Γ = 2 one,
`dp/dρ = γρ_c = 5.773810e-18`, i.e. **0.720364 m/s** (A16's 0.720473), and the two speeds are related by
`c_T²/c_s,el² = 1/(ηρ_c)` (K9) — they coincide only under the hydrodynamic matching `ηρ_c = 1` (K10), while the
closure needs `ηρ_c = 7.486283e-09`, an inertia `1.335776e+08` times below the medium's density (K11). The
equipartition half is worse: `3k_BT_dS/m_P = 2.764049 σ_c²`, giving **13.8418 km/s, not 8.3257** (K12), and since
`σ_c² = a0L*` that version *predicts* `a₀ = 3cH_Λ/2π = 2.587150e-10 m/s²`, i.e. `κ = 1.143542`, **6.49σ** from
A51's `0.371 ± 0.119` — excluded, not merely unforced (K15, K16). The number that does come out right,
`k_BT_dS/m_P = 0.921350 σ_c²`, is *identically* the A72 thermal footing `a0 = cH_Λ/2π = 8.623833e-11` (K13,
K14), so the candidate's agreement is a known identity of the record read with the wrong dof count. And the
premise fails outright: `m_P/T_dS = 1.407276e+09` — the P particle is a billion times heavier than the de
Sitter bath, its equilibrium occupation underflows, and equilibrium would need `L* = 33.77 Gpc`
(`3.377462e+10 pc`), `1.407e+09` times the fitted value (K17, K18). Adopted anyway, the closure is *consistent*
but empty: `γ/η = 7.712519e-10`, `η = 769.8057 eV⁻⁴`, `m_T = 1.046497e-29 eV`, `λ_C = 611.0801 kpc`
`= 2.5462e+04 L*`, sitting **248.43×** below A69's one-sided bound (K24), with `S(0.2) = 0.999795`,
`S(0.5) = 0.998718`, `S(5) = 0.87794`, a half-mode at `k_1/2 = 11.1632 h/Mpc` and
`M_J = 3.266079e+10 M☉` at the mean density (K27–K31) — and `611.0801 kpc` matches nothing measured: the ratios
to A29's splashback (1.414 Mpc), A29's `u = 1/2` crossing (1.065 Mpc), A18's `r_v` (1.6863 Mpc) and A29's
`R_200c` (1.0344 Mpc) are `0.4322`, `0.5738`, `0.3624`, `0.5908` (K32), and it *cannot* match anything, because
A69's static sector is η-independent (G5/G6) so the law has no Yukawa range, while the transverse modes that do
carry `γ/η` are unpopulated, uncoupled and unsourced. In the other direction the medium's real pressure is
elastic — `ρσ²/p_el = 1.335776e+08`, `c_T/c_s,el = 1.1558e+04` (K39) — so the speed that governs structure
formation is **0.720364 m/s** (`λ_J,el = √2πL* = 106.6218 pc`, density-free, `M_J,el = 2.115564e-02 M☉` at the
mean density; K34–K37), and `8.3257 km/s` enters only through free-streaming, only if `σ_c` is a dispersion —
which is exactly what the elastic EOS denies. **Verdict (b): `γ/η` is still free.** The missing principle is a
matching condition for the kinetic coefficient — a Kubo/transport relation `η⁻¹ = lim_{ω→0}(1/ω)∫dt⟨[P_i(t),P_j(0)]⟩`,
or its hydrodynamic limit `η = 1/ρ_c` — that ties the P field's inertia to the medium's mass current. Nothing in
the frozen action, the Γ = 2 EOS, the de Sitter temperature or the Gauss law supplies one; and the honest
prediction for the P-mode range remains the whole interval `(0, ∞)` allowed by A69, from the hydrodynamic corner
`γ/η = 5.773810e-18`, `λ_C = 7.06 Gpc`, `c_T = 0.7204 m/s` to the candidate corner `611.0801 kpc`,
`8.33 km/s` — a factor `1.335776e+08` in `γ/η` that only a new principle can close.
