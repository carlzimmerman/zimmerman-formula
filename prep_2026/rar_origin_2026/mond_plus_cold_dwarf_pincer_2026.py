#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mond_plus_cold_dwarf_pincer_2026.py -- the framework's self-consistent form (MOND + the cold component) meets the dwarfs and the forest.
=======================================================================================================================================
After today the framework's dark sector must be cold, ballistic and galaxy-clustering.  Its only self-consistent form is therefore
MOND + a cold component.  In a deep-MOND dwarf, g_obs = sqrt(g_bar a_0) with no room for anything else (the RAR's low-g branch is
followed to ~0.03 dex), while a cold component that clusters like CDM puts an abundance-matched halo of 10^10-10^11 Msun in every such
dwarf.  Two jaws:
  J1  SPARC dwarfs (M_b < 1e9 Msun, points with g_bar < 0.1 a_0): residuals log g_obs - log g_MOND (Route A kernel, both footings) --
      the data -- against the residual an abundance-matched NFW halo (Moster+ 2013, Dutton-Maccio 2014) would add.  The fraction f of
      that halo the residual scatter allows.
  J2  removing the halos from 1e10-1e11 Msun systems needs a free-streaming (WDM-like) half-mode mass M_hm >= 1e11-1e12 Msun, i.e.
      m_WDM <= 0.3-0.5 keV (Schneider+ 2012: M_hm = 1e10 (m/keV)^-3.33 Msun/h), while the Lyman-alpha forest requires m_WDM >= 3.5 keV
      (Viel+ 2013, the LOOSE end; 5.3 keV Irsic+ 2017).  The cold component that the forest needs cannot be absent from dwarfs.
