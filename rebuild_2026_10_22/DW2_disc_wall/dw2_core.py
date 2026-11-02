#!/usr/bin/env python3
"""DW2 shared core: MC1's model (X39 contraction, ZN2 shape, EM1/share). Read-only on other lanes. kappa = 1/2 FITTED; cold dark energy, never a particle; not theory closed."""
import json, math, os, glob, csv
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = bool(os.environ.get("DW2_MUTATE")); TAG = "_MUTATE" if MUT else ""
A0 = dict(canonical=9.3603e-11 * (1.5 if MUT else 1), alt=1.1312e-10 * (1.5 if MUT else 1)); FEET = ("canonical", "alt"); SHARE = 5.35 * (0.5 if MUT else 1)
G, MS, PC, CK = 6.674e-11, 1.989e30, 3.0857e16, 299792.458; KPC = PC * 1e3; MPC = PC * 1e6; KMS2 = 1e6; H = 0.672
RHOC = 3 * (100e3 * H / MPC) ** 2 / (8 * math.pi * G); MSPC3 = MS / PC ** 3
BINS = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]; BN = [f"{a}-{b}" for a, b in BINS]; FQ = 0.872
INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs"); FC = 5.35 / 6.35
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def lawinv(g, a): return g * g / (g + a)
SJ = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); LX = np.log(np.array(SJ["x"]))
TAGS = sorted(((float(SJ[m]["0.00"]["lgM"]), np.array(SJ[m]["0.00"]["lnm"])) for m in ("1e10", "1e11", "1e12", "1e13", "1e14")), key=lambda t: t[0])
def lnm(lg):
    if lg <= TAGS[0][0]: return TAGS[0][1]
    if lg >= TAGS[-1][0]: return TAGS[-1][1]
    k = next(i for i in range(len(TAGS) - 1) if TAGS[i][0] <= lg <= TAGS[i + 1][0]); w = (lg - TAGS[k][0]) / (TAGS[k + 1][0] - TAGS[k][0]); return (1 - w) * TAGS[k][1] + w * TAGS[k + 1][1]
def r200(M200): return (3 * M200 * MS / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
def Mc_native(M200, r, s=1.0):
    """Stretch s: M(<r) = native(r/s) renormalised to keep M(<R200)."""
    R = r200(M200); ln_ = lnm(math.log10(M200)); rr = np.minimum(np.asarray(r, float), R)
    def sh(q):
        lx = np.log(np.maximum(q / R, 1e-300)); return np.exp(np.where(lx >= LX[0], np.interp(lx, LX, ln_), ln_[0] + 2 * (lx - LX[0])))
    if s == 1.0: return FC * M200 * sh(rr)
    return FC * M200 * sh(rr / s) * sh(np.array(R)) / sh(np.array(R / s))
_x = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); SGN = 1; exec(_x[_x.index("def contract(r, Mb, M0, F, gnedin=None):"):_x.index('P("\\n=== checks")')])
def contract_fast(r, Mb, M0, F, n=40):
    lr = np.log(r); rf = r.copy(); Mi = M0
    for _ in range(n): rf = 0.5 * rf + 0.5 * r * Mi * (1 + F) / np.maximum(np.interp(np.log(np.maximum(rf, r[0])), lr, Mb) + Mi, 1e-300)
    o = np.maximum.accumulate(rf); return np.interp(lr, np.log(o), M0, left=0.0, right=M0[-1])
def em1(lMb, a=11.18): return 10 ** (a + 0.9 * (lMb - 10))
def share200(Mb): return (1 + SHARE) * Mb
def load(all175=False):
    T = {}
    for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) == 19:
            try: T[t[0]] = dict(Inc=float(t[5]), L36=float(t[7]), SB=float(t[10]), Rd=float(t[11]), MHI=float(t[13]), Vflat=float(t[15]), Q=float(t[17]))
            except ValueError: pass
    out = []
    for f_ in sorted(glob.glob(os.path.join(INP, "sparc", "rotmod", "*_rotmod.dat"))):
        n = os.path.basename(f_).replace("_rotmod.dat", ""); a = np.loadtxt(f_, comments="#", ndmin=2); m = T[n]
        if not all175 and (m["Q"] > 2 or m["Inc"] < 30 or len(a) < 3): continue
        g = dict(name=n, R=a[:, 0] * KPC, V=a[:, 1], eV=a[:, 2], Vg=a[:, 3], Vd=a[:, 4], Vb=a[:, 5], **m)
        g["fb"] = float(a[-1, 5] ** 2 / max(a[-1, 4] ** 2 + a[-1, 5] ** 2, 1e-9)); g["TOT"] = 1 + 0.4 * g["fb"]; out.append(g)
    return out
