# MV28 collective model: a leading-log microscopic stiffness ratio

This is a distinct, specified trial following the singlet-model failure.
It calculates both a positive sector energy and a stiffness in one
renormalizable matter model, at leading logarithmic order. It does not
establish a gravitational UV completion, an observed numerical ratio, or
the required halo pressure.

## Model and normalization

Gauge SU(5), with canonical Kahler potential for adjoint chiral fields A,B
and singlet X, and

    W=(h/2)X Tr A^2+(lambda/2)Tr A^2 B+fX.

The classical valley is the known one recorded in Shih v3, appendix A.2,
equations (A.8)-(A.12), checked here in the exact primary PDF. With
D=diag(2,2,2,-3,-3), it has

    A=i sqrt[2fh/(30h^2+lambda^2)] D,
    B=(hX/lambda)D,
    T=sqrt(30h^2+lambda^2)X/lambda,
    f_eff=f lambda/sqrt(lambda^2+30h^2),
    V_tree=f_eff^2.

T is the canonically normalized radial flat direction at tree level; its
F direction mixes the singlet with the charged adjoint B. W restricted to
the valley is f_eff T, so no fictitious addition of interfering F energies
has been made. A and B commute with their adjoints, giving D-flatness.
Gauging introduces gauge thresholds and positive D-term energies.

Use adjoint matrix components normalized by Tr(T_a T_b)=delta_ab and
gauge coupling g with the conventional fundamental generators having trace
delta_ab/2. Then C_adj=5. The one-loop anomalous dimensions, including
the group contractions of the specified superpotential, are

    gamma_X=[12h^2]/(16pi^2),
    gamma_B=[21lambda^2/20-10g^2]/(16pi^2),
    gamma_A=[h^2+21lambda^2/10-10g^2]/(16pi^2).              (I1)

The source for the general gamma and superpotential beta functions is
Martin-Vaughn v4, equations (2.7)-(2.10), checked in RG_SOURCES.md.
The specific group factors here are derived and separately tested with
an explicit SU(5) generator basis, not imported as a phenomenological fit.

The one-loop flows in t=ln(mu) are

    h_t=h(gamma_X+2gamma_A),
    lambda_t=lambda(gamma_B+2gamma_A),
    g_t=-5g^3/(16pi^2),     (ln f)_t=gamma_X.

The gauge coefficient follows from two adjoints: sum S(R)-3C_G=10-15.
Applying these flows directly to f_eff gives exactly at this order

    (ln f_eff)_t=gamma_eff,
    gamma_eff=[lambda^2 gamma_X+30h^2 gamma_B]
                           /(lambda^2+30h^2)
      =h^2[(87/2)lambda^2-300g^2]
           /[(16pi^2)(lambda^2+30h^2)].                      (I2)

## Leading-log vacuum and stiffness

In a common-threshold, RG-improved large-field approximation take
mu proportional to the radial |T| and U approximately f_eff(mu)^2.
Then at a radial stationary point gamma_eff=0. For h>0,

    g_*^2=(29/200)lambda_*^2.                               (I3)

This is a radiative critical surface, not a fixed point of all couplings.
Its location in dimensional field space depends on RG boundary data.
For s=ln(|T|/v), the trial portal still has to be specified as exp(2s).
At the stationary point U_ss/U=2(dgamma_eff/dt), giving

    B_curv/V_model =
      29/[12(16pi^2)^2]
        * h_*^2 lambda_*^2(16h_*^2+13lambda_*^2)
                       /(lambda_*^2+30h_*^2).                (I4)

It is positive for all h_*,lambda_*>0, so this leading-log stationary
point is a radial minimum. The equation is obtained by differentiating
the actual model's running positive F energy; it does not introduce a
free scalar-potential B. The positive height itself is
V_model=f_*^2 lambda_*^2/(lambda_*^2+30h_*^2), at this accuracy.
The microscopic f scale and remaining couplings are not fixed by (I3).

## Accuracy and remaining physical obligations

Equation (I4) is a leading-log, two-loop-order curvature obtained by
differentiating one-loop flow. Explicit higher-loop anomalous dimensions,
finite thresholds, and the relation between the moving physical thresholds
and |T| have not been computed. At the stationary surface a two-loop shift
of gamma changes its location; its derivative normally enters the curvature
at higher order under the assumed single-scale perturbative hierarchy.
That power counting is conditional on smooth threshold matching, not a
certificate of the actual multiscale spectrum. Some chiral modes can be
light, and massless unbroken gauge sectors can introduce infrared dynamics.
The common-threshold leading-log reduction must be validated against the
full gauged spectrum before treating (I4) as a controlled physical prediction.

This differs from the ungauged model in Shih's appendix; its positive
origin mass is not the large-field gauged calculation claimed here.
We have not computed the complete gauged Coleman-Weinberg potential,
transverse stability, lifetime, Goldstone/gauge dynamics, or infrared
nonperturbative contribution. The numerical RG test checks this stated
approximation, not those missing implications.

For gravity the same Kahler/W0 restrictions in MODEL.md recur. Canonical
sub-Planckian matching with no W0 gives a positive leading F energy, but
the absolute full gravitating energy and all sectors require a specified
supergravity action and controlled corrections. The continuous R symmetry
has gauge anomalies; no exact quantum-gravitational protection is proved.
An independent W0 or unknown Kahler operator can change the conclusion.

Finally, a shallow radiative minimum does not automatically yield the
PN28 logarithmic pressure. Its matter response still obeys equation (6)
in MODEL.md. The portal and successful halo dynamics remain separate,
unproved physical inputs. No coupling in this calculation is fitted to
0.002329458 or to an acceleration measurement. Formula (I4) is a conditional
microscopic relation and a useful explicit model to improve, rather than
a universal coefficient.
