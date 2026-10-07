# CFG401: Genzel+2017 with stars + an extended gas disc. Do the six galaxies agree on a0? NO (gate failed)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 009c0205e. Inputs: CFG400's digitised points (cfg400_points.csv); the shape is declared with no fit: gas disc at 2 x R_d (the record's convention), gas fractions from Genzel's Table 1 priors (0.40-0.70); beam cut at FWHM 0.6".

**Gate G-CONSISTENCY: FAIL. No law comparison is made.**

| galaxy | z | f_gas | points | best a0 (x local) | chi2/N |
|---|---|---|---|---|---|
| COS4 01351 | 0.85 | 0.40 | 12 | x1.41 | 0.46 |
| D3a 6397 | 1.50 | 0.48 | 7 | **x0.01 (grid edge)** | 1.49 |
| GS4 43501 | 1.61 | 0.45 | 7 | x0.89 | 0.38 |
| zC 406690 | 2.20 | 0.70 | 8 | **x0.01 (grid edge)** | 2.90 |
| zC 400569 | 2.24 | 0.52 | 6 | **x0.01 (grid edge)** | 0.50 |
| D3a 15504 | 2.38 | 0.45 | 8 | x0.07 | 0.77 |

The spread (16-84%) is 1.99 dex.

**Reading.**
- Adding the extended gas disc removes CFG400's "a0 -> huge" pull. The two lower-z discs now sit near the local a0 (x1.4, x0.9).
- Three of the four z > 2 discs (and D3a 6397) now prefer a0 -> 0: their curves fall like pure Newtonian baryons, with no MOND boost. That is Genzel+2017's own headline, and a known tension for MOND-type laws at high z (open in the literature: outer pressure support, the external-field effect, disc thickness and beam corrections all move it).
- By the frozen gate this is NOT scored: the per-galaxy a0 is shape-degenerate with only 6-8 beam-resolved points at g of about 1-10 a0 (y mostly >= 1).
- **It is recorded as a possible high-z tension for the law, unresolved until resolved gas maps fix the baryon shapes.** It is neither a pass nor a fail of a0(z).

**Consequence for the decisive test.** Public Genzel+2017 data cannot run CFG385's self-calibrated test. It needs (i) resolved gas-profile shapes (ALMA CO / [CI] at sub-kpc), (ii) AO-resolved inner curves and (iii) deep outer curves that reach y <~ 0.3, all for the same galaxies. That is a future-data / proposal item, not something this repository can do now.

MUTATE (gas at 1 x R_d) moves the spread 1.99 -> 2.41 dex (> 0.2), rc 1. C1 (reduction to stars-only) passes.
