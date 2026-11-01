#!/usr/bin/env python3
"""SL1_symbolic_law_search (FROZEN_CRITERIA.md): closed-form operators A (core radius) and B (radial cold response) with no fitted float, on NR1 PRIMARY's baseline, from cache/sl1_cache.pkl (sl1_harvest.py).
    python3 -I discover_law.py --checks                 # K1-K3, K5-K7, MUTATE, speed
    python3 -I discover_law.py --planted                # K8
    python3 -I discover_law.py --ga SPEC|NATIVE SEED    # population 250, 200 generations; resumes; SIGTERM checkpoints
    python3 -I discover_law.py --sweep SPEC|NATIVE      # bounded enumeration, then best A x best B
    python3 -I discover_law.py --report
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; not theory closed."""
import hashlib, itertools, json, math, os, pickle, random, signal, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.environ["SL1_HERE"]; RB = os.path.dirname(HERE); CACHE = os.path.join(HERE, "cache", "sl1_cache.pkl")
TA, TB = "A_c2b_refit", "B_cfg886_bg"; TAGS = (TA, TB); HKS = ("h0672", "h0686"); BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400))
ET1_CI = ((52, 85), (81, 124), (118, 200), (98, 190), (137, 272), (182, 596)); KEYS = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]
CL = 2.99792458e8; ERG = 1e-7; POP, GENS, LAM = 250, 200, 0.02; MAXN, MAXD = 11, 4; SPLIT_SEED = 20261101
# ------------------------------------------------------------------ genome
CONST = {"k": 0.5, "fb": 0.15945, "Rn": 5.271, "1": 1.0, "2": 2.0, "pi": math.pi, "0": 0.0}
LEAF_A = ["q", "v", "z", "eta", "cf"]; LEAF_B = {"SPEC": ["xb", "xc", "fl", "q"], "NATIVE": ["fl", "q"]}; CONS = {"SPEC": ["k", "fb", "Rn", "1", "2", "pi"], "NATIVE": ["fb", "Rn", "1", "2", "pi"]}
BIN = ("add", "sub", "mul", "div"); UN = ("sqrt", "log1p", "inv1p")
def leaves(kind, gram): return (LEAF_A if kind == "A" else LEAF_B[gram]) + CONS[gram]
def to_s(t):
    if isinstance(t, str): return t
    return f"{t[0]}({','.join(to_s(c) for c in t[1:])})"
def size(t): return 1 if isinstance(t, str) else 1 + sum(size(c) for c in t[1:])
def depth(t): return 0 if isinstance(t, str) else 1 + max(depth(c) for c in t[1:])
def simplify(t):
    if isinstance(t, str): return t
    c = [simplify(x) for x in t[1:]]; o = t[0]
    if o in UN:
        if c[0] == "0": return "0" if o != "inv1p" else "1"
        return (o, c[0])
    a, b = c; sa, sb = to_s(a), to_s(b)
    if o in ("add", "mul") and sb < sa: a, b, sa, sb = b, a, sb, sa
    if o == "add":
        if a == "0": return b
    if o == "sub":
        if sa == sb: return "0"
        if b == "0": return a
    if o == "mul":
        if a == "0": return "0"
        if a == "1": return b
    if o == "div":
        if sa == sb: return "1"
        if b == "1": return a
        if a == "0": return "0"
    return (o, a, b)
def src(t):
    if isinstance(t, str): return repr(CONST[t]) if t in CONST else f"V[{t!r}]"
    if t[0] in UN: return {"sqrt": f"np.sqrt({src(t[1])})", "log1p": f"np.log1p({src(t[1])})", "inv1p": f"(1.0/(1.0+{src(t[1])}))"}[t[0]]
    return f"({src(t[1])}{ {'add': '+', 'sub': '-', 'mul': '*', 'div': '/'}[t[0]]}{src(t[2])})"
_CODE = {}
def ev(t, V):
    s = to_s(t); c = _CODE.get(s)
    if c is None:
        if len(_CODE) > 400000: _CODE.clear()
        c = _CODE[s] = compile(src(t), "tree", "eval")
    with np.errstate(all="ignore"):
        try: return eval(c, {"np": np, "V": V})
        except (ZeroDivisionError, OverflowError): return float("nan")
def uses(t, name): return t == name if isinstance(t, str) else any(uses(c, name) for c in t[1:])
_gA = {k: v.ravel() for k, v in zip(("v", "z", "eta", "cf"), np.meshgrid([1e-4, 3e-3], [1.0, 3.0, 9.0], [10.0, 30.0], [4.0, 10.0]))}; T1A = dict(_gA, q=np.zeros(24))
_xc = np.array([1e-3, 0.1, 1.0, 10.0, 1e3]); T1B0 = dict(xb=np.zeros(5), fl=np.zeros(5), q=np.zeros(5), xc=_xc); _qo = np.array([0.0, 1.0, 100.0, 1e4]); T1B1 = dict(xc=np.full(4, 1e-30), fl=np.full(4, 1 / 5.271), xb=np.full(4, 1e-30 / 5.271), q=_qo)
def tier1(t, kind):
    if kind == "A": return bool(np.all(np.abs(np.broadcast_to(ev(t, T1A), (24,)) - 1) < 1e-12))
    return bool(np.all(np.abs(np.broadcast_to(ev(t, T1B0), (5,)) - 1) < 1e-12) and np.all(np.abs(np.broadcast_to(ev(t, T1B1), (4,)) - 1) < 1e-12))
