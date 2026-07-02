#!/usr/bin/env python3
"""
LANE B3 (part 2) -- M/L-FORK ROBUSTNESS of the nu-shape test + a0 placement
=============================================================================
Same MIGHTEE-HI paper (arXiv:2504.20857). Their Figure 'RAR_comp.pdf' shows the
SAME 80 RAR points under three mass-to-light footings:
  panel 1: radially varying Upsilon_K (fiducial; published MLS a0=1.69+/-0.13e-10)
  panel 2: fixed Upsilon_K = 0.6      (published MLS a0=1.08+/-0.09e-10)
  panel 3: radial-average Upsilon_K   (published MLS a0=1.47+/-0.13e-10)
Extract all three, validate each against the published fits, then:
  - shape head-to-head (framework nu vs MLS nu, a0 free) per fork
  - placement of a0 = 9.36e-11 (canonical) / 1.13e-10 (fork) / 1.2e-10 (Milgrom)
    on the framework-nu profile per fork
GATE 0: panel-1 points must reproduce the independently-validated extraction
from the main figure (mightee_rar_extracted.csv) point-by-point.
"""
import sys
import numpy as np
import fitz
from scipy.optimize import minimize

A0_FRAMEWORK, A0_FORK, A0_MLS = 9.36e-11, 1.13e-10, 1.2e-10
PUB = {1: (1.69e-10, 0.13e-10, 0.045), 2: (1.08e-10, 0.09e-10, 0.060),
       3: (1.47e-10, 0.13e-10, 0.090)}
NAME = {1: 'radially varying Y_K (fiducial)', 2: 'fixed Y_K = 0.6',
        3: 'radial-average Y_K'}

doc = fitz.open('src/Figures/RAR_comp.pdf')
page = doc[0]
dr = page.get_drawings()

# ---- ticks
xt, yt = [], []
for d in dr:
    if d['type'] == 'fs':                      # tick marks are 'fs'; error bars are 's'
        r = d['rect']
        if abs(r.width) < 0.05 and 3 < r.height < 7:
            xt.append(((r.x0+r.x1)/2, r.y0))
        if abs(r.height) < 0.05 and 3 < r.width < 7:
            yt.append((r.x0, (r.y0+r.y1)/2))
xt.sort(); yt.sort()
assert len(xt) == 18, 'x ticks'
panels = {1: [t[0] for t in xt[:6]], 2: [t[0] for t in xt[6:12]], 3: [t[0] for t in xt[12:]]}
vx = np.arange(-12.5, -9.9, 0.5)
XCAL = {p: np.polyfit(panels[p], vx, 1) for p in (1, 2, 3)}
# y ticks: group by x0 (three panels), 9 each, values -11.50..-9.50 top->bottom
yt_x0 = sorted(set(round(t[0]) for t in yt))
assert len(yt) == 27, 'y ticks'
groups = {}
for x0, yy in yt:
    key = min((1, 2, 3), key=lambda p: abs(panels[p][0]-x0-14))  # nearest panel left edge
    groups.setdefault(key, []).append(yy)
YCAL = {}
vy = np.arange(-9.50, -11.51, -0.25)   # pdf y increases downward
for p in (1, 2, 3):
    ys = np.array(sorted(groups[p]))
    assert len(ys) == 9, 'panel %d y ticks: %d' % (p, len(ys))
    YCAL[p] = np.polyfit(ys, vy, 1)

# ---- markers + error bars
mk = []
for d in dr:
    if d['type'] != 'fs': continue
    r = d['rect']
    if abs(r.width-10.0) < 0.5 and abs(r.height-10.0) < 0.5:
        mk.append((r.x0+r.width/2, r.y0+r.height/2))
mk = np.array(mk)
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

def match(bars, pts, tol=1.2):
    out = np.full(len(pts), np.nan)
    for bx, by, ln in bars:
        dd = np.hypot(pts[:,0]-bx, pts[:,1]-by)
        i = np.argmin(dd)
        if dd[i] < tol: out[i] = ln
    return out

