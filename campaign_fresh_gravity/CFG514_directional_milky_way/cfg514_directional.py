#!/usr/bin/env python3
"""CFG514: looking out through the Milky Way's cold energy, direction by direction.

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 6a303d380).
Framework: QUMOND phantom with nu_mono on McMillan 2017 baryons (the settled cold energy has the phantom's profile).
Rival: the same baryons plus a spherical NFW fitted to the same rotation curve (Eilers+2019).
CFG514_MUTATE=1 replaces the phantom by its spherical shell average (shape forced NFW-like).
kappa = 1/2 is FITTED; both footings; the cold energy's mass is still required; not theory closed.
Run:  nice -n 15 python3 cfg514_directional.py   (<= 4 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")
import sys, json, math, glob, time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import least_squares, minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
DESI_DIR = os.path.join(EXT, "desi_mws", "rvtab")
WORK = os.path.join(EXT, "cfg514_work")
MUTATE = os.environ.get("CFG514_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT_LINES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT_LINES.append(s)


CHECKS = []


def check(cond, msg):
    CHECKS.append((bool(cond), msg))
    P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


# ------------------------------------------------------------------ units: kpc, Msun, km/s
G = 4.30091e-6                     # kpc (km/s)^2 / Msun
C_KMS = 299792.458
KPC_M = 3.0856775814913673e19
KPC_KMS_S = KPC_M / 1e3            # seconds per (kpc / (km/s))
A0_SI = {"canonical": 9.36e-11, "alt": 1.13e-10}
A0 = {k: v * KPC_M / 1e6 for k, v in A0_SI.items()}   # (km/s)^2/kpc
F_B = 0.157134                     # record's f_b (CFG462/CFG423)
R0 = 8.122                         # kpc (Eilers+19 adopted)
UVW = np.array([11.1, 245.6, 7.3])  # km/s, declared
H0 = 67.7                          # km/s/Mpc, only labels M200/c
RHO_CRIT = 3 * (H0 / 1e3) ** 2 / (8 * math.pi * G)  # Msun/kpc^3

# ------------------------------------------------------------------ McMillan 2017 Table 3 baryons (as mi_aqual_mcmillan2017_2026.py)
PC2 = 1e6                          # Msun/pc^2 -> Msun/kpc^2
PC3 = 1e9
S0_THIN, RD_THIN, ZD_THIN = 896.0 * PC2, 2.50, 0.300
S0_THICK, RD_THICK, ZD_THICK = 183.0 * PC2, 3.02, 0.900
RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = 98.4 * PC3, 1.8, 0.075, 2.1, 0.5
R_FID = 8.33
S0_HI = 10.0 * PC2 / math.exp(-4.0 / R_FID - R_FID / 7.0)
S0_H2 = 2.0 * PC2 / math.exp(-12.0 / R_FID - R_FID / 1.5)


def rho_baryon(R, z):
    z = np.abs(z)
    thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-z / ZD_THIN - R / RD_THIN)
    thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-z / ZD_THICK - R / RD_THICK)
    rp = np.maximum(np.sqrt(R * R + (z / Q_B) ** 2), 1e-7)
    bulge = RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)
    Rs = np.maximum(R, 1e-6)
    hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(z / (2 * 0.085)) ** 2
    h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(z / (2 * 0.045)) ** 2
    return thin + thick + bulge + hi + h2


def rho_stars_only(R, z):
    z = np.abs(z)
    thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-z / ZD_THIN - R / RD_THIN)
    thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-z / ZD_THICK - R / RD_THICK)
    rp = np.maximum(np.sqrt(R * R + (z / Q_B) ** 2), 1e-7)
    return thin + thick + RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)


def nu_mono(y):
    y = np.maximum(y, 1e-30)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


# ------------------------------------------------------------------ axisymmetric finite-volume grid
class Grid:
    def __init__(self, n=200, first=0.02, growth=1.045):
        d = first * growth ** np.arange(n)
        self.Re = np.concatenate([[0.0], np.cumsum(d)])
        self.ze = self.Re.copy()
        self.Rc = 0.5 * (self.Re[:-1] + self.Re[1:])
        self.zc = self.Rc.copy()
        self.dR = d.copy(); self.dz = d.copy()
        n = len(d); self.n = n
        Rc, zc, dR, dz, Re = self.Rc, self.zc, self.dR, self.dz, self.Re
        self.RR, self.ZZ = np.meshgrid(Rc, zc, indexing="ij")
        self.VOL = Rc[:, None] * dR[:, None] * dz[None, :]       # 2pi omitted throughout
        self.dRf, self.dzf = np.diff(Rc), np.diff(zc)
        self.dR_o, self.dz_o = dR[-1] / 2, dz[-1] / 2
        self.AR = Re[1:-1, None] * dz[None, :]                    # interior R faces (n-1, n)
        self.AZ = (Rc * dR)[:, None] * np.ones((1, n - 1))         # interior z faces (n, n-1)
        self.ARo = Re[-1] * dz                                    # outer R face per z cell
        self.AZo = Rc * dR                                        # outer z face per R cell
        self.rbR = np.sqrt(Re[-1] ** 2 + zc ** 2)                 # boundary points
        self.rbZ = np.sqrt(Rc ** 2 + self.ze[-1] ** 2)
        self.rc = np.sqrt(self.RR ** 2 + self.ZZ ** 2)
        self._build()

    def _build(self):
        n = self.n
        idx = np.arange(n * n).reshape(n, n)
        cR = self.AR / self.dRf[:, None]
        cZ = self.AZ / self.dzf[None, :]
        diag = np.zeros((n, n))
        diag[:-1, :] -= cR; diag[1:, :] -= cR
        diag[:, :-1] -= cZ; diag[:, 1:] -= cZ
        self.bR = self.ARo / self.dR_o
        self.bZ = self.AZo / self.dz_o
        diag[-1, :] -= self.bR
        diag[:, -1] -= self.bZ
        rows = [idx.ravel(), idx[:-1, :].ravel(), idx[1:, :].ravel(), idx[:, :-1].ravel(), idx[:, 1:].ravel()]
        cols = [idx.ravel(), idx[1:, :].ravel(), idx[:-1, :].ravel(), idx[:, 1:].ravel(), idx[:, :-1].ravel()]
        vals = [diag.ravel(), cR.ravel(), cR.ravel(), cZ.ravel(), cZ.ravel()]
        L = sparse.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n * n, n * n))
        self.lu = splu(L)

    def poisson(self, rho, phib_R, phib_Z):
        rhs = 4 * math.pi * G * rho * self.VOL
        rhs[-1, :] -= self.bR * phib_R
        rhs[:, -1] -= self.bZ * phib_Z
        return self.lu.solve(rhs.ravel()).reshape(self.n, self.n)

    def grad(self, Phi, phib_R, phib_Z):
        """centre values of dPhi/dR and dPhi/dz from face differences (symmetry faces = 0)."""
        n = self.n
        fR = np.zeros((n + 1, n)); fZ = np.zeros((n, n + 1))
        fR[1:-1, :] = (Phi[1:, :] - Phi[:-1, :]) / self.dRf[:, None]
        fR[-1, :] = (phib_R - Phi[-1, :]) / self.dR_o
        fZ[:, 1:-1] = (Phi[:, 1:] - Phi[:, :-1]) / self.dzf[None, :]
        fZ[:, -1] = (phib_Z - Phi[:, -1]) / self.dz_o
        # linear interpolation from faces to centres
        wR = (self.Rc - self.Re[:-1]) / self.dR
        wZ = (self.zc - self.ze[:-1]) / self.dz
        dPdR = fR[:-1, :] * (1 - wR[:, None]) + fR[1:, :] * wR[:, None]
        dPdz = fZ[:, :-1] * (1 - wZ[None, :]) + fZ[:, 1:] * wZ[None, :]
        return dPdR, dPdz

    def phantom_source(self, PhiN, phibR, phibZ, nu_c):
        """4 pi G rho_ph * VOL = sum_faces A_f (nu_f - 1) (PhiN_nb - PhiN_c)/d_f  (FV divergence)."""
        n = self.n
        q = np.zeros((n, n))
        nuR = 0.5 * (nu_c[1:, :] + nu_c[:-1, :]) - 1
        nuZ = 0.5 * (nu_c[:, 1:] + nu_c[:, :-1]) - 1
        flR = self.AR / self.dRf[:, None] * nuR * (PhiN[1:, :] - PhiN[:-1, :])
        flZ = self.AZ / self.dzf[None, :] * nuZ * (PhiN[:, 1:] - PhiN[:, :-1])
        q[:-1, :] += flR; q[1:, :] -= flR
        q[:, :-1] += flZ; q[:, 1:] -= flZ
        q[-1, :] += self.bR * (nu_c[-1, :] - 1) * (phibR - PhiN[-1, :])
        q[:, -1] += self.bZ * (nu_c[:, -1] - 1) * (phibZ - PhiN[:, -1])
        return q / (4 * math.pi * G * self.VOL)

    def shell_average(self, rho, nb=400):
        """spherical shell average on log bins of r (cell-volume weighted), mapped back to cells."""
        r = self.rc.ravel(); w = self.VOL.ravel(); v = rho.ravel()
        edges = np.concatenate([[0], np.geomspace(0.01, r.max() * 1.0001, nb)])
        k = np.clip(np.searchsorted(edges, r) - 1, 0, nb - 1)
        num = np.bincount(k, weights=v * w, minlength=nb)
        den = np.bincount(k, weights=w, minlength=nb)
        avg = np.where(den > 0, num / np.maximum(den, 1e-300), 0.0)
        return avg[k].reshape(rho.shape)

    def enclosed(self, rho, rs):
        r = self.rc.ravel(); m = (2 * math.pi * rho * self.VOL).ravel() * 2   # both hemispheres
        o = np.argsort(r); cm = np.cumsum(m[o])
        return np.interp(rs, r[o], cm)


def phi_kepler(M, r):
    return -G * M / r


def phi_qumond_sph(Mb, a0, r):
    """far-field spherical QUMOND potential (exact in spherical symmetry), zero at r = 1000 kpc."""
    rr = np.geomspace(1000.0, max(np.max(r), 1001.0) * 1.01, 4000)
    gN = G * Mb / rr ** 2
    g = nu_mono(gN / a0) * gN
    Phi = np.concatenate([[0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(rr))])
    return np.interp(r, rr, Phi)


# ------------------------------------------------------------------ a solved model
class Model:
    """field of one model on the grid: Phi, dPhi/dR, dPhi/dz, rho_dark; plus analytic NFW pieces."""

    def __init__(self, name, g, Phi, phibR, phibZ, rho_dark, nfw=None, Phi_bar=None, extra=None):
        self.name, self.g, self.Phi = name, g, Phi
        self.dPdR, self.dPdz = g.grad(Phi, phibR, phibZ)
        self.rho_dark = rho_dark
        self.nfw = nfw
        self.Phi_bar = Phi_bar
        self.extra = extra or {}
        pts = (g.Rc, g.zc)
        kw = dict(bounds_error=False, fill_value=None)
        self._iP = RegularGridInterpolator(pts, Phi, **kw)
        self._iR = RegularGridInterpolator(pts, self.dPdR, **kw)
        self._iZ = RegularGridInterpolator(pts, self.dPdz, **kw)
        self._iD = RegularGridInterpolator(pts, rho_dark, **kw) if rho_dark is not None else None

    def _clip(self, R, z):
        R = np.clip(np.abs(R), self.g.Rc[0], self.g.Rc[-1]); za = np.clip(np.abs(z), self.g.zc[0], self.g.zc[-1])
        return R, za

    def phi(self, R, z):
        R, za = self._clip(np.asarray(R, float), np.asarray(z, float))
        out = self._iP(np.stack([R, za], -1))
        if self.nfw is not None:
            out = out + nfw_phi(self.nfw, np.sqrt(R ** 2 + za ** 2))
        return out

    def gRz(self, R, z):
        """returns (dPhi/dR, dPhi/d|z|) >= 0 pulls inward."""
        R0_, z0_ = np.asarray(R, float), np.asarray(z, float)
        R, za = self._clip(R0_, z0_)
        pts = np.stack([R, za], -1)
        dR, dz = self._iR(pts), self._iZ(pts)
        if self.nfw is not None:
            r = np.sqrt(R ** 2 + za ** 2)
            gr = nfw_g(self.nfw, r)
            dR = dR + gr * R / r; dz = dz + gr * za / r
        return dR, dz

    def rho_d(self, R, z):
        R, za = self._clip(np.asarray(R, float), np.asarray(z, float))
        if self.nfw is not None:
            return nfw_rho(self.nfw, np.sqrt(R ** 2 + za ** 2))
        return self._iD(np.stack([R, za], -1))

    def vc(self, R):
        dR, _ = self.gRz(np.asarray(R, float), np.zeros_like(np.asarray(R, float)))
        return np.sqrt(np.maximum(R * dR, 0))

    def Kz(self, R, z):
        _, dz = self.gRz(R, z)
        return dz

    def M_enclosed(self, r, nth=200):
        """Gauss: M(<r) = r^2/G * <g_r> over the sphere."""
        mu = np.linspace(-1, 1, 2 * nth + 1)[1:-1:2] if False else (np.arange(nth) + 0.5) / nth   # cos(theta) in (0,1)
        out = []
        for rr in np.atleast_1d(r):
            z = rr * mu; R = rr * np.sqrt(1 - mu ** 2)
            dR, dz = self.gRz(R, z)
            gr = (dR * R + dz * z) / rr
            out.append(rr ** 2 * np.mean(gr) / G)
        return np.array(out)


# ------------------------------------------------------------------ NFW
def nfw_params(M200, c):
    r200 = (3 * M200 / (4 * math.pi * 200 * RHO_CRIT)) ** (1 / 3)
    rs = r200 / c
    m = math.log(1 + c) - c / (1 + c)
    rhos = M200 / (4 * math.pi * rs ** 3 * m)
    return dict(M200=M200, c=c, r200=r200, rs=rs, rhos=rhos)


def nfw_g(p, r):
    x = r / p["rs"]
    return G * 4 * math.pi * p["rhos"] * p["rs"] ** 3 * (np.log1p(x) - x / (1 + x)) / r ** 2


def nfw_phi(p, r):
    x = r / p["rs"]
    return -4 * math.pi * G * p["rhos"] * p["rs"] ** 3 * np.log1p(x) / r


def nfw_rho(p, r):
    x = r / p["rs"]
    return p["rhos"] / (x * (1 + x) ** 2)


# ------------------------------------------------------------------ data
def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = rows[0]; arr = np.array([[float(x) for x in r] for r in rows[1:]])
    return {h: arr[:, i] for i, h in enumerate(hdr)}


def load_bird(path):
    d = {}
    for l in open(path):
        l = l.split("#")[0].split()
        if len(l) >= 2:
            try:
                d[l[0]] = float(l[1])
            except ValueError:
                pass
    return d


EIL = load_tsv(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
EIL_R, EIL_V = EIL["R_kpc"], EIL["vc_kms"]
EIL_E = np.hypot(0.5 * (EIL["sig_minus"] + EIL["sig_plus"]), 0.02 * EIL_V)
BR = load_tsv(os.path.join(DATA, "mw_kz11_bovyrix2013_table3.tsv"))
BR_R = BR["R_kpc"] + (R0 - 8.0)
BR_K, BR_E = BR["Kz11_o2piG"], BR["dKz11_o2piG"]
BR_E5 = np.hypot(BR_E, 0.05 * BR_K)
BIRD = load_bird(os.path.join(DATA, "mw_halo_bird2022_jeans.txt"))
KZ_UNIT = 2 * math.pi * G * 1e6     # K_z/(2 pi G) in Msun/pc^2: divide (km/s)^2/kpc by this

# ------------------------------------------------------------------ build the framework / rival
T0 = time.time()
P("=" * 110)
P(f"CFG514 directional Milky Way  {'*** MUTATE: spherical phantom ***' if MUTATE else 'PRIMARY'}")
P("=" * 110)
GR = Grid()
P(f"grid: {GR.n}x{GR.n} cells, R,z to {GR.Re[-1]:.0f} kpc; cell at R0: dR = {GR.dR[np.searchsorted(GR.Re, R0)-1]:.3f} kpc")

# ---- K1 / K2: Plummer controls
P("\n--- numerical controls")
Mp, bp = 1e11, 3.0
rho_pl = 3 * Mp / (4 * math.pi * bp ** 3) * (1 + GR.rc ** 2 / bp ** 2) ** -2.5
phR = -G * Mp / np.sqrt(GR.rbR ** 2 + bp ** 2); phZ = -G * Mp / np.sqrt(GR.rbZ ** 2 + bp ** 2)
Phi_pl = GR.poisson(rho_pl, phR, phZ)
mpl = Model("plummer", GR, Phi_pl, phR, phZ, None)
rt = np.array([1, 2, 5, 10, 20, 50, 100.0]); mu_t = np.array([0.0, 0.5, 0.9])
err1 = 0; err2 = 0
for mu in mu_t:
    R = rt * np.sqrt(1 - mu ** 2); z = rt * mu
    dR, dz = mpl.gRz(R, z); gnum = np.hypot(dR, dz)
    gan = G * Mp * rt / (rt ** 2 + bp ** 2) ** 1.5
    err1 = max(err1, np.max(np.abs(gnum / gan - 1)))
check(err1 < 0.01, f"K1 Newtonian Plummer |g| vs analytic, r = 1-100 kpc, three directions: max dev {err1:.2e} (< 1%)")
a0c = A0["canonical"]
nuc = nu_mono(np.hypot(*GR.grad(Phi_pl, phR, phZ)) / a0c)
rph = GR.phantom_source(Phi_pl, phR, phZ, nuc)
pbR = phi_qumond_sph(Mp, a0c, GR.rbR); pbZ = phi_qumond_sph(Mp, a0c, GR.rbZ)
Phi_q = GR.poisson(rho_pl + rph, pbR, pbZ)
mq = Model("plummerQ", GR, Phi_q, pbR, pbZ, None)
for mu in mu_t:
    R = rt * np.sqrt(1 - mu ** 2); z = rt * mu
    dR, dz = mq.gRz(R, z); gnum = np.hypot(dR, dz)
    gN = G * Mp * rt / (rt ** 2 + bp ** 2) ** 1.5
    err2 = max(err2, np.max(np.abs(gnum / (nu_mono(gN / a0c) * gN) - 1)))
check(err2 < 0.02, f"K2 QUMOND Plummer |g| vs exact spherical nu(g_N) g_N: max dev {err2:.2e} (< 2%)")

# ---- baryons, Newtonian
rho_b1 = rho_baryon(GR.RR, GR.ZZ)
Mb1 = 2 * np.sum(2 * math.pi * rho_b1 * GR.VOL)
# analytic total: discs 2 pi S0 Rd^2 each; bulge and gas by a fine direct integral
Rf = np.geomspace(1e-4, 80, 3000); zf = np.geomspace(1e-5, 30, 3000)
RRf, ZZf = np.meshgrid(Rf, zf, indexing="ij")
Mb_direct = 2 * np.trapz(np.trapz(2 * math.pi * RRf * rho_baryon(RRf, ZZf), zf, axis=1), Rf)
check(abs(Mb1 / Mb_direct - 1) < 0.02, f"K3a baryon mass on the grid {Mb1:.4e} vs direct integral {Mb_direct:.4e} Msun ({Mb1/Mb_direct-1:+.2%})")
phNR = phi_kepler(Mb1, GR.rbR); phNZ = phi_kepler(Mb1, GR.rbZ)
PhiN1 = GR.poisson(rho_b1, phNR, phNZ)
mN1 = Model("baryons", GR, PhiN1, phNR, phNZ, None)
zcol = np.linspace(0, 1.1, 4001)
sig_direct = 2 * np.trapz(rho_baryon(np.full_like(zcol, R0), zcol), zcol) / 1e6
sig_solver = mN1.Kz(np.array([R0]), np.array([1.1]))[0] / KZ_UNIT
check(abs(sig_solver / sig_direct - 1) < 0.03,
      f"K3b Newtonian K_z(R0, 1.1)/2piG = {sig_solver:.1f} vs direct column {sig_direct:.1f} Msun/pc^2 ({sig_solver/sig_direct-1:+.2%})"
      f"  [K_z also carries the radial-force term, so a few % is expected]")
vN_R0 = mN1.vc(np.array([R0]))[0]
P(f"  baryons alone: M_b = {Mb1:.3e} Msun, v_c(R0) = {vN_R0:.1f} km/s")


def build_framework(A, foot, edge, label):
    a0 = A0[foot]
    rho_b = A * rho_b1; Mb = A * Mb1
    PhiN = A * PhiN1; pNR, pNZ = A * phNR, A * phNZ
    dR, dz = GR.grad(PhiN, pNR, pNZ)
    nu_c = nu_mono(np.hypot(dR, dz) / a0)
    rho_ph = GR.phantom_source(PhiN, pNR, pNZ, nu_c)
    rM = math.sqrt(G * Mb / a0)
    r_edge = rM / math.log(1 / (1 - F_B))
    rho_ph_full = rho_ph.copy()
    if edge:
        rho_ph = np.where(GR.rc > r_edge, 0.0, rho_ph)
    if MUTATE:
        rho_ph = GR.shell_average(rho_ph)
    if edge:
        Mph = 2 * np.sum(2 * math.pi * rho_ph * GR.VOL)
        pbR, pbZ = phi_kepler(Mb + Mph, GR.rbR), phi_kepler(Mb + Mph, GR.rbZ)
    else:
        pbR, pbZ = phi_qumond_sph(Mb, a0, GR.rbR), phi_qumond_sph(Mb, a0, GR.rbZ)
    Phi = GR.poisson(rho_b + rho_ph, pbR, pbZ)
    neg = np.sum(np.minimum(rho_ph_full, 0) * GR.VOL * (GR.rc < 100)) / np.sum(np.abs(rho_ph_full) * GR.VOL * (GR.rc < 100))
    m = Model(label, GR, Phi, pbR, pbZ, rho_ph, Phi_bar=PhiN,
              extra=dict(A=A, foot=foot, edge=edge, Mb=Mb, rM=rM, r_edge=r_edge, neg_frac=float(neg), rho_ph_full=rho_ph_full))
    return m


def chi2_rc(m):
    return float(np.sum(((m.vc(EIL_R) - EIL_V) / EIL_E) ** 2))


MODELS = {}
FITS = {}
for foot in ("canonical", "alt"):
    for edge in (False, True):
        base = "F0e" if edge else "F0"
        m0 = build_framework(1.0, foot, edge, f"{base}_{foot}")
        MODELS[m0.name] = m0
        FITS[m0.name] = dict(A=1.0, chi2_rc=chi2_rc(m0), npar=0)
        res = minimize_scalar(lambda A: chi2_rc(build_framework(A, foot, edge, "tmp")), bounds=(0.6, 2.5), method="bounded",
                              options=dict(xatol=2e-3))
        mA = build_framework(res.x, foot, edge, f"{'FAe' if edge else 'FA'}_{foot}")
        MODELS[mA.name] = mA
        FITS[mA.name] = dict(A=float(res.x), chi2_rc=chi2_rc(mA), npar=1)

# NFW rival (same baryons, A = 1) -- independent of footing and of MUTATE


def nfw_model(M200, c):
    p = nfw_params(M200, c)
    return Model("N", GR, PhiN1, phNR, phNZ, None, nfw=p)


def nfw_resid(x):
    m = nfw_model(10 ** x[0], x[1])
    return (m.vc(EIL_R) - EIL_V) / EIL_E


fitN = least_squares(nfw_resid, x0=[12.0, 10.0], bounds=([11.0, 1.0], [13.3, 40.0]))
MN = nfw_model(10 ** fitN.x[0], fitN.x[1])
MN.name = "N"
J = fitN.jac
try:
    cov = np.linalg.inv(J.T @ J); okcov = np.all(np.isfinite(cov)) and np.all(np.diag(cov) > 0)
except np.linalg.LinAlgError:
    okcov = False; cov = np.full((2, 2), np.nan)
FITS["N"] = dict(log10M200=float(fitN.x[0]), c=float(fitN.x[1]), chi2_rc=float(np.sum(fitN.fun ** 2)), npar=2,
                 err_logM=float(np.sqrt(cov[0, 0])) if okcov else None, err_c=float(np.sqrt(cov[1, 1])) if okcov else None,
                 rs=MN.nfw["rs"], r200=MN.nfw["r200"])
check(okcov, f"K6 NFW fit converged: log M200 = {fitN.x[0]:.3f} +- {FITS['N']['err_logM']}, c = {fitN.x[1]:.2f} +- {FITS['N']['err_c']}")

# ---- K4, K5
for foot in ("canonical", "alt"):
    m = MODELS[f"F0_{foot}"]; a0 = A0[foot]
    rr = np.array([40.0, 50.0, 60.0])
    gN = G * m.extra["Mb"] / rr ** 2
    vs = np.sqrt(nu_mono(gN / a0) * gN * rr)
    dev = np.max(np.abs(m.vc(rr) / vs - 1))
    check(dev < 0.03, f"K4 [{foot}] F0 midplane v_c at 40-60 kpc vs spherical nu(gN)gN: max dev {dev:.2%} (< 3%)")
if MUTATE:
    for foot in ("canonical", "alt"):
        m = MODELS[f"F0_{foot}"]
        rr = np.array([5, 10, 20, 50, 100.0])
        Mmut = GR.enclosed(m.rho_dark, rr); Morig = GR.enclosed(m.extra["rho_ph_full"], rr)
        dev = np.max(np.abs(Mmut / Morig - 1))
        check(dev < 0.005, f"K5 [{foot}] sphericalised phantom keeps M_ph(<r) at 5-100 kpc: max dev {dev:.2e} (< 0.5%)")
else:
    P("  K5 applies to the MUTATE run only")

P("\n--- rotation-curve fits (Eilers+19, 38 points, sigma = stat (+) 2%)")
P(f"  {'model':<16}{'A':>7}{'chi2':>9}{'npar':>5}{'v_c(R0)':>9}{'M_b':>11}{'r_M':>7}{'r_edge':>8}{'neg ph':>8}")
for k, m in MODELS.items():
    f = FITS[k]
    P(f"  {k:<16}{f['A']:>7.3f}{f['chi2_rc']:>9.1f}{f['npar']:>5d}{m.vc(np.array([R0]))[0]:>9.1f}{m.extra['Mb']:>11.3e}"
      f"{m.extra['rM']:>7.2f}{m.extra['r_edge']:>8.1f}{m.extra['neg_frac']:>8.3f}")
P(f"  {'N (NFW)':<16}{'1.000':>7}{FITS['N']['chi2_rc']:>9.1f}{2:>5d}{MN.vc(np.array([R0]))[0]:>9.1f}   M200 = {10**fitN.x[0]:.3e}, c = {fitN.x[1]:.2f}, rs = {MN.nfw['rs']:.1f} kpc")

RESULTS = dict(mutate=MUTATE, fits=FITS, checks=None)
VERD = {}
FOOTS = ("canonical", "alt")
FVARS = ("F0", "FA")


def fw(var, foot, edge=False):
    return MODELS[f"{var}{'e' if edge else ''}_{foot}"]


# ================================================================== O1  K_z,1.1(R) vs Bovy & Rix
P("\n" + "=" * 110 + "\nO1  K_z,1.1(R) vs Bovy & Rix 2013 (43 MAPs)\n" + "=" * 110)


def expfit(Rv, K, e):
    def r(x):
        return (x[0] * np.exp(-(Rv - R0) / x[1]) - K) / e
    f = least_squares(r, x0=[70, 2.7])
    Jm = f.jac; cv = np.linalg.inv(Jm.T @ Jm) * max(1.0, np.sum(f.fun ** 2) / (len(K) - 2))
    return f.x, np.sqrt(np.diag(cv))


(dK0, dh), (edK0, edh) = expfit(BR_R, BR_K, BR_E5)
(dK0s, dhs), (edK0s, edhs) = expfit(BR_R, BR_K, BR_E)
P(f"  data exponential refit (sigma (+) 5%): K0 = {dK0:.1f} +- {edK0:.1f}, h = {dh:.2f} +- {edh:.2f} kpc;  stat-only: K0 = {dK0s:.1f}, h = {dhs:.2f} +- {edhs:.2f}")
o1 = {}


def o1_stats(m):
    Km = m.Kz(BR_R, np.full_like(BR_R, 1.1)) / KZ_UNIT
    c5 = float(np.sum(((Km - BR_K) / BR_E5) ** 2)); cs = float(np.sum(((Km - BR_K) / BR_E) ** 2))
    (k0, h), _ = expfit(BR_R, Km, BR_E5)
    return dict(chi2=c5, chi2_stat=cs, K0=float(k0), h=float(h), K_R0=float(m.Kz(np.array([R0]), np.array([1.1]))[0] / KZ_UNIT))


o1["N"] = o1_stats(MN)
o1["baryons"] = o1_stats(mN1)
P(f"  {'model':<16}{'chi2(5%)':>10}{'chi2stat':>10}{'K(R0)':>8}{'K0fit':>8}{'h':>7}{'dchi2 vs N':>12}")
for nm in ("N", "baryons"):
    s = o1[nm]; P(f"  {nm:<16}{s['chi2']:>10.1f}{s['chi2_stat']:>10.1f}{s['K_R0']:>8.1f}{s['K0']:>8.1f}{s['h']:>7.2f}")
for k, m in MODELS.items():
    s = o1_stats(m); s["dchi2"] = s["chi2"] - o1["N"]["chi2"]; o1[k] = s
    P(f"  {k:<16}{s['chi2']:>10.1f}{s['chi2_stat']:>10.1f}{s['K_R0']:>8.1f}{s['K0']:>8.1f}{s['h']:>7.2f}{s['dchi2']:>+12.1f}")
sg = [np.sign(o1[f"{v}_{f}"]["dchi2"]) * (abs(o1[f"{v}_{f}"]["dchi2"]) >= 4) for v in FVARS for f in FOOTS]
VERD["O1"] = "FAVOURS FRAMEWORK" if all(s < 0 for s in sg) else "FAVOURS NFW" if all(s > 0 for s in sg) else "NOT DIAGNOSTIC"
P(f"  shape (h): data {dh:.2f} +- {edh:.2f}; NFW {o1['N']['h']:.2f} ({(o1['N']['h']-dh)/edh:+.1f} sig); "
  + "; ".join(f"{v}_{f} {o1[f'{v}_{f}']['h']:.2f} ({(o1[f'{v}_{f}']['h']-dh)/edh:+.1f})" for v in FVARS for f in FOOTS))
P(f"  O1 VERDICT (frozen dchi2 rule, both footings and F0/FA): {VERD['O1']}")
RESULTS["O1"] = dict(data=dict(K0=dK0, h=dh, eK0=edK0, eh=edh, h_stat=dhs, eh_stat=edhs), models=o1, verdict=VERD["O1"])

# ================================================================== O2  K_z(z) at R0
P("\n" + "=" * 110 + "\nO2  K_z(z) at R0 (prediction only)\n" + "=" * 110)
zz = np.array([0.25, 0.5, 0.75, 1.1, 1.5, 2.0, 3.0, 4.0])
o2 = {"z": zz.tolist()}
KN = MN.Kz(np.full_like(zz, R0), zz) / KZ_UNIT
o2["N"] = KN.tolist()
P("  z [kpc]       " + "".join(f"{z:>8.2f}" for z in zz) + "     S=K(1.1)/K(4)")
P(f"  {'N':<14}" + "".join(f"{k:>8.1f}" for k in KN) + f"{KN[3]/KN[-1]:>12.3f}")
o2["S_N"] = float(KN[3] / KN[-1])
for k, m in MODELS.items():
    K = m.Kz(np.full_like(zz, R0), zz) / KZ_UNIT
    o2[k] = K.tolist(); o2[f"S_{k}"] = float(K[3] / K[-1]); o2[f"ratio_{k}"] = (K / KN).tolist()
    P(f"  {k:<14}" + "".join(f"{x:>8.1f}" for x in K) + f"{K[3]/K[-1]:>12.3f}")
for k in MODELS:
    P(f"  ratio {k:<10}" + "".join(f"{x:>8.3f}" for x in o2[f'ratio_{k}']))
# vertical shape of the dark component alone at R0: K_z,dark(z)/K_z,dark(4)
P("  dark-only vertical force at R0 (framework: total minus Newtonian baryons; NFW: halo):")
for k in ("F0_canonical", "FA_canonical", "F0_alt"):
    m = MODELS[k]
    Kd = (m.Kz(np.full_like(zz, R0), zz) - m.extra["A"] * mN1.Kz(np.full_like(zz, R0), zz)) / KZ_UNIT
    o2[f"dark_{k}"] = Kd.tolist()
    P(f"  {k:<14}" + "".join(f"{x:>8.1f}" for x in Kd) + f"   S_dark = {Kd[3]/Kd[-1]:.3f}")
KdN = (KN - mN1.Kz(np.full_like(zz, R0), zz) / KZ_UNIT)
o2["dark_N"] = KdN.tolist()
P(f"  {'N':<14}" + "".join(f"{x:>8.1f}" for x in KdN) + f"   S_dark = {KdN[3]/KdN[-1]:.3f}")
VERD["O2"] = "NOT DIAGNOSTIC (prediction only; no K_z(z) table on disk)"
RESULTS["O2"] = o2

# ================================================================== O3  flattening
P("\n" + "=" * 110 + "\nO3  potential flattening q_Phi(r) and dark-density axis ratio (prediction only)\n" + "=" * 110)
rq = np.array([10.0, 20.0, 30.0, 50.0, 100.0])


def qphi(phifun, r):
    target = phifun(np.array([r]), np.array([0.0]))[0]
    f = lambda z: phifun(np.array([GR.Rc[0]]), np.array([z]))[0] - target
    lo, hi = 0.05 * r, 1.5 * r
    if f(lo) * f(hi) > 0:
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-6 * r) / r


def qrho(rhofun, r):
    target = rhofun(np.array([r]), np.array([0.0]))[0]
    f = lambda z: rhofun(np.array([GR.Rc[0]]), np.array([z]))[0] - target
    lo, hi = 0.05 * r, 2.0 * r
    try:
        if not (target > 0) or f(lo) * f(hi) > 0:
            return float("nan")
        return brentq(f, lo, hi, xtol=1e-6 * r) / r
    except ValueError:
        return float("nan")


o3 = {"r": rq.tolist()}
qN_tot = [qphi(MN.phi, r) for r in rq]
o3["N"] = dict(qphi_tot=qN_tot, qphi_dark=[1.0] * len(rq), qrho_dark=[1.0] * len(rq), pole_plane_rho=[1.0] * len(rq))
P(f"  r [kpc]                 " + "".join(f"{r:>8.0f}" for r in rq))
P(f"  N  q_Phi total          " + "".join(f"{q:>8.3f}" for q in qN_tot))
for k, m in MODELS.items():
    A = m.extra["A"]
    phid = lambda R, z, m=m, A=A: m.phi(R, z) - A * mN1.phi(R, z)
    qt = [qphi(m.phi, r) for r in rq]; qd = [qphi(phid, r) for r in rq]
    qr = [qrho(m.rho_d, r) for r in rq]
    pp = [float(m.rho_d(np.array([GR.Rc[0]]), np.array([r]))[0] / m.rho_d(np.array([r]), np.array([0.0]))[0]) for r in rq]
    o3[k] = dict(qphi_tot=qt, qphi_dark=qd, qrho_dark=qr, pole_plane_rho=pp)
    P(f"  {k:<14} q_Phi tot " + "".join(f"{q:>8.3f}" for q in qt))
    P(f"  {'':<14} q_Phi dark" + "".join(f"{q:>8.3f}" for q in qd))
    P(f"  {'':<14} q_rho dark" + "".join(f"{q:>8.3f}" for q in qr))
    P(f"  {'':<14} rho pole/plane" + "".join(f"{q:>8.3f}" for q in pp))
VERD["O3"] = "NOT DIAGNOSTIC (prediction only; stream constraints not on disk)"
RESULTS["O3"] = o3

# local phantom-disc diagnostics
P("\n  local dark density at the Sun and dark column |z|<1.1 kpc at R0:")
loc = {}
zl = np.linspace(0, 1.1, 2201)
for k, m in list(MODELS.items()) + [("N", MN)]:
    rl = float(m.rho_d(np.array([R0]), np.array([0.0]))[0]) / 1e9
    col = float(2 * np.trapz(m.rho_d(np.full_like(zl, R0), zl), zl)) / 1e6
    loc[k] = dict(rho_dark_sun_Msun_pc3=rl, Sigma_dark_1p1_Msun_pc2=col)
    P(f"  {k:<16} rho_dark(R0,0) = {rl:.4f} Msun/pc^3   Sigma_dark(|z|<1.1) = {col:.1f} Msun/pc^2")
RESULTS["local"] = loc

# ================================================================== O4  DESI BHB latitude test
P("\n" + "=" * 110 + "\nO4  halo-star dispersion by Galactocentric latitude: DESI DR1 MWS BHB stars\n" + "=" * 110)
os.makedirs(WORK, exist_ok=True)
cache = os.path.join(WORK, "cfg514_desi_bhb.npz")


def build_bhb():
    from astropy.io import fits
    keep = []
    files = sorted(glob.glob(os.path.join(DESI_DIR, "rvtab_*.fits")))
    for i, f in enumerate(files):
        try:
            with fits.open(f, memmap=False) as h:
                rv = h["RVTAB"].data; fm = h["FIBERMAP"].data
                sel = ((rv["SUCCESS"] == 1) & (rv["RVS_WARN"] == 0) & (np.char.strip(rv["RR_SPECTYPE"].astype(str)) == "STAR")
                       & (rv["VRAD_ERR"] < 10) & (rv["TEFF"] >= 7000) & (rv["TEFF"] <= 9500) & (rv["LOGG"] >= 2.5)
                       & (rv["LOGG"] <= 3.75) & (rv["FEH"] < -1.2))
                if not np.any(sel):
                    continue
                assert np.all(rv["TARGETID"] == fm["TARGETID"])
                for j in np.where(sel)[0]:
                    keep.append((rv["TARGETID"][j], rv["TARGET_RA"][j], rv["TARGET_DEC"][j], rv["VRAD"][j], rv["VRAD_ERR"][j],
                                 fm["FLUX_G"][j], fm["FLUX_R"][j], fm["EBV"][j], rv["FEH"][j], rv["TEFF"][j], rv["LOGG"][j]))
        except Exception as e:  # noqa
            P(f"    skip {os.path.basename(f)}: {e}")
    a = np.array(keep, dtype=float) if keep else np.zeros((0, 11))
    np.savez(cache, a=a, nfiles=len(files))
    return a, len(files)


if os.path.exists(cache):
    z_ = np.load(cache); bhb, nfiles = z_["a"], int(z_["nfiles"])
    P(f"  BHB candidate rows read from cache {os.path.basename(cache)} ({nfiles} files scanned)")
else:
    bhb, nfiles = build_bhb()
    P(f"  scanned {nfiles} rvtab files")
P(f"  rows passing the spectroscopic cuts: {len(bhb)}")
o4 = dict(n_spec=int(len(bhb)))
if len(bhb):
    # one row per TARGETID, lowest VRAD_ERR
    o = np.lexsort((bhb[:, 4], bhb[:, 0])); b = bhb[o]
    _, first = np.unique(b[:, 0], return_index=True); b = b[first]
    tid, ra, dec, vr, evr, fg, fr, ebv, feh, teff, logg = b.T
    ok = (fg > 0) & (fr > 0)
    g0 = 22.5 - 2.5 * np.log10(np.where(ok, fg, 1)) - 3.214 * ebv
    r0 = 22.5 - 2.5 * np.log10(np.where(ok, fr, 1)) - 2.165 * ebv
    gr = g0 - r0
    ok &= (gr >= -0.25) & (gr <= 0.0)
    Mg = 0.434 - 0.169 * gr + 2.319 * gr ** 2 + 20.449 * gr ** 3 + 94.517 * gr ** 4
    d = 10 ** ((g0 - Mg - 10) / 5)          # kpc
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    sc = SkyCoord(ra=ra * u.deg, dec=dec * u.deg).galactic
    l, bb = sc.l.rad, sc.b.rad
    X = R0 - d * np.cos(l) * np.cos(bb); Y = d * np.sin(l) * np.cos(bb); Z = d * np.sin(bb)
    Rg = np.hypot(X, Y); rg = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    vgsr = vr + UVW[0] * np.cos(l) * np.cos(bb) + UVW[1] * np.sin(l) * np.cos(bb) + UVW[2] * np.sin(bb)
    th = np.degrees(np.arcsin(np.abs(Z) / np.maximum(rg, 1e-9)))
    o4["n_unique"] = int(len(b)); o4["n_colour"] = int(ok.sum())

    def ml_sigma(v, e):
        def nll(s):
            var = s ** 2 + e ** 2
            mu = np.sum(v / var) / np.sum(1 / var)
            return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
        return minimize_scalar(nll, bounds=(1, 400), method="bounded").x

    rng = np.random.default_rng(514)

    def ratio_stats(sel_p, sel_q):
        vp, ep = vgsr[sel_p], evr[sel_p]; vq, eq = vgsr[sel_q], evr[sel_q]
        rat = ml_sigma(vp, ep) / ml_sigma(vq, eq)
        bs = []
        for _ in range(1000):
            ip = rng.integers(0, len(vp), len(vp)); iq = rng.integers(0, len(vq), len(vq))
            bs.append(ml_sigma(vp[ip], ep[ip]) / ml_sigma(vq[iq], eq[iq]))
        return float(rat), float(np.std(bs))

    # Jeans predictions
    def jeans_sigma_grid(m, qt):
        rt_ = np.sqrt(GR.RR ** 2 + (GR.ZZ / qt) ** 2)
        nt = np.where(rt_ < 22, (rt_ / 22) ** -3.5, (rt_ / 22) ** -4.7)
        dz = m.gRz(GR.RR.ravel(), GR.ZZ.ravel())[1].reshape(GR.RR.shape)
        integ = nt * dz * GR.dz[None, :]
        tail = np.cumsum(integ[:, ::-1], axis=1)[:, ::-1] - 0.5 * integ
        return np.sqrt(np.maximum(tail / nt, 0))

    def pred_ratio(m, qt, sel_p, sel_q):
        sg = jeans_sigma_grid(m, qt)
        it = RegularGridInterpolator((GR.Rc, GR.zc), sg, bounds_error=False, fill_value=None)
        sp = it(np.stack([Rg[sel_p], np.abs(Z[sel_p])], -1)); sq = it(np.stack([Rg[sel_q], np.abs(Z[sel_q])], -1))
        return float(np.sqrt(np.mean(sp ** 2)) / np.sqrt(np.mean(sq ** 2)))

    for win, (rlo, rhi) in (("primary", (15, 40)), ("variant", (10, 60))):
        inr = ok & (rg >= rlo) & (rg <= rhi)
        sp = inr & (th > 50); sq = inr & (th < 30)
        rec = dict(r=[rlo, rhi], n_pole=int(sp.sum()), n_plane=int(sq.sum()))
        P(f"  [{win} r {rlo}-{rhi} kpc] stars: pole {sp.sum()}, plane {sq.sum()}")
        if sp.sum() >= 10 and sq.sum() >= 10:
            rat, erat = ratio_stats(sp, sq)
            rec.update(measured=rat, err=erat,
                       sigma_pole=float(ml_sigma(vgsr[sp], evr[sp])), sigma_plane=float(ml_sigma(vgsr[sq], evr[sq])))
            P(f"    measured sigma_pole = {rec['sigma_pole']:.1f}, sigma_plane = {rec['sigma_plane']:.1f} km/s, ratio = {rat:.3f} +- {erat:.3f}")
            for qt in (1.0, 0.7):
                pN = pred_ratio(MN, qt, sp, sq); rec[f"N_q{qt}"] = pN
                line = f"    q_t={qt}: N {pN:.4f}"
                gate = []
                for k in ("F0_canonical", "F0_alt", "FA_canonical", "FA_alt"):
                    pF = pred_ratio(MODELS[k], qt, sp, sq); rec[f"{k}_q{qt}"] = pF
                    line += f" | {k} {pF:.4f} (dF-N {pF-pN:+.4f})"
                    gate.append(abs(pF - pN) >= erat)
                rec[f"gate_q{qt}"] = bool(any(gate))
                P(line)
                P(f"    power gate q_t={qt}: |F-N| >= sigma(measured) = {erat:.3f}?  {'OPEN' if any(gate) else 'CLOSED -> NOT DIAGNOSTIC'}")
                if any(gate):
                    zN = (rat - pN) / erat
                    zF = {k: (rat - rec[f'{k}_q{qt}']) / erat for k in ("F0_canonical", "F0_alt", "FA_canonical", "FA_alt")}
                    rec[f"z_q{qt}"] = dict(N=zN, **zF)
                    P(f"    z: N {zN:+.2f}; " + "; ".join(f"{k} {v:+.2f}" for k, v in zF.items()))
        o4[win] = rec
    prim = o4.get("primary", {})
    if prim.get("measured") is None or not prim.get("gate_q1.0", False):
        VERD["O4"] = "NOT DIAGNOSTIC (power gate closed)" if prim.get("measured") is not None else "NOT DIAGNOSTIC (too few stars)"
    else:
        zz_ = prim["z_q1.0"]
        fav_f = all(abs(zz_["N"]) - abs(zz_[k]) >= 2 for k in zz_ if k != "N")
        fav_n = all(abs(zz_[k]) - abs(zz_["N"]) >= 2 for k in zz_ if k != "N")
        VERD["O4"] = "FAVOURS FRAMEWORK" if fav_f else "FAVOURS NFW" if fav_n else "NOT DIAGNOSTIC"
else:
    VERD["O4"] = "NOT DIAGNOSTIC (no stars)"
P(f"  O4 VERDICT: {VERD['O4']}")
RESULTS["O4"] = o4

# ================================================================== O5  satellites, power only
P("\n" + "=" * 110 + "\nO5  satellites by direction (power argument; no positions on disk)\n" + "=" * 110)
o5 = {}
half_err = math.sqrt(2) * 21.4 / 231.9
for k in ("F0_canonical", "F0_alt", "FA_canonical", "N"):
    m = MODELS.get(k, MN)
    vals = []
    for r in (30.0, 50.0, 78.0, 100.0):
        vpole = math.sqrt(r * m.gRz(np.array([GR.Rc[0]]), np.array([r]))[1][0])
        vpl = math.sqrt(r * m.gRz(np.array([r]), np.array([0.0]))[0][0])
        vals.append(vpole / vpl)
    o5[k] = vals
    P(f"  {k:<14} V_c(pole)/V_c(plane) at r = 30/50/78/100 kpc: " + " ".join(f"{v:.4f}" for v in vals))
dmax = max(abs(o5[k][i] - o5["N"][i]) for k in o5 if k != "N" for i in range(4))
o5["half_sample_err"] = half_err; o5["max_F_minus_N"] = dmax
P(f"  largest |F - N| = {dmax:.4f} vs half-sample error {half_err:.3f}: {'below' if dmax < half_err else 'above'}")
VERD["O5"] = "NOT DIAGNOSTIC (predicted gap below the half-sample error; positions not on disk)" if dmax < half_err else "NOT DIAGNOSTIC (positions not on disk)"
RESULTS["O5"] = o5

# ================================================================== sightline utilities
LB = {"GC": (0.0, 0.0), "anticentre": (180.0, 0.0), "NGP": (0.0, 90.0), "Baade": (1.0, -3.9),
      "LMC": (280.5, -32.9), "SMC": (302.8, -44.3), "M31": (121.2, -21.6)}


def sight(lb, s):
    l, b = np.radians(lb[0]), np.radians(lb[1])
    X = R0 - s * np.cos(l) * np.cos(b); Y = s * np.sin(l) * np.cos(b); Z = s * np.sin(b)
    return np.hypot(X, Y), Z


def line_int(fun, lb, D, n=4000, weight=None):
    s = np.concatenate([[0], np.geomspace(1e-3, D, n)])
    R, Z = sight(lb, s)
    v = fun(R, Z)
    if weight is not None:
        v = v * weight(s)
    return np.trapz(v, s)


# ================================================================== O6  Shapiro and redshift
P("\n" + "=" * 110 + "\nO6  Shapiro delay and gravitational redshift by direction (prediction only)\n" + "=" * 110)
o6 = {}
cmp_models = [("N", MN)] + [(k, MODELS[k]) for k in ("F0_canonical", "F0_alt", "FA_canonical")]
for D in (1.0, 8.0, 50.0):
    P(f"  differential Shapiro delay to D = {D:.0f} kpc relative to the NGP direction [days]:")
    for k, m in cmp_models:
        row = {}
        ref = line_int(m.phi, LB["NGP"], D)
        for nm in ("GC", "anticentre", "Baade", "LMC", "SMC", "M31"):
            dI = line_int(m.phi, LB[nm], D) - ref           # (km/s)^2 kpc
            dt = -2 * dI / C_KMS ** 3 * KPC_KMS_S / 86400   # days
            row[nm] = dt
        o6[f"shapiro_D{D:.0f}_{k}"] = row
        P(f"    {k:<14}" + " ".join(f"{nm} {v:+9.3f}" for nm, v in row.items()))
P("  gravitational redshift (Phi_source - Phi_sun)/c [km/s] and Phi difference F - N:")
srcs = {"LMC(50)": (LB["LMC"], 50.0), "NGP 20 kpc": (LB["NGP"], 20.0), "GC 20 kpc": (LB["GC"], 20.0),
        "M31-dir 100 kpc": (LB["M31"], 100.0)}
for k, m in cmp_models:
    ps = m.phi(np.array([R0]), np.array([0.0]))[0]
    row = {}
    for nm, (lb, D) in srcs.items():
        R, Z = sight(lb, np.array([D]))
        row[nm] = float((m.phi(R, Z)[0] - ps) / C_KMS)
    o6[f"redshift_{k}"] = row
    P(f"    {k:<14}" + " ".join(f"{nm} {v:+.4f}" for nm, v in row.items()))
for k in ("F0_canonical", "F0_alt", "FA_canonical"):
    P(f"    F-N {k:<10}" + " ".join(f"{nm} {1e3*(o6['redshift_'+k][nm]-o6['redshift_N'][nm]):+.1f} m/s" for nm in srcs))
VERD["O6"] = "NOT DIAGNOSTIC (no measurement; static delays have no reference; redshifts degenerate with systemic velocity)"
RESULTS["O6"] = o6

# ================================================================== O7  microlensing
P("\n" + "=" * 110 + "\nO7  microlensing optical depth (smooth cold energy and CDM both give tau_dark = 0)\n" + "=" * 110)
TAUK = 4 * math.pi * G / C_KMS ** 2     # per (Msun/kpc^3 * kpc^2)
o7 = {}
targets = {"Baade(8.5)": (LB["Baade"], 8.5), "LMC(50)": (LB["LMC"], 50.0), "SMC(62)": (LB["SMC"], 62.0), "M31(MW to 300)": (LB["M31"], 300.0)}
star_fun = lambda R, Z: rho_stars_only(R, Z)
for nm, (lb, Ds) in targets.items():
    w = lambda s, Ds=Ds: s * (Ds - s) / Ds
    tst = TAUK * line_int(star_fun, lb, Ds, weight=w)
    row = dict(tau_stars=tst)
    for k, m in [("N", MN), ("F0_canonical", MODELS["F0_canonical"]), ("F0_alt", MODELS["F0_alt"])]:
        row[f"tau_dark_if_compact_{k}"] = TAUK * line_int(m.rho_d, lb, Ds, weight=w)
    o7[nm] = row
    P(f"  {nm:<16} tau_stars = {tst:.2e};  tau_dark if compact: " + ", ".join(f"{k} {v:.2e}" for k, v in row.items() if k.startswith("tau_dark")))
VERD["O7"] = "NOT DIAGNOSTIC (tau_dark = 0 in both: a smooth field and CDM particles do not microlens)"
RESULTS["O7"] = o7

# ================================================================== O8 / O9  dark convergence and column sky maps
P("\n" + "=" * 110 + "\nO8/O9  dark convergence (to 300 kpc) and dark column (to 100 kpc) over the sky\n" + "=" * 110)
nl, nb = 72, 36
lg = np.linspace(0, 360, nl, endpoint=False) + 2.5
bg = np.degrees(np.arcsin(np.linspace(-1, 1, nb + 1)[:-1] + 1 / nb))
maps = {}
for k, m in [("N", MN), ("F0_canonical", MODELS["F0_canonical"]), ("F0_alt", MODELS["F0_alt"]), ("FA_canonical", MODELS["FA_canonical"])]:
    col = np.zeros((nb, nl)); kap = np.zeros((nb, nl))
    s1 = np.concatenate([[0], np.geomspace(1e-3, 100.0, 1500)])
    s2 = np.concatenate([[0], np.geomspace(1e-3, 300.0, 1800)])
    for i, b_ in enumerate(bg):
        for j, l_ in enumerate(lg):
            R, Z = sight((l_, b_), s1); col[i, j] = np.trapz(m.rho_d(R, Z), s1) / 1e6
            R, Z = sight((l_, b_), s2); kap[i, j] = TAUK * np.trapz(m.rho_d(R, Z) * s2, s2)
    maps[k] = dict(col=col, kap=kap)
o89 = {}
for k, mp in maps.items():
    col, kap = mp["col"], mp["kap"]
    pole = col[np.abs(bg) > 60].mean(); plane = col[np.abs(bg) < 10].mean()
    gcd = col[np.abs(bg) < 10][:, (lg < 30) | (lg > 330)].mean(); acd = col[np.abs(bg) < 10][:, (lg > 150) & (lg < 210)].mean()
    # dipole/quadrupole of kappa (equal-area grid)
    lr, br = np.meshgrid(np.radians(lg), np.radians(bg))
    nx, ny, nz = np.cos(br) * np.cos(lr), np.cos(br) * np.sin(lr), np.sin(br)
    km = kap.mean()
    dip = 3 * np.array([np.mean(kap * nx), np.mean(kap * ny), np.mean(kap * nz)])
    quad_z = np.mean(kap * (3 * nz ** 2 - 1) / 2) * 5
    o89[k] = dict(col_pole=pole, col_plane=plane, plane_over_pole=plane / pole, col_GCdir=gcd, col_anticentre=acd,
                  GC_over_AC=gcd / acd, kappa_mean=km, kappa_dipole=dip.tolist(), kappa_quad_z=quad_z)
    P(f"  {k:<14} column(<100 kpc) [Msun/pc^2]: pole {pole:.1f}, plane {plane:.1f} (x{plane/pole:.2f}), GC-dir {gcd:.1f}, anticentre {acd:.1f} (x{gcd/acd:.2f})"
      f" | kappa mean {km:.2e}, dipole |{np.linalg.norm(dip):.2e}|, quad_z {quad_z:+.2e}")
VERD["O8"] = "NOT DIAGNOSTIC (kappa ~1e-6 with an unobservable uniform part)"
RESULTS["O8_O9"] = o89

# ================================================================== O10 enclosed mass and the edge
P("\n" + "=" * 110 + "\nO10 enclosed mass vs Bird+2022 (radial) and the zero-knob edge\n" + "=" * 110)
pts = [("KG", BIRD["JEANS_KG_r_kpc"], BIRD["JEANS_KG_M_e11"], math.hypot(BIRD["JEANS_KG_Mrand_e11"], BIRD["JEANS_KG_Msys_e11"])),
       ("BHB", BIRD["JEANS_BHB_r_kpc"], BIRD["JEANS_BHB_M_e11"], math.hypot(BIRD["JEANS_BHB_Mrand_e11"], BIRD["JEANS_BHB_Msys_e11"]))]
o10 = {}
for k, m in list(MODELS.items()) + [("N", MN)]:
    zs = []
    rec = {}
    for nm, r, M, e in pts:
        Mm = m.M_enclosed(r)[0] / 1e11
        rec[nm] = dict(M=Mm, z=(Mm - M) / e); zs.append((Mm - M) / e)
    v78 = math.sqrt(G * m.M_enclosed(78.0)[0] / 78.0)
    rec["chi2"] = float(np.sum(np.square(zs))); rec["Vc78"] = v78
    o10[k] = rec
    P(f"  {k:<16} M(<52) = {rec['BHB']['M']:.2f} (z {rec['BHB']['z']:+.2f}), M(<73) = {rec['KG']['M']:.2f} (z {rec['KG']['z']:+.2f}) e11; "
      f"sum z^2 = {rec['chi2']:.2f}; V_c,sph(78 kpc) = {v78:.1f} km/s")
sg = []
for v in ("F0", "FA"):
    for f in FOOTS:
        d = o10[f"{v}_{f}"]["chi2"] - o10["N"]["chi2"]; sg.append(np.sign(d) * (abs(d) >= 4))
VERD["O10"] = "FAVOURS FRAMEWORK" if all(s < 0 for s in sg) else "FAVOURS NFW" if all(s > 0 for s in sg) else "NOT DIAGNOSTIC"
sge = []
for v in ("F0e", "FAe"):
    for f in FOOTS:
        d = o10[f"{v}_{f}"]["chi2"] - o10["N"]["chi2"]; sge.append(np.sign(d) * (abs(d) >= 4))
VERD["O10_edge"] = "FAVOURS FRAMEWORK" if all(s < 0 for s in sge) else "FAVOURS NFW" if all(s > 0 for s in sge) else "NOT DIAGNOSTIC"
P(f"  O10 VERDICT (no edge): {VERD['O10']};  with the edge: {VERD['O10_edge']}")
RESULTS["O10"] = o10

# ================================================================== ranking
P("\n" + "=" * 110 + "\nRANKING: D_now = |F-N|/sigma_now, D_DR4 = |F-N|/sigma_DR4 (declared, unsourced sigma_DR4)\n" + "=" * 110)
rank = {}
for foot in FOOTS:
    for v in FVARS:
        k = f"{v}_{foot}"
        # O1: mean |F-N| over the 6-12 kpc K_z,1.1 run, in units of 2% per bin
        Rr = np.linspace(6, 12, 13)
        KF = MODELS[k].Kz(Rr, np.full_like(Rr, 1.1)); KNr = MN.Kz(Rr, np.full_like(Rr, 1.1))
        frac = np.abs(KF / KNr - 1)
        d1_dr4 = float(np.sqrt(np.sum((frac / 0.02) ** 2)))
        d1_now = float(math.sqrt(abs(o1[k]["dchi2"])))
        # O2: K_z(z) ratio over 8 z-bins at 3%
        rz = np.array(o2[f"ratio_{k}"]); d2 = float(np.sqrt(np.sum(((rz - 1) / 0.03) ** 2)))
        # shape-only O2: the S signature, normalisation removed
        dS = abs(o2[f"S_{k}"] - o2["S_N"]) / (o2["S_N"] * 0.03 * math.sqrt(2))
        # O3: q_Phi total at 20 kpc with sigma 0.05
        q3 = o3[k]["qphi_tot"]; d3 = float(np.nanmax([abs(q3[i] - qN_tot[i]) for i in range(len(rq))]) / 0.05)
        # O4: x sqrt(10) for an assumed x10 DR4 halo sample
        if "measured" in o4.get("primary", {}):
            gap = abs(o4["primary"].get(f"{k}_q1.0", np.nan) - o4["primary"]["N_q1.0"])
            d4n = gap / o4["primary"]["err"]; d4 = d4n * math.sqrt(10)
        else:
            d4n = d4 = float("nan")
        rank[k] = dict(O1_now=d1_now, O1_DR4=d1_dr4, O2_DR4=d2, O2_shape_S_DR4=float(dS), O3_DR4=d3, O4_now=float(d4n), O4_DR4=float(d4),
                       O5_now=dmax / half_err)
        P(f"  {k:<14} O1 now {d1_now:5.1f}, DR4 {d1_dr4:5.1f} | O2 DR4 {d2:5.1f} (shape S {dS:4.1f}) | O3 DR4 {d3:5.1f} | O4 now {d4n:5.2f}, DR4 {d4:5.2f} | O5 now {dmax/half_err:5.3f}")
RESULTS["ranking"] = rank
RESULTS["verdicts"] = VERD

# ================================================================== figure
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    ext = [lg[0] - 2.5, lg[-1] + 2.5, -90, 90]
    for a_, k, t in ((ax[0, 0], "F0_canonical", "framework F0 (canonical)"), (ax[0, 1], "N", "NFW fitted to Eilers+19")):
        im = a_.imshow(np.log10(maps[k]["col"]), origin="lower", aspect="auto",
                       extent=[0, 360, -90, 90], cmap="viridis", vmin=np.log10(maps["N"]["col"].min()) - 0.3,
                       vmax=np.log10(maps["F0_canonical"]["col"].max()))
        a_.set_title(f"dark column to 100 kpc, log Msun/pc$^2$\n{t}")
        a_.set_xlabel("l (deg, equal-area in sin b)"); a_.set_ylabel("b (deg)")
        plt.colorbar(im, ax=a_)
    im = ax[0, 2].imshow(maps["F0_canonical"]["col"] / maps["N"]["col"], origin="lower", aspect="auto", extent=[0, 360, -90, 90], cmap="RdBu_r",
                         vmin=0, vmax=2 * np.median(maps["F0_canonical"]["col"] / maps["N"]["col"]))
    ax[0, 2].set_title("column ratio framework / NFW"); plt.colorbar(im, ax=ax[0, 2])
    Rr = np.linspace(4, 10, 100)
    ax[1, 0].errorbar(BR_R, BR_K, BR_E, fmt="k.", alpha=0.6, label="Bovy & Rix 2013 MAPs")
    for k, c_ in (("N", "C0"), ("F0_canonical", "C3"), ("F0_alt", "C1"), ("FA_canonical", "C2")):
        m = MN if k == "N" else MODELS[k]
        ax[1, 0].plot(Rr, m.Kz(Rr, np.full_like(Rr, 1.1)) / KZ_UNIT, c_, label=k)
    ax[1, 0].plot(Rr, mN1.Kz(Rr, np.full_like(Rr, 1.1)) / KZ_UNIT, "k--", label="baryons")
    ax[1, 0].set_yscale("log"); ax[1, 0].set_xlabel("R (kpc)"); ax[1, 0].set_ylabel(r"$K_{z,1.1}/2\pi G$ (Msun/pc$^2$)"); ax[1, 0].legend(fontsize=8)
    ax[1, 0].set_title("O1: vertical force at 1.1 kpc")
    zp = np.linspace(0.05, 4, 80)
    for k, c_ in (("N", "C0"), ("F0_canonical", "C3"), ("FA_canonical", "C2")):
        m = MN if k == "N" else MODELS[k]
        ax[1, 1].plot(zp, m.Kz(np.full_like(zp, R0), zp) / KZ_UNIT, c_, label=k)
    ax[1, 1].set_xlabel("z (kpc)"); ax[1, 1].set_ylabel(r"$K_z/2\pi G$ at R$_0$"); ax[1, 1].legend(fontsize=8); ax[1, 1].set_title("O2: K_z(z) at the Sun")
    ax[1, 2].plot(rq, qN_tot, "C0o-", label="NFW total")
    for k, c_ in (("F0_canonical", "C3"), ("FA_canonical", "C2")):
        ax[1, 2].plot(rq, o3[k]["qphi_tot"], c_ + "o-", label=f"{k} total")
        ax[1, 2].plot(rq, o3[k]["qphi_dark"], c_ + "s--", label=f"{k} phantom only")
    ax[1, 2].axhline(1, color="k", lw=0.5); ax[1, 2].set_xscale("log"); ax[1, 2].set_xlabel("r (kpc)"); ax[1, 2].set_ylabel(r"$q_\Phi$")
    ax[1, 2].legend(fontsize=8); ax[1, 2].set_title("O3: potential flattening")
    fig.suptitle(f"CFG514 directional Milky Way {'(MUTATE: spherical phantom)' if MUTATE else ''}")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"cfg514_directional{TAG}.png"), dpi=110)
    P(f"\nfigure: cfg514_directional{TAG}.png")
except Exception as e:  # noqa
    P(f"figure failed: {e}")

# ================================================================== MUTATE pass test
exit_code = 0
if MUTATE:
    prim_path = os.path.join(HERE, "cfg514_results.json")
    P("\n" + "=" * 110 + "\nMUTATE comparison with the primary run\n" + "=" * 110)
    if os.path.exists(prim_path):
        prim = json.load(open(prim_path))
        shrink = {}
        for foot in FOOTS:
            for v in FVARS:
                k = f"{v}_{foot}"
                g1p = abs(prim["O1"]["models"][k]["dchi2"]); g1m = abs(o1[k]["dchi2"])
                gSp = abs(prim["O2"][f"S_{k}"] - prim["O2"]["S_N"]); gSm = abs(o2[f"S_{k}"] - o2["S_N"])
                q20p = abs(prim["O3"][k]["qphi_tot"][1] - prim["O3"]["N"]["qphi_tot"][1]); q20m = abs(o3[k]["qphi_tot"][1] - o3["N"]["qphi_tot"][1])
                Kp = abs(prim["O2"][f"ratio_{k}"][3] - 1); Km = abs(o2[f"ratio_{k}"][3] - 1)
                shrink[k] = dict(O1_dchi2=(g1p, g1m), O2_S=(gSp, gSm), O3_q20=(q20p, q20m), O2_Kz11_ratio=(Kp, Km))
                P(f"  {k:<14} |dchi2| {g1p:.1f} -> {g1m:.1f} | |S_F-S_N| {gSp:.3f} -> {gSm:.3f} | |q20_F-q20_N| {q20p:.3f} -> {q20m:.3f} | |K11 F/N-1| {Kp:.3f} -> {Km:.3f}")
        RESULTS["mutate_vs_primary"] = shrink
        sig = all(v["O2_S"][1] <= 0.5 * v["O2_S"][0] and v["O3_q20"][1] <= 0.5 * v["O3_q20"][0] for v in shrink.values())
        P(f"  shape signals (S and q_Phi(20)) shrink by >= 50% in every model: {sig}")
        exit_code = 1 if sig else 0
        P(f"  MUTATE {'DETECTED (shape signal removed): exit 1' if sig else 'NOT DETECTED: exit 0'}")
    else:
        P("  primary results not found; run the primary first")

npass = sum(c for c, _ in CHECKS)
P(f"\nchecks: {npass}/{len(CHECKS)} pass;  run time {time.time()-T0:.0f} s")
P("VERDICTS: " + json.dumps(VERD, indent=1))
RESULTS["checks"] = [dict(ok=c, msg=m) for c, m in CHECKS]


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items() if k != "rho_ph_full"}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


json.dump(_clean(RESULTS), open(os.path.join(HERE, f"cfg514_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg514_directional{TAG}.out"), "w").write("\n".join(OUT_LINES) + "\n")
sys.exit(exit_code)
