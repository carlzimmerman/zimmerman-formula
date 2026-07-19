#!/usr/bin/env python3
"""
CONFRONTATION LANE  --  galaxy-side a0(z) vs the two COSMIC reference tracks.
=============================================================================
Cross-scale a0(z) test, de Sitter-Unruh MODIFIED-INERTIA framework (C. P.
Zimmerman). The framework FORCES the galaxy acceleration scale to track the
cosmic dark-energy density:  a0(z) = c^2 sqrt(rho_DE(z)/32pi), i.e.
  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)   (a BRIDGE between two INDEPENDENT
measurements: galaxy dynamics [BTFR zero-point] vs cosmic rho_DE [SNe/DESI]).
LCDM gives NO reason for a galaxy's acceleration scale to track cosmic
expansion; the framework does. This lane does the CONFRONTATION:

  galaxy-side a0(z)/a0(0)  (from galaxy_a0z.py, the Lambda-blind BTFR readout)
     -- confronted against --
  COSMIC track A: flat-Lambda  (w=-1)         -> a0(z)/a0(0) = 1.0  (all z)
  COSMIC track B: DESI-DR2 evolving (w0,wa)   -> a0(3)/a0(0) ~ 0.70 (declining)

Questions answered:
  Q1  Does the galaxy a0(z) PREFER flat or declining, and at what significance?
  Q2  Is the test CONSTRAINING (separates the two tracks >2sigma) or
      UNDERPOWERED (consistent with BOTH)?  -> the SEPARABILITY statistic.
  Q3  The z=0 tie:  galaxy a0(0) vs the cosmic a0(0) implied by rho_DE0.
  Q4  Both footings (canonical rho_DE/cH_Lambda vs alt rho_total/cH0).
  Q5  FORECAST: how many z~2-3 rotators, at what BTFR precision, decisively
      (3sigma) separate flat from the 0.60-0.75 decline (ELT/JWST/ALMA)?

Ratios cancel the a0 FOOTING; it re-enters only in the Big-Wheel ABSOLUTE
(Q4), shown all three ways. NO 'proves'; a0 magnitude inherits the posited Z;
only the RATIO/tracking is tested. High-z M_bar is the dominant systematic and
carries a MILD distance-cosmology dependence -- but testing a0-tracks-rho_DE
does NOT assume the DE evolution (a wrong background shifts all points
together, it does not manufacture a decline), so it is not circular in the
fatal sense.

Exit 0. numpy/scipy only. Outputs to this directory. Frozen repo READ-ONLY.

Credits: Milgrom 1999 (nu-kernel + BTFR, a0 propto sqrt(rho_vac)); McGaugh &
Lelli (SPARC BTFR); Ubler+2017, Tiley+2019, Di Teodoro+2016, Sharma+2024
(high-z TFR); Big Wheel arXiv:2409.17956; Limbach-Psaltis-Ozel 2008
(a0 propto sqrt(rho_DE)); Brout+2022 / DESI DR2 (rho_DE(z)).
"""
import numpy as np
from scipy.stats import norm

np.random.seed(0)
G, Msun, c = 6.67430e-11, 1.98892e30, 2.99792458e8
MPC = 3.0856776e22

# --------------------------------------------------------------------------
# COSMIC reference tracks   a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
#   CPL: rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
# --------------------------------------------------------------------------
def rhoDE_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
def a0_track(z, w0, wa):
    return np.sqrt(rhoDE_ratio(z, w0, wa))

FLAT = (-1.00, 0.00)     # flat-Lambda  -> 1.0
DESI = (-0.75, -0.90)    # DESI-DR2 evolving -> ~0.70 by z~3 (declining)
Om   = 0.315
def Ez(z): return np.sqrt(Om*(1+z)**3 + (1-Om))   # alt-cH0 footing rises as E(z)

print("="*78)
print("CONFRONTATION: galaxy-side a0(z)  vs  cosmic rho_DE(z)  [flat vs DESI-evolving]")
print("="*78)
zshow = np.array([0.5, 1.0, 2.0, 3.0, 3.25])
print("Cosmic reference a0(z)/a0(0):")
print(f"  {'z':>5} | {'flat-Lambda':>11} | {'DESI-evolve':>11} | {'flat-DESI sep(dex)':>18} | {'alt cH0(rise)':>13}")
for z in zshow:
    tf, td = a0_track(z,*FLAT), a0_track(z,*DESI)
    print(f"  {z:5.2f} | {tf:11.3f} | {td:11.3f} | {np.log10(tf/td):18.3f} | {Ez(z):13.3f}")
