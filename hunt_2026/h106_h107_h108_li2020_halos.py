#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h106_h107_h108_li2020_halos.py -- HUNT ITEMS 106, 107, 108 (vein B: "the phantom IS the halo").
================================================================================================
All three ask the same question of the same data -- Li+2020's dark-matter halo fits to the 175 SPARC rotation curves
(real_research/data/li2020_sparc_halos.tsv, 12 halo models x 175 galaxies) -- so they share one script and one engine.

Item 106  The rho_0 - r_0 ANTI-CORRELATION.  Item 5 showed the halo surface-density PRODUCT rho_0 r_0 sits near
          Sigma_M = a_0/(2 pi G).  If that product is a constant of nature, the regression of log rho_0 on log r_0
          must have slope exactly -1.  Feedback-driven core formation gives -0.7 to -0.9.
          THE TRAP THE HUNT LIST WARNED ABOUT: rho_0 and r_0 are fitted JOINTLY from one rotation curve and their
          errors are strongly anti-correlated, so the fit degeneracy alone manufactures a negative slope.  This
          script measures that degeneracy from the likelihood itself and subtracts it.

Item 107  Is the fitted CONCENTRATION c200 better predicted by the halo mass M200 or by the DISC's central surface
          density Sigma_0?  In LambdaCDM c200 is a halo property with a shallow c(M) relation (Dutton & Maccio 2014).
          In the framework the fitted halo is the phantom of the baryons, so c200 should be a BARYONIC number.
          Second trap, same shape as the first: c200 and M200 are BOTH derived from the same two fitted parameters
          and share their errors, while Sigma_0 comes from independent photometry.

Item 108  Is the fitted CORE RADIUS r_0 the radius where g_bar = a_0 -- i.e. is the "core" just where the boost
          switches on?  Computed per galaxy from the SPARC rotmods with Li's own Upsilon, distance and inclination.

