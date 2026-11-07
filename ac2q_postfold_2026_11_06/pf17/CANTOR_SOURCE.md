# Slice Cantor source has no independent forcing term

Within SOURCE_VARIATION.md's continuous-clock subclass, take the Cantor parts
of its slice BV identities. A,P have no spatial singular derivative. The
continuity of r,theta and the measure-forced equations give continuous slice
representatives of u,v. With the PF08 coefficient notation,

    D^c u=f D^c theta,
    D^c v=g_tilde D^c theta+j D^c r,
    D^c B=E_beta D^c theta.

The source F_sigma=F_sigma(r,A,P,B,u,v;phi) therefore satisfies

    D^c F_sigma=alpha_sigma D^c r+beta_sigma D^c theta,
    alpha_sigma=partial_r F_sigma+j partial_v F_sigma,
    beta_sigma=E_beta partial_B F_sigma
               +f partial_u F_sigma+g_tilde partial_v F_sigma.

All partial derivatives hold the other displayed arguments fixed. Rolling
potential terms are included in F_sigma and have no independent singular
clock-slice derivative. The acceleration contribution in the conservative
gradient equation is a_n F_sigma=-(F_sigma/r)e(r), so its singular source is

    (alpha_sigma-F_sigma/r) D^c r+beta_sigma D^c theta.

Curvature supplies only a bounded density under the native Einstein identity.
Also W_sigma^c=D^c theta+sigma D^c r/(r c). Thus this slice singular source is
a bounded linear combination of W_plus^c and W_minus^c, with coefficients
controlled by the compact bounds and ||u,v||infinity.

This is a useful homogeneous-source property. It is NOT a closed evolution
law for the Cantor parts themselves. Distributionally differentiating a
measure's absolutely continuous and singular pieces does not preserve those
classes, and their derivatives can cancel in the signed transport equation.
No equation for partial_t W_sigma^c follows by simply taking the Cantor part
of the full divergence, which is a derivative of a measure. In particular a
Gronwall estimate for total Cantor mass would require the same missing native
transport/renormalization theorem. No propagation of zero Cantor mass or
existence of a Cantor continuation is claimed here.
