#!/usr/bin/env python3
"""
LANE B3 -- nu-SHAPE TEST ON RESOLVED-M/L DATA (MIGHTEE-HI RAR, arXiv:2504.20857)
=================================================================================
Varasteanu, Jarvis, Ponomareva, Desmond, et al., MNRAS 2025: 19 HI-selected
galaxies, spatially-resolved M/L from 10-band SED fitting, 80 RAR points.
Per-point table NOT published (commented-out \\input{gbar_gobs_table} in the
arXiv source; "available on request"). Data here are extracted from the vector
PDF of their fiducial figure (Figures/RAR_best_fit_residuals_with_postpredictive.pdf
in the arXiv source tarball): 80 markers + 80 x-error bars + 80 y-error bars,
axis calibration from tick-label positions (calibration residuals 0.0000 dex).

TEST (framework on its OWN terms, both-ways):
  Framework nu (de Sitter-Unruh MI):  g_obs = sqrt(g_bar^2 + g_bar*a0),
                                      nu(y) = sqrt(1+1/y), a0 = 9.36e-11 m/s^2
  McGaugh/MLS nu:                     g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0))),
                                      a0 = 1.2e-10 m/s^2 (canonical MOND)
  (1) shape separation in dex across their g_bar range (fixed-a0 and free-a0)
  (2) MNR-style fits (Roxy-equivalent likelihood, exact 1D quadrature):
      each nu at FIXED canonical a0, then a0 FREE; chi2 + BIC; transition focus
  (3) where does 9.36e-11 sit on their resolved-M/L footing with a0 free
      (canonical fork; also rising fork 1.13e-10 per footing-fork rule)

Likelihood = Marginalised Normal Regression (Bartlett & Desmond, roxy), the
method the paper itself used: per-point x-errors, y-errors, intrinsic scatter,
Gaussian hyperprior on true x (mu_g, w_g). Marginalization over true x done by
exact Gauss-Hermite quadrature (no linearization) -- symmetric between models.

VALIDATION GATE: refitting THEIR nu (MLS) with a0 free must reproduce their
published a0 = (1.69 +/- 0.13)e-10 and sigma_int = 0.045 +/- 0.022 dex. If that
fails, the extraction is not faithful and NO verdict is issued.
"""
import sys, collections
import numpy as np
import fitz
from scipy.optimize import minimize
from scipy.stats import chi2 as chi2dist

SRC = 'src/Figures/RAR_best_fit_residuals_with_postpredictive.pdf'
A0_FRAMEWORK = 9.36e-11    # c^2 sqrt(Lambda/32pi) = cH_Lambda/Z  (canonical fork)
A0_FORK_RISING = 1.13e-10  # rho_total/cH0 footing fork (rule: run both, show spread)
A0_MLS = 1.2e-10           # canonical Milgrom/McGaugh
A0_PAPER = 1.69e-10        # their published MLS fit (resolved-M/L footing)

# ----------------------------------------------------------------------------
# 1. EXTRACTION
# ----------------------------------------------------------------------------
doc = fitz.open(SRC)
page = doc[0]
dr = page.get_drawings()
words = page.get_text('words')

# x-calibration from the 6 drawn tick MARKS (label bboxes are biased by font-box
# centering -- verified: labels match ticks in x to 0.0000 dex, but the y-axis
# label bboxes are offset by a uniform -0.026 dex; hence y is calibrated from
# the drawn g_obs=g_bar 1:1 line, which pins slope AND intercept exactly).
xtm, ytm_res = [], []
for d in dr:
    if d['type'] in ('fs', 's'):
        r = d['rect']
        if abs(r.width) < 0.05 and 4 < r.height < 6 and r.y0 > 370:
            xtm.append((r.x0+r.x1)/2)                     # x-axis tick marks
        if abs(r.height) < 0.05 and 4 < r.width < 6 and r.x0 < 70 and 300 < r.y0 < 390:
            ytm_res.append((r.y0+r.y1)/2)                 # residual-panel y ticks
