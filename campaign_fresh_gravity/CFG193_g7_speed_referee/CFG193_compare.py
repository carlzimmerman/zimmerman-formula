#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_compare -- PHASE 2 ONLY: run after my own main and MUTATE runs are saved.  Opens CFG186's outputs (its .npz, .json, first-run
and second-run files) and compares them with mine:  (1) velocities, (2) u, (3) the 2D curves cell by cell, (4) MY fitter on THEIR
curves (decomposes the beta_hat difference into curves / speeds / fitter), (5) the row-by-row numbers, (6) attack (e): first vs second
vs final runs.  No CFG186 script is imported or run.  Outputs: CFG193_compare.out, CFG193_compare_results.json.
Rerun: ZF_REPO=<repo> python3 CFG193_compare.py  (< 3 min).  Exit 0 (the classification of each difference is in README.md)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *

T = Tee(os.path.join(HERE, "CFG193_compare.out"))
P = T.p
LANE = os.path.join(REPO, "campaign_fresh_gravity", "CFG186_a0_vs_cmb_speed")
P("CFG193_compare (repo = <repo>; CFG186 files read: its .npz / .json / .out only)")
th = np.load(os.path.join(LANE, "cfg186_a_curves.npz"), allow_pickle=True)
tnames = [str(x) for x in th["names"]]
tj_a = json.load(builtins.open(os.path.join(LANE, "cfg186_a_curves_power_results.json")))["numbers"]
tj_b = json.load(builtins.open(os.path.join(LANE, "cfg186_b_fit_results.json")))["numbers"]
mj_c = json.load(builtins.open(os.path.join(HERE, "CFG193_c_fit_power_results.json")))
mj_a = json.load(builtins.open(os.path.join(HERE, "CFG193_a_velocities_results.json")))
R = {}

# ------------------------------------------------------------------ (1) velocities
ut = np.load(os.path.join(HERE, "CFG193_utable.npz"))
un = [str(x) for x in ut["names"]]
tcz = dict(zip(tnames, th["cz_hel"])); tsrc = dict(zip(tnames, [str(x) for x in th["cz_src"]]))
mcz = dict(zip(un, ut["cz"]))
import csv
msrc = {}
with builtins.open(os.path.join(HERE, "CFG193_utable.csv")) as f:
    for r in csv.DictReader(f):
        msrc[r["name"]] = r["source"]
only_t = [n for n in tnames if np.isfinite(tcz[n]) and n not in mcz]
only_m = [n for n in un if n not in tcz or not np.isfinite(tcz[n])]
both = [n for n in tnames if n in mcz and np.isfinite(tcz[n])]
dcz = np.array([mcz[n] - tcz[n] for n in both])
P("(1) velocities among the 149 clean: CFG186 has %d with a velocity, mine %d; in both %d; only in CFG186: %s; only in mine: %s" % (
    sum(np.isfinite(tcz[n]) for n in tnames), len(un), len(both), only_t, only_m))
P("    cz_hel differences over the %d common galaxies: max |dcz| = %.1f km/s; galaxies with |dcz| > 0.5: %s" % (len(both), float(np.max(np.abs(dcz))), [(n, mcz[n], tcz[n]) for n in both if abs(mcz[n] - tcz[n]) > 0.5]))
sdiff = [(n, msrc[n], tsrc[n]) for n in both if msrc[n] != tsrc[n]]
P("    source label differences (mine vs CFG186) among common galaxies: %s" % sdiff)
R["vel"] = dict(only_theirs=only_t, only_mine=only_m, max_dcz=float(np.max(np.abs(dcz))), source_diffs=sdiff)
# whole-sample source counts in CFG186 (all 175) vs mine
P("    velocity source counts, all 175 (README/JSON of CFG186 vs mine): %s  vs  %s" % (tj_a["velocity_sources"], mj_a["sources"]))

