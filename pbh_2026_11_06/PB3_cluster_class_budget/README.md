# PB3: uniform-born PBHs as the cluster / class extra mass. SPLIT: PARTIAL (canonical) / FAILS (alt). Coma UDGs FAIL everywhere; the Bullet FAILS

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings graded separately, never pooled.
**PBHs are not a particle, but their mass is a component that has to be paid for.** The amounts below are
Omega_PBH ~ 0.02-0.17, i.e. 0.5 to 4 times the baryons: a cold collisionless mass component by another name. The cold
sector stays RETIRED (11-01) and nothing here reinstates it.

- Criteria: `FROZEN_CRITERIA.md` (05d916ef99), committed alone before any script or number.
- Script: `pb3.py` (main), `pb3.py --mutate`, `pb3.py --bullet`. GB1's battery, KD1, DX1, SE2 and DB1 are used
  read-only. DB1's Bullet code is exec'd from its source with its output handle swapped for a StringIO, so nothing in
  DB1's folder is written.
- Outputs: `pb3.json` / `pb3.out`, `pb3_MUTATE.json` / `.out`, `pb3_bullet.json` / `.out`.
- Runs on one thread in about 25 s per mode. A rerun of main gives a byte-identical `pb3.json`.

## Models
- **U, no segregation.** b = 1 + F at every point, KD1's uniform convention.
- **I, collisionless vs dissipative infall (primary).** The PBHs stay in an isothermal spheroid out to r_vir, set by
  (1+F) M_b at 200 rho_c0 with h = 0.70 (a convention). The baryons sit where they are observed.
- **Brackets.** r_vir x 0.5, r_vir x 2, and a Hernquist profile with c = 10.
- **Grading.** A class is reproduced when the PBH shift lands inside SE2's 95 % posterior interval. SPARC is graded on
  GB1 G1.

## Verdict (model I primary)

