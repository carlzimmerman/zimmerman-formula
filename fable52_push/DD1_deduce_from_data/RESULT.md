# DD1 RESULT: deduce the rule from the data (2026-11-10)

Criteria 2a3f76f295 (committed alone, before any script or number). Table 441824e854 (frozen before any fit). TEST lane,
quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled. No amendment. Origin ids: see
the last section.

## Label

**NO RULE AMONG THE CANDIDATES / NO RULE AMONG THE CANDIDATES** (canonical / alt).

Every known answer passes. Every MUTATE arm bites (M3 only barely). `DD1.lean` compiles (6 theorems, standard axioms);
its false twin fails with 5 errors, one per false statement.

The question was: does the non-baryonic mass follow one rule across every class of system on disk? It does not. Not
one candidate holds even the two half-splits in any of 51 seeds. Every candidate that covers all 16 classes fails at
least 11 of them. Six classes fail every candidate.

The statistic is SHP1's: X = g_obs / g_bar - 1, the enclosed non-baryonic mass over the enclosed baryons. It is scored
as Y = log10(1 + X), so an offset is dex in g_obs at fixed g_bar. Scatter is the class-balanced robust scatter of the
held-out residuals, as the mean of the two splits. The reference is 0.284 dex: that is what you get by predicting each
class with its own training median. "Beyond errors" means a class misses by more than 3 se in some test. The other
failures miss only the 0.10 dex line, within their errors.

