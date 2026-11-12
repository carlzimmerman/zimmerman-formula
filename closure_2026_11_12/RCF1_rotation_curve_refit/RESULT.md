# RCF1 RESULT: the stellar-mass need holds under a proper refit; on Ou's curve it gets slightly worse

2026-11-12. Criteria `FROZEN_CRITERIA.md` (sha256 d90617bc..., `FREEZE_STAMP.txt`), written before the script.
TEST lane. Adopts nothing. Relabels no other lane. Published masses are MWI1's look-ups of abstracts and are
PROVISIONAL. One amendment (`AMENDMENT_A1.md`): a post hoc diagnostic only; no criterion or label changed.

## Labels (graded: McMillan census, stars x s, cold gas fixed, MB15 hot gas, stat+sys errors)

| data set | footing | required M* [1e10 Msun] (68%) | label | MWI1's need | classes vs MWI1 |
|---|---|---|---|---|---|
| Ou 2024 | canonical | 7.25 -0.19 / +0.16 | **SUPPLIED BY 0 OF 5; AT McM17 NOT SUPPLIED** | **HOLDS** | **CLASSES CHANGE** (LN15 SUPPLIED -> WITHIN 2 SIGMA, z = 1.01) |
| Ou 2024 | alt | 6.64 -0.15 / +0.15 | **SUPPLIED BY 1 OF 5 (LN15); AT McM17 NOT SUPPLIED** | **HOLDS** | **CLASSES CHANGE** (McM17 WITHIN 2 -> NOT, z = 2.05; I25 SUPPLIED -> WITHIN 2, z = 1.78) |
| Eilers 2019 | canonical | 6.96 -0.16 / +0.13 | **SUPPLIED BY 1 OF 5 (LN15); AT McM17 NOT SUPPLIED** | **HOLDS** | **CLASSES UNCHANGED** |
| Eilers 2019 | alt | 6.40 -0.12 / +0.12 | **SUPPLIED BY 2 OF 5 (LN15, I25); AT McM17 WITHIN 2 SIGMA** | **HOLDS** | **CLASSES UNCHANGED** |

With no hot gas the masses rise by 0.05 and the labels are the same, except Eilers alt: SUPPLIED BY 1 OF 5
(LN15); I25 goes to WITHIN 2 SIGMA (z = 1.08).

e_N upper limit: **>= 0.03 (bound)** on every footing and data set. The best fit sits at the frozen bound.

## What it says

1. **MWI1's need holds.** Freeing only the stars (cold gas and hot gas fixed) gives required stellar masses
   inside MWI1's ranges: canonical 6.96 to 7.25 (MWI1 7.05 to 7.41), alt 6.40 to 6.64 (MWI1 6.36 to 6.73).
   The subtraction MWI1 used was a fair shortcut.
2. **The error bar is small.** The fit's 68 per cent error is 0.12 to 0.19 x 10^10 (2 to 3 per cent). Added in
   quadrature it barely softens the z values. The two curves differ by 0.25 to 0.28 x 10^10, more than the
   fit error, so the pipeline choice matters more than the statistical error.
3. **Class changes are at the margins and go both ways with the curve.** On Ou's curve, the best fit (not
   MWI1's lower end) is graded, so canonical loses its only SUPPLIED (LN15 at z = 1.01) and alt loses I25 and
   drops McM17 to NOT SUPPLIED (z = 2.05). On Eilers' curve every class matches MWI1.
