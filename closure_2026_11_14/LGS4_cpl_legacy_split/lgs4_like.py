"""LGS4 likelihood module: flat w0-wa (CPL) or constant dark energy, fitted to
  DES-SN5YR Dovekie supernovae (absolute magnitude profiled; optional free magnitude offset on the legacy rows)
  + DESI DR2 BAO (table of arXiv:2503.14738, as CFG681) with the sound horizon r_d computed here
  + 15 cosmic chronometers with the Moresco covariance (as CFG684)
  + the compressed CMB summary (100 theta*, omega_b, omega_bc) and BBN prior printed in arXiv:2610.23657 Eq. 18-21.
Parameters: p = (h, Omega_bc, omega_b, w0, wa[, dM_legacy]).  Nothing here is fitted by the framework; no a0 enters.
An independent implementation: the early-universe integrals are done numerically (exact Fermi-Dirac neutrinos),
not with the Hu-Sugiyama closed form used in the paper."""
import os, warnings
import numpy as np
# numpy 1.26 on Apple Accelerate raises spurious "encountered in matmul" warnings on large products; K4 checks the values
warnings.filterwarnings("ignore", message=".*encountered in matmul")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
IN = os.path.normpath(os.path.join(REPO, "..", "_external_data", "cfg684_inputs"))

# ---------------- constants (SI where it matters) ----------------
C_KMS = 299792.458
T_CMB = 2.72548                      # K (Fixsen 2009), as the paper
N_EFF = 3.044
M_NU_EV = (0.050, 0.010, 0.0)        # eV, as the paper
A_RAD = 7.565733e-16                 # J m^-3 K^-4
G_SI = 6.67430e-11
MPC_M = 3.0856775814913673e22
RHO_C100 = 3 * (100e3 / MPC_M) ** 2 / (8 * np.pi * G_SI)          # kg m^-3 for h = 1
OMEGA_G = A_RAD * T_CMB ** 4 / (299792458.0 ** 2) / RHO_C100      # omega_gamma = Omega_gamma h^2
K_B_EV = 8.617333262e-5
T_NU0 = (4.0 / 11.0) ** (1.0 / 3.0) * (N_EFF / 3.0) ** 0.25 * T_CMB
NU_REL = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0) * (N_EFF / 3.0)  # one species, relativistic, in units of rho_gamma
Y0 = np.array([m / (K_B_EV * T_NU0) for m in M_NU_EV])             # m c^2 / (k T_nu0)

# Fermi-Dirac energy density ratio F(y) = rho(m) / rho(m = 0), y = m a / (k T_nu0)
_x = np.linspace(1e-6, 60.0, 20001)
_w = np.gradient(_x)
_ly = np.linspace(-5, 6, 1101)
_F = np.array([np.sum(_w * _x ** 2 * np.sqrt(_x ** 2 + (10 ** l) ** 2) / (np.exp(_x) + 1)) for l in _ly])
_F /= np.sum(_w * _x ** 3 / (np.exp(_x) + 1))
def nu_factor(a):
    """sum over the three species of F(y_i a): 3 when all are relativistic."""
    a = np.atleast_1d(a); tot = np.zeros_like(a, dtype=float)
    for y0 in Y0:
        if y0 == 0: tot += 1.0
        else: tot += np.interp(np.log10(np.maximum(y0 * a, 1e-5)), _ly, _F)
    return tot
NU_TODAY = float(nu_factor(1.0)[0])
OMEGA_NU = OMEGA_G * NU_REL * NU_TODAY           # omega_nu today (massive + massless), about 6.5e-4

# decoupling and drag temperatures: quadratic fits of arXiv:2610.23657 Eq. 20-21 (to CLASS, 0.8 mK)
_D0 = np.array([0.0225, 0.1450])
_TS, _GS, _HS = 2970.29, np.array([-3188.92, 194.09]), np.array([[265960.27, -7860.93], [-7860.93, -488.36]])
_TD, _GD, _HD = 2892.74, np.array([5925.64, 203.34]), np.array([[-189076.80, -4767.87], [-4767.87, -626.49]])
def t_star_drag(wb, wbc):
    d = np.array([wb, wbc]) - _D0
    return _TS + d @ _GS + 0.5 * d @ _HS @ d, _TD + d @ _GD + 0.5 * d @ _HD @ d

# compressed CMB (SPT-3G + ACT DR6 + Planck) and BBN, arXiv:2610.23657 Eq. 18 and Section 3.3.2
MU_CMB = np.array([1.04161, 0.02240, 0.14265])
C_CMB = 1e-9 * np.array([[53.8482, 1.10723, -28.7005], [1.10723, 9.20447, -17.6016], [-28.7005, -17.6016, 843.132]])
CI_CMB = np.linalg.inv(C_CMB)
BBN = (0.021915, 0.000215)