# ------------------------------------------------------------------ data
def Bf(x): return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
_x = np.linspace(1e-5, 1, 200001); _bb = Bf(_x) * 4 * _x ** 2 / (1 + _x ** 2) ** 1.5 / _x; I1 = float(np.sum(0.5 * (_bb[1:] + _bb[:-1]) * np.diff(_x)))
class Sys:
    """systems: r0, Rout, Mout, and A's leaves."""
    def __init__(s, c, Mst, halos=None, r0=None, Rout=None, S=None, eta=None, zf=None, Mtot=None):
        g = c["GE"]; s.r0 = np.array([h["r0"] for h in halos] if halos else r0, float); s.R = np.array([h["R200"] for h in halos] if halos else Rout, float); s.S = np.array([h["S"] for h in halos] if halos else S, float); eta = np.array([h["eta"] for h in halos] if halos else eta, float); zf = np.array([h["zf"] for h in halos] if halos else zf, float); Mt = np.array([h["M2"] for h in halos] if halos else Mtot, float)
        s.Mout = math.pi * s.S * s.r0 ** 2 * Bf(s.R / s.r0); W = g * (math.pi * s.S * s.r0 ** 2) ** 2 / s.r0 * I1; E = (np.asarray(Mst, float) / 100.0) * 1e51 * ERG + 0.1 * 0.005 * np.asarray(Mst, float) * c["MSUNE"] * CL ** 2
        s.V = dict(q=E / W, v=np.sqrt(g * Mt / s.R) / CL, z=1 + zf, eta=eta, cf=4 * (eta / 10.82) ** 0.8)
    def rho(s, t):
        if t == "1": return np.ones_like(s.r0)
        return np.broadcast_to(ev(t, s.V), s.r0.shape).astype(float)
    def Mfrac(s, rho, r, idx=None):
        """M_c(r; rho) with mass at Rout held; r broadcast with idx-selected systems."""
        r0 = (s.r0 if idx is None else s.r0[idx]); R = (s.R if idx is None else s.R[idx]); M = (s.Mout if idx is None else s.Mout[idx]); p = (rho if idx is None else rho[idx]); re = p * r0
        return M * Bf(np.minimum(r, R) / re) / Bf(R / re)
