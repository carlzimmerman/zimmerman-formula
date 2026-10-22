# A47 — the `f_ret = 0.10` factor: ten times the cosmic share, or ten times the baryons?

Lane A47. Script `a47_checks.py`, output `a47.out`, numbers `a47_results.json`, mutations `MUTATE.md`.
Footing `a0 = 9.3603e-11 m/s²` (canonical); the alt footing appears only where A44's own number is quoted
for it, never pooled. Sources read from disk: CFG416 `FROZEN_CRITERIA.md`, CFG804 and CFG801 `README.md`,
`A18_two_ratios`, `A29_u_radial`, `A43_cold_eos`, `A44_no_edge` results.

## Claim

**The factor 10 is a baryon deficit, not a cold overdensity, and the record's two `f_ret`s are different
objects with different symbols.** CFG416 defines one `f_ret` — the fraction of a catchment's cosmic
baryons that end up as the galaxy's gas + stars, `f_ret^b ≡ M_b/(f_b M_ta) ≤ 0.90`. `N = R_cosmic/f_ret^b`
is *derived* from it, not a second retention fraction; and because `M_b = f_ret^b f_b M_ta`, the cold mass
`5.364 M_b/f_ret^b` is **identically** the cosmic dark share of the catchment, `(1−f_b) M_ta`
(K3: sympy 1, numeric residual 2e-16). At `f_ret^b = 0.10`, A44's 53.64 `M_b` is exactly **1.000 ×** the
catchment's cold share: **saturation** of the availability ceiling, not a violation of it.

**A43's `f_ret` is a third normalization, and its ceiling is the denominator the lensing excludes.**
A43 computes `f_ret = M_c,rest/(R_cosmic M_b)` — the EOS reading's cold rest mass in units of the
*system's own* cosmic share — and gets `2.195 ± 0.34`. That is a real 3.5σ exceedance of 1, but 1 in that
normalization means `N = 5.364`: the *system* denominator, which the same KiDS data exclude at
Δχ² = +197 (CFG801, reproduced by A44 K3). Written against the catchment's share — the physical ceiling —
the same requirement is `f_c = f_s·f_ret^b = 0.219`, **4.6× below** the ceiling. So A43's `f_ret = 2.195`
is not evidence against the catchment budget; it is a second, independent measurement that the budget is
larger than the system's share, and it is comfortably inside the catchment's. **No contradiction
survives** — but A43's Task-4 claim that "`f_ret ≤ 1` excludes the EOS reading at 3.6σ" does not survive
either: its physics no-go (the tether is 2.35×10⁴ too weak) stands, its baryon-budget argument does not.