print("  framework DISTINCTIVE prediction: a0(3)/a0(0) ~ 0.60-0.75 (declining).")
print(f"  [DESI track at z=3.00 = {a0_track(3.0,*DESI):.3f}, at z=3.25 = {a0_track(3.25,*DESI):.3f}]\n")

# --------------------------------------------------------------------------
# GALAXY-SIDE a0(z)/a0(0)  --  reproduced from galaxy_a0z.py (identical inputs)
# --------------------------------------------------------------------------
A0_SPARC, A0_SPARC_E = 1.181e-10, 1.90e-11         # z=0 anchor, Lambda-blind (16%)
A0_CANON, A0_ALT     = 9.355e-11, 1.1305e-10       # framework footings

# --- z=3.25 Big Wheel Monte-Carlo (the one clean deep-MOND high-z datum) ---
V_rot, V_err, sig_int = 280.0, 31.0, 61.0
Mstar, Mstar_e = 1.7e11, 0.7e11
Mgas,  Mgas_e  = 1.8e11, 0.9e11
HE, n = 1.36, 400000
V   = np.random.normal(V_rot, V_err, n)*1e3
Vc2 = V**2 + 3.4*(sig_int*1e3)**2
Ms  = np.clip(np.random.normal(Mstar, Mstar_e, n), 0.05e11, None)
Mg  = np.clip(np.random.normal(Mgas,  Mgas_e,  n), 0.05e11, None)
a0BW = Vc2**2/(G*(Ms+HE*Mg)*Msun)
bw_lo, bw_med, bw_hi = np.percentile(a0BW, [16,50,84])

def a0ratio_from_db(db):     # naive deep-MOND map: Delta log a0 = -Delta_b (slope 4)
    return 10.0**(-db)

# honest galaxy a0(z)/a0(0) points (matches galaxy_a0z.py section 4)
gz   = np.array([0.0, 1.0, 2.3, 3.25])
gr   = np.array([1.00,
                 np.median([a0ratio_from_db(-0.44), a0ratio_from_db(+1.17), 1.0, 1.0]),
                 a0ratio_from_db(-0.27),
                 bw_med/A0_SPARC])
gerr = np.array([A0_SPARC_E/A0_SPARC/np.log(10),        # z0 SPARC 16%
                 0.35, 0.30,                            # z1/z2.3 systematics-dominated
                 0.5*(np.log10(bw_hi)-np.log10(bw_lo))])# z3.25 Big Wheel MC
clean = np.array([True, False, False, True])            # deep-MOND (a0-valid) flag

print("-"*78)
print("GALAXY-SIDE a0(z)/a0(0) points confronted (dex errors; clean=deep-MOND a0-valid):")
print("-"*78)
print(f"  {'z':>5} | {'a0/a0_0':>8} | {'+/-dex':>7} | {'clean':>5} | {'vs flat':>10} | {'vs DESI':>10}")
for z, r, ed, cl in zip(gz, gr, gerr, clean):
    tf, td = a0_track(z,*FLAT), a0_track(z,*DESI)
    sf = abs(np.log10(r/tf))/ed
    sd = abs(np.log10(r/td))/ed
    print(f"  {z:5.2f} | {r:8.2f} | {ed:7.2f} | {str(cl):>5} | {sf:6.1f} sig | {sd:6.1f} sig")
print()

# --------------------------------------------------------------------------
# Q1  Does the data PREFER flat or declining?  Per-point + JOINT chi2.
# --------------------------------------------------------------------------
def chi2_track(track, mask=None):
    m = np.ones_like(gz, bool) if mask is None else mask
    d = np.log10(gr[m]) - np.log10([a0_track(z,*track) for z in gz[m]])
    return np.sum((d/gerr[m])**2)

