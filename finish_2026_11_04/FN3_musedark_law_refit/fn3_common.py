"""FN3 shared engine. Criteria: FROZEN_CRITERIA.md (c6640225c2). kappa = 1/2 FITTED; not theory closed.

Pieces: K0 hash checks, loaders for the released MUSE-DARK DC14 runs, the survey's Planck15 distances (K1 only),
CFG689's native background and band, the DC14 halo, an MGE of the Sersic [OII] profile and its circular speed,
the constant-Sigma gas term, pressure-support variants, the law's nu, and the Tacconi 2020 molecular-gas scaling.
"""
import hashlib
import json
import math
import os

import warnings

import numpy as np
from scipy import integrate, optimize

# numpy 1.26 on Apple Accelerate prints spurious matmul RuntimeWarnings; values are unaffected (checked against Freeman 1970).
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*encountered in matmul")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data", "muse_dark"))
NUMERIC = os.path.join(EXT, "numeric")
CFG689_JSON = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")

G_KPC = 4.30091e-6            # kpc (km/s)^2 / Msun
C_KMS = 299792.458
KPC_M = 3.0856775814913673e19
A_FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
NU_ROWS = 4                   # released .dat tables: value, std, CI low, CI high


# ---------------------------------------------------------------- K0: hashes
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_hashes():
    """K0: every released file against the committed manifests. Returns (n_ok, list of failures)."""
    fails, n = [], 0
    man = os.path.join(REPO, "data_assembly", "musedark_catalogues", "numeric_manifest_sha256.txt")
    for line in open(man):
        parts = line.split()
        if len(parts) != 2:
            continue
        hsh, rel = parts
        p = os.path.join(NUMERIC, rel)
        n += 1
        if not os.path.exists(p) or sha256(p) != hsh:
            fails.append(rel)
    cat = json.load(open(os.path.join(REPO, "data_assembly", "musedark_catalogues", "manifest.json")))
    for fn, d in cat.items():
        p = os.path.join(EXT, fn)
        n += 1
        if not os.path.exists(p) or sha256(p) != d["sha256"]:
            fails.append(fn)
    return n, fails


