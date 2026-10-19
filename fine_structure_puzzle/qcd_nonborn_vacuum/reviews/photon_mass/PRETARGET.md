# Photon-mass independent pretarget derivation

This mathematical derivation was completed before reading the new author
photon_mass/ lane or any candidate projector. It uses the preserved
common_clean/SOURCECRITICAL.md and parent proton_kernel/DERIVATION.md §§1-3.
The old-file read also displayed §§4-6; no new-lane formula was exposed.

Provenance limitation: the first persistence command failed because a Python
triple-quoted string collided with derivative notation. After the derivation
but before this successful durable pin, a parent message disclosed that Endres
footnote 42 allows an m_gamma^2 A^2 N-dagger-N operator. That contact question
is thus NOT blind in this reviewer. No candidate projector factor or new author
packet has been read. The formulas below preceded that message; the new contact
question remains unchecked here.

## NB sector

Let s=lambda_gamma^2>0, P_s(Q^2)=Q^2/(Q^2+s), D_s=1/(Q^2+s), u=e^2,
and f(s)=M_u(s)/M at fixed pure-QCD renormalized parameters and fixed pure-QCD
M. Include the complete current/action/matching contacts. Use the complete
covariant Born subtraction at fixed positive pion mass. With a=alpha_E/u,
b=beta_M/u, the Euclidean polarizability action is 2*pi*u*(a E_E^2-b B_E^2).
Its complete angular contraction is 3*pi*u*(a-b)*Q^2*D_s. Hence a soft ball
of radius Lambda gives

 f_NB(s)-f_NB(0)=3(a-b)/(16*pi*M)*
 [-s Lambda^2+s^2 log((Lambda^2+s)/s)]+analytic hard terms+higher soft terms.

If matched hard terms are analytic in s,

 f_NB(s)=A0+A1*s+A2*s^2+gamma_NB*s^2 log(s/mu^2)+O(s^3 log s),
 gamma_NB=-3(a-b)/(16*pi*M).

A0=f_NB(0), A1 and A2 remain unknown. Changing the log scale changes only A2.
This statement concerns the fixed-QCD-tensor canonical convolution. It does
not yet equate that convolution to every possible massive-photon EFT mass
curve with regulator-dependent operators.

## Full charged-proton Born sector

With t=s/(4M^2), the parent's complete Born kernel is
B(z)=1+c z^2+d z^3+O(z^4),

 c=-3/2-4*kappa-2*kappa^2-(4/3)M^2*r_E^2,
 d=2+6*kappa+(3/2)kappa^2.

The linear z term vanishes only after the regular non-pole Born term is kept.
Since f_B(s)-f_B(0)=-t/(2*pi^2)*integral B(z)/(z^2+t) dz,

 f(s)=f(0)+A1*s+A2*s^2-sqrt(s)/(8*pi*M)
      +c*s^(3/2)/(32*pi*M^3)
      +(gamma_B+gamma_NB)*s^2 log(s/mu^2)+O(s^(5/2)),
 gamma_B=-d/(64*pi^2*M^4).

Thus Delta M=-u lambda_gamma/(8*pi)=-alpha_em lambda_gamma/2 for unit charge.
There is no s log s because the complete Born kernel has no z term. The hard
analytic coefficient A1 is not fixed. Gamma_B needs kappa but no form-factor
slopes; c needs r_E^2 if explicitly subtracted. Higher remainder control still
needs bounds on further form-factor coefficients. For general charge q,
d=2q^2+6q*kappa+(3/2)kappa^2. A p-minus-n comparison requires both moments (or
kappa_s,kappa_v), not kappa_s alone.

## Differential projectors

Let E=s*d/ds. For NB alone,

 Pi_NB f=E(E-1)(E-2)f/(2s^2)=(s/2)*d^3f/ds^3 -> gamma_NB.

For the full proton, annihilate unknown analytic terms and both lower Born
half powers without radius input:

 Pi_full f=(2/(3s^2))*E(E-1)(E-2)(E-1/2)(E-3/2)f -> gamma_total.

The normalization follows from the derivative of the polynomial at its root
2: 2*(2-1)*(2-1/2)*(2-3/2)=3/2. Then

 a-b=-(16*pi*M/3)*[gamma_total+d/(64*pi^2*M^4)].

The remaining kappa is independent proton data. These differential limits
need controlled differentiated remainders; a bare big-O statement does not
justify taking five derivatives.

