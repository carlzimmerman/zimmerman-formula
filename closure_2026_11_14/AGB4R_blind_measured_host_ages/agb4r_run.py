"""AGB4R blind re-grade: checks and fits, written from AGB4's FROZEN_CRITERIA.md and READING.md of this folder.

Usage:  python3 -I agb4r_run.py MODE      MODE in: k1 k2 k3 kr k4 fits rows words
Each mode writes agb4r_<mode>.json beside this file and prints a plain log (redirect it to agb4r_<mode>.out).
Mode k3 exits 3 if all eight twins pass and 4 otherwise.
"""
import os
import sys
import json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb4r_data as D  # noqa: E402  (sets BLAS threads to 2 before numpy)
import numpy as np  # noqa: E402

NB_PP = 8
NB_BIG = 16
NB_ROSE = 4
SEED = 20261117
NDRAW = 400


# ---------------------------------------------------------------- linear algebra (einsum: no BLAS calls)
def wls(M, y, w):
    F = np.einsum("ij,i,ik->jk", M, w, M)
    rhs = np.einsum("ij,i,i->j", M, w, y)
    beta = np.linalg.solve(F, rhs)
    Finv = np.linalg.inv(F)
    r = y - np.einsum("ij,j->i", M, beta)
    chi2 = float(np.einsum("i,i,i->", w, r, r))
    return beta, Finv, r, chi2


def bins_of(s, nb):
    return D.equal_count_bins(s["z"], nb, s["cid"])


def other_columns(s, nb, step, ab):
    b = bins_of(s, nb)
    cols, names = [], []
    for k in range(nb):
        cols.append((b == k).astype(float)); names.append(f"o{k}")
    if step:
        cols.append(s["L"] - 0.5); names.append("g")
    if ab:
        cols.append(s["x1"]); names.append("a")
        cols.append(s["c"]); names.append("b")
    return cols, names


def y_of(s, reading):
    if reading == "R":
        return s["mB"] - s["mu_fid"]
    if reading == "P":
        return s["m_b_corr"] - s["mu_fid"]
    if reading == "big":
        return s["y"]
    raise ValueError(reading)


def templates(age, kind):
    if kind == "single":
        return [D.SLOPE * age], ["A"]
    if kind == "hinge":
        return [D.SLOPE * np.minimum(age, 6.0), D.SLOPE * np.maximum(age - 6.0, 0.0)], ["A_below6", "A_above6"]
    if kind == "pieces":
        return [D.SLOPE * age * (age < 6.0), D.SLOPE * age * (age >= 6.0)], ["A_below6", "A_above6"]
    raise ValueError(kind)


def fit(s, reading, nb, step, age, kind="single", y=None):
    """Fit; return dict. For kind 'single' also the two refits with A fixed at 0 and 1."""
    ab = reading in ("R", "big")
    ocols, onames = other_columns(s, nb, step, ab)
    tcols, tnames = templates(age, kind)
    M = np.column_stack(ocols + tcols)
    names = onames + tnames
    yy = y_of(s, reading) if y is None else y
    w = s["w"]
    beta, Finv, r, chi2 = wls(M, yy, w)
    N, p = M.shape
    out = dict(N=int(N), nbins=nb, reading=reading, step=bool(step), kind=kind, chi2=chi2, dof=int(N - p),
               chi2_per_dof=chi2 / (N - p))
    for j, nm in enumerate(names):
        if nm.startswith("o"):
            continue
        out[nm] = float(beta[j]); out["sig_" + nm] = float(np.sqrt(Finv[j, j]))
    if kind == "single":
        ia = names.index("A")
        A, sA = beta[ia], np.sqrt(Finv[ia, ia])
        Mo = np.column_stack(ocols)
        d = {}
        for k in (0, 1):
            _, _, _, chi2k = wls(Mo, yy - k * tcols[0], w)
            d[k] = chi2k - chi2
        out.update(dchi2_A0=float(d[0]), dchi2_A1=float(d[1]),
                   dchi2_A0_formula=float((A / sA) ** 2), dchi2_A1_formula=float(((A - 1) / sA) ** 2))
        # sandwich (HC0; one row per supernova)
        meat = np.einsum("ij,i,ik->jk", M, (w * r) ** 2, M)
        V = np.einsum("ij,jk,kl->il", Finv, meat, Finv)
        out["sig_A_sandwich_HC0"] = float(np.sqrt(V[ia, ia]))
        out["sig_A_sandwich_HC1"] = float(np.sqrt(V[ia, ia] * N / (N - p)))
    else:
        i1, i2 = len(onames), len(onames) + 1
        out["corr_A_below_above"] = float(Finv[i1, i2] / np.sqrt(Finv[i1, i1] * Finv[i2, i2]))
    return out


