# EUC12 (COMMON STELLAR-MASS SCALE, EUCLID vs SLACS): FROZEN CRITERIA

2026-11-12. Committed alone, before any EUC12 script exists and before any cross-match or common-scale number is
seen. TEST lane. κ = ½ FITTED; not theory closed. Footings canonical a₀ = 9.3603e-11, alt a₀ = 1.132e-10 m/s²,
never pooled. No outcome is a pass of the theory.

## 1. Question

On one common stellar-mass scale and one dispersion-fitting scale, does law S need the same stars (the same boost
over the stellar mass) for Euclid's typical lens galaxies as for the SLACS lens galaxies?

## 2. Samples

- **Euclid.** EUC5R's sample P (35 lenses: grade A, EUC1 §2 cuts, quality-passing DESI dispersion from EUC5R's
  chosen spectrum). Classes by catalogue `eclipse_effective_einstein_radius` θ_E: **primary = θ_E < 1.3″**; also all
  of P and θ_E ≥ 1.3″.
- **SLACS b side.** The SLACS lenses whose SDSS spectrum EUC5R fitted with its own fitter (`euc5r_slacs_fits.csv`,
  30) that pass that fit's quality flag and have finite Auger `logMs`, `zlens`, `Re(V)` (else `Re(I)`, counted).
- **SLACS δ side.** Every Auger 2009 lens with finite `logMs` (any of the 85), matched as in §3. Reported beside: δ_S
  restricted to the lenses of the b side.

## 3. Constructions

**A (primary): DESI DR1 CIGALE** (`IronPhysProp_v1.2.fits`, `LOGM`, Chabrier, WMAP7 H₀ = 70.4, Ω_m = 0.272; read
memory-mapped in row chunks, needed columns only).
- Euclid match: the TARGETID of EUC5R's chosen spectrum (via `euc2_matches.csv`); if several CIGALE rows share it,
  the row with the same SURVEY and PROGRAM, else the Z nearest `z_desi`. Kept if LOGM finite and > 8.
- SLACS match: nearest CIGALE row within 1.5″ of Auger's position with |Z − zlens| ≤ 0.005, LOGM finite and > 8.
- Cosmology: the CIGALE mass is moved to each side's own cosmology, M × (D_L,side(z)/D_L,WMAP7(z))² (Euclid side:
  ECLIPSE's H₀ 67.74, Ω_m 0.3089; SLACS side: Auger's h 0.7, Ω_m 0.3), so that each side's δ and b share distances.
