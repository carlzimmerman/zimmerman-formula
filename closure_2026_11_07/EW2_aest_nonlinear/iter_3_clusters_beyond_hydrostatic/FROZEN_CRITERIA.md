# EW2 iter_3 frozen criteria: does AeST's dust condense in deep hot wells (X-COP, groups) and stay out of discs?

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md before any script or number. Both footings,
never pooled. Loaders read-only: QX5 (xcop(), groups(); QX20 uses the same), QX10 iter_2's profile_from rule (baryons
interpolated log-log, flat beyond the last point at Mb_last). Need: the plain law's X-COP offset +0.467 / +0.435 dex and
groups +0.36 / +0.32 (fst 0) (QX20 KA values); the record's residue +0.44 / +0.41 (X-COP), +0.23 / +0.19 (groups).

## A. The static (hydrostatic) branch, on the measured wells (graded)

Static spherical v4 solve (iter_1 equations) on each X-COP cluster's baryon profile and on each Lovisari group (gas x
(1 + fst), fst 0 and 1, QX10's convention), Delta = 0 primary, at every declared member mu (iter_2's list) and on
iter_2's map over [1e-3, 1e3] Mpc^-1. M_AeST(<r) = g_AeST(r) r^2/G; D_i = log10(M_obs,i/M_AeST(<r_i)).
- X-COP gate (QX10 line): PASS iff |mean D| <= 0.05 dex and rms D <= 0.10 dex over the X-COP points.
- Groups gate (QX10 strict rule): a group passes iff every point has |D| <= 2 eM/(M_obs ln 10); PASS iff >= 16 groups pass
  at fst 0 and at fst 1.
- Zero-point envelope (reported only; a free per-object constant counted +1 if it is what passes): one universal
  Delta in [-8, 2] step 0.25.
- Static dust mass inside R500 reported per cluster: M_d = M_b - M_eff, against the need.

## B. Beyond the hydrostatic branch (graded as stated)

AeST's dust-like (time-dependent) behaviour exists on the scalar's dust branch only: comoving k < a mu on FRW, i.e.
physical scales above 1/mu (iter_1; H1's Jeans-type band below). A deep well can condense the field as dust inside
radius R only if the dust branch reaches R: mu R >= 1. Inside 1/mu the field is in its static branch (part A) or in the
band, where the record's dynamic reduced system (AN1 v3, Q0 -> infinity, spherical, K10-checked dust sphere) finds no
settling: at mu 0.0156-0.1 the 1e15 Msun rows gather M_d/M_ph 0.026-0.032 inside R500 (wrong sign against the X-COP
window), or fold at the centre; nothing past a fold is defined without a completion (X14: costs a constant).
- Gate DB (per footing): at every member that passes iter_2's G6 (the host side), the dust branch must reach the X-COP
  measurement radii: mu R_i >= 1 for the X-COP points (r_i = 0.3-1 R500). PASS iff it holds for >= 90 % of X-COP points.
  If no member passes G6, DB is graded at mu_h (iter_2) and at every declared member.
- Past the fold: NOT EVALUABLE (stated, not graded).
- Discs: the same dust must stay out of SPARC discs. Graded in iter_4 (SPARC on the same equations).

## Label

PASS if A (X-COP and groups) passes, or if DB passes and the dust branch is shown to supply the need (it is not computed
past the fold, so a DB pass alone gives NOT EVALUABLE, not PASS). FAIL if A fails and DB fails at every host-compatible
member, on both footings. Labels per footing.

## Known-answer checks

- KA1: mu = 1e-6: D reproduces the plain law's X-COP mean (QX20 KA: 0.467499 / 0.434523) to 1e-3 and groups to 1e-3
  (QX20: 0.358644 / 0.320274 at fst 0).
- KA2: dust bookkeeping: M_b - M_eff equals (mu^2/G) Int Phi r^2 dr to 1e-6 relative at R500 on one cluster.

## MUTATE (separate outputs *_MUTATE)

- M1 (lane MUTATE, K2 -> 0): static dust 0; D equals the plain law's (KA1 values) at every member, so the X-COP gate FAILS.
  Bites iff it changes D by more than 1e-3 at some member with mu >= 0.1 (shows the term acts).
- M2 (positive control of the grader): add to M_b at each X-COP radius the mass that makes the law return M_obs; the X-COP
  gate must PASS (|mean D| <= 1e-6). Bites iff it passes.
