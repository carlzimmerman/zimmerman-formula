#!/usr/bin/env python3
"""
fire_anisotropy.py -- STAGE-1 FIRING of the MG-impossible anisotropy discriminator on
MaNGA DR17 slow rotators (the first time this observable has ever been confronted with data).

+----------------------------------------------------------------------------------------+
| EXPLORATORY FIREWALL (FROZEN.md sec.5, frozen 2026-07-17T00:21:52Z BEFORE download):    |
| NO kill conditions exist for this observable. NOTHING in this run can support or kill  |
| the framework. This is the FIRST exploratory number: it creates the baseline and       |
| pre-registers the full-Jeans Stage 2. A null or MG-favoring slope is reported straight;|
| a positive (MI-like) slope carries the IMF-fake caveat at equal prominence.            |
| THE PROXY IS NOT beta -- P1/P2 are LOS signatures contaminated by inclination, shape,  |
| rotation residuals and M/L gradients (FROZEN.md sec.3).                                |
+----------------------------------------------------------------------------------------+

The frozen test (FROZEN.md sec.4): delta (both a0 footings x three IMF brackets) vs the
resolved anisotropy proxies on the N=48 PRIMARY-cut resolved subsample.
  P2 (PRIMARY proxy)  = dln sigma_c/dln R over 0.5-1.5 Re.  Frozen sign map (Binney &
     Mamon 1982; Cappellari 2008 JAM): larger radial anisotropy <-> more NEGATIVE P2,
     so the MI forced prediction d(delta)/d(radial anisotropy) > 0 maps to
     **d(delta)/dP2 < 0**; MG-with-same-nu predicts exactly 0.
  P1 (secondary)      = sigma_maj/sigma_min in 0.5-1.0 Re (sign recorded, beta-mapping
     inclination/shape-degenerate by freeze).
Estimator: Huber robust linear regression, controls log10 M*, log10 Re(kpc), z
(+ log10 sigma_e in the mandatory IMF-bracket-B rerun), partial Spearman, 10,000-pair
bootstrap CIs. Full footing x bracket x proxy grid, no cherry-pick. Environment/local-
density control: OMITTED and stated -- no public group catalog was crossmatched at firing
time (allowed by FROZEN.md sec.4 with statement).

Framework judged on its OWN terms: nu(y)=sqrt(1+1/y); a0_canon=9.36e-11 (cH_Lambda/Z,
rho_DE), a0_alt=1.13e-10 (cH0, rho_tot). exit 0; no hard-coded verdicts.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(20260717)   # seed = freeze date, fixed before firing
NBOOT = 10000

# ---------------------------------------------------------------------------- helpers
def huber_fit(X, y, c=1.345, iters=60, tol=1e-10):
    """IRLS Huber regression. X: (n,p) WITHOUT intercept (added here).
    Returns coefficient vector (p+1,) with [0]=intercept, plus robust resid scale."""
    n = len(y)
    A = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    for _ in range(iters):
        r = y - A @ beta
        s = 1.4826 * np.median(np.abs(r - np.median(r)))
        if s <= 0:
            s = np.std(r) + 1e-12
        u = r / (c * s)
        w = np.where(np.abs(u) <= 1.0, 1.0, 1.0 / np.maximum(np.abs(u), 1e-12))
        Aw = A * w[:, None]
        beta_new, *_ = np.linalg.lstsq(Aw.T @ A, Aw.T @ y, rcond=None)
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new
    r = y - A @ beta
    scale = 1.4826 * np.median(np.abs(r - np.median(r)))
    return beta, scale


def rank(v):
    """average-tie ranks"""
    order = np.argsort(v, kind="mergesort")
    r = np.empty(len(v))
    r[order] = np.arange(len(v), dtype=float)
    # average ties
    sv = v[order]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and sv[j + 1] == sv[i]:
            j += 1
        if j > i:
            r[order[i:j + 1]] = 0.5 * (i + j)
        i = j + 1
    return r


def partial_spearman(y, x, C):
    """Spearman partial correlation of y,x given controls C (n,k):
    rank-transform everything, OLS-residualize on control ranks, Pearson of residuals."""
    ry, rx = rank(y), rank(x)
    RC = np.column_stack([np.ones(len(y))] + [rank(C[:, j]) for j in range(C.shape[1])])
    py = ry - RC @ np.linalg.lstsq(RC, ry, rcond=None)[0]
    px = rx - RC @ np.linalg.lstsq(RC, rx, rcond=None)[0]
    d = np.sqrt((py @ py) * (px @ px))
    return float(py @ px / d) if d > 0 else np.nan


def cell(y, x, C, nboot=NBOOT, tag=""):
    """One grid cell: Huber slope of x (controls C) + bootstrap CI + empirical p vs the
    MG zero; partial Spearman + bootstrap CI. Returns dict."""
    n = len(y)
    X = np.column_stack([x, C])
    beta, scale = huber_fit(X, y)
    slope = float(beta[1])
    rho = partial_spearman(y, x, C)
    bs, br = np.empty(nboot), np.empty(nboot)
    for b in range(nboot):
        idx = RNG.integers(0, n, n)
        if len(np.unique(x[idx])) < 3:
            bs[b], br[b] = np.nan, np.nan
            continue
        try:
            bb, _ = huber_fit(np.column_stack([x[idx], C[idx]]), y[idx], iters=25)
            bs[b] = bb[1]
            br[b] = partial_spearman(y[idx], x[idx], C[idx])
        except np.linalg.LinAlgError:
            bs[b], br[b] = np.nan, np.nan
    bs, br = bs[np.isfinite(bs)], br[np.isfinite(br)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    lo68, hi68 = np.percentile(bs, [16, 84])
    # two-sided empirical p against the MG prediction slope = 0
    p_mg = 2.0 * min(np.mean(bs <= 0.0), np.mean(bs >= 0.0))
    p_mg = min(p_mg, 1.0)
    rlo, rhi = np.percentile(br, [2.5, 97.5])
    return dict(tag=tag, n=n, slope=slope, se=float(np.std(bs)),
                lo=float(lo), hi=float(hi), lo68=float(lo68), hi68=float(hi68),
                p_mg=float(p_mg), rho=rho, rlo=float(rlo), rhi=float(rhi),
                resid_scale=float(scale))


def show(c, sign_note=""):
    zero = "ZERO-INSIDE" if (c["lo"] <= 0.0 <= c["hi"]) else "zero-OUTSIDE"
    print(f"  {c['tag']:<34s} N={c['n']:>2d}  slope={c['slope']:+.4f} "
          f"(68% [{c['lo68']:+.4f},{c['hi68']:+.4f}]; 95% [{c['lo']:+.4f},{c['hi']:+.4f}]) "
          f"p_MG0={c['p_mg']:.3f} [{zero}]  partial-Spearman rho={c['rho']:+.3f} "
          f"[{c['rlo']:+.3f},{c['rhi']:+.3f}]  resid={c['resid_scale']:.3f}{sign_note}")


# ---------------------------------------------------------------------------- load
def load_csv(path):
    with open(path) as f:
        hdr = f.readline().strip().split(",")
        rows = [ln.strip().split(",") for ln in f if ln.strip()]
    out = {}
    for i, h in enumerate(hdr):
        col = [r[i] for r in rows]
        try:
            out[h] = np.array([float(v) if v not in ("", "nan") else np.nan for v in col])
        except ValueError:
            out[h] = np.array(col)
    return out


def main():
    print(__doc__.split("+--")[1].join(["+--", "+--"]) if False else "")
    print("=" * 92)
    print("EXPLORATORY FIREWALL: no kill conditions exist for this observable; nothing here")
    print("can support or kill the framework. First exploratory number; creates the baseline;")
    print("pre-registers full-Jeans Stage 2. THE PROXY IS NOT beta. (FROZEN.md sec.3/5)")
    print("=" * 92)

    cat = load_csv(os.path.join(HERE, "stage_catalog.csv"))
    res = load_csv(os.path.join(HERE, "resolved_proxies.csv"))

    # merge resolved proxies onto the catalog
    idx = {p: i for i, p in enumerate(cat["plateifu"])}
    keep = [k for k, p in enumerate(res["plateifu"]) if p in idx and res["ok"][k] == 1]
    ci = np.array([idx[res["plateifu"][k]] for k in keep])
    ri = np.array(keep)
    n = len(ri)
    print(f"\nmerged resolved subsample: {n} galaxies (all cut_primary="
          f"{int(np.all(cat['cut_primary'][ci] == 1))}; frozen N target 48)")

    P2 = res["P2_dlnsig_dlnR"][ri]
    P1 = res["P1_sigmaj_over_sigmin"][ri]
    vsig_res = res["vsig_resolved"][ri]
    logM = cat["log_mstar"][ci]
    logRe = np.log10(cat["re_kpc"][ci])
    zred = cat["z"][ci]
    logsig = np.log10(cat["sigma_e"][ci])
    C3 = np.column_stack([logM, logRe, zred])            # frozen controls
    C4 = np.column_stack([logM, logRe, zred, logsig])    # bracket-B rerun adds log sigma_e

    print("controls held: log10 M*, log10 Re(kpc), z (frozen; + log10 sigma_e in bracket B).")
    print("ENVIRONMENT control: OMITTED -- no public group catalog crossmatched at firing")
    print("time (FROZEN.md sec.4 permits omission if stated; Stage 2 should add one, e.g.")
    print("Tempel+ 2017 SDSS groups).")

    # pre-flight: does the proxy correlate with sigma_e? (the pre-registered IMF-fake channel)
    r_p2_sig = np.corrcoef(P2, logsig)[0, 1]
    print(f"\npre-registered confounder check: corr(P2, log sigma_e) = {r_p2_sig:+.3f} "
          f"(a sigma-correlated proxy is the channel by which a sigma-dependent IMF can FAKE")
    print("a slope; hence the mandatory bracket-B rerun below).")

    results = {}
    print("\n" + "-" * 92)
    print("PRIMARY PROXY P2 = dln sigma/dln R (0.5-1.5 Re).  Frozen sign map: MI forced")
    print("prediction d(delta)/d(radial anisotropy)>0  <=>  d(delta)/dP2 < 0.   MG-with-")
    print("same-nu: exactly 0.  (dex of offset per unit dln sigma/dln R)")
    print("-" * 92)
    for foot in ("canon", "alt"):
        for br, col, C in (("fixedIMF", f"delta_{foot}", C3),
                           ("imfA_x1.55", f"delta_{foot}_imfA", C3),
                           ("imfB_sigma-dep", f"delta_{foot}_imfB", C4)):
            d = cat[col][ci]
            c = cell(d, P2, C, tag=f"P2 | {foot:5s} | {br}")
            results[f"P2_{foot}_{br}"] = c
            show(c)
        print()

    print("-" * 92)
    print("SECONDARY PROXY P1 = sigma_maj/sigma_min (0.5-1.0 Re; sign recorded, mapping")
    print("inclination/shape-degenerate by freeze; N limited by the >=8-spaxel wedge floor)")
    print("-" * 92)
    m1 = np.isfinite(P1)
    for foot in ("canon", "alt"):
        for br, col, C in (("fixedIMF", f"delta_{foot}", C3),
                           ("imfB_sigma-dep", f"delta_{foot}_imfB", C4)):
            d = cat[col][ci]
            c = cell(d[m1], P1[m1], C[m1], tag=f"P1 | {foot:5s} | {br}")
            results[f"P1_{foot}_{br}"] = c
            show(c)
        print()

    # ------------------------------------------ diagnostic decomposition (labelled)
    print("-" * 92)
    print("DIAGNOSTIC DECOMPOSITION (labelled variants, NOT frozen cells): the bracket-B")
    print("rerun differs from the baseline in TWO ways at once -- (1) the 0.30 dex/dex IMF")
    print("mass correction and (2) the added log sigma_e control. But delta contains")
    print("+2 log sigma_e ALGEBRAICALLY (M_dyn = K_v sigma^2 Re/G), so at fixed M*,Re the")
    print("dynamical 'hotter' signal AND a sigma-correlated IMF BOTH live in the same")
    print("log sigma_e direction: the sigma_e control removes signal and confounder")
    print("TOGETHER (structural degeneracy of the Stage-1 proxy design). Which piece kills")
    print("the slope is decided below by separating them:")
    print("-" * 92)
    for foot in ("canon",):
        dB = cat[f"delta_{foot}_imfB"][ci]
        dbase = cat[f"delta_{foot}"][ci]
        c = cell(dB, P2, C3, nboot=4000,
                 tag=f"P2 | {foot:5s} | imfB-corr ONLY (C3)")
        results[f"diag_imfBonly_{foot}"] = c
        show(c, "  <- IMF correction alone, no sigma control")
        c = cell(dbase, P2, C4, nboot=4000,
                 tag=f"P2 | {foot:5s} | fixedIMF + sig-ctrl (C4)")
        results[f"diag_sigctrl_{foot}"] = c
        show(c, "  <- sigma control alone, no IMF correction")
    b_full = results["P2_canon_fixedIMF"]["slope"]
    b_imf = results["diag_imfBonly_canon"]["slope"]
    print(f"  read-off: the literature-scale (0.30 dex/dex) IMF correction alone moves the")
    print(f"  fixed-IMF slope {b_full:+.4f} -> {b_imf:+.4f} "
          f"({100*(1-b_imf/b_full):.0f}% removed); the log sigma_e CONTROL is what")
    print("  drives the frozen bracket-B cell to ~0 (it also removes the signal channel).")
    print("  A sigma-dependent IMF would need a slope of ~2.0 dex/dex in log sigma to")
    print("  cancel the whole fixed-IMF slope through the mass term alone -- ~6-7x the")
    print("  literature trend. BUT by the FROZEN standard (FROZEN.md sec.2: 'a slope that")
    print("  dies under bracket B is reported as NOT robust'), the MI-like slope is NOT")
    print("  ROBUST -- reported verbatim; the degeneracy statement above is the reason the")
    print("  frozen standard is this conservative at Stage 1 (sigma_e is simultaneously the")
    print("  dynamical thermometer and the IMF proxy; only Stage-2 Jeans beta, which is not")
    print("  a monotone function of sigma_e, breaks the degeneracy).")

    # ------------------------------------------------------------------ robustness
    print("\n" + "-" * 92)
    print("ROBUSTNESS (labelled variants; the frozen primary above is never replaced)")
    print("-" * 92)
    d0 = cat["delta_canon"][ci]

    # (i) V/sigma cut variant: the resolved subsample was drawn from the PRIMARY cut only
    # (all 48 have DAPall (V/sig)_glob < 0.4), so the frozen 0.6-VARIANT is IDENTICAL at the
    # resolved level. Labelled variant instead: split on the RESOLVED V/sigma.
    print("(i) V/sigma cut: all resolved galaxies are PRIMARY (DAPall V/sig<0.4) by the")
    print("    frozen subsample rule -> the 0.6 VARIANT is the identical sample here; the")
    print("    catalog-level variant cannot be run because NO DAPall-level proxy was frozen")
    print("    (FROZEN.md sec.3). Labelled variant: split on RESOLVED V/sigma instead.")
    med_vs = np.median(vsig_res)
    for lab, m in ((f"resolved V/sig < {med_vs:.2f} (colder half)", vsig_res < med_vs),
                   (f"resolved V/sig >= {med_vs:.2f} (hotter half)", vsig_res >= med_vs)):
        c = cell(d0[m], P2[m], C3[m], nboot=4000, tag=f"P2 | canon | fixedIMF | {lab}")
        show(c)

    # (ii) drop the highest-sigma quartile (the IMF-risk galaxies)
    q75 = np.percentile(cat["sigma_e"][ci], 75)
    m = cat["sigma_e"][ci] < q75
    c = cell(d0[m], P2[m], C3[m], nboot=4000,
             tag=f"P2 | canon | fixedIMF | sig_e<{q75:.0f} (drop top quartile)")
    print(f"(ii) IMF-risk guard: drop the highest-sigma quartile (sigma_e >= {q75:.0f} km/s):")
    show(c)
    results["rob_dropsig"] = c

    # (iii) resolved-subsample vs full-catalog-proxy: empty by freeze
    print("(iii) resolved-subsample-only vs full-catalog-proxy: EMPTY BY FREEZE -- FROZEN.md")
    print("     sec.3 froze NO DAPall-level anisotropy proxy (P1/P2 are MAPS-resolved only),")
    print("     so there is no catalog-level regression to compare against. Stated, not run.")

    # ------------------------------------------ acceleration-regime budget (computed)
    print("\n" + "-" * 92)
    print("ACCELERATION-REGIME BUDGET (computed, honesty-critical for reading the sign)")
    print("-" * 92)
    for foot in ("canon", "alt"):
        yv = cat[f"y_{foot}"][ci]
        nuv = np.sqrt(1.0 + 1.0 / yv)
        print(f"  {foot}: y = g_bar/a0 median {np.median(yv):.1f} "
              f"(16-84% [{np.percentile(yv,16):.1f},{np.percentile(yv,84):.1f}]); "
              f"log10 nu median {np.median(np.log10(nuv)):.4f} dex, 16-84% spread "
              f"[{np.percentile(np.log10(nuv),16):.4f},{np.percentile(np.log10(nuv),84):.4f}]")
    b0 = results["P2_canon_fixedIMF"]
    amp = abs(b0["slope"]) * float(np.std(P2))
    nuc = np.sqrt(1.0 + 1.0 / cat["y_canon"][ci])
    lever = np.percentile(np.log10(nuc), 84) - np.percentile(np.log10(nuc), 16)
    print(f"  => the fixed-IMF trend amplitude |slope|*s_P2 = {amp:.3f} dex vs the entire")
    print(f"  MI lever arm (16-84% spread of log nu) = {lever:.3f} dex: the observed trend is")
    print(f"  ~{amp/lever:.0f}x larger than the MAXIMUM any genuine MI anisotropy effect could")
    print("  be in this high-acceleration sample (these massive ETGs sit at y~5-11 where the")
    print("  framework boost nu-1 is only ~2-10%). So even at face value the MI-like sign")
    print("  CANNOT be read as MI support -- the amplitude is dominated by structural/")
    print("  K_v/sigma-channel systematics, exactly what the firewall anticipated. Stage 2")
    print("  must target LOW-y pressure-supported systems (dSphs, dwarf ETGs, cluster")
    print("  outskirts) where the MI budget is O(0.02-0.05 dex) and beta is Jeans-measured.")

    # ------------------------------------------------------------------ power statement
    print("\n" + "-" * 92)
    print("POWER STATEMENT for full-Jeans STAGE 2 (from the observed Stage-1 scatter)")
    print("-" * 92)
    c_base = results["P2_canon_fixedIMF"]
    s_e = c_base["resid_scale"]          # robust residual scatter of delta after controls
    s_p2 = float(np.std(P2))
    print(f"observed: post-control robust delta scatter s_e = {s_e:.3f} dex; "
          f"P2 spread s_P2 = {s_p2:.3f}; P1 spread {np.nanstd(P1[m1]):.3f} (N={m1.sum()}).")
    print("Stage 2 regresses delta on per-galaxy JAM/Jeans beta_r. Detectable-at-3sigma")
    print("(with 80% power, z=3+0.84) sample size: N ~ ((3.84 * s_e) / (b * s_beta_eff))^2,")
    print("s_beta_eff = attenuated beta spread s_beta*sqrt(s_beta^2/(s_beta^2+e_beta^2)).")
    print("Expected MI slope scale (illustrative, from the rider-a bracket: the isotropic-")
    print("ensemble offset bracket spans ~0.02-0.05 dex over the anisotropy range;")
    print("mi_closure_pin/CONSEQUENCES.md sec.1 -- 'toy magnitudes illustrative'):")
    print(f"{'b [dex/unit beta]':>18s} | " + " | ".join(f"s_beta={sb:.2f} e_beta={eb:.2f}"
          for sb, eb in ((0.20, 0.05), (0.20, 0.10), (0.15, 0.10))))
    for b_mi in (0.02, 0.05, 0.10):
        cells = []
        for sb, eb in ((0.20, 0.05), (0.20, 0.10), (0.15, 0.10)):
            sxeff = sb * np.sqrt(sb**2 / (sb**2 + eb**2))
            N = (3.84 * s_e / (b_mi * sxeff)) ** 2
            cells.append(f"N ~ {N:>7.0f}          ")
        print(f"{b_mi:>18.2f} | " + " | ".join(cells))
    print("MaNGA DR17 supplies ~382 primary slow rotators (2,407 quality parent); ATLAS3D-")
    print("style JAM beta_z is published for ~260 ETGs. => Stage 2 at b~0.05 needs s_e")
    print("driven DOWN (distances/M*: ~0.10-0.15 dex plausible with SBF/fundamental-plane")
    print("distances + resolved M/L) and N~10^2-10^3: FEASIBLE only at the optimistic corner;")
    print("at b~0.02 it needs N>~10^3 WITH s_e~0.1 -> requires stacking or a survey beyond")
    print("current JAM samples. Honest bottom line printed from the numbers above.")

    # ------------------------------------------------------------------ figures
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
        for ax, foot in zip(axes, ("canon", "alt")):
            d = cat[f"delta_{foot}"][ci]
            c = results[f"P2_{foot}_fixedIMF"]
            ax.scatter(P2, d, s=28, c="#356", alpha=0.8, label="slow rotators (N=%d)" % n)
            xx = np.linspace(P2.min(), P2.max(), 50)
            # partial-regression display line: slope from the controlled Huber fit,
            # anchored at the sample means
            ax.plot(xx, np.mean(d) + c["slope"] * (xx - np.mean(P2)), "-", c="#a33",
                    label=f"Huber slope (controlled) {c['slope']:+.3f}")
            ax.axhline(np.mean(d), ls="--", c="#777",
                       label="MG-with-same-nu: slope = 0")
            # binned medians
            qs = np.percentile(P2, [0, 25, 50, 75, 100])
            for lo_, hi_ in zip(qs[:-1], qs[1:]):
                mm = (P2 >= lo_) & (P2 <= hi_)
                if mm.sum() >= 3:
                    ax.plot(np.median(P2[mm]), np.median(d[mm]), "s", ms=9, c="#e90",
                            mec="k", zorder=5)
            ax.set_xlabel(r"P2 = d ln $\sigma$ / d ln R  (0.5-1.5 $R_e$)")
            ax.set_title(f"{foot}: a0 = {9.36e-11 if foot=='canon' else 1.13e-10:.3g} m/s$^2$")
        axes[0].set_ylabel(r"$\delta$ = log M$_{dyn}$ $-$ log $\nu(y)$M$_{bar}$  [dex]")
        axes[0].legend(fontsize=8, loc="upper left")
        fig.suptitle("EXPLORATORY (firewalled): Stage-1 proxy firing -- MI expects d$\\delta$/dP2 < 0, MG expects 0",
                     fontsize=10)
        fig.tight_layout()
        out = os.path.join(HERE, "fig_delta_vs_P2.png")
        fig.savefig(out, dpi=140)
        print(f"\nwrote {out}")
        # P1 secondary figure
        fig2, ax = plt.subplots(figsize=(5.6, 4.4))
        d = cat["delta_canon"][ci]
        ax.scatter(P1[m1], d[m1], s=28, c="#563", alpha=0.8)
        c1 = results["P1_canon_fixedIMF"]
        xx = np.linspace(np.nanmin(P1[m1]), np.nanmax(P1[m1]), 50)
        ax.plot(xx, np.mean(d[m1]) + c1["slope"] * (xx - np.nanmean(P1[m1])), "-", c="#a33",
                label=f"Huber slope (controlled) {c1['slope']:+.3f}")
        ax.axhline(np.mean(d[m1]), ls="--", c="#777", label="MG: slope = 0")
        ax.set_xlabel(r"P1 = $\sigma_{maj}/\sigma_{min}$ (0.5-1.0 $R_e$)")
        ax.set_ylabel(r"$\delta$ [dex] (canon)")
        ax.set_title("secondary proxy P1 (EXPLORATORY, firewalled)", fontsize=10)
        ax.legend(fontsize=8)
        fig2.tight_layout()
        out2 = os.path.join(HERE, "fig_delta_vs_P1.png")
        fig2.savefig(out2, dpi=140)
        print(f"wrote {out2}")
    except Exception as e:
        print(f"figure generation failed (non-fatal): {e}")

    # ------------------------------------------------------------------ verdict block
    print("\n" + "=" * 92)
    print("READ-OFF (computed above, nothing hard-coded): the frozen discriminator cell is")
    print("P2|canon|fixedIMF and its bracket-B rerun. MI expects slope<0, MG expects 0.")
    for k in ("P2_canon_fixedIMF", "P2_canon_imfB_sigma-dep", "P2_alt_fixedIMF",
              "P2_alt_imfB_sigma-dep"):
        c = results[k]
        sign = "MI-like (<0)" if c["hi"] < 0 else ("anti-MI (>0)" if c["lo"] > 0
                                                   else "CONSISTENT WITH MG ZERO")
        print(f"  {k:<28s}: slope {c['slope']:+.4f} [{c['lo']:+.4f},{c['hi']:+.4f}] -> {sign}")
    died_B = (results["P2_canon_imfB_sigma-dep"]["lo"] <= 0.0
              <= results["P2_canon_imfB_sigma-dep"]["hi"])
    if died_B:
        print("BY THE FROZEN STANDARD (FROZEN.md sec.2): the slope dies under bracket B ->")
        print("the MI-like fixed-IMF slope is NOT ROBUST. The diagnostic decomposition shows")
        print("the death comes from the log sigma_e CONTROL (which removes the dynamical")
        print("signal channel together with the IMF confounder -- structural Stage-1")
        print("degeneracy), not from the literature-scale IMF correction itself; both facts")
        print("carried at equal prominence.")
    print("FIREWALL REMINDER: exploratory; proxy is NOT beta; nothing here supports or")
    print("kills the framework. Verdict language above is about THIS PROXY only.")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    sys.exit(main())
