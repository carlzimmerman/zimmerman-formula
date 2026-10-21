# Invariant quantum state: the sphere spectrum and the missing cubic

2026-10-20. Base 9a9ab4032; criteria-only commit 2591280c8.
**The original healthy microscopic xi=1/4 goal remains open.**
This tests a de Sitter invariant determinant and an interacting continuation,
not the already tested ordinary thermal model. No target or measured value
selects a coupling, subtraction, state, curvature or source normalization.
Use c=hbar=1, signature -+++, D=n+1 spacetime dimensions, n>=2.
Primary versions, exact pins and extraction limits are in SOURCES_QUANTUM.md.

## 1. Ensemble and an explicit regular microscopic coupling

W4-04 PROOF.md R2T is inherited: a flat thermal boson has a negative
free-energy cubic -T m^3/(12pi). For fixed mass, U=F-T partial_T F
cancels this cubic; U is not the fixed-T force potential. An adiabatic
Legendre transform retains the appropriate force through its chain rule.
Replacing T by H/(2pi) does not turn that flat gas into a de Sitter state.
The Euclidean geometry is S4, not S1 times infinite flat R3.

A regular Lorentz-invariant mass-source realization, requiring no clock, is

    S=int sqrt(-g)[M_Pl^2 R/2-(Z+lambda_s^2 chi^2)(partial Phi)^2/2
          -(partial chi)^2/2-(mu0^2+xi_R R)chi^2/2-u4 chi^4/4]
          +S_ct+S_m[exp(2q Phi)g],  Z,u4,lambda_s,q>0.

For the candidate set mu0=xi_R=0. The classical two-field kinetic metric
diag(Z+lambda_s^2 chi^2,1) is positive and the quartic is bounded below.
This is a regular effective action, not a renormalizable/complete UV theory.
On a spacelike scalar background z=(partial Phi)^2=h^2, chi has the
mass source lambda_s^2 z. Its exact microscopic scalar current is
J^mu=(Z+lambda_s^2 chi^2)partial^mu Phi; dust gives nabla_mu J^mu=q rho.
Taking a quantum expectation does not make <chi^2>[Phi,g] a local function.
Counterterms and any microscopic completion must be varied as well.

A nonzero classical unit timelike clock cannot be invariant under the
full de Sitter group: the Lorentz isotropy group at a point fixes no such
vector. Nor can a smooth real Phi on compact S4 have constant positive
|grad Phi|^2: Phi has extrema. A constant mass spurion below is therefore
a spectral diagnostic, not a global constant-gradient solution or a
proved local constitutive action for an actual halo. At Phi constant,
the chi sector can instead have an invariant vacuum. These are different claims.

## 2. Exact S^(n+1) spectrum, subtraction and derivative sign

Hold H>0 and all renormalized parameters and the renormalization scale fixed.
For N identical free real bosons, let m0^2=mu0^2+xi_R D(D-1)H^2>=0.
On the D-sphere define

    V_D=2pi^((D+1)/2)/[Gamma((D+1)/2) H^D],
    A_l=H^2 l(l+D-1)+m0^2,
    d_l=(2l+D-1)(l+D-2)!/[l!(D-1)!],  l=0,1,...,
    W=(N/(2V_D)) sum_l d_l log[(A_l+lambda_s^2 z)/mu_R^2]+W_ct.

The raw sum is divergent. For D=4 and m0^2>0 it has the precise representation

    W_ren=c0+c1 z+c2 z^2+(N/(2V_4)) sum_l d_l
       [log(1+a_l z)-a_l z+(a_l z)^2/2],  a_l=lambda_s^2/A_l.

The tail is O(l^(-3)) uniformly on compact positive-z intervals.
Near zero the sum is analytic for |lambda_s^2 z|<m0^2.
The one-loop heat-kernel divergences in four dimensions are local and at
most quadratic in the mass-squared spurion: at fixed H their counterterms
are c0+c1 z+c2 z^2. Curvature and curvature-times-z terms are included here.
Thus, under this subtraction/matching contract, the finite exact derivative is

    partial_z^3 W_ren=(N lambda_s^6/V_4)
                         sum_l d_l/(A_l+lambda_s^2 z)^3 >0.

This is a new application of the spectrum, not an attributed source theorem.
Arbitrary additional finite higher-dimension EFT operators are separate
matching data; the sign does not silently constrain their third derivatives.
Analytic local counterterms cannot themselves supply a leading z^(3/2).
Such a positive term C z^(3/2) would have third derivative
-3C/(8z^(3/2))<0. The analytic representation directly excludes it here;
one need not assume that differentiating an unspecified little-o remainder
preserves its asymptotics.