# ------------------------------------------------------------------ (2) u
def their_u(names, dist="luminosity"):
    """CFG186's own construction (D read as a LUMINOSITY distance in its z_cos table), recomputed from ITS cz_hel, l, b (its .npz)"""
    out = {}
    for n in names:
        i = tnames.index(n)
        if not np.isfinite(th["cz_hel"][i]):
            continue
        zc = cmb_convert(th["cz_hel"][i], th["l"][i], th["b"][i])
        out[n] = float(u_los(zc, th["D"][i], H0_PRIMARY, dist=dist))
    return out
prim_t = [n for n, ip in zip(tnames, th["isprim"]) if ip]
prim_m = [n for n in un if ut["fD"][un.index(n)] in (2, 3, 4, 5)]
P("(2) primary sets: CFG186 %d, mine %d; identical: %s" % (len(prim_t), len(prim_m), sorted(prim_t) == sorted(prim_m)))
ut_their = their_u(prim_t)
d_prim = []
for n in prim_t:
    ui = un.index(n)
    d_prim.append((n, float(ut["u"][ui]), ut_their.get(n, np.nan), float(ut["ulum"][ui])))
du_comov = np.array([a[1] - a[2] for a in d_prim]); du_lum = np.array([a[3] - a[2] for a in d_prim])
P("    R2 |u_mine(comoving D) - u_CFG186 (recomputed by its convention: D luminosity, its cz)|: max %.1f, median %.1f km/s; galaxies > 20 km/s: %d; > 10: %d" % (
    np.max(np.abs(du_comov)), np.median(np.abs(du_comov)), int(np.sum(np.abs(du_comov) > 20)), int(np.sum(np.abs(du_comov) > 10))))
P("    same with my luminosity-D variant (only the D convention matches): max %.2f, median %.2f km/s" % (np.max(np.abs(du_lum)), np.median(np.abs(du_lum))))
P("    largest 5 |du| (comoving vs CFG186): %s" % sorted([(n, round(a - b, 1)) for n, a, b, c in d_prim], key=lambda x: -abs(x[1]))[:5])
R["u"] = dict(max_abs_comoving=float(np.max(np.abs(du_comov))), n_gt20=int(np.sum(np.abs(du_comov) > 20)), max_abs_lum=float(np.max(np.abs(du_lum))))
P("    sigma_u medians (mine vs CFG186 JSON): %s  vs  %s" % (mj_a["sigma_u_median"], {k: round(v["sigma_u_med"], 1) for k, v in tj_a["velocity_by_method"].items() if k in ("TRGB", "Cepheid", "UMa", "SNIa")}))
P("    z catalogue sd: mine %.4f vs CFG186 %.4f; corr(u, V_LG.n): mine %.3f vs CFG186 %.3f" % (mj_c["rms_z"], tj_a["z_W1_catalogue"]["sd"], mj_a["r_u_VLGn"], tj_a["corr_u_VLGproj"]))

# ------------------------------------------------------------------ (3) curves cell by cell
cnp = np.load(os.path.join(HERE, "CFG193_curves.npz")); cn = [str(x) for x in cnp["names"]]
tch = th["chi"].astype(float)
tt2 = (TG ** 2)[None, :, None]
def compare_curves(cnp_, label):
    cn_ = [str(x) for x in cnp_["names"]]
    per = {}
    allrel, alld = [], []
    for n in cn_:
        if n not in tnames:
            continue
        a = cnp_["C"][cn_.index(n)] + (TG ** 2)[:, None]
        b = tch[tnames.index(n)]
        m = np.isfinite(a) & np.isfinite(b)
        gmin = np.nanmin(b)
        sel = m & (b - gmin <= 25.0)
        d = (a - b)[sel]
        per[n] = (float(np.max(np.abs(d))), float(np.median(d)))
        alld.append(d)
    ad = np.concatenate(alld)
    worst = sorted(per.items(), key=lambda kv: -kv[1][0])[:6]
    P("(3) curves [%s]: %d galaxies, %d cells within dchi2<=25 of the minimum: median (mine - CFG186) = %+.4f, 95%% |d| = %.4f, max |d| = %.3f; galaxies with max|d| > 0.1: %d" % (
        label, len(per), ad.size, float(np.median(ad)), float(np.percentile(np.abs(ad), 95)), float(np.max(np.abs(ad))), sum(1 for v in per.values() if v[0] > 0.1)))
    P("    worst galaxies (max|d|, median d): %s" % [(k, round(v[0], 3), round(v[1], 3)) for k, v in worst])
    return per
