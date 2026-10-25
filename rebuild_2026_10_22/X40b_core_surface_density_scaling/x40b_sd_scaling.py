#!/usr/bin/env python3
"""X40b_core_surface_density_scaling: can a framework-native rule (no new constant) raise the cold dark energy core surface
density at cluster masses while galaxies stay at a0/(2 pi G)?  Rules A (max(a0, g_b(r0))), A' (max(a0, g_N,tot(r0))),
B (a0 at formation epoch, DESI M-DEC), C (empirical S ~ M^alpha, reported only).

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (b09db13390). EM1's SPARC machinery and X30's cluster machinery
executed read-only as X38/X39; CFG922 BCG matched as X39; P4's group estimator executed read-only. One thread.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x40b_sd_scaling.py                  -> .out, _results.json
    X40B_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x40b_sd_scaling.py     -> max -> min (K2 must fail)
"""
import os, sys, json, math, time, resource, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUTATE = os.environ.get("X40B_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

# ------------------------------------------------------------------ EM1 + X30 read-only (as X38)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- backgrounds")], EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, line, UPS, LAW, A0 = (NE[k] for k in ("GALS", "fit_one", "pooled", "line", "UPS", "LAW", "A0"))
GE, MSUNE, MPCE = NE["G"], NE["MSUN"], NE["MPC"]
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "x40b_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
FEET, HK, BN, M, DC, I, TID, T3M, ALLI, N, X1m, wls1, bsum, prep, PREP, RG, RM, X7J, MY = (NX[k] for k in (
    "FEET", "HK", "BN", "M", "DC", "I", "TID", "T3M", "ALLI", "N", "X1m", "wls1", "bsum", "prep", "PREP", "RG", "RM", "X7J", "MY"))
O_, P_, A_, DS_, KG, RF, SB, DAT = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT"))
P(f"X40b_core_surface_density_scaling  {'MUTATE run (max -> min)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E (Newtonian, law emergent); cold dark energy (not matter) Burkert cores, Sigma = s * a0/(2 pi G); not theory closed")
P(f"EM1 and X30 machinery executed read-only [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
KPC = 3.0857e19

# ------------------------------------------------------------------ Burkert: X38's reference solver (verbatim) + fast compact-root inversion
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def solve_r0_x38(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk), True
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14)), False
def dlnB(x):  # d ln B / d ln x
    x = np.asarray(x, float); return x * (2 * x / (1 + x * x) + 2 / (1 + x) - 2 / (1 + x * x)) / B(x)
LXPK = brentq(lambda lx: float(dlnB(math.exp(lx))) - 2.0, math.log(0.1), math.log(100.0), xtol=1e-15)
LYMAX = float(np.log(B(math.exp(LXPK)))) - 2 * LXPK
LXT = np.linspace(LXPK, math.log(1e8), 6000); LYT = np.log(B(np.exp(LXT))) - 2 * LXT          # decreasing
def r0_fast(Mt, R, Sig):
    """Compact root of pi Sig r0^2 B(R/r0) = Mt (vectorised); saturated -> peak. Returns r0, sat."""
    Mt, R, Sig = np.broadcast_arrays(np.asarray(Mt, float), np.asarray(R, float), np.asarray(Sig, float))
    ly = np.log(Mt / (math.pi * Sig * R * R)); sat = ly > LYMAX
    lx = np.interp(-np.minimum(ly, LYMAX), -LYT, LXT)
    for _ in range(4):
        x = np.exp(lx); f = np.log(B(x)) - 2 * lx - ly; d = dlnB(x) - 2.0
        lx = np.where(sat, LXPK, np.maximum(lx - f / np.where(np.abs(d) > 1e-12, d, -1e-12), LXPK))
    return R / np.exp(lx), sat
SIG = {f: A0[f] / (2 * math.pi * GE) for f in FEET}
SIG_PC = {f: SIG[f] * KPC ** 2 / 1e6 / MSUNE for f in FEET}
B1 = float(B(1.0))