The dimensional qualification precedes setting n=3. As l grows,
d_l~l^(D-1), A_l~l^2, so the kth derivative sum behaves as
sum l^(D-1-2k). It converges exactly when 2k>D; its sign is
(-1)^(k-1), with coefficient N(k-1)!lambda_s^(2k)/(2V_D).
The third-derivative test is UV finite for D<6, equivalently spatial n<5.
At D=6 a cubic-in-z logarithmic counterterm can affect that derivative.
The general spectrum is not a dimension-counting selection of n=3.

### The actual smooth-profile Euclidean family

Take a fixed smooth real Phi_* on S4, Phi=s Phi_*, t=s^2 and
v=|grad Phi_*|^2>=0, with v not identically zero. Set B=lambda_s^2 v
as a bounded multiplication operator and A_t=-Delta+m0^2+tB.
For m0^2>0, K0=A0^(-1/2) B A0^(-1/2)>=0 satisfies
K0<=||B|| A0^(-1). The sphere spectrum therefore bounds its ordered
eigenvalues kappa_j by ||B|| times those of A0^(-1), so
sum kappa_j^3<infinity in D=4. The subtracted relative determinant is

    Gamma_ren(t)=c0+c1 t+c2 t^2+(N/2)sum_j
             [log(1+t kappa_j)-t kappa_j+(t kappa_j)^2/2].

