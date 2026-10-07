# CFG412 FROZEN CRITERIA: screen the remaining switch-reader families for a filament-blind switch
(committed alone, before any script; light CPU; analysis of existing snapshots only, no PM run)

**Why.** CFG410: 86-89% of the residual growth excess under RES + MIX-A lives in T1-ON cells with l3 < 0, and a
plain l3 veto removes it but switches off host 3-stream / infall shells (KiDS +52, CFG355). The record proves that
no reader of the eigenvalues of Hess(psi) alone can be OFF in dense filament cores and ON at a host edge (CFG354 S8).
Wanted: ON in the single-stream infall region out to r_ta around every host and in the hosts; OFF in dense filament
cores; legal; at most 1 constant in total (T1's width eps = 0.077 counts as that constant if reused).

**Candidate families (declared now).**
- (a) Velocity-shear (V-web) readers. Particle velocities are NOT stored in the CFG410 z0 snapshots (pos, f, l3
  only), so the PM diagnostic uses the LINEAR-THEORY velocity from the z0 potential, v = -f H grad(Phi)/(4 pi G rho_bar)
  (DECLARED). Candidates: A1 = T1 AND (all three V-web eigenvalues converging); A2 = V-web middle eigenvalue at T1's
  threshold. The spherical-host test of (a) uses the NONLINEAR velocity of an analytic secondary-infall model (the
  record's Lambda shell ODE, a seed plus background, single-stream region between the outer caustic and r_ta).
- (b) Non-local readers. B1 = "turnaround cover": ON at x if x lies inside the turnaround sphere of some density
  peak c, i.e. the mean density in the ball of radius |x - c| about c, taken with the first-crossing rule from c
  outward, satisfies (Dbar - 1)/3 >= tau, smeared with T1's eps (0 new constants). Peaks = local maxima of delta on
  the deposit mesh. It reads enclosed mass (a Gauss flux of grad psi), not the potential's zero point, so it is not
  CFG353's reader. B1T = T1 AND B1 (min of the two smeared switches). B2 = khronon lapse / smoothed potential at a
  host-scale filter: assessed analytically (zero point or a filter-scale constant), not scored numerically.
- (c) Any other family justified in the README (beyond the closed CFG337-355 table).

**Measurements per candidate.**
1. PM diagnostic (an ESTIMATE; no PM re-run) on CFG410's BASE z0 snapshots, canonical and alt, re-deposited at 256^3
   on one thread: R_fil = 1 - M_fil(cand)/M_fil(T1), with M_fil = sum of (1 + delta) over cells with f > 0.5 and
   l3 < 0 (CFG410's mass weighting). Also the retained ON mass in l3 >= 0 cells, and an excess-share estimate
   Xhat = X_CFG410 * (1 - E_fil(cand)/E_fil(T1)), E_fil = sum over l3 < 0 of f_cand * max(s_ph - s_c, 0) (CFG410's
   RES pre-compensation excess source).
2. Spherical-host KiDS condition: in the record's spherical host (cfg100_lib r_ta_law, Delta_ta 11.765 from
   cfg100_lib and 11.806 from the CFG361 table), the fraction of r_ta out to which the reader is ON (f > 0.5)
   continuously from the centre; log M_b = 10.5, 11.0, 11.5 at z = 0, both footings, never pooled.
3. Legality and constant count. LEGAL = reads matter only (MS1 as relaxed by the owner), leaf-instantaneous
   (causality criterion B), leaf-covariant (G9) AND has a written action with defined Euler-Lagrange equations.
   CONDITIONAL = the first three hold but no smooth action with defined EL equations is written and checked.
   FAIL = any of the first three fails.

**Verdicts per candidate (per footing; the candidate's verdict is the worse footing).**
- PROMISING: R_fil >= 0.60, ON to >= 0.90 r_ta in every host and both thresholds, LEGAL, <= 1 constant.
- PARTIAL: at least one of the first two criteria passes and the constant count is <= 1, but not PROMISING
  (CONDITIONAL legality caps a candidate at PARTIAL).
- NO-GO: otherwise.
Lane verdict = the best candidate. If anything is PROMISING, state the CFG410-style RES + MIX-A PM run that would
confirm it; do not run it.

**Checks that can fail (main mode).** K1: re-computed T1 ON classification agrees with the stored f on >= 99.5% of
cells. K2: the l3 veto's ON-mass drop reproduces CFG410's 64% within 3 points. K3: linear V-web eigenvalues equal
f H x the Hessian eigenvalues to rel. 1e-4. K4: B1 on an isolated analytic sphere ends at r_ta to one grid step.
K5: the secondary-infall solver reproduces Delta_ta at the turnaround shell to 1%.

**MUTATE (CFG412_MUTATE=1, separate outputs).** Every candidate's reader is replaced by T1 alone; R_fil must drop
to |R_fil| < 0.01 for every candidate, and the script exits 1 (detected).

**Scope.** Bookkeeping reservoir; 256^3; z0 only; linear velocities in the PM leg; kappa = 1/2 fitted; both a0
footings (9.3603e-11 / 1.1312e-10) never pooled. The cold mass is still required; no particle species.
