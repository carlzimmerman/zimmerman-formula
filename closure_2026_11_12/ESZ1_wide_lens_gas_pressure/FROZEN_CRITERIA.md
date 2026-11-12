# ESZ1 (WIDE-LENS GAS PRESSURE): FROZEN CRITERIA

2026-11-12. Committed alone, before any script of this lane exists and before the Compton-y map was read at the
position of any lens, control, cluster or offset. A test lane; it adopts nothing. κ = ½ FITTED. Footings (canonical
a₀ = 9.3603e-11, alt 1.132e-10 m/s²) graded separately, never pooled. One-sided: no outcome favours the framework.
Cold dark energy is a gravitating field component, never a particle.

## Question

EUC4 (confirmed blind by EUC4R) found that Euclid's wide-separation lenses need more projected mass than law S gives
the lens galaxy's stars; EUC8 put the shortfall at 45 to 61 % of the lensing mass. EUC4 Part B (exploratory) and EUC8
computed how much extra SOURCE mass law S would need if the missing pull came from an extended body around the lens.
The only baryons that could be such a body are hot gas, and hot gas in equilibrium has a pressure the
Sunyaev-Zel'dovich effect sees.

**Is the hot gas there?** If law S acting on stars plus hot gas supplies these lenses, the gas must be so massive, and
to stand still in law S's own field so hot, that a stack of the ACT Compton-y map on the lenses must show it.
Part G grades that. Part C asks whether wide lenses carry more gas pressure than matched small-separation lenses.
Part D reports what the stack measures, in physical units, including against the cold-share reading of EUC8.

## Data

