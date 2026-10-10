#!/usr/bin/env python3
"""CFG545: does LCDM's emergent RAR scale track Lambda? s = d ln a0_emergent / d ln Lambda (FROZEN_CRITERIA.md, 58aa36f22).
CFG477's machinery is exec'd from source unedited; only its c_dm (concentration) is wrapped by c_lambda/c_1 from declared
formation-time models, with physical omega_m, omega_b and early amplitude fixed and only rho_Lambda varied.
Run: nice -n 10 python3 cfg545_lambda_scaling.py [--mutate]"""
import os, sys, json, math, io, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erfcinv
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

# ---------- CFG477 machinery, exec'd from source unedited (stop before its own runs) ----------
p477 = os.path.join(LANES, "CFG477_lcdm_dc14_rar", "cfg477_dc14.py")
src = open(p477).read()
ns = {"__file__": p477, "__name__": "c477"}
argv = sys.argv; sys.argv = [argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[:src.index("k1rows, _ = run(76")], ns)
sys.argv = argv
ns["MUT"] = False                         # CFG477's own mutate flag (X-3) is never used here
c_dm0, run477, halo_g0, gals, NU = ns["c_dm"], ns["run"], ns["halo_g"], ns["gals"], ns["C"].nu_mono
A0_477 = 9.686e-11                        # CFG477 committed median (README / results JSON)
a477 = float(np.median(json.load(open(os.path.join(LANES, "CFG477_lcdm_dc14_rar", "cfg477_dc14_results.json")))["a0"]))

# ---------- cosmology with varied rho_Lambda (physical units: Msun, Mpc) ----------
RHO100 = 2.775e11                         # Msun/Mpc^3 for h = 1
OM_H2, OB_H2, NS, S8, H1, OL1 = 0.1431, 0.02237, 0.965, 0.811, 0.674, 0.685
RHO_M0 = OM_H2 * RHO100; RHO_L0 = OL1 * H1 ** 2 * RHO100
RHO_REF = 0.7 ** 2 * RHO100               # CFG476 aperture convention (h = 0.7), fixed with lambda
DC = 1.686

def Hsq(a, lam): return RHO_M0 * a ** -3 + lam * RHO_L0          # proportional to H^2 (units of rho)
def Dgrow(a, lam):
    I = quad(lambda x: 1.0 / (x * math.sqrt(Hsq(x, lam))) ** 3, 0, a, limit=200)[0]
    return 2.5 * RHO_M0 * math.sqrt(Hsq(a, lam)) * I                 # -> a in matter era
def age(a, lam):                                                     # in units of 1/sqrt(8 pi G/3 * rho) consistently
    if lam == 0: return (2 / 3) * a ** 1.5 / math.sqrt(RHO_M0)
    HL = math.sqrt(lam * RHO_L0)
    return (2 / (3 * HL)) * math.asinh(math.sqrt(lam * RHO_L0 / (RHO_M0 * a ** -3)))

# EH98 no-wiggle transfer, physical k [1/Mpc]
TH = 2.7255 / 2.7; FB = OB_H2 / OM_H2
SOUND = 44.5 * math.log(9.83 / OM_H2) / math.sqrt(1 + 10 * OB_H2 ** 0.75)
ALG = 1 - 0.328 * math.log(431 * OM_H2) * FB + 0.38 * math.log(22.3 * OM_H2) * FB ** 2
def Tk(k):
    g = OM_H2 * (ALG + (1 - ALG) / (1 + (0.43 * k * SOUND) ** 4)); q = k * TH ** 2 / g
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)
KK = np.logspace(-4, 3, 4000)
PK = KK ** NS * Tk(KK) ** 2
def sig_raw(R):
    x = KK * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapz(KK ** 2 * PK * W ** 2, KK) / (2 * math.pi ** 2))
D11 = Dgrow(1.0, 1.0)
NORM = S8 / sig_raw(8 / H1) / D11                 # sigma(M, a; lam) = NORM * sig_raw * D_lam(a)
def sigM(M): return NORM * sig_raw((3 * M / (4 * math.pi * RHO_M0)) ** (1 / 3))

