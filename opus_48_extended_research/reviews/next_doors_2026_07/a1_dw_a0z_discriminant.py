#!/usr/bin/env python3
"""
A1 prong 2 -- THE a0(z) DISCRIMINANT: Deffayet-Woodard (arXiv:2512.10513) background Z[g](z) on LCDM
vs the framework's a0(z) = cH_Lambda(z)/Z  (canonical declining-sqrt(rho_DE) fork AND rising cH*E(z) fork,
both shown per the footing rule).

DW machinery (their Appendix 7, eqs (48)-(52) arXiv numbering):
  -Z_bg = B(z)^2,  B(z) = (6 c H0 / a0) (1+z)^3 * Int_z^inf dz' [Om_r(1+z')^4 + (1/2)Om_m(1+z')^3 - Om_L]
                                                       / [ (1+z')^4 sqrt(Om_r(1+z')^4+Om_m(1+z')^3+Om_L) ]
  They state B has a zero-crossing at z ~= 0.0880 (citing Kim, Tan & Woodard 2016) -- reproduced below.
  Their a0 is a CONSTANT fixed by rho_0 = 45 a0^2/(16 pi G) ~= (5/6)(3/10) rho_crit  =>  a0 = c H0/sqrt(30).

Static systems superpose (leading order; cross term vanishes because the cosmological gradient of
chi = (1/box)(R_uu) is timelike and the galaxy's is spatial):
  Z_tot = (2 g_obs/a0)^2 - B(z)^2
so the MOND branch (Z>0) exists only ABOVE the acceleration floor  g_floor(z) = (a0/2) |B(z)|.
Their own sec. 4 wording assumes "space dependence dominates inside gravitationally bound systems" --
the floor quantifies exactly when that assumption holds.

Exits 0. All load-bearing numbers printed.
"""
import numpy as np
from scipy import integrate, optimize

c = 299792458.0
Mpc = 3.0856775814913673e22
H0_kms = 67.4
H0 = H0_kms*1e3/Mpc
cH0 = c*H0

# ---- their cosmology (paper values, eq (51)) ----
Om_r, Om_m, Om_L = 1e-4, 0.3, 0.7
a0_DW = cH0/np.sqrt(30.0)          # their eq (10) coincidence
Zfw   = np.sqrt(32*np.pi/3)        # framework Z
Om_L_fw = 0.685
a0_fw = cH0*np.sqrt(3*Om_L_fw/(32*np.pi))   # = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z

print("="*104)
print("CONSTANTS")
print("="*104)
print(f"  H0 = {H0_kms} km/s/Mpc ; cH0 = {cH0:.4e} m/s^2")
print(f"  DW   a0 = cH0/sqrt(30)            = {a0_DW:.4e} m/s^2   (their 'a0 ~= 1.2e-10'; STATIC, set at t=0)")
print(f"  FW   a0 = cH0 sqrt(3*Om_L/32pi)   = {a0_fw:.4e} m/s^2   (canonical 9.36e-11, Om_L={Om_L_fw})")
print(f"  ratio a0_DW/a0_fw = {a0_DW/a0_fw:.3f}")
chk = 6*np.sqrt(30)*np.sqrt(Om_r)
print(f"  their check '(6cH0/a0) sqrt(Om_r) ~= 1/3':  {chk:.4f}   [paper: ~=1/3]")
assert abs(chk - 1/3) < 0.01

# ---- B(z) via u = 1/(1+z') substitution: integrand smooth on (0, 1/(1+z)] ----
def integrand_u(u, Om_r=Om_r, Om_m=Om_m, Om_L=Om_L):
    return (Om_r + 0.5*Om_m*u - Om_L*u**4)/np.sqrt(Om_r + Om_m*u + Om_L*u**4)

def B(z, Om_r=Om_r, Om_m=Om_m, Om_L=Om_L):
    pref = 6*np.sqrt(30.0)   # 6 c H0 / a0_DW  (H0-independent by their a0 definition)
    I, _ = integrate.quad(integrand_u, 0.0, 1.0/(1.0+z), args=(Om_r, Om_m, Om_L), limit=400)
    return pref*(1+z)**3*I