# ---------------------------------------------------------------- released files
def parse_table(path):
    """'|'-delimited table: header names, then rows of floats (value, std, CI low, CI high)."""
    rows = [ln.strip() for ln in open(path) if ln.strip().startswith("|")]
    names = [c.strip() for c in rows[0].strip("|").split("|")]
    vals = []
    for ln in rows[1:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        vals.append([float(c) if c not in ("", "nan") else float("nan") for c in cells])
    return names, np.array(vals, float)


def parse_kv(path):
    """key = value lines from run_parameters / model files."""
    out = {}
    for ln in open(path):
        if "=" in ln:
            k, v = ln.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def galaxy_ids():
    return sorted(int(d[2:]) for d in os.listdir(NUMERIC) if d.startswith("ID"))


def load_galaxy(gid):
    d = os.path.join(NUMERIC, f"ID{gid:04d}")
    pre = os.path.join(d, f"DC14_{gid}_")
    gn, gv = parse_table(pre + "galaxy_parameters.dat")
    dn, dv = parse_table(pre + "derived_parameters.dat")
    vn, vv = parse_table(pre + "true_Vrot.dat")
    run = parse_kv(pre + "run_parameters.txt")
    model = parse_kv(pre + "model.txt")
    par = dict(zip(gn, gv[0]))
    der = dict(zip(dn, dv[0]))
    rot = {k: vv[:, i] for i, k in enumerate(vn)}
    psf = {}
    txt = open(pre + "run_parameters.txt").read()
    for key in ("fwhm", "beta"):
        for ln in txt.splitlines():
            s = ln.strip()
            if s.startswith(key) and "=" in s:
                psf[key] = float(s.split("=")[1].split()[0])
                break
    return dict(gid=gid, par=par, par_tab=(gn, gv), der=der, der_tab=(dn, dv), rot=rot, run=run, model=model, psf=psf,
                z=float(model["redshift"]), kpc=float(model["kpc"]), h=float(model["h"]), Ez=float(model["Ez"]),
                DeltaVir=float(model["DeltaVir"]), pixscale=float(model["pixscale"]), aspect=float(model["aspect"]),
                bulge=("bulge_radius" in par or model.get("rotation_curve_bulge", "none") != "none"))


def load_catalogue():
    cols = None
    phot = {}
    for ln in open(os.path.join(EXT, "photometry_catalogue.txt")):
        p = ln.split()
        if not p:
            continue
        if cols is None:
            cols = p
            continue
        row = dict(zip(cols, p))
        try:
            mid = int(row["muse_id"])
        except ValueError:
            continue
        rec = {}
        for k in cols[1:]:
            try:
                rec[k] = float(row.get(k, "nan"))
            except ValueError:
                rec[k] = float("nan")
        phot[mid] = rec
    fit = {}
    cols = None
    for ln in open(os.path.join(EXT, "Fit_statistics_all_models.txt")):
        p = ln.split()
        if not p:
            continue
        if cols is None:
            cols = p
            continue
        row = dict(zip(cols, p))
        try:
            fit[int(row["muse_id"])] = {k: float(v) for k, v in row.items() if k != "muse_id"}
        except ValueError:
            continue
    return phot, fit


# ---------------------------------------------------------------- distances
def planck15():
    from astropy.cosmology import Planck15
    return Planck15


class Native:
    """CFG689 primary (BAO+SN) posterior-mean background: H(z) = 100 sqrt(E2) km/s/Mpc, E2 in omega units."""

    def __init__(self):
        d = json.load(open(CFG689_JSON))
        po = d["BAO+SN"]["posterior"]
        self.nodes = np.array(d["cfg"]["nodes"], float)
        self.w = np.array(po["node_mean"], float)
        self.w_std = np.array(po["node_std"], float)
        self.wb, self.wc, self.wk = po["omega_b"][0], po["omega_c"][0], po["omega_k"][0]
        self.wm = self.wb + self.wc                      # CFG689: om = wb + wc (f 0, m_nu 0)
        self.wr = 2.4728e-5 * (1 + 0.2271 * 3.044)       # CFG689: OMR = OMG (1 + 0.2271 N_rel)
        self.h2 = self.wm + self.wr + self.wk + self.w[0]
        self.h = math.sqrt(self.h2)
        self.P1 = d["BAO+SN"]["P1"]
        self.zg = np.linspace(0.0, 2.5, 25001)
        self.Hg = self.H(self.zg)
        chi = np.r_[0, np.cumsum(0.5 * (1 / self.Hg[1:] + 1 / self.Hg[:-1]) * np.diff(self.zg))] * C_KMS
        s = 100 * math.sqrt(abs(self.wk)) / C_KMS
        self.DMg = np.sinh(s * chi) / s if self.wk > 0 else (np.sin(s * chi) / s if self.wk < 0 else chi)

    def wde(self, z):
        return np.interp(z, self.nodes, self.w)          # np.interp holds the end values outside [0, 2.33]

    def H(self, z):
        z = np.asarray(z, float)
        return 100 * np.sqrt(self.wm * (1 + z) ** 3 + self.wr * (1 + z) ** 4 + self.wk * (1 + z) ** 2 + self.wde(z))

    def E(self, z):
        return self.H(z) / (100 * self.h)

    def DM(self, z):
        return np.interp(z, self.zg, self.DMg)

    def DA(self, z):
        return self.DM(z) / (1 + z)

    def DL(self, z):
        return self.DM(z) * (1 + z)

    def kpc_per_arcsec(self, z):
        return self.DA(z) * 1e3 * math.pi / (180 * 3600)

    def age_gyr(self, z):
        """cosmic time at z: integral of dz/((1+z)H) from z to 1e7 on a log grid (Gyr)."""
        lz = np.linspace(math.log(1 + z), math.log(1 + 1e7), 20001)
        zz = np.exp(lz) - 1
        f = 1 / self.H(zz)                               # d ln(1+z) / H, H in km/s/Mpc
        t = integrate.trapezoid(f, lz)                   # Mpc s / km
        return t * 3.0856775814913673e19 / 3.15576e16    # Mpc/(km/s) -> Gyr

    def band_ratio(self, z):
        return np.sqrt(self.wde(z) / self.w[0])

    def band_sigma_dex(self, z):
        """Criteria s6: 68 % half-width of log10 sqrt(X) at the nearest node. P1's quantiles where CFG689 gives them
        (z 1.0, 1.2, 1.5, 2.33); at nodes 0.4 and 0.7, from node_std with the two nodes taken as independent."""
        pts = {}
        for zs, v in self.P1.items():
            q = v["sqrtX_q"]
            pts[float(zs)] = 0.5 * (math.log10(q[3]) - math.log10(q[1]))
        for i, zn in enumerate(self.nodes):
            if zn in (0.4, 0.7):
                rel = math.hypot(self.w_std[i] / self.w[i], self.w_std[0] / self.w[0])
                pts[float(zn)] = 0.5 * rel / math.log(10)
        keys = np.array(sorted(pts))
        return pts[float(keys[np.argmin(np.abs(keys - z))])]


# ---------------------------------------------------------------- DC14 halo (Di Cintio et al. 2014)
def dc14_shape(X):
    a = 2.94 - math.log10((10 ** (X + 2.33)) ** -1.08 + (10 ** (X + 2.33)) ** 2.29)
    b = 4.23 + 1.34 * X + 0.26 * X * X
    g = -0.06 + math.log10((10 ** (X + 2.56)) ** -0.68 + 10 ** (X + 2.56))
    return a, b, g


def dc14_vc2(r_kpc, Vvir, c2, X, h, Ez, DeltaVir):
    """v^2 (km/s)^2 of a DC14 halo; c2 = R_vir / r_-2; R_vir = V_vir / (H(z) sqrt(Delta/2))."""
    a, b, g = dc14_shape(X)
    Hz = 100 * h * Ez / 1e3                               # km/s/kpc
    Rvir = Vvir / (Hz * math.sqrt(DeltaVir / 2))
    Mvir = Vvir ** 2 * Rvir / G_KPC
    rs = (Rvir / c2) * ((b - 2) / (2 - g)) ** (1 / a)
    f = lambda t: t ** (2 - g) * (1 + t ** a) ** (-(b - g) / a)
    xs = np.r_[0.0, np.geomspace(1e-6, max(10.0, Rvir / rs * 1.01), 4000)]
    ys = f(np.maximum(xs, 1e-300))
    ys[0] = 0.0
    m = np.r_[0, np.cumsum(0.5 * (ys[1:] + ys[:-1]) * np.diff(xs))]
    mvir = np.interp(Rvir / rs, xs, m)
    r = np.asarray(r_kpc, float)
    M = Mvir * np.interp(r / rs, xs, m) / mvir
    return G_KPC * M / np.maximum(r, 1e-6), dict(alpha=a, beta=b, gamma=g, rs=rs, Rvir=Rvir, Mvir=Mvir)


# ---------------------------------------------------------------- Sersic, MGE, disc speed
def b_n(n):
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n * n) + 131 / (1148175 * n ** 3)


