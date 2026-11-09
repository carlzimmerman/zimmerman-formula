# KO1R RESULT: independent regrade of KO1 (are KiDS's outer points the lens's own field?)

TEST lane, quarantined, not registered. Relabels nothing. Footings never pooled.
This regrade was written from `fable52_push/KO1_kids_outer_points/FROZEN_CRITERIA.md` (b1b91fae33) alone. No other file in that
folder was opened, listed, grepped or imported before this commit. All code is new (`ko1r.py`). Data conventions come from the
record's CFG96, CFG110, CFG116 and CFG903 staging scripts. One disclosure: after every KO1R number below was saved, and before this
commit, a `git status` of `fable52_push/` printed the file names in KO1's folder. It printed names only, not contents. Nothing in
KO1R changed after that. Run: `OMP_NUM_THREADS=1 python3 -u ko1r.py` (25 s on one thread;
peak RSS 1.38 to 1.46 GB across four complete runs, all numbers identical).

## Label

- **canonical (a0 9.3603e-11): NOT SEPARATED.** The raw label is LAW LEVEL HOLDS. The mass-scatter-corrected label is NO POWER,
  because the scaled error s^c = 0.2031 is 1.5 % above the 0.20 line. The two labels differ, so the frozen rule gives NOT SEPARATED.
  This label sits on a knife edge (see "How firm the canonical label is").
- **alt (a0 1.1312e-10): LAW LEVEL HOLDS.** The raw and corrected labels agree, and they hold under every variant tried.

KA1 to KA5 and the cross-shear null pass on both footings. All four MUTATEs bite.

## Numbers

