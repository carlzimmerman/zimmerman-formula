#!/usr/bin/env python3
"""CFG378 controls (FROZEN_CRITERIA.md 18bfc1a98).
Normal mode: C1 mass conservation (every snapshot of every run JSON present), C2 Gamma = 0 two-species == single-species S0 (128^3 DEV),
C3 settling-step algebra on a 64^3 test field.  MUTATE mode (CFG378_MUTATE=1): C1 on the MUTATE run + the sensitivity check
(target x10 must move z = 0 sigma8 by >= 1% vs the unmutated 128^3 g = 1 canonical run).  Writes cfg378_checks[_MUTATE].out; rc 1 on any failure."""
import os, sys, json, glob, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("eng", os.path.join(HERE, "cfg378_pm.py")); eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
W = eng.WORK; MUT = eng.MUTATE; LOG = []; ok_all = True
def P(s=""): print(s); LOG.append(s)
def chk(name, ok, msg):
    global ok_all
    ok_all &= bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  {msg}")
def load(tag):
    p = os.path.join(W, f"cfg378_{tag}.json"); return json.load(open(p)) if os.path.exists(p) else None
P(f"CFG378 checks ({'MUTATE' if MUT else 'normal'})")
# ---- C1 on every run JSON in scope
files = sorted(glob.glob(os.path.join(W, "cfg378_*.json")))
files = [f for f in files if ("_MUTATE" in f) == MUT and "SMOKE" not in f]
for f in files:
    r = json.load(open(f)); N = r["np"] ** 3; worst = 0.0; cnt = True; mn = 1e30
    for s in r["snap"].values():
        worst = max(worst, s["cold_mass_total_rel_err"]); cnt &= s["cold_count"] == N; mn = min(mn, s["cold_min_cic"])
    chk(f"C1 {r['tag']}", worst <= 1e-10 and cnt and mn >= 0, f"max mass rel err {worst:.1e}, count const {cnt}, min cold CIC {mn:.3g} (overdraw 0 by construction)")
if not MUT:
    # ---- C2
    a, b = load("TWO_g0_FLAT_canonical_N128_DEV"), load("S0_g0_FLAT_canonical_N128_DEV")
    if a and b:
        sa, sb = a["snap"]["z0"], b["snap"]["z0"]; r8 = sa["sigma8"] / sb["sigma8"]
        pr = np.array(sa["P"]) / np.array(sb["P"]); k = np.array(sa["k"]); dp = float(np.max(np.abs(pr[k <= 1] - 1)))
        chk("C2 Gamma=0 == S0 (128^3)", abs(r8 - 1) <= 1e-4 and dp <= 1e-3, f"sigma8 ratio - 1 = {r8 - 1:.2e}, max|P-1| k<=1 = {dp:.2e}")
    else:
        chk("C2 Gamma=0 == S0 (128^3)", False, "runs missing")
    # ---- C3 step algebra on a 64^3 test field
    m = eng.Mesh(64); pos, _ = eng.initial_conditions(64, 1.0)
    pos = (pos + 0.0) % eng.L
    q = (np.indices((64,) * 3).reshape(3, -1).T + 0.5) * (eng.L / 64)
    disp = (pos - q + eng.L / 2) % eng.L - eng.L / 2
    pos = (q + 25.0 * disp) % eng.L                       # IC displacements x25 -> a clustered test field
    x = (np.indices((64,) * 3) + 0.5) * (eng.L / 64)
    blob = 1.0 + 4.0 * np.exp(-((x[0] - 100) ** 2 + (x[1] - 100) ** 2 + (x[2] - 100) ** 2) / (2 * 20.0 ** 2))
    rho_t = (blob / blob.mean() * (1 - eng.FB)).astype(np.float32)
    N = pos.shape[0]; rc = eng.deposit_raw(m, pos); rho_c = (1 - eng.FB) * rc / (N / 64 ** 3)
    F = eng.FLOOR_FRAC * (1 - eng.FB)
    d0 = float(np.sum((np.log(np.maximum(rho_c, F)) - np.log(rho_t)) ** 2))
    info = eng.settle(m, pos, rho_c.astype(np.float32), rho_t, np.full((64,) * 3, 0.2, np.float32))
    rc2 = eng.deposit_raw(m, pos); rho_c2 = (1 - eng.FB) * rc2 / (N / 64 ** 3)
    d1 = float(np.sum((np.log(np.maximum(rho_c2, F)) - np.log(rho_t)) ** 2))
    chk("C3 one step moves rho_c toward rho_t", d1 < d0, f"sum(log ratio)^2 {d0:.4g} -> {d1:.4g} ({d1 / d0:.3f}); clip frac {info['clip_frac']:.3f}")
    chk("C3 mass exact", pos.shape[0] == N and abs(rc2.sum() - N) / N <= 1e-10, f"count {pos.shape[0]} = {N}, total rel err {abs(rc2.sum() - N) / N:.1e}")
else:
    a, b = load("TWO_g1_FLAT_canonical_N128_DEV_MUTATE"), load("TWO_g1_FLAT_canonical_N128_DEV")
    if a and b:
        d = a["snap"]["z0"]["sigma8"] / b["snap"]["z0"]["sigma8"] - 1
        chk("MUTATE target x10 moves sigma8 by >= 1%", abs(d) >= 0.01, f"sigma8(x10)/sigma8(x1) - 1 = {d:+.4f}; R x10 {a['snap']['z0']['R']:.3f} vs x1 {b['snap']['z0']['R']:.3f}")
    else:
        chk("MUTATE", False, "runs missing")
P(f"  overall: {'PASS' if ok_all else 'FAIL'}")
open(os.path.join(HERE, "cfg378_checks" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if ok_all else 1)
