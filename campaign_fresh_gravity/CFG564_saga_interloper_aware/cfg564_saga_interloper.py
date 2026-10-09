#!/usr/bin/env python3
"""CFG564: SAGA DR3 satellite kinematics with the interloper fraction FIXED from SAGA's own redshift catalogue (Table C2).
See FROZEN_CRITERIA.md.  Run:  python3 cfg564_saga_interloper.py --stage power | --stage score | --mutate"""
import os, sys, json, math, io, contextlib, hashlib, warnings
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr, ndtri
from astropy.table import Table
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, ROOT)
D562 = os.path.join(ROOT, "CFG562_saga_satellite_dispersion"); EXT = os.path.join(ROOT, "_external_data", "cfg564")
MUT = "--mutate" in sys.argv
STAGE = "mutate" if MUT else (sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "score")
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def save(tag, obj, code):
    json.dump(obj, open(os.path.join(HERE, f"cfg564_{tag}_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg564_{tag}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(code)
G, MSUN, KPC, H, CKMS = 6.674e-11, 1.989e30, 3.0857e19, 0.7, 299792.458
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; COSMIC = 0.1200 / 0.02237
VT, EPS, RT = 275.0, 20.0, 1000.0
REDGES = np.array([30., 60., 110., 190., 300.])
RHOC = 3 * (H * 100 * 1e3 / 3.0857e22) ** 2 / (8 * math.pi * G)
def nu(y): return C.nu_mono(np.atleast_1d(np.asarray(y, float)))

# ---------------- K0 data
SHA = {os.path.join(D562, "data", "saga-dr3-tableC1.txt"): "278239bbdbebb6093555b65fd91dbc3ec6bebf225c81c035ca0e8e8ae0a595bf",
       os.path.join(D562, "data", "saga-dr3-tableC3.txt"): "14c0841d13b270468dee202f3246dd671f1e1ce05f83c66d33ff41c291d75f8b",
       os.path.join(EXT, "saga-dr3-tableC2.txt"): "91e8ab349c0f54f526f7c43e9f2cf4d6cce0a0d3a31a1c4054e694f139dde3cd"}
for f, h in SHA.items():
    assert hashlib.sha256(open(f, "rb").read()).hexdigest() == h, f
checks = {"K0_sha256": True}
hosts = Table.read(os.path.join(D562, "data", "saga-dr3-tableC1.txt"), format="ascii.mrt")
sats = Table.read(os.path.join(D562, "data", "saga-dr3-tableC3.txt"), format="ascii.mrt")
zc = Table.read(os.path.join(EXT, "saga-dr3-tableC2.txt"), format="ascii.mrt")
HID = list(hosts["HOSTID"]); hidx = {h: i for i, h in enumerate(HID)}
lMs = np.array(hosts["log(M*)"], float)
lHI = np.ma.filled(np.ma.masked_invalid(np.ma.array(hosts["log(MHI)"], dtype=float)), np.nan)
Mb = np.where(np.isfinite(lHI), 10 ** lMs + 1.33 * 10 ** np.nan_to_num(lHI), 1.2 * 10 ** lMs)
lMh_lim = np.array(hosts["log(Mhalo)"], float)
HRV = np.array(hosts["HRV"], float); DIST = np.array(hosts["Dist"], float); DM = np.array(hosts["DistMod"], float)
HRA = np.radians(np.array(hosts["RAdeg"], float)); HDE = np.radians(np.array(hosts["DEdeg"], float))
sh = np.array([hidx[h] for h in sats["HOSTID"]]); R = np.array(sats["Rhost"], float)
V = np.array(sats["DVhost"], float); samp = np.array(sats["sample"], int)
sel = (R >= REDGES[0]) & (R < REDGES[-1]); selGS = sel & (samp <= 2)
P(f"stage {STAGE}; hosts {len(HID)}; satellites {len(R)}, primary {sel.sum()}; C2 rows {len(zc)}")

# ---------------- K1 geometry of the redshift catalogue
zh = np.array([hidx.get(h, -1) for h in zc["HOSTID"]]); z = np.array(zc["z"], float)
ok = (zh >= 0) & (z > 0); zh, z = zh[ok], z[ok]
ra, de = np.radians(np.array(zc["RAdeg"], float)[ok]), np.radians(np.array(zc["DEdeg"], float)[ok])
rmag = np.array(zc["rmag"], float)[ok]; oid = np.array(zc["OBJID"])[ok]; zsamp = np.array(zc["sample"], int)[ok]
cs = np.sin(de) * np.sin(HDE[zh]) + np.cos(de) * np.cos(HDE[zh]) * np.cos(ra - HRA[zh])
Rz = DIST[zh] * 1e3 * np.arccos(np.clip(cs, -1, 1))
zhost = HRV[zh] / CKMS
DVF = {"relativistic": CKMS * (z - zhost[...]) / (1 + zhost), "cz-HRV": CKMS * z - HRV[zh]}
pos = {o: k for k, o in enumerate(oid)}; m = np.array([pos.get(o, -1) for o in sats["OBJID"]])
found = float(np.mean(m >= 0)); mm = m >= 0
dR = float(np.median(np.abs(Rz[m[mm]] - R[mm])))
DV = None
for nm, dv in DVF.items():
    ddv = float(np.median(np.abs(dv[m[mm]] - V[mm])))
    passed = found >= 0.99 and dR < 1 and ddv < 2
    P(f"K1 geometry ({nm}): C3 found in C2 {found:.3f}; median |dR| {dR:.3f} kpc; median |d dv| {ddv:.3f} km/s -> {passed}")
    if passed and DV is None: DV, DVNAME = dv, nm
checks["K1_geometry"] = DV is not None
if DV is None:
    P("K1 failed for both dv formulas: lane stops, no verdict"); save(STAGE, dict(checks=checks), 1)

# ---------------- interloper estimate
Mabs_sat = np.array(sats["rmag"], float) - DM[sh]; MLO, MHI = Mabs_sat[sel].min(), Mabs_sat[sel].max()
Mabs = rmag - DM[zh]; magok = (Mabs >= MLO) & (Mabs <= MHI)
rin = (Rz >= REDGES[0]) & (Rz < REDGES[-1]); rbin = np.digitize(Rz, REDGES) - 1
n_obs = np.bincount(np.digitize(R[sel], REDGES) - 1, minlength=4).astype(float)
def sideband(vlo, vhi):
    s = rin & magok & (np.abs(DV) >= vlo) & (np.abs(DV) < vhi)
    return np.bincount(rbin[s], minlength=4).astype(float)
def fint_flat(vhi):
    Ns = sideband(VT, vhi); nint = Ns * (2 * VT) / (2 * (vhi - VT))
    return np.minimum(nint / n_obs, 0.9), Ns, nint
FINT, NSIDE, NINT = fint_flat(1000.0)
win_all = rin & magok & (np.abs(DV) < VT)
P(f"\nmagnitude window M_r [{MLO:.2f}, {MHI:.2f}]; dv formula {DVNAME}")
P(f"C2 objects in window (30-300 kpc, mag-matched): {win_all.sum()}, of which flagged satellites {np.sum(win_all & (zsamp > 0))}")
for k in range(4):
    P(f"  bin {REDGES[k]:.0f}-{REDGES[k+1]:.0f}: n_obs {n_obs[k]:.0f}; sideband 275-1000 N {NSIDE[k]:.0f} (+-{math.sqrt(NSIDE[k]):.1f}) "
      f"-> n_int {NINT[k]:.2f} (+-{math.sqrt(NSIDE[k])*550/1450:.2f}); f_int {FINT[k]:.3f}")
P(f"  overall expected interloper fraction {NINT.sum()/n_obs.sum():.3f}")
F2000 = fint_flat(2000.0)[0]
sb = rin & magok & (np.abs(DV) >= VT) & (np.abs(DV) < 3000.0); x = np.abs(DV[sb])
VSG = np.logspace(2, math.log10(20000), 2000)
llv = [np.sum(-x / vs) - len(x) * math.log(vs * (math.exp(-VT / vs) - math.exp(-3000 / vs))) for vs in VSG]
VS = float(VSG[int(np.argmax(llv))])
Ns3 = np.bincount(rbin[sb], minlength=4).astype(float)
ratio = (1 - math.exp(-VT / VS)) / (math.exp(-VT / VS) - math.exp(-3000 / VS))
FSLOPE = np.minimum(Ns3 * ratio / n_obs, 0.9)
P(f"variant sideband 275-2000: f_int {np.round(F2000, 3).tolist()}; sloped: v_s {VS:.0f} km/s, f_int {np.round(FSLOPE, 3).tolist()}")

# ---------------- models (CFG562, unchanged)
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
    return np.where(r <= re, g, G * M * (1 + COSMIC / f) * MSUN / (r * KPC) ** 2)
def g_nfw(r, M, Mh):
    c = c_dm(Mh); R200 = (3 * Mh * MSUN / (4 * math.pi * 200 * RHOC)) ** (1 / 3) / KPC; x = r / (R200 / c)
    m = lambda x: np.log(1 + x) - x / (1 + x)
    return G * (Mh * m(x) / m(c) + M) * MSUN / (r * KPC) ** 2
RP = np.array(list(np.linspace(25, 310, 30)))
def sig_los(gfun, gam, beta, rg, Rp=RP, rt=RT):
    g = gfun(rg) * KPC / 1e6
    integ = rg ** (2 * beta) * rg ** (-gam) * g
    seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(rg)
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    lP = np.log(np.maximum(rg ** (-2 * beta) * cum, 1e-300)); out = []
    for Rv in Rp:
        umax = math.sqrt(rt ** 2 - Rv ** 2); u = np.concatenate([[0], np.logspace(-2, math.log10(umax), 500)])
        r = np.sqrt(Rv ** 2 + u ** 2); Pi = np.exp(np.interp(np.log(r), np.log(rg), lP)); Pi[r >= rt] = 0
        num = np.trapz((1 - beta * Rv ** 2 / r ** 2) * Pi, u); den = np.trapz(r ** (-gam), u)
        out.append(math.sqrt(max(num / den, 0)))
    return np.array(out)
def fit_gamma(Rs):
    a, b = REDGES[0], REDGES[-1]; L = np.log(Rs).sum(); n = len(Rs)
    def nll(gm):
        k = 2 - gm
        norm = math.log(b / a) if abs(k + 1) < 1e-9 else (b ** (k + 1) - a ** (k + 1)) / (k + 1)
        return -(k * L - n * math.log(norm))
    gs = np.linspace(0.5, 4.0, 3501); return gs[np.argmin([nll(x) for x in gs])]
GAM = fit_gamma(R[sel]); P(f"tracer gamma_t {GAM:.3f} (CFG562 1.992)")
used = sorted(set(sh[sel])); Mh_am = {i: 10 ** inv_moster(lMs[i]) for i in used}
KEYS = [("a", "canonical"), ("a", "alt"), ("b", "canonical", 0.18), ("b", "alt", 0.18), ("b", "canonical", 0.1),
        ("b", "alt", 0.1), ("c",), ("c_lim",), ("b", "canonical", 1.0)]
def name(k): return k[0] if len(k) == 1 else (f"a[{k[1]}]" if k[0] == "a" else f"b[{k[1]},f={k[2]}]")
def model_sig(beta):
    rg = np.logspace(np.log10(0.5), np.log10(RT), 700); T = {}
    for i in used:
        M = Mb[i]
        T[("c",), i] = sig_los(lambda r: g_nfw(r, M, Mh_am[i]), GAM, beta, rg)
        T[("c_lim",), i] = sig_los(lambda r: g_nfw(r, M, 10 ** lMh_lim[i]), GAM, beta, rg)
        for ft, a0 in A0.items():
            T[("a", ft), i] = sig_los(lambda r: g_law(r, M, a0), GAM, beta, rg)
            for f in (0.1, 0.18, 1.0):
                T[("b", ft, f), i] = sig_los(lambda r: g_sup(r, M, a0, f), GAM, beta, rg)
    idx = np.where(sel)[0]
    return {k: np.sqrt(np.array([np.interp(R[j], RP, T[k, sh[j]]) for j in idx]) ** 2 + EPS ** 2) for k in KEYS}
S0 = model_sig(0.0)
IDX = np.where(sel)[0]; KB = np.digitize(R[IDX], REDGES) - 1

# ---------------- likelihood
def pg_of(v, s):
    return np.exp(-0.5 * (v / s) ** 2) / (s * math.sqrt(2 * math.pi)) / (ndtr(VT / s) - ndtr(-VT / s))
def m2lnl(v, s, f, pint=None):
    """v (..., n); f per satellite (n,) ; pint per-satellite interloper pdf or None (uniform)."""
    pi = 1 / (2 * VT) if pint is None else pint
    return -2 * np.sum(np.log((1 - f) * pg_of(v, s) + f * pi), axis=-1)
FS = FINT[KB]
def SET(ft): return [("a", ft), ("b", ft, 0.18), ("c",)]
def verdict(L, ft):
    s = SET(ft); vals = np.array([L[k] for k in s]); j = int(np.argmin(vals)); d = vals - vals[j]
    if np.all(np.delete(d, j) > 9): return ["LAW-FLAT", "SUPPLY EDGE", "NFW-PREFERRED"][j]
    return "NON-DISCRIMINATING"
def draw(s, rng, n, f):
    sig = np.broadcast_to(s, (n, len(s))); lo, hi = ndtr(-VT / sig), ndtr(VT / sig)
    v = sig * ndtri(lo + (hi - lo) * rng.random((n, len(s))))
    rep = rng.random((n, len(s))) < f
    return np.where(rep, rng.uniform(-VT, VT, (n, len(s))), v)

GEN = lambda ft: [("a", ft), ("b", ft, 0.18), ("b", ft, 0.1), ("c",)]
if STAGE == "power":
    P("\n== STAGE 1 POWER (positions + f_int only; no satellite velocities used)")
    pw = {}; kinj = {}
    for ft in A0:
        pw[ft] = {}
        for gk in GEN(ft):
            rng = np.random.default_rng(5640 + len(name(gk)) * 7 + (ft == "alt"))
            v = draw(S0[gk], rng, 300, FS)
            L = {k: m2lnl(v, S0[k], FS) for k in SET(ft) + [("b", ft, 0.1)]}
            vd = [verdict({k: L[k][t] for k in L}, ft) for t in range(300)]
            fr = {x: vd.count(x) / 300 for x in ["LAW-FLAT", "SUPPLY EDGE", "NFW-PREFERRED", "NON-DISCRIMINATING"]}
            med = {name(k): float(np.median(L[k] - L[gk if gk in L else SET(ft)[0]])) for k in L}
            pw[ft][name(gk)] = dict(verdict_frac=fr, median_dm2lnL_vs_generator=med,
                                    median_m2lnL={name(k): float(np.median(L[k])) for k in L})
            P(f"  {ft} generator {name(gk):20s} verdicts " + ", ".join(f"{a} {b:.2f}" for a, b in fr.items())
              + " | median Delta vs generator: " + ", ".join(f"{a} {b:+.1f}" for a, b in med.items()))
            if ft == "canonical" and gk != ("b", ft, 0.1):
                kinj[name(gk)] = bool(min(SET(ft), key=lambda k: np.median(L[k])) == gk)
    rng = np.random.default_rng(5649); v = draw(S0[("a", "canonical")], rng, 50, FS)
    AG = np.linspace(0, 1 / FINT.max(), 401)
    Ahat = [AG[np.argmin([m2lnl(v[t], S0[("a", "canonical")], np.minimum(A * FS, 1)) for A in AG])] for t in range(50)]
    kinj["A_scale_median"] = float(np.median(Ahat))
    checks["K3_injection"] = bool(all(kinj[n] for n in kinj if n != "A_scale_median") and 0.8 <= kinj["A_scale_median"] <= 1.2)
    P(f"K3 injection-recovery (canonical): {kinj} -> {checks['K3_injection']}")
    save("power", dict(checks=checks, f_int=FINT.tolist(), n_obs=n_obs.tolist(), n_side=NSIDE.tolist(), n_int=NINT.tolist(),
                       dv_formula=DVNAME, mag_window=[MLO, MHI], power=pw, K3=kinj), 0)

vdat = V[IDX].copy()
if MUT:
    vdat = draw(S0[("c",)], np.random.default_rng(56499), 1, FS)[0]
    P("MUTATE: velocities replaced by NFW-Moster draws plus interlopers at the fixed f_int")
P("\n== STAGE 2 SCORE: primary (fixed f_int, flat sideband 275-1000, isotropic)")
Lp = {k: float(m2lnl(vdat, S0[k], FS)) for k in KEYS}
summ = {}
for ft in A0:
    vd = verdict(Lp, ft); best = min(Lp[k] for k in SET(ft))
    summ[ft] = dict(verdict=vd, delta={name(k): Lp[k] - best for k in SET(ft) + [("b", ft, 0.1), ("c_lim",)]})
    P(f"  {ft}: VERDICT {vd}; Delta(-2lnL): " + ", ".join(f"{a} {b:+.2f}" for a, b in summ[ft]["delta"].items()))
for k in KEYS: P(f"   -2lnL {name(k):22s} {Lp[k]:9.2f}")
if MUT:
    det = summ["canonical"]["verdict"] != "LAW-FLAT"
    P(f"MUTATE detected (verdict not LAW-FLAT): {det}")
    save("mutate", dict(summary=summ, m2lnL={name(k): v for k, v in Lp.items()}), 1 if det else 0)

# ---------------- K2 reproduce CFG562 free constant-f
j562 = json.load(open(os.path.join(D562, "cfg562_saga_dispersion_results.json")))["unbinned"]
fs = np.linspace(0, 0.6, 601); k2 = []; free = {}
for k in KEYS:
    Lm = np.array([m2lnl(vdat, S0[k], np.full(len(vdat), f)) for f in fs]); j = int(np.argmin(Lm))
    free[name(k)] = dict(m2lnL=float(Lm[j]), f=float(fs[j]))
    if name(k) in j562:
        k2.append(abs(Lm[j] - j562[name(k)]["m2lnL_mix"]) < 0.05 and abs(fs[j] - j562[name(k)]["f_int"]) < 0.002)
checks["K2_cfg562"] = bool(all(k2)) and len(k2) >= 7
P(f"K2 reproduce CFG562 free-f: {sum(k2)}/{len(k2)} match -> {checks['K2_cfg562']}")
for k in KEYS: P(f"   free constant f {name(k):22s} -2lnL {free[name(k)]['m2lnL']:9.2f} f {free[name(k)]['f']:.3f}")

# ---------------- reported variants
var = {}
AG = np.linspace(0, 1 / FINT.max(), 401); var["free_shape_A"] = {}
for k in KEYS:
    Lm = np.array([m2lnl(vdat, S0[k], np.minimum(A * FS, 1)) for A in AG]); j = int(np.argmin(Lm))
    var["free_shape_A"][name(k)] = dict(m2lnL=float(Lm[j]), A=float(AG[j]))
def vtab(label, L):
    out = {ft: dict(verdict=verdict(L, ft), delta={name(k): L[k] - min(L[q] for q in SET(ft))
                                                    for k in SET(ft) + [("b", ft, 0.1), ("c_lim",)]}) for ft in A0}
    P(f"  {label}: " + " | ".join(f"{ft} {o['verdict']} (" + ", ".join(f"{a} {b:+.1f}" for a, b in o['delta'].items()) + ")"
                                  for ft, o in out.items()))
    return out
P("\n== REPORTED variants")
var["free_shape"] = vtab("free shape A", {k: var["free_shape_A"][k_]["m2lnL"] for k in KEYS for k_ in [name(k)]})
P("   fitted A: " + ", ".join(f"{a} {b['A']:.2f}" for a, b in var["free_shape_A"].items()))
var["free_const"] = vtab("free constant f", {k: free[name(k)]["m2lnL"] for k in KEYS})
F2 = F2000[KB]; var["side2000"] = vtab("sideband 275-2000", {k: float(m2lnl(vdat, S0[k], F2)) for k in KEYS})
pint = np.exp(-np.abs(vdat) / VS) / (2 * VS * (1 - math.exp(-VT / VS))); FSL = FSLOPE[KB]
var["sloped"] = vtab(f"sloped sideband v_s {VS:.0f}", {k: float(m2lnl(vdat, S0[k], FSL, pint)) for k in KEYS})
Sb = model_sig(0.3); var["beta0.3"] = vtab("beta 0.3", {k: float(m2lnl(vdat, Sb[k], FS)) for k in KEYS})
gs = samp[IDX] <= 2
var["gold_silver"] = vtab("Gold+Silver", {k: float(m2lnl(vdat[gs], S0[k][gs], FS[gs])) for k in KEYS})
var["no_interlopers"] = vtab("f_int = 0 (CFG562 zero-parameter)", {k: float(m2lnl(vdat, S0[k], 0 * FS)) for k in KEYS})
# goodness of fit of the best model in S (canonical and alt)
gof = {}
for ft in A0:
    bk = min(SET(ft), key=lambda k: Lp[k]); v = draw(S0[bk], np.random.default_rng(5648), 500, FS)
    gof[ft] = dict(model=name(bk), p=float(np.mean(m2lnl(v, S0[bk], FS) >= Lp[bk])))
P(f"goodness of fit (fraction of best-model mocks with -2lnL >= data): {gof}")
pw = json.load(open(os.path.join(HERE, "cfg564_power_results.json")))
lowp = {ft: {g: o["verdict_frac"] for g, o in pw["power"][ft].items()} for ft in A0}
P(f"stage-1 power checks: {pw['checks']}")
checks.update({k: v for k, v in pw["checks"].items() if k == "K3_injection"})
P(f"\nchecks: {checks}")
save("score", dict(summary=summ, checks=checks, m2lnL={name(k): v for k, v in Lp.items()}, free_const=free,
                   variants=var, gof=gof, f_int=FINT.tolist(), f_int_2000=F2000.tolist(), f_int_sloped=FSLOPE.tolist(),
                   v_s=VS, dv_formula=DVNAME, power_verdict_frac=lowp), 0 if all(checks.values()) else 1)
