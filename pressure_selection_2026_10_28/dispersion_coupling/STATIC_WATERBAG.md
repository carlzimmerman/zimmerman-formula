# PN28-DISP: static kinetic interpretation of the finite-gradient equations

This is a supplementary derivation for the action in `REPORT.md`, not an
assertion that its zero-density dynamical extension is complete.

## One-particle Hamiltonian and state

Use canonical specific momentum p and mass distribution f(r,p). Define
`rho=integral f dp`, `j_p=integral p f dp`, `pbar=j_p/rho`. At a static mean-rest
state with `pi_s=pbar=0`, the matter Hamiltonian can be written

    H_m=integral f p^2/(2Z(s)) dp
          +(1-1/Z(s)) |j_p|^2/(2rho),       Z=exp(2s).

For rho>0 the second term has zero first variation at j_p=0. The terms
containing pi_s in the complete Hamiltonian also have zero first variation
there. With the ordinary Newtonian gravitational energy varied consistently,

    h(r,p)=delta H/delta f=p^2/(2Z(s))+Phi(r).                   (1)

Consequently a global energy waterbag

    f(r,p)=f_* 1_(h(r,p)<mu),       f_*>0 constant,

is stationary under the canonical Vlasov equation: the distributional
Poisson bracket of a function of h with h vanishes. Its local support is
`p^2<p_F^2=2Z(mu-Phi)_+`, and elementary integrals give

    rho=(4pi/3)f_*[2Z(mu-Phi)_+]^(3/2),
    K=(3/10)rho p_F^2=k rho^(5/3),
    E_rel=K/Z=(3/5)rho(mu-Phi)_+,
    k=(3/10)[3/(4pi f_*)]^(2/3).                               (2)

Thus the same waterbag relation used by the local EOS can also arise as an
exact stationary kinetic state of the chosen rest-frame parent, with a
spatially varying finite scalar. It remains a particular phase-level state;
generic cold-field dynamics has not been shown to select it.

## Self-consistent static equations and stress

The scalar and gravity equations in the occupied region are

    F^2 c_s^2 laplacian s=3B(exp(3s)-1)-2E_rel,
    laplacian Phi=4pi G rho.                                   (3)

No local scalar minimization is made in (3). The isotropic conjugate kinetic
stress is `P_kin=2E_rel/3`. Multiplying the stationary Vlasov equation by p gives

    grad P_kin=-rho grad Phi+2E_rel grad s.

The scalar static stress is

    T_s,ij=F^2 c_s^2[partial_i s partial_j s
                       -(1/2)delta_ij |grad s|^2]-U(s)delta_ij.

Its divergence is

    div T_s=[F^2 c_s^2 laplacian s-U'(s)] grad s
           =-2E_rel grad s.

Hence the scalar and kinetic interaction forces cancel in the total stress
balance, leaving `div(P_kin I+T_s)=-rho grad Phi`. At finite gradient, scalar
stress is anisotropic and the local barotropic EOS must not replace (3).

Define the same scales as in EOS.md,

    rho_*=[3B/(2k)]^(3/5),
    h_*=5B/(2rho_*),      L^2=h_*/(4pi G rho_*),
    psi=(mu-Phi)/h_*,     r=L x,
    alpha=F^2 c_s^2/(3B L^2).

Equation (2) becomes exactly

    rho/rho_*=exp(3s) psi_+^(3/2).

The spherical static equations are therefore

    psi''+2psi'/x=-exp(3s) psi_+^(3/2),
    alpha(s''+2s'/x)=exp(3s)[1-psi_+^(5/2)]-1.                 (4)

Setting alpha=0 gives the previously derived local minimizer
`exp(3s)=[1-psi^(5/2)]^-1` in 0<psi<1. At alpha>0 the exterior scalar equation
is `alpha laplacian s=exp(3s)-1`, with the vacuum boundary s->0. The exterior
gravitational potential remains harmonic. Specifying the bound energy cutoff,
regular center, vacuum scalar boundary and mass is necessary to define a
particular finite configuration.

## Vacuum and scope qualification

The original local action uses `u=j/rho`; its full Hamiltonian contains
`pi_s/rho`. Those expressions need a vacuum/exterior prescription at rho=0.
The static branch `j=pi_s=0` has a natural continuous zero-mean energy
extension, and one may explicitly continue the one-particle Hamiltonian (1)
into the empty exterior. Then the displayed global waterbag is a stationary
solution of that defined rest-frame kinetic/scalar/Poisson system.

This is weaker than constructing a differentiable, well-posed Hamiltonian for
arbitrary vacuum-crossing perturbations. In particular `|j_p|^2/rho` need not
have a direction-independent functional derivative at f=0. The choice of its
zero-mean static continuation does not settle that issue. Thus a finite-
gradient numerical solution of (4) can be described as a **stationary kinetic
waterbag under the declared static vacuum continuation**, not as a completed
formation model or a proof of full PDE health.
