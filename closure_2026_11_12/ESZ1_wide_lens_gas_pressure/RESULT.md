# ESZ1 (WIDE-LENS GAS PRESSURE): RESULT

**Part G: ONLY A CUSP IS LEFT / ONLY A CUSP IS LEFT** (canonical / alt), unchanged in all five brackets.
**Part C: NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map].**

The hot gas that law S would need to supply Euclid's wide-separation lenses from an extended gas body is not there.
A body with a core (30 or 100 kpc) is excluded by its own pressure at 19 to 114 σ. A body cusped on the lens centre
(density ∝ r⁻²) needs so little pressure that this map cannot see it either way. No outcome here is a pass.

2026-11-12. Criteria `07a07ec1a6` (committed alone, first); script and run `c107fd8afe`. TEST lane; adopts nothing.

## The numbers

Units: 10⁻⁶ arcmin² of integrated Compton-y in a 2′ compensated aperture. Canonical / alt where two values.

| | |
|---|---|
| Wide lenses stacked (θ_E ≥ 1.7″, inside the map, ≥ 12 covered offsets) | 237 of 316 |
| Measured stack | **+3.83 ± 1.47** |
| Same lenses moved half a degree (twin `shift`) | +0.20 ± 1.52 |
| Least pressure needed, 30 kpc core (B30) | 37.2 / 32.4, so 22.7 / 19.4 σ above the measurement |
| Least pressure needed, 100 kpc core (B100) | 171 / 145, so 114 / 96 σ above |
| Least pressure needed, r⁻² cusp (G2) | 2.03 / 1.86, below 3 σ = 4.4: NO POWER |

"Least" means the least demanding setting the criteria allow: source at infinite distance, stars 0.10 dex heavier
than Salpeter, zero confining pressure at the gas edge. At Salpeter stars the cored bodies need 48.6 / 42.8 (B30)
and 227 / 194 (B100); with sources near z ≈ 2 (the central case), 88 to 134 and 412 to 672.

- **How much is missing.** At 2 σ the stack holds at most 18 / 21 % of B30's least pressure and 4.0 / 4.7 % of
  B100's. Gas could hide only by sitting 5 times (B30) or 21 to 25 times (B100) below its hydrostatic temperature.
- **What law S would need** (median, least setting): B30 2.2 / 1.8 × 10¹³ M☉ at 0.94 keV; B100 5.4 / 4.4 × 10¹³ M☉
  at 1.5 to 1.6 keV; G2 3.2 / 2.8 × 10¹² M☉ at 0.41 keV with 0.20 / 0.18 electrons per cm³ at the Einstein radius.
- **What the stack is, as gas.** ∫P_e dV = (8.7 ± 2.6) × 10⁵³ J per lens: 5.2 × 10¹² M☉ if the gas is at 1 keV
  (10.4 at 0.5 keV, 2.6 at 2 keV); 2 σ upper limit 8.3 × 10¹² M☉ at 1 keV, 16 mean stellar masses.

Brackets (measured ± σ; lane word the same on both footings in each): CIB-deprojected map +4.36 ± 1.91;
θ_d = 1.5′ +1.49 ± 1.02; θ_d = 3.0′ +7.19 ± 2.95; grade A only (141) +4.52 ± 1.88; z_l ≤ 0.6 only (154)
+1.27 ± 2.02.

## Part C: wide lenses against matched controls

237 pairs (median |Δz| 0.010, median |Δ log M★| 0.069). Mean difference, wide minus control:
+4.17 [−0.20, +8.67] on the primary map, +7.12 [+2.12, +12.16] on the CIB-deprojected map. The frozen word on the
primary map is NO EXCESS DETECTED; the bracket reads an excess, so the word carries the tag. Stacks: wide
+3.83 ± 1.47, controls −0.34 ± 1.64.

## Part D: what the stack measures (no word)

| Class | N | Y, primary | Y, CIB-deprojected | gas at 1 keV (10¹² M☉) | 2 σ limit |
|---|---|---|---|---|---|
| W, θ_E ≥ 1.7″ | 237 | +3.83 ± 1.47 | +4.36 ± 1.91 | 5.2 | < 8.3 |
| Controls | 237 | −0.34 ± 1.64 | −2.76 ± 1.89 | −0.5 | < 3.0 |
| 1.3–1.7″ | 474 | +0.42 ± 1.21 | +0.80 ± 1.27 | 0.9 | < 3.4 |
| 1.0–1.3″ | 876 | +0.60 ± 0.95 | +0.99 ± 1.37 | 0.8 | < 3.2 |
| below 1.0″ | 2,863 | +0.61 ± 0.44 | +0.25 ± 0.55 | 0.7 | < 1.9 |
| All valid S | 4,450 | +0.76 ± 0.38 | +0.67 ± 0.48 | 1.0 | < 1.9 |
| L, flagged large systems | 100 | +27.5 ± 4.0 | +25.6 ± 4.0 | | |

