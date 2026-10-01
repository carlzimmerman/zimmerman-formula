# Prescribed reference work and a time-dependent field-coordinate change

Root proof fixed before reading the new FGF032 worker derivation. This uses
the inherited diagnostic Q action, not a new gravity mechanism or a metric
completion. Spatial domain is a fixed finite interval [0,d], per transverse
area. Fields and fluid are smooth, rho>0 and g=phi_x>0; coefficients are
constant. The identities require classical equations or the displayed residuals.
They make no global existence claim through shocks or g=0.

## Action and field equations

Write C=4 pi G, tau=K/c²>0, sigma=J/v_chi²>0, J>0 and
U(chi)=S0[cosh(2chi)-1]/4. Let the spatially uniform prescribed function
lambda(t) be C², set ell=lambda_dot, and a=a_c exp(chi+lambda).
The field Lagrangian density and matter coupling are

    L_f = [tau phi_t²/2 - W(g,a) + sigma chi_t²/2
             - J chi_x²/2 - U(chi)]/C,
    L_int = -rho phi.

Here B=W_g=(sqrt(a²+4g²)-a)/2, with g²=B²+aB. Set
T=-W_chi=-W_lambda=-a W_a. Since W=integral_0^g B(v,a)dv
and B_a=(a/sqrt(a²+4v²)-1)/2<0 for v>0, T>0 for g>0.
All derivatives W_chi,W_lambda above hold g fixed. These statements use Q;
no action for registered M or filtered MONO has been supplied.

The fluid has internal energy e(rho), p=rho e'-e (the inherited isothermal
choice is e=c_s² rho[log(rho/rho_*)-1]). Continuity and Euler equations are

    rho_t+(rho v)_x=0,
    rho(v_t+v v_x)=-p_x-rho phi_x.

The field equations at prescribed lambda are

    tau phi_tt-B_x=-C rho,
    sigma chi_tt-J chi_xx+U'(chi)=T.

Their dynamic source is B_x=C rho+tau phi_tt; B_x=C rho holds only in the
static limit. The MOND constitutive flux B has not been replaced by g.

## Local and integrated physical energy

Define E_m=rho v²/2+e and F_m=v(E_m+p). Continuity and Euler give
(E_m)_t+(F_m)_x=-rho v phi_x. The interaction identity is

    (rho phi)_t+(rho v phi)_x=rho phi_t+rho v phi_x.

It cancels fluid force work and leaves rho phi_t. Meanwhile,

    E_phi=(tau phi_t²/2+W)/C,    F_phi=-B phi_t/C,
    (E_phi)_t+(F_phi)_x=-rho phi_t-T(chi_t+ell)/C;
    E_chi=(sigma chi_t²/2+J chi_x²/2+U)/C,
    F_chi=-J chi_t chi_x/C,
    (E_chi)_t+(F_chi)_x=T chi_t/C.

Thus, for the physical energy and flux

    E=E_m+rho phi+E_phi+E_chi,
    F=v(E_m+p+rho phi)-(B phi_t+J chi_t chi_x)/C,

the exact balance is

    E_t+F_x=-ell T/C,
    d/dt integral_0^d E dx = -[F]_0^d-ell integral_0^d T/C dx.       (1)

This is the canonical energy in the original chi variables with an externally
specified reference; it includes interaction energy. No global lower bound
on this nonlinear self-gravitating energy is asserted. On smooth solutions,
internal chi/phi/matter exchanges cancel but explicit reference work remains.
In particular, with zero physical boundary flux and g>0 on a set of positive
measure, increasing lambda makes the physical energy decrease. No assertion
is made that every closed protocol has nonzero net work.

