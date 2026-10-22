# A35 — the two laws are two capacity-budget topologies, and least dissipation picks n = 1

Lane A35, `deepseek_push/DS_FINAL_2026_10_21/`. Inputs: `a0 = 9.36e-11 m s^-2` (BRIEF §4), `c = 2.99792458e8 m/s`, `kpc = 3.0856775814913673e19 m`. Reads `FINAL_THEORY.md` §2 and `A2_medium/report.md` first. Every algebraic statement below is a sympy remainder in `a35_checks.py` (zero = exact); every number is in `a35_results.json`.

## Claim

The harmonic identity `1/A = 1/g + 1/a0` is exact and it **is** a two-element series statement — of *compliances*, not impedances (the same equation is a **parallel** pair `g ‖ a0`; §1). The motive's second half is false, and exactly false: `sqrt(g²+a0²/4) − a0/2` is **not** the n=2 response — it is the n=2 **baryonic field `g_N`**, the quadrature (90°-phase) combination of `g` and `a0/2` shifted down by `a0/2`; at `g = a0` it is `φ = 1.618034` times the true response. The n=2 response is `A = g + a0/2 − sqrt(g²+a0²/4)`, whose exact constitutive form is `1/A = 1/g + 1/(a0 − A)`: a series string whose medium element is **self-limiting** (its admittance *is* its remaining budget), not an ideal reservoir. So the two laws are not two wirings of one element: they are the two **endpoints of one family**, a single capacity `a0` whose admittance is depleted by its own response at rate `λ`, with `n − 1 = λ`. Capacity `a0/(1+λ)` (`a0` at n=1, `a0/2` at n=2); deep limit `g_N = g²/a0 + O(g³)` for **every** `λ`, so the a₀-line can never select `n`; cubic coefficient `1−λ`, so n=2 is exactly the even member. The discrete selection is then sharp: only n=1 is a stationary point of the least-dissipation functional (n=2 residual `2−√5` at `g=a0`, excess energy `(9−4√5)a0/4`), and only n=1 has zero entropy production (n=2's occupancy is not a steady state at all, `σ > 0` everywhere). n=1 follows from *(i)* the element is linear in its order parameter and *(ii)* least dissipation; `θ_max = 1` then gives capacity = affinity = `a0`, with nothing fitted. The topology leaves one footprint — not in the mean law, which both wirings reproduce exactly, but in the **noise**: the skew of `δg` flips at `g = a0` for n=1 and at `g = 3a0/8` for n=2, with **opposite signs on `(0.375, 1)a0`**.

## Derivation

### 1. What the harmonic sum says, exactly

With `A ≡ g − g_N`, `x = g/a0`, `θ = x/(1+x)`:

```
A  = a0 θ = a0 g/(g+a0),      g_N = g θ = g²/(g+a0),      g = (a0+g) θ,        (1)
1/A = 1/g + 1/a0.                                                                 (2)
```

`1/A` is the total **reluctance**: the medium contributes the constant `1/a0`, the drive contributes `1/g`, and they add. Read as impedances, (2) is a **parallel** pair `Z1 = g`, `Z2 = a0` (`A = g a0/(g+a0)`); read as compliances it is a **series** pair. The compliance reading is the physical one, because the medium's constitutive variable is a displacement: two compliant elements in series, sharing `θ`, with `A = a0θ` and `g_N = gθ`. That `θ` is shared is not an assumption — it is the *output* of §7's variational principle. So (2) says: **the medium is one linear element of compliance `1/a0` in series with the drive, and all the nonlinearity sits in the divider fraction `θ = g/(g+a0)`, a pure ratio of drive to capacity.**

### 2. The n=2 branch: the motive's expression is `g_N`, not `A`

The n=2 law is `g² − g_N² = a0 g_N`, i.e. `g² = g_N² + a0 g_N`. Completing the square:

```
(g_N + a0/2)² = g² + a0²/4   ⇒   g_N = sqrt(g² + a0²/4) − a0/2     (exactly).        (3)
```

So `sqrt(g²+a0²/4) − a0/2` is the **transmitted** field: the hypotenuse of a right triangle with legs `g` and `a0/2`, minus the leg. It is a *quadrature* (reactive, 90°-phase) addition, not a parallel addition of conductances, and it lands on the baryonic branch. The response is its complement,

