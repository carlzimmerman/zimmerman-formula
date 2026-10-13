"""CFG681 (criteria fe91fd3bc): BAO from raw distances only. DESI DR2 BAO (arXiv 2503.14738 Table) + Pantheon+ shape
(STAT+SYS cov, sha256 abf806d9...). No CMB, no CPL, no LCDM model: dark energy X(z) = rho_DE(z)/rho_DE(0) piecewise-linear.
MUTATE=M1 (DESI -> its own X=1 best fit), MUTATE=M2 (inject eps=0.10 into SN distances)."""
import json, os, sys, numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE", "")
EXT = os.path.join(HERE, "..", "..", "..", "_external_data", "pantheonplus_dr")
# ---- DESI DR2 (Table, arXiv 2503.14738v2): z, D_M/r_d, sig, D_H/r_d, sig, r ----
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)
NODES = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]); h = 0.68; OMR = 2.469e-5 / h**2 * (1 + 0.2271 * 3.046)
zg = np.linspace(0, 2.5, 5001)
def Efun(om, xn, z):
    X = np.interp(z, NODES, np.r_[1.0, xn]); E2 = om*(1+z)**3 + OMR*(1+z)**4 + (1 - om - OMR)*X
    return np.sqrt(np.where(E2 > 1e-6, E2, np.nan))
def Igrid(om, xn):
    E = Efun(om, xn, zg); f = 1/E; I = np.r_[0, np.cumsum(0.5*(f[1:]+f[:-1])*np.diff(zg))]; return I
def bao_chi2(om, xn, data=None):
    I = Igrid(om, xn)
    if not np.all(np.isfinite(I)): return 1e9, None
    ms, ds, Cis = [], [], []
    for (nm, z, dm, sdm, dh, sdh, r) in (data or ANISO):
        m = np.array([np.interp(z, zg, I), 1/Efun(om, xn, np.array([z]))[0]]); C = np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])
        ms.append(m); ds.append(np.array([dm, dh])); Cis.append(np.linalg.inv(C))
    z, dv, sdv = BGS; Iz = np.interp(z, zg, I); mv = (z*Iz**2/Efun(om, xn, np.array([z]))[0])**(1/3)
    num = sum(m@Ci@d for m, d, Ci in zip(ms, ds, Cis)) + mv*dv/sdv**2; den = sum(m@Ci@m for m, Ci in zip(ms, Cis)) + mv*mv/sdv**2
    q = num/den
    chi = sum((d-q*m)@Ci@(d-q*m) for m, d, Ci in zip(ms, ds, Cis)) + ((dv - q*mv)/sdv)**2
    return chi, q
# ---- Pantheon+ ----
cols = open(os.path.join(EXT, "PantheonPlusSH0ES.dat")).readline().split()
raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
covfull = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); N = int(round(np.sqrt(covfull.size))); covfull = covfull.reshape(N, N)
sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
zhd, zhel, mb = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float); Csn = covfull[np.ix_(sel, sel)]
if MUT == "M2": mb = mb + 5*0.10*np.log10(1 + zhd)
Cisn = np.linalg.inv(Csn); one = np.ones(len(mb)); A11 = one@Cisn@one
def sn_chi2(om, xn):
    I = Igrid(om, xn)
    if not np.all(np.isfinite(I)): return 1e9
    mu = 5*np.log10((1 + zhel)*np.interp(zhd, zg, I)); r = mb - mu; b = one@Cisn@r
    return r@Cisn@r - b*b/A11
def fit(which, fixX=False, om_fix=None, extra=None, data=None, start=None):
    def f(p):
        om = om_fix if om_fix is not None else p[0]; xn = np.ones(5) if fixX else (p[1:] if om_fix is None else p)
        if not (0.15 <= om <= 0.45): return 1e9
        c = 0.0
        if "bao" in which: c += bao_chi2(om, xn, data)[0]
        if "sn" in which: c += sn_chi2(om, xn)
        if extra: c += extra(om, xn)
        return c
    best = None
    starts = [[0.30]] if fixX else [[om] + list(x) for om in (0.25, 0.30, 0.35) for x in (np.ones(5), np.linspace(1, 0.7, 5), np.linspace(1, 1.3, 5))]
    if om_fix is not None: starts = [s[1:] for s in starts] if not fixX else [[0]]
    if start is not None: starts = [list(start)]
    for s in starts:
        if fixX and om_fix is None:
            r = minimize(lambda p: f(p), s, method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-6))
        else:
            r = minimize(f, s, method="Nelder-Mead", options=dict(maxiter=20000, maxfev=20000, xatol=1e-6, fatol=1e-7))
            r = minimize(f, r.x, method="Powell", options=dict(maxiter=20000, xtol=1e-6, ftol=1e-8))
        if best is None or r.fun < best.fun: best = r
    return best