xtm = sorted(xtm); vx = np.arange(-12.5, -9.9, 0.5)
assert len(xtm) == 6
Ax, Bx = np.polyfit(xtm, vx, 1)

# 1:1 line: the unique long diagonal single-segment stroke
line = None
for d in dr:
    if d['type'] == 's' and len(d['items']) == 1 and d['items'][0][0] == 'l':
        p1, p2 = d['items'][0][1], d['items'][0][2]
        if abs(p2.x-p1.x) > 50 and abs(p2.y-p1.y) > 50:
            line = (p1, p2)
p1, p2 = line
m_line = (p2.y-p1.y)/(p2.x-p1.x); c_line = p1.y - m_line*p1.x
Ay = Ax/m_line; By = Bx - Ay*c_line       # data_y == data_x along the line

ytm_res = sorted(ytm_res); vres = np.array([0.25, 0.00, -0.25])
assert len(ytm_res) == 3
Ar, Br = np.polyfit(ytm_res, vres, 1)

calib_res = np.max(np.abs(Ax*np.array(xtm)+Bx - vx))
assert calib_res < 2e-3, 'axis calibration failed'

mk = []
for d in dr:
    if d['type'] != 'fs': continue
    r = d['rect']
    if abs(r.width-7.07) < 0.5 and abs(r.height-7.07) < 0.5:
        mk.append((r.x0+r.width/2, r.y0+r.height/2, str(d.get('fill'))))
mxy = np.array([(m[0], m[1]) for m in mk]); mcol = [m[2] for m in mk]
top = mxy[:,1] < 290
assert top.sum() == 80 and (~top).sum() == 80, 'expected 80+80 markers'

H, V = [], []
for d in dr:
    if d['type'] != 's': continue
    its = d['items']
    if len(its) == 1 and its[0][0] == 'l':
        p1, p2 = its[0][1], its[0][2]
        if abs(p1.y-p2.y) < 0.01 and abs(p1.x-p2.x) > 0.02:
            H.append(((p1.x+p2.x)/2, (p1.y+p2.y)/2, abs(p2.x-p1.x)))
        elif abs(p1.x-p2.x) < 0.01 and abs(p1.y-p2.y) > 0.02:
            V.append(((p1.x+p2.x)/2, (p1.y+p2.y)/2, abs(p2.y-p1.y)))
H, V = np.array(H), np.array(V)

def match(bars, pts, tol=1.0):
    out = np.full(len(pts), np.nan)
    for bx, by, ln in bars:
        dd = np.hypot(pts[:,0]-bx, pts[:,1]-by)
        i = np.argmin(dd)
        if dd[i] < tol: out[i] = ln
    return out

pts  = mxy[top];  cols = [c for c, t in zip(mcol, top) if t]
rpts = mxy[~top]; rcols = [c for c, t in zip(mcol, top) if not t]
ex = match(H[H[:,1] < 290], pts); ey = match(V[V[:,1] < 290], pts)
assert np.isfinite(ex).all() and np.isfinite(ey).all(), 'unmatched error bars'

x  = Ax*pts[:,0] + Bx          # log10 g_bar  [m/s^2]
y  = Ay*pts[:,1] + By          # log10 g_obs  [m/s^2]
sx = np.abs(Ax)*ex/2.          # 1-sigma x error (dex); bar total length = 2 sigma
sy = np.abs(Ay)*ey/2.          # 1-sigma y error (dex)
n  = len(x)

print('='*78)
print('EXTRACTION: %d points, 19 galaxies (%d distinct marker colours)' %
      (n, len(set(cols))))
print('  log g_bar in [%.2f, %.2f], log g_obs in [%.2f, %.2f]' %
      (x.min(), x.max(), y.min(), y.max()))
print('  median sigma_x = %.3f dex, median sigma_y = %.3f dex' %
      (np.median(sx), np.median(sy)))