The off-shell form, useful for checks, is

    E_t+F_x+ell T/C
      = v R_v +(v²/2+e'(rho)+phi) R_c
        +phi_t R_phi/C+chi_t R_chi/C,                           (2)

where R_c=rho_t+(rho v)_x,
R_v=rho(v_t+v v_x)+p_x+rho phi_x,
R_phi=tau phi_tt-B_x+C rho,
R_chi=sigma chi_tt-J chi_xx+U'-T.
This identity distinguishes arbitrary manufactured fields from actual solutions.

## The exact theta coordinates

Let theta=chi+lambda(t). This is invertible for prescribed lambda. The
transformed density is

    L_f^theta=[tau phi_t²/2-W(g,a_c exp(theta))
       +sigma(theta_t-ell)²/2-J theta_x²/2-U(theta-lambda)]/C.    (3)

Matter and its interaction are unchanged. In particular, the velocity shift
and the shifted potential must BOTH remain. The transformed scale equation is

    sigma(theta_tt-lambda_ddot)-J theta_xx+U'(theta-lambda)=T.

It is just the original scale equation. Replacing (3) by an autonomous density
with sigma theta_t²/2 and U(theta) changes the physical model. Even a constant
nonzero lambda shifts the potential argument unless its origin is transformed.

The momenta are pi_theta=sigma(theta_t-ell)/C=pi_chi and
pi_phi=tau phi_t/C. Holding matter coordinates fixed in the Legendre transform,
the transformed canonical density is

    H_theta=E+ell pi_theta.                                    (4)

Equivalently, the field part contains C pi_theta²/(2 sigma)+ell pi_theta,
W(g,a_c exp(theta))/C+J theta_x²/(2C)+U(theta-lambda)/C, plus the
unchanged phi/matter terms. This follows directly from
pi_theta theta_t=pi_chi chi_t+ell pi_chi. It does not require assigning
lambda a momentum or an equation of motion.

The corresponding canonical energy flux is

    F_theta=F-J ell theta_x/C.

Using pi_theta,t-J theta_xx/C=(T-U')/C and (1),

    (H_theta)_t+(F_theta)_x
          =lambda_ddot pi_theta-ell U'(theta-lambda)/C.          (5)

This equals minus the explicit partial-time derivative of (3), holding theta,
theta_t and spatial gradients fixed. Conversely, subtracting the density and
flux corrections in (4)-(5) recovers exactly (1), not zero. The transformed
canonical generator differs from physical energy for a time-dependent change
of variables. That difference cannot remove the work required by the protocol.

Boundary data transform too. Original time-independent Dirichlet chi and phi
with impermeable v=0 give F=0 at a wall. In theta coordinates the same wall has
theta_t=ell, not zero, and F_theta=-J ell theta_x/C may be nonzero. Imposing
theta_t=0 instead changes the physical wall. Keep these fluxes in integrated
forms rather than assuming both coordinate descriptions have zero canonical flux.

## Controls, units and the precise missing sector

On an interval where lambda is constant, ell=lambda_ddot=0, the reference-work
source vanishes, H_theta=E and F_theta=F. The potential remains shifted if
lambda is nonzero. At an isolated instant ell=0 but lambda_ddot!=0, the energies
and fluxes coincide in value while their time derivatives can differ by
lambda_ddot pi_theta. Merely checking zero rate at one instant is insufficient
to identify the generators for an evolving protocol.

For a C² compact-time protocol with lambda and ell zero outside its support,
initial/final canonical and physical energies coincide. The intervening physical
energy change remains -integral ell T/C dx dt minus boundary transport. Equal
endpoint reference values do not by themselves set that work integral to zero.
No manufactured trajectory is claimed or needed for this exact derivation.

E has units J/m³, F has units W/m², T/C has units J/m³, ell has units1/s,
and pi_theta has units J s/m³. These dimensional relations check (1),(4),(5).
Use either registered positive a_c reference, 9.3619e-11 or1.1279e-10 m/s²,
with corresponding declared lambda; the identities do not equate their vacuum
densities. A prescribed lambda=log E(z(t)) is still external input here. No
FLRW equation, expansion friction or physical metric is present. The earlier
stage04 prescribed-chi H-trajectory obstruction is not rerun or removed.

A conserving autonomous completion must provide a physical sector whose
energy exchange cancels -ell T/C, with its own equations, energy and boundary
data, or derive the reference history internally. Equation (1) specifies the
obligation; it does not construct such a sector, decide its stability or count
its degrees of freedom. No new arbitrary reservoir is adopted in this proof.
