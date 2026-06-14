#!/usr/bin/env python3
"""HOSTILE INDEPENDENT RECHECK of the baryon-budget forensic eta ladder.
Recompute every load-bearing number from scratch on the real eRASS1 FITS.
Goal: confirm or break (a) the framework a0 value, (b) the eta ladder,
(c) the deep-MOND scaling, (d) the massive-cluster gas-complete sub-test,
(e) the f_b=0.48 -> eta=1 nonphysical claim, (f) the a0/interp both-ways spread.
"""
import numpy as np
from astropy.io import fits

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685; Om = 0.315
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)

# ---- (a) framework a0 from scratch, two written forms ----
# claimed: a0 = c^2 sqrt(Lambda/32pi). Lambda = 3 OmL H0^2 / c^2 (so rho_DE = OmL rho_crit).
Lambda = 3*OmL*H0**2 / c**2
a0_closedform = c**2 * np.sqrt(Lambda/(32*np.pi))
# script form: 0.5*c*sqrt(G*rho_DE0)
a0_scriptform = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)
A0_FRAME = a0_scriptform
A0_MOND = 1.2e-10
A0_TOT = 1.13e-10  # rho_total/cH0 footing (claimed)
fb_cosmic = 0.157  # Omega_b/Omega_m

print("=== (a) a0 cross-check ===")
print(f"  a0 (c^2 sqrt(Lambda/32pi)) = {a0_closedform:.4e}")
print(f"  a0 (0.5 c sqrt(G rho_DE))  = {a0_scriptform:.4e}")
print(f"  agree? {np.isclose(a0_closedform, a0_scriptform, rtol=1e-3)}  ; banked value 9.36e-11")
print(f"  inflate factor vs canonical = sqrt(1.2e-10/a0) = {np.sqrt(A0_MOND/A0_FRAME):.4f}")

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

def load():
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("","--","nan") else np.nan for v in d[col]], float)
    z, M500, Mgas, fgas, R500 = f("BEST_Z"), f("M500"), f("MGAS500"), f("FGAS500"), f("R500")
    ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
    return dict(z=z[ok], M500=M500[ok]*1e13*Msun, M500_13=M500[ok]*1e13,
                Mgas=Mgas[ok]*1e11*Msun, fgas=fgas[ok], R500=R500[ok]*kpc, N=int(ok.sum()))

d = load()
print(f"\n=== sample ===  N={d['N']}  z_med={np.median(d['z']):.2f}  M500_med={np.median(d['M500_13']):.3e} Msun")
print(f"  fgas_med (X-ray gas) = {np.median(d['fgas']):.4f}")

gobs = G*d['M500']/d['R500']**2
print(f"  g_bar(gas)/a0 median = {np.median(G*d['Mgas']/d['R500']**2/A0_FRAME):.4f} (deep-MOND regime)")

# interpolation functions
def nu_simple(y):   return 0.5 + np.sqrt(0.25 + 1.0/y)            # framework dSU/simple
def nu_standard(y): return np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y**2))
def nu_rar(y):      return 1.0/(1.0 - np.exp(-np.sqrt(y)))

def eta(Mbar, a0, nu):
    gbar = G*Mbar/d['R500']**2
    gpred = nu(gbar/a0)*gbar
    e = gobs/gpred
    return np.median(e), 10**np.mean(np.log10(e))

# ---- (b) the eta ladder, framework a0, simple nu ----
print("\n=== (b) eta ladder (framework a0, simple/dSU nu): median (geomean) ===")
ladders = [
    ("gas only",                 d['Mgas']),
    ("gas + 0.2*gas stars",      1.2*d['Mgas']),
    ("gas + stars+ICL x1.65",    1.65*d['Mgas']),
]
for lab, Mb in ladders:
    m, gm = eta(Mb, A0_FRAME, nu_simple)
    print(f"  {lab:28s} {m:.3f} ({gm:.3f})")

