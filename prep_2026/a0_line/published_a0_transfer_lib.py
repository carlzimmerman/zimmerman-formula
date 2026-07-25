#!/usr/bin/env python3
"""
published_a0_transfer_lib.py -- shared machinery for the question:
  DOES THE a0-LINE ESTIMATOR BIAS (+10.3 pp on gls_origin, deep-MOND, per-point a0)
  TRANSFER TO THE *PUBLISHED* SPARC a0 (g_dagger = 1.20e-10, McGaugh+2016 / Lelli+2017)?

Nothing here decides anything.  It provides:
  * make_sample()  -- real SPARC structure, FULL range (y ~ 0.01 .. 98) or the frozen
                      gas-dominated cut (y <= 0.19) used as the regression anchor.
  * draw_noise()   -- byte-for-byte the frozen PREREG_ESTIMATOR_BIAS.md recipe
                      (globals -> per-galaxy -> per-point, same guards, same order).
  * observables()  -- the frozen forward model, generalized to either nu form.
  * the two nu forms and their log-log slopes.
  * every estimator family, each implemented in ITS OWN convention.

HONESTY RAILS carried from the frozen prereg:
  * mocks are generated FROM a nu, so they test ESTIMATORS only, never the law;
  * a0's VALUE remains POSITED in the framework -- this is measurement methodology;
  * each family is injected at 9.355e-11, 1.1305e-10 AND 1.2e-10 so no value is privileged;
  * a family is judged on |bias| only, so the gate cannot see which way it leans.
"""
import numpy as np, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fire_common as fc                                             # noqa: E402

LN10 = math.log(10.0)
SLNB, SIG_LNU, SIG_LNG, SIG_INC = fc.SLNB, fc.SIG_LNU, fc.SIG_LNG, fc.SIG_INC

# the three injected values -- identical to the frozen prereg, so NEITHER footing and
# NEITHER the published value is privileged
A0_CANON = 9.354769736111044e-11        # c*H_Lambda/Z   (framework, canonical footing)
A0_ALT = 1.1305322040279838e-10         # c*H0/Z          (framework, ALT footing)
A0_MOND = 1.2e-10                       # g_dagger        (McGaugh+2016 published)
INJ = [A0_CANON, A0_ALT, A0_MOND]
INJ_LAB = ["canonical cH_L/Z", "ALT cH0/Z", "published g_dagger"]


# ============================================================== the two nu / RAR forms
def F_form(g, a, form):
    """Model g_obs(g_bar; a).  FW = the framework's OWN nu = sqrt(1+1/y);
    MCG = the McGaugh+2016 / Lelli+2017 RAR function that the PUBLISHED g_dagger fits."""
    if form == "FW":
        return np.sqrt(g * g + a * g)
    if form == "MCG":
        return g / (-np.expm1(-np.sqrt(g / a)))
    raise ValueError(form)


def S_form(g, a, form):
    """d log F / d log g_bar -- the log-log slope (needed for every errors-on-both-axes
    fit).  Both forms -> 1/2 deep, 1 Newtonian."""
    if form == "FW":
        return (2.0 * g + a) / (2.0 * (g + a))
    if form == "MCG":
        s = np.sqrt(g / a)
        return 1.0 - s * np.exp(-s) / (2.0 * (-np.expm1(-s)))
    raise ValueError(form)


# ===================================================================== the real sample
def make_sample(Ud=0.70, gas_only=False):
    """Real SPARC structure held FIXED as the truth: Q<=2, inc>=30 deg, eV/Vobs<0.10."""
    gals = fc.load(Ud)
    GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, gas_only)
    _, GALI = np.unique(GAL, return_inverse=True)
    G = int(GALI.max()) + 1
    NPT = np.bincount(GALI)
    assert np.array_equal(GALI, np.repeat(np.arange(G), NPT)), "points not galaxy-ordered"
    STARTS = np.concatenate(([0], np.cumsum(NPT)[:-1]))
    SLD_g = np.array([SLD[GALI == k][0] for k in range(G)])
    INC_g = np.arctan(1.0 / np.array([CTI[GALI == k][0] for k in range(G)]))
    S = dict(GB=GB, GO_real=GO, FV=FV, PHI=PHI, GALI=GALI, NPT=NPT, STARTS=STARTS,
             SLD_g=SLD_g, INC_g=INC_g, CTI=CTI, G=G, N=len(GB), Ud=Ud, gas_only=gas_only)
    # the analyst's assumed per-point log10 errors (what a published fit actually uses)
    S["sig_log_obs"] = np.sqrt(np.repeat(SLD_g, NPT) ** 2
                               + (2.0 * CTI * SIG_INC) ** 2 + (2.0 * FV) ** 2) / LN10
    S["sig_log_bar"] = np.sqrt((PHI * SIG_LNU) ** 2 + ((1 - PHI) * SIG_LNG) ** 2
                               + SLNB ** 2) / LN10
    return S


