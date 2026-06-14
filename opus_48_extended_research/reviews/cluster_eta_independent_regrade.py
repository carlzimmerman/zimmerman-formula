#!/usr/bin/env python3
"""INDEPENDENT regrade of the cluster eta forensic. Recompute every load-bearing number
from scratch off the raw FITS, with no reuse of the forensic's helper functions, and
verify the equipment claims (M500 = WL-calibrated scaling mass) directly from the data."""
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685; Om = 0.315
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
A0_FRAME = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)   # 9.36e-11 pure dark energy
A0_TOT   = 0.5*c*np.sqrt(G*1.0*RHO_CRIT0)   # rho_total/cH0 -> sqrt(Om+OmL)=sqrt(1)=... check
A0_MOND  = 1.2e-10

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

d = fits.open(FITS)[1].data
def f(col): return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[col]], float)

# raw columns
z, M500, Mgas, fgas, R500, KT = f("BEST_Z"), f("M500"), f("MGAS500"), f("FGAS500"), f("R500"), f("KT")
# luminosity / count rate columns for the equipment check
cols = d.columns.names
print("FITS has %d columns. Mass/observable-related:" % len(cols))
for cand in ["L500","LX500","CR500","COUNT_RATE","M500_L","M500_H"]:
    matches = [cc for cc in cols if cand.upper() in cc.upper()]
    if matches: print("  ", cand, "->", matches)

L500 = None
for cc in cols:
    if "L500" in cc.upper() and "ERR" not in cc.upper() and "_L" != cc[-2:].upper() and "_H" != cc[-2:].upper():
        L500 = f(cc); print("using luminosity col:", cc); break
CR = None
for cc in cols:
    if "CR500" in cc.upper() or "RATE" in cc.upper():
        CR = f(cc); print("using count-rate col:", cc); break
M500H, M500L = f("M500_H"), f("M500_L")

ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
N = int(ok.sum())
print("\nClean N = %d, median z = %.3f, median fgas = %.4f" % (N, np.median(z[ok]), np.median(fgas[ok])))

# ---- EQUIPMENT: is M500 a scaling-relation (count-rate/luminosity) mass? ----
def scatter_slope(x, y):
    m = np.isfinite(x)&np.isfinite(y)&(x>0)&(y>0)
    lx, ly = np.log10(x[m]), np.log10(y[m])
    A = np.vstack([lx, np.ones_like(lx)]).T
    slope, icpt = np.linalg.lstsq(A, ly, rcond=None)[0]
    resid = ly - (slope*lx+icpt)
    return np.std(resid), slope, m.sum()
print("\n-- EQUIPMENT: log M500 vs observable (lower scatter => deterministic scaling mass) --")
for lab, x in [("L500", L500), ("CR500", CR), ("KT", KT)]:
    if x is None: print("  %-7s: column not found" % lab); continue
    sc, sl, n = scatter_slope(x[ok], M500[ok])
    print("  log M500 vs log %-6s: scatter %.3f dex, slope %.3f, N=%d" % (lab, sc, sl, n))

# ---- accelerations ----
def accels(fstar):
    M_kg = M500[ok]*1e13*Msun
    Mb_kg = (1+fstar)*Mgas[ok]*1e11*Msun
    R_m = R500[ok]*kpc
    return G*M_kg/R_m**2, G*Mb_kg/R_m**2
gobs, _ = accels(0.0)
print("\nmedian g_obs/a0 (framework) = %.3f  [regime: deep-MOND if <<1, transition if ~0.5]" % np.median(gobs/A0_FRAME))

# ---- interpolation families ----
def nu_simple(y):   return 0.5 + np.sqrt(0.25 + 1.0/y)
def nu_standard(y): return np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y**2))
def nu_rar(y):      return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_n2(y):       return np.sqrt(1.0 + 1.0/y)
NUS = {"simple":nu_simple,"standard":nu_standard,"RAR":nu_rar,"sqrt":nu_n2}

def etaA(gobs, gbar, a0, nu): return gobs/(nu(gbar/a0)*gbar)
def etaB(gobs, gbar, a0):
    gN = np.array([brentq(lambda x: nu_simple(x/a0)*x - go, go*1e-9, go*100) for go in gobs])
    return gN/gbar

print("\n-- Def A (g-space) across interp, framework a0, fstar=0.2 --")
gobs, gbar = accels(0.2)
for nm,nu in NUS.items():
    e = etaA(gobs,gbar,A0_FRAME,nu)
    print("  %-9s median %.3f geomean %.3f" % (nm, np.median(e), 10**np.mean(np.log10(e))))

print("\n-- baryon sweep (simple nu, framework a0) Def A and Def B --")
for fstar in (0.0,0.2,0.5,0.7,1.0):
    gobs,gbar = accels(fstar)
    eA = etaA(gobs,gbar,A0_FRAME,nu_simple)
    eB = etaB(gobs,gbar,A0_FRAME)
    print("  fstar=%.2f  etaA %.3f  etaB %.3f" % (fstar, np.median(eA), np.median(eB)))

print("\n-- a0 lever (simple nu, fstar=0.2) --")
gobs,gbar = accels(0.2)
for lab,a0 in (("framework 9.36e-11",A0_FRAME),("rho_tot/cH0",A0_TOT),("canonical 1.2e-10",A0_MOND)):
    e = etaA(gobs,gbar,a0,nu_simple)
    print("  %-22s a0=%.3e etaA median %.3f" % (lab, a0, np.median(e)))
print("  sqrt(1.2e-10/9.36e-11) = %.3f" % np.sqrt(A0_MOND/A0_FRAME))

print("\n-- significance --")
gobs,gbar = accels(0.2)
logeta = np.log10(etaA(gobs,gbar,A0_FRAME,nu_simple))
print("  mean log eta = %+.4f dex, scatter %.4f dex, N=%d" % (np.mean(logeta), np.std(logeta), N))
for floor in (0.10,0.15,0.20):
    print("    vs %.2f dex floor: %.1f sigma" % (floor, np.mean(logeta)/floor))

# ---- Zhang2026 mapping cross-check: their frame is r200 deep-MOND, ICM-only ----
print("\n-- Zhang2026 frame replication (deep-MOND asymptote, gas-only, etaB-style) --")
# In deep MOND: M_dyn/M_bar = sqrt(g_obs/a0)*... ; use their reported numbers as anchor
print("  Zhang reported: ICM-only 52%% of M_dyn => eta=1/0.52=%.2f; +IGIMF remnants 88%% => eta=%.2f" %
      (1/0.52, 1/0.88))
# eRASS1 Zhang-regime subsample: z<0.1 and M500>5e14 (=50 in 1e13 units)
zsub = (z[ok]<0.1)&(M500[ok]>50)
print("  eRASS1 Zhang-regime subsample (z<0.1, M500>5e14): N=%d" % zsub.sum())
if zsub.sum()>5:
    gobs0,gbar0 = accels(0.0)
    eB_sub = etaB(gobs0[zsub], gbar0[zsub], A0_FRAME)
    print("    gas-only Def B on this subsample: median %.2f (vs Zhang 1.92)" % np.median(eB_sub))
