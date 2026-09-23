"""Core-restricted forward model: Sersic rotating disk (law) + spatially-uniform outflow line (nuisance), core mask.
Linear amplitudes (disk, outflow) solved by weighted least squares at every evaluation."""
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.special import erf
from model import (load, vcirc, PC_PER_ARCSEC, PIX, MU_LENS, SIG_LSF, RR, PP, AREA)

YC, XC, RMASK = 19, 20, 8.0            # core mask radius 8 px = 0.16"
NAMES = ["logM", "cosi", "pa", "x0", "y0", "v0", "sig0", "Re", "n", "psi", "lam1", "psf", "vout", "sout"]
BOUNDS = [(6.0, 9.0), (0.1, 0.99), (0.0, np.pi), (16, 24), (15, 23), (-120, 80), (0, 120), (2, 400), (0.5, 4.0),
          (0.0, np.pi), (2.5, 6.19), (float(__import__("os").environ.get("PSF_MIN", "0.08")), 0.30), (-300, 200), (30, 400)]


def mask_for(shape):
    yy, xx = np.indices(shape)
    return (np.hypot(yy - YC, xx - XC) <= RMASK).astype(float)


def disk_cube(p, law, footing, shape, vch, dv):
    logM, cosi, pa, x0, y0, v0, sig0, Re, n, psi, lam1, psf, vout, sout = p
    cosi = np.clip(cosi, 0.05, 0.999); sini = np.sqrt(1 - cosi ** 2)
    lam1 = np.clip(lam1, np.sqrt(MU_LENS) * 1.0001, MU_LENS / 1.0001); lam2 = MU_LENS / lam1
    bn = 2 * n - 1 / 3 + 0.009876 / n
    flux = np.exp(-bn * ((RR / max(Re, 1.0)) ** (1 / n) - 1)) * AREA
    vlos = v0 + vcirc(RR, logM, law, footing) * sini * np.cos(PP)
    xp = RR * np.cos(PP); yp = RR * np.sin(PP) * cosi
    ca, sa = np.cos(pa), np.sin(pa)
    xs = xp * ca - yp * sa; ys = xp * sa + yp * ca
    cp, sp = np.cos(psi), np.sin(psi)
    u = (xs * cp + ys * sp) * lam1; w_ = (-xs * sp + ys * cp) * lam2
    xi = u * cp - w_ * sp; yi = u * sp + w_ * cp
    ix = x0 + xi / PC_PER_ARCSEC / PIX; iy = y0 + yi / PC_PER_ARCSEC / PIX
    ny, nx = shape
    jx = np.floor(ix + 0.5).astype(int); jy = np.floor(iy + 0.5).astype(int)
    ok = (jx >= 0) & (jx < nx) & (jy >= 0) & (jy < ny)
    lin = (jy * nx + jx)[ok]; fl = flux[ok]; vl = vlos[ok]
    s2 = np.sqrt(2) * np.sqrt(sig0 ** 2 + SIG_LSF ** 2)
    cube = np.empty((len(vch), ny, nx))
    for c, vc in enumerate(vch):
        frac = 0.5 * (erf((vc + dv / 2 - vl) / s2) - erf((vc - dv / 2 - vl) / s2))
        img = np.bincount(lin, weights=fl * frac, minlength=ny * nx).reshape(ny, nx)
        cube[c] = gaussian_filter(img, psf / 2.3548 / PIX, mode="constant")
    return cube


def outflow_cube(p, shape, vch, dv):
    vout, sout = p[12], p[13]
    s2 = np.sqrt(2) * np.sqrt(sout ** 2 + SIG_LSF ** 2)
    prof = 0.5 * (erf((vch + dv / 2 - vout) / s2) - erf((vch - dv / 2 - vout) / s2))
    return prof[:, None, None] * np.ones((1,) + tuple(shape))


def chi2(p, law, footing, D, M):
    sh = D["data"].shape[1:]
    m1 = disk_cube(p, law, footing, sh, D["v"], D["dv"]); m2 = outflow_cube(p, sh, D["v"], D["dv"])
    w = M[None] / D["err"] ** 2
    A = np.array([[np.sum(w * m1 * m1), np.sum(w * m1 * m2)], [np.sum(w * m1 * m2), np.sum(w * m2 * m2)]])
    b = np.array([np.sum(w * m1 * D["data"]), np.sum(w * m2 * D["data"])])
    try:
        a = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return 1e12, (0, 0)
    a = np.maximum(a, 0)
    r = D["data"] - a[0] * m1 - a[1] * m2
    return float(np.sum(w * r * r)), a


def f(p, law, footing, D, M):
    for x, (lo, hi) in zip(p, BOUNDS):
        if x < lo or x > hi:
            return 1e12
    return chi2(p, law, footing, D, M)[0]
