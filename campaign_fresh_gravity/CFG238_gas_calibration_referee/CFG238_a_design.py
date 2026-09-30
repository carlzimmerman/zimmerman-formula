#!/usr/bin/env python3
"""CFG238 attack a: z slopes at fixed L_IR and whether the L_IR conditioning is selection-driven (frozen sections 5 D5-D8 and 6a). Exit 0."""
import sys
from scipy.stats import norm
from CFG238_common import *

outp, jp = out_paths("CFG238_a_design")
T = Tee(outp)
banner(T, "CFG238 attack a (design anatomy, overlap and sample-flag estimators, permutation nulls, power, selection mocks)")
EDGES = [10.5, 11.0, 11.5, 12.0, 12.5]
SW = {("ad", "aCO"): (0.056, 0.050), ("dax", "aCO"): (0.004, 0.072), ("xa", "aCO"): (-0.002, 0.066), ("dax", "XCI"): (-0.039, 0.080),
      ("xa", "XCI"): (-0.026, 0.064), ("xd", "XCI"): (-0.104, 0.066), ("ad", "kappaH"): (-0.056, 0.042), ("dax", "GDR"): (-0.025, 0.078), ("xd", "GDR"): (-0.084, 0.066)}
R = {}
LINES = []


def line(lid, ok, msg):
    LINES.append((lid, ok))
    T(f"  [{'PASS' if ok else 'MISS'}] {lid} {msg}")


def pinv_boot(X, y, B=10000, seed=238):
    rng = np.random.default_rng(seed)
    n, p = X.shape
    out = np.empty((B, p))
    i = 0
    while i < B:
        m = min(2000, B - i)
        idx = rng.integers(0, n, (m, n))
        Xb = X[idx]; yb = y[idx]
        A = np.einsum("bni,bnj->bij", Xb, Xb)
        r = np.einsum("bni,bn->bi", Xb, yb)
        out[i:i + m] = (np.linalg.pinv(A) @ r[..., None])[..., 0]
        i += m
    return out


def lbin(L):
    return np.digitize(L, EDGES)


def merge_bins(idx, minN):
    idx = idx.copy()
    changed = True
    while changed:
        changed = False
        u = sorted(set(idx.tolist()))
        for k, b in enumerate(u):
            if (idx == b).sum() < minN and len(u) > 1:
                tgt = u[k - 1] if k > 0 else u[k + 1]
                idx[idx == b] = tgt
                changed = True
                break
    return idx


def dummies(idx):
    u = sorted(set(idx.tolist()))
    return np.column_stack([(idx == b).astype(float) for b in u])


def rank_add(cols, base):
    X = base
    kept = []
    for nm, c in cols:
        if c.std() == 0:
            continue
        Xn = np.column_stack([X, c])
        if np.linalg.matrix_rank(Xn) > np.linalg.matrix_rank(X):
            X = Xn
            kept.append(nm)
    return X, kept


def fast_b(x, L, y, n_perm=None):
    pass


