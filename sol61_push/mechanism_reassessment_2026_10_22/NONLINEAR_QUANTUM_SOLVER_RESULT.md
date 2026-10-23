# Nonlinear quantum Hamiltonian implemented: validated benchmark, not a cosmological relic

**A nonlinear quantum evolution implementation now exists and has been run. The requested evolution through cosmological bath formation and the surviving cold abundance are still not obtained.** The implementation is a finite-mode, finite-occupation Hamiltonian benchmark. It does not replace the high-H source with a small prescribed particle population and call that a cosmological calculation.

## Implemented dynamics

`quantum_fock_solver.py` constructs the original complex-scalar interactions directly in an occupation basis:

\[
H_{\rm int}=g\int d^3x:\!(X^\dagger\Phi^2+X\Phi^{\dagger2})\!:
+\lambda\int d^3x:\!\Phi^{\dagger2}\Phi^2\!:.
\]

The fields have their particle and antiparticle expansions with the factors 1/sqrt(2 E V). Every momentum-conserving creation/annihilation monomial is included, including terms that change particle number. Normal ordering is an explicit finite-regulator prescription, not a demonstrated continuum renormalization of the cosmological model.

There are three retained momenta (-p,0,+p), along one spatial axis, for each of Phi+, Phi-, X+, X-: twelve bosonic oscillators. Other spatial modes are omitted. V=100 in units mPhi^-3 is compatible with a rectangular box whose x-length is 2pi/p. The basis also has free-energy and total-occupation cutoffs. Charge and total momentum sectors are enforced exactly.

The unchanged dimensionless couplings are g/mPhi=0.002168, lambda=0.00881292 and M/mPhi=2 sqrt(1+0.02²). Constant-H evolution uses spectral propagation; the reusable solver also implements unitary exponential-midpoint propagation for a time-dependent scale factor. In canonical conformal radiation-era variables,

\[
H(a)=H_0+(a^2-1)\left[m^2\int:\!\Phi^\dagger\Phi\!:
+M^2\int:\!X^\dagger X\!:\right]+agH_3+\lambda H_4.
\]

Here H0 uses reference a=1 free frequencies, and H3,H4 have their couplings factored out. Time-dependent vacuum constants are consistently omitted; this changes only an overall state phase, but they would need attention when assigning renormalized cosmological energy. Inflationary curvature terms and a full source density matrix are not implemented by this radiation-era expression.

The full state is evolved. No Gaussian factorization of its connected correlations, thermal matching time, or appended collision rate is used. Both directions of every retained process arise from the same Hermitian Hamiltonian.

## Absorption and inverse without an added collision term

The new reaction is X+Phi+antiPhi -> Phi+Phi. The benchmark uses its threshold incoming momenta and outgoing momenta satisfying energy conservation. These few-particle states are scattering validation inputs, not a proposed cold seed or replacement for the cosmological source.

We independently compared old-fashioned Hamiltonian perturbation sums against the previously derived covariant tree amplitude. With i,f the initial/final Fock states and R=(Ei-H0)^-1 excluding degenerate denominators, the tested terms are

\[
g\lambda\langle f|(H_3RH_4+H_4RH_3)|i\rangle,
\qquad
g^3\langle f|H_3RH_3RH_3|i\rangle.
\]

For this transition the excluded degenerate intermediates have zero contribution to these sums. No generic real-intermediate-state subtraction rule is inferred from that fact.

At a free-energy cutoff of 12 mPhi, both terms agree with the independently normalized covariant expressions to 4.5e-16 relative:

| Contribution | Hamiltonian matrix element, units mPhi |
|---|---:|
| g lambda | -3.58113889772417e-9 |
| g cubed | +4.77315476079243e-13 |

The full Hamiltonian evolution also gives identical forward/inverse transition probabilities within 8.3e-25 absolute, norm error below 2.7e-15 and fixed-H energy drift below 7e-15 relative in the original benchmark. These are finite-basis numerical checks, not a continuum reaction-rate measurement.

**Important cutoff finding:** at cutoff 8 mPhi, the mixed amplitude is wrong by 33.34%; at cutoff 10 mPhi, the cubic amplitude is still wrong by 11.11%. Virtual intermediate states must be retained even when barely populated. A small population at the upper occupation/energy boundary is not by itself a convergence certificate.

No absorption-rate term was added to H. Its agreement with the independently derived amplitude tests that the elementary vertices already generate the process, so adding that same rate to this exact finite-Hamiltonian evolution would count it twice.

## Other loss channels checked

The same Hamiltonian reproduces, to 8.9e-16 relative:

- X antiX -> Phi antiPhi at leading order g²;
- Phi 4-to-2 in the 3-plus/1-minus channel at leading order lambda²;
- Phi 4-to-2 in the 2-plus/2-minus channel at leading order lambda².

