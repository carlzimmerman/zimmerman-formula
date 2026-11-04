#!/usr/bin/env python3
"""NV2 core (NV1 nv1_core.py copied with attribution; E1 from nv2_env): NP2's admissible Gaussian-process rule (../NP2_admissible_rule/np2_core.py, imported read-only) on the arm L3+E (log y, log ell, f, E),
E held fixed along the admissibility directions; gates 1-4 on rows that have E; CX1 centre rows with their sub-line (NP1's cx_rows, copied with `sub` kept);
the sign test (FROZEN_CRITERIA step 1); plants. kappa = 1/2 FITTED; not theory closed."""
import math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
from scipy.stats import qmc, spearmanr
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); NP2D = os.path.join(RB, "NP2_admissible_rule")
sys.path.insert(0, HERE); sys.path.insert(0, NP2D)
import np2_core as N
import nv2_env as V
C = N.C; DD = C.DD; ARM = "L3E"
SIG_E1 = V.SIG["E1"]   # FROZEN_CRITERIA: median per-system sigma_E1 over systems with E1
WIDE_E = dict(E1=(-7.0, 1.0)); CUR = {"cand": "E1"}

# ---------- NP2 hooks for the 4-leaf arm (NP2's own code paths otherwise unchanged)
_ffb, _wp = N.feats_from_box, N.wide_points
def feats_from_box(P, arm): return P.copy() if arm == ARM else _ffb(P, arm)
def wide_points(arm, n=2 ** 16, seed=20261104):
    if arm != ARM: return _wp(arm, n, seed)
    lo = [N.WIDE["logy"][0], N.WIDE["logell"][0], 0.0, WIDE_E[CUR["cand"]][0]]; hi = [N.WIDE["logy"][1], N.WIDE["logell"][1], 1.0, WIDE_E[CUR["cand"]][1]]
    return qmc.scale(qmc.Sobol(4, scramble=True, seed=seed).random(n), lo, hi)
N.feats_from_box = feats_from_box; N.wide_points = wide_points

# ---------- rows and E
NAMES = dict(S=V.sl1_sparc_names(), X=V.xcop_names(), LT=V.sl1_lt_names())
def rows_E(A, kind, c, emap=None):
    """E per BF1 row; emap: optional {(kind, name): E} override (shuffles)."""
    idx = A[:, 4].astype(int); nm = NAMES[kind]; f = {"S": V.sparc_E, "X": V.xcop_E, "LT": V.lt_E}[kind]; out = np.empty(len(A))
    for i in np.unique(idx):
        n = nm[i]; out[idx == i] = emap.get((kind, n), np.nan) if emap is not None else f(n, c)
    return out, np.array([nm[i] for i in idx])
def featsE(A, E): return np.column_stack([C.feats(A, "L3"), E])
def target(A, a0, g=None): return C.target(A, a0, g)
BLOCKS = dict(XT=(C.XT, "X"), ST=(C.ST, "S"), XH=(C.XH, "X"), SH=(C.SH, "S"), LT=(C.LTA, "LT"))
def all_E(c, emap=None): return {k: rows_E(A, kd, c, emap) for k, (A, kd) in BLOCKS.items()}
def system_table(c):
    """{(kind, name): E} over BF1's systems with finite E (for shuffles)."""
    o = {}
    for kd, nm in NAMES.items():
        f = {"S": V.sparc_E, "X": V.xcop_E, "LT": V.lt_E}[kd]
        for n in nm:
            e = f(n, c)
            if np.isfinite(e): o[(kd, n)] = float(e)
    return o
def shuffled(tab, seed):
    k = sorted(tab); v = np.array([tab[q] for q in k]); p = np.random.default_rng(seed).permutation(len(k)); return {q: float(v[p[i]]) for i, q in enumerate(k)}

