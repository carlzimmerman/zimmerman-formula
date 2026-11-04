# CC11: energy, vectors and physical decay matching

The requested calculations have substantially improved the weak-coupling
description. **No complete viable cold-matter history has been demonstrated.**
The tested late charged population still fails the charged-relic requirement;
its neutral-adjoint decay source is too hot and too small to supply the dark
matter. Early photino production remains a separate open route. No global
exclusion of this model follows from the conditional late calculation.

All new work uses e=.003, mu=2e6 GeV and xi=.02, with the same leading
gravity trajectory packet. The separately exported finite local gravity
packet is not interchangeable with it. Vacuum energy remains tuned to the
chosen residual, rather than derived from the matter calculation. No portal,
entropy injection, new production sector or strong coupling was introduced.

## Energy: the old defect is repaired, state refinement is separate

The old warm history mixed backward-Euler populations with an independently
advanced log action. Its finite increments did not conserve the same
Hamiltonian; the error was about 23.85% of orbital excitation. Local collision
energy and the continuum force/action identity were already correct.

`energy/split_energy_v7.py` instead composes expansion half steps and a
collision step whose actual population increment obeys constant endpoint
Hamiltonian. The collision geometry is centered in population and **action**.
Using a centered energy surface would fail near a moving minimum, because
the minimum energy is concave in the populations. Each population fixed-point
trial starts from the same old physical state. FRW stress work is independently
integrated by Simpson quadrature; it is not assigned from the energy change.

The complete fresh 25-group coarse/fine benchmark reaches
N=.0021690179772784167, with maximum steps 1e-4/5e-5. Its independent
energy/work errors are 3.60e-7/1.17e-7 of orbital excitation. The action is
2.12177629116e-6/2.22418570094e-6, a **4.83%** refinement change. Charged
yield changes -.0386% and the photino yield -1.71%. These quantities have
different numerical errors. Energy closure is not a claim of 1% action
convergence. See `energy/run_benchmark001/result.json` and `energy/DERIVATION.md`.

The independent direct field plus 30-population calculation over an actual
initial orbit gives a 3.9945-fold improvement in maximum energy defect when
64 steps become 128. It also exposes newborn-chain timing errors: one/two/four
averaged BE steps give photino counts 5.941/2.994/1.879 times the direct result,
closely tracking the three-generation BE factors 6/3/1.875. The largest
newborn discrepancy is temporal; this is not a general phase-averaging proof.
The outer geometry tolerance also remains distinct from the tighter Newton
population residual. See `review/energy/REVIEW.md`.

The positive implicit-midpoint candidate is **not promoted**. The larger-step
control exhausted its CPU cap; the reduced-step control completed one/two-step
cases but not the four-step comparison. No second-order history has been
established. The failures are preserved and are not interpreted as a physical
instability.

## Vectors and cold gauge transport

`integration/common.py` adds broken-vector longitudinal/transverse groups and
the three unbroken transverse gauge sectors, for 30 groups. Their masses,
statistics and gas forces share one background. `vectors/transport_v3.py`
contains the canonical VSS, VFF and SVV channels, inverse reactions and quantum
factors. Ward/Goldstone relations, spin traces, degeneracies, signed charge,
angular refinement, energy and detailed balance have finite controls. Massive
vectors carry charge and can return it to scalar/fermion carriers; they are
not an irreversible radiation sink.

The fresh common tree history starts at N=0 with exactly empty vectors and the
original charged FD packet. The completed coarse endpoint is
`integration/run_joint006/result.json`: J=1.95727961076e-6,
Y_charged=3.03302210296e-7, Y_chi=1.10626332678e-9 and
Y_vectors=7.30677396563e-10. Its maximum independent energy/work error is
4.0023e-7 of excitation. Compared with the 25-group run at the same step size,
vectors change the action by -7.75%. This is a warm checkpoint, not a final
relic abundance or a retained-vacuum theorem.

