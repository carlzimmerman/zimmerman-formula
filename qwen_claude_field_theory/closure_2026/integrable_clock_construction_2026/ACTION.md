# IC-1: integrable auxiliary-clock construction

Base: `e9a8b4e05d48182947de4bd6d965960fa3428534`, 2026-09-08.
**OPEN construction, not a certified DHOST theory or completed MOND model.**
All results in this package refer to this action. Existing dirty G03 work is
not modified or silently imported as evidence.

In signature (-+++), c=1, m=M^2>0, a0>0, kappa>0, set
X=-g^{mu nu}T_mu T_nu/2>0, N=(2X)^(-1/2),
n_mu=-T_mu/sqrt(2X), h_mu nu=g_mu nu+n_mu n_nu,
a_mu=n^nu nabla_nu n_mu=D_mu ln N, K_mu nu=h_mu^rho nabla_rho n_nu.
T is a varied clock, not an external foliation. Its normalization makes X
dimensionless; kappa has units of energy density. u is an independent real
field, initially restricted to the regular branch 0<u<1.

Define

    U(c) = (1-c)[ln(1-c)^2-2 ln(1-c)+2]-2,
    w(N,u) = (u-1) ln N,    W = n^mu nabla_mu w,
    Q_mu nu = K_mu nu - h_mu nu W.

The explicit covariant action is

    S = integral sqrt(-g) {m/2 [R4-2 Lambda +4 K W-6 W^2
                  +2(1-u^2) a_mu a^mu -2 a0^2 U(u^2)]
                  + kappa X} + S_m[g,psi].

Ordinary matter and photons couple minimally to the same g. Kinetic ADM form
is m N sqrt(h)(Q_ij Q^ij-Q^2)/2. No independent Einstein metric is used for
matter. The canonical clock term is not a license to call every scalar healthy.

## Constructive mechanism to prove

Mixing only (u-1) n.grad ln N into K leaves an auxiliary-dependent primary
constraint. The accompanying ln N n.grad u term is fixed by the exact
differential dw, not by selecting a desired rank. The point transformation
bar h_ij=exp(-2w) h_ij should remove both lapse and u velocities from the
kinetic term simultaneously. Derive its primary algebra and then continue
preservation; a null Hessian by itself does not count physical modes.

## Work order / evidence contract

1. Differentiate the actual eight-velocity kinetic density; compute primaries
   and their brackets, including a missing-term control.
2. Vary the static metric potentials independently, retaining the exact
   Legendre potential. Explicitly retain clock/vacuum sources before taking
   any local weak-field approximation.
3. Derive the homogeneous Hamiltonian and constraints, their actual bracket
   matrix and preservation. Seek a nonempty expanding regular branch.
4. Continue with the inhomogeneous secondary-constraint operator and reduced
   scalar action on that branch. No full count, health, causality or PPN pass
   is inherited from steps 1-3.

Arithmetic: exact SymPy identities and explicitly labeled numerical branch
diagnostics. u=0, u=1, zero momentum and k=0 are distinct strata; a regular
branch count is never extended by substitution across a rank change.
No empirical or Lean claim is made by this package. No global novelty claim.

Homogeneous unitary gauge T=t, physical scale A, B=A exp(-w):

    L = -3m B Bdot^2 N^(3u-4)
        -m B^3 N^(3u-2) [Lambda+a0^2 U(u^2)]
        +kappa B^3 N^(3u-4)/2.

The homogeneous analysis varies N and u; neither is fixed to a background
constant before variation. Physical expansion is Adot/(N A), not Bdot/B.
