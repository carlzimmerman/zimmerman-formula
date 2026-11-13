"""EXR1R library: written blind from EXR1's, ESZ1's and EUC1's frozen texts (no EXR1/ESZ1/EUC1 code read).

Lens model (EUC1 text), G2 gas (ESZ1 text), APEC reader, MM83 absorption, eROSITA TM0 folding, KBN limits.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import csv
import json
import os
import re
import numpy as np
from scipy import special, integrate, optimize

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXT = os.path.join(ROOT, '_external_data')

# constants (SI unless stated)
G = 6.6743e-11
C = 2.99792458e8
MSUN = 1.98841e30
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
MP = 1.67262192369e-27
KEV = 1.602176634e-16
ERG = 1e-7
ARCSEC = np.pi / 180 / 3600
A0 = {'canonical': 9.3603e-11, 'alt': 1.132e-10}
MU, MU_E = 0.59, 1.14
XH = 2.0 / MU_E - 1.0
MU_I = 1.0 / (1.0 / MU - 1.0 / MU_E)
RT_KPC = 300.0          # G2 cut
RMAX_KPC = 1e6          # projection limit (EUC1 section 3)
ECF = 1.074e12          # catalogue ECF 0.2-2.3 keV, cm^2/erg
FCLIP = 1e-12
SEED = 20261112


# ---------------------------------------------------------------- cosmology
class Cosmo:
    def __init__(self, H0, Om):
        self.H0, self.Om = H0, Om
        self.DH = C / (H0 * 1e3 / MPC)  # m
        zg = np.concatenate([np.linspace(0, 5, 5001)[:-1], np.geomspace(5, 1200, 3000)])
        f = lambda z: 1.0 / np.sqrt(Om * (1 + z) ** 3 + 1 - Om)
        dc = np.zeros_like(zg)
        for i in range(1, len(zg)):
            dc[i] = dc[i - 1] + integrate.quad(f, zg[i - 1], zg[i], epsabs=0, epsrel=1e-12)[0]
        self._zg, self._dc = zg, dc * self.DH

    def DC(self, z):
        return np.interp(z, self._zg, self._dc)

    def DA(self, z):
        return self.DC(z) / (1 + np.asarray(z))

    def DL(self, z):
        return self.DC(z) * (1 + np.asarray(z))

    def DA12(self, z1, z2):
        return (self.DC(z2) - self.DC(z1)) / (1 + np.asarray(z2))

    def sigma_cr(self, zl, zs):
        Dl, Ds, Dls = self.DA(zl), self.DA(zs), self.DA12(zl, zs)
        return C ** 2 * Ds / (4 * np.pi * G * Dl * Dls)  # kg/m^2


EUCLID = Cosmo(67.74, 0.3089)
LCDM70 = Cosmo(70.0, 0.3)


# ---------------------------------------------------------------- ECLIPSE sample
def _b(s):
    return str(s).strip().lower() in ('true', '1', 't', 'yes')


def _f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return np.nan


def load_sample():
    """Sample S (EUC1 section 2, grades A and B) with finite ra/dec."""
    base = os.path.join(EXT, 'euclid_dr1_eclipse')
    obj = {}
    with open(os.path.join(base, 'ECLIPSE_object_catalogue.csv')) as fh:
        for r in csv.DictReader(fh):
            obj[r['Unique_Identifier']] = r
    rows, cnt = [], {'grade_AB': 0, 'model_final_lsw': 0, 'cuts': 0, 'radec': 0}
    with open(os.path.join(base, 'eclipse_dr1_catalogue_key_v20261103.csv')) as fh:
        for r in csv.DictReader(fh):
            if r['lens_grade'] not in ('A', 'B'):
                continue
            cnt['grade_AB'] += 1
            o = obj.get(r['unique_identifier'])
            if o is None or not (_b(r['lens_model_success']) and _b(r['final_sample'])
                                 and not _b(o['large_system_warning'])):
                continue
            cnt['model_final_lsw'] += 1
            te, re_, n = _f(r['eclipse_effective_einstein_radius']), _f(r['eclipse_effective_radius']), \
                _f(r['eclipse_sersic_index'])
            z, lm = _f(r['eclipse_median_phz']), _f(r['eclipse_log_survived_mass_med'])
            if not (te > 0 and re_ > 0 and 0.6 <= n <= 10 and z > 0 and lm > 0):
                continue
            cnt['cuts'] += 1
            ra, dec = _f(r['ra']), _f(r['dec'])
            if not (np.isfinite(ra) and np.isfinite(dec)):
                continue
            cnt['radec'] += 1
            rows.append(dict(id=r['unique_identifier'], grade=r['lens_grade'], ra=ra, dec=dec, z=z, logm=lm,
                             thE=te, thR=re_, n=n))
    rows.sort(key=lambda d: d['id'])
    return rows, cnt


# ---------------------------------------------------------------- lens model (EUC1 section 3, from text)
def bn_exact(n):
    return optimize.brentq(lambda b: special.gammainc(2 * n, b) - 0.5, 1e-6, 50 * n + 10, xtol=1e-14)


def p_ps(n):
    return 1.0 - 0.6097 / n + 0.05463 / n ** 2


class Lens:
    """One lens: stars (Prugniel-Simien), G2 gas, law S. Lengths in m internally."""

    def __init__(self, d, bstar=0.10, zs=1100.0, cosmo=EUCLID):
        self.d = d
        self.z = d['z']
        self.DA = float(cosmo.DA(self.z))
        self.DL = float(cosmo.DL(self.z))
        self.RE = d['thE'] * ARCSEC * self.DA
        self.Re = d['thR'] * ARCSEC * self.DA
        self.n = d['n']
        self.Ms = 10 ** (d['logm'] + bstar) * MSUN
        self.bn = bn_exact(self.n)
        self.pn = p_ps(self.n)
        self.zs = zs
        self.Mmin = np.pi * self.RE ** 2 * float(cosmo.sigma_cr(self.z, zs))
        self.rt = RT_KPC * KPC
        self._nodes()

    def mstar(self, r):
        x = self.bn * (np.asarray(r) / self.Re) ** (1.0 / self.n)
        return self.Ms * special.gammainc((3 - self.pn) * self.n, x)

    def mgas(self, r, A):
        return 4 * np.pi * A * np.minimum(r, self.rt)

    @staticmethod
    def law(gN, a0):
        gN = np.maximum(gN, 1e-300)
        return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / gN))

    def g(self, r, A, a0):
        return self.law(G * (self.mstar(r) + self.mgas(r, A)) / r ** 2, a0)

    def _nodes(self, nper=160):
        R = self.RE
        U = np.arccosh(RMAX_KPC * KPC / R)
        cuts = [0.0]
        for rc in (3 * R, 30 * R, self.rt):
            if rc > R:
                cuts.append(np.arccosh(rc / R))
        cuts = sorted(set([c for c in cuts if c < U])) + [U]
        x, w = np.polynomial.legendre.leggauss(nper)
        us, ws = [], []
        for a, b in zip(cuts[:-1], cuts[1:]):
            us.append(0.5 * (b - a) * x + 0.5 * (b + a))
            ws.append(0.5 * (b - a) * w)
        u, wt = np.concatenate(us), np.concatenate(ws)
        self._r = R * np.cosh(u)
        self._w = wt
        self._ms = self.mstar(self._r)

    def m2d(self, A, a0):
        r = self._r
        gN = G * (self._ms + self.mgas(r, A)) / r ** 2
        return self.RE ** 2 / G * np.sum(self._w * self.law(gN, a0))

    def solve_A(self, a0):
        if self.m2d(0.0, a0) >= self.Mmin:
            return 0.0
        # gas scale: A such that 4 pi A RE ~ Mmin
        lo, hi = 0.0, self.Mmin / (4 * np.pi * self.RE)
        while self.m2d(hi, a0) < self.Mmin:
            hi *= 2
        return optimize.brentq(lambda A: self.m2d(A, a0) - self.Mmin, lo, hi, xtol=1e-14 * hi, rtol=1e-12, maxiter=300)

    def kT_profile(self, A, a0, rmin_kpc=0.01, npts=4000):
        """kT(r) [keV] on a log grid: kT = mu m_p r^2 int_r^rt g/r'^2 dr' (zero pressure at rt)."""
        r = np.geomspace(rmin_kpc * KPC, self.rt, npts)
        f = self.g(r, A, a0) / r  # integrand per d ln r of g/r'^2 * r'
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(np.log(r)))])
        tail = cum[-1] - cum      # int_r^rt
        kT = MU * MP * r ** 2 * tail / KEV
        return r, kT

    def mgas_total(self, A):
        return 4 * np.pi * A * self.rt


# ---------------------------------------------------------------- APEC tables
APEC_DIR = os.path.join(EXT, 'exr1_erass1', 'atomdb', 'atomdb_v3.1.3')
EDGES = np.geomspace(1e-3, 60.0, 40001)      # fine rest-frame grid, keV
ECEN = np.sqrt(EDGES[1:] * EDGES[:-1])


def _cumint_pl(x, y, e):
    """Exact integral of the piecewise-linear (x, y) from x[0] to each e (zero outside)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    seg = np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])
    e = np.clip(e, x[0], x[-1])
    k = np.clip(np.searchsorted(x, e, side='right') - 1, 0, len(x) - 2)
    dx = e - x[k]
    slope = (y[k + 1] - y[k]) / np.where(x[k + 1] > x[k], x[k + 1] - x[k], 1.0)
    return seg[k] + y[k] * dx + 0.5 * slope * dx ** 2