W at the three apertures: 1.5′ +1.49 ± 1.02; 2.0′ +3.83 ± 1.47; 3.0′ +7.19 ± 2.95.

**Cold-share reading (EUC8).** Taking EUC8's r⁻² component as cold dark energy (median 4.0 / 3.6 × 10¹² M☉ inside
300 kpc), the 5.41 share asks for 7.4 / 6.7 × 10¹¹ M☉ of baryons there, so 2.4 / 1.6 × 10¹¹ M☉ of gas beyond the
stars (30 / 35 % of lenses need none), at 0.52 keV. Its least pressure is 0.29 / 0.26 against σ = 1.47: **no
power**, as the criteria expected. The measured stack is above it by 2.4 σ, which the criteria ask to be stated; it
is not a test of the share.

## Checks and twins

All nine pass. K1 geometry 2.9e-11 pixel. K2 new files 559,699,200 bytes each; seam correlation 0.990 against 0.992
and 0.993 against 0.992. K3 prediction against brute-force rendering: B30 0.06 %, B100 0.07 %, G2 0.56 %.
K4 hydrostatic solver 3.1e-5. K5 beam 4.5e-5 and 1.3e-5. K6 EUC4 Part B reproduced (N = 316; 13.44 / 13.37,
13.84 / 13.77). K7 EUC8 reproduced exactly. K8 eRASS1 clusters: N = 1,643, +78.2 ± 1.9, 41 σ. K9 nulls: mean 0.000,
largest 3.76 (2.6 σ).

Twins, all exit 1: `inject` (B100's least pressure added to every W lens: B100 reads ALLOWED / ALLOWED, lane word
HOT GAS NOT EXCLUDED); `shift` (K8 fails: clusters −0.35 ± 0.56); `newton` (B100's least pressure rises to 505).

## Reading (mine; not part of the word)

1. EUC4 Part B said law S would need 10 to 30 times the gas X-ray groups hold, quoting that range from memory.
   This lane measures it on the lenses themselves: an extended gas body is ruled out by a wide margin, on both
   footings, in every bracket.
2. What pressure cannot rule out is gas piled on the centre. That is an X-ray question, not an SZ one: 0.2
   electrons per cm³ at 12.6 kpc and 0.4 keV would be very bright and would cool quickly (my estimate from memory,
   not computed here: 10⁴⁴ to 10⁴⁵ erg/s per lens, cooling time tens of Myr). A stack of eROSITA data on the same
   237 lenses would settle it.
3. The wide lenses do show some gas pressure (2.6 σ; matched controls show none), about a seventh of what the
   expert-flagged large systems show. That fits EUC6's richer environments, but by this lane's own rule it is not a
   detection of an excess.
4. For the framework: nothing passes and nothing new fails. The residual in wide lenses is not hot gas in any
   extended form, so it is either a central cusp of gas or not baryonic gas at all. The framework still has no
   constructed state for it.

## Disclosures

- **Seed.** The first run drew a separate bootstrap stream per statistic, so the same stack's σ printed as 1.47 to
  1.54 in different places. The criteria name one seed (20261112). The run was repeated with it. No word and no
  per-lens value changed (`esz1_per_lens.csv` byte-identical); the first run is kept as `esz1_run1_seeds.*`.
- **Coverage.** 4,735 of 6,173 S positions lie inside the map rows and are finite; rule (iii) keeps 4,482; 4,450
  have at least 12 covered offsets.
- **K9** is weak in its second half: σ is defined as the larger of the bootstrap and the null-stack rms, so a null
  stack beyond 3.5 σ is nearly impossible by construction.
- **Download.** Before this lane the owner was told the map on disk covered the lenses; it covered a quarter of
  them. The southern rows (2 × 559.7 MB, NASA LAMBDA) were fetched on 2026-11-12 with the owner's go.
- **Hand estimate against outcome.** N 240 (237); σ 1.5 to 2 (1.47); B30 20 to 40 (37 to 60); B100 30 to 60 (171 to
  286: low by a factor of 4 to 5); G2 about 3 (2 to 3); lane word and Part C's primary word as expected; the
  bracket dependence of Part C was not foreseen.
- No independent re-grade has been run.

## Limits

Spherical; hydrostatic; y sees pressure, not mass. Photometric lens redshifts; no source redshifts. Lensed sources
are dusty and massive ellipticals host radio sources; the CIB-deprojected bracket covers only the first. The 2′
aperture is 712 kpc at the median redshift 0.45 (755 kpc at 0.5; the criteria's "730" was a rounding slip), so
neighbours add pressure, which works against EXCLUDED.
Coverage is set by local noise, a proxy for the survey mask. It tests no part of a₀ or κ.

## Commit ids (local / origin)

Criteria `07a07ec1a6` / `a22f1554b2`; script and run `c107fd8afe` / `eb08cfdcbc`; result `eb59dcf96b` /
`41b11ac851`. Pushed by replay onto origin's tip, so the two histories carry different ids for the same content.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
