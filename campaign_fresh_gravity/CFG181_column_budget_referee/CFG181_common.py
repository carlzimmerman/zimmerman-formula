# CFG181_common -- shared helpers of the CFG181 referee lane (written from the frozen criteria; nothing imported from the repo).
# Deviation from the frozen script plan (disclosed): helpers live here instead of being duplicated in main and attacks.
import math, numpy as np
G = 6.67430e-11; C = 299792458.0
MSUN = 1.32712440018e20 / G          # IAU nominal GM_sun
PC = 3.0856775814913673e16; MPC = PC * 1e6; KPC = PC * 1e3
GYR = 3.15576e16
MSUN_PC2 = MSUN / PC**2              # kg/m^2 per Msun/pc^2 (inverse used below)
A0_A = 9.3603e-11; A0_B = 1.13e-10
def H0_si(h): return h * 1e5 / MPC
def rho_crit(h): return 3 * H0_si(h)**2 / (8 * math.pi * G)
def rho_L(h, OL): return OL * rho_crit(h)
def to_msunpc2(sig_kgm2): return sig_kgm2 / MSUN * PC**2
def age_flat(h, OL, Or=0.0):
    """cosmic age (s) of a flat LCDM; Or=0 -> closed form."""
    Om = 1 - OL - Or
    if Or == 0.0:
        return 2 / (3 * H0_si(h) * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om))
    from scipy.integrate import quad
    f = lambda a: 1.0 / (H0_si(h) * math.sqrt(Om / a + Or / a**2 + OL * a**2))
    return quad(f, 0, 1, limit=200)[0]
def t_of_z(h, OL, z):
    Om = 1 - OL
    return 2 / (3 * H0_si(h) * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om) * (1 + z)**-1.5)
def E_of_z(Om, z): return math.sqrt(Om * (1 + z)**3 + 1 - Om)
def nu_p2(y): y = np.asarray(y, float); return np.sqrt(1.0 + 1.0 / y)
def nu_simple(y): y = np.asarray(y, float); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def nu_rar(y): y = np.asarray(y, float); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def build_nu_mono():
    """re-implementation of the shared definition (Bcommon nu_mono): independence STOPS here."""
    from scipy.optimize import brentq
    def h(y):
        y = np.asarray(y, float)
        with np.errstate(over="ignore"):
            return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
    def dh(y, e=1e-6): return (h(y * (1 + e)) - h(y * (1 - e))) / (2 * y * e)
    YP = brentq(lambda y: float(dh(y)), 1.0, 5.0); HP = float(h(YP))
    L = np.linspace(-14, 14, 280001); Y = 10**L
    DH = np.maximum(dh(Y), 0.05 * HP / (Y + YP))
    HM = float(h(Y[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(Y))])
    def nu(y):
        y = np.maximum(np.asarray(y, float), 1e-14)
        return 1.0 + np.interp(np.log10(y), L, HM) / y
    return nu
def col_units(nu, y):
    """M_c(<r)/(pi r^2) of a point mass in units of a0/(2 pi G), y = g_N/a0 = 1/x^2:  2 y (nu-1)."""
    return 2.0 * np.asarray(y, float) * (nu(y) - 1.0)
def Sigma_P2(a0): return to_msunpc2(a0 / (2 * math.pi * G))      # Msun/pc^2
def swept(h, OL, t, u=C): return to_msunpc2(rho_L(h, OL) * u * t)
def r500(M, h, delta=500.0, rho_ref=None):
    rho = rho_crit(h) if rho_ref is None else rho_ref
    return (3 * M * MSUN / (4 * math.pi * delta * rho))**(1 / 3)   # m
