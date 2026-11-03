#!/usr/bin/env python3
"""CX1_leaf_collision: collisions in BF1/SY1 leaf space. Modes: controls (K checks, smooth null, planted class), real, mutate.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 10 python3 -I cx1.py <mode>. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cx1_rows as C
from scipy.stats import norm as NORM
MODE = sys.argv[1] if len(sys.argv) > 1 else "real"
FEET = ("canonical", "alt")
ARMS = {"L3": [0, 1, 2], "L5": [0, 1, 2, 3], "L3+E": [0, 1, 2, 5], "L5+E": [0, 1, 2, 3, 5]}
POINT_STANDIN = ("LT", "G", "Dw", "Dw-UFD", "IC1613")      # single-radius systems: SY1's s stand-in, L5 NOT GRADED
TOL = {"S": 0.03, "X": 0.05, "L": 0.05, "LT": 0.10, "G": 0.10, "Dw-UFD": 0.10, "Dw": 0.10, "IC1613": 0.10, "S_odd": 0.03, "S_even": 0.03}
MINSYS = {"IC1613": 1}
GAP = os.environ.get("CX1_GAP", "marginal")   # AMENDMENT_A1: marginal gap primary, conditional reported
FLOOR = 0.01; NBOOT = 200; BSEED = 20261104; MSEED = 20261105
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

class Data:
    def __init__(s, S, MU, COV, META):
        s.S, s.MU, s.COV, s.META = S, MU, COV, META
        s.line = np.array([S[i].line for i, k in META]); s.name = np.array([S[i].name for i, k in META]); s.sub = np.array([S[i].sub for i, k in META])
        sids = sorted({S[i].sid for i, k in META}); ix = {x: n for n, x in enumerate(sids)}; s.sys = np.array([ix[S[i].sid] for i, k in META]); s.sidname = sids
        s.k = np.array([k for i, k in META])

def rows_for(D, arm, variant, MU=None, lines=None):
    MU = D.MU if MU is None else MU; L = D.line if lines is None else lines; idx = ARMS[arm]
    m = np.all(np.isfinite(MU[:, idx + [4]]), 1)
    if arm.startswith("L5"): m &= ~np.isin(D.line, POINT_STANDIN)
    if variant == "noX": m &= D.line != "X"
    if variant == "noLG": m &= ~np.isin(D.line, ("L", "G"))
    return m

def scan(D, arm, mask, MU=None, COV=None, lines=None):
    """All cross-system pairs: near pairs (d_L <= 1) with conditional gap m (i minus j), v, z; and min d_L per cross-line pair."""
    MU = D.MU if MU is None else MU; COV = D.COV if COV is None else COV; L = D.line if lines is None else lines
    li = ARMS[arm]; q = li + [4]; idx = np.nonzero(mask)[0]; M = MU[np.ix_(idx, q)]; Cv = COV[np.ix_(idx, q, q)].copy()
    nl = len(li)
    for a in range(nl): Cv[:, a, a] = np.maximum(Cv[:, a, a], FLOOR ** 2)
    sy = D.sys[idx]; ln = L[idx]; sdl = np.sqrt(np.stack([Cv[:, a, a] for a in range(nl)], 1))
    I, J, DL, MM, VV, MC, VC = [], [], [], [], [], [], []; mind = {}
    for a in range(len(idx) - 1):
        b = np.arange(a + 1, len(idx)); b = b[sy[b] != sy[a]]
        if not len(b): continue
        dlt = M[a] - M[b]; cross = ln[b] != ln[a]
        pre = np.all(np.abs(dlt[:, :nl]) <= np.sqrt(sdl[a] ** 2 + sdl[b] ** 2) + 1e-12, 1) | cross
        b = b[pre]; dlt = dlt[pre]; cross = cross[pre]
        if not len(b): continue
        Sg = Cv[a] + Cv[b]; Sll = Sg[:, :nl, :nl]; SlB = Sg[:, :nl, nl]
        sol = np.linalg.solve(Sll, np.stack([dlt[:, :nl], SlB], 2))          # Sll^-1 [Delta_l, Sigma_lB]
        d2 = np.einsum("nk,nk->n", dlt[:, :nl], sol[:, :, 0]); m = dlt[:, nl] - np.einsum("nk,nk->n", SlB, sol[:, :, 0])
        v = Sg[:, nl, nl] - np.einsum("nk,nk->n", SlB, sol[:, :, 1]); dL = np.sqrt(np.maximum(d2, 0))
        for t in np.nonzero(cross)[0]:
            key = tuple(sorted((ln[a], ln[b[t]])))
            if key not in mind or dL[t] < mind[key][0]: mind[key] = (float(dL[t]), int(idx[a]), int(idx[b[t]]))
        n = dL <= 1.0
        if n.any():
            I.append(np.full(n.sum(), idx[a])); J.append(idx[b[n]]); DL.append(dL[n]); MC.append(m[n]); VC.append(np.maximum(v[n], 1e-12))
            MM.append(dlt[n, nl]); VV.append(np.maximum(Sg[n, nl, nl], 1e-12))
    cat = lambda x, dt=float: np.concatenate(x) if x else np.zeros(0, dt)
    I, J, DL, MM, VV, MC, VC = cat(I, int), cat(J, int), cat(DL), cat(MM), cat(VV), cat(MC), cat(VC)
    if GAP == "conditional": MM, VV, MC, VC = MC, VC, MM, VV
    return dict(I=I, J=J, dL=DL, m=MM, v=VV, z=np.abs(MM) / np.sqrt(VV), m_other=MC, v_other=VC, z_other=np.abs(MC) / np.sqrt(VC), mind=mind)

def line_level(D, R, lines=None, seed=BSEED, MU=None, arm="L3"):
    """AMENDMENT_A1: per line pair, weighted regression over near pairs of the boost gap (A minus B) on the leaf gap (A minus B) with an intercept;
    the intercept is the line offset at equal leaves, so a smooth rule's local gradient times a systematic leaf offset is not read as a collision."""
    L = D.line if lines is None else lines; MU = D.MU if MU is None else MU; li = ARMS[arm]; la, lb = L[R["I"]], L[R["J"]]; out = {}
    rng = np.random.default_rng(seed)
    for A, B in sorted({tuple(sorted((x, y))) for x, y in zip(la, lb) if x != y}):
        s = ((la == A) & (lb == B)) | ((la == B) & (lb == A)); sg = np.where(la[s] == A, 1.0, -1.0)
        m = R["m"][s] * sg; w = 1 / R["v"][s]; sa = np.where(sg > 0, D.sys[R["I"][s]], D.sys[R["J"][s]]); sb = np.where(sg > 0, D.sys[R["J"][s]], D.sys[R["I"][s]])
        X = np.column_stack([np.ones(s.sum()), (MU[R["I"][s]][:, li] - MU[R["J"][s]][:, li]) * sg[:, None]])
        ua, ia = np.unique(sa, return_inverse=True); ub, ib = np.unique(sb, return_inverse=True)
        def fit(ww):
            sw = np.sqrt(ww); c, *_ = np.linalg.lstsq(X * sw[:, None], m * sw, rcond=None); return float(c[0])
        npar = X.shape[1]; okn = s.sum() >= 2 * npar
        mean = fit(w) if okn else float(np.sum(w * m) / np.sum(w)); raw = float(np.sum(w * m) / np.sum(w)); bs = []
        for _ in range(NBOOT):
            ca = rng.multinomial(len(ua), np.ones(len(ua)) / len(ua)); cb = rng.multinomial(len(ub), np.ones(len(ub)) / len(ub)); ww = w * ca[ia] * cb[ib]
            if (ww > 0).sum() >= 2 * npar: bs.append(fit(ww))
        sd = float(np.std(bs)) if len(bs) > 20 else float("inf"); tol = TOL[A] + TOL[B]
        enough = okn and len(ua) >= MINSYS.get(A, 3) and len(ub) >= MINSYS.get(B, 3)
        coll = enough and abs(mean) >= 3 * sd and abs(mean) > tol; und = enough and (not coll) and abs(mean) > tol
        out[f"{A}|{B}"] = dict(n_pairs=int(s.sum()), n_sys=[int(len(ua)), int(len(ub))], mean_m=round(mean, 4), raw_mean=round(raw, 4), sd=round(sd, 4), tol=tol,
                               collision=bool(coll), undetermined=bool(und), nsig=round(abs(mean) / sd, 2) if 0 < sd < float("inf") else None)
    return out

