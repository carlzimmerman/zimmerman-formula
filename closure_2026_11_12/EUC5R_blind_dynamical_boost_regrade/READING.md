# EUC5R (BLIND RE-GRADE OF EUC5, DYNAMICAL BOOST): READING

2026-11-12. Committed alone, before any EUC5R script exists and before any number of this lane is computed.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², never pooled. Not "theory closed". No outcome
here is a pass of the theory; a favourable result stays "a reading". This lane does not relabel EUC5.

## 0. Blindness disclosure

Read of EUC5 before this file: `FROZEN_CRITERIA.md` and `AMENDMENT_A1.md` only. Nothing else in that folder has been
opened, listed by content, grepped or diffed. No EUC5 git log message or `git show` has been read. No memory file and
no EUC3, EUC6 or EUC7 result has been read. EUC1's `FROZEN_CRITERIA.md` and `RESULT.md` sections 1-6 were read (to
section 7, not including it). EUC2's `FROZEN_CRITERIA.md` lines on extension lenses, its `AMENDMENT_A1.md` and the
header and counts of `euc2_matches.csv` were read (A1.1 names that file). A55's and A85's scripts were read for their
SLACS conventions (loader, cosmology, `ReV`, Fs × Mass stellar normalisation); nothing is imported from them.

What the lead told me, verbatim: "EUC5 ended NOT EVALUABLE on its frozen route because too few lenses have an SDSS/BOSS
pipeline dispersion, and NOT EVALUABLE on its amended route A1 (dispersions fitted to public DESI spectra) because its
fitter failed its own mock-recovery gate by several per cent. Afterwards, post hoc, it calibrated its fits against real
spectra of SLACS lenses. The lead knows EUC5's numbers and has not passed any of them to me."

Also seen, inside the allowed file `AMENDMENT_A1.md`: the frozen run had 7 lenses of P with an SDSS dispersion
(against 30); EUC5's SDSS readings were 16 lenses with `b_dyn` median +0.05 / +0.04 and 9 of 16 below their lensing
bound; EUC2 had 382 DESI spectra of 369 lenses, 39 lenses of P.

## 1. Reading of the criteria

**Statistic.** Per lens, `b_dyn` = log₁₀ B where B multiplies the catalogued Salpeter stellar mass (total mass B·M★ in
the spherical Sérsic body) so that the model's luminosity-weighted line-of-sight second moment in the fibre equals the
measured dispersion. Search range B ∈ [10^-1.5, 10^+1.5]; a lens at an end is kept at the end and counted.
`b_med` = median over lenses, 95 % percentile bootstrap interval (2,000 resamples of lenses, seed 20261112).

**Samples.** P = EUC1 §2: grade A, `lens_model_success`, `final_sample`, not `large_system_warning`,
`eclipse_effective_einstein_radius > 0`, `eclipse_effective_radius > 0`, 0.6 ≤ n ≤ 10, `eclipse_median_phz > 0`,
`eclipse_log_survived_mass_med > 0`. S = the same with grades A and B. Recomputed by me from the two catalogue files.

**Model.** Prugniel-Simien deprojection of the catalogue Sérsic (n, R_e = θ_e·D_A), total mass B·M★; tracer = the same
profile (light traces stars); no gas, halo, neighbours, external field. Law S `g = ½ g_N (1 + √(1 + 4a₀/g_N))`
(headline), law B `g² = g_N² + a₀ g_N` (reported). Spherical Jeans, constant β; β = 0 headline, β = ±0.2 variants.
Observable: luminosity-weighted second moment through a circular fibre after a Gaussian PSF.
Cosmology flat, H₀ = 67.74, Ω_m = 0.3089 for ECLIPSE lenses.

**Route frozen (SDSS/BOSS pipeline `veldisp`).** I cannot run it: the SDSS rows are not on disk outside EUC5's folder
and archive queries are not allowed in this lane. Its word is not re-graded here; A1's text records N = 7 < 30, which
by §3 is NOT EVALUABLE. I state that as read, not recomputed.

**Route A1 (DESI DR1 spectra).**
- Spectra: rows of `euc2_matches.csv` that are flagged (catalogue `desi_deflector_specz`) or extension rows whose DESI
  redshift (warning 0) lies in the photo-z 70 % interval widened by 0.1 (EUC2 §3's definition of a deflector
  spectrum), for lenses of S, spectrum on disk. One per lens: the primary, else the one with the smaller fitted error.
- Deflector redshift: the catalogue `desi_deflector_specz` for flagged lenses, the DESI redshift for extension lenses.
  M★ rescaled by (D_L(z_spec)/D_L(z_phot))²; R_e, R_E and the fibre converted at z_spec.
