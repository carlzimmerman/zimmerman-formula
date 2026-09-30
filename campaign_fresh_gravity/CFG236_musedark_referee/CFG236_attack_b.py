"""CFG236 attack (b): is true_Vrot's v_kms v_perp or a projected velocity; the asymmetric-drift term.  B1-B5 of the frozen criteria.
Needs the external .dat files ([DAT]); B4 (CSV only) always runs.  Seed 2361."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

SEED = 2361
B = 2000
o = c.Out("attack_b")
c.header(o, "CFG236 attack (b): velocity column and drift term")
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
sini = np.sin(np.radians(C["incl"]))
DAT = c.dat_available()
R198 = c.routes(C)
rng = np.random.default_rng(SEED)


def ols_boot(x, y, B_, seed):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    r = np.random.default_rng(seed)
    n = len(x)
    bb = np.empty(B_)
    for t in range(B_):
        i = r.integers(0, n, n)
        bb[t] = np.polyfit(x[i], y[i], 1)[0]
    return float(np.polyfit(x, y, 1)[0]), c.ci(bb)


def score_readings(label, vobs, sig, vref, Rfac, tag):
    """vobs: observed file v at the radius; vref: reference v_c (km/s); Rfac = r/r_d at that radius."""
    sAD1 = 0.92 * Rfac * sig ** 2 / vref ** 2
    sAD2 = np.full(vobs.shape, 0.92 * 0.15 ** 2 * Rfac)
    res = {}
    lr = np.log10(vobs / vref)
    lsi = np.log10(sini)
    for name, (pred, nm) in {
        "(a) v_perp, drift D1": (np.sqrt(np.where(sAD1 < 1, 1 - sAD1, np.nan)), 1),
        "(a) v_perp, drift D2": (np.sqrt(1 - sAD2), 2),
        "(b) projected": (sini, 0),
        "(c) projected + drift D1": (sini * np.sqrt(np.where(sAD1 < 1, 1 - sAD1, np.nan)), 1),
        "(c) projected + drift D2": (sini * np.sqrt(1 - sAD2), 2),
        "(d) already v_c": (np.ones_like(vobs), 0)}.items():
        r = lr - np.log10(pred)
        m = np.isfinite(r)
        sl, cl = ols_boot(lsi, r, B, SEED)
        res[name] = dict(n=int(m.sum()), median=float(np.nanmedian(r)), mad=float(np.nanmedian(np.abs(r - np.nanmedian(r)))),
                         med_abs=float(np.nanmedian(np.abs(r))), slope_sini=sl, slope_ci=cl,
                         slope_null=bool(cl[0] <= 0 <= cl[1]))
        o.P(f"   {tag} {name:28s} n={res[name]['n']:3d} median resid {res[name]['median']:+.3f}  median|r| {res[name]['med_abs']:.3f}  MAD {res[name]['mad']:.3f}  slope vs log sin i {sl:+.2f} [{cl[0]:+.2f},{cl[1]:+.2f}]")
    okc = {k: v for k, v in res.items() if v["slope_null"]}
    if okc:
        best = min(okc, key=lambda k: okc[k]["med_abs"])
        second = sorted(okc.values(), key=lambda v: v["med_abs"])
        tie = len(second) > 1 and (second[1]["med_abs"] - second[0]["med_abs"]) < 0.03
        o.P(f"   {tag} best supported (smallest median|r| among readings with null sin-i slope): {best}{'  [within 0.03 dex of the next: NOT SEPARATED]' if tie else ''}")
    else:
        best, tie = None, None
        o.P(f"   {tag} no reading has a residual slope consistent with 0")
    return res, best, tie


if DAT:
    dat = c.load_dat(T, idx)
    o.P(f"[DAT] v_f(R_e) median {np.median(dat['v1']):.1f}, sigma_f(R_e) median {np.median(dat['s1']):.1f}; at 2.2 R_d: v {np.median(dat['v22r']):.1f}, sigma {np.median(dat['s22r']):.1f}; v22 (derived) {np.median(C['v22']):.1f}; median sin i {np.median(sini):.2f}")
    o.P(f"ratio v_f(2.2 R_d)/v22: median {np.median(dat['v22r']/C['v22']):.3f} [16-84: {np.percentile(dat['v22r']/C['v22'],16):.3f}, {np.percentile(dat['v22r']/C['v22'],84):.3f}]; divided by sin i: median {np.median(dat['v22r']/C['v22']/sini):.3f}; r(ratio, sin i) = {np.corrcoef(dat['v22r']/C['v22'], sini)[0,1]:+.2f}")
    o.P(f"implied s_AD at 2.2 R_d from the file's sigma (D1): median {np.median(0.92*2.2*dat['s22r']**2/C['v22']**2):.3f}  (data chat inferred ~0.52 if v_table = v_perp)")
    o.P("B1: ratio test v_f(2.2 R_d) vs v22 under four readings")
    B1, best1, tie1 = score_readings("B1", dat["v22r"], dat["s22r"], C["v22"], 2.2, "B1")
    o.res["B1"] = dict(res=B1, best=best1, tie=tie1)
    # B2
    o.P("B2: Spearman of (v_f/v_c) against sin i, three comparators")
    vc198 = np.sqrt(R198["gobs"] * C["Re"])
    vdyn = np.where(np.isfinite(C["logMdyn"]), np.sqrt(c.G * 10 ** np.where(np.isfinite(C["logMdyn"]), C["logMdyn"], 0) / C["Re"]), np.nan)
    B2 = {}
    for cn, vc, vf in (("CFG198 reconstruction at R_e", vc198, dat["v1"]), ("v22 at 2.2 R_d", C["v22"], dat["v22r"]), ("v_dyn=sqrt(G M_dyn/R_e) at R_e", vdyn, dat["v1"])):
        for rd in ("a", "b"):
            vp = vf / sini if rd == "b" else vf
            mm = np.isfinite(vp / vc) & (vp > 0)
            rho, p = c.stats.spearmanr((vp / vc)[mm], sini[mm])
            B2[f"{cn}|{rd}"] = float(rho)
            o.P(f"   comparator {cn:34s} reading ({rd}): rho = {rho:+.2f} (p={p:.3f}); median ratio {np.nanmedian((vp/vc)[mm]):.3f}")
    o.res["B2"] = B2
    # B3 slopes
    o.P("B3: slopes, R199, reading x drift (Theil-Sen [CI B=2000] and OLS)")
    B3 = {}
    cfgs = [("a", None), ("a", "D1"), ("a", "D2"), ("b", None), ("b", "D1"), ("b", "D2")]
    for rd, dr in cfgs:
        gp = c.gperp_reading(dat["v1"], C["Re"], C["incl"], rd, dat["s1"], dr)
        R = c.routes(C, dict(mode="R199", gperp=gp))
        cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
        st, bs = c.slope_table(z, cols, B, SEED, {"d": ("i", "ii")})
        both = np.isfinite(cols["i"]) & np.isfinite(cols["ii"])
        ols_d = c.ols(z[both], cols["ii"][both]) - c.ols(z[both], cols["i"][both])
        vi = np.isfinite(R["a0_i"])
        th = c.thirds(z[vi])
        lev = float(np.median(c.level_log(R["a0_i"])[np.where(vi)[0][th[0]]]))
        key = f"{rd}|{dr}"
        B3[key] = dict(b_i=st["i"]["b"], b_ii=st["ii"]["b"], b_iii=st["iii"]["b"], d=st["d"]["b"], d_ci=(st["d"]["lo"], st["d"]["hi"]),
                       b_ii_ci=(st["ii"]["lo"], st["ii"]["hi"]), ols_d=ols_d, level=lev)
        o.P(f"   reading ({rd}) drift {str(dr):4s}: b_i {st['i']['b']:+.3f}  b_ii {st['ii']['b']:+.3f} [{st['ii']['lo']:+.2f},{st['ii']['hi']:+.2f}]  b_iii {st['iii']['b']:+.3f}  Delta b (TS) {st['d']['b']:+.3f} [{st['d']['lo']:+.2f},{st['d']['hi']:+.2f}]  Delta b (OLS) {ols_d:+.3f}  level {lev:.2f}")
    o.res["B3"] = B3
    base = B3["a|None"]
    o.P("B3 structural prediction: b's move together and Delta b unchanged within 0.03:")
    for k, v in B3.items():
        o.P(f"   {k}: shift b_i {v['b_i']-base['b_i']:+.3f}, b_ii {v['b_ii']-base['b_ii']:+.3f}, Delta b(TS) {v['d']-base['d']:+.3f}, Delta b(OLS) {v['ols_d']-B3['a|None']['ols_d']:+.3f}")
    # B5 levels classification
    o.P("B5: level (lowest z-third, route (i)) against the footings, per reading/drift (bootstrap CI B=2000):")
    for rd, dr in cfgs:
        gp = c.gperp_reading(dat["v1"], C["Re"], C["incl"], rd, dat["s1"], dr)
        R = c.routes(C, dict(mode="R199", gperp=gp))
        vi = np.isfinite(R["a0_i"]); th = c.thirds(z[vi])
        low = c.level_log(R["a0_i"])[np.where(vi)[0][th[0]]]
        lo_, hi_ = c.boot_median(low, B, SEED)
        cls = "below both" if hi_ < c.LOG_CAN else ("above both" if lo_ > c.LOG_ALT else "consistent with footing(s)")
        o.P(f"   ({rd}, {dr}): {np.median(low):.2f} [{lo_:.2f},{hi_:.2f}] -> {cls}")
        o.res.setdefault("B5", {})[f"{rd}|{dr}"] = dict(med=float(np.median(low)), ci=(lo_, hi_), cls=cls)
else:
    o.P("[DAT] NOT RUN (external directory not found)")

# B4 CSV-only
o.P("B4 (CSV only): outermost row of the positive side against v22 (flat-curve stand-in, weak)")
vmax = T["v_at_maxR_pos"][idx]
smax = T["sig_at_maxR_pos"][idx]
Rmax = T["maxR_over_Re_pos"][idx]
Rfac = 1.678 * Rmax
sAD = 0.92 * Rfac * smax ** 2 / C["v22"] ** 2
o.P(f"   outermost R/R_e median {np.median(Rmax):.2f}; sigma_maxR median {np.median(smax):.1f}; v/v22 median {np.median(np.abs(vmax)/C['v22']):.3f}; s_AD (D1, R=r_max) median {np.median(sAD):.2f} (>1 for {int(np.sum(sAD>=1))} rows)")
lr = np.where(vmax != 0, np.log10(np.maximum(np.abs(vmax), 1e-300) / C["v22"]), np.nan)
lsi = np.log10(sini)
B4 = {}
for name, pred in {"(a) v_perp, D1": np.sqrt(np.where(sAD < 1, 1 - sAD, np.nan)), "(b) projected": sini,
                   "(c) projected + D1": sini * np.sqrt(np.where(sAD < 1, 1 - sAD, np.nan)), "(d) already v_c": np.ones_like(sini)}.items():
    r = lr - np.log10(pred)
    sl, cl = ols_boot(lsi, r, B, SEED)
    B4[name] = dict(median=float(np.nanmedian(r)), med_abs=float(np.nanmedian(np.abs(r))), slope=sl, ci=cl, n=int(np.isfinite(r).sum()))
    o.P(f"   {name:22s} n={B4[name]['n']:3d} median resid {B4[name]['median']:+.3f} median|r| {B4[name]['med_abs']:.3f} slope vs log sin i {sl:+.2f} [{cl[0]:+.2f},{cl[1]:+.2f}]")
o.res["B4"] = B4
o.finish()
sys.exit(0)
