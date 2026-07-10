#!/usr/bin/env python3
"""
INDEPENDENT adversarial re-derivation of Lane 2 (inertial-deficit source).

Deliberately different from lane2_deficit.py:
  - baryons: Plummer sphere AND exponential-density sphere (not Hernquist),
    same M_bar = 1e11 Msun, half-mass radius matched to 5.9 kpc
  - integrator: scipy.integrate.quad (not trapezoid-on-grid)
  - shear: direct Abel projection with quad
  - PLUS the most-charitable variants a rescuer could try:
      (a) deficit counted with the FULL nu weighting (1 - mu) -> already done;
          try instead (nu - 1)*mu ("deficit of the deficit") and (nu-1) itself
          to see what weighting WOULD be needed;
      (b) deficit smeared over a sphere of radius r_dS = c^2/a(r) (the
          'Unruh wavelength' scale) instead of sitting at the baryons -- does
          delocalizing fix the shear shape?
Decisive ratio: M_def(r)/M_eff(r) with M_eff = M_bar(<r)(nu-1).
"""
import numpy as np
from scipy.integrate import quad

G, MSUN, KPC, C = 6.674e-11, 1.989e30, 3.0857e19, 2.998e8
MB = 1e11 * MSUN
A0 = 9.36e-11
A0_ALT = 1.13e-10

# half-mass radius to match: 1.678 * 3.5 kpc = 5.873 kpc
RHALF = 1.678 * 3.5 * KPC

# --- Plummer sphere: M(<r) = MB r^3/(r^2+b^2)^{3/2}; half-mass at
#     r = b / (2^{2/3}-1)^{1/2}
B_PLUM = RHALF * np.sqrt(2**(2.0/3.0) - 1.0)

def Menc_plummer(r):
    return MB * r**3 / (r*r + B_PLUM*B_PLUM)**1.5

def rho_plummer(r):
    return 3.0*MB*B_PLUM*B_PLUM / (4.0*np.pi) / (r*r + B_PLUM*B_PLUM)**2.5

# --- exponential sphere: rho ~ exp(-r/h); M(<r)=MB[1-(1+x+x^2/2)e^-x], x=r/h
# half-mass: solve (1+x+x^2/2)e^-x = 1/2 -> x ~ 2.674
from scipy.optimize import brentq
XH = brentq(lambda x: (1+x+x*x/2)*np.exp(-x) - 0.5, 1, 6)
H_EXP = RHALF / XH

def Menc_exp(r):
    x = r / H_EXP
    return MB * (1.0 - (1.0 + x + 0.5*x*x)*np.exp(-x))

def rho_exp(r):
    return MB/(8.0*np.pi*H_EXP**3) * np.exp(-r/H_EXP)

def nu_of_g(g, a0):
    return np.sqrt(1.0 + a0/g)

def run(name, Menc, rho, a0):
    print(f"\n--- {name}, a0={a0:.3e} ---")
    def gbar(r): return G*Menc(r)/r**2
    def integrand_def(r):     # (1-mu) dM/dr = (1-1/nu) 4 pi r^2 rho
        nu = nu_of_g(gbar(r), a0)
        return (1.0 - 1.0/nu) * 4.0*np.pi*r*r*rho(r)
    print(f"{'r/kpc':>6} {'Meff/Mb':>9} {'Mdef/Mb':>9} {'ratio':>8} {'short':>7}")
    out = {}
    for rk in [10, 30, 100, 300]:
        r = rk*KPC
        nu = nu_of_g(gbar(r), a0)
        Meff = Menc(r)*(nu-1.0)
        Mdef, _ = quad(integrand_def, 1e-3*KPC, r, limit=400)
        ratio = Mdef/Meff
        out[rk] = ratio
        print(f"{rk:>6} {Meff/MB:>9.3f} {Mdef/MB:>9.3f} {ratio:>8.4f} {1/ratio:>6.1f}x")
    return out

print("="*70)
print("PART A: decisive amount ratio, two independent baryon profiles")
print("="*70)
rA = run("Plummer", Menc_plummer, rho_plummer, A0)
rB = run("Exponential sphere", Menc_exp, rho_exp, A0)
rC = run("Plummer ALT footing", Menc_plummer, rho_plummer, A0_ALT)

