"""FN3 3D forward model of an [OII] cutout and its fitter. Criteria: FROZEN_CRITERIA.md (c6640225c2); conventions:
AMENDMENT_A1.md (gas pi G Sigma r, drift D1 x scale, MGE q 0.15, sigma^2 = sigma0^2 + (h v_c/R)^2, h = 0.15 r_half).

Geometry: a thick Sersic disc, Gaussian in height (sigma_z = 0.15 r_half), integrated along each line of sight with
Gauss-Hermite nodes in height. Disc coordinates for sky offsets (x_maj, y_min) and height Z:
X = x_maj, Y = y_min / cos i + Z tan i, R = sqrt(X^2 + Y^2); v_los = v_perp(R) (X/R) sin i.
Line: [OII] 3726.2, 3728.9 (the survey's line list), channel-integrated Gaussians, MUSE UDF LSF, Moffat PSF.
kappa = 1/2 FITTED; not theory closed.
"""
import math

import numpy as np
from scipy import optimize, special

import fn3_common as C

L1, L2 = 3726.2, 3728.9
SQ2 = math.sqrt(2.0)


def muse_lsf_fwhm(lam):
    """MUSE UDF line-spread FWHM in Angstrom (Bacon et al. 2017)."""
    return 5.866e-8 * lam ** 2 - 9.187e-4 * lam + 6.040


# ---------------------------------------------------------------- mass models (1D, kpc and km/s)
_MGE_CACHE = {}


def mge_unit(n):
    """v^2 per unit mass of an MGE Sersic disc with R_e = 1 kpc, q 0.15, on a fixed dimensionless grid."""
    key = round(float(n), 3)
    if key not in _MGE_CACHE:
        sig, frac, _ = C.sersic_mge(key)
        x = np.geomspace(1e-3, 60.0, 260)
        _MGE_CACHE[key] = (x, C.mge_vc2(x, sig, frac, 1.0, 0.15))
    return _MGE_CACHE[key]


def disc_v2(R, M, Re, n):
    x, f = mge_unit(n)
    u = np.asarray(R, float) / Re
    out = np.interp(u, x, f, left=0.0)
    far = u > x[-1]
    out = np.where(far, f[-1] * x[-1] / np.maximum(u, 1e-9), out)   # Keplerian beyond the grid
    return M / Re * out


class LawMass:
    """the law on stars + H2 (distributed like the stars) + constant-Sigma HI; a0 in m/s^2."""

    def __init__(self, MH2, a0, k_gas=math.pi):
        self.MH2, self.a0, self.k = MH2, a0, k_gas

    def vc2(self, R, Re, n, logM, SigHI):
        R = np.maximum(np.asarray(R, float), 1e-4)
        vN2 = disc_v2(R, 10 ** logM + self.MH2, Re, n) + C.sgas_vc2(R, SigHI, self.k)
        gN = vN2 / R
        return C.law_g(gN * C.ACC_UNIT, self.a0) / C.ACC_UNIT * R


class DC14Mass:
    """the survey's decomposition: DC14 halo + MGE disc (M* = 10^X M_vir) + constant-Sigma gas (K3)."""

    def __init__(self, h, Ez, DeltaVir, k_gas=math.pi):
        self.h, self.Ez, self.Dv, self.k = h, Ez, DeltaVir, k_gas

    def vc2(self, R, Re, n, Vvir, c2, X, SigHI):
        R = np.maximum(np.asarray(R, float), 1e-4)
        v2dm, info = C.dc14_vc2(R, Vvir, c2, X, self.h, self.Ez, self.Dv)
        return v2dm + disc_v2(R, 10 ** X * info["Mvir"], Re, n) + C.sgas_vc2(R, SigHI, self.k)


