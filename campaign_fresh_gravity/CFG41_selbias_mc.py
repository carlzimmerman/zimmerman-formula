#!/usr/bin/env python3
"""
selbias_mc.py -- Monte-Carlo of the SELECTION BIAS on log(v_obs / v_law) for a
sample cut on OBSERVED speed (v_obs > 300 km/s) and log M_* > 11.0.
This checks a bias.  It does not judge any theory.

EVERYTHING BELOW IS DECLARED BEFORE THE FIRST RUN (nothing tuned afterwards).

1. Law (asymptotic flat speed):  v_law^4 = G * M_b * a0,  a0 = 1.2e-10 m/s^2,
   M_b = M_* + M_gas.   G = 6.6743e-11, Msun = 1.98847e30 kg.  v in km/s.
   (300 km/s corresponds to log M_b = 11.71 on the law: the cut is a large
   upward fluctuation for typical log M_b ~ 11.2-11.4.)

2. Parent population (per Mpc^3 per dex): Schechter in log M_*,
       phi(x) dx  ∝  u^(alpha+1) exp(-u),   u = 10^(x - logMc),   x = log M_*
   restricted to x >= 11.0 (upper edge 12.4, negligible), sampled by exact
   inverse-CDF on a 200001-point grid.
     BASE : alpha = -1.0, logMc = 10.7   (Chabrier-IMF-like characteristic mass);
            local slope of the number density at x=11.0 is -4.6 per dex.
     FLAT : alpha = -0.6, logMc = 10.9   (slower fall-off, slope -2.0 per dex).
     STEEP: alpha = -1.2, logMc = 10.5   (faster fall-off, slope -7.7 per dex).
   The parent is the population of spirals; a morphology/HI-detection factor is
   NOT modelled (its mass dependence would only alter the slope, which the
   FLAT/STEEP variants bracket).  M_* is treated as exactly known.

3. Gas: log M_gas = 10.3 + 0.3 * N(0,1), independent of M_*  (M_gas =
   10^10.3 Msun (M_*/1e11)^0 with 0.3 dex Gaussian scatter).  M_b known exactly.

4. Observed speed (SINGLE-MEASUREMENT model, the one requested):
       log v_obs = log v_law(M_b) + delta + s * N(0,1)
   s in {0.02, 0.04, 0.06, 0.08, 0.10} dex.  delta = 0 (law true) and
   delta = +0.05 dex (extra true excess).  The SAME v_obs is used for the cut and
   for the test statistic.  Selection: v_obs > 300 km/s and log M_* >= 11.0.

5. Statistic: e = log10(v_obs / v_law) among the selected.  Reported per config:
   parent survival fraction, n_surv, mean(e), SD(e) among the selected;
   E[mean_N] = mean(e) (the mean of N i.i.d. selected galaxies is unbiased for the
   selected-population mean) with SE = SD/sqrt(N) for N = 13 and 15; significance
   mean/SE(15); the a0-equivalent factor 10^(4 mean) (v^4 = G M a0, so a speed
   offset of d dex is an a0 rescaling of 4 d dex).  A 20000-replicate resample of
   N=13,15 from the selected pool checks SE.  Also mean log v_obs, mean arithmetic
   v_obs, mean log M_*, mean log M_b, expected min/max of log M_* and of v in a
   15-galaxy draw (resampling), for comparison with the real 15 (mean v_flat ~290,
   mean log M_* ~11.25, log M_* 11.0-11.7, v_flat 176-450).

6. Exact cross-check: deterministic quadrature (trapezoid, 12001 x 801 grid, truncated-normal moments over a
   log M_* x log M_gas grid) of survival fraction, mean e, SD e, mean log M_*.

7. TWO-MEASUREMENT EXTENSION (realism; needed because the real selection speed is
   the ALFALFA width and the tested speed is the modelled HI v_flat, and because
   mean(v_flat) = 290 < 300 cannot occur if one v_obs is both cut and tested):
       log v_sel  = log v_law + e_int + e_w      (cut variable, > 300 km/s)
       log v_flat = log v_law + e_int + e_f      (tested variable)
   e_int ~ N(0, s_int) shared (true speed departure from the law + anything common
   to both measurements), e_w ~ N(0, s_w) width/inclination error (selection
   only), e_f ~ N(0, 0.02) v_flat modelling error.  Grid: s_int in {0.02,0.04,0.06},
   s_w in {0.03,0.05,0.08,0.12,0.16}; BASE mass function; law true (delta = 0).
   Bias of the test = mean(e_int + e_f) among the selected.
   AMENDMENT (declared after a reduced-size smoke test of this script, before the
   full run; the smoke test showed the v_flat spread was far narrower than the real
   176-450 km/s): the grid is widened to s_int in {0.02,0.04,0.06,0.08,0.10} and
   e_f width s_f in {0.02, 0.08} (s_f does not change the bias, only the v_flat
   spread/SE).  A row is flagged MATCH if mean v_flat in [280,300] km/s AND mean
   log M_* in [11.20,11.30] (the real sample's ~290 km/s and ~11.25).
   Also added to Table 2: P(max log M_* >= 11.65 in a 15-galaxy draw).

8. DESIGNS, all evaluated inside the same MC (BASE mass function, single-measurement):
   A  raw mean of e among the selected (the biased estimator);
   B  OLS of log M_b on log v_obs among the selected (v as the independent
      variable): slope, and offset of the fitted line from the law expressed in
      speed units, [logM_law(x) - yhat(x)]/4, at x = mean log v_obs and at
      x = log 300; plus mean e in observed-speed bins (Tweedie/Eddington check);
   C  mass-selected subsample: (i) no speed cut (selection independent of v) and
      (ii) speed-selected sample restricted to log M_b > X, X in {11.3,...,12.1};
   D  truncated-likelihood estimate of delta CONDITIONED on M_b, with the
      per-galaxy truncation point c_i = log(300/v_law,i) and known s (also s
      mis-specified by x0.7 and x1.3):
        logL(delta) = sum_i [ -(e_i-delta)^2/(2 s^2) - log Phi((delta-c_i)/s) ]
      evaluated at N=15 by 3000 resamples of the selected pool; mean and SD of
      (delta_hat - delta_true).

9. Sizes and seeds: 2e8 parent draws per single-measurement mass function (chunks
   of 4e6), 1e8 for the two-measurement extension, seed 20260928.  Pools of at most
   400000 selected galaxies are kept per configuration for resampling/regression.
"""
import sys
import time
import numpy as np
from scipy.special import ndtr, log_ndtr
from scipy.stats import norm

