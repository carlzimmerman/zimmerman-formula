# EUC9 (GRISM SPECTRA SOURCE REDSHIFTS): FROZEN CRITERIA

Committed alone, before any EUC9 script exists in the repository and before the extracted grism spectrum of any ECLIPSE
lens or grade-X object has been fetched or opened. 2026-11-12.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". No outcome of this lane may be described as the data favouring the framework.

## 0. What this lane is

EUC3 (`../EUC3_nisp_source_redshifts/RESULT.md`) looked for lensed-source redshifts in Euclid's DR1 grism *catalogue*
and was NOT EVALUABLE: the catalogue's first solution passes its rule in non-lenses as often as in lenses. This lane
goes to the extracted 1D red-grism spectra of the lens objects and fits the lines itself.

**The handle.** The red grism is exposed with two opposite dispersion directions. An emitter displaced from the
extraction centre by θ_x along the dispersion therefore appears in the co-added spectrum as a **mirrored pair** of
lines at λ ± s, s = 44.7 Å per arcsec × θ_x (13.4 Å per 0.3″ pixel), and its true wavelength is the midpoint. A lensed
arc sits about one Einstein radius from the deflector's centre. The deflector's own line, or a deflector whose photo-z
is wrong (EUC3's main contaminant), is centred and gives one line. (The two-direction geometry is from memory of the
instrument description: PROVISIONAL. The truth gate of §4 tests it.)

EUC1-F and EUC5-F are not redesigned here. This lane supplies source redshifts under a rule and gates frozen below.

## 1. Data (frozen)

- ECLIPSE files and EUC3's cached tables (`_external_data/euclid_dr1_eclipse/nisp_tables/`), as EUC3.
- IRSA, anonymous, one paced stream: `euclid.objectid_spectrafile_association_dr1` (objectid, path, hdu), and each
  spectrum through `https://irsa.ipac.caltech.edu/api/spectrumdm/convert/<path>?dataset_id=euclid_combspec&hdu=<hdu>`.
  Columns WAVELENGTH, SIGNAL, UNCERTAINTY (1e-16 erg s⁻¹ cm⁻² Å⁻¹), MASK, NDITH; common grid of 531 pixels, 11,900 to
  19,002 Å, 13.4 Å per pixel. A spectrum not on that grid is not evaluable. Spectra stay outside git.
- Good pixel: MASK even and below 64 (IRSA's tutorial rule, from memory: PROVISIONAL), UNCERTAINTY > 0, NDITH ≥ 1.

**Seen before freezing (disclosed).** EUC3's whole result, including its void reading (sample P, 18 systems: median b
+0.251 / +0.236; sample S, 35: +0.292 / +0.277) and its diagnostics. EUC5-F's sealed bands. The catalogue rows of the
truth lens EUCL-DR1-L015763: first solution z = 2.1144 (the [O III] doublet reading), second solution z = 1.3768 (the Hα
reading of its red peak), DESI z_s = 1.3657. **The mirrored-pair design was derived from those rows**: two peaks at
15,530 ± 73 Å fit both readings, and 73 Å is 1.6″ against θ_E = 1.51″. Its recovery is therefore necessary, not
independent evidence. The association-table schema; 31 field spectra in a 0.05° box at RA 140.50, Dec +71.05, none
chosen from or matched to ECLIPSE, used to learn the format and to test the code: no pair in any of them, one
sign-flipped pair at the widest aperture; injected pairs of combined S/N 12 recovered at 97 %, S/N 8 at 70–74 %;
injected single lines read as a pair in 0.3–3 %. **No spectrum of any ECLIPSE lens or grade-X object has been fetched.**

## 2. Systems (frozen)

- **Lens side:** EUC1's sample S (6,173; contains sample P, 3,192). The truth lens EUCL-DR1-L015763 (not in S) is
  searched for the truth gate only and enters no reading.
