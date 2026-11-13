# CP02: the combined retention and external-field route, pushed through its dynamics

**The current QX17/PIK1 density-gated implementation is not a closed, healthy theory.** We have moved beyond identifying missing calculations: the full constrained scalar equations give an explicit instability, a separate leading-Newtonian experiment enters the corresponding local negative-response region, and the proposed quiet external-field transition violates the actual force equation. An inner galaxy force solution does exist. That success survives the audit, but it does not cure the failures of the complete construction.

This is a negative result about specified implementations and repair classes. It does not refute every possible realization of the Zimmerman relation or every modified-gravity theory. A universal impossibility claim would exceed the evidence. The original broad goal of a healthy predictive theory remains open; the original unrestricted quadratic-clock/flat-gate closure claim is contradicted.

**The final repair test gives a concrete incompatibility:** on the declared galaxy target, the pressure bound requires the clock coefficient below approximately **450/Mpc**. Keeping that same conserved component on the unchanged quadratic early-universe branch requires it above **8.89 million/Mpc** under the program's frozen radiation test. Even allowing stiff energy as large as all radiation requires above **2.30 million/Mpc**. There is no common setting. This uses the corrected equations and an independently reconstructed static bound, not the old growth threshold. [Joint proof and exact hypotheses](joint_obstruction/RESULT.md).

## What was actually completed

The [target contract](CONTRACT.md) began at Git `2207a1df48348f01ca1084d4add5d214c55d0e7e`. This is a shared dirty checkout whose HEAD moved during execution; input hashes and immutable snapshots, rather than Git HEAD alone, identify the evidence. No commit, reset or manuscript integration was performed by this phase.

The [previous phase](../combined_route/RESULT.md) corrected the mass accounting, external-field density interpretation, growth equations and several numerical/observational claims. Its results remain historical evidence. CP02 attacks the dynamical and matching steps that were missing there.

| Obligation | Executed result | Evidence |
|---|---|---|
| Exact conserved quantity and transport | Derived the gated covariant current and closed leading Newtonian equations; nonlinear evolution conserves total charge | [Current and evolution](current_transport/RESULT.md) |
| Full metric constraints in the stability test | Explicit regular positive-density constrained states have an unbounded short-wavelength scalar instability | [GR derivation](coupled_health/DERIVATION.md), [independent audit](health_audit/RESULT.md) |
| Changing the flat gate's shape | A calculus lemma extends the unrestricted-state failure to all positive, nonconstant, nonincreasing C² flat-origin multiplicative gates with the quadratic clock and fixed finite stiffness | [Family theorem](coupled_health/FAMILY_OBSTRUCTION.md), [independent lemma](health_audit/GATE_LEMMA.md) |
| Restricting to initially healthy states | A clamped-gate finite Newtonian evolution crosses from D<=0 to negative high-frequency response during compression | [Dynamics and controls](hamiltonian/RESULT.md), [independent review](health_audit/COMPRESSION_REVIEW.md) |
| Actual inner galaxy solution | A coupled physical-parameter annulus reproduces the reference force to 3.55e-7 fractional accuracy | [Static equations and runs](static_gate/RESULT.md) |
| Quiet return to the cosmological gate | An exact two-pole bound excludes an unchanged EFE field through that transition, including an arbitrary static clock offset | [Transition calculation](static_gate/RESULT.md) |
| Allowing a deformed, compensated exterior | Literal-gate static matching fails on the explicitly nonnegative polarization-principal branch; this is not every GR-healthy branch | [Matching proof](static_gate/matching/RESULT.md) |
| Stabilizing with a bounded clock piece and a Q-independent potential | The required stabilizer changes the actual polarization coupling enormously and destroys the retained force law with unchanged W | [Repair force test](static_gate/matching/RESULT.md) |
| Restoring the force with a Q-dependent compensator | An explicit convex/concave repair restores the force coefficient but necessarily carries excessive pressure on the specified galaxy target | [Repair construction and pressure bound](coupled_health/repair/RESULT.md) |
| Lowering the clock coefficient and restricting its range | The inherited growth bound is withdrawn; corrected growth is computed. The same conserved early history and static pressure requirement still have disjoint parameter intervals | [Growth/background audit](growth_gate_audit/RESULT.md), [independent joint audit](growth_derivation/BBN_STATIC_AUDIT.md) |

## Why the instability is a decisive new result

The old objection concerned only a polarization block. That was insufficient. Here lapse, shift, the metric scalar, tangency and the polarization constraint are all included. At the specified regular center, the physical high-frequency characteristic is

    omega² = (n_eff/A_infinity) k² + lower-order terms,
    A_infinity = Q² H_QQ - c²/D,
    c = 1 + gamma Pi - H_Pi + Q H_QPi,
    D = H_PiPi - gamma.

There are regular constraint data with n_eff>0 and A_infinity<0. An independently evaluated weak-offset example gives `omega²/k²=-2.90764228e-6`. The growth rate increases with wavenumber. It is not ordinary bounded gravitational collapse and is not removed by imposing the Einstein constraints.

The example is a stated action-family parameter witness, not a fit to an observed galaxy. The accompanying analytic theorem applies to every fixed finite positive clock coefficient and threshold and every fixed finite stiffness in the specified gate family, on its unrestricted classical state and wavelength domain. A justified cutoff or a proven restricted domain changes that claim; neither is supplied by the present action.

