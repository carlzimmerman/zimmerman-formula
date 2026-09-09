# L59 — second-order covariant scalars: the lock survives, but **PAPER9 must be amended before deposit**

2026-09-09. Lane L59 of [CHARTER.md](CHARTER.md), answering the single open computation named by
[L39_NONLOCAL_MODES.md](L39_NONLOCAL_MODES.md) §7 item 1 and by PAPER9's "what is not proved" item 2.
Script: [`L59_second_order_scalars.py`](L59_second_order_scalars.py) →
[`L59_second_order_scalars.out`](L59_second_order_scalars.out). **46 checks, 42 PASS / 4 FAIL.**
Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) on every dimensional number.

Method: nothing under `closure_2026/` or the lead agent's directories was imported, executed or copied.
The symbolic algebra — Christoffels → Riemann → the four quadratic invariants, the transverse-operator
and transverse-bilinear-kernel solves, the quadratic Einstein–Hilbert action in static longitudinal
gauge, the Euler–Lagrange variation — was built from scratch in sympy here. L39's, L51's, L31's and
L57's load-bearing numbers are re-derived as **controls**, not inherited. 13 controls, all PASS.

---

## The verdict, first — and the first line is the amendment

> **PAPER9 must be amended before deposit.** Its stated reason for setting second-order scalars aside is
> **false**. The sentence, verbatim from the paper (§"what is not proved", item 2) and from L39 §7:
>
> > "Scalars beginning at second order — Kretschmann, `R_μνR^μν`, `C²` — do separate `Φ` from `Ψ` and are
> > *not* covered. **They are, however, exactly the objects step E showed to be uniform-field blind and
> > nearest-star dominated.**"
>
> The bolded clause is true of the **local** second-order scalars and **false of the nonlocal ones**, by
> a factor **2.2 × 10⁶ in the wrong direction**. An exact identity, proved here, turns `□⁻¹` of a
> quadratic curvature invariant into the square of the **coherent** acceleration. Step E's obstruction
> does not touch it.
>
> **The conclusion nevertheless stands. The lensing lock survives at second order** — for three
> different reasons, none of which is the one the paper gives. The theorem is unchanged; the argument on
> the way to it is wrong, and it is wrong in a public paper about to receive a DOI.

**The answer to L39's question, in L39's own form.** *Is there a nonlocal scalar, quadratic or higher in
curvature, that both separates the Newtonian from the lensing potential AND remains sensitive to the
coherent coarse-grained field?* **Yes to both halves as L39 posed them, and it is still excluded.** The
object exists, it separates, it sees the coherent field — and it fails on three requirements L39's
question did not contain. So hypothesis (iv) is **not** removable outright by the argument PAPER9 offers;
it is removable by the arguments below, over the quadratic-curvature class, with the residual named in §7.

---

## 1. Controls (13, all PASS)

| control | L39 / L51 / L31 / L57 | here |
|---|---|---|
| A1 transverse symmetric operators `O^{μν}(k)` | 1 without `ū`, 2 with | **1 / 2**, by a numerical rank solve at random `k` (independent method) |
| A2a–c linearised curvature of the static two-potential metric | `R_00 = ∇²Φ`, `R^(1) = 2∇²(2Ψ−Φ)`, `G_00 = 2∇²Ψ` | **identical**, from the exact nonlinear metric |
| A3 L51's exhibited pair and determinant | `[[−2,4],[1,0]]`, **det = −4** | **identical** |
| A3b L39's lock ratio | 1 : 2 | **identical** |
| A4a/a2 quadratic Einstein–Hilbert action, varied | — | `δL/δΦ = 4∇²Ψ`, `δL/δΨ = −4∇²Ψ + 4∇²Φ` ⇒ `∇²Ψ = 4πGρ`, `Φ = Ψ` |
| A4b **the locked identity** for a frame-free first-order addition | `∇²(Φ+Ψ) = 8πGρ` exactly | **`D_Ψ + 2D_Φ = 0` identically, for any weight** |
| A4c the `u`-built block does not satisfy it | — | `D_Ψ + 2D_Φ = 2∇²w ≠ 0` |
| A5 uniform field leaves the Hessian unchanged | exact | **exact** |
| A6 **Step E's central number** | 1488× | **1487.6× on both footings** |
| A7 Step E's physical numbers | 8.19e-31 s⁻², 9.03e-30 s⁻², `d_eq` = 2.23 pc, 99.0% | **8.191e-31, 9.036e-30, 2.23 pc, 99.0%** |
| A8 L57's cube law | `∫ρ_ℓ² ∝ ℓ⁻³` | **slope −3.000000** |
| C1/C2 the new identity, symbolic and on a grid | — | residual **0** symbolically, **1.9e-7** on a 64³ FFT |
| E1a `∇⁻²` raises a power-law exponent by 2 | — | exact at five test exponents |

