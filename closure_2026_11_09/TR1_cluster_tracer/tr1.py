#!/usr/bin/env python3
"""TR1 (FROZEN_CRITERIA.md, 45ee5f7d8b): which baryon tracer does the cluster missing mass follow, per cluster and per
r/R500 bin? Fit M_X(<r) = A_T,c M_T(<r), one amplitude per cluster, for T = gas, stars, bar (gas + stars), tot (the
hydrostatic / lensing total), on X-COP (primary leg, 7 with measured stars) and CLASH (per cluster; bar = gas + BCG, tot).
Two readings of the missing mass: D = M_dyn - M_law(M_bar) (the brief's), S = r^2 g_N(g_dyn)/G - M_bar (extra source
inside the law). Both footings separately, never pooled.
    python3 tr1.py            -> tr1.json / tr1.out
    python3 tr1.py --mutate   -> tr1_MUTATE.json / tr1_MUTATE.out (M1 swap, M2 plant, M3 amplitude x2)
HL3's point builder (and through it NA2's loaders) is executed from source, read-only, up to its KA4 block (nothing is
written in its folder); QX29 / QX27 are imported read-only for KA2. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
1 thread, nice 10; SIGTERM exits before any output is written (rerun from scratch is the checkpoint)."""
import os, sys, io, re, json, math, signal, resource, warnings, contextlib, importlib.util
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))
try: os.nice(10)
except OSError: pass
import numpy as np
from scipy.optimize import nnls

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "tr1_MUTATE" if MUT else "tr1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; EDGES_IN = [0.0, 0.25, 0.5, 0.75, 1.0]; SUB = [0.0, 0.05, 0.10, 0.25]
B, SEED = 10000, 1103; MARK = -1.0; L_RMS, L_BIN, L_SPREAD, L_TIE = 0.10, 0.15, 0.10, 0.02
LG2 = math.log10(2.0)

# ------------------------------------------------------------------ HL3's point builder, executed from source (read-only)
HL3 = os.path.join(REPO, "closure_2026_11_08", "HL3_lensing_leg_shape", "hl3.py")
src = open(HL3).read(); cut = src.index("# ------------------------------------------------------------------ KA4")
NS = {"__file__": HL3, "__name__": "hl3_reused"}; argv0 = sys.argv; sys.argv = [HL3]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], HL3, "exec"), NS)
sys.argv = argv0
A0, glaw, G, MS, KPC = (NS[k] for k in ("A0", "glaw", "G", "MS", "KPC"))
FOOTS = list(A0)
P(f"TR1 {'MUTATE' if MUT else 'MAIN'}: footings {', '.join(f'{f} a0 {A0[f]:.4e}' for f in FOOTS)} (the loaders' values), graded separately. Criteria 45ee5f7d8b. "
  "kappa = 1/2 FITTED; not theory closed.")
P(f"bins r/R500 {EDGES}; FOLLOWS iff RMS <= {L_RMS} and max |SHAPE_b| <= {L_BIN} dex over graded bins (>= 6 shape clusters); UNIVERSAL iff SD(log A) <= {L_SPREAD} dex; "
  f"bootstrap B {B}, seed {SEED}; M_X <= 0 points enter as l = {MARK}.")

# ------------------------------------------------------------------ points, both legs
XC = []
for h in NS["HYD"]:
    XC.append(dict(leg="xcop", name=h["name"], x=h["x"], r_kpc=h["r_kpc"], M_gas=h["M_gas"], M_star=h["M_star"], M_bar=h["M_gas"] + h["M_star"], M_dyn=h["M_hyd"],
                   measured=h["stars_measured"], a2319=h["a2319"], rho={f: h[f"rho_{f}"] for f in FOOTS}))
CL = []
for t in NS["LENS"]:
    r = t["r_kpc"] * KPC
    CL.append(dict(leg="clash", name=t["name"], x=t["x"], r_kpc=t["r_kpc"], M_bar=10 ** t["lgbar"] * r ** 2 / G / MS, M_dyn=10 ** t["lgtot"] * r ** 2 / G / MS,
                   merger=t["merger"], rho={f: t[f"rho_{f}"] for f in FOOTS}))
def gN_of_g(g, a0): return g * g / (g + a0)
def mx_point(p, f, reading):
    r = p["r_kpc"] * KPC; a0 = A0[f]; gb = G * p["M_bar"] * MS / r ** 2; gd = G * p["M_dyn"] * MS / r ** 2
    if reading == "D": return p["M_dyn"] - float(glaw(np.array(gb), a0)) * r ** 2 / G / MS
    return float(gN_of_g(gd, a0)) * r ** 2 / G / MS - p["M_bar"]
