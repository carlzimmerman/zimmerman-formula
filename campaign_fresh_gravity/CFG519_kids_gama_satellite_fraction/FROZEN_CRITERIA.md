# CFG519: FROZEN CRITERIA -- the observed satellite (leakage) fraction and spectroscopic companion count of the KiDS isolated lenses, from the KiDS-bright x GAMA DR4 overlap

Written 2026-10-08, before any script of this lane exists and before any GAMA-matched number of this lane has been computed. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

## 0. Why

CFG506's framework-native environment ruler failed its photometric check (companions within 0.5 Mpc per isolated lens: measured 0.205, predicted 0.313; ratio 0.653 outside [0.67, 1.5]). Its stack-weighted leaked-satellite fraction is 0.343 (variant F, canonical) / 0.432 (variant P), against CFG502's HOD value f_W = 0.171 (CFG503's f = 0.181). Both numbers are model outputs; none is measured. This lane measures the satellite fraction of the SAME isolated sample directly, with spectroscopic redshifts and the GAMA G3C group catalogue, and measures the companion count with spectroscopic line-of-sight separations.

This is pure data. The a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2; kappa = 1/2 FITTED) do not enter any quantity here; no gravity model is evaluated.

## 1. Data

- **KiDS isolated lenses (unchanged from the record):** `../_external_data/cfg502_work/cfg502_stage.npz` (CFG502's staging; its C5 reproduces `lr_lenses.npz` exactly). ALL = 605,531 lens candidates; ISO = `iso10` (W = 10 Mpc, 181,477 = stack P); f30 = `iso30` reported. Lensing weight per lens w_l = sum over the 15 bins of `WW` (CFG502's "stack-weighted" convention). The isolation itself is the record's: no pool galaxy with log M* > log M*_lens - 1 within 3 Mpc comoving transverse and |Delta chi_phot| < W; pool = KiDS-DR4 bright, r < 20, 0.1 < z_ANNz2 < 0.5, unmasked, log M* = LePhare MASS_MED + 0.15.
- **KiDS pool (for companions and completeness):** `real_research/data/lensing_rar/KiDS_DR4_brightsample(.fits, _LePhare.fits)`, the same pool definition as CFG502 (rebuilt by the same code lines; check C2).
- **GAMA DR4 G3C v10** (Robotham+11 group finder on the GAMA-II r < 19.8 equatorial sample): `G3CGalv10.csv` (CATAID, RA, Dec, Z, Rpetro, SURVEY_CODE, GroupID, RankIterCen, RankBCG; 204,110 rows) and `G3CFoFGroupv10.csv`, fetched for CFG471 from the Data Central TAP service (public; logged with SHA-256 in `CFG471_kids_split_gama_groups/FETCH_LOG.md`). They are copied to `../_external_data/cfg519_work/` and the script refuses to run unless both SHA-256 values equal CFG471's log (check C3). **No new download is needed for the frozen analysis**; any further fetch (owner-approved scope only: public GAMA DR4 / KiDS-bright tables) is logged in this lane's `FETCH_LOG.md` (URL, bytes, SHA-256, date, no home paths) and disclosed as a departure if it changes an input.
- **Footprint:** the three GAMA equatorial fields that lie inside KiDS-N: G09 129.0 < RA < 141.0, -2 < Dec < 3; G12 174.0 < RA < 186.0, -3 < Dec < 2; G15 211.5 < RA < 223.5, -2 < Dec < 3 (deg). G02 is outside KiDS; G23 is not in G3C v10. A lens is IN the overlap if its 0.5 Mpc comoving disc (radius 0.5 / chi_phot rad) lies inside a field box.
- **Match:** each KiDS galaxy (lens or pool) to the nearest G3CGal galaxy within 1.5 arcsec, one-to-one by nearest separation (a G3C galaxy claimed by two KiDS objects keeps the closer one).

## 2. Definitions