print()
print("="*104)
print("VALIDATION: reproduce their z ~= 0.0880 zero-crossing (their Appendix 7, citing Kim et al 1608.07858)")
print("="*104)
# Kim, Rahat, Sayeb, Tan, Woodard & Xu (PRD 94, 104009, 2016) computed the crossing with Planck-2015
# cosmology (Om_m ~= 0.3089); the 2026 paper's ROUNDED Om_m=0.30 shifts it slightly. Both shown.
z_c_kim = optimize.brentq(lambda z: B(z, 1e-4, 0.3089, 1-1e-4-0.3089), 0.01, 0.4, xtol=1e-8)
print(f"  eq (52) with Planck-2015 Om_m=0.3089 (Kim et al's input):  z_c = {z_c_kim:.4f}   [paper: 0.0880]")
assert abs(z_c_kim - 0.088) < 0.002, "failed to reproduce their zero-crossing on Kim et al's cosmology"
z_c = optimize.brentq(B, 0.01, 0.4, xtol=1e-8)
print(f"  eq (52) with the 2026 paper's rounded (0.3, 0.7):          z_c = {z_c:.4f}")
z_c2 = optimize.brentq(lambda z: B(z, 9.2e-5, 0.315, 0.685), 0.01, 0.4, xtol=1e-8)
print(f"  with Planck-2018 (9.2e-5, 0.315, 0.685):                   z_c = {z_c2:.4f}")
print(f"  => implementation VALIDATED (0.0880 recovered on the cited paper's cosmology); the crossing is")
print(f"     robustly at z_c ~ 0.07-0.10, +-0.02 for Om_m in [0.30, 0.32]. Headline numbers below use the")
print(f"     2026 paper's own (0.3, 0.7); z_c-sensitive statements carry the band.")
# slope at crossing and high-z law
dz = 1e-4
Bp = (B(z_c+dz)-B(z_c-dz))/(2*dz)
print(f"  slope B'(z_c) = {Bp:.2f}  =>  local floor law g_floor ~= (a0/2)*{Bp:.1f}*|z - {z_c:.3f}|")
print(f"  high-z check: B(30)/[(6cH0/a0)sqrt(Om_r)(1+z)^2] = {B(30)/(chk*31**2):.3f}  (their (1+z)^2 sqrt(Om_r) law; ->1 only above z_eq~3000: {B(5000)/(chk*5001**2):.3f})")
# lookback time to z_c
E = lambda z: np.sqrt(Om_r*(1+z)**4 + Om_m*(1+z)**3 + Om_L)
t_lb, _ = integrate.quad(lambda z: 1.0/((1+z)*E(z)), 0, z_c)
print(f"  lookback time to z_c: {t_lb/H0/(3.156e16):.2f} Gyr  (the one moment DW is exactly floor-free)")

print()
print("="*104)
print("THE DW MOND-OFF FLOOR vs THE FRAMEWORK'S a0(z)  [the discriminant table]")
print("="*104)
# framework forks
def rho_DE_ratio(z, w0=-0.752, wa=-0.86):   # CPL, DESI-like (banked numbers)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
a0_fw_desi = lambda z: a0_fw*np.sqrt(rho_DE_ratio(z))       # canonical declining-sqrt(rho_DE) fork
a0_fw_rise = lambda z: a0_fw*E(z)                            # rising cH(z)E(z) fork (footing-bug contrast)
muse = lambda z: (1.0 + 1.59*z)*1e-10                        # MUSE-DARK III fitted law (Ciocan+ 2026)

zs = [0.0, 0.03, z_c, 0.15, 0.2, 0.3, 0.45, 0.673, 0.9, 1.1, 1.44, 2.0, 3.0]
hdr = f"{'z':>6} | {'B(z)':>8} | {'Z_bg':>9} | {'g_floor [m/s^2]':>15} | {'/a0_DW':>7} | {'/a0_fw':>7} | {'a0_fw canon':>11} | {'a0_fw DESI':>10} | {'a0_fw rise':>10} | {'MUSE fit':>9}"
print(hdr); print("-"*len(hdr))
for z in zs:
    b = B(z); fl = 0.5*a0_DW*abs(b)
    print(f"{z:>6.3f} | {b:>8.3f} | {-b*b:>9.3f} | {fl:>15.3e} | {fl/a0_DW:>7.3f} | {fl/a0_fw:>7.3f} | "
          f"{a0_fw:>11.3e} | {a0_fw_desi(z):>10.3e} | {a0_fw_rise(z):>10.3e} | {muse(z):>9.3e}")
