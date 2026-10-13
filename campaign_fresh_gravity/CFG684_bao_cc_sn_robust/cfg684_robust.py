"""CFG684 (criteria 4696798a1): narrow the tracking band CMB-free with cosmic chronometers (Moresco CCcovariance, BC03, 15 pts,
cov = diag + IMF + SPS-ooo per Moresco's notebook) and swap SN sets (DES-SN5YR Dovekie HD + STAT+SYS inverse cov; Union3 binned
mu_mat). BAO, X(z) model, bands: CFG681/682/683 verbatim. No CMB. MUTATE=1: CC -> best-fit E(z) of BAO+PP."""
import os, json, numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
SRC = os.path.join(HERE, "..", "CFG681_bao_raw_geometry", "cfg681_bao.py"); os.environ.pop("MUTATE", None)
g = {"__file__": SRC, "__name__": "cfg681"}; exec(open(SRC).read().split("def sig_equiv")[0], g)
NODES, bao_chi2, sn_pp, Igrid, Efun, zg, OMR = g["NODES"], g["bao_chi2"], g["sn_chi2"], g["Igrid"], g["Efun"], g["zg"], g["OMR"]
IN = os.path.join(HERE, "..", "..", "..", "_external_data", "cfg684_inputs")
# ---- cosmic chronometers ----
cz, cH, ceH = np.genfromtxt(os.path.join(IN, "cc", "HzTable_MM_BC03.dat"), comments="#", usecols=(0, 1, 2), unpack=True, delimiter=",")
zm, imf, slib, sps, spsooo = np.genfromtxt(os.path.join(IN, "cc", "data_MM20.dat"), comments="#", usecols=(0, 1, 2, 3, 4), unpack=True)
fi, fo = np.interp(cz, zm, imf)/100, np.interp(cz, zm, spsooo)/100
Ccc = np.diag(ceH**2) + np.outer(cH*fi, cH*fi) + np.outer(cH*fo, cH*fo); Cicc = np.linalg.inv(Ccc)
def cc_chi2(om, xn, Hdat=None):
    Hd = cH if Hdat is None else Hdat; m = Efun(om, xn, cz)
    if not np.all(np.isfinite(m)): return 1e9
    H0 = (m@Cicc@Hd)/(m@Cicc@m); r = Hd - H0*m; return float(r@Cicc@r)          # H0 profiled, no prior
# ---- DES-SN5YR (Dovekie) ----
import csv
rows = [l.split() for l in open(os.path.join(IN, "des5", "DES-Dovekie_HD.csv")) if l.startswith("SN:")]   # SNANA format: SN: CID IDSURVEY zHD zHEL MU ...
dz = np.array([float(r[3]) for r in rows]); dzh = np.array([float(r[4]) for r in rows]); dmu = np.array([float(r[5]) for r in rows])
npz = np.load(os.path.join(IN, "des5", "STAT+SYS.npz")); n = int(npz[npz.files[0]][0]); Wd = np.zeros((n, n)); Wd[np.triu_indices(n)] = npz[npz.files[1]]
Wd = Wd + np.triu(Wd, 1).T; ww = dz > 0; Cd = np.linalg.inv(Wd)[np.ix_(ww, ww)]; Wd = np.linalg.inv(Cd); dz, dzh, dmu = dz[ww], dzh[ww], dmu[ww]
one_d = np.ones(len(dmu)); Cd1 = one_d@Wd@one_d
def sn_des(om, xn):
    I = Igrid(om, xn)
    if not np.all(np.isfinite(I)): return 1e9
    r = dmu - 5*np.log10((1 + dzh)*np.interp(dz, zg, I)); b = one_d@Wd@r; return float(r@Wd@r - b*b/Cd1)
# ---- Union3 (binned spline-node mu, weight matrix) ----
from astropy.io import fits
M = fits.open(os.path.join(IN, "union3", "mu_mat_union3_cosmo=2_mu.fits"))[0].data
uz, umu, Wu = M[0, 1:], M[1:, 0], M[1:, 1:]; one_u = np.ones(len(umu)); Cu1 = one_u@Wu@one_u
def sn_u3(om, xn):
    I = Igrid(om, xn)
    if not np.all(np.isfinite(I)): return 1e9
    r = umu - 5*np.log10((1 + uz)*np.interp(uz, zg, I)); b = one_u@Wu@r; return float(r@Wu@r - b*b/Cu1)
# ---- combinations ----
Hmock = None
def total(combo, om, xn):
    c = bao_chi2(om, xn)[0]
    if "PP" in combo: c += sn_pp(om, xn)
    if "DES5" in combo: c += sn_des(om, xn)
    if "U3" in combo: c += sn_u3(om, xn)
    if "CC" in combo: c += cc_chi2(om, xn, Hmock)
    return c
def fitnodes(combo, om, start):
    f = lambda x: total(combo, om, x)
    best = None
    for s in start:
        r = minimize(f, s, method="L-BFGS-B", options=dict(maxiter=500))
        if best is None or r.fun < best.fun: best = r
    if best.fun > 1e8 or not best.success:
        r = minimize(f, best.x, method="Powell", options=dict(xtol=1e-5, ftol=1e-8)); best = r if r.fun < best.fun else best
    return best
def hessian(fun, x, h=0.01):
    n_ = len(x); H = np.zeros((n_, n_))
    for i in range(n_):
        for j in range(i, n_):
            ei, ej = np.eye(n_)[i]*h, np.eye(n_)[j]*h
            H[i, j] = H[j, i] = (fun(x+ei+ej) - fun(x+ei-ej) - fun(x-ei+ej) + fun(x-ei-ej))/(4*h*h)
    return H
