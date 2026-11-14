"""AGB3R checks KM, K1, K2, K3, K4 and Part D (blind re-grade of AGB3; rules: AGB3's FROZEN_CRITERIA.md, my READING.md).

Usage: python3 -I agb3r_hosts.py MODE
  KM        the two-component model (no magnitude)
  forecast  design-only errors (no magnitude)
  K1        the table against the distance file; the column identity
  K3        mutation twins (exit 3 if all pass, 4 otherwise)
  K2K4      K2 (raw step in reading B) and K4 (shuffles, sandwich)
  D         Part D: D2, U, their forks, and the reported rows
Each mode writes agb3r_<MODE>.json and prints its log.
"""
import json, os, sys, time, warnings
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import agb3r_data as DA
import agb3r_model as M

MODE = sys.argv[1] if len(sys.argv) > 1 else "KM"
SLOPE = 0.030
ZG01 = np.round(np.arange(0.0, 1.6001, 0.01), 2)
SEED_K4, NDRAW = 20261115, 400
AGB2 = M.AGB2
log = lambda m: print(m, flush=True)


# ---------------- templates ----------------
def run_dtau(lm_sample, dtd="S"):
    """Delta tau(z) on the 0.01 grid: mean mass-only age of the sample's high-mass hosts minus that of its low-mass hosts."""
    hi, lo = lm_sample[lm_sample >= 10.0], lm_sample[lm_sample < 10.0]
    A = M.mass_age(hi[None, :], ZG01[:, None], dtd).mean(1); B = M.mass_age(lo[None, :], ZG01[:, None], dtd).mean(1)
    return A - B


def template(kind, z, lm, ls, zf=3.0, dtd="S", dtau=None):
    if kind == "sfr":
        return -SLOPE*M.mean_age(ls, z, zf, dtd)
    if kind == "mass":
        return -SLOPE*M.mass_age(lm, z, dtd)
    if kind == "run":
        return SLOPE*np.interp(z, ZG01, dtau)*((lm < 10.0).astype(float) - 0.5)
    raise ValueError(kind)


# ---------------- the linear fit ----------------
def y_of(meta, idx, reading):
    mf = DA.mu_fid(meta.zHD[idx], meta.zHEL[idx])
    if reading == "R": return meta.mB[idx] - mf
    if reading == "P": return meta.MU[idx] - mf
    if reading == "B": return meta.mB[idx] + 0.169*meta.x1[idx] - 3.14*meta.c[idx] - meta.biasCor_mu[idx] - mf
    raise ValueError(reading)


def design(meta, idx, reading, nb, step, D, L=None, extra=()):
    b = DA.bins(meta.zHD[idx], nb); n = len(idx)
    cols = [(b == k).astype(float) for k in range(nb)]; names = [f"o{k}" for k in range(nb)]
    L = meta.L[idx] if L is None else L
    if step: cols.append(L - 0.5); names.append("g")
    for nm, v in extra: cols.append(v); names.append(nm)
    if D is not None: cols.append(D); names.append("A")
    if reading == "R": cols += [meta.x1[idx], meta.c[idx]]; names += ["a", "b"]
    return np.column_stack(cols), names


def wls(X, y, w):
    sw = np.sqrt(w); p = np.linalg.lstsq(X*sw[:, None], y*sw, rcond=None)[0]
    B = X.T@(X*w[:, None]); C = np.linalg.inv(B); r = y - X@p
    return p, C, float((w*r*r).sum()), r


def sandwich(X, w, r, C):
    meat = X.T@(X*(w*w*r*r)[:, None])
    return C@meat@C


def fit(meta, idx, reading, nb, step, D, y=None, L=None, extra=()):
    X, names = design(meta, idx, reading, nb, step, D, L, extra)
    w = 1.0/meta.MUERR_RENORM[idx]**2
    y = y_of(meta, idx, reading) if y is None else y
    p, C, chi2, r = wls(X, y, w)
    out = dict(n=int(len(idx)), nbins=nb, reading=reading, step=bool(step), chi2=chi2, dof=int(len(idx) - X.shape[1]))
    for k in ("A", "g", "a", "b"):
        if k in names:
            j = names.index(k); out[k] = float(p[j]); out["sd_" + k] = float(np.sqrt(C[j, j]))
    for nm, _ in extra:
        j = names.index(nm); out[nm] = float(p[j]); out["sd_" + nm] = float(np.sqrt(C[j, j]))
    if "A" in names:
        j = names.index("A"); out["sd_A_sandwich"] = float(np.sqrt(sandwich(X, w, r, C)[j, j]))
        out["D_A0"] = (out["A"]/out["sd_A"])**2; out["D_A1"] = ((out["A"] - 1)/out["sd_A"])**2
    out["_X"] = X; out["_names"] = names; out["_w"] = w
    return out