# ------------------------------------------------------------------ constants
G = 6.6743e-11
MSUN = 1.98847e30
A0 = 1.2e-10
LOGK = np.log10(G * MSUN * A0)
VCUT = 300.0
LOGCUT = np.log10(VCUT)
XMIN = 11.0
XMAX = 12.4
LOGMG0, SIGMG = 10.3, 0.3
S_LIST = [0.02, 0.04, 0.06, 0.08, 0.10]
DELTAS = [0.0, 0.05]
SEED = 20260928
N_PARENT = int(2e8)
N_PARENT_TWO = int(1e8)
CHUNK = int(4e6)
POOLCAP = 400000
XS_MB = [11.3, 11.5, 11.7, 11.9, 12.1]
EBINS = [(300, 320), (320, 350), (350, 400), (400, 600)]


def log_vlaw(logMb):
    """log10 of v_law in km/s"""
    return 0.25 * (LOGK + logMb) - 3.0


def logM_of_logv(x):
    """law-implied log M_b for log10 v (km/s) = x"""
    return 4.0 * (x + 3.0) - LOGK


class MassFn:
    def __init__(self, name, alpha, logMc):
        self.name, self.alpha, self.logMc = name, alpha, logMc
        self.grid = np.linspace(XMIN, XMAX, 200001)
        u = 10 ** (self.grid - logMc)
        self.pdf = u ** (alpha + 1.0) * np.exp(-u)
        cdf = np.cumsum(self.pdf)
        self.cdf = (cdf - cdf[0]) / (cdf[-1] - cdf[0])
        u0 = 10 ** (XMIN - logMc)
        self.slope = np.log(10) * ((alpha + 1.0) - u0)

    def draw(self, rng, n):
        return np.interp(rng.random(n), self.cdf, self.grid)


MASSFNS = [MassFn("BASE", -1.0, 10.7), MassFn("FLAT", -0.6, 10.9),
           MassFn("STEEP", -1.2, 10.5)]


