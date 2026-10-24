# X11_cross_shear_diagnosis: is X7's cross-shear offset a systematic or a fluctuation?

Criteria: `FROZEN_CRITERIA.md` (committed alone, 9a105431c9; amendments A1–A4 below). Inputs and classes:
`ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not
"theory closed". Nothing here says the data favour the framework.

## Verdict (frozen classes; JSON keys in `x11_analysis_results.json`)

**CONSISTENT WITH A FLUCTUATION** (`verdict`).
- No pre-declared split or correlation of the cross-shear MID offset reaches Δχ² ≥ 9 or p_const < 0.0027 in any cell
  (`candidates_any_cell`: 19 variables × 4 cells, none). The largest is psfE4: Δχ² 5.6–6.1, p_const 0.008–0.054.
- The same rule applied to pure-noise rotations fires in 4.5–5.5 % of realisations (`look_elsewhere`).
- All three nulls pass (`N1`, `N2`, `N3`).
  - The extended random points give a cross level of +0.000 ± 0.022 (Z +0.02 / −0.39).
  - The per-cluster excess variance is χ² 316 / 308 for 312 clusters (p_var 0.44 / 0.52).
  - The 90° identity holds to 2e-13.

**Z_MID = STAT** (`Z_MID`): 5.21 / 5.47 canonical (h 0.672 / 0.686), 4.47 / 4.74 alt. That is REAL by X7's rule. The cross
offset beside it has p_× = 0.015 / 0.010 / 0.015 / 0.010 (200 rotations; `all_MID.<cell>.p_x`).

**What that verdict does not settle: the tangential excess depends on source size** (`E3_sub`: E-MODE SOURCE DEPENDENCE
FOUND: size2, size4). This is a frozen sub-verdict, reported beside the main class and never changing it.
- **Halves** (`E3.<cell>.size2`, paired bootstrap): small sources give A_MID 1.10–1.24 (Z_STAT +0.9 to +1.8, consistent with
  the law). Large sources give 1.86–2.11 (Z_STAT +5.1 to +6.1). Δχ² = 15.9–17.4 in all 4 cells.
- **Quartiles:** 0.81–0.91 / 1.34–1.49 / 1.29–1.49 / 2.04–2.44 (Δχ² 15.8–21.9).
- **Not the class boosts** (0.934 vs 0.920), **nor the count deficit** (0.861 vs 0.858), **nor the boost convention** (clipped:
  Δχ² 16.6–18.2; `per_class_boost_count`, `E3_clip`).
- The cross offset sits mostly in the small-source half: +0.35 to +0.46 ± 0.10–0.12 (no rotation reaches it), against +0.09
  to +0.11 ± 0.14–0.16 for large sources. The class difference is only Δχ² 2.0–2.9, so size is not a cross-shear candidate.
- The mechanism is not identified.

**So:** the cross shear gives no reason to treat the core excess as MARGINAL. Its offset behaves like noise, and about a third
of it came from F1's random points. But the excess is not established either: its amplitude depends on a source property it
should not depend on.

## Step 0: same data, same code (`x11_s0_check.out`: S0-1–S0-4 PASS)

- **X7's four scripts.** They ran unchanged through `x11_step0.py` (sha256-checked source; output paths only) on a cache rebuilt
  from the raw KiDS FITS in session scratch.
- **S0-1.** The 7 cache columns have X7's committed sha256.
- **S0-2.** All 25 arrays of the per-cluster npz equal X7's exactly.
- **S0-3.** 104 numbers of the analysis JSON equal X7's to 0.0: A_×, σ_n,×, p_×, rand_x, Z_STAT, Z_CAL, the cross profile χ²,
  and V1 MARGINAL.
- **S0-4.** All 18 X7 checks PASS.

| cell | A_× MID | σ_n,× | p_× | Z_STAT | Z_CAL (X7) |
|---|---|---|---|---|---|
| canonical h 0.672 | +0.205 | 0.091 | 0.015 | +5.21 | +2.93 |
| canonical h 0.686 | +0.236 | 0.096 | 0.010 | +5.47 | +2.78 |
| alt h 0.672 | +0.188 | 0.084 | 0.015 | +4.47 | +2.52 |
| alt h 0.686 | +0.216 | 0.088 | 0.010 | +4.74 | +2.41 |

## Step 1–2: the cross offset by split (A units, C\*, boost; ± rotated-noise σ)

The class values below are for canonical h 0.672. Δχ² and p_const are ranges over the 4 cells, against the rotation
covariance; the bootstrap covariance is in brackets. The last column is the **tangential** split (E3, paired bootstrap).
Keys: `splits.<cell>|<var>.{a, sig, Z, p, rot, boot}` and `E3.<cell>|<var>`.

| variable | cross offset per class | Δχ² (boot) | p_const | tangential Δχ² (E3) |
|---|---|---|---|---|
| tomo Z_B (0.1–0.3 … 0.9–1.2) | +7.6±4.6 / −0.07±0.56 / +0.27±0.19 / +0.21±0.18 / +0.17±0.17 | 0.03–0.04 (0.00–0.10) | 0.58–0.65 | 0.0–0.2 |
| mag2 (bright / faint) | +0.03±0.16 / +0.35±0.13 | 2.1–4.5 (2.5–4.8) | 0.033–0.145 | 0.1–0.2 |
| mag4 | +0.81±0.79 / +0.00±0.22 / +0.89±0.35 / +0.37±0.18 | 0.9–2.3 (0.1–1.7) | 0.09–0.18 | 0.6–1.4 |
| size2 (small / large) | +0.38±0.11 / +0.10±0.16 | 2.0–2.9 (1.8–2.5) | 0.09–0.16 | **15.9–17.4** |
| size4 | +0.30±0.15 / +0.30±0.16 / −0.05±0.18 / −0.55±0.88 | 2.4–4.4 (2.0–3.8) | 0.10–0.33 | **15.8–21.9** |
| psfT4 (PSF size) | +0.74±0.37 / +34±23 / +0.10±0.30 / −0.22±0.33 | 3.2–3.8 (2.8–3.4) | 0.09–0.11 | 0.7–1.6 |
| psfE4 (PSF ellipticity) | −0.58±0.27 / −0.4±4.7 / −0.07±0.43 / +1.36±0.65 | 5.6–6.1 (4.6–4.8) | 0.008–0.054 | 0.1–0.4 |
| psfx2 (PSF cross projection −/+) | +0.17±0.13 / +0.18±0.14 | 0.00 (0.00) | 0.96 | 0.0–0.3 |
| psft2 (PSF tangential projection −/+) | +0.10±0.14 / +0.33±0.14 | 0.7–1.1 (0.6–1.0) | 0.29–0.39 | 0.3–0.9 |
| nbr2 (close / far neighbour) | +0.12±0.12 / +0.29±0.14 | 0.7–0.9 (0.5–0.7) | 0.33–0.40 | 0.0 |
| dzls2 (Z_B − z_l < / ≥ 0.532) | +0.36±0.15 / +0.10±0.13 | 1.5–1.8 (1.8–2.0) | 0.18–0.22 | 1.4–3.4 |
| tile3 (tile seeing good / mid / poor) | +0.36±0.19 / +0.46±0.31 / −0.05±0.16 | 3.3–4.2 (2.4–3.3) | 0.05–0.13 | 4.2–6.5 |
| radial3 (MID bins) | +0.05±0.23 / +0.31±0.17 / +0.19±0.13 | 0.02–0.13 (0.04–0.05) | 0.65–0.89 | 8.3–9.6 (2 cells ≥ 9) |
| patch (N / S) | +0.34±0.13 / +0.09±0.14 | 1.1–1.5 (1.2–1.6) | 0.22–0.30 | 0.6–0.7 |
| z2 (≤ / > 0.223) | +0.23±0.12 / +0.17±0.14 | 0.00–0.09 (0.00–0.08) | 0.77–0.97 | 6.1–8.1 |
| mass3 (MGAS500 terciles) | +0.27±0.23 / +0.37±0.16 / +0.03±0.12 | 1.3–2.4 (1.4–2.5) | 0.18–0.41 | 2.4–2.5 |
| straddle2 (two+ tiles / one tile) | +0.21±0.13 / +0.19±0.16 | 0.01–0.23 (0.01–0.29) | 0.63–0.92 | 1.8–2.0 |
| aniso2 (coverage m = 2, low / high) | +0.18±0.12 / +0.24±0.15 | 0.09–0.32 (0.09–0.34) | 0.57–0.77 | 1.4–2.7 |
| off2 (X-ray offset, low / high) | +0.20±0.13 / +0.21±0.12 | 0.00–0.02 (0.00–0.02) | 0.89–0.99 | 0.5–0.7 |

- **Very large σ in some classes** (tomo bin 1, psfT4 Q2, psfE4 Q2) come from the frozen per-class weights W = 1/E². E is taken
  from the cluster's own shape variance, and in a class-bin holding one or two sources it can be tiny. Those classes carry
  almost no weight in the GLS, so they cannot create or hide a candidate.
- **Smallest-p items** (none reaches the line): psfE4 p_const 0.008 (h 0.686 only) and mag2 Δχ² 4.5 (h 0.686).
- **PSF leakage around clusters** is cleanly null. Splitting by the sign of the PSF's cross projection gives identical offsets
  (Δχ² 0.00). This matches X7's leakage ≤ 0.003.

## Nulls (`nulls.<cell>`)

| cell | F1 randoms × (Z) | extended randoms × ± σ (Z) | cluster − extended randoms × ± σ (p) | N3 χ²_cl / 312 (p_var) |
|---|---|---|---|---|
| canonical h 0.672 | −0.070 (−1.66) | +0.000 ± 0.022 (+0.02) | +0.135 ± 0.087 (0.150) | 316.1 (0.435) |
| canonical h 0.686 | −0.078 (−1.88) | −0.009 ± 0.022 (−0.39) | +0.167 ± 0.090 (0.065) | 308.4 (0.515) |
| alt h 0.672 | −0.064 (−1.66) | +0.000 ± 0.020 (+0.02) | +0.124 ± 0.080 (0.150) | 316.1 (0.435) |
| alt h 0.686 | −0.072 (−1.88) | −0.008 ± 0.020 (−0.39) | +0.153 ± 0.083 (0.065) | 308.4 (0.515) |

- **Extended randoms.** There are 6,499 of them: 20 per cluster for 325 clusters and 13 for one, from 9,598 tries
  (`x11_randoms.out`). They put the field cross level at zero. The −0.07 of F1's 5–6 randoms per cluster is therefore a
  fluctuation of those randoms, and it supplies about a third of X7's offset.
- **Cluster-only offset.** Against the extended randoms it is +0.12 to +0.17, 1.5–1.9σ (p 0.065–0.15). This is reported, not
  graded; the graded estimator stays F1's.
- **N3.** There is no excess cluster-to-cluster variance in the cross channel. X7's jackknife σ_× of 1.3 × shape noise does not
  recur in the per-cluster χ².
- **The 90° rotation of source positions about each cluster flips both channels exactly** (2φ → 2φ + π; max |Δ| 1.9e-13). It is
  an identity, so it was recorded as a code check, not as independent evidence. The informative B-mode nulls are the 200
  rotated-source realisations and N3.

## E-mode systematics (`emode`, `E3`, `E3_clip`, `tangential_Z_per_class`)

- **E1 count deficit** (MID, h 0.672): Q − 1 = −0.140 ± 0.038 in unweighted source counts.
  - Per bin it runs from −0.25 (innermost) to −0.09 (outermost).
  - X7's weighted boost is B − 1 = −0.07 to −0.08 in MID.
  - By class: bright −0.157, faint −0.133; close-neighbour −0.121, far −0.160.
- **E2 magnification.**
  - The catalogue's MAG_AUTO count slope gives α = 0.43, with a bracket of 0.12–0.64.
  - The law's κ in MID is 0.009, scaled by A_MID.
  - The predicted deficit is −0.6 to −2.6 % (central −1.7 %).
  - Sub-verdict: **EXCESS DEFICIT**. About 11 % of sources near the cores are missing beyond magnification, from obscuration or
    blending (f_obs 0.114).
- **E3 tangential splits.**
  - **Size dependence FOUND** (above).
  - **No blending dependence:** the neighbour-distance halves are equal (Δχ² ≤ 0.02). The far-neighbour half gives Z_MID,STAT
    +4.1 / +4.3 / +3.5 / +3.7.
  - **No tomographic, magnitude or PSF dependence.**
  - Cluster z (Δχ² 6.1–8.1, high-z higher) and the MID radial profile (8.3–9.6; 2 cells ≥ 9) fall short of all-4-cell
    candidacy.
- **E4: the deficit's counterpart.** If the deficit is obscuration or magnification with no shape bias, the boost B < 1 should
  not be applied. With B = 1:

  | | canonical h 0.672 | canonical h 0.686 | alt h 0.672 | alt h 0.686 |
  |---|---|---|---|---|
  | A_MID | 1.77 | 1.82 | 1.62 | 1.67 |
  | Z_STAT | 5.80 | 6.05 | 5.12 | 5.38 |
  | Z_CAL | 3.26 | 3.07 | 2.88 | 2.73 |

## Z_MID re-derived (step 3)

The outcome is FLUCTUATION, so the frozen rule reports **Z_STAT**: 5.21 / 5.47 / 4.47 / 4.74 (REAL by X7's rule). The
cross offset's p_× is 0.010–0.015 against pure shape noise. That falls to 0.065–0.15 for the cluster-only offset against
the extended randoms (reported).

Read Z_STAT together with the size result:

| source half | canonical h 0.672 | canonical h 0.686 | alt h 0.672 | alt h 0.686 |
|---|---|---|---|---|
| small sources, Z_STAT | +1.6 | +1.8 | +0.9 | +1.1 |
| large sources, Z_STAT | +5.6 | +6.1 | +5.1 | +5.6 |

Which half measures the true lensing amplitude is not known.

## Against the record (suggested fixes; no other file edited)

1. **X7 "What this does not show" / V1 MARGINAL (MAP §1.A.3).** The premise of X7's CAL rule is not supported: an isotropic
   systematic seen in the cross channel. The offset shows no instrumental or cluster dependence in 19 pre-declared splits, no
   excess variance, and a zero field level at 6,499 random points. About a third of it is F1's random-point fluctuation.
   - Suggest: "cross offset consistent with shape noise (X11); Z_MID 4.5–5.5 statistical".
   - Add in the same sentence: "the core-excess amplitude depends on source size (small-source half A 1.1–1.2, consistent
     with the law; large-source half 1.9–2.1; X11 E3), unexplained". The excess should therefore not be cited as REAL either.
2. **F1 "the member-dilution boost could not be measured (deficit-dominated)".** The deficit is now quantified at 14 ± 4 % of
   unweighted MID counts. Magnification explains only 1–3 % of it. The rest is obscuration or blending, and blending shows no
   tangential signature. So the graded boost convention (B < 1) lowers A_MID by about 8 % (1.64 → 1.77 clipped, canonical h 0.672). The clipped convention is the
   physically consistent one if no shape bias accompanies the deficit (E4).
3. **X7 note "the random-point cross stack (−0.07)".** It is a fluctuation of 5–6 randoms per cluster; the field level is
   0.000 ± 0.022.
4. **Next lane (suggested, not done here; stop rule).** A frozen test of the size dependence:
   - in OUTER and INNER, and around random points;
   - against a resolution variable (size relative to PSF);
   - with per-class photo-z checks;
   - with the KiDS image-simulation m(size), if it can be put on disk. It is not on disk now.
   Until then the core excess is best quoted as "statistically 4.5–5.5σ, with an unexplained source-size dependence".

## Amendments (full text in `FROZEN_CRITERIA.md`)

- **A1 (POST-RESULT, X3 memory only).** `x11_extract_extra.py` failed X3 at 1.124 GB. It now re-executes with
  `MallocMediumZone=0` (X7 A3), and the rerun reproduced every edge exactly (0.710 GB). No shear number existed.
- **A2 (PRE-RESULT, implementation).**
  - (i) A rejected random returns right after its h 0.70 count, and only the needed columns are read; M1, M2 and R1 verify
    that nothing changed. The first full `x11_measure.py` run was stopped after about 2 min of progress lines.
  - (ii) `x11_randoms.py` runs in two parts with the generator state carried over. After (i) the parts took 9 + 9 min, so
    one run would have fit.
  - (iii) E1 of the step-0 extractor compares against X7's scratch cache; S0-1 checks the committed sha256.
  - (iv) The rule for a clean subset of a source variable (GLS of the clean classes) was written down. It was not needed.
- **A3 (POST-RESULT, bug).** In a development run (stub extended randoms, all other inputs final), straddle2 and aniso2 had a
  single class. 14 clusters have no MID source at h 0.672, so their f_main and m2 are NaN, and the median was NaN. The fix
  uses nanmedian and puts those clusters, which carry zero MID weight, in class 0. Nothing else changed.
- **A4 (POST-RESULT, reporting only).** Added after the development run showed the E3 size dependence: E3 under the clipped
  boost, the per-class boost and count ratio, and the per-class Z_STAT for size2 and mag2. None of it is graded.

## Checks

| script | checks | MUTATE |
|---|---|---|
| `x11_step0.py` → `x11_s0_x7_*` | X7's E1–E3, G1–G3, M1–M6, K0–K5: 18/18 PASS | — |
| `x11_s0_check.py` | S0-1–S0-4 PASS | S0-2 FAIL as required (Dx sign) |
| `x11_extract_extra.py` | X1–X3 PASS (0.71 GB) | X1 FAIL as required (no reorder) |
| `x11_measure.py` | M1–M6 PASS (493 s, 0.77 GB); M1/M2 exact (0.0) | M1, M2 FAIL as required (20 clusters, e2 flipped) |
| `x11_randoms.py` (P1 + part 2) | R1, R3 (P1); R2, R3 PASS (541 + 563 s, 0.40 GB) | R1 FAIL as required (e2 flipped) |
| `x11_analysis.py` | S0-K1, K1–K4 PASS (29 s, 0.65 GB) | K1 FAIL as required (tangential as cross) → UNDECIDED |

## What this does not show

- **A fluctuation verdict cannot exclude a systematic that is uniform across every declared split.** A uniform systematic and
  a fluctuation give the same split pattern. Only the declared instrumental and cluster-property causes are removed.
- **The size dependence has no mechanism.** It was not tested in OUTER, at random points, against a resolution variable or
  against image simulations. The KiDS m(size) and n(z) per class are not on disk. It could also be a statistical outlier of
  the E3 family: 19 variables, p 1e-5 to 3e-4 in each cell.
- **The frozen per-class weights are inefficient for sparse classes.** They were not changed.
- **"Pair separation in the source plane" was read as the line-of-sight separation Δz_ls.** The angular separation at fixed R is
  degenerate with cluster z (z2 split), so it was not split separately.
- **E2 is approximate.** The lensing selection is soft, the count slope bracket is wide, and κ is the law's (× A). Even its top
  end, 2.6 %, is far below the 14 % deficit.
- **No new physics.** The model is X2's C\* (spherical AQUAL, β-model gas, Chae+21 field). The A-unit normalisation of the cross
  channel depends on it; the split tests (ratios within a cell) hardly do.

## Files and runs (`OMP_NUM_THREADS=1 nice -n 15`)

| file | what |
|---|---|
| `x11_step0.py` | runs X7's committed scripts read-only (sha-checked, output paths substituted) → `x11_s0_x7_*.out/json` |
| `x11_s0_check.py` → `.out`, `_results.json`, `_MUTATE.*` | step-0 equality with X7's committed products |
| `x11_extract_extra.py` → `.out`, `_results.json`, `_MUTATE.*` | MAG_AUTO, size, PSF size, neighbour distance; frozen class edges (scratch `x11_edges.json`) |
| `x11_common.py` | shared estimator (X7's verbatim plus per-class sums and rotations) |
| `x11_measure.py` → `.out`, `_results.json`, `_MUTATE.*` | split measurement (scratch `x11_measure_classes.npz`) |
| `x11_randoms.py` → `_P1.out`, `.out`, `_results_P1.json`, `_results.json`, `_MUTATE.*` | extended random points (scratch `x11_randoms.npz`) |
| `x11_analysis.py` → `.out`, `_results.json`, `_MUTATE.*` | splits, tests, nulls, E-mode, verdict |

Run order:
1. `x11_step0.py extract <cache> <x7 scratch cache>`, then `regress <cache>`, `measure <cache> <scratch>`,
   `analysis <scratch>`.
2. `x11_s0_check.py <cache> <scratch>`.
3. `x11_extract_extra.py <cache>`.
4. `x11_measure.py <cache> <scratch>`.
5. `x11_randoms.py <cache> <scratch> --part1`, then `--part2`.
6. `x11_analysis.py <scratch> <cache>`.

Read-only inputs:
- the KiDS FITS (outside the repo)
- the eRASS1 FITS
- X7's scripts, npz and JSON
- X2's source, npz and JSON
- F1's source and JSON
- F2's `f2_aqual.py`
- the Chae+21 CSV

Nothing was downloaded.
