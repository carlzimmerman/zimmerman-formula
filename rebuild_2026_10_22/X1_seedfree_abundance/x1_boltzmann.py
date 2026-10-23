"""X1 E2: momentum-resolved quantum Boltzmann for the isotropic, charge-symmetric Phi bath (FROZEN_CRITERIA §2 E2).

Conformal units (comoving p in a_e H_inf, conformal time tau = H_inf eta). Radiation era and m a << m_H, so the kinetic
equation is autonomous. 2<->2 elastic, contact |M|^2 = (4 lam)^2 for Phi+Phi+ and Phi+Phi-, effective S|M|^2 = 24 lam^2,
full Bose factors (classical=True keeps only the cubic terms, the classical-statistical limit used for the TW overlap).
Exact isotropic reduction:
  C(p1) = S|M|^2/(16 pi^4 E1 p1) int dp2 dp3 (p2 p3/(E2 E3)) J(p1,p2,p3,p4) F,   E4 = E1+E2-E3,
  J = int_0^inf dl l^-2 prod_i sin(l p_i) = -(pi/16) sum_j c_j |a_j|  (eight signed combinations).
Hartree mass m_H^2 = (2 lam/pi^2) int p^2 f/E dp, self-consistent. Number and energy conserved by a two-parameter
projection on the f(1+f) shape.
"""
import numpy as np
from scipy.integrate import solve_ivp

LAM = .00881292
SIGNS = [(+1, (1, -1, 1, -1)), (+1, (1, -1, -1, 1)), (-1, (1, -1, 1, 1)), (-1, (1, -1, -1, -1)),
         (-1, (1, 1, 1, -1)), (-1, (1, 1, -1, 1)), (+1, (1, 1, 1, 1)), (+1, (1, 1, -1, -1))]


def Jfun(p1, p2, p3, p4):
    s = 0.
    for c, (a, b, cc, d) in SIGNS:
        s = s+c*np.abs(a*p1+b*p2+cc*p3+d*p4)
    return -np.pi/16*s


class Boltz:
    def __init__(self, pmax=8., Np=96, lam=LAM, classical=False):
        self.dp = pmax/Np; self.p = (np.arange(Np)+.5)*self.dp; self.Np = Np; self.lam = lam
        self.classical = classical; self.SM2 = 24*lam*lam

    def hartree(self, f, m2=0.):
        m2h = m2
        for _ in range(30):
            E = np.sqrt(self.p**2+m2h); new = 2*self.lam/np.pi**2*np.sum(self.p**2*f/E)*self.dp
            if abs(new-m2h) < 1e-14*max(new, 1e-30): m2h = new; break
            m2h = new
        return m2h

    def interp_f(self, E4, E, f, inside):
        """Interpolate in energy the variable that is linear for the stationary state: ln(1+1/f) (Bose-Einstein) or
        1/f (classical Rayleigh-Jeans), so equilibrium is reproduced exactly between grid points."""
        fs = np.maximum(f, 1e-300)
        if self.classical:
            y = np.interp(E4, E, 1/fs); out = 1/np.maximum(y, 1e-300)
        else:
            y = np.interp(E4, E, np.log1p(1/fs)); out = 1/np.expm1(np.maximum(y, 1e-300))
        return np.where(inside & (E4 >= E[0]), out, np.where(inside, f[0], 0.))

    def grid_eq(self, f, m2h):
        """Stationary distribution with the same grid number and energy: BE(T, mu) (quantum) or T/(E - mu) (classical).
        Returns (feq, T, mu, saturated) where saturated means mu hit the lowest grid energy (overpopulation)."""
        p = self.p; E = np.sqrt(p*p+m2h); w = p*p
        N = np.sum(w*f); R = np.sum(w*E*f)
        def shape(T, mu):
            x = np.maximum((E-mu)/T, 1e-12)
            return T/(E-mu) if self.classical else 1/np.expm1(np.minimum(x, 700))
        from scipy.optimize import brentq
        mumax = E[0]*(1-1e-6)
        def T_for(mu):
            g = lambda lt: np.sum(w*E*shape(np.exp(lt), mu))-R
            return np.exp(brentq(g, -12, 8))
        def resid(mu):
            T = T_for(mu); return np.sum(w*shape(T, mu))-N
        lo, hi = -50*E[-1], mumax
        try:
            if resid(hi) < 0:
                T = T_for(hi); return shape(T, hi), T, hi, True
            mu = brentq(resid, lo, hi, xtol=1e-14); T = T_for(mu); return shape(T, mu), T, mu, False
        except ValueError:
            return None, np.nan, np.nan, True

    def collision(self, f, m2h, subtract=True):
        C, pr = self.collision_raw(f, m2h)
        if subtract:
            feq, T, mu, sat = self.grid_eq(f, m2h)
            if feq is not None:
                Ce, _ = self.collision_raw(feq, m2h); C = C-Ce
        return C, pr

    def collision_raw(self, f, m2h):
        p = self.p; E = np.sqrt(p**2+m2h); dp = self.dp
        P2, P3 = np.meshgrid(p, p, indexing='ij'); E2, E3 = np.meshgrid(E, E, indexing='ij')
        f2, f3 = np.meshgrid(f, f, indexing='ij')
        C = np.zeros_like(f)
        for i in range(self.Np):
            E4 = E[i]+E2-E3; ok = E4 > np.sqrt(m2h)+1e-300
            p4 = np.sqrt(np.maximum(E4**2-m2h, 0.))
            f4 = self.interp_f(E4, E, f, p4 <= p[-1]+dp/2)
            J = Jfun(p[i], P2, P3, p4)
            if self.classical:
                F = f3*f4*(f[i]+f2)-f[i]*f2*(f3+f4)
            else:
                F = f3*f4*(1+f[i])*(1+f2)-f[i]*f2*(1+f3)*(1+f4)
            integ = np.where(ok, P2*P3/(E2*E3)*J*F, 0.)
            C[i] = self.SM2/(16*np.pi**4*E[i]*p[i])*np.sum(integ)*dp*dp
        # conservation projection (number and energy) on the f(1+f) shape
        w = p*p*f*(1+f)+1e-300; A = np.array([[np.sum(w), np.sum(w*E)], [np.sum(w*E), np.sum(w*E*E)]])
        b = -np.array([np.sum(p*p*C), np.sum(p*p*E*C)])
        try:
            al, be = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            al = be = 0.
        corr = (al+be*E)*w/(p*p)
        return C+corr, float(np.max(np.abs(corr))/max(np.max(np.abs(C)), 1e-300))

    def moments(self, f, m2h):
        E = np.sqrt(self.p**2+m2h); w = self.p**2*self.dp/(2*np.pi**2)
        return dict(n=float(2*np.sum(w*f)), rho=float(2*np.sum(w*E*f)), mH2=float(m2h))

    def evolve(self, f0, tau0, tau1, ntimes=40, rtol=1e-5, fmax_stop=1e6):
        ts = np.unique(np.concatenate([[tau0], np.geomspace(max(tau0, 1.), tau1, ntimes)]))
        ts = ts[(ts >= tau0) & (ts <= tau1)]
        state = {'proj': 0.}
        def rhs(t, f):
            fpos = np.maximum(f, 0.); m2h = self.hartree(fpos)
            C, pr = self.collision(fpos, m2h); state['proj'] = max(state['proj'], pr); return C
        def blow(t, f): return fmax_stop-np.max(f)
        blow.terminal = True
        sol = solve_ivp(rhs, (tau0, tau1), f0, t_eval=ts, rtol=rtol, atol=1e-10, method='RK45', events=blow)
        out = []
        for k, t in enumerate(sol.t):
            f = np.maximum(sol.y[:, k], 0.); m2h = self.hartree(f); mom = self.moments(f, m2h)
            out.append(dict(tau=float(t), f=f.tolist(), **mom))
        return out, dict(status=int(sol.status), message=sol.message, nfev=int(sol.nfev), max_projection=state['proj'],
                         condensation_stop=bool(sol.status == 1))


