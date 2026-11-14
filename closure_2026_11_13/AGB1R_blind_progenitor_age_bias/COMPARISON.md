# AGB1R against AGB1 — comparison (written after both builds landed)

Order of events: `READING.md` committed at 9090ca051c, before any real-data number. `RESULT_BLIND.md` with all scripts and
outputs committed at 632add7214. Only after that did I open AGB1's `README.md`, and then its output files and the parts of
`agb1_run.py` / `agb1_template.py` needed to explain differences. The comparison helpers (`agb1r_compare_numbers.py`,
`agb1r_compare_points.py`, `agb1r_compare_templates.py`) and their outputs were written after that point. They change no
number or word in `RESULT_BLIND.md`. Nothing is adopted; no ledger is edited.

## Words, side by side

| word | AGB1 | AGB1R (blind) | same? |
|---|---|---|---|
| W1 | UNDECIDED / ROBUST | UNDECIDED, ROBUST | yes |
| W2, A = 0 | ACCELERATING TODAY | ACCELERATING TODAY | yes |
| W2, A = 1 | SIGN NOT SETTLED | SIGN NOT SETTLED | yes |
| W2, A free | SIGN NOT SETTLED | SIGN NOT SETTLED | yes |
| W3, all three forks | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA | yes |
| W2 / W3 on `des_only` | same words as `full` | same words as `full` | yes |
| W1c | UNDECIDED / ROBUST | UNDECIDED, ROBUST | yes |
| W2c (A = 0, 1, free) | ACCELERATING TODAY / SIGN NOT SETTLED / SIGN NOT SETTLED | the same | yes |
| W3c, all three forks | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA | NEVER-ACCELERATED EXCLUDED AT 3 SIGMA | yes |
| first word of W1 on `des_only`, `rand197`, `bao_overlap` | UNDECIDED ×3 | UNDECIDED ×3 | yes |
| Part B (A1–A3, B1, B2) | run (AGE-DEPENDENT; SHIFTED at z* 1.0 and 1.2, STABLE at 1.5 and 2.33; CLASS UNCHANGED) | **not run** (outside the blind reading list) | not compared |

**No word differs.** Every known-answer check passes in both builds: KT, K1, K2, K3 (both twins), K4, KA, K5, K6.

## Numbers
`agb1r_compare_numbers.py` compares 196 numbers from the two builds' outputs: the A profile summaries of all six
sample/part combinations, every fork's parameters, χ² and Δχ², the largest grid-point gap in each profile, the T_W rows
and K5. 182 agree within 0.005 in χ² and 0.0015 in parameters. The typical gap is 3 × 10⁻⁴ in χ² and 4 × 10⁻⁵ in an
interval end. The `rand197` numbers agree to 4 × 10⁻⁴ in χ², so my reading of LGS1's draw (READING.md, ambiguity 2)
picked the same 197 supernovae.

Every difference larger than rounding at the README's printed precision, with which build is right:

