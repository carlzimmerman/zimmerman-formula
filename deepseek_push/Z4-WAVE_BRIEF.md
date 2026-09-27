# Z4-WAVE BRIEF (conductor tick 2026-09-27 ~02:3x EDT)

Spawn gate: 0 deepseek lanes running; load 3.61/16; >=1 OPEN door. 3 LIGHT lanes on
3 DISTINCT OPEN doors (load-gate precedent Z2 tick). delegate_task re-confirmed absent
via tool_search (0 matches) — conductor-run detached pattern (double-fork launcher
Z4wave_launch.py, the V03b/V03c silent-death fix). House rules 1-10 (LOOP_CONDUCTOR.md)
binding on every lane; leaf lanes do NOT commit. Files claimed by prefix+name.
BARRED (register): SPARC-deep deficit sizing (premise moot per D02); V04 factorized
N=1 route (V04b mechanism); N01 density-locality (KILLED); all U-rule rehashes
(A-chain CLOSED by A5); ai_slop/autoresearch_v3; raw data commits (WALLABY tsv stays
UNTRACKED).

## QF4 — Q-closure finer-tau0 rerun (door: QF3b recast, verbatim: "the residual is
tau0-grid/structure bias ... door recast to a finer-tau0 rerun"; n-scaling CLOSED).
Goal: measure E[Q] on an INTERSTITIAL tau0 grid {0.4, 0.7, 1.5, 2.5} x q {0,3,10} x
{central,volume} at n=6e5 (fresh seeds 20260930+90000+, Pool(6), checkpoint
QF4_stage1.json), reusing L02_q_functional.measure, QF1 evaluate, QF2 run_table (loaded,
never transcribed). Pool with the QF3+QF3b replicate tables (n_eff 1.2e6 at original
tau0) into a DENSER tau0 table; evaluate the QF1 families on it.
Pre-registered (fixed BEFORE any number):
 - P0 parity: 2 fresh original-grid cells (tau0=0.5,q=0,central; tau0=2,q=3,volume)
   must match QF3_stage1 E_Q within 3 combined SE, else machinery FAIL, exit 1.
 - G1 BANK (verbatim QF1 gate): best in-fit <= 3.0 SE AND best holdout <= 5.0 SE
   (central AND volume) on the DENSER grid -> CLOSED FORM BANKED, exit 0.
 - G2 STRUCTURAL: best in-fit > 6.5 SE -> tau0-grid discretization is NOT the cause;
   Q-closure door CLOSED honest-FAIL at the current engine; no successor rehash.
 - G3 partial (<= 6.5, not banked): discretization bias CONFIRMED as contributor;
   project the tau0 density needed from the measured improvement; door stays OPEN.
 - bookkeeping gate: max |Q - X| < 1e-9 on every cell (QF3b verbatim).

## VE1 — LOS-frame window correction (door: V02 registered next, verbatim:
"measured LOS inflation ~= eps^-0.10 central / eps^-0.13 volume vs the frozen-frame
eps^-0.35 / eps^-0.38 ... An LOS-frame re-derivation of the window correction is the
registered next step"). Goal: re-measure R_lo at i=90 (edge-on LOS), q=0, tau0=1,
eps {1.0,0.7,0.5,0.3} x {central,volume}, n=6e5, fresh seeds (V02 seed_for + 555000,
Pool(4)) via V02_inclination.one_cell (loaded, never transcribed); fit the LOS
inflation exponent; deliver corr_los(eps) and decide the portability of the K10
frozen correction.
Pre-registered:
 - K0 parity: fresh R_lo at (eps=0.5, i=90) matches V02_results.json stored R within
   3 combined SE (each src), else machinery FAIL exit 1.
 - K1 exponent decision (at eps=0.3, deepest lever): p = ln infl / ln eps with delta-
   method SE; LOS-FLAT if |p - (-0.10)| <= max(2 SE, 0.03) central / |p-(-0.13)| <= ...
   volume; FROZEN-LIKE if within the same band of -0.35 / -0.38; both/neither ->
   MEASURED-OTHER recorded honestly (no forced call).
 - K2 power-law adequacy: |ln infl_meas(eps) - p ln eps| <= 3 sigma_ln at EVERY eps
   in {0.3,0.5,0.7} (both srcs), else the single-exponent correction fails -> record.
 - K3 portability: with corr_los = (eps/1)^p applied to V02's STORED R_lo tables, the
   corrected LOS window R_corr must NOT invert: R_corr(eps) >= R_corr(1.0) - 3 combined
   SE at every eps (both srcs); the frozen K10 correction reproducing V02's inversion
   (R_corr(0.3) central 0.530 / volume 0.507 < anchor 0.685, from stored tables) is
   the contrast. All four of K0/K1/K2/K3 recorded; exit 0 only if K0 pass AND K2 pass
   AND K3 pass (K1 records whatever it measures).

## LR1 — M-roads Lean roadmap: Lean certificate for the J09 central window law
(register rows 10-11: VERIFIED 27/27 + 21/21, Lean status "open (M01)"). New file
fable_independent_2026/lean_2026/LR1_j09_window_law.lean (append-only repo; no
overwrites): W(q) = (1+q/3)/(1/2+q/4); theorems denom_pos, W_le_two, W_ge_four_thirds,
W_strict_antitone (0 <= a <= b -> W b <= W a, cross-difference = (b-a)/12 by ring).
Compile via lake env lean (toolchain v4.34.0-rc2). Exit 0 ONLY on: compile rc 0, zero
sorry, zero errors, #print axioms subseteq {propext, Classical.choice, Quot.sound}
for every theorem, and the python numeric witness (q in {0,3,10}: 2, 1.5556, 1.4444,
all inside [4/3,2], strictly decreasing) passes. Scope note (I-series precedent):
Lean certifies the ALGEBRA; the J09 MC verification (27/27) remains the empirical leg.
Kill: any compile error/sorry/axiom excess -> honest exit 1, fix-forward next tick.