def point_level(D, R, lines=None):
    L = D.line if lines is None else lines; N = len(R["z"]); zl = float(NORM.isf(0.025 / max(N, 1))); thr = max(3.0, zl)
    cross = L[R["I"]] != L[R["J"]]; c3 = R["z"] >= 3; st = R["z"] >= thr
    und = cross & (np.abs(R["m"]) >= 0.3) & (~st)
    return dict(N_near=N, z_LEE=round(zl, 3), n_coll_cross=int((c3 & cross).sum()), n_strong_cross=int((st & cross).sum()), n_coll_within=int((c3 & ~cross).sum()),
                n_strong_within=int((st & ~cross).sum()), n_undet_cross=int(und.sum()), strong_cross_idx=np.nonzero(st & cross)[0], thr=thr)

def analyze(D, arm, variant, MU=None, COV=None, lines=None):
    MU = (D.MU if MU is None else MU).copy()
    if variant == "Xshift": MU[D.line == "X", 4] -= 0.12
    mask = rows_for(D, arm, variant, MU, lines); R = scan(D, arm, mask, MU, COV, lines)
    return R, point_level(D, R, lines), line_level(D, R, lines, MU=MU, arm=arm), int(mask.sum())

def load(foot, ups="U50", amult=1.0):
    S = C.systems(foot, ups, amult); MU, COV, META, drop = C.mc(S, foot); return Data(S, MU, COV, META), drop