per_main = compare_curves(cnp, "my main curves vs CFG186")
R["curves_main"] = {k: v[0] for k, v in per_main.items()}
u2f = os.path.join(HERE, "CFG193_curves_U2.npz")
if os.path.exists(u2f):
    per_u2 = compare_curves(np.load(u2f), "my U2 point-mask variant vs CFG186")
    R["curves_U2"] = {k: v[0] for k, v in per_u2.items()}
# which galaxies have a different point set (CFG186 drops points with baryonic V^2 <= 0 at fiducial Upsilon and uses unsigned Vd^2)
gal = load_sparc(); gb = {g["name"]: g for g in gal}
diffpts = []
for n in prim_t:
    g = gb[n]
    m1 = usable_mask(g, "U1"); m2 = usable_mask(g, "U2")
    if m1.sum() != m2.sum():
        diffpts.append((n, int(m1.sum()), int(m2.sum())))
P("    primary galaxies whose usable-point set differs between my U1 and the U2 (CFG186-like) mask: %s" % diffpts)
R["point_mask_diffs"] = diffpts

# ------------------------------------------------------------------ (4) MY fitter on THEIR curves
def build_z(names, u0, h0=H0_PRIMARY, dist="comoving"):
    Zs = []
    for n, u_ in zip(names, u0):
        i = tnames.index(n)
        zc = cmb_convert(th["cz_hel"][i], th["l"][i], th["b"][i])
        D, eD = th["D"][i], th["eD"][i]
        Dt = np.maximum(D + eD * TF, 0.3 * D)
        du = u_los(zc, Dt, h0, dist=dist) - u_los(zc, D, h0, dist=dist)
        Zs.append(((u_ + du) / W_REF) ** 2)
    return np.array(Zs)
def fit_on(C, npt, names, Zmat, label):
    cv = Curves(names, C, meta=dict(N=npt))
    sg, xh, _ = cv.sigma_i()
    L0, tau = cv.tau_ml(sg, xh)
    st = Stat(cv.ceff_fast(tau))
    L, b, F = fit_LB(st, Zmat, L0=L0, retall=True)
    z0 = Zmat[:, 80]
    v = 1 / (sg ** 2 + tau ** 2); zb = np.sum(v * z0) / np.sum(v)
    fis = LN10 / math.sqrt(np.sum(v * (z0 - zb) ** 2))
    prof = {}
    for bb in (0.0, 0.5, 0.887):
        from scipy.optimize import minimize_scalar
        r = minimize_scalar(lambda LL: st.F(LL, bb, Zmat), bounds=(-11.3, -9.0), method="bounded", options=dict(xatol=1e-5))
        prof[bb] = r.fun - F
    P("(4) %-52s beta_hat = %+.3f (L %.3f), tau %.3f, median sigma_i %.3f, Fisher %.3f, dF(0) %.2f dF(0.5) %.2f dF(0.887) %.2f" % (label, b, L, tau, np.median(sg), fis, prof[0.0], prof[0.5], prof[0.887]))
    return b, tau, float(np.median(sg)), fis, prof