# D(a) inversion table per lambda
AG = np.logspace(-3, math.log10(3.0), 400)
_DT = {}
def Dtab(lam):
    if lam not in _DT: _DT[lam] = np.array([Dgrow(a, lam) for a in AG])
    return _DT[lam]
def a_of_D(D, lam):
    t = Dtab(lam)
    if D <= t[0]: return D                          # matter era, D = a
    return float(10 ** np.interp(math.log10(D), np.log10(t), np.log10(AG)))
_AOBS = {}
def a_obs(lam, conv):
    if conv == "P" or lam == 1: return 1.0
    if (lam, conv) not in _AOBS:
        t0 = age(1.0, 1.0); _AOBS[(lam, conv)] = math.exp(brentq(lambda la: age(math.exp(la), lam) - t0, math.log(0.05), math.log(1e8)))
    return _AOBS[(lam, conv)]

mfun = lambda x: math.log(1 + x) - x / (1 + x)
def c_ludlow(M, lam, conv, form):
    ao = a_obs(lam, conv); Do = Dgrow(ao, lam)
    dsig = math.sqrt(2 * (sigM(0.02 * M) ** 2 - sigM(M) ** 2))
    def F(c):
        frac = mfun(1) / mfun(c); x = float(erfcinv(frac))
        Dm2 = DC / (DC / Do + x * dsig)          # EPS barrier: dc/D(a_-2) - dc/D(a_obs) = x * sqrt(2[s^2(fM) - s^2(M)]), s at D = 1
        am2 = a_of_D(Dm2, lam)
        rhoX = Hsq(am2, lam) if form == "crit" else RHO_M0 * am2 ** -3 / (RHO_M0 / Hsq(1.0, 1.0))
        return 200 * RHO_REF * c ** 3 * mfun(1) / mfun(c) - 650 * rhoX
    for lo, hi in ((1.05, 200.0), (1.0001, 2000.0)):
        if F(lo) * F(hi) < 0: return brentq(F, lo, hi)
    return float("nan")                              # no solution (disclosed; that lambda is skipped for this variant)

def a_coll_L16(M):                                  # collapse epoch a_{-2} of L16-crit at lambda = 1 (for D04)
    c = c_ludlow(M, 1.0, "P", "crit"); frac = mfun(1) / mfun(c); x = float(erfcinv(frac))
    dsig = math.sqrt(2 * (sigM(0.02 * M) ** 2 - sigM(M) ** 2)); Do = Dgrow(1.0, 1.0)
    return a_of_D(DC / (DC / Do + x * dsig), 1.0)

LMG = np.linspace(9.0, 14.0, 21)
def ratio_table(model, conv, lam):
    if lam == 1.0: return np.ones_like(LMG)
    out = []
    for lm in LMG:
        M = 10 ** lm
        if model == "D04":
            ac = a_coll_L16(M); r = Dgrow(ac, lam) / Dgrow(ac, 1.0)
        else:
            form = "crit" if model == "L16-crit" else "m"
            r = c_ludlow(M, lam, conv, form) / c_ludlow(M, 1.0, "P", form)
        out.append(r)
    return np.array(out)

def a0_emergent(rtab, lam):
    ns["c_dm"] = lambda Mh: c_dm0(Mh) * float(np.interp(math.log10(Mh), LMG, rtab))
    if MUT:                                          # inject the owner's law: halo term = nu(gb/a0) gb - gb
        a0l = 9.3603e-11 * math.sqrt(lam); gbmap = {id(g["R"]): g["gb"] for g in gals}
        ns["halo_g"] = lambda Mh, r_m, c, abg: (NU(gbmap[id(r_m)] / a0l) - 1) * gbmap[id(r_m)]
    else:
        ns["halo_g"] = halo_g0
    rows, _ = run477(77, "dc14")
    return float(np.median(rows[:, 1])), float(np.percentile(rows[:, 1], 16)), float(np.percentile(rows[:, 1], 84))

