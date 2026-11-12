# MWJ1 RESULT: one reading of the Milky Way passes every data set at once

> **NOTE 2026-11-12, after this result: owner decision on the external field** (`campaign_fresh_gravity/OWNER_DECISION_2026-11-12_EXTERNAL_FIELD_READING.md`).
> The owner adopted the actual-field reading of the Milky Way's external field. The field cases in this
> file use the record's earlier reading (e_N = 0.01273 inside the kernel as a Newtonian source). Under the
> adopted reading e_N is 0.000160 (canonical) / 0.000110 (alt), the field takes over near 800 kpc, and
> inside 300 kpc the line is the no-field case. The adopted field (0.00016 / 0.00011) lies inside the window at census baryons; the label's WEAKER FIELD is then the adopted field itself.
> See `closure_2026_11_12/EFC1_external_field_convention/RESULT.md`. The frozen labels stand as frozen.

2026-11-12. Criteria `FROZEN_CRITERIA.md` (b1235e89cd), committed alone before the script. A post hoc
consolidation: every input had been seen (NMB1, PLT1, the rotation-curve fit of hunt item 35). TEST
lane. Adopts nothing. Relabels no other lane. kappa = 1/2 FITTED; not theory closed.

## Labels

| footing | label |
|---|---|
| canonical | **CLOSES WITH CENSUS BARYONS, WEAKER FIELD, ROTATION CURVE INSIDE** |
| alt | **CLOSES WITH CENSUS BARYONS, WEAKER FIELD, ROTATION CURVE INSIDE** |

The window is the set of (external field e_N, baryon amplitude A) at which the line passes the
shape-measuring DESI curves at 30 and 80 kpc, the published masses at 100 kpc and beyond, and the
plateau rows beyond 150 kpc, together.

## The window

| | canonical | alt |
|---|---|---|
| field range at census baryons (A = 1) | 0 to 0.0075 | 0 to 0.0075 |
| the same without the plateau rows | 0 to 0.0145 | 0 to 0.0160 |
| amplitude range with no field | 0.91 to 1.50 | 0.79 to 1.31 |
| amplitude range at e_N = 0.008 | 1.02 to 1.51 | 1.02 to 1.32 |
| amplitude range at the record's field, 0.01273 | 1.26 to 1.51 | 1.26 to 1.32 |
| field range at the rotation curve's amplitude | 0 to 0.0130 (A = 1.28) | 0 to 0.0110 (A = 1.18) |
| rotation-curve box inside the window | all of it (102 of 102 grid points) | 113 of 155, those with e_N up to 0.011 |

What sets each edge: past 0.0075 at A = 1 the plateau rows fail first (satellite-class median
-2.04 at 0.008); below and above the amplitude range the DESI curves fail (Q just over 6.18).

## What it says

1. **All four data sets pass at one setting.** Rotation curve, halo-star curves, outer masses and
   plateau rows agree at a baryon amplitude of 1.26 to 1.31 times the McMillan census (canonical)
   or 1.15 to 1.21 (alt), with an external field no larger than the rotation curve's own limit of
   0.008. In mass that is 8.4 to 8.75 x 10^10 Msun (canonical) or 7.7 to 8.1 x 10^10 (alt).
2. **Census baryons pass everything except the rotation curve.** At A = 1 the halo stars and the
   outer masses are satisfied for fields up to 0.0075, but the rotation curve is not: it is what
   asks for the extra baryons (item 35).
3. **The record's point (0.01273, A = 1) fails on one gate only,** the plateau rows (satellite
   class, median -2.72). It passes the curves (Q 4.89 / 2.91) and the outer masses.
4. **More baryons, not a weaker field, is the other way to pass.** At the rotation curve's
   amplitude the outer data allow fields up to 0.013 on the canonical footing, which includes the
   environment's 0.01273. PLT1's post hoc statement that the satellite masses want a field below
   0.0078 holds only at census baryons. What then excludes 0.01273 is the rotation curve's own field
   limit (0.006 to 0.008), not the outer data.
5. **So the Milky Way reduces to one number.** The framework needs the Galaxy's baryons to be about
   a quarter to a third above the census (canonical). With that, every Milky Way data set in hand
   passes and nothing else has to move. Without it, the rotation curve fails. The census used has no
   hot halo gas; whether that supplies the difference is not computed here.

## What this is not

It does not derive kappa, the cold share or the missing rule (the joint). It selects no footing:
both pass. A window is the absence of a contradiction, on gates that NMB1 and PLT1 found to have
little power (the paper's own NFW passes them). The rotation-curve box is taken from the record,
not recomputed, and its amplitudes carry no error bars there.

## Checks

KA1: NMB1's Q reproduced at four points (4.89, 2.91, 2.40, 0.05). KA2: PLT1's class medians
reproduced at the same points. KA3: the line at 80 kpc 5.691 / 6.218 and 4.977 / 5.109. M1 (a0 times
16) and M2 (Newtonian baryons alone) each leave zero passing points on the full grid
(`mwj1_mut.out`).

## Files

`FROZEN_CRITERIA.md`, `mwj1.py`, `mwj1.out`, `mwj1_results.json`, `mwj1_mut.out`.