4. **The external field reverses.** Item 35 (Ou's census, all baryons scaled) found e_N consistent with zero
   with ceilings 0.006 to 0.015. With McMillan's census and only the stars scaled, the fit prefers the largest
   allowed field. Post hoc (A1, not graded), free on [0, 0.2], the best e_N is 0.038 to 0.065 (Delta chi2 = 1
   reach 0.07 to 0.10), and the gain over e_N = 0 is Delta chi2 = 1.6 to 5.6. So item 35's e_N ceiling depends on
   how the baryons are modelled. It is not a property of the data alone. On Ou's own census, with stars only
   scaled (reported variant), the ceilings are 0.005 to 0.016, close to item 35's.
5. **The bound moves M* by about 0.2.** Post hoc: with e_N = 0 fixed, M* = 7.08 / 6.81 (canonical, Ou / Eilers)
   and 6.42 / 6.20 (alt). With e_N free to 0.2: 7.32 / 7.00 and 6.87 / 6.58. All of these stay within about
   0.2 of MWI1's ranges.

## Numbers (stat+sys; McMillan census stars 5.490e10, cold gas 1.191e10)

| hot gas | curve | footing | s | M* [68%] | e_N best / upper | chi2/N |
|---|---|---|---|---|---|---|
| MB15 | Ou | canonical | 1.3200 | 7.247 [7.058, 7.409] | 0.030 / >= 0.03 | 0.169 |
| MB15 | Ou | alt | 1.2095 | 6.640 [6.489, 6.791] | 0.030 / >= 0.03 | 0.174 |
| MB15 | Eilers | canonical | 1.2685 | 6.964 [6.802, 7.096] | 0.030 / >= 0.03 | 0.201 |
| MB15 | Eilers | alt | 1.1650 | 6.396 [6.273, 6.520] | 0.030 / >= 0.03 | 0.225 |
| none | Ou | canonical | 1.3295 | 7.299 [7.091, 7.459] | 0.030 / >= 0.03 | 0.168 |
| none | Ou | alt | 1.2185 | 6.690 [6.539, 6.841] | 0.030 / >= 0.03 | 0.165 |
| none | Eilers | canonical | 1.2770 | 7.011 [6.830, 7.143] | 0.030 / >= 0.03 | 0.200 |
| none | Eilers | alt | 1.1735 | 6.443 [6.319, 6.566] | 0.030 / >= 0.03 | 0.213 |

z values (MB15; canonical Ou / alt Ou / canonical Eilers / alt Eilers): LN15 +1.01 / +0.49 / +0.77 / +0.28;
McM17 +3.03 / +2.05 / +2.59 / +1.66; C20 +4.70 / +3.51 / +4.19 / +3.03; I25 +3.77 / +1.78 / +2.96 / +0.89;
L25 +11.3 / +10.3 / +11.0 / +9.9.

Reported, not graded (`rcf1.out`):
- Stat-only errors: M* 7.16 / 6.68 (Ou), 6.85 / 6.36 (Eilers), intervals +-0.01 to 0.02, chi2/N 3 to 7.
- Radii >= 12 kpc only: M* 7.35 / 6.63 (Ou), 7.04 / 6.34 (Eilers), errors about +-0.2.
- Ou census, stars only scaled, MB15: M* 7.46 / 6.81 (Ou curve), 7.06 / 6.47 (Eilers). These are 0.08 to 0.21
  above the McMillan-census values.

## Checks

- KA1 (item 35 reproduced: Ou census 6.157e10, all scaled, no hot gas, its grids): M_b 8.745 (Ou) / 8.388
  (Eilers) canonical, alt A 1.307 / 1.253, e_N ceilings 0.0085 / 0.0057 canonical, 0.0154 / 0.0080 alt. PASS.
- KA2: McMillan stars 5.4903, cold gas 1.1911; MWI1 force ratios 1.0599, 1.0614, 1.0586. PASS.
- KA3 (independent, SI): a razor-thin exponential disc matches Freeman's analytic force within 0.34 per cent
  at 4 to 24 kpc. PASS.
- KA4: MB15 inside 27 kpc 0.1526e10. PASS.
- KA5: a noiseless mock (s = 1.30, e_N = 0.005) is recovered exactly. PASS.
- M1 (kernel off) bites everywhere: M* 12.7 (Ou) / 11.9 (Eilers), chi2/N 5.7 / 8.2. M2 (hot gas x 10) lowers
  M* by 0.42 to 0.45 (`rcf1_mut.out`).
- No check failed.

## Limits

- **The e_N bound binds.** The graded intervals are conditional on e_N <= 0.03. The post hoc unbounded fit
  wants 0.04 to 0.065, above the field that M31 supplies (0.017) and above item 35's ceiling.
- **The fit error model is generous.** chi2/N is 0.17 to 0.23, so the stat+sys per-point errors (a coherent
  systematic treated as random, as in item 35) are oversized. The Delta chi2 = 1 interval belongs to this
  error model and is not a full systematic budget. With stat-only errors the interval is 10 times narrower,
  but chi2/N is 3 to 7.
- Like item 35, the fit uses every tabulated radius (Ou 6.3 to 27.3 kpc, Eilers 5.3 to 24.8 kpc). MWI1
  describes 12 to 27 kpc. The R >= 12 variant moves M* by +0.10 / -0.01 (Ou) and +0.07 / -0.06 (Eilers).
- Disc scale lengths, bulge shape and gas discs are held at McMillan's values; the bulge is the MWI1 port
  (G M / (R + 0.7 kpc)^2). The kernel is applied algebraically in the plane, with no curl term.
- The census matters at the 0.1 to 0.2 level: Ou's census asks for more stars than McMillan's.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `rcf1.py`, `rcf1.out`, `rcf1_results.json`, `rcf1_mut.out`,
`AMENDMENT_A1.md`, `rcf1_posthoc.py`, `rcf1_posthoc.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