def wvec(z): return np.array([np.interp(z, NODES, np.r_[0.0, np.eye(5)[i]]) for i in range(5)])
OMS = np.round(np.arange(0.24, 0.36 + 1e-9, 0.005), 4); ZS = [1.0, 1.5, 2.33]; L10 = np.log(10)
def run(combo):
    rows, prev = [], None
    for om in OMS:
        st = ([prev] if prev is not None else []) + [np.ones(5), np.linspace(1, 1.5, 5)]
        b = fitnodes(combo, om, st); prev = b.x
        cov = 2*np.linalg.pinv(hessian(lambda x: total(combo, om, x), b.x))
        Xs = {}
        for z in ZS:
            w = wvec(z); X = float(np.interp(z, NODES, np.r_[1.0, b.x])); sX = float(np.sqrt(max(w@cov@w, 0))); E = float(Efun(om, b.x, np.array([z]))[0])
            Xs[str(z)] = dict(X=X, sX=sX, E=E, sE=(1 - om - OMR)*sX/(2*E))
        rows.append(dict(om=float(om), chi2=float(b.fun), nodes=b.x.tolist(), z=Xs))
    chi = np.array([r["chi2"] for r in rows]); keep = chi <= chi.min() + 1.0; out = dict(rows=rows, dchi2_max=float(chi.max() - chi.min()),
        om_best=float(OMS[np.argmin(chi)]), om_in_1sig=[float(OMS[keep].min()), float(OMS[keep].max())])
    for z in ZS:
        sel = [r["z"][str(z)] for r, k in zip(rows, keep) if k]
        Elo = min(np.log10(s["E"]) - s["sE"]/(s["E"]*L10) for s in sel); Ehi = max(np.log10(s["E"]) + s["sE"]/(s["E"]*L10) for s in sel)
        Xhi = max(s["X"] + s["sX"] for s in sel); Xlo = min(s["X"] - s["sX"] for s in sel)
        gap = Elo - 0.5*np.log10(Xhi); sEl = np.median([s["sE"]/(s["E"]*L10) for s in sel]); sXl = np.median([0.5*s["sX"]/(s["X"]*L10) for s in sel if s["X"] > 0] or [np.inf])
        es = np.linspace(0.005, 1, 1000); ok = [e for e in es if gap > 0 and gap/np.sqrt(e*e + sEl**2 + sXl**2) >= 3]
        out[str(z)] = dict(rival=[float(10**Elo), float(10**Ehi)], tracking=[float(np.sqrt(max(Xlo, 0))), float(np.sqrt(Xhi))], gap=float(gap), e3=float(max(ok)) if ok else None)
    # flat-a0 Omega_m (CFG682 method, z* 2.33, e = 0.02) + central crossing
    X = np.array([r["z"]["2.33"]["X"] for r in rows]); sX = np.array([r["z"]["2.33"]["sX"] for r in rows])
    lsq = np.where(X > 0, 0.5*np.log10(np.maximum(X, 1e-12)), -np.inf); sl = np.where(X > 0, 0.5*sX/(np.maximum(X, 1e-12)*L10), np.inf)
    s = np.sqrt(0.02**2 + sl**2); L = np.where(np.isfinite(lsq), np.exp(-0.5*(lsq/s)**2)/s, 0); P = np.exp(-0.5*(chi - chi.min()))*L; P /= P.sum()
    m = float((P*OMS).sum()); sd = float(np.sqrt((P*(OMS - m)**2).sum()))
    idx = np.where(np.diff(np.sign(X - 1)))[0]; cross = [float(np.interp(1, X[[k+1, k]], OMS[[k+1, k]])) for k in idx]
    out["flat_a0_om"] = dict(mean=m, sd=sd, crossing=cross)
    return out
COMBOS = ["BAO+PP", "BAO+CC", "BAO+PP+CC", "BAO+DES5+CC", "BAO+U3+CC", "BAO+DES5", "BAO+U3"]
res = {"mutate": MUT, "n_cc": int(len(cz)), "n_des5": int(len(dmu)), "n_u3_nodes": int(len(umu))}
if MUT:
    ref = run("BAO+PP"); rb = min(ref["rows"], key=lambda r: r["chi2"]); m_ = Efun(rb["om"], np.array(rb["nodes"]), cz)
    H0 = (m_@Cicc@cH)/(m_@Cicc@m_); Hmock = H0*m_; COMBOS = ["BAO+PP+CC"]; res["BAO+PP"] = ref
for c in COMBOS:
    o = run(c); res[c] = o
    print(f"\n=== {c}  MUTATE={MUT}  Δχ²_max over Ωm 0.24-0.36 = {o['dchi2_max']:.2f}  best Ωm {o['om_best']}  Δχ²≤1 range {o['om_in_1sig']}")
    for z in ZS:
        q = o[str(z)]; print(f"   z*={z}: rival {q['rival'][0]:.3f}-{q['rival'][1]:.3f}  tracking {q['tracking'][0]:.3f}-{q['tracking'][1]:.3f}  gap {q['gap']:+.3f} dex  e_3σ {q['e3']}")
    f_ = o["flat_a0_om"]; print(f"   flat-a0 Ωm (z* 2.33, e 0.02) = {f_['mean']:.4f} ± {f_['sd']:.4f}  crossing {np.round(f_['crossing'], 4).tolist()}")
if MUT:
    d = min(r["chi2"] for r in res["BAO+PP+CC"]["rows"]) - min(r["chi2"] for r in res["BAO+PP"]["rows"])
    print(f"\nMUTATE: χ²min(BAO+PP+CCmock) − χ²min(BAO+PP) = {d:.3f} (must be ≤ 1)"); res["mutate_dchi2"] = float(d)
json.dump(res, open(os.path.join(HERE, "cfg684_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)
