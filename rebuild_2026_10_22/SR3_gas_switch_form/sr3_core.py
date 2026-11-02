#!/usr/bin/env python3
"""SR3 core: BF1's split, FG1's free-Upsilon path, form evaluation. Criteria FROZEN_CRITERIA.md. SR3_MUTATE=1: a0 x 1.5 labelled the law. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, pickle, re
import numpy as np
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); CRG = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
MUT = os.environ.get("SR3_MUTATE") == "1"
A0 = dict(canonical=9.360324825027975e-11, alt=1.1312e-10); A0_ACC = dict(canonical=9.3603e-11, alt=1.1312e-10)
if MUT: A0 = {k: 1.5 * v for k, v in A0.items()}
G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; KPC = 3.0857e19; C = 299792458.0
UPS = np.round(np.arange(0.30, 1.2000001, 0.01), 2); GRID = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00, 1.20]; IG = [int(np.argmin(np.abs(UPS - u))) for u in GRID]
L_S, L_XM, L_XR = 0.110, 0.05, 0.10; FIX_LINE = 0.1747
SEED = 20261102
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def H_plant(f, y): return 1 + 3 * f * f * y / (1 + y * y)
def gals_all():
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]; meta = {g["name"]: g for g in Q}; names = sorted(meta); T = {}
    for l in open(os.path.join(CRG, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) == 19:
            try: T[t[0]] = dict(Inc=float(t[5]), Vflat=float(t[15]), Q=float(t[17]))
            except ValueError: pass
    out = []
    for i, n in enumerate(names):
        a = np.loadtxt(os.path.join(CRG, "sparc", "rotmod", n + "_rotmod.dat"), comments="#", ndmin=2); t = T[n]; assert meta[n]["Q"] == t["Q"] and abs(meta[n]["inc"] - t["Inc"]) < 1e-9
        out.append(dict(name=n, pos=i, R=a[:, 0] * KPC, Vobs=a[:, 1].copy(), eV=a[:, 2], Vgas=a[:, 3], Vdisk=a[:, 4], Vbul=a[:, 5], **t))
    return out
def xcop():
    D = os.path.join(REPO, "real_research", "data", "xcop"); out = []
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for j, n in enumerate(sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))):
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (0.1, 0.2, 0.3, 0.5, 0.7):
            r = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(ga["RADIUS"] * rg, ga["MGAS"], r); ms = li(st["RADIUS"], st[st.names[1]], r); em = li(hm["RADIUS"], hm["EM_FORW"], r)
            if not np.all(np.isfinite([mh, mg, ms])): continue
            R = r * 1e3 * PC; ff = 1 / R ** 2 * G * MS; out.append((ff * (mg + ms), ff * mh, mg / (mg + ms), j, em / mh / math.log(10)))
    return np.array(out)
def lt_rows():
    rows = []
    for r in csv.DictReader(open(os.path.join(CRG, "little_things", "oh2015_table2.csv"))):
        if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")):
            Mg = float(r["Mgas_1e7Msun"]) * 1e7; Mb = Mg + float(r["MSED_1e7Msun"]) * 1e7; R = float(r["Rmax_kpc"]) * KPC; V = float(r["V_kms"]) * 1e3
            rows.append((6.6743e-11 * Mb * 1.98847e30 / R ** 2, V * V / R, Mg / Mb, r["name"]))
    return rows
def prep(job="real", foot="canonical"):
    """Returns dict with gals (each with F, GB fine-grid matrices, gO), X. job: real, scrambled, planted, label."""
    a0 = A0[foot]; Gs = gals_all(); X = xcop(); rng = np.random.default_rng(SEED)
    for g in Gs:
        g["GB"] = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + UPS[:, None] * g["Vdisk"] ** 2 + 1.4 * UPS[:, None] * g["Vbul"] ** 2) * 1e6 / g["R"]
        gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; g["F"] = np.clip(np.where(g["GB"] > 0, gg / np.where(g["GB"] > 0, g["GB"], 1), 0.0), 0, 1)
        g["fixgb"] = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * np.sign(g["Vdisk"]) * g["Vdisk"] ** 2 + 0.7 * np.sign(g["Vbul"]) * g["Vbul"] ** 2) * 1e6 / g["R"]; g["fixf"] = np.clip(gg / np.where(g["fixgb"] > 0, g["fixgb"], 1), 0, 1)
    if job == "planted":
        for g in Gs:
            U = 0.6 * 10 ** (0.1 * rng.standard_normal()); gb = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / g["R"]; gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; f = np.clip(gg / np.where(gb > 0, gb, 1), 0, 1)
            s = np.maximum(2 / math.log(10) * np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1), 0.05); m = law(np.maximum(gb, 1e-300), a0) * H_plant(f, np.maximum(gb, 1e-300) / a0) * 10 ** (s * rng.standard_normal(len(gb))); g["Vobs"] = np.where((gb > 0) & (g["Vobs"] > 0), np.sqrt(m * g["R"]) / 1e3, 0.0)
        y = X[:, 0] / a0; X = X.copy(); X[:, 1] = law(X[:, 0], a0) * H_plant(X[:, 2], y) * 10 ** (0.05 * rng.standard_normal(len(y)))
    if job == "label":
        for g in Gs: g["F"] = g["F"] * 0; g["fixf"] = g["fixf"] * 0
        X = X.copy(); X[:, 2] = 1.0
    if job == "scrambled":
        tr = [g for g in Gs if is_train(g)]
        for k in range(len(UPS)):
            A = [(g, i) for g in tr for i in np.nonzero(g["GB"][k] > 0)[0]]; ys = np.array([g["GB"][k, i] for g, i in A]); fs = np.array([g["F"][k, i] for g, i in A]); q = np.searchsorted(np.quantile(ys, np.arange(.1, 1, .1)), ys); r = np.random.default_rng(SEED + k); nf = fs.copy()
            for b in range(10):
                m = np.nonzero(q == b)[0]; nf[m] = fs[r.permutation(m)]
            for (g, i), v in zip(A, nf): g["F"][k, i] = v
        A = [(g, i) for g in tr for i in np.nonzero(g["fixgb"] > 0)[0]]; ys = np.array([g["fixgb"][i] for g, i in A]); fs = np.array([g["fixf"][i] for g, i in A]); q = np.searchsorted(np.quantile(ys, np.arange(.1, 1, .1)), ys); r = np.random.default_rng(SEED); nf = fs.copy()
        for b in range(10):
            m = np.nonzero(q == b)[0]; nf[m] = fs[r.permutation(m)]
        for (g, i), v in zip(A, nf): g["fixf"][i] = v
        X = X.copy(); t = np.nonzero(X[:, 3].astype(int) % 2 == 0)[0]; X[t, 2] = X[np.random.default_rng(SEED).permutation(t), 2]
    return dict(gals=Gs, X=X, a0=a0, job=job, foot=foot)
def is_train(g): return g["pos"] % 2 == 1 and g["Q"] < 3 and g["Inc"] >= 30
def is_hold(g): return g["pos"] % 2 == 0 and g["Q"] < 3 and g["Inc"] >= 30
_SUB = {"sqrt": np.sqrt, "square": np.square, "log1p": np.log1p, "exp": np.exp, "pi": math.pi}
def compile_form(eq, tier="T0"):
    s = eq.replace("^", "**"); c = compile(s, "form", "eval")
    def Hf(f, y):
        e = {"f": f, "y": y, "yg": f * y, "ys": (1 - f) * y, "one": 1.0, "two": 2.0, "pii": math.pi, **_SUB}
        v = eval(c, {"__builtins__": {}}, e) * np.ones_like(y, dtype=float)
        return v if tier == "T0" else 1 + f * v
    return Hf
def n_fitted(eq): return len(re.findall(r"(?<![A-Za-z_])\d+\.?\d*(?:[eE][-+]?\d+)?", re.sub(r"\^\s*2\b", "", eq)))
def free_path(gals, Hf, a0):
    """FG1's fit with f, y recomputed at each U. Hf None = law."""
    aa, bb, Yb, Vf, ql = [], [], [], [], []
    for g in gals:
        gb = g["GB"]; F = g["F"]; gO = (g["Vobs"] * 1e3) ** 2 / g["R"]; ok = (gb > 0) & (gO > 0) & (g["Vobs"] > 0); W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2
        p = law(np.where(gb > 0, gb, 1e-300), a0)
        if Hf is not None:
            H = Hf(F, np.where(gb > 0, gb, 1e-300) / a0); bad = (~np.isfinite(H) | (H <= 0)) & ok; p = p * np.where(bad, 1.0, H)
        else: bad = ok * False
        r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.0)) - np.log10(np.maximum(p, 1e-300)), 0.0); a = (W[None] * r * r * ok).sum(1); b = (W[None] * ok).sum(1); q = np.where(b > 0, a / np.where(b > 0, b, 1), np.inf); q = np.where(bad.any(1), np.inf, q)
        if not np.isfinite(q).any(): aa.append(0); bb.append(0); Yb.append(np.nan); Vf.append(g["Vflat"]); ql.append(False); continue
        i = int(np.argmin(q)); aa.append(a[i]); bb.append(b[i]); Yb.append(UPS[i]); Vf.append(g["Vflat"]); ql.append(g["Q"] <= 2 and g["Inc"] >= 30)
    Yb, Vf, ql = np.array(Yb), np.array(Vf), np.array(ql); nan = int(np.isnan(Yb).sum()); lo = ql & (Vf > 0) & (Vf < 100); hi = ql & (Vf > 150)
    return dict(rms=math.sqrt(sum(aa) / max(sum(bb), 1e-300)), U=float(np.nanmedian(Yb)) if (~np.isnan(Yb)).any() else float("nan"), tilt=float(np.nanmedian(Yb[lo]) - np.nanmedian(Yb[hi])) if lo.any() and hi.any() else float("nan"), invalid=nan, n=len(gals))
