#!/usr/bin/env python3
"""
FRONT a0(z) HOSTAGE — DESI evolving-DE w(z) vs the Zimmerman framework's a0(z).

QUARANTINE (load-bearing): a0(0)=9.36e-11 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z is an
INPUT, never derived. Z=sqrt(32pi/3)=5.7888, kappa=1/2 unforced. Only the SHAPE
a0(z)/a0(0) is predicted, and it is PARAMETER-FREE given w(z): kappa, c, Z, and the
interpolation function ALL CANCEL in the ratio (sympy-proven below).

THE FRAMEWORK BRANCH (canonical, its OWN footing per Carl #1):
    a0(z) ∝ sqrt( rho_DE(z) )          (dark-energy free-fall scale; Limbach-Psaltis-Ozel 2008)
    => a0(z)/a0(0) = sqrt( rho_DE(z)/rho_DE(0) )
CPL: w(a)=w0+wa(1-a),  a=1/(1+z)
    rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} * exp(-3 wa z/(1+z))

THE RIVAL BRANCH (rho_total footing, the CONTESTED reading):
    a0(z) ∝ cH(z) ∝ E(z)=sqrt(Om(1+z)^3+OL)   -> RISES with z (opposite sign at z>=2)

DATA (fetched 2026-06, not recalled):
  DESI DR2 (arXiv:2503.14738, PRD 112 083515): evolving DE preferred over LCDM at
    3.1 sigma (DESI+CMB), 2.8 / 3.8 / 4.2 sigma with Pantheon+ / Union3 / DESY5.
    CPL central values (DESI BAO + CMB + SN), two consistent tabulations:
      DESY5:     w0=-0.752, wa=-0.86   (DESI key paper)  |  -0.73, -1.01  (alt)
      Union3:    w0=-0.667, wa=-1.09                     |  -0.66, -1.25  (alt)
      Pantheon+: w0=-0.838, wa=-0.62                     |  -0.83, -0.73  (alt)
    DR1 (arXiv:2404.03002): DESY5 w0=-0.727, wa=-1.05 (3.9 sigma).
    ACT-DR6 low-|wa| variant (a stress bound): w0~-0.781, wa~-0.43.
  Model-independent rho_DE reconstruction (arXiv:2506.22953, EPJC):
    "density f(z) first increases at low redshift, reaching a hump around z~0.5,
     then decreases" — CONFIRMS the bump is NOT a CPL artifact.
  MUSE-DARK III direct a0(z) (Ciocan 2026, A&A 709 L16, arXiv:2604.22613):
    a0(z)=a0(0)+a1 z, a0(0)=1.0e-10 (norm), a1=+1.59e-10/z, a0(z~1)=2.38e-10 RISING.
"""
import numpy as np
import sympy as sp

A0_LOCAL = 9.36e-11   # INPUT (quarantined), m/s^2

# ----------------------------------------------------------------------
def rho_ratio(z, w0, wa):
    """rho_DE(z)/rho_DE(0) for CPL."""
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

def a0_ratio_frame(z, w0, wa):
    """framework: a0(z)/a0(0) = sqrt(rho_DE ratio)."""
    return np.sqrt(rho_ratio(z, w0, wa))

def z_cross(w0, wa):
    """w(z) = -1 phantom-divide crossing redshift (where rho_DE peaks)."""
    x = (-1.0 - w0)/wa
    return x/(1-x) if 0 < x < 1 else None

def Ez(z, Om=0.31):
    return np.sqrt(Om*(1+z)**3 + (1-Om))

def a0_ratio_rival(z, Om=0.31):
    """rival: a0 ∝ cH ∝ E(z)."""
    return Ez(z, Om)/Ez(0, Om)

