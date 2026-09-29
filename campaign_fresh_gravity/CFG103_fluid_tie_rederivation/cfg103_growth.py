"""CFG103 growth core (own code): Newtonian sub-horizon two-fluid linear growth in ln a, LCDM background, pressured fluid with c_s^2 from its EOS.
Frozen definitions: see FROZEN_DOCSTRING.txt (b).  Units: k comoving in 1/Mpc, c/H0 = 299792.458/(100 h) Mpc."""
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

C_KMS = 299792.458
class Cosmo:
    def __init__(self, H0=67.4, Om=0.315, Ob=0.0493, OL=0.685, kappa=0.5):
        self.H0, self.Om, self.Ob, self.OL, self.Oc = H0, Om, Ob, OL, Om - Ob
        self.h = H0 / 100.0; self.fb = Ob / Om; self.fc = 1 - self.fb
        self.kappa = kappa; self.eps = kappa**2 / (8 * np.pi)
        self.cH = C_KMS / H0                                    # c/H0 in Mpc
    def E2(self, a): return self.Om * a**-3 + self.OL
    def dlnH(self, a): return -1.5 * self.Om * a**-3 / self.E2(a)
    def Oma(self, a): return self.Om * a**-3 / self.E2(a)

# ---- EOS shape:  P = Pcap F(x),  rho = m n + Pcap G(x),  G = x Int_0^x F(y)/y^2 dy   (arctan: F=x^2/(1+x^2), G = x atan x)
_tabs = {}
def _shape(p):
    if p == "atan":
        F = lambda x: x**2 / (1 + x**2); dF = lambda x: 2 * x / (1 + x**2)**2; G = lambda x: x * np.arctan(x)
        return F, dF, G
    if p in _tabs: return _tabs[p]
    def F(x):
        x = np.asarray(x, float); return 1.0 / (1.0 + np.exp(-p * np.log(x)))               # = x^p/(1+x^p), overflow-safe
    def dF(x):
        x = np.asarray(x, float); f = 1.0 / (1.0 + np.exp(-p * np.log(x))); return p * f * (1 - f) / x
    ls = np.linspace(-12, 12, 1201); xs = 10**ls
    # I(x) = Int_0^x F(y)/y^2 dy = x0^(p-1)/(p-1) [tail 0..x0, F ~ y^p] + cumulative quad over [x_j, x_j+1]   (p > 1)
    Iv = np.empty_like(xs); Iv[0] = xs[0]**(p - 1) / (p - 1)
    for j in range(1, len(xs)): Iv[j] = Iv[j - 1] + quad(lambda y: F(y) / y**2, xs[j - 1], xs[j], epsabs=0, epsrel=1e-12)[0]
    Gt = xs * Iv
    G = lambda x: np.exp(np.interp(np.log10(x), ls, np.log(Gt)))
    _tabs[p] = (F, dF, G); return _tabs[p]

def cs2_eos(x, nu, eps, p="atan"):
    """c_s^2 = n P_n/(rho+P)  with  mn = nu*rho_L*x, P = eps rho_L F(x), rho = mn + eps rho_L G(x)   (all in units of rho_L)."""
    F, dF, G = _shape(p)
    return eps * x * dF(x) / (nu * x + eps * (G(x) + F(x)))

def growth_ratio(nu, k, cos, zi=1e4, zev=0.0, cs="eos", shape="atan", rtol=1e-9, ret_full=False, bg=None, y0=None):
    """delta_m(zev)/delta_m^LCDM(zev) for the pressured-fluid model (LCDM background, pressureless baryons f_b, fluid f_c)."""
    ai, ae = 1.0 / (1 + zi), 1.0 / (1 + zev)
    def cs2(a):
        if cs == "zero": return 0.0
        if isinstance(cs, (int, float)): return float(cs)
        x = (cos.Oc / cos.OL) * a**-3 / nu
        return cs2_eos(x, nu, cos.eps, shape)
    def rhs(s, y):
        a = np.exp(s); E = np.sqrt(cos.E2(a)); dl = cos.dlnH(a)
        src = 1.5 * cos.Oma(a) * (cos.fb * y[0] + cos.fc * y[2])
        pres = cs2(a) * (k * cos.cH / (a * E))**2 * y[2]
        return [y[1], -(2 + dl) * y[1] + src, y[3], -(2 + dl) * y[3] + src - pres]
    y0 = [ai, ai, ai, ai] if y0 is None else y0
    sol = solve_ivp(rhs, [np.log(ai), np.log(ae)], y0, method="LSODA", rtol=rtol, atol=1e-16 * ai, first_step=1e-6)
    dm = cos.fb * sol.y[0, -1] + cos.fc * sol.y[2, -1]
    return dm if ret_full else dm

_ref = {}
def lcdm_dm(cos, zi=1e4, zev=0.0):
    key = (cos.Om, cos.OL, cos.Ob, zi, zev)
    if key not in _ref: _ref[key] = growth_ratio(1.0, 1.0, cos, zi, zev, cs="zero")
    return _ref[key]

def ratio(nu, k, cos, zi=1e4, zev=0.0, cs="eos", shape="atan"):
    return growth_ratio(nu, k, cos, zi, zev, cs, shape) / lcdm_dm(cos, zi, zev)

def numin_scan(k, cos, deltas, zi=1e4, zev=0.0, shape="atan", cs="eos", nu_est=None, step=0.05, floor=0.2):
    """nu_min(k;d): smallest nu* such that ratio >= 1-d for every nu' >= nu*.  Descend from a high nu* (30x estimate) in 0.05-dex steps until
    ratio < floor, then brentq inside the bracket of each threshold."""
    if nu_est is None: nu_est = 2e5 * (k / 2.0)**1.5 * (cos.eps / (0.25 / (8 * np.pi)))**0.75
    nus, rs = [], []
    nu = nu_est * 30.0
    r = ratio(nu, k, cos, zi, zev, cs, shape)
    n_ext = 0
    while r < 1 - min(deltas) + 0.04 and n_ext < 6: nu *= 10; r = ratio(nu, k, cos, zi, zev, cs, shape); n_ext += 1
    nus.append(nu); rs.append(r)
    for i in range(1, 400):
        nu = nu * 10**(-step); r = ratio(nu, k, cos, zi, zev, cs, shape)
        nus.append(nu); rs.append(r)
        if r < floor: break
    out = {}
    for d in deltas:
        thr = 1 - d; j = next((j for j, r_ in enumerate(rs) if r_ < thr), None)
        if j is None or j == 0: out[d] = np.nan; continue
        f = lambda ln: ratio(np.exp(ln), k, cos, zi, zev, cs, shape) - thr
        out[d] = float(np.exp(brentq(f, np.log(nus[j]), np.log(nus[j - 1]), xtol=1e-4)))
    return out, (np.array(nus), np.array(rs))
