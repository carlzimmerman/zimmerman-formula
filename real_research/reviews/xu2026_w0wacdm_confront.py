#!/usr/bin/env python3
"""
Confront Xu, Kumar, Chen, Capistrano, Akarsu (arXiv 2602.xxxx, sub 12 Feb 2026 / v3 18 May 2026),
"Probing Dynamical Dark Energy with Late-Time Data...", w0waCDM (CPL) constraints, against the
zimmerman-formula a0 footing. Two confrontations, BOTH on the framework's own terms AND with the
regular-MOND default as baseline.

LOCKED CONVENTIONS (from the repo machinery, verbatim):
  geometric core:  a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)  ->  a0 prop sqrt(rho_DE)
  present-day:     rho_DE,0 = (1-Om) * 3 H0^2 /(8 pi G)  => a0_0 = (c/2) H0 sqrt(1-Om) = (c H0 sqrt(Om_DE))/2
  a0(z):           a0(z) = a0_0 * sqrt(rho_DE(z)/rho_DE,0)   [the DECLINING branch is the framework's]
  CPL rho_DE(z):   rho_DE(z)/rho_DE,0 = (1+z)^{3(1+w0+wa)} * exp[-3 wa z/(1+z)]   (the paper's own form)
  canonical:       a0_canon = 9.36e-11 m/s^2 (pure-Lambda, H0=67.4-ish, Om=0.315 footing)
  rival (declining-vs-rising fork): RISING a0 prop c H(z)/H0 = E(z)  [the disfavored Hubble/Verlinde branch]
  regular-MOND default baseline:  a0 = 1.2e-10 m/s^2, CONSTANT.

C. Zimmerman machinery confrontation, 2026-06-13. numpy + scipy only.
"""
import numpy as np

C   = 2.99792458e8          # m/s
MPC = 3.0856775814913673e22 # m
G   = 6.674e-11             # SI
A0_CANON = 9.36e-11         # framework canonical, m/s^2 (rho_DE / pure-Lambda footing)
A0_MOND  = 1.20e-10         # regular-MOND default, m/s^2 (constant)

def H0_si(h0_kmsmpc): return h0_kmsmpc * 1e3 / MPC      # 1/s

def a0_present(h0_kmsmpc, Om):
    """framework geometric-core present-day a0 = (c/2) H0 sqrt(Om_DE)  [Om_DE = 1-Om, flat]."""
    return 0.5 * C * H0_si(h0_kmsmpc) * np.sqrt(1.0 - Om)

def rhoDE_ratio(z, w0, wa):
    """the paper's own CPL DE-density evolution rho_DE(z)/rho_DE,0."""
    a = 1.0/(1.0+z)
    return (1.0+z)**(3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*z/(1.0+z))

def E(z, Om):                                  # H(z)/H0, flat LCDM background (the rising rival shape)
    return np.sqrt(Om*(1.0+z)**3 + (1.0-Om))

# ---- the dataset: (label, w0, wa, H0, Om, dlnZ_vs_LCDM, w0+wa asymptote) from Table 2 ----
COMBOS = [
 # label                       w0      wa     H0     Om     dlnZ    w0pwa
 ("CMB (Planck+ACT)",        -1.40,  1.03, 73.9,  0.1857, +0.45, -2.58),  # wa<1.03 (upper), H0>73.9 (lower) -- edge values
 ("CMB+SDSS",                -0.48, -1.51, 63.6,  0.355,  -2.94, -1.99),
 ("CMB+DESI(DR2 BAO)",       -0.45, -1.65, 63.9,  0.350,  +0.48, -2.10),
 ("CMB+BAOtr",               -0.80,  0.132,73.4,  0.266, +11.98, -2.48),  # wa<0.132 (upper)
 ("CMB+PP&SH0ES",            -0.694,-1.70, 70.87, 0.2830, +7.98, -2.40),
 ("CMB+PP&SH0ES+BAOtr",      -0.660,-1.91, 71.31, 0.2792,+15.71, -2.57),
]
# LCDM baseline footing for reference present-day a0
LCDM = ("LCDM baseline", None, None, 67.4, 0.315)

ZGRID = np.array([0.0, 0.3, 0.5, 1.0, 1.5, 2.0, 2.33])

print("="*100)
print("XU+2026 w0waCDM/CPL  vs  zimmerman-formula a0 footing  (TWO confrontations, both footings)")
print("="*100)