ip = [tnames.index(n) for n in prim_t]
Ct = th["chi"][ip].astype(float) - (TG ** 2)[None, :, None]           # their curves without t^2
npt_t = th["npt"][ip]
u_their_arr = np.array([ut_their[n] for n in prim_t])
Z_their = build_z(prim_t, u_their_arr, dist="luminosity")
u_mine_arr = np.array([float(ut["u"][un.index(n)]) for n in prim_t])
Z_mine = build_z(prim_t, u_mine_arr, dist="comoving")
DU_mine = Z_mine * 0.0
for _i, _n in enumerate(prim_t):
    _k = tnames.index(_n); _zc = cmb_convert(th["cz_hel"][_k], th["l"][_k], th["b"][_k]); _Dt = np.maximum(th["D"][_k] + th["eD"][_k] * TF, 0.3 * th["D"][_k])
    DU_mine[_i] = u_los(_zc, _Dt) - u_los(_zc, th["D"][_k])
res4 = {}
res4["their_curves__their_speeds"] = fit_on(Ct, npt_t, prim_t, Z_their, "THEIR curves, THEIR speeds (lum D), MY fitter")
res4["their_curves__my_speeds"] = fit_on(Ct, npt_t, prim_t, Z_mine, "THEIR curves, MY speeds (comoving D), MY fitter")
Cm = np.array([cnp["C"][cn.index(n)] for n in prim_t])
Nm = np.array([cnp["N"][cn.index(n)] for n in prim_t])
res4["my_curves__their_speeds"] = fit_on(Cm, Nm, prim_t, Z_their, "MY curves, THEIR speeds, MY fitter")
res4["my_curves__my_speeds"] = fit_on(Cm, Nm, prim_t, Z_mine, "MY curves, MY speeds, MY fitter")
if os.path.exists(u2f):
    cu2 = np.load(u2f); cn2 = [str(x) for x in cu2["names"]]
    C2 = np.array([cu2["C"][cn2.index(n)] for n in prim_t]); N2 = np.array([cu2["N"][cn2.index(n)] for n in prim_t])
    res4["my_U2_curves__my_speeds"] = fit_on(C2, N2, prim_t, Z_mine, "MY U2-mask curves, MY speeds, MY fitter")
    res4["my_U2_curves__their_speeds"] = fit_on(C2, N2, prim_t, Z_their, "MY U2-mask curves, THEIR speeds, MY fitter")

# (4b) who is right where the curves differ: direct 40-start least-squares at the worst cell of every galaxy with max|d| > 0.1
from scipy.optimize import least_squares
nu_m = get_kernel("mono")
bad = [n for n, v in per_main.items() if v[0] > 0.1]
P("(4b) galaxies whose curves differ by > 0.1 anywhere within dchi2<=25 of the minimum: %d" % len(bad))
who = {}
for n in bad:
    a_ = cnp["C"][cn.index(n)] + (TG ** 2)[:, None]
    b_ = tch[tnames.index(n)]
    dd_ = a_ - b_
    sel_ = np.isfinite(dd_) & (b_ - np.nanmin(b_) <= 25.0)
    dabs = np.where(sel_, np.abs(dd_), -1.0)
    i, j = np.unravel_index(np.argmax(dabs), dabs.shape)
    G = Gal(gb[n])
    a0 = 10 ** XG[j]; scl = math.sqrt(max(G.D + G.eD * TG[i], 0.3 * G.D) / G.D)
    lo_, hi_ = np.array([-1.6, -1.6, 5.0]), np.array([0.8, 0.8, 89.0])
    rng = np.random.RandomState(7)
    best = 1e9
    for s_ in range(40):
        p0 = np.clip([math.log10(0.5) + rng.uniform(-0.3, 0.3), math.log10(0.7) + rng.uniform(-0.3, 0.3), G.inc + rng.uniform(-2, 2) * G.einc], lo_ + 1e-6, hi_ - 1e-6)
        sol = least_squares(lambda p: resid(G, np.array([p]), np.array([a0]), np.array([scl]), nu_m, True)[0], p0, bounds=(lo_, hi_))
        best = min(best, 2 * sol.cost)
    direct = best + TG[i] ** 2
    who[n] = (float(TG[i]), float(XG[j]), float(a_[i, j]), float(b_[i, j]), float(direct))
    verdict = "CFG186 above the direct minimum (trapped)" if b_[i, j] - direct > 0.1 else ("MINE above the direct minimum (trapped)" if a_[i, j] - direct > 0.1 else "both at the direct minimum (different point set / model)")
    P("     %-10s worst cell t=%+.2f x=%.2f: mine %.3f | CFG186 %.3f | direct 40-start %.3f -> %s" % (n, TG[i], XG[j], a_[i, j], b_[i, j], direct, verdict))
