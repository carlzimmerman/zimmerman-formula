# EUC3 (NISP SOURCE REDSHIFTS): RESULT

2026-11-12. Criteria bf72d787a8 (alone, before any script and before any grism row of a lens or grade-X object was
queried). First pass 5a5d3feeca (preserved as seen). Post hoc diagnostics 133adb2f73 (disclosed, before their script ran).

## Verdict: NOT EVALUABLE / NOT EVALUABLE (canonical / alt). EUC1-F stays open.

The frozen rule finds a "secure" source redshift in 1.53 % of Euclid's lenses and in 1.28 % of the grade-X systems the
experts judged not to be lenses. The purity null fails at both frozen tiers, so by the frozen ladder no reading is
made. Euclid's public DR1 grism catalogue does not carry lensed-source redshifts that can be told apart from what a
non-lens gives. All instrument checks pass; both mutation twins exit 1.

κ = ½ FITTED. No outcome favours the framework. Nothing here bears on the law.

## 1. What was searched

14,958 grade A/B lenses with an Einstein radius and 2,580 grade-X systems: 27,534 MER objects within 3″, their red-grism
quality, redshift, line, photo-z and class rows (IRSA TAP, anonymous, paced; 70 table chunks; six re-queried chunks
identical).

| Set | N | Evaluable (a usable grism spectrum, a lens object, a redshift interval) |
|---|---|---|
| P (EUC1's gate sample) | 3,192 | 1,177 (36.9 %) |
| S (grades A+B) | 6,173 | 2,282 (37.0 %) |
| all grade A/B | 14,958 | 5,253 (35.1 %) |
| X (null) | 2,580 | 934 (36.2 %) |

Two thirds of lens objects have no wide-survey spectrum with ≥ 300 valid pixels and more than three dithers.

## 2. Gates

| Check | Result |
|---|---|
| K1 EUC1 reproduced | N(P) = 3,192; source-free median b −0.0185 / −0.0439 (pass) |
| K2 EUC2 anchor L015763 | +0.2314 / +0.2149 against +0.231 / +0.215 (pass) |
| K3 association | lens object carries ECLIPSE's MER id: S 98.3 %, X 96.9 %; never a different object (pass) |
| K4 apertures | median radius S 1.565″, X 1.567″ (pass) |
| K5 fetch | complete; re-queries identical (pass) |
| **H2 purity null, tier T5 (Hα S/N ≥ 5)** | **X: 12 of 934 pass the rule; limit 2.9. FAIL.** S: 35 of 2,282; P: 18 of 1,177 |
| **H2, tier T8 (S/N ≥ 8, frozen fallback)** | **X: 7; limit 1.8. FAIL.** S: 22; P: 11 |
| H4 truth | 0 of 3 recovered, 0 contradicted (pass; recovery is not a gate) |
| MUTATE newton | anchor b +0.231 / +0.215 → +0.330 / +0.330; P median +0.251 / +0.236 → +0.347 / +0.347; exit 1 |
| MUTATE noguard | X hits 12 → 68, S hits 35 → 144; exit 1 |

Rates with 95 % intervals, T5: S 1.53 % [1.07, 2.13]; all A/B 1.83 % [1.48, 2.23]; X 1.28 % [0.67, 2.23]. The null
predicts 15 false among P's 18 and 29 among S's 35.

**The null hits are real galaxies, not noise.** Six of the twelve show a second line; the brightest (EUCL-DR1-L022970)
has Hα at S/N 21 and [S II] at S/N 6 at z = 1.266 against a photo-z of 0.72. They are emission-line objects well above
their photo-z interval, or chance neighbours. A lens with a wrong photo-z or a projected neighbour looks the same in
the catalogue. A second code path recounts the eight lens-object hits in X exactly.

**The truth set.** EUCL-DR1-L015763 (DESI z_s = 1.3657): the lens object's best solution is z = 2.1144 with probability
1.000, the line read as [O III]; the Hα reading of the same line is the second solution, z = 1.3768. The 0.011 offset is
what an arc 1.6″ from the extraction centre gives in a slitless spectrum. L012826 and L014688 have no object in the
wide-survey MER table. So the catalogue's first solution fails on the one known pair it could have found.

## 3. The reading that was printed (VOID; seen, not used)

| Sample | N | Median b at the catalogue redshift [95 %], canonical | alt | Same lenses, source-free |
|---|---|---|---|---|
| P | 18 | +0.251 [+0.079, +0.421] | +0.236 [+0.063, +0.403] | −0.127 / −0.152 |
| S | 35 | +0.292 [+0.206, +0.397] | +0.277 [+0.190, +0.384] | −0.119 / −0.142 |
| U, not quality-cut | 91 | +0.422 [+0.333, +0.518] | +0.408 [+0.319, +0.509] | +0.002 / −0.022 |

This is not EUC1-F and not an early reading: most of these redshifts are not lensed sources. Six of P's 18 pair a lens
photo-z of 0.93–1.04 with a "source" 0.2–0.7 above it, and three of those need 3 to 11 × Salpeter, the mark of a wrong
pairing. Had the gate applied, the word would have been NO VERDICT on both footings. Robustness rows are in `euc3.out`; they inherit
the same void.

## 4. Post hoc diagnostics (disclosed; none is a verdict)

Is the failure a product of how the null was built? Grade-X objects are fainter (median H flux 38 against 74 µJy).

1. **Threshold.** X against S at Hα S/N ≥ 5 / 8 / 12: 1.28 / 0.75 / 0.43 % against 1.53 / 0.96 / 0.31 %. Fails at each.
2. **Matched null.** X reweighted to S's brightness and redshift distribution: 0.87 %. Expected false among S's 35:
   19.9 (57 %), against the 20 % line. Fails.
3. **Excess.** S − X = +0.25 % [−0.63, +1.13]; all A/B − X = +0.54 % [−0.27, +1.35]. Real sources this allows among
   P's 18: 2.9 [0, 14.7].
4. **Splits.** Bright deflectors: S 1.93 % against X 0.74 % (2 of 271). Faint: 1.14 % against 1.51 %. Hits on the lens
   object: 1.49 % against 0.86 %. A lens excess may exist among bright deflectors; it is far from separable.
5. **The own-line guard does real work** (seen in the census; not in the diagnostics plan). It set aside 73 S systems:
   49 in the [S III] 9533 band against 26 expected if hits were spread evenly in redshift, 19 in the He I band against
   17. Deflectors' own [S III] is being read as Hα about as often as a real source is found.
6. L015763 at its second-solution redshift reads +0.231 / +0.214, as EUC2 found at the DESI redshift.

## 5. What this means

1. **Euclid's lens gate cannot be graded from the public grism catalogue.** A redshift above the deflector turns up
   in non-lenses as often as in lenses, so at most a handful of the 18 in sample P are real and no one can say which.
2. **EUC1-F stays open and EUC1 stays NO VERDICT / NO VERDICT.** The law's saturation ceiling is neither passed nor
   broken by the November release.
3. **The information is in the spectra, not in the catalogue's first solution.** The one known pair has the right
   redshift as its second solution, displaced by the arc's offset.
4. **Two routes remain.** Row-level source redshifts from the ECLIPSE follow-up (Storfer et al.; 4MOST), which is what
   EUC1-F was written for. Or a lane on the extracted grism spectra themselves (IRSA's object-to-spectrum table): fit
   the line at the arc's offset with the deflector's continuum removed, graded by the same grade-X null. Not run here.

## 6. Disclosures

- The fetch ran in two parts (S, truth lenses and X first; the other A/B lenses after), partly as two request
  streams. The service ends a job after about five minutes; a few requests timed out and were retried.
- `euc3.py` changed twice after the first pass, outputs only (`euc3_systems.csv`; twins write no tables). The complete
  run reproduces the first pass for P, S and X line for line.
- Selection, as frozen: 0.84 < z_s < 1.88 and Hα ≥ 2e-16 erg s⁻¹ cm⁻². The guards close 68 % of that window for the
  average evaluable lens of S (the criteria's "58 %" was computed from the ECLIPSE interval alone; the frozen union
  with the pipeline photo-z interval is wider). Lenses whose sources lie elsewhere are not addressed.

## 7. Files

`euc3_fetch.py`, `euc3.py`, `euc3.out`, `euc3_results.json`, `euc3_sources.csv` (245 lens systems with a class; the
91 "secure" ones with usable inputs carry b), `euc3_systems.csv` (every evaluable system), `euc3_MUTATE_*.out` / `_results.json`,
`euc3_interim.*` (first pass), `POSTHOC_DIAGNOSTICS.md`, `euc3_posthoc.py`, `euc3_posthoc.out`, `_results.json`.

Commits (local / origin): criteria bf72d787a8 / 17a2678a40; scripts and first pass 5a5d3feeca / 67992a8339; post hoc
plan 133adb2f73 / a4efbec24c. Tables are outside git (`_external_data/euclid_dr1_eclipse/nisp_tables/`).

    python3 -I euc3_fetch.py --data-dir <dir> --part first      (then --part rest --sys-chunk 600)
    python3 -I euc3.py --data-dir <dir>
