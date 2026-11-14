"""AGB5R run modes: K1, KA, K3, K4, L1, REP, PP. One mode per process: agb5r_<MODE>.json and .out.
Usage: python3 -I agb5r_run.py MODE"""
import os
import sys
import json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb5r_data as D  # noqa: E402
import agb5r_fit as F  # noqa: E402

SEED = 20261118
NDRAW = 400
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


def stepsample(t):
    return D.subset(t, np.isfinite(t["L"]))


def get():
    t1, t2 = D.tables()
    return t1, t2


def fmtA(r):
    return "A = %+.4f +- %.4f (beta %+.5f +- %.5f mag/Gyr)" % (r["A"], r["sA"], r["A"] * F.S25, r["sA"] * abs(F.S25))


def mode_K1():
    t1, t2 = get()
    s1, s2 = set(t1["id"].tolist()), set(t2["id"].tolist())
    ndiff = int(np.sum(t1["hr"] != t1["hr_orig"]))
    rms = float(np.sqrt(np.mean((t1["hr"] - t1["hr_orig"]) ** 2)))
    res = dict(n1=len(t1["id"]), n2=len(t2["id"]), shared=len(s1 & s2), union=len(s1 | s2),
               all_in_sako=bool(t1["in_sako"].all() and t2["in_sako"].all()),
               t1_resid_rows_differ=ndiff, t1_resid_rms_diff=rms,
               mass1=int(np.isfinite(t1["L"]).sum()), mass2=int(np.isfinite(t2["L"]).sum()),
               lowmass_share1=float(np.nanmean(t1["L"])), lowmass_share2=float(np.nanmean(t2["L"])))
    res["pass"] = bool(res["n1"] == 199 and res["n2"] == 102 and res["shared"] == 33 and res["all_in_sako"] and ndiff > 0)
    for k, v in res.items():
        say("K1", k, v)
    # descriptive (no residual): age vs low-mass flag
    for nm, t in (("t1", t1), ("t2", t2)):
        s = stepsample(t)
        say("K1 desc", nm, "mean age L=1 %.2f L=0 %.2f corr(age,L) %+.3f mean sig_age^2 %.2f var(age) %.2f" % (
            s["age"][s["L"] > 0.5].mean(), s["age"][s["L"] < 0.5].mean(), np.corrcoef(s["age"], s["L"])[0, 1],
            np.mean(t["sage"] ** 2), np.var(t["age"])))
    return res


def mode_KA():
    t1, t2 = get()
    out = {}
    p1 = F.plain(t1, False)
    p2 = F.plain(t2, False)
    c = F.combine([p1, p2])
    out["plain_t1"] = p1; out["plain_t2"] = p2; out["plain_comb"] = c
    out["struct_t2"] = F.structural(t2, False)
    out["struct_t1"] = F.structural(t1, False)
    out["struct_t1orig"] = F.structural(t1, False, hr="hr_orig")
    out["plain_t1orig"] = F.plain(t1, False, hr="hr_orig")
    tests = [("plain_t2", out["plain_t2"]["beta"], -0.038), ("plain_t1", out["plain_t1"]["beta"], -0.025),
             ("plain_comb", c["beta"], -0.030), ("struct_t2", out["struct_t2"]["beta"], -0.062),
             ("struct_t1", out["struct_t1"]["beta"], -0.047), ("struct_t1orig", out["struct_t1orig"]["beta"], -0.037)]
    ok = True
    for nm, b, tgt in tests:
        p = abs(b - tgt) <= 0.004
        ok &= p
        say("KA %-14s beta %+.5f target %+.3f diff %+.5f %s" % (nm, b, tgt, b - tgt, "PASS" if p else "FAIL"))
    for nm in ("struct_t2", "struct_t1", "struct_t1orig"):
        r = out[nm]
        say("KA %-14s s_beta %.5f (h-check %.5f) tau %.3f sint %.4f n %d" % (nm, r["s_beta"], r["s_beta_hcheck"], r["tau"], r["sint"], r["n"]))
    say("KA L0 combined (plain, no step):", fmtA(c))
    out["pass"] = bool(ok)
    say("KA", "PASS" if ok else "FAIL")
    return out