DATA = {}
# panel ownership bounded by the panels' left spines (y-tick x0 positions)
for p, (xlo, xhi) in {1: (78.0, 412.6), 2: (412.6, 746.3), 3: (746.3, 1080.)}.items():
    sel = (mk[:,0] > xlo) & (mk[:,0] < xhi)
    pts = mk[sel]
    assert sel.sum() == 80, 'panel %d markers: %d' % (p, sel.sum())
    hb = H[(H[:,0] > xlo) & (H[:,0] < xhi) & (H[:,1] < 300)]
    vb = V[(V[:,0] > xlo) & (V[:,0] < xhi) & (V[:,1] < 300)]
    ex, ey = match(hb, pts), match(vb, pts)
    Axp, Bxp = XCAL[p]; Ayp, Byp = YCAL[p]
    x = Axp*pts[:,0] + Bxp
    y = Ayp*pts[:,1] + Byp
    sx = np.abs(Axp)*ex/2.; sy = np.abs(Ayp)*ey/2.
    nb = np.isfinite(sx) & np.isfinite(sy)
    # a few bars can hide fully under 10pt markers; keep points, fill median err
    sx[~np.isfinite(sx)] = np.nanmedian(sx); sy[~np.isfinite(sy)] = np.nanmedian(sy)
    DATA[p] = (x, y, sx, sy)
    print('panel %d: 80 pts, bars matched %d/80, med sx %.3f sy %.3f, x[%.2f,%.2f]'
          % (p, nb.sum(), np.nanmedian(sx), np.nanmedian(sy), x.min(), x.max()))
    np.savetxt('mightee_rar_fork%d.csv' % p, np.column_stack([x, y, sx, sy]),
               header='MIGHTEE-HI RAR (2504.20857) fork: %s; extracted from RAR_comp.pdf panel %d\n'
                      'unmatched error bars (hidden under markers) filled with panel median\n'
                      'columns: log10_gbar  log10_gobs  sigma_x[dex]  sigma_y[dex]' % (NAME[p], p),
               fmt='%.4f', delimiter=',')

# ---- GATE 0: panel 1 == main-figure extraction
ref = np.loadtxt('mightee_rar_extracted.csv', delimiter=',')
x1, y1 = DATA[1][0], DATA[1][1]
o1 = np.lexsort((y1, x1)); oref = np.lexsort((ref[:,1], ref[:,0]))
dxy = np.hypot(x1[o1]-ref[oref,0], y1[o1]-ref[oref,1])
print('\nGATE 0 (panel1 vs validated main-figure extraction): max |d| = %.4f dex'
      % dxy.max())
assert dxy.max() < 0.01, 'panel-1 extraction mismatch'

# ---- MNR likelihood (same machinery as part 1)
GH_T, GH_W = np.polynomial.hermite.hermgauss(48)
def make_neg2lnL(x, y, sx, sy):
    def F(model, logg, a0):
        g = 10.**logg
        if model == 'framework': return 0.5*np.log10(g*g + g*a0)
        return logg - np.log10(1. - np.exp(-np.sqrt(g/a0)))
    def neg2lnL(theta, model, a0=None):
        if a0 is None: la0, sig, mug, wg = theta; a0v = 10.**la0
        else: sig, mug, wg = theta; a0v = a0
        if sig < 0 or wg <= 1e-4: return 1e10
        s2 = sx**2 + wg**2
        m_i = (x*wg**2 + mug*sx**2)/s2
        s_i = np.sqrt(sx**2*wg**2/s2)
        lnpref = -0.5*np.log(2*np.pi*s2) - 0.5*(x-mug)**2/s2
        st2 = sy**2 + sig**2
        xt_ = m_i[:, None] + np.sqrt(2.)*s_i[:, None]*GH_T[None, :]
        fy = F(model, xt_, a0v)
        ln_g = -0.5*np.log(2*np.pi*st2)[:, None] - 0.5*(y[:, None]-fy)**2/st2[:, None]
        mx = ln_g.max(axis=1)
        lnint = mx + np.log(np.sum(GH_W[None, :]*np.exp(ln_g-mx[:, None]), axis=1)/np.sqrt(np.pi))
        return -2.*np.sum(lnpref + lnint)
    return neg2lnL

