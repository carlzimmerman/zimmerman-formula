# WLG1 RESULT: are Euclid's wide lenses fast groups? (scorecard row 40)

**As frozen: WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, FRAGILE (canonical) / GROUPS TOO SLOW: ROW 40 FAILS, FRAGILE
(alt).**

The canonical word is a HIT, not a pass. It is post hoc and awaits a blind re-grade. It rests on two things this lane
did not measure lens by lens:
- **The gas.** ESZ1's class-mean hot gas, 5.2e12 Msun, is assigned to every wide lens. It is 78 % of the baryons
  counted. With no gas, both footings read GROUPS TOO SLOW.
- **The source redshift.** Sources are put at infinity, the least mass lensing allows. At EUC8's central source case
  (z_s about 2) the canonical word is HALO SHORT: ROW 40 FAILS.

The member galaxies the census counted barely move either word.

TEST lane: adopts nothing, relabels nothing, registers nothing; the scorecard is not edited. Criteria 8ca77a609e
(alone, before any script, query or number); scripts b44a61c9e9 (before the analysis was run). Footings side by side,
never pooled. Cold dark energy is a gravitating field component of the record, not a particle and not matter.
kappa = 1/2 and X = 5.41 are FITTED. Nothing here says the theory is closed or that the data favour the framework over
LCDM.

## 1. What was counted

The census covers 298 of the 316 wide lenses (3 lost to the edge rule, 15 to photo-z coverage below 80 %) and 241 of
EUC6R's 249 matched controls.
- **Neighbours.** Euclid DR1 MER objects brighter than H_E = 22 (EUC6R's cut and cones). Each has a photo-z and a
  stellar mass from `dr1.phz_photo_z_wide` and `dr1.phz_physical_parameters_wide` (ESA archive, by id lists): 665 cones,
  no failed request, 10 MB, untracked under `_external_data/wlg1_phz_by_id/`.
- **Members.** Galaxy class only, with |z_phot - z_l| <= 0.08 (1 + z_l), at 30 kpc to R_sys. Background is the same
  window at 600 to 1000 kpc.

Medians over W; the controls C are in the last column.

| quantity | W (wide lenses) | C (controls) |
|---|---|---|
| lens stars, EUC17-corrected, common scale | 8.27e11 | 5.05e11 |
| net member stars inside R_sys | 5.58e11 [4.50, 6.46] e11 | 0.53e11 |
| net member stars inside 300 kpc | 3.41e11; paired W - C +2.40e11 [+1.37, +3.11] (227 pairs) | 0.66e11 |
| gas (ESZ1 class level, G-MID) | 5.2e12 | 0 |
| M_b | 6.63e12 [6.49, 6.78] e12 | 0.60e12 |
| R_sys (self-consistent 200 rho_c radius) | 600 kpc (179 lenses clipped at 600) | 268 kpc |

The scale constant Delta puts the archive's stellar masses on the lens scale. It is +0.437 dex (520 lenses, 16 to 84 %
+0.30 to +0.60), measured as the lens's corrected mass minus its own archive mass.

### Speed: s = v_L(M_b) / v*(z_l), median [95 %]

| footing | W | fraction of W at s >= 1 | C |
|---|---|---|---|
| canonical | **1.093 [1.061, 1.125]: FAST** | 192 / 298 | 0.520 (5 % fast) |
| alt | **0.904 [0.878, 0.931]: SLOW** | 102 / 298 | 0.430 (2 % fast) |

### Amount: each W lens treated as fast, z_s at infinity

The amount uses Newtonian lens stars plus the projected reference halo at the 5.41 share, plus gas in the halo's shape.
It is the same on both footings, because the N-A layout has no a0.

| quantity | value |
|---|---|
| M_obs | 7.23e11 |
| lens stars inside R_E (M_obs minus the missing mass, medians) | about 3.6e11 |
| cold-halo cylinder | 3.17e11 |
| gas cylinder | 0.46e11 |
| missing mass in the fast layout (M_obs - Newtonian stars) | 3.64e11 |
| what the halo supplies, as a share of it | 0.90 [0.85, 0.95] |
| r = log10(M_obs / M_ref) | **+0.023 [+0.008, +0.035]: FITS** |
| r on the lenses that are fast | -0.005 (canonical, 192), -0.040 (alt, 102) |

