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
