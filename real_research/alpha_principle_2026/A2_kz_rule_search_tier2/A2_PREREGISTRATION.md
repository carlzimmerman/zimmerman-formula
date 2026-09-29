# A2 -- tier 2 of the decoy-calibrated zero-knob rule search (pre-registration)

Written 2026-09-29 BEFORE `a2_kz_rule_search_tier2.py` was run. Same method, targets, hit criterion and decoy protocol as lane A1 (commit d2cadcdc0), with a DIFFERENT declared grammar, to widen coverage without leaving the zero-knob rule
(only kappa = 1/2, Z = 2 sqrt(8 pi/3), pi and group-theory rationals). Cumulative accounting is part of the design: A1 used 5,488,000 rules (P_chance = 0.001); this tier is sized so the CUMULATIVE rule count stays where the cumulative chance of a hit stays below 1e-2.

## Grammar (declared)
* Multipliers c_i from ALL distinct rationals p/q with p, q in {1,...,8} (45 values), independently per coupling.
* Common monomial A = pi^r * Z^p * kappa^q with r, p in {-1,0,1,2} and q in {-1,0,1} (48 monomials).
* Four scales: M_P, M_red, M_red/sqrt(118), M_P/Z; two normalisations (Y, GUT): 8 target sets.
* Rules: 48 * 45^3 * 8 = 34,992,000. Cumulative with A1: 40,480,000.

## Criteria (declared)
* S1 (power): P_chance (4000 decoys, same construction as A1) < 1e-2 for this tier; and the CUMULATIVE bound P_A1 + P_A2 < 1.5e-2.
* S2 (real result): the number of real hits H_real, each listed with offsets in sigma; a LEAD only if the tier's P_chance < 1e-3 (and then the cumulative bound is stated); no physical reading is claimed.
* S3 (positive control): 200/200 planted rules (drawn from the FULL multiplier set) recovered.
* MUTATE control: the search grammar silently loses its last multiplier (8/7) while planted rules use the full set: exactly S3 must fail: exit 1; exit 3 if broken.
* Expected (declared): 0 real hits; P_chance ~ 6 times A1's (about 6e-3).

## Amendment 1 (2026-09-29, after the first run; disclosed; no criterion changed)

(a) Count: the number of distinct rationals p/q with p, q in 1..8 is 43, not 45; the tier has 48 * 43^3 * 8 = 30,530,688 rules (cumulative with A1: 36,018,688), not 34,992,000. (b) RESULT AGAINST THE DECLARED CRITERIA: 0 real hits, but P_chance = 0.01425 (57 of 4000 decoys hit; 95% upper bound 0.018)
FAILS the declared power criterion S1 (P_chance < 1e-2), so this tier is NOT powered at the pre-registered standard; my declared expectation (about 6e-3) was too optimistic by a factor ~2.4 because the denser multiplier set (43 values with many near-duplicates in ratio) raises the chance density faster than the rule count. The cumulative criterion (P_A1 + P_A2 < 1.5e-2) also fails (0.001 + 0.01425 = 0.01525).
The script therefore exits 1 on its real run BY DESIGN (a failed declared criterion). (c) A wording bug in the first version printed 'the search is powered' whenever there were no hits; the verdict text now depends on S1 (the first-run output is kept as `a2_kz_rule_search_tier2_FIRSTRUN.out`).
(d) The control (grammar loses its largest multiplier while planted rules use the full set) was checked: exactly S3 fails and the script exits 1.
