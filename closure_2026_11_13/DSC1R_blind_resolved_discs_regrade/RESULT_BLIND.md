# DSC1R RESULT (blind): the crossing-speed joint on resolved rotation curves at z 0.85-2.4

TEST lane, blind and independent. Criteria ad6ac2377e (committed alone, before any script or fit); script and outputs
ab30d74358; no amendment. Footings never pooled. Cold dark energy is a gravitating field component; no particle.
Blindness held: no file of the earlier lane or of the other named lanes was opened, listed, grepped or read (only the
folder names of `closure_2026_11_13/` appeared in one directory listing); no commit message was searched.

## Labels (as frozen)

| group | canonical | alt |
|---|---|---|
| ABOVE (reference halo, no law boost) | **NO POWER, FRAGILE** | **NO POWER, FRAGILE** |
| BELOW (law on the baryons) | **LAW HOLDS BELOW, FRAGILE** | **LAW HOLDS BELOW, FRAGILE** |

Known answers KA1-KA3 pass on both footings; both twins bite on both groups and footings. A HOLDS is a hit, not a pass,
and this one is relative only: every layout, the law included, is rejected in absolute terms (p ~ 1e-41).

## Membership and per-disc numbers (main run)

log threshold = log(v*(z)^4 / (G a0)); v*(0) 668.54 / 807.93 km/s. Per-disc A is the fit of that disc alone (95 %,
inflated by its own misfit). chi^2 values are corrected for correlated points (divided by c = N / N_eff).

| disc | z | log M_b | margin can / alt | group can / alt | n / N_eff | R (kpc) | g_N/a0 (out-in) | A alone [95 %] | chi^2 A=0 / A=1 / law can / law alt | R_fold (kpc) |
|---|---|---|---|---|---|---|---|---|---|---|
| COS4 01351 | 0.854 | 10.954 | -1.39 / -1.64 | below / below | 14 / 7.6 | 2.9-21.9 | 0.29-3.21 | 3.02 [2.19, 3.98] | 238.0 / 91.1 / 26.8 / 19.9 | 121 |
| D3a 6397 | 1.500 | 11.362 | -0.35 / -0.59 | below / below | 12 / 2.6 | 2.6-9.3 | 2.36-13.4 | 1.47 [-1.07, 5.23] | 11.4 / 7.2 / 6.7 / 6.8 | 120 |
| GS4 43501 | 1.613 | 10.875 | -0.73 / -0.98 | below / below | 10 / 4.2 | 2.7-14.1 | 0.55-5.13 | 1.81 [-0.15, 5.00] | 75.2 / 43.6 / 36.3 / 37.1 | 79 |
| zC 406690 (edge can) | 2.196 | 11.146 | **+0.02** / -0.23 | ABOVE / below | 12 / 2.6 | 2.9-10.0 | 1.37-6.15 | 3.18 [0.60, 7.10] | 49.3 / 24.7 / 20.6 / 18.0 | 75 |
| zC 400569 (edge alt) | 2.242 | 11.398 | +0.31 / **+0.06** | ABOVE / ABOVE | 11 / 2.1 | 2.6-8.1 | 4.95-20.3 | -2.00 (grid edge) [-2.00, 3.40] | 26.3 / 35.1 / 37.1 / 39.3 | 90 |
| D3a 15504 (edge alt) | 2.383 | 11.301 | +0.32 / **+0.07** | ABOVE / ABOVE | 12 / 4.2 | 2.5-12.9 | 1.62-8.05 | 0.84 [-0.49, 2.59] | 15.3 / 10.9 / 11.1 / 12.1 | 78 |
| zC-488879 (Lelli+23) | 1.470 | 10.890 | -0.85 / -1.09 | below / below | 10 / 5.0 | 0.9-8.6 | 1.12-8.04 | 15.87 [9.12, 25.81] | 285.2 / 218.4 / 183.1 / 171.6 | 85 |

Every point of every disc lies far inside R_fold (75-121 kpc against R_max <= 22 kpc), so the below statement is the
law at every observed radius. The reference halo (X = 5.41) has c 3.4-6.6, r_s 15-24 kpc; at the outermost point it
adds 13-60 % of the baryons' g.

## Above group: the free multiple A of the reference halo (one A per group)