def build_apec_table(cache):
    """Photons cm^3 s^-1 per fine bin, for H+He and for Z>=3, at each tabulated kT."""
    if os.path.exists(cache):
        z = np.load(cache)
        return z['kT'], z['hhe'], z['met']
    from astropy.io import fits
    L = fits.open(os.path.join(APEC_DIR, 'apec_v3.1.3_line.fits'), memmap=True)
    Co = fits.open(os.path.join(APEC_DIR, 'apec_v3.1.3_coco.fits'), memmap=True)
    kT = np.array(L[1].data['kT'], float)
    nT = len(kT)
    hhe = np.zeros((nT, len(ECEN)))
    met = np.zeros((nT, len(ECEN)))
    for i in range(nT):
        ld = L[i + 2].data
        lam = np.array(ld['Lambda'], float)
        eps = np.array(ld['Epsilon'], float)
        el = np.array(ld['Element'], int)
        E = 12.398419843320026 / lam
        idx = np.searchsorted(EDGES, E) - 1
        ok = (idx >= 0) & (idx < len(ECEN)) & np.isfinite(eps)
        for tab, sel in ((hhe, el <= 2), (met, el >= 3)):
            m = ok & sel
            tab[i] += np.bincount(idx[m], weights=eps[m], minlength=len(ECEN))
        cd = Co[i + 2].data
        for row in cd:
            Z = int(row['Z'])
            if int(row['rmJ']) != 0:
                continue
            tab = hhe if Z <= 2 else met
            for en, vn, nn in (('E_Cont', 'Continuum', 'N_Cont'), ('E_Pseudo', 'Pseudo', 'N_Pseudo')):
                nk = int(row[nn])
                if nk < 2:
                    continue
                x = np.array(row[en][:nk], float)
                y = np.array(row[vn][:nk], float)
                ci = _cumint_pl(x, y, EDGES)
                tab[i] += np.diff(ci)
    np.savez(cache, kT=kT, hhe=hhe, met=met)
    return kT, hhe, met


