# WLG1R RESULT (blind re-grade of WLG1's frozen question, scorecard row 40)

2026-11-14. Brief ec7fed6252; builder's frozen criteria 8a730ebaa1 (committed alone); fetch script 5fb840fa9d and main
script f498060fc8 committed before any query or graded run. Written before WLG1's results were opened (they were not
opened). TEST lane, blind, POST HOC. Adopts nothing. kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Cold dark
energy is a gravitating field component, not a particle. Footings side by side, never pooled.

## Frozen words

| footing | word |
|---|---|
| canonical (a0 9.3603e-11) | **NOT EVALUABLE, BLIND** |
| alt (a0 1.1312e-10) | **NOT EVALUABLE, BLIND** |

Cause: **KA-6 fails on the W sample**: 283 of 316 W lenses (0.896) have their own ECLIPSE MER object in their cone
with a photo-z row; the line is 0.90 (C passes, 0.952). Every other known answer, both instrument checks and all three
must-bite twins pass; 298 W lenses are graded (>= 150).

The fail was checked as hard as a pass would be. Of the 33 W lenses missing: 18 have no `MER_object_id` in the
ECLIPSE object catalogue at all (all from the "Systematic" campaign), 1 has an id that is not in its EUC6R cone, and 14
have an id in the cone but no row in the archive. A fresh query of those ids (both `dr1.phz_photo_z_wide` and
`dr1.phz_physical_parameters_wide`) returned no rows, and the other build's untracked photo-z files hold no rows for them
either. The miss is in the data, not in this code. KA-6 only feeds Delta, which uses the 520 W and C lenses that do have
a row, so the readings below are still informative. They are post hoc.

## Post hoc reading (what the words would be if KA-6 had passed; NOT the frozen word)

| | canonical | alt |
|---|---|---|
| (S) median s [95 %] | 1.093 [1.061, 1.125] FAST | 0.904 [0.878, 0.931] SLOW |
| W with s >= 1 / C with s >= 1 | 0.644 / 0.050 (12 C) | 0.342 / 0.021 (5 C) |
| (A) median r [95 %], N-A, z_s = inf | +0.023 [+0.008, +0.035] FITS | same (N-A does not depend on a0) |
| control condition | met trivially (12 < 20) | met trivially (5 < 20) |
| would-be word | WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, **FRAGILE** (flips: G-0 -> GROUPS TOO SLOW; G-HI -> NO VERDICT, control fails; B-ZS2 -> HALO SHORT) | GROUPS TOO SLOW: ROW 40 FAILS, **FRAGILE** (flip: G-HI -> NO VERDICT, MIXED speed) |

**The speed depends on the gas.** In the primary configuration, the median W system's baryons are 6.6e12 Msun:
class-level gas 5.2e12 (78 % of M_b, ESZ1's 1 keV stacked value given to every W lens), lens stars 12 %, net members 8 %.
With no gas (G-0), s = 0.634 / 0.524 and both footings read SLOW. Members alone do not make the groups fast.

**The amount depends on the source redshift.** Inside R_E the halo terms supply a median 0.90 of the fast-layout missing
mass (M_obs - M*_lens F_2D). The halo fits at z_s = infinity, the least mass lensing allows. At EUC8's central z_s it
falls short (+0.170 [+0.155, +0.189], UNDER) on both footings.

## Numbers

- Samples: W 316 (298 graded: 3 edge, 16 photo-z coverage < 80 %), C 249 (241), L 40 (38), R 60 (54); edge reference
  median N_bg 135, threshold 54. EUC17 correction: W 316 of 316, C 136 of 249 (the rest are grade B, uncorrected).
- Photo-z: 179,867 ids (179,823 cut objects plus 44 lens objects that fail the neighbour cut, added so that KA-6 and
  Delta can be read; disclosed), 180 requests, no retries, 171,898 rows. Against the other build's files on 12 W cones:
  2,230 ids in both, 0 value mismatches, 1 id only there.
- Delta = +0.437 dex (520 lenses; B-UNC +0.326). No member needed the H-band fallback. R_sys: median 600 kpc; 179 of
  298 W clipped at 600, none at 100; all converged.
- Median net member stellar mass: inside R_sys W 5.6e11, C 5.3e10; inside 300 kpc W 3.4e11, C 6.6e10, L 1.16e12 Msun.

## Known answers, checks, twins

KA-1 PASS (max |diff| 5e-5, which is the 4-decimal rounding; 1 / 0 fast). KA-2 PASS (5e-5 dex). KA-3 PASS (665 of 665
targets exact; +3.59 on 242 pairs). KA-4 PASS (668.53 / 807.93). KA-5 PASS (median rel 7e-6). **KA-6 FAIL (W 0.896, C
0.952).** KA-7 PASS (2e-15). N1 PASS (R median -8.9e10, |.| <= 1e11; 54 fields). N2 PASS (L - C +1.09e12
[+3.9e11, +1.87e12]). TW-ZS bites (W median 3.41e11 -> 2.55e10). TW-INJ bites (FITS / FITS; true by construction).
TW-X0 (the builder's own twin) bites: r +0.260 [+0.239, +0.280], UNDER on both footings. TW-H: FAST on both footings.
TW-D: SLOW on both. All three twins exit 1.

## Traps and disagreements with the brief

1. **KA-6's 90 % line sits at the data's limit.** 18 W lenses have no MER id in ECLIPSE. The line may be stricter than
   the question needs, because KA-6 feeds only Delta. Relaxing it after seeing the numbers would be post hoc.
2. **Class gas given to every lens dominates the speed.** One stacked value (5.2e12 at 1 keV) is credited whole to each
   W lens at every R_sys (reading B.2). The brief scales gas mass as 1 / T and does not bracket T. Any per-lens gas
   estimate would decide row 40's speed on its own.
3. **R_sys clips at 600 kpc for 60 % of W.** Members beyond 600 kpc, out to turnaround, are not counted (the brief says
   so). R600 does not change the reading.
4. **Control condition.** Fewer than 20 C lenses are fast in the primary, so the condition is met trivially. Under G-HI
   it is tested (93 / 35 C lenses fast) and **fails**.
5. Crash fix after the script commit, with no number changed: an empty cone gave a non-boolean array (`dtype=bool`
   added), before any output.

Outputs: `wlg1r.out`, `wlg1r.json`, `wlg1r_per_lens.csv`, `wlg1r_fetch_manifest.csv`, `wlg1r_MUTATE_{ZS,INJ,X0}.*`.
Raw photo-z rows: `_external_data/wlg1r_phz_by_id/` (untracked). Not pushed. Scorecard not edited.

kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Adopts nothing.
