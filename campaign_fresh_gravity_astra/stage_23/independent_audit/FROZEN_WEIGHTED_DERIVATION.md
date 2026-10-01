# Independently frozen FGF036 derivation

Derived from task036, FGF035 crossing and FGF023 action before reading new author/root proofs. No new formula preview. No mathematical computation.

Let I=(-h,h), length l=2h, be a restriction of the same central local Q solution. All coefficients are physical: C,cs²,J,tau,sigma>0. Write r=-(rho xi)', m=U''-T_chi, q_s=sgn(g)q, A=b_g. The pinned crossing implies A comparable to sqrt(|x|), q_s=O(x), rho bounded positive and C1, and m bounded. Denote S=int_I 1/A, P=l S, R=max rho, D=max(-m,0)+2 max(q_s²/A), with quotient extended by zero at the center. S finite and P=O(h^(3/2)); D bounded (in fact q_s²/A tends to zero).

## Weighted phi space and center

Define V_A as absolutely continuous functions on the full closed interval, zero at the two outer ends, with int A psi'² finite. Its energy seminorm is a norm. Set y=int_left^x 1/A; y runs over [0,S]. Under v(y)=psi(x(y)), int A psi'² dx=int |v_y|²dy. Conversely v in H1_0(0,S) yields an AC psi because int|psi'|dx=int|v_y|dy is finite; change of variables holds off the single central point, then by monotone exhaustion. Thus V_A is isometric in derivative norm to H1_0(0,S). Completeness can be proved directly: Cauchy derivatives converge in L2, integrals from the left converge uniformly, and the right zero trace is retained. In x coordinates

 |psi(x)-psi(z)|² <= int_between 1/A * int_between A psi'²,
 ||psi||_2² <= l S int A psi'².

In particular center traces from both sides agree; jumps are not allowed. There is no center Dirichlet condition. This follows from integrable reciprocal A, not a choice of reflecting wall.

Smooth compactly supported x functions are dense. For v in H1_0 in y, flatten it to its center value inside |y-y0|<epsilon, interpolate with a Lipschitz cutoff by 2epsilon, and keep it elsewhere. The derivative error is bounded by a constant times int_|y-y0|<2epsilon |v'|², which tends to zero: use |v-v(y0)|² <= |y-y0| int_local |v'|² for the cutoff term. The resulting psi is constant near x=0 and otherwise lies in ordinary H1 on regions with A bounded below. Endpoint cutoffs and ordinary piecewise-linear/mollified approximants there give smooth x approximants. Ordinary H1 density used here has a direct elementary construction: extend by zero at outer endpoints, approximate the L2 derivative by smooth functions with corrected zero integral, and integrate; local convolution can be kept away from the center where norms are equivalent. The constant central value need not vanish.

The weighted embedding into L2 is compact: bounded derivative energy gives a uniform sup bound and common modulus (int_between 1/A)^(1/2). Absolute continuity of the L1 integral 1/A gives uniform smallness on short x intervals. Approximating every function by its values on a finite fine grid gives uniformly small L2 error; bounded grid vectors have finite nets. This is a direct total-boundedness proof. Fluid and scale H1 embeddings have the same argument with A=1. Smooth triples are dense also in the positive kinetic L2 space.

## Full form and a sufficient shortness condition