# ------------------------------------------------------------ quadrature check
def quad_single(mf, s, d, nx=12001, ng=801):
    xs = np.linspace(XMIN, XMAX, nx)
    u = 10 ** (xs - mf.logMc)
    ws = u ** (mf.alpha + 1.0) * np.exp(-u)
    wtrap = np.ones(nx)
    wtrap[0] = wtrap[-1] = 0.5          # trapezoid end weights
    ws = ws * wtrap
    ws /= ws.sum()
    zg = np.linspace(-7, 7, ng)
    wg = norm.pdf(zg)
    wg /= wg.sum()
    lg = LOGMG0 + SIGMG * zg
    Mb = np.log10(10 ** xs[:, None] + 10 ** lg[None, :])
    c = LOGCUT - log_vlaw(Mb)
    z0 = (c - d) / s
    logQ = log_ndtr(-z0)
    P = np.exp(logQ)
    lam = np.exp(norm.logpdf(z0) - logQ)
    me = d + s * lam
    ve = s * s * (1.0 + z0 * lam - lam * lam)
    W = ws[:, None] * wg[None, :]
    frac_parent = (W * P).sum()
    mu = (W * P * me).sum() / frac_parent
    e2 = (W * P * (ve + me * me)).sum() / frac_parent
    sd = np.sqrt(e2 - mu * mu)
    mMs = (W * P * xs[:, None]).sum() / frac_parent
    return frac_parent, mu, sd, mMs


# ------------------------------------------------------------- single-meas MC
def run_single(mf, n_parent, seed):
    rng = np.random.default_rng(seed)
    configs = [(s, d) for d in DELTAS for s in S_LIST]
    acc = {}
    for cfg in configs:
        acc[cfg] = dict(n=0, se=0.0, se2=0.0, sx=0.0, sv=0.0, sMs=0.0, sMb=0.0,
                        nX=np.zeros(len(XS_MB)), seX=np.zeros(len(XS_MB)),
                        nB=np.zeros(len(EBINS)), seB=np.zeros(len(EBINS)),
                        pool=[], npool=0)
    tot = 0
    sum_e_parent = {s: 0.0 for s in S_LIST}
    sum_e2_parent = {s: 0.0 for s in S_LIST}
    nch = n_parent // CHUNK
    for ic in range(nch):
        logMs = mf.draw(rng, CHUNK)
        logMg = LOGMG0 + SIGMG * rng.standard_normal(CHUNK)
        z = rng.standard_normal(CHUNK)
        logMb = np.log10(10 ** logMs + 10 ** logMg)
        lv = log_vlaw(logMb)
        tot += CHUNK
        for s in S_LIST:
            sum_e_parent[s] += s * z.sum()
            sum_e2_parent[s] += (s * s) * (z * z).sum()
        for (s, d) in configs:
            e = d + s * z
            x = lv + e
            m = x > LOGCUT
            a = acc[(s, d)]
            n = int(m.sum())
            if n == 0:
                continue
            es, xsel, Ms, Mb = e[m], x[m], logMs[m], logMb[m]
            a['n'] += n
            a['se'] += es.sum()
            a['se2'] += (es * es).sum()
            a['sx'] += xsel.sum()
            a['sv'] += (10 ** xsel).sum()
            a['sMs'] += Ms.sum()
            a['sMb'] += Mb.sum()
            for k, X in enumerate(XS_MB):
                mm = Mb > X
                a['nX'][k] += mm.sum()
                a['seX'][k] += es[mm].sum()
            vs = 10 ** xsel
            for k, (lo, hi) in enumerate(EBINS):
                mm = (vs >= lo) & (vs < hi)
                a['nB'][k] += mm.sum()
                a['seB'][k] += es[mm].sum()
            if a['npool'] < POOLCAP:
                take = min(n, POOLCAP - a['npool'])
                a['pool'].append(np.vstack([Ms[:take], Mb[:take], es[:take],
                                            xsel[:take]]))
                a['npool'] += take
    for cfg in configs:
        a = acc[cfg]
        a['pool'] = np.hstack(a['pool']) if a['pool'] else np.zeros((4, 0))
        a['tot'] = tot
    return acc, tot, sum_e_parent, sum_e2_parent


