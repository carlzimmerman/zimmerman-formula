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
must be justified as second-class in G4), higher_derivative (MUST name its Ostrogradsky evasion —
degeneracy condition / constraint — in claimed_mechanism).
GEOMETRY: a SECOND field of type "metric" is allowed (bimetric/Hassan-Rosen family). Declare which
metric matter couples to via top-level "matter_metric": "g" (default) | "f" | "composite". The known
bimetric price (ghost-free HR => linear Yukawa = anti-MOND) must be addressed in claimed_mechanism:
say HOW the acceleration scale a0 arises (nonlinear helicity-0 sector, composite coupling, ...).
FROZEN: mu=1-e^-y; single metric; matter minimal; a0=9.3619e-11 (kappa=1/2 FITTED).
FORBIDDEN combos (auto-G0-kill): unscreened preferred_frame coupling; lapse_weighted MOND; temporal
nonlocality on main branches; kinetic_normalization_source=screened_coupling with a degenerate field.

BIMETRIC CANDIDATES MUST also declare top-level "bimetric_spec": {"interaction":
"hassan_rosen"|"composite"|"other", "matter_metric": "g"|"f"|"composite", "mond_source":
"linear_massive_graviton"|"nonlinear_helicity0"|"composite_matter"|"f_sector", "m_FP": "~H0"|"other"}.
Auto-kills: linear_massive_graviton (Yukawa != mu, the ghost-free-XOR-MOND fork); interaction "other"
without argued degeneracy (BD ghost); matter sourcing the 2nd metric without a declared matter_metric
(doubly-coupled ghost); claiming a massive graviton with no declared interaction potential.

RELATIVE-CONNECTION (extended BIMOND, Milgrom 0912.0790 + 2022 ext) tokens for couplings.sources:
  C_tensor (=Gamma(g)-Gamma(h)), C_invariant_1..n (independent quadratic C-scalars).
Declare via bimetric_spec.interaction="bimond_connection" + mond_source="connection_invariants".
KNOWN WALL: derivative bimetric interactions are GENERICALLY ghosty; the decisive gate is the
Hamiltonian/BD audit (escalated, A-P ladder D/E). The MOND nonrelativistic limit and lensing slip
come from the C-invariants; several invariants share the same NR limit but differ relativistically.
