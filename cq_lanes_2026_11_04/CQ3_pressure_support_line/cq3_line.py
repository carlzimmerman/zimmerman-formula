#!/usr/bin/env python3
"""CQ3: do the four dispersion-support excesses (VS1, HX1, KU1/KU2, CW6) fall on ONE line E = k P of one pressure variable P?
FROZEN_CRITERIA.md (963bc31242). python3 -I cq3_line.py [--mutate]. One thread. kappa = 1/2 FITTED; not theory closed.
No downloads: sockets are disabled. Inputs are on-disk lane outputs and the MaNGA DynPop table KU1 already reads."""
import json, math, os, sys, socket
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
def _no_net(*a, **k): raise RuntimeError("network disabled: CQ3 makes no downloads")
socket.socket.connect = _no_net
import numpy as np
from astropy.io import fits
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RB = os.path.join(REPO, "rebuild_2026_10_22"); HX = os.path.join(RB, "HX1_hot_ladder")
MUT = "--mutate" in sys.argv; SFX = "_MUTATE" if MUT else ""
OUT = []; RES = {"mode": "mutate" if MUT else "normal"}; fail = 0
def P(s=""): print(s, flush=True); OUT.append(s)
LN10 = math.log(10.0); FEET = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G, MS, MPC, CKMS, H0 = 6.6743e-11, 1.98892e30, 3.0857e22, 2.99792458e5, 70.0; NB = 300; KE = 1.1

def Pmap(lam, ke=KE):
    l = np.clip(np.asarray(lam, float), 0.0, 0.999); a = ke ** 2 * (1 - l ** 2); return a / (a + l ** 2)
def Pmap_1ml(lam): return 1.0 - np.clip(np.asarray(lam, float), 0.0, 1.0)

# ------------------------------------------------------------------ S3 and the DynPop population (KU1's code, verbatim logic)
F = os.path.join(REPO, "_external_data", "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits")
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / y)
with fits.open(F) as h:
    d = h[1].data
    lam, eps, sig, me, msr, z, q = (np.array(d[k], float) for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "nsa_elpetro_mass", "nsa_sersic_mass", "z", "Qual"))
    absm = np.array(d["nsa_elpetro_absmag"], float)
    MT = np.array([np.array(h[i].data["log_Mt_rhalf"], float) for i in range(2, 12)]); RH = np.array([np.array(h[i].data["rhalf_arcsec"], float) for i in range(2, 12)])
if absm.ndim != 2 or absm.shape[1] != 7: raise SystemExit("NOT EVALUABLE: nsa_elpetro_absmag is not a 7-vector")
nfin = np.sum(np.isfinite(MT) & np.isfinite(RH) & (RH > 0), axis=0)
sel = (q >= 1) & np.isfinite(me) & (me > 0) & np.isfinite(msr) & (z > 0.005) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & (nfin >= 8)
lam, eps, sig, me, msr, z, absm, MT, RH = lam[sel], eps[sel], sig[sel], me[sel], msr[sel], z[sel], absm[sel], MT[:, sel], RH[:, sel]
slow = (lam < 0.08 + eps / 4) & (eps < 0.4); n = len(z)
DA = CKMS * z / H0 / (1 + z) * MPC
def accel(mt_log, rh_arcsec, mstar_log):
    r = rh_arcsec * math.pi / 648000 * DA; return G * 10 ** mt_log * MS / r ** 2, G * 0.5 * 10 ** mstar_log * MS / r ** 2
def resid(go, gb, a0): return np.log(go) - np.log(nu(gb / a0) * gb)
mtm = np.nanmedian(MT, axis=0); rhm = np.nanmedian(RH, axis=0)
go, gb = accel(mtm, rhm, me); okc = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
rr0 = np.full(n, np.nan); rr0[okc] = resid(go[okc], gb[okc], FEET["canonical"]); gmask = np.isfinite(rr0)       # the working population
colr = absm[:, 2] - absm[:, 4]; cfin = np.isfinite(colr); red = gmask & cfin & (colr > 2.0); blue = gmask & cfin & (colr <= 2.0)
P("CQ3 pressure-support line (FROZEN_CRITERIA.md 963bc31242, AMENDMENT_A1.md 33ec245b34). kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Footings never pooled.")
P(f"DynPop population: {int(gmask.sum())} galaxies with finite residual (KU1 selection {n}); slow {int((slow & gmask).sum())}, fast {int((~slow & gmask).sum())}; u-r finite {int((gmask & cfin).sum())}, red {int(red.sum())}, blue {int(blue.sum())}")

