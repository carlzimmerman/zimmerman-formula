"""CFG520 shared pieces (FROZEN_CRITERIA.md section 2; criteria commit 6d184c37d).

CFG506's joint abundance match and satellite occupation (cfg506_box.py section 3, copied), with the occupation constant 17 replaced by B
and an optional exponent alpha (the declared fallback form): N_sat(> m | M) = [max(M - M_min(m), 0) / (B M_min(m))]^alpha.
B = 17, alpha = 1 is CFG506 exactly.
"""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr

L = 200.0
V = L ** 3


def smf_phi(lm):                                   # Baldry+12 (U), per dex, Mpc^-3 (h = 0.7)   (CFG506, copied)
    Ms = 10 ** 10.66; x = 10 ** lm / Ms
    return math.log(10) * np.exp(-x) * (3.96e-3 * x ** (-0.35 + 1) + 0.79e-3 * x ** (-1.47 + 1))


LMG = np.linspace(7.0, 12.8, 5801)
_cum = np.concatenate([[0.0], np.cumsum(0.5 * (smf_phi(LMG[1:]) + smf_phi(LMG[:-1])) * np.diff(LMG))])
NCUM = (_cum[-1] - _cum) / 0.7 ** 3               # n(> m) in (Mpc/h)^-3


def n_smf(m): return np.interp(m, LMG, NCUM)


MGRID = np.arange(12.2, 8.59, -0.02)
MF = 8.6
MS_FINE = np.arange(MF, 12.5, 0.01)


def nsat_of(M, Mm, B, alpha):
    """N_sat(> m | M) for host mass(es) M and threshold halo mass Mm = M_min(m)."""
    x = np.maximum(M - Mm, 0) / (B * Mm)
    return x if alpha == 1.0 else x ** alpha


class Sham:
    """CFG506's abundance match on one box's catalogue (Mta), generalised to (B, alpha)."""

    def __init__(self, Mta, MP, B=17.0, alpha=1.0):
        self.B, self.alpha = float(B), float(alpha)
        self.Mta = Mta
        MCOMP = 150 * MP; self.MCOMP = MCOMP
        Mcomp_sorted = np.sort(Mta[Mta >= MCOMP])[::-1]
        MFIT = np.geomspace(MCOMP, 10 * MCOMP, 11)
        NFIT = np.array([np.searchsorted(-Mcomp_sorted, -x) for x in MFIT], float)
        okf = NFIT > 10
        SLOPE_HMF = -np.polyfit(np.log10(MFIT[okf]), np.log10(NFIT[okf]), 1)[0]
        NC_ = np.searchsorted(-Mcomp_sorted, -MCOMP) / V
        LMX = np.linspace(7.5, math.log10(MCOMP), 400); MX = 10 ** LMX
        DNDM = SLOPE_HMF * NC_ * (MX / MCOMP) ** (-SLOPE_HMF) / MX
        B, alpha = self.B, self.alpha

        def f_root(lMmin, m):
            Mm = 10 ** lMmin
            if Mm >= MCOMP:
                ncen = np.searchsorted(-Mcomp_sorted, -Mm) / V
            else:
                ncen = NC_ * (Mm / MCOMP) ** (-SLOPE_HMF)
            sel = Mcomp_sorted[Mcomp_sorted > Mm]
            if alpha == 1.0:
                nsat = (sel - Mm).sum() / (B * Mm) / V            # CFG506's expression verbatim at B = 17
            else:
                nsat = nsat_of(sel, Mm, B, alpha).sum() / V
            if Mm < MCOMP:
                u = MX > Mm
                nsat += np.trapz((nsat_of(MX, Mm, B, alpha) * DNDM)[u], MX[u])
            return ncen + nsat - n_smf(m)

        lMmin = np.full(len(MGRID), np.nan)
        for k, mm_ in enumerate(MGRID):
            lo, hi = 7.6, 15.8
            if f_root(lo, mm_) < 0 or f_root(hi, mm_) > 0:
                continue
            lMmin[k] = brentq(lambda x: f_root(x, mm_), lo, hi, xtol=1e-5)
        okm_ = np.isfinite(lMmin)
        valid = okm_ & (lMmin >= math.log10(MCOMP))
        if not valid.any():
            raise RuntimeError("abundance matching failed")
        self.mlim_box = float(MGRID[valid].min())
        self.vm, self.vM = MGRID[okm_][::-1], lMmin[okm_][::-1]
        self.MGRID_ok, self.lMmin_ok = MGRID[okm_], lMmin[okm_]
        self.slope = float(SLOPE_HMF)

    def ms_of_lM(self, x): return np.interp(np.asarray(x, float), self.vM, self.vm)

    def lMmin_of_m(self, m): return np.interp(np.asarray(m, float), self.vm, self.vM)

    def cum_sat(self, M):
        """N_sat(> m | M) on MS_FINE for one host (CFG506's 'cum')."""
        return nsat_of(M, 10 ** self.lMmin_of_m(MS_FINE), self.B, self.alpha)

    def parent_fraction_expect(self, edges, scatter=0.15):
        """expected satellite fraction of all box galaxies in [lo, hi) bins (catalogue halos only, as the drawn catalogue)."""
        lM = np.log10(self.Mta); mu = self.ms_of_lM(lM)
        out = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            ncen = float((ndtr((hi - mu) / scatter) - ndtr((lo - mu) / scatter)).sum())
            Mlo, Mhi = 10 ** self.lMmin_of_m(lo), 10 ** self.lMmin_of_m(hi)
            ns = float((nsat_of(self.Mta, Mlo, self.B, self.alpha) - nsat_of(self.Mta, Mhi, self.B, self.alpha)).sum())
            out.append(ns / (ns + ncen))
        return np.array(out)


