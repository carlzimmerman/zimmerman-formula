# A20 — measuring the stiffness length `L*` from the inner structure of galaxies

Lane A20. Script `a20_checks.py` (18 checks), output `a20.out`, numbers `a20_results.json`,
pre-registration `FROZEN_CRITERIA.md` (written before the data were touched), mutations `MUTATE.md`. SI.

## Claim

**The prediction is sharp, the data are not, and one of the two candidate formulas is dead.**

**(1)** A16's `r_switch = L*` is exact only for a *self-gravitating* cold sector. Compared with the **total**
gravity — which is what a rotation curve measures — the ratio carries the cold-sector mass fraction,
`R(r) = f_c(r) (L*/r)^2`, so the core is **always smaller than `L*`**, at
`r_switch = L* sqrt(f_c(r_switch))`: **3.73 pc** in an MW-like halo and **18.40 pc** in a dwarf-like one for
`L* = 24 pc`, scaling quasi-linearly with `L*` (drift 15.5 % over 41.7×). Inside, the exact hydrostatic
solution of `p = pi G L*^2 rho^2` is the `n = 1` polytrope `rho = rho_0 sin(xi)/xi` with edge
`R_core = (pi/sqrt2) L* = 53.31 pc`, in which the pressure gradient equals gravity *identically* (K2). The
rotation-curve deficit saturates at `1 - sqrt(1 - f_c)`: **1.21–1.48 %** across the `L*` grid for the
MW-like halo and **35.8–53.6 %** for the dwarf — **the depth is set by `f_c`, the radius by `L*`**, and that
split is why the core is a dwarf phenomenon observationally even though `L*` is universal.

**(2)** **SPARC cannot see it.** The innermost tabulated radius over all 175 curves is **80 pc = 3.33 L***
and the 30″ beam floor is **142.5 pc**; **0/175** galaxies have an innermost reliable radius inside `L*` for
`L* = 24 pc` *and* for `L* = 100 pc` (0.00 % in both cases; 1.14 % at 300 pc, 22.29 % at 1 kpc). The
smallest resolvable `L*` in SPARC is **80 pc**, 3.33× the target. A16's "3.3×" is exactly this number.

**(3)** **LITTLE THINGS does bound it.** 26 dwarfs, 20–530 pc beams (median 157 pc), innermost points
10–470 pc. Requiring `R_core <= R0.3` (inside a core `v ∝ r`, so a core larger than the measured turnover
radius would force slope 1 where the data give 0.3) gives **`L* <= 90.0 pc`** from `IC_10`
(`R0.3 = 200 pc`), **184.6 pc** at the 10th percentile and 787.8 pc at the median. The window therefore
collapses from `[24 pc, 1 kpc]` to **`[24 pc, 90 pc]`**: 300 pc is excluded **3.33×**, 1 kpc **11.11×**.

**(4)** **No-juggling verdict.** Candidate 2, `L* = V_f^2/(9 a0)`, is killed at the first gate and twice
more after it: it predicts a **2.637 dex spread** of `L*` (9.8 pc – 4231.9 pc) where the pre-registration
demands one number, it puts **30.29 %** of the SPARC sample outside `[24 pc, 1 kpc]` (2.86 % below 24 pc,
27.43 % above 1 kpc), and its implied cold-medium dispersion is `V_f/3 = 55.07 km/s` for the MW —
**6.691×** the 8.23 km/s cold-phase value. Candidate 1, `L* = sigma_c^2/a0`, survives **at 24 pc**
(`sigma_c = 8.326 km/s`, **1.012×** the `10^4 K` thermal width, `R_core = 53.31 pc < 200 pc`) and dies at
the **1 kpc** end of its own window (`sigma_c = 53.742 km/s`, **6.530×**). **The surviving number is
`L* = 24 pc`; the number that kills candidate 2 is 55.07 km/s.**

**(5)** The best on-disk test of a 24 pc core is `DDO_210`'s innermost point (40 pc, `0.84 km/s` error): the
predicted dip there is **11.21 %**, i.e. **0.36 sigma**. Nothing on disk can do better.

## Derivation

`p = (gamma/2) rho_c^2` with `gamma = 2 pi G L*^2` (AG6D `Gamma = 2` polytrope, A16 §1); `R(r)` is the
pressure gradient in units of the local gravity; `f_c = rho_c/rho_tot = M_ph/(M_b+M_ph)`.