R["who_is_right"] = who
# (4b) swap tests: replace the differing galaxies' curves
def swap_fit(base_C, base_N, other_C, names_swap, label):
    C_ = base_C.copy()
    for n in names_swap:
        if n in prim_t:
            C_[prim_t.index(n)] = other_C[prim_t.index(n)]
    return fit_on(C_, base_N, prim_t, Z_mine, label)
bad_prim = [n for n in bad if n in prim_t]
trapped3 = [n for n in bad_prim if n in ("NGC2403", "F571-8", "UGC05764")]
P("     primary galaxies among the differing ones: %s" % bad_prim)
res4["their_curves_with_my_NGC2403"] = swap_fit(Ct, npt_t, Cm, ["NGC2403"], "THEIR curves, NGC2403 replaced by mine, MY speeds")
res4["their_curves_with_my_3"] = swap_fit(Ct, npt_t, Cm, trapped3, "THEIR curves, %s replaced by mine, MY speeds" % trapped3)
res4["their_curves_with_my_all_differing"] = swap_fit(Ct, npt_t, Cm, bad_prim, "THEIR curves, all %d differing primaries replaced by mine" % len(bad_prim))
res4["my_curves_with_their_NGC2403"] = swap_fit(Cm, Nm, Ct, ["NGC2403"], "MY curves, NGC2403 replaced by THEIRS, MY speeds")

# (4c) speed-shuffle null (400 permutations, seed 193102 stream) on THEIR curves, THEIR curves with my NGC2403, and MY curves, all with MY fitter
import multiprocessing as mp
_STAT = {}
def _shuf_task(args):
    key, seed = args
    st, u0, du = _STAT[key]
    rng = np.random.RandomState(seed)
    perm = rng.permutation(len(u0))
    zz = ((u0[perm][:, None] + du) / W_REF) ** 2
    return fit_LB(st, zz, L0=-10.06)[1]
def null_on(C_, N_, label, seeds):
    cv_ = Curves(prim_t, C_, meta=dict(N=N_)); sg_, xh_, _ = cv_.sigma_i(); L0_, tau_ = cv_.tau_ml(sg_, xh_)
    st_ = Stat(cv_.ceff_fast(tau_))
    u0_ = u_mine_arr
    du_ = DU_mine
    _STAT[label] = (st_, u0_, du_)
    Lb, bb = fit_LB(st_, Z_mine, L0=L0_)
    with mp.get_context("fork").Pool(min(14, os.cpu_count() or 4)) as pool:
        out = np.array(pool.map(_shuf_task, [(label, sd) for sd in seeds], chunksize=4))
    p_ = (1 + int(np.sum(np.abs(out) >= abs(bb)))) / (len(out) + 1)
    P("(4c) shuffle null on %-40s beta_hat %+.3f; null 16/50/84%% = %+.3f / %+.3f / %+.3f; p(|beta|>=|obs|) = %.3f (N=%d)" % (label, bb, np.percentile(out, 16), np.median(out), np.percentile(out, 84), p_, len(out)))
    return dict(beta=float(bb), p16=float(np.percentile(out, 16)), p50=float(np.median(out)), p84=float(np.percentile(out, 84)), p=float(p_))