**Words.** Canonical: FAST + FITS. The control condition is met trivially: only 12 controls are fast, below the 20 the
criteria need. That gives the pass word. Alt: SLOW gives GROUPS TOO SLOW.

## 2. Brackets (one change each; words canonical / alt)

| bracket | s (can / alt) | r | word canonical | word alt |
|---|---|---|---|---|
| **G-0** (no gas) | 0.634 / 0.524 | +0.159 | GROUPS TOO SLOW | GROUPS TOO SLOW |
| **G-HI** (ESZ1 2 sigma: 8.3e12; C 3.0e12) | 1.232 / 1.019 | -0.012 | NO VERDICT (control condition fails: 93 fast controls, r -0.35) | NO VERDICT (MIXED) |
| B-UNC (uncorrected lens masses) | 1.063 / 0.879 | +0.098 | PASSES | TOO SLOW |
| B-RAW (archive masses unscaled) | 1.064 / 0.880 | +0.026 | PASSES | TOO SLOW |
| B-W05 / B-W12 (photo-z window) | 1.086 / 1.099 can | +0.023 / +0.021 | PASSES | TOO SLOW |
| R300 / R600 | 1.077 / 1.094 can | +0.025 / +0.023 | PASSES | TOO SLOW |
| N-B (the lens keeps its law) | 1.093 / 0.904 | -0.078 / -0.091 | PASSES | TOO SLOW |
| B-C07 / B-C14 (concentration) | unchanged | +0.092 / -0.056 | PASSES | TOO SLOW |
| **B-ZS2** (z_s = max(2, z_l + 0.5)) | unchanged | +0.170 | **HALO SHORT** | TOO SLOW |
| B-STAR+ (member stars x 1.4) | 1.119 / 0.926 | +0.020 | PASSES | TOO SLOW |

Canonical is FRAGILE through G-0, G-HI and B-ZS2. Alt is FRAGILE through G-HI. Every bracket on stars, members, window,
radius, nesting and concentration leaves both words unchanged.

## 3. Known answers, checks, twins (all pass)

| item | result |
|---|---|
| KA-1 lens stars only (LNJ1) | s matches lnj1_per_lens to 5e-5; above v* **1 / 0** of 316 |
| KA-2 LNJ1's projections on W (obs, law can / alt, joint X 5.41) | max difference 5e-5 dex |
| KA-3 EUC6R | 0 count mismatches on 665 targets; paired median richness +3.588 on 242 pairs (target +3.59) |
| KA-4 v*(0) | 668.53 / 807.93 km/s |
| KA-5 EUC8 far excess per lens | median relative difference 7e-6 |
| KA-6 lens MER objects with photo-z | 520 / 565 = 0.92 |
| KA-7 virial definition | 2e-15 |
| N1 blank fields (54) | net member mass in 300 kpc -0.89e11 (limit +/- 1e11; close to the line) |
| N2 positive control | L 1.16e12 (38) against C 0.07e12; lower bound of the difference +3.9e11 |
| TW-ZS photo-z shuffle | W members in 300 kpc 3.41e11 -> 0.26e11: bites; exit 1 |
| TW-INJ | r = 0, FITS on both footings; exit 1 |
| TW-H (v*/2) / TW-D (2 v*) | FAST / SLOW on both footings (the boundary matters) |

The shuffle twin bites on its gate, but its word does not change (`wlg1_MUTATE_ZS.out`): canonical s is 1.056 and r
+0.025. Collapsing the members barely moves M_b, which shows that the gas carries the result.

## 4. POST HOC readings (no word; `wlg1_posthoc.py`, `wlg1_posthoc.out`)

1. **Source redshift.** For each lens, sources nearer than z_s* leave the halo short (r > +0.10).
   - The median z_s* is **3.82**.
   - 61 of 298 lenses are short even at infinity.
   - 24 % have z_s* < 2 and 42 % have z_s* < 3.

   EUC1's ceiling-break redshift was 4.34 / 3.58, so the fit needs sources about as distant as the law alone does.