class Data:
    def __init__(d, cachef=CACHE):
        C = pickle.load(open(cachef, "rb")); d.C = C; d.c = C["const"]; d.UPS = C["UPS"]; d.a0 = dict(C["const"]["A0"]); g = C["gals"]; d.gals = g
        d.sel = [i for i, q in enumerate(g) if q["vf"] > 0 and q["Q"] <= 2 and q["inc"] >= 30 and 20 <= q["vf"] <= 400]; d.split = d.make_split()
        d.ctx = {}; d.pl = None
        d.lt = {t: d.build_lt(t) for t in TAGS}; d.cl = {h: d.build_cl(h) for h in HKS}; d.xc = d.build_xc(); d.gr = C["groups"]
    def make_split(d):
        f = os.path.join(HERE, "split.json")
        if os.path.exists(f): return json.load(open(f))
        r = np.random.default_rng(SPLIT_SEED); tr, ho = [], []
        for k, (lo, hi) in enumerate(BINS):
            m = [i for i in d.sel if (lo <= d.gals[i]["vf"] < hi or (hi == 400 and d.gals[i]["vf"] == 400))]; m = list(r.permutation(m)); n = len(m) // 2 + (len(m) % 2 if k % 2 == 1 else 0); tr += [int(x) for x in m[:n]]; ho += [int(x) for x in m[n:]]
        o = dict(seed=SPLIT_SEED, n_unique=len(d.sel), train=sorted(tr), holdout=sorted(ho), train_names=sorted(d.gals[i]["name"] for i in tr), holdout_names=sorted(d.gals[i]["name"] for i in ho)); json.dump(o, open(f, "w"), indent=1); return o
    def sparc(d, idx, tag):
        key = (tuple(idx), tag)
        if key in d.ctx: return d.ctx[key]
        G = [d.gals[i] for i in idx]; n = [len(q["Rm"]) for q in G]; st = np.r_[0, np.cumsum(n)[:-1]]; gid = np.repeat(np.arange(len(G)), n); Rm = np.concatenate([q["Rm"] for q in G]); GB = np.vstack([q["GB"] for q in G]); lgo = np.concatenate([np.log10(q["GO"]) for q in G]); OK = np.vstack([q["OK"] for q in G]); W = np.concatenate([q["W"] for q in G])
        Wm = np.where(OK, W[:, None], 0.0); ge = d.c["GE"]; s = Sys(d.c, [0.5 * q["L36"] * 1e9 for q in G], [q["halo"][tag] for q in G])
        M0 = s.Mfrac(np.ones_like(s.r0), Rm, gid); Mb = np.maximum(GB * Rm[:, None] ** 2 / ge, 0.0); o = dict(s=s, gid=gid, st=st, Rm=Rm, GB=GB, lgo=lgo, Wm=Wm, ws=np.add.reduceat(Wm, st, axis=0), M0=M0, Mb=Mb, gc0=ge * M0 / Rm ** 2, vf=np.array([q["vf"] for q in G]), q_p=s.V["q"][gid][:, None], memo={}); d.ctx[key] = o; return o
    def build_lt(d, tag):
        L = d.C["lt"]; ge = d.c["GE"]; K = d.c["MPCE"] / 1e3; s = Sys(d.c, [r["Mstar"] for r in L], [r["halo"][tag] for r in L]); R = np.array([r["R"] for r in L]) * K; Mb = 10 ** np.array([r["logMb"] for r in L]) * d.c["MSUNE"]; V = np.array([r["V"] for r in L]); return dict(s=s, R=R, Mb=Mb, lgo=np.log10((V * 1e3) ** 2 / R), M0=s.Mfrac(np.ones_like(s.r0), R))
    def build_cl(d, h):
        c = d.C["clusters"]["by_hk"][h]; R = c["rows"]; A = lambda k: np.array([r[k] for r in R]); st = 0.034 / 1.034; s = Sys(d.c, st * A("Mbt") / d.c["MSUNE"], r0=A("r0"), Rout=A("rta"), S=A("S"), eta=A("eta"), zf=A("zf"), Mtot=A("Mfair") + A("Mbt")); nd = A("nd"); idx = np.arange(len(R))[:, None]; M0 = s.Mfrac(np.ones_like(s.r0), nd, idx); ok = c["m2"] > 0
        return dict(s=s, nd=nd, idx=idx, M0=M0, Mb=A("Mb_nd"), P0=A("P0"), S0=A("S0"), LP=A("LP"), LS=A("LS"), W=c["W"], m2=np.where(ok, c["m2"], 1.0), m=c["m"], ok=ok)
    def build_xc(d):
        X = d.C["xcop_halo"]; nm = list(X); A = lambda k: np.array([X[n][k] for n in nm]); s = Sys(d.c, 0.034 / 1.034 * A("Mbt") / d.c["MSUNE"], r0=A("r0"), Rout=A("rta"), S=A("S"), eta=A("eta"), zf=A("zf"), Mtot=A("Mfair") + A("Mbt")); rows = d.C["xcop"]["canonical"]["rows"]; ix = np.array([nm.index(r["cluster"]) for r in rows]); return dict(s=s, ix=ix, r=np.array([r["r_kpc"] for r in rows]) * 1e3 * 3.0857e16, Mb=np.array([r["Mb_Msun"] for r in rows]) * d.c["MSUNE"], MH=np.array([r["MHSE_Msun"] for r in rows]) * d.c["MSUNE"])
    # -------------------------------------------------------------- graders
    def sparc_fit(d, o, At, Bt, a0):
        s = o["s"]; A = s.rho(At)
        if not valid_A(A): return None
        Mc = o["M0"] if At == "1" else s.Mfrac(A, o["Rm"], o["gid"]); gc = d.c["GE"] * Mc / o["Rm"] ** 2
        if Bt == "1": gh = gc[:, None]
        else:
            k = (to_s(Bt), a0); Bv = o["memo"].get(k)
            if Bv is None:
                if len(o["memo"]) > 300: o["memo"].clear()
                f = o["Mb"] / o["M0"][:, None]; V = dict(xb=o["GB"] / a0, xc=(o["gc0"] / a0)[:, None], fl=f, q=o["q_p"]); Bv = np.broadcast_to(ev(Bt, V), o["GB"].shape); okp = o["Wm"] > 0
                if not (np.all(np.isfinite(Bv[okp])) and np.all(Bv[okp] > 0)): Bv = False
                o["memo"][k] = Bv
            if Bv is False: return None
            gh = gc[:, None] * Bv
        r = o["lgo"][:, None] - np.log10(np.maximum(o["GB"] + gh, 1e-300)); wr2 = np.add.reduceat(o["Wm"] * r * r, o["st"], axis=0); iu = np.argmin(wr2 / np.maximum(o["ws"], 1e-300), axis=1); ig = np.arange(len(iu)); return d.UPS[iu], wr2[ig, iu], o["ws"][ig, iu], A
    def lt_E(d, tag, At, Bt, a0):
        o = d.lt[tag]; s = o["s"]; A = s.rho(At)
        if not valid_A(A): return None
        ge = d.c["GE"]; R = o["R"]; Mc = s.Mfrac(A, R); gN = ge * o["Mb"] / R ** 2
        if Bt != "1":
            Bv = np.broadcast_to(ev(Bt, dict(xb=gN / a0, xc=ge * o["M0"] / R ** 2 / a0, fl=o["Mb"] / o["M0"], q=s.V["q"])), R.shape)
            if not (np.all(np.isfinite(Bv)) and np.all(Bv > 0)): return None
            Mc = Mc * Bv
        return o["lgo"] - np.log10(gN + ge * Mc / R ** 2)
    def cluster_V(d, h, At, Bt, a0):
        o = d.cl[h]; s = o["s"]; A = s.rho(At)
        if not valid_A(A): return None
        ratio = (s.Mfrac(A, o["nd"], o["idx"]) / o["M0"]) if At != "1" else 1.0
        if Bt != "1":
            ge = d.c["GE"]; r2 = o["nd"] ** 2; Bv = np.broadcast_to(ev(Bt, dict(xb=ge * o["Mb"] / r2 / a0, xc=ge * o["M0"] / r2 / a0, fl=o["Mb"] / o["M0"], q=s.V["q"][:, None])), o["nd"].shape)
            if not (np.all(np.isfinite(Bv)) and np.all(Bv > 0)): return None
            ratio = ratio * Bv
        de = ratio - 1.0
        if np.isscalar(de) or np.ndim(de) == 0: Pp, Sb = o["P0"], o["S0"]
        else: Pp = o["P0"] + np.einsum("ibk,ik->ib", o["LP"], de); Sb = np.maximum(o["S0"] + np.einsum("ibk,ik->ib", o["LS"], de), 1e-300)
        return o["W"] * Pp * redf(o, Sb)
    def keys_from_V(d, V, foot, h):
        return keys_core(d.C["clusters"], V, foot, h, d.pl)
    def cluster_keys(d, At, Bt, foot="canonical"):
        a0 = d.a0[foot]; Z = {}
        for h in HKS:
            V = d.cluster_V(h, At, Bt, a0)
            if V is None: return None
            Z[h] = d.keys_from_V(V, foot, h)
        return Z
    def S_eff(d, s, A):
        re = A * s.r0; return s.Mout / (math.pi * re ** 2 * Bf(s.R / re)) / (d.c["MSUNE"] / d.c["PC2"])
    def grade(d, At, Bt, idx=None, foot="canonical", intervals=None, keys=True):
        idx = d.split["train"] if idx is None else idx; a0 = d.a0[foot]; R = dict(g1=0.0, g2=0.0, g3=0.0, g4=0.0, detail={})
        for t in TAGS:
            o = d.sparc(idx, t); f = d.sparc_fit(o, At, Bt, a0)
            if f is None: return None
            U, _, _, A = f; md = float(np.median(U)); lo = o["vf"] < 100; hi = o["vf"] > 150; tilt = float(np.median(U[lo]) - np.median(U[hi])); R["g1"] += max(0.0, abs(md - 0.65) - 0.15) + max(0.0, abs(tilt) - 0.15); R["detail"][t] = dict(U=md, tilt=tilt)
            if t == TA:
                S = d.S_eff(o["s"], A); zs = []; iv = intervals or ET1_CI
                if d.pl: iv = d.pl["iv"]
                for k, (l, h_) in enumerate(BINS):
                    m = (o["vf"] >= l) & (o["vf"] < h_ if h_ < 400 else o["vf"] <= h_); sm = float(np.median(S[m])); a, b = iv[k]; c_, w = 0.5 * math.log(a * b), 0.5 * math.log(b / a); z = 1.96 * (math.log(sm) - c_) / w; zs.append(z); R["g2"] += max(0.0, abs(z) - 1.96)
                R["detail"]["S_z"] = zs
            Es = d.lt_E(t, At, Bt, a0)
            if Es is None: return None
            e = float(np.median(Es)) - (d.pl["ltoff"][t] if d.pl else 0.0); R["g3"] += max(0.0, abs(e) - 0.05) / 0.05; R["detail"]["E_" + t] = e
        if keys:
            Z = d.cluster_keys(At, Bt, foot)
            if Z is None: return None
            w = np.maximum(np.abs(Z[HKS[0]]), np.abs(Z[HKS[1]])); R["g4"] = float(np.sum(np.maximum(0.0, w - 2.0))); R["detail"]["Z"] = {h: Z[h].tolist() for h in HKS}; R["detail"]["bad"] = [KEYS[i] for i in np.where(w > 2)[0]]
        R["gate"] = R["g1"] + R["g2"] + R["g3"] + R["g4"]; R["loss"] = R["gate"] + LAM * (size(At) + size(Bt)); return R
    def xcop(d, At, Bt, foot="canonical"):
        o = d.xc; s = o["s"]; A = s.rho(At)
        if not valid_A(A): return None
        i = o["ix"]; a0 = d.a0[foot]; ge = d.c["GE"]; Mc = s.Mfrac(A, o["r"], i)
        if Bt != "1":
            M0 = s.Mfrac(np.ones_like(s.r0), o["r"], i); r2 = o["r"] ** 2; Bv = np.broadcast_to(ev(Bt, dict(xb=ge * o["Mb"] / r2 / a0, xc=ge * M0 / r2 / a0, fl=o["Mb"] / M0, q=s.V["q"][i])), o["r"].shape); Mc = Mc * Bv
        x = np.log10(o["MH"] / (o["Mb"] + Mc)); return dict(mean=float(x.mean()), rms=float(np.sqrt(np.mean(x ** 2))), PASS=bool(abs(x.mean()) <= 0.05 and np.sqrt(np.mean(x ** 2)) <= 0.10))
    def groups(d, At, Bt, foot="canonical"):
        g = d.gr; XG, LXG, RH, MH = g["XG"], g["LXG"], g["RHO_H"], g["M_H"]; G_, MS, KP, HR = g["G"], g["MS"], g["KP"], g["HERN_RE"]; a0 = d.a0[foot]; D, SL = [], []
        def one(o, dl):
            h = o[f"h{dl:+.2f}"]; lM = o["lM"] + dl; Mb = 10 ** lM * MS; a = o["Re"] * KP / HR; s = Sys(d.c, [Mb / d.c["MSUNE"]], [h]); A = s.rho(At)
            if not valid_A(A): return None
            rr = XG * a; Mc = s.Mfrac(A, rr, np.zeros(1, int)[0]) if False else (s.Mout[0] * Bf(np.minimum(rr, s.R[0]) / (A[0] * s.r0[0])) / Bf(s.R[0] / (A[0] * s.r0[0])))
            if Bt != "1":
                M0 = s.Mout[0] * Bf(np.minimum(rr, s.R[0]) / s.r0[0]) / Bf(s.R[0] / s.r0[0]); Mbr = Mb * MH; Bv = np.broadcast_to(ev(Bt, dict(xb=G_ * Mbr / rr ** 2 / a0, xc=G_ * M0 / rr ** 2 / a0, fl=Mbr / M0, q=s.V["q"][0])), rr.shape)
                if not (np.all(np.isfinite(Bv)) and np.all(Bv > 0)): return None
                Mc = Mc * Bv
            gN = MH / XG ** 2 + Mc / Mb / XG ** 2; s2 = float(np.trapz(4 * np.pi * XG ** 2 * RH * XG * gN * XG, LXG) / 3.0) * G_ * Mb / a; return 0.5 * math.log10(s2) - 3.0
        for o in g["rows"]:
            v, p, m = one(o, 0.0), one(o, 0.01), one(o, -0.01)
            if None in (v, p, m): return None
            D.append(o["ls"] - v); SL.append((p - m) / 0.02)
        D = np.array(D); n = len(D); me = float(D.mean()); se = float(D.std(ddof=1) / math.sqrt(n)); sy = float(np.mean(SL) * 0.10); tot = math.hypot(se, sy); Z = me / tot; ver = "NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW")); return dict(mean=me, Z=Z, verdict=ver, PASS=ver == "CONSISTENT")
