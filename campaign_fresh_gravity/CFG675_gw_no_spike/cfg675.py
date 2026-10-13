#!/usr/bin/env python3
"""CFG675: no cold-energy spike around black holes; LISA IMRI dephasing (criteria 1d8d97ca6).
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, io, json, math, hashlib, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG675_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, PC, C = C4.G_SI, C4.MSUN, C4.PC, 2.99792458e8
YR = 3.15576e7; RHO_U = MSUN / PC ** 3
nu = lambda y: np.asarray(C4.nu_mono(np.asarray(y, float)), float)

def rho_framework(r, m1, a0):
    """rho_c = (1/4 pi G r^2) d/dr [r^2 (nu-1) g_N], point mass m1 (nu_mono ceiling)"""
    lr = np.log(r); h = 1e-4
    def Q(x):
        rr = np.exp(x); gN = G * m1 / rr ** 2
        return rr ** 2 * (nu(gN / a0) - 1) * gN
    dQ = (Q(lr + h) - Q(lr - h)) / (2 * h) / r
    return dQ / (4 * math.pi * G * r ** 2)

def rho_spike(r, m1, gam, rho_sp=226 * RHO_U, r_sp=0.54 * PC):
    return rho_sp * (r_sp / r) ** gam

def dephase(m1s, m2s, rhof):
    m1, m2 = m1s * MSUN, m2s * MSUN; M = m1 + m2
    r_isco = 6 * G * m1 / C ** 2
    Pgw = lambda r: 32 / 5 * G ** 4 * m1 ** 2 * m2 ** 2 * M / (C ** 5 * r ** 5)
    lnL = math.log(math.sqrt(m1s / m2s))
    Pdf = lambda r: 4 * math.pi * G ** 2 * m2 ** 2 * rhof(r) * lnL / np.sqrt(G * m1 / r)
    dEdr = lambda r: G * m1 * m2 / (2 * r ** 2)
    f = lambda r: np.sqrt(G * M / r ** 3) / math.pi
    # vacuum: r(t) analytic t = (5/256) c^5 r^4 / (G^3 m1 m2 M); 5-yr start radius
    tau = lambda r: 5 / 256 * C ** 5 * r ** 4 / (G ** 3 * m1 * m2 * M)
    r_start = (5 * YR * 256 * G ** 3 * m1 * m2 * M / (5 * C ** 5) + r_isco ** 4) ** 0.25
    x = np.linspace(math.log(r_isco), math.log(r_start), 20001); r = np.exp(x)
    dt_vac = dEdr(r) / Pgw(r); dt_env = dEdr(r) / (Pgw(r) + Pdf(r))
    integ = f(r) * (dt_vac - dt_env) * r
    dN = float(np.sum(0.5 * (integ[1:] + integ[:-1]) * np.diff(x)))
    Nvac = float(np.sum(0.5 * ((f(r) * dt_vac * r)[1:] + (f(r) * dt_vac * r)[:-1]) * np.diff(x)))
    return dict(r_isco_pc=r_isco / PC, r_start_pc=r_start / PC, f_band_Hz=[float(f(r_start)), float(f(r_isco))],
                N_vac=Nvac, dN=dN, rho_at_rstart_Msun_pc3=float(rhof(np.array([r_start]))[0] / RHO_U),
                rho_at_1em3pc=float(rhof(np.array([1e-3 * PC]))[0] / RHO_U))

SYS = [(1e3, 1.4), (1e4, 10.0)]
out = {"lane": "CFG675", "criteria": "1d8d97ca6", "mutate": MUT, "framework_F0": {}, "dm_spike_context": {}}
L = []
for foot, a0 in C4.A0.items():
    out["framework_F0"][foot] = {}
    for m1, m2 in SYS:
        d = dephase(m1, m2, lambda r, m1=m1: rho_framework(r, m1 * MSUN, a0))
        out["framework_F0"][foot][f"{m1:g}+{m2:g}"] = d
        L.append(f"F0 {foot} {m1:g}+{m2:g}: N_vac {d['N_vac']:.3e}, dN = {d['dN']:.3e} cycles; rho_c(1e-3 pc) = {d["rho_at_1em3pc"]:.3e} Msun/pc^3")
for gam in (7 / 3, 9 / 4, 3 / 2):
    d = dephase(1e3, 1.4, lambda r, g=gam: rho_spike(r, 1e3 * MSUN, g))
    out["dm_spike_context"][f"gamma={gam:.3f}"] = d
    L.append(f"DM spike (static, rho_sp 226, r_sp 0.54 pc) gamma {gam:.3f}, 1e3+1.4: dN = {d['dN']:.3e}; rho(1e-3 pc) = {d["rho_at_1em3pc"]:.3e}")
ok = all(v["dN"] < 1 for f in out["framework_F0"].values() for v in f.values())
out["prediction"] = ("VACUUM-GR IMRI: framework cold-energy dephasing < 1 cycle (ceiling) for both systems, both footings"
                     if ok else "framework ceiling dephasing >= 1 cycle: see numbers")
L.append("PREDICTION: " + out["prediction"])
if MUT:
    z = dephase(1e3, 1.4, lambda r: 0 * r)["dN"]; big = dephase(1e3, 1.4, lambda r: 1e6 * rho_framework(r, 1e3 * MSUN, C4.A0["canonical"]))["dN"]
    bite = (z == 0.0) and (big > 1); L.append(f"MUTATE: rho=0 -> dN {z}; rho x1e6 -> dN {big:.3e}: {'BITES' if bite else 'DOES NOT BITE'}")
js = json.dumps(out, indent=1, sort_keys=True) + "\n"
open(os.path.join(HERE, f"cfg675_predictions{TAG}.json"), "w").write(js)
L.append(f"sha256(cfg675_predictions{TAG}.json) = {hashlib.sha256(js.encode()).hexdigest()}")
open(os.path.join(HERE, f"cfg675{TAG}.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
if MUT: sys.exit(1 if bite else 0)
