# BF1_exhaustive_law_search, level L3: NO HIT. 2.1e9 expressions in three wrappers, zero Stage 1 survivors, same as the scrambled control. A near-miss family fits X-COP out of sample and breaks discs

Criteria: `FROZEN_CRITERIA.md` (f8e7d248fa, moved in 18622e62b3). `bf1.py`, `bf1_read.py`, `bf1_check.py`, logs. **Not blind.** kappa = 1/2 FITTED. No cold component. Reinstates nothing. Not theory closed. Nothing here says the data favour the framework.

| Run | Expressions | Prefilter hits | Stage 1 |
|---|---|---|---|
| real | 2.102e9 | 18 | **0** |
| scrambled control | 2.103e9 | 1 | 0 |
| MUTATE, gate 1 at 1e-6 | 2.102e9 | 0 | 0 |
| planted (1 + f) log1p(1/y) | 2.102e9 | 3.7e6 | recovered exactly, rms 0.0 |

Known answer: H = 1 gives X-COP +0.4675, 0.4763, record +0.467, 0.476. The L2 closure was 26,469, under the 150,000 cap, so the cap didn't bind. The prefilter is looser than Stage 1, so these counts are an upper bound on Stage 1.

## Near misses, no label
All 18 real prefilter hits are one family in W3: g = law x (about 0.7-1.4 + pi^2 g_gas / a0), where y f = g_gas / a0. They read X-COP train about +0.01 to +0.04, rms under 0.10, and on the 3 unseen clusters -0.04 to 0, rms 0.07-0.09. SPARC is the failure: rms 0.22-0.24 against the law's 0.166 and a line of 0.175, so **they fail gate 2**.

The term tracks LM1's "deficit is a multiple of the gas". 18 against the control's 1 isn't a significance: the 18 are one family, and the pi^2 was picked from 2e9 tries. Four train clusters plus three unseen is a thin test, on hydrostatic masses, and GM1 records that HSC lensing reads the same ratio about 1.7 times higher.

## Limits
Fixed Upsilon, pointwise rms, so the gate 2 statistic is noisier than FG1's. No fitted float, so a right form with an unlisted constant is missed. Three leaves only. Stage 2's later gates were never reached.

kappa = 1/2 FITTED. Not theory closed.
