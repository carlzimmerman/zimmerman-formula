"""S3_v3_mw_seals: the lane's AQUAL disc solver (criteria FROZEN_CRITERIA.md §1, commit 8f6c6587e1).

Units: kpc, km/s, Msun; G = 4.30091e-6 kpc (km/s)^2 / Msun; a0 in (km/s)^2/kpc.  Phi < 0 with lap(Phi) = 4 pi G rho.
v3's static limit (E2, C4): AQUAL  div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b,  mu(x) = x/(1+x)
(spherical: nu1(y) = (1 + sqrt(1 + 4/y))/2).

* Axisymmetric (R, z) finite volume on a geometric grid, full z range (no mirror assumption), one cell centred on z = 0.
  Kacanov iteration (mu frozen per step, sparse LU) with Anderson acceleration.  Dirichlet values on the outer faces:
  isolated = exact spherical AQUAL potential of the total mass; EFE along +z = g_e z + linearised AQUAL far field
  -GM/(mu_e sqrt(1+L0) Rt), Rt = sqrt(R^2 + z^2/(1+L0)) (E2 aqual_axi's form).
* 3-D periodic FFT fixed point for the EFE at an arbitrary angle (E2 aqual_fft's iteration, re-implemented):
  F = F_N + F_e + P_L[(1 - mu(|F|)) F - (1 - mu_e) F_e], F = grad Phi, F_N interpolated from the axisymmetric Newtonian solve.
MUTATE (S3_MUTATE=1 or --mutate): mu == 1 inside the AQUAL solver (Newton).
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os
import sys
import math
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
import scipy.fft as sfft

np.seterr(all="ignore")
G = 4.30091e-6
KPC_M = 3.0856775814913673e19
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")


def a0u(a_si):
    """m/s^2 -> (km/s)^2/kpc"""
    return a_si * KPC_M / 1e6


A0 = {k: a0u(v) for k, v in A0_SI.items()}
MUTATE = os.environ.get("S3_MUTATE", "0") == "1" or "--mutate" in sys.argv
CACHE = os.environ.get("S3_CACHE_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache_final")   # not committed
os.makedirs(CACHE, exist_ok=True)
TAG = "_MUTATE" if MUTATE else ""


def mu_s(x):
    if MUTATE:
        return np.ones_like(np.asarray(x, float))
    x = np.asarray(x, float)
    return x / (1.0 + x)


def mu_true(x):
    x = np.asarray(x, float)
    return x / (1.0 + x)


def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def gtot_from_newton(eN):
    """total external field in units of a0 from the Newtonian e_N (spherical AQUAL = nu1)."""
    return float(nu1(eN) * eN) if eN > 0 else 0.0


def sph_aqual_potential(M, a0, r, r_ref):
    """spherical AQUAL potential of a point mass M (exact: g = nu1(GM/r^2/a0) GM/r^2), zero at r_ref."""
    r = np.asarray(r, float)
    out = np.empty_like(r)
    ref = np.log(r_ref)
    for k, rr in np.ndenumerate(r):
        lo, hi = sorted((np.log(rr), ref))
        lr = np.linspace(lo, hi, 4001)
        x = np.exp(lr)
        gN = G * M / x ** 2
        g = (nu1(gN / a0) if not MUTATE else 1.0) * gN
        val = np.trapz(g * x, lr)
        out[k] = val if np.log(rr) > ref else -val
    return out


# ----------------------------------------------------------------------------- grid
class Grid:
    def __init__(self, dR0, qR, Rmax, dz0, qz, Zmax):
        w, t, d = [], 0.0, dR0
        while t < Rmax:
            w.append(d); t += d; d *= qR
        self.dR = np.array(w)
        self.Re = np.concatenate([[0.0], np.cumsum(self.dR)])
        self.Rc = 0.5 * (self.Re[:-1] + self.Re[1:])
        zw, t, d = [], dz0 / 2, dz0 * qz
        while t < Zmax:
            zw.append(d); t += d; d *= qz
        zp = dz0 / 2 + np.cumsum(zw)
        self.ze = np.concatenate([-zp[::-1], [-dz0 / 2, dz0 / 2], zp])
        self.dz = np.diff(self.ze)
        self.zc = 0.5 * (self.ze[:-1] + self.ze[1:])
        self.jc = len(zw)
        assert abs(self.zc[self.jc]) < 1e-14
        nR, nz = len(self.Rc), len(self.zc)
        self.nR, self.nz = nR, nz
        self.V = self.Rc[:, None] * self.dR[:, None] * self.dz[None, :]           # 2 pi omitted
        self.AR = self.Re[1:-1, None] * self.dz[None, :]                           # interior R faces (nR-1, nz)
        self.dRc = np.diff(self.Rc)
        self.ARo = self.Re[-1] * self.dz
        self.dRo = self.Re[-1] - self.Rc[-1]
        self.AZ = (self.Rc * self.dR)[:, None] * np.ones((1, nz - 1))              # interior z faces (nR, nz-1)
        self.dzc = np.diff(self.zc)
        self.AZb = self.Rc * self.dR
        self.dzb = self.zc[0] - self.ze[0]
        self.dzt = self.ze[-1] - self.zc[-1]
        idx = np.arange(nR * nz).reshape(nR, nz)
        self.idx = idx
        rows = [idx.ravel(), idx[:-1].ravel(), idx[1:].ravel(), idx[:, :-1].ravel(), idx[:, 1:].ravel()]
        cols = [idx.ravel(), idx[1:].ravel(), idx[:-1].ravel(), idx[:, 1:].ravel(), idx[:, :-1].ravel()]
        rows, cols = np.concatenate(rows), np.concatenate(cols)
        n = nR * nz
        A = sp.csc_matrix((np.arange(1, len(rows) + 1, dtype=float), (rows, cols)), shape=(n, n))
        self._perm = (A.data - 1).astype(np.int64)
        self._A = A
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")

    def describe(self):
        return dict(nR=self.nR, nz=self.nz, Rmax=float(self.Re[-1]), Zmax=float(self.ze[-1]), dR0=float(self.dR[0]),
                    dz0=float(self.dz[self.jc]))

    # ---- boundary points
    def bpoints(self):
        return dict(R=(np.full(self.nz, self.Re[-1]), self.zc), B=(self.Rc, np.full(self.nR, self.ze[0])),
                    T=(self.Rc, np.full(self.nR, self.ze[-1])))

    def matrix(self, cR, cRo, cZ, cB, cT):
        diag = np.zeros((self.nR, self.nz))
        diag[:-1, :] -= cR; diag[1:, :] -= cR
        diag[:, :-1] -= cZ; diag[:, 1:] -= cZ
        diag[-1, :] -= cRo; diag[:, 0] -= cB; diag[:, -1] -= cT
        vals = np.concatenate([diag.ravel(), cR.ravel(), cR.ravel(), cZ.ravel(), cZ.ravel()])
        A = self._A.copy()
        A.data = vals[self._perm]
        return A

    def cell_derivs(self, Phi, PB, ge=0.0):
        PR, PBo, PT = PB["R"], PB["B"], PB["T"]
        dPz = np.empty_like(Phi)
        dPz[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (self.zc[2:] - self.zc[:-2])[None, :]
        dPz[:, 0] = (Phi[:, 1] - PBo) / (self.zc[1] - self.ze[0])
        dPz[:, -1] = (PT - Phi[:, -2]) / (self.ze[-1] - self.zc[-2])
        dPR = np.empty_like(Phi)
        dPR[1:-1] = (Phi[2:] - Phi[:-2]) / (self.Rc[2:] - self.Rc[:-2])[:, None]
        dPR[0] = (Phi[1] - Phi[0]) / (self.Rc[1] + self.Rc[0])
        dPR[-1] = (PR - Phi[-2]) / (self.Re[-1] - self.Rc[-2])
        if ge:
            dPz = dPz + ge
        return dPR, dPz

    def face_grads(self, Phi, PB, ge=0.0):
        """(normal, tangential) total gradient at every face; ge = a uniform extra d/dz (external field along z)."""
        dPR, dPz = self.cell_derivs(Phi, PB, ge)
        gR = ((Phi[1:] - Phi[:-1]) / self.dRc[:, None], 0.5 * (dPz[1:] + dPz[:-1]))
        gRo = ((PB["R"] - Phi[-1]) / self.dRo, dPz[-1])
        gZ = ((Phi[:, 1:] - Phi[:, :-1]) / self.dzc[None, :] + ge, 0.5 * (dPR[:, 1:] + dPR[:, :-1]))
        gB = ((Phi[:, 0] - PB["B"]) / self.dzb + ge, dPR[:, 0])
        gT = ((PB["T"] - Phi[:, -1]) / self.dzt + ge, dPR[:, -1])
        return gR, gRo, gZ, gB, gT

    def coeffs(self, Phi, PB, a0, mufun, ge=0.0):
        fg = self.face_grads(Phi, PB, ge)
        if mufun is None:
            m = [np.ones_like(n) for n, t in fg]
        else:
            m = [np.maximum(mufun(np.hypot(n, t) / a0), 1e-12) for n, t in fg]
        cR = self.AR / self.dRc[:, None] * m[0]
        cRo = self.ARo / self.dRo * m[1]
        cZ = self.AZ / self.dzc[None, :] * m[2]
        cB = self.AZb / self.dzb * m[3]
        cT = self.AZb / self.dzt * m[4]
        return cR, cRo, cZ, cB, cT

    def extra(self, c, ge):
        """per-cell net outward flux of the uniform part ge (z faces only): ge (A mu)_up - ge (A mu)_down."""
        cR, cRo, cZ, cB, cT = c
        up = np.zeros((self.nR, self.nz)); dn = np.zeros((self.nR, self.nz))
        up[:, :-1] = cZ * self.dzc[None, :]; up[:, -1] = cT * self.dzt
        dn[:, 1:] = cZ * self.dzc[None, :]; dn[:, 0] = cB * self.dzb
        return ge * (up - dn)

    def rhs(self, S, PB, c, ge=0.0):
        cR, cRo, cZ, cB, cT = c
        b = S.copy()
        if ge:
            b -= self.extra(c, ge)
        b[-1, :] -= cRo * PB["R"]
        b[:, 0] -= cB * PB["B"]
        b[:, -1] -= cT * PB["T"]
        return b

    def apply(self, Phi, PB, c, ge=0.0):
        """sum_f c_f (Phi_nb - Phi_c) per cell (+ the uniform part's flux if ge)."""
        cR, cRo, cZ, cB, cT = c
        out = np.zeros_like(Phi) if not ge else self.extra(c, ge)
        fl = cR * (Phi[1:] - Phi[:-1]); out[:-1] += fl; out[1:] -= fl
        fl = cZ * (Phi[:, 1:] - Phi[:, :-1]); out[:, :-1] += fl; out[:, 1:] -= fl
        out[-1] += cRo * (PB["R"] - Phi[-1])
        out[:, 0] += cB * (PB["B"] - Phi[:, 0])
        out[:, -1] += cT * (PB["T"] - Phi[:, -1])
        return out

    # ---- solves
    def newton(self, rho, PB):
        S = 4 * math.pi * G * rho * self.V
        c = self.coeffs(None if False else np.zeros((self.nR, self.nz)), PB, 1.0, None)
        A = self.matrix(*c)
        return splu(A).solve(self.rhs(S, PB, c).ravel()).reshape(self.nR, self.nz)

    def aqual(self, rho, a0, PB, Phi_init_N=None, PB_N=None, tol=1e-8, maxit=200, depth=5, mufun=None, verbose=False,
              ge=0.0, ye_a0=0.0):
        """Kacanov + Anderson.  Returns (phi, info); the total potential is phi + ge z (ge = total external field along z,
        ye_a0 = its Newtonian value, used only for the starting mu).  Start: mu from the algebraic field of the Newtonian solve."""
        mufun = mu_s if mufun is None else mufun
        S = 4 * math.pi * G * rho * self.V
        Snorm = float(np.sum(np.abs(S)))
        if Phi_init_N is not None:
            fg = self.face_grads(Phi_init_N, PB_N, ye_a0)
            m = []
            for n, t in fg:
                y = np.hypot(n, t) / a0
                m.append(np.maximum(mufun(nu1(y) * y), 1e-12))
            c = (self.AR / self.dRc[:, None] * m[0], self.ARo / self.dRo * m[1], self.AZ / self.dzc[None, :] * m[2],
                 self.AZb / self.dzb * m[3], self.AZb / self.dzt * m[4])
            x = splu(self.matrix(*c)).solve(self.rhs(S, PB, c, ge).ravel())
        else:
            c = self.coeffs(np.zeros((self.nR, self.nz)), PB, a0, None)
            x = splu(self.matrix(*c)).solve(self.rhs(S, PB, c, ge).ravel())
        X, Fh, hist = [], [], []
        res = np.inf
        for it in range(maxit):
            P = x.reshape(self.nR, self.nz)
            c = self.coeffs(P, PB, a0, mufun, ge)
            r = self.apply(P, PB, c, ge) - S
            res = float(np.sum(np.abs(r)) / Snorm)
            hist.append(res)
            if verbose:
                print(it, res, flush=True)
            if res < tol:
                break
            # round-off floor (AMENDMENT A2): stalled for 10 iterations at <= 1e-7
            if it >= 12 and res <= 1e-7 and min(hist[-10:]) >= 0.5 * min(hist[:-10]):
                break
            g = splu(self.matrix(*c)).solve(self.rhs(S, PB, c, ge).ravel())
            f = g - x
            X.append(x.copy()); Fh.append(f.copy())
            if len(X) > depth + 1:
                X.pop(0); Fh.pop(0)
            if len(X) > 1:
                dF = np.stack([Fh[k + 1] - Fh[k] for k in range(len(Fh) - 1)], axis=1)
                dX = np.stack([X[k + 1] - X[k] for k in range(len(X) - 1)], axis=1)
                gam, *_ = np.linalg.lstsq(dF, f, rcond=None)
                xn = x + f - (dX + dF) @ gam
                # safeguard: fall back to the plain Kacanov step if the accelerated residual is worse
                Pn = xn.reshape(self.nR, self.nz)
                rn = float(np.sum(np.abs(self.apply(Pn, PB, self.coeffs(Pn, PB, a0, mufun, ge), ge) - S)) / Snorm)
                if not np.isfinite(rn) or rn > res:
                    xn = g
                    X, Fh = [], []
                x = xn
            else:
                x = g
        return x.reshape(self.nR, self.nz), dict(iters=it + 1, residual=res, hist=hist, floor=bool(res >= tol))

    # ---- outputs
    def plane_gR(self, Phi):
        """dPhi/dR along the central row, at the midpoints between cell centres."""
        j = self.jc
        Rm = 0.5 * (self.Rc[1:] + self.Rc[:-1])
        return Rm, (Phi[1:, j] - Phi[:-1, j]) / self.dRc

    def vc2(self, Phi, R):
        Rm, g = self.plane_gR(Phi)
        R = np.asarray(R, float)
        return R * np.interp(np.log(R), np.log(Rm), g)

    def gR_plane(self, Phi, R):
        Rm, g = self.plane_gR(Phi)
        return np.interp(np.log(np.asarray(R, float)), np.log(Rm), g)

    def interp2(self, F, R, z):
        """bilinear interpolation of a cell-centred field."""
        from scipy.interpolate import RegularGridInterpolator
        it = RegularGridInterpolator((self.Rc, self.zc), F, bounds_error=False, fill_value=None)
        return it(np.stack([np.asarray(R, float), np.asarray(z, float)], -1))

    def kz_sym(self, Phi, PB, R, z):
        """mirror-symmetric vertical gradient 0.5[dPhi/dz(R,|z|) - dPhi/dz(R,-|z|)] (removes a uniform field along z)."""
        _, dPz = self.cell_derivs(Phi, PB)
        R = np.asarray(R, float); z = np.abs(np.asarray(z, float))
        return 0.5 * (self.interp2(dPz, R, z) - self.interp2(dPz, R, -z))

    def lap_density(self, Phi, PB):
        """rho_dyn = discrete lap(Phi)/(4 pi G) per cell."""
        c = self.coeffs(Phi, PB, 1.0, None)
        return self.apply(Phi, PB, c) / (4 * math.pi * G * self.V)

    def grad_cells(self, Phi, PB):
        return self.cell_derivs(Phi, PB)


# ----------------------------------------------------------------------------- boundary values
def bc_newton(grid, M):
    out = {}
    for k, (R, z) in grid.bpoints().items():
        out[k] = -G * M / np.hypot(R, z)
    return out


def bc_aqual_iso(grid, M, a0):
    rref = float(grid.Re[-1])
    out = {}
    for k, (R, z) in grid.bpoints().items():
        r = np.hypot(R, z)
        # vectorised: integrate on a common log grid
        lr = np.linspace(np.log(r.min()) - 1e-9, np.log(max(r.max(), rref)) + 1e-9, 20001)
        x = np.exp(lr)
        gN = G * M / x ** 2
        g = (nu1(gN / a0) if not MUTATE else 1.0) * gN
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] * x[1:] + g[:-1] * x[:-1]) * np.diff(lr))])
        pr = np.interp(np.log(r), lr, cum)
        out[k] = pr - np.interp(np.log(rref), lr, cum)
    return out


