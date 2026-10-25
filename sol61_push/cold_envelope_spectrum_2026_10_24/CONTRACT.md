# CCT-008: necessary stationary envelope spectrum

Test whether nonnegative occupations of bound radial eigenmodes in the target cold+baryonic Newtonian potential can reproduce four previously specified Plummer cold profiles, using common eta=3000 pc km/s. This is a stationary density-matrix / random-phase field extension of the CCT candidate. It is not automatically a stationary single coherent wave: cross terms in a pure field remain an explicit obligation. Equal occupation across m makes the ensemble spherical and zero net spin; large angular momentum dispersion is not net angular momentum storage.

For each l, H_l=-eta² d²/dr²/2+eta² l(l+1)/(2r²)+Phi_c+Phi_b,N. Dirichlet radial boundaries, regular origin. Bound states only. Fit their nonnegative shell masses to cumulative target mass at logarithmic apertures, with relative weights. Target Phi_c is computed from the same target mass once; Xi is excluded from cold dynamics. A good density reconstruction is a necessary approximate self-consistency check, not a formation, stability, capture, stellar-heating or galaxy-data inference result.

Baseline: uniform radial 1536 interior cells, rmax=20 cold scale radii, l<=32, <=20 radial states/l; eta=3000. Refine radial grid and angular cutoff only to test identified sensitivity. Mass beyond rmax and aperture interpolation are disclosed. Target profiles come from CCT-006, not newly fitted data. Draco/Fornax/Leo I are illustrative global-moment profiles; Sextans is the conditional actual-position survey fit.

Numerical checks: radial eigenpair residuals; normalization; nonnegative occupations; compare target-density quantum kinetic lower bound with virial kinetic demand; recover analytic Plummer self-virial and amplitude-gradient kinetic coefficients; report maximum relative aperture discrepancy and potential discrepancy. Finite adequacy threshold: max relative enclosed-mass discrepancy <5% at tested apertures 0.08..12 cold radii, and potential discrepancy <5%. Failure means this finite spectral library did not construct the target, not a universal impossibility proof.

Run single-threaded: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 sol61_push/cold_envelope_spectrum_2026_10_24/spectrum.py --tag baseline

No heavy jobs, frozen inputs, published criteria, automations or external repositories are changed. Memory cap 1GB. Preserve source/input hashes before and after, run parameters, fit arrays and failed fits. No four-dwarf closure is claimed from equilibrium existence.