for p in XC + CL: p["MX"] = {(f, rd): mx_point(p, f, rd) for f in FOOTS for rd in ("D", "S")}
TKEY = dict(gas="M_gas", stars="M_star", bar="M_bar", tot="M_dyn")
X_PRIM = [p for p in XC if p["measured"]]; X_NOA = [p for p in X_PRIM if not p["a2319"]]; X_ALL = XC
C_PRIM = [p for p in CL if not p["merger"]]; C_ALL = CL
P(f"X-COP: {len(X_PRIM)} points in {len({p['name'] for p in X_PRIM})} clusters with measured stars (PRIMARY: {sorted({p['name'] for p in X_PRIM})}); all 12: {len(X_ALL)} points (5 imputed)")
P(f"CLASH: {len(CL)} points in {len({p['name'] for p in CL})} clusters (per-cluster identity in the table's Name column: graded PER CLUSTER); PRIMARY {len({p['name'] for p in C_PRIM})} X-ray selected")

# ------------------------------------------------------------------ known answers
P(); P("KNOWN ANSWERS")
KA = {}; ok_all = True
def cl_bin_median(points, val, edges):
    names = sorted({p["name"] for p in points}); M = np.full((len(names), len(edges) - 1), np.nan)
    for i, nm in enumerate(names):
        for b in range(len(edges) - 1):
            v = [val(p) for p in points if p["name"] == nm and edges[b] <= p["x"] < edges[b + 1]]
            if v: M[i, b] = float(np.median(v))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); return np.nanmedian(M, axis=0)
ref1 = {"canonical": [0.530, 0.463, 0.372, 0.264, 0.161], "alt": [0.500, 0.429, 0.339, 0.229, 0.126]}
KA["KA1"] = {}
for f in FOOTS:
    med = cl_bin_median(X_PRIM, lambda p: p["rho"][f], EDGES); ok = bool(np.all(np.abs(med - np.array(ref1[f])) <= 0.0015)); ok_all &= ok
    KA["KA1"][f] = dict(medians=med.tolist(), ref=ref1[f], passed=ok)
    P(f"KA1 [{f}] HL3 hydrostatic per-bin medians on the 7: {' / '.join(f'{v:+.4f}' for v in med)} (HL3 {' / '.join(f'{v:+.3f}' for v in ref1[f])}) -> {'PASS' if ok else 'FAIL'}")
ref3 = {"canonical": [0.578, 0.516], "alt": [0.549, 0.485]}
KA["KA3"] = dict(n_points=len(CL), n_clusters=len({p["name"] for p in CL}))
for f in FOOTS:
    med = cl_bin_median(C_PRIM, lambda p: p["rho"][f], EDGES)[:2]; ok = bool(len(CL) == 84 and KA["KA3"]["n_clusters"] == 20 and np.all(np.abs(med - np.array(ref3[f])) <= 0.0015)); ok_all &= ok
    KA["KA3"][f] = dict(medians=med.tolist(), ref=ref3[f], passed=ok)
    P(f"KA3 [{f}] CLASH {len(CL)} points / {KA['KA3']['n_clusters']} clusters; HL3 lensing medians on the 16, bins 0-0.25 / 0.25-0.5: {med[0]:+.4f} / {med[1]:+.4f} (HL3 {ref3[f][0]:+.3f} / {ref3[f][1]:+.3f}) -> {'PASS' if ok else 'FAIL'}")
KA["KA4"] = {}
for f in FOOTS:
    a0 = A0[f]; gN = np.geomspace(1e-6, 1e6, 61) * a0; g = glaw(gN, a0); rt = float(np.max(np.abs(gN_of_g(g, a0) / gN - 1)))
    dev = 0.0
    for p in X_PRIM[::7] + CL[::5]:
        r = p["r_kpc"] * KPC; q = dict(p); q["M_dyn"] = float(glaw(np.array(G * p["M_bar"] * MS / r ** 2), a0)) * r ** 2 / G / MS
        dev = max(dev, abs(mx_point(q, f, "D")) / q["M_dyn"], abs(mx_point(q, f, "S")) / q["M_dyn"])
    ok = bool(rt <= 1e-12 and dev <= 1e-9); ok_all &= ok; KA["KA4"][f] = dict(roundtrip=rt, zero_test=dev, passed=ok)
    P(f"KA4 [{f}] round trip g^2/(g + a0) = g_N over 1e-6..1e6 a0: max dev {rt:.1e}; D and S give M_X = 0 at M_dyn = M_law(M_bar): max |M_X|/M_dyn {dev:.1e} -> {'PASS' if ok else 'FAIL'}")
