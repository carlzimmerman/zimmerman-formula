"""AGB2R checks and Part H (blind re-implementation of AGB2 from FROZEN_CRITERIA.md + AMENDMENT_1.md; see READING.md).

Usage: python3 agb2r_run.py MODE
  design : K3 mutation twins (both weightings) and the power forecast sigma_A of every Part H configuration.
           Reads no supernova magnitude. Exit 3 if every twin passes, 4 otherwise.
  K1     : flat LCDM on sample k1, m_b_corr, full covariance, offset profiled.
  H      : K2, K4 (as frozen and as amended), Part H (both weightings), and the reported-only items.
Each mode writes agb2r_<MODE>.json and prints its log (redirect to agb2r_<MODE>.out).
Weightings: "full" = inverse of the symmetrised STAT+SYS sub-block (as frozen); "diag" = 1/C_ii (amendment 1).
"""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb2r_galaxy as G

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
PPDIR = os.path.normpath(os.path.join(REPO, "..", "_external_data", "pantheonplus_dr"))
SLOPE = 0.030
SEED = 20261114
NDRAW = 400
BANDS = [(0.01, 0.05), (0.05, 0.15), (0.15, 0.30), (0.30, 0.50), (0.50, 1.00)]
LOWZ_OTHER = [5, 18, 50, 51, 56, 57, 61, 62, 63, 64, 65, 66]
DROPS = {"SDSS": [1], "SNLS": [4], "PS1": [15], "DES": [10], "Foundation": [150], "other_lowz": LOWZ_OTHER}


# ---------------- data ----------------
class Pantheon:
    COLS_META = ["CID", "IDSURVEY", "zHD", "zHEL", "x1", "c", "HOST_LOGMASS", "HOST_LOGMASS_ERR"]
    COLS_MAG = ["mB", "m_b_corr"]

    def __init__(s, mags):
        rows = [l.split() for l in open(os.path.join(PPDIR, "PantheonPlusSH0ES.dat"))]
        head = rows[0]; R = rows[1:]; ix = {k: i for i, k in enumerate(head)}
        col = lambda k: [r[ix[k]] for r in R]
        s.cid = np.array(col("CID")); s.ids = np.array(col("IDSURVEY"), int)
        for k in ("zHD", "zHEL", "x1", "c", "HOST_LOGMASS", "HOST_LOGMASS_ERR"):
            setattr(s, k, np.array(col(k), float))
        s.mags = mags
        if mags:
            s.mB = np.array(col("mB"), float); s.mbc = np.array(col("m_b_corr"), float)
        raw = np.array(open(os.path.join(PPDIR, "PantheonPlusSH0ES_STAT+SYS.cov")).read().split(), float)
        n = int(raw[0]); C = raw[1:].reshape(n, n)
        s.asym = float(np.max(np.abs(C - C.T))); s.C = 0.5*(C + C.T); s.n = n
        assert n == len(R)

    def mask(s, name):
        z, M, Me = s.zHD, s.HOST_LOGMASS, s.HOST_LOGMASS_ERR
        if name == "k1": return z > 0.01
        a = (z > 0.01) & (z <= 1.0) & (M > 5)
        if name == "all": return a
        if name == "measured": return a & (Me > 0) & (Me < 2) & (M != 7.0) & (M != 11.5)
        if name == "zle07": return a & (z <= 0.7)
        if name.startswith("drop_"): return a & ~np.isin(s.ids, DROPS[name[5:]])
        raise ValueError(name)


def dm_flat(z, om):
    zg = np.linspace(0, 2.6, 26001); f = 1/np.sqrt(om*(1 + zg)**3 + 1 - om)
    cum = np.concatenate([[0.0], np.cumsum(0.5*(f[1:] + f[:-1])*np.diff(zg))])
    return np.interp(z, zg, cum)


def mu_fid(zhd, zhel, om=0.334):
    return 5*np.log10((1 + zhel)*dm_flat(zhd, om))


def make_bins(z, nb):
    zs = np.sort(z); N = len(z)
    edges = zs[[int(round(k*N/nb)) for k in range(1, nb)]]
    return np.searchsorted(edges, z, side="right")


