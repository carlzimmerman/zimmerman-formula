# CFG391: satellite-plane members vs non-members under the law (MW VPOS, M31 GPoA)

## Verdict (frozen rule, FROZEN_CRITERIA.md, commit a02cef75f)

| test | footing | members / non | Delta [dex] | predicted if members Newtonian | verdict |
|---|---|---|---|---|---|
| MW, VPOSnew (164.0, -6.9), 30 deg (PRIMARY) | canonical 9.3603e-11 | 16 / 27 | +0.098 +- 0.092 | -0.699 | **DISFAVOURED** |
| same | alt 1.1312e-10 | 16 / 27 | +0.098 +- 0.092 | -0.720 | **DISFAVOURED** |
| M31, Ibata 2013 15 planar (PRIMARY) | canonical | 14 / 17 | +0.010 +- 0.110 | -0.656 | **NON-DISCRIMINATING** |
| same | alt | 14 / 17 | +0.010 +- 0.109 | -0.676 | **NON-DISCRIMINATING** |
| COMBINED (MW D1 30 + M31 G1) | canonical | 30 / 44 | +0.028 +- 0.073 | -0.676 | **DISFAVOURED** |
| same | alt | 30 / 44 | +0.028 +- 0.073 | -0.697 | **DISFAVOURED** |

Plane members are not mass-poor relative to the law. In both hosts they keep about the full law boost
(retained fraction 1 - Delta/Delta_pred = 1.14 MW, 1.02 M31, 1.04 combined). The Newtonian expectation for
the same objects is about -0.7 dex. The M31 primary only just misses DISFAVOURED: Delta - 2 sigma = -0.210
against the -0.2 bar. Its sensitivity variants G3 (+NGC 205, LGS 3) and S4 (Collins 2013 sigma) do pass
DISFAVOURED. The verdict stands as computed: NON-DISCRIMINATING.

## What it means for the fork
These are the frozen implication rules. A fair reading is that MW is DISFAVOURED and M31 points the same way
without clearing the bar. So the pairing "VPOS/GPoA are tidal-dwarf planes" AND "old tidal dwarfs are
Newtonian under the settling model" cannot both hold. **This test cannot say which one fails.**
- Branch A: the planes are not made of tidal dwarfs. They are then not a TDG population, and the settling
  model's TDG prediction is not tested here.
- Branch B: the planes are tidal-dwarf planes, but old TDGs carry the full law boost. Then the settling
  model's "no catchment, so Newtonian" premise fails for TDGs a few Gyr old or more. That would be a design
  constraint on the settling model, for example a catchment refilled after formation or a fast settling time.
The framework itself is MOND-like: there, TDGs and primordial dwarfs both follow the law. The extra mass is
the cold fluid, not a particle, and its amount still has to be supplied. That reading is consistent with
these numbers, but it is not favoured over LCDM by them. In LCDM, plane members (if TDGs) would also be
DM-free and would also show low sigma, so this null weighs against TDG planes in LCDM too.

## Robustness (all in cfg391_plane_membership.out)
- MW, VPOSnew, any orbital sense: 20 deg +0.148 +- 0.102 (9/34); 30 deg +0.098 +- 0.092 (16/27);
  40 deg +0.082 +- 0.079 (20/23). All DISFAVOURED, so the MW verdict is ROBUST. Co-orbiting only:
  +0.166 / +0.159 / +0.134, all DISFAVOURED.
- MW, other published normals at 30 deg: VPOSclass +0.134 +- 0.073, PPK12 DoS +0.098 +- 0.094,
  PK20 mean pole k=7 +0.044 +- 0.099. All DISFAVOURED.
- MW, the PK20 published classical list (6 members / 3 non-members, classicals only): +0.134 +- 0.137, DISFAVOURED.
- M31: G2 (13 co-rotating) +0.007 +- 0.112 NON-DISC; G3 (+3 plausible) +0.010 +- 0.086 DISFAVOURED;
  S3 (upper limits at the limit) -0.006 +- 0.102 NON-DISC; S4 (Collins sigma) +0.062 +- 0.124 DISFAVOURED.
- Both footings agree to within 0.001 dex in Delta. The per-population median subtraction absorbs the footing.

## Controls
- C1 permutation null: the median permuted Delta was within 0.001 of 0 in every primary test (PASS).
  One-sided p(Delta_perm <= Delta_obs): MW 0.866, M31 0.606, combined 0.811. Members are nowhere near the
  low tail.
- C2 session-06 reproduction (recalled normal, 30 deg, a0 9.36e-11): +0.0338 +- 0.1011 vs +0.034 +- 0.098.
  PASS within the frozen tolerance. The sigma differs slightly because the bootstrap rows are in a different
  order.
- C3: our Monte Carlo poles vs PK20 Table 3 match for 9/9 classicals (PASS). Seven agree to within 10 deg.
  Leo I (32.6 deg) and Leo II (39.9 deg) fall inside their large PK20 uncertainties. Our LVD proper motions
  put Leo II outside the 30 deg VPOSnew cut, while PK20 counts it a member. The D3 list test covers that case.
- MUTATE (members made Newtonian): TDG-ORIGIN SUPPORTED on all three primaries at both footings, with
  permutation p = 0.000. Exit 1 as required (cfg391_plane_membership_MUTATE.out).

## Published inputs (FETCH_LOG.md has the location and sha256 for each)
- VPOSnew (164.0, -6.9) and VPOSclass (157.3, -12.7): Pawlowski & Kroupa 2020, Sect. 2.3. PK20 mean pole
  (179.5, -9.0): its Table 4. Classical poles: its Table 3. Membership: Sect. 2.3.3.
- DoS (156.4, -2.2): Pawlowski, Pflamm-Altenburg & Kroupa 2012, Table 1.
- **The recalled session-06 normal (169.3, -2.8) is in neither paper.** It is 6.7 deg from VPOSnew,
  and the conclusion does not change.
- GPoA: Ibata et al. 2013, Supplementary Information Sect. 2 (arXiv PDF p. 17).

## Caveats
- The isolated law is used for both hosts. M31 satellites, and inner MW satellites, sit in the host's external
  field. EFE lowers sigma_law, and does so mostly for the inner objects. Membership is not obviously correlated
  with host distance, but this was not tested.
- Plane membership for the UFDs uses one membership rule: the orbital pole within a cut of the normal in at
  least 50% of the Monte Carlo draws. The only published per-object list used is PK20's, which covers the
  classicals only.
- Ibata's list is spatial plus line-of-sight velocity (no proper motions), so it includes interlopers by
  construction. And XII drops out of every M31 test except S3, because it has only an upper limit on sigma.
- The NGC 147/185 dEs are bright and only mildly boosted (0.5 log nu about 0.15-0.2). The populations are
  median-subtracted separately, but the M31 "classical" bin mixes dSphs and dEs.
- Delta is a difference of medians, and the sample sizes are small (14-16 members per host).

## Departures from the frozen criteria
None in method. One clarification: in C2 the session-06 sigma is reproduced to within 0.0031, inside the
frozen 0.01 tolerance.

## Files
- `FROZEN_CRITERIA.md` (frozen first), `FETCH_LOG.md`
- `cfg391_plane_membership.py` produces `cfg391_plane_membership.out` and `_results.json`. With `--mutate` it
  produces `_MUTATE.out` and `_MUTATE_results.json` (exit 1 means the planted signal was seen).
- `fetched/` (git-ignored, lane-local) holds the raw arXiv sources and PDF.