def mode_K3():
    t1, t2 = get()
    out = {}
    ok = True
    for nm, t in (("t1", t1), ("t2", t2)):
        s = stepsample(t)
        for At in (1.0, 0.0):
            y = 0.1 + 0.05 * (s["L"] - 0.5) + At * (F.S25 * s["age"])
            r = F.plain(s, True, y=y)
            p = abs(r["A"] - At) <= 1e-6
            ok &= p
            out["%s_A%d" % (nm, At)] = dict(A=r["A"], g=r["g"], alpha=r["alpha"], chi2=r["chi2"], pass_=bool(p))
            say("K3 %s A_true %.0f: A_hat %.10f g %.10f alpha %.10f chi2 %.2e %s" % (nm, At, r["A"], r["g"], r["alpha"], r["chi2"], "PASS" if p else "FAIL"))
    out["pass"] = bool(ok)
    say("K3", "PASS" if ok else "FAIL")
    return out


def take(s, idx):
    n = len(s["age"])
    return {k: (v[idx] if isinstance(v, np.ndarray) and v.shape[:1] == (n,) else v) for k, v in s.items()}


def k4_table(s):
    r0 = F.plain(s, True)
    sA = r0["sA"]
    n = len(s["age"])
    rng = np.random.default_rng(SEED)
    sh = []
    for _ in range(NDRAW):
        perm = rng.permutation(n)
        ss = dict(s)
        ss["age"] = s["age"][perm]
        ss["L"] = s["L"][perm]
        sh.append(F.plain(ss, True)["A"])
    sh = np.array(sh)
    rng = np.random.default_rng(SEED)
    bs = []
    for _ in range(NDRAW):
        idx = rng.integers(0, n, n)
        bs.append(F.plain(take(s, idx), True)["A"])
    bs = np.array(bs)
    res = dict(A=r0["A"], sA=sA, sA_scaled=r0["sA_scaled"], chi2=r0["chi2"], dof=r0["dof"],
               shuffle_mean=float(sh.mean()), shuffle_sd=float(sh.std(ddof=1)),
               boot_mean=float(bs.mean()), boot_sd=float(bs.std(ddof=1)))
    res["shuffle_mean_over_sA"] = res["shuffle_mean"] / sA
    res["shuffle_sd_over_sA"] = res["shuffle_sd"] / sA
    res["boot_sd_over_sA"] = res["boot_sd"] / sA
    res["pass_shuffle_mean"] = bool(abs(res["shuffle_mean"]) <= 0.2 * sA)
    res["pass_shuffle_sd"] = bool(0.8 <= res["shuffle_sd_over_sA"] <= 1.25)
    res["pass_boot"] = bool(0.8 <= res["boot_sd_over_sA"] <= 1.25)
    res["pass"] = res["pass_shuffle_mean"] and res["pass_shuffle_sd"] and res["pass_boot"]
    return res


def mode_K4():
    t1, t2 = get()
    out = {}
    ok = True
    for nm, t in (("t1", t1), ("t2", t2)):
        r = k4_table(stepsample(t))
        out[nm] = r
        ok &= r["pass"]
        say("K4 %s A %+.4f sA %.4f (chi2/dof %.1f/%d, scaled sA %.4f)" % (nm, r["A"], r["sA"], r["chi2"], r["dof"], r["sA_scaled"]))
        say("K4 %s shuffle mean %+.4f (= %+.3f sA, |.|<=0.2 %s); shuffle sd %.4f (= %.3f sA, in [0.8,1.25] %s)" % (
            nm, r["shuffle_mean"], r["shuffle_mean_over_sA"], r["pass_shuffle_mean"], r["shuffle_sd"], r["shuffle_sd_over_sA"], r["pass_shuffle_sd"]))
        say("K4 %s bootstrap mean %+.4f sd %.4f (= %.3f sA, in [0.8,1.25] %s)" % (nm, r["boot_mean"], r["boot_sd"], r["boot_sd_over_sA"], r["pass_boot"]))
    out["pass"] = bool(ok)
    say("K4", "PASS" if ok else "FAIL")
    return out


