# T15 — the cold-fluid budget: who can afford a cold fluid?

**The ledger is exact and the framework loses.* With the record's own
calibration, the settled kernel supply at every clock over-predicts the
observed deficit — the cold fluid is forced NEGATIVE, and the T12/T14
line of work was reading one of three numbers in the record as another.

## The identity (Lean-certified, master cert #14–16)

    M_cold/M_b = x − f_law·S(<R)/M_b,   x = deficit = M_missing/M_b
    f_obs = 1/(1+x)                     (deficit_to_fraction)
    M_cold ≥ 0  ⇒  f_law·S ≤ x·M_b      (cold_ceiling)

## The branch audit (S1) — the record's numbers mean THREE things

| value | CFG382 meaning | → settled f | T12/T14 read it as |
|---|---|---|---|
| 0.14 | leftover e = e^{−Γt} | 0.86 | f (wrong branch) |
| 0.60 (groups) | leftover e | 0.40 | f (wrong branch) |
| 0.43 (clusters) | leftover e | 0.57 | f (wrong branch) |
| 0.79/0.41 (b=0) | deficit x = M_missing/M_b (def-A) | f_obs = 0.56/0.71 | — |
| 1.76/0.91 (b=0.3) | deficit x (def-A) | f_obs = 0.36/0.52 | — |

The T12 "three-clock λ confirmation" fitted the settling law to
deficits-as-fractions, inflating the settled phantom by S/M_b = 4.98–6.15
within R500 — that is the audit's factor-2.37/f>1 mess: the ledger
straining. T14's scatter readings inherit the same branch error; only
the f-only fork survives as exponential-law content.

## The overdraft (S2) — 6/6 PASS, MUTATE flips C2–C5

| clock | f_law (CFG382 λ=0.028) | deficit x | M_cold/M_b | verdict |
|---|---|---|---|---|
| MW 30 kpc (V=188/200/230) | 0.86 | 1.48/1.80/2.70 | −0.97/−0.65/+0.25 | negative at the measured level |
| groups (b=0 / b=0.3) | 0.286 | 0.79/1.76 | −0.93/+0.04 | negative; knife-edge at b=0.3 |
| clusters (b=0 / b=0.3) | 0.286 | 0.41/0.91 | −0.98/−0.48 | negative at every b |

- The settled kernel supply at R500 exceeds the deficit by 2.2× (groups,
  b=0) and 3.5× (clusters, b=0). At the MW calibration point itself the
  floor-implied phantom (0.86·2.85 M_b with M_b(30 kpc) = 7e10) exceeds
  the rotation-implied missing mass by ~65% (V=188).
- Ceilings: f_law ≤ 0.0824 (clusters, b=0), ≤ 0.1285 (groups, b=0);
  λ_max = 0.0073–0.0117 vs the floor λ = 0.028 — **no single universal λ
  survives the cluster budget** (3.8× margin); T12's fitted range
  [0.029, 0.066] violates the b=0 cluster ceiling by ≥ 3.95×.
- The MUTATE control IS the historical error: identifying f_law :=
  deficit reproduces the T12 illusion and violates the ledger harder
  (M_cold = x(1−S) ≈ −2 to −9) — C2–C5 flip as declared.

## The forced reading (S3)

