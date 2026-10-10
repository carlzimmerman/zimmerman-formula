# CFG587 FROZEN CRITERIA — ACE first test: one colour clock, or a class step? (P1 + P3(i) of the ACE model)

(owner chat, "yes run the first test"). Model: campaign_fresh_gravity/MODEL_accumulating_cold_energy_2026-10-10.md (7a8faf7c8).
Committed alone before any lensing number in these bins.

Sample: all f30 lenses (57,265), CFG531's estimator (executed via cfg585_age.py's head, unedited), CFG529's validated
environment. Clock: colour residual δc = (u−r) − median(u−r) of ALL f30 lenses in the same log M* quintile (fixed mass).
Bins: six equal-count δc bins over all f30 lenses (both classes mixed); per bin record N and the early fraction f_E.
ε per bin in K9 (PRIMARY; where CFG585/586 found the signal) and K-in (reported); constructions A, B; both footings.
Covariance: 50-patch leave-one-out jackknife of the 6-vector, Hartlap (50 − 6 − 2)/49.
Models (GLS on the 6 bins):
 ACE  ε = a + b·δc_bin          (colour clock, no class term; linear-in-colour version, no age mapping)
 STEP ε = a + Δ·f_E,bin         (class only)
 BOTH ε = a + b·δc_bin + Δ·f_E,bin
Verdict per cell: ACE FAVOURED iff χ²(STEP) − χ²(ACE) ≥ 4 AND χ²(ACE) − χ²(BOTH) < 4; STEP FAVOURED iff the mirror holds;
 else UNDECIDED. Overall = the same call in all four cells, else MIXED.
P3(i) consistency (reported, frozen threshold): the ACE fit's predicted OLD−YOUNG difference at CFG585's δc medians must lie
 within 2σ of CFG586's measured D_env(K9).
Declared variant (report only): log-age clock τ ∝ 10^{δc / 1.0 mag} (u−r ≈ 1 mag per dex of age for old populations;
 RECALLED, PROVISIONAL), ε = a + A·τ/τ_ref.
Controls: C1 the six bins partition f30 and each has ≥ 8,000 lenses; C2 the all-f30 ε(K9, A, canonical) from the executed
 estimator reproduces CFG531's base value to 0.005.
MUTATE (CFG587_MUTATE=1): shuffle δc within (class × mass quintile) — destroys within-class colour information but keeps the
 class step; ACE must NOT be FAVOURED in any cell.
κ = ½ fitted; footings never pooled; colour also tracks dust/metallicity/M/L; cold energy's mass required; not theory closed.
