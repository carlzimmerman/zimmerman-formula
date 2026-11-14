"""AGB5 checks and fits (criteria: FROZEN_CRITERIA.md in this folder).

The published age slope on the claim's own tables (Chung et al. 2025), with a host-mass step allowed:
    HR_i = alpha + beta x age_i + g (L_i - 1/2),   A = beta / (-0.030 mag/Gyr).
Usage: python3 -I agb5_run.py MODE [outdir [boot]]
  "boot" (AMENDMENT_1.md): slope errors from 400 bootstrap resamples of the hosts; outputs agb5_<MODE>_boot.json.
  KA published slopes reproduced   K1 the tables   K3 twins (exit 3 pass, 4 fail)   K4 error bar   L the fits
Each mode writes agb5_<MODE>.json and prints its log (redirect to agb5_<MODE>.out)."""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import agb5_data as D
import agb5_eiv as E

MODE = sys.argv[1] if len(sys.argv) > 1 else "none"; OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
BOOT = len(sys.argv) > 3 and sys.argv[3] == "boot"; TAG = "_boot" if BOOT else ""; BSEED = 20261119
SLOPE = -0.030; SEED = 20261118


def plain(T, y=None, step=False, zterm=False, sel=None, sint=0.10, age=None, low=None):
    """Weighted line. Returns slope (mag/Gyr), its error, the step and its error."""
    y = T["hr"] if y is None else y; age = T["age"] if age is None else age
    low = (T["mass"] < 10) if low is None else low
    k = np.isfinite(y) & (np.ones(len(y), bool) if sel is None else sel)
    if step: k = k & np.isfinite(T["mass"])
    if zterm: k = k & (T["z"] > 0)
    w = 1/(T["s_hr"][k]**2 + sint**2); cols = [np.ones(k.sum()), age[k]] + ([low[k] - 0.5] if step else []) + ([T["z"][k]] if zterm else [])
    X = np.column_stack(cols); XW = X.T*w; cov = np.linalg.inv(XW@X); b = cov@(XW@y[k]); r = y[k] - X@b
    out = dict(n=int(k.sum()), beta=float(b[1]), sd_beta=float(np.sqrt(cov[1, 1])), chi2=float((w*r*r).sum()), dof=int(k.sum()) - len(b))
    if step: out.update(g=float(b[2]), sd_g=float(np.sqrt(cov[2, 2])))
    return out


def struct(T, y=None, step=False, sel=None, scale=1.0):
    y = T["hr"] if y is None else y; k = np.isfinite(y) & (np.ones(len(y), bool) if sel is None else sel)
    if step: k = k & np.isfinite(T["mass"])
    return E.fit(T["age"][k], T["s_age"][k], y[k], T["s_hr"][k], L=(T["mass"][k] < 10) if step else None, step=step, sx_scale=scale)


def sub(T, i):
    return {q: (v[i] if isinstance(v, np.ndarray) else v) for q, v in T.items()}


def booted(fn, T, n=400, **kw):
    """fn(T, **kw) with, under amendment 1, its slope error replaced by the bootstrap error over hosts."""
    r = fn(T, **kw)
    if BOOT:
        rng = np.random.default_rng(BSEED); N = len(T["age"]); kb = {k: v for k, v in kw.items() if k not in ("y", "sel")}
        b = []
        for _ in range(n):
            i = rng.integers(0, N, N); Tb = sub(T, i)
            b.append(fn(Tb, y=None if kw.get("y") is None else kw["y"][i], sel=None if kw.get("sel") is None else kw["sel"][i], **kb)["beta"])
        r["sd_beta_formula"] = r["sd_beta"]; r["sd_beta"] = float(np.std(b, ddof=1))
    return r


