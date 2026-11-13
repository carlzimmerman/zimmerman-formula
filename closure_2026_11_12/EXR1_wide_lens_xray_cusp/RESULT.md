# EXR1 (WIDE-LENS X-RAY CUSP): RESULT

**Frozen word: NOT EVALUABLE / NOT EVALUABLE** (canonical / alt). Instrument check K8 failed because the criteria
were wrongly designed (`AMENDMENT_A1.md`). **Post hoc reading A1: EXCLUDED / EXCLUDED**, the same in every bracket;
the frozen measurement read conservatively (reading R) is also EXCLUDED. Part C: frozen NOT EVALUABLE; post hoc
reading WIDE LENSES ARE BRIGHTER IN X-RAYS.

ESZ1 left law S one hot gas body: a cusp, ρ ∝ r⁻², around Euclid's wide lenses. eRASS1 sees about a thirtieth of the
least X-ray flux that gas must emit; not a word, because a frozen check failed. No outcome here is a pass. 2026-11-12.
Criteria `0cc195b7f6` (alone, first); frozen run `726d2a6ba8`; amendment `676977b65b` (alone); A1 run `07360f21b4`.

## The numbers

Units: 10⁻¹⁵ erg s⁻¹ cm⁻², eRASS1 catalogue-equivalent 0.2–2.3 keV flux (absorbed, Γ = 2 convention) in the
upper-limit service's ~30″ aperture. Canonical / alt where two values are given.

| | |
|---|---|
| Wide lenses (θ_E ≥ 1.7″) in the eROSITA-DE sky, all tested | **263 of 316** (exposure 221 s, background 1.05 counts) |
| Measured stack, frozen (no offset subtraction; σ = null rms) | +5.80 ± 1.77 |
| Measured stack, A1 (lens minus its 8 positions 0.5° away) | **+4.19 ± 0.85** |
| Least prediction (far source, stars +0.10 dex, Z 0.1, r ≥ R_E and inside 10″, aperture factor 2/3, N_H 2 × HI4PI) | **141.7 / 121.3** |
| Margin, A1 | 161 / 137 σ; 24 / 21 × (measured + 2σ); 34 / 29 × measured |
| Same, frozen numbers (not a word) | 77 / 65 σ; 15 / 13 × (measured + 2σ) |
| Z = 0 (H and He only), A1 | 78.0 / 67.3, 13 / 11 × (measured + 2σ) |

Under A1 and R, every bracket reads EXCLUDED on both footings: Z = 0, Z = 0.3, N_H = 1 × HI4PI, point source,
r_in = R_E/2, r_in = 1 kpc (602 / 541), grade A only (159), z_l ≤ 0.6 only (172). Also reported: Z = 1.0 (429 / 373),
sources near z ≈ 2 (377 / 334), Salpeter stars (190 / 164). At 2σ the stack allows at most **20 / 22 %** of the
required gas mass at the same profile and temperature (R: 23 / 25 %). To hide, the gas would have to sit below
**0.16 × its hydrostatic temperature** (about 0.08 keV at R_E), where it emits below the band.

**What law S needs** (median, least setting): 3.15 / 2.73 × 10¹² M☉ of gas inside 300 kpc (4 / 8 % of lenses need
none), kT 0.48 keV and n_e 0.20 / 0.18 cm⁻³ at R_E (12.6 kpc). The gas at r ≥ R_E alone emits 1.6 / 1.3 × 10⁴⁴
erg/s (rest 0.2–2.3 keV, Z 0.1); down to 1 kpc it emits 2.0 / 1.6 × 10⁴⁵. Its cooling time at R_E is 44 / 49 Myr at
Z 0.1 and 26 / 29 Myr at Z 0.3.

## Why the frozen word is NOT EVALUABLE

K8 asked the 8 null stacks to average within 3σ/4 of zero; all eight are positive, averaging +1.61 against a limit of
1.33. A random 30″ aperture holds a catalogued source 1.9 % of the time and eRASS1's smooth background map leaves
detected sources out, so random apertures have a positive mean. ESZ1's test assumed zero-mean nulls because ESZ1
subtracted offsets; EXR1 did not (to stay conservative) but kept the test. The amendment adds two readings and moves no
threshold: A1, ESZ1's own lens-minus-offsets construction (K8 passes: null mean 0.000, largest 1.36 against σ 0.85),
and R, the unsubtracted stack with σ from the null scatter about its mean.

## Part C, Part L, Part D