The complete fresh refined endpoint is
`integration/run_joint_fine009/result.json`: J=2.06557095630e-6,
Y_charged=3.03150605405e-7, Y_chi=1.08609722788e-9 and
Y_vectors=7.24103953429e-10. Its independent error is 1.2981e-7 of excitation.
Halving the step changes J by +5.53%, chi yield by -1.82%, charged yield by
-.0500% and the full number vector by .568% in relative L1. At the refined
resolution, adding vectors changes J by -7.13% and chi yield by +5.50%, compared
with the scalar/fermion reference. See `integration/run_warm_seed001/result.json`.

There is an actual early chi seed that would be cold **if its population and
momenta survive and its mass settles to the retained-pole value**: the refined
conditional mean travel distance is .1824 kpc. Its current number would supply
only .02585% of DM rest density. Neither survival nor final production is
established by this diagnostic. It is not the late hot-adjoint-decay component.

Weak coupling does not imply negligible cold Coulomb transport. The physical
generator factor is 7/12, assembled from 2/9, 3/16 and 25/144. At the old late
memory endpoint, momentum diffusion is .1908 per Hubble time. A positive
892,504-event screened direct-t scalar self-scattering operator agrees with the
independent rate probe, preserves physical number and kinetic energy, and
passes detailed balance/entropy/Jacobian tests. Over .1/H it changes the shape
by 2.14%, while pressure changes only 1.7e-11 relatively and the old annihilation
functional changes about -5e-5. Number- and energy-preserving elastic scattering
cannot remove the charged rest density.

The subsequent conditional old-late cooling calculation retains the four-state
resonance kernel, massive neutral cohorts and signed scalar work. Its refined
results are in `vectors/run_cold_split001` and `run_cold_split002`: adding
elastic scattering increases the surviving charged yield by .14373%/.14440%.
The baseline recovers the older continuous memory result to 5.6e-9 relative.
The tested endpoint remains about 304 times the charged-relic gate. These are
not continuations of the new warm vector state. The un-subtracted model
energy/work defect is reported separately, about 4e-8 of initial energy;
the much smaller residual-subtracted closure is bookkeeping, not an independent
energy certificate. Direct chemical gauge annihilation is negligible over the
tested late interval, with rate/H about 3e-13 down to 3e-15 including the
computed Coulomb enhancement. This does not extend a Born approximation to
arbitrarily late screened resonances or bound states.

The common cold scalar self-scattering API is now portable to the root 3.9
runtime: `vectors/coulomb/scalar_factory_v3.py`, `elastic_builder_v3.py` and
`template_v2.py`. Paired 3.13/3.9 controls reproduce coefficient, geometry and
energy fingerprints exactly. The earlier builders remain valid 3.13 records
but use syntax unsupported by 3.9; they were not silently edited.

## Physical leading two-body decay matching

The checked local pole packet contains all six triangle classes FFS, FSS,
FFV, FVV, FSV and FVS, the correct conjugate vector-index orientation, physical
Goldstones separated from the two physical flat scalar modes, and the relevant
leg/selection checks. Gauge/UV/basis, messenger and weak-scaling controls pass.
The independent audit supports the leading fixed-pole packet, not all x,
higher multiplicities or a fully matched gravity current.

| Parent | Lifetime | Branch to chi + adjoint gaugino |
|---|---:|---:|
| S8_0 | 4.367102 ms | .3794989902 |
| S3_0 | 5.827441 microseconds | .4685413320 |

The octet also has a .00589873 adjoint-gaugino-pair branch. Every gauge and
partner daughter is retained separately. The exact unitary transpose charge
conjugation forbids the adjoint-scalar/adjoint-gaugino/Goldstino exit and the
chi/adjoint-gaugino/one-gauge transition under symmetry-preserving additions.
It does not forbid the ordinary chi/charged-scalar/charged-fermion current.

The authoritative rates/cohorts are `decay/INTERFACE.json`, `decay/run005`,
`run_legs003`, `run_bridge001` and `run_production002`; the independent audit is
`review/decay/REVIEW.md`. Read `decay/REVIEW_CORRECTIONS.md` with the preserved
original derivation: it corrects the reported octet gauge spread, the scope
of the messenger test and representation-forbidden open thresholds.

