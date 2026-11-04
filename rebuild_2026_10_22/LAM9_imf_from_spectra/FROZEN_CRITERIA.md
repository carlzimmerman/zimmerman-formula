# LAM9_imf_from_spectra: FROZEN CRITERIA, committed alone before any download, fit or regrade

κ = ½ FITTED and held fixed. Footings canonical a0 9.3603e-11 and alt a0 1.1312e-10 are graded apart and never pooled.
No ΛCDM input. The cold sector stays retired: no particle, no cold component and no halo is added. The IMF changes only
the stellar mass. Nothing here says the data favour the framework. Reinstates nothing. Not theory closed.

The owner asked to start this lane on 2026-11-04. The owner's notes called it LAM8. That ID was taken earlier the same day
by `LAM8_orbit_shape_resolved_sigma` (b9b94ead6d), so this lane is LAM9.

## Precondition: the owner approves this download
Nothing is fetched until the owner says yes to these exact files. Source: the MILES team's cloud storage at the Instituto de
Astrofísica de Canarias, linked as "MILES Cloud storage" on the MILES home page (https://research.iac.es/proyecto/miles/).
Public share https://cloud.iac.es/index.php/s/aYECNyEQfqgYwt4 ("MILES_FTP"). Each file is at
`https://cloud.iac.es/public.php/webdav/<path>`, with the share token as the user name and no password. Sizes are from the
share's WebDAV listing and HEAD requests on 2026-11-04. Apart from three short text headers read on screen (`HEADER_out_mass`,
`HEADER_out_phot` and the Na-enhanced models' `_README_`, 2.3 KB in all), no file was fetched.

| path in the share | bytes | what it is (from the MILES pages; contents not yet seen) |
|---|---|---|
| `E-MILES/EMILES_BASTI_BASE_BI_FITS.tar.gz` | 1,407,892,199 | E-MILES SSP spectra, BaSTI isochrones, base [α/Fe], bimodal IMF: 13 Γb (0.3-3.5) x 53 ages (0.03-14 Gyr) x 12 [M/H] (-2.27 to +0.40), 1680-50000 Å |
| `Photometric_predictions/out_mass_BI_BASTI` | 970,536 | stellar + remnant mass and M/L_V of each bimodal SSP |
| `Photometric_predictions/out_mass_CH_BASTI` | 69,324 | the same for a Chabrier IMF (KU2's mass reference) |
| `Photometric_predictions/out_mass_KU_BASTI` | 69,324 | the same for a Kroupa IMF (the Tian+2026 mass reference) |
| `Photometric_predictions/HEADER_out_mass` | 183 | column names of the three tables |
| **total** | **1,409,001,566** | 1.41 GB; 1092 of the tarball's expected 8268 spectra are used |

The tarball's member names are expected from the MILES naming page (for example `Ebi1.30Zp0.06T10.0000_iTp0.00_baseFe.fits`).
They are not seen before the download and are recorded in an amendment. Web reads are provisional.

The smallest official set is the Padova00 one: `E-MILES/EMILES_PADOVA00_BASE_BI_FITS.tar.gz` (756,891,568 B) with
`out_mass_BI_PADOVA00`, `out_mass_CH_PADOVA00`, `out_mass_KU_PADOVA00` and `HEADER_out_mass` (534,100 + 38,150 + 38,150 + 183 B),
757,502,151 B in all. It is not chosen. Its [M/H] grid stops at +0.22, where massive early types sit inside R_e, and a fit
pinned at a grid edge pushes extra metal-line strength into Γb. If the owner approves only this set, an amendment before any
fit switches to Padova00 ages 1.00-14.13 Gyr at about 0.1 dex and [M/H] -0.71, -0.40, 0.00, +0.22. Galaxies whose light-weighted
[M/H] is within 0.05 of +0.22 are then counted and reported.

## Question
Does a spectroscopic IMF remove the law's early-type excess? Does LAM6's h4 lean survive once the IMF is fixed?
- **Q1.** Does KU2's absolute residual at r_half shrink when M★ carries each galaxy's measured IMF? KU1 found +1.2 to +1.4 ln,
  uncalibrated.
- **Q2.** HX1 found that MaNGA ellipticals need B 3-4 inside R_e. Does that need go away?
- **Q3.** Does LAM6's h4 lean (E +0.040 / +0.042 ln, NO VERDICT) survive with IMF-corrected masses?

## Method
- Fit a bimodal IMF slope Γb (Gamma_b) to each half-light sum from LAM4 and LAM7. The fit uses pPXF 9.5.2 and the E-MILES
  variable-IMF SSPs above.
- The IMF-sensitive features are Na I 8190, the Ca II triplet (CaT) and TiO. The blue part of the spectrum pins age and
  metallicity.
- Turn each fit into an IMF mass factor α: M★/L at the fitted IMF over M★/L at Γb 1.3, for the same light.
- Test recovery on synthetic sums at the real S/N first (K1).
- Then regrade KU2's residual, HX1's MaNGA need and LAM6's statistic with M★ x α.

## Not blind
- KU1 and KU2 on all 6056 galaxies: absolute median residual +1.176 (fast) and +1.402 (slow) ln canonical, +1.113 and
  +1.348 alt. KU2's D is +0.023 / +0.025 (UNIVERSAL).
- HX1's MaNGA rungs, median B_need by σ quartile: 1.95, 3.15, 3.55, 4.22 canonical and 1.72, 2.79, 3.15, 3.73 alt. HX1's
  result is NO LADDER, and its reading named the IMF as a possible cause of the MaNGA need.
- LAM6 on 963 galaxies: E +0.040 [-0.008, +0.093] canonical and +0.042 [-0.003, +0.096] alt.
- LAM7 failed its K1. I have seen LAM8's MUTATE output, which uses shuffled h4. I have not seen a real LAM7 or LAM8 effect.
- The stage-0 numbers below, and a software timing of pPXF on random templates (no data).
- Not seen: any Γb, any IMF-sensitive index, any residual on the graded sample, any variable-IMF model spectrum.
- Q3 is graded on a sample that includes LAM4's galaxies, so it is not independent of LAM6's look. Its question is the IMF's
  effect on the lean, not a new detection of it.

## Stage 0 (`lam9_stage0.py`, reads only; 44 s, 0.3 GB; committed right after this file)
- **Record.** No lane on record has fit an IMF or used Na I, CaT or TiO. pPXF appears only in the LAM kinematic fits. The IMF
  enters the record only as posits:
  - CFG926 R5, S2 O7 and CFG928 use an ATLAS3D JAM α-σ relation.
  - XR33 (F44) uses Conroy & van Dokkum 2012's spectroscopic α on SLACS.
  - SG1 bounds the IMF by M_JAM on SLUGGS.
  - DF1 uses F ≤ 2 in dwarfs.
  - CFG528 uses "2x Chabrier".
- **On-disk templates.** `spectra_emiles_9.0.npz` is E-MILES with Padova isochrones and a Salpeter IMF (pPXF's data README,
  read verbatim). It has 25 ages (0.063-15.85 Gyr) x 6 [M/H] (-1.71 to +0.22) over 1680-50000 Å. FWHM is 2.51 Å from 3540
  to 8950 Å and σ 60 km/s beyond. It has one IMF, so it cannot fit Γb.
- **Sums.** All 6056 KU2 galaxies have a sum (1000 from LAM4, 5056 from LAM7). z median 0.040, 5-95 % 0.021-0.102, max 0.150.
- **Coverage.** The sums end at 10,354 Å observed. Every sum covers rest Na I 8143-8244 Å and CaT 8474-8792 Å, and every sum
  reaches 8900 Å rest. 98.5 % have both windows with fewer than 20 % bad pixels.
- **S/N per rest-frame Å, formal, median (5-95 %), all 6056** (sums with under 20 % bad pixels in the window). Na I 93
  (40-215), CaT 85 (34-196), TiO2sdss 101 (44-212), V band 85 (39-186).
- **S/N on the candidate sample** (fibre gas-poor, Σ_Re ≥ 100 km/s). Na I 110 (58-232), CaT 100 (40-208).
- **The formal noise is low.** The LAM4/LAM7 kinematic fits have χ² median 2.41 (5-95 % 1.25-7.55), so the formal noise is
  low by about 1.55x. Scaled by sqrt(χ²), the candidate's Na I S/N is 72 and its CaT S/N is 66.
- **Sky and telluric residuals.** These come from an observed-frame stack of all 6056 sums. Each sum is divided by its 101-pixel
  running median, the median is taken over galaxies, and the stack's own 21-pixel running median is subtracted.
  - Residual rms by observed band: 0.18 % at 4000-5500 Å, 0.21 % at 8100-8600, 0.78 % at 8600-9100, 3.0 % at 9100-9600 and
    22 % at 9600-10300 Å.
  - Candidate Na I window: rms 0.32 %. It is 0.15-0.33 % for z ≤ 0.063 and 0.96 % above. 11 % of its pixels sit on OH
    noise spikes.
  - Candidate CaT window: rms 0.96 %. It is 0.75-0.96 % for z ≤ 0.063 and 3.3 % above. A median 83 % of CaT pixels fall in
    the nominal water bands. 16 % carry a coherent residual above 1 %, and 16 % sit on OH spikes.
  - TiO windows: 0.3-0.7 %. TiO1 meets the 6300 Å [O I] sky line.
  - For scale, going from Γb 1.3 to 3 deepens Na I 8190 by about 1-2 % of the continuum in the literature models. That figure
    is from memory and provisional; K1 measures the real sensitivity.
- **Candidate sample.** 2526 galaxies, 432 slow. Median z 0.049; 1690 are at z ≤ 0.063.
- **Tian+2026 MaNGA ellipticals.** 1218 rows (1206 objects). 922 are in KU2's sample, all with sums. Candidate-sample rows by
  HX1's σ quartile are 165, 232, 238 and 185, so 655 are in Q2-Q4.
- **Mass units** (inputs, not graded).
  - log L_MGE - log L_r (NSA elpetro absmag as stored) has median +0.257 (16-84 % +0.198, +0.303).
  - log M★,NSA (as stored) - log L_MGE has median -0.017. That is an r-band M★/L near 1, below any old population.
  - Both point to NSA's h = 1 units, which would add 0.31 dex at h 0.7. LAM2 assumed this; KU1 left it open.
  - KU2's convention is kept for the graded lines, and the h70 reading is a row.
  - Tian logMbar - NSA elpetro (as stored) has median +0.575 on the 922 shared galaxies.

## Graded sample
1. KU2's 6056 galaxies, from `ku2.py`'s selection exactly, each with its half-light sum.
2. Fibre gas-poor: MPA-JHU -h_alpha_eqw < 3 Å (LAM2 A1's sign). Galaxies without a galSpecLine row are excluded and counted.
3. KU2's Σ_Re ≥ 100 km/s, the resolution cut of LAM2, LAM4 and LAM8.
4. The LAM4/LAM7 kinematic fit is ok, with σ_int > 0 and |h4| < 0.3.
5. After variant A's masks (below), at least 70 % of the Na I 8190 feature pixels (8180-8200 Å rest) and at least 70 % of the TiO2sdss
   feature pixels (6189-6272 Å) are left.
6. The variant-A fit returns without error.

Stage 0 counts 2526 galaxies (432 slow) after steps 1-4. Exclusions are counted at every step.

## Templates (after the download)
- **Grid.** All 13 bimodal slopes: Γb 0.3, 0.5, 0.8, 1.3, 1.5, 1.8, 2.0, 2.3, 2.5, 2.8, 3.0, 3.3, 3.5.
- **Ages.** 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 10.00, 12.00 and 14.00 Gyr. 14 Gyr is the BaSTI
  grid's end, not a cosmology prior.
- **[M/H].** -0.96, -0.66, -0.35, +0.06, +0.26, +0.40.
- That gives 1092 spectra (BaSTI, base [α/Fe], `iTp0.00_baseFe`). The amendment records their names, count and sha256.
- **Masses.** Stellar + remnant mass per M_sun formed, from `out_mass_BI_BASTI`.
- **Wavelengths.** MILES stores air wavelengths. The sums stay in vacuum, as in LAM4. The ~83 km/s offset sits in the fixed V.
  Its 2.5 km/s drift over 3900-8900 Å is ignored.
- **Preparation.** Each spectrum is cut to 3500-9400 Å rest, then broadened per sum to the sum's rest LSF (2.355 σ_LSF / (1+z))
  with pPXF's `varsmooth`. Where the sum is sharper, the broadening is clipped at zero. The spectra are log-rebinned to 69.03
  km/s (c ln10 1e-4, the MaNGA step) and normalised to mean 1 over 5070-5950 Å. The weights are therefore V-band light
  weights, as in LAM2 and LAM4.

## Fit window and masks
- **Rest window.** It starts at the first λ ≥ 3900 Å where the sum's rest FWHM is at least 2.51 Å (LAM4's rule). It ends at
  8900 Å; E-MILES keeps FWHM 2.51 Å up to 8950 Å.
- **IMF-sensitive features**, fitted as part of the full window and not as indices:
  - Na I 8190: feature 8180-8200 Å, continua 8143-8153 and 8233-8244 (La Barbera et al. 2013, NaI8190sdss).
  - CaT: 8484-8513, 8522-8562 and 8642-8682 Å, continua 8474-8484, 8563-8577, 8619-8642, 8700-8725 and 8776-8792
    (Cenarro et al. 2001).
  - TiO1: 5936-5994 Å, continua 5816-5849 and 6038-6103 (Trager et al. 1998).
  - TiO2sdss: 6189-6272 Å, continua 6066-6141 and 6422-6455 (La Barbera et al. 2013).
- **Masks** (rest frame unless stated):
  - m1: the sum's bad pixels, var ≤ 0 and non-finite flux.
  - m2: pPXF's standard emission-line mask (`determine_goodpixels`, as in LAM4).
  - m3: observed 5577.3 ± 5 Å and 6300.3 ± 5 Å (LAM4).
  - m4, OH lines: pixels where the sum's noise exceeds 1.5x its own 51-pixel running median, grown by ±1 pixel.
  - m5, coherent sky and telluric residuals: observed pixels where the all-sums stack has |s| > 0.01, grown by ±1 pixel. The
    stack is built exactly as `lam9_stage0.py` builds it, and the fit script rebuilds it.
  - m6: Na D 5880-5910 Å, for interstellar absorption.
  - m7: the E-MILES library joins at 7395-7425 and 8335-8365 Å. These ranges are provisional; the template amendment checks
    them against Vazdekis et al. 2016.
- **Variant A** (primary): masks m1-m7.
- **Variant B** (the Na test): A plus 8143-8244 Å masked. It fits the same galaxies as A.

## The Γb fit
One fit per sum and variant. There are no refits, and failures are counted.
- pPXF 9.5.2, single thread.
- The kinematics are fixed at the sum's LAM4 or LAM7 values: V, σ and h3-h6, moments 6, `fixed=[1]*6`.
- `clean=False`, because clipping could remove the IMF lines themselves.
- **Step a.** degree -1, mdegree 10, regul 0. The multiplicative polynomial is kept. pPXF's χ²/DOF from this step, χ²_a,
  scales the noise for step b.
- **Step b.** The sum and its noise are divided by step a's polynomial, and the noise is multiplied by sqrt(χ²_a). Then
  degree -1, mdegree 0, regul 100, reg_dim (14, 6, 13), reg_ord 2 and pPXF's default reg_step.
- **Outputs.**
  - The light weights w (1092 of them).
  - Γ̄b = Σ w Γb / Σ w, and the light-weighted log age and [M/H].
  - The edge share: the weight at Γb 0.3 or 3.5.
  - χ²_a.
  - Step a's unregularised Γ̄b, as a row.

## From Γb to M★/L
- **Per template t.** Υ_r,t = M(*+remn)_t / L_r,t. L_r,t comes from the native spectrum through pPXF's
  `synthetic_photometry` (band "SDSS/r", z = 0), in solar units from pPXF's solar spectrum, as `sps_lib.mass_to_light`
  does.
- **r-band light of each template in the fit.** ℓ_t = (w_t / n_t) L_r,t, where n_t is the template's V normalisation.
- **α** = Σ ℓ_t Υ_r,t / Σ ℓ_t Υ_r(age_t, [M/H]_t, Γb 1.3). The light stays the same and only the IMF changes.
- **IMF references.**
  - KU2's M★ are NSA kcorrect masses, which assume a Chabrier 2003 IMF.
  - Tian+2026's masses assume Kroupa 2001. This is from arXiv 2605.26965 HTML v1 and v2, read through a summariser, so it is
    provisional.
  - α_KU2 = α x Υ_V(BI 1.3) / Υ_V(CH) and α_Tian = α x Υ_V(BI 1.3) / Υ_V(KU). Both ratios come from the `out_mass` tables'
    M(*+remn)/L_V at the grid point nearest the galaxy's light-weighted age and [M/H].
- **KU2.** M★ becomes α_KU2 M★.
- **HX1, primary.** Mbar becomes α_Tian Mbar. Scaling the whole baryonic mass is an upper bound on the IMF's effect.
- **HX1, variant.** α_Tian is applied to 0.92 Mbar and 0.08 Mbar is held fixed. The 0.08 is the paper's median hot-gas share
  (provisional).

## K1: recovery at the sums' S/N (run and read before any regrade)
- **Synthetics.** 300 synthetic sums, 100 in each third of the graded sample's χ²_a-scaled Na I S/N. Donors are drawn at random
  from the graded sample (seed 20261105). Γb_in is drawn uniformly from the grid values 0.8-3.3, which are ten values.
- **Build.**
  - Take the donor's variant-A light weights, sum them over Γb and place them at Γb_in.
  - Convolve with the donor's fixed LOSVD and multiply by its step-a polynomial.
  - Multiply by (1 + s), where s is the stack residual at the donor's observed wavelengths.
  - Add Gaussian noise from the donor's noise vector x sqrt(max(χ²_a, 1)), LAM4 A1's rule with the donor's own χ²_a.
- The true α_in comes from the injected weights by the α rule.
- Each synthetic is fitted with the frozen pipeline in both variants.
- **K1 PASS (variant A)** needs all four lines:
  - |median(Γ̄b,out - Γb,in)| ≤ 0.15;
  - rms(Γ̄b,out - Γb,in) ≤ 0.40;
  - |median(log α_out - log α_in)| ≤ 0.03 dex;
  - rms(log α_out - log α_in) ≤ 0.10 dex.
- **Where the lines come from.**
  - 0.10 dex is the stellar-mass systematic that HX1 and RQ3's B1 already carry.
  - A 0.03 dex bias moves r by 0.05 ln, a third of Q1's 0.15 ln line. It moves HX1's MaNGA y by 0.02-0.03, about a third of
    a rung error (HX1's own ±0.10 dex rows give dy / dlog M of 0.75-1.13).
  - 0.15 and 0.40 in Γb are about half a grid step and one and a half grid steps.
- **If K1 fails,** every label is NOT MEASURABLE.
- **Variant B** is judged by the same lines. If B fails, A's labels carry "(Na I robustness not tested)".
- **Reported:** results by S/N third and z third, and the slope of Γ̄b,out on Γb,in.

## K2: h4 leak (gates Q3)
- The first 100 synthetics are refitted with h4 fixed at the true value ± 0.03.
- b = median of [log α(+0.03) - log α(-0.03)] / 0.06.
- K2 PASSES if 0.69 ln(10) |b| IQR(h4_int) ≤ 0.01 ln, where the IQR is over the graded sample. That is the lean this leak alone
  could make in E.
- If K2 fails, Q3 is NOT MEASURABLE.

## K3: reported, not a gate
The Spearman correlation of Γ̄b with log Σ_Re on the graded sample, with its p-value. The literature trend is positive. A null
here would point to an insensitive fit, and is stated next to the labels.

## Checks
- **C1.** The graded N is at least 1000 for Q1 and Q3. Q2 needs at least 150 Tian rows in Q2-Q4. Otherwise that question is
  NOT MEASURABLE.
- **C2.** KU2's D is reproduced on KU2's full sample to 1e-6 on both footings, as in LAM6 and LAM7.
- **C3.** With α ≡ 1, R1 = R0, E1 = E0 and y1 = y0 exactly. HX1's four MaNGA rung medians (`Bmed`), on all 1218 rows, match
  `hx1_ladder.json` to 1e-6 on both footings.
- **C4.** The M/L code reproduces the Johnson-Cousins V M(*+remn)/L_V of five templates to within 3 % of
  `out_mass_BI_BASTI`. The five are Γb 0.8, 1.3, 2.3 and 3.3 at 12 Gyr and [M/H] +0.06, and Γb 1.3 at 2 Gyr and +0.06.
- If C2, C3 or C4 fails, every question gets NO VERDICT, because the code is wrong.

## Q1: KU2's absolute residual
- **Residual.** r is KU2's residual at r_half, computed exactly as `ku2.py` does it:
  - the JAM model chosen by lowest chi2_dof;
  - g_obs = G M_t(r_half) / r_half²;
  - g_bar = G 0.5 M★ / r_half²;
  - simple ν;
  - NSA elpetro masses as stored;
  - KU2's low-z distances at H0 70.
- **Statistic.**
  - R0 = median r over the graded sample.
  - R1 = median r with α_KU2 M★.
  - f = (R0 - R1) / R0.
  - 95 % intervals come from 2000 bootstrap draws over galaxies (seed 20261105), with R0, R1 and f taken from the same
    draws.
- **Lines, per footing:**
  - **IMF ABSORBS:** R1's interval lies inside ±0.15 ln.
  - **IMF OVERSHOOTS:** R1's interval lies below -0.15 ln.
  - **IMF DOESN'T:** f's interval lies below 0.5.
  - **IMF PARTLY:** f's interval lies above 0.5, and the label is neither ABSORBS nor OVERSHOOTS.
  - Otherwise **NO VERDICT**.
  - If R0's interval itself lies inside ±0.15 ln, there is nothing to absorb, and the label is NO VERDICT.
- **The 0.15 ln line** is HX1's ±0.10 dex mass systematic carried through the law's slope. At KU2's median y the slope
  d ln g_law / d ln g_bar is 0.687 canonical and 0.672 alt, which gives 0.16 ln.
- **Known before the fit** (simple ν at KU2's median y):
  - Removing KU2's +1.18 to +1.40 ln needs α 4.7-6.2 (log α 0.68-0.79 dex) canonical and 4.5-6.0 alt.
  - Reading the NSA units as h70 would lower r by 0.50-0.51 ln on its own.

## Q2: HX1's MaNGA need
- **Code.** HX1's B1 integral exactly. `hx1_ladder.py`'s source is run in memory up to its SLUGGS block, the way LAM6 runs
  `ku2.py`. The only change sends its output handle to memory, so no HX1 file is written. If HX1's harness writes caches, it
  runs on a temporary copy of HX1's folder.
- **Rows.** Every Tian catalogue row (all rows, as HX1 counts them) whose galaxy is in the graded sample and whose σ is above
  HX1's first quartile edge, 143.8 km/s. The edges come from all 1218 rows. Stage 0 counts 655 such rows before the fit cuts.
- **Statistic.**
  - y0 = log10 median B_need with Tian's Mbar.
  - y1 = the same with α_Tian Mbar.
  - s0 and s1 follow HX1's rung error rule. The half-width of the 16-84 % interval of y over 2000 bootstrap draws is combined
    in quadrature with |y(+0.10 dex) - y(-0.10 dex)| / 2, B1's mass systematic. Seed 20261105.
- **Lines, per footing:**
  - **NO NEED ON THIS SUBSET:** y0 ≤ 2 s0. No other label is then given.
  - **IMF ABSORBS:** |y1| ≤ 2 s1, and this also holds with α_Tian on 0.92 Mbar only.
  - **IMF OVERSHOOTS:** y1 < -2 s1.
  - **IMF DOESN'T:** y1 > 2 s1 and y1 ≥ 0.5 y0.
  - **IMF PARTLY:** y1 > 2 s1 and y1 < 0.5 y0.
  - Otherwise **NO VERDICT**.
- |Z| ≤ 2 is HX1's own tolerance line.

## Q3: LAM6's h4 lean at fixed IMF
- **Statistic.** LAM6's statistic exactly. E is the OLS slope of within-group demeaned r on demeaned h4_int, times
  IQR(h4_int) over the graded sample. Groups are KU2 cell x class, with at least 3 galaxies. h4_int comes from
  `lam4_fit.jsonl` and `lam7_fit.jsonl`.
- E0 uses KU2's r, and E1 uses r at α_KU2 M★. ΔE = E1 - E0.
- One set of 2000 bootstrap draws over galaxies (seed 20261105) gives all three intervals. Groups are re-demeaned in each draw,
  and the IQR is held fixed.
- **Lines, per footing, applied in this order:**
  1. **IMF DOESN'T:** ΔE's interval lies inside ±0.01 ln. The IMF then moves the statistic by less than a quarter of LAM6's
     +0.040.
  2. **IMF ABSORBS:** E0's interval excludes 0, E1's includes 0, and ΔE's excludes 0 with the sign opposite to E0.
  3. **IMF DOESN'T:** E1's interval excludes 0 with the sign of E0. The lean survives the IMF.
  4. Otherwise **NO VERDICT**.
- Q3 is NOT MEASURABLE if K2 fails, and NO VERDICT if M1 fails.

## Variant B, the Na I test
All three questions are graded again with variant B's α. If A and B agree, the label stands. If they disagree, A's label
carries "(NOT ROBUST TO Na I)".

## M1 MUTATE twin
- α is shuffled within groups: KU2 cell x class for Q1 and Q3, and HX1 σ quartile for Q2. Seed 20261105.
- Outputs are `lam9_grade_MUTATE.out` and `lam9_grade_MUTATE.json`.
- For Q3, ΔE's 95 % interval must include 0 on both footings. Otherwise Q3 is NO VERDICT.
- Q1 and Q2 under MUTATE are reported only. A within-group shuffle keeps their medians close to the real ones by
  construction, so it is not their null. Their null is α ≡ 1 (C3).

## Labels
- Each question gets one label per footing: IMF ABSORBS, IMF PARTLY, IMF DOESN'T, IMF OVERSHOOTS, NO VERDICT or NOT
  MEASURABLE. Q2 can also be NO NEED ON THIS SUBSET.
- The owner's three labels (IMF ABSORBS, IMF DOESN'T, NOT MEASURABLE) are kept. PARTLY and OVERSHOOTS name the two outcomes
  those three do not cover.
- Order: a C2, C3 or C4 failure gives NO VERDICT. A K1 or C1 failure gives NOT MEASURABLE (for Q3, so does K2). Then the lines
  apply.
- A label printed before K1, K2 or M1 has run is marked PROVISIONAL.

## Rows (reported, not graded)
- **Q1 variants.**
  - Q1 with the h70 reading of NSA masses (+0.310 dex, LAM2's conversion), with the same lines.
  - Q1 for slow and fast galaxies apart.
  - KU2's D recomputed with α: slow - fast at matched cells.
- **Early-type excess without the calibration.** This uses KU2's D statistic with gas-poor against gas-bearing (σ ≥ 100)
  galaxies in place of slow against fast, at matched cells. It is computed before and after α is applied on the gas-poor side.
  The gas-bearing side is kept at α = 1, which is an assumption.
- **Q2 detail.**
  - Each of HX1's four MaNGA quartile rungs before and after.
  - HX1's L-ORDER recomputed with the four MaNGA rungs replaced by their IMF-corrected values on this subset. All other rungs
    come from `hx1_ladder.json`.
  - X-COP's L-FLAT failure does not involve stars, so no IMF touches it.
- **Q3 detail.**
  - Q3 with log α as a second covariate, using a joint within-group OLS of r on h4 and log α.
  - Q3 within slow and within fast galaxies.
  - Q3 by S/N third.
- **Γb detail.**
  - Γ̄b against log Σ_Re, log M★, h4_int, light-weighted age and [M/H].
  - The edge share.
  - The mean fit residual (data - model) in each IMF window, in the rest frame.
  - All by z third (≤ 0.037, 0.037-0.063, above 0.063). Stage 0 shows that CaT and Na I degrade above z 0.063.
- **Unregularised results.** Step a's Γb and α.

## Compute plan
- **Download, after the yes.** curl with resume into a new, empty `_external_data/lam9_emiles_bi_basti/`.
  - Sizes are checked against this file, and sha256 sums go into an amendment.
  - The tar members are listed first. Then a lane script extracts only the 1092 members it needs. It runs with `python3 -I`
    and takes paths as arguments, because downloaded data are untrusted.
  - One npz of about 60 MB (float32) holds the templates, masses, L_r, L_V and grid axes. The tarball is kept.
- **`lam9_fit.py`.** For each graded sum, it broadens the templates, then runs step a and step b for A and then B.
  - It writes one JSON line per sum and variant to `lam9_fit_A.jsonl` and `lam9_fit_B.jsonl`, flushed and fsync'd. On resume a
    torn last line is dropped.
  - SIGTERM sets a flag, and the script exits 75 at the next sum boundary. `--resume` skips finished sums and exits 0 once
    complete.
  - Single thread (OMP and BLAS at 1), `nice -n 10`, queued with `compute_queue/heavyq.py` at est_gb 1.0.
- **`lam9_k.py`.** K1 and K2: 300 synthetics in both variants plus 200 leak refits. Same contract. It writes `lam9_k.jsonl`,
  `.out` and `.json`.
- **`lam9_grade.py [MUTATE]`.** Takes minutes. It writes `lam9_grade.out/.json`, `lam9_grade_B.out/.json` and
  `lam9_grade_MUTATE.out/.json`.
- **Memory.** A timing run of pPXF on random templates of this size (1092 templates, 3550 pixels, no data) peaked at a 0.43 GB
  footprint. The fit should stay under 1 GB.
- **Wall time.**
  - In that timing run, step a took 5.3 s and step b 0.6 s.
  - With about 2 s of broadening, that is about 13 s per sum for both variants.
  - So about 9 h for about 2500 sums, 1.5 h for K, and minutes for grading: about 11 h of one core.
- **Order.** Scripts are committed before any fit. K1 and K2 are run and read before any regrade. LAM7's process and files are
  never touched; this lane reads its outputs only.

## Expectations on record (priors, before any number)
| | prior |
|---|---|
| K1 passes, variant A | 55 % |
| Q1 IMF DOESN'T on both footings | 85 %. It needs log α of about 0.7 dex. Literature IMF fits of massive early types reach about +0.2 to +0.4 dex over Kroupa (from memory) |
| Q2 IMF DOESN'T | 50 %. HX1's own mass rows suggest Q4 needs α near 3 to reach B = 1 (a rough reading, not a fit) |
| Q2 IMF ABSORBS or PARTLY | 40 % |
| Q2 IMF OVERSHOOTS | 5 % |
| Q3 IMF DOESN'T | 60 % |
| A and B agree on all three questions | 50 % |

## Limits
- **[Na/Fe].** The base E-MILES models do not vary [Na/Fe]. Massive early types are Na-enhanced, and a fit driven by Na I
  reads that as a heavier IMF. Variant B tests this. Na-enhanced E-MILES models ([Na/Fe] +0.3 to +1.2, Padova00 only, about
  635 MB per step) are on the same share. They are not requested.
- **CaT.** Above z 0.05 most sums have CaT in the water bands, and CaT is weak in Γb. It is fitted but not relied on.
- **Aperture.** The IMF is an average inside the half-light ellipse, while r_half is JAM's 3D half-light radius. IMF gradients
  are not modelled.
- **Gas.** The gas flag is from the fibre. Any emission inside R_e is handled only by pPXF's line mask.
- **Calibration.** KU2's absolute level stays uncalibrated: NSA's h units, kcorrect masses and sphere-enclosed JAM mass. Q1
  says only how much of that level an IMF can carry.
- **Tian's masses.** The paper names only SED fitting with a Kroupa IMF (provisional).
- **Scope.** No lens, cluster or dwarf enters. No a0 or κ is refitted.

## Literature (provisional; not read for this file)
- Tortora et al. 2014 (ATLAS3D) and Parikh et al. 2018 (MaNGA) cover parts of this question.
- Models: Vazdekis et al. 1996 (the bimodal IMF) and Vazdekis et al. 2016 (E-MILES).
- Indices: La Barbera et al. 2013 (NaI8190sdss, TiO2sdss), Cenarro et al. 2001 (CaT) and Trager et al. 1998 (TiO1).
- Spectroscopic IMFs: Conroy & van Dokkum 2012.

κ = ½ FITTED; not theory closed.
