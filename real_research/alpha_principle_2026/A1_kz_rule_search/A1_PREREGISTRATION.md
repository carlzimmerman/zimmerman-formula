# A1 -- a decoy-calibrated search over ~5.5 million zero-knob rules for the three gauge couplings (pre-registration)

Written 2026-09-29 BEFORE `a1_kz_rule_search.py` was run. The user asked for many lanes ('I dont care if we have to try 1000 lanes') under the zero-knob rule (only kappa = 1/2 and Z = 2 sqrt(8 pi/3) free, plus pi and group-theory numbers).
Lane Y1 (commit f73411efe) made the three Standard-Model couplings at the Planck-scale region known to 0.02-0.23%, which gives a programmatic search real statistical power that a search for alpha alone never had.

## The search space (declared, all zero-knob)
* **Targets.** For each of the declared scales S (8) and normalisations (2), the Y1 central values t = (1/alpha_1 or 1/alpha_Y, 1/alpha_2, 1/alpha_3)(S) with 1-sigma relative errors (0.23%, 0.021%, 0.12%) (Y1's errors at M_P used at all scales; Y1 reports M_red and the species scale within 0.01 percentage points).
  Scales: M_P, M_P/Z, M_P*Z, M_P/Z^2, M_P*Z^2, M_red, M_red/sqrt(118), M_red/Z. Normalisations: Y (a_Y, a_2, a_3) and GUT (a_1 = 0.6 a_Y, a_2, a_3).
* **Rules.** A rule is (monomial A, multiplier triple c): the predicted values are v_i = c_i * A, with A = pi^r * Z^p * kappa^q for r, p, q in {-2,-1,0,1,2} (125 monomials) and c_i drawn independently for each coupling from the 14 group-theory numbers
  C = {1, 2, 3, 4, 5, 6, 8, 12, 1/2, 1/3, 2/3, 3/2, 3/5, 5/3}. Rules per (scale, normalisation): 125 * 14^3 = 343,000; total = 343,000 * 8 * 2 = 5,488,000 rules. There are no free reals.
* **A hit.** All three predicted values within 3 sigma (Y1's relative 1-sigma) of the target: |v_i - t_i| < 3 * sigma_i * t_i for i = 1..3.

## Decoy calibration (declared)
The same search is applied to 4000 decoy target sets. A decoy multiplies each of the three coordinates by an independent random factor (1 + u_i) with |u_i| uniform in [0.03, 0.5] and random sign, the SAME three factors applied to all 16 (scale, normalisation) target sets so that the internal correlations are preserved.
P_chance = fraction of decoys with at least one hit anywhere in the 5,488,000 rules. A real hit is significant only if P_chance < 1e-3.

## Criteria (declared)
* S1 (power): P_chance < 1e-2 (the search must be powered; otherwise it is reported as unpowered and no hit means anything).
* S2 (real result): the number of real hits H_real; if H_real >= 1, each is listed with its (scale, normalisation, monomial, multipliers) and the 3-sigma offsets, and it is a LEAD ONLY IF P_chance < 1e-3; it then goes to adversarial follow-up (a physical reading is NOT claimed).
* S3 (positive control): a planted target t = (c1*A, c2*A, c3*A) for a random rule must be recovered by the search 100% of the time over 200 plantings.
* MUTATE control: the tolerance is set to 0 sigma; S3 must FAIL (and only S3): exit 1, exit 3 if broken.
* Expected (declared): no real hit; P_chance small (the search is powered).

## Reading rules
A hit would be a numerical coincidence between three running couplings and an expression; it would carry no physical claim until a mechanism is supplied. alpha stays an INPUT; kappa = 1/2 FITTED; the trial count (5,488,000) enters every probability.
