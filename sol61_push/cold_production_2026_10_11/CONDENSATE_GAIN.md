# Initial condensate gain from the produced shell

2026-10-11. The preceding turn removed a tree-amplitude cancellation and
verified production with alpha=2. This turn evaluates the corresponding
initial gain integral. It changes an amplitude-level possibility into a
conditional kinetic growth coefficient; it does not complete the evolution.

## Result

For a fixed, dephased daughter spectrum taken from the x=200 homogeneous
Gaussian output, with modes outside the produced band initially empty:

| Candidate | Initial zero-mode gain coefficient | Fixed-bath e-folding time |
| --- | ---: | ---: |
| Original alpha=1 | 0.000369221 /s | 2708.41 s |
| Revised alpha=2 | 184.7601 /s | 0.00541242 s |

The revised coefficient is about 500,000 times larger. Both signs are positive.
These times describe small zero-mode occupation in the stipulated bath, not a
condensate fraction, formation time, or permanent yield. In particular, the
finite-volume occupation reaches a macroscopic density only after its volume,
initial seed, depletion and inverse reactions are accounted for.

## Kinetic derivation and normalization

Write the daughter interaction as k psi†² psi² with k_eff depending on pair
invariant energy, matched to the same tree-level source-exchange amplitude.
A collision 1+2 <-> 0+3 has p_3=p_1+p_2, and at leading nonrelativistic order
energy conservation with the zero mode requires p_1.p_2=0. With outgoing
zero-mode occupation N_0 and cloud occupation f(epsilon), a fixed-bath equation
is

    dN_0/dt = A_plus (N_0+1) - A_minus N_0,
    A_plus = (2m³/pi³) integral dE1 dE2 k_eff² f1 f2 (1+f3),
    A_minus = (2m³/pi³) integral dE1 dE2 k_eff² (1+f1)(1+f2) f3,
    E3=E1+E2.

The displayed rates are in natural units; divide by hbar for /s. To fix the
normalization, the distinct-mode matrix element is 4k/V. Golden rule and
unordered cloud-pair counting give 2pi*(4k)²/2. The momentum delta function
sets p3=p1+p2, and the energy delta integrates the relative angle with factor
m/(p1 p2). Thus the remaining two-particle phase-space integral is
m/(8pi^4) integral p1 p2 dp1 dp2, giving the stated coefficient after
p dp=m dE. The same convention gives the identical-boson threshold cross
section sigma=2m²k²/pi=lambda_eff²/(8pi m²).

The exact invariant when one outgoing daughter rests is s=2m(2m+E1+E2).
The numerical diagnostic uses exact one-particle kinetic energies, their
quadrature Jacobian and this invariant in k_eff, while retaining the leading
NR phase-space coefficient. It is a controlled small-velocity approximation
at the shell speed 0.01c, not a fully relativistic collision calculation.
For alpha=1, the narrow cancellation makes small effects comparatively more
important; the finite radial width dominates the saved diagnostic rather
than the exact-shell residual alone.

In a thermal Bose cloud with zero chemical potential, f1 f2(1+f3) equals
(1+f1)(1+f2)f3. Therefore a generic equilibrium cloud has zero net gain, even
when both gross rates are large. The code independently checks this identity.

## Reconstructing the initial cloud

The saved production variables satisfy F_j=w_j f_j, with

    w_j=m³ epsilon q_j dv_j/(4 pi² n_source_initial),
    q_j=p_j/m.

The script reconstructs occupations, verifies their number density against
2*n_source_initial*sum(F_j), and evaluates the two-energy integral on each
saved quadrature. For every sampled pair E1+E2 lies above the populated
production band. Under the declared zero-exterior assumption f3=0, so the
initial inverse coefficient vanishes and A_plus is positive. This does not
mean that f3 stays empty after collisions: each gain event also creates an
energetic escort daughter there.

The bath is treated as incoherent, with no anomalous pair covariance or
moving-source correlations in the collision operator. The Gaussian output
itself is a correlated squeezed state. No physical dephasing or quantum-to-
kinetic handoff is established by reconstructing its occupation numbers.
A large source-mode occupation, coherent memory, or medium-induced spectrum
shift could require a different dynamical treatment.

## Checks and limitations that decide the next step

Four production runs per candidate test 512/1024 nodes, the wider 1536-node
band, and tighter time tolerance. Gain rates agree within the declared 1e-4
relative threshold (actual displayed agreement is much closer). Independent
checks cover density reconstruction, constant-kernel factorization, empty
escort-band kinematics and thermal detailed balance. All 33 finite checks
pass, and `condensate_gain_run/manifest.json` validates current provenance.
These are implementation checks, not validation of the kinetic handoff.

For alpha=2, hbar*A_plus divided by the weighted rms shell energy width is
1.26e-8. The rate is therefore slow compared with the inverse shell energy
spread, a useful necessary timescale separation for a Markov description.
It does not demonstrate loss of the actual pair correlations. The gain/H
ratio on the inherited radiation background is 8.82e9, but expansion is not
the only competing process.

Crucially, the earlier moving-source response becomes appreciable on the
nanosecond production timescale in a frozen-shell forcing approximation.
That calculation is not a nonlinear source fraction, but it directly warns
that the assumed cloud can change long before a 5.4-millisecond gain time.
Thus it would be incorrect to integrate N0=exp(A_plus*t)-1 through a putative
condensation episode while freezing this particular production output.
The revised channel remains useful; the whole initial spectrum must be evolved.

The next decisive model must couple daughter momentum redistribution,
condensate occupation, energetic escort modes and moving-source reactions,
with charge and energy conserved and inverse reactions retained. The early
coherent phase and subsequent kinetic phase require a justified match. Real
source conversion and resonant elastic exchange must not be double-counted.
The 97-98% ideal endpoint remains a candidate destination, not an attained
state. None of this yet supplies the repo's halo attractor or acceleration
normalization.