- Fit (pPXF 9.5.2): moments (V, σ); 84 E-MILES BaSTI templates, bimodal Γ = 1.30, 14 ages × 6 metallicities; rest
  3750-5600 Å inside observed 3650-9700 Å; log-rebinned; additive Legendre degree 8, mdegree 0; noise 1/√ivar.
  Masks: ivar ≤ 0 or any mask bit; ±10 Å rest around [O II] 3727/3730, [Ne III] 3870, Hδ, Hγ, Hβ, [O III] 4960/5008;
  observed 5570-5590, 6290-6310, 6860-6960, 7590-7700 Å. One pass of 3σ clipping of the residuals, then one refit.
  σ² = σ_fit² + σ_tpl² − σ_inst² in km/s at the mean rest wavelength of the fitted pixels; σ_tpl from FWHM 2.51 Å;
  σ_inst = `wave_sigma` (Å, DESI) at the observed mean wavelength, divided by (1+z), in km/s.
  Error = formal × √max(χ²/dof, 1).
- Quality: σ ∈ [70, 500] km/s, err/σ ≤ 0.25, |V| ≤ 300 km/s, ≥ 800 unmasked pixels.
- Aperture: DESI fibre radius 0.75″, seeing FWHM 1.1″ headline, 0.9″ and 1.3″ variants.
- Gates: F1 (mock recovery, below) is a gate; F2 (DESI vs SDSS pipeline, ≥ 5 pairs: median ratio in 0.85-1.15) is a
  gate; J1-J3 are gates. F3 (repeat spectra) reported.