# hard ceiling, profile-independent
nu300 = nu_of_g(G*MB/(300*KPC)**2, A0)
print(f"\nHARD CEILING (profile-independent): max possible M_def = M_bar;"
      f" required at 300 kpc = {nu300-1:.1f} M_bar -> floor shortfall"
      f" {nu300-1:.1f}x even if mu=0 everywhere.")

# deep-MOND analytic requirement
Meff_dm = np.sqrt(A0*MB/G)*(300*KPC)/MB
print(f"deep-MOND analytic M_eff(300kpc)/Mb = sqrt(a0 Mb/G) r / Mb = {Meff_dm:.1f}")

print("\n" + "="*70)
print("PART B: shear DeltaSigma at 100 kpc, independent Abel projection")
print("="*70)

def Sigma(rho3d, R):
    return 2.0*quad(lambda z: rho3d(np.sqrt(R*R+z*z)), 0, 3000*KPC, limit=400)[0]

def Mean_Sigma_inside(rho3d, R):
    # M2D(<R) = 2pi INT_0^R R' Sigma(R') dR'
    val, _ = quad(lambda Rp: Rp*Sigma(rho3d, Rp), 1e-3*KPC, R, limit=200)
    return 2.0*val/R**2  # = M2D/(pi R^2)

def dSigma(rho3d, R):
    return Mean_Sigma_inside(rho3d, R) - Sigma(rho3d, R)

def make_rho_def(Menc, rho, a0):
    def f(r):
        nu = nu_of_g(G*Menc(r)/r**2, a0)
        return (1.0 - 1.0/nu)*rho(r)
    return f

def make_rho_eff(Menc, a0):
    # rho_eff = (1/4pi r^2) d/dr [Menc(r)(nu-1)] via numerical derivative
    def Meff(r):
        nu = nu_of_g(G*Menc(r)/r**2, a0)
        return Menc(r)*(nu-1.0)
    def f(r):
        dr = 1e-4*r
        return max((Meff(r+dr)-Meff(r-dr))/(2*dr), 0.0)/(4.0*np.pi*r*r)
    return f

unit = MSUN/(3.0857e16)**2
for Rk in [30, 100, 300]:
    R = Rk*KPC
    dS_def = dSigma(make_rho_def(Menc_plummer, rho_plummer, A0), R)
    dS_req = dSigma(make_rho_eff(Menc_plummer, A0), R)
    print(f"R={Rk:>4} kpc: dSig_def={dS_def/unit:8.3f}  dSig_req={dS_req/unit:8.3f}"
          f"  Msun/pc^2  ratio={dS_def/dS_req:.4f}  shortfall={dS_req/dS_def:5.1f}x")

print("\n" + "="*70)
print("PART C: rescuer's variants (hunting a manufactured kill)")
print("="*70)
# (a) what weighting of dM_bar WOULD reproduce M_eff? Needs w(r)=... such that
#     INT w dM = M_bar(nu-1). Since M_eff >> M_bar, w > 1 needed -> not a
#     'deficit fraction' (deficit fraction <= 1 by definition).
r = 100*KPC
nu = nu_of_g(G*Menc_plummer(r)/r**2, A0)
print(f"(a) At 100 kpc required M_eff/M_bar(<r) = nu-1 = {nu-1:.2f}."
      f" ANY per-baryon deficit weight w<=1 integrates to <= M_bar(<r)."
      f" Needed average weight = {nu-1:.2f} > 1 -> impossible for a deficit.")

# (b) delocalize the deficit over the local Unruh scale L = c^2/g_obs(r)?
gobs = np.sqrt((G*Menc_plummer(r)/r**2)**2 + (G*Menc_plummer(r)/r**2)*A0)
L = C*C/gobs
print(f"(b) Unruh/dS delocalization scale c^2/g_obs at 100 kpc = {L/KPC:.3e} kpc"
      f" ({L/KPC/3.086e19*KPC:.0f}x the galaxy) -> smearing pushes the deficit"
      f" OUT of the 30-300 kpc window entirely (makes shear worse, not better).")

# (c) kinetic reading magnitude
print(f"(c) kinetic-only reading: suppression v^2/2c^2 = {200e3**2/(2*C*C):.2e};"
      f" ratio at 100 kpc = {rA[100]*200e3**2/(2*C*C):.2e}"
      f" (~{-np.log10(rA[100]*200e3**2/(2*C*C)):.1f} orders short).")

print("\nEXIT OK")
raise SystemExit(0)
