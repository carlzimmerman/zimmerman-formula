# AS021 run_20260928T0007 — failed attempts record (preserved causes)

All three failures below were fixed by rerunning in the same unique run directory;
intermediate `err.txt`/`raw_output.txt` contents were overwritten by the succeeding
runs. The verbatim findings are preserved here so no cause is lost.

## F1. mpmath findroot stall on `y_p` (peak of h_RAR)
- Symptom (1st run, err.txt):
  ```
  Traceback ... File "compute_AS021_sign_domain_audit.py", line 159, in <module>
      y_p = mp.findroot(dhRAR, (M(1), M(8)), maxsteps=50)
  ... optimization.py, line 985, in findroot
      raise ValueError('Could not find root within given tolerance. '
  ValueError: Could not find root within given tolerance.
      (1.5589357398107888...e-34 > 2.6101217871994098...e-54)
  ```
- Cause: `dhRAR(y) = h_RAR'(y)` is extremely flat near its zero at y_p ≈ 2.5396
  (h_RAR'' ≈ 0 there), so the secant-style findroot stalls with |f| ~ 1e-34 at
  tolerance ~ 1e-54.
- Fix: replaced findroot with sign-based bisection to width 1e-45 in y
  (`bisect_root`), plus a single-sign-change verification on a 400-point grid.

## F2. Assertion `dhRAR not monotone on [1,8]` (initial bisection guard)
- Symptom (2nd run): AssertionError in the newly added monotonicity guard.
- Cause: dhRAR is NOT monotone on [1,8]: it has a minimum near y ≈ 6.7 (value
  ≈ −0.0325) then rises back toward 0 from below (dhRAR(12) ≈ −0.0255). The
  single zero on [1,8] is at y_p ≈ 2.5396; bisection only needs one sign change,
  not monotonicity.
- Fix: replaced the monotonicity assertion with `single_sign_change(...) == 1`.

## F3. Section D bug: deep-limit ratios ~3.4e10 (B passed as the a0 argument)
- Symptom (3rd run): `g/sqrt(a0*B)` printed 33778161059 at B/a0 = 1e-1 instead
  of ~1.05.
- Cause: the branch force functions were written with the Newtonian acceleration
  B1 = 1 m/s^2 hard-coded inside; Section D called `f(Bk)` (the small B) in the
  a0 slot. Physics of the branch definitions was untouched; the call convention
  was wrong.
- Fix: branch functions now take `(a0, B=B1)`; Section D calls `f(a0f, Bk)`.
  After the fix the ratios converge to 1 as B/a0 -> 0 (Q: 1+5e-10 at 1e-9,
  RAR/MU2/EXP/MONO: 1+O(1.6e-5)), matching the analytic first corrections
  {1/2 in y for Q; 1/2, 3/8, 1/4, 1/2 in sqrt(y) for RAR, MU2, EXP, MONO}.

## F4. Two check-definition defects (tolerances, not physics)
- (a) RAR/EXP `g - B` monotonicity checks failed because the 50-digit floor
  (0.0) plateaued; fixed with a floor-aware criterion (strictly decreasing
  until the floor, flat at the floor) — feature of the arithmetic, not of the
  limit behavior.
- (b) `deep_Q_first_coeff` was checked in the sqrt(B/a0) basis, but Q's deep
  expansion is analytic in B/a0 (sqrt(1+y) = 1 + y/2 - ...); the check now uses
  the branch-appropriate basis. This was a mis-prediction of the coefficient
  basis in the check, corrected without touching the physics.
