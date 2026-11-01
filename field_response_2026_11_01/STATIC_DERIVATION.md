# Fixed-mass response to a prescribed spherical baryon field

This extends the snapshotted PN28 static parent without changing its
`B,k,C_s` or canonical waterbag level. It is a restricted equilibrium
calculation, not a time-dependent formation model or stability proof.

## Variation and the mass condition

At fixed dark rest mass, add `rho Phi_b` to the PN28 excess-energy density,
with `Phi_b` prescribed and independent of dark density. The self-gravity
term is still `rho Phi_d/2`. Its first variation is `Phi_d delta rho`;
the baryon term has no factor one half. Thus the occupied stationary state
satisfies

    (5/3) k rho^(2/3) exp(-2s)+Phi_d+Phi_b=mu,
    C_s Delta s=3B(exp(3s)-1)-2k rho^(5/3)exp(-2s).

Use the original `rho_star, h_star=5B/(2rho_star), ell` and
`epsilon=C_s/(3B ell^2)`, defining
`psi=(mu-Phi_d-Phi_b)/h_star`. In these units,

    n=exp(3s) psi_+^(3/2),
    Delta psi=-n-n_b,
    epsilon Delta s=exp(3s)(1-psi_+^(5/2))-1.

For `phi_b=Phi_b/h_star=-mb/sqrt(r^2+a^2)`, direct differentiation gives

    n_b=Delta phi_b=3mb a^2/(r^2+a^2)^(5/2),
    m_b(r)=integral_0^r n_b(t)t^2 dt=mb r^3/(r^2+a^2)^(3/2).

Let `M=integral_0^R n r^2 dr` denote dimensionless DARK mass, not total mass.
For any enclosing domain L, central regularity and the mass constraint give

    psi'(0)=s'(0)=0,
    -L^2 psi'(L)=M+m_b(L),
    s'(L)+(sqrt(3/epsilon)+1/L)s(L)=0.

The central psi and chemical potential become outputs. Fixing central psi
as well would overconstrain the response and generally change dark mass.
At fixed epsilon, every response retains the parent coefficients and baseline
M. Distinct epsilon experiments are not one jointly calibrated physical model.

The exterior dark potential is `phi_d=-M/r`; hence

    mu/h_star=psi(L)-M/L+phi_b(L),
    phi_d(r)=mu/h_star-psi(r)-phi_b(r).

This fixes the potential gauge at infinity despite the Plummer tail extending
beyond L. Baryons beyond the dark matter edge are not discarded.

## Stress and virial checks

Define `A=exp(3s)psi_+^(5/2)` and `U=exp(3s)-3s-1`. The dimensionless total
radial and tangential stresses remain

    Pi_r=A-U+(3epsilon/2)s'^2,
    Pi_t=A-U-(3epsilon/2)s'^2.

Their independently differentiated balance is

    Pi_r'+2(Pi_r-Pi_t)/r=(5/2)n psi'.

The right side includes BOTH gravitational sources. Retaining only the
matter pressure or only self-gravity would fail the full balance. Integration
against r^3 gives, in units `4pi B ell^3`,

    2E_rel-3E_U-E_grad+W_d+W_b=L^3 Pi_r(L),
    W_d=-(5/2) integral n m_d(r) r dr,
    W_b=-(5/2) integral n mb r^4/(r^2+a^2)^(3/2) dr.

The independently reconstructed self-potential energy is
`E_d=(5/4) integral n phi_d r^2 dr`, and it must equal `W_d`.
The external potential energy is instead
`E_b=(5/2) integral n phi_b r^2 dr`. For a finite-scale Plummer field,
`E_b` is NOT generally `W_b`; substituting it in the virial theorem is wrong.
The code records both separately.

The mass tests use adaptive quadrature of density, distinct from the imposed
outer derivative. At the matter edge they check

    integral_0^R n r^2 dr=M,
    -R^2 psi'(R)=integral_0^R n r^2 dr+m_b(R).

A negative control replaces the final plus sign by a minus sign in this
measured identity; it must fail for every nonzero forcing. This tests source
sign sensitivity without pretending the wrong equation is a physical branch.
The independent scalar integral check retains its finite boundary term.

## Edge, state and interpretation

If a computed branch has a simple first zero `psi(R)=0`, finite `s(R)` and
`psi'(R)<0`, then

    n(r)=exp(3s(R))[-psi'(R)]^(3/2)(R-r)^(3/2)[1+O(R-r)].

The script reports density ratios to this leading asymptote at predetermined
inward offsets; they are diagnostics, not a uniform error certificate.
The canonical stationary kinetic distribution becomes
`f=f_star 1_{exp(-2s)p^2/2+Phi_d+Phi_b<mu}`, retaining the same `f_star`.
Its existence as a stationary interior does not establish that an evolving
halo retains this isotropic waterbag under baryon assembly.

The measured column is `C_q=sqrt(5/2)n_c r_(n_c/4)`. A response ratio can be
obtained without inserting an acceleration target. The weak diffuse and
strong compact Plummer forcings are diagnostic dimensionless cases only;
they do not represent calibrated dwarf/spiral populations. Agreement of
static checks neither selects `B/V` nor proves observational success.

Execution results, failures and provenance will be in the fresh runner
directory. No numerical result is asserted by this derivation itself.