## Geometric stencil

For T_q f(s)=f(qs), define
R(X)=(X-1)(X-q)(X-q^2)(X-sqrt(q))(X-q^(3/2)). Then

 R(T_q)f(s)/[s^2 log(q) q^2 R'(q^2)] -> gamma_total.

For q=4,
R(X)=X^5-31X^4+310X^3-1240X^2+1984X-1024,
so the six weights for j=0,...,5 are [-1024,1984,-1240,310,-31,1] and the
normalization is 322560 log(4) s^2. The largest argument is 1024*s and must
remain far below M_pi^2. For NB alone the polynomial is X^3-21X^2+84X-64,
normalization 2880 log(4) s^2. A finite stencil needs an ordinary remainder
o(s^2) uniformly at its finite scaled arguments, rather than five derivative
bounds. Statistical cancellation and error amplification remain practical
limitations. It removes the unknown f(0), not determines it.

## Propagator kernels and sign

(-d/ds)^n D_s(Q)=n!/(Q^2+s)^(n+1)>0.
Pi_NB D_s=-3s/(Q^2+s)^4; its negative is positive.
Writing x=Q^2, the full annihilator instead has

 Pi_full D_s=-5s(3x-s)(x-3s)/(x+s)^6.

It changes sign at x=s/3 and x=3s. A radius-free full annihilator is therefore
not a positive photon kernel merely because ordinary alternating propagator
derivatives are positive. A positive photon weight cannot cancel a positive
unit-charge Coulomb endpoint without subtraction or a signed combination.
Positivity of a photon weight is also not positivity of the NB current trace.

For r=|x_E| and m=sqrt(s), the four-dimensional Bessel representation is

 D_s(r)=m K_1(mr)/(4*pi^2 r),
 (-d/ds)^n D_s(r)=r^(n-1)K_(n-1)(mr)/(4*pi^2*2^n*m^(n-1)), n>=1,
 Pi_NB D_s(r)=-r^2 K_2(mr)/(64*pi^2).

The small-m constant divergence cancels only with complete NB Ward moments
and contacts. Deleting contacts before the limit is unsafe.

## Sharp cutoff versus photon mass

f_NB(0<Q<K)=3(a-b)K^4/(32*pi*M)+o(K^4), whereas the photon-mass shape is
lambda_gamma^4 log(lambda_gamma^2). Its coefficient is -2 times that sharp
K^4 coefficient. Likewise the complete Born d term has sharp-ball coefficient
d/(128*pi^2*M^4), versus massive-photon log coefficient -d/(64*pi^2*M^4).
The sharp Coulomb endpoint is K/(4*pi^2*M), versus -lambda_gamma/(8*pi*M).
One cannot substitute K=lambda_gamma.

## Limits, zero modes, state definition and calibration

Keep M_pi>0 while taking s->0 and require lambda_gamma<<M_pi. Extract a charged
mass at fixed s>0 with specified gauge/dressing and endpoint terms, requiring
lambda_gamma*T large. Take L->infinity before s->0, or prove uniform control
with lambda_gamma*L->infinity. At fixed L the spatial zero mode produces a
charged energy of order u Q^2/(2*s*L^3), not killed by the listed roots.

Indeed its temporal kernel is exp(-lambda_gamma|t|)/(2lambda_gamma L^3),
and a straight charge worldline self-action is
u Q^2/[2lambda_gamma^2 L^3]*[T-(1-exp(-lambda_gamma T))/lambda_gamma].
A finite four-torus constant mode instead gives a t^2 factor in the charged
correlator. Removing zero modes defines another finite-volume prescription.
The infinite-volume massless charged theory has infraparticle behavior rather
than an isolated pole; state-residue limits cannot be assumed uniform.

Hold the QCD renormalized parameters fixed while varying s. Retuning them for
each s can inject the same nonanalytic terms being measured. A full calibration
Jacobian and its path derivatives are then needed. Annihilating analytic local
matching terms does not authorize arbitrary nonanalytic retuning. M is fixed,
not a separately s-retuned normalization. These operations leave f(0), the full
M_u(0), A, R and physical alpha unknown. No useful numerical remainder bound
follows from formal power counting alone.

A source-only subagent checked known QED_M literature separately. No novelty
claim is made: the proposed extraction is a method translation/formal corollary
of massive-photon response methods, pending precise canonical matching.