- Per lens δ = log₁₀(M_cat / M_common). Euclid M_cat = ECLIPSE Salpeter survived mass rescaled to the DESI redshift
  by (D_L(z_spec)/D_L(z_phot))² (EUC5R's convention; δ with the unrescaled mass reported). SLACS M_cat = 10^logMs.

**B (frozen fallback and bracket, independent of CIGALE's SED fit): one luminosity-based mass.**
- Photometry: Legacy Surveys DR10 Tractor (`ls_dr10.tractor`) through the NOIRLab Data Lab TAP service: for each
  lens (P and every Auger lens with `logMs`) one cone of 2″, nearest non-PSF object within 1.5″; `flux_w1`,
  `flux_z` divided by `mw_transmission_*`. One paced stream, ≥ 1 s apart, generic User-Agent, no personal detail.
  If the service is unreachable, B uses the Legacy Surveys fluxes carried in the CIGALE file (matched objects only),
  and says so.
- Recipe (identical for both samples): E-MILES BaSTI bimodal Γ = 1.30, [M/H] = +0.06, age = t(z) − t(z = 3) in the
  side's cosmology (linear interpolation in log age between grid ages, capped at 14 Gyr); the SSP spectrum per unit
  initial mass is redshifted and integrated through a top-hat band (W1: 3.00-3.70 μm; z: 8,500-10,000 Å), as AB f_ν
  photon-weighted; mass = observed flux / model flux per unit mass × M(*+remn) of that SSP. Headline band W1; z band
  reported. Same δ definition and cosmology as A.

## 4. Statistic

Per footing, law S, β = 0, Euclid seeing FWHM 1.1″ (DESI fibre radius 0.75″, EUC5R's convention), SLACS seeing
FWHM 1.5″ (SDSS fibre radius 1.5″, n = 4, Auger cosmology, EUC5R's J3 convention):

**Δb_common = [median_class b_dyn,E + median_class δ_E] − [median b_dyn,S + median δ_S].**

b_dyn per lens = log₁₀ of the factor on the catalogue Salpeter mass that makes EUC5R's model (`euc5r_model.py`,
imported) reproduce the dispersion. Euclid σ = EUC5R's DESI fits (raw, no READING R scale). SLACS σ = EUC5R's own
fitter on the SDSS spectra **degraded to DESI noise** (`deg_sigma`, quality `deg_q`; primary, matches the Euclid
S/N); **as observed** (`nat_sigma`, `nat_q`) is the stability variant; Auger's published σ is a bracket (it is a
different fitter, so it does not share the scale and cannot veto the word). 95 % interval: 2,000 bootstrap draws,
seed 20261112, each of the four lens sets resampled independently, percentiles 2.5 / 97.5. Reported beside: the
per-lens form median(b + δ) on lenses that have both, each side; δ_E, δ_S, δ_E − δ_S with intervals.

## 5. Words (per footing, per class; primary class θ_E < 1.3″, construction A)

Margin 0.10 dex = the usual disagreement between stellar-mass codes, so a difference inside it cannot be told from
a code difference.
- **SAME STARS**: interval inside [−0.10, +0.10].
- **EUCLID NEEDS MORE**: lower bound > 0 and median ≥ +0.10.
- **EUCLID NEEDS LESS**: upper bound < 0 and median ≤ −0.10.
- **NO VERDICT**: otherwise, or if the word differs between the SLACS "at DESI noise" and "as observed" fits.
- **NOT EVALUABLE**: only if both A and B fall below the minimum N.

Minimum N: A is primary if ≥ 10 SLACS lenses have δ_S and ≥ 10 primary-class Euclid lenses have δ_E. Otherwise B
is primary with the same lines and minimum. If both fail: NOT EVALUABLE. Whichever is not primary is a bracket.
A known-answer failure that I cannot trace to a bug makes that construction NOT EVALUABLE.

## 6. Known answers (gates, before any graded number is read)

- K1 Chabrier/Salpeter: δ_S computed with Auger `logMc` minus δ_S with `logMs`, median −0.25 ± 0.02 (Auger's
  constant, with table rounding).
- K2 shifted positions (+60″ in Dec): the SLACS position-plus-redshift match returns ≤ 1 object.
- K3 redshifts: Euclid matched Z equals EUC5R's `z_desi` within 1e-4 for all; SLACS median |Z − zlens| ≤ 0.001.
  Euclid CIGALE RA/Dec within 1.0″ of the ECLIPSE position for ≥ 90 % (positional cross-check).
- K4 EUC5R's J3 through my use of its machinery: median σ_pred/σ_meas = 0.966 ± 0.002.
- K5 catalogue-scale Euclid medians on P (θ_E all, law S, β 0, 1.1″): +0.202 / +0.197 ± 0.002; per-lens b within
  1e-3 dex of `euc5r_per_lens.csv`.
- K6 cancellation: Euclid catalogue masses × 10^0.2 leave Δb_common unchanged within 0.005.
- K7 B recipe: my V-band (top-hat 5,000-6,000 Å) M(*+remn)/L_V of the 10 Gyr [M/H] +0.06 SSP within 15 % of the
  E-MILES table value.
- Mutation twin `EUC12_MUTATE=shift`: +0.20 dex added to the Euclid common-scale masses; Δb_common must fall by
  0.20 ± 0.01 on both footings; separate outputs; exits 1. Newton twin (a₀ → 1e-30) reported.

## 7. Reported beside (no word)

Matched Euclid subsample vs P (z, mass, θ_E); δ_E with and without the spec-z rescaling; Euclid seeing 0.9 / 1.3″
and SLACS seeing 1.2 / 1.8″; a reading, labelled not a gate, of EUC10 Part B's lensing numbers moved to the common
scale: (b_lens,E + δ_E(P)) − (b_lens,S + δ_S).

## 8. Disclosure: seen before freezing

From the lead's brief: EUC5R P medians +0.202 / +0.197 and classes +0.12 / +0.18 / +0.26 (θ_E < 1.0, 1.0-1.3,
> 1.3″); gate lines 0.15 / 0.25; SLACS lensing +0.082 / +0.070 and dynamics about +0.085; EUC10 Part B +0.238 /
+0.220 (AGEL DR2) and +0.298 / +0.282 (DESI SLF IV); J3 0.966; the ECLIPSE paper's statement that SLACS lenses have
θ_E 0.3 dex smaller at fixed stellar mass; the lead's unverified hand estimate (catalogue-scale typical-class gap
+0.03 to +0.10, mass-scale offset up to 0.15 dex either way, likeliest NO VERDICT or SAME STARS). From files read:
EUC5R's RESULT and READING (fitter scale 1.049 as observed, 1.057 at DESI noise against published SLACS σ), the
headers and first rows of its CSVs, the CIGALE column list and FETCH_LOG, the Auger column list and first rows. I have
not seen any CIGALE row of any lens or any SLACS b_dyn on EUC5R's own-fitter σ. A Data Lab TAP capabilities request
(no data) returned HTTP 200.

My hand estimate: Prospector's non-parametric masses usually run 0.1-0.2 dex above parametric fits; Auger used
parametric SPS on HST photometry; CIGALE is parametric. So δ_E − δ_S ≈ +0.05 to +0.20 and, with the own-fitter
SLACS σ raising SLACS's b by about 0.04, Δb_common ≈ +0.05 to +0.25 in the primary class: likeliest NO VERDICT,
EUCLID NEEDS MORE possible. Known systematic stated now: the samples sit at different redshifts (Euclid ≈ 0.3-0.9,
SLACS ≈ 0.1-0.35), so any redshift-dependent bias of the common code does not cancel; arc light in the Tractor
photometry enters both sides.
