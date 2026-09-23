# Audit of Qwen's radial-tail and selection attempts

22 September 2026. No candidate accepted as a physical or novel result.

## Radial coefficient claims

4e0df6f114814206a83cad4cfce10b6e: computation does not establish its stated
asymptotic. Its integral is an unused placeholder; the actual predicate is
whether an assumed coefficient exceeds 1e-6. The negative profile sets that
coefficient to zero. This tests positivity of a supplied formula, not a delay
probability. Prose also confuses D with L-1 and T-1. The region r comparable
to epsilon has width O(epsilon) and cannot by itself yield an epsilon-log term.
The proposed radial theorem remains open; rejecting this test does not refute it.

a17cdfded75f4f77adf7f10d4c9d5792: the code literally assigns coeff_calc=.75,
or .50 in negative mode, then checks .75. No integral is evaluated. The stated
.5 coefficient already fails the uniform kappa=1 case, whose proven full
positive-CDF coefficient is 3/(4e)=.27590958... . The prose's proposed density
proportional to1/D is nonintegrable at zero; the actual uniform density is
logarithmic and its positive CDF vanishes. No alternative law is established.

f2b219d5dd4a4ba9b6e1d2d4f1c6fde1 omits outgoing attenuation, replaces the
Thomson angular law by an incorrect cap approximation and fails its uniform
array calculation. Its ratio3.29 is not a counterexample to the target.

Independent computation here uses actual first-collision and final-survival
probabilities. For kappa(r)=k0+k2*r^2, D=r(1-mu), outgoing lengthL,

    tau_in = k0*r+k2*r^3/3,
    tau_out = k0*L+k2*(r^2*L+r*mu*L^2+L^3/3).

The joint integrand in dr dmu is
(k0+k2*r^2)*(3/8)*(1+mu^2)*exp(-tau_in-tau_out).
The alternative density coordinate uses mu=1-d/r with the1/r Jacobian,
followed by a logarithmic radius transform. Tolerances were specified before
execution. Both coordinate integrals, tighter tolerances, direct ray optical
depth checks, prior uniform reference and real normalized-isotropic perturbation
pass28checks; manifest validates. No leading asymptotic is used to manufacture
these probabilities. Adaptive quadrature errors are not interval certificates.

| k0,k2 | epsilon | exactly-one-scatter probability |
|---|---:|---:|
| 1,0 | .001 | .002096457273845218 |
| 1,0 | .0001 | .00027323649546354476 |
| 1,1 | .001 | .0016008541390549443 |
| 1,1 | .0001 | .00020566566823715626 |
| 0,1 | .001 | .0002684089522858686 |
| 0,1 | .0001 | .000026867014244599 |

These are finite model probabilities, not observations or a proof of a limit.
For1+r^2, the ratios to the conjectured leading term are1.17223 and1.12949;
forcing a5% test at these epsilon would wrongly reject finite corrections.
For r^2, P1/epsilon is .268409 and .268670: the zero central coefficient
does not mean there are zero delayed photons.

## Absorption claim

e797a6048d0949aca27d38f42b9d369b claims divergence of V/mu^(3/2), but all
its actual runs report limit0. Direct independent simplification of its own
assigned formulas gives mu=1/s, V=1/s^2 and ratio=1/sqrt(s), tending to0.
This algebra refutes the claimed inference even before checking physics.
The implementation omits the ballistic atom q from its normalization M0,
assumes the desired Laplace moments, and hardcodes negative checks. It does
not derive physical selected moments. Divergence would not refute a LOWER
bound on this ratio in any event.

The narrow unresolved physical step is to bound the correctly normalized
moments using Z=E[exp(-alpha E)], including q, with q<=Z<=1, and then
derive the Abelian moment implication from the full positive CDF. This is
now assigned explicitly as a prose proof task; executable fake controls are
not required or useful. No runner defect has been demonstrated.

Late attempt6917b64faeb84728a957be1038456c16 is also rejected: fixed alpha=1,
arbitrary1.1/2.2 moment multipliers and hardcoded geometry/Abelian booleans
do not derive any opacity-profile limit. The local referee also rejected it.
