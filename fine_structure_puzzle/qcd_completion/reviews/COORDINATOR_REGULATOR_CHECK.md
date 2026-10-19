# Coordinator check of the finite electric matching term

This hand check was written after reading the independent reviewer's raw
Pauli--Villars and dimensional-regulator derivations and after the author
confirmed the correction. It is not a blinded derivation. A third fresh
adjudicator was dispatched without a candidate coefficient. This note uses
an exact constant-electric oscillator to check the local versus integrated
bulk representatives and their signs. It is not an executable experiment.

Use the charged-pair counting fixed in both raw derivations:
Gamma_n=Tr_4 log H_n-2 Tr log Q_n. Put p=omega_n+h and
m_M=sqrt(p^2+M^2), with a common added regulator mass in vector and ghost
operators. The spin trace contributes -1/(2pi m_M) to both electric and
magnetic coefficients. There are two net scalar orbital traces.

For one scalar in a locally constant electric gradient, choose
h(x_1)=h_0+E x_1. The exact diagonal oscillator heat kernel is

    K_n(s;x)=(4pi s)^(-3/2) [2Es/sinh(2Es)]^(1/2)
             exp[-M^2 s-p(x)^2 tanh(Es)/E].

Its second-order multiplier relative to exp[-(p^2+M^2)s] is

    1-E^2 s^2/3+p^2 E^2 s^3/3.

The two proper-time integrals are
I_2=1/(8pi m_M) and I_3=1/(16pi m_M^3). Consequently the scalar
**local diagonal** electric coefficient is

    1/(24pi m_M)-p^2/(48pi m_M^3).

The scalar two-point bubble instead gives the fully integrated-by-parts
coefficient p^2/(48pi m_M^3). Their difference is the constant-gradient
restriction of Delta m_M/(24pi). More generally the local density is

    p Delta h/(24pi m_M)
       +E^2/(24pi m_M)-p^2 E^2/(48pi m_M^3),

so the same divergence identity holds for a nonconstant gradient. The
constant-magnetic scalar coefficient is 1/(48pi m_M).

Combining the two scalar traces and the spin trace gives the regulator's
integrated-by-parts coefficients

    K_B^M=-11/(24pi m_M),
    K_E^M=p^2/(24pi m_M^3)-1/(2pi m_M),
    K_E^M-K_B^M=-M^2/(24pi m_M^3).

Thus the physical-minus-regulator difference is positive. The large-M
circle sum has limit

    sum_n M^2/[(2pi n/L+h)^2+M^2]^(3/2)
        -> L/(2pi) integral_R dp M^2/(p^2+M^2)^(3/2)=L/pi.

This yields K_E-K_B=L/(24pi^2) in the common four-dimensional regulator,
in agreement with the reviewer's independent dimensional epsilon-times-pole
calculation. It cannot be removed by changing a single common Maxwell
coupling. Strict three-dimensional mode coefficients are equal; their
harmonic-first sum requires this additional electric matching term to
represent that four-dimensional determinant.

For the two net scalar traces the local-minus-IBP density is
Delta F_0(h)/(12pi), with
F_0'(h)=1-Lh/pi inside the positive holonomy chamber. On h=v-1/r its
outer surface contributes +L/(3pi R) to Gamma. Separately the finite
electric matching term contributes -L/(6pi R) to the IBP Coulomb-shell
Gamma, or +L/(6pi R) to logweight. These are different operations and
must not be combined by declaring both the divergence and an equation of
motion zero. An equation-of-motion representative plus its explicit
surface and a fully IBP representative must agree as complete integrals.

The local quartic potential adds its already checked logweight term
L/(3pi R). Therefore the author's original harmonic-first IBP loop
coefficient acquires +L/(6pi), giving

    a_loop,4D-IBP=L/(2pi)
       -11L(1+n_mag^2)F(Lv/(2pi))/(12pi),

where F=-psi(nu)-psi(1-nu)-2gamma_E and the common coupling is fixed
through the magnetic coefficient. This remains an off-shell exterior bulk
coefficient. It does not fix the finite-wall spectral boundary functional,
the neutral ensemble stress, or electromagnetic alpha. No conclusion
about a primary source's whole off-shell action is needed for this check;
its equation-of-motion and surface conventions require a separate audit.
