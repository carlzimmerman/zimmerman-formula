"""
Framework a0(z) on its OWN footing: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)).
Coefficient (c^2 sqrt(Lambda/32pi)) and the interpolation function CANCEL in the
ratio -- only w(z) [via rho_DE(z)] enters. This is the published-paper branch.

We pin:
  (1) the +6% phantom-divide bump location & size,
  (2) the -26% (z=3) decline,
  (3) the BTFR V-offset dlogV = (1/8) dlog rho_DE  -> -7.3% at z=3,
under DESI DR2 CPL (DESY5) w0,wa -- the framework's OWN declining branch.
Then we run it BOTH WAYS vs the rival rising branch (rho_total / cH(z) ~ E(z)).
"""
import numpy as np
from scipy.integrate import quad

# ---- CPL dark-energy density evolution ----
# rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))
def rho_DE_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

def a0_ratio(z, w0, wa):
    return np.sqrt(rho_DE_ratio(z, w0, wa))

# w(z) CPL
def w_of_z(z, w0, wa):
    return w0 + wa*z/(1+z)

# phantom-divide crossing: w(z)= -1  =>  w0 + wa z/(1+z) = -1
def phantom_cross(w0, wa):
    # solve w0 + wa*z/(1+z) = -1  -> z/(1+z) = (-1-w0)/wa
    if wa == 0:
        return None
    r = (-1 - w0)/wa
    if not (0 < r < 1):
        return None
    return r/(1-r)

# ---- DESI DR2 (2025) CPL central values across SN datasets ----
# These are the headline DESI DR2 BAO + CMB + SN combos.
datasets = {
    "DESI DR2 + CMB + DESY5":      dict(w0=-0.752, wa=-0.86),
    "DESI DR2 + CMB + Pantheon+":  dict(w0=-0.838, wa=-0.62),
    "DESI DR2 + CMB + Union3":     dict(w0=-0.667, wa=-1.09),
    "DESI DR1 + CMB + DESY5 (2024)":dict(w0=-0.727, wa=-1.05),
    "LCDM (w=-1, null)":           dict(w0=-1.0,   wa=0.0),
}

zgrid = [0.0, 0.2, 0.405, 0.5, 1.0, 2.0, 3.0, 5.0]

print("="*92)
print("FRAMEWORK a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)  -- DECLINING branch (paper)")
print("="*92)
for name, p in datasets.items():
    w0, wa = p['w0'], p['wa']
    zc = phantom_cross(w0, wa)
    # find the actual peak of a0_ratio numerically
    zz = np.linspace(0, 1.5, 30001)
    rr = a0_ratio(zz, w0, wa)
    ipk = int(np.argmax(rr))
    zpeak, rpeak = zz[ipk], rr[ipk]
    print(f"\n{name}:  w0={w0:+.3f}, wa={wa:+.3f}")
    print(f"   phantom-divide w=-1 at z = {zc if zc else 'n/a':}")
    if zc:
        print(f"   a0 ratio PEAK numerically at z={zpeak:.3f}, ratio={rpeak:.4f}  (bump = {(rpeak-1)*100:+.2f}%)")
    row = "   z:    " + "".join(f"{z:>8.3f}" for z in zgrid)
    print(row)
    print("   a0/a0:" + "".join(f"{a0_ratio(z,w0,wa):>8.4f}" for z in zgrid))
    print("   w(z): " + "".join(f"{w_of_z(z,w0,wa):>8.3f}" for z in zgrid))

# ---- BTFR V-offset:  V^4 ~ G M a0  =>  dlogV = (1/4) dlog a0 = (1/8) dlog rho_DE ----
print("\n" + "="*92)
print("BTFR V-offset (deep-MOND): dlogV = (1/4) dlog a0 = (1/8) dlog rho_DE")
print("="*92)
for name, p in [("DESY5", datasets["DESI DR2 + CMB + DESY5"])]:
    w0, wa = p['w0'], p['wa']
    for z in [1.0, 2.0, 3.0]:
        da0 = a0_ratio(z, w0, wa)
        dlogV = 0.25*np.log10(da0)         # dex offset in logV
        dV_frac = 10**(dlogV) - 1
        print(f"   z={z}: a0/a0(0)={da0:.4f}  -> dlogV={dlogV:+.4f} dex  -> dV={dV_frac*100:+.2f}% (vs local BTFR)")

# ---- RIVAL rising branch: a0 ~ cH(z) ~ E(z) = sqrt(Om(1+z)^3 + OL) [rho_total footing] ----
print("\n" + "="*92)
print("RIVAL rising branch (BOTH-WAYS): a0 ~ cH(z) ~ E(z) [rho_total / Verlinde-QI]")
print("="*92)
Om, OL = 0.315, 0.685
def Ez(z): return np.sqrt(Om*(1+z)**3 + OL)
print("   z:        " + "".join(f"{z:>8.3f}" for z in zgrid))
print("   E(z):     " + "".join(f"{Ez(z):>8.4f}" for z in zgrid))
# Verlinde a0 ~ (1+z)^{3/2} in matter era (Milgrom 2017 exclusion form)
print("   (1+z)^1.5:" + "".join(f"{(1+z)**1.5:>8.4f}" for z in zgrid))

# ---- MUSE-DARK III (Ciocan 2026) linear fit a0(z)=a0(0)+a1 z ----
print("\n" + "="*92)
print("MUSE-DARK III (Ciocan 2026) measured: a0(z)=1.0 + 1.59 z  [x1e-10], RAW")
print("="*92)
a0_muse = lambda z: 1.0 + 1.59*z
print("   z:        " + "".join(f"{z:>8.3f}" for z in zgrid))
print("   a0_muse:  " + "".join(f"{a0_muse(z):>8.3f}" for z in zgrid))
print("   (ratio):  " + "".join(f"{a0_muse(z)/1.0:>8.3f}" for z in zgrid))
print("\nDirection check at z=1: framework(DESY5)={:.3f}, rival E(z)={:.3f}, MUSE-raw={:.3f}".format(
    a0_ratio(1.0,-0.752,-0.86), Ez(1.0), a0_muse(1.0)))
