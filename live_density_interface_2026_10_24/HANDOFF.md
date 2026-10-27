# Joint density checkpoint: exact continuation state

## Latest implementation supersedes the earlier numerical checkpoint below

Use `stable_compatible.py` and `stable_recovery.py`, runs LD-17/18, with
LD-19's `current_assessment.json` and `current_result.png`. LD-1 through14
used incompatible gravity/W quadratures that produced a core density comb.
LD-15/16 failed numerical checks before optimization; LD-17 repaired feasible
initialization, common enclosed-mass quadrature and the stable small-u W tail.
The cold bulk law now emerges to1e-6dex or better in the inner benchmark,
without empty/full-cell oscillations. The analytic law and seed instability
remain valid. The coupled transition deficit survives the corrected action.

Current n128 charge-free beta20,K3 result: inner law error.000317828dex;
to30kpc .2318066dex; to50kpc .353006dex. Outer T fraction.0677648, so the
original .05 gate is not passed. Reference interpolated radius44.8675539kpc;
joint -1kpc displacement returns44.8672683; +1kpc goes46.1210291 with energy
change -0.000524545Eunit. Do not substitute crossing-cell identity for recovery.
Material KKT residuals are .001–.009, not exact equilibrium. Tiny-seed branch
still fragments and does not recover the good inner core.

The full user goal remains open. No new physical density stiffness was added.
The next physical route must address transition depletion without hiding its
bulk-force effect or assuming a density profile. Local transport/conversion
dynamics could also test the still-unproved formation basin. The numerical
checks and new energy must be retained in either continuation. Earlier
charged high-resolution and high-K/domain8 tests remain resource-inconclusive.

## Earlier checkpoint (historical numbers, not the current implementation)

Base revision: 2ce8f3c2b80cefac2ac466cbebf3a7391dd6996a.
User goal remains open: finite restoring boundary, simultaneous material
equilibrium, a free outer reservoir, and galaxy-law emergence. No goal-complete
claim is justified. Read README, DERIVATION and AUDIT before another attempt.

## New information that must survive

1. The dark density is now variable. Gravity, W, phase stiffness, barrier,
   charge/tension and F pressure all enter one differentiable energy. Do not
   go back to inserting the target density or adding pressure after solving.
2. Pure cold T equilibrium exactly gives g²/(a0+g)=g_b+g_F. The original law
   follows only with negligible interior F. The all-T bulk numerical control
   recovers it from law-independent mass starts to about.001–.005dex.
3. Material relaxation subtracts a Schur complement from frozen-density
   stiffness. A positive phase Hessian alone remains inadequate.
4. F pressure creates a genuine charge-free seed instability. At Q=0, all-F
   has phase quadratic energy -(pi²/4) integral rho h_F x². But tiny-seed
   minimizations reached fragmented states; generic inside-out formation is
   not demonstrated. Pressure closure, dissipation and microscopic rates are
   still postulated/unsolved.
5. The beta20,ell30,K3,k=tau=0 front-start state recovers the inner law and
   retains substantial outer F, but evacuates a transition region. Its actual
   gravity error becomes .23dex to30kpc and .35–.36dex to50kpc.
6. At n128 its interpolated q=.5 radius is44.85947kpc. Joint perturbations
   -1 and+1kpc relax to44.87303 and46.12244kpc. Both energies are lower; the
   outward state does not restore. Merely reporting the same crossing-cell
   index would falsely suggest recovery. Material residuals also worsen.

## Evidence map

LD-1 run_joint:9 softmax live-mass minimizations; nonstationary and saturation
continuation states retained. LD-2 run_constrained:4 direct-mass states;
constraints and false optimizer success audited. LD-3 run_warm:3 continuations,
first two near stationary, third cap-active. LD-4 run_bulk:3 positive all-T
controls. LD-5 run_reservoir:3 invalid transferred starts, NOT physics.
LD-6 run_volume:3 corrected volume transfers; high-K states box-confined.
LD-7 run_radius:assertion failed before any optimization. LD-8
run_conservative_radius:4 species-conserving lower-tension trials; outer basin
has .003dex inner law but initial-basin dependence and material residuals.
LD-9 run_curvature:independent species transfer/Hessian checks and two relaxed
curvatures. LD-10 run_recovery:n256 charged run timed out before a final state.
LD-11 run_pressure:4 charge-free front/seed states. LD-12
run_pressure_refine:one completed n192 K3 state saved before timeout during the
remaining work; K10/domain8 and recovery not concluded. LD-13 run_checkpoint:
completed n128 refinement and two recoveries, with intermediate files saved.

## Do not repeat or silently reinterpret

Transfer both species conservatively in cell volume, reconstruct phase, and
verify u<1 before optimization. Recover actual source edges from cell centers;
do not use radius-linear cumulative mass. The corrective initial dilation is
recorded and is not an imposed final radius. Failed initialization says
nothing about mechanism viability.

Never count a saturation-cap-active result, box-confined reservoir,
empty-interior phase fraction, raw optimizer success or tiny softmax gradient
as an equilibrium. Report direct mass KKT residuals, true gravity, outer mass,
cap slack and phase residuals. Near-empty central cells can dominate a KKT
residual; locate them rather than hiding or rounding them away.

Do not equate same crossing cell with restored radius. Use interpolated q=.5
crossings plus energies/densities. Do not call a tiny inner force error a law
across the transition. Do not count all-T bulk control as free-reservoir success.

## Open continuations, not exhausted routes

* A genuine local transport/conversion evolution with heat accounting could
  discriminate the front-start basin from fragmented small-seed outcomes.
  The exact seed instability motivates it, but global SLSQP minimization is
  not physical dynamics. Do not invent rates or a Gyr timescale.
* Interface stress must be checked for whether it creates a material cavity.
  Adding a new density stiffness would require a new variational contract and
  its bulk-force correction; it cannot be called interface-only if it acts
  throughout a varying-density pure T interior. No such modification was tested.
* Charged n256 restoration and larger-domain high-entropy charge-free support
  remain resource-inconclusive. They may be resumed with checkpointed solves;
  their timeout is not an exclusion. They are lower priority than the already
  measured transition-law deficit and non-restoration of the simpler branch.

All work is local and self-reviewed. No manuscripts, prior experiments,
unrelated user changes, or observational catalogs were overwritten. No
independent reviewer was used. Current run statuses and validation results
are preserved; ongoing execution is not implied by a saved checkpoint.