# KA2: QX29 B1 at f_cap R through QX29's host rule and QX27's grader (imported read-only; argv cleared so its own --mutate switch stays off)
p29 = os.path.join(REPO, "closure_2026_11_06", "QX29_dipolar_medium", "qx29.py")
argv0 = sys.argv; sys.argv = [p29]
with contextlib.redirect_stdout(io.StringIO()):
    s29 = importlib.util.spec_from_file_location("qx29_lib", p29); Q29 = importlib.util.module_from_spec(s29); s29.loader.exec_module(Q29)
sys.argv = argv0
ref2 = {"canonical": (-0.003, 0.082), "alt": (-0.027, 0.087)}; KA["KA2"] = {}
for f in FOOTS:
    with contextlib.redirect_stdout(io.StringIO()):
        o = Q29.M27.grade(Q29.Cand("B1", Q29.FCAP * Q29.R), Q29.A0K[f], Q29.M27.BASE[f])
    ok = bool(abs(o["X_mean"] - ref2[f][0]) <= 0.0015 and abs(o["X_rms"] - ref2[f][1]) <= 0.0015); ok_all &= ok
    KA["KA2"][f] = dict(X_mean=o["X_mean"], X_rms=o["X_rms"], ref=ref2[f], amp=Q29.FCAP * Q29.R, a0_SI_loader=Q29.FOOT_SI[f], passed=ok)
    P(f"KA2 [{f}] QX29 B1 at f_cap R = {Q29.FCAP * Q29.R:.4f} (baryon-traced source inside the law; loader a0 {Q29.FOOT_SI[f]:.4e}): X-COP mean / rms {o['X_mean']:+.4f} / {o['X_rms']:.4f} "
      f"(QX29 {ref2[f][0]:+.3f} / {ref2[f][1]:.3f}) -> {'PASS' if ok else 'FAIL'}")
P(f"KNOWN ANSWERS {'ALL PASS -> the grade may be read' if ok_all else 'FAILED -> DO NOT READ THE GRADE'}")

# ------------------------------------------------------------------ the fit and the statistics
def interp_x(points, key):
    """per cluster: log-log interpolator of a profile in r/R500 (for M1)."""
    out = {}
    for nm in sorted({p["name"] for p in points}):
        q = sorted((p["x"], p[key]) for p in points if p["name"] == nm and p[key] > 0); xs = np.log10([a for a, _ in q]); ys = np.log10([b for _, b in q])
        out[nm] = (lambda xv, xs=xs, ys=ys: float(10 ** np.interp(math.log10(xv), xs, ys)) if xs[0] <= math.log10(xv) <= xs[-1] else float("nan"))
    return out
