#!/usr/bin/env python3
"""p64 -- raw SPARC with the fewest assumptions: (A) is the cold energy per baryon the same for gas and stars (within-galaxy
contrast), (B) what kappa do the TRGB gas-dominated galaxies give with no H0 anywhere, (C) one flux scale for them.

Criteria: FROZEN_CRITERIA.md (d8b8fa3e4) + Amendment 1 (3ed1622da: run condition, two implementation readings, (C) UNTESTED)
+ Amendment 2 (a07bf55af: the frozen M2 window looks mis-set; run as frozen). Written 2026-10-20 by a parallel session on the
owner's instruction ("keep swinging all of them"), from the frozen text only.
Kernel: simple mu, inverted point by point: a0_i = g_obs (g_obs - g_bar)/g_bar where g_obs > g_bar. K1 uses nu_mono (CFG442's code).
Light: numpy/scipy, one process, seconds. Run from this directory:
    OMP_NUM_THREADS=1 nice -n 10 python3 p64_raw_sparc_minimal.py > p64_raw_sparc_minimal.out
    MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 p64_raw_sparc_minimal.py > p64_raw_sparc_minimal_MUTATE.out
MUTATE: M1 gas x0.7 in (A); M2 all distances x1.10 in (B); M3 omega_Lambda labels swapped in (B).
kappa = 1/2 FITTED. Not theory closed.
"""
import contextlib, io, json, math, os, re, sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "campaign_fresh_gravity"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
MUT = os.environ.get("MUTATE") == "1"
KPC = 3.0857e19
G_SI, C_SI, MPC = 6.67430e-11, 2.99792458e8, 3.0856775814913673e22
OUT, checks = [], []


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": detail, "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def scaled(g, fD=1.0, inc_new=None):
    """distance factor fD (R ~ D, V_bar ~ sqrt D, V_obs fixed) and inclination change (V_obs ~ 1/sin i)"""
    h = dict(g)
    h["R"] = g["R"] * fD
    s = math.sqrt(fD)
    for k in ("Vgas", "Vdisk", "Vbul"):
        h[k] = g[k] * s
    if inc_new is not None and g["meta"]["Inc"] > 0:
        f = math.sin(math.radians(g["meta"]["Inc"])) / math.sin(math.radians(inc_new))
        h["Vobs"] = g["Vobs"] * f
        h["eV"] = g["eV"] * f
    return h


def accel(g, U=0.5, fgas=1.0):
    R = g["R"] * KPC
    vg2 = fgas * np.sign(g["Vgas"]) * g["Vgas"] ** 2
    gb = (vg2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / R
    go = (g["Vobs"] * 1e3) ** 2 / R
    return go, gb


def classes(g):
    """fiducial classification (Upsilon_d 0.5, f_gas 1): gas- and star-dominated points (Amendment 1, reading 1)"""
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vs2 = 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    vb2 = vg2 + vs2
    ok = (vb2 > 0) & (g["Vobs"] > 0) & (g["R"] > 0)
    return ok & (vg2 >= 0.7 * vb2), ok & (vs2 >= 0.7 * vb2)


def log_a0_points(g, mask, U=0.5, fgas=1.0):
    go, gb = accel(g, U, fgas)
    m = mask & (gb > 0) & (go > gb)
    return np.log10(go[m] * (go[m] - gb[m]) / gb[m])


nu_s = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))


def log_a0_points_rar(g, mask, U=0.5, fgas=1.0):
    """frozen cross-check: RAR kernel nu_e(y) = 1/(1 - exp(-sqrt y)) inverted per point: a0 = g_bar / ln(1 - g_bar/g_obs)^2"""
    go, gb = accel(g, U, fgas)
    m = mask & (gb > 0) & (go > gb)
    return np.log10(gb[m] / np.log(1 - gb[m] / go[m]) ** 2)

# ============================================================================================ load
GAL = [g for g in C.load_sparc() if g["meta"]]
P("p64  raw SPARC, fewest assumptions" + ("  [MUTATE: M1 gas x0.7 (A); M2 D x1.10 (B); M3 omega labels swapped (B)]" if MUT else ""))
P("kernel: simple mu, a0_i = g_obs (g_obs - g_bar)/g_bar (g_obs > g_bar); kappa = 1/2 FITTED; not theory closed\n")

