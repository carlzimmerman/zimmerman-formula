#!/usr/bin/env python3
"""BK2 dear gates on named formulas, law row first as known answer. python3 bk2_dear.py keys|mw|bullet FOOT LIST.json OUT.json. LIST is a JSON list of formula strings. One thread; keys run LW1's real path at gas +0.005, f* 0.034, the primary cell, for margins; a formula reaching this gate by passing everything else gets the other cells. kappa = 1/2 FITTED; not theory closed."""
import json, os, re, subprocess, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, HERE); import numpy as np
LAW = "I1(gb,a0)"; what, foot, lst, outf = sys.argv[1:5]; FS = [LAW] + [f for f in json.load(open(lst)) if f != LAW]
from scipy.stats import chi2
def keys():
    sys.path.insert(0, os.path.join(RB, "LW1_law_scorecard")); import lw1_keys as L
    T = L.T; a = 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE, S'; assert T.count(a) == 1
    T = T.replace(a, 'return RM ** 2 * _BKF(gb, _A0L[foot]) / GE, S')
    b = "def _msrc(Mb, foot):"; assert T.count(b) == 1
    T = T.replace(b, f'''import sys as _s, json as _j
_s.path.insert(0, {HERE!r}); import bk2_lib as _B
_BKS = _j.load(open(os.environ["BK2_LIST"]))
def _BKF(gb, a0_):
    fs_ = float(os.environ["X73_FSTAR"]); gb_ = np.maximum(gb, 1e-300); gg_ = gb_ / (1 + fs_); lM_ = np.log(gb_ * RM ** 2); lR_ = np.log(RM); dl_ = np.gradient(lM_, lR_); c_ = np.r_[np.cumsum((0.5 * (gb_[1:] + gb_[:-1]) * np.diff(RM))[::-1])[::-1], 0.0]; L_ = _B._local(gb_ - gg_, gg_, RM, dl_, RM * gb_ + c_ + gb_[-1] * RM[-1], a0_); return _B.ev(_BKS[int(_LAW["mut"][1:])], L_)
''' + b)
    W = os.path.join(HERE, "chunks", f"dear_keys_{foot}"); os.makedirs(W, exist_ok=True); TL = os.path.join(W, "tail.py"); open(TL, "w").write(T); O = os.path.join(W, "keys.json"); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
    for a_, b_ in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % 0.005) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {os.path.join(RB, "LW1_law_scorecard", "cache_g005_f034")!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}')):
        assert d.count(a_) == 1, a_; d = d.replace(a_, b_)
    df = os.path.join(W, "driver.py"); open(df, "w").write(d); lf = os.path.join(W, "list.json"); json.dump(FS, open(lf, "w")); env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", LW1_A0X="1.0", BK2_LIST=lf, DR1_RUN=json.dumps(dict(rows=[["R1", 0, foot, f"F{i}"] for i in range(len(FS))], k2=False)))
    p = subprocess.run(["nice", "-n", "19", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT); print("driver", p.returncode, flush=True); J = json.load(open(O)); res = []
    KS = None; TERMS = (.021, .007, .031, .011, .079)
    for i, f in enumerate(FS):
        c = J.get(f"R1|c0|{foot}|F{i}") or next((v for k, v in J.items() if k.endswith(f"|F{i}")), None)
        if c is None: res.append(dict(F=f, missing=True)); continue
        o = dict(F=f, cells={})
        for h in ("h0672", "h0686"):
            Z = c["Z"][h]; R = J["R"][foot][h]; ks = R["keys"]; z0 = np.array([Z[k] for k in ks]); Rb = np.array(R["R_boot"]); w, V = np.linalg.eigh(Rb); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ z0; c2 = float((z * z / w[ok]).sum()); dof = int(ok.sum()); s_ = .118; zt = Z["G-OUT-M3"] * s_ / np.sqrt(s_ * s_ + sum(t * t for t in TERMS)); bad = [k for k in ks if abs(Z[k]) >= 2]; o["cells"][h] = dict(Z=Z, n_ok=15 - len(bad), bad=bad, M3=Z["G-OUT-M3"], M3_tot=float(zt), chi2=c2, dof=dof, p=float(chi2.sf(c2, dof)))
        res.append(o); print(i, f[:80], {h: (o["cells"][h]["n_ok"], round(o["cells"][h]["M3"], 2), round(o["cells"][h]["M3_tot"], 2), round(o["cells"][h]["chi2"], 1), float(f"{o['cells'][h]['p']:.2g}")) for h in o["cells"]}, flush=True)
    return res
def mw():
    src = open(os.path.join(RB, "LW1_law_scorecard", "lw1_mw.py")).read().split('if "--grade" in sys.argv:')[0]; src = src.replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {os.path.join(RB, 'LW1_law_scorecard')!r}"); ns_ = {"__name__": "lw1mw", "__file__": os.path.join(RB, "LW1_law_scorecard", "lw1_mw.py")}; exec(compile(src, "lw1_mw", "exec"), ns_); import bk2_lib as B
    ns = ns_["ns"]; L = ns_["L"]; PS = ns_["PS"]; OR, BR_R, R0, KZU, lines, spec, classify = ns_["OR"], ns_["BR_R"], ns_["R0"], ns_["KZU"], ns_["lines"], ns_["spec"], ns_["classify"]; a0 = B.A0S[foot]; cf = os.path.join(HERE, "chunks", f"dear_mw_{foot}.json"); Rall = np.r_[R0, OR, BR_R]; S_ = spec(); cache = json.load(open(cf)) if os.path.exists(cf) else []
    for i, (c, rhof) in enumerate(S_):
        if i < len(cache): continue
        Mu = PS.mass_unit(a0); g = ns["mw_grid"](6.6e10 / Mu); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol)); pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); PhiN = pr.solve_newton(); oN = ns["mw_obs"](g, PhiN, a0); vb = L.vc_plane(ns, g, PhiN, a0, Rall); cache.append(dict(c, vb=vb.tolist(), K=list(map(float, oN["K"])), K0=float(oN["K_R0"]))); 
        if i % 5 == 0: json.dump(cache, open(cf, "w"))
    json.dump(cache, open(cf, "w")); res = []; ak = 1e6 / B.PC / 1e3; nR = 1 + len(OR); o_ = np.argsort(Rall)
    for f in FS:
        rows = []
        for q in cache:
            vb = np.array(q["vb"]); Rk = Rall; gbk = vb ** 2 / Rk; Rs = Rk * 1e3 * B.PC; gs = gbk * ak; M = gs * Rs ** 2; dl = np.interp(np.log(Rs), np.log(Rs[o_]), np.gradient(np.log(np.maximum(M[o_], 1e-300)), np.log(np.maximum(Rs[o_], 1e-300)))); Lf = B._local(gs, 0 * gs, Rs, dl, 2 * Rs * gs, a0); Fv = B.ev(f, Lf); gc = (Fv - gs) / ak; vR = np.sqrt(np.maximum(vb ** 2 + Rk * gc, 0)); K = np.array(q["K"]) + gc[nR:] * 1.1 / BR_R / KZU; K0 = q["K0"] + gc[0] * 1.1 / R0 / KZU; rows.append(dict({k: q[k] for k in ("sig_b", "M_bb", "R_d", "Mstar", "tag_Rd_IN", "tag_Mstar_IN")}, R=lines(float(vR[0]), K, float(K0), vR[1:nR])))
        cl = classify(rows, "R"); res.append(dict(F=f, cls=cl["cls"], n_all=cl["n_all"], D=cl["best"]["D"], D_in=(cl["best_in_prior"] or {}).get("D"), label=cl["label"])); print(f[:80], cl["cls"], cl["n_all"], round(cl["best"]["D"], 2), flush=True)
    return res