print("="*78)
print("Q1  Does the galaxy a0(z) PREFER flat or declining?  (joint chi2, lower=better fit)")
print("="*78)
for label, mask in [("ALL 4 points", None),
                    ("CLEAN deep-MOND only (z=0 + Big Wheel z=3.25)", clean)]:
    cf = chi2_track(FLAT, mask); cd = chi2_track(DESI, mask)
    nd = int(np.sum(np.ones_like(gz,bool) if mask is None else mask))
    dchi = cf - cd
    pref = "declining (DESI)" if dchi > 0 else "flat-Lambda"
    print(f"  {label} (N={nd}):")
    print(f"    chi2(flat)={cf:.2f}   chi2(DESI-decl)={cd:.2f}   Delta = {dchi:+.2f}")
    print(f"    -> data mildly prefer {pref}, |Delta chi2|={abs(dchi):.2f} "
          f"({'NOT significant, <1 for 0 extra dof' if abs(dchi)<1 else 'weak'})")
print()

# --------------------------------------------------------------------------
# Q2  CONSTRAINING or UNDERPOWERED?  -> the SEPARABILITY between the two tracks.
#     If the flat and declining tracks were the two hypotheses, the maximum
#     distinguishing power the CURRENT errors permit is
#       S = sqrt( sum_i [ (log a0_flat(z_i) - log a0_DESI(z_i)) / sigma_i ]^2 ).
#     S<2 => the data CANNOT separate them (underpowered); S>2 => constraining.
# --------------------------------------------------------------------------
def separability(mask=None):
    m = np.ones_like(gz, bool) if mask is None else mask
    sep = np.array([np.log10(a0_track(z,*FLAT)/a0_track(z,*DESI)) for z in gz[m]])
    return np.sqrt(np.sum((sep/gerr[m])**2))

print("="*78)
print("Q2  CONSTRAINING or UNDERPOWERED?  (separability of flat vs DESI given current errors)")
print("="*78)
S_all   = separability(None)
S_clean = separability(clean)
# Big Wheel alone (the sharpest single lever)
sep_bw  = np.log10(a0_track(3.25,*FLAT)/a0_track(3.25,*DESI))
S_bw    = abs(sep_bw)/gerr[-1]
print(f"  track separation at z=3.25 = {abs(sep_bw):.3f} dex; Big-Wheel error = {gerr[-1]:.3f} dex")
print(f"    -> Big Wheel alone separates flat vs DESI at only {S_bw:.2f} sigma.")
print(f"  Joint separability, CLEAN probes (z=0 + z=3.25) : S = {S_clean:.2f} sigma")
print(f"  Joint separability, ALL 4 points               : S = {S_all:.2f} sigma")
verdict = "CONSTRAINING (>2sigma)" if S_all > 2 else "UNDERPOWERED (<2sigma: consistent with BOTH)"
print(f"  => VERDICT: {verdict}")
print( "     The current galaxy a0(z) CANNOT distinguish the 0.70 decline from flat:")
print( "     the M_bar systematic (~0.23 dex on the clean z=3.25 datum, ~0.30-0.35 dex")
print( "     on the sign-contested intermediate-z points) EXCEEDS the 0.157-dex signal.\n")

# --------------------------------------------------------------------------
# Q3  the z=0 TIE  --  galaxy a0(0) vs the cosmic a0(0) implied by rho_DE0.
#     a0(0) = (c/2) sqrt(G rho_DE0),  rho_DE0 = Omega_DE * 3 H0^2/(8 pi G).
# --------------------------------------------------------------------------
def a0_from_cosmo(OmDE, H0):    # H0 in km/s/Mpc
    H0si = H0*1e3/MPC
    rho = OmDE*3*H0si**2/(8*np.pi*G)
    return (c/2)*np.sqrt(G*rho)

print("="*78)
print("Q3  the z=0 TIE:  galaxy-measured a0(0) vs cosmic a0(0) = (c/2)sqrt(G rho_DE0)")
print("="*78)
print(f"  SPARC galaxy a0(0) (Lambda-blind) = {A0_SPARC:.3e} +/- {A0_SPARC_E:.2e} (16%)")
for OmDE, H0, tag in [(0.685, 67.4, "Planck  Om_DE=0.685, H0=67.4"),
                      (0.685, 73.0, "SH0ES-H0 Om_DE=0.685, H0=73.0")]:
    a0c = a0_from_cosmo(OmDE, H0)
    sig = abs(np.log(A0_SPARC/a0c))/(A0_SPARC_E/A0_SPARC)
    print(f"    cosmic a0(0) [{tag}] = {a0c:.3e}  ratio a0_SPARC/a0_cosmic="
          f"{A0_SPARC/a0c:.3f}  ({sig:.2f} sigma)")
