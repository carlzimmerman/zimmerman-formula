#!/usr/bin/env python3
"""MK2 row e (criteria 3b4f515ff8, A1 5f2304176e): SPARC through QX8's grader and line with the exponential dust's T_K.
Outer potential per galaxy and U: the Hernquist-softened (x_a 0.2) capped state with the dust at M_b(R_last) (A1), from a table in
log M built by continuation in increasing mass at each c_s; inside R_last the data's law field with three iterations of the dust's
feedback (MK1 row 5's construction, exponential source). KA4: no dust = QX8 exactly. KA1: the quadratic with point-mass baryons
reproduces MK1 row 5 at MK1's grid points around its bound. Reported: x_a 0.1 / 0.4; QX6's recheck line. MUTATE M-2X (share doubled).
    python3 mk2_sparc.py -> mk2_sparc.json / .out, mk2_sparc_MUTATE.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk2_lib as L
QX8D = os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field")
NS = dict(__file__=os.path.join(QX8D, "qx8.py"), __name__="qx8_readonly")
exec(compile(open(os.path.join(QX8D, "qx8.py")).read(), os.path.join(QX8D, "qx8.py"), "exec"), NS)
load_sparc, fit_one, pooled, line, UPS, NODES, nu = NS["load_sparc"], NS["fit_one"], NS["pooled"], NS["line"], NS["UPS"], NS["NODES"], NS["nu"]
G, MS, KPC, MPC, C = L.G, L.MSUN, L.KPC, L.MPC, L.C_SI
OUT, OUTM = [], []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
ONE = json.load(open(os.path.join(REPO, "fable52_push", "ONE1_counted_once", "one1.json"))); XP = {f: float(ONE["foot"][f]["X"]) for f in L.FOOT}
KD1 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
RHO = {f: KD1["footings"][f]["setting"]["I0_Mpc-2"] * C ** 2 / (8 * math.pi * G) / MPC ** 2 for f in L.FOOT}
GALS = load_sparc(); n = len(GALS)
PARTSQ = {f: [dict(np.load(os.path.join(QX8D, "parts", f, f"{i:03d}.npz"), allow_pickle=False)) for i in range(n)] for f in L.FOOT}
lU = np.log(UPS); lN = np.log(NODES); i50 = int(np.where(UPS == 0.50)[0][0])
CS = 10 ** (4.0 - 0.025 * np.arange(121))
XG = np.geomspace(1e-3, 300.0, 600); LXG = np.log(XG); LMG = np.arange(6.0, 12.5001, 0.05)
PARTS = os.path.join(HERE, "parts", "sparc"); os.makedirs(PARTS, exist_ok=True)
P(f"MK2 row e SPARC: {n} galaxies through QX8's grader. {L.NOTE}")

def outer_table(f, kind, par, X, xa):
    """phi(x; log M) [units s] of the capped Hernquist state with the dust, continuation in increasing mass (A1). kind 'exp': par = c_s [km/s];
    'quad': par = mu [1/Mpc]. Folded masses -> nan rows."""
    fn = os.path.join(PARTS, f"tab_{f}_{kind}_{par:.6g}_X{X:.3f}_xa{xa}.npz")
    if os.path.exists(fn): d = np.load(fn); return dict(PH=d["PH"], ok=d["ok"])
    a0 = L.A0[f]; Bh = L.hernquist(xa); grid = L.Grid(Bh, 1e-4, 1e5, h=0.01)
    st0 = L.shoot_fast(grid, 0, 0, 1, 0, X, 1.0, 1.0, -(1.0 / (1e-4 + xa) + 10.0), first=True); Pv = st0["Phi0"]   # guess ~ the centre's depth
    PH = np.full((len(LMG), len(XG)), np.nan); ok = np.zeros(len(LMG), bool); alive = True
    for i, lm in enumerate(LMG):
        if not alive: continue
        M = 10 ** lm * MS; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0)
        if kind == "exp": st = L.shoot_fast(grid, 1, 4 * math.pi * RHO[f] * rM ** 3 / M, (par * 1e3) ** 2 / s, 0, X, 1.0, 1.0, Pv)
        else: st = L.shoot_fast(grid, 2, 0, 1, (par / MPC * rM) ** 2, X, 1.0, 1.0, Pv)
        if not st["ok"]: alive = False; continue
        Pv = st["Phi0"]; ok[i] = True
        inside = XG <= st["rc"]
        PH[i] = np.where(inside, np.interp(LXG, st["u"], st["Phi"]), -(st["C"] / XG + 1.0 / (XG + xa)))
    np.savez(fn, PH=PH, ok=ok); return dict(PH=PH, ok=ok)

def phi_outer(TAB, lm, x):
    fm = (lm - LMG[0]) / 0.05; im = np.clip(np.floor(fm).astype(int), 0, len(LMG) - 2); a = np.clip(fm - im, 0, 1)
    bad = ~(TAB["ok"][im] & TAB["ok"][im + 1]) | (fm < 0) | (fm > len(LMG) - 1)
    v0 = np.array([np.interp(math.log(xx), LXG, TAB["PH"][i]) for i, xx in zip(im, x)]); v1 = np.array([np.interp(math.log(xx), LXG, TAB["PH"][i + 1]) for i, xx in zip(im, x)])
    return np.where(bad, np.nan, (1 - a) * v0 + a * v1)

def dust_T(q, a0, kind, par, rho, TAB):
    R = q["Rm"]; GB = q["GB"]; o = np.argsort(R); R = R[o]; GBs = np.maximum(GB[o], 0.0); nU = GB.shape[1]
    Mb_all = R[:, None] ** 2 * GBs / G; Mtot = np.where(Mb_all[-1] > 0, Mb_all[-1], Mb_all.max(0)); Mtot = np.maximum(Mtot, 1e-30)
    rM = np.sqrt(G * Mtot / a0); s = np.sqrt(G * Mtot * a0); xl = R[-1] / rM
    phl = phi_outer(TAB, np.log10(Mtot / MS), xl) * s
    gK = np.zeros_like(GBs); MK = np.zeros_like(GBs)
    for _ in range(3):
        g = 0.5 * (GBs + gK) + np.sqrt(0.25 * (GBs + gK) ** 2 + a0 * np.maximum(GBs + gK, 0.0))
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(R)[:, None]
        Phi = phl[None, :] - np.concatenate([np.cumsum(seg[::-1], 0)[::-1], np.zeros((1, nU))], 0)
        r2 = np.concatenate([[0.0], R]); ph2 = np.concatenate([Phi[:1], Phi], 0)
        if kind == "exp":
            d2 = rho * np.expm1(np.minimum(np.abs(ph2) / (par * 1e3) ** 2, 700.0))
        else:
            d2 = (par / MPC) ** 2 * np.abs(ph2) / (4 * math.pi * G)
        inte = 0.5 * (4 * math.pi * r2[1:, None] ** 2 * d2[1:] + 4 * math.pi * r2[:-1, None] ** 2 * d2[:-1]) * np.diff(r2)[:, None]
        MK = np.cumsum(inte, 0); gK = G * MK / R[:, None] ** 2
    gb = GBs; gl = 0.5 * gb + np.sqrt(0.25 * gb * gb + a0 * gb); gt = np.maximum(gb + gK, 1e-300); gn = 0.5 * gt + np.sqrt(0.25 * gt * gt + a0 * gt)
    T = np.log10(np.maximum(gn, 1e-300) / np.maximum(gl, 1e-300)); T = np.where(gb > 0, T, 0.0)
    Tout = np.empty_like(T); Tout[o] = T
    return Tout, bool(np.all(np.isfinite(phl))), float(np.nanmax(MK[-1] / Mtot))

def grade(f, kind, par, TAB):
    a0 = L.A0[f]; rows = []; fix = []; folded = 0; fr = []
    for q, pt in zip(GALS, PARTSQ[f]):
        lgl = np.log10(np.maximum(nu(q["GB"] / a0) * q["GB"], 1e-300)); Tn = pt["T"]
        lge = lgl + np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])
        if TAB is not None:
            TK, okp, fK = dust_T(q, a0, kind, par, RHO[f], TAB)
            if not okp: folded += 1
            lge = lge + np.nan_to_num(TK, nan=0.0); fr.append(fK)
        rows.append(fit_one(q, lge)); OK = q["OK"][:, i50]; r = np.log10(q["GO"]) - lge[:, i50]
        fix.append((np.sum(q["W"][OK] * r[OK]), np.sum(q["W"][OK] * r[OK] ** 2), np.sum(q["W"][OK])))
    st = pooled(rows); fm = sum(a for a, _, _ in fix) / sum(c for _, _, c in fix)
    return dict(par=par, rms=st["rms"], U_median=st["U_median"], fixedU_mean=fm, folded=folded, PASS=bool(line(st) and folded == 0), max_MK_over_Mb=(max(fr) if fr else 0.0))

def scan(f, X, xa=0.2, cs_list=CS, printer=P, tag=""):
    base = grade(f, "exp", 1e9, None); pts = []
    for cs in cs_list:
        TAB = outer_table(f, "exp", float(cs), X, xa); r = grade(f, "exp", float(cs), TAB)
        r["recheck_ok"] = bool(r["rms"] - base["rms"] <= 0.01 and abs(r["fixedU_mean"] - base["fixedU_mean"]) <= 0.02); pts.append(r)
    ps = [r["par"] for r in pts if r["PASS"]]
    lo = None
    for r in pts:                      # descending c_s: the bound is the last value of the first run of passes from the top
        if r["PASS"]: lo = r["par"]
        else: break
    rc = None
    for r in pts:
        if r["recheck_ok"]: rc = r["par"]
        else: break
    return dict(base=base, points=pts, passing=ps, lower_bound=lo, recheck_lower=rc)

RES = dict(lane="MK2", row="e SPARC", criteria="3b4f515ff8 (A1 5f2304176e)", note=L.NOTE, KA={}, rows={})
MU = dict(lane="MK2", row="e SPARC MUTATE", arms={})
REF = {"canonical": (0.0560, 0.58), "alt": (0.0558, 0.52)}
for f in L.FOOT:
    b = grade(f, "exp", 1e9, None); ok = abs(b["rms"] - REF[f][0]) <= 1e-4 and abs(b["U_median"] - REF[f][1]) < 1e-9
    RES["KA"][f"KA4 SPARC no dust {f}"] = dict(rms=b["rms"], U=b["U_median"], ok=bool(ok))
    P(f"KA4 [{f}] no dust: rms {b['rms']:.4f} @ U {b['U_median']:.2f} (QX8 {REF[f]}) -> {'PASS' if ok else 'FAIL'}")
    # KA1: the quadratic with point-mass baryons (x_a 1e-6) at MK1's grid points around its bound
    kref = {"canonical": ((7.079457843841417, True), (7.943282347242822, False)), "alt": ((5.623413251903491, True), (6.309573444801936, False))}[f]
    got = []
    for mu, want in kref:
        T = outer_table(f, "quad", mu, XP[f], 1e-6); r = grade(f, "quad", mu, T); got.append((mu, r["PASS"], r["rms"], r["U_median"], want))
    okq = all(g[1] == g[4] for g in got)
    RES["KA"][f"KA1 SPARC quadratic {f}"] = dict(points=got, ok=bool(okq))
    P(f"KA1 [{f}] quadratic through this code: " + "; ".join(f"mu {m:.2f}: {'P' if p else 'F'} (rms {r_:.4f} @ {u:.2f}; MK1 {'P' if w else 'F'})" for m, p, r_, u, w in got) + f" -> {'PASS' if okq else 'FAIL'}")
    sc = scan(f, XP[f]); RES["rows"][f"e {f}"] = sc
    for r in sc["points"][::6]:
        P(f"   [{f}] c_s {r['par']:8.1f}: rms {r['rms']:.4f} @ U {r['U_median']:.2f}, fixed-U mean {r['fixedU_mean']:+.4f}, folded {r['folded']}, max M_d/M_b at last point {r['max_MK_over_Mb']:.3g} -> {'PASS' if r['PASS'] else 'FAIL'}")
    P(f"[{f}] row e: c_s >= {sc['lower_bound']} km/s passes (every larger grid value passes); passing set size {len(sc['passing'])}; recheck line holds down to {sc['recheck_lower']}  [{time.time() - T0:.0f} s]")
    for xa in (0.1, 0.4):
        sx = scan(f, XP[f], xa=xa, cs_list=CS[(CS <= 600) & (CS >= 30)]); RES["rows"][f"e {f} x_a {xa} (reported)"] = dict(lower_bound=sx["lower_bound"], grid="30-600 km/s")
        P(f"   [{f}] reported x_a {xa}: lower bound {sx['lower_bound']}")
    sm = scan(f, 2 * XP[f], cs_list=CS[(CS <= 600) & (CS >= 30)], printer=PM); MU["arms"][f"M-2X {f}"] = dict(lower_bound=sm["lower_bound"], primary=sc["lower_bound"], grid="30-600 km/s")
    PM(f"M-2X [{f}]: lower bound {sm['lower_bound']} (primary {sc['lower_bound']})")
RES["KA_all_pass"] = all(v["ok"] for v in RES["KA"].values())
P(f"Known answers (row e): {sum(v['ok'] for v in RES['KA'].values())} of {len(RES['KA'])} PASS. runtime {time.time() - T0:.0f} s"); P(L.NOTE)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "mk2_sparc.json"), "w"), indent=1); open(os.path.join(HERE, "mk2_sparc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(MU), open(os.path.join(HERE, "mk2_sparc_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "mk2_sparc_MUTATE.out"), "w").write("\n".join(OUTM + [L.NOTE]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
