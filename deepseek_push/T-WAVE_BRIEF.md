# T-WAVE BRIEF — conductor-run successor wave to the S-wave (spawned at the 2026-09-24 tick)

2026-09-24, conductor tick. 0 python3 lanes running (< 6); OPEN doors exist. delegate_task is not in
this session's toolchain (QWAVE/RWAVE/SWAVE precedent: conductor-run lanes). Three lanes spawned on
OPEN doors only (no KILLED door rehashed; no ai_slop/autoresearch_v3 collision; S/J/K/Q/R-prefix files
read-only except S01_r10_moment.py's own conductor fix-forward, recorded in-script). Kills
PRE-REGISTERED here, before any run. House rules 1-10 apply. T-prefix outputs only
(T01 reuses the S01 lane's script verbatim apart from the recorded output-reroute fix-forward).

## T01 — r^10 rung completion (S01 rerun, fix-forward) (door: S01 died mid-run; M05/R01 ladder)
Context: SWAVE_BRIEF S01 registered the m=10 rung of the exact ladder E[int r^(2m) ds] (landed:
3/4, 5/12, 1/4, 149/700, 1069/6300 at m=1,2,3? [m=2,4,6,8]); S01_r10_moment.py died after printing
only the sympy candidate I_10 = 13649/97020. Pipeline (derive(), 40-dps route-1, mu->t weight,
V/(1-R^2) divisibility check) already replicated from R01 verbatim.
K0 (registered): pipeline must reproduce 5/12, 149/700, 1069/6300 exactly, else lane INVALID.
K1: exact-rational claim ONLY if route-1 agrees < 1e-10 abs AND denominator <= 1e4; otherwise
NON-CLOSED recorded with the exact value + best convergent, honest FAIL, no forcing. (The candidate
q = 97020 > 1e4: NON-CLOSED is the expected registered outcome; the route agreement + Lean identity
cert are still deliverables — an exact identity can be Lean-certified WITHOUT the "closed-form
ladder member" claim.)
K2: Lean exit 0, zero sorry, axioms {propext, Classical.choice, Quot.sound}; compile failure = FAIL
verbatim.
K3: scope 1D only.
Deliverables: S01_r10_moment.py rerun -> S01_r10_moment_results.json / S01.out / S01_r10_core.lean(+.out).

## T02 — constant-floor hull check: is c* = 0.28177 valid BETWEEN the cloud points? (door: R02
registered caveat "validity CHECKED only at the 6 landed cloud R values"; the SWAVE_BRIEF S03 door
was NOT executed — S03 ran a different lane (q-anchored family, registered above); this lane executes
the original brief.)
Inputs (all runtime-read, no retyped numbers): Q03_results.json floor_check (6 clouds: R_i, d_i,
margin, margin_in_se -> se_i = margin/margin_in_se, b_i = d_i + 3*se_i); R02_results.json best
(c_registered = 0.2817733312220705, c_conservative = 0.2799667038685411).
Method (registered assumption, recorded as an assumption not a theorem): sort the 6 (R_i, b_i) points
by R; B(R) = piecewise-LINEAR interpolation of the b_i on [R_min, R_max]; test f(R) = c* <= B(R) on a
dense 2000-pt grid over the hull; also test the conservative c_conservative (informational).
K1: ANY interior violation (c* > B(R)) -> DOWNGRADE: constant floor valid pointwise-only, R02 caveat
stands unresolved (honest banked FAIL, no rescue fit).
K2: report the hull's R-coverage of [0,1] explicitly; R = 1 certified only if inside [R_min, R_max]
(no extrapolation claim); no new claim without K1+K2 clean.
K3: inputs runtime-read (Q03 + R02), cloud count must be 6, else lane INVALID.
Deliverables: deepseek_push/T02_floor_hull.py/.out/.json.

## T03 — MIGHTEE deep-subpopulation attribution (door: S02's CHANNEL-DEPENDENT z = +6.99 — is the
offset a population property or carried by a few colour groups?)
Context: S02 measured MIGHTEE deep a0_eff/a0 = 2.1638 +/- 0.1860 (18 deep colour groups, N_deep = 72)
vs Q02 SPARC-deep anchor 0.8314 +/- 0.0422. Parse the digitized table exactly as S02 (log10 columns,
colour id = r|g|b string, deep = X < 0.2*A0), same ratio_stat.
K1 (machinery): whole-deep ratio must equal N05 mightee_deep a0eff_a0 within 1e-9, else lane INVALID.
K2 (pre-registered both-ways rule): leave-one-colour-group-out jackknife over the deep groups; if
excluding the single largest-drop group moves a0_eff/a0 DOWN by more than 50% of the gap
(r_full - 0.8314) -> CONCENTRATION-DRIVEN (selection-artifact flag attached to the S02 verdict);
else DIFFUSE (channel-dependent stands as a population property). Either outcome is a result;
no re-tuning, no budget widening.
K3: per-group table (n >= 5 groups: group ratio + n) reported informational; no group-level law
claimed (n too small).
Deliverables: deepseek_push/T03_mightee_subpop.py/.out/.json.