for combo in COMBOS:
    t, c = combo
    key = f"{t}:{c}"
    A = factor_arrays(t, c, "fb")
    m = np.isfinite(A["L"])
    z, x, L, y, F = A["z"][m], A["x"][m], A["L"][m], A["y"][m], A["F"][m]
    n = len(y)
    T(f"\n=== {key}  (N with L_IR, master-else-opt fallback: {n}; master-only N {np.isfinite(factor_arrays(t, c)['L']).sum()})")
    RR = {}
    # ---- 1 anatomy
    r_xL = float(np.corrcoef(x, L)[0, 1])
    Xl = np.column_stack([np.ones(n), L])
    bx, *_ = np.linalg.lstsq(Xl, x, rcond=None)
    R2 = 1 - ((x - Xl @ bx) ** 2).sum() / ((x - x.mean()) ** 2).sum()
    vif_L = 1 / (1 - R2)
    grp = np.where(z < 0.6, 0, np.where(z < 1.6, 1, 2))
    lb = lbin(L)
    tab = np.zeros((6, 3), int)
    for bi in range(6):
        for g in range(3):
            tab[bi, g] = int(((lb == bi) & (grp == g)).sum())
    ov = [bi for bi in range(6) if tab[bi, 0] >= 8 and tab[bi, 2] >= 8]
    lo_rng = (float(L[grp == 0].min()), float(L[grp == 0].max())) if (grp == 0).any() else None
    hi_rng = (float(L[grp == 2].min()), float(L[grp == 2].max())) if (grp == 2).any() else None
    T(f"  r(x, L_IR) {r_xL:+.3f}  VIF(x | L_IR) {vif_L:.2f}; L range z<0.6 {lo_rng}, z>=1.6 {hi_rng}")
    T("  L_IR bin x z-group counts (rows: <10.5,10.5-11,11-11.5,11.5-12,12-12.5,>=12.5; cols: z<0.6, 0.6-1.6, >=1.6): " + str(tab.tolist()))
    T(f"  overlap bins (>=8 at z<0.6 AND >=8 at z>=1.6): {ov}  (number {len(ov)})")
    RR.update(N=n, r_xL=r_xL, VIF_L=vif_L, table=tab.tolist(), overlap_bins=ov)
    # flags
    Fn = {k: int(F[:, i].sum()) for i, k in enumerate(FLAGS)}
    byz = {b: {k: int(F[(z >= lo) & (z < hi), i].sum()) for i, k in enumerate(FLAGS)} for b, lo, hi in BINS}
    T(f"  sample flags (rows): {Fn}; by z bin: {byz}")
    base = np.column_stack([np.ones(n), x, L - 11.7])
    Xf, kept = rank_add([(k, F[:, i]) for i, k in enumerate(FLAGS)], base)
    xo = np.column_stack([np.ones(n), L - 11.7] + [Xf[:, 3 + j] for j in range(len(kept))])
    bxo, *_ = np.linalg.lstsq(xo, x, rcond=None)
    vif_F = 1 / (1 - (1 - ((x - xo @ bxo) ** 2).sum() / ((x - x.mean()) ** 2).sum()))
    T(f"  flags kept after rank test: {kept}; VIF(x | L_IR + flags) {vif_F:.2f}")
    RR.update(flags_kept=kept, VIF_LF=vif_F)
    # ---- README-model slope on this row set
    w0 = slope_fit(dict(x=x, L=L, y=y), True, 10000, 238)
    tb, tsd = SW[combo]
    T(f"  README-model slope on this set: b {w0['b']:+.3f} +- {w0['b_boot_sd']:.3f} (README {tb:+.3f} +- {tsd}); {w0['b'] / w0['b_boot_sd']:+.2f} sigma")
    RR["b_readme_model"] = w0
    # ---- 2 overlap estimator
    if len(ov) >= 1:
        sel = np.isin(lb, ov)
        Xo = np.column_stack([dummies(lb[sel]), x[sel]])
        bo = pinv_boot(Xo, y[sel], 10000, 238)
        be, *_ = np.linalg.lstsq(Xo, y[sel], rcond=None)
        res = y[sel] - Xo @ be
        se_an = math.sqrt((res @ res) / (sel.sum() - Xo.shape[1]) * np.linalg.inv(Xo.T @ Xo)[-1, -1])
        b_ov, sd_ov = float(be[-1]), float(bo[:, -1].std(ddof=1))
        T(f"  overlap-bin FE estimator ({len(ov)} bins, N {int(sel.sum())}): b {b_ov:+.3f} boot SD {sd_ov:.3f} ({b_ov / sd_ov:+.2f} sigma); analytic SE {se_an:.3f}")
        # contrast estimator
        cons = []
        for bi in ov:
            a_ = y[(lb == bi) & (grp == 2)]; b_ = y[(lb == bi) & (grp == 0)]
            d_ = a_.mean() - b_.mean(); v_ = a_.var(ddof=1) / len(a_) + b_.var(ddof=1) / len(b_)
            dz = np.log10(1 + z[(lb == bi) & (grp == 2)]).mean() - np.log10(1 + z[(lb == bi) & (grp == 0)]).mean()
            cons.append((bi, d_, math.sqrt(v_), dz))
        wts = np.array([1 / s ** 2 for _, _, s, _ in cons]); dd = np.array([d for _, d, _, _ in cons])
        dcomb = float((wts * dd).sum() / wts.sum()); secomb = float(1 / math.sqrt(wts.sum()))
        dzm = float(np.mean([c_[3] for c_ in cons]))
        T(f"  contrast (z>=1.6 minus z<0.6) per overlap bin: " + "; ".join(f"bin{bi}: {d_:+.3f}+-{s_:.3f} (dx {dz_:.2f})" for bi, d_, s_, dz_ in cons))
        T(f"  inverse-variance combined contrast {dcomb:+.3f} +- {secomb:.3f} ({dcomb / secomb:+.2f} sigma); mean dx {dzm:.2f} -> slope-equivalent {dcomb / dzm:+.3f} +- {secomb / dzm:.3f}")
        RR["overlap"] = dict(b=b_ov, sd=sd_ov, N=int(sel.sum()), contrast=dcomb, contrast_se=secomb, dx=dzm, per_bin=cons)
    else:
        T("  no overlap bin: the fixed-luminosity comparison is an extrapolation of the linear L_IR term")
        RR["overlap"] = None
    # ---- 3 sample-flag estimator
    if kept:
        Xs_ = Xf
        bs = pinv_boot(Xs_, y, 10000, 238)
        bf, *_ = np.linalg.lstsq(Xs_, y, rcond=None)
        b_fl, sd_fl = float(bf[1]), float(bs[:, 1].std(ddof=1))
        T(f"  sample-flag estimator (L_IR + {kept}): b {b_fl:+.3f} boot SD {sd_fl:.3f} ({b_fl / sd_fl:+.2f} sigma)")
        RR["flag"] = dict(b=b_fl, sd=sd_fl, kept=kept)
    else:
        RR["flag"] = None
    # POST HOC (labelled, not frozen): within-SMG-flag rows at z >= 1.6, slope with L_IR
    msm = (F[:, FLAGS.index("SMG")] == 1) & (z >= 1.6)
    if msm.sum() >= 20:
        wsm = slope_fit(dict(x=x, L=L, y=y), True, 10000, 238, mask=msm)
        T(f"  POST HOC within SMG-flag rows at z >= 1.6 only (N {wsm['N']}, x spans {x[msm].min():.2f}-{x[msm].max():.2f}): slope with L_IR {wsm['b']:+.3f} +- {wsm['b_boot_sd']:.3f} ({wsm['b'] / wsm['b_boot_sd']:+.1f} sigma)")
        RR["within_smg"] = dict(N=wsm["N"], b=wsm["b"], sd=wsm["b_boot_sd"])
    # ---- 4 permutation nulls
    rng = np.random.default_rng(2382)
    NP = 5000
    lbm = merge_bins(lb, 3)
    xp = np.tile(x, (NP, 1))
    for bi in set(lbm.tolist()):
        ii = np.where(lbm == bi)[0]
        for k in range(NP):
            xp[k, ii] = x[rng.permutation(ii)]
    Lc = L - 11.7
    def batch_b(xpm):
        # OLS y ~ 1 + x_p + Lc, batch over permutations
        out = np.empty(len(xpm)); se = np.empty(len(xpm))
        for k in range(len(xpm)):
            X = np.column_stack([np.ones(n), xpm[k], Lc])
            XtXi = np.linalg.inv(X.T @ X)
            be_ = XtXi @ X.T @ y
            r_ = y - X @ be_
            out[k] = be_[1]; se[k] = math.sqrt(r_ @ r_ / (n - 3) * XtXi[1, 1])
        return out, se
    bnull, senull = batch_b(xp)
    rng = np.random.default_rng(2383)
    xg = np.array([x[rng.permutation(n)] for _ in range(NP)])
    bgl, segl = batch_b(xg)
    T(f"  permutation null within L_IR bins (5000, seed 2382): mean b {bnull.mean():+.4f} SD {bnull.std(ddof=1):.3f}; mean |b/SE|>2: {float((np.abs(bnull / senull) > 2).mean()):.3f}; README-set bootstrap SD {w0['b_boot_sd']:.3f}")
    T(f"  global shuffle null (seed 2383): mean b {bgl.mean():+.4f} SD {bgl.std(ddof=1):.3f}; |b/SE|>2: {float((np.abs(bgl / segl) > 2).mean()):.3f}")
    RR["perm"] = dict(mean=float(bnull.mean()), sd=float(bnull.std(ddof=1)), frac2=float((np.abs(bnull / senull) > 2).mean()), global_sd=float(bgl.std(ddof=1)), global_frac2=float((np.abs(bgl / segl) > 2).mean()))
    line(f"H-C3:{key}:mean", abs(bnull.mean()) <= 0.005, f"{key} permutation null mean {bnull.mean():+.4f}")
    line(f"H-C3:{key}:sd", abs(bnull.std(ddof=1) / w0["b_boot_sd"] - 1) <= 0.25, f"{key} null SD {bnull.std(ddof=1):.3f} vs bootstrap SD {w0['b_boot_sd']:.3f} (ratio {bnull.std(ddof=1) / w0['b_boot_sd']:.2f})")
    # ---- 5 power (D7)
    X3 = np.column_stack([np.ones(n), x, Lc])
    beta3, _, sres = ols(X3, y)
    lbm2 = merge_bins(lb, 5)
    Xg = np.column_stack([dummies(lbm2), x])
    XtXi3 = np.linalg.inv(X3.T @ X3); XtXig = np.linalg.inv(Xg.T @ Xg)
    se_b3 = math.sqrt(sres ** 2 * XtXi3[1, 1]); se_bg = math.sqrt(sres ** 2 * XtXig[-1, -1])
    BT = [0, 0.05, 0.10, 0.15, 0.20, 0.30]
    rng = np.random.default_rng(2381)
    K = 2000
    pw = {}
    for est, X_, XtXi_, pidx in (("README-model", X3, XtXi3, 1), ("grid-FE", Xg, XtXig, Xg.shape[1] - 1)):
        pw[est] = {}
        for bt in BT:
            mu = X3 @ np.array([beta3[0], bt, beta3[2]])
            Y = mu[:, None] + rng.normal(0, sres, (n, K))
            Bh = XtXi_ @ X_.T @ Y
            Rs = Y - X_ @ Bh
            s2 = (Rs ** 2).sum(0) / (n - X_.shape[1])
            tt = Bh[pidx] / np.sqrt(s2 * XtXi_[pidx, pidx])
            pw[est][bt] = dict(power=float((np.abs(tt) > 2).mean()), bmean=float(Bh[pidx].mean()), bsd=float(Bh[pidx].std()))
        ps = [pw[est][bt]["power"] for bt in BT]
        mdb = None
        for k in range(1, len(BT)):
            if ps[k] >= 0.8 > ps[k - 1]:
                mdb = BT[k - 1] + (0.8 - ps[k - 1]) / (ps[k] - ps[k - 1]) * (BT[k] - BT[k - 1])
        pw[est]["mdb80"] = mdb
        T(f"  power {est}: " + ", ".join(f"b={bt}: {pw[est][bt]['power']:.2f} (bhat {pw[est][bt]['bmean']:+.3f})" for bt in BT) + f"; min detectable b at 80% (interp) {mdb}")
    T(f"  analytic: SE(README model) {se_b3:.3f} -> 2.8 SE = {2.8 * se_b3:.3f}; SE(grid FE) {se_bg:.3f} -> 2.8 SE = {2.8 * se_bg:.3f}; residual SD {sres:.3f}")
    real = {}
    for dex in (0.05, 0.10, 0.15):
        bt = dex / 0.54
        real[dex] = float(norm.cdf(-1.96 + bt / se_b3) + norm.cdf(-1.96 - bt / se_b3))
    T("  power to see a real change of 0.05/0.10/0.15 dex across z=0->2.5 (b = dex/0.54, README model, analytic): " + ", ".join(f"{k}: {v:.2f}" for k, v in real.items()))
    RR["power"] = dict(pw=pw, se_b3=se_b3, se_bg=se_bg, real=real, sres=sres, mdb_an=2.8 * se_b3)
    # ---- 6 selection mocks (D8)
    sel_c = {}
    for c2 in (-0.06, -0.03, 0.0, 0.03, 0.06):
        yn = beta3[0] + beta3[2] * Lc + c2 * Lc ** 2
        b_lin = (XtXi3 @ X3.T @ yn)[1]
        b_grid = (XtXig @ Xg.T @ yn)[-1]
        Y = yn[:, None] + rng.normal(0, sres, (n, 2000))
        sd_lin = (XtXi3 @ X3.T @ Y)[1].std()
        sel_c[c2] = dict(b_lin=float(b_lin), b_grid=float(b_grid), sd_lin=float(sd_lin))
    T("  selection mock S1 (curvature c2 per dex^2, no z trend): " + "; ".join(f"c2={k:+.2f}: b_lin {v['b_lin']:+.3f}, b_grid {v['b_grid']:+.3f}" for k, v in sel_c.items()) + f"   (README SE {w0['b_boot_sd']:.3f})")
    smg = F[:, FLAGS.index("SMG")] == 1
    sel_s = {}
    for dl in (0, 0.05, 0.10, 0.15):
        yn = beta3[0] + beta3[2] * Lc + dl * smg
        b_with = (XtXi3 @ X3.T @ yn)[1]
        X2 = np.column_stack([np.ones(n), x]); b_wo = (np.linalg.inv(X2.T @ X2) @ X2.T @ yn)[1]
        sel_s[dl] = dict(b_with=float(b_with), b_without=float(b_wo))
    T(f"  selection mock S2 (offset on SMG-flag rows, N SMG {int(smg.sum())} of {n}): " + "; ".join(f"delta={k}: b_with {v['b_with']:+.3f}, b_without {v['b_without']:+.3f}" for k, v in sel_s.items()))
    RR["sel"] = dict(curv=sel_c, samp=sel_s, nsmg=int(smg.sum()))
    R[key] = RR
    # ---- pass lines for estimates
    line(f"H-C5:{key}", max(abs(sel_c[-0.05 if False else -0.06]["b_lin"]), abs(sel_c[0.06]["b_lin"])) > 0.5 * w0["b_boot_sd"], f"curvature |b_lin| at c2=+-0.06: {abs(sel_c[-0.06]['b_lin']):.3f}/{abs(sel_c[0.06]['b_lin']):.3f} > 0.5 SE {0.5 * w0['b_boot_sd']:.3f} (expected, P 0.45)")
    line(f"H-C6:{key}", 0.05 <= abs(sel_s[0.05]["b_with"]) <= 0.20 or 0.05 <= abs(sel_s[0.10]["b_with"]) <= 0.40, f"sample offset 0.05 -> spurious b_with {sel_s[0.05]['b_with']:+.3f}; 0.10 -> {sel_s[0.10]['b_with']:+.3f} (hand estimate ~0.10 for 0.05 dex)")