def train_set(c, Eb, a0, gX=None, gS=None):
    EX, _ = Eb["XT"]; ES, _ = Eb["ST"]; F = np.vstack([featsE(C.XT, EX), featsE(C.ST, ES)]); t = np.r_[target(C.XT, a0, gX), target(C.ST, a0, gS)]
    cls = np.r_[np.zeros(len(C.XT), int), np.ones(len(C.ST), int)]; sid = np.r_[C.XT[:, 4].astype(int), C.ST[:, 4].astype(int)]; ok = np.all(np.isfinite(F), 1) & np.isfinite(t)
    return F[ok], t[ok], cls[ok], sid[ok], dict(n_train=int(ok.sum()), n_dropped=int((~ok).sum()), xcop_dropped=int((~ok[:len(C.XT)]).sum()), sparc_dropped=int((~ok[len(C.XT):]).sum()))

def gates14E(rule, a0, Eb, plant=None):
    """NP1's gates14 on the rows with E; SPARC lines 1.05 x the REAL law's rms on the same rows."""
    P = plant or {}; o = {}; rms = C.rms
    def d(k):
        A = BLOCKS[k][0]; E = Eb[k][0]; m = np.isfinite(E); g = P.get(k); g = g[m] if g is not None else None
        return target(A[m], a0, g) - rule.m(featsE(A[m], E[m])), A[m]
    (dx, _), (ds, As), (dxh, _), (dsh, Ah), (dl, _) = d("XT"), d("ST"), d("XH"), d("SH"), d("LT")
    lS, lH = C.SF * rms(target(As, a0)), C.SF * rms(target(Ah, a0))
    o["n"] = {k: [int(np.isfinite(Eb[k][0]).sum()), len(Eb[k][0])] for k in BLOCKS}
    o["g1"] = dict(mean=float(dx.mean()), rms=rms(dx), ok=bool(np.all(np.isfinite(dx)) and abs(dx.mean()) <= C.XM and rms(dx) <= C.XR))
    o["g2"] = dict(rms=rms(ds), med=float(np.median(ds)), line=lS, ok=bool(np.all(np.isfinite(ds)) and rms(ds) <= lS and abs(np.median(ds)) <= C.SM))
    o["g3S"] = dict(rms=rms(dsh), med=float(np.median(dsh)), line=lH, ok=bool(np.all(np.isfinite(dsh)) and rms(dsh) <= lH and abs(np.median(dsh)) <= C.SM))
    o["g3X"] = dict(mean=float(dxh.mean()), rms=rms(dxh), ok=bool(np.all(np.isfinite(dxh)) and abs(dxh.mean()) <= C.XM and rms(dxh) <= C.XR))
    o["g3"] = dict(ok=o["g3S"]["ok"] and o["g3X"]["ok"])
    o["g4"] = dict(med=float(np.median(dl)) if len(dl) else float("nan"), n=len(dl), ok=bool(len(dl) and np.all(np.isfinite(dl)) and abs(np.median(dl)) <= C.LTT))
    return o
def g14s(o): return (f"G1 {o['g1']['mean']:+.3f}/{o['g1']['rms']:.3f} {'P' if o['g1']['ok'] else 'F'} | G2 {o['g2']['rms']:.3f}/{o['g2']['line']:.3f} med {o['g2']['med']:+.3f} {'P' if o['g2']['ok'] else 'F'} | "
                    f"G3 S {o['g3S']['rms']:.3f}/{o['g3S']['line']:.3f} med {o['g3S']['med']:+.3f} {'P' if o['g3S']['ok'] else 'F'}, X {o['g3X']['mean']:+.3f}/{o['g3X']['rms']:.3f} {'P' if o['g3X']['ok'] else 'F'} | G4 {o['g4']['med']:+.3f} (n {o['g4']['n']}) {'P' if o['g4']['ok'] else 'F'} | rows with E {o['n']}")