def mode_K4S():
    """Reading only (judges nothing): how K4's numbers move with the random-number convention."""
    t1, t2 = get()
    s = {"t1": stepsample(t1), "t2": stepsample(t2)}
    out = {}

    def run(st, rng_sh, rng_bs):
        r0 = F.plain(st, True)
        n = len(st["age"])
        sh = []
        for _ in range(NDRAW):
            perm = rng_sh.permutation(n)
            ss = dict(st); ss["age"] = st["age"][perm]; ss["L"] = st["L"][perm]
            sh.append(F.plain(ss, True)["A"])
        bs = [F.plain(take(st, rng_bs.integers(0, n, n)), True)["A"] for _ in range(NDRAW)]
        return dict(shuffle_mean_over_sA=float(np.mean(sh) / r0["sA"]), shuffle_sd_over_sA=float(np.std(sh, ddof=1) / r0["sA"]),
                    boot_sd_over_sA=float(np.std(bs, ddof=1) / r0["sA"]))
    # (a) one generator for everything, in the order t1 shuffle, t1 bootstrap, t2 shuffle, t2 bootstrap
    g = np.random.default_rng(SEED)
    for nm in ("t1", "t2"):
        out["onegen_" + nm] = run(s[nm], g, g)
    # (b) other seeds, fresh generator per table and per test
    for k in range(1, 6):
        for nm in ("t1", "t2"):
            out["seed+%d_%s" % (k, nm)] = run(s[nm], np.random.default_rng(SEED + k), np.random.default_rng(SEED + k))
    for k, v in out.items():
        say("K4S %-12s shuffle mean %+.3f sA, shuffle sd %.3f sA, bootstrap sd %.3f sA" % (k, v["shuffle_mean_over_sA"], v["shuffle_sd_over_sA"], v["boot_sd_over_sA"]))
    return out


def l1_rows(estimator="plain"):
    """The primary combination and its six single changes. Returns dict name -> (A, sA, per-table rows)."""
    t1, t2 = get()
    s1, s2 = stepsample(t1), stepsample(t2)
    shared = np.isin(s1["id"], t2["id"])
    s1d = D.subset(s1, ~shared)

    def fit(s, **kw):
        if estimator == "plain":
            return F.plain(s, True, **kw)
        return F.structural(s, True, **kw)
    rows = {}
    a1, a2 = fit(s1), fit(s2)
    rows["primary"] = (F.combine([a1, a2]), [a1, a2])
    rows["table1_alone"] = (dict(A=a1["A"], sA=a1["sA"]), [a1])
    rows["table2_alone"] = (dict(A=a2["A"], sA=a2["sA"]), [a2])
    b1 = fit(s1d)
    rows["shared_dropped_t1"] = (F.combine([b1, a2]), [b1, a2])
    c1 = fit(s1, hr="hr_orig")
    rows["t1_original_resid"] = (F.combine([c1, a2]), [c1, a2])
    if estimator == "plain":
        z1, z2 = F.plain(s1, True, zterm=True), F.plain(s2, True, zterm=True)
        rows["redshift_term"] = (F.combine([z1, z2]), [z1, z2])
    return rows


