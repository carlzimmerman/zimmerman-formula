# CFG498 FROZEN CRITERIA: the clock taper with a capped, mass-conserving draw (reconciling growth and KiDS)

Written 2026-10-08 and committed alone, before any CFG498 script exists and before any CFG498 number is computed.
Nothing below may change after a result is seen; any later departure goes in the README as a disclosed deviation.

**Standing.** κ = ½ is FITTED (the only declared constant; it enters through a0). Kernel ν_mono. Both footings,
a0 = 9.3603e-11 and 1.1312e-10 m/s², scored separately and never pooled. a0 flat in z. "Cold energy" = the cold
clumping component (the cosmic amount; its MASS is still required; no particle species). Never "theory closed"; never
"the data favour the framework".

**The clash being tested.** Growth needs the law confined (CFG424-CFG460: edge 5.850 r_M + per-catchment mass
conservation). KiDS rejects the 5.850 r_M edge on real galaxies (CFG485 caveat 2; CFG487 +60.5 / +70.6). CFG487 found that
V1's settling clock alone (λ = 1, no edge) passes KiDS (+2.05 / +0.71 vs CFG413 best) and SPARC, but in the PM without
the edge the draw overdraws catchments (POST-HOC V1-CATCH: overdraw 26% / 52%, q_max 2.0 / 2.3, P(k = 1) 0.826 / 0.798,
TENSION).

**Not blind (disclosed).** I have read CFG487's README, criteria, engine, data script and outputs (including its
POST-HOC CATCH rows above), CFG424's README/results, CFG485's README and script, and CFG495's criteria. A mental estimate
(no script): on the analytic lens and SPARC models the cap cannot bind by more than ~19% even with m = 1
(D ≤ M_ta − M_b against (1 − f_b) M_ta), and the taper reduces D further, so the cap is probably INERT there and (b), (c)
probably reproduce CFG487's "V1 switch only" rows. The open question is the PM. Also noted: CFG487's V1-SA had P(k = 1)
0.827 with only 0.1% overdraw, so the small-scale deficit may NOT be caused by overdraw; if so the cap will not cure it.

## 1. The object (one object, two clock versions)

- **Settled fraction m** exactly as CFG487 §1: Dm/Dt = Γ L (1 − m), Γ = √(4πG ρ_X) (λ = 1), latch L at θ ≤ 0, never
  resets; m' = 1 − (1 − m) exp(−Γ Δt L).
  - **V1** (cold-energy clock; reads the cold energy's state = **MS1 EXCEPTION**, NOT ADMISSIBLE under original MS1;
    owner: "test both"): CFG487's V1 latch and rate.
  - **V2** (baryon clock, strict MS1): CFG487's V2 latch and rate.