# ------------------------------------------------------------------ the rules: self-consistent s* (FROZEN section 2)
SGRID_UP = np.geomspace(1.0, 1e3, 400); SGRID_DN = np.geomspace(1.0, 1e-3, 400)
FLAGS = {"runaway": 0, "sat": 0}
def solve_s(gfun, Mt, R, Sig0, a0, own):
    """gfun(r) -> baryonic g (m/s^2). own: include the halo's own g at r0 (rule A'). Returns s*, r0."""
    def gtot(s, r0):
        g = gfun(r0)
        if own: g = g + GE * math.pi * Sig0 * s * r0 ** 2 * B(np.minimum(R, r0) / r0) / r0 ** 2
        return g / a0
    def h(s):
        r0, _ = r0_fast(Mt, R, Sig0 * s); y = gtot(s, r0)
        return (np.minimum(1.0, y) if MUTATE else np.maximum(1.0, y)) - s
    h1 = float(h(1.0))
    if (not MUTATE and h1 <= 0) or (MUTATE and h1 >= 0):
        s = 1.0
    else:
        grid = SGRID_DN if MUTATE else SGRID_UP; hv = h(grid)
        idx = np.where(hv >= 0)[0] if MUTATE else np.where(hv <= 0)[0]
        if len(idx) == 0:
            s = float(grid[-1]); FLAGS["runaway"] += 1
        else:
            k = int(idx[0]); s = math.exp(brentq(lambda ls: float(h(math.exp(ls))), math.log(grid[k - 1]), math.log(grid[k]), xtol=1e-14, rtol=1e-15))
    r0, sat = r0_fast(Mt, R, Sig0 * s); FLAGS["sat"] += int(sat)
    return s, float(r0)
def fp_resid(gfun, Mt, R, Sig0, a0, own, s):
    r0, _ = r0_fast(Mt, R, Sig0 * s); g = gfun(r0)
    if own: g = g + GE * math.pi * Sig0 * s * r0 ** 2 * B(np.minimum(R, r0) / r0) / r0 ** 2
    return abs(max(1.0, float(g) / a0) - s) / s

RES = dict(frozen="b09db13390", mutate=MUTATE, Sigma_a0_Msun_pc2=SIG_PC, checks={}, footings={}); checks = []
P(f"Sigma_a0 = a0/(2 pi G): canonical {SIG_PC['canonical']:.1f}, alt {SIG_PC['alt']:.1f} Msun/pc^2; Burkert x_pk {math.exp(LXPK):.5f}; B(1) {B1:.5f}")

# K1: fast inversion vs X38 solve_r0
rng = np.random.default_rng(40)
k1d = []; k1m = []; nsat = 0
for _ in range(200):
    R = 10 ** rng.uniform(np.log10(30 * KPC), np.log10(3e3 * KPC)); Sg = SIG["canonical"] * 10 ** rng.uniform(-0.5, 1.5)
    Mmax = math.pi * Sg * R * R * math.exp(LYMAX); Mt = Mmax * 10 ** rng.uniform(-4, 0.3)
    ra, sa = solve_r0_x38(Mt, R, Sg); rb, sb = r0_fast(Mt, R, Sg); rb = float(rb); nsat += int(sa)
    k1d.append(abs(rb / ra - 1))
    if not sb: k1m.append(abs(math.pi * Sg * rb ** 2 * float(B(R / rb)) / Mt - 1))