# ---------------------------------------------------------------- words
def word_M0(A, d1):
    if d1 < 4:
        return "HOSTS AS LARGE AS THE SLOPE NEEDS"
    if A < 1:
        return "SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA" if d1 >= 9 else "SLOPE OVERPREDICTS THE HOSTS (2 SIGMA)"
    return "HOSTS LARGER THAN THE SLOPE NEEDS"


def word_M1(d0, d1):
    if d1 >= 9 and d0 < 4:
        return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4:
        return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4:
        return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4:
        return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4:
        return "AGE BIAS UNDECIDED"
    return "AGE BIAS NEITHER"


def word_of(model, f):
    return word_M0(f["A"], f["dchi2_A1"]) if model == "M0" else word_M1(f["dchi2_A0"], f["dchi2_A1"])


# ---------------------------------------------------------------- helpers
def jdump(obj, name):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        raise TypeError(type(o))
    with open(os.path.join(HERE, f"agb4r_{name}.json"), "w") as fh:
        json.dump(obj, fh, indent=1, default=conv)


def jload(name):
    with open(os.path.join(HERE, f"agb4r_{name}.json")) as fh:
        return json.load(fh)


def wide_mask(pp, rule):
    if rule == "halfwidth":
        return (pp["age_hi"] - pp["age_lo"]) / 2.0 > 2.5
    if rule == "eitherside":
        return np.maximum(pp["age"] - pp["age_lo"], pp["age_hi"] - pp["age"]) > 2.5
    raise ValueError(rule)


def fmt(f):
    return (f"A = {f['A']:+.4f} +- {f['sig_A']:.4f}  dchi2(A=0) = {f['dchi2_A0']:.3f}  dchi2(A=1) = {f['dchi2_A1']:.3f}"
            f"  N = {f['N']}  chi2/dof = {f['chi2']:.1f}/{f['dof']}"
            + (f"  g = {f['g']:+.4f} +- {f['sig_g']:.4f}" if 'g' in f else "")
            + (f"  a = {f['a']:+.4f} b = {f['b']:+.3f}" if 'a' in f else ""))


# ---------------------------------------------------------------- modes
def mode_k1(X):
    pp = X["pp"]
    dz = np.abs(pp["zHD"] - pp["z_tab_cmb"])
    dzh = np.abs(pp["zHD"] - pp["z_tab_hel"])
    r = float(np.corrcoef(pp["mass_pp"], pp["mass_fsps"])[0, 1])
    allm = X["allm"]
    dz_all = np.abs(allm["zHD"] - allm["z_tab_cmb"])
    res = dict(n_sdss=X["match"]["n_sdss"], n_found=X["match"]["n_found"], N_pp=len(pp["cid"]),
               max_dz_cmb_pp=float(dz.max()), max_dz_hel_pp=float(dzh.max()),
               n_dz_gt_003_pp=int((dz > 0.03).sum()), n_dz_gt_003_all321=int((dz_all > 0.03).sum()),
               corr_mass_pp_fsps=r, mean_mass_diff_pp_minus_fsps=float(np.mean(pp["mass_pp"] - pp["mass_fsps"])))
    res["pass"] = bool(res["n_sdss"] == 321 and res["n_found"] == 321 and res["max_dz_cmb_pp"] <= 0.03 and r >= 0.80)
    for k, v in res.items():
        print(f"K1 {k}: {v}")
    jdump(res, "k1")


def low_share(x1, mask):
    return float(np.mean(x1[mask] < -1)) if mask.sum() else float("nan")