**The master equations**, derived here from the action rather than quoted, are what the whole lane runs
on. With `ds² = −(1+2Φ)dt² + (1−2Ψ)δ_ij dx^i dx^j` and `D_Φ = δΔS/δΦ`, `D_Ψ = δΔS/δΨ`:

    ∇²Ψ      = 4πG(ρ − D_Φ)
    ∇²(Φ−Ψ)  = −4πG D_Ψ
    ∇²(Φ+Ψ)  = 8πGρ − 4πG( D_Ψ + 2 D_Φ )
    ∇²Φ      = 4πG(ρ − D_Φ − D_Ψ)

so **the locked identity holds ⟺ `D_Ψ + 2D_Φ = 0`**, and **the lensing is correct ⟺ `D_Ψ = 0`**. Those
two criteria carry the rest of the lane.

---

## 2. The enumeration, done rather than sampled

**B1 — the counting extends, and the answer changes.** A covariant scalar whose expansion begins at
second order has `S^(2) = ∫h_μν M^{μν,αβ} h_αβ`, and because its first-order piece vanishes identically
its second-order piece is invariant under *linearised* gauge transformations by itself, forcing
`k_μ M^{μν,αβ} = 0`. Building the most general symmetric `M` from the available structures and imposing
transversality by an explicit rank computation:

| | first order (`O^{μν}`) | second order (`M^{μν,αβ}`) |
|---|---|---|
| no preferred vector | **1** | **2** |
| one unit timelike `u` | **2** | **5** |

**So a frame-free theory does gain a second structure at second order.** That is exactly the gap, and it
is real: the spin-2 and spin-0 transverse projectors.

**B2 — the complete basis.** In four dimensions the parity-even quadratic curvature scalars are exactly
three. Computed here at `O(h²)` from the exact metric and resolved on the six independent structures a
static two-potential field admits (`P2 = (∂_i∂_jΦ)²`, `S2 = (∂_i∂_jΨ)²`, `X = ∂∂Φ·∂∂Ψ`, `LP = (∇²Φ)²`,
`LS = (∇²Ψ)²`, `LX = ∇²Φ∇²Ψ`):

| invariant | P2 | S2 | X | LP | LS | LX |
|---|---|---|---|---|---|---|
| `R²` | 0 | 0 | 0 | 4 | 16 | −16 |
| `R_μνR^μν` | 1 | 1 | −2 | 1 | 5 | −2 |
| `R_μναβR^μναβ` | **4** | **4** | 0 | 0 | 4 | 0 |
| Gauss–Bonnet | 0 | 0 | 8 | 0 | 0 | −8 |

Every one resolves exactly, so the basis is complete for the static weak field and the enumeration below
is exhaustive rather than a sample. Kretschmann collapses to L31's `K = 8(∂_i∂_jΦ)²` on `Φ = Ψ` in
vacuum, reproducing the linearised dictionary.

**B3 — Gauss–Bonnet is Euler-trivial unweighted and NOT weighted.** So the weighted / nonlinear
enumeration carries **three** invariants where the pure quadratic action carries two. Both counts are
kept.