- **Support:** the phantom density is multiplied by m (the clock taper). **No edge.** The support ends at the
  catchment: the turnaround sphere (analytic: r_ta = cfg100's r_ta_law; PM: the engine's in_cover(x = 1) components,
  CFG424's catchment).
- **Mass conservation (CFG424, unchanged):** the excess e = m · max(s_ph − s_c, 0) inside a catchment is drawn from the
  cold energy of the same catchment in proportion to its local cold density: comp = q · s_c, q = Σe / Σs_c.
- **The cap (the only new statement; it is the mass-conservation statement, not a constant):** the draw cannot exceed
  the catchment's available cold energy. Per catchment, with q_raw = Σe / Σs_c:
  - e → e / max(1, q_raw) (the phantom is supply-limited, uniformly within the catchment), comp = min(1, q_raw) · s_c.
  - So comp ≤ s_c everywhere (no negative cold energy) and the added source still sums to zero on every catchment.
  - When q_raw ≤ 1 the object is identical to CFG487's CATCH mode.
- **Inputs:** κ (via a0) and f_b = 0.02237/0.14237. Nothing else is added. Inherited and disclosed (not tuned): the
  ΛCDM spherical-collapse Δ_ta(z); MIX-A; the in_cover peak finder (its threshold still contains T1's ε = 0.077, as in
  CFG424/CFG487).

### Analytic implementation (KiDS, SPARC, early types)
- Per lens / galaxy: phantom ΔM_ph(r) = ∫_0^r m(r') dM_ph,law(r') out to r_ta, mass frozen beyond (CFG487's
  "switch only" construction, m from cfg487_lib.ShellClock, V1: ρ_X = law mass, V2: ρ_X = M_b(<r)/f_b).
- Available cold energy C = (1 − f_b) M_ta, M_ta = (4π/3) r_ta³ (1 + δ_ta(z)) ρ̄_m(z) (CFG487's E2 M_ta).
- D = ΔM_ph(r_ta); q_raw = D / C.
- **PRIMARY cap (scored):** if q_raw > 1 the whole tapered phantom is multiplied by 1/q_raw (the PM engine's rule).
- **REPORTED cap (no verdict weight):** outer-first: the tapered phantom is truncated at the radius where ΔM_ph = C.
- Reported: the q_raw distribution, the fraction of lenses / galaxies where the cap binds, and the consistency
  M_b + M_ph,law(<r_ta) vs M_ta.

## 2. Tests

**(a) Growth**, 256³, seed 359, CFG487 engine copy (`cfg498_pm.py`; FB, MIX-A, ICs, steps, k_J unchanged), new
confinement mode CAP (CATCH + the cap), both footings, against CFG359's S0 with CFG361's cuts: GROWTH OK iff
|σ8 ratio − 1| ≤ 0.05 AND max_{k ≤ 1 h/Mpc} |P ratio − 1| ≤ 0.10; TENSION if the σ8 shift is in (5%, 20%] or P > 10% with
σ8 within 20%; FAIL if the σ8 shift > 20%.
- Runs: V1-CAP canonical, V1-CAP alt, V2-CAP canonical, V2-CAP alt.
- **MUTATE-N (the frozen, must-fail control): no compensation and no cap** (V1 clock, CAP support, canonical; src = e).
  It must NOT be GROWTH OK. If it is GROWTH OK the growth leg is NOT DIAGNOSTIC.
  Expectation (not blind): CFG424's no-compensation MUTATE gave 0.154 with the much smaller edge support, so this should
  be detected.
- **MUTATE-U (cap removed) = control C1:** the CAP engine with the cap switched off must reproduce CFG487's committed
  POST-HOC V1-CATCH canonical row (σ8 ratio 0.9972, max|P − 1| 0.1741) within 1e-3 on both numbers. Its outcome is
  known (TENSION), so it is a reproduction and attribution row, not a blind control.
- Reported: MUTA-CAP (FRW-firing clock with the cap, canonical): does the clock's history matter once capped?
- Reported diagnostics at z = 0: q_raw max, the catchment-mass fraction where the cap binds, Σsrc, e_mean.
- **Growth PASS for a version** iff GROWTH OK on both footings AND MUTATE-N detected (not GROWTH OK).
- **512³ rule:** a 512³ canonical run is made ONLY if a version passes (a) with MUTATE-N detected AND passes (b) and (c),
  AND no other 512³ job is running (`pgrep -f "N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"` empty, ERE form). Otherwise
  it is not run and the README says why.

**(b) KiDS** (CFG413's stack P via CFG487's copied harness: CFG377 primary stack, 181,477 lenses, 15 g_bar bins,
50-patch jackknife, Hartlap; free R^-0.8 two-halo amplitude profiled, sign free), PRIMARY cap:
PASS iff χ²(version) − χ²_best(CFG413) ≤ 4 on BOTH footings, χ²_best = 8.9479 / 9.7704 (cfg413_kids_results.json).
- Reported: the same with the two-halo term FROZEN at CFG495's committed A_equiv = 0.07 (in CFG377's R^-0.8 template;
  CFG495 FROZEN_CRITERIA a703a87da), and with A = 0; Δχ² against CFG413's x = 1 row; drop-one-bin range; fitted A against
  CFG486's range; outer-first cap row; the uncapped row (must equal CFG487's V1/V2 switch-only rows: control C2).

**(c) SPARC** (CFG346's S clauses via CFG487's copied harness): S-A3 |½ log10(M_mod/M_law)| < 0.03 at R_HI for ≥ 90% of
spirals and of dwarfs, and rotmod RAR |Δrms| < 0.005 dex, both footings. PASS iff all six clauses pass.

**(d) Early-type lensing levels (CFG485 caveat 2; REPORTED, not in the verdict):** CFG485's R8 construction (CFG95's
machinery read-only; released per-class blocks on K1; two-halo profiled per class, 6 dof), with the capped V1 / V2
taper-to-r_ta phantom in place of the 5.850 r_M truncation. Report χ² (free 2h and no 2h) for early and late types against
B1 (CFG95's law to 0.40 r_ta) and against CFG485's S (30.5 / 38.1 early). Label "early-type levels OK" iff
χ²_early − χ²_B1,early ≤ 4 on both footings (free 2h).

## 3. Verdict per version (frozen)
- **RECONCILED** iff (a) growth PASS (GROWTH OK both footings, MUTATE-N detected) AND (b) passes AND (c) passes.
- **RECONCILED, GROWTH NOT DIAGNOSTIC:** (b), (c) pass and both footings GROWTH OK, but MUTATE-N is also GROWTH OK.
- **NOT RECONCILED (legs):** otherwise; the failing legs are named.
- V1 always carries "MS1 EXCEPTION; NOT ADMISSIBLE under original MS1". V2 is strict MS1.
- A 512³ result, if run, can only lower a verdict (a 512³ TENSION/FAIL → NOT RECONCILED at 512³, stated beside the 256³).
- Legality is not re-derived here: CFG487's suffix (V1 CONDITIONAL, V2 over-couples gas; the ratchet has no fully legal
  ordinary action, CFG349) carries over. The catchment is bilocal (it needs the turnaround sphere), as CFG424's.

## 4. Controls (a failed control is reported and kept, never silently fixed)
- **C1** MUTATE-U reproduces CFG487 POST-HOC V1-CATCH canonical within 1e-3 (σ8 ratio and max|P − 1|).
- **C2** the uncapped analytic rows reproduce CFG487's committed V1/V2 switch-only KiDS χ² within 0.01 and its SPARC
  A3 / Δrms exactly; CFG413's x = 0.5 / 1.0 χ² reproduced within 0.01.
- **C3** PM mass conservation with the cap: |Σ src| / Σ e ≤ 1e-3 at every diagnostic snapshot, and comp ≤ s_c
  (min(s_c − comp) ≥ −1e-6 relative) in CAP runs.
- **C4** CFG485's machinery reproduces its committed R8 B1 χ² (early / late, both footings) within 1e-6.
- **C5** m in [0, 1] and never decreasing on any particle (as CFG487 C6).

## 5. Compute and hygiene
- Local compute only, no downloads. nice -n 10; at most 6 threads for this lane (two PM workers × 3 threads).
- Scripts, `.out`, `_MUTATE.out`, JSON, plain README in `campaign_fresh_gravity/CFG498_clock_taper_capped/`; large arrays
  in `../_external_data/cfg498_work/` (not committed). Commit locally; do not push.
