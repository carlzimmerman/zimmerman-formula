#!/usr/bin/env python3
"""CFG562: SAGA DR3 stacked satellite LOS velocity dispersion vs (a) law, (b) CFG398 supply-limited law, (c) NFW.
See FROZEN_CRITERIA.md. Run: python3 cfg562_saga_dispersion.py [--mutate]"""
import os, sys, json, math, io, contextlib, hashlib, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import chi2 as CHI2
from astropy.table import Table
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, ROOT)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MSUN, KPC, H = 6.674e-11, 1.989e30, 3.0857e19, 0.7
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; COSMIC = 0.1200 / 0.02237
VT, EPS, RT = 275.0, 20.0, 1000.0
REDGES = np.array([30., 60., 110., 190., 300.])
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
FGRID = [0.05, 0.07, 0.10, 0.13, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0]
def nu(y): return C.nu_mono(np.atleast_1d(np.asarray(y, float)))

# ---------------- data
SHA = {"saga-dr3-tableC1.txt": "278239bbdbebb6093555b65fd91dbc3ec6bebf225c81c035ca0e8e8ae0a595bf",
       "saga-dr3-tableC3.txt": "14c0841d13b270468dee202f3246dd671f1e1ce05f83c66d33ff41c291d75f8b"}
for f, h in SHA.items():
    assert hashlib.sha256(open(os.path.join(HERE, "data", f), "rb").read()).hexdigest() == h, f
hosts = Table.read(os.path.join(HERE, "data", "saga-dr3-tableC1.txt"), format="ascii.mrt")
sats = Table.read(os.path.join(HERE, "data", "saga-dr3-tableC3.txt"), format="ascii.mrt")
HID = list(hosts["HOSTID"]); hidx = {h: i for i, h in enumerate(HID)}
lMs = np.array(hosts["log(M*)"], float)
lHI = np.ma.filled(np.ma.masked_invalid(np.ma.array(hosts["log(MHI)"], dtype=float)), np.nan)
Mb = np.where(np.isfinite(lHI), 10 ** lMs + 1.33 * 10 ** np.nan_to_num(lHI), 1.2 * 10 ** lMs)
lMh_lim = np.array(hosts["log(Mhalo)"], float)
P(f"hosts {len(HID)}: HI available for {np.isfinite(lHI).sum()}; log M_b median {np.median(np.log10(Mb)):.2f} "
  f"(range {np.log10(Mb).min():.2f}-{np.log10(Mb).max():.2f})")
sh = np.array([hidx[h] for h in sats["HOSTID"]]); R = np.array(sats["Rhost"], float)
V = np.array(sats["DVhost"], float); samp = np.array(sats["sample"], int)
P(f"satellites {len(R)}; |dv| max {np.abs(V).max():.1f}; R max {R.max():.1f} kpc")
sel = (R >= REDGES[0]) & (R < REDGES[-1])
selGS = sel & (samp <= 2)

# ---------------- models
def moster(lMh):
    Mh = 10 ** lMh; M1 = 10 ** 11.590
    return math.log10(2 * 0.0351 * Mh / ((Mh / M1) ** -1.376 + (Mh / M1) ** 0.608))
def inv_moster(l): return brentq(lambda x: moster(x) - l, 9.0, 15.5)
def c_dm(Mh): return 10 ** (0.905 - 0.101 * math.log10(Mh * H / 1e12))
def r_edge(M, a0, f):
    g = lambda lr: (nu(G * M * MSUN / ((10 ** lr) * KPC) ** 2 / a0)[0] - 1) - COSMIC / f
    return 10 ** brentq(g, -1, 6)
def g_law(r, M, a0):
    gN = G * M * MSUN / (r * KPC) ** 2; return gN * nu(gN / a0)
def g_sup(r, M, a0, f):
    re = r_edge(M, a0, f); g = g_law(r, M, a0)
    return np.where(r <= re, g, G * M * (1 + COSMIC / f) * MSUN / (r * KPC) ** 2), re
def g_nfw(r, M, Mh):
    c = c_dm(Mh); R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3) / KPC; x = r / (R200 / c)
    m = lambda x: np.log(1 + x) - x / (1 + x)
    return G * (Mh * m(x) / m(c) + M) * MSUN / (r * KPC) ** 2

