#!/usr/bin/env python3
"""CFG473: locality of the force needed to hold an isothermal fluid at the law's target (FROZEN_CRITERIA.md). Run: python3 cfg473_locality.py [--mutate]"""
import os, sys, json, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
SIG2 = 0.5 * (2 if MUT else 1)
R = np.logspace(-3, 3, 20001); lr = np.log(R)
def profile(Mb):
    gN = Mb / R ** 2; nu = C.nu_mono(gN); Mph = (nu - 1) * Mb
    rho = np.gradient(Mph, R) / (4 * np.pi * R ** 2)
    dlnrho = np.gradient(np.log(np.clip(rho, 1e-300, None)), R)
    f = SIG2 * dlnrho + nu * gN
    return gN, nu, rho, dlnrho, f
gP, nuP, rhoP, dlP, fP = profile(np.ones_like(R))       # point mass
m = R >= 30
k1 = float(np.max(np.abs(fP[m]) / (nuP[m] * gP[m]))); k1ok = k1 < 0.01
k2 = float(np.max(np.abs(dlP[m] * R[m] + 2) / 2)); k2ok = k2 < 0.01
P(f"K1 point-mass deep f / (nu gN) max over r>=30: {k1:.4f} -> {'PASS' if k1ok else 'FAIL'};  K2 dln rho/dr vs -2/r: {k2:.4f} -> {'PASS' if k2ok else 'FAIL'}")
Y = np.logspace(-1, 1, 41); prof = {}
for a in (0.1, 0.3, 1.0, 3.0):
    gN, nu, rho, dl, f = profile(R ** 2 / (R + a) ** 2)
    ok = (rho > 0)
    # y decreases outward for these profiles beyond the peak; use the outer branch (beyond the g_N maximum)
    ipk = int(np.argmax(gN)); yy, ff = gN[ipk:][ok[ipk:]], f[ipk:][ok[ipk:]]
    o = np.argsort(yy); fy = np.interp(np.log(Y), np.log(yy[o]), ff[o], left=np.nan, right=np.nan)
    prof[a] = fy
    P(f"a = {a:3.1f}: f/a0 at y = 0.1, 1, 10: {fy[0]:+.4f}, {fy[20]:+.4f}, {fy[40]:+.4f}; outward fraction over y in [0.1,10] {np.nanmean(fy > 0):.2f}")
F = np.array([prof[a] for a in prof])
med = np.nanmedian(np.abs(F), axis=0)
S = np.nanmax(np.abs(np.log10(np.abs(F) / med)), axis=0)
sgn_ok = np.all((np.sign(F) == np.sign(F[0])) | np.isnan(F), axis=0)
Smax = float(np.nanmax(S)); flip = bool(not sgn_ok.all())
v = "LOCAL" if (Smax <= 0.04 and not flip) else "NONLOCAL" if (Smax > 0.15 or flip) else "WEAKLY LOCAL"
P(f"locality spread max over y in [0.1,10]: {Smax:.3f} dex; sign flip across compactness: {flip} -> {v}")
for i in (0, 10, 20, 30, 40): P(f"   y = {Y[i]:6.3f}: f/a0 by a = " + ", ".join(f"{prof[a][i]:+.4f}" for a in prof) + f"  spread {S[i]:.3f} dex")
json.dump(dict(K1=k1, K2=k2, Smax=Smax, flip=flip, verdict=v, Y=Y.tolist(), f={str(a): prof[a].tolist() for a in prof}), open(os.path.join(HERE, f"cfg473_locality{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg473_locality{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if not k1ok else 0)
sys.exit(0 if (k1ok and k2ok) else 1)
