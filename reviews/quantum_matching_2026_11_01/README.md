# TP02: weak quantum matching and derived material response

The pressure obstruction survives every computed weak-coupling RG/scale
prescription and the calculated finite heavy-relaxation subset. Actual
microscopic state couplings were also derived: the phase-current state is
pressure-rich, while a massive-eigenmode gas has a small conditional cold
window with no established stable number or lifetime. Complete finite
two-loop/current matching remains open. This checkpoint is not a physical
all-order no-go, a selected cold component or a kappa derivation.

The owner's request and hypotheses are fixed in [CONTRACT.md](CONTRACT.md).
Base revision: `40d43dbb8a9f1517e214302380f7659df7626e6a`, in an active dirty
shared checkout. Exact input hashes identify the scientific versions.
TP01 and all prior theory/solver/certificate inputs were retained.

## Quantum matching actually calculated

The full SU(5) one- and two-loop beta/anomalous-dimension functions were
derived independently, including the dimensional f and field transport.
The full one-loop spectrum satisfies its exact Callan–Symanzik cancellation.
The old critical gauge ratio is imposed only at Q0; it runs away from that
surface. Canonical X and the re-minimized flat coordinate T have distinct
running. Finite one-loop thresholds, CS-required second-order scale logs,
and finite normal heavy displacement are kept separate.

Trials use f(Q0)=Q0=1, h(Q0)=lambda(Q0)=e in {.01,.03,.05,.1}, and the
inherited gauge comparator g(Q0)=sqrt(29/200)e. These are trial boundary
data, not fitted or selected constants. Matching-scale factors .5,1,2,
different running/log prescriptions and independent derivatives were tested.

For the **old assumed waterbag coupling**, all 28 scheme/coupling cases
retain a positive-source, radially stable compressibility boundary and a
negative-compressibility witness at X/Xmin=1.2. Adding the known finite
vacuum heavy-relaxation correction retains that failure in all four trials:

| e | Fixed one-loop boundary | RG-improved central boundary | Plus finite heavy relaxation |
|---:|---:|---:|---:|
| .01 | 1.177300 | 1.177179 | 1.177112 |
| .03 | 1.177300 | 1.177393 | 1.176779 |
| .05 | 1.177300 | 1.179115 | 1.177392 |
| .10 | 1.177300 | 1.191494 | 1.185303 |

Ratios use the retained reference-X chart and each approximation's own
vacuum. They are diagnostics, not measured amplitudes. Searches concern
the inherited connected branch; some outer radial endpoints were outside
the compact brackets. No exhaustive branch classification is asserted.

The finite term is computed from full mass-matrix spectral derivatives:

    Delta U_relax=-1/2[(CW_a)^2/(120fh)
                         +(CW_b)^2/(60lambda^2 a0^2)].

This gauge/scheme-dependent subset is not the complete finite two-loop
potential. Its root shift is much larger than the residual scale spread
after completing the CS logs, directly showing why scale stability cannot
serve as an error bar on missing finite diagrams. [Threshold report](rg_threshold/REPORT.md),
[independent RG derivation](rg_derivation/DERIVATION.md),
[implementation review](rg_derivation/IMPLEMENTATION_REVIEW.md).

## The material interaction changes the pressure problem

The canonical complex field supplies a genuine phase-charge energy
n_theta^2/(4|T|^2). Its density exponent is two, rather than the old
waterbag's five-thirds. With a matched angular coefficient F(s), the
two-derivative response depends on F, its derivatives and U together;
the old Uss>3Us condition cannot be transferred to this different state.

For occupied heavy matching, the actual normal source is
CW_b-omega^2*60b0. Keeping its full square includes the vacuum correction,
induced angular metric and omega^4 term exactly once. At e=.03:

| Native phase approximation | Compressibility endpoint X/Xmin | Excess P/epsilon there |
|---|---:|---:|
| Fixed complete one-loop thresholds | 1.21339321 | .614799 |
| RG and running angular metric | 1.21362615 | .614460 |
| Plus complete known occupied heavy square | 1.21263208 | .615670 |

The native phase still has positive sound speed at ratio 1.2 and negative
sound speed at 1.3 in the tested continuation. The old waterbag's negative
1.2 witness is a different calculation. A zero sound speed at the endpoint
does not make the excess component cold. A connected-branch inequality
also bounds its two-derivative pressure from below over this short field
range. The anomaly prevents assuming an exact quantum R-charge lifetime.

Actual massive eigenmodes instead couple through sqrt(p^2+m_a(T)^2).
The field-dependent rest energy dominates their cold scalar source;
dropping it reverses the source sign for the light branch. One explicit
light-adjoint occupation has a cold, positive-susceptibility window ending
at ratio 1.01932024. Its charged/interacting modes have no derived conserved
number or lifetime, so this is an instantaneous state diagnostic, not an
adopted dark-matter-particle proposal. [Matter report](matter_coupling/REPORT.md),
[occupied-state derivation](matter_coupling/OCCUPIED_DERIVATION.md),
[independent occupied review](rg_derivation/OCCUPIED_REVIEW.md).

## What remains unresolved

The direct finite two-loop vacuum graphs and direct finite one-loop
component kinetic/current graphs remain uncomputed. Running wavefunctions
and the heavy-induced angular correction do not supply all of them.
Light-sector/IR matching, anomalous-current evolution, occupation/lifetime,
and gravity also remain open. A weak-coupling sign persists asymptotically
under a uniformly smaller matched derivative remainder, but the needed
finite-e remainder bound is a condition, not an established error estimate.

The source/field dictionaries and independent coordinator reconstructions
are in [SOURCE_CHECKS.md](SOURCE_CHECKS.md),
[COORDINATOR_RG_AUDIT.md](COORDINATOR_RG_AUDIT.md),
[PHASE_RESPONSE_AUDIT.md](PHASE_RESPONSE_AUDIT.md) and
[HEAVY_MATCHING_AUDIT.md](HEAVY_MATCHING_AUDIT.md).
[VERIFICATION.json](VERIFICATION.json) records final current-hash validation
and review provenance; [HANDOFF.md](HANDOFF.md) identifies the next exact
matching obligation. No production simulation, new data download, queue
change, dependency installation, Git commit or push was performed.
