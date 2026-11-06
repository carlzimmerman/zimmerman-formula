# QX26: does stellar IMF variation explain the hot/early-type step? PARTLY for early-type galaxies, NOT for groups, clusters or dSphs

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (local c2cbd5086d, origin
44b5658218), committed and pushed before any script. Script: qx26.py (one thread, under a minute). Outputs: qx26.out /
qx26.json (main) and qx26_MUTATE.out / qx26_MUTATE.json (alpha x 2).

**IMF relation:** Posacki+2015, log alpha = 0.38 log(sigma_e/200) - 0.06, with alpha measured relative to Salpeter.
Relative to Kroupa that is a factor of x1.06 at 100 km/s, x1.38 at 200 km/s and x1.61 at 300 km/s.

## Labels (primary inputs, both footings)

| Class | Kroupa offset (canonical / alt) | after IMF | F removed | Label |
|---|---|---|---|---|
| X-ray ellipticals | +0.210 / +0.189 | **+0.093 / +0.074** | 0.56 / 0.61 | **PARTLY**; now inside the G7 line, sigma x0.9-1.1 robust |
| KiDS early-type lenses (step +0.158 +- 0.064) | +0.158 | residual +0.080 to +0.122 | 0.23-0.49 (sigma_e 130-210) | **PARTLY** |
| X-COP | +0.467 / +0.435 | +0.448 / +0.415 | 0.04 | **NOT** |
| groups (f* 0.5) | +0.264 / +0.226 | +0.227 / +0.190 | 0.11-0.19 | **NOT** |
| dSphs | about +0.2 | no correction (sigma 7-12 km/s, outside the relation) | 0 | **NOT** |

### X-ray ellipticals

- The heavier IMF brings the class mean inside G7's 0.15 line. The frozen F threshold for "explained" is 0.8, and the
  IMF removes only 56-61% of the offset, so the label is PARTLY.
- **Per-galaxy offsets after IMF (canonical).** NGC 720 still sits at +0.42 and NGC 4649 at +0.26. The three galaxies
  that were near zero go negative, to -0.05 / -0.11 / -0.12.
- The galaxy carrying the largest miss, NGC 720, has one of the lowest sigma in the sample, so the IMF helps it
  least.

### SPARC consistency (bulge Upsilon x IMF factor at sigma_b 100-200 km/s)

- **Canonical.** The rms moves from 0.0541 to 0.0584 at U 0.51-0.52, which still passes. The pass is preserved.
- **Alt.** The frozen rule reads "BREAKS SPARC". That is a defect in the rule, disclosed here: alt already fails the
  U line at bulge factor 1 (U 0.44). That baseline failure is QX8's known law-mode result. The IMF does not cause it,
  and it changes rms by at most 0.0034.
- The correct reading on both footings is that the IMF relation does not change SPARC's pass/fail.

## Reading

**IMF variation is a real, measured systematic, and it takes about half of the step in early-type galaxies:**
- X-ray ellipticals: 56-61%;
- KiDS early-type lenses: 23-49%.

It cannot touch the step where stars are a small share of the baryons, or where sigma is low. Groups keep 81-89% of
their offset, X-COP keeps 96%, and dSphs keep all of it. In dSphs, nulling +0.2 in deep MOND would take x2.5
stellar mass, while the relation runs the other way at low sigma.

**So the cluster/group part of the step, and the dSph part, survive any IMF reading.** QX20-QX24's target for a
mechanism stands, with the early-type-galaxy rung lowered to about +0.07 to +0.12.

## Known answers and controls

- KA1: with Kroupa, the X-ray ellipticals reproduce QX18 to 1.1e-4 / 2.4e-4 (line 1e-3). X-COP and groups reproduce
  QX20's class means to 8e-7. PASS.
- KA2: the SPARC grade at bulge factor 1 reproduces P4 / QX8 KA1 exactly (0.054087 @ 0.52, 0.053718 @ 0.44). PASS.
- MUTATE (alpha x 2 on the ellipticals): F = 1.71 / 1.87, which over-corrects (line F > 1), so the control bites.

## Disclosed limits

- Posacki's coefficients were web-verified against the arXiv abstract only (PROVISIONAL). Its alpha comes from Jeans
  models that include a dark halo, so it is a halo-processed input.
- The elliptical sigma_0 values are transcribed HyperLEDA values, not read from a file. The labels hold for all
  sigma_0 scaled x0.9 and x1.1.
- KiDS has no per-lens sigma, so the bracket 130-210 km/s is a proxy. The correction assumes f_cold = 0 for early
  types, which is the maximum.
- X-COP and group stellar masses are taken as Kroupa-equivalent; this is stated, not checked.
- The SPARC bulge sigma is a bracket, not per galaxy.

Kappa = 1/2 FITTED; not theory closed.
