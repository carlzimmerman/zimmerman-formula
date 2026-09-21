# Continue from the audit: derive, discriminate, and repair

Baseline: `3e857b5a6f8f05b48e29d0cbe42136998e9f9445` (2026-09-20).

**Start here for the next dispatch.** This follow-up adds twenty concrete execution cards, approximately 14.75 agent-days of bounded first decisions, with an explicit continuation after every supported, refuted or inconclusive result. Read [FOLLOWUP_PACKETS.md](FOLLOWUP_PACKETS.md); dispatch from [FOLLOWUP_TASKS.json](FOLLOWUP_TASKS.json). Inputs are pinned in [FOLLOWUP_INPUTS.json](FOLLOWUP_INPUTS.json).

These cards subdivide and sharpen the original 32 packets. **Do not add 14.75 blindly to the original effort estimate or assign another agent to duplicate the parent task.** The existing parent owner either adopts the card or hands off a disjoint part. Original lanes not refined here continue under [PROGRAM.md](PROGRAM.md). The output is a work order for the existing swarm, not a new running scheduler.

The objective is a coherent particle-free result that survives its own equations and independent measurements. A failed inference should lead to a corrected model, a scoped obstruction or a better experiment. It should not produce another declaration of closure with the same unresolved premise.

## First dispatch: cheap tests that control many downstream claims

| Order | Cards | Immediate decision | What this unlocks |
| --- | --- | --- | --- |
| 1 | R01, R02 | Exact active density, asymptote and integrated mass; isolate the finite-window slope artifact | Corrected rotation curves and the self-gravity branch |
| 2 | R06 | Unequal-mass force conservation under the PD20 premises | The actual action-derived two-body calculation |
| 3 | R10 | Which full force laws are mathematically the same model? | Correct attribution of quarter-slope, normalization and screening predictions |
| 4 | R13, R14 | What does the BH atmosphere independently measure about gravity and radius? | A noncircular population test and a useful observation request |
| 5 | R19 | Which load-bearing gates actually reject wrong inputs? | Trustworthy regression controls for every repaired branch |

R01, R06, R10, R13, R14 and R19 are initially ready for scientific work. R20 may prepare the integration ledger immediately but needs returned evidence before reporting results. R02 begins after the density contract is checked. Agents waiting for B1/B2/C1/B3/F1/B4 should help those original prerequisites rather than insert guessed equations.

Suggested eight-worker first allocation: one worker each on R01, R06, R10, R13, R14 and R19; one on the B2 full-source bridge; one on B1/C1 model/background reconciliation and integration. Transfer spare capacity to the ready proof or analytic control, not a new summary index.

## Three concrete mathematical targets worth pursuing

These are **conditional derivation targets**, not claims of new laws or completed Lean certificates. They make the next calculations precise. Every symbol and physical assumption must survive translation to the chosen action.

### 1. Replace the halo exponent with the correct integrated law

The L304 surrogate defines, with positive `B,D,u` and `0<K<2`,

```text
rho = (2-K) D (B u^2 + 2u^3/3)
w-1 = (2u/3)/(B+2u/3)
rho_act = (w-1)rho = (2/3)(2-K)D u^3.
```

With `u(B+u)=A/r`, `A>0`, its positive root satisfies `u ~ A/(B r)`. Therefore this surrogate approaches `rho_act ~ C/r^3`, not a density whose enclosed mass grows as a square root. For an exact `C/r^3` shell,

```text
M(r) = M(r0) + 4*pi*C*log(r/r0),    r >= r0 > 0.
```

The previous review independently found that fitting a pure logarithm with the same sampled interval and a zero mass at the lower cutoff gives an apparent power exponent about 0.578. R01/R02 must reproduce that calculation, certify the exact shell integral, and bound the actual profile's finite-radius remainder. Do not discard the interior mass or apply a large-radius asymptote automatically at observed radii.

### 2. Try a curvature discriminator that removes amplitude

Suppose the *same justified force prescription* gives

```text
v^4 = a0 G M_total(r),
beta = d log(v)/d log(r) = (1/4) d log(M_total)/d log(r).
```

Then proposed R03 certificates distinguish these mass continuations:

| Conditional mass model | Proposed relation |
| --- | --- |
| `M_total = Mbase + C_log log(r/r0)` | `d beta/d log r + 4 beta^2 = 0` |
| `M_total = Mbase + C_sqrt sqrt(r)` | `d beta/d log r + 4 beta^2 = beta/2` |

Use positive coefficients and a domain with `M_total>0`; record any further regularity and circular-motion assumptions. Derive the relations from the definitions and formalize them. These equations do not establish either mass profile physically, and the first force prescription itself still needs the full-source bridge. Their value is a precise comparison of shapes without fitting a separate amplitude into the comparison statistic. A curvature estimate requires a second derivative of noisy velocity data; R18 may find it impractical. That feasibility result is preferable to claiming a detectable prediction prematurely.