def valid_A(A): return bool(np.all(np.isfinite(A)) and np.all(A >= 1e-3) and np.all(A <= 1e3))
def redf(o, Sb):
    f = np.ones_like(Sb)
    for p in range(6): f = f + Sb ** (p + 1) * o["m"][:, p] / o["m2"]
    return np.where(o["ok"], f, 1.0)
_FC = {}
def keys_core(CC, V, foot, h, plant=None):
    cl = f"{foot}|{h}"; T = CC["tmpl"][cl]; vC = T if False else CC["tmpl"][cl + "|vC"]; I, TID, T3M, X = CC["I"], CC["TID"], CC["T3M"], CC["X1m"]; ba = CC["BANDS"]; BN = CC["BN"]; vB = np.array([V[..., ba[b]].sum(-1) for b in BN]).T; kt, ktC = vB[I], vC[I]
    k_ = (foot, h)
    if k_ not in _FC:
        _FC[k_] = dict(F=[np.linalg.inv(np.einsum("i,ij,ik->jk", ktC[:, b], X, X)) for b in range(3)], t=[[ktC[TID == t, b].sum() for t in range(3)] for b in range(3)], a=[ktC[:, b].sum() for b in range(3)], m=[[vC[T3M == t, b].sum() for t in range(3)] for b in range(3)], al=[vC[:, b].sum() for b in range(3)])
    q = _FC[k_]; p = {}
    At = lambda b: [kt[TID == t, b].sum() / q["t"][b][t] for t in range(3)]; bp = lambda b: float((q["F"][b] @ (X.T @ kt[:, b]))[1])
    a1, a2 = At(1), At(2)
    for t in range(3): p[f"G-MID-T{t+1}"] = a1[t]; p[f"G-OUT-T{t+1}"] = a2[t]; p[f"G-OUT-M{t+1}"] = vB[T3M == t, 2].sum() / q["m"][2][t]
    p["G-MID-b"] = bp(1); p["G-OUT-b"] = bp(2); p["G-OUT-all"] = kt[:, 2].sum() / q["a"][2]; p["G-IN-all"] = kt[:, 0].sum() / q["a"][0]; p["G-OUT-Mall"] = vB[:, 2].sum() / q["al"][2]; p["G-IN-Mall"] = vB[:, 0].sum() / q["al"][0]
    pv = np.array([p[k] for k in KEYS]); ms = np.array([T[k] for k in KEYS])
    if plant is not None and plant.get("meas") is not None: ms = np.c_[plant["meas"][h], ms[:, 1]]
    if plant is not None and plant.get("capture"): plant["pred_out"][h] = pv.copy()
    return (ms[:, 0] - pv) / ms[:, 1]
