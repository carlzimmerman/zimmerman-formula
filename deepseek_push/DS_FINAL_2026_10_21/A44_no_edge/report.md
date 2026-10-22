# A44 — the NO-EDGE tension: an edge, not a slope; a denominator, not a step

Lane A44. Script `a44_checks.py`, output `a44.out`, numbers `a44_results.json`, mutations `MUTATE.md`.
Footings: `a0 = 9.3603e-11` (canonical, quoted first) and `1.1312e-10 m/s^2` (alt, in the JSON), never pooled.

## Claim

**The mass budget is not what the KiDS-1000 isolated lensing tests.** At fixed shape, the cold mass of the
law's phantom is degenerate with the profiled baryon mass (exactly so up to the small baryon point mass):
multiplying it by 6 or by 10 returns the same χ² = 493.45 and moves the best-fit `M_b` down by the same
factor (the `EA` block of `a44_results.json`). What the data fix is the
**radius at which the profile stops**. The record's excluded model (Zenodo 23420675 / CFG801) cuts the law
phantom at `r_e = 5.8426 r_M`, where its enclosed mass is `5.364 M_b` — **34–81 kpc** for the four bins. The
census model that fits (`N = 1/f_ret = 6–10`, CFG804) is the *same function with the same `M_b`-locked
amplitude*, cut at `31–54 r_M` = **0.19–0.45 Mpc**; the extra 25–48 `M_b` sits entirely outside `r_e`. So
the difference is a truncation radius — **an edge, not a slope** — and the fit is bought with the edge, not
with the mass: at the *same* cold mass of 31.9 `M_b`, moving the cut from 5.84 to 32.5 `r_M` moves Δχ² from
**+409.6 to −8.2** (K5c), while the same mass in an NFW halo gives **+112.7** (K6).

**The A29 splashback step does not resolve it.** At the four KiDS masses `r_sp = 1.3674 r200c = 152, 210, 232,
271 kpc`, i.e. **3.35–4.46 × r_e**: the suppressed region covers the inner two-thirds of the primary range
(0.035–0.15 of 0.035–0.30 Mpc in log R for bin 1), and the step cannot be where the edge is. Applied literally with the *system's* cosmic share, the step makes the tension worse:
Δχ² = **+244.8** against +197.0 for the truncation it was meant to repair (K8c). Applied on the full
phantom it still fails, **+94.8**, and the u it requires is **0.96** — 9.7σ from A29's 0.47 (K8, K8b). Only
when the step is combined with **A18's catchment denominator** (cold mass `5.364/f_ret = 53.64 M_b` inside
`r_sp`) does it come close: **+11.1**, an 18× reduction, still 3.3σ from no step (K8d).

**What resolves it is A18's denominator, not a new profile.** `5.364 M_b,ta = 5.364 M_b/f_ret` with
`f_ret = 0.10` is **53.64 M_b**, and the edge where that is used up is `r_e = 54.14 r_M` = 0.19–0.75 Mpc.
That model — the *same* law phantom, no step, no shape change — gives **Δχ² = +1.1** (alt: −0.0), and its
per-bin census version reproduces the record's −0.3 / +150.7 against the published −0.2 / +148.7 (K10).
The number that decides is `f_ret = 0.10`: it is a factor **10.0** between the excluded model and the
accepted one, and it moves Δχ² by **195.9**. The second number is the cold mass the data require inside
0.31 Mpc: **4.0–9.6 × 5.364 M_b = 1.2–2.8 × 10^12 M_sun** (K11), which only the catchment budget holds.

## Derivation

Units `c = 1`; `G = 4.30091e-3 pc (km/s)²/M_sun`; `a0 = 9.3603e-11 m/s²`; `M_☉ = 1.98847e30`; `h = 0.674`;
`ρ_crit = 1.2607e11 M_sun/Mpc³`. Data: Brouwer+21 KiDS-1000 Fig. 3, 4 stellar-mass bins × 15 radii
(0.0354–2.6035 Mpc), the full 60×60 covariance with the `(1+K)` correction, primary = the 8 radii
`R ≤ 0.31 Mpc`. `M_b` is profiled per bin on `log M_b = 9.00…12.00` (0.01 dex), one number per bin, applied
identically to every model — CFG801's estimator, reproduced to the digit (K2, K3).

