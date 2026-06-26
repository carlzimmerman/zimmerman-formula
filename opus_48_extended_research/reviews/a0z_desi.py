import numpy as np
from scipy.integrate import quad

# Framework: a0(z)/a0(0) = sqrt( rho_DE(z) / rho_DE(0) )
# CPL: w(a) = w0 + wa*(1-a), a=1/(1+z)
# rho_DE(z)/rho_DE(0) = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z))

def rho_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

def a0_ratio(z, w0, wa):
    return np.sqrt(rho_ratio(z, w0, wa))

# w(z) crossing -1 (phantom divide): w0 + wa*(1 - 1/(1+z)) = -1 -> z_cross
def z_cross(w0, wa):
    # w0 + wa*z/(1+z) = -1 -> z/(1+z) = (-1-w0)/wa -> x=(-1-w0)/wa ; z=x/(1-x)
    x = (-1.0 - w0)/wa
    if 0 < x < 1:
        return x/(1-x)
    return None

cases = {
 "DESI DR2 DESY5 (w0=-0.752,wa=-0.86)": (-0.752, -0.86),
 "DESI DR2 Union3 (w0=-0.667,wa=-1.09)": (-0.667, -1.09),
 "DESI DR2 Pantheon+ (w0=-0.838,wa=-0.62)": (-0.838, -0.62),
 "DESI DR1 DESY5 (w0=-0.727,wa=-1.05)": (-0.727, -1.05),
 "DESI DR1 best-fit (w0=-0.733,wa=-1.01)": (-0.733, -1.010),
}

for name,(w0,wa) in cases.items():
    zc = z_cross(w0,wa)
    # find z where rho_DE peaks: d/dz rho_ratio =0 . rho peaks where w=-1 (phantom->normal crossing from below)
    zs = np.linspace(0,5,200001)
    rr = rho_ratio(zs,w0,wa)
    ipk = np.argmax(rr)
    zpk = zs[ipk]; peak = rr[ipk]
    print(f"\n=== {name} ===")
    print(f"  w(z)=-1 phantom crossing at z = {zc}")
    print(f"  rho_DE peaks at z = {zpk:.3f}, rho_DE(peak)/rho_DE(0) = {peak:.4f}")
    print(f"  => a0 BUMP at peak: a0(z_pk)/a0(0) = {np.sqrt(peak):.4f}  ({100*(np.sqrt(peak)-1):+.2f}%)")
    for z in [0.405, 1, 2, 3, 5]:
        ar = a0_ratio(z,w0,wa)
        print(f"  a0({z})/a0(0) = {ar:.4f}  ({100*(ar-1):+.1f}%)")
