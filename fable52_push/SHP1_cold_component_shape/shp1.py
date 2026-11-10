#!/usr/bin/env python3
"""SHP1 the shape of the cold component, from raw data (criteria db5f7da07b). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread. Usage: python3 shp1.py [--mutate]

The cold component = all gravitating mass that is not baryons. In the law's variables
  x = sqrt(a0 / g_bar),  X = g_obs / g_bar - 1 = M_C(<r) / M_b(<r)
the counted-once law (form B) is X_L(x) = (sqrt(1 + 4 x^2) - 1) / 2 (SHP1.lean).
Data: SPARC rotation curves (FLD1's loader) and B21 KiDS-1000 isolated-lens ESD profiles (SNP1's conversion).
Constants, u_in and Rms come from ../SWT1_switch_theorems/swt1.py (its library part, as SNP1 imports it).
"""
import os, sys, json, math, time
import numpy as np
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SWT1 = os.path.join(HERE, "..", "SWT1_switch_theorems")
MUT = "--mutate" in sys.argv
TAG = "shp1_MUTATE" if MUT else "shp1"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

src = open(os.path.join(SWT1, "swt1.py")).read(); cut = src.index("RES = dict(lane=")
NS = {"__file__": os.path.abspath(os.path.join(SWT1, "swt1.py")), "__name__": "swt1_lib"}
_argv = sys.argv; sys.argv = ["swt1.py"]; exec(compile(src[:cut], "swt1.py", "exec"), NS); sys.argv = _argv
G, MS, PC, MPC, KPC, A0, R_DUST = (NS[k] for k in ("G", "MS", "PC", "MPC", "KPC", "A0", "R_DUST"))
u_in, Rms = NS["u_in"], NS["Rms"]
FOOT = ("canonical", "alt")
G_PC = 4.52e-30                                      # B21's G in pc^3 / (Msun s^2)
CONV = 4 * G_PC * PC                                 # ESD (Msun/pc^2) -> g_obs (m/s^2), as SNP1 loads it
BINS = (9.4, 10.45, 10.7, 10.9)
XS_RECORD = {"X=1 (5.56)": R_DUST, "PD1 (59.5)": 59.5}
ZN = (3.0, 6.0, 1.5)
LBX = np.arange(-1.25, 1.5001, 0.25)                 # log10 x bin edges (R1)

RES = dict(lane="SHP1", criteria="db5f7da07b", tag=TAG, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           partA={}, KA={}, rows={}, labels={}, reported={}, MUTATE={})

def g_law(gbar, a0): return a0 * u_in(np.asarray(gbar, float) / a0)
def X_L(x): x = np.asarray(x, float); return (np.sqrt(1 + 4 * x * x) - 1) / 2

