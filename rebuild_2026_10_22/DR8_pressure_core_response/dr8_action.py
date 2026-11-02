"""DR8 part B: exact spherical isotropic adiabatic response. J_r and L conserved for each particle in a sequence of spherical potentials, disc monopole, self-consistent (Young 1980's scheme, particle form). Not fitted. kappa = 1/2 FITTED, unused; not theory closed."""
import numpy as np
G = 4.30091e-9
XGL, WGL = np.polynomial.legendre.leggauss(32); TH = 0.5 * np.pi * XGL; WT = 0.5 * np.pi * WGL; ST, CT = np.sin(TH), np.cos(TH)
class Pot:
    def __init__(self, rg, Mg):
        self.rg, self.lg = rg, np.log(rg); self.M = Mg; dl = self.lg[1] - self.lg[0]; I = G * Mg / rg; tail = np.zeros(len(rg)); tail[:-1] = np.cumsum((I[:-1] + I[1:])[::-1] * 0.5 * dl)[::-1]; self.Phi = -(tail + G * Mg[-1] / rg[-1]); self.Lc = np.sqrt(np.maximum(G * Mg * rg, 1e-300)); self.Lcm = np.maximum.accumulate(self.Lc)
    def phi(self, r): return np.interp(np.log(r), self.lg, self.Phi)
    def turning(self, E, L):
        rc = np.exp(np.interp(np.log(np.maximum(L, 1e-300)), np.log(self.Lcm), self.lg)); W = lambda r: 2 * (E - self.phi(r)) - (L / r) ** 2
        def bis(a, b, sign):
            la, lb = np.log(a), np.log(b)
            for _ in range(46):
                m = 0.5 * (la + lb); inside = W(np.exp(m)) >= 0
                if sign > 0: la = np.where(inside, m, la); lb = np.where(inside, lb, m)
                else: lb = np.where(inside, m, lb); la = np.where(inside, la, m)
            return np.exp(0.5 * (la + lb))
        return bis(np.full_like(E, self.rg[0]), rc, -1), bis(rc, np.full_like(E, self.rg[-1]), +1), rc
    def nodes(self, E, L):
        ra, rb, _ = self.turning(E, L); rm, am = 0.5 * (ra + rb), 0.5 * (rb - ra); r = rm[:, None] + am[:, None] * ST; v2 = 2 * (E[:, None] - self.phi(r)) - (L[:, None] / r) ** 2; vr = np.sqrt(np.maximum(v2, 0.0)); return r, vr, am
    def Jr(self, E, L, chunk=8000):
        O = np.empty_like(E)
        for i in range(0, len(E), chunk): r, vr, am = self.nodes(E[i:i + chunk], L[i:i + chunk]); O[i:i + chunk] = (vr * am[:, None] * CT * WT).sum(1) / np.pi
        return O
    def Ec(self, L):
        rc = np.exp(np.interp(np.log(np.maximum(L, 1e-300)), np.log(self.Lcm), self.lg)); return self.phi(rc) + 0.5 * (L / rc) ** 2
def solve_E(P, J, L, Eguess=None, its=34):
    lo = P.Ec(L); hi = np.full_like(L, P.Phi[-1]); hi = np.maximum(hi, lo + 1e-6)
    for _ in range(its):
        m = 0.5 * (lo + hi); up = P.Jr(m, L) < J; lo = np.where(up, m, lo); hi = np.where(up, hi, m)
    return 0.5 * (lo + hi)
def occupancy(P, E, L, edges, chunk=8000):
    """Time-weighted cumulative count of orbits inside edges (log bins)."""
    H = np.zeros(len(edges) + 1)
    for i in range(0, len(E), chunk):
        r, vr, am = P.nodes(E[i:i + chunk], L[i:i + chunk]); w = am[:, None] * CT * WT / np.maximum(vr, 1e-12 * np.maximum(1.0, vr.max())); circ = am < 1e-6 * r.mean(1); w[circ] = WT; w = w / w.sum(1, keepdims=True); idx = np.searchsorted(edges, r.ravel()); np.add.at(H, idx, w.ravel())
    return np.cumsum(H)[:-1]
def respond(x, v, rg, Mi, Mb, frac, m, passes=10):
    """x, v: particles about the centre, in the start potential of total mass Mi(r) on rg. Mb(r): the disc's spherical mass at the end. frac: each particle's mass goes m -> m frac. Returns M_f(r) of the cold particles on rg, last relative change."""
    Pi = Pot(rg, Mi); r = np.sqrt((x * x).sum(1)); L = np.linalg.norm(np.cross(x, v), axis=1); E = Pi.phi(r) + 0.5 * (v * v).sum(1); J = Pi.Jr(E, L); Mf = Mi * frac; ch = 1.0
    for _ in range(passes):
        P = Pot(rg, Mf + Mb); Ef = solve_E(P, J, L); new = occupancy(P, Ef, L, rg) * m * frac; new = np.maximum.accumulate(new); new[-1] = max(new[-1], new[-2]); s = rg > rg[0] * 30; ch = float(np.max(np.abs(new[s] / np.maximum(Mf[s], 1e-300) - 1)[new[s] > 200 * m * frac])); Mf = 0.5 * (Mf + new)
    return Mf, ch, J, L