def clean(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def sel(meta, name):
    return np.where(meta.sample(name))[0]


# ---------------- words ----------------
def w1(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def wu(a, d1):
    if d1 < 4: return "HOSTS AS LARGE AS THE SLOPE NEEDS"
    if a < 1 and d1 >= 9: return "SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA"
    if a < 1: return "SLOPE OVERPREDICTS THE HOSTS (2 SIGMA)"
    return "HOSTS LARGER THAN THE SLOPE NEEDS"


def halve(d):
    """The same fit with the template halved: amplitude 2A, error 2 sd."""
    a, s = 2*d["A"], 2*d["sd_A"]
    return dict(A=a, sd_A=s, D_A0=(a/s)**2, D_A1=((a - 1)/s)**2, n=d["n"], half_of=dict(A=d["A"], sd_A=d["sd_A"]))


# ---------------- modes ----------------
def mode_KM(res):
    import scipy.integrate as I
    G2 = M.G2
    tf = float(M.t_of_z(0.05) - M.t_of_z(3.0)); a13 = float(M.mean_age(-13.0, 0.05))
    ok1 = abs(a13/tf - 1) <= 0.02
    log(f"KM (i): log s = -13 at z 0.05: mean age {a13:.4f} Gyr, burst age {tf:.4f} Gyr, ratio - 1 {a13/tf - 1:+.4f} (<= 0.02) -> {'PASS' if ok1 else 'FAIL'}")
    S6 = float(np.interp(6.0, M._TAU, M._SURV)); logs6 = float(np.log10(1.0/S6/1e9))
    det = M.mean_age(logs6, 0.05, detail=True); a6 = float(det["age"])
    phi = G2.dtd_childress
    q1 = I.quad(lambda t: t*phi(t), 0, 6, limit=400, points=[0.3])[0]; q0 = I.quad(phi, 0, 6, limit=400, points=[0.3])[0]
    ok2 = abs(a6 - q1/q0) <= 0.001 and abs(float(det["tc"]) - 6.0) < 1e-6 and float(det["mb"]) == 0.0
    log(f"KM (ii): constant star formation over 6 Gyr (log s {logs6:.4f}, T_c {float(det['tc']):.6f}, burst {float(det['mb'])}):"
        f" model {a6:.4f} Gyr, quadrature {q1/q0:.4f} Gyr, diff {a6 - q1/q0:+.5f} (<= 0.001) -> {'PASS' if ok2 else 'FAIL'}")
    zg, lmg, mean, med, tr = G2.table("S")
    rows3 = []; worst = 0.0
    for z in (0.05, 0.5):
        t_obs = float(G2.t_of_z(z)); k = int(round((t_obs - tr["tk"][0])/tr["dt"])); k = min(max(k, 2), tr["K"])
        live = tr["kf"] <= k - 2
        m = tr["m"][live, :k]; tau = (k - np.arange(k) - 0.5)*tr["dt"]
        w = m*G2.dtd_childress(tau)[None, :]; tot = w.sum(1); ok = tot > 0
        mage = (w[ok]*tau[None, :]).sum(1)/tot[ok]
        Mk = tr["M"][live, k][ok]; lm = np.log10(Mk)
        sfr_yr = m[ok, k - 1]/tr["dt"]/1e9; logs = np.log10(np.maximum(sfr_yr/Mk, 1e-30))
        keep = (lm >= 9.0) & (lm <= 11.5)
        a2 = M.mean_age(logs[keep], z); d = a2 - mage[keep]
        j = int(np.argmax(np.abs(d))); worst = max(worst, float(np.abs(d).max()))
        grid = {}
        for x in (9.0, 9.5, 10.0, 10.5, 11.0, 11.5):
            i = int(np.argmin(np.abs(lm[keep] - x)))
            grid[f"{x:.1f}"] = dict(logM=float(lm[keep][i]), logs=float(logs[keep][i]), mass_age=float(mage[keep][i]), twocomp_age=float(a2[i]))
        rows3.append(dict(z=z, n_tracks=int(keep.sum()), max_abs=float(np.abs(d).max()), at_logM=float(lm[keep][j]),
                          diff_at=float(d[j]), grid=grid))
        log(f"KM (iii) z {z}: {int(keep.sum())} tracks with log M 9 ... 11.5; largest |two-component - mass-only| {np.abs(d).max():.3f} Gyr"
            f" (at log M {lm[keep][j]:.2f}, {d[j]:+.3f})")
        for x, g in grid.items():
            log(f"     log M {g['logM']:.2f}: log s {g['logs']:+.2f}  mass-only {g['mass_age']:.2f}  two-component {g['twocomp_age']:.2f}")
    ok3 = worst <= 1.5
    log(f"KM (iii): largest {worst:.3f} Gyr (<= 1.5) -> {'PASS' if ok3 else 'FAIL'}")
    ls = [-13, -12, -11, -10.5, -10, -9.5, -9, -8.5, -8]
    tab = {str(z): [float(v) for v in M.mean_age(ls, z)] for z in (0.05, 0.5, 1.0)}
    for zf in (2.0, 5.0):
        tab[f"zf{zf:g}_0.05"] = [float(v) for v in M.mean_age(ls, 0.05, zf)]
    res.update(KM=dict(i=dict(age=a13, burst_age=tf, passed=bool(ok1)), ii=dict(model=a6, quad=q1/q0, passed=bool(ok2)),
                       iii=dict(rows=rows3, worst=worst, passed=bool(ok3)), table_logs=ls, table=tab,
                       passed=bool(ok1 and ok2 and ok3)))
    log(f"KM -> {'PASS' if res['KM']['passed'] else 'FAIL'}")


def mode_forecast(res, meta):
    out = {}
    for sample in ("des_only", "full"):
        idx = sel(meta, sample); z, lm, ls = meta.zHD[idx], meta.lm[idx], meta.ls[idx]
        dt = run_dtau(lm)
        for nm, kind, step in (("D2", "sfr", True), ("U", "sfr", False), ("D1", "run", True)):
            D = template(kind, z, lm, ls, dtau=dt)
            X, names = design(meta, idx, "R", 20, step, D)
            w = 1.0/meta.MUERR_RENORM[idx]**2; C = np.linalg.inv(X.T@(X*w[:, None]))
            out[f"{nm}_{sample}"] = float(np.sqrt(C[names.index("A"), names.index("A")]))
    log("design-only sd_A (reading R, 20 bins): " + ", ".join(f"{k} {v:.3f}" for k, v in out.items()))
    log("criteria: D2 des_only 0.079, U des_only 0.065, D2 full 0.055, U full 0.050, D1 des_only 0.79, D1 full 0.44")
    res["forecast"] = out


def mode_K1(res, meta):
    hd = DA.read_hd(); j = DA.hd_index(meta, hd)
    same_order = bool(np.all(j == np.arange(meta.n)))
    dz = float(np.max(np.abs(meta.zHD[j] - hd["zHD"]))); dmu = float(np.max(np.abs(meta.MU[j] - hd["MU"])))
    de = float(np.max(np.abs(meta.MUERR_RENORM[j] - hd["MUERR"]))); dzh = float(np.max(np.abs(meta.zHEL[j] - hd["zHEL"])))
    ok_tab = len(hd["key"]) == 1820 == meta.n and dz <= 1e-5 and dmu <= 1e-4 and de <= 1e-4
    v = meta.mB + 0.169*meta.x1 - 3.14*meta.c - meta.biasCor_mu - meta.MU
    lo, hi = v[meta.L == 1], v[meta.L == 0]
    step = float(lo.mean() - hi.mean()); sc = [float(lo.std()), float(hi.std())]
    ok_id = abs(step - 0.033) <= 0.002 and max(sc) <= 0.002
    sha = DA.sha256(DA.META); ok_sha = sha == DA.META_SHA256
    log(f"K1: sha256 {'matches' if ok_sha else 'DIFFERS'}; {meta.n} rows; distance file rows {len(hd['key'])}; same row order: {same_order}")
    log(f"K1: max |zHD diff| {dz:.2e} (<= 1e-5), |zHEL diff| {dzh:.2e}, |MU diff| {dmu:.2e} (<= 1e-4), |MUERR_RENORM - MUERR| {de:.2e} (<= 1e-4)")
    log(f"K1: mB + 0.169 x1 - 3.14 c - biasCor_mu - MU: low-mass mean {lo.mean():+.5f} (sd {sc[0]:.5f}), high-mass mean {hi.mean():+.5f}"
        f" (sd {sc[1]:.5f}); step {step:.5f} (0.033 +- 0.002, scatter <= 0.002)")
    ok = bool(ok_tab and ok_id and ok_sha)
    log(f"K1 -> {'PASS' if ok else 'FAIL'}")
    res["K1"] = dict(sha_ok=ok_sha, same_order=same_order, max_dz=dz, max_dzhel=dzh, max_dmu=dmu, max_derr=de, step=step,
                     scatter=sc, passed=ok)


def mode_K3(res, meta):
    idx = sel(meta, "des_only"); z, lm, ls = meta.zHD[idx], meta.lm[idx], meta.ls[idx]
    dt = run_dtau(lm); b = DA.bins(z, 20); off = 0.10 + 0.01*b
    allok = True; rows = []
    for cfg, kind, step in (("D1", "run", True), ("D2", "sfr", True), ("U", "sfr", False)):
        D = template(kind, z, lm, ls, dtau=dt)
        for reading in ("R", "P"):
            for at in (1.0, 0.0):
                y = off + (0.05*(meta.L[idx] - 0.5) if step else 0.0) + at*D
                if reading == "R": y = y - 0.15*meta.x1[idx] + 3.1*meta.c[idx]
                f = fit(meta, idx, reading, 20, step, D, y=y)
                ok = abs(f["A"] - at) <= 1e-6 and f["chi2"] <= 1e-8; allok &= ok
                rows.append(dict(cfg=cfg, reading=reading, A_true=at, A=f["A"], chi2=f["chi2"], passed=bool(ok)))
                log(f"K3 {cfg} reading {reading} A_true {at:.0f}: A {f['A']:+.10f}  chi2_min {f['chi2']:.2e} -> {'PASS' if ok else 'FAIL'}")
    res["K3"] = dict(rows=rows, passed=bool(allok))
    log(f"K3 -> {'PASS' if allok else 'FAIL'} (exit {3 if allok else 4})")
    return 3 if allok else 4


def mode_K2K4(res, meta):
    idx = sel(meta, "full")
    f = fit(meta, idx, "B", 20, True, None)
    ok2 = abs(f["g"] - 0.033) <= 0.016
    log(f"K2: reading B, full, constant step alone: g {f['g']:+.4f} +- {f['sd_g']:.4f} mag (low-mass fainter if > 0); |g - 0.033| <= 0.016 -> {'PASS' if ok2 else 'FAIL'}")
    res["K2"] = dict(g=f["g"], sd_g=f["sd_g"], n=f["n"], passed=bool(ok2))
    # K4
    idx = sel(meta, "des_only"); z = meta.zHD[idx]; lm0, ls0 = meta.lm[idx].copy(), meta.ls[idx].copy()
    dt = run_dtau(lm0); b = DA.bins(z, 20); groups = [np.where(b == k)[0] for k in range(20)]
    cfgs = (("D1", "run", True), ("D2", "sfr", True), ("U", "sfr", False))
    real = {}
    for nm, kind, step in cfgs:
        real[nm] = fit(meta, idx, "R", 20, step, template(kind, z, lm0, ls0, dtau=dt))
    rng = np.random.default_rng(SEED_K4); draws = {nm: [] for nm, _, _ in cfgs}
    for _ in range(NDRAW):
        p = np.arange(len(idx))
        for g in groups:
            p[g] = g[rng.permutation(len(g))]
        lm, ls = lm0[p], ls0[p]; L = (lm < 10.0).astype(float)
        for nm, kind, step in cfgs:
            D = template(kind, z, lm, ls, dtau=dt)
            draws[nm].append(fit(meta, idx, "R", 20, step, D, L=L)["A"])
    out = {}
    for nm, _, _ in cfgs:
        a = np.array(draws[nm]); s = real[nm]["sd_A"]; m, sc = float(a.mean()), float(a.std(ddof=1))
        sw = real[nm]["sd_A_sandwich"]
        ok = abs(m) <= 0.2*s and 0.8 <= sc/s <= 1.25 and 0.8 <= sw/s <= 1.25
        out[nm] = dict(sd_A=s, mean_shuffle=m, scatter_shuffle=sc, ratio_scatter=sc/s, sd_sandwich=sw, ratio_sandwich=sw/s,
                       mean_over_sd=m/s, passed=bool(ok))
        log(f"K4 {nm}: sd_A {s:.4f}; shuffles: mean {m:+.4f} ({m/s:+.3f} sd, |.| <= 0.2), scatter {sc:.4f} (ratio {sc/s:.3f}, 0.8-1.25);"
            f" sandwich {sw:.4f} (ratio {sw/s:.3f}, 0.8-1.25) -> {'PASS' if ok else 'FAIL'}")
    res["K4"] = dict(draws=NDRAW, seed=SEED_K4, cfg=out)


def mode_D(res, meta):
    def run(sample, reading, kind, step, nb=20, zf=3.0, dtd="S"):
        idx = sel(meta, sample); z, lm, ls = meta.zHD[idx], meta.lm[idx], meta.ls[idx]
        dt = run_dtau(lm, dtd) if kind == "run" else None
        f = clean(fit(meta, idx, reading, nb, step, template(kind, z, lm, ls, zf, dtd, dt)))
        f.update(sample=sample, template=kind, zf=zf, dtd=dtd)
        return f
    D2 = dict(primary=run("des_only", "R", "sfr", True))
    D2["P"] = run("des_only", "P", "sfr", True); D2["full"] = run("full", "R", "sfr", True)
    D2["bins40"] = run("des_only", "R", "sfr", True, nb=40); D2["pure"] = run("pure", "R", "sfr", True)
    D2["zf2"] = run("des_only", "R", "sfr", True, zf=2.0); D2["zf5"] = run("des_only", "R", "sfr", True, zf=5.0)
    D2["half"] = halve(D2["primary"])
    U = dict(primary=run("des_only", "R", "sfr", False))
    U["B"] = run("des_only", "B", "sfr", False); U["full"] = run("full", "R", "sfr", False)
    U["bins40"] = run("des_only", "R", "sfr", False, nb=40); U["pure"] = run("pure", "R", "sfr", False)
    U["zf2"] = run("des_only", "R", "sfr", False, zf=2.0); U["zf5"] = run("des_only", "R", "sfr", False, zf=5.0)
    U["half"] = halve(U["primary"]); U["mass"] = run("des_only", "R", "mass", False)
    for name, blk, rule in (("D2", D2, "w1"), ("U", U, "wu")):
        log(f"{name}:")
        for k, d in blk.items():
            word = w1(d["D_A0"], d["D_A1"]) if rule == "w1" else wu(d["A"], d["D_A1"])
            d["word"] = word
            extra = f"  g {d['g']:+.4f} +- {d['sd_g']:.4f}" if "g" in d else ""
            sw = f"  sandwich sd {d['sd_A_sandwich']:.4f}" if "sd_A_sandwich" in d else ""
            log(f"  {k:8s} n {d['n']:5d}  A {d['A']:+.4f} +- {d['sd_A']:.4f}  dchi2(A=0) {d['D_A0']:8.3f}  dchi2(A=1) {d['D_A1']:8.3f}{extra}{sw}  -> {word}")
    res["D2"] = D2; res["U"] = U
    # reported rows
    rep = {}
    rep["D1_des_only"] = run("des_only", "R", "run", True); rep["D1_full"] = run("full", "R", "run", True)
    rep["D1_des_only_P"] = run("des_only", "P", "run", True)
    H = json.load(open(os.path.join(AGB2, "agb2_H_diag.json")))["fits"]["sample_drop_DES"]["H1"]
    a2, s2 = float(H["A"]), float(H["sd_A"])
    a1, s1 = rep["D1_des_only"]["A"], rep["D1_des_only"]["sd_A"]
    wsum = 1/s1**2 + 1/s2**2; ac = (a1/s1**2 + a2/s2**2)/wsum; sc = wsum**-0.5
    rep["D1_combined"] = dict(A=ac, sd_A=sc, D_A0=(ac/sc)**2, D_A1=((ac - 1)/sc)**2, agb2_drop_DES_H1=[a2, s2],
                              word_by_W1_rules=w1((ac/sc)**2, ((ac - 1)/sc)**2))
    rep["H2_des_only"] = run("des_only", "R", "mass", True); rep["H2_des_only_P"] = run("des_only", "P", "mass", True)
    rep["D2_shortdelay"] = run("des_only", "R", "sfr", True, dtd="W"); rep["D2_full_P"] = run("full", "P", "sfr", True)
    rep["U_full_P"] = run("full", "P", "sfr", False)
    log("reported:")
    for k, d in rep.items():
        log(f"  {k:16s} A {d['A']:+.4f} +- {d['sd_A']:.4f}  dchi2(A=0) {d['D_A0']:8.3f}  dchi2(A=1) {d['D_A1']:8.3f}"
            + (f"  (W1 rules: {d['word_by_W1_rules']}; AGB2 drop-DES H1 {a2:+.4f} +- {s2:.4f})" if k == "D1_combined" else f"  (W1 rules: {w1(d['D_A0'], d['D_A1'])})"))
    # band steps on full
    idx = sel(meta, "full"); z = meta.zHD[idx]; lm, ls, col = meta.lm[idx], meta.ls[idx], meta.col[idx]
    bands = [(0.0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 1.2)]
    age2 = M.mean_age(ls, z); agem = M.mass_age(lm, z)
    splits = dict(mass=(lm < 10.0), sfr=(ls >= -10.0), colour=(col <= 1.0))
    bs = {}
    for sp, young in splits.items():
        S = young.astype(float); bs[sp] = {}
        ex = [(f"g{j}", ((z >= lo) & (z < hi)).astype(float)*(S - 0.5)) for j, (lo, hi) in enumerate(bands)]
        for reading in ("R", "P"):
            f = fit(meta, idx, reading, 20, False, None, extra=ex)
            rows = []
            for j, (lo, hi) in enumerate(bands):
                inb = (z >= lo) & (z < hi)
                pred = SLOPE*(age2[inb & ~young].mean() - age2[inb & young].mean())
                predm = SLOPE*(agem[inb & ~young].mean() - agem[inb & young].mean())
                rows.append(dict(band=[lo, hi], n_young=int((inb & young).sum()), n_old=int((inb & ~young).sum()),
                                 step=f[f"g{j}"], sd=f[f"sd_g{j}"], pred_twocomp=float(pred), pred_massonly=float(predm)))
            bs[sp][reading] = rows
            log(f"  band steps, split {sp} (young side minus old side), reading {reading}:")
            for r in rows:
                log(f"     z {r['band'][0]:.1f}-{r['band'][1]:.1f}  n {r['n_young']:4d}/{r['n_old']:4d}  step {r['step']:+.4f} +- {r['sd']:.4f}"
                    f"   slope predicts {r['pred_twocomp']:+.4f} (two-component), {r['pred_massonly']:+.4f} (mass-only)")
    rep["band_steps"] = bs
    res["reported"] = rep


def main():
    t0 = time.time(); res = dict(mode=MODE, numpy=np.__version__); code = 0
    log(f"AGB3R mode {MODE}")
    if MODE == "KM":
        mode_KM(res)
    else:
        meta = DA.Meta()
        if MODE == "forecast": mode_forecast(res, meta)
        elif MODE == "K1": mode_K1(res, meta)
        elif MODE == "K3": code = mode_K3(res, meta)
        elif MODE == "K2K4": mode_K2K4(res, meta)
        elif MODE == "D": mode_D(res, meta)
        else: raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"agb3r_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb3r_{MODE}.json ({res['seconds']} s) exit {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