| Class | canonical | alt | at F* (X-COP on SE2's median): shift vs SE2 95 % |
|---|---|---|---|
| SPARC discs (G1) | **FAILS** | **FAILS** | rms 0.148 / 0.157 vs line ~0.146 / 0.143 (Z -0.056 / -0.076) |
| X-COP | REPRODUCED | REPRODUCED | +0.440 / +0.408 (anchor) |
| groups (f* 0, 1) | REPRODUCED | REPRODUCED | +0.31, +0.29 / +0.28, +0.27 |
| ellipticals | REPRODUCED | REPRODUCED | +0.057 / +0.051 |
| KiDS early-late | REPRODUCED | REPRODUCED | +0.004 / +0.003 (no power: SE2's interval is wide) |
| bright M31 | REPRODUCED | REPRODUCED | -0.008 / -0.007 |
| **Coma UDGs** | **FAILS** | **FAILS** | +0.13 / +0.12 against a needed >= +0.54 / +0.47 |

**Overall: SPLIT (PARTIAL / FAILS).**
- Canonical: SPARC and X-COP share F 1.26-1.41 (grid), which makes it PARTIAL.
  - Inside that window, ellipticals, KiDS, groups and bright M31 also pass. This was checked post-freeze and is
    reported only.
  - Only the UDGs fail there.
- Alt: SPARC allows F <= 0.77, but X-COP needs 1.12-1.78, which makes it FAILS.
- **The split is the same under all four I variants.**
  - Canonical windows: [0.56, 0.63] at s = 0.5, [3.16, 3.55] at s = 2, [0.50, 0.56] for Hernquist.
  - Alt: empty in every variant.
- **Model U (no segregation): FAILS on both footings.** SPARC allows <= 0.33 / 0.19; X-COP needs 3.75 / 3.38 after
  SE2 (raw 4.18 / 3.78).

## (1) Mass budget
- **X-COP under U needs F = 3.75 / 3.38.**
  - That is f = 0.79 / 0.77 of baryons plus PBHs.
  - It gives Omega_PBH = 0.17 / 0.15 at Omega_b 0.0442 (BBN, PROVISIONAL).
  - M_PBH / M_gas = 4.15 / 3.74, against DB1's 4.4-5.4. DB1 zeroed the raw residual; PB3 subtracts SE2's
    systematics.
- **Under I the same clusters need F about 1.7 / 1.5** (Omega_PBH about 0.075 / 0.066). The PBH spheroid sits more
  centrally than the gas inside r_vir.
- **Spread needed, in U-equivalent units per X-COP:**

  | Class | Factor needed |
  |---|---|
  | SPARC | <= 0.087 / 0.057 |
  | ellipticals | 0.06 / 0.05 |
  | groups | 0.42-0.45 / 0.37-0.38 |
  | X-COP | 1 |
  | Coma UDGs | 23 |

  **UDG / SPARC: 265x / 398x.** A uniform-born population gives 1 for every class.

## (2) Segregation processes
- **S1 dynamical friction and S2 relaxation (Newtonian, t_H 13.8 Gyr). They do not make the spread.**
  - In discs, ellipticals, groups and clusters, at M <= 1e6 Msun, the fraction that sinks is <= 2 % and the fraction
    that evaporates is <= 10 %.
  - Where they do act (dSphs at M >= 1e3-1e4, UDGs at M >= 1e5), they remove PBHs. That is the wrong sign for the
    UDGs, which need more.
  - In dSphs at >= 1e4 there are fewer than 100 PBHs inside r_h. At 1e6-1e7 the stars are heated within 11-2 Gyr.
- **S3/S4, the collisionless spheroid, is the only process that delivers a spread.**
  - Delivered factors (units of F, at the class points): SPARC 0.18, ellipticals 0.10, bright M31 0.24, MW classical
    0.15, UDG 0.45, groups 1.3, X-COP 2.0.
  - The ordering is right for ellipticals, groups and dSphs.
  - X-COP / SPARC reaches about 11, against about 11.5 needed on canonical and about 17.5 on alt.
- **S4b, baryon expulsion needed at F*.**
  - UDGs would need eps = 0.991: 99 % of their original baryons lost while every PBH is kept.
  - On alt, SPARC needs eps = -0.43, meaning PBHs would have to be removed from discs.
- **Disc heating (Lacey-Ostriker form, MW at 8 kpc, rho_PBH 1.1e-3 Msun/pc^3):** sigma passes 40 km/s at
  M >= 4.9e6 Msun.

## (3) Bullet: FAILS on both footings
I used DB1's own map, with the PBHs on the galaxies and R_j = F*(M_gas + M_st) / M_st at U's F*.
- The masses are fine: M300 is 4.07 / 1.89 e14 (Z +1.08 / -1.19) on canonical and 3.99 / 1.90 e14 on alt.
- The bullet subcluster's lens peak stays nearer its gas: d_gal 104 kpc against d_gas 54 kpc. Its dkappa is only
  +0.014 / +0.003.
- The cause is that an amount proportional to the initial baryons is in effect gas-proportional in the gas-rich
  bullet (gas/stars 5.8). This is DB1 P1G / P3's failure again.
- KA4 (R = 0 gives DB1's K1) passes.

## (4) Millilensing (order of magnitude; a prediction, not graded; outside bounds belong to PB2)
- **Count.** Per X-COP cluster, M_PBH is about 6e13 Msun inside about 400 kpc. That is N = 6e11 PBHs at 1e2 Msun and
  6e6 at 1e7.
- **Share and image scale.** PBHs carry 0.46 / 0.42 of the law's lensing mass. Each has theta_E from 28 uas (1e2) to
  9 mas (1e7), so the astrometric jitter is about 0.7 theta_E.
- **What it predicts.** With kappa_PBH about 0.4:
  - every cluster-lensed compact source should be broken into milli-images;
  - its flux ratios should be perturbed at order unity;
  - its macro-caustics should be corrugated.
- **Reading.** This is likely in strong tension with long-lived caustic-transient stars and with VLBI of
  cluster-lensed sources (PROVISIONAL, from memory). It is flagged and not computed.

## What it needs, plainly
- **Amount.** F about 1.3-1.4 times the baryons (canonical, model I), with mass M about 1e2 to about 5e6 Msun. That
  is Omega_PBH about 0.06, or 0.2-0.6 of all matter in black holes.
- **Bounds.** Standard bounds in this mass range (CMB accretion, Poisson isocurvature / Ly-alpha, dynamical, X-ray /
  radio) are about f_DM <= 1e-3 to 1e-2. The need is **likely 1-2 orders of magnitude or more above them.** This is
  for PB2 to grade with framework-native modifications.
- **Formation.** No formation channel is in hand.

## Checks
- **KA1 PASS:**
  - DB1 M_cb / M_gas: P1G 4.82 / 4.36 and P3 5.44 / 4.82, i.e. 4.4-5.4.
  - GB1 L0 class means vs KA20: 4.3e-7 / 4.5e-7.
- **KA2 PASS:** model U re-derives every KD1 need and SPARC_f_max to 0 relative.
- **KA3 PASS:** the SE2 table matches to 0 at 3 dp.
- **KA4 PASS:** Bullet at R = 0 gives M300 1.112e14 and 7.337e13, dkappa -0.068 and -0.111.
- **MUTATE:**
  - M1: planted perfect segregation reproduces DX1 O1 to 0, with equal statuses, on both footings. It **HOLDS**.
  - M2: F = 0 gives GB1 L0 to 0 in all five models. It **HOLDS**.
  - M3: U at F* fails SPARC (Z -0.455 / -0.449). It **BITES**.

## Disclosed
1. The r_vir convention (200 rho_c0, h = 0.70) is a convention borrowed from standard cosmology, not derived under
   the law. So is the isothermal shape; under the law the spheroid's equilibrium is set by the law's potential. The
   brackets move the window but not the split.
2. The canonical PARTIAL is thin: SPARC fails by rms at F*, and the window sits at X-COP's lower 95 % edge.
3. dSph shifts use all GB1 points (25 bright M31), not SE2's 21 admissible ones. Groups are graded at f* 0 and 1
   against SE2's single interval.
4. The Bullet and the millilensing use U's F, as frozen. Model I's F* (1.7) would give the bullet subcluster less
   mass, which is worse.
5. Added after the first run, with no graded number changed: the S4b eps block (frozen in the criteria and missing
   from the first script; it was added and the script rerun) and the "all but UDG" intersection, which is a
   post-freeze diagnostic and reported only. The first run's keys are byte-equal to the rerun's.
6. Every literature input (Omega_b h^2, t_H, Lacey-Ostriker, the bounds, the caustic transients) is PROVISIONAL and
   from memory. No downloads were made.
7. The machine load was about 38.

Kappa = 1/2 FITTED; not theory closed.
