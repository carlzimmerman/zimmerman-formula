# Q-WAVE BRIEF — conductor-run (no delegate_task in this session's toolchain; O04b precedent "O-lane (conductor-run)")

2026-09-24, tick after 0e9c7466e. 0 lanes were running (< 6); three lanes spawned on
OPEN doors only. Kills PRE-REGISTERED here, before any run. House rules 1-10 apply
(append-only, no fabrication, honest FAILs, exit 0 only on real passes, raw data
untracked, no lane collisions: Q-prefix files only, Lean artifact Q01_r6_core.lean
in fable_independent_2026/lean_2026/).

## Q01 — Lean certification of the first-flight ladder via the exact R-core (door: P01 "PENDING (candidate for the M01/N03 spine)")
Context: P01 landed E[int r^6 ds] = 149/700 exactly (two independent 40-digit routes,
2.87e-42 agreement; MC z=0.30). M05's 3/4, 5/12, 1/4 already numerically anchored;
N03 certified only the reduced w-cores (the 2D change of variables is not in mathlib).
Goal: derive, symbolically (sympy, exact rationals), for each moment m in
{chord=3/4, r2=5/12, r4=1/4, r6=149/700} an explicit POLYNOMIAL P_m(R) on [0,1] with
I_m = int_0^1 P_m(R) dR, then Lean-certify all four as exact 1D polynomial integrals
(FTC engine idiom of N03_small_spine.lean, toolchain v4.34.0-rc2).
Kill conditions (pre-registered):
- K1: P_m must integrate to its target EXACTLY in sympy rational arithmetic AND the
  symbolic F_m(R) = P_m(R) + Q_m(R)·artanh(R) reduction must be verified against
  mpmath 40-dps route-2 values at >= 5 sample R per moment (agreement < 1e-30).
  If artanh divisibility V_m/(1-R^2) fails for any moment: that moment is NOT
  certified (honest FAIL recorded); no polynomial is forced through.
- K2: Lean exit 0, zero sorry, axioms subset {propext, Classical.choice, Quot.sound}.
  Compile failure = FAIL recorded verbatim, no workaround tuning.
- K3: Lean status stays "1D core certified; 2D->1D reduction analytic (sympy exact) +
  numerically cross-checked (P01 routes)" — never upgraded to "2D certified".
Deliverables: deepseek_push/Q01_r6_lean.py/.out/.json; fable_independent_2026/lean_2026/Q01_r6_core.lean(+.out).

## Q02 — Deep-regime ONSET test: is the 4.2sigma deep tension a constant offset or structure? (doors: L06 4.2sigma deep tension = OPEN; N05 two-sided mirror)
Context: L06 deep-SPARC a0_eff = 6.78e-11 = 0.73 a0 (z=-4.17); O04b joint (SPARC-deep +
G114 dwarfs + MW) = 0.7172 +/- 0.0593; G208 staircase register 0.692 a0 = 6.478e-11.
OPEN question: within SPARC, does a0_eff/g_bar-bin stay flat across the deep band
(constant-offset sub-a0 law) or turn on/off (onset/gradient)? N01's density-locality
door is KILLED — this lane tests RADIAL/REGIME STRUCTURE of the deficit, not a
rho -> a0 law; no rehash.
Method: SPARC ring ensemble rebuilt under the L06/G071 declared conventions
(corpus v7, v_b^2 = sign(Vgas)*Vgas^2 + m2l*(Vdisk^2+Vbul^2), m2l_disk or 0.5);
bins in log10(g_bar/a0) over [-2.5, 0.5] (width 0.5); per-bin a0_eff =
(E[g_obs^2] - E[g_bar^2]) / E[g_bar]; SE = galaxy-clustered bootstrap, B=2000,
seed 20260924. Weighted linear slope of a0_eff/a0 vs log10(g_bar/a0) across
resolved bins (N >= 100), slope SE from the same bootstrap.
Kill conditions (pre-registered):
- K1 (machinery): synthetic line control (N=8000, log10 X ~ U(-12.4,-9.3), 4% scatter)
  must return a0_eff/a0 = 1 within 3 SE in EVERY resolved bin; else lane INVALID.
- K2: if |slope| < 3 SE -> verdict CONSTANT-OFFSET (banks "the deep deficit is
  uniform across the deep band, a0_eff/a0 = joint value within SE"); if >= 3 SE ->
  verdict STRUCTURE with the slope + SE banked verbatim (both outcomes are results;
  no tuning). Bins with N < 100: NOT-RESOLVED, recorded, never forced.
- K3: weighted a0_eff must agree with O04b 0.7172 +/- 0.0593 (z < 3) or the
  discrepancy is recorded as a finding, not smoothed away.
Deliverables: deepseek_push/Q02_deep_onset.py/.out/.json.

## Q03 — Geometry-marginalized width floor: quantifying the K12 withdrawal (door: K12 "Thm-2 lower endpoint withdrawn under unknown geometry")
Context: K12 landed: frozen Thm-2 lower endpoint (sqrt(1+R)-1)/2 fails under volume
at 14.9/39.3/111.1 SE (q=0/3/10) and shell r0=0.9 (+21.1 SE); upper endpoint
survives; audit line: lower holds iff E[Q] <= d + 2d^2 (uniform-kappa, q=0 only).
Goal: (a) re-derive every stored band violation from raw fields (d, R, se_D) —
must match stored SEs within 1%; (b) verify the uniform-kappa identity
E[Q] = (R - 2d)/2 and the criterion equivalence on volume_q0; (c) tabulate the
q>0 kappa compensator (E[N] vs E[tau], E_N_vs_En_time_ratio) as the registered
reason the identity is q=0-only; (d) hunt the largest geometry-free lower floor
f(R) valid on ALL landed geometry clouds: candidate f(R) = c*·R with
c* = min over clouds of (d/R); check d >= f(R) - 3 se_D on every cloud, and
quantify the discrimination-power loss vs the central floor at R=1.
Kill conditions (pre-registered):
- K1: any re-derived SE off by > 1% vs stored => engine fault, lane FAILs.
- K2: identity/criterion must hold on volume_q0 within 5 combined SE; failure =
  honest FAIL (the analytic claim is wrong, recorded as such).
- K3: if c* fails the d >= f - 3se check on ANY cloud, verdict = NO geometry-free
  floor at all on the landed set (recorded, not replaced by a tuned floor).
Deliverables: deepseek_push/Q03_band_floor.py/.out/.json.