def grade(points, T, f, rd, edges=EDGES, mx_mult=None, tracer=None, a_shift=0.0, boot=True, sub=False):
    """returns per-cluster logA, per-bin q and residuals, SHAPE, RMS, SPREAD, FOLLOWS. mx_mult(p) multiplies M_X; tracer(p) replaces M_T(p);
    a_shift adds to every fitted log A after the fit (M3a)."""
    NB = len(edges) - 1; names = sorted({p["name"] for p in points}); n = len(names)
    Q = np.full((n, NB), np.nan); npos = 0; nneg = 0
    for i, nm in enumerate(names):
        for b in range(NB):
            l = []
            for p in points:
                if p["name"] != nm or not (edges[b] <= p["x"] < edges[b + 1]): continue
                m = p["MX"][(f, rd)] * (mx_mult(p) if mx_mult else 1.0); t = tracer(p) if tracer else p[TKEY[T]]
                if not (np.isfinite(t) and t > 0): continue
                if m > 0: l.append(math.log10(m / t)); npos += 1
                else: l.append(MARK); nneg += 1
            if l: Q[i, b] = float(np.median(l))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); logA = np.nanmean(Q, axis=1) + a_shift
    D = Q - logA[:, None]; nb_c = np.isfinite(Q).sum(axis=1); shp = nb_c >= 2
    Ds = D[shp]; ncl_b = np.isfinite(Ds).sum(axis=0); graded = ncl_b >= 6
    with warnings.catch_warnings():
        warnings.simplefilter("ignore"); SH = np.nanmedian(Ds, axis=0)
    sel = Ds[:, graded]; rms = float(np.sqrt(np.nanmean(sel ** 2))) if graded.any() else float("nan")
    maxb = float(np.nanmax(np.abs(SH[graded]))) if graded.any() else float("nan")
    lo = hi = [float("nan")] * NB
    if boot and shp.sum() >= 3:
        rng = np.random.default_rng(SEED); idx = rng.integers(0, len(Ds), (B, len(Ds)))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore"); S = np.nanmedian(Ds[idx], axis=1); lo = np.nanpercentile(S, 2.5, axis=0).tolist(); hi = np.nanpercentile(S, 97.5, axis=0).tolist()
    la = logA[shp]; spread = float(np.std(la, ddof=1)) if len(la) >= 2 else float("nan")
    follows = bool(graded.any() and rms <= L_RMS and maxb <= L_BIN)
    return dict(tracer=T, footing=f, reading=rd, names=names, logA=logA.tolist(), A=(10 ** logA).tolist(), Q=Q.tolist(), resid=D.tolist(), shape_clusters=[nm for nm, s in zip(names, shp) if s],
                shape=SH.tolist(), shape_lo=lo, shape_hi=hi, n_bin=ncl_b.tolist(), graded=graded.tolist(), rms=rms, max_bin=maxb, spread=spread,
                A_median=float(10 ** np.median(la)) if len(la) else float("nan"), follows=follows, universal=bool(spread <= L_SPREAD), n_pos=npos, n_nonpos=nneg)
def fmt(v): return "  --  " if not np.isfinite(v) else f"{v:+.3f}"
def show(g, edges=EDGES, tag=""):
    NB = len(edges) - 1
    P(f"  {tag}{g['tracer']:5s} RMS {g['rms']:.3f}  max|SHAPE| {g['max_bin']:.3f}  SHAPE " + " ".join(fmt(g['shape'][b]) + ('' if g['graded'][b] else '*') for b in range(NB)) +
      f"  | A median {g['A_median']:.3f}, SD(log A) {g['spread']:.3f} -> {'FOLLOWS' if g['follows'] else 'DOES NOT FOLLOW'}, {'UNIVERSAL' if g['universal'] else 'CLUSTER-DEPENDENT'}"
      + (f"  [M_X<=0 points: {g['n_nonpos']}]" if g['n_nonpos'] else ""))
def label(res):
    fol = sorted([T for T, g in res.items() if g["follows"]], key=lambda T: res[T]["rms"])
    if fol:
        w = fol[0]
        if len(fol) > 1 and res[fol[1]]["rms"] - res[w]["rms"] <= L_TIE: return f"TIE ({w}, {fol[1]})", w, fol
        return w, w, fol
    c = min(res, key=lambda T: res[T]["rms"] if np.isfinite(res[T]["rms"]) else 9.0); sh = [v for v, gr in zip(res[c]["shape"], res[c]["graded"]) if gr]
    pat = "inner HIGH (missing mass more concentrated than " + c + ")" if sh[0] > sh[-1] else "inner LOW (missing mass less concentrated than " + c + ")"
    return f"NO TRACER FOLLOWS (closest {c}: {pat})", c, fol

LEGS = dict(xcop=dict(prim=X_PRIM, tracers=("gas", "stars", "bar", "tot"), brackets=dict(b1_noA2319=(X_NOA, EDGES), b2_all12_imputed=(X_ALL, EDGES), b3_inside_R500=(X_PRIM, EDGES_IN))),
            clash=dict(prim=C_PRIM, tracers=("bar", "tot"), brackets=dict(all20=(C_ALL, EDGES))))
RES = dict(criteria="45ee5f7d8b", footings=A0, edges=EDGES, KA=KA, ka_all_pass=bool(ok_all), legs={})

