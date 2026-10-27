# Retention, detuning and drift requirements for the lower-power route

Parent checkpoint: 0aa08d9329761b7baecccaa68d641639dbbd6080.
The assigned lower-power point does not require the full multi-day ideal
storage lifetime to give nonzero useful-scale model probabilities. It does
require narrow frequency matching. This package quantifies both requirements;
it does not demonstrate either or establish the hypothetical carriers.

## Fixed benchmark and independent control parameters

Retain 628.3185 W circulating in each wave, Omega=0.0008706271/s,
pulse duration 1804.21246 s and assigned common-laser Lorentzian linewidth
1 mHz. The four-state model includes vacuum, pair and two single-carrier
states. Dephasing gamma=4 pi times the common-laser linewidth is unchanged.

Vary the independent single-carrier lifetime tau, or a constant common-laser
frequency offset delta nu. The pair Hamiltonian diagonal offset is
Delta=4 pi delta nu. In the stationary equations, coherence damping is
kappa=gamma+1/tau and the stimulated population-transfer coefficient is
W=2 Omega^2 kappa/(kappa^2+Delta^2). Therefore

    Ppair,steady=Omega^2 kappa /
        [(kappa^2+Delta^2)/tau+4 Omega^2 kappa].

Independent linear-system solutions verify this expression. Finite pulse
probabilities are obtained by exponentiating the full density-matrix generator,
not by substituting the stationary result.

The retention sweep changes only the prescribed leakage rate. A real change
to the material barrier would also change orbitals, detuning and source overlap;
that joint uncertainty propagation is NOT done here.

## Retention requirement

At zero mean detuning, pair probabilities after 1804.2 s are

| Single-carrier lifetime | Retained pair probability |
|---|---:|
| 100 s | 0.003314 |
| 220.7 s | 0.009416 |
| 1000 s | 0.046733 |
| 10000 s | 0.145014 |
| 100000 s | 0.169654 |
| 527482 s | 0.172144 |

A bracketed solve gives tau=2965.33 s, about 49.4 minutes, for probability
0.10. This 10% value is an explicitly chosen diagnostic threshold, not a
redefinition of the research goal or an experimental detection criterion.
It is a SINGLE-carrier lifetime; independent pair survival has rate 2/tau.

The 220.7 s row is near the earlier half-barrier tunneling lifetime only as
a numerical comparison. It is not a recomputed half-barrier preparation
prediction. The result shows why complete material/loss characterization
matters, and why assuming days of retention is stronger than necessary for
this particular finite-time probability target.

## Frequency matching

At the original ideal tunneling lifetime, a common-laser offset of
1.143418 mHz reduces the finite-time probability to half its on-resonance
value. This is the halfwidth of the PREPARATION response, not the assigned
laser spectral linewidth. Its corresponding pair-energy mismatch is
9.45759e-18 eV. Relative to an approximately 1 eV laser photon, the frequency
halfwidth is 4.72880e-18.

| Constant common-laser offset | Retained pair probability |
|---|---:|
| 0 | 0.172144 |
| 0.1 mHz | 0.170827 |
| 1 mHz | 0.097499 |
| 10 mHz | 0.002235 |
| 100 mHz | 0.00002265 |

A separate linear sweep centered on resonance includes slow deterministic
drift in addition to the assigned fast phase diffusion. A total 1 mHz sweep
over the pulse gives 0.164235; a 10 mHz sweep gives 0.056726. The assumed
sweep crosses the TRUE resonance at the midpoint. These results do not supply
a way to know where that resonance is.

## Leading geometry diagnostic

For the reference s-wave orbital, let x=a sqrt(2mE0)/(hbar c),
z=a sqrt(2mU)/(hbar c), beta=sqrt(z^2-x^2), and
F=x cot(x)+beta=0. At fixed barrier U,

    F_x=cot(x)-x csc(x)^2-x/beta,
    d ln(E0)/d ln(a)=2[-z^2/(beta x F_x)-1].

The leading bare pair derivative is 2 dE0/da=-8.50540e-8 eV/m.
Dividing the response energy halfwidth by its magnitude gives a radius change
of 1.11195e-10 m, or 0.111 nm. This is a sensitivity diagnostic with fixed
laser frequency, not a universal mechanical-stability requirement: tracking
the resonance can compensate changes if a usable error signal exists.
Derivatives of pair self-energy, material potential and other shifts are
excluded. Thermal expansion and refractive-index changes have not been
converted to temperature specifications here.

## What remains unresolved

The narrow response cannot be justified by simply writing m=1 eV and tuning
a laser to that assumed number. The microscopic mass, material shift and
interacting resonance have not been measured to the required accuracy.
An experimental route needs a resonance search and observable readout or
feedback signal. A small assumed linewidth is not evidence of correct mean
frequency, stable cavity geometry or an identifiable dark-pair signal.

Twenty numerical checks cover the inherited baseline, finite-time thresholds,
positive/negative detuning symmetry, detuned stationary formula, ODE refinement
for linear sweeps, comparison of ODE and matrix exponential, and aggregate
density-matrix invariants. The bounded-run manifest validates its inputs and
outputs. The orbital sensitivity is an analytic implicit-differentiation
diagnostic, not a new Lean-certified material model.

This sharpens the lower-power requirements: order-hour total retention can
be sufficient for the chosen 10% benchmark, while millihertz frequency
matching and an observable resonance remain central challenges. Readout and
resonance acquisition should be investigated before treating long coherent
pulses as an experimentally executable creation procedure. The larger goal
remains open, including empirical particle admission, full material response,
stimulated channels and the revised thick-shell optical mode.