RG = np.logspace(np.log10(0.5), np.log10(RT), 700)
RP = np.array(list(np.linspace(25, 310, 30)))
def sig_los(gfun, gam, beta=0.0, rg=None, Rp=RP, rt=RT):
    """Jeans: nu ~ r^-gam to rt, constant beta; g in m/s^2 on rg (kpc). Returns sigma_los(Rp) km/s."""
    rg = RG if rg is None else rg
    g = gfun(rg) * KPC / 1e6                                  # (km/s)^2 per kpc
    integ = rg ** (2 * beta) * rg ** (-gam) * g
    seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(rg)
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    Pr = rg ** (-2 * beta) * cum                              # nu sigma_r^2
    lP = np.log(np.maximum(Pr, 1e-300)); out = []
    for Rv in Rp:
        umax = math.sqrt(rt ** 2 - Rv ** 2); u = np.concatenate([[0], np.logspace(-2, math.log10(umax), 500)])
        r = np.sqrt(Rv ** 2 + u ** 2); Pi = np.exp(np.interp(np.log(r), np.log(rg), lP)); Pi[r >= rt] = 0
        num = np.trapz((1 - beta * Rv ** 2 / r ** 2) * Pi, u); den = np.trapz(r ** (-gam), u)
        out.append(math.sqrt(max(num / den, 0)))
    return np.array(out)

# ---------------- estimator
SGRID = np.arange(5.0, 600.0, 0.5)
def mle_sigma(v, eps=EPS):
    v = np.atleast_2d(v)                                     # (nreal, n)
    if len(v) > 40: return np.concatenate([mle_sigma(v[i:i + 40], eps) for i in range(0, len(v), 40)])
    S = np.sqrt(SGRID ** 2 + eps ** 2)[:, None, None]
    ll = -0.5 * (v[None] / S) ** 2 - np.log(S) - np.log(ndtr(VT / S) - ndtr(-VT / S))
    return SGRID[np.argmax(ll.sum(-1), axis=0)]
def draw_trunc(sig, rng, n=1, eps=EPS):
    s = np.sqrt(sig ** 2 + eps ** 2); lo, hi = ndtr(-VT / s), ndtr(VT / s)
    from scipy.special import ndtri
    return s * ndtri(lo + (hi - lo) * rng.random((n, len(sig))))

# ---------------- K1: reproduce CFG398
j398 = json.load(open(os.path.join(ROOT, "CFG398_supply_edge_kids", "cfg398_supply_edge_results.json")))["res"]
def r_ta(l): return 10 ** (math.log10(0.95) + (l - 10) / 1.5 * (math.log10(2.25) - math.log10(0.95)))
k1 = max(abs(r_edge(10 ** l, a0, f) / 1e3 / r_ta(l) / j398[f"{ft}|{f}"]["x"][i] - 1)
         for ft, a0 in A0.items() for f in (0.07, 0.1, 0.18) for i, l in enumerate((10.0, 10.5, 11.0, 11.5)))
checks = {"K1_cfg398": bool(k1 < 1e-6)}
P(f"K1 reproduce CFG398 x: max rel dev {k1:.2e} -> {checks['K1_cfg398']}")
for ft, a0 in A0.items():
    P("   " + ft + ": " + "; ".join(f"log M_b {l} f {f}: r_edge {r_edge(10**l, a0, f):.0f} kpc"
                                   for f in (0.10, 0.18) for l in (10.6, 11.0)))
# K2 Jeans
rgk = np.logspace(np.log10(0.5), 5, 900)
sk = sig_los(lambda r: (200e3) ** 2 / (r * KPC), 2.5, rg=rgk, Rp=[100.0], rt=1e5)[0]
checks["K2_jeans"] = bool(abs(sk / (200 / math.sqrt(2.5)) - 1) < 0.01)
P(f"K2 Jeans log potential: {sk:.2f} vs {200/math.sqrt(2.5):.2f} -> {checks['K2_jeans']}")
rngk = np.random.default_rng(1)
sk3 = mle_sigma(draw_trunc(np.full(2000, 120.0), rngk))[0]
checks["K3_estimator"] = bool(abs(sk3 / 120 - 1) < 0.03); P(f"K3 estimator: {sk3:.1f} vs 120 -> {checks['K3_estimator']}")

# ---------------- tracer slope
def fit_gamma(Rs):
    a, b = REDGES[0], REDGES[-1]; L = np.log(Rs).sum(); n = len(Rs)
    def nll(gm):
        k = 2 - gm
        norm = math.log(b / a) if abs(k + 1) < 1e-9 else (b ** (k + 1) - a ** (k + 1)) / (k + 1)
        return -(k * L - n * math.log(norm))
    gs = np.linspace(0.5, 4.0, 3501); return gs[np.argmin([nll(x) for x in gs])]