`integration/loop_transport.py` embeds these fixed-pole widths and their
inverses into the common number operator, with all daughter sectors and
quantum availability. `run_loop001` passes fourteen finite controls. Its
hard-support check uses q up to 30000 and soft NR parents; it does not certify
arbitrary hard-parent support or a spin-asymmetric distribution.

For early NR parents, fixed pole and collisionless propagation, mean photino
travel distances are **302.14 and 67.38 Mpc**. The distinct old-late yield
normalization supplies only 2.183e-7 of DM in photino rest mass. Achieving a
mean distance of 1 kpc at this same mass would require hypothetical total-rate
multipliers 3.468e12 and 6.749e10; even the 100-kpc diagnostic requires 1.657e8
and 3.206e6. These are timing requirements, not computed new widths or an
observational transfer-function exclusion. Small perturbative corrections
cannot supply those factors. See `integration/run_cold_source001`.

The allowed chi+C<->F inverse current was also checked. A large spontaneous
width/H is not the absorption probability: the redshifting narrow-line column
must be integrated. With the tested old-late populations and the declared
fixed-pole future-column upper bound, the maximum absorption optical depth is
.00066261, with an off-resonant bound 1.72e-9 outside the 10% line band. These
interactions cannot cool the bulk of that late hot component. This bound does
not establish survival of the early warm seed. See `vectors/run_opacity001`.

## Cold numerical continuation and the remaining physical implication

The inherited orbit oracle uses a harmonic branch below J/J_initial=1e-7 and
loses very small excitation when adding it to a large total minimum energy.
The separate `cold_offsets/` package computes nonharmonic local orbits from
stable potential differences and a rational gas-energy remainder, retaining
excitation independently. It retains excitation down to 3.19e-27 mu^4 in the
warm stress fixture and resolves amplitudes down to 1e-10 in the conditional
scalar-only cold-pole fixture. Independent action checks are at about 2e-15
relative for these finite representations. Its tests are artificial-action
fixtures, not cosmological histories. The coupled stepper still needs stable minimum
energy differences, collision increments and separate excitation bookkeeping;
an improved orbit oracle alone does not supply that API.

The next load-bearing calculation is a coherent **fresh** continuation through
cooling, trapping and depletion with adequate soft and hard momentum support,
controlled scalar motion and full daughter/inverse transport. The q<=80 warm
grid cannot carry arbitrarily late hard neutral decays. The old late endpoint
must not be spliced onto the new warm history. The early photino seed's
survival, opacity and eventual abundance must be computed, not assumed.

Thus the tested late cleanup/source route still fails. The microscopic photino
window is not eliminated by this result, but its simultaneous production,
charged-cleanup and retained-gravity-vacuum requirements remain unmet.

## Reproducibility and preservation

Every numerical job has a prior finite contract and bounded v2 manifest:
wall<=240s, CPU<=235s, one numerical thread, measured RSS. Root integrations
use Python 3.9.6/numpy 1.26.2/scipy 1.11.4. Some vector jobs use Python 3.13.9/
numpy 1.26.4/scipy 1.14.1; `vectors/ENVIRONMENT_ERRATUM.md` preserves and corrects
the stale software descriptions in their early contracts. Historical source
versions, failures and time/resource limits remain available. A completed
process is not automatically a successful mathematical assertion.

The final inventory checks 117 run records: 94 completed, 22 failed and one
resource-limited. Seven historical current-path validator differences have
exact archived original bytes; they are distinguished from current preferred
records. No unrecovered inputs, changed recorded outputs or unexpected
validator failures remain. The failed midpoint refinement is included in these
records and is not relabeled as a successful method.

The final integrity certificate is `VERIFICATION.json`, regenerated by
`python3 reviews/weak_completion_2026_11_04/verify_records_v2.py`. It distinguishes
newer-interpreter archival syntax from root-runtime portability. Frozen prior
checks cover all 819 CC10 and 896 TP06/CT09 artifact pins. This phase has not
modified prior physics artifacts or performed Git mutations.