def scaled(g, D=1.0, gas=1.0):
    if D == 1.0 and gas == 1.0: return g
    q = dict(g); q["R"] = g["R"] * D; q["Vg"] = g["Vg"] * math.sqrt(D * gas); q["Vd"] = g["Vd"] * math.sqrt(D); q["Vb"] = g["Vb"] * math.sqrt(D); q["L36"] = g["L36"] * D * D; q["MHI"] = g["MHI"] * D * D * gas; return q
def gbar(g, U): return (np.abs(g["Vg"]) * g["Vg"] + U * np.abs(g["Vd"]) * g["Vd"] + 1.4 * U * np.abs(g["Vb"]) * g["Vb"]) * KMS2 / g["R"]
def Mbtot(g, U): return (U * g["L36"] + 1.33 * g["MHI"]) * 1e9
def M200_of(g, mass, a=11.18): return em1(math.log10(Mbtot(g, 0.5)), a) if mass == "em1" else share200(Mbtot(g, 0.5))
def cold_pair(g, U, mass, s=1.0, a=11.18, fast=False, mbfun=None):
    """Returns Newtonian g_c at f 0 and at f 1 on g's radii."""
    R = g["R"]; Mb = Mbtot(g, U); M200 = M200_of(g, mass, a); Rv = r200(M200)
    n = 120 if fast else 300; rg = np.geomspace(R[0] * 0.05, Rv * 1.2, n); M0 = Mc_native(M200, rg, s); Mbk = np.maximum.accumulate(np.maximum(gbar(g, U) * R ** 2 / G / MS, 0)); Mt = max(Mbk[-1], Mb)
    Mg = np.where(rg < R[0], Mbk[0] * (rg / R[0]) ** 2, np.interp(np.log(rg), np.log(R), Mbk)); o = rg > R[-1]; t = np.clip(np.log(rg[o] / R[-1]) / math.log(3), 0, 1); Mg[o] = np.exp(np.log(max(Mbk[-1], 1e-30)) * (1 - t) + np.log(Mt) * t); Mg = np.maximum.accumulate(Mg)
    F = Mt / float(M0[-1])
    if mbfun is not None: Mg, F = mbfun(rg, Mg, M0, F)
    Mf = contract_fast(rg, Mg, M0, F) if fast else contract(rg, Mg, M0, F)[0]
    lr, lg = np.log(R), np.log(rg); return G * np.interp(lr, lg, M0) * MS / R ** 2, G * np.interp(lr, lg, Mf) * MS / R ** 2
def outer(g): return (g["R"] >= g["R"].max() * 2 / 3) & (g["V"] > 0)
def binof(g):
    for i, (a, b) in enumerate(BINS):
        if a <= g["Vflat"] < b: return i
    return -1
def boot_med(v, seed=20261102, nb=2000):
    v = np.asarray(v); r = np.random.default_rng(seed); i = r.integers(0, len(v), (nb, len(v))); return float(np.median(v)), float(np.median(v[i], axis=1).std())
def dgal(gO, gb, gc, a0, rd, psi):
    return float(np.mean(np.log10(gO / (law(gb, a0) + psi * gc if rd == "N" else law(gb + psi * gc, a0)))))
def psi_bin(items, a0, rd, sigma=None):
    """items: list of (gO, gb, gc) on outer points. Returns psi, capped flag, floor, d0, sigma, d at psi 1."""
    D0 = [dgal(a, b, c, a0, rd, 0.0) for a, b, c in items]
    d0, s = boot_med(D0) if sigma is None else (float(np.median(D0)), sigma); fl = min(d0, 0.0) - 2 * s
    f = lambda p: float(np.median([dgal(a, b, c, a0, rd, p) for a, b, c in items])); d1 = f(1.0)
    if d1 >= fl: return dict(psi=1.0, capped=True, floor=fl, d0=d0, s=s, d1=d1)
    lo, hi = 0.0, 1.0
    for _ in range(14):
        c = 0.5 * (lo + hi); lo, hi = (c, hi) if f(c) >= fl else (lo, c)
    return dict(psi=lo, capped=False, floor=fl, d0=d0, s=s, d1=d1)
def item(g, U, gc0, gc1, f):
    gO = g["V"] ** 2 * KMS2 / g["R"]; gb = np.maximum(gbar(g, U), 1e-20); gc = gc0 + f * (gc1 - gc0); m = outer(g); return gO[m], gb[m], gc[m]