| | canonical (zC 406690, zC 400569, D3a 15504) | alt (zC 400569, D3a 15504) |
|---|---|---|
| A_best [95 %] | 1.255 [-0.300, 3.365] | 0.200 [-1.350, 2.420] |
| chi^2 at A = 0 / 1 / 2 | 90.8 / 70.7 / 75.1 | 41.5 / 46.0 / 61.9 |
| chi^2_min, N_eff, s^2, p | 69.99, 8.9, 8.91, 4e-12 | 41.18, 6.3, 7.76, 1e-7 |
| excludes A = 0 / 1 / 2 | no / no / no | no / no / no |
| word | NO POWER | NO POWER |
| context (not graded): law on these discs, chi^2 | 68.8 | 51.4 |

The record's PD1 X (55.7-59.5) would be A ~ 10.3-11.0: outside the interval on both footings, and outside every
bracket's interval except I- canonical (3.3-14.4) (reported only; the brief fixes X = 5.41).

## Below group: law (L) vs baryons alone (N) vs baryons + free reference halo (H)

| | canonical (COS4, D3a 6397, GS4, zC-488879) | alt (+ zC 406690) |
|---|---|---|
| chi^2 L / N / H (A) / H at A = 1 | 252.9 / 609.7 / 206.1 (3.36) / 360.3 | 253.4 / 659.0 / 215.5 (3.34) / 385.1 |
| N_eff, s^2 | 19.3, 11.27 | 21.8, 10.34 |
| power: max(N-L, H1-L) >= 9 s^2 | 356.8 >= 101.4: yes | 405.6 >= 93.1: yes |
| preferred layout: L - min(N, H) >= 9 s^2 | 46.9 < 101.4: no | 37.9 < 93.1: no |
| p(chi^2_L) | 1.2e-42 | 2.4e-41 |
| word | LAW HOLDS BELOW | LAW HOLDS BELOW |

The law is far better than the baryons alone, but a free halo near A = 3.4 is better than the law by 47 / 38, below the
frozen 9 s^2 line only because every layout misfits (s^2 ~ 10-11). zC-488879 alone contributes 183 / 172 of the law's
chi^2: its SED stars plus CO gas (alpha_CO 1.31) are far too light for its 336 km/s curve (alone it wants A ~ 16).

## Brackets (both groups, both footings, same rule; membership recomputed where M_b changes)

Above: A_best [95 %] -> word. Below: chi^2 L - min(N, H) (s^2) -> word.