```
A₂ = g − g_N = g + a0/2 − sqrt(g² + a0²/4),   A₂(0)=0, A₂'(0)=1, A₂(∞)=a0/2,           (4)
1/A₂ = 1/g + 1/(a0 − A₂),     g = A(a0 − A)/(a0 − 2A),     A₂² − A₂(2g+a0) + a0 g = 0.  (5)
```

and at `g = a0` the ratio `(3)/(4)` is `φ = 1.618034` (K2). (5) is the finding: n=2 is a series string in which the medium's admittance is its **remaining budget** `a0 − A`, not a constant. It saturates where response meets headroom, `A = a0 − A`, hence capacity `a0/2`. The factor 2 comes from that meeting, not from a wiring.

### 3. One capacity, two budget topologies: `n − 1 = λ`

Give the element the law `Y_m = a0 − λA` (admittance = budget minus `λ` times its own response). Then `1/A = 1/g + 1/(a0 − λA)`, i.e. with `G = g/a0`, `x = A/a0`:

```
G = x (1 − λx)/(1 − (1+λ)x).                                                        (6)
```

`λ = 0` is the **ideal reservoir** (admittance `a0` whatever it is doing — n=1, capacity a property of the vacuum, not of the response). `λ = 1` is the **fully self-depleting** element (admittance = unused budget — n=2, (6) reduces to (5)). `λ > 1` gives negative admittance at large `A`, so the physical interval is `λ ∈ [0,1]`. Hence **`n = 1 + λ`, and `n − 1` is the depletion fraction of the capacity**: the two laws in the record are the endpoints of the only interval with positive admittance, which is why only those two appear and why they are the only two that could.

### 4. Capacity, deep limit, cubic coefficient

The capacity is the pole of (6) in `x`, `x_max = 1/(1+λ)`:

```
A_max = a0/(1+λ):   a0 (n=1),  a0/2 (n=2),   ratio 2  (K4).                          (7)
```

The task's capacity statement is right in its numbers, wrong in its mechanism: `a0` vs `a0/2` is not produced by re-wiring a fixed element set (§6), but by depletion. Inverting (6) at small `G`:

```
g_N/a0 = G² − (1−λ) G³ + O(G⁴)   ⇒   g = sqrt(a0 g_N)(1 + O(g_N/a0))  for every λ.    (8)
```

Two exact consequences. **(a)** The deep limit measures the *affinity* scale `a0`, not the capacity — no deep-limit observation can select `n` (K5). **(b)** The cubic coefficient is `1−λ`: n=1 has 1, n=2 has 0, so n=2 is the unique **even** member (K6) — A2's evenness criterion is exactly `λ = 1`.