def bullet():
    p = os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"); src = open(p).read(); i = src.index('say("=" * 90); say("UX6_gas_term_bullet"'); src = src[:i]; src = src.replace('OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")', 'OUT = open(os.devnull, "w")').replace('KFIT = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json")))', f'KFIT = json.load(open({os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json")!r}))').replace("HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)", f"HERE = {os.path.dirname(p)!r}; RB = {RB!r}; REPO = os.path.dirname(RB)")
    a = '        if form == "LAW": return tuple(out)\n'; assert src.count(a) == 1
    src = src.replace('        a0, k, sc, form = sp["a0"], sp["k"], sp.get("scale", 1.0), sp["form"]\n', '        a0, k, sc, form = sp["a0"], sp["k"], sp.get("scale", 1.0), sp["form"]\n        if form in ("BK", "BKm"): return s.bk(sp, C, reg, form)\n')
    src = src.replace("    def extra(s, sp, C, reg=True):", '''    def bk(s, sp, C, reg, form):
        import bk2_lib as B
        a0 = sp["a0"]; gv = tuple(sum(c[i] for c in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]; X, Y, Z = C["X"], C["Y"], C["Z"]
        if reg: gb[1] = gb[1] + a0 / 1000.0
        g = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); gg = np.sqrt(gv[0] ** 2 + gv[1] ** 2 + gv[2] ** 2); gs_ = np.sqrt(C["st"][0] ** 2 + C["st"][1] ** 2 + C["st"][2] ** 2); gg = np.minimum(gg, g); gs = g - gg
        rB = np.minimum(np.sqrt(X ** 2 + Y ** 2 + Z ** 2), np.sqrt((X - BCG3[0]) ** 2 + (Y - BCG3[1]) ** 2 + Z ** 2)) + 0.5; rho = 0 * X; Phi = 0 * X
        for M, a, xc, yc in s.gas + s.gal:
            d2 = (X - xc) ** 2 + (Y - yc) ** 2 + Z ** 2 + a * a; rho = rho + 3 * M * MSUN / (4 * math.pi * (a * KPC) ** 3) * (a * a / d2) ** 2.5; Phi = Phi + G * M * MSUN / (np.sqrt(d2) * KPC)
        if form == "BKm":
            gm = 0 * X
            for ctr, lr, tg, tb in s.tab["N2"]: gm = gm + np.interp(np.log(np.maximum(np.sqrt((X - ctr[0]) ** 2 + (Y - ctr[1]) ** 2 + Z ** 2), 0.5)), lr, tg)
            gg = gm; g = gs + gg
        rm = rB * KPC; L_ = dict(gs=gs, gg=gg, gb=g, r=rm, Sig=2 * rm * rho, rho=rho, Phi=np.maximum(Phi, rm * g), G=B.G, c=B.C, a0=a0, rde=B.rde_of(a0)); F = B.ev(sp["F"], L_); m = F / np.maximum(g, 1e-300)
        if form == "BKm": gdir = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); return tuple(gb[i] / np.maximum(gdir, 1e-300) * F - gb[i] for i in range(3))
        return tuple(gb[i] * (m - 1) for i in range(3))
    def extra(s, sp, C, reg=True):''')
    ns = {"__name__": "ux6", "__file__": p}; exec(compile(src, "ux6", "exec"), ns); import bk2_lib as B
    a0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}[foot]; res = []
    SP = {"LAW": dict(form="LAW", k=0.0, a0=a0)}
    for i, f in enumerate(FS): SP[f"F{i}"] = dict(form="BK", k=0.0, a0=a0, F=f); SP[f"M{i}"] = dict(form="BKm", k=0.0, a0=a0, F=f)
    R = ns["run"](SP); law = ns["observe"](*R["LAW"]); o0 = ns["observe"](*R["F0"]); print("known answer LAW vs F0 M300", law["M300"], o0["M300"], "dkappa", law["main"]["dkappa"], o0["main"]["dkappa"], flush=True)
    for i, f in enumerate(FS):
        for t, lab in ((f"F{i}", "present"), (f"M{i}", "carried")):
            o = ns["observe"](*R[t]); res.append(dict(F=f, reading=lab, cls=o["cls"], main=dict(Z=o["main"]["Z"], d_gas=o["main"]["d_gas"], d_bcg=o["main"]["d_bcg"], dk=o["main"]["dkappa"], guard=o["main"]["guard"]), sub=dict(Z=o["sub"]["Z"], d_gas=o["sub"]["d_gas"], d_bcg=o["sub"]["d_bcg"], dk=o["sub"]["dkappa"], guard=o["sub"]["guard"]), M300=o["M300"], ZO3=o["ZO3"])); print(lab, f[:70], o["cls"], "dk", round(o["main"]["dkappa"], 3), round(o["sub"]["dkappa"], 3), "ZO3", np.round(o["ZO3"], 1).tolist(), "Z", round(o["main"]["Z"], 2), round(o["sub"]["Z"], 2), flush=True)
    return res
res = dict(keys=keys, mw=mw, bullet=bullet)[what](); json.dump(res, open(outf, "w"), indent=0, default=float)