**What is in the span, checked and stated:** `Weyl² = K − 2R_μνR^μν + R²/3`; Gauss–Bonnet; every dressing
`R F(□) R`, `R_μν F(□) R^μν`, `R_μναβ F(□) R^μναβ` with `F` **any** function — `□⁻¹`, `□⁻²`, `exp(ℓ²□)`,
`(1−ℓ²□)^{-n}`; and `F(Q₁,Q₂,Q₃)` for any `F`, analytic or not, which at linear response is a **weight**.
The parity-odd Pontryagin density `R*R` vanishes identically on any static two-potential configuration
and is carried, not ignored. So the complete space of achievable additions to the static field equations
is

    ΔS = ∫ w · ( λ₁ R² + λ₂ R_μνR^μν + λ₃ R_μναβR^μναβ ),    w arbitrary, λ arbitrary,

and both criteria of §1 can be applied to it in closed form.

**B4 — they do separate.** The lock-preserving subspace of the three-parameter family is
**one-dimensional** — it is `λ₂ = λ₃ = 0`, i.e. `R²` alone, and B5b shows why: it is the *square of the
locked combination*, resolving as `4LP + 16LS − 16LX`, a perfect square in `(∇²Φ, ∇²Ψ)`. Every other
member breaks `∇²(Φ+Ψ) = 8πGρ`. **L39's own statement is confirmed: the first-order lock's exact identity
does not survive to second order.**

**B5 — but `D_Ψ = 0` has only the trivial solution.** Correct lensing requires the addition to be blind to
the spatial-curvature potential `Ψ`. Solved as a linear system over `(λ₁,λ₂,λ₃)`: the solution space is
**zero-dimensional**. Picking out `Φ` alone is precisely what `R_μν u^μ u^ν` does and precisely what no
frame-free scalar can do — the same content as the first-order lemma, one order up.

---

## 3. THE HOLE — the identity that defeats Step E

For the tidal invariant `Q = (∂_i∂_jΦ)(∂^i∂^jΦ)`, proved symbolically (C1) and verified on a grid (C2):

    Q  =  ½ ∇²( |∇Φ|² )  −  ∇Φ · ∇( ∇²Φ )

hence, applying `∇⁻²` with decaying boundary conditions,

    U ≡ ∇⁻² Q  =  ½ |∇Φ|²  −  4πG ∇⁻²( ∇Φ · ∇ρ ) .

**The first term is MOND's variable.** For a point mass the decaying solution is exactly `U = ½|∇Φ|²`
(C2b, symbolic). `□⁻¹` of a quadratic curvature invariant *reconstructs the square of the coherent
acceleration* — which no local invariant can do, and which is the whole reason nonlocality buys something
at second order that it did not buy at first order.

**Put Step E's own configuration to it** (C4): a solar mass at 1 pc, inside the Milky Way at `R_☉`.

| | star at 1 pc | coherent Galaxy | who wins |
|---|---|---|---|
| **LOCAL** invariant (tidal, s⁻²) | 9.036e-30 | 8.191e-31 | **star, by 11.0×** |
| **NONLOCAL** `U = ∇⁻²Q`, vacuum part (m² s⁻⁴) | 9.718e-27 | 2.148e-20 | **coherent, by 2.21e6×** |

and `√(2U_coherent)/a₀` returns **2.2138** (canonical) / **1.8375** (alt) — *exactly* the true galactic
`y`, on both footings, where the local invariant returns 1.5e-3 / 1.2e-3. **A 2.4 × 10⁷ reversal.**

**What does survive of Step E** (C5): a strictly *uniform* external field. Under `Φ → Φ + g·x` the change
in `½|∇Φ|²` is `2g·∇Φ + g²`, which is **harmonic** wherever `∇²Φ = 0` and therefore lives entirely in the
kernel of `∇⁻²`. So `U` reconstructs the field of **bounded sources** and is blind to a strictly uniform
one. Real external fields are sourced, so this costs the external-field effect in the infinite-distance
idealisation, not the coherent field of a real galaxy. **Step E's uniform-field blindness survives
exactly; its nearest-star domination does not.**

---

## 4. The obstruction that replaces it, and the length it demands

