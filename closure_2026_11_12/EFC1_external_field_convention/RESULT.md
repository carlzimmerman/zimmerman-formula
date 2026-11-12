# EFC1 RESULT: the Milky Way's plateau exists only in the record's reading of the external field

2026-11-12. Criteria `FROZEN_CRITERIA.md` (5aa1a8ad15), committed alone before the script. A post hoc
consolidation prompted by LIT1. TEST lane. Adopts nothing. Relabels no other lane. Does not decide
which reading is right. kappa = 1/2 FITTED; not theory closed.

## Label

**CONVENTION-DEPENDENT** on both footings.

## The readings (canonical; alt in `efc1.out`)

Item 81's total external acceleration is 1.191 x 10^-12 m/s^2. Its dominant term is the LambdaCDM
linear-theory acceleration from all matter.

| reading | e_N inside the kernel | actual field it implies [a0] | takeover radius [kpc] | saturation mass [10^11] | line at 200 kpc [10^11] | census baryons | with hot gas |
|---|---|---|---|---|---|---|---|
| R, the record's: 1.19e-12 is the Newtonian source | 0.01273 | 0.119 | 88 | 5.28 | 5.26 | FAILS the plateau rows (-2.72) | PASSES |
| A: 1.19e-12 is the actual field | 0.00016 | 0.0127 | 789 | 44 | 13.7 | PASSES | PASSES (alt: fails the plateau rows high, +2.00) |
| L: literature, actual 0.01 a0 | 0.00010 | 0.010 | 1003 | 56 | 13.7 | PASSES | PASSES (alt: +2.01) |
| L: literature, actual 0.03 a0 | 0.00087 | 0.030 | 337 | 19 | 13.4 | PASSES | PASSES |
| B: baryons-only source | 0.0027 | 0.053 | 192 | 11 | 10.8 | PASSES | PASSES |

## What it says

1. **The record's reading implies an external acceleration 9.4 times (canonical) or 10.2 times (alt)
   the one it was derived from.** Putting 1.19 x 10^-12 m/s^2 inside the kernel as a Newtonian source
   makes the actual field 0.12 a0, or 1.1 x 10^-11 m/s^2. The published Milky Way work in this family
   quotes an actual field of 0.01 to 0.03 a0 (LIT1, PROVISIONAL).
2. **The plateau near 100 kpc belongs to that reading alone.** Under R the field takes over at
   88 kpc and the mass saturates at 5.3 x 10^11. If the same acceleration is the actual field, the
   takeover moves to about 800 kpc, and inside 300 kpc the line is the no-field line (13.7 x 10^11 at
   200 kpc). With a baryons-only source it is 192 kpc and 11 x 10^11.
3. **Every reading except the record's passes the outer data with census baryons.** The "field
   reading fails low against the satellite masses" (PLT1), "the record's point fails" (MWJ1) and the
   rescue by hot gas (MWG1) are all statements about reading R.
4. **Under the actual-field reading, hot gas is slightly too much on the alt footing.** The line then
   sits just above the satellite-class plateau rows (+2.00 to +2.01, at the gate).
5. **What this touches in the record.** Everything that used e_N = 0.01273 (or 0.02) inside the
   kernel: DW1's external-field rows, G239's plateau and its 80 kpc pulls, hunt item 38's "stops at
   5.07 x 10^11 beyond 71 kpc", FALSIFIER_MATRIX row 32 and its kill (a measured M(<200 kpc) >=
   1.0 x 10^12, which readings A and L would predict themselves), the 2026-11-12 correction lane's
   matched-field values, and today's PLT1, MWJ1, MWG1, SAT1 and NIM2 field cases. None is edited here.

## The lead's reading, labelled as such

Form B counts the cold component once: the kernel's boost is that component. The large-scale
acceleration item 81 computed already contains all matter, so applying the kernel to it counts the
cold component twice. On that argument reading A is the consistent one. This is an argument, not a
derivation, and the choice is the owner's.

## Checks

KA1: the vector sum of item 81's three terms reproduces 1.1913 x 10^-12 m/s^2 toward (268.4, +33.0).
KA2: at 0.01273, census, canonical: Q 4.89 and satellite-class plateau median -2.72 (MWJ1). KA3: the
inversion round trip to 2 x 10^-16. M1: with the kernel set to 1, reading A's e_N equals reading R's
(0.01273 / 0.01054), so the two differ by exactly the kernel factor (`efc1_mut.out`).

The first execution stopped on an undefined helper after the checks and the mutation and before any
reading was printed; the helper was replaced by the census total (6.6814 x 10^10) and the script
re-run. The criteria were not touched.

## Limits

- Hot gas is MWG1's uncapped Miller and Bregman profile; HG2's published-radius version narrows
  windows slightly.
- Reading B uses 0.049 for the baryon density against the source library's 0.0493.
- The large-scale term is linear theory on one density reconstruction with one bias (1.2); the lane
  takes item 81's number as given.
- The takeover radius is for a point mass equal to the census.
- The gates have little power (NMB1, PLT1).

## Files

`FROZEN_CRITERIA.md`, `efc1.py`, `efc1.out`, `efc1_results.json`, `efc1_mut.out`.
