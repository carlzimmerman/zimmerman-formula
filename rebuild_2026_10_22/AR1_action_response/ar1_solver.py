"""AR1: exact spherical isotropic adiabatic response on a deterministic orbit grid (FROZEN_CRITERIA.md). J_r and L conserved per orbit, cold mass per orbit conserved, self-consistent (Young's scheme). Start: isotropic Eddington DF of (1 + F) rho_0, tapered as DR8. Same physics as DR8's dr8_action.py, with quadrature in place of particles. Units free: everything is normalised to the edge and M0(edge), G = 1. No fitted number. kappa = 1/2 FITTED, unused; not theory closed."""
import math
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
NE, NY, NT = 192, 32, 64; DL = 0.005; PASSES = 16; DAMP = 0.5; TOL = 2e-3; S8 = math.sqrt(8) * math.pi ** 2
class Grid:
    def __init__(self, lg, Mt):
        self.lg = lg; self.l0 = lg[0]; self.dl = lg[1] - lg[0]; self.n = len(lg); self.x = np.exp(lg); self.Mt = Mt; I = Mt / self.x; t = np.zeros(self.n); t[:-1] = np.cumsum((I[:-1] + I[1:])[::-1] * 0.5 * self.dl)[::-1]; self.phi = -(t + Mt[-1] / self.x[-1]); self.Lc = np.sqrt(np.maximum(Mt * self.x, 1e-300)); self.Lm = np.maximum.accumulate(self.Lc) * (1 + 1e-12 * np.arange(self.n)); self.Ecg = self.phi + 0.5 * Mt / self.x
    def at(self, lnr):
        t = (lnr - self.l0) / self.dl; i = np.clip(t.astype(int), 0, self.n - 2); w = t - i; return (1 - w) * self.phi[i] + w * self.phi[i + 1]
    def ic(self, L): return np.clip(np.searchsorted(self.Lm, L), 0, self.n - 1)
    def lnc(self, L):
        i = np.clip(np.searchsorted(self.Lm, L), 1, self.n - 1); a, b = self.Lm[i - 1], self.Lm[i]; return self.lg[i - 1] + self.dl * np.clip((L - a) / np.maximum(b - a, 1e-300), 0, 1)
    def Ec(self, L): lc = self.lnc(L); return self.at(lc) + 0.5 * (L * np.exp(-lc)) ** 2
    def turning(self, E, L):
        """Root of W = 2(E - phi) - L^2/r^2 either side of r_c, integer bisection on the grid, then linear in ln r."""
        L2 = L * L; ic = self.ic(L); W = lambda i: 2 * (E - self.phi[i]) - L2 * np.exp(-2 * self.lg[i])
        def bis(lo, hi, inner):
            for _ in range(11):
                m = (lo + hi) // 2; pos = W(m) >= 0
                if inner: hi = np.where(pos, m, hi); lo = np.where(pos, lo, m)
                else: lo = np.where(pos, m, lo); hi = np.where(pos, hi, m)
            a, b = W(lo), W(hi); return self.lg[lo] + self.dl * (hi - lo) * np.clip(a / np.where(a - b == 0, 1.0, a - b), 0, 1)
        nl = np.zeros_like(ic); nh = np.full_like(ic, self.n - 1); Ic = np.maximum(ic, 1); Ih = np.minimum(Ic, self.n - 2)
        return np.exp(bis(nl, Ih, True)), np.exp(bis(Ih, nh, False))
class Nodes:
    def __init__(self, nT):
        xg, wg = np.polynomial.legendre.leggauss(nT); self.th = 0.5 * np.pi * xg; self.wt = 0.5 * np.pi * wg; self.st = np.sin(self.th); self.ct = np.cos(self.th); self.nT = nT
        # segment edges in sin(theta), for spreading each node's time over its piece of the orbit
        ed = np.r_[-np.pi / 2, 0.5 * (self.th[1:] + self.th[:-1]), np.pi / 2]; self.se = np.sin(ed)
