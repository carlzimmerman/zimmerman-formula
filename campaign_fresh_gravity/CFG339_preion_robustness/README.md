# CFG339: robustness of the pre-reionisation cold-share candidate

**Verdict (frozen): ROBUST, 8 of 9 combinations.**

Tested: the candidate from CFG338, under
- the CFG317 yield bracket (-0.5 / -0.2 / +0.1), and
- the CFG336 formation-epoch bracket (UFD z_f 6/8/10, others 2/3/4).

The candidate is M_c = R_ind M_b / f_b, with max bookkeeping and the record collapse profile. A combination passes when all five dwarf populations (MW UFD, MW classical, M31 Collins, M31 LVD, LV field) are within 2 sigma on both footings.

The one failure is the extreme corner (yield +0.1, earliest z_f). There the classicals and M31 overshoot by 2.1-2.4 sigma.

**MUTATE** (R_ind permuted across populations) passes 0 of 9. The match depends on each population having its own measured baryon loss.

**Not blind:** the central combination was seen in CFG338, and this lane tests only its robustness.

Still required before this counts as a solution:
- (a) per-object loss factors instead of population medians;
- (b) a derivation of why the cold share tracks the pre-reionisation baryons;
- (c) a check that galaxies, lensing and clusters are unaffected. Large galaxies retain their baryons (R near 1), but this must be verified.

Run: `python3 campaign_fresh_gravity/CFG339_preion_robustness/cfg339_robust.py` (CFG339_MUTATE=1 for the control).