def F_truth(D, arm, which):
    MU = D.MU; y = 10 ** MU[:, 0]
    if which == "F1": return np.log10((1 + MU[:, 2]) * np.log1p(1 / y))
    return 0.1 * np.nan_to_num(MU[:, ARMS[arm]]).sum(1)      # F2 on the arm's own leaves only (AMENDMENT_A1 item 3)

def synth(D, arm, which, seed, delta=0.0):
    """Truth at each row's mean leaves, log B = F, plus one draw from the row's own covariance (E only where finite)."""
    rng = np.random.default_rng(seed); MU = D.MU.copy(); MU[:, 4] = F_truth(D, arm, which)
    if delta: MU[(D.line == "S") & (D.sub == "odd"), 4] += delta
    for r in range(len(MU)):
        q = [0, 1, 2, 3, 4] + ([5] if np.isfinite(MU[r, 5]) else []); Cq = D.COV[r][np.ix_(q, q)]
        w, V = np.linalg.eigh(Cq); MU[r, q] += V @ (np.sqrt(np.maximum(w, 0)) * rng.standard_normal(len(q)))
    return MU

def summ_line(LL): return {k: v for k, v in LL.items() if v["collision"] or v["undetermined"]}

def controls():
    res = {}
    P("CX1 controls (read before the real result). kappa = 1/2 FITTED; not theory closed.")
    # K units: SY1's own leaves on BF1's train rows
    sys.path.insert(0, os.path.join(C.RB, "SY1_free_constant_law_search")); import sy1_data as SD
    D0, _ = load("canonical"); names = sorted(g["name"] for g in C.R.SP.load_gal()); xn = sorted(c["name"] for c in C.R.C.xcop_load())
    cen = {}
    for s in D0.S:
        if s.line not in ("S", "X"): continue
        r = np.asarray(s.rows["r"]); gb = np.asarray(s.rows["gb"]); gg = np.asarray(s.rows["gg"]); sl = C.slope_1d(gb, r)
        cen[(s.line, s.name)] = [(gb[k] / C.A0C, r[k] * C.A0C / C.CL ** 2, min(1, max(0, gg[k] / gb[k])), sl[k]) for k in range(len(r))]
    dev = {"X": [], "S": []}; miss = {"X": 0, "S": 0}
    for c, A in (("X", SD.XT), ("S", SD.ST)):
        L = SD._cols(A)
        for n in range(len(A)):
            nm = (xn if c == "X" else names)[int(A[n, 4])]; ell = L["ell"][n]
            cand = [a for a in cen.get((c, nm), []) if abs(a[1] / ell - 1) < 1e-6]
            if not cand: miss[c] += 1; continue
            a = cand[0]; dev[c].append([abs(a[0] / L["y"][n] - 1), abs(a[1] / ell - 1), abs(a[2] - L["f"][n]), abs(a[3] - L["s"][n])])
    K = {c: dict(n=len(v), unmatched=miss[c], max_dev_y_ell_f_s=[float(x) for x in np.max(np.array(v), 0)] if v else None) for c, v in dev.items()}
    P("K units vs SY1 build('real') rows (X-COP train + SPARC odd train): ", json.dumps(K))
    # law known answers at the centre
    xs = np.concatenate([np.log10(s.rows["gobs"] / C.law(s.rows["gb"], C.A0C)) for s in D0.S if s.line == "X"])
    lt = np.concatenate([np.log10(s.rows["gobs"] / C.law(s.rows["gb"], C.A0C)) for s in D0.S if s.sub == "LT"])
    KA = dict(xcop_mean_logB=round(float(xs.mean()), 4), record=0.4675, lt_median_logB=round(float(np.median(lt)), 4), record_lt=-0.0252,
              pass_=bool(abs(xs.mean() - 0.4675) <= 0.005 and abs(np.median(lt) + 0.0252) <= 0.005))
    P("K known answer (centre values, canonical):", json.dumps(KA)); res["K"] = dict(units=K, known=KA)
    res["nulls"] = {}; res["planted"] = {}
    for foot in FEET:
        D, drop = load(foot); P(f"\n== {foot}: rows {len(D.MU)}, dropped {len(drop)}")
        for arm in ARMS:
            NL = {}
            for which in ("F1", "F2"):
                cnt = []
                for sd in range(20):
                    MU = synth(D, arm, which, 1000 + sd); R, PL, LL, n = analyze(D, arm, "all", MU)
                    cnt.append(dict(strong_cross=PL["n_strong_cross"], strong_within=PL["n_strong_within"], coll3_cross=PL["n_coll_cross"], line_coll=sum(v["collision"] for v in LL.values()),
                                    line_coll_pairs=[k for k, v in LL.items() if v["collision"]], N_near=PL["N_near"]))
                seeds_pt = sum(c["strong_cross"] > 0 for c in cnt); seeds_ln = sum(c["line_coll"] > 0 for c in cnt)
                NL[which] = dict(seeds_with_strong_point_cross=seeds_pt, seeds_with_line_collision=seeds_ln, ok_point=seeds_pt <= 1, ok_line=seeds_ln <= 1,
                                 coll3_cross_p99=float(np.percentile([c["coll3_cross"] for c in cnt], 99)), per_seed=cnt)
                P(f"  null {arm:5s} {which}: seeds with strong cross point {seeds_pt}/20, with line collision {seeds_ln}/20, z>=3 cross p99 {NL[which]['coll3_cross_p99']:.0f}, N_near median {int(np.median([c['N_near'] for c in cnt]))}")
            res["nulls"][f"{foot}|{arm}"] = NL
            lines = np.where(D.line == "S", np.where(D.sub == "odd", "S_odd", "S_even"), D.line); PLT = {}
            for delta in (0.3, 1.0):
                MU = synth(D, arm, "F1", 2000, delta); R, PL, LL, n = analyze(D, arm, "all", MU, lines=lines)
                k = "S_even|S_odd"; LLk = LL.get(k, {})
                PLT[str(delta)] = dict(line=LLk, strong_within_or_cross=PL["n_strong_cross"], coll3_cross=PL["n_coll_cross"],
                                       found=bool(LLk.get("collision")) if delta == 0.3 else PL["n_strong_cross"] > 0)
                P(f"  planted {arm:5s} delta {delta}: S_odd|S_even line {LLk.get('mean_m')} +- {LLk.get('sd')} coll {LLk.get('collision')}; strong cross points {PL['n_strong_cross']} -> found {PLT[str(delta)]['found']}")
            if arm == "L3":
                MU = synth(D, arm, "F1", 2001); MU[D.sub == "LT", 4] += 0.5; R, PL, LL, n = analyze(D, arm, "all", MU)
                PLT["LT+0.5"] = dict(line={k: v for k, v in LL.items() if "LT" in k}, strong_cross=PL["n_strong_cross"])
                P(f"  planted L3 LT+0.5 (reported): LT|S {LL.get('LT|S')}")
            res["planted"][f"{foot}|{arm}"] = PLT
            P(f"  rss {rss():.2f} GB")
    return res

