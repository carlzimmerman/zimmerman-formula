# RCF1 FROZEN CRITERIA: refit the Milky Way rotation curves with the stellar mass free

2026-11-12. Written before any script or number for this lane. TEST lane. Adopts nothing. Relabels
no other lane. The published stellar masses are MWI1's web look-ups of abstracts and are
PROVISIONAL. kappa = 1/2 FITTED; not theory closed.

## Question

MWI1 took the rotation curve's baryon need from hunt item 35, which scaled ALL baryons of one census
by one amplitude A, gave no error on A, and had no hot gas, and then subtracted McMillan's cold gas
(1.191e10) and MB15 hot gas inside 27 kpc (0.15e10) to get a required stellar mass of 7.05 to 7.41e10
(canonical) and 6.36 to 6.73e10 (alt). Refit both curves with the stars as the only free mass (cold gas
and hot gas fixed), get the required stellar mass with a 68 per cent profile-likelihood interval and
the e_N upper limit, and regrade MWI1's five inventories with the fit's own error added.

## Disclosed before freezing

- Read before freezing: hunt item 35 (`hunt_2026/h34_h35_h38_milky_way.py` and `.out`), MWI1's
  criteria, script and result, MWG1's result.
- Item 35 fitted its amplitude on Ou et al.'s OWN baryon model (Misiriotis discs + de Salas Hernquist
  bulge; total 6.16e10), not on McMillan's; MWI1 then applied that A to McMillan's 6.681e10. Item 35
  also fitted over EVERY tabulated radius (Ou 6.3 to 27.3 kpc, Eilers 5.3 to 24.8 kpc), not 12 to 27
  kpc; only its slope statistic used 12 to 27 / 12 to 25.
- Hand expectation (not computed): with gas held fixed, every extra unit of mass must be stellar, and
  stellar force falls faster with radius than the gas discs', so the required stellar mass may come out
  somewhat ABOVE MWI1's subtraction (guess 7.2 to 7.8e10 canonical). Item 35's stat+sys chi2 is about
  0.4 to 0.6 per point, so the Delta chi2 = 1 interval should be a few per cent of the mass (guess
  +- 0.1 to 0.3e10), too small to move most of MWI1's classes. Not a prediction; disclosed.

## Inputs

- Data: `real_research/data/mw_rc_ou2024_table1.tsv` (37 points), `real_research/data/mw_rc_eilers2019_table1.tsv`
  (38 points). Random error = mean of the two quoted sides, as item 35.