_seeds = [193102 + k for k in range(400)]
res4["null_their"] = null_on(Ct, npt_t, "THEIR curves", _seeds)
_Csw = Ct.copy(); _Csw[prim_t.index("NGC2403")] = Cm[prim_t.index("NGC2403")]
res4["null_their_my2403"] = null_on(_Csw, npt_t, "THEIR curves + my NGC2403", _seeds)
res4["null_mine"] = null_on(Cm, Nm, "MY curves", _seeds)
R["fit_on"] = {k: dict(beta=v[0], tau=v[1], sigma_i=v[2], fisher=v[3]) for k, v in res4.items() if isinstance(v, tuple)}
P("    CFG186's own values: beta_hat = %+.3f, tau = %.3f, median sigma_i = %.3f, Fisher %.3f (dF(0) = %.2f)" % (tj_b["primary"]["beta"], tj_a["tau"], tj_a["primary_sigma_median"], tj_a["power"]["W1_H67.66"]["sigma_fisher"], tj_b["primary"]["dF_beta0"]))

# ------------------------------------------------------------------ (5) row-by-row numbers
P("(5) row-by-row: mine (CFG193) vs CFG186; 'within' uses the frozen pass lines")
def rowline(label, mine, theirs, lo=None, hi=None, fmt="%+.3f", tol=None):
    ok = ""
    if lo is not None:
        ok = " -> %s" % ("within [%g, %g]" % (lo, hi) if lo <= mine <= hi else "OUTSIDE [%g, %g]" % (lo, hi))
    P("    %-46s mine %s | CFG186 %s%s" % (label, fmt % mine, fmt % theirs, ok))
rowline("Fisher sigma_beta (W1, H0 67.66)", mj_c["fisher"], tj_a["power"]["W1_H67.66"]["sigma_fisher"], 0.405, 0.495, "%.4f")
rowline("median Birge s", mj_c["median_s"], 1.43, fmt="%.3f")
rowline("median sigma_i (dex)", mj_c["median_sigma_i"], tj_a["primary_sigma_median"], fmt="%.4f")
rowline("tau (dex)", mj_c["tau"], tj_a["tau"], fmt="%.4f")
rowline("L0 (ML, beta = 0)", mj_c["L0_ml"], tj_a["L0"], fmt="%.4f")
rowline("beta_hat (primary)", mj_c["beta"], tj_b["primary"]["beta"], 0.74, 1.04)
rowline("log10 abar0", mj_c["L"], tj_b["primary"]["L"], fmt="%.4f")
rowline("bootstrap sigma (16-84 half-width)", mj_c["boot_sigma"], tj_b["bootstrap"]["sigma"], 0.60, 0.74, "%.4f")
rowline("bootstrap 2.5%", mj_c["boot_lo"], tj_b["bootstrap"]["p2.5"])
rowline("bootstrap 97.5%", mj_c["boot_hi"], tj_b["bootstrap"]["p97.5"])
rowline("speed-shuffle p (two-sided)", mj_c["p_shuffle"], tj_b["nulls"]["perm"]["p_two"], 0.04, 0.13, "%.4f")
rowline("speed-shuffle null median", mj_c["shuffle_median"], tj_b["nulls"]["perm"]["median"])
rowline("speed-shuffle null 16%", mj_c["shuffle_p16"], tj_b["nulls"]["perm"]["p16"])
rowline("speed-shuffle null 84%", mj_c["shuffle_p84"], tj_b["nulls"]["perm"]["p84"])
rowline("shuffle within method groups p", mj_c["p_shuffle_within_method"], tj_b["nulls"]["perm_within_groups"]["p_two"], fmt="%.4f")
rowline("noise-injection p (mine: C3 point-level mocks, N=40; CFG186: curve-level mocks)", mj_c["p_noise"], tj_b["nulls"]["noise"]["p_two"], fmt="%.4f")
rowline("mock sigma_beta at beta = 0 (mine C3; CFG186 curve-level)", mj_c["sigma_c3"], tj_a["power"]["W1_H67.66"]["sigma_mock"], fmt="%.3f")
rowline("beta_det (2 sigma)", mj_c["beta_det"], tj_a["power"]["W1_H67.66"]["beta_det_2sigma"], fmt="%.2f")
rowline("W2 Fisher sigma_beta", mj_c["A4"]["fisher_W2"], tj_a["power"]["W2_H67.66"]["sigma_fisher"], fmt="%.3f")
rowline("H0 = 73 Fisher sigma_beta", mj_c["A1"]["u73"]["fisher"], tj_a["power"]["W1_H73"]["sigma_fisher"], fmt="%.3f")
rowline("shuffle-Neyman 95% upper limit", mj_c["neyman_up95"], tj_b["neyman_shuffle"]["beta95"], fmt="%.2f")
rowline("bootstrap 95th percentile", mj_c["boot_p95"], tj_b["beta95_bootstrap"], fmt="%.2f")
rowline("QUOTED 95% upper limit (largest of construction/bootstrap)", mj_c["quoted_limit"], tj_b["beta95_quoted"], fmt="%.2f")
rowline("KM1 eps_min", mj_c["km1_eps_min"], tj_b["KM1"]["eps_min_95"], fmt="%.2e")
smap = {"H0 = 73": "H0 = 73", "z frozen at catalogue distance": "z frozen at catalogue distance", "I: TRGB + Cepheid + SNIa": "I: TRGB + Cepheid + SNIa",
        "UMa only": "UMa (one cluster distance)", "W2 (coherent LG flow)": "W2 (LG-coherent transverse motion)", "LG-apex hemisphere": "LG-apex hemisphere (n.V_LG > 0)",
        "antapex hemisphere": "LG-antapex hemisphere (n.V_LG < 0)", "Galactic b > 0": "Galactic north (b > 0)", "Galactic b < 0": "Galactic south (b < 0)", "no tau softening": "no tau softening (tau = 0)",
        "no Birge scaling": "no Birge scaling"}
