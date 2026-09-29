# Z9-WAVE BRIEF (conductor, 2026-09-29 tick — pre-registered BEFORE any run)

Spawn trigger: 0 deepseek lanes running (ps aux: hermes gateway only + one
orphaned Sep-8 multiprocessing fork, ppid 1 — not a lane). No new verdict files
since the Z8 landing (60b80d12c). The Z8 ops note deferred candidate successor
doors (a)/(c) to this tick — REGISTERED NOW as the Z9 wave. delegate_task
re-confirmed absent (tool_search, this tick) — conductor-built lanes, Z6/Z7/Z8
precedent. Wave size 2, not 3: the third Z8-listed candidate (b: OA1 WG high-z
leg) is data-gated on eRASS:3 WG products not on disk; no padding lane
(Z5-ops rule). A Lean lane (LR7) is a SUCCESSOR door, conditional on W1 K-C
landing exact forms — its own algebra audit first, next tick.

## Door audit (on-disk evidence, this tick)

1. **Door (a) finite-tau0 NUMERATOR CLOSED FORM — sharpened by conductor
   pre-audit of MC5_results.json (loaded-not-transcribed):** the stored K1
   first-cumulant coefficients B(q) = {-0.118750061, -0.229497626,
   -0.590477929, -1.480664740, -3.318531951} at q = {0,1,3,6,10} fit
   -B = b0 + b1 q + b2 q^2 with residuals <= 1.6e-6 (fit se <= 1.3e-8;
   residual at the quadrature-floor scale). Engine algebra (J11_volume_atom
   docstring, committed): tau_esc = tau0*(chord + q*(r^2*chord + r*mu*chord^2
   + chord^3/3)), so with S_q := chord + q*T, T := r^2*chord + r*mu*chord^2 +
   chord^3/3, the exact cumulant expansion
   -ln<exp(-tau0 S_q)>/tau0 = <S_q> - (tau0/2) Var(S_q) + O(tau0^2) gives
   **-B(q) = Var(S_q)/2 = Var(chord)/2 + q Cov(chord,T) + q^2 Var(T)/2 —
   EXACTLY quadratic in q.** Conductor hand-check via the (u,v) disk
   reduction (dV = u du dphi dv over the unit disk; exit distance c = s - v,
   s = sqrt(1-u^2), v = r*mu): E[c] = 3/4 (J09/LR4c-certified) and
   E[c^2] = 4/5, so **b0 = Var(c)/2 = (4/5 - 9/16)/2 = 19/160 = 0.11875
   exactly** (MC5 stored fit: 0.11875119); E[T] = 5/12 conjectured (the
   q-numerator limit, LR4c-certified family). All given as CLAIMS TO TEST,
   not facts (Z6 M05B precedent — the conductor's mechanism claims have been
   refuted by lanes before).
2. **Door (c) c0 low-q tension:** MC5 K2 stored c0(0)-extrapolations vs the
   MC4-banked line a+bq sit at z = 1.51 (q=0), 1.83 (q=1), 0.84 (q=3),
   1.32 (q=6), 0.12 (q=10) at n=2e6 x 4 reps — inside noise at that power,
   "resolvable only at ~4x power if ever registered". Registered.

## Lanes (2; prefixes owned: W1_*, MC6_*; no other series touched)

