# EUC9 (GRISM SPECTRA SOURCE REDSHIFTS): RESULT

2026-11-12. Criteria bea4eacfa8 (alone, before any script and before any lens or grade-X spectrum was fetched).
Pre-data amendment A0 82cf65da28. Post hoc amendment A1 25d7f82cc2 and its addendum 8bc1675a42 (each alone, before
the amended search ran on anything but the truth lens and field spectra).

## Verdict: NOT EVALUABLE / NOT EVALUABLE (canonical / alt). EUC1-F and EUC5-F are not graded.

**As frozen**, the search fails all three of its gates on every rung: the truth lens is not found, 40 grade-X
non-lenses pass against a limit of 6.0, and sign-flipped noise pairs come at half the rate of real ones.

**Under the post hoc amendment A1** the search finds the truth lens at z_s = 1.3659 (DESI: 1.3657) and passes its
signal-free null, but 6 grade-X systems pass against a limit of 2.3, so it is NOT EVALUABLE too. No reading is made.

All instrument checks pass in both runs; all four mutation twins exit 1. κ = ½ FITTED. No outcome favours the
framework. Nothing here bears on the law.

## 1. What was done

The co-added spectrum and every individual dither spectrum of the lens object of 3,184 systems (2,260 of sample S, of
which 1,164 in P; 923 grade X; the truth lens), read by byte range from Euclid's DR1 tile files at IRSA: 3,184 of
3,184, 103 MB, 20 re-reads identical, 31 field objects identical to IRSA's per-object service. 36.6 % of S and 35.8 %
of X are evaluable (the rest have no usable grism spectrum).

The handle is confirmed in the file headers: each dither carries its grism position, RGS000 or RGS180, and the two
disperse in opposite directions. An emitter off the extraction centre is therefore seen at λ + s in one and λ − s in
the other.

## 2. The frozen search (Euclid's own co-added spectra)

| Rung | S | X (limit) | sign-flipped S (limit) | truth lens | |
|---|---|---|---|---|---|
| TA | 73 of 2,260 (3.2 %) | 40 of 923 (6.0) | 37 (14.6) | not found | all three FAIL |
| TB | 29 | 15 (2.4) | 10 (5.8) | not found | all three FAIL |
| TA-D (A0: dither test required) | 15 | 3 (1.2) | 5 (3.0) | not found | all three FAIL |
| TB-D | 7 | 2 (1.0) | 1 (1.4) | not found | H2, H4 FAIL |

Checks: K1, K2, K5 pass; injected pairs recovered 96 %; single lines read as pairs 0.3 %; injected mirrored pairs pass
the dither test 95 %, true doublets 2 %. Twins: newton exit 1; single exit 1 (X 40 → 77).

**Why it fails.** Euclid's co-addition drops dithers where they disagree. A mirrored line is a place where the two
grism positions disagree. At the truth lens's blue peak the co-add keeps 2 of 4 dithers; the red peak's central pixel
is flagged "do not use". The co-add is the one product from which the signature has been removed, and what is left in
it is symmetric noise structure.

## 3. The truth lens in its dither spectra

EUCL-DR1-L015763, re-co-added without rejection: two peaks at 15,464 and 15,598 Å, 40.6 σ and 34.8 σ. Midpoint
15,531.4 Å = Hα at **z_s = 1.3659**. Half-split 67.0 Å = **1.50″ against θ_E = 1.51″**. The blue peak is the stronger
in RGS000 and the red in RGS180 (dither statistic D = −6.4): an arc and a fainter counter-image, mirrored.

It also explains Euclid's catalogue (EUC3): the pair's separation is close to the [O III] 4960–5008 spacing, so the
pipeline's first solution reads it as [O III] at z = 2.114. This lane's own line-identity step made the same mistake
until the partner line was fitted jointly with the pair (addendum).

## 4. Post hoc amendment A1 (re-co-added dithers, dither test required)

Designed on the truth lens alone; every other spectrum was unopened when it was committed.

| Rung | P | S | X (limit) | sign-flipped S (limit) | sign-flipped X | truth | |
|---|---|---|---|---|---|---|---|
| A1-TA | 17 | 28 of 2,260 (1.24 % [0.82, 1.79]) | **6 of 923 (2.3): FAIL** | 4 (5.6): pass | 5 | recovered | NOT EVALUABLE |
| A1-TB | 12 | 18 (0.80 %) | **3 (1.5): FAIL** | 1 (3.6): pass | 3 | recovered | NOT EVALUABLE |

Checks: K1, K2, K5 pass; injected mirrored pairs returned 78.7 %, passing the dither test 77.0 %; single lines 0 %;
true doublets 2.0 %. Twins: newton exit 1; single exit 1 (X 6 → 79). The truth lens's recovery is not evidence here.

