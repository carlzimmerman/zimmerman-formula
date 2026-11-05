# Exact static branch of the single-clock candidate

Continuation: derive own-action sourced equations, not transfer v3s results.
Freeze before symbolic checks. No numerical fit, no new normalization input.
Restrict V=constant for the exact static ansatz phi=q t, q>0, so scalar
shift symmetry makes its static equation automatically satisfied for zero
radial scalar current. This ansatz does not describe general V(phi), a
cosmological matching solution, or a nonlinear stability test.

Metric ds^2=-N(r)^2 dt^2+B(r)^2 dr^2+r^2 dOmega^2, N,B>0.
Radial polarization P^r=p/(K B), 0<p<a0(N), a0^2=b[q^2/(2N^2)+V].
Extrinsic curvature of the phi leaves is zero. Their intrinsic curvature is
R3=2/r^2[1-1/B^2+2r B'/B^3], and D.P=(p'+2p/r)/(K B).

Check the first-derivative radial Einstein action by explicit integration
by parts. Differentiate the full reduced density with respect to N,B,p.
Verify GR Schwarzschild and vacuum de Sitter when q,p vanish, taking the
uncharged equations after variation. Verify polarization unscreened limit
and the density-portal lapse source sign. Canonical energy in the lapse
equation must be q^2/(2N^2)+V; portal contribution must include N W_N.
Use exact symbolic checks, no fixture scan or full boundary solve in this step.

Mutation omits N W_N from the lapse equation and must fail the independently
differentiated Euler-Lagrange identity for q,p,b>0. Separate result and exit1.
This step establishes a set of equations and benchmarks only, not existence,
stability or phenomenological viability of their charged solutions.
