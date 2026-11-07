# NC3: do early types that formed inside clumps carry a residue over the law that field early types do not? (FRAMEWORK_CANDIDATE_2 R5 / K4)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (born-clumped cold dark energy; no particle).
Footings graded separately, never pooled.
- Criteria: FROZEN_CRITERIA.md (b5625a2299), committed alone before any script or residual.
- Script: nc3.py -> nc3.json / nc3.out; nc3.py --mutate -> nc3_MUTATE.json / nc3_MUTATE.out.
- One thread, 4 s, peak RSS 0.24 GB. Nothing downloaded.

## Label: UNRESOLVED on both footings. No member residue is detected; members carry at most about +0.065 dex

**Sample.** MaNGA DynPop early types (T15 MType <= -1, QX22's cuts) matched to Tully 2015's 2MASS nests:
- IN, 96 galaxies: 76 cluster members (nest Mlum >= 1e14, Nmb >= 5) and 20 group centrals.
- FIELD, 122 galaxies: 2MRS singletons.

**Statistic.** D is the median residual ln(g_obs / g_law) at r_half, IN minus FIELD, matched in M* x sigma cells. Matching
on sigma is the IMF control.

| | canonical | alt |
|---|---|---|
| D (dex), 15 cells | **+0.011** | **+0.012** |
| sigma_D (bootstrap / model / M*) | 0.028 (0.025 / 0.009 / 0.009) | 0.028 (0.025 / 0.009 / 0.011) |
| 95 % CI | [-0.044, +0.065] | [-0.043, +0.068] |
| Frozen label | UNRESOLVED | UNRESOLVED |

- **Why UNRESOLVED and not NO DIFFERENCE:** the CI's upper edge, +0.065 / +0.068, is just past the +0.05 line.
- **Why not R5 SIGNAL:** D is a fifth of the +0.05 line, and the CI contains 0.
- **What the data allow:** at r_half, early types that formed inside clumps carry no more than about 16 % extra
  dynamical mass over field early types of the same M* and sigma (95 %).
- **The test had power.** M2 injects +0.10 dex into the IN galaxies and reads back +0.111 / +0.112 [+0.057, +0.168]:
  R5 SIGNAL on both footings.
- **K4 reading: NOT DECIDED by the frozen rule**, because the label is not NO DIFFERENCE.
  - The stripping budget does not rescue a hidden residue. 79 % of the IN galaxies are stripping-proof at r_half at
    r_p 0.1 Mpc (r_t >= 2 r_half), and 99 % at 0.5 Mpc. The 33 centrals are not stripped at all.
  - So if members ever carried the component inside r_half, it would still be there, and it is not detected above
    +0.065 dex.
  - The reading that survives: the component was never inside members' r_half, or members carry less than ~16 % there.
  - The candidate states no galaxy-scale number, so this bounds it but does not grade it.

## Reported readings (not graded)

| Reading | canonical D [95 %] | alt D [95 %] |
|---|---|---|
| Cluster members only (76) | +0.032 [-0.021, +0.086] | +0.033 [-0.023, +0.088] |
| Group centrals only (20) | -0.069 [-0.213, +0.074], NO POWER | -0.069 [-0.212, +0.075], NO POWER |
| Group satellites (33) | +0.050 [-0.067, +0.166], NO POWER | +0.052 [-0.064, +0.167], NO POWER |
| Red u - r >= 2.5 instead of MType (57 / 77) | +0.015 [-0.041, +0.071] | +0.014 [-0.042, +0.069] |
| Posacki IMF per galaxy, M*-only cells | +0.029 [-0.037, +0.096] | +0.034 [-0.028, +0.095] |
| M*-only cells, no IMF | +0.052 [-0.002, +0.106] | +0.054 [+0.000, +0.107] |
| FIELD restricted to cz < 6000 | only 3 field galaxies, no cells | |

- **Without sigma matching or an IMF correction,** members sit about 0.05 dex high. On alt that reads R5 SIGNAL by a
  hair (CI lower edge +0.0004). Matching on sigma, or applying Posacki's sigma-IMF, takes it to +0.01 to +0.03. This is
  the IMF trend, as ST1 found for the ellipticals. That is why the frozen statistic matches on sigma.
- **Raw medians, no matching:** IN +0.61 / +0.59 dex, FIELD +0.55 / +0.53. Both classes sit well above the law at r_half
  in raw terms. That is the known early-type offset, which is IMF plus the 0.5 M* convention.
- **The candidate's purest case, group centrals,** has no power (n 20, 5 cells). It sits on the low side (-0.07).

## The two added reads

- **KiDS isolated lenses, the field-by-construction control (KX1 M2):** the law against the isolated-lens data with the
  joint budget reads z_law +1.50 / -0.21 / -0.06 / -0.62 (canonical) and +1.80 / +0.18 / +0.36 / -0.16 (alt).
  - The posterior excess is -0.21 to +0.05 dex. Nothing shows in the field, as the candidate requires (R4).
- **CLASH lensing-only s (QX33):**
  - Past the BCG (r > 50 kpc), the medians are negative in both halves: HIGH -0.110 [-0.364, +0.146] and LOW -0.077
    [-0.270, +0.057] canonical; -0.127 / -0.099 alt. The missing mass sits more concentrated than gas plus BCG, which is
    the sign an early-collapsed clump gives.
  - Every CI contains 0, so this is consistent with the candidate, not evidence for it.
  - At all radii, the BCG cusp makes s +0.16 / +0.09.
  - QX33 had no power on evolution, and that is unchanged.

## Small samples, reported only

- **SLUGGS** (CFG330 K0 outer GC-bin offsets, tagged by T15 within 60 arcsec, no velocity cut): median IN +0.102 (n 8),
  FIELD +0.127 (n 2), group satellites +0.080 (n 4), other +0.104 (n 3), canonical.
  - CFG330's "centrals +0.22 vs others +0.06" was a centrals split. It does not reappear as IN over FIELD.
- **The seven X-ray ellipticals** (QX24 T2 raw offsets): IN NGC 1407 +0.22, NGC 4261 +0.01, NGC 4472 +0.27, NGC 4649 +0.41,
  NGC 6482 +0.08. "Other" (small nests): NGC 720 +0.51, NGC 4125 -0.02. None is a T15 singleton.
  - The largest offset, NGC 720, is not IN. That runs against R5, as EV1 found for membership.

## Controls

- **KA1:** the reimplemented QX22 sample reproduces QX22's D, +0.001593 / +0.002276, to < 1e-6. **PASS.**
- **M1 (shuffled tags within cells, 200 seeds):** mean D +0.0001 / +0.0003 (sd 0.022). The first shuffle's CI contains 0.
  **PASS.**
- **M2 (+0.10 dex injection):** R5 SIGNAL on both footings. **PASS.**

## Disclosed

- The T15-match counts (1545 all; red 179) were seen before the freeze. After QX22's cuts the matched set is 1188 and the
  graded early types 313. No residual was seen before the freeze.
- T15 Mlum is a luminosity-based nest mass, and "singleton" means alone above 2MRS K 11.75. At MaNGA's redshifts that
  limit misses fainter companions, so some FIELD galaxies sit in faint groups. That would dilute D toward 0. The cz < 6000
  control has no power (3 field galaxies).
- The SLUGGS and X-ray positions are tagged with no velocity check (60 arcsec). The X-ray positions are partly from the
  literature, as in QX24.

## One sentence

At fixed stellar mass and dispersion, MaNGA early types that formed inside clusters or at group centres sit +0.011 /
+0.012 dex from field early types (95 % at most +0.065 / +0.068). The test could see +0.10, and stripping cannot hide
a residue at r_half. So the born-clumped picture survives at galaxy scale only if the component never sat inside members'
r_half. The KiDS field control shows nothing, and CLASH's past-BCG s leans to the sign an early clump gives, without power.

Kappa = 1/2 FITTED; not theory closed.