| quantity | canonical | alt |
|---|---|---|
| KA1: per-lens sums by patch x type vs `cfg96_stack.npz` (W10/W20/W30), max relative deviation | 3.1e-11, PASS | same |
| KA2: candidates / lenses / fields ra, dec, z, logM, Mgal, typ, chi / f20, f30 | 605,531 / 181,477 / all equal / equal, PASS | same |
| KA3: x1.3, law plant, two-phase plant (max deviation) | 3.4e-16, PASS | 2.2e-16, PASS |
| KA4: std of z over 200 halvings (seed 52); mean | 1.053; +0.018, PASS | 1.053; +0.018, PASS |
| KA5: 1,000 planted hosts flagged; finder = brute force; decoys host their own lens | 1000/1000; yes; 0/3000, PASS | same |
| host-free n, f_w at (Delta 0.3, W 230) | 40,149, 0.2850 | same |
| host-free n, f_w at (0.3, 115) / (0.5, 230) / (0.5, 115) | 70,955, 0.4683 / 94,530, 0.6409 / 121,183, 0.7717 | same |
| setting the frozen rule selects | (0.3 dex, 230 Mpc), the first with f_w >= 0.20 | same |
| **A_hf +- s** (bins O, jackknife of A, 50 patches) | **1.0822 +- 0.1583** | **0.9847 +- 0.1440** |
| A_hf - 2s ... A_hf + 2s | 0.766 ... 1.399 | 0.697 ... 1.273 |
| A_II at X = 5.562 | 0.0554 | 0.0504 |
| A_II at X = 53.64 (the label's line) | 0.4611 | 0.4196 |
| mass-scatter slope b per log M* tercile (edges 10.391, 10.735) | +1.127 / +6.305 / +5.342 | same |
| e at sigma_M 0.2 (host-free WW-weighted over terciles); factor 10^(e/2) | 0.2163 dex; 1.2828 | same |
| **A_hf^c +- s^c** (sigma_M 0.2) | **1.3882 +- 0.2031** | **1.2632 +- 0.1848** |
| A_hf^c at sigma_M 0.1 (reported) | 1.1517 | 1.0480 |
| cross-shear null A_x (with the primary s_k); \|A_x\| / s | +0.1449; 0.92, PASS | +0.1318; 0.92, PASS |
| A, full W10 stack (181,477) | 1.7069 +- 0.0860 | 1.5531 +- 0.0783 |
| A(hosted) (141,328) | 2.0091 +- 0.1052 | 1.8281 +- 0.0958 |
| **A(hosted) - A_hf**, joint jackknife | **+0.9269 +- 0.1873** (4.9 s) | **+0.8434 +- 0.1704** (4.9 s) |
| R1 shells: W10 not W20 / W20 not W30 / W30 | 1.977 / 2.210 / 0.939 | 1.799 / 2.011 / 0.854 |
| bracket (three lowest bins) A_hf | 0.9908 +- 0.1906 | 0.9015 +- 0.1734 |
| per-bin D_k / M_k, host-free (bins 1-4 of O) | 0.07 / 0.96 / 1.54 / 1.24 | 0.07 / 0.87 / 1.40 / 1.13 |
| per-bin D_k / M_k, W10 | 1.54 / 1.45 / 1.97 / 1.93 | 1.40 / 1.32 / 1.79 / 1.76 |
| label: raw / corrected / final | LAW LEVEL HOLDS / NO POWER / **NOT SEPARATED** | LAW LEVEL HOLDS / LAW LEVEL HOLDS / **LAW LEVEL HOLDS** |

**What the numbers say.** Removing lenses that have a galaxy at least 0.3 dex more massive inside their own measured range, over a
230 Mpc window, takes the outer amplitude from 1.71 (W10, canonical) to 1.08. The lenses removed sit at 2.01, and the
hosted-minus-host-free difference is 4.9 s on both footings. So hosts carry the excess of the record's W10 stack above the law.
The host-free lenses sit at the law's level. They also sit above the two-phase exterior at the census cap: A_hf - 2s exceeds
A_II(53.64) by 0.31 (canonical) and 0.28 (alt). The canonical verdict fails to be LAW LEVEL HOLDS only because the corrected error
crosses 0.20. The lowest bin carries almost no host-free signal (D/M 0.07 +- 0.45 canonical), and the other three carry it.

**Unit-chain check (not R7 proper).** B21's published isolated points in these g_bar bins, converted here independently in SI, lie
1.18 / 1.49 / 1.56 / 1.73 times the point-mass law at the bin centres (canonical). The record's W10 stack, which has no random
subtraction, sits 1.4 to 2.0 times the law. Both are the same order, so the ESD-to-g chain is consistent.

## How firm the canonical label is (reported, not graded)

Before any lensing amplitude had been computed, the code fixed two readings: the tercile combination of e (C5) and the tie rule
(C3). The first run crashed after printing the mass-scatter factor and before any amplitude. The block below was added after the
second run, once the canonical s^c was seen to sit 1.5 % above the line. Nothing graded changed.

| variant | e (dex) | canonical A_c +- s_c, label | alt A_c +- s_c, label |
|---|---|---|---|
| graded: host-free WW-weighted terciles | 0.2163 | 1.3882 +- 0.2031, NOT SEPARATED | 1.2632 +- 0.1848, LAW LEVEL HOLDS |
| host-free count-weighted terciles | 0.2076 | 1.3744 +- 0.2010, NOT SEPARATED | 1.2506 +- 0.1829, LAW LEVEL HOLDS |
| one b over all lenses (no terciles; b = +5.145) | 0.2058 | 1.3716 +- 0.2006, NOT SEPARATED | 1.2480 +- 0.1826, LAW LEVEL HOLDS |
| per-lens model lowered by 10^(-e_t/2), A and s recomputed | n/a | 1.3866 +- 0.2027, NOT SEPARATED | 1.2616 +- 0.1845, LAW LEVEL HOLDS |
| unweighted mean of the tercile e's | 0.1703 | 1.3166 +- 0.1926, LAW LEVEL HOLDS | 1.1980 +- 0.1752, LAW LEVEL HOLDS |
| NO POWER tested on the uncorrected s in both computations | 0.2163 | LAW LEVEL HOLDS | LAW LEVEL HOLDS |
| mass ties by plain float comparison (40,667 host-free) | 0.2163 | A_hf 1.0978 +- 0.1544, A_c +- s_c 1.4082 +- 0.1981, LAW LEVEL HOLDS | A_hf 0.9989 +- 0.1405, LAW LEVEL HOLDS |

The canonical s^c reaches 0.20 at e = 0.2031 dex. The measured value is 0.2163. A rerun that counts mass ties by plain float
comparison, or that tests NO POWER on the uncorrected s, will read canonical LAW LEVEL HOLDS from the same data. Alt is LAW LEVEL
HOLDS in every variant. The correction itself is approximate. The frozen e = b sigma_M^2 assumes ln P(host-free) is linear in
log M*, but in the top tercile P is 0.246 / 0.470 / 0.716 at -0.1 / 0 / +0.1 dex.

## MUTATE (`ko1r_MUTATE.json`)

- M1, flags permuted within type x mass tercile x z-half cells: A(hosted) - A_hf = +0.326 +- 0.173 (canonical) and +0.296 +- 0.158
  (alt), inside 2 s. **Bites.** The true difference is 4.9 s, so M1 has power.
- M2, host-free WG over O x 0.4: BELOW THE LAW, TWO-PHASE WINDOW on both footings (A 0.433 / 0.394). **Bites.**
- M3, host-free WG = WW x the law model: LAW LEVEL HOLDS on both footings (A = 1.000). **Bites.**
- M4, isolation threshold log M* - 0.5: 208,250 lenses, and KA2 fails. **Bites.**

Not done in this regrade: R2 (except the three-bin bracket), R3 to R7, and the Lean file. The task named the primary statistic, the
label, KA1/KA2, the host flags, A(W10), A(hosted) and their difference.

## Reading choices

- **C1, jackknife of A.** Delete-one-patch over all 50 patches, normalised by (N-1)/N, with s_k fixed. The stack model M_k is
  recomputed in each replicate from that replicate's lenses. Holding M_k fixed changes s by less than 6e-5.
- **C2, lens chi in the host finder.** The lens's chi comes from the same comoving-distance call as the neighbour pool (the
  record's DC on the pool's own z array, grid to z 0.8), not from `lr_lenses.npz` (grid to z < 0.5). They differ by at most
  4e-5 Mpc. Using `lr_lenses.npz` chi changes no flag at any of the four settings.
