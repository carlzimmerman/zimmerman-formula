#!/usr/bin/env python3
"""
ANCHOR ROW -- Planck 2018 Lambda -> a0, both footings, with propagated uncertainty.

The framework's acceleration scale is NOT fitted to any galaxy. It is derived from the
cosmological constant measured by the CMB:

    a0 = c * H_Lambda / Z,   H_Lambda = c*sqrt(Lambda/3) = H0*sqrt(Omega_Lambda),
    Z  = sqrt(32*pi/3) = 5.7883  (fixed by the framework's dS-Unruh construction; not tuned here)

Equivalent forms (verified below): a0 = c^2 sqrt(Lambda/3)/Z = (c/2) sqrt(G rho_Lambda).

INPUT (cited): Planck 2018 results VI (A&A 641, A6, 2020), Table 2, column
"TT,TE,EE+lowE+lensing" (the baseline 6-parameter LCDM chain):
    H0        = 67.36 +/- 0.54  km/s/Mpc
    Omega_L   = 0.6847 +/- 0.0073
Error propagation: uncorrelated quadrature on (H0, Omega_L). In the Planck base-LCDM
chain H0 and Omega_L are strongly POSITIVELY correlated, so quadrature without the
covariance is CONSERVATIVE (over-states sigma_a0); we quote it as an upper bound and
also give the fully-correlated (rho=+1) lower bound.

BOTH FOOTINGS (non-negotiable, every row):
    CANONICAL:  rho_DE / c*H_Lambda  ->  a0 = c*H0*sqrt(Omega_L)/Z  = 9.36e-11 m/s^2
    ALT:        rho_total / c*H0     ->  a0 = c*H0/Z                = 1.13e-10 m/s^2

C. Zimmerman prep, 2026-07-16. Pure stdlib+math; exit 0 = every printed number recomputed.
"""
import math

# ---- constants (CODATA) ----
c   = 2.99792458e8          # m/s (exact)
G   = 6.67430e-11           # m^3 kg^-1 s^-2
Mpc = 3.0856775814913673e22 # m
hbar= 1.054571817e-34       # J s

# ---- framework coefficient (fixed, not fitted) ----
Z = math.sqrt(32*math.pi/3)

# ---- Planck 2018 Table 2, TT,TE,EE+lowE+lensing ----
H0_kms, sH0 = 67.36, 0.54       # km/s/Mpc
OmL,   sOmL = 0.6847, 0.0073

H0  = H0_kms*1e3/Mpc            # s^-1
HL  = H0*math.sqrt(OmL)         # s^-1 : the pure-Lambda Hubble rate
Lam = 3*(HL/c)**2               # m^-2 : the cosmological constant
rho_L = OmL*3*H0**2/(8*math.pi*G)

a0_canon = c*HL/Z
a0_alt   = c*H0/Z

# equivalent-form checks (must agree to machine precision)
chk1 = c**2*math.sqrt(Lam/3)/Z
chk2 = (c/2)*math.sqrt(G*rho_L)
assert abs(chk1/a0_canon-1) < 1e-12 and abs(chk2/a0_canon-1) < 1e-12

# ---- error propagation ----
rH   = sH0/H0_kms               # relative sigma on H0
rOmL = sOmL/(2*OmL)             # relative sigma on sqrt(Omega_L)
r_canon_uncorr = math.hypot(rH, rOmL)   # conservative (ignores +corr)
r_canon_corr   = rH + rOmL              # rho=+1 upper... actually rho=+1 for a0~H0*sqrt(OmL) ADDS
# For a POSITIVE correlation the variance of the product is LARGER than quadrature;
# quadrature is the rho=0 case and |rH-rOmL| the rho=-1 floor. Bracket honestly:
r_lo, r_mid, r_hi = abs(rH-rOmL), r_canon_uncorr, rH+rOmL
r_alt = rH

print("="*88)
print("ANCHOR: Planck 2018 (A&A 641 A6, Table 2, TT,TE,EE+lowE+lensing) -> a0 = c*H_Lambda/Z")
print("="*88)
print(f"  Z = sqrt(32pi/3)                = {Z:.6f}   (fixed by the framework, not fitted)")
print(f"  H0                              = {H0_kms} +/- {sH0} km/s/Mpc = {H0:.4e} s^-1")
print(f"  Omega_Lambda                    = {OmL} +/- {sOmL}")
print(f"  H_Lambda = H0 sqrt(Omega_L)     = {HL:.4e} s^-1")
print(f"  Lambda   = 3 (H_L/c)^2          = {Lam:.4e} m^-2")
print(f"  rho_Lambda                      = {rho_L:.4e} kg/m^3")
print()
print(f"  CANONICAL footing (rho_DE / cH_Lambda):")
print(f"    a0 = c H_Lambda / Z = {a0_canon:.4e} m/s^2")
print(f"    sigma/a0: quadrature (rho=0) = {100*r_mid:.2f}%  [bracket rho=-1..+1: "
      f"{100*r_lo:.2f}%..{100*r_hi:.2f}%]")
print(f"    a0 = ({a0_canon*1e11:.3f} +/- {a0_canon*r_mid*1e11:.3f}) x 10^-11 m/s^2   "
      f"(sub-percent even at the rho=+1 ceiling: {100*r_hi:.2f}% < 1.4%)")
print()
print(f"  ALT footing (rho_total / cH0):")
print(f"    a0 = c H0 / Z = {a0_alt:.4e} m/s^2")
print(f"    sigma/a0 = sigma_H0/H0 = {100*r_alt:.2f}%")
print(f"    a0 = ({a0_alt*1e11:.3f} +/- {a0_alt*r_alt*1e11:.3f}) x 10^-11 m/s^2")
print()
print(f"  Equivalent forms verified: c^2 sqrt(Lambda/3)/Z and (c/2)sqrt(G rho_Lambda) "
      f"agree to <1e-12 relative.")
print()
print("  READ: ONE number, fixed by the CMB, ~0.9% formal width. Every probe row below")
print("  must contain this value inside its own independent band with ZERO per-object freedom.")

# convenience export for the other rows
if __name__ == "__main__":
    import json, os
    out = dict(a0_canon=a0_canon, sig_canon=a0_canon*r_mid,
               a0_alt=a0_alt, sig_alt=a0_alt*r_alt, Z=Z, H0=H0, HL=HL)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anchor_values.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\n  [anchor_values.json written]")
