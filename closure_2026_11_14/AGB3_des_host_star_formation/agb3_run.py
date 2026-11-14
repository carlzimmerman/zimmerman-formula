"""AGB3 checks and fits (criteria: FROZEN_CRITERIA.md in this folder).

The progenitor-age slope of Son et al. (2025) tested on the DES-SN5YR (Dovekie) host table: host mass, specific
star-formation rate and colour for 1,820 supernovae. Linear model, weighted least squares with each supernova's
published error (AGB2 amendment 1):
    y_i = sum_b o_b [z_i in bin b] + g (L_i - 1/2) + A x D_i  (+ a x1_i + b c_i in reading R)
L_i = 1 for a low-mass host (log M < 10). Templates D (mag):
  run   0.030 x [age gap between the sample's mass groups at z_i, mass-only galaxy model of AGB2] x (L_i - 1/2)
  sfr   -0.030 x [age of host i from its measured specific star-formation rate and redshift, two-component model]
  mass  -0.030 x [age of host i from its mass and redshift, mass-only galaxy model]

Usage: python3 -I agb3_run.py MODE [outdir]
  FORECAST  error bars from the design alone (reads no magnitude)
  KM        age-model checks (reads no supernova file)
  K1        the host table against the distance file on disk; column identity and the published mass step
  K2        the constant mass step recovered from the published standardisation
  K3        noise-free mutation twins (exit 3 on pass, 4 on fail)
  K4        the error bar against shuffled hosts and against the residuals
  D         the fits: D1, D2, U, their forks and the reported rows
Each mode writes agb3_<MODE>.json and prints its log (redirect to agb3_<MODE>.out)."""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious Accelerate BLAS floating-point flags

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("AGB3_REPO") or os.path.normpath(os.path.join(HERE, "..", ".."))     # AGB3_REPO: only for runs from a scratch copy
AGB2 = os.path.join(REPO, "closure_2026_11_14", "AGB2_host_mass_step_redshift")
sys.path.insert(0, HERE); sys.path.insert(1, AGB2)
import agb2_galaxy as G
import agb3_twocomp as T2

EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
META = os.path.join(EXT, "agb3_des_dovekie_metadata", "DES-Dovekie_Metadata.csv")
HD = os.path.join(EXT, "cfg684_inputs", "des5", "DES-Dovekie_HD.csv")
MODE = sys.argv[1] if len(sys.argv) > 1 else "none"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
SEED = 20261115
OM_FID = 0.330
ALPHA, BETA, GAMMA = 0.169, 3.14, 0.033            # published Dovekie global parameters (README beside the distance file)
BANDS = [(0.0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 1.2)]


def read_table(path):
    hdr = None; rows = []
    for line in open(path):
        if line.startswith("VARNAMES:"): hdr = line.split()[1:]
        elif line.startswith("SN:") or (hdr is not None and line.strip() and not line.startswith("#")):
            p = line.split(); rows.append(p[1:] if p[0] == "SN:" else p)
    if hdr is None:                                  # the metadata file: first line is "VARNAMES: ..." too; kept for safety
        raise RuntimeError("no VARNAMES line in " + os.path.basename(path))
    a = np.array(rows, dtype=object)
    return {n: a[:, i] for i, n in enumerate(hdr)}


class DES:
    """The Dovekie host table."""
    def __init__(s):
        t = read_table(META); f = lambda n: t[n].astype(float)
        s.cid = t["CID"].astype(str); s.ids = f("IDSURVEY").astype(int)
        s.z, s.zh, s.mu, s.err = f("zHD"), f("zHEL"), f("MU"), f("MUERR_RENORM")
        s.mB, s.x1, s.c, s.bias = f("mB"), f("x1"), f("c"), f("biasCor_mu")
        s.lm, s.ls, s.col, s.pcc = f("HOST_LOGMASS"), f("HOST_LOGsSFR"), f("HOST_COLOR"), f("PROBCC_BEAMS")
        s.n = len(s.z)

    def mask(s, name):
        if name == "full": return np.ones(s.n, bool)
        if name == "des_only": return s.ids == 10
        if name == "pure": return (s.ids == 10) & (s.pcc <= 0.1)
        raise ValueError(name)


