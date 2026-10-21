# A18 — the two 5.364s: the cosmic ratio and the law's own phantom ratio

## Claim

The two 5.364s are the same number carrying two different **denominators**, and once the
denominators are made explicit they are not the same statement. `R_cosmic = (1−f_b)/f_b =
5.364327` is a **budget** identity: cold energy per unit of *catchment* baryon mass, fixed once
and for all by the CMB. `F(y) = ½[√(1+4/y)−1]` is a **force** identity: phantom mass per unit of
*enclosed* baryon mass at radius `r`, fixed pointwise by the law. They coincide at exactly one
point of the `(M_v, c)` plane — `y* = 0.029291`, `r = 5.843 r_M`, **`M_v = 1.7584e14 M☉`,
independent of concentration** — and nowhere else; below it the law's ratio to enclosed baryons
exceeds 5.364, above it falls short, by a factor 647 at `1e8 M☉` and 0.56 at `1e15 M☉`. Restoring
the correct denominator (the catchment holds `1/f_ret` times the system's baryons, so the supply
is `N = 5.364/f_ret`, not 5.364) turns the comparison into the **sourcing fraction**
`u ≡ R_tot/N`, which is **0.467** for an MW-like system and **0.439** for a cluster, and stays in
**0.39–0.72** over `1e10–1e14 M☉`: the law's phantom is 40–72% of the acquired cold energy, never
all of it. At cluster masses the record's own three lensing amplitudes fix the missing factor
 algebraically: the required cold-to-baryon ratio is **5.55 ± 0.43**, i.e. **0.44σ from 5.364
and 6.9σ from 2.62**. So the cluster data have already selected "the cold energy is the cosmic
share" over "the cold energy is the law's phantom" at **Δχ² = 58.7**, and what must be new is not
a normalization but a *sourcing rule*: the law governs a fraction `u ≈ ½` of the cold sector, and
the remainder falls natively and is more concentrated.

## Derivation

Units `c = 1`; `G = 6.67430e-11`; `a0 = 9.36e-11 m/s²` (canonical footing, never pooled);
`H0 = 67.4 km/s/Mpc`; `ρ_c = 3H0²/8πG`; `Δ_v = 200`; Hernquist baryons; spherical symmetry.

**1. The law and its inverse.** `g_N = g²/(g+a0)` is quadratic; the physical root is

    g = (g_N/2)(1 + √(1 + 4a0/g_N)).                                                (1)

K1: (1) is an exact symbolic root (residual 0).

**2. Identity I — the law's identity (local, differential).** With `M_ph(<r) ≡ r²(g−g_N)/G` and
`M_b(<r) ≡ r²g_N/G` — each the Gauss-law mass of its own field — dividing gives, with
`y ≡ g_N/a0 = GM_b(<r)/(a0r²)`,

    M_tot(<r) = M_b(<r)[1 + F(y(r))],      F(y) = ½[√(1+4/y) − 1],
    M_ph(<r) = F(y(r)) M_b(<r).                                                      (2)

(2) is exact at *every* r for any spherical baryon profile; it contains no normalization freedom
and no mass scale except through `y(r)`. K2: exact symbolically.

**3. Identity II — the cosmic budget (global, integral).** With `f_b = ω_b/ω_m = 0.02237/0.14237
= 0.157126` (CFG515 `cfg515_lib.py:15`),

    M_c = R_cosmic · M_b,ta,     R_cosmic = (1−f_b)/f_b = 5.364327,
    M_b,ta ≡ f_b M_ta.                                                               (3)

(3) fixes a *total mass* and has no r-dependence. K3: the exact inverse of `F` is
`y = 4/[(2R+1)²−1]`, so `F(y*) = R_cosmic` at `y* = 0.029290868`, i.e. `r = 5.842973 r_M` (K4;
A11 K4b).

**4. The split, and what "not yet sourced" means.**

    M_tot(<r) = M_b(<r) + M_ph(<r) + M_x(<r),
    M_x(<r_v) = M_c − M_ph(<r_v)   (for a catchment that covers the virial ball).      (4)

where `M_x` is supplied-but-not-yet-sourced cold energy: it gravitates, but it is not the phantom
and the law does not describe it. (4) is the *only* place the two identities meet, and they meet
through one scalar.

**5. Where each 5.364 enters.**

