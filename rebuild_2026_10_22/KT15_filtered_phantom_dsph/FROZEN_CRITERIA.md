# KT15_filtered_phantom_dsph: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-03: "keep pushing". KT14's filtered QUMOND passed the Milky Way on alt at xi = 2.0 kpc (post hoc, box corners). Its first owed test is dwarf spheroidals, written into KT14's criteria before its result. κ = 1/2 FITTED and held fixed. Footing alt 1.1312e-10 for the filtered arms (where KT14 passed); plain QUMOND on both footings as reference. Never pooled. Not theory closed. No cold component, no particle. No download: McConnachie 2012 (`real_research/data/dsph/mcconnachie2012_dsph.csv`, VizieR extraction on record).

**Not blind.** I've read the table's columns and know the classical dwarfs' rough MOND standing from the literature (Draco and Ursa Minor run high in plain MOND). By hand: universal xi = 2 kpc cuts a dwarf's own boost at r_half by about (r_half/xi)^1.5, so **I expect arm A1 KILLED**. Arm A2's xi is under 0.1 kpc for these dwarfs, so **I expect A2 to track A0**. Reported as found.

## Sample, frozen
Rows with V_mag <= -8 and a listed e_sigma, excluding M32, NGC 147, NGC 185, NGC 205 (compact and dwarf ellipticals, not dSph-like) and Sagittarius (disrupting). No other cut.

## Model
Plummer sphere, a = R2 (projected half-light radius). Mass M = Upsilon_V L_V + 1.33 M_HI, L_V from V_mag with M_V,sun = 4.83. Field: g(r) = g_N(r) + (nu(sqrt(g_e^2 + gh^2)/a0) - 1) gh(r), where gh is the Newtonian field of rho smoothed by a 3D Gaussian of sigma xi (gh = g_N at xi = 0); simple nu, the board law's. Spherical, with the external field entering only through nu's argument (the usual 1D approximation, labelled). Prediction: global sigma_los^2 = (1/3M) integral rho r g 4 pi r^2 dr (virial, no anisotropy assumption).
- **Isolated:** g_e = 0, all rows.
- **EFE:** MW satellites only, g_e = (200 km/s)^2 / D; M31 and field rows isolated.

## Arms
- **A0:** xi = 0, plain QUMOND, both footings, isolated and EFE. Reference.
- **A1:** xi = 2.0 kpc universal, alt.
- **A2:** xi = eps r_M with r_M = sqrt(G M / a0), eps frozen from the Milky Way: M_b,MW = 7.0e10 Msun (KT14's passing M* 5.8-6.1e10 plus about 1.2e10 gas, rounded), so eps = 2.0 kpc / r_M,MW at alt's a0. The dwarf's r_M uses its own M at each Upsilon. Alt.

## Gate, per dwarf, per arm and field case
PASS if some Upsilon_V in [1, 3] gives |sigma_pred - sigma_obs| <= 2 e_sigma. Counts reported, plus the Upsilon each passing dwarf needs.

## Labels, per arm (EFE case primary, isolated beside)
- **KILLED BY DSPH:** pass count at most half of A0-alt's.
- **SURVIVES DSPH:** pass count at least A0-alt's minus 2.
- **HURT:** between.
A2 surviving would be a lead for a size-scaled filter, still owed SPARC, wide binaries (xi for a solar-mass binary about 1500 AU at this eps), Cassini and lensing. It would also be post hoc: eps came from one galaxy.

## Checks
C1: A0 isolated on a very diffuse Plummer (M 1e6, a 2 kpc) against the deep-MOND estimator sigma^4 = (4/81) G M a0, within 3 percent. C2: smoothing conserves mass to 1e-3. C3: a Gaussian of width w smoothed gives width sqrt(w^2 + xi^2), 1e-3. MUTATE: nu = 1 (Newton) on A0; separate `_MUTATE` output, exit 1. Expected to fail most rows.

Register row after the result. Seconds to minutes, single thread.
