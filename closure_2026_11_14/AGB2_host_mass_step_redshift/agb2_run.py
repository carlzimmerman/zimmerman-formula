"""AGB2 checks and Part H (criteria: FROZEN_CRITERIA.md in this folder).

The progenitor-age slope of Son et al. (2025) tested on Pantheon+ host galaxies. Linear model, generalised least
squares with the full STAT+SYS covariance:
    y_i = sum_b o_b [z_i in bin b] + g (L_i - 1/2) + A x D_i  (+ a x1_i + b c_i in reading R)
L_i = 1 for a low-mass host (log M < 10). D is the step-run template or the per-host template built from the
galaxy model in agb2_galaxy.py. A = 0: no age dependence beyond a constant step; A = 1: the published slope.

Usage: python3 agb2_run.py MODE [outdir [diag]]
  "diag" (AMENDMENT_1.md): diagonal weights 1/C_ii for every fit except K1; outputs go to agb2_<MODE>_diag.json.
  KG  galaxy-model checks (reads no supernova file)
  K1  supernovae-only flat LCDM Omega_m from the published magnitudes
  K2  the raw constant host-mass step
  K3  noise-free mutation twins (exit 3 on pass, 4 on fail)
  K4  the error bar against shuffled host masses
  H   Part H: primary fits, the four forks, and the reported rows
Each mode writes agb2_<MODE>.json and prints its log (redirect to agb2_<MODE>.out)."""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious Accelerate BLAS floating-point flags (the twins recover the truth to 1e-6)
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb2_galaxy as G

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.normpath(os.path.join(REPO, "..", "_external_data", "pantheonplus_dr"))
MODE = sys.argv[1] if len(sys.argv) > 1 else "none"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
WEIGHTS = sys.argv[3] if len(sys.argv) > 3 else "full"        # "full" (as frozen) or "diag" (AMENDMENT_1.md)
assert WEIGHTS in ("full", "diag")
TAG = "" if WEIGHTS == "full" else "_diag"
SEED = 20261114
OM_FID = 0.334
GROUPS = {"SDSS": (1,), "SNLS": (4,), "PS1": (15,), "DES": (10,), "Foundation": (150,)}
BANDS = [(0.01, 0.05), (0.05, 0.15), (0.15, 0.30), (0.30, 0.50), (0.50, 1.00)]


class PP:
    """Pantheon+ table and covariance."""
    def __init__(s):
        f = os.path.join(DATA, "PantheonPlusSH0ES.dat")
        hdr = open(f).readline().split(); raw = np.genfromtxt(f, skip_header=1, dtype=str)
        g = lambda n: raw[:, hdr.index(n)].astype(float)
        s.z, s.zh, s.mcorr, s.mB, s.x1, s.c = g("zHD"), g("zHEL"), g("m_b_corr"), g("mB"), g("x1"), g("c")
        s.lm, s.le = g("HOST_LOGMASS"), g("HOST_LOGMASS_ERR")
        s.cid = raw[:, hdr.index("CID")]; s.ids = g("IDSURVEY").astype(int)
        cov = np.fromfile(os.path.join(DATA, "PantheonPlusSH0ES_STAT+SYS.cov"), sep=" "); n = int(cov[0])
        assert n == len(s.z) and len(cov) == n*n + 1
        C = cov[1:].reshape(n, n); s.asym = float(np.abs(C - C.T).max()); s.C = 0.5*(C + C.T); s._ci = {}

    def mask(s, name):
        base = (s.z > 0.01) & (s.z <= 1.0) & (s.lm > 5)
        if name == "all": return base
        if name == "k1": return s.z > 0.01
        if name == "measured":
            return base & (s.le > 0) & (s.le < 2) & ~np.isclose(s.lm, 7.0, atol=5e-4) & ~np.isclose(s.lm, 11.5, atol=5e-4)
        if name == "zle07": return base & (s.z <= 0.7)
        if name.startswith("drop_"):
            grp = name[5:]
            named = np.isin(s.ids, [i for v in GROUPS.values() for i in v])
            return base & ~(np.isin(s.ids, GROUPS[grp]) if grp in GROUPS else ~named)   # drop_other: every set not named
        raise ValueError(name)

    def cinv(s, m, full=False):
        """Weight matrix of the rows of mask m: inverse covariance (as frozen, and always for K1) or 1/C_ii (amendment 1)."""
        k = (m.tobytes(), full or WEIGHTS == "full")
        if k not in s._ci:
            s._ci[k] = np.linalg.inv(s.C[np.ix_(m, m)]) if k[1] else np.diag(1.0/np.diag(s.C)[m])
        return s._ci[k]


