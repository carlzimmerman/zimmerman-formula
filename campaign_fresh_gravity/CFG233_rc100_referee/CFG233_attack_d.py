"""CFG233 attack (d): the sign of the negative flat slope in the 62 non-RC41 galaxies (selection, RC41 definition, errors-in-variables)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *
from scipy import stats

start("CFG233_attack_d")
d = load_rc100(); z = d["z"]; n = len(z)
m41, matched, unmatched, rc = rc41_match(d)
o = sub(d, ~m41); k = sub(d, m41)
n62 = len(o["z"])
R = {}
def slopes(dd, B=10000, seed=SEED_MAIN, mask=None):
    m = np.ones(len(dd["z"]), bool) if mask is None else mask
    zz = dd["z"][m]
    f_, r_ = delta_pair(dd["D"][m], dd["gbar"][m], zz)
    bs = boot_ts(zz, [f_, r_], B, seed)
    out = dict(n=int(m.sum()), flat=ts(zz, f_), ci_flat=ci(bs[0]), rival=ts(zz, r_), ci_rival=ci(bs[1]), med_flat=float(np.median(f_)))
    out["cls"] = classify(out["ci_flat"], out["ci_rival"])
    return out
def show(lab, r):
    print(f"  {lab:34}: n={r['n']:3d} flat {r['flat']:+.3f} [{r['ci_flat'][0]:+.3f},{r['ci_flat'][1]:+.3f}] rival {r['rival']:+.3f} [{r['ci_rival'][0]:+.3f},{r['ci_rival'][1]:+.3f}] class {r['cls']}")
print("=== d1 reproduce")
d1 = slopes(o); show(f"non-RC41 ({n62})", d1); R["d1"] = d1
show(f"RC41 matched ({len(k['z'])})", slopes(k))
print("\n=== d2 selection: cuts on the 62 (nu_mono canonical, B=10000)")
d2 = {}
for lab, m in (("logM >= 10.0", o["logM"] >= 10.0), ("logM >= 10.3", o["logM"] >= 10.3), ("logM >= 10.6", o["logM"] >= 10.6),
               ("z >= 0.8", o["z"] >= 0.8), ("z <= 2.3", o["z"] <= 2.3), ("0.05<=f<=0.95", (o["f"] >= 0.05) & (o["f"] <= 0.95)),
               ("g_bar < 3 a0", o["gbar"] < 3 * A0["canonical"]), ("f_DM >= 0.10", o["f"] >= 0.10)):
    r = slopes(o, mask=m); d2[lab] = r; show(lab, r)
R["d2"] = d2
print("  KS tests, non-RC41 (62) vs RC41 (38): p-values")
ks = {}
for nm, a, b in (("z", o["z"], k["z"]), ("logM_bar", o["logM"], k["logM"]), ("log g_bar", np.log10(o["gbar"]), np.log10(k["gbar"])), ("R_e", o["Re"], k["Re"]),
                 ("sigma0", o["s0"], k["s0"]), ("f_DM", o["f"], k["f"]), ("log V_c", np.log10(o["Vc"]), np.log10(k["Vc"]))):
    p = stats.ks_2samp(a, b); ks[nm] = (float(p.statistic), float(p.pvalue)); print(f"    {nm}: KS D={p.statistic:.2f} p={p.pvalue:.3f}; medians {np.median(a):.3g} vs {np.median(b):.3g}")
R["ks"] = ks
zt = np.percentile(z, [33.3, 66.7])
print("  by z tercile (full sample): n(62)/n(38), median logM_bar (62 / 38), median log g_bar/a0 (62 / 38)")
for lab, lo_, hi_ in (("low z", 0, zt[0]), ("mid z", zt[0], zt[1]), ("high z", zt[1], 9)):
    a = (o["z"] > lo_) & (o["z"] <= hi_); b = (k["z"] > lo_) & (k["z"] <= hi_)
    print(f"    {lab}: {a.sum()}/{b.sum()}, logM {np.median(o['logM'][a]):.2f}/{np.median(k['logM'][b]) if b.sum() else float('nan'):.2f}, log g/a0 {np.median(np.log10(o['gbar'][a]/A0['canonical'])):+.2f}/{np.median(np.log10(k['gbar'][b]/A0['canonical'])) if b.sum() else float('nan'):+.2f}")
print("  correlation of z with logM_bar in the 62: %.2f ; with log g_bar: %.2f ; in the 38: %.2f ; %.2f" % (
    np.corrcoef(o["z"], o["logM"])[0, 1], np.corrcoef(o["z"], np.log10(o["gbar"]))[0, 1], np.corrcoef(k["z"], k["logM"])[0, 1], np.corrcoef(k["z"], np.log10(k["gbar"]))[0, 1]))

print("\n=== d3 RC41 definition by (|dz|<=0.01 and |logM_bar,RC100 - logMbar_1D| <= 0.05)")
m41b = np.zeros(n, bool)
for r in rc:
    zr, lm = float(r["z"]), float(r["logMbar_1D"])
    cand = np.where((abs(d["z"] - zr) <= 0.01) & (abs(d["logM"] - lm) <= 0.05))[0]
    if len(cand) >= 1: m41b[cand[np.argmin(abs(d["z"][cand] - zr) + abs(d["logM"][cand] - lm))]] = True
print(f"  alternative RC41 set n={m41b.sum()} (by name: {m41.sum()}); overlap {int((m41 & m41b).sum())}; name-only {int((m41 & ~m41b).sum())}; alt-only {int((~m41 & m41b).sum())}")
dd3 = slopes(d, mask=~m41b); show("complement of alt RC41 set", dd3); R["d3"] = dd3
R["d3_sets"] = dict(alt=int(m41b.sum()), name=int(m41.sum()), overlap=int((m41 & m41b).sum()))

print("\n=== d4(i) delta on log g_bar, log M_bar; partial z-slope")
for lab, dd in (("all 100", d), ("non-RC41 62", o)):
    f_ = delta_of(dd["D"], dd["gbar"], dd["z"], "flat")
    lg = np.log10(dd["gbar"]); zz = dd["z"]
    bg = ts(lg, f_); bm = ts(dd["logM"], f_)
    bsg = boot_ts(lg, [f_], 4000, SEED_MAIN)[0]
    # OLS partial
    X = np.vstack([np.ones(len(zz)), zz, lg]).T
    coef, *_ = np.linalg.lstsq(X, f_, rcond=None)
    rng = np.random.default_rng(SEED_MAIN); bz = []
    for _ in range(4000):
        j = rng.integers(0, len(zz), len(zz)); c_, *_ = np.linalg.lstsq(X[j], f_[j], rcond=None); bz.append(c_[1])
    # OLS z-only
    X1 = np.vstack([np.ones(len(zz)), zz]).T; c1, *_ = np.linalg.lstsq(X1, f_, rcond=None)
    res = f_ - (np.median(f_ - bg * lg) + bg * lg)   # residual after removing TS dependence on log g_bar
    print(f"  {lab}: TS slope of delta on log g_bar {bg:+.3f} CI {ci(bsg)}, on log M_bar {bm:+.3f}; OLS z-slope alone {c1[1]:+.3f}, OLS z-slope with log g_bar in the model {coef[1]:+.3f} CI ({np.percentile(bz,2.5):+.3f},{np.percentile(bz,97.5):+.3f}); OLS coefficient of log g_bar {coef[2]:+.3f}; TS z-slope of residual {ts(zz,res):+.3f}")
    R["d4i_" + lab] = dict(b_g=bg, b_m=bm, ols_z_alone=float(c1[1]), ols_z_partial=float(coef[1]), ci_partial=(float(np.percentile(bz, 2.5)), float(np.percentile(bz, 97.5))), ts_resid=ts(zz, res))
rcm = load_rc41(); sigM = float(np.median([0.5 * (float(r["logMbar_lo"]) + float(r["logMbar_hi"])) for r in rcm]))
s_bar = 0.22
print(f"  analytic attenuation of delta-vs-log g_bar slope from noise sigma_eps={sigM:.2f}: -(1-s)sigma^2/(var(x)+sigma^2) = {-(1-s_bar)*sigM**2/(np.var(np.log10(o['gbar']))+sigM**2):+.3f} (NOT the z-slope)")

print("\n=== d4(ii) flat-truth mocks on the 62 galaxies (their z, R_e, g_obs), errors as in attack b, three selection rules; N=4000, seeds 233 and 234")
gobs0 = o["gobs"]; Re = o["Re"]; zo = o["z"]
gb_true = invert_gbar(gobs0, a0_of("flat", zo), nu_mono)
df_o, _ = delta_pair(o["D"], o["gbar"], zo)
obs_sc = 1.4826 * np.median(abs(df_o - np.median(df_o))); obs62 = ts(zo, df_o)
sigV = math.log10(1.05)
gbmin, gbmax = o["gbar"].min(), o["gbar"].max()
def make(B, rng, sig_int, rule):
    nn = len(zo)
    gobs_true = gobs0[None] * 10 ** rng.normal(0, sig_int, (B, nn))
    gobs_m = gobs_true * 10 ** (2 * rng.normal(0, sigV, (B, nn)))
    gb_as = gb_true[None] * 10 ** rng.normal(0, sigM, (B, nn))
    f = 1 - gb_as / gobs_m
    keep = np.ones((B, nn), bool)
    if rule == "drop_f<0.01": keep &= f >= 0.01
    f = np.clip(f, 0.01, 0.99); f = np.round(f, 2); f = np.clip(f, 0.01, 0.99)
    V = np.round(np.sqrt(gobs_m * Re[None] * KPC) / 1e3); go = (V * 1e3) ** 2 / (Re[None] * KPC); gb = (1 - f) * go; D = 1 / (1 - f)
    if rule == "gbar_in_range": keep &= (gb >= gbmin) & (gb <= gbmax)
    a = delta_of(D, gb, np.broadcast_to(zo, (B, nn)), "flat")
    if keep.all():
        return ts_batch(np.broadcast_to(zo, (B, nn)), a), a
    sl = np.array([ts(zo[kp], a[i][kp]) if kp.sum() > 6 else np.nan for i, kp in enumerate(keep)])
    return sl, a
def cal(rule):
    lo, hi = 0.0, 0.5
    for _ in range(14):
        mid = 0.5 * (lo + hi); rng = np.random.default_rng(1234)
        _, a = make(200, rng, mid, "none"); sc = np.mean([1.4826 * np.median(abs(x - np.median(x))) for x in a[:60]])
        if sc < obs_sc: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
sint = cal("none")
print(f"  observed 62-galaxy flat slope {obs62:+.4f}; robust SD {obs_sc:.3f}; sigma_M {sigM:.3f}; calibrated sigma_int {sint:.3f}")
d4 = {}
for seed in (233, 234):
    for rule in ("none", "gbar_in_range", "drop_f<0.01"):
        rng = np.random.default_rng(seed)
        sl, _ = make(4000, rng, sint, rule)
        sl = sl[np.isfinite(sl)]
        d4[f"{rule}/seed{seed}"] = dict(mean=float(sl.mean()), sd=float(sl.std()), p_le_027=float((sl <= -0.027).mean()), p_le_obs=float((sl <= obs62).mean()), p_lt_010=float((sl <= -0.010).mean()))
        print(f"  seed {seed} rule {rule:14}: mock flat slope mean {sl.mean():+.4f} sd {sl.std():.4f}; P(<= -0.010) {d4[f'{rule}/seed{seed}']['p_lt_010']:.3f}; P(<= -0.027) {d4[f'{rule}/seed{seed}']['p_le_027']:.3f}; P(<= observed {obs62:+.3f}) {d4[f'{rule}/seed{seed}']['p_le_obs']:.3f}")
R["d4ii"] = d4
frac = max(v["p_le_027"] for v in d4.values()); part = max(v["p_lt_010"] for v in d4.values())
print(f"  verdict rule: explained if some mechanism gives slope <= -0.027 in >= 50% of mocks (max seen {frac:.3f}); partly explained if the mean lies in [-0.027,-0.010) (means: {[round(v['mean'],4) for v in d4.values()]}) -> ", end="")
means = [v["mean"] for v in d4.values()]
print("EXPLAINED" if frac >= 0.5 else ("PARTLY EXPLAINED" if min(means) < -0.010 else "UNEXPLAINED (kept)"))
savejson("CFG233_attack_d", R)
