# Physical number and explicit Pauli-hole solver protocol

The backend returns physical comoving number derivatives C=dY/dtau, with
Y_i=nu_i f_i, nu_i the positive spin-resolved number measure. An exact-angular
backend accepts both f and availability A=1+eta f as independent arrays.
This is essential when f rounds to one while A remains positive below an ulp.
The backend Jacobian is dC/dY, already including occupation-to-number factors.

For each fermion, choose a number or hole coordinate while the occupation is
moderate. Set Z=Y for a number coordinate and Z=nu-Y for a hole coordinate;
write s=+1 or -1 respectively. Bosons always use number coordinates. Then

    dZ/dtau = diag(s) C,
    d(dZ/dtau)/dZ = diag(s) (dC/dY) diag(s).

There is no additional factor 1/nu in this chain rule. The original event
implementation needed such a factor because its first derivative was with
respect to f; the number protocol does not. `protocol_holes.py` implements
this distinction, preserves the adapter class in `QuantumState.copy`, and
passes the explicit hole availability to every backend evaluation.

The implicit driver solves

    R=Z_new-Z_old-dtau diag(s) C(Y_new)=0

with sparse Newton and a physical-domain line search. Coordinate changes
also transform the old state so the same backward-Euler equation is retained.
No accepted state is clipped. `number_gross` returns the nonnegative integrated
per-node sum of absolute stoichiometric magnitudes times forward-plus-reverse
reaction measure. The stopping allowance is

    |R_i| <= tol [1e-30 nu_i + max(|Zold_i|,|Znew_i|)]
             +32 eps dtau gross_i.

The final term is a declared floating-point cancellation allowance, not a
physical collision or an energy proof. The controls separately evaluate the
actual number-coordinate residual and each local collision energy derivative.

## Scalar reference with sub-ulp holes

The independently solved toy has F -> C + lambda, measures (1,1,m), energies
(2,1,1), and initial f=(1/2,c0,0), c0=1e-30. For lambda occupation x=1-h,
its single-event number extent is m x, hence

    fF=1/2-m x, fC=c0+m x,
    m x = dt [(1/2-mx)(1+c0+mx) h
              -(1/2+mx)(c0+mx) x].

`run_toy001` brackets this scalar equation with 100-digit mpmath arithmetic
and compares the actual finite backward-Euler solution. At dt=1 and m=1e-24,
h=3.000001e-24 to the reported precision, with relative numerical error
5.1e-15. This differs from the infinite-time equilibrium hole. At dt=1000m,
the finite-step transient is h approximately 1/(1+500)=.001996, which explains
the failed equilibrium expectation in the earlier integration control.

A double number near 1/2 cannot resolve a loss of order 1e-24. Therefore the
toy also records the reconstructed energy/number difference and its floating
roundoff scale; a nonzero reconstructed difference below that scale is not
called an exact numerical conservation proof. Event stoichiometry itself is
energy conserving. `run_protocol001` repeats the reference through a backend
having no event-array/S interface and checks its physical-number Jacobian
against finite differences, with relative error 2.88e-11.

## Averaging physical-number backends

`protocol_average.AveragedNumberEvents` normalizes nonnegative phase weights
and sums number RHS, physical-number Jacobian and gross measure with the same
weights. It retains `local_events`, their own energy vectors, `phase_weights`,
and `energy_average`. It also combines occupied-forward omitted/included
measures when every local backend provides them, and marks their availability.
This is not an inverse omitted-state bound.

Each phase conserves its own collision energy. The phase-averaged gas energy
need not be collision invariant: scalar-action covariance compensates

    Tc^3 [sum_k w_k E_k dot C_k - E_average dot C_average].

The first term vanishes for a complete local conservative operator; the second
generally does not. The helper therefore labels the averaged energy explicitly
and exposes local energy rates for independent checks. `run_average002`
verifies weighted RHS/Jacobian/gross, omission and a bounded physical step
against an independent scaled-backend construction.

## Actual exact-angular warm checkpoint

`run_angular001` uses the frozen full 25-group exact-angular operator at the
actual warm checkpoint N=.0021690179772784167, with the common consistent-mass
background and eight actual orbital phase nodes. It advances two successive
fixed-background collision intervals dN=1e-6. The production tolerance is
2e-8. Newton takes 14 and 3 iterations; independent number residual L1 is
about 8e-17, or 3.85e-17 relative. Per-phase collision energy rate relative
errors are below 7.2e-16, separately from Newton's roundoff allowance. Entropy
increases and the physical bounds hold.

The inherited low-angular-order warm state relaxes: maximum fermion
occupation becomes .956741 and then .926255, rather than remaining at its
previous saturated soft cells. This demonstrates that the earlier soft-hole
trap is not preserved by exact angular integration at this checkpoint. It
does not prove that all later physical occupations stay away from saturation.
The initial warm history itself used the old angular approximation, so this
is an explicit operator restart, not an initial-to-final exact-angular history.

`run_angular_refine001` extends that fixed-operator test to total dN=3e-5,
comparing three steps 1e-5 with six steps 5e-6. The final physical-number L1
difference is 1.50e-5; charged number, U1 number and U1 mean momentum change
by 4.89e-6, 3.52e-5 and -3.07e-5 relative. Independent number residual is
below 4.75e-17 relative and each local collision energy rate below 8.92e-16
relative. Both histories retain the quantum domain and increase entropy.
This verifies a bounded warm continuation of the physical-number protocol,
with a concrete collision-time control. Its phase background is fixed;
the scalar force, action and expansion are not advanced by this test.

The exact angular backend remains the declared entropy-variable finite radial
projection. These controls do not prove phase averaging, radial convergence,
full singlet coherence, omitted gauge/2-to-2 channels, a cosmological abundance
or vacuum survival. The coordinator owns the new common coupled evolution.