# ============================================ the frozen noise recipe (copied verbatim)
def draw_noise(S, n_real, seed=20260725):
    """Draw order EXACTLY as frozen: globals -> per-galaxy -> per-point, same redraw
    guards.  Independent of a_inj and of the nu form -> common random numbers."""
    G, N, SLD_g, INC_g, FV = S["G"], S["N"], S["SLD_g"], S["INC_g"], S["FV"]
    seqs = np.random.SeedSequence(seed).spawn(n_real)
    dlnU = np.empty(n_real); dlnG = np.empty(n_real)
    dlnD = np.empty((n_real, G)); di = np.empty((n_real, G))
    eps = np.empty((n_real, N)); dv = np.empty((n_real, N))
    n_ri = n_rv = 0
    lo, hi = np.deg2rad(5.0), np.deg2rad(90.0)
    for r in range(n_real):
        rng = np.random.default_rng(seqs[r])
        dlnU[r] = rng.normal(0.0, SIG_LNU)
        dlnG[r] = rng.normal(0.0, SIG_LNG)
        dlnD[r] = rng.normal(0.0, SLD_g)
        d = rng.normal(0.0, SIG_INC, G)
        bad = (INC_g + d <= lo) | (INC_g + d > hi)
        while bad.any():
            n_ri += int(bad.sum())
            d[bad] = rng.normal(0.0, SIG_INC, int(bad.sum()))
            bad = (INC_g + d <= lo) | (INC_g + d > hi)
        di[r] = d
        eps[r] = rng.normal(0.0, SLNB, N)
        v = rng.normal(0.0, FV)
        bad = (1.0 + v) <= 0.05
        while bad.any():
            n_rv += int(bad.sum())
            v[bad] = rng.normal(0.0, FV[bad])
            bad = (1.0 + v) <= 0.05
        dv[r] = v
    return dict(dlnU=dlnU, dlnG=dlnG, dlnD=dlnD, di=di, eps=eps, dv=dv,
                n_redraw_i=n_ri, n_redraw_v=n_rv)


def slice_noise(nz, s, e):
    return {k: (v[s:e] if isinstance(v, np.ndarray) and v.ndim >= 1 else v)
            for k, v in nz.items()}


def observables(S, a_inj, form, nz, scale=1.0):
    """The frozen forward model.  g_bar is EXACTLY distance-independent; distance,
    inclination and velocity enter only g_obs.  No clipping, no re-cutting, ever."""
    GB, PHI, NPT, INC_g = S["GB"], S["PHI"], S["NPT"], S["INC_g"]
    gt = F_form(GB, a_inj, form)
    fU = np.exp(scale * nz["dlnU"])[:, None]
    fG = np.exp(scale * nz["dlnG"])[:, None]
    gbar = GB[None, :] * (PHI[None, :] * fU + (1 - PHI[None, :]) * fG) \
        * np.exp(scale * nz["eps"])
    incf = (np.sin(INC_g)[None, :] / np.sin(INC_g[None, :] + scale * nz["di"])) ** 2
    gobs = gt[None, :] * np.exp(-scale * np.repeat(nz["dlnD"], NPT, axis=1)) \
        * np.repeat(incf, NPT, axis=1) * (1.0 + scale * nz["dv"]) ** 2
    return gbar, gobs