GAM = fit_gamma(R[sel]); GAM_GS = fit_gamma(R[selGS])
P(f"tracer: gamma_t = {GAM:.3f} (all samples, N={sel.sum()}); Gold+Silver {GAM_GS:.3f} (N={selGS.sum()})")

# ---------------- model sigma_los per host
used = sorted(set(sh[sel])); Mh_am = {i: 10 ** inv_moster(lMs[i]) for i in used}
def model_table(gam, beta, rt):
    rg = np.logspace(np.log10(0.5), np.log10(rt), 700); T = {}
    for i in used:
        M = Mb[i]
        T[("c",), i] = sig_los(lambda r: g_nfw(r, M, Mh_am[i]), gam, beta, rg, rt=rt)
        T[("c_lim",), i] = sig_los(lambda r: g_nfw(r, M, 10 ** lMh_lim[i]), gam, beta, rg, rt=rt)
        for ft, a0 in A0.items():
            T[("a", ft), i] = sig_los(lambda r: g_law(r, M, a0), gam, beta, rg, rt=rt)
            for f in FGRID:
                T[("b", ft, f), i] = sig_los(lambda r: g_sup(r, M, a0, f)[0], gam, beta, rg, rt=rt)
    return T
def per_sat(T, key, mask):
    return np.array([np.interp(R[k], RP, T[key, sh[k]]) for k in np.where(mask)[0]])

lMb = np.log10(Mb); medM = np.median(lMb[used]); P(f"host-mass split at log M_b {medM:.3f} ({len(used)} hosts with satellites in range)")
def bin_ids(mask, mass_split=True):
    idx = np.where(mask)[0]; rb = np.digitize(R[idx], REDGES) - 1
    mb = (lMb[sh[idx]] > medM).astype(int) if mass_split else np.zeros(len(idx), int)
    return idx, rb + 4 * mb, (8 if mass_split else 4)
def binned(v, idx, b, nb, eps=EPS):
    return np.array([mle_sigma(v[idx][b == k], eps)[0] for k in range(nb)])
def boot(v, idx, b, nb, nboot, seed, eps=EPS):
    rng = np.random.default_rng(seed); hs = np.array(sorted(set(sh[idx]))); out = np.zeros((nboot, nb))
    byh = {h: np.where(sh[idx] == h)[0] for h in hs}
    for t in range(nboot):
        pick = np.concatenate([byh[h] for h in rng.choice(hs, len(hs))])
        vv, bb = v[idx][pick], b[pick]
        out[t] = [mle_sigma(vv[bb == k], eps)[0] if (bb == k).sum() else np.nan for k in range(nb)]
    return out
def model_bins(T, key, idx, b, nb, nreal=200, seed=5620, eps=EPS):
    s = np.array([np.interp(R[k], RP, T[key, sh[k]]) for k in idx]); rng = np.random.default_rng(seed)
    vv = draw_trunc(s, rng, nreal, eps)
    return np.array([mle_sigma(vv[:, b == k], eps).mean() for k in range(nb)])

def analyse(v, mask, T, mass_split=True, nboot=1000, seed=562, eps=EPS, quiet=False, models=None):
    idx, b, nb = bin_ids(mask, mass_split)
    d = binned(v, idx, b, nb, eps); bs = boot(v, idx, b, nb, nboot, seed, eps); err = np.nanstd(bs, axis=0)
    cov = np.cov(np.where(np.isfinite(bs), bs, np.nanmean(bs, 0)).T)
    keys = models or ([("c",), ("c_lim",)] + [("a", ft) for ft in A0] + [("b", ft, f) for ft in A0 for f in FGRID])
    mv = {k: model_bins(T, k, idx, b, nb, eps=eps) for k in keys}
    c2 = {k: float(np.sum(((d - m) / err) ** 2)) for k, m in mv.items()}
    ci = np.linalg.inv(cov); c2cov = {k: float((d - m) @ ci @ (d - m)) for k, m in mv.items()}
    return dict(d=d, err=err, n=np.bincount(b, minlength=nb), mv=mv, c2=c2, c2cov=c2cov, nb=nb)

def verdict(c2, ft, nb=8):
    a, b18, c = c2[("a", ft)], c2[("b", ft, 0.18)], c2[("c",)]
    v = []
    if a - b18 > 9: v.append("SUPPLY EDGE SEEN")
    if a - c > 9 and b18 - c > 9: v.append("NFW-PREFERRED")
    if not v and CHI2.sf(a, nb) > 0.01 and b18 - a > 9: v.append("LAW-FLAT")
    return " + ".join(v) if v else "NON-DISCRIMINATING"