# ---------- plants (NP1's noise draw, NP2's admissible plant; FROZEN_CRITERIA controls 4, 5)
def plant_adm(a0, noise=True, boost=None):
    """g = law(g_b, a0 (1 + 0.5 f)) [x 10^(boost[k])]; SPARC rows at NP1's error draw (seed 20261103 + parity)."""
    P = {}
    for k, (A, _) in BLOCKS.items():
        P[k] = C.law(A[:, 0], a0 * (1 + 0.5 * A[:, 3]))
        if boost is not None: P[k] = P[k] * 10 ** boost[k]
    if noise:
        for k, A, par in (("ST", C.ST, 1), ("SH", C.SH, 0)):
            e = DD.sparc_err(par); r = np.random.default_rng(20261103 + par); P[k] = P[k] * 10 ** (e * r.standard_normal(len(e)))
    return P

# ---------- CX1 centre rows with sub-line (NP1's cx_rows, copied; `sub` and sd kept)
def cx_rows(foot):
    sys.path.insert(0, C.CXD); import cx1_rows as CR
    S = [s for s in CR.systems(foot) if s.line in C.CX_LINES]; MU, COV, META, _ = CR.mc(S, foot); a0 = C.FOOT[foot]; R = []
    sdmap = {(si, k): math.sqrt(COV[j][4, 4]) for j, (si, k) in enumerate(META)}
    for si, s in enumerate(S):
        r = np.asarray(s.rows["r"], float); gb = np.asarray(s.rows["gb"], float); gg = np.asarray(s.rows["gg"], float); go = np.asarray(s.rows["gobs"], float)
        for k in range(len(r)):
            if (si, k) not in sdmap: continue
            y = gb[k] / C.A0C; ell = r[k] * C.A0C / C.CL ** 2; f = min(1.0, max(0.0, gg[k] / gb[k]))
            R.append(dict(line=s.line, sub=s.sub, name=s.name, lE=float(s.lE), y=y, ell=ell, f=f, logB=float(np.log10(go[k] / C.law(gb[k], a0))), sd=sdmap[(si, k)], gb=gb[k], gg=gg[k], r=r[k]))
    return R
_X1BY = None
def cx_E(q, c):
    """E1 for a CX1 row (NV2): IC 1613's LITTLE THINGS row through the SPARC alias (none -> NaN); dwarfs NaN; lens bins from Step 0 (NaN unless graded); groups NaN."""
    if q["line"] == "IC1613" and q["sub"] == "LT": return V.lt_E(q["name"], c)
    if q["line"] == "L": return V.lens_bin_E(int(str(q["name"]).replace("bin", "")) - 1)
    return float("nan")
def cx_F(R, E): return np.column_stack([np.log10([q["y"] for q in R]), np.log10([q["ell"] for q in R]), [q["f"] for q in R], E])