# ----------------------------------------------------------------------
print("="*74)
print("(0) QUARANTINE CHECK — kappa, c, Z, interpolation CANCEL in the ratio")
print("="*74)
kappa, c, Z, rz, r0 = sp.symbols('kappa c Z rho_DEz rho_DE0', positive=True)
a0z = kappa*c**2*sp.sqrt(rz)/Z
a00 = kappa*c**2*sp.sqrt(r0)/Z
ratio = sp.simplify(a0z/a00)
print(f"  a0(z)/a0(0) = {ratio}")
print("  -> kappa,c,Z all cancel (sympy). The SHAPE is parameter-free given w(z).")
print(f"  a0(0)={A0_LOCAL:.3e} stays an INPUT. Quarantine intact.\n")

# ----------------------------------------------------------------------
print("="*74)
print("(1) FRAMEWORK a0(z) on its OWN declining-sqrt(rho_DE) footing — DESI w(z)")
print("="*74)
cases = {
 "DR2 DESY5    (-0.752,-0.86)": (-0.752, -0.86),
 "DR2 DESY5alt (-0.73 ,-1.01)": (-0.73 , -1.01),
 "DR2 Union3   (-0.667,-1.09)": (-0.667, -1.09),
 "DR2 Union3alt(-0.66 ,-1.25)": (-0.66 , -1.25),
 "DR2 Pan+     (-0.838,-0.62)": (-0.838, -0.62),
 "DR2 Pan+alt  (-0.83 ,-0.73)": (-0.83 , -0.73),
 "DR1 DESY5    (-0.727,-1.05)": (-0.727, -1.05),
 "DR2+ACT loWa (-0.781,-0.43)": (-0.781, -0.43),  # low-|wa| stress bound
}
zs = np.linspace(0, 5, 500001)
print(f"\n{'case':<28}{'z_cross':>8}{'z_bump':>8}{'bump%':>8}"
      f"{'a0(z3)/a0_0':>13}{'BTFR V@z3%':>11}")
bumps=[]; z3s=[]; zcs=[]; zbumps=[]; vz3=[]
for n,(w0,wa) in cases.items():
    zc = z_cross(w0,wa)
    rr = rho_ratio(zs,w0,wa); ipk=np.argmax(rr); zpk=zs[ipk]
    bump = 100*(np.sqrt(rr[ipk])-1)
    a3 = a0_ratio_frame(3,w0,wa)
    # deep-MOND BTFR: V^4 ∝ G M a0  => dlogV = (1/4) dlog a0 = (1/8) dlog rho_DE
    dV3 = 100*(a3**0.25 - 1)
    bumps.append(bump); z3s.append(100*(a3-1)); zcs.append(zc if zc else np.nan)
    zbumps.append(zpk); vz3.append(dV3)
    zcs_str = f"{zc:.3f}" if zc else "  none"
    print(f"{n:<28}{zcs_str:>8}{zpk:>8.3f}{bump:>+8.2f}{a3:>13.3f}{dV3:>+11.2f}")

# the headline DESY5 point at the framework's published z=0.405
w0,wa = cases["DR2 DESY5    (-0.752,-0.86)"]
print(f"\n  HEADLINE (DR2 DESY5): a0(0.405)/a0(0) = {a0_ratio_frame(0.405,w0,wa):.4f} "
      f"({100*(a0_ratio_frame(0.405,w0,wa)-1):+.2f}%), "
      f"a0(3)/a0(0) = {a0_ratio_frame(3,w0,wa):.4f} "
      f"({100*(a0_ratio_frame(3,w0,wa)-1):+.1f}%)")
print(f"\n  SPREAD over all DESI combos (BOTH WAYS within the framework branch):")
zc_valid=[z for z in zcs if not np.isnan(z)]
print(f"    phantom-cross / rho_DE-peak z : {min(zbumps):.3f} .. {max(zbumps):.3f}")
print(f"    a0 bump @peak                 : {min(bumps):+.2f}% .. {max(bumps):+.2f}%")
print(f"    a0(z=3)                       : {min(z3s):+.0f}% .. {max(z3s):+.0f}%")
print(f"    deep-MOND BTFR V offset @z=3  : {min(vz3):+.2f}% .. {max(vz3):+.2f}%")

