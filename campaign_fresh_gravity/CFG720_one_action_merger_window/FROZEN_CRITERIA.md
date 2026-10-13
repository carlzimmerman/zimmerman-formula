# CFG720 FROZEN CRITERIA: the one-action construction C* on the merger stopwatch (response-time window)

Date: 2026-10-13. Written and committed ALONE, before any CFG720 code or run. Block CFG720–729 (owner reservation, d71aab58a). Nothing
below may be edited after this commit.

κ = ½ is fitted. Footings (canonical, alt) judged separately, never pooled. The cold energy's mass is required. No particle species.
Not "theory closed". Yardsticks are CFG623's raw data (Bullet f, Harvey β̄). Nothing will be phrased as "the data favour the
framework". The Lean / orchestrator chat's lanes (CFG690–699, CFG658) are read only.

## 0. What has been seen (stated before any choice below)

- CFG658 / CFG694 / CFG695 (other chat): C* = vacuum polarization P whose bound charge ∇·P is the cold mass, critical quadratic,
  saturating W (static law g_N = g²/(g + a₀), ν_s(y) = ½ + √(¼ + 1/y)), stiffness L* = 5.75 pc, free-fall basins. It passes the EFE
  gates, SPARC and CFG686 cluster shear; fails C3 (early types) and X-COP as built. **It has not faced the merger stopwatch.** It has
  no phase label, so its bound charge responds to all baryons, hot gas included (CFG658's A5 tension).
- CFG623 (VALID): the α = ∞ class (phantom recomputed from the baryons every step, CFG599 field mode, ν_mono) is **EXCLUDED** on both
  footings (Bullet f 1.027 / 1.052, Z_B +7.86 / +8.06; Harvey Z_H +15.0 / +15.1). CFG639, CFG641 seen.
- **Author's expectation, before any run:** C* with instant response is the α = ∞ class with a slightly different kernel, so it
  should be EXCLUDED; a lag of order the time since pericentre (≈ 0.2–0.6 Gyr) or longer is needed. The inertia (I/2)|Ṗ|² of C* sets
  that lag, but I is a free constant of the action.

## 1. Model

- CFG623's pipeline unchanged (cfg622_sim, the masked estimator, Harvey window, stability rule, scores), imported read-only.
- **Field mode** (CFG599 α = ∞): no cold particles; the cold mass is a grid field built from each progenitor's own baryons by the
  round rule inside r_t (CFG599 `phantom_field`, the record's stand-in for per-system basins).
- **Kernel:** the static law of C*, ν_s(y) = ½ + √(¼ + 1/y), swapped in for ν_mono (in the progenitors and in the field), as CFG658
  swaps kernels.
- **Lag:** the field relaxes toward its instantaneous target with response time t_resp,
  field ← field + (target − field)(1 − e^(−Δt/t_resp)); t_resp = 0 is instant (CFG623's α = ∞ update). This is an **overdamped**
  linear-response stand-in for (I/2)|Ṗ|²; the undamped (oscillating) case is not tested.
- **Nodes:** t_resp ∈ {0, 0.1, 0.3, 1, 3} Gyr × both footings = 10 runs.
- **Calibration:** (v0, η) re-fit with CFG621's `calibrate()` in field mode, ν_s, t_resp = 0, canonical (as CFG641 did per model);
  held for every node and both footings. If calibration fails, the lane is VOID. Footing validity (CFG623 K1/G1) is checked at
  t_resp = 0.

## 2. Controls

- **C-R:** ν_mono, t_resp = 0, CFG621's calibration must reproduce CFG623's `ainf_can` run exactly (max 0 kpc over epochs; sub
  gal/gas/lens/variants). If not, VOID.
- **C-L (lag acts):** at t_resp = 1 Gyr (canonical), the field's mass-weighted centroid offset from its instantaneous target at the
  first epoch after pericentre must exceed 20 kpc; otherwise the lag is NOT DIAGNOSTIC.

## 3. Verdicts (CFG623's score_run and classes unchanged; no interpolation between nodes)

- **VR-1 (quasi-static C*):** the class of t_resp = 0 on both footings (expected EXCLUDED).
- **VR-2 (window):** the smallest t_resp node ALLOWED on both footings, reported as "mergers require t_resp ≥ that node"; **NO WINDOW
  UP TO 3 Gyr** if none is allowed.
- **VR-3 (galaxy compatibility of the window):** C*'s static galaxy passes assume the field has equilibrated. Declared rule: COMPATIBLE
  if the smallest allowed node is ≤ 1 Gyr (≥ 5 e-folds in a 5 Gyr-old galaxy); TENSION if it is 3 Gyr; INCOMPATIBLE if NO WINDOW.

## 4. MUTATE (`CFG720_MUTATE=1`)

- M1: t_resp = 0 with ν_s must differ from the C-R ν_mono run (the kernel swap acts): max sub lens difference > 5 kpc.
- M2: a huge lag (t_resp = 100 Gyr) must make the field nearly static: Bullet f within 0.1 of the field-frozen-at-t=0 expectation (the
  field stays with its starting positions, so f should fall well below t_resp = 0's value).

## 5. Machine rules

Heavy (CFG623 footprint ≈ 10 GB over 4 processes). A waiter starts CFG720 only when no `_pm.py` 1024³ job (cfg596/636/640/650) or other
merger lane is running and ≥ 16 GB is free; ≤ 4 processes, `nice -n 10`, one thread each.
