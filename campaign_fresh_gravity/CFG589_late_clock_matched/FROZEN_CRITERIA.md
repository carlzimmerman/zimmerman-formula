# CFG589 FROZEN CRITERIA — ACE: is there a colour clock in LATE types at exactly matched mass?

(owner chat, "OK" to the late-type follow-up of CFG588). Committed alone before any lensing number in these bins.
CFG588: common within-class clock Z +3.0; early slope +3.1–3.4 (Z ≈ 2.6); late +1.0 ± 1.0 (Z ≈ 1.00) with mass-unmatched
late tertiles (spread 0.11 dex, C1 failed). ACE predicts the same clock in late types.

Construction (mass-STRATIFIED tertiles): within each class, ten log M* quantile bins; inside each bin, colour residual
δc = (u−r) − bin median, and the lowest / middle / highest third of δc in THAT bin go to tertiles 0 / 1 / 2. The tertiles
then share the class's mass distribution by construction. Both classes built this way (early for comparison).
ε per tertile from CFG531's estimator (cfg585_age.py head, unedited; CFG529 validated environment). K9 PRIMARY, K-in reported;
constructions A, B; both footings. Slope by GLS on each class's 3 tertiles (ε = a + b·median δc), 50-patch LOO jackknife
covariance, Hartlap (50 − 3 − 2)/49; slope difference via the joint 6-vector covariance.
POWER (declared): CFG588's late slope error ≈ 1.0 per mag; if late types share the early clock (b ≈ 3.2), expected Z ≈ 3
(P(Z ≥ 2) ≈ 0.85); if the CFG588 late value (+1.0) is the truth, Z ≈ 1.
Verdict per cell:
 SAME CLOCK IN LATE TYPES iff b_L > 0 with Z ≥ 2 AND |b_E − b_L| < 2σ.
 LATE CLOCK, DIFFERENT SLOPE iff b_L > 0 with Z ≥ 2 AND |b_E − b_L| ≥ 2σ.
 NO LATE CLOCK iff Z(b_L) < 1 AND b_E − b_L ≥ 2σ (late slope significantly below early).
 UNDECIDED otherwise. Overall = the same call in all four cells, else SPLIT.
Controls: C1 within each class the three tertiles' median log M* agree within 0.02 dex; C2 early slope positive with Z ≥ 2
 (reproduces CFG588's early clock under the new construction).
MUTATE (CFG589_MUTATE=1): δc shuffled within (class × mass bin); late slope must have |Z| < 2 in every cell.
κ = ½ fitted; footings never pooled; colour also tracks dust/metallicity/M/L; cold energy's mass required; not theory closed.
