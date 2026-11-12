# EUC2 (DESI SOURCE HUNT): FROZEN CRITERIA

Committed alone, before any EUC2 script exists and before any lens spectrum is retrieved. 2026-11-12.
Owner, 2026-11-12: "Yes, hunt them" (pull the public DESI spectra of the Euclid lenses and look for source redshifts).

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt), never pooled. Not "theory closed". No outcome may be
described as the data favouring the framework.

## 0. What this lane is

EUC1 (898cefb457 / origin dcc8e51300) found Euclid's strong lenses at the law's saturation ceiling with the source at
infinity, and showed the answer turns on the source redshifts, which the ECLIPSE catalogue does not carry. DESI DR1
spectra are public. A DESI fibre on a lens galaxy also collects light from the lensed arcs, so a background emission-line
system in the deflector's spectrum is the source. Storfer et al. (in preparation) did this by eye and report 20 systems
with both redshifts without listing them. This lane finds them independently, with a frozen automatic search, and reads
EUC1's statistic at the true source redshift.

## 1. Data (frozen)

- Lens list: the EUC1 files (same hashes). **Flagged** = every ECLIPSE row, any grade, with a `desi_deflector_specz`.
  **Extension** = every lens of EUC1's sample S (grades A+B, valid inputs) that is not flagged.
- Spectra: NOIRLab SPARCL public service, data release `DESI-DR1`, anonymous. For each lens, every spectrum within
  1.5″ of the catalogue position. Fields: flux, ivar, model (Redrock best fit), mask, wavelength, wave_sigma, redshift,
  redshift_warning, spectype, specprimary, survey, program, targetid.
- Spectra are stored outside git; the match table (identifiers, separations, DESI redshifts) is committed.

**Seen before freezing (disclosed).** The service's field list; the response format, from one spectrum of an unrelated
object in a different field, not analysed; EUC1's results; the ECLIPSE paper's statements that 20 systems have both
redshifts (12 A, 5 B, 3 C), 8 have a source redshift only, and source redshifts span 0.3 to 2.7; that
EUCL-DR1-L015763 (PS1J1821+7130) has z_s = 1.366 ± 0.008 from Euclid NISP "with DESI support". No lens spectrum has
been retrieved or looked at.

## 2. The search (frozen)

**Preparation, per spectrum.** Good pixels: ivar > 0, mask = 0, finite. Residual `r = flux − model`, minus its running
median over 151 pixels. Errors rescaled by the running robust scatter (1.4826 × MAD of r√ivar over 501 pixels, floor 1).
Pixels within 3 Å of the sky lines at 5578.9, 6302.0 and 6365.5 Å are dropped.

**Line statistic.** Matched filter with a unit-area Gaussian of width
`σ² = wave_sigma² + (70 km/s · λ/c)²`, on line centres every 0.2 Å. `SN = Σ r t ivar / √(Σ t² ivar)`; undefined where
less than 80 % of the template weight falls on good pixels.

**Lines (vacuum Å).** [O II] 3727.092, 3729.875; [Ne III] 3869.86; Hβ 4862.683; [O III] 4960.295, 5008.240; Hα 6564.61.
For [O II]: `S_OII = √(SN₁² + SN₂²)` when both components are positive.

**Trial redshifts.** From `z_ref + 0.05` upward in steps of 5e-5, as far as each line stays inside 3600–9824 Å.
`z_ref` is the deflector redshift (§3). A line within 6 Å of a deflector line at `z_ref` ([O II], Hβ, [O III], Hα,
[N II] 6585.27, [S II] 6718.29 / 6732.67) does not count.

**Classes.**
- **SECURE-D** (resolved [O II] doublet): `S_OII ≥ 7`, both components `SN ≥ 3`, amplitude ratio 3729/3727 in [0.35, 2.0].
- **SECURE-M** (several lines): a lead with `SN ≥ 6` ([O II] by `S_OII`, [O III] 5008 or Hα) and at least one other line
  of the list with `SN ≥ 4` at the same redshift (|Δz| ≤ 3e-4). An [O III] 5008 + 4960 pair must have amplitude ratio in
  [1.5, 6].
- **CANDIDATE**: one line with `SN ≥ 8` and nothing else. Reported, never used.

Per spectrum the secure redshift with the largest quadrature sum of its line SNs is kept. Two secure redshifts more than
0.01 apart in one spectrum, or secure redshifts that disagree between two spectra of one lens, exclude the lens (counted).

