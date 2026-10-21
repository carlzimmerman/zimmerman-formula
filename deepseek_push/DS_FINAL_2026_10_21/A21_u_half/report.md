# A21 — is the sourcing fraction u exactly 1/2, the same number as κ?

## Claim

**No — on four counts.** Each is earned below.

1. **The measurement allows 1/2 and does not establish it.** The record's three amplitudes give the
   sourcing fraction with no model at all — `u = (A_newton − A_law)/(A_law(A_newton − 1))`, the law's
   phantom share of the *observed* excess over baryons. In the MID band
   **u = 0.4716 ± 0.0362**, i.e. **0.78σ** from 1/2 (0.41σ if a ±0.06 band→3D systematic is folded in).
   `u = 1` is excluded at 14.6σ. The MW anchor gives **0.4668 ± 0.0977** (0.34σ, theory band, not
   data); the joint **0.4710 ± 0.0340** (0.85σ, χ² = 0.73 for 2 dof, p = 0.69). 1/2 survives; nothing selects it.

2. **But u is not one number: the same inversion in the OUTER band gives 0.9865 ± 0.0984.**
   `A_OUT` is `1.0118 ± 0.0869` (law) and `7.262 ± 0.62` (baryons only), so the phantom accounts for
   essentially *all* of the OUTER excess and half of the MID excess. 1/2 is **4.9σ away in OUTER**, and
   the two bands differ by `0.515` — **≥3.8σ for any band correlation**. "The sourcing fraction"
   therefore depends on the annulus (A18's K18 shape mismatch in `u` units).

3. **The "≈1/2 at both anchors" is not a property of the law.** Between the anchors the law's own ratio
   spans **9.566×** and the CFG416 retained-fraction table spans **9.0×**; their quotient is **1.063**,
   which is why both land near 0.47. With one denominator (`f_ret = 1`, cold = the cosmic share of the
   system's own baryons) the same two anchors give **4.668** (MW) and **0.488** (cluster), a factor
   **9.57** apart. Worse, at the cluster `f_ret ≤ 1` caps `u ≤ 0.4880`, so **u = 1/2 there requires a
   retained fraction of 1.0245 — more baryons than the cosmic share.**

4. **It is not derivable, and it is not κ.** The law fixes one function of radius (the active density
   `ρ+3p`); `u` needs the ratio `p/ρ`. Each route converts "u = 1/2" into a *new premise*: (i) gives
   `u = 1+3⟨w⟩` exactly, so 1/2 ⇔ **w = −1/6** (`c_s² = −1/6 < 0` for a barotropic fluid); (ii) gives
   `u = 3f_s`, so 1/2 ⇔ a stiff fraction **f_s = 1/6**; (iii) gives **neither** — `μ(x=1) = φ = 1.6180`,
   `1−μ = −0.6180` — and the law's only exact 1/2 is the *local mass fraction* `M_ph/(M_b+M_ph) = 1/2`
   at `x = 1/2`, which is 0.963 (MW) and 0.790 (cluster) at the virial radii. And `u` is a function:
   **0.3696–0.7164** over `1e10–1e14 M☉` at `c = 7`, crossing 1/2 three times. κ is a constant of the
   vacuum-tied scale; something varying by 1.94× over the observed mass range cannot *be* κ.

## Derivation

Units `c = 1`; `G = 6.67430e-11`; `a0 = 9.36e-11 m/s²` (canonical, never pooled); `H0 = 67.4 km/s/Mpc`;
`ρ_c = 3H0²/8πG`; `Δ_v = 200`; `M_☉ = 1.98847e30 kg`; Hernquist baryons; spherical symmetry.
`f_b = ω_b/ω_m = 0.02237/0.14237 = 0.157126` [EXT CFG515], `R_cosmic = (1−f_b)/f_b = 5.364327` [EXT],
`κ = 1/2` (BRIEF §1). `f_ret(M_ta)` is the CFG416 three-segment table [EXT]: 0.10 below `1e12.5`,
+0.45/decade to `1e13.5`, +0.30/decade capped at 0.90; `M_ta = M_b h/(f_ret f_b16)`, `h = 0.674`, `f_b16 = 0.157`.

**1. The law.** `g_N = g²/(g+a0)` ⇒ `g = (g_N/2)(1+√(1+4a0/g_N))` (K1, exact), with `y ≡ g_N/a0 = GM_b(<r)/(a0r²)`:

    M_ph(<r)/M_b(<r) = g/g_N − 1 = ½[√(1+4/y) − 1] ≡ F(y).                        (1)

K2: exact. The response `μ ≡ g/a0` for `x ≡ g_N/a0 = μ²/(1+μ)` is `μ = (x+√(x²+4x))/2`, so **μ(1) = φ** (K3).

**2. Three different u's — the lane's premise conflates them.** With `R_tot ≡ μ_v(1+F(y_v))−1` the
phantom per *system* baryon and `N ≡ R_cosmic/f_ret` the catchment cold energy per system baryon:

    u_catch = R_tot/N = R_tot f_ret/R_cosmic        (A18's u: 0.4668 MW, 0.4392 cluster)   (2)
    u_sys   = R_tot/R_cosmic                        (f_ret = 1: 4.668 MW, 0.488 cluster)  (3)
    u_data  = M_ph/M_c,measured = R_tot/R_req = 1/λ_req                                   (4)

(2) is what the lane quotes; (3) is what its prose defines ("M_c = 5.3643 M_b"); they differ by `f_ret`.
Only (4) is a measurement, and only at the cluster.

**3. u from the record's amplitudes, with no model.** CFG687's `A` is `Σw·ΔΣ_obs/Σw·ΔΣ_model` on the
total signal, so with `B` the baryonic and `P` the phantom band signal, `A_law = D/(B+P)`,
`A_newton = D/B`, and

    u = P/(D−B) = (A_newton − A_law)/(A_law(A_newton − 1)) = 1/λ_req,
    λ_req ≡ A_l(A_n−1)/(A_n−A_l).                                                             (5)

K4: the two forms agree to 1e-12. With `A_law = 1.910194 ± 0.118637`, `A_newton = 10.173704 ± 0.65`
(CFG687 MID, 318 eRASS1 × KiDS clusters, `canonical|b0.67|rc0.15|f0.20`):

    f_band = 1 − A_l/A_n = 0.8122,   λ_req = 2.1206 ± 0.1630,   u_MID = 0.47157 ± 0.03625.     (6)

`dln u/dA_l = −A_n/[A_l(A_n−A_l)] = −0.6445`, so `σ_u/u = 0.0769` — the 7.7% is the amplitude error, not
the model. (5) contains no `f_ret`, no `R_tot`, no `a0`. K5: 1/2 is 0.78σ away; `u = 1` is 14.6σ away.

**4. The same inversion in OUTER, and the band dependence (K5b).** With `A_OUT,law = 1.011801 ±
0.086872`, `A_OUT,newton = 7.262 ± 0.62`:

    u_OUT = 0.9865 ± 0.0984,   λ_OUT = 1.0137,   1/2 is 4.9σ away.                         (7)

The two bands differ by `0.5149`, which is 4.9σ in quadrature and **≥3.8σ for any band correlation**
(`σ_diff` runs from `|σ₁−σ₂| = 0.062` — 8.3σ — at ρ = +1, to `σ₁+σ₂ = 0.135` — 3.8σ — at ρ = −1).
So `u` is band-dependent: the phantom over-explains the OUTER excess and under-explains the MID one.
The data/law residual ratio is `1.9102/1.0118 = 1.888` MID/OUTER, i.e. the data's excess is more
centrally concentrated than the law's phantom by that factor.

**5. The MW anchor is a prediction, not a measurement.** `u_MW = 25.0429/53.643 = 0.46684` (K6) with a
theory band from ±25% on `M_b`, ±25% on `a`, ±20% on the CFG416 value: `dln u/dln M_b = −0.246`,
`dln u/dln a = −0.025`, giving ±0.0977 (inputs only: ±0.0289). There is no data-driven `u` for the MW —
the cold mass is never measured — so this anchor tests the table, not nature. Joint with the cluster
(K7): `û = 0.4710 ± 0.0340`, 0.85σ from 1/2; the two anchors agree with *each other* at 0.05σ.

**6. Why both anchors land near 1/2 (K8, K9).** `u_MW/u_cl = (R_tot,MW/R_tot,cl)(f_ret,MW/f_ret,cl) =
9.566 × 0.1111 = 1.063`. The cancellation is a 6% coincidence of the law's span with the table's span.
Because `f_ret ≤ 1` by definition (the retained fraction of the cosmic baryon share of the turnaround
mass),

    u ≤ R_tot/R_cosmic = 0.4880  at the cluster anchor,                                          (8)
    u = 1/2 there requires f_ret = R_cosmic/(2R_tot) = 1.0245 > 1.                             (9)

The MW needs `f_ret = 0.1071` (admissible, 7% above the table floor), so the anchors are not symmetric:
**the cluster cannot reach 1/2 under its own bookkeeping**, by 2.4%.

**7. Route (i), virial split — exact, and underdetermined.** For `T^{μν} = ρu^μu^ν + p h^{μν}` in the
static frame, `T^0_0 = −ρ`, `T^i_i = 3p`, `T = −ρ+3p`, hence `T_00 − ½g_00T = (ρ+3p)/2` and

    ∇²Φ = 4πG(ρ+3p),   M_g(<r) = ∫(ρ+3p)dV = M_c + 3∫p dV,   u = M_g/M_c = 1 + 3⟨w⟩,            (10)

with `⟨w⟩ ≡ ∫p dV/∫ρ dV` the **volume-weighted** mean (K10, K11 exact in sympy). For constant `w` this
is profile-independent; for `w(r) = w_0(r/R)^n` with `ρ ∝ r^{-2}` it is `w_0/(n+1)`, half the
constant-`w` value at `n = 1` (K11b). Hence

    u = 1/2  ⇔  ⟨w⟩ = −1/6 = −0.166667,                                                       (11)

and for a barotropic fluid `c_s² = dp/dρ = w = −1/6 < 0`: unstable (K12). The obstruction is K13: two
media with the *same* `ρ+3p` — `(ρ,p) = (2ρ_ph, −ρ_ph/3)` and `(ρ_ph, 0)` — produce the same field and
give `u = 1/2` and `u = 1`. **The law fixes the sum; u needs the split.** One equation, two functions.

**8. Route (ii), two-fluid — a number, not a derivation.** With energy fractions `f_s` (stiff, w=1) and
`1−f_s` (dust, w=0), `⟨w⟩ = f_s`, so `u = 3f_s` (phantom = pressure part) or `u = 1+3f_s` (phantom =
whole gravity). `u = 1/2` needs `f_s = 1/6` (or `−1/6`, unphysical) — K14. The "same density" reading
(`f_s = 1/2`) gives **1.50 or 2.50**, never 1/2. `1/6 = 0.166667` matches nothing in the framework: the
nearest number is `f_b = 0.157126`, 5.7% away (K15). The one numerical coincidence is `3f_b = 0.471377`,
`−0.01σ` from `u_MID`; it corresponds to `f_s = f_b` (stiff fraction = cosmic baryon fraction), has no
mechanism, and would freeze `u` at 0.4714 at every mass, contradicting the theory's own `u(M)` running.

**9. Route (iii), saturation — neither.** `μ(x=1) = φ = 1.618034 ≠ 1/2`; `1−μ(x=1) = −0.618034 ≠ 1/2`
(K16). The law's exact 1/2 is elsewhere: `F(y) = 1` at `y = 1/2`, so `M_ph/(M_b+M_ph) = 1/2` at
`x = 1/2`, `r = √2 r_M` — a *local mass fraction* at one radius, equal to 0.963 (MW) and 0.790
(cluster) at `r_v`. The n=2 "half capacity" is a high-acceleration statement: `F₁/F₂ → 2` as `y→∞`,
`→ 1` as `y→0` (the deep limit where the two laws coincide), 1.492 at `y = 1`, and 1.019 / 1.123 at the
anchors' `y_v` (K17). None of these is `u`.

**10. The scaling (Task 3).** From (2), with `μ = (c/(1+c))²`, `y_v = μ M_v^{1/3}(4πΔρ_c/3)^{2/3}G/a0`,

    u(M_v, c) = (f_ret(M_b)/R_cosmic)·{½[√(1+4/y_v) − 1]·(1+μ) − 1},
    u ≃ (f_ret/R_cosmic)[ (y_v)^{-1/2} − ½ ]  for y_v ≪ 1,   ∂ln u/∂ln M_v → +1/6.            (12)

K18: `u ∈ [0.3696, 0.7164]` over `1e10–1e14 M☉` at `c = 7` (1.94×), with **three** crossings of 1/2
(`2.21e10`, `1.81e11`, `8.81e13 M☉`) produced by the table's knees. K19: imposing `u = 1/2` is
equivalent to a *retention law*

    f_ret(M) = R_cosmic/(2R_tot) = 0.1071 (MW), 0.2568 (1e13), 1.0245 (cluster),                   (13)

which exceeds `f_ret = 1` above `M_v = 4.91e14 M☉` (`c = 7`; 2.53e14 at `c = 4`, 1.30e15 at `c = 100`).

**11. What u = 1/2 would predict, if postulated.** (a) `M_c(<r_v) = 2M_ph(<r_v)` exactly, i.e.
`R_c = 2R_tot(M,c)` — 50.09 (MW), 20.89 (1e13, c=7), 5.236 (cluster): a cold-to-baryon ratio that *falls*
with mass, against the cosmic share's constant 5.364. (b) At the cluster `λ = 2` exactly, so
`A_MID = 1+(2−1)f_band = 1.8122` versus 1.8521 (cosmic) and 1.9102 measured: **the two hypotheses are
0.34σ apart at the cluster** — it cannot decide them. (c) At `1e13` they are 1.334× apart in cold mass
(`A_MID` 1.8122 vs 1.4051), so groups decide it (K20). (d) Exactly half the cold energy (`1−u = 1/2`)
must never be sourced and must fall natively — the fixed "unrelaxed fraction".

## Status

- **Task 1 — NUMERICAL.** MID `u = 0.47157 ± 0.03625` (0.78σ from 1/2; 0.41σ with the band-mapping
  systematic); OUTER `0.9865 ± 0.0984` (4.9σ from 1/2); the bands differ at ≥3.8σ. MW
  `0.46684 ± 0.09774` (0.34σ, theory band, not data); joint MID+MW `0.47099 ± 0.03398` (0.85σ).
  **1/2 is consistent with the MID band at <1σ, excluded in OUTER at 4.9σ, and nowhere established**;
  `u = 1` is out at 14.6σ in MID.
- **Task 2 — NO-GO(obstruction).** `u = 1+3⟨w⟩` and the law supplies only `ρ+3p`: `u` is not a
  functional of the law. (i) needs `w = −1/6` (`c_s² < 0`), (ii) needs `f_s = 1/6`, (iii) is neither
  (`μ(1) = φ`). No route yields 1/2 as a consequence.
- **Task 3 — NO-GO + the scaling, and a structural exclusion.** `u(M,c)` is (12); `u = 1/2` is a
  *retention law* (13) that exceeds `f_ret = 1` above `4.91e14 M☉`. The exact missing premise is
  **(P1) the cold sector's active mass is half its energy, `⟨w⟩ = −1/6`**, and, for the catchment
  version, **(P2) the cold mass inside `r_v` is the whole catchment (`f_ret = 1`)**. Neither is in the
  theory; P2 is contradicted by the record's own table at the cluster.
- **Task 4 — DECIDABLE.** See §Falsifier.

## Checks

`a21_checks.py` — 25 checks, deterministic, stdlib + numpy/scipy/sympy, 0.4 s, no network, exit 0 iff
all pass; three mutations each break ≥1 check and exit 1 (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | law root exact (sympy) | 0 | <1e-30 |
| K2 | `F(y)` exact (sympy) | 0 | <1e-25 |
| K3 | `μ(1) = φ`, `F(1/2) = 1` | 1.618034, 1.000000 | ±1e-12 |
| K4 | `u = 1/λ = (A_n−A_l)/(A_l(A_n−1))` | 0.47157 ± 0.03625 | 0.47157 ± 0.001 |
| K5 | 1/2 vs the MID measurement | 0.78σ | 0 < Z < 1.5 |
| K5b | OUTER inversion and the MID–OUTER gap | 0.9865 ± 0.0984; ≥3.8σ | Z<−4; gap>3.4σ any ρ |
| K6 | MW anchor and its theory band | 0.46684 ± 0.09774 | ±0.002 |
| K7 | joint, and the anchors against each other | 0.85σ; 0.05σ | Z<1, p>0.1 |
| K8 | the 9.566 × 0.1111 cancellation | ratio 1.063 | ±0.005 |
| K9 | cluster ceiling `f_ret ≤ 1` | u ≤ 0.4880; `f_ret` = 1.0245 | > 1 |
| K10 | `T_00 − ½g_00T = (ρ+3p)/2` (sympy) | 0 | <1e-25 |
| K11 | `u = 1+3⟨w⟩`; profile dependence `w_0/(n+1)` | 0 / 0 | <1e-25 |
| K12 | `u=1/2 ⇔ w=−1/6`, `c_s² = −1/6` | −0.166667 | exact, < 0 |
| K13 | same field, `u = 0.5` vs `1.0` | identical `ρ+3p` | — |
| K14 | two-fluid: `f_s = 1/6`; equal densities 1.5 / 2.5 | 0.166667 | exact |
| K15 | no framework number is 1/6; `3f_b` is the near-miss | 5.7% | >0.008 |
| K16 | `μ(1)` and `1−μ(1)` are not `u` | 1.6180 / −0.6180 | > 0.5 |
| K17 | n=2 "half capacity" is `y→∞`; deep limit → 1 | 2.0 / 1.0 / 1.019 | ±0.02 |
| K18 | `u(M,c)` is a function: window, three crossings | 0.3696–0.7164 | ratio > 1.8 |
| K19 | `u=1/2` is a retention law; `f_ret > 1` above `4.91e14` | 1.0245 | > 1 |
| K20 | group-scale split 1.334× / 0.407 in `A_MID` | 1.3345 | ±0.01 |
| K21 | 3σ needs `σ_u ≤ 0.00948`, `σ_A ≤ 0.0312`, N ≥ 4602 | 3.82× | 4000 < N < 5500 |
| K21b | group route needs `σ_A ≤ 0.136` | 0.1357 | 0.10–0.20 |
| K22 | `u` is not a constant, so not κ | 6.3% anchor spread | > 1% |
| K23 | numerology audit: 2 of 12 candidates within 1σ | reported | — |

## What this does not do

1. `u_data` is a **ΔΣ-weighted band fraction**, not a 3D mass ratio; the band→3D mapping is not modelled
   (A18 §What-this-does-not-do 4: `f_band = 0.812` is a weighted share, the 3D value at the MID centre is
   0.65). Folding a ±0.06 systematic moves the 1/2 distance from 0.78σ to 0.41σ. The MID–OUTER gap of §4
   is the honest statement of how much this matters: 0.47 vs 0.99.
2. The MW anchor is a **prediction with a ±20% table band**, not a measurement; it tests the CFG416
   table, not nature. It also sits 0.09 dex below the table's knee at `1e12.5`, so a +25% baryon mass
   moves it across the knee (`dlnu/dlnM = −0.246` is the two-sided average of a kinked response).
3. `f_ret` is inherited and fitted; `u_catch` inherits every error in it. Nothing here derives it.
   `w = −1/6` is excluded **for a barotropic perfect fluid** (`c_s² < 0`); a non-barotropic medium
   (network, solid) is not excluded by K12, but the isotropic-solid route is already closed (BRIEF §2,
   round 2: `λ = −μ`, negative bulk modulus).
4. The MID and OUTER amplitudes come from the same 318 clusters and the same shear catalogue, so their
   errors are correlated. That is why §4 quotes the correlation-free bound (≥3.8σ): a positive
   correlation makes the *difference* more significant, not less.
5. Spherical symmetry, Hernquist baryons, no EFE, no disc geometry throughout. The group-scale `A_MID`
   numbers (K20) reuse the cluster's `f_band` and are `CONDITIONAL(shape-preserving, same band share)`.
6. I do not attempt a new κ derivation (BRIEF §2 lists four failed ones); §K22 only refuses the
   *identity* `u = κ`, on the grounds of `u`'s measured mass dependence.

## Falsifier

`u` is measured by a band amplitude through (5). Excluding 1/2 at 3σ needs `σ_u ≤ 0.00948` — a **3.82×**
improvement on 0.03625, i.e. `σ(A_MID) ≤ 0.0312` (now 0.1186), i.e. **≥ 4602 clusters** at the
318-cluster per-object noise (K21).

> **Dataset.** eRASS1 (Bulbul+2024, ~12 000 clusters) over its **full sky** — not the 920 KiDS-box
> candidates that yield the present 318 — crossed with **LSST Y1 / UNIONS** shear, same CFG686/687
> estimator, MID 0.5–1.2 Mpc, jackknife over ≥30 patches: ~4 100 clusters and `σ_u ≈ 0.010`.

But the decisive measurement is not a deeper cluster stack — it is a **different mass**. At
`M_v = 1e13` the hypotheses differ by 33% in cold mass (`A_MID` 1.8122 vs 1.4051), so `σ_A ≤ 0.136`
separates them at 3σ (K21b): a few hundred group-mass stacks (`M_500 ≈ 2e13`) from eRASS1 × DESI Y3 or
ACT DR6 × DES Y3, annuli scaled to each group's `r_500`. The cluster anchor is degenerate between
`u = 1/2` and the cosmic share at 0.34σ; only the mass *scaling* breaks it.

## Next

1. Compute the band→3D mapping for the CFG687 stack (`f_band → f_3D`): the largest single systematic on
   `u_data`, and a one-afternoon job on the existing per-cluster `.npz`. Until it exists the MID/OUTER
   split (0.47 vs 0.99) is the honest error bar and `u` should be quoted per band.
2. The premise to attack is **(P1)**: is there a stable medium with `⟨w⟩ = −1/6` and no anisotropic
   stress? A 1:1 energy mix of dust (`w=0`) and a `w = −1/3` string network gives exactly `−1/6` — the
   only structural reading I found, and a new postulate, not a derivation.
3. Measure `u` as a *function*, not a number: the same inversion in 4–5 mass bins, testing the predicted
   `M_v^{1/6}` run of (12) rather than a constant.
