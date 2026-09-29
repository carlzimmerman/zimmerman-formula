# V1 -- what 'exact to many decimal places' can mean for alpha today (pre-registration)

Written 2026-09-29 BEFORE `v1_exactness_harness.py` was run. The user's requirement: a derivation must be exact to many decimals.
This lane quantifies what that requirement means against the CURRENT measurements and builds the acceptance harness any candidate must pass.

## Measured values used (all RECALLED from memory of the literature; they are inputs, not derived; each is labelled and the harness prints them)
alpha^-1 (relative uncertainty in parentheses):
* CODATA 2022 adjusted value: 137.035999177(21)
* CODATA 2018 adjusted value: 137.035999084(21)
* Cs recoil (Parker et al. 2018): 137.035999046(27)
* Rb recoil (Morel et al. 2020): 137.035999206(11)
* electron g-2 (2023 measurement, with the Standard Model / QED prediction) inferred: 137.035999166(15)
Because these are recalled, the numeric outputs are 'as recalled'; the STRUCTURE of the conclusions (the two atom-interferometer values disagree with each other far beyond their stated errors)
does not depend on the last digits.

## Declared quantities and criteria
1. For each measurement: relative uncertainty in ppb; for the Cs-Rb pair: difference in units of the combined uncertainty and in ppb.
2. The number of decimal digits of alpha^-1 that are established by ALL of these measurements jointly (the largest d such that all values agree to within their errors when truncated at d digits).
3. The acceptance harness (a function of a candidate's high-precision value): reports the candidate to 40 digits, its offset from each measurement in units of that measurement's sigma, the joint verdict
   'consistent with all', 'consistent with some', or 'inconsistent with all', and whether the claimed precision exceeds what any measurement can currently test.
4. MUTATE control: a candidate placed at the CODATA-2022 centre must be 'consistent with CODATA 2022' but must FAIL a control that shifts the CODATA reference by +5 sigma.
5. Expected (declared): the Cs-Rb disagreement is > 5 sigma; the digits established jointly number about 8-9; no candidate can be tested beyond ~10 digits today.

## Reading rules
alpha stays an INPUT; this lane derives nothing. It is a measuring stick.

## Amendment 1 (2026-09-29, after an independent re-run; disclosed, no result changed)

(a) The declared digit-count criterion (item 2) was NOT computed in the first version; it is now check A4 (the five central values share exactly 9 leading significant digits, 137.035999). (b) The first B1 compared a candidate with the reference that was built from the same literal,
so it was a tautology in the real run; B1 now tests that a bare decimal candidate is parsed exactly (no float round-trip), which also fixes a real defect (a bare decimal --candidate had been converted through a float). B3 adds a decoy (137) that must be inconsistent with all five measurements.
(c) The control was changed from shifting the CODATA reference to forcing the float parse, and it now exits 1 only if EXACTLY B1 fails, exit 3 if the control is broken. (d) The measured values remain RECALLED inputs.
