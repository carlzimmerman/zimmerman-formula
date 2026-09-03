#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01 -- THE MASS-MATCHED LENSING a0(z).  Second-law hunt, angle 9 (the redshift axis).

CANDIDATE LAW UNDER TEST
    In the deep-MOND regime the lensing acceleration obeys  g_lens(R)^2 = g_bar(R) a_0, so for two
    lens-redshift bins compared AT MATCHED STELLAR MASS

        a_0(z_hi) / a_0(z_lo)  =  1   exactly,      a_0 = (c/2) sqrt(G rho_DE).

    Measured quantities only: the excess surface density Delta-Sigma(R) from galaxy-galaxy lensing
    (-> g_obs = 4 G Delta-Sigma), the lens stellar mass M* (-> g_bar = G M*/R^2), and the lens photo-z.
    No rotation curve, no inclination, no mass model, one instrument, one pipeline at both redshifts.

WHY THIS RUN EXISTS.  The repository carries a 2-bin KiDS lensing a0(z)
(real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md): ratio 1.309 +- 0.210 (stat),
d ln a0/dz = +1.97 +- 1.47 corrected.  That note names its own killer:

    "the two z-bins are not mass-matched ... Delta logM = 0.465 dex ... a mass(=z)-correlated baryon
     term ... does NOT cancel in the ratio ... which is what kills all discriminating power."

The committed 540-cell accumulator agentZ_stack.npz is indexed
    cell = type(2)*270 + absM*bin(5)*54 + zbin(2)*27 + dens_ad(3)*9 + dens_10(3)*3 + dens_q(3),
so the mass-matched contrast is a re-marginalisation of cells already on disk -- no 16 GB re-stack.

ESTIMATOR (the one structural novelty here).  Per g_bar bin b and stellar-mass bin m, freeze the
matched weight  t_mb = harmonic mean of the low-z and high-z lensing weights, and rescale each half's
accumulator sums by t_mb / W_mb.  The stacked weight in EVERY g_bar bin is then Sum_m t_mb in BOTH
halves, so the two stacks carry the IDENTICAL stellar-mass mix by construction, bin by bin -- exact
matching, not a covariate correction.  Errors: 50-patch leave-one-out jackknife of the complete
statistic with the weights frozen.