- `R_cosmic` enters **only** in (3), as a total: `M_c = 5.364 M_b,ta`. It never appears in (2).
- `F(y)` enters **only** in (2), as a profile: `M_ph(<r) = F(y)M_b(<r)`. It never appears in (3).
- For the two to be the *same* statement one needs `M_x = 0` at `r_v` **and** the same denominator:

      F(y_v) = R_cosmic · (M_b,ta / M_b(<r_v)) = N,     N ≡ R_cosmic/f_ret.           (5)

  With `M_b,ta = M_b(<r_v)` (a catchment that is exactly the virial ball) this reduces to
  `F(y_v) = 5.364327` — the "one point" of §3. With the record's actual catchment it is
  `F(y_v) = N`, which is a *different* equation. Both are one equation in one unknown; neither is
  an identity.

**6. The grid (Task 2).** For each `(M_v, c)`, `r_v` is fixed by `M_v` alone
(`r_v³ = 3M_v/4πΔ_vρ_c`), `μ ≡ M_b(<r_v)/M_b,tot = (c/(1+c))²`, and the enclosed baryon mass solves
`M_b(<r_v)[1+F(y_v)] = M_v`. 90 points: `M_v = 10^8…10^15 M☉` (15 values) × `c = 4, 7, 10, 20, 40,
100`. Because the virial condition fixes `M_b(<r_v) = M_v/(1+F)`, `y_v` is **independent of c** —
hence

    R_enc ≡ M_ph(<r_v)/M_b(<r_v) = 5.364327  at  M_v = 1.7584e14 M☉  for every c,   (6)

to a spread of 0 (K7). The ratio to the *system's total* baryons,
`R_tot = μ(1+F)−1`, reaches 5.364 at a c-dependent mass below that: 3.79e13 (c=4), 6.94e13 (c=7),
1.64e14 (c=100) — i.e. `R_tot` is 5.364 only in the `μ→1` limit at `1.7584e14` (K8). Sign
structure, both quantities, monotone in `M_v` (K9):

| `log10 M_v` | c=4 `R_enc`/`R_tot` | c=7 | c=100 |
|---|---|---|---|
| 8 | 647.5 / 414.0 | 647.5 / 495.5 | 647.5 / 634.7 |
| 11 | 64.75 / 41.08 | 64.75 / 49.34 | 64.75 / 63.45 |
| 14 | 6.475 / 3.784 | 6.475 / 4.723 | 6.475 / 6.327 |
| 15 | 3.005 / 1.563 | 3.005 / 2.067 | 3.005 / 2.926 |

Below `1.7584e14` the law **over**-supplies relative to the cosmic ratio (`R > 5.364`); above it,
**under**-supplies. The agreement is therefore a crossing of a function that spans 647→3.0 over the
range, not a reconciliation.

