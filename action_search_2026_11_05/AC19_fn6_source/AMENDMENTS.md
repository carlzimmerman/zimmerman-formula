# AC19 amendments

## A1 (POST-RESULT, 2026-11-06): regime-consistent control MUTATE-B

The frozen MUTATE (rho_X ~ M^(-1/4), deep-MOND balance radius normalized to 2 kpc for the MW) did NOT
bite: its planted length has p = 3/8 and is 2 kpc, but the MW's r_M is 8.6-9.5 kpc, so a 2 kpc length
cannot be a deep-MOND balance radius and the grader's frozen regime check correctly rejected it. Its
outputs stay as ac19_MUTATE.json / .out (exit 1). By the frozen rule the label is NO VERDICT.

This exposes a structural fact used below: FN6's L_MW (1.5-3 kpc) is inside the MW's r_M, so any action
length that could fill the window must be a Newtonian-regime (r << r_M) balance radius.

MUTATE-B (added after seeing the main result, so labelled POST-RESULT): plant rho_X = A M^(-3/8) in place
of s^2, normalized so its Newtonian-regime balance radius 2 a0/(4 pi G rho_X) is 2 kpc for the MW on each
footing. Its exponent is 3/8 and it is regime-consistent; the unchanged grader must flag it PASS. Outputs:
ac19_MUTATE_B.json / .out. No main-run line, row, tolerance or exponent changed.