- **Null:** the 2,580 grade-X systems, each given an Einstein radius from S exactly as in EUC3 §2.
- **Spectrum searched:** the lens object's only (the nearest MER object within 0.6″ of the catalogue position, as
  EUC3). Neighbours' spectra are not used: an arc deblended as its own object is centred in its own extraction and
  cannot be told from a projected galaxy.
- **Evaluable system:** has a lens object; a lens redshift interval [z_lo, z_up] (EUC3 §2); a quality row with
  `spe_npix` ≥ 300, `spe_n_dith_med` > 3 and both error flags 0; an association row; a spectrum on the common grid with
  at least 100 good pixels.

## 3. The rule (frozen)

**Preparation.** Continuum = running median over good pixels, window 41 pixels (at least 10 good). Residual r = SIGNAL
− continuum. Errors multiplied by max(1, 1.4826 × MAD of r/error).

**Pair fit.** Templates are pixel-integrated Gaussians of unit flux. For every blue centre on a 6.7 Å grid, every
half-split s from 30 Å to 44.7 Å × (θ_E + 0.5″) in 3.35 Å steps, and σ = 12, 16, 20, 25 Å (both components alike), the
two line fluxes are fitted jointly by weighted least squares. A candidate needs: both fluxes positive; flux ratio
blue/red in [0.45, 2.2] (two of four dithers each way, or two against one); NDITH ≥ 3 at both centres; at least 80 % of
each template on good pixels.

**Single-line alternative.** The best single Gaussian with centre anywhere from 27 Å blueward of the blue centre to
27 Å redward of the red one and σ = 12 to 130 Å (eleven values). Δχ² = χ² gain of the pair − χ² gain of that line.

**Tiers.** TA (primary): each component S/N ≥ 3.5, combined S/N ≥ 6, Δχ² ≥ 9. TB (frozen fallback): 5, 8, 16. The
system's pair is the candidate of largest χ² gain that passes; λ₀ is its midpoint.

**Which line.** With the pair's split, width and flux ratio held, a partner pair is fitted at a scaled midpoint:
- [O III] 4960 at λ₀ × 4960.295/5008.24: if its S/N ≥ 3 and its flux is 0.15 to 0.6 of the pair's, the pair is
  [O III] 5008: class **O3**, z_s = λ₀/5008.24 − 1 (kept if 1.41 < z_s < 2.78);
