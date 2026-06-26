import sympy as sp
# Structural numbers the claim relies on
Z_target = sp.sqrt(32*sp.pi/3)
kernel   = sp.sqrt(8*sp.pi/3)
print("Z = sqrt(32 pi/3)      =", float(Z_target), " (claim says 5.789)")
print("kernel sqrt(8 pi/3)    =", float(kernel))
print("Z * kappa  at kappa=1/2:", float(Z_target*sp.Rational(1,2)),
      " vs kernel sqrt(8pi/3)=", float(kernel), " -> locked?", 
      sp.simplify(Z_target*sp.Rational(1,2) - kernel)==0)
# a0 numeric at kappa=1/2 (LOCATING only): a0 = c^2 sqrt(Lambda/32pi)
c = 299792458.0
# Lambda from rho_DE: use H0, OmegaLambda. Just confirm the 9.36e-11 ballpark via cH_Lambda/Z.
# cH_Lambda = c * H_Lambda, H_Lambda = sqrt(Lambda/3) c. a0 = cH_Lambda / Z.
# Use Planck-ish: H0=67.4 km/s/Mpc, OmegaL=0.685 -> H_Lambda = H0 sqrt(OmegaL).
import math
H0 = 67.4*1000/(3.0857e22)           # s^-1
HL = H0*math.sqrt(0.685)
cHL = c*HL
a0 = cHL/float(Z_target)
print("\ncH_Lambda =", cHL, " m/s^2")
print("a0 = cH_Lambda / Z =", a0, " m/s^2  (claim/framework: 9.36e-11) -- LOCATING only")
print(">>> ratio a0/cH_Lambda = 1/Z =", 1/float(Z_target), " = 0.1727 (matches prior verdict)")