if not MUT:
    for leg, L in LEGS.items():
        RES["legs"][leg] = {}
        for rd in ("D", "S"):
            for f in FOOTS:
                P(); P(f"== {leg.upper()} reading {rd} [{f}] ({'M_dyn - M_law(M_bar)' if rd == 'D' else 'r^2 g_N(g_dyn)/G - M_bar'}); SHAPE per bin {EDGES} (* = not graded, < 6 shape clusters)")
                res = {T: grade(L["prim"], T, f, rd) for T in L["tracers"]}
                for T in L["tracers"]: show(res[T])
                lab, w, fol = label(res)
                br = {}
                for bn, (pts, ed) in L["brackets"].items():
                    br[bn] = {T: grade(pts, T, f, rd, edges=ed, boot=False) for T in L["tracers"]}
                    P(f"  bracket {bn}: " + "; ".join(f"{T} RMS {br[bn][T]['rms']:.3f} max {br[bn][T]['max_bin']:.3f} {'F' if br[bn][T]['follows'] else 'nf'}" for T in L["tracers"]))
                sens = [bn for bn in br if br[bn][w]["follows"] != res[w]["follows"]]
                if sens: lab += " (bracket-sensitive: " + ", ".join(sens) + ")"
                P(f"  LABEL {leg} {rd} [{f}]: {lab}; following: {fol if fol else 'none'}; {w} amplitude {'UNIVERSAL' if res[w]['universal'] else 'CLUSTER-DEPENDENT'} (SD {res[w]['spread']:.3f})")
                P(f"  {w} per-cluster residuals (dex), bins {EDGES}:")
                for i, nm in enumerate(res[w]["names"]):
                    P(f"    {nm:10s} A {res[w]['A'][i]:7.3f}  " + " ".join(fmt(v) for v in res[w]["resid"][i]))
                RES["legs"][leg][f"{rd}_{f}"] = dict(primary=res, brackets=br, label=lab, winner_or_closest=w, following=fol)
    # amplitude table, every tracer, X-COP primary + CLASH primary
    P(); P("AMPLITUDE TABLE A_T,c (X-COP primary; median and SD(log A) in the lines above)")
    for rd in ("D", "S"):
        for f in FOOTS:
            r = RES["legs"]["xcop"][f"{rd}_{f}"]["primary"]; nm = r["gas"]["names"]
            P(f"  [{rd} {f}] " + "  ".join(f"{n}: " + "/".join(f"{r[T]['A'][i]:.2f}" for T in ("gas", "stars", "bar", "tot")) for i, n in enumerate(nm)) + "   (gas/stars/bar/tot)")
    # r1 core read: sub-bins inside 0.25, residual relative to the cluster's five-bin log A
    P(); P(f"r1 CORE READ (reported, not graded): X-COP primary, cluster-median residual in sub-bins {SUB} relative to the five-bin fit")
    RES["r1_core"] = {}
    for rd in ("D", "S"):
        for f in FOOTS:
            row = {}
            for T in ("gas", "stars", "bar", "tot"):
                g5 = RES["legs"]["xcop"][f"{rd}_{f}"]["primary"][T]; gs = grade(X_PRIM, T, f, rd, edges=SUB, boot=False)
                Qs = np.array(gs["Q"]) - np.array(g5["logA"])[:, None]
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore"); row[T] = np.nanmedian(Qs, axis=0).tolist()
            RES["r1_core"][f"{rd}_{f}"] = row
            P(f"  [{rd} {f}] " + "; ".join(f"{T} " + " ".join(fmt(v) for v in row[T]) for T in row))
    # r2 two-component NNLS: M_X = a M_gas + b M_star, relative residuals
    P(); P("r2 TWO-COMPONENT MIX (reported, never a label: two amplitudes): M_X = a M_gas + b M_star per cluster, NNLS on relative residuals, X-COP primary")
    RES["r2_mix"] = {}
    for rd in ("D", "S"):
        for f in FOOTS:
            rows = []
            for nm in sorted({p["name"] for p in X_PRIM}):
                pts = [p for p in X_PRIM if p["name"] == nm and p["MX"][(f, rd)] > 0]; m = np.array([p["MX"][(f, rd)] for p in pts])
                Am = np.array([[p["M_gas"] / mm, p["M_star"] / mm] for p, mm in zip(pts, m)]); (a, b), _ = nnls(Am, np.ones(len(m)))
                mod = a * np.array([p["M_gas"] for p in pts]) + b * np.array([p["M_star"] for p in pts]); lr = np.log10(m / np.maximum(mod, 1e-300))
                xs = np.array([p["x"] for p in pts]); per = []
                for bb in range(len(EDGES) - 1):
                    s_ = (xs >= EDGES[bb]) & (xs < EDGES[bb + 1]); per.append(float(np.median(lr[s_])) if s_.any() else float("nan"))
                rows.append(dict(name=nm, a_gas=float(a), b_star=float(b), rms_bins=float(np.sqrt(np.nanmean(np.array(per) ** 2))), bins=per))
            RES["r2_mix"][f"{rd}_{f}"] = rows
            P(f"  [{rd} {f}] " + "; ".join(f"{r_['name']} a {r_['a_gas']:.2f} b {r_['b_star']:.2f} (bins rms {r_['rms_bins']:.3f})" for r_ in rows))
    # r4 (added after the first run, reported only, disclosed in RESULT.md): QX29 B1's model (S reading, bar tracer, ONE sample-wide amplitude f_cap R)
    # on TR1's points, read both on the TOTAL mass (QX29 G4's statistic) and on the COMPONENT (TR1's statistic), to reconcile KA2 with the S/bar grade
    AB = Q29.FCAP * Q29.R
    P(); P(f"r4 RECONCILIATION WITH KA2 (reported, not graded; added after the first run): QX29 B1's model M_need = (1 + {AB:.4f}) M_bar (S reading, bar, one amplitude for all clusters) on TR1's X-COP primary points;"
           " total-mass residual log10(M_dyn / M_pred) with g_pred = g_law(G M_need / r^2), and component residual log10(M_src / (A M_bar)); per-bin cluster medians")
    RES["r4_b1_reconcile"] = {}
    for f in FOOTS:
        tot_r = []; comp_r = []; xs = []; nms = []
        for p in X_PRIM:
            r = p["r_kpc"] * KPC; mp = float(glaw(np.array(G * (1 + AB) * p["M_bar"] * MS / r ** 2), A0[f])) * r ** 2 / G / MS
            tot_r.append(math.log10(p["M_dyn"] / mp)); m = p["MX"][(f, "S")]; comp_r.append(math.log10(m / (AB * p["M_bar"])) if m > 0 else MARK); xs.append(p["x"]); nms.append(p["name"])
        tot_r, comp_r, xs, nms = map(np.array, (tot_r, comp_r, xs, nms)); m7 = (xs >= 0.1) & (xs <= 0.7)
        def bmed(v):
            out = []
            for b in range(len(EDGES) - 1):
                u = [float(np.median(v[(nms == n) & (xs >= EDGES[b]) & (xs < EDGES[b + 1])])) for n in sorted(set(nms)) if np.any((nms == n) & (xs >= EDGES[b]) & (xs < EDGES[b + 1]))]
                out.append(float(np.median(u)) if u else float("nan"))
            return out
        row = dict(amp=AB, total_mean_01_07=float(np.mean(tot_r[m7])), total_rms_01_07=float(np.sqrt(np.mean(tot_r[m7] ** 2))), total_bins=bmed(tot_r), comp_bins=bmed(comp_r),
                   comp_rms_01_07=float(np.sqrt(np.mean(comp_r[m7] ** 2))))
        RES["r4_b1_reconcile"][f] = row
        P(f"  [{f}] total mass, r/R500 0.1-0.7: mean {row['total_mean_01_07']:+.3f}, rms {row['total_rms_01_07']:.3f} (QX29 G4 at its 5 radii: {ref2[f][0]:+.3f} / {ref2[f][1]:.3f}); "
          f"total bins {' '.join(fmt(v) for v in row['total_bins'])}; COMPONENT bins {' '.join(fmt(v) for v in row['comp_bins'])}, component rms 0.1-0.7 {row['comp_rms_01_07']:.3f}")
    # r3 HFF projected member light (stellar tracer only; no lensing profile on disk)
    P(); P("r3 HFF MEMBER LIGHT (reported, not graded): projected cumulative F160W member light L(<R) around the brightest F160W member; slope d log L / d log R over 50-300 kpc")
    zU = NS["Z"]; zG = None
    for ln in open(os.path.join(DATA, "groener2016_cluster_concentrations.tsv")):
        c = ln.rstrip("\n").split("\t")
        if len(c) > 3 and re.sub(r"\s", "", c[1]).lower() in ("abell2744", "a2744"):
            try: zG = float(c[2]); break
            except ValueError: pass
    H0 = 70.0; OMm, OLm = 0.27, 0.73; cK = 299792.458
    def DA_kpc(z):
        zz = np.linspace(0, z, 2001); Ez = np.sqrt(OMm * (1 + zz) ** 3 + OLm); return float(cK / H0 * np.trapz(1 / Ez, zz) / (1 + z) * 1e3)
    RES["r3_hff"] = {}
    for tag, zk in (("a2744", None), ("as1063", "2248"), ("m0416", "0416"), ("m1149", "1149")):
        z = zG if zk is None else zU.get(zk)
        if z is None: P(f"  {tag}: no redshift on disk -> skipped"); continue
        rows = []
        for ln in open(os.path.join(DATA, f"hff_granata_{tag}.tsv")):
            c = ln.rstrip("\n").split("\t")
            if len(c) < 7 or ln.startswith("#"): continue
            try: rows.append((float(c[1]), float(c[2]), float(c[6])))
            except ValueError: continue
        a = np.array(rows); ib = int(np.argmin(a[:, 2])); ra0, de0 = a[ib, 0], a[ib, 1]
        dx = (a[:, 0] - ra0) * math.cos(math.radians(de0)); dy = a[:, 1] - de0; R = np.radians(np.hypot(dx, dy)) * DA_kpc(z); Lm = 10 ** (-0.4 * a[:, 2])
        Rg = np.geomspace(50, 300, 12); Lc = np.array([Lm[R <= rr].sum() for rr in Rg]); sl = float(np.polyfit(np.log10(Rg), np.log10(Lc), 1)[0])
        RES["r3_hff"][tag] = dict(z=z, n_members=len(a), R_max_kpc=float(R.max()), slope_50_300=sl)
        P(f"  {tag}: z {z:.3f} ({'Groener+2016 table' if zk is None else 'Umetsu+2016 table1'}), {len(a)} members, field reaches R {R.max():.0f} kpc; projected light slope {sl:.3f}")
    sl3 = {}
    for key_, lab_ in (("M_star", "X-COP 3D stars"), ("M_gas", "X-COP 3D gas")):
        v = []
        for nm in sorted({p["name"] for p in X_PRIM}):
            q = sorted((p["r_kpc"], p[key_]) for p in X_PRIM if p["name"] == nm and 50 <= p["r_kpc"] <= 300)
            if len(q) >= 3: v.append(float(np.polyfit(np.log10([u for u, _ in q]), np.log10([w_ for _, w_ in q]), 1)[0]))
        sl3[lab_] = float(np.median(v))
    for rd in ("D", "S"):
        v = []
        for nm in sorted({p["name"] for p in X_PRIM}):
            q = sorted((p["r_kpc"], p["MX"][("canonical", rd)]) for p in X_PRIM if p["name"] == nm and 50 <= p["r_kpc"] <= 300 and p["MX"][("canonical", rd)] > 0)
            if len(q) >= 3: v.append(float(np.polyfit(np.log10([u for u, _ in q]), np.log10([w_ for _, w_ in q]), 1)[0]))
        sl3[f"X-COP 3D missing mass {rd} canonical"] = float(np.median(v))
    RES["r3_xcop_slopes_50_300"] = sl3
    P("  beside (3D, 50-300 kpc, median over the 7): " + "; ".join(f"{k} {v:.3f}" for k, v in sl3.items()))
    P("  projection: a projected cumulative slope exceeds the 3D one for the same density law (a 3D cusp projects shallower in density, steeper in cumulative); member light is not ICL and is"
      " magnitude-limited; the HFF field covers the core only. A shape check, never graded.")
    # summary labels
    P(); P("SUMMARY LABELS (X-COP primary decides; CLASH the second leg)")
    for leg in LEGS:
        for rd in ("D", "S"):
            P(f"  {leg:5s} reading {rd}: " + " / ".join(f"{f} {RES['legs'][leg][f'{rd}_{f}']['label']}" for f in FOOTS))
