# A4_ppn — the canonical law at planetary accelerations, and stability at every acceleration

Lane A4 of `DS_FINAL_2026_10_21`. Script: `a4_checks.py` (13 checks). Captured output: `a4.out`.
Machine-readable numbers: `a4_results.json` (every number quoted below appears there).
Mutation: `MUTATE.md`.

Footing: canonical `a0 = 9.36e-11 m/s²`, `Λ = 1.0890e-52 m⁻²`, `B_E = 3.66e-14 m/s²`
(Earth 2σ bound on a constant radial anomaly; Sereno & Jetzer 2006 Table 1 via Eq. 9 — the
number behind the published "1279×"). Alt footing `a0 = 1.13e-10` carried where it matters.

## Claim

The framework's **canonical** law `g_N = g²/(g+a₀)` has the strong-field limit
`g = g_N + a₀ − a₀²/g_N + …`: its constant anomaly is **a₀, not a₀/2**. Against
`B_E = 3.66e-14` that is **2557.38×** — **2×** the quadrature law's published
1279× (ratio to the published factor 1.99951; exactly 2 in the algebra, `a₀` vs `a₀/2`), i.e. the canonical law is *twice as
excluded* as the variant for which the `y_t ≈ 94–129` turn-off cure was designed.
Exactly: `ν_can(y) − 1 = ½(√(1+4/y) − 1)` and `ν_quad(y) − 1 = √(1+1/y) − 1` have the
*same* tail exponent `1/y` with coefficients **1** and **1/2** (this corrects the
tasking, which said 1/√y — see §D3), so the vacuum integral
`Λc⁴/a₀² = ½∫(ν−1)d(y²) = ∫y(ν−1)dy` **diverges linearly**, canonical twice as fast
(π/2 vs π/4 per unit `y_t`), not as `y^{3/2}`. The exact closure for the canonical law is
`Λc⁴/a₀² = (π/2)y_t − ln(y_t/4) + C_can` with `C_can = 8C_quad = −0.8862943611`, and
exactly `F_can(Y) = 8 F_quad(Y/4)`. Closing to the observed Λ gives **y_t^can = 66.2999**
(vs 128.7559 for the quadrature): **the two laws cannot share one turn-off** — feeding the
canonical law the quadrature's `y_t` over-predicts Λ by **1.9707×**. One `y_t` does both
jobs for the canonical law: 66.3 is far below every planet's cap (tightest 605.96 with an
over-tight stand-in bound, 5966.86 with published bounds only; margin **9.14×** / **90.0×**),
and the worst planet sits at **0.0120** of its bound. Both laws are **linearly stable at
every acceleration**: `dg/dg_N > 0` everywhere, response tensor positive-definite, the only
singular point being `u = 0` where `dg/du ≈ ½√(a₀/u) → +∞` (identical coefficient for both
laws, positive and integrable, not an instability). The patched law is itself monotone for
`y_t > 0.06253`; the required 66.3 clears that by **1060×**.

## Derivation

### D1. Inversion and the constant term (item 1)

`g_N = g²/(g+a₀)` is a quadratic in `g`: `g² − g_N g − a₀ g_N = 0`, so

  (1)  `g = (g_N/2)(1 + √(1 + 4a₀/g_N))`,  `y ≡ g_N/a₀`,  `g = a₀(y/2)(1 + √(1+4/y))`.

Expanding (sympy, exact):

  (2)  `g = g_N + a₀ − a₀²/g_N + 2a₀³/g_N² + O(g_N⁻³)`
  (3)  `g_quad = g_N + a₀/2 − a₀²/(8g_N) + …`

so `lim (g−g_N)/a₀ = 1` (canonical) vs `1/2` (quadrature). In μ-language
`μ(x) ≡ g_N/g` with `x = g/a₀`, the canonical law is **exactly** `μ(x) = x/(1+x)`
(checked symbolically: `g·μ(g/a₀) − g²/(g+a₀) = 0`), the quadrature is
`μ(x) = (√(1+4x²)−1)/(2x)`; these are the two classical p = 1 interpolations.