# ---------------- sample object ----------------
class Sample:
    def __init__(s, P, name, nb=20):
        s.name = name; s.idx = np.where(P.mask(name))[0]; i = s.idx
        s.z, s.zhel, s.x1, s.c = P.zHD[i], P.zHEL[i], P.x1[i], P.c[i]
        s.logm = P.HOST_LOGMASS[i].copy(); s.cid = P.cid[i]; s.ids = P.ids[i]; s.n = len(i)
        s.C = P.C[np.ix_(i, i)]; s.Cinv = np.linalg.inv(s.C); s.wd = 1/np.diag(s.C)
        s.set_bins(nb)
        if P.mags:
            mf = mu_fid(s.z, s.zhel); s.y = {"R": P.mB[i] - mf, "P": P.mbc[i] - mf}

    def set_bins(s, nb):
        s.nb = nb; s.bin = make_bins(s.z, nb); s.B = np.eye(nb)[s.bin]

    def L(s, logm=None):
        return ((s.logm if logm is None else logm) < 10).astype(float)


def dtau_grid(tau, logm, L, zmax=1.0):
    zg = np.round(np.arange(0, zmax + 1e-9, 0.01), 2)
    T = tau(logm[:, None], zg[None, :])
    hi, lo = L == 0, L == 1
    return zg, T[hi].mean(0) - T[lo].mean(0)


def templates(S, tau, logm=None):
    logm = S.logm if logm is None else logm; L = S.L(logm)
    zg, dt = dtau_grid(tau, logm, L)
    step = SLOPE*np.interp(S.z, zg, dt)*(L - 0.5)
    host = -SLOPE*tau(logm, S.z)
    return dict(step=step, host=host, L=L, zg=zg, dtau=dt)


def design(S, reading, L, D=None, g=True, extra=None):
    cols = [S.B]; names = [f"o{b}" for b in range(S.nb)]
    if g: cols.append((L - 0.5)[:, None]); names.append("g")
    if D is not None: cols.append(D[:, None]); names.append("A")
    if extra is not None:
        for nm, v in extra: cols.append(v[:, None]); names.append(nm)
    if reading == "R": cols += [S.x1[:, None], S.c[:, None]]; names += ["a", "b"]
    return np.hstack(cols), names


def wls(S, X, y, weight, cluster=None):
    """Weighted / generalised least squares. Returns beta, covariance (XᵀWX)⁻¹, chi2 and optionally the
    clustered sandwich covariance."""
    WX = S.Cinv@X if weight == "full" else S.wd[:, None]*X
    F = X.T@WX; Fi = np.linalg.inv(F); beta = Fi@(WX.T@y); r = y - X@beta
    chi2 = float(r@(S.Cinv@r)) if weight == "full" else float((S.wd*r*r).sum())
    out = dict(beta=beta, cov=Fi, chi2=chi2, r=r)
    if cluster is not None:
        u = WX*r[:, None]
        _, inv = np.unique(cluster, return_inverse=True); Gn = inv.max() + 1
        sg = np.zeros((Gn, X.shape[1])); np.add.at(sg, inv, u)
        V = Fi@(sg.T@sg)@Fi; out["sandwich"] = V; out["n_clusters"] = int(Gn)
    return out


def summary(fit, names, S, reading):
    j = {n: k for k, n in enumerate(names)}; b, V = fit["beta"], fit["cov"]
    d = dict(n=S.n, nbins=S.nb, reading=reading, chi2=fit["chi2"], ndof=int(S.n - len(names)))
    for k in ("A", "g", "a", "b"):
        if k in j: d[k] = float(b[j[k]]); d["s" + k] = float(np.sqrt(V[j[k], j[k]]))
    if "A" in j:
        d["D_A0"] = (d["A"]/d["sA"])**2; d["D_A1"] = ((d["A"] - 1)/d["sA"])**2
        if "sandwich" in fit:
            d["sA_sandwich_CR0"] = float(np.sqrt(fit["sandwich"][j["A"], j["A"]]))
            G_ = fit["n_clusters"]; d["sA_sandwich_CR1"] = d["sA_sandwich_CR0"]*np.sqrt(G_/(G_ - 1))
    if "g" in j and "sandwich" in fit:
        d["sg_sandwich_CR0"] = float(np.sqrt(fit["sandwich"][j["g"], j["g"]]))
    return d