# ----------------------------------------------------------- two-meas MC
def run_two(mf, n_parent, seed, s_ints, s_ws, s_fs):
    rng = np.random.default_rng(seed + 1)
    configs = [(si, sw, sf) for si in s_ints for sw in s_ws for sf in s_fs]
    acc = {c: dict(n=0, se=0.0, se2=0.0, sxf=0.0, svf=0.0, sMs=0.0, sxf2=0.0,
                   sxs=0.0, pool=[], npool=0) for c in configs}
    tot = 0
    for ic in range(n_parent // CHUNK):
        logMs = mf.draw(rng, CHUNK)
        logMg = LOGMG0 + SIGMG * rng.standard_normal(CHUNK)
        zi = rng.standard_normal(CHUNK)
        zw = rng.standard_normal(CHUNK)
        zf = rng.standard_normal(CHUNK)
        logMb = np.log10(10 ** logMs + 10 ** logMg)
        lv = log_vlaw(logMb)
        tot += CHUNK
        for (si, sw, s_f) in configs:
            eint = si * zi
            xsel = lv + eint + sw * zw
            m = xsel > LOGCUT
            n = int(m.sum())
            if n == 0:
                continue
            a = acc[(si, sw, s_f)]
            ef = (eint + s_f * zf)[m]
            xf = lv[m] + ef
            a['n'] += n
            a['se'] += ef.sum()
            a['se2'] += (ef * ef).sum()
            a['sxf'] += xf.sum()
            a['sxf2'] += (xf * xf).sum()
            a['svf'] += (10 ** xf).sum()
            a['sMs'] += logMs[m].sum()
            a['sxs'] += xsel[m].sum()
            if a['npool'] < POOLCAP:
                take = min(n, POOLCAP - a['npool'])
                a['pool'].append(np.vstack([logMs[m][:take], ef[:take], xf[:take]]))
                a['npool'] += take
    for c in configs:
        a = acc[c]
        a['pool'] = np.hstack(a['pool']) if a['pool'] else np.zeros((3, 0))
    return acc, tot


# ----------------------------------------------------------------- utilities
def ols_vec(x, y):
    """x,y shape (R,N): slope, intercept per row"""
    xm, ym = x.mean(1, keepdims=True), y.mean(1, keepdims=True)
    b = ((x - xm) * (y - ym)).sum(1) / ((x - xm) ** 2).sum(1)
    a = ym[:, 0] - b * xm[:, 0]
    return b, a


def mle_delta(e, c, s_assume, grid):
    """e,c shape (R,N). returns delta_hat per row (grid + parabolic refinement)"""
    R, N = e.shape
    ll = np.empty((R, grid.size))
    for j, dl in enumerate(grid):
        ll[:, j] = (-(e - dl) ** 2 / (2 * s_assume ** 2)
                    - log_ndtr((dl - c) / s_assume)).sum(1)
    j = ll.argmax(1)
    j = np.clip(j, 1, grid.size - 2)
    r = np.arange(R)
    y0, y1, y2 = ll[r, j - 1], ll[r, j], ll[r, j + 1]
    h = grid[1] - grid[0]
    den = (y0 - 2 * y1 + y2)
    off = np.where(np.abs(den) > 1e-12, 0.5 * (y0 - y2) / den, 0.0)
    return grid[j] + np.clip(off, -1, 1) * h


def fmt(v, w=8, p=4):
    return f"{v:{w}.{p}f}"


def main():
    t0 = time.time()
    out = []
    P = lambda *a: (print(*a), sys.stdout.flush())

    P("=" * 100)
    P("selbias_mc.py  --  selection bias of a v_obs > 300 km/s cut on log(v_obs/v_law)")
    P(f"a0={A0:g}  G={G:g}  logM_b at which v_law=300 km/s: {logM_of_logv(LOGCUT):.3f}")
    P("law speed for the real sample's mean M_*=10^11.25, M_gas=10^10.3: "
      f"{10**log_vlaw(np.log10(10**11.25+10**10.3)):.1f} km/s "
      f"(log(290/that)={np.log10(290/10**log_vlaw(np.log10(10**11.25+10**10.3))):+.3f} dex)")
    for mf in MASSFNS:
        P(f"mass fn {mf.name}: alpha={mf.alpha}, logMc={mf.logMc}, number-density slope at 11.0 = {mf.slope:.2f}/dex")
    P("=" * 100)

    results = {}
    for mf in MASSFNS:
        acc, tot, sep, se2p = run_single(mf, N_PARENT, SEED)
        results[mf.name] = (acc, tot, sep, se2p)
        P(f"[{mf.name}] single-measurement MC done ({tot:.2e} parent draws), t={time.time()-t0:.0f}s")

    rng = np.random.default_rng(SEED + 7)
    base_acc, base_tot, sep, se2p = results["BASE"]

    # ------------------------------------------------------------ TABLE 1
    def summarise(a):
        n = a['n']
        mean = a['se'] / n
        sd = np.sqrt(max(a['se2'] / n - mean ** 2, 0.0))
        return n, mean, sd

    for d in DELTAS:
        P("")
        P(f"TABLE 1{'a' if d == 0 else 'b'}  BASE mass fn, single-measurement, delta_true = {d:+.2f} dex, "
          f"cut v_obs>300 & logM*>=11.0")
        hdr = ("  s    frac_surv  n_surv  mean_e(MC)  quad    SD_e   | N=13: mean +/- SE  | N=15: mean +/- SE  "
               "z(15)  a0-fac 10^(4 mean)" + ("  induced=mean-delta" if d else ""))
        P(hdr)
        for s in S_LIST:
            a = base_acc[(s, d)]
            n, mean, sd = summarise(a)
            fq, muq, sdq, mMsq = quad_single(MASSFNS[0], s, d)
            se13, se15 = sd / np.sqrt(13), sd / np.sqrt(15)
            P(f"{s:5.2f}  {n/base_tot:9.3e} {n:7d}  {mean:+.4f}    {muq:+.4f}  {sd:.4f} |"
              f"  {mean:+.4f} +/- {se13:.4f}  |  {mean:+.4f} +/- {se15:.4f}  {mean/se15:5.2f}  "
              f"{10**(4*mean):6.3f}" + (f"      {mean-d:+.4f}" if d else ""))
        P("  (quad columns: frac_surv_quad, SD_quad below)")
        for s in S_LIST:
            fq, muq, sdq, mMsq = quad_single(MASSFNS[0], s, d)
            a = base_acc[(s, d)]
            n, mean, sd = summarise(a)
            P(f"   s={s:.2f}: frac quad={fq:.3e} (MC {n/base_tot:.3e});  SD quad={sdq:.4f} (MC {sd:.4f});  "
              f"mean logM* quad={mMsq:.4f} (MC {a['sMs']/n:.4f})")

    # resample check of SE
    P("")
    P("SE CHECK (BASE, delta=0): empirical SD of the mean of N i.i.d. selected galaxies (20000 resamples) vs SD/sqrt(N)")
    for s in S_LIST:
        a = base_acc[(s, 0.0)]
        pool = a['pool']
        n, mean, sd = summarise(a)
        row = []
        for N in (13, 15):
            idx = rng.integers(0, pool.shape[1], size=(20000, N))
            mN = pool[2][idx].mean(1)
            row.append(f"N={N}: emp mean {mN.mean():+.4f} SD {mN.std():.4f} vs SD/sqrtN {sd/np.sqrt(N):.4f}")
        P(f"  s={s:.2f}  " + "   ".join(row) + f"   (pool {pool.shape[1]})")

    # ------------------------------------------------------------ TABLE 2
    P("")
    P("TABLE 2  properties of the SELECTED sample, BASE mass fn (single-measurement).  Real sample: mean v_flat ~290, "
      "mean logM* ~11.25, logM* 11.0-11.7, v_flat 176-450")
    P("  delta   s    mean_logv_obs  mean_v_obs[km/s]  mean_logM*  mean_logM_b   E[min logM*]/E[max logM*] (N=15)  "
      "E[min v]/E[max v] (N=15)   P(max logM*>=11.65)")
    for d in DELTAS:
        for s in S_LIST:
            a = base_acc[(s, d)]
            n = a['n']
            pool = a['pool']
            idx = rng.integers(0, pool.shape[1], size=(5000, 15))
            Ms15, x15 = pool[0][idx], pool[3][idx]
            P(f"  {d:+.2f}  {s:.2f}   {a['sx']/n:9.4f}   {a['sv']/n:12.1f}     {a['sMs']/n:8.4f}   {a['sMb']/n:8.4f}"
              f"      {Ms15.min(1).mean():.3f} / {Ms15.max(1).mean():.3f}                      "
              f"{10**x15.min(1).mean():.0f} / {10**x15.max(1).mean():.0f}       {(Ms15.max(1) >= 11.65).mean():.3f}")

    # ------------------------------------------------------------ TABLE 3
    P("")
    P("TABLE 3  mass-function variants (single-measurement), delta=0: frac_surv, mean_e, SD_e, mean logM*, and quad check")
    P("  mf      s    frac_surv   n_surv   mean_e    SD_e   SE(15)   mean_logM*   | quad: frac   mean_e   SD_e")
    for mf in MASSFNS:
        acc, tot, _, _ = results[mf.name]
        for d in DELTAS:
            for s in S_LIST:
                a = acc[(s, d)]
                n, mean, sd = summarise(a)
                fq, muq, sdq, mMsq = quad_single(mf, s, d)
                P(f"  {mf.name:5s} d={d:+.2f} {s:.2f}  {n/tot:9.3e} {n:8d}  {mean:+.4f}  {sd:.4f}  {sd/np.sqrt(15):.4f}"
                  f"   {a['sMs']/n:8.4f}    | {fq:9.3e} {muq:+.4f} {sdq:.4f}")

    # ------------------------------------------------------------ TABLE 4 two-measurement
    s_ints = [0.02, 0.04, 0.06, 0.08, 0.10]
    s_ws = [0.03, 0.05, 0.08, 0.12, 0.16]
    s_fs = [0.02, 0.08]
    acc2, tot2 = run_two(MASSFNS[0], N_PARENT_TWO, SEED, s_ints, s_ws, s_fs)
    P("")
    P(f"TABLE 4  TWO-MEASUREMENT extension (BASE mass fn, delta=0; cut on v_sel, test v_flat)  [{tot2:.1e} parent draws]")
    P("  s_int  s_w   s_f  frac_surv   n_surv   BIAS=mean(e_flat)  SD(e_flat) SE(15)  z(15)  mean_v_flat mean_logM*  "
      "SD(logv_flat) E[min/max logM*](15) E[min/max v_flat](15)  MATCH")
    for si in s_ints:
        for sw in s_ws:
            for sf in s_fs:
                a = acc2[(si, sw, sf)]
                n = a['n']
                mean = a['se'] / n
                sd = np.sqrt(max(a['se2'] / n - mean ** 2, 0))
                mxf = a['sxf'] / n
                sdlv = np.sqrt(max(a['sxf2'] / n - mxf ** 2, 0))
                pool = a['pool']
                idx = rng.integers(0, pool.shape[1], size=(4000, 15))
                Ms15 = pool[0][idx]
                v15 = 10 ** pool[2][idx]
                mv, mMs = a['svf'] / n, a['sMs'] / n
                flag = "MATCH" if (280 <= mv <= 300 and 11.20 <= mMs <= 11.30) else ""
                P(f"  {si:.2f}  {sw:.2f}  {sf:.2f} {n/tot2:9.3e} {n:8d}     {mean:+.4f}          {sd:.4f}   {sd/np.sqrt(15):.4f} "
                  f"{mean/(sd/np.sqrt(15)):5.2f}   {mv:8.1f}    {mMs:.4f}     {sdlv:.4f}"
                  f"      {Ms15.min(1).mean():.2f}/{Ms15.max(1).mean():.2f}        {v15.min(1).mean():.0f}/{v15.max(1).mean():.0f}      {flag}")

    # ------------------------------------------------------------ TABLE 5 designs
    P("")
    P("TABLE 5  DESIGNS (BASE mass fn, single-measurement)")
    P(" 5B  OLS of log M_b (y) on log v_obs (x) among the SELECTED; law: slope 4.")
    P("     offset_B(x) = [logM_law(x) - yhat(x)]/4 in dex of speed.  At x=mean(x) it equals mean(e) EXACTLY (OLS passes")
    P("     through the means), so it is the same number as design A.  SD of slope at N=15 by resampling.")
    P("  delta   s    slope_pop   slope SD(N=15)   offset_B(mean x)=mean_e   offset_B(x=log300)   intercept-only(slope=4)=same as A")
    for d in DELTAS:
        for s in S_LIST:
            a = base_acc[(s, d)]
            pool = a['pool']
            Mb, e, x = pool[1], pool[2], pool[3]
            b = np.polyfit(x, Mb, 1)
            slope, icpt = b[0], b[1]
            xm = x.mean()
            off_mean = (logM_of_logv(xm) - (icpt + slope * xm)) / 4.0
            off_300 = (logM_of_logv(LOGCUT) - (icpt + slope * LOGCUT)) / 4.0
            idx = rng.integers(0, pool.shape[1], size=(4000, 15))
            b15, a15 = ols_vec(x[idx], Mb[idx])
            P(f"  {d:+.2f}  {s:.2f}   {slope:8.3f}     {b15.std():8.3f}        {off_mean:+.4f} (mean e {e.mean():+.4f})"
              f"        {off_300:+.4f}                  {e.mean():+.4f}")
    P("")
    P(" 5B'  mean e in bins of OBSERVED speed (all galaxies in the bin are above the cut, so this is E[e | v_obs]; it is")
    P("      positive for ANY sample with a falling mass function: Tweedie/Eddington term  s^2 |d ln m/d log v|, NOT the cut)")
    P("  delta   s    " + "   ".join(f"[{lo},{hi})km/s" for lo, hi in EBINS))
    for d in DELTAS:
        for s in S_LIST:
            a = base_acc[(s, d)]
            cells = []
            for k in range(len(EBINS)):
                cells.append(f"{a['seB'][k]/a['nB'][k]:+.4f}({int(a['nB'][k])})" if a['nB'][k] > 0 else "   n/a")
            P(f"  {d:+.2f}  {s:.2f}   " + "   ".join(cells))

    P("")
    P(" 5C  mass-selected subsamples (selection independent of the speed noise):")
    P("     (i) no speed cut, logM*>=11.0: mean e over the whole parent (should be 0 +/- s/sqrt(N_parent)); SE for N=15 is s/sqrt(15)")
    for s in S_LIST:
        m = sep[s] / base_tot
        sd = np.sqrt(se2p[s] / base_tot - m * m)
        P(f"     s={s:.2f}: mean e = {m:+.2e}   SD e = {sd:.4f}   SE(N=15) = {sd/np.sqrt(15):.4f}")
    P("     (ii) speed-selected (v_obs>300) but restricted to logM_b > X: mean e (n).  Bias -> 0 only once X is high enough that")
    P("          the cut is no longer binding (P(sel|M_b) ~ 1 needs v_law >~ 300*10^(2 s), i.e. logM_b >~ 11.71 + 8 s).")
    P("  delta   s    " + "   ".join(f"X={X}" for X in XS_MB))
    for d in DELTAS:
        for s in S_LIST:
            a = base_acc[(s, d)]
            cells = []
            for k in range(len(XS_MB)):
                cells.append(f"{a['seX'][k]/a['nX'][k]:+.4f}({int(a['nX'][k])})" if a['nX'][k] > 0 else "   n/a")
            P(f"  {d:+.2f}  {s:.2f}   " + "   ".join(cells))

    P("")
    P(" 5D  truncated-likelihood estimate of delta conditioned on M_b (per-galaxy cut), N=15, 3000 resamples of the selected pool")
    P("      columns: s_assumed/s_true ; mean(delta_hat - delta_true) ; SD(delta_hat)  ;  (for reference raw-mean bias, raw SD at N=15)")
    grid = np.arange(-0.25, 0.35, 0.002)
    P("  delta   s    | s_assumed=1.0 s: bias   SD  | 0.7 s: bias   SD  | 1.3 s: bias   SD  | raw mean: bias   SD")
    for d in DELTAS:
        for s in S_LIST:
            a = base_acc[(s, d)]
            pool = a['pool']
            Mb, e = pool[1], pool[2]
            c = LOGCUT - log_vlaw(Mb)
            idx = rng.integers(0, pool.shape[1], size=(3000, 15))
            E, C = e[idx], c[idx]
            cells = []
            for f in (1.0, 0.7, 1.3):
                dh = mle_delta(E, C, s * f, grid)
                cells.append(f"{dh.mean()-d:+.4f} {dh.std():.4f}")
            raw = E.mean(1)
            P(f"  {d:+.2f}  {s:.2f}   | {cells[0]} | {cells[1]} | {cells[2]} | {raw.mean()-d:+.4f} {raw.std():.4f}")
    P("")
    P(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
