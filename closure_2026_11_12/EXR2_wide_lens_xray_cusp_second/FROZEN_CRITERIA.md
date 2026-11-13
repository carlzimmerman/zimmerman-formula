# EXR2 (WIDE-LENS X-RAY CUSP, SECOND MEASUREMENT): FROZEN CRITERIA

2026-11-12. Committed alone, before any script of this lane exists and before this lane sent any lens, control or
offset position to the eROSITA archive. A test lane; it adopts nothing. κ = ½ FITTED. Footings (canonical
a₀ = 9.3603e-11, alt 1.132e-10 m/s²) graded separately, never pooled. One-sided: no outcome favours the framework.
Cold dark energy is a gravitating field component, never a particle.

**This is not a blind re-grade.** EXR1 asked the same question tonight and its outcome was read before this file
was written (see "Known before freezing"). EXR1's frozen word is NOT EVALUABLE because one of its checks was
wrongly designed; its post hoc reading is EXCLUDED. EXR2 exists to give the question a word from criteria that are
frozen before its own data are fetched, by a route that shares as little as possible with EXR1's.

## Question

ESZ1 left law S one hot gas body that pressure could not judge: a cusp around Euclid's wide lenses (ρ ∝ r⁻², cut at
300 kpc; ESZ1's G2). **Does eRASS1 see the X-rays that gas must emit?**

## How EXR2 differs from EXR1

| | EXR1 | EXR2 |
|---|---|---|
| Band graded | 0.2–2.3 keV | **0.6–2.3 keV** (little absorbed; 0.2–2.3 is a bracket) |
| Model flux to service flux | folded through an ARF and RMF | the service's own Γ = 2 conversion, calibrated from its answers |
| Absorption | Morrison & McCammon on 2 × HI4PI | one fixed transmission, 0.40 |
| Plasma code | AtomDB tables read directly | pyatomdb 1.2.2 on the same AtomDB 3.1.3 tables |
| Sample | 263 wide lenses in the eROSITA-DE sky | ESZ1's 237 wide lenses and ESZ1's own 237 controls |
| Null | positions 0.5° away, not subtracted (its K8 failed) | 8 offsets 0.3° away, **subtracted**, frozen here |
| Stack | mean of clipped fluxes | exposure-weighted mean of net rates, unclipped |

Shared: ESZ1's gas model code, the eRASS1 upper-limit service, the ECLIPSE catalogue.

## Data

- **Lenses:** ESZ1's `esz1_per_lens.csv`: W = rows with `is_W = 1` (237); C = rows with `control_of` set (237, one
  per W lens). Positions from the ECLIPSE key file frozen in EUC1.
- **eRASS1:** eRODat upper-limit service, `…/erodat/upperlimit/service_multi`, `dr_survey = DR1_eRASS1`, bands
  `022` (0.6–2.3 keV) and `024` (0.2–2.3 keV). Per position: `Count` (counts in the service's aperture, EEF 0.75),
  `Bkg_counts`, `Exposure`, `UL_B`, `Flag_pos`, `de_sky` (Tubín-Arenas et al. 2024). Also, for the W lens positions
  only, `DR2_eRASSc3` band `024`, which returns upper limits but no counts (Part D only).
- **Catalogue (check K2 only):** eRODat cone search, `CAT = DR1_Main`, `VERB = 3`.
- **Plasma:** pyatomdb `CIESession` on AtomDB 3.1.3 (already on disk), its default abundance table, hydrogen and
  helium at 1, elements Z ≥ 3 scaled by the metallicity. Energy grid 0.05–20 keV, 3,000 logarithmic bins.
- Fetches: one stream, at least 1.5 s between requests, generic client name; raw answers kept outside git with a
  manifest committed here.

## Measurement

- **Positions:** each target and 8 offsets on a circle of radius 0.3° (position angles k × 45°). A position is
  usable if `de_sky` is true, `Flag_pos` is 0, `Exposure` > 0 and `Count` is returned. A target is valid if it is
  usable and at least 6 of its offsets are.
- **Value:** net rate r = (Count − Bkg_counts) / Exposure; a target's value v = r(target) − mean r(its usable
  offsets). Null k: offset k as the target, the other usable offsets as its offsets.
- **Flux scale:** for look-ups with Count = 0, `UL_B × Exposure` is a constant K of the band (check K1). The flux of
  a rate is `rate × K / 6.6077`, where 6.6077 = −ln(1 − 0.99865) is the count limit for zero counts at the
  service's one-sided 3 σ level. This is the service's own conversion: Γ = 2, N_H = 3e20, EEF 0.75.
