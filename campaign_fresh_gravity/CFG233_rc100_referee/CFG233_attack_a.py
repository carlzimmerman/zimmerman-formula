"""CFG233 attack (a): independence of f_DM from the authors' priors; propagation of mis-specified gas scaling, tilts, pressure."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *
from CFG233_syslib import *

t0 = start("CFG233_attack_a")
d = load_rc100(); z = d["z"]; n = len(z); zmed = np.median(z); dz = z - zmed
R = {}
B = 2000
base = measure(z, d["D"], d["gbar"], d["gobs"], B=10000)
print("base:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in base.items()})
R["base"] = base

# ----------------------------------------------------- a1 information content
gg = freeman_gbar(d["logM"], d["Re"])
lf = np.log10(d["gbar"]); lg = np.log10(gg)
diff = lf - lg
A = np.vstack([lg, np.ones(n)]).T
coef, *_ = np.linalg.lstsq(A, lf, rcond=None)
res = lf - A @ coef
bs_diff = boot_ts(z, [diff], 10000, SEED_MAIN)[0]
print(f"a1: log g_bar(f_DM) - log g_bar(Freeman, M_bar table): median {np.median(diff):+.3f}, SD {diff.std():.3f}, 16-84% {np.percentile(diff,16):+.3f}..{np.percentile(diff,84):+.3f}")
print(f"    OLS log gbar_f = {coef[0]:.3f} log g_geom + {coef[1]:.3f}; residual SD {res.std():.3f} dex; corr {np.corrcoef(lf,lg)[0,1]:.3f}")
print(f"    TS slope of (log gbar_f - log g_geom) vs z: {ts(z,diff):+.4f} CI {ci(bs_diff)}")
R["a1"] = dict(median=float(np.median(diff)), sd=float(diff.std()), ols=list(coef), resid_sd=float(res.std()), corr=float(np.corrcoef(lf, lg)[0, 1]), ts_slope=ts(z, diff), ts_ci=ci(bs_diff))
# variance decomposition of delta_flat
df, dr = delta_pair(d["D"], d["gbar"], z)
print("    corr(delta_flat, log M_bar) = %.3f ; corr(delta_flat, log V_c) = %.3f ; corr(delta_flat, log g_bar) = %.3f ; corr(delta_flat, z) = %.3f" % (
    np.corrcoef(df, d["logM"])[0, 1], np.corrcoef(df, np.log10(d["Vc"]))[0, 1], np.corrcoef(df, lf)[0, 1], np.corrcoef(df, z)[0, 1]))
R["a1"]["corr_delta_logM_logV_logg_z"] = [float(np.corrcoef(df, x)[0, 1]) for x in (d["logM"], np.log10(d["Vc"]), lf, z)]

# ----------------------------------------------------- a2 same-galaxy route comparison (RC100 vs RC41 1D)
m41, matched, unmatched, rc = rc41_match(d)
idx = {r["id"].replace("_", " "): r for r in rc}
rows = [(i, idx[nm]) for i, nm in enumerate(d["name"]) if nm in idx]
ii = np.array([i for i, _ in rows]); rr = [r for _, r in rows]
f41 = np.array([float(r["fDM_Re_1D"]) for r in rr]); lm41 = np.array([float(r["logMbar_1D"]) for r in rr])
re41 = np.array([float(r["Re_1D_kpc"]) for r in rr]); s41 = np.array([float(r["sigma0_1D_kms"]) for r in rr])
ms = np.array([float(r["logMstar_SED"]) for r in rr]); mg = np.array([float(r["logMgas"]) for r in rr])
lmprior = np.log10(10 ** ms + 10 ** mg)
zz = z[ii]
def s16(x): return f"{np.median(x):+.3f} [{np.percentile(x,16):+.3f},{np.percentile(x,84):+.3f}]"
comps = {"f_DM RC100-RC41": d["f"][ii] - f41, "logMbar RC100-RC41": d["logM"][ii] - lm41, "Re RC100-RC41 kpc": d["Re"][ii] - re41,
         "sigma0 RC100-RC41": d["s0"][ii] - s41, "logMbar RC100 - log(M*+Mgas)": d["logM"][ii] - lmprior,
         "logMbar RC41-1D - log(M*+Mgas)": lm41 - lmprior}
print(f"a2: {len(ii)} matched galaxies, same-galaxy comparison (median [16,84]) and TS slope vs z of each difference (95% boot CI)")
R["a2"] = {}
for k, v in comps.items():
    bs = boot_ts(zz, [v], 5000, SEED_MAIN)[0]
    print(f"    {k}: {s16(v)}; slope {ts(zz, v):+.3f} CI ({ci(bs)[0]:+.3f},{ci(bs)[1]:+.3f})")
    R["a2"][k] = dict(med=float(np.median(v)), sl=ts(zz, v), ci=ci(bs))
# gas ratio trend of the authors' own gas column
lmu = mg - ms
X = np.vstack([zz, np.ones(len(zz))]).T
cb, *_ = np.linalg.lstsq(X, lmu, rcond=None)
rng = np.random.default_rng(233)
bb = []
for _ in range(4000):
    j = rng.integers(0, len(zz), len(zz)); c_, *_ = np.linalg.lstsq(X[j], lmu[j], rcond=None); bb.append(c_[0])
bauth, aauth = cb[0], cb[1]
print(f"G1: log10(M_gas/M*) = {aauth:+.3f} + {bauth:+.3f} z (RC41 own columns, n={len(zz)}); slope 95% boot CI ({np.percentile(bb,2.5):+.3f},{np.percentile(bb,97.5):+.3f}); residual SD {np.std(lmu-X@cb):.3f}")
R["G1"] = dict(a=float(aauth), b=float(bauth), b_ci=(float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))), n=len(zz))
mu_G1 = 10 ** (aauth + bauth * z)
mu_G2 = np.clip(0.25 + 0.35 * z, 0.1, 1.3)
print("mu_G1(z=0.61, 1.5, 2.52) =", [round(float(10 ** (aauth + bauth * x)), 3) for x in (0.61, 1.5, 2.52)], " mu_G2 =", [round(float(np.clip(0.25 + 0.35 * x, 0.1, 1.3)), 3) for x in (0.61, 1.5, 2.52)])
print("sigma(log M_bar) RC41 median of (lo,hi):", float(np.median([0.5 * (float(r['logMbar_lo']) + float(r['logMbar_hi'])) for r in rc])),
      "; sigma(f_DM):", float(np.median([0.5 * (float(r['fDM_lo']) + float(r['fDM_hi'])) for r in rc])))

# ----------------------------------------------------- PHIBSS measured gas tilt
ph = load_phibss()
zc, lmu_ph = [], []
for r in ph:
    try:
        if float(r["mbar_is_upper_limit"]) == 1 or float(r["co_upper_limit"]) == 1: continue
        mm, ms_, zco = float(r["mmol_msun"]), float(r["mstar_msun"]), float(r["z_co"])
        if not (mm > 0 and ms_ > 0 and np.isfinite(zco)): continue
        zc.append(zco); lmu_ph.append(np.log10(mm / ms_))
    except Exception:
        pass
zc, lmu_ph = np.array(zc), np.array(lmu_ph)
Xp = np.vstack([zc, np.ones(len(zc))]).T
cp, *_ = np.linalg.lstsq(Xp, lmu_ph, rcond=None)
bp = []
for _ in range(4000):
    j = rng.integers(0, len(zc), len(zc)); c_, *_ = np.linalg.lstsq(Xp[j], lmu_ph[j], rcond=None); bp.append(c_[0])
b_ph, se_ph = cp[0], np.std(bp)
t_data = b_ph - bauth
se_t = np.sqrt(se_ph ** 2 + np.std(bb) ** 2)
print(f"PHIBSS (n={len(zc)}, z {zc.min():.2f}-{zc.max():.2f}, clean rows): log10(mmol/M*) = {cp[1]:+.3f} + {b_ph:+.3f} z, SE {se_ph:.3f}; level at z=1.5 mu_mol = {10**(cp[1]+1.5*b_ph):.2f} ; RC41 G1 at z=1.5 mu_gas = {10**(aauth+1.5*bauth):.2f}")
print(f"data-informed tilt t_data = b_PHIBSS - b_auth = {t_data:+.3f} +/- {se_t:.3f} dex per unit z")
R["phibss"] = dict(n=len(zc), a=float(cp[1]), b=float(b_ph), se=float(se_ph), t_data=float(t_data), se_t=float(se_t))

# ----------------------------------------------------- gas grid
def gas_cell(mu, c, t, B=B, seed=SEED_MAIN):
    mu_true = c * mu * 10 ** (t * dz)
    kf = (1 + mu) / (1 + mu_true)
    ok, zz_, D, gb, go = redecompose(d, kfac=kf, s_press=3.0)
    o = measure(zz_[ok], D[ok], gb[ok], go[ok], B=B, seed=seed)
    o["n_excl"] = int((~ok).sum())
    return o
cs = [0.25, 0.5, 1.0, 2.0, 4.0]; ts_ = [-0.30, -0.15, 0.0, 0.15, 0.30]
grid = {}
for name, mu in (("G1", mu_G1), ("G2", mu_G2)):
    print(f"\n=== gas grid {name}: rows = c (true gas / authors' gas), cols = tilt t; entries: flat slope | rival slope | tension of BOTH slopes vs rival expectation (min) | class | excluded")
    for c in cs:
        for t in ts_:
            o = gas_cell(mu, c, t)
            tmin = min(abs(o["T_flat_vs_rival"]), abs(o["T_rival_vs_rival"]))
            grid[f"{name}/c{c}/t{t}"] = dict(o, tmin=tmin)
            print(f"  {name} c={c:4} t={t:+.2f}: flat {o['slope_flat']:+.3f} rival {o['slope_rival']:+.3f} | exp_R {o['exp_R_flat']:+.3f} | T_flat-vs-R {abs(o['T_flat_vs_rival']):.1f} T_rival-vs-R {abs(o['T_rival_vs_rival']):.1f} min {tmin:.1f} | T_flat-vs-F {abs(o['T_flat_vs_flat']):.1f} T_rival-vs-F {abs(o['T_rival_vs_flat']):.1f} | {o['cls']} | excl {o['n_excl']}")
R["grid"] = grid
for name in ("G1", "G2"):
    band = [grid[f"{name}/c{c}/t{t}"] for c in (0.5, 1.0, 2.0) for t in (-0.15, 0.0, 0.15)]
    surv = sum(b["tmin"] >= 3 for b in band)
    print(f"{name}: plausible band (9 cells): rival tension of BOTH slopes >= 3 sigma in {surv}/9 cells -> {'SURVIVES' if surv/9>=0.8 else ('FAILS' if surv/9<0.6 else 'WEAKENED')} (line: >=80% survive, <60% fail)")
    R[f"band_{name}"] = dict(surv=int(surv), tmin=[b["tmin"] for b in band])

# data-informed rows
for lab, tt in (("t_data", t_data), ("t_data-1se", t_data - se_t), ("t_data+1se", t_data + se_t)):
    o = gas_cell(mu_G1, 1.0, tt)
    print(f"data-informed {lab} = {tt:+.3f}: flat {o['slope_flat']:+.3f} rival {o['slope_rival']:+.3f} T_flat-vs-R {abs(o['T_flat_vs_rival']):.1f} T_rival-vs-R {abs(o['T_rival_vs_rival']):.1f} class {o['cls']} excl {o['n_excl']}")
    R["data_" + lab] = o

# break-evens (point slopes, expected slope fixed at the sample's rival-true value)
target = base["exp_R_flat"]
def sl_flat(kfun):
    ok, zz_, D, gb, go = redecompose(d, kfac=kfun)
    return ts(zz_[ok], delta_of(D[ok], gb[ok], zz_[ok], "flat")), int((~ok).sum())
def bisect(fn, lo, hi, tgt, it=40):
    flo = fn(lo)[0] - tgt; fhi = fn(hi)[0] - tgt
    if flo * fhi > 0: return None, fn(lo)[0], fn(hi)[0]
    for _ in range(it):
        mid = 0.5 * (lo + hi); fm = fn(mid)[0] - tgt
        if flo * fm <= 0: hi = mid; fhi = fm
        else: lo = mid; flo = fm
    return 0.5 * (lo + hi), None, None
print("\n=== break-evens: value of a systematic at which the observed flat slope equals the rival-true expectation (%+.4f)" % target)
be = {}
for name, mu in (("G1", mu_G1), ("G2", mu_G2)):
    r_ = bisect(lambda t: sl_flat((1 + mu) / (1 + mu * 10 ** (t * dz))), -2.0, 2.0, target)
    be["gas_t_" + name] = r_
    print(f"gas tilt t* ({name}, c=1): {r_}")
    r0 = sl_flat(1 + mu)  # zero true gas: k = 1 + mu
    r0b = sl_flat((1 + mu) / (1 + 0 * mu))
    print(f"   zero true gas at all z ({name}): flat slope {r0[0]:+.4f} (excluded {r0[1]}); shift {r0[0]-base['slope_flat']:+.4f}; needed {target-base['slope_flat']:+.4f}")
    be["zero_gas_" + name] = r0
    dlog = np.log10(1 + mu[np.argmax(z)]) - np.log10(1 + mu[np.argmin(z)])
    print(f"   total log10(1+mu) change z_lo->z_hi under {name}: {dlog:+.3f} dex (max Delta log M_bar tilt gas can supply over the range, at zero true gas)")
    be["gas_total_dlog_" + name] = float(dlog)
tau_b = bisect(lambda tau: sl_flat(10 ** (tau * dz)), -1.0, 1.0, target)
print("M_bar tilt tau* (dex per unit z; k=10^(tau dz)):", tau_b, "-> total over z range:", None if tau_b[0] is None else tau_b[0] * (z.max() - z.min()), "dex")
be["tau"] = tau_b
def sl_q(q):
    ok, zz_, D, gb, go = redecompose(d, qtilt=q)
    return ts(zz_[ok], delta_of(D[ok], gb[ok], zz_[ok], "flat")), int((~ok).sum())
q_b = bisect(sl_q, -0.3, 0.3, target)
print("V_c tilt q* (dex per unit z on V_c, D_obs shifts 2q):", q_b, "-> total over range", None if q_b[0] is None else q_b[0] * (z.max() - z.min()), "dex")
be["q"] = q_b
R["breakeven"] = be
# scan of total M_bar offset (post-freeze display; labelled)
print("\n=== M_bar (baryon-mass) tilt scan; total dex over z 0.61-2.52 (POST-FREEZE display for the CFG217 question); tau = total/%.2f" % (z.max() - z.min()))
scan = {}
for tot in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.26, 0.30, 0.40):
    tau = tot / (z.max() - z.min())
    ok, zz_, D, gb, go = redecompose(d, kfac=10 ** (tau * dz))
    o = measure(zz_[ok], D[ok], gb[ok], go[ok], B=B, seed=SEED_MAIN)
    scan[tot] = dict(o, n_excl=int((~ok).sum()))
    print(f"  total {tot:.2f} dex (baryons over-assumed at high z): flat {o['slope_flat']:+.3f} [{o['ci_flat'][0]:+.3f},{o['ci_flat'][1]:+.3f}] rival {o['slope_rival']:+.3f} | T_flat-vs-rival-exp {o['T_flat_vs_rival']:+.1f}, T_rival-vs-0 {o['T_rival_vs_rival']:+.1f}, T_flat-vs-0 {o['T_flat_vs_flat']:+.1f}, T_rival-vs-flat-exp {o['T_rival_vs_flat']:+.1f} | {o['cls']} | excl {scan[tot]['n_excl']}")
R["tau_scan"] = scan

# ----------------------------------------------------- a3 pressure axis
print("\n=== a3 pressure axis: V_c'^2 = V_c^2 - (1 - s/3) P, P = 3.356 sigma_0^2 (Price+2021's stated constant-sigma exponential-disc asymmetric drift; s=3 = table as given)")
P = 2 * d["s0"] ** 2 * 1.678
print(f"   P/V_c^2: median {np.median(P/d['Vc']**2):.3f}; z<=1.53: {np.median((P/d['Vc']**2)[z<=1.53]):.3f}; z>1.53: {np.median((P/d['Vc']**2)[z>1.53]):.3f}; sigma0 median low/high z: {np.median(d['s0'][z<=1.53]):.0f}/{np.median(d['s0'][z>1.53]):.0f} km/s")
pres = {}
for s in (0.0, 1.0, 1.42, 1.62, 1.69, 3.0):
    ok, zz_, D, gb, go = redecompose(d, s_press=s)
    o = measure(zz_[ok], D[ok], gb[ok], go[ok], B=B, seed=SEED_MAIN)
    pres[s] = dict(o, n_excl=int((~ok).sum()))
    print(f"  s={s:4}: flat {o['slope_flat']:+.3f} [{o['ci_flat'][0]:+.3f},{o['ci_flat'][1]:+.3f}] rival {o['slope_rival']:+.3f} | exp_R {o['exp_R_flat']:+.3f} | T_flat-vs-R {o['T_flat_vs_rival']:+.1f} T_rival-vs-0 {o['T_rival_vs_rival']:+.1f} | {o['cls']} | excl {pres[s]['n_excl']}")
R["pressure"] = pres
shift1 = pres[1.0]["slope_flat"] - pres[3.0]["slope_flat"]
print(f"   s=1 (Kretschmer-like) shifts the flat slope by {shift1:+.4f} = {shift1/base['sd_flat']:+.2f} sigma_slope; fail line: > 1 sigma_slope -> {'FAIL' if abs(shift1) > base['sd_flat'] else 'PASS'}")
R["pressure_shift_s1"] = shift1
savejson("CFG233_attack_a", R)
print("done")