**1. The cusp ratio, and a correction to A16 (K1).** For `rho_c ∝ r^-n`, `M = 4 pi rho_c r^3/(3-n)`,
`g = G M/r^2`, and `(1/rho_c) dp/dr = gamma rho_c' = 2 pi G L*^2 rho_c'`,

    R_self(r) = |(1/rho_c) dp/dr| / g_self = [n(3-n)/2] (L*/r)^2 = (L*/r)^2   for n = 1, 2.       (1)

K1 returns residual `0` for both. Note A16's eq. (10) prints `2 pi G L*^2 |d ln rho_c/dr| / g`, which is
dimensionally short by one factor `rho_c`; their eq. (11) is right, because there `g` is the cold sector's
*own* gravity and `rho_c` cancels. That premise is the whole issue:

    R(r) = |(1/rho_c) dp/dr| / g_tot = [n(3-n)/2] (L*/r)^2 f_c(r) = (L*/r)^2 f_c(r),              (2)

for a common cusp slope (`n_c = n_tot`); if the two slopes differ the prefactor is `[n_c(3-n_tot)/2]`, still
O(1) and still density-free. From here on `n = 1` unless stated.

**2. The switch radius.** `R(r_switch) = 1` gives

    r_switch = L* sqrt(f_c(r_switch)),          (3)

so `r_switch <= L*` always, with equality only for a self-gravitating cold sector. For the two frozen halos
(Hernquist baryons + the frozen law, `y = g_N/a0`, `M_ph/M_b = (1/2)(sqrt(1+4/y)-1)`):

| halo | `M_b` | `a` | `r_M` | `f_c` at the switch | `r_switch(24 pc)` | `delta_plateau` |
|---|---|---|---|---|---|---|
| MW-like | `6e10` | 1.5 kpc | 9.453 kpc | 0.0241 | **3.73 pc** | **1.21 %** |
| dwarf-like | `1e8` | 0.7 kpc | 386 pc | 0.5882 | **18.40 pc** | **35.82 %** |

**3. The core is an exact polytrope (K2, K3).** With `p = pi G L*^2 rho^2` the hydrostatic equation is the
`n = 1` Lane–Emden equation, whose solution is `theta = sin(xi)/xi`. K2 verifies symbolically that
(a) the Lane–Emden residual is `0` and (b) `|(1/rho) dp/dr| / g_self = 1` **identically** — the pressure
gradient balances self-gravity at every radius, so this configuration **needs no rotation at all**
(`v_rot = 0` is an exact solution) and has no internal structure left to adjust. Its edge is

    R_core = pi a = (pi/sqrt2) L* = 2.22144 L* = 53.3146 pc at L* = 24 pc,                          (4)

which reproduces A16's `R_TF` to `1e-6` (K3). `R_core` is halo-independent and is the *largest* the core can
be, so using it in the C5 bound is conservative.

**4. The rotation-curve deviation.** With `v^2 = r(g_tot - (1/rho)dp/dr)` and `R` from (2),

    delta(r) = 1 - v/v_pure = 1 - sqrt(1 - min[1, (r_switch/r)^2]),                                 (5)

This is the **force-balance** deficit `delta_F`: the fraction of the weight the pressure carries. It equals
1 at `r_switch` (pressure carries all of it) and falls as `(1/2)(r_switch/r)^2` outside — the
halo-independent ladder of K4: `delta_F = 50 %` at `1.154701 r_switch`, `10 %` at `2.294157 r_switch`, `1 %`
at `7.088812 r_switch`, `0.1 %` at `22.366 r_switch`. The **observable** deficit is smaller, because the
cold mass is redistributed rather than removed: for `r << r_switch` the polytrope pushes essentially all of
it outside `r`, so `delta_obs` saturates at `1 - sqrt(1-f_c)` — 1.21 % (MW) / 35.82 % (dwarf) at
`L* = 24 pc`. The two are different numbers for different questions; both are reported below, labelled.

**5. The prediction table (K5, K6).** `r_switch` in pc, `delta_F` at fixed radii (`dF`), and `d_obs` = the
saturated observable deficit:

