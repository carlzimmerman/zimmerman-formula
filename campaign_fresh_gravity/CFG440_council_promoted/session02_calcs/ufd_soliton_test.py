#!/usr/bin/env python3
"""Session 2: light-end soliton idea for the MW ultra-faints. Criteria: FROZEN_CRITERIA.md (written first).
Run: python3 ufd_soliton_test.py [--mutate]   -> ufd_soliton_test[_MUTATE].out / _results.json next to this file.
kappa = 1/2 fitted; both footings for the law row. No DM particle: the fluid is the record's cold wave field."""
import os, sys, csv, math, json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

Gpc = 4.3009e-3                      # pc (km/s)^2 / Msun
HBAR_C, C_KMS, PC_M = 1.97327e-7, 2.99792e5, 3.0857e16
def hbar_over_m(m_ev):               # pc km/s
    return HBAR_C / m_ev * C_KMS / PC_M
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
RHO_NORM = 1.9 * (10.0 if MUT else 1.0)   # Schive 2014, Msun/pc^3 at m=1e-23 eV, r_c=1 kpc

def fnum(v):
    try:
        x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None

# ---------------------------------------------------------------- data (AUDIT_UFD cut)
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))))
RES, UL = [], []
for r in rows:
    MV = fnum(r["M_V"]); sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if MV is None or MV <= -7.7 or rh is None or Dh is None:
        continue
    d = dict(name=r["name"], MV=MV, Ms=2 * 10 ** (0.4 * (4.83 - MV)), Re=rh, Dgc=fnum(r["distance_gc"]) or Dh)
    erh = 0.5 * ((fnum(r["rhalf_em"]) or 0) + (fnum(r["rhalf_ep"]) or 0)) / (fnum(r["rhalf"]) or 1)
    d["eRe_frac"] = erh if erh > 0 else 0.1
    if sig is not None and ul is None and sig > 0:
        d["sig"] = sig
        d["esig"] = 0.5 * ((fnum(r["vlos_sigma_em"]) or 0.2 * sig) + (fnum(r["vlos_sigma_ep"]) or 0.2 * sig))
        RES.append(d)
    elif ul is not None:
        d["sig_ul"] = ul; UL.append(d)

checks = {}
P("Session 2: light-end soliton idea vs MW ultra-faints" + (" [MUTATE: rho_c x10]" if MUT else ""))
P("=" * 100)
checks["K1_sample_31_9"] = (len(RES), len(UL)) == (31, 9)
P(f"K1 sample: {len(RES)} resolved + {len(UL)} upper limits -> {'PASS' if checks['K1_sample_31_9'] else 'FAIL'}")

# ---------------------------------------------------------------- profiles
def plummer_nu(r, a):                 # normalised 3-D light density, total 1
    return 3.0 / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def plummer_M(r, a, M):
    return M * r ** 3 / (r ** 2 + a ** 2) ** 1.5

def sol_rhoc(m_ev, rc_pc):
    return RHO_NORM * (m_ev / 1e-23) ** -2 * (rc_pc / 1e3) ** -4
_X = np.concatenate([np.linspace(0, 20, 4001)[1:], np.geomspace(20.005, 2000, 4000)])
_I = np.concatenate([[0.0], np.cumsum(np.diff(np.concatenate([[0.0], _X])) * 0.5 *
       (np.concatenate([[0.0], _X[:-1]]) ** 2 / (1 + 0.091 * np.concatenate([[0.0], _X[:-1]]) ** 2) ** 8 +
        _X ** 2 / (1 + 0.091 * _X ** 2) ** 8))])[1:]
_ITOT = _I[-1]
def sol_M(r, m_ev, rc):               # enclosed soliton mass
    x = r / rc
    return 4 * math.pi * sol_rhoc(m_ev, rc) * rc ** 3 * float(np.interp(x, _X, _I, left=0.0, right=_ITOT))
