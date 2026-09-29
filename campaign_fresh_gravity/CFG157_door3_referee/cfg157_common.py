#!/usr/bin/env python3
"""cfg157_common -- shared machinery of the CFG157 re-derivation of CFG121's G1/B1 headline (own code; no import from any CFG121 file).
Frozen criteria: CFG157_FROZEN_CRITERIA.md.  kappa = 1/2 is FITTED; nothing here fits anything.
SI units inside the G1 script; the B1 target ODE is dimensionless (x = r/r_M, mu = m/M, beta = h/r_M).
No script prints an absolute home path: only <repo>-relative or bare file names are printed."""
import os, sys, math, json
import numpy as np
from scipy.special import gammainc
from scipy.optimize import minimize_scalar
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    p = os.environ.get("ZF_REPO")
    if p and os.path.isdir(os.path.join(p, "campaign_fresh_gravity")):
        return p
    d = HERE
    while True:
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        n = os.path.dirname(d)
        if n == d:
            return None
        d = n
def rel(path):
    """print-safe path: relative to the repo if found, else the bare file name; never an absolute home path"""
    r = find_repo()
    ap = os.path.abspath(path)
    if r and ap.startswith(r + os.sep):
        return "<repo>/" + os.path.relpath(ap, r)
    return os.path.basename(ap)

G_CFG121 = 6.6743e-11
MSUN = 1.98841e30
KPC = 3.0856775814913673e19
G_ALT = 4.30091727e-6 * 1e6 * KPC / MSUN      # G in m^3/(kg s^2) from 4.30091727e-6 kpc (km/s)^2/Msun (CFG44's unit system)
A0 = {"canonical": 9.3603e-11, "second": 1.1312e-10}
MASSES = [1e9, 1e10, 1e11, 1e12]
def h_of_M(M):
    """scale-length rule (CFG121 disclosure, CFG50's four points): h = 2 + (log10 M - 9) kpc; returns metres"""
    return (2.0 + (math.log10(M) - 9.0)) * KPC

# ------------------------------------------------------------------ baryon profiles (SI)
class ExpSphere:
    """3-D exponential sphere rho = rho0 exp(-r/h), rho0 = M/(8 pi h^3); m(<r) = M gammainc(3, r/h) = M[1-(1+s+s^2/2)e^-s]"""
    kind = "exp"
    def __init__(self, Mkg, h):
        self.M, self.h = Mkg, h
    def m(self, r):
        return self.M * gammainc(3.0, np.asarray(r, float) / self.h)
    def rho(self, r):
        return self.M / (8 * math.pi * self.h ** 3) * np.exp(-np.asarray(r, float) / self.h)
    def mp(self, r):
        r = np.asarray(r, float)
        return 4 * math.pi * r ** 2 * self.rho(r)
    def mtot(self):
        return self.M
class PointMass:
    kind = "pm"
    def __init__(self, Mkg):
        self.M = Mkg
    def m(self, r):
        return self.M * np.ones_like(np.asarray(r, float))
    def rho(self, r):
        return np.zeros_like(np.asarray(r, float))
    def mp(self, r):
        return np.zeros_like(np.asarray(r, float))
    def mtot(self):
        return self.M

# ------------------------------------------------------------------ kernels nu(y), y = g_b/a0, and dnu/dy (analytic)
def nu_p2(y):
    return np.sqrt(1.0 + 1.0 / y)
def dnu_p2(y):
    return -1.0 / (2.0 * y * y * nu_p2(y))
def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)
def dnu_simple(y):
    return -1.0 / (2.0 * np.sqrt(0.25 + 1.0 / y) * y * y)
def nu_rar(y):
    return 1.0 / (-np.expm1(-np.sqrt(y)))
def dnu_rar(y):
    e = np.exp(-np.sqrt(y))
    return -(nu_rar(y) ** 2) * e / (2.0 * np.sqrt(y))
# RECONSTRUCTED nu_mono: the exponential RAR kernel up to y_m = argmax of y(nu-1) (CFG89: 'nu_mono equals the RAR kernel for y < 2.54'),
# and above y_m the bound charge y(nu-1) is held at its maximum c (the 'monotone' completion: (nu-1) g_N non-decreasing).
# This recipe is my reading of 'mono'; it is validated only by reproducing CFG44's quoted point-mass R(x=1) = 1.46 (README-level number).
_r = minimize_scalar(lambda y: -y / np.expm1(np.sqrt(y)), bounds=(0.5, 10), method="bounded", options={"xatol": 1e-13})
Y_M = float(_r.x)
C_M = float(Y_M / np.expm1(math.sqrt(Y_M)))
def nu_mono(y):
    y = np.asarray(y, float)
    return np.where(y <= Y_M, nu_rar(np.minimum(y, Y_M)), 1.0 + C_M / y)
def dnu_mono(y):
    y = np.asarray(y, float)
    return np.where(y <= Y_M, dnu_rar(np.minimum(y, Y_M)), -C_M / y ** 2)
KERNELS = {"P2": (nu_p2, dnu_p2), "simple": (nu_simple, dnu_simple), "mono": (nu_mono, dnu_mono), "rar": (nu_rar, dnu_rar)}

