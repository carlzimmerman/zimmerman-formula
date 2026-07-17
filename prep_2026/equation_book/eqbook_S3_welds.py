#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M1, SEAM S3: cosmological welds of the framework premise
    a0 = c H_Lambda / Z,   H_Lambda = c sqrt(Lambda/3),   Z = sqrt(32 pi / 3)

CREDIT/HONESTY: the a0 ~ cH0 and a0 ~ c sqrt(Lambda/3) COINCIDENCES are Milgrom's
(1983; 1999). What the framework adds is a definite COEFFICIENT (1/Z) and a definite
FOOTING (pure-Lambda H_Lambda = H0 sqrt(Omega_Lambda)); the welds below are exact
consequences of THAT premise, and the novel content is the closed consistency
polygon + the estimator chains, not the coincidence itself. a0's VALUE is
POSTULATED (kappa-closure memory: one-parameter EFT) -- these are consistency
relations of the postulate, never a derivation of it. Both footings run.

  E-S3.1  Lambda weld:      Lambda = 3 Z^2 a0^2 / c^4                       [EXACT premise inversion]
  E-S3.2  Triangle weld:    H0 sqrt(Omega_Lambda) = Z a0 / c                [EXACT]
  E-S3.3  Pythagorean form (flat FRW): H0^2 = (Z a0/c)^2 + (8 pi G/3) rho_m0
          -> an H0 PREDICTION from {galactic a0} + {CMB physical density omega_m},
          with NO distance ladder if a0 comes from the distance-free pair
          estimator (E-S8.1)                                                [EXACT given flatness]
  E-S3.4  Hubble-tension map: the weld converts H0-tension into a0-tension:
          a0(H0) = c H0 sqrt(Omega_Lambda)/Z -- Planck vs SH0ES numbers      [EXACT]
  E-S3.5  Memory-time weld:  tau_mem = 2c/a0 = 2Z/(H0 sqrt(Omega_Lambda))    [EXACT]
  E-S3.6  a0(z) CPL bump closed form (DECLINING footing a0 propto sqrt(rho_DE)):
          z_peak = -(1+w0)/(1+w0+wa)  and the exact peak amplitude
          a0(z_pk)/a0(0) = [ (wa/(1+w0+wa))^{3(1+w0+wa)} e^{3(1+w0)} ]^{1/2}  [EXACT given CPL]
          RISING footing a0 propto c H(z) E(z)-type: monotonic, NO peak -- both shown.