# ------------------------------------------------------------------ search
class Search:
    def __init__(S, D, gram, seed, tag=None, pop=POP, gens=GENS):
        S.D, S.gram, S.seed, S.pop_n, S.gens = D, gram, seed, pop, gens; S.r = random.Random(seed); S.cache = {}; S.hits = []; S.pareto = []; S.n_eval = 0; S.n_t1 = 0; S.n_t1_pass = 0; S.tag = tag or f"{gram}_s{seed}"; S.f = os.path.join(HERE, "runs", f"genome_bank_{S.tag}.json"); S.stop = False; S.best = []; S.near = []
    def rand_tree(S, kind, d):
        L = leaves(kind, S.gram)
        if d == 0 or S.r.random() < 0.3: return S.r.choice(L)
        if S.r.random() < 0.3: return (S.r.choice(UN), S.rand_tree(kind, d - 1))
        return (S.r.choice(BIN), S.rand_tree(kind, d - 1), S.rand_tree(kind, d - 1))
    def legal(S, t, kind):
        t = simplify(t)
        if size(t) > MAXN or depth(t) > MAXD: return None
        if t == "0" : return None
        S.n_t1 += 1
        if t != "1" and not tier1(t, kind): return None
        S.n_t1_pass += 1; return t
    def seed_tree(S, kind):
        """Random tree of a form that can pass Tier 1: the search's start. Mutation is then unconstrained."""
        for _ in range(400):
            X = S.rand_tree(kind, 2)
            if kind == "A": f = S.r.choice([("add", "1", X), ("inv1p", X), ("sqrt", ("add", "1", X)), ("add", "1", ("log1p", X)), ("inv1p", ("log1p", X))]); t = _sub_factor(f, X, S.r.choice([("mul", "q", X), ("div", "q", X)]), S.r)
            else:
                fac = S.r.choice([("mul", "fl", "xc") if S.gram == "SPEC" else "fl", "xb" if S.gram == "SPEC" else ("mul", "fl", "q"), "q"]); t = S.r.choice([("add", "1", ("mul", fac, X)), ("inv1p", ("mul", fac, X)), ("add", "1", ("log1p", ("mul", fac, X)))])
            t = S.legal(t, kind)
            if t is not None and t != "1": return t
        return "1"
    def nodes(S, t, path=()):
        yield path, t
        if not isinstance(t, str):
            for i, c in enumerate(t[1:], 1): yield from S.nodes(c, path + (i,))
    def put(S, t, path, x):
        if not path: return x
        l = list(t); l[path[0]] = S.put(t[path[0]], path[1:], x); return tuple(l)
    def mutate(S, t, kind):
        p, n = S.r.choice(list(S.nodes(t))); u = S.r.random()
        if u < 0.45: x = S.rand_tree(kind, S.r.randint(0, 2))
        elif u < 0.75:
            if isinstance(n, str): x = S.r.choice(leaves(kind, S.gram))
            elif n[0] in UN: x = (S.r.choice(UN), n[1])
            else: x = (S.r.choice(BIN), n[1], n[2])
        elif u < 0.9: x = (S.r.choice(BIN), n, S.rand_tree(kind, 1)) if S.r.random() < 0.7 else (S.r.choice(UN), n)
        else: x = n if isinstance(n, str) else S.r.choice(list(n[1:]))
        return S.put(t, p, x)
    def cross(S, a, b):
        pa, _ = S.r.choice(list(S.nodes(a))); _, nb = S.r.choice(list(S.nodes(b))); return S.put(a, pa, nb)
    def score(S, A, B):
        k = (to_s(A), to_s(B)); v = S.cache.get(k)
        if v is not None: return v
        R = S.D.grade(A, B); S.n_eval += 1
        v = (1e9,) if R is None else (R["loss"], R["gate"], R["g1"] + R["g2"] + R["g3"], R["g4"], R["g1"], R["g2"], R["g3"]); S.cache[k] = v
        if R is not None:
            S.note(A, B, v, R)
        return v
    def note(S, A, B, v, R):
        rec = dict(A=to_s(A), B=to_s(B), At=A, Bt=B, gate=v[1], g123=v[2], g4=v[3], g1=v[4], g2=v[5], g3=v[6], nodes=size(A) + size(B), bad=R["detail"]["bad"])
        if v[1] == 0.0: S.hits.append(rec)
        if v[2] == 0.0 and max(abs(z) for h in HKS for z in R["detail"]["Z"][h]) <= 2.25: S.near.append(rec)
        S.best.append(rec)
        if len(S.best) > 400: S.best = sorted(S.best, key=lambda x: x["gate"])[:200]
        if not any(p["g123"] <= rec["g123"] and p["g4"] <= rec["g4"] for p in S.pareto):
            S.pareto = [p for p in S.pareto if not (rec["g123"] <= p["g123"] and rec["g4"] <= p["g4"])] + [rec]
    def child(S, P_):
        a = S.tourn(P_); b = S.tourn(P_); A, B = a; u = S.r.random(); which = S.r.random() < 0.5; kind = "A" if which else "B"; x = A if which else B; y = b[0] if which else b[1]
        for _ in range(30):
            c = S.cross(x, y) if u < 0.4 else S.mutate(x, kind); c = S.legal(c, kind)
            if c is not None: return (c, B) if which else (A, c)
        return (A, B)
    def tourn(S, P_):
        return min(S.r.sample(P_, min(3, len(P_))), key=lambda g: S.score(*g)[0])
    def save(S, gen, P_):
        os.makedirs(os.path.dirname(S.f), exist_ok=True); tmp = S.f + ".tmp"; json.dump(dict(gen=gen, pop=P_, rng=None, n_eval=S.n_eval, n_t1=S.n_t1, n_t1_pass=S.n_t1_pass, n_distinct=len(S.cache), hits=S.hits, near=S.near, pareto=S.pareto, best=sorted(S.best, key=lambda x: x["gate"])[:60], hist=S.hist, gram=S.gram, seed=S.seed, done=gen >= S.gens or bool(S.hits and S.stop_on_hit)), open(tmp, "w"), default=str); os.replace(tmp, S.f)
    hist = None; stop_on_hit = False
    def run(S, stop_on_hit=False, quiet=False):
        S.stop_on_hit = stop_on_hit; S.hist = []; g0 = 0; P_ = None
        if os.path.exists(S.f):
            J = json.load(open(S.f))
            if J.get("done"): print(S.tag, "already done"); return J
            fix = lambda t: t if isinstance(t, str) else tuple(fix(c) if i else c for i, c in enumerate(t)); P_ = [(fix(a), fix(b)) for a, b in J["pop"]]; g0 = J["gen"]; S.hist = J["hist"]; S.hits = J["hits"]; S.near = J.get("near", []); S.pareto = J["pareto"]; S.best = J["best"]; S.n_eval = J["n_eval"]; S.n_t1, S.n_t1_pass = J["n_t1"], J["n_t1_pass"]; S.r.seed(S.seed * 1000 + g0)
        if P_ is None: P_ = [("1", "1")] + [(S.seed_tree("A") if i % 3 else "1", S.seed_tree("B") if i % 3 != 1 else "1") for i in range(S.pop_n - 1)]
        signal.signal(signal.SIGTERM, lambda *a: setattr(S, "stop", True)); t0 = time.time()
        for gen in range(g0, S.gens):
            sc = sorted(P_, key=lambda g: S.score(*g)[0]); b = S.score(*sc[0]); S.hist.append([gen, b[0], b[1], S.n_eval, len(S.hits)])
            if not quiet and (gen % 20 == 0 or gen == S.gens - 1): print(f"{S.tag} gen {gen}: loss {b[0]:.3f} gate {b[1]:.3f} (g1 {b[4]:.2f} g2 {b[5]:.2f} g3 {b[6]:.2f} g4 {b[3]:.2f}) A {to_s(sc[0][0])} B {to_s(sc[0][1])}; evals {S.n_eval}, hits {len(S.hits)}; {time.time()-t0:.0f} s", flush=True)
            if (stop_on_hit and S.hits): S.save(gen, sc); return dict(hits=S.hits, gen=gen, n_eval=S.n_eval)
            if S.stop: S.save(gen, sc); print("SIGTERM: checkpoint", flush=True); sys.exit(75)
            # diversity (K8's first run stalled on clones): one copy of each pair, at most 8 pairs per A and per B, 15 % new blood
            seen, na, nb, sc2 = set(), {}, {}, []
            for g in sc:
                k = (to_s(g[0]), to_s(g[1])); ka, kb = k
                if k in seen or na.get(ka, 0) >= 8 or nb.get(kb, 0) >= 8: continue
                seen.add(k); na[ka] = na.get(ka, 0) + 1; nb[kb] = nb.get(kb, 0) + 1; sc2.append(g)
            nw = sc2[:10] + [(S.seed_tree("A") if S.r.random() < 0.7 else "1", S.seed_tree("B") if S.r.random() < 0.5 else "1") for _ in range(int(0.15 * S.pop_n))]
            for _ in range(20 * S.pop_n):
                if len(nw) >= S.pop_n: break
                g = S.child(sc2); k = (to_s(g[0]), to_s(g[1]))
                if k in seen: continue
                seen.add(k); nw.append(g)
            P_ = (nw + sc2)[:S.pop_n]
            if gen % 10 == 9: S.save(gen + 1, P_)
        S.save(S.gens, P_); return dict(hits=S.hits, gen=S.gens, n_eval=S.n_eval)
