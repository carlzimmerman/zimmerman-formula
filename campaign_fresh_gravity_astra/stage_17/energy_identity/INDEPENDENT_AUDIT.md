# Independent proof audit: prescribed reference work

Reviewer: /root/pressure_extrema. **Accepted as a conditional exact local
identity for the stated diagnostic Q action.** No mathematical correction
is needed. I inspected ROOT_DERIVATION.md and independently expanded its
derivatives and boundary terms. I did not read the new worker proof or other
independent-audit proofs. No computation or trajectory was run, and no
conserving completion, cosmology or metric sector is inferred.

## Field signs and constitutive derivatives

With B=W_g, varying phi in the displayed action gives
tau phi_tt-B_x=-C rho. The sign of -rho phi is essential. Thus the dynamic
flux equation is B_x=C rho+tau phi_tt, while B_x=C rho is a static statement.
Nothing in this calculation permits replacing the MOND flux B by phi_x.

For a=a_c exp(chi+lambda), at fixed g both W_chi and W_lambda equal a W_a.
The displayed Q inverse has B_a=(a/sqrt(a²+4v²)-1)/2. It is negative for v>0;
therefore T=-a W_a is positive for g>0. Varying chi then gives
sigma chi_tt-J chi_xx+U'=T. These signs also follow by direct integration by
parts of the action. This audit accepts the explicitly displayed action as
the premise; it does not derive a relativistic or filtered-MONO action.

## Matter, interaction and the off-shell identity

For p=rho e'-e, direct product differentiation gives

    (E_m)_t+[v(E_m+p)]_x
      =v[rho(v_t+v v_x)+p_x]+(v²/2+e') R_c.

This verifies the enthalpy term, without imposing continuity prematurely.
The corresponding unrestricted interaction derivative is

    (rho phi)_t+(rho v phi)_x
      =phi R_c+rho phi_t+rho v phi_x.

Consequently their sum is

    v R_v+(v²/2+e'+phi) R_c+rho phi_t.

The interaction rho phi appears once. It is not added again inside either
field energy. In this local dynamical-field representation no extra factor
of one half belongs on that explicit interaction term.

The remaining direct derivatives are

    (E_phi)_t+(F_phi)_x
      =phi_t R_phi/C-rho phi_t-T(chi_t+ell)/C,
    (E_chi)_t+(F_chi)_x
      =chi_t R_chi/C+T chi_t/C.

The B phi_xt terms cancel in the first line, and the J chi_x chi_xt terms
cancel in the second. Adding all lines proves exactly identity (2), including
the plus ell T/C on its left. Setting all residuals to zero gives the physical
source **-ell T/C** and the stated integrated outward-flux balance. No global
nonlinear energy lower bound follows from this bookkeeping identity.

## Time-dependent coordinate change and canonical quantities

For theta=chi+lambda(t), chi_t=theta_t-ell and chi_x=theta_x. Both the shifted
velocity and U(theta-lambda) must be kept. Their variation gives the stated
scale equation with sigma(theta_tt-lambda_ddot). Replacing either term by
its autonomous-looking counterpart changes the action; even constant nonzero
lambda retains a shifted potential argument.

The momentum pi_theta=sigma(theta_t-ell)/C equals pi_chi. Because
pi_theta theta_t=pi_chi chi_t+ell pi_chi, the Legendre transform adds
**+ell pi_theta** to the original physical energy. The spatial derivative of
the scale Lagrangian is -J theta_x/C, so its canonical energy flux is
-J theta_x theta_t/C. Relative to the original scale flux this contributes
**-J ell theta_x/C**. Matter and phi terms are unchanged.

Differentiating those corrections and using
pi_theta,t-J theta_xx/C=(T-U')/C gives

    (H_theta)_t+(F_theta)_x
       =lambda_ddot pi_theta-ell U'/C.

As a second sign check, the explicit partial-time derivative of the transformed
Lagrangian, holding theta, theta_t and gradients fixed, is
-lambda_ddot pi_theta+ell U'/C. Its negative agrees with the canonical balance.
Subtracting the density and flux corrections recovers -ell T/C, rather than
an autonomous conservation law for physical energy. No momentum or dynamical
equation for prescribed lambda was silently introduced.

## Protocol and boundary distinctions

At an isolated instant with ell=0, H_theta=E and F_theta=F in value; their
time derivatives need not agree if lambda_ddot pi_theta is nonzero. Only on
a constant-reference interval do ell and lambda_ddot both vanish throughout.
For a compact-time protocol returning lambda and ell to zero, canonical and
physical endpoint energies coincide, but the path integral of ell T need
not vanish. Nor does the derivation assert that every such protocol performs
nonzero net work.

Time-independent original Dirichlet phi and chi imply phi_t=chi_t=0 at each
wall. Together with v=0 this sets physical F=0. The equivalent transformed
wall has theta_t=ell, so F_theta=-J ell theta_x/C can remain nonzero. Imposing
theta_t=0 instead selects a different physical boundary condition. Thus the
integrated canonical and physical fluxes cannot both be discarded by the
same informal argument.

The stated units are consistent: T/C is energy density, ell is inverse time,
pi_theta is energy density times time, and both canonical correction terms
have the required density or flux units.

## Scope of acceptance

The proof assumes smooth classical fluid/field variables, rho>0, g>0, constant
couplings, a fixed flat spatial interval and a spatially uniform prescribed
C² lambda. It does not provide global smooth evolution, shock control,
expanding geometry, physical metric/photon coupling, a stable reservoir, or
an autonomous reference history. It specifies the exchange that an additional
conserving sector would need to supply; it does not construct that sector.

Both registered positive reference normalizations can be used without
equating their vacuum densities. A prescribed log E(z(t)) remains external
input. Q was used explicitly; no RAR, registered-M or operative filtered-MONO
mechanism, empirical fit, historical novelty or complete-theory conclusion
is licensed by this identity.
