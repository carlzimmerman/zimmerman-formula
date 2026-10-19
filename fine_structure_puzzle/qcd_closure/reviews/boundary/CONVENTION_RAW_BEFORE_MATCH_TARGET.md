# Independent convention calculation before reading the new matching target

2026-10-19 UTC. This calculation was saved before reading
`common_regulator_match/INDEPENDENT_RAW.md`. It preserves both prior review
files. The new delegation supplied the suspected normal-flux relation, but
the normalization, sign, collar matching, and combined coefficient below
were recomputed from the diagonal scalar heat kernel and Duhamel variation.

Use q_k(h)=2*pi*k/L+h, mu_kj=sqrt(q_k^2+M_j^2), and common PV coefficients
c_j with c_0=1, M_0=0 and the same vector/ghost domains. The scalar part of
the stipulated four-vector-minus-two-ghost trace has rank two.

For V=mu^2 the bulk diagonal kernel, through two derivatives, is

    2 (4*pi*t)^(-3/2) exp(-t V)
      [1-t^2 Delta V/6+t^3 (partial V)^2/12+...].

After the minus proper-time log integral, its derivative density is

    L_diag,scalar = Delta V/(24*pi*mu)
                    -(partial V)^2/(96*pi*mu^3).

Integrating the first term by parts gives

    Gamma_diag,scalar = Gamma_IBP,scalar
                        + integral_boundary partial_out mu/(12*pi),
    L_IBP,scalar = (partial V)^2/(96*pi*mu^3)
                 = q^2 (partial h)^2/(24*pi*mu^3).

This sign is outward-normal. At first order around a constant V, the
integrated bulk Duhamel variation contains only the volume insertion of
delta V; its derivatives are assigned to the collar. In the diagonal
representation, the bulk first variation also has
`integral Delta(delta V)/(24*pi*mu)`, whose normal flux must instead be
subtracted from that collar. Consequently

    old Duhamel collar = collar_IBP,
    collar_diag = collar_IBP - integral_boundary partial_out mu/(12*pi).

This verifies rather than assumes the convention stated in the first
review. Adding diagonal bulk to the unshifted Duhamel collar double counts
the normal flux.

Define F0(h)=sum_(k,j)c_j mu_kj. At finite common PV masses,
F0''(h)=sum_(k,j)c_j M_j^2/mu_kj^3. In a gapped interval 0<h<2*pi/L the
physical contribution is zero; each heavy regulator tends to L/pi by its
Riemann sum. Since sum_(j>0)c_j=-1,

    F0'' -> -L/pi.

Reflection at h=pi/L gives F0'=0 there. Thus after common PV removal

    F0'(h)=1-L*h/pi.

For h=v-a/r the outward surface term at r=R is

    S(R)=a F0'(v-a/R)/3
        =a(1-L*v/pi)/3+L*a^2/(3*pi*R).

In particular at center holonomy, Gamma_diag-Gamma_IBP has inverse-radius
coefficient `+L*a^2/(3*pi)`, and the diagonal collar shifts by its negative.
For M=0 this inverse-radius term vanishes at each fixed frequency because
q/mu is a constant sign. Dropping regulators modewise loses the finite
common-PV tower contribution.

For the combined bulk calculation let magnetic field be B=b/r^2 and
electric field E=partial_r h=a/r^2, with Lorentz/gauge multiplicities as in
the original complex charged pair. The Lorentz spin insertion contributes
`-(E^2+B^2)/(2*pi*mu)`; the spatial orbital curvature contributes
`+B^2/(24*pi*mu)`. The scalar IBP term above completes

    L_IBP,2der = -(11 K1+K3) E^2/(24*pi)
                -11 K1 B^2/(24*pi),
    K1=sum_(k,j)c_j/mu_kj,
    K3=sum_(k,j)c_j M_j^2/mu_kj^3 -> -L/pi.

The radial integral through R contributes the negative of its exterior
tail. Its inverse-radius coefficient is therefore

    C_bulk,IBP = 11(a^2+b^2) K1/6 + a^2 K3/6
               ->11(a^2+b^2) K1/6-L*a^2/(6*pi).

The diagonal bulk instead gives

    C_bulk,diag = 11(a^2+b^2) K1/6-a^2 K3/6
                ->11(a^2+b^2) K1/6+L*a^2/(6*pi),

and differs by the surface shift above.

The local scalar collar from the old calculation gives at center

    C_collar,IBP =16 K1/315 -4 a^2 K3/3
                 ->16 K1/315+4 L*a^2/(3*pi).

The odd term vanishes by k -> -k-1 at every finite common PV mass. The
diagonal collar subtracts the surface flux:

    C_collar,diag =16 K1/315-a^2 K3
                  ->16 K1/315+L*a^2/pi.

For the zero-derivative GPY density W(h)=-sum c_j mu_kj^3/(3*pi), the
gapped physical fourth derivative vanishes, while
`d^4(q^2+M^2)^(3/2)/dq^4=9 M^4/(q^2+M^2)^(5/2)`.
Its integral on the real line is 12. The heavy Matsubara Riemann sum and
sum_(j>0)c_j=-1 therefore give W''''=2 L/pi^2. At center reflection kills
the cubic term, and W(v-a/r) contains `L*a^4/(12*pi^2*r^4)`.
Its interior radial integral contributes

    C_GPY=-L*a^4/(3*pi).

Both consistently matched local sums therefore give

    C_local = [16/315+11(a^2+b^2)/6] K1
              + (L/pi)[7 a^2/6-a^4/3].

For a=b=1 this is `(1171/315) K1+5 L/(6*pi)`. K1 retains the common
geometric/coupling renormalization and is not assigned an absolute finite
value here. This is a local bulk-plus-collar statement only; no smooth
core, complete global spectral remainder, metric stress, or alpha map has
been derived. It is conditional on the same uniformity and full-operator
obligations recorded in the prior review.
