# Common microscopic origin: a new infrared matching requirement

The 32pi puzzle remains open. The inspected OpenAI manuscripts supply no
identity fixing the positive gravitating vacuum and the two force coefficients.
The useful additional result here is a formal infrared term missing from the
previous finite-shell calculation. It sharpens what a common-origin model must
control; it is not a new microscopic theory or an established quantum force law.

Kappa=1/2 is FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and
kappa_crit=0.345 +/- 0.078 remain separate, and are not calculation inputs.

## What the external work changes

The October 26 release adds a Euclidean wave smoothing manuscript and an
algorithmic manuscript. The relevant wave theorem concerns exp(-iT|D|),
not a gravitating vacuum or interacting medium. Its auxiliary determinant
and conserved-current construction are mathematical devices for estimating
wave norms, not a supplied microscopic action. No coefficient in that estimate
can be identified with a physical vacuum amplitude. Our frequency below has
both k^2 and k^4 terms and background dependence; the theorem does not directly
establish its dynamics or the validity of its quantum expansion.

The older scale-to-conformal manuscript could constrain a proposed critical
sector under its specific hypotheses. The existing W4-08 critical-symmetry
analysis already tested the dimension-4/3 scalar portal, vector and tensor
unitarity tests, finite-charge sectors, and vacuum stress. Repeating those
would not be a new opening. The manuscript neither supplies the needed positive
vacuum nor a joint amplitude identity. These are source-scope assessments,
not independent verification or refutation of either manuscript's proof.
See [SOURCE_CHECK.md](SOURCE_CHECK.md) for exact links and local predecessors.

## New bounded calculation: integrate the infrared before expanding

Start with the same preferred-frame EFT as
[the earlier audit](../lifshitz_radiative_protection_2026_10_24/RESULT.md):

    L = K phi_dot^2/2 - D (laplacian phi)^2/2
        - gamma |grad phi|^3/3 - V,       K,D,gamma > 0.

For a constant background |grad phi|=s>0, the quadratic mode is

    omega^2 = [D k^4 + gamma s k^2 (1+mu^2)]/K.

This assumes the bare cubic already exists. It does not derive that operator
from a regular microscopic parent. With n spatial dimensions the crossover
k_* ~ sqrt(gamma s/D) makes the infrared energy scale as
s^((n+2)/2), after separating ultraviolet terms; logarithms can occur where
this power coincides with an analytic subtraction. Now specialize to n=3.
The exact radial integral for each angle is

    I(m,L) = integral_0^L k^3 sqrt(k^2+m^2) dk,
    m^2 = gamma s (1+mu^2)/D,
    I = (L^2+m^2)^(5/2)/5 - m^2(L^2+m^2)^(3/2)/3 + 2m^5/15
      = L^5/5 + L^3 m^2/6 - L m^4/8 + 2m^5/15
        - m^6/(16L) + O(m^8/L^3).

The zero-point energy is hbar sqrt(D/K)/(4pi^2) times the angular average
of I, where <f>=integral_0^1 f(mu) dmu. Therefore

    Delta E(s) = E0 + A1 s + A2 s^2 + B s^(5/2) + O(s^3),
    B = hbar gamma^(5/2) A / (30pi^2 sqrt(K) D^2) > 0,
    A = <(1+mu^2)^(5/2)>
      = 67sqrt(2)/48 + 5 asinh(1)/16.

E0, A1 and A2 agree with the earlier shell expressions with lower endpoint
zero. B is independent of the upper cutoff in this continuum determinant.
That does not make it universal across microscopic theories or unrestricted
matching counterterms. Polynomial counterterms through s^2 cannot cancel it;
a new s^(5/2) operator, other modes, or altered infrared dynamics can.

At a fixed positive lower endpoint, the 2m^5/15 pieces of I(m,L)-I(m,kL)
cancel. The old expansion requires m<<kL and cannot be used uniformly as
kL->0. This explains precisely why its finite-shell Taylor calculation missed
B. Searches of the direct predecessor and its SUSY continuation found no
calculation of this full-infrared term; no global literature novelty is claimed.

