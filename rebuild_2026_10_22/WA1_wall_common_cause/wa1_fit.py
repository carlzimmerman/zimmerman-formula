#!/usr/bin/env python3
"""WA1 joint fit. Criteria FROZEN_CRITERIA.md; amendments AMENDMENTS.md. python3 wa1_fit.py fit | final  (WA1_MUTATE=1: response signs flipped, separate outputs). Reads resp/*.json, hat/*.json and key caches; writes wa1_*.json/.out. Deterministic. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys, zlib
from wa1_common import *
from scipy.stats import chi2 as CH2
from scipy.optimize import least_squares
np.seterr(all="ignore")
MUT = os.environ.get("WA1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; TOUCH = 0.10; PLINE = 0.05; NM = int(os.environ.get("WA1_NM", 4000)); NS = int(os.environ.get("WA1_NS", 2000))
SOFT = lambda l: l.split("|")[0] in ("A3", "A4", "A5", "A6", "A9", "A10", "A13", "A15", "A17", "A18", "A20", "A23a", "A23b", "A24", "A26a", "A26b", "A30", "B1", "B2", "X", "K")
M3T = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_results.json")))["Ztot"]
HH = ("h0672", "h0686")
def J(*p): return json.load(open(os.path.join(*p)))
def keys_block(cid, foot):
    if cid not in KEYC: return None
    D, nm = KEYC[cid]; rk = f"R1|c0|{foot}"
    K = {t: J(D, f"{nm}_{t}", "keys.json") for t in ("g005_f034", "g005_f0615", "g0_f034")}
    X = {t: J(HERE, "cache_k2", f"{cid}_{t}", "keys.json") for t in ("tiltm1", "tilt0", "carrylo", "carryhi")}
    ks = K["g005_f034"]["R"][foot]["h0672"]["keys"]; Z = lambda d, h: np.array([d[rk]["Z"][h][k] for k in ks]); z0 = []; res = {n: [[], []] for n in NN}
    for h in HH:
        f034, f0615, g0 = Z(K["g005_f034"], h), Z(K["g005_f0615"], h), Z(K["g0_f034"], h); tm, t0, cl, ch = Z(X["tiltm1"], h), Z(X["tilt0"], h), Z(X["carrylo"], h), Z(X["carryhi"], h)
        z0.append(.5 * (f034 + f0615) + (t0 - f034)); gas = (f034 - g0) / .005
        res["gas_abs"][0].append(gas * NUIS["gas_abs"][1]); res["gas_rel"][0].append(gas * NUIS["gas_rel"][1])
        res["tilt"][0].append(.5 * (f034 - tm)); res["tilt"][1].append(.5 * (f034 + tm - 2 * t0))
        res["carry"][0].append(.5 * (ch - cl)); res["carry"][1].append(.5 * (ch + cl - 2 * f034)); res["fstar"][0].append(.5 * (f0615 - f034))
        tm_ = K["g005_f034"][rk]["tmpl"][h]; res["lens"][0].append(NUIS["lens"][1] * np.array([tm_[k][0] / tm_[k][1] for k in ks]))
    dl = (Z(K["g005_f034"], "h0686") - Z(K["g005_f034"], "h0672")) / math.log(.686 / .672); res["dist"][0] = [-NUIS["dist"][1] * dl]
    z = np.mean(z0, 0); a = {n: (np.mean(v[0], 0) if v[0] else z * 0) for n, v in res.items()}; b = {n: (np.mean(v[1], 0) if v[1] else z * 0) for n, v in res.items()}
    q = [M3T[f"{f}|{h}"] for f in ("0.034", "0.0615") for h in HH]; s = np.mean([x["s"] for x in q]); xm = np.mean([x["leak"] ** 2 + x["seed"] ** 2 for x in q]) / s ** 2; i = ks.index("G-OUT-M3"); sc = np.ones(len(ks)); sc[i] = 1 / math.sqrt(1 + xm); z = z * sc; a = {n: v * sc for n, v in a.items()}; b = {n: v * sc for n, v in b.items()}
    harness = {k: max([K[t][rk]["Z"][h][k] for t in ("g005_f034", "g005_f0615") for h in HH], key=abs) for k in ks}
    return dict(ks=ks, z=z, a=a, b=b, R=np.array(K["g005_f034"]["R"][foot]["h0672"]["R_boot"]), harness=harness, xm=float(xm))
def build(cid, foot, swap=False, drop=(), xfloor=0.0):
    r = J(HERE, "resp", f"{cid}_{foot}.json"); z0 = r["z0"]; xM = np.array(r["extra"].get("xM", []), float) if "xM" in r["extra"] else None; sX = {}; CX = None
    XS = ("0.1", "0.2", "0.3", "0.5", "0.7")
    if xM is not None and xM.size:
        C = np.ma.cov(np.ma.masked_invalid(xM), rowvar=False).filled(0.0); n = (~np.isnan(xM)).sum(0); Cs = .5 * C + .5 * np.diag(np.diag(C)); Cn = Cs / np.sqrt(np.outer(n, n)) + xfloor ** 2 * np.eye(5); sg = np.sqrt(np.diag(Cn)); CX = Cn / np.outer(sg, sg); sX = {f"X|{x}": sg[i] for i, x in enumerate(XS)}
    cval = lambda l, v: v / sX[l] if l in sX else v
    bad = lambda l: (l.startswith("A13") if swap else l.startswith("A12"))
    lines = [l for l in z0 if (SOFT(l) or (swap and l.startswith("A12"))) and not bad(l) and not any(l.startswith(d) for d in drop)]
    if cid == "UX3": lines = [l for l in lines if not l.startswith("X|")]
    lines = sorted(lines); nl = len(lines); a = np.zeros((nl, len(NN))); b = np.zeros((nl, len(NN))); z = np.array([cval(l, z0[l]) for l in lines])
    for jn, n in enumerate(NN):
        nod = r["nodes"].get(n)
        if not nod: continue
        for i, l in enumerate(lines):
            xs, ys = [], []
            for x, v in nod.items():
                if l in v["l"]: xs.append(float(x)); ys.append(cval(l, v["l"][l]) - z[i])
            if xs: m = np.linalg.lstsq(np.c_[xs, np.square(xs)], np.array(ys), rcond=None)[0]; a[i, jn], b[i, jn] = m
    kb = keys_block(cid, foot) if "K" not in drop else None
    blocks = []
    idx = {l: i for i, l in enumerate(lines)}
    if kb:
        i0 = nl; lines = lines + [f"K|{k}" for k in kb["ks"]]; z = np.r_[z, kb["z"]]; a = np.vstack([a, np.array([kb["a"][n] for n in NN]).T]); b = np.vstack([b, np.array([kb["b"][n] for n in NN]).T]); blocks.append(("keys", list(range(i0, i0 + 15)), kb["R"]))
        idx = {l: i for i, l in enumerate(lines)}
    # correlations
    Lz = len(lines); used = set(i for bk in blocks for i in bk[1])
    h = r["extra"].get("h", {}); bt = r.get("boot") or {}
    for bn in ("60-100", "100-150", "150-200", "200-250", "250-400"):
        p, q_ = f"A5|{bn}", f"A6|{bn}"
        if p in idx and q_ in idx and p in h and q_ in h and bn in bt:
            rho = min(.95, (bt[bn] ** 2 + .04 ** 2) / abs(h[p] * h[q_])); blocks.append((bn, [idx[p], idx[q_]], np.array([[1, rho], [rho, 1]]))); used |= {idx[p], idx[q_]}
    if "B2|R500" in idx and "B2|R2500" in idx: blocks.append(("B2", [idx["B2|R500"], idx["B2|R2500"]], np.array([[1, .5], [.5, 1]]))); used |= {idx["B2|R500"], idx["B2|R2500"]}
    xi = [idx[f"X|{x}"] for x in XS if f"X|{x}" in idx]
    if len(xi) == 5 and CX is not None: blocks.append(("X", xi, CX)); used |= set(xi)
    rows = []
    for nm_, ii, Rm in blocks:
        w, V = np.linalg.eigh(Rm); ok = w >= 1e-3 * w.max() if nm_ == "keys" else w > 0
        for k in np.where(ok)[0]:
            v = np.zeros(Lz); v[ii] = V[:, k] / math.sqrt(w[k]); rows.append(v)
    for i in range(Lz):
        if i not in used: v = np.zeros(Lz); v[i] = 1; rows.append(v)
    W = np.array(rows); s = -1.0 if MUT else 1.0
    return dict(lines=lines, z=z, a=a * s, b=b * s, W=W, r=r, sX=sX, kb=kb)
class Fit:
    def __init__(s, c, pscale=1.0):
        s.WA = c["W"] @ c["a"] * pscale; s.WB = c["W"] @ c["b"] * pscale ** 2; s.e0 = c["W"] @ c["z"]; s.Pi = np.linalg.inv(prior_corr()); s.P = prior_corr(); s.d = len(s.e0)
    def solve(s, e0, Pi=None, mask=None, t0=None, it=40):
        Pi = s.Pi if Pi is None else Pi; WA, WB = (s.WA, s.WB) if mask is None else (s.WA[:, mask], s.WB[:, mask]); Pi = Pi if mask is None else Pi[np.ix_(mask, mask)]; n = WA.shape[1]; t = np.zeros(n) if t0 is None else t0.copy(); lam = 1e-4
        c2 = lambda t: float(np.sum((e0 + WA @ t + WB @ (t * t)) ** 2) + t @ Pi @ t); cur = c2(t)
        for _ in range(it):
            Jc = WA + 2 * WB * t; r = e0 + WA @ t + WB @ (t * t); H = Jc.T @ Jc + Pi; g = Jc.T @ r + Pi @ t
            for __ in range(12):
                dt = np.linalg.solve(H + lam * np.eye(n), -g); new = c2(t + dt)
                if new < cur: break
                lam *= 8
            else: break
            done = cur - new < 1e-9; t = t + dt; cur = new; lam = max(lam / 4, 1e-8)
            if done: break
        return t, cur
    def marg(s, e0, t, c2):
        Jc = s.WA + 2 * s.WB * t; H = Jc.T @ Jc + s.Pi; sg, ld = np.linalg.slogdet(s.P @ H); return c2 + ld
def do_cell(cid, foot, nm=NM, ns=NS, pscale=1.0, swap=False, drop=(), full=True, c=None, xfloor=0.0):
    c = c or build(cid, foot, swap, drop, xfloor); F = Fit(c, pscale); seed = zlib.crc32(f"{cid}|{foot}|{pscale}|{swap}|{drop}|{xfloor}".encode()); rng = np.random.default_rng(seed); e0 = F.e0; c0 = float(e0 @ e0)
    best = None
    starts = [np.zeros(len(NN))] + [rng.normal(size=len(NN)) for _ in range(6)]
    for st in starts:
        t, x = F.solve(e0, t0=st)
        if best is None or x < best[1] - 1e-7: best = (t, x)
    t, cp = best; cm = F.marg(e0, t, cp); Lc = np.linalg.cholesky(F.P)
    t00, cp00 = F.solve(e0)
    MC = {}; zv = c["z"] + c["a"] * pscale @ t + c["b"] * pscale ** 2 @ (t * t); touched = (np.abs(c["a"] * pscale).max(1) + np.abs(c["b"] * pscale ** 2).max(1)) >= TOUCH; pinv = np.linalg.pinv(c["W"])
    A_, B_ = F.WA, F.WB; XP, XM, X0, MP, MU = [], [], [], [], []; xz = []
    for _ in range(nm):
        td = Lc @ rng.standard_normal(len(NN)); xi = rng.standard_normal(F.d); e = xi - (A_ @ td + B_ @ (td * td)); tt, x = F.solve(e); XP.append(x); XM.append(F.marg(e, tt, x)); X0.append(float(xi @ xi)); MP.append(np.abs(tt).max()); MU.append(np.abs((pinv @ xi)[~touched]).max() if (~touched).any() else 0.0)
    XP, XM, X0, MP, MU = map(np.array, (XP, XM, X0, MP, MU)); P = lambda arr, v: float((1 + (arr >= v).sum()) / (len(arr) + 1))
    line95 = float(np.quantile(XP, .95)); rate_p = float((XP <= line95).mean()); rate_all = float(((XP <= line95) & (MP <= 2)).mean()); rate_all_u = float(((XP <= line95) & (MP <= 2) & (MU <= 2)).mean())
    out = dict(cid=cid, foot=foot, n_lines=len(c["lines"]), dim=F.d, lines=c["lines"], chi2_0=c0, chi2_prof=cp, chi2_marg=cm, theta=t.tolist(), p_0=P(X0, c0), p_prof=P(XP, cp), p_marg=P(XM, cm), asym_p0=float(CH2.sf(c0, F.d)), asym_prof=float(CH2.sf(cp, F.d)), mock_median_prof=float(np.median(XP)), mock_95_prof=line95, mock_rate_pull_ok=rate_all, mock_rate_pull_untouched_ok=rate_all_u, z0=c["z"].tolist(), zhat=zv.tolist(), touched=touched.tolist(), restart_gap=float(cp00 - cp))
    if not full: return out
    D = c0 - cp
    # box
    def res(tb): return np.r_[e0 + A_ @ tb + B_ @ (tb * tb), np.linalg.cholesky(F.Pi).T @ tb]
    bx = least_squares(res, np.clip(t, -1.99, 1.99), bounds=(-2, 2)); out["theta_box"] = bx.x.tolist(); out["chi2_box"] = float(np.sum(bx.fun ** 2)); out["p_box_mock"] = P(XP, out["chi2_box"])
    # scramble
    Ds = []
    for _ in range(ns):
        ep = rng.permutation(e0); tt, x = F.solve(ep); Ds.append(float(ep @ ep) - x)
    Ds = np.array(Ds); out["D"] = D; out["p_scramble"] = P(Ds, D); out["scr_median_D"] = float(np.median(Ds))
    # release
    rel = {}
    for j, n in enumerate(NN):
        if np.abs(A_[:, j]).max() == 0 and np.abs(B_[:, j]).max() == 0: rel[n] = dict(D=0.0, theta=0.0, required=None, none=True); continue
        tj, xj = F.solve(e0, mask=[j]); tr, xr = F.solve(e0, Pi=np.zeros_like(F.Pi), mask=[j]); rel[n] = dict(D=c0 - xj, theta=float(tj[0]), required=float(tr[0]), D_free=c0 - xr)
    out["release"] = rel; return out
def k1_inject(foot):
    """Data = law at theta*, real rows for ups, hse, gas_abs, dist, lens, keys by response. Fit priors off. Recover."""
    c = build("LAW", foot); r = c["r"]; F = Fit(c); o = {}; tgt = {}; kbn = [l for l in c["lines"] if l.startswith("K|")]; Kset = dict(gas_rel=1.0, carry=-1.0, tilt=1.0, fstar=-1.0)
    def as_z(l, v): return v / c["sX"][l] if l in c["sX"] else v
    sg = -1.0 if MUT else 1.0
    for tag, inj in r["inj"].items():
        th = {n: 0.0 for n in NN}; th.update(inj["theta"]); inj_l = inj["l"]; tv = np.array([th[n] for n in NN]); zreal = c["z"] + sg * (c["a"] @ tv + c["b"] @ (tv * tv))
        for i, l in enumerate(c["lines"]):
            if l in inj_l: zreal[i] = as_z(l, inj_l[l])
        zobs = c["z"] - zreal; e = c["W"] @ zobs
        info = np.sum(F.WA ** 2, 0); tt, x = F.solve(e, Pi=1e-10 * np.eye(len(NN))); o[tag] = dict(injected=tv.tolist(), recovered=tt.tolist(), info=info.tolist(), ok=bool(all(abs(tt[j] - tv[j]) <= .25 for j in range(len(NN)) if info[j] >= 1)))
    return o
def k2_noise(foot):
    c = build("LAW", foot); F = Fit(c); rng = np.random.default_rng(99 + len(foot)); tv = np.array([(1 if i % 2 == 0 else -1) * .8 for i in range(len(NN))]); Ie = F.WA.T @ F.WA; S = np.linalg.solve(Ie + F.Pi, Ie); ex = S @ tv; R = []
    for _ in range(400):
        xi = rng.standard_normal(F.d); e = xi - (F.WA @ tv + F.WB @ (tv * tv)); R.append(F.solve(e)[0])
    m = np.mean(R, 0); return dict(mean=m.tolist(), expected=ex.tolist(), maxdiff=float(np.abs(m - ex).max()), ok=bool(np.abs(m - ex).max() <= .15))
def k3_cal(cid, foot):
    c = build(cid, foot); F = Fit(c); rng = np.random.default_rng(7 + len(cid)); Lc = np.linalg.cholesky(F.P)
    def mk(n):
        o = []
        for _ in range(n):
            td = Lc @ rng.standard_normal(len(NN)); xi = rng.standard_normal(F.d); e = xi - (F.WA @ td + F.WB @ (td * td)); o.append(F.solve(e)[1])
        return np.array(o)
    a, b = mk(4000), mk(2000); q = float(np.quantile(a, .95)); fr = float((b > q).mean()); return dict(frac=fr, ok=bool(.03 <= fr <= .07))
if __name__ == "__main__":
    st = sys.argv[1]; cids = [x for x in REAL]
    if st == "fit":
        o = {}
        for cid in cids + ["CAL"]:
            for f in FEET:
                if not os.path.exists(os.path.join(HERE, "resp", f"{cid}_{f}.json")): continue
                t = do_cell(cid, f, nm=1, full=False)["theta"]; o[f"{cid}|{f}"] = {n: float(v) for n, v in zip(NN, t)}
        json.dump(o, open(os.path.join(HERE, f"wa1_thetahat{TAG}.json"), "w"), indent=1, sort_keys=True)
    elif st == "k":
        o = dict(K1={f: k1_inject(f) for f in FEET}, K2={f: k2_noise(f) for f in FEET})
        if not MUT: o["K3"] = {f"{c}|{f}": k3_cal(c, f) for c in ("LAW", "MX1") for f in FEET}
        json.dump(o, open(os.path.join(HERE, f"wa1_checks{TAG}.json"), "w"), indent=1, sort_keys=True); print(json.dumps({k: {kk: (vv if k != "K1" else {t: x["ok"] for t, x in vv.items()}) for kk, vv in v.items()} for k, v in o.items()}, indent=0, default=float)[:3000])
    elif st == "final":
        R = {}
        for cid in cids + ["CAL"]:
            for f in FEET:
                R[f"{cid}|{f}"] = do_cell(cid, f, nm=(NM if cid != "CAL" else 1000), ns=(NS if cid != "CAL" else 500)); print(cid, f, round(R[f"{cid}|{f}"]["chi2_prof"], 2), flush=True)
        S = {}
        for cid in cids:
            for f in FEET:
                S[f"{cid}|{f}"] = dict(x2=do_cell(cid, f, nm=1000, pscale=2.0, full=False), a12=do_cell(cid, f, nm=1000, swap=True, full=False), nodisp=do_cell(cid, f, nm=1000, drop=("A5", "A6", "A10", "A15", "A18", "A23a", "A23b", "A26a", "B2", "X", "K"), full=False), xfl=do_cell(cid, f, nm=1000, xfloor=.05, full=False), nox=do_cell(cid, f, nm=1000, drop=("X",), full=False))
        json.dump(dict(cells=R, sens=S), open(os.path.join(HERE, f"wa1_results{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