def amp(fits):
    """Inverse-variance mean of slopes, in units of the published slope."""
    w = np.array([1/f["sd_beta"]**2 for f in fits]); b = np.array([f["beta"] for f in fits])
    a = float((w*b).sum()/w.sum()/SLOPE); s = float(w.sum()**-0.5/abs(SLOPE))
    return dict(A=a, sd_A=s, D_A0=(a/s)**2, D_A1=((a - 1)/s)**2, slope=a*SLOPE, sd_slope=s*abs(SLOPE))


def main():
    t0 = time.time(); log = lambda s: print(s, flush=True); res = dict(mode=MODE); code = 0
    T1, T2 = D.table(1), D.table(2); shared = np.isin(T1["id"], T2["id"])
    log(f"AGB5 mode {MODE}; table 1: {len(T1['age'])} hosts ({int(np.isfinite(T1['mass']).sum())} with a mass); table 2: {len(T2['age'])} ({int(np.isfinite(T2['mass']).sum())}); shared {int(shared.sum())}")
    if MODE == "K1":
        ok = len(T1["age"]) == 199 and len(T2["age"]) == 102 and int(shared.sum()) == 33 and bool(np.any(np.abs(T1["hr"] - T1["hr_orig"]) > 1e-3))
        res.update(n1=len(T1["age"]), n2=len(T2["age"]), shared=int(shared.sum()), max_correction=float(np.nanmax(np.abs(T1["hr"] - T1["hr_orig"]))), passed=bool(ok))
        log(f"K1: rows {len(T1['age'])} and {len(T2['age'])}; shared {int(shared.sum())}; every id found in the SDSS-II table; largest redshift correction in table 1 {res['max_correction']:.3f} mag -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "KA":
        p2, p1 = plain(T2), plain(T1); c = amp([p1, p2]); s2, s1, s1o = struct(T2), struct(T1), struct(T1, y=T1["hr_orig"])
        ok = (abs(p2["beta"] + 0.038) <= 0.004 and abs(p1["beta"] + 0.025) <= 0.004 and abs(c["slope"] + 0.030) <= 0.004
              and abs(s2["beta"] + 0.062) <= 0.004 and abs(s1["beta"] + 0.047) <= 0.004 and abs(s1o["beta"] + 0.037) <= 0.004)
        res.update(plain_t2=p2, plain_t1=p1, combined=c, struct_t2=s2, struct_t1=s1, struct_t1_orig=s1o, passed=bool(ok))
        log(f"KA plain line, no step: table 2 {p2['beta']:+.4f} +- {p2['sd_beta']:.4f} (published -0.038 +- 0.007); table 1 {p1['beta']:+.4f} +- {p1['sd_beta']:.4f} (-0.025 +- 0.006);"
            f" combined {c['slope']:+.4f} +- {c['sd_slope']:.4f} (-0.030), A {c['A']:+.3f} +- {c['sd_A']:.3f}")
        log(f"KA structural fit, no step: table 2 {s2['beta']:+.4f} +- {s2['sd_beta']:.4f} (-0.062 +- 0.014); table 1 {s1['beta']:+.4f} +- {s1['sd_beta']:.4f} (-0.047 +- 0.015);"
            f" table 1 original residuals {s1o['beta']:+.4f} +- {s1o['sd_beta']:.4f} (-0.037 +- 0.015) -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K3":
        ok = True; res["twins"] = []
        for nm, T in (("table 1", T1), ("table 2", T2)):
            k = np.isfinite(T["mass"])
            for a_true in (1.0, 0.0):
                y = np.where(k, 0.1 + 0.05*((T["mass"] < 10) - 0.5) + a_true*SLOPE*T["age"], np.nan); r = plain(T, y=y, step=True)
                good = abs(r["beta"]/SLOPE - a_true) <= 1e-6; ok = ok and good; res["twins"].append(dict(table=nm, A_true=a_true, A=r["beta"]/SLOPE, passed=bool(good)))
                log(f"K3 twin {nm} A_true {a_true}: A {r['beta']/SLOPE:+.9f}  g {r['g']:+.9f} -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(ok); code = 3 if ok else 4
    elif MODE == "K4":
        rng = np.random.default_rng(SEED); ok = True
        for nm, T in (("table1", T1), ("table2", T2)):
            k = np.where(np.isfinite(T["mass"]))[0]; real = plain(T, step=True); s = real["sd_beta"]; sh, bs = [], []
            for _ in range(400):
                p = rng.permutation(k); age = T["age"].copy(); low = (T["mass"] < 10).copy(); age[k] = T["age"][p]; low[k] = (T["mass"] < 10)[p]
                sh.append(plain(T, step=True, age=age, low=low)["beta"])
                i = rng.choice(k, len(k)); Tb = {q: (v[i] if isinstance(v, np.ndarray) else v) for q, v in T.items()}; bs.append(plain(Tb, step=True)["beta"])
            sh, bs = np.array(sh), np.array(bs); good = abs(sh.mean()) <= 0.2*s and 0.8 <= sh.std(ddof=1)/s <= 1.25 and 0.8 <= bs.std(ddof=1)/s <= 1.25; ok = ok and good
            if BOOT:                                               # AMENDMENT_1.md: shuffle with the fitted signal taken out; bootstrap ratio
                lw = T["mass"] < 10; yres = T["hr"] - real["beta"]*T["age"] - real["g"]*(lw - 0.5); sr = []
                for _ in range(400):
                    p = rng.permutation(k); age = T["age"].copy(); low = lw.copy(); age[k] = T["age"][p]; low[k] = lw[p]
                    sr.append(plain(T, y=yres, step=True, age=age, low=low)["beta"])
                sr = np.array(sr); good = 0.8 <= bs.std(ddof=1)/s <= 1.25 and 0.8 <= sr.std(ddof=1)/s <= 1.25; ok = (ok or True) and good
                res[nm] = dict(bootstrap_over_sigma=float(bs.std(ddof=1)/s), shuffle_no_signal_over_sigma=float(sr.std(ddof=1)/s), passed=bool(good))
                log(f"K4 amended {nm}: bootstrap / sigma {bs.std(ddof=1)/s:.3f}; shuffle with the fitted signal removed / sigma {sr.std(ddof=1)/s:.3f} (both allowed 0.8-1.25) -> {'PASS' if good else 'FAIL'}")
                continue
            res[nm] = dict(mean_over_sigma=float(sh.mean()/s), shuffle_over_sigma=float(sh.std(ddof=1)/s), bootstrap_over_sigma=float(bs.std(ddof=1)/s), passed=bool(good))
            log(f"K4 {nm}: shuffle mean {sh.mean()/s:+.3f} sigma (allowed 0.2); shuffle scatter / sigma {sh.std(ddof=1)/s:.3f}; bootstrap / sigma {bs.std(ddof=1)/s:.3f} (both allowed 0.8-1.25) -> {'PASS' if good else 'FAIL'}")
        res["passed"] = bool(all(res[t]["passed"] for t in ("table1", "table2")))
    elif MODE == "L":
        F = {}
        f1, f2 = booted(plain, T1, step=True), booted(plain, T2, step=True)
        F["primary"] = dict(amp([f1, f2]), table1=f1, table2=f2)
        F["table1_alone"] = dict(amp([f1]), table1=f1); F["table2_alone"] = dict(amp([f2]), table2=f2)
        fd = booted(plain, T1, step=True, sel=~shared); F["shared_dropped"] = dict(amp([fd, f2]), table1=fd)
        fo = booted(plain, T1, y=T1["hr_orig"], step=True); F["original_residuals"] = dict(amp([fo, f2]), table1=fo)
        z1, z2 = booted(plain, T1, step=True, zterm=True), booted(plain, T2, step=True, zterm=True); F["redshift_term"] = dict(amp([z1, z2]), table1=z1, table2=z2)
        s1, s2 = booted(struct, T1, n=200, step=True), booted(struct, T2, n=200, step=True); F["structural"] = dict(amp([s1, s2]), table1=s1, table2=s2)
        n1, n2 = booted(plain, T1), booted(plain, T2); F_nostep = dict(amp([n1, n2]), table1=n1, table2=n2); res["no_step"] = F_nostep
        log(f"no step (the published configuration): A {F_nostep['A']:+.3f} +- {F_nostep['sd_A']:.3f}")
        for k, v in F.items():
            log(f"L1 {k:20s} A {v['A']:+.3f} +- {v['sd_A']:.3f}  dchi2(A=0) {v['D_A0']:6.2f}  dchi2(A=1) {v['D_A1']:6.2f}   slope {v['slope']:+.4f} +- {v['sd_slope']:.4f} mag/Gyr   "
                + "  ".join(f"{t}: {v[t]['beta']:+.4f} +- {v[t]['sd_beta']:.4f}, g {v[t]['g']:+.3f} +- {v[t]['sd_g']:.3f}, n {v[t]['n']}" for t in ("table1", "table2") if t in v))
        R = {}
        log("reported only:")
        for nm, T in (("table1", T1), ("table2", T2)):
            a0 = plain(T); k = np.isfinite(T["mass"]); lowm = T["mass"] < 10
            X = np.column_stack([np.ones(k.sum()), lowm[k] - 0.5]); w = 1/(T["s_hr"][k]**2 + 0.01); cov = np.linalg.inv((X.T*w)@X); b = cov@((X.T*w)@T["hr"][k])
            lo, hi = plain(T, sel=k & lowm), plain(T, sel=k & ~lowm)
            R[nm] = dict(no_step=a0, step_only=[float(b[1]), float(np.sqrt(cov[1, 1]))], slope_low_mass=lo, slope_high_mass=hi,
                         struct_half_errors=struct(T, step=True, scale=0.5), struct_no_age_errors=struct(T, step=True, scale=1e-3),
                         struct_no_step_half=struct(T, scale=0.5))
            log(f"   {nm}: slope with no step {a0['beta']:+.4f} +- {a0['sd_beta']:.4f}; step alone (no age term) {b[1]:+.3f} +- {np.sqrt(cov[1, 1]):.3f} mag;"
                f" slope inside low-mass hosts {lo['beta']:+.4f} +- {lo['sd_beta']:.4f} (n {lo['n']}), inside the others {hi['beta']:+.4f} +- {hi['sd_beta']:.4f} (n {hi['n']})")
            log(f"   {nm}: structural fit with a step, stated age errors x 0.5: {R[nm]['struct_half_errors']['beta']:+.4f} +- {R[nm]['struct_half_errors']['sd_beta']:.4f};"
                f" with no age errors: {R[nm]['struct_no_age_errors']['beta']:+.4f} +- {R[nm]['struct_no_age_errors']['sd_beta']:.4f}")
        # these ages on Pantheon+ magnitudes (AGB4's fit)
        sys.path.insert(0, os.path.join(D.REPO, "closure_2026_11_14", "AGB4_measured_host_ages")); sys.argv = ["agb4_run.py", "none"]
        import agb4_run as R4
        P = R4.sample("pp"); p = D.D4.pantheon_sdss(); keep = np.isfinite(p["sako_age_Ravi"]) & (p["sako_age_lo_Ravi"] > 0); cid = p["cid"][keep]
        a1 = dict(zip(T1["id"], T1["age"])); a2 = dict(zip(T2["id"], T2["age"])); age = np.array([a1.get(c, a2.get(c, np.nan)) for c in cid])
        for k, gf in (("M0", False), ("M1", True)):
            r = R4.fit(P, age, gf); R[f"pantheon_{k}"] = r; log(f"   these ages on Pantheon+ magnitudes, {k}: " + R4.fmt(r))
        res["fits"] = F; res["reported"] = R
    else:
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, f"agb5_{MODE}{TAG}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb5_{MODE}{TAG}.json  ({res['seconds']} s)  exit {code}"); sys.exit(code)


if __name__ == "__main__":
    main()