def mu_fid(z, zh, om=OM_FID):
    """5 log10[(1 + zHEL) D_M(zHD)] for flat LCDM, D_M in units of c/H0 (a constant offset is irrelevant)."""
    zg = np.expm1(np.linspace(0, np.log(3.5), 20001)); e = np.sqrt(om*(1 + zg)**3 + 1 - om)
    dm = np.concatenate([[0.0], np.cumsum(0.5*(1/e[1:] + 1/e[:-1])*np.diff(zg))])
    return 5*np.log10((1 + zh)*np.interp(z, zg, dm))


def bins_of(z, nb):
    e = np.quantile(z, np.linspace(0, 1, nb + 1))
    return np.clip(np.searchsorted(e, z, side="right") - 1, 0, nb - 1), e


def dtau_curve(lm, low, stat="mean", dtd="S", quench="nominal"):
    """Model age gap (Gyr) between the sample's high-mass and low-mass hosts, both aged to redshift z."""
    zg = np.linspace(0, 1.0, 101)
    dt = np.array([G.age(lm[~low], np.full((~low).sum(), q), stat, dtd, quench).mean()
                   - G.age(lm[low], np.full(low.sum(), q), stat, dtd, quench).mean() for q in zg])
    return zg, dt


def templates(pp, m, stat="mean", dtd="S", quench="nominal", dmass=0.0, lm=None):
    """Step-run and per-host templates (mag) for the rows of mask m. lm overrides the catalogue masses (K4)."""
    zz = pp.z[m]; lm = pp.lm[m] if lm is None else lm; low = lm < 10
    zg, dt = dtau_curve(lm + dmass, low, stat, dtd, quench)
    return dict(run=G.SLOPE*np.interp(zz, zg, dt)*(low - 0.5), host=-G.SLOPE*G.age(lm + dmass, zz, stat, dtd, quench),
                low=low, zg=zg, dtau=dt)


def gls(X, y, Ci):
    N = X.T@Ci@X; cov = np.linalg.inv(N); b = cov@(X.T@Ci@y); r = y - X@b
    return b, cov, float(r@Ci@r)


def fit(pp, m, reading, D, low, nb=20, gfree=True, y=None, extra_cols=None):
    """One GLS fit. D: template or None. Returns the amplitude, the constant step and the fit quality."""
    zz = pp.z[m]; b, edges = bins_of(zz, nb); n = int(m.sum())
    B = np.zeros((n, nb)); B[np.arange(n), b] = 1.0
    cols = [B]; names = [f"bin{i}" for i in range(nb)]
    if reading == "R":
        cols += [pp.x1[m], pp.c[m]]; names += ["x1", "c"]
        yv = pp.mB[m] - mu_fid(zz, pp.zh[m])
    else:
        yv = pp.mcorr[m] - mu_fid(zz, pp.zh[m])
    if y is not None: yv = y
    if extra_cols is not None:
        for nm_, v in extra_cols: cols.append(v); names.append(nm_)
    if gfree: cols.append(low - 0.5); names.append("g")
    if D is not None: cols.append(D); names.append("A")
    X = np.column_stack(cols); W = pp.cinv(m); beta, cov, chi2 = gls(X, yv, W); sd = np.sqrt(np.diag(cov))
    # sandwich error clustered by supernova (rows of one CID share their intrinsic scatter): reported beside the formula error
    _, inv = np.unique(pp.cid[m], return_inverse=True); Mv = (X.T@W)*(yv - X@beta)[None, :]
    Vk = np.zeros((inv.max() + 1, X.shape[1])); np.add.at(Vk, inv, Mv.T); sand = np.sqrt(np.diag(cov@(Vk.T@Vk)@cov))
    out = dict(n=n, n_low=int(low.sum()), n_high=int((~low).sum()), reading=reading, nbins=nb, n_par=X.shape[1], chi2=chi2,
               dof=n - X.shape[1], z_edges=[float(edges[0]), float(edges[-1])])
    for nm_ in ("x1", "c", "g", "A"):
        if nm_ in names:
            i = names.index(nm_); out[nm_] = float(beta[i]); out["sd_" + nm_] = float(sd[i])
            if nm_ in ("g", "A"): out["sandwich_sd_" + nm_] = float(sand[i])
    if "A" in names:
        out["D_A0"] = (out["A"]/out["sd_A"])**2; out["D_A1"] = ((out["A"] - 1)/out["sd_A"])**2
        if "g" in names: out["corr_A_g"] = float(cov[names.index("A"), names.index("g")]/(sd[names.index("A")]*sd[names.index("g")]))
    out["_beta"], out["_cov"], out["_names"] = beta, cov, names
    return out