## Why this is a constraint, not a prediction of a different galaxy law

Even granting that the constant, linear and quadratic terms have been matched
or protected, the formal ratio of this correction to the bare cubic is

    Delta E_IR / E_classical = (3B/gamma) s^(-1/2).

It increases toward zero gradient. But the background expansion loses uniform
control there too. The low-momentum fluctuation variance is

    <|grad delta_phi|^2>_(k<k_*) / s^2
      = hbar gamma^(3/2)/(4pi^2 sqrt(K) D^2 sqrt(s))
        * <integral_0^1 x^3 / sqrt(x^2+1+mu^2) dx>.

The integral is finite and positive. Both ratios thus grow as s^(-1/2).
This precludes a controlled extrapolation of this one-loop calculation all
the way to s=0. It does not prove that every finite correction-dominated
window is impossible. Moreover a local treatment of an inhomogeneous galaxy
would require k_* times the background variation length to be large.
No such hierarchy or full quantum resummation has been established here.

For a diagnostic only, if an effective positive B h^(5/2) term dominated a
local static action with source q rho_b, spherical Gauss law would give

    4pi r^2 (5B/2) h^(3/2) = q M,
    h = [q M/(10pi B r^2)]^(2/3),
    g = q h,      v_c proportional M^(1/3) r^(-1/6).

That differs from the cubic model's flat-speed and v_c^4 proportional M
scalings. It is an independently testable consequence IF a controlled branch
with that effective energy is constructed. It is not a prediction we can
currently compare honestly against observed galaxies.

## The next microscopic requirement is more specific now

For modes with this same dispersion form and angular structure, cancellation
of the new term would require the signed, degeneracy-weighted spectral moment

    sum_i sigma_i d_i gamma_i^(5/2)/(sqrt(K_i) D_i^2) = 0,

where sigma is + for bosonic and - for fermionic zero-point contributions.
This formula is conditional on having actual modes of that form, including
consistent physical constraints. Healthy bosonic modes alone cannot satisfy
it with positive coefficients. Integer-power ultraviolet cancellation rules
do not automatically imply this fractional-power condition.

The existing SUSY audit cancels the entire one-loop determinant for identical
paired spectra, but does not select the bare cubic or a positive vacuum.
The remaining opening is a concrete protected interacting or constrained
spectrum that controls this infrared term while retaining the sourced MOND
response and fixing the vacuum in the same state. Merely imposing the displayed
sum rule would be another tuning, not a solution. No such spectrum was found
in the inspected release.

The original joint invariant remains epsilon C3^2/C2^3, with physical high-
and low-field matching as specified in W4-04. V in the present action is still
an independent constant; shifting it changes no frequency above. Thus even
successful infrared protection would leave the common-origin normalization
obligation, and this calculation supplies no kappa value.

## Verification and scope

Criteria-only freeze: ac5e89d73f. Final checker: 18/18 pass, including exact
radial integration, angular factors, predecessor matching and two independent
numerical quadratures. Removing longitudinal anisotropy gives 12/18 and exit
1, as expected. The first run caught an incorrect subleading m^6 coefficient
and low-precision substitution in the numerical fixtures; both were corrected
before the final runs. They did not alter the s^(5/2) result.

Runs were single process, under one second each; the sandbox disallowed nice,
so ordinary priority was used. No downloads or empirical fits. This is an
algebraically checked formal one-loop result, self-reviewed but not independently
reviewed, with no claim of all-orders stability or a UV completion. I1-I8:
no forbidden empirical input in executable; no measured dependence; explicit
dimension/scaling check; no target-name identification; no Friedmann equation;
rho_DE kept separate; hbar retained; pi tracked in phase space. Selection
screens requiring relativistic completion and a fixed vacuum remain unmet.
