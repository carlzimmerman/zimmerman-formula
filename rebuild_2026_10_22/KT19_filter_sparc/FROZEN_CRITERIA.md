# KT19_filter_sparc: FROZEN CRITERIA, committed with KT18 and KT20's criteria, before any of their scripts or numbers

Owner, 2026-11-03: "run one after another". KT17's filtered QUMOND (phantom sourced by mass smoothed over xi = 0.55 sqrt(G M_b / a0)) passed the Milky Way, dwarfs and Cassini. Its main open risk is SPARC: a 1e10 Msun galaxy gets xi of about 1.9 kpc, so inner points may lose boost. κ = 1/2 FITTED, held fixed. Both footings, never pooled. Not theory closed. No download.

**Not blind:** I know the board law's SPARC fit is good, and that the inner points of small discs are where the risk sits. I don't know the size of the change. No expectation beyond "inner residuals go negative".

## Model (approximation stated)
Per galaxy: g_bar(R) = V_bar^2 / R from SPARC's rotmod, V_bar^2 = V_gas|V_gas| + 0.5 V_disk|V_disk| + 0.7 V_bul|V_bul|. **Spherical smoothing approximation:** enclosed mass M(r) = V_bar^2 r / G at the data radii (made monotone by running maximum), interpolated in r with M(0) = 0; beyond the last point, the remaining mass M_b - M_last (if positive) in an exponential tail with the table's R_disk. rho = dM/dr / (4 pi r^2), smoothed by a 3D Gaussian of sigma xi, giving gh(R). Model: g = g_bar + (nu(gh / a0) - 1) gh, simple nu. At xi = 0, gh = g_bar exactly at the data radii, so the model reduces to the board law; only the smoothing is approximate.
M_b = 0.5 L[3.6] + 1.33 M_HI from the table (bulge light at the disc's Upsilon, a small error in xi only). xi = 0.55 sqrt(G M_b / a0).

## Statistic and gate
Points with V_obs > 0, e_V/V_obs < 0.1, g_bar > 0; galaxies with at least 3 points (KT7's cuts). Residual log g_obs - log g_model; galaxy-equal rms and median, as KT11. Inner points: R < 2 R_disk, reported separately (median residual).
- **SURVIVES SPARC:** rms rises by at most 0.005 dex over xi = 0 and |median| <= 0.05.
- **HURT:** rms rises by 0.005 to 0.02, median within 0.05.
- **FAILS SPARC:** rms rises by more than 0.02, or |median| > 0.05.
Beside it, no label: one global stellar scale f fitted for both xi = 0 and the filter (so a pure Upsilon shift isn't read as a failure); the f each wants.

## Checks
C1: xi = 0 reproduces the board law's per-point prediction (nu(g_bar/a0) g_bar), 1e-10. C2: smoothing conserves mass to 1e-3 on three galaxies (smallest, median, largest M_b). C3: monotone M(r) changed at most 5 percent of points (reported). MUTATE: nu = 1 must give the Newtonian rms (large); separate output, exit 1.
