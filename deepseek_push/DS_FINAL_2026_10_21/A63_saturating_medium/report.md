# A63 — what medium produces the saturating vacuum term, and does nature pick n=1 or n=2?

Lane A63, `deepseek_push/DS_FINAL_2026_10_21/`. Reads `A2_medium`, `A35_series_parallel`,
`A7_discriminator`, `A25_kernel_conflict` first. Inputs `a0 = 9.36e-11 m s^-2` (BRIEF §4),
`G = 6.67430e-11`, `M_sun = 1.98892e30 kg`, `AU = 1.495978707e11 m`. Every algebraic statement
below is a sympy remainder in `a63_checks.py` (31/31 PASS, exit 0); every number is repeated in
`a63_results.json`. `--mutate` and `--mutate-n2` replace the identified medium by the tanh
dielectric and by the n=2 element respectively; the first breaks the seven identification checks, the
second those seven plus K11, and each reproduces the rival's numbers exactly (`a63_MUTATE.out`,
`a63_MUTATE_n2.out`, `MUTATE.md`).

## Claim

The saturating term is realised by a **one-sided, hard-core, single-occupancy lattice driven by an
activity** — a Langmuir gate. What the medium must supply is not "saturation" but **rectification**:
the isotherm must have `f''(0) ≠ 0`, so that the response begins `A = g − g²/a₀ + …`. Every
centrosymmetric saturating medium (`tanh`, Langevin) is odd, has `f''(0) = 0`, and therefore gives
`g_N ∝ g³` — a deep exponent 3, not 2, i.e. no MOND at all. Born–Infeld fails the other way: it
caps the **drive** (`g → E_max`) instead of the **response** (`A → a₀`) and anti-screens at every
field. The one serious dielectric rival — a *biased*, non-centrosymmetric `tanh` — can match the
deep limit exactly but its capacity is bounded by `a₀/2`, so it cannot reach the observed anomaly.