2. **Gas needed for s = 1**, given the stars and members counted here:
   - canonical: median 3.5e12 (36 % of lenses need more than ESZ1's measured 5.2e12; 8 % more than its 2-sigma limit);
   - alt: median 7.7e12 (66 % need more than 5.2e12; 45 % more than 8.3e12).
3. **Gas share.** Gas is a median 78 % of M_b in the main configuration.

## 5. What this says

1. **Stars and members alone do not make the wide lenses fast.** The census finds real group members: 2.4e11 Msun more
   stars inside 300 kpc than the controls, and the photo-z shuffle removes them. Even so, lens plus members is about
   1.4e12 Msun, and s is 0.63 / 0.52. Row 40's assumption needs the hot gas.
2. **With ESZ1's class-mean gas, the canonical boundary sits just below the median wide lens; the alt boundary sits just
   above it.** The 1 keV conversion is self-consistent at v* (a system at v* has kT about 0.8 to 1.2 keV). The gas
   number has three weaknesses:
   - it is a 2.6 sigma stack in a 2' (about 700 kpc) compensated aperture that includes the line of sight;
   - ESZ1's own wide-minus-control word was NO EXCESS DETECTED;
   - it is assigned to every lens.
3. **Given that much baryon mass, the reference halo at the 5.41 share supplies about 90 % of the missing mass inside
   R_E**, with the source at infinity and the halo centred on the lens. This is the first lane where the projected
   reference halo reaches the wide lenses' Einstein masses. LNJ1's lens-only halo fell short by 0.23 to 0.38 dex.
4. **The fit does not survive realistic sources.** At z_s about 2 the halo is short by 0.17 dex. Real sources only raise
   M_obs, so the z_s-infinity FITS is the best case, not a robust one.
5. **The controls.** At G-MID only 5 % / 2 % of controls are fast, so the rule leaves them the law's layout, which EUC1
   found sits at its ceiling. At G-HI, 93 / 35 controls would be fast, and the reference layout over-predicts them by
   0.35 dex (at z_s infinity, not robust).
6. **Row 40 stays open.** The canonical HIT turns on unmeasured per-lens gas and distant sources; alt fails on speed.
   What would decide it:
   - per-lens hot-gas masses (X-ray or SZ group masses);
   - real source redshifts (EUC1-F);
   - a blind re-grade of this census.

## 6. Disclosures and traps

- **Code fix before any word (run 1 kept as `wlg1_run1_unitbug.out`).** The first run returned the lane's lensing
  masses in kg, not Msun. KA-2 (off by 30.3 dex = log10 Msun) and KA-5 failed, so the run read NOT EVALUABLE. Two lines
  were changed to divide by Msun. No criterion, cut or number of the frozen design changed. The speeds in run 1 are
  identical to the final ones; I saw them, and run 1's amounts were meaningless.
- **Lens identification.** 45 of 565 W / C lenses have no photo-z row for their ECLIPSE MER id (many have no
  MER_object_id in ECLIPSE). They still enter with their ECLIPSE mass and are left out of Delta only. Their own MER
  object cannot be counted as a member, because it lies inside the excluded inner 30 kpc.
- **N1 is near its line** (-0.89e11 against +/- 1e11). The background subtraction may be slightly over-subtracting,
  which would bias members low. That does not affect the words.
- **Not bracketed:** the gas temperature (gas mass scales as 1 / T); the halo's centre (it is centred on the lens; an
  offset group centre would put less inside R_E); member stars inside the cylinder; turnaround-scale baryons beyond
  600 kpc (cones end at 1 Mpc).
- **Data etiquette.** One paced stream at 1.5 s, generic client name, no personal details; read with `python3 -I`.
- **Hand estimate against outcome.**
  - Expected HALO SHORT on both footings (P 0.6). Got a canonical PASS and an alt TOO SLOW.
  - My halo estimate was low by about 1.6 x: I took r_s about 200 kpc, and the code's r_s is about 110 kpc at these
    masses.
  - The speed estimate was right: about 1.1 / 0.9 with ESZ1's gas.

## 7. Files and commits

- **Code:** `wlg1_fetch.py`, `wlg1.py`, `wlg1_posthoc.py`.
- **Main run:** `wlg1.out`, `wlg1.json`, `wlg1_per_lens.csv`, `wlg1_fetch_manifest.csv`.
- **Twins:** `wlg1_MUTATE_ZS.*` and `wlg1_MUTATE_INJ.*` (both exit 1).
- **Other:** `wlg1_posthoc.out`, `wlg1_run1_unitbug.out`.

Commits (local, not pushed): criteria 8ca77a609e; scripts b44a61c9e9; results and this file in the next commit.

kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Adopts nothing.
