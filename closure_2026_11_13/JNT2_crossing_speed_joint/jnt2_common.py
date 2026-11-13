"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): the crossing speed v*(z) and the boundary modes. SI throughout.
v* = a0 / (10 (1 + X) H) (route D check C5: v^3 = 10 G M H with M = (1 + X) M_b meets v^4 = G M_b a0), X = 5.41,
H0 = 67.4 km/s/Mpc, OL = 0.6847 (route D's inputs). v*(z) = v*(0) / E(z), a0 constant.
Modes: main (v*), S (FRZ1's v_stiff with SRJ2's membership; twin TW-S), 0 (no boundary; TW-0), H (v*/2; TW-H), D (2 v*; TW-D).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import math
G = 6.67430e-11; MSUN = 1.98892e30; MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XS = 5.41; H0 = 67.4e3 / MPC; OL = 0.6847; OM = 1.0 - OL
VSTIFF = {"canonical": 265.8, "alt": 288.1}
MODES = ("main", "S", "0", "H", "D"); FAC = {"main": 1.0, "H": 0.5, "D": 2.0}
def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def vstar0_kms(ft): return A0[ft] / (10 * (1 + XS) * H0) / 1e3
def vstar_kms(ft, z, mode="main"):
    """the boundary speed in km/s at z for a mode (inf for mode 0; v_stiff constant for mode S)."""
    if mode == "0": return math.inf
    if mode == "S": return VSTIFF[ft]
    return FAC[mode] * vstar0_kms(ft) / E(z)
def vL_kms(Mb_sun, z):
    """the lemma's model virial speed of total mass (1 + X) M_b at 200 rho_crit(z): (10 G M H(z))^(1/3)."""
    return (10 * G * (1 + XS) * Mb_sun * MSUN * H0 * E(z)) ** (1 / 3) / 1e3
def vh_kms(M_sun, z):
    """the same convention for a total mass M (haloes)."""
    return (10 * G * M_sun * MSUN * H0 * E(z)) ** (1 / 3) / 1e3
def logMstar(ft, z, mode="main"):
    """log10 M_b (Msun) above which v_L > v*(z) (main / H / D)."""
    v = vstar_kms(ft, z, mode) * 1e3
    return math.log10(v ** 3 / (10 * G * (1 + XS) * H0 * E(z)) / MSUN)
