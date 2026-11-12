"""AZ2 (criteria 8c95369a28): CFG681's statistic sqrt X(2.33) = a0(2.33)/a0(0) with the DESI DR2 Lya AP pair
(arXiv:2607.27410 Eq. 26, PROVISIONAL) REPLACING CFG681's Lya pair. Model, data handling and chi^2 copied from
campaign_fresh_gravity/CFG681_bao_raw_geometry/cfg681_bao.py; profile taken directly on the 2.33 node.
Usage: python3 az2_flat_a0.py MODE   with MODE in KA1, KA2, canonical, alt;  MUTATE=1 env shifts new D_H/r_d by -5 sigma."""
import json, os, sys, numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2 as C2
HERE = os.path.dirname(os.path.abspath(__file__)); MODE = sys.argv[1]; MUT = os.environ.get("MUTATE", "") == "1"
A2 = os.environ.get("AZ2_A2", "") == "1"   # AMENDMENT A2 (fbf7814e5d): profile grid augmented around the free X5
A1 = os.environ.get("AZ2_A1", "") == "1"   # AMENDMENT A1 (a3d9e9bf28): free fit re-started from the lowest profile point
EXT = os.path.join(HERE, "..", "..", "..", "_external_data", "pantheonplus_dr")
GAL = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
       ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
       ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500)]
LYA_OLD = ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)   # CFG681 (arXiv 2503.14738)
LYA_NEW = ("Lya", 2.330, 39.32, 0.33, 8.600, 0.066, 0.225)      # arXiv 2607.27410v3 Eq. 26, PROVISIONAL
if MUT: LYA_NEW = ("Lya", 2.330, 39.32, 0.33, 8.600 - 5*0.066, 0.066, 0.225)
BGS0 = (0.295, 7.942, 0.075)
NODES = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]); zg = np.linspace(0, 2.5, 5001)
G, CL = 6.6743e-11, 2.99792458e8; RHOC100 = 3*(1e5/3.0856775814913673e22)**2/(8*np.pi*G)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def omr(h): return 2.469e-5/h**2*(1 + 0.2271*3.046)
def h_footing(a0, om): return float(np.sqrt((2*a0/CL)**2/G/((1 - om)*RHOC100)))
class Model:
    def __init__(s, aniso, bgs, OR): s.aniso, s.bgs, s.OR = aniso, bgs, OR
    def E(s, om, xn, z):
        X = np.interp(z, NODES, np.r_[1.0, xn]); E2 = om*(1+z)**3 + s.OR*(1+z)**4 + (1 - om - s.OR)*X
        return np.sqrt(np.where(E2 > 1e-6, E2, np.nan))
    def I(s, om, xn):
        f = 1/s.E(om, xn, zg); return np.r_[0, np.cumsum(0.5*(f[1:]+f[:-1])*np.diff(zg))]
    def bao(s, om, xn):
        I = s.I(om, xn)
        if not np.all(np.isfinite(I)): return 1e9, None
        ms, ds, Cis = [], [], []
        for (nm, z, dm, sdm, dh, sdh, r) in s.aniso:
            ms.append(np.array([np.interp(z, zg, I), 1/s.E(om, xn, np.array([z]))[0]])); ds.append(np.array([dm, dh]))
            Cis.append(np.linalg.inv(np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])))
        z, dv, sdv = s.bgs; mv = (z*np.interp(z, zg, I)**2/s.E(om, xn, np.array([z]))[0])**(1/3)
        q = (sum(m@Ci@d for m, d, Ci in zip(ms, ds, Cis)) + mv*dv/sdv**2)/(sum(m@Ci@m for m, Ci in zip(ms, Cis)) + mv*mv/sdv**2)
        return sum((d-q*m)@Ci@(d-q*m) for m, d, Ci in zip(ms, ds, Cis)) + ((dv - q*mv)/sdv)**2, q
    def sn(s, om, xn):
        I = s.I(om, xn)
        if not np.all(np.isfinite(I)): return 1e9
        r = mb - 5*np.log10((1 + zhel)*np.interp(zhd, zg, I)); b = one@Cisn@r
        return r@Cisn@r - b*b/A11
    def chi(s, which, om, xn):
        if not (0.15 <= om <= 0.45): return 1e9
        return (s.bao(om, xn)[0] if "bao" in which else 0) + (s.sn(om, xn) if "sn" in which else 0)
# ---- Pantheon+ (as CFG681) ----
raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
cov = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); N = int(round(np.sqrt(cov.size))); cov = cov.reshape(N, N)
sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
zhd, zhel, mb = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float)
Cisn = np.linalg.inv(cov[np.ix_(sel, sel)]); one = np.ones(len(mb)); A11 = one@Cisn@one
def nmp(f, x0):
    r = minimize(f, x0, method="Nelder-Mead", options=dict(maxiter=20000, maxfev=20000, xatol=1e-6, fatol=1e-7))
    return minimize(f, r.x, method="Powell", options=dict(maxiter=20000, xtol=1e-6, ftol=1e-8))