- Errors (graded, item 35's "stat+sys"): sigma^2 = stat^2 + (f v)^2 with f = 0.04 for Ou at R < 22 kpc,
  0.15 for Ou at R >= 22 kpc, 0.035 for every Eilers point.
- Primary baryon census (graded): McMillan 2017 as ported in MWI1 (`mwi1.py`): thin disc, thick disc
  (exponential, Hankel in-plane force with their vertical profiles), bulge G M/(R + 0.7 kpc)^2 with
  M = 9.23e9; HI and H2 discs. Stars = thin + thick + bulge = 5.490e10, scaled together by s. Cold gas
  (HI + H2, 1.191e10) FIXED.
- Hot gas (graded): MB15, spherical, M_hot(<r) = 4.3e10 (r / 250 kpc)^1.5 Msun, in-plane force
  G M_hot(<R) / R^2, FIXED. Variant "none": no hot gas (reported per footing and data set, graded too).
- Kernel: nu(y) = 1 / (1 - exp(-sqrt(y))). Footings a0 = 9.36e-11 (canonical), 1.13e-10 (alt) m/s^2.
- External field, exactly item 35's form: v^2 / R = nu((g_N + e_N a0) / a0) g_N, with g_N the total
  in-plane Newtonian field at R; e_N free in [0, 0.03].
- Constants as in item 35: G = 6.674e-11, kpc = 3.0857e19 m, Msun = 1.989e30 kg.

## Statistic

chi2(s, e_N) = sum over points of ((v_model - v_obs) / sigma)^2, on a grid s in [0.5, 2.5] (step
0.0005) and e_N in [0, 0.03] (step 0.0002).

- Required stellar mass: M* = s_best x 5.490e10, with s_best at the global minimum.
- 68 per cent interval: s values whose profile chi2_p(s) = min over e_N of chi2 lies within 1 of the
  global minimum. Fit lower error = M*(best) - M*(lower end); upper likewise.
- e_N upper limit: the largest e_N whose profile over s lies within 1 of the global minimum (item 35's
  Delta chi2 = 1 rule). If it is the grid edge, report ">= 0.03 (bound)".
- chi2 per point at the best fit.

## Grading (per footing, per data set, per hot-gas variant)

For each of the five inventories (MWI1's values, units 1e10 Msun; upward error):
LN15 6.08 + 1.14; McM17 5.43 + 0.57; C20 5.04 + 0.43; I25 6.18 + 0.21; L25 2.607 + 0.363.

z = (M*(best) - published) / sqrt(published upward error^2 + fit lower error^2).
**SUPPLIED** if z <= 1; **WITHIN 2 SIGMA** if 1 < z <= 2; **NOT SUPPLIED** if z > 2.
Label per footing and data set: **SUPPLIED BY k OF 5** (naming them), followed by the class at McM17.
The MB15 variant is the headline; the no-hot-gas variant is graded and reported beside it.

## The question MWI1 asked, answered with a fixed rule (MB15 variant)

Per footing, per data set: the need **HOLDS** if M*(best) lies in [MWI1 low - 0.20, MWI1 high + 0.20]
(canonical [6.85, 7.61], alt [6.16, 6.93]); otherwise it **MOVES UP** or **MOVES DOWN**. Separately, the
number of inventories whose class differs from MWI1's class on that footing is reported
(MWI1: canonical LN15 SUPPLIED, others NOT SUPPLIED; alt LN15 and I25 SUPPLIED, McM17 WITHIN 2 SIGMA,
C20 and L25 NOT SUPPLIED). "CLASSES CHANGE" if that number is >= 1, else "CLASSES UNCHANGED".

## Reported, not graded

- Stat-only errors (item 35's other treatment): best s and interval.
- Radii R >= 12 kpc only (the radii MWI1 describes): best s, interval, e_N limit.
- Ou census variant: Ou's disc + bulge (5.20e10) scaled, Ou's HI, H2 and dust fixed, MB15 added.

## Known-answer checks (all must pass before any label; the script stops otherwise)

| id | check | pass condition |
|---|---|---|
| KA1 | item 35 reproduced: Ou's census (total must come out 6.16e10 within 0.5 per cent), ALL baryons scaled by A, no hot gas, item 35's own grids (A geomspace(0.5, 6, 120); e_N in {0} + geomspace(0.002, 5, 120)), stat+sys | canonical best M_b 8.75e10 (Ou curve) and 8.39e10 (Eilers) each within 0.10e10; alt A 1.31 (Ou) and 1.25 (Eilers) each within 0.02; e_N upper limits canonical 0.008 (Ou) and 0.006 (Eilers), alt 0.015 and 0.008, each within 0.002 |
| KA2 | McMillan census as ported | stars 5.490, cold gas 1.191 (1e10) each within 0.2 per cent; MWI1's force ratios r g_R / (G M_b) = 1.0599, 1.0614, 1.0586 at 20, 25, 30 kpc each within 0.003 |
| KA3 | independent SI check of the disc force routine | a razor-thin-limit exponential disc (z_d = 0.01 kpc, R_d = 2.5 kpc, M = 3.5e10) against Freeman's analytic v^2 = 4 pi G Sigma0 R_d y^2 [I0K0 - I1K1], y = R / 2R_d, at R = 4, 8, 16, 24 kpc, each within 0.5 per cent |
| KA4 | hot gas | MB15 mass inside 27 kpc = 0.153e10 within 1 per cent |
| KA5 | fit machinery | a mock curve made from the primary model at s = 1.30, e_N = 0.005 (canonical), with the Ou errors and no noise, returns s = 1.300 within 0.002 and chi2 < 1e-3 |

## Mutations (must bite; written to a separate file)

- M1 (must bite): kernel switched off (nu = 1). The required stellar mass on each data set must rise
  by more than 3 times the primary fit's upper error, or the best chi2 per point must at least double.
  If it does not, no label.
- M2 (reported): hot gas x 10 at fixed shape. The required stellar mass should fall.

## What a label will and will not mean

The interval is a Delta chi2 = 1 interval on per-point errors that treat a coherent systematic as
random; item 35 itself noted this flatters the fit, so the interval is a statement about this error
model, not a full systematic budget. Disc scale lengths, bulge shape and gas masses are held at the
census values. SUPPLIED says the fitted requirement is inside one published inventory's combined error
bar, not that the Galaxy has that mass.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
