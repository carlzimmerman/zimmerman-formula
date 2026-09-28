# Z7-WAVE BRIEF (conductor tick 2026-09-27 ~19:4x EDT)

Doors (from the register's standing OPEN list after Z6; barred list respected —
no SPARC-deep deficit, no V04/N01, no U-band A-chain, no Q-closure family search,
no KILLED doors, no ai_slop/autoresearch_v3). House rules 1-10 of
LOOP_CONDUCTOR.md bind every lane; no git commits by lanes; every number must
exist on disk; honest FAILs preserved verbatim; kills pre-registered HERE before
any number exists.

## Door 1 (lane LR4, owns LR4_*): cov discharge G2b-full
Upgrade LR3b_m05_reduction.lean's conditional theorems (chord_cond, I1_cond) to
UNCONDITIONAL by proving covStatement H for every continuous H. Proof plan
(conductor-derived, lane must verify every step): step1 (already certified)
turns the mu-integral into ∫₋ᵣ^r H(√(r²−v²), v) dv with factor r (multiply
step1 by r, valid also at r=0 where both sides vanish); split v>=0/v<0 with the
negation substitution; triangle-Fubini ∫₀¹∫₀^r Φ dv dr = ∫₀¹∫_v^1 Φ dr dv via
set integrals (setIntegral_indicator + integral_integral_swap + integral_of_le
+ Ioc_ae_eq_Icc); per-slice substitution r = √(u²+v²) via
intervalIntegral.integral_deriv_smul_comp (v=0 slice handled separately — |u|
is not differentiable at 0); half-disk Fubini (same set-Fubini skeleton on
D = {(u,v): u>=0, u²+v²<=1}). Toolchain v4.34.0-rc2, lake env lean.
KILLS (pre-registered): exit 0 iff covStatement discharged unconditionally with
chord and I1 statements zero-sorry (axioms ⊆ {propext, Classical.choice,
Quot.sound}); ANY sorry or remaining hypothesis -> exit 1 with the precise
remaining blocker recorded in LR4_cov_discharge.out/.err. No budget tuning.

## Door 2 (lane MC2, owns MC2_*): c0(q) linearity at higher power (MC1 recast)
Engine J02_moment_hierarchy.simulate (loaded, never transcribed). Budget fixed
BEFORE any run: q in {0,1,3,6,10}, tau0=1e-3, 4 replicates x n=6e6 per point
(n_eff = 2.4e7/point), seeds 1101..1120, Pool(8), single pass, no re-tuning.
Gates: P0 pooled c0 vs MC1_results.json stored per-q c0, |z| <= 3 each.
SE1 split-SE honesty: replicate-based SE of the pooled mean vs analytic
s_pooled/sqrt(n_eff): if replicate SE > 2x analytic -> SE-MODEL-MISMATCH flag,
record, do NOT bank (honest).
M2: weighted LS a+bq on {0,1,3}, PREDICT {6,10}; ANY |z_pred| > 3 ->
c0-NOT-LINEAR-HIGHPOWER (kill, exit 1). Else BANKED-LINEAR at n_eff=2.4e7 with
honest MDE; the thin-window curve R_v(0,q) = (3/4 + 5q/12)/(a+bq) is recorded
as CANDIDATE (not banked as exact law at this power).

## Door 3 (lane LR5, owns LR5_*): E[D^2] >= 3E[Dv^2]^2/E[v^4] Lean leg (register row 15, 'open (M01)')
R0 audit FIRST (numbers before Lean): mechanical sympy + synthetic-cloud check
of the J06 chain (J06_bound_sharpen.py verbatim: E[D ang] = E[Dv^2]/2,
E[ang^2] = E[v^4]/12, B_1 = 3E[Dv^2]^2/E[v^4] = E[Dang]^2/E[ang^2] under the
conditional-Gaussian identities v|ang ~ N(0, 2ang)); synthetic cloud
v|ang ~ N(0,2ang), D = 1.3*ang must attain slack 1 (bound tight), a noised
cloud must have slack > 1; the algebraic identity 3*(x/2)^2/(12*y) = x^2/(4*y)
checked symbolically. Lean targets (probed against the local mathlib before
writing): T1 unconditional Gaussian moment E[X^4] = 3 sigma^4 for X with
density N(0,sigma^2); T3 Cauchy-Schwarz in L2 for real RVs
E[D*ang]^2 <= E[D^2]*E[ang^2] (existing mathlib lemma may be cited/re-wrapped);
T2-lite the coefficient algebra as a real identity. KILLS: exit 0 iff R0 passes
AND at least one of T1/T3 compiles zero-sorry; if mathlib lacks the Gaussian
machinery, record the precise blocker, exit 1 honestly (the empirical leg
J06 86/86 stands regardless; this lane is the Lean leg only).

Ops: lanes spawned detached via Z7wave_launch.py (double-fork pattern, Z6
precedent); LR4 probe-compiled by the conductor before its detached verdict run
(recorded precedent); no lane touches another lane's files; raw data untouched.

AMENDMENT 1 (conductor, same tick, pre-first-successful-run): LR5 run-1 R0 caught a
coefficient slip in the conductor's own T2lite identity: 3*(x/2)^2/(12*y) = x^2/(16*y),
NOT x^2/(4*y) (recorded verbatim in LR5_ed2_bound.out run-1). The correct chain
identity is 3*(2*a)^2/(12*b) = a^2/b with a := E[D ang], b := E[ang^2]
(E[Dv^2] = 2*E[Dang] and E[v^4] = 12*E[ang^2] give B_1 = 3*4a^2/(12b) = a^2/b).
T2lite is RE-REGISTERED as that corrected identity; T3 (L2 Cauchy-Schwarz,
discriminant proof) unchanged; kills unchanged.
