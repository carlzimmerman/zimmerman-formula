# Radial stability separates low-density and dense portal spheres

Status: a sufficient analytic radial-stability condition and numerical
negative-energy radial witnesses for the coherent pressure-only Newtonian
fluid of PORTAL_HYDROSTATIC.md. These are not stability results for the
full reacting field, nor a completed mode spectrum or halo-selection law.

## Radial perturbation equations

Write radial displacement as delta r=r eta(r) exp(i omega t). For a
barotropic equilibrium with sound speed c_s^2=dP/d rho, mass conservation
and the Lagrangian pressure response give

    Delta rho=-rho(3 eta+r eta'),
    Delta P=c_s^2 Delta rho,
    delta rho=Delta rho-r eta rho',
    delta P=Delta P-r eta P',
    delta M=-4 pi r^3 rho eta.

Substitute these into the linear radial momentum equation,

    -omega^2 rho r eta=-delta P'-g delta rho-rho G delta M/r^2,

using P'=-rho g and M'=4 pi r^2 rho. With Gamma=rho c_s^2/P, this yields

    (Gamma P r^4 eta')' + r^3[(3 Gamma-4)P]' eta
        + omega^2 rho r^4 eta=0.

Regular displacements at the center and the zero-pressure free surface
remove the integrated boundary terms. Define B=(3 Gamma-4)P. The radial
Rayleigh numerator and positive inertia denominator are

    K[eta]=integral [Gamma P r^4 eta'^2-r^3 B' eta^2] dr,
    I[eta]=integral rho r^4 eta^2 dr.

Integration by parts gives an equivalent form without pressure derivatives,

    K=integral [Gamma P r^4 eta'^2+3B r^2 eta^2
                +2B r^3 eta eta'] dr.

For eta=constant this reproduces the previous homologous energy test.
Allowing eta to vary permits the core to move relative to the envelope.
A negative quotient K/I bounds the lowest omega^2 above by a negative
number, and therefore provides an instability witness. A positive quotient
for a finite family of trials is not a stability proof.

## Analytic sufficient condition for the low-density branch

A second exact rearrangement is

    K=integral [(4/3)P r^4 eta'^2
         +(Gamma-4/3)P r^2(3 eta+r eta')^2] dr.

Thus Gamma>=4/3 everywhere makes the radial quadratic form nonnegative.
For this EOS, set t=1/sqrt(1+x^2) with x=rho/rho_0. Direct differentiation
gives Gamma=t+t^2. Density decreases outward, so Gamma is smallest at the
center. The sufficient condition is

    x_c <= sqrt(t_*^-2-1)=0.8596784156,
    t_*=(sqrt(19/3)-1)/2.

For nonzero admissible displacements the form is positive for these
nontrivial spheres: Gamma>4/3 on an interior region even when equality
holds at the central point. This establishes absence of unstable linear
adiabatic radial modes in the retained barotropic fluid. It says nothing
about nonradial, chemical, incoherent kinetic, relativistic or quantum-field
perturbations, or nonlinear asymptotic stability.

## Negative-energy witnesses on the dense branch

The numerical calculation reconstructs each hydrostatic sphere and uses a
constant plus Gaussian radial displacement profiles. Widths span the core
and envelope. A generalized eigenvalue problem minimizes K/I within that
trial space; nearly dependent inertia directions are discarded. The final
trial is evaluated directly in the original quadratic form as a check.

Representative 14-Gaussian trial results, in units omega^2/(4 pi G rho_0):

| Central density / rho_0 | Lowest retained trial quotient | Conclusion |
|---|---:|---|
| 0.1 | +0.0376063 | Covered by analytic sufficient condition |
| 0.8 | +0.1605824 | Covered by analytic sufficient condition |
| 1 | +0.1473003 | This calculation does not decide stability |
| 2 | -0.0128070 | Negative radial-energy witness |
| 3 | -0.1827942 | Negative radial-energy witness |
| 10 | -1.1594254 | Negative radial-energy witness |
| 30 | -3.6761121 | Negative radial-energy witness |

The dense examples have negative directions despite the positive uniform
rescaling curvature reported earlier. There is no contradiction: uniform
rescaling samples only one direction. The numbers are variational upper
bounds in the numerical equilibrium approximation, not exact eigenvalues
or a certified continuum spectrum. The finite scan does not establish
that every density above 2 is unstable or locate the transition.

## Numerical scope and verification

portal_radial_modes.py uses hydrostatic ODE relative tolerance 2e-12,
logarithmically spaced radial quadrature intervals, 8 and 14 Gaussian
profiles plus the constant, and 8-point Gaussian quadrature. It repeats
three dense examples with 12-point quadrature. The inertia matrix is
rescaled by its diagonal; eigenvectors with normalized eigenvalues below
1e-10 are omitted. Both basis sizes show negative quotients at x_c=2,3,10,30.
The retained dimension varies because some trial functions are nearly
dependent. These are not nested spaces, so monotone convergence is not
claimed.

Checks compare the two exact quadratic-form expressions, the direct
Rayleigh quotient and reduced matrix result, quadrature refinements, and
agreement with the analytic positive branch. All 39 checks pass; the
manifest validates provenance. The negative signs at the sampled points
are well separated from the observed quadrature shifts. No interval error
certification or independent full eigenmode solver has been supplied.
The analysis is self-reviewed.

A narrow web search located university notes on radial pulsation, but the
two attempted primary PDF fetches failed. No external theorem or coefficient
is imported from those snippets. The equations used here follow from the
explicit linearized mass, pressure, momentum and gravity relations above.

## Consequence for the proposed cold medium

The candidate interaction supports a radially stable low-density branch
within the reduced model, while denser compact equilibria can be unstable.
Positive local compressibility and a positive uniform-contraction test were
insufficient. This is useful evidence for the interaction's viable regime,
not evidence that formation selects that branch.

Kinetic stress, source/daughter reactions and quantum gradients may change
the stability boundary. The original production history has not been rerun
with the new interaction, and no baryonic/vacuum-dependent normalization
has emerged. The full cold-energy construction remains incomplete.