class Apec:
    def __init__(self, cache):
        self.kT, self.hhe, self.met = build_apec_table(cache)
        self.lkT = np.log(self.kT)

    def weights(self, kT):
        """Linear-in-log-kT interpolation weights onto the table: returns (idx_lo, w_lo, w_hi)."""
        lk = np.log(np.clip(kT, self.kT[0], self.kT[-1]))
        j = np.clip(np.searchsorted(self.lkT, lk) - 1, 0, len(self.kT) - 2)
        t = (lk - self.lkT[j]) / (self.lkT[j + 1] - self.lkT[j])
        return j, 1 - t, t

    def node_weights(self, kT, em):
        """Distribute emission measures em (at temperatures kT) onto table nodes."""
        j, wl, wh = self.weights(np.atleast_1d(kT))
        W = np.zeros(len(self.kT))
        np.add.at(W, j, wl * em)
        np.add.at(W, j + 1, wh * em)
        return W

    def spectrum(self, W, Z):
        """Photon spectrum per fine bin for node weights W and metallicity Z (x AG89)."""
        return W @ self.hhe + Z * (W @ self.met)

    def band_energy(self, W, Z, e1, e2):
        """Rest-frame energy emissivity (erg cm^3/s per unit W) in [e1, e2] keV."""
        s = self.spectrum(W, Z)
        return _band_sum(s * ECEN * KEV / ERG, e1, e2)


def _band_sum(v, e1, e2, edges=EDGES):
    """Sum of per-bin quantity v over [e1, e2], fractional bins at the ends (by log-width)."""
    lo, hi = edges[:-1], edges[1:]
    frac = np.clip((np.minimum(hi, e2) - np.maximum(lo, e1)) / (hi - lo), 0, 1)
    return np.sum(v * frac, axis=-1)


# ---------------------------------------------------------------- absorption (Morrison & McCammon 1983, Table 2)
MM_EMAX = np.array([0.100, 0.284, 0.400, 0.532, 0.707, 0.867, 1.303, 1.840, 2.471, 3.210, 4.038, 7.111, 8.331,
                    10.000])
MM_C0 = np.array([17.3, 34.6, 78.1, 71.4, 95.5, 308.9, 120.6, 141.3, 202.7, 342.7, 352.2, 433.9, 629.0, 701.2])
MM_C1 = np.array([608.1, 267.9, 18.8, 66.8, 145.8, -380.6, 169.3, 146.8, 104.7, 18.7, 18.7, -2.4, 30.9, 25.2])
MM_C2 = np.array([-2150., -476.1, 4.3, -51.4, -61.1, 294.0, -47.7, -31.5, -17.0, 0.0, 0.0, 0.75, 0.0, 0.0])