Use V=H1_0(xi) x V_A(psi) x H1_0(eta). Equivalently replace xi by z=rho xi in H1_0, since rho,rho' bounded and rho bounded below. The full quadratic form is

 Q=int [cs² r²/rho+2r psi+(A psi'²-2q_s eta psi'+J eta'²+m eta²)/C].

Young inequalities give

 2|r psi| <= cs² r²/(2R)+2R psi²/cs²,
 2|q_s eta psi'| <= A psi'²/2+2(q_s²/A)eta².

Also ||eta||² <= l²||eta'||², by integrating from one wall. Hence if

 2 C R P/cs² <= 1/4,       D l² <= J/2,

then

 Q >= cs²/(2R)||r||² + (1/(4C))int A psi'² + J/(2C)||eta'||².

Every constant is dimensionally consistent: the first dimensionless combination is C R P/cs²; D l²/J is dimensionless. These conditions hold for all sufficiently short induced intervals of the same central solution. No fitting or coefficient retuning is required. The resulting lower bound controls the weighted product norm and kinetic L2 norm after fixed positive component scalings, but never the unweighted psi H1 derivative. The full form is bounded on V: q_s/sqrt(A) bounded makes the scale mixed term continuous, and weighted Poincare controls the matter mixed term. The lower/upper bounds and completeness prove it is closed, positive and coercive in this weighted space.

For z=rho xi, ||xi||² <= l²/rho_min² ||r||². Thus kinetic M=int[rho xi²+(tau psi²+sigma eta²)/C] is bounded by a fixed finite multiple of the displayed coercive derivative norm, giving a positive Rayleigh lower bound. This is an existential short-interval estimate; no physical frequency or calibrated interval width is supplied.

## Operator and actual transmission

Polarize Q to a symmetric bilinear form a. In kinetic Hilbert space H with inner product M, define u in D(L) iff u in V and a(u,v)=(f,v)_H for some f in H and all v in V; set Lu=f. No center boundary is added. Define

 H_f=cs² r/rho+psi,       F=A psi'-q_s eta.

The differential expressions are

 (Lu)_xi=H_f',
 (Lu)_psi=(-F'+C r)/tau,
 (Lu)_eta=(-J eta''+m eta-q_s psi')/sigma.

The domain has the equivalent concrete conditions H_f in H1(I), F in H1(I), eta in H2(I), together with u in V and the outer traces already specified. Necessity follows by testing the weak equations with smooth compact test components: H_f'=f_xi (rho cancels after integration), F'=C r-tau f_psi, and eta''=(m eta-q_s psi'-sigma f_eta)/J. The last RHS is L2 because q_s²/A bounded. Conversely these conditions permit integration by parts, including weighted psi tests since they are globally AC and have integrable derivative. This proves equivalence, not merely a formal differential notation.

All xi,psi,eta are continuous at the center. H_f, F and J eta' are also continuous there. These are the actual transmission conditions. A(0)=0 does not imply F(0)=0: psi' may scale like 1/A and have finite weighted energy because int 1/A finite. For example a flux with a nonzero constant value near zero yields psi proportional locally to int 1/A, which is continuous with a square-root cusp. This example is a kinematic weighted-domain illustration, not a new full coupled eigenfunction. Imposing a zero center flux would change the weak domain and split the interval artificially. Fluid mass is fixed since int r=0 by outer displacement traces.

## Existence and self-adjointness without a hidden operator leaf

For f in H, minimize a(v,v)/2-(f,v)_H on V. Coercivity bounds a minimizing sequence; the parallelogram identity forces its Cauchy property in the a norm, so completeness gives a unique minimizer Tf satisfying a(Tf,v)=(f,v)_H. This proves a bounded inverse map T:H->V directly. Viewed H->H, T is compact by the proved compact embedding, symmetric because a is symmetric, positive and injective. Its range is dense: a vector perpendicular to the range has T applied to it zero by symmetry, hence is zero.

L=T^-1 is self-adjoint on range T: if (v,Lu)=(g,u) for every u=Tf, then (v,f)=(Tg,f), so v=Tg lies in D(L) and Lv=g. This proves equality of adjoint domains. Positivity and the kinetic lower bound follow from a. Compact inverse, a positive variational gap, and a legitimate global transmission operator are therefore established without quoting a spectral theorem. One can further derive discrete eigenvectors by maximizing the positive compact T Rayleigh quotient, extracting a weakly convergent subsequence of bounded vectors by diagonal selection in a countable dense basis and using compactness to pass T strongly; repeat on orthogonal complements. Compactness forces nonzero eigenvalues to have finite multiplicity and to approach zero, and the remaining complement is zero since T is injective. This elementary argument gives a complete kinetic-orthonormal eigenbasis and positive L eigenvalues diverging to infinity. Modal expansion then gives conservative finite-energy linear solutions; no nonlinear evolution theorem follows. If that optional spectral construction is not needed, the preceding direct inverse/adjoint argument already establishes the bounded inverse and gap.

Both a0 choices and frozen H branches are separate positive-reference cases. Actual varying H requires the old driver conservation obligation; responsive local scale does not prove literal constant-vacuum identity. Q only; RAR/M, physical metric/photon/DOF and empirical claims are excluded. The failed standard H1 theorem remains failed. Arbitrary preassigned walls, astrophysical lengths and nonlinear Cauchy or old H2 parameter response remain unproved.
