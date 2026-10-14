# Conditional finite-pulse preparation of a confined carrier pair

Parent checkpoint: dad0237903cba9e520577414567139ac0f9f1651.
This advances the preparation subproblem, not the existence or empirical
admissibility of the hypothetical cold sector. Previous user-facing 94%
preliminary result is now reproduced with a bounded, hash-recorded run.

## Model and derivation boundary

Use the silica-shell source and ground orbital from the parent package:
a=2 cm, shell thickness 5 mm, carrier mass 1 eV, prescribed intensity
1e12 W/m^2 in each counterpropagating wave. The optical mode through the
shell and achievable power remain unverified. The single-carrier tunneling
lifetime is 3.17578 s, not a total physical lifetime.

For one fixed orbital per charge sign, let a,b be boson annihilation operators.
Use the following rotating-frame Hamiltonian in angular-frequency units:

    H/hbar = J[na nb-(na+nb)/2]
             + K[na(na-1)+nb(nb-1)]
             + Omega f(t)(a†b†+ab).

Here Omega=8.70627/s, J=-157.30417/s and K=1.08498e-7/s.
The number-linear subtraction tunes vacuum-to-one-pair resonance.
The single-pair resolvent self-energy contributes to J: annihilating an
opposite-sign pair has squared matrix element proportional to na nb.
Using the SAME denominator and fixed spatial orbitals for every occupation
is an additional instantaneous second-order approximation. The parent
single-pair calculation does not prove the whole many-body Hamiltonian.

For the parent's parameters mu^2=lambda M_R^2, the opposite-sign contact
coefficient is 3 lambda/(4m^2) times the orbital fourth-power integral.
The coefficient multiplying each same-sign n(n-1) is lambda/(8m^2)
times that integral, giving K=D/(6 hbar), where D is the parent's contact
shift. Resonant opposite-sign exchange is included in J, not added again
to that contact coefficient.

Evolve the density operator with Lindblad jumps a/sqrt(tau), b/sqrt(tau).
States with unequal occupations are retained after one carrier escapes.
No other loss channels are included. The drive has 5 ms half-cosine rise
and fall, a flat plateau, and total duration 0.185421246 s, chosen so
Omega times its integrated envelope equals pi/2.

## Numerical findings

| Assumed interaction | Probability of exactly one retained pair |
|---|---:|
| Half J, other inputs fixed | 0.920304 |
| Baseline J | 0.938176 |
| Twice J, other inputs fixed | 0.942539 |
| Baseline J, no tunneling | 0.994270 |

Baseline final probability in unequal-occupation states is 0.055118;
in higher balanced pairs 0.002525; vacuum 0.004181. These are mutually
exclusive final populations, not histories of individual loss events.

The attractive effective interaction detunes additional pairs: the
one-pair to two-pair diagonal frequency difference is 2J+4K, about
-314.6/s, whereas its drive matrix element is 2 Omega=17.41/s.
This suppresses higher occupations in the chosen orbital. It is not a
proof against excitation of other orbitals or other many-body states.

An independent analytic comparison shows why the interaction is important.
For J=K=0 and no loss, the state is a two-mode squeezed vacuum:

    q=tanh(A)^2, A=Omega integral f(t)dt,
    P(n,n)=(1-q)q^n,
    P(1,1)=q(1-q)<=1/4.

At A=pi/2, P(1,1)=0.133604 and mean particle number is 10.59195.
That comparison changes both interaction and loss; it is not a numerical
prediction for the lossy noninteracting apparatus. The bound follows from
q(1-q)=1/4-(q-1/2)^2. Strong one-pair selectivity is therefore a conditional
interaction effect, not a generic consequence of resonant illumination.

## Elimination and pulse leakage diagnostics

The mediator gap gives a memory timescale 0.591 microseconds, or 1.18e-4
of the ramp time. The one-pair nonlinear shift is 9.29e-5 of the gap;
25 times that scale, covering na nb at the cutoff, is 0.00232 of the gap.
These are scale-separation diagnostics, not rigorous error bounds on the
eliminated many-body dynamics.

For the compact half-cosine pulse, the total variation of its second
derivative, including endpoint jumps, is 4 pi^2/ramp^2. Three integrations
by parts in the distributional sense bound its Fourier transform by
4 pi^2/(ramp^2 |frequency|^3). Applying this to the free mediator continuum
with minimum angular detuning gap/hbar, and using Parseval for the assigned
spatial optical source, bounds direct free-mediator excitation by
2.56e-18 expected particles. This covers the direct linear optical source
only, not all pump-assisted transitions, pair-mediated processes or losses.

## Verification and limitations

The bounded runner completed and the manifest validates against current
inputs and outputs. There are 37 recorded tolerance checks, including
sampled density-matrix trace, Hermiticity, positivity and charge symmetry;
a two-level pi-pulse control; a small-area analytic squeezing control;
and occupation-cutoff and ODE-tolerance comparisons. Baseline cutoffs
3 versus 5 differ in P11 by 5.46e-8; tightening the ODE tolerance changes
it by 1.35e-11. The baseline cutoff boundary population is 2.78e-15.
Positivity is sampled, not a rigorous continuous-time numerical guarantee.
The factor-two sensitivity runs use cutoff 5 without separate refinement;
their tiny final boundary weights alone are not a convergence proof.

No new Lean certification is claimed. Numerical checks do not establish
particles, material response, optical feasibility, or a gravitational device.
Remaining preparation obligations include a multimode derivation/test of
the effective interaction, full electromagnetic boundary conditions and
additional dissipative channels. In particular, the assumption that all
created pairs occupy the selected ground orbitals requires a spectral
check of other pair transitions. That is the next discriminating calculation.
The larger goal remains open, including empirical constraints and whether
this microscopic sector can represent the repo's cosmological component.

Authoritative inputs, command, caps and output hashes are in run/manifest.json;
full numerical populations and diagnostics are in run/results.json.