print('  axis-calibration max residual: %.4f dex' % calib_res)

# --- cross-check A: the figure's own best-fit curves, in this calibration,
#     must reproduce the PUBLISHED fits (red = MLS@1.69e-10 sample-alone,
#     blue = MLS@1.32e-10 combined) -- absolute anchors for the extraction.
def F_mls(logg, a0):
    g = 10.**logg
    return logg - np.log10(1. - np.exp(-np.sqrt(g/a0)))

def curve_pts(d):
    P = []
    for it in d['items']:
        if it[0] == 'l': P += [it[1], it[2]]
        elif it[0] == 'c': P += [it[1], it[2], it[3], it[4]]
    return np.array([[p.x, p.y] for p in P])

red = blue = None
for d in dr:
    if d['type'] == 's' and len(d['items']) > 5:
        if d.get('color') == (1.0, 0.0, 0.0): red = d
        if d.get('color') == (0.0, 0.0, 1.0): blue = d
for tag, cdr, a0c in (('red = published sample-alone MLS@1.69e-10', red, 1.69e-10),
                      ('blue = published combined MLS@1.32e-10   ', blue, 1.32e-10)):
    P = curve_pts(cdr)
    lx = Ax*P[:,0]+Bx; ok = (lx > -12.4) & (lx < -10.0)
    rr = (Ay*P[ok,1]+By) - F_mls(lx[ok], a0c)
    print('  curve anchor [%s]: mean %+0.4f dex, rms %.4f dex' % (tag, rr.mean(), rr.std()))
    assert abs(rr.mean()) < 5e-3 and rr.std() < 5e-3, 'curve anchor failed'

# --- cross-check B: bottom residual panel equals (model - data) at their fit
res_extracted = Ar*rpts[:,1] + Br
order_top = np.argsort(pts[:,0]); order_res = np.argsort(rpts[:,0])
dx_pair = np.abs(pts[order_top,0] - rpts[order_res,0])
model_minus_data = F_mls(x[order_top], A0_PAPER) - y[order_top]
rms_check = np.sqrt(np.mean((model_minus_data - res_extracted[order_res])**2))
print('  cross-check (residual panel vs model-data @ their a0=1.69e-10):')
print('    marker x-alignment: max %.3f pt; rms(published residual - recomputed) = %.4f dex'
      % (dx_pair.max(), rms_check))

# ----------------------------------------------------------------------------
# 2. THE TWO INTERPOLATIONS + MNR LIKELIHOOD
# ----------------------------------------------------------------------------
def F_framework(logg, a0):
    """log10 g_obs = log10 sqrt(g_bar^2 + g_bar*a0)  (nu = sqrt(1+1/y))"""
    g = 10.**logg
    return 0.5*np.log10(g*g + g*a0)

FUN = {'framework': F_framework, 'mls': F_mls}

# Gauss-Hermite nodes for exact marginalization over true x
GH_T, GH_W = np.polynomial.hermite.hermgauss(48)

def neg2lnL(theta, model, a0=None):
    """theta = (log10 a0?, sigma_int, mu_g, w_g); MNR marginal likelihood."""
    if a0 is None:
        la0, sig, mug, wg = theta; a0v = 10.**la0
    else:
        sig, mug, wg = theta; a0v = a0
    if sig < 0 or wg <= 1e-4: return 1e10
    F = FUN[model]
    s2 = sx**2 + wg**2
    m_i = (x*wg**2 + mug*sx**2)/s2          # posterior mean of true x
    s_i = np.sqrt(sx**2*wg**2/s2)           # posterior sd of true x
    lnpref = -0.5*np.log(2*np.pi*s2) - 0.5*(x-mug)**2/s2
    st2 = sy**2 + sig**2
    xt = m_i[:, None] + np.sqrt(2.)*s_i[:, None]*GH_T[None, :]   # (n, K)
    fy = F(xt, a0v)
    ln_gauss = -0.5*np.log(2*np.pi*st2)[:, None] - 0.5*(y[:, None]-fy)**2/st2[:, None]
    mx = ln_gauss.max(axis=1)
    lnint = mx + np.log(np.sum(GH_W[None, :]*np.exp(ln_gauss-mx[:, None]), axis=1)/np.sqrt(np.pi))
    return -2.*np.sum(lnpref + lnint)

