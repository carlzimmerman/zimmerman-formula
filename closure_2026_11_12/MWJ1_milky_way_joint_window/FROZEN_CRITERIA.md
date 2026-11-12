# MWJ1 FROZEN CRITERIA: is there one reading of the Milky Way that passes every data set at once?

Committed alone, 2026-11-12, before any script and before any joint number was formed. TEST lane.
Adopts nothing. Relabels no other lane. kappa = 1/2 FITTED; not theory closed.

## Question

The owner asked to use the data to find closure. Data cannot derive the missing rule of the theory
(the joint, PAPER72 rule 6). What today's lanes can do is close one open input. The framework's
Milky Way line has two things it does not predict here: the external field strength e_N (the record
uses 0.01273 from the environment; the rotation curve prefers 0) and the baryon amplitude A (census
= 1; the rotation curve asks for more). For each footing, is there a single (e_N, A) at which the
line passes the shape-measuring DESI curves, the published masses at 100 kpc and beyond, and the
plateau rows beyond 150 kpc, all at once? And is the record's own value inside it?

## Post hoc consolidation, disclosed

Every input has been seen: NMB1's combined masses and covariance (origin 9d17287e7e), PLT1's rows
and its post hoc field value 0.0078 (origin b6a6f1d4f5), and the rotation-curve fit in
`hunt_2026/h34_h35_h38_milky_way.out` (item 35). The outline of the answer is therefore
foreseeable: a window near zero field that excludes 0.01273. What is new and frozen here is the
joint window in two variables, which gate binds each edge, and whether the rotation curve's own
values sit inside.

## Gates, per footing, on a grid e_N in [0, 0.03] step 0.0005 and A in [0.70, 1.80] step 0.01

The line is DW1's: McMillan 2017 baryons times A, kernel nu(y) = 1/(1 - exp(-sqrt(y))), G239's
QUMOND angle average at e_N (e_N = 0 is the no-field line). Footings canonical 9.36e-11, alt 1.13e-10.

- **G1, the curves:** NMB1's statistic Q at 30 and 80 kpc, with NMB1's theta and V unchanged,
  Q <= 6.180.
- **G2, the outer masses:** PLT1's rule unchanged: every row at r >= 100 kpc, 20 per cent floor,
  |median pull| <= 2 in class H and in class S.
- **G2p, the plateau rows:** the same on rows at r >= 150 kpc only (three in H, four in S).
- **The window W** is the set of grid points passing G1, G2 and G2p.
- **Rotation-curve box,** from the record, not recomputed: canonical A in [1.256, 1.310] and e_N in
  [0, 0.008]; alt A in [1.152, 1.208] and e_N in [0, 0.015] (item 35's two pipelines, amplitudes
  converted to the McMillan census; the narrower field limits 0.006 and 0.008 are reported too).

## Label, per footing

- **CLOSES AT THE RECORD'S VALUES** if (e_N = 0.01273, A = 1) is in W.
- **CLOSES WITH CENSUS BARYONS, WEAKER FIELD** if W contains points with A = 1 but not at 0.01273.
- **CLOSES ONLY WITH MORE BARYONS** if W is not empty but has no point at A = 1.
- **DOES NOT CLOSE** if W is empty.
- **ROTATION CURVE INSIDE** or **ROTATION CURVE OUTSIDE** is added according to whether W contains
  any point of the rotation-curve box.

Reported: the field range of W at A = 1 and at the rotation curve's amplitude; the amplitude range
at e_N = 0, 0.008 and 0.01273; which gate fails first past each edge; W without G2p.

## Known-answer checks (before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | at (0.01273, 1) and (0, 1) the script reproduces NMB1's Q | 4.89 / 2.91 and 2.40 / 0.05, each within 0.03 |
| KA2 | at the same points it reproduces PLT1's class medians (all rows) | -0.68, -1.56 / -0.66, -1.54 and +1.01, +0.28 / +1.34, +0.61, each within 0.02 |
| KA3 | the line at 80 kpc | 5.691 / 6.219 (no field) and 4.977 / 5.109 (0.01273), within 0.5 per cent |

## Mutations (each must empty the window)

M1: a0 multiplied by 16. M2: the kernel replaced by 1 (Newtonian baryons alone).

## What a label will and will not mean

A window says the Milky Way data in hand do not contradict the line at those two input values. It
does not derive either input, and it does not touch the missing rule. If the window excludes the
environment's field, that is a statement about the external-field treatment or about the outer
masses, on four satellite-class rows and a 20 per cent floor.
