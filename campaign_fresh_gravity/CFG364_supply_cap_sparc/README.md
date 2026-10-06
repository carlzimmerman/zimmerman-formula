# CFG364: does the supply cap (dark mass = min(phantom, cold supply)) survive SPARC?

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 58840961d.

**Verdict: MARGINAL (canonical, primary) / DEAD (alt).** Never pooled.

| | canonical | alt |
|---|---|---|
| galaxies whose law phantom inside R_last exceeds 5.36 x their total baryons | **46 / 175 = 26%** | **57 / 175 = 33%** |
| dwarfs (V_flat < 60) | 7/17 (41%) | 8/17 (47%) |
| intermediate (60-150) | 24/64 (38%) | 30/64 (47%) |
| massive (>= 150) | 4/54 (7%): NGC 289, NGC 3198, UGC 6614, UGC 9133 | 5/54 (9%) |
| strict supply (baryons inside R_last) | 14% | 20% |
| **observed** dark mass inside R_last above 5.36 x baryons (model-independent) | **27%** | 27% |

Median Q = 0.69 (canonical). The largest Q are UGC 5750 2.8, UGC 5005 2.2, NGC 3741 2.2, UGC 128 2.2 and DDO 170 2.0.

**Reading.**
- Inside the measured radius, about a quarter to a third of real galaxies already need more dark mass than the entire cosmic cold share of their present-day baryons. That holds for the law's phantom and for the raw observed dark mass alike. The phantom keeps growing beyond R_last, so this is a lower bound on the cap's problem.
- Low-mass and intermediate galaxies are hit hardest. A cap keyed to present-day baryons therefore cannot be the rule.
- **The way out, untested here.** Galaxies are baryon-poor relative to the cosmic fraction (the missing-baryon problem; CFG317's leaky box). If the supply belongs to each system's ORIGINAL baryon reservoir rather than what is left today, the cap loosens by the inverse of the retained baryon fraction. That would make the cap hinge on baryon retention, a new quantity the framework would have to supply. That is exactly the move CFG338-344 used for the dwarfs.

**Disclosed.** In the first run the T0b control (the phantom identity) failed because of an arithmetic typo in the control itself: a stray "/ R". The main computation was unaffected. It was fixed after that run, which had already shown the verdict. All the numbers above are unchanged by the fix. Controls 4/4. MUTATE (supply x 0.1) gives DEAD with 99% breaking, rc 1.

Run: `python3 cfg364_supply_cap.py` (seconds).