def draw_galaxies(sham, cen, Mta, rta, r200m, pos, tree, seed=506):
    """CFG506's draw (cfg506_box.py lines 366-395, copied; occupation from sham). Returns GPOS, GLMS, GSAT, GHALO, rng (state after)."""
    rng = np.random.default_rng(seed)
    lM = np.log10(Mta)
    lms_c = sham.ms_of_lM(lM) + rng.normal(0, 0.15, len(lM))
    Mmin_f = 10 ** sham.lMmin_of_m(MS_FINE)
    sat_pos, sat_lms, sat_host = [], [], []
    nsat_exp = nsat_of(Mta, Mmin_f[0], sham.B, sham.alpha)
    nsat = rng.poisson(nsat_exp)
    hosts = np.where(nsat > 0)[0]
    for i in hosts:
        rr = r200m[i] if r200m[i] > 0 else 0.3 * rta[i]
        li = tree.query_ball_point(cen[i], rr) if pos is not None else []
        if len(li) == 0:
            li = [tree.query(cen[i])[1]] if pos is not None else [0]
        cum = nsat_of(Mta[i], Mmin_f, sham.B, sham.alpha)
        u = rng.uniform(0, 1, nsat[i]) * cum[0]
        ms = np.interp(u, cum[::-1], MS_FINE[::-1])
        pick = rng.choice(len(li), nsat[i], replace=True)
        if pos is not None:
            sat_pos.append(pos[np.asarray(li)[pick]])
        sat_lms.append(ms); sat_host.append(np.full(nsat[i], i))
    sat_pos = np.concatenate(sat_pos) if sat_pos else np.zeros((0, 3))
    sat_lms = np.concatenate(sat_lms) if sat_lms else np.zeros(0)
    sat_host = np.concatenate(sat_host) if sat_host else np.zeros(0, int)
    GPOS = np.concatenate([cen, sat_pos]) if pos is not None else None
    GLMS = np.concatenate([lms_c, sat_lms])
    GSAT = np.concatenate([np.zeros(len(cen), bool), np.ones(len(sat_lms), bool)])
    GHALO = np.concatenate([np.arange(len(cen)), sat_host])
    return GPOS, GLMS, GSAT, GHALO, rng, lms_c, sat_lms, sat_host
