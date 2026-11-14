# Latest exact-junction review and next closure obligation

**Verdict: incomplete, with a specific missing current-matching equation.**
XJ1 supplies a useful positive, mass-conserving spatial construction. It has
not supplied the velocity, polarization and stress fields needed to make
that construction evolve under the action. Its observational results are
finite results for chosen layouts, not a completed dynamical theory or a
theory of everything.

Review checkpoint: CJUMP_XJ1_2026_11_14. Assigned base was 38b52055e1; this
shared working tree was actively changing. First observed HEAD was
e278b5be2f07b1bc9e6f9e44c420367117d2631d. The final successful bounded run pinned
HEAD 3c8097b7a069e4ca29d1198d3002b904017c5600, dirty=true, with all 63
declared input hashes unchanged before/after. The per-file hashes, rather
than an assumed stable branch tip, identify the evidence reviewed.

## What the latest work actually changes

XJ1's `RESULT.md` distinguishes two materially different constructions.
The old FZS1 junction multiplied the interior cold profile by
s=C_R(R)/C_B(R); it preserved the reference enclosed mass at the junction.
The new construction leaves the supplied B profile unscaled inside, then
rescales the remaining exterior charge by
t=(T-C_B(R))/(T-C_R(R)). This is a substantive correction to what “the law
inside” meant in earlier summary statements.

In XJ1's stored build-B results, the exact junction makes f=2, f=3 and the
zero-velocity surface fail the flux-forest gate on both footings. The f=2
Delta chi-square values are 16.37/25.73, against a gate of 4. The proposed
second and third caustics give 1.213/1.648 and 0.512/0.691 respectively.
Those caustics were selected after earlier results were inspected. XJ1
explicitly calls them post hoc hits awaiting blind re-grade, and says the
action derives neither the junction nor the caustics. Its second/third
caustics use the reflecting-centre continuation beyond first crossing,
where the existing single-stream dynamics does not define that continuation.

These quoted forest numbers were read, not recomputed here. This audit
runs no forest boxes and no new shell trajectories. The source result
still described build A and bracket completion as pending at the pinned
revision. A blind XJ1R brief exists; no completed blind result was used.

“Unscaled B profile” must be kept distinct from “raw algebraic-law solution.”
FRZ1's mode B already caps its galaxy phantom profile at the available
model reservoir and contains other prescribed terms. The sibling
`../calculation/` audit addresses the reservoir and actual-law distinction.
The new theorem deliberately proves preservation of the supplied interior
profile rather than silently identifying every mode-B profile with the
uncapped algebraic law.

## Work executed in this review

`JUNCTION_THEOREM.md` gives a direct proof that XJ1's construction preserves
nonnegative cold mass, total mass, continuous enclosed mass and the supplied
spherical interior force under explicitly stated monotonicity and budget
hypotheses. Density continuity is an additional equality, not a consequence.

The same note derives the exact current condition

    [J^r] - Rdot [J^t] = 0,
    J^mu = n^mu rho_Q - lambda P^mu/Q.

QX17's stationary inner field equations force lambda_in=0, hence no inner
radial current. A stationary junction then requires the exterior
polarization flux to cancel any charge influx. If the exterior is strictly
polarization-free dust with positive charge and inward flow, the stationary
junction is impossible. This is a restricted exact-current obstruction,
not a full-action no-go.

For a moving front the explicit required exterior flux is

    lambda_out (P_out^r-Rdot P_out^t)/Q_out
      = rho_Q,out (n_out^r-Rdot n_out^t)
        + Rdot n_in^t rho_Q,in.

That equation is a concrete next boundary condition to solve. No current
XJ1 routine supplies its fields. In COL1's leading Newtonian advective
reduction, it becomes

    v_out = Rdot (1-N_in/N_out)

when the interior stands still and nonadvective flux is omitted.

The bounded script evaluated 7,110 active caustic-profile snapshots:
all 321 halo mass nodes, z=0 plus the twelve forest bins z=2.2,...,4.4,
both footings and k=2,3, with the existing v-star selection. Results:

| Check | Result |
|---|---:|
| Interior equals the supplied B profile | Exact on tested nodes |
| Maximum endpoint mass relative error | 6.66e-16 |
| Negative total-mass increments | None |
| Positive exterior cold density | 7,083 profiles |
| Degenerate exterior density, t approximately zero | 27 profiles, all z=0 k=2 |
| N_in/N_out < 0.999 | 3,706 profiles |
| N_in/N_out > 1.001 | 3,373 profiles |
| Within the density-equality tolerance | 4 profiles |
| Maximum one-sided-slope refinement change, positive-density cases | 3.18e-6 |

The 3,706 low-ratio cases require outward exterior velocity if the front
expands and the interior is stationary in the purely advective reduction.
They cannot simultaneously represent inward infall under those assumptions.
These are snapshot/grid counts, not abundance-weighted fractions, and no
front history or actual exterior velocity was inferred from equal halo-bin
indices at different redshifts. They identify a condition a dynamical
completion must address; they do not disprove every completion.

