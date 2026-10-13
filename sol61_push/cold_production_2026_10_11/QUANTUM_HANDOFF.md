# Finite-box vacuum growth followed by correlated spatial evolution

2026-10-11. This replaces the arbitrary seed of [SPATIAL_CONVERSION.md](SPATIAL_CONVERSION.md)
with a declared Gaussian quantum-to-classical prescription. It is not a
controlled solution of the full quantum field theory.

## Early quantum calculation in the same box

Use the spatial envelope's dq=0.4 and retain 245 unordered, nonzero
opposite-momentum pairs with q^2<=4. The initial daughters are in their vacuum.
With the chosen physical density and masses, the periodic box contains
N_s=1.8826819994e67 initial source quanta, so each pair has weight
w=1/N_s=5.3115714727e-68. This fixes the spontaneous source term; there is
no manually chosen initial daughter amplitude.

The Gaussian equations are those of CHARGED_PRODUCTION, adapted consistently
to the spatial envelope: no expansion, G=1, v_j=1, pair detuning 2L_A(q),
and k=0.2000001. The source depletes and both quartic terms are included.
Handoff events occur when sum F reaches 1e-5, 1e-4 and 1e-3. These are
matching choices, not physical input daughter populations. Their times are
x=72.59345593, 73.76850999 and 74.94375360, respectively.

[quantum_handoff_v2.py](quantum_handoff_v2.py) uses relative tolerance 1e-12
and pair absolute tolerance 1e-13 times w. The first run retained in
`quantum_handoff_run` failed the covariance criterion in almost-empty modes.
The tighter run passes the unchanged criterion: maximum relative correction
to impose pure Gaussian covariance is below 7.14e-11 at all handoff events.
The dominant amplified modes were already much more accurate in the first
run. No failed result was overwritten.

## Covariance-preserving daughter sampling

For each pair define its normalized classical Fourier amplitudes a,b.
Their desired Wigner moments are

\[
 \mathbb E|a|^2=\mathbb E|b|^2=s={F+w/2\over2},\qquad
 \mathbb E(ab)=d={C\over2}.
\]

The half quantum is required by symmetric ordering. For pure Gaussian
moments, |C|^2=F(F+w), hence s^2-|d|^2=w^2/16. Numerically project |C| to
sqrt(F(F+w)) while retaining its phase; the small projection error above
is recorded rather than hidden.

For independent unit-variance circular complex Gaussian variables z_1,z_2,
let L=(s+|d|)/2 and l=(s-|d|)/2. Sample

\[
 a=\sqrt L z_1+\sqrt l z_2,\qquad
 b=e^{i\arg d}(\sqrt L z_1^*-\sqrt l z_2^*).
\]

These expressions reproduce both moments directly. Evaluate
l=(w/4)^2/[2(s+|d|)] to avoid subtracting nearly equal numbers at enormous
occupation. At the 1e-4 handoff, the most amplified pair has occupation
about 1.57e62. A 100,000-draw check of that pair's variance and anomalous
covariance passes the declared 2% sampling tolerance. The analytic moment
identities, not this finite check, establish the distribution's covariance.

The general semiclassical phase-space framework is discussed by
[Polkovnikov, arXiv:0905.3384v3](https://arxiv.org/abs/0905.3384v3). Its abstract
explicitly distinguishes truncated-Wigner evolution from further quantum
corrections. No error theorem for this model or this handoff is imported
from that reference; checked 2026-10-11.

## Source adjustment is an explicit approximation

A single sampled daughter field does not have exactly its ensemble-average
charge. Holding the Gaussian source amplitude fixed would give each
classical realization a different total charge. Here the source phase is
retained, and its uniform amplitude is changed to
sqrt(1-sum |A_k|^2). Daughter amplitudes are not rescaled, so their sampled
correlations are preserved. Vacuum half-quanta in the retained modes are
negligible compared with the occupied charge but remain part of this
finite classical normalization.

This produces source/daughter correlations by prescription. It is **not**
sampling a derived exact joint quantum state. It changes the source at
order of the early daughter fraction, which motivates varying the handoff
point. Also, zero and higher-momentum vacuum modes are not sampled, and
source quantum noise is omitted. These omissions require control before
claiming full quantum accuracy.

## Spatial continuation and handoff sensitivity

[matched_spatial.py](matched_spatial.py) evolves the sampled fields with the
full moving-source envelope on a 24^3 grid, time step at most 0.005, to
absolute x=100. It uses one reproducible random draw (seed 471901) at both
handoffs, allowing comparison along corresponding sampled realizations.
The source-adjustment magnitudes are 1.87e-6 and 1.87e-5, respectively.

| Mean handoff daughter charge | Sampled daughter charge initially | Daughters at x=100 | Moving source charge at x=100 |
|---|---:|---:|---:|
| 1e-5 | 1.373946e-5 | 0.62764550 | 0.29441578 |
| 1e-4 | 1.373946e-4 | 0.62766752 | 0.29439108 |

Both runs pass charge and energy diagnostics. Maximum charge drift is below
5.4e-11 and energy drift below 1.4e-5. The endpoint daughter difference is
2.20e-5, comparable to the time-step sensitivity seen in the earlier spatial
pilot. This supports the internal handoff prescription for this realization;
it is not a rigorous quantum/classical error estimate or a statistical yield.

The large difference between sampled and mean initial daughter charge is
expected to matter for ensemble testing: this coarse momentum box has only
12 effectively populated pairs, as measured by (sum F)^2/sum F^2. Hence
one random draw is emphatically not self-averaging. A larger box changes
resonant-mode sampling and must also be tested; increasing grid N alone
would not resolve that issue.

Evidence: [tight quantum results](quantum_handoff_run_v2/results.json),
[quantum manifest](quantum_handoff_run_v2/manifest.json),
[spatial results](matched_spatial_run/results.json), and
[spatial manifest](matched_spatial_run/manifest.json). All current manifests
validate against their inputs. The code and derivation were self-reviewed,
not independently audited.

**Result:** there is now an executable sequence from retained-mode quantum
vacuum to a correlated high-occupation sample and then spatial conversion,
with a small handoff-point dependence in one realization. It retains the
moving-source channel that altered earlier conversion histories. The next
checks are ensemble and box-size dependence, followed by expansion and
quantum-correction control. This is progress on a candidate formation route,
not a completed cosmic origin, abundance or galaxy-law explanation.