The *second* term of the same identity is the new obstruction, and it is not Step E's. Since
`∫∇Φ·∇ρ = −4πG∫ρ²` (C2c, verified on the grid to 2e-3), every compact object contributes a monopole
`4πG²(∫ρ²)/d` to `U`. `∫ρ²` is enormous inside a star: **the invariant is dominated by stellar
interiors.**

**D1, unsmoothed, at the Sun** — with `∫ρ² = M²/V` for a *uniform* Sun, a conservative lower bound since
real stars are centrally concentrated:

    U_grain  = 6.202e+04 m² s⁻⁴          U_coherent = 2.148e-20 m² s⁻⁴
    graininess / coherent = 2.89e+24

**D2, smoothed.** With L57's cube law `∫ρ_ℓ² = m²/(8π^{3/2}ℓ³)`, the coherence condition is

    ℓ_crit³  =  G m |Φ_pop| / ( √π g² )        ⇒        ℓ_crit = r ( m / (√π M) )^{1/3}

— **the local mean separation between the discrete masses.** That is a property of a system's
granularity, not a constant of nature. Computed for five environments (a₀ enters through the MOND
acceleration `g = g_N ν(g_N/a₀)`):

| environment | `g_N/a₀` (can/alt) | `ℓ_crit` canonical | `ℓ_crit` alt |
|---|---|---|---|
| MW solar neighbourhood | 2.21 / 1.84 | **1.202 pc** | 1.171 pc |
| MW outer disc, 30 kpc | 0.0993 / 0.0824 | 2.641 pc | 2.505 pc |
| dSph (Draco-like) | 0.0112 / 0.00927 | 0.533 pc | 0.502 pc |
| globular cluster (NGC 2419) | 3.35 / 2.78 | 0.148 pc | 0.145 pc |
| galaxy cluster (granules = galaxies) | 0.149 / 0.124 | **38 542 pc** | 36 631 pc |

**A factor 2.6e5 (canonical) / 2.5e5 (alt).** The theory's own coherence length `ξ = 4.00 pc` (L47,
outside-J placement, identical on both footings) suffices in **4 of 5** environments and is short by
**9.6e3× / 9.2e3×** at the worst. L57 independently needed `ℓ_rms ≥ 600 kpc` for the same clusters, from
the shear data rather than from graininess — two different routes to the same order of magnitude.

**D4 — and the smoothing must be covariant.** A spatial smoothing needs a slicing (L57 B4), which is the
preferred foliation the theorem is about. The covariant options:

| covariant smoother | poles added | cost |
|---|---|---|
| `(1 − ℓ²□)^{-1}` | 1, at `□ = 1/ℓ²` | a propagating mode; tachyonic |
| `(1 − ℓ²□)^{-n}`, `n ≥ 2` | `n` | `n` modes, alternating ghost signs |
| `exp(ℓ²□)` (entire) | **0** | anti-diffusive in **time**; no well-posed Cauchy problem |
| `□⁻¹` alone | 0 | **no suppression of compact sources at all** |

The entire (infinite-derivative) family is the only ghost-free one, and its cost is exactly the
DEFW-class cost L39 already priced: an effective classical equation with no variational or causal
definition. **This lane does not close the route on Ostrogradsky and does not claim to.**

---

## 5. The two-sided test, and the two things that kill it

### E1 — THE HOMOGENEITY PINCER (and it needs no smoothing at all)

A flat rotation curve is `Φ = α ln r` with `α = v²`, and MOND fixes `α² = GMa₀`, so the **same** vacuum
equation must admit the log potential for **every** `α`. The Einstein–Hilbert term contributes
`∇²Φ = α/r²`: linear in `α`, going as `r⁻²`.

Let the addition be `F = Π_n U_n^{d_n}` with `U_n = □⁻ⁿ(a quadratic invariant)` — the complete dressed
family of B4, `n = 0` local, `n = 1` the one that reconstructs `|∇Φ|²`, `n ≥ 2` deeper. On the log
potential `U_n ~ α² r^{2n−4}`, the weight in slot `n` is `w_n = □⁻ⁿ(∂F/∂U_n)`, and the resulting field-
equation contribution goes as `α^{2Σd−1} r^{Σ(2n−4)d_n}`. Two conditions:

    radial profile :  Σ_n (2n−4) d_n = −2
    mass scaling   :  2 Σ_n d_n − 1 = 1        ⇒   Σ_n d_n = 1

