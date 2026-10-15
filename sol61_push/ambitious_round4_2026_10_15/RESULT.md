# Fourth round: new static theorems and an executed lensing falsifier

15 October 2026. **Three analytic results survive independent reconstruction:
all nonspherical static sectors of the specified hybrid body, a full static
Einstein branch of its covariantized action, and an exact finite-stock
binding-energy formula.** The empirical work also advances: a controlled
continuous lensing calculation passes its relative gate, fails absolute fit,
and identifies an extended baryon source as a large but insufficient improvement.
The complete physical theory remains **OPEN**.

This executes [the round contract](CONTRACT.md), following the published
progress review at `f10c462424fc0804fa8ea66bdfae5bfa7fc96e9c`. The starting
checkout was `a553a4a663d393f29ec5da69c8cae68c164bb5b0`; concurrent work
advanced it. Each computation records its actual inputs and revision. The
[next instructions](CURRENT.md) now start beyond the implications established
here. These results have different model scopes and cannot be combined into
a single stability or galaxy theorem by citation alone.

## Static energy beyond spherical perturbations

The [angular proof](angular/PROOF.md), with its
[derivation appendix](angular/DERIVATION_APPENDIX.md) and
[independent audit](angular/EINSTEIN_AGENT_AUDIT.md), treats arbitrary
independent baryon and cold density perturbations and a common moving wall.
The entire wall area mass gravitates; both electric phases and the actual
finite-density Gauss jump vary. In the frozen hybrid Newtonian model, for
every harmonic l>=2 it proves

\[
 Q_l\ \ge\ .01\sum_a\int_0^1\eta_a^2 r^2dr
       +.25(l-1)(l+2)h^2.
\]

The electric moving-phase term can be negative; its control requires the
exterior Maxwell square and boundary jump, rather than bulk convexity alone.
The l=1 physical kernel is translation. Material relabelings and vortical
displacements supply additional static null directions. Together with the
inherited radial result, this establishes static configuration-energy
nonnegativity modulo those symmetries. It does not establish a positive
spectral gap for every displacement, interface evolution or radiation health.
The 219 exact finite checks support the reductions; the analytic estimates
and kernel identity establish the all-l statement.

## A body solving the full static Einstein equations

The [Einstein proof](einstein/PROOF.md) and
[independent reconstruction](einstein/ANGULAR_AGENT_AUDIT.md) replace the
hybrid Poisson source by the actual Hilbert stress of the minimally
covariantized current/gauge action. Proper rest stocks source the charge;
internal and gauge energy and anisotropic pressure all gravitate. An
uncharged Nambu–Goto wall satisfies both Israel jumps and joins to a genuine
asymptotically flat Maxwell/Reissner–Nordström exterior.

A uniform contraction with constant below .08 proves a regular static
branch for every eta=1/c² in [0,10^-4], with uniqueness inside its stated
function box. Positive eta gives the Einstein body; eta=0 is the classical
limit. The tension is selected along this branch, and the proper stocks
are outputs. This is not continuation at separately fixed tension and stocks.
The [128 checks and eight illustrative IVPs](einstein/COMPUTATION.md) are
separate from that analytic existence argument. At c=100, the example's
interior mass is 26.65772126 and its full ADM mass 26.65811653 in the
assigned units, including the counted wall, binding and Maxwell tail.

The EOS, occupied phase, reflecting contact and scales remain chosen inputs.
Neither the hybrid radial nor angular positivity theorem transfers to this
Einstein action without a new constrained perturbation argument. The
[junction convention check](JUNCTION_SOURCE_CHECK.md) includes a direct
distributional derivation, so no vacuum-interior shell formula is assumed.

## Lensing: controls resolved, absolute discrepancy remains

The [executed lensing report](lensing/RESULT.md) and
[independent code/derivation audit](lensing/INDEPENDENT_AUDIT.md) use continuous
mass and supply, actual profile cutoffs, trial-dependent exclusion in both
comparison families, equal nuisance freedom and the supplied full covariance.
The declared CFG416 threshold convention is Msun/h: physical turnaround mass
enters retention as log10(h Mta), with h=.6736. The legacy physical-Msun
argument is retained as a fixed secondary. This resolves the local source
dictionary, not the observational census calibration.