**7. The sourcing fraction (Task 1, completed).** `N = R_cosmic/f_ret` with `f_ret` the CFG416
table evaluated at `M_ta`, solved implicitly from `M_ta = M_b h/(f_ret f_b16)`, `h = 0.674`,
`f_b16 = 0.157` (reproducing A11's `N = 53.643, 44.125, 14.917, 8.296, 5.960`). Then

    u ≡ R_tot/N,     u(MW) = 25.043/53.643 = 0.4668,   u(cluster) = 2.6179/5.960 = 0.4392.   (7)

Over `M_b = 1e10…1e14` at `c = 7`, `u` runs 0.394–0.716 (K11) — the law carries between two-fifths
and three-quarters of the supply, never all of it. `u = 1` is reached only at
`M_b = 1.425e9 M☉` (`M_v = 7.79e10`); below that the law's phantom at `r_v` would need more cold
energy than the entire catchment holds, so the profile must truncate inside `r_v` (K12).

**8. The cluster shortfall (Task 3).** At `M_b = 1.4e14`, `a = 250 kpc`: `r_v = 1.6863 Mpc`,
`M_v = 5.0651e14`, `F(y_v) = 3.7702`, `R_tot = 2.6179`, `y_v = 0.05560` (K5, reproducing A11's
2.62). The cosmic share gives `λ_cosmic = 5.364327/2.6179 = 2.0491`, i.e. the law is short by
**0.3116 dex** (K13).

The record's own amplitudes give the same number independently, with no model. `A` in CFG686/687
is `Σw·ΔΣ_obs / Σw·ΔΣ_model` applied to the **total** signal, so for the three published MID
amplitudes on the *same* 318 clusters, same weights, same band,

    A_law = 1.9102 ± 0.1186,  A_newton = 10.17 ± 0.65,  A_HUT = 1.0109 ± 0.0632
    f_band ≡ Σ_ph/(Σ_b+Σ_ph) = 1 − A_law/A_newton = 0.8122 ± 0.0167                     (8)
    λ_req  ≡ (A_newton−1)(1−f_band)/f_band = A_law(A_newton−1)/(A_newton−A_law)
           = 2.1207 ± 0.1630                                                            (9)
    R_req  = λ_req · R_tot = 5.552 ± 0.427.                                             (10)

`λ_req/A_law = 1.110`, not 1: the amplitude multiplies the *total*, so the cold mass must be
rescaled by more than `A` itself (K14, K16). (10) sits **0.44σ from 5.364** and **6.9σ from
2.62** (K15). In dex the measured shortfall is 0.3265 against the cosmic 0.3116 — the two agree to
0.015 dex. The record's *post*-5.364 residual, `A_MID = 1.0109 ± 0.0632` rising to 1.21 in the
middle tercile (CFG949, CFG959 language), maps to `5.44 ± 0.42` to `6.75`: no further cold energy
is required (K20).

**9. The discriminator (Task 4).** One number, one dataset, two predictions:

    "cold = exactly the law's phantom":        A_MID = 1.000
    "cold = cosmic share, law emergent":       A_MID = 1 + (λ_cosmic−1) f_band = 1.852        (11)
    measured (CFG687, 318 eRASS1 × KiDS):      A_MID = 1.9102 ± 0.1186

The predictions are **7.18σ** apart; the data sit **0.49σ** from (11) and **7.67σ** from 1.000,
`Δχ² = 58.7` (K17). The shape channel is independent and points the same way: MID/OUTER = **0.966
± 0.102** for native cold debris against **1.888 ± 0.203** for the law's phantom (K18) — the law's
phantom is too centrally concentrated by 1.96×.

**10. The rule (Task 5).** The two ratios cannot be reconciled without one: (5) holds at a single
mass, and with the correct denominator `F(y_v) = N` holds nowhere. The missing ingredient is a rule
for how much of the acquired cold energy the law sources.

> **POSTULATE P-A18.** The law's phantom is the *sourced* share `u` of a system's acquired cold
> energy, with `u` a mass-independent constant: `u = 0.45 ± 0.03` at the two anchor systems (0.467
> MW-like, 0.439 cluster) and required to stay within 0.39–0.72 over `1e10–1e14 M☉`. The unsourced
> share `1−u` falls natively, is therefore more concentrated than the phantom, and is what the
> cluster cores show.

*Falsifier*: the MID/OUTER ratio of the stacked cluster excess. P-A18 requires the excess to be
dominated by natively-falling cold energy, hence `MID/OUTER ≤ 1`; the law's phantom alone gives
1.888 ± 0.203. A stack measuring **MID/OUTER > 1.3** kills P-A18 (>3.3σ above the present 0.966).
The present value is 0.966 ± 0.102, i.e. 3.3σ on the safe side.

## Status

- **Task 1 — DERIVED.** Two identities with different denominators, written explicitly as (2)/(3)
  and split as (4); the meeting condition is (5), one scalar, not an identity.
- **Task 2 — NO-GO(obstruction).** The agreement is a single crossing at `M_v = 1.7584e14 M☉`
  (c-independent, eq. 6); the law's ratio spans 647→3.0 across `1e8–1e15`, so no universal
  identification exists.
- **Task 3 — NUMERICAL / DECIDABLE.** Shortfall 0.3116 dex (cosmic) and 0.3265 dex (measured);
  `R_req = 5.552 ± 0.427`, 0.44σ from 5.364 and 6.9σ from 2.62.
- **Task 4 — DECIDABLE, and already decided on data on disk:** `A_MID`, `Δχ² = 58.7`.
- **Task 5 — CONDITIONAL(P-A18).** One new number (`u`), one falsifier (MID/OUTER > 1.3).

## Checks

`a18_checks.py` — 20 checks, deterministic, stdlib + numpy/scipy/sympy, 0.6 s, no network, exit 0
iff all pass. `a18.out` is the captured stdout.

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | (1) exact root of the law (sympy) | 0 | <1e-30 |
| K2 | (2) exact (sympy) | 0 | <1e-25 |
| K3 | closed-form inverse of `F`; `F(y*)=5.364327` | 0 | <1e-12 |
| K4 | `r*/r_M = 5.84297` | 5.842973027 | ±1e-9 |
| K5 | A11 anchors: `r_v` 0.2455/1.6863 Mpc, `R_tot` 25.04/2.62 | 7.9e-4 rel | <2e-3 |
| K6 | non-universality MW/cluster | 9.5659 | >2 |
| K7 | `R_enc = 5.364` at 1.7584e14, c-independent | spread 0 | <1e-9 |
| K8 | `R_tot` crossing c-dependent, all below 1.7584e14 | 3.79e13→1.64e14 | both < 1.758e14 |
| K9 | monotone, sign + at 1e8 / − at 1e15 | 647.5→3.005 | — |
| K10 | `u`(MW) 0.4668, `u`(cluster) 0.4392 | both <1 | ±0.01 |
| K11 | `u` over 1e10–1e14 (c=7) | 0.394–0.716 | [0.35,0.75], max/min<2 |
| K12 | `u=1` at `M_b=1.425e9` | 1.425e9 | 1e9–3e9 |
| K13 | cosmic shortfall at cluster | 0.3116 dex | 0.3113±1e-3 |
| K14 | `λ_req ≠ A` (amplitude is on the total) | λ/A=1.1102 | 1.05–1.20 |
| K15 | `R_req` vs 5.364 and 2.62 | 5.552±0.427 | <1σ, >3σ |
| K16 | `f_band` from `A_law/A_newton`, model-free | 0.8122 | ±0.01 |
| K17 | `A_MID` predictions separated; data on cosmic side | 7.18σ / 0.49σ | >5σ, <1σ |
| K18 | MID/OUTER shape: 0.966 vs 1.888 | 1 is the fence | — |
| K19 | `u=1` would need `f_ret`=0.214 (MW), 2.05 (cluster) | cluster >1 | — |
| K20 | post-5.364 residual maps to 5.44±0.42…6.75 | <0.5σ | — |

Two mutations, both recorded in `MUTATE.md`, both exit 1. **M1** (catchment = system, `f_ret = 1`)
breaks K10 (`u`(MW) 4.668), K11 and K12 — the lane's central denominator error. **M2** (read the
amplitude `A` as the rescaling `λ`) breaks K14 (`λ/A` = 1.0000).

