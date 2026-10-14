# Energy-conserving source/continuum feedback surrogate

2026-10-13. Base checkpoint: 9bef94e533372ad26b2fda8acb60a77629eced34.
This follows the time-gradient warning in ../threshold_memory_audit_2026_10_13.
The manufacturing goal remains open. We now test a closed Hamiltonian surrogate
that retains coherent conversion and a population-dependent threshold, rather
than setting an instantaneous rate to zero at a moving threshold.

## Model and calibration

Let a be a source amplitude and b_j the amplitude of a pair in continuum cell j.
In units of the initial pair excess D0, with time tau=t D0/hbar, define

    N=|a|^2+B,  B=sum_j |b_j|^2,
    H=|a|^2 + sum_j epsilon_j |b_j|^2 + kappa B^2/2
      +2 Re[a* sum_j v_j b_j].

The coefficients v_j are real. Hamilton's complex amplitude equations are

    i da/dtau = a + sum_j v_j b_j,
    i db_j/dtau = (epsilon_j+kappa B)b_j+v_j a.

The common pair rest energy has been subtracted using the conserved norm N.
The dimensional energy tracked here is excess energy D0*H per initial source;
it is not the whole relativistic rest-energy content. B counts pair-sector
weight, so a free pair would contain two carriers.

Initially a=1 and b_j=0, so N=H=1. This is an imposed bare source initial
state, not a thermally dressed density matrix. The Hamiltonian is held fixed
during the run: there is no external power input after this initialization.
Preparation work and initial correlations are not derived from the source bath.

The common shift kappa B is the derivative of kappa B^2/2. Counting the full
kappa B^2 as interaction energy would double-count the mean-field energy.
Hermiticity gives dN/dtau=0; the canonical flow of this time-independent H
gives dH/dtau=0. In the finite discretization, bounded norm also prevents the
polynomial vector field from escaping to infinity in finite time.

To match two initial moment quantities of the earlier T=2 MeV diagnostic, set

    D0=2.2831240019e-5 eV,
    fstar=1.6604056498e-5,
    kappa=1/fstar=60226.246527,
    tau_star=53.5262762291,
    gamma=2 fstar/tau_star=6.2040768265e-7.

Here fstar is the earlier estimated consumed source fraction at sharp closure.
The effective initial conversion width gamma D0 matches that fraction's initial
growth. It is NOT the microscopic rest-source width: the old moment calculation
averaged moving-parent decay and inverse daughter energies. A single effective
continuum cannot retain all those momentum correlations. These matches define
the surrogate; they do not derive it from the original thermal field theory.

Choose the continuum spectral weight

    v(epsilon)^2 d epsilon
      = gamma/(2pi) sqrt(epsilon) exp[(1-epsilon)/L] d epsilon,
    epsilon>=0.

Thus 2pi v(1)^2=gamma for every tested L. L=2,5,10 are independent choices
for the spectral shape, not measured parameters. The source energy is the bare
coefficient 1; a regulator-dependent pole matching or counterterm is not imposed.
The tested energy cutoffs 120 and 160 are distinct from the exponential scale L.

The corresponding stationary golden-rule equation would contain

    dB/dtau = gamma (1-B) sqrt(1-kappa B)
              *exp[kappa B/L], for B<1/kappa.

Its real on-shell rate vanishes at B=fstar. The coherent calculation instead
keeps amplitudes, their history and reversible transfer through that point.

## Finite-window result

The evolution is computed until tau=2 tau_star, equivalent to about 3.086 ns
under the calibration. All entries below refer to the bare continuum component
B, not a count of extracted, asymptotically free carriers.

| Spectral scale L | Largest sampled B/fstar | B/fstar at tau_star | B/fstar at 2 tau_star |
|---:|---:|---:|---:|
| 2 | 1.06413 | 1.06256 | 1.03470 |
| 5 | 1.05183 | 1.04755 | 1.03033 |
| 10 | 1.04812 | 1.03781 | 1.02950 |

