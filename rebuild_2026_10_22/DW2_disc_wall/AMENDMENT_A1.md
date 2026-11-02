# DW2 AMENDMENT A1. Written AFTER the first A4 run, before any harness run on MAX; part (a) A1-A3 still running, part (b) not started

**Disclosed:** A4's first run has been read. MAX with share mass and f_Q gave rms 0.0609, U 0.51 / 0.44, tilt +0.05 / -0.01, slope -0.015, LT -0.025, X-COP -0.020 rms 0.095 on the path of dw2_a4.py. That is a near pass I did not expect at that size. So everything below is post-result, chosen knowing it.

**Weakness found in that run, before the second implementation.** The X-COP row in A4 ties M200 to the cluster's own hydrostatic mass. It reads as a fit to the data, and it doesn't use the share rule the row claims. So X-COP in A4 is not a test of the share row. It stays printed, labelled generous.

**Second implementation = RQ2's acceptance harness** run on `cand_max_*.py`, separate SPARC loader and fit (CRG1), separate lensing, groups, X-COP, keys path, with this lane's candidate using its own contraction (bisection on r_f, no X39 code). The candidate sees only g_b(r) and r, never V_obs or a label except what the harness rules allow. Rule fixed now:
- M_b = largest g_b r^2/G on the system's arrays; M200 = M_b x (1 + 5.35) for "share", EM1 for "em1"; ZN2 shape, clamped at R200; contraction scaled by f (0 or 0.872), applied in every system, no selector; g = max(law(g_b), g_b + g_c).
- X-COP's arrays stop at 0.7 R500, so its M_b there is a floor. Primary: M_b continues linearly in r to R200 (rho ~ r^-2). Floor reported as `cand_max_share_fq_floor`. Choosing primary after seeing the generous row is disclosed.
- Where r is not finite (the Bullet map) the candidate returns the law, so B28 there is the law's map, not the rule's. The cold there isn't computed through this harness, and the row reads NOT COMPUTED for the rule.
- No VERTICAL given, so Milky Way and DiskMass read NOT COMPUTABLE, and are stated as open, with the note that g >= law everywhere so MAX can't relieve what the law overshoots.

**Lines:** RQ2's, unchanged, the harness's tolerances. Margins printed. Twin: cold x 10 must fail rows the real one passes. K8 now means agreement of the harness run with dw2_a4.py on rms within 0.003 and U within 0.03; if it differs, both are reported and the row gets no label.

**What a pass would and wouldn't mean, fixed now.** MAX is a description: no action, no field equation, a kink. It says the cold's gravity and the law's term don't add, and gives no reason. It is not a process, it reinstates nothing, and it doesn't show that cold exists in discs. At share mass, by construction it is close to the law in discs, so "passes in discs" inherits the law's pass and is weak evidence. The test with content is clusters, keys and lensing, where the cold branch runs.

kappa = 1/2 FITTED. Not theory closed.