# ---------------- background ----------------
def e2h2(a, h, obc, wb, w0, wa):
    """(H / 100 km/s/Mpc)^2 at scale factor a, flat."""
    wbc = obc * h * h
    wde = h * h - wbc - OMEGA_G * (1 + NU_REL * NU_TODAY)
    f = a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a))
    return wbc * a ** -3 + OMEGA_G * a ** -4 * (1 + NU_REL * nu_factor(a)) + wde * f

_GLx, _GLw = np.polynomial.legendre.leggauss(400)
def sound_horizon(a_end, h, obc, wb, w0, wa):
    """comoving sound horizon [Mpc] from a = 0 to a_end."""
    a = 0.5 * a_end * (_GLx + 1); w = 0.5 * a_end * _GLw
    R = 0.75 * wb / OMEGA_G * a
    H = 100 * np.sqrt(e2h2(a, h, obc, wb, w0, wa))
    return float(np.sum(w * C_KMS / np.sqrt(3 * (1 + R)) / (a * a * H)))

_XG = np.linspace(0, np.log(1 + 1300.0), 12001)       # x = ln(1 + z)
_ZG = np.expm1(_XG); _AG = np.exp(-_XG)
def dc_grid(h, obc, wb, w0, wa):
    """comoving distance [Mpc] on the grid _ZG, and H there."""
    H = 100 * np.sqrt(e2h2(_AG, h, obc, wb, w0, wa))
    f = C_KMS * (1 + _ZG) / H
    D = np.r_[0, np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(_XG))]
    return D, H

# ---------------- data ----------------
# DESI DR2 (arXiv:2503.14738 table, copied from CFG681): z, D_M/r_d, sig, D_H/r_d, sig, r
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)
_BAO_CI = [np.linalg.inv(np.array([[sm * sm, r * sm * sh], [r * sm * sh, sh * sh]])) for (_, _, _, sm, _, sh, r) in ANISO]

# cosmic chronometers (as CFG684: Moresco BC03 table, cov = diag + IMF + SPS-ooo)
cz, cH, ceH = np.genfromtxt(os.path.join(IN, "cc", "HzTable_MM_BC03.dat"), comments="#", usecols=(0, 1, 2), unpack=True, delimiter=",")
_zm, _imf, _slib, _sps, _spsooo = np.genfromtxt(os.path.join(IN, "cc", "data_MM20.dat"), comments="#", usecols=(0, 1, 2, 3, 4), unpack=True)
_fi, _fo = np.interp(cz, _zm, _imf) / 100, np.interp(cz, _zm, _spsooo) / 100
CI_CC = np.linalg.inv(np.diag(ceH ** 2) + np.outer(cH * _fi, cH * _fi) + np.outer(cH * _fo, cH * _fo))

SEED_RAND = 20261113        # the LGS1 draw