# ================================================================== summary
T("\n== Summary of attack a")
nsig_ov = []
for key, RR in R.items():
    if not isinstance(RR, dict):
        continue
    ov_ = RR.get("overlap"); fl_ = RR.get("flag")
    s1 = f"{ov_['b'] / ov_['sd']:+.2f}" if ov_ else "n/a"
    s2 = f"{fl_['b'] / fl_['sd']:+.2f}" if fl_ else "n/a"
    T(f"  {key}: overlap bins {len(RR['overlap_bins'])}; overlap-FE b/SD {s1}; flag-estimator b/SD {s2}; README-model {RR['b_readme_model']['b'] / RR['b_readme_model']['b_boot_sd']:+.2f}; MDB80 (README model, grid) {RR['power']['pw']['README-model']['mdb80']}, {RR['power']['pw']['grid-FE']['mdb80']}; analytic 2.8SE {RR['power']['mdb_an']:.3f}")
    if ov_:
        nsig_ov.append(abs(ov_["b"] / ov_["sd"]))
    if fl_:
        nsig_ov.append(abs(fl_["b"] / fl_["sd"]))
T(f"  disagreement (i): any overlap or flag estimator >= 2 SD from zero: {any(v >= 2 for v in nsig_ov)} (max {max(nsig_ov):.2f})")
ov_counts = {k: len(v['overlap_bins']) for k, v in R.items() if isinstance(v, dict)}
T(f"  overlap-bin counts per (table:factor): {ov_counts}")
T(f"  disagreement (iii): fewer than two overlap bins in: {[k for k, v in ov_counts.items() if v < 2]}")
# estimate lines
a = R["ad:aCO"]
line("H-C1", len(a["overlap_bins"]) == 2, f"ad alpha_CO overlap bins {len(a['overlap_bins'])} (estimate 2, P 0.45)")
ovd = a["overlap"]
line("H-C2a", ovd is not None and abs(ovd["b"] / ovd["sd"]) < 2, f"ad alpha_CO overlap-FE consistent with 0 at 2 sigma: {ovd['b']:+.3f} +- {ovd['sd']:.3f}" if ovd else "no overlap")
line("H-C2b", ovd is not None and ovd["sd"] >= 1.3 * 0.050, f"overlap SE {ovd['sd']:.3f} >= 1.3 x 0.050" if ovd else "no overlap")
line("H-C4a", abs(a["power"]["mdb_an"] - 0.14) <= 0.035, f"ad alpha_CO min detectable (2.8 SE) {a['power']['mdb_an']:.3f} vs 0.14")
line("H-C4b", all(0.15 <= R[k]["power"]["mdb_an"] <= 0.25 for k in ("dax:aCO", "xa:aCO", "xa:XCI", "xd:XCI", "dax:XCI")), "daX/xa/xd min detectable in [0.15, 0.25]: " + str({k: round(R[k]["power"]["mdb_an"], 3) for k in ("dax:aCO", "xa:aCO", "xa:XCI", "xd:XCI", "dax:XCI")}))
line("H-C4c", abs(a["power"]["real"][0.05] - 0.45) <= 0.15, f"ad alpha_CO power for a 0.05 dex change across z 0->2.5: {a['power']['real'][0.05]:.2f} (estimate 0.45)")
R["lines"] = LINES
dump(jp, R)
T.close()
sys.exit(0)