## What this does not do

1. It does not derive `u`. P-A18 is a fitted one-parameter rule; the measured 0.394–0.716 is a
   1.8× spread, so "constant" is a 2× statement, not a precision one.
2. `f_ret` is not derived. `N` inherits the CFG416 three-segment table, and `u = R_tot/N` therefore
   inherits every error in it. The table's kink at `1e12.5` is visible as the dip in `u` at `1e11`.
3. `λ_req` in (9) is **CONDITIONAL(shape-preserving rescaling)**: it assumes the required extra cold
   mass follows the law's own radial shape. CFG949 shows a native NFW shape fits the same data with
   `A = 1.011` and *no* rescaling. The two routes agree on the *ratio* (5.55 vs 5.36) but they are
   not independent measurements of the same quantity.
4. (8)–(10) treat `A` as a ratio of weighted band sums, which is exact for the CFG686 estimator only
   because the weights are data-only and common to all three models. The band-to-3D mapping is not
   modelled; `f_band = 0.812` is a ΔΣ-weighted share, not a mass ratio (the 3D value at the
   MID band centre is 0.65).
5. Spherical symmetry and a Hernquist baryon profile throughout; no EFE (A11 §What-this-does-not-do
   item 4 applies unchanged), no disc geometry, no non-spherical baryons.
6. `A_MID` and `A_OUTER` are jackknife errors over 318 clusters of one survey and one shear
   catalogue; the 7.18σ separation is a *record-internal* significance, not a survey-independent one.
7. The `u > 1` statement below `M_b = 1.425e9` assumes the untruncated law profile at `r_v`; with
   truncation the demand is lower, so that mass is an upper bound on where truncation is forced.

## Next

The one measurement that would close this lane is not a new ratio but a **radial shape at fixed
mass**: `A_MID/A_OUTER` on a cluster stack binned by `M_500`, compared against the two frozen
predictions 1.888 (phantom) and ≤1 (native). That separation is a forecast, not a fit: at
`M_v = 1e13`, `R_tot = 10.45` (c=7) against a cosmic share of `N = 15.65`, a factor 1.50 — a
stacked group-scale lensing measurement with `σ(A) < 0.2` per bin separates them at >5σ. Datasets:
DESI Y3 or LSST Y1 group stacks, `0.3 < R < 2 Mpc`, cross-matched to ROSAT/eRASS1 X-ray groups.
Until then the honest statement is the one the record already supports: at cluster masses the cold
sector is at the cosmic ratio (0.44σ) and not at the law's phantom (6.9σ), and the law therefore
describes a *fraction* of it.