def kinematics(vc2_R, R, Re, n, sig0, drift_scale):
    """v_perp and sigma on radius grid R (kpc) from v_c^2; A1 conventions."""
    vc2 = np.maximum(vc2_R, 0.0)
    h = 0.15 * Re
    sig2 = sig0 ** 2 + h * h * vc2 / np.maximum(R, 1e-4) ** 2
    vad2 = drift_scale * (-2.0 * sig2 * C.sersic_dlnS(R, Re, n))
    vp = np.sqrt(np.maximum(vc2 - vad2, 0.0))
    return vp, np.sqrt(sig2)


# ---------------------------------------------------------------- cube model
class CubeModel:
    def __init__(self, nx, ny, lam, pix, kpc_arcsec, psf_fwhm, psf_beta, os=3, ngh=8):
        self.nx, self.ny, self.lam = nx, ny, np.asarray(lam, float)
        self.nz = len(self.lam)
        self.dlam = float(self.lam[1] - self.lam[0])
        self.edges = np.r_[self.lam - 0.5 * self.dlam, self.lam[-1] + 0.5 * self.dlam]
        self.pix, self.kpc, self.os = pix, kpc_arcsec, os
        sub = (np.arange(os) + 0.5) / os - 0.5
        xs = (np.arange(nx)[:, None] + sub[None, :]).ravel()
        ys = (np.arange(ny)[:, None] + sub[None, :]).ravel()
        self.X, self.Y = np.meshgrid(xs, ys, indexing="xy")
        t, w = np.polynomial.hermite_e.hermegauss(ngh)
        self.t, self.w = t, w / w.sum()
        self.lsf = muse_lsf_fwhm(float(np.mean(self.lam))) / 2.3548
        self.psf_ft, self.pad = self._psf(psf_fwhm, psf_beta)
        self.Rgrid = np.geomspace(0.01, 80.0, 300)

    def _psf(self, fwhm, beta):
        os = 5
        half = 12
        g = (np.arange(-half * os, half * os + os) + 0.5) / os - 0.5
        xx, yy = np.meshgrid(g, g)
        alpha = fwhm / (2 * math.sqrt(2 ** (1 / beta) - 1)) / self.pix
        k = (1 + (xx ** 2 + yy ** 2) / alpha ** 2) ** (-beta)
        n = 2 * half + 1
        k = k.reshape(n, os, n, os).sum((1, 3))
        k /= k.sum()
        py, px = self.ny + n, self.nx + n
        K = np.zeros((py, px))
        K[:n, :n] = k
        K = np.roll(np.roll(K, -half, 0), -half, 1)
        return np.fft.rfft2(K), (py, px)

    def convolve(self, cube):
        py, px = self.pad
        out = np.empty_like(cube)
        for j in range(self.nz):
            F = np.fft.rfft2(cube[j], s=(py, px))
            out[j] = np.fft.irfft2(F * self.psf_ft, s=(py, px))[: self.ny, : self.nx]
        return out

    def model(self, geo, vp_R, sig_R, psf=True):
        """geo: x0, y0 (pix), lc (channel of L1 at systemic), flux, rhalf (arcsec), n, inc, pa (deg), rline."""
        x0, y0, lc, flux, rh, n, inc, pa, rline = geo
        ci, si = math.cos(math.radians(inc)), math.sin(math.radians(inc))
        cp, sp = math.cos(math.radians(pa)), math.sin(math.radians(pa))
        dx = (self.X - x0) * self.pix
        dy = (self.Y - y0) * self.pix
        xm = dx * cp + dy * sp
        ym = -dx * sp + dy * cp
        hz = 0.15 * rh
        Yd = ym[..., None] / ci + (hz * self.t)[None, None, :] * (si / ci)
        Xd = np.broadcast_to(xm[..., None], Yd.shape)
        R = np.sqrt(Xd ** 2 + Yd ** 2)
        Rk = np.maximum(R * self.kpc, 1e-4)
        S = np.exp(-C.b_n(n) * ((R / rh) ** (1.0 / n) - 1.0)) * self.w[None, None, :]
        v = np.interp(Rk, self.Rgrid, vp_R)
        s = np.interp(Rk, self.Rgrid, sig_R)
        vlos = v * (Xd / np.maximum(R, 1e-9)) * si
        lam1 = self.lam[0] + lc * self.dlam
        mu1 = lam1 * (1 + vlos / C.C_KMS)
        mu2 = mu1 * (L2 / L1)
        sl = np.sqrt((s / C.C_KMS * lam1) ** 2 + self.lsf ** 2)
        Sf = S.reshape(-1)
        e = self.edges[None, :]
        p1 = special.ndtr((e - mu1.reshape(-1)[:, None]) / sl.reshape(-1)[:, None])
        p2 = special.ndtr((e - mu2.reshape(-1)[:, None]) / sl.reshape(-1)[:, None])
        prof = np.diff(p1, axis=1) + rline * np.diff(p2, axis=1)
        sub = (Sf[:, None] * prof).reshape(Yd.shape[0], Yd.shape[1], len(self.t), self.nz).sum(2)
        tot = Sf.sum() * (1 + rline)
        cube = sub.reshape(self.ny, self.os, self.nx, self.os, self.nz).sum((1, 3)).transpose(2, 0, 1)
        cube *= flux / max(tot, 1e-300)
        return self.convolve(cube) if psf else cube


