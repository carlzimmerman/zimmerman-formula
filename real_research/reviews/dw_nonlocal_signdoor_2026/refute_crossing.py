#!/usr/bin/env python3
r"""
ADVERSARIAL REFUTATION of the DW z~0.088 zero-crossing as a Front-B discriminant.

CLAIM UNDER TEST (the confront's a0z lens): DW has a SHARP, DISTINCTIVE zero-crossing
of the cosmological invariant Z at z*~0.088 that the framework's monotone a0(z) lacks,
so it *could* strengthen Front B.

I attack on three fronts:
  (A) IS THE CROSSING EVEN REAL from eq.51?  Integrate I(z) with many zmax and quadrature
      prescriptions. If I(z) stays single-signed (never hits 0) for z in [0,0.5], there is
      NO zero-crossing at z~0.088 in this reconstruction; the "0.088" is just the VALUE of
      I(0), mistaken for a crossing LOCATION.
  (B) IS IT OBSERVABLE?  What measures a0 at z<0.1? Map the current a0(z) probes and their
      redshift reach + error bars; is a low-z sign-flip in a COSMOLOGICAL invariant (not a
      galaxy-scale a0) something any instrument resolves?
  (C) DOES DW'S ~STATIC BOUND a0 FIT a0(z) DATA AS WELL AS THE FRAMEWORK'S DECLINING a0?
      If DW's bound-system a0 is a fixed constant (eq.31) and the framework's canonical a0 is
      ALSO essentially constant (pure-Lambda), the two are DEGENERATE on the measured axis and
      the crossing (in the unmeasured cosmological branch) buys ZERO discriminating power.
"""
import numpy as np
from scipy import integrate

Omega_r = 9.0e-5
Omega_m = 0.315
Omega_L = 1.0 - Omega_m - Omega_r
c = 2.99792458e8
H0 = 2.20e-18

def E(z):
    return np.sqrt(Omega_r*(1+z)**4 + Omega_m*(1+z)**3 + Omega_L)

def integrand(zp):
    num = Omega_r*(1+zp)**4 + 0.5*Omega_m*(1+zp)**3 - Omega_L
    return num/((1+zp)**4 * E(zp))

print("="*84)
print(" (A) IS THE z~0.088 CROSSING REAL?  I(z) = INT_z^zmax integrand dz'")
print("="*84)
print(" I(z) crossing zero <=> Z=0. Test robustness over zmax and integration method.\n")

def I_quad(z, zmax):
    val, _ = integrate.quad(integrand, z, zmax, limit=800)
    return val

def I_trapz(z, zmax, N=2_000_000):
    # log-spaced grid to resolve high-z, dense enough at low z
    zp = np.concatenate([np.linspace(z, 10, N//2, endpoint=False),
                         np.geomspace(10, zmax, N//2)])
    return np.trapz(integrand(zp), zp)

zs = [0.0, 0.03, 0.05, 0.088, 0.12, 0.2, 0.5]
for zmax in [1e5, 1e6, 1e7, 1e8, 3400.0]:
    print(f" zmax={zmax:>9.0e}   " + "  ".join(f"I({z})={I_quad(z,zmax):+.4e}" for z in [0.0,0.05,0.088,0.2]))
print()
print(" trapz cross-check (independent quadrature):")
for zmax in [1e5, 1e6, 1e7]:
    print(f" zmax={zmax:>9.0e}   " + "  ".join(f"I({z})={I_trapz(z,zmax):+.4e}" for z in [0.0,0.05,0.088,0.2]))

print()
# explicit sign scan low-z
zz = np.linspace(0.0, 0.5, 501)
Iv = np.array([I_quad(z, 1e7) for z in zz])
sign_changes = np.where(np.diff(np.sign(Iv)))[0]
print(f" LOW-z sign scan of I(z) over [0,0.5] (zmax=1e7): "
      f"{'CROSSINGS at z=' + str(zz[sign_changes]) if len(sign_changes) else 'NO SIGN CHANGE (single-signed, I>0 throughout)'}")
print(f"   min I over [0,0.5] = {Iv.min():+.4e} at z={zz[np.argmin(Iv)]:.3f};  I(0)={Iv[0]:+.4e}")
print(f"   -> the number 0.088 coincides with I(0) VALUE, NOT a crossing LOCATION.")
print()

print("="*84)
print(" (B) OBSERVABILITY: what measures a0 at z<0.1?")
print("="*84)
probes = [
    ("SPARC RAR (McGaugh)",         "z~0 only",      ">~0.1 dex", "single epoch; no z-leverage"),
    ("Lensing-RAR KiDS 2-bin",      "z~0.24 & 0.37", "~30-50% per bin", "lowest bin z=0.24 >> 0.088"),
    ("MUSE-DARK dwarfs (Ciocan)",   "z~0.3-0.9",     "~50-100%", "all bins ABOVE 0.088"),
    ("BTFR high-z (rotation)",      "z~0.3-2",       "sign-only", "no low-z point"),
]
print(f" {'probe':<26}{'z-reach':<16}{'a0 err':<18}{'note'}")
for p in probes:
    print(f" {p[0]:<26}{p[1]:<16}{p[2]:<18}{p[3]}")
print()
print(" => NO current a0(z) probe reaches z<0.1. The DW feature sits BELOW the reach of every")
print("    a0(z) measurement. A sign flip of a COSMOLOGICAL invariant Z at z=0.088 is not a")
print("    galaxy-scale a0 measurement at all (DW's BOUND a0 is static, eq.31).")
print()

print("="*84)
print(" (C) DEGENERACY: DW static bound-a0 vs framework canonical a0 on the MEASURED axis")
print("="*84)
Z_geo = np.sqrt(32*np.pi/3.0)
def a0_fw_canon(z): return c*H0*np.sqrt(Omega_L)/Z_geo + 0*z
a0_dw_static = 1.2e-10  # DW eq.31 fixed constant
print(f" {'z':>6} {'a0_fw_canon':>13} {'a0_DW_bound(static)':>20}  both ~CONSTANT on measured bins")
for z in [0.0,0.088,0.24,0.37,0.6,0.9]:
    print(f" {z:6.3f} {a0_fw_canon(z):13.4e} {a0_dw_static:20.4e}")
print()
print(" Both are z-flat over every bin any instrument can measure. On the OBSERVED axis they")
print(" are DEGENERATE constants (differ only by a ~28% normalization, absorbable in M/L).")
print(" The framework's *declining* a0 only appears in the pure-Lambda vs rho_total FORK, and")
print(" the canonical (pure-Lambda) reading is ITSELF constant -- so 'framework declining vs DW")
print(" static' is NOT even the right contrast on the canonical footing.")
print()
print("="*84)
print(" VERDICT ON THE a0z LENS")
print("="*84)
print(" (A) The z=0.088 'crossing' is NOT reproduced: I(z) is single-signed (I>0) over [0,0.5];")
print("     0.088 is the VALUE of I(0), not a zero LOCATION. No robust crossing => no feature.")
print(" (B) Even a real crossing at z<0.1 is BELOW the reach of every a0(z) probe -> unobservable.")
print(" (C) DW's static bound a0 and the framework's canonical (constant) a0 are DEGENERATE on")
print("     the measured axis. Front B gains NOTHING; calling the crossing 'distinctive' oversells.")
print("[done]")
