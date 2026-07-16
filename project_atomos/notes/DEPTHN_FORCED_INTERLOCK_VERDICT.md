# Escalating constructive forced-interlock sweep, depth D>=6 — VERDICT (build validation @ depth 6)

**File:** `exhaust_depthN_forced.py` (depth-parametric, `--depth D`). Continues the committed
depth-3/4/5 CLEAN NULLS (commits ee44122 depth-4, 9230fbd depth-5). RULE 3 held: **zero git diff** on
`gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py exhaust_depth5_forced.py` — the
depth-5 machinery (nodes, `_decorate`, streaming dedup, the 6 GB watchdog, the parallel block, the a0
legs, the soundness leg, the committed-brute depth-4 completeness anchor) is imported and reused
VERBATIM via `import exhaust_depth5_forced as D5`. Only the skeleton/germ/split enumerator and the
per-depth completeness self-check are new (depth-parametric).

## The depth model (from the engine, verbatim)
`depth = build-steps + 1`. Total build steps at depth D = D-1. A Gate-B-passable DIMENSIONLESS tree
needs the germ triple {3, sqrt(8pi/3), one free} (>=3 decorate steps) PLUS a dimensionless scale
skeleton (>=2 scale leaves = >=1 binary step). Residual skeleton budget **R = D-4**. Depth 5 (R=1) had
one skeleton shape; depth D>=6 opens the three budget branches the spec flagged as load-bearing:
(a) more bare scale leaves, (b) POW/unary-decorated skeleton leaves, (c) extra same-value-free /
higher-power-forced germ steps. **All three are covered** by the generalized enumerator (budget splits
`budget_splits(D)`, skeleton layer `_skeleton_value_nodes` incl. pow/unary, germ layer `_germ_recipes`
with >=3 steps distributed over the 3 keys) and by the per-depth completeness self-check.

## Constructive scheme (three generalizations of depth-5)
A Gate-B-passable dimensionless depth-D tree = { dimensionless scale skeleton, budget b_s } x
{ germ recipe, budget g_s }, over every split b_s+g_s = D-1, g_s>=3, b_s>=1 (>=2 scale leaves).
Streamed one ExprNode at a time, **value-deduped** — the raw list is never materialized.

**Germ layer is CANONICAL (order-free, net-exponent).** Germ factors commute, so a recipe's value is
fixed by the NET signed-exponent per germ key. We enumerate (a) the composition of g_s steps among the
3 keys (each key >=1 step -> all present -> Gate-B tag fixed), (b) per key the distinct reachable net
exponent (`_net_exps`), emitting ONE canonical realization (`_realize_net`, exact memoized DFS). This
yields the IDENTICAL germ VALUE-factor set and the IDENTICAL Gate-B tag as the naive
`g_s! x (op x exp)^g_s` brute, without its over-generation. **Proven equivalent:** the canonical g_s=3
layer on the depth-5 skeleton reproduces the committed depth-5 distinct-value set EXACTLY
(**13,247 == 13,247, 0 missed / 0 extra**). (The naive brute made the depth-6 build blow past 10 min /
3.5 GB from a redundant `seen_canon` string set + ordering explosion; the canonical layer + value-only
dedup cut it to **9.8 s / 0.32 GB** with the same value set.)

## DEPTH-6 BUILD VALIDATION — all exit 0, peak RSS 0.42 GB (<< 6 GB cap)

| check | result |
|---|---|
| **a0-validity** (targeted, NOT brute) | **PASS** — LEG1 depth-4 dimensional re-derivation re-finds a0 `((c/Z)*H_L)=9.36018e-11` (rel_err 1.97e-5); LEG2 depth-6 identity tree `(((((c*H_L)/3)... )^1` evaluates to a0 (L/T^2), gate **FDR-DEAD** (expected: one forced provenance -> not overdetermined) |
| **constructive completeness** | **PASS** — per-split skeleton cross-check (scheme==independent brute): (b_s=1,g_s=4) 13==13, (b_s=2,g_s=3) 73==73, **0 missed / 0 extra**; committed brute depth-4 anchor reproduced **11,209==11,209**, dimensionless-<=4 empty both sides |
| **soundness** | **PASS** — 300/300 sampled depth-6 candidates pass the keep-predicate (Fset=={both forced}, \|Rset\|==1) AND the REAL `gate.forced_kernel` `kernel.passed=True` |
| **FDR non-smuggle** | **HELD** — Gate A density over the FULL 25-germ library (asserted len==25), mult = 21 targets |
| **single-target smoke** (`r_mu_e`) | exit 0, **CLEAN NULL** — 0 in-window matches, 0 CERTIFIED, 0 RE-LABELED |