# ================================================ FAMILY (a): the a0-line per-point route
def gls_vec(S, GBo, GOo, itmax=300):
    """fire_common.gls, vectorized: iterated through-origin GLS with MODEL-based weights,
    a0_hat = sum w E g / sum w g^2.  This is the INCUMBENT that is biased +10.3 pp on the
    gas-dominated cut.  It is a WEIGHTED MEAN of per-point a0 -- i.e. mean-like."""
    FV = S["FV"]
    GBo = np.atleast_2d(GBo); GOo = np.atleast_2d(GOo)
    M = GOo.shape[0]
    E = GOo ** 2 - GBo ** 2
    a0 = np.full(M, 1e-10); fint = np.full(M, 0.2)
    active = np.ones(M, bool)
    for _ in range(itmax):
        GOm2 = GBo ** 2 + a0[:, None] * GBo
        s2 = (4 * GOm2 * FV) ** 2 + (2 * GBo ** 2 * SLNB) ** 2 + (fint[:, None] * GOm2) ** 2
        w = 1.0 / s2
        a0n = (w * E * GBo).sum(1) / (w * GBo ** 2).sum(1)
        c2n = ((E - a0n[:, None] * GBo) ** 2 * w).sum(1) / GOo.shape[1]
        fintn = np.maximum(0.01, fint * c2n ** 0.25)
        conv = active & (np.abs(a0n - a0) < 1e-17) & (np.abs(c2n - 1) < 1e-3)
        a0 = np.where(active, a0n, a0)
        fint = np.where(active, fintn, fint)
        active &= ~conv
        if not active.any():
            break
    return a0


def median_a0pt(GBo, GOo):
    return np.median((GOo ** 2 - GBo ** 2) / GBo, axis=1)


# =========================================== grid machinery for every likelihood family
def _parab(chi2, lg):
    """Sub-grid minimum of chi2(lg) by 3-point parabolic interpolation, row-wise.
    Returns (a_hat, at_edge)."""
    j = np.argmin(chi2, axis=1)
    edge = (j == 0) | (j == chi2.shape[1] - 1)
    jc = np.clip(j, 1, chi2.shape[1] - 2)
    r = np.arange(chi2.shape[0])
    c0, cm, cp = chi2[r, jc], chi2[r, jc - 1], chi2[r, jc + 1]
    den = (cp - 2 * c0 + cm)
    step = np.where(np.abs(den) > 0, 0.5 * (cm - cp) / np.where(den == 0, 1.0, den), 0.0)
    step = np.clip(step, -1.0, 1.0)
    d = lg[1] - lg[0]
    return 10.0 ** (lg[jc] + step * d), edge


