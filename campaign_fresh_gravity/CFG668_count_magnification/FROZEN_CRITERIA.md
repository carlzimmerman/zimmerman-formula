# CFG668 — background-galaxy counts through clusters vs blank sky (FROZEN, before any data pull)

Block CFG660–669 (owner chat). Question (owner, 2026-10-12): how many background galaxies do we see
looking through rich clusters (where cold energy sits) vs looking through blank sky?

## Data (raw, no ΛCDM)
- Clusters: redMaPPer SDSS DR8 (VizieR J/ApJS/224/1/cat_dr8), richness λ > 60, 0.1 ≤ z_λ ≤ 0.3. Positions only.
- Galaxies: SDSS DR18 PhotoObj type=3 (galaxy), clean photometry, dereddened r, joined to Photoz.
- Controls: random positions in the same SDSS footprint (≥ as many as clusters), same query.
- Apertures are ANGULAR (0–2', 2–4', 4–6' annuli); no distances, no halo model, no cosmology.
- Background: photo-z > z_λ + 0.2 (and > 0.4 for controls matched to the cluster z distribution).

## Statistic
Ratio R = N(behind clusters) / N(blank sky), per annulus, per magnitude bin.
Count slope s = d log10 N / dm measured from the CONTROL counts themselves.
Lensing (any mass that lenses) predicts R = μ^(2.5 s − 1): EXCESS where s > 0.4, DEFICIT where s < 0.4.
Member contamination / bad photo-z predicts EXCESS in every bin, rising inward. Obscuration by members predicts deficit in every bin.

## Decision rules
- LENSING DETECTED: R−1 changes sign across s = 0.4 between bright and faint bins, each side ≥ 2σ (bootstrap over clusters), in the inner annulus.
- CONTAMINATED: excess ≥ 2σ in both steep and shallow bins → not diagnostic for mass; reported as such.
- NULL: |R−1| < 2σ in all bins → no projected mass detected at this depth.
- If detected, the implied μ is converted to κ ≈ (μ−1)/2 (weak-field) and reported as a raw projected-mass statement, NOT compared to any ΛCDM halo.
MUTATE: shuffle cluster positions onto random footprint points → R must return to 1.
κ fitted; cold energy mass required; not theory closed.
