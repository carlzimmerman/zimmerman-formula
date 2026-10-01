# Weighted coupled form on a short Q crossing

2026-09-30 17:31 UTC pass. Exact conditional proof from FGF035/023 and task036;
fixed before reading any new worker/auditor proof or receiving formula previews.
The task itself suggests a weighted route. No numerical run or external source.

## Setup and domain

Restrict ONE FGF035 local solution to I_l=(-l,l). All central data and positive
physical coefficients C=4piG,cs²,J,S0,a_ref,tau,sigma stay fixed as l decreases.
Walls and mass are induced by this restriction. Write rho for its positive
C1 density, g=phi', a=a_ref exp chi, and

A=b_g(|g|,a), q=sgn(g)(|g|A-b), S=T_chi, m=U''-S.

Here q is SIGNED. The accepted crossing gives
A~a_c sqrt(|x|), a_c>0; q=O(x); S=O(|x|^(3/2)); m(0)=U''(chi_*)>0.
A is continuous, positive off zero, and bounded. In particular 1/A is in L1.
For l small, R_l=integral_I 1/A=O(sqrt(l)), P_l=2l R_l=O(l^(3/2)).
No physical coefficient has been retuned in these limits.

Define X_A={psi absolutely continuous on Ibar, psi(-l)=psi(l)=0,
integral A psi'^2<infinity}. Cauchy-Schwarz yields

|psi(x)-psi(y)|² <= integral_y^x A psi'^2 * integral_y^x 1/A,
||psi||_infinity² <= R_l E_A[psi], ||psi||_2² <= P_l E_A[psi],
E_A[psi]=integral A psi'^2.                                      (1)

The derivative norm E_A is a genuine norm by the zero endpoints. To check
completeness, an E_A-Cauchy sequence has derivatives converging in L2(A dx).
The integral functional v->integral v is continuous there since 1/A is L1.
Its limit derivative has zero integral. Integration from -l reconstructs an
absolutely continuous zero-trace function, with uniform convergence by (1).
Thus X_A is a Hilbert space with derivative inner product. It is equivalent
to the norm adding ||psi||_2²; this is the completed energy domain, not H1.

For explicit smooth density, approximate v=psi' in L2(A dx) by smooth compact
functions supported away from zero and endpoints: truncate small neighborhoods
and large values, then ordinary smooth approximation on the remaining compact
sets where A is bounded above/below. If their integrals are e_n, they tend to
integral v=0. Subtract e_n h with fixed smooth h supported away from zero and
endpoints and integral h=1. The corrected derivatives converge and have zero
integral. Their integrals from -l are C_c^infinity(I), converging in X_A.
This proves that no extra jump or center trace is created by completion.
Conversely a jump cannot satisfy absolute continuity or the bound (1).

Take V=H1_0(I) for xi, X_A for psi, H1_0(I) for eta. Fixed reference-unit
weights may be inserted into all product norms. Let d=-(rho xi)'. Then d is
L2 and integral d=0. The map xi->d is a bounded isomorphism from H1_0 to
zero-integral L2, since xi=-rho^-1 integral_-l^x d, rho and rho' bounded,
rho_min>0. In particular D=integral cs² d²/rho controls the xi H1 norm on
this fixed interval. The norm D+E_A+||eta'||² is complete and equivalent to
the product norm. Different terms are compared in fixed physical units.

## Full form and a sufficient shortness condition

The bilinear form is obtained by polarizing

Q[u]=integral {cs²d²/rho+2d psi
        +[A psi'^2-2q eta psi'+J eta'^2+m eta²]/C}.                 (2)

It includes the full coupled density and scale response; no division by A
at the center or positive-gradient H2 theorem is used. The cross term is
bounded because q/sqrt(A) is bounded and tends to zero. All other terms are
bounded in V by (1), positive bounded rho and ordinary endpoint estimates.
Thus Q is continuous on V and extends the smooth directional Hessian.

Apply, with physical factors explicit,

2d psi >= -(1/2)cs²d²/rho -2rho psi²/cs²,
-2q eta psi' >= -(1/2)A psi'^2 -2q² eta²/A.

Since q²/A=O(|x|^(3/2)) and m(0)=m0>0, choose l sufficiently small that
m-2q²/A>=m0/2 throughout I_l. Also require

2 rho_max P_l/cs² <= 1/(4C).                                     (3)

These requirements hold on every sufficiently short restriction of the SAME
central solution. They imply

Q[u] >= D/2 + E_A/(4C) + (J/C)||eta'||² + (m0/(2C))||eta||².       (4)

This proves positivity/coercivity in V, with explicit sufficient conditions,
not a numerical physical radius. In particular there is a positive lower
bound relative to the kinetic L2 norm on any fixed selected interval.
It does not contradict FGF035: E_A cannot control the ordinary ||psi'||_2.
The phi-only localized countersequence remains valid in the stronger H1 norm.

## Closed form and compact embedding, with the needed arguments

Use the positive kinetic Hilbert product

(u,v)_H=integral [rho xi zeta+(tau psi theta+sigma eta kappa)/C].

V is dense in H because smooth compact triples are dense in its three weighted
L2 factors, whose weights rho,tau/C,sigma/C are bounded above/below positively.
Equations (1),(4) bound ||u||_H by Q[u]^(1/2). Q is equivalent to the complete
V norm; hence Q+||.||_H² is closed. No merely formal differential operator is
being assumed self-adjoint at the cusp.

Embedding V into H is compact. For bounded X_A balls, (1) gives a uniform
bound and a common continuity modulus: integrals of the fixed L1 function
1/A over intervals go uniformly to zero with interval length. Finite mesh
piecewise-linear interpolation therefore approximates every such function
uniformly with arbitrarily small error. Its finitely many bounded nodal
values admit a finite-dimensional convergent subsequence. A diagonal choice
of meshes gives uniform convergence of a subsequence. Ordinary H1 endpoint
bounds give the same finite-mesh argument for xi and eta. This proves the
needed compactness directly, including passage through the center.

For f in H minimize (1/2)Q[u]-(f,u)_H over V. Coercivity bounds minimizing
sequences. The quadratic parallelogram identity makes a minimizing sequence
Cauchy in the Q norm (compare its midpoint with the infimum), so completeness
gives a unique minimizer Rf. Its first variation is

Q(Rf,v)=(f,v)_H for all v in V.                                  (5)

This proves existence rather than merely naming a form-representation theorem.
R:H->V is bounded and, as an H operator, compact, symmetric and positive;
(f,Rf)_H=Q[Rf]>0 for f!=0, since V is dense and (5) excludes Rf=0 then.
It is injective with dense range: anything H-orthogonal to its range belongs
to its kernel by symmetry. Define L=R^-1 on Ran R. Equation (5) is its exact
weak domain definition; in particular it gives an inverse at zero, not at
an unspecified spectral parameter.

For completeness the spectral step can be recovered from this compact operator:
maximize (f,Rf)_H on the unit sphere. Compactness of R and a weakly convergent
subsequence give attainment; positivity makes the maximizer have unit norm,
and varying along orthogonal unit directions gives an eigenvector. Repeat in
the invariant orthogonal complements. Infinitely many eigenvalues bounded
away from zero would give orthogonal vectors whose R-images have no convergent
subsequence, contradicting compactness. If the remaining orthogonal complement
were nonzero, injective positive R would have a positive maximum there and
supply another eigenvector. Hence the resulting eigenvectors form an H basis,
with positive eigenvalues mu_n tending to zero (finite multiplicities).
This also follows by the usual diagonal finite-coordinate weak subsequence
construction in this separable weighted L2 space, so no compact-resolvent
hypothesis at the cusp is imported. L acts diagonally with lambda_n=1/mu_n>0,
and domain sum lambda_n² |u_n|²<infinity; that real diagonal domain is
self-adjoint by testing its adjoint against each basis vector. Q's domain
has sum lambda_n |u_n|²<infinity: the eigenvectors are Q-orthogonal and
Q-complete since Q(v,e_n)=lambda_n(v,e_n)_H. Thus the spectral step has its
required domain rather than just a list of formal frequencies.

For initial (u0,v0) in V times H, the coefficient solutions
u_n(t)=u0_n cos(sqrt(lambda_n)t)+v0_n sin(sqrt(lambda_n)t)/sqrt(lambda_n)
define the unique finite-energy weak LINEAR solution u_tt+Lu=0. Partial sums
converge in V times H and preserve (||u_t||_H²+Q[u])/2; uniqueness follows
coefficientwise. This is a conditional linear perturbation theorem for the
specified frozen diagnostic model. It is not nonlinear differentiability,
nonlinear Cauchy well-posedness, metric coupling or a physical scale reservoir.

## Exact domain and transmission; center flux need not vanish

Let h=cs²d/rho+psi, P=A psi'-q eta. From (5), distributionally

(Lu)_xi=h',
(Lu)_psi=(C d-P')/tau,
(Lu)_eta=(-J eta''+m eta-q psi')/sigma.                            (6)

The first sign follows by testing d_v=-(rho zeta)' and integrating once.
The weights in H are essential to the C,tau,sigma factors. Since q/sqrt(A)
is bounded, q psi' is L2 for every u in V. Likewise P and h are initially L2.
Therefore the exact domain is

D(L)={u in V: h and P in H1(I), eta in H2(I)}.                     (7)

Necessity follows from (6) with Lu in H; sufficiency follows by integration
by parts against smooth triples and density in V. No extra flux endpoint
conditions are imposed alongside Dirichlet traces. For weighted psi tests,
absolute continuity and finite endpoint traces justify integration by parts
with P in H1; its term pairs with L2 psi and L1 psi'.

Consequently psi is continuous through zero by its energy domain, while
P, h and J eta' are continuous through zero by the operator domain. These
are transmission conditions, not two disconnected half-interval problems.
In particular no equation imposes P(0)=0. To show nonzero center flux is
actually admissible, take a smooth P equal to a nonzero constant near zero
and add a smooth adjustment away from zero so integral P/A=0. Set
psi(x)=integral_-l^x P/A, eta=0, choose

d=-rho psi/cs²+c rho, c=integral rho psi/(cs² integral rho),
xi=-rho^-1 integral_-l^x d.

Then psi lies in X_A with zero endpoints (1/A is integrable), d has zero
integral, xi is H1_0 and h=cs² c is constant. P is H1; q psi'=qP/A is L2
because q/A=O(sqrt(|x|)). Hence (7) holds with P(0)!=0, and psi'~constant/
sqrt(|x|) is generally not L2. This also proves the actual coupled operator
domain contains weighted functions excluded by standard H1. A phi-only
construction with xi=0 would fail the h in H1 gate here; retaining the fluid
response is necessary for this example.

## Limits and next gate

The theorem is restricted to all sufficiently short induced-wall patches of
a given Q crossing, subject to (3) and the scale margin. No explicit physical
l, fixed-mass family across reference choices, larger-domain assertion or
observational fit is supplied. Both a_ref=9.3619e-11 and1.1279e-10 m/s² are
independent positive choices; frozen a0 E(z), E²=.315(1+z)^3+.685, is a separate
static comparison and evolving H retains its work/reservoir obligation.
MOND flux B_x=C rho, not phi_xx=C rho, is the source. Q is not RAR or M;
no filtered-MONO/metric/photon/DOF or literal local-vacuum identity follows.

A remaining obstruction before using this linear theorem as nonlinear control
is that weighted energy permits singular perturbation gradients and need not
control finite increments of W. The next discriminating question would compare
the exact nonlinear energy with its quadratic form on this completed domain;
no such Taylor or nonlinear stability theorem is asserted in this pass.
