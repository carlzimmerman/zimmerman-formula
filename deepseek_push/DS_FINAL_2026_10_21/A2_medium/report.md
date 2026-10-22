# A2 — the saturating medium is a Langmuir lattice: n=1 is forced, n=2 is not a lattice

Lane A2, `deepseek_push/DS_FINAL_2026_10_21/`. Inputs: `a0 = 9.36e-11 m s^-2` (BRIEF §4),
`G = 6.67430e-11`, `GM_sun = 1.32712440018e20 m^3 s^-2` (IAU nominal), `kpc = 3.0856775814913673e19 m`.

## Claim

The canonical law `g_N = g²/(g+a0)` **is** the stationary condition of a lattice of
independent bistable gates — two states, at most one occupant per site, adsorption rate
linear in the local **total** acceleration `g`, desorption independent of it — when the gate
capacity `C = ν p̂` and affinity `s = k_d/k_a` are both the single vacuum-tied scale `a0`.
The identity is exact and carries no fitted constant: with `x = g/a0`, `θ = x/(1+x)`, the
medium's share of the field is `A ≡ g − g_N = a0 θ` (capacity × occupancy) and the baryonic
share is `g_N = g θ` (drive × occupancy); they sum to `g` precisely because `θ = g/(g+a0)`.
The same lattice **cannot** give the n=2 a₀-line: the deep MOND limit forces `C = s`, hence
capacity `a0`, hence n=1, while the quadrature law has capacity `a0/2` at the same deep-limit
scale, is even in `g` where every single-scale Langmuir is not, and lies outside the closure
of *positive* mixtures of two-state gates — its response has square-root branch points at
`g = ±i a0/2` instead of a cut on the negative real axis. "n" is therefore exactly a capacity
assignment: n=1 is "capacity = affinity = a0"; n=2 is "capacity a0/2 with a non-Langmuir
response". The lattice also predicts one thing that is not the law: a binomial occupancy
variance fixing the *shape* of the RAR scatter at fixed `g_N` (∝ g^{-3/2}) and flipping the
sign of its skewness at `g = a0`.

## Derivation

### 1. The identity (exact; K1)

With `g` observed, `g_N` baryonic, `A = g − g_N`, `x = g/a0` and the Langmuir occupancy

```
θ(x) = x/(1+x),   x = g/a0,                                                (1)
A   = g − g²/(g+a0) = a0 g/(g+a0) = a0 θ      i.e.  1/A = 1/g + 1/a0,     (2)
g_N = g²/(g+a0)     = g·g/(g+a0)  = g θ,                                   (3)
g   = (a0 + g) θ.                                                          (4)
```

(2) is the content: the medium response is the harmonic mean of `a0` and `g`, saturating at
capacity `a0`. (4) splits the field into a capacity term `a0θ` and a drive term `gθ`;
eliminating `θ` between (2) and (3) is the identity. Both laws are homogeneous of degree one in
`(g, a0)` (K14): `a0` is the only scale either can carry.

### 2. The lattice, grand-canonically (K2, K3)

One site, two states: empty (energy 0, occupation 0) and occupied (`−ε`, occupation 1).

```
Z = 1 + e^{β(μ+ε)},   θ = x/(1+x),   x = e^{β(μ+ε)}.                       (5)
μ(g) = k_BT ln(g/a0) − ε   ⇒   x = g/a0,   θ = g/(g+a0),                   (6)
k_a g (1−θ) = k_d θ        ⇒   θ/(1−θ) = (k_a/k_d) g,   k_d/k_a = a0.      (7)
```

(6) is the grand-canonical statement, (7) the equivalent driven mass-action statement: two
rate constants, but only the ratio survives. The potential, with `u = a0θ`, is

```
K W_full(u) = a0²[−θ − ln(1−θ)],      K W_full'(u) = a0θ/(1−θ) = g,        (8)
K W_rem = K W_full − u²/2 = a0²[−ln(1−u/a0) − u/a0 − u²/(2a0²)],           (9)
```

which is Eq. (2) of `core_open_problems_2026_10_20/02_medium` at `n=1`, exactly. Note what
(9) is *not*: its entropy is `−ln(1−θ)`, not the lattice-gas mixing entropy
`θlnθ + (1−θ)ln(1−θ)`. The match is at the level of the **equation of state**, and (8) is
conjugate to the *activity*, not to a chemical potential. That is the premise in **Status**.

### 3. The drive cannot enter linearly (K4)

