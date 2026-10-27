# Root candidate reconstruction: exact signed momentum-transfer gate

Candidate, not independently accepted yet. Derived before reading any new
FGF052 author/reviewer proof. Root has received the author's progress preview
that the ordinary energy estimate loses a factor N; no blind independence
claim is made. This reconstruction does not prove the actual transfer budget.
Use the pinned task/FGF051 equations, physical units and fixed coefficients.

Let C=4 pi G, g=phi_x,p=phi_t,k=chi_x,w=chi_t and W_g=B,W_chi=-T.
Write the scale potential as U. Define

  K= tau p g + sigma w k,
  S= g B-W+tau p^2/2+sigma w^2/2+J k^2/2-U.

Differentiate directly using g_t=p_x, k_t=w_x and both field equations:

  K_t=(B_x-Cn)g+tau p p_x+(J k_x+T-U')k+sigma w w_x
     =S_x-Cng.

The W_chi k=-T k contribution cancels the scale source T k. With matter
momentum (nv)_t+(nv^2+cs^2 n)_x=-ng this gives

  (nv-K/C)_t + (nv^2+cs^2 n+S/C)_x=0.                 (1)

The sign of the field contribution to total momentum is negative. Reversing
it would double rather than cancel the force source. In a stationary
hydrostatic background S0_x=C rho g0 and cs^2 rho_x=-rho g0;
therefore cs^2 rho+S0/C is constant across a connected background interval.

CONDITION: suppose fixed endpoints a_N,b_N remain exactly hydrostatic for
the entire time interval under consideration. FGF051 supplies local domains
from which this needs a smaller exterior subcone proof; it is not automatic
from boundedness alone. Suppose a positive classical branch exists throughout
[a_N,b_N]. Then its mass M is constant, its full total momentum is P0,
and, defining matter momentum P and field integral F,

  P=int n v, F=int K/C, P-F=P0, D=-F=P0-P.

Let J1=int x n and R0=b_N M-J1(0)>0. No-flux boundary continuity implies
J1'=P. Since n>0 and x<=b_N, J1(t)<=b_N M. Consequently every such branch
must obey the EXACT SIGNED NECESSARY gate

  int_0^t D(s) ds >= P0 t-R0.                         (2)

Negative transfer helps contradict survival; using int D_+ is a stronger,
not equivalent, sufficient assumption. If int_0^t D(s)ds<P0 t-R0, that
classical branch cannot exist through t. A practical sufficient bound is
D(s)<=theta P0 with theta<1 and (1-theta)P0 t>R0.
No pointwise bound on g_x occurs in this conditional criterion.

Take symmetric endpoints x* +/- (ell+h), ell=L N^-3,
h=d L N^-7/2 with fixed d>0, V=v0 N. Initially n=rho and
v=V(1-y^2)^2 on |y|<1, zero elsewhere. The direct polynomial integral is
2(1-2/3+1/5)=16/15. Uniform smoothness of the fixed background yields

  M/(2 rho(x*) ell) -> 1,
  P0/(rho(x*) V ell) -> 16/15,
  R0/(M ell) -> 1.

Hence P0/(MV)->8/15. At t=B_dagger ell/V the dimensionless necessary
transfer threshold tends

  [P0 t-R0]/(M ell) -> (8/15)B_dagger-1.              (3)

In particular, for fixed theta<1 and B_dagger>15/[8(1-theta)],
the pointwise sufficient bound D<=theta P0 excludes such classical survival
for all sufficiently large N. Equality is not sufficient, and the time
coefficient is newly chosen, not the old FGF049 comparison constant.
All statements are conditional on the exact boundaries and transfer bound.

An additional exact diagnostic, with these endpoints, is int p=0:

  tau d_t int p=[B]_a^b-CM=C int rho-CM=0,

using initial p=0 and conserved M=int rho. Also int g=[phi]_a^b remains its
background value. Neither identity bounds int p g by its mean product.
Dropping their covariance would be an invalid closure of the field momentum.
Full energy is conserved because both endpoint field velocities and matter
velocity vanish; both field fluxes must be retained. No coercive quantitative
energy-to-transfer estimate is asserted by this note.

Zero-velocity hydrostatic control has P0=P=F=D=0, J1 constant and positive
R0, and obeys (1)-(2) without contradiction. The actual high-velocity family's
transfer budget remains unproved. This is a conditional finite-interval
criterion, not an existence theorem or endpoint classification.
Both a0 values and separately compatible fixed constant/frozen H(z) references
apply independently. An evolving reference is excluded from autonomous energy
claims. Q remains distinct from RAR/M/filtered MONO; no physical completion,
calibrated evidence, cosmological result or historical novelty is inferred.
Zero mathematical executable computations. Administrative hash checks only.