def sig_equiv(dchi2, dof):
    from scipy.stats import chi2, norm
    p = chi2.sf(max(dchi2, 0), dof); return float(p), float(norm.isf(p/2)) if p > 0 else 99.0
res = {"mutate": MUT}
data = None
if MUT == "M1":
    b = fit(["bao"], fixX=True); om = b.x[0]; _, q = bao_chi2(om, np.ones(5)); I = Igrid(om, np.ones(5))
    data = [(nm, z, q*np.interp(z, zg, I), sdm, q/Efun(om, np.ones(5), np.array([z]))[0], sdh, r) for (nm, z, dm, sdm, dh, sdh, r) in ANISO]
    zb_, dv, sdv = BGS; BGS = (zb_, q*(zb_*np.interp(zb_, zg, I)**2/Efun(om, np.ones(5), np.array([zb_]))[0])**(1/3), sdv)
def xat(p, z): return float(np.interp(z, NODES, np.r_[1.0, p[1:]]))
for tag, which in [("T1_BAO", ["bao"]), ("T2_BAO+SN", ["bao", "sn"])]:
    f0 = fit(which, fixX=True, data=data); f1 = fit(which, data=data)
    d = f0.fun - f1.fun; p, s = sig_equiv(d, 5)
    out = dict(chi2_const=float(f0.fun), om_const=float(f0.x[0]), chi2_free=float(f1.fun), om_free=float(f1.x[0]), X_nodes=f1.x[1:].tolist(), dchi2=float(d), p=p, sigma_equiv=s)
    if MUT != "M2":
        # profile-likelihood intervals of sqrt X at the frozen redshifts
        band = {}
        for zs in (0.5, 1.0, 1.5, 2.33):
            x0 = xat(f1.x, zs); grid = np.unique(np.r_[np.linspace(0.02, max(x0, 1.0) + 2.5, 30), 1.0]); prof = []  # RUN2: must span X=1 (RUN1 grid bug); prof = []
            for v in grid:
                pen = lambda om, xn, v=v, zs=zs: 1e6*(np.interp(zs, NODES, np.r_[1.0, xn]) - v)**2
                st = f1.x.copy(); st[1:] = st[1:] + (v - x0); prof.append(fit(which, extra=pen, data=data, start=st).fun - f1.fun)
            prof = np.array(prof)
            def ivl(level):
                ok = grid[prof <= level]; return [float(np.sqrt(max(ok.min(), 0))), float(np.sqrt(ok.max()))] if len(ok) else [None, None]
            band[str(zs)] = dict(sqrtX_best=float(np.sqrt(max(x0, 0))), ci68=ivl(1.0), ci95=ivl(3.84), dchi2_at_X1=float(prof[np.argmin(abs(grid - 1.0))]))
        out["sqrtX_band"] = band
        # dark degeneracy: fixed Omega_m grid
        out["fixed_om"] = {}
        for omf in (0.25, 0.30, 0.35):
            g1 = fit(which, om_fix=omf, data=data); g0 = fit(which, fixX=True, om_fix=omf, data=data) if False else None
            c0 = (bao_chi2(omf, np.ones(5), data)[0] if "bao" in which else 0) + (sn_chi2(omf, np.ones(5)) if "sn" in which else 0)
            out["fixed_om"][str(omf)] = dict(chi2_const=float(c0), chi2_free=float(g1.fun), X_nodes=list(map(float, g1.x)), sqrtX_2p33=float(np.sqrt(max(g1.x[-1], 0))))
    res[tag] = out
    print(f"\n=== {tag}  (MUTATE={MUT or 'none'})\n  X≡1 : chi2 = {f0.fun:.2f}  Om = {f0.x[0]:.4f}\n  free: chi2 = {f1.fun:.2f}  Om = {f1.x[0]:.4f}  X(0.4,0.7,1.0,1.5,2.33) = {np.round(f1.x[1:], 3).tolist()}")
    print(f"  Δχ² = {d:.2f} (5 dof)  p = {p:.3g}  ≈ {s:.2f}σ")
    if "sqrtX_band" in out:
        for zs, b in out["sqrtX_band"].items(): print(f"  a0(z)/a0(0) = √X at z={zs}: best {b['sqrtX_best']:.3f}  68% {np.round(b['ci68'], 3).tolist()}  95% {np.round(b['ci95'], 3).tolist()}  (Δχ² at flat a0: {b['dchi2_at_X1']:.2f})")
        for omf, g in out["fixed_om"].items(): print(f"  fixed Ωm={omf}: χ² const {g['chi2_const']:.2f} free {g['chi2_free']:.2f}  √X(2.33) = {g['sqrtX_2p33']:.3f}")
