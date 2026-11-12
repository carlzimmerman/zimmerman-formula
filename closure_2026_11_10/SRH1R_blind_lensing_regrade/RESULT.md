# SRH1R RESULT: blind re-grade of SRH1's lensing gate inside the forest window

## Label

- **canonical (a0 9.3603e-11): NO VERDICT** [does not separate]
- **alt (a0 1.1312e-10): NO VERDICT** [does not separate]

The label is NO VERDICT because two of the three frozen MUTATE twins do not bite (MU1 and MU3). It is not a pass.
**What the numbers under it say:** my gate passes at all four window f on both footings, with a wide margin, and it
passes equally at f = 0.05 and with the cold reference everywhere. This lensing test cannot tell one f from another.

TEST lane, quarantined. The family is post hoc to FRZ1 and FZS1. Nothing here turns SRH1's frozen label (WINDOW EMPTY)
into a pass, nothing here is a pass of form B, and nothing here is in PAPER72.

**Blindness was not perfect.** Before freezing I knew SRH1's label, that its lensing gate fails in the window by a narrow
margin, and (from the one-line memory index) "KiDS lensing f >= 1.0". I had read SRH1's criteria only. Section 1 of my
criteria lists everything else seen. Criteria: local 641865e0b3, origin 8fd213d5ac, pushed alone before any script.

## The numbers that set it

Graded set: host-free at the 1.6 R_h veto, KO1R's tie rule: 16,846 lenses (late 2,613, early 14,233). Thirteen g_bar
bins, one fitted mass factor k, 12 degrees of freedom. Line: p >= 0.0167 (T <= 24.63).

| f | canonical: T all / late / early (k all) | alt: T all / late / early (k all) | gate |
|---|---|---|---|
| 0.40 | 7.74 / 5.37 / 8.03 (1.379) | 7.74 / 5.37 / 8.03 (1.378) | PASS / PASS |
| 0.50 | 7.75 / 5.37 / 8.04 (1.378) | 7.75 / 5.37 / 8.05 (1.377) | PASS / PASS |
| 0.60 | 7.67 / 5.37 / 7.97 (1.380) | 7.69 / 5.37 / 7.99 (1.379) | PASS / PASS |
| 0.70 | 7.39 / 5.38 / 7.73 (1.388) | 7.42 / 5.38 / 7.76 (1.386) | PASS / PASS |
| comparator f = 0 (reference everywhere) | 7.73 / 5.37 / 8.02 (1.379) | 7.73 / 5.37 / 8.02 (1.379) | PASS / PASS |
| comparator f = inf (R_set = r_ta) | 9.45 / 6.29 / 11.19 (1.672) | 8.47 / 5.74 / 10.08 (1.455) | PASS / PASS |
| comparator: the law's halo to x_t (ONE1's layout) | 9.49 / 6.29 / 11.22 (1.678) | 8.48 / 5.73 / 10.10 (1.452) | PASS / PASS |

- The smallest p in the window is 0.78 (early, f 0.50). The Hotelling form of p agrees (0.79 to 0.94).
- Across the window T (all) moves by 0.36. Between f = 0.50 and f = 0 it moves by 0.02.
- Why: the layout keeps the reference's enclosed cold mass at R_set, and R_set is 50 to 110 kpc for these lenses. The
  graded cells start near 65 kpc and reach 3 Mpc. Outside R_set every f is the same NFW reference, so the signal is the
  same. The footings also agree to the second decimal for the same reason: a0 enters only inside R_set.

**Known answers.** KA1, KA3, KA4, KA5, KA6, KA7, KA8 pass as frozen. KA6 reproduces the host-free counts exactly (40,667
/ 25,708 / 17,335; 40,149) and KO1R's A_hf (1.0822 +- 0.1583 / 0.9847 +- 0.1440). KA2 passes only as amended:
`AMENDMENT_A1.md` (my frozen expectation left out an analytic (2 / pi) / u term; committed alone before any data).

**MUTATE twins** (`srh1r_grade_MUTATE.json`), same on both footings:
- MU1, share x 0.1: **does not bite.** k runs to its bound (8.000) on "all" and "early", so the gate is NOT EVALUABLE,
  not FAIL. Even on the bound T is 21.99 / 22.30, inside the line. A tenth of the share on eight times the mass is nearly
  the same halo: with k free, this statistic tests shape only, not the amount of cold mass per unit catalogued mass.
- MU2, reference outside R_set removed: **bites.** T (all) 73.81 / 73.90, +66 over f = 0.5; gate FAIL.
- MU3, f = 0.05: **does not bite.** T (all) moves by -0.02; gate PASS.

So the test has power on the outer layout (MU2) and none on f (MU3) or on the share at free k (MU1).

**Fragile qualifier: not set.** At every window f the gate also passes with the plain tie rule (17,335 lenses, T all
6.4 to 6.7), with the 1.3 R_h veto (25,191 lenses, T all 10.5 to 10.9), and with the permuted-position sum subtracted
(T all 10.5 to 11.0).

## Reported, not graded

- Per bin at f 0.50 (canonical, all; 4 G DeltaSigma in 1e-12 m/s^2; data +- error | model): bin 0: 0.16 +- 0.24 | 0.20;
  bin 3: 1.29 +- 0.29 | 1.06; bin 6: 3.08 +- 0.74 | 3.08; bin 9: 9.14 +- 1.77 | 8.42; bin 12: 16.96 +- 2.85 | 20.13.
  Bins 13 and 14 (not graded): 23.6 +- 4.6 | 26.4 and 28.7 +- 6.9 | 35.2. Full table in `srh1r_grade.out`.
- Neighbours are 26 % of the model in bin 0, 33 % in bin 3, 4 % in bin 12. Without them T (all) is 13.9 to 14.4, still
  inside the line.
- The permuted-position sum is not small: about half the real neighbour term in every bin. Permuted positions are still
  galaxy positions, so this is a clustering baseline and not a clean null. Subtracting it does not change any status.
- k fixed at 1: T (all) 18.9, late 5.4, early 21.4 to 21.6 (13 degrees of freedom). The fitted k is 1.38 (all), 0.91
  (late), 1.42 (early).
- Late types: 2,613 lenses, T 5.4. That line passes on a large error, not on a tight fit.
- The neighbour term's k interpolation: error under 0.3 % of the model. A numpy matmul warning (divide by zero) was
  printed during the run; every reported value is finite.

## What is not claimed

- Not a pass. The frozen rule gives NO VERDICT when a twin does not bite, and two do not.
- Not a test of f. KiDS lensing as graded here does not see inside R_set. It neither supports nor excludes f = 0.4 to 0.7.
- Not a test of the share. With k free, share and mass calibration trade off.
- Not a statement about SRH1's other gates, form B, or the joint. The window, if any, is in a family picked after the
  forest fails were seen. The reference halo is FRZ1's (PROVISIONAL inputs); the pool is flux-limited, so the neighbour
  term is a lower bound; baryons are a central point; neighbours are laid out at the lens's redshift.
- My model for the data is 4 G DeltaSigma itself. SRH1 and ONE1 use the law's value times a projected ratio, a k fitted
  on the inner window, and a shape ratio. These are different statistics; see the comparison below.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