# ---------- the sign test (FROZEN_CRITERIA step 1)
from scipy.stats import rankdata
GROUPS = dict(T10=lambda q: q["line"] == "IC1613" and q["sub"] == "LT", TUFD=lambda q: q["line"] == "Dw-UFD", TDW=lambda q: q["line"] == "Dw", T30=lambda q: q["line"] == "L")
class SignTest:
    """Fixed part (NP2 residuals, neighbours in NP2's kernel metric) computed once; run(Etrain, Ecx) evaluates the test for any E assignment (real or shuffled)."""
    def __init__(s, c, np2rule, a0, cx, Etrain_sys):
        s.c = c; Ftr = np.vstack([C.feats(C.XT, "L3"), C.feats(C.ST, "L3")]); r = np.r_[target(C.XT, a0), target(C.ST, a0)] - np2rule.m(Ftr)
        kind = np.r_[np.full(len(C.XT), "X"), np.full(len(C.ST), "S")]; nm = np.r_[[NAMES["X"][i] for i in C.XT[:, 4].astype(int)], [NAMES["S"][i] for i in C.ST[:, 4].astype(int)]]
        s.rowkey = list(zip(kind, nm)); s.keys = sorted(set(s.rowkey)); s.sm = {q: float(np.mean(r[(kind == q[0]) & (nm == q[1])])) for q in s.keys}
        s.Ztr = np2rule.std(Ftr) / np2rule.ell; s.cx = cx
        Fcx = np.column_stack([np.log10([q["y"] for q in cx]), np.log10([q["ell"] for q in cx]), [q["f"] for q in cx]]); s.rcx = np.array([q["logB"] for q in cx]) - np2rule.m(Fcx); s.Zcx = np2rule.std(Fcx) / np2rule.ell
        s.cxkey = [(q["line"], q["sub"], q["name"]) for q in cx]; s.G = {}
        okE = np.array([np.isfinite(Etrain_sys.get(k, np.nan)) for k in s.rowkey]); s.okE = okE; idxE = np.nonzero(okE)[0]
        for g, sel in GROUPS.items():
            ii = np.array([i for i, q in enumerate(cx) if sel(q)], int)
            if not len(ii): s.G[g] = None; continue
            nsys = len({cx[i]["name"] for i in ii}); med = float(np.median(s.rcx[ii])); sd = float(np.median([cx[i]["sd"] for i in ii]) / math.sqrt(nsys))
            nb = set()
            for i in ii:
                if len(idxE): d = np.sqrt(((s.Ztr[idxE] - s.Zcx[i]) ** 2).sum(1)); nb.update(idxE[np.argsort(d)[:50]].tolist())
            s.G[g] = dict(ii=ii, nsys=nsys, med=med, sd=sd, want=int(np.sign(med)) if abs(med) > 2 * sd else 0, nb=np.array(sorted(nb), int))
    def run(s, Etr, Ecx, nperm=2000, seed=20261107):
        o = {}; sk = [q for q in s.keys if np.isfinite(Etr.get(q, np.nan))]; o["train_systems_with_E"] = len(sk); o["train_systems"] = len(s.keys)
        if len(sk) >= 5:
            x = rankdata([Etr[q] for q in sk]); y = rankdata([s.sm[q] for q in sk]); x = (x - x.mean()) / x.std(); y = (y - y.mean()) / y.std(); rho = float(np.mean(x * y))
            g = np.random.default_rng(seed); P = np.array([g.permutation(len(x)) for _ in range(nperm)]); pr = (x[P] * y[None, :]).mean(1); p = float((np.sum(np.abs(pr) >= abs(rho) - 1e-12) + 1) / (nperm + 1))
            o.update(rho=rho, p=p, s_train=int(np.sign(rho)) if p < 0.05 else 0)
        else: o.update(rho=None, p=None, s_train=None)
        Erow = np.array([Etr.get(k, np.nan) for k in s.rowkey]); Ec = np.array([Ecx.get(k, np.nan) for k in s.cxkey]); sig = V.SIG.get(s.c, SIG_E1); G = {}
        for gname, d in s.G.items():
            if d is None: G[gname] = dict(status="NO ROWS"); continue
            jj = d["ii"][np.isfinite(Ec[d["ii"]])]; q = dict(n_rows=len(d["ii"]), n_systems=d["nsys"], n_with_E=len(jj), median_r=d["med"], sd=d["sd"], want=d["want"])
            nb = d["nb"][np.isfinite(Erow[d["nb"]])] if len(d["nb"]) else d["nb"]
            if not len(jj) or not len(nb) or o["s_train"] is None: q["status"] = "NOT COMPUTABLE"; G[gname] = q; continue
            dE = float(np.median(Ec[jj]) - np.median(Erow[nb])); q.update(E_group=float(np.median(Ec[jj])), E_neigh=float(np.median(Erow[nb])), n_neigh=len(nb), dE=dE, sigma_E=sig)
            sep = bool(q["want"] != 0 and o["s_train"] != 0 and abs(dE) > sig and int(np.sign(dE)) * o["s_train"] == q["want"]); q["status"] = "SEPARATES" if sep else "DOES NOT SEPARATE"; G[gname] = q
        o["groups"] = G; comp = [g for g in G.values() if g.get("status") in ("SEPARATES", "DOES NOT SEPARATE") and g["want"] != 0]
        wants = {g["want"] for g in comp}; ns = sum(g["status"] == "SEPARATES" for g in comp)
        o["label"] = "NOT COMPUTABLE" if not comp else ("SEPARATES" if ns == len(comp) and wants == {-1, 1} else ("PARTIAL" if ns else "DOES NOT SEPARATE")); return o