**Depth-6 constructive size:** raw/target = **236,624** (splits (1,4): 13 skel x 9,936 germ recipes;
(2,3): 73 skel x 1,472 germ recipes) -> **107,719 distinct dimensionless values**. build **9.8 s**,
peak RSS **0.32 GB**. Brute depth-6 = 7.08e12/target (closed form) — the constructive scheme shrinks it
~3e7x. **Depth-6 verdict: CLEAN NULL (as expected/valid), gates fire, no certified survivor.**

## PROJECTED ESCALATION 7..10 (measured skeleton value-counts + measured depth-6 dedup 0.455 & RSS slope)

Measured skeleton value-counts (branch (a)+(b), incl. pow/unary): b_s=1->13, 2->73, 3->247, 4->1147
(the spec's bare-leaf floor 13/7/59/79 is exceeded by branch (b) — pow/unary inflation is real).

| depth D | splits (b_s,g_s) | raw/target | proj distinct | proj peak RSS | vs 6 GB cap |
|--:|---|--:|--:|--:|:--|
| 6 | (1,4)(2,3) | 236,624 | **107,719** (meas.) | **0.32 GB** (meas.) | under |
| 7 | (1,5)(2,4)(3,3) | 1,566,116 | ~712,900 | ~1.47 GB | under (last runnable) |
| 8 | (1,6)(2,5)(3,4)(4,3) | 8,123,807 | ~3,698,000 | **~7.15 GB** | **FIRST BREACH** |
| 9 | (1,7)..(5,3) | 38,488,660 | ~17,521,000 | ~33 GB | breach |
| 10 | (1,8)..(6,3) | 177,446,932 | ~80,780,000 | ~154 GB | breach |

## THE WALL (empirically anticipated)
- **Memory wall = depth 8** (projected ~7.15 GB > 6 GB cap), with **depth 7 the last runnable depth**
  under the cap (~1.5 GB). This is TIGHTER than the spec's projected depth-9/10 breach because the
  spec's projection used the bare-leaf skeleton floor; branch-(b) pow/unary inflation (measured b_s=3/4
  = 247/1147 vs floor 59/79) and the correct per-split germ-recipe growth pull the breach down to
  depth 8. Per the spec, **the runtime watchdog (`HARD_MEM_CAP_GB=6.0`), not this table, declares the
  ceiling** — `--escalate` runs 6->7->8... and STOPS the instant total RSS exceeds 6 GB.
- **Independent completeness-validation wall ~depth 8-9:** the honest per-depth skeleton-brute
  cross-check at b_s=4 already costs 107 s (24^4 x 11 sequences); b_s=5 (to validate depth 9) is
  ~40 min and b_s=6 (depth 10) infeasible — so provable per-depth completeness itself walls near
  depth 8-9. A depth whose completeness cannot be validated within budget has an **INVALID null** by
  the honesty constraint, so it is not certifiable as a clean null regardless of memory.

**Ceiling to report: depth 7 is the last fully-runnable+validatable depth under the 6 GB cap; depth 8
is the first projected memory breach (~7.15 GB) and the watchdog trip point.** Escalate with
`python3 exhaust_depthN_forced.py --escalate` to let the watchdog declare it live.

## Working-rule posture (both-ways, honest)
Depth 6 is a CLEAN NULL with the gates ACTUALLY FIRING (Gate A over the full 25-germ library, Gate B
overdetermined-forced, Gate C interlock) — no certified survivor, no manufactured win, no manufactured
dismissal. a0 re-derives + returns the EXPECTED FDR-DEAD (targeted construction, never brute). No git
commit. New files only: `exhaust_depthN_forced.py`, `notes/DEPTHN_FORCED_INTERLOCK_VERDICT.md`.