# ---- T3: AP ratio F = D_M/D_H at the six anisotropic tracers, X≡1 shape, Om free ----
def ap_chi2(om, xn, data_=None):
    I = Igrid(om, xn); c = 0; pulls = []
    for (nm, z, dm, sdm, dh, sdh, r) in (data_ or ANISO):
        F = dm/dh; sF = F*np.sqrt((sdm/dm)**2 + (sdh/dh)**2 - 2*r*sdm*sdh/(dm*dh))
        Fm = np.interp(z, zg, I)*Efun(om, xn, np.array([z]))[0]; pulls.append((F - Fm)/sF); c += pulls[-1]**2
    return c, pulls
r3 = minimize(lambda p: ap_chi2(p[0], np.ones(5), data)[0] if 0.15 <= p[0] <= 0.45 else 1e9, [0.3], method="Nelder-Mead")
c3, pulls = ap_chi2(r3.x[0], np.ones(5), data); from scipy.stats import chi2 as _c2
res["T3_AP"] = dict(om=float(r3.x[0]), chi2=float(c3), dof=5, p=float(_c2.sf(c3, 5)), pulls=dict(zip([a[0] for a in ANISO], map(float, pulls))))
print(f"\n=== T3 AP ratio, X≡1 shape: Ωm = {r3.x[0]:.4f}  χ² = {c3:.2f}/5  p = {_c2.sf(c3, 5):.3g}  pulls " + ", ".join(f"{a[0]} {p_:+.2f}" for a, p_ in zip(ANISO, pulls)))
# ---- T4: distance duality, kernel-weighted SN at each anisotropic tracer z <= 1.5 ----
bf = fit(["bao", "sn"], data=data); omb, xb = bf.x[0], bf.x[1:]; Ib = Igrid(omb, xb)
def mu_shape(z, zh): return 5*np.log10((1 + zh)*np.interp(z, zg, Ib))
rows, A = [], []
for (nm, z, dm, sdm, dh, sdh, r) in (data or ANISO):
    if z > 1.5: continue
    w = np.exp(-0.5*((zhd - z)/0.03)**2); k = w > np.exp(-0.5*9)
    if k.sum() < 5: continue
    shift = mu_shape(np.full(k.sum(), z), np.full(k.sum(), z)) - mu_shape(zhd[k], zhel[k])   # move each SN to z (best-fit shape; small)
    Ci = np.linalg.inv(Csn[np.ix_(k, k)]); a = Ci@w[k]; a = a/a.sum()
    vec = np.zeros(len(mb)); vec[k] = a; A.append(vec)
    rows.append((nm, z, float(a@(mb[k] + shift)), dm, sdm, int(k.sum())))
A = np.array(A); Cbin = A@Csn@A.T
mubar = np.array([r_[2] for r_ in rows]); zz = np.array([r_[1] for r_ in rows]); DM_ = np.array([r_[3] for r_ in rows]); sDM = np.array([r_[4] for r_ in rows])
y = mubar - 5*np.log10((1 + zz)*DM_); Cy = Cbin + np.diag((5/np.log(10)*sDM/DM_)**2)
M = np.c_[np.ones_like(zz), 5*np.log10(1 + zz)]; Ciy = np.linalg.inv(Cy); F = M.T@Ciy@M; pr = np.linalg.solve(F, M.T@Ciy@y); er = np.sqrt(np.diag(np.linalg.inv(F)))
chi4 = float((y - M@pr)@Ciy@(y - M@pr))
res["T4_duality"] = dict(tracers=[(r_[0], r_[1], r_[5]) for r_ in rows], eps=float(pr[1]), sig_eps=float(er[1]), chi2=chi4, dof=len(y) - 2)
print(f"\n=== T4 distance duality (η ∝ (1+z)^ε), tracers {[(r_[0], r_[5]) for r_ in rows]}\n  ε = {pr[1]:+.4f} ± {er[1]:.4f}  ({pr[1]/er[1]:+.2f}σ)  χ² = {chi4:.2f}/{len(y)-2}")
# ---- verdicts ----
def v12(s): return "EVOLVING DE REQUIRED" if s >= 3 else ("CONSISTENT WITH CONSTANT" if s < 2 else "HINT")
res["verdict"] = dict(T1=v12(res["T1_BAO"]["sigma_equiv"]), T2=v12(res["T2_BAO+SN"]["sigma_equiv"]),
                      T3="X≡1 SHAPE EXCLUDED" if res["T3_AP"]["p"] < 0.003 else "X≡1 SHAPE ALLOWED",
                      T4="DUALITY VIOLATED" if abs(pr[1]/er[1]) >= 3 else ("CONSERVED" if abs(pr[1]/er[1]) < 2 else "HINT"))
print("\nVERDICTS:", res["verdict"])
json.dump(res, open(os.path.join(HERE, "cfg681_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json"), "w"), indent=1, default=float)
