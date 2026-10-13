#!/usr/bin/env python3
"""CFG677: our own answers to the two GW questions (criteria 0ec641cf5). Forecasts; assumptions explicit.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, io, json, math, contextlib, importlib.util
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
MUT = os.environ.get("CFG677_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
spec = importlib.util.spec_from_file_location("c675", os.path.join(LANES, "CFG675_gw_no_spike", "cfg675.py"))
src = open(spec.origin).read().split("SYS = [")[0]                     # reuse CFG675's physics, not its run block
g675 = {"__file__": spec.origin, "__name__": "c675"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, spec.origin, "exec"), g675)
dephase, rho_fw, MSUN, PC, RHO_U, A0 = g675["dephase"], g675["rho_framework"], g675["MSUN"], g675["PC"], g675["RHO_U"], g675["C4"].A0
L, out = [], {"lane": "CFG677", "criteria": "0ec641cf5", "mutate": MUT, "Q1": {}, "Q2": {}}
P = lambda s: (print(s, flush=True), L.append(s))

# ---------------- Q1
P("Q1: density bound from a no-dephasing IMRI (last 5 yr to ISCO)")
for m1, m2 in ((1e3, 1.4), (1e4, 10.0)):
    b = dephase(m1, m2, lambda r: 0 * r); rp = math.sqrt(b["r_isco_pc"] * b["r_start_pc"]) * PC
    ceil_1em3 = float(rho_fw(np.array([1e-3 * PC]), m1 * MSUN, A0["canonical"])[0] / RHO_U)
    ceil_rp = float(rho_fw(np.array([rp]), m1 * MSUN, A0["canonical"])[0] / RHO_U)
    for gam in (1.0, 1.5, 7 / 3):
        for th in (1.0, 10.0):
            f = lambda lr: dephase(m1, m2, lambda r: 10 ** lr * RHO_U * (r / rp) ** (-gam))["dN"] - th
            lr = brentq(f, -10, 30, xtol=1e-4)
            rho_p = 10 ** lr; rho_1em3 = rho_p * ((1e-3 * PC) / rp) ** (-gam)
            key = f"{m1:g}+{m2:g} gamma={gam:.3f} dN={th:g}"
            out["Q1"][key] = dict(r_probe_pc=rp / PC, rho_bound_at_rprobe=rho_p, rho_bound_at_1em3pc=rho_1em3,
                                  framework_ceiling_at_rprobe=ceil_rp, framework_ceiling_at_1em3pc=ceil_1em3,
                                  bound_over_killline_1em3pc=rho_1em3 / (10 * ceil_1em3))
            P(f"  {key}: r_probe {rp/PC:.2e} pc; rho < {rho_p:.2e} Msun/pc^3 there (framework ceiling {ceil_rp:.2e}); "
              f"extrapolated to 1e-3 pc: {rho_1em3:.2e} (kill line {10*ceil_1em3:.2e}; ratio {rho_1em3/(10*ceil_1em3):.2e})")

# ---------------- Q2
P("Q2: own Fisher forecast for 3G bright sirens, GW alone (H0, Om, w0, wa)")
C = 299792.458
def dL(z, H0, om, w0, wa):
    E = lambda x: math.sqrt(om * (1 + x) ** 3 + (1 - om) * (1 + x) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * x / (1 + x)))
    return (1 + z) * C / H0 * quad(lambda x: 1 / E(x), 0, z, epsabs=0, epsrel=1e-9)[0]
fid = np.array([67.0, 0.31, -0.752, -0.86])          # DESY5 combination (CFG676) as fiducial
zg = np.linspace(0.05, 3.0, 60); w = zg ** 2 * np.exp(-zg / 0.6); w /= w.sum()
lens = lambda z: 0.066 * ((1 - (1 + z) ** -0.25) / 0.25) ** 1.8
def deriv(z):
    g = []
    for i, h in enumerate((0.1, 0.002, 0.005, 0.02)):
        p, m = fid.copy(), fid.copy(); p[i] += h; m[i] -= h
        g.append((math.log(dL(z, *p)) - math.log(dL(z, *m))) / (2 * h))
    return np.array(g)
D = np.array([deriv(z) for z in zg])
for delens in (1.0, 0.5):
    for sinst in (0.05,):
        for N in (100, 300, 1000, 3000):
            for prior in (None, 0.01):
                sig = np.sqrt(sinst ** 2 + (delens * lens(zg)) ** 2)
                F = (D.T * (N * w / sig ** 2)) @ D
                if prior: F[1, 1] += 1 / prior ** 2
                cov = np.linalg.inv(F); s0, sa = math.sqrt(cov[2, 2]), math.sqrt(cov[3, 3]); rho = cov[2, 3] / (s0 * sa)
                meet = s0 <= 0.06 and sa <= 0.11
                key = f"N={N} sinst={sinst} lens x{delens}" + (" +Om prior 0.01" if prior else " GW-alone")
                out["Q2"][key] = dict(sigma_w0=s0, sigma_wa=sa, corr=rho, meets_CFG676_z3=meet)
                P(f"  {key}: sigma(w0) {s0:.3f}, sigma(wa) {sa:.3f}, corr {rho:+.2f}  -> CFG676 z=3 requirement {'MET' if meet else 'not met'}")
if MUT:
    z0 = dephase(1e3, 1.4, lambda r: 0 * r)["dN"] == 0.0
    sig = np.sqrt(0.05 ** 2 + (0.5 * lens(zg)) ** 2)
    sw = lambda sg: math.sqrt(np.linalg.inv((D.T * (1000 * w / sg ** 2)) @ D)[2, 2])
    a, b2 = sw(sig), sw(sig / 2)
    bite = z0 and abs(a / b2 - 2) < 1e-6; P(f"MUTATE: rho0 dN=0 {z0}; sigma_lnD halved: sigma(w0) {a:.4f}->{b2:.4f} (ratio {a/b2:.6f}): {'BITES' if bite else 'NO'}")
json.dump(out, open(os.path.join(HERE, f"cfg677_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg677{TAG}.out"), "w").write("\n".join(L) + "\n")
if MUT: sys.exit(1 if bite else 0)
