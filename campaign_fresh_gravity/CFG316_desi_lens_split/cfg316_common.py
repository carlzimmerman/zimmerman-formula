#!/usr/bin/env python3
"""CFG316 shared helpers: paths, cosmology (the record's h70 / Om 0.3 convention), the June KiDS ESD estimator (agentK_jackknife_stack.py
stage_stack, verbatim per lens), the agentK patch scheme generalised to N = 30, and catalogue readers that read only the named columns.

Data live outside the repository (../_external_data relative to the repository root); intermediate per-lens arrays go to
../_external_data/cfg316_work/ (outside git).  No catalogue is copied.
"""
import os, sys, time, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
EXT = os.path.normpath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg316_work")
os.makedirs(WORK, exist_ok=True)
F_SHEAR = os.path.join(EXT, "kids_lensing_zsplit", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
F_BGS = os.path.join(EXT, "desi_dr1_bgs", "BGS_BRIGHT_full_HPmapcut.dat.fits")
F_CIG = os.path.join(EXT, "desi_dr1_cigale", "IronPhysProp_v1.2.fits")
F_KB = os.path.join(EXT, "kids_lensing_zsplit", "KiDS_DR4_brightsample.fits")
F_KBL = os.path.join(EXT, "kids_lensing_zsplit", "KiDS_DR4_brightsample_LePhare.fits")
LR = os.path.join(REPO, "real_research", "data", "lensing_rar")          # the record's staged KiDS products (read-only)

c = 2.998e8; G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; H0 = 70 * 1e3 / Mpc   # agentK / lr_esd_remeasure constants
KG = 1.989e30 / (3.0857e16) ** 2                                                    # kg/m^2 per Msun/pc^2 (June convention)
CKMS = 299792.458
GBAR_EDGES = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)                      # CFG61 EDGES
K1 = [8, 9, 10, 11, 12, 13, 14]
NPATCH = 30                                                                         # D7
UR_SPLIT = 2.0                                                                      # D3 (b): KiDS LePhare u - r > 2.0
FLUXSCALE_DEX = 0.15                                                                # lr_esd_remeasure v4 (KiDS LePhare masses)
T0 = time.time()


def say(s):
    print(f"[{time.time() - T0:7.1f} s] {s}", flush=True)


def DC(z, n=2048):
    """comoving distance [h70^-1 Mpc], flat LCDM Om = 0.3 (lr_esd_remeasure.py / agentK verbatim, incl. the grid to max(z))."""
    z = np.atleast_1d(np.asarray(z, dtype="f8"))
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c / H0) / Mpc
    return np.interp(z, zz, chi)


_ZT = np.linspace(0, 1.5, 30001)
_CT = DC(_ZT, n=30001)


def chi_of(z):
    """smooth comoving distance table (same cosmology) for selection quantities (not used inside the verbatim estimator)."""
    return np.interp(np.asarray(z, "f8"), _ZT, _CT)


def fcold(lm):
    return 10 ** (-0.69 * lm + 6.63)                                                # Brouwer / CFG61