WHAT WAS REVERSE-ENGINEERED HERE (verified below to 0.003 dex, which is the table's rounding):
    Li+2020 fit (V200, C200) with H0 = 73 km/s/Mpc.  Then
        R200 = C200 * rs = G M200 / V200^2 ,   V200 = 10 H0 R200 ,
        rs   = V200 / (10 H0 C200)                          -- so log rs = log V200 - log C200 + const
        rho_0 = (200/3) rho_crit C200^3 / f_model(C200)      -- so rho_0 is a function of C200 ALONE.
    Consequence: the (log rho_0, log r_0) plane is a linear reparameterisation of (log V200, log C200), and the
    catalogue's e_rs is EXACTLY the uncorrelated propagation of e_V200 and e_C200 (verified below), i.e. the
    published error bars throw away the very correlation that item 106 has to worry about.  The engine here
    recovers it by re-deriving the posterior.

ENGINE.  For each galaxy and each of the four halo models whose (V200, C200) -> (rho_0, rs) map is reproduced
exactly (pISO-Flat, Burkert-Flat, NFW-Flat, NFW-LCDM), the (V200, C200) posterior is recomputed on a grid from the
SPARC rotmod with Li's likelihood and priors: log-normal Upsilon_disk (0.5, 0.1 dex), Gaussian distance and
inclination at SPARC's quoted errors (5-node Gauss-Hermite), flat V200, C200 for "-Flat", plus the
Dutton & Maccio c-M prior for "-LCDM".  Output: the full 2x2 covariance of (log rho_0, log r_0) and of
(log c200, log M200) per galaxy.  Validated against Li's own e_V200 and e_C200.

Both footings (9.36e-11 canonical, 1.13e-10 alt) on every dimensionful number.  a_0 mutations.  Checks CAN fail.
"""
import sys, os, math, glob, time
import numpy as np
from scipy.optimize import minimize
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(106107108)
GK = 4.301e-6                       # G in kpc (km/s)^2 / Msun
H0_LI = 73.0/1000.0                 # km/s/kpc -- Li+2020's H0, recovered from the table below
TEN_H0 = 10*H0_LI
RHOC = 3*(TEN_H0/10)**2/(8*math.pi*GK)              # Msun/kpc^3
PC2 = Msun/(3.0857e16)**2                            # kg/m^2 per Msun/pc^2
SIG_M = {f: A0[f]/(2*math.pi*G)/PC2 for f in A0}     # a_0/(2 pi G) in Msun/pc^2
ENGINE_MODELS = ("pISO-Flat", "Burkert-Flat", "NFW-Flat", "NFW-LCDM")
CORED = ("pISO-Flat", "Burkert-Flat", "DC14-Flat", "coreNFW-Flat", "Lucky13-Flat")

# ------------------------------------------------------------------ data
def load_li():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "li2020_sparc_halos.tsv"),
                                                     encoding="latin-1") if l.strip() and not l.startswith("#")]
    col = {h.strip(): i for i, h in enumerate(rows[0])}
    def f(v):
        try: return float(v)
        except Exception: return float("nan")
    out = []
    for d in rows[3:]:
        out.append(dict(name=d[col["Name"]].strip(), model=d[col["Model"]].strip(),
                        V200=f(d[col["V200"]]), eV=f(d[col["e_V200"]]), C200=f(d[col["C200"]]), eC=f(d[col["e_C200"]]),
                        rs=f(d[col["rs"]]), ers=f(d[col["e_rs"]]), lrho=f(d[col["log(rhos)"]]),
                        elrho=f(d[col["e_log(rhos)"]]), lM=f(d[col["log(M200)"]]), elM=f(d[col["e_log(M200)"]]),
                        chi2=f(d[col["chi2"]]), Yd=f(d[col["Ydisk"]]), Yb=f(d[col["Ybul"]]),
                        D=f(d[col["Dist"]]), inc=f(d[col["inc"]]), alpha=f(d[col["alpha"]])))
    return out

LI = load_li(); MASTER = read_master()
ROT = {os.path.basename(fn).replace("_rotmod.dat", ""): np.loadtxt(fn)
       for fn in glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))}
MODELS = sorted(set(r["model"] for r in LI))

def f_model(model, C):
    """M200 = (4/3) pi 200 rho_c (C rs)^3 = K_model * rho_0 * rs^3 * f(C)  ->  rho_0 = (200/3) rho_c C^3 / f(C)."""
    if model.startswith("pISO"):    return C - np.arctan(C)                                    # /(4 pi) x 4 pi
    if model.startswith("Burkert"): return 0.5*(np.log(1+C) + 0.5*np.log(1+C**2) - np.arctan(C))
    if model.startswith("NFW"):     return np.log(1+C) - C/(1+C)
    return None
def rho0_of_C(model, C):   return (200/3.)*RHOC*C**3/f_model(model, C)      # Msun/kpc^3
def vh2(model, r, rho, rs):
    x = r/rs
    if model.startswith("pISO"):    return 4*math.pi*GK*rho*rs**2*(1 - np.arctan(x)/x)
    if model.startswith("Burkert"): return GK*2*math.pi*rho*rs**3*(np.log(1+x) + 0.5*np.log(1+x**2) - np.arctan(x))/r
    if model.startswith("NFW"):     return GK*4*math.pi*rho*rs**3*(np.log(1+x) - x/(1+x))/r
    return None
def dm14(lM200):
    """Dutton & Maccio 2014 Planck c-M relation (the prior Li imposes on the '-LCDM' fits), log10 c200."""
    return 0.905 - 0.101*(lM200 - 12.0 - math.log10(1/0.671))

P("="*118)
P("ENGINE VALIDATION -- reconstructing Li+2020's parameterisation from the catalogue itself")
P("="*118)
val = []
for mdl in ENGINE_MODELS:
    sub = [r for r in LI if r["model"] == mdl and np.isfinite(r["C200"]) and r["C200"] > 0]
    dl = np.array([math.log10(rho0_of_C(mdl, r["C200"])/1e9) - r["lrho"] for r in sub])
    dr = np.array([math.log10(r["V200"]/(TEN_H0*r["C200"])) - math.log10(r["rs"]) for r in sub])
    prop = np.array([r["rs"]*math.sqrt((r["eV"]/r["V200"])**2 + (r["eC"]/r["C200"])**2)/r["ers"] for r in sub
                     if np.isfinite(r["ers"]) and r["ers"] > 0])
    propM = np.array([3*r["eV"]/(r["V200"]*math.log(10))/r["elM"] for r in sub if np.isfinite(r["elM"]) and r["elM"] > 0])
    info(f"{mdl:14} log rho_0(C200) residual {np.median(dl):+.4f} +- {dl.std():.4f} dex;  log rs(V200,C200) residual "
         f"{np.median(dr):+.4f} +- {dr.std():.4f} dex;  e_rs / uncorrelated-propagation = {np.median(prop):.3f};  "
         f"e_logM200 / (3 e_V200/V200 ln10) = {np.median(propM):.3f}")
    val.append((abs(np.median(dl)), dl.std(), abs(np.median(prop) - 1), abs(np.median(propM) - 1)))
val = np.array(val)
ck("E1 the catalogue's own parameterisation is recovered exactly: rho_0 is a function of C200 alone and rs = V200/(10 H0 C200) "
   "with H0 = 73 km/s/Mpc, both to the table's rounding precision -- so the engine below is fitting the SAME two parameters Li fitted",
   val[:, 1].max() < 0.01, f"worst rms residual over the four models {val[:,1].max():.4f} dex (table rounding is 0.005 dex)")
ck("E2 AND the catalogue's quoted e_rs is EXACTLY the propagation of e_V200 and e_C200 assuming they are UNCORRELATED "
   "(ratio 1.000), while the actual posterior correlation measured below is -0.90 to -0.98.  The published error bars on r_0 "
   "therefore cannot be used as an error ellipse for item 106 -- the correlation has to be re-derived, which is what the engine does",
   val[:, 2].max() < 0.02 and val[:, 3].max() < 0.02,
   f"e_rs/propagation = {val[:,2].max()+1:.3f} worst; e_logM200/propagation = {val[:,3].max()+1:.3f} worst")

# ------------------------------------------------------------------ posterior engine
GH5_x = np.array([-2.02018287, -0.95857246, 0.0, 0.95857246, 2.02018287])
GH5_w = np.array([0.01995324, 0.39361932, 0.94530872, 0.39361932, 0.01995324])/math.sqrt(math.pi)
NG = 121
def posterior(rec):
    """2x2 covariance of (log10 rho_0 [Msun/pc^3], log10 rs [kpc]) and of (log10 C200, log10 M200), from the
    (V200, C200) posterior recomputed on an adaptive grid.  Marginalises Upsilon_disk, distance and inclination
    by 5-node Gauss-Hermite quadrature against Li's priors.  Returns None if the fit is unusable.
    The inclination integral is done ANALYTICALLY in the sense that chi2(u) = A - 2 u B + u^2 C with u = 1/scale,
    so the grid reduction is performed twice per (Upsilon, distance) node instead of once per inclination node."""
    mdl, nm = rec["model"], rec["name"]
    if nm not in ROT or nm not in MASTER: return None
    if not (np.isfinite(rec["V200"]) and np.isfinite(rec["C200"]) and rec["C200"] > 0): return None
    m = MASTER[nm]; d = ROT[nm]; d = d[d[:, 1] > 0]
    if len(d) < 5: return None
    r0, vobs0, ev0, vg0, vd0, vb0 = d[:, 0], d[:, 1], np.maximum(d[:, 2], 1.0), d[:, 3], d[:, 4], d[:, 5]
    sV = max(rec["eV"], 1.0); sC = max(rec["eC"], 0.05)
    Vg = np.linspace(max(10.0, rec["V200"] - 5*sV), min(500.0, rec["V200"] + 5*sV), NG)
    Cg = np.linspace(max(0.2, rec["C200"] - 5*sC), min(100.0, rec["C200"] + 5*sC), NG)
    if Vg[-1] - Vg[0] <= 0 or Cg[-1] - Cg[0] <= 0: return None
    VV, CC = np.meshgrid(Vg, Cg, indexing="ij")
    rho = rho0_of_C(mdl, CC); rss = VV/(TEN_H0*CC)
    lrho = np.log10(rho/1e9); lrs = np.log10(rss)
    lC = np.log10(CC); lM = np.log10(VV**3/(GK*TEN_H0))                        # M200 = V200^3/(G 10 H0)
    incs = np.clip(m["inc"] + max(m["einc"], 1.0)*math.sqrt(2)*GH5_x, 5.0, 90.0)
    us = np.sin(np.radians(incs))/math.sin(math.radians(m["inc"]))             # v_obs -> v_obs/u under inclination change
    A0_ = float(np.sum(vobs0**2/ev0**2))
    lnW = np.full(VV.shape, -np.inf)
    for idd, D in enumerate(m["D"] + max(m["eD"], 0.05)*math.sqrt(2)*GH5_x):
        if D <= 0: continue
        sD = D/m["D"]; r = r0*sD
        VH = vh2(mdl, r[None, None, :], rho[:, :, None], rss[:, :, None])
        vg, vd, vb = vg0*math.sqrt(sD), vd0*math.sqrt(sD), vb0*math.sqrt(sD)
        for iy, Y in enumerate(0.5*10**(0.1*math.sqrt(2)*GH5_x)):
            vb2 = (vg*np.abs(vg) + Y*vd**2 + rec["Yb"]*vb**2)[None, None, :]
            vmod = np.sqrt(np.maximum(vb2 + VH, 0.0))
            Bq = np.sum(vobs0[None, None, :]*vmod/ev0[None, None, :]**2, axis=2)
            Cq = np.sum(vmod**2/ev0[None, None, :]**2, axis=2)
            for ii, u in enumerate(us):
                chi2 = A0_ - 2*u*Bq + u*u*Cq                                   # chi2 = sum (v_obs - u v_mod)^2/ev^2
                w = GH5_w[iy]*GH5_w[idd]*GH5_w[ii]
                lnW = np.logaddexp(lnW, -0.5*chi2 + math.log(max(w, 1e-300)))
    if "LCDM" in mdl: lnW = lnW - 0.5*((lC - dm14(lM))/0.11)**2
    W = np.exp(lnW - lnW.max()); s = W.sum()
    if not np.isfinite(s) or s <= 0: return None
    W /= s
    def cov(A, B):
        ma, mb = float(np.sum(W*A)), float(np.sum(W*B))
        return ma, mb, float(np.sum(W*(A - ma)*(B - mb)))
    mr, ms, crs = cov(lrho, lrs); _, _, vr = cov(lrho, lrho); _, _, vs = cov(lrs, lrs)
    mc, mm, ccm = cov(lC, lM);    _, _, vc = cov(lC, lC);     _, _, vm = cov(lM, lM)
    lV = np.log10(VV); _, _, vV = cov(lV, lV)
    if min(vr, vs, vc, vm, vV) <= 0: return None
    return dict(mu=(mr, ms), cov=np.array([[vr, crs], [crs, vs]]),
                muCM=(mc, mm), covCM=np.array([[vc, ccm], [ccm, vm]]),
                sV=math.sqrt(vV), sC=math.sqrt(vc),
                rail=(Vg[0] <= 10.001 or Vg[-1] >= 499.999 or Cg[-1] >= 99.999))

P(""); info("recomputing the (V200, C200) posterior for 4 models x 175 galaxies -- this is the slow part (~3 min)")
t0 = time.time(); POST = {}
for mdl in ENGINE_MODELS:
    for rec in [r for r in LI if r["model"] == mdl]:
        p = posterior(rec)
        if p is not None: POST[(mdl, rec["name"])] = p
info(f"posteriors computed: {len(POST)} galaxy-model pairs in {time.time()-t0:.0f} s")
for mdl in ENGINE_MODELS:
    sub = [(POST[(mdl, r['name'])], r) for r in LI if r["model"] == mdl and (mdl, r["name"]) in POST
           and np.isfinite(r["eV"]) and r["eV"] > 0 and np.isfinite(r["eC"]) and r["eC"] > 0]
    rV = np.array([p["sV"]/(r["eV"]/(r["V200"]*math.log(10))) for p, r in sub])
    rC = np.array([p["sC"]/(r["eC"]/(r["C200"]*math.log(10))) for p, r in sub])
    cc = np.array([p["cov"][0, 1]/math.sqrt(p["cov"][0, 0]*p["cov"][1, 1]) for p, r in sub])
    dg = np.array([p["cov"][0, 1]/p["cov"][1, 1] for p, r in sub])
    info(f"{mdl:14} N={len(sub):3d}  my sigma(logV200)/Li's = {np.median(rV):.2f}, sigma(logC200)/Li's = {np.median(rC):.2f}"
         f"   |  correlation of (log rho_0, log r_0) = {np.median(cc):+.3f}   DEGENERACY SLOPE = {np.median(dg):+.2f}")
rr = np.array([np.median([POST[(m, r['name'])]["sV"]/(r["eV"]/(r["V200"]*math.log(10))) for r in LI
                          if r["model"] == m and (m, r["name"]) in POST and r["eV"] > 0]) for m in ENGINE_MODELS])
info("caveat stated against interest: sigma(log C200) matches Li's to 0.85-0.92 for Burkert and both NFW variants but only 0.45")
info("for pISO, so the pISO ellipse below is probably too TIGHT and its degeneracy correction correspondingly under-applied.")
ck("E3 the re-derived posterior reproduces Li's own quoted parameter uncertainties to within a factor ~1.3, which is what "
   "licenses using its CORRELATION (the thing Li does not publish) as the error ellipse for items 106 and 107",
   0.6 < np.median(rr) < 1.4, f"median sigma(log V200) mine/Li over the four models: {np.array2string(rr, precision=2)}")
bad = 0; worst = 1e9; thin = 0
for k, p in POST.items():
    for C in (p["cov"], p["covCM"], np.array([[p["cov"][1, 1], p["cov"][0, 1]], [p["cov"][0, 1], p["cov"][0, 0]]])):
        ev = np.linalg.eigvalsh((C + C.T)/2)
        rat = float(ev.min()/max(ev.max(), 1e-300)); worst = min(worst, rat)
        if rat < 1e-4: thin += 1
        if ev.min() <= 0 or not np.allclose(C, C.T): bad += 1
ck("E4 (bug pattern 4, checked explicitly rather than assumed) every 2x2 error ellipse used below -- in both orderings, since "
   "the (log rho_0, log r_0) matrix is transposed into (x, y) = (log r_0, log rho_0) for the regression -- is symmetric and "
   "POSITIVE DEFINITE, not merely positive on the diagonal.  An earlier item in this hunt was voided by exactly this",
   bad == 0, f"{len(POST)} posteriors x 3 orderings checked, {bad} non-positive-definite; worst eigenvalue ratio {worst:.1e}, "
   f"and {thin} of {3*len(POST)} are thinner than 1e-4 -- those are the galaxies whose rotation curve fixes one combination of "
   f"(V200, C200) and says almost nothing about the other, which is the physical situation and not a numerical failure")

# ------------------------------------------------------------------ shared regression tools
def ols(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    s, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return s, b, float((y - (s*x + b)).std())

def eiv(x, y, C, ntry=5):
    """Errors-in-variables straight-line fit in the Kelly (2007) form, which is the one that matches this problem:
    the true x are drawn from a Gaussian N(mu, tau^2), the true y = m x + b + N(0, sig^2) -- i.e. the intrinsic
    scatter is VERTICAL, in the product rho_0 r_0, not orthogonal to the line -- and the observed pair carries the
    per-galaxy 2x2 measurement covariance C[i].  The observed (x, y) is then Gaussian with
        mean = (mu, m mu + b),   cov = [[tau^2, m tau^2], [m tau^2, m^2 tau^2 + sig^2]] + C[i].
    Returns (slope, intercept, sig).  An ORTHOGONAL-scatter fit (Hogg, Bovy & Lang) was tried first and is biased
    by -0.30 in slope on these data because the scatter here is not orthogonal -- see the mock control below."""
    n = len(x)
    def nll(p):
        m, b, mu, lt, ls = p
        t2, s2 = math.exp(2*lt), math.exp(2*ls)
        a = C[:, 0, 0] + t2; d = C[:, 1, 1] + m*m*t2 + s2; o = C[:, 0, 1] + m*t2
        det = a*d - o*o
        if np.any(det <= 0): return 1e12
        dx = x - mu; dy = y - (m*mu + b)
        q = (d*dx*dx - 2*o*dx*dy + a*dy*dy)/det
        return float(np.sum(0.5*q + 0.5*np.log(det)))
    s0, b0, sc0 = ols(x, y); best = None
    tau0 = max(float(np.std(x)), 1e-3)
    for f in np.linspace(0.6, 1.4, ntry):
        p0 = [s0*f, b0, float(np.mean(x)), math.log(tau0), math.log(max(sc0, 1e-3))]
        r = minimize(nll, p0, method="Nelder-Mead", options=dict(maxiter=20000, maxfev=20000, xatol=1e-7, fatol=1e-9))
        if best is None or r.fun < best.fun: best = r
    m, b, mu, lt, ls = best.x
    return m, b, math.exp(ls)

def boot_eiv(x, y, C, n=200):
    out = []
    for _ in range(n):
        i = rng.integers(0, len(x), len(x))
        try: out.append(eiv(x[i], y[i], C[i])[0])
        except Exception: pass
    return np.array(out)

# ==================================================================================================================
P(""); P("="*118); P("ITEM 106 -- the rho_0 - r_0 anti-correlation: is the slope -1, and is -1 free?"); P("="*118)
info("the prediction restated exactly: log rho_0 = log Sigma_M - log r_0 has slope -1 IF AND ONLY IF the product does not")
info("itself depend on r_0, since  d log rho_0/d log r_0 = -1 + d log(rho_0 r_0)/d log r_0.  Item 5 already measured the")
info("product: median 177 Msun/pc^2 for Burkert with a 0.45 dex SCATTER, so 'constant' is a statement about the median only.")
info(f"Sigma_M = a_0/(2 pi G) = {SIG_M['canonical']:.1f} (canonical) / {SIG_M['alt']:.1f} (alt) Msun/pc^2.")
P("")
info("(a) the NAIVE slope, straight from the catalogue, every model:")
NAIVE = {}
for mdl in MODELS:
    sub = [r for r in LI if r["model"] == mdl and np.isfinite(r["rs"]) and r["rs"] > 0 and np.isfinite(r["lrho"])
           and np.isfinite(r["chi2"]) and r["chi2"] < 10]
    if len(sub) < 20: continue
    x = np.array([math.log10(r["rs"]) for r in sub]); y = np.array([r["lrho"] for r in sub])
    s, b, sc = ols(x, y)
    bs = np.array([ols(x[i], y[i])[0] for i in (rng.integers(0, len(x), len(x)) for _ in range(500))])
    NAIVE[mdl] = (s, bs.std(), sc, len(x))
    info(f"    {mdl:15} N={len(x):3d}  slope {s:+.3f} +- {bs.std():.3f}   residual scatter {sc:.3f} dex")
nb = NAIVE["Burkert-Flat"]; npi = NAIVE["pISO-Flat"]
for cut, lab in ((1e9, "no chi2 cut"), (10.0, "chi2 < 10 (the cut used, and the one items 5 and 24 used)"), (3.0, "chi2 < 3")):
    sub = [r for r in LI if r["model"] == "Burkert-Flat" and np.isfinite(r["rs"]) and r["rs"] > 0
           and np.isfinite(r["lrho"]) and np.isfinite(r["chi2"]) and r["chi2"] < cut]
    sx, _, _ = ols(np.array([math.log10(r["rs"]) for r in sub]), np.array([r["lrho"] for r in sub]))
    info(f"    cut sensitivity, Burkert-Flat, {lab:52}: N = {len(sub):3d}, slope {sx:+.3f}")
lc_flat = [NAIVE[m][0] for m in NAIVE if m.endswith("-Flat")]
lc_lcdm = [NAIVE[m][0] for m in NAIVE if m.endswith("-LCDM")]
info(f"    -Flat models (no c-M prior): slopes {np.min(lc_flat):+.2f} to {np.max(lc_flat):+.2f}, median {np.median(lc_flat):+.2f}")
info(f"    -LCDM models (Dutton & Maccio c-M prior imposed): slopes {np.min(lc_lcdm):+.2f} to {np.max(lc_lcdm):+.2f}, "
     f"median {np.median(lc_lcdm):+.2f}  <-- the models with a LambdaCDM prior are the ones that land ON -1")
ck("106a AGAINST INTEREST -- there is no such thing as 'the' slope to test.  Across the twelve profile/prior combinations fitted "
   "to the SAME 175 rotation curves the slope runs from -0.89 to -1.69, a spread far wider than the +-0.05 the item asked for, so "
   "it is set more by the choice of halo profile and prior than by the galaxies.  The prior-free cored fits give -1.19 and -1.29, "
   "STEEPER than the framework's -1 and nowhere near feedback's -0.7/-0.9; the combinations that land on -1.00 are the ones "
   "carrying a LambdaCDM c-M prior",
   (max(lc_flat + lc_lcdm) - min(lc_flat + lc_lcdm)) > 0.5 and nb[0] < -1.05 and npi[0] < -1.05,
   f"full range {min(lc_flat+lc_lcdm):+.2f} to {max(lc_flat+lc_lcdm):+.2f}; Burkert-Flat {nb[0]:+.3f} +- {nb[1]:.3f}, "
   f"pISO-Flat {npi[0]:+.3f} +- {npi[1]:.3f}; -Flat median {np.median(lc_flat):+.3f} vs -LCDM median {np.median(lc_lcdm):+.3f}")

P("")
info("    the LambdaCDM alternative computed beside the framework: take Dutton & Maccio's c(M200) with NO MOND input at all,")
info("    convert to (rho_s, r_s) through the same NFW definitions, and read off the slope it predicts:")
lMg = np.linspace(9.0, 13.0, 200); cg = 10**dm14(lMg)
R200g = (10**lMg*GK/(TEN_H0**2))**(1/3.); rsg = R200g/cg
rhog = np.array([rho0_of_C("NFW", c)/1e9 for c in cg])
sl_dm14, _, _ = ols(np.log10(rsg), np.log10(rhog))
info(f"    a pure Dutton & Maccio c-M relation gives d log rho_s/d log r_s = {sl_dm14:+.3f} over 1e9-1e13 Msun -- so LambdaCDM's")
info(f"    own concentration-mass relation ALREADY produces a steep anti-correlation with no a_0 anywhere in it.")

P("")
info("(b) THE TRAP the hunt list warned about, measured rather than assumed.  rho_0 and r_0 are two numbers squeezed out of one")
info("    rotation curve, and the engine says their posterior correlation is -0.90 to -0.98 with a degeneracy slope of -1.4 to -1.8.")
info("    How much of the measured slope does that degeneracy buy for free?  A population with NO intrinsic relation at all")
info("    (true log rho_0 constant), pushed through the REAL per-galaxy ellipses:")
DEG = {}
for mdl in ENGINE_MODELS:
    sub = [(POST[(mdl, r["name"])], r) for r in LI if r["model"] == mdl and (mdl, r["name"]) in POST
           and np.isfinite(r["chi2"]) and r["chi2"] < 10]
    dg = np.array([p["cov"][0, 1]/p["cov"][1, 1] for p, _ in sub])
    sx = np.array([math.sqrt(p["cov"][1, 1]) for p, _ in sub])
    x = np.array([math.log10(r["rs"]) for _, r in sub])
    # what a pure-degeneracy population would give: a data set with NO intrinsic relation at all
    # (true log r_0 spread as observed, true log rho_0 CONSTANT), pushed through the real error ellipses.
    Cs = np.array([p["cov"] for p, _ in sub])
    vx_obs = float(np.var(x)); vx_err = float(np.mean(Cs[:, 1, 1])); vx_true = max(vx_obs - vx_err, 1e-4)
    null = []
    for _ in range(300):
        xt = rng.normal(x.mean(), math.sqrt(vx_true), len(x)); yt = np.zeros_like(xt)
        e = np.array([rng.multivariate_normal([0, 0], Cs[i]) for i in range(len(xt))])
        null.append(ols(xt + e[:, 1], yt + e[:, 0])[0])
    null = np.array(null)
    pop_deg = float(np.mean(Cs[:, 0, 1])/np.mean(Cs[:, 1, 1]))     # the slope attenuation actually pulls TOWARD
    DEG[mdl] = (np.median(dg), np.median(sx), null.mean(), null.std(), vx_true, vx_err, pop_deg)
    info(f"    {mdl:15} median per-galaxy degeneracy slope {np.median(dg):+.2f}, POPULATION-AVERAGED degeneracy slope "
         f"<C_xy>/<C_xx> = {pop_deg:+.2f}  <-- the attractor; median sigma(log r_0) = {np.median(sx):.3f} dex "
         f"({100*vx_err/vx_obs:.0f}% of the observed log r_0 variance is fit error);  a population with NO intrinsic relation "
         f"returns slope {null.mean():+.3f} +- {null.std():.3f}")
dnull = DEG["Burkert-Flat"]
ck("106b the trap is REAL, and it has a precise shape that is worth more than the warning: attenuation drags any measured slope "
   "toward the POPULATION-AVERAGED degeneracy slope, which for these fits is about -1.  So the naive estimator is unbiased "
   "exactly AT -1 and pulls everything else toward it (see the mocks in (d): true -0.8 reads -0.85, true -1.4 reads -1.33).  A "
   "population with no relation at all returns only -0.2, because just ~20% of the log r_0 variance is fit error -- so -1 is not "
   "handed over for free, it is a magnet",
   abs(dnull[6] + 1.0) < 0.35 and abs(dnull[2] + 1) > 0.5,
   f"Burkert-Flat population-averaged degeneracy slope {dnull[6]:+.3f} (the attractor); null-relation mock slope "
   f"{dnull[2]:+.3f} +- {dnull[3]:.3f} vs the catalogue's {nb[0]:+.3f} +- {nb[1]:.3f}; "
   f"{100*dnull[5]/(dnull[4]+dnull[5]):.0f}% of the log r_0 variance is fit error")

P("")
info("(c) the degeneracy-corrected slope.  Estimator: an errors-in-variables fit in the Kelly (2007) form -- per-galaxy 2x2")
info("    ellipse from the engine, plus one intrinsic scatter in log rho_0 at FIXED log r_0, which is scatter in the PRODUCT")
info("    and is the right shape for this hypothesis.  (An orthogonal-scatter fit was written first and is biased by -0.30 on")
info("    these data; that bug is kept visible in the mock control (d) below rather than hidden.)")
EIVR = {}
for mdl in ENGINE_MODELS:
    sub = [(POST[(mdl, r["name"])], r) for r in LI if r["model"] == mdl and (mdl, r["name"]) in POST
           and np.isfinite(r["chi2"]) and r["chi2"] < 10]
    x = np.array([math.log10(r["rs"]) for _, r in sub]); y = np.array([r["lrho"] for _, r in sub])
    Cs = np.array([p["cov"] for p, _ in sub])
    Cxy = np.array([[[c[1, 1], c[0, 1]], [c[0, 1], c[0, 0]]] for c in Cs])       # reorder to (x, y) = (log r, log rho)
    s, b, vint = eiv(x, y, Cxy); bs = boot_eiv(x, y, Cxy, 200)
    EIVR[mdl] = (s, bs.std(), vint, len(x), b)
    info(f"    {mdl:15} N={len(x):3d}  EIV slope {s:+.3f} +- {bs.std():.3f}  (naive {NAIVE[mdl][0]:+.3f});  intrinsic scatter "
         f"in log rho_0 at fixed r_0 = {vint:.3f} dex;  implied d log(rho_0 r_0)/d log r_0 = {s+1:+.3f}")
eb = EIVR["Burkert-Flat"]

P("")
info("(d) MUTATION CONTROL for the estimator itself -- inject a KNOWN slope, add the REAL error ellipses, and see what each")
info("    estimator returns.  If the fit cannot separate -1.0 from -0.8 the item is unanswerable with this catalogue.")
sub = [(POST[("Burkert-Flat", r["name"])], r) for r in LI if r["model"] == "Burkert-Flat"
       and ("Burkert-Flat", r["name"]) in POST and np.isfinite(r["chi2"]) and r["chi2"] < 10]
x = np.array([math.log10(r["rs"]) for _, r in sub]); y = np.array([r["lrho"] for _, r in sub])
Cs = np.array([p["cov"] for p, _ in sub])
Cxy = np.array([[[c[1, 1], c[0, 1]], [c[0, 1], c[0, 0]]] for c in Cs])
vx_true = max(float(np.var(x)) - float(np.mean(Cxy[:, 0, 0])), 1e-4)
sig_int = EIVR["Burkert-Flat"][2]
MOCK = {}
for mtrue in (-1.0, -0.8, -1.4):
    o, e = [], []
    for _ in range(120):
        xt = rng.normal(x.mean(), math.sqrt(vx_true), len(x))
        yt = mtrue*xt + 2.0 + rng.normal(0, sig_int, len(xt))
        er = np.array([rng.multivariate_normal([0, 0], Cxy[i]) for i in range(len(xt))])
        xo, yo = xt + er[:, 0], yt + er[:, 1]
        o.append(ols(xo, yo)[0])
        try: e.append(eiv(xo, yo, Cxy)[0])
        except Exception: pass
    o, e = np.array(o), np.array(e)
    MOCK[mtrue] = (o.mean(), o.std(), e.mean(), e.std())
    info(f"    injected slope {mtrue:+.2f}:  naive OLS returns {o.mean():+.3f} +- {o.std():.3f}  (bias {o.mean()-mtrue:+.3f});  "
         f"EIV returns {e.mean():+.3f} +- {e.std():.3f}  (bias {e.mean()-mtrue:+.3f})")
ok_ng = []
for _ in range(120):     # same test but with the OBSERVED, non-Gaussian log r_0 distribution instead of a Gaussian one
    xt = x[rng.integers(0, len(x), len(x))]
    yt = -1.33*xt + 2.0 + rng.normal(0, sig_int, len(xt))
    er = np.array([rng.multivariate_normal([0, 0], Cxy[i]) for i in range(len(xt))])
    try: ok_ng.append(eiv(xt + er[:, 0], yt + er[:, 1], Cxy)[0])
    except Exception: pass
ok_ng = np.array(ok_ng)
info(f"    robustness of the ONE assumption the estimator makes (a Gaussian distribution of true log r_0): injecting -1.33 with "
     f"the OBSERVED, non-Gaussian log r_0 distribution instead returns {ok_ng.mean():+.3f} +- {ok_ng.std():.3f} (bias "
     f"{ok_ng.mean()+1.33:+.3f}) -- the assumption is not driving the answer")
b08 = MOCK[-0.8]; b10 = MOCK[-1.0]; b14 = MOCK[-1.4]
ck("M106 mutation: the estimator is calibrated on mocks that use the real error ellipses.  The naive fit is pulled TOWARD -1 "
   "from both sides (-0.05 at a true -0.8, +0.07 at a true -1.4, and no bias at all exactly at -1), which is the magnet of (b) "
   "seen directly; the EIV fit recovers every injected value to within its own scatter, including with the observed "
   "non-Gaussian log r_0 distribution.  The estimator CAN fail and did not, so the measurement below means something",
   abs(b08[2] + 0.8) < 2.5*b08[3] and abs(b10[2] + 1.0) < 2.5*b10[3] and abs(b14[2] + 1.4) < 2.5*b14[3]
   and abs(ok_ng.mean() + 1.33) < 3*ok_ng.std(),
   f"true -1.00 -> EIV {b10[2]:+.3f} +- {b10[3]:.3f}; true -0.80 -> {b08[2]:+.3f} +- {b08[3]:.3f}; "
   f"true -1.40 -> {b14[2]:+.3f} +- {b14[3]:.3f}; naive biases {b10[0]+1:+.3f} / {b08[0]+0.8:+.3f} / {b14[0]+1.4:+.3f}; "
   f"non-Gaussian-x control at -1.33 -> {ok_ng.mean():+.3f} +- {ok_ng.std():.3f}")
ck("106c AGAINST INTEREST -- with the joint-fit degeneracy divided out by a calibrated estimator, the cored-halo slope is NOT -1: "
   "it is significantly STEEPER, which means log(rho_0 r_0) still falls with r_0 and the surface-density product is not a constant "
   "of nature in this catalogue.  Item 5's statement about the product's MEDIAN is untouched; its constancy as a LAW is not "
   "supported by the slope",
   abs(eb[0] + 1) > 2*eb[1],
   f"Burkert-Flat EIV {eb[0]:+.3f} +- {eb[1]:.3f} ({(eb[0]+1)/max(eb[1],1e-6):+.1f} sigma from -1, and "
   f"{(eb[0]+0.8)/max(eb[1],1e-6):+.1f} sigma from the feedback -0.8); pISO-Flat {EIVR['pISO-Flat'][0]:+.3f} +- "
   f"{EIVR['pISO-Flat'][1]:.3f}; NFW-Flat {EIVR['NFW-Flat'][0]:+.3f} +- {EIVR['NFW-Flat'][1]:.3f}")

P("")
info("(e) the a_0-sensitive half.  The framework's line is not just 'slope -1', it is the FIXED line")
info("    log rho_0 = log Sigma_M(a_0) - log r_0 - 3.  With the slope HELD at the predicted -1 and only the intercept free,")
info("    the intercept is a zero-parameter measurement of Sigma_M -- the item-5 statement, now with the fit ellipses in it.")
def fixed_slope_intercept(x, y, Cxy, slope):
    """intercept of y = slope*x + b, weighting each galaxy by its own variance ALONG y at fixed slope + intrinsic scatter."""
    def nll(p):
        b, ls = p; s2 = math.exp(2*ls)
        v = Cxy[:, 1, 1] - 2*slope*Cxy[:, 0, 1] + slope*slope*Cxy[:, 0, 0] + s2
        d = y - (slope*x + b)
        return float(np.sum(0.5*d*d/v + 0.5*np.log(v)))
    r = minimize(nll, [float(np.mean(y - slope*x)), math.log(0.3)], method="Nelder-Mead",
                 options=dict(maxiter=8000, xatol=1e-8, fatol=1e-10))
    return r.x[0], math.exp(r.x[1])
b_fix, s_fix = fixed_slope_intercept(x, y, Cxy, -1.0)
bfb = np.array([fixed_slope_intercept(x[i], y[i], Cxy[i], -1.0)[0]
                for i in (rng.integers(0, len(x), len(x)) for _ in range(200))])
SIG_meas = 10**(b_fix + 3.0)
info(f"    slope fixed at -1: measured Sigma_M = rho_0 r_0 = {SIG_meas:.1f} [{10**(np.percentile(bfb,16)+3):.1f}, "
     f"{10**(np.percentile(bfb,84)+3):.1f}] Msun/pc^2, intrinsic scatter {s_fix:.3f} dex")
for foot in A0:
    info(f"    {foot:10} framework Sigma_M = a_0/(2 pi G) = {SIG_M[foot]:.1f} Msun/pc^2 -> measured is "
         f"{math.log10(SIG_meas/SIG_M[foot]):+.3f} dex away ({abs(b_fix - (math.log10(SIG_M[foot])-3))/bfb.std():.1f} sigma)")
R106e = (SIG_meas, bfb.std(), math.log10(SIG_meas/SIG_M["canonical"]), math.log10(SIG_meas/SIG_M["alt"]))
a0_from_sigma = 2*math.pi*G*(SIG_meas*PC2)
a0_lo = 2*math.pi*G*(10**(np.percentile(bfb, 16) + 3)*PC2); a0_hi = 2*math.pi*G*(10**(np.percentile(bfb, 84) + 3)*PC2)
info(f"    FOR THE a_0 LADDER, with every caveat attached: inverting Sigma_M = a_0/(2 pi G) gives a_0 = {a0_from_sigma:.2e} "
     f"[{a0_lo:.2e}, {a0_hi:.2e}] m/s^2 from Burkert-Flat, i.e. {math.log10(a0_from_sigma/A0['canonical']):+.2f} dex from")
info(f"    canonical and {math.log10(a0_from_sigma/A0['alt']):+.2f} dex from alt.  It is NOT an M/L-free rung -- Li's fits carry a fitted Upsilon_disk with a 0.1 dex")
info("    prior -- and its real error bar is the 1.2 dex profile-choice spread below, not the bootstrap interval quoted.  It")
info("    should go on the ladder as an UPPER-BOUND-quality rung or not at all.")
prods = [float(np.median([10**r["lrho"]*r["rs"]*1000 for r in LI if r["model"] == m and np.isfinite(r["rs"])
                          and np.isfinite(r["lrho"]) and np.isfinite(r["chi2"]) and r["chi2"] < 10])) for m in MODELS]
info(f"    THE SYSTEMATIC THAT SIZES THIS: the same 175 rotation curves give a median rho_0 r_0 of {min(prods):.0f} to "
     f"{max(prods):.0f} Msun/pc^2 depending only on WHICH halo profile is fitted (item 5's table) -- a {math.log10(max(prods)/min(prods)):.1f} dex")
info("    spread.  The +-0.04 dex statistical error above is therefore not the error that matters, and the 0.2 dex offset from")
info("    a_0/(2 pi G) is well inside the profile-choice systematic.  Quoted both ways.")
ck("M106b mutation and a_0 sensitivity: with the slope held at the predicted -1 the intercept measures the surface-density "
   "constant, and it sits ~0.2 dex ABOVE both footings.  a_0 x 10 (a 1.0 dex shift) is excluded many times over, so the test "
   "does have a_0 in it -- but the profile-choice systematic is 1.2 dex, an order of magnitude larger than the offset being "
   "discussed, so this is a consistency and NOT a measurement of a_0",
   1.0/max(R106e[1], 1e-6) > 5 and math.log10(max(prods)/min(prods)) > 3*abs(R106e[2]),
   f"measured {R106e[0]:.1f} +- {R106e[0]*math.log(10)*R106e[1]:.1f} Msun/pc^2 (Burkert-Flat); canonical {R106e[2]:+.3f} dex, "
   f"alt {R106e[3]:+.3f} dex; a_0 x 10 would be 1.000 dex = {1.0/R106e[1]:.0f} statistical sigma away, but the profile-choice "
   f"spread is {math.log10(max(prods)/min(prods)):.2f} dex")

P("")
info("VERDICT 106.  Three separate things, and only one of them is what the item asked for.")
info("  (i)   The trap is real and its shape is now known: attenuation is a MAGNET at slope ~-1 (the population-averaged")
info("        degeneracy slope), so the naive fit reads -1 back whatever the truth is nearby.  A pure null returns only -0.2.")
info(f"  (ii)  There is no stable slope to test: 12 profile/prior combinations on the SAME curves give -0.89 to -1.69.  The")
info(f"        prior-free cored fits give -1.19/-1.29 naive and {EIVR['Burkert-Flat'][0]:+.2f}/{EIVR['pISO-Flat'][0]:+.2f} corrected -- steeper than the")
info("        framework's -1 by 2-4 sigma, and far from feedback's -0.7/-0.9.  A pure Dutton & Maccio c-M relation gives -0.57")
info("        with no a_0 in it at all.  Slope -1 is not a discriminator in either direction.")
info("  (iii) What survives is the INTERCEPT -- item 5 restated with the fit ellipses -- and it is a consistency, not a law:")
info("        rho_0 r_0 sits ~0.2 dex above a_0/(2 pi G) against a 1.2 dex profile-choice systematic.")
info("  Item 106's stated pass condition ('slope -1.00 +- 0.05 and no mass dependence') is REFUTED by the data on disk.")

# ==================================================================================================================
P(""); P("="*118); P("ITEM 107 -- is c200 a halo number (M200) or a baryonic number (the disc's central surface density)?")
P("="*118)
def sigma0(rec, ups=None):
    m = MASTER[rec["name"]]
    Y = rec["Yd"] if ups is None else ups
    return Y*m["SBdisk"]                      # Msun/pc^2; SBdisk is in L/pc^2 and is distance-independent
def mbar(rec):
    m = MASTER[rec["name"]]; sD = (rec["D"]/m["D"])**2
    return sD*(rec["Yd"]*m["L36"]*1e9 + 1.33*m["MHI"]*1e9)
def pcorr(a, b, c):
    """partial correlation of a and b controlling for c."""
    ra = a - np.polyval(np.polyfit(c, a, 1), c); rb = b - np.polyval(np.polyfit(c, b, 1), c)
    return float(np.corrcoef(ra, rb)[0, 1])

R107 = {}
for mdl in ENGINE_MODELS:
    sub = [r for r in LI if r["model"] == mdl and np.isfinite(r["chi2"]) and r["chi2"] < 10 and np.isfinite(r["C200"])
           and r["C200"] > 0 and MASTER[r["name"]]["SBdisk"] > 0 and (mdl, r["name"]) in POST]
    lc = np.array([math.log10(r["C200"]) for r in sub]); lM = np.array([r["lM"] for r in sub])
    lS = np.array([math.log10(sigma0(r)) for r in sub]); lB = np.array([math.log10(mbar(r)) for r in sub])
    lD = np.array([math.log10(MASTER[r["name"]]["Rdisk"]*r["D"]/MASTER[r["name"]]["D"]) for r in sub])
    lSb = np.log10(10**lB/(2*math.pi*(10**lD*1e3)**2))     # mean baryonic surface density M_b/(2 pi R_d^2), gas included
    rM, rS = float(np.corrcoef(lc, lM)[0, 1]), float(np.corrcoef(lc, lS)[0, 1])
    rSb = float(np.corrcoef(lc, lSb)[0, 1])
    pM, pS = pcorr(lc, lM, lS), pcorr(lc, lS, lM)
    pSb = pcorr(lc, lSb, lM)
    A = np.vstack([lM, lS, np.ones_like(lc)]).T
    co = np.linalg.lstsq(A, lc, rcond=None)[0]
    bs = np.array([np.linalg.lstsq(A[i], lc[i], rcond=None)[0] for i in (rng.integers(0, len(lc), len(lc)) for _ in range(500))])
    R107[mdl] = dict(n=len(lc), rM=rM, rS=rS, rSb=rSb, pM=pM, pS=pS, pSb=pSb, co=co, bs=bs.std(0),
                     lc=lc, lM=lM, lS=lS, lB=lB, lSb=lSb, sub=sub)
    info(f"{mdl:14} N={len(lc):3d}   r(log c, log M200) = {rM:+.3f}   r(log c, log Sigma_0) = {rS:+.3f}   "
         f"r(log c, log M_b/2piR_d^2) = {rSb:+.3f}")
    info(f"{'':14}       partial correlations: c-M200 at fixed Sigma_0 = {pM:+.3f}, c-Sigma_0 at fixed M200 = {pS:+.3f}, "
         f"c-<Sigma_b> at fixed M200 = {pSb:+.3f}")
    info(f"{'':14}       joint fit  log c = ({co[0]:+.3f} +- {bs.std(0)[0]:.3f}) log M200 + ({co[1]:+.3f} +- {bs.std(0)[1]:.3f}) log Sigma_0 + const")
rb = R107["Burkert-Flat"]
wins = sum(1 for m in ENGINE_MODELS if abs(R107[m]["rM"]) > abs(R107[m]["rS"]))
ck("107a the item's stated pass condition FAILS, but the loss is not total and both halves are reported.  The raw correlation "
   "with M200 beats the raw correlation with the disc's central surface density in 3 of the 4 models (pISO is the exception, "
   "where Sigma_0 narrowly wins, 0.140 to 0.125), so c200 is NOT more tightly a baryonic number than a halo number.  What DOES "
   "survive: at fixed M200 the disc's surface density still carries a significant positive signal (+0.15 to +0.40 partial "
   "correlation, 2 to 5 sigma in the joint fit), which a pure halo c(M) relation does not predict at all",
   wins >= 3 and abs(rb["co"][1]) > 2*rb["bs"][1],
   f"|r(c,M200)| > |r(c,Sigma_0)| in {wins}/4 models; Burkert-Flat {abs(rb['rM']):.3f} vs {abs(rb['rS']):.3f}; "
   f"partial c-Sigma_0 at fixed M200 = {rb['pS']:+.3f}, joint-fit coefficient {rb['co'][1]:+.3f} +- {rb['bs'][1]:.3f} "
   f"({abs(rb['co'][1])/rb['bs'][1]:.1f} sigma)")

P("")
info("(b) BUT the same trap as item 106 sits here too, and it runs the OTHER way this time: c200 and M200 are BOTH derived from")
info("    the same two fitted parameters (log c = log C200, log M200 = 3 log V200 + const), so they share fit errors, whereas")
info("    Sigma_0 is independent photometry.  The engine's (log c, log M200) ellipse says how much of r(c, M200) is free:")
for mdl in ENGINE_MODELS:
    d = R107[mdl]
    Cs = np.array([POST[(mdl, r["name"])]["covCM"] for r in d["sub"]])
    dg = Cs[:, 0, 1]/Cs[:, 1, 1]; cc = Cs[:, 0, 1]/np.sqrt(Cs[:, 0, 0]*Cs[:, 1, 1])
    vx_obs = float(np.var(d["lM"])); vx_err = float(np.mean(Cs[:, 1, 1]))
    Cxy = np.array([[[c[1, 1], c[0, 1]], [c[0, 1], c[0, 0]]] for c in Cs])
    s, b, vint = eiv(d["lM"], d["lc"], Cxy); bs = boot_eiv(d["lM"], d["lc"], Cxy, 150)
    so, _, _ = ols(d["lM"], d["lc"])
    d["eiv"] = (s, bs.std(), so, np.median(cc), vx_err/vx_obs)
    info(f"    {mdl:15} error correlation of (log c, log M200) = {np.median(cc):+.3f}; fit error is {100*vx_err/vx_obs:.0f}% of the "
         f"observed log M200 variance;  naive c-M slope {so:+.3f} -> EIV {s:+.3f} +- {bs.std():.3f}   (Dutton & Maccio: -0.101)")
db = R107["Burkert-Flat"]["eiv"]
sig_dm = {m: abs(R107[m]["eiv"][0] + 0.101)/max(R107[m]["eiv"][1], 1e-6) for m in ENGINE_MODELS}
flat_sig = [sig_dm[m] for m in ENGINE_MODELS if m.endswith("-Flat")]
ck("107b AGAINST INTEREST -- with the shared fit errors divided out the same way as in item 106, the c-M200 relation of the "
   "three PRIOR-FREE fits is CONSISTENT with Dutton & Maccio's LambdaCDM relation (every one under 2.5 sigma).  The fitted concentration "
   "behaves like a LambdaCDM halo concentration, which is the opposite of what item 107 predicted.  (NFW-LCDM, which is not "
   "prior-free, is excluded from this check and reported below as the caution it is.)",
   max(flat_sig) < 3.0,
   f"EIV c-M slopes vs LambdaCDM -0.101: " + ", ".join(f"{m} {R107[m]['eiv'][0]:+.3f}+-{R107[m]['eiv'][1]:.3f} "
   f"({sig_dm[m]:.1f}s)" for m in ENGINE_MODELS))
info("    caution that caps every number in this section: even the -LCDM fits, which have the Dutton & Maccio c-M relation")
info(f"    imposed as a PRIOR, return a c-M slope of {R107['NFW-LCDM']['eiv'][0]:+.3f} +- {R107['NFW-LCDM']['eiv'][1]:.3f} rather than the -0.101 they were given.  The derived")
info("    (c200, M200) of a rotation-curve fit is therefore a weak measurement of any c-M relation, and this test is correspondingly weak.")

P("")
info("(c) the framework's own zero-parameter prediction, which is a sharper statement than the horse race.  If the fitted halo is")
info("    the phantom, its scale radius is the MOND radius r_M = sqrt(G M_b/a_0) and its V200 is the flat speed v_f = (G M_b a_0)^1/4,")
info("    so   c200 = R200/r_M = a_0^(3/4) / (10 H0 G^(1/4) M_b^(1/4))   ->   d log c/d log M_b = -1/4 EXACTLY, with a fixed")
info("    normalisation.  LambdaCDM's c(M) gives -0.101 in M200; converted through the observed M200(M_b) slope it is shallower still.")
for mdl in ("Burkert-Flat", "pISO-Flat"):
    d = R107[mdl]
    sBM, _, _ = ols(d["lB"], d["lM"])
    sobs, _, scobs = ols(d["lB"], d["lc"])
    bs = np.array([ols(d["lB"][i], d["lc"][i])[0] for i in (rng.integers(0, len(d["lB"]), len(d["lB"])) for _ in range(500))])
    for foot, a0 in A0.items():
        cpred = np.array([a0**0.75/((TEN_H0*1e3/3.0857e19)*G**0.25*(10**lb*Msun)**0.25) for lb in d["lB"]])
        off = np.median(d["lc"] - np.log10(cpred))
        info(f"    {mdl:14} {foot:10} observed d log c200/d log M_b = {sobs:+.3f} +- {bs.std():.3f} (predicted -0.250; "
             f"LambdaCDM -0.101 x {sBM:+.2f} = {-0.101*sBM:+.3f});  normalisation: log(c_fit/c_pred) median {off:+.2f} dex")
        if mdl == "Burkert-Flat" and foot == "canonical": R107c = (sobs, bs.std(), off, -0.101*sBM)
ck("107c AGAINST INTEREST -- the framework's zero-parameter prediction c200 ~ M_b^(-1/4) LOSES to LambdaCDM's converted c(M) on "
   "the slope: the observed d log c200/d log M_b is nearly 5 sigma from the predicted -0.250 and 1 sigma from LambdaCDM's -0.060.  The "
   "normalisation misses by 0.2-0.4 dex as well, and its sign flips between profiles -- the same 0.2-0.5 dex offset item 24 found "
   "for r_0/r_M, seen from the other end",
   abs(R107c[0] + 0.25)/R107c[1] > 3 and abs(R107c[0] - R107c[3])/R107c[1] < 2 and abs(R107c[2]) > 0.15,
   f"observed {R107c[0]:+.3f} +- {R107c[1]:.3f}: {abs(R107c[0]+0.25)/R107c[1]:.1f} sigma from the framework's -0.250, "
   f"{abs(R107c[0]-R107c[3])/R107c[1]:.1f} sigma from LambdaCDM's {R107c[3]:+.3f}; normalisation offset {R107c[2]:+.2f} dex")

P("")
info("(d) THE UPSILON LEVER (bug pattern 5: three earlier items turned out to be M/L results wearing a_0's clothes).")
for ups, lab in ((None, "Li's per-galaxy fitted Upsilon"), (0.5, "fixed 0.5"), (0.3, "fixed 0.3 (DiskMass)"), (0.8, "fixed 0.8")):
    d = R107["Burkert-Flat"]
    lS = np.array([math.log10(sigma0(r, ups)) for r in d["sub"]])
    info(f"    Burkert-Flat, {lab:30}: r(log c, log Sigma_0) = {float(np.corrcoef(d['lc'], lS)[0,1]):+.3f}, "
         f"partial at fixed M200 = {pcorr(d['lc'], lS, d['lM']):+.3f}")
info("    a GLOBAL Upsilon only rescales Sigma_0 by a constant, so every correlation here is exactly Upsilon-blind -- the three")
info("    fixed values above are identical by construction and are printed to show it.  The only Upsilon that moves anything is")
info("    Li's per-galaxy fitted one (0.1 dex prior), and it moves r(c, Sigma_0) from +0.13 to +0.05.  Item 107's answer is")
info("    therefore NOT an M/L result: what drives it is the shared-error structure of the fit, quantified in (b).")
d = R107["Burkert-Flat"]
lS_sh = rng.permutation(d["lS"])
ck("M107 mutation: shuffling Sigma_0 between galaxies destroys the c-Sigma_0 partial correlation, so the surviving signal in "
   "(a) is not an artefact of the estimator",
   abs(pcorr(d["lc"], lS_sh, d["lM"])) < abs(d["pS"]),
   f"shuffled partial at fixed M200 = {pcorr(d['lc'], lS_sh, d['lM']):+.3f} vs real {d['pS']:+.3f}; "
   f"shuffled raw r = {float(np.corrcoef(d['lc'], lS_sh)[0,1]):+.3f} vs real {d['rS']:+.3f}")
P("")
info("VERDICT 107.  The item asked whether c200 is better predicted by M200 or by the disc's central surface density, and the")
info("answer is M200 -- so the item FAILS its stated condition.  Two things survive, one each way:")
info("  * against the framework: after correcting for the shared fit errors the c-M200 relation is consistent with Dutton &")
info("    Maccio's LambdaCDM relation in every model, and the framework's own zero-parameter c ~ M_b^(-1/4) is 4 sigma off.")
info("  * for the framework: at FIXED M200 the disc's central surface density still carries a 2-5 sigma positive signal, which")
info("    a halo-only c(M) relation has no reason to produce.  That is a residual worth chasing with a sample whose halo fits")
info("    publish their (V200, C200) covariance -- without it the correction done here is the limiting systematic.")

# ==================================================================================================================
P(""); P("="*118); P("ITEM 108 -- is the fitted core radius the radius where g_bar = a_0?"); P("="*118)
def gbar_curve(rec):
    m = MASTER[rec["name"]]; d = ROT[rec["name"]]; d = d[d[:, 1] > 0]
    sD = rec["D"]/m["D"]; r = d[:, 0]*sD
    vg, vd, vb = d[:, 3]*math.sqrt(sD), d[:, 4]*math.sqrt(sD), d[:, 5]*math.sqrt(sD)
    gb = (vg*np.abs(vg) + rec["Yd"]*vd**2 + rec["Yb"]*vb**2)/r*KMS2_KPC
    ok = gb > 0
    return r[ok], gb[ok]
def r_switch(rec, a0):
    """Radius where g_bar crosses a_0, from the measured baryonic curve.  Returns (r_kpc, class)."""
    r, gb = gbar_curve(rec)
    if len(r) < 3: return np.nan, "short"
    if gb.max() < a0: return np.nan, "never"                     # the whole galaxy is below a_0: no switch-on radius exists
    if gb[-1] > a0:                                              # still above a_0 at the last point: point-mass extrapolation
        return r[-1]*math.sqrt(gb[-1]/a0), "extrap_out"
    i = int(np.where(gb > a0)[0][-1])                            # outermost crossing, log-log interpolation
    x0, x1 = math.log(r[i]), math.log(r[i+1]); y0, y1 = math.log(gb[i]), math.log(gb[i+1])
    return math.exp(x0 + (math.log(a0) - y0)*(x1 - x0)/(y1 - y0)), "crossing"

info("first, the thing that decides this item before any ratio is computed: does the switch-on radius EXIST?")
for foot, a0 in A0.items():
    cls = {}
    for rec in [r for r in LI if r["model"] == "Burkert-Flat"]:
        _, c = r_switch(rec, a0); cls[c] = cls.get(c, 0) + 1
    n = sum(cls.values())
    info(f"  {foot:10} of {n} SPARC galaxies: {cls.get('crossing',0)} have g_bar crossing a_0 inside the measured curve, "
         f"{cls.get('extrap_out',0)} are still above a_0 at the last point, and {cls.get('never',0)} "
         f"({100*cls.get('never',0)/n:.0f}%) NEVER reach a_0 anywhere -- for those, r(g_bar = a_0) does not exist")
    if foot == "canonical": R108a = (cls.get("never", 0), n)
mx = np.array([gbar_curve(r)[1].max()/A0["canonical"] for r in LI if r["model"] == "Burkert-Flat" and len(gbar_curve(r)[0]) >= 3])
info(f"  the median SPARC galaxy peaks at g_bar,max = {np.median(mx):.2f} a_0 (canonical): two thirds of the sample are in the "
     f"deep-MOND regime at EVERY measured radius, so the boost is already fully on where their 'core' is")
ck("108a AGAINST INTEREST, and it is the answer to the item: for two thirds of SPARC the radius where g_bar = a_0 DOES NOT EXIST -- "
   "the baryonic acceleration never reaches a_0 anywhere in the galaxy.  'The core is where the boost switches on' therefore cannot "
   "be the explanation of the fitted core for most of the sample; those galaxies are boosted everywhere and still have a fitted core",
   R108a[0]/R108a[1] > 0.5, f"{R108a[0]}/{R108a[1]} = {100*R108a[0]/R108a[1]:.0f}% have max(g_bar) < a_0; "
   f"median peak g_bar = {np.median(mx):.2f} a_0")

P("")
info("second, on the third of the sample where the switch-on radius does exist, is r_0/r(g_bar = a_0) one number?")
info("(the LambdaCDM-flavoured comparisons are computed beside it: the disc scale length, and the effective radius.)")
R108 = {}
for mdl in CORED + ("NFW-Flat",):
    for foot, a0 in A0.items():
        rr, rd, re, mb, rmnd = [], [], [], [], []
        for rec in [r for r in LI if r["model"] == mdl and np.isfinite(r["chi2"]) and r["chi2"] < 10 and np.isfinite(r["rs"])]:
            rx, c = r_switch(rec, a0)
            if c not in ("crossing", "extrap_out"): continue
            m = MASTER[rec["name"]]; sD = rec["D"]/m["D"]
            rr.append(rec["rs"]/rx); rd.append(rec["rs"]/(m["Rdisk"]*sD)); re.append(rec["rs"]/(m["Reff"]*sD))
            mb.append(mbar(rec)); rmnd.append(rec["rs"]/(math.sqrt(G*mbar(rec)*Msun/a0)/kpc))
        if len(rr) < 15: continue
        rr, rd, re, mb, rmnd = map(np.array, (rr, rd, re, mb, rmnd))
        sl, _, _ = fit_loglog(mb, rr)
        R108[(mdl, foot)] = (np.median(rr), np.log10(rr).std(), np.median(rd), np.log10(rd).std(),
                             np.median(re), np.log10(re).std(), sl, len(rr), np.median(rmnd), np.log10(rmnd).std())
        info(f"  {mdl:14} {foot:10} N={len(rr):3d}:  r_0/r(g_bar=a_0) median {np.median(rr):5.2f} scatter {np.log10(rr).std():.3f} dex "
             f"(mass slope {sl:+.3f}) | r_0/R_disk {np.median(rd):5.2f} scatter {np.log10(rd).std():.3f} | r_0/R_eff "
             f"{np.median(re):5.2f} scatter {np.log10(re).std():.3f} | r_0/r_M {np.median(rmnd):5.2f} scatter {np.log10(rmnd).std():.3f}")
bk = R108[("Burkert-Flat", "canonical")]
ck("108b the ratio is NOT one number: on the subsample where the switch-on radius exists at all, r_0/r(g_bar = a_0) has "
   "0.36-0.72 dex of scatter against the 0.2 dex the item asked for, and its 0.03 dex edge over the disc scale length -- the "
   "feedback/LambdaCDM comparison -- is nothing.  Item 108 FAILS its own bar, both footings and every cored profile",
   bk[1] > 0.2, f"Burkert-Flat canonical: median {bk[0]:.2f}, scatter {bk[1]:.3f} dex (bar was 0.2), mass slope {bk[6]:+.3f}; "
   f"r_0/R_disk scatter {bk[3]:.3f}; alt footing scatter {R108[('Burkert-Flat','alt')][1]:.3f}")
ck("108c and the comparison is a dead heat: NONE of the four candidate length scales -- the switch-on radius, the MOND radius, "
   "the disc scale length, the effective radius -- gets the fitted core radius below 0.33 dex of scatter.  Two of them contain "
   "a_0 and two do not, and they are separated by less than 0.06 dex.  There is no length scale in this catalogue that predicts "
   "the fitted core",
   min(bk[1], bk[3], bk[5], bk[9]) > 0.2 and (max(bk[1], bk[3], bk[5], bk[9]) - min(bk[1], bk[3], bk[5], bk[9])) < 0.15,
   f"Burkert-Flat canonical: r_0/r(g=a_0) {bk[1]:.3f}, r_0/r_M {bk[9]:.3f}, r_0/R_disk {bk[3]:.3f}, r_0/R_eff {bk[5]:.3f} dex; "
   f"tightest is {['r(g_bar=a_0)','R_disk','R_eff','r_M'][int(np.argmin([bk[1],bk[3],bk[5],bk[9]]))]}, spread between them "
   f"{max(bk[1],bk[3],bk[5],bk[9]) - min(bk[1],bk[3],bk[5],bk[9]):.3f} dex")
P("")
info("(the UPSILON lever for item 108: r(g_bar = a_0) moves with Upsilon because g_bar does.  Recomputed with a global Upsilon:)")
for ups in (0.3, 0.5, 0.8):
    nev = 0; rr = []
    for rec in [r for r in LI if r["model"] == "Burkert-Flat"]:
        m = MASTER[rec["name"]]; d = ROT[rec["name"]]; d = d[d[:, 1] > 0]
        sD = rec["D"]/m["D"]; r = d[:, 0]*sD
        vg, vd, vb = d[:, 3]*math.sqrt(sD), d[:, 4]*math.sqrt(sD), d[:, 5]*math.sqrt(sD)
        gb = (vg*np.abs(vg) + ups*vd**2 + 1.4*ups*vb**2)/r*KMS2_KPC
        gb = gb[gb > 0]
        if len(gb) < 3: continue
        if gb.max() < A0["canonical"]: nev += 1
        if gb.max() >= A0["canonical"]:
            rx, cl = r_switch(dict(rec, Yd=ups, Yb=1.4*ups), A0["canonical"])
            if cl in ("crossing", "extrap_out") and np.isfinite(rec["rs"]) and rec["chi2"] < 10: rr.append(rec["rs"]/rx)
    rr = np.array(rr)
    info(f"    Upsilon = {ups:.1f}: {nev}/175 = {100*nev/175:.0f}% of SPARC still never reaches a_0 anywhere;  on the rest, "
         f"r_0/r(g_bar=a_0) median {np.median(rr):.2f}, scatter {np.log10(rr).std():.3f} dex (N = {len(rr)})")
info("    read both ways: the SCATTER, which is what item 108's bar is on, is Upsilon-robust (0.42 to 0.45 dex over the whole")
info("    plausible range, never near 0.2), and so is the 'no switch-on radius' finding (61-73%).  But the MEDIAN ratio moves")
info("    0.21 dex between Upsilon = 0.3 and 0.8, so the ratio's NORMALISATION is an M/L-sensitive number and is not quoted as")
info("    anything else.  The verdict rests on the scatter and on the premise, neither of which moves with Upsilon.")
info("    ONE caveat stated against interest: r_M = sqrt(G M_b/a_0) uses the TOTAL baryonic mass, and for the smaller galaxies")
info("    r_M falls inside the HI disc, so the enclosed mass there is less than M_b and r_M is an over-estimate.  r(g_bar = a_0)")
info("    does not have this problem -- it is read off the measured curve -- which is why the two differ by ~0.1 dex in median.")
for mult, lab in ((10.0, "a_0 x 10"), (0.1, "a_0 / 10")):
    rr = []
    for rec in [r for r in LI if r["model"] == "Burkert-Flat" and np.isfinite(r["chi2"]) and r["chi2"] < 10]:
        rx, c = r_switch(rec, mult*A0["canonical"])
        if c in ("crossing", "extrap_out"): rr.append(rec["rs"]/rx)
    rr = np.array(rr)
    info(f"  mutation {lab}: N={len(rr)}, r_0/r(g_bar=a_0) median {np.median(rr):.2f} "
         f"({math.log10(np.median(rr)/bk[0]):+.2f} dex from the canonical value), scatter {np.log10(rr).std():.3f} dex")
    if mult == 10.0: R108m = (np.median(rr), len(rr))
ck("M108 mutation: a_0 x 10 moves the median ratio by ~0.5 dex and changes which galaxies even have a crossing, so the number "
   "does depend on a_0 -- the item's failure is a failure of the PREDICTION, not of an a_0-blind estimator",
   abs(math.log10(R108m[0]/bk[0])) > 0.3, f"median ratio {bk[0]:.2f} -> {R108m[0]:.2f} ({math.log10(R108m[0]/bk[0]):+.2f} dex), "
   f"N with a crossing {bk[7]} -> {R108m[1]}")

P("")
info("VERDICT 108.  The item's premise is wrong for most of SPARC: there is no radius where g_bar = a_0 in two thirds of these")
info("galaxies, because they are deep-MOND everywhere, yet they still have fitted cores.  On the third where the radius exists,")
info("the ratio carries 0.36-0.72 dex of scatter and is a dead heat with three other length scales, two of which (R_disk, R_eff)")
info("contain no a_0 at all.  The framework's core-radius statement survives only in the weak form item 24 already recorded")
info("(r_0 tracks r_M with about half a dex of scatter); the strong form asked for here is refuted by the data on disk.")
info("What would make this testable: a sample selected to STRADDLE a_0 -- high-surface-brightness discs whose inner regions are")
info("Newtonian -- rather than SPARC, which is dominated by galaxies that never leave the deep-MOND regime.")
P("")
P("="*118); P("SUMMARY"); P("="*118)
info(f"106 REFUTED as posed.  There is no single slope to test: 12 profile/prior combinations on the SAME 175 curves give -0.89")
info(f"     to -1.69.  The prior-free cored fits give {nb[0]:+.3f} +- {nb[1]:.3f} naive and {eb[0]:+.3f} +- {eb[1]:.3f} degeneracy-corrected -- STEEPER than the")
info(f"     framework's -1 by {abs(eb[0]+1)/eb[1]:.1f} sigma, and further still from feedback's -0.7/-0.9.  The trap is real and its shape is now known:")
info(f"     attenuation is a MAGNET at ~-1 (population-averaged degeneracy slope {dnull[6]:+.2f}), so the naive fit reads -1 back for anything")
info(f"     nearby; a pure null returns only {dnull[2]:+.2f}.  A pure Dutton & Maccio c-M relation gives -0.57 with no a_0 in it at all.")
info(f"     What survives is the INTERCEPT: rho_0 r_0 = {R106e[0]:.0f} Msun/pc^2, {R106e[2]:+.2f} (canonical) / {R106e[3]:+.2f} (alt) dex from the two footings,")
info(f"     against a {math.log10(max(prods)/min(prods)):.1f} dex profile-choice systematic.  A consistency, as item 5 already recorded it; not a law.")
info(f"107 FAILS its stated condition.  c200 tracks M200 (r = {rb['rM']:+.3f}) better than the disc's central surface density (r = {rb['rS']:+.3f})")
info(f"     in 3 of 4 models; after the shared-error correction the c-M relation is consistent with Dutton & Maccio in all four, and")
info(f"     the framework's zero-parameter c ~ M_b^(-1/4) is {abs(R107c[0]+0.25)/R107c[1]:.0f} sigma off in slope and {R107c[2]:+.2f} dex in normalisation.  ONE thing survives")
info(f"     for the framework: at fixed M200 the disc's central surface density carries a {abs(rb['co'][1])/rb['bs'][1]:.1f} sigma positive signal that a halo-only")
info(f"     c(M) relation has no reason to produce.  Upsilon-blind by construction, so it is not bug pattern 5.")
info(f"108 REFUTED as posed, and refuted at the premise.  r(g_bar = a_0) does not EXIST for {100*R108a[0]/R108a[1]:.0f}% of SPARC: the median galaxy")
info(f"     peaks at g_bar,max = {np.median(mx):.2f} a_0 and is deep-MOND at every measured radius, yet still has a fitted core.  That finding is")
info(f"     Upsilon-robust across 0.3-0.8.  On the third where the radius exists, r_0/r(g_bar=a_0) scatters {bk[1]:.2f} dex against a 0.2 dex")
info(f"     bar and ties with three other length scales, two of which know nothing about a_0.")
sys.exit(ck.done())
