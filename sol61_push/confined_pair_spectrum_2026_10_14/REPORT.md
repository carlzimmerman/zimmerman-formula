# Spatial-spectrum check for conditional pair preparation

Parent: 6f1855a23e4765bad7b1832bb780d9586166c692.
The preceding preparation result assumes a single spatial orbital per charge
sign. This calculation tests for nearby competing independent-particle pair
levels. It does not establish the full interacting multimode dynamics.

## Reference problem

Retain a=2 cm, m=1 eV and silica barrier U=2.85732356519e-8 eV.
As in the parent ground-orbital calculation, the exterior barrier extends to
infinity. This is a reference well, not the actual finite-shell scattering
problem. For each angular momentum l, match the regular interior spherical
Bessel function to the exterior decaying modified spherical Bessel function:

    x j_l'(x) k_l(b) - b k_l'(b) j_l(x) = 0,
    x = a sqrt(2m E), b = sqrt(z^2-x^2), z = a sqrt(2m U).

Lengths here are in natural units. Numerically divide the determinant by
k_l(b) to improve scaling; do not divide by j_l(x), which would introduce
poles in the root search. For l=0 the independent elementary check is
x cot(x)+sqrt(z^2-x^2)=0.

The search samples 4000 and 8000 radial points for each l=0,...,25 and
brackets sign changes. Both resolutions find 75 radial/angular multiplets,
1009 states counting magnetic degeneracy. This is an enumerated finite search,
not a certified root count. Large l need not be searched indefinitely:
if l(l+1)>=z^2, the centrifugal potential inside r<=a already exceeds U,
while outside the total potential exceeds U. Such l have no bound levels
below U. The angular cutoff used here covers that condition.

## Nearby pair energies

All energies below are excess above the two rest masses. Excited-pair energies
are bare sums of reference orbital energies; the target is the parent's
*dressed* ground pair at 8.85815922883e-10 eV.

| Pair orbitals (l,n) | Bare excess energy, eV | Detuning / hbar, per second |
|---|---:|---:|
| (0,1) and (1,1) | 1.34898442638e-9 | 703676.8 |
| (1,1) and (1,1) | 1.81204939040e-9 | 1407196.4 |

The stipulated optical source and spherical wall are invariant under spatial
inversion. The source therefore couples vacuum only to even total parity:
l1+l2 must be even. The first row is forbidden in that symmetric model.
Axisymmetry additionally requires the sum of magnetic quantum numbers to
vanish. The second row has combinations satisfying both conditions, although
symmetry permission alone does not calculate their amplitudes. Imperfections
can break these selection rules.

The lowest symmetry-allowed reference gap is 9.26233e-10 eV, about 8950
times the magnitude of the calculated ground-pair self-energy. Its angular
detuning is about 162000 times the assigned ground-pair drive of 8.706/s.
These comparisons support spectral separation; they are not bounds on other
channels' interaction shifts or their source matrix elements.

## Pulse diagnostic and its limit

For a weakly driven isolated competing channel with drive frequency g_j,
fixed vacuum amplitude and angular detuning w_j, first-order perturbation
theory gives amplitude -i g_j integral f(t) exp(i w_j t) dt.
For the parent's half-cosine pulse, integration by parts gives

    P_j <= |g_j|^2 [4 pi^2/(ramp^2 |w_j|^3)]^2.

For the lowest even-parity competitor, the coefficient multiplying |g_j|^2
is 3.21152e-25 s^2. We have NOT calculated g_j here. This is not a total
population bound: the vacuum is strongly depleted in the actual proposed
pi pulse, and interactions mix channels. Replacing its time-dependent
vacuum amplitude by one is inappropriate for a rigorous leakage estimate.
This diagnostic also does not sum the continuum or all excited states.

## Evidence and next implication

85 tolerance checks pass. They include root-grid refinement, determinant
residuals, independent elementary s-wave matching, and agreement with the
parent ground energy. The manifest validates recorded input/output hashes.
These numerical checks do not certify physics or exact spectral completeness;
no new Lean theorem is claimed.

The bare reference spectrum does not reveal a near-degenerate competitor.
The next calculation must evaluate the actual optical and mediator overlap
matrices for the lowest symmetry-allowed excited pairs and propagate them
with the ground pair, including vacuum depletion. That will distinguish
true suppression from the misleading use of an undepleted-source Fourier
bound. Finite-shell losses of excited modes and the complete electromagnetic
mode remain separate obligations. The overarching creation goal stays open.
