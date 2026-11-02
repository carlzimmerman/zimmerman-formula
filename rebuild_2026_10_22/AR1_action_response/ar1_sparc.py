#!/usr/bin/env python3
"""AR1 SPARC and LITTLE THINGS rows (FROZEN_CRITERIA.md), own driver on UL1's engine, read only. Response at 17 U nodes, interpolated in ln(M_f/M0) at each R. Each galaxy checkpoints; SIGTERM exits 75, rerun resumes. Prints no graded number.
    ar1_sparc.py ROW [ROW...]   ROW = shape_mode_mb[_mut2][_t2], shape hand|nat, mode act|blum, mb v2r|inv|exp. kappa = 1/2 FITTED, unused; not theory closed."""
import math, os, pickle, signal, sys
sys.dont_write_bytecode = True
_a = sys.argv; sys.argv = [_a[0]]
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path[:0] = [HERE, os.path.join(RB, "UL1_measured_upsilon_test"), os.path.join(RB, "DR3_thin_disc_monopole")]; import ul1_core as C, ar1_solver as A
from scipy.optimize import brentq
sys.argv = _a; CD = os.path.join(HERE, "cache_rows"); RW = os.path.join(HERE, "rows"); os.makedirs(CD, exist_ok=True); os.makedirs(RW, exist_ok=True); UPS = C.UPS; GE, MSUNE, KPC = C.GE, C.MSUNE, C.KPC; TG = C.TG
_iu = sorted(set([int(np.argmin(abs(UPS - u))) for u in np.geomspace(0.06, 2.40, 17)] + [int(np.argmin(abs(UPS - 0.5)))])); IU = np.array(_iu); LU = np.log(UPS)
SPD = os.path.join(RB, "..", "real_research", "data", "sparc_data"); STOP = [False]; signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__(0, True))
def mexp(R_kpc, M, h): x = R_kpc / h; return M * (1 - (1 + x) * np.exp(-x))
class Mono:
    """DR3's true monopole, text of dr3_tail_add.py in function form: SPARC's SB, bulge 1.4 U Vbul^2 r/G, gas exp or DR3's inversion."""
    def __init__(s, G):
        s.SB = {}; s.GR = {}; s.GI = {}; f = os.path.join(CD, "gasinv.pkl")
        for q in G:
            d = np.genfromtxt(os.path.join(SPD, q["name"] + "_rotmod.dat"), comments="#"); Rk = d[:, 0]; sb = np.maximum(d[:, 6], 0.0); i = np.empty_like(Rk); i[0] = 0.5 * sb[0] * Rk[0] ** 2; i[1:] = 0.5 * (sb[1:] * Rk[1:] + sb[:-1] * Rk[:-1]) * np.diff(Rk); s.SB[q["name"]] = 2 * math.pi * 1e6 * np.cumsum(i); mh = q["meta"]["MHI"] * 1e9; rh = q["meta"]["RHI"]
            if mh <= 0 or rh <= 0: s.GR[q["name"]] = None; continue
            w = 2 * math.pi * rh ** 2 * 1e6 / mh; x = 2.0 if w >= 4 * math.exp(-2) else brentq(lambda x: x * x * math.exp(-x) - w, 2.0, 200.0); s.GR[q["name"]] = rh / x
        if os.path.exists(f): s.GI = pickle.load(open(f, "rb"))
        else:
            from dr3_gasinv import invert
            for q in G: Rk = q["R"]; s.GI[q["name"]] = invert(Rk, np.sign(q["Vgas"]) * q["Vgas"] ** 2, 1.33 * q["meta"]["MHI"] * 1e9)[0]
            pickle.dump(s.GI, open(f + ".tmp", "wb")); os.replace(f + ".tmp", f)
    def Mbk(s, q, iu, kind):
        R_ = q["Rm"]; U = float(UPS[iu])
        if kind == "v2r": return np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R_ ** 2 / GE, 0.0))
        n = q["name"]; Rk = R_ / KPC; Mb = U * s.SB[n] * MSUNE + 1.4 * U * (q["Vbul"] * 1e3) ** 2 * R_ / GE
        if kind == "inv": Mb = Mb + s.GI[n] * MSUNE
        elif s.GR[n] is not None: Mb = Mb + mexp(Rk, 1.33 * q["meta"]["MHI"] * 1e9, s.GR[n]) * MSUNE
        else: Mb = Mb + np.sign(q["Vgas"]) * (q["Vgas"] * 1e3) ** 2 * R_ / GE
        return np.maximum.accumulate(np.maximum(Mb, 0.0))
def baryon(q, iu, rg, kind, M, mb=1.0):
    R_ = q["Rm"]; U = float(UPS[iu]); Mbk = M.Mbk(q, iu, kind); Mt = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE); Mbg = np.where(rg < R_[0], Mbk[0] * (rg / R_[0]) ** 2, np.interp(np.log(rg), np.log(R_), Mbk)); o = rg > R_[-1]
    if o.any(): t = np.clip(np.log(rg[o] / R_[-1]) / math.log(3.0), 0, 1); Mbg[o] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t) + np.log(Mt) * t)
    return mb * np.maximum.accumulate(Mbg), mb * Mt
