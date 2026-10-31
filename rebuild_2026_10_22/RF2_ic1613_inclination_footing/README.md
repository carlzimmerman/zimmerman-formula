# RF2_ic1613_inclination_footing: FAILS under every halo-free inclination, both footings. IN2's failure does not rest on the MUSE number. It is disfavoured, not excluded

Criteria and ledger 6b060cbb33 (committed alone, before any script or number); script 11a69cd226; no amendment. One class was
added at the freeze, MIXED, and it did not fire. No new data. **No new falsifier; IN1's stands.**

## Verdict (frozen): **FAILS under every halo-free inclination** (canonical and alt)

"FAILS" means IN1's frozen falsifier is met: central i ≥ 30°. It does not mean excluded.

| row | class | median [16–84] | P(IN1 band) can / alt | density at 22.5° / peak | status |
|---|---|---|---|---|---|
| Optical isophote, ε 0.20 ± 0.05, e_int 0.10 | photometric | 34.4 [24.5–42.5] | **0.143 / 0.109** | 0.41 | QUALIFYING, FAILS |
| HI footprint, measured here, e_int 0.10 | rendered moment-0 map | 37.9 [27.8–45.8] | **0.089 / 0.067** | 0.23 | QUALIFYING, FAILS |
| Lake & Skillman 1989, 38 ± 5 | HI, second-hand, PROVISIONAL | 37.9 [32.9–42.8] | 0.011 / 0.005 | 0.008 | QUALIFYING, FAILS |
| MUSE Read+16 formalism, 36 ± 11 | stellar-kinematic comparator | 35.9 [25.0–46.8] | 0.138 / 0.108 | 0.47 | comparator, FAILS |
| MUSE Weijmans+08, 32 ± 11 | stellar-kinematic comparator | 31.9 [21.0–42.8] | 0.199 / 0.161 | 0.69 | comparator, FAILS |
| Oh+15 tilted ring, 48 (held fixed) | HI kinematic | 48, no usable error | none | none | central only |
| Read+16 39 ± 2, 15° | mass-model fit, ΛCDM-PROCESSED | | 0.000 | 0.000 | BRACKET |
| Collins & Read 2022 ~20° | BTFR imposed, circular here | | | | BRACKET |
| TRGB geometry; moment-0 FITS | NOT ON DISK | | | | |

## The answer to the question

**None of IN2's failure rests on the Read+16 number alone.** Removing both MUSE rows leaves the class unchanged. The two
geometric rows give P(band) about the same as MUSE or smaller, so the single number was not doing special work.

**IN1's prediction at those inclinations** (canonical, q_σ 0.6): at i = 37°, E_HI −0.410 (Z −5.46), E_σ −0.096 (Z −1.21). Alt: −0.448 (−5.97), −0.134 (−1.70). The HI
tracer carries the failure. The stellar σ tracer stays inside 2σ out to 48.5° (alt 41°) on IN1's masses.

## How firm this is

The result is a clear central value with thin margins. Against it:

- **The band keeps real probability under each first-hand row.** 9–14 % canonical. No combined probability is given: the rows
  are not shown to be independent, and Lake & Skillman's argument compares HI and optical isophotes.
- **It depends on e_int, which I declared.** e_int is the intrinsic ovalness of the disc, unsourced on disk.

| e_int | optical median, half-width, P(band), class | HI median, half-width, P(band), class |
|---|---|---|
| 0 | 36.7, ±4.8, 0.027, FAILS | 39.6, ±5.7, 0.021, FAILS |
| 0.05 | 36.4, ±5.8, 0.059, FAILS | 39.3, ±6.5, 0.038, FAILS |
| **0.10** | 34.4, ±9.0, 0.143, FAILS | 37.9, ±9.0, 0.089, FAILS |
| 0.15 | 29.7, ±13.4, 0.207, BETWEEN | 34.5, ±12.8, 0.152, FAILS |
| 0.20 | 26.0, ±15.4, 0.219, CONSISTENT | 30.2, ±15.5, 0.193, FAILS |

  The optical row stops failing above e_int 0.14. The HI row holds through 0.20. **The ±10° gate holds for the first-hand rows
  only up to about e_int 0.10.** Above that, or with a prior flat in i (half-width ±11.7, medians 30.8 and 34.8), the only row
  under ±10° is Lake & Skillman's, which I have not read. Dropping that row in those cases would read UNDETERMINED.
- **Disc thickness goes the other way.** q₀ 0.2 / 0.4 / 0.6 moves the optical median up to 37.7 / 40.9 / 49.1, P(band) 0.022 to 0.003.
- **Optical PA 90 ± 1 and HI PA 72 ± 2 differ by 18°.** So the optical disc is not a thin circular disc, and this is why e_int
  is not zero. The HI footprint's PA is 70.8 ± 8.2, close to the kinematic 72–73.7, with no kinematics used. That supports the
  map measure.

**HI footprint.** b/a 0.769, PA 70.8, 8804 px; ε 0.231 ± 0.064 (boot 0.047, method spread). Variants b/a 0.710 (raw mask, no fill), 0.736,
0.795; intensity-weighted, reported only, 0.700. It is a published figure at about 72 ppi with holes, not the FITS. The fill and dilation
round it slightly: the injected test returned 0.816 for 0.80. 6 % of the panel's edge band is in the footprint, so a
small clip by the panel, beam or S/N mask cannot be ruled out. **The FITS moment-0 map would improve this row.** K4's scale (4.9 px/arcmin) was read by eye from panel (d)'s
ticks and only guards a factor 2.

## Verifying the fail

- **The stellar mass matters more than the inclination.** IN1's band and its σ pass use LITTLE THINGS' SED M★ 2.88e7. At X1 / LVD's
  1.9e8: **the σ tracer has no consistent inclination at all, on either footing**, and I_HI moves to 14–19.5° (alt 13.5–18.5°). So at that mass it fails at every i
  on the σ tracer, and the HI band sits lower still. Here IN1's mass is the kinder choice; this lane was not asked to choose between them.
- s ± 0.01 moves I_HI by at most 0.5–1° (19–25.5°, 18–27°).
- Framing from Taibi+24 (read from TeX; IN2): the HI curve rises unusually slowly, attributed there to holes in the HI, and a value
  near 35° would make IC 1613 a BTFR outlier in their framework too. Context, not a rescue.

**Read plainly:** on-disk geometry puts IC 1613 near 34–38°, where the law misses its HI curve at Z about −5. It rests on geometry and on the HI curve, not on the Read+16 formalism. It is not an
exclusion, and it remains one galaxy with a disturbed HI disc.

## What would improve it (owner's OK needed)

1. LITTLE THINGS IC 1613 moment-0 FITS (replaces the rendered panel).
2. Lake & Skillman 1989 itself, to know what the 38 ± 5 measures.
3. A measured e_int distribution for dwarf irregular discs, or deep-photometry isophotes with radius (Higgs+21; Bernard+ style star maps), to replace the declared 0.10.
4. A published TRGB distance gradient across the disc, if one exists.

## Checks (`rf2_ic1613.out`)

K0 HO3 −0.5352, RT1 −0.5928. K1 I_HI [18.5, 26.5], [18, 25]. K2 thin circular limit 36.75 against 36.87. K3 normalisation. K4 diameter 24.9′ against 2R_max 26.6′. K5 injected 0.80 / 70° returned 0.816 / 70.4°. K6 RSS.
7/7, rerun byte-identical (`ca21620597d7…`). MUTATE (`RF2_MUTATE=1`): K2 gives 53.00, FAIL, exit 1.

Rerun: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf2_ic1613.py`.

κ = ½ FITTED; c_f not used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
