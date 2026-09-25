"""Forward model of the QSO1 narrow-Halpha cube: thin rotating disk in the source plane, local linear lens map,
Gaussian PSF + LSF, linear flux scale solved analytically.  Laws: kepler / framework (RAR kernel) / rival."""
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from scipy.special import erf

C_KMS = 299792.458
G, MSUN, PC = 6.6743e-11, 1.98892e30, 3.0856775814913673e16
Z_SYS = 7.0367
PC_PER_ARCSEC = 5323.29          # proper, Planck18, z = 7.0367
PIX = 0.02                       # arcsec
MU_LENS = 6.2                    # Furtak+24 image A
SIG_LSF = C_KMS / 3700 / 2.3548  # km/s (G395H at 5.28 um, R ~ 3700 per the paper)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
E7 = np.sqrt(0.3153 * (1 + 7.0451) ** 3 + 0.6847)
VWIN = 450.0


import os, hashlib, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CUBE = os.path.join(REPO, "real_research", "data", "qso1", "Halpha_nr_only_cube_02px.fits")
URL = "https://zenodo.org/api/records/19402518/files/Halpha_nr_only_cube_02px.fits/content"
SHA256 = "7bdbae460cc70d2792052b7ede0dc13b620b6e149da5526e523ae93706330292"


def ensure_cube(path=CUBE):
    """Juodzbalis+26 narrow-Halpha cube (Zenodo 19402518, CC-BY-4.0, 86 MB; gitignored)."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(URL, path)
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert h == SHA256, f"cube checksum mismatch: {h}"
    return path


def load(path=None):
    alt = os.environ.get("QSO1_CUBE")                    # a re-extracted cube (derived product, no Zenodo checksum)
    if path is None and alt:
        path = os.path.join(REPO, "real_research", "data", "qso1", alt)
    h = fits.open(ensure_cube() if path is None else path)
    d = h["SCI"].data; e = h["ERR"].data
    hd = h["SCI"].header
    w = hd["CRVAL3"] + np.arange(d.shape[0]) * hd["CDELT3"]
    v = (w / (0.6564614 * (1 + Z_SYS)) - 1) * C_KMS
    sel = np.abs(v) < VWIN
    dv = np.median(np.diff(v))
    return dict(data=d[sel].astype(float), err=1.6 * e[sel].astype(float), v=v[sel], dv=dv,
                full_data=d, full_err=e, full_v=v)


def vcirc(R_pc, logM, law, footing="canonical"):
    GM = G * 10 ** logM * MSUN
    r = R_pc * PC
    vk2 = GM / r
    if law == "kepler":
        nu = 1.0
    else:
        a0 = A0[footing] * (E7 if law == "rival" else 1.0)
        y = GM / (r * r * a0)
        nu = 1.0 / (1.0 - np.exp(-np.sqrt(y)))
    return np.sqrt(vk2 * nu) / 1e3      # km/s


# source-plane polar grid (log-spaced in R so the inner Keplerian region is sampled)
NR, NPHI = 90, 96
R_EDGES = np.logspace(np.log10(0.5), np.log10(1500.0), NR + 1)
R_C = np.sqrt(R_EDGES[1:] * R_EDGES[:-1])
DR = np.diff(R_EDGES)
PHI = (np.arange(NPHI) + 0.5) * 2 * np.pi / NPHI
RR, PP = np.meshgrid(R_C, PHI, indexing="ij")
AREA = (RR * np.outer(DR, np.ones(NPHI)) * (2 * np.pi / NPHI))


def model_cube(p, law, footing, shape, vch, dv, return_parts=False):
    logM, cosi, pa, x0, y0, v0, sig0, Rd, psi, lam1, psf = p
    cosi = np.clip(cosi, 0.05, 0.999); sini = np.sqrt(1 - cosi ** 2)
    lam1 = np.clip(lam1, np.sqrt(MU_LENS) * 1.0001, MU_LENS / 1.0001); lam2 = MU_LENS / lam1
    flux = np.exp(-RR / max(Rd, 1.0)) * AREA
    vlos = v0 + vcirc(RR, logM, law, footing) * sini * np.cos(PP)
    xp = RR * np.cos(PP); yp = RR * np.sin(PP) * cosi
    ca, sa = np.cos(pa), np.sin(pa)
    xs = xp * ca - yp * sa; ys = xp * sa + yp * ca
    cp, sp = np.cos(psi), np.sin(psi)
    u = xs * cp + ys * sp; w_ = -xs * sp + ys * cp          # lens eigenframe
    u *= lam1; w_ *= lam2
    xi = u * cp - w_ * sp; yi = u * sp + w_ * cp
    ix = x0 + xi / PC_PER_ARCSEC / PIX; iy = y0 + yi / PC_PER_ARCSEC / PIX
    ny, nx = shape
    jx = np.floor(ix + 0.5).astype(int); jy = np.floor(iy + 0.5).astype(int)
    ok = (jx >= 0) & (jx < nx) & (jy >= 0) & (jy < ny)
    lin = (jy * nx + jx)[ok]; fl = flux[ok]; vl = vlos[ok]
    sig = np.sqrt(sig0 ** 2 + SIG_LSF ** 2)
    cube = np.empty((len(vch), ny, nx))
    s2 = np.sqrt(2) * sig
    for c, vc in enumerate(vch):
        frac = 0.5 * (erf((vc + dv / 2 - vl) / s2) - erf((vc - dv / 2 - vl) / s2))
        img = np.bincount(lin, weights=fl * frac, minlength=ny * nx).reshape(ny, nx)
        cube[c] = gaussian_filter(img, psf / 2.3548 / PIX, mode="constant")
    return cube


def chi2(p, law, footing, D, mask=None):
    m = model_cube(p, law, footing, D["data"].shape[1:], D["v"], D["dv"])
    wgt = 1.0 / D["err"] ** 2
    if mask is not None:
        wgt = wgt * mask
    a = np.sum(wgt * m * D["data"]) / max(np.sum(wgt * m * m), 1e-300)   # analytic flux scale
    a = max(a, 0.0)
    r = D["data"] - a * m
    return float(np.sum(wgt * r * r)), a