def setup(q, t, shape):
    bg = C.BG[t]; rc = C.rc_of(t); lMb = q["lMb"]; R_ = q["Rm"]; M2 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MSUNE; R2 = (3 * M2 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    if shape == "hand": s = C.Sfn(bg["a"] + bg["b"] * (lMb - 10), t); r0 = C.r0_of(M2, R2, s); rg = np.geomspace(R_[0] * 0.05, R2, 300); return M2, R2, rg, math.pi * s * r0 ** 2 * C.Bs(rg / r0), M2, r0
    rg = np.geomspace(R_[0] * 0.05, R2 * 1.2, 300); M0 = C.natmass(M2, rc, rg, "tot"); return M2, R2, rg, M0, float(M0[-1]), None
def response(q, t, shape, mode, kind, M, mb=1.0, rdec=0.1, nodes=IU, STATS=None):
    """ln(M_f/M0) at q's radii at each node."""
    M2, R2, rg, M0, Mref, _ = setup(q, t, shape); st = A.Start(rg, M0, rdec, thin=(0.35 if shape != "hand" else None)) if mode == "act" else None; O = np.zeros((len(q["Rm"]), len(nodes))); lg = np.log(rg); lr = np.log(q["Rm"]); m0r = np.maximum(np.interp(lr, lg, M0), 1e-300)
    for k, iu in enumerate(nodes):
        Mbg, Mt = baryon(q, iu, rg, kind, M, mb); F = Mt / Mref
        Mf = A.act_contract(rg, Mbg, M0, F, st=st, stats=STATS, rdec=rdec)[0] if mode == "act" else C.contract(rg, Mbg, M0, F)[0]
        O[:, k] = np.log(np.maximum(np.interp(lr, lg, Mf), 1e-300) / m0r)
    return O, m0r
def gh_from(O, m0r, q, nodes=IU):
    """Interpolate in ln U onto the whole grid; g_halo(R, U)."""
    x = LU[nodes]; gh = np.empty((len(q["Rm"]), len(UPS)))
    for i in range(len(q["Rm"])): gh[i] = np.interp(LU, x, O[i])
    return GE * m0r[:, None] * np.exp(gh) / q["Rm"][:, None] ** 2
def parse(n):
    p = n.split("_"); return dict(shape=p[0], mode=p[1], kind=p[2], mb=2.0 if "mut2" in p else 1.0, rdec=0.2 if "t2" in p else 0.1)
def lt(t, c):
    C.contract = (lambda r, Mb, M0, F, gnedin=None: A.act_contract(r, Mb, M0, F, rdec=c["rdec"], st=A.Start(r, M0, c["rdec"], thin=(0.35 if c["shape"] != "hand" else None)))) if c["mode"] == "act" else _CX
    v = C.lt_row(t, "hand" if c["shape"] == "hand" else "tot", "f", 1.0); C.contract = _CX; return v
_CX = C.contract
def run(name, G, M):
    o = os.path.join(RW, name + ".npz")
    if os.path.exists(o): return
    c = parse(name); R = {}; Sall = {}
    for t in TG:
        ck = os.path.join(CD, f"{name}_{t}.pkl"); D = pickle.load(open(ck, "rb")) if os.path.exists(ck) else dict(rows={}, lt=None, stats={})
        for j, q in enumerate(G):
            if q["name"] in D["rows"]: continue
            Oq, m0 = response(q, t, c["shape"], c["mode"], c["kind"], M, c["mb"], c["rdec"], STATS=D["stats"]); D["rows"][q["name"]] = C.mse_of(q, np.log10(np.maximum(q["GB"] + gh_from(Oq, m0, q), 1e-300)))
            if STOP[0] or j % 10 == 0:
                pickle.dump(D, open(ck + ".tmp", "wb")); os.replace(ck + ".tmp", ck)
                if STOP[0]: print("signal: checkpoint", name, t, j, flush=True); sys.exit(75)
        if D["lt"] is None and c["mb"] == 1.0: D["lt"] = lt(t, c)
        pickle.dump(D, open(ck + ".tmp", "wb")); os.replace(ck + ".tmp", ck); R[t] = D; print(name, t, "done", flush=True)
    np.savez_compressed(o, **{f"{t}_wr2": np.array([R[t]["rows"][q["name"]][0] for q in G]) for t in TG}, **{f"{t}_ws": np.array([R[t]["rows"][q["name"]][1] for q in G]) for t in TG}, lt=np.array([R[t]["lt"] if R[t]["lt"] is not None else np.nan for t in TG]), stats=np.array(repr({t: R[t]["stats"] for t in TG})))
if __name__ == "__main__":
    G = C.load(); M = Mono(G); print("loaded", len(G), flush=True)
    for n in sys.argv[1:]: run(n, G, M)
