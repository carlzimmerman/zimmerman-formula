#!/usr/bin/env python3
"""V1 (Gauss law vs analytic), V2 (Poisson vs Plummer), V4 (resume equivalence) for khronon_fluid.py."""
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("kf", HERE / "khronon_fluid.py")
kf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kf)
G = kf.G
checks, out = [], {}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:3s} {'PASS' if ok else 'FAIL'}  {detail}")


def v1(h, sign, a0):
    g = kf.Grid(h)
    b = 200.0
    GQ = sign * 0.5 * a0 * b ** 2 / ((1 / math.sqrt(2)) / 1.5 ** 1.5)
    rr = np.linspace(0, 4000, 400001)
    f = GQ * rr / (rr ** 2 + b ** 2) ** 1.5                                # signed radial component of P*4piG
    A = f / (1 - np.abs(f) / a0)
    Psi_r = cumulative_trapezoid(A, rr, initial=0.0)
    Psi = lambda R, z: np.interp(np.sqrt(R ** 2 + z ** 2), rr, Psi_r)
    bc = g.bc_values(Psi)
    r = np.hypot(g.RR, g.ZZ)
    rho = (3 * GQ / (4 * math.pi * G)) * b ** 2 / (r ** 2 + b ** 2) ** 2.5
    P, nit, res = g.gauss(4 * math.pi * G * rho, bc, a0)
    gR, gz = g.cell_grad(P, bc)
    num = np.hypot(gR, gz)
    ana = np.abs(np.interp(r, rr, A))
    sel = (r >= 2 * h) & (r <= 1500)
    err = float(np.max(np.abs(num[sel] - ana[sel]) / ana[sel]))
    return err, nit, res


a0 = kf.A0["canonical"]
e20 = [v1(20.0, s, a0) for s in (1, -1)]
e10 = [v1(10.0, s, a0) for s in (1, -1)]
ok1 = all(e[0] <= 0.03 for e in e20) and all(e20[i][0] / e10[i][0] >= 2.5 for i in range(2))
record("V1", ok1, f"Gauss law, Plummer-profile charge, max|f| = 0.5 a0: max rel err of |grad Psi| (r 2h-1500 kpc) "
                  f"h=20: {e20[0][0]:.4f} (+) / {e20[1][0]:.4f} (-); h=10: {e10[0][0]:.4f} / {e10[1][0]:.4f}; ratios "
                  f"{e20[0][0] / e10[0][0]:.2f} / {e20[1][0] / e10[1][0]:.2f}; iterations {e20[0][1]}/{e20[1][1]}, residual {e20[0][2]:.1e}")
out["V1"] = {"h20": e20, "h10": e10}

# V2 Poisson vs Plummer (one sphere at the origin), h = 20
g = kf.Grid(20.0)
M = 1e11
phi_an = lambda R, z: -G * M / np.sqrt(R ** 2 + z ** 2 + kf.EPS ** 2)
bc = g.bc_values(phi_an)
d = kf.plummer_rho(g, g.RR, g.ZZ, 0.0, M)
rho = d * M / np.sum(d * g.V)
phi = g.poisson(4 * math.pi * G * rho, bc)
gR, gz = g.cell_grad(phi, bc)
r = np.hypot(g.RR, g.ZZ)
ana = G * M * r / (r ** 2 + kf.EPS ** 2) ** 1.5
sel = (r >= 3 * kf.EPS) & (r <= 1500)
err2 = float(np.max(np.abs(np.hypot(gR, gz)[sel] - ana[sel]) / ana[sel]))
record("V2", err2 <= 0.02, f"Poisson, Plummer 1e11 Msun: max rel err of |grad phi| for r >= 3 eps: {err2:.4f}")
out["V2"] = err2

# V4 resume equivalence: 40-step segment uninterrupted vs SIGTERM-equivalent stop at step 17 + --resume
base = [sys.executable, str(HERE / "khronon_fluid.py"), "--foot", "canonical", "--orbit", "O1", "--ti", "6", "--tsteps", "40"]
runs = HERE / "runs"
for t in ("v4_full", "v4_cut"):
    for ext in (".json", ".ckpt.npz"):
        p = runs / f"{t}{ext}"
        if p.exists():
            p.unlink()
r1 = subprocess.run(base + ["--tag", "v4_full"], capture_output=True, text=True)
r2 = subprocess.run(base + ["--tag", "v4_cut", "--kill-at-step", "17"], capture_output=True, text=True)
r3 = subprocess.run(base + ["--tag", "v4_cut", "--kill-at-step", "17", "--resume"], capture_output=True, text=True)
r4 = subprocess.run(base + ["--tag", "v4_cut", "--resume"], capture_output=True, text=True)
A = json.loads((runs / "v4_full.json").read_text())
B = json.loads((runs / "v4_cut.json").read_text())
same = np.array_equal(np.array(A["final_Rp"]), np.array(B["final_Rp"])) and np.array_equal(np.array(A["final_zp"]), np.array(B["final_zp"]))
record("V4", r1.returncode == 0 and r2.returncode == 75 and r3.returncode == 0 and r4.returncode == 0 and same,
       f"exit codes full {r1.returncode}, cut {r2.returncode} (75 = yield), resume {r3.returncode}, re-resume {r4.returncode} "
       f"(0 = idempotent); final positions bit-identical: {same}")
out["V4"] = {"codes": [r1.returncode, r2.returncode, r3.returncode, r4.returncode], "bit_identical": same}
out["checks"] = checks
(HERE / "kf_tests_results.json").write_text(json.dumps(out, indent=1, default=float))
print(f"{sum(c['pass'] for c in checks)}/{len(checks)} PASS")