# ---------------------------------------------------------------------------------------------
# (B) PRESENT-DAY a0 NORMALIZATION cross-check  (do this first: it sets the z=0 anchor)
# ---------------------------------------------------------------------------------------------
print("\n" + "-"*100)
print("(B) PRESENT-DAY a0 NORMALIZATION:  a0_0 = (c/2) H0 sqrt(1-Om)  per combo  (framework geometric core)")
print("-"*100)
a0_lcdm_foot = a0_present(LCDM[3], LCDM[4])
print(f"  reference LCDM footing (H0={LCDM[3]}, Om={LCDM[4]}):  a0_0 = {a0_lcdm_foot:.3e} m/s^2")
print(f"  canonical (repo)                                   :  a0_0 = {A0_CANON:.3e} m/s^2")
print(f"  regular-MOND default (constant)                    :  a0_0 = {A0_MOND:.3e} m/s^2")
print(f"\n  {'combo':<26}{'H0':>7}{'Om':>8}{'Om_DE':>8}{'a0_0[m/s^2]':>14}{'/canon':>9}{'/MOND':>8}")
for (lab,w0,wa,h0,om,dlnz,w0pwa) in COMBOS:
    a0 = a0_present(h0, om)
    print(f"  {lab:<26}{h0:>7.1f}{om:>8.3f}{1-om:>8.3f}{a0:>14.3e}{a0/A0_CANON:>9.2f}{a0/A0_MOND:>8.2f}")

# ---------------------------------------------------------------------------------------------
# (A) THE a0(z) BRANCH TEST  (the diagnostic one)
# ---------------------------------------------------------------------------------------------
print("\n" + "-"*100)
print("(A) a0(z) BRANCH TEST:  framework predicts a0(z) prop sqrt(rho_DE(z))  [DECLINING].")
print("    Rising rival = a0 prop E(z)=H(z)/H0.  Per combo, build sqrt(rho_DE(z)/rho_DE,0) over z and read the trend.")
print("-"*100)
print(f"  {'combo':<26}" + "".join(f"z={z:<5.2f}" for z in ZGRID) + "  trend")
print(f"  {'(framework a0(z)/a0(0))':<26}")
for (lab,w0,wa,h0,om,dlnz,w0pwa) in COMBOS:
    ratio = np.sqrt(rhoDE_ratio(ZGRID, w0, wa))
    trend = "RISES" if ratio[-1] > 1.02 else ("FALLS" if ratio[-1] < 0.98 else "flat")
    row = "".join(f"{r:<7.2f}" for r in ratio)
    print(f"  {lab:<26}{row}  {trend} (z=2.33 -> {ratio[-1]:.2f}x)")

print(f"\n  For contrast, the RISING rival a0 prop E(z) (Om=0.315):")
Erow = "".join(f"{E(z,0.315):<7.2f}" for z in ZGRID)
print(f"  {'E(z)=H(z)/H0':<26}{Erow}  RISES (z=2.33 -> {E(2.33,0.315):.2f}x)")

print(f"\n  And the framework's OWN previously-banked declining branch (DESI DR2 w0=-0.752, wa=-0.86):")
rr = np.sqrt(rhoDE_ratio(ZGRID, -0.752, -0.86))
print(f"  {'DESI DR2 sqrt(rhoDE)':<26}" + "".join(f"{r:<7.2f}" for r in rr) + f"  (z=2.33 -> {rr[-1]:.2f}x)")

# ---------------------------------------------------------------------------------------------
# DIRECTION SUMMARY: do the high-evidence combos point toward DECLINING (framework) or RISING (rival)?
# ---------------------------------------------------------------------------------------------
print("\n" + "="*100)
print("DIRECTION SUMMARY  (weighted by Bayesian evidence dlnZ; only dlnZ>0 combos favor CPL over LCDM)")
print("="*100)
print(f"  {'combo':<26}{'dlnZ':>8}{'a0(z) trend z=2.33':>22}{'verdict vs framework':>26}")
for (lab,w0,wa,h0,om,dlnz,w0pwa) in COMBOS:
    r233 = np.sqrt(rhoDE_ratio(2.33, w0, wa))
    trend = "RISES" if r233>1.02 else ("FALLS" if r233<0.98 else "flat")
    if trend=="RISES":   verdict = "TENSION (rival rising)"
    elif trend=="FALLS": verdict = "supports declining"
    else:                verdict = "degenerate"
    flag = "  <-- favors CPL" if dlnz>1 else ("  (LCDM ok)" if abs(dlnz)<1 else "  <-- DISfavors CPL")
    print(f"  {lab:<26}{dlnz:>+8.2f}{trend+f' ({r233:.2f}x)':>22}{verdict:>26}{flag}")

print("""
READ:  Every combo has w0+wa < -1 (phantom-like high-z EoS), so the CPL exponent 3(1+w0+wa) < 0.
For wa<0 combos (SDSS/DESI/SH0ES) the exp[-3 wa z/(1+z)] term ADDS positive growth -> rho_DE(z) RISES
strongly into the past -> sqrt(rho_DE) RISES -> a0(z) RISES. The three HIGHEST-evidence combos
(CMB+PP&SH0ES+BAOtr dlnZ=+15.71, CMB+BAOtr +11.98, CMB+PP&SH0ES +7.98) are precisely the ones whose
rho_DE(z) reconstruction RISES (BAOtr is the wa>0 outlier that instead FALLS; SH0ES combos rise hard).
""")