- **C3, mass ties.** "log M*_j >= log M*_l + Delta" counts decimal ties as hosts, using a 1e-9 dex tolerance. MASS_MED carries
  5 or 6 significant digits, so exact 0.3 dex differences occur, and float rounding puts about half of them on either side.
  A plain float comparison changes 518 flags at (0.3, 230) (40,667 host-free instead of 40,149), 465 at (0.3, 115), and none at
  0.5 dex. **This flips the canonical label** (see the variant table above).
- **C4, separation and window.** theta is the great-circle angle from the chord, 2 arcsin(chord/2). The tests are d <= R_h
  (inclusive) and |chi_j - chi_l| < W (strict). R_h uses the record's constants (G 6.674e-11, Msun 1.989e30, Mpc 3.0857e22),
  the same ones the staged g_bar binning used.
- **C5, mass-scatter control.** Each lens's log M* is shifted by +-0.1. The threshold becomes (log M*_l + shift) + Delta, Mgal is
  recomputed from the shifted mass with the record's cold-gas recipe, and R_h follows it. Neighbour masses are not shifted.
  Terciles are the unweighted log M* terciles of the 181,477 lenses at their unshifted masses. P(host-free) is the unweighted
  fraction in each tercile, and b = [ln P(+0.1) - ln P(-0.1)] / 0.2. **One e for the whole set is the mean of b_t sigma_M^2,
  weighted by each tercile's host-free share of sum WW over O (0.045 / 0.267 / 0.688).** A_hf^c = A_hf 10^(e/2) and
  s^c = s 10^(e/2).
- **C6, null.** "Same weights" means the cross-shear amplitude uses the WG stack's s_k as inverse-variance weights. The "2.5 s"
  is the primary s of A_hf. With its own s_k and its own jackknife, A_x = +0.198 +- 0.176 (canonical), and the null still passes.
- **C7, gate line.** 0.891 as printed (10^-0.05 = 0.8913 changes nothing).
- **C8, corrected label.** It is computed with the full table, so NO POWER is tested on s^c. Unequal raw and corrected labels give
  NOT SEPARATED. **This is the reading that makes canonical NOT SEPARATED.**
- **C9, KA5.** "Flagged for exactly those lenses" cannot hold literally. A planted object 0.3 dex above its target also lies inside
  the measured range of other host-free lenses, and by the definition it is their host: 3,010 such lenses here, the same as brute
  force. KA5 was graded as follows. All 1,000 targets are flagged. The tree finder's flagged set equals a brute-force evaluation of
  the definition over every host-free lens. Of 3,000 decoys, placed at 1.05 R_h, at 1.02 W, or 0.02 dex under the threshold, none
  is a host of its own lens. Every decoy lens the finder flags (61) is one that brute force also flags.
- **C10, KA1.** The relative deviation is taken per cell, |a - b| / |b|. Cells where b = 0 must match exactly.
- **C11, KA4.** Exact halves come from a permutation (numpy default_rng(52)). The same 200 halvings serve both footings. Each half
  uses its own s_k and its own jackknife s. The std of z uses ddof = 1.
- **C12, M1.** "2 s" is the permuted difference's own joint jackknife error.
- **C13, A_II.** The stack two-phase model sum WW m_II / sum WW is projected onto the law model with the data's s_k, on the same
  lens set. The model is (4/pi)(1+X) times the annulus area-mean of G Mgal / R^2, on all four bins of O, since all lie outside
  the wall at 9.69e-15.
- **C14, law model.** The annulus area-mean of nu(g/a0) g is taken in closed form, (F(g_hi) - F(g_lo')) / (1/g_lo' - 1/g_hi) with
  g_lo' = max(g_lo, G Mgal / (3 Mpc)^2). It agrees with 96-point quadrature to 2e-13. Cells wholly beyond 3 Mpc carry no weight
  (checked: sum WW = 0).
- **C15, neighbour pool.** masked takes only the values 0 and 1, so "masked 0 or 1" keeps all objects. The pool holds 888,795
  objects (161,217 masked). The lens is excluded by its catalogue row.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
