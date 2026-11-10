#!/usr/bin/env python3
"""MK1 row 5 (criteria b1fbded1e2, amendment A1 916f4e0e22): SPARC through QX8's grader and line (rms <= 0.110, median U in
[0.50, 0.80]) with QX8's exact-field T per point plus the static dust's T_K = log10[g_law(g_bar + G M_K(<r)/r^2) / g_law(g_bar)].
Phi per galaxy and U: the law's field inside the last point (with the dust's own feedback, three iterations), and outside it the
capped point-mass profile with the dust (this lane's solver, branch continuous from m = 0, M_b = r_last^2 g_bar(r_last)/G).
KA3: at mu_K = 0 the regrade equals QX8's exact-field numbers. Reported: QX6's recheck line; the uncapped Phi (S4's zero point).
MUTATE (separate outputs): M-NOCAP (uncapped Phi), M-2X (share doubled), M-SIGN (dust sign flipped).
    python3 mk1_sparc.py  -> mk1_sparc.json / .out, mk1_sparc_MUTATE.json / .out
QX8's qx8.py is executed read-only (functions only; its parts/*.npz are read). kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk1_lib as LB
QX8D = os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field")
NS = dict(__file__=os.path.join(QX8D, "qx8.py"), __name__="qx8_readonly")
exec(compile(open(os.path.join(QX8D, "qx8.py")).read(), os.path.join(QX8D, "qx8.py"), "exec"), NS)
load_sparc, fit_one, pooled, line, UPS, NODES, nu = NS["load_sparc"], NS["fit_one"], NS["pooled"], NS["line"], NS["UPS"], NS["NODES"], NS["nu"]
G, MPC, KPC = LB.G, LB.MPC, 3.0857e19
OUT, OUTM = [], []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
ONE = json.load(open(os.path.join(REPO, "fable52_push", "ONE1_counted_once", "one1.json")))
XP = {f: float(ONE["foot"][f]["X"]) for f in LB.FOOT}
GALS = load_sparc(); n = len(GALS)
PARTS = {f: [dict(np.load(os.path.join(QX8D, "parts", f, f"{i:03d}.npz"), allow_pickle=False)) for i in range(n)] for f in LB.FOOT}
lU = np.log(UPS); lN = np.log(NODES); i50 = int(np.where(UPS == 0.50)[0][0])
P(f"MK1 row 5 SPARC: {n} galaxies through QX8's grader; X = {XP['canonical']:.4f} / {XP['alt']:.4f}. {LB.NOTE}")

# capped outer profiles phi(x; m) on a log m grid by continuation (A1)
XG = np.geomspace(1e-3, 300.0, 700); LXG = np.log(XG)
def outer_table(X, sig):
    ms = list(10 ** np.arange(-6.0, 1.0001, 0.05)); br = LB.capped_branch(ms, X, sig)
    PH = np.full((len(ms) + 1, len(XG)), np.nan); ok = np.zeros(len(ms) + 1, bool); xc = np.full(len(ms) + 1, np.nan)
    p0 = LB.capped_profile(0.0, X); rows = [p0] + br
    for i, p in enumerate(rows):
        if not p["ok"]: continue
        ok[i] = True; xc[i] = p["xc"]
        PH[i] = np.where(XG <= p["xc"], np.interp(LXG, np.log(p["x"]), p["phi"]), -(1 + X) / XG)
    return dict(lm=np.log10(np.array(ms)), PH=PH, ok=ok, xc=xc)
def phi_outer(TAB, m, x):
    """bilinear in (log10 m, log x); m below the grid -> blend with the m = 0 row; returns nan where the branch has folded."""
    lm = np.log10(np.maximum(m, 1e-300)); fm = (lm - TAB["lm"][0]) / 0.05; im = np.floor(fm).astype(int); am = fm - im
    low = fm < 0; r0 = np.where(low, 0, np.clip(im, 0, len(TAB["lm"]) - 2) + 1); r1 = np.where(low, 1, np.clip(im, 0, len(TAB["lm"]) - 2) + 2)
    w = np.where(low, np.clip(m / 10 ** TAB["lm"][0], 0, 1), np.clip(am, 0, 1))
    v0 = np.array([np.interp(np.log(xx), LXG, TAB["PH"][a]) for a, xx in zip(np.atleast_1d(r0), np.atleast_1d(x))])
    v1 = np.array([np.interp(np.log(xx), LXG, TAB["PH"][b]) for b, xx in zip(np.atleast_1d(r1), np.atleast_1d(x))])
    bad = ~(TAB["ok"][r0] & TAB["ok"][r1]) | (fm > len(TAB["lm"]) - 1)
    return np.where(bad, np.nan, (1 - w) * v0 + w * v1)

def dust_T(q, a0, mu_m, TAB, sig=1.0, mode="capped", X=None):
    """T_K (npts, nU) for one galaxy; nan where no capped state exists."""
    R = q["Rm"]; GB = q["GB"]; o = np.argsort(R); R = R[o]; GBs = np.maximum(GB[o], 0.0); nU = GB.shape[1]
    Mb_all = R[:, None] ** 2 * GBs / G; Mtot = np.where(Mb_all[-1] > 0, Mb_all[-1], Mb_all.max(0)); Mtot = np.maximum(Mtot, 1e-30)
    rM = np.sqrt(G * Mtot / a0); s = np.sqrt(G * Mtot * a0); xl = R[-1] / rM; m = mu_m * rM
    if mode == "capped":
        phl = phi_outer(TAB, m, xl) * s
    else:   # uncapped: S4 zero point (reported only). One profile per galaxy at the U = 0.50 mass; phi(x_last) in units of s reused at every U.
        j = i50; x3 = 3 * MPC / rM[j]; xe = 30 * MPC / rM[j]
        if m[j] <= 0:
            ph = float(LB.phi_law(xl[j], (-1 / x3 + math.log(x3)) - float(LB.phi_law(x3))))
        else:
            p = LB.uncapped_profile(m[j], x3, 1.01 * xl[j], sig)          # Phi(R_last) needs the outward integral only to the last point
            ph = float(np.interp(math.log(xl[j]), np.log(p["x"]), p["phi"])) if p["ok"] else np.nan
        phl = ph * s
    gK = np.zeros_like(GBs)
    for _ in range(3):
        g = 0.5 * (GBs + gK) + np.sqrt(0.25 * (GBs + gK) ** 2 + a0 * np.maximum(GBs + gK, 0.0))
        seg = 0.5 * (g[1:] + g[:-1]) * np.diff(R)[:, None]
        Phi = phl[None, :] - np.concatenate([np.cumsum(seg[::-1], 0)[::-1], np.zeros((1, nU))], 0)
        r2 = np.concatenate([[0.0], R]); ph2 = np.concatenate([Phi[:1], Phi], 0)
        inte = 0.5 * ((r2[1:, None] ** 2) * np.abs(ph2[1:]) + (r2[:-1, None] ** 2) * np.abs(ph2[:-1])) * np.diff(r2)[:, None]
        MK = sig * mu_m * mu_m / G * np.cumsum(inte, 0)
        gK = G * MK / R[:, None] ** 2
    gb = GBs; gl = 0.5 * gb + np.sqrt(0.25 * gb * gb + a0 * gb); gt = np.maximum(gb + gK, 1e-300); gn = 0.5 * gt + np.sqrt(0.25 * gt * gt + a0 * gt)
    T = np.log10(np.maximum(gn, 1e-300) / np.maximum(gl, 1e-300)); T = np.where(gb > 0, T, 0.0)
    Tout = np.empty_like(T); Tout[o] = T
    return Tout, bool(np.all(np.isfinite(phl))), MK[-1] / Mtot

def grade(f, mu, TAB, sig=1.0, mode="capped", X=None):
    a0 = LB.A0[f]; mu_m = mu / MPC; rows = []; fix = []; folded = 0; fr = []
    for q, pt in zip(GALS, PARTS[f]):
        lgl = np.log10(np.maximum(nu(q["GB"] / a0) * q["GB"], 1e-300))
        Tn = pt["T"]; Tf = np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])
        lge = lgl + Tf
        if mu > 0:
            TK, okp, fK = dust_T(q, a0, mu_m, TAB, sig, mode, X)
            if not okp: folded += 1
            lge = lge + np.nan_to_num(TK, nan=0.0); fr.append(float(np.nanmax(fK)))
        rows.append(fit_one(q, lge)); OK = q["OK"][:, i50]; r = np.log10(q["GO"]) - lge[:, i50]
        fix.append((np.sum(q["W"][OK] * r[OK]), np.sum(q["W"][OK] * r[OK] ** 2), np.sum(q["W"][OK])))
    st = pooled(rows); fm = sum(a for a, _, _ in fix) / sum(c for _, _, c in fix)
    ok = line(st) and folded == 0
    return dict(mu=mu, rms=st["rms"], U_median=st["U_median"], fixedU_mean=fm, folded=folded, PASS=bool(ok),
                max_MK_over_Mb_at_last=(max(fr) if fr else 0.0))

def scan(f, TAB, grid, sig=1.0, mode="capped", printer=P, tag=""):
    res = []; base = grade(f, 0.0, TAB)
    for mu in grid:
        r = grade(f, mu, TAB, sig, mode); r["recheck_ok"] = bool(r["rms"] - base["rms"] <= 0.01 and abs(r["fixedU_mean"] - base["fixedU_mean"]) <= 0.02); res.append(r)
    ub = None
    for r in res:
        if r["PASS"]: ub = r["mu"]
        else: break
    ff = next((r["mu"] for r in res if not r["PASS"]), None)
    rc = None
    for r in res:
        if r["recheck_ok"]: rc = r["mu"]
        else: break
    return dict(base=base, points=res, upper_bound=ub, first_fail=ff, recheck_upper=rc)

GRID = list(10 ** np.arange(-2.0, 4.0001, 0.05))
RES = dict(lane="MK1", row="5 SPARC", criteria="b1fbded1e2 (A1 916f4e0e22)", note=LB.NOTE, KA={}, rows={})
REF = {"canonical": (0.0560, 0.58), "alt": (0.0558, 0.52)}
for f in LB.FOOT:
    TAB = outer_table(XP[f], 1.0)
    b = grade(f, 0.0, TAB); ok = abs(b["rms"] - REF[f][0]) <= 1e-4 and abs(b["U_median"] - REF[f][1]) < 1e-9
    RES["KA"][f"KA3 {f}"] = dict(rms=b["rms"], U=b["U_median"], ref=REF[f], ok=bool(ok))
    P(f"KA3 [{f}] mu_K 0 regrade: rms {b['rms']:.4f} @ U {b['U_median']:.2f} (QX8 {REF[f][0]} @ {REF[f][1]}) -> {'PASS' if ok else 'FAIL'}")
    sc = scan(f, TAB, GRID); RES["rows"][f"capped {f}"] = sc
    for r in sc["points"]:
        if r["mu"] in (GRID[0],) or abs(math.log10(r["mu"]) * 4 - round(math.log10(r["mu"]) * 4)) < 1e-9 or r["mu"] == sc["first_fail"]:
            P(f"   [{f}] mu {r['mu']:.4g}: rms {r['rms']:.4f} @ U {r['U_median']:.2f}, fixed-U mean {r['fixedU_mean']:+.4f}, folded {r['folded']}, max M_K/M_b at last point {r['max_MK_over_Mb_at_last']:.3g} -> "
              f"{'PASS' if r['PASS'] else 'FAIL'}{'' if r['recheck_ok'] else ' (recheck line exceeded)'}")
    P(f"[{f}] capped upper bound {sc['upper_bound']} (first fail {sc['first_fail']}); QX6 recheck line holds up to {sc['recheck_upper']}  [{time.time() - T0:.0f} s]")
    RES["rows"][f"capped {f}"]["outer_table_folded"] = int((~TAB["ok"]).sum())
ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all_pass"] = ka_ok

# uncapped (reported; also M-NOCAP), coarse grid
UGRID = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
MU = dict(lane="MK1", row="5 SPARC MUTATE", criteria=RES["criteria"], arms={})
for f in LB.FOOT:
    sc = scan(f, None, UGRID, mode="uncapped"); RES["rows"][f"uncapped {f}"] = sc; MU["arms"][f"M-NOCAP {f}"] = dict(upper_bound=sc["upper_bound"], first_fail=sc["first_fail"])
    P(f"[{f}] UNCAPPED (S4 zero point; reported): " + "; ".join(f"mu {r['mu']:g}: rms {r['rms']:.4f} @ {r['U_median']:.2f} {'P' if r['PASS'] else 'F'}" for r in sc["points"]) + f" -> upper bound {sc['upper_bound']}")
    PM(f"M-NOCAP [{f}]: upper bound {sc['upper_bound']} on the coarse grid (capped: {RES['rows'][f'capped {f}']['upper_bound']})")
for f in LB.FOOT:
    TAB2 = outer_table(2 * XP[f], 1.0); sc = scan(f, TAB2, GRID, printer=PM); MU["arms"][f"M-2X {f}"] = dict(upper_bound=sc["upper_bound"], first_fail=sc["first_fail"], recheck_upper=sc["recheck_upper"])
    PM(f"M-2X [{f}]: upper bound {sc['upper_bound']} (first fail {sc['first_fail']}); capped primary {RES['rows'][f'capped {f}']['upper_bound']}")
    TABs = outer_table(XP[f], -1.0); sc = scan(f, TABs, GRID, sig=-1.0, printer=PM); MU["arms"][f"M-SIGN {f}"] = dict(upper_bound=sc["upper_bound"], first_fail=sc["first_fail"],
                                                                                                                  folded_at_first_fail=next((r["folded"] for r in sc["points"] if not r["PASS"]), None))
    PM(f"M-SIGN [{f}]: upper bound {sc['upper_bound']} (first fail {sc['first_fail']}, galaxies with no capped state there {MU['arms'][f'M-SIGN {f}']['folded_at_first_fail']})")
P(f"Known answers (row 5): {sum(v['ok'] for v in RES['KA'].values())} of {len(RES['KA'])} PASS. runtime {time.time() - T0:.0f} s"); P(LB.NOTE)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "mk1_sparc.json"), "w"), indent=1); open(os.path.join(HERE, "mk1_sparc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(MU), open(os.path.join(HERE, "mk1_sparc_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "mk1_sparc_MUTATE.out"), "w").write("\n".join(OUTM + [LB.NOTE]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
