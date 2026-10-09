# CFG519: the observed leaked-satellite fraction of the KiDS isolated lenses (stack P) is 0.223 +- 0.004 (KiDS-bright x GAMA G3C). It lies between CFG502's HOD (0.171) and CFG506's box (0.343 / 0.432). Under the frozen rule all four references are EXCLUDED, so CFG506's box galaxy-halo rule needs re-calibration. The spectroscopic companion count is 0.125 per lens, not 0.205

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (ff98baf04).
- **Data, no new download.** KiDS-bright is already on disk. The GAMA DR4 G3C v10 tables are CFG471's logged fetch, SHA-checked (`FETCH_LOG.md`). nice 10, single thread, about 30 s per run.
- **Pure data: the a0 footings do not enter.** canonical 9.3603e-11 and alt 1.1312e-10 are irrelevant here. kappa = 1/2 is FITTED elsewhere. No gravity model is evaluated.
- "Cold energy" = the cold clumping component. Its mass is still required, and no particle species is added.
- Nothing here says the data favour the framework. Not "theory closed".

## The sample
- **Lenses.** The record's stack P: 181,477 KiDS isolated lenses, W = 10 Mpc, from CFG502's staging (C1 and C2 reproduce it exactly).
- **Overlap.** 34,541 of them sit in GAMA G09 / G12 / G15. 20,294 (58.8%) match a G3C galaxy within 1.5 arcsec.
  - Median separation 0.13 arcsec.
  - Photo-z NMAD 0.017; |dz| / (1 + z) > 0.15 in 0.14%.
- **Completeness and reweighting.**
  - The KiDS pool's G3C completeness is 0.96-0.98 at r < 19.5 and 0.42 at r 19.5-20.
  - The fractions are reweighted over 48 (log M*, z_phot, colour) cells to the lensing weight of the whole stack P. Cells with >= 20 matched lenses carry 99.6% of the weight.
- **Representativeness (C5 PASS).** The close-pair veto probability p_10 is 0.075 in the overlap and 0.070 outside it. The ISO pass fraction is 0.284 in the overlap and 0.304 outside.

## Results (numbers from `cfg519_satfrac_results.json`; errors are 12-region jackknife)

| quantity | measured | reference |
|---|---|---|
| **leaked-satellite fraction, ISO, S_IC (G3C member, not the iterative centre)** | **0.2234 +- 0.0034 stat, +- 0.0044 tot** | CFG502 HOD 0.171; CFG503 0.181; CFG506 box F 0.343 / P 0.432 |
| same, S_BCG | 0.2249 | |
| same, groups with Nfof >= 3 only (lower bound) | 0.1319 | |
| unreweighted matched lenses | 0.2258 | |
| parent (ALL lens candidates) | 0.3134 +- 0.0033 | CFG502 f_par 0.254 |
| ISO / ALL at fixed cells | 0.757 +- 0.009 | CFG502 model 0.67 |
| f30 (W = 30) | 0.169 +- 0.006 | |
| **spec-z companions within 0.5 Mpc, abs(dv) < 1000 km/s, log M* >= 10.44** | **0.1246 +- 0.0046** | CFG506 F box predicted 0.313; photometric 0.205 (KiDS-wide) |
| same, abs(dv) < 2000 km/s | 0.1264 | |
| photometric count, same lenses, same weighting | 0.1981 +- 0.0098 | |
| spec pair-satellite fraction (chance-corrected) | 0.093 | |

Satellite fraction per cell (S_IC, ISO). Columns are z_phot bins; the number of matched lenses is in brackets.