**No phase-space or availability obstruction.** For `M_b = 1e11` the model needs `5.364e12 M_sun` inside
`r_e = 0.661 Mpc`. The z = 0 cosmic cold density (`3.347e10 M_sun/Mpc³`) supplies **18.0%** of that
inside the catchment radius (1.90 Mpc) and 13.5% inside the zero-velocity sphere (1.73 Mpc); the
remaining 82% is the catchment's own 5.55× turnaround overdensity — the same assumption that makes any
halo exist, since the cold sector is 84% of the matter. Escape velocity (`v_esc = 267 km/s` against
`v_H = 45`; the ambient 300 km/s capacity `v²r/G` is 2.6× the budget), the tidal field (an equal-mass
neighbour must sit beyond 0.95 Mpc, a 10× neighbour beyond 2.05 Mpc) and phase space (the coarse-grained
density implies a Tremaine–Gunn floor of 37 eV; the sector's own `σ_c` could bind only 0.2% of `M_tot`)
all fail to cap it. The cold medium at `r_e` is 133× the cosmic cold density and 5.5×10³× at 0.1 Mpc —
"ten times the cosmic share" is not a density at any radius.

**The decisive number: `N_avail/N_req = 2.38`** (2.77 at `1e11`, 1.91 on the alt footing). CFG416's table
is not constant: solved at the four KiDS masses its fixed point gives `N = 53.6, 53.6, 50.3, 37.9 M_b`
and 44.1 at `1e11`, against the `N_req = 15.94` the data require at Δχ² ≤ 4. Availability therefore never
caps below the requirement, and the available budget fits *better* than 53.64 (Δχ² = −0.4 vs +1.1). The
no-edge tension does not return on the primary range, and no error in CFG801's covariance is needed.
What the cap does explain is the outer range: the edge sits at `1.39–1.64 r200c = 0.31–0.37 r_ta`, so a
single halo runs out of cold supply at 0.3–0.6 Mpc while the lensing continues to 2.6 Mpc — the
+55 to +150 all-radii residual is a two-halo problem, exactly as CFG804 states.

## Derivation

Units `c = 1`; `G = 4.30091e-9 Mpc (km/s)²/M_sun`; `a0 = 9.3603e-11 m/s²`; `ρ_crit = 1.2607e11 M_sun/Mpc³`
(h = 0.674); `Ω_m = 0.315`; `f_b = ω_b/ω_m = 0.157126`; `R_cosmic = (1−f_b)/f_b = 5.364327`;
`Δ_ta = (3π/4)² = 5.5517`; `σ_c = 8.33 km/s` (THEORY §3.3, as used by A43 K9). Cosmic cold density
`ρ̄_cold = (1−f_b) Ω_m ρ_crit = 3.3472e10 M_sun/Mpc³`.

**1. The two objects (task 1).** CFG416's `FROZEN_CRITERIA.md` states, verbatim on disk,

    x_h·r_ON = r_edge = (5.364/f_ret) · r_M(M_b,now),   M_b,now = f_ret · f_b · M_ta,
    M_ta = (4π/3) r_ON³ Δ_ta(a) ρ̄_m,                    r_M = √(G M_b,now/a0),
    f_ret (gas + stars fraction relative to cosmic): 0.10 below 10^12.5 M_sun/h; log-linear to 0.55 at
    10^13.5 and 0.85 at 10^14.5; capped at 0.90.                                            (1)

`f_ret` is therefore a **retention efficiency**: of the `f_b M_ta` baryons in the catchment, the fraction
that is still gas + stars in the galaxy. It is dimensionless, in (0, 0.90], and the ceiling 1 is
definitional (K1, K2). Everything else follows algebraically:

    N ≡ R_cosmic/f_ret^b = M_c/M_b,        M_c = R_cosmic f_b M_ta = (1−f_b) M_ta.            (2)

So the "factor 10" is `1/f_ret^b = M_ta/M_b`: **the catchment holds ten times the galaxy's baryons**, and
the cold mass is the cosmic share of *that* reservoir. A18 §7's `N = 53.643, 44.125, 14.917, 8.296,
5.960` are this `N` at five `M_ta`; A18's `u = R_tot/N` is the *law phantom's* share of that budget, so
`u ≤ 1` is automatic and never constrained `f_ret` (K16: `R_tot/N = 0.4668` against A29's `u_MID =
0.4716 ± 0.0361`, 0.13σ — numerically the same, functionally different: a 3D budget fraction against a
ΔΣ-weighted band ratio).

A43's number uses a third denominator. Define its own normalization explicitly,

    f_s ≡ M_c,rest/(R_cosmic M_b) = N/R_cosmic,      f_c ≡ M_c/(R_cosmic f_b M_ta) = f_s · f_ret^b,   (3)

so `f_s ≤ 1` is the statement `N ≤ 5.364` — the **system** denominator — while `f_c ≤ 1` is the physical
availability statement (no more cold mass than the catchment contains). A44's model has
`f_s = 10.00`, `f_c = 1.000`; A43's EOS reading has `f_s = 2.195 ± 0.34`, `f_c = 0.219`; the record's
excluded system model has `f_s = 1.000`, `f_c = 0.100` (K4):

| model | `M_c/M_b` | `f_ret^b` | `f_s` (A43's units) | `f_c` (catchment units) | reading |
|---|---|---|---|---|---|
| system cosmic share (CFG801's excluded model) | 5.364 | 1.00 | 1.000 | 0.100 | 10% of the catchment's cold share |
| **A44's catchment model** | 53.64 | 0.10 | **10.00** | **1.000** | the whole catchment share — saturation |
| **A43's EOS reading of `u = 0.4716`** | 11.77 | 0.10 | **2.195 ± 0.34** | **0.219** | 4.6× inside the ceiling |

`f_s = 2.195` is `(1/0.4716) × (R_req/R_cosmic) = 2.120 × 1.035`; A43's `±0.34` gives 3.5σ above 1 (my
recomputation from the quoted `σ_u`, `σ_R` gives ±0.24, i.e. 4.9σ, so A43's bar is the conservative one).
The 3.5σ is **against the system denominator**, and that is the one thing the KiDS data rule out at
Δχ² = +197. Against the catchment the same number is 0.22 — so the EOS reading is not budget-limited at
all, and A43's exclusion of it must rest on its microphysics (§7 of that lane), which is unaffected.

**2. What "ten times" is not (task 2).** With `M_b = 1e11`: `r_M = 12.20 kpc`, `r_e = 54.14 r_M =
0.661 Mpc`, `M_c = 5.364e12`, `M_tot = M_b + M_c = 5.464e12`, `r200c = 0.373 Mpc`. The cold overdensity
inside `r_e` is

    1 + δ_cold(r_e) = M_c/(ρ̄_cold V(r_e)) = 133,      1 + δ_cold(0.1 Mpc) = 5.5e3,       (4)

and `r200` is 200 by construction (K7). Ten is nowhere in that list: it is `M_ta/M_b`, a ratio of baryon
reservoirs. Taking the brief's premise literally — a ceiling of `10 ρ̄_cold V(r_e)` — would allow
0.40 `M_b` (4.0e10 M_sun) of cold mass, i.e. **0.76%** of what the data need; that reading is refuted by
a factor 133, and the `density` mutation is built to show it (MUTATE.md).

**3. Availability, computed three ways (task 2).**

*(i) The cosmic share as an upper bound.* `M_ta = M_b/(f_ret f_b) = 63.64 M_b = 6.364e12 M_sun` at
`f_ret = 0.10`, and the catchment radius at `Δ_ta` is `r_ta = 1.903 Mpc`. The cold mass at the present
mean density inside that sphere is `ρ̄_cold V(r_ta) = 0.180 × M_c` — and generally `1/Δ_ta` exactly,
independent of `f_b`:

    M_c/(ρ̄_cold V_ta) = Δ_ta = 5.55,   i.e. 18.0% of the budget is there at the mean density.        (5)

Inside the zero-velocity sphere `r_ZV = (G M_tot/H0²)^{1/3} = 1.730 Mpc` it is 13.5%. To hold the whole
`M_c` at the mean density one would need `r = 3.37 Mpc = 1.95 r_ZV` — i.e. the budget **cannot** be
assembled from the mean-density field inside the bound sphere. The missing 82% is the catchment's
turnaround overdensity, which is not a new assumption: it is the statement that the cold sector is 84%
of the matter and has been falling in since turnaround. Availability is therefore conditional on the
framework's starting point (cold traces matter), not on any extra cold mass.

*(ii) Escape velocity.* At `r_e`: `v_c = 189 km/s`, `v_esc = 267 km/s`, `v_H = H0 r_e = 45 km/s`, so the
material is bound by 6× in velocity, and `v_esc/σ_c = 32` for the sector's own 8.33 km/s. The
gravitational capacity at the edge for an ambient 300 km/s infall is `v²r/G = 1.38e13 = 2.6 M_c` (K9).
This bound does not bite.

*(iii) Tidal field.* `r_t = d (M/(3M_env))^{1/3}`, so for `r_t ≥ r_e` an equal-mass neighbour must sit
beyond `r_e·3^{1/3} = 0.95 Mpc`, and a 10× neighbour beyond `2.05 Mpc` (K10). For the self-consistent
budget (N = 37.9, `r_e = 0.47 Mpc`) the equal-mass requirement drops to 0.68 Mpc. The 53.64 model is
therefore viable for a genuinely isolated lens, but it *requires* isolation at the ~1 Mpc scale; B21's
own isolation criterion is not in the on-disk README, so this is a requirement, not a verified fact.

*Phase space.* At `r_e`, `ρ = 3.01e-28 g/cm³` and `ρ/σ_c³ = 5.2e-46 g cm⁻⁶ s³`, which for `g = 2` implies
a Tremaine–Gunn floor `m ≥ 37 eV` (K11) — the standard warm floor, no new obstruction, and no constraint
at all if the sector is a field rather than a particle. The relevant statement is not a mass ceiling but
a support one: `σ_c² r_e/G = 1.07e10 M_sun` is 0.2% of `M_tot`, so the halo is bound by its total mass,
not by the cold sector's dispersion. There is no phase-space reason the halo cannot hold 53.64 `M_b`;
there is only the baryon-budget reason, and that one is satisfied.

**4. The decisive number (task 3).** CFG416's table is evaluated at `M_ta` and `M_ta` depends on
`f_ret`, so the budget is a fixed point, `M_ta = M_b h/(f_ret(M_ta) f_b)`. Solving it (K12; reproduces
A18's 44.125 at `1e11` and 14.917 at `1e12`; the root is unique, one sign change on `f ∈ [0.02, 0.97]`):

| bin | `log M_b` | `f_ret^b` | `log M_ta` [M_sun/h] | `N` | `M_c` [`M_b`] | `r_e` [kpc] | `r_e` at 53.64 | `r_e/r200c` | `r_e/r_ta` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 10.36 | 0.100 | 11.99 | **53.64** | 53.64 | 316 | 316 | 1.39 | 0.31 |
| 2 | 10.78 | 0.100 | 12.41 | **53.64** | 53.64 | 513 | 513 | 1.63 | 0.36 |
| 3 | 10.91 | 0.107 | 12.51 | **50.32** | 50.32 | 559 | 596 | 1.64 | 0.37 |
| 4 | 11.11 | 0.141 | 12.59 | **37.94** | 37.94 | 532 | 750 | 1.47 | 0.33 |

`f_ret^b = 0.10` is the table's value only while `M_ta ≤ 10^12.5 M_sun/h`, i.e. `M_b ≤ 7.37e10`
(K15). The two low-mass bins are on that branch exactly; at `1e11` the self-consistent value is
`f_ret^b = 0.1215`, `N = 44.15`; at the top KiDS bin it is `f_ret^b = 0.141`, `N = 37.94`. **53.64 `M_b` is
available for bins 1–2, 82% of it at `1e11`, 71% at bin 4.** A44's constant is the low-mass branch applied
one bin too far.

Against what the data need: `N_req = 15.94` (A44's scan, Δχ² ≤ 4; `19.85` on the alt footing). The
smallest available budget is 37.9, so

    N_avail/N_req = 37.94/15.94 = 2.38  (canonical),   44.15/15.94 = 2.77 at 1e11,
    = 37.94/19.85 = 1.91 (alt).                                                              (6)

Availability **does not** cap the cold mass below the requirement in any bin, on either footing. The
Δχ² confirms it: interpolating A44's common-`N` scan, `Δχ²(44.1) = −0.4`, `Δχ²(53.64) = +1.1`,
`Δχ²(15.9) = +4.0`; the per-bin census model (CFG804's `N = 10.0, 8.95, 7.35, 5.68`, i.e. cold masses
53.6, 48.0, 39.4, 30.5 `M_b`) gives −0.25. **The available budget fits slightly better than A44's
headline number.** No covariance error in CFG801 is required, and the no-edge tension does not return.

**5. Where the cap does bite.** The edge is at `1.39–1.64 r200c` and `0.31–0.37 r_ta` (K17): inside the
catchment, so no cold mass is demanded from outside the supply region, but **outside the virial radius**,
in the infall zone. That is exactly where the model runs out: `r_e = 0.32–0.56 Mpc` against data to
2.6 Mpc, and the all-radii Δχ² stays at +55 (E_catch) to +150 (CFG804). The geometric cap is far larger
(`N ≤ 155` before the edge reaches `r_ta`), so the binding constraint is the baryon budget, not the
volume; and the outer residual is a two-halo term, not a cold-budget deficit. This is CFG804's own
conclusion, now with the number that makes it quantitative: the single halo is exhausted at 0.3–0.6 Mpc
by construction, not by a failure of the law.

## Status

- **Task 1 — DERIVED (two symbols, three normalizations).** CFG416's `f_ret^b` is a retained baryon
  fraction, range (0, 0.90]; `N = R_cosmic/f_ret^b` is derived and the cold mass is exactly `(1−f_b) M_ta`
  (K3). A43's `f_ret` is `f_s = N/R_cosmic`, whose ceiling 1 is the system denominator; in catchment units
  it is `f_c = f_s f_ret^b`. A44's model: `f_s = 10.0`, `f_c = 1.000`; A43's reading: `f_s = 2.195 ± 0.34`,
  `f_c = 0.219`. **Same symbol, different objects; no contradiction — and A43's 3.5σ is against a
  denominator the lensing excludes.**
- **Task 2 — NUMERICAL (available, conditionally).** 18.0% of the budget at the cosmic mean density
  inside `r_ta` (13.5% inside `r_ZV`); the rest is the 5.55× turnaround overdensity. `v_esc/v_H = 6`,
  ambient capacity 2.6× the budget, tidal isolation 0.95 Mpc (1:1) / 2.05 Mpc (10:1), Tremaine–Gunn floor
  37 eV, `σ_c²r_e/G = 0.2%` of `M_tot`. The phase-space density required is a halo, not an impossibility.
- **Task 3 — DECIDABLE, and decided: not capped.** `N_avail = 53.6, 53.6, 50.3, 37.9`; `N_req = 15.9`;
  ratio 2.38 (2.77 at `1e11`, 1.91 alt). `Δχ²(44.1) = −0.4` ≤ `Δχ²(53.64) = +1.1`. The tension returns
  only in the outer range, as a two-halo residual.
- **Task 4 — verdict.** The factor 10 is `1/f_ret^b`, a baryon-reservoir ratio; the cold sector holds
  **1.000×** the cosmic share of its catchment, i.e. 10× the cosmic share *of the galaxy's own baryons*.
  A44's 53.64 is right at the low-mass end, 1.2–1.4× too large at `1e11`–`1.3e11`, and irrelevant to the
  verdict because the data need only 36% of the smallest available budget.

## Checks

`a47_checks.py` — 18 checks, deterministic, stdlib only (sympy used if present), 0.12 s, no network,
exit 0 iff all pass; three mutations each break a group, all exit 1 (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | CFG416 defines `f_ret` as a retained baryon fraction, all six definitional strings on disk | 6/6; 0.10 / 0.55 / 0.85 / 0.90 | all present |
| K2 | the table is monotone and capped at 0.90 | 0.10, 0.10, 0.33, 0.55, 0.70, 0.85, 0.90, 0.90 | monotone, cap |
| K3 | `f_c = M_c/(R_cosmic f_b M_ta) = 1` identically | sympy `1`; residual 2e-16 | < 1e-12 |
| K4 | three normalizations: `f_s` = 1.000 / 10.00 / 2.195, `f_c` = 0.100 / 1.000 / 0.219 | 3.5σ above the *system* ceiling | exact, > 3σ |
| K5 | CFG804's `N = 1/f_ret` vs A44's `N = 5.364/f_ret` is one model, factor 5.364 | 10.0 → 53.6 `M_b`; 53.64 | < 1e-9 |
| K6 | A44's numbers reproduce; CFG804's per-bin edges reproduce | 53.643, 54.141, 316–750 kpc; 324/454/439/429 | ±5e-3, ±12 kpc |
| K7 | the factor 10 is not a density | 1+δ_cold = 133 at `r_e`, 5.5e3 at 0.1 Mpc; `r200` = 200 | 100–200, > 1e3 |
| K8 | mean-density availability inside `r_ta` / `r_ZV`; `r_needed` | 0.180 / 0.135; 3.37 Mpc = 1.95 `r_ZV` | 0.15–0.20, 1.8–2.1 |
| K9 | escape velocity does not cap | `v_esc` 267, `v_H` 45, capacity 2.6× | > 2 |
| K10 | tidal isolation required | 0.95 / 0.68 / 2.05 Mpc | 0.85–1.05, 1.9–2.2 |
| K11 | phase space: TG floor; `σ_c` cannot bind | 37 eV; 0.20% of `M_tot` | 25–50 eV, < 0.5% |
| K12 | the fixed point exists, is unique, reproduces A18 | 44.15 vs 44.125; 14.921 vs 14.917; 1 sign change | ±0.2, =1 |
| K13 | `N_avail > N_req` | min 37.9/15.9 = 2.38 | > 1 |
| K14 | Δχ² at the available budget | −0.4 (44.1), +1.1 (53.64), +4.0 (15.9), −0.25 (per bin) | < 2, ≤ 4.5 |
| K15 | the factor 10 is the low-mass branch | `M_b,lim = 7.37e10`; 53.64/37.9 = 1.41 | 6e10–9e10, > 1.3 |
| K16 | `u` ledger: same number, different functional | 0.4668 vs 0.4716 ± 0.0361 (0.13σ) | < 1σ |
| K17 | the edge is inside the catchment | 1.39–1.64 `r200c`, 0.31–0.37 `r_ta`; `N_geom` = 155 | < 2, < 0.5, > 100 |
| K18 | alt footing not pooled; verdict footing-independent | 37.9/19.85 = 1.91; `r_e` × 0.910 | > 1.5 |

## What this does not do

1. **It does not derive `f_ret`.** The table is an observational input carried in the record (CFG804's
   own caveat); this lane only shows what it *means* and what it implies. A framework-native `f_ret`
   (CFG806's failed attempt) would turn the denominator into a prediction.
2. **It corrects A43's baryon-budget argument, not its physics.** A43's Task 4 has two legs: the tether
   is 2.35×10⁴ too weak (untouched here) and `f_ret ≤ 1` (denominator-dependent, and its 1 is the system
   denominator). Anyone re-using A43's "3.6σ" should re-read it as "2.2× the system's cosmic share", which
   is a *confirmation* of the catchment denominator rather than a violation of the ceiling.
3. **The `M_ta` convention matters and is inconsistent across lanes.** CFG416's table is in `M_sun/h`;
   A44's solver omits the `h` when evaluating it, A18's includes it. That 0.17 dex moves `f_ret` and
   therefore `N` (A44's 53.64 at `1e11` vs 44.15 with `h`). This lane uses CFG416's convention (with `h`)
   and reproduces A18; A44's numbers are quoted as A44 computes them. Nothing in the verdict depends on
   the choice — both are above `N_req`.
4. **`M_b` is profiled, so the amplitude is not measured.** A44's own §3 shows the cold amplitude is
   exactly degenerate with `M_b` at fixed edge; the fit measures `r_e`, not 53.64 `M_b`. This lane's
   "available" statement is about the budget, not about a measurement of the cold mass.
5. **The mean-density fraction is not an independent measurement.** `1/Δ_ta` follows from the definition
   of the catchment; the physical content is the assumption that the cold sector traces the matter at
   `1−f_b` of it. If the cold sector were segregated from the baryons before turnaround, the availability
   argument would change — nothing in the record tests that.
6. **The tidal requirement is not checked against B21's selection.** The isolation radius needed
   (0.95 Mpc for a 1:1 neighbour) is a requirement on the sample; the on-disk README does not state the
   criterion, and I did not fetch the paper.
7. **The phase-space floor assumes `σ = σ_c = 8.33 km/s` and `g = 2`.** A warmer medium lowers the
   Tremaine–Gunn floor; a field has no floor at all. The number is illustrative of "no obstruction", not
   a particle-physics claim.
8. **The 2-halo term is not modelled.** Every statement about the outer range is CFG804's, restated. The
   +55 to +150 all-radii residuals are not repaired here.
9. **`Δ_ta = 5.5517` is the EdS turnaround value at z = 0.** With Λ the turnaround overdensity is lower
   (~4.3); `r_ta` would grow by 9% and the mean-density fraction would fall to 0.23. No conclusion moves.

## Next

1. **Evaluate `f_ret` with the `h` convention fixed in A44's own solver** and re-report the census model:
   the difference (53.64 → 44.15 at `1e11`) is larger than the Δχ² separation between the competing
   models (+1.1 vs −0.4), so the record should not quote both conventions.
2. **Replace the constant with the per-bin budget** in the CFG804/CFG801 chain. This is a one-line change
   with a better fit (−0.25 vs +1.1) and it removes the only number in the resolution that is not
   self-consistent.
3. **Restate A43's Task 4** in catchment units (`f_c = 0.219`) so that the record does not carry two
   incompatible ceilings under one symbol.
4. **Two-halo term for the 0.4–2.6 Mpc range**, now with a hard upper bound on the single-halo
   contribution: the catchment is exhausted at 0.32–0.56 Mpc, so everything beyond is neighbours.
5. **Measure `f_ret^b` directly** — a baryon census (stars + gas + CGM) in the same KiDS bins would test
   the 0.10–0.14 assumption that carries the whole denominator.

## Falsifier

The lane's claim is that the factor 10 is a baryon deficit and that the available budget exceeds the
data's requirement. Two numbers kill it:

- **A measured `f_ret^b > 0.337` at `M_b = 1e10–1e11`** (i.e. galaxies retaining more than a third of
  their catchment's cosmic baryons). Then `N < 15.9`, the budget drops below `N_req`, and the no-edge
  tension returns at Δχ² > 4 — with no cold-sector fix left except a different profile or a covariance
  error. The observed "missing baryons" put `f_ret^b` at 0.1–0.3, so the margin is a factor 2.4, not a
  factor 10.
- **A stacked measurement of the cold mass inside 0.3 Mpc below `4 × 5.364 M_b`** (1.2e12 `M_sun` at
  `1e11`). The available budget is 44 `M_b`; the requirement is 16; a factor-3 lower normalization would
  make the *available* budget the excluded one and re-open the denominator question.