# ---------- controls ----------
k2 = abs(Dgrow(0.5, 0.0) - 0.5) < 1e-4 and abs(Dgrow(1.0, 0.0) - 1.0) < 1e-4
cL = c_ludlow(1e12, 1.0, "P", "crit"); cD = c_dm0(1e12); k4 = 1 / 1.5 <= cL / cD <= 1.5
P(f"CFG545 {'MUTATE (owner law a0 = 9.36e-11 sqrt(lambda) injected)' if MUT else 'main'}; CFG477 exec'd unedited, seed 77, 200 realisations per lambda")
P(f"K2 D(a) EdS = a: {'PASS' if k2 else 'FAIL'};  K4 L16-crit c(1e12) {cL:.2f} vs Dutton-Maccio {cD:.2f} (ratio {cL/cD:.2f}) -> {'PASS' if k4 else 'FAIL'}")
P(f"sigma8 check at lambda=1: {NORM*sig_raw(8/H1)*D11:.3f};  D_lam(1)/D_1(1): " + ", ".join(f"{l}:{Dgrow(1.0,l)/D11:.3f}" for l in (0, 0.1, 1, 10, 100)))

LAMS = [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 10.0, 30.0, 100.0]
VARS = [("L16-crit", "P"), ("L16-m", "P"), ("D04", "P"), ("L16-crit", "T"), ("L16-m", "T"), ("D04", "T")]
if MUT: VARS = [("L16-crit", "P")]
res = {}; k3 = True
for model, conv in VARS:
    key = f"{model}/{conv}"; res[key] = {}
    for lam in LAMS:
        rt = ratio_table(model, conv, lam)
        if lam == 1.0: k3 &= bool(np.all(rt == 1.0))
        if not np.all(np.isfinite(rt)):
            res[key][str(lam)] = dict(a0=None, note="no L16 solution for some masses", n_nan=int(np.sum(~np.isfinite(rt))), a_obs=a_obs(lam, conv)); continue
        a0m, a16, a84 = a0_emergent(rt, lam)
        res[key][str(lam)] = dict(a0=a0m, p16=a16, p84=a84, c_ratio_1e11=float(np.interp(11, LMG, rt)), c_ratio_1e12=float(np.interp(12, LMG, rt)),
                                  a_obs=a_obs(lam, conv))
    r = res[key]; s = math.log(r["2.0"]["a0"] / r["0.5"]["a0"]) / math.log(4); sspan = math.log(r["10.0"]["a0"] / r["0.1"]["a0"]) / math.log(100)
    r["s"] = s; r["s_span_0p1_10"] = sspan
    P(f"\n{key}: s = d ln a0/d ln Lambda at Lambda0 = {s:+.4f};  span slope [0.1,10] = {sspan:+.4f}")
    for lam in LAMS:
        e = r[str(lam)]
        if e.get("a0") is None: P(f"   lambda {lam:6.1f}  a_obs {e['a_obs']:.3f}  NO SOLUTION ({e['n_nan']} of {len(LMG)} masses) -> skipped"); continue
        P(f"   lambda {lam:6.1f}  a_obs {e['a_obs']:.3f}  c ratio (1e11/1e12) {e['c_ratio_1e11']:.3f}/{e['c_ratio_1e12']:.3f}  a0 {e['a0']:.4e} (16-84% {e['p16']:.3e}-{e['p84']:.3e})")

k1 = abs(res[f"{VARS[0][0]}/{VARS[0][1]}"]["1.0"]["a0"] / a477 - 1) < 0.01
P(f"\nK1 lambda=1 a0 {res[f'{VARS[0][0]}/{VARS[0][1]}']['1.0']['a0']:.4e} vs CFG477 JSON median {a477:.4e} (README {A0_477:.3e}): {'PASS' if k1 else 'FAIL'};  K3 ratio = 1 at lambda = 1: {'PASS' if k3 else 'FAIL'}")

