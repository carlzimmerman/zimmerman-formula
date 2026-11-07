# Outside solver's protocol for lane AK1 (filed 2026-11-07 ~16:40, before any AK1 number)

Pasted by the owner from the outside solver. Filed as a pre-registered expectation table for AK1; the AK1 lane owns
its frozen criteria and may adopt, tighten or reject these lines, stating which. Nothing here is a result.
Kappa = 1/2 FITTED; not theory closed.

## Three regimes the fold PDE can select at the D.P = 0 stream-crossing front

| Regime | shock width delta | post-fold clock speed v_post | with L* 22 -> 90 pc | with host depth (M234 vs M490, AC14 grid) | reading |
|---|---|---|---|---|---|
| I. local stiffness balance (CK2 baseline) | ~ L* ~ 22 pc | ~ sqrt(a0 L*) (Phi/c^2)^alpha ~ 1-100 km/s | L*^(1/2) | tracks v_f | REFUTED |
| II. non-relativistic caustic dispersion (Phi/c^2-suppressed) | ~ (L*^2 Phi/a0)^(1/3) = (L*^2 r_M)^(1/3) | ~ v_f^(2/3) (a0 L*)^(1/3) ~ 35-180 km/s | L*^(1/3) | v_f^(2/3) | REFUTED |
| III. relativistic unit clock-rate jump at the caustic | lambda_crit = (L*^2 c^2/a0)^(1/3) = 2.09 / 2.25 kpc | 2 c (a_geo L*)^(1/3) = 578 / 571 km/s | L*^(1/3) (x1.26 on doubling) | flat | CONFIRMED, theorem owed |

Regime III needs Q - 1 to reach O(1) locally inside the front (a foliation caustic), not O(Phi/c^2); the solver names
that as the only escape from Regime II.

## Observables and gates
1. Width ratio R_delta = FWHM of the D.P gradient pulse (or the c_s^2 grad rho_Q spike) at first fold, over
   lambda_crit. Gate 0.5 <= R_delta <= 2.0 on both hosts. R_delta ~ 1e-2 (20-100 pc) = Regime I/II.
2. v_post = mass-weighted rms of (v - v_bulk) behind the front. Gate 500-650 km/s with |d ln v_post / d ln v_f| << 1
   across the AC14 depth grid.
3. Mutations: L* doubled must shift the width by 2^(2/3) = 1.587 and v_post by 2^(1/3) = 1.260 (578 -> 728 km/s);
   Pi^6 -> Pi^4 core (b and C^4 continuity fixed) must lower v_post by ~sqrt(2); if v_post is unchanged under the
   branch swap the heating is gravitational phase mixing (~ v_f), not the F(Pi) core.

## Consequence the solver states if Regime III is confirmed
Because D10 bounds L* only from below (>= 21.7 / 22.9 pc), v_post in 500-650 km/s would require L* in [14, 31] pc:
a two-sided prediction that the outer globulars at 22-30 pc must begin to show stiffness-core departures.

## Orchestrator's caution for the AK1 lane
FS1/FS2 and AC14 are planar, non-dimensionalised folds. Before reading any of the lines above, state the mapping of the
code units to L*, a0 and c on both footings, and whether the solver's domain can resolve both 22 pc and 2 kpc at once
(a factor 100 in scale); if it cannot, say which regime the resolution can and cannot see, and freeze that.
