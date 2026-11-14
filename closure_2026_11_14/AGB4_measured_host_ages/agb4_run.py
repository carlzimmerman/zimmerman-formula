"""AGB4 checks and fits (criteria: FROZEN_CRITERIA.md in this folder).

The published age slope, 0.030 mag/Gyr, tested on published host ages of SDSS-II supernova hosts. Weighted least
squares inside redshift bins:
    y_i = sum_b o_b [z_i in bin b] + g (L_i - 1/2) + A x D_i + a x1_i + b c_i,    D_i = -0.030 x (host age of i, Gyr)
A = 1 is the published slope. M0: no mass step (g = 0). M1: mass step free.

Usage: python3 -I agb4_run.py MODE [outdir]
  K1 the match   K2 ages against stretch   K3 twins (exit 3 pass, 4 fail)   K4 error bar   KR Rose et al.'s result
  M  the fits, their forks and the reported rows
Each mode writes agb4_<MODE>.json and prints its log (redirect to agb4_<MODE>.out)."""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import agb4_data as D

MODE = sys.argv[1] if len(sys.argv) > 1 else "none"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
SEED = 20261117; SLOPE = 0.030


def mu_fid(z, zh, om=0.334):
    zg = np.expm1(np.linspace(0, np.log(2.0), 20001)); e = np.sqrt(om*(1 + zg)**3 + 1 - om)
    dm = np.concatenate([[0.0], np.cumsum(0.5*(1/e[1:] + 1/e[:-1])*np.diff(zg))])
    return 5*np.log10((1 + zh)*np.interp(z, zg, dm))


def bins_of(z, nb):
    e = np.quantile(z, np.linspace(0, 1, nb + 1))
    return np.clip(np.searchsorted(e, z, side="right") - 1, 0, nb - 1)


def wls(cols, y, w):
    X = np.column_stack(cols); XW = X.T*w; cov = np.linalg.inv(XW@X); beta = cov@(XW@y); r = y - X@beta
    M = XW*r[None, :]; return beta, cov, cov@(M@M.T)@cov, float((w*r*r).sum())


def sample(name):
    """Arrays for one sample: z, y (reading R), yP (reading P or None), x1, c, w, low, ages, age interval half-width."""
    if name == "big":
        S = D.sako()
        s = (np.isin(S["type"], ["SNIa", "zSNIa"]) & np.isfinite(S["age_Ravi"]) & (S["age_lo_Ravi"] > 0) & np.isfinite(S["x0"]) & (S["x0"] > 0)
             & np.isfinite(S["x1"]) & np.isfinite(S["c"]) & (S["z"] > 0.03) & (S["z"] < 0.45) & (np.abs(S["x1"]) < 3) & (np.abs(S["c"]) < 0.3) & np.isfinite(S["muerr"]))
        z = S["z"][s]
        return dict(name=name, z=z, y=-2.5*np.log10(S["x0"][s]) - mu_fid(z, z), yP=None, x1=S["x1"][s], c=S["c"][s], w=1/(S["muerr"][s]**2 + 0.01),
                    low=S["logMass_Ravi"][s] < 10, mass=S["logMass_Ravi"][s], age=S["age_Ravi"][s], half=(S["age_hi_Ravi"][s] - S["age_lo_Ravi"][s])/2,
                    age_mat=S["age_Mat"][s], spec=S["type"][s] == "SNIa", nb=16)
    p = D.pantheon_sdss(); s = np.isfinite(p["sako_age_Ravi"]) & (p["sako_age_lo_Ravi"] > 0)
    out = dict(name="pp", z=p["z"][s], y=p["mB"][s] - mu_fid(p["z"][s], p["zh"][s]), yP=p["mcorr"][s] - mu_fid(p["z"][s], p["zh"][s]), x1=p["x1"][s], c=p["c"][s],
               w=1/p["var"][s], low=p["lm"][s] < 10, mass=p["lm"][s], age=p["sako_age_Ravi"][s], half=(p["sako_age_hi_Ravi"][s] - p["sako_age_lo_Ravi"][s])/2,
               age_mat=p["sako_age_Mat"][s], rose_local=p["rose_local"][s], rose_global=p["rose_global"][s], sako_z=p["sako_z"][s],
               sako_mass=p["sako_logMass_Ravi"][s], nb=8, n_all=len(p["z"]), n_matched=int(p["matched"].sum()))
    return out


