# CT5: candidate A (four-form tie inside screened v3s), RESULT: FAILS G0 (health), both footings

Grading lane under owner decision D1 and `../CT_GATES_COMMON.md`; gates frozen in `FROZEN_CRITERIA.md` before any number. A go to grade, not an adoption; the 2026-11-01 retirement stands; no particle. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Not theory closed. Nothing here says the data favour the framework.

Script `ct5_candidate_a.py` (sympy + numpy, 1.6 s, 0.12 GB, one thread) writes `ct5_candidate_a.out` / `_results.json`. Control `--mutate` (slaving off, eps = 0) writes `_MUTATE.*`: G0 then passes 19/19 (min M_L 1.002), so the failure comes from the tie, not the grader.

## The action and the derived slaving law
S_A is v3s (Khronon + P, switched stiffness, K(Q) dust) with Lambda removed from J_x, a0^2 = xi G q^2, and a Henneaux-Teitelboim four-form P(q) = Z q^2/2 - C0 (FROZEN_CRITERIA.md section 1). The A_3 equation makes Pi = dL/dq one global constant; q has no local mode and is slaved to the khronon acceleration. Derived symbolically (`.out`:3-10): the static limit is the simple-mu law S; on FRW q = Pi/Z is constant (w = -1); rho_DE c^2 = Z q^2/2 only if C0 = 0; kappa^2 = 2 xi/Z (a TRADE); and locally

    r [1 + eps h(x/r)] = 1,  r = a_loc/a0,  x = g/a0,  h = 2f - s f' > 0,  eps = kappa^2/(8 pi) = 0.009947.

## Gates
- **G0 health: FAIL** (`.out`:27-53). DOF 3, no ghost (dPi/dq/Z >= 0.826), total static operator elliptic (min dF/dg 0.0020). But the khronon's own J-flux j = g a_loc/(g + a_loc) is capped (X14), and the slaved a_loc falls with g, which tilts the capped branch downward. dj/dg crosses zero at x = 10.14 on both footings (about eps^-1/2) and stays negative until the switch-off at x = 1/eps = 100.5. On that band M_L < 1 (min -4.9e4), which breaks v3s's own condition M >= 1 (`switched_stable_where_positive`). For a 6e10 Msun point mass the band lies at 0.94-3.10 kpc (canonical) / 0.86-2.82 kpc (alt), where rho_tau > 0 everywhere. Growth e-folds in 1.0-1.6 Myr at wavelengths above 5-10 pc, even with L* = 21.7 pc. Near the pole, M_L tends to minus infinity, so the rate has no bound. No kappa > 0 removes the band; it is the v3s analogue of XR31's k04 fold. W4b is inherited and still UNDECIDED (CT2_REPORT.md:7).
- G1-G3 were not graded (the candidate stops at G0). UNGRADED READINGS from the same equation:
  - G1 law deviation: max 0.0043 / 0.0042 dex (`.out`:57-58).
  - G2 environment spread at 30 kpc: at most 0.0046 / 0.0036 dex, set by the cluster core (`.out`:59-71). This is under the 0.015 line, so CT1's expected decider would have passed; pointwise, 0.015 dex is reached at x = 6.5.
  - G3: a0 is flat in time. Against CPL (-0.75, -0.86, PROVISIONAL) the offsets are +0.086 dex at z 2.33 (`.out`:74).
- G4 not reached.

## Hand-set constants
kappa (= 2 xi/Z), C0 = 0, Pi (sets rho_DE), L*, mu_K, the form of J_x, and the dust abundance. Inherited v3s failures, unchanged: clusters, growth, BBN, hosted dwarfs, the MW disc, caustics (V3S_FINAL_VERDICT_2026-10-24.md:60-64). Dust phase: A supplies none tied to rho_DE (K(Q) has d rho/d a0 = 0), so it must come from elsewhere (CT8).
