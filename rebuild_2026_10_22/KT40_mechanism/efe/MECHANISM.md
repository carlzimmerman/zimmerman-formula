# Why an external gradient activates a repulsive curvature stress

This is a property of the fixed KT39 action, not a new model or a derivation
of its searched p=9/8 and ell=3 kpc values. Write e=eta a0 and assume the
controlled regime |g_self|/e<<1 and s^p/eta²<<1 throughout the region of
interest. Expand the field energy at fixed external gradient:

    E(e+g_self,H)=a0²Q(|e+g_self|²/a0²)
                  +e² R'(eta²) s^p + higher terms,
    s=ell²(H:H)/a0².

For simple nu, Q' decreases. Since R(z)=Q(z)/z is the average of Q' on
[0,z], R(z)>Q'(z), and R'(z)=[Q'(z)-R(z)]/z<0. The curvature term reduces
the field-energy density E. The on-shell matter potential energy has the
opposite sign, U=−integral E/(8piG), so its leading curvature contribution is

    U_H=−e² R'(eta²) ell^(2p)/(8piG a0^(2p))
                          integral (H:H)^p d³r > 0.

It costs positive potential energy to compress a source and increase its
curvature. Under fixed-mass compression rho_lambda=lambda³rho(lambda r),
H_lambda=lambda³H(lambda r), hence

    U_H(lambda)=lambda^(6p−3) U_H(1),
    W_H=−dU_H/d(log lambda)=−(6p−3)U_H < 0  (p>1/2).

This is an effective repulsive stress in the scalar virial, not an extra
attractive MOND enhancement. It need not be fatal when small: positive
Newtonian and ordinary MOND binding can dominate it. The dwarf-scale
failure occurs when this stress overwhelms them. No assumption that a
negative static susceptibility is a dynamical ghost is used here.

## Closed Plummer leading term

For the same Plummer source of mass M and radius a, with u=r/a,

    H:H=(GM/a³)² * 3(1+2u⁴)/(1+u²)^5,
    J_p=integral_0^infinity u²[3(1+2u⁴)/(1+u²)^5]^p du.

J_p is positive and converges for p>1/2. Thus

    sigma_H² = W_H/(3M)
      =(p−1/2) J_p e² R'(eta²) ell^(2p)
                          (GM)^(2p−1) a^(3−6p) / a0^(2p) < 0.

With xi=GM/(a²a0), this is equivalently

    sigma_H²=(p−1/2) J_p a0 a eta² R'(eta²)
                                    (ell/a)^(2p) xi^(2p−1).

At p=9/8, J_p=0.4322655081522538, (ell/a) has power9/4 and xi has power5/4.
The small weak-source suppression is offset by the large size ratio ell/a
in compact dwarf systems. As M tends to zero at fixed size and external
field, this term scales as M^(5/4), eventually subleading to the ordinary
M-linear binding; that asymptotic statement does not ensure dwarf viability
at their actual fixed masses.

The ordinary linear external-field contribution for a spherical source is

    sigma_QUMOND,lin² = [nu(eta)+eta nu'(eta)/3] * pi GM/(32a).

The factor1/3 is the angular mean of the squared direction cosine. The
leading total is the sum of this ordinary term and sigma_H². This is an
asymptotic expansion, not the formula used for the finite-field results.
Both small parameters are reported for every comparison in localize_001.
For canonical Draco at eta3, max|g_self|/e=.002215 and max(s^p)/eta²=.014615:
the leading curvature variance is−61.4606 versus exact−61.2034 (km/s)².
Sculptor and LeoII have larger curvature expansion parameters, so their
leading coefficients are not promoted to precision predictions.

At eta=.01 the exact Draco curvature response is strongly nonlinear; the
small-parameter formula is explanatory, not substituted into that result.
The full A/B integrals, their independent force-monopole check, and direct
high-precision energy derivatives provide the finite-field evidence.

A new response law that avoids this failure must control this curvature
stress in a finite external field while retaining its intended screening.
Simply calling the source isolated hides the term that the external gradient
activates. This statement does not derive a replacement law or a microscopic
carrier for the response.