No Lyα class: a single line cannot be made secure by this search, and sources between z = 1.63 and 1.96 show no strong
line in the DESI range. The search is therefore blind above z_s = 1.63. That is a property of the lane, stated here.

## 3. Deflector redshift and the extension (frozen)

- Flagged lens: `z_ref` = the catalogue's `desi_deflector_specz`.
- Extension lens whose DESI redshift (warning 0) lies within the photo-z 70 % interval widened by 0.1: `z_ref` = the DESI
  redshift, treated as a deflector spectrum.
- Extension lens whose DESI redshift (warning 0, GALAXY) exceeds the upper end of the photo-z 70 % interval by 0.15 or
  more: the DESI redshift is a **source candidate**. It is SECURE-Z only if the same search, run on
  `flux − running median` with no model subtracted and `z_ref` = photo-z, returns SECURE-D or SECURE-M within 0.002 of
  the DESI redshift. The deflector stays at its photo-z.
- Anything else in the extension: not used.

## 4. Instrument checks (frozen; a failure of H1, H2 or H3 makes the lane NOT EVALUABLE)

- **H1 injection.** [O II] doublets (ratio 1.3, 70 km/s) injected into 200 real prepared residuals (seed 20261112),
  at random redshifts in [z_ref + 0.1, 1.6], with matched-filter `S_OII` = 10: at least 90 % recovered as secure with
  |Δz| < 3e-4.
- **H2 nulls.** (a) FAKE-SEP: the SECURE-D rule with a rest separation of 4.50 Å in place of 2.783 Å, on the same
  spectra. Gate: the fake count ≤ max(1, 20 % of the real SECURE-D count). (b) FLIP: all classes on the sign-flipped
  residual; reported.
- **H3 join.** For flagged lenses with a primary DESI spectrum, |z_DESI − `desi_deflector_specz`| < 0.002 in ≥ 95 %.
- **H4 known pair.** If a DESI spectrum of EUCL-DR1-L015763 is retrieved, the search must return a secure redshift
  within 0.01 of 1.366. If it does not, this is reported in the first paragraph. If there is no spectrum, noted.
- **H5 yield (reference, no threshold).** Secure systems among flagged lenses by grade, beside the paper's 12 / 5 / 3.
- **MUTATE** (`EUC2_MUTATE=fakesep`): the search run with the 4.50 Å separation as if it were the signal must return
  fewer than 20 % of the reference SECURE-D count and exit 1. Separate outputs.

Every secure detection is also plotted (line windows) and looked at; a detection judged an artefact by eye is **not**
removed, it is listed with the reason.

## 5. The reading (frozen)

For every lens in EUC1's sample S with a secure source redshift (SECURE-D, SECURE-M or SECURE-Z): EUC1's `b`, the log
stellar-mass boost the law needs, now at the true source redshift, with EUC1's model, cosmology and code. Deflector at
the DESI redshift when flagged or accepted as a deflector spectrum (stellar mass rescaled by the luminosity-distance
ratio squared, as EUC1's run 4b), otherwise at the photo-z.

Reported, law S and law B, both footings: the per-lens table; the median `b` with a 95 % bootstrap interval for
(i) sample P and (ii) sample S; and beside each, the same lenses' source-free `b∞` from EUC1.

**Words.**
- If N(P) ≥ 10, EUC1-F applies exactly as frozen in EUC1's RESULT §8, on law S per footing:
  LENS GATE HOLDS (upper bound ≤ 0.15), LENS GATE FAILS (lower bound ≥ 0.25), else NO VERDICT.
- If N(P) < 10: **EARLY READING, NOT A GATE**. The numbers are reported with that label and EUC1-F stays open.
- Sample S (grades A+B) is always labelled a reading, never the gate.

**Selection, stated now.** The search only finds sources below z_s = 1.63 with strong lines, inside a 1.5″ fibre on the
lens. That favours small Einstein radii and nearby sources, the SLACS-like corner of the sample. `b` at the true source
redshift is correct for each lens found; the subsample is not the Euclid population.

## 6. Not claimed

- That a background emission system in the fibre must be the lensed source. It is assumed, as in every fibre-selected
  lens survey; systems with an Einstein radius above 2″ are flagged in the table.
- Any measurement of a₀ or κ.
- Completeness of the search.