The checks include normalization of identical zero-momentum incoming Fock states. The Hamiltonian contains further virtual processes as allowed by its basis, but the full cubic-containing 4-to-2 amplitude and its continuum limit were not independently validated in this run. Inverse processes are supplied by the same Hermitian operator, rather than an independently chosen loss term.

## Non-Gaussian correlation evolution and numerical validation

`audit_quantum_fock_evolution_v2.py` calculates the connected two-time X-number correlation

\[
C(t,t')=\langle N_X(t)N_X(t')\rangle
-\langle N_X(t)\rangle\langle N_X(t')\rangle,
\quad F_N=\mathrm{Re}\,C,\quad\rho_N=-2\mathrm{Im}\,C.
\]

The statistical function is symmetric, the spectral function antisymmetric, and the equal-time statistical function agrees with an independently evaluated number variance within 3e-15. A nonzero spectral correlation is retained; populations alone are not substituted for the quantum state. These are number-operator correlations, not a completed field-propagator/self-energy solver.

Raising the energy cutoff from 12 to 14 mPhi (occupation cutoff 10) increases the benchmark basis from 286 to 655 states. The maximum difference between absorption-probability histories, normalized by the maximum probability on the finer run, is 2.075e-5 over the tested interval t mPhi=0..10000. This is a comparison of two energy cutoffs at fixed momenta; momentum/volume continuum convergence has not been established.

A separate time-dependent test compares exponential-midpoint propagation against an adaptive DOP853 solution. Halving the step reduces state-vector error from 3.6993e-5 to 9.2630e-6, as expected for second-order propagation. The scale factor in this check is a numerical test function, not the high-H cosmological history.

An interacting ground-state test remains stationary in probability to 1.43e-12. This matters because evolving a bare free vacuum under a suddenly switched-on interacting Hamiltonian would produce a quench response; that must not be mislabeled spontaneous cosmological production.

## Why no surviving abundance follows yet

The original high-H source has large coherent displacements and many squeezed modes. It is outside the low-occupation benchmark space. For an orthonormal zero-mode quadrature with conformal effective hbar lambda, any oscillator reference frequency omega obeys

\[
\langle N\rangle\ge
\frac{L^3}{2\lambda}\left(\omega\bar q^2+\frac{\bar v^2}{\omega}\right)
\ge\frac{L^3|\bar q\bar v|}{\lambda}.
\]

Using the saved source means, this last bound is approximately 741436 for the first Phi real component and 922834 and 73247 for the two X components. This is a **representation bound in an undisplaced conformal oscillator basis**, not a measured physical particle abundance for super-Hubble fields. A displaced/squeezed basis can remove this particular cost; it does not remove the many-mode nonlinear correlation problem or provide an error-controlled truncation automatically.

The source was therefore not loaded into a state cutoff of eight or ten particles. Doing so would silently replace the physical initial conditions. The three-momentum finite box also has coherent recurrences and cannot supply a continuum thermalization or freeze-out rate. No entropy fit, cold-fraction threshold or matching epoch was used to conceal these limitations.

The remaining work is a large-occupation, many-mode treatment that preserves the verified interaction content, the source's quantum initial conditions and consistent renormalization, followed by tests of actual bath formation and subsequent cooling. A displaced/Bogoliubov basis or a conserving correlation closure is a plausible continuation; neither has been implemented and validated here. The exact finite-mode code now provides a non-Gaussian benchmark against which such approximations can be tested.

## Files, provenance and failures retained

- `quantum_fock_solver.py`: original-action Hamiltonian construction and unitary evolution.
- `test_quantum_fock_solver.py`: vertex-normalization, charge/momentum and Hermiticity checks; three tests pass.
- `quantum_fock_benchmark_run/manifest.json`: completed, absorption amplitude and unitary reaction benchmark.
- `quantum_fock_evolution_audit_v2_run/manifest.json`: completed, two-time correlations, independent evolution check, cutoff comparison and source representation audit.
- `quantum_collision_channels_v2_run/manifest.json`: completed, pair and contact number-changing amplitude checks.

The initial `quantum_fock_evolution_audit_run` is preserved as failed: its ground-state stationarity error 1.43e-12 exceeded a 1e-12 test threshold. Version 2 explicitly adopts the 1e-10 unitary-propagation tolerance already used by the main benchmark; the computed error is unchanged. The first `quantum_collision_channels_run` failed while serializing a NumPy Boolean; version 2 converts the flags to native Booleans. Neither failure was silently overwritten.

**Status:** the original interactions, new absorption channel and its inverse are realized and checked in a nonlinear quantum benchmark. Cosmological bath formation, cold survival and a seed-free abundance remain unresolved. No new abundance is claimed.
