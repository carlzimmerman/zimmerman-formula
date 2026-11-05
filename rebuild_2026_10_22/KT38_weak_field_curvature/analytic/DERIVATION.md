# KT38 weak-field curvature action

This is a new phenomenological functional choice within the generalized
nonrelativistic QUMOND action framework of Milgrom, arXiv:2305.01589v2,
equation 6: https://arxiv.org/html/2305.01589v2. It is not a claim that the
specific function below is literally that paper's equation 16 or is derived
from a fundamental theory. The primary-source framework was authenticated
in the preceding KT37 work; see its SOURCE_CHECK.md. The fixed exponent two
is a structural modeling choice. There is one continuous physical parameter,
ell, common to every object. The original a0 values, baryons, cuts and Q
function are retained.

With g=grad(psi), H=Hess(psi), define dimensionless invariants

    x = g.g/a0^2,  s = ell^2 H:H/a0^2,  z = x+s^2,
    P = x Q(z)/z = x R(z),  E = a0^2 P,
    Q(0)=0, Q'(z)=nu_simple(sqrt(z)).

The full Cartesian Frobenius contraction counts both off-diagonal entries.
The stable Q, R and scalar derivatives are reused read-only from KT37.
The integration constant Q(0)=0 remains essential because an additive
constant would change xQ(z)/z and hence the physical response.

For the action density -rho Phi-[2 grad(Phi).grad(psi)-E]/(8 pi G),
variation gives Delta psi=4 pi G rho and

    Delta Phi_ph = div A - partial_i partial_j B_ij,
    A = .5 E_g-g = [R-1+xR'] g,
    B = .5 E_H = 2 ell^2 s x R' H.

Indeed, partial z/partial H=4 ell^2 s H/a0^2. Omitting this factor or
the double-divergence adjoint produces a different equation. A has units
of acceleration and B acceleration times length. The weak source is

    integral v Delta Phi_ph = -integral grad(v).A - integral Hess(v):B

after boundary terms vanish or are explicitly retained. The boundary term
in the energy variation is the same general expression as KT37:

    integral_boundary n_i [(E_gi-partial_j E_Hij) delta psi
                           +E_Hij partial_j(delta psi)].

Code evaluates d=zR'=Q'-R and f=x/z, then A=[R-1+fd]g and
B=2 ell^2 s fd H. This avoids separately multiplying x by a singular R'
where possible. At g=H=0, E,A,B have their continuous zero values and no
physical regularization floor is imposed. Naked invariant-coordinate
partials R,R' remain singular. The energy is C1 at the joint zero jet;
second derivatives need not be bounded. As in KT37, non-smooth density
profiles and products of distributional Hessians require a specified
interpretation, not substitution into the scalar formula.

## Controls and weak-field scaling

Q=z gives E=g.g and exactly A=B=0. Setting ell=0 gives the unchanged
simple-QUMOND action and response. Far from a finite isolated mass, s^2/x
decays as r^-8, so the ordinary deep-MOND radial normalization is recovered.

Under (g,H)->lambda(g,H) at a fixed point with g!=0,

    x->lambda^2 x,  s->lambda^2 s,
    z=lambda^2 x+lambda^4 s^2.

Hence A+g has the ordinary deep-MOND leading term
lambda^(1/2) sqrt(a0/|g|) g, while B=O(lambda^(5/2)). The KT37 curvature
invariant instead entered at the same lambda^2 order as x. This structural
change was selected in response to its weak-dwarf and uniform-field
susceptibility obstructions, before the KT38 observational runs.

The recovery is pointwise away from persistent g=0 saddles and is not
uniform near them. At a quadratic saddle with Hessian K!=0,
s0=ell^2 tr(K^2)/a0^2, z0=s0^2, the local anomalous source is

    S_ph = [R(z0)-1] tr K
           - (4 ell^2 s0/a0^2) R'(z0) tr(K^3).

It need not vanish at a vacuum saddle. Setting A=B=0 at the central point
does not justify setting their differentiated source to zero there.

For a smooth spherical core g=kappa r+O(r^3),

    g_total = kappa r [R(z0)-(4/3) z0 R'(z0)] + O(r^3),
    z0 = (3 ell^2 kappa^2/a0^2)^2.

For positive kappa tending to zero at fixed ell, this central slope tends
to 16 a0/(9 sqrt(3) ell), although the affected spatial core shrinks.
Taking the weak-amplitude and r->0 limits in different orders therefore
gives different local slopes. This does not contradict the fixed nonzero-r
weak-field limit and does not constitute a global health result.

For a point field g=GM/r^2, at fixed ell>0 and r->0,

    s=6 ell^2 (GM)^2/(a0^2 r^6),
    g_ph ~ -5 a0^2 r^4/(9 ell^2 GM).

The anomalous gradient is negative in this limit but much smaller than the
positive Newtonian GM/r^2 term. This sign is retained in the implementation.
The point formula is an exterior asymptotic expression; it does not define
the action on a distributional point-source Hessian.

## Static linearization around a uniform external field

At g0=eta a0 e with eta>0 and H0=0, s^2 is quartic in H and
B=O(H^3). Thus its linear variation vanishes. The gradient variation is
the ordinary QUMOND one, U=nu I+eta nu' ee, so

    delta Phi_hat / delta psi_hat = nu+eta nu' cos^2(alpha).

The KT37 negative ell^2 k^2 term is absent at this particular background.
This removes that static linear obstruction, not every possible nonlinear,
inhomogeneous-background or dynamical instability. A relativistic kinetic
sector and a microscopic/coarse-graining prescription remain unspecified.

## Exact spherical reduction

Put b=g/r, x=g^2/a0^2 and s=ell^2[(g')^2+2b^2]/a0^2. With

    C=R-1+xR',  D=2 ell^2 s xR',
    A_r=Cg,  B_r=Dg',  B_t=Dg/r,

the full anomalous gradient is

    g_ph=A_r-B_r'-2(B_r-B_t)/r
        =Cg-D'g'-D[g''+2g'/r-2g/r^2].

The coefficient derivative is evaluated analytically:

    x'=2gg'/a0^2,
    s'=2ell^2[g'g''+2(g/r)(g'/r-g/r^2)]/a0^2,
    z'=x'+2ss',
    D'=2ell^2[(s'x+sx')R'+sxR''z'].

The dwarf virial calculation checks this force against both an integration
by parts and direct homology variation of the actual energy. Plummer g,
g',g'' are analytic; no variable-width surrogate replaces the Hessian term.

For a shrinking Gaussian source of width sigma, kappa is proportional to
sigma^-3 and z0 grows as ell^4 kappa^4. At fixed eta and ell>0, the smooth
STF origin contacts scale as O(eta^2 sigma^15/ell^6): C_x=O(z^-3/2),
and D_xx=O(ell^2 s z^-5/2). This is a contact estimate, not by itself a
uniform proof for every source regulator or for a simultaneous ell->0 limit.

The six analytic tests cover full tensor energy first variation, Newtonian,
ell=0 and joint-zero controls, weak scaling away from saddles, uniform-field
linear variation, smooth-core and point-field limits, and the exact radial
Plummer reduction. Their finite numerical checks accompany the derivation;
they do not establish all-configuration health or observational success.