def bc_aqual_efe_z(grid, M, a0, eN):
    """uniform external field along +z: returns the far-field values of phi (Phi = phi + ge z) and ge = nu1(eN) eN a0."""
    xe = gtot_from_newton(eN) if not MUTATE else eN
    ge = xe * a0
    if MUTATE:
        mue, L0 = 1.0, 0.0
    else:
        mue, L0 = xe / (1 + xe), 1.0 / (1 + xe)
    out = {}
    for k, (R, z) in grid.bpoints().items():
        Rt = np.sqrt(R ** 2 + z ** 2 / (1 + L0))
        out[k] = -G * M / (mue * math.sqrt(1 + L0) * Rt)          # phi only; the total is phi + ge z
    return out, ge


# ----------------------------------------------------------------------------- mass helpers
def total_mass(grid, rho):
    return float(2 * math.pi * np.sum(rho * grid.V))


def freeman_v2(M, Rd, R):
    from scipy.special import i0, i1, k0, k1
    y = np.asarray(R, float) / (2 * Rd)
    return 2 * G * M / Rd * y * y * (i0(y) * k0(y) - i1(y) * k1(y))


# ----------------------------------------------------------------------------- 3-D EFE (periodic FFT)
class EFE3D:
    """F = grad Phi.  F = FN + Fe + d,  d = P_L[(1 - mu(|F|))F - (1 - mu_e)Fe]."""

    def __init__(self, N, Lbox, FN_func, Fe_vec, a0, mufun=None):
        self.N, self.L = N, Lbox
        self.dx = Lbox / N
        self.xs = (np.arange(N) - N / 2 + 0.5) * self.dx
        self.a0 = a0
        self.mufun = mu_s if mufun is None else mufun
        k = (2 * np.pi * sfft.fftfreq(N, self.dx))
        kz = (2 * np.pi * sfft.rfftfreq(N, self.dx))
        self.k = (k[:, None, None].astype(np.float32), k[None, :, None].astype(np.float32), kz[None, None, :].astype(np.float32))
        k2 = self.k[0] ** 2 + self.k[1] ** 2 + self.k[2] ** 2
        k2[0, 0, 0] = 1.0
        self.ik2 = (1.0 / k2).astype(np.float32)
        self.Fe = np.asarray(Fe_vec, float)
        self.xe = float(np.linalg.norm(self.Fe)) / a0
        self.ome = float(1.0 - self.mufun(np.array([self.xe]))[0])
        self.FN = np.empty((3, N, N, N), dtype=np.float32)
        Y, Z = np.meshgrid(self.xs, self.xs, indexing="ij")
        for i in range(N):
            fx, fy, fz = FN_func(np.full_like(Y, self.xs[i]), Y, Z)
            self.FN[0, i], self.FN[1, i], self.FN[2, i] = fx, fy, fz
        self.d = np.zeros_like(self.FN)

    def project(self, S):
        D = sfft.rfftn(S[0], workers=1) * self.k[0]
        D += sfft.rfftn(S[1], workers=1) * self.k[1]
        D += sfft.rfftn(S[2], workers=1) * self.k[2]
        D *= self.ik2
        D[0, 0, 0] = 0.0
        for c in range(3):
            S[c] = sfft.irfftn(D * self.k[c], s=(self.N,) * 3, workers=1)

    def G_map(self, d):
        """one fixed-point map d -> P_L[(1 - mu(|F|))F - (1 - mu_e)Fe]."""
        S = np.empty_like(self.FN)
        for i in range(self.N):
            tx = self.FN[0, i] + self.Fe[0] + d[0, i]
            ty = self.FN[1, i] + self.Fe[1] + d[1, i]
            tz = self.FN[2, i] + self.Fe[2] + d[2, i]
            mag = np.sqrt(tx * tx + ty * ty + tz * tz) / self.a0
            f = 1.0 - self.mufun(mag)
            S[0, i] = f * tx - self.ome * self.Fe[0]
            S[1, i] = f * ty - self.ome * self.Fe[1]
            S[2, i] = f * tz - self.ome * self.Fe[2]
        self.project(S)
        return S

    def solve(self, maxit=800, tol=2e-6, probe=None, verbose=False):
        """plain fixed point (contraction 1/(1+x)^2 <= 1); float32 storage, so the stop rule is on the probe values
        (in-plane fields at the radii used): relative change < tol over 5 consecutive iterations."""
        hist, ok = [], 0
        prev = None
        for it in range(maxit):
            self.d = self.G_map(self.d)
            val = np.asarray(probe(self)) if probe else np.array([float(np.max(np.abs(self.d)))])
            ch = float(np.max(np.abs(val - prev) / np.maximum(np.abs(val), 1e-30))) if prev is not None else np.inf
            hist.append(ch)
            if verbose and it % 20 == 0:
                print(it, ch, flush=True)
            ok = ok + 1 if ch < tol else 0
            if ok >= 5:
                break
            prev = val
        return dict(iters=it + 1, last_change=hist[-1], converged=bool(ok >= 5))

    def d_at(self, P):
        """trilinear interpolation of d at points P (n, 3)."""
        P = np.asarray(P, float)
        u = (P - self.xs[0]) / self.dx
        i0 = np.clip(np.floor(u).astype(int), 0, self.N - 2)
        t = u - i0
        out = np.zeros((len(P), 3))
        for dx_ in (0, 1):
            for dy_ in (0, 1):
                for dz_ in (0, 1):
                    w = (t[:, 0] if dx_ else 1 - t[:, 0]) * (t[:, 1] if dy_ else 1 - t[:, 1]) * (t[:, 2] if dz_ else 1 - t[:, 2])
                    ii, jj, kk = i0[:, 0] + dx_, i0[:, 1] + dy_, i0[:, 2] + dz_
                    for c in range(3):
                        out[:, c] += w * self.d[c, ii, jj, kk]
        return out