For an equilibrium Gibbs state with linear coupling, `H = −λ g σ_z`, `θ_F = 1/(1+e^{−βλg})`
is finite at `g = −a0` where `θ_L = g/(g+a0)` has its only pole, and `g(1−θ_F) → 0` while
`g(1−θ_L) → a0`. Meromorphic functions agreeing on an interval share their pole sets, so no
`(λ, T)` reproduces (1): the Langmuir form is necessarily a **driven** steady state. This is
also why the round-1 §2 analyticity obstruction is evaded, not violated: the isotherm is
analytic in the scalar `g`, but the Legendre dual `W_rem(|u|)` carries `|u|³/(3a0)` — C² and
**not** analytic in the vector components, exactly the nonanalyticity `02_medium` §2 named.

### 4. One scale ⇒ n = 1, uniquely (K5, K8, K15, K16)

For capacity `C = νp̂` and affinity `s`,

```
g_N = g − C g/(g+s) = g(1 − C/s) + C g²/s² − C g³/s³ + …                   (10)
```

The deep limit `g → √(a0 g_N)` requires the linear term to vanish, i.e. `C = s` **exactly**;
then `g_N = g²/(g+s)` and the deep limit is `g = √(s g_N)`, so `s = a0`. Hence
`C = s = a0`: capacity and affinity are the same number, and it is the vacuum scale. Two
gates per site (or any number of identical gates) just add capacities, `2c·g/(g+s)` — one
Langmuir again; with `A'(0) = 2c/s = 1` one gets `2c = s = a0`, the same law. Multi-occupancy
ladders `N = 0…N_max`, `E = εN + U N(N−1)/2`, have capacity `N_max·a0` for every `U` (K15):
reaching `a0/2` would need `N_max = 1/2`.

### 5. What the n=2 a₀-line would have to be (K6, K7)

```
g_N = √(g² + a0²/4) − a0/2,                                                (11)
```

which is **even** in `g`: `g²/a0 − g⁴/a0³ + …` against (3)'s `g²/a0 − g³/a0² + g⁴/a0³ − …`.
The laws share the `g²` coefficient and differ first at O(g³) by exactly `1/a0²`
(dimensionless: 1); no choice of `(C, s)` removes that, since a single Langmuir is never
even. In the response variable, with `a ≡ a0/2`,

```
A₂(g) = g + a − √(g²+a²),   A₂(0)=0,  A₂'(0)=1,  A₂(∞)=a0/2,              (12)
A₂(g)/g = 1 + a/g − √(1+a²/g²),    branch points at  g = ±i a0/2.          (13)
```

A positive mixture of gates, `A = ∫ g/(g+s) dμ(s)`, `μ ≥ 0`, is a Stieltjes function:
analytic off `(−∞,0]`, all singularities on the negative real axis. Those of (13) are
imaginary, so **no** distribution of two-state gates — discrete or continuous, one scale or
many — reproduces n=2 exactly. Independently `A₂''' = 3a²(a²−4g²)/(a²+g²)^{7/2}` changes
sign at `g = a0/4`, so `A₂'` is not completely monotone and (12) is not a Laplace–Stieltjes
mixture either. The three candidates fail correspondingly. *Two internal degrees of freedom
per site*: a positive mixture with additive capacity (K8, K15), giving n=1 with capacity
`2c` or `N_max a0`. *Capacity additive in energy*: a bound on stored energy caps the
**field** (`g ≤ F'(u*)`), not the response, so it cannot produce a pole at finite `u`; its
ladder version still has capacity `≥ a0` (K15). *Continuous distribution of threshold
fields*: represents **any** monotone response with density `ρ = A' ≥ 0`, so it encodes
either law and selects neither, and with thermal elements it is excluded by (13).
Microscopically (13) is a relativistic-dispersion shape — `A₂' = 1 − g/√(g²+a²)` is `1 − β`
for mass `a0/2` — the class round 2 tested (Clifford spectrum, `E = √(v²k²+m²)`), which
gives the right `u²` force power but the wrong quartic sign and no capacity pole.

| object | n = 1 | n = 2 |
|---|---|---|
| capacity `A_max` / affinity `s` | `a0` / `a0` | `a0/2` / `a0` (common deep limit) |
| isotherm | `θ = x/(1+x)` | implicit `4x(1−θ) = θ(2−θ)` |
| `A(g)` | `a0 x/(1+x)` | `g + a − √(g²+a²)`, `a = a0/2` |
| analytic structure / gates | pole at `g=−a0`; one gate | branch points `±i a0/2`; no positive mixture |

### 6. How far apart the laws are (K9, K10)

