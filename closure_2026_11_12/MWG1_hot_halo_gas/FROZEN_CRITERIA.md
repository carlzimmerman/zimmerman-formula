# MWG1 FROZEN CRITERIA: can hot halo gas supply the Milky Way's missing baryons?

Committed alone, 2026-11-12, before any script and before any gate was evaluated with gas added.
TEST lane. Adopts nothing. Relabels no other lane. kappa = 1/2 FITTED; not theory closed.

## Question

MWJ1 (origin 574212f896) reduced the Milky Way to one number: the line passes every data set if the
baryons are 1.26 to 1.31 times the McMillan census (canonical) or 1.15 to 1.21 (alt). The census has
no hot halo gas. Published estimates put a few times 10^10 Msun of it inside the virial radius. Two
separate things are asked, because the gas is extended and the rotation curve is not:

1. Does the hot gas inside the rotation curve's radii supply what the rotation curve asks for?
2. With the census left at A = 1 and the hot gas added where it is, do the outer data pass, and at
   what external field?

## Disclosed before freezing

From general knowledge, a profile with mass rising as r^1.5 puts only a few per cent of its total
inside 27 kpc, so the expected answer to (1) is no. For (2), a hand estimate with the Miller and
Bregman profile at the record's field gave satellite-class plateau pulls near -1.3, so a pass is
expected there. Neither has been computed with the gates. The literature values below came from web
look-ups of abstracts and are PROVISIONAL.

## Hot-gas models (enclosed mass M_hot(<r) = M_ref (r / r_ref)^p; spherical)

| id | source | M_ref inside r_ref | p | status of the shape |
|---|---|---|---|---|
| MB15 (primary) | Miller and Bregman 2015, ApJ 800, 14: O VIII emission, beta = 0.50 | 4.3 x 10^10 inside 250 kpc | 1.5 | published: also gives 3.8 x 10^9 inside 50 kpc, which p = 1.5 reproduces |
| S15 (low) | Salem et al. 2015: LMC ram pressure | 2.6 x 10^10 inside 300 kpc | 1.5 | beta profile; beta = 0.5 assumed here |
| F20 | Faerman et al. 2020, isentropic corona | 5.5 x 10^10 inside 280 kpc | 1.5 | shape not in the abstract; assumed |
| F17 (high) | Faerman et al. 2017, isothermal corona | 1.2 x 10^11 inside 250 kpc | 2.0 | radius and slope from memory; assumed |

MB15 is primary because it is the only one whose profile is fixed by two published masses and whose
method does not assume a gravity law. The Faerman models are hydrostatic in a dark-matter potential.
A disc-like hot component (eROSITA, scale height 1 to 3 kpc) is not included: no mass was found for
it.

## Part 1, the rotation curve

Item 35's fit covers 12 to 27 kpc. Needed extra baryons, from the record: 1.71 to 2.07 x 10^10 Msun
(canonical), 1.01 to 1.39 x 10^10 (alt). Supplied: M_hot(<27 kpc), the most that can act inside the
outermost fitted radius. **SUPPLIED** if M_hot(<27 kpc) reaches the lower end of the need; **NOT
SUPPLIED** otherwise; the fraction is printed for every model.

## Part 2, the outer data

The line is MWJ1's with M_b(<r) = census M_sph(<r) + M_hot(<r), amplitude A = 1 on the census, same
kernel, G239's angle average at e_N, both footings. Gates exactly as MWJ1: G1 (NMB1's Q <= 6.180 at
30 and 80 kpc), G2 (PLT1's class medians, rows at r >= 100 kpc), G2p (rows at r >= 150 kpc). For each
model and footing: the range of e_N in [0, 0.03] (step 0.0005) passing all three, and whether the
record's 0.01273 passes.

## Label, per footing

- Part 1: **ROTATION CURVE NOT SUPPLIED** if no model supplies it; **SUPPLIED IN k OF 4** otherwise.
- Part 2, on MB15: **RECORD'S FIELD PASSES WITH HOT GAS** if e_N = 0.01273 passes G1, G2 and G2p;
  **RECORD'S FIELD STILL FAILS** otherwise. **FRAGILE** is appended if S15, F20 or F17 gives the
  other answer.

Reported: the field window for each model; the plateau medians at 0.01273; whether the window still
contains fields at or below the rotation curve's limit of 0.008.

## Known-answer checks (before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | with no gas the script reproduces MWJ1 | Q 4.89 / 2.91 and satellite-class plateau median -2.72 at (0.01273, 1); field window at A = 1 equal to 0 to 0.0075 on both footings |
| KA2 | MB15's profile | 3.8 x 10^9 inside 50 kpc within 3 per cent |
| KA3 | the line at 80 kpc with no gas | 5.691 / 6.219 and 4.977 / 5.109 within 0.5 per cent |

## Mutation (must bite)

M1: ten times the MB15 gas. The point (e_N = 0, census) must then fail at least one gate.

## What a label will and will not mean

Hot-gas masses differ by a factor of about four between methods and rest on assumed metallicities
and extents. A pass in Part 2 says published gas, placed where it is published to be, lifts the
outer line enough; it does not measure the gas. Part 1 is an upper bound argument: a spherical halo's
mass inside the outermost fitted radius, not a refit of the rotation curve.