**The second forces total degree 1 for every dressing** — the addition is *exactly quadratic in `h`* and
the field equations are **linear**. The local corner (`d = e₀`) needs `d₀ = 1/2` and violates `Σd = 1`;
the nonlocal corner (`d = e₁`) needs `d₁ = 1` and satisfies both — **and `d₁ = 1` is the linear one.**

**E2 — what linearity costs.** A linear theory superposes, so `g_obs` is a linear functional of `ρ`:

| | MOND | linear survivor |
|---|---|---|
| transition radius over 10⁸–10¹² M☉ | `r_M = √(GM/a₀)`: 0.386 → 38.6 kpc (canonical), 0.352 → 35.2 kpc (alt) — **spans 100×** | one fixed length, **ratio 1** |
| Tully–Fisher | `v⁴ ∝ M` (v = 33.4/105.6/333.9 km/s canonical; 35.0/110.6/349.8 alt) | `v² ∝ M`, i.e. `v⁴ ∝ M²` |

**The unique member surviving the pincer is not a MOND theory at all** — it is a linear modification with
a length, which is the L5/L17 class this programme already closed.

### E3 — and the lensing deficit is a fixed number

Setting the pincer aside, define the lensing efficiency
`η = [∇²(Φ+Ψ)/2]_added / [∇²Φ]_added = (D_Ψ + 2D_Φ)/(2(D_Φ + D_Ψ))`; `η = 1` is correct lensing.
E1 already fixed the weight the flat rotation curve requires: `w ~ r²`, i.e. `p = 2`. At `p = 2`, on the
no-slip background it perturbs, evaluated at two independent sample points:

    numerator   = −10800 λ₃ / 251          denominator = −14400 λ₃ / 251
    η = 3/4      EXACTLY, and INDEPENDENT of (λ₁, λ₂, λ₃) — λ₁ and λ₂ drop out of both forms.

**Every frame-free second-order term under-lenses by exactly 25% at the weight a flat rotation curve
requires**, and the deficit cannot be tuned away because the entire three-parameter family gives the same
number — or, at `λ₃ = 0`, no modification at all. Away from `p = 2`, `η = 1` *can* be arranged on any
single configuration; **E3b** stacks the `η = 1` conditions over eight configurations and finds **rank 3
of 3**, so the only frame-free term with correct lensing everywhere is the zero one. That is the
numerical form of B5.

### E4 — both conditions at one smoothing length?

**Yes for one system, no for all of them.** The separation test is algebraic and holds at every `ℓ`; the
coherence test holds for `ℓ ≥ ℓ_crit`. So for a single system both can be met at one `ℓ` — that is the
honest answer to the brief's question. What cannot be met is the pair with **one** `ℓ` across systems
(2.6e5), and what cannot be met at **any** `ℓ` is the third requirement neither test contains: that the
separation go in the direction lensing needs, and that the term be nonlinear enough to carry an
acceleration scale.

---

## 6. The requirements ledger

The candidate, in full: **a frame-free covariant addition `ΔS = ∫√−g F(□⁻¹ Q_smoothed)`**, `Q` a quadratic
curvature invariant, smoothed with an entire covariant form factor on a length `ℓ`. It is the only object
the enumeration leaves, it is exactly what L39 §7 asks for, and it is **not a straw man**.