P("    systematics rows: beta (boot sigma; shuffle p) mine | CFG186")
for k, kk in smap.items():
    mk = [x for x in mj_c["ROWS"] if x.startswith(k)]
    if not mk or kk not in tj_b["systematics"]:
        continue
    m_ = mj_c["ROWS"][mk[0]]; t_ = tj_b["systematics"][kk]
    P("      %-34s %+7.3f (%.3f; p %.3f) | %+7.3f (%.3f; p %.3f)" % (k, m_["beta"], m_["boot_sigma"], m_.get("shuffle_p", float("nan")), t_["beta"], t_["sigma"], t_["p_shuffle"]))
P("      free dipole: beta %+.3f (boot %.3f), |D| %.3f | CFG186 +0.312 (0.613), |D| 0.411 (its text)" % (mj_c["ROWS"]["free sky dipole"]["beta"], mj_c["ROWS"]["free sky dipole"]["boot_sigma"], mj_c["ROWS"]["free sky dipole"]["Dmag"]))
P("      distance term: beta %+.3f gamma %+.3f | CFG186 +0.921, gamma +0.019 (its text)" % (mj_c["ROWS"]["distance term"]["beta"], mj_c["ROWS"]["distance term"]["gamma"]))
P("      jackknife range: [%+.3f, %+.3f] | CFG186 [+0.682, +1.288] (its text)" % (mj_c["ROWS"]["jackknife range"]["lo"], mj_c["ROWS"]["jackknife range"]["hi"]))

# ------------------------------------------------------------------ MUTATE comparison
mut = json.load(builtins.open(os.path.join(LANE, "cfg186_b_fit_results_MUTATE.json")))["numbers"]
P("    CFG186 MUTATE (beta = 0.30 injected): %s" % json.dumps(mut.get("M1_diagnostics", {}))[:400])
for k in (1, 2, 3, 4, 5, 6):
    j = json.load(builtins.open(os.path.join(HERE, "CFG193_c_fit_power_MUTATE%d_results.json" % k)))
    P("    my MU%d: beta_hat %+.3f; bites = %s" % (k, j["beta"], j["mutate_bites"]))

