# PN28 dispersion route: frozen conditional EOS equations

Owner `/root/mechanism_closure`; requested base
`66c45c5082f651dd54e171f98c11acd9cb3d9086`, 2026-10-28.
This file pins the algebra for the parallel halo calculation. The action,
energy transfer, provenance and limitations are developed in `REPORT.md`.

## Explicit model and state assumptions

`s` is a dimensionless internal dilation field. The relative stream kinetic
metric is `Z(s)=exp(2s)>0`. Its chosen potential is

    U(s)=V+B[exp(3s)-3s-1],       B>0.

The physical vacuum candidate is `V=U(0)`, and `U''(0)=9B`. The form of U,
including its exponents, is a new model assumption, not a microscopic theorem.
B is never set to an acceleration-matching value in this route.

Let `K` be canonical random kinetic energy per volume. Its physical Hamiltonian
contribution is `E_rel=K exp(-2s)`, while the scalar contributes `U(s)`.
In the local, static scalar limit minimize

    W(K,s)=K exp(-2s)+U(s).

Its second s derivative is `4K exp(-2s)+9B exp(3s)>0`, and W is coercive.
For K>0 there is one minimum with s>0. Put y=exp(3s)>1. Stationarity gives

    K=(3B/2) y^(2/3)(y-1),
    E_rel=(3B/2)(y-1),
    W_min-V=B[(5/2)(y-1)-ln y].                                 (1)

To turn K into a density variable, impose an isotropic one-level canonical
waterbag, `f=f_* 1_(|p|<p_F)` in the local rest frame, f_*>0 fixed. Then

    rho=(4pi/3) f_* p_F^3,
    K=(3/10) rho p_F^2=k rho^(5/3),
    k=(3/10)[3/(4pi f_*)]^(2/3).

This is a specified phase-space state, not a derivation from a generic cold
field. The same relation holds along the declared isotropic canonical affine
family. Dynamic isotropy and selection of f_* remain separate obligations.

Define rho_*=[3B/(2k)]^(3/5). The exact reduced EOS is

    rho/rho_*=y^(2/5)(y-1)^(3/5),
    P_total+V=B ln y.                                          (2)

The pressure follows from the full matter-plus-scalar energy:

    P_total=(5/3)K partial_K W_min-W_min
           =(2/3)E_rel-U(s).

It is not the bare velocity-moment pressure or the conjugate kinetic stress
alone. In particular

    P_kin=(2/3)E_rel=B(y-1),
    P_total+V=B ln y,
    (P_total+V)/P_kin=ln(y)/(y-1).

The exact logarithmic slope is

    dP_total/dln rho=5B(y-1)/(5y-2)>0.                          (3)

As rho/rho_* goes to infinity, y/(rho/rho_*) goes to one, so

    P_total+V=B ln(rho/rho_*)+o(1),
    dP_total/dln rho -> B.

As rho goes to zero, `P_total+V=(2/3)k rho^(5/3)+o(rho^(5/3))`.
Thus the same explicitly chosen parent has a polytropic low-density end and
an asymptotically logarithmic high-density response. It is not an exact
logarithmic law on a finite interval; use (2) for finite halos.

## Independent amplitude and deformation tests

With scalar kinetic coefficient F^2>0 and canonical phi=F s, write g=1/F.
Then `m_phi^2=U_phi_phi(0)=9g^2 B`, so

    B=m_phi^2/(9g^2).

This relates the asymptotic pressure coefficient to two parameters of the
specified parent. Neither is tied to V. Changing B at fixed V preserves the
vacuum location and its energy and changes the pressure coefficient.

The allowed positive deformation

    delta U=epsilon B[exp(6s)-6s-1],       epsilon>0,

also preserves U(0)=V and U'(0)=0, but dominates at high density. It gives
`W_min proportional to K^(3/4)` and, along the same waterbag family,
`P_total+V proportional to rho^(5/4)`, rather than a log asymptote.
No symmetry excluding this term has been derived. The shape and the vacuum
normalization therefore remain conditional on physical input beyond this
construction.

If the high-density halo limit independently recovers the MC27 quarter-core
coefficient, the adopted column-to-acceleration identification would give
`a0^2=pi xi_quarter^2 G B`. Neither that finite-halo limit nor the identification
is assumed as an equation of the parent action here.
