# Stiffness origin: bounded research contract

Owner: stiffness_origin subagent. Base checkpoint: `431f22bd6fe998759b843d13113762d73356aec6`.
Local research date: 2026-10-20. Write scope: this directory only. No other current lane reports are inputs.

Target: derive the coefficient `gamma = (4 pi G) Lstar^2 / 2` of the frozen S2 action from a specified mechanism with independently fixed microscopic inputs. Merely fitting a new parameter or matching a numerically selected product of constants is not success. Finite response calculations, explicit matching conditions, and scoped obstructions are partial progress.

Fixed conventions: `u = K |P|`, `K = 4 pi G`, `K Wrem'(u) = u^2/(a0-u)`, `0 <= u < a0`. Canonical and alternate a0 are separate (9.3603e-11 and 1.1312e-10 m/s^2). S3's density interpretation is used only when explicitly assumed. Spatial Fourier k is angular wavenumber, so a wavelength is `2 pi/k`; an inverse wavenumber is `1/k`.

Constraint provenance is read, not re-scored: CFG820 gives the primary globular lower edges 24.0/24.7 pc; CFG821's <=22 pc result already has a bad unscreened fit and is not a clean independent stiffness upper edge; PARAMRED C_LSTAR gives a soft 2042/2138 pc SPARC upper edge, not a confidence bound, under point-source screening. The requested 24 pc–1 kpc window is a benchmark, not an exact allowed interval.

Routes fixed before new numerical execution:

1. Positive isotropic finite-range alignment energy of P. Compute its exact Fourier symbol and low-k coefficient. Success requires independent interaction range and strength plus validity across tested scales. Discriminator: derivative expansion at fixed `k ell`; a positive kernel must produce positive gamma and remain consistent with required high-k response.
2. Compressibility of a cold mass continuum, with an explicit contact-interacting boson realization. Derive the required equation of state, tensor-sector scope, and mass/coupling relation. Success requires parameters predicted outside stiffness data and a bridge to S2; the Jeans balance of an ordinary gravitating fluid is a comparison, not an assumed S2 mode.
3. Quantum gradient energy of a density condensate. Derive its operator under `delta rho = div P`, compare powers of k, and compute conditional Jeans/healing scales. Success requires the actual S2 k^2 operator rather than one matched wavelength.

Shared finite checks: exact derivatives of W; gravitational Schur complement; independent Cartesian finite-difference Hessians for six backgrounds; eigenvalues at seven backgrounds and 13 directions; exact contact-EOS and Fourier identities; kernel expansion and negative-sign mutation; density/length parameter inversions; k^4 versus k^2 mismatch over seven wavenumbers and a mutation that intentionally erases the k power. These checks do not establish microscopic existence, cosmological viability, or observational fits.

No exponents, numerical constants, coupling values, or new scale products will be searched to land inside the window. Inversions of the window into necessary microscopic parameters are explicitly labeled requirements, not predictions. The conventional illustrative relativistic coupling value 1 and reference particle mass 1e-22 eV/c^2 are benchmarks only.
