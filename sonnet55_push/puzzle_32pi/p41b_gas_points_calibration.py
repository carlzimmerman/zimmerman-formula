"""p41b (after p41's pre-written checks FAILED: galaxy-level 'gas-dominated' samples are Upsilon-sensitive, 63% spread): calibrate on POINTS where gas
supplies > fcut of the baryonic pull (at Upsilon 0.5), which should be Upsilon-independent. Then Upsilon* from star-dominated POINTS (gas < 0.2), and a0 for all points at
Upsilon* with a galaxy bootstrap. SPARC MLS16 cuts, sigma_int 0.11, framework kernel (RAR as systematic). fcut = 0.8 (primary), 0.7 / 0.9 reported.
Run: python3 p41b_gas_points_calibration.py [NBOOT]  |  MUTATE=1: fcut = 0.0 (all points: the calibrator becomes Upsilon-sensitive, check G must fail)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 60
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
def sub(g, m):
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h
def split(fcut, lowcut=0.2):
    G_, S_ = [], []
    for g in gals:
        vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
        fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
        mg, ms = fg > fcut, fg < lowcut
        if mg.sum() >= 2: G_.append(sub(g, mg))
        if ms.sum() >= 2: S_.append(sub(g, ms))
    return G_, S_
A = np.exp(np.linspace(math.log(0.4e-10), math.log(2.6e-10), 61))
UG = np.round(np.arange(0.35, 0.951, 0.025), 3)
fit = lambda sel, IF, u: V.parabola_min(A, V.Profile(sel, IF, ufixed=u).scan(A, 0.11), k=6)[0]
def ustar(G_, S_, IF):
    aG = fit(G_, IF, 0.5)                                   # the calibrator (checked Upsilon-insensitive)
    d = np.array([math.log(fit(S_, IF, u) / aG) for u in UG])
    if not (d.min() < 0 < d.max()): return float("nan"), aG
    i = int(np.where(np.diff(np.sign(d)) != 0)[0][0])
    return float(UG[i] - d[i] * (UG[i + 1] - UG[i]) / (d[i + 1] - d[i])), aG
FC = 0.0 if MUTATE else 0.8
for fc in ((FC,) if MUTATE else (0.7, 0.8, 0.9)):
    G_, S_ = split(fc)
    sens = [fit(G_, V.IF_alpha1, u) for u in (0.3, 0.5, 0.7)]
    print(f"   fcut {fc}: gas points from {len(G_)} galaxies ({sum(len(g['Rm']) for g in G_)} pts); a0_gas at Upsilon 0.3/0.5/0.7 = "
          f"{sens[0]:.3e}/{sens[1]:.3e}/{sens[2]:.3e} (spread {100*(max(sens)/min(sens)-1):.1f}%)")
    if fc == FC: sensP, GP, SP = sens, G_, S_
check(f"G the gas-point calibrator is Upsilon-insensitive (spread {100*(max(sensP)/min(sensP)-1):.1f}% < 10% over Upsilon 0.3-0.7)", max(sensP) / min(sensP) < 1.10)
out = {}
for nm, IF in (("framework", V.IF_alpha1), ("RAR", V.IF_rar)):
    us, aG = ustar(GP, SP, IF)
    aall = fit(gals, IF, us) if np.isfinite(us) else float("nan")
    rng = np.random.default_rng(411); B = []
    nb = NB if nm == "framework" else max(NB // 3, 10)
    idxG = {id(g): i for i, g in enumerate(GP)}
    for _ in range(nb):
        Gb = [GP[i] for i in rng.integers(0, len(GP), len(GP))]; Sb = [SP[i] for i in rng.integers(0, len(SP), len(SP))]
        ub, aGb = ustar(Gb, Sb, IF)
        if np.isfinite(ub): B.append((ub, aGb))
    B = np.array(B)
    out[nm] = (us, aG, aall, B)
    print(f"   {nm:9s}: gas-point a0 (Upsilon-free) = {aG:.3e} (68% {np.percentile(B[:,1],16):.3e}-{np.percentile(B[:,1],84):.3e}); "
          f"Upsilon* = {us:.3f} (68% {np.percentile(B[:,0],16):.3f}-{np.percentile(B[:,0],84):.3f}); a0(all, Upsilon*) = {aall:.3e}")
us, aG, aall, B = out["framework"]
pe = (np.percentile(B[:, 1], 84) - np.percentile(B[:, 1], 16)) / 2 / aG
print(f"   framework gas-point a0 = {aG:.3e} +- {100*pe:.1f}% (stat);  vs 9.360e-11 {100*(aG/9.3603e-11-1):+.1f}%, vs 1.131e-10 {100*(aG/1.1312e-10-1):+.1f}%, vs 1.061e-10 {100*(aG/1.061e-10-1):+.1f}%;"
      f"  kernel systematic (RAR) {100*abs(out['RAR'][1]/aG-1):.1f}%")
check(f"U the calibrated Upsilon* = {us:.3f} lies inside the 3.6 um population prior (0.40-0.63)", 0.40 <= us <= 0.63)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
