# V-WAVE BRIEF (conductor tick 2026-09-25, spawned from the landed U-wave)

Successor wave to U01/U02/U03. 3 conductor-run lanes (delegate_task absent from
this session's toolchain; Q/R/S/T/U precedent). Distinct OPEN doors only — no
KILLED door rehashed (register KILLED column consulted: two-moment closure 5sig,
J03, J04, NSE a0-loading, kurtosis-3 — none touched). No collision with
ai_slop/autoresearch_v3. Files claimed: V01_*, V02_*, V03_* in deepseek_push/,
plus fable_independent_2026/lean_2026/V01_chord_moment_2d.lean (+ its .out).
House rules 1-10 (LOOP_CONDUCTOR.md) bind: exit 0 only on real passes; honest
FAILs preserved verbatim; no lane commits; raw data never committed.

## V01 — 2D chord-moment 3/4: mathlib-gap route + Lean cert attempt
Door: M01's single CONJECTURED item — chordMomentVol = 3/4 (fable_independent_2026/
lean_2026/M01_alg_spine.lean, def chordMomentVol, 32 certified + 1 conjectured).
M01 ruled the natural proof needs a 2D change of variables (r,μ)↦(r√(1−μ²),rμ),
"not in mathlib". This lane claims that blocker is AVOIDABLE:
  (1) the μ-linear term rμ vanishes by oddness;
  (2) for fixed r, substitute v = rμ (a 1D interval-integral substitution,
      v ∈ [−r, r]): r²·∫₋₁¹ √(1−r²+r²μ²) dμ = r·∫₋ᵣ^r √(1−r²+v²) dv (r=0 both 0);
  (3) Fubini over the triangle T = {(r,v): 0 ≤ r ≤ 1, |v| ≤ r} flips the order;
  (4) the inner r-antiderivative of r√(1−r²+v²) is −(1/3)(1−r²+v²)^{3/2}
      (elementary, argument ≥ v² ≥ 0), so ∫_v^1 = (1−|v|³)/3 and
      I = ∫₋₁¹ (1−|v|³)/3 dv = 1/2; chordMomentVol = 3·½·I = 3/4.
  NO 2D substitution theorem needed anywhere — only 1D substitution + triangle
  Fubini + a cubic antiderivative.
- K1 (numeric machinery): direct 60-dps double quadrature of chordMomentVol vs the
  triangle-chain quadrature (steps 1-4) agree ≤ 1e-30 abs; MC 1e7 z ≤ 3 vs 0.75.
- K2 (Lean): cert = exit 0, zero sorry, axioms exactly {propext, Classical.choice,
  Quot.sound}. If the full assembly does not certify within this lane's budget,
  record INCOMPLETE honestly with the exact blocker — certified partial pieces
  (oddness reduction, per-r substitution identity, antiderivative lemma) may be
  banked individually and labeled partial. No fabricated certificate.
- K3: the claimed result is the ROUTE + whatever certifies; no physics claim.

## V02 — geometry-free floor cloud extension (R02/T02 caveat zone R < 1.51)
Door: R02 registered that the constant floor c* = 0.28177 is checked only at the
6 landed K12 cloud R-values (hull covers [1.5133, 28.2393]; T02: R=1 OUTSIDE,
caveat stands for R < 1.51). No cloud below R = 1.5133 has ever been tested.
This lane BUILDS the missing clouds with the K12 engine convention:
  new clouds (J02.simulate / K12.simulate_shell, q = 0, n = 1e6, fresh seeds
  recorded in-file): central tau0 = 0.5, central tau0 = 0.7, volume tau0 = 0.5,
  volume tau0 = 0.7, shell r0 = 0.9 tau0 = 0.7 — chosen to span R ≈ 0.4-1.6
  (E[v²] = 2E[N] scales ~ tau0², so sub-thin tau0 lands BELOW 1.5133).
- K1 (machinery): seed-replication gate — rerunning K12's exact cloud
  (volume, tau0=1, q=0, seed 9000, n=1e6) reproduces K12's stored volume_q0
  E_D/E_v2 EXACTLY (same engine, same seed, deterministic); plus criterion
  consistency vs Q03's 6 stored clouds where names overlap.
- K2 (both-ways, pre-registered): on the EXTENDED 11-cloud set test
  (a) the landed constant floor c* = 0.28177 and (b) the landed linear floor
  c* = 0.06844371 (criterion f(R_i) ≤ E_D_i + 3·se_D_i, identical to Q03/R02):
  any violation → that floor is DOWNGRADED with its validity domain restated;
  then record the maximal power-law floor on the extended set (p scanned on a
  grid; c maximized given p), with its hull coverage interval. Either outcome a
  result; no re-tuning of landed constants to pass.
- K3: all landed inputs runtime-read (K12/Q03/R02 JSONs); new numbers from the
  runs recorded with seeds/n; no physics claim beyond the floor channel.

## V03 — O01 dwarf primary/deep-tail influence audit (T03 analog on G114)
Door: O01 verdict banked "deep tension NOT weakened, directionally REPRODUCED"
(primary LT-deep a0_eff/a0 = 0.64 ± 0.16, N=16) with the registered caveat that
the offset is driven by IC 1613 / DDO 50 / NGC 1569 (post-hoc-labeled min3
subset = 0.97 ± 0.15, N=13). T03 quantified exactly this concentration question
for the MIGHTEE channel (50%-of-gap rule → DIFFUSE). Never run on the dwarf
sample. This lane quantifies per-galaxy influence from O01's stored per-galaxy
values (runtime-read O01_results.json; recompute gate against stored means).
- K1 (machinery): per-sample mean of stored per-galaxy log10_a0eff_a0 reproduces
  O01's stored log10_a0eff_over_a0 to 1e-9 (primary N=16, deep tail N=7).
- K2 (both-ways, pre-registered): leave-one-out jackknife over the 16 primaries
  and over the 7 deep-tail galaxies; for each sample report the largest
  single-galaxy drop of a0_eff/a0 as a fraction of the gap to 1.0 (and to the
  SPARC-deep anchor 0.73):
  largest drop > 50% of the gap-to-1.0 → CONCENTRATED flag (driver-driven, the
  O01 caveat is quantified and the population claim narrows); ≤ 50% → DIFFUSE
  (population property). Either outcome a result; no re-tuning.
- K3 (power, no new law): state, from stored SEs, whether the N=13 remainder and
  the N=7 deep tail resolve 0.73-vs-1.0 at 3σ (they are expected NOT to on the
  remainder — recorded as an honest power statement, consistent with O01's MC-B;
  no kill attached).