def orbit(g, E, L, N):
    ra, rb = g.turning(E, L); rm, am = 0.5 * (ra + rb), 0.5 * (rb - ra); r = rm[:, None] + am[:, None] * N.st; lnr = np.log(r); v2 = 2 * (E[:, None] - g.at(lnr)) - (L[:, None] / r) ** 2; vr = np.sqrt(np.maximum(v2, 0.0)); vfl = np.maximum(vr, 1e-3 * vr.max(1, keepdims=True) + 1e-30); ac = am[:, None] * N.ct * N.wt; J = (vr * ac).sum(1) / np.pi; dt = ac / vfl; T = 2 * dt.sum(1); return J, T, dt, rm, am
def solve_E(g, Jt, L, N, E0=None, maxit=30, tol=2e-4):
    lo = g.Ec(L); hi = np.full_like(L, g.phi[-1]); hi = np.maximum(hi, lo + 1e-9 * np.abs(lo)); E = 0.5 * (lo + hi) if E0 is None else np.clip(E0, lo, hi); fl = 1e-5 * Jt.max()
    for k in range(maxit):
        J, T, _, _, _ = orbit(g, E, L, N); er = J - Jt; up = er < 0; lo = np.where(up, E, lo); hi = np.where(up, hi, E)
        if np.all(np.abs(er) <= np.maximum(tol * Jt, fl)): break
        En = E - er * 2 * np.pi / np.maximum(T, 1e-300); bad = (En <= lo) | (En >= hi); E = np.where(bad, 0.5 * (lo + hi), En)
    return E
def deposit(g, E, L, w, N):
    """Cumulative mass of the orbits on g's grid, each node's time spread uniformly in ln r over its segment. Returns M(<x_i)."""
    _, T, dt, rm, am = orbit(g, E, L, N); m = w[:, None] * 2 * dt / np.maximum(T, 1e-300)[:, None]; re = rm[:, None] + am[:, None] * N.se; le = np.log(np.maximum(re, g.x[0])); ta = (le[:, :-1] - g.l0) / g.dl; tb = (le[:, 1:] - g.l0) / g.dl; wid = np.maximum(tb - ta, 1e-3); s = (m / wid).ravel(); H = np.zeros(g.n + 2)
    for tt, sg in ((ta.ravel(), s), ((ta + wid).ravel(), -s)):
        t = np.clip(tt, 0, g.n); i = t.astype(int); fr = t - i; H += np.bincount(i, sg * (1 - fr), g.n + 2) + np.bincount(i + 1, sg * fr, g.n + 2)
    return np.cumsum(np.cumsum(H))[: g.n]