XSTARTS = [np.ones(5), np.linspace(1, 0.7, 5), np.linspace(1, 1.3, 5)]
def fit_free(M, which):           # Om and X free (CFG681 T1/T2)
    best = None
    for om in (0.25, 0.30, 0.35):
        for x in XSTARTS:
            r = nmp(lambda p: M.chi(which, p[0], p[1:]), np.r_[om, x])
            if best is None or r.fun < best.fun: best = r
    return best
def fit_const(M, which):
    return minimize(lambda p: M.chi(which, p[0], np.ones(5)), [0.30], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-6))
def fit_omfix(M, which, om):
    best = None
    for x in XSTARTS:
        r = nmp(lambda p: M.chi(which, om, p), x)
        if best is None or r.fun < best.fun: best = r
    return best
def profile(M, which, om, x5s, xfree):
    out = {}; cur = xfree[:4].copy()
    for v in sorted(x5s, key=lambda v: abs(v - xfree[4])):
        best = None
        for st in (cur, xfree[:4], np.ones(4), np.linspace(1, v, 6)[1:5]):
            r = nmp(lambda p: M.chi(which, om, np.r_[p, v]), np.array(st, float))
            if best is None or r.fun < best.fun: best = r
        out[float(v)] = (float(best.fun), best.x.tolist()); cur = best.x
    return out
def ap_T3(M):
    def c(om):
        I = M.I(om, np.ones(5)); s = 0; pl = []
        for (nm, z, dm, sdm, dh, sdh, r) in M.aniso:
            F = dm/dh; sF = F*np.sqrt((sdm/dm)**2 + (sdh/dh)**2 - 2*r*sdm*sdh/(dm*dh))
            pl.append((F - np.interp(z, zg, I)*M.E(om, np.ones(5), np.array([z]))[0])/sF); s += pl[-1]**2
        return s, pl
    r = minimize(lambda p: c(p[0])[0] if 0.15 <= p[0] <= 0.45 else 1e9, [0.3], method="Nelder-Mead"); s, pl = c(r.x[0])
    return dict(om=float(r.x[0]), chi2=float(s), p=float(C2.sf(s, 5)), pulls=dict(zip([a[0] for a in M.aniso], map(float, pl))))
def label(Db, Dr):
    if Db >= 9: return "FLAT FAILS"
    if Db < 4 and Dr < 4: return "NO POWER"
    if Db < 4: return "FLAT HOLDS"
    return "FLAT HOLDS (HINT)" if Dr >= 4 else "NO POWER"
BAND = [0.81, 0.86, 0.91, 0.96, 1.0, 1.05, 1.10, 1.16, 1.21]; COARSE = list(np.arange(-1.0, 15.01, 0.5))
def cell(M, which, om):
    ff = fit_omfix(M, which, om); xf = np.array(ff.x); rival = om*3.33**3 + M.OR*3.33**4 + (1 - om - M.OR)
    extra = [round(float(xf[4]) + d, 4) for d in np.arange(-0.5, 0.501, 0.05)] if A2 else []
    pr = profile(M, which, om, sorted(set(BAND + COARSE + [round(rival, 4)] + extra)), xf)
    pmin = min(v[0] for v in pr.values())
    if A1:
        kb = min(pr, key=lambda k: pr[k][0]); r = nmp(lambda p: M.chi(which, om, p), np.r_[pr[kb][1], kb])
        if r.fun < ff.fun: ff = r
        xf = np.array(ff.x)
    fmin = min(ff.fun, pmin)
    D = {k: v[0] - fmin for k, v in pr.items()}
    Db = min(D[b] for b in BAND); Dr = D[round(rival, 4)]; Dt = None
    ks = np.array(sorted(D)); ds = np.array([D[k] for k in ks])
    def ivl(lv):
        ok = ks[ds <= lv]; return [float(ok.min()), float(ok.max())] if len(ok) else [None, None]
    return dict(chi2_free=float(ff.fun), chi2_prof_min=float(pmin), ka3_gap=float(ff.fun - pmin), X_nodes=xf.tolist(),
                X5_best=float(xf[4]), sqrtX_best=float(np.sqrt(max(xf[4], 0))), D_band=float(Db), D_flat_X1=float(D[1.0]),
                X5_rival=float(rival), sqrtX_rival=float(np.sqrt(rival)), D_rival=float(Dr),
                X5_ci68=ivl(1.0), X5_ci95=ivl(4.0), label=label(Db, Dr), profile={str(k): v for k, v in sorted(D.items())})