def _sub_factor(f, X, repl, r):
    if f == X: return repl
    if isinstance(f, str): return f
    return tuple([f[0]] + [_sub_factor(c, X, repl, r) for c in f[1:]])
# ------------------------------------------------------------------ bounded enumeration, value-deduplicated
class Enum:
    """Bottom-up, depth <= MAXD. Rows are values on Tier 1's points and a sample of real systems; a row that repeats an earlier one (10 significant digits) is dropped, as is one non-finite on real systems. Only sizes completed are ever called exhausted."""
    def __init__(E, D, kind, gram, max_rows=400000, max_pairs=4e8, nreal=12):
        E.kind, E.gram = kind, gram; r = np.random.default_rng(7); Tv, Rv = {}, {}
        if kind == "A":
            pool = [D.sparc(D.split["train"], TA)["s"], D.lt[TA]["s"], D.cl[HKS[0]]["s"]]; names = LEAF_A
            for n in names: Rv[n] = np.concatenate([p.V[n] for p in pool])
            ix = r.choice(len(Rv["q"]), nreal, replace=False); Rv = {k: v[ix] for k, v in Rv.items()}; _t = np.arange(0, 24, 3); Tv = {k: T1A[k][_t] for k in names}; E.nt = 8
        else:
            o = D.sparc(D.split["train"], TA); iu = int(np.argmin(abs(D.UPS - 0.5))); a0 = D.a0["canonical"]; c = D.cl[HKS[0]]; ge = D.c["GE"]; xb = np.r_[o["GB"][:, iu] / a0, (ge * c["Mb"] / c["nd"] ** 2 / a0).ravel()]; xc = np.r_[o["gc0"] / a0, (ge * c["M0"] / c["nd"] ** 2 / a0).ravel()]; fl = np.r_[o["Mb"][:, iu] / o["M0"], (c["Mb"] / c["M0"]).ravel()]; q = np.r_[o["s"].V["q"][o["gid"]], np.repeat(c["s"].V["q"], c["nd"].shape[1])]; ok = fl > 0; ix = r.choice(np.where(ok)[0], nreal, replace=False); Rv = dict(xb=xb[ix], xc=xc[ix], fl=fl[ix], q=q[ix]); names = LEAF_B[gram]; Tv = {k: np.r_[T1B0[k], T1B1[k]] for k in names}; E.nt = 9
        E.names = names; E.rows = []; E.back = []; E.dep = []; E.sz = []; E.seen = set(); E.R = r; E.w = r.integers(1, 2 ** 62, E.nt + nreal, dtype=np.int64) | 1; E.max_rows = max_rows; E.max_pairs = max_pairs; E.by = {}; E.done = 0; E.surv = {}; E.counts = {}
        init = [np.r_[Tv[n], Rv[n]] for n in names] + [np.full(E.nt + nreal, CONST[c_]) for c_ in CONS[gram]]; lab = names + CONS[gram]; E.lab = lab; E.add(np.array(init), [("L", l, -1) for l in lab], np.zeros(len(init), int), 1)
    def hash(E, X):
        with np.errstate(all="ignore"):
            m = np.where((X == 0) | ~np.isfinite(X), 1.0, 10.0 ** np.floor(np.log10(np.abs(np.where(np.isfinite(X) & (X != 0), X, 1.0))))); Y = np.round(np.nan_to_num(X / m, nan=7.25, posinf=8.25, neginf=9.25), 9); Z = np.round(np.nan_to_num(np.log10(m), nan=0.0), 0)
        return ((Y * 1e9).astype(np.int64) * E.w + (Z.astype(np.int64) * 1000003) * E.w[::-1]).sum(1)
    def keep(E, X):
        nr = X[:, E.nt:]; return np.all(np.isfinite(nr), axis=1) & np.all(np.abs(nr) < 1e30, axis=1)
    def add(E, X, back, dep, sz, store=True):
        """back may be a list or (op codes, i, j) arrays. store False is a last size: Tier 1 survivors only, no value dedup."""
        if not store:
            sv = np.all(np.abs(X[:, :E.nt] - 1) < 1e-12, axis=1) & E.keep(X); E.counts[sz] = E.counts.get(sz, 0) + len(X); E.back_extra = getattr(E, "back_extra", [])
            for i in np.where(sv)[0]: E.back_extra.append((back[0][i], int(back[1][i]), int(back[2][i]))); E.surv.setdefault(sz, []).append(-len(E.back_extra))
            return len(X)
        k = E.keep(X); idx = np.where(k)[0]
        if not len(idx): return 0
        X = X[idx]; dep = dep[idx]; h = E.hash(X); _, u = np.unique(h, return_index=True); u = np.sort(u); nk = []
        for i in u:
            hi = int(h[i])
            if hi not in E.seen: E.seen.add(hi); nk.append(i)
        if not nk: return 0
        nk = np.array(nk); X = X[nk]; dep = dep[nk]; bk = [back[idx[i]] for i in nk] if isinstance(back, list) else [(back[0][idx[i]], int(back[1][idx[i]]), int(back[2][idx[i]])) for i in nk]
        d1 = np.abs(X[:, :E.nt] - 1); sv = np.all(d1 < 1e-12, axis=1)
        base = E.total_rows(); E.by.setdefault(sz, []).append(np.arange(base, base + len(nk))); E.rows.append(X); E.dep.append(dep); E.back += bk; E.surv.setdefault(sz, []).extend((base + np.where(sv)[0]).tolist())
        E.counts[sz] = E.counts.get(sz, 0) + len(nk); return len(nk)
    def total_rows(E): return sum(len(x) for x in E.rows)
    def tree(E, i):
        b = E.back_extra[-1 - i] if i < 0 else E.back[i]
        if b[0] == "L": return b[1]
        o = (BIN + UN)[b[0]]; return (o, E.tree(b[1])) if b[2] < 0 else (o, E.tree(b[1]), E.tree(b[2]))
    def size_ids(E, s): return np.concatenate(E.by[s]) if s in E.by else np.zeros(0, int)
    def grow(E, s, store=True, t_limit=1e9):
        M = np.vstack(E.rows); Dp = np.concatenate(E.dep); E.rows = [M]; E.dep = [Dp]; chunk = 40000; t0 = time.time(); npair = 0
        def proc(ai, bi, code):
            nonlocal npair
            for k in range(0, len(ai), chunk):
                a_ = ai[k:k + chunk]; b_ = bi[k:k + chunk] if bi is not None else None; d_ = (np.maximum(Dp[a_], Dp[b_]) if b_ is not None else Dp[a_]) + 1; m = d_ <= MAXD
                if not m.any(): continue
                a_ = a_[m]; d_ = d_[m]; x = M[a_]
                with np.errstate(all="ignore"):
                    if code < 4:
                        b2 = b_[m]; y = M[b2]; X = x + y if code == 0 else x - y if code == 1 else x * y if code == 2 else x / y
                    else: b2 = np.full(len(a_), -1); X = np.sqrt(x) if code == 4 else np.log1p(x) if code == 5 else 1 / (1 + x)
                npair += len(a_); E.add(X, (np.full(len(a_), code), a_, b2), d_, s, store)
                if time.time() - t0 > t_limit: return False
            return True
        ok = True
        for c in (4, 5, 6):
            ok = ok and proc(E.size_ids(s - 1), None, c)
        for sa in range(1, s - 1):
            sb = s - 1 - sa
            A_, B_ = E.size_ids(sa), E.size_ids(sb)
            if not len(A_) or not len(B_): continue
            for c in (0, 1, 2, 3):
                if c in (0, 2) and sa > sb: continue
                aa = np.repeat(A_, len(B_)); bb = np.tile(B_, len(A_))
                if c in (0, 2) and sa == sb: m = aa <= bb; aa, bb = aa[m], bb[m]
                ok = ok and proc(aa, bb, c)
        return ok, npair
    def pairs_at(E, s):
        n = {k: len(E.size_ids(k)) for k in E.by}; return 3 * n.get(s - 1, 0) + 4 * sum(n.get(a, 0) * n.get(s - 1 - a, 0) for a in range(1, s - 1))