**Capacity = affinity, derived.** Write the medium as a linear element in its order parameter, `A = a0θ`, `θ ∈ [0,1]`. Then `C ≡ A(θ=1) = a0` *because the order parameter is normalised*, and the affinity `s` (drive at which `θ = 1/2`) is `a0` because `θ = g/(g+a0)`. Hence `C = s = a0`: the single scale is used twice because `θ_max = 1`, not because two constants were fitted. (A2's K5 reached `C = s` from the vanishing linear term; this is the same statement as a normalisation.)

### 5. What plays the role of the impedance

Static: `Z_dc = 1/A = 1/g + 1/a0`, a pure **resistance** `1/a0` in the acceleration domain; differentially, with `x = A/a0`,

```
Z₁ = dg/dA = (1 + g/a0)²,        Z₂ = (1 − 2x + 2x²)/(1 − 2x)²,                       (9)
Z₁(0)=Z₂(0)=1,  Z₁(a0)=4,  Z₂(a0)=5+2√5=9.472136,  Z₂→∞ at x=1/2.                     (10)
```

The three candidates, scored. **Stiffness `K`: not the impedance** — it cancels from the equation of state identically, `K W'(u) = a0u/(a0−u)`, no `K` (K14); it sets the energy density `a0²/K`, not the response. **Inertia: the inductance, not the resistance** — the gate's relaxation `τ θ̇ = θ_eq − θ` gives a Debye compliance `C(ω) = C_dc/(1+iωτ)`, hence `Z(ω) = Z_dc(1+iωτ)`, a **series R–L** with `R = Z_dc`, `L = τZ_dc`; the inertia enters only as `L`. **Relaxation time: yes** — the only carrier of the reactive part, `τ = L/c_s` with `c_s = sqrt(γ/η) ≤ c` (A3). For a 10 kpc element `τ = 3.262e4 yr`; for a 200 km/s orbit `ωτ = 6.671e-4`, phase `0.0382°` (K15): the reactive part is `6.7e-4` of the resistive part, so **the RAR is a dc measurement** and cannot see the inertia.

**Verdict: the impedance is the medium's reluctance `1/a0` (dc) and its relaxation time (ac). The stiffness drops out; the inertia is the series inductance, unobservable in the RAR.**

### 6. Why the wiring cannot be the discriminator: a 2-element network is self-dual

Compose `N` identical Langmuir elements `(c,s)`. Series (same response, drives add) gives `A = cg/(g+Ns)` — capacity `c`, affinity `Ns`. Parallel (same drive, responses add) gives `A = Ncg/(g+s)` — capacity `Nc`, affinity `s`. Both are Langmuirs, and **both reproduce the canonical law exactly**: parallel with `(c=a0/N, s=a0)`, series with `(c=a0, s=a0/N)` (K8). The static law is *exactly degenerate* between the two wirings. Composition never lowers capacity below the smallest element's (`c` series, `Nc` parallel), so `a0/2` is unreachable from capacity-`a0` elements by any wiring (K8). The naive "responses add" parallel — a constant source `a0` across the drive — gives `A = g + a0`, hence `g_N = −a0 < 0`: excluded outright by positivity of the baryonic field (K7).

The structural reason is stronger: for two elements, *series compliance* and *parallel stiffness* are the **same equation**, `1/k = 1/k₁ + 1/k₂`. A two-element network is self-dual under `Z ↔ 1/Z` and carries **no topological information**. Topology becomes physical only through (a) the element's constitutive law — §3's `λ` — or (b) the number of independent coordinates, which is a noise statement (§9).

### 7. Least dissipation: the discrete selection

**Requirement (i) is degenerate.** Both laws vanish with the drive and with `a0`, and both have unit slope at the origin: `A(0)=0`, `A(a0→0)=0`, `A'(0)=1` for n=1 *and* n=2 (K22, exact limits). The vanishing conditions therefore cannot select `n` — the whole selection rests on requirement (ii), the stationarity of the dissipation functional.

Two channels share the drive: the medium channel, stiffness `a0`, displacement `θ_A` (`A = a0θ_A`), and the transmitted channel, `g_N = gθ_N`. The drive is the sum of the forces, `a0θ_A + gθ_N = g`. Minimise the stored (equivalently dissipated) quadratic form

```
U = ½ a0 θ_A² + ½ g θ_N²    s.t.  a0θ_A + gθ_N = g                              (11)
⇒ θ_A = θ_N = g/(g+a0)   (Lagrange; K9)   ⇒   A = a0 g/(g+a0).                     (12)
```

The common occupancy — the series topology — is **derived**, not imposed. On the constraint surface `U` reduces to

```
Ψ(A) = A²/(2a0) + (g−A)²/(2g),   Ψ'(A) = A/a0 − (g−A)/g,   Ψ'' = 1/a0 + 1/g > 0,     (13)
Ψ'(A)=0  ⇔  A = a0g/(g+a0)  ⇔  n = 1,   uniquely (strict convexity).                (14)
```

This is the Onsager/Thomson functional: Joule power in the resistive representation, stored energy in the elastic one — the same stationarity condition, the two being Legendre twins. For n=2 the same functional gives

```
R ≡ Ψ'(A₂) = A₂/g + A₂/a0 − 1:  R(a0) = 2−√5 = −0.236068,  R ≠ 0 ∀g,  R → −½;          (15)
Ψ(A₂) − Ψ(A₁) = (9−4√5)a0/4 = 0.013932 a0  at g=a0,   sup = a0/8.                      (16)
```

The variational image is exactly `{Langmuir(C)}` for *any* capacity `C` (K11: the `g²` coefficient forces `C = a0`, the `g³` coefficient is then `−1/a0 ≠ 0`), so n=2 is outside the image for **every** capacity, not just `a0`. The discrete content is the binary property `λ = 0` vs `λ > 0` — *does the element's own response consume its capacity?* — and only `λ = 0` is stationary. **This is the sharpest derivation of n=1 available: two premises (linear element, least dissipation), no fitted number.**

### 8. n=2 is not a steady state of the medium

With A2's grand-canonical closure `μ(g) = kT ln(g/a0) − ε` (A2 eq. 6), the free energy `F(θ) = kT[θlnθ+(1−θ)ln(1−θ)] − (μ+ε)θ` satisfies

```
F'(θ)/kT = ln[θ/(1−θ)] − ln(g/a0) = 0  ⇔  θ = g/(g+a0) = θ₁.                        (17)
```

At the n=2 occupancy `θ₂ = 2A₂/a0` (capacity `a0/2`), `θ₂ > θ₁` for every `g` (over-occupied), and

```
F'(θ₂)/kT = ln 2φ = 1.174359 at g=a0,  → ln 4 = 1.386294 as g→∞;  never zero.      (18)
```

The entropy production `σ(θ) = [g(1−θ) − a0θ]ln[g(1−θ)/(a0θ)] ≥ 0` vanishes **iff** `θ = θ₁`; at `θ₂` it is `0.619902 a0 k_a` at `g = a0` and positive for all `g` (K13). A single site has no cycle, so every steady state is detailed-balanced: **`σ > 0` means `θ₂` is not a steady state — the n=2 law is a transient, not a state.** (A cyclic NESS could run at `σ > 0`, but then the response would not be a function of `g` alone, which the law requires.)

### 9. The discriminator that does follow: noise

Binomial occupancy, `N_s` objects, `Var(θ) = θ(1−θ)/N_s`, `δg = Cδθ/(1−A')`:

```
σ(log g)|_{g_N} = C sqrt(θ(1−θ)/N_s) / [(1−A') g ln10],    μ₃ = N_s θ(1−θ)(1−2θ).   (19)
```

| quantity | n = 1 | n = 2 |
|---|---|---|
| `σ(0.3a0)/σ(3a0)` | **22.3422** | **34.4859** |
| `σ(a0)/σ(10a0)` | **22.9984** | **30.3822** |
| asymptotic slope | −1.4998 | −1.5000 |
| skew flip (`θ=1/2`) | `g = a0` | `θ₂=1/2 ⇔ A=a0/4 ⇔ g = 3a0/8 = 0.375a0` |
| skew at `g = a0/2` (`N_s=1`) | **+0.7071** | **−0.3483** |
| Nyquist `S ∝ 4kT Re Z` at `g=a0` | 1 | **2.368034** = `(5+2√5)/4`, divergent at `a0/2` |

The n=1 column reproduces A2's K12/K13 exactly (22.34/34.49, 23.00/30.38, flip at `a0`), so this
is A2's noise model extended to the second element, not a new one. So "different skewness signs,
and where" has a precise answer: the **sign pattern is the same** (each law flips once), but the **flip location differs by a factor 2.667** and the two signs are **opposite on `g/a0 ∈ (0.375, 1)`** — at `g = a0/2`, `+0.7071` vs `−0.3483`. That window is where a measurement should look; one sign there decides the element. The Nyquist ratio is `T`-free (a ratio at the same `T`) but needs `T ≠ 0`, and the cold sector's temperature is not predicted — if it is 0 the Johnson channel vanishes for both, leaving the occupancy skew as the practical discriminator. Caveat: n=1's carrier is *derived* (the gate whose steady state is the law), n=2's two-state carrier is *postulated*; if n=2 is instead a coherent reactive element it has **no dc occupancy noise at all**, and the discriminator becomes noise vs no noise.

Finally, the wiring *is* observable in the noise although invisible in the law: a series string of `N` gates shares one collective coordinate, so `Var(A) = a0²θ(1−θ)` with no averaging, while a parallel array of `N` has `Var(A) = (a0²/N)θ(1−θ)`. **Ratio `N`** (K20).

## Status

**DERIVED n=1** from (linear element in the order parameter) + (least stored energy / Onsager), no fitted number — the vanishing conditions alone are degenerate (K22) and cannot select; **NO-GO n=2** as (a) any series/parallel composition of capacity-`a0` elements — the composite capacity is `c` or `Nc`, never `a0/2` — and (b) a stationary point of the least-dissipation functional, residual `2−√5` at `g=a0` and nonzero everywhere, for *every* capacity; **CONDITIONAL(A2 P1: mass-action closure)** for the entropy-production version of the same selection; **NUMERICAL** for the discriminator (skew flip at `a0` vs `0.375a0`, ratios 22.34/34.49).

## Checks

`a35_checks.py` prints `<id> PASS|FAIL <measured> <threshold>`, ends `A35 COMPLETE: 22/22 checks PASS.`, exit 0; `a35.out` is the captured run (0.75 s).

| id | what it proves | measured |
|---|---|---|
| K1 | (1)–(2) exact; harmonic sum in both readings | 0 |
| K2 | the motive's `sqrt(g²+a0²/4)−a0/2` **is `g_N`**, not `A`; ratio `φ` at `g=a0` | 0, 1.618034 |
| K3 | (5): `1/A = 1/g + 1/(a0−A)`; quadratic form | 0 |
| K4 | (7) capacity `a0/(1+λ)`; `a0` vs `a0/2` | 1.0 (ratio 2) |
| K5 | (8) same deep limit for both and for `λ = ¼,½,¾` | 0 |
| K6 | cubic coefficient `1−λ`; n=2 even | 1.0e-3 |
| K7 | naive parallel: `g_N = −a0 < 0`, no capacity — excluded | −1 |
| K8 | both wirings give the *same* law; composite capacity `Nc`/`c`; `a0/2` unreachable | 0 |
| K9 | (11)–(14): Lagrange derives `θ_A=θ_N`; unique minimum = canonical law | 0 |
| K10 | (15)–(16): residual `2−√5`, excess `(9−4√5)/4`, `R → −½` | −0.236068 |
| K11 | n=2 is not `Langmuir(C)` for any `C` | 0 |
| K12 | (17)–(18): `F'(θ₁)=0`, `F'(θ₂)=kT ln2φ → kT ln4`, `θ₂>θ₁` | 1.174359 |
| K13 | `σ(θ₁)=0`, `σ(θ₂)>0` everywhere | 0.619902 |
| K14 | `K` cancels; `Z₁(a0)=4`, `Z₂(a0)=5+2√5` | 9.472136 |
| K15 | Debye `Z=Z_dc(1+iωτ)`; `ωτ=6.671e-4`, phase `0.0382°` | 6.671e-4 |
| K16 | (19) ratios 22.3422/34.4859, 22.9984/30.3822; slope −1.4998 | 22.3422 |
| K17 | skew flips at `a0` vs `3a0/8`; opposite signs at `a0/2` | 0.375 |
| K18 | Nyquist ratio `(5+2√5)/4`; divergence at `a0/2` | 2.368034 |
| K19 | both laws homogeneous degree 1 in `(g,a0)` | 0 |
| K20 | wiring noise ratio `= N` (one coordinate vs `N`) | 8 |
| K21 | the *identified* law's discriminator is the n=1 one (flip `a0`, ratio 22.34) | 1.0 |
| K22 | (i) is degenerate: `A(0)=0`, `A(a0→0)=0`, `A'(0)=1` for **both** laws | 2 |

`MUTATE.md`: making the element self-depleting (`λ = 1`) breaks K1, K4, K9, K21 and leaves the 17 law-level/algebraic checks standing — the mutation bites exactly the identification.

## What this does not do

- It does not derive `a0`; `a0` is an input (BRIEF §4), consumed once (the element's stiffness).
- It does not prove the least-dissipation principle from the action. §7 uses it as a principle; §8's kinetic selection does not depend on it, which is why both are reported.
- The series-string noise is treated by counting independent coordinates (1 vs `N`), not by a full Langevin solution of the constrained string.
- `T_cold` is not predicted, so the Nyquist statement is a ratio only.
- The "not a steady state" argument is for a single site / acyclic network; a cyclic NESS is excluded only because the law is a function of `g` alone.
- No data were used. The skew-flip window is a pre-registration, not a measurement.

## Next

1. **The cheap decisive measurement**: the sign of `skew(δg)` at fixed `g_N` in `g/a0 ∈ (0.375, 1)`. One sign separates the elements; no amplitude calibration, no `N_s`.
2. **The wiring measurement**: the variance ratio `N` at fixed law (§9) — a beam-size scan of the intrinsic scatter at fixed `g_N` measures the number of independent coordinates, which the mean law cannot see.
3. **Upgrade §7 from principle to derivation**: is `W(u)` the minimum of a functional of the `P`-field at fixed `g`? If yes, the last premise of the n=1 derivation disappears.
