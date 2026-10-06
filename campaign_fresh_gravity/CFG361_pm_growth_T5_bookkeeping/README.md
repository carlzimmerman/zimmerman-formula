# CFG361: CFG359's nonlinear PM growth with B's T5 bookkeeping: FAIL (A0-FLAT, both footings)

Criteria 6373544c3. Engine `cfg361_pm.py`, launcher `cfg361_run_all.py` (21 runs, work data in ../_external_data/cfg361_work/), analysis `cfg361_pm_growth_T5.py`, Lean certificate `CFG361_T5_bookkeeping.lean` (compiles, no sorry). Built by an agent and finished by the orchestrator: the analysis was run from the committed JSONs, and the Lean CRIT/S/K4 certificates were appended.

**σ₈ ratio to S0 at z = 0 (canonical / alt)**

| Run | σ₈ ratio | Verdict |
|---|---|---|
| T5 FLAT (lane verdict) | 1.205 / 1.257 | **FAIL** |
| T5 CRIT (the a₀ ∝ H(z) rival) | 1.50 / 1.59 | FAIL |
| T5 DE (reported) | 1.19 / 1.24 | FAIL |
| S FLAT (own verdict) | 1.194 / 1.249 | FAIL (canonical alone is on the TENSION side) |
| S CRIT | 1.49 / 1.58 | FAIL |
| T5F force analogue (reported) | 1.10 / 1.12 | TENSION |
| ADD (CFG359 reproduction) | 1.58 / 1.65 | FAIL |

**Reading.**
- Max bookkeeping removes about 65% of the additive excess, but not enough to pass.
- 94–97% of the ON mass is phantom-dominated, so max(phantom, cold) is almost always the phantom. That is why S's f_ex is 0 everywhere and S ≈ T5.

**Controls.** K1, K2, K3, K5 and K6 PASS.

**K4 FAILS, kept.** T5 FLAT canonical is 1.151 at 128³ (TENSION side) and 1.205 at 256³ (FAIL side). Higher resolution gives MORE excess, so the FAIL is not a resolution artefact in the lenient direction. It does mean the canonical number is not converged.

**What follows.** The phantom over-builds structure where the T1 switch is ON. CFG366's reservoir rule (another chat) removes most of the σ₈ excess, but at the host scale R_c = 3 Mpc/h it leaves +30% small-scale power. The cold fluid is still required. κ = ½ is fitted.
