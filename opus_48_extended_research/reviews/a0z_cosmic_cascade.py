import numpy as np

# ============================================================
# a0(z) = c^2 sqrt(Lambda_eff(z)/32pi) = (c/2) sqrt(G rho_DE(z))
#   => a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) )
# Framework constants
c = 2.99792458e8
G = 6.674e-11
H0 = 67.4 * 1000 / 3.0857e22   # s^-1  (Planck-ish)
Om = 0.315
OL = 0.685
Or = 9.2e-5     # radiation today (photons+neutrinos)
a0_now = 9.36e-11  # framework canonical

# rho_DE(z)/rho_DE(0) for CPL w(a)=w0+wa(1-a):
def rho_de_ratio(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def a0_ratio(z, w0, wa):
    return np.sqrt(rho_de_ratio(z, w0, wa))

# matter and radiation densities relative to DE today
# rho_m(z)/rho_DE0 = (Om/OL)(1+z)^3 ; rho_r(z)/rho_DE0=(Or/OL)(1+z)^4

print("="*70)
print("PART A: a0 at recombination (z~1100) and BBN (z~3e8)")
print("="*70)

# Case 1: pure Lambda (w=-1): a0 CONSTANT at all z. trivial.
print("\n[w=-1 cosmological constant]: rho_DE const => a0(z)=a0(0) EXACTLY at ALL z.")
print(f"  a0(z_rec)=a0(z_BBN)=a0(0)= {a0_now:.3e} m/s^2  (NO early-universe a0 evolution)")

# Case 2: DESI CPL extrapolated. CPL is a LATE-TIME parametrization; extrapolating to
# z=1100 is formally divergent/unphysical but we compute the FORMAL number to show the issue.
print("\n[DESI DR2 DESY5 CPL w0=-0.752,wa=-0.86 — FORMAL extrapolation]:")
w0,wa=-0.752,-0.86
for z in [1100, 3.4e8]:
    r=rho_de_ratio(z,w0,wa)
    print(f"  z={z:.3g}: rho_DE(z)/rho_DE0 = {r:.4e}  => a0 ratio = {np.sqrt(r):.4e}")
# exponent 3(1+w0+wa)=
expo=3*(1+w0+wa)
print(f"  power-law index 3(1+w0+wa) = {expo:.3f}  (rho_DE ~ (1+z)^{expo:.2f} at high z)")
print(f"  exp term -> exp(-3*wa) = exp({-3*wa:.2f}) = {np.exp(-3*wa):.3f} (bounded const as z->inf)")

# So for DESI CPL, at high z rho_DE ~ (1+z)^-0.276 * const -> SLOWLY DECLINING (a0 shrinks)
