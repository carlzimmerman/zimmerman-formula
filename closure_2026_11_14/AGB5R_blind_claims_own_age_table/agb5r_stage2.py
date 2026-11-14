"""AGB5R stage 2: AGB5's amendment 1 applied (bootstrap errors, amended K4). Written after stage 1 was committed.
Modes: K4B (amended K4), LB (L1 with bootstrap errors). Outputs agb5r_K4_boot.{json,out}, agb5r_L_boot.{json,out}.
Usage: python3 -I agb5r_stage2.py MODE"""
import os
import sys
import json
import time
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb5r_data as D  # noqa: E402
import agb5r_fit as F  # noqa: E402
from agb5r_run import stepsample, take, _clean  # noqa: E402

SEED_BOOT = 20261119   # amendment 1
SEED_SHUF = 20261118   # frozen K4 shuffle seed (the amendment names none for its shuffle)
NDRAW = 400
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


# ---- structural fit for bootstrap resamples: same likelihood, fewer starts, no Hessian ----
def structural_beta(s, step, hr, p_full):
    x, sx, y, sy = s["age"], s["sage"], s[hr], s["shr"]
    L = s["L"] if step else np.zeros_like(x)
    f = lambda p: F._nll(p, x, sx, y, sy, L, step)
    pl = F.plain(s, step, hr=hr)
    vx = max(np.var(x) - np.mean(sx ** 2), 0.25)
    if step:
        m0, m1 = np.mean(x[L < 0.5]), np.mean(x[L > 0.5])
        st = [list(p_full), [pl["alpha"], pl["beta"] * 1.6, pl["g"], m0, m1, np.sqrt(vx), 0.12],
              [pl["alpha"], pl["beta"], pl["g"], m0, m1, np.std(x), 0.12]]
    else:
        st = [list(p_full), [pl["alpha"], pl["beta"] * 1.6, np.mean(x), np.sqrt(vx), 0.12],
              [pl["alpha"], pl["beta"], np.mean(x), np.std(x), 0.12]]
    best = None
    for s0 in st:
        r = minimize(f, np.array(s0, float), method="BFGS", options={"gtol": 1e-8, "maxiter": 3000})
        r = minimize(f, r.x, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 20000, "maxfev": 40000})
        if best is None or r.fun < best.fun:
            best = r
    return float(best.x[1]), float(abs(best.x[-2]))


def boot_sd(s, fitA, seed=SEED_BOOT):
    rng = np.random.default_rng(seed)
    n = len(s["age"])
    vals = np.array([fitA(take(s, rng.integers(0, n, n))) for _ in range(NDRAW)])
    return vals


def mode_K4B():
    t1, t2 = D.tables()
    out = {}
    ok = True
    for nm, t in (("t1", t1), ("t2", t2)):
        s = stepsample(t)
        r0 = F.plain(s, True)
        sA = r0["sA"]
        bs = boot_sd(s, lambda ss: F.plain(ss, True)["A"])
        # shuffle with the fitted signal removed: HR - beta*age - g*(L-1/2), then (age, L) permuted together
        y0 = s["hr"] - r0["beta"] * s["age"] - r0["g"] * (s["L"] - 0.5)
        sig_rms = float(np.sqrt(np.mean((r0["beta"] * (s["age"] - s["age"].mean()) + r0["g"] * (s["L"] - s["L"].mean())) ** 2)))
        rng = np.random.default_rng(SEED_SHUF)
        n = len(s["age"])
        sh = []
        for _ in range(NDRAW):
            perm = rng.permutation(n)
            ss = dict(s); ss["age"] = s["age"][perm]; ss["L"] = s["L"][perm]
            sh.append(F.plain(ss, True, y=y0)["A"])
        sh = np.array(sh)
        r = dict(A=r0["A"], sA_stated=sA, boot_mean=float(bs.mean()), boot_sd=float(bs.std(ddof=1)),
                 boot_sd_over_sA=float(bs.std(ddof=1) / sA), signal_rms=sig_rms,
                 shuffle_removed_mean_over_sA=float(sh.mean() / sA), shuffle_removed_sd_over_sA=float(sh.std(ddof=1) / sA))
        r["pass_boot"] = bool(0.8 <= r["boot_sd_over_sA"] <= 1.25)
        r["pass_shuffle_removed"] = bool(0.8 <= r["shuffle_removed_sd_over_sA"] <= 1.25)
        r["info_shuffle_removed_mean_ok"] = bool(abs(r["shuffle_removed_mean_over_sA"]) <= 0.2)
        r["pass"] = r["pass_boot"] and r["pass_shuffle_removed"]
        ok &= r["pass"]
        out[nm] = r
        say("K4B %s A %+.4f stated sA %.4f | bootstrap (seed %d) sd %.4f = %.3f sA [%s] | signal rms %.3f mag; shuffle with signal removed sd %.3f sA [%s], mean %+.3f sA" % (
            nm, r["A"], sA, SEED_BOOT, r["boot_sd"], r["boot_sd_over_sA"], r["pass_boot"], sig_rms,
            r["shuffle_removed_sd_over_sA"], r["pass_shuffle_removed"], r["shuffle_removed_mean_over_sA"]))
    out["pass"] = bool(ok)
    say("K4B (amended K4)", "PASS" if ok else "FAIL")
    return out