if MUT:
    s = res["L16-crit/P"]["s"]; ok = 0.45 <= s <= 0.55
    P(f"MUTATE: injected s = 0.5, recovered s = {s:.4f} -> {'bite detected (exit 1)' if ok else 'NOT recovered'}")
    json.dump(dict(K1=bool(k1), K2=bool(k2), K3=bool(k3), res=res, recovered_s=s, ok=bool(ok)), open(os.path.join(HERE, f"cfg545_lambda_scaling{TAG}_results.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg545_lambda_scaling{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 0)

# K-null: lambda held at 1 on the grid -> identical a0 at "0.5" and "2" -> s = 0
an1, _, _ = a0_emergent(np.ones_like(LMG), 1.0); an2, _, _ = a0_emergent(np.ones_like(LMG), 1.0)
snull = math.log(an2 / an1) / math.log(4); knull = abs(snull) < 1e-6
P(f"K-null (lambda fixed): s = {snull:.2e} -> {'PASS' if knull else 'FAIL'}")

# analytic proxy g_-2 = G M_-2 / r_-2^2 (L16-crit, P), at M = 1e11, 1e12
G_SI, MSUN, MPC = 6.674e-11, 1.989e30, 3.0857e22
prox = {}
for lm in (11.0, 12.0):
    M = 10 ** lm; gl = {}
    for lam in (0.5, 1.0, 2.0, 0.1, 10.0):
        c = c_ludlow(M, lam, "P", "crit"); R200 = (3 * M / (4 * math.pi * 200 * RHO_REF)) ** (1 / 3); rm2 = R200 / c
        gl[lam] = G_SI * M * mfun(1) / mfun(c) * MSUN / (rm2 * MPC) ** 2
    sp = math.log(gl[2.0] / gl[0.5]) / math.log(4)
    prox[str(lm)] = dict(g_m2_lam1=gl[1.0], s_proxy=sp, s_proxy_span=math.log(gl[10.0] / gl[0.1]) / math.log(100))
    P(f"proxy g_-2 at log M {lm:.0f}: {gl[1.0]:.3e} m/s^2 at lambda=1; s_proxy = {sp:+.4f} (span [0.1,10] {prox[str(lm)]['s_proxy_span']:+.4f})")

svals = {k: res[k]["s"] for k in res}; smax = max(abs(v) for v in svals.values()); sprim = svals["L16-crit/P"]
cls = "COINCIDENCE-LIKE" if smax <= 0.15 else ("TRACKS-LAMBDA" if sprim >= 0.35 else "NOT DIAGNOSTIC")
published_varied_lambda_rar = False               # census (README): no varied-Lambda run measured an acceleration scale
overall = "TEST AVAILABLE" if published_varied_lambda_rar else "TEST NEEDS NEW SIMULATIONS"
# precision: two runs lambda = 1, 10; separate s = 0.5 from s_LCDM at 3 sigma -> per-run ln a0 error
dS = abs(0.5 - sprim); prec = dS * math.log(10) / (3 * math.sqrt(2))
P(f"\ns by variant: " + ", ".join(f"{k} {v:+.4f}" for k, v in svals.items()))
P(f"max |s| = {smax:.4f}; primary s = {sprim:+.4f}; owner's picture s = 0.5 -> LCDM estimate {cls}")
P(f"precision needed (two runs, lambda 1 and 10, 3 sigma): per-run ln a0 error < {prec:.3f} ({prec/math.log(10):.3f} dex)")

# time domain, from committed CFG565 JSON
d565 = json.load(open(os.path.join(LANES, "CFG565_feedback_gdagger_vs_z", "cfg565_gdagger_z_results.json")))["res"]
P("time domain (CFG565 committed JSON, feedback-LCDM g+(z)/g+(0), median 16-84%): " + "; ".join(f"z {z}: {v['median']:.2f} ({v['p16']:.2f}-{v['p84']:.2f})" for z, v in d565.items()))
P("   owner's picture: flat for w = -1 (sqrt(rho_DE(z))); Mayer+23 Magneticum: ~x3 by z = 2 (abstract)")
P(f"OVERALL: {overall} (LCDM analytic estimate: {cls})")
json.dump(dict(K1=bool(k1), K2=bool(k2), K3=bool(k3), K4=bool(k4), Knull=bool(knull), c_L16_1e12=cL, c_DM_1e12=cD, res=res, s=svals, s_max=smax, s_primary=sprim,
               proxy=prox, classification=cls, overall=overall, precision_ln=prec, cfg565=d565, published_varied_lambda_rar=published_varied_lambda_rar),
          open(os.path.join(HERE, f"cfg545_lambda_scaling{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg545_lambda_scaling{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (k1 and k2 and k3 and k4 and knull) else 1)
