#!/usr/bin/env python3
"""UL1 core, own code: per-galaxy best U on a wide grid for each row. EM1's data and fit, X39's contract, SP3's S table of NR2 medians, ZN2's z = 0 shapes. Reads only; each row caches, so a run resumes.
    ul1_core.py ROW [ROW...]   kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, pickle, re, sys
import numpy as np
from scipy.optimize import brentq, minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RT = os.path.dirname(RB); CD = os.path.join(HERE, "cache_rows"); os.makedirs(CD, exist_ok=True); RWD = os.path.join(HERE, "rows"); os.makedirs(RWD, exist_ok=True)
GE, MSUNE, MPCE = 6.67430e-11, 1.98847e30, 3.0857e22; KPC = MPCE / 1e3
UPS = np.round(np.arange(0.06, 2.4001, 0.01), 2); IREC = np.where((UPS >= 0.2999) & (UPS <= 1.2001))[0]; TG = ("A_c2b_refit", "B_cfg886_bg"); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
SGN = 1.0; _x = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(compile(_x[_x.index("def contract(r, Mb, M0, F, gnedin=None):"):_x.index('P("\\n=== checks")')], "x39", "exec"))
def load():
    d_ = os.path.join(RT, "real_research", "data", "sparc_data"); gal = []; keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q"); tab = {}
    for line in open(os.path.join(RT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
        t = line.split()
        if len(t) != 19: continue
        try: tab[t[0]] = dict(zip(keys, [float(a) for a in t[1:18]]))
        except ValueError: continue
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"): continue
        try: d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        q = dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]); q["meta"] = tab[q["name"]]; R = q["R"] * 3.0857e19
        VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2; GB = VB2 * 1e6 / R[:, None]; GO = (q["Vobs"] * 1e3) ** 2 / R
        OK = (GB > 0) & (GO > 0)[:, None] & np.isfinite(GB) & (q["Vobs"] > 0)[:, None]
        q.update(Rm=R, GB=GB, GO=GO, OK=OK, W=1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2, lMb=math.log10((0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9)); gal.append(q)
    return gal
def mse_of(q, lgp, GO=None):
    go = q["GO"] if GO is None else GO; OK = q["OK"] if GO is None else q["OK"] & (GO > 0)[:, None]; r = np.where(OK, np.log10(np.where(go > 0, go, 1.0))[:, None] - lgp, 0.0); Wm = np.where(OK, q["W"][:, None], 0.0); return (Wm * r * r).sum(0), Wm.sum(0)
ST = json.load(open(os.path.join(HERE, "ul1_S_table.json"))); BG = ST["bg"]
Z = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); ZX = np.log(np.array(Z["x"])); ZT = sorted(((float(Z[m]["0.00"]["lgM"]), np.array(Z[m]["0.00"]["lnm"])) for m in ("1e10", "1e11", "1e12", "1e13", "1e14")), key=lambda a: a[0]); RN = json.load(open(os.path.join(RB, "RET1_retention_replaces_em1", "ret1_results.json")))["RNAT"]; FC = RN / (1 + RN)
def Bs(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def rc_of(t): h = BG[t]["h"]; return 3 * (100 * h * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
def Sfn(lM, t):
    x, y = ST["lgM"], np.log10(ST["S"][t])  # below the table's 1e9: linear extrapolation in log (LITTLE THINGS; K4 tests it)
    v = float(np.interp(lM, x, y)) if lM >= x[0] else float(y[0] + (y[2] - y[0]) / (x[2] - x[0]) * (lM - x[0])); return 10 ** v * MSUNE / KPC ** 2
def r0_of(M, R, S):
    lm = lambda l: math.log(math.pi * S * math.exp(2 * l) * float(Bs(R / math.exp(l)))); pk = minimize_scalar(lambda l: -lm(l), bounds=(math.log(R * 1e-6), math.log(R * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(pk.x) < math.log(M): return math.exp(pk.x)
    return math.exp(brentq(lambda l: lm(l) - math.log(M), math.log(R * 1e-7), pk.x, xtol=1e-14))
def lnm(lg):
    if lg <= ZT[0][0]: return ZT[0][1]
    if lg >= ZT[-1][0]: return ZT[-1][1]
    k = next(i for i in range(len(ZT) - 1) if ZT[i][0] <= lg <= ZT[i + 1][0]); w = (lg - ZT[k][0]) / (ZT[k + 1][0] - ZT[k][0]); return (1 - w) * ZT[k][1] + w * ZT[k + 1][1]
def natmass(Mc, rc, r, mp):
    Mt = Mc / FC; ln = lnm(math.log10(Mt / MSUNE)); M_, R_ = (FC * Mt, (3 * Mt / (4 * math.pi * 200 * rc)) ** (1 / 3)) if mp == "tot" else (Mc, (3 * Mc / (4 * math.pi * 200 * rc)) ** (1 / 3)); lx = np.log(np.maximum(np.minimum(np.asarray(r, float), R_) / R_, 1e-300)); return M_ * np.exp(np.where(lx >= ZX[0], np.interp(lx, ZX, ln), ln[0] + 2 * (lx - ZX[0])))
def baryon(q, iu, rg, mb=1.0, U=None):
    R_ = q["Rm"]; U = UPS[iu]; Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0)); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < R_[0], Mbk[0] * (rg / R_[0]) ** 2, np.interp(np.log(rg), np.log(R_), Mbk)); o = rg > R_[-1]
    if o.any(): t = np.clip(np.log(rg[o] / R_[-1]) / math.log(3.0), 0, 1); Mbg[o] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t) + np.log(Mt) * t)
    return mb * np.maximum.accumulate(Mbg), mb * Mt
def gh_table(q, t, shape, mode, fq=1.0, mb=1.0, self_mb=False):
    """g_halo(R, U), m/s^2. shape hand|tot|fc1. mode off|f|gnedin. self_mb: EM1's line and the halo at each trial U's M_b."""
    bg = BG[t]; rc = rc_of(t); R_ = q["Rm"]; gh = np.zeros((len(R_), len(UPS)))
    def setup(lMb):
        M2 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MSUNE; R2 = (3 * M2 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        if shape == "hand":
            s = Sfn(bg["a"] + bg["b"] * (lMb - 10), t); r0 = r0_of(M2, R2, s); rg = np.geomspace(R_[0] * 0.05, R2, 300); return M2, R2, rg, math.pi * s * r0 ** 2 * Bs(rg / r0), (lambda r: math.pi * s * r0 ** 2 * Bs(np.minimum(r, R2) / r0))
        rg = np.geomspace(R_[0] * 0.05, R2 * 1.2, 300); return M2, R2, rg, natmass(M2, rc, rg, shape), (lambda r: natmass(M2, rc, r, shape))
    if not self_mb: M2, R2, rg, M0, F0 = setup(q["lMb"])
    if mode == "off" and not self_mb: return np.broadcast_to((GE * F0(R_) / R_ ** 2)[:, None], gh.shape).copy()
    for iu, U in enumerate(UPS):
        if self_mb: M2, R2, rg, M0, F0 = setup(math.log10((U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9))
        if mode == "off": gh[:, iu] = GE * F0(R_) / R_ ** 2; continue
        Mbg, Mt = baryon(q, iu, rg, mb); Mf = contract(rg, Mbg, M0, Mt / (M2 if shape == "hand" else float(M0[-1])), gnedin=(0.85, 0.8, R2) if mode == "gnedin" else None)[0]; gh[:, iu] = GE * np.interp(np.log(R_), np.log(rg), M0 + fq * (Mf - M0)) / R_ ** 2
    return gh
LTR = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["lt"]
def lt_row(t, shape, mode, fq, self_mb=False):
    bg = BG[t]; rc = rc_of(t); E = []
    for r in LTR:
        lMb = r["logMb"]; M2 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MSUNE; R2 = (3 * M2 / (4 * math.pi * 200 * rc)) ** (1 / 3); R_ = r["R"] * KPC; Mb = 10 ** lMb * MSUNE
        if shape == "hand": s = Sfn(bg["a"] + bg["b"] * (lMb - 10), t); r0 = r0_of(M2, R2, s); rg = np.geomspace(R_ * 1e-3, R2, 600); M0 = math.pi * s * r0 ** 2 * Bs(rg / r0); F = Mb / M2
        else: rg = np.geomspace(R_ * 1e-3, max(R2 * 1.2, R_ * 2), 600); M0 = natmass(M2, rc, rg, shape); F = Mb / float(M0[-1])
        Mbg = Mb * np.minimum(rg / R_, 1.0) ** 2
        if mode == "off": Mc = M0
        else: Mf = contract(rg, Mbg, M0, F, gnedin=(0.85, 0.8, rg[-1]) if mode == "gnedin" else None)[0]; Mc = M0 + fq * (Mf - M0)
        E.append(math.log10((r["V"] * 1e3) ** 2 / R_) - math.log10(GE * Mb / R_ ** 2 + GE * float(np.interp(math.log(R_), np.log(rg), Mc)) / R_ ** 2))
    return float(np.median(E))
ROWS = {"hand_off": ("hand", "off", 1), "hand_fq": ("hand", "f", .872), "hand_blum": ("hand", "f", 1), "hand_gnedin": ("hand", "gnedin", 1), "nat_off": ("tot", "off", 1), "nat_fq": ("tot", "f", .872), "nat_blum": ("tot", "f", 1), "nat_gnedin": ("tot", "gnedin", 1), "fc1_off": ("fc1", "off", 1), "fc1_fq": ("fc1", "f", .872)}
def run_row(name, GALS):
    o = os.path.join(RWD, name + ".npz")
    if os.path.exists(o): return
    res = {}
    for t in TG:
        ck = os.path.join(CD, f"{name}_{t}.pkl")
        if os.path.exists(ck): res[t] = pickle.load(open(ck, "rb")); continue
        if name.startswith("law_"):
            a0 = A0[name[4:]]; rows = [mse_of(q, np.log10(np.maximum((0.5 + np.sqrt(0.25 + a0 / np.maximum(q["GB"], 1e-300))) * q["GB"], 1e-300))) for q in GALS]; lt = None
        else:
            selfm = name.endswith("_self"); base = name[:-5] if selfm else name; mb = 1.0
            if base.endswith("_mb2"): base = base[:-4]; mb = 2.0
            sh, mo, fq = ROWS[base]; rows = []
            for q in GALS:
                gh = gh_table(q, t, sh, mo, fq, mb, selfm); rows.append(mse_of(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))))
                if base == "nat_fq" and not selfm and mb == 1.0: pickle.dump(gh.astype(np.float32), open(os.path.join(CD, f"gh_{t}_{q['name']}.pkl"), "wb"))
            lt = lt_row(t, sh, mo, fq)
        res[t] = dict(wr2=np.array([a for a, b in rows]), ws=np.array([b for a, b in rows]), lt=lt); pickle.dump(res[t], open(ck, "wb")); print(name, t, "done", flush=True)
    np.savez_compressed(o, **{f"{t}_wr2": res[t]["wr2"].astype(np.float64) for t in TG}, **{f"{t}_ws": res[t]["ws"] for t in TG}, lt=np.array([res[t]["lt"] if res[t]["lt"] is not None else np.nan for t in TG]))
if __name__ == "__main__":
    G = load(); print(len(G), flush=True)
    for n in sys.argv[1:]: run_row(n, G)