def mode_k2(X):
    pp = X["pp"]
    old = pp["age"] >= 6.0
    res = {}
    for lab, x1 in (("pantheon_x1", pp["x1"]), ("table_x1", pp["x1_tab"])):
        so, sy = low_share(x1, old), low_share(x1, ~old)
        res[lab] = dict(share_old=so, share_young=sy, diff=so - sy, n_old=int(old.sum()), n_young=int((~old).sum()),
                        corr_age_x1=float(np.corrcoef(pp["age"], x1)[0, 1]))
    res["corr_pegase_age_x1"] = float(np.corrcoef(pp["age_mat"], pp["x1"])[0, 1])
    edges = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 14)]
    res["share_by_age_bin"] = [dict(lo=lo, hi=hi, n=int(((pp["age"] >= lo) & (pp["age"] < hi)).sum()),
                                    share=low_share(pp["x1"], (pp["age"] >= lo) & (pp["age"] < hi)))
                               for lo, hi in edges]
    res["pass"] = bool(res["pantheon_x1"]["diff"] >= 0.15)
    print(json.dumps(res, indent=1))
    jdump(res, "k2")


def mode_k3(X):
    rows = []
    allpass = True
    for sname, s, reading, nb in (("pp", X["pp"], "R", NB_PP), ("big", X["big"], "big", NB_BIG)):
        b = bins_of(s, nb)
        for model in ("M0", "M1"):
            step = model == "M1"
            for A_true in (1.0, 0.0):
                y = (-19.30 + 0.02 * b) + (0.05 * (s["L"] - 0.5) if step else 0.0) - 0.15 * s["x1"] + 3.1 * s["c"] \
                    + A_true * D.SLOPE * s["age"]
                f = fit(s, reading, nb, step, s["age"], y=y)
                ok = abs(f["A"] - A_true) <= 1e-6 and f["chi2"] <= 1e-8
                allpass &= ok
                rows.append(dict(sample=sname, model=model, A_true=A_true, A_hat=f["A"], chi2=f["chi2"],
                                 g=f.get("g"), a=f["a"], b=f["b"], passed=bool(ok)))
                print(f"K3 {sname} {model} A_true={A_true:.0f}: A_hat={f['A']:.12f} chi2={f['chi2']:.3e} "
                      f"a={f['a']:+.9f} b={f['b']:+.9f} g={f.get('g')} pass={ok}")
    jdump(dict(twins=rows, pass_=bool(allpass)), "k3")
    print("K3 all pass:", allpass)
    sys.exit(3 if allpass else 4)


def mode_kr(X):
    t = D.load_tsv("campbell_local.tsv")
    R = X["rose_summary"]
    snid = t["SNID"].astype(int)
    assert len(set(snid)) == len(snid)
    has = np.array([s in R for s in snid])
    z, mu, emu = t["redshift"], t["mu"], t["err_mu"]
    mu_line = D.mu_flat(z, z, 0.3)
    hr = mu - mu_line
    loc = np.array([R[s]["local"] if s in R else np.nan for s in snid])
    m = has & np.isfinite(loc)
    young = m & (loc < 8.0); old = m & (loc >= 8.0)
    w = 1.0 / emu ** 2

    def wmean(x, k):
        return float(np.sum(w[k] * x[k]) / np.sum(w[k])), float(1 / np.sqrt(np.sum(w[k])))
    my, ey = wmean(hr, young); mo, eo = wmean(hr, old)
    step_w = my - mo; err_w = float(np.hypot(ey, eo))
    step_u = float(hr[young].mean() - hr[old].mean())
    err_u = float(np.sqrt(hr[young].var(ddof=1) / young.sum() + hr[old].var(ddof=1) / old.sum()))
    own = t["hr"]
    step_own_w = wmean(own, young)[0] - wmean(own, old)[0]
    step_own_u = float(own[young].mean() - own[old].mean())
    res = dict(n_rows=int(len(snid)), n_with_age=int(m.sum()), n_young=int(young.sum()), n_old=int(old.sum()),
               n_age_exactly_8=int((loc == 8.0).sum()),
               step_weighted=step_w, err_weighted=err_w, step_unweighted=step_u, err_unweighted=err_u,
               step_own_hr_weighted=float(step_own_w), step_own_hr_unweighted=step_own_u,
               target=0.114, tol=0.04)
    res["pass"] = bool(abs(step_w - 0.114) <= 0.04)
    for k, v in res.items():
        print(f"KR {k}: {v}")
    jdump(res, "kr")