# ============================================================================================ (A)
A_S = []
for g in GAL:
    if g["meta"]["Q"] > 2 or g["meta"]["Inc"] < 30:
        continue
    gm, sm = classes(g)
    if len(log_a0_points(g, gm)) >= 3 and len(log_a0_points(g, sm)) >= 3:
        A_S.append((g, gm, sm))
P(f"(A) within-galaxy gas-vs-star contrast: {len(A_S)} galaxies (Q <= 2, i >= 30 deg, >= 3 valid points of each class at the fiducial)")
UD = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
FG = [0.70, 0.85, 1.00, 1.15]
fg_mut = 0.7 if MUT else 1.0
grid = {}
for U in UD:
    for fgas in FG:
        dg = []
        for g, gm, sm in A_S:
            la_g = log_a0_points(g, gm, U, fgas * fg_mut)
            la_s = log_a0_points(g, sm, U, fgas * fg_mut)
            if len(la_g) >= 2 and len(la_s) >= 2:
                dg.append(float(np.median(la_g) - np.median(la_s)))
        dg = np.array(dg)
        rng = np.random.default_rng(64)
        bs = np.array([np.median(dg[rng.integers(0, len(dg), len(dg))]) for _ in range(2000)]) if len(dg) else np.array([np.nan])
        med, sd = float(np.median(dg)) if len(dg) else float("nan"), float(np.std(bs))
        grid[(U, fgas)] = dict(n=len(dg), median=med, sd=sd, z=med / sd if sd > 0 else float("nan"))
P("    median Delta_g = median log a0(gas) - median log a0(stars) [dex], galaxy bootstrap 2000 (seed 64); rows Upsilon_d, cols f_gas")
P("     Ud   " + "  ".join(f"f_gas {f:4.2f}         " for f in FG))
for U in UD:
    P(f"    {U:3.1f}  " + "  ".join(f"{grid[(U, f)]['median']:+.3f}+-{grid[(U, f)]['sd']:.3f} (n{grid[(U, f)]['n']:3d})" for f in FG))
core = [(U, f) for U in UD if 0.4 <= U <= 0.8 for f in FG if 0.85 <= f <= 1.15]
contrast = all(abs(grid[k]["z"]) > 3 for k in core)
absorbed = any(abs(grid[k]["z"]) < 1 for k in core)
nmin = min(grid[k]["n"] for k in core)
vA = "UNDETERMINED" if nmin < 8 else ("CONTRAST" if contrast else ("ABSORBED" if absorbed else "UNDETERMINED"))
sign = np.sign(grid[(0.5, 1.0)]["median"])
P(f"    verdict (A): {vA}" + (f"; sign {'negative (gas points imply less cold energy per baryon)' if sign < 0 else 'positive'}" if vA == "CONTRAST" else ""))
P("    reading rule: CONTRAST is consistent with (1) cold energy tracking stars more than cold gas, or (2) a gas-mass-scale"
  " error / uncorrected pressure in gas-rich outskirts; never a cold-energy detection")
# distance / inclination lever at the fiducial (report)
lev_D, lev_i = [], []
for g, gm, sm in A_S:
    base = np.median(log_a0_points(g, gm)) - np.median(log_a0_points(g, sm))
    eD = g["meta"]["eD"] / max(g["meta"]["D"], 1e-9)
    for sgn in (+1, -1):
        h = scaled(g, 1 + sgn * eD)
        lev_D.append(abs(np.median(log_a0_points(h, gm)) - np.median(log_a0_points(h, sm)) - base))
        h = scaled(g, 1.0, g["meta"]["Inc"] + sgn * g["meta"]["eInc"])
        lev_i.append(abs(np.median(log_a0_points(h, gm)) - np.median(log_a0_points(h, sm)) - base))
dg_rar = [float(np.median(log_a0_points_rar(g, gm)) - np.median(log_a0_points_rar(g, sm))) for g, gm, sm in A_S]
rngr = np.random.default_rng(64)
bs_r = [np.median(np.array(dg_rar)[rngr.integers(0, len(dg_rar), len(dg_rar))]) for _ in range(2000)]
A_rar = dict(median=float(np.median(dg_rar)), sd=float(np.std(bs_r)))
P(f"    RAR-kernel cross-check (frozen; fiducial cell): median Delta_g {A_rar['median']:+.3f} +- {A_rar['sd']:.3f} dex"
  f" (simple mu {grid[(0.5, 1.0)]['median']:+.3f}): the contrast is {'kernel-robust' if abs(A_rar['median']) > 3 * A_rar['sd'] else 'kernel-sensitive'}")
