# CFG669: independent F277W photometry of B1938+666 perturber A — NOT DIAGNOSTIC (the method cannot separate A from the arc)

Criteria 899403b81 (committed alone before any pixel was opened). Scores the sealed CFG668 prediction (9162427f…). Data: JWST
GO 8281 F277W level-3 mosaic (88 ks, public), in `../../../_external_data/cfg668_go8281/` (not committed). `python3 -I cfg669.py`.
κ = ½ FITTED; footings separate; cold energy mass required; not "theory closed"; nothing here says the data favour the framework.

**Label (both footings): NOT DIAGNOSTIC.** CFG668's prediction stands untested; it waits for the PI team's lens + light modelling.

## What happened, in order

1. **Frozen centre rule failed (bug, disclosed).** "Brightest pixel within 1″" locked onto a bright knot of the Einstein ring,
   not the lens nucleus, so A's aperture fell outside the ring (`*_FROZENCENTRE.*`, kept: S = 0.03, limit 25.4 AB, MUTATE not
   recovered). **Deviation:** the nucleus = local maximum nearest the flux-weighted centre of lens + ring (env `CFG669_CENTRE`;
   `frozen` reproduces the original). The corrected cutout (`cfg669_cutout.png`) puts A on the arc, as Vegetti+2012 describe.
2. **With the correct centre the frozen rule fires "SURVIVES" (S = 9.9, m_A = 23.4 AB). It is rejected, not claimed:**
   - 23.4 AB is ~3 mag brighter than the predicted bright end (26.4) — it would mean ~1e10 M☉ of stars inside a 1e8 M☉ lens mass;
   - the MUTATE tooth fails: an injected 28.0 AB point source changes E by only 2% and is "recovered" at 23.35, i.e. the aperture
     is dominated by something ~100× brighter;
   - the image shows the aperture on the brightest ridge of the lensed arc; the local annulus cannot remove a curved arc, and A's
     position (the arc's brightest part) ranks highest among the same-radius references for that reason.
   The excess is lensed source light, not A.
3. Per the record's rule (a measurement whose tooth fails is not diagnostic), the lane is NOT DIAGNOSTIC.

## What it takes

A full lens + source + lens-light model (pixelated source reconstruction) so the arc is predicted and subtracted, then the
residual at A tested against the sealed 26.4–29.6 AB band. That is what GO 8281 was designed for; the PI team's paper, or an
independent forward model (e.g. PyAutoLens), is the scorer. CFG668's sealed numbers and rules are unchanged.

---

# Part 2 (criteria 83f30af17): full lens + source + light model — NOT DIAGNOSTIC (tooth fails)

`python3 -I cfg669_lensmodel.py` → `cfg669_lensmodel.out/.log`, `cfg669_lensmodel_results.json`, `cfg669_lensmodel.png` (~5 min).
Empirical PSF from 22 stars; Sérsic lens light; SIE + shear; 24² pixelated source with evidence-set regularisation; PSF point
component at A. Frozen method, run once.

| quantity | value |
|---|---|
| fit | χ² 2.23e6 on 1681 pixels (χ²_ν 1337); λ_rel at the grid edge (1e-3); Sérsic R_e and q at their bounds |
| A amplitude | 7.2e-7 Jy (24.25 AB), σ_tot 4.7e-7 Jy (stat 2.4e-7, same-radius 3.7e-7, sys 1.7e-7); **S = 1.5** |
| 2σ limit | **23.96 AB** (needed for a test: 29.6–30.8) |
| tooth | 28.0 AB injected: recovered 28.00 (linear) / 27.55 (refit) but **S = 0.05 / 0.07 → FAILS** |
| **verdict** | **NOT DIAGNOSTIC (tooth fails), both footings** |

**Why, and what it means (diagnostic, no verdict weight):** the model reproduces the ring by eye, but the residuals are ±5σ
everywhere (sky level not modelled, single Sérsic too simple at S/N ~400 per pixel). More important, even a perfect model would not
reach the exclusion line here: the statistical error on A's amplitude at χ²_ν = 1 is 2.4e-7/√1337 = **6.6e-9 Jy, a 2σ floor of
≈ 28.1 AB**, set by the degeneracy between a point source at A and the reconstructed arc at 0.063″ pixels. So in F277W this data
could at best **confirm** A if it sits at the bright end of the sealed band (26.4–28.1 AB) but **cannot exclude** it (exclusion
needs a limit fainter than 30.8). The F115W mosaic (0.031″ pixels, 2.4 GB, not downloaded) and the PI team's dedicated modelling
are the remaining routes. CFG668 stays sealed and untested.
