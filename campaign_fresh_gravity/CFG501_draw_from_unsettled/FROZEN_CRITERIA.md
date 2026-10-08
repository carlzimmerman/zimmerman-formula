# CFG501 FROZEN CRITERIA: draw the phantom only from UNSETTLED cold energy

Written 2026-10-08 and committed alone, before any CFG501 script exists and before any CFG501 number is computed.
Nothing below may change after a result is seen; any later departure goes in the README as a disclosed deviation.

**Standing.** κ = ½ is FITTED (it enters through a0). Kernel ν_mono. Both footings, a0 = 9.3603e-11 and 1.1312e-10 m/s²,
scored separately and never pooled. a0 flat in z. "Cold energy" = the cold clumping component (its MASS is still required;
no particle species). Never "theory closed"; never "the data favour the framework".

**Why this lane.** CFG498 (fb482c786): V1's settling clock (λ = 1, no edge) gives the broad taper KiDS wants
(+2.05 / +0.71 vs CFG413 best), but in the 256³ PM growth leg it loses 17-20% of the power at k = 1 h/Mpc, capped or not,
and the loss grows with the switch's support. CFG498's untested reading: the CFG424 compensation draws cold energy in
proportion to the LOCAL cold density, so it pulls source out of halo cores and moves it outward.

**The physical fix tested (zero new constants).** The phantom is built only from cold energy that has NOT YET SETTLED.
Settled cold energy is already part of the phantom profile and is not drawn again. The draw weight changes from
ρ_c to (1 − m) ρ_c, with m the V1 (or V2) clock's settled fraction (the same field that sets the taper).

**Not blind (disclosed).** I have read CFG498's README, criteria, engine, data, early-type, growth and verdict scripts and
its committed numbers (including the frozen-two-halo rows), and CFG413's committed x scan. Mental expectations (no script):
(i) in the PM, m is close to 1 in latched cores, so the (1 − m) weight should move the draw out of cores; but the unsettled
supply inside a catchment is smaller than the full cold supply, so the cap can bind more often and suppress the phantom;
(ii) analytically, CFG498's V1 q_raw against the full supply was 0.76-0.79; against the unsettled supply it will be larger,
possibly > 1 on many objects, in which case the uniform cap scales the phantom down and (b) / (c) can fail where CFG498
passed. Both outcomes are allowed; neither is the goal.

## 1. The object (one rule, two clock versions)

- **Clock:** exactly CFG487 §1 / CFG498: Dm/Dt = Γ L (1 − m), Γ = √(4πG ρ_X) (λ = 1), latch L never resets.
  - **V1** (cold-energy clock; MS1 EXCEPTION, NOT ADMISSIBLE under original MS1). **V2** (baryon clock, strict MS1).
- **Support:** phantom × m (the clock taper), no edge, inside the turnaround catchment (PM: the engine's in_cover(x = 1)
  components; analytic: r < r_ta), exactly as CFG498.
- **The draw (the only change):** inside each catchment, with e = m · max(s_ph − s_c, 0) and the unsettled cold energy
  w_c = (1 − m) · s_c (PM: m = the CIC mass-weighted settled-fraction grid SW that already multiplies the phantom):
  - q_raw = Σe / Σw_c (per catchment);
  - the cap on the unsettled supply: e → e / max(1, q_raw); comp = min(1, q_raw) · w_c;
  - so comp ≤ (1 − m) s_c ≤ s_c everywhere, and the added source src = e − comp still sums to zero on every catchment.