def fixed_rows(gals, a0):
    gb, gh, f = [], [], []
    for g in gals:
        for i in range(len(g["R"])):
            if g["R"][i] > 0 and g["Vobs"][i] > 0 and g["fixgb"][i] > 0: gb.append(g["fixgb"][i]); gh.append((g["Vobs"][i] * 1e3) ** 2 / g["R"][i]); f.append(g["fixf"][i])
    return np.array(gb), np.array(gh), np.array(f)
def fixed_path(gals, Hf, a0):
    gb, gh, f = fixed_rows(gals, a0); H = 1.0 if Hf is None else Hf(f, gb / a0); d = np.log10(gh / (law(gb, a0) * H)); return dict(rms=float(np.sqrt(np.mean(d * d))), med=float(np.median(d)))
def xcop_stat(X, Hf, a0, which=None):
    m = np.ones(len(X), bool) if which is None else (X[:, 3].astype(int) % 2 == which); A = X[m]; y = A[:, 0] / a0; H = 1.0 if Hf is None else Hf(A[:, 2], y); d = np.log10(A[:, 1] / (law(A[:, 0], a0) * H)); mean = float(d.mean()); stat = float(np.sqrt(np.mean(A[:, 4] ** 2) / len(A))); return dict(mean=mean, rms=float(np.sqrt(np.mean(d * d))), Z_real=mean / math.hypot(stat, 0.12), n=int(m.sum()))
