# Zero-free-parameter prediction of the Pantheon+ Hubble diagram from galaxies

`predict_diagram.py` -> `predict_diagram_results.json` + `predict_diagram_fig.png`.
Data: `pantheonplus_full.dat` (PantheonPlusSH0ES DataRelease, 1701 SNe; 1580 in the
cosmology sample = non-calibrator, z>0.01), binned into 24 inverse-variance points.

## What is (and is not) being tested

Carl Zimmerman's de Sitter-Unruh **modified-inertia** framework **does not modify the
cosmological background**. `a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z` modifies galaxy
inertia, not expansion; Lambda is a genuine constant, so `H(z) = H0 sqrt(Om(1+z)^3+OL)`
and `mu(z)` are **standard flat LCDM**. There is no framework-native SNe formula. The only
thing the framework contributes to the diagram is a **galaxy-side value of Lambda** (hence
`Omega_Lambda`), which we here propagate INTO the SNe diagram and confront with the data.

Pipeline (per footing, per H0):
`a0 -> Lambda = 32 pi a0^2/c^4 -> Omega_Lambda = Lambda c^2/(3 H0^2)` (this depends on H0)
`-> flat mu(z)` with **Omega_Lambda FIXED by galaxies** (not fit) and **Omega_m fixed at
the SNe value 0.334** `-> ` one vertical offset (the H0/M_B degeneracy SNe cannot break)
marginalized analytically `-> ` chi2/dof and Delta-chi2 vs the best-fit flat LCDM
(Omega_m fit freely to the same binned data).

**Zero SNe-fitted shape parameters.** The one nuisance (offset) is marginalized; the
deceleration is set entirely by the galaxy Omega_Lambda + the shared Omega_m.

**Honest scope.** The galaxy model shares Omega_m and the offset with LCDM, so this is a
test of **Omega_Lambda-from-galaxies only**, not of the whole diagram. Errors are the
Pantheon+ **diagonal** errors, so absolute chi2 is optimistic (systematics are correlated;
the full covariance would loosen every chi2). **Use the RELATIVE Delta-chi2 ordering, not
the absolute magnitude.** The flat luminosity-distance form is used as instructed even when
`Om+OL != 1`; a genuinely curved `d_L` would partly compensate the largest offsets, so the
big Delta-chi2 values below are upper-bound-flavoured, not a clean sigma count.

## Results

Best-fit flat LCDM on the binned data: **Om = 0.350, chi2/dof = 0.956**. Reference flat
LCDM held at the SNe Om = 0.334 (OL = 0.666): chi2/dof = 0.941. Both are good fits -- the
binned diagram is standard-LCDM-concordant, as expected.

| footing (a0)                    | rho_DE (kg/m^3) | H0    | Omega_Lambda(gal) | Om+OL | chi2/dof | dChi2 vs LCDM |
|---------------------------------|-----------------|-------|-------------------|-------|----------|---------------|
| **measured GLS** 1.181e-10 *(genuine)* | 9.308e-27 | 67.4 | 1.091 | 1.425 | 2.716 | **+41.4** |
|                                 |                 | 73.0 | 0.930 | 1.264 | 1.859 | **+21.7** |
| **measured median** 9.726e-11   | 6.307e-27       | 67.4 | 0.739 | 1.073 | 1.090 | +4.0 |
|                                 |                 | 73.0 | 0.630 | 0.964 | 0.915 | +0.0 |
| canonical 9.355e-11 *(CIRCULAR)*| 5.836e-27       | 67.4 | 0.684 | 1.018 | 0.967 | +1.2 |
|                                 |                 | 73.0 | 0.583 | 0.917 | 0.942 | +0.6 |
| alt 1.131e-10                   | 8.523e-27       | 67.4 | 0.999 | 1.333 | 2.213 | +29.9 |
|                                 |                 | 73.0 | 0.851 | 1.185 | 1.495 | +13.4 |

## Reading

- **The verdict is footing- and H0-dependent.**
  - **Measured MEDIAN a0** predicts a diagram *consistent* with the SNe data:
    Delta-chi2 = +4.0 (H0=67.4) and +0.0 (H0=73.0). This is a genuine, Lambda-blind
    galaxy input landing on the SNe diagram with essentially no penalty at SH0ES H0.
  - **Measured GLS a0** predicts *too much* dark energy (OL_gal = 1.09 / 0.93): Delta-chi2
    = +41.4 / +21.7 -- in tension with the SNe diagram. This is the same story as the
    density-ratio lane (GLS gives rho_DE ~1.4-1.6x the SNe value, +1.0 to +1.5 sigma);
    the diagram amplifies it because a nearly-closed Om+OL=1.42 geometry forced through the
    flat-form d_L and scored on optimistic diagonal errors is punished hard.
  - **canonical a0 fits almost perfectly (Delta-chi2 ~ +1), but this is CIRCULAR**: the
    canonical a0 = cH_Lambda/Z was DEFINED from a cosmological (Planck) Lambda, so
    "canonical a0 -> Omega_Lambda ~ 0.68" is Planck's Lambda re-inserted, i.e. algebra run
    backwards. Its good fit re-checks Planck-vs-SNe Lambda, NOT the framework.

- **The genuine cross-check** is the *measured* a0 (SPARC rotation-curve dynamics alone,
  Lambda-blind). It lands between "consistent" (median, at SH0ES H0) and "mild tension"
  (GLS, at Planck H0), i.e. the galaxy-inferred Lambda is the right order and within a
  factor ~1.0-1.6 of the SNe/Planck Lambda -- an **independent cross-corroboration at the
  factor level, not a precision match, and not a null.** Consistent with the banked
  "1.1-1.6x" a0-line result.

## Caveats (do not oversell)

- Diagonal errors only -> absolute chi2 optimistic; full Pantheon+ covariance would shrink
  every Delta-chi2. The GLS "+41" is not a clean ~6-sigma kill.
- Flat-form d_L used with Om+OL != 1 as instructed; curvature would soften the extreme
  offsets. This lane isolates Omega_Lambda-from-galaxies, sharing Om + offset with LCDM.
- No "proves". The framework background IS LCDM; rho_DE-from-SNe is the standard extraction.
  The framework adds only the galaxy-side Lambda cross-check computed here.

Credit: Milgrom (a0 kernel); Brout+2022 / Scolnic (Pantheon+SH0ES); Perlmutter, Riess,
Schmidt (acceleration discovery); Sarkar (the SNe-leg critique this is relevant to).
