# Retarded response and a damped collective wave

12 October 2026. Continuation of NODAL_RING_ORIGIN.md and NODAL_FORCE_LIMITS.md. The homogeneous, zero-temperature fermion response generates positive low-frequency inertia as well as positive static stiffness. Its absorption has the passive sign. A specified isotropic gapless ensemble supports a decaying collective resonance with low-momentum frequency proportional to k^(3/2). These results concern the candidate's controlled patch theory, not stability or formation of an inhomogeneous galaxy.

## Retarded kernel from the same fermions

Use exp(-i omega t), hbar=1, zero temperature and chemical potential. Let m=Delta be a homogeneous gap and q the energy-valued axial momentum. Divide the polarization Hessian by A h^2, where A=N m_*/(2 pi v). Write z=omega+i0 and s=sqrt(q^2-z^2), continued from positive real s at imaginary frequency. The renormalized kernels are

    Pi_parallel(z,q)/(A h^2)
      = m+(s^2+4m^2)/(2s) atan(s/(2m)),
    Pi_perp(z,q)/(A h^2)
      = m+s/2 atan(s/(2m)).

At s=0 use their continuous limits 2m and m. At m=0 both become pi s/4. The static limits agree with the preceding calculation and retain its explicitly chosen quadratic subtraction. This is the leading nodal-patch continuum result below the band cutoff, not the full original band response at arbitrary momentum.

The derivation replaces each static interband denominator 1/(E_-+E_+) with

    (E_-+E_+)/[(E_-+E_+)^2-z^2].

The same band-projector overlaps enter. Twenty mass, momentum, imaginary-frequency and polarization-channel combinations compare direct momentum integration with the displayed expressions. A separate frequency integral over the absorption spectrum checks each imaginary-frequency shift. No noisy real-frequency analytic continuation from numerical data was used.

## Positive inertia and fermion-pair absorption

At q=0 and |omega| much less than m,

    Pi_parallel/(A h^2)=2m-omega^2/(6m)+...,
    Pi_perp/(A h^2)=m-omega^2/(4m)+... .

Thus the induced kinetic coefficients are A h^2/(6m) and A h^2/(4m), both positive. They were computed, rather than selected to repair a negative kinetic term. Additional bare kinetic terms remain assumptions of the scalar-polarization sector.

For a single axial patch the pair-production threshold is omega_th=sqrt(q^2+4m^2). Below it the ideal zero-temperature response is nondissipative. Above it define t=sqrt(omega^2-q^2). The absorption is

    -Im Pi_parallel/(A h^2)=pi (t^2-4m^2)/(4t),
    -Im Pi_perp/(A h^2)=pi t/4.

Both are nonnegative. A periodic source does nonnegative average work on the fermion excitations with this convention. This is an energy-transfer channel into the medium, not disappearance of energy or a free power supply.

For positive imaginary frequency Omega, the subtracted spectral identity is

    Pi(i Omega,q)-Pi(0,q)
       = (2 Omega^2/pi) integral_{omega_th}^infinity
          [-Im Pi(w,q)]/[w(w^2+Omega^2)] dw >= 0.

The tested direct-band, spectral and closed-form calculations agree within their declared tolerances. The infinite upper bound refers to the continuum patch expression; finite-band effects are outside this approximation.

## What the positive-bath check establishes

A regulated positive absorption spectrum can be represented by oscillator modes with positive frequencies Omega_n and couplings c_n. With x collecting the scalar and polarization perturbations, write the quadratic energy

    H = positive kinetic terms + x^T K_static x/2
         + sum_n Omega_n^2 [y_n-(c_n dot x)/Omega_n^2]^2/2.

If K_static is positive, this regulated Hamiltonian is nonnegative. Eliminating y_n generates a retarded term

    -sum_n c_n c_n^T z^2/[Omega_n^2 (Omega_n^2-z^2)],

which has exactly the subtracted passive spectral form. This supplies a reason for stability of the retained homogeneous linear problem, rather than treating the sign of one imaginary part as a proof by itself. It does not fix the required static counterterm or establish a renormalized ultraviolet completion.

For a=Z=I=A h^2=v=1, gap m=0.3, and the scalar coupled to the parallel polarization channel, the static two-field matrix is

    [[k^2, -k], [-k, 1+Pi_parallel(0,k)]].

Its determinant is k^2 Pi_parallel(0,k)>0 for k>0. Three 80-mode positive spectral discretizations at k=0.1,1,3 have minimum squared frequencies 0.003749, 0.348946 and 1.918095. Their Schur complements recover the input static matrix. These finite checks illustrate the positive-energy construction; they are not a continuum spectrum or a count of all poles in an inhomogeneous background.