def fit(model, a0=None, la0_start=None):
    starts = []
    for sig0 in (0.02, 0.08):
        for mug0 in (np.mean(x),):
            for wg0 in (np.std(x), 0.7*np.std(x)):
                s = [sig0, mug0, wg0]
                if a0 is None: s = [la0_start if la0_start else -9.8] + s
                starts.append(s)
    best = None
    for s0 in starts:
        r = minimize(neg2lnL, s0, args=(model, a0), method='Nelder-Mead',
                     options=dict(maxiter=6000, xatol=1e-6, fatol=1e-8))
        if best is None or r.fun < best.fun: best = r
    return best

# ----------------------------------------------------------------------------
# 3. VALIDATION GATE: reproduce THEIR published fit with THEIR nu
# ----------------------------------------------------------------------------
val = fit('mls', a0=None, la0_start=np.log10(A0_PAPER))
a0_val = 10.**val.x[0]; sig_val = val.x[1]
print('\n' + '='*78)
print('VALIDATION GATE (their nu, a0 free)  [published: a0=(1.69+/-0.13)e-10, sig=0.045+/-0.022]')
print('  recovered: a0 = %.3fe-10, sigma_int = %.3f dex, mu_g=%.2f, w_g=%.2f'
      % (a0_val*1e10, sig_val, val.x[2], val.x[3]))
ok = (abs(a0_val-1.69e-10) < 0.13e-10) and (abs(sig_val-0.045) < 0.022)
print('  gate: %s (|d a0|=%.2f sigma_pub, |d sig|=%.3f dex)'
      % ('PASS' if ok else 'FAIL', abs(a0_val-1.69e-10)/0.13e-10, abs(sig_val-0.045)))
assert ok, 'VALIDATION FAILED -- extraction not faithful; no verdict'

# ----------------------------------------------------------------------------
# 4. SHAPE SEPARATION IN DEX (before any verdict)
# ----------------------------------------------------------------------------
print('\n' + '='*78)
print('SHAPE SEPARATION across their range log g_bar in [%.2f, %.2f]' % (x.min(), x.max()))
gg = np.linspace(x.min(), x.max(), 200)
d_fixed = F_framework(gg, A0_FRAMEWORK) - F_mls(gg, A0_MLS)
print('  (a) fixed canonical a0 (9.36e-11 vs 1.2e-10):')
print('      Delta log g_obs: min %+.3f, max %+.3f dex  (offset+shape)' %
      (d_fixed.min(), d_fixed.max()))

# ----------------------------------------------------------------------------
# 5. THE FOUR FITS + PROFILE LIKELIHOODS
# ----------------------------------------------------------------------------
print('\n' + '='*78)
print('FITS (MNR likelihood, n=%d; BIC = -2lnL + k ln n)' % n)
rows = {}
# fixed-a0 fits (k=3)
for name, model, a0v in (('framework @ 9.36e-11', 'framework', A0_FRAMEWORK),
                         ('framework @ 1.13e-10 (fork)', 'framework', A0_FORK_RISING),
                         ('MLS       @ 1.20e-10', 'mls', A0_MLS),
                         ('MLS       @ 1.69e-10 (their fit)', 'mls', A0_PAPER)):
    r = fit(model, a0=a0v)
    rows[name] = dict(m2l=r.fun, k=3, sig=r.x[0])