def name(k): return k[0] if len(k) == 1 else (f"a[{k[1]}]" if k[0] == "a" else f"b[{k[1]},f={k[2]}]")
def report(res, label, nb=8):
    P(f"\n== {label}")
    P("  bin  N   sigma_obs+-err  | " + "  ".join(name(k) for k in [("a", "canonical"), ("b", "canonical", 0.18), ("b", "canonical", 0.1), ("c",)]))
    for k in range(res["nb"]):
        lo, hi = REDGES[k % 4], REDGES[k % 4 + 1]
        P(f"  {'hiM' if k >= 4 else 'loM' if res['nb']==8 else 'all'} {lo:.0f}-{hi:.0f} n={res['n'][k]:3d} {res['d'][k]:6.1f}+-{res['err'][k]:5.1f} | "
          + "  ".join(f"{res['mv'][kk][k]:6.1f}" for kk in [("a", "canonical"), ("b", "canonical", 0.18), ("b", "canonical", 0.1), ("c",)]))
    for k in sorted(res["c2"], key=lambda k: res["c2"][k]):
        if k[0] == "b" and k[2] not in (0.1, 0.18, 1.0): continue
        P(f"   chi2 {name(k):22s} {res['c2'][k]:7.2f} (p {CHI2.sf(res['c2'][k], nb):.3g}); full-cov {res['c2cov'][k]:7.2f}")

# ---------------- main (data or MUTATE)
T0 = model_table(GAM, 0.0, RT)
for ft, a0 in A0.items():
    re = [r_edge(Mb[i], a0, f) for f in (0.10, 0.18) for i in used]
    P(f"{ft}: SAGA hosts r_edge median f0.10 {np.median(re[:len(used)]):.0f} kpc, f0.18 {np.median(re[len(used):]):.0f} kpc")
vdat = V.copy()
if MUT:
    rngm = np.random.default_rng(56299); sc = np.array([np.interp(R[k], RP, T0[("c",), sh[k]]) if sh[k] in used else 100.0 for k in range(len(R))])
    vdat = draw_trunc(sc, rngm)[0]; P("MUTATE: velocities replaced by draws from the NFW model (c)")
res = analyse(vdat, sel, T0); report(res, "PRIMARY: all samples, 2 mass x 4 radial bins, beta 0, eps 20, r_t 1 Mpc")
summary = {}
for ft in A0:
    summary[ft] = dict(verdict=verdict(res["c2"], ft), chi2_a=res["c2"][("a", ft)], chi2_b18=res["c2"][("b", ft, 0.18)],
                       chi2_b10=res["c2"][("b", ft, 0.1)], chi2_c=res["c2"][("c",)], chi2_clim=res["c2"][("c_lim",)],
                       p_a=float(CHI2.sf(res["c2"][("a", ft)], 8)), p_b18=float(CHI2.sf(res["c2"][("b", ft, 0.18)], 8)),
                       p_c=float(CHI2.sf(res["c2"][("c",)], 8)))
    fc = {f: float(np.sum(((res["mv"][("b", ft, f)] - res["mv"][("a", ft)]) / res["err"]) ** 2)) for f in FGRID}
    det = [f for f in FGRID if fc[f] >= 9]; summary[ft]["forecast_dchi2"] = fc
    summary[ft]["detectable_fret_min"] = min(det) if det else None
    P(f"\n{ft}: VERDICT {summary[ft]['verdict']}; forecast dchi2(b-a) by f_ret: " + ", ".join(f"{f}:{fc[f]:.1f}" for f in FGRID)
      + f"; detectable f_ret >= {summary[ft]['detectable_fret_min']}")