def sersic_mge(n, ng=24, rmin=0.02, rmax=12.0):
    """Gaussian expansion (circular, projected) of a Sersic profile with R_e = 1. Returns sigma_j and mass fractions."""
    R = np.geomspace(rmin * 0.5, rmax * 1.5, 300)
    I = np.exp(-b_n(n) * (R ** (1 / n) - 1))
    keep = I > 1e-9 * I.max()                            # fit only where the profile is representable
    R, I = R[keep], I[keep]
    sig = np.geomspace(rmin, min(rmax, R.max()), ng)
    A = np.exp(-R[:, None] ** 2 / (2 * sig[None, :] ** 2)) / (2 * math.pi * sig[None, :] ** 2)
    W = 1 / I                                            # relative residuals
    w, _ = optimize.nnls(A * W[:, None], I * W)
    frac = w / w.sum()
    model = A @ w
    sel = (R > rmin) & (R < 4) & (I > 1e-6 * I.max())
    err = float(np.max(np.abs(model / I - 1)[sel]))
    return sig, frac, err


_TH, _WT = np.polynomial.legendre.leggauss(64)
_TH = 0.25 * math.pi * (_TH + 1)
_WT = 0.25 * math.pi * _WT


def mge_vc2(R, sig, frac, M, q):
    """Equatorial v^2 of a sum of oblate Gaussians (intrinsic axis ratio q), total mass M. R and sig in kpc.
    v^2 = sum_j 4 pi G rho0_j q R^2 int_0^1 exp(-R^2 u^2 / 2 s^2) u^2 / sqrt(1 - (1-q^2) u^2) du, u = sin(theta)."""
    R = np.atleast_1d(np.asarray(R, float))
    su = np.sin(_TH)
    kern = su ** 2 * np.cos(_TH) / np.sqrt(1 - (1 - q * q) * su ** 2)
    v2 = np.zeros_like(R)
    for s, f in zip(sig, frac):
        pref = 4 * math.pi * G_KPC * M * f / ((2 * math.pi) ** 1.5 * s ** 3)
        e = np.exp(-(R[:, None] ** 2) * su[None, :] ** 2 / (2 * s * s))
        v2 += pref * R ** 2 * (e * kern[None, :] * _WT[None, :]).sum(1)
    return v2