def fit(nll, model, a0=None, la0_start=-9.8):
    best = None
    for sig0 in (0.02, 0.08):
        for wg0 in (0.4, 0.6):
            s0 = [sig0, -11.3, wg0]
            if a0 is None: s0 = [la0_start] + s0
            r = minimize(nll, s0, args=(model, a0), method='Nelder-Mead',
                         options=dict(maxiter=6000, xatol=1e-6, fatol=1e-8))
            if best is None or r.fun < best.fun: best = r
    return best

print('\n%-34s %-10s %-22s %-30s %s' % ('fork', 'gate', 'MLS a0 (pub)', 'framework: a0 / dChi2@canon',
      'shape dChi2 fw-MLS'))
summary = []
for p in (1, 2, 3):
    x, y, sx, sy = DATA[p]
    nll = make_neg2lnL(x, y, sx, sy)
    a0p, ea0p, sigp = PUB[p]
    vml = fit(nll, 'mls', la0_start=np.log10(a0p))
    a0_ml = 10.**vml.x[0]
    gate = abs(a0_ml-a0p) < ea0p and abs(vml.x[1]-sigp) < 0.025
    vfw = fit(nll, 'framework', la0_start=np.log10(a0p*1.15))
    a0_fw = 10.**vfw.x[0]
    d936 = fit(nll, 'framework', a0=A0_FRAMEWORK).fun - vfw.fun
    d113 = fit(nll, 'framework', a0=A0_FORK).fun - vfw.fun
    d120_ml = fit(nll, 'mls', a0=A0_MLS).fun - vml.fun
    dshape = vfw.fun - vml.fun
    print('%-34s %-10s %.2fe-10 (%.2f+/-%.2f)   a0=%.2fe-10; 9.36e-11:%5.1f->%4.1fs, 1.13:%4.1fs   %+6.2f'
          % (NAME[p], 'PASS' if gate else 'FAIL', a0_ml*1e10, a0p*1e10, ea0p*1e10,
             a0_fw*1e10, d936, np.sqrt(max(d936, 0)), np.sqrt(max(d113, 0)), dshape))
    summary.append((p, gate, a0_ml, a0_fw, d936, d113, d120_ml, dshape, vml.x[1], vfw.x[1]))

print('\nDETAIL')
for p, gate, a0_ml, a0_fw, d936, d113, d120_ml, dshape, sig_ml, sig_fw in summary:
    print('fork %d (%s): gate=%s' % (p, NAME[p], 'PASS' if gate else 'FAIL'))
    print('   MLS  a0-free: a0=%.3fe-10, sig=%.3f | Milgrom 1.2e-10: dChi2=%.2f -> %.2f sigma'
          % (a0_ml*1e10, sig_ml, d120_ml, np.sqrt(max(d120_ml, 0))))
    print('   FW   a0-free: a0=%.3fe-10, sig=%.3f | 9.36e-11: dChi2=%6.2f -> %.2f sigma | 1.13e-10: %6.2f -> %.2f sigma'
          % (a0_fw*1e10, sig_fw, d936, np.sqrt(max(d936, 0)), d113, np.sqrt(max(d113, 0))))
    print('   SHAPE (a0 free, equal k): Delta(-2lnL) framework-MLS = %+.2f  (%s; ln B ~ %+.2f)'
          % (dshape, 'framework better' if dshape < 0 else 'MLS better', -dshape/2.))
print('\nEXIT 0')