# ------------------------------------------------------------------ (6) attack (e): first vs second vs final
P("(6) ATTACK (e): CFG186 part A first run vs second run vs final")
ja = {}
for lab, f in (("first", "cfg186_a_curves_power_results_firstrun.json"), ("second", "cfg186_a_curves_power_results_secondrun.json"), ("final", "cfg186_a_curves_power_results.json")):
    ja[lab] = json.load(builtins.open(os.path.join(LANE, f)))["numbers"]
P("    %-28s %10s %10s %10s" % ("quantity", "first", "second", "final"))
def g3(fn, fmt):
    return "  ".join(fmt % fn(ja[k]) if fn(ja[k]) is not None else "  -  " for k in ("first", "second", "final"))
for lab, fn, fmt in (("N_primary", lambda d: d["N_primary"], "%10d"), ("z sd (W1)", lambda d: d["z_W1_catalogue"]["sd"], "%10.4f"), ("L0", lambda d: d["L0"], "%10.4f"), ("tau", lambda d: d["tau"], "%10.4f"),
                     ("median sigma_i", lambda d: d["primary_sigma_median"], "%10.4f"), ("Fisher sigma_beta W1", lambda d: d["power"]["W1_H67.66"]["sigma_fisher"], "%10.4f"),
                     ("mock sigma (beta=0)", lambda d: d["power"]["W1_H67.66"]["sigma_mock"], "%10.3f"), ("mock mean beta_hat", lambda d: d["power"]["W1_H67.66"]["mock_mean"], "%10.3f"),
                     ("mock median beta_hat", lambda d: d["power"]["W1_H67.66"].get("mock_median"), "%10.3f"), ("beta_det (2 sigma)", lambda d: d["power"]["W1_H67.66"]["beta_det_2sigma"], "%10.3f"),
                     ("tau without edge galaxies", lambda d: d.get("tau_without_edge_galaxies"), "%10.4f")):
    P("    %-28s %s" % (lab, g3(fn, fmt)))
jb = {}
for lab, f in (("first", "cfg186_b_fit_results_firstrun.json"), ("final", "cfg186_b_fit_results.json"), ("mut_first", "cfg186_b_fit_results_MUTATE_firstrun.json"), ("mut_final", "cfg186_b_fit_results_MUTATE.json")):
    jb[lab] = json.load(builtins.open(os.path.join(LANE, f)))["numbers"]
P("    part B: quantity | first-run | final | MUTATE first | MUTATE final")
for lab, fn, fmt in (("beta_hat", lambda d: d["primary"]["beta"], "%+.4f"), ("bootstrap sigma", lambda d: d["bootstrap"]["sigma"], "%.4f"), ("shuffle p (two-sided)", lambda d: d["nulls"]["perm"]["p_two"], "%.4f"),
                     ("noise p", lambda d: d["nulls"]["noise"]["p_two"], "%.4f"), ("beta95 quoted", lambda d: d.get("beta95_quoted", d["KM1"].get("beta95")) if "beta95_quoted" in d else None, "%.3f")):
    vals = []
    for k in ("first", "final", "mut_first", "mut_final"):
        try:
            x = fn(jb[k]); vals.append(fmt % x if x is not None else "-")
        except Exception:
            vals.append("-")
    P("      %-24s %s" % (lab, " | ".join(vals)))
R["attack_e"] = {k: dict(fisher=ja[k]["power"]["W1_H67.66"]["sigma_fisher"], tau=ja[k]["tau"], sig=ja[k]["primary_sigma_median"], mock_sigma=ja[k]["power"]["W1_H67.66"]["sigma_mock"], mock_mean=ja[k]["power"]["W1_H67.66"]["mock_mean"]) for k in ja}
jdump(R, os.path.join(HERE, "CFG193_compare_results.json"))
P("done")
sys.exit(0)