def mu_fid(z, zh, om=OM_FID):
    zg = np.expm1(np.linspace(0, np.log(3.5), 20001)); e = np.sqrt(om*(1 + zg)**3 + 1 - om)
    dm = np.concatenate([[0.0], np.cumsum(0.5*(1/e[1:] + 1/e[:-1])*np.diff(zg))])
    return 5*np.log10((1 + zh)*np.interp(z, zg, dm))


def bins_of(z, nb):
    e = np.quantile(z, np.linspace(0, 1, nb + 1))
    return np.clip(np.searchsorted(e, z, side="right") - 1, 0, nb - 1)


def gap_curve(lm, low, stat="mean"):
    """Mass-only model: age gap (Gyr) between the sample's high-mass and low-mass hosts, both aged to redshift z."""
    zg = np.linspace(0, 1.2, 121)
    dt = np.array([G.age(lm[~low], np.full((~low).sum(), q), stat).mean() - G.age(lm[low], np.full(low.sum(), q), stat).mean() for q in zg])
    return zg, dt


def templates(d, m, stat="mean", zf=3.0, dtd="S", lm=None, ls=None):
    zz = d.z[m]; lm = d.lm[m] if lm is None else lm; ls = d.ls[m] if ls is None else ls; low = lm < 10
    zg, dt = gap_curve(lm, low, stat)
    return dict(run=G.SLOPE*np.interp(zz, zg, dt)*(low - 0.5), sfr=-G.SLOPE*T2.age(lm, ls, zz, zf=zf, dtd=dtd),
                mass=-G.SLOPE*G.age(lm, zz, stat), low=low, zg=zg, gap=dt)


def yvec(d, m, reading):
    mf = mu_fid(d.z[m], d.zh[m])
    if reading == "R": return d.mB[m] - mf                                       # nothing removed; x1 and c coefficients free
    if reading == "B": return d.mB[m] + ALPHA*d.x1[m] - BETA*d.c[m] - d.bias[m] - mf   # published standardisation and bias corrections, mass step undone
    if reading == "P": return d.mu[m] - mf                                       # as published
    raise ValueError(reading)


def fit(d, m, reading, D, low, nb=20, gfree=True, y=None, extra_cols=None):
    """One weighted-least-squares fit with weights 1 / MUERR^2. Returns amplitude, step, errors (formula and sandwich)."""
    zz = d.z[m]; b = bins_of(zz, nb); n = int(m.sum()); w = 1.0/d.err[m]**2
    B = np.zeros((n, nb)); B[np.arange(n), b] = 1.0
    cols = [B]; names = [f"bin{i}" for i in range(nb)]
    if reading == "R": cols += [d.x1[m], d.c[m]]; names += ["x1", "c"]
    yv = yvec(d, m, reading) if y is None else y
    if extra_cols is not None:
        for nm_, v in extra_cols: cols.append(v); names.append(nm_)
    if gfree: cols.append(low - 0.5); names.append("g")
    if D is not None: cols.append(D); names.append("A")
    X = np.column_stack(cols); XW = X.T*w; cov = np.linalg.inv(XW@X); beta = cov@(XW@yv); r = yv - X@beta
    sd = np.sqrt(np.diag(cov)); M = XW*r[None, :]; sand = np.sqrt(np.diag(cov@(M@M.T)@cov))
    out = dict(n=n, n_low=int(low.sum()), n_high=int((~low).sum()), reading=reading, nbins=nb, n_par=X.shape[1],
               chi2=float((w*r*r).sum()), dof=n - X.shape[1])
    for nm_ in ("x1", "c", "g", "A"):
        if nm_ in names:
            i = names.index(nm_); out[nm_] = float(beta[i]); out["sd_" + nm_] = float(sd[i]); out["sandwich_sd_" + nm_] = float(sand[i])
    if "A" in names:
        out["D_A0"] = (out["A"]/out["sd_A"])**2; out["D_A1"] = ((out["A"] - 1)/out["sd_A"])**2
        out["D_A1_half"] = ((2*out["A"] - 1)/(2*out["sd_A"]))**2                 # the same test with the template halved
    out["_beta"], out["_cov"], out["_names"] = beta, cov, names
    return out