def chi2_block(S, gbar, gobs, form, a):
    """chi2(a) for FOUR point-level published-style families at once, plus the per-galaxy
    chi2 needed by the Li+2018-style route.  gbar/gobs: (M,N).  a: (J,).
    Returns dict of (M,J) arrays + 'pergal' (M,G,J).

      odr_log  -- errors-on-BOTH-axes fit in the log-log plane (the effective-variance
                  form of orthogonal distance regression).  THIS IS THE McGaugh+2016 /
                  Lelli+2017 STATISTIC: scipy.odr, unbinned 2693 points, errors in both
                  variables, log-log plane, one free parameter g_dagger.
      odr_lin  -- the same errors-on-both-axes fit performed in LINEAR acceleration space
                  (the other admissible reading of 'orthogonal distance regression').
      nls_log  -- plain vertical-residual weighted least squares in log space (the
                  simplest member of the same family; no horizontal term).
      like_log -- FULL likelihood: log-space Gaussian with the errors CORRECTLY MODELLED,
                  i.e. distance+inclination correlated WITHIN each galaxy (rank-1 block
                  per galaxy) and the Upsilon / gas-cal offsets correlated GLOBALLY
                  (rank-2 across all points), velocity+shape diagonal.  Woodbury.
      pergal   -- Li+2018 convention: chi2 in LINEAR g_obs with sigma = 2 V dV / R
                  = g_obs * 2 * fv, per galaxy.
    """
    FV, PHI, STARTS, NPT = S["FV"], S["PHI"], S["STARTS"], S["NPT"]
    slo, slb = S["sig_log_obs"], S["sig_log_bar"]
    SLD_g, CTI = S["SLD_g"], S["CTI"]
    gb = gbar[:, :, None]; go = gobs[:, :, None]; aa = a[None, None, :]
    F = F_form(gb, aa, form)
    Sl = S_form(gb, aa, form)
    r = np.log10(go) - np.log10(F)
    sy2 = (slo ** 2)[None, :, None]
    sx2 = (slb ** 2)[None, :, None]
    out = {}
    out["nls_log"] = (r * r / sy2).sum(1)
    out["odr_log"] = (r * r / (sy2 + Sl * Sl * sx2)).sum(1)
    rl = go - F
    sy2l = (go * LN10 * slo[None, :, None]) ** 2
    sx2l = (gb * LN10 * slb[None, :, None]) ** 2
    dFdg = F / gb * Sl
    out["odr_lin"] = (rl * rl / (sy2l + dFdg * dFdg * sx2l)).sum(1)
    # ---- Li+2018 per-galaxy chi2 (linear g space, velocity errors only)
    sg = (go * 2.0 * FV[None, :, None]) ** 2
    out["pergal"] = np.add.reduceat(rl * rl / sg, STARTS, axis=1)
    # ---- FULL likelihood, correctly-modelled correlated log-space errors (Woodbury)
    d = (2.0 * FV[None, :, None] / LN10) ** 2 + (Sl * SLNB / LN10) ** 2
    Di = 1.0 / d
    sk = (SLD_g ** 2 + (2.0 * np.array([CTI[STARTS[k]] for k in range(S["G"])])
                        * SIG_INC) ** 2)[None, :, None]          # (1,G,1)
    u = Sl * (PHI[None, :, None]) / LN10                          # global Upsilon vector
    w = Sl * (1 - PHI[None, :, None]) / LN10                      # global gas-cal vector

    def c1inv_dot(x, y):
        """x^T C1^{-1} y with C1 = diag(d) + sum_k s_k q_k q_k^T, q_k = 1_k / LN10."""
        xy = np.add.reduceat(Di * x * y, STARTS, axis=1).sum(1)
        sx_ = np.add.reduceat(Di * x, STARTS, axis=1) / LN10
        sy_ = np.add.reduceat(Di * y, STARTS, axis=1) / LN10
        qq = np.add.reduceat(Di, STARTS, axis=1) / LN10 ** 2
        return xy - (sk * sx_ * sy_ / (1.0 + sk * qq)).sum(1)

    Arr = c1inv_dot(r, r)
    Muu, Mww, Muw = c1inv_dot(u, u), c1inv_dot(w, w), c1inv_dot(u, w)
    bu, bw = c1inv_dot(u, r), c1inv_dot(w, r)
    Auu = Muu + 1.0 / SIG_LNU ** 2
    Aww = Mww + 1.0 / SIG_LNG ** 2
    det = Auu * Aww - Muw * Muw
    quad = (Aww * bu * bu - 2 * Muw * bu * bw + Auu * bw * bw) / det
    out["like_log"] = Arr - quad
    return out