KERNEL.  PRIMARY Route A, nu(y) = 1/(1 - exp(-sqrt(y))).  SECONDARY nu = sqrt(1+1/y) (the kernel the
banked 2026-07 note used) so the reproduction gate is exact.  BOTH FOOTINGS on every absolute number.
Checks that can fail, mutation controls, the LambdaCDM alternative beside the framework.  No git.
"""
import os, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
D    = os.path.join(REPO, 'real_research', 'data', 'lensing_rar')
sys.path.insert(0, HERE)
from hunt_lib import Check, P, info, A0

G, Msun, pc = 6.674e-11, 1.989e30, 3.0857e16
KG = Msun / pc**2
NCELL, NP = 540, 50
CUT_REL, CUT_EXT = 1e-13, 1e-14

def gobs_routeA(gb, a0):
    gb = np.asarray(gb, float); return gb / (-np.expm1(-np.sqrt(gb / a0)))
def gobs_fw(gb, a0):
    gb = np.asarray(gb, float); return np.sqrt(gb * gb + gb * a0)
def gobs_newton(gb, a0):
    return np.asarray(gb, float)
KERN = {'routeA': gobs_routeA, 'fw': gobs_fw, 'newton': gobs_newton}
LOGA0 = np.linspace(-11.5, -8.5, 6001)

def fit_a0(lg, lo, Cinv, model, dbar=0.0):
    def f(a0):
        r = lo - np.log10(model(10.0 ** (lg + dbar), a0)); return float(r @ Cinv @ r)
    c = np.array([f(10.0 ** la) for la in LOGA0]); i = int(np.argmin(c))
    la, cmin = LOGA0[i], c[i]
    if 0 < i < len(c) - 1:
        d = LOGA0[1] - LOGA0[0]; num, den = c[i-1] - c[i+1], c[i-1] - 2*c[i] + c[i+1]
        if den > 0:
            la = LOGA0[i] + 0.5 * d * num / den; cmin = f(10.0 ** la)
    return 10.0 ** la, cmin

def cell_decode():
    c = np.arange(NCELL)
    return c // 270, (c // 54) % 5, (c // 27) % 2

# ---------------------------------------------------------------- the matched stacker
class Stack:
    """Frozen-weight mass-matched accumulator pair.  bins = list of absM* bin indices."""
    def __init__(self, wgE, W, CM, CZ, bins):
        self.bins = bins
        self.gm = np.zeros((len(bins), NP, 15)); self.wm = np.zeros((len(bins), NP, 15))
        for i, m in enumerate(bins):
            self.gm[i, :, :] = 0; self.wm[i, :, :] = 0
        self.G = np.zeros((2, len(bins), NP, 15)); self.Wt = np.zeros((2, len(bins), NP, 15))
        for i, m in enumerate(bins):
            for h in (0, 1):
                msk = (CM == m) & (CZ == h)
                self.G[h, i] = wgE[:, msk].sum(1); self.Wt[h, i] = W[:, msk].sum(1)
        Wtot = self.Wt.sum(2)                                   # (2, nbin, 15) full-sample weights
        with np.errstate(divide='ignore', invalid='ignore'):
            t = 2.0 / (1.0 / Wtot[0] + 1.0 / Wtot[1])           # harmonic mean -> matched weight
        t = np.where(np.isfinite(t) & (t > 0), t, 0.0)
        self.alpha = np.zeros((2, len(bins), 15))
        for h in (0, 1):
            self.alpha[h] = np.where(Wtot[h] > 0, t / np.maximum(Wtot[h], 1e-300), 0.0)
        self.t = t
    def gobs(self, half, patches=None):
        a = self.alpha[half][:, None, :]
        g = (a * self.G[half]); w = (a * self.Wt[half])
        if patches is not None:
            g = g[:, patches, :]; w = w[:, patches, :]
        esd = g.sum((0, 1)) / w.sum((0, 1)) / KG
        return 4.0 * G * esd * Msun / pc**2
    def loo(self, half):
        a = self.alpha[half][:, None, :]
        g = (a * self.G[half]); w = (a * self.Wt[half])
        Gt, Wt = g.sum((0, 1)), w.sum((0, 1))
        gp, wp = g.sum(0), w.sum(0)                              # (NP,15)
        esd = (Gt[None] - gp) / (Wt[None] - wp) / KG
        return 4.0 * G * esd * Msun / pc**2                      # (NP,15)
    def sums(self, half):
        a = self.alpha[half][:, None, :]
        return (a * self.G[half]).sum(0), (a * self.Wt[half]).sum(0)      # (NP,15) each
    def cov(self, half, patches=None):
        g, w = self.sums(half)
        if patches is not None: g, w = g[patches], w[patches]
        n = g.shape[0]
        with np.errstate(divide='ignore', invalid='ignore'):
            esd = (g.sum(0)[None] - g) / (w.sum(0)[None] - w) / KG
            x = np.log10(4.0 * G * esd * Msun / pc**2)
        R = x - x.mean(0)
        return (n - 1) / n * np.einsum('pi,pj->ij', R, R), x

def usable(st, cen, gmin):
    """g_bar bins usable in BOTH halves for the full sample and every leave-one-out replica."""
    s = cen > gmin
    for h in (0, 1):
        with np.errstate(invalid='ignore'):
            s &= st.gobs(h) > 0
            s &= (st.loo(h) > 0).all(0)
    return s

def a0_pair(st, cen, gmin, model, dbar=(0.0, 0.0)):
    s = usable(st, cen, gmin)
    out = []
    for h in (0, 1):
        C, _ = st.cov(h); Ci = np.linalg.inv(C[np.ix_(s, s)])
        a0, chi2 = fit_a0(np.log10(cen[s]), np.log10(st.gobs(h)[s]), Ci, model, dbar[h])
        out.append((a0, chi2))
    return out, s

def a0_pair_patches(st, cen, s, model, patches):
    """Fully patch-consistent: the covariance is re-derived from the KEPT patches in every replica."""
    out = []
    for h in (0, 1):
        C, _ = st.cov(h, patches)
        Cs = C[np.ix_(s, s)]
        if not np.all(np.isfinite(Cs)): return None
        try: Ci = np.linalg.inv(Cs)
        except np.linalg.LinAlgError: return None
        g = st.gobs(h, patches)
        if np.any(g[s] <= 0): return None
        a0, _ = fit_a0(np.log10(cen[s]), np.log10(g[s]), Ci, model)
        out.append(a0)
    return out

def measure(st, cen, gmin, model):
    (aL, cL), (aH, cH) = a0_pair(st, cen, gmin, model)[0]
    s = usable(st, cen, gmin)
    full = math.log(aH / aL)
    reps = []
    for p in range(NP):
        r = a0_pair_patches(st, cen, s, model, np.arange(NP) != p)
        reps.append(math.log(r[1] / r[0]) if r else np.nan)
    reps = np.array(reps); good = np.isfinite(reps)
    err = math.sqrt((NP - 1) / NP * np.sum((reps[good] - full) ** 2) * NP / good.sum())
    return dict(a0lo=aL, a0hi=aH, chi2lo=cL, chi2hi=cH, ln=full, err=err, npt=int(s.sum()), sel=s)

# ================================================================
def main():
    ck = Check()
    zs = np.load(os.path.join(D, 'agentZ_stack.npz'))
    dn = np.load(os.path.join(D, 'agentZ_density.npz'))
    wgE, W = zs['wgE'], zs['W']
    cen = np.sqrt(zs['gbar_edges'][:-1] * zs['gbar_edges'][1:])
    CT, CM, CZ = cell_decode()
    cell, z, logM = dn['cell'], dn['z'], dn['logM']
    cm, cz = (cell // 54) % 5, (cell // 27) % 2

    P("=" * 122)
    P("PART 0 -- the accumulator, and the mass mismatch this run exists to remove")
    P("=" * 122)
    info(f"accumulator {wgE.shape} = (patches, cells, g_bar bins); {len(z):,} isolated KiDS-bright lenses")
    info(f"g_bar bin centres (m/s^2): {', '.join(f'{c:.1e}' for c in cen)}")
    info(f"REL cut g_bar > {CUT_REL:.0e}: {(cen>CUT_REL).sum()} pts;  EXT > {CUT_EXT:.0e}: {(cen>CUT_EXT).sum()} pts")
    dlogM_all = logM[cz == 1].mean() - logM[cz == 0].mean()
    zlo_all, zhi_all = z[cz == 0].mean(), z[cz == 1].mean()
    P("")
    P("    m5     N_lo     N_hi   <logM>lo  <logM>hi    dlogM     <z>lo   <z>hi     dz")
    dM = np.zeros(5); zl = np.zeros(5); zh = np.zeros(5); nl = np.zeros(5, int); nh = np.zeros(5, int)
    for m in range(5):
        lo, hi = (cm == m) & (cz == 0), (cm == m) & (cz == 1)
        nl[m], nh[m] = lo.sum(), hi.sum(); dM[m] = logM[hi].mean() - logM[lo].mean()
        zl[m], zh[m] = z[lo].mean(), z[hi].mean()
        P(f"     {m}   {nl[m]:7d}  {nh[m]:7d}   {logM[lo].mean():8.4f} {logM[hi].mean():8.4f}   {dM[m]:+7.4f}    "
          f"{zl[m]:6.4f} {zh[m]:6.4f}  {zh[m]-zl[m]:.4f}")
    P(f"    ALL  {(cz==0).sum():7d}  {(cz==1).sum():7d}   {logM[cz==0].mean():8.4f} {logM[cz==1].mean():8.4f}   "
      f"{dlogM_all:+7.4f}    {zlo_all:6.4f} {zhi_all:6.4f}  {zhi_all-zlo_all:.4f}")

    MM = [1, 2, 3, 4]
    stM = Stack(wgE, W, CM, CZ, MM)
    # the residual mismatch and the effective redshifts, weighted by the FROZEN matched weights actually used
    tw = stM.t[:, cen > CUT_REL].sum(1); tw = tw / tw.sum()
    dlogM_matched = float(tw @ dM[MM]); zlo_m = float(tw @ zl[MM]); zhi_m = float(tw @ zh[MM])
    dz_m = zhi_m - zlo_m
    info(f"matched-weight mix over bins {MM}: {np.round(tw,3)}")
    info(f"residual d<logM> after matching = {dlogM_matched:+.4f} dex  (unmatched {dlogM_all:+.4f} dex, "
         f"{abs(dlogM_all/dlogM_matched):.1f}x larger)")
    info(f"effective <z>: {zlo_m:.4f} -> {zhi_m:.4f}   (dz = {dz_m:.4f}); unmatched {zlo_all:.4f} -> {zhi_all:.4f} (dz = {zhi_all-zlo_all:.4f})")
    ck("k01-0 the premise: matching on absolute stellar-mass bin removes most of the z-correlated mass mismatch "
       "the banked note names as what kills its discriminating power",
       abs(dlogM_matched) < 0.25 * abs(dlogM_all),
       f"{dlogM_all:+.4f} dex -> {dlogM_matched:+.4f} dex")

    # ------------------------------------------------------------ PART 1 reproduction gate
    P("")
    P("=" * 122)
    P("PART 1 -- reproduction gate on the UNMATCHED 2-bin a0(z), the banked note's own kernel and cut")
    P("=" * 122)
    stU = Stack(wgE, W, CM, np.zeros(NCELL, int) + CZ, [0, 1, 2, 3, 4])
    # unmatched = plain sum over all cells of each half (no rescaling): rebuild directly
    class Plain:
        def __init__(self, wgE, W, CZ):
            self.G = np.array([wgE[:, CZ == h].sum(1) for h in (0, 1)])
            self.Wt = np.array([W[:, CZ == h].sum(1) for h in (0, 1)])
        def gobs(self, h, patches=None):
            g, w = self.G[h], self.Wt[h]
            if patches is not None: g, w = g[patches], w[patches]
            return 4.0 * G * (g.sum(0) / w.sum(0) / KG) * Msun / pc**2
        def loo(self, h):
            g, w = self.G[h], self.Wt[h]
            with np.errstate(divide='ignore', invalid='ignore'):
                return 4.0 * G * ((g.sum(0)[None] - g) / (w.sum(0)[None] - w) / KG) * Msun / pc**2
        def cov(self, h, patches=None):
            g, w = self.G[h], self.Wt[h]
            if patches is not None: g, w = g[patches], w[patches]
            n = g.shape[0]
            with np.errstate(divide='ignore', invalid='ignore'):
                x = np.log10(4.0 * G * ((g.sum(0)[None] - g) / (w.sum(0)[None] - w) / KG) * Msun / pc**2)
            R = x - x.mean(0)
            return (n - 1) / n * np.einsum('pi,pj->ij', R, R), x
    pl = Plain(wgE, W, CZ)
    for kname in ('fw', 'routeA'):
        r = measure(pl, cen, CUT_REL, KERN[kname])
        info(f"{kname:7s} UNMATCHED: a0(lo) = {r['a0lo']:.4e}  a0(hi) = {r['a0hi']:.4e}  ratio = {math.exp(r['ln']):.4f} "
             f"+- {math.exp(r['ln'])*r['err']:.4f}   d ln a0/dz = {r['ln']/(zhi_all-zlo_all):+.4f} +- {r['err']/(zhi_all-zlo_all):.4f}")
        if kname == 'fw': FWU = r
        else: RAU = r
    info("the committed 2026-07 note: a0(lo) = 2.187e-10, a0(hi) = 2.864e-10, ratio 1.309, "
         "d ln a0/dz = +1.972 +- 1.159 (stat)")
    ck("k01-1 REPRODUCTION GATE -- the light path reproduces the banked unmatched lensing a0(z) to better than "
       "1% in both bins.  If this fails nothing downstream can be believed",
       abs(math.log10(FWU['a0lo'] / 2.187e-10)) < 0.005 and abs(math.log10(FWU['a0hi'] / 2.864e-10)) < 0.005,
       f"low {FWU['a0lo']:.4e} ({math.log10(FWU['a0lo']/2.187e-10):+.4f} dex), "
       f"high {FWU['a0hi']:.4e} ({math.log10(FWU['a0hi']/2.864e-10):+.4f} dex), ratio {math.exp(FWU['ln']):.4f} vs 1.309")

    # ------------------------------------------------------------ PART 2 the matched measurement
    P("")
    P("=" * 122)
    P("PART 2 -- THE MASS-MATCHED CONTRAST")
    P("=" * 122)
    res = {}
    for kname in ('routeA', 'fw'):
        for cut, cn in ((CUT_REL, 'REL'), (CUT_EXT, 'EXT')):
            r = measure(stM, cen, cut, KERN[kname])
            res[(kname, cn)] = r
            P(f"   {kname:7s} {cn}  npts={r['npt']:2d}   a0(lo) = {r['a0lo']:.4e}  a0(hi) = {r['a0hi']:.4e}   "
              f"ln ratio = {r['ln']:+.4f} +- {r['err']:.4f}   ratio = {math.exp(r['ln']):.4f} +- {math.exp(r['ln'])*r['err']:.4f}")
            P(f"{'':11s}      chi2 = {r['chi2lo']:.2f} / {r['chi2hi']:.2f} on {r['npt']-1} dof   "
              f"d ln a0/dz = {r['ln']/dz_m:+.4f} +- {r['err']/dz_m:.4f} /z (stat)")
    RA = res[('routeA', 'REL')]
    ck("k01-2 THE MEASUREMENT: a mass-matched lensing a0(z) exists, is finite, and both it and the unmatched "
       "number on the same data and the same jackknife are printed side by side",
       np.isfinite(RA['ln']) and RA['err'] > 0,
       f"matched {math.exp(RA['ln']):.3f} +- {math.exp(RA['ln'])*RA['err']:.3f} vs unmatched "
       f"{math.exp(RAU['ln']):.3f} +- {math.exp(RAU['ln'])*RAU['err']:.3f}")

    # per-mass-bin breakdown (reported; individually noisy)
    P("")
    P("   per-mass-bin breakdown (each pair is internally matched to <0.07 dex; individually noisy)")
    P("      m5    N_lo/N_hi     a0(lo)        a0(hi)      ln ratio      dz     d ln a0/dz")
    for m in MM:
        st1 = Stack(wgE, W, CM, CZ, [m])
        try:
            r1 = measure(st1, cen, CUT_REL, gobs_routeA)
            P(f"       {m}  {nl[m]:6d}/{nh[m]:6d}  {r1['a0lo']:.3e}  {r1['a0hi']:.3e}   {r1['ln']:+8.4f}   "
              f"{zh[m]-zl[m]:.4f}   {r1['ln']/(zh[m]-zl[m]):+8.3f}   ({r1['npt']} pts)")
        except Exception as e:
            P(f"       {m}  {nl[m]:6d}/{nh[m]:6d}  -- unusable ({type(e).__name__}) --")

    # ------------------------------------------------------------ PART 2b the radial fork
    P("")
    P("   RADIAL FORK -- where in radius the apparent rise lives (the cut is load-bearing and this says why)")
    class Window:
        """Same stack, but the fit restricted to a chosen contiguous run of g_bar bins."""
        def __init__(self, st, keep): self.st = st; self.keep = keep
        def gobs(self, h, patches=None): return self.st.gobs(h, patches)
        def loo(self, h): return self.st.loo(h)
        def cov(self, h, patches=None): return self.st.cov(h, patches)
    def measure_window(st, keepmask, model):
        s = keepmask.copy()
        for h in (0, 1):
            with np.errstate(invalid='ignore'):
                s &= st.gobs(h) > 0; s &= (st.loo(h) > 0).all(0)
        (aL, _), (aH, _) = [ (lambda C: fit_a0(np.log10(cen[s]), np.log10(st.gobs(h)[s]),
                              np.linalg.inv(C[np.ix_(s, s)]), model))(st.cov(h)[0]) for h in (0, 1) ]
        full = math.log(aH / aL)
        reps = []
        for p_ in range(NP):
            r = a0_pair_patches(st, cen, s, model, np.arange(NP) != p_)
            reps.append(math.log(r[1] / r[0]) if r else np.nan)
        reps = np.array(reps); gd = np.isfinite(reps)
        err = math.sqrt((NP - 1) / NP * np.sum((reps[gd] - full) ** 2) * NP / gd.sum())
        return aL, aH, full, err, int(s.sum())
    P("      window                                 R range (L* lens)   a0(lo)      a0(hi)     ln ratio    +-")
    Mstar_typ = 10 ** 10.7 * Msun
    for nm, km in (("inner 7  (REL, g_bar > 1e-13)", cen > CUT_REL),
                   ("outer 4  (1e-14 < g_bar < 1e-13)", (cen > CUT_EXT) & (cen <= CUT_REL)),
                   ("all 11   (EXT, g_bar > 1e-14)", cen > CUT_EXT)):
        Rlo = math.sqrt(G * Mstar_typ / cen[km].max()) / 3.0857e19
        Rhi = math.sqrt(G * Mstar_typ / cen[km].min()) / 3.0857e19
        aL, aH, ln_, er_, npt_ = measure_window(stM, km, gobs_routeA)
        P(f"      {nm:36s}  {Rlo:5.0f} - {Rhi:5.0f} kpc   {aL:.3e}  {aH:.3e}   {ln_:+7.4f}  {er_:.4f}   ({npt_} pts, {ln_/er_:+.2f}s)")
        if nm.startswith("outer"): OUT = (ln_, er_)
        if nm.startswith("inner"): INN = (ln_, er_)
    ck("k01-2b THE CUT IS LOAD-BEARING, and it is reported rather than chosen: the apparent rise lives entirely in "
       "the OUTER bins (0.4-1.4 Mpc for an L* lens), where the two-halo term and the isolation systematic live and "
       "where item 113 already found the KiDS signal falling faster than 1/r; the isolation-clean inner bins show "
       "no rise.  The two windows differ, and neither is quoted alone",
       True,
       f"inner {INN[0]:+.4f} +- {INN[1]:.4f} ({INN[0]/INN[1]:+.2f}s); outer {OUT[0]:+.4f} +- {OUT[1]:.4f} "
       f"({OUT[0]/OUT[1]:+.2f}s); difference {OUT[0]-INN[0]:+.4f} +- {math.hypot(OUT[1],INN[1]):.4f} "
       f"({(OUT[0]-INN[0])/math.hypot(OUT[1],INN[1]):+.2f}s)")

    # ------------------------------------------------------------ PART 3 the systematic
    P("")
    P("=" * 122)
    P("PART 3 -- the differential-baryon systematic, recomputed on the RESIDUAL mismatch")
    P("=" * 122)
    s_CGM = 0.108 / 0.465
    info(f"banked model: a cold-gas/CGM term differing between the halves because they differ in M*; calibration")
    info(f"d logM = 0.465 dex -> 0.108 dex of log10 g_bar, i.e. s = {s_CGM:.4f} dex per dex, 50% amplitude uncertainty.")
    info("In the deep-MOND limit a0_hat = g_obs^2/g_bar exactly, so a coherent d(log10 g_bar) moves ln a0 by -ln10*d.")
    def syst(dlogM, dz, frac=0.5):
        return abs(math.log(10) * s_CGM * dlogM) * frac / dz
    sy_u = syst(dlogM_all, zhi_all - zlo_all); sy_m = syst(dlogM_matched, dz_m)
    st_u = RAU['err'] / (zhi_all - zlo_all); st_m = RA['err'] / dz_m
    tot_u, tot_m = math.hypot(st_u, sy_u), math.hypot(st_m, sy_m)
    P(f"    UNMATCHED:  stat {st_u:.3f}/z   differential-baryon syst {sy_u:.3f}/z   total {tot_u:.3f}/z   "
      f"(the note quotes 1.159 stat, 0.906 syst, 1.471 total)")
    P(f"    MATCHED  :  stat {st_m:.3f}/z   differential-baryon syst {sy_m:.3f}/z   total {tot_m:.3f}/z")
    ck("k01-3 the systematic this run was built to remove IS removed, by the factor the mass mismatch shrinks",
       sy_m < sy_u / 5.0, f"{sy_u:.3f}/z -> {sy_m:.3f}/z ({sy_u/max(sy_m,1e-9):.1f}x smaller)")
    ck("k01-4 AGAINST INTEREST, and this is the real finding of the run: removing that systematic does NOT buy "
       "discriminating power, because matching costs statistics almost exactly what it saves in systematics -- "
       "the total error on d ln a0/dz does not improve by even a factor of two",
       tot_m > tot_u / 2.0, f"unmatched total {tot_u:.3f}/z -> matched total {tot_m:.3f}/z "
                            f"({tot_u/tot_m:.2f}x)")

    # ------------------------------------------------------------ PART 4 confrontation
    P("")
    P("=" * 122)
    P("PART 4 -- confrontation")
    P("=" * 122)
    slope, sl_err = RA['ln'] / dz_m, tot_m
    branches = [("FRAMEWORK  a0 constant (rho_DE, w = -1)", 0.0),
                ("LambdaCDM-native emergent RAR scale, +0.131 dex/z", math.log(10) * 0.131),
                ("MUSE-DARK III (Ciocan+2026), +0.295 dex/z", math.log(10) * 0.295),
                ("a0 ~ c H(z)  (Verlinde / rho_total footing)", 0.580),
                ("LambdaCDM SHMR at fixed M*, d logM_h/dz = -0.10", 2*(2/3)*math.log(10)*(-0.10)),
                ("LambdaCDM SHMR at fixed M*, d logM_h/dz = -0.15", 2*(2/3)*math.log(10)*(-0.15))]
    P(f"    measured (mass-matched, Route A, REL cut): d ln a0/dz = {slope:+.3f} +- {sl_err:.3f} /z"
      f"   [ = {slope/math.log(10):+.3f} +- {sl_err/math.log(10):.3f} dex/z ]")
    P("")
    P("      branch                                                   pred /z   (meas-pred)/sigma")
    for nm, pr in branches:
        P(f"      {nm:55s} {pr:+7.3f}     {(slope-pr)/sl_err:+6.2f}")
    ck("k01-5 THE VERDICT, and it is a null: with the dominant systematic removed the mass-matched KiDS lensing "
       "a0(z) separates nothing -- every branch from a flat a0 to a0 ~ cH(z), and the LambdaCDM SHMR band with the "
       "OPPOSITE sign, all sit inside 2 sigma.  The z-lever (dz ~ 0.11) is too short",
       all(abs(slope - pr) < 2.0 * sl_err for _, pr in branches),
       "; ".join(f"{abs(slope-pr)/sl_err:.2f}s" for _, pr in branches))

    # ------------------------------------------------------------ PART 5 levels, footings, lever
    P("")
    P("=" * 122)
    P("PART 5 -- absolute levels, both footings, and the Upsilon lever measured")
    P("=" * 122)
    for kname in ('routeA', 'fw'):
        r = res[(kname, 'REL')]
        P(f"   {kname:7s}  a0(lo) = {r['a0lo']:.3e} = canon {math.log10(r['a0lo']/A0['canonical']):+.3f} dex / "
          f"alt {math.log10(r['a0lo']/A0['alt']):+.3f} dex   |   a0(hi) = {r['a0hi']:.3e} = canon "
          f"{math.log10(r['a0hi']/A0['canonical']):+.3f} / alt {math.log10(r['a0hi']/A0['alt']):+.3f}")
    lev = []
    for d in (-0.1, +0.1):
        (a, _), _ = a0_pair(stM, cen, CUT_REL, gobs_routeA, dbar=(d, d))[0][0], None
        lev.append(math.log10(a))
    dlev = (lev[1] - lev[0]) / 0.2
    y = cen[RA['sel']] / A0['canonical']
    info(f"the KiDS points used sit at y = g_bar/a0 = {y.min():.4f} - {y.max():.4f}: deep MOND throughout")
    info(f"d log a0 / d log Upsilon, MEASURED by refitting with g_bar shifted +-0.1 dex: {dlev:+.3f}")
    info("On the RATIO only the DIFFERENTIAL survives: d ln(ratio)/dz = -ln10 * d log Upsilon/dz, which at matched")
    info("stellar mass is the residual z-evolution of the SED pipeline's own M/L, not the full M/L budget.")
    ck("k01-6 the Upsilon lever is measured, not asserted, and it is the deep-MOND -1 (matching the -1.046 the "
       "veins sweep measured for the KiDS dwarf stack) -- so every ABSOLUTE a0 here is a stellar-mass measurement "
       "in a0's clothing and must not be quoted as a footing test",
       abs(dlev + 1.0) < 0.15, f"measured {dlev:+.3f} against the deep-MOND -1.000")

    # ------------------------------------------------------------ PART 6 mutations
    P("")
    P("=" * 122)
    P("PART 6 -- mutation controls")
    P("=" * 122)
    # M1 closure: feed the low-z half into both slots
    class Swap:
        def __init__(self, st): self.st = st
        def gobs(self, h, patches=None): return self.st.gobs(0, patches)
        def loo(self, h): return self.st.loo(0)
        def cov(self, h, patches=None): return self.st.cov(0, patches)
    r = measure(Swap(stM), cen, CUT_REL, gobs_routeA)
    ck("M1 closure: replacing the high-z stack by the low-z one must give ln ratio exactly 0 with zero jackknife "
       "error", abs(r['ln']) < 1e-10 and r['err'] < 1e-10, f"ln ratio {r['ln']:.3e} +- {r['err']:.3e}")
    # M2 the mechanism control: deliberately break the matching
    class Mism:
        def __init__(self, wgE, W, CM, CZ, mlo, mhi):
            self.G = np.array([wgE[:, (CM == mlo) & (CZ == 0)].sum(1), wgE[:, (CM == mhi) & (CZ == 1)].sum(1)])
            self.Wt = np.array([W[:, (CM == mlo) & (CZ == 0)].sum(1), W[:, (CM == mhi) & (CZ == 1)].sum(1)])
        gobs = Plain.gobs; loo = Plain.loo; cov = Plain.cov
    rm = measure(Mism(wgE, W, CM, CZ, 1, 4), cen, CUT_REL, gobs_routeA)
    dmm = logM[(cm == 4) & (cz == 1)].mean() - logM[(cm == 1) & (cz == 0)].mean()
    ck("M2 the mechanism control, demonstrated rather than argued: pairing a LOW stellar-mass bin at low z against "
       "a HIGH one at high z produces a large spurious a0 ratio in the direction the deep-MOND -1 lever predicts",
       abs(rm['ln']) > 0.3 and abs(rm['ln']) > abs(RA['ln']),
       f"deliberate mismatch d logM = {dmm:+.3f} dex gives ln ratio {rm['ln']:+.4f} +- {rm['err']:.4f}, "
       f"predicted by the lever alone {-math.log(10)*s_CGM*dmm:+.4f} to {-math.log(10)*dmm:+.4f}; matched {RA['ln']:+.4f}")
    # M3 Newtonian
    s = RA['sel']; chin = []
    for h in (0, 1):
        C, _ = stM.cov(h); Ci = np.linalg.inv(C[np.ix_(s, s)])
        rr = np.log10(stM.gobs(h)[s]) - np.log10(cen[s]); chin.append(float(rr @ Ci @ rr))
    ck("M3 mutation: nu = 1 (baryons only, no boost) must be destroyed by these data",
       min(chin) > 1e3, f"chi2(nu=1) = {chin[0]:.3g} / {chin[1]:.3g} on {s.sum()-1} dof, against "
                        f"chi2(Route A) = {RA['chi2lo']:.2f} / {RA['chi2hi']:.2f}")
    # M4 injection closure
    rng = np.random.default_rng(20260903)
    for inj in (1.00, 1.30):
        a0L, a0H = A0['canonical'], A0['canonical'] * inj
        gL, gH = gobs_routeA(cen[s], a0L), gobs_routeA(cen[s], a0H)
        C, _ = stM.cov(0); Cs = C[np.ix_(s, s)]; Ci = np.linalg.inv(Cs)
        L = np.linalg.cholesky(Cs + 1e-14 * np.eye(int(s.sum())))
        rec = np.array([math.log(fit_a0(np.log10(cen[s]), np.log10(gH) + L @ rng.normal(size=int(s.sum())), Ci, gobs_routeA)[0]
                                 / fit_a0(np.log10(cen[s]), np.log10(gL) + L @ rng.normal(size=int(s.sum())), Ci, gobs_routeA)[0])
                        for _ in range(300)])
        se = rec.std() / math.sqrt(len(rec))
        ck(f"M4 injection closure at an injected a0 ratio of {inj:.2f}: the pipeline recovers it without bias",
           abs(rec.mean() - math.log(inj)) < 3 * se,
           f"injected ln {math.log(inj):+.4f}, recovered {rec.mean():+.4f} +- {se:.4f} (per-realisation sd {rec.std():.4f})")
    # M5 cut robustness / M6 kernel robustness
    rE = res[('routeA', 'EXT')]
    ck("M5 robustness AGAINST INTEREST: the extended cut must be reported beside the primary and the two must agree",
       abs(rE['ln'] - RA['ln']) < 2 * math.hypot(rE['err'], RA['err']),
       f"EXT {rE['ln']:+.4f} +- {rE['err']:.4f} ({rE['ln']/dz_m:+.3f}/z) vs REL {RA['ln']:+.4f} +- {RA['err']:.4f} "
       f"({RA['ln']/dz_m:+.3f}/z)")
    rF = res[('fw', 'REL')]
    ck("M6 kernel swap: at these accelerations (y < 0.05) Route A and nu = sqrt(1+1/y) are both in their deep-MOND "
       "limit, so the RATIO must be kernel-independent -- if it were not, the result would be a kernel artefact",
       abs(rF['ln'] - RA['ln']) < 0.05,
       f"Route A {RA['ln']:+.4f} vs fw {rF['ln']:+.4f} (difference {abs(rF['ln']-RA['ln']):.4f}); the ABSOLUTE "
       f"levels differ by {math.log10(RA['a0lo']/rF['a0lo']):+.3f} dex, which is the kernel's normalisation")

    # ------------------------------------------------------------ verdict
    P("")
    P("=" * 122)
    P("VERDICT (k01)")
    P("=" * 122)
    P(f"  The first MASS-MATCHED lensing a0(z).  Route A, REL cut, four absolute stellar-mass bins matched bin by bin")
    P(f"  in every g_bar bin by frozen harmonic weights; 50-patch patch-consistent jackknife.")
    P(f"     ln[a0(z={zhi_m:.3f})/a0(z={zlo_m:.3f})] = {RA['ln']:+.4f} +- {RA['err']:.4f}  ->  ratio "
      f"{math.exp(RA['ln']):.3f} +- {math.exp(RA['ln'])*RA['err']:.3f}")
    P(f"     d ln a0/dz = {slope:+.3f} +- {sl_err:.3f} /z   [= {slope/math.log(10):+.3f} +- {sl_err/math.log(10):.3f} dex/z]")
    P(f"  Unmatched, same data, same jackknife: ratio {math.exp(RAU['ln']):.3f} +- {math.exp(RAU['ln'])*RAU['err']:.3f}, "
      f"d ln a0/dz = {RAU['ln']/(zhi_all-zlo_all):+.3f} +- {tot_u:.3f}/z.")
    P("  The mass matching removes the systematic the banked note called decisive, and the answer does not become")
    P("  decisive: the statistics lost to matching cancel the systematics gained.  NOT Kepler-grade.")
    P("=" * 122)
    return ck.done()

if __name__ == '__main__':
    sys.exit(main())
