# Peer review of the newest gravity calculations — 2026-09-26

**The requested complete theory is not established. Primary verdict:
incomplete, with specific missing implications.** This review carries the
earlier work forward and audits the newest XC1/XC2 and dark-sector claims.
It finds additional defects in the claimed closure, preserves valid partial
results, and supplies reproducible calculations for both exponential laws.

The starting revision was `f3b848273e635b81bc328882db0ffb4206d86e45`, with
substantial existing uncommitted work. The earlier
[closure review](../closure_resume_2026_09_26/README.md) and
[construction campaign](../closure_doors_2026_09_26/CONTRACT.md) are the
baseline, not superseded research to repeat. In this conversation the user
explicitly requested exploration of **both** the published RAR law and the
closure specification's exact exponential AQUAL law. They are tracked as
separate branches; the original thirteen-requirement spec is unchanged.

## What was already known, and what this review adds

Already established: `nu_mono` differs from the exact targets; the gate needs
its own variation; prescribed carrier dynamics are not derived from the
permitted field action; a scalar block or Lean identity is not a full
constraint/PPN certificate; the original heat filter need not contract a
lapse-weighted energy. Those are inherited findings, not new discoveries here.

| New or newly checked finding | Consequence | Evidence |
|---|---|---|
| L381/L387 use an active p=1, xc0=1.5 merger gate while importing p=2, xc0=2 PM retentions | Their merger verdict cannot certify or exclude the claimed common parameter cell | [Dark-sector source trace and checks](dark_sector/REPORT.md) |
| PM and merger calculations use different source/force operations | Fixing only the gate numbers still does not supply the same theory | [Operator comparison](dark_sector/REPORT.md) |
| XC2's zero-field claim excludes an admissible homogeneous field and degenerate isolated zeros | Its Osgood argument does not close the full zero-field requirement | [XC2 counterexamples](xc2/REVIEW.md) |
| XC2 applies unweighted heat contraction to a different, lapse-weighted norm | Its all-kernel/all-lapse convexity claim fails; the earlier counterexample is independently checked and extended to RAR | [XC2 weighted Hessian review](xc2/REVIEW.md) |
| Varying the heat operator creates mixed metric/scalar terms without one exponential suppression per leg | XC1 does not close full strong coupling; XC2's full-symbol reduction remains unproved | [XC1 mixed variation](xc1/REVIEW.md), [XC2 mixed symbol](xc2/REVIEW.md) |
| L340's monotone splice has a jump in the next constitutive derivative | A single cubic Taylor expansion is unavailable at the splice without specifying a smoother replacement | [XC1 splice calculation](xc1/REVIEW.md) |
| Both exact laws fail the same current frozen scalar completion in its small-alpha window | Neither exact target inherits `nu_mono`'s health pass; the RAR calculation extends the prior EXP result | [Separate branch calculation](kernel/REVIEW.md) |

## Decisive results and what survives

The merger-gate mismatch is executable, not just documentary. At z=0.4 its
two thresholds are **2.320594** and **4.786806** on the same background.
Retention medians and saved pass flags reproduce, but the physics input
differs. Only the assumed S1 shapes at 600 and 625 km/s pass the stored
Harvey test. The phase-mixed S2 value at 600 is **0.108644**, above its 0.10
cutoff under the inherited gate. No corrected-gate pass or exclusion is
claimed. A separate 12-case spherical check supplies both requested kernels'
gate derivatives; neither exact law fixes the canonical massive flagship's
activation failure under that approximation.

For XC2, take an allowed flat closed leaf with U=0 and perturb it by
epsilon sin x. The leading deep-MOND flux is homogeneous of degree one half,
so its response scales as **sqrt(epsilon)**, including a nonzero mode after
the outer heat filter. It does not obey the claimed linear/logarithmic
modulus at that background. This invalidates that proof of control, not
every possible nonsmooth existence or uniqueness method. A genuinely
monotone continuous kernel still has a sound fixed-background convex
auxiliary problem modulo constants. The two exact nonmonotone branches
require additional lapse restrictions or another solvability argument.

XC1's flat khronon cubic/quartic power counting is independently supported.
Its restricted UV momentum scale remains very high. But mixed heat-operator
variations survive the exponential-per-leg argument, and its fixed
normalization is not a bound over all momenta. A diagnostic using running
normalization stays tiny in the sampled cells; it is neither a full G8
certificate nor evidence that strong coupling actually occurs. The missing
full-action calculation matters regardless of that numerical margin.

For the two exact kernels, the independently reduced C-H/K block requires
alpha>0.062527 at one RAR witness, or alpha>0.270671 at the EXP witness,
instead of the candidate's stated ceiling 3.2e-9. A finite heat filter leaves
a lower-k interval with negative squared speed and a singular crossing in
that block. A larger alpha also changes the static force response, so it
cannot be counted as a repair without rematching the law and measured G.
This is a result about the specified completion, not a universal obstruction
to the user's framework.

## Framework fidelity and remaining dependency chain

The common target remains one explicit action with ordinary matter, the
permitted field content, derived lensing and conservation, correct gravity
limits, stable evolution, and an acceptable cosmology. The proposed scale
relation a0=(c/2)sqrt(G rho_Lambda) stays explicit as an input unless actually
derived. Agreement of simulations or formula identities does not derive its
coefficient. Numerical particles may sample a classical field or distribution;
their use alone neither violates a no-particle ontology nor derives the
independent carrier's dynamics and initial data.

The necessary chain is:

`one action + one branch definition -> full variation and constraints ->
one physical source/force operator -> healthy background and transport ->
same gate/kernel/epoch/shape parameters -> observable comparisons`.

The reviewed papers and scripts supply pieces of this chain. The missing
bridges cannot be replaced by adding their pass counts. The
[next-calculation work order](NEXT_CALCULATIONS.md) specifies the checks that
would move each open implication forward without repeating the old scans.

## Computation and delivery scope

The kernel, XC1, XC2 and dark-sector subdirectories contain independent
checks, contracts, logs, results and provenance manifests. These finite
checks support their stated algebraic or numerical assertions; they are not
full-theory certificates. Exact counterexample arguments and conditional
source dependencies are explained separately in each review.

The original simulation scripts and their result files were preserved. The
status entry points are annotated so that the disputed claims are visible
where future work starts. No commit, publication or message to another
person was made.

L386 has an incomplete log and no completed result JSON at inspection;
its actual process state is **unknown**. L387 has no completed result and
depends on L386. DE2 has a saved result whose W3 test fails, and source/output
freshness is unresolved. No new multi-hour run was launched: the gate and
operator mismatches must be resolved before those runs can answer the
same-theory question. Existing recorded costs were 3.67 hours for L380 and
1.52 hours for L381; those are historical measurements, not new runtime estimates.

**Review boundary:** this is a focused peer review of the newest calculations,
with extensions of existing exact checks. It is not a line-by-line audit of
the entire repository, a fresh observational analysis, a completed covariant
construction, or confirmation of a theory of gravity in nature.