| `L*` (pc) | halo | `r_switch` | `R_core` | `dF(2 r_sw)` | `dF(5 r_sw)` | `dF(100 pc)` | `dF(500 pc)` | `d_obs` plateau |
|---|---|---|---|---|---|---|---|---|
| 24 | MW | 3.73 | 53.3 | 13.40 % | 2.02 % | 0.07 % | 0.003 % | 1.21 % |
| 100 | MW | 15.64 | 222.1 | 13.40 % | 2.02 % | 1.23 % | 0.05 % | 1.23 % |
| 300 | MW | 47.87 | 666.4 | 13.40 % | 2.02 % | 12.20 % | 0.46 % | 1.28 % |
| 1000 | MW | 171.64 | 2221.4 | 13.40 % | 2.02 % | 100 % | 6.08 % | 1.48 % |
| 24 | dwarf | 18.40 | 53.3 | 13.40 % | 2.02 % | 1.71 % | 0.07 % | **35.82 %** |
| 100 | dwarf | 78.23 | 222.1 | 13.40 % | 2.02 % | 37.72 % | 1.23 % | **37.72 %** |
| 300 | dwarf | 244.93 | 666.4 | 13.40 % | 2.02 % | 100 % | 12.82 % | **42.26 %** |
| 1000 | dwarf | 885.69 | 2221.4 | 13.40 % | 2.02 % | 100 % | 100 % | **53.57 %** |

The *shape* in units of `r_switch` is identical in both halos (columns 5–6 are constants) — that is the
density-free content of (1). What differs is where the knee sits (`r_switch`) and how deep the plateau is
(`f_c`). **"Maximum fractional deviation and radius where it peaks": the deviation is a plateau, not a bump —
`delta_obs` is maximal for every `r <= r_switch` and its knee is at `r_switch`.** For `L* = 24 pc` that is
1.21 % at 3.73 pc (MW) and 35.82 % at 18.40 pc (dwarf); `delta_F` at the same knee is 100 % by definition.

**6. What SPARC can resolve (K7–K9).** 175 curves, 3391 points, `D = 0.98–127.8 Mpc` (median 16.5),
`r_first = 80–9930 pc` (median 630). With the frozen 30″ HI beam, `beam_pc = 145.4 D[Mpc]` — **142.5 pc** at
the nearest galaxy (`D = 0.98 Mpc`), **2399.8 pc** at the median distance. `r_rel = max(r_first, beam)`:

| `L*` | 24 pc | 100 pc | 300 pc | 1000 pc |
|---|---|---|---|---|
| fraction with `r_first < L*` | 0.00 % | 3.43 % | 23.43 % | 71.43 % |
| fraction with `r_rel < L*` (**primary**) | **0.00 %** | **0.00 %** | **1.14 %** | **22.29 %** |

So SPARC returns a **null for 24 pc and for 100 pc** — not a marginal one: the floor is 80 pc (tabulated) or
142.5 pc (beam), i.e. **3.33×** and 5.94× the target.

**7. What LITTLE THINGS can bound (K11–K13).** 26 dwarfs; per-galaxy beam `Rmax/(Rmax/HI)` = 20.0–530.0 pc
(median 156.6); `r_first = 10–470 pc`; `R0.3 = 200–5430 pc` (median 1750). Because `L*` is **one number**,
the single best-resolved galaxy bounds the sample:

    L* <= min_g R0.3(g) / 2.22144 = 200 pc / 2.22144 = 90.0 pc   (IC_10, D = 0.70 Mpc, beam 20 pc).   (6)

The bound is not a one-galaxy fluke: 30.77 % (8/26) of the sample individually excludes `L* >= 300 pc`, the
10th percentile of the per-galaxy bound is 184.6 pc, and a cruder `v = 0.8 v_max` estimator gives 151.9 pc.
Only 2/26 galaxies have `r_first < 53 pc` (the `L* = 24 pc` core size) — `WLM` (10 pc) and `DDO_210`
(40 pc) — so the 24 pc core is *at* the resolution limit of exactly two objects.

**8. The two candidates against the frozen criteria (K14–K17).** `sigma_c = sqrt(a0 L*)` inverts each
`L*` into the dispersion the cold medium must have; `8.23 km/s` is the `10^4 K`, `mu = 1.22` thermal width.

| | C1 one number | C3 window | C4 `sigma_c/8.23` | C5 `R_core` vs 200 pc | verdict |
|---|---|---|---|---|---|
| **cand 1** `L* = sigma_c^2/a0`, `L* = 24 pc` | 0.000 dex ✔ | 24 pc ✔ | **1.012** ✔ | 53.3 pc ✔ | **SURVIVES** |
| cand 1 at `L* = 1 kpc` | 0.000 dex ✔ | 1 kpc ✔ | **6.530** ✘ | 2221 pc ✘ | fails |
| **cand 2** `L* = V_f^2/(9 a0)` | **2.637 dex** ✘ | **30.29 %** ✘ | **6.691** ✘ | 9401 pc ✘ | **NO-GO** |

