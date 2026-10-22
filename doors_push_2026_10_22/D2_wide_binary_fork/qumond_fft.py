"""Independent QUMOND two-body solver with a uniform external field (lane D2_wide_binary_fork).

Not A24's method: A24 integrates the phantom density on an axisymmetric (rho, z) grid with the
field along the separation.  Here the phantom field is the LONGITUDINAL (curl-free) projection of
S = (nu(|g_N|/a0) - 1) g_N done by a 3-D FFT, for any field orientation.

Units: separation s = 1, a0 = 1, so G*M_tot = y_tot = G M_tot/(s^2 a0).  Two equal stars at
(0, 0, -1/2) and (0, 0, +1/2), both at cell CENTRES so that each star's own (odd) near field cancels
exactly in the 8-node average.  Newtonian external field y_e along e = (sin th, 0, cos th).
"""
import numpy as np
import scipy.fft as sfft


def nu(y):
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def dlnnu_dlny(y):
    # K = d ln nu / d ln y for nu = (1 + sqrt(1 + 4/y))/2
    r = np.sqrt(1.0 + 4.0 / y)
    return -(2.0 / (y * r)) / (1.0 + r)


def y_newton_from_obs(x):
    """law g_N = g^2/(g + a0)  ->  y = x^2/(1 + x)."""
    return x * x / (1.0 + x)


def _grid(N, m):
    dx = 1.0 / (2 * m + 1)
    xs = (np.arange(N) - N // 2 + 0.5) * dx      # 0 is a cell centre
    zs = (np.arange(N) - N // 2) * dx            # +-1/2 = (m + 1/2) dx are cell centres
    return dx, xs, zs


def _star_nodes(N, m):
    # 8 nodes around (0,0,+1/2) and (0,0,-1/2)
    ix = [N // 2 - 1, N // 2]
    kz_up = [N // 2 + m, N // 2 + m + 1]
    kz_dn = [N // 2 - m - 1, N // 2 - m]
    return ix, kz_up, kz_dn


def phantom_rel(y_tot, y_e, theta, N=192, m=8, mode="full", project=True):
    """Return a_rel / a_N along the separation.

    mode = 'full'   : S = (nu(|g|) - 1) g - (nu_e - 1) g_e    (nonlinear QUMOND)
    mode = 'linear' : S = (nu_e - 1) g_i + nu_e K (e.g_i) e   (linear EFE order, for control C1)
    project = False is the MUTATE: the phantom field is taken to be S itself (no curl removal).
    """
    dx, xs, zs = _grid(N, m)
    e = np.array([np.sin(theta), 0.0, np.cos(theta)])
    GM1 = 0.5 * y_tot
    nue = nu(y_e) if y_e > 0 else None
    K = dlnnu_dlny(y_e) if y_e > 0 else None
    S = np.empty((3, N, N, N), dtype=np.float32)
    X = xs[:, None]
    Y = xs[None, :]
    for k in range(N):                            # slab over z keeps memory low
        z = zs[k]
        gx = np.zeros((N, N)); gy = np.zeros((N, N)); gz = np.zeros((N, N))
        for zc in (-0.5, 0.5):
            dzz = z - zc
            r2 = X * X + Y * Y + dzz * dzz
            r3 = r2 * np.sqrt(r2)
            gx += -GM1 * X / r3
            gy += -GM1 * Y / r3
            gz += -GM1 * dzz / r3
        if mode == "linear":
            eg = e[0] * gx + e[1] * gy + e[2] * gz
            sx = (nue - 1.0) * gx + nue * K * eg * e[0]
            sy = (nue - 1.0) * gy + nue * K * eg * e[1]
            sz = (nue - 1.0) * gz + nue * K * eg * e[2]
        else:
            tx = gx + y_e * e[0]; ty = gy + y_e * e[1]; tz = gz + y_e * e[2]
            mag = np.sqrt(tx * tx + ty * ty + tz * tz)
            f = nu(mag) - 1.0
            sx = f * tx; sy = f * ty; sz = f * tz
            if y_e > 0:
                sx -= (nue - 1.0) * y_e * e[0]
                sy -= (nue - 1.0) * y_e * e[1]
                sz -= (nue - 1.0) * y_e * e[2]
        # axis order (x, y, z) -> array [ix, iy, kz]
        S[0, :, :, k] = sx; S[1, :, :, k] = sy; S[2, :, :, k] = sz
    if project:
        kx = 2 * np.pi * sfft.fftfreq(N, dx)
        kz = 2 * np.pi * sfft.rfftfreq(N, dx)
        D = sfft.rfftn(S[0], workers=1) * kx[:, None, None].astype(np.float32)
        D += sfft.rfftn(S[1], workers=1) * kx[None, :, None].astype(np.float32)
        Sz_hat = sfft.rfftn(S[2], workers=1)
        D += Sz_hat * kz[None, None, :].astype(np.float32)
        del Sz_hat, S
        k2 = (kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2).astype(np.float32)
        k2[0, 0, 0] = 1.0
        D *= kz[None, None, :].astype(np.float32) / k2
        D[0, 0, 0] = 0.0
        del k2
        gphz = sfft.irfftn(D, s=(N, N, N), workers=1)
        del D
    else:
        gphz = S[2]
    ix, kup, kdn = _star_nodes(N, m)
    up = np.mean(gphz[np.ix_(ix, ix, kup)])
    dn = np.mean(gphz[np.ix_(ix, ix, kdn)])
    a_rel_ph = dn - up                            # star 1 (down) pulled +z, star 2 (up) pulled -z
    if mode == "linear":
        return float(a_rel_ph / y_tot)            # = B(theta) - 1 analytically
    return float(1.0 + a_rel_ph / y_tot)


def linear_analytic(y_e, theta):
    """B(theta) - 1 for linear QUMOND EFE: nu_e(1 + K sin^2(th)/2) - 1."""
    return nu(y_e) * (1.0 + dlnnu_dlny(y_e) * np.sin(theta) ** 2 / 2.0) - 1.0


GL3_MU = np.array([0.1127016653792583, 0.5, 0.8872983346207417])   # Gauss-Legendre on [0,1]
GL3_W = np.array([5.0, 8.0, 5.0]) / 18.0


def gamma_v(y_tot, y_e, theta=None, **kw):
    """theta=None -> orientation average of a_rel over cos(theta) uniform."""
    if theta is not None:
        return float(np.sqrt(phantom_rel(y_tot, y_e, theta, **kw)))
    a = sum(w * phantom_rel(y_tot, y_e, float(np.arccos(mu)), **kw) for mu, w in zip(GL3_MU, GL3_W))
    return float(np.sqrt(a))