With `y = g_N/a0`, `z = √(1+4/y)`,

```
g₁/g₂ = (z+1)/√(z²+3),   d/dz (g₁/g₂) = (3−z)/(z²+3)^{3/2}  ⇒  z=3,  y=1/2,   (14)
max (g₁−g₂)/g₂ = 2/√3 − 1 = 0.1547005384,                                  (15)
max (v₁−v₂)/v₂ = √(2/√3) − 1 = 0.0745699318.                               (16)
```

The 7.46% of `core_open_problems_2026_10_20` is **reproduced** — as the *circular-speed*
maximum; the *acceleration* maximum at the same point is 15.47%. Both sit at
`g_N/a0 = 0.499994` (scan). The fraction depends only on `g_N/a0`, so at fixed `M_b` (varying
`r` via `g_N = GM_b/r²`) the same maximum occurs at `r* = √(2GM_b/a0) = √2 r_M`, mass-independently.

| `M_b` (`M_sun`) | `r*` (kpc) | `v₁` (km/s) | `v₂` (km/s) | `(v₁−v₂)/v₂` |
|---:|---:|---:|---:|---:|
| 1e8 | 0.54574 | 39.701 | 36.946 | 0.074570 |
| 1e9 | 1.72577 | 70.600 | 65.701 | 0.074570 |
| 1e10 | 5.45736 | 125.546 | 116.834 | 0.074570 |
| 1e11 | 17.2577 | 223.257 | 207.764 | 0.074570 |

(With `a0 = 9.3603e-11`, as in the prior report, these become 5.45785 kpc / 125.554 km/s; the
9.0e-5 relative difference is the `a0` rounding.) The separation exceeds 1%, 5%, 10% for
`g_N/a0 ∈ [4.13e-4, 47.7]`, `[1.20e-2, 7.74]`, `[6.43e-2, 2.70]`; for `1e10 M_sun` that is
`r ∈ [0.790, 269]`, `[1.96, 49.8]`, `[3.32, 21.5]` kpc.

### 7. An observable that is not the law: occupancy noise (K11–K13)

For `N_s` independent gates in the resolution element the occupancy is binomial,

```
Var(N)/N_s = θ(1−θ)   ⇒   (σ_u/u)² = (1−θ)/(θ N_s),   u = Cθ.             (17)
```

At fixed `g_N`, `g = g_N + u` gives `δg = C ξ/(1−u')`, `Var(ξ) = θ(1−θ)/N_s`, so

```
σ_g = C √(θ(1−θ)/N_s)/|1−u'(g)|,     σ(log g) = σ_g/(g ln10);              (18)
σ(log g)|_{g_N} = a0^{3/2}(g+a0)/[g^{3/2}(g+2a0)√N_s ln10] ∝ g^{−3/2}     (19)
```

for n=1, with a different curve for n=2 from (12). `N_s` cancels in ratios, which is what
makes this falsifiable without knowing the gate density:

```
σ(0.3a0)/σ(3a0) = 22.34 (n=1) vs 34.49 (n=2);  σ(a0)/σ(10a0) = 23.00 vs 30.38,
asymptotic slope −1.4998.                                                  (20)
```

The normalisation inverts to the gate number: 0.03 dex intrinsic scatter at `g = a0` means
`N_s = 93.1` gates per resolution element (0.05 dex → 33.5; 0.10 dex → 8.4), 0.05 dex at
`g = 0.3a0` means `N_s = 892.7`. The third moment gives an `N_s`-free zero: binomial noise
has `skew(δg) ∝ (1−2θ)`, changing sign exactly at `θ = 1/2`, i.e. at `g = a0` (K13). Shape
(19), ratios (20) and the skew flip are lattice consequences, not restatements of the law.

> **ERRATUM (2026-10-22, doors push D1):** "`N_s`-free zero" holds only for δg in linear g. RAR errors are symmetric in log g, and in log g both laws give a negative skew across (0.375, 1)a₀, so the skew sign does not decide n on RAR residuals (D1 SCOPED NO-GO, `doors_push_2026_10_22/D1_skew_preflight/README.md`).

## Status

**CONDITIONAL(single-scale driven two-state lattice: capacity = affinity = a0)** for the
medium, **n = 1 forced** in that class; **NO-GO(thermal-lattice class)** for n=2 by (13);
**NUMERICAL** for (14)–(16) and (20). Two premises, neither a fitted number: (P1) the gate's
steady state is mass-action with adsorption linear in the local total acceleration and
drive-independent desorption — the drive enters as an activity (§2–3; the linear-coupling
equilibrium state is excluded by K4); (P2) no acceleration scale other than `a0`, so
`C = s = a0` (§4). Given (P1)–(P2) there is no freedom left; conversely any single-scale
lattice reproducing the observed deep-limit scale `a0` must have `C = s = a0` and *is* the
canonical law, not a family member.

