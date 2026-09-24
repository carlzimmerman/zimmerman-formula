# S-WAVE BRIEF — conductor-run successor wave to the landed R-wave (commit 5e5581a41)

2026-09-24, conductor tick. 0 python3 lanes running (< 6); OPEN doors exist. delegate_task is not
in this session's toolchain (QWAVE/RWAVE precedent: conductor-run lanes). Three lanes spawned on
OPEN doors only (no KILLED door rehashed; no ai_slop/autoresearch_v3 collision; R/Q/P-prefix files
read-only). Kills PRE-REGISTERED here, before any run. House rules 1-10 apply. S-prefix files only.

## S01 — ladder extension: E[int r^10 ds] exact? (doors: M05/R01 "next rung open"; M-roads Lean roadmap)
Context: P01/Q01/R01 closed m in {1,2,4,6,8} exactly (3/4, 5/12, 1/4, 149/700, 1069/6300; R01_r8_core.lean
exit 0 zero-sorry). Pipeline replicated from R01_r8_moment.py verbatim (same derive(), same route-1
40-dps original-variable quadrature, same mu->t weight (3R/4)(t^2+1-R^2)/t^2, h-substitution,
V/(1-R^2) divisibility CHECKED not assumed), m=10 (k=5).
K0 (registered): pipeline must reproduce 5/12 (m=2), 149/700 (m=6), 1069/6300 (m=8) exactly, else lane INVALID.
K1: exact-rational claim ONLY if route-1 and route-2 agree < 1e-10 abs AND denominator <= 1e4;
otherwise NON-CLOSED, best convergent recorded, honest FAIL, no forcing.
K2: Lean exit 0, zero sorry, axioms {propext, Classical.choice, Quot.sound}; compile failure = FAIL
verbatim (fix-forward precedent, not a tuning license).
K3: scope 1D only (never claim 2D certification).
Deliverables: deepseek_push/S01_r10_moment.py/.out/.json; fable_independent_2026/lean_2026/S01_r10_core.lean(+.out).

## S02 — MIGHTEE mirror: does the CONSTANT-OFFSET law hold off-SPARC? (doors: N05 arbitration card "MIGHTEE is the SIGN-MIRROR"; Q02/R03 constant-offset banked on SPARC only)
Context: Q02/R03 banked a0_eff/a0 = 0.8314 +/- 0.0422 (SPARC deep band) / O04b joint 0.7172 +/- 0.0593,
but N05 measured MIGHTEE deep a0_eff/a0 = 2.164 (z=+6.58, opposite sign). The constant-offset law is
so far a ONE-SAMPLE law. Test it on the independent MIGHTEE-HI 80-ring digitized sample
(data2/mightee2025_rar_digitized_points.csv, runtime-read) with the SAME deep convention
(g_bar < 0.2 a0) and the SAME M1 channel: a0_eff/a0 = 1 + Delta/(a0*E[g_bar]) with Delta =
E[Y^2]-E[X^2]-a0*E[X]... expressed as (E[Y^2]-E[X^2])/E[X] / a0 - 1 per the estimator algebra; ring-level
bootstrap (no galaxy ids in the digitized table; recorded as a limitation, B=2000, seed 20260924).
K1 (power): if N_deep(MIGHTEE) < 20 rings -> UNDECIDABLE recorded honestly, no verdict forced.
K2 (pre-registered both-ways rule): |z_MIGdeep - 0.8314| < 3 SE (SE = max(ring-boot, Q02 SE in quadrature? NO -- quadrature of MIGHTEE SE alone with the SPARC SE) -> CONSISTENT-UNIVERSAL (constant-offset crosses channels, B-class banked); |z| >= 3 -> CHANNEL-DEPENDENT recorded, the two-sided >4sigma contradiction stands and sharpens (registered either way; no re-tuning, no budget widening).
K3: full-range MIGHTEE Delta re-fit must reproduce L06's stored Delta within 5% (machinery check), else lane INVALID.
Deliverables: deepseek_push/S02_mightee_mirror.py/.out/.json.

## S03 — constant-floor hull check: is c*=0.28177 valid BETWEEN the cloud points? (door: R02 registered caveat "validity CHECKED only at the 6 landed cloud R values; R=1 extrapolation is a family choice")
Context: R02's constant floor c* = 0.28177 was verified only at the discrete cloud R values. This lane
quantifies the caveat and, where possible, closes it: per cloud, sort (R_i, b_i = d_i + 3*se_i);
build the piecewise-LINEAR upper-bound curve B_i(R) inside each cloud's own R-range (registered
assumption: linear interpolation of the bound, recorded as an assumption not a theorem); test
f(R) = c* <= B_i(R) on a dense grid (2000 pts) over each cloud range, and over the union hull.
K1: ANY interior violation (c* > B_i(R) on the interpolated curve) -> DOWNGRADE: constant floor valid
pointwise-only, R02 caveat stands unresolved (honest FAIL banked, no rescue fit).
K2: if no violation, report the hull's R-coverage of [0,1] explicitly; R=1 certified only if inside a
cloud range (no extrapolation claim). p=0 vs best power-law re-scan on the hull grid reported as
informational (no new claim without K1+K2 clean).
K3: all inputs runtime-read from Q03_results.json (+ K12_results.json for the volume_q10 se chain), no retyped numbers.
Deliverables: deepseek_push/S03_floor_hull.py/.out/.json.