def sym_kernel(name, y):
    import sympy as sp
    if name == "P2":
        return sp.sqrt(1 + 1 / y)
    if name == "simple":
        return sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)
    if name == "rar":
        return 1 / (1 - sp.exp(-sp.sqrt(y)))
    if name == "mono":
        return sp.Piecewise((1 / (1 - sp.exp(-sp.sqrt(y))), y <= Y_M), (1 + C_M / y, True))
    raise KeyError(name)

# ------------------------------------------------------------------ the model observable: three independent derivative routes
def ratio_from_mpol(m, M_pol, Mp_pol, r, a0, G, mtarget):
    """C_model / C_tgt with C_model = rho_pol r^3 g_model, rho_pol = M_pol'/(4 pi r^2), g_model = G (m + M_pol)/r^2, C_tgt = (a0/4pi) mtarget"""
    rho_pol = Mp_pol / (4 * math.pi * r ** 2)
    g_model = G * (m + M_pol) / r ** 2
    return rho_pol * r ** 3 * g_model / (a0 * mtarget / (4 * math.pi))

def route_chain(sph, kern, sgn, a0, G, r, mtarget=None):
    """route 1: chain rule with the exact rho_b: M_pol' = sgn[ m'(nu-1) + m nu_y g'/a0 ], g' = G m'/r^2 - 2 g/r"""
    nu, dnu = KERNELS[kern]
    r = np.asarray(r, float)
    m, mp = sph.m(r), sph.mp(r)
    g = G * m / r ** 2
    gp = G * mp / r ** 2 - 2 * g / r
    y = g / a0
    Mpol = sgn * m * (nu(y) - 1.0)
    Mppol = sgn * (mp * (nu(y) - 1.0) + m * dnu(y) * gp / a0)
    mt = sph.mtot() if mtarget == "total" else m
    return ratio_from_mpol(m, Mpol, Mppol, r, a0, G, mt)

def route_fd(sph, kern, sgn, a0, G, r, mtarget=None, hh=2e-3):
    """route 2: 5-point central difference of M_pol(r) in ln r (M_pol itself from m(<r) and the kernel only)"""
    nu, _ = KERNELS[kern]
    r = np.asarray(r, float)
    def Mp(rr):
        m = sph.m(rr)
        return sgn * m * (nu(G * m / rr ** 2 / a0) - 1.0)
    f = lambda k: Mp(r * math.exp(k * hh))
    dlnr = (-f(2) + 8 * f(1) - 8 * f(-1) + f(-2)) / (12 * hh)
    Mppol = dlnr / r
    m = sph.m(r)
    mt = sph.mtot() if mtarget == "total" else m
    return ratio_from_mpol(m, Mp(r), Mppol, r, a0, G, mt)

_SYM_CACHE = {}
def route_sympy(sph, kern, sgn, a0, G, r, mtarget=None):
    """route 3: sympy derivative of M_pol(r) built from the explicit closed-form enclosed mass, lambdified"""
    import sympy as sp
    key = (sph.kind, kern, sgn, round(sph.M, 6), round(getattr(sph, "h", 0.0), 6), a0, G)
    if key not in _SYM_CACHE:
        rs = sp.symbols("r", positive=True)
        if sph.kind == "exp":
            s = rs / sp.Float(sph.h)
            msym = sp.Float(sph.M) * (1 - (1 + s + s ** 2 / 2) * sp.exp(-s))
        else:
            msym = sp.Float(sph.M) + 0 * rs
        y = sp.Float(G) * msym / rs ** 2 / sp.Float(a0)
        Mpol = sgn * msym * (sym_kernel(kern, y) - 1)
        dM = sp.diff(Mpol, rs)
        _SYM_CACHE[key] = (sp.lambdify(rs, msym, "numpy"), sp.lambdify(rs, Mpol, "numpy"), sp.lambdify(rs, dM, "numpy"))
    fm, fM, fdM = _SYM_CACHE[key]
    r = np.asarray(r, float)
    m = fm(r) * np.ones_like(r)
    mt = sph.mtot() if mtarget == "total" else m
    return ratio_from_mpol(m, fM(r) * np.ones_like(r), fdM(r) * np.ones_like(r), r, a0, G, mt)

def Bfun(y):
    return 0.25 / (y + 0.5 + np.sqrt(y * (y + 1.0)))     # = y + 1/2 - sqrt(y(y+1)), stable form
def closed_form_P2(sph, a0, G, r):
    """my section-3 hand result: C_model/C_tgt = 1 + (dln m/dln r) B(y)   (P2, sign +, target with enclosed mass)"""
    r = np.asarray(r, float)
    m, mp = sph.m(r), sph.mp(r)
    y = G * m / r ** 2 / a0
    return 1.0 + (r * mp / m) * Bfun(y)

def grid_x(n, lo=0.1, hi=30.0):
    return np.logspace(math.log10(lo), math.log10(hi), n)
def rM(Mkg, a0, G):
    return math.sqrt(G * Mkg / a0)

class Tee:
    def __init__(self, path):
        self.f = open(path, "w")
        self.fails = []
    def P(self, s=""):
        print(s)
        self.f.write(s + "\n")
        self.f.flush()
    def check(self, name, ok, detail=""):
        self.P("  [%s] %s  %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            self.fails.append(name)
        return ok
    def close(self):
        self.f.close()