There is a modest overshoot of the sharp threshold followed by partial reverse
transfer. These runs neither remain exactly at the old threshold nor grow
without limit over the tested interval. This is a result for these specified
initial states and spectral shapes, not a late-time saturation theorem or a
prediction for the thermal bath. The maxima are over 201 stored times.

At L=5 and tau=2 tau_star, the energy account, relative to the initial source
and divided by fstar, is approximately

    source energy loss:   -1.03032714
    continuum kinetic:    +0.54962304
    repulsive interaction:+0.53078700
    coherent interaction: -0.05007967

The residual is about 3.3e-6 in these units. The negative coherent term is
part of the conserved Hamiltonian; dropping it would give a false impression
of unexplained energy. The presence of this term also matters operationally:
the bare pair component includes dressing/correlations, and switching off
couplings or measuring free outgoing particles can change the energy account.
No extraction yield can be obtained by identifying B with stored inventory.

## Numerical verification and the failed first check

The algorithm uses a symmetric composition of two exact subflows: a diagonal
phase evolution with B fixed, and a source/bright-continuum rotation. Each
preserves norm; their composition conserves the full H only to numerical
accuracy, which is checked separately on the small conversion-energy scale
D0*fstar rather than only relative to the large initial energy D0.

The linear finite-grid limit is independently solved by matrix diagonalization.
The first attempted step 0.002 gave maximum amplitude error 2.35293e-7, missing
the declared 2e-7 target. Steps 0.004,0.002,0.001,0.0005 gave respectively
9.41204e-7,2.35293e-7,5.88228e-8,1.47057e-8: second-order convergence.
The final check uses step 0.001 without relaxing its tolerance.

The initial failed source and contract snapshots are preserved with the failed
run record. That record hashes the then-current check.py; its old hash agrees
with initial_failed_check.py, not with the revised check.py. The final evidence
is run_verified/manifest.json, whose current-input hashes validate.

Sixteen checks pass in the final run:

- Independent linear matrix evolution, maximum amplitude difference 5.89e-8.
- Weak-coupling threshold probability versus the preceding finite-pulse
  analytic formula, relative difference 1.29e-5.
- Six norm checks, maximum sampled error across runs below 2.5e-12.
- Six energy checks, maximum sampled error across runs below 6.3e-5 D0*fstar.
- Time refinement at L=5, maximum population difference 3.38e-6 fstar.
- Continuum-grid/cutoff refinement at L=5, difference below 1.1e-14 fstar
  over this window. This close agreement does not establish convergence for
  other spectral shapes, much later times or arbitrary precision.

The midpoint grid uses epsilon=q^2 to resolve the square-root threshold.
There is no arbitrary random seed. Full trajectories, numerical settings,
input hashes and execution limits are retained. No bath scattering, photon
loss, Bose enhancement or thermal inverse-collision integral is simulated.

## Formal scope and research decision

HamiltonianIdentities.lean checks the finite-sum norm tangent identity and
canonical energy-gradient cancellation. These are algebraic identities over
the reals for arbitrary finite mode sets. Derivation of the Hamiltonian from
the full field theory, differentiability/chain-rule application, convergence
of the numerical flow and particle existence are outside those lemmas.
Lean compilation status and printed axioms are recorded separately.

This checkpoint supplies the previously missing energy-accounted example of
threshold crossing with reversible feedback. It does not supply a justified
source-to-reservoir pathway. The remaining decisive step is to identify which
part of the populated continuum becomes free outgoing carriers under a
specified source preparation and decoupling protocol, with its switching work
included, then replace the effective continuum with the momentum-resolved
thermal source. Without that, the modest overshoot cannot be advertised as
extra stored cold energy. Material confinement and empirical mediator
constraints remain separate unresolved requirements.

Reproduce from repository root:

    OPENBLAS_NUM_THREADS=1 python3 sol61_push/coherent_threshold_feedback_2026_10_13/check.py /tmp/coherent_feedback_results.json

The manufacturing goal remains active. This is a Hamiltonian surrogate result,
not experimental evidence or a certification of the complete mechanism.
