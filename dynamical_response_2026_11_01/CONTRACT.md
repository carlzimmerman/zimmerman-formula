# DR01: finite-halo kinetic quadrupole response

The user authorized the proposed dynamical-response calculation and publication
on 2026-11-01. This contract is written before scientific execution. FR01 input
snapshots are immutable. Only this new directory belongs to this task.

## Question and actual finite assertion

Does the specified PN28 canonical field distribution have a self-consistent
linear response to finite rotating quadrupole forcing, including its own
gravity, reciprocal scalar response and canonical-current feedback? Compute
the response and energy/angular-momentum transfer on the FR01 pc=.2,
epsilon=.01 baseline and its existing fixed-mass compact-baryon endpoint.
The diffuse endpoint is a control if both primary cases finish and validate.

Use the controlled limit F²→0 at fixed Cs=F² c_chi² and finite forcing
frequency. The scalar solves its spatial elliptic equation at each instant.
This is a declared singular limit of the parent, not a selected finite speed,
an ordinary-gravity tracer model, a fluid closure, or a radiation calculation.
Retain (1−exp(−2s)) p·δj/n in the single-stream Hamiltonian. Empty-space
kinetic transport is not needed for this linear occupied-shell calculation;
this does not supply nonlinear moving-vacuum evolution.

Use energy-shell action quadrature and orbital Fourier modes, and variational
radial bases for Poisson, scalar and current feedback. Keep frozen orbital
zero modes unexcited. Positive finite Hamiltonian curvature permits a stable
finite response; it is not a continuum stability proof. A negative curvature
alone is not a growing-mode proof. If the finite Hamiltonian is indefinite,
record that gate and do not reinterpret it as absorption by a stable state.

## Fixed experiment choices

- Units: FR01 ell, h_star and t_star=ell/sqrt(h_star). Report frequencies in
  each state's sqrt(M_total(<R)/R³); these are diagnostics, not measured bars.
- Forcing radial profile U=(r/a)²/[1+(r/a)²]^(5/2), normalized to max=1,
  a=.3 times the original baseline radius. Multiply normalized Y_22 and take
  the real part. Amplitude A=1e-3 times baseline central psi is a formal
  linear-response normalization. Changing A scales response and work exactly;
  no finite-amplitude nonlinear validity is claimed.
- Pattern frequencies Omega_p/omega_dyn = .25,.5,1,2,4. A sin² envelope lasts
  T=20/omega_dyn, followed by observation through 2T. No artificial damping.
- Initial resolution ladder: (L quadrature, orbit phases, radial harmonics,
  radial basis count)=(16,256,12,6),(24,512,18,8),(40,1024,24,10).
  Additional isolated refinements only to discriminate a named error.
- Scalar basis includes exterior decay; gravity uses exact l=2 vacuum tail.
  Do not reuse FR01's l=0 scalar boundary condition.
- Bounds: each recorded execution <=1800 seconds, <=1 thread; retain failed
  attempts. No installed packages, physical parameter tuning, new galaxy fits,
  modified FR01 result or shared branch change.

## Controls and interpretation

Require independent orbit-period/invariant controls, shell measure and spatial
Gram sum rules, l=2 angular factors, canonical-current inclusion, positive
finite Hamiltonian (where claimed), causal zero initial state, and pulse work
matching final perturbation energy. Check torque plus envelope work against
the rotating-pattern identity; compare independent resolution changes and
finite-duration bare response. Quantify Krylov/time-quadrature errors.
Target <=1% in significant integrated work on the final two resolutions;
failures are reported as unresolved convergence, not physical exclusion.

The local forcing work inside the radius containing FR01's original core mass
can be measured, but is not the net heat retained there: transport and field
energy cross that surface. The l=2 linear calculation cannot by itself predict
a second-order spherical core expansion or reversal of the 31.4% contraction.
Positive work can reside in coherent modes. No permanent heating, selected
stellar reservoir, continuum damping coefficient, universal acceleration,
galaxy fit, cluster fit, microscopic potential selection or formation claim.

Possible outcomes: validated finite transfer with self-consistent feedback;
negligible response in the stated forcing band; finite stability obstruction;
or numerical/resource inconclusiveness. Every outcome is conditional on the
parent, waterbag state and fast-scalar limit. Publish code, exact finite scope,
raw outputs, failed runs, manifests, review and a reproducible command.
