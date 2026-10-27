# FSP-N: what coefficient is actually being predicted?

Base: FSP-000, Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`.
This note specifies a tree-level effective-theory calculation. It does not assert that every such effective theory has a quantum-gravity completion.

## Definitions

Use rationalized natural units, hbar=c=1. Fix a compact U(1)^r charge lattice and a connection column A with covariant derivative D=partial+i q^T A for an integer charge column q. Write the CP-even two-derivative kinetic term as L=-F^T K F/4, with real symmetric positive-definite K. The matrix K is dimensionless. Hold q and the charge lattice fixed when varying physical parameters. An electron need not be primitive in an arbitrary lattice convention; identify its actual q explicitly.

For conserved sources the Euclidean transverse inverse propagator at tree level is z K+M^2, where z=p_E^2 and M^2 is positive semidefinite. Contact terms and higher-derivative terms do not change the simple pole residue under the assumptions below. If all r fields are massless (M^2=0), the coefficient of the 1/r potential between identical charges is alpha_q=q^T K^{-1}q/(4 pi). This is a force coefficient; it need not describe a unique photon when r>1. More generally, for any full-column-rank matrix N spanning ker(M^2), replace K^{-1} by N(N^T K N)^{-1}N^T; N2 below treats the single-photon case.

## N1: basis covariance

For any real invertible S, the coordinate change A=S A' gives K'=S^T K S, q'=S^T q. Thus q'^T K'^{-1}q'=q^T K^{-1}q. Only lattice-preserving changes (GL(r,Z) in a primitive integral basis) preserve the original integer-coordinate lattice without also transforming its description. A continuous rescaling of A alone cannot supply a physical prediction.

## N2: a single surviving photon

Suppose ker(M^2) is one-dimensional and spanned by a nonzero vector n. Then

lim(z->0+) z (z K+M^2)^{-1}=n n^T/(n^T K n),

and the massless-pole coefficient is

alpha_q(0)=(q^T n)^2/(4 pi n^T K n).

Proof: let P=K^{-1/2} M^2 K^{-1/2}, a real symmetric positive-semidefinite matrix. Then (z K+M^2)^{-1}=K^{-1/2}(z I+P)^{-1}K^{-1/2}. The spectral decomposition gives lim z(z I+P)^{-1} as the orthogonal projection onto ker P. That kernel is spanned by K^{1/2}n; its projection is K^{1/2}n n^T K^{1/2}/(n^T K n). Multiplying by K^{-1/2} on each side proves the claim. This argument requires a finite-dimensional positive K and a positive spectral gap on the complement of the kernel.

For a Higgs of integer charge h in U(1)^2, M^2=v^2 h h^T and n can be the primitive integer vector (h_2,-h_1)/gcd(h_1,h_2). A rescaling of n cancels. A nonprimitive Higgs can leave a discrete gauge group; the pole formula does not classify that group.

## N3: the order of massless and zero-momentum limits matters

For K=[[a,b],[b,c]], a>0, ac>b^2, M^2=diag(0,m^2), and q=(1,0), direct inversion gives

z q^T(z K+M^2)^{-1}q=(c z+m^2)/((ac-b^2)z+a m^2).

For any fixed m>0 the z->0 residue is 1/a. If m=0 first, the residue is c/(ac-b^2). The two iterated limits differ for b!=0. Using the massless Schur complement as the Thomson-limit photon coupling after giving the hidden photon a mass can therefore manufacture a spurious dependence on mixing. This is tree-level decoupling; radiative threshold corrections can still change the matched a.

## N4: fixed kinetic eigenvalues and fixed charge integers are insufficient

Take q=(1,0), h=(0,1), and K(theta)=R(theta) diag(1,2) R(theta)^T. Keep q and h fixed, with m>0. Then det K=2 and tr K=3 for every theta, yet the unique massless-photon coupling satisfies 4 pi alpha_q=1/(cos(theta)^2+2 sin(theta)^2). It varies continuously from 1 to 1/2. This is a family of physically different relative orientations between K and the charge lattice, not a change of basis of one theory: q and h are held fixed. Vectorlike charged fermions can be used so that changing K introduces no perturbative chiral gauge anomaly.

This counterfamily refutes only the proposed implication from these data to a unique coupling. It does not refute an ultraviolet theory that fixes K in the physical charge basis. A global duality identification can identify some points; no such identification was supplied by this toy model.

## N5: a useful predictivity test

Let lambda label the remaining continuous physical inputs of a specified model, F(lambda)=0 its independently derived constraints, and A(lambda)=alpha(0)^-1 after charge normalization, symmetry breaking, running and matching. At a smooth solution point every admissible tangent v obeys DF v=0. A necessary condition for local prediction is dA(v)=0 for every such v. A single admissible tangent with dA(v)!=0 disproves local uniqueness there. The converse is not sufficient for global uniqueness, and a zero derivative at an isolated stationary point need not establish even local constancy.

Crucially, an arbitrary F^2 deformation is not automatically admissible in a proposed UV completion. It may leave a required UV critical surface. The actual constrained tangent, including gravitational, Yukawa, scalar and threshold inputs, is what must be checked.

## Literature context and scope

Mixed Abelian gauge kinetic matrices and charge lattices are established physics, not a novelty claim. See Del Zotto, Heckman, Kumar, Malekian and Wecht, *Kinetic mixing at strong coupling*, [Phys. Rev. D 95, 016007](https://doi.org/10.1103/PhysRevD.95.016007), Section 2, Eqs. (2.5)-(2.8), for the charge basis and complex coupling matrix. Their conventions use Im(tau)=4 pi K. Here only the CP-even electric sector is used. The source authenticates the setup; N1-N5 are derived above. Magnetic running is a distinct subtlety: [Newey, Terning and Verhaaren, arXiv:2407.13823v2](https://arxiv.org/html/2407.13823v2), Eqs. (5)-(7), keeps the electric-magnetic coupling product RG invariant. It does not fix either coupling's value.

## Discriminator and continuation

Any proposed geometric, topological or UV coefficient must yield the physical projected norm n^T K n, not merely tr K, det K, an unnormalized current norm or one matrix entry before symmetry breaking. The immediate application is the mixed-U(1) fixed-point route FSP-U. Check its full matrix direction, free overall gravity coefficient and mass thresholds. This note supplies a gate and a scoped counterexample, not a derivation of alpha.