else:
    P(); P("MUTATE: each run on the winner (or the closest tracer when none follows) of each reading / footing, X-COP primary")
    base = json.load(open(os.path.join(HERE, "tr1.json")))
    RES["mutate"] = {}
    names = sorted({p["name"] for p in X_PRIM})
    for rd in ("D", "S"):
        for f in FOOTS:
            w = base["legs"]["xcop"][f"{rd}_{f}"]["winner_or_closest"]; g0 = grade(X_PRIM, w, f, rd, boot=False); out = dict(target=w, base_rms=g0["rms"], base_follows=g0["follows"], base_spread=g0["spread"])
            # M1 swap the tracer profile between the two clusters whose log M_T(0.5)/M_T(0.1) differ most
            F_ = interp_x(X_PRIM, TKEY[w]); s = {nm: math.log10(F_[nm](0.5) / F_[nm](0.1)) for nm in names}
            pair = max(((a, b) for i, a in enumerate(names) for b in names[i + 1:]), key=lambda ab: abs(s[ab[0]] - s[ab[1]])); sw = {pair[0]: pair[1], pair[1]: pair[0]}
            def trc(p, sw=sw, F_=F_, key=TKEY[w]):
                if p["name"] in sw: return F_[sw[p["name"]]](p["x"]) * (F_[p["name"]](0.5) / F_[sw[p["name"]]](0.5))
                return p[key]
            g1 = grade(X_PRIM, w, f, rd, tracer=trc, boot=False)
            def pair_rms(g):
                ii = [g["names"].index(n) for n in pair]; v = np.array(g["resid"])[ii][:, np.array(g["graded"])]; return float(np.sqrt(np.nanmean(v ** 2)))
            r0, r1_ = pair_rms(g0), pair_rms(g1); out["M1"] = dict(pair=list(pair), shapes={k: s[k] for k in pair}, pair_rms_base=r0, pair_rms_swapped=r1_, rms_swapped=g1["rms"], bites=bool(r1_ - r0 >= 0.02))
            # M2 plant 0.3 dex inner excess
            g2 = grade(X_PRIM, w, f, rd, mx_mult=lambda p: 10 ** 0.3 if p["x"] < 0.25 else 1.0, boot=False)
            d0 = g2["shape"][0] - g0["shape"][0]; b2 = (g0["follows"] and not g2["follows"]) or ((not g0["follows"]) and d0 >= 0.20)
            out["M2"] = dict(shape0_base=g0["shape"][0], shape0_planted=g2["shape"][0], rise=d0, rms_planted=g2["rms"], follows_planted=g2["follows"], bites=bool(b2))
            # M3a A x2, no refit; M3b M_X x2 for the alphabetically first half, refit
            g3 = grade(X_PRIM, w, f, rd, a_shift=LG2, boot=False); b3a = (not g3["follows"]) if g0["follows"] else (g3["rms"] - g0["rms"] >= 0.10)
            half = set(names[:len(names) // 2]); g3b = grade(X_PRIM, w, f, rd, mx_mult=lambda p, h=half: 2.0 if p["name"] in h else 1.0, boot=False)
            b3b = (not g3b["universal"]) if g0["universal"] else (g3b["spread"] - g0["spread"] >= 0.10)
            out["M3a"] = dict(rms=g3["rms"], max_bin=g3["max_bin"], follows=g3["follows"], bites=bool(b3a))
            out["M3b"] = dict(half=sorted(half), spread=g3b["spread"], universal=g3b["universal"], bites=bool(b3b))
            RES["mutate"][f"{rd}_{f}"] = out
            P(f"[{rd} {f}] target {w} (base RMS {g0['rms']:.3f}, {'FOLLOWS' if g0['follows'] else 'does not follow'}, SD(log A) {g0['spread']:.3f}, SHAPE_0 {g0['shape'][0]:+.3f})")
            P(f"   M1 swap {pair[0]} <-> {pair[1]} (log M_T(0.5)/M_T(0.1) {s[pair[0]]:.3f} vs {s[pair[1]]:.3f}): pair RMS {r0:.3f} -> {r1_:.3f} -> {'BITES' if out['M1']['bites'] else 'NO POWER'}")
            P(f"   M2 plant +0.3 dex at r/R500 < 0.25: SHAPE_0 {g0['shape'][0]:+.3f} -> {g2['shape'][0]:+.3f} (rise {d0:+.3f}), RMS {g2['rms']:.3f}, {'FOLLOWS' if g2['follows'] else 'DOES NOT FOLLOW'} -> {'BITES' if b2 else 'NO POWER'}")
            P(f"   M3a A x2 no refit: RMS {g3['rms']:.3f}, max|SHAPE| {g3['max_bin']:.3f} (every residual moves -0.301), {'FOLLOWS' if g3['follows'] else 'DOES NOT FOLLOW'} -> {'BITES' if b3a else 'NO POWER'}")
            P(f"   M3b M_X x2 for {sorted(half)}, refit: SD(log A) {g0['spread']:.3f} -> {g3b['spread']:.3f}, {'UNIVERSAL' if g3b['universal'] else 'CLUSTER-DEPENDENT'} -> {'BITES' if b3b else 'NO POWER'}")
    allb = all(v[k]["bites"] for v in RES["mutate"].values() for k in ("M1", "M2", "M3a", "M3b"))
    RES["all_bite"] = bool(allb); P(f"MUTATE: {'ALL BITE' if allb else 'NOT ALL BITE (see NO POWER lines)'}")

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e6 if sys.platform == "darwin" else 1e3); RES["rss_MB"] = rss
P(); P(f"peak RSS {rss:.0f} MB. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