def sgas_vc2(R, Sigma_pc2, k):
    """v^2 = k G Sigma R (Sigma in Msun/pc^2); k = pi or 2 pi, pinned by K1."""
    return k * G_KPC * Sigma_pc2 * 1e6 * np.asarray(R, float)


def sersic_dlnS(R, Re, n):
    return -(b_n(n) / n) * (np.asarray(R, float) / Re) ** (1 / n)


def drift_v2(variant, R, Re, n, sig_tot, sig0, dlnsig2):
    """v_AD^2 variants of the criteria: D1 -2 s^2 dlnS; D2 D1 - s^2 dln(s^2)/dlnR; D3 -2 s0^2 dlnS."""
    dl = sersic_dlnS(R, Re, n)
    if variant == "D1":
        return -2 * sig_tot ** 2 * dl
    if variant == "D2":
        return -2 * sig_tot ** 2 * dl - sig_tot ** 2 * dlnsig2
    if variant == "D3":
        return -2 * sig0 ** 2 * dl
    raise ValueError(variant)


# ---------------------------------------------------------------- the law and the gas scaling
def nu_simple(y):
    y = np.asarray(y, float)
    return 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))


def law_g(gN, a0):
    return nu_simple(gN / a0) * gN


def speagle_logsfr(logm, t_gyr):
    return (0.84 - 0.026 * t_gyr) * logm - (6.51 - 0.11 * t_gyr)


def mu_mol_t20(z, logm, logsfr=None, t_gyr=None, use_dms=True):
    """Tacconi, Genzel & Sternberg 2020 eq. 2 (log10 throughout), as CFG90 codes it, plus 0.51 log(delta_MS)."""
    x = math.log10(1 + z) - 0.65
    lm = 0.06 - 3.33 * x * x - 0.41 * (logm - 10.7)
    if use_dms and logsfr is not None and np.isfinite(logsfr):
        lm += 0.51 * (logsfr - speagle_logsfr(logm, t_gyr))
    return 10 ** lm


ACC_UNIT = 1e6 / KPC_M        # (km/s)^2 / kpc -> m/s^2