It is analytic for |t|<1/||K0||, with guaranteed radius at least
m0^2/(lambda_s^2 ||v||_infinity). Uniform convergence of the cubic
remainder justifies the derivatives for real t with A_t>0 (in particular
t>=0), without commuting B and A0:

    Gamma_ren'''(t)=N Tr[(A_t^(-1/2) B A_t^(-1/2))^3]>0.

This defines the relative subtraction equivalently by its convergent
third derivative and three matching constants. Standard one-loop local
counterterms along this fixed profile have degree at most two in t.
For general D, the same eigenvalue bound suffices when 2k>D.
For m0=0 let P project onto constants, Q=1-P and A_Q=-Delta|_Q.
The Q block has gap at least 4H^2 for t>=0. Its exact Schur complement is

    S(t)=t b00-t^2 PBQ(A_Q+tQBQ)^(-1)QBP,
    b00=<constant|B|constant>=lambda_s^2 mean(v)>0.

Thus S(t)=t[b00+O(t)], while its bracket and the renormalized Q
determinant are analytic near zero. The full result is (N/2)log t plus
an analytic function. This block identity is exact at finite cutoff;
the convergent Q relative determinant supplies its continuum one-loop
extension under the same local subtraction contract.
A proposed leading local C3|grad Phi|^3 would instead give
C3 t^(3/2) int v^(3/2)>0. Neither profile result has this term.
This tests actual smooth Euclidean scalar configurations, while still
not equating a Euclidean volume functional to a Lorentzian static force.

## 3. Free zero mode, constrained mean and order of limits

For D=4, m0=0, d0=1 and the first nonzero eigenvalue is 4H^2.
Separating l=0 gives

    W_ren=(N/(2V_4))log(lambda_s^2 z/mu_R^2)+W_nonzero(z),

where W_nonzero is analytic near z=0 with radius at least
4H^2/lambda_s^2 under the same local subtractions. This is a logarithm,
not a cubic. Its singular response has E_h=N/(V_4 h) and
E_hh=-N/(V_4 h^2) before regular analytic terms. The free minimally
coupled massless limit itself has the zero-mode state problem; it is not
a regular MOND vacuum. Positive curvature coupling instead gaps l=0
and restores the analytic case in section 2.

Fixing the mean chi0=0 in a constraint effective potential removes l=0.
The first eigenvalue stays 4H^2, so this constrained one-loop response is
analytic too. The constrained mean is an additional ensemble definition;
it is not automatically the scalar force functional in Lorentzian spacetime.
At fixed H>0, h->0 gives these analytic/logarithmic limits. Taking H->0
first recovers the four-dimensional continuum m^4 log m^2, not a thermal
three-dimensional zero-Matsubara continuum. The limits need not commute.
For m=lambda_s h>>H the bosonic leading term is
m^4[log(m^2/mu_R^2)-3/2]/(64pi^2), per real field, plus curvature terms.
It is eventually positive but quartic-logarithmic, not an actual UV C2 h^2.
A bare quadratic may dominate a finite validity window; that is not the
requested global crossover. No conclusion about all interacting theories follows.

## 4. A retained interacting zero mode: regular, analytic, concave

Retain the bounded quartic instead of assigning a guessed dynamical mass.
At fixed V=V_4, the zero-mode contribution with a z-independent measure is

    Z0(z)=int_R dc exp[-V(u4 c^4/4+lambda_s^2 z c^2/2)],
    W0(z)=-log Z0(z)/V.

Quartic domination makes Z0 entire in complex z. It is positive on the
real axis, so W0 is locally analytic at every real z, including zero.
Differentiating this convergent integral gives exactly

    W0'=lambda_s^2 <c^2>/2>0,
    W0''=-V lambda_s^4 Var(c^2)/4<0.

Writing r_G=Gamma(3/4)/Gamma(1/4), the massless point has

    <c^2>=2r_G/sqrt(V u4), <c^4>=1/(V u4),
    W0(z)=W0(0)+lambda_s^2 r_G z/sqrt(V u4)
             -lambda_s^4(1-4r_G^2)z^2/(8u4)+O(z^3).

Strict positive variance proves 1-4r_G^2>0. There is no |h|^3.
This extends the earlier affine-source concavity observation to this
explicit quantum measure; it is not a new general concavity principle.
At a finite positive-measure regulator, the full affine mass-source path
integral similarly gives W''=-lambda_s^4 Var(int chi^2)/(4V)<=0.
Finite nonaffine counterterms, fermion measures and derivative-source
interactions are outside that inequality's unqualified scope.
For the actual smooth profile at finite UV cutoff, write
Z(t)=int Dc exp[-S0(c)-t O(c)], O=lambda_s^2 int v chi^2/2>=0.
The bounded positive quartic makes this integral entire in complex t;
Z is positive on the real axis, so its logarithm is locally analytic.
Here W'= <O>/V and W''=-Var(O)/V. The continuum interacting limit
requires its own construction and renormalization; finite cutoff is explicit.
For the specified positive microscopic sigma metric, the un-subtracted
static slope is Z/2+lambda_s^2<chi^2>/2>0. Cancelling it requires an added
sector/operator or abandoning that pointwise positive bare kinetic metric.
Even a separately imposed linear cancellation leaves analytic h^4 and
higher powers here, not a positive leading h^3. Nonzero-mode corrections
are separate from the exact zero-mode integral and its stated approximation.

## 5. Actual invariant stress is not the value of a free-energy density

For the complete renormalized quantum-sector family Gamma_E(H)=V_4(H)W(0,H),
uniform metric scaling on an invariant state gives

    <T_mu nu>=-epsilon_dS g_mu nu,
    epsilon_dS=W-(H/4)partial_H W,

with renormalized parameters and mu_R held fixed, including every term in
that sector's action/measure. Choosing mu_R=H before varying requires its RG
chain rule. This formula does not assign a gravitational energy to an
isolated zero-mode normalization. In a local W(z,R) representation,

    T_mu nu=-Wg_mu nu+2W_z partial_mu Phi partial_nu Phi
       +2W_R R_mu nu+2(g_mu nu Box-nabla_mu nabla_nu)W_R.

At z=0, constant R gives epsilon=W-(R/2)W_R, agreeing with the scaling
formula. At nonzero gradient the directional term must also be retained.
Finite covariant c0+cR R changes epsilon by c0+cR R/2; its Einstein term
belongs in the calibrated gravitational coefficient. A local R^2 term
has zero variation on exact four-dimensional de Sitter. Neither variance
nor Euclidean periodicity fixes these finite matching data or epsilon's sign.

## 6. Force map and the precise remaining bridge

If an actual local static E(h) were obtained, universal conformal matter
would give div[(E_h/h)grad Phi]=q rho and
Omega_(n-1)r^(n-1)E_h=q m. For genuine UV C2 h^2 and IR C3 h^3,
Gs_n=q^2/(2Omega_(n-1)C2), a_s=2qC2/(3C3), and
g_IR=sqrt(Gs_n m a_s)/r^((n-1)/2). Only n=3 has a 1/r force.
There R=epsilon C3^2/C2^3 and xi_s=32pi/(9R); tensor/physical-metric
and inferred-density conversions remain required as in the previous lane.
This model supplies no positive leading C3, so no operational R is predicted.

The interacting Euclidean zero-mode/finite-cutoff model regularizes the free
zero-mode singularity. It does not supply the missing MOND operator or a
normalization selector. The genuinely remaining question is a Lorentzian
interacting/nonlocal response outside the finite-volume analytic class,
computed together with its renormalized stress and physical source current.
A nondegenerate analytic gap/Einstein equation at H0>0 preserves local
analyticity by the implicit
function theorem; a critical collective mode or a nonuniform limit would
need an explicit action, state, order of limits and retained-mode health.
No such bridge is proved here. This closes the specified free smooth-profile
Euclidean and finite-cutoff quartic attempts, not all quantum state routes.