### D2. The general gate (why both laws are in the same excluded class)

If `μ(x) = 1 − c/x + O(x⁻²)` then `g_N = gμ(g/a₀) = g − c a₀ + O(a₀²/g)`, hence

  (4)  `Δg_∞ ≡ lim_{g_N→∞}(g − g_N) = c·a₀`,  and  `ν − 1 = c/y + O(y⁻²)`.

Measured: `c_can = 1`, `c_quad = 1/2` (sympy limits). The ephemeris bound requires
`c ≤ B_E/a₀ = 3.910×10⁻⁴`. So **the gate is on the coefficient of the 1/x term in μ**, and
both framework members fail it by construction; only interpolations with
`μ − 1 = O(x⁻²)` (α ≥ 2) pass at any `a₀`. Ratios: `a₀/B_E = 2557.38`,
`(a₀/2)/B_E = 1278.69` (the published 1279), `a₀_alt/B_E = 3087.43` (published pair 1279/1544).

### D3. `ν−1` and its tail — correction to the tasking

  (5)  `ν_can(y) = (1+√(1+4/y))/2 = 1 + 1/y − 1/y² + 2/y³ − …`
  (6)  `ν_quad(y) = √(1+1/y) = 1 + 1/(2y) − 1/(8y²) + …`

Exact: `ν_can − 1 = ½(√(1+4/y)−1) = 2/(y(√(1+4/y)+1))`. Hence

  (7)  `lim y(ν_can−1) = 1`,  `lim y(ν_quad−1) = 1/2`,  `lim √y(ν_can−1) = 0`.

**The tail is 1/y for both laws, not 1/√y** (a 1/√y tail would need
`√y(ν−1) → const ≠ 0`; the measured slope `d ln(ν−1)/d ln y = −0.99999979` over y ∈ [10⁶,10⁸]).
The tasking's "1/√y" and its corollary "y^{3/2}" are both retracted here; the physics
conclusion is unchanged in direction and *sharper* in size: the coefficients differ by
exactly 2, which is the same factor as the a₀ vs a₀/2 anomaly.

### D4. The vacuum integral: exact integrand, divergence exponent (item 2)