def fit_grid(S, gbar, gobs, form, lg_coarse, keys, nfine=31, dfine=1.5, chunk=20,
             jblock=None):
    """Two-stage grid: coarse chi2 -> per-realization fine grid -> parabola.
    Returns {key: (a_hat, edge_flag)} plus 'pergal_a' (M,G) for the per-galaxy family."""
    M = gbar.shape[0]
    dc = lg_coarse[1] - lg_coarse[0]
    res = {k: np.empty(M) for k in keys}
    edges = {k: np.zeros(M, bool) for k in keys}
    pg_a = np.empty((M, S["G"])); pg_edge = np.zeros((M, S["G"]), bool)
    jb = jblock or max(8, len(lg_coarse) // 4)
    for s in range(0, M, chunk):
        e = min(M, s + chunk)
        gb, go = gbar[s:e], gobs[s:e]
        # ---- stage 1 (coarse), grid streamed in blocks to bound memory
        acc = {k: [] for k in keys}
        pgacc = []
        for js in range(0, len(lg_coarse), jb):
            je = min(len(lg_coarse), js + jb)
            c = chi2_block(S, gb, go, form, 10.0 ** lg_coarse[js:je])
            for k in keys:
                acc[k].append(c[k])
            pgacc.append(c["pergal"])
        C = {k: np.concatenate(acc[k], axis=1) for k in keys}
        PG = np.concatenate(pgacc, axis=2)
        # ---- stage 2 (fine, per realization) for the point-level families
        for k in keys:
            j = np.clip(np.argmin(C[k], axis=1), 1, len(lg_coarse) - 2)
            lgf = lg_coarse[j][:, None] + np.linspace(-dfine * dc, dfine * dc, nfine)[None]
            ch = np.empty((e - s, nfine))
            for i in range(e - s):
                ci = chi2_block(S, gb[i:i + 1], go[i:i + 1], form, 10.0 ** lgf[i])
                ch[i] = ci[k][0]
            a_hat, ed = _parab(ch, np.linspace(-dfine * dc, dfine * dc, nfine))
            res[k][s:e] = a_hat * 10.0 ** lg_coarse[j]
            edges[k][s:e] = ed | (np.argmin(C[k], axis=1) == 0) \
                | (np.argmin(C[k], axis=1) == len(lg_coarse) - 1)
        # ---- per-galaxy: coarse parabola only (49-147 values, then combined robustly)
        jj = np.argmin(PG, axis=2)
        pg_edge[s:e] = (jj == 0) | (jj == len(lg_coarse) - 1)
        jc = np.clip(jj, 1, len(lg_coarse) - 2)
        i0 = np.arange(e - s)[:, None]; i1 = np.arange(S["G"])[None, :]
        c0 = PG[i0, i1, jc]; cm = PG[i0, i1, jc - 1]; cp = PG[i0, i1, jc + 1]
        den = cp - 2 * c0 + cm
        st = np.where(np.abs(den) > 0, 0.5 * (cm - cp) / np.where(den == 0, 1.0, den), 0.0)
        pg_a[s:e] = 10.0 ** (lg_coarse[jc] + np.clip(st, -1, 1) * dc)
    return res, edges, pg_a, pg_edge


# ============================================== FAMILY (d): the binned-mean route
BIN_EDGES = np.arange(-12.2, -7.99, 0.2)


def binned_fits(S, gbar, gobs, form, lg_coarse, minpts=5):
    """Bin in log10 g_bar, collapse each bin to ONE point, then fit the RAR form to the
    bin representatives with EQUAL weight per bin.  Two variants, differing ONLY in how
    the bin is collapsed:
       meanlog -- mean of log10 g  (geometric / median-like)
       meanlin -- log10 of mean g  (arithmetic / mean-like)
    Everything else identical, so the pair isolates the Jensen step exactly."""
    M = gbar.shape[0]
    nb = len(BIN_EDGES) - 1
    out = {}
    for tag in ("meanlog", "meanlin"):
        out[tag] = np.empty(M)
    lb = np.log10(gbar); lo_ = np.log10(gobs)
    for m in range(M):
        idx = np.digitize(lb[m], BIN_EDGES) - 1
        ok = (idx >= 0) & (idx < nb)
        cnt = np.bincount(idx[ok], minlength=nb)
        good = cnt >= minpts
        xg = np.bincount(idx[ok], weights=lb[m][ok], minlength=nb)[good] / cnt[good]
        yg = np.bincount(idx[ok], weights=lo_[m][ok], minlength=nb)[good] / cnt[good]
        xl = np.log10(np.bincount(idx[ok], weights=gbar[m][ok],
                                  minlength=nb)[good] / cnt[good])
        yl = np.log10(np.bincount(idx[ok], weights=gobs[m][ok],
                                  minlength=nb)[good] / cnt[good])
        for tag, (X, Y) in (("meanlog", (xg, yg)), ("meanlin", (xl, yl))):
            gx = 10.0 ** X
            ch = ((Y[None, :] - np.log10(F_form(gx[None, :],
                                                (10.0 ** lg_coarse)[:, None], form)))
                  ** 2).sum(1)
            j = int(np.clip(np.argmin(ch), 1, len(lg_coarse) - 2))
            den = ch[j + 1] - 2 * ch[j] + ch[j - 1]
            st = 0.5 * (ch[j - 1] - ch[j + 1]) / den if den != 0 else 0.0
            d = lg_coarse[1] - lg_coarse[0]
            out[tag][m] = 10.0 ** (lg_coarse[j] + np.clip(st, -1, 1) * d)
    return out