- otherwise Hα, z_s = λ₀/6564.61 − 1 (kept if 0.84 < z_s < 1.88): class **HA2** if [S II] (λ₀ × 6725.5/6564.61),
  [O III] 5008 or Hβ shows a partner pair at S/N ≥ 3, else **HA1** (Hα assumed, as the catalogue's prior does).

**Guards** (EUC3's, on the same intervals): G1 z_s ≥ z_up + 0.15. G2: λ₀ must not lie within 66 Å of
(1 + z) λ for z in [z_lo, z_up] and λ = [S III] 9533.2; He I 10833.3 to Pa γ 10941.1; Pa β 12821.6 (an inclined
star-forming deflector's own line is extended and can also split). Failing only G2: **AMBIGUOUS-OWN**, never secure.

A system passing everything at a tier is **SECURE** there.

## 4. Gates on the search (frozen; any failure makes the lane NOT EVALUABLE at that tier)

- **H2 purity null.** The identical search on grade X. Pass if `n_X ≤ max(1, 0.20 · n_S · E_X / E_S)` (E = evaluable,
  n = SECURE). Not signal-free in the conservative direction only, as in EUC3.
- **H2b signal-free null.** The identical search on the sign-flipped residuals of the S spectra (emission cannot make a
  negative pair). Pass if `n_flip ≤ max(1, 0.20 · n_S)`.
- **H4 truth.** EUCL-DR1-L015763 must be SECURE with |z_s − 1.3657| ≤ 0.004. Not recovered, or recovered elsewhere:
  fail.
- **I1 sensitivity.** One mirrored pair (combined S/N 12, σ 16 Å, ratio 1, s uniform in the allowed range, random λ₀)
  injected into each of 300 S spectra (seed 20261112): at least 70 % returned within 13.4 Å.
- **I2 discrimination.** One single centred line (S/N 12, σ 20 Å) injected into the same 300: at most 5 % returned as a
  pair within 80 Å.
- **Coverage.** At least 30 % of S and of X evaluable.
- **Tier ladder.** TA first. If TA fails H2, H2b or H4, TB is graded by the same gates and labelled "TB (frozen
  fallback)". If TB fails too: NOT EVALUABLE, and it stays that way; any repair is a separate, disclosed amendment.

## 5. Readings and verdicts (frozen)

EUC1's `b` (law S and B, both footings) at z_s for every SECURE lens, lens inputs exactly as EUC1's primary run, with
`euc1.py`'s own functions; the same lenses' source-free `b` beside it. Lenses with z_l ≥ z_s − 0.2 are dropped and
counted.

- **EUC1-F, exactly as frozen in EUC1 RESULT §8**, on sample P if N(P) ≥ 10: median b, law S, per footing, 95 %
  bootstrap interval (`euc1.stats`). **LENS GATE HOLDS** if the upper bound ≤ 0.15; **LENS GATE FAILS** if the lower
  bound ≥ 0.25; otherwise **NO VERDICT**. If N(P) < 10: **EARLY READING, NOT A GATE**.
- **EUC5-F, exactly as sealed in EUC5 RESULT §3c**, on sample S, per class with N ≥ 10. Classes θ_E < 1.0″; 1.0 to
  < 1.3″; ≥ 1.3″. Bands, canonical: −0.19 to +0.22; −0.05 to +0.30; +0.03 to +0.32. Alt: −0.19 to +0.21; −0.06 to
  +0.34; +0.03 to +0.31. **LENSING EQUALS DYNAMICS** if the 95 % interval on the class median overlaps the band;
  **EXCEEDS** if its lower bound lies above; **BELOW** if its upper bound lies below. A class with N < 10: NOT GRADED.
- **Line identity.** HA1 lenses are also read at the [O III] redshift, (1 + z_s) × 6564.61/5008.24 − 1. If that changes
  an EUC1-F or EUC5-F word, the word carries "(IDENTIFICATION-DEPENDENT)" and the RESULT says so in its first paragraph.

**Selection, stated.** Only sources displaced along the dispersion by at least 0.67″, with resolved components, enter:
the search favours wide-separation lenses and bright, compact line emitters, and loses arcs lying across the
dispersion. The Einstein-radius distribution of the secure sample is printed beside P's. The reading describes those
lenses, not the median of P.

## 6. Robustness (frozen list; reported; cannot change a word except through §5's identity rule)

1. HA1 at the [O III] redshift. 2. Two-line classes only (HA2, O3). 3. Tier TB only. 4. AMBIGUOUS-OWN added.
5. Lens redshift and mass at the DESI deflector redshift where one exists.

## 7. Instrument checks and twins (frozen; a failed check makes the lane NOT EVALUABLE)

- **K1** EUC1 reproduced (N(P) = 3,192; source-free median b −0.019 / −0.044 to 0.001). **K2** EUC2's anchor
  (+0.231 / +0.215 to 0.002).
- **K5** fetch: every evaluable target has a cached spectrum or a recorded reason; 20 spectra fetched again at the end
  are identical.
- **MUTATE twins**, separate output names, each must exit 1: `EUC9_MUTATE=newton` (a₀ → 10⁻³⁰: b must rise on both
  footings, on the reading sample if it exists and on the K2 anchor); `EUC9_MUTATE=single` (the pair requirement
  removed: the best single line of S/N ≥ 6 and σ ≤ 40 Å counts; the number of SECURE grade-X systems must rise).

## 8. Not claimed

- No measurement of a₀ or κ. No statement about lenses whose sources are not found.
- A HOLDS is not a confirmation of the law; an EQUALS is an overlap of two wide intervals.
