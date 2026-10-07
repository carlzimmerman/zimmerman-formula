# CFG375: the minimum energy any settling mechanism must handle (optimal transport), against the vacuum budget

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 402c886d0. Script `cfg375_ot_settling_energy.py`; less than 1 s of CPU. kappa = 1/2 is FITTED. Both footings are scored separately and never pooled. No dark-matter particle is added. The cold fluid's amount (5.364 M_b) is an input, not derived. This is not "theory closed".

## Verdict: ALLOWED on both footings, for both bounds. Two frozen controls failed and are kept (see below).

The question: settling the cold fluid from its never-collected Lagrangian sphere into the phantom profile inside the ownership edge (0.4 r_ta) has a minimum cost. Does that cost fit inside the local vacuum energy?
- The method: the optimal-transport map between radial measures is the equal enclosed-mass rearrangement.
- **The answer is yes, by 3 to 9 orders of magnitude.**

| footing | bound (a) kinetic, tau 10.3 Gyr | bound (a) kinetic, tau 1 Gyr | bound (b) binding B1 (primary) | B2 pure log | B3 Newtonian (eq. 1) |
|---|---|---|---|---|---|
| canonical, epsilon max | 7.4e-7 | 7.8e-5 | 3.1e-6 | 3.0e-6 | 1.0e-6 |
| alt, epsilon max | 9.4e-7 | 1.0e-4 | 4.0e-6 | 3.9e-6 | 1.3e-6 |
| epsilon min (both footings) | 2.8e-10 | 2.9e-8 | 1.4e-8 | 1.4e-8 | 5.6e-10 |

Here epsilon = E / (rho_Lambda c^2 V_catch). The ALLOWED cut is 0.1, because local a0 must stay uniform to 5% (a0 is proportional to sqrt(rho_Lambda)). Every cell is ALLOWED (12 host and f_ret cells per footing, each with both tau values and every potential variant). B2 and B3 give the same category as B1, so nothing is flagged.

**Example: the Milky Way (M_b = 1e11, canonical, f_ret = 1).**
- r_ta = 2.05 Mpc, r_out = 818 kpc, R_L = 1.56 Mpc, W2 = 768 kpc.
- E_kin = 2.8e51 J (tau 10.3 Gyr), E_bind = 5.2e52 J, against a budget of 2.5e59 J.

**Against CFG373 G4 (3e-8 to 1.3e-5).**
- At tau = 10.3 Gyr and for the binding bounds, every minimum sits at or below CFG373's upper end.
- With the fast 1 Gyr bracket, 3 of 12 cells per footing exceed it, up to 1.0e-4: M_b = 1e12 at f_ret = 0.18, and M_b = 1e13 at both f_ret values.
- So CFG373's G4 range is a slight underestimate for fast settling in massive hosts. It still passes its own 1e-3 cut, and it stays far inside this lane's 0.1 cut.

**Post-freeze stress number (reported, not a verdict input).** If the budget is only the vacuum energy inside the host (r < r_out) rather than the whole catchment, the worst cell is 1.1e-2 (alt, 1e13, f_ret 0.18, tau 1 Gyr). That is still under 0.1.

**Lean.** `CFG375_budget.lean` certifies the arithmetic only: at the worst cell's rational enclosures (E <= 1.38e58 J, B >= 1.37e62 J), E/B <= 1/10, and also <= 1/1000. It has zero sorry, and its axioms are listed in `CFG375_budget.lean.out`. It certifies no physics.

## What it means
- The vacuum can absorb the minimum settling energy on energy grounds. This holds for any mechanism, since the bound is the transport minimum.
- Energy is therefore not the obstacle. The open pieces stay open:
  - the settling FORCE (CFG60, and CFG373's assumed K ~ Gamma/c);
  - the rate Gamma;
  - the AMOUNT (5.364, not derived).
- This is a necessary-condition pass, not evidence for the model.

## Controls (frozen)
- **C1: FAIL, kept.** Two parts failed, both because the control was mis-specified at freeze.
  - (i) CFG100's own dta(0) = 11.7646, not 11.806 (CFG354 K4's value; CFG359 accepted it at 1%). The difference is 0.35% against my 0.1% tolerance. The script uses the frozen 11.806, which moves r_ta by 0.17% against the record's r_ta_law (the r_ta cross-check, also at 1e-3, fails narrowly).
  - (ii) The record's nu_mono (cfg100_lib) is the MONOTONISED kernel. It equals 1/(1 - exp(-sqrt y)) to 3e-9 for y < Y_P = 2.54 but departs by up to 2.4% in the Newtonian interior (y ~ 10). I wrongly assumed the two were identical.
  - Post-freeze sensitivity, `CFG375_KERNEL=analytic` (outputs `*_ANALYTIC`): the verdict is unchanged, and the epsilon maxima move by under 1% (B1 3.13e-6 vs 3.14e-6 canonical).
- **C2: PASS.** The monotone map's W2 is at or below the anti-monotone map's and 20 random quantile pairings in every cell.
- **C3: PASS.** The uniform-ball self-energy matches -(3/5)GM^2/R to 1.4e-10.
- **C4: PASS.** Mass is conserved.
- Because C1 fails, the main run exits rc 1.
- **MUTATE** (`CFG375_MUTATE=1`, outputs `*_MUTATE`): the anti-monotone map makes C2 FAIL as declared, rc 1, with W2 up 6-54%. The verdict categories do not change, because the budget margin is 3+ dex.

## Caveats
- **Point-mass baryons.** The phantom then sits mostly beyond the stellar disc, so this matters little for M_ph. B1's inner potential is the least certain part. B3 brackets it low and B2 high.
- **The supply binds in 11 of 12 cells per footing.** Only 5.36 or 29.8 M_b is available against M_ph(<r_out) = 21-244 M_b. So the transported mass is the supply, and the law is only partly realised inside r_out (the working model's open piece 4). Only M_b = 1e13 at f_ret = 0.18 is target-limited.
- **The source is the innermost part of the supply ball.** The target is the phantom profile, scaled. The self-energy counts only the transported fluid, and the background is ignored (Jeans swindle).
- **tau** is a declared bracket, not derived. E_kin scales as tau^-2, so it would reach 0.1 only for tau of about 32 Myr in the worst cell (canonical: about 28 Myr).
- **z = 0 only.** Physical densities today, Omega_c = Omega_m - Omega_b = 0.266. The ratio 5.396 differs slightly from the 5.364 used for supply, as declared.
- The OpenAI-math results 360 (regular OT) and 374 (Brenier W2^{1/3} stability) are cited as context only. The radial monotone map is exact here by uniqueness and symmetry, and C2 checks its optimality numerically.

Files: `cfg375.out`, `cfg375_results.json` (main), `*_MUTATE`, `*_ANALYTIC` (post-freeze sensitivity), `CFG375_budget.lean(.out)`.
