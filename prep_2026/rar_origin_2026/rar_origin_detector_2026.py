#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
rar_origin_detector_2026.py -- detecting the cold component where it matters: is the RAR made of halos or of a_0?  SPARC, data in hand.
========================================================================================================================================
The cold component is detected three times (CMB, Bullet, forest).  The one place its gravity is NOT yet seen is inside galaxies, where
the radial acceleration relation is what it would have to be made of.  Two readings of the same 175 rotation curves:
  FRAMEWORK  g_obs = g_bar nu(g_bar/a_0), one universal a_0 = (c/2) sqrt(G rho_DE) for every galaxy (Route A kernel nu = 1/(1-e^-sqrt y)).
             Prediction: the per-galaxy fitted a_0 scatters only by the error budget, with NO trend with galaxy mass.
  LCDM       g_obs = g_bar + g_NFW, halo from abundance matching (Moster+ 2013) with its 0.15 dex scatter, concentration from
             Dutton-Maccio 2014 with its 0.11 dex scatter.  Prediction: the per-galaxy "a_0" scatters by the halo-population scatter
             and trends with mass.  (No adiabatic contraction, no feedback: the plain halo population; noted.)
The detector: fit the SAME per-galaxy a_0 to (i) the data, (ii) framework mocks with the full observational error budget (V errors,
distance, inclination, M/L), (iii) LCDM mocks with the same error budget.  Compare the spread and the mass slope.  Both a_0 footings.
Selection as Lelli+ 2016/2017: Q <= 2, i >= 30 deg, >= 6 points.  Upsilon_disk = 0.5, Upsilon_bulge = 0.7 (3.6 micron).
Checks CAN fail.  Prior art: McGaugh, Li, Lelli & Schombert 2018 (per-galaxy a_0 consistent with universal); Desmond 2017 (LCDM
predicts more RAR scatter than observed); Rodrigues+ 2018 vs Kroupa+ 2018 (the systematics dispute) -- this is a re-run of that
question with the framework's own kernel and a halo-population mock on the same footing.
"""
import sys, math, glob, os
import numpy as np
from scipy.optimize import minimize_scalar, brentq
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "..", "real_research", "data")
G = 6.674e-11; kpc = 3.0857e19; Msun = 1.989e30; KMS2_KPC = 1e6/kpc                 # (km/s)^2/kpc -> m/s^2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; UPS_D, UPS_B = 0.5, 0.7
h = 0.674; rho_crit = 3*(100*h*1e3/3.0857e22)**2/(8*math.pi*G)*(kpc**3)/Msun    # Msun/kpc^3
# ---------------------------------------------------------------- SPARC
def read_master():
    """SPARC_Lelli2016c.mrt: data rows follow the LAST dashed line; whitespace-split (galaxy names carry no spaces):
    Galaxy T D e_D f_D Inc e_Inc L36 e_L36 Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q Ref"""
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    rows = {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) < 18: continue
        try:
            rows[f[0]] = dict(D=float(f[2]), eD=float(f[3]), inc=float(f[5]), einc=float(f[6]), L36=float(f[7]), MHI=float(f[13]), Vflat=float(f[15]), Q=int(f[17]))
        except ValueError: continue
    return rows
master = read_master()
gals = []
for f in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(f).replace("_rotmod.dat", "")
    if name not in master: continue
    m = master[name]
    if m["Q"] > 2 or m["inc"] < 30: continue
    d = np.loadtxt(f); d = d[d[:, 1] > 0]
    if len(d) < 6: continue
    r, vobs, ev, vg, vd, vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    gbar = (vg*np.abs(vg) + UPS_D*vd**2 + UPS_B*vb**2)/r*KMS2_KPC
    good = gbar > 0
    Mb = (UPS_D*(m["L36"]*1e9) + 1.33*m["MHI"]*1e9)                                # Msun (disk + gas; bulge folded into L36)
    gals.append(dict(name=name, r=r[good], vobs=vobs[good], ev=ev[good], vg=vg[good], vd=vd[good], vb=vb[good], gbar=gbar[good], Mb=Mb, **m))
info(f"SPARC: {len(gals)} galaxies pass Q<=2, i>=30, >=6 points")
# ---------------------------------------------------------------- the framework's kernel and the per-galaxy a_0 fit
def nu(y): y = np.maximum(y, 1e-12); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def fit_loga0(gbar, gobs, sig_log):
    chi2 = lambda la: float(np.sum(((np.log10(gobs) - np.log10(gbar*nu(gbar/10**la)))/sig_log)**2))
    res = minimize_scalar(chi2, bounds=(-12.0, -8.5), method="bounded")
    la = res.x; c0 = res.fun
    # 1-sigma from delta chi2 = 1 (bounded by the search box)
    lo = la - 1.5; hi = la + 1.5
    try: lo = brentq(lambda l: chi2(l) - c0 - 1, la - 3, la)
    except Exception: lo = la - 3
    try: hi = brentq(lambda l: chi2(l) - c0 - 1, la, la + 3)
    except Exception: hi = la + 3
    return la, 0.5*(hi - lo)
def obs_loga0(g, rng=None, perturb=False):
    """per-galaxy log a_0 from the data; with perturb=True, resample within the error budget (V, D, inc, M/L)"""
    r, vobs, vg, vd, vb = g["r"], g["vobs"], g["vg"], g["vd"], g["vb"]
    if perturb:
        fD = 1 + rng.normal(0, g["eD"]/g["D"]); inc = g["inc"] + rng.normal(0, g["einc"]); ups = UPS_D*10**rng.normal(0, 0.1)
        r = r*fD; vobs = vobs*math.sin(math.radians(g["inc"]))/math.sin(math.radians(max(inc, 15.0))) + rng.normal(0, g["ev"])
        vg = vg*math.sqrt(fD); vd = vd*math.sqrt(fD); vb = vb*math.sqrt(fD)
    else: ups = UPS_D
    gbar = (vg*np.abs(vg) + ups*vd**2 + UPS_B*vb**2)/r*KMS2_KPC; gobs = vobs**2/r*KMS2_KPC
    ok = (gbar > 0) & (gobs > 0)
    sig = np.maximum(2*g["ev"]/(np.maximum(g["vobs"], 1.0)*math.log(10)), 0.02)[ok]
    return fit_loga0(gbar[ok], gobs[ok], sig)
# ---------------------------------------------------------------- LCDM halo population
def moster_ratio(Mh):
    M1 = 10**11.59; N = 0.0351; beta = 1.376; gam = 0.608
    return 2*N/((Mh/M1)**(-beta) + (Mh/M1)**gam)
def Mh_of_Mstar(Ms):
    f = lambda lm: math.log10(moster_ratio(10**lm)*10**lm) - math.log10(Ms)
    return 10**brentq(f, 9.0, 15.5)
def c_DM14(Mh): return 10**(0.905 - 0.101*math.log10(Mh*h/1e12))
def g_nfw(r_kpc, Mh, c):
    R200 = (3*Mh/(800*math.pi*rho_crit))**(1/3); x = c*r_kpc/R200
    Menc = Mh*(np.log(1+x) - x/(1+x))/(math.log(1+c) - c/(1+c))
    return G*Menc*Msun/(r_kpc*kpc)**2
def mock_loga0(g, a0, mode, rng):
    """mock g_obs from the FRAMEWORK (universal a_0) or from LCDM (AM halo + NFW), then the same fit with the same noise"""
    r, vg, vd, vb = g["r"], g["vg"], g["vd"], g["vb"]
    gbar_true = (vg*np.abs(vg) + UPS_D*vd**2 + UPS_B*vb**2)/r*KMS2_KPC
    if mode == "framework": gobs_true = gbar_true*nu(gbar_true/a0)
    else:
        Ms = UPS_D*g["L36"]*1e9*10**rng.normal(0, 0.15)                          # stellar mass with the AM scatter
        Mh = Mh_of_Mstar(max(Ms, 1e6)); c = c_DM14(Mh)*10**rng.normal(0, 0.11)
        gobs_true = gbar_true + g_nfw(r, Mh, c)
    vtrue = np.sqrt(np.maximum(gobs_true, 1e-30)/KMS2_KPC*r)
    fD = 1 + rng.normal(0, g["eD"]/g["D"]); inc = g["inc"] + rng.normal(0, g["einc"]); ups = UPS_D*10**rng.normal(0, 0.1)
    rr = r*fD; vobs = vtrue*math.sin(math.radians(g["inc"]))/math.sin(math.radians(max(inc, 15.0))) + rng.normal(0, g["ev"])
    gbar = (vg*np.abs(vg)*fD + ups*vd**2*fD + UPS_B*vb**2*fD)/rr*KMS2_KPC; gobs = vobs**2/rr*KMS2_KPC
    ok = (gbar > 0) & (gobs > 0)
    sig = np.maximum(2*g["ev"]/(np.maximum(vtrue, 1.0)*math.log(10)), 0.02)[ok]
    return fit_loga0(gbar[ok], gobs[ok], sig)
def spread_and_slope(la, sig, logMb):
    """inverse-variance weighted mean, weighted rms spread, and the slope vs log M_b; galaxies with sigma > 0.5 dex dropped"""
    m = sig < 0.5; la, sig, lm = la[m], sig[m], logMb[m]
    w = 1/sig**2; mean = np.sum(w*la)/np.sum(w); rms = math.sqrt(np.sum(w*(la - mean)**2)/np.sum(w))
    A = np.vstack([lm - lm.mean(), np.ones_like(lm)]).T*np.sqrt(w)[:, None]; slope = np.linalg.lstsq(A, la*np.sqrt(w), rcond=None)[0][0]
    return mean, rms, slope, int(m.sum())
logMb = np.array([math.log10(g["Mb"]) for g in gals])
P("="*100); P("1. the data: per-galaxy a_0 with the framework's kernel"); P("="*100)
la_obs = np.array([obs_loga0(g)[0] for g in gals]); sg_obs = np.array([obs_loga0(g)[1] for g in gals])
mean_o, rms_o, slope_o, n_o = spread_and_slope(la_obs, sg_obs, logMb)
info(f"N = {n_o} constrained galaxies: weighted mean log a_0 = {mean_o:.3f} (a_0 = {10**mean_o:.2e}), weighted rms spread = {rms_o:.3f} dex, slope vs log M_b = {slope_o:+.3f} dex/dex")
info(f"reference: canonical a_0 = 9.36e-11 (log {math.log10(9.36e-11):.3f}), alt 1.13e-10 (log {math.log10(1.13e-10):.3f})")
P(""); P("="*100); P("2. mocks with the full error budget (V, D, inc, 0.1 dex M/L): what spread and slope each reading predicts"); P("="*100)
NMC = 60; rng = np.random.default_rng(11)
def run_mock(mode, a0):
    rms, sl = [], []
    for _ in range(NMC):
        la = []; sg = []
        for g in gals:
            l_, s_ = mock_loga0(g, a0, mode, rng); la.append(l_); sg.append(s_)
        _, r_, s2_, _ = spread_and_slope(np.array(la), np.array(sg), logMb); rms.append(r_); sl.append(s2_)
    return np.percentile(rms, [16, 50, 84]), np.percentile(sl, [16, 50, 84])
res = {}
for foot, a0 in A0.items():
    res[("framework", foot)] = run_mock("framework", a0)
    r_, s_ = res[("framework", foot)]
    info(f"FRAMEWORK mock ({foot:9s}): spread = {r_[1]:.3f} [{r_[0]:.3f}-{r_[2]:.3f}] dex (error budget only), slope = {s_[1]:+.3f} [{s_[0]:+.3f},{s_[2]:+.3f}]")
res["lcdm"] = run_mock("lcdm", A0["canonical"]); r_, s_ = res["lcdm"]
info(f"LCDM mock (AM + NFW, c-M scatter):     spread = {r_[1]:.3f} [{r_[0]:.3f}-{r_[2]:.3f}] dex, slope = {s_[1]:+.3f} [{s_[0]:+.3f},{s_[2]:+.3f}]")
P(""); P("="*100); P("3. verdicts"); P("="*100)
intr = {f: math.sqrt(max(rms_o**2 - res[("framework", f)][0][1]**2, 0.0)) for f in A0}
info("intrinsic per-galaxy a_0 spread implied by the data (observed minus the framework's error budget, in quadrature): " + ", ".join(f"{f}: {v:.3f} dex" for f, v in intr.items()))
check("V1 the observed per-galaxy a_0 spread is within 1.5x of the framework's error-budget-only prediction on at least one footing: the data are consistent with ONE a_0 for every galaxy (intrinsic spread <= 0.10 dex)",
      any(rms_o < 1.5*res[("framework", f)][0][1] for f in A0) and min(intr.values()) <= 0.10, f"observed {rms_o:.3f} vs error-only " + ", ".join(f"{f}: {res[('framework', f)][0][1]:.3f}" for f in A0))
check("V2 the LCDM halo population predicts a per-galaxy a_0 spread LARGER than observed (median mock spread > observed): halos carry their population scatter into the RAR, the data do not show it",
      res["lcdm"][0][1] > rms_o, f"LCDM {res['lcdm'][0][1]:.3f} vs observed {rms_o:.3f}")
check("V3 the LCDM halo population predicts a mass trend of the effective a_0 that the data do not show: |observed slope| < |LCDM median slope| and the observed slope lies inside the framework mock's 16-84 range",
      abs(slope_o) < abs(res["lcdm"][1][1]) and any(res[("framework", f)][1][0] - 0.02 <= slope_o <= res[("framework", f)][1][2] + 0.02 for f in A0),
      f"observed {slope_o:+.3f}, LCDM {res['lcdm'][1][1]:+.3f}, framework " + ", ".join(f"{f}: [{res[('framework', f)][1][0]:+.3f},{res[('framework', f)][1][2]:+.3f}]" for f in A0))
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The cold component's gravity is looked for inside galaxies through the one number a halo population cannot keep fixed: the")
P("  per-galaxy acceleration scale.  See V1-V3.  Caveats: the LCDM mock is the plain abundance-matched NFW population without")
P("  adiabatic contraction or feedback, which can tighten it (Keller & Wadsley 2017, Ludlow+ 2017 report 0.05-0.09 dex intrinsic RAR")
P("  scatter in hydrodynamical runs); the error budget is the SPARC one; the framework mock uses the same budget.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