## Isotropic averaging creates damping even below v k

Retain the equal-speed, uniformly oriented ring ensemble assumed in NODAL_FORCE_LIMITS.md. At zero gap, its retarded response is

    Pi_iso(omega,k) = (A h^2 pi v k/4) F(omega/(v k)),
    F(x)=pi(1-x^2)/4
         - i [x-(1-x^2) atanh(x)]/2,  0<x<1.

Direct angular integration of sqrt(1-u^2-(x+i0)^2) over u from 0 to 1 verifies this expression. Some ring tangents align almost with the perturbation wavevector, giving arbitrarily small transverse pair thresholds. Consequently the isotropic ensemble absorbs at every positive frequency even when omega<v k. Transferring the nondissipative axial threshold to this ensemble would be incorrect.

For small x,

    Pi_iso = eta k - eta omega^2/(v^2 k)
              - i b omega^3/k^2 + ...,
    eta=A h^2 pi^2 v/16,
    b=A h^2 pi/(12 v^2).

The low-frequency inertia is again positive, but nonlocal and momentum-dependent at zero gap. A single constant I cannot replace it throughout this regime.

## Collective mode calculated rather than prescribed

Coupling this response to the existing scalar-polarization quadratic sector gives the determinant

    D(omega,k)=(a k^2-Z omega^2)
                 [1/a+Pi_iso(omega,k)-I omega^2]-k^2.

For positive a,Z,I and sufficiently small k, its slow branch has

    omega_0^2 approximately (a^2 eta/Z) k^3,
    Gamma approximately (a^2 b/(2Z)) omega_0^2,
    omega=omega_0-i Gamma.

The branch is damped, with Gamma/omega_0 tending to zero as k^(3/2). Its dispersion exponent 3/2 arises here from the fermion-generated |k| response combined with the critical two-field coupling. It is not the assumed single-fermion k^(3/2) dispersion used in the older bulk_cubic_spectrum.py toy, and those two calculations must not be identified.

For the dimensionless choice a=Z=I=A h^2=v=1, the real-frequency calculation gives a low-k fitted exponent 1.49949. Six additional complex-root solves continue the retarded upper-rim expression through 0<Re(omega)/(v k)<1 onto its resonance sheet. All six roots have positive real frequency and negative imaginary part. They confirm decaying resonances, not complex eigenvalues of the conservative finite oscillator bath. No global complex-pole count is claimed.

For example, the initial real-part/weak-damping calculation gives Gamma/omega about 3.24e-6 at k=0.001, 0.00260 at k=0.1 and 0.01959 at k=1. The independently solved complex poles and residuals are in nodal_resonance_run/results.json; the higher-k damping estimates need not coincide exactly with those poles.

## Implications and remaining gap

This candidate now has a calculated homogeneous cubic energy, spatial response, positive induced inertia, passive absorption, and a long-lived collective resonance in a defined ensemble. The elementary dynamical checks do not expose the growing-mode failure found in the earlier dipolar-fluid route.

That is not a completed cold-energy theory. The critical quadratic matching, existence and orientation distribution of the medium, temperature and occupation state, baryonic coupling and absolute scale remain undetermined. A homogeneous calculation cannot establish a galaxy's stability. The weak-source mass-scaling discrepancy found in NODAL_FORCE_LIMITS.md also remains; a stable wave does not repair it.

There is an additional formation constraint: at small k, the damping time scales as k^-3 while the oscillation period scales as k^-3/2. Large-scale modes can be stable but slow to settle. No number in years can be assigned until the physical coefficients are fixed. Passive absorption permits energy transfer; it does not by itself show that a galaxy reaches the proposed equilibrium during its lifetime.

The next physical bottleneck is the nonlinear sourced state and its parameter selection, including the transition between the two calculated mass–velocity regimes. The vacuum relation a0=(c/2)sqrt(G rho_DE) has still not been derived.

## Reproducibility and scope of verification

nodal_dynamics.py and nodal_dynamics_run/ contain 96 checks of direct interband integrals, spectral integrals, absorption thresholds, induced inertia and finite bath matrices. nodal_collective.py and nodal_collective_run/ contain 42 orientation and weak-damping mode checks. nodal_resonance.py and nodal_resonance_run/ contain 18 complex-root convergence, residual and decay-sign checks. Each has a matching contract. All three bounded runs pass; validated manifests record their inputs and outputs. These 156 checks are computational consistency evidence, not independent observations or a claim of model validation. The arguments are self-reviewed; no independent external referee audit has occurred.