| candidate | held-out scatter (dex) | classes failing (of 16) | of which beyond errors | worst class: test, offset (dex), in se |
|---|---|---|---|---|
| (a) g_bar (the same as x = sqrt(a0/g_bar)) | 0.329 | 13 | 8 | NGC 1052 UDGs: A->B, -1.02, -2.9 |
| (b) g_obs | 0.564 | 15 | 12 | tidal dwarfs: B->A, -1.49, -7.7 |
| (c) local depth g_obs r / c^2 | 0.443 | 14 | 9 | NGC 1052 UDGs: A->B, -2.00, -5.7 |
| (c') system depth | 0.480 | 13 | 8 | NGC 1052 UDGs: A->B, -2.00, -5.7 |
| (d) system baryonic surface density [9 classes only] | 0.271 | 6 of 9 | 3 | NGC 1052 UDGs: A->B, -0.83, -2.4 |
| (e) enclosed baryon mass | 0.405 | 12 | 10 | MW ultra-faints: B->A, -4.9 (extrapolated), -26 |
| (f) radius | 0.315 | 13 | 6 | Coma UDGs: A->B, +1.21, +7.1 |
| (g) redshift (control) | 0.386 | 16 | 12 | MW ultra-faints: LOCO, +0.94, +8.9 |
| P1 (g_bar, r) | 0.314 | 12 | 10 | MW ultra-faints: B->A, +0.97, +5.0 |
| P2 (g_bar, z) | 0.259 | 13 | 11 | NGC 1052 UDGs: LOCO, -1.01, -4.1 |
| **P3 (g_bar, system depth)** | **0.219** | 12 | 7 | KiDS: B->A, +0.80, +5.2 |
| L0 the law at the footing's a0 | 0.336 / 0.334 | 14 / 14 | 9 | NGC 1052 UDGs: A->B, -0.94 / -0.98, -2.7 |
| L1 the law's curve, one free a0 | 0.334 | 11 | 8 | NGC 1052 UDGs: A->B, -1.06, -3.0 |
| L2 the law's curve, a0 per class (diagnostic) | 0.181 | 7 | 2 | NGC 1052 UDGs: A->B, -0.22, -0.6 |
| CONS0 X at the last point = C | 0.721 | 16 | 13 | KiDS: LOCO, +2.08, +18 |
| CONS1 X at the last point = C dsys^p | 0.786 | 15 | 12 | KiDS: B->A, +2.25, +14 |

Rows without a footing pair are identical on both footings. A free function of x or of g_obs/a0 does not depend on a0
(Lean `law_scale`). Only L0 moves with the footing.

**Six classes fail every one of the 13 candidates that cover all classes.** For each, the "kindest" number is the
offset under the candidate that treats it best. The "law" range is its offset under L0 across the three tests.

| class | kindest candidate, its worst offset | under the law (L0, canonical) | candidates failed beyond errors |
|---|---|---|---|
| tidal dwarfs (6) | radius, -0.29 | -0.61 to -0.87 | 12 of 13 |
| NGC 1052 UDGs (DF2, DF4) | radius, -0.35 | -0.74 to -0.94 | 9 |
| MW ultra-faints (31) | radius, -0.15 | +0.51 to +0.60 | 10 |
| Coma UDGs (11) | P3, +0.21 | +0.31 to +0.37 | 8 |
| faint gas-rich rotators (20) | CONS0, -0.10 | -0.24 to -0.27 | 8 |
| M31 dwarfs (33) | L1, -0.12 | +0.01 to +0.19 | 5 |

**The class that breaks every candidate the hardest is the tidal dwarfs.** The least they miss by is 0.29 dex, and under
the law they miss by 0.6 to 0.9 dex, beyond their errors under 12 of the 13 candidates. The breakers go both ways. Some
low-mass systems carry far less non-baryonic mass than any rule built on the rest gives them: the tidal dwarfs, DF2 and
DF4, and the faint gas-rich rotators. Others carry far more: the MW ultra-faints and the Coma UDGs.

## The numbers that carry it

**Under the law, class by class** (L0, offsets A->B / B->A / LOCO, canonical; alt within 0.04 except where given):
- SPARC +0.00 / +0.02 / +0.00. It passes. That is SHP1.
- KiDS +0.13 / +0.14 / +0.14. It is within errors (se 0.15), but over the 0.10 line. On alt it is +0.09 / +0.10 / +0.10
  and passes.
- ATLAS3D +0.07 / +0.08 / +0.07, at 4-7 se. That is at Chabrier. At Salpeter it is -0.10 to -0.12.
- RC100 +0.07 / +0.11 / +0.09.
- Massive spirals +0.16 / +0.02 / +0.07.
- Groups +0.16 / +0.17 / +0.16, at 4-7 se.
- X-COP +0.57 / +0.48 / +0.50 and CLASH +0.55 / +0.55 / +0.55, at 15-24 se.
- MW ultra-faints +0.51 / +0.60 / +0.59. Coma UDGs +0.37 / +0.31 / +0.32.
- MW bright dwarfs, M31 dwarfs and LG field dwarfs sit at -0.09 to +0.20, within errors.
- Faint rotators -0.27 / -0.24 / -0.24. Tidal dwarfs -0.61 / -0.87 / -0.69. NGC 1052 UDGs -0.94 / -0.74 / -0.84.

**The law's curve with a0 per class** (L2, all systems of each class, 68 % bootstrap over systems), in units of the
canonical a0:
- Near zero: tidal dwarfs below 0.01, NGC 1052 UDGs at the floor.
- Below 1: faint rotators 0.24 (0.13-0.28), LG field dwarfs 0.65 (0.51-0.98).
- About 1: SPARC 1.05 (0.99-1.11).
- 1.3 to 1.5: massive spirals 1.34, MW bright dwarfs 1.38 (0.73-4.9), M31 dwarfs 1.54 (1.2-2.4).
- About 2: KiDS 1.89 (1.81-1.99), ATLAS3D 2.10, groups 2.12, RC100 2.16.
- Coma UDGs 4.6 (2.9-7.0).
- 14 to 20: X-COP 14.4 (13.3-17.5), MW ultra-faints 16.0 (11-20), CLASH 20.4 (18.9-21.8).

So within a class the law's curve holds the shape well: L2's held-out scatter is 0.18 dex, the lowest of any row. But
its scale runs over more than three decades. One shared a0 (L1) settles at 1.6-1.8 times canonical. That fails SPARC
(-0.06 to -0.12) and still fails the clusters, the ultra-faints and the low rows.

**The best two-variable rule, P3 (the baryons' field and the depth of the whole system)**, is the only full-cover rule
that beats class labels by a clear margin (0.219 against 0.284). In the splits it brings these together within 0.045 dex:
SPARC, ATLAS3D, RC100, groups, X-COP and CLASH. Even with the class left out, X-COP reads -0.05 and CLASH +0.06, and both
pass. Groups read +0.07, beyond errors. So, at a fixed baryonic field, the hot systems' excess tracks how deep the whole
well is. P3 is not clean there either: with the class left out it also misses SPARC (-0.08) and ATLAS3D (+0.03), both
beyond errors.

P3 fails these:
- tidal dwarfs, -0.47 to -0.56;
- faint rotators, -0.15;
- MW ultra-faints, +0.26 to +0.39;
- LG field dwarfs, +0.18 to +0.24;
- NGC 1052 UDGs, -0.26 to -0.37;
- KiDS, +0.6 to +0.8. Part of this is how the frozen grid treats four stacks: each stack has its own system depth, and
  the 0.4-dex cells rarely hold two of them.

**Other numbers:**
- (a) with the class left out: groups +0.29, X-COP +0.41, CLASH +0.48 and KiDS -0.42. KiDS reads low here because, at
  KiDS's g_bar, the free function is set by the Local Group dwarfs. Those sit higher than the lensing stacks at the same
  field.
- CONS0's fitted C is 1.7-1.9. The last measured points sit at very different places from class to class: X_last is
  0.07 for DF2 / DF4, about 5 for X-COP, about 9 for groups and about 330 for KiDS. No constant and no depth power law
  fits them.

## Step 4: what the nearly-surviving rules would require (no theory claim)

- **(a) / L0, the amount set by the baryons' field alone.** Any theory would need the same non-baryonic mass at the
  same g_bar in every kind of system.
  - The data allow this for SPARC, and within errors for KiDS (alt) and three dwarf classes.
  - They forbid it for clusters (+0.5 dex), groups (+0.16), ATLAS3D and RC100 (+0.07 to +0.11), the ultra-faints and the
    Coma UDGs (+0.3 to +0.6). They also forbid it for the tidal dwarfs, DF2 / DF4 and the faint rotators, which sit
    -0.24 to -0.94 low.
  - This is form B's galaxy rule. The record's known cluster shortfall (QX2, RB1) and RB2's hosted dwarfs are the same
    numbers seen from here.
  - The measurement that separates it from P3: X at matched g_bar in systems of very different depth, such as the X-ray
    halos of isolated massive ellipticals against spirals at the same g_bar and radius. P3 says the deeper one carries
    more. (a) says the two are equal.
- **P3, the amount set by the field and by the depth of the whole well.** Any theory would need a second input beyond
  the local field: something that knows the potential depth of the whole system.
  - In form, this matches the record's static-clock term n_d = -mu_K^2 Phi / K (EQUATIONS.md section 5), whose density
    grows with depth. But the record closed every amplitude tried for that term: MK1 NO VALUE, CLS1 NO STATE at
    mu_K >= 198 per Mpc. MK2's exponential term goes the other way for clusters.
  - P3 cannot hold the shallow systems, which scatter both high and low at the same field and depth.
  - The measurement that separates P3 from L2: velocity dispersions with resolved baryons for the ultra-faints and for
    UDGs in fields of different depth. L2 needs a per-class scale. P3 needs depth to set it.
- **L2, the law's shape with a scale per class.** Any theory would need the law's curve, with a0 set by something each
  class carries, ranging from below 0.01 to 20 times canonical. That is not compatible with one a0 = (1/2) c
  sqrt(G rho_DE), the record's relation, unless the classes far from 1 are explained by their systematics.
  - The measurement that tests that escape: the tidal dwarfs' inclinations, and the ultra-faints' dispersions cleaned of
    binaries. Those are the two ends.
- **"The total is fixed and baryons are missing"** (CONS0, CONS1) is not testable with these apertures. Each class's
  outermost measured point sits somewhere different: the half-light radius for dwarfs, about 260 r_M for KiDS. As
  stated, the reading fails 15-16 classes.

## The data table and its systematics, per class

| class | points / systems | g_bar contains | median lg g_bar | median Y | median X_last | main systematic |
|---|---|---|---|---|---|---|
| SPARC | 2700 / 149 | stars (Upsilon 0.5 / 0.7), HI x 1.33 | -10.84 | 0.49 | 3.3 | Upsilon (SHP1: 0.3 / 0.8 move bins by 0.15 dex) |
| faint rotators (McQuinn+22) | 20 / 20 | stars + HI, total as enclosed | -11.26 | 0.39 | 1.5 | asymmetric drift, rising curves |
| tidal dwarfs (Lelli+15) | 6 / 6 | HI + H2 + stars, total | -11.45 | 0.07 | 0.17 | inclination (V ~ 1/sin i), equilibrium |
| massive spirals (Di Teodoro+23) | 12 / 12 | W1 stars + 1.36 HI, totals | -11.16 | 0.66 | 3.6 | curves read off figures |
| ATLAS3D | 187 / 187 | stars, Salpeter SPS x 0.61 | -9.55 | 0.17 | 0.47 | IMF (Salpeter flips L0's sign) |
| RC100 | 100 / 100 | paper's Mbar (stars + cold gas) | -9.79 | 0.26 | 0.81 | no errors on disk (0.087 / 0.20 dex stated) |
| KiDS (B21, 4 bins) | 60 / 4 | stars + cold gas, no hot gas | -13.13 | 1.75 | 329 | stellar masses (0.2 dex), calibration, host leakage |
| groups (Lovisari+15) | 20 / 20 | hot gas + KVM18 stars | -11.66 | 1.00 | 9.1 | hydrostatic bias, stars by scaling relation |
| X-COP (7 with stars) | 129 / 7 | hot gas + measured stars | -10.68 | 0.92 | 4.9 | hydrostatic bias, M_FORW form |
| CLASH (Tian+20) | 84 / 20 | hot gas + BCG | -10.45 | 0.94 | 7.6 | satellites' stars missing; lensing model |
| MW bright dwarfs | 11 / 11 | stars (M/L_V 2) | -12.20 | 1.39 | 23 | equilibrium, tides |
| MW ultra-faints | 31 / 31 | stars | -13.12 | 2.08 | 118 | binaries (RB2 factor), tides, membership |
| M31 dwarfs | 33 / 33 | stars | -12.50 | 1.36 | 22 | the same |
| LG field dwarfs | 13 / 13 | stars only (their HI not counted) | -11.95 | 0.98 | 8.5 | gas omitted |
| Coma UDGs (Freundlich+22) | 11 / 11 | stars | -12.15 | 1.39 | 23 | membership, anisotropy |
| NGC 1052 UDGs | 2 / 2 | stars | -11.67 | 0.01 | 0.07 | distance, tides |

**Left out, with the reason:**
- SLACS: projected aperture masses only; a 3D g needs a profile.
- LITTLE THINGS: no errors; in LaTeX only.
- KMOS3D, KROSS and MSA3D: no radius, or no gas.
- Globular clusters: their masses are N-body fits to the dynamics, so there is no independent baryonic mass.
- The Milky Way curve: no baryon model on disk.
- Collins+2013: duplicates LVD's M31 rows.
- Humphrey+2006: NFW fits.
- Catalogues whose masses come from scaling relations or NFW fits: Lovisari+2020, eRASS1, eFEDS, PSZ2, Mahdavi+2013
  lensing.
- X-COP's 5 clusters without a stellar file.

Two notes on the inputs:
- Five faint rotators and one massive spiral are SPARC galaxies. They were kept in SPARC only.
- The KiDS lens redshift is the median of the record's lens catalogue (KO1's) per B21 mass bin: 0.23, 0.30, 0.33 and 0.37.
  It is not B21's own figure.

## What it does not settle

- **Mass-to-light.**
  - SPARC passes the law only near Upsilon 0.5 / 0.7 (SHP1).
  - ATLAS3D's sign under the law depends on the IMF. At Chabrier it is +0.07 above, at Salpeter -0.10 to -0.12 below.
  - The dwarfs' M/L_V of 2 sets their g_bar directly.
  - Neither bracket changes the label: the ATLAS3D Salpeter run is also NO RULE.
- **Hot gas.** With B21's hot gas, the lane has one stack and no mass bins.
  - The label is unchanged.
  - KiDS under the law reads +0.08 in the one direction where it is held out.
- **Hydrostatic bias.** X-COP and the groups use hydrostatic masses. A 10-20 % bias moves them by 0.05-0.1 dex. That
  cannot close +0.5 dex for clusters under the law. It could close the groups' +0.16.
- **The lensing calibration that SHP1 and KO1 flag.** KiDS carries a stated 0.2 dex stellar-mass systematic, so its se
  is about 0.15. KiDS fails the law only on the 0.10 line, within errors, and passes on alt.
- **Total as enclosed.** The faint rotators, the tidal dwarfs and the massive spirals use total baryons at the last
  radius. If gas lies beyond that radius, their g_bar is too high and they read low. That is the right sign for the
  faint rotators' -0.24. The tidal dwarfs' main lever is inclination.
- **Dwarf dynamics.** Equilibrium, tides and binaries are not modelled. RB2's binary factor (median 0.855) is applied to
  every dwarf not in its list, as RB2 did.
- **Small classes against a fixed line.** With n = 1 per half (NGC 1052 UDGs) or se above 0.1 dex (the MW bright
  dwarfs), the 0.10 dex line fails a class unless its offset is small by luck. The "beyond errors" column separates
  those cases. The label does not rest on them: even counting only failures beyond errors, every candidate fails at
  least 6 classes.

## What this lane finds in SHP1, EQUATIONS.md and CLOSURE.md

- **SHP1.** Nothing wrong. Its SPARC bins reproduce to 7e-16, and its KiDS means and chi^2 to 1e-6. But its "rotation
  curves follow it in every bin" is SPARC's scope. The other rotation-supported samples on disk do not all follow the
  law at the footing's a0:
  - faint gas-rich rotators -0.24 to -0.27 dex;
  - tidal dwarfs -0.6 to -0.9;
  - RC100 at z 0.6-2.5, +0.07 to +0.11;
  - massive spirals +0.02 to +0.16.
- **EQUATIONS.md section 6.** "The cold component's pull never exceeds a0" is a property of the law. The measured
  g_obs - g_bar reaches 6.1 a0 in X-COP and 6.2 a0 in CLASH. Section 7's [M] line is SPARC-only in the same way as SHP1.
- **CLOSURE.md.** Nothing found wrong. DD1 does not grade form B.

## Checks

| check | result |
|---|---|
| KA1 SHP1 | 175 files / 149 galaxies / 2700 points. R1 bins to 6.0e-16 / 6.7e-16. KiDS Nobins mean - 1: +0.4025 / +0.2801; hot gas -0.0921 / -0.1730. chi^2 194.14 / 132.95 and 346.00 / 395.41. All equal to `shp1.json`: PASS |
| KA2 (i) law truth | (a) PASSES (worst +0.004) and L0 PASSES on both footings. (g) fails 16 classes and the scatter line: PASS |
| KA2 (ii) constant X = 5 | CONS0 PASSES with C = 5.0000 / 5.0000; (a) PASSES: PASS |
| KA2 (iii) depth truth X = (c / 150 km/s) dep^(1/2) | (c) PASSES (worst +0.012). (a) fails 7 classes and (g) fails: PASS |
| KA3 loaders | CLASH 84 / 20, RC100 100, groups 20, X-COP 7, TDG 6, Coma 11. Coma's own columns agree to 0.016 dex: PASS |
| KA4 identities | X g_obs = a0 and g_bar (g + a0) = g^2 hold to 6.7e-16: PASS |
| M1 class labels shuffled | (a)'s worst offset 1.022 -> 0.410: bites |
| M2 CLASH g_bar x 2 | CLASH under (a) +0.453 -> +0.281: bites |
| M3 errors halved | failing triples 484 -> 487: bites, barely. Most failures are beyond the 0.10 dex line, not limited by errors |
| M4 a0 x 2 in L0 | SPARC -0.003 (pass) -> -0.118 (fail): bites |
| Lean `DD1.lean` | exit 0. 6 theorems: `X_is_mass_ratio`, `law_curve`, `law_in_gobs`, `law_scale`, `law_mono_a`, `law_one_a0`. Axioms propext, Classical.choice and Quot.sound only |
| Lean `DD1_MUTATE.lean` | exit 1. 5 errors, one in each false statement |
| 50 other seeds | no candidate holds both splits in any seed |

**Against the pre-freeze hand estimates.**
- Held: the label, clusters and ultra-faints breaking (a), DF2 / DF4 low, and the redshift control failing.
- Not foreseen:
  - The tidal dwarfs and faint rotators are among the hardest breakers.
  - P3 organizes the hot systems with the galaxies even with the class left out.
  - KiDS fails (a) in a split, not only when left out, because the dwarfs set the function at its field.

## What it means, in plain words

- No single measured variable, and no pair tried, tells you how much non-baryonic mass a system holds across all the
  kinds of systems on disk.
- The baryons' field (the law's variable) works for disc galaxies at z ~ 0. It fails, beyond errors, for clusters,
  groups, early types, distant discs, the ultra-faints and the UDGs.
- Adding the depth of the whole system brings the hot systems in line with the galaxies. It still fails the smallest
  systems.
- The smallest systems split both ways at the same field and depth. Tidal dwarfs, DF2 / DF4 and faint gas-rich rotators
  hold little or none; the ultra-faints and the Coma UDGs hold a lot. Whatever sets the amount there is not in this
  table's variables, or it sits in their systematics (inclination, binaries, tides, total-as-enclosed).

## Files

- `FROZEN_CRITERIA.md`
- `dd1_table.py`, with `dd1_table.csv` (the frozen table), `dd1_table.out` and `dd1_table_counts.json`. After the
  table commit, the house end line was added to `dd1_table.py` as a comment. Re-running it rebuilds the same table byte
  for byte.
- `dd1.py`, with `dd1.json` / `dd1.out` and `dd1_MUTATE.json` / `dd1_MUTATE.out`
- `DD1.lean`, `DD1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`

## Commit ids

| | shared checkout | origin |
|---|---|---|
| criteria | 2a3f76f295 | 850c91839f |
| table | 441824e854 | f86496a251 |
| result | c8df8e2859 | 91c159b746 |

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