def mode_k4(X):
    pp = X["pp"]
    b = bins_of(pp, NB_PP)
    out = {}
    for model in ("M0", "M1"):
        step = model == "M1"
        f = fit(pp, "R", NB_PP, step, pp["age"])
        sA = f["sig_A"]
        rng = np.random.default_rng(SEED)
        As = np.empty(NDRAW)
        for i in range(NDRAW):
            perm = np.arange(len(b))
            for k in range(NB_PP):
                idx = np.where(b == k)[0]
                perm[idx] = idx[rng.permutation(len(idx))]
            s2 = dict(pp)
            s2["age"] = pp["age"][perm]; s2["L"] = pp["L"][perm]
            As[i] = fit(s2, "R", NB_PP, step, s2["age"])["A"]
        mean_r = float(As.mean() / sA); scat_r = float(As.std(ddof=1) / sA)
        sand_r = f["sig_A_sandwich_HC0"] / sA
        ok = abs(mean_r) <= 0.2 and 0.8 <= scat_r <= 1.25 and 0.8 <= sand_r <= 1.25
        out[model] = dict(sig_A=sA, shuffle_mean_A=float(As.mean()), shuffle_scatter=float(As.std(ddof=1)),
                          mean_over_sig=mean_r, scatter_over_sig=scat_r, sandwich_HC0=f["sig_A_sandwich_HC0"],
                          sandwich_HC0_over_sig=sand_r, sandwich_HC1_over_sig=f["sig_A_sandwich_HC1"] / sA,
                          passed=bool(ok))
        print(f"K4 {model}: sig_A={sA:.4f} mean(A_shuf)/sig={mean_r:+.3f} scatter/sig={scat_r:.3f} "
              f"sandwich(HC0)/sig={sand_r:.3f} HC1/sig={f['sig_A_sandwich_HC1'] / sA:.3f} pass={ok}")
    jdump(out, "k4")


def forks(X, model):
    pp = X["pp"]
    step = model == "M1"
    keep = ~wide_mask(pp, "halfwidth")
    ppn = D.subset(pp, keep)
    res = {
        "primary": fit(pp, "R", NB_PP, step, pp["age"]),
        "reading_P": fit(pp, "P", NB_PP, step, pp["age"]),
        "bins_12": fit(pp, "R", 12, step, pp["age"]),
        "sample_big": fit(X["big"], "big", NB_BIG, step, X["big"]["age"]),
        "pp_no_wide": fit(ppn, "R", NB_PP, step, ppn["age"]),
    }
    keep2 = ~wide_mask(pp, "eitherside")
    pp2 = D.subset(pp, keep2)
    res["reading_only_pp_no_wide_eitherside"] = fit(pp2, "R", NB_PP, step, pp2["age"])
    for k, f in res.items():
        f["word"] = word_of(model, f)
    return res


def mode_fits(X):
    out = {}
    for model in ("M0", "M1"):
        out[model] = forks(X, model)
        for k, f in out[model].items():
            print(f"{model} {k:36s} {fmt(f)}  ->  {f['word']}")
    jdump(out, "fits")


def reliability(s, nb, step, ab, Z2key):
    b = bins_of(s, nb)
    w = s["w"]

    def dm(x):
        o = x.astype(float).copy()
        for k in range(nb):
            i = b == k
            o[i] = x[i] - np.sum(w[i] * x[i]) / np.sum(w[i])
        return o
    W, Z1, Z2 = dm(s["age"]), dm(s["x1"]), dm(s[Z2key])
    sw = w.sum()

    def cov(u, v):
        return float(np.sum(w * u * v) / sw)
    shared = cov(W, Z1) * cov(W, Z2) / cov(Z1, Z2)
    varW = cov(W, W)
    rel = shared / varW
    noise = varW - shared
    ocols, _ = other_columns(s, nb, step, ab)
    _, _, rW, _ = wls(np.column_stack(ocols), s["age"], w)
    var_left = float(np.sum(w * rW ** 2) / sw)
    rel_fit = 1 - noise / var_left
    return dict(cov_W_Z1=cov(W, Z1), cov_W_Z2=cov(W, Z2), cov_Z1_Z2=cov(Z1, Z2), var_W=varW, shared=shared,
                reliability=rel, noise=noise, var_left_in_fit=var_left, reliability_in_fit=rel_fit)