class SN:
    """Dovekie Hubble diagram with a selection. sample: full | des_only | rand197."""
    def __init__(self, sample):
        rows = [l.split() for l in open(os.path.join(IN, "des5", "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
        ids = np.array([int(r[2]) for r in rows]); z = np.array([float(r[3]) for r in rows])
        zh = np.array([float(r[4]) for r in rows]); mu = np.array([float(r[5]) for r in rows])
        npz = np.load(os.path.join(IN, "des5", "STAT+SYS.npz")); n = int(npz[npz.files[0]][0])
        W = np.zeros((n, n)); W[np.triu_indices(n)] = npz[npz.files[1]]; W = W + np.triu(W, 1).T
        sel = z > 0
        if sample == "des_only":
            sel &= ids == 10
        elif sample == "rand197":
            des = np.where(ids == 10)[0]
            drop = np.random.default_rng(SEED_RAND).choice(des, int((ids != 10).sum()), replace=False)
            sel[drop] = False
        elif sample != "full":
            raise ValueError(sample)
        C = np.linalg.inv(W)[np.ix_(sel, sel)]; self.W = np.linalg.inv(C)
        self.z, self.zh, self.mu, self.ids = z[sel], zh[sel], mu[sel], ids[sel]
        self.n = int(sel.sum()); self.n_des = int((self.ids == 10).sum()); self.n_leg = self.n - self.n_des
        self.one = np.ones(self.n); self.leg = (self.ids != 10).astype(float)
        self.W1 = self.W @ self.one; self.s11 = float(self.one @ self.W1)
        self.WL = self.W @ self.leg; self.sLL = float(self.leg @ self.WL); self.s1L = float(self.one @ self.WL)
        self.x = np.log1p(self.z)

    def chi2(self, D, dm_leg=0.0, profile_offset=False):
        """D = comoving distance on _XG. Returns chi2 with M profiled (and the legacy offset profiled if asked)."""
        r = self.mu - 5 * np.log10((1 + self.zh) * np.interp(self.x, _XG, D)) - dm_leg * self.leg
        Wr = self.W @ r; rr = float(r @ Wr); b1 = float(self.one @ Wr)
        if not profile_offset:
            return rr - b1 * b1 / self.s11
        bL = float(self.leg @ Wr); A = np.array([[self.s11, self.s1L], [self.s1L, self.sLL]]); b = np.array([b1, bL])
        sol = np.linalg.solve(A, b)
        return rr - float(b @ sol), float(sol[1])


def early(h, obc, wb, w0, wa):
    wbc = obc * h * h
    ts, td = t_star_drag(wb, wbc)
    a_s, a_d = T_CMB / ts, T_CMB / td
    return sound_horizon(a_s, h, obc, wb, w0, wa), sound_horizon(a_d, h, obc, wb, w0, wa), 1 / a_s - 1, 1 / a_d - 1


def parts(p, sn=None, use=("sn", "bao", "cc", "cmb", "bbn"), profile_offset=False):
    """chi2 by probe. p = (h, Omega_bc, omega_b, w0, wa[, dM_legacy])."""
    h, obc, wb, w0, wa = p[:5]; dm = p[5] if len(p) > 5 else 0.0
    out = {}
    e2 = e2h2(np.array([1.0, 1e-3]), h, obc, wb, w0, wa)
    if not np.all(np.isfinite(e2)) or np.any(e2 <= 0):
        return None
    D, H = dc_grid(h, obc, wb, w0, wa)
    if not np.all(np.isfinite(D)):
        return None
    rs, rd, zs, zd = early(h, obc, wb, w0, wa)
    if "sn" in use:
        if profile_offset:
            out["sn"], out["dm_hat"] = sn.chi2(D, 0.0, True)
        else:
            out["sn"] = sn.chi2(D, dm)
    if "bao" in use:
        c = 0.0
        for (nm, z, dmv, sm, dhv, sh, r), Ci in zip(ANISO, _BAO_CI):
            x = np.log1p(z); d = np.array([np.interp(x, _XG, D) / rd - dmv, C_KMS / np.interp(x, _XG, H) / rd - dhv])
            c += float(d @ Ci @ d)
        z, dv, sdv = BGS; x = np.log1p(z)
        DV = (z * np.interp(x, _XG, D) ** 2 * C_KMS / np.interp(x, _XG, H)) ** (1 / 3)
        out["bao"] = c + ((DV / rd - dv) / sdv) ** 2
    if "cc" in use:
        r = cH - np.interp(np.log1p(cz), _XG, H); out["cc"] = float(r @ CI_CC @ r)
    if "cmb" in use:
        th = 100 * rs / np.interp(np.log1p(zs), _XG, D)
        d = np.array([th, wb, obc * h * h]) - MU_CMB; out["cmb"] = float(d @ CI_CMB @ d); out["theta100"] = float(th)
    if "bbn" in use:
        out["bbn"] = ((wb - BBN[0]) / BBN[1]) ** 2
    out["rd"], out["rs"], out["zs"], out["zd"] = rd, rs, zs, zd
    out["om"] = obc + OMEGA_NU / (h * h)
    return out


PROBES = ("sn", "bao", "cc", "cmb", "bbn")
# priors of arXiv:2610.23657 Table 1 (model comparison block); dM_legacy U(-1, 1)
PRIOR = dict(h=(0.40, 1.00), obc=(0.05, 0.70), wb=(0.020, 0.025), w0=(-2.0, 0.0), wa=(-3.0, 2.0), dm=(-1.0, 1.0))
def in_prior(p, lcdm=False):
    h, obc, wb, w0, wa = p[:5]
    ok = PRIOR["h"][0] < h < PRIOR["h"][1] and PRIOR["obc"][0] < obc < PRIOR["obc"][1] and PRIOR["wb"][0] < wb < PRIOR["wb"][1]
    if not lcdm:
        ok = ok and PRIOR["w0"][0] < w0 < PRIOR["w0"][1] and PRIOR["wa"][0] < wa < PRIOR["wa"][1]
    if len(p) > 5:
        ok = ok and PRIOR["dm"][0] < p[5] < PRIOR["dm"][1]
    return ok


def chi2_total(p, sn=None, use=PROBES, profile_offset=False):
    o = parts(p, sn, use, profile_offset)
    if o is None:
        return 1e30
    return float(sum(o[k] for k in use))
