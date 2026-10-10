#!/usr/bin/env python3
"""CFG557 library (FROZEN_CRITERIA.md section 1, D3): the dynamical settling catchment s_c = M_c / M_ta.

A shell of enclosed mass M enters the mobility region B n C when it turns around (D1: for a spherical halo B = the turnaround ball).
Its cold energy counts as settled at t_obs only if  t_reach(M; r_e) + t_cap(r_e; alpha) <= t_obs :
  t_reach  first time the shell's spherical-collapse trajectory (flat LCDM, Lambda term, growing-mode start at a_i = 1e-3) reaches the
           edge radius r_e after turnaround (free-fall-limited; = t_ta if the shell turned around inside r_e);
  delta_L(M) from the EPS mean main-progenitor ODE in the barrier variable omega (Neistein, van den Bosch & Dekel 2006 form, recalled,
           PROVISIONAL): dM/domega = -sqrt(2/pi) M / sqrt(S(M/q) - S(M)), q = 2.2, started at (delta_ta,lin(t_obs), M_ta);
  r_e      = r_M / ln(1 + M_b / (s_c (1 - f_b) M_ta)) (point-mass supply-exhaustion edge, CFG541 T2a);
  t_cap    = 1/Gamma at the edge = r_e / (alpha V_f), V_f = (G M_b a0)^(1/4)  (CFG541 Gamma = alpha (rho_c/rho_m) sqrt(4 pi G rho_m),
           deep-law point-mass phantom density at the edge, rho_c/rho_m = 1); alpha = inf -> t_cap = 0 (free-fall ceiling).
s_c is the fixed point of the r_e <-> M_c loop, iterated from s_c = 1.
Units: masses Msun/h, lengths Mpc/h (CFG556 conventions), times in units of 1/H0 internally.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid

# ------------------------------------------------------------------ cosmology + linear spectrum (CFG556 = cfg361_pm.py, verbatim)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000)
_PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (np.trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
RHO_M = Om * 2.77536627e11                    # Msun/h per (Mpc/h)^3
G = 4.30091e-9                                # Mpc km^2 s^-2 Msun^-1
MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0MPC = {f: v * MPC / 1e6 for f, v in A0.items()}
GYR_PER_HINV = 977.792221 / (100 * h)          # 1/H0 in Gyr
MPC_KMS_GYR = 977.792221                       # (1 Mpc)/(1 km/s) in Gyr

def fret_of(lM):
    """CFG416 cfg416_pm.py fret_of, copied verbatim (as in cfg515_lib.py / cfg556)."""
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)

# sigma(M) at z = 0 on a fine log grid
_LMS = np.linspace(5.0, 17.0, 1201)
def _sigma_R(R):
    x = np.outer(R, _KG); w = _W8(np.maximum(x, 1e-6))
    return np.sqrt(np.trapz(_PK * w ** 2 * _KG ** 2, _KG, axis=1) / (2 * math.pi ** 2))
_SIG0 = _sigma_R((3 * 10 ** _LMS / (4 * math.pi * RHO_M)) ** (1 / 3))
def S0(M):
    return np.interp(np.log10(M), _LMS, _SIG0) ** 2

# ------------------------------------------------------------------ background: age, growth (no radiation)
def Hof(a): return math.sqrt(Om / a ** 3 + OL)
def age(a):                                   # in 1/H0
    return quad(lambda x: 1.0 / (x * Hof(x)), 0.0, a, epsabs=1e-13, epsrel=1e-12, limit=200)[0] if a > 0 else 0.0
def Dgrow(a):                                 # unnormalised growing mode, D ~ a early
    return 2.5 * Om * Hof(a) * quad(lambda x: 1.0 / (x * Hof(x)) ** 3, 0.0, a, epsabs=1e-14, epsrel=1e-12, limit=200)[0]
def a_of_t(t):
    return brentq(lambda a: age(a) - t, 1e-6, 50.0, xtol=1e-14)
T0 = age(1.0)

# ------------------------------------------------------------------ spherical collapse tables per observation epoch
AI = 1e-3
UGRID = np.concatenate([np.geomspace(0.003, 0.2, 40), np.linspace(0.205, 1.0, 80)])

def shell(dL, a_obs, t_end=None):
    """trajectory of a shell with linear overdensity dL (extrapolated to a_obs).  r in units of the comoving Lagrangian radius R_L.
    returns dict(t_ta, r_ta, a_ta, t_coll, dt_of_u (array on UGRID: time from turnaround to r = u r_ta))."""
    di = dL * Dgrow(AI) / Dgrow(a_obs)
    ti = age(AI)
    ri = AI * (1 - di / 3.0); vi = Hof(AI) * AI * (1 - 2 * di / 3.0)
    rhs = lambda t, y: [y[1], -0.5 * Om / y[0] ** 2 + OL * y[0]]
    ev = lambda t, y: y[1]; ev.terminal = True; ev.direction = -1
    te = t_end if t_end is not None else 400.0
    s1 = solve_ivp(rhs, (ti, te), [ri, vi], events=ev, rtol=1e-11, atol=1e-14, method="DOP853")
    if not s1.t_events[0].size:
        return None
    tta = s1.t_events[0][0]; rta = s1.y_events[0][0][0]
    ev2 = lambda t, y: y[0] - 0.002 * rta; ev2.terminal = True; ev2.direction = -1
    s2 = solve_ivp(rhs, (tta, tta + 400.0), [rta, 0.0], events=ev2, rtol=1e-11, atol=1e-14, method="DOP853", dense_output=True)
    tc = s2.t_events[0][0]
    tt = np.linspace(tta, tc, 4000); rr = s2.sol(tt)[0]
    # r decreasing monotonically after turnaround
    dt = np.interp(UGRID, rr[::-1] / rta, (tt - tta)[::-1])
    # collapse time to r = 0 (extrapolate the last bit as free fall ~ r^{3/2})
    tcoll = tc + (2.0 / 3.0) * (0.002 * rta) ** 1.5 / math.sqrt(Om)
    return dict(t_ta=tta, r_ta=rta, a_ta=a_of_t(tta), t_coll=tcoll, dt=dt)

class Epoch:
    """spherical-collapse tables at one observation epoch (z_obs)."""
    def __init__(self, z_obs=0.0, t_obs_override=None, ndl=170):
        self.z = z_obs; self.a = 1.0 / (1.0 + z_obs); self.t_obs = age(self.a) if t_obs_override is None else t_obs_override
        self.Dratio = Dgrow(self.a) / Dgrow(1.0)
        tob = age(self.a)
        # delta_ta,lin(t_obs): shell turning around exactly at the (true) observation epoch
        def f_ta(d):
            r = shell(d, self.a)
            return 1e3 if r is None else r["t_ta"] - tob
        self.d_ta = brentq(f_ta, 0.3, 3.0, xtol=1e-10)
        st = shell(self.d_ta, self.a)
        self.Delta_ta = (st["a_ta"] / st["r_ta"]) ** 3
        def f_c(d):
            r = shell(d, self.a)
            return 1e3 if r is None else r["t_coll"] - tob
        self.d_c = brentq(f_c, 1.0, 4.0, xtol=1e-9)
        self.DL = np.geomspace(self.d_ta * 0.999, 60.0, ndl)
        rows = [shell(d, self.a) for d in self.DL]
        self.TTA = np.array([r["t_ta"] for r in rows]); self.RTA = np.array([r["r_ta"] for r in rows])
        self.DT = np.array([r["dt"] for r in rows])
        self.lDL = np.log(self.DL)

    def t_reach(self, dL, x_rL):
        """dL array of shells' linear overdensities; x_rL = r_e / R_L per shell.  Time (1/H0) when each shell first reaches r_e."""
        ld = np.log(np.clip(dL, self.DL[0], self.DL[-1]))
        tta = np.interp(ld, self.lDL, self.TTA); rta = np.interp(ld, self.lDL, self.RTA)
        u = x_rL / rta
        out = tta.copy()
        m = u < 1.0
        if np.any(m):
            j = np.clip(np.searchsorted(self.lDL, ld[m]) - 1, 0, len(self.DL) - 2)
            w = (ld[m] - self.lDL[j]) / (self.lDL[j + 1] - self.lDL[j])
            uu = np.clip(u[m], UGRID[0], 1.0)
            d0 = np.array([np.interp(a, UGRID, self.DT[i]) for a, i in zip(uu, j)])
            d1 = np.array([np.interp(a, UGRID, self.DT[i + 1]) for a, i in zip(uu, j)])
            out[m] = tta[m] + (1 - w) * d0 + w * d1
        return out

    def mah(self, Mta, q=2.2, xmin=0.02):
        """mean main-progenitor history in omega: returns (x = M/M_ta grid, delta_L(x))."""
        Dr2 = self.Dratio ** 2
        def rhs(om, y):
            M = math.exp(y[0]); ds = (S0(M / q) - S0(M)) * Dr2
            return [-math.sqrt(2 / math.pi) / math.sqrt(max(ds, 1e-30))]
        ev = lambda om, y: y[0] - math.log(xmin * Mta); ev.terminal = True
        s = solve_ivp(rhs, (self.d_ta, self.d_ta + 200.0), [math.log(Mta)], events=ev, rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.05)
        om = np.linspace(self.d_ta, s.t[-1], 3000); lx = s.sol(om)[0] - math.log(Mta)
        X = np.geomspace(xmin, 1.0, 300)
        dL = np.interp(np.log(X), lx[::-1], om[::-1])
        return X, dL

