# CFG483 — khronon-boundary settling class (C7): sigma^4 = G M_b a0 / 4

**FROZEN CRITERIA** (pre-registered, 2026-10-08, by the CFG461 repo review)

## Target (unchanged from CFG461)
Cold-fluid settling law sigma^4 = G M_b a0 / 4.  CFG461's RFI: every menu class
is c-free (does not contain a0, no-c-carrying), all gates G_a..G_e; the gap =
a no-flux boundary + an energy sink, both c-carrying, with NO new constant;
"the lead costs one constant unless the boundary and the sink come from the
same c-carrying field with a derived coupling".

## C7 construction (this lane)
1. **Boundary is derived, not inserted.**  The cold fluid (phantom, cosmic
   share M_c = (Omega_m/Omega_b) M_b, nu = 5.364) infalls from the turnaround
   and shocks.  The khronon-lapse field (G1, CFG373) provides the local total
   field F_tot = a0*nu(y)*y.  Post-shock the fluid is isothermal:
   2 sigma^2 = r F_tot(r).  The self-similar infall shock encloses (4/3) x the
   relaxed mass.  The no-flux surface sits where support = supply field AND
   the enclosed relaxed mass equals the cosmic share:
   F_tot(r_e) = (3/4) G M_c / r_e^2  =>  nu(y_e) = (3/4) nu  =>
   deep form y_e = 16/(9 nu^2),  r_e = (3/4) nu r_M = 4.02 r_M,
   g_tot(r_e) = 0.249 a0 (CFG461's edge class ~0.19-0.25 a0).
2. **Amplitude falls out exactly.**  Isothermal shock sigma^2 = (3/16) v_ff^2,
   v_ff at r_e, M(<r_e) via the enclosure: sigma^4 = (9/64) G^2 M_c^2 / r_e^2
   = G M_b a0 / 4 identically (the (9/64)(16/9) = 1/4 coefficient).
3. **Sink.**  Not required in this route: the infall delivers the kinetic
   energy; ram pressure balances post-shock support at the no-flux surface.
   The K^2 channel stays the record's standing CONDITIONAL item for the
   energy-conserving virial route (R_K ~ (alpha_c/c2)(V/c)^2 = 1e-11 short;
   direct lambda_x = +1 constant: CFG381) — reported, unchanged, NOT claimed.
4. **No new constant.**  Inputs: G, c, rho_L (a0), Omega_m/Omega_b, z_c,
   baryon profile; coefficients (3/16) (isothermal shock) and (4/3)
   (self-similar enclosure) are dimensionless physics, not fitted.
   kappa = 1/2 FITTED: both footings scored separately.

   NB: CFG461's own restatement (R0) used the law-output edge r = r_M/ln(1-f_b)
   = 5.85 r_M (+0.073 dex amplitude error, G-c fail).  C7's edge
   r_e = 0.75 nu r_M = 4.02 r_M is the mass-budget edge that makes the
   amplitude EXACT (0.0000 dex); the check "edge field in the 0.19-0.25 a0
   class" accepts both (0.19 vs 0.249 a0) and documents the difference.

## Pre-registered tests and kill condition
- G-b: |dex(sigma^4/true)| <= 0.10 (EXACT construction: 0.0000); amplitude
  delta-free.
- Scaling: d ln sigma^4 / d ln M_b = 1 (sympy control); d ln sigma^4 / d ln a0
  = 1 EXACT (a0 = kappa c sqrt(G rho_L): the c-carrying), tested at a0 -> 1.2a0.
- MUTATE: a0 -> 2a0  AND  M_b -> 10^10.5 M_sun inside the mechanism
  (baryon dependence dropped).  Expect amplitude ratio ~2.0 (+0.30 dex) and
  rc 1.  Fails => teeth (mechanism is not inserted-amplitude).
- FALSIFIER (experimental, novel prediction): the settled liquid phase of
  the two-valued SED must sit at phantom share
      eta_L = s_ph / s_c = 1 + (nu-1) f_b = 2 nu/(1+nu) = 1.6858
  (the liquid's phantom-to-baryon source ratio = 2 Omega_c/Omega_m; cf.
  CFG482 z0 GMM liquid component at x = +16.35 with modal s_c ~ 24
  => 1.681, 0.3% agreement claimed there).
  Estimator: ratio of means s_ph / s_c over the liquid population
  (s_ph = eta s_c is a LINEAR claim; per-cell ratios diverge where s_c -> 0).
  Population definitions counted: all x>0; sc >= p50; sc >= p75;
  x > 12 (GMM-like); the cut-ROBUST RANGE is the statistic.
  KILL: a 512^3 rerun whose liquid-population eta_L range lies FULLY outside
  [1.586, 1.786] kills C7.  At 256^3 the z0 result is UNDECIDED
  (range 1.306..1.724; GMM-like cut 1.724 = +2.3%).

## Verdict rules
- derivations (controls + amplitude + edge + G-c) PASS and falsifier PASS =>
  MECHANISM (sink status reported separately).
- derivations PASS and falsifier UNDECIDED => MECHANISM STANDING, kill armed
  (rc 1 with json falsifier field = UNDECIDED).
- falsifier KILL-BOX or MUTATE breaks nothing => KILL (rc 1).

## Lane status (as pushed)
PASS/UNDECIDED: derivations 7/7; amplitude exact; MUTATE +0.301 dex rc 1;
falsifier UNDECIDED at 256^3 (1.306..1.724 vs 1.6858), GMM-like cut 1.724
(+2.3%), KILL armed for the 512^3 rerun.