- **Lenses:** ECLIPSE catalogue, the two files and hashes frozen in EUC1; EUC1's `load`, `select`, `build`, `g_law`,
  cosmology (`EUCLID`: H₀ 67.74, Ω_m 0.3089, the catalogue's own). Sample S = `select(rows, ("A", "B"))`.
- **Compton-y:** ACT DR6.02 needlet-ILC map `act-planck_dr6.02_nilc_ComptonY.fits` (NASA LAMBDA), CAR, 0.5′ pixels,
  43200 × 10320, big-endian float32, beam 1.6′ FWHM Gaussian. Rows 3239 to 8040 (Dec −36° to +4°) were on disk
  (fetched 2026-10-29, hashes in that directory's SHA256SUMS). Rows 0 to 3238 (Dec −63° to −36°; bytes 2880 to
  559,702,079 of the file, 559,699,200 bytes) are being fetched today by HTTP byte range, with the owner's go, for
  this map and for its CIB-deprojected twin `…_ComptonY_deproj_cib_1.0_10.7.fits` (the bracket). Their sha256 values
  are recorded in the run log on first read; LAMBDA publishes no per-range checksum, so check K2 stands in for one.
  The two row ranges are read as one array of rows 0 to 8040.
- **Positive control:** the eRASS1 cluster table already on disk (`cfg687_inputs/erass1_main.tsv`, GO1's reader).

## Samples

- **Covered:** a position is covered if (i) the square of half-width 26′ around it lies inside rows 0 to 8040,
  (ii) every pixel of it is finite, and (iii) the pixel rms of that square outside a 6′ radius lies between 0.5 and
  2.0 times the median of the same quantity over all positions of S passing (i) and (ii). (Outside ACT's footprint
  the map is not zero but very small; rule (iii) removes those positions and the tapered edge.)
- **W:** lenses of S with θ_E ≥ 1.7″ (EUC1's effective Einstein radius), covered. EUC8's W is 316 lenses on the whole
  sky; about 240 are expected here. **Required N ≥ 100.**
- **C (controls):** one per W lens, taken in identifier order: the covered lens of S with θ_E < 1.0″ nearest in
  `(Δz_l / 0.05)² + (Δ log M★ / 0.1)²`, without replacement (EUC6's rule; ties go to the lower identifier).
- **Classes for the report:** 1.3–1.7″, 1.0–1.3″, below 1.0″; **L:** covered grade A or B lenses with
  `large_system_warning = True` (not in S).
- **Offsets:** for every target, 16 positions on a circle of radius 20′ (position angles k × 22.5°), each required to
  be covered. A target with fewer than 12 covered offsets is dropped.

## Measurement

Compensated aperture photometry on the pixel grid, sub-pixel centre, pixel solid angle 0.25 cos(Dec) arcmin²:
`CAP = Σ_disk y Ω_pix − (N_disk / N_ring) Σ_ring y Ω_pix`, disk r < θ_d, ring θ_d ≤ r < √2 θ_d. **θ_d = 2.0′**
(brackets 1.5′ and 3.0′). Each target's value is its CAP minus the mean CAP of its offsets. The stack is the
unweighted mean over targets. **σ** is the larger of (a) the bootstrap standard deviation over targets (2,000
resamples, seed 20261112) and (b) the rms of the 16 null stacks (offset k treated as the target, the other offsets as
its offsets).

## Part G: the hot gas law S would need (words)

Model, per W lens (spherical): stars as in EUC8 (Sérsic, Prugniel–Simien, catalogued Salpeter mass × 10^b★) plus a
gas body; the Newtonian fields add and law S acts on the sum. Families, one amplitude each:

| Name | Gas density | Source |
|---|---|---|
| B30, B100 | ∝ (1 + r²/r_c²)⁻¹, r_c = 30 and 100 kpc, cut at 500 kpc | EUC4 Part B's `GasEngine`, verbatim |
| G2 | ∝ r⁻², cut at 300 kpc | EUC8's γ = 2 family, verbatim |

The amplitude is solved so that stars plus gas under law S give π R_E² Σ_cr(z_l, z_s); zero if the stars alone do.
Source cases as EUC8: **far** z_s = 1100 (least mass), **central** max(2.0, z_l + 0.5), **near** z_l + 0.5.
b★ = −0.10, 0, +0.10.

Pressure: hydrostatic balance in the law's own field, `dP/dr = −ρ_gas g`, `g = law_S(g_N★ + g_N gas)`, with **zero
pressure at the cut-off** (any confining pressure only adds, so this is the least pressure such gas can have).
Electron pressure P_e = P μ/μ_e with μ = 0.59, μ_e = 1.14. y(R) = (σ_T / m_e c²) ∫ P_e dl. The profile is convolved
with the 1.6′ beam, placed on the lens's own pixel grid and passed through the same CAP estimator (offsets predicted
as zero). The predicted stack is the mean over the same W lenses, zeros included.

Family words, per footing, with `pred_min` = the predicted stack in the least demanding setting (far, b★ = +0.10):

- **NO POWER**: pred_min < 3 σ.
- **EXCLUDED**: measured stack + 2 σ < pred_min.
- **ALLOWED**: otherwise.

Lane word, per footing:

- **NOT EVALUABLE**: an instrument check fails or N_W < 100.
- **HOT GAS DOES NOT SUPPLY THE WIDE LENSES**: B30, B100 and G2 are all EXCLUDED.
- **ONLY A CUSP IS LEFT**: B30 and B100 EXCLUDED; G2 ALLOWED or NO POWER.
- **HOT GAS NOT EXCLUDED**: B30 or B100 is ALLOWED.
- **NO VERDICT**: otherwise.
- Tag **[BRACKET-DEPENDENT: list]** if the lane word moves under any of: the CIB-deprojected map; θ_d = 1.5′ or
  3.0′; grade A only; z_l ≤ 0.6 only.

No word here is a pass. EXCLUDED says the gas is not there at hydrostatic pressure; colder gas is not seen by y, so
each family also gets the factor `f_T = (measured + 2σ) / pred_min`: how far below its hydrostatic temperature the
gas would have to sit to hide.

## Part C: wide lenses against matched controls (word)

D_i = value(W_i) − value(C_i) over complete pairs; mean D with a bootstrap 95 % interval (2,000 resamples).
**Required N ≥ 100 pairs**, else NOT EVALUABLE.

- **WIDE LENSES HOLD MORE GAS PRESSURE**: the lower bound is above zero.
- **NO EXCESS DETECTED**: otherwise (the upper bound is reported).
- Tag [BRACKET-DEPENDENT] if the word moves on the CIB-deprojected map.

## Part D: what the stack measures (reported; no word)

- Mean CAP (arcmin²), mean CAP × D_A² (Mpc²) and the electron thermal energy `E_e = Y D_A² m_e c² / σ_T` for W, C,
  each class, L and all covered S, with σ and 2σ upper limits; the gas mass that energy is at kT = 0.5, 1 and 2 keV
  (`M = E_e μ_e m_p / kT`), in M☉ and in units of the mean stellar mass.
- Per family: median required gas mass, median mass-weighted hydrostatic temperature (keV), median electron density
  at R_E (cm⁻³), predicted stack in every source case and b★.
- **Cold-share reading (EUC8):** take EUC8's γ = 2 component X (far case, b★ = 0) as cold dark energy. Baryons
  required inside 300 kpc at the record's free share: M_X / 5.41. Gas = that minus the stars (zero if negative), as a
  B100-shaped body cut at 300 kpc, in hydrostatic balance in `law_S(g_N★ + g_NX + g_N gas)` with zero edge pressure.
  Its predicted stack is given beside σ. Expected to be far below σ (no power); it is reported so that the size of
  the gap is on record. If the measured stack exceeds it by more than 2σ, that is stated too.

## Instrument checks (all must pass)

- **K1 geometry:** the analytic pixel map against the stored FITS header's WCS at (12.3, −5.0), (47.7, −56.2),
  (60.0, −45.0), (355.2, 2.9): below 0.01 pixel.
- **K2 files and seam:** both new files are 559,699,200 bytes; the correlation between rows 3238 and 3239 over
  columns where both are inside the footprint is at least 0.9 times the correlation between rows 3239 and 3240, on
  both maps.
- **K3 prediction against brute force:** for the median W lens (far, b★ = 0, canonical), the predicted CAP equals a
  brute-force one (profile drawn at 0.05′, convolved in two dimensions, rebinned to 0.5′) within 3 % for B30 and
  B100 and 5 % for G2, at θ_d = 1.5′, 2.0′, 3.0′.
- **K4 hydrostatic solver:** Newtonian limit, no stars, G2 alone: P(r) = (G M_t² / 8π r_t²)(r⁻² − r_t⁻²) to 1e-4 at
  r = 0.01, 0.1, 0.5 r_t.
- **K5 beam:** a point source through the beam convolution has the fraction 1 − exp(−θ²/2σ_b²) inside θ (to 1e-3),
  and the convolution conserves the total Y of a B100 profile (to 1e-3).
- **K6 EUC4 Part B reproduced:** on EUC4's 316 lenses, far, b★ = 0, median log₁₀ M_gas = 13.44 / 13.37 (r_c 30) and
  13.84 / 13.77 (r_c 100), each ± 0.01.
- **K7 EUC8 reproduced:** the γ = 2 mass inside 300 kpc for W (far, b★ = 0, each footing) equals the value stored in
  `euc8_results.json` to 0.1 %.
- **K8 positive control (sign and scale of the map):** eRASS1 clusters with catalogued M500 ≥ 2e14 M☉, 0.1 ≤ z ≤ 0.6,
  covered, N ≥ 20: stacked value positive at ≥ 5 σ. (The catalogued mass only selects obviously massive clusters; it
  enters no graded number.)
- **K9 nulls:** over the 16 null stacks of W, the mean is within 3 σ/4 of zero and none exceeds 3.5 σ.

## Mutation twins

- `ESZ1_MUTATE=inject` (the B100 prediction of the far, b★ = +0.10, canonical setting added to every W lens's value):
  B100 must read ALLOWED on both footings; exit 1.
- `ESZ1_MUTATE=shift` (every lens, control and cluster moved +0.5° in declination): K8 must fail; exit 1.
- `ESZ1_MUTATE=newton` (a₀ → 1e-30): pred_min of B100 must rise on both footings; exit 1.

## Known before freezing (disclosed)

- EUC1 to EUC8's results, including EUC4 Part B's medians quoted in K6 and EUC8's "4 to 8e12 M☉ inside 300 kpc" for
  γ = 2; GO1 and GO2's y machinery and GO2's finding that the y census had no power on 369 low-redshift groups.
- Counts of catalogue rows by declination band and Einstein-radius class (no map value): 1,253 rows with
  θ_E ≥ 1.7″ at Dec −62.5° to +3.5°, of which 324 in the old strip; EUC6's target list has 192 W in the same band.
- From the partly downloaded southern file, its first 200 rows (Dec −63.0° to −61.3°) only: all finite, all
  non-zero, rms 2.3e-8. That is how coverage rule (iii) came about. No lens, control, cluster or offset position was
  read; no aperture was formed.
- The map headers; the eRASS1 table's column layout (three lines).

## Hand estimate (before any number; unverified)

N_W ≈ 240. B100: median gas mass 4 to 6e13 M☉, law-S circular speed near 850 km/s at 300 kpc, hydrostatic kT 1 to
2.5 keV, Y ≈ 5 to 8e-5 arcmin² at z 0.5, so a predicted stack of 3 to 6e-5; B30 2 to 4e-5; G2 (6e12 M☉, 0.6 keV)
about 3e-6. Noise per lens about 2 to 3e-5 arcmin² (white-noise guess), so σ ≈ 1.5 to 2e-6. Real groups should show
1 to 5e-6. Expected: B30 and B100 EXCLUDED by more than ten σ, G2 NO POWER or ALLOWED, lane word **ONLY A CUSP IS
LEFT**; Part C **NO EXCESS DETECTED** (an excess near 1e-6 at about one σ); cold-share row far below σ.

## Limits

Spherical; hydrostatic; y sees pressure, not mass. Photometric lens redshifts; no source redshifts (the far case is
the least mass). Lensed sources are dusty and massive ellipticals host radio sources; both leak into a y map, and
the CIB-deprojected bracket covers only the first. The aperture (730 kpc radius at z 0.5) takes in neighbours, which
adds pressure and so works against EXCLUDED. A coverage rule set by local noise is a proxy for the survey mask.
It tests no part of a₀ or κ.

## Compute

At most 4 threads, nice 19; minutes. Outputs `esz1.out`, `esz1_results.json`, one `.out` and `.json` per twin,
`esz1_per_lens.csv`, `RESULT.md` (label first).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
