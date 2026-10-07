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