def clean(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def fmt(r):
    s = f"A {r['A']:+.3f} +- {r['sd_A']:.3f} (sandwich {r['sandwich_sd_A']:.3f})  dchi2(A=0) {r['D_A0']:.2f}  dchi2(A=1) {r['D_A1']:.2f}  [half template: {r['D_A1_half']:.2f}]"
    if "g" in r: s += f"  g {r['g']:+.4f} +- {r['sd_g']:.4f}"
    if "x1" in r: s += f"  a {r['x1']:+.3f} b {r['c']:+.3f}"
    return s + f"  chi2 {r['chi2']:.1f}/{r['dof']}  n {r['n']} ({r['n_low']} low, {r['n_high']} high)"


CONFIGS = {  # name: (template, constant step free)
    "D1": ("run", True), "D2": ("sfr", True), "U": ("sfr", False)}


def three(d, sample, reading, nb=20, **tk):
    m = d.mask(sample); T = templates(d, m, **tk)
    return {k: clean(fit(d, m, reading, T[tn], T["low"], nb, gfree=gf)) for k, (tn, gf) in CONFIGS.items()}


def tracer_steps(d, m, reading, which):
    """Constant step band by band for one tracer (no template), beside the same estimator applied to the A = 1
    prediction of the star-formation ages. Group 1 is the 'young' side: low mass, high sSFR, blue."""
    zz = d.z[m]; low = d.lm[m] < 10
    g1 = {"mass": d.lm[m] < 10, "ssfr": d.ls[m] >= -10.0, "colour": d.col[m] <= 1.0}[which]
    ex = [(f"g{i}", (g1 - 0.5)*((zz > a) & (zz <= b))) for i, (a, b) in enumerate(BANDS)]
    r = fit(d, m, reading, None, low, gfree=False, extra_cols=ex)
    ix = [r["_names"].index(f"g{i}") for i in range(len(BANDS))]
    pred = -G.SLOPE*T2.age(d.lm[m], d.ls[m], zz)
    p = fit(d, m, reading, None, low, gfree=False, extra_cols=ex, y=pred)
    age = T2.age(d.lm[m], d.ls[m], zz)
    return dict(tracer=which, reading=reading, bands=BANDS, n=[int(((zz > a) & (zz <= b)).sum()) for a, b in BANDS],
                n_young=[int((((zz > a) & (zz <= b)) & g1).sum()) for a, b in BANDS],
                step=r["_beta"][ix].tolist(), sd=np.sqrt(np.diag(r["_cov"]))[ix].tolist(),
                predicted_A1=p["_beta"][[p["_names"].index(f"g{i}") for i in range(len(BANDS))]].tolist(),
                age_gap=[float(age[((zz > a) & (zz <= b)) & ~g1].mean() - age[((zz > a) & (zz <= b)) & g1].mean()) if (((zz > a) & (zz <= b)) & g1).sum() and (((zz > a) & (zz <= b)) & ~g1).sum() else None for a, b in BANDS])


def main():
    t0 = time.time(); log = lambda s: print(s, flush=True)
    res = dict(mode=MODE, numpy=np.__version__); code = 0
    log(f"AGB3 mode {MODE}")
    if MODE == "KM":
        from scipy.integrate import quad
        tf = float(T2.t_of_z(0.05) - T2.t_of_z(3.0)); passive = float(T2.age(10.5, -13.0, 0.05))
        num = quad(lambda t: t*T2.dtd_childress(t), 0, 6.0, limit=400, points=[0.3])[0]; den = quad(lambda t: T2.dtd_childress(t), 0, 6.0, limit=400, points=[0.3])[0]
        grid = float(np.interp(6.0, T2._TAU, T2._C["S"][1])/np.interp(6.0, T2._TAU, T2._C["S"][0]))
        tr = G.table()[4]; rows = []; worst = 0.0
        for z in (0.05, 0.5):
            k = min(int(round((float(G.t_of_z(z)) - tr["tk"][0])/tr["dt"])), tr["K"]); live = tr["kf"] <= k - 2
            M = tr["M"][live, k]; sf = tr["m"][live, k - 1]/(tr["dt"]*1e9); lm = np.log10(M); ls = np.log10(np.maximum(sf/M, 1e-30))
            o = np.argsort(lm); lm, ls = lm[o], ls[o]
            for target in (9.0, 10.0, 10.5, 11.0, 11.5):
                i = int(np.argmin(np.abs(lm - target))); a1 = float(G.age(lm[i], z)); a2 = float(T2.age(lm[i], ls[i], z))
                rows.append(dict(z=z, logm=float(lm[i]), logssfr=float(ls[i]), mass_only=a1, two_component=a2)); worst = max(worst, abs(a2 - a1))
                log(f"   z {z}: model galaxy log M {lm[i]:.2f}, log sSFR {ls[i]:.2f}: mass-only age {a1:.2f} Gyr, two-component {a2:.2f} Gyr")
        ok = abs(passive/tf - 1) <= 0.02 and abs(grid - num/den) <= 1e-3 and worst <= 1.5
        res.update(burst_age=tf, passive_age=passive, const_quad=num/den, const_grid=grid, tracks=rows, worst_track_gap=worst, passed=bool(ok))
        log(f"KM (i) a host with no star formation at z 0.05: age {passive:.2f} Gyr against the burst age {tf:.2f} (within 2 %)")
        log(f"KM (ii) constant star formation over 6 Gyr: mean age {grid:.4f} on the grid, {num/den:.4f} by quadrature (within 0.001)")
        log(f"KM (iii) the mass-only model's own galaxies through the two-component model: largest difference {worst:.2f} Gyr (<= 1.5)")
        log(f"KM -> {'PASS' if ok else 'FAIL'}")
    else:
        d = DES()
        log(f"Dovekie host table: {d.n} rows; DES {int((d.ids == 10).sum())}, legacy {int((d.ids != 10).sum())}")
        res["counts"] = {s: [int(d.mask(s).sum()), int((d.lm[d.mask(s)] < 10).sum())] for s in ("full", "des_only", "pure")}
        for s, v in res["counts"].items(): log(f"   sample {s}: {v[0]} rows; {v[1]} low-mass, {v[0] - v[1]} high-mass")
    if MODE == "FORECAST":
        out = {}
        for sample in ("des_only", "full"):
            m = d.mask(sample); T = templates(d, m); zeros = np.zeros(int(m.sum()))
            for k, (tn, gf) in CONFIGS.items():
                for rd in ("R", "P"):
                    r = fit(d, m, rd, T[tn], T["low"], gfree=gf, y=zeros); out[f"{sample}_{k}_{rd}"] = r["sd_A"]
            log(f"   {sample}: sigma_A  D1 {out[sample + '_D1_R']:.3f} (P {out[sample + '_D1_P']:.3f})  D2 {out[sample + '_D2_R']:.3f} (P {out[sample + '_D2_P']:.3f})"
                f"  U {out[sample + '_U_R']:.3f} (P {out[sample + '_U_P']:.3f})")
            zs = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.1]
            log("   mass-only age gap high - low (Gyr) at z " + " ".join(f"{q:g}" for q in zs) + ": " + " ".join(f"{v:.2f}" for v in np.interp(zs, T["zg"], T["gap"])))
        res["sigma_A"] = out
    elif MODE == "K1":
        t = read_table(HD); hz = dict(zip(t["CID"].astype(str), zip(t["zHD"].astype(float), t["MU"].astype(float), t["MUERR"].astype(float))))
        dz = max(abs(hz[c][0] - z) for c, z in zip(d.cid, d.z)); dmu = max(abs(hz[c][1] - v) for c, v in zip(d.cid, d.mu)); de = max(abs(hz[c][2] - v) for c, v in zip(d.cid, d.err))
        off = d.mB + ALPHA*d.x1 - BETA*d.c - d.bias - d.mu; hi = d.lm >= 10
        step = float(np.median(off[~hi]) - np.median(off[hi])); sc = float(max(off[hi].std(), off[~hi].std()))
        ok = len(hz) == d.n and dz <= 1e-5 and dmu <= 1e-4 and de <= 1e-4 and abs(step - GAMMA) <= 0.002 and sc <= 0.002
        res.update(n_common=len(set(hz) & set(d.cid)), max_dz=dz, max_dmu=dmu, max_derr=de, identity_step=step, identity_scatter=sc, passed=bool(ok))
        log(f"K1 host table against the distance file: {res['n_common']} supernovae in common; largest differences z {dz:.1e}, MU {dmu:.1e}, error {de:.1e}")
        log(f"K1 column identity mB + {ALPHA} x1 - {BETA} c - biasCor_mu - MU: low-mass minus high-mass {step:+.4f} mag (published step {GAMMA} +- 0.002);"
            f" scatter inside a group {sc:.4f} (<= 0.002) -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2":
        m = d.mask("full"); low = d.lm[m] < 10; r = fit(d, m, "B", None, low)
        ok = abs(r["g"] - GAMMA) <= 0.016
        res.update(B=clean(r), R=clean(fit(d, m, "R", None, low)), P=clean(fit(d, m, "P", None, low)), target=GAMMA, tol=0.016, passed=bool(ok))
        log(f"K2 constant mass step from the published standardisation with the step undone (full sample): g {r['g']:+.4f} +- {r['sd_g']:.4f} mag"
            f" (published {GAMMA} +- 0.008; tolerance 0.016) -> {'PASS' if ok else 'FAIL'}")
        log(f"   reported: raw magnitudes g {res['R']['g']:+.4f} +- {res['R']['sd_g']:.4f} (a {res['R']['x1']:+.3f}, b {res['R']['c']:+.3f}); as published g {res['P']['g']:+.4f} +- {res['P']['sd_g']:.4f}")
    elif MODE == "K3":
        m = d.mask("des_only"); T = templates(d, m); low = T["low"]; b = bins_of(d.z[m], 20)
        truth = 0.1*np.sin(np.arange(20.0))[b]; ok = True; res["twins"] = []
        for reading in ("R", "P"):
            base = truth + (-0.15*d.x1[m] + 3.1*d.c[m] if reading == "R" else 0.0)
            for k, (tn, gf) in CONFIGS.items():
                for a_true in (1.0, 0.0):
                    r = fit(d, m, reading, T[tn], low, gfree=gf, y=base + (0.05*(low - 0.5) if gf else 0.0) + a_true*T[tn])
                    good = abs(r["A"] - a_true) <= 1e-6 and r["chi2"] <= 1e-8; ok = ok and good
                    res["twins"].append(dict(reading=reading, config=k, A_true=a_true, A=r["A"], chi2=r["chi2"], passed=bool(good)))
                    log(f"K3 twin reading {reading} {k:2s} A_true {a_true}: A {r['A']:+.9f}  chi2_min {r['chi2']:.2e} -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok); code = 3 if ok else 4
    elif MODE == "K4":
        m = d.mask("des_only"); T = templates(d, m); zz = d.z[m]; b = bins_of(zz, 20); lm, ls = d.lm[m], d.ls[m]
        real = {k: fit(d, m, "R", T[tn], T["low"], gfree=gf) for k, (tn, gf) in CONFIGS.items()}
        rng = np.random.default_rng(SEED); draws = {k: [] for k in CONFIGS}
        for _ in range(400):
            p = np.arange(len(zz))
            for k in range(20):
                i = np.where(b == k)[0]; p[i] = rng.permutation(i)
            lms, lss = lm[p], ls[p]; lows = lms < 10                     # a host's mass and star-formation rate move together
            Ds = dict(run=G.SLOPE*np.interp(zz, T["zg"], T["gap"])*(lows - 0.5), sfr=-G.SLOPE*T2.age(lms, lss, zz))
            for k, (tn, gf) in CONFIGS.items(): draws[k].append(fit(d, m, "R", Ds[tn], lows, gfree=gf)["A"])
        ok = True
        for k in CONFIGS:
            a = np.array(draws[k]); s = real[k]["sd_A"]; sw = real[k]["sandwich_sd_A"]/s
            good = abs(a.mean()) <= 0.2*s and 0.8 <= a.std(ddof=1)/s <= 1.25 and 0.8 <= sw <= 1.25; ok = ok and good
            res[k] = dict(mean_over_sigma=float(a.mean()/s), sd_over_sigma=float(a.std(ddof=1)/s), sandwich_over_sigma=float(sw), sigma_A=s, passed=bool(good))
            log(f"K4 {k:2s}: 400 shuffles of hosts inside redshift bins: mean A {a.mean()/s:+.3f} sigma (allowed 0.2); scatter / sigma_A {a.std(ddof=1)/s:.3f};"
                f" sandwich / sigma_A {sw:.3f} (both allowed 0.8-1.25) -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok)
    elif MODE == "D":
        P = {}
        def show(key, r):
            log(f"{key}:"); [log(f"   {k:2s} " + fmt(r[k])) for k in CONFIGS]
        P["primary"] = three(d, "des_only", "R"); show("primary (des_only, reading R, 20 bins, z_f 3)", P["primary"])
        for key, kw in (("fork_P", dict(sample="des_only", reading="P")), ("fork_full", dict(sample="full", reading="R")),
                        ("fork_bins40", dict(sample="des_only", reading="R", nb=40)), ("fork_pure", dict(sample="pure", reading="R")),
                        ("fork_median", dict(sample="des_only", reading="R", stat="median")), ("fork_zf2", dict(sample="des_only", reading="R", zf=2.0)),
                        ("fork_zf5", dict(sample="des_only", reading="R", zf=5.0)), ("fork_B", dict(sample="des_only", reading="B"))):
            P[key] = three(d, **kw); show(key, P[key])
        m = d.mask("des_only"); T = templates(d, m)
        P["U_mass"] = clean(fit(d, m, "R", T["mass"], T["low"], gfree=False)); log("U with the mass-only per-host ages:  " + fmt(P["U_mass"]))
        log("reported only:")
        P["mass_perhost"] = clean(fit(d, m, "R", T["mass"], T["low"])); log("   per host, mass-only ages, constant step free (AGB2's H2 on this sample): " + fmt(P["mass_perhost"]))
        P["dtdW"] = three(d, "des_only", "R", dtd="W"); show("   short-delay delay-time distribution (two-component ages only)", P["dtdW"])
        P["full_P"] = three(d, "full", "P"); show("   full sample, as published", P["full_P"])
        zs = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.1]; res["gap"] = dict(z=zs, gyr=np.interp(zs, T["zg"], T["gap"]).tolist())
        age2 = T2.age(d.lm[m], d.ls[m], d.z[m]); agec = G.age(d.lm[m], d.z[m]); low = T["low"]
        res["contrast"] = dict(two_component=float(age2[~low].mean() - age2[low].mean()), mass_only=float(agec[~low].mean() - agec[low].mean()))
        log(f"   age gap between the mass groups, des_only: {res['contrast']['two_component']:.2f} Gyr from measured star formation, {res['contrast']['mass_only']:.2f} Gyr from the mass-only model")
        for sample in ("des_only", "full"):
            ms = d.mask(sample)
            for rd in ("R", "P"):
                for tr_ in ("mass", "ssfr", "colour"):
                    bs = tracer_steps(d, ms, rd, tr_); P[f"steps_{sample}_{rd}_{tr_}"] = bs
                    if sample == "des_only":
                        log(f"   {tr_} step by band, reading {rd} (young side minus old side, mag; star-formation ages predict at A = 1):")
                        for (a, b), n, ny, g, s, p, ag in zip(bs["bands"], bs["n"], bs["n_young"], bs["step"], bs["sd"], bs["predicted_A1"], bs["age_gap"]):
                            if n: log(f"      z {a:.1f}-{b:.1f} (n {n:4d}, young side {ny:4d}): {g:+.4f} +- {s:.4f}   predicted {p:+.4f}   age gap {ag if ag is None else round(ag, 2)} Gyr")
        res["fits"] = P
    elif MODE not in ("KM", "FORECAST", "K1", "K2", "K3", "K4"):
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, f"agb3_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb3_{MODE}.json  ({res['seconds']} s)  exit {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
