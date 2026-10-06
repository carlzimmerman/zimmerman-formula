"""QUMOND field of the Sun in a uniform external Newtonian field g_Ne (z axis), solved exactly (no algebraic shortcut):
nabla^2 psi = div D,  D = nu(|G|/a0) G - g_sun - nu_e g_Ne,  G = g_sun + g_Ne;  the physical field is g_sun + nu_e g_Ne + grad psi (curl part of D discarded).
D is localised (-> 0 far away), so psi is solved by a Legendre multipole expansion:
  s_l(r) = (2l+1)/2 [ r^-2 d/dr(r^2 D_r,l) + r^-1 int sin(th) D_th P_l'(mu) dmu ],  D_r,l = int D_r P_l dmu
  psi_l = -[ r^(-l-1) int_0^r s_l r'^(l+2) dr' + r^l int_r^inf s_l r'^(1-l) dr' ]/(2l+1)
The Sun falls with nu_e g_Ne + (uniform l=1 gradient at r -> 0); the force on a test body relative to the Sun is grad psi(r) - grad psi(0).
Units AU, yr, GM_sun = 4 pi^2.  Q2 (Milgrom 2009 / Blanchet-Novak convention, Phi_Q = -(Q2/2) r^2 (mu^2 - 1/3)) = -3/5 int_0^inf s_2 r'^-1 dr'.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss, legval
from scipy.optimize import brentq
GM = 4 * np.pi**2
MS2 = (3.15576e7)**2 / 1.495978707e11
YR = 3.15576e7
def Pl(l, mu):
    c = np.zeros(l + 1); c[l] = 1; return legval(mu, c)
def dPl(l, mu):
    c = np.zeros(l + 1); c[l] = 1
    from numpy.polynomial.legendre import legder
    return legval(mu, legder(c)) if l > 0 else np.zeros_like(mu)
class Field:
    def __init__(self, nu1, a0_si, ge_obs_si=2.146e-10, L=8, Nr=6000, Nmu=256, rmin=1e-2, rmax=3e7):
        self.a0 = a0_si * MS2
        ye = brentq(lambda y: (1 + float(nu1(np.array(y)))) * y - ge_obs_si / a0_si, 1e-4, 1e3)
        self.ye, self.nue = ye, 1 + float(nu1(np.array(ye)))
        gNe = ye * self.a0
        r = np.geomspace(rmin, rmax, Nr); mu, wmu = leggauss(Nmu); st = np.sqrt(1 - mu**2)
        R, M = np.meshgrid(r, mu, indexing="ij")
        gs = -GM / R**2                                  # radial sun field
        Gr = gs + gNe * M; Gt = -gNe * np.sqrt(1 - M**2)  # g_Ne = gNe z-hat: z = mu r-hat - sin(th) th-hat
        Gn = np.sqrt(Gr**2 + Gt**2)
        n1 = nu1(Gn / self.a0)
        Dr = n1 * Gr - (self.nue - 1) * gNe * M
        Dt = n1 * Gt + (self.nue - 1) * gNe * np.sqrt(1 - M**2)
        self.r, self.L = r, L
        lnr = np.log(r)
        self.psi, self.dpsi, self.Iout0 = [], [], []
        for l in range(L + 1):
            Drl = (Dr * Pl(l, mu)[None, :]) @ wmu
            Dtl = (Dt * (st * dPl(l, mu))[None, :]) @ wmu
            sl = (2 * l + 1) / 2 * (np.gradient(r**2 * Drl, lnr) / r**3 + Dtl / r)
            fin = sl * r**(l + 3); fout = sl * r**(2 - l)            # integrands in d ln r
            Iin = np.concatenate([[0], np.cumsum(0.5 * (fin[1:] + fin[:-1]) * np.diff(lnr))])
            cum = np.concatenate([[0], np.cumsum(0.5 * (fout[1:] + fout[:-1]) * np.diff(lnr))]); Iout = cum[-1] - cum
            # inner boundary: s_l ~ const/r for the monopole near the Sun -> int_0^rmin s r^(l+2) dr negligible
            self.psi.append(-(r**(-l - 1) * Iin + r**l * Iout) / (2 * l + 1))
            self.dpsi.append(-(-(l + 1) * r**(-l - 2) * Iin + l * r**(l - 1) * Iout) / (2 * l + 1))
            self.Iout0.append(Iout[0])
        self.unif = -self.Iout0[1] / 3.0                # uniform z-gradient of psi_1 at r -> 0
        self.Q2 = -3.0 / 5.0 * self.Iout0[2] / YR**2     # s^-2
    def force(self, rv, zhat):
        """relative anomalous force (AU/yr^2) at positions rv[..., 3] (ecliptic), field axis zhat."""
        rn = np.linalg.norm(rv, axis=-1); mu = (rv @ zhat) / rn
        lr = np.log(rn); x = np.log(self.r)
        Fr = np.zeros_like(rn); Fmu = np.zeros_like(rn)
        for l in range(self.L + 1):
            dps = np.interp(lr, x, self.dpsi[l]); ps = np.interp(lr, x, self.psi[l])
            Fr += dps * Pl(l, mu); Fmu += ps / rn * dPl(l, mu)
        rh = rv / rn[..., None]
        # grad psi = Fr r-hat + (1/r) dpsi/dmu * grad(mu)*r = Fmu * (zhat - mu r-hat)
        F = Fr[..., None] * rh + Fmu[..., None] * (zhat - mu[..., None] * rh)
        return F - self.unif * zhat
