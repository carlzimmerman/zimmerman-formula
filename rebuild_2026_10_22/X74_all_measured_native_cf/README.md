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

## Pre-read before A4 (2026-10-29; plan `PREREAD_A3_PLAN.md`, 1eb269646d; not part of X74's verdict)
Only committed inputs: X48 A3's ng 64 median c_f(10¹²) = 7.74 (68 % 6.10–9.24, labelled RESOLUTION-DEPENDENT).
No A4 output opened. The outputs carry the script's automatic label "[c_f NATIVE, X48 A4]"; for these runs read it as
"A3 at 10¹² plus the stated assumed values at 10¹³/10¹⁴". Files: `preread_*`. Each run took about 1 min and used 0.44–0.48 GB.

SPARC line = rms ≤ 0.110 and median Υ in [0.50, 0.80] (EM1 `line`). Canonical footing, f★ 0.034 (0.0615 is identical on SPARC):

| c_f(10¹²) (clusters at 4) | rule active (of 175) | rms | median Υ | canonical line | alt line (Υ) |
|---|---|---|---|---|---|
| 4 (X73 / K1) | 0 | 0.0713 | 0.56 | PASS | FAIL (0.47) |
| 5 (bracket) | 9 | 0.0713 | 0.56 | PASS | FAIL (0.47) |
| 6 (bracket) | 41 | 0.0698 | 0.54 | PASS | FAIL (0.47) |
| 7 (bracket) | 56 | 0.0683 | 0.51 | PASS | FAIL (0.44) |
| **7.74 (A3, P1)** | 66 | 0.0685 | **0.48** | **FAIL** | FAIL (0.43) |

- **P1 (A3 at 10¹², clusters at the best case 4):**
  - Every cluster key and the groups pass.
  - The SPARC line fails on both footings at both f★.
  - The frozen read is triggered: "A3 already breaks X74's SPARC line".
- **The break is narrow, and its mechanism is the Υ floor, not the fit.**
  - The collapse branch adds core mass to the brighter galaxies, so the best-fit stellar Υ falls below 0.50. The rms actually improves.
  - The canonical boundary lies between c_f(10¹²) = 7.0 and 7.74.
  - A3's own 68 % interval (6.10–9.24) straddles it. **At A3's precision this is a knife edge, not a settled break.**
  - The 5/6/7 bracket was added after the plan and is reported only.
- **The alt footing fails the SPARC line at every c_f tried, including 4,** on Υ 0.47 against 0.50. This is X73's own state: its pass was canonical-only. X74's label needs both footings to agree, so on the frozen rule X74 cannot read PASSES at f★ 0.034/0.0615 whatever A4 gives. The headline stays canonical.
- **P2 (7.74 flat):** SPARC fails, and five cluster keys go OVER, as `sens_cf8.log` shows.
- **What decides X74's canonical line is c_f(10¹²) convergence (ng ≥ 80) and its error, not A4's cluster masses.** A4 still decides the cluster keys.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
