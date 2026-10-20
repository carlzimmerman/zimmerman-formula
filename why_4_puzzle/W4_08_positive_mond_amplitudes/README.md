# W4-08: attacking the microscopic MOND amplitude

2026-10-20. **Target not achieved.** No healthy microscopic model found
here forces `epsilon C3^2/C2^3 = 128pi/9`, or equivalently `xi=1/4`
in the single-mediator force convention. The advance is an explicit
positive-energy band family with the entire positive MOND constitutive
response, followed by dynamical, stress and normalization tests. Its
remaining physical mass ratio is exposed exactly; it is not a field
normalization or a common loop factor.

Standing empirical status: **kappa=1/2 FITTED**. CFG493 gives
kappa_Lambda=0.417+/-0.095 and kappa_crit=0.345+/-0.078 on separate
footings. Neither is used as an input to any calculation here.

## Strongest new construction

Pair equal-weight two-dimensional Dirac and bosonic bands. Their squared
gaps are `y^2 h^2` and `y^2 h^2+Delta^2`, with positive physical band
edge L, h=|grad phi|, and a common band factor A. Grant zero parent energy
when the splitting vanishes. The actual homogeneous determinant is

    D(z)=A[(L^2+Delta^2+z)^(3/2)-(Delta^2+z)^(3/2)
           -(L^2+z)^(3/2)+z^(3/2)],  z=y^2 h^2.

At the critical quadratic cancellation, `E(h)=D(z)-D'(0)z`, this has
positive baseline energy, positive cubic infrared response, positive
quadratic ultraviolet response, and positive radial and tangential
static Hessians at every h>0. With d=Delta/L,

    b=1+d-sqrt(1+d^2),  f=(1+d^2)^(3/2)-1-d^3,
    epsilon_band=A L^3 f,
    C2=(3/2)A L y^2 b,  C3=A y^3,
    R_band=(8/27)f/b^3=(4/27)(1+2u)/(1-u),
    u=sqrt(1+d^2)/(1+d).

A, y and L cancel from R. The gap d remains physical. The exact reciprocal
identity R(d)=R(1/d) has its unique minimum `(16+12sqrt(2))/27` at d=1.
No microscopic symmetry selecting d=1 has been established; even that
choice would give the wrong ratio. Requiring the target instead imposes

    u=(96pi-1)/(96pi+2),
    d=[u^2 +/- sqrt(2u^2-1)]/(1-u^2).

This is tuning a free gap, not a prediction. Positive algebraic d cannot
give the target because R is then algebraic. This limited coefficient
statement is not a theorem excluding interacting transcendental amplitudes.

There are two further obstacles. The actual band stress satisfies
`rho+p_parallel=(3A/2)L^2[sqrt(L^2+Delta^2)-L]>0`, so its positive
energy has not become dark energy. For a continuum or sufficiently smooth
local UV realization the gapless fermion bubble is nonlocal: the leading
scalar kernel contains `k^2 sqrt(omega_E^2+v^2 k_parallel^2)`. The
homogeneous band integral alone does not specify a nonuniform band kernel.
A local constitutive approximation requires frequency and inverse length
well below the induced gap yh. Neither homogeneous convexity nor the
cubic exponent proves dynamical health or an all-radius halo solution.

## Two completion attempts pushed further

The documented two-field superfluid parent has an open region with a
positive local quadratic Hamiltonian, including both radial modes. Its
actual tensor-plus-phonon force gives `a0=lambda^3/(8pi G Lambda)`;
the single-mediator amplitude dictionary cannot be imported. The matter
coupling lambda remains free. Its finite-charge state is not a vacuum,
the regular parent leaves an independent V0, and one low-energy phase
characteristic exceeds the metric light speed. This last calculation
does not determine the front velocity of a UV completion. The parent
therefore supplies useful local stability evidence, not the requested
healthy microscopic normalization.

An original constrained construction gives the exact attractive law
`g=gN+sqrt(a0 gN)`, positive reduced energy and subluminal local scalar
cones at every nonzero gradient. Its amplitude ratio is still
`R=8epsilon0/(9gamma b^3)`. Making its auxiliary variable propagate with
any small positive kinetic term reveals a tachyon. Generating a positive
vacuum from a linear term in that same auxiliary sector instead moves
the vacuum to y0>0 and restores a quadratic infrared response. Using the
old cubic coefficient after that deformation would not be an operational
MOND amplitude. These are concrete failures of the tested completions,
not a no-go for all constraints or all microscopic theories.

## Evidence and continuation

The raw derivations are in [PROOF.md](PROOF.md); authenticated primary
source locators and original-work boundaries are in [SOURCES.md](SOURCES.md).
Three independent raw-proof reviewers checked the band/dynamical,
two-field-parent and constrained calculations. Review forced an explicit
restriction on the parent's empty-vacuum statement; it is incorporated.
See [REVIEW.md](REVIEW.md) for hashes, scope and independence limits.

The exact checker passes **53/53** normal assertions. The separate mutant
run passes **49/53**, exits 1 and fails precisely the four frozen baseline
tests: physical gap, critical stiffness, source coupling and same-sector
vacuum deformation. Both v2 manifests validate against the current input
hashes. These checks corroborate the listed algebra, not complete
microscopic health. No numerical target search, parameter fit or source
download was used.

The remaining task is precise: derive a protected critical gradient
coupling, a controlled nonlocal source solution, vacuum-like stress and
a gap equation that fixes the surviving dimensionless ratio, all in the
same microscopic theory. Merely adding positive energy or matching a
cubic exponent no longer addresses those obligations. Detailed resumption
conditions are in [HANDOFF.md](HANDOFF.md).