if MUT:
    det = summary["canonical"]["verdict"].startswith("NFW") or "NFW" in summary["canonical"]["verdict"] or summary["canonical"]["p_a"] <= 0.01
    P(f"MUTATE detected: {det}")
    json.dump(dict(summary=summary), open(os.path.join(HERE, f"cfg562_saga_dispersion{TAG}_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg562_saga_dispersion{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if det else 0)

# ---------------- reported variants
var = {}
KS = [("a", "canonical"), ("a", "alt"), ("b", "canonical", 0.18), ("b", "alt", 0.18), ("b", "canonical", 0.1), ("c",), ("c_lim",)]
def short(r): return {name(k): round(r["c2"][k], 2) for k in KS}
r = analyse(vdat, selGS, T0, models=KS, nboot=500); report(r, "VARIANT Gold+Silver"); var["gold_silver"] = short(r)
r = analyse(vdat, sel, T0, mass_split=False, models=KS, nboot=500); report(r, "VARIANT all-host stack (4 bins)", 4); var["all_stack"] = short(r)
for e in (0.0, 40.0):
    r = analyse(vdat, sel, T0, eps=e, models=KS, nboot=500); report(r, f"VARIANT eps {e}"); var[f"eps{e:.0f}"] = short(r)
Tb = model_table(GAM, 0.3, RT); r = analyse(vdat, sel, Tb, models=KS, nboot=500); report(r, "VARIANT beta 0.3"); var["beta0.3"] = short(r)
for rt in (600.0, 3000.0):
    Tr = model_table(GAM, 0.0, rt); r = analyse(vdat, sel, Tr, models=KS, nboot=500); report(r, f"VARIANT r_t {rt:.0f} kpc"); var[f"rt{rt:.0f}"] = short(r)

# unbinned likelihood (+ interloper mixture)
P("\n== unbinned log-likelihood (zero free parameters) and with a fitted uniform interloper fraction")
ub = {}
idx = np.where(sel)[0]
for k in KS + [("b", "canonical", 1.0)]:
    s = np.sqrt(np.array([np.interp(R[j], RP, T0[k, sh[j]]) for j in idx]) ** 2 + EPS ** 2); v = vdat[idx]
    pg = np.exp(-0.5 * (v / s) ** 2) / (s * math.sqrt(2 * math.pi)) / (ndtr(VT / s) - ndtr(-VT / s))
    L0 = float(np.log(pg).sum()); fs = np.linspace(0, 0.6, 601)
    Lm = [float(np.log((1 - f) * pg + f / (2 * VT)).sum()) for f in fs]; j = int(np.argmax(Lm))
    ub[name(k)] = dict(m2lnL=-2 * L0, m2lnL_mix=-2 * Lm[j], f_int=float(fs[j]))
    P(f"   {name(k):22s} -2lnL {-2*L0:9.2f}; with interlopers -2lnL {-2*Lm[j]:9.2f} at f_int {fs[j]:.3f}")

# ---------------- injection
P("\n== K-INJ injection (canonical footing)")
def inj(f_inj, n=20, seed=7000):
    rng = np.random.default_rng(seed); out = []
    s = np.array([np.interp(R[k], RP, T0[("b", "canonical", f_inj), sh[k]]) if sh[k] in used else 100.0 for k in range(len(R))])
    idx, b, nb = bin_ids(sel)
    for t in range(n):
        v = draw_trunc(s, rng)[0]; d = binned(v, idx, b, nb); e = np.nanstd(boot(v, idx, b, nb, 200, 900 + t), 0)
        out.append({k: float(np.sum(((d - res["mv"][k]) / e) ** 2)) for k in res["mv"]})
    return out
i18 = inj(0.18); dd = np.array([o[("a", "canonical")] - o[("b", "canonical", 0.18)] for o in i18])
frac = float(np.mean(dd > 9)); fc18 = summary["canonical"]["forecast_dchi2"][0.18]
checks["KINJ_018"] = bool(np.median(dd) > 0 and ((fc18 >= 9 and frac >= 0.5) or (fc18 < 9 and frac <= 0.5)))
P(f"   f_ret 0.18: median dchi2(a-b) {np.median(dd):.2f}, fraction SUPPLY EDGE SEEN {frac:.2f}, forecast {fc18:.2f} -> {checks['KINJ_018']}")
i1 = inj(1.0, seed=7100); cand = [("a", "canonical"), ("b", "canonical", 0.1), ("b", "canonical", 0.18), ("b", "canonical", 1.0), ("c",)]
nwin = sum(min(cand, key=lambda k: o[k]) == ("b", "canonical", 1.0) for o in i1)
checks["KINJ_1.0"] = bool(nwin >= 15); P(f"   f_ret 1.0: (b,1.0) best in {nwin}/20 -> {checks['KINJ_1.0']}")

ser = lambda dct: {name(k): v for k, v in dct.items()}
json.dump(dict(summary=summary, checks=checks, gamma_t=GAM, gamma_t_GS=GAM_GS, medM=medM,
               data=dict(sigma=res["d"].tolist(), err=res["err"].tolist(), n=res["n"].tolist()),
               models={name(k): v.tolist() for k, v in res["mv"].items()}, chi2=ser(res["c2"]), chi2_cov=ser(res["c2cov"]),
               variants=var, unbinned=ub, inj018_dchi2=dd.tolist(), inj1_wins=int(nwin)),
          open(os.path.join(HERE, f"cfg562_saga_dispersion{TAG}_results.json"), "w"), indent=1, default=str)
P(f"\nchecks: {checks}")
open(os.path.join(HERE, f"cfg562_saga_dispersion{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(checks.values()) else 1)
