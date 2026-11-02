"""DR8 part B: isotropic equilibrium realizations by Eddington inversion on the unsoftened potential. Units Mpc, km/s, Msun. Taper: Kazantzidis form beyond R200, stated. kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os
import numpy as np
G = 4.30091e-9; HERE = os.path.dirname(os.path.abspath(__file__))
def setup(tag="A_c2b_refit"):
    S = json.load(open(os.path.join(HERE, "dr8_setup_1e12.json")))[tag]; D = json.load(open(os.path.join(os.path.dirname(HERE), "LC1_live_contraction", "lc1_setup.json"))); return dict(M2=S["M2"], R2=S["R2_kpc"] * 1e-3, r0=S["r0_kpc"] * 1e-3, Md=D["Md"], Rd=D["Rd_kpc"] * 1e-3, c_nfw=12.95)
def rho_inner(kind, r, S):
    if kind == "core": return (1 + (r / S["r0"]) ** 2) ** -1.5
    rs = S["R2"] / S["c_nfw"]; y = r / rs; return 1 / (y * (1 + y) ** 2)
def rho_shape(kind, r, S, rdec=0.1):
    """Shape, unnormalised: inner profile to R200, continuous value and slope beyond."""
    R2 = S["R2"]; rd = rdec * R2; h = 1e-5; gam = (math.log(rho_inner(kind, R2 * (1 + h), S)) - math.log(rho_inner(kind, R2 * (1 - h), S))) / (2 * h); eps = gam + R2 / rd; o = rho_inner(kind, r, S); m = r > R2
    o = np.where(m, rho_inner(kind, R2, S) * (r / R2) ** eps * np.exp(-(r - R2) / rd), o); return o
class Model:
    """rho(r) on a log grid; M, Psi (relative to the edge), f(E) by the Abel form, f = d/dE of the integral of drho/dPsi / sqrt(E - Psi), / (sqrt 8 pi^2)."""
    def __init__(self, rfun, Mnorm_fun, rmin, rmax, n=6000, ne=1500):
        self.r = r = np.geomspace(rmin, rmax, n); lr = np.log(r); dl = lr[1] - lr[0]; rho = rfun(r); k = 4 * np.pi * r ** 3 * rho; M = np.empty(n); M[0] = 4 / 3 * np.pi * rmin ** 3 * rho[0]; M[1:] = M[0] + np.cumsum(0.5 * (k[1:] + k[:-1])) * dl; c = Mnorm_fun(r, M); self.rho = rho = rho * c; self.M = M = M * c; self.c = c; self.Mtot = M[-1]
        I = G * M / r; ex = 4 * np.pi * r ** 2 * rho * G  # dPsi/dlnr = -G M / r
        tail = np.zeros(n); tail[:-1] = np.cumsum((I[:-1] + I[1:])[::-1] * 0.5 * dl)[::-1]; self.Psi = tail  # zero at the edge, bound inside the cut
        pa = self.Psi[::-1]; ra = rho[::-1]; pa = np.maximum.accumulate(pa); keep = np.concatenate(([True], np.diff(pa) > 0)); pa, ra = pa[keep], ra[keep]; self.pa, self.ra = pa, ra
        drdp = np.diff(ra) / np.diff(pa); E = pa[np.unique(np.linspace(1, len(pa) - 1, ne).astype(int))]; self.E = E; ne = len(E); Gv = np.empty(ne)  # E on the radial grid, so a cusp's top is resolved
        for j, e in enumerate(E):
            k_ = np.searchsorted(pa, e, side="right") - 1; q = np.sqrt(np.maximum(e - pa[:k_ + 1], 0.0)); q2 = np.concatenate((q, [0.0])) if k_ + 1 < len(pa) else q; s = q2[:-1] - q2[1:]; Gv[j] = 2 * np.sum(drdp[:len(s)] * s)
        self.f = np.gradient(Gv, E) / (math.sqrt(8) * np.pi ** 2); self.fmin_rel = float(self.f.min() / self.f.max())
    def f_at(self, e):
        return np.exp(np.interp(np.log(np.maximum(e, self.E[0])), np.log(self.E), np.log(np.maximum(self.f, 1e-300))))
    def rho_from_f(self, psi):
        O = []
        for p in psi:
            th = np.linspace(0, np.pi / 2, 800); e = p * np.sin(th) ** 2; O.append(4 * np.pi * np.trapz(self.f_at(e) * math.sqrt(2 * p) * np.cos(th) * 2 * p * np.sin(th) * np.cos(th), th))
        return np.array(O)
    def sample(self, N, seed, ulim=1.0):
        rng = np.random.default_rng(seed); r = np.exp(np.interp(ulim * rng.random(N), self.M / self.M[-1], np.log(self.r))); psi = np.interp(np.log(r), np.log(self.r), self.Psi); pt = np.geomspace(psi.min(), psi.max() * 1.0001, 300); mx = []
        for p in pt: e = p * np.linspace(0, 1, 400)[1:-1]; v2 = 2 * (p - e); mx.append(np.max(v2 * self.f_at(e)))
        mx = np.exp(np.interp(np.log(psi), np.log(pt), np.log(mx))) * 1.05; v = np.zeros(N); todo = np.arange(N)
        while len(todo):
            vm = np.sqrt(2 * psi[todo]); tr = vm * rng.random(len(todo)); e = psi[todo] - 0.5 * tr * tr; ok = rng.random(len(todo)) * mx[todo] < tr * tr * self.f_at(e); v[todo[ok]] = tr[ok]; todo = todo[~ok]
        def iso(n): u = rng.standard_normal((n, 3)); return u / np.linalg.norm(u, axis=1)[:, None]
        x = r[:, None] * iso(N); vv = v[:, None] * iso(N); return x - x.mean(0), vv - vv.mean(0)
def build(kind, S, N, seed, rdec=0.1):
    """Particles carry M_sim: cold M(<R200) = M2 at the end, plus M_d now. Returns x, v, m, Msim, model."""
    R2 = S["R2"]
    def norm(r, M): return S["M2"] / float(np.interp(math.log(R2), np.log(r), M))
    Mod = Model(lambda r: rho_shape(kind, r, S, rdec), norm, 1e-3 * S["r0"] if kind == "core" else 1e-5 * R2, R2 + 10 * rdec * R2)
    Mc = Mod.Mtot; Msim = Mc + S["Md"]; fac = Msim / Mc
    def norm2(r, M): return fac * S["M2"] / float(np.interp(math.log(R2), np.log(r), M))
    Mod = Model(lambda r: rho_shape(kind, r, S, rdec), norm2, 1e-3 * S["r0"] if kind == "core" else 1e-5 * R2, R2 + 10 * rdec * R2)
    x, v = Mod.sample(N, seed); return x, v, Mod.Mtot / N, Mod.Mtot, Mod