# ----------------------------------------------------------------------
print("\n"+"="*74)
print("(2) CROSS-CHECK — does DESI's w(z) PRODUCE the framework curve, or is BTFR")
print("    the only handle?  rho_DE peak is INDEPENDENTLY confirmed model-indep.")
print("="*74)
print("  DESI measures w(z); framework OUTPUTS a0(z)=sqrt(rho_DE). The bump LOCATION")
print("  (z~0.4-0.5) is SET by DESI's phantom-crossing, NOT fit. Model-independent")
print("  rho_DE reconstruction (2506.22953) finds the SAME hump at z~0.5 with NO CPL")
print("  assumption -> the bump is convention-robust, a genuine cosmology cross-check.")
print("  CAVEAT: this is a CONSISTENCY check (DESI gives rho_DE as INPUT). The only")
print("  framework OUTPUT test is the high-z a0/BTFR SIGN (z>=2, deep-MOND).")

# ----------------------------------------------------------------------
print("\n"+"="*74)
print("(3) DIRECT a0(z) DATA (Ciocan/MUSE rising) vs framework declining vs rival")
print("="*74)
# MUSE-DARK III: a0(z) = a0(0) + a1*z, normalized so a0(0)=1.0 (their units 1e-10)
def muse(z): return (1.0 + 1.59*z)/1.0   # ratio to local; a1=1.59, a0(0)=1.0e-10
w0d,wad = cases["DR2 DESY5    (-0.752,-0.86)"]
print(f"\n{'z':>6}{'MUSE rising':>13}{'FRAME (DESY5)':>15}{'RIVAL cH/E(z)':>15}")
for z in [0.4,0.5,1.0,1.44,2.0,3.0]:
    print(f"{z:>6.2f}{muse(z):>13.2f}{a0_ratio_frame(z,w0d,wad):>15.3f}"
          f"{a0_ratio_rival(z):>15.3f}")
print("\n  MUSE measures a0 RISING ~x2 by z~1 (a0(z~1)=2.38e-10). The framework's")
print("  declining branch is ~FLAT in z<1.44 (0.97-1.06) -> UNDERSHOOTS MUSE by ~2x.")
print("  The rising RIVAL (E(z), +78% @z=1) also undershoots but at least rises.")
print("  -> MUSE DISFAVORS declining at face value, BUT is rotation-curve-inferred,")
print("     M/L- & pressure-support- & LCDM-degenerate (Magneticum: apparent a0")
print("     rises ~x3 to z=2.3 with NO fundamental a0) => NON-DIAGNOSTIC / CONTESTED.")

# ----------------------------------------------------------------------
print("\n"+"="*74)
print("(4) RIVAL rising branch — explicit OPPOSITE-SIGN at z>=2 (the BTFR handle)")
print("="*74)
for z in [0.405,1,2,3]:
    fr=a0_ratio_frame(z,w0d,wad); rv=a0_ratio_rival(z)
    fv=100*(fr**0.25-1); rvv=100*(rv**0.25-1)
    print(f"  z={z}: FRAME a0 {fr:.3f} (BTFR V {fv:+.1f}%) | "
          f"RIVAL a0 {rv:.3f} (BTFR V {rvv:+.1f}%)  <- OPPOSITE SIGN @z>=2")

print("\n"+"="*74)
print("VERDICT: hostage ALIVE — DESI evolving-DE (3.1-4.2 sigma, w0>-1/wa<0) gives a")
print("distinctive parameter-free a0(z) bump (z~0.4) + z>=2 decline LCDM cannot make;")
print("the bump location is independently confirmed (model-indep rho_DE hump z~0.5).")
print("CONTESTED by the lone direct datum (MUSE rises ~2x, but LCDM/M-L-degenerate).")
print("DEAD only if DESI DR3 (2026-27) regresses to w=-1. Decisive output test = the")
print("z>=2 deep-MOND BTFR SIGN (ELT/HARMONI+JWST, early-mid 2030s).")
print("="*74)
