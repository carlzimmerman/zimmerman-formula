# Continuation: phase-gradient stiffness

The first partial local-barrier scan showed that an unstable core can convert
and significantly contaminate a still-tethered surrounding region. It also
stopped when the explicit solver slightly left the phase interval; those
partial trajectories are not accepted as a completed scan. The final solver
uses implicit BDF with an independently checked analytic Hessian and tighter
tolerances. This is a numerical correction, not an outcome threshold change.

Test the positive local energy

    E_gradient = (a0^2 / (2 K)) ell_chi^2 |grad x|^2.

Its energy and force vanish for a uniform endpoint, but it couples the internal
state of neighboring regions. ell_chi is a new common physical length. It is
not assumed equal to the original polarization stiffness length L*. We use a
zero-normal-gradient boundary at the finite halo radius; no environmental or
cosmological boundary value is derived.

First scan endpoint Hessian stability at N=64, beta={20,40}, and
ell_chi={.024,.1,.3,1,3,10,30,100,300} kpc. Cross all four mass/size profiles
with the same f={0,.3,.7,.95,.99}. Record the lowest mass-metric eigenvalue
and the uniform-mode Rayleigh quotient. Negative uniform curvature cannot
be cured by any gradient coefficient.

Select the shortest scanned common length (then smallest beta) with positive
lowest eigenvalue for every f>=.95 case and a negative eigenvalue for every
f<=.3 case. This is an explicitly post-hoc *feasibility* choice, not an
independently predicted parameter or an observed fit. Then run the nonlinear
phase equations at those parameters, including reverse (initially free)
histories. Report all four crossed profiles; never use labels inside the gate.

Refine relevant eigenvalues and trajectories to N=128/256. Fraction changes
over 0.02 fail numerical robustness. Keep energy+receiver tolerance 1e-5.
Assess uniform-path activation barriers and thermal-escape requirements;
these upper-bound possible nucleation barriers, not proven lifetimes.