# ====================================================================== data
def sparc(ud=0.5, ub=0.7):
    d = os.path.join(REPO, "real_research", "data")
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(d, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19: continue
        try: tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError: continue
    pts, nfile = [], 0
    for fn in sorted(os.listdir(os.path.join(d, "sparc_data"))):
        if not fn.endswith("_rotmod.dat"): continue
        nm = fn.replace("_rotmod.dat", "")
        a = np.genfromtxt(os.path.join(d, "sparc_data", fn), comments="#")
        if a.ndim != 2 or a.shape[1] < 6 or nm not in tab: continue
        nfile += 1; m = tab[nm]
        if m["Q"] >= 3 or m["Inc"] < 30: continue
        Mb = (ud * m["L36"] + 1.33 * m["MHI"]) * 1e9 * MS
        for R, Vo, eV, Vg, Vd, Vb in a[:, :6]:
            if Vo <= 0 or R <= 0 or eV / Vo > 0.1: continue
            r = R * KPC
            gb = (Vg * abs(Vg) + ud * Vd * abs(Vd) + ub * Vb * abs(Vb)) * 1e6 / r
            if gb <= 0: continue
            pts.append((nm, gb, Vo * Vo * 1e6 / r, Mb))
    nm = np.array([p[0] for p in pts]); gb = np.array([p[1] for p in pts]); go = np.array([p[2] for p in pts])
    Mb = np.array([p[3] for p in pts])
    return dict(name=nm, gbar=gb, gobs=go, Mb=Mb, nfile=nfile, ngal=len(set(nm)))

B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
def esd(fn):
    a = np.loadtxt(os.path.join(B21, fn), comments="#")
    return dict(gbar=a[:, 0], gobs=4 * G_PC * a[:, 1] / a[:, 4] * PC, esd=a[:, 1] / a[:, 4], bias=a[:, 4])   # SNP1's expression, same order
def cov(fn, blocks):
    """blocks: list of (bin_min key or -999, gbar array). Returns the converted covariance on g_obs (m^2/s^4)."""
    c = np.loadtxt(os.path.join(B21, fn), comments="#")
    idx = {}
    o = 0
    for key, gb in blocks:
        for i, g in enumerate(gb): idx[(key, i)] = o + i
        o += len(gb)
    C = np.zeros((o, o)); seen = np.zeros((o, o), bool)
    gmap = {key: gb for key, gb in blocks}
    def find(key, g):
        gb = gmap[key]; i = int(np.argmin(np.abs(np.log(gb / g)))); assert abs(math.log(gb[i] / g)) < 1e-3; return idx[(key, i)]
    keys = [k for k, _ in blocks]
    def kfix(v):
        best = min(keys, key=lambda k: abs(k - v)); assert abs(best - v) < 1e-3; return best
    for row in c:
        m, n, Ri, Rj, cv, _, bias = row[:7]
        I = find(kfix(m), Ri); J = find(kfix(n), Rj)
        C[I, J] = CONV ** 2 * cv / bias; seen[I, J] = True
    assert seen.all(), "covariance incomplete"
    return C

NOB = esd("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
NOB_C = cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", [(-999.0, NOB["gbar"])])
HOT = esd("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
HOT_C = cov("Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt", [(-999.0, HOT["gbar"])])
MB = [esd(f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt") for i in (1, 2, 3, 4)]
MB_KEYS = (8.5, 10.3, 10.6, 10.8)
MB_C = cov("Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt", [(k, d["gbar"]) for k, d in zip(MB_KEYS, MB)])

# ====================================================================== the separate halo (R4)
def esd_tsis(R, Mtot, Rh):
    """ESD (kg/m^2) of a truncated singular isothermal sphere of mass Mtot inside Rh, at projected radius R (SI)."""
    R = np.asarray(R, float); v2 = G * Mtot / Rh; out = np.empty_like(R)
    lo = R < Rh
    Rl = R[lo]; A = np.arctan(np.sqrt(Rh * Rh / (Rl * Rl) - 1))
    sbar = v2 / (math.pi * G * Rl * Rl) * (Rl * A + Rh - np.sqrt(Rh * Rh - Rl * Rl))
    sig = v2 / (2 * math.pi * G * Rl) * A
    out[lo] = sbar - sig
    out[~lo] = Mtot / (math.pi * R[~lo] ** 2)
    return out
def esd_tsis_numeric(R, Mtot, Rh):
    """direct quadrature, no closed form: Sigma(R) = 2 int_0^zmax rho dz; M_2D(<R) = int 4 pi r^2 rho f(r, R) dr with f the
    share of a shell of radius r inside the cylinder (1 for r <= R, 1 - sqrt(1 - R^2/r^2) beyond)."""
    from scipy.integrate import quad
    rho0 = Mtot / (4 * math.pi * Rh)
    def rho(r): return rho0 / (r * r) if r < Rh else 0.0
    zmax = math.sqrt(Rh * Rh - R * R) if R < Rh else 0.0
    Sig = 2 * quad(lambda z: rho(math.sqrt(R * R + z * z)), 0, zmax, epsabs=0, epsrel=1e-12, limit=400)[0] if zmax > 0 else 0.0
    m_in = quad(lambda r: 4 * math.pi * r * r * rho(r), 0, min(R, Rh), epsabs=0, epsrel=1e-12)[0]
    m_out = quad(lambda r: 4 * math.pi * r * r * rho(r) * (1 - math.sqrt(1 - R * R / (r * r))), R, Rh, epsabs=0, epsrel=1e-12, limit=400)[0] if R < Rh else 0.0
    return (m_in + m_out) / (math.pi * R * R) - Sig

def gls_fit(r, t, C):
    Ci = np.linalg.inv(C); F = float(t @ Ci @ t); b = float(t @ Ci @ r)
    xh = b / F; sig = 1 / math.sqrt(F)
    chi0 = float(r @ Ci @ r)
    def chi(X): d = r - X * t; return float(d @ Ci @ d)
    ul = xh + 2 * sig if xh >= 0 else xh + math.sqrt(4 * sig * sig + xh * xh)
    best = max(xh, 0.0)
    return dict(X_hat=xh, sigma=sig, X_best_clamped=best, UL_2sigma=ul, chi2_zero=chi0, chi2_best=chi(best), N=len(r), chi=chi)

def kids_R(gbar, lm): return np.sqrt(G * 10 ** lm * MS / np.asarray(gbar))

# ====================================================================== rows
def R1(S, a0, shift=None):
    x = np.sqrt(a0 / S["gbar"]); d = np.log10(S["gobs"] / g_law(S["gbar"], a0))
    if shift is not None: d = d + shift
    lx = np.log10(x); rows = []
    for lo, hi in zip(LBX[:-1], LBX[1:]):
        m = (lx >= lo) & (lx < hi); n = int(m.sum())
        if n == 0: continue
        Xo = S["gobs"][m] / S["gbar"][m] - 1
        rows.append(dict(lx_lo=float(lo), lx_hi=float(hi), n=n, median_delta=float(np.median(d[m])),
                         median_X_obs=float(np.median(Xo)), X_L_mid=float(X_L(10 ** ((lo + hi) / 2))),
                         graded=bool(n >= 20)))
    ok = all(abs(r["median_delta"]) <= 0.10 for r in rows if r["graded"])
    return dict(bins=rows, pass_=bool(ok), delta=d, lx=lx)

def R2(D, C, a0):
    r = D["gobs"] - g_law(D["gbar"], a0); Ci = np.linalg.inv(C); c2 = float(r @ Ci @ r); n = len(r)
    w = Ci @ np.ones(n); mean_q = float(((D["gobs"] / g_law(D["gbar"], a0) - 1) @ (np.diag(g_law(D["gbar"], a0)) @ w)) / w.sum()) if False else None
    q = D["gobs"] / g_law(D["gbar"], a0) - 1; Cq = C / np.outer(g_law(D["gbar"], a0), g_law(D["gbar"], a0))
    Cqi = np.linalg.inv(Cq); o = np.ones(n); mq = float(o @ Cqi @ q / (o @ Cqi @ o)); smq = float(1 / math.sqrt(o @ Cqi @ o))
    p = float(CHI2.sf(c2, n))
    return dict(chi2=c2, N=n, p=p, mean_ratio_minus_1=mq, sigma=smq, sign="ABOVE" if mq > 0 else "BELOW",
                pass_=bool(p >= 0.01), per_point=[dict(gbar=float(gb), x=float(math.sqrt(a0 / gb)), ratio=float(1 + qq),
                                                      err=float(math.sqrt(Cq[i, i]))) for i, (gb, qq) in enumerate(zip(D["gbar"], q))])

def R3a(S, a0, extra=None):
    d = np.log10(S["gobs"] / g_law(S["gbar"], a0)); lM = np.log10(S["Mb"] / MS)
    if extra is not None: d = d + extra(lM)
    lx = np.log10(np.sqrt(a0 / S["gbar"])); sl, ws, rows = [], [], []
    for lo, hi in zip(LBX[:-1], LBX[1:]):
        m = (lx >= lo) & (lx < hi)
        if m.sum() < 20 or np.ptp(lM[m]) < 0.5: continue
        s = float(np.polyfit(lM[m], d[m], 1)[0]); sl.append(s); ws.append(int(m.sum()))
        rows.append(dict(lx_lo=float(lo), n=int(m.sum()), slope=s, logMb_range=[float(lM[m].min()), float(lM[m].max())]))
    mean = float(np.average(sl, weights=ws))
    return dict(bins=rows, mean_slope=mean, pass_=bool(abs(mean) <= 0.05))

def R3b(a0, mb=None):
    mb = MB if mb is None else mb
    n = len(mb[0]["gbar"]); assert all(np.allclose(np.log(d["gbar"] / mb[0]["gbar"]), 0, atol=1e-3) for d in mb)
    gl = np.concatenate([g_law(d["gbar"], a0) for d in mb])
    q = np.concatenate([d["gobs"] for d in mb]) / gl - 1
    Cq = MB_C / np.outer(gl, gl); Ci = np.linalg.inv(Cq)
    A = np.zeros((4 * n, n))
    for k in range(4): A[k * n:(k + 1) * n, :] = np.eye(n)
    mu = np.linalg.solve(A.T @ Ci @ A, A.T @ Ci @ q); res = q - A @ mu
    c2 = float(res @ Ci @ res); dof = 3 * n; p = float(CHI2.sf(c2, dof))
    # bin-wise mean offsets about the common profile (reported)
    off = []
    for k in range(4):
        rk = res[k * n:(k + 1) * n]; Ck = Ci[k * n:(k + 1) * n, k * n:(k + 1) * n]; o = np.ones(n)
        off.append(float(o @ Ck @ rk / (o @ Ck @ o)))
    return dict(chi2=c2, dof=dof, p=p, pass_=bool(p >= 0.01), bin_offsets=off)

def R4(a0, zn, mb=None, inj=None):
    mb = MB if mb is None else mb
    r_all, t_all = [], []
    for lm, d in zip(BINS, mb):
        Mb = 10 ** lm * MS; Rh = Rms("NC", Mb, 0.0, 1 / (1 + zn))
        R = kids_R(d["gbar"], lm); t = 4 * G * esd_tsis(R, Mb, Rh)       # per unit X_s
        gobs = d["gobs"] if inj is None else g_law(d["gbar"], a0) + inj * t
        r_all.append(gobs - g_law(d["gbar"], a0)); t_all.append(t)
    r = np.concatenate(r_all); t = np.concatenate(t_all); f = gls_fit(r, t, MB_C)
    out = {k: v for k, v in f.items() if k != "chi"}
    out["dchi2_vs_best"] = {k: f["chi"](v) - f["chi2_best"] for k, v in XS_RECORD.items()}
    out["dchi2_vs_zero"] = {k: f["chi"](v) - f["chi2_zero"] for k, v in XS_RECORD.items()}
    out["Rh_kpc"] = {str(lm): Rms("NC", 10 ** lm * MS, 0.0, 1 / (1 + zn)) / KPC for lm in BINS}
    return out

def R4_nobins(D, C, a0, zn, lm=10.45):
    Mb = 10 ** lm * MS; Rh = Rms("NC", Mb, 0.0, 1 / (1 + zn))
    t = 4 * G * esd_tsis(kids_R(D["gbar"], lm), Mb, Rh); r = D["gobs"] - g_law(D["gbar"], a0)
    f = gls_fit(r, t, C); out = {k: v for k, v in f.items() if k != "chi"}
    out["dchi2_vs_zero"] = {k: f["chi"](v) - f["chi2_zero"] for k, v in XS_RECORD.items()}
    return out

# ====================================================================== Part A numbers + known answers
S = sparc()
P(f"SHP1 {TAG}: SPARC {S['nfile']} files, {S['ngal']} galaxies, {len(S['gbar'])} points after Lelli+2017's cuts")
xs = np.logspace(-3, 3, 601)
ka4 = float(np.max(np.abs(X_L(xs) - (u_in(1 / xs ** 2) * xs ** 2 - 1)) / (1 + X_L(xs))))
RES["KA"]["KA4"] = dict(max_rel_err=ka4, pass_=bool(ka4 < 1e-12))
P(f"KA4 closed form vs u_in: max rel err {ka4:.2e} -> {'PASS' if ka4 < 1e-12 else 'FAIL'}")
R_t, Mt, Rht = 120 * KPC, 1e11 * MS, 300 * KPC
ka5 = abs(esd_tsis(np.array([R_t]), Mt, Rht)[0] / esd_tsis_numeric(R_t, Mt, Rht) - 1)
R_t2 = 40 * KPC; ka5b = abs(esd_tsis(np.array([R_t2]), Mt, Rht)[0] / esd_tsis_numeric(R_t2, Mt, Rht) - 1)
RES["KA"]["KA5"] = dict(rel_err=[float(ka5), float(ka5b)], pass_=bool(max(ka5, ka5b) < 1e-4))
P(f"KA5 truncated-isothermal ESD vs numeric projection: {ka5:.1e}, {ka5b:.1e} -> {'PASS' if max(ka5, ka5b) < 1e-4 else 'FAIL'}")
ka3 = len(S["gbar"]); RES["KA"]["KA3"] = dict(points=ka3, files=S["nfile"], galaxies=S["ngal"],
                                             pass_=bool(S["nfile"] == 175 and abs(ka3 / 2693 - 1) <= 0.10))
P(f"KA3 SPARC: {S['nfile']} files, {ka3} points (Lelli+2017: 2693) -> {'PASS' if RES['KA']['KA3']['pass_'] else 'FAIL'}")
# KA2: SNP1's arrays and B21's README v_circ on Fig-3 bin 1
ka2a = all(np.array_equal(d["gobs"], 4 * 4.52e-30 * np.loadtxt(os.path.join(B21, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")[:, 1]
                          / np.loadtxt(os.path.join(B21, f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")[:, 4] * PC) for i, d in zip((1, 2, 3, 4), MB))
f3 = np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbin-1.txt"), comments="#")
vR = np.sqrt(4 * G_PC * f3[:, 1] / f3[:, 4] * f3[:, 0] * 1e6) * 3.086e13          # km/s, README eq.
g_readme = (vR * 1e3) ** 2 / (f3[:, 0] * MPC); g_ours = CONV * f3[:, 1] / f3[:, 4]
pos = f3[:, 1] > 0; ka2b = float(np.max(np.abs(g_readme[pos] / g_ours[pos] - 1)))
RES["KA"]["KA2"] = dict(snp1_identical=bool(ka2a), readme_max_rel=ka2b, pass_=bool(ka2a and ka2b < 2e-3))
P(f"KA2 conversion: SNP1 arrays identical {ka2a}; README v_circ vs ours max rel {ka2b:.1e} -> {'PASS' if RES['KA']['KA2']['pass_'] else 'FAIL'}")
# KA1 synthetic law data
ka1 = {}
for f in FOOT:
    a0 = A0[f]
    Ss = dict(S); Ss["gobs"] = g_law(S["gbar"], a0)
    r1 = R1(Ss, a0); r3 = R3a(Ss, a0)
    syn = [dict(d, gobs=g_law(d["gbar"], a0)) for d in MB]
    r3b = R3b(a0, syn); r4 = R4(a0, 3.0, mb=syn)
    nobs = dict(NOB, gobs=g_law(NOB["gbar"], a0)); r2 = R2(nobs, NOB_C, a0)
    mx = max(abs(b["median_delta"]) for b in r1["bins"])
    ok = mx < 1e-6 and abs(r3["mean_slope"]) < 1e-6 and r2["chi2"] < 1e-12 and r3b["chi2"] < 1e-12 and abs(r4["X_hat"]) < 1e-6
    ka1[f] = dict(max_median_delta=mx, slope=r3["mean_slope"], chi2_R2=r2["chi2"], chi2_R3b=r3b["chi2"], X_hat=r4["X_hat"], pass_=bool(ok))
    P(f"KA1 synthetic law data ({f}): max |median delta| {mx:.1e}, slope {r3['mean_slope']:.1e}, chi2 {r2['chi2']:.1e} / {r3b['chi2']:.1e}, "
      f"X_hat {r4['X_hat']:.1e} -> {'PASS' if ok else 'FAIL'}")
RES["KA"]["KA1"] = ka1
KA_OK = all(v["pass_"] for k, v in RES["KA"].items() if k != "KA1") and all(v["pass_"] for v in ka1.values())

# ====================================================================== graded rows
def run_rows(a0, f, a0_scale=1.0, sparc_extra=None):
    a = a0 * a0_scale
    r1 = R1(S, a); r2 = R2(NOB, NOB_C, a); r2h = R2(HOT, HOT_C, a); r3a = R3a(S, a, sparc_extra); r3b = R3b(a)
    r4 = {str(z): R4(a, z) for z in ZN}
    r4n = dict(published=R4_nobins(NOB, NOB_C, a, 3.0), hotgas=R4_nobins(HOT, HOT_C, a, 3.0))
    return dict(R1={k: v for k, v in r1.items() if k not in ("delta", "lx")}, R2=r2, R2_hotgas=r2h, R3a=r3a, R3b=r3b, R4=r4, R4_nobins=r4n)

def labels(rw):
    if not KA_OK: return "NO VERDICT", "NO VERDICT"
    if not rw["R1"]["pass_"]: shape = "NOT THE LAW'S SHAPE"
    elif rw["R2"]["pass_"]: shape = "THE LAW'S SHAPE"
    else: shape = f"THE LAW'S SHAPE ON ROTATION CURVES, LENSING {rw['R2']['sign']}"
    uni = "ONE SHAPE" if (rw["R3a"]["pass_"] and rw["R3b"]["pass_"]) else \
          "NOT ONE SHAPE (" + ", ".join(n for n, ok in (("R3a", rw["R3a"]["pass_"]), ("R3b", rw["R3b"]["pass_"])) if not ok) + ")"
    return shape, uni

if not MUT:
    for f in FOOT:
        a0 = A0[f]; rw = run_rows(a0, f); RES["rows"][f] = rw; RES["labels"][f] = labels(rw)
        P(f"\n=== {f} (a0 {a0:.4e}) ===")
        P("R1 SPARC, log10 x bin: n, median X_obs, X_L(mid), median delta (dex)")
        for b in rw["R1"]["bins"]:
            P(f"  [{b['lx_lo']:+.2f},{b['lx_hi']:+.2f}) n {b['n']:5d}  X_obs {b['median_X_obs']:9.3f}  X_L {b['X_L_mid']:9.3f}  "
              f"delta {b['median_delta']:+.3f}{'' if b['graded'] else '  (not graded, n<20)'}")
        P(f"  R1 {'PASS' if rw['R1']['pass_'] else 'FAIL'}")
        for nm, r in (("R2 B21 Nobins", rw["R2"]), ("R2 hot-gas bracket", rw["R2_hotgas"])):
            P(f"{nm}: chi2 {r['chi2']:.1f} / {r['N']}, p {r['p']:.3g}; mean g_obs/g_law - 1 = {r['mean_ratio_minus_1']:+.3f} +- {r['sigma']:.3f} "
              f"-> {'CONSISTENT' if r['pass_'] else r['sign']}")
            P("   x: " + "  ".join(f"{pp['x']:.0f}:{pp['ratio']:.2f}+-{pp['err']:.2f}" for pp in r["per_point"]))
        P(f"R3a SPARC slope of delta vs log M_b: mean {rw['R3a']['mean_slope']:+.4f} dex/dex over {len(rw['R3a']['bins'])} bins "
          f"-> {'PASS' if rw['R3a']['pass_'] else 'FAIL'}  (per bin: " + ", ".join(f"{b['slope']:+.3f}" for b in rw["R3a"]["bins"]) + ")")
        P(f"R3b KiDS four mass bins about one profile: chi2 {rw['R3b']['chi2']:.1f} / {rw['R3b']['dof']}, p {rw['R3b']['p']:.3g} "
          f"-> {'PASS' if rw['R3b']['pass_'] else 'FAIL'}; bin offsets " + ", ".join(f"{o:+.3f}" for o in rw["R3b"]["bin_offsets"]))
        for z, r in rw["R4"].items():
            P(f"R4 separate halo (share profile, z_n {z}; R_h " + "/".join(f"{v:.0f}" for v in r["Rh_kpc"].values()) + " kpc): "
              f"X_s hat {r['X_hat']:+.1f} +- {r['sigma']:.1f} M_b; 2-sigma UL {r['UL_2sigma']:.1f}; "
              + "; ".join(f"dchi2({k}) vs best {r['dchi2_vs_best'][k]:+.1f}, vs none {r['dchi2_vs_zero'][k]:+.1f}" for k in XS_RECORD))
        for k, r in rw["R4_nobins"].items():
            P(f"R4 Nobins at log M_b 10.45, z_n 3 ({k}): X_s hat {r['X_hat']:+.1f} +- {r['sigma']:.1f}; UL {r['UL_2sigma']:.1f}; "
              + "; ".join(f"dchi2({kk}) vs none {v:+.1f}" for kk, v in r["dchi2_vs_zero"].items()))
        P(f"LABEL ({f}): {RES['labels'][f][0]}; {RES['labels'][f][1]}")
    # brackets: Upsilon
    rep = {}
    for ud, ub in ((0.3, 0.5), (0.8, 1.0)):
        Sb = sparc(ud, ub); rr = {}
        for f in FOOT:
            r1 = R1(Sb, A0[f]); r3 = R3a(Sb, A0[f])
            rr[f] = dict(R1_pass=r1["pass_"], worst=max((abs(b["median_delta"]) for b in r1["bins"] if b["graded"])), slope=r3["mean_slope"])
        rep[f"U_d {ud}, U_b {ub}"] = rr
        P(f"bracket Upsilon_d {ud} / bulge {ub}: " + "; ".join(f"{f}: R1 {'PASS' if v['R1_pass'] else 'FAIL'} (worst {v['worst']:.3f} dex), R3a slope {v['slope']:+.4f}" for f, v in rr.items()))
    RES["reported"]["upsilon_brackets"] = rep
    # the shape's local slope from the SPARC medians and the KiDS points (reported)
    for f in FOOT:
        b = [bb for bb in RES["rows"][f]["R1"]["bins"] if bb["graded"] and bb["median_X_obs"] > 0]
        sl = [dict(lx=(b[i]["lx_lo"] + b[i + 1]["lx_hi"]) / 2, s=(math.log(b[i + 1]["median_X_obs"]) - math.log(b[i]["median_X_obs"])) / (0.25 * math.log(10)))
              for i in range(len(b) - 1)]
        RES["reported"].setdefault("slope", {})[f] = sl
        P(f"local slope s = dlnX/dlnx from SPARC medians ({f}): " + ", ".join(f"x~{10 ** s_['lx']:.2g}: {s_['s']:.2f}" for s_ in sl)
          + "   (law: 2 inside r_M, 1 outside; rho_C ~ r^(s-3))")
else:
    for f in FOOT:
        a0 = A0[f]
        m1 = R1(S, 2 * a0)
        syn = [dict(d, gobs=g_law(d["gbar"], a0) + 59.5 * 4 * G * esd_tsis(kids_R(d["gbar"], lm), 10 ** lm * MS, Rms("NC", 10 ** lm * MS, 0.0, 0.25)))
               for lm, d in zip(BINS, MB)]
        m2 = R4(a0, 3.0, mb=syn)
        m3 = R3a(S, a0, extra=lambda lM: 0.2 * (lM - 10))
        RES["MUTATE"][f] = dict(M1_R1_pass=m1["pass_"], M1_worst=max(abs(b["median_delta"]) for b in m1["bins"] if b["graded"]),
                                M2_X_hat=m2["X_hat"], M2_sigma=m2["sigma"], M2_flag=bool(m2["X_hat"] > 2 * m2["sigma"]),
                                M3_slope=m3["mean_slope"], M3_R3a_pass=m3["pass_"])
        bites = (not m1["pass_"]) and m2["X_hat"] > 2 * m2["sigma"] and not m3["pass_"]
        RES["MUTATE"][f]["all_bite"] = bool(bites)
        P(f"MUTATE ({f}): M1 a0 x 2 -> R1 {'PASS' if m1['pass_'] else 'FAIL'} (worst {RES['MUTATE'][f]['M1_worst']:.3f} dex); "
          f"M2 injected 59.5 -> X_hat {m2['X_hat']:.1f} +- {m2['sigma']:.1f} ({'flagged' if RES['MUTATE'][f]['M2_flag'] else 'NOT flagged'}); "
          f"M3 -> slope {m3['mean_slope']:+.3f}, R3a {'PASS' if m3['pass_'] else 'FAIL'}; all bite: {bites}")

P(f"\nknown answers all pass: {KA_OK}; wall time {time.time() - T0:.0f} s")
RES["KA_all_pass"] = bool(KA_OK); RES["end"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