# free-a0 fits (k=4): profile over log a0 for robustness + CI + canonical placement
prof = {}
la_grid = np.linspace(-10.6, -9.3, 53)
for model in ('framework', 'mls'):
    m2l = np.array([fit(model, a0=10.**la).fun for la in la_grid])
    prof[model] = m2l
    i = np.argmin(m2l)
    # parabolic refine around minimum
    lo, hi = max(i-2, 0), min(i+3, len(la_grid))
    cc = np.polyfit(la_grid[lo:hi], m2l[lo:hi], 2)
    la_best = -cc[1]/(2*cc[0])
    r = fit(model, a0=None, la0_start=la_best)
    la_best, m2l_best = r.x[0], r.fun
    # 1-sigma from Delta(-2lnL)=1 on the profile
    dd = m2l - m2l_best
    left = la_grid[(la_grid < la_best) & (dd > 1)]
    right = la_grid[(la_grid > la_best) & (dd > 1)]
    e_lo = 10.**la_best - 10.**(np.interp(1., dd[(la_grid < la_best)][::-1],
                                          la_grid[(la_grid < la_best)][::-1]) if len(left) else la_grid[0])
    e_hi = 10.**(np.interp(1., dd[la_grid > la_best], la_grid[la_grid > la_best]) if len(right) else la_grid[-1]) - 10.**la_best
    rows['%s a0 FREE' % model] = dict(m2l=m2l_best, k=4, sig=r.x[1],
                                      a0=10.**la_best, e_lo=e_lo, e_hi=e_hi)

    def sig_at(a0v):
        d = fit(model, a0=a0v).fun - m2l_best
        return np.sqrt(max(d, 0.)), d
    rows['%s a0 FREE' % model]['placements'] = {
        '9.36e-11': sig_at(A0_FRAMEWORK), '1.13e-10': sig_at(A0_FORK_RISING),
        '1.20e-10': sig_at(A0_MLS)}

m2l_ref = rows['framework a0 FREE']['m2l']
print('\n%-36s %10s %8s %8s %10s' % ('model', '-2lnL', 'k', 'BIC', 'sigma_int'))
for name, d in rows.items():
    bic = d['m2l'] + d['k']*np.log(n)
    d['bic'] = bic
    extra = ''
    if 'a0' in d:
        extra = '  a0=(%.2f -%.2f +%.2f)e-10' % (d['a0']*1e10, d['e_lo']*1e10, d['e_hi']*1e10)
    print('%-36s %10.2f %8d %8.2f %9.3f%s' % (name, d['m2l'], d['k'], bic, d['sig'], extra))

# ----------------------------------------------------------------------------
# 6. HEAD-TO-HEAD NUMBERS
# ----------------------------------------------------------------------------
print('\n' + '='*78)
print('HEAD-TO-HEAD')
fw_free, ml_free = rows['framework a0 FREE'], rows['mls a0 FREE']
fw_fix, ml_fix = rows['framework @ 9.36e-11'], rows['MLS       @ 1.20e-10']

dbic_shape_free = fw_free['bic'] - ml_free['bic']
print('A. SHAPE, a0 free both (k=4 each, BIC diff = chi2 diff):')
print('   -2lnL: framework %.2f vs MLS %.2f -> Delta = %+.2f (framework %s)'
      % (fw_free['m2l'], ml_free['m2l'], fw_free['m2l']-ml_free['m2l'],
         'better' if fw_free['m2l'] < ml_free['m2l'] else 'worse'))
print('   ln Bayes factor (BIC approx) framework:MLS = %+.2f' % (-dbic_shape_free/2.))

# residual shape separation at the two best-fit a0's
d_free = F_framework(gg, fw_free['a0']) - F_mls(gg, ml_free['a0'])
d_free_c = d_free - d_free.mean()
print('   residual shape separation at best-fit a0s: full range %+.3f..%+.3f dex,'
      % (d_free.min(), d_free.max()))
print('   mean-removed amplitude %.3f dex rms (vs median sigma_y %.3f, sigma_int %.3f)'
      % (d_free_c.std(), np.median(sy), val.x[1]))

