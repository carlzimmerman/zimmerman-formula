# CFG829 FROZEN CRITERIA: does weak lensing show the dwarfs' +0.44 dex excess at the dwarfs' own accelerations? (before any script)

**Why.** CFG828: the dwarf excess over the galaxy law lives only at g_bar ≲ 10⁻¹² m/s² (21 dwarfs, mean Δ = +0.44 dex),
below SPARC's floor. Either the law's deep regime fails there (LAW-SHAPE), or something acting only on faint satellites
inflates them (tides / external field, binaries, non-equilibrium). KiDS-1000 lensing of ISOLATED galaxies reaches the same
g_bar with none of those satellite effects. Late-type (blue) lenses are the cleanest comparison.

## Data (on disk; Brouwer et al. 2021, B21)
- `real_research/data/lensing_rar/brouwer2021_rar/`: Fig-8 colour bins (bin 1: u−r < 2.5 = blue/late, PRIMARY; bin 2: red),
  Fig-4-5-C1 all isolated (no bins), Fig-10 isolated dwarfs (reported). Column 1 = g_bar (m/s²), g_obs = 4 G ESD_t / bias
  (B21 Eq. 7, README), covariances from the matching covmatrix files with the bias correction applied as the README states.
- B21's own g_bar (stars + its cold-gas estimate); the hot-gas variant is NOT used.

## Law and statistic
- g_law = g_bar ν(g_bar/a0); primary ν(y) = 1/(1 − e^{−√y}) (CFG821–828 kernel); simple-ν bracket; canonical a0 = 9.3603e-11
  (alt 1.1312e-10 reported).
- **Window W = the dwarfs' range: 10^−13.3 ≤ g_bar < 10^−11.9 m/s²** (all B21 points whose g_bar falls inside).
- Amplitude A = best-fit scaling of the law to the data in W with the full covariance: A = (gℓᵀ C⁻¹ gₒ)/(gℓᵀ C⁻¹ gℓ),
  σ_A = (gℓᵀ C⁻¹ gℓ)^−1/2. Δ_lens = log10 A. The dwarf value is A_dw = 10^0.44 = 2.75.

## Classes (primary: blue lenses, primary ν, canonical)
- **LAW HOLDS AT LOW g** if |A − 1| < 2 σ_A AND (A_dw − A) ≥ 3 σ_A: lensing sits on the law where the dwarfs sit above it
  → the dwarf excess is NOT a law-shape failure; it is specific to faint satellites.
- **LAW-SHAPE** if A ≥ 2.0 AND (A − 1) ≥ 3 σ_A: lensing shows a dwarf-like excess.
- **INTERMEDIATE** otherwise (report where A sits between 1 and 2.75).
- NOT DIAGNOSTIC if fewer than 2 B21 points fall in W.
- Report the same for red lenses, all isolated lenses and the B21 isolated-dwarf lenses, and A in the neighbouring
  window 10^−11.9 ≤ g_bar < 10^−10.9 (where SPARC and dwarfs agree, CFG828) as a calibration check.

## Controls
- K1: A in the calibration window [10^−11.9, 10^−10.9) for blue lenses within 3 σ_A of SPARC's +0.04 dex (CFG828).
- MUTATE (separate output): multiply every g_obs by 2.75 → the primary must class LAW-SHAPE.

κ = ½ fitted; cold energy mass required; not theory closed. Lensing is assumed to trace the same g as dynamics (as in
CFG801–805); a relativistic completion could change that, declared.