P(f"    D and i by +-1 sigma move Delta_g by a median {np.median(lev_D):.3f} / {np.median(lev_i):.3f} dex (the levers differ; report)")

# ============================================================================================ (B)
P("\n(B) kappa from the TRGB/Cepheid/SN gas-dominated galaxies (CFG449 S0 rule: f_D in {2,3,5}, Q <= 2, >= 3 gas points)")
def sel_points(g):                                              # CFG442's, unchanged
    vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
    vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return (vg2 >= 0.7 * vb2) & (vb2 > 0) & (g["Vobs"] > 0)
S0 = [g for g in GAL if g["meta"]["Q"] <= 2 and g["meta"]["fD"] in (2, 3, 5) and sel_points(g).sum() >= 3]
P(f"    S0: {len(S0)} galaxies: {', '.join(g['name'] for g in S0)}")
# K1: CFG442 per-galaxy single fits with nu_mono, CFG397's arrays/fit unchanged
def arrays442(gs, U):
    out = []
    for g in gs:
        m = sel_points(g); R = g["R"][m] * KPC; vg = g["Vgas"][m]
        b = (np.sign(vg) * vg ** 2 + U * g["Vdisk"][m] ** 2 + 1.4 * U * g["Vbul"][m] ** 2) * 1e6 / R
        o = (g["Vobs"][m] * 1e3) ** 2 / R
        w = 1 / (np.clip(g["eV"][m], 1, None) / np.clip(g["Vobs"][m], 1, None)) ** 2
        ok = (b > 0) & (o > 0)
        out.append((b[ok], o[ok], w[ok]))
    return out
def fit442(parts, nu=C.nu_mono):
    gb = np.concatenate([p[0] for p in parts]); go = np.concatenate([p[1] for p in parts]); w = np.concatenate([p[2] for p in parts])
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(nu(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.8, -9.3), method="bounded", options={"xatol": 1e-5}).x
ref = json.load(open(ROOT / "campaign_fresh_gravity/CFG442_a0_rung_expansion/cfg442_rung_results.json"))["per_galaxy"]
k1 = {g["name"]: (float(fit442(arrays442([g], 0.5))), ref[g["name"]]["log_a0_single"]) for g in S0 if g["name"] in ref}
k1_dev = max(abs(a - b) for a, b in k1.values()) if k1 else float("nan")
k1_ok = len(k1) == 10 and len(S0) == 10 and k1_dev <= 0.01
check("K1 CFG442 per-galaxy nu_mono single fits reproduced (code identity)", f"{len(k1)} matched, max |dev| {k1_dev:.4f} dex", k1_ok)

dfac = 1.10 if MUT else 1.0
S0m = [scaled(g, dfac) for g in S0]
per = {}
for g0, g in zip(S0, S0m):
    gm = sel_points(g0)
    la = log_a0_points(g, gm)
    x = float(np.median(la))
    eD = g0["meta"]["eD"] / max(g0["meta"]["D"], 1e-9)
    sD = 0.5 * abs(np.median(log_a0_points(scaled(g, 1 + eD), gm)) - np.median(log_a0_points(scaled(g, 1 - eD), gm)))
    si = 0.5 * abs(np.median(log_a0_points(scaled(g, 1.0, g0["meta"]["Inc"] + g0["meta"]["eInc"]), gm))
                   - np.median(log_a0_points(scaled(g, 1.0, g0["meta"]["Inc"] - g0["meta"]["eInc"]), gm)))
    hp, hm = dict(g), dict(g)
    hp["Vobs"], hm["Vobs"] = g["Vobs"] + g["eV"], np.maximum(g["Vobs"] - g["eV"], 1e-3)
    go, gb = accel(g); mm = gm & (gb > 0) & (go > gb)
    lap, lam_ = np.log10(accel(hp)[0][mm] * (accel(hp)[0][mm] - gb[mm]) / gb[mm]), None
    gom = accel(hm)[0][mm]
    lam_ = np.log10(np.clip(gom * (gom - gb[mm]) / gb[mm], 1e-30, None))
    sv_pt = 0.5 * np.abs(lap - lam_)
    sV = float(1.253 * np.median(sv_pt) / math.sqrt(max(len(sv_pt), 1)))
    per[g0["name"]] = dict(log_a0=x, n=len(la), sD=float(sD), si=float(si), sV=sV, sig=float(math.sqrt(sD ** 2 + si ** 2 + sV ** 2)))