class Start:
    """Normalised start: cold M on the grid, DF, orbit grid. Depends on M0's shape and on nothing else, so Mb and F scale in later."""
    def __init__(s, r, M0, rdec=0.1, nE=NE, nY=NY, nT=NT, dl=DL, thin=None):
        inc = np.where(np.diff(M0) > 0)[0]; n = int(inc[-1]) + 1; s.edge = float(r[n]); s.Me = float(M0[n]); s.n = n; x = r[: n + 1] / s.edge; y = M0[: n + 1] / s.Me; pos = y > 0; lx = np.log(x[pos]); ly = np.log(y[pos]); xlo = min(float(x[pos][0]) / 3, 1e-3); s.xlo = xlo; lg = np.arange(math.log(xlo), math.log(4.0) + dl, dl); s.dl = dl; s.lg = lg; X = np.exp(lg); sl0 = (ly[1] - ly[0]) / (lx[1] - lx[0]); ins = lg <= 0; Mg = np.empty_like(lg); keep = np.zeros_like(lx, bool); keep[np.unique(np.searchsorted(lx, np.arange(lx[0], lx[-1], thin or 0.25 * dl)))] = True; keep[-1] = True; keep[-2] = False if thin else keep[-2]; lxk, lyk = lx[keep], ly[keep]; sp = CubicSpline(lxk, lyk); ds = sp.derivative(); li = np.where(lg[ins] < lx[0], ly[0] + sl0 * (lg[ins] - lx[0]), sp(np.minimum(lg[ins], 0.0))); dM = np.where(lg[ins] < lx[0], sl0, ds(np.minimum(lg[ins], 0.0))); Mg[ins] = np.exp(li)
        if np.any(dM < 0): sp = PchipInterpolator(lxk, lyk); ds = sp.derivative(); li = np.where(lg[ins] < lx[0], ly[0] + sl0 * (lg[ins] - lx[0]), sp(np.minimum(lg[ins], 0.0))); dM = np.where(lg[ins] < lx[0], sl0, ds(np.minimum(lg[ins], 0.0))); Mg[ins] = np.exp(li)
        rho = dM * Mg[ins] / (4 * np.pi * X[ins] ** 3); j = int(ins.sum()) - 1; k = max(j - 6, 1); d1 = float(ds(0.0)); d2 = float(ds.derivative()(0.0)); gam = d2 / max(d1, 1e-300) + d1 - 3.0; eps = gam + 1 / rdec; tail = X > 1; rt = rho[j] * X ** eps * np.exp(-(X - 1) / rdec); rr = np.zeros_like(X); rr[ins] = rho; rr[tail] = rt[tail]; s.nout = int(np.searchsorted(X, 2.0)); rr[s.nout + 1:] = 0.0
        Mg[~ins] = Mg[j] + np.cumsum(4 * np.pi * (rr[j:-1] * X[j:-1] ** 3 + rr[j + 1:] * X[j + 1:] ** 3) * 0.5 * dl)[: int((~ins).sum())]; s.M = np.maximum.accumulate(Mg); s.rho = rr; s.rdec = rdec; s.N = Nodes(nT); s.nE, s.nY = nE, nY; s.Mtot = float(s.M[s.nout]); s._df(); s._orbits()
    def _df(s, ne=400):
        """Eddington on the unit (1 + F = 1) start. f scales through (1 + F) with the same shape; orbits are in scaled form."""
        g = Grid(s.lg[: s.nout + 1], s.M[: s.nout + 1]); psi = -(g.phi - g.phi[-1]); pa = psi[::-1]; ra = s.rho[: s.nout + 1][::-1]; keep = np.r_[True, np.diff(pa) > 0]; pa, ra = pa[keep], ra[keep]; dr = np.diff(ra) / np.diff(pa); E = pa[np.unique(np.linspace(1, len(pa) - 1, ne).astype(int))]; ne = len(E); G = np.empty(ne)  # on the radial grid, so the top of the well is resolved
        for j, e in enumerate(E):
            q = np.sqrt(np.maximum(e - pa, 0.0)); G[j] = 2 * np.sum(dr * (q[:-1] - q[1:]))
        f = np.gradient(G, E) / S8; s.fneg = float(np.sum(f < 0) / ne); s.fneg_rel = float(max(0.0, -f.min() / max(f.max(), 1e-300))); s.fraw = f; s.Etab = E; s.ftab = np.maximum(f, 1e-300); s.g0 = g; s.psi = psi; s.pmax = float(pa[-1])
    def fE(s, e): return np.exp(np.interp(e, s.Etab, np.log(s.ftab)))
    def _orbits(s):
        g = s.g0; Ecg = lambda l: g.at(l) + 0.5 * np.exp(np.interp(l, g.lg, np.log(g.Mt))) * np.exp(-l); lb = g.lg[int(np.argmax(Ecg(g.lg) >= g.phi[-1]))]; ed = np.linspace(g.lg[0], lb, s.nE + 1); Ea = Ecg(ed); dE = np.abs(np.diff(Ea)); lc = 0.5 * (ed[1:] + ed[:-1]); E = Ecg(lc); Lc = np.sqrt(np.exp(np.interp(lc, g.lg, np.log(g.Mt))) * np.exp(lc)); yg, wy = np.polynomial.legendre.leggauss(s.nY); yg = 0.5 * (yg + 1); wy = 0.5 * wy; Ee = np.repeat(E, s.nY); Ll = np.repeat(Lc, s.nY) * np.tile(yg, s.nE); J, T, _, _, _ = orbit(g, Ee, Ll, s.N); w = 8 * np.pi ** 2 * np.repeat(Lc ** 2 * dE, s.nY) * np.tile(yg * wy, s.nE) * T * s.fE(np.maximum(-(Ee - g.phi[-1]), 0.0)); s.E, s.L, s.J, s.w_raw = Ee, Ll, J, w; s.w = w * s.Mtot / w.sum(); s.Fm = float(w.sum() / s.Mtot); s.mneg = float(w[np.interp(np.maximum(-(Ee - g.phi[-1]), 0.0), s.Etab, s.fraw) <= 0].sum() / max(w.sum(), 1e-300)); s.dep0 = None