def sweep(D, gram, budget_s=1500, top=120, out=None):
    R = dict(gram=gram, A={}, B={}); best = {}
    for kind in ("A", "B"):
        E = Enum(D, kind, gram); done = 1; t0 = time.time()
        for s in range(2, MAXN + 1):
            p = E.pairs_at(s)
            if p > E.max_pairs or time.time() - t0 > budget_s: break
            last = E.total_rows() > E.max_rows; res = E.grow(s, store=not last, t_limit=budget_s); ok = res[0]
            print(f"{gram} {kind} size {s}: pairs {p:.3g}, new values {E.counts.get(s, 0)}, Tier 1 survivors {len(E.surv.get(s, []))}, rows {E.total_rows()}, {time.time()-t0:.0f} s", flush=True)
            if ok: done = s
            if not ok or last: break
        trees = []
        for s in sorted(E.surv):
            if s > done: continue
            for i in E.surv[s]:
                t = simplify(E.tree(i))
                if t != "1" and tier1(t, kind) and size(t) <= MAXN and depth(t) <= MAXD: trees.append(t)
        trees = list({to_s(t): t for t in trees}.values()); sc = []; t1 = time.time(); fin = 0
        for t in trees:
            r = D.grade(t, "1") if kind == "A" else D.grade("1", t)
            if r is not None: sc.append((r["gate"], r["g1"] + r["g2"] + r["g3"], r["g4"], to_s(t), t)); fin += 1
            if time.time() - t1 > budget_s: print("evaluation budget hit", flush=True); break
        sc.sort(key=lambda x: x[0]); best[kind] = sc[:top]; R[kind] = dict(completed_size=done, counts=E.counts, tier1_survivors=len(trees), finite_graded=fin, all_graded=len(sc) == fin and time.time() - t1 <= budget_s, hits=[x[3] for x in sc if x[0] == 0], top=[dict(tree=x[3], gate=x[0], g123=x[1], g4=x[2]) for x in sc[:40]])
        print(f"{gram} {kind}: completed size {done}; {len(trees)} Tier 1 trees, {fin} finite; best " + "; ".join(f"{x[3]} {x[0]:.3f}" for x in sc[:3]), flush=True); del E
    S = Search(D, gram, 0, tag=f"SWEEP_{gram}"); t1 = time.time(); n = 0
    for a in [("1", 0)] + [(x[4], 0) for x in best["A"]]:
        for b in [("1", 0)] + [(x[4], 0) for x in best["B"]]:
            S.score(a[0], b[0]); n += 1
    R["cross"] = dict(n=n, s=time.time() - t1, hits=S.hits, near=S.near, best=sorted(S.best, key=lambda x: x["gate"])[:40], pareto=S.pareto)
    print(f"{gram} cross {n} pairs, {time.time()-t1:.0f} s, hits {len(S.hits)}; best " + "; ".join(f"{x['A']} | {x['B']} {x['gate']:.3f}" for x in R["cross"]["best"][:3]), flush=True)
    if out: json.dump(R, open(out, "w"), indent=1, default=str)
    return R
if __name__ == "__main__" and "--sweep" in sys.argv:
    i = sys.argv.index("--sweep"); os.makedirs(os.path.join(HERE, "runs"), exist_ok=True); D = Data(); sweep(D, sys.argv[i + 1], out=os.path.join(HERE, "runs", f"sweep_{sys.argv[i + 1]}.json")); sys.exit(0)
if __name__ == "__main__" and "--ga" in sys.argv:
    i = sys.argv.index("--ga"); D = Data(); Search(D, sys.argv[i + 1], int(sys.argv[i + 2])).run(); sys.exit(0)