**What the numbers say, and do not say.**
- Lenses show twice the rate of non-lenses (1.24 % against 0.65 %; difference +0.59 % [−0.10, +1.28]) and seven times
  their own sign-flipped rate (28 against 4). In EUC3 the ratio was 1.2; in the frozen search above, 0.75.
- The grade-X hits are matched by grade-X sign-flipped hits (6 against 5). Grade-X spectra make spurious pairs of
  either sign three times as often as lens spectra do (0.54 % against 0.18 %). So the grade-X null may overstate the
  false rate among lenses. That is a reading of two nulls that disagree, made after the fact; it does not pass the gate.
- 15 of the 28 lens pairs sit at the smallest split the rule allows (0.67″), in lenses with θ_E of 0.55–0.98″. Either
  small arcs pressing on the floor, or an emitter a few tenths of an arcsecond off the extraction centre: a deflector
  above its photo-z with lopsided emission would do it. Two of the six grade-X hits are of that kind, at 23 σ and 12 σ.
- Split against Einstein radius correlates at +0.75 in lenses and +0.81 in grade X, whose radii were assigned at
  random. The allowed range scales with θ_E. That correlation is produced by the search window and is not evidence.

**The void reading (seen, not used).** P, 17 lenses: median b +0.264 [+0.151, +0.342] canonical, +0.252
[+0.134, +0.328] alt; the same lenses source-free −0.183 / −0.210. S, 28: +0.258 / +0.243. By class of S: below 1.0″,
N = 20, +0.191 [+0.099, +0.335]; the other two classes have 4 lenses each. Had the gates applied, EUC1-F would have
read NO VERDICT on both footings. With the single-line lenses read as [O III] instead of Hα the P median falls to
+0.136 / +0.119: the answer would turn on line identity, and 22 of the 28 have one line.

## 5. What this means

1. **Euclid's lens gate still cannot be graded.** Three routes to source redshifts have now been tried (DESI fibres,
   Euclid's grism catalogue, Euclid's grism spectra) and none certifies a sample. EUC1-F stays open; EUC1 stays
   NO VERDICT / NO VERDICT; EUC5-F stays sealed and ungraded.
2. **The signature is real and the instrument shows it.** On the one known pair the dither spectra give the DESI
   redshift to 0.0002, with a split equal to the Einstein radius to 0.01″. Euclid's co-added spectra and catalogue
   cannot, by construction.
3. **For the first time lenses separate from non-lenses, by a factor of two.** The gate asks for five. The remaining
   contaminant is an emitter slightly off-centre, which a 1D spectrum cannot tell from a small arc.
4. **What would close it.** Predict each lens's split before looking: the arc's position from the image and the
   dispersion direction on the sky fix the sign and size of the split per dither. A non-lens has no arc to predict
   from, so a null built that way is clean. It needs the pointing roll angles and the arc positions; not run here.
   The 28 candidate redshifts in `euc9_a1_sources.csv` are a target list, not a sample.

## 6. Disclosures

- The fetch route changed before any lens spectrum was opened (A0): the per-object service takes about 30 s per
  object. The 15 spectra it returned first were never opened. Reading the tile files is what revealed the dithers.
- A1 and its addendum are two repairs made on the single truth lens. A dry run of the frozen search on the first 52
  spectra, and code-only dry runs on later partial subsets, preceded the complete runs; counts from them were seen.
- The mask rule and the two-direction geometry, marked PROVISIONAL in the criteria, are confirmed by the file headers.
- Objects observed at several roll angles (most lens objects have more than four dithers) have their split smeared.
- `euc9_core.py` changed after the criteria only by additions with frozen defaults (dither test, re-co-addition,
  joint partner fit); the frozen search path is as tested on field spectra before freezing.

## 7. Files

`euc9_common.py`, `euc9_core.py`, `euc9_fetch.py`, `euc9.py`; frozen run `euc9.out`, `euc9_results.json`,
`euc9_sources.csv`, `euc9_MUTATE_*`; A1 run `euc9_a1.out`, `euc9_a1_results.json`, `euc9_a1_sources.csv` (every pair
passing the rule on the re-co-addition, with its dither statistic; grade X rows marked), `euc9_a1_MUTATE_*`,
`figs_a1/` (95 pairs: black co-add, blue RGS000, red RGS180; the truth lens is the first panel).

Commits (local): criteria bea4eacfa8; A0 82cf65da28; scripts 410cbe74da; A1 25d7f82cc2; addendum 8bc1675a42; origin
ids are in the commit that follows this file. Spectra are outside git
(`_external_data/euclid_dr1_eclipse/nisp_spectra_dith/`).

    python3 -I euc9_fetch.py --data-dir <dir>
    python3 -I euc9.py --data-dir <dir>            (frozen)
    python3 -I euc9.py --data-dir <dir> --a1       (post hoc)