For example, at z=3 the third caustic requires outflow for 80 of 129 active
canonical profiles and 78 of 139 alt profiles. At z=0 those numbers are
38 of 240 and 48 of 250. Positive density alone therefore does not resolve
the transport issue even on the post hoc caustic candidates.

## Constructive continuation: an actual conserved transport path

`TRANSPORT_PATH.md` advances beyond the obstruction. For fixed monotone
reference/target cumulative charges with the same endpoints and a C1
mixing schedule, it constructs

    C(r,t)=(1-a)C_R(r)+a C_E(r),
    v=-a_dot(C_E-C_R)/[(1-a)C_R'+a C_E'].

This solves spherical charge continuity exactly, preserves positivity and
the fixed total charge, and gives zero origin/outer-boundary flux. It
allows the interior to move while assembling; it does not assume a static
interior throughout the path. For a=1-exp(-t/tau), strictly increasing
C_R and nondecreasing C_E give

    |v| <= |C_E-C_R|/(tau C_R').

A uniform bound additionally requires the displayed profile ratio to have
finite essential supremum. The target is approached asymptotically, and
velocity need not tend to zero where the final density is zero. The
arbitrary tau is not a derived physical timescale. Constitutive, force,
stress and energy equations are still unsolved. This is a proven kinematic
transport construction under stated assumptions, not a physical settling
mechanism.

The new checks give three symbolic zero residuals, two exact schedule/cap
identities and 36 rational trace checks, including a target with an outer
zero-density cap. The final run repeats all prior profile checks after
the CJ1 wording correction. The profile results match run_005 exactly.

An independent fresh-agent derivation verified positivity, weak
continuity, boundary/interface flux and the conditional bound. It found
one missing regularity assumption: mere differentiability of a(t) is
insufficient for the claimed weak equation. The theorem now requires a
continuously differentiable schedule; the exponential schedule qualifies.
The reviewer then returned “proved as written under its stated
hypotheses,” limited to kinematic continuity and the conditional velocity
bound. This review does not establish the field equations.

## Provenance, checks and scope

The accepted record is `run_007/manifest.json`, status `completed`, runtime
8.96 seconds, one numerical thread, 120-second wall cap and 110-second CPU cap.
`run_007/junction_checks.json` contains every profile and the five
symbolic zero residuals. Exact rational examples exhibit both an
inflow-compatible moving front and a positive junction requiring outflow.
The same result contains the constructive transport checks described above.

The finite-difference traces use relative radial steps 1e-4, 1e-5 and 1e-6.
The refinement gate is relative error 1e-3 plus absolute 1e-9 Mta/R, needed
because differentiating a numerically constant cap subtracts nearly equal
floating-point values. All positive-density cases are stable at much better
than the relative gate. Their ratios do not depend on the absolute floor.

Exploratory attempts are retained: run_001 lacked numpy under isolated
system Python; run_002 incorrectly assumed every outer density positive;
run_003 hit numpy-bool JSON serialization; run_004 exposed cancellation
noise at the capped zero-density profiles under a purely relative
convergence check. These are not theory failures or accepted evidence.
Run_005 passed the profile audit; run_006 added the transport checks and
corrected CJ1 source. Run_007 is the final finite verification, pinning the
independently reviewed C1 schedule restriction in the transport proof.

Reproduce from the repository root in a fresh output directory:

    python3 -B codex_mass_budget_2026_11_14/latest_review/run_checks.py run_008

Validate the accepted manifest:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py codex_mass_budget_2026_11_14/latest_review/run_007/manifest.json --root .

Key input SHA-256 values (full dependency list in the manifest):

| Input | SHA-256 |
|---|---|
| XJ1 xj1_lib2.py | cc05aea6029ace03ea383d66a3c38b7812a52cf52465231481001d83fe2a0d36 |
| XJ1 RESULT.md | 2edb45073ab132b909fbc59ee27ad6d6ba735d967691611bb3fd1bb42f3c5f7a |
| QX17 RESULT.md | dd2a318fbfb01a8449f33448547989ca4074e2ebae6925ffdee9937c951d010b |
| CJ1 COMPLETED_FORM.md | caeab2fe7f6cd061b36ed3b161e3b58dae2a1ea84bf75befc3d41e6b15c3a189 |

Independent review applies to the existing XJ1 sources; the new current
theorem is self-reviewed mathematical work. No external theorem is needed
for the displayed distributional calculation. QX17/COL1 are treated as
named internal dependencies, not independently recertified field theories.
Self-proofreading covered the new theorem, transport proof and report: no mathematical-token
correction was needed; all source claims and approximation limits remain
explicit. No existing source file was changed.

## Most useful next step

Use one tracked halo and one finite-width junction. Specify the actual
charge budget first, then solve the required full-current flux together
with QX17's polarization equation and stress/metric equations. Require a
finite, nonnegative charge density and show where infall energy goes.
Demonstrate that the resulting trajectory produces a settled law interior
and selects a radius or caustic index without choosing it from survey fits.
The present current identity makes that proposal testable before another
large forest rerun. A successful junction would close one important
gravity/assembly obligation; it would not by itself supply the fitted
constants, the unresolved kinetic function, or the quantum and matter
unification needed for a theory of everything.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
