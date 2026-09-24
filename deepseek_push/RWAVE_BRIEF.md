# R-WAVE BRIEF — conductor-run successor wave to the landed Q-wave (commit 00298f7f6)

2026-09-24, same tick. 0 python3 lanes running (< 6); OPEN doors exist. delegate_task is not in
this session's toolchain (QWAVE_BRIEF precedent: conductor-run lanes). Three lanes spawned on
OPEN doors only (no KILLED door rehashed; no ai_slop/autoresearch_v3 collision; Q-prefix files
read-only). Kills PRE-REGISTERED here, before any run. House rules 1-10 apply. R-prefix files only.

## R01 — ladder extension: E[int r^8 ds] exact? (doors: M05 "E[int r^6] uncertified -> NOW CERTIFIED by Q01; next rung open"; M-roads Lean roadmap)
Context: Q01/P01 closed m in {1,2,4,6} exactly (3/4, 5/12, 1/4, 149/700; Q01_r6_core.lean exit 0
zero-sorry). The pipeline: g_m = t-antiderivative of (R^2+2Rmu*t+t^2)^(m/2) expanded; inner exact
t-integral [1-R,1+R] with weight (3/4)R((t^2+1-R^2)/t^2); artanh-part divisibility CHECKED not
assumed; P~_m even polynomial core; I_m = int_0^1 P~_m dR; Lean-certify the 1D core (FTC engine,
Q01_r6_core.lean idiom, MAXDEG grown to the actual degree).
Kill conditions (pre-registered):
- K1: exact-rational claim ONLY if route-1 (2D mpmath 40-dps quadrature of the original 2D
  integral) and route-2 (int_0^1 P~_8 dR in mpmath) agree to < 1e-10 absolute AND the value is
  rational with denominator <= 1e4. Otherwise: record the numeric value + best convergent,
  status NON-CLOSED, honest FAIL recorded, no forcing.
- K2: Lean exit 0, zero sorry, axioms subset {propext, Classical.choice, Quot.sound}; compile
  failure = FAIL verbatim (Q01 run-1 is the fix-forward precedent, not a tuning license).
- K3: scope 1D only (never claim 2D certification).
Deliverables: deepseek_push/R01_r8_moment.py/.out/.json; fable_independent_2026/lean_2026/R01_r8_core.lean(+.out).

## R02 — geometry-free floor sharpening beyond linear (door: Q03 "f(1)/central_floor = 0.3305; larger geometry-free floor = open")
Context: Q03 landed c*R floor, c* = 0.06844371, valid on all 6 landed clouds, binding at
volume_q10 (margin 0); power at R=1 = 33.05% of the central floor 0.2071. Registered criterion
(kept identical): floor valid on cloud i iff f(R_i) <= d_i + 3*se_i, se_i read from
Q03_results.json (se_i = margin_i/margin_in_se_i where positive; volume_q10 se from its stored
K12 re-derivation chain: se = (lo_rederived - d)/nse_rederived).
Method: (a) power-law family f_p(R) = c_p * R^p, c_p = min_i (d_i + 3 se_i)/R_i^p, scan
p in [0, 1.5] (grid 0.001); (b) report best (p, c_p), f_p(1), gain vs the linear 0.3305;
(c) ALSO the conservative no-SE variant c_p' = min_i d_i/R_i^p (validity f <= d exactly).
Kill conditions (pre-registered):
- K1: any claimed floor violating f(R_i) <= d_i + 3 se_i on ANY cloud = INVALID (kill fires).
- K2: gain claimed only if f(1)/0.20710678 exceeds the linear floor 0.33048 by >= 5% relative;
  otherwise verdict NO-MEANINGFUL-GAIN recorded honestly (curve-fitting that buys nothing is
  theatre — say so and bank the null).
- K3: all inputs runtime-read from Q03_results.json/K12_results.json (no retyped numbers).
Deliverables: deepseek_push/R02_floor_sharpen.py/.out/.json.

## R03 — CONSTANT-OFFSET robustness battery (door: Q02 verdict borderline at z=2.82 vs 3-SE rule)
Context: Q02 verdict CONSTANT-OFFSET rests on slope z = 2.82 < 3 — inside one SE of the kill
rule. Pre-registered perturbation battery decides whether the label is robust.
Method: rebuild the SPARC ring ensemble under the declared Q02 conventions (corpus v7; registered
check: N_rings = 3389, N_galaxies = 175, and per-bin N MUST equal Q02_results.json exactly, else
lane INVALID). Perturbations: (i) bin edges shifted -0.1 dex; (ii) +0.1 dex; (iii) bin width 0.4;
(iv) bin width 0.6; (v) deep-band-only refit over [-2.5, -1.0); (vi) galaxy-leave-one-out
jackknife SE on the Q02 binning. Slope z recomputed per perturbation (B=2000 galaxy-clustered
bootstrap, seeds 20260924+k; machinery speed-up via per-galaxy per-bin sufficient statistics,
registered check: main bin point estimates reproduce Q02_results.json EXACTLY and SEs within 5%).
Verdict rule (pre-registered): count perturbations with z >= 3 among (i)-(iv); if >= half ->
STRUCTURE-flag (upgrade recorded, slope values banked verbatim); else CONSTANT-OFFSET stands.
Battery result is recorded either way; no re-tuning to escape the borderline.
Deliverables: deepseek_push/R03_offset_robust.py/.out/.json.