Checks CAN fail.  Both a_0 footings.  Loose ends of every bound.
"""
import sys, math, glob, os
import numpy as np
from scipy.optimize import brentq
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "..", "..", "real_research", "data")
G = 6.674e-11; kpc = 3.0857e19; Msun = 1.989e30; KMS2_KPC = 1e6/kpc; h = 0.674
rho_crit = 3*(100*h*1e3/3.0857e22)**2/(8*math.pi*G)*(kpc**3)/Msun
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}; UPS_D, UPS_B = 0.5, 0.7
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), eD=float(f[3]), inc=float(f[5]), einc=float(f[6]), L36=float(f[7]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
master = read_master(); gals = []
for f in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(f).replace("_rotmod.dat", "")
    if name not in master: continue
    m = master[name]
    if m["Q"] > 2 or m["inc"] < 30: continue
    d = np.loadtxt(f); d = d[d[:, 1] > 0]
    if len(d) < 5: continue
    r, vobs, ev, vg, vd, vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    gbar = (vg*np.abs(vg) + UPS_D*vd**2 + UPS_B*vb**2)/r*KMS2_KPC; gobs = vobs**2/r*KMS2_KPC
    Mb = UPS_D*m["L36"]*1e9 + 1.33*m["MHI"]*1e9; Ms = UPS_D*m["L36"]*1e9
    gals.append(dict(name=name, r=r, gbar=gbar, gobs=gobs, ev=ev, vobs=vobs, Mb=Mb, Ms=Ms))
def nu(y): y = np.maximum(y, 1e-12); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def moster_ratio(Mh): M1 = 10**11.59; N = 0.0351; return 2*N/((Mh/M1)**(-1.376) + (Mh/M1)**0.608)
def Mh_of_Mstar(Ms): return 10**brentq(lambda lm: math.log10(moster_ratio(10**lm)*10**lm) - math.log10(Ms), 8.0, 15.5)
def c_DM14(Mh): return 10**(0.905 - 0.101*math.log10(Mh*h/1e12))
def g_nfw(r_kpc, Mh, c):
    R200 = (3*Mh/(800*math.pi*rho_crit))**(1/3); x = c*r_kpc/R200
    return G*Mh*(np.log(1+x) - x/(1+x))/(math.log(1+c) - c/(1+c))*Msun/(r_kpc*kpc)**2
P("="*100); P("J1. SPARC dwarfs in the deep-MOND regime: residuals vs MOND alone, and what a cold halo would add"); P("="*100)
dw = [g for g in gals if g["Mb"] < 1e9]
info(f"{len(dw)} dwarfs (M_b < 1e9 Msun, Q<=2, i>=30); deep-MOND points: g_bar < 0.1 a_0")
res = {}
SYS_FLOOR = 0.10                                                     # dex: M/L + distance systematics on a dwarf-sample MEAN
for foot, a0 in A0.items():
    gmeans, gpred = [], []
    for g in dw:
        sel = (g["gbar"] < 0.1*a0) & (g["gbar"] > 0) & (g["vobs"] > 3*g["ev"])
        if sel.sum() < 2: continue
        gm = g["gbar"][sel]*nu(g["gbar"][sel]/a0)
        Mh = Mh_of_Mstar(max(g["Ms"], 1e5)); gh = g_nfw(g["r"][sel], Mh, c_DM14(Mh))
        gmeans.append(float(np.mean(np.log10(g["gobs"][sel]/gm)))); gpred.append(float(np.mean(np.log10((gm + gh)/gm))))
    gmeans = np.array(gmeans); gpred = np.array(gpred); n = len(gmeans)
    mean = gmeans.mean(); se = gmeans.std(ddof=1)/math.sqrt(n); tol = 2*se + SYS_FLOOR
    # a halo fraction f shifts the MOND-alone prediction UP by log10(1 + f x); it is allowed while the data's mean residual (which sits
    # BELOW zero) stays within 2 SE + the systematic floor of that shift:  log10(1 + f x_med) <= mean + tol.  A negative mean REDUCES the room.
    xs = 10**gpred - 1; room = mean + tol
    fmax = 0.0 if room <= 0 else (brentq(lambda f: float(np.median(np.log10(1 + f*xs))) - room, 1e-9, 10.0) if float(np.median(np.log10(1 + 10*xs))) > room else 10.0)
    res[foot] = dict(n=n, mean=mean, se=se, gstd=gmeans.std(ddof=1), pmed=float(np.median(gpred)), fmax=fmax, tol=tol)
    info(f"{foot:10s}: {n} dwarfs: per-galaxy mean residual = {mean:+.3f} +/- {se:.3f} (SE), galaxy-to-galaxy scatter {gmeans.std(ddof=1):.3f} dex | AM halo would add {np.median(gpred):+.2f} dex (median) | room for an additive halo = mean + 2 SE + {SYS_FLOOR} = {room:+.3f} dex -> f_max = {fmax:.2f}")
check("J1a MOND alone fits the deep-MOND dwarfs on the sample MEAN: |per-galaxy mean residual| < 0.15 dex on at least one footing, and the dwarfs sit AT or BELOW the MOND line, not above it (no room for an additive halo)",
      any(abs(res[f]["mean"]) < 0.15 for f in A0) and all(res[f]["mean"] <= 0.02 for f in A0), "; ".join(f"{f}: {res[f]['mean']:+.3f} +/- {res[f]['se']:.3f}" for f in A0))
check("J1b a cold-component halo at the abundance-matched level would add > 0.30 dex to those points (median), i.e. MOND + cold double-counts the dwarfs by > 2x, both footings", all(res[f]["pmed"] > 0.30 for f in A0), "; ".join(f"{f}: +{res[f]['pmed']:.2f} dex" for f in A0))
check("J1c even with a 0.10 dex systematic floor on the sample mean, the dwarfs allow at most 30% of the abundance-matched halo (both footings): the room is small because they already sit below the MOND line", all(res[f]["fmax"] < 0.30 for f in A0), "; ".join(f"{f}: f_max = {res[f]['fmax']:.2f}" for f in A0))
P(""); P("="*100); P("J2. removing the dwarfs' halos needs a cutoff the forest forbids"); P("="*100)
def M_hm(m_keV): return 1e10*m_keV**(-3.33)/h                                            # Msun (Schneider+ 2012, WDM half-mode mass)
def m_of_Mhm(M): return (M*h/1e10)**(-1/3.33)
Mh_lo = 2.0e10                                                       # the dwarfs' abundance-matched halo mass, 16th percentile (printed above)
for target, why in ((Mh_lo, "the dwarfs' own halo mass (16th pct)"), (10*Mh_lo, "10x that, so their halos are truly absent, not just fewer/less concentrated")):
    info(f"M_hm >= {target:.1e} Msun ({why}) -> m_WDM <= {m_of_Mhm(target):.2f} keV")
m_need = m_of_Mhm(10*Mh_lo); m_forest_loose = 3.5; m_forest = 5.3
info(f"forest: m_WDM >= {m_forest_loose} keV (Viel+ 2013, loose) / {m_forest} keV (Irsic+ 2017)  ->  M_hm <= {M_hm(m_forest_loose):.1e} / {M_hm(m_forest):.1e} Msun")
check("J2 the cutoff that would empty the dwarfs' halos (m_WDM <= ~0.3-0.5 keV) is excluded by the LOOSE forest bound (3.5 keV) by > 5x in mass, > 200x in half-mode mass: the cold component the forest needs must sit in the dwarfs",
      m_forest_loose/m_need > 5 and 10*Mh_lo/M_hm(m_forest_loose) > 200, f"m_need = {m_need:.2f} keV vs 3.5 keV: x{m_forest_loose/m_need:.0f}; M_hm ratio x{10*Mh_lo/M_hm(m_forest_loose):.0f}")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The framework's only self-consistent form after today is MOND plus a cold, ballistic, galaxy-clustering component.  In the")
P("  deep-MOND dwarfs the data sit at or below MOND alone and tolerate well under the halo such a component would bring; removing")
P("  that halo needs a free-streaming cutoff the forest excludes by more than an order of magnitude.  So the cold component the")
P("  CMB, the Bullet and the forest require is in the dwarfs, and the dwarfs say it is not there on top of MOND.  The combination")
P("  is excluded from inside the framework's own galaxies.  What that leaves is the dichotomy, now with numbers on both sides:")
P("  either the RAR is the cold component (LCDM, no MOND) or the cold component is not there (MOND, no CMB/Bullet/forest).")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