def mode_LB():
    t1, t2 = D.tables()
    s1, s2 = stepsample(t1), stepsample(t2)
    shared = np.isin(s1["id"], t2["id"])
    s1d = D.subset(s1, ~shared)
    cfg = {  # name -> (sample, estimator, hr, zterm)
        "t1": (s1, "plain", "hr", False), "t2": (s2, "plain", "hr", False),
        "t1_dropped": (s1d, "plain", "hr", False), "t1_orig": (s1, "plain", "hr_orig", False),
        "t1_z": (s1, "plain", "hr", True), "t2_z": (s2, "plain", "hr", True),
        "t1_struct": (s1, "struct", "hr", False), "t2_struct": (s2, "struct", "hr", False),
    }
    fits = {}
    for nm, (s, est, hr, zt) in cfg.items():
        t0 = time.time()
        if est == "plain":
            full = F.plain(s, True, zterm=zt, hr=hr)
            vals = boot_sd(s, lambda ss: F.plain(ss, True, zterm=zt, hr=hr)["A"])
            nbad = 0
        else:
            full = F.structural(s, True, hr=hr)
            pf = [full[k] for k in ("alpha", "beta", "g", "mu0", "mu1", "tau", "sint")]
            taus = []

            def fa(ss):
                b, tau = structural_beta(ss, True, hr, pf)
                taus.append(tau)
                return b / F.S25
            vals = boot_sd(s, fa)
            nbad = int(np.sum(np.array(taus) < 0.05))
        sd = float(vals.std(ddof=1))
        q16, q50, q84 = np.percentile(vals, [16, 50, 84])
        fits[nm] = dict(A=full["A"], sA_stated=full["sA"], sA_boot=sd, boot_mean=float(vals.mean()),
                        boot_q16=float(q16), boot_q50=float(q50), boot_q84=float(q84), n=full["n"], tau_near_zero=nbad)
        say("LB fit %-11s n %3d A %+.4f stated sA %.4f bootstrap sd %.4f (ratio %.3f) mean %+.4f q16/50/84 %+.3f %+.3f %+.3f%s [%.0fs]" % (
            nm, full["n"], full["A"], full["sA"], sd, sd / full["sA"], vals.mean(), q16, q50, q84,
            ("  tau<0.05 in %d draws" % nbad) if est == "struct" else "", time.time() - t0))

    def row(parts):
        return F.combine([dict(A=fits[p]["A"], sA=fits[p]["sA_boot"]) for p in parts])
    rows = {"primary": row(["t1", "t2"]), "table1_alone": row(["t1"]), "table2_alone": row(["t2"]),
            "shared_dropped_t1": row(["t1_dropped", "t2"]), "t1_original_resid": row(["t1_orig", "t2"]),
            "redshift_term": row(["t1_z", "t2_z"]), "structural": row(["t1_struct", "t2_struct"])}
    out = {"fits": fits}
    order = ["primary", "table1_alone", "table2_alone", "shared_dropped_t1", "t1_original_resid", "redshift_term", "structural"]
    for k in order:
        c = rows[k]
        w, d0, d1 = F.w1_word(c["A"], c["sA"])
        out[k] = dict(A=c["A"], sA=c["sA"], dchi2_A0=d0, dchi2_A1=d1, word=w)
        say("LB %-18s A = %+.4f +- %.4f (bootstrap)  dchi2(A=0) %6.2f  dchi2(A=1) %6.2f  %s" % (k, c["A"], c["sA"], d0, d1, w))
    first = out["primary"]["word"]
    changed = [k for k in order[1:] if out[k]["word"] != first]
    out["first_word"] = first
    out["second_word"] = "ROBUST" if not changed else "FRAGILE (" + ", ".join(changed) + ")"
    say("LB reading (amendment 1):", first, "/", out["second_word"])
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    res = {"K4B": mode_K4B, "LB": mode_LB}[mode]()
    name = {"K4B": "agb5r_K4_boot", "LB": "agb5r_L_boot"}[mode]
    with open(os.path.join(HERE, name + ".json"), "w") as f:
        json.dump(_clean(res), f, indent=1, sort_keys=True)
    with open(os.path.join(HERE, name + ".out"), "w") as f:
        f.write("\n".join(LINES) + "\n")
