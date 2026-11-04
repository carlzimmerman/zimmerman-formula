"""FN4a core: data access, the cube forward model (AMENDMENTS A4-A7), and the law's field from the baryon maps.
Criteria FROZEN_CRITERIA.md (a616530a1a), amendments AMENDMENTS.md. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, math, os
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(os.path.dirname(REPO), "_external_data", "fn4a_ic1613_2026_11")
CACHE = os.path.join(HERE, "cache")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
D_MPC = 0.73                      # A7: the record's distance (UNGC, Cepheid)
PIX = 6.0                         # A5: binned pixel, arcsec
BIN = 4
BMAJ, BMIN, BPA = 3.6642e-3 * 3600, 3.0514e-3 * 3600, -4.95      # AIPS CLEAN record in the cube header
DV = 2.572356689                  # km/s channel
SIG_INST = 2 * DV / 2.355         # A4
RING = 13.2                       # A6, arcsec
GPC = 4.30091e-3                  # pc (km/s)^2 / Msun
KMS2_PC_TO_SI = 1e6 / 3.0857e16   # (km/s)^2/pc -> m/s^2
OH15 = dict(ra=(1 + 4 / 60 + 49.6 / 3600) * 15, dec=2 + 8 / 60 + 14.1 / 3600, vsys=-232.2, pa=73.7, inc=48.0, D=0.7, Rmax_kpc=2.71, Vmax=16.9, Mgas=5.93e7, He=1.4)
_law = None


def law_g(gb_si, a0):
    """the record's law (RQ3 candidates/law.py, loaded read-only)."""
    global _law
    if _law is None:
        p = os.path.join(REPO, "rebuild_2026_10_22", "RQ3_acceptance_v2", "candidates", "law.py")
        sp = importlib.util.spec_from_file_location("fn4a_law", p); _law = importlib.util.module_from_spec(sp); sp.loader.exec_module(_law)
    return _law.g(dict(gb=gb_si, a0=a0))


def arcsec_to_pc(x, D=D_MPC): return x * D * 1e6 * math.pi / (180 * 3600)


# ------------------------------------------------------------------ geometry
def disc_coords(XE, YN, x0, y0, pa, inc):
    """sky offsets (arcsec, east and north from Oh+15's centre) -> disc radius (arcsec) and cos/sin of the azimuth from the receding major axis."""
    p = math.radians(pa); xe = XE - x0; yn = YN - y0
    a = xe * math.sin(p) + yn * math.cos(p); b = -xe * math.cos(p) + yn * math.sin(p)
    bd = b / math.cos(math.radians(inc)); R = np.hypot(a, bd); Rs = np.where(R > 0, R, 1e-9)
    return R, a / Rs, bd / Rs


# ------------------------------------------------------------------ beam
def beam_otf(ny, nx):
    """Fourier transfer of the beam (plus the 4x4 binning box as a Gaussian) on a (ny, nx) padded grid of PIX pixels.
    Built from a supersampled real-space kernel with physical offsets: x index runs west (RA decreasing), y index north."""
    sb = math.sqrt((BMAJ / 2.3548) ** 2 + PIX ** 2 / 12); sm = math.sqrt((BMIN / 2.3548) ** 2 + PIX ** 2 / 12); p = math.radians(BPA)
    yy, xx = np.meshgrid(np.fft.fftfreq(ny) * ny, np.fft.fftfreq(nx) * nx, indexing="ij")
    k = np.zeros((ny, nx)); ss = 5
    for oy in (np.arange(ss) + 0.5) / ss - 0.5:
        for ox in (np.arange(ss) + 0.5) / ss - 0.5:
            xe = -(xx + ox) * PIX; yn = (yy + oy) * PIX
            u = xe * math.sin(p) + yn * math.cos(p); w = -xe * math.cos(p) + yn * math.sin(p)
            k += np.exp(-0.5 * (u * u / sb ** 2 + w * w / sm ** 2))
    k /= k.sum(); return np.fft.rfft2(k)


# ------------------------------------------------------------------ the forward model (A4)
class Cube:
    def __init__(s, P, chans=None):
        s.D = P["cube"]; s.v = P["v"]; s.mask = P["mask"]; s.XE = P["XE"]; s.YN = P["YN"]; s.sig = float(P["noise"])
        s.I = np.clip(P["mom0"], 0, None); s.grid = P["grid"]
        s.nk, s.ny, s.nx = s.D.shape
        # no zero padding: the HI ends more than 3 binned pixels inside the 30' crop, so the beam's wrap-around touches nothing;
        # the intensity is zeroed in a 4-pixel border to guarantee it
        s.I = s.I.copy(); s.I[:4] = 0; s.I[-4:] = 0; s.I[:, :4] = 0; s.I[:, -4:] = 0
        s.py, s.px = s.ny, s.nx
        s.otf = beam_otf(s.py, s.px)
        s.Sobs = (s.D * s.mask).sum(0)
        s.sel = s.grid & s.mask
        s.ndat = int(s.sel.sum())

    def model(s, vlos, sig):
        """vlos, sig: (ny, nx) maps. Gaussian lines weighted by moment 0, beam-convolved channel by channel, locally normalised."""
        se = np.sqrt(sig ** 2 + SIG_INST ** 2)
        L = s.I[None] * np.exp(-0.5 * ((s.v[:, None, None] - vlos[None]) / se[None]) ** 2)
        F = np.fft.rfft2(L, s=(s.py, s.px)) * s.otf[None]
        C = np.fft.irfft2(F, s=(s.py, s.px))[:, :s.ny, :s.nx]
        Sm = (C * s.mask).sum(0); f = np.where((s.Sobs > 0) & (Sm > 0), s.Sobs / np.where(Sm > 0, Sm, 1), 0.0)
        return C * f[None]

    def resid(s, vlos, sig):
        M = s.model(vlos, sig); return ((s.D - M) / s.sig)[s.sel]