def ku_class_E(lm, a0, mt, rh, mask):
    g_o, g_b = accel(mt, rh, lm); ok = np.isfinite(g_o) & np.isfinite(g_b) & (g_o > 0) & (g_b > 0) & mask
    r = np.full(n, np.nan); r[ok] = resid(g_o[ok], g_b[ok], a0); return r
def cls_med(r, c):
    x = r[c & np.isfinite(r)]; return float(np.median(x)) / LN10

cell = np.floor(me / 0.2).astype(int) * 1000 + np.floor(np.log10(sig) / 0.1).astype(int); Pall = Pmap(lam); _num = _den = 0.0
for _c in np.unique(cell[gmask]):
    _ii = np.where((cell == _c) & gmask)[0]; _s = slow[_ii]; _ns = int(_s.sum()); _nf = len(_ii) - _ns
    if _ns >= 2 and _nf >= 2: _w = min(_ns, _nf); _num += _w * (Pall[_ii][_s].mean() - Pall[_ii][~_s].mean()); _den += _w
dP_matched = _num / _den if _den else float("nan")
# ------------------------------------------------------------------ S2: HX1's own text through `tian` (output file line swapped for a null file)
txt = open(os.path.join(HX, "hx1_ladder.py")).read().split("\n")
assert "return O, inv(" in txt[36], "HX1 line 37 is not the end of tian()"
head = "\n".join(txt[:37]); old = 'OUT = open(os.path.join(HERE, f"hx1_ladder{TAG}.out"), "w")'; assert old in head
head = head.replace(old, 'OUT = open(os.devnull, "w")')
ns = {"__file__": os.path.join(HX, "hx1_ladder.py"), "__name__": "hx1_in_cq3"}; cwd0 = os.getcwd(); argv0 = list(sys.argv); os.chdir(HX); sys.argv = ["hx1_ladder.py"]
exec(compile(head, os.path.join(HX, "hx1_ladder.py"), "exec"), ns)
os.chdir(cwd0); sys.argv = argv0
tian = ns["tian"]
hxj = json.load(open(os.path.join(HX, "hx1_ladder.json")))["footings"]
vs = json.load(open(os.path.join(RB, "VS1_rotation_split", "vs1.json")))
ku1j = json.load(open(os.path.join(RB, "KU1_kappa_universality_rotators", "ku1.json")))
cwj = json.load(open(os.path.join(REPO, "cw_lanes_2026_11_04", "CW6_lensing_measured_gas", "cw6_b21c.json")))["prof"]["FIXED"]
try: ku2j = json.load(open(os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.json")))
except Exception: ku2j = {}
cw_readme = {"canonical": (1.313, 0.878), "alt": (1.200, 0.802)}

def build(foot):
    """Returns the ten points for one footing: dict(sid, name, lam (member lambda arrays), E, s_stat, s_sys), plus K1 records."""
    a0 = FEET[foot]; pts = []; k1 = []; rng = np.random.default_rng(20261104)
    # S1 VS1
    pg = vs[foot]["per_galaxy"]; off = np.array([v[0] for v in pg.values()]); lamv = np.array([v[3] for v in pg.values()]); sl = np.array([v[2] for v in pg.values()], bool)
    for nm, m in (("slow", sl), ("fast", ~sl)):
        x = off[m]; pts.append(dict(sid="S1 VS1", name=nm, lam=lamv[m], E=float(x.mean()), s_stat=float(x.std(ddof=1) / math.sqrt(len(x))), s_sys=0.0, n=int(m.sum())))
    k1.append(("VS1 mean slow", pts[0]["E"], vs[foot]["mean_slow"], 1e-3)); k1.append(("VS1 mean fast", pts[1]["E"], vs[foot]["mean_fast"], 1e-3))
    # S2 HX1
    O, B, kk, sN, sL, sO = tian("MaNGA elliptical", a0); Eg = np.log10(sO / sL); qd = np.percentile(kk, [25, 50, 75]); edges = [0.0, *map(float, qd), 1e9]
    tp = tian("MaNGA elliptical", a0, 0.10); tm = tian("MaNGA elliptical", a0, -0.10); Ep = np.log10(tp[5] / tp[4]); Em = np.log10(tm[5] / tm[4])
    for j in range(4):
        lo, hi = edges[j], edges[j + 1]; m = (kk > lo) & (kk <= hi); x = Eg[m]
        bs = [np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(NB)]
        pop = gmask & red & (sig > lo) & (sig <= hi)
        pts.append(dict(sid="S2 HX1", name=f"MaNGA Q{j + 1}", lam=lam[pop], E=float(np.median(x)), s_stat=float(np.std(bs)), s_sys=float(abs(np.median(Ep[m]) - np.median(Em[m])) / 2), n=int(m.sum()), n_dyn=int(pop.sum()), sig_lo=lo, sig_hi=hi))
        k1.append((f"HX1 Q{j + 1} median B_need", float(np.median(B[m])), hxj[foot]["rungs"][f"MaNGA Q{j + 1}"]["Bmed"], 1e-9 * max(1.0, float(np.median(B[m])))))
    # S3 KU
    rk = ku_class_E(me, a0, mtm, rhm, gmask); rks = ku_class_E(msr, a0, mtm, rhm, gmask)
    rmod = [ku_class_E(me, a0, MT[k], RH[k], gmask) for k in range(10)]
    rngk = np.random.default_rng(20261105)
    for nm, c in (("slow", slow & gmask), ("fast", ~slow & gmask)):
        x = rk[c] / LN10; E = float(np.median(x)); bs = [np.median(x[rngk.integers(0, len(x), len(x))]) for _ in range(NB)]
        sm = float(np.std([cls_med(r, c) for r in rmod])); dM = abs(cls_med(rks, c) - E)
        pts.append(dict(sid="S3 KU", name=nm, lam=lam[c], E=E, s_stat=float(np.std(bs)), s_sys=math.hypot(sm, dM), n=int(c.sum()), s_models=sm, s_mstar=dM, E_h70=cls_med(ku_class_E(me + 0.31, a0, mtm, rhm, gmask), c)))
        k1.append((f"KU1 abs median {nm} (ln)", E * LN10, ku1j[foot]["abs_median_" + nm], 1e-6))
    # S4 CW6
    for nm, key, msk in (("red", "red", red), ("blue", "blue", blue)):
        A, sA = cwj[foot][key]["A"], cwj[foot][key]["sA"]
        pts.append(dict(sid="S4 CW6", name=nm, lam=lam[msk], E=math.log10(A), s_stat=sA / (A * LN10), s_sys=0.0, n=int(msk.sum()), A=A, sA=sA))
    k1.append(("CW6 A red", cwj[foot]["red"]["A"], cw_readme[foot][0], 1e-3)); k1.append(("CW6 A blue", cwj[foot]["blue"]["A"], cw_readme[foot][1], 1e-3))
    return pts, k1

def covmat(pts):
    N = len(pts); C = np.zeros((N, N)); sid = [p["sid"] for p in pts]
    for i in range(N):
        C[i, i] = pts[i]["s_stat"] ** 2
        for j in range(N):
            if sid[i] == sid[j]: C[i, j] += pts[i]["s_sys"] * pts[j]["s_sys"]
    return C
def gls(E, Pv, C):
    Ci = np.linalg.inv(C); w = float(Pv @ Ci @ Pv); k = float(Pv @ Ci @ E) / w; r = E - k * Pv; return k, w ** -0.5, float(r @ Ci @ r)
def grade(E, Pv, C, sid):
    k, sk, chi2 = gls(E, Pv, C); dof = len(E) - 1; p = float(stats.chi2.sf(chi2, dof)); per = {}
    for s in dict.fromkeys(sid):
        ix = [i for i, x in enumerate(sid) if x == s]; ks, sks, _ = gls(E[ix], Pv[ix], C[np.ix_(ix, ix)]); per[s] = dict(k=ks, sk=sks, z=(ks - k) / sks)
    if not np.all(np.isfinite([k, sk, chi2, p])) or not np.all(np.isfinite(Pv)) or not np.all(np.isfinite(E)): lab = "NOT EVALUABLE"
    elif k / sk < 2: lab = "NOT EVALUABLE"
    elif p >= 0.05 and all(abs(v["z"]) <= 2 for v in per.values()): lab = "ONE LINE"
    else: lab = "NOT ONE LINE"
    br = [s for s, v in per.items() if abs(v["z"]) > 2]
    return dict(k=k, sk=sk, k_over_sk=k / sk, chi2=chi2, dof=dof, p=p, per=per, label=lab, breakers=br)

RES["notes"] = "kappa = 1/2 FITTED; not theory closed"
permseed = np.random.default_rng(20261104).permutation(10)
for foot in FEET:
    P(f"\n=================== [{foot}] a0 = {FEET[foot]:.4e}")
    pts, k1 = build(foot); N = len(pts); sid = [p["sid"] for p in pts]; C = covmat(pts)
    ok1 = True
    for nm, got, ref, tol in k1:
        ok = abs(got - ref) <= tol; ok1 &= ok; P(f"  K1 {nm}: got {got:.6g}, ref {ref:.6g}, |d| {abs(got - ref):.2e} (tol {tol:.0e}) {'PASS' if ok else 'FAIL'}")
    fail += (not ok1); small = [p["sid"] + " " + p["name"] for p in pts if p["sid"] != "S1 VS1" and len(p["lam"]) < 30]   # A1: floor on the DynPop reference population only
    Pv = np.array([float(np.mean(Pmap(p["lam"]))) for p in pts]); E = np.array([p["E"] for p in pts])
    if small: P(f"  points below 30 members: {small}")
    if MUT: Pv = Pv[permseed]; P("  [MUTATE: P shuffled across the ten points, seed 20261104]")
    P(f"  {'sample':7s} {'point':9s} {'n':>5s} {'P':>7s} {'E dex':>8s} {'stat':>7s} {'sys':>7s}")
    for p, pv in zip(pts, Pv): P(f"  {p['sid']:7s} {p['name']:9s} {p['n']:5d} {pv:7.3f} {p['E']:+8.4f} {p['s_stat']:7.4f} {p['s_sys']:7.4f}")
    g = grade(E, Pv, C, sid)
    if small: g["label"] = "NOT EVALUABLE"
    P(f"  joint k = {g['k']:.4f} +- {g['sk']:.4f} dex per unit P (k/sigma {g['k_over_sk']:.2f}); chi2 {g['chi2']:.2f} / {g['dof']}, p {g['p']:.2e}")
    for s, v in g["per"].items(): P(f"    {s}: own k {v['k']:+.4f} +- {v['sk']:.4f}, z against joint {v['z']:+.2f}")
    P(f"  LABEL [{foot}]: {g['label']}" + (f"   breakers: {', '.join(g['breakers'])}" if g["breakers"] else ""))
    # --- K2 planted line and shuffle share; MUTATE share
    rng = np.random.default_rng(20261106); Pr = np.array([float(np.mean(Pmap(p["lam"]))) for p in pts]); NS = 2000
    draws = rng.multivariate_normal(0.2 * Pr, C, size=NS); hit = 0; hit_sh = 0
    for dr in draws:
        hit += grade(dr, Pr, C, sid)["label"] == "ONE LINE"; hit_sh += grade(dr, rng.permutation(Pr), C, sid)["label"] == "ONE LINE"
    mshare = 0
    for _ in range(NS): mshare += grade(E, rng.permutation(Pr), C, sid)["label"] == "ONE LINE"
    k2a, k2b = hit / NS, hit_sh / NS; ok2 = (k2a >= 0.70) and (k2b <= 0.10); fail += (not ok2)
    P(f"  K2 planted E = 0.2 P + noise from C: ONE LINE in {k2a:.3f} of {NS} (need >= 0.70); same draws with P shuffled {k2b:.3f} (need <= 0.10): {'PASS' if ok2 else 'FAIL'}")
    P(f"  MUTATE share: real E, P shuffled across the ten points, {mshare / NS:.4f} of {NS} read ONE LINE")
    # --- beside, not graded
    P("  --- beside, not graded")
    def sub(drop, tag, Pvec=None):
        keep = [i for i in range(N) if sid[i] not in drop]; Pu = Pv if Pvec is None else Pvec
        gg = grade(E[keep], Pu[keep], C[np.ix_(keep, keep)], [sid[i] for i in keep])
        P(f"  {tag}: k {gg['k']:.4f} +- {gg['sk']:.4f} (k/sigma {gg['k_over_sk']:.1f}), chi2 {gg['chi2']:.2f}/{gg['dof']} p {gg['p']:.2e}, {gg['label']}" + (f"; breakers {', '.join(gg['breakers'])}" if gg["breakers"] else "")); return gg
    gA = sub({"S3 KU"}, "(a) without S3"); gB = sub({"S2 HX1"}, "(a) without S2"); gC = sub({"S2 HX1", "S3 KU"}, "(a) S1 + S4 only"); gD = sub({"S1 VS1", "S4 CW6"}, "(a) S2 + S3 only")
    P("  (b) E / P per point: " + "; ".join(f"{p['sid'][:2]} {p['name']} {p['E'] / pv:+.3f}" for p, pv in zip(pts, Pv)))
    E70 = E.copy(); ix3 = [i for i in range(N) if sid[i] == "S3 KU"]
    for i in ix3: E70[i] = pts[i]["E_h70"]
    g70 = grade(E70, Pv, C, sid); P(f"  (c) S3 with NSA masses read h = 0.7 (+0.31 dex, LAM9): S3 E {E70[ix3[0]]:+.3f} slow, {E70[ix3[1]]:+.3f} fast; all ten: k {g70['k']:.4f} +- {g70['sk']:.4f}, chi2 {g70['chi2']:.2f}/{g70['dof']} p {g70['p']:.2e}, {g70['label']}" + (f"; breakers {', '.join(g70['breakers'])}" if g70["breakers"] else ""))
    P70 = np.array([float(np.mean(Pmap_1ml(p["lam"]))) for p in pts]); gE = grade(E, P70, C, sid)
    P(f"  (d) P = 1 - lambda_Re: P " + " ".join(f"{x:.2f}" for x in P70) + f"; k {gE['k']:.4f} +- {gE['sk']:.4f}, chi2 {gE['chi2']:.2f}/{gE['dof']} p {gE['p']:.2e}, {gE['label']}" + (f"; breakers {', '.join(gE['breakers'])}" if gE["breakers"] else ""))
    Ci = np.linalg.inv(C); X = np.column_stack([np.ones(N), Pv]); cov = np.linalg.inv(X.T @ Ci @ X); beta = cov @ X.T @ Ci @ E; ra = E - X @ beta; chia = float(ra @ Ci @ ra)
    P(f"  (e) affine E = E0 + kP: E0 {beta[0]:+.3f} +- {math.sqrt(cov[0, 0]):.3f}, k {beta[1]:+.3f} +- {math.sqrt(cov[1, 1]):.3f}, chi2 {chia:.2f}/{N - 2} p {stats.chi2.sf(chia, N - 2):.2e}")
    dsc = vs[foot]["discs"]; Pd = (11.0 / 200.0) ** 2; pred = g["k"] * Pd
    P(f"  (f) SPARC disc arm: E {dsc['mean']:+.3f} +- {dsc['sem']:.3f}; line at P_disc {Pd:.4f}: {pred:+.4f}; z {(dsc['mean'] - pred) / dsc['sem']:+.2f}")
    # (g) the remaining pairs, (h) post-hoc calibration-free slopes
    for a_, b_ in (("S1 VS1", "S2 HX1"), ("S1 VS1", "S3 KU"), ("S2 HX1", "S4 CW6"), ("S3 KU", "S4 CW6")): sub(set(sid) - {a_, b_}, f"(g) {a_[:2]} + {b_[:2]} only")
    sl_ = {}
    for s_ in dict.fromkeys(sid):
        ix = [i for i in range(N) if sid[i] == s_]; Cis = np.linalg.inv(C[np.ix_(ix, ix)]); Xs = np.column_stack([np.ones(len(ix)), Pv[ix]]); cv = np.linalg.inv(Xs.T @ Cis @ Xs); bt = cv @ Xs.T @ Cis @ E[ix]; sl_[s_] = (float(bt[1]), math.sqrt(cv[1, 1]))
    comb = dict(sl_); txt_h = "; ".join(f"{k_[:2]} {v_[0]:+.2f} +- {v_[1]:.2f}" for k_, v_ in sl_.items())
    try:
        D2, sD2 = ku2j[foot]["D"], ku2j[foot]["sigma_D"]; comb["S3 KU"] = (D2 / LN10 / dP_matched, sD2 / LN10 / dP_matched)
        txt_h += f"; S3 matched (KU2 D {D2:+.3f} ln +- {sD2:.3f} over matched dP {dP_matched:+.3f}) {comb['S3 KU'][0]:+.2f} +- {comb['S3 KU'][1]:.2f}"
    except Exception as ex_: txt_h += f"; S3 matched unavailable ({ex_!r})"
    wv = np.array([1 / v_[1] ** 2 for v_ in comb.values()]); sv = np.array([v_[0] for v_ in comb.values()]); sbar = float((wv * sv).sum() / wv.sum()); chih = float((wv * (sv - sbar) ** 2).sum()); ph = float(stats.chi2.sf(chih, len(sv) - 1))
    P(f"  (h) POST-HOC, calibration-free, not graded: dE/dP inside each sample (free intercept): {txt_h}; common slope {sbar:+.2f} +- {wv.sum() ** -0.5:.2f}, chi2 {chih:.1f}/{len(sv) - 1}, p {ph:.2e}")
    extra = dict(slopes={k_: list(v_) for k_, v_ in comb.items()}, dP_matched=dP_matched, common=sbar, chi2=chih, p=ph); RES.setdefault("extra", {})[foot] = extra
    RES[foot] = dict(points=[{k: (v if not isinstance(v, np.ndarray) else None) for k, v in p.items() if k != "lam"} | dict(P=float(pv)) for p, pv in zip(pts, Pv)], k1=[dict(name=a, got=b, ref=c_, tol=d_) for a, b, c_, d_ in k1], fit={k: v for k, v in g.items()},
                     K2=dict(planted_share=k2a, shuffled_share=k2b, ok=bool(ok2)), mutate_share=mshare / NS,
                     beside=dict(no_S3=gA["label"], no_S2=gB["label"], S1_S4=gC["label"], S2_S3=gD["label"], h70=dict(k=g70["k"], p=g70["p"], label=g70["label"]), one_minus_lambda=dict(k=gE["k"], p=gE["p"], label=gE["label"]),
                                 affine=dict(E0=float(beta[0]), k=float(beta[1]), p=float(stats.chi2.sf(chia, N - 2))), disc=dict(E=dsc["mean"], sem=dsc["sem"], line=pred)))
RES["failed_checks"] = int(fail)
P(f"\nfailed checks: {fail}")
P("LABELS: " + "; ".join(f"{f} {RES[f]['fit']['label']}" for f in FEET))
open(os.path.join(HERE, f"cq3_line{SFX}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"cq3_line{SFX}.json"), "w"), indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
sys.exit(1 if (MUT or fail) else 0)