# ----------------------------------------------------------------------------- child-process batches (RSS hygiene)
def run_batch(module, func, jobs, batch=4, here=None):
    """Run module.func(**job) for each job in fresh single-threaded child processes, `batch` jobs per child (SuperLU's
    allocations fragment the heap, so each process's peak RSS grows with the number of distinct factorizations).
    Returns (results, max child peak RSS in MB)."""
    import subprocess
    import json as _json
    here = here or os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", S3_CHILD="1")
    code = ("import sys, json, resource; sys.path.insert(0, %r); import %s as M; jobs = json.loads(sys.stdin.read()); "
            "out = [M.%s(**j) for j in jobs]; "
            "print('@@' + json.dumps(dict(res=out, rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)))" % (here, module, func))
    res, peak = [], 0.0
    for i in range(0, len(jobs), batch):
        chunk = jobs[i:i + batch]
        p = subprocess.run([sys.executable, "-c", code] + (["--mutate"] if MUTATE else []), input=_json.dumps(chunk),
                           capture_output=True, text=True, env=env)
        if p.returncode != 0:
            raise RuntimeError(p.stderr[-3000:])
        d = _json.loads([ln for ln in p.stdout.splitlines() if ln.startswith("@@")][-1][2:])
        res += d["res"]
        peak = max(peak, d["rss"])
    return res, peak