k1 = max(k1d) < 1e-8 and max(k1m) < 1e-8 and nsat > 0
P(f"K1 fast compact root vs X38 solve_r0: max |dr0/r0| {max(k1d):.1e} ({nsat} saturated cases), mass return {max(k1m):.1e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))

# K2a: floor on a test halo with g_b = 0
k2a = True
for own in (False, True):
    Mt, R = 1e11 * MSUNE, 97 * KPC
    s, r0 = solve_s(lambda r: np.zeros_like(np.asarray(r, float)), Mt, R, SIG["canonical"], A0["canonical"], own)
    rx, _ = solve_r0_x38(Mt, R, SIG["canonical"])
    ok = s == 1.0 and abs(r0 / rx - 1) < 1e-8; k2a &= ok
    P(f"K2a floor test (g_b = 0, rule {'A-prime' if own else 'A'}): s* = {s:.6g}, r0/r0_X38 - 1 = {r0 / rx - 1:+.1e}: {'ok' if ok else 'FAIL'}")
FLAGS["sat"] = 0; FLAGS["runaway"] = 0
SMIN = {"min": float("inf")}; FPR = {"max": 0.0}

# ------------------------------------------------------------------ SPARC
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
def sparc_gb(q, iu, R200):
    """X39's spherical baryon construction at Upsilon index iu -> g_b(r) function."""
    R = q["Rm"]; U = UPS[iu]
    rg = np.geomspace(R[0] * 0.05, R200, 300)
    Mbk = np.maximum.accumulate(np.maximum(q["GB"][:, iu] * R ** 2 / GE, 0.0))
    Mtot = max(float(Mbk[-1]), (U * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"]) * 1e9 * MSUNE)
    Mbg = np.where(rg < R[0], Mbk[0] * (rg / R[0]) ** 2, np.interp(np.log(rg), np.log(R), Mbk))
    out = rg > R[-1]
    if out.any():
        t = np.clip(np.log(rg[out] / R[-1]) / math.log(3.0), 0, 1); Mbg[out] = np.exp(np.log(max(Mbk[-1], 1e-300)) * (1 - t) + np.log(Mtot) * t)
    Mbg = np.maximum.accumulate(Mbg); lrg = np.log(rg); g0 = GE * Mbg[0] / rg[0] ** 2
    def gfun(r):
        r = np.asarray(r, float)
        return np.where(r < rg[0], g0, GE * np.interp(np.log(np.maximum(r, rg[0])), lrg, Mbg) / np.maximum(r, rg[0]) ** 2)
    return gfun
def sparc(f, bg, rule, alpha=None):
    a, b, hh = bg["a"], bg["b"], bg["h"]
    rc = 3 * (100 * hh * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); rows = []; sch = []; lm_ = []; r0ch = []
    for q in GALS:
        lM = a + b * (q["lMb"] - 10); M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); R = q["Rm"]
        gh = np.zeros((len(R), len(UPS))); sv = np.ones(len(UPS)); rv = np.zeros(len(UPS))
        if rule in ("A", "Ap"):
            for iu in range(len(UPS)):
                s, r0 = solve_s(sparc_gb(q, iu, R200), M200, R200, SIG[f], A0[f], rule == "Ap")
                sv[iu] = s; rv[iu] = r0; gh[:, iu] = GE * math.pi * SIG[f] * s * r0 ** 2 * B(R / r0) / R ** 2
                SMIN["min"] = min(SMIN["min"], s)
                if 1 < s < 1e3: FPR["max"] = max(FPR["max"], fp_resid(sparc_gb(q, iu, R200), M200, R200, SIG[f], A0[f], rule == "Ap", s))
        else:
            s = {"one": 1.0, "B": SB_GAL, "C": 1.0}[rule]
            r0, _ = r0_fast(M200, R200, SIG[f] * s); r0 = float(r0); sv[:] = s; rv[:] = r0
            gh[:] = (GE * math.pi * SIG[f] * s * r0 ** 2 * B(R / r0) / R ** 2)[:, None]
        w = fit_one(q, np.log10(np.maximum(q["GB"] + gh, 1e-300))); rows.append(w)
        sch.append(sv[int(w[2])]); lm_.append(lM); r0ch.append(rv[int(w[2])] / KPC)
    st = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
    return dict(st, line=line(st), s_median=float(np.median(sch)), s_max=float(np.max(sch)), frac_s_gt1=float(np.mean(np.array(sch) > 1 + 1e-12)),
                r0_median_kpc=float(np.median(r0ch))), np.array(sch), np.array(lm_)

# ------------------------------------------------------------------ CFG922 BCG (X39's matching, verbatim)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
P687 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
CEN = json.load(open(os.path.join(LANES, "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]
J9 = np.full(N, -1)
for i in range(N):
    dd = np.hypot((P687["ra"] - MY["ra"][i]) * np.cos(np.radians(MY["dec"][i])), P687["dec"] - MY["dec"][i]) * 3600; j = int(np.argmin(dd))
    if dd[j] < 5 and abs(P687["z"][j] - MY["z"][i]) < 1e-3: J9[i] = j
meas = np.array([j >= 0 and not CEN[j].get("not_measured", False) for j in J9])
bcg = np.array([float(CEN[j]["bcg_med"]) if j >= 0 else np.nan for j in J9])
BCG = np.where(meas & (bcg > 0), bcg, np.nan); nb = int(np.isfinite(BCG).sum()); FILL = BCG.copy()
for t in range(3):
    m = T3M == t; FILL[m & ~np.isfinite(BCG)] = float(np.nanmedian(BCG[m]))
P(f"CFG922 BCG matched {nb} (X39: 190); filled {int((~np.isfinite(BCG)).sum())} by MGAS500-tercile median")

# ------------------------------------------------------------------ clusters
def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)
LRM = np.log(RM)
DIAG = {}
def cluster_halo(i, foot, hk, rule, bcg=True, alpha=None):
    pp = prep(i, foot, hk); rta = pp["rta"]; Mt = pp["Mfair"]
    if rule in ("A", "Ap"):
        Mbg = pp["Mb"] + (FILL[i] * MSUNE * RM ** 2 / (RM + 10 * KPC) ** 2 if bcg else 0.0)
        gb = GE * Mbg / RM ** 2
        gfun = lambda r: np.exp(np.interp(np.log(np.asarray(r, float)), LRM, np.log(np.maximum(gb, 1e-300))))
        s, r0 = solve_s(gfun, Mt, rta, SIG[foot], A0[foot], rule == "Ap"); SMIN["min"] = min(SMIN["min"], s)
        if bcg and hk == "h0672":
            Mg_r0 = float(np.exp(np.interp(math.log(r0), LRM, np.log(np.maximum(pp["Mb"], 1e-300))))); Mbc_r0 = FILL[i] * MSUNE * r0 ** 2 / (r0 + 10 * KPC) ** 2
            DIAG[i] = (Mbc_r0 / (Mg_r0 + Mbc_r0), GE * (Mg_r0 + Mbc_r0) / r0 ** 2 / A0[foot])
        if 1 < s < 1e3: FPR["max"] = max(FPR["max"], fp_resid(gfun, Mt, rta, SIG[foot], A0[foot], rule == "Ap", s))
    else:
        s = {"one": 1.0, "B": SB_CL, "C": max(1.0, (Mt / MPIV) ** alpha) if alpha is not None else 1.0}[rule]
        r0 = float(r0_fast(Mt, rta, SIG[foot] * s)[0])
    return math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(RM, rta) / r0), s, r0, Mt
def grade_clusters(foot, rule, bcg=True, alpha=None):
    out = {}; meta = {}; S_all = np.zeros(N); M_all = np.zeros(N)
    for hk in HK:
        V = np.zeros((N, 8)); r0l = np.zeros(N); sl = np.zeros(N)
        for i in ALLI:
            Mh, s, r0, Mt = cluster_halo(int(i), foot, hk, rule, bcg, alpha); r0l[i] = r0 / 3.0857e22; sl[i] = s
            if hk == "h0672": S_all[i] = s; M_all[i] = Mt / MSUNE
            V[i] = dvecN(int(i), foot, hk, prep(int(i), foot, hk)["Mb"] + Mh)
        PREP.clear()
        cl = f"{foot}|{hk}"; o = M[cl]; vB = bsum(V); vC = bsum(DC[(foot, hk)]); kt, ktC = vB[I], vC[I]; g = {}
        for bi, b in enumerate(BN):
            At = [float(kt[TID == t, bi].sum() / ktC[TID == t, bi].sum()) for t in range(3)]; Aa = float(kt[:, bi].sum() / ktC[:, bi].sum())
            bp = float(wls1(kt[:, bi], ktC[:, bi], X1m)[1])
            if b == "MID":
                for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"], At[t])
                g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"], bp)
            if b == "OUTER":
                g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"], Aa)
                for t in range(3): g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"], At[t])
                g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"], bp)
            if b == "INNER":
                g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"], Aa)
        r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
        Am = [[float(vB[T3M == t, bi].sum() / vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
        Aall = [float(vB[:, bi].sum() / vC[:, bi].sum()) for bi in range(3)]
        g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
        for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
        g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
        out[hk] = {k: dict(meas=v[0], s=v[1], pred=v[2], Z=(v[0] - v[2]) / v[1]) for k, v in g.items()}
        meta[hk] = dict(r0_Mpc={f"T{t+1}": float(np.median(r0l[I][TID == t])) for t in range(3)}, s_KT={f"T{t+1}": float(np.median(sl[I][TID == t])) for t in range(3)},
                        s_median_all=float(np.median(sl[ALLI])), s_max=float(np.max(sl[ALLI])))
    keys = list(out["h0672"])
    ok = {k: all(abs(out[hk][k]["Z"]) <= 2 for hk in HK) for k in keys}
    bad = [k for k in keys if not ok[k]]
    sgn = {k: ("OVER" if out["h0672"][k]["pred"] > out["h0672"][k]["meas"] else "UNDER") for k in bad}
    return dict(cells=out, ok=ok, fails=[f"{k} ({sgn[k]})" for k in bad], meta=meta), S_all, M_all

# ------------------------------------------------------------------ groups (P4 T3's estimator, read-only)
P4SRC = open(os.path.join(REB, "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles.py")).read()
NSG = {"np": np, "math": math}
exec(P4SRC[P4SRC.index("G540, MSUN540, KPC540 = "):P4SRC.index('if want("T3")')], NSG)
G540, MS540, KP540, HERN_RE, XG, LXG, RHO_H, M_H = (NSG[k] for k in ("G540", "MSUN540", "KPC540", "HERN_RE", "XG", "LXG", "RHO_H", "M_H"))
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
GROUPS = []
for l in open(TIAN):
    if l.startswith("#"): continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group": continue
    GROUPS.append(dict(id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]), elM=float(r[8]), Re=float(r[10])))
def group_logsig_halo(o, foot, rule, dlM=0.0, fair=False, alpha=None, halo=True, ret_s=False):
    lMb = o["lM"] + dlM; Mb = 10 ** lMb * MS540; a = o["Re"] * KP540 / HERN_RE
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * G540)
    M200 = (5.364 * Mb) if fair else 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540
    R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
    gN = M_H / XG ** 2; s = 1.0
    if halo:
        if rule in ("A", "Ap"):
            gfun = lambda r: G540 * Mb * (np.asarray(r, float) / (np.asarray(r, float) + a)) ** 2 / np.asarray(r, float) ** 2
            s, r0 = solve_s(gfun, M200, R200, SIG[foot], A0[foot], rule == "Ap")
        else:
            s = {"one": 1.0, "B": SB_GRP, "C": max(1.0, (M200 / MSUNE / MPIV_MSUN) ** alpha) if alpha is not None else 1.0}[rule]
            r0 = float(r0_fast(M200, R200, SIG[foot] * s)[0])
        rr = XG * a
        Mh = math.pi * SIG[foot] * s * r0 ** 2 * B(np.minimum(rr, R200) / r0)
        gN = gN + Mh / Mb / XG ** 2
    s2 = float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * gN * XG, LXG) / 3.0) * G540 * Mb / a
    v = 0.5 * math.log10(s2) - 3.0
    return (v, s) if ret_s else v
def grade_groups(foot, rule, fair=False, alpha=None, halo=True):
    d, sl, ss = [], [], []
    for o in GROUPS:
        v, s = group_logsig_halo(o, foot, rule, fair=fair, alpha=alpha, halo=halo, ret_s=True)
        sp = (group_logsig_halo(o, foot, rule, 0.01, fair, alpha, halo) - group_logsig_halo(o, foot, rule, -0.01, fair, alpha, halo)) / 0.02
        d.append(o["ls"] - v); sl.append(sp); ss.append(s)
    st = NSG["class_stats"](d, sl); st["s_median"] = float(np.median(ss)); st["PASS"] = st["verdict"] == "CONSISTENT"
    return st
k4n = max(abs(group_logsig_halo(o, "canonical", "one", halo=False) - NSG["group_logsig"](o, A0["canonical"], lambda y: np.ones_like(np.asarray(y, float)))) for o in GROUPS)
k4 = len(GROUPS) == 63 and k4n < 1e-4
P(f"K4 groups: {len(GROUPS)} rows; no-halo integrator vs P4 group_logsig (nu = 1) max |d| {k4n:.1e} dex: {'PASS' if k4 else 'FAIL'}")
checks.append(("K4", k4))

# ------------------------------------------------------------------ rule B inputs: DESI M-DEC
J223 = json.load(open(os.path.join(LANES, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
ZC = np.array(J223["curves"]["z"], float); MDEC = np.array(J223["curves"]["M-DEC"], float)
mdec = lambda z: float(np.interp(z, ZC, MDEC))
SB_GAL, SB_GRP, SB_CL = mdec(1.5), mdec(1.0), mdec(0.5)
w3 = ZC <= 3.0 + 1e-12
B_bound = float(MDEC[w3].max() / MDEC[w3].min())
w1 = ZC <= 1.0 + 1e-12; dslope = np.gradient(MDEC[w1], ZC[w1])
zpk = float(ZC[w3][np.argmax(MDEC[w3])])
P(f"\n=== rule B inputs (M-DEC = a0(z)/a0(0), DESI CPL): z 0 / 0.5 / 1.0 / 1.5 / 2.0 / 3.0 -> "
  + " / ".join(f"{mdec(z):.4f}" for z in (0, 0.5, 1.0, 1.5, 2.0, 3.0)))
P(f"  s(SPARC z_f 1.5) {SB_GAL:.4f}, s(groups z_f 1.0) {SB_GRP:.4f}, s(clusters z_f 0.5) {SB_CL:.4f}; cluster/galaxy {SB_CL / SB_GAL:.4f}")
P(f"  epoch-free bound on [0, 3]: max/min = {B_bound:.4f} (peak at z {zpk:.2f}); d(a0/a0_0)/dz on [0, 1]: {dslope.min():+.3f} .. {dslope.max():+.3f}")
RES["ruleB_inputs"] = dict(s_gal=SB_GAL, s_grp=SB_GRP, s_cl=SB_CL, ratio_cl_gal=SB_CL / SB_GAL, bound_0_3=B_bound, z_peak=zpk,
                           slope_0_1=[float(dslope.min()), float(dslope.max())], curve={str(z): mdec(z) for z in (0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0)})
# rule C pivot
rcA = 3 * (100 * BGS["A_c2b_refit"]["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
MPIV_MSUN = max(10 ** (BGS["A_c2b_refit"]["a"] + BGS["A_c2b_refit"]["b"] * (q["lMb"] - 10)) for q in GALS); MPIV = MPIV_MSUN * MSUNE
P(f"  rule C pivot: largest SPARC M200 (bg A) = {MPIV_MSUN:.3e} Msun")

# ------------------------------------------------------------------ K0: s = 1 reproduces X38
k0 = True; k0d = 0.0
for f in FEET:
    for t, bg in BGS.items():
        st, _, _ = sparc(f, bg, "one"); x = X38J["footings"][f]["sparc"][t]
        k0d = max(k0d, abs(st["rms"] - x["rms"]), abs(st["U_median"] - x["U_median"]))
    gc, _, _ = grade_clusters(f, "one")
    for hk in HK:
        for k, v in gc["cells"][hk].items():
            k0d = max(k0d, abs(v["pred"] - X38J["footings"][f]["clusters"]["cells"][hk][k]["pred"]))
    RES["footings"].setdefault(f, {})["X38_groups"] = grade_groups(f, "one")
    RES["footings"][f]["X38_groups_fair"] = grade_groups(f, "one", fair=True)
k0 = k0d < 1e-6
P(f"K0 s = 1 reproduces X38's committed SPARC and 30 cluster preds per footing: max |d| {k0d:.1e}; Step 0 (scratch rerun of X38) identical: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0)); P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ grading per footing
def fmt_keys(gc, base=None):
    c0, c1 = gc["cells"]["h0672"], gc["cells"]["h0686"]
    for k in c0:
        bz = f" (X38 Z {base[k]['Z']:+.2f})" if base else ""
        P(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f}{bz} | h0.686 Z {c1[k]['Z']:+.2f}" + ("" if gc["ok"][k] else "  FAIL"))
RULES = [("A", "A (max(a0, g_b(r0)))"), ("Ap", "A-prime (max(a0, g_N,tot(r0)))"), ("B", "B (a0 at formation epoch)")]
PASSV = {}
for f in FEET:
    P(f"\n=== [{f}] Sigma_a0 {SIG_PC[f]:.1f} Msun/pc^2   X38 groups (s = 1): mean {RES['footings'][f]['X38_groups']['mean']:+.4f} Z {RES['footings'][f]['X38_groups']['Z']:+.2f} {RES['footings'][f]['X38_groups']['verdict']}")
    base = X38J["footings"][f]["clusters"]["cells"]["h0672"]; FR = RES["footings"][f]
    for rk, rname in RULES:
        P(f"  --- rule {rname}")
        FLAGS["runaway"] = 0; FLAGS["sat"] = 0
        sp_ = {}; SS = None
        for t, bg in BGS.items():
            st, sch, lms = sparc(f, bg, rk); sp_[t] = st
            if t == "A_c2b_refit": SS, LMS = sch, lms
            x = X38J["footings"][f]["sparc"][t]
            P(f"  SPARC [{t}]: rms {st['rms']:.4f}, median U {st['U_median']:.2f} -> line {'PASS' if st['line'] else 'FAIL'}  (X38 {x['rms']:.4f}@{x['U_median']:.2f}); "
              f"s* median {st['s_median']:.3f}, max {st['s_max']:.2f}, frac s*>1 {st['frac_s_gt1']:.2f}; median r0 {st['r0_median_kpc']:.2f} kpc")
        rs = dict(runaway=FLAGS["runaway"], sat=FLAGS["sat"]); FLAGS["runaway"] = 0; FLAGS["sat"] = 0
        gc, SC, MC = grade_clusters(f, rk)
        rc_ = dict(runaway=FLAGS["runaway"], sat=FLAGS["sat"])
        fmt_keys(gc, base)
        P(f"     cluster s* by KT tercile {gc['meta']['h0672']['s_KT']}, all-326 median {gc['meta']['h0672']['s_median_all']:.3f}, max {gc['meta']['h0672']['s_max']:.3f}; "
          f"r0 (Mpc) {gc['meta']['h0672']['r0_Mpc']}; RUNAWAY sparc/clusters {rs['runaway']}/{rc_['runaway']}; SATURATED {rs['sat']}/{rc_['sat']}")
        gr = grade_groups(f, rk); grf = grade_groups(f, rk, fair=True)
        P(f"     groups: mean {gr['mean']:+.4f} Z {gr['Z']:+.2f} tot {gr['tot']:.4f} {gr['verdict']} (s* median {gr['s_median']:.3f}); fair-share variant {grf['mean']:+.4f} Z {grf['Z']:+.2f} {grf['verdict']}")
        # effective scaling (SPARC bg A at chosen U + clusters all 326 h0672)
        x_ = np.concatenate([LMS, np.log10(MC[ALLI])]); y_ = np.concatenate([np.log10(SS), np.log10(SC[ALLI])])
        alpha_eff = float(np.polyfit(x_, y_, 1)[0]) if np.ptp(y_) > 0 else 0.0
        ratio = float(np.median(SC[I][TID == 2]) / np.median(SS))
        P(f"     effective scaling: alpha_eff (OLS log s* on log M, SPARC + 326 clusters) {alpha_eff:+.4f}; s*(KT T3 median) / s*(SPARC median) {ratio:.3f}")
        rep = {}
        if rk in ("A", "Ap") and DIAG:
            bsh = np.array([DIAG[int(i)][0] for i in I]); gba = np.array([DIAG[int(i)][1] for i in I])
            rep["gb_r0_diag"] = {f"T{t+1}": dict(BCG_share=float(np.median(bsh[TID == t])), gas_share=float(1 - np.median(bsh[TID == t])), gb_over_a0=float(np.median(gba[TID == t]))) for t in range(3)}
            P(f"     (diagnostic) g_b(r0) by KT tercile (median): " + "; ".join(f"T{t+1} g_b/a0 {rep['gb_r0_diag'][f'T{t+1}']['gb_over_a0']:.3f}, BCG share {rep['gb_r0_diag'][f'T{t+1}']['BCG_share']:.3f}, gas share {rep['gb_r0_diag'][f'T{t+1}']['gas_share']:.3f}" for t in range(3)))
        DIAG.clear()
        if rk in ("A", "Ap"):
            g2, _, _ = grade_clusters(f, rk, bcg=False)
            rep["no_BCG"] = dict(fails=g2["fails"], MID_T3=g2["cells"]["h0672"]["G-MID-T3"]["pred"], s_KT=g2["meta"]["h0672"]["s_KT"])
            P(f"     (reported) no BCG: fails {g2['fails'] or 'none'}; MID T3 pred {rep['no_BCG']['MID_T3']:.3f}; s* KT {rep['no_BCG']['s_KT']}")
        spass = all(v["line"] for v in sp_.values()); cpass = not gc["fails"]
        det = ([] if spass else ["SPARC line"]) + gc["fails"]
        PASSV[(f, rk)] = spass and cpass
        FR[rk] = dict(sparc=sp_, clusters=gc, groups=gr, groups_fair=grf, flags=dict(sparc=rs, clusters=rc_), alpha_eff=alpha_eff,
                      s_ratio_T3_over_sparc=ratio, reported=rep, closes=spass and cpass, failing=det)
        P(f"     RULE {rk} [{f}]: {'CLOSES (SPARC + every cluster key)' if spass and cpass else 'does not close'}" + (f"  (failing: {', '.join(det)})" if det else "")
          + f"; groups {'PASS' if gr['PASS'] else 'FAIL'}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    # (C) reported only
    P("  --- (C) reported only, NOT framework-native: s = (M/M_piv)^alpha above the largest SPARC M200; SPARC = X38 exactly")
    scan = {}
    for al in np.round(np.arange(0.0, 1.0001, 0.05), 2):
        g3, SC3, _ = grade_clusters(f, "C", alpha=float(al))
        chi = float(sum(v["Z"] ** 2 for v in g3["cells"]["h0672"].values()))
        scan[float(al)] = dict(chi2_h0672=chi, n_fail=len(g3["fails"]), fails=g3["fails"], MID_T3=g3["cells"]["h0672"]["G-MID-T3"]["Z"],
                               MIDb=g3["cells"]["h0672"]["G-MID-b"]["Z"], OUT_all=g3["cells"]["h0672"]["G-OUT-all"]["Z"], M3=g3["cells"]["h0672"]["G-OUT-M3"]["Z"],
                               s_T3=g3["meta"]["h0672"]["s_KT"]["T3"], s_T1=g3["meta"]["h0672"]["s_KT"]["T1"])
        P(f"     alpha {al:.2f}: chi2(15 keys, h0.672) {chi:7.2f}, fails {len(g3['fails'])}; Z MID-T3 {scan[float(al)]['MID_T3']:+.2f} MID-b {scan[float(al)]['MIDb']:+.2f} "
          f"OUT-all {scan[float(al)]['OUT_all']:+.2f} M3 {scan[float(al)]['M3']:+.2f}; s* KT T1/T3 {scan[float(al)]['s_T1']:.2f}/{scan[float(al)]['s_T3']:.2f}")
    abest = min(scan, key=lambda a: scan[a]["chi2_h0672"]); allpass = [a for a in scan if scan[a]["n_fail"] == 0]
    FR["C"] = dict(scan=scan, alpha_best=abest, alpha_all_pass=allpass, M_piv_Msun=MPIV_MSUN)
    P(f"     (C) alpha_best {abest:.2f} (chi2 {scan[abest]['chi2_h0672']:.2f}, fails {scan[abest]['fails'] or 'none'}; s* T3 {scan[abest]['s_T3']:.2f}); alpha with every key passing: {allpass or 'none'}")

# ------------------------------------------------------------------ verdict
def cls(f):
    for rk, lab in (("A", "RULE A CLOSES THE CLUSTER CORES (and keeps SPARC)"), ("Ap", "RULE A' CLOSES THE CLUSTER CORES (and keeps SPARC)"),
                    ("B", "RULE B CLOSES THE CLUSTER CORES (and keeps SPARC)")):
        if PASSV[(f, rk)]: return lab
    return "NO FRAMEWORK-NATIVE RULE CLOSES IT"
V = {f: cls(f) for f in FEET}
RES["verdict_per_footing"] = V
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"UNDECIDED (footings disagree: {V})"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
for f in FEET:
    P(f"  [{f}] groups line: " + ", ".join(f"{rk} {'PASS' if RES['footings'][f][rk]['groups']['PASS'] else 'FAIL'} (Z {RES['footings'][f][rk]['groups']['Z']:+.2f})" for rk, _ in RULES)
      + f"; X38 {RES['footings'][f]['X38_groups']['verdict']} (Z {RES['footings'][f]['X38_groups']['Z']:+.2f})")

k2b = SMIN["min"] >= 1.0
k2 = k2a and k2b
P(f"\nK2 floor: test halo ok {k2a}; min s* over graded A / A-prime halos {SMIN['min']:.4g} (>= 1): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))
k3 = FPR["max"] < 1e-8
P(f"K3 fixed point: max |max(1, g/a0) - s*| / s* over halos with s* > 1: {FPR['max']:.1e}: {'PASS' if k3 else 'FAIL'}"); checks.append(("K3", k3))
checks.append(("K5", rss() < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"x40b_sd_scaling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x40b_sd_scaling_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
