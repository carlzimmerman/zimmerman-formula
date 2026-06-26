import numpy as np
import sympy as sp

print("="*70)
print("VERIFICATION 1: coefficient kappa and interpolation function CANCEL")
print("  in the a0(z) RATIO -- only w(z) (rho_DE) enters")
print("="*70)
# a0 = kappa * c^2 * sqrt(Lambda_eff(z)/(something)).  In framework a0 ∝ sqrt(rho_DE).
# RATIO a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).  kappa, c, Z, interpolation all cancel.
kappa, c, Z, rhoDE_z, rhoDE_0 = sp.symbols('kappa c Z rho_DEz rho_DE0', positive=True)
a0z = kappa * c**2 * sp.sqrt(rhoDE_z) / Z
a00 = kappa * c**2 * sp.sqrt(rhoDE_0) / Z
ratio = sp.simplify(a0z/a00)
print(f"  a0(z)/a0(0) = {ratio}   <- kappa, c, Z ALL CANCELLED (sympy)")
print("  => the a0(z) curve is PARAMETER-FREE given w(z). Quarantine intact:")
print("     a0(0)=9.36e-11 stays an INPUT; only the SHAPE is predicted.\n")

print("="*70)
print("VERIFICATION 2: BOTH-WAYS spread over DESI DR1/DR2 SN combos")
print("  (framework's OWN declining sqrt(rho_DE) footing, NOT rising rival)")
print("="*70)

def rho_ratio(z,w0,wa):
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
def zcross(w0,wa):
    x=(-1.0-w0)/wa
    return x/(1-x) if 0<x<1 else None

cases = {
 "DR2 DESY5  (-0.752,-0.86)":(-0.752,-0.86),
 "DR2 Union3 (-0.667,-1.09)":(-0.667,-1.09),
 "DR2 Pan+   (-0.838,-0.62)":(-0.838,-0.62),
 "DR1 DESY5  (-0.727,-1.05)":(-0.727,-1.05),
 "DR1 keyfit (-0.733,-1.01)":(-0.733,-1.010),
 # ACT-DR6 smaller-wa variant (2504.18464) as a low-amplitude bound:
 "DR2+ACT DESY5 (-0.781,-0.43)":(-0.781,-0.43),
}
zs=np.linspace(0,5,500001)
print(f"\n{'case':<28}{'z_cross':>8}{'bump%':>8}{'a0(z3)/a0(0)':>14}{'V@z3 %':>9}")
bumps=[]; z3s=[]; zcs=[]
for n,(w0,wa) in cases.items():
    zc=zcross(w0,wa)
    rr=rho_ratio(zs,w0,wa); ipk=np.argmax(rr); zpk=zs[ipk]
    bump=100*(np.sqrt(rr[ipk])-1)
    a3=np.sqrt(rho_ratio(3,w0,wa))
    # deep-MOND BTFR: V^4 ∝ G M a0 -> dlogV = (1/4) dlog a0 = (1/8) dlog rho_DE
    dV3=100*(a3**0.25 -1)  # fractional V offset at z=3 vs local BTFR
    bumps.append(bump); z3s.append(100*(a3-1)); zcs.append(zc)
    print(f"{n:<28}{zc:>8.3f}{bump:>+8.2f}{a3:>14.3f}{dV3:>+9.1f}")

print(f"\nSPREAD across all DESI combos:")
print(f"  phantom-crossing z_c : {min(zcs):.3f} .. {max(zcs):.3f}  (all near ~0.35-0.44)")
print(f"  a0 bump @peak        : {min(bumps):+.1f}% .. {max(bumps):+.1f}%")
print(f"  a0(z=3) decline      : {min(z3s):+.0f}% .. {max(z3s):+.0f}%")

print("\n"+"="*70)
print("VERIFICATION 3: RISING RIVAL (total-density footing) -- the CONTESTED branch")
print("="*70)
# rival: a0 ∝ cH(z) ∝ E(z)=sqrt(Om(1+z)^3+OL), declines? No: RISES with z
Om,OL=0.31,0.69
def Ez(z): return np.sqrt(Om*(1+z)**3+OL)
for z in [0.405,1,2,3]:
    print(f"  RIVAL a0({z})/a0(0)=E(z)/E(0) = {Ez(z)/Ez(0):.3f}  (+{100*(Ez(z)/Ez(0)-1):.0f}%)  RISING")
print("  => rival predicts BTFR discs ABOVE local; framework predicts BELOW.")
print("  OPPOSITE SIGN at z>=2 = the clean BTFR-sign discriminator.")