- **Stack:** `Σ T v / Σ T` over valid targets, T = the target's exposure. **σ** = the larger of the bootstrap
  standard deviation over targets (2,000 resamples, seed 20261112) and the rms of the 8 null stacks.

## Part G: the X-rays the cusp must emit (words)

Per W lens, ESZ1's code unchanged (`solve_gas`, `gas_body`, `pressure`, `grid`; μ = 0.59, μ_e = 1.14): the G2 gas
mass that makes stars plus gas under law S give the lensing mass, in the **least demanding setting** (source at
infinite distance, stars 0.10 dex above Salpeter); hydrostatic in the law's own field with zero pressure at 300 kpc,
so kT(r) = μ m_p P/ρ is the least temperature such gas can have. n_e = ρ/(μ_e m_p), n_H = (2/μ_e − 1) ρ/m_p.

Predicted flux of lens i at metallicity Z:

`F_i = 0.80 × 0.40 × (1 / 4π d_L²) × ∫ n_e n_H Λ(kT(r); Z) 4π r² dr`, from r = R_E to min(300 kpc, 15″ × D_A),

- Λ = APEC emissivity in the rest band 0.6 (1 + z_l) to 2.3 (1 + z_l) keV, tabulated at 60 temperatures from 0.03
  to 5 keV and interpolated in log–log; zero below 0.03 keV.
- **Only gas outside the Einstein radius counts**, and only inside 15″, where it is point-like for eROSITA.
- **0.80** is a stated allowance for that gas not being a true point source in an aperture built for one.
- **0.40** is a stated transmission for Galactic absorption at 0.6–2.3 keV. It is set low on purpose (my estimate
  from memory: 0.5 or more for columns up to 10²¹ cm⁻²; every lens here has |b| ≥ 22°).
- The service's Γ = 2 conversion is applied to a softer thermal spectrum. Assumption, from memory and not checked
  here: eROSITA's area over photon energy falls across 0.6–2.3 keV, so a softer spectrum gives more counts per unit
  flux and the conversion understates the prediction.

Predicted stack `pred(Z) = Σ T F / Σ T` over the same lenses, zeros included.

Family words, per footing:

- **NO POWER**: pred(Z) < 3 σ. **EXCLUDED**: measured + 2 σ < pred(Z). **ALLOWED**: otherwise.

Lane word, per footing:

- **NOT EVALUABLE**: an instrument check fails or fewer than 100 valid W lenses.
- **CUSP EXCLUDED**: the metal-free cusp (Z = 0, hydrogen and helium only) is EXCLUDED.
- **CUSP EXCLUDED UNLESS METAL-FREE**: Z = 0.3 is EXCLUDED and Z = 0 is not.
- **CUSP NOT EXCLUDED**: Z = 0.3 is ALLOWED.
- **NO VERDICT**: otherwise.
- Tag **[BRACKET-DEPENDENT: list]** if the lane word moves under any of: band 024 (the same predicted 0.6–2.3 keV
  flux, a lower bound there, times K₀₂₄/K₀₂₂); inner radius 2 R_E; transmission 0.25; unweighted mean of fluxes;
  grade A only; z_l ≤ 0.6 only.

No word here is a pass. Reported beside the words: measured + 2 σ as a fraction of each prediction, and the share of
the required gas mass that fraction allows at the same profile and temperature (its square root).

## Part C: wide lenses against ESZ1's matched controls (word)

D = flux(W) − flux(its control) over pairs with both valid; mean with a bootstrap 95 % interval. **Required N ≥ 100.**

- **WIDE LENSES ARE BRIGHTER IN X-RAYS**: the lower bound is above zero. **NO EXCESS DETECTED**: otherwise.
- Tag [BRACKET-DEPENDENT] if the word moves in band 024.

## Part D (reported; no word)

Stacks of W and C in both bands, as flux and as luminosity 4π d_L² F (no K-correction); the mean net rate of the
offsets themselves (the sky's offset from the service's smooth background); per lens, how many W lenses have the
service's own 3 σ limit below their prediction, in eRASS1 band 022 and in the three-survey DR2 band 024; predictions
at Salpeter stars and with sources near z ≈ 2; the median gas mass, kT and n_e at R_E; the luminosity of the gas
outside R_E.

## Instrument checks (all must pass)

- **K1 service constant:** among returned look-ups with Count = 0, `UL_B × Exposure` is constant to 0.5 % in each
  band (N ≥ 50 each) and equals the values met before freezing (8.1534e-12 for 022, 8.2439e-12 for 024) to 0.5 %;
  6.6077 / K₀₂₄ / 0.75 is within 3 % of the published 1.074e12 cm²/erg.