def fit(S, age, gfree, reading="R", nb=None, sel=None, y=None, split=None):
    """One fit. sel: boolean sub-selection; split: break age (two amplitudes, below and above)."""
    sel = np.ones(len(S["z"]), bool) if sel is None else sel
    sel = sel & np.isfinite(age); nb = S["nb"] if nb is None else nb
    z = S["z"][sel]; n = int(sel.sum()); b = bins_of(z, nb); B = np.zeros((n, nb)); B[np.arange(n), b] = 1.0; w = S["w"][sel]; a = age[sel]
    yv = (S["y"] if reading == "R" else S["yP"])[sel] if y is None else y
    cols = [B] + ([S["x1"][sel], S["c"][sel]] if reading == "R" else []) + ([S["low"][sel] - 0.5] if gfree else [])
    if split is None:
        beta, cov, sand, chi2 = wls(cols + [-SLOPE*a], yv, w); A, sA, sw = beta[-1], np.sqrt(cov[-1, -1]), np.sqrt(sand[-1, -1])
        out = dict(n=n, n_low=int(S["low"][sel].sum()), reading=reading, nbins=nb, A=float(A), sd_A=float(sA), sandwich_sd_A=float(sw), chi2=chi2,
                   dof=n - len(beta), D_A0=float((A/sA)**2), D_A1=float(((A - 1)/sA)**2))
        if gfree: out.update(g=float(beta[-2]), sd_g=float(np.sqrt(cov[-2, -2])))
        return out
    beta, cov, sand, chi2 = wls(cols + [-SLOPE*np.minimum(a, split), -SLOPE*np.maximum(a - split, 0.0)], yv, w)
    return dict(n=n, n_above=int((a > split).sum()), A_below=float(beta[-2]), sd_below=float(np.sqrt(sand[-2, -2])), A_above=float(beta[-1]), sd_above=float(np.sqrt(sand[-1, -1])))


def fmt(r):
    return (f"A {r['A']:+.3f} +- {r['sd_A']:.3f} (sandwich {r['sandwich_sd_A']:.3f})  dchi2(A=0) {r['D_A0']:.2f}  dchi2(A=1) {r['D_A1']:.2f}"
            + (f"  g {r['g']:+.4f} +- {r['sd_g']:.4f}" if "g" in r else "") + f"  chi2 {r['chi2']:.1f}/{r['dof']}  n {r['n']} ({r['n_low']} low-mass)")


