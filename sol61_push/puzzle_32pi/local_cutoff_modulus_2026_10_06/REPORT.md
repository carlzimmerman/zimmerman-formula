# A local cutoff modulus responds to sources but does not select the vacuum

Base checkpoint: 1288c215ccf61b97e0ae2c5a2dfb0c53a8a5e02b. This executes the local-field continuation left open by the sourced variational test, using Claude's actual p35 cutoff. It is a new nonrelativistic action diagnostic, not an asserted covariant completion or a derived 32pi principle.

## Action and dimensions before specialization

Let n=d−1≥3 spatial dimensions, S be the area of the unit (n−1)-sphere, and normalize G_n by ΔPhi_N=S G_n rho. Then g_N=G_n M/r^(n−1), and [G_n]=L^n/(mass time²). Take dimensionless cutoff T>0 and

L=−[2 gradPhi·gradPhi_N−a0² Q(z,T)]/(2S G_n)−rho Phi−Z|gradT|²/2−V(T),

z=|gradPhi_N|²/a0², Q(y²,T)=y²+q(y,T),
q(y,T)=2 integral_0^y t chi_T(t)dt,
chi_T(y)=(sqrt(1+1/y)−1)/(1+(y/T)²).

Here [a0]=L/time², [V]=energy/L^n and [Z]=energy/L^(n−2). All terms are energy densities. T is dimensionless; a finite Z supplies a new length scale through V''/Z. No hbar occurs. The n=3 normalization is the actual QUMOND action 1/(8piG), authenticated in the frozen parent SOURCE_REVIEW and independently checked by root against arXiv:0911.5464v2 equations (3)–(6). A preferred-frame static stiffness alone proves no relativistic causal or propagating health claim.

Vary all three fields, with fixed source and admissible fixed boundary data:

ΔPhi_N=S G_n rho,
ΔPhi=div[nu(y,T) gradPhi_N],  nu=1+chi_T,
−Z ΔT+V'(T)=a0² q_T(y,T)/(2S G_n).

The physical force remains −gradPhi. In particular the second equation includes spatial gradients of T through the divergence. Treating it as a fixed-kernel Poisson equation after solving T would omit source reaction. The Newtonian field and y are independent of T in this NR two-potential model, making the modulus equation a concrete rather than phenomenological test.

## Universal constant cutoff obstruction

q_T(y,T)=2 integral_0^y t partial_T chi_T(t)dt>0 for every y>0,T>0. In source-free zero-field vacuum, any constant cutoff T0 satisfies V'(T0)=0. The same constant cannot solve the modulus equation in a region with y>0: its left side remains zero while its right side is positive. Thus a dynamical local cutoff cannot remain exactly equal to its vacuum minimum around an ordinary source in this declared action. A boundary condition, large stiffness or large mass can make the change small, but does not derive the minimum's value.

Take the explicit bounded-below potential V=V0+Z m²(T−T0)²/2, with m>0. Wherever a solution with positive T exists, any negative interior minimum of T−T0 contradicts the modulus equation. With T→T0 at infinity (or fixed T0 boundary), its response is nonnegative; nontrivial sources make it nonconstant. This is a maximum-principle sign argument, not a proof of existence or uniqueness of the full nonlinear coupled boundary problem.

At fixed m, large Z gives the controlled formal leading response

(−Δ+m²) deltaT=J(x)/Z+O(Z^−2),
J=a0² q_T(y,T0)/(2S G_n)>0.

For n=3 the Green function is exp(−m|x−x'|)/(4pi|x−x'|), so the leading convolution is positive. In a smooth-source setting this is an ordinary elliptic linear response. The stiffness expansion must remain small relative to T0; no arbitrary finite Z nonlinear existence is claimed.

## A massive modulus still has an algebraic far-field tail

The gravitational source for T is not confined to the baryonic body. At small y,

partial_T chi_T(y)=2 y^(3/2)/T³+O(y²),
q_T(y,T)=8 y^(7/2)/(7T³)+O(y⁴).

For an isolated spherical source of compact baryonic support, outside that support y=(rM/r)^(n−1), rM=(G_n M/a0)^(1/(n−1)). Hence J∝r^(−k), k=7(n−1)/2. At fixed positive m and r≫m^−1, the leading elliptic response has the asymptotic particular tail

deltaT=J/(Z m²)+O(r^(−k−2))+O(r^(−4(n−1))).

The first remainder is the spatial-derivative correction; the second is the next small-y power. This statement concerns the leading large-Z response. Compact core contributions decay exponentially, but the extended source forces an algebraic tail. For n=3, the leading coefficient is a0² rM^7/(7pi G Z m² T0³) times r^−7. Calling the entire response Yukawa would discard the actual gravitational-field source. It is not a direct force tail for matter: deltaT must still be inserted into the varied Phi equation.

For the massless leading control (m=0, boundary T0 rather than a uniquely selected vacuum minimum), the source integral is finite for a point-mass idealization: q_T saturates as y→infinity and decays as y^(7/2) at small y. Its scalar charge is

integral J d^n x = a0² rM^n/(n G_n) integral_0^infinity y^(−1/(n−1)) partial_T chi_T(y)dy.

The response tail is this charge divided by Z(n−2)S r^(n−2). It scales as M^(n/(n−1)), not a universal source-independent vacuum cutoff. Point-source Newtonian self-energy is not evaluated. In n=3 the corresponding center response is finite and equals a0² rM²/(8pi G Z) integral_0^infinity partial_T chi_T(y)dy. These controls demonstrate source dependence; they do not replace a smooth-source construction.

## What this changes for the original goal

The absence of a stationary global cutoff did not exclude a local dynamical cutoff. This local action shows the actual escape and its cost: ordinary sources displace T, alter the physical MOND equation and create an additional source-dependent response. The vacuum value T0 is an input of V; adding the constant V0 changes no equation above. In a minimally covariant embedding V0 would affect vacuum stress, but that embedding and its metric constraints have not been derived. No value of C(T0), no Lambda dictionary, no preferred vacuum versus total-density tracking and no 32pi follows here. The next required arrow is a covariant action determining V and its additive constant while retaining these source reactions and healthy constrained modes.

The algebraic-tail prediction is specific to this retained p35 kernel and positive-stiffness action. Other kernel derivatives, couplings or screening interactions may change it. The displayed two-term remainder assumes compact spherical baryonic support; a slowly decaying baryonic mass tail adds its own asymptotic correction. Symbolic checks corroborate the coefficients and general-dimensional source normalization; the analytic action variation and maximum-principle argument supply their stated scope. This is not a novelty claim or a completed theory.