def vfield(cube, x0, y0, pa, inc, vsys, Vfun, sigfun, nc=None):
    R, c, sn = disc_coords(cube.XE, cube.YN, x0, y0, pa, inc); si = math.sin(math.radians(inc))
    v = Vfun(R) * c
    if nc is not None:
        s1, c2, s2 = nc(R); v = v + s1 * sn + c2 * (2 * c * c - 1) + s2 * (2 * sn * c)
    return vsys + si * v, sigfun(R), R


def interp_nodes(nodes_R, vals):
    nodes_R = np.asarray(nodes_R, float); vals = np.asarray(vals, float)
    return lambda R: np.interp(R, nodes_R, vals)


# ------------------------------------------------------------------ the law's field (A7)
class Baryons:
    """gas Sigma_sky (Msun/pc^2, x1.33) on the binned sky grid, and an axisymmetric stellar profile in the disc plane."""
    def __init__(s, P, mstar):
        s.gas = P["gas_sky"]; s.XE = P["XE"]; s.YN = P["YN"]; s.dx = PIX
        s.sR = P["star_R"]; s.sprof = P["star_prof"] * (mstar / P["star_norm"])
        n = int(2 * 1000 / PIX) | 1; c = (np.arange(n) - n // 2) * PIX; s.FX, s.FY = np.meshgrid(c, c, indexing="xy")
        s.n = n; s.pad = 1 << int(math.ceil(math.log2(2 * n))); s.kern = {}

    def _kernel(s, eps_pc):
        if eps_pc in s.kern: return s.kern[eps_pc]
        d = arcsec_to_pc(PIX); i = np.fft.fftfreq(s.pad) * s.pad; yy, xx = np.meshgrid(i, i, indexing="ij"); rx = xx * d; ry = yy * d
        r3 = (rx * rx + ry * ry + eps_pc ** 2) ** 1.5; kx = -rx / r3; ky = -ry / r3
        s.kern[eps_pc] = (np.fft.rfft2(kx), np.fft.rfft2(ky)); return s.kern[eps_pc]

    def face_on(s, x0, y0, pa, inc):
        p = math.radians(pa); ci = math.cos(math.radians(inc))
        a = s.FX; b = s.FY * ci                                   # disc (X along major, Y along minor) -> sky
        xe = x0 + a * math.sin(p) - b * math.cos(p); yn = y0 + a * math.cos(p) + b * math.sin(p)
        jx = (xe - s.XE[0, 0]) / (s.XE[0, 1] - s.XE[0, 0]); jy = (yn - s.YN[0, 0]) / (s.YN[1, 0] - s.YN[0, 0])
        g = ndimage.map_coordinates(s.gas, [jy, jx], order=1, mode="constant", cval=0.0) * ci
        Rd = np.hypot(s.FX, s.FY); st = np.interp(Rd, s.sR, s.sprof, right=0.0)
        return g, st, Rd

    def vc2(s, x0, y0, pa, inc, a0, nu=True, eps_pc=200.0, Rgrid=None):
        g, st, Rd = s.face_on(x0, y0, pa, inc); sig = g + st; d = arcsec_to_pc(PIX)
        kx, ky = s._kernel(eps_pc); F = np.fft.rfft2(sig, s=(s.pad, s.pad))
        gx = np.fft.irfft2(F * kx, s=(s.pad, s.pad))[:s.n, :s.n] * GPC * d * d; gy = np.fft.irfft2(F * ky, s=(s.pad, s.pad))[:s.n, :s.n] * GPC * d * d
        # the kernel is centred at index 0, so the convolution maps map i -> i; shift back by n//2 is not needed (map at origin offsets)
        Rs = np.where(Rd > 0, Rd, 1e-9); gR = -(gx * s.FX + gy * s.FY) / Rs           # inward positive, (km/s)^2/pc
        if Rgrid is None: Rgrid = np.arange(0.5, 160) * PIX
        edges = np.r_[0, 0.5 * (Rgrid[1:] + Rgrid[:-1]), Rgrid[-1] + 0.5 * (Rgrid[-1] - Rgrid[-2])]
        idx = np.digitize(Rd.ravel(), edges) - 1; ok = (idx >= 0) & (idx < len(Rgrid))
        gm = np.bincount(idx[ok], weights=gR.ravel()[ok], minlength=len(Rgrid)) / np.maximum(np.bincount(idx[ok], minlength=len(Rgrid)), 1)
        gsum = np.bincount(idx[ok], weights=g.ravel()[ok], minlength=len(Rgrid)) / np.maximum(np.bincount(idx[ok], minlength=len(Rgrid)), 1)
        gN = np.clip(gm, 0, None) * KMS2_PC_TO_SI
        gl = law_g(gN, a0) if nu else gN
        Rpc = arcsec_to_pc(Rgrid); v2 = gl / KMS2_PC_TO_SI * Rpc
        return Rgrid, v2, gsum