P("    per galaxy (simple mu, Upsilon_d 0.5): log a0 = median over gas points; sigma = e_D (+) e_i (+) e_V")
for k, v in per.items():
    P(f"      {k:12s} n {v['n']:3d}  log a0 {v['log_a0']:+.3f} +- {v['sig']:.3f}  (D {v['sD']:.3f}, i {v['si']:.3f}, V {v['sV']:.3f})")
xs = np.array([v["log_a0"] for v in per.values()]); ss = np.array([v["sig"] for v in per.values()])
# E1 pooled weighted fit (Amendment 1, reading 2), E2 median, E3 mean, E4 ML with intrinsic scatter
parts = arrays442(S0m, 0.5)
E1 = float(fit442(parts, nu_s))
rng = np.random.default_rng(64)
bi = [rng.integers(0, len(S0m), len(S0m)) for _ in range(2000)]
E1b = [float(fit442([parts[i] for i in ix], nu_s)) for ix in bi[:500]]
E2, E3 = float(np.median(xs)), float(np.mean(xs))
E2b = [float(np.median(xs[ix])) for ix in bi]; E3b = [float(np.mean(xs[ix])) for ix in bi]
def nll(p):
    mu, lt = p; t2 = math.exp(2 * lt)
    v = ss ** 2 + t2
    return float(np.sum((xs - mu) ** 2 / v + np.log(v)))
best = min((minimize(nll, [E2, lt0], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8}) for lt0 in (-3.0, -1.5, -0.5)), key=lambda r: r.fun)
E4, tau = float(best.x[0]), float(math.exp(best.x[1]))
taus = np.linspace(0, 1.0, 1001)
prof = np.array([min(nll([m_, math.log(max(t_, 1e-6))]) for m_ in np.linspace(E4 - 0.6, E4 + 0.6, 241)) for t_ in taus])
tau_in = taus[prof <= prof.min() + 1]
mus = np.linspace(E4 - 0.6, E4 + 0.6, 1201)
pm = np.array([min(nll([m_, math.log(max(t_, 1e-6))]) for t_ in np.linspace(0, 1.0, 201)) for m_ in mus])
mu_in = mus[pm <= pm.min() + 1]
EST = {"E1 pooled weighted fit": (E1, float(np.std(E1b))), "E2 median over galaxies": (E2, float(np.std(E2b))),
       "E3 mean over galaxies": (E3, float(np.std(E3b))), "E4 ML with intrinsic scatter": (E4, 0.5 * float(mu_in.max() - mu_in.min()))}
P(f"    E4 intrinsic scatter tau = {tau:.3f} dex, Delta(-2lnL) = 1 interval [{tau_in.min():.3f}, {tau_in.max():.3f}]"
  f" -> tau {'consistent' if tau_in.min() == 0 else 'NOT consistent'} with 0")
# kappa: no H0 anywhere
cfg886 = (ROOT / "campaign_fresh_gravity/CFG886_ratio_fret_without_planck/cfg886.out").read_text()
m886 = re.search(r"\(a\) PRIMARY BAO\+BBN.*?h ([0-9.]+)\+-[0-9.]+\s+Om ([0-9.]+)\+-", cfg886)
h886, om886 = float(m886.group(1)), float(m886.group(2))
OMEGA = {"Planck 0.685 x 0.674^2": 0.685 * 0.674 ** 2, "CFG886 BAO+BBN (1-Om) h^2": (1 - om886) * h886 ** 2}
if MUT:
    k_ = list(OMEGA.keys()); OMEGA = {k_[0]: OMEGA[k_[1]], k_[1]: OMEGA[k_[0]]}         # M3: labels swapped
H100 = 1e5 / MPC
s_of = {k: C_SI * math.sqrt(G_SI * w * 3 * H100 ** 2 / (8 * math.pi * G_SI)) for k, w in OMEGA.items()}
P(f"    omega_Lambda: " + ", ".join(f"{k} = {w:.4f}" for k, w in OMEGA.items()) + "  (rho_L = omega 3 (100 km/s/Mpc)^2/(8 pi G); no H0)")
kap = {}
for en, (la, sl) in EST.items():
    row = {}
    for wn, s in s_of.items():
        kv = 10 ** la / s
        lo1, hi1 = 10 ** (la - sl) / s, 10 ** (la + sl) / s
        lo2, hi2 = 10 ** (la - 2 * sl) / s, 10 ** (la + 2 * sl) / s
        pos = "inside 1 sigma" if lo1 <= 0.5 <= hi1 else ("inside 2 sigma" if lo2 <= 0.5 <= hi2 else "outside 2 sigma")
        row[wn] = dict(kappa=kv, lo1=lo1, hi1=hi1, half=pos)
    kap[en] = dict(log_a0=la, sig=sl, by_omega=row)
    P(f"    {en:30s} log a0 {la:+.4f} +- {sl:.4f}  " + "  ".join(f"[{wn.split()[0]}] kappa {r['kappa']:.3f} ({r['half']})" for wn, r in row.items()))
