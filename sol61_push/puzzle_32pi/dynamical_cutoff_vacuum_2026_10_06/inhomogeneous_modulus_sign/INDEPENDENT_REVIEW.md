# Independent fixed-invariant and inhomogeneous modulus audit

Accepted as a necessary-equation obstruction for this explicit UV-normalized canonical completion. Spatial inhomogeneity and stationary shifts cannot stabilize a finite modulus on a compact stationary no-flux slice. The result does not prove an admitted full-field evolution or impose a universal selector restriction on different completions.

Inspected at HEAD `42ac8fadd721cdc921aa382431f9c91582b52eaf`: frozen REPORT SHA256 `213a99f313801011bf9ac77ca00aa03b0058c090a4039372e5d5d08902286d3f`; checks `16c0a42a9e9f71393ca0256d5d4b12890ef82e6e93266b8bb0cd0c41ecb52bae`; contract `3ddd5b46c863b0d633a3194b4a9203f2eb7419132b5b47eb96fd1896d21a9f9b`. The actual parent action was read directly, parent REPORT SHA `1860ae1e3ce34b1fe42c3c3937ba0e9ee086537a82e4ac97082ffb9587e3fff4`. No author inputs were modified.

## Fixed-invariant chain reconstructed

The independent modulus is u=lnT; the normalized foliation clock is a different field. At fixed metrics/clock, I has no explicit u dependence. For the admitted local source branch, q_y=2d and x_y=1+2d_y imply M_y=2d x_y. At fixed x=sqrt(I), x_T=2d_T gives y_T=−2d_T/x_y. Thus the entire 4d d_T term from differentiating 2d² is canceled by M_y y_T; the result is M_T|I=q_T−A_T. No Newtonian identification of a generic nonspherical local invariant is needed for this algebra.

Directly differentiating e=b(t)T²/(T²+t²) gives e_T=2T t²b(t)/(T²+t²)²>0. Consequently

M_u|I=−4T² integral_y^infinity t³b(t)/(T²+t²)² dt<0.

At infinity b(t)~1/(2t), so the integrand is ~1/(2t²). Near zero it is proportional to t^(5/2) for fixed T>0, and is also integrable. Differentiation of q and A is legitimate at each finite positive T on compact T intervals with these dominating endpoint estimates. At y=0 the continuous endpoint is −A_u; finite y never makes the tail vanish. A fold without an admitted differentiable local branch is excluded. In addition y<=x, since x=y+2d and d>=0; finite bounded invariant does not secretly require an unbounded y on the branch.

The UV subtraction is load-bearing. M(infinity,T)=0 requires the field-dependent A(T); replacing it by a fixed constant changes the action and leaves M_u=Tq_T>=0 instead, with a degenerate vacuum derivative at y=0. That is an alternative premise, not cancellation of the retained force by a spatial pattern. Added modulus potentials or explicit kinetic/matter couplings are likewise outside this theorem.

## Both ADM currents and orientation

Varying the actual kinetic action gives J^mu=(f²/2)(sqrt(−g)g^{mu nu}+sqrt(−ghat)ghat^{mu nu})u_nu and E_u=partial_mu J^mu+2K chi_n a0²v M_u=0. Thus partial_mu J^mu=F>0, with F=−2K chi_n a0²v M_u.

Independently inverting the ADM form ds²=−N²dt²+gamma_ij(dx^i+S^i dt)(dx^j+S^j dt) gives g00=−1/N², g0i=S^i/N² and gij=gamma^ij−S^iS^j/N². Contracting with u derivatives gives

J0_g=−(f²/2)sqrt(gamma)(udot−S·grad u)/N,
Ji_g=(f²/2)[N sqrt(gamma)gamma^ij u_j+sqrt(gamma)S^i(udot−S·grad u)/N],

with the same independent expression for L,R,hatgamma. The shifted spatial term has the positive sign reported. At udot=0 it contains gamma^ij−S^iS^j/N²; positivity of that stationary spatial form is not required for the integrated proof. Dropping the shifts from the canonical current would be incorrect even though the projected invariant itself is shift independent in this foliation.

The actual canonical momentum is pi_u=−J0, so Q=−integral J0 is the integrated momentum, not cold number or a conserved shift charge. With no boundary flux, Qdot=−integral F<0. Its units are action in c=1, and chi_n>0 for every n>=3. In the coincident homogeneous limit Q=f²a^n udot and Qdot=−a^n V_u, agreeing with the independently varied parent scalar equation. This also checks the two-sector factor f²/2 and the sign.

## Compact theorem and precise exceptions

For stationary fields/current coefficients on a compact periodic slice, J0 is time independent and integral div Ji=0. The Euler equation would require 0=integral F>0. Finite positive T and nonsingular positive metric volumes on the compact slice make the strict positive integral well-defined; no lapse equality or spatial ellipticity assumption is inserted. A constant modulus has zero current pointwise and cannot satisfy the equation on any admitted finite-invariant geometry. The stronger zero-shift statement for coordinate-stationary u remains true even with time-dependent metric coefficients because J0 itself is then zero.

For evolving fields the strict momentum identity does not imply monotonicity of average u or T: the weights and shift advection are dynamical. It does forbid an exact recurrence of all current-defining fields on the same compact no-flux foliation. No global regularity, positive-energy or stable-attractor theorem follows.

For a boundary, direct integration yields Qdot=−integral F+integral_boundary Ji n_i. A stationary solution therefore needs a positive outward current flux equal to its positive bulk source. Boundary-forced solutions are not excluded. In the noncompact exception stated in the report, asymptotically constant nondegenerate stationary coefficients, I→0 and finite u_infinity give F→F_infinity>0. The bulk integral grows as F_infinity Omega_(n−1)r^n/n; the additional uniform assumption grad u=o(r) gives surface current o(r^n), a contradiction. This is exactly a conditional asymptotic gate. Horizons, degenerate coefficients, boundary flux, nonconstant asymptotics, T→0 or an undefined branch do not satisfy it and are not covered.

## Current computation evidence

Independently validated all four current manifests: main_a 36/36 and the three declared controls 36/37 each. The direct ADM inverse identity and independent tail substitutions are consistent with the raw derivation. The smooth periodic numerical fixture has arbitrary prescribed metrics, shifts and modulus; it is explicitly not an Einstein/clock solution. Its residual only illustrates why a positive source cannot be balanced by an integrated periodic divergence. The analytic proof does not depend on that fixture, its sample count or the check count.

No blocking correction remains. This closes a genuine inhomogeneous stationary route for the declared canonical UV-normalized field. It does not identify dark matter, derive a vacuum coefficient, prove full covariant evolution, or exclude modified stabilizers and boundary mechanisms.