Candidate 2's failure is structural: `V_f^2/a0 = r_M` is the MOND radius, so `L* = r_M/9` is a *galaxy
property*, not a medium property — it cannot be one number, and the cleanest single number that kills it is
`sigma_c = V_f/3 = 55.07 km/s` against the 8.23 km/s cold phase (**6.691×**, and 32.16 km/s at the median
SPARC `V_f = 96.47 km/s`, 3.91×). Candidate 1 passes only because the *bottom* of the window is the thermal
width of `10^4 K` gas; its own upper end (53.742 km/s) is not a cold medium. **The window's surviving part
is [24, 90] pc and the dispersion picks the bottom of it.** Two independent criteria land on the same
ceiling: C5 (the LITTLE THINGS turnover) gives `L* <= 90.0 pc`, and C4 alone (`sigma_c <= 2 x 8.23 km/s`)
gives `L* <= 93.8 pc`. The upper half of the record's window is not merely unmeasured — it is excluded by
two different kinds of measurement.

**9. The other HI data on disk (K10).** `MIGHTEE-HI DR1` cutouts (`mightee_pipeline_2026_10_19`, 7 cubes)
have `beam = 75.6"`, `z = 0.047`, `D_L = 216.2 Mpc`, i.e. **79.3 kpc** linear resolution — 3302× `L*`, no
bound. The 21 ALFALFA global profiles (`hi_profiles_2026_10_18`) have no spatial information at all and
cannot isolate the cold-phase dispersion (they are rotation-dominated).

## Status

- **Task 1 — DERIVED, with a correction to the motive.** (1)–(5) are exact or symbolic (`K1`–`K3` residual
  0). The switch is at `L* sqrt(f_c)`, **not** at `L*`, once total gravity is used; the core is the `n = 1`
  polytrope with `R_core = 2.22144 L*`, which needs no rotation. `delta_plateau` = 1.21 % (MW) / 35.82 % (dwarf)
  at `L* = 24 pc`.
- **Task 2 — NUMERICAL / null.** **0/175** SPARC galaxies reach inside `L* = 24 pc` (0/175 at 100 pc);
  floor 80 pc = 3.33 `L*`. SPARC **cannot** see a 24 pc core, and the smallest `L*` it could resolve is
  **80 pc**.
- **Task 3 — NUMERICAL / bound.** `L* <= 90.0 pc` (LITTLE THINGS, one shared number), 184.6 pc at the 10th
  percentile; window `[24, 90] pc`, 300 pc excluded 3.33×, 1 kpc 11.11×.
- **Task 4 — DECIDABLE, decided.** Candidate 2 **NO-GO(C1)** and independently fails C3 (30.29 %) and C4
  (6.691×). Candidate 1 **survives at `L* = 24 pc`** and is excluded at 1 kpc by C4 (6.530×).
- **Task 5 — forecast.** `ngVLA` 21 cm, 0.15″ (reaches 24 pc out to 33 Mpc), ~30 dwarfs with
  `V_f < 40 km/s` inside 8 Mpc, 3 km/s channels, `0.3 km/s` per point: a 21.03 % dip at 30 pc and 11.21 % at
  40 pc, ≥ 5 sigma per galaxy in a stack.

## Checks

