# Continuum and nuclear calculations: what has actually been derived

## Coulomb scattering problem

We keep atomic units a_D=hbar/(m_C c alpha), E_D=m_C c²alpha², and the
charge assignments X:+Q, C:−Q. At clamped internuclear separation R, two
spin1/2 electrons interact through the full Coulomb repulsion and exchange.
The inner wavefunction includes antisymmetrized ionic-target x continuum
configurations and two-electron square-integrable configurations. The target
is the complete18-orbital aug-cc-pVDZ one-electron space, giving18 ionic states.
The electronic continuum is represented by center-of-mass B splines and real
spherical harmonics. UKRmol+ generates the inner Hamiltonian, boundary
amplitudes, R matrix, and Coulomb-matched open-channel K matrix.

All current scattering runs use singlet Ag symmetry in D2h and a20-bohr sphere.
Ag contains several axial angular-momentum sectors; it must not be relabeled
as a complete Sigma calculation or a spin-averaged total cross section.
Target nuclear mass does not enter the clamped calculation. It DOES enter
nuclear scattering and the final mass-ratio100 rate; ordinary-H rates are not
imported here. Nuclear spin statistics and full symmetry sectors remain open.

UKRmol writes the symmetric K upper triangle by columns. It reports collision
energies in Rydbergs; we divide by2 for Hartree atomic units. The Coulomb-relative
open-channel matrix is
 S=(I+iK)(I−iK)^−1.
Its symmetry, unitarity and eigenphase sums are checked. The independent UKRmol
eigenphase output can differ by multiples of pi; comparison must be modulo pi.
This does not include the divergent forward pure-Coulomb amplitude in a total
elastic cross section. No finite total Coulomb collision rate is inferred.

At fixed nuclei, below electronic thresholds, all channels in this calculation
are elastic. Numerical 1−S†S is NOT a dissociative-recombination probability.
It must never be clipped into a positive artificial reaction source.

## Integral and propagation errors matter even when S is unitary

The continuum partial-wave cutoff is DIFFERENT from the multipole order used
in evaluating mixed Gaussian/B-spline integrals. Reducing the latter to8 caused
unphysical deep inner poles, despite correct one-electron target energies and
unitary output S matrices. These data and their apparent resonances are rejected.
A Gaussian-only two-electron calculation with the same stored integrals matches
PySCF; the problem emerges when continuum mixed integrals enter. Restoring order15
removes the deep poles; order20 tests the remaining integral error. This isolates
an inadequate numerical integral approximation, not a new physical bound state.

The first automatic outer propagation also selected too few intervals. Explicit
approximately one-bohr intervals substantially improve matching-radius stability.
Inner basis, integral multipoles and outer propagation are independent checks.
Passing one cannot establish the others. Every successful executable run is
therefore classified separately from its physical/numerical acceptance.

## Actual bound-state nuclear derivative couplings

For four real spin-singlet Ag FCI states, compute wavefunctions at R and R±h.
The cross-geometry molecular-orbital overlap is
 O(R,R')=C(R)^T S_AO(R,R') C(R').
For one alpha and one beta electron, the CI overlap is
 <Psi_i(R)|Psi_j(R')>=sum_abcd CI_i(ab) O_ac O_bd CI_j(cd).
This includes movement of the Gaussian centers. Ignoring that movement would
compute the wrong nuclear derivative. Signs at R±h are aligned to states at R.

 d_ij=<Psi_i|partial_R Psi_j>
      approximately [<Psi_i(R)|Psi_j(R+h)>−<Psi_i(R)|Psi_j(R−h)>]/(2h),
 g_i=||partial_R Psi_i||²
      approximately [2−2<Psi_i(R−h)|Psi_i(R+h)>]/(4h²).
The overlap matrix at equal R is checked against identity. Antisymmetry error
d+d^T decreases by about4 on halving h; the ground metric changes by less than
5e−6. The four-state omitted derivative norm is
 g_i−sum_{j in four states}|d_ji|².
At R2 this is about56% of the ground metric. That is a norm-completeness result,
not a56% error estimate for a reaction rate. Higher states and continuum response
are missing. The finite Gaussian-basis pseudostates are not continuum-normalized.

For nuclear reduced mass mu_N=50, the radial nuclear kinetic operator has terms
 −[delta_ij partial_R²+2d_ij partial_R+tau_ij]/(2mu_N).
A complete basis would relate tau to d' and d². The four-state projection cannot
silently use that completeness identity. The reported `ground_DBOC` is ONLY
the radial contribution g_0/(2mu_N), about.001962 at R2, not the complete
finite-mass adiabatic correction including other nuclear coordinates.

Finite differences of corrected S(R,E) provide another nuclear-response
diagnostic, at FIXED ELECTRON KINETIC ENERGY. A fixed-total-energy frame
transformation requires the R-dependent ionic threshold shift as well.
No complete nuclear scattering matrix is obtained by identifying these two.

## Resonances and reaction rates

Energy scans can identify electronic resonance candidates from the unwrapped
sum of eigenphases. A local Breit–Wigner fit, if used, extracts numerical pole
parameters from the computed amplitudes; it does not introduce a freely fitted
astrophysical rate. Candidate widths must survive integral/basis/energy-grid
checks and overlapping-resonance ambiguities before use. Rejected order8
candidate scans remain archived with their failure classification.

Physical DR requires nuclear outgoing flux on neutral dissociation channels,
including spin and product branching, or an equivalent validated multichannel
quantum-defect/frame-transformation treatment. Those amplitudes are NOT yet
computed here. Even a valid fixed-R electronic width is not the nuclear DR rate.
No finite physical chemical coefficient is passed to the photon solver.

The dimensional rate prefactor remains a_D³/t_D=hbar²/(m_C² c alpha), with
no independent tunable normalization. The dimensionless reaction probability
still has to be computed. Excited product atoms also change the heat defect:
 T_b+C -> A(n)+A(m) releases 1/(2n²)+1/(2m²)−.5−D_b
in the previous leading-BO convention. The old photon/collision adapter covers
only n=m=1; using it for all branches would violate the intended energy ledger.
The full reaction network and nuclear outgoing boundary problem therefore
remain prerequisites for a physical disk/dwarf/cluster test.
