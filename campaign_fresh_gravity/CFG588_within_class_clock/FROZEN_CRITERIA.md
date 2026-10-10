# CFG588 FROZEN CRITERIA — ACE: is there a colour clock INSIDE each class (early AND late) at matched mass?

(owner chat, "yes run the within-class version"). Committed alone before any lensing number in these bins.
CFG587 showed mixed-class colour bins cannot separate a clock from a class step. Here the class step is removed by
construction: separate intercepts per class, so only within-class colour can produce a slope.

Sample: f30 lenses; classes early (u−r > 2.0) and late. Within EACH class: colour residual δc = (u−r) − median(u−r) in that
class's own log M* quintile; tertiles of δc within the class (CFG585's construction for early is reproduced exactly).
ε per tertile from CFG531's estimator (cfg585_age.py head executed unedited; CFG529 validated environment); K9 PRIMARY
(where CFG585/586 found the signal), K-in reported; constructions A, B; both footings.
Covariance: joint 50-patch leave-one-out jackknife of the 6-vector (3 early + 3 late), Hartlap (50 − 6 − 2)/49.
Models (GLS):
 M0 STEP-ONLY   ε = a_E·[E] + a_L·[L]                       (no within-class clock)
 M1 COMMON CLOCK ε = a_E·[E] + a_L·[L] + b·δc_tertile        (one slope, ACE's single clock)
 M2 SEPARATE     ε = a_E·[E] + a_L·[L] + b_E·δc·[E] + b_L·δc·[L]
Verdict per cell:
 CLOCK IN BOTH CLASSES iff b (M1) > 0 with Z ≥ 2 AND b_L (M2) > 0 with Z ≥ 1 AND |b_E − b_L| < 2σ (consistent slopes).
 EARLY-ONLY CLOCK iff b_E > 0 with Z ≥ 2 and b_L consistent with ≤ 0 (Z_L < 1).
 NO CLOCK iff |Z(b)| < 1 (M1).
 Else MIXED. Overall = the same call in all four cells, else SPLIT.
ACE predicts CLOCK IN BOTH CLASSES; a morphology/class-specific effect predicts EARLY-ONLY or NO CLOCK.
Controls: C1 early tertile medians of log M* agree within 0.05 dex, same for late; C2 the early top/bottom tertiles reproduce
 CFG585's OLD/YOUNG ε(K9, A, canonical) +1.197 / +0.256 to 0.005.
MUTATE (CFG588_MUTATE=1): δc shuffled within (class × mass quintile); M1 slope must have |Z| < 2 in every cell.
κ = ½ fitted; footings never pooled; colour also tracks dust/metallicity/M/L; cold energy's mass required; not theory closed.
