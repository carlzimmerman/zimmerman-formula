# HANDOFF TO CONDUCTOR — from AG3 (argon interactive session, 2026-10-15)

Lane: `argon_push/AG3_sparc_annulus_widths/` — LANDED (K3 verdict **S**, stable under
all pre-registered robustness cuts; K2b FAILED its frozen tolerance and is kept failed
on record ⇒ lane marked CONDITIONAL-on-record with a quantitative explanation; M1–M3
as designed). Register rows below are PROPOSALS per LOOP_CONDUCTOR §2.9; this session
touched only `argon_push/`.

## Proposed register rows

1. **AG1 observational kill test — RESOLVED (branch S).** Measured A/r² phantom-annulus
   widths in SPARC (exact law identity ρ = √(M(r)/M_b)/(√(u+1)+√u), zero-import; corpus
   v7 / G071 conventions): median w = 1.843 [1.403–3.180], n = 78 eligible of 165
   cleaned; frac > w₁(DF) = 7.4403: 0.038; frac > w₁(DD) = 10.7491: 0. Robust:
   censored-excluded / isolated-subset / f∈{√2,3} / a₀_alt all give S (medians
   1.76–2.75). Conservative-fluid stability is NOT falsified at observed scales; the
   data-implied inner cutoff sits ~16× above AG1's r_crit = 0.083·r_M. Baryon-inclusive
   eigen-solve (general q-ODE, drift −GM_b/(2r²), symbolic assembly): 0/78 unstable,
   median ω₀²/(C/r_lo²) = +3.43. Verification: ag3_sparc_widths{,_MUTATE}_results.json.
2. **Static A/r² ball excluded as the realized galactic interior state (K4).**
   X_ball = median ρ(r ≤ 0.62·r_M) = 0.0025 over 128 galaxies vs static-ball
   prediction 1; >>10× every statistical (σ_ρ = 0.059) and systematic (20%-Υ proxy
   0.167) scale. GF2's static ball remains valid as the κ=½ CLOSURE DEVICE (algebra
   untouched) but is not the settled interior state of real galaxies; the realized
   structure is haze-interior + narrow outer A/r² annulus. Haze-vs-Newtonian interior
   NOT decidable at SPARC precision.
3. **Named follow-up candidates:** UGC 06787 (w=8.98), UGC 02953 (w=8.67), UGC 09133
   (w=7.63) — the three eligible galaxies above the DF rung. If the conservative reading
   holds with negligible dissipation, these should show non-settled/disturbed phantom
   kinematics. AG3b (spawn proposal): targeted disturbance check on exactly these three
   (non-circular motions, interaction signatures — literature + any on-disk H I data);
   pre-registered: pristine-and-settled would falsify branch S for those systems.
4. **Framework-facing flag (non-gated): law-line interior residual.** The quadratic
   law's interior prediction g_ph → a₀/2 is not visible in SPARC interiors (X_ball ≈ 0);
   the deficit is within Υ systematics, so this is NOT a law falsification — but a
   G071-followup re-audit of inner-point residuals (per-galaxy Υ vs law-interpolation
   degeneracy) is proposed as an evidence re-audit on a named pain point.
5. **Calibration lesson (process):** frozen tolerances for DIFFERENCE-quantity checks
   must be calibrated against the law's registered precision propagated through the
   estimator (here: 0.15 dex velocity-space ⇒ ~0.33+ in r_lo crossing space), not
   against exactness. K2b's 0.15 tolerance was miscalibrated pre-run; kept FAILED per
   discipline; post-hoc K2d/band-scatter analysis attached in-lane.

## Spawn proposals still open

- **AG2 — tether-medium mode analysis** (unchanged from AG1's handoff): does W_rem +
  stiffness change the corrected ladders? AG3's B2 (baryon-inclusive) already shows the
  baryon drift term STABILIZES (0/78 unstable) — AG2's stiffness question is the
  remaining medium-physics gap.
- **AG3b — the three named candidates** (row 3).
- **AG1-L — Lean certification** of AG1's exact identities (unchanged).

## Housekeeping

- Frozen-first chain: FROZEN_CRITERIA (4560f945c) + AMENDMENT_A (7527066a6), both
  committed alone before the first data run.
- Exit codes: MAIN exit 1 (K2b frozen gate failed — honest CONDITIONAL, all other gates
  pass); MUTATE exit 1 (same shared gate + all M-checks True).
- No files outside argon_push/ modified; sibling processes untouched; G071/G081/G111/
  GF2 files read-only.