Definition (inherited from Zenodo 23171085/23251231, not re-derived; in `c = 1` units this is
the prior papers' `Λ/a₀²`):

  (8)  `Λc⁴/a₀² = ½∫₀^∞ (ν−1) d(y²) = ∫₀^∞ y(ν−1) dy → ∫₀^∞ [y(ν−1)]/(1+(y/y_t)²) dy`

  (9)  canonical integrand:  `y(ν_can−1) = ½(√(y²+4y) − y) → 1` as `y→∞`
  (10) quadrature integrand: `y(ν_quad−1) = √(y²+y) − y → 1/2`

so the divergence with a hard cutoff `Y` is **linear in Y**, coefficient π/2 (canonical) and
π/4 (quadrature): measured `I_can(Y)/Y → 1.5707963`, `I_quad(Y)/Y → 0.7853982`, log-log
slopes `1.00000021` and `1.00000006`. **Exponent = 1, not 3/2.** (A `y^{-1/2}` tail would
give `∫ y·y^{-1/2}dy ∝ Y^{3/2}`; that is where the tasking's 3/2 came from.)

Exact evaluation. With `v = √(y²+4y) − y` (y: 0→∞ ⇔ v: 0→2):

  (11) `F_can(Y) ≡ ∫₀^∞ y(ν_can−1)/(1+(y/Y)²) dy = Y² ∫₀² v²(4−v)/[4Y²(2−v)² + v⁴] dv`

a rational integral, evaluated to 30 digits (cross-checked against adaptive quadrature of (9)
to 1e-18 relative). Scale identity: with `z = y/4`, `y(ν_can−1)|_y = 2·z(ν_quad−1)|_z` and
`dy = 4 dz`, hence

  (12) `F_can(Y) = 8 F_quad(Y/4)`  (verified numerically to 1e-12; `C_can/C_quad = 8.000000`).

Large-`Y` form (tan θ = y/Y, expanding `√(1+k cotθ)`, the log from the θ→0 cutoff):

  (13) `F_can(Y) = (π/2)Y − ln(Y/4) + C_can + O(1/Y)`,  `C_can = −0.8862943611`
  (14) `F_quad(Y) = (π/4)Y − (1/8)ln Y + C_quad + O(1/Y)`,  `C_quad = −0.1107867951`

`C_can` is Richardson-extrapolated from Y = 10⁶…10¹² (residual at 10⁸: −0.886294393 vs
−0.886294361); at `y_t = 66.3` the asymptotic form (13) is accurate to 4.3×10⁻⁴ relative.
**The canonical closure is (π/2)y_t − ln(y_t/4) + C_can, not (π/4)y_t.**

### D5. The turn-off `y_t` (item 3a)

With `ν_fix = 1 + (ν−1)/(1+(y/y_t)²)` (the 23171085 patch; deep limit unchanged since
`y/y_t → 0` there):

  (15) `F_can(y_t) = Λc⁴/a₀² = 100.405845`  ⇒  **`y_t^can = 66.2999`**,  `y_t^can·a₀ = 6.2057×10⁻⁹ m/s²`

Inverting (13) instead gives 66.2719 (rel. 4.23×10⁻⁴ — the closure is self-consistent).
Same procedure for the quadrature law: `y_t^quad = 128.7559` (`y_t·a₀ = 1.2052×10⁻⁸ m/s²`),
and `F_quad(129)/N_Λ = 1.00191` — i.e. **the top of the published 94–129 band reproduces the
observed Λ to 0.19% in this normalization**, which is the external validation of (8).
Consequences:

  (16) `y_t^quad/y_t^can = 1.942`   (asymptotically exactly 2, from π/2 vs π/4)
  (17) `F_can(128.7559)/N_Λ = 1.9707` → sharing the quadrature's cure **over-predicts Λ by 1.97×**
  (18) alt footing (a₀ = 1.13×10⁻¹⁰): `N_Λ = 68.8896`, `y_t^can = 46.0148`, `y_t^quad = 88.5690`

### D6. Every planet inside its bound, and the one-`y_t` test (item 3b)

Anomaly `Δg(y) = a₀·y(ν−1)/(1+(y/y_t)²)` with the exact (9); `y = GM_⊙/(r²a₀)`. Each planet
caps the turn-off at `y_t ≤ y/√(a₀/B − 1)`:

| planet | r/AU | y | Δg (m/s²) | bound (m/s²) | Δg/B | y_t cap |
|---|---|---|---|---|---|---|
| Mercury | 0.387 | 4.23e8 | 2.30e-24 | 4.6e-14 | 5.0e-11 | 9.38e6 |
| Venus | 0.723 | 1.21e8 | 2.81e-23 | 8.0e-14 | 3.5e-10 | 3.54e6 |
| Earth | 1.000 | 6.34e7 | 1.03e-22 | 8.7e-15 | 1.2e-8 | 6.11e5 |
| Mars | 1.524 | 2.73e7 | 5.52e-22 | 1.4e-15 | 4.0e-7 | 1.06e5 |
| Jupiter | 5.204 | 2.34e6 | 7.52e-20 | 5.6e-13 | 1.3e-7 | 1.81e5 |
| Saturn | 9.583 | 6.90e5 | 8.64e-19 | 7.0e-15 | 1.2e-4 | 5.97e3 |
| Uranus* | 19.19 | 1.72e5 | 1.39e-17 | 7.0e-15 | 2.0e-3 | 1.49e3 |
| Neptune* | 30.07 | 7.01e4 | 8.38e-17 | 7.0e-15 | 1.20e-2 | 605.96 |

\* no published per-planet δg bound in the source table; Saturn's is carried as a deliberately
**over-tight** stand-in (the true Uranian/Neptunian bounds are weaker, so this errs conservative),
flagged `published_bound: false` in `a4_results.json`.

Worst ratio `0.011972` (Neptune, stand-in) — all eight pass. `y_t^max = 605.96` (all planets) or
`5966.86` (published bounds only, Saturn binds). Required 66.2999 ⇒ margin **9.14×** (conservative)
or **90.0×** (published only). Logic of the test: Λ fixes `y_t` to a single value (`F` is monotone
increasing), while each planet caps it from above; compatibility is the one-sided inequality
`y_t^req ≤ y_t^max`, which holds.

### D7. Stability at every acceleration (item 4)

`g = ν(u)u`, `u = g_N`. Exact response functions:

  (19) canonical:  `dg/du = ν + uν' = (1+s)²/(4s)`, `s = √(1+4a₀/u)`;  `= g²/[u(2g−u)]`
  (20) quadrature: `dg/du = (1 + 1/(2y))/√(1+1/y)`  (`y = u/a₀`)

Values across `u ∈ (0,a₀]`: at `u/a₀ = 10⁻⁶, 10⁻³, 0.1, 0.5, 1`: canonical
500.50, 16.317, 2.1398, 1.3333, 1.17082; quadrature 500.00, 15.835, 1.8091, 1.1547, 1.06066.
Both are positive and finite on `(0,∞)`. The isotropic response tensor
`∂g_i/∂g_N,j = ν δ_ij + ν' u_i u_j/u` has eigenvalues `ν` (×2) and `ν + uν' = dg/du`; both are
positive for every `u > 0` in both laws (for the canonical law `(1+s)²/(4s) > 0` for all `s > 1`,
symbolically). **There is no acceleration at which the linear response fails.** The single
singular point is `u = 0`, where `dg/du ≈ ½√(a₀/u) → +∞` for *both* laws (measured
`y(dg/du)² → 0.2500005` and `0.25000000`): positive, integrable, the usual deep-MOND square-root
cusp — it makes linear perturbation theory *at exactly* `u = 0` invalid, not the theory unstable.
Deep-limit **condition**: stability ⇔ `μ(x) + x μ'(x) > 0 ∀x ≥ 0` (equivalently `dg_N/dg > 0`).
Canonical: `x(2+x)/(1+x)² > 0`; quadrature: `2x/√(1+4x²) > 0`; both hold with equality only at
`x = 0` (where `dg/du = ∞`). The **patched** law must also be monotone: `min_y dg/dy > 0` requires
`y_t > y_t^crit = 0.06253` (`y_t^crit·a₀ = 5.85×10⁻¹² m/s²`); at `y_t = 66.30` the minimum response
is 0.99086, so the cure is gradient-stable by **1060×**.

## Status

**`CONDITIONAL(turn-off premise)`** for every "passes the Solar System" statement; the *failures*
are unconditional.

- Item 1 — **DERIVED** (exact series, sympy) **+ NO-GO**: the bare canonical law, held at all
  accelerations, produces a constant anomaly of `a₀`, i.e. `2557.38 B_E`. This is a two-sided
  embarrassment: the cure on record was calibrated on the quadrature member (1279×) and the
  canonical member is exactly twice as bad. No new fitted constant enters this statement.
- Item 2 — **DERIVED**: tail coefficient 1 (vs 1/2), linear divergence (exponent 1), exact
  integrand (11), identity (12), constants (13)–(14).
- Item 3a — **NUMERICAL**: `y_t^can = 66.2999` (transcendental root of the exact rational
  integral; asymptotic closure reproduces it to 4.2×10⁻⁴).
- Item 3b — **NUMERICAL**: all eight planets pass; one `y_t` does both jobs with margin 9.14×.
- Item 4 — **DERIVED**: response positive-definite at every acceleration, both laws; patched-law
  monotonicity threshold `y_t^crit = 0.06253`.

## Checks

`a4_checks.py` prints 13 lines, all PASS (`a4.out`), exit 0; `--mutate` breaks 4 and exits 1.

- K1 exact series: `g − g_N → a₀` (canonical), `a₀/2` (quadrature).
- K2 `a₀/B_E = 2557.377` = 2×1279 to 0.024% (`a0_alt` → 3087.43).
- K3 exact `ν−1` and limits 1 / 1/2 / 0 (tail is 1/y, `√y(ν−1) → 0`).
- K4 numerical tail exponent −0.9999998.
- K5 exact rational integrand vs adaptive quadrature (1e-18) and divergence exponent 1.0000002.
- K6 `C_can` to 1e-6 of the Richardson value; exact identity ratio 8.0; asymptotic closure 4.3e-4.
- K7 closure (13) inverts to 66.2719 vs exact root 66.2999.
- K8 `F_quad(129)/N_Λ = 1.00191` (normalization validated); transplant ratio 1.9707.
- K9 worst planet ratio 0.011972 < 1.
- K10 `y_t` margin 9.14 (all planets) with `y_t^max = 605.96`, `5966.86` (published only).
- K11 response minimum over `u ∈ (0,a₀]` = 1.06066; deep limit 0.2500 for both.
- K12 patched-law critical `y_t = 0.06253`; required/critical = 1060.
- K13 the general gate: `c_can = 1`, `c_quad = 1/2`, allowed `c ≤ 3.910×10⁻⁴`, and
  `g·μ(g/a₀) − g²/(g+a₀) = 0` (the identification μ = x/(1+x)).

## What this does not do

- **It does not derive the turn-off.** `ν_fix` is a posit inherited from Zenodo 23171085; `y_t`
  is a fitted number and, as shown here, a *law-dependent* one (66.30 vs 128.76). Nothing in this
  lane explains why a turn-off should exist at `~6×10⁻⁹ m/s²`.
- **No external-field (EFE) suppression is computed.** 2557× is the isolated-sphere monopole. The
  repo's earlier EFE estimate for the quadrature law is an O(10²) suppression; applied here it
  would leave the canonical law over the bound by more than an order of magnitude, but that
  number is not recomputed in this lane.
- **No Cassini Q₂.** The quadrupole is a different functional of `ν`; the patched canonical law's
  Q₂ is a separate calculation (and the sharper gate in Park+2026).
- **No galactic/RAR fit.** The turn-off costs 2.22% of the anomaly at `y = 10`
  (`1/(1+(10/y_t)²) = 0.97776`; quadrature 0.99400) — 3.71× more intrusive than the quadrature's
  cure. Whether SPARC tolerates that is a different lane's gate, and it is the most likely place
  for a real conflict: raising `y_t` to protect galaxies would over-predict Λ.
- **The planetary bounds are precession-σ conversions**, which Fienga & Minazzoli 2024 explicitly
  discourage reading as theory bounds; the self-consistent probe is the simultaneous Q₂ fit. The
  conclusion is insensitive to this: the worst planet sits at 1.2% of its bound, and Uranus/Neptune
  carry a stand-in bound.
- **The `8×` identity is a scaling identity, not a derivation of the normalization** (8); the
  normalization itself is an input from the prior papers, cross-checked only by `F_quad(129)/N_Λ`.

## Next

1. **EFE for the canonical law.** Repeat the external-field estimate with `c = 1` (not 1/2) and
   the `y_t = 66.30` patch; the question is whether the Galaxy's field buys the factor 2557.
2. **Cassini Q₂ at `y_t = 66.30`.** The quadrupole of the patched canonical law is uncomputed and
   is the sharper gate; the patch suppresses it by the same `1/(1+(y/y_t)²)` but the integral
   differs.
3. **Galactic zero-point.** Fit `y_t` against the SPARC RAR with the 2.22%-at-`y=10` suppression
   included; if the RAR prefers `y_t > 100`, the canonical law's Λ closure (which wants 66.30)
   and the RAR pull apart and the member is in trouble.
4. **Member selection.** The two laws are now distinguishable by a number: `a₀` with `y_t = 66.30`
   (canonical) vs `a₀/2` with `y_t = 128.76` (quadrature). A shared cure is excluded at 1.97× in Λ,
   so "the framework" must pick one before any Solar-System or cosmological number is quoted.