def clean(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def fmt(r):
    s = f"A {r['A']:+.3f} +- {r['sd_A']:.3f} (sandwich {r['sandwich_sd_A']:.3f})  dchi2(A=0) {r['D_A0']:.2f}  dchi2(A=1) {r['D_A1']:.2f}"
    if "g" in r: s += f"  g {r['g']:+.4f} +- {r['sd_g']:.4f}"
    if "x1" in r: s += f"  a {r['x1']:+.3f} b {r['c']:+.3f}"
    return s + f"  chi2 {r['chi2']:.1f}/{r['dof']}  n {r['n']} ({r['n_low']} low, {r['n_high']} high)"


def pair(pp, sample, reading, stat="mean", nb=20, **model):
    """H1 (step run) and H2 (per host) for one configuration."""
    m = pp.mask(sample); T = templates(pp, m, stat, **model)
    return dict(H1=clean(fit(pp, m, reading, T["run"], T["low"], nb)), H2=clean(fit(pp, m, reading, T["host"], T["low"], nb)))


def band_steps(pp, m, reading, T):
    """The constant step band by band (no template), the same estimator applied to the A = 1 prediction, and a line."""
    zz = pp.z[m]; low = T["low"]
    ex = [(f"g{i}", (low - 0.5)*((zz > a) & (zz <= b))) for i, (a, b) in enumerate(BANDS)]
    r = fit(pp, m, reading, None, low, gfree=False, extra_cols=ex)
    ix = [r["_names"].index(f"g{i}") for i in range(len(BANDS))]
    gb = r["_beta"][ix]; cg = r["_cov"][np.ix_(ix, ix)]
    p = fit(pp, m, reading, None, low, gfree=False, extra_cols=ex, y=T["run"])      # the same estimator on the noise-free A = 1 prediction
    pb = p["_beta"][[p["_names"].index(f"g{i}") for i in range(len(BANDS))]]
    zb = np.array([zz[(zz > a) & (zz <= b)].mean() for a, b in BANDS]); nbd = [int(((zz > a) & (zz <= b)).sum()) for a, b in BANDS]
    Xl = np.column_stack([np.ones(len(BANDS)), zb]); W = np.linalg.inv(cg); cl = np.linalg.inv(Xl.T@W@Xl)
    line = cl@(Xl.T@W@gb); line_p = cl@(Xl.T@W@pb)
    return dict(reading=reading, bands=BANDS, z_mean=zb.tolist(), n=nbd, step=gb.tolist(), sd=np.sqrt(np.diag(cg)).tolist(),
                predicted_A1=pb.tolist(), line_slope=float(line[1]), line_slope_sd=float(np.sqrt(cl[1, 1])),
                line_slope_predicted_A1=float(line_p[1]), chi2=r["chi2"], dof=r["dof"])


def main():
    t0 = time.time(); log = lambda s: print(s, flush=True)
    res = dict(mode=MODE, weights=WEIGHTS, numpy=np.__version__); code = 0
    log(f"AGB2 mode {MODE}; weights: {'inverse of the full covariance (as frozen)' if WEIGHTS == 'full' else 'diagonal, 1/C_ii (amendment 1)'}")
    if MODE == "KG":
        zg, lmg, mean, med, tr = G.table()
        a = lambda lm, z, st="mean": float(G.age(lm, z, st))
        anchor = float(G.log_mq(0.35)); br = (float(G.log_mq(1.5)), 8.56 + 5.6*np.log10(2.5))
        frac = (a(11.5, 0) - a(10.0, 0))/(a(12.0, 0) - a(8.0, 0))
        k = tr["K"]; tau = (k - np.arange(k) - 0.5)*tr["dt"]; lm0 = np.log10(tr["M"][:, k])
        i = int(np.argmin(np.abs(lm0 - 11.5))); cw = np.cumsum(tr["m"][i, :k][::-1]); ts = tau[::-1]
        q25, q50, q75 = (float(np.interp(f*cw[-1], cw, ts)) for f in (0.25, 0.5, 0.75))
        _, _, mean2, med2, _ = G.table(dt=0.002)
        conv = float(max(np.abs(mean - mean2).max(), np.abs(med - med2).max()))
        pop = G.schechter_population()
        ok = (abs(anchor - 10.55) <= 0.01 and abs(br[0] - br[1]) <= 0.005 and frac >= 0.5 and 8.0 <= q50 <= 11.5
              and (q75 - q25) <= 2.0 and conv <= 0.05)
        lms = [8.0, 9.0, 10.0, 10.5, 11.0, 11.5, 12.0]
        res.update(anchor=anchor, branches=br, frac_rise=frac, track_logm=float(lm0[i]), half_formed_lookback=q50,
                   middle_half_span=q75 - q25, step_convergence=conv, population_z0_median=pop[0], population_z0_mean=pop[1],
                   logm=lms, mean_age={f"{z}": [a(x, z) for x in lms] for z in (0.0, 0.5, 1.0)},
                   median_age={f"{z}": [a(x, z, "median") for x in lms] for z in (0.0, 0.5, 1.0)}, passed=bool(ok))
        for z in (0.0, 0.5, 1.0):
            log(f"   mean age z {z}: " + " ".join(f"{v:5.2f}" for v in res["mean_age"][f"{z}"]))
        log("   median age z 0.0: " + " ".join(f"{v:5.2f}" for v in res["median_age"]["0.0"]))
        log(f"KG (i) log M_Q(0.35) {anchor:.3f} (10.55 +- 0.01); branches at z 1.5 {br[0]:.3f} / {br[1]:.3f}")
        log(f"KG (ii) share of the z = 0 rise of the mean age (log M 8 to 12) inside 10.0-11.5: {frac:.3f} (>= 0.5)")
        log(f"KG (iii) track ending at log M {lm0[i]:.2f}: half of the stars formed by lookback {q50:.2f} Gyr [8, 11.5];"
            f" middle half within {q75 - q25:.2f} Gyr (<= 2)")
        log(f"KG (iv) time step 4 vs 2 Myr: largest change of a tabulated age {conv:.4f} Gyr (<= 0.05)")
        log(f"   reported: z = 0 population (C14 mass function, supernova-weighted) median {pop[0]:.2f} Gyr, mean {pop[1]:.2f} Gyr")
        log(f"KG -> {'PASS' if ok else 'FAIL'}")
    else:
        pp = PP()
        log(f"Pantheon+: {len(pp.z)} rows; covariance asymmetry {pp.asym:.1e} (symmetrised)")
        for nm_ in ("all", "measured", "k1"):
            m = pp.mask(nm_); log(f"   sample {nm_}: {int(m.sum())} rows; {int((pp.lm[m] < 10).sum())} low-mass, {int((pp.lm[m] >= 10).sum())} high-mass")
        res["counts"] = {nm_: [int(pp.mask(nm_).sum()), int((pp.lm[pp.mask(nm_)] < 10).sum())] for nm_ in ("all", "measured", "k1")}
    if MODE == "K1":
        m = pp.mask("k1"); Ci = pp.cinv(m, full=True); one = np.ones(int(m.sum()))

        def c2(om):
            r = pp.mcorr[m] - mu_fid(pp.z[m], pp.zh[m], om); r = r - (one@Ci@r)/(one@Ci@one); return float(r@Ci@r)
        r = minimize_scalar(c2, bounds=(0.1, 0.6), method="bounded", options=dict(xatol=1e-7))
        ok = abs(r.x - 0.334) <= 0.009
        res.update(Om=float(r.x), chi2=float(r.fun), n=int(m.sum()), target=[0.334, 0.018], tol=0.009, passed=bool(ok))
        log(f"K1 supernovae-only flat LCDM on {int(m.sum())} rows: Om {r.x:.4f} (Brout et al. 2022: 0.334 +- 0.018)  chi2 {r.fun:.1f}"
            f" -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2":
        m = pp.mask("all"); low = pp.lm[m] < 10
        r = fit(pp, m, "R", None, low); p = fit(pp, m, "P", None, low)
        ok = 0.02 <= r["g"] <= 0.09
        res.update(R=clean(r), P=clean(p), window=[0.02, 0.09], passed=bool(ok))
        log(f"K2 raw constant step (reading R, low-mass minus high-mass): g {r['g']:+.4f} +- {r['sd_g']:.4f} mag  a {r['x1']:+.3f} b {r['c']:+.3f}"
            f"  chi2 {r['chi2']:.1f}/{r['dof']}  window [0.02, 0.09] -> {'PASS' if ok else 'FAIL'}")
        log(f"   reported: the same on the published magnitudes (reading P): g {p['g']:+.4f} +- {p['sd_g']:.4f} mag")
    elif MODE == "K3":
        m = pp.mask("all"); T = templates(pp, m); low = T["low"]; zz = pp.z[m]; b, _ = bins_of(zz, 20)
        truth = 0.1*np.sin(np.arange(20.0))[b] + 0.05*(low - 0.5)
        ok = True; res["twins"] = []
        for reading in ("R", "P"):
            base = truth + (-0.15*pp.x1[m] + 3.1*pp.c[m] if reading == "R" else 0.0)
            for tn in ("run", "host"):
                for a_true in (1.0, 0.0):
                    r = fit(pp, m, reading, T[tn], low, y=base + a_true*T[tn])
                    good = abs(r["A"] - a_true) <= 1e-6 and r["chi2"] <= 1e-8
                    ok = ok and good
                    res["twins"].append(dict(reading=reading, template=tn, A_true=a_true, A=r["A"], g=r["g"], chi2=r["chi2"], passed=bool(good)))
                    log(f"K3 twin reading {reading} template {tn:4s} A_true {a_true}: A {r['A']:+.9f}  g {r['g']:+.9f}  chi2_min {r['chi2']:.2e}"
                        + (f"  a {r['x1']:+.6f} b {r['c']:+.6f}" if reading == "R" else "") + f" -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok); code = 3 if ok else 4
    elif MODE == "K4":
        m = pp.mask("all"); T = templates(pp, m); zz = pp.z[m]; b, _ = bins_of(zz, 20); lm = pp.lm[m]
        ucid, first, inv = np.unique(pp.cid[m], return_index=True, return_inverse=True)
        ub, ulm = b[first], lm[first]
        real = {tn: fit(pp, m, "R", T[tn], T["low"]) for tn in ("run", "host")}
        rng = np.random.default_rng(SEED); draws = {"run": [], "host": []}
        for _ in range(400):
            new = ulm.copy()
            for k in range(20):
                i = np.where(ub == k)[0]; new[i] = ulm[rng.permutation(i)]
            lms = new[inv]; lows = lms < 10
            Dr = G.SLOPE*np.interp(zz, T["zg"], T["dtau"])*(lows - 0.5); Dh = -G.SLOPE*G.age(lms, zz, "mean")
            draws["run"].append(fit(pp, m, "R", Dr, lows)["A"]); draws["host"].append(fit(pp, m, "R", Dh, lows)["A"])
        ok = True
        for tn in ("run", "host"):
            a = np.array(draws[tn]); s = real[tn]["sd_A"]; good = abs(a.mean()) <= 0.2*s and 0.8 <= a.std(ddof=1)/s <= 1.25
            sw = real[tn]["sandwich_sd_A"]/s
            if WEIGHTS == "diag": good = good and 0.8 <= sw <= 1.25          # AMENDMENT_1.md, item 2
            ok = ok and good
            res[tn] = dict(mean=float(a.mean()), sd=float(a.std(ddof=1)), sigma_A=s, mean_over_sigma=float(a.mean()/s),
                           sd_over_sigma=float(a.std(ddof=1)/s), sandwich_over_sigma=float(sw), n_draws=len(a), passed=bool(good))
            log(f"K4 {tn:4s}: 400 shuffles of host mass inside redshift bins ({len(ucid)} supernovae): mean A {a.mean():+.4f}"
                f" ({a.mean()/s:+.3f} sigma; allowed 0.2)  scatter {a.std(ddof=1):.4f} against sigma_A {s:.4f} (ratio {a.std(ddof=1)/s:.3f};"
                f" allowed 0.8-1.25)  sandwich error / sigma_A {sw:.3f}" + (" (allowed 0.8-1.25)" if WEIGHTS == "diag" else " (reported)")
                + f" -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok)
    elif MODE == "H":
        P = {}
        P["primary"] = pair(pp, "all", "R"); log("primary (all, reading R, mean age, 20 bins):")
        log("   H1 step run: " + fmt(P["primary"]["H1"])); log("   H2 per host: " + fmt(P["primary"]["H2"]))
        for key, kw in (("fork_P", dict(sample="all", reading="P")), ("fork_median", dict(sample="all", reading="R", stat="median")),
                        ("fork_bins40", dict(sample="all", reading="R", nb=40)), ("fork_measured", dict(sample="measured", reading="R"))):
            P[key] = pair(pp, **kw); log(f"{key}:"); log("   H1 step run: " + fmt(P[key]["H1"])); log("   H2 per host: " + fmt(P[key]["H2"]))
        log("reported only:")
        m = pp.mask("all"); T = templates(pp, m)
        zs = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
        res["dtau"] = dict(z=zs, gyr=np.interp(zs, T["zg"], T["dtau"]).tolist())
        log("   model age gap high - low (Gyr) at z " + " ".join(f"{z:g}" for z in zs) + ": " + " ".join(f"{v:.2f}" for v in res["dtau"]["gyr"]))
        P["R_g0"] = clean(fit(pp, m, "R", T["run"], T["low"], gfree=False))
        log("   reading R, constant step fixed at 0 (every bit of the step is age): " + fmt(P["R_g0"]))
        for rd in ("R", "P"):
            bs = band_steps(pp, m, rd, T); P["bands_" + rd] = bs
            log(f"   band steps, reading {rd} (low-mass minus high-mass, mag; prediction of the slope at A = 1 beside it):")
            for (a, b), zb, n, g, s, p in zip(bs["bands"], bs["z_mean"], bs["n"], bs["step"], bs["sd"], bs["predicted_A1"]):
                log(f"      z {a:.2f}-{b:.2f} (mean {zb:.3f}, n {n:4d}): {g:+.4f} +- {s:.4f}   predicted {p:+.4f}")
            log(f"      line through the five: {bs['line_slope']:+.4f} +- {bs['line_slope_sd']:.4f} mag per unit z; predicted at A = 1: {bs['line_slope_predicted_A1']:+.4f}")
        for key, kw in (("model_eq11", dict(quench="eq11")), ("model_dtdW", dict(dtd="W")), ("model_mplus", dict(dmass=0.2)), ("model_mminus", dict(dmass=-0.2))):
            P[key] = pair(pp, "all", "R", **kw); log(f"   {key}: H1 " + fmt(P[key]["H1"])); log(f"   {key}: H2 " + fmt(P[key]["H2"]))
        for key in ["zle07"] + ["drop_" + g for g in list(GROUPS) + ["other"]]:
            P["sample_" + key] = pair(pp, key, "R"); log(f"   sample {key}: H1 " + fmt(P["sample_" + key]["H1"])); log(f"   sample {key}: H2 " + fmt(P["sample_" + key]["H2"]))
        res["fits"] = P
    elif MODE != "KG":
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, f"agb2_{MODE}{TAG}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb2_{MODE}{TAG}.json  ({res['seconds']} s)  exit {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