| log M* | z 0.1-0.2 | z 0.2-0.3 | z 0.3-0.4 | z 0.4-0.5 |
|---|---|---|---|---|
| 8.5-9.5 | 0.20 (650) | 0.18 (174) | pooled | pooled |
| 9.5-10.0 | 0.21 (813) | 0.16 (1079) | 0.14 (163) | pooled |
| 10.0-10.25 | 0.23 (500) | 0.22 (1075) | 0.17 (223) | pooled |
| 10.25-10.5 | 0.21 (536) | 0.25 (1923) | 0.21 (776) | 0.06 (51) |
| 10.5-10.75 | 0.24 (343) | 0.24 (2603) | 0.24 (2326) | 0.14 (278) |
| 10.75-11.0 | 0.15 (126) | 0.22 (1561) | 0.24 (4108) | 0.19 (959) |

- The fraction is flat in mass at 0.20-0.25 for z < 0.4.
- At z 0.4-0.5 it drops. That is where G3C is least complete: GAMA sees only the bright members.
- **Direct veto efficiency (C6).** A G3C satellite's own matched iterative centre vetoes it 10.3% of the time (6,981 qualifying pairs, z < 0.3). CFG502's close-pair p_10 was about 0.07.

## Verdicts (frozen rules)

**V1, leaked-satellite fraction.** f_obs = 0.2234 +- 0.0044 (sigma_sys 0.0028 from IterCen vs BCG and from the reweighting).

| reference | value | distance | verdict |
|---|---|---|---|
| CFG502 HOD | 0.171 | 11.7 sigma | EXCLUDED |
| CFG503 | 0.181 | 9.6 sigma | EXCLUDED |
| CFG506 box F | 0.343 | 27.0 sigma | EXCLUDED |
| CFG506 box P | 0.432 | 46.9 sigma | EXCLUDED |

- **CFG506's box galaxy-halo rule needs re-calibration: YES.**
  - The box makes 1.54x (F) / 1.93x (P) too many leaked satellites.
  - Its parent satellite fraction at log M* 10.5-10.6 is 0.66. The measured value is 0.343 (post-hoc PH2), so the box is about 2x too high.
- **CFG502 / 503 leakage input confirmed: NO. Label "LEAKAGE INPUT CONTRADICTED".** The HOD's 0.171 is low by 0.052, i.e. 30%.

**V2, companion count.**
- C_spec / 0.313 = 0.398, outside [0.67, 1.5]. The box companion prediction is NOT CONSISTENT with spectroscopy.
- C_spec vs C_phot on the same lenses: 0.125 vs 0.198, 10.3 sigma apart. The photometric excess is QUESTIONED as a count of real companions.

### What the verdicts mean (post-hoc, `cfg519_posthoc.*`; not part of the frozen verdict)
- **PH1: where the photometric excess comes from.** On these lenses the photometric excess is 0.191 in-field. It splits into three parts:
  - 0.110 are companions with a GAMA redshift within 1000 km/s: real one-halo companions.
  - 0.047 have a GAMA redshift but sit >= 1000 km/s away. These are correlated line-of-sight structure that survives the annulus subtraction.
  - 0.035 have no redshift (almost all r > 19.5).

  So the photometric count is real correlated structure, but only about 60% of it is near-velocity companions. CFG506's box emulation counts correlated pairs out to |D| <= 100 Mpc/h with the photo-z kernel. It is therefore like-for-like with the photometric 0.205, not with C_spec. **CFG506's frozen ratio 0.653 stays the relevant validation number. The V2 box ratio (0.40) overstates the mismatch.** "QUESTIONED" means the photometric count is not a satellite count. It does not mean the count is wrong.
- **PH2: how the satellite definition matters.**
  - The definition "in a G3C group with a matched member more massive in KiDS log M*" gives 0.145 +- 0.002.
  - Groups with Nfof >= 3 give 0.132.
  - These two are lower than S_IC because the more massive member can be missing from the KiDS pool (z_phot cut, mask), because KiDS masses are noisy, and because Nfof >= 3 drops the pairs.
  - The definitional spread is therefore about 0.13-0.22. **It brackets CFG502's 0.171 / 0.181. It never comes near CFG506's 0.343 / 0.432.**
  - So the robust statement is: the box rule is too satellite-rich under every definition. CFG502's HOD is excluded only under the frozen (IterCen) definition and its narrow error band; G3C interlopers and fragmentation are not in that band.