def mode_L1():
    out = {}
    rows = l1_rows("plain")
    t1, t2 = get()
    st1 = F.structural(stepsample(t1), True)
    st2 = F.structural(stepsample(t2), True)
    rows["structural"] = (F.combine([st1, st2]), [st1, st2])
    order = ["primary", "table1_alone", "table2_alone", "shared_dropped_t1", "t1_original_resid", "redshift_term", "structural"]
    for k in order:
        c, parts = rows[k]
        w, d0, d1 = F.w1_word(c["A"], c["sA"])
        out[k] = dict(A=c["A"], sA=c["sA"], dchi2_A0=d0, dchi2_A1=d1, word=w, parts=parts)
        say("L1 %-18s A = %+.4f +- %.4f  dchi2(A=0) %6.2f  dchi2(A=1) %6.2f  %s" % (k, c["A"], c["sA"], d0, d1, w))
        for p in parts:
            extra = ""
            if "g" in p:
                extra = " g %+.4f +- %.4f" % (p["g"], p.get("s_g", float("nan")))
            if "cz" in p:
                extra += " cz %+.4f +- %.4f" % (p["cz"], p["s_cz"])
            if "sint" in p:
                extra += " tau %.3f sint %.4f mu0 %.2f mu1 %.2f s_beta h-check %.5f" % (p["tau"], p["sint"], p["mu0"], p["mu1"], p["s_beta_hcheck"])
            if "sA_scaled" in p:
                extra += " [chi2 %.1f/%d, scaled sA %.4f]" % (p["chi2"], p["dof"], p["sA_scaled"])
            say("      part n=%d %s%s" % (p["n"], fmtA(p), extra))
    first = out["primary"]["word"]
    changed = [k for k in order[1:] if out[k]["word"] != first]
    out["first_word"] = first
    out["second_word"] = "ROBUST" if not changed else "FRAGILE (" + ", ".join(changed) + ")"
    say("L1 reading:", first, "/", out["second_word"])
    return out


def mode_REP():
    t1, t2 = get()
    out = {}
    for nm, t in (("t1", t1), ("t2", t2), ("t1orig", t1)):
        hr = "hr_orig" if nm == "t1orig" else "hr"
        s = stepsample(t)
        gonly = F.wls(np.column_stack([np.ones_like(s["age"]), s["L"] - 0.5]), s[hr], 1.0 / (s["shr"] ** 2 + F.SCAT ** 2))
        g0, s0 = float(gonly[0][1]), float(np.sqrt(gonly[1][1, 1]))
        wa = F.plain(s, True, hr=hr)
        out[nm + "_step"] = dict(g_no_age=g0, s_g_no_age=s0, g_with_age=wa["g"], s_g_with_age=wa["s_g"])
        say("REP %s step g: no age term %+.4f +- %.4f ; with age term %+.4f +- %.4f (n %d)" % (nm, g0, s0, wa["g"], wa["s_g"], wa["n"]))
        for Lv in (0.0, 1.0):
            sub = D.subset(s, s["L"] == Lv)
            r = F.plain(sub, False, hr=hr)
            out["%s_inside_L%d" % (nm, Lv)] = r
            say("REP %s slope inside L=%d (n %d): %s" % (nm, Lv, r["n"], fmtA(r)))
        # no-step plain on the step sample, for comparison with the step fit
        r = F.plain(s, False, hr=hr)
        out[nm + "_nostep_stepsample"] = r
        say("REP %s plain no step on the step sample (n %d): %s" % (nm, r["n"], fmtA(r)))
    # structural with age errors scaled
    for sc in (1.0, 0.5, 0.0):
        for step in (False, True):
            parts = []
            for nm, t in (("t1", t1), ("t2", t2)):
                s = stepsample(t) if step else t
                r = F.structural(s, step, age_err_scale=sc)
                parts.append(r)
                out["struct_%s_scale%.1f_step%d" % (nm, sc, step)] = r
                say("REP structural %s sig_age x %.1f step %d (n %d): %s tau %.3f sint %.4f" % (nm, sc, step, r["n"], fmtA(r), r["tau"], r["sint"]))
            c = F.combine(parts)
            w, d0, d1 = F.w1_word(c["A"], c["sA"])
            out["struct_comb_scale%.1f_step%d" % (sc, step)] = dict(c, dchi2_A0=d0, dchi2_A1=d1, word=w)
            say("REP structural combined sig_age x %.1f step %d: %s dchi2(0) %.2f dchi2(1) %.2f [%s]" % (sc, step, fmtA(c), d0, d1, w))
    # plain without step, combined on the step sample, and with step: words for reference
    return out


def mu_fid(zhd, zhel, om=0.334):
    zg = np.linspace(0, max(zhd) * 1.01 + 1e-3, 20001)
    E = np.sqrt(om * (1 + zg) ** 3 + 1 - om)
    inv = 1 / E
    cum = np.concatenate([[0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(zg))])
    dm = np.interp(zhd, zg, cum) * 299792.458 / 70.0  # Mpc
    return 5 * np.log10((1 + zhel) * dm) + 25