dbic_fixed = (fw_fix['m2l']+3*np.log(n)) - (ml_fix['m2l']+3*np.log(n))
print('B. CANONICAL FIXED a0 (framework@9.36e-11 vs MLS@1.2e-10, k=3 each):')
print('   -2lnL: %.2f vs %.2f -> Delta = %+.2f; ln B = %+.2f  (%s favored)'
      % (fw_fix['m2l'], ml_fix['m2l'], fw_fix['m2l']-ml_fix['m2l'], -dbic_fixed/2.,
         'framework' if dbic_fixed < 0 else 'MLS'))

print('C. WHERE DOES 9.36e-11 SIT (framework nu, their resolved-M/L footing)?')
for tag, (nsig, dchi) in fw_free['placements'].items():
    print('   a0 = %s: Delta chi2 = %6.2f  -> %5.2f sigma' % (tag, dchi, nsig))
print('   [MLS-side reference] 1.20e-10 on MLS profile: Delta chi2 = %.2f -> %.2f sigma'
      % (ml_free['placements']['1.20e-10'][1], ml_free['placements']['1.20e-10'][0]))

# transition-region focus: per-point -2lnL contribution split at log gbar = -11
print('D. TRANSITION-REGION FOCUS (per-point contributions, best-fit free-a0 models):')
def perpoint_m2l(model, pars):
    sig, mug, wg = pars[1], pars[2], pars[3]
    a0v = 10.**pars[0]
    F = FUN[model]
    s2 = sx**2 + wg**2
    m_i = (x*wg**2 + mug*sx**2)/s2
    s_i = np.sqrt(sx**2*wg**2/s2)
    lnpref = -0.5*np.log(2*np.pi*s2) - 0.5*(x-mug)**2/s2
    st2 = sy**2 + sig**2
    xt = m_i[:, None] + np.sqrt(2.)*s_i[:, None]*GH_T[None, :]
    fy = F(xt, a0v)
    ln_g = -0.5*np.log(2*np.pi*st2)[:, None] - 0.5*(y[:, None]-fy)**2/st2[:, None]
    mx = ln_g.max(axis=1)
    lnint = mx + np.log(np.sum(GH_W[None, :]*np.exp(ln_g-mx[:, None]), axis=1)/np.sqrt(np.pi))
    return -2.*(lnpref + lnint)
best_fw = fit('framework', a0=None, la0_start=np.log10(fw_free['a0']))
best_ml = fit('mls', a0=None, la0_start=np.log10(ml_free['a0']))
pp_fw = perpoint_m2l('framework', best_fw.x)
pp_ml = perpoint_m2l('mls', best_ml.x)
hi = x > -11.0
print('   log g_bar > -11 (transition, %d pts): Delta(-2lnL) fw-MLS = %+.2f' %
      (hi.sum(), pp_fw[hi].sum()-pp_ml[hi].sum()))
print('   log g_bar < -11 (deep,       %d pts): Delta(-2lnL) fw-MLS = %+.2f' %
      ((~hi).sum(), pp_fw[~hi].sum()-pp_ml[~hi].sum()))

# save extracted data for the repo
out = np.column_stack([x, y, sx, sy])
hdr = ('MIGHTEE-HI RAR (arXiv:2504.20857) fiducial varying-M/L sample, extracted from\n'
       'vector PDF RAR_best_fit_residuals_with_postpredictive.pdf (arXiv source tarball).\n'
       'Validation: MNR refit with their nu reproduces published a0=(1.69+/-0.13)e-10.\n'
       'columns: log10_gbar[m/s2]  log10_gobs[m/s2]  sigma_x[dex]  sigma_y[dex]')
np.savetxt('mightee_rar_extracted.csv', out, header=hdr, fmt='%.4f', delimiter=',')
print('\nsaved: mightee_rar_extracted.csv (%d points)' % n)
print('EXIT 0')