E2_rar = float(np.median([np.median(log_a0_points_rar(g, sel_points(g0))) for g0, g in zip(S0, S0m)]))
P(f"    RAR-kernel cross-check (frozen): E2 log a0 {E2_rar:+.4f} -> " + ", ".join(f"[{wn.split()[0]}] kappa {10 ** E2_rar / s:.3f}" for wn, s in s_of.items()))
spread = max(v["log_a0"] for v in kap.values()) - min(v["log_a0"] for v in kap.values())
lever = []
for f in (10 ** 0.01, 10 ** 0.017):
    xs_f = [float(np.median(log_a0_points(scaled(g, f), sel_points(g0)))) for g0, g in zip(S0, S0m)]
    lever.append(float(np.median(xs_f) - E2))
P(f"    systematics: estimator spread {spread:.3f} dex; ladder zero point 0.01 / 0.017 dex in distance moves E2 by {lever[0]:+.4f} / {lever[1]:+.4f} dex")

# ============================================================================================ (C)
P("\n(C) one flux scale for the TRGB dwarfs: UNTESTED (Amendment 1: the SPARC table on disk has no coordinates and downloads are"
  " forbidden; the frozen pre-freeze expectation was already at most 2 of 10 in alpha.100's sky)")

# ============================================================================================ MUTATE checks
RES = dict(mutate=MUT, A_rar=A_rar, B_E2_rar=E2_rar, A=dict(n_gal=len(A_S), grid={f"{U}|{f}": v for (U, f), v in grid.items()}, verdict=vA,
                              lever_D=float(np.median(lev_D)), lever_i=float(np.median(lev_i))),
           B=dict(S0=[g["name"] for g in S0], K1=dict(ok=k1_ok, max_dev=k1_dev), per_galaxy=per, estimators=kap, tau=tau,
                  tau_interval=[float(tau_in.min()), float(tau_in.max())], spread=spread, ladder=lever, omega=OMEGA),
           C="UNTESTED", checks=checks)
if MUT:
    try:
        base = json.load(open(HERE / "p64_raw_sparc_minimal_results.json"))
        d_A = grid[(0.5, 1.0)]["median"] - base["A"]["grid"]["0.5|1.0"]["median"]
        check("M1 gas x0.7 moves the fiducial median Delta_g by > 0.05 dex", f"{d_A:+.3f} dex", abs(d_A) > 0.05)
        d_B = EST["E2 median over galaxies"][0] - base["B"]["estimators"]["E2 median over galaxies"]["log_a0"]
        check("M2 D x1.10 moves E2 log a0 into [-0.30, -0.15] dex (as frozen)", f"{d_B:+.3f} dex (Amendment 2 lever arithmetic: -0.083 to -0.124)",
              -0.30 <= d_B <= -0.15)
        k0 = base["B"]["estimators"]["E2 median over galaxies"]["by_omega"]
        names = list(k0.keys())
        swapped = all(abs(kap["E2 median over galaxies"]["by_omega"][names[i]]["kappa"] / 10 ** (d_B) -
                          k0[names[1 - i]]["kappa"]) < 1e-9 + 1e-6 * k0[names[1 - i]]["kappa"] for i in (0, 1))
        check("M3 omega labels swapped: the two kappa columns exchange (after removing M2's shift)", f"{swapped}", swapped)
    except OSError:
        P("MUTATE: run the normal mode first")
    json.dump(RES, open(HERE / "p64_raw_sparc_minimal_results_MUTATE.json", "w"), indent=1, default=float)
else:
    json.dump(RES, open(HERE / "p64_raw_sparc_minimal_results.json", "w"), indent=1, default=float)
P(f"\nchecks: {sum(c['pass'] for c in checks)}/{len(checks)} pass")
sys.exit(0 if all(c["pass"] for c in checks) else 1)
