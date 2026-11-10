"""R541B core: expanding background of action (A) + (-V(tau)), P = 0.
Units: time in 1/H0, densities in rho_c0 = 3 H0^2 / (8 pi G), so H^2 = sum of densities (H0 = 1).
K rho_c0 = (3/2) H0^2, hence Q - 1 = K C / (mu^2 a^3) = 1.5 C / (m^2 a^3) with m = mu_K c / H0, and
rho_K = mu^2 (Q^2 - 1) / (2K) = (m^2 / 3)(Q^2 - 1), p_K = (m^2 / 3)(Q - 1)^2.
Charge equation (KA1): dC/dt = -a^3 V'(tau); in N = ln a: dC/dN = -a^3 V'(tau) / H, dtau/dN = Q / H."""
import numpy as np
from scipy.integrate import solve_ivp

H0_PER_MPC = 67.4 / 299792.458          # H0 / c in 1/Mpc at h 0.674
H0_SI = 67.4e3 / 3.0856775814913673e22   # 1/s
h = 0.674
OMEGA_R = 2.47e-5 * (1 + 0.2271 * 3.044) / h**2
FOOT = {"canonical": dict(omb=0.02236, R=5.410), "alt": dict(omb=0.02234, R=5.412)}
OMD = 0.1209 / h**2


METHOD = "LSODA"


def cosmo(foot, omb_scale=1.0):
    ob = FOOT[foot]["omb"] / h**2 * omb_scale
    return dict(Ob=ob, Or=OMEGA_R, OL=1 - ob - OMD - OMEGA_R, R=FOOT[foot]["R"])


def m_of_mu(mu_per_mpc):
    return mu_per_mpc / H0_PER_MPC


class Pot:
    """V(tau) and V'(tau); kind in exp, tanh, power, step-free zero."""
    def __init__(self, kind, V0, ts, **kw):
        self.kind, self.V0, self.ts, self.kw = kind, V0, ts, kw

    def V(self, tau):
        k, V0, ts = self.kind, self.V0, self.ts
        if k == "zero":
            return 0.0
        if k == "exp":
            return V0 * np.exp(-tau / ts)
        if k == "tanh":
            D = self.kw["D"]
            return 0.5 * V0 * (1 - np.tanh((tau - ts) / D))
        if k == "power":
            return V0 * (1 + tau / ts) ** (-self.kw["n"])
        if k == "rising":  # MU1: sign flip, V increases with tau and saturates
            return V0 * (1 - np.exp(-tau / ts))
        raise ValueError(k)

    def dV(self, tau):
        k, V0, ts = self.kind, self.V0, self.ts
        if k == "zero":
            return 0.0
        if k == "exp":
            return -V0 / ts * np.exp(-tau / ts)
        if k == "tanh":
            D = self.kw["D"]
            return -0.5 * V0 / D / np.cosh(min((tau - ts) / D, 700.0)) ** 2
        if k == "power":
            n = self.kw["n"]
            return -n * V0 / ts * (1 + tau / ts) ** (-n - 1)
        if k == "rising":
            return V0 / ts * np.exp(-tau / ts)
        raise ValueError(k)


def Hof(a, C, Vv, cp, m):
    x = 1.5 * C / (m**2 * a**3)          # Q - 1, kept separately to avoid cancellation in Q^2 - 1
    Q = 1 + x
    rhoK = (C / a**3) * (1 + x / 2)        # = (m^2/3)(Q^2 - 1) = (m^2/3) x (2 + x)
    return np.sqrt(cp["Or"] / a**4 + cp["Ob"] / a**3 + rhoK + Vv + cp["OL"]), Q, rhoK


def t_rad(a, cp):
    """proper time since the bang in the radiation era: t = 1/(2H), H = sqrt(Or)/a^2."""
    return a**2 / (2 * np.sqrt(cp["Or"]))


def run(pot, cp, m, a_ini=1e-14, a_end=1.0, C_i=0.0, tau_off=0.0, segs=None, rtol=1e-10, dense=True):
    """Integrate (C, tau) in N = ln a. segs: list of (N_lo, N_hi, max_step) for fine regions."""
    def rhs(N, y):
        a = np.exp(N); C, tau = y
        Vv = pot.V(tau)
        H, Q, _ = Hof(a, C, Vv, cp, m)
        return [-a**3 * pot.dV(tau) / H, Q / H]
    N0, N1 = np.log(a_ini), np.log(a_end)
    y0 = [C_i, t_rad(a_ini, cp) + tau_off]
    edges = [N0]
    steps = []
    if segs:
        for lo, hi, ms in sorted(segs):
            lo, hi = max(lo, N0), min(hi, N1)
            if lo >= hi:
                continue
            if lo > edges[-1]:
                edges.append(lo); steps.append(np.inf)
            edges.append(hi); steps.append(ms)
    if edges[-1] < N1:
        edges.append(N1); steps.append(np.inf)
    sols = []
    y = y0
    for i in range(len(steps)):
        try:
            s = solve_ivp(rhs, (edges[i], edges[i + 1]), y, method=METHOD, rtol=rtol, atol=[1e-30, 1e-40],
                          max_step=steps[i], dense_output=dense)
        except ValueError:   # LSODA dense output with a repeated time: fall back to Radau
            s = solve_ivp(rhs, (edges[i], edges[i + 1]), y, method="Radau", rtol=rtol, atol=[1e-30, 1e-40],
                          max_step=steps[i], dense_output=dense)
        if not s.success:
            raise RuntimeError(s.message)
        sols.append(s); y = s.y[:, -1]
    return Sol(sols, pot, cp, m)


class Sol:
    def __init__(self, sols, pot, cp, m):
        self.sols, self.pot, self.cp, self.m = sols, pot, cp, m
        self.Nmin = sols[0].t[0]; self.Nmax = sols[-1].t[-1]

    def y(self, N):
        for s in self.sols:
            if s.t[0] <= N <= s.t[-1]:
                return s.sol(N)
        return self.sols[-1].y[:, -1] if N > self.Nmax else self.sols[0].y[:, 0]

    def C(self, a):
        return self.y(np.log(a))[0]

    def Cfin(self):
        return self.sols[-1].y[0, -1]

    def state(self, a):
        C, tau = self.y(np.log(a))
        Vv = self.pot.V(tau)
        H, Q, rhoK = Hof(a, C, Vv, self.cp, self.m)
        x = 1.5 * C / (self.m**2 * a**3)
        pK = (self.m**2 / 3) * x**2
        return dict(C=C, tau=tau, V=Vv, dV=self.pot.dV(tau), H=H, Q=Q, x=x, rhoK=rhoK, pK=pK)

    def z_of_frac(self, f):
        """largest z at which C reached fraction f of the final charge (scan)."""
        Cf = self.Cfin()
        Ns = np.linspace(self.Nmin, self.Nmax, 6001)
        Cs = np.array([self.y(N)[0] for N in Ns])
        idx = np.argmax(Cs >= f * Cf)
        return np.exp(-Ns[idx]) - 1