def main():
    t0 = time.time(); log = lambda s: print(s, flush=True); res = dict(mode=MODE); code = 0
    log(f"AGB4 mode {MODE}")
    P = sample("pp")
    log(f"sample pp: {len(P['z'])} supernovae with an FSPS host age (of {P['n_all']} Pantheon+ SDSS rows, {P['n_matched']} matched by id); z {P['z'].min():.3f}-{P['z'].max():.3f}")
    if MODE == "K1":
        dz = float(np.abs(P["z"] - P["sako_z"]).max()); cm = float(np.corrcoef(P["mass"], P["sako_mass"])[0, 1])
        ok = P["n_matched"] == P["n_all"] == 321 and dz <= 0.03 and cm >= 0.80
        res.update(n_matched=P["n_matched"], n_pp=len(P["z"]), max_dz=dz, corr_mass=cm, passed=bool(ok))
        log(f"K1: {P['n_matched']} of {P['n_all']} matched; largest |zHD - table z| {dz:.4f} (<= 0.03); mass correlation {cm:.3f} (>= 0.80) -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2":
        lo = P["x1"] < -1; old = P["age"] >= 6; d = float(lo[old].mean() - lo[~old].mean()); ok = d >= 0.15
        rows = [dict(age=[a, b], n=int(((P["age"] >= a) & (P["age"] < b)).sum()), share=float(lo[(P["age"] >= a) & (P["age"] < b)].mean())) for a, b in ((0, 4), (4, 6), (6, 8), (8, 14))]
        res.update(share_old=float(lo[old].mean()), share_young=float(lo[~old].mean()), diff=d, rows=rows, corr_age_x1=float(np.corrcoef(P["age"], P["x1"])[0, 1]), passed=bool(ok))
        for r in rows: log(f"   age {r['age'][0]}-{r['age'][1]} Gyr: n {r['n']:3d}  low-stretch share {r['share']:.3f}")
        log(f"K2: low-stretch share {lo[old].mean():.3f} at 6 Gyr and above, {lo[~old].mean():.3f} below; difference {d:.3f} (>= 0.15) -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K3":
        ok = True; res["twins"] = []
        for S in (P, sample("big")):
            b = bins_of(S["z"], S["nb"]); truth = 0.1*np.sin(np.arange(float(S["nb"])))[b] - 0.15*S["x1"] + 3.1*S["c"]
            for gf in (False, True):
                for a_true in (1.0, 0.0):
                    r = fit(S, S["age"], gf, y=truth + (0.05*(S["low"] - 0.5) if gf else 0.0) + a_true*(-SLOPE*S["age"]))
                    good = abs(r["A"] - a_true) <= 1e-6 and r["chi2"] <= 1e-8; ok = ok and good
                    res["twins"].append(dict(sample=S["name"], step_free=gf, A_true=a_true, A=r["A"], chi2=r["chi2"], passed=bool(good)))
                    log(f"K3 twin {S['name']:3s} {'M1' if gf else 'M0'} A_true {a_true}: A {r['A']:+.9f}  chi2_min {r['chi2']:.2e} -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok); code = 3 if ok else 4
    elif MODE == "K4":
        b = bins_of(P["z"], P["nb"]); rng = np.random.default_rng(SEED); ok = True
        real = {k: fit(P, P["age"], gf) for k, gf in (("M0", False), ("M1", True))}; draws = {"M0": [], "M1": []}
        for _ in range(400):
            p = np.arange(len(b))
            for k in range(P["nb"]):
                i = np.where(b == k)[0]; p[i] = rng.permutation(i)
            Q = dict(P); Q["low"] = P["low"][p]
            for k, gf in (("M0", False), ("M1", True)): draws[k].append(fit(Q, P["age"][p], gf)["A"])
        for k in ("M0", "M1"):
            a = np.array(draws[k]); s = real[k]["sd_A"]; sw = real[k]["sandwich_sd_A"]/s
            good = abs(a.mean()) <= 0.2*s and 0.8 <= a.std(ddof=1)/s <= 1.25 and 0.8 <= sw <= 1.25; ok = ok and good
            res[k] = dict(mean_over_sigma=float(a.mean()/s), sd_over_sigma=float(a.std(ddof=1)/s), sandwich_over_sigma=float(sw), passed=bool(good))
            log(f"K4 {k}: mean {a.mean()/s:+.3f} sigma (allowed 0.2); shuffle scatter / sigma_A {a.std(ddof=1)/s:.3f}; sandwich / sigma_A {sw:.3f} (both allowed 0.8-1.25) -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok)
    elif MODE == "KR":
        t = np.genfromtxt(os.path.join(D.ROSE, "campbell_local.tsv"), delimiter="\t", names=True, dtype=None, encoding=None)
        ages = {str(int(r[0])): r[1] for r in np.genfromtxt(os.path.join(D.ROSE, "results-summary.csv"), delimiter=",", skip_header=1)}
        ids = [str(int(v)) for v in t["SNID"]]; z = t["redshift"].astype(float); mu = t["mu"].astype(float); em = t["err_mu"].astype(float)
        a = np.array([ages.get(i, np.nan) for i in ids]); k = np.isfinite(a) & np.isfinite(mu)
        hr = mu[k] - mu_fid(z[k], z[k], 0.3); w = 1/em[k]**2; hr = hr - np.average(hr, weights=w); y, o = a[k] < 8, a[k] >= 8
        step = float(np.average(hr[y], weights=w[y]) - np.average(hr[o], weights=w[o])); un = float(hr[y].mean() - hr[o].mean())
        ok = abs(step - 0.114) <= 0.04
        res.update(n=int(k.sum()), n_old=int(o.sum()), step_weighted=step, step_unweighted=un, target=0.114, tol=0.04, passed=bool(ok))
        log(f"KR: {int(k.sum())} hosts ({int(o.sum())} older than 8 Gyr by local age): young minus old Hubble residual {step:+.4f} mag weighted ({un:+.4f} unweighted);"
            f" Rose et al. 0.114 +- 0.039; tolerance 0.04 -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "M":
        F = {}; B = sample("big"); narrow = P["half"] <= 2.5
        log(f"sample big: {len(B['z'])} ({int(B['spec'].sum())} spectroscopic); pp with age interval within +-2.5 Gyr: {int(narrow.sum())}")
        for k, gf in (("M0", False), ("M1", True)):
            F[k] = dict(primary=fit(P, P["age"], gf), reading_P=fit(P, P["age"], gf, "P"), bins12=fit(P, P["age"], gf, nb=12), big=fit(B, B["age"], gf),
                        narrow=fit(P, P["age"], gf, sel=narrow))
            log(f"{k} ({'mass step free' if gf else 'no mass step'}):")
            for name, r in F[k].items(): log(f"   {name:10s} " + fmt(r))
        log("reported only:")
        R = {}
        for name, age, nb in (("rose_global", P["rose_global"], 4), ("rose_local", P["rose_local"], 4), ("pegase", P["age_mat"], 8)):
            for k, gf in (("M0", False), ("M1", True)):
                R[f"{name}_{k}"] = fit(P, age, gf, nb=nb); log(f"   {name:12s} {k}: " + fmt(R[f"{name}_{k}"]))
        for k, gf in (("M0", False), ("M1", True)):
            R[f"big_spec_{k}"] = fit(B, B["age"], gf, sel=B["spec"]); log(f"   big, spectroscopic only {k}: " + fmt(R[f"big_spec_{k}"]))
        for S, lab in ((P, "pp"), (B, "big")):
            for k, gf in (("M0", False), ("M1", True)):
                r = fit(S, S["age"], gf, split=6.0); R[f"split6_{lab}_{k}"] = r
                log(f"   split at 6 Gyr, {lab} {k}: below {r['A_below']:+.3f} +- {r['sd_below']:.3f}; above {r['A_above']:+.3f} +- {r['sd_above']:.3f} ({r['n_above']} hosts above)")
        # reliability of the FSPS age from stretch and host mass as witnesses (AGB3's post hoc method), pp
        def rel(idx):
            w = P["w"][idx]; b = bins_of(P["z"][idx], P["nb"]); Bm = np.zeros((len(idx), P["nb"])); Bm[np.arange(len(idx)), b] = 1.0
            rs = lambda v, cols: v - np.column_stack(cols)@np.linalg.solve((np.column_stack(cols).T*w)@np.column_stack(cols), (np.column_stack(cols).T*w)@v)
            cv = lambda a, c: float((w*a*c).sum()/w.sum())
            W, Z1, Z2 = (rs(v[idx], [Bm]) for v in (P["age"], P["x1"], P["mass"])); vx = cv(W, Z1)*cv(W, Z2)/cv(Z1, Z2); vu = cv(W, W) - vx
            out = [vx/cv(W, W)]
            for cols in ([Bm, P["x1"][idx], P["c"][idx]], [Bm, P["x1"][idx], P["c"][idx], P["low"][idx] - 0.5]):
                Wr = rs(P["age"][idx], cols); out.append(1 - vu/cv(Wr, Wr))
            return out
        n = len(P["z"]); r0 = rel(np.arange(n)); rng = np.random.default_rng(SEED + 1); bs = np.array([rel(rng.integers(0, n, n)) for _ in range(300)])
        R["reliability"] = dict(unconditional=[r0[0], float(bs[:, 0].std(ddof=1))], inside_M0=[r0[1], float(bs[:, 1].std(ddof=1))], inside_M1=[r0[2], float(bs[:, 2].std(ddof=1))],
                                M0_corrected=F["M0"]["primary"]["A"]/r0[1], M1_corrected=F["M1"]["primary"]["A"]/r0[2])
        log(f"   reliability of the FSPS age (stretch and mass as witnesses): {r0[0]:.3f} +- {bs[:, 0].std(ddof=1):.3f}; inside M0 {r0[1]:.3f} +- {bs[:, 1].std(ddof=1):.3f}, inside M1 {r0[2]:.3f} +- {bs[:, 2].std(ddof=1):.3f};"
            f" amplitudes divided by it: M0 {R['reliability']['M0_corrected']:+.3f}, M1 {R['reliability']['M1_corrected']:+.3f}")
        res["fits"] = F; res["reported"] = {k: v for k, v in R.items() if v is not None}
    else:
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, f"agb4_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb4_{MODE}.json  ({res['seconds']} s)  exit {code}"); sys.exit(code)


if __name__ == "__main__":
    main()
