# EUC5 (DYNAMICAL BOOST): FROZEN CRITERIA

Committed alone, before any EUC5 script exists and before any velocity dispersion of a Euclid lens is retrieved.
2026-11-12. Owner, 2026-11-12: "keep swinging while EUC3 runs".

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt), never pooled. Not "theory closed". No outcome may be
described as the data favouring the framework.

## 0. What this lane is

EUC1's statistic `b` is the factor (in dex) by which a lens galaxy's catalogued Salpeter stellar mass must be
multiplied for the law to supply its lensing. Lensing gives only a lower bound on `b`, because the Euclid catalogue has
no source redshifts. **Stellar dynamics measures the same `b` with no source at all.** Under the framework light and
matter see one potential (A12), so the law that sets the deflection also sets the stars' velocity dispersion. A85
checked this on SLACS: lensing-calibrated masses predict the measured dispersions to −2.3 % in the mean.

Many Euclid lens galaxies are old SDSS / BOSS spectroscopic targets with pipeline velocity dispersions. This lane
reads `b_dyn` from them: a two-sided measurement, where EUC1 had a one-sided bound.

## 1. Data (frozen)

- Lenses: EUC1's catalogue files (same hashes), samples P (grade A) and S (grades A+B) as EUC1 defines them.
- Dispersions: `sdss_dr17.specobj`, NOIRLab Data Lab TAP, anonymous. A spectrum qualifies if it lies within 1.0″ of the
  lens position and has `scienceprimary = 1`, `class = 'GALAXY'`, `zwarning = 0`, `veldisp` in [70, 500] km/s,
  `veldisperr > 0` and `veldisperr / veldisp ≤ 0.25`.
- The spectrum's redshift must lie inside the lens's photo-z 70 % interval widened by 0.1 on each side; otherwise the
  lens is dropped and counted. The deflector is then placed at the spectroscopic redshift and its stellar mass rescaled
  by the luminosity-distance ratio squared (EUC1's run 4b).

**Seen before freezing (disclosed).** The table's column list; the sky distribution of the lenses (3,738 grade A/B
lenses north of the equator); EUC1, EUC2 and EUC4 results; the SLACS record (A55 0.885, A70 1.174, A85 −2.33 %). No
SDSS row of any lens has been retrieved.

## 2. Model (frozen)

- Tracer and mass: EUC1's spherical Sérsic body (catalogue `n`, `R_e`, Prugniel–Simien), total mass `B × M★`. No gas,
  no halo, no neighbours, no external field.
- Field: law S (headline) and law B on those stars.
- Dynamics: spherical Jeans equation with constant anisotropy β; **β = 0** is the headline.
- Observable: the luminosity-weighted line-of-sight second moment inside the fibre, radius 1.0″ (`instrument = BOSS`)
  or 1.5″ (`SDSS`), after Gaussian seeing of FWHM 1.5″. The pipeline `veldisp` is taken as measured.
- Per lens, `b_dyn` = log₁₀ of the `B` at which the model equals `veldisp` (searched over −1.5 to +1.5; a lens at
  either end is counted and kept at the end).
- Cosmology: the catalogue's (flat ΛCDM, H₀ = 67.74, Ω_m = 0.3089).

## 3. Statistic and words (frozen)

`b_med` = median `b_dyn` with a 95 % bootstrap interval (2,000 resamples, seed 20261112), per law and footing, on the
lenses of P with a qualifying spectrum (N ≥ 30 required), and beside it on S.

Words per footing, law S, β = 0, on P, with EUC1-F's own lines because the quantity is the same:
- **DYNAMICAL GATE HOLDS** if the upper bound of `b_med` ≤ 0.15;
- **DYNAMICAL GATE FAILS** if the lower bound ≥ 0.25;
- **NO VERDICT** otherwise.
If the word differs among β = −0.2, 0, +0.2 or among seeing 1.2″, 1.5″, 1.8″, the word is NO VERDICT and the spread is
reported. N < 30 or a failed instrument check: NOT EVALUABLE.

**Reported, no word:**
- by Einstein radius (below 1.0″, 1.0–1.3″, 1.3–1.7″, above 1.7″), the split EUC4 confirmed;
- `b_dyn − b∞` per lens, where `b∞` is EUC1's source-free lensing bound for the same lens at the same redshift. A real
  source needs `b_lens ≥ b∞`, and one potential needs `b_lens = b_dyn`, so `b_dyn − b∞` must be positive up to noise.
  Its median and the fraction below −0.25 are printed: a strongly negative value would mean the law's lensing and
  dynamics disagree on these galaxies, or that the catalogue inputs are wrong;
- the source redshift at which each lens's lensing boost equals its dynamical boost (median, and the fraction with no
  solution), labelled CONDITIONAL on one potential and on the model.

## 4. Instrument checks (frozen; a failure of J1–J3 makes the lane NOT EVALUABLE)

- **J1** Plummer sphere, isotropic, Newtonian: projected dispersion equals `(3π/64) GM/a (1 + R²/a²)^(-1/2)` to 1 % at
  R = 0.5a and 2a.
- **J2** tracer `ν ∝ r⁻³` in a flat rotation curve with β = 0.3: projected `σ² = v_c²/3` to 1 %.
- **J3** SLACS (A85's test): with each lens's stellar mass set by its own lens equation at the true source redshift
  (law S, a₀ = 1.132e-10, n = 4, fibre radius 1.5″, seeing 1.5″, β = 0), the median of predicted / measured dispersion
  lies within 0.977 ± 0.05.
- **J4** (reported) on SLACS, the median of `b_dyn − b_lens(true z_s)`.
- **MUTATE** (`EUC5_MUTATE=newton`, a₀ → 10⁻³⁰): `b_med` on P must rise on both footings; exit 1; separate outputs.

## 5. Selection and caveats, stated now

- SDSS / BOSS targeted luminous red galaxies at z ≈ 0.15–0.7: the massive end of the lens sample, north only.
- The fibre also collects arc light; it dilutes the absorption lines slightly. Not modelled.
- Pipeline dispersions at low signal-to-noise scatter by 15–25 % per galaxy (0.15–0.2 dex in `b`); the median is the
  statistic for that reason.
- `b_dyn` carries the IMF degeneracy A70 found for lensing: it does not measure a₀.
- A HOLDS is not a pass of the law; it says these galaxies' stars, at a Salpeter-like mass, move as the law says.
