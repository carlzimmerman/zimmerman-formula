# X74_all_measured_native_cf: PENDING A4 (pre-built; identity checks pass)

Criteria: `FROZEN_CRITERIA.md` (c3e69578c5), committed before this script and before any A4 number.
Governing post-A4 regrade of route E: X73's all-measured configuration (smooth core, native Ω_c/Ω_b, measured X-COP gas
tail to r_ta, measured f★) with the native c_f(M) from X48 A4. X72 (the X71 configuration) is still run as frozen.

## Pre-built checks (no A4 number used)
- **K1 identity:** with c_f ≡ 4, `x74_native_cf.py` reproduces X73's committed PRIMARY JSON exactly at f★ 0.034 and
  0.0615 (cluster preds, SPARC rms, groups Z: max |d| = 0). Logs `k1_fs*.log`, outputs `x74_results_fs*_c4_*.json`.
- **K2:** η(M) equals the formula at 1e12–1e15 (PASS).
- **K3:** the inherited check pattern matches X73 (K0 / K0x38 fail off f★ 0.20 by construction, as in X73 and X71;
  hence exit 1 at these f★).
- **Sensitivity (reported, not graded; not A4):** c_f ≡ 8 (X74_CFMULT=2 on the constant) moves G-OUT-M3's pred
  1.447 → 1.617 (Z by −1.64) and fails both footings: SPARC line and six cluster keys OVER (`sens_cf8.log`). The pass
  window in c_f is narrow. For scale only: X48 A3's native c_f at 1e12 (ng 64) is 7.74; the cluster masses are not yet
  measured at ng 64.

## After A4
`watch_A4_then_run.sh` (nohup, one `ls` per 10 min) waits for all 18 `done.json`, then runs X72's frozen
`run_after_A4.sh` (builds `x48_analyze_results_ng64_A4.json`, scores PREREG 23095bf23a, grades X72) and this lane's
`run_after_A4.sh` (PRIMARY at both f★, s16/s84, MUTATE). Log: `watch_A4.log`.

κ = ½ FITTED. Footings never pooled. c_f label becomes [c_f NATIVE, X48 A4] on native runs. Cold dark energy is a
gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