def table_rows(D, R, PL, k=12, lines=None):
    L = D.line if lines is None else lines; ii = PL["strong_cross_idx"]
    cross = np.nonzero(L[R["I"]] != L[R["J"]])[0]; order = cross[np.argsort(-R["z"][cross])][:k]
    T = []
    for t in order:
        i, j = R["I"][t], R["J"][t]
        def row(a): sd = np.sqrt(np.diag(D.COV[a])); return dict(line=str(L[a]), name=str(D.name[a]), k=int(D.k[a]), log_y=round(float(D.MU[a, 0]), 3), log_ell=round(float(D.MU[a, 1]), 3),
                                                              f=round(float(D.MU[a, 2]), 3), s=round(float(D.MU[a, 3]), 3), E=None if not np.isfinite(D.MU[a, 5]) else round(float(D.MU[a, 5]), 2),
                                                              log_B=round(float(D.MU[a, 4]), 3), sd_log_B=round(float(sd[4]), 3))
        T.append(dict(a=row(i), b=row(j), dL=round(float(R["dL"][t]), 3), m=round(float(R["m"][t]), 3), sd_m=round(float(np.sqrt(R["v"][t])), 3), z=round(float(R["z"][t]), 2),
                      strong=bool(R["z"][t] >= PL["thr"])))
    return T