### 3. Test the feedback rather than assume it self-regulates

If, and only if, B2 establishes a genuine extra density `rho=A_g g^3` with constant positive `A_g`, and the deep force law uses its enclosed total mass,

```text
g^2 = a0 G M/r^2,
dM/d log r = K_g M^(3/2),
K_g = 4*pi*A_g*(a0*G)^(3/2),
M(r)^(-1/2) = M(r0)^(-1/2) - (K_g/2) log(r/r0).
```

This conditional system predicts a finite-radius singular continuation, with `d beta/d log r = 2 beta^2`. R04 must determine whether the physical approximation ceases to apply before that point. An inferred phantom density must not be reinserted as a second source. If the source is real and the obstruction is within the valid domain, find the pressure, supply limit, branch transition or coupling in the action that changes the equation. The new calculation must demonstrate that change; simply imposing a halo edge is not a mechanism.

## Continuation map

```text
R01 -> R02 -> R03 -> geometry/covariance gate -> R18
  + B2 -> R04 -> regulated action branch OR scoped obstruction
R02 + B2 -> R05 -> joint lensing/dynamics gate -> R18
R06 + B1 -> R07 + F1 -> R08 + B4 -> R09 -> R18
R10 -> R11 (new selector) and R12 (independent observable pair)
R13 + R14 -> R15 -> independent radius/covariance gate -> R18
C1 + B3 -> R16 -> R17 -> D1 action-to-Boltzmann interface
R19 supplies adversarial checks throughout; R20 integrates reviewed outcomes.
```

Arrows require reviewed inputs. They do not say a conjecture must be true before useful downstream work can happen. An explicit counterexample can close a proposed implication and become the starting point of a restricted replacement. If a branch changes the action, give it a new model ID and rerun every affected gate. Do not combine a favorable result from the old force law with a favorable result from the new cosmology.

Original goals still active: normalization inference A2; local constraints B4; abundance C4; the full action-to-Boltzmann mapping D1; cluster infall E2; validated geometry F1; high-redshift identification F4; and radial stability H4. This supplement sharpens their prerequisites; it does not mark them complete or discard them.

## How to keep progressing after each result

1. **After a proof:** extract the strongest statement with exact premises, compile the load-bearing theorem and print its axioms, then attack the first remaining physical bridge. Do not stop at a renamed consequence of an assumed law.
2. **After a counterexample:** preserve a minimal witness and identify the exact claim it refutes. Try a repair only when it changes a named equation, boundary condition or physical input. Run the counterexample again as a regression control.
3. **After a numerical result:** vary resolution, cutoff and an independently selected control. Derive a scaling or bound where feasible; another point in the same scan is not automatically more useful.
4. **After an identifiability failure:** exhibit the parameter transformation or covariance direction that preserves the observations. Choose a measurement with a different dependence, rather than increasing the sample size along the same degeneracy.
5. **After an unavailable input:** return the exact data/source/operator requirement, mark that branch blocked or inconclusive as appropriate, and take another ready independent packet. Never replace the missing input with the desired answer.
6. **After completing a packet:** the integrator assigns the next ready card, or records a new bounded card with a different mechanism. Preserve evidence and ancestry. A stronger theorem or a new empirical result must change the recorded claim, not only its headline.

Use the shared [result template](RESULT_TEMPLATE.md), include raw failed runs, and distinguish execution completion from mathematical or physical success. Start with an analytic or small control; retain the original program's bounded local compute policy. Continue within the already authorized repo work without repeatedly requesting routine permission. External publication, paid compute and messages to other people are outside this work order.

## Integration and release directions

Write only `followup_work/<ID>/` under this program directory. Propose changes to old scripts as patches inside the owned output; one integrator reviews and applies them directly to main. Do not edit historical PASS records to erase the failed version. Preserve unrelated working files, source ownership and frozen observation protocols.

R20 should maintain a model/claim table with five separate columns: exact statement, model/input revision, proof status, empirical status, and novelty status. A literature-supported known theorem with a new Lean formalization is valuable, but has a different claim from a new physical mechanism. The known isolated deep-MOND virial relation is a source to translate in R07, not a new result to rename.

Release candidates can be a corrected mass-growth theorem plus an observable test, a momentum-consistent two-body reduction, a noncircular normalization selector, a constrained cosmological operator with an initial-mode result, or an independently identified BH-layer test. A precise obstruction or calibrated observational limitation is also a legitimate outcome. Do not publish a universal physical claim by counting successful conditional lemmas.

The next checkpoint is substantive: at least one new reviewed theorem/obstruction, one independently validated forward calculation, or one demonstrably identifiable measurement. Report what changed and dispatch the next discriminator. There is no requirement to manufacture a positive breakthrough by a deadline.
