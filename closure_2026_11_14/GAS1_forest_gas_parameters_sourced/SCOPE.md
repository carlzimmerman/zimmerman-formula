# GAS1 scope (frozen file; committed alone before any look-up)

Date: 2026-11-14. Lane type: literature look-up. Not blind, not a graded test. It relabels nothing and computes no forest
number.

## What I had seen before freezing

Only the brief. I have not yet opened any forest lane file, any forest code, or any web page for this lane. From memory I
know the papers named in the brief exist; no number from memory will be marked anything but PROVISIONAL.

## Quantities

1. Pressure smoothing scale lambda_P (comoving kpc after conversion to the record's convention).
2. Slope gamma of the temperature-density relation T = T0 (1+delta)^(gamma-1).
3. Temperature at mean density T0 (K).
4. Effective optical depth tau_eff(z) of the Lyman-alpha forest.

## Redshifts

Look-up grid: z = 2.2, 2.6, 3.0, 3.4, 3.8, 4.4. Reading anchors: z = 2.2, 3.0, 4.4.

## Bracket values to place

- lambda_P: 39.5, 79 (record primary), 91.4, 100 proper kpc (converted to comoving at each anchor: 100 (1+z) comoving kpc),
  138.6, 158 comoving kpc. Each converted to each paper's convention before placing.
- gamma: 1.2, 1.5 (record primary), 1.6.
- T0: 1e4 K (record primary).
- tau_eff: the record's formula 0.751 ((1+z)/4.5)^2.90 - 0.132 times 0.9, 1.0 (primary), 1.1.

## Also checked

- How lambda_P enters the record's own forest code (kernel form, comoving or proper, units), in both builds named in the
  brief, and whether a sqrt(2) or other factor separates it from each paper's definition.
- Whether 91.4 and 138.6 comoving kpc are correctly attributed to Rorai et al. 2017, Table S2, z 3.0.
- Whether the tau_eff formula is Becker et al. 2013's and whether its offset term is included.

## The rule (restated, frozen)

A bracket value is INSIDE 1 SIGMA at an anchor redshift if it lies within the 1-sigma interval of at least one published
measurement whose redshift is within 0.3 of the anchor; INSIDE 2 SIGMA likewise with 2-sigma intervals; otherwise
OUTSIDE. Where a paper gives only a 1-sigma interval, the 2-sigma interval is taken as twice the 1-sigma half-widths about
the central value (stated as such where used). Simulation-calibrated values are listed but marked as such and do not count
as measurements. Where measurements disagree with each other, say so and give both readings.

## Status labels

SEEN IN TEXT: the number was read in the fetched text of the paper or its table (quote under 15 words). PROVISIONAL: from a
search snippet, an abstract-level statement, a summariser's paraphrase, or memory. A number is never upgraded unless seen.
If a table cannot be opened, that is said rather than filled in.

## Files

SCOPE.md (this), SOURCES.md, CONVENTION.md, READING.md, fetch_log.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
