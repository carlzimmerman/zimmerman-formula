# A charged sea determinant on a closed cellular regulator

FSP-010 coordinator candidate, before execution. This is an explicitly defined
finite SU(3) gauge theory with integer-flavor staggered Grassmann determinants
and a canonical noncompact photon. It is not a computation of physical QCD on
a smooth round S4. The polynomial coefficient below is a microscopic Taylor
coefficient of the full unconditioned partition, not a selected topological
population, fit, or a claim of continuum universality.

Let K_n be the cubical boundary of [0,n]^5, with all boundary cells of dimension
0 through4 and spacing a. Orient edges by increasing coordinate. Let d0,d1 be
its vertex-to-edge and edge-to-plaquette incidence maps. Its topology is S4;
H1(K_n,R)=0. For k<5,

 N_k=C(5,k)n^k[(n+1)^(5-k)-(n-1)^(5-k)].

Thus N0=10n4+20n2+2, N1=40n4+40n2, N2=60n4+20n2,
N3=40n4, N4=10n4, and rank d1=N1-N0+1=30n4+20n2-1.
These counts are obtained by choosing varying cell axes and requiring a fixed
coordinate on the external boundary; there is no physical boundary of K_n.

Take positive plaquette weights w_p. Use normalized product SU(3) Haar measure,
color action exp[(beta/3) sum_p w_p Re Tr U_p], and a photon Gaussian with
S_gamma=(1/2) sum_p w_p F_p^2, F=d1 A. Remove pure gauges, with no harmonic
one-form on this complex, and normalize this Gaussian to one. Its normalization
is independent of u=e^2; pure photon metric terms are separate. For its
covariance C_p=<F_p^2>, exact Gaussian linear algebra gives

 sum_p w_p C_p=tr[d1(d1^T w d1)^+ d1^T w]=rank d1.        (1)

Here the inverse is on gauge-orthogonal cochains; equivalently use a tree gauge.
The weighted curvature covariance is a projector on the exact two-cochains.
All photon modes in this finite definition are included.

Define one-component lattice fermions with D_f=1-kappa H_f. For a forward link
x->x+e_mu, H_f(x,x+e_mu)=eta_mu(x) U_link exp(i e q_f A_link),
eta_mu(x)=(-1)^(sum_(nu<mu) x_nu). The reverse matrix entry is minus its Hermitian
conjugate. This defines the finite model globally using the ambient coordinates;
no continuum spin-connection matching is assumed. H is anti-Hermitian and the
graph is bipartite. Its nonzero eigenvalues pair as +/-i lambda, so each integer
flavor determinant is positive. There is no valence-only replacement.

Expanding log det D=-sum_l kappa^l Tr H^l/l, length2 backtracks and length4
retracings have no photon flux. Around each elementary square the staggered
phase is -1. Four starting sites for each orientation yield

 [log det D_f]_(plaquette,kappa4)
    =kappa4(Tr U_p exp(i e q_f F_p)+h.c.)
    =2 kappa4 Re[Tr U_p exp(i e q_f F_p)].                (2)

The coefficient2 belongs to this staggered finite model. In particular it is
not the coefficient16 of flat-space Wilson spinors. A curved Wilson-fermion
translation would require parallel-transport/spin factors and is not asserted.

The full partition is Z=integral dU dmu_gamma(A) exp(color action) product_f detD_f,
with no state/topology conditioning. Write S_Q=sum_f q_f^2. At order kappa4,
the photon characteristic function is exp(-u q_f^2 C_p/2). Haar orthogonality
and the SU(3) center give integral (ReTr U_p)^2=1/2; hence at first beta
<ReTr U_p>=beta w_p/6. Combining these results gives the exact multivariate
Taylor coefficient

 [partial_u W]_(beta kappa4)
      =(beta kappa4 S_Q/6) sum_p w_p C_p
      =(beta kappa4 S_Q/6)(30n4+20n2-1), W=-log Z.       (3)

Two separate current-loop insertions start at kappa8; the order-kappa4 flux
second derivative in (2) includes the required contact at this order. Repeated
link paths have zero flux. This is an actual charged determinant contribution,
not the pure-gauge coefficient with e silently set nonzero.

No n3 term occurs in this coefficient for any n or positive w_p in this defined
model. For the unprojected polyhedral family V=10a4 n4 and formal radius
variation t=log n at fixed a,beta,kappa, the polynomial interpolation gives

 [rho_u]_(beta kappa4)=beta kappa4 S_Q/a4 [1/2+1/(6n2)].  (4)

The flat piece and n^-2 correction are regulator coefficients. There is no
n^-1 density term at this order. This does not prove a zero physical A or A_u:
the geometry is polyhedral, n is discrete, quarks are heavy, the lattice spacing
is finite, and the continuum spin/taste and mass/metric path have not been
matched. Higher hopping/gauge orders and the physical limit are not bounded
by this Taylor coefficient. Normalizing the free photon measure is harmless
for this charge derivative because that factor is independent of u; it does
not supply the absolute metric normalization of full continuum QCD+QED.

Finite checks will construct the actual boundary cell complex, count it,
check d1d0=0 and F2 ranks, enumerate all staggered plaquette signs, and evaluate
Gaussian flux variances independently in a tree gauge for n=1 with two positive
weight prescriptions. The real-coefficient H1/rank theorem is the analytic
reduction, not inferred universally from finite-field tests. No physical
proton, A, R, alpha or QCD truncation uncertainty is computed.