For any saturating medium with unit linear response, **one number organises the whole class**: the
deep limit `g_N = g²/a₀` forces `capacity = affinity = −c₂a₀`, where `c₂ = f''(0)/2` is the
isotherm's second-order coefficient. The Langmuir's `c₂ = −1` gives `C = s = a₀`. The n=2 law has
the **same** `c₂` but **half** the capacity (`a₀/2`): it is the same element with its own response
consuming half its budget (A35's `λ = 1`), not a second lattice.

Because `W` is the integral of the isotherm, `W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)]` and
`g_N = g²/(g+a₀)` are **one condition, not two** (K2, K3): a medium that reproduces the law
reproduces the log form automatically, and vice versa. What has content is the isotherm, and only
the lattice supplies it.

The discriminator that is not a rotation-curve fit is the **sign of the occupancy-noise skew**,
`skew = (1−2θ)/√(N_s θ(1−θ))`: **+0.7071 for n=1 and −0.3483 for n=2 at g = a₀/2**, zero at
**g = a₀ vs 3a₀/8**, hence **opposite signs on (0.375, 1)a₀**. It is a sign, so it is immune to
normalisation, to `Υ` and to `N_s`; the window is in units of `a₀`, so the footing must be pinned
(a 20 % footing shift moves the flip by 20 %, A7's alt footing), but no amplitude calibration is
needed. It is the only difference between the two laws that a measurement can report as a sign.

## 1. What any medium must do: the admissibility theorem

Write the response of any saturating medium as

```
A(g) = C f(g/s),   f(0)=0,  f'(0)=1,  f(∞)=1,  f(x) = x + c₂x² + c₃x³ + …            (1)
```

`C` is the capacity (`A(∞)`) and `s` the drive scale of the isotherm. Then

```
g_N = g − A = g(1 − C/s) − (C c₂/s²) g² − (C c₃/s³) g³ − …                          (2)
```

**(i)** The deep limit requires the linear term to vanish — otherwise `g_N ∝ g` and there is no
MOND. Hence `C = s`. This is A2's §4 condition, and it is *not* special to the lattice: every
saturating medium must obey it.

**(ii)** With `C = s`, `g_N = −(c₂/s) g² + …`, so `g_N = g²/a₀` requires `s = −c₂ a₀`.

**(iii)** Therefore `C = s = −c₂ a₀`. **The capacity is not a free parameter: it is the isotherm's
curvature at zero drive.** (K8.) The theorem assumes the shape is normalised so that the
linear-response scale and the saturation scale coincide (`f'(0) = f(∞) = 1`); an isotherm whose
shape has `f'(0)/f(∞) ≠ 1` — the Langevin's is `1/3` — cannot satisfy both, and with unit slope its
capacity is `3s`; such shapes are excluded anyway by `c₂ = 0` (below).

This sharpens A2 §4 rather than contradicting it. A2 derived the isotherm first — so `c₂ = −1` was
already in hand — and then used the deep limit *inside* the Langmuir family to conclude `C = s = a₀`.
The theorem makes explicit which premise does which job: **the deep limit alone gives only
`C = s = −c₂a₀`; the lattice's contribution is `c₂ = −1`.** Two media with the same deep limit and
different `c₂` are different laws with different capacities (e.g. `c₂ = −1/2` gives `C = s = a₀/2`
and still `g_N = g²/a₀` to leading order).

What the theorem does *not* constrain is the next coefficient: `c₃` is free, and it is the first
number that distinguishes media which all pass (i)–(iii). That is why the third-order response is
the natural fingerprint of a medium (K23):

```
R ≡ c₃ c₁ / c₂² :   Langmuir +1,   n=2 0,   centrosymmetric dielectric ∞.           (3)
```

| candidate | isotherm / response | `c₂ a₀` | `c₃ a₀²` | `C/a₀` | deep `g_N` | verdict |
|---|---|---|---|---|---|---|
| **Langmuir lattice** | `θ = x/(1+x)` | **−1** | **+1** | **1** | `g²/a₀` | **admissible** |
| tanh dielectric | `tanh x` | 0 | −1/3 | 1 | `g³/(3a₀²)` | excluded: exponent 3 |
| Langevin | `L(x) = coth x − 1/x` | 0 | −1/15 | ≠1 (two scales) | `g³/(15g_c²)` | excluded: exponent 3 |
| biased tanh | `tanh(x/E_c+w) − tanh w` | −1 (forced) | `R = 1−1/(3u²)` | `u/(1+u) ≤ 1/2` | `g²/a₀` | excluded: capacity, shape |
| Born–Infeld | `g_N/√(1+g_N²/E²)` | — | — | caps `g` | `g_N` (linear) | excluded: anti-screening |
| n=2 element | `4x(1−θ) = θ(2−θ)` | −1 | 0 | 1/2 | `g²/a₀` | excluded: not a state (A35) |

## 2. Candidate (a): the saturating dielectric

`P = P_max tanh(E/E_c)` with the linear response matched, `A'(0) = 1` (otherwise the deep law is
Newtonian), i.e. `P_max = E_c`. In units `x = g/E_c`, `A_max = E_c`:

```
tanh x        = x − x³/3 + 2x⁵/15 − 17x⁷/315 + …
A/A_max       = x − x³/3 + …                       c₂ = 0,  c₃ = −1/3
g_N/A_max     = x³/3 − 2x⁵/15 + …      ⇒  g_N = g³/(3 E_c²)   (exponent 3)            (4)
```

Measured log–log slope at `g/a₀ = 10⁻⁴`: **3.0000** (K6). The Langevin function is the same story
one order weaker:

```
L(x)          = coth x − 1/x = x/3 − x³/45 + …        (slope 1/3, saturates at 1)
f(x) ≡ 3L(x)  = x − x³/15 + 2x⁵/315 − …               f'(0)=1, f(∞)=3
A             = E_c f(g/E_c)      ⇒  A'(0)=1,  A(∞)=3E_c
g_N           = E_c[x − f(x)]  →  g³/(15 E_c²)  as g → 0   (exponent 3)               (5)
```

`Langevin` is worth a remark because it *does* saturate algebraically (`1 − L ≈ 1/x`), exactly like
the Langmuir — and it still fails, because its failure is at **small** drive, not at saturation:
it is odd, so `c₂ = 0`. (Its shape also has `f'(0)/f(∞) = 1/3`, so "unit slope" and "unit
saturation" cannot both hold: a second, independent mismatch of scales.) This separates two
properties that are easy to conflate. Saturation with the right tail is not enough; the medium must
be **non-centrosymmetric**.

Physically: a dielectric obeys `P(−E) = −P(E)` by symmetry. Its isotherm is odd, its Taylor series
has only odd powers, and the response to a one-sided drive `g ≥ 0` carries no `g²` term. MOND's deep
limit *is* a `g²` term. **The gravitational medium must rectify**, not merely saturate. In the
lattice the rectification is the hard core: `θ ∈ [0,1]`, so `A(g)` on `g > 0` is not the odd
continuation of anything (its analytic continuation has a pole at `g = −a₀`, K17; the n=2 response
has branch points at `±i a₀/2` instead, A2's K7).

**Effective susceptibility, explicitly.** `χ ≡ dP/dE = (P_max/E_c) sech²(E/E_c)`. In terms of the
normalised polarisation `u = P/P_max`, `E/E_c = artanh u`, so `χ(u) = (P_max/E_c)(1−u²)` — even in
`u`, with correction `−u²` and no linear term. The Langevin susceptibility `χ = dL/dx` is even in
`x`, hence even in `u = L(x)` as well, with correction `−(9/5)u² + …`. Both are even in the response
variable, so neither can generate the Langmuir's all-powers `u − u² + u³ − …`; the parity mismatch is
the exclusion, not the saturation.

**The strongest dielectric rival, derived.** Break the symmetry by hand: a biased `tanh`,
`A = P[tanh((g−E_b)/E_c) + tanh(E_b/E_c)]`, with `P`, `E_c`, `E_b` chosen so that `A(0) = 0`,
`A'(0) = 1` and `A''(0) = −2/a₀` (the exact deep limit). The solution is a **one-parameter family**
(`u = tanh(E_b/E_c) ∈ (0,1)`):

```
E_c = a₀ u,   P = E_c cosh²(atanh u),   C = A(∞) = a₀ u/(1+u) ≤ a₀/2,
R   = 1 − 1/(3u²)  ≤ 2/3.                                                             (6)
```

(K9.) So a biased dielectric *can* reproduce `g_N = g²/a₀` at leading order — and then its capacity
is at most half of the required `a₀`, and its third-order fingerprint never reaches `R = 1`.
Because the capacity is `≤ a₀/2`, it under-predicts the anomaly by **50–91 % at `g ≳ 10a₀`** and by
**14–82 % at `g = a₀`**, depending on `u` (for `u ∈ [0.1, 0.99]`). The reason is structural: exponential saturation
ties the curvature at zero to the total capacity; only algebraic (`1/x`) saturation decouples them.
**The medium must saturate hyperbolically, not exponentially.**

## 3. Candidate (b): Born–Infeld

The maximum-field action is `L = −E_max² √(1 − E²/E_max²)`, whose Hamiltonian and field are

```
H(D) = E_max² (√(1 + D²/E_max²) − 1),     E = dH/dD = D/√(1 + D²/E_max²).             (7)
```

The identification is fixed by the theory's own structure: `g = K W'(u)` is the total field and `u`
is the medium variable sourced by the baryons, so `g ↔ E` (total) and `g_N ↔ D` (source). Then

```
g = g_N/√(1 + g_N²/E_max²) = g_N − g_N³/(2E_max²) + 3g_N⁵/(8E_max⁴) − …
A ≡ g − g_N = −g_N³/(2E_max²) + …  < 0   for every g_N > 0.                            (8)
```

Four independent failures, all exact:

1. **No quadratic term.** `g` is *linear* in `g_N` (coefficient 1), so the deep exponent is **1**:
   Newtonian, no MOND (K10).
2. **Wrong sign.** `A < 0` everywhere: the total field is *less* than the baryonic one — BI
   anti-screens. At `g_N = a₀` with `E_max = a₀`, `A = −0.2929a₀` against the law's `+0.5a₀`
   (K10). This is not a 41 % shortfall; it is the opposite sign.
3. **Wrong topology.** `g → E_max` as `g_N → ∞`: BI caps the **drive**. The theory caps the
   **response** (`A → a₀`, `g → ∞`). At `g_N = 10³a₀`, BI gives `g = 0.9999995 E_max` while the
   theory at `g = 10⁹a₀` still has `g = 10⁹a₀` and `A = 0.999999a₀` (K11). Reading BI instead as a
   potential, `K W_BI(u) = E_max²(√(1+u²/E_max²) − 1)`, gives `g = u/√(1+u²/E_max²)` — again
   saturating the drive, again the wrong variable.
4. **Quantitatively unusable.** Maximum relative deviation from the law over
   `g_N/a₀ ∈ [10⁻³, 10]`: **96.9 %** (K10).

BI gives neither the Langmuir form, nor the quadratic form, nor MOND. It is excluded by the sign of
the anomaly alone.

## 4. Candidate (c): the finite-capacity lattice

`N_s` sites, at most one occupant each, energy `−ε` when occupied. The drive is the flux through the
gate: adsorption at rate `k_a g` per empty site, desorption at `k_d` per occupied site. Steady state

```
k_a g (1−θ) = k_d θ   ⇒   θ = g/(g+s),   s = k_d/k_a     (mass action)               (9)
Z = 1 + z,  θ = z/(1+z),  z = g/a₀                        (grand canonical)           (10)
```

— the two routes agree (K12, K13), which is the statement that the drive enters as an **activity**,
`z = e^{β(μ+ε)}` with `μ ∝ k_BT ln g`. Each occupied site contributes a quantum `q` to the response,

```
A = q N_s θ = C θ,   C = N_s q;   deep limit ⇒ C = s = a₀  ⇒  q = a₀/N_s.            (11)
```

**Capacity per site and the site's own field.** `q = a₀/N_s` is the per-site capacity; it is *not*
predicted, it fixes the gate density (`N_s = a₀/q`). The affinity `s = a₀` **is** the site's own
saturation field: the drive at which a single site is half occupied. So the answer to the task's
question is: **yes, the law's `a₀` is the site's saturation field, while the capacity per site is
`a₀/N_s`** — the total capacity equals the per-site field only because `N_s q = a₀` is what the deep
limit demands (K14).

**Three things are forced, each by a different observation.**

- **One occupant per site.** With `N_max` occupants the capacity is `N_max a₀`, so the linear
  coefficient of `g_N` is `1 − N_max`: for `N_max = 2` it is `−1`, i.e. `g_N = −g` at small `g`
  (anti-gravity). Measured: `gN(10⁻³a₀)/a₀ = −9.99×10⁻⁴` (K15). No ladder with `N_max ≥ 2`
  survives positivity.
- **Linear adsorption.** For `θ = x^α/(1+x^α)` the deep exponent is 2 only at `α = 1`: `α = 2` gives
  exponent 1 (linear, Newtonian), `α = 1/2` gives exponent 0.5 with `g_N < 0` (K26). The drive must
  enter the **rate** linearly — a flux, not a power.
- **Activity, not energy.** A thermal two-level gate with linear coupling, `H = −λgσ_z`, has
  `θ_F = 1/(1+e^{−βλg})` and `A(0) = a₀/2 ≠ 0`: a medium with a nonzero response at zero drive, and
  no pole (K16). The empty state must be infinitely favoured at `g = 0`, which is exactly the
  activity. This is A2's (P1) restated as a *consequence* of `A(0) = 0`.

**Physical realisations.** Any hard-core, one-occupant-per-site medium driven by a rate: Langmuir
adsorption (the original), ion-channel block, a saturable absorber with site exclusion, and the
exclusion processes of statistical mechanics (TASEP-like). The common feature is not a material but
a **structure**: a bounded integer occupancy plus a rate drive. In the gravitational sector the
"sites" are the medium's own degrees of freedom; the map from `T^φ_μν` to a site density is not
given here (A2's caveat), so this identifies the *class*, not the material.

## 5. The medium that works, and why "both" is one condition

With `θ = g/(g+a₀)`, `A = a₀θ` and `g = (a₀+g)θ`:

```
g_N = g θ = g²/(g+a₀),   A = a₀θ = a₀g/(g+a₀),   A + g_N = (a₀+g)θ = g,
1/A = 1/g + 1/a₀.                                                                     (12)
```

The potential is the integral of the isotherm along the response:

```
K W(u) = ∫₀^u g(u′) du′ = ∫₀^u a₀u′/(a₀−u′) du′ = a₀²[−u/a₀ − ln(1−u/a₀)].            (13)
```

`W(0) = W′(0) = 0`, and `K W′(u) = a₀u/(a₀−u) = g` identically (K2, with a quadrature cross-check
to 10⁻⁹). The converse is the same computation read backwards: given (13), `K W′(u) = g` inverts to
`u = a₀g/(g+a₀)`, hence `g_N = g − u = g²/(g+a₀)` (K3). **The log form and the law are one equation
of state.** "Reproduces both" is therefore not two tests but one — and it is why exactly one medium
works: the isotherm is the only free object.

Series, exactly (K4, K5):

```
K W(u)/a₀² = Σ_{n≥2} u^n/(n a₀^n)  = u²/(2a₀²) + u³/(3a₀³) + u⁴/(4a₀⁴) + u⁵/(5a₀⁵) + …   (14)
K W₂(u)/a₀² = u²/(2a₀²) + u³/(3a₀³) + u⁴/(2a₀⁴) + 4u⁵/(5a₀⁵) + …                          (15)
```

Two corrections to the premise as stated. **(a)** `W`'s series starts at `u²/2`, not `u`: `W(0) =
W′(0) = 0`. The series with unit leading coefficient is the *force*,
`g(u) = u + u²/a₀ + u³/a₀² + … = Σ_{n≥1} u^n/a₀^{n−1}`. **(b)** The n=2 law does **not** "need only
`u²`". Its potential agrees with (14) through `u³` and differs first at `u⁴`, by a factor **2**
(K5), then 4, 8, …; what is even is `g_N(g)`, not `W(u)`:

```
g_N/a₀ = x² − x³ + x⁴ − x⁵ + …   (n=1, all powers)
g_N/a₀ = x²       − x⁴ + 2x⁶ − …  (n=2, even)                                         (16)
```

Both statements are exact and they are different statements. The parity lives in the *drive*; the
potential's series lives in the *response*. The discriminating local number is the third-order
coefficient of the response, `+1/a₀²` for n=1 and exactly `0` for n=2 — equivalently the cubic
coefficient of `g_N(g)`, `−1/a₀²` vs `0`, and `R = +1` vs `0` in (3).

The n=2 "medium" is the self-depleting element `4x(1−θ) = θ(2−θ)`, capacity `a₀/2`, which violates
the admissibility relation (iii) of §1 by exactly the factor 2 (K29) — A35's `λ = 1`. It is not a
positive mixture of two-state gates at all: its response has branch points at `g = ±ia₀/2` while
every positive mixture has its singularities on the negative real axis (A2 K7; K17 here). So
"n=2" is not another medium in this class; it is the same element with its capacity consumed by its
own response.

## 6. The discriminator

### 6.1 The skew of the occupancy noise — a sign, not a magnitude

`N_s` independent gates in the resolution element give a binomial occupancy,
`Var(θ̂) = θ(1−θ)/N_s` and third central moment `θ(1−θ)(1−2θ)/N_s²`. At fixed `g_N`,
`δg = C δθ/(1−A′)` with `1−A′ > 0` for both laws, so the Jacobian is positive and the standardised
third moment is

```
skew(δg | g_N) = (1 − 2θ)/√(N_s θ(1−θ)).                                              (17)
```

(K18, exact symbolically.) It is `N_s^{-1/2}` times a pure function of the occupancy, so its **sign
is the sign of `1−2θ`** — dimensionless, normalisation-free, `N_s`-free, `Υ`-free, `a₀`-free. The
flip is at **half capacity**, `θ = 1/2`, which is a different drive for the two laws:

```
n=1:  θ = g/(g+a₀) = 1/2  ⇔  g = a₀
n=2:  θ = 2A₂/a₀   = 1/2  ⇔  A₂ = a₀/4  ⇔  g = 3a₀/8 = 0.375a₀                        (18)
```

(K19: ratio `8/3 = 2.667`.) Values, `N_s = 1`:

| `g/a₀` | 0.10 | 0.20 | 0.375 | 0.50 | 0.75 | 1.00 | 1.50 | 2.00 | 3.00 |
|---|---|---|---|---|---|---|---|---|---|
| n=1 | +2.846 | +1.789 | +1.021 | **+0.707** | +0.289 | **0** | −0.408 | −0.707 | −1.155 |
| n=2 | +1.664 | +0.757 | **0** | **−0.348** | −0.859 | −1.243 | −1.832 | −2.294 | −3.029 |

On the whole window `g/a₀ ∈ (0.375, 1)` — i.e. `g_N/a₀ ∈ (0.102, 0.5)` — the signs are **opposite at
every point** (K20; the smallest `|skew|` in the window is 0.0513, at the n=1 edge `g → a₀` where
n=1's own skew vanishes). At `g = a₀` n=1 predicts *zero* and n=2 predicts −1.2430.

Two caveats, stated because they matter for any analysis. **(i) Conditioning.** The sign is defined at
fixed `g_N` (the RAR conditioning: baryons known, total field measured). Conditioned at fixed `g`
instead, `δg_N = −Cδθ` and the sign flips for *both* laws; the window and the flip ratio survive,
the absolute sign does not. **(ii) Independence.** (17) assumes independent sites. Correlated
domains rescale `N_s` and can change the magnitude; the sign survives as long as the domain
occupancy is itself binomial.

### 6.2 Signal-to-noise, honestly

With Gaussian measurement noise the sample skewness has `SE ≈ √(6/N)`, and the true skew is diluted
by the occupancy fraction of the scatter, `φ = σ_occ/σ_tot`, as `s_obs = s_true φ³`: the third
moment picks up `σ_occ³` while the standardisation divides by `σ_tot³`. So

```
N(3σ) = 54/(s_true φ³)² :   φ=0.7 → 918,   φ=0.5 → 6912,   φ=0.447 → 1.35×10⁴,
                            φ=0.3 → 1.48×10⁵.                                          (19)
```

(K30.) A2's normalisation — 0.03 dex of occupancy noise at `g = a₀` (`N_s = 93`) on a 0.06 dex
background — gives `φ ≈ 0.45`, hence **N ≈ 7,000–13,500 independent points in the window**, i.e.
~2–4× the whole of SPARC (3375 points, ~10³ in the window) and comparable to A7's requirement of
1330–1980 *galaxies*. The measurement is the third standardised moment of the RAR residual at fixed
`g_N`, in `g_N/a₀ ∈ (0.10, 0.5)`, from resolved or stacked kinematics with independently determined
baryonic masses. **One sign decides: positive → n=1, negative → n=2.** A null at `σ_s ≈ 0.02`
bounds the occupancy fraction of the variance (hence `N_s`, hence the gate density); it does not
rescue n=2.

### 6.3 The other candidates, with their numbers

**Third-order response in a laboratory analogue.** `R = c₃c₁/c₂²` (a Miller-delta analogue) is
**+1 for a Langmuir medium, 0 for the n=2 element, divergent for a centrosymmetric dielectric**, and
sweeps `(−∞, 2/3]` over the biased-tanh family (K23, K9). It is measurable in a day on a saturable
medium by second- and third-harmonic generation (`χ₂`, `χ₃`): the sharpest number in this report and
the cheapest experiment. But it measures the medium *you built*: it confirms the classification, not
which class gravity uses. It is the right calibration and the wrong discriminator.

**Transition-region curvature.** `d²ln ν/d(ln y)²` at the knee `y = g_N/a₀ = 1/2`: **0.0741 (n=1)
vs 0.1111 (n=2)** — a 50 % difference, larger than the 15.47 % in `g` (K21). But it is a second
derivative of a fit, it is a rotation-curve measurement, and A7's forecast (1330–1980 galaxies;
`Δχ² = +219/−345`, `z = 0.75/−1.21` on 171) is the price. Excluded by the task's own constraint.

**Added: wide binaries.** At `1 M_sun` and `10 kAU`, `g_N = 0.634a₀` — exactly the knee —
`v(n=1)/v(n=2) = 1.0740`, a **7.40 %** difference (6.58 % at `2 M_sun`, 6.97 % at `1.5 M_sun`/
`20 kAU`; K22). This is the best *mean-field* non-rotation-curve route: no `Υ`, no profile
decomposition, ~10³–10⁴ pairs, systematic-limited by triples and contamination at the few-percent
level. But it is a magnitude, and it needs the stellar mass scale.

### 6.4 The pick

**The skew sign (6.1).** It is the only candidate that is a *sign*, so it has no normalisation
budget at all: no `Υ`, no distance scale, no `N_s`, no mass-luminosity relation (the window is in
units of `a₀`, so the footing must be pinned, but it need not be calibrated to better than the
window width). Its price is statistical, not systematic, and it is stated in (19). The mean-field alternatives are all
5–15 % magnitudes whose systematics are the dominant error (A7: `z = 0.75` on 171 galaxies; wide
binaries: triple contamination at the few-percent level). For a question that is *which of two
interpolations*, a sign is worth more than a magnitude; for a question that is *what medium*, it is
the only observable that tests the medium's microstructure rather than its mean response.

The trade is explicit. A mean-field difference of 7.4 % against a 3 % coherent systematic has a
per-sample S/N of ≈2.5 that **does not improve with `N`**: averaging reduces the random part, not
the coherent part. The skew's signal has no coherent systematic — a sign cannot be manufactured by a
normalisation error, and an odd moment is blind to any symmetric error — so its S/N grows as `√N`
without bound; the only question is how many points are needed, and (19) answers it. That is why it
wins on signal-to-noise even though it needs more data than the mean-field routes.

## 7. Verdict

**The medium.** A one-sided, hard-core, single-occupancy lattice driven by an activity — the
Langmuir gate. Capacity per site `q = a₀/N_s`; the affinity is `a₀`, the site's own half-occupancy
field; total capacity `N_s q = a₀` because the deep limit demands `C = s = −c₂a₀` and the lattice
supplies `c₂ = −1`. All rivals are excluded structurally, not by fitting: `tanh`/Langevin are odd
(exponent 3); Born–Infeld caps the drive and anti-screens (exponent 1, `A < 0`); the biased `tanh`
is the only near-miss and its capacity is bounded by `a₀/2`; multi-occupancy ladders give `g_N < 0`;
a linear-coupling thermal gate gives `A(0) = a₀/2`.

**The law it gives.** `g_N = g²/(g+a₀)` **and** `K W(u) = a₀²[−u/a₀ − ln(1−u/a₀)]` — one equation
of state, `W` being the integral of the isotherm. Series: `K W = Σ u^n/(n a₀^{n−2})`;
`g(u) = Σ u^n/a₀^{n−1}`; `g_N/a₀ = x² − x³ + x⁴ − …`. The n=2 potential agrees through `u³` and
differs first at `u⁴` by a factor 2; its `g_N(g)` is even. `R = c₃c₁/c₂² = +1` vs `0`.

**Does nature pick n=1?** If the medium is a lattice — the only admissible medium in this class —
then **n=1 is forced**, twice over: by the isotherm's `c₂ = −1` with `C = s = a₀` (here, and A2), and
by least dissipation, n=2 not being a stationary state (A35). Nothing in the data yet confirms it:
A7 shows SPARC cannot separate the two laws. The one observation that would is the **sign of the
occupancy-noise skew at fixed `g_N` in `g_N/a₀ ∈ (0.10, 0.5)`**:

> **+0.7071 (n=1) vs −0.3483 (n=2) at `g = a₀/2`; zero at `g = a₀` vs `3a₀/8`; opposite signs on
> `(0.375, 1)a₀`. One sign decides, and it needs no calibration — N ≈ 7,000–13,500 points in the
> window if the occupancy noise is at A2's level.**

## Status

**DERIVED** — the admissibility theorem `C = s = −c₂a₀` (K8); the exclusion of `tanh`, Langevin,
Born–Infeld, the biased `tanh`, multi-occupancy ladders and linear-coupling thermal gates (K6, K7,
K9–K11, K15, K16); the equivalence of the law and the log `W` (K2, K3); the lattice's capacity
bookkeeping (K12–K14). **CONDITIONAL(one occupant per site + activity drive + linear adsorption)** —
inherited from A2's (P1), here shown to be forced by `A(0) = 0`, positivity and the deep exponent
(K15, K16, K26). **NUMERICAL** — all series coefficients, the skew table and its flip (K18–K20), the
15.47 %/7.46 % separation (K21), the wide-binary 7.40 % (K22), the sample sizes (K30).
**NO-GO** — n=2 as a lattice or as a positive mixture (A2's analyticity, A35's least dissipation;
K17, K29 here). **UNDECIDED** — n=1 vs n=2 on existing data (A7).

## Checks

`a63_checks.py` prints `<id> PASS|FAIL <measured> <threshold>`, ends
`A63 COMPLETE: 31/31 checks PASS.`, exit 0, ≈1 s, no network. `a63.out` is the captured run.

| id | what it proves | measured |
|---|---|---|
| K1 | `A=a₀θ`, `g_N=gθ`, `A+g_N=g`, `1/A=1/g+1/a₀`, `g=(a₀+g)θ` | 0 |
| K2 | `K W = ∫₀^u a₀u′/(a₀−u′)du′`; `W(0)=W′(0)=0`; quadrature | 7.5e−10 |
| K3 | converse: the log `W` implies the law (one condition, not two) | 0 |
| K4 | `K W/a₀² = Σ_{n≥2} u^n/(n a₀^n)`, coefficients 1/2…1/7 | 0 |
| K5 | `W₂/W₁ = 1,1,2,4` at `u²…u⁵`: first difference at `u⁴`, factor 2 | 2.0 |
| K6 | `tanh`: `c₂=0`, `c₃=−1/3`, deep exponent 3 | slope 3.0000 |
| K7 | Langevin: `c₂=0`, `c₃=−1/15`, `g_N=g³/(15g_c²)` | −0.066667 |
| K8 | admissibility: `C=s=−c₂a₀`; Langmuir `c₂=−1` → `a₀` | 1.0 |
| K9 | biased tanh: capacity `a₀u/(1+u) ≤ a₀/2`, `R ≤ 2/3` | 0.5 |
| K10 | BI: `g` linear (no `g²`), `A=−g_N³/(2E²)<0`, `−0.2929a₀` | −0.292893 |
| K11 | BI caps `g`; the theory caps `A`: opposite topology | 0.9999995 |
| K12, K13 | mass action and grand canonical give the same Langmuir | 0 |
| K14 | capacity per site `q=a₀/N_s`; affinity = site's field = `a₀` | 0.01 (`N_s=100`) |
| K15 | two occupants: linear coefficient `1−N_max=−1` → `g_N<0` | −1e−3 |
| K16 | Fermi gate: `A(0)=a₀/2`, no real pole | 0.5 |
| K17 | n=1 pole `−a₀`; n=2 branch points `±ia₀/2` | 0.5 |
| K18 | `skew=(1−2θ)/√(N_sθ(1−θ))`; +0.707107 / −0.348327 at `a₀/2` | 0.707107 |
| K19 | flip at `a₀` (from the medium) vs `3a₀/8`; ratio 8/3 | 1.0 |
| K20 | opposite signs on all of `(0.375,1)a₀` | 0.0513 (min abs) |
| K21 | max split `2/√3−1=0.1547005`; knee curvature 0.0741 vs 0.1111 | 0.1547005 |
| K22 | wide binary 1 M☉/10 kAU: `y=0.634`, `Δv/v=7.40 %` | 0.073999 |
| K23 | `R=c₃c₁/c₂²` from the medium: +1 (Langmuir), 0 (n=2) | 1.0 |
| K24 | both laws homogeneous of degree 1 in `(g,a₀)` | 0 |
| K25 | capacity `a₀` vs `a₀/2`; at `g_N=a₀` anomaly 0.618 vs 0.414 | 0.5 |
| K26 | deep exponent 2 only at adsorption exponent `α=1` | 2.0000 |
| K27 | the medium reproduces the law to 2e−13 and `K W′=g` to 1e−15 | 1.1e−15 |
| K28 | half occupancy exactly at `g=a₀`; saturation at `a₀` | 0.5 |
| K29 | n=2: same `c₂=−1/a₀`, capacity `a₀/2` — violates `C=−c₂a₀` by 2 | 0.5 |
| K30 | skew `N(3σ)`: 918 / 6912 / 1.35e4 / 1.48e5 at φ=0.7/0.5/0.447/0.3 | 1.35e4 |
| K31 | the report's 9-point skew table reproduces for both laws | 4.9e−6 |

`MUTATE.md`: replacing the medium by `tanh` breaks K18, K19, K20, K23, K27, K28, K31 (24/31, exit 1)
and returns the dielectric's numbers (flip at 0.5493 a₀, skew +0.152, `R = ∞`); replacing it by the
n=2 element breaks the same seven plus K11 and returns **exactly** the n=2 predictions
(K18 → −0.34831, K19 → 0.375, K23 → 0, 23/31, exit 1). The checks bite on precisely the quantity
`n` encodes.

## What this does not do

- It does not derive `a₀` (BRIEF §4 input) or the site density `N_s`; `q = a₀/N_s` is fixed only in
  the combination `N_s q`.
- It does not supply the microscopic identity of the sites: the map from `T^φ_μν` to a gate density
  is not given (A2's caveat). "Medium class", not "material". The identification `u = A = K|P|` in
  the static sector (which licenses reading `W` as the integral of the isotherm) is inherited from
  A2/A33, not re-derived here.
- (P1) — mass action with linear adsorption and drive-independent desorption — is inherited from A2,
  now shown to be *forced* by `A(0)=0`, positivity and the deep exponent, but not derived from the
  action.
- The skew S/N uses `SE ≈ √(6/N)` (Gaussian) and an assumed occupancy fraction; a correlated medium
  rescales `N_s` and the magnitude.
- The wide-binary number is a circular-speed equivalent, not a full orbital-population model
  (eccentricity, projection, triples are not modelled).
- n=2's carrier is postulated (A35's caveat), and n=2 is excluded here only as a lattice / positive
  mixture. A gapless relativistic medium with an inserted capacity pole is not excluded.
- No EFE, no relativistic completion, no data fit of any kind.

## Next

1. **Measure the sign.** The skew at fixed `g_N` in `(0.10, 0.5)a₀`; one sign decides. The cheapest
   path is a stacked IFU sample (MaNGA/SAMI) with independently calibrated baryonic masses, where
   several points per galaxy fall in the window.
2. **Bound `N_s` from a null.** A measured `σ_s` converts to an occupancy fraction, hence to a bound
   on the gate density — a medium statement even if n is not decided.
3. **Calibrate the classification in the lab.** `R = χ₃χ₁/χ₂² = +1` for a Langmuir-class saturable
   medium, `0` for a self-depleting one: a day-scale experiment that makes the fingerprint physical.
4. **Tie `N_s` to `L_*`.** With `N_s = a₀/q` and a beam volume, `q` is the only unknown; A2's `L_*`
   route (24 pc) is the one length that could fix it.