B0 = B(0.0)
print(f"""
  STRUCTURE: DW's a0 is CONSTANT ({a0_DW:.3e}), but the MOND branch only exists above a z-dependent
  acceleration FLOOR that (i) is ~{0.5*abs(B0):.2f} a0_DW TODAY, (ii) vanishes exactly at z_c={z_c:.3f},
  (iii) then rises steeply ~ (1+z)^(3/2) (matter era). The framework has NO floor at any z and an a0(z)
  that is flat (w=-1) / varies by <~ +6%/-26% out to z=3 across the two footing forks. These are
  structurally different z-dependences -- the discriminant is REAL.""")

print("="*104)
print("CONFRONTATION 1 -- TODAY (z~=0): the SPARC deep-RAR vs DW's floor  [data fully in hand]")
print("="*104)
fl0 = 0.5*a0_DW*abs(B0)
gbar_floor = fl0**2/a0_DW   # deep-MOND mapping g_obs = sqrt(a0 g_bar)
print(f"  B(0) = {B0:.3f}  =>  Z_bg(0) = {-B0**2:.2f}  =>  g_floor(0) = {fl0:.3e} m/s^2 = {fl0/a0_DW:.2f} a0_DW")
print(f"  their own 'deep MOND' band is 0 < Z <~ 1, i.e. g_obs <= a0/2 = {a0_DW/2:.2e} -- the floor sits")
print(f"  {fl0/(a0_DW/2):.2f}x ABOVE the top of the deep-MOND band: on-branch, the ENTIRE deep-MOND regime is")
print(f"  background-drowned TODAY (|Z_bg(0)|={B0**2:.1f} > 1).")
print(f"  In g_bar: floor at g_bar ~= {gbar_floor:.2e} m/s^2; SPARC's clean MOND locus (framework nu, 0.108 dex)")
print(f"  extends to g_bar ~ 1e-12 => {np.log10(gbar_floor/1e-12):.1f} dex of the measured RAR lie BELOW the floor.")
print(f"  Also: f(Z) is NOT suppressed there: at Z_bg(0)={-B0**2:.2f}, exp(-sqrt|Z|/3) = {np.exp(-abs(B0)/3):.2f} --")
print(f"  the galaxy-outskirt regime today lands in the UNANALYZED Z<0, |Z|~O(1) corner of their f.")
print("""  => On the naive on-branch reading, DW predicts a deep-RAR breakdown TODAY that SPARC does not show.
     CAVEAT (both ways): below-floor phenomenology is governed by their M-transport memory (their eq (33)),
     which their own sec. 4.2 defers as a 'formidable numerical undertaking' -- this is a severe TENSION
     pending their transition analysis, not a completed kill. Their sec. 4 premise ('space dependence
     dominates inside gravitationally bound systems') quantitatively FAILS for g_obs < g_floor(0).""")

print("="*104)
print("CONFRONTATION 2 -- the z<0.1 SHARP structure: what data tests it")
print("="*104)
for z in (0.0, 0.02, 0.05, z_c, 0.12, 0.15):
    fl = 0.5*a0_DW*abs(B(z))
    print(f"    z={z:>5.3f}:  g_floor = {fl:.2e} m/s^2  ({fl/a0_DW:.3f} a0_DW)")