**Part C** (263 pairs; median |Δz| 0.010, |Δ log M★| 0.072): wide minus control +3.11 [+1.21, +5.02]; controls
+2.69 ± 0.56. The frozen word is NOT EVALUABLE: the script applies the checks to Part C, as ESZ1's did. The post hoc
reading, WIDE LENSES ARE BRIGHTER IN X-RAYS, is safe from the sky offset, which cancels in the difference. It fits
EUC6's richer environments and ESZ1's Part C, where the excess showed only on the CIB-deprojected map.
**Part L, per lens:** the least prediction is a median 0.83 / 0.66 of eRASS1's own 3σ bound at the lens. eRASS1's
bound lies below the prediction for 127 / 111 of 263 lenses. An empty aperture could do that for 142 / 129. A
Main-catalogue source lies within 30″ of 16 lenses (6.1 %, against 1.9 % by chance; median flux 31.5, largest 208).
Single lenses mostly cannot decide; the stack does. **Part D:** the stack as a mean luminosity is 5.4 × 10⁴² erg/s
(no K-correction). Other lens classes (frozen measurement): 1.3–1.7″ +3.30 ± 0.47 (543); 1.0–1.3″ +2.77 ± 0.31 (971);
below 1.0″ +2.41 ± 0.31 (3,156).

**Checks and twins.** K1–K7 pass; K8 fails. K1 APEC read from AtomDB 3.1.3 against CFG581's pyatomdb values −1.4 % / +2.1 %; K2 band ECF
ratios 0.887 / 1.281 / 0.952 against 0.858 / 1.265 / 0.944; K3 UL_B recomputed (Kraft–Burrows–Nousek, 99.87 %) at all
4,933 de_sky lens positions, largest deviation 7.5e-4; K4 on 39 eRASS1 groups with kT to 30 %: count rate per flux
0.982, flux to luminosity 1.034, L500 over the least luminosity of their gas mass 2.51; K5 3.7e-7; K6 exact; K7 60.8 σ,
60 of 60. Twins all exit 1: `inject` ALLOWED / ALLOWED, `shift` K7 fails, `newton` pred_min 348 / 348, A1 `inject`.

## Reading (mine; not part of the word)

1. Taken with ESZ1, no hydrostatic hot gas body tested supplies the wide lenses under law S. Pressure rules out the
   cored bodies, and X-rays rule out the cusp (post hoc: 24 / 21 times measured + 2σ in the least setting, at least
   11 times in every bracket, Z = 0 included). Not tested: gas below about 0.08 keV, multiphase or clumped gas, other
   profiles, non-baryonic components. The hydrostatic cusp itself would cool in 26–49 Myr.
2. For the wide-lens residual, this says it is not hot gas in any tested hydrostatic form. It does not say what it
   is, and the framework still has no constructed state for it. Nothing passes, and nothing fails beyond this body.
3. The wide lenses' extra X-ray flux over matched small lenses, about 3 × 10⁻¹⁵ (2.5 × 10⁴² erg/s), is about what a
   group emits. That is under a fortieth of what the cusp needs.

## Disclosures

- **Order of runs.** The frozen script first ran on the cached upper limits with an empty cone table (pipeline test)
  and printed every number but Part L and K7's recovery leg; K8's failure showed there. One output-only file
  (`exr1_arrays.npz`) was then added to `exr1.py`; then the frozen run; then the amendment.
- K7's stack leg reads 7.1 σ on clusters moved 0.5° (the same sky offset), so `shift` bites only through K7's
  recovery leg (4 of 60). `inject` passes K8 only because the injected values raise σ to 15.0.
- **Known before freezing** (lens-free positions; listed in the criteria): the ECF, the absorbed convention, the
  upper-limit formula and the K4 group ratios. **PROVISIONAL, from memory:** K4's cosmology for the groups (H₀ 70,
  Ω_m 0.3) and their Z = 0.3; K4(a, b) pass at 2–3 %. The Morrison & McCammon table was checked against the scanned
  paper. The PSF bound behind the 2/3 aperture factor is stated, not fitted.
- **Downloads:** AtomDB 3.1.3 (185 MB, md5 as CFG580's), one source product (1.7 MB), 407 scripted requests (11.6 MB);
  outside git with manifests (scripted manifest copied here).
- **Hand estimate against outcome:** N 263 (≈ 263); σ 0.85 (≈ 1); median prediction 4.6e-14 (5e-14; the stack mean,
  1.4e-13, is pulled up by low-redshift lenses); measured 4–6e-15 (2–5e-15); cooling 26–49 Myr (10–30). The lead's
  2e44 / 3e45 erg/s came out at 1.6e44 / 2.0e45, and its 40 Myr at 26–49 Myr. Its "nearly every lens a bright
  catalogued source" was wrong: per lens the least prediction sits below eRASS1's 3σ bound.
- Controls re-drawn inside the eROSITA-DE sky with ESZ1's rule (not ESZ1's pairs). No independent re-grade has run.

**Limits.** Spherical, hydrostatic, single-phase gas in collisional ionisation equilibrium; photometric lens redshifts
(the far source is the least mass); a stated PSF bound. AGN or group emission at a lens adds flux, which works against
EXCLUDED. It tests no part of a₀ or κ.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