def lt_stat(Hf, a0, job="real"):
    E = []
    for gN, gO, fg, _ in lt_rows():
        if job == "label": fg = 0.0
        H = 1.0 if Hf is None else float(Hf(np.array([fg]), np.array([gN / a0]))[0]); E.append(float(np.log10(gO) - np.log10(law(gN, a0) * H)) if H > 0 and np.isfinite(H) else float("nan"))
    md = float(np.median(E)); return dict(E=md, rmsE=float(np.std(E)), n=len(E))
def search_table(P, fixed=False):
    """Expanded rows for the Julia loss. Returns X (n,7), lgO, lgL, w, galaxy id, U id, and X-COP tail."""
    a0 = P["a0"]; tr = [g for g in P["gals"] if is_train(g)]; rows = []; gid = 0
    if fixed:
        gb, gh, f = fixed_rows(tr, a0); rows = [(f[i], gb[i] / a0, np.log10(gh[i]), np.log10(law(gb[i], a0)), 1.0, 0, 0) for i in range(len(gb))]; ng = 1
    else:
        for g in tr:
            W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2; gO = (g["Vobs"] * 1e3) ** 2 / g["R"]; any_ = False
            for u, k in enumerate(IG):
                for i in range(len(gO)):
                    if g["GB"][k, i] > 0 and gO[i] > 0 and g["Vobs"][i] > 0: rows.append((g["F"][k, i], g["GB"][k, i] / a0, np.log10(gO[i]), np.log10(law(g["GB"][k, i], a0)), W[i], gid, u)); any_ = True
            gid += any_
        ng = gid
    X = P["X"]; T = X[X[:, 3].astype(int) % 2 == 0]; R = np.array(rows, float)
    return dict(S=R, ng=ng, Xf=T[:, 2], Xy=T[:, 0] / a0, Xd=np.log10(T[:, 1] / law(T[:, 0], a0)))
def py_loss(tab, Hf, fixed=False):
    S = tab["S"]; H = Hf(S[:, 0], S[:, 1]); r = S[:, 2] - S[:, 3] - np.log10(H); W = S[:, 4]; d = tab["Xd"] - np.log10(Hf(tab["Xf"], tab["Xy"])); xm = d.mean(); xr2 = np.mean(d * d)
    if fixed: return float(np.mean(r * r) / FIX_LINE ** 2 + xm ** 2 / L_XM ** 2 + xr2 / L_XR ** 2)
    a, b, U = 0.0, 0.0, []
    for g in range(tab["ng"]):
        best = None
        for u in range(len(GRID)):
            m = (S[:, 5] == g) & (S[:, 6] == u)
            if m.any():
                A = float((W[m] * r[m] ** 2).sum()); B = float(W[m].sum())
                if best is None or A / B < best[0]: best = (A / B, A, B, u)
        a += best[1]; b += best[2]; U.append(best[3])
    lg = np.log10(np.array(GRID)[np.array(U)]); mu = float(np.median(lg)); lo, hi = math.log10(.5), math.log10(.8); dd = lo - mu if mu < lo else (mu - hi if mu > hi else 0.0)
    return float(a / b / L_S ** 2 + xm ** 2 / L_XM ** 2 + xr2 / L_XR ** 2 + (dd / 0.05) ** 2)