At R500 the settled fraction is the RESERVOIR fraction: f_res = x/S =
0.0824–0.183 (clusters across b), 0.128–0.286 (groups) — not 0.286, not
T12's 0.43. The deficit itself is the reservoir (CFG379/CFG365
compatible: baryon-depletion ordering). The cold fluid's derived
large-scale law: ρ_cold(R) = (1−f)·ρ_res — a flat/equilibrium
complement, distinguishable from cusped CDM profiles by calibrated
lensing fits. Its small-scale clumping scale (T_cold, needed by
CFG344's ultra-faint mechanism) remains OPEN — the budget constrains
its mass (≈ 0 at every clock; ≤ 0 inside R500), not its temperature.

## Falsifier (registered)

A lensing-calibrated R500 deficit (one footing, known b) clearing the
settled kernel supply without negative cold fluid (deficit ≥
f_law·S/M_b for a universal λ — i.e. ≥ 2.2–3.5× the b=0 values) kills
S2. The ledger also closes EXACTLY at the groups b=0.3 point without
any cold fluid (deficit 1.76 = f·S) — the knife-edge that separates the
reservoir reading from the overdraft.

## Lean (master certificate extension)

`deficit_to_fraction`, `cold_budget_identity`, `cold_ceiling` — 3 new
theorems; the master file now holds **17 theorems, all audited** to
{propext, Classical.choice, Quot.sound}, zero sorry, rc 0.

## Bottom line

The framework's cold fluid has no budget at any clock under the
record's own settling calibration: the settled phantom alone
over-predicts the observed missing mass at R500 (2.2–3.5×) and at the
MW calibration radius (~1.65× at V=188). The cold fluid is not an
option — it is a contradiction — unless the settling is far slower than
the floor calibration (λ ≤ 0.0073–0.0117 at cluster/group densities) or
the kernel supply is replaced by the deficit-reservoir inside R500. The
T12 λ-confirmation and T14's scatter readings both inherit the branch
misread; the budget is the reason the audit's numbers refused to be
fit.

## Correction (dated 2026-10-07) — MW-30 row: unit mix in the script

The T15 script mixed units in the MW-30 row: the deficit x was computed
in M_b = 1e11 units while S(<30 kpc) used M_b = 7e10 (enclosed baryons)
— the reported −0.97/−0.65/+0.25 were wrong. Corrected (both in M_b =
7e10 units; x = (M_tot − M_b)/M_b with M_tot from V):

    V = 188 km/s:  x = 2.53, S = 2.85, f·S = 2.45 → M_cold = +0.08
    V = 200 km/s:  x = 3.00 → f·S = 0.86·2.85 = 2.45 → M_cold = +0.55
    V = 230 km/s:  x = 4.29 → M_cold = +1.84

**The MW-30 point CLOSES (positive cold fluid) — it sits on the
knife-edge:** the deficit approaches the kernel supply (f_max = 0.89 at
V=188; the budget becomes INFEASIBLE (deficit > supply, M_cold < 0
unavoidable) for V ≳ 195 with M_b = 7e10. The boundary: M_b(30 kpc) ∈
[6.4, 7.3]e10 at the measured flat level — a mass-model test, not a
coupling test. The groups (−0.93/+0.04) and clusters (−0.98/−0.48)
rows are unaffected (same M_b convention in x and S there). T15's other
conclusions stand untouched: deficits ≠ settled fractions (branch
error), the cluster/group overdraft, the λ ceiling 0.0073–0.0172, the
T12-range violation (≥ 3.95×), the reservoir reading, MUTATE = the T12
identification.

## Correction (2026-10-18, calc chat; owner go): the group/cluster overdraft is a units mismatch
The group and cluster inputs 0.79/1.76 and 0.41/0.91 are CFG382 definition A,
x_A = (M_tot - M_b - M_ph)/(5.364 M_b): the excess beyond the law, per cosmic cold share. They are not
x = M_missing/M_b = (M_tot - M_b)/M_b, the definition stated in FROZEN_CRITERIA and used for the MW-30 point. The exact
relation is x = 5.364 x_A + (nu - 1) (verified per object to 4e-15). The tell is in T15 C1 itself: f_obs(clusters) =
1/(1 + 0.41) = 0.709, while X-COP measures f_b = 0.163 (b = 0).

On the stated definition (campaign_fresh_gravity/CFG453_t15_deficit_units, criteria b1132dd48, result de0514adb; both
a0 footings, never pooled), with x = 5.12/7.74 for clusters and 10.8/15.9 for groups at b = 0/0.3:
- Clusters M_cold/M_b = +3.8 to +4.3 (b = 0) and +6.4 to +6.9 (b = 0.3); groups +9 to +14. Positive, not overdrawn.
- No lambda ceiling: the dark mass exceeds even the fully settled kernel supply, so the floor lambda 0.028 is allowed at R500.
- Clusters dark mass = 0.95 of one cosmic cold share; groups 2.0 (gas-poor, f_b 0.084).

Therefore, NOT TO BE CITED:
- S2 (the group/cluster overdraft, "cold fluid forced NEGATIVE"), S3 (reservoir fraction 0.083-0.28; "cold fluid
  (nearly) absent at cluster scales"), C3-C5 (the lambda ceilings 0.0073-0.025, the T12 violation >= 3.95x) and C4's
  f_res windows, for groups and clusters.

Unaffected: the MW-30 rows, which use the stated definition (the T16/T17/T18 MW knife-edge stands as computed), the
budget identity and the Lean certificates (arithmetic only), and the branch-audit point that leftover e is not settled f.
T17's motivating "reservoir complement (T15)" rests on S3 and should be read with this note. CFG382's own P2 cluster miss
(leftover branch, like-for-like) is a separate result and stands. Nothing above this section was changed.