def assign_patches(ra, dec, npatch=NPATCH):
    """agentK's equal-lens-count RA-quantile stripes (N: dec > -15; S: RA unwrapped), generalised: if one region is empty, all npatch
    stripes go to the other (the KiDS-1000 x DESI DR1 overlap is KiDS-N only)."""
    south = dec < -15.0
    ra_u = np.where(south, (ra + 180.0) % 360.0, ra)
    patch = np.zeros(len(ra), dtype=np.int64); off = 0
    regs = [m for m in (~south, south) if m.sum() > 0]
    nper = [npatch // len(regs)] * len(regs); nper[0] += npatch - sum(nper)
    for m, npr in zip(regs, nper):
        q = np.quantile(ra_u[m], np.linspace(0, 1, npr + 1)); q[0] -= 1e-6; q[-1] += 1e-6
        patch[m] = off + np.clip(np.searchsorted(q, ra_u[m], side='right') - 1, 0, npr - 1)
        off += npr
    return patch


# ------------------------------------------------------------------ shear catalogue (only the named columns, in row chunks)
def read_shear_columns(names, chunk=2_000_000):
    import fitsio
    f = fitsio.FITS(F_SHEAR)
    n = f[1].get_nrows()
    out = {k: [] for k in names}
    for i0 in range(0, n, chunk):
        d = f[1].read(columns=names, rows=np.arange(i0, min(i0 + chunk, n)))
        for k in names:
            out[k].append(np.asarray(d[k]))
    f.close()
    return {k: np.concatenate(v) for k, v in out.items()}


# ------------------------------------------------------------------ the June estimator, per lens (agentK stage_stack verbatim)
class Stacker:
    """holds the source arrays; lens(...) returns the per-bin sums (wgE, W, NN, wgX) of ONE lens exactly as agentK accumulates them.
    wgX (cross shear) is an addition used only by the C4 null; it does not touch the verbatim sums."""

    def __init__(self, raS, decS, e1, e2, w, zB):
        from scipy.spatial import cKDTree
        self.raS, self.decS, self.e1, self.e2, self.w, self.zB = raS, decS, e1, e2, w, zB
        self.tree = cKDTree(np.c_[np.radians(raS), np.radians(decS)])

    def lens(self, rl, dl, zl_, chil_, Mg):
        wg = np.zeros(15); ww_ = np.zeros(15); nn = np.zeros(15); wx = np.zeros(15)
        theta_max = 3.0 * (1 + zl_) / chil_
        ii = self.tree.query_ball_point([np.radians(rl), np.radians(dl)], theta_max)
        ii = np.array(ii, dtype=int)
        if ii.size < 5: return wg, ww_, nn, wx
        back = self.zB[ii] > zl_ + 0.2
        ii = ii[back]
        if ii.size < 5: return wg, ww_, nn, wx
        raS, decS, e1, e2, w, zB = self.raS, self.decS, self.e1, self.e2, self.w, self.zB
        dra = (np.radians(raS[ii]) - np.radians(rl)) * np.cos(np.radians(dl)); dde = np.radians(decS[ii]) - np.radians(dl)
        R = np.hypot(dra, dde) * chil_ / (1 + zl_)
        phi = np.arctan2(dde, dra)
        et = -(e1[ii] * np.cos(2 * phi) - e2[ii] * np.sin(2 * phi))
        ex = (e1[ii] * np.sin(2 * phi) + e2[ii] * np.cos(2 * phi))          # cross component in the same (e2-flipped) frame
        chis = DC(zB[ii]); Dls = (chis - chil_) / (1 + zB[ii]); Dl = chil_ / (1 + zl_); Ds = chis / (1 + zB[ii])
        inv_sc = np.clip(4 * np.pi * G / (c ** 2) * (Dl * Mpc) * (Dls / Ds), 0, None)
        gbar = G * Mg * Msun / (R * Mpc) ** 2
        k = np.digitize(gbar, GBAR_EDGES) - 1
        ok = (k >= 0) & (k < 15) & (inv_sc > 0)
        ww = w[ii] * inv_sc ** 2
        isc = np.where(inv_sc > 0, inv_sc, 1)
        vg = (ww * et / isc)[ok]; vw = ww[ok]; kk = k[ok]; vx = (ww * ex / isc)[ok]
        np.add.at(wg, kk, vg); np.add.at(ww_, kk, vw); np.add.at(nn, kk, 1); np.add.at(wx, kk, vx)
        return wg, ww_, nn, wx


    def pairs(self, rl, dl, zl_, chil_, Mg):
        """the same pair selection and weights as lens(), returning (bin k, w Sigma_crit^-2, Sigma_crit^-1 [SI], g_bar) of the kept pairs;
        used ONLY by the SELFTEST (synthetic shear), never with the real e1/e2."""
        theta_max = 3.0 * (1 + zl_) / chil_
        ii = np.array(self.tree.query_ball_point([np.radians(rl), np.radians(dl)], theta_max), dtype=int)
        e = (np.zeros(0, int), np.zeros(0), np.zeros(0), np.zeros(0))
        if ii.size < 5: return e
        ii = ii[self.zB[ii] > zl_ + 0.2]
        if ii.size < 5: return e
        dra = (np.radians(self.raS[ii]) - np.radians(rl)) * np.cos(np.radians(dl)); dde = np.radians(self.decS[ii]) - np.radians(dl)
        R = np.hypot(dra, dde) * chil_ / (1 + zl_)
        chis = DC(self.zB[ii]); Dls = (chis - chil_) / (1 + self.zB[ii]); Dl = chil_ / (1 + zl_); Ds = chis / (1 + self.zB[ii])
        inv_sc = np.clip(4 * np.pi * G / (c ** 2) * (Dl * Mpc) * (Dls / Ds), 0, None)
        gbar = G * Mg * Msun / (R * Mpc) ** 2
        k = np.digitize(gbar, GBAR_EDGES) - 1
        ok = (k >= 0) & (k < 15) & (inv_sc > 0)
        return k[ok], (self.w[ii] * inv_sc ** 2)[ok], inv_sc[ok], gbar[ok]


_ST = None


def _init_worker(st):
    global _ST
    _ST = st


def _work(args):
    ra, dec, z, chi, Mg = args
    out = np.zeros((len(ra), 4, 15))
    with np.errstate(divide="ignore", invalid="ignore"):
        for i in range(len(ra)):
            out[i] = np.array(_ST.lens(ra[i], dec[i], z[i], chi[i], Mg[i]))
    return out


def stack_perlens(st, ra, dec, z, chi, Mg, nproc=12, chunk=500, label=""):
    """per-lens sums (N, 4, 15): [wgE, W, NN, wgX], computed in a forked pool (each lens independent, so the result does not depend on
    the parallel split)."""
    import multiprocessing as mp
    global _ST
    _ST = st
    jobs = [(ra[i:i + chunk], dec[i:i + chunk], z[i:i + chunk], chi[i:i + chunk], Mg[i:i + chunk]) for i in range(0, len(ra), chunk)]
    ctx = mp.get_context("fork")
    res = []
    with ctx.Pool(nproc) as pool:
        for j, r in enumerate(pool.imap(_work, jobs)):
            res.append(r)
            if j % 20 == 0 or j == len(jobs) - 1:
                say(f"  {label} lenses {min((j + 1) * chunk, len(ra)):,}/{len(ra):,}")
    return np.concatenate(res) if res else np.zeros((0, 4, 15))


# ------------------------------------------------------------------ split statistics on per-lens sums
def class_patch_sums(PL, cls, patch, sel, wts=None, npatch=NPATCH):
    """sums per (patch, class, bin) from per-lens sums PL (N,4,15), for lenses in sel; cls 1 early / 0 late; optional per-lens weights."""
    S = np.zeros((4, npatch, 2, 15))
    idx = np.where(sel)[0]
    wv = np.ones(len(idx)) if wts is None else wts[idx]
    for q in range(4):
        np.add.at(S[q], (patch[idx], cls[idx].astype(int)), PL[idx, q, :] * wv[:, None])
    return S


def esd_loo(S):
    tg, tw = S[0].sum(0), S[1].sum(0)
    esd = tg / np.maximum(tw, 1e-300) / KG
    loo = (tg[None] - S[0]) / np.maximum(tw[None] - S[1], 1e-300) / KG
    return esd, loo


def esdx_loo(S):
    tg, tw = S[3].sum(0), S[1].sum(0)
    return tg / np.maximum(tw, 1e-300) / KG, (tg[None] - S[3]) / np.maximum(tw[None] - S[1], 1e-300) / KG


def jk_cov(reps):
    n = reps.shape[0]
    Rr = reps - reps.mean(0)
    return (n - 1) / n * (Rr.T @ Rr)


def hartlap(n, p):
    return (n - p - 2) / (n - 1)


# ------------------------------------------------------------------ analytic power for D (Stage A; no shear value read)
class PowerModel:
    """sigma^2 of each class's ESD on K1 scales as 1 / sum_lenses M_gal n_src(zB > z + 0.2) <Sigma_crit^-2> / D_A^2 (pairs in a g_bar bin
    sit at R^2 = G M_gal / g, so the annulus holds ∝ M_gal / D_A^2 sources).  The June per-class jackknife covariances on K1
    (lr_esd_jackknife.npz) are scaled by the information ratio and summed (no cross-class term); the noncentrality of a KiDS-size split
    (CFG88's D) against B's calibrated D_B (CFG95's committed D, KiDS lens distribution) follows, with Hartlap (N - 9)/(N - 1), N = 30."""

    def __init__(self, zbh, zbe):
        import json as _json
        self.zbc = 0.5 * (zbe[1:] + zbe[:-1]); self.zbh = zbh
        self.zq = np.linspace(0.1, 0.5, 81); self.Qt = self.Q_of(self.zq)
        LN = np.load(os.path.join(LR, "lr_lenses.npz"))
        self.IK = {cl: self.info(LN["Mgal"][LN["typ"] == cl], LN["z"][LN["typ"] == cl]) for cl in (0, 1)}
        J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
        tg, tw = J["wgE"].sum(0), J["W"].sum(0)
        loo = (tg[None] - J["wgE"]) / (tw[None] - J["W"]) / KG
        esdJ = tg / tw / KG
        self.Cc = {cl: jk_cov(loo[:, cl, K1]) for cl in (0, 1)}
        self.D88 = (esdJ[1] - esdJ[0])[K1]
        self.g95 = _json.load(open(os.path.join(CFG, "CFG95_kids_split_own_calibration_results.json")))["numbers"]["H"]
        self.lamJ = {f: float((self.D88 - np.array(self.g95[f]["D"])) @ np.linalg.solve(self.Cc[0] + self.Cc[1], self.D88 - np.array(self.g95[f]["D"])))
                     * hartlap(50, 7) for f in ("canonical", "alt")}

    def Q_of(self, z):
        out = np.zeros(len(z)); zbc, zbh = self.zbc, self.zbh
        chs = chi_of(zbc)
        for i, z_ in enumerate(z):
            b = zbc > z_ + 0.2
            cl = chi_of(z_); Dl = cl / (1 + z_); Ds = chs[b] / (1 + zbc[b]); Dls = (chs[b] - cl) / (1 + zbc[b])
            out[i] = np.sum(zbh[b] * (Dl * Dls / Ds) ** 2) / Dl ** 2
        return out

    def info(self, Mg_, z_):
        return float(np.sum(Mg_ * np.interp(z_, self.zq, self.Qt)))

    def rows(self, Mg_l, zl, cls, f, P, nm):
        from scipy.stats import ncx2, norm, chi2 as CHI2
        if f.sum() == 0: return None
        IN = {cl: self.info(Mg_l[f & (cls == cl)], zl[f & (cls == cl)]) for cl in (0, 1)}
        if min(IN.values()) <= 0: return None
        Cn = self.Cc[0] * self.IK[0] / IN[0] + self.Cc[1] * self.IK[1] / IN[1]
        sig = np.sqrt(np.diag(Cn))
        out = {}
        for foot in ("canonical", "alt"):
            dlt = self.D88 - np.array(self.g95[foot]["D"])
            lam = float(dlt @ np.linalg.solve(Cn, dlt)) * hartlap(NPATCH, 7)
            for fac in (1.0, 1.58):
                lf = lam / fac ** 2
                pmed = float(CHI2.sf(ncx2.median(7, lf), 7))
                out[f"{foot}_x{fac}"] = dict(lam=lf, z_median=float(norm.isf(pmed / 2)) if pmed > 0 else float("inf"),
                                             p_median=pmed, P_reject_001=float(ncx2.sf(CHI2.isf(0.01, 7), 7, lf)))
        res = dict(N=int(f.sum()), info_ratio_early=IN[1] / self.IK[1], info_ratio_late=IN[0] / self.IK[0], sigma_D_K1=sig.tolist(),
                   sigma_ratio_vs_june=(sig / np.sqrt(np.diag(self.Cc[0] + self.Cc[1]))).tolist(), **out)
        o_ = out
        P(f"  {nm:3s}: N {int(f.sum()):,}; information vs the June 181,477 lenses: early x{IN[1] / self.IK[1]:.3f}, late x{IN[0] / self.IK[0]:.3f}; "
          f"sigma(D) on K1 x{np.median(sig / np.sqrt(np.diag(self.Cc[0] + self.Cc[1]))):.2f} the June value (median)")
        for foot in ("canonical", "alt"):
            P(f"       {foot:9s}: a KiDS-size split (CFG88's D) vs B's calibrated D_B: lambda {o_[foot + '_x1.0']['lam']:.2f} -> median "
              f"{o_[foot + '_x1.0']['z_median']:.2f} sigma, P(reject at p<0.01) {o_[foot + '_x1.0']['P_reject_001']:.2f}; at x1.58: "
              f"lambda {o_[foot + '_x1.58']['lam']:.2f} -> {o_[foot + '_x1.58']['z_median']:.2f} sigma, P {o_[foot + '_x1.58']['P_reject_001']:.2f}")
        return res