def sol_Mtot(m_ev, rc):
    return 4 * math.pi * sol_rhoc(m_ev, rc) * rc ** 3 * _ITOT
X_HALF = float(np.interp(0.5 * _ITOT, _I, _X))          # soliton r_1/2 / r_c

def sigma_los(Menc, a):
    """global sigma_los^2 = (1/3) <G M(<r)/r> over Plummer light of scale a (= projected half-light R_e)."""
    f = lambda r: plummer_nu(r, a) * 4 * math.pi * r ** 2 * Gpc * Menc(r) / max(r, 1e-9)
    v = quad(f, 0, 50 * a, limit=400)[0] + quad(f, 50 * a, 5000 * a, limit=200)[0]
    return math.sqrt(v / 3.0)

# K2: self-gravitating Plummer
a_t, M_t = 30.0, 1e6
s_num = sigma_los(lambda r: plummer_M(r, a_t, M_t), a_t)
s_an = math.sqrt(math.pi * Gpc * M_t / (32 * a_t))
checks["K2_plummer_virial"] = abs(s_num / s_an - 1) < 1e-3
P(f"K2 Plummer virial: numeric {s_num:.5f} vs analytic {s_an:.5f} km/s -> {'PASS' if checks['K2_plummer_virial'] else 'FAIL'}")
# K3: Schive mass relation
m22, rc_k = 1e-22, 1.0
k3 = sol_Mtot(m22, rc_k * 1e3) / 2.2e8
checks["K3_schive_mass"] = abs(k3 - 1) < 0.05
P(f"K3 soliton M_tot at m=1e-22, r_c=1 kpc: {sol_Mtot(m22, 1e3):.3e} Msun (Schive 2.2e8; ratio {k3:.3f}) -> {'PASS' if checks['K3_schive_mass'] else 'FAIL'}")
P(f"   soliton r_1/2 = {X_HALF:.3f} r_c")

# ---------------------------------------------------------------- G0: ambient MW fluid granule heating
P("\nG0  ambient MW-fluid granule heating over 10 Gyr (deep-MOND isothermal phantom of 6e10 Msun at current D_gc)")
G0 = {}
for foot, a0 in A0.items():
    Vf = (6.674e-11 * 6e10 * 1.989e30 * a0) ** 0.25 / 1e3
    worst = 0.0
    for m_ev in (2.0e-20, 4.4e-20):
        for d in RES + UL:
            r = d["Dgc"] * 1e3
            rho = Vf ** 2 / (4 * math.pi * Gpc * r ** 2)
            s = Vf / math.sqrt(2)
            meff = rho * (math.sqrt(math.pi) * hbar_over_m(m_ev) / s) ** 3
            rate = 4 * math.sqrt(2 * math.pi) * Gpc ** 2 * rho * meff * 3.0 / s   # (km/s)^3/pc
            dsig2 = 2 * rate * 1.0227 * 1e4                                        # x2 systematic; km/s/pc = 1.0227 /Myr
            worst = max(worst, dsig2)
    G0[foot] = dict(V_flat=Vf, worst_dsig2=worst)
    P(f"   {foot:9s} V_flat {Vf:.0f} km/s: worst delta sigma^2 = {worst:.2e} (km/s)^2 -> {'PASS' if worst < 1 else 'FAIL'}")

# ---------------------------------------------------------------- law residuals (deep MOND, for scatter comparison)
def sig_law(d, a0):
    return (4.0 / 81.0 * 6.674e-11 * d["Ms"] * 1.989e30 * a0) ** 0.25 / 1e3
for foot, a0 in A0.items():
    res = np.array([math.log10(d["sig"] / sig_law(d, a0)) for d in RES])
    P(f"\nlaw (deep-MOND 4/81) residual, {foot}: median {np.median(res):+.3f} dex, scatter {np.std(res, ddof=1):.3f} dex")