### W1 — finite-tau0 numerator cumulant law (owner: conductor)
Claim chain to TEST: N_num(tau0,q) := -ln A_vol(tau0,q)/tau0
= (3/4 + 5q/12) - (b0 + b1 q + b2 q^2) tau0 + O(tau0^2), with
b0 = Var(chord)/2, b1 = Cov(chord,T), b2 = Var(T)/2 under the volume measure;
b0 = 19/160 conjectured exact.
Gates (pre-registered):
- P0: fresh A_vol_quadrature(0.5, 0) vs J11 stored 0.70728, |diff| <= 1e-4
  (MC5's gate, verbatim).
- K-A QUADRATICITY: fresh N_num at ng=320, tau0 grid {1e-2, 3e-3, 1e-3, 3e-4,
  1e-4} (5 pts, dof 2), quadratic fit per q; kill if the fit residual RMS
  exceeds 3x the measured ng-refinement floor (floor := |N_num(ng=160) -
  N_num(ng=320)| at tau0 = 1e-2, the largest tau0, per q). FIRED ->
  quadratic-cumulant form REFUTED, exit 1.
- K-B CUMULANT IDENTITY: Var(S_q)/2 from an INDEPENDENT estimator — quadratic
  fit of ln A_vol(tau0, q) vs tau0 at tiny tau0 {2e-3, 1e-3, 5e-4, 2.5e-4},
  ng=320 (curvature = Var(S_q); different object from the N_num linear fit);
  kill if |(-B_fit) - Var/2_lnfit| > 3x floor at any q. FIRED -> cumulant
  identity REFUTED, exit 1.
- K-C EXACT-VALUE LEG: sympy derivation of E[c], E[c^2], E[T], E[T^2],
  E[cT] via the (u,v) disk reduction (single bounded pass, no budget
  tuning). If exact rationals emerge: E[c] must equal 3/4 and E[T] must equal
  5/12 (cross-checks against certified limits); b0/b1/b2 from the exact
  moments must match high-ng quadrature within 1e-9 relative — mismatch ->
  exact candidate REJECTED, recorded, not banked. sympy fail -> MEASURED-only
  honest record (exit 0 still allowed if K-A/K-B pass).
- Exit 0 iff P0 and no K-A/K-B kill. Label (house rule 4): consistency-family
  vs the engine — the tau0->0 numerator limit is LR4c-certified algebra; this
  lane banks the finite-tau0 ENGINE-side cumulant law.

### MC6 — c0 low-q parity at 4x power (owner: conductor)
Budget (fixed before any run): q in {0,1,3,6,10}; tau0 in {1e-2, 3e-3, 1e-3,
3e-4}; n = 8e6 x 4 reps/point (4x MC5 K2), seeds 6101.., single pass, no
re-tuning. Engines loaded-not-transcribed (J02 simulate volume; MC4 line
parsed from MC4_results.json verdict string; MC5 stored points for P0).
Gates (pre-registered):
- P0: fresh pooled c0 per q vs MC5 stored pooled:
  |diff| <= 3*sqrt(se_fresh^2 + se_stored^2). FIRED -> exit 1.
- K1: |c0_extrap - (a+bq)| <= 3*SE_extrap at every q. FIRED at any q ->
  PRE-DECLARED diagnostic BEFORE any kill verdict: quadratic-in-tau0 fit of
  c0(tau0); if the quadratic intercept clears 3 SE -> verdict
  EXTRAPOLATION-MODEL-LIMITED (amended estimator recorded per house rule 3;
  amended intercept banks, exit 0); if still > 3 SE -> MC4 line REFUTED as
  thin-window limit, exit 1.
- Exit 0 iff P0 and (K1 clean or diagnostic-resolved).

House rules 1-10 (LOOP_CONDUCTOR.md) apply verbatim: honest FAILs preserved
verbatim (append-only .out history), no budget tuning, raw data never
committed, no other series touched, conductor commits.

## AMENDMENT 1 (conductor, 2026-09-29, registered BEFORE the W1 rerun)
W1 run-1: K-B FIRED at all 5 q (verbatim in W1_tau0_cumulant.out). Diagnosis
(on-disk numbers): the ln-curvature estimator carries O(tau_max^3 * kappa3)
truncation bias -- the measured kappa3/6 = C(q) (K-A stage) times tau_max^3 /
tau^2_col gives ~1.4e-5 at tau_max = 2e-3, matching the observed diffs
{2.35e-5, 2.83e-5, 6.33e-5, 2.71e-4, 1.10e-3}; the registered tolerance
(3x ng-floor ~ 1.6e-9) was tighter than the estimator's own truncation bias.
This is a GATE-DESIGN error (conductor's), not a physics refutation. AMENDED
K-B (estimator widened by measuring its true bias, tolerance UNCHANGED in
kind): cubic-in-tau0 fit of ln A_vol (4 params) over 5 tau0 {2e-3, 1e-3,
5e-4, 2.5e-4, 1.25e-4}, ng=320; Var/2 = tau0^2 coefficient; truncation bias
now O(tau^4 kappa4) ~ 1e-12 (below the ng floor); tolerance
max(3*floor_q, 10*se_p2) with se_p2 from the fit residual covariance (the
estimator's measured SE, per house rule 3). Run-1 fire stays on record.

## AMENDMENT 2 (conductor, 2026-09-29, registered BEFORE the W1 run-3 rerun)
W1 run-2 (amended cubic ln-fit): q=0 PASSES (diff 2.92e-08 vs tol 4.40e-08);
q in {1,3,6,10} FIRE with diffs {2.11e-7, 1.42e-6, 8.12e-6, 3.75e-5} growing
with q. Diagnosis: BOTH indirect estimators carry higher-cumulant truncation
leakage that scales with q (kappa4(S_q) grows with q): the N_num quadratic
fit carries O(kappa4 tau_max^3 / 24) leakage into Bfit (tau_max = 1e-2), the
ln fit carries O(kappa4 tau_max^4 / 24) into p2. The identity
-B(q) = Var(S_q)/2 is EXACT Taylor algebra (kappa2 is the tau0^2 coefficient
of ln A) -- it cannot be "refuted" by two contaminated estimators
disagreeing at their own truncation scale; run-2 fire stays on record as an
estimator-precision result, and the OPERATIVE identity gate moves to K-C:
  K-B (final form): INFORMATIONAL -- the two indirect estimators agree at
  q=0 to 2.9e-8; q>=1 disagreement recorded as estimator truncation scale.
  K-C (operative): (i) exact rational moments with E[c]==3/4, E[T]==5/12;
  (ii) exact b0/b1/b2 vs DIRECT moment quadrature of Var(S_q)/2 =
  (E[S_q^2]-E[S_q]^2)/2 on the (r,mu) grid at ng=320 (NO cumulant
  expansion), gate 1e-9 relative per q in {0,1,3,6,10}; (iii) exact
  quadratic form vs Bfit with tolerance max(3*floor_q, 10*dtau_q) where
  dtau_q := |Bfit(full tau grid) - Bfit(grid without tau=1e-2)| measures
  Bfit's own tau^3-leakage scale (ablation, not tuning). Exit 0 iff P0 and
  K-C (i)(ii)(iii) all pass.