res = dict(mode=MODE, mutate=MUT)
if MODE == "KA1":
    M = Model(GAL + [LYA_OLD], BGS0, omr(0.68))
    for tag, w in [("T1", ["bao"]), ("T2", ["bao", "sn"])]:
        f0, f1 = fit_const(M, w), fit_free(M, w)
        fx = {str(om): float(np.sqrt(max(fit_omfix(M, w, om).x[4], 0))) for om in (0.25, 0.30, 0.35)}
        res[tag] = dict(dchi2=float(f0.fun - f1.fun), chi2_const=float(f0.fun), chi2_free=float(f1.fun), sqrtX233_fixed_om=fx)
        print(tag, res[tag], flush=True)
    res["T3"] = ap_T3(M); print("T3", res["T3"])
    tgt = dict(T1=(7.41, [1.93, 1.14, 0.00]), T2=(12.08, [1.97, 1.24, 0.00]))
    ok = abs(res["T3"]["chi2"] - 5.98) <= 0.05
    for t, (d, s3) in tgt.items():
        ok &= abs(res[t]["dchi2"] - d) <= 0.10
        ok &= all(abs(res[t]["sqrtX233_fixed_om"][k] - v) <= 0.05 for k, v in zip(("0.25", "0.3", "0.35"), s3))
    res["KA1_pass"] = bool(ok); print("KA1", "PASS" if ok else "FAIL")
elif MODE == "KA2":
    M0 = Model(GAL + [LYA_NEW], BGS0, omr(0.68)); om = 0.30; _, q = M0.bao(om, np.ones(5)); I = M0.I(om, np.ones(5))
    an = [(nm, z, q*np.interp(z, zg, I), sdm, q/M0.E(om, np.ones(5), np.array([z]))[0], sdh, r) for (nm, z, dm, sdm, dh, sdh, r) in M0.aniso]
    zb, dv, sdv = BGS0; bg = (zb, q*(zb*np.interp(zb, zg, I)**2/M0.E(om, np.ones(5), np.array([zb]))[0])**(1/3), sdv)
    M = Model(an, bg, omr(0.68)); c = cell(M, ["bao"], om); res["T1_om0.30"] = c
    res["KA2_pass"] = bool(c["D_band"] < 0.05 and abs(c["sqrtX_best"] - 1) <= 0.03); print("KA2", c["D_band"], c["sqrtX_best"], res["KA2_pass"])
else:
    a0 = A0[MODE]; res["a0_footing"] = a0; res["rho_DE0"] = (2*a0/CL)**2/G; res["cells"] = {}
    for om in (0.25, 0.30, 0.35):
        h = h_footing(a0, om); M = Model(GAL + [LYA_NEW], BGS0, omr(h))
        for tag, w in [("T1", ["bao"]), ("T2", ["bao", "sn"])]:
            c = cell(M, w, om); c["h_footing"] = h; c["a0_233"] = a0*c["sqrtX_best"]; res["cells"][f"{tag}_om{om:.2f}"] = c
            print(MODE, tag, om, "h", round(h, 4), "sqrtX", round(c["sqrtX_best"], 3), "Db", round(c["D_band"], 2), "Dr", round(c["D_rival"], 1),
                  "ci95 X5", c["X5_ci95"], "gap", round(c["ka3_gap"], 3), c["label"], flush=True)
    if not MUT:
        M = Model(GAL + [LYA_NEW], BGS0, omr(h_footing(a0, 0.30)))   # Om-profiled row, reported only (Or at Om 0.30's h)
        for tag, w in [("T1", ["bao"]), ("T2", ["bao", "sn"])]:
            f1 = fit_free(M, w); best1 = None
            for om in (0.25, 0.30, 0.35):
                r = nmp(lambda p: M.chi(w, p[0], np.r_[p[1:], 1.0]), np.r_[om, np.ones(4)])
                if best1 is None or r.fun < best1.fun: best1 = r
            f0 = fit_const(M, w)
            res[f"{tag}_om_profiled"] = dict(om_free=float(f1.x[0]), sqrtX_best=float(np.sqrt(max(f1.x[5], 0))), D_X5eq1=float(best1.fun - f1.fun),
                                             dchi2_const_vs_free=float(f0.fun - f1.fun), p_5dof=float(C2.sf(max(f0.fun - f1.fun, 0), 5)))
            print(MODE, tag, "Om profiled", res[f"{tag}_om_profiled"], flush=True)
        res["T3"] = ap_T3(M); print("T3", res["T3"])
    hc = res["cells"]["T2_om0.30"]["label"]; labs = {res["cells"][f"T2_om{o:.2f}"]["label"] for o in (0.25, 0.30, 0.35)}
    res["headline"] = hc + (" / EXPANSION-MODEL DEPENDENT" if len(labs) > 1 else ""); print("HEADLINE", MODE, res["headline"])
out = f"az2_{MODE}" + ("_MUTATE" if MUT else "") + ("_A1" if A1 else "") + ("_A2" if A2 else "") + ".json"
json.dump(res, open(os.path.join(HERE, out), "w"), indent=1)