def pp_fit(P, idx, age, step, nbin=8):
    z = P["zHD"][idx]
    order = np.argsort(z, kind="stable")
    binid = np.empty(len(idx), int)
    for b, chunk in enumerate(np.array_split(order, nbin)):
        binid[chunk] = b
    y = P["mB"][idx] - mu_fid(z, P["zHEL"][idx])
    cols = [(binid == b).astype(float) for b in range(nbin)]
    cols += [P["x1"][idx], P["c"][idx], F.S25 * age]
    names = ["o%d" % b for b in range(nbin)] + ["a", "b", "A"]
    if step:
        L = (P["HOST_LOGMASS"][idx] < 10).astype(float)
        cols.append(L - 0.5)
        names.append("g")
    X = np.column_stack(cols)
    w = 1 / P["Cii"][idx]
    p, cov, chi2 = F.wls(X, y, w)
    iA = names.index("A")
    A, sA = float(p[iA]), float(np.sqrt(cov[iA, iA]))
    w1, d0, d1 = F.w1_word(A, sA)
    r = dict(A=A, sA=sA, dchi2_A0=d0, dchi2_A1=d1, word=w1, n=len(idx), chi2=chi2, dof=len(idx) - X.shape[1],
             a=float(p[names.index("a")]), b=float(p[names.index("b")]))
    if step:
        r["g"] = float(p[names.index("g")]); r["s_g"] = float(np.sqrt(cov[names.index("g")] [names.index("g")]))
    return r


def mode_PP():
    t1, t2 = get()
    P = D.load_pantheon()
    sd = np.where(P["IDSURVEY"] == 1)[0]
    cid = np.array([int(c) for c in P["CID"][sd]])
    age1 = dict(zip(t1["id"].tolist(), t1["age"].tolist()))
    age2 = dict(zip(t2["id"].tolist(), t2["age"].tolist()))
    out = {}
    samples = {}
    m = np.array([c in age1 or c in age2 for c in cid])
    samples["union_t1age"] = (sd[m], np.array([age1.get(c, age2.get(c)) for c in cid[m]]))
    samples["union_t2age"] = (sd[m], np.array([age2.get(c, age1.get(c)) for c in cid[m]]))
    m1 = np.array([c in age1 for c in cid])
    samples["t1_hosts"] = (sd[m1], np.array([age1[c] for c in cid[m1]]))
    m2 = np.array([c in age2 for c in cid])
    samples["t2_hosts"] = (sd[m2], np.array([age2[c] for c in cid[m2]]))
    say("PP Pantheon+ SDSS rows %d; union matched %d (t1 %d, t2 %d, both %d)" % (len(sd), m.sum(), m1.sum(), m2.sum(), (m1 & m2).sum()))
    for nm, (idx, age) in samples.items():
        for step in (False, True):
            r = pp_fit(P, idx, age, step)
            out["%s_step%d" % (nm, step)] = r
            gs = (" g %+.4f +- %.4f" % (r["g"], r["s_g"])) if step else ""
            say("PP %-12s step %d n %d: A = %+.4f +- %.4f dchi2(0) %.2f dchi2(1) %.2f [%s] a %+.3f b %+.3f chi2 %.1f/%d%s" % (
                nm, step, r["n"], r["A"], r["sA"], r["dchi2_A0"], r["dchi2_A1"], r["word"], r["a"], r["b"], r["chi2"], r["dof"], gs))
    return out


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


if __name__ == "__main__":
    mode = sys.argv[1]
    tag = sys.argv[2] if len(sys.argv) > 2 else ""
    res = {"K1": mode_K1, "KA": mode_KA, "K3": mode_K3, "K4": mode_K4, "K4S": mode_K4S, "L1": mode_L1, "REP": mode_REP, "PP": mode_PP}[mode]()
    base = os.path.join(HERE, "agb5r_%s%s" % (mode, tag))
    with open(base + ".json", "w") as f:
        json.dump(_clean(res), f, indent=1, sort_keys=True)
    with open(base + ".out", "w") as f:
        f.write("\n".join(LINES) + "\n")
    if mode == "K3":
        sys.exit(3 if res["pass"] else 4)