| | requirement | verdict |
|---|---|---|
| R1 | separates `Φ` from `Ψ` | **PASS** — the lock-preserving subspace is 1 of 3 |
| R2 | coherent-dominated, not nearest-star dominated | **PASS** — by 2.21e6×, where the local invariant loses by 11.0× |
| R3 | adds no propagating mode | **PASS** — entire or purely-IR-nonlocal form factors are ghost-free; `N_grav = 2` |
| R4 | the separation goes the way lensing needs (`η = 1`) | **FAIL** — `η = 3/4` exactly, for the whole family |
| R5 | nonlinear enough to carry an acceleration scale | **FAIL** — degree forced to 1; `v⁴ ∝ M²`, one fixed length |
| R6 | one fixed covariant `ℓ` works in every system | **FAIL** — `ℓ_crit` spans 2.6e5; `ξ = 4.00 pc` short by 9.6e3× |

**Three of six met. The three failures are independent, and any one of them is fatal.**

---

## 7. What is still not proved — named as precisely as L39 named its own gap

1. **E1's pincer assumes asymptotic homogeneity.** It takes the deep-MOND limit to be an exact power law
   and `F` to be asymptotically homogeneous in the invariants. A genuinely non-homogeneous `F` — an
   interpolation that never reaches a power law — is not covered. **THE MISSING COMPUTATION:** *does the
   flat-rotation-curve requirement, imposed over a finite range of radii and masses rather than
   asymptotically, still force total degree 1?* This is a strictly smaller target than L39's was.
2. **`η = 3/4` is a linear-response result** about the no-slip background. Its backreacted, fully
   nonlinear value is not computed here. The sign and the `O(1)` size are robust; the exact `3/4` is not
   claimed beyond linear response.
3. **Cubic and higher invariants are not enumerated.** `R³`, `R_μν R^να R_α^μ`, `□⁻¹` of them, begin at
   *third* order in `h` and lie outside both the first-order lemma and this lane's second-order
   enumeration. B1's counting method extends to them; the count was not run.
4. **Nothing here says whether nature is MONDian**, and nothing here tests the deposited theory.

---

## 8. What this changes in the programme's standing record

- **PAPER9 must be amended before deposit, in two places** — the abstract's clause and §"what is not
  proved" item 2 — wherever the text says second-order scalars are dismissed because step E showed them
  nearest-star dominated. Suggested replacement, carrying only what is proved:

  > Scalars beginning at second order do separate `Φ` from `Ψ` and are not covered by Lemma (ops).
  > Nor are they dismissed by step E: a nonlocal second-order scalar `□⁻¹Q` reconstructs `½|∇Φ|²` of
  > the coherent field exactly and beats the nearest star by `2.2 × 10⁶`. They are excluded instead,
  > over the quadratic-curvature class, by three independent facts: at the weight a flat rotation
  > curve requires, the entire family gives lensing efficiency `η = 3/4`; the radial-profile and
  > mass-scaling conditions together force the addition to be exactly quadratic in `h`, hence linear,
  > hence without an acceleration scale; and the smoothing length that would let it see the coherent
  > field is the local mean separation between the discrete masses, which spans `2.6 × 10⁵` across the
  > systems MOND is applied to. Cubic and higher invariants remain unenumerated.

- **The lensing lock is stronger, not weaker.** It was one exact identity at first order. It is now that
  identity plus a fixed 25% deficit and a linearity theorem at second order, over an enumerated class.
- **`□⁻¹(curvature²) = ½|∇Φ|²` should be banked as a positive result** and carried whenever a lane needs
  a *covariant, frame-free, metric-only* object that measures the coherent acceleration. It is the first
  such object this programme has exhibited. It does not solve anything on its own — the pincer sees to
  that — but the "no local scalar can carry `y`" lemma should never again be quoted as if it covered the
  nonlocal case.
- **L57's tuned length gets an independent second derivation.** L57 needed `ℓ_rms ≥ 600 kpc` fitted to
  five clusters' shear. This lane gets `ℓ_crit ≈ 38 kpc`–`180 kpc` for the same objects from pure
  graininess, with no shear data at all. Two routes, same order of magnitude, same conclusion: the length
  is a property of the source population, not a constant.
- **L31's step E should be re-labelled**, exactly as L39 re-labelled DEFW's row. Its uniform-field lemma
  is exact and untouched. Its nearest-star corollary is **local-only** and must not be quoted against
  nonlocal objects.
- **Nothing in the lead's IC-series is contradicted.**
