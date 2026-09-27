# Z5-WAVE BRIEF (conductor tick 2026-09-27 ~03:1x EDT; successor to the same-tick Z4 landing)

House rules 1-10 (LOOP_CONDUCTOR.md) binding; leaf lanes do NOT commit. Detached
launcher Z5wave_launch.py (double-fork, silent-death fix). Honest remaining OPEN
doors after Z4: (1) J09p general-p window Lean leg (register rows 10-11, "open (M01)");
(2) the LOS-frame corrected discriminator plane (VE1 banked corr_los only at i=90;
V02's registered program completes by testing the corrected window across ALL i);
(3) O02's honest FAIL K2 "M-RISE not excluded" (register row 86: C07 split-0.15
+0.0775 SE 0.0247 = 4.3 SE positive, design-level arbitration missing). BARRED:
all U-rule rehashes (A-chain CLOSED), Q-closure (QF4 G2 STRUCTURAL closed), SPARC-deep
deficit sizing, V04, N01, ai_slop/autoresearch_v3, raw-data commits. 3 lanes (band
floor justified: only 3 distinct honest doors remain; no rehash padding).

## LR2 — general-p window law Lean certificate (J09p)
W_p(q) = (1 + q/(p+1)) / (1/2 + q/(p+2)), p : ℝ, 1 ≤ p, q ≥ 0. Theorems: denom_pos_p,
Wp_le_two (p ≥ 0), Wp_ge_limit (W_p ≥ (p+2)/(p+1)), Wp_antitone_q (cross-difference
= (b−a)·p/(2(p+1)(p+2)) exactly, by ring), Wp_mem (band). Numeric witness p ∈ {1,2,4},
q ∈ {0,3,10} (exact Fractions), all inside [(p+2)/(p+1), 2], decreasing in q. Exit 0
ONLY on compile rc 0 + zero sorry/errors + axioms ⊆ {propext, Classical.choice,
Quot.sound} + witness pass. Falsifier (J09p verbatim): measured deviation > 5 SE from
(p+2)/(p+1) at any p ∈ {1,2,4} — empirical leg stays with J09p (21/21); Lean certifies
the algebra only. Scope note in-file (I-series precedent).

## VE2 — LOS-corrected discriminator plane (VE1 completion)
corr_los(eps) = eps^p, p = −0.1061 central / −0.1307 volume (VE1 banked, on disk).
Fresh MC at q=0, tau0=1, eps ∈ {1.0,0.7,0.5,0.3} × i ∈ {20,40,60,90} × src (n=4e5,
Pool(8), fresh seeds = V02 seed_for + 911000, via V02_inclination.one_cell loaded-not-
transcribed). Gates (pre-registered):
 - P0 parity: fresh R_lo(0.5, 90) both srcs within 3 combined SE of V02 stored.
 - G1: with corr_los applied, R_corr(eps, i=90) within 3 combined SE of the eps=1
   anchor at every eps (both srcs) — the i=90 repair holds at fresh statistics.
 - G2 (the new content): across ALL i ∈ {20,40,60}, no (eps, i, src) with
   R_corr(eps,i) below the eps=1 SAME-i anchor by > 3 combined SE (ordering not
   inverted anywhere on the plane), else HONEST FAIL with the offending cells listed.
 - G3: U_los separates central-vs-volume at >= 3 sigma at every (eps, i) (V02's
   standing result re-verified at the lighter budget), else record honestly.
 Exit 0 iff P0 ∧ G1 ∧ G2 ∧ G3.

## OA1 — cluster a0(z) M-RISE exclusion design card (O02 K2 honest-FAIL door)
FEASIBILITY/DESIGN CARD ONLY (W03 precedent): no new physics claim, no new data.
Load O02_results.json + U02_arbitration_refresh_results.json (loaded, never
transcribed); recompute C07's estimators' z (K1 gate, 1e-9 on stored SEs); derive the
n-scaling card: clusters needed for 5σ from the best estimator (split-0.15
M500-matched, +0.0596 SE 0.0247 at n=7): n_5sig = n0 * (5/z0)^2; record the
pre-registered kill conditions for the future measurement lane (K2 verbatim: M-RISE
excluded iff the matched-mass estimator reads ≥ 5σ; sign flip at ≥ 3σ kills the
a0(z) cluster channel). Card written to OA1_DESIGN_CARD.md; exit 0 iff K1 recomputes
exact and the card carries stored numbers verbatim with provenance.