"""
import sympy as sp
import numpy as np

ok = 0
def check(name, cond):
    global ok
    assert cond, "FAILED: " + name
    ok += 1
    print("[OK %2d] %s" % (ok, name))

c, a0, Z, Lam, H0, OmL, Omm, G, rho_m = sp.symbols(
    "c a0 Z Lambda H0 Omega_L Omega_m G rho_m", positive=True)
w0, wa = sp.symbols("w0 wa", real=True)      # DE params are NEGATIVE in practice
z = sp.symbols("z", real=True)

Zval = sp.sqrt(32*sp.pi/3)

# ---------------------------------------------------------------- E-S3.1
premise = sp.Eq(a0, c**2*sp.sqrt(Lam/3)/Z)
Lam_sol = sp.solve(premise, Lam)[0]
check("E-S3.1 Lambda = 3 Z^2 a0^2 / c^4", sp.simplify(Lam_sol - 3*Z**2*a0**2/c**4) == 0)

# ---------------------------------------------------------------- E-S3.2
# H_Lambda^2 = Lambda c^2/3 = H0^2 Omega_Lambda  (definition of Omega_Lambda)
HLam = sp.sqrt(Lam*c**2/3)
weld = sp.Eq(H0*sp.sqrt(OmL), Z*a0/c)
check("E-S3.2 H0 sqrt(Omega_L) = Z a0/c follows from premise + Omega_L def",
      sp.simplify(HLam.subs(Lam, Lam_sol) - Z*a0/c) == 0)

# ---------------------------------------------------------------- E-S3.3
# flat FRW: H0^2 = H0^2 Omega_m + H0^2 Omega_L (late-time, radiation negligible)
# H0^2 Omega_m = (8 pi G/3) rho_m0 (definition)
H0sq = (Z*a0/c)**2 + sp.Rational(8, 3)*sp.pi*G*rho_m
check("E-S3.3 Pythagorean weld H0^2 = (Z a0/c)^2 + (8piG/3) rho_m0 (flatness)",
      sp.simplify(H0sq - (H0**2*OmL + H0**2*Omm)
                  .subs(OmL, (Z*a0/(c*H0))**2)
                  .subs(Omm, sp.Rational(8, 3)*sp.pi*G*rho_m/H0**2)) == 0)

# numbers, both footings + inverse direction (a0 -> H0 given omega_m)
print("\n--- E-S3.3/E-S3.4 NUMBERS ---")
cv = 2.99792458e8
Zv = float(Zval)
KMSMPC = 1.0e3/3.0856775814913673e22          # km/s/Mpc -> 1/s
h100 = 100*KMSMPC
om_m_planck = 0.1430                           # Planck omega_m = Omega_m h^2 (physical)
for tag, a0v in [("canonical 9.36e-11", 9.36e-11), ("alternate 1.13e-10", 1.13e-10)]:
    HL = Zv*a0v/cv                             # = H0 sqrt(Omega_L)
    H0v = np.sqrt(HL**2 + om_m_planck*h100**2)  # Pythagorean weld
    OmLv = HL**2/H0v**2
    print("  %s: H_Lambda=%.4e /s -> with omega_m=%.4f: H0 = %.2f km/s/Mpc, "
          "Omega_L = %.4f" % (tag, HL, om_m_planck, H0v/KMSMPC, OmLv))
# Hubble-tension map: a0 implied by Planck vs SH0ES (Omega_L=0.685 fixed)
for tag, H0k in [("Planck  67.4", 67.4), ("SH0ES   73.0", 73.0)]:
    a0imp = cv*H0k*KMSMPC*np.sqrt(0.685)/Zv
    print("  E-S3.4 %s km/s/Mpc -> a0 = %.4e m/s^2" % (tag, a0imp))
print("  => the weld maps the 8.3%% Hubble tension onto an 8.3%% a0 split;")
print("     a distance-free galactic a0 at few-%% precision ARBITRATES it (see E-S8.1).")
check("E-S3.4 Planck H0 + Omega_L=0.685 reproduces the canonical footing to <1%",
      abs(cv*67.4*KMSMPC*np.sqrt(0.685)/Zv/9.36e-11 - 1) < 0.01)

# ---------------------------------------------------------------- E-S3.5
tau = 2*c/a0
check("E-S3.5 tau_mem = 2c/a0 = 2Z/(H0 sqrt(Omega_L))",
      sp.simplify(tau.subs(a0, c*H0*sp.sqrt(OmL)/Z) - 2*Z/(H0*sp.sqrt(OmL))) == 0)
tau_v = 2*cv/9.36e-11/(3.15576e16)  # Gyr
print("\n  E-S3.5 tau_mem = %.1f Gyr (canonical), = 2Z/sqrt(Omega_L) Hubble times = %.2f/H0"
      % (tau_v, 2*Zv/np.sqrt(0.685)))

# ---------------------------------------------------------------- E-S3.6 CPL bump
# DECLINING footing: a0(z)^2 propto rho_DE(z); CPL w(z) = w0 + wa z/(1+z)
rho_DE = (1 + z)**(3*(1 + w0 + wa))*sp.exp(-3*wa*z/(1 + z))
dlnrho = sp.simplify(sp.diff(sp.log(rho_DE), z))
zpk = sp.solve(dlnrho, z)
zpk = sp.simplify(zpk[0])
zpk_claimed = -(1 + w0)/(1 + w0 + wa)
check("E-S3.6 CPL peak z_pk = -(1+w0)/(1+w0+wa)",
      sp.simplify(zpk - zpk_claimed) == 0)
amp2 = sp.simplify(rho_DE.subs(z, zpk_claimed))   # rho ratio at peak
amp2_claimed = (wa/(1 + w0 + wa))**(3*(1 + w0 + wa))*sp.exp(3*(1 + w0))
check("E-S3.6b exact peak amplitude rho_pk/rho_0 = (wa/(1+w0+wa))^{3(1+w0+wa)} e^{3(1+w0)}",
      sp.simplify(sp.log(amp2) - sp.log(amp2_claimed)) == 0)
# DESI DR2 CPL numbers (w0 = -0.75, wa = -0.86 class)
w0v, wav = -0.75, -0.86
zp = -(1 + w0v)/(1 + w0v + wav)
ampl = ((wav/(1 + w0v + wav))**(3*(1 + w0v + wav))*np.exp(3*(1 + w0v)))**0.5
print("  E-S3.6 DESI-class (w0=%.2f, wa=%.2f): a0 peaks at z_pk = %.3f, "
      "a0(z_pk)/a0(0) = %.4f (a %.1f%% bump)" % (w0v, wav, zp, ampl, 100*(ampl-1)))
check("E-S3.6c peak exists only if -(1+w0) and (1+w0+wa) share sign (z_pk>0); DESI-class does",
      zp > 0)
# RISING footing: a0 propto H(z) => monotonic in z for w>-1 matter+DE; show no interior peak
Ez2 = 0.3*(1 + z)**3 + 0.7   # LCDM-like E(z)^2
dE = sp.diff(sp.sqrt(Ez2), z)
check("E-S3.6d RISING footing a0 propto H(z): dH/dz > 0 for all z>=0 -- NO bump "
      "(the bump is a DECLINING-footing-only signature)",
      all(not (s.is_real and s > 0) for s in sp.solve(sp.Eq(dE, 0), z)))

print("\nALL %d CHECKS PASSED -- exit 0" % ok)