def r_lagr(M):
    return (3 * M / (4 * math.pi * RHO_M)) ** (1 / 3)        # comoving Mpc/h

def edge(Mb, Mta, sc, foot):
    """point-mass supply-exhaustion edge (Mpc/h, physical) for settled supply sc (1 - f_b) M_ta; baryons Mb (Msun/h)."""
    rM = math.sqrt(G * Mb * h / A0MPC[foot])
    if sc <= 0:
        return 0.0
    return rM / math.log1p(Mb / (sc * (1 - FB) * Mta))

def t_cap(Mb, re, foot, alpha):
    if not np.isfinite(alpha):
        return 0.0
    Vf = (G * (Mb / h) * A0MPC[foot]) ** 0.25                  # km/s
    return MPC_KMS_GYR * (re / h) / Vf / alpha / GYR_PER_HINV    # in 1/H0

def s_catch(E, Mta, Mb, foot, alpha=math.inf, q=2.2, mah=None, tol=1e-6, itmax=200, full=False):
    """fixed point s_c for one object (M_ta, M_b in Msun/h) at epoch E."""
    X, dL = mah if mah is not None else E.mah(Mta, q=q)
    RL = r_lagr(X * Mta)                                        # comoving Mpc/h; trajectories are in units of R_L (r = a at mean)
    sc = 1.0; hist = []
    for it in range(itmax):
        re = edge(Mb, Mta, sc, foot)
        tr = E.t_reach(dL, re / RL) + t_cap(Mb, re, foot, alpha)
        ok = tr <= E.t_obs
        if ok.all():
            new = 1.0
        elif not ok.any():
            new = float(X[0])
        else:
            i = int(np.nonzero(~ok)[0][0])                       # first failing shell (outermost satisfied is i-1)
            if i == 0:
                new = float(X[0])
            else:
                t1, t2 = tr[i - 1] - E.t_obs, tr[i] - E.t_obs
                new = float(X[i - 1] + (X[i] - X[i - 1]) * (-t1) / (t2 - t1))
        hist.append(new)
        if abs(new - sc) < tol:
            sc = new; break
        sc = new
    conv = abs(hist[-1] - (hist[-2] if len(hist) > 1 else 1.0)) < tol or len(hist) == 1
    if full:
        re = edge(Mb, Mta, sc, foot)
        return dict(sc=sc, re=re, iters=len(hist), converged=bool(conv), tcap_gyr=t_cap(Mb, re, foot, alpha) * GYR_PER_HINV)
    return sc