An [independently proved extension](health_audit/GATE_LEMMA_EXTENSION.md) also covers C² nonnegative monotone gates that reach exactly zero, with positive initial value and a flat origin. Its unstable witness lies where S is still strictly positive, before the zero-gate degeneracy. Setting the gate exactly to zero later therefore does not remove this counterexample.

Clamping the gate on negative Pi is a real change of action and was tested separately. In the finite periodic leading-Newtonian model, initially positive charge with D<=0 crosses into the bad region while the polarization constraint remains regular. Grid refinement and timestep halving agree on entry near normalized time .00174. Charge and energy conservation, endpoint constraints, and zero/reversed-velocity controls are recorded. This is evidence against automatic domain preservation, not a full relativistic formation calculation.

The independent GR audit found and corrected a cubic term missing from a radial Taylor series. It does not change the instability. The source snapshots, correction and separate series check remain available; agreement among agents is not substituted for the displayed derivation.

## What survives from the combined idea

Mass retention can change the local dark-to-observed-baryon ratio. The original cosmic ratio 5.41 is not a universal cap: reaching 59.5 requires `F_b/F_c=5.41/59.5`, approximately .0909244. This is an accounting requirement, not a prediction of the retention fractions.

The external-field response can provide a finite asymptotic effective mass in the reduced AQUAL problem. The effective density is signed, so interpreting it everywhere as positive conserved particle mass remains unjustified. The physical inner annulus now demonstrates that the gate can suppress the unwanted clock source without spoiling the force over a finite reference annulus. We therefore do not claim that no galaxy solution can exist even locally.

What fails is identifying those separately useful facts with one completed dynamical model. The full gate derivative modifies the force; its return to the cosmological regime cannot be treated as a quiet switch. The cosmological shift charge also retains a free integration constant. The derived current conserves it but does not select the required local retention history or the fitted kappa normalization.

## The strongest repair was constructed and tested

We did not assume that every stabilizing action was impossible. A nonmultiplicative construction keeps the original homogeneous clock behavior, suppresses clock energy and removes the identified positive-curvature problem. A first version fails because its stabilizing term also changes the force coupling. A second version exploits the exact boundary identity for Q Pi to restore that coupling.

The second version has a different, unavoidable cost within its stated class: positive pressure. The exact bound includes the full on-shell static stress, the original positive stiffness and the polarization potential. On the same canonical galaxy target, even the optimized pressure floor is about **2.06e12 times the outer polarization density** for the large cosmological clock coefficient. The lower imported coefficient still gives a ratio about 8001. These are conditional consistency tests of a specified target, not observational fits.

That pressure cannot be omitted while retaining the Einstein equations. A global subtraction would alter the original cosmological clock pressure. A new compensating sector would be another action, requiring its own derivation and tests. The [repair report](coupled_health/repair/RESULT.md) records both the successful mathematical construction and the force/pressure obstruction; it does not claim that no other action can exist.

We then weakened the requirement to the small rectangular clock range already present in the reference galaxy. The lower imported coefficient initially escaped a raw pressure exclusion. Following that remaining possibility exposed another inherited error: the quoted 25120/Mpc clustering floor used a polarization-off acoustic equation. The full cold dark energy's self-gravity factor is `mu²/(mu²+k_phys²)`. Corrected post-recombination growth was executed and independently derived; no replacement CMB likelihood is claimed.

The lower coefficient nevertheless fails the independent unchanged-history radiation test. Exact current conservation leaves a positive `a^-6` energy term in the homogeneous clock. Both tested repairs preserve it. Combining that early-history requirement with the deformation-permitting static lapse-flux bound gives the disjoint intervals stated above. The latter includes the full stress and positive Lambda benchmarks. The 0.067 early-radiation budget is a declared historical criterion, not a new empirical nucleosynthesis likelihood; relaxing it to 1 leaves a gap exceeding 5000 in the coefficient. The [joint report](joint_obstruction/RESULT.md) states every shared assumption and the changes needed to evade it.

## Status of broader continuations

The unrestricted flat multiplicative-gate family is rejected as an everywhere-healthy classical completion. Changing only its threshold, making its origin flatter, or rechecking its homogeneous background does not address the family obstruction.

A substantially different action, an independently justified physical cutoff, or a dynamically preserved restricted state domain remains a different research question. A deformed clamped-gate exterior also lies outside the literal-gate matching theorem. These are open alternatives, not successful repairs. The exact changes and remaining obligations are preserved in the [continuation handoff](HANDOFF.md); no open alternative is silently labeled impossible or completed.

The newly found errors and forward notices are recorded in [CORRECTIONS.md](CORRECTIONS.md). Historical numerical bodies and frozen criteria remain preserved.

The numerical evidence inventory and manifest checks are in `verification.json` and `artifact_inventory.json`. Failed controls, rejected attempts and superseded/custom-format execution records are retained and distinguished from accepted evidence.

Final provenance check: all **32 selected current schema-v2 evidence records validate**, including the three deliberately failing mutation controls. An earlier growth-derivation run became historically stale when its source report received the forward correction; the accepted replacement pins the immutable pre-notice snapshot and validates. Custom-format metadata remains archived separately. These integrity checks do not replace the proofs, independent reviews or declared computational limits.