- **Satellite, primary (S_IC):** a matched lens that is a member of a G3C group (GroupID > 0) and is not its iterative centre (RankIterCen != 1). Ungrouped matched lenses (GroupID = 0) and iterative centres are centrals.
- Variants (reported; they enter only the systematic band of section 4): **S_BCG** (RankBCG != 1 instead of RankIterCen); **S_N3** (satellite only in groups with Nfof >= 3; a lower bound, reported, not in the band).
- **Spectroscopic pair satellite (S_pair, reported):** a matched lens with at least one more massive (KiDS log M*_j > log M*_lens) G3C-matched pool galaxy within R_p < 0.5 Mpc comoving (lens chi from its spec-z, H0 = 70, Om = 0.3, the record's DC) and |Delta v| < 1000 km/s (|z_j - z_l| < (1000 km/s / c)(1 + z_l)); chance-corrected with the 4-6 Mpc annulus rate lambda_bg per lens: f_pair = 1 - (1 - f_raw) / <exp(-lambda_bg)>.
- **Spectroscopic companion count (C_spec):** per matched lens, sum over G3C-matched pool galaxies j with log M*_j > log M*_lens, R_p < 0.5 Mpc comoving and |Delta v| < 1000 km/s of 1 / c(r_j, z_j), minus the same sum in the 4-6 Mpc annulus scaled by 0.25 / (20 a_ann), where a_ann = the fraction of the annulus area inside the field box (200 random points per lens, seed 519). c(r, z) = the completeness map of section 3. Cells with c < 0.1 contribute nothing; the share of the photometric companion excess lying in such cells (KiDS r and z_phot of the companion) is reported. Variant |Delta v| < 2000 km/s reported.
- **Photometric companion count on the same lenses (C_phot):** CFG502's `cin - can x 0.25 / 20` (10 < |Delta chi_phot| < 600 Mpc), read from the staging file, on exactly the lenses and weights used for C_spec.

## 3. Completeness and reweighting to the full stack P

- **Pool completeness map c(r, z):** fraction of KiDS pool galaxies inside the field boxes that have a G3C match, in bins of KiDS MAG_AUTO_CALIB r (0.1 mag, 14-20) x z_phot (0.05, 0.10-0.50). It absorbs GAMA's target selection (SDSS r_petro < 19.8), redshift failures and masks.
- **Lens cells:** log M* edges [8.5, 9.5, 10.0, 10.25, 10.5, 10.75, 11.0] x z_phot edges [0.1, 0.2, 0.3, 0.4, 0.5] x colour type typ (u - r > 2 early, the record's split) = 48 cells. In each cell the satellite fraction f_cell = sum(w_l S) / sum(w_l) over matched in-overlap ISO lenses. **Stack-weighted fraction f_obs = sum_cells W_cell f_cell / sum W_cell**, W_cell = the summed w_l of ALL 181,477 stack-P lenses in that cell (so f_obs refers to the whole stack P, as CFG502's and CFG506's numbers do). A cell with fewer than 20 matched lenses takes the fraction pooled over z for its (log M*, typ); if still < 20, pooled over typ too. Reported: the share of W in cells with >= 20 matched lenses, the matched fraction per cell, and the unreweighted matched-lens value f_raw.
- Same reweighting for C_spec and C_phot on the subset log M* >= 10.44 (CFG506's comparison subset; meas_sub = 0.205) and on all lenses (meas_all = 0.254).
- Also reported, by the same code: f for ALL (the parent, compare CFG502's f_par = 0.254 and CFG506's box parent fraction) and for f30; f_obs in each (log M*, z) cell; the ISO / ALL ratio at fixed cells (CFG502's model: 0.171 / 0.254 = 0.67).

## 4. Errors

- sigma_stat: delete-one jackknife over 12 sub-regions (each field cut into 4 equal RA strips of 3 deg), the whole pipeline (completeness map, cells, reweighting) redone per jackknife.
- sigma_sys = quadrature sum of (a) |f_obs(S_IC) - f_obs(S_BCG)| and (b) |f_obs - f_raw|. sigma_tot = sqrt(sigma_stat^2 + sigma_sys^2).
- C_spec uses sigma_stat only (jackknife), with the |Delta v| < 2000 variant reported.

## 5. Verdicts (frozen)

**V1, the leaked-satellite fraction.** For each reference X: CFG502 HOD 0.171, CFG503 0.181, CFG506 F 0.343, CFG506 P 0.432:
- CONSISTENT if |f_obs - X| <= 2 sigma_tot; EXCLUDED if |f_obs - X| > 3 sigma_tot; otherwise TENSION.
- **"CFG506's box galaxy-halo rule needs re-calibration"** iff X = 0.343 is EXCLUDED (and then the measured f_obs is the calibration target). **"CFG502/503's leaked-satellite input is confirmed"** iff X = 0.171 is CONSISTENT; if 0.171 is EXCLUDED, CFG502 / 503 / 504's E is built on a wrong leakage fraction and their verdicts carry the label "LEAKAGE INPUT CONTRADICTED".

**V2, the companion count (lenses log M* >= 10.44, stack-weighted).**
- C_spec / 0.313 (CFG506 F canonical prediction) in [0.67, 1.5] -> the box companion prediction is CONSISTENT with spectroscopy; otherwise NOT.
- C_spec vs C_phot on the same lenses: |C_spec - C_phot| <= 2 sigma (jackknife of the difference) -> "photometric excess = real companions" CONFIRMED; otherwise the photometric check of CFG502 / CFG506 is itself questioned, and that is reported next to CFG506's verdict.

## 6. Controls and MUTATE

- C1: ISO count 181,477 and stack-P weights equal the staging file (exact).
- C2: the rebuilt pool reproduces CFG502's pool (count; the ISO lenses' (ra, dec, z, logM) equal the staging file) exactly.
- C3: SHA-256 of both G3C files equals CFG471's FETCH_LOG (load-bearing; the script exits otherwise).
- C4: match quality: median separation of matched pool galaxies < 0.5 arcsec; |z_spec - z_phot| / (1 + z_spec): NMAD and the > 0.15 outlier fraction reported.
- **C5, representativeness of the GAMA area (load-bearing for the label):** the close-pair veto probability p_10 (CFG502's method: R_p < 0.3 Mpc, log M*_j > log M*_lens - 1, excess over the 4-6 Mpc annulus, |Delta chi_phot| < 10 over < 600 Mpc, z_l < 0.3) measured on ALL lenses inside the overlap vs outside it: if |p_10,GAMA - p_10,rest| > 0.02 the verdicts carry "GAMA-AREA PHOTO-Z NOT REPRESENTATIVE" (the ANNz2 photo-z were trained on spectroscopy that includes GAMA). The ISO pass fraction inside vs outside is reported.
- C6 (reported): the direct veto efficiency: among matched ALL lenses that are S_IC satellites whose iterative centre is a matched pool galaxy within 3 Mpc with log M* > log M*_lens - 1, the fraction whose |Delta chi_phot| to the centre is < 10 Mpc (compare CFG502's p_10 = 0.07 at z < 0.3).
- **MUTATE (CFG519_MUTATE=1; outputs `*_MUTATE.out`, `*_MUTATE.json`), both load-bearing:**
  - M1, shuffled redshifts: G3CGal Z values are permuted among G3C galaxies within each field (seed 519). C_spec and f_pair must collapse: |C_spec,mut| < max(3 sigma_jk, 0.2 C_spec,main) and |f_pair,mut| < max(3 sigma_jk, 0.2 f_pair,main). If they do not, the spectroscopic signal is not a real-space signal and V2 is void.
  - M2, displaced positions: every KiDS object's RA is shifted by +1.0 deg (wrapped inside its field box) before matching; the match rate of in-overlap ISO lenses must fall below 2% (chance matches), so S_IC is undefined and V1 cannot be computed. If it does not, the matching is not positional and V1 is void.
  - A MUTATE that fails to destroy its signal is reported as a failed control, next to every verdict.

## 7. Implication for CFG506 / 502 / 503 (rules, frozen)

- No CFG506 re-score is run in this lane: CFG506's per-box tables carry the companion count only as a total (no central / satellite split), so a re-weighting to f_obs is not cheap. If V1 says re-calibration is needed, the README specifies the follow-up lane (a galaxy-halo rule frozen to reproduce f_obs per (log M*, z) cell, then CFG506's frozen validation and re-score).
- If 0.171 is CONSISTENT, CFG502 / 503 / 504's environment term keeps its leakage input; their gate failures (where they failed) are then not caused by the leakage fraction. If it is EXCLUDED, the README states the direction and size of the change in E's leaked-satellite term (E's satellite part scales ~ f), as information only, not a re-score.

## 8. Wording and limits

kappa = 1/2 is FITTED; footings irrelevant here and never pooled anywhere. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". G3C is incomplete at z > 0.3 (GAMA's r < 19.8 sees only bright group members; FoF fragmentation) and has interlopers in small groups; S_N3 brackets the first. The reweighting assumes satellite status is independent of r magnitude at fixed (log M*, z, typ). nice -n 10, single thread; raw tables in `../_external_data/cfg519_work/`, never committed.