def mode_rows(X):
    pp, rose, big = X["pp"], X["rose"], X["big"]
    out = {}
    for model in ("M0", "M1"):
        step = model == "M1"
        r = {}
        for agek in ("age_rose_global", "age_rose_local"):
            for reading in ("R", "P"):
                r[f"rose_{agek}_{reading}"] = fit(rose, reading, NB_ROSE, step, rose[agek])
        r["rose_fsps_R_same66"] = fit(rose, "R", NB_ROSE, step, rose["age"])
        r["pegase_R"] = fit(pp, "R", NB_PP, step, pp["age_mat"])
        bs = D.subset(big, big["type"] == "SNIa")
        r["big_spec387"] = fit(bs, "big", NB_BIG, step, bs["age"])
        for f in r.values():
            f["word_if_judged"] = word_of(model, f)
        r["split6_hinge"] = fit(pp, "R", NB_PP, step, pp["age"], kind="hinge")
        r["split6_pieces"] = fit(pp, "R", NB_PP, step, pp["age"], kind="pieces")
        prim = fit(pp, "R", NB_PP, step, pp["age"])
        for Z2 in ("mass_pp", "mass_fsps"):
            rl = reliability(pp, NB_PP, step, True, Z2)
            rl["A_corrected"] = prim["A"] / rl["reliability_in_fit"]
            rl["sig_A_corrected"] = prim["sig_A"] / rl["reliability_in_fit"]
            r[f"reliability_Z2_{Z2}"] = rl
        out[model] = r
        for k, f in r.items():
            if "A" in f:
                print(f"{model} {k:30s} {fmt(f)}  [{f['word_if_judged']}]")
            elif "A_below6" in f:
                print(f"{model} {k:30s} A_below6 = {f['A_below6']:+.3f} +- {f['sig_A_below6']:.3f}  "
                      f"A_above6 = {f['A_above6']:+.3f} +- {f['sig_A_above6']:.3f}  corr {f['corr_A_below_above']:+.2f}")
            else:
                print(f"{model} {k:30s} reliability {f['reliability']:.3f} in fit {f['reliability_in_fit']:.3f}  "
                      f"A/rel = {f['A_corrected']:+.3f} +- {f['sig_A_corrected']:.3f}  (var_W {f['var_W']:.3f}, "
                      f"shared {f['shared']:.3f}, var_left {f['var_left_in_fit']:.3f})")
    k2 = jload("k2")
    out["low_stretch_share_by_age"] = k2["share_by_age_bin"]
    jdump(out, "rows")


def mode_words():
    k1, k2, k3, k4 = jload("k1"), jload("k2"), jload("k3"), jload("k4")
    kr, fits = jload("kr"), jload("fits")
    gate = k1["pass"] and k2["pass"] and k3["pass_"]
    res = dict(K1=k1["pass"], K2=k2["pass"], K3=k3["pass_"], K4_M0=k4["M0"]["passed"], K4_M1=k4["M1"]["passed"],
               KR=kr["pass"])
    for model in ("M0", "M1"):
        F = fits[model]
        first = F["primary"]["word"]
        diff = [k for k in ("reading_P", "bins_12", "sample_big", "pp_no_wide") if F[k]["word"] != first]
        second = "ROBUST" if not diff else "FRAGILE (" + ", ".join(diff) + ")"
        if not gate:
            word = "NOT EVALUABLE (K1/K2/K3)"
        elif not k4[model]["passed"]:
            word = "NO WORD (K4 failed for this configuration)"
        else:
            word = f"{first}, {second}"
        res[model] = dict(word=word, first_word_as_read=first, second_word_as_read=second,
                          A=F["primary"]["A"], sig_A=F["primary"]["sig_A"],
                          dchi2_A0=F["primary"]["dchi2_A0"], dchi2_A1=F["primary"]["dchi2_A1"])
        print(f"{model}: {word}   (A = {F['primary']['A']:+.4f} +- {F['primary']['sig_A']:.4f}, "
              f"dchi2(A=0) = {F['primary']['dchi2_A0']:.3f}, dchi2(A=1) = {F['primary']['dchi2_A1']:.3f})")
    res["rose_rows"] = "evaluable" if kr["pass"] else "NOT EVALUABLE (KR failed)"
    print("checks:", {k: res[k] for k in ("K1", "K2", "K3", "K4_M0", "K4_M1", "KR")})
    print("Rose rows:", res["rose_rows"])
    jdump(res, "words")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "words":
        mode_words()
    else:
        X = D.build_samples()
        dict(k1=mode_k1, k2=mode_k2, k3=mode_k3, kr=mode_kr, k4=mode_k4, fits=mode_fits, rows=mode_rows)[mode](X)