- **PH3: weighting convention.** CFG506 weighted by the outermost bin only; with that weighting f = 0.2239. The weighting does not matter.

## Implications
- **CFG506 (native ruler).** Its failure (companion ratio 0.653) is now explained on the data side. The box's leaked-satellite fraction (0.34) and parent fraction (0.66 at 10.5) are both about 1.5-2x the observed values (0.22, 0.34).
  - No re-score is run here. The box tables keep the companion count only as a total (no central / satellite split), as declared in the criteria.
  - **Follow-up lane, to be frozen first:**
    1. A box galaxy-halo rule whose parent satellite fraction reproduces the measured ALL fraction per (log M*, z) cell. Use this lane's PH2 / cell tables: 0.29-0.35. For example, raise M_1 / M_min above 17, or fix the host-mass definition.
    2. Then CFG506's frozen validation unchanged: photometric companions 0.205, [0.67, 1.5]. Check also that the leaked fraction lands at 0.22 +- 0.03.
    3. Then CFG506's re-score.
- **CFG502 / 503 / 504 (LCDM-native E).**
  - Under the frozen rule the leakage input carries "LEAKAGE INPUT CONTRADICTED". The measured fraction is 1.30x CFG502's.
  - E's leaked-satellite part scales roughly with f. That would raise E at 0.3-0.8 Mpc by about 0.45-0.7 Msun/pc² (30% of 1.5-2.4). This is information only, not a re-score.
  - Direction: it helps the 1.0-1.4 Mpc deficit CFG502 found (data above LCDM + E). It worsens the inner bins, where data already sit below LCDM.
  - Within the definitional spread (0.13-0.22) CFG502's value is not clearly wrong. A re-score with f = 0.22 belongs in a frozen follow-up, not here.
- **CFG502's parent fraction is also low** (0.254 vs 0.313 measured). Isolation is less effective than the HOD model says: ISO / ALL is 0.76, against 0.67.

## Controls and MUTATE
- **Pass:**
  - C1 (ISO = staging).
  - C2 (pool rebuild exact).
  - C2b (inner photometric counts = CFG502's cin on all 34,541 overlap lenses, exact).
  - C3 (G3C SHA-256).
  - C4 (reported: match median 0.13 arcsec).
  - C5 (p_10 0.075 vs 0.070).
- **MUTATE (`cfg519_satfrac_MUTATE.out`, `_results_MUTATE.json`), both load-bearing, both PASS:**
  - M1, redshifts shuffled within each field. C_spec 0.0056 +- 0.0022 (main 0.125); f_pair 0.0035 (main 0.093).
  - M2, positions displaced by 1 deg. The match rate falls to 0.07%, so V1 cannot be computed.
- **Departures: none.** Implementation fixes, dated 2026-10-08, none of which changes a number:
  - The first MUTATE run crashed while collecting files, after M1 had printed (wrong temp-JSON name). The name was fixed and the run repeated; M1 was identical.
  - C2b had been skipped under M1 with a misleading message. It now runs and passes.
  - A state save for the post-hoc script was added. The main run was repeated with identical numbers.
- **Limits.**
  - G3C is incomplete at z > 0.3 and has interlopers in N = 2 groups.
  - The reweighting assumes satellite status does not depend on r at fixed (log M*, z, colour). 41% of the overlap ISO lenses (r 19.8-20) have no redshift.
  - The ANNz2 photo-z were trained with GAMA. C5 shows the pair veto in the overlap is within 0.005 of elsewhere.

## Run
```
nice -n 10 python3 -u cfg519_satfrac.py                      # main: .out, _results.json; state -> ../_external_data/cfg519_work
CFG519_MUTATE=1 nice -n 10 python3 -u cfg519_satfrac.py      # M1 + M2 -> _MUTATE.out, _results_MUTATE.json
nice -n 10 python3 -u cfg519_posthoc.py                      # PH1-PH3 (post-hoc)
```
