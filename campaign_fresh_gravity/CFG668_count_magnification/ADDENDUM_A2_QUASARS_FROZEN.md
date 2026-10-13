# CFG668 addendum A2 — quasars behind clusters (FROZEN, committed before any quasar catalogue is downloaded)

Why: galaxy counts (SDSS, KiDS, DES; 33ff902b3, 3698e6452) could not separate lensing from member leakage, and the faint galaxies
sat at slope s ≈ 0.4, where magnification changes nothing. Quasars at z_Q > z_cl + 0.5 cannot be cluster members, and quasar counts
are steep at the bright end and flatten at the faint end, so they can show the sign flip.

## Data (raw; no cosmology; angular apertures only)
- Quaia G < 20.0 (Storey-Fisher+2024, VizieR J/ApJ/964/69/quaiag200): Gaia + unWISE selection, space-based, no fibre collisions.
- SDSS DR16Q (Lyke+2020, VizieR VII/289): spectroscopic quasars.
- Clusters: SDSS redMaPPer DR8, λ ≥ 20, 0.1 ≤ z_λ ≤ 0.6. Background: z_Q > z_λ + 0.5.
- Blank fields: 3 per cluster, offset 1–3° (seed 668), no λ≥20 cluster within 15'.
- Footprint cut (same for clusters and blanks, per catalogue): number of quasars (all z) within 30' of the point ≥ 0.5 × the blank median.
- Annuli: 0–1', 1–2', 2–4'. PRIMARY aperture: Quaia 0–4'; DR16Q 1–4' (inside 1' SDSS fibre collisions with cluster galaxies bias low).
- Magnitude bins: Quaia G 17–19.0, 19.0–19.6, 19.6–20.0; DR16Q PSF i < 19.5, 19.5–20.5, 20.5–22. Slope s = dlog10N/dm from blanks.

## Statistic
R = mean count per cluster / mean count per blank field; errors by bootstrap over pointings. Lensing: R = μ^(2.5s−1).

## Decision rules
- LENSING DETECTED: the steepest bin (s > 0.4) in the primary aperture shows an excess at ≥ 3σ in the inverse-variance combination of
  the two catalogues, each catalogue with R > 1 in that bin, AND the bins are ordered as lensing demands (R lower where s is lower).
  STRONG FORM: in addition, a bin with s < 0.4 shows a deficit at ≥ 2σ.
- WRONG SIGN: a deficit at ≥ 3σ in the steepest bin → no lensing mass detected; reported as a fail of 'cold energy lenses'.
- NULL: no bin departs at ≥ 2σ.
- If detected: implied μ = R^(1/(2.5s−1)) and κ ≈ (μ−1)/2 reported as raw projected mass along cluster sightlines; no ΛCDM halo used.
MUTATE: blanks split in half, one half plays clusters → R must be 1.
κ fitted; cold energy mass required; not theory closed.