**1. What was truncated, and at what radius (task 1).** The law's settled (phantom) profile, in
`x = r/r_M`, `r_M = √(GM_b/a0)`:

    ρ_c(r) = (M_b/r_M³) ρ̂(x),   ρ̂ = 1/(2π x √(1+4x²)),
    M_c(<r)/M_b = m(x) ≡ ½(√(1+4x²) − 1)  →  M_b x  at large x.                      (1)

`m(x) = 5.364` at `x_e = √(5.364 × 6.364) = 5.8426`, i.e. `r_e = r_M√(N(N+1))` with `N = 5.364` — exactly
the relation A16 (and A11 eq. 7) uses for the supply edge. K5 checks the normalization independently:
`4π∫₀^{x_e} x²ρ̂ dx = 5.364000`, and the projected cold mass at infinity is 5.362 `M_b` (CFG801's K-check).
For the four bins at the no-edge-preferred `M_b = 2.29, 6.03, 8.13, 12.9 × 10^10 M_sun`, `r_M = 5.8, 9.5,
11.0, 13.9 kpc` and **`r_e = 34.1, 55.3, 64.3, 80.9 kpc`**. (CFG801 quotes 44–90 kpc because it profiles
`M_b` 0.22 dex *higher* inside the edge — the edge model's own compensation for the missing outer mass.)
Truncating here is excluded: **Δχ² = +197.0** on the primary range and **+753.0** at all radii (K3;
alt +234.0 / +813.0, K3b). This is the record's number.

**2. What the census `N = 6–10` implies (task 1).** Not a different profile. CFG804's `profile(s_max)`
projects the *same* `ρ̂`, normalized to the *same* `M_b`; `N` enters only through
`s_max = √(((2·5.364·N+1)²−1)/4)`, the radius where `m(x) = 5.364 N`. So the census model has

    cold mass 5.364 N M_b = 30.5 … 53.6 M_b,   s_max = 30.6 … 54.1 r_M = 0.32 … 0.45 Mpc,     (2)

with an inner amplitude *identical* to the excluded model. All of the extra 25–48 `M_b` lies outside
`r_e`. The census is therefore a statement about the edge, and — because the amplitude is degenerate with
`M_b` — **not** a measurement of a larger mass.

**3. Edge or slope? Three tests.** (a) *Same function*: at every `x ≤ 5` the 5.364 `M_b` and 53.64 `M_b`
profiles agree in 3D exactly and in projection to ≤ 7.3%, the difference being the line-of-sight column of
the outer mass that the bigger halo adds (K5). (b) *Same mass, two edges*: 31.9 `M_b` cut at 5.84 `r_M`
gives Δχ² = **+409.6**; cut at 32.5 `r_M` gives **−8.2** (K5c). (c) *Same mass, other shape*: an NFW with
`M200 = 5.364 M_b` and `c200 = c_DM14(M200) = 10.16, 9.21, 8.94, 8.53` gives **+112.7** (K6). The edge is
the discriminator; the shape is not, and the mass is not measured at all. A fourth statement makes the last
point explicit: `EA(6)` and `EA(10)` — the same 5.84 `r_M` cut with 6× and 10× the cold mass per baryon —
both return χ² = 493.45 with `M_b` lower by the same factors (the degeneracy is exact for the cold part and
broken only by the fixed baryon point mass).

**4. The two profiles at the same total mass (task 2).** (i) the cosmic share truncated at
`r_e = 5.8426 r_M`; (ii) the same `5.364 M_b` in an NFW with the census concentration. `ΔΣ(R)` in
`h70 M_sun/pc²`, at the data radii, for the lowest and highest stellar-mass bins:

| R [Mpc] | data (bin 1) | (i) E(5.364) | (ii) NFW | no edge | data (bin 4) | (i) | (ii) | no edge |
|---|---|---|---|---|---|---|---|---|
| 0.1208 | 10.40 ± 2.12 | 3.18 | 3.09 | 8.37 | 19.16 ± 3.07 | 17.87 | 12.62 | 20.70 |
| 0.1643 | 6.63 ± 1.57 | 1.72 | 1.92 | 6.11 | 17.83 ± 2.28 | 9.67 | 8.14 | 14.94 |
| 0.2233 | 3.53 ± 1.17 | 0.93 | 1.18 | 4.47 | 17.48 ± 1.69 | 5.23 | 5.18 | 10.83 |
| 0.3035 | 1.89 ± 0.87 | 0.50 | 0.72 | 3.27 | 9.17 ± 1.26 | 2.83 | 3.25 | 7.89 |
| 0.4126 | 1.51 ± 0.64 | 0.27 | 0.44 | 2.40 | 7.83 ± 0.94 | 1.53 | 2.01 | 5.76 |
| 0.5609 | 1.92 ± 0.48 | 0.15 | 0.27 | 1.76 | 6.12 ± 0.70 | 0.83 | 1.23 | 4.21 |
| 0.7625 | 2.06 ± 0.36 | 0.08 | 0.15 | 1.29 | 3.96 ± 0.52 | 0.45 | 0.75 | 3.09 |
| 1.0365 | 1.28 ± 0.27 | 0.04 | 0.08 | 0.95 | 3.15 ± 0.39 | 0.24 | 0.46 | 2.26 |

with the record's covariance: **(i) Δχ² = +197.0** (all radii +753.0); **(ii) Δχ² = +112.7** (all +473.2).
The NFW is less bad than the truncation — it still has mass beyond 34–81 kpc — but it is still excluded at
8σ, and it is excluded in the *opposite direction*: at 0.12–0.30 Mpc its slope is `d lnΔΣ/d lnR = −1.31 …
−1.50` against the data's −0.66 … −1.85 and the law's −0.95 … −0.98 (the NFW is too steep, the truncation
too steep in the point-mass limit, the law about right). Letting `c` vary does not rescue it: `c = 4.5`
gives +70.9, `c = 10` +127.2, `c = 20` +185.6. *A different shape at the same mass does not fit.*

**5. The A29 step: geometry (task 3).** A29 measures `u = 1+3⟨w⟩` with `u = M_ph/M_c` the phantom's share of
the observed cold mass: `u_in = 0.335/0.412/0.472` inside and `0.986` outside, with
`r_sp = 0.83 r200m = 1.3674 r200c`. For the four KiDS bins, taking `M200 = M_b + M_c = 6.364 M_b`:

| bin | `M_b` | `r_M` | `r_e` | `r_sp` | `r_sp/r_e` | `M_ph(r_sp)/5.364M_b` | `M_ph(r_sp)/53.64M_b` |
|---|---|---|---|---|---|---|---|
| 1 | 2.29e10 | 5.8 kpc | 34.1 kpc | 152.2 kpc | **4.46** | 4.77 | 0.477 |
| 2 | 6.03e10 | 9.5 | 55.3 | 210.2 | **3.80** | 4.04 | 0.404 |
| 3 | 8.13e10 | 11.0 | 64.3 | 232.2 | **3.61** | 3.84 | 0.384 |
| 4 | 12.9e10 | 13.9 | 80.9 | 270.7 | **3.35** | 3.55 | 0.355 |

`r_sp = r_e` only at `M_b = 1.8 × 10^14` (`M200 = 1.15 × 10^15`, K7c). Below that mass — every galaxy and
group, and all but the most massive clusters — **the splashback radius is outside the radius at which the
cosmic share is already spent**, by 5× at these galaxies. "u = 1 outside r_sp" therefore describes a region that, on the
`5.364 M_b` budget, should contain no cold mass at all; "u = 0.47 inside r_sp" suppresses the amplitude
exactly where the truncation has already left a deficit. The A29 *stack* is itself ambiguous: its
`r200c = 1.032 Mpc` implies `M200 = 1.16 × 10^14`, so `r_sp/r_e = 1.47` on the self-consistent
`M_b = M200/6.364 = 1.83 × 10^13`, but 0.53 if one instead uses A18's much larger cluster anchor
`M_b = 1.4 × 10^14`. The record does not fix the sign of this ratio for clusters; it is fixed — positive —
for the galaxies this lane is about.

**6. The A29 step: ΔΣ and Δχ² (task 3).** Four readings, all with `M_b` profiled:

| model | what it is | Δχ² primary | Δχ² all |
|---|---|---|---|
| S1 | step + the **system** cosmic share inside `r_sp`, cut at `r_sp` | **+244.8** | +728.1 |
| S2 | the `r_e` truncation kept, amplitude × u | +185.3 | +737.0 |
| S3 | step applied to the full phantom (no renormalisation), cut at the catchment edge | **+94.8** | +99.2 |
| S4 | step + the **catchment** share `5.364/f_ret` inside `r_sp`, cut at `r_sp` | **+11.1** | +330.9 |
| — | catchment share, **no step**, cut at `54.14 r_M` | **+1.1** | +54.6 |

`ΔΣ` at 0.1208 Mpc for bin 1: data 10.40, S1 1.31, S3 4.05, S4 8.64, no-step catchment 8.40. The step with
the system share is worse than the truncation (**+244.8 vs +197.0**, K8c) because it both keeps the edge at
152 kpc and halves the amplitude inside it. The step on the full phantom is excluded at **+94.8**, and the
u it would need is **0.96 ± 0.03** — A29's 0.47 is 9.7σ away (K8b). S4 shows what is really going on: once
the budget inside `r_sp` is the *catchment* value (53.64 `M_b`), the step's amplitude is right by
construction — `u_in × A = u_in × 53.64/m(x_sp) = 0.47 × 2.1 = 1.0` — and Δχ² falls from +197 to +11.
But +11 is still above CFG801's own frozen threshold of 9: the sharp cut at `r_sp` costs 3.3σ relative to
the same profile continued smoothly (K8d). **The step is consistent in amplitude and not required in shape.**

**7. Why the denominator, and not the step, is the answer (task 4).** A18's Eq. (7) defines the cold budget
per *system* baryon as `N = R_cosmic/f_ret`, with `f_ret` the CFG416 retained fraction at the turnaround
mass. For `M_b ≈ 10^10–10^11 M_sun`, `f_ret = 0.10` and `N = 53.64`, i.e. the cold mass is
`5.364 M_b,ta`, **ten times** the `5.364 M_b` of the system's own baryons. The edge where *that* is used up
is `54.14 r_M`, and the same law phantom then gives Δχ² = **+1.1** (alt −0.0). The record's accepted census
model is the same statement with the per-bin `f_ret`: `N = 10.0, 8.95, 7.35, 5.68`, cold masses 53.6, 48.0,
39.4, 30.5 `M_b`, edges 54.1, 48.5, 39.9, 31.0 `r_M` — **reproduced here at −0.3 / +150.7 against the
published −0.2 / +148.7** (K10; alt −1.7 / +174.9 against −1.5 / +172.2, K10b; the 0.1–2 residuals are the
0.15-dex `M_b` table and the record's 0.25-wide `N` snapping). So the census model that "fits with no
free parameter" is not evidence for an edgeless halo: it is evidence that the cosmic share must be applied
to the **catchment**, exactly as A18 says, and it is why the same data exclude the system-denominator
version at +197.

**8. The numbers that decide.** Two, and they agree:

- **`f_ret = 0.10`.** It multiplies the budget by 10.0 and moves `r_e` from 34–81 kpc to 0.19–0.75 Mpc;
  Δχ² falls from **+197.0 to +1.1**. No new profile, no new parameter — a denominator (K9).
- **`M_c(<0.31 Mpc) = 9.60, 5.88, 5.05, 3.99 × 5.364 M_b` for bins 1–4 = 1.2–2.8 × 10^12 M_sun** (K11). The data demand
  4–10× the system's cosmic share inside the primary range; the catchment budget (30.5–53.6 `M_b`) is the
  only one that contains it. Equivalently, the edge required at Δχ² ≤ 4 is `N ≥ 15.9 M_b`,
  `r_e ≥ 16.4 r_M` = **0.10–0.23 Mpc**, 2.97× the cosmic-share edge (K11b).

The `u` that A29 measures is what this geometry predicts: `u_in = M_ph(r_sp)/(5.364/f_ret) = 0.48, 0.40,
0.38, 0.36` for the four bins, bracketing the measured 0.41–0.47. That is a consistency, not a derivation —
the same formula gives 0.49 or 1.51 for the A29 stack depending on its `M_b` route, so `u_in` stays a
premise (A29's P1′).

## Status

- **Task 1 — NUMERICAL.** Truncated object: the law phantom `ρ̂` of (1); radius `r_e = 5.8426 r_M`
  (34.1–80.9 kpc), where `m(x) = 5.364` exactly (`4π∫x²ρ̂dx = 5.364000`). The census `N = 6–10` implies the
  same function at the same `M_b` with `s_max = 31–54 r_M` (0.19–0.45 Mpc) and 30.5–53.6 `M_b` of cold
  mass, all of the excess outside `r_e`. **The difference is an edge, not a slope** (K5, K5c, K6); the
  mass itself is degenerate with the profiled `M_b` and is not measured.
- **Task 2 — NUMERICAL / NO-GO(shape).** (i) `+197.0 / +753.0`; (ii) NFW at the same mass
  `+112.7 / +473.2` (c-scan +70.9 … +185.6). Both excluded; the NFW is too steep (`−1.3 … −1.5` against the
  data's `−0.66 … −1.85`) and the truncation too steep beyond `r_e` (point-mass `−2`).
- **Task 3 — NO-GO(as stated) / CONDITIONAL(with the catchment budget).** `r_sp/r_e = 3.35–4.46` at the
  four KiDS masses; S1 `+244.8`, S2 `+185.3`, S3 `+94.8` (`u_req = 0.96`, 9.7σ), S4 `+11.1`. The step
  repairs the amplitude only when the budget inside `r_sp` is the catchment share, and even then the sharp
  cut is 3.3σ disfavoured against no step.
- **Task 4 — DECIDABLE, and decided on data on disk.** The tension is a denominator, not a profile:
  `5.364 M_b,ta = 5.364 M_b/f_ret` with `f_ret = 0.10` → 53.64 `M_b`, `r_e = 54.14 r_M`, Δχ² `+197.0 →
  +1.1`. The splashback step is neither necessary (no-step wins by 10.0 in Δχ²) nor sufficient
  (`+11.1` on its best reading).

## Checks

`a44_checks.py` — 22 checks, deterministic, stdlib + numpy/scipy, 50 s, no network, exit 0 iff all pass;
three mutations each break a group (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | data: 4×15 rows, 60×60 covariance symmetric, diag = quoted error² | asym 0, dev 6.2e-5 | <2e-3 |
| K1b | primary radii `R ≤ 0.31 Mpc` | 8 radii, `R_max` 0.3035 | = 8 |
| K2 | no-edge reference reproduces CFG801 | 83.86 | ±0.1 |
| K2b | alt no-edge reference | 79.71 | ±0.3 |
| K3 | CFG801 reproduction | +197.0 / +753.0 | ±0.5 / ±1.0 |
| K3b | CFG801 alt reproduction | +234.0 / +813.0 | ±1.5 / ±2.0 |
| K5 | law profile integrates to 5.364 `M_b` at `r_e`; 5.364/53.64 `M_b` halos share the 3D density | 5.364000; ΔΣ dev 7.3% | <1e-4; <10% |
| K5b | same, alt footing | 5.364000; 7.3% | same |
| K5c | same mass 31.9 `M_b`, two edges | +409.6 vs −8.2 | >300, <40 |
| K6 | NFW at the same mass still excluded | +112.7 | >100 |
| K7 | `r_sp > 3 r_e` at all four KiDS masses | 3.35–4.46 | >3 |
| K7b | `M_ph(r_sp)` exceeds the cosmic share | 3.55–4.77× | >3 |
| K7c | the step can sit inside the edge only above `M_b = 1e14` | crossover 14.26 | >14 |
| K8 | A29 step at u = 0.4716 excluded | +94.8 | >9 |
| K8b | u required by the data | 0.96 | ≥0.8 |
| K8c | S1 worse than the truncation | +244.8 vs +197.0 | > |
| K8d | S4 repairs E1 | +11.1 vs +197.0 | drop >150 |
| K9 | catchment share fits where the system share fails | +1.1 vs +197.0 | <5 |
| K10 | CFG804 reproduction | −0.3 / +150.7 | ±1.5 / ±5 |
| K10b | CFG804 alt reproduction | −1.7 / +174.9 | ±1.5 / ±6 |
| K11 | `M_c(<0.31 Mpc) > 3 × 5.364 M_b` | 9.60/5.88/5.05/3.99 | ≥3 of 4 |
| K11b | edge required > 2× the cosmic-share edge | `N = 15.9 M_b`, 2.97× | >2 |

## What this does not do

1. **The 2-halo term is not modelled.** The record's own number is that it narrows the outer deficit from
   +149 to +11 (effective bias 0.2–0.5). At 0.2–0.31 Mpc a 10^10 `M_sun` galaxy is 1.8–2.8 `r200` from its
   centre, so the outer primary radii are the least clean and are exactly where S4's +11 is incurred. The
   +1.1 of the no-step catchment model is not immune either: its all-radii Δχ² (+54.6) is a 2-halo-shaped
   residual, and the all-radii scan prefers an even larger edge (`N = 100`, −15.1).
2. **`f_ret` is inherited, not derived.** The CFG416 three-segment table (0.10 below `M_ta = 1e12.5`) is an
   input; `N = 5.364/f_ret` inherits every error in it. The claim "the denominator is the answer" is only as
   good as that table — a framework-native `f_ret` (CFG806's failed attempt) would be the derivation.
3. **`M_b` is profiled, so the normalization is not independently measured.** The amplitude of any
   scale-free profile is exactly degenerate with `M_b`; only the edge and the shape are constrained. The
   best-fit `M_b` sits 0.1–0.2 dex above the provisional `M_*` means (CFG801's own disclosure), and the
   quoted `M_c(<0.31 Mpc)` scales with it.
4. **`r_sp` is A29's cluster-calibrated geometry extrapolated three decades down.** `0.83 r200m` (More+15,
   ±0.06) × 1.647 is calibrated on clusters; `r_sp` for a 10^10 `M_sun` halo is not measured, and the
   `∝ M^(1/3)` scaling is assumed. Only the ordering `r_sp ≫ r_e` is robust to the coefficient: reversing it
   at `M_b = 2.3e10` needs `r_sp` smaller by 4.5×, i.e. `0.83 r200m` wrong by a factor 4.5.
5. **`u(r)` is a projected, ΔΣ-weighted share.** No deprojection is performed here (A29's caveat 2 applies
   unchanged); the step is applied in projection as A29 fits it.
6. **The cluster-side geometry is not consistent inside the record.** A29's `r200c = 1.032 Mpc` gives
   `M200 = 1.16e14`, hence `M_b = 1.83e13` on `M200 = 6.364 M_b` and `r_sp/r_e = 1.47`; A18's cluster
   anchor `M_b = 1.4e14` with the same `r_sp` gives 0.53. This lane reports both and claims the sign only
   for galaxies.
7. **Spherical symmetry, one survey, one shear catalogue.** No miscentring, no EFE, no per-cluster `r_sp`,
   no colour/Sérsic split; the significance is record-internal, not survey-independent.

## Next

1. **Deproject the step** (`u_proj(R) → u_3D(r)`) for a two-parameter profile — the same job A29 lists as
   its top item, now with a second dataset (galaxies) that constrains the amplitude but not the feature.
2. **Add the 2-halo term** to S4 and to the catchment model, using the record's own T1x simulation: the
   +11 of S4 and the +54.6 of E(53.64) at all radii are both 2-halo-shaped, and the comparison is not
   meaningful without it.
3. **Derive `f_ret`** (CFG806's open problem). Everything in §7 and §8 rides on `f_ret = 0.10`; a
   framework-native value would turn the denominator from a fitted input into a prediction.

## Falsifier

The lane's claim is that the edge, not the step, is what the data measure. Two numbers kill it:

- **A measured `r_sp/r_e < 1` at galaxy masses.** At `M_b = 2.29e10` this lane predicts `r_sp/r_e = 4.46`
  (`r_sp = 152 kpc`, `r_e = 34 kpc`). A stacked measurement of the splashback feature at 30–60 kpc around
  `~10^10 M_sun` lenses (rather than at 150 kpc) would put the step inside the supply edge and revive it.
- **A cold mass inside 0.31 Mpc below 3 × 5.364 M_b.** The required value is `3.99–9.60 × 5.364 M_b`
  (1.2–2.8 × 10^12 `M_sun`). A factor-3 lower normalization — e.g. a `ΔΣ` calibration that removes the
  known massive/early-type excess — would let the system-denominator model back in and remove the need for
  the catchment factor.

Conversely, if `f_ret` at `10^10–10^11 M_sun` is not 0.10 but ~1, the whole resolution collapses back to
+197 and the tension is real again — that is the single input this lane cannot check.