## Checks

`a2_checks.py` prints `<id> PASS|FAIL <measured> <threshold>` per check, ends
`A2 COMPLETE: 16/16 checks PASS.`, exit 0; `a2.out` is the captured run.

| id | what it proves | measured |
|---|---|---|
| K1, K14 | identities (2)–(4), homogeneity deg 1 (sympy remainders) | 0 |
| K2, K3 | mass action (7) and GC (5)–(6) ⇒ law; `K W_full'=g`; `W_rem` = prior Eq. (2), n=1 | 0 |
| K4 | no linear Gibbs state: Fermi finite at `g=−a0`; `g(1−θ)→0` vs `→a0` | 0.2689 |
| K5 | `g_N` linear coefficient `1−C/s`; MOND forces `C=s` | 0 |
| K6 | n=2 even in `g`; shared `g²/a0`; cubic gap `1/a0²` | 1.0 |
| K7 | n=2 branch points `±ia0/2`; `A₂'` not completely monotone (flip at `a0/4`) | 2 |
| K8, K15 | two gates = one Langmuir (capacity adds); ladders capacity `≥a0`, `a0/2` unreachable | 0, 1.0 |
| K9, K10 | max fraction 0.1547005 (g) / 0.0745699 (v) at `g_N/a0=0.5`; `r*=5.45736 kpc`, mass-independent | 0.1547005 |
| K11 | `Var(θ)/θ²=(1−θ)/(θN_s)`; binomial MC 0.011199 vs 0.011180 | 0.00169 |
| K12, K13 | slope −1.4998, ratios (20); skew sign flip at `θ=1/2` (`g=a0`) | −1.4998 |
| K16 | lattice inversion `(C,s)=(a0,a0)` reproduces the law on `g_N/a0∈[1e-3,1e3]` | 1.1e-15 |

`MUTATE.md`: halving the capacity (`C = a0/2`) breaks K5 (linear coefficient 0.5) and K16
(93.8% deviation) — the checks have teeth on exactly the quantity `n` encodes.

## What this does not do

- It does not derive `a0`; `a0` is an input (BRIEF §4), consumed twice (capacity, affinity)
  with nothing added. Deriving `κ = 1/2` remains closed (BRIEF §2).
- It does not supply a Hamiltonian. (P1) is *kinetic*; (8) is conjugate to the activity, not
  an equilibrium free energy, and the equilibrium lattice-gas free energy (mixing entropy)
  gives the `artanh` law of `02_medium` §5, not (9). Derived: the equation of state, not a
  partition function of the gravitational sector.
- It does not identify `u` with the action's `K P`: `g` in (1) is the total field, consistent
  with `g = K W_full'(u)` of the frozen action, but the map from `T^φ_μν` to a site density
  is not given.
- n=2 is excluded only as a *thermal/positive-mixture* lattice; a gapless relativistic medium
  with an added capacity pole at `u = a0/2` is not excluded by (13), and round 2 showed the
  Clifford spectrum alone has neither that pole nor the right quartic sign.
- The noise prediction assumes independent gates, fixed `N_s`, no non-circular motion and no
  measurement error; `N_s` is *not* predicted — it is measured by the normalisation.
- No RAR dataset was used; §7's "flat observed scatter" comparison is a stated 0.03–0.05 dex.

## Next

1. The decisive measurement is the **g-dependence** of the intrinsic RAR scatter: (19)
   predicts `g^{−3/2}` with the `(g+a0)/(g+2a0)` modulation, plus the skew flip at `g = a0`.
   Flatness across `0.3a0 → 3a0` within a factor 1.2 would push `N_s ≳ 10³` and make the
   lattice noise subdominant — not falsify the lattice.
2. Tie `N_s` to the medium's own length: with `νp̂ = a0`, a beam of volume `V` has
   `N_s = a0V/p̂`; the stiffness scale `L*` (24 pc, BRIEF §1) is the only length that could
   fix `p̂`, so this is testable on the same globular sample that bounds `L*`.
3. Replace (P1) with a concrete excitable element (threshold + refractory time) and check
   that its steady-state isotherm is Langmuir in `g` rather than Boltzmann in `Φ` — the one
   premise left between this construction and a closed derivation.