Independent real-space and Hankel projections agree to 1.18e-6 relative;
one-halo direct quadrature, actual normalization mutations and refinement
controls also pass. The authoritative point-source fit was rerun after
the supplemental mutation passed. The original failed K2 and all earlier
scores remain unchanged.

| All-radius diagnostic | chi-square / nominal dof | nominal p |
|---|---:|---:|
| Infinite point-source reference B | 161.8411 / 52 | — |
| Finite point-source D | 165.3582 / 52 | 9.78e-14 |
| Fixed distributed baryon radius 20 kpc | 109.2949 / 52 | 5.89e-6 |
| One fitted common radius, 35.33 kpc | 83.7763 / 51 | .002594 |
| Four fitted baryon radii | 75.7342 / 48 | .006516 |

The native point-source relative gap is +3.5171, passing the declared <=4
gate, while the absolute p>=.01 gate fails. The residual is spread over
inner, intermediate and outer radii. The distributed-source follow-up
recomputes the cold response, density, stock edge and exclusion from the
same Plummer baryons. Its four fitted projected half-mass radii are
12.19/42.29/37.89/37.80 kpc. Their actual baryon/gas observational constraints
have not been supplied. Even this expanded family misses the absolute gate.
No relative claim is made without an extended reference with matched freedom.
These are post-data diagnostics; the nominal p values are not calibrated
selection probabilities.

[Full predictions and residuals](lensing/summary_verified_001/predictions_residuals.csv),
[covariance](lensing/summary_verified_001/full_covariance.csv) and
[the comparison figure](lensing/summary_verified_001/profile_comparison.png)
make the remaining discrepancy inspectable. The environment still uses
matter auto-power times a fitted amplitude, rather than the required
isolation-selected galaxy–matter cross-correlation. Its cosmological initial
conditions/background remain inherited.

## Exact energy required for formation

In the separately scoped Newtonian fixed-point-baryon, critical-charge,
zero-stiffness reduction, the [new formula](inventory_energy/PROOF.md) gives
the unique constrained minimum's energy for every cold stock s=Mc/Mb>0:

\[
 V_*(s)=\frac23\left[s^{3/2}\operatorname{arsinh}(s^{-1/2})
 -\sqrt{s(s+1)}-2\operatorname{arsinh}\sqrt{s}\right].
\]

An exact positive series with a remainder bound evaluates finite uniform
starts. Every admissible such resting start has strict excess energy above
this minimum. Conservation therefore requires that excess to remain in
heat, dispersion, remnants or another counted channel, or leave the subsystem,
if the exact resting minimum is reached. Closed strong convergence to that
minimum in the conserved-energy topology is excluded; weak phase mixing
is not excluded. The
[independent audit](inventory_energy/AUDIT.md) accepts the analytic formula
and conditional obstruction. Nine exact checks, three independent
high-precision integrals and nine finite starts support the stated computations.

For an assigned Mb=10^10.5 solar masses and a start at twice the final edge,
N=3/6/10 gives about 3.15/3.70/4.12e51 joules of excess. These are conditional
state-energy differences, not luminosities, a cooling rate or derived supply.
They do not yet apply to nonzero stiffness or the Einstein body.

## What has and has not closed

The static angular obligation for the specified hybrid body, the static
Einstein existence/junction obligation for the covariantized branch, and
the zero-stiffness finite-start energy calculation are now supported by
analytic arguments and separate same-team audits. These are not external
peer review or formal verification. [Audit and provenance](AUDIT.md) records
the accepted runs and preserved failures.

Physical phase selection, constrained dynamical stability, nonzero-stiffness
formation with a receiver, actual finite supply/census, a candidate-matched
lensing source, parameter origins and native cosmology remain open. Existing
T1x already implements numerical unique-host ownership and caps; the missing
bridge is physical current/transport and the selected lens–matter statistic.
Concurrent CFG806's frozen cooling-based census attempt is NOT DERIVED;
its ceiling-only trend is not an abundance mechanism. DR4 Amendment 22 has
been filed, so the old instruction to obtain that convention is superseded
by implementing and auditing its actual scorer. The
[source checkpoint](source_checkpoint.json) pins the inspected records.