def verdict(flags):
    a, b = flags.get("canonical", False), flags.get("alt", False)
    return "NO-GO IN LEAF SPACE" if a and b else ("NO-GO ON ONE FOOTING ONLY (" + ("canonical" if a else "alt") + ")" if (a or b) else None)

def real(mutate=False):
    res = dict(mode="MUTATE" if mutate else "real", arms={}); tag = "_MUTATE" if mutate else ""
    P(f"CX1 {'MUTATE' if mutate else 'real'} run. kappa = 1/2 FITTED; not theory closed. Footings never pooled.")
    CTRL = json.load(open(os.path.join(HERE, "cx1_controls.json"))) if not mutate else None
    DD = {}
    for foot in FEET:
        DD[foot] = load(foot)[0]; DD[foot + "x2"] = load(foot, amult=2.0)[0]; DD[foot + "low"] = load(foot, "low")[0]
    for arm in ARMS:
        A = res["arms"][arm] = {}
        for variant in ("all", "noX", "Xshift", "noLG", "low"):
            V = A[variant] = {}; lflag, pflag, lund, pund = {}, {}, {}, {}
            for foot in FEET:
                D = DD[foot + ("low" if variant == "low" else "")]; var = "all" if variant == "low" else variant
                MU = D.MU.copy()
                if mutate:
                    m_ = rows_for(D, arm, var); ii = np.nonzero(m_)[0]; MU[ii, 4] = MU[np.random.default_rng(MSEED).permutation(ii), 4]
                R, PL, LL, n = analyze(D, arm, var, MU)
                D2 = DD[foot + "x2"]; R2, PL2, LL2, _ = analyze(D2, arm, var) if (variant in ("all", "noX", "Xshift") and not mutate) else (None, None, {}, 0)
                robust = {k: v for k, v in LL.items() if v["collision"] and LL2.get(k, {}).get("collision")} if R2 is not None else {}
                ok_ctrl = True
                if CTRL:
                    nl = CTRL["nulls"][f"{foot}|{arm}"]; pl = CTRL["planted"][f"{foot}|{arm}"]
                    ok_line = nl["F1"]["ok_line"] and nl["F2"]["ok_line"] and pl["0.3"]["found"]; ok_pt = nl["F1"]["ok_point"] and nl["F2"]["ok_point"] and pl["1.0"]["found"]
                else: ok_line = ok_pt = True
                lflag[foot] = bool(robust) and ok_line if R2 is not None else any(v["collision"] for v in LL.values()) and ok_line
                lund[foot] = (any(v["undetermined"] for v in LL.values()) or (any(v["collision"] for v in LL.values()) and not lflag[foot])) or not ok_line
                pst = PL["n_strong_cross"] > 0
                if R2 is not None: pst = pst and PL2["n_strong_cross"] > 0
                pflag[foot] = pst and ok_pt; pund[foot] = (PL["n_undet_cross"] > 0 or (PL["n_strong_cross"] > 0 and not pflag[foot])) or not ok_pt
                V[foot] = dict(n_rows=n, point={k: v for k, v in PL.items() if k not in ("strong_cross_idx",)}, point_x2=None if PL2 is None else {k: v for k, v in PL2.items() if k != "strong_cross_idx"},
                               line_pairs=LL, line_robust_x2=sorted(robust), controls_ok=dict(line=ok_line, point=ok_pt),
                               min_dL_cross={f"{a}|{b}": dict(dL=round(v[0], 3), a=str(D.name[v[1]]), b=str(D.name[v[2]])) for (a, b), v in sorted(R["mind"].items())},
                               top=table_rows(D, R, PL))
                P(f"\n[{arm} {variant} {foot}] rows {n}; near pairs {PL['N_near']}, z_LEE {PL['z_LEE']}; point cross z>=3 {PL['n_coll_cross']}, strong cross {PL['n_strong_cross']}"
                  f" (x2: {None if PL2 is None else PL2['n_strong_cross']}), within-line z>=3 {PL['n_coll_within']}, strong within {PL['n_strong_within']}, undet cross {PL['n_undet_cross']}")
                for k, v in LL.items():
                    P(f"   line {k:14s} pairs {v['n_pairs']:6d} sys {v['n_sys']} mean m {v['mean_m']:+.3f} +- {v['sd']:.3f} tol {v['tol']:.2f}"
                      f"{'  COLLISION' if v['collision'] else ''}{'  undetermined' if v['undetermined'] else ''}{'  (x2 robust)' if k in robust else ''}")
                P("   min d_L cross-line: " + "; ".join(f"{k} {v['dL']}" for k, v in V[foot]["min_dL_cross"].items()))
            def lab(fl, un):
                v = verdict(fl); return v if v else ("UNDETERMINED" if any(un.values()) else "NO COLLISION")
            V["verdict_line"] = lab(lflag, lund); V["verdict_point"] = lab(pflag, pund)
            P(f"== {arm} {variant}: line-level {V['verdict_line']}; point-level {V['verdict_point']}")
    res["rss_GB"] = rss(); return res

if __name__ == "__main__":
    t0 = time.time()
    if MODE == "controls":
        r = controls(); fn = "cx1_controls"
    elif MODE == "real":
        r = real(); fn = "cx1_real"
    elif MODE == "mutate":
        r = real(mutate=True); fn = "cx1_MUTATE"
        base = json.load(open(os.path.join(HERE, "cx1_real.json")))
        changed = any(base["arms"][a]["all"][f]["point"]["n_coll_cross"] + base["arms"][a]["all"][f]["point"]["n_coll_within"]
                      != r["arms"][a]["all"][f]["point"]["n_coll_cross"] + r["arms"][a]["all"][f]["point"]["n_coll_within"] for a in ARMS for f in FEET)
        r["count_changed"] = bool(changed); P(f"MUTATE: point-collision count changed vs real: {changed}")
    r["wall_s"] = round(time.time() - t0, 1); r["rss_GB"] = rss()
    json.dump(r, open(os.path.join(HERE, fn + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    open(os.path.join(HERE, fn + ".out"), "w").write("\n".join(OUT) + "\n")
    if MODE == "mutate" and not r["count_changed"]: sys.exit(1)
