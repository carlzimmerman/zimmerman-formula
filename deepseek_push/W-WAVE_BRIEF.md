# W-WAVE BRIEF (conductor tick 2026-09-25, spawned from the landed V-wave)

Successor wave to V01/V02/V03. 3 conductor-run lanes (delegate_task absent from
this session's toolchain; Q/R/S/T/U/V precedent). Distinct OPEN doors only — no
KILLED door rehashed (register KILLED column consulted: two-moment closure 5sig,
J03, J04, NSE a0-loading, kurtosis-3, N01, landed-constant-floor-on-extended —
none touched). No collision with ai_slop/autoresearch_v3. Files claimed:
W01_* / W02_* / W03_* in deepseek_push/, plus an APPEND to
fable_independent_2026/lean_2026/V01_chord_moment_2d.lean (same lane's file,
append-only; certified Stage A/B text untouched). House rules 1-10
(LOOP_CONDUCTOR.md) bind: exit 0 only on real passes; honest FAILs preserved
verbatim; no lane commits; raw data never committed.

## W01 — chordMomentVol = 3/4: complete the V01 INCOMPLETE Fubini-flip assembly
Door: V01 banked 6 sorry-free Lean theorems (inner_eq, step2, peel_r, peel_v,
step4, final_half) but the Fubini-flip assembly (J_value) + main
(chordMomentVol = 3/4) was recorded INCOMPLETE — this is M01's single
CONJECTURED item (chordMomentConjecture). This lane completes the assembly by
APPEND (Stage C) to V01_chord_moment_2d.lean:
  J := ∫_{r=0}^{1} ∫_{v=-r}^{r} r·√(1−r²+v²) dv dr  (so chordMomentVol = 3/2·J)
  flip: J = ∫_{v=-1}^{1} ∫_{r=|v|}^{1} r·√(1−r²+v²) dr dv = ∫ (1−|v|³)/3 = 1/2,
  hence chordMomentVol = 3·(1/2)·(1/2) = 3/4.
- K1 (numeric machinery — BUDGET CHANGE RECORDED OPENLY per house rule 3): the
  V-wave K1 gate (60-dps direct quadrature ≤ 1e-30) is UNREACHABLE — mpmath's
  nested-quadrature maxdegree floor measured at 7e-19 (V01 lane, exit 1 kept).
  W01 re-registered gate: sympy exact antiderivative residual = 0 AND final
  v-integral = 1/2 exact AND step-2 identity exact at 40 dps on the r-grid AND
  MC 1e7 z ≤ 3 vs 0.75 AND direct-vs-triangle-chain agreement ≤ 1e-15 abs at
  50 dps (measured achievable: 7e-19). This is a budget re-registration with
  the measured reason on record — NOT a pass-by-tuning.
- K2 (Lean): Stage C appends compile exit 0, zero sorry, axioms exactly
  {propext, Classical.choice, Quot.sound} on EVERY new theorem including main:
  chordMomentVol = 3/4. M01_alg_spine.lean is NOT touched (lane collision rule);
  the register row records that M01's conjecture is now certified in the V01
  file. If the assembly does not certify: record INCOMPLETE with the exact
  blocker, bank only what compiles, exit non-zero honestly.
- K3: math-only claim (route + cert); no physics.

## W02 — floor-family caveat quantification (R02/V02 "family-bound caveat")
Door: V02 banked the new maximal POWER-LAW floor p=0.6719, c=0.205581
(retention 0.993 at R=1, hull [0.8407, 28.2393]) with the registered caveat
that the floor is family-bound. This lane quantifies the caveat: scan the
pre-registered family set {power-law c·R^p (landed), hinge max(c0, c1·R),
affine c0 + c1·R (landed Q03), power-law with free floor c0 + c·R^p} on the
EXTENDED 11-cloud set and record each family's maximal valid floor (criterion
f(R_i) ≤ b_i = E_D_i + 3·se_D_i, identical to Q03/R02/V02), its retention
f(1)/central_floor, and binding cloud.
- K1 (machinery): recompute V02's stored extended-floor p/c to 1e-9 with the
  SAME scan grid as V02 (p ∈ linspace(-3,3,1201) + refine ±0.0025/501; recorded
  in-script); all inputs runtime-read from V02_floor_extension_results.json +
  K12_results.json + Q03_results.json. No new MC runs (reanalysis only).
- K2 (both-ways, pre-registered): family-choice sensitivity of the R=1
  retention — spread = max over families of f(1)/central_floor minus V02's
  power-law 0.993, reported per family; if ANY pre-registered family achieves
  retention > 0.993 + 0.05 → FAMILY-FRAGILE flag (the V02 R=1-inside-hull
  resolution carries an explicit family caveat with the dominating family and
  its numbers); else FAMILY-STABLE. Either outcome banked; no re-tuning.
- K3: floor-channel claim only; families pre-registered BEFORE scanning.

## W03 — WALLABY DR2 arbitration-card feasibility audit (N05/U02 open door)
Door: U02's refreshed card: SPARC-deficit 5σ attribution needs 1656 deep rings
(≈ 59 galaxies); MIGHTEE-excess already fired at N=72; cross-channel 5σ
difference needs n = 232 NEW deep rings per channel. Open question: does
WALLABY DR2 (data2/wallaby_dr2_kinematic_catalogue.tsv, on disk, untracked)
supply the deep-band rings? This lane is a FEASIBILITY AUDIT (card arithmetic +
data census), no physics claim, no new a0_eff measurement.
- Definitions fixed BEFORE counting: deep band = log10(g_bar/a0) < −0.7 (the
  S02/U01 deep cut, a0 = 9.3619e-11); z = 1420.405752 MHz/freq − 1 per galaxy;
  Hubble-flow distance D = (c/H0)·z with H0 = 70 km/s/Mpc (recorded
  assumption); g_bar = Vrot_model²/(R_phys) with R_phys = Rad·(π/180/3600)·D
  (Rad in arcsec), Vrot and Inc from the catalogue row; a ring counts if its
  log10(g_bar/a0) < −0.7 AND Vrot_model > 3·e_Vrot_model AND Inc ≥ 30 deg.
- K1 (machinery): recompute U02's F2 SPARC N = 1656 (1e-9) and F3 n = 232
  (1e-9) from the stored JSONs (runtime-read).
- K2 (both-ways, pre-registered): deep-band ring count N_res(WALLABY) from the
  census above: ≥ 232 → CROSS-CHANNEL-FEASIBLE (recipe recorded); ≥ 1656 →
  also SPARC-SIDE-FEASIBLE; else INFEASIBLE with the exact shortfall and the
  named blocker (recorded either way; no re-tuning of definitions).
- K3: feasibility card only; NO a0_eff measured from WALLABY here (engine
  calibration out of scope, stated explicitly).