z_half = optimize.brentq(lambda z: abs(B(z))-1.0, z_c+1e-4, 1.0)     # floor = a0/2 (deep band gone)
z_full = optimize.brentq(lambda z: abs(B(z))-2.0, z_c+1e-4, 1.5)     # floor = a0
z_half_lo = optimize.brentq(lambda z: abs(B(z))-1.0, 0.0, z_c-1e-4) if abs(B0)>1 else np.nan
print(f"  deep-MOND band fully off-branch (floor >= a0/2): z >= {z_half:.3f}  (and z <= {z_half_lo:.3f} on the low side)")
print(f"  floor reaches a0 itself at z = {z_full:.3f}; MUSE's lowest bin (z=0.33) floor = {0.5*a0_DW*abs(B(0.33)):.2e} m/s^2")
print(f"""  SIGNATURE: an INVERTED low-z trend with a cusp -- deep-MOND quality is BEST at z~{z_c:.3f} and
  degrades toward BOTH z=0 and z>~0.15. Testable NOW: SPARC (z~=0) vs WALLABY DR2 z-bins (z<~0.09,
  the banked B2 corpus straddles the crossing) vs MIGHTEE-HI (z<~0.08). The framework predicts a FLAT
  deep-RAR across 0 < z < 0.15; DW-naive predicts the cusp pattern above. No other model on the table
  predicts MORE MOND at z=0.09 than at z=0.""")

print("="*104)
print("CONFRONTATION 3 -- the MUSE-DARK III window (0.33<z<1.44): can DW mimic the measured rise?")
print("="*104)
print(f"  MUSE fitted a0(z) = (1.0 +- 0.04) + (1.59 +0.11/-0.10) z  [x1e-10]; bins climb 1.99e-10 -> 2.71e-10")
for z in (0.33, 0.45, 0.9, 1.1, 1.44):
    fl = 0.5*a0_DW*abs(B(z))
    print(f"    z={z:>4.2f}:  DW floor = {fl:.2e} m/s^2 = {fl/1e-10:>6.2f} x1e-10  vs MUSE fitted a0 = {muse(z)/1e-10:.2f} x1e-10")
print(f"""  DW's floor EXCEEDS the entire measured acceleration scale across the whole MUSE window (by z=0.33
  the floor is already {0.5*a0_DW*abs(B(0.33))/muse(0.33):.1f}x the fitted a0; by z=1 it is {0.5*a0_DW*abs(B(1.0))/muse(1.0):.0f}x). On-branch MOND is
  entirely absent there: everything MUSE sees is, in DW-world, the CDM-MIMIC sector (their sec. 2 fluid),
  which is built to be indistinguishable from CDM => DW is LCDM-DEGENERATE at 0.33<z<1.44.
  BOTH-WAYS on Front B: (a) DW does NOT fit the MUSE rise with a rising fundamental a0 -- it hides behind
  the same LCDM-assembly degeneracy (Magneticum) that already makes MUSE non-diagnostic for the framework;
  no NEW loss of Front-B power at 0.33<z<1.44 (that power was already conceded to LCDM-degeneracy).
  (b) The framework-vs-DW separators live where DW is NOT degenerate: the z~=0 deep-RAR (Confrontation 1,
  data in hand, DW-naive severely stressed) and the z<0.15 cusp (Confrontation 2). Front B does NOT lose
  discriminating power against DW -- the discriminant just lives at LOW z, not in the MUSE window.""")

print("="*104)
print("SUMMARY NUMBERS")
print("="*104)
print(f"  z_c = {z_c:.4f} (paper 0.0880: reproduced); B(0) = {B0:.2f}; g_floor(0) = {fl0:.2e} m/s^2 = {fl0/a0_fw:.2f} a0_fw")
print(f"  floor kills deep-MOND band outside {z_half_lo:.3f} < z < {z_half:.3f}; floor(z=1) = {0.5*a0_DW*abs(B(1.0)):.1e} m/s^2 (~{0.5*abs(B(1.0)):.1f} a0_DW)")
print(f"  framework spread at z=1: canonical {a0_fw:.2e} (flat) | DESI fork {a0_fw_desi(1.0):.2e} ({100*(a0_fw_desi(1.0)/a0_fw-1):+.1f}%) | rising fork {a0_fw_rise(1.0):.2e} ({100*(a0_fw_rise(1.0)/a0_fw-1):+.0f}%)")
print(f"  MUSE at z=1: {muse(1.0):.2e} (+{100*(muse(1.0)/1e-10-1):.0f}% over its own z=0) -- rises faster than ANY fork (banked standing unchanged)")
print("EXIT 0")