- **Inputs:** κ (via a0) and f_b. Nothing else. Inherited and disclosed (not tuned): ΛCDM spherical-collapse Δ_ta(z),
  MIX-A, the in_cover peak finder (threshold still contains T1's ε = 0.077, as in CFG424/487/498).

### Analytic implementation (KiDS, SPARC, early types)
- As CFG498: tapered phantom ΔM_ph(r) = ∫_0^r m dM_ph,law to r_ta, mass frozen beyond; V1 ρ_X = law mass, V2
  ρ_X = M_b(<r)/f_b; D = ΔM_ph(r_ta).
- **Unsettled supply** C_u = (1 − f_b) ∫_0^{r_ta} (1 − m(r)) dM_law(r), with M_law(r) = M_b ν(g_N/a0) the law's total mass
  (the catchment's matter, distributed as the law profile; M_law(r_ta) = M_ta to 5e-13 per CFG498), and m the same clock
  profile that tapers the phantom (V1 / V2). Innermost grid point: dM_law = M_law(r_0) with m(r_0).
- q_u = D / C_u. **PRIMARY (scored):** if q_u > 1 the whole tapered phantom is multiplied by 1/q_u (the PM's uniform rule).
- Reported rows: CFG498's full-supply cap (q = D / ((1 − f_b) M_ta); control C2) and the uncapped taper.
- Reported: q_u distribution (median, 90%, max) and the fraction of lens groups / lenses / galaxies / early-type nodes
  where the cap binds.

## 2. Tests

**(a) Growth**, 256³, seed 359, engine = a copy of CFG498's `cfg498_pm.py` (`cfg501_pm.py`) with ONLY the draw weight
changed (env switch: UNSETTLED default; PROP = CFG498's weight), plus extra z = 0 field dumps for the diagnostic (no effect
on dynamics). Mode CAP, both footings, against CFG359's S0 with CFG361's cuts: GROWTH OK iff |σ8 ratio − 1| ≤ 0.05 AND
max_{k ≤ 1 h/Mpc} |P ratio − 1| ≤ 0.10; FAIL if the σ8 shift > 20%; TENSION otherwise.
- Scored runs: V1-U canonical, V1-U alt, V2-U canonical, V2-U alt.
- **MUTATE-N (frozen must-fail control, kept from CFG498): no compensation and no cap** (V1 clock, canonical; src = e).
  The draw weight does not enter, so it is CFG498's MUTATE-N re-run in this engine. It must NOT be GROWTH OK; if it is,
  the growth leg is NOT DIAGNOSTIC.
- **Growth PASS for a version** iff GROWTH OK on both footings AND MUTATE-N is not GROWTH OK.
- **512³ rule:** a 512³ canonical run is made ONLY if a version passes (a), (b) and (c) at 256³ AND no other 512³ job is
  running (`pgrep -f "N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"` empty). A 512³ result can only lower a verdict.

**(b) KiDS** (CFG413's stack P via CFG498's harness: CFG377 primary stack, 181,477 lenses, 15 g_bar bins, 50-patch
jackknife, Hartlap; free R^-0.8 two-halo amplitude profiled): PASS iff χ²(version, PRIMARY) − χ²_best(CFG413) ≤ 4 on BOTH
footings, χ²_best = 8.9479 / 9.7704.
- Reported (no verdict weight): χ² with the two-halo amplitude FROZEN at CFG495's A_equiv = 0.07, compared with CFG413's
  best UNDER THE SAME FROZEN TREATMENT (the minimum over CFG413's x grid 0.23, 0.3, 0.4, 0.5, 0.7, 1.0, recomputed with the
  frozen amplitude); χ² with no two-halo; Δχ² vs CFG413 x = 1; drop-one-bin range; fitted A vs CFG486's range.

**(c) SPARC** (CFG346's S clauses via CFG498's harness): S-A3 |½ log10(M_mod/M_law)| < 0.03 at R_HI for ≥ 90% of spirals
and of dwarfs, and rotmod RAR |Δrms| < 0.005 dex, both footings, with the PRIMARY unsettled cap (q_u from each galaxy's
point-mass profile to r_ta, as CFG498 applies its q). PASS iff all six clauses pass.

**(d) Early-type levels (REPORTED, not in the verdict):** CFG498's CFG485-R8 construction with the unsettled-cap taper.
Label "early-type levels OK" iff χ²_early − χ²_B1,early ≤ 4 on both footings (free 2h).

**Core-emptying diagnostic (REPORTED, not in the verdict).** Fields dumped at z = 0 (1 + δ, e, comp, SW) for: the
PROP control run (CFG498's weight), V1-U canonical, V2-U canonical, MUTATE-N; S0 from CFG359's committed z = 0
particle positions (CIC on the 256³ mesh).
- Halo centres: local maxima (3×3×3) of S0's density smoothed by a Gaussian of σ = 1 cell, ranked by smoothed peak
  density, the top 200 with mutual separation ≥ 8 cells (periodic). In each run the centre is re-found as the maximum of
  that run's smoothed density within ±2 cells.
- Stacked over the 200 halos, in spherical shells of width 1 cell (0.78 Mpc/h) out to 12 cells: mean 1 + δ, e, comp,
  src = e − comp, SW. Reported: M_run(< r) / M_S0(< r) at r = 1, 2, 3, 6 cells; the fraction of the stacked draw Σcomp
  and of the stacked phantom Σe inside r ≤ 2 cells; the cumulative src(< r).
- "The (1 − m) draw stops emptying cores" is stated only if M(< 2 cells)/M_S0 for V1-U is closer to 1 than for PROP AND
  V1-U's draw fraction inside 2 cells is lower than PROP's. Otherwise the README says it does not.

## 3. Verdict per version (frozen)
- **RECONCILED** iff (a) growth PASS AND (b) passes AND (c) passes.
- **RECONCILED, GROWTH NOT DIAGNOSTIC:** (b), (c) pass and GROWTH OK both footings, but MUTATE-N is also GROWTH OK.
- **NOT RECONCILED (legs):** otherwise; the failing legs are named.
- V1 always carries "MS1 EXCEPTION; NOT ADMISSIBLE under original MS1". V2 is strict MS1.
- Legality is not re-derived: CFG487's suffix carries over (V1 conversion CONDITIONAL, V2 over-couples gas, the ratchet
  has no fully legal ordinary action, CFG349); the catchment is bilocal.

## 4. Controls (a failed control is reported and kept, never silently fixed)
- **C1** the PROP run (CFG498's weight, cap on, V1, canonical) reproduces CFG498's committed V1-CAP canonical run
  bit for bit: σ8 identical and the z = 0 P(k) array identical (max |ΔP| = 0).
- **C1b** (reported) MUTATE-N reproduces CFG498's MUTATE-N bit for bit.
- **C2** analytic: the full-supply-cap rows reproduce CFG498's V1_cap / V2_cap KiDS χ² within 0.01 and its SPARC A3 / Δrms
  exactly; CFG413's x = 0.5 / 1.0 χ² reproduced within 0.01.
- **C3** PM conservation: |Σ src| / Σ|e| ≤ 1e-3 at every diagnostic snapshot of every U run, and comp ≤ (1 − m) s_c
  (min((1 − m) s_c − comp)/s_c ≥ −1e-6).
- **C4** CFG485's machinery reproduces its committed R8 B1 χ² within 1e-6.
- **C5** m in [0, 1] and never decreasing on any particle.
- **Data MUTATE** (outputs `_MUTATE`): CFG498's FRW-firing clock (m = background value on every shell). Must move the V1
  PRIMARY KiDS χ² by > 4 on both footings from the real clock's row; otherwise the analytic leg is reported NOT DIAGNOSTIC.

## 5. Compute and hygiene
- Local compute only, no downloads. nice -n 10; at most 6 threads (two PM workers × 3 threads).
- Scripts, `.out`, `_MUTATE.out`, JSON, plain README in `campaign_fresh_gravity/CFG501_draw_from_unsettled/`; large
  arrays in `../_external_data/cfg501_work/` (not committed). Commit locally; do not push.