TABLES = None


def tau_fn(kind="mean", model="", shift=0.0):
    global TABLES
    if TABLES is None: TABLES = G.tables_from_npz()
    key = kind + (("_" + model) if model else "")
    return G.AgeModel({kind: TABLES[key]}, kind, shift)


# ---------------- modes ----------------
def mode_design(log, res):
    P = Pantheon(mags=False); code = 0
    S = Sample(P, "all"); tpl = templates(S, tau_fn())
    res["dtau_all_mean"] = {f"{z:.2f}": float(np.interp(z, tpl["zg"], tpl["dtau"])) for z in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9)}
    log("Delta tau(z), sample all, mean age (Gyr): " + "  ".join(f"z {k}: {v:.3f}" for k, v in res["dtau_all_mean"].items()))
    log("   (criteria quote 3.45, 3.31, 3.08, 2.68, 2.33, 1.79, 1.38, 1.07)")
    twins = []
    for weight in ("full", "diag"):
        for reading in ("R", "P"):
            for t in ("step", "host"):
                for a_true in (1.0, 0.0):
                    X, names = design(S, reading, tpl["L"], tpl[t])
                    j = {n: k for k, n in enumerate(names)}
                    beta = np.zeros(len(names)); beta[:S.nb] = 24.0 + 0.01*np.arange(S.nb); beta[j["g"]] = 0.05; beta[j["A"]] = a_true
                    if reading == "R": beta[j["a"]] = -0.15; beta[j["b"]] = 3.1
                    y = X@beta
                    f = wls(S, X, y, weight); A = float(f["beta"][j["A"]])
                    ok = abs(A - a_true) <= 1e-6 and f["chi2"] <= 1e-8
                    twins.append(dict(weight=weight, reading=reading, template=t, A_true=a_true, A=A, chi2=f["chi2"], passed=bool(ok)))
                    log(f"K3 twin [{weight}] reading {reading} {t:4s} A_true {a_true:.0f}: A {A:+.10f}  chi2_min {f['chi2']:.2e} -> {'PASS' if ok else 'FAIL'}")
    res["K3"] = dict(twins=twins, passed_full=all(t["passed"] for t in twins if t["weight"] == "full"),
                     passed_diag=all(t["passed"] for t in twins if t["weight"] == "diag"))
    allok = res["K3"]["passed_full"] and res["K3"]["passed_diag"]
    log(f"K3 full covariance: {'PASS' if res['K3']['passed_full'] else 'FAIL'};  K3 diagonal: {'PASS' if res['K3']['passed_diag'] else 'FAIL'}")
    code = 3 if allok else 4
    # power forecast: sigma_A from the design alone
    fc = {}
    for weight in ("full", "diag"):
        for lab, sample, reading, kind, nb in (("primary", "all", "R", "mean", 20), ("P", "all", "P", "mean", 20),
                                                ("median", "all", "R", "median", 20), ("bins40", "all", "R", "mean", 40),
                                                ("measured", "measured", "R", "mean", 20)):
            Sx = S if sample == "all" else Sample(P, sample)
            Sx.set_bins(nb); tp = templates(Sx, tau_fn(kind))
            for t in ("step", "host"):
                X, names = design(Sx, reading, tp["L"], tp[t])
                WX = Sx.Cinv@X if weight == "full" else Sx.wd[:, None]*X
                sA = float(np.sqrt(np.linalg.inv(X.T@WX)[names.index("A"), names.index("A")]))
                fc[f"{weight}|{t}|{lab}"] = sA
            Sx.set_bins(20)
        log(f"power forecast [{weight}] sigma_A step: " + "  ".join(f"{l} {fc[f'{weight}|step|{l}']:.3f}" for l in ("primary", "median", "bins40", "measured", "P"))
            + " | host: " + "  ".join(f"{l} {fc[f'{weight}|host|{l}']:.3f}" for l in ("primary", "median", "bins40", "measured", "P")))
    log("   (criteria, full covariance: step 0.40 / 0.32 / 0.40 / 0.51 / 0.40; host 0.10 / 0.07 / 0.10 / 0.15 / 0.10;"
        " amendment, diagonal: step 0.41, host 0.12)")
    res["forecast_sigma_A"] = fc
    res["n_all"] = S.n; res["n_low"] = int(tpl["L"].sum()); res["cov_asymmetry"] = P.asym
    log(f"sample all: {S.n} rows ({int(tpl['L'].sum())} low-mass); bin counts {np.bincount(S.bin).tolist()}; covariance max |C - C^T| {P.asym:.2e}")
    return code