# ---------------------------------------------------------------- fitter
GEO = ("x0", "y0", "lc", "flux", "rhalf", "n", "inc", "pa", "rline")


class Fitter:
    """least squares on (data - model)/sigma; mass = 'law' (logM, SigHI) or 'dc14' (Vvir, c2, X, SigHI)."""

    def __init__(self, cm, data, var, mass, kind, drift_scale=1.0, inc_box=None, sighi_fixed=None):
        self.cm, self.data, self.kind, self.mass = cm, data, kind, mass
        self.iw = 1.0 / np.sqrt(np.where(var > 0, var, np.inf))
        self.drift = drift_scale
        self.inc_box = inc_box
        self.sighi_fixed = sighi_fixed

    def names(self):
        if self.kind == "law":
            return GEO + ("sig0", "logM") + (() if self.sighi_fixed is not None else ("SigHI",))
        return GEO + ("sig0", "Vvir", "c2", "X", "SigHI")

    def unpack(self, th):
        d = dict(zip(self.names(), th))
        if self.kind == "law" and self.sighi_fixed is not None:
            d["SigHI"] = self.sighi_fixed
        return d

    def curves(self, d):
        Re = d["rhalf"] * self.cm.kpc
        R = self.cm.Rgrid
        if self.kind == "law":
            vc2 = self.mass.vc2(R, Re, d["n"], d["logM"], d["SigHI"])
        else:
            vc2 = self.mass.vc2(R, Re, d["n"], d["Vvir"], d["c2"], d["X"], d["SigHI"])
        return kinematics(vc2, R, Re, d["n"], d["sig0"], self.drift)

    def model(self, th):
        d = self.unpack(th)
        vp, sg = self.curves(d)
        return self.cm.model([d[k] for k in GEO], vp, sg)

    def resid(self, th):
        r = ((self.data - self.model(th)) * self.iw).ravel()
        return np.where(np.isfinite(r), r, 0.0)

    def fit(self, th0, lo, hi, max_nfev=400):
        th0 = np.clip(th0, np.asarray(lo) + 1e-9, np.asarray(hi) - 1e-9)
        r = optimize.least_squares(self.resid, th0, bounds=(lo, hi), x_scale="jac", max_nfev=max_nfev,
                                   diff_step=1e-3, method="trf")
        npix = int(np.isfinite(self.data).sum())
        chi2 = float(np.sum(r.fun ** 2))
        dof = max(npix - len(th0), 1)
        try:
            J = r.jac
            cov = np.linalg.pinv(J.T @ J) * (chi2 / dof)
            err = np.sqrt(np.clip(np.diag(cov), 0, None))
        except Exception:
            err = np.full(len(th0), np.nan)
        return dict(x=r.x, err=err, chi2=chi2, dof=dof, chi2_red=chi2 / dof, nfev=r.nfev, status=r.status,
                    names=self.names())