- **K2 flux scale, end to end:** DR1_Main sources within 1° of (35, −45), (45, −35), (50, −50), (60, −40),
  (65, −55), (75, −45), (80, −35), (55, −30) with `ext` = 0 and `ml_flux_1` between 1e-13 and 1e-12: the median of
  `[(Count − Bkg_counts) / Exposure × K₀₂₄ / 6.6077] / ml_flux_1` in band 024 lies in 0.75 to 1.25, N ≥ 20; at the
  same positions moved 0.1° north it lies below 0.2.
- **K3 nulls:** none of the 8 null stacks of W exceeds 3.5 σ. (Weak by construction, as ESZ1's K9 was; the nulls'
  own mean is zero because offsets are subtracted. EXR1's failed check is not repeated.)
- **K4 emissivity:** Λ(1 keV, Z = 0) summed over the grid is within 30 % of the free–free estimate
  1.4e-27 √T × 1.2 × 1.4 erg cm³/s (CFG581's control); in the rest band 0.87–3.34 keV at 0.45 keV, Z = 0.3 gives
  more than twice Z = 0.
- **K5 ESZ1 reproduced:** over the 237 W lenses, the median G2 gas mass and median n_e at R_E in the least setting
  equal the values stored in `esz1_results.json` to 1e-6, both footings.
- **K6 luminosity integral:** for ρ ∝ r⁻² and a constant Λ the numerical integral equals
  `Λ (2/μ_e − 1) μ_e n_E² 4π R_E⁴ (1/R_E − 1/r_out)` to 1e-3.

## Mutation twins

- `EXR2_MUTATE=inject` (each W lens's Z = 0 canonical prediction added to its value): Z = 0 must read ALLOWED on
  both footings; exit 1.
- `EXR2_MUTATE=shift` (check K2 run on the positions moved 0.1° north in place of the true ones): K2 must fail;
  exit 1.
- `EXR2_MUTATE=newton` (a₀ → 1e-30): pred(Z = 0) must rise on both footings; exit 1.

## Known before freezing (disclosed)

- **EXR1's result, read in full:** 263 lenses; frozen stack +5.80 ± 1.77 and post hoc (offset-subtracted)
  +4.19 ± 0.85 × 10⁻¹⁵ erg/s/cm² in 0.2–2.3 keV; least prediction 141.7 / 121.3 (Z = 0.1), 78.0 / 67.3 (Z = 0);
  its K8 failure (random apertures average +1.61 × 10⁻¹⁵); wide minus control +3.11 [+1.21, +5.02]; exposure 221 s;
  16 lenses with a catalogued source. Most of EXR2's choices in the table above (band, conversion, fixed
  transmission, sample, subtracted offsets, weighting) were settled in this session before EXR1's folder was opened;
  the offset radius was changed from 4′ to 0.3° afterwards, and this file was written afterwards. There is no dated
  record of that order, so treat every choice as made with EXR1's outcome known.
- ESZ1's result and my scoping estimate (free–free only, all gas outside R_E, unabsorbed: mean 1.2 × 10⁻¹³ at
  0.6–2.3 keV).
- Test queries at eight positions with no lens ((194, −5.7), (150, −20), (150.3, −20.2), (151, −21), (200, −30),
  (200.4, −30.3), (201, −31), (130, −10)): the K values quoted in K1; that DR2 returns no counts; one cone search at
  (194, −5.7) for the column names.
- pyatomdb band emissivities at 0.30, 0.45, 0.60 keV for Z = 0 and 0.3 (ratios 6.8, 4.7, 4.1).

## Hand estimate (before any number of this lane; unverified)

Valid W about 230; exposure about 220 s; σ about 0.5 to 1 × 10⁻¹⁵; measured 1 to 4 × 10⁻¹⁵. pred(Z = 0) 2 to
5 × 10⁻¹⁴ and pred(Z = 0.3) 1 to 2.5 × 10⁻¹³, so **CUSP EXCLUDED / CUSP EXCLUDED** by a factor of 5 or more over
measured + 2 σ, in every bracket; Part C: brighter.

## Limits

Spherical, hydrostatic, single-phase gas in collisional ionisation equilibrium. Photometric lens redshifts; the far
source is the least mass. Three stated factors (0.80, 0.40, the Γ = 2 conversion) rest on memory, not on a fitted
response; each is set on the side that lowers the prediction, and EXR1's response-folded route is the cross-check.
Gas colder than hydrostatic emits below the band and is not tested. AGN or group emission at a lens adds flux, which
works against EXCLUDED. Not blind. It tests no part of a₀ or κ.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