def mode_K1(log, res):
    P = Pantheon(mags=True); m = P.mask("k1"); i = np.where(m)[0]
    C = P.C[np.ix_(i, i)]; Ci = np.linalg.inv(C); one = np.ones(len(i)); Ci1 = Ci@one; s11 = float(one@Ci1)
    y = P.mbc[i]; zh, zl = P.zHD[i], P.zHEL[i]

    def chi2(om):
        r = y - mu_fid(zh, zl, om); b = float(Ci1@r)
        return float(r@(Ci@r) - b*b/s11)
    r = minimize_scalar(chi2, bounds=(0.1, 0.7), method="bounded", options=dict(xatol=1e-7))
    om = float(r.x); ok = abs(om - 0.334) <= 0.009
    # 1-sigma from the curvature
    h = 1e-3; curv = (chi2(om + h) - 2*chi2(om) + chi2(om - h))/h**2
    res.update(n=int(len(i)), Om=om, sigma_curv=float(np.sqrt(2/curv)), chi2=float(r.fun), target=[0.334, 0.018], tol=0.009, passed=bool(ok))
    log(f"K1 flat LCDM, k1 ({len(i)} rows), m_b_corr, full covariance, offset profiled: Om {om:.4f} +- {np.sqrt(2/curv):.4f}"
        f"  chi2 {r.fun:.2f}  (Brout et al. 2022: 0.334 +- 0.018; pass |dOm| <= 0.009) -> {'PASS' if ok else 'FAIL'}")
    return 0


def fit_config(S, reading, weight, tpl, t, g=True, cluster=False):
    X, names = design(S, reading, tpl["L"], tpl[t] if t else None, g=g)
    f = wls(S, X, S.y[reading], weight, cluster=S.cid if cluster else None)
    return summary(f, names, S, reading)


