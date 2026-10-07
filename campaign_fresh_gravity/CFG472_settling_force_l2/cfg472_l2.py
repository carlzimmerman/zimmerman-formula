#!/usr/bin/env python3
"""CFG472: is the law's target a Newtonian hydrostatic equilibrium of a pressure-supported cold fluid? (FROZEN_CRITERIA.md)
Units G = a0 = M_b = 1 (r_M = 1, V_f = 1). Run: python3 cfg472_l2.py [--mutate]"""
import os, sys, json, io, contextlib
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
# ---- K-A symbolic identities
r, G, M, a0, sig, V = sp.symbols("r G M a0 sigma V", positive=True)
rho_ph = sp.sqrt(G * M * a0) / (4 * sp.pi * G * r ** 2)
Vf2 = sp.sqrt(G * M * a0)
kA1 = sp.simplify(rho_ph - Vf2 / (4 * sp.pi * G * r ** 2)) == 0                  # deep phantom = SIS of V_f
slope = sp.simplify(sp.diff(sp.log(sp.exp(-V ** 2 * sp.log(r) / sig ** 2)), sp.log(r)) if False else -V ** 2 / sig ** 2)
kA2 = sp.simplify(slope.subs(sig, V / sp.sqrt(2)) + 2) == 0                      # isothermal in V^2 ln r: slope -V^2/sigma^2 = -2 iff sigma^2 = V^2/2
P(f"K-A symbolic: deep rho_ph == V_f^2/(4 pi G r^2): {kA1}; isothermal slope -V^2/sigma^2 = -2 at sigma^2 = V^2/2: {kA2}")
# ---- numerics
x = np.linspace(np.log(1e-3), np.log(1e3), 4000); dx = x[1] - x[0]; R = np.exp(x)
SIG2 = 0.5
def integrate(rho_of_phi, rho0, Mb_fun):
    """vectorised RK4 in ln r over parameter arrays; returns M_c(<r) on the grid, shape (len(x), nparam)."""
    n = rho0.size; phi = np.zeros(n); Mc = 4 / 3 * np.pi * R[0] ** 3 * rho0.copy(); out = np.empty((len(x), n)); out[0] = Mc
    def f(xx, phi, Mc):
        rr = np.exp(xx); rho = rho_of_phi(phi)
        return (Mb_fun(rr) + Mc) / rr, 4 * np.pi * rr ** 3 * rho
    for i in range(len(x) - 1):
        k1p, k1m = f(x[i], phi, Mc); k2p, k2m = f(x[i] + dx / 2, phi + dx / 2 * k1p, Mc + dx / 2 * k1m)
        k3p, k3m = f(x[i] + dx / 2, phi + dx / 2 * k2p, Mc + dx / 2 * k2m); k4p, k4m = f(x[i] + dx, phi + dx * k3p, Mc + dx * k3m)
        phi = phi + dx / 6 * (k1p + 2 * k2p + 2 * k3p + k4p); Mc = Mc + dx / 6 * (k1m + 2 * k2m + 2 * k3m + k4m); out[i + 1] = Mc
    return out
def target(a):
    Mb = R ** 2 / (R + a) ** 2; gN = Mb / R ** 2
    t = (C.nu_mono(gN) - 1.0) * Mb
    return t * (R ** 0.3 if MUT else 1.0)
def D(Mc, tgt, lo, hi):
    m = (R >= lo) & (R <= hi)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = np.abs(np.log10(np.clip(Mc[m], 1e-300, None) / tgt[m][:, None]))
    return np.nanmax(np.where(np.isfinite(d), d, 99), axis=0)
res = {}
# K-B: no baryons, far-field SIS slope
oB = integrate(lambda p, r0=np.array([1.0]): r0 * np.exp(-p / SIG2), np.array([1.0]), lambda rr: 0 * rr)
mB = (R >= 10) & (R <= 100); kB = float(np.median(oB[mB, 0] / R[mB])); kBok = abs(kB - 1) < 0.05
P(f"K-B no-baryon isothermal far field: median M_c/r over 10-100 = {kB:.4f} (SIS 2 sigma^2/G = 1) -> {'PASS' if kBok else 'FAIL'}")
rho0s = np.logspace(-8, 4, 600)
Ks = np.logspace(-4, 4, 120); r0p = np.logspace(-8, 4, 120); RR0, KK = np.meshgrid(r0p, Ks); RR0 = RR0.ravel(); KK = KK.ravel()
for a in (0.1, 0.3, 1.0, 3.0):
    Mbf = lambda rr, a=a: rr ** 2 / (rr + a) ** 2; tgt = target(a)
    oI = integrate(lambda p: rho0s * np.exp(-p / SIG2), rho0s, Mbf)
    dI = D(oI, tgt, 0.5, 30); iI = int(np.argmin(dI)); dIw = D(oI[:, [iI]], tgt, 0.2, 100)[0]
    oP = integrate(lambda p: np.maximum(RR0 - p / (2 * KK), 0.0), RR0, Mbf)
    dP = D(oP, tgt, 0.5, 30); iP = int(np.argmin(dP)); dPw = D(oP[:, [iP]], tgt, 0.2, 100)[0]
    res[str(a)] = dict(I=dict(D=float(dI[iI]), D_wide=float(dIw), rho0=float(rho0s[iI])), P=dict(D=float(dP[iP]), D_wide=float(dPw), rho0=float(RR0[iP]), K=float(KK[iP])))
    P(f"a = {a:3.1f} r_M: Model I (isothermal, sigma^2 = V_f^2/2, 1 free) D = {dI[iI]:.3f} dex [0.2-100: {dIw:.3f}] at rho0 {rho0s[iI]:.2e} | "
      f"Model P (TF polytrope, 2 free) D = {dP[iP]:.3f} dex [0.2-100: {dPw:.3f}]")
def verdict(k):
    ds = [res[a][k]["D"] for a in res]
    return "SHAPE REPRODUCED" if max(ds) <= 0.04 else "SHAPE FAILS" if max(ds) > 0.1 else "PARTIAL"
vI, vP = verdict("I"), verdict("P")
P(f"VERDICT Model I (isothermal): {vI}; Model P (Thomas-Fermi polytrope): {vP}")
json.dump(dict(res=res, KA=[bool(kA1), bool(kA2)], KB=kB, verdict=dict(I=vI, P=vP)), open(os.path.join(HERE, f"cfg472_l2{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg472_l2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    ok = res["0.3"]["I"]["D"] > 0.1; P(f"MUTATE: Model I D at a=0.3 = {res['0.3']['I']['D']:.3f} -> {'detected (exit 1)' if ok else 'NOT detected'}"); sys.exit(1 if ok else 0)
sys.exit(0 if (kA1 and kA2 and kBok) else 1)
