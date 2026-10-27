# Focused self-audit

**Primary verdict: incomplete, with the smallest missing implication being a single predicted cold-density solution and baryonic motion that meets all requested observations.** The reduced field action and several conditional obstructions are established below; the target of a complete viable parent is not.

Claim card: explicit Newtonian material-current action in CONTRACT.md, constant coupling and separately declared density-weighted variant. Positive field coefficients, rho_b>0, chi>0, conserved material densities. Growth is a quasistatic EdS subhorizon diagnostic. Circular force assumes stationary cylindrical flow and a local adiabatic mediator with locally constant chi. The radius proof assumes regular spherical static data, attractive gravity, nonnegative baryon density, passive X=0 and phase/polarization boundary conditions. None of these restrictions is optional.

Dependency map:
- Action -> material variations -> reciprocal force and positive kinetic square -> transverse principal block / absence of linear scalar source.
- Quadratic cold energy -> quasistatic S -> declared EdS integration -> amplitude table.
- Cold chemical equilibrium + Poisson + passive chi bound + outward polarization -> radial flux inequalities -> pi ell0 first-zero bound.
- Positive gradient energy -> polarization minimum principle and no improvement in S -> bound persists under stated boundary conditions.

| Obligation | Status | Scope/evidence |
|---|---|---|
| Baryons varied dynamically | Passed | Cartesian material derivative and cylindrical reconstruction; momentum and density variations retained |
| Density-coupling derivative | Passed after corrected general-slope conjecture | Original failure preserved; omission control fails |
| Gravity counted once | Passed | No extra P.grad Phi term; Poisson from the displayed action |
| Homogeneous transverse stability | Passed | Exact characteristic determinant; positive nonzero omega squared |
| Full nonlinear characteristic/constraint system | Not addressed | Homogeneous Hamiltonian squares do not prove it |
| Scalar growth decoupling of new X/chi | Passed at stated perturbative order | curl of a longitudinal velocity zero; phase source quadratic |
| Full cosmological growth | Conditional | Finite P inertia, radiation, dark energy and relativistic reference sector not derived |
| EdS ODE execution | Passed in stated finite cases | RK45 versus DOP853, dust control, convergence below thresholds |
| Radius comparison proof | Passed under claim-card conditions | Monotone test function; centre/boundary terms retained; no use of finite sample as universal proof |
| Surplus versus total cold mass/lensing | Passed in wording | Bound concerns e only; compact mass and exterior polarization not excluded |
| Positive P stiffness extension | Passed under nonnegative boundary polarization | Negative-minimum contradiction; exact Schur sign |
| Positive phase lower bound with gradients | Passed under passive boundary conditions | Minimum principle for -Dchi laplacian chi+mu^2(chi-chi0)>=0 |
| Numerical radial solutions | Conditional finite evidence | Local scalar limit, declared sources/amplitudes; not full Dchi>0 BVP or observed systems |
| Dwarf/cluster masses and formation | Not addressed | No independently fixed inventory, central amplitude, capture or survival |
| Rotation-curve agreement | Not established | Derived correction is generally nonzero; no global disc or sample fit |
| Independent review | Not performed | All reasoning and code review are self-review |

Checks against overreach: the vorticity scalar source uses mean material velocity, not arbitrary stellar random motion; constant-density rotation does not imply every power-law rotation has zero correction; a first zero of h is not automatically a cold-halo surface; compact sources affect lensing outside their support; a finite-z diagnostic is not a general FRW theorem; the original strict tolerance is accompanied by the explicit amplitude sensitivity table.

Control revision: the first checks.py used a reporting-level control for one radial assertion. Before final evidence, the mutation was strengthened to actually omit the restoring density in the radial equations and the reciprocal momentum term in the fluid variation. run2 and mutation are the current pair. Normal equations and normal results did not change. run remains historical with the earlier script hash.

General-slope correction: density_run's additional guessed n(1-p^2) coefficient failed. The correct coefficient is (n-2p)(1-p^2), independently recovered in DENSITY_CORRECTION.md. No tolerance was relaxed; contracted flat/rigid/zero-vorticity predictions were unchanged. density_run2 and density_mutation2 are current supporting evidence.

Prose/math self-proofreading covered new files only. q_a denotes acceleration while q is its dimensionless form; cosmological k is explicitly comoving; chi0 sets ell0 whereas the polarization length belongs to gamma. The source tables are project context, not independently reverified literature. No novel-result priority or formal-proof certification is claimed.