def mode_H(log, res):
    P = Pantheon(mags=True)
    S = Sample(P, "all"); tpl = templates(S, tau_fn())
    res["n_all"] = S.n
    # ---------- K2 (and the published-magnitude constant step, reported) ----------
    k2 = {}
    for weight in ("full", "diag"):
        for reading in ("R", "P"):
            d = fit_config(S, reading, weight, tpl, None, cluster=True); k2[f"{weight}|{reading}"] = d
        d = k2[f"{weight}|R"]; ok = 0.02 <= d["g"] <= 0.09
        k2[f"{weight}|passed"] = bool(ok)
        log(f"K2 [{weight}] reading R, all, constant step alone: g {d['g']:+.4f} +- {d['sg']:.4f} mag  (a {d['a']:+.4f}, b {d['b']:+.4f})"
            f"  [0.02, 0.09] -> {'PASS' if ok else 'FAIL'};  reading P constant step {k2[f'{weight}|P']['g']:+.4f} +- {k2[f'{weight}|P']['sg']:.4f}")
    res["K2"] = k2
    # ---------- Part H, primary and forks, both weightings ----------
    H = {}
    configs = [("primary", "all", "R", "mean", 20), ("P", "all", "P", "mean", 20), ("median", "all", "R", "median", 20),
               ("bins40", "all", "R", "mean", 40), ("measured", "measured", "R", "mean", 20)]
    samples = {"all": S}
    for lab, sample, reading, kind, nb in configs:
        if sample not in samples: samples[sample] = Sample(P, sample)
        Sx = samples[sample]; Sx.set_bins(nb); tp = templates(Sx, tau_fn(kind))
        for weight in ("full", "diag"):
            for t in ("step", "host"):
                d = fit_config(Sx, reading, weight, tp, t, cluster=True); H[f"{weight}|{t}|{lab}"] = d
                log(f"H [{weight}] {t:4s} {lab:9s} ({Sx.n} rows, {nb} bins, reading {reading}, {kind}): A {d['A']:+.4f} +- {d['sA']:.4f}"
                    f"  dchi2(A=0) {d['D_A0']:7.3f}  dchi2(A=1) {d['D_A1']:7.3f}  g {d['g']:+.4f} +- {d['sg']:.4f}"
                    f"  sandwich {d['sA_sandwich_CR0']:.4f}")
        Sx.set_bins(20)
    res["H"] = H
    # ---------- K4: host masses shuffled inside the primary bins, by CID ----------
    rng = np.random.default_rng(SEED)
    ucid, inv = np.unique(S.cid, return_inverse=True)
    cid_mass = np.zeros(len(ucid)); cid_mass[inv] = S.logm
    cid_bin = np.zeros(len(ucid), int); cid_bin[inv] = S.bin
    groups = [np.where(cid_bin == b)[0] for b in range(S.nb)]
    draws = {f"{w}|{t}": [] for w in ("full", "diag") for t in ("step", "host")}
    tau0 = tau_fn()
    for k in range(NDRAW):
        newmass = cid_mass.copy()
        for gidx in groups:
            newmass[gidx] = cid_mass[gidx[rng.permutation(len(gidx))]]
        lm = newmass[inv]; tp = templates(S, tau0, logm=lm)
        for w in ("full", "diag"):
            for t in ("step", "host"):
                X, names = design(S, "R", tp["L"], tp[t]); f = wls(S, X, S.y["R"], w)
                draws[f"{w}|{t}"].append(float(f["beta"][names.index("A")]))
    k4 = {}
    for w in ("full", "diag"):
        for t in ("step", "host"):
            a = np.array(draws[f"{w}|{t}"]); ref = H[f"{w}|{t}|primary"]; sA = ref["sA"]
            mean_ok = abs(a.mean()) <= 0.2*sA; sc = float(a.std(ddof=1)); sc_ok = 0.8*sA <= sc <= 1.25*sA
            sw = ref["sA_sandwich_CR0"]; sw_ok = 0.8*sA <= sw <= 1.25*sA
            k4[f"{w}|{t}"] = dict(mean=float(a.mean()), scatter=sc, sigma_A=sA, mean_over_sigma=float(a.mean()/sA),
                                  scatter_over_sigma=sc/sA, sandwich=sw, sandwich_over_sigma=sw/sA,
                                  sandwich_CR1_over_sigma=ref["sA_sandwich_CR1"]/sA,
                                  passed_frozen=bool(mean_ok and sc_ok), passed_amended=bool(mean_ok and sc_ok and sw_ok))
            log(f"K4 [{w}] {t:4s}: mean A {a.mean():+.4f} ({a.mean()/sA:+.3f} sigma; |.| <= 0.2)  scatter {sc:.4f} ({sc/sA:.3f} sigma; 0.8-1.25)"
                f"  sandwich {sw:.4f} ({sw/sA:.3f} sigma)  -> frozen form {'PASS' if mean_ok and sc_ok else 'FAIL'};"
                f" amended form {'PASS' if mean_ok and sc_ok and sw_ok else 'FAIL'}")
    res["K4"] = k4; res["K4_draws"] = {k: v for k, v in draws.items()}
    # ---------- reported only ----------
    rep = {}
    # g fixed at 0
    for w in ("full", "diag"):
        for t in ("step", "host"):
            d = fit_config(S, "R", w, tpl, t, g=False); rep[f"g0|{w}|{t}"] = d
            log(f"reported [{w}] reading R, g fixed at 0, {t:4s}: A {d['A']:+.4f} +- {d['sA']:.4f}")
    # band-by-band constant step
    band = np.full(S.n, -1)
    for k, (lo, hi) in enumerate(BANDS): band[(S.z > lo) & (S.z <= hi)] = k
    assert (band >= 0).all()
    pred = SLOPE*np.interp(S.z, tpl["zg"], tpl["dtau"])
    zbar = np.array([S.z[band == k].mean() for k in range(5)]); pbar = np.array([pred[band == k].mean() for k in range(5)])
    for w in ("full", "diag"):
        for reading in ("R", "P"):
            extra = [(f"g{k}", (tpl["L"] - 0.5)*(band == k)) for k in range(5)]
            X, names = design(S, reading, tpl["L"], None, g=False, extra=extra); f = wls(S, X, S.y[reading], w)
            jj = [names.index(f"g{k}") for k in range(5)]; gk = f["beta"][jj]; Vg = f["cov"][np.ix_(jj, jj)]
            Xl = np.vstack([np.ones(5), zbar]).T; Wl = np.linalg.inv(Vg); Fl = np.linalg.inv(Xl.T@Wl@Xl)
            line = Fl@Xl.T@Wl@gk; pline = Fl@Xl.T@Wl@pbar
            rep[f"bands|{w}|{reading}"] = dict(z_mean=zbar.tolist(), n=[int((band == k).sum()) for k in range(5)], g=gk.tolist(),
                                               sg=np.sqrt(np.diag(Vg)).tolist(), predicted_A1=pbar.tolist(),
                                               slope=float(line[1]), sslope=float(np.sqrt(Fl[1, 1])), intercept=float(line[0]),
                                               slope_predicted_A1=float(pline[1]))
            log(f"bands [{w}] reading {reading}: " + "  ".join(f"z {zbar[k]:.3f}: {gk[k]:+.4f}+-{np.sqrt(Vg[k, k]):.4f} (A=1 {pbar[k]:.4f})" for k in range(5))
                + f" | line slope {line[1]:+.4f} +- {np.sqrt(Fl[1, 1]):.4f} mag/unit z (A=1 line {pline[1]:+.4f})")
    # model forks and sample forks, both templates, both readings, both weightings
    forks = []
    for lab, kind, model, shift in (("altMQ", "mean", "altMQ", 0.0), ("TW", "mean", "TW", 0.0),
                                    ("mass+0.2", "mean", "", 0.2), ("mass-0.2", "mean", "", -0.2)):
        forks.append((lab, "all", tau_fn(kind, model, shift)))
    for lab in ["zle07"] + [f"drop_{k}" for k in DROPS]:
        forks.append((lab, lab, tau_fn()))
    for lab, sample, tau in forks:
        if sample not in samples: samples[sample] = Sample(P, sample)
        Sx = samples[sample]; tp = templates(Sx, tau)
        for w in ("full", "diag"):
            for reading in ("R", "P"):
                for t in ("step", "host"):
                    d = fit_config(Sx, reading, w, tp, t); rep[f"fork|{lab}|{w}|{reading}|{t}"] = d
            dR = rep[f"fork|{lab}|{w}|R|step"]; hR = rep[f"fork|{lab}|{w}|R|host"]
            log(f"fork {lab:16s} [{w}] ({Sx.n} rows) reading R: step A {dR['A']:+.4f} +- {dR['sA']:.4f}, host A {hR['A']:+.4f} +- {hR['sA']:.4f}"
                f" | reading P: step {rep[f'fork|{lab}|{w}|P|step']['A']:+.4f}, host {rep[f'fork|{lab}|{w}|P|host']['A']:+.4f}")
    rep["dtau_all_mean"] = dict(z=tpl["zg"].tolist(), dtau=tpl["dtau"].tolist())
    res["reported"] = rep


def main():
    mode = sys.argv[1]; t0 = time.time(); log = lambda m: print(m, flush=True)
    res = dict(mode=mode, numpy=np.__version__); code = 0
    log(f"AGB2R mode {mode}")
    if mode == "design": code = mode_design(log, res)
    elif mode == "K1": code = mode_K1(log, res)
    elif mode == "H": mode_H(log, res)
    else: raise SystemExit(f"unknown mode {mode}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"agb2r_{mode}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb2r_{mode}.json ({res['seconds']} s) exit {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