**Words, per footing, law S, β = 0, sample P, labelled "under A1".** DYNAMICAL GATE HOLDS if the upper 95 % bound of
`b_med` ≤ 0.15; DYNAMICAL GATE FAILS if the lower bound ≥ 0.25; NO VERDICT otherwise. NO VERDICT if the word moves among
β ∈ {−0.2, 0, +0.2} or seeing ∈ {0.9, 1.1, 1.3}″. NOT EVALUABLE if N < 30, or F1, F2 or J1-J3 fail.
Reported beside, no word: sample S; law B; b_dyn by Einstein-radius class (frozen four: < 1.0, 1.0-1.3, 1.3-1.7,
> 1.7″; plus the lead's three: < 1.0, 1.0-1.3, > 1.3″); `b_dyn − b∞` (median, fraction < −0.25); the conditional source
redshift where b_lens(z_s) = b_dyn (median, fraction with no solution), labelled CONDITIONAL.

## 2. Ambiguities and how I resolve them (fixed now)

1. **F1 mock construction.** A1 says "a 10 Gyr solar template broadened to σ_in ... with that spectrum's resolution".
   I read the input as a galaxy whose true dispersion is σ_in observed through DESI's LSF. The template already carries
   the MILES LSF (σ_tpl), which is broader than DESI's rest-frame LSF. So the mock is the template convolved, per
   rest wavelength, with a Gaussian of width² = σ_in² + σ_inst,rest²(λ) − σ_tpl²(λ) (in Å, via `varsmooth`), so that
   the total width at every wavelength equals σ_in ⊕ σ_inst. The truth after the A1 correction is then σ_in. This is
   the gate. Reported beside (not a gate): the literal mock (template convolved by σ_in in velocity only), whose
   correct recovered value is √(σ_in² + σ_tpl² − σ_inst²), not σ_in. Template: `Ebi1.30Zp0.06T10.0000` (Z = +0.06 is
   the BaSTI grid point nearest solar). z = 0.45. "That spectrum": among all flagged primary spectra, the one with the
   median S/N, S/N = median of flux·√ivar over good pixels in the observed window of rest 3750-5600 Å at its own
   deflector redshift (lower middle if even). The mock is scaled to that spectrum's median flux in the same observed
   window used for z = 0.45, noise drawn from its 1/√ivar, its masked pixels masked, plus the A1 line masks at
   z = 0.45. 40 realisations per σ_in, seed 20261112. Gate: |median/σ_in − 1| ≤ 0.05 at 150, 250 and 350 km/s.
   If it fails, A1 is NOT EVALUABLE and I say so; I do not change settings until it passes. I also run, reported only,
   a template-mismatch mock (input template 5 Gyr, Z = −0.35) at the same noise.
2. **F2 cannot be run blind.** No SDSS pipeline dispersion of a Euclid lens is on disk outside EUC5's folder and no
   archive query is allowed. My blind A1 word is therefore conditional: "the word if F2 passes or has fewer than 5
   pairs". After unblinding I read EUC5's F2 and state whether it changes the word.
3. **Redshift window of frozen §1 under A1.** A1.1 selects the spectra; the catalogue's deflector redshift is already
   vetted. I keep flagged lenses whatever their photo-z, and report the reading with lenses outside photo-z 70 % ± 0.1
   dropped, as a sensitivity.
4. **SDSS `wave_sigma` units** (for the SLACS spectra). Read from the files' header-free arrays before any fit: it
   falls from about 1.14 at 3,880 Å to 0.76 at 7,570 Å. In pixels (69.03 km/s each) that is 79 → 52 km/s, matching SDSS
   R ≈ 1,800-2,200; in Å it would be 30 km/s in the red, impossible for SDSS. So SDSS `wave_sigma` is taken as pixels.
   DESI `wave_sigma` is taken as Å (0.63-0.80 Å, R ≈ 2,300-5,400, DESI's published range).
5. **Seeing and fibre for the frozen J3.** 1.5″ radius, FWHM 1.5″, β = 0, n = 4, a₀ = 1.132e-10, SLACS's own
   cosmology (flat, h = 0.7, Ω_m = 0.3, in which Auger's R_E in kpc is tabulated), R_e = `Re(V)` (A55's choice),
   lenses with finite σ, R_E, z_s and Re(V). B per lens from the lens equation at the true z_s.
6. **b∞.** EUC1's definition (Σ_cr at z_s = 1100, effective Einstein radius), computed with my own projection at the
   deflector's spectroscopic redshift with the rescaled mass, per footing and law.
7. **Seeing variants** follow A1.4 (0.9, 1.1, 1.3″), not the frozen SDSS set.
8. **A lens at a search end** is kept at the end in the median and counted.

## 3. Validation plan (known answers, tolerances)

- **J1** Plummer sphere, isotropic, Newtonian, via my general Jeans code: projected σ² = (3π/64)GM/a (1+R²/a²)^(-1/2)
  at R = 0.5a and 2a, to 1 % (in σ²). Gate.
- **J2** tracer ν ∝ r⁻³, flat rotation curve, β = 0.3: projected σ² = v_c²/3 to 1 %. Gate.
- **J3** SLACS (frozen form above): median σ_pred/σ_meas in 0.977 ± 0.05. Gate.
- **J4** SLACS: median b_dyn − b_lens(true z_s). Reported.
- **K-proj** lensing projection: point mass returns M to 1e-6 at a₀ → 0; aperture weight of a point source at the
  centre equals 1 − exp(−R_ap²/2s²) to 1e-4. Gate for my code (not a frozen check).
- **K-sanity** SLACS dispersions predicted from Auger's Salpeter masses (`logMs`), Re(V), n = 4, law S alt: median
  σ_pred/σ_meas reported; expected band 0.85-1.00 (Salpeter falls about 12 % short in Einstein radius, A55); outside
  it I stop and look for a bug before reading any graded number.
- **F1** above (gate), F3 reported.
- **MUTATE** `EUC5R_MUTATE=newton` (a₀ → 1e-30): `b_med` on P must rise on both footings; the script exits 1; outputs
  under separate names.

## 4. My addition, declared now: a real-spectra scale (separately labelled; never changes a frozen word)

The 30 SLACS SDSS spectra on disk are fitted with exactly the A1 fitter (same templates, window, masks, polynomial,
clipping, correction with the SDSS LSF), de-redshifted with Auger's z_lens:
(a) as observed; (b) degraded to DESI noise: Gaussian noise added so that each spectrum's median S/N per rest-frame Å
in the fit window equals the median of that quantity over the DESI spectra that enter the graded P reading (a
spectrum already noisier is left as is and counted); 5 noise realisations per lens, the lens's value = median of the 5.
DESI's resolution is finer than SDSS's, so resolution cannot be degraded; the LSF difference is what F1 tests.
The published SLACS σ come from the same SDSS fibre (1.5″ radius), so no aperture correction enters the ratio.

Scale `s` = median over SLACS lenses passing A1.3's quality cuts of σ_EUC5R / σ_SLACS in case (b), with a 95 %
bootstrap interval (2,000 resamples, seed 20261112). Case (a) reported beside.

Rule: **READING R** (EUC5R addition, post-measurement calibration, not a frozen word) divides every DESI σ by s and
recomputes b_dyn per lens; its interval is the envelope of the bootstrap intervals obtained with s at its lower and
upper 95 % bounds. The would-be word under EUC1-F's lines is printed with the label "READING R", beside the A1 word,
never in place of it. If the interval on s contains 1, READING R is still printed and noted as consistent with no
scale. Caveat stated now: the SLACS σ are themselves a template fit (Bolton et al.) to the same spectra; s measures
my fitter against theirs, not against truth.

## 5. Hand estimate (before any number)

Typical ECLIPSE lens (EUC1 sample medians): log M★ = 11.42, R_e ≈ 6 kpc, n ≈ 5. Newtonian virial σ_e² ≈ GM/(5R_e)
≈ (190-200 km/s)²; g_N at R_e ≈ 5 a₀, so law S adds roughly 10-20 % to g inside the fibre, giving σ ≈ 205-215 km/s at
B = 1. Measured σ for log M★ ≈ 11.4 early types are typically 230-260 km/s, so b_dyn ≈ +0.10 ± 0.10 per lens and
b_med ≈ +0.05 to +0.15 on ~35 lenses with a ± 0.05-0.07 interval: most likely NO VERDICT, HOLDS possible, FAILS
unlikely. SLACS: A85's −2.3 % in σ at the lensing boost suggests J4 ≈ +0.02 to +0.05 dex. Template mismatch and an
LSF-correction error each move σ by a few per cent (0.02-0.04 dex in b).