# gas raised to a target f_b within R500: M_bar = f_b * M500
for lab, fb in [("gas->0.85*cosmic in R500", 0.85*fb_cosmic),
                ("gas->FULL cosmic in R500", fb_cosmic)]:
    Mb = fb*d['M500']
    m, gm = eta(Mb, A0_FRAME, nu_simple)
    print(f"  {lab:28s} {m:.3f} ({gm:.3f})  (f_b={fb:.3f})")

# ---- (e) what f_b within R500 drives eta_median to 1? ----
print("\n=== (e) f_b within R500 needed for eta_median=1 ===")
from scipy.optimize import brentq
def eta_med_at_fb(fb):
    Mb = fb*d['M500']
    gbar = G*Mb/d['R500']**2
    return np.median(gobs/(nu_simple(gbar/A0_FRAME)*gbar))
fb1 = brentq(lambda fb: eta_med_at_fb(fb)-1.0, 0.05, 1.0)
print(f"  f_b for eta=1: {fb1:.3f}  = {fb1/fb_cosmic:.2f}x cosmic   (claim: 0.48 = 3.1x)")

# ---- (c) deep-MOND scaling eta ~ 1/sqrt(M_bar) ----
print("\n=== (c) deep-MOND scaling check ===")
eg, _ = eta(d['Mgas'], A0_FRAME, nu_simple)
ec, _ = eta(fb_cosmic*d['M500'], A0_FRAME, nu_simple)
Mgas_med = np.median(d['Mgas']); Mcos_med = np.median(fb_cosmic*d['M500'])
print(f"  eta(gas)/eta(cosmic) = {eg/ec:.3f}   sqrt(M_cos/M_gas)_med = {np.sqrt(Mcos_med/Mgas_med):.3f}")

# ---- (f) both-ways a0 x interp spread at gas-only and full-cosmic ----
print("\n=== (f) both-ways a0 x interp spread ===")
for tag, Mb in [("gas-only", d['Mgas']), ("full-cosmic-in-R500", fb_cosmic*d['M500'])]:
    vals = []
    for a0 in (A0_FRAME, A0_TOT, A0_MOND):
        for nu in (nu_simple, nu_standard, nu_rar):
            vals.append(eta(Mb, a0, nu)[0])
    print(f"  {tag:22s} median eta spans [{min(vals):.2f}, {max(vals):.2f}] over 3 a0 x 3 nu")

# canonical a0 effect at gas-only (simple nu)
print(f"  gas-only framework a0 = {eta(d['Mgas'],A0_FRAME,nu_simple)[0]:.3f} ; canonical a0 = {eta(d['Mgas'],A0_MOND,nu_simple)[0]:.3f}")

# ---- (d) massive-cluster gas-complete sub-test (hand them X-COP f_b=0.146) ----
print("\n=== (d) massive cluster sub-test (deficit where budget is complete) ===")
fb_xcop = 0.146
for Mcut in (3e14, 5e14, 7e14):
    sel = d['M500_13'] >= Mcut
    Nsel = sel.sum()
    fgas_med = np.median(d['fgas'][sel])
    # eta with gas+0.2stars
    Mb_gs = 1.2*d['Mgas'][sel]
    gbar = G*Mb_gs/d['R500'][sel]**2
    e_gs = np.median(gobs[sel]/(nu_simple(gbar/A0_FRAME)*gbar))
    # eta handing them full X-COP universal f_b
    Mb_x = fb_xcop*d['M500'][sel]
    gbarx = G*Mb_x/d['R500'][sel]**2
    e_x = np.median(gobs[sel]/(nu_simple(gbarx/A0_FRAME)*gbarx))
    print(f"  M500>={Mcut:.0e}  N={Nsel:5d}  fgas_med={fgas_med:.3f}  eta(gas+0.2*)={e_gs:.2f}  eta(@f_b=0.146)={e_x:.2f}")

# f_b within R500 reported
print("\n=== f_b within R500 ===")
print(f"  gas: <f_gas>_med = {np.median(d['fgas']):.4f} ; gas+0.2stars f_b = {1.2*np.median(d['fgas']):.4f} ; cosmic 0.157")