# ---------------------------------------------------------------- T1 regression
lS = np.log10([d["sig"] for d in RES]); lR = np.log10([d["Re"] for d in RES]); lM = np.log10([d["Ms"] for d in RES])
eS = np.array([d["esig"] / d["sig"] for d in RES]) / math.log(10); eR = np.array([d["eRe_frac"] for d in RES]) / math.log(10)
def fit(s, r, m):
    A = np.vstack([np.ones_like(r), r, m]).T
    return np.linalg.lstsq(A, s, rcond=None)[0]
b0 = fit(lS, lR, lM)
rng = np.random.default_rng(7); boots = []
n = len(RES)
for _ in range(2000):
    i = rng.integers(0, n, n)
    boots.append(fit(lS[i] + rng.normal(0, eS[i]), lR[i] + rng.normal(0, eR[i]), lM[i]))
boots = np.array(boots); cov = np.cov(boots[:, 1:].T); icov = np.linalg.inv(cov)
P(f"\nT1  log sigma = a + b log R_e + c log M*  (N {n}):  b = {b0[1]:+.3f} +- {boots[:,1].std():.3f},  c = {b0[2]:+.3f} +- {boots[:,2].std():.3f}  (corr {np.corrcoef(boots[:,1], boots[:,2])[0,1]:+.2f})")
P(f"    corr(log R_e, log M*) in sample = {np.corrcoef(lR, lM)[0,1]:+.2f}")
models = {"law deep-MOND": (0.0, 0.25), "soliton traced": (-1.0, 0.0), "harmonic core": (1.0, 0.0), "LCDM cusp (reported)": (0.5, 0.0)}
T1 = {"b": b0[1], "c": b0[2], "sb": boots[:, 1].std(), "sc": boots[:, 2].std(), "models": {}}
def mdist(p, q):
    v = np.array(p) - np.array(q); return float(math.sqrt(v @ icov @ v))
for k, v in models.items():
    dd = mdist((b0[1], b0[2]), v)
    verdict = "DISFAVOURED" if dd > 3.44 else "allowed"
    T1["models"][k] = dict(pred=v, dist=dd, verdict=verdict)
    P(f"    {k:22s} (b,c)={v}: Mahalanobis {dd:6.2f} -> {verdict}")
sep = mdist(models["law deep-MOND"], models["soliton traced"])
T1["law_vs_soliton_sep"] = sep
T1["non_discriminating"] = bool(sep < 3.44 or boots[:, 1].std() > 0.5)
P(f"    law vs soliton separation in fit metric: {sep:.2f} -> {'NON-DISCRIMINATING' if T1['non_discriminating'] else 'discriminating'}")

# ---------------------------------------------------------------- T2 implied m under trace
P("\nT2  implied field mass if the stars trace the soliton (soliton r_1/2 = 1.305 R_e)")
def sig_trace(d, m_ev, sig_scale=1.0):
    rc = 1.305 * d["Re"] / X_HALF
    return sigma_los(lambda r: sol_M(r, m_ev, rc) + plummer_M(r, d["Re"], d["Ms"]), d["Re"])
T2rows = []
for d in RES:
    out = []
    for s in (d["sig"], d["sig"] - d["esig"], d["sig"] + d["esig"]):
        s = max(s, 0.05)
        f = lambda lm: sig_trace(d, 10 ** lm) - s
        try:
            out.append(10 ** brentq(f, -23.0, -16.0, xtol=1e-4))
        except ValueError:
            out.append(float("nan"))
    m0, m_hi, m_lo = out[0], out[1], out[2]          # lower sigma -> heavier m
    T2rows.append(dict(name=d["name"], sig=d["sig"], Re=d["Re"], m=m0, m_lo=m_lo, m_hi=m_hi))
    P(f"    {d['name']:22s} sigma {d['sig']:5.2f} R_e {d['Re']:6.1f} pc  m = {m0:.2e} eV  [{m_lo:.2e}, {m_hi:.2e}]")
