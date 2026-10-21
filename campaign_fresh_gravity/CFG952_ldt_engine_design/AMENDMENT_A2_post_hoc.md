# CFG952 AMENDMENT A2 (2026-10-21, POST HOC)

Written after the K, MUTATE and MAIN results were seen, and committed alone before the post-hoc stage below was coded or run.
The frozen grades and lane class stand unchanged: **SMOKE PARTIAL, with b1, c1 and c2 failing.** Nothing in this amendment can
move a grade; the stage it defines is a reported diagnostic for the design document.

## A2.1 What was seen

**K.** All pass (K1 2.2e-16 / 5.6e-17; K2 0.021; K3 0.013; K4 3.3e-9).

**MUTATE.** Every tooth bites:
- Mu1 −0.114 dex;
- Mu2 B/I 0.82;
- Mu3 J_trigger 2.77 against RAMP's max 0.94;
- Mu5 1.35.

**MAIN.**
- (a): a0, a1 and a2 pass.
- (b) DIPSLAVE: B/I 81, 145 infeasible steps from t = 2.56, dipole miss 0.83. DIPFREE gives B/I 0.79; LIN is infeasible from the first step.
- (c) RAMP:
  - trigger at t = 9.64, J at the trigger 0.025;
  - max J 0.94 at t = 28.6;
  - 44 infeasible steps over t 0.12–28.6;
  - max J before the first infeasible step 0.011;
  - zero-sum max 0.49;
  - book B/I 71.

## A2.2 Diagnosis read from the outputs

**Zero-sum (c2) and the J spikes (c1).** The zero-sum violations occur only on Newton-failure steps. When the Newton solve fails,
the frozen code keeps its last iterate, and that iterate satisfies neither zero-sum nor the dipole. This is an implementation
choice of this prototype, not a property of LDT.

**DIPSLAVE infeasibility (b1).** This is a real capacity limit. The slaved 𝒮 dipole (D̈_t = Σ S g) asks for a draw displacement
that the shell's positive, capped cold cannot supply.

## A2.3 The post-hoc stage (CFG952_POSTHOC=1; outputs cfg952_POSTHOC.out / cfg952_results_POSTHOC.json)

**FB-ZS fallback.** When the Newton solve fails:
- for each λ on a 41-point grid in [0, 1], each free component's λ_X is re-solved by bisection at β′ = λβ_last, so that zero-sum
  holds to round-off (positivity holds by construction);
- the λ with the smallest realised dipole miss is kept;
- the miss is recorded.

Converged steps are unchanged.

| run | draw | merge rule |
|---|---|---|
| PH-b | DIPSLAVE + FB-ZS | (b) as frozen |
| PH-c-RAMP | DIPSLAVE + FB-ZS | RAMP |
| PH-c-INSTANT | DIPSLAVE + FB-ZS | INSTANT |
| PH-c-NONE | DIPSLAVE + FB-ZS | NONE |
| PH-c-DIPFREE | DIPFREE + FB-ZS | RAMP |

Each run reports:
- max J, J at the trigger, and max J before and after the ramp;
- zero-sum max, number of infeasible steps and the max dipole miss;
- book B/I;
- the object separation history.

## A2.4 Reading rule (declared now, before running)

**Merge transition.** If, under FB-ZS, RAMP's max J ≤ 0.03 while INSTANT's J at the trigger ≥ 0.05, the continuity of the merge
transition is attributed to the ramp, and c1's frozen failure to the fallback artefact. Otherwise c1's failure is not explained.

**Momentum book.** The book residual B/I under FB-ZS measures the momentum the capacity-limited draw cannot carry. It is a design
number, never a pass.

κ = ½ FITTED; footings never pooled; not theory closed.
