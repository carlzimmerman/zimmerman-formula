# ARCHITECTURE GRAMMAR (machine-readable candidate space)
Candidates are json objects (see prompts/architect.md for the exact schema). Ingredient tokens usable
in couplings.sources:
  metric: R, R_munu, R3, R3_ij_TF, spatial_einstein, weyl_E
  foliation (only on screened-PF / khronon branches): khronon_T, u_mu, a_mu(accel), K_ij, theta
  MOND: y, mu(y), chi(aux-Legendre), P_i=mu*DPhi (constitutive momentum), D(iPj)_TF, q=-1/6 ln det(gamma)
  auxiliary: chi_scalar, Q_stf, multiplier
  nonlocal (spatial only on main branches): inv_laplacian, elliptic_kernel_f(D2/a0^2)
  matter: rho (minimal coupling only)
Kinetic options per field: none (auxiliary/algebraic), standard, degenerate (det H=0 by design —
must be justified as second-class in G4).
FROZEN: mu=1-e^-y; single metric; matter minimal; a0=9.3619e-11 (kappa=1/2 FITTED).
FORBIDDEN combos (auto-G0-kill): unscreened preferred_frame coupling; lapse_weighted MOND; temporal
nonlocality on main branches; kinetic_normalization_source=screened_coupling with a degenerate field.