print("  -> the z=0 tie HOLDS at ~1 sigma on the canonical (Planck-H0) footing:")
print("     the galaxy acceleration scale and the cosmic rho_DE0 agree at z=0 by")
print("     construction of the framework (this anchor is what the bridge extends).\n")

# --------------------------------------------------------------------------
# Q4  BOTH FOOTINGS  --  the Big-Wheel absolute (where the footing re-enters).
# --------------------------------------------------------------------------
print("="*78)
print("Q4  BOTH FOOTINGS (ratios cancel; footing re-enters only in Big-Wheel absolute):")
print("="*78)
print(f"  Big Wheel a0_eff(z=3.25) = {bw_med*1e10:.2f} "
      f"(+{(bw_hi-bw_med)*1e10:.2f}/-{(bw_med-bw_lo)*1e10:.2f}) e-10 m/s^2")
for lab, a00 in [("SPARC   1.181e-10", A0_SPARC),
                 ("canonical 0.936e-10 (rho_DE/cH_Lambda)", A0_CANON),
                 ("alt     1.131e-10 (rho_tot/cH0)", A0_ALT)]:
    rr = np.percentile(a0BW/a00, [16,50,84])
    # what flat and DESI predict for a0(3.25)/a0(0) on this footing (both =track, footing-indep)
    print(f"    a0(3.25)/a0(0) vs {lab:38s} = {rr[1]:.2f} (+{rr[2]-rr[1]:.2f}/-{rr[1]-rr[0]:.2f})")
print(f"  cosmic predictions for a0(3.25)/a0(0):  flat = {a0_track(3.25,*FLAT):.2f},  "
      f"DESI-decl = {a0_track(3.25,*DESI):.2f},  alt-cH0 rise = {Ez(3.25):.2f}")
print("  -> on EVERY footing the Big Wheel ratio is CONSISTENT with constant (flat)")
print("     and with the DESI decline; it DISFAVORS the alt-cH0 ~5x RISE (~2 sigma,")
print("     banked P~1-3%). The declining vs flat choice stays undetermined.\n")

# --------------------------------------------------------------------------
# Q5  FORECAST  --  N rotators / precision to separate flat from decline at 3 sigma.
# --------------------------------------------------------------------------
print("="*78)
print("Q5  FORECAST: decisive (3sigma) separation of flat vs the 0.60-0.75 decline")
print("="*78)
sig_decl = -np.log10(0.70)    # 0.155 dex target signal at z~3
print(f"  target signal (flat - decline) at z~3: {sig_decl:.3f} dex  "
      f"(need sigma_mean = {sig_decl/3:.3f} dex for 3 sigma)")
for sper, lab in [(0.10, "SPARC-like clean deep-MOND, M_bar to 0.10 dex"),
                  (0.25, "realistic high-z per-object, M_bar systematics ~0.25 dex")]:
    N3 = np.ceil((3.0*sper/sig_decl)**2)
    print(f"    {lab}:  N ~ {N3:.0f} clean deep-MOND rotators per z~2-3 bin")
# also: precision needed for a FIXED sample size
for N in (10, 20, 40):
    sper_need = sig_decl/3.0*np.sqrt(N)
    print(f"    with N={N:2d} clean z~2-3 rotators: per-object BTFR precision "
          f"<= {sper_need:.3f} dex reaches 3 sigma")
print("  Feasibility: JWST/ALMA already deliver ~tens of z~2-3 gas-traced rotators;")
print("  ELT/HARMONI resolves individual OUTER (deep-MOND) rotation curves. A sample")
print("  of ~20-40 CLEAN deep-MOND z~2-3 disks (Big-Wheel-like), M_bar to ~0.1 dex,")
print("  reaches 3 sigma on the declining track -- the DECISIVE future test.\n")

print("="*78)
print("BOTTOM LINE:  S(all)=%.2f sigma  ->  %s" % (S_all, verdict))
print("  z=0 tie holds (~1 sigma, canonical footing); the predicted 0.70 decline is")
print("  NEITHER detected NOR excluded; every galaxy point sits <=~1.2 sigma from BOTH")
print("  the flat and the declining track. The framework's forced a0-tracks-rho_DE")
print("  bridge is currently UNTESTED-BY-UNDERPOWER, not passed and not failed.")
print("="*78)
print("EXIT 0")