def be_fit(n, rho, lam=LAM, gdof=2):
    """Bose-Einstein (T, mu) with Hartree mass reproducing number and energy densities (both charges); if the number
    exceeds the mu -> m_H limit the excess is a condensate (returned)."""
    from scipy.optimize import brentq
    u = np.linspace(1e-4, 60, 4000)
    def thermo(T, mu):
        m2 = 0.
        for _ in range(50):
            E = np.sqrt((u*T)**2+m2); x = np.minimum((E-mu)/T, 700); f = 1/np.expm1(np.maximum(x, 1e-12))
            m2n = 2*lam/np.pi**2*np.trapz((u*T)**2*f/E, u*T)
            if abs(m2n-m2) < 1e-13*max(m2n, 1e-30): m2 = m2n; break
            m2 = m2n
        E = np.sqrt((u*T)**2+m2); x = np.maximum((E-mu)/T, 1e-12); f = 1/np.expm1(np.minimum(x, 700))
        nn = gdof*np.trapz((u*T)**2*f, u*T)/(2*np.pi**2); rr = gdof*np.trapz((u*T)**2*E*f, u*T)/(2*np.pi**2)
        return nn, rr, m2
    def T_of(mu_frac):
        # energy matched at chemical potential mu = mu_frac * m_H(T,mu)
        def g(T):
            nn, rr, m2 = thermo(T, 0.)
            mu = mu_frac*np.sqrt(m2); nn, rr, m2 = thermo(T, mu); return rr-rho
        return brentq(g, 1e-6, 1e3)
    T0 = T_of(0.); n0, r0, m20 = thermo(T0, 0.)
    if n <= n0:
        return dict(T=T0, mu=0., mH2=m20, n_eq_mu0=n0, overpopulation=n/n0, condensate_n=0.)
    lo, hi = 0., .999999
    for _ in range(60):
        mid = (lo+hi)/2; T = T_of(mid); nn, rr, m2 = thermo(T, mid*np.sqrt(m2 if 'm2' in dir() else 0.))
        nn, rr, m2 = thermo(T, mid*np.sqrt(thermo(T, 0.)[2]))
        if nn < n: lo = mid
        else: hi = mid
    T = T_of(lo); nn, rr, m2 = thermo(T, lo*np.sqrt(thermo(T, 0.)[2]))
    return dict(T=T, mu=lo*np.sqrt(m2), mH2=m2, n_eq_mu0=n0, overpopulation=n/n0, condensate_n=max(n-nn, 0.))
