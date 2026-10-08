# CFG358: N = 2047, the final grid for the zero-field nonlinear question (G5/G10). CONFIRMED-FAIL by the frozen letter, decided by the zero-guard

The criteria were committed first. The script is `cfg358_zero_field_N2047.py` (log `cfg358_run.log`, results JSON). Wall time was 42.7 h. 36/36 ν_mono runs were regular and convex. C1 (reproduction of CFG321) and C2 (GR control at order 2.0) pass.

| ε | λ at N = 63 … 2047 | increments Δ1, Δ2, Δ3 | frozen reading |
|---|---|---|---|
| 1e-3 | 0.0124, 0.0414, 0.0663, 0.0721, 0.0709, 0.0773 | +0.006, −0.001, +0.006 | fail pattern |
| 1e-4 | 0.0372, 0.0569, 0.0762, 0.0916, 0.0875, 0.0855 | +0.015, −0.004, −0.002 | CONVERGENT, λ∞ = 0.086 |

**Verdict: CONFIRMED-FAIL** (frozen rule: either set in the fail pattern). G5/G10 nonlinear dependence stays FAIL (CFG321).

**How the verdict is reached, stated plainly:**
- At ε = 1e-3, |Δ2| = 0.0012 is below the frozen ZERO = 0.005 (CFG322 lineage). The ratio rule therefore sets r3 = ∞.
- Δ3 = 0.0064 clears the 0.005 fail threshold by 0.0014.
- The λ values themselves wander within ±0.003 of about 0.073 over the last three grids, while the ε = 1e-4 set converges.
- So the frozen verdict rests on a single 0.006 bump that passes the zero-guard. This is recorded as a knife-edge, not reinterpreted.

**Scope.** This is 1-D only, and it applies to the UNGATED chassis: the law is on everywhere, including the open FRW background (CFG321's setup). It is not a test of candidate B, whose switch is off in unbound regions, and B's action does not exist, so for B it is untested. It says nothing about growth or σ₈.
