"""CFG806 -- the baryon census f_ret(M_ta) derived from the framework (energy vs the law's potential, cooling, accretion).
Criteria: FROZEN_CRITERIA.md (fb6a0f9d4), committed alone first.  Run: nice python3 cfg806.py   (CFG806_MUTATE=1: e_SN = 0).
kappa = 1/2 FITTED; no dark matter particle species; not theory closed.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "..")
MUT = os.environ.get("CFG806_MUTATE") == "1"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ---------------------------------------------------------------- constants (SI unless noted)
G, MSUN, KPC, C = 6.674e-11, 1.989e30, 3.0857e19, 2.998e8
MP, KB = 1.6726e-27, 1.380649e-23
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FB = 1 / (1 + 5.364)
RHOM0 = 2.77536627e11 * 0.31285 * 0.67403 ** 2 / 1e9            # M_sun / kpc^3 (as CFG656)
DTA = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
delta_ta = lambda z: float(np.interp(z, DTA["z"], DTA["D"]))
ESN0 = 1e49 * 1e-7 / MSUN                                          # 1e49 erg/M_sun -> J/kg = m^2 s^-2
MU, NE_NH, N_NH = 0.6, 1.17, 2.3                                   # CFG640 / cm12 values
CENSUS = {12: 0.100, 13: 0.325, 14: 0.700, 15: 0.900}

def fret_census(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)

def r_ta(Mta_sun, z):                                              # metres
    return (3 * Mta_sun / (4 * math.pi * delta_ta(z) * RHOM0 * (1 + z) ** 3)) ** (1 / 3) * KPC

def g_law(r, M, a0):
    gN = G * M / r ** 2
    return 0.5 * gN + math.sqrt(0.25 * gN * gN + gN * a0)

def dphi(M, a0, r1, r2):                                           # law potential difference, quadrature in ln r
    return quad(lambda lr: g_law(math.exp(lr), M, a0) * math.exp(lr), math.log(r1), math.log(r2), limit=200)[0]

def lam_cool(T):                                                   # Tozzi & Norman Z=0.3 fit as carried in CFG640 (cgs)
    kT = min(max(1.380649e-16 * T / 1.602177e-9, 0.01), 20.0)
    return (8.6e-3 * kT ** -1.7 + 5.8e-2 * kT ** 0.5 + 6.3e-2) * 1e-22

def chi_cool(Mgas, V, Rp):
    """CFG640 construction (cgs): isothermal gas T = mu m_p V^2/2k, rho ~ r^-2 to Rp, r_cool where t_cool = r/V."""
    Vc, Rc, Mc = V * 100.0, Rp * 100.0, Mgas * 1000.0
    T = MU * MP * V * V / (2 * KB)
    A = 3 * N_NH * 1.380649e-16 * T * MU * 1.6726e-24 * N_NH * 4 * math.pi * Rc / (2 * NE_NH * lam_cool(T) * Mc)
    return min(1.0, 1.0 / (A * Vc) / Rc), T

def system(f, Mta_sun, a0, z):
    Mb = f * FB * Mta_sun * MSUN
    rM = math.sqrt(G * Mb / a0); rt = r_ta(Mta_sun, z)
    V = (G * Mb * a0) ** 0.25
    return Mb, rM, rt, V, dphi(Mb, a0, rM, max(rt, rM * 1.0001))

def f_model(lM, foot="canonical", model="M2", eps=1.0, esn=1.0, z=0.0, hunits=False, agn=False):
    Mta = 10 ** lM / (0.67403 if hunits else 1.0)
    a0 = A0[foot]; e = 0.0 if MUT else eps * esn * ESN0
    if agn: e += 0.1 * 0.05 * C * C * 1e-3                         # E4 bracket, per unit M*
    def F(f):
        Mb, rM, rt, V, dp = system(f, Mta, a0, z)
        s = 1.0 if model == "M1" else chi_cool(Mb, V, rt)[0]
        return f * (1 + e * s / dp) - 1
    if F(1.0) <= 0: return 1.0
    return brentq(F, 1e-6, 1.0, xtol=1e-10)

def f_M3(lM, foot, T):
    Mta = 10 ** lM; Mb, rM, rt, V, dp = system(1.0, Mta, A0[foot], 0.0)
    return 1.0 if 2.5 * KB * T / (MU * MP) < dp else 0.0

def classify(fs):
    r = [fs[k] / CENSUS[k] for k in (12, 13, 14, 15)]
    if all(0.667 <= x <= 1.5 for x in r): return "CENSUS DERIVED"
    v = [fs[k] for k in (12, 13, 14, 15)]
    if all(b > a for a, b in zip(v, v[1:])) and v[3] / v[0] >= 3: return "SHAPE DERIVED"
    return "NOT DERIVED"
RANK = {"NOT DERIVED": 0, "SHAPE DERIVED": 1, "CENSUS DERIVED": 2}

P(f"CFG806  baryon census f_ret(M_ta) from the framework" + ("   [MUTATE e_SN = 0]" if MUT else ""))
# ---------------------------------------------------------------- controls
M = 10 ** 10.5 * MSUN; a0 = A0["canonical"]; rM = math.sqrt(G * M / a0); rt = r_ta(10 ** 12.3, 0.0)
q1 = dphi(M, a0, rM, rt)
xs = np.linspace(math.log(rM), math.log(rt), 200001); gs = np.array([g_law(math.exp(x), M, a0) * math.exp(x) for x in xs])
q2 = float(np.sum(0.5 * (gs[1:] + gs[:-1]) * np.diff(xs)))
V = (G * M * a0) ** 0.25
k1 = abs(q1 / q2 - 1) < 1e-4
P(f"  K1 dPhi(r_M -> r_ta) 1e10.5 Msun: quad {q1:.5e}, trapz {q2:.5e} (rel {q1 / q2 - 1:+.1e}); "
  f"V^2 ln(r_ta/r_M) = {V * V * math.log(rt / rM):.4e} (+ Newtonian-regime offset {q1 - V * V * math.log(rt / rM):.3e}): {'PASS' if k1 else 'FAIL'}")
k2 = abs(ESN0 / 5.03e11 - 1) < 1e-3
P(f"  K2 e_SN = {ESN0:.4e} m^2/s^2 ({math.sqrt(ESN0) / 1e3:.0f} km/s): {'PASS' if k2 else 'FAIL'}")
k3 = abs(delta_ta(0) - 11.8308) < 1e-3
P(f"  K3 Delta_ta(0) = {delta_ta(0):.4f}: {'PASS' if k3 else 'FAIL'}")

RES = dict(lane="CFG806", mutate=MUT, criteria="fb6a0f9d4", K=dict(K1=k1, K2=k2, K3=k3), census=CENSUS, runs={})
LM = (12, 13, 14, 15)
def run(label, **kw):
    fs = {k: f_model(k, **kw) for k in LM}
    cl = classify(fs); RES["runs"][label] = dict(f=fs, cls=cl, settings=kw)
    P(f"  {label:34s} " + "  ".join(f"{fs[k]:.3f} ({fs[k] / CENSUS[k]:.2f})" for k in LM) + f"   {cl}")
    return fs, cl

P("\n  f_ret (ratio to census) at log M_ta =        12              13              14              15")
P(f"  {'census (CFG416)':34s} " + "  ".join(f"{CENSUS[k]:.3f}       " for k in LM))
prim = {}
for foot in ("canonical", "alt"):
    prim[foot] = run(f"M2 PRIMARY eps=1 {foot}", foot=foot, model="M2")
    run(f"M1 (s=1) eps=1 {foot}", foot=foot, model="M1")
    run(f"M2 eps=0.1 {foot}", foot=foot, model="M2", eps=0.1)
P("  -- brackets (canonical M2 unless stated)")
run("e_SN 0.7e49", esn=0.7); run("e_SN 1.2e49", esn=1.2); run("z = 1", z=1.0); run("M_ta in Msun/h", hunits=True)
run("+ AGN (E4)", agn=True); run("M1 eps=0.1", model="M1", eps=0.1); run("eps=0.3", eps=0.3)

# diagnostics for the primary
P("\n  primary internals (canonical, M2, eps=1): log M_ta, f, log M_b, V km/s, r_M kpc, r_ta kpc, dPhi/V^2, chi, kT keV")
for k in (11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15):
    f = f_model(k); Mb, rM_, rt_, V_, dp = system(f, 10 ** k, A0["canonical"], 0.0)
    ch, T = chi_cool(Mb, V_, rt_)
    P(f"    {k:5.1f}  {f:.3f}  {math.log10(Mb / MSUN):6.2f}  {V_ / 1e3:6.0f}  {rM_ / KPC:6.1f}  {rt_ / KPC:6.0f}  {dp / V_ ** 2:5.2f}  {ch:.3f}  {KB * T / 1.602177e-16:.3f}")

# mechanism (iii)
P("\n  M3 accretion vs the catchment's law potential (step): f at 12/13/14/15")
for foot in ("canonical", "alt"):
    for T in (1e4, 1e6):
        fs = {k: f_M3(k, foot, T) for k in LM}; cl = classify(fs); RES["runs"][f"M3 T={T:.0e} {foot}"] = dict(f=fs, cls=cl)
        P(f"    {foot:9s} T {T:.0e} K: " + " ".join(f"{fs[k]:.0f}" for k in LM) + f"   {cl}")

# KiDS check at CFG804's primary-fit masses
P("\n  KiDS check (CFG804 primary log M_b per bin; N_min 3 canonical / 4 alt): log M_ta, f, N")
kids = {}
for foot, fn, nmin in (("canonical", "cfg804_results.json", 3), ("alt", "cfg804_results_alt.json", 4)):
    LB = json.load(open(os.path.join(LANES, "CFG804_catchment_supply_derived", fn)))["primary"]["logMb"]
    rows = []
    for lb in LB:
        f = 0.1
        for _ in range(200):
            lmt = lb - math.log10(f * FB); fn_ = f_model(lmt, foot=foot)
            if abs(fn_ - f) < 1e-9: break
            f = 0.5 * (f + fn_)
        rows.append((lb, lmt, f, 1 / f))
    ok = all(r[3] >= nmin for r in rows); kids[foot] = dict(rows=rows, pass_=ok)
    P(f"    {foot}: " + "; ".join(f"M_b {r[0]:.2f} -> M_ta {r[1]:.2f}, f {r[2]:.3f}, N {r[3]:.1f}" for r in rows) + f"  -> {'PASS' if ok else 'FAIL'}")
RES["kids"] = kids

# POST-FREEZE diagnostics (reported only, no verdict weight): root uniqueness of M2, and the KiDS check with M1
P("\n  POST-FREEZE diagnostic 1: sign changes of the M2 fixed-point function over f in [1e-4, 1] (canonical, eps 1)")
nroots = {}
for k in LM:
    Mta = 10 ** k; fg = np.logspace(-4, 0, 400); Fv = []
    for f in fg:
        Mb, rM_, rt_, V_, dp = system(f, Mta, A0["canonical"], 0.0)
        Fv.append(f * (1 + (0.0 if MUT else ESN0) * chi_cool(Mb, V_, rt_)[0] / dp) - 1)
    Fv = np.array(Fv); idx = np.where(np.sign(Fv[1:]) != np.sign(Fv[:-1]))[0]
    nroots[k] = [float(fg[i]) for i in idx]
    P(f"    log M_ta {k}: roots near f = " + ", ".join(f"{x:.4f}" for x in nroots[k]))
RES["post_freeze_roots_M2"] = nroots
P("  POST-FREEZE diagnostic 2: KiDS check with M1 (s = 1, eps = 1) instead of M2")
for foot, fn, nmin in (("canonical", "cfg804_results.json", 3), ("alt", "cfg804_results_alt.json", 4)):
    LB = json.load(open(os.path.join(LANES, "CFG804_catchment_supply_derived", fn)))["primary"]["logMb"]
    rows = []
    for lb in LB:
        f = 0.1
        for _ in range(300):
            lmt = lb - math.log10(f * FB); fn_ = f_model(lmt, foot=foot, model="M1")
            if abs(fn_ - f) < 1e-9: break
            f = 0.5 * (f + fn_)
        rows.append((lb, lmt, f, 1 / f))
    ok = all(r[3] >= nmin for r in rows); RES.setdefault("post_freeze_kids_M1", {})[foot] = dict(rows=rows, pass_=ok)
    P(f"    {foot}: " + "; ".join(f"M_b {r[0]:.2f} -> M_ta {r[1]:.2f}, f {r[2]:.3f}, N {r[3]:.1f}" for r in rows) + f"  -> {'PASS' if ok else 'FAIL'}")

c_prim = prim["canonical"][1]
c_eps01 = RES["runs"]["M2 eps=0.1 canonical"]["cls"]
qual = " (CEILING-CONDITIONAL)" if RANK[c_eps01] < RANK[c_prim] else ""
CLS = c_prim + qual
P(f"\n  CLASS (M2 primary, canonical, eps = 1): {CLS};  alt: {prim['alt'][1]};  eps = 0.1: {c_eps01}")
if MUT: P(f"  MUTATE: {'bites' if c_prim == 'NOT DERIVED' else 'DID NOT BITE'}")
RES["cls"] = CLS
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg806_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg806{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