def sigma_mm(E):
    E = np.asarray(E, float)
    k = np.clip(np.searchsorted(MM_EMAX, E), 0, len(MM_EMAX) - 1)
    return (MM_C0[k] + MM_C1[k] * E + MM_C2[k] * E ** 2) / E ** 3 * 1e-24


# ---------------------------------------------------------------- instrument (TM0 ARF/RMF)
SRC = os.path.join(EXT, 'exr1_erass1', 'srcprod_180135_00004', 'x')


class Instrument:
    def __init__(self):
        from astropy.io import fits
        a = fits.open(os.path.join(SRC, 'em01_180135_020_ARF_00004_c010.fits'))[1].data
        r = fits.open(os.path.join(SRC, 'em01_180135_020_RMF_00004_c010.fits'))
        m, eb = r['MATRIX'].data, r['EBOUNDS'].data
        self.elo = np.array(a['ENERG_LO'], float)
        self.ehi = np.array(a['ENERG_HI'], float)
        assert np.allclose(self.elo, m['ENERG_LO']) and np.allclose(self.ehi, m['ENERG_HI'])
        self.arf = np.array(a['SPECRESP'], float)
        nch = len(eb)
        R = np.zeros((len(self.elo), nch))
        for i in range(len(m)):
            ng = int(m['N_GRP'][i])
            fc, nc, mat = np.atleast_1d(m['F_CHAN'][i]), np.atleast_1d(m['N_CHAN'][i]), np.array(m['MATRIX'][i])
            p = 0
            for g_ in range(ng):
                c0, n_ = int(fc[g_]) - 1, int(nc[g_])
                R[i, c0:c0 + n_] = mat[p:p + n_]
                p += n_
        self.rmf = R
        self.chlo, self.chhi = np.array(eb['E_MIN'], float), np.array(eb['E_MAX'], float)
        self.chmid = 0.5 * (self.chlo + self.chhi)
        self.edges = np.concatenate([self.elo, [self.ehi[-1]]])

    def eff(self, b1=0.2, b2=2.3):
        """Counts in channels with midpoint in [b1, b2] per photon in each ARF bin (cm^2)."""
        sel = (self.chmid >= b1) & (self.chmid <= b2)
        return self.arf * self.rmf[:, sel].sum(axis=1)

    def eff_fine(self, Eobs, b1=0.2, b2=2.3):
        e = self.eff(b1, b2)
        k = np.searchsorted(self.edges, Eobs, side='right') - 1
        ok = (k >= 0) & (k < len(e))
        out = np.zeros_like(Eobs)
        out[ok] = e[k[ok]]
        return out


def powerlaw_ref(inst, NH=3e20, gamma=2.0, b1=0.2, b2=2.3, fb1=None, fb2=None):
    """Count rate (band channels) and absorbed energy flux (band) of a photon index gamma power law (norm 1)."""
    fb1 = b1 if fb1 is None else fb1
    fb2 = b2 if fb2 is None else fb2
    E = ECEN
    ph = E ** (-gamma) * np.diff(EDGES) * np.exp(-sigma_mm(E) * NH)
    cr = np.sum(ph * inst.eff_fine(E, b1, b2))
    fl = _band_sum(ph * E * KEV / ERG, fb1, fb2)
    return cr, fl


# ---------------------------------------------------------------- KBN upper limit
def kbn_ul(N, B, CL=0.9987):
    N = np.asarray(N, float)
    B = np.asarray(B, float)
    q = special.gammaincc(N + 1, B)
    return special.gammainccinv(N + 1, (1 - CL) * q) - B


# ---------------------------------------------------------------- sky geometry
def offset_pos(ra, dec, pa_deg, rho_deg):
    ra, dec, pa, rho = map(np.radians, (ra, dec, pa_deg, rho_deg))
    d2 = np.arcsin(np.sin(dec) * np.cos(rho) + np.cos(dec) * np.sin(rho) * np.cos(pa))
    ra2 = ra + np.arctan2(np.sin(pa) * np.sin(rho) * np.cos(dec), np.cos(rho) - np.sin(dec) * np.sin(d2))
    return np.degrees(ra2) % 360, np.degrees(d2)


def unitvec(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.stack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)], axis=-1)


def sep_arcsec(ra1, dec1, ra2, dec2):
    u, v = unitvec(ra1, dec1), unitvec(ra2, dec2)
    return np.degrees(2 * np.arcsin(np.clip(np.linalg.norm(u - v, axis=-1) / 2, 0, 1))) * 3600