ms = np.array([t["m"] for t in T2rows]); good = np.isfinite(ms)
med = float(np.median(ms[good])); scat = float(np.std(np.log10(ms[good]), ddof=1))
overlap = sum(1 for t in T2rows if np.isfinite(t["m"]) and (np.nan_to_num(t["m_hi"], nan=1) >= 2.0e-20 and np.nan_to_num(t["m_lo"], nan=0) <= 4.4e-20))
inwin = sum(1 for m in ms[good] if 2.0e-20 <= m <= 4.4e-20)
if 2.0e-20 <= med <= 4.4e-20 and overlap >= 0.5 * good.sum():
    v2 = "PASS"
elif med < 1.0e-20 or med > 8.8e-20:
    v2 = "FAIL"
else:
    v2 = "MARGINAL"
P(f"    median implied m = {med:.2e} eV; scatter of log m = {scat:.3f} dex; central value in window {inwin}/{good.sum()}; 1-sigma overlap {overlap}/{good.sum()} -> T2 {v2}")
P(f"    16-84%: {np.percentile(ms[good],16):.2e} - {np.percentile(ms[good],84):.2e} eV")

# ---------------------------------------------------------------- T3 free soliton
P("\nT3  free soliton at fixed m (reported only): r_c, M_sol, r_c / lambda_dB, tidal density ratio at current D_gc")
T3 = {}
for m_ev in (2.0e-20, 4.4e-20):
    rowsT3 = []
    for d in RES:
        f = lambda lrc: sigma_los(lambda r: sol_M(r, m_ev, 10 ** lrc) + plummer_M(r, d["Re"], d["Ms"]), d["Re"]) - d["sig"]
        try:
            rc = 10 ** brentq(f, -1.0, 5.0, xtol=1e-4)
        except ValueError:
            rowsT3.append(None); continue
        Ms = sol_Mtot(m_ev, rc); lam = 2 * math.pi * hbar_over_m(m_ev) / d["sig"]
        rho_in = (sol_M(d["Re"], m_ev, rc) + plummer_M(d["Re"], d["Re"], d["Ms"])) / (4 / 3 * math.pi * d["Re"] ** 3)
        Vf = (6.674e-11 * 6e10 * 1.989e30 * A0["canonical"]) ** 0.25 / 1e3
        R = d["Dgc"] * 1e3; rho_mw = 3 * Vf ** 2 / (4 * math.pi * Gpc * R ** 2)   # mean enclosed density of isothermal
        rowsT3.append(dict(name=d["name"], rc=rc, Msol=Ms, rc_over_lam=rc / lam, tidal=rho_in / rho_mw))
    ok = [x for x in rowsT3 if x]
    T3[str(m_ev)] = ok
    P(f"  m = {m_ev:.1e} eV: solved {len(ok)}/{len(RES)}; median r_c {np.median([x['rc'] for x in ok]):.1f} pc, "
      f"median M_sol {np.median([x['Msol'] for x in ok]):.2e} Msun, median r_c/lambda {np.median([x['rc_over_lam'] for x in ok]):.2f}, "
      f"tidal ratio < 3 in {sum(x['tidal'] < 3 for x in ok)} objects")

# ---------------------------------------------------------------- verdict
allk = all(checks.values())
P("\nControls: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()))
P(f"SUMMARY  G0 {'PASS' if all(v['worst_dsig2'] < 1 for v in G0.values()) else 'FAIL'} | T1 " +
  "; ".join(f"{k}: {v['verdict']}" for k, v in T1["models"].items()) + f" | T2 {v2}")
json.dump(dict(mutate=MUT, checks=checks, G0=G0, T1=T1, T2=dict(rows=T2rows, median=med, scatter=scat, verdict=v2,
               in_window=inwin, overlap=overlap, n=int(good.sum())), T3=T3),
          open(os.path.join(HERE, f"ufd_soliton_test{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"ufd_soliton_test{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if allk else 1)