`a20_checks.py`: 18 checks, deterministic, 3.5 s, stdlib + numpy + sympy, no network, exit 0 iff all pass.

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | (1) exact for `n = 1, 2` (sympy) | residual `0, 0` | exactly 0 |
| K2 | `n = 1` polytrope is exact hydrostatic: `LE = 0`, ratio `= 1` | `0` ; `1` (signed −1) | 0 ; 1 |
| K3 | `R_core = 2.22144 L*` reproduces A16 `R_TF` | 53.3146 pc | 53.3146 ± 1e-6 |
| K4 | the ladder `1.1547 / 2.2942 / 7.0888 / 22.366` | exact | 1e-5 |
| K5 | plateau depths, MW vs dwarf | 1.484 % ; 35.82 % | 0.0148±0.001 ; 0.3582±0.005 |
| K6 | `r_switch` quasi-linear in `L*` | 46.06 / 48.12 (drift 15.5 %) | 41.67 ± 20 % |
| K7 | SPARC census | 175 / 3391 | 175 / 3391 |
| K8 | fraction inside `L*` (`r_rel`) | 0 / 0 / 1.14 % / 22.29 % | exact |
| K9 | SPARC floor vs 24 pc | 80 pc = 3.33× | > 3× |
| K10 | MIGHTEE linear resolution | 79.3 kpc = 3302× 24 pc | > 100× |
| K11 | LITTLE THINGS census | 26 gal, beam 20–530 pc | 26, 20 pc |
| K12 | C5 core bound | `L* <= 90.0 pc` | < 100 pc |
| K13 | window after the bound | 300 pc 3.33×, 1 kpc 11.11× | > 2× |
| K14 | C1 spread | 0.000 ; 2.637 dex | exact |
| K15 | C3 window fraction | 30.29 % | ±0.5 % |
| K16 | C4 dispersion ratios | 1.012 / 6.530 / 6.691 | ±0.02 |
| K17 | C5 `R_core` | 53 pc ; 9401 pc | < 200 ; > 200 |
| K18 | forecast arithmetic | 21.03 % / 11.21 % ; 0.62″ at 8 Mpc | exact |

## What this does not do

1. **No detection.** No galaxy on disk resolves `L* = 24 pc`; the result is a null (SPARC) plus a one-sided
   bound (LITTLE THINGS), not a measurement of the core.
2. **`L*` is still not derived.** Candidate 1 surviving at 24 pc is a *consistency* statement: it says the
   number that makes the cold medium `10^4 K` thermal gas also sits at the bottom of the window and below
   the core bound. The `10^4 K` is an external astrophysical input, not a theorem.
3. **The C5 bound assumes the cold sector dominates the inner mass.** For `f_c = 0.5` the bound weakens by
   `1/sqrt(f_c)` to 127 pc, and at `f_c = 0.25` to 180 pc — still below 300 pc, but the "90 pc" is the
   `f_c -> 1` reading. `IC_10`'s own `V_DM/V_tot` from the published decomposition is unstable (values
   `> 1` at the inner points), so no joint `chi^2` fit was attempted; the bound is deliberately
   assumption-light.
4. **The 30″ SPARC beam is an external choice** (`[EXT]`), not measured per galaxy; at 15″ the floor becomes
   71 pc (still 2.97× 24 pc) and at 60″ 285 pc. The *null* for 24 pc survives the whole 15–60″ range
   because the tabulated `r_first` floor (80 pc) is independent of it.
5. **`f_c` uses a Hernquist baryon model** with `M_b`, `a` frozen in `FROZEN_CRITERIA.md` §4. The
   `delta_plateau` values are model-dependent at the factor-2 level; the *scaling* `r_switch ∝ L* sqrt(f_c)`
   and the ordering MW << dwarf are not.
6. **`R_core = 2.22144 L*` is the mass-conserving polytrope edge.** A density-matched embedding gives a
   smaller core; the conservative (largest) choice was used for the bound.

## Next

1. **The decisive measurement**: `ngVLA` 21 cm at **0.15″** (2.9 pc at 4 Mpc), 3 km/s channels, **N ≈ 30**
   dwarfs with `V_f < 40 km/s` inside **8 Mpc**, reaching `0.3 km/s` per 10 pc point. The statistic is the
   *turnover*, not the slope: `v(30 pc)/v(100 pc) = 0.80` versus 1.00 for any core-free model — a 21.03 %
   dip, ≥ 5 sigma per galaxy. A 24 pc core must also show `v -> 0` at `18.4 ± 2 pc`; that is the signature
   no cored-halo fit reproduces.
2. **Cheaper intermediate**: `JWST/NIRSpec` or `ELT/HARMONI` Hα IFU at 0.1″ on the same dwarfs reaches
   0.48 pc at 1 Mpc and tests the turnover in the nearest 3–5 systems years earlier.
3. **Do not** re-run SPARC for this: `0/175` at 24 pc and 100 pc is a hard null set by `r_first >= 80 pc`,
   not by sample size.
4. **Theory side, one open premise**: `f_c` at the switch decides whether the core is a dwarf-only
   phenomenon. That is a statement about the cold sector's fraction in the inner 20 pc of a spiral, which
   no current data constrain; it is the single number that would turn `delta_plateau = 1.21 %` into a
   prediction for `MW`-like disks.