| bracket | above canonical | above alt | below canonical | below alt |
|---|---|---|---|---|
| main | 1.26 [-0.30, 3.37] NO POWER | 0.20 [-1.35, 2.42] NO POWER | +46.9 (11.3) HOLDS | +37.9 (10.3) HOLDS |
| AD0 drift off | -0.20 [-1.57, 1.74] NO POWER | -1.28 [-2.00, 0.55] **FAILS (A < 1)** | +9.0 (13.4) HOLDS | +2.6 (12.3) HOLDS |
| AD2 drift doubled | 2.85 [0.99, 5.31] **HOLDS** | 1.66 [-0.30, 4.43] NO POWER | +115.1 (9.6) **FAILS** | +119.3 (8.8) **FAILS** |
| M- (M_b -1 sigma) | 2.75 [1.43, 4.37] **FAILS (A > 1)** (zC 406690 drops out) | empty: NO POWER | +362.8 (10.6) **FAILS** | +279.6 (9.9) **FAILS** |
| M+ (M_b +1 sigma) | -1.23 [-2.00, 1.30] NO POWER | -2.00 [-2.00, 1.01] NO POWER | +7.7 (11.8) **NO POWER** | +20.7 (10.8) **NO POWER** |
| STARS (gas removed) | 2.39 [0.64, 4.73] **HOLDS** (D3a 15504 only) | empty: NO POWER | +206.6 (10.8) **FAILS** | +144.9 (10.2) **FAILS** |
| GLO (less gas) | 0.97 [-0.57, 3.05] NO POWER (2 discs) | empty: NO POWER | +125.1 (10.8) **FAILS** | +54.1 (11.0) HOLDS |
| GHI (more gas) | -0.11 [-1.62, 2.04] NO POWER | -0.11 [-1.62, 2.04] NO POWER (zC 406690 joins) | +0.5 (9.1) HOLDS | -1.4 (8.6) HOLDS |
| I- (inclination - err) | 7.75 [3.29, 14.41] **FAILS (A > 1)** | 3.72 [1.58, 6.47] **FAILS (A > 1)** | +151.1 (10.2) **FAILS** | +250.5 (15.0) **FAILS** |
| I+ (inclination + err) | -0.44 [-1.54, 1.15] NO POWER | -0.99 [-2.00, 1.28] NO POWER | +8.1 (14.5) HOLDS | -15.8 (12.6) HOLDS |
| BEAM (inner cut 0.6" / inner ring) | 1.26 [-0.10, 3.04] NO POWER | 0.39 [-0.93, 2.18] NO POWER | +70.2 (6.3) **FAILS** | +51.5 (6.1) HOLDS |
| OUT (outermost dropped) | 1.39 [-0.46, 4.00] NO POWER | 0.06 [-1.75, 2.77] NO POWER | +37.0 (13.3) HOLDS | +35.9 (11.8) HOLDS |
| ALTC (Lelli curve for zC 400569) | 1.23 [-0.37, 3.42] NO POWER | 0.12 [-1.50, 2.53] NO POWER | not applicable (= main) | not applicable (= main) |

Which assumption each label depends on most: above, the inclination (I- moves A by 6.5 / 3.5) and then the pressure
term (AD0 / AD2 swing A over -1.3 to +2.9); below, the baryon mass (M- moves L - min(N, H) by 316 / 242), then
stars-alone, inclination and pressure. The same assumptions push the two groups the same way: anything that makes the
discs need more mass (more drift support, lower inclination, lighter baryons) turns the above group toward A > 1 and the
below group to LAW FAILS BELOW, because the free halo then beats the law; anything that makes them need less mass
(no drift, higher inclination, heavier baryons) turns the above group toward A <= 1 and the below group to NO POWER or
a narrow HOLDS.

## Known answers and twins

- KA1 (SI): v*(0) 668.54 / 807.93 km/s, log threshold at z 2 11.279 / 11.526; halo cold mass at r_ta = X M_b to
  1e-10; r200m in SI 74.92 vs script 74.94 kpc (M_b 2e11, z 2.3); law identity 4e-16. PASS.
  Reported: CO gas masses reproduce CFG278 (zC-488879 7.79e9 / 8.38e10 at alpha 0.4 / 4.3; zC-400569 9.35e9 at 0.4).
- KA2 (noise-free A = 1 data on the real radii and errors): A_best 1.000, JOINT'S STATEMENT HOLDS, both footings. PASS.
- KA3 (noise-free law data): chi^2_L = 0, LAW HOLDS BELOW, both footings. PASS.
- TW-V (all V x 1.25): above A 4.96 / 3.54 (FAILS), below L - min 409 / 422 (FAILS): bites everywhere.
- TW-M (baryon mass halved, halo rebuilt): above A 5.16 / 4.09 (FAILS), below 489 / 504 (FAILS): bites everywhere.

## What was left out or is weak

- Genzel+17 inclination and mass errors are not in the on-disk Table 1 transcription: +-10 deg (CFG405's choice;
  +-12 for zC 406690 as CFG402) and 0.20 dex on M_b are declared assumptions.
- Genzel's kpc/" (their cosmology) is kept for their curves; Lelli's curves use the brief's cosmology (8.68 / 8.45).
- The correlated-point correction (N_eff from one beam per 0.6" per side; two rings per beam for Lelli) is a frozen
  approximation; no covariance from the cubes exists on disk.
- No resolved high-z curve beyond these seven discs was used; RC100 (one point per disc) has no shape. The above group
  has only three (canonical) / two (alt) discs, all with 2-4 effective beams each.
- Baryons are fixed per bracket; no joint fit of mass, inclination and A was made (frozen choice).
- A HOLDS here does not test the law in an absolute sense: no layout fits the curves (chi^2 / N_eff ~ 8-13).

## What the result says

On the six Genzel+2017 deep curves and Lelli+2023's zC-488879, the joint's above statement cannot be tested: the
two or three massive z > 2 discs that sit above the crossing speed allow the reference halo at zero, one or two times its
mass, and their curves are not fitted well by any layout, so the misfit-inflated interval of A covers everything
from -0.3 (-1.35 alt) to 3.4 (2.4 alt). The below statement scores a hit, but a weak and relative one: the law beats the
baryons alone by a wide margin, a free halo of about 3.4 times the reference beats the law by 38-47 in chi^2 without
reaching the frozen 9 s^2 line, and every layout is rejected in absolute terms, mostly because zC-488879's photometric
baryons are too light for its curve. Both words are fragile, and they flip together on the same data-side
assumptions: drift support, inclination and baryon mass. Six (canonical) / four (alt) of the twelve brackets turn the
below word into LAW FAILS BELOW, and four (canonical) / two (alt) turn the above word into FAILS or HOLDS. These curves do not decide the joint either way, and
nothing here is a pass of the theory.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