| # | quantity | AGB1 | AGB1R | cause | right build |
|---|---|---|---|---|---|
| 1 | Part C `full` A = 0: Δχ²_today (printed) | 27.374 (27.37) | 27.379 (27.38) | Both builds reach the same fitted point to four decimals. AGB1 interpolates the Part C supernova D_M linearly from a 601-point CAMB grid in ln(1+z) (`agb1_run.py`), which moves μ by up to 2 × 10⁻⁵ mag and lowers the SN χ² at that point by 0.0046. With AGB1's interpolation my model gives AGB1's SN χ² (1650.1022) exactly. | **AGB1R.** It takes CAMB's D_M at each redshift, which is exact to 10⁻¹³. |
| 2 | Part C `full` A = 0: Δχ²_never | 199.311 | 199.336 | Two effects pull in opposite directions. AGB1's interpolation lowers its χ² at the never point by 0.012. My Part C penalty minimiser stopped 0.013 short: my model scores 1839.0896 at AGB1's point (q ≥ −2 × 10⁻⁵), below my own fit's 1839.1028. With exact distances, the value is ≤ 199.323. | **Neither exactly.** AGB1's minimiser and AGB1R's distances are right. Both print 199.3; the word holds by a wide margin. |
| 3 | Part C `des_only` A = 0: Δχ²_never | 118.237 | 118.246 | As in row 2: my minimiser 0.007 short, AGB1's interpolation −0.002. With exact distances, ≤ 118.239. | **AGB1 is closer** (by its minimiser). Both print 118.2. |
| 4 | Part C, other never fits (`full` A1, Afree; `des_only` A1, Afree) | 56.980, 39.280, 50.377, 38.470 | 56.985, 39.281, 50.378, 38.474 | The same two effects, each ≤ 0.004. With exact distances: ≤ 56.984, 39.279, 50.378, 38.470. | Within 0.005; both print the same. |
| 5 | Part A `bao_overlap`, A free: Δχ²_never | 16.784 | 16.776 | Both fits sit on the Ω_m = 0.05 floor. My fit's χ² is 1651.7689; AGB1's point scores 1651.7765 in my model (the same model as its own to 10⁻³), so AGB1's minimiser stopped 0.008 short on the prior edge. | **AGB1R.** It is a control with no word, and both print 16.8. |
| 6 | Part C `full` profile, far end: χ² at A = 2.75 and 3.0 | 1679.743, 1698.761 | 1679.735, 1698.725 | At A = 2.75 the gap is the interpolation alone (my model at AGB1's point gives 1679.7354). At A = 3.0, where the fit sits on wa = −3, AGB1's minimiser stopped 0.026 short, plus 0.011 from the interpolation. | **AGB1R.** No interval or word reaches this end. |
| 7 | `tmpl_W` (reported only), `full`: best A_W; Δχ²(A_W = 0, 0.23, 1); Δχ² = 1 lower end | 2.278; 1.845, 1.492, 0.582; 0.602 | 2.287; 1.859, 1.505, 0.590; 0.611 | The template. I built a reference T_W with the 40 Myr cutoff handled exactly and adaptive quadrature for t(z) (`agb1r_compare_templates.out`). AGB1's T_W sits 3 to 7 × 10⁻⁵ mag above it: its trapezoid in τ on a log grid from 1 Myr straddles the cutoff. Mine is within 4 × 10⁻⁶. With AGB1's T_W in my fitter, I get AGB1's numbers (A_W 2.2784, χ² 1636.5002, Δχ²(0) 1.8448). | **AGB1R.** No frozen word. AGB1's README prints 1.84 / 1.49 / 0.58; the reference template gives 1.86 / 1.50 / 0.59. |
| 8 | `tmpl_W`, `des_only`: best A_W; Δχ² = 1 lower end; Δχ²(A_W = 1) printed | 1.936; 0.176; 0.28 | 1.939; 0.179; 0.29 (0.286) | Same template cause. | **AGB1R.** |

Within rounding, though the printed digits differ:
- **K3.** AGB1 recovers A as 1.00000 / 0.00000 with χ²_min about 10⁻¹⁰. Mine gives 1.00001 / −0.00001 with χ²_min
  4 × 10⁻⁸, because my Nelder–Mead tolerance is looser. Both pass by three orders of magnitude.
- **KA spline minimum.** 0.61814 against 0.61817.
- **Redshift of the smallest q.** Printed 0.29 / 0.28 / 0.19 by AGB1 against 0.285 / 0.285 / 0.185 by me, and 0 against
  0.005 for Part C `full` A = 0. AGB1 scans q on a 0.01 grid and I use 0.005. The smallest q itself agrees to 10⁻⁴.
- **`bao_overlap`, A = 1: wa.** AGB1 −0.85352 prints −0.854; mine −0.85350 prints −0.853.
- **Part A profile at A = 3.0.** My χ² is lower by up to 0.0045, with the fits on the wa = −3 wall. It is inside the
  tolerance and touches no interval.

## What only one build has
- **Part B (AGB1 only).** Not checked by this re-grade. Its words (CFG684 AGE-DEPENDENT, FLOOR HOLDS on `full` and
  FLOOR LOST on `des_only`; CFG689 SHIFTED at z* 1.0 and 1.2) rest on AGB1 alone.
- **AGB1's post hoc no-supernova table.** Its BAO + CMB row (Ω_m 0.351, w0 −0.448, wa −1.638, q0 +0.063) equals my K5
  w0–wa fit (0.3506, −0.448, −1.638, +0.063).
- **AGB1R's brute-force grid cross-check** of all 18 Part A fork fits on `full` and `des_only`. It confirms the fork
  minima of both builds to 10⁻⁴ (one at 3 × 10⁻⁴).
- **AGB1R's random-start check** of the threshold-nearest Part C fit. W2c at A = 1 is 3.567 (mine) against 3.569
  (AGB1); with exact distances the value is 3.567. The two builds agree that it lies below 4.

## Bottom line
Two builds written apart, with different integrators (cubic Hermite against linear interpolation in Part A; CAMB at
each redshift against a 601-point grid in Part C), different template integration and different minimisers. They reach
the same frozen words (W1–W3 and W1c–W3c, every fork, `full` and `des_only`) and the same check verdicts. Their numbers agree to the printed digit except for the eight
rows above. Each of those is explained: one template quadrature error and one interpolation error on AGB1's side, and
a never-accelerated minimiser that stops up to 0.013 short on mine in Part C. None moves a word. The nearest thresholds
are W2 at A = 1 (3.41 Part A, 3.57 Part C, against 4) and W1's Δχ²(A = 0) on `full` (2.10 Part A, 2.54 Part C, against
4). Both builds agree on those to ≤ 0.002.

AGB1's README ends "No blind re-grade has been run." This folder is that re-grade. I did not edit AGB1's README.

kappa = 1/2 FITTED; not theory closed.