def respond(S, lg, Mb, F, passes=PASSES, damp=DAMP, tol=TOL):
    """Mb on S.lg (normalised to S.Me, x normalised to edge), constant beyond the edge. Start potential (1 + F) M. Returns Mf, Q, change."""
    q = math.sqrt(1 + F); Li, Ji = S.L * q, S.J * q; gs = Grid(lg, S.M * (1 + F)); Ei = (S.E - S.g0.phi[-1]) * (1 + F) + gs.phi[S.nout]; dep0 = deposit(gs, Ei, Li, S.w, S.N); res = dep0 > 1e-8 * S.Mtot; i0 = int(np.argmax(res)); Mf = S.M.copy(); E = Ei; ch = 1.0
    for it in range(passes):
        g = Grid(lg, Mf + Mb); E = solve_E(g, Ji, Li, S.N, E0=E); d = deposit(g, E, Li, S.w, S.N); Q = np.where(res, d / np.maximum(dep0, 1e-300), d[i0] / max(dep0[i0], 1e-300)); new = np.maximum.accumulate(S.M * Q); sel = (new > 1e-4 * S.Mtot) & (lg <= math.log(2.0)); ch = float(np.max(np.abs(new[sel] / np.maximum(Mf[sel], 1e-300) - 1))); Mf = damp * Mf + (1 - damp) * new
        if ch < tol and it >= 3: break
    return Mf, ch, it + 1, float(np.max(np.abs(d[res][-40:] / dep0[res][-40:] - 1))) if F == 0 else 0.0
_CACHE = {}
def act_contract(r, Mb, M0, F, gnedin=None, rdec=0.1, nE=NE, nY=NY, nT=NT, dl=DL, st=None, stats=None, cap=True):
    """Same call as X39's contract: M_cold,f on r. r ascending, Mb and M0 cumulative on r."""
    assert gnedin is None
    S = st or Start(r, M0, rdec, nE, nY, nT, dl); lx = np.log(r / S.edge); lg = S.lg; mb = np.maximum(Mb, 0.0) / S.Me; pos = mb > 0
    if pos.any():
        lmb = np.interp(lg, lx[pos], np.log(mb[pos]), right=np.log(mb[pos][np.searchsorted(lx[pos], 0.0, side="right") - 1] if (lx[pos] <= 0).any() else mb[pos][0])); i0 = np.searchsorted(lg, lx[pos][0]); Mbg = np.exp(lmb); Mbg[:i0] = mb[pos][0] * np.exp(3 * (lg[:i0] - lx[pos][0])); Mbg = np.maximum.accumulate(np.where(lg > 0, np.exp(float(np.interp(0.0, lx[pos], np.log(mb[pos])))), Mbg))
    else: Mbg = np.zeros_like(lg)
    Mf, ch, its, _ = respond(S, lg, Mbg, float(F)); o = M0 * np.exp(np.interp(np.minimum(lx, 0.0), lg, np.log(np.maximum(Mf, 1e-300) / np.maximum(S.M, 1e-300))))
    out = lx > 0
    if out.any(): o[out] = np.exp(np.interp(lx[out], lg, np.log(np.maximum(Mf, 1e-300)))) * S.Me
    if cap: o = np.minimum(o, S.Me)
    if stats is not None: stats.update(calls=stats.get("calls", 0) + 1, ch=max(stats.get("ch", 0.0), ch), chbad=stats.get("chbad", 0) + int(ch > 1e-2), its=max(stats.get("its", 0), its), fneg=max(stats.get("fneg", 0.0), S.mneg), Fm=max(stats.get("Fm", 0.0), abs(S.Fm - 1)))
    return np.maximum.accumulate(o), ch, its
