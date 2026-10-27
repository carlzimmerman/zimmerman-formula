# Source depletion emerges from a unitary source–pair calculation

2026-10-12. The preceding turn bounded feedback for an imposed exponential
source amplitude. This turn removes that imposed time dependence in a
finite near-resonant one-source/pair model. The same 1 MeV daughter example
is used. This is a substantive production check, not a halo calculation.

## Closed Hamiltonian and matching

Use a source state |s> and orthogonal daughter-pair states |j> spanning a
finite continuum window. Measure pair energy relative to M in units of the
saved vacuum width Gamma, and time in tau=Gamma*t/hbar. The Hamiltonian is

    H/Gamma = b |s><s| + sum_j x_j |j><j|
                 + sum_j v_j (|s><j|+|j><s|),
    v_j=sqrt[J(x_j) dx],
    J(x)=Gamma_vac(M+Gamma*x)/(2pi Gamma_vac(M)).

Here Gamma_vac(E)=g² sqrt(1-4m²/E²)/(8pi E), evaluated on a near-resonant band.
This matches the on-shell spectral density to the candidate's tree width.
Its off-shell continuation is a declared effective-model choice, not a full
relativistic propagator derived with all counterterms. The width sets the
coupling strength; no imaginary damping term or prescribed source decay is
inserted in H.

Set b=sum_j [(J(x_j)-J(0))/x_j] dx. On a symmetric grid this is the finite-band
principal-value subtraction that makes the real continuum self-energy vanish
at the reference resonance. The Hamiltonian remains Hermitian. This matching
choice is explicit; b is not adjusted to fit a survival curve.

Initially the state is |s>. Matrix-exponential evolution then determines both
source depletion and daughter-pair amplitudes, including coherent returns
within this model. All basis states have total charge two. The conserved
energy includes source–pair coherence; particle kinetic energy alone need not
be conserved during the transfer. The physical rest-energy offset can be
added back without changing the dynamics.

## Finite-band and grid checks

The half-bandwidth L runs from 50 to 400 source widths. At the largest L the
pair energy lies within about 0.341 eV of M, well above the physical daughter
threshold at M-2m about 100 eV below M. The calculation resolves the resonant
region but does not include that actual threshold or the full ultraviolet
continuum. Grid spacings dx=0.2 and 0.1 give recurrence scales approximately
31.4 and 62.8 lifetimes; evolution stops at ten lifetimes, before these scales.

| L | dx | Pair modes | Source survival at tau=1 | At tau=5 | At tau=10 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 50 | 0.2 | 500 | 0.370182 | 0.00660503 | 4.30310e-5 |
| 100 | 0.2 | 1000 | 0.369032 | 0.00667312 | 4.42972e-5 |
| 200 | 0.2 | 2000 | 0.368457 | 0.00670601 | 4.48365e-5 |
| 400 | 0.2 | 4000 | 0.368170 | 0.00672193 | 4.51094e-5 |
| 400 | 0.1 | 8000 | 0.368170 | 0.00672193 | 4.51096e-5 |

At the finest grid, daughter-pair probability at ten lifetimes is
0.9999548904. Ten nominal lifetimes are 7.7117e-12 seconds. These are
probabilities in the one-source/pair sector, not a demonstrated many-source
cosmological yield. The repeated digits show finite-grid precision only.

The maximum sampled absolute deviation of survival from exp(-tau) decreases
from 0.00902 at L=50 to 0.00140 at L=400. This is bandwidth convergence toward
the weak-decay expectation over the tested interval, not a certified error
bound for the omitted physical continuum. At L=400, halving dx changes the
survival at tau=5 by about 2e-9.

Probability conservation error is below 1.1e-14 across all runs; total
Hamiltonian-energy error is below 3.5e-15 in width units. Those tests verify
unitary numerical evolution, not the completeness of the Hamiltonian.

## What is now better supported

The dilute branch no longer relies solely on assuming that the source
amplitude follows a vacuum exponential. A closed, explicitly coupled model
with the matched resonant spectrum gives essentially complete pair transfer
on the expected timescale and reproduces that exponential increasingly well
as the spectral band widens. This complements the small-occupation and weak
inverse-feedback checks in DILUTE_FEEDBACK.md.

The daughter energies in this band remain close to the near-threshold cold
kinematics. The positive-square action's conserved charge and excess-energy
structure supplies the separate broader coldness argument; a probability
transfer calculation alone does not prove a pressure theorem.

## Remaining limits and evidence

`dilute_unitary_decay.py` and its contract specify the Hermitian star model,
on-shell matching and test interval. All 18 checks pass. Its run manifest
validates recorded code and parameter inputs. The physical spectral threshold,
far tails and source preparation are not resolved by this finite window.
The model also omits daughter quartic rescattering, other multi-particle sectors
and interactions among many prepared sources. The dilute occupation bound
motivates their study as corrections; it does not make them disappear.

The next production refinement is to include the actual threshold/continuum
or bound its memory corrections, and to test the omitted interaction channels
in this dilute regime. This is a conditional way to populate a cold carrier
from a prepared charged source. It still does not supply that source's origin,
a cosmological abundance prediction, the repo's halo attractor or its
baryon/vacuum-dependent acceleration normalization.
