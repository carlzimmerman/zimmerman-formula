#!/usr/bin/env python3
"""
digitise_rotcur.py -- digitise the raster rotation-curve figure of Lelli et al. (2023)

Source figure : arXiv:2302.00030, Fig. "Rotation curves of zC-400569 (left) and zC-488879 (right)",
                file Rotcur.jpg (1984 x 982 px JPEG, 100 dpi; whole-pixel marker placement, i.e. the
                signature of a matplotlib/Agg raster).
                green squares = CO(2-1), blue circles = CO(3-2), cyan squares = CO(4-3),
                red stars = H-alpha; every point carries a vertical error bar with end caps.
Output        : lelli2023_rotcur_digitised.csv   (galaxy,line,radius_arcsec,vrot_kms,err_lo_kms,
                                                  err_hi_kms,pixel_x,pixel_y,notes)
                qa_overlay.png                   (digitised points drawn over the original, 2x)
                a QA summary printed to stdout.

Run (offline, deterministic, ~5 s):   python3 digitise_rotcur.py [--image PATH] [--outdir DIR]

Only the image pixels are used.  Nothing is downloaded and nothing physical beyond reading values off
a plot is computed (no accelerations, masses or force laws).

Method (details and evidence in README.md)
------------------------------------------
1. Calibration.  Frame (spine) lines and the 1-px tick marks of each panel are located; the tick
   labels (read visually: 0.0..1.0 and 0..350 | 0.0..1.0 and 0..400) are assigned to the tick pixels
   in order, and x(pixel) / y(pixel) are least-squares straight lines.  Residuals, a minimax fit and
   a label-centre cross-check are reported.
2. Everything in this raster sits on the integer pixel lattice (every tick, spine, error bar, cap
   and marker was blitted at a whole-pixel offset, so all markers of one type are pixel-identical up
   to JPEG noise).  Positions are therefore integers by construction and the information content of
   the figure is +-0.5 px per coordinate; a "sub-pixel centroid" cannot improve on that.  Sub-pixel
   centroids of the un-occluded markers are still measured and reported as a check of the lattice.
3. Error bars first.  For each colour class (red / blue / cyan / green; chroma scores that are robust
   to JPEG) vertical thin lines are found (long vertical runs, gaps tolerated where another marker
   sits on the bar, non-maximum suppression across the 1.4-px line profile).  The bar's end caps are
   the 1-row horizontal lines at its two ends (min(left,right) darkness statistic, so a neighbouring
   bar 4 px away cannot fake a cap).
4. Markers.  For every colour class a pixel template is built from the median of the un-occluded
   instances (iteratively registered; absolute centre fixed by the template's soft centroid).  Each
   marker is then located along its own bar by an integer-lattice template match whose cost is a
   truncated SSD evaluated only on pixels that do not belong to another colour class (this is how
   the markers that are partly hidden behind another marker are recovered from their visible edges).
5. Conversion: value = (pixel - a) / b, err_hi = v(cap_top) - v(marker), err_lo = v(marker) - v(cap_bottom).
6. Legend boxes (found as long horizontal frame lines inside each panel) are excluded.
7. The whole localisation is repeated under alternative mask / cost settings (robustness check).

Pixel coordinates in the CSV are (column, row) array indices of the original image, i.e. the origin
is the CENTRE of the top-left pixel and y increases downward.
"""

import argparse
import contextlib
import csv
import hashlib
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IMAGE = '/Users/carlzimmerman/new_physics/_external_data/arxiv_src/2302.00030/Rotcur.jpg'
CSV_NAME = 'lelli2023_rotcur_digitised.csv'
OVERLAY_NAME = 'qa_overlay.png'

# ----------------------------------------------------------------------------- configuration
# Tick-label values were read visually from the figure.  Left panel: x 0.0-1.0, y 0-350.
# Right panel: x 0.0-1.0 (axis ends at 1.1, unlabelled), y 0-400.
GALAXIES = [
    dict(name='zC-400569', panel=0,
         x_labels=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
         y_labels=[0, 50, 100, 150, 200, 250, 300, 350],
         xlim_right=None,
         lines=[('red', 'Halpha', 6), ('blue', 'CO(3-2)', 5), ('cyan', 'CO(4-3)', 4)]),
    dict(name='zC-488879', panel=1,
         x_labels=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
         y_labels=[0, 50, 100, 150, 200, 250, 300, 350, 400],
         xlim_right=1.1,
         lines=[('green', 'CO(2-1)', 5), ('blue', 'CO(3-2)', 5)]),
]
LINE_OF = {'red': 'Halpha', 'blue': 'CO(3-2)', 'cyan': 'CO(4-3)', 'green': 'CO(2-1)'}
SHAPE_OF = {'red': 'star', 'blue': 'circle', 'cyan': 'square', 'green': 'square'}
TAG_OF = {'red': 'H', 'blue': 'C32-', 'cyan': 'C43-', 'green': 'C21-'}
CLASSES = ['red', 'blue', 'cyan', 'green']
# <V_rot> +- uncertainty from the authors' 3D fits (Table 'tab:3Dfits' of the paper source, line 289 of
# ColdGasDiskCosmicNoon.tex; the +- follows Eq. 3 of Lelli et al. 2016a, it is NOT the scatter of the points).
# Used only for the comparison in the QA summary; nothing is measured from them.
PAPER_MEAN = {'zC-400569': (254.0, 41.0), 'zC-488879': (336.0, 29.0)}

RAD = 12                 # half-size of the marker window / template (px)
T_BAR = 40.0             # class score of a bar-centre pixel
BAR_GAP = 24             # rows of gap tolerated inside a bar (another marker may sit on it)
BAR_MIN_LEN = 60         # shortest accepted bar (px); legend glyph bars are ~36 px and are excluded anyway
T_FOREIGN = 20.0         # class score above which a pixel counts as "another colour"
FOREIGN_DILATE = 2       # px by which the foreign-colour mask is grown
TRUNC = 3 * 60.0 ** 2    # per-pixel squared-RGB-distance cap in the template cost
MIN_VALID = 0.25         # a candidate position needs this fraction of un-masked window pixels
FILL_FOREIGN = 60.0      # class score of another colour that counts as 'covering' a silhouette pixel
FILL_T = {'red': 150.0, 'blue': 150.0, 'cyan': 150.0, 'green': 90.0}   # class score of marker fill
S_REF = {'red': 250.0, 'blue': 250.0, 'cyan': 250.0, 'green': 128.0}   # nominal fill score
SIGMA_Q = 1.0 / np.sqrt(12.0)                                           # rms of a +-0.5 px rounding

# alternative settings for the robustness check (positions must not change)
ROBUSTNESS_VARIANTS = [
    dict(T_FOREIGN=30.0),
    dict(T_FOREIGN=45.0, FOREIGN_DILATE=1),
    dict(FOREIGN_DILATE=1),
    dict(FOREIGN_DILATE=3, MIN_VALID=0.20),
    dict(TRUNC=1e12),                       # no truncation of the per-pixel cost
    dict(TRUNC=1.5 * 60.0 ** 2),
    dict(MIN_VALID=0.35),
]

# settings OUTSIDE the validity range: over-masking leaves too few usable pixels around touching markers, a very low
# colour threshold flags JPEG chroma noise as 'another colour'.  Reported for information (they document the limits).
STRESS_VARIANTS = [
    dict(FOREIGN_DILATE=4, MIN_VALID=0.20),
    dict(T_FOREIGN=12.0),
]


@contextlib.contextmanager
def params(**kw):
    """Temporarily override module-level tuning constants (used by the robustness check)."""
    saved = {k: globals()[k] for k in kw}
    globals().update(kw)
    try:
        yield
    finally:
        globals().update(saved)


# ----------------------------------------------------------------------------- small helpers
def load_image(path):
    im = np.asarray(Image.open(path).convert('RGB'), dtype=np.float64)
    lum = 0.299 * im[..., 0] + 0.587 * im[..., 1] + 0.114 * im[..., 2]
    return im, lum


def class_scores(im):
    """Chroma scores, ~250 on the pure fill colour, ~0 on white/grey/black.  JPEG-robust."""
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    return {'red': r - np.maximum(g, b),
            'blue': b - np.maximum(r, g),
            'cyan': np.minimum(g, b) - r,
            'green': g - np.maximum(r, b)}


def longest_run(b):
    """Longest run of True in a 1-D bool array -> (length, start index)."""
    if not b.any():
        return 0, 0
    d = np.diff(np.concatenate(([0], b.astype(np.int8), [0])))
    st = np.nonzero(d == 1)[0]
    en = np.nonzero(d == -1)[0]
    ln = en - st
    k = int(np.argmax(ln))
    return int(ln[k]), int(st[k])


def runs_with_gap(mask, gap):
    """Index runs of True in a 1-D mask; runs separated by <= gap False entries are merged."""
    idx = np.nonzero(mask)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - p > gap + 1:
            out.append((int(s), int(p)))
            s = v
        p = v
    out.append((int(s), int(p)))
    return out


def centroid_1d(profile, i0, half=2):
    lo, hi = max(i0 - half, 0), min(i0 + half + 1, len(profile))
    w = np.clip(profile[lo:hi], 0.0, None)
    return float((np.arange(lo, hi) * w).sum() / w.sum())


def win(cx, cy, r=None):
    r = RAD if r is None else r
    return (slice(cy - r, cy + r + 1), slice(cx - r, cx + r + 1))


# ----------------------------------------------------------------------------- frames, ticks, legends
def find_frames(lum):
    """Locate the two panel frames (spine lines) and their sub-pixel centres."""
    H, _ = lum.shape
    dark = lum < 100.0
    cols = np.nonzero(dark.sum(axis=0) >= 0.8 * H)[0]
    xs = []
    for c in cols:                                   # merge directly adjacent columns of one line
        if xs and c - xs[-1][-1] <= 1:
            xs[-1].append(int(c))
        else:
            xs.append([int(c)])
    xs = [int(round(np.mean(g))) for g in xs]
    if len(xs) != 4:
        raise RuntimeError('expected 4 full-height spine lines, found %r' % (xs,))
    amt = 255.0 - lum
    panels = []
    for xa, xb in ((xs[0], xs[1]), (xs[2], xs[3])):
        rows = np.nonzero(dark[:, xa:xb + 1].sum(axis=1) >= 0.9 * (xb - xa))[0]
        ya, yb = int(rows.min()), int(rows.max())
        p = dict(x0=xa, x1=xb, y0=ya, y1=yb)
        px = np.median(amt[ya + 15:yb - 14, :], axis=0)
        py = np.median(amt[:, xa + 15:xb - 14], axis=1)
        p['x0c'], p['x1c'] = centroid_1d(px, xa), centroid_1d(px, xb)
        p['y0c'], p['y1c'] = centroid_1d(py, ya), centroid_1d(py, yb)
        panels.append(p)
    return panels


def find_ticks(lum, p, axis, side):
    """Sub-pixel centres of the 1-px inward tick marks along one side of a panel (corners excluded)."""
    amt = 255.0 - lum
    if axis == 'x':
        y = p['y1'] if side == 'bottom' else p['y0']
        sgn = -1 if side == 'bottom' else +1
        prof = amt[[y + sgn * d for d in range(3, 9)], :].mean(axis=0)
        lo, hi = p['x0'] + 4, p['x1'] - 3
    else:
        x = p['x0'] if side == 'left' else p['x1']
        sgn = +1 if side == 'left' else -1
        prof = amt[:, [x + sgn * d for d in range(3, 9)]].mean(axis=1)
        lo, hi = p['y0'] + 4, p['y1'] - 3
    out, i = [], lo
    while i <= hi:
        if prof[i] > 50.0:
            j = i
            while j <= hi and prof[j] > 50.0:
                j += 1
            w = prof[i:j]
            out.append(float((np.arange(i, j) * w).sum() / w.sum()))
            i = j
        else:
            i += 1
    return out


def find_legend(lum, p):
    """Legend box = the two long horizontal frame lines inside the panel (rows) + their extent."""
    dark = lum < 100.0
    rows = []
    for y in range(p['y0'] + 4, p['y1'] - 3):
        ln, s = longest_run(dark[y, p['x0'] + 4:p['x1'] - 3])
        if ln >= 150:
            rows.append((y, ln, p['x0'] + 4 + s))
    if len(rows) != 2:
        raise RuntimeError('expected 2 legend frame rows, found %r' % (rows,))
    return dict(x0=rows[0][2], x1=rows[0][2] + rows[0][1] - 1, y0=rows[0][0], y1=rows[1][0])


def fit_axis(pix, val):
    """pix = a + b*val.  Least squares (adopted) + minimax (feasibility of the rounding model)."""
    pix, val = np.asarray(pix, float), np.asarray(val, float)
    n = len(val)
    A = np.column_stack([np.ones(n), val])
    coef = np.linalg.lstsq(A, pix, rcond=None)[0]
    resid = pix - A @ coef
    # minimax: min t  s.t. |pix - a - b val| <= t.  A rounding-to-nearest-pixel model needs t <= 0.5.
    Aub, bub = [], []
    for v, i in zip(val, pix):
        Aub.append([-1.0, -v, -1.0]); bub.append(-i)
        Aub.append([1.0, v, -1.0]); bub.append(i)
    sol = linprog([0, 0, 1], A_ub=Aub, b_ub=bub, bounds=[(None, None), (None, None), (0, None)])
    vbar, Svv = val.mean(), ((val - val.mean()) ** 2).sum()
    return dict(a=float(coef[0]), b=float(coef[1]), n=n, resid=resid,
                rms=float(np.sqrt((resid ** 2).mean())), maxabs=float(np.abs(resid).max()),
                t_star=float(sol.x[2]), a_mm=float(sol.x[0]), b_mm=float(sol.x[1]),
                vbar=float(vbar), Svv=float(Svv), pix=pix, val=val)


def axis_value(fit, pix):
    return (np.asarray(pix, float) - fit['a']) / fit['b']


def axis_sigma_pix(fit, v):
    """1-sigma pixel uncertainty of the fitted line at value v (uniform rounding noise on the ticks)."""
    return SIGMA_Q * np.sqrt(1.0 / fit['n'] + (np.asarray(v) - fit['vbar']) ** 2 / fit['Svv'])


def _clusters(has, gap):
    idx = np.nonzero(has)[0]
    cl, s, q = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - q > gap:
            cl.append((int(s), int(q)))
            s = v
        q = v
    cl.append((int(s), int(q)))
    return cl


def label_centre_check(lum, p, x_ticks, y_ticks):
    """Cross-check: glyph clusters of the tick labels sit on the detected ticks (x: centred; y: constant offset)."""
    dark = lum < 140.0
    out = {}
    off = max(p['x0'] - 35, 0)                       # x labels: rows just below the bottom spine
    cl = _clusters(dark[p['y1'] + 6:p['y1'] + 32, off:p['x1'] + 36].any(axis=0), 10)
    centres = [0.5 * (a + b) + off for a, b in cl]
    out['x_labels_found'] = len(centres)
    out['x_label_dev_max'] = float(max(min(abs(c - t) for t in x_ticks) for c in centres))
    # y labels: columns just left of the left spine; the bottom "0" label is skipped (it touches the "0.0" x label)
    cl = _clusters(dark[p['y0'] - 15:p['y1'] - 20, p['x0'] - 60:p['x0'] - 6].any(axis=1), 6)
    centres = [0.5 * (a + b) + p['y0'] - 15 for a, b in cl]
    d = [c - min(y_ticks, key=lambda u: abs(u - c)) for c in centres]
    out['y_labels_found'] = len(centres)
    out['y_label_offset_mean'] = float(np.mean(d))
    out['y_label_offset_spread'] = float(np.max(d) - np.min(d))
    return out


# ----------------------------------------------------------------------------- bars
def find_bars(sc, lum, p, leg, cls):
    """Vertical thin lines of colour class `cls` inside panel p (legend excluded) -> (x, top, bottom)."""
    y_lo, y_hi = p['y0'] + 4, p['y1'] - 3
    rows = np.arange(y_lo, y_hi)
    cand = []
    for x in range(p['x0'] + 4, p['x1'] - 3):
        m = sc[cls][y_lo:y_hi, x] > T_BAR
        if leg['x0'] - 2 <= x <= leg['x1'] + 2:
            m = m & ~((rows >= leg['y0'] - 2) & (rows <= leg['y1'] + 2))
        for a, b in runs_with_gap(m, BAR_GAP):
            if b - a + 1 >= BAR_MIN_LEN:
                r0, r1 = int(rows[a]), int(rows[b])
                cand.append((x, r0, r1, float((255.0 - lum[r0:r1 + 1, x]).mean())))
    cand.sort()
    keep, used = [], set()
    for i, c in enumerate(cand):                  # non-maximum suppression across the 1.4-px profile
        if i in used:
            continue
        grp = [c]
        used.add(i)
        for j in range(i + 1, len(cand)):
            if j not in used and abs(cand[j][0] - c[0]) <= 2 and \
                    min(cand[j][2], c[2]) - max(cand[j][1], c[1]) > 20:
                grp.append(cand[j])
                used.add(j)
        keep.append(max(grp, key=lambda t: t[3]))
    return [(k[0], k[1], k[2]) for k in keep]


def cap_row(dark, xb, r_end):
    """Row of the 1-px horizontal cap nearest to a bar end.  Statistic = min(left, right) darkness
    over the three columns 2..4 px either side of the bar, so a neighbouring bar cannot fake a cap."""
    best, second, brow = -1.0, -1.0, None
    for r in range(r_end - 3, r_end + 4):
        hl = sum(dark[r, xb - d] for d in (2, 3, 4))
        hr = sum(dark[r, xb + d] for d in (2, 3, 4))
        h = min(hl, hr)
        if h > best:
            second, best, brow = best, h, r
        elif h > second:
            second = h
    return brow, float(best), float(second)


# ----------------------------------------------------------------------------- templates and matching
def foreign_masks(sc, classes):
    """Per colour class: pixels showing ANY OTHER colour class of the same panel, grown by FOREIGN_DILATE px.
    (Only the classes that exist in the panel are used: blue/green blends otherwise fake a 'cyan'.)"""
    cm = {c: sc[c] > T_FOREIGN for c in classes}
    out = {}
    for c in classes:
        m = np.zeros(sc[c].shape, bool)
        for c2 in classes:
            if c2 != c:
                m |= cm[c2]
        out[c] = ndi.binary_dilation(m, structure=np.ones((3, 3)), iterations=FOREIGN_DILATE)
    return out


def blob_seeds(sc, cls, allowed):
    m = (sc[cls] > FILL_T[cls]) & allowed
    mo = ndi.binary_opening(m, structure=np.ones((5, 5)))
    lab, n = ndi.label(mo)
    seeds = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        seeds.append((int(np.floor(xs.mean() + 0.5)), int(np.floor(ys.mean() + 0.5))))
    return seeds


def register(im, centres, iters=3, search=2):
    """Iteratively align instances to their median (integer shifts) -> centres, template, stable?"""
    centres = [tuple(c) for c in centres]
    stable = False
    for _ in range(iters):
        tm = np.median(np.stack([im[win(*c)] for c in centres]), axis=0)
        new = []
        for c in centres:
            best = None
            for dx in range(-search, search + 1):
                for dy in range(-search, search + 1):
                    q = (c[0] + dx, c[1] + dy)
                    s = ((im[win(*q)] - tm) ** 2).sum(axis=2).mean()
                    if best is None or s < best[0]:
                        best = (s, q)
            new.append(best[1])
        stable = (new == centres)
        centres = new
    tm = np.median(np.stack([im[win(*c)] for c in centres]), axis=0)
    return centres, tm, stable


def template_weights(tm, cls):
    r, g, b = tm[..., 0], tm[..., 1], tm[..., 2]
    s = {'red': r - np.maximum(g, b), 'blue': b - np.maximum(r, g),
         'cyan': np.minimum(g, b) - r, 'green': g - np.maximum(r, b)}[cls]
    return np.clip(s / S_REF[cls], 0.0, 1.0)


def weighted_centroid(w):
    yy, xx = np.mgrid[-RAD:RAD + 1, -RAD:RAD + 1]
    return float((w * xx).sum() / w.sum()), float((w * yy).sum() / w.sum())


def panel_index(x, panels):
    for i, p in enumerate(panels):
        if p['x0'] <= x <= p['x1']:
            return i
    raise ValueError(x)


def build_template(im, sc, FOR_P, panels, cls, allowed):
    seeds = [s for s in blob_seeds(sc, cls, allowed) if cls in FOR_P[panel_index(s[0], panels)]]
    clean = [s for s in seeds if FOR_P[panel_index(s[0], panels)][cls][win(*s)].sum() == 0]
    if len(clean) < 2:
        raise RuntimeError('fewer than 2 clean instances for class %s' % cls)
    centres, tm, stable = register(im, clean)
    dx, dy = weighted_centroid(template_weights(tm, cls))
    shift = (int(np.round(dx)), int(np.round(dy)))        # fix the absolute centre by symmetry
    if shift != (0, 0):
        centres = [(c[0] + shift[0], c[1] + shift[1]) for c in centres]
        tm = np.median(np.stack([im[win(*c)] for c in centres]), axis=0)
        dx, dy = weighted_centroid(template_weights(tm, cls))
    dev = [float(np.abs(im[win(*c)] - tm).mean()) for c in centres]
    lum_t = 0.299 * tm[..., 0] + 0.587 * tm[..., 1] + 0.114 * tm[..., 2]
    sil = (255.0 - lum_t) > 60.0                 # the marker's visible silhouette (fill + edge) ...
    sil[:, RAD - 1:RAD + 2] = False              # ... without the bar columns that run through it
    return dict(tm=tm, sil=sil, centres=centres, n_seed=len(seeds), n_clean=len(clean), stable=stable,
                centroid=(dx, dy), shift=shift, mean_abs_dev=dev, w=template_weights(tm, cls))


def match_along_bar(im, FOR, T, cls, xb, top, bot):
    """Integer-lattice template match along a bar.  Cost = truncated SSD on un-masked pixels."""
    tm = T['tm']
    cands = []
    for dx in (-1, 0, 1):
        x = xb + dx
        for y in range(top + RAD, bot - RAD + 1):
            w = win(x, y)
            valid = ~FOR[cls][w]
            n = int(valid.sum())
            if n < MIN_VALID * valid.size:
                continue
            d = np.minimum(((im[w] - tm) ** 2).sum(axis=2), TRUNC)
            cands.append(((d * valid).sum() / n, x, y, n))
    cands.sort()
    best = cands[0]
    far = [c for c in cands if abs(c[2] - best[2]) >= 3]
    near = [c[0] for c in cands if (c[1], c[2]) != (best[1], best[2]) and abs(c[1] - best[1]) <= 1
            and abs(c[2] - best[2]) <= 1]
    return dict(ssd=float(best[0]), x=int(best[1]), y=int(best[2]), n_valid=int(best[3]),
                ssd_far=float(far[0][0]) if far else float('nan'),
                ssd_near=float(min(near)) if near else float('nan'))


def locate_markers(im, lum, sc, panels, legends, allowed):
    """Foreign masks -> templates -> bars -> markers (everything that depends on the tuning constants)."""
    dark = 255.0 - lum
    FOR_P = [foreign_masks(sc, [c for c, _, _ in g['lines']]) for g in GALAXIES]   # per panel
    T = {cls: build_template(im, sc, FOR_P, panels, cls, allowed) for cls in CLASSES}
    markers = []
    for gi, (g, p, lg) in enumerate(zip(GALAXIES, panels, legends)):
        FOR = FOR_P[gi]
        pcls = [c for c, _, _ in g['lines']]
        for cls, line, nexp in g['lines']:
            for (xb, top, bot) in find_bars(sc, lum, p, lg, cls):
                mt = match_along_bar(im, FOR, T[cls], cls, xb, top, bot)
                r_top, h_t, h2_t = cap_row(dark, xb, top)
                r_bot, h_b, h2_b = cap_row(dark, xb, bot)
                w = win(mt['x'], mt['y'])
                clean = FOR[cls][w].sum() == 0
                # fraction of the marker's own silhouette (fill + edge, bar columns excluded) showing another colour
                sil = T[cls]['sil']
                covered = {c2: float(((sc[c2][w] > FILL_FOREIGN) & sil).sum() / sil.sum())
                           for c2 in pcls if c2 != cls}
                # sub-pixel centroid of the un-occluded marker relative to the template centroid
                sub = None
                if clean:
                    cx, cy = weighted_centroid(np.clip(sc[cls][w] / S_REF[cls], 0.0, 1.0))
                    sub = (cx - T[cls]['centroid'][0], cy - T[cls]['centroid'][1])
                # template-free cross-check: centroid of the opened own-colour fill blob nearest the window centre
                blob = None
                lab, nlab = ndi.label(ndi.binary_opening(sc[cls][w] > FILL_T[cls], structure=np.ones((5, 5))))
                if nlab:
                    cen = []
                    for i in range(1, nlab + 1):
                        ys, xs = np.nonzero(lab == i)
                        cen.append((xs.mean() - RAD, ys.mean() - RAD))
                    blob = min(cen, key=lambda c: c[0] ** 2 + c[1] ** 2)
                # other markers / bars of the same panel inside the window
                near = []
                for c2 in pcls:
                    if c2 == cls:
                        continue
                    if int((sc[c2][w] > FILL_T[c2]).sum()) >= 15:
                        near.append((c2, 'marker'))
                    elif int((sc[c2][w] > T_FOREIGN).sum()) > 0:
                        near.append((c2, 'error bar'))
                markers.append(dict(gi=gi, cls=cls, line=line, bar_x=xb, x=mt['x'], y=mt['y'], match=mt,
                                    cap_top=r_top, cap_bot=r_bot, cap_q=(h_t / max(h2_t, 1e-9), h_b / max(h2_b, 1e-9)),
                                    clean=bool(clean), hidden=sum(covered.values()), covered=covered,
                                    sub=sub, near=near, blob=blob))
    return markers, T, FOR_P


# ----------------------------------------------------------------------------- overlay
def draw_overlay(im, markers, cals, panels, legends, outpath, font):
    S = 2
    H, W, _ = im.shape
    big = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).resize((W * S, H * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    MAG, ORG, GRN = (255, 0, 255), (255, 120, 0), (0, 170, 0)

    def hline(x0, x1, y, col):               # 1 source-pixel thick, centred on source pixel row y
        d.rectangle([S * x0, S * y, S * x1 + S - 1, S * y + S - 1], fill=col)

    for m in markers:
        x, y = m['x'], m['y']
        # horizontal arms outside the marker body (so the body and its original centre stay visible) + a small
        # square on the digitised centre; the bar column through the square shows the x position
        hline(x - 20, x - 11, y, MAG); hline(x + 11, x + 20, y, MAG)
        d.rectangle([S * (x - 1), S * (y - 1), S * (x + 1) + S - 1, S * (y + 1) + S - 1], outline=MAG, width=2)
        # digitised cap rows, drawn outside the original 9-px cap (original spans x-4..x+4)
        for r in (m['cap_top'], m['cap_bot']):
            hline(x - 10, x - 6, r, ORG); hline(x + 6, x + 10, r, ORG)
        tw = d.textlength(m['tag'], font=font)
        if m['cls'] == 'blue':          # CO(3-2) tags to the left of the bar, all others to the right
            d.text((S * (x - 12) - tw, S * (m['cap_top'] - 8)), m['tag'], fill=(0, 0, 0), font=font)
        else:
            d.text((S * (x + 12), S * (m['cap_top'] - 8)), m['tag'], fill=(0, 0, 0), font=font)
    for p, cal in zip(panels, cals):
        for t in cal['x_ticks_used']:
            d.rectangle([S * int(t) - 2, S * (p['y1'] - 16) - 2, S * int(t) + 3, S * (p['y1'] - 16) + 3], fill=GRN)
        for t in cal['y_ticks_used']:
            d.rectangle([S * (p['x0'] + 16) - 2, S * int(t) - 2, S * (p['x0'] + 16) + 3, S * int(t) + 3], fill=GRN)
    for lg in legends:
        d.rectangle([S * (lg['x0'] - 4), S * (lg['y0'] - 4), S * (lg['x1'] + 4), S * (lg['y1'] + 4)],
                    outline=ORG, width=2)
        d.text((S * (lg['x0'] + 6), S * (lg['y0'] - 22)), 'legend: excluded', fill=ORG, font=font)
    key = ['QA overlay (2x): magenta square + arms = digitised point (centre / row); orange dashes = digitised',
           'error-bar ends; green squares = calibration ticks used; orange box = legend excluded; tag = CSV order.']
    for i, line in enumerate(key):
        d.text((S * 1170, S * 470 + i * 30), line, fill=(0, 0, 0), font=font)
    big.save(outpath, format='PNG', optimize=False, compress_level=6)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--image', default=DEFAULT_IMAGE)
    ap.add_argument('--outdir', default=HERE)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    im, lum = load_image(args.image)
    H, W = lum.shape
    sc = class_scores(im)

    def pr(s=''):
        print(s)

    pr('QA SUMMARY  (image %s, %dx%d px)' % (os.path.basename(args.image), W, H))
    pr('=' * 78)

    # ---------------------------------------------------------------- 1. frames, ticks, calibration
    panels = find_frames(lum)
    legends = [find_legend(lum, p) for p in panels]
    cals = []
    pr('1. CALIBRATION (pixel = a + b * value; pixel = array index, centre of top-left pixel = 0)')
    for g, p, lg in zip(GALAXIES, panels, legends):
        for k in ('x0c', 'x1c', 'y0c', 'y1c'):          # spines/ticks are 1-px snapped: check lattice
            assert abs(p[k] - round(p[k])) < 0.05, (k, p[k])
        sp = dict(x0=int(round(p['x0c'])), x1=int(round(p['x1c'])), y0=int(round(p['y0c'])), y1=int(round(p['y1c'])))
        tb = [int(round(t)) for t in find_ticks(lum, p, 'x', 'bottom')]
        tt = [int(round(t)) for t in find_ticks(lum, p, 'x', 'top')]
        tl = [int(round(t)) for t in find_ticks(lum, p, 'y', 'left')]
        tr = [int(round(t)) for t in find_ticks(lum, p, 'y', 'right')]
        mirror_ok = (tb == tt) and (tl == tr)
        # x: left spine = first label, then inner ticks (+ right spine if it is the last label)
        xpos = [sp['x0']] + tb
        if len(xpos) == len(g['x_labels']) - 1:
            xpos.append(sp['x1'])
        # y: bottom spine = 0, inner ticks bottom->top, top spine = last label
        ypos = [sp['y1']] + sorted(tl, reverse=True) + [sp['y0']]
        if len(xpos) != len(g['x_labels']) or len(ypos) != len(g['y_labels']):
            raise RuntimeError('tick/label count mismatch: x %d/%d, y %d/%d' %
                               (len(xpos), len(g['x_labels']), len(ypos), len(g['y_labels'])))
        fx = fit_axis(xpos, g['x_labels'])
        fy = fit_axis(ypos, g['y_labels'])
        chk = label_centre_check(lum, p, [float(v) for v in xpos], [float(v) for v in ypos])
        cals.append(dict(fx=fx, fy=fy, x_ticks_used=xpos, y_ticks_used=ypos, spines=sp, chk=chk, mirror_ok=mirror_ok))
        pr('   %s  panel frame x %d..%d, y %d..%d;  legend box x %d..%d, y %d..%d (excluded)' %
           (g['name'], sp['x0'], sp['x1'], sp['y0'], sp['y1'], lg['x0'], lg['x1'], lg['y0'], lg['y1']))
        pr('      x ticks used (px): %s  <->  %s' % (xpos, g['x_labels']))
        pr('      y ticks used (px): %s  <->  %s' % (ypos, g['y_labels']))
        pr('      x: a=%.3f  b=%.4f px/arcsec | resid rms %.3f px (%.5f arcsec), max %.3f px | minimax t*=%.3f' %
           (fx['a'], fx['b'], fx['rms'], fx['rms'] / fx['b'], fx['maxabs'], fx['t_star']))
        pr('      y: a=%.3f  b=%.4f px/(km/s) | resid rms %.3f px (%.3f km/s), max %.3f px (%.3f km/s) | minimax t*=%.3f' %
           (fy['a'], fy['b'], fy['rms'], fy['rms'] / abs(fy['b']), fy['maxabs'], fy['maxabs'] / abs(fy['b']), fy['t_star']))
        if g['xlim_right'] is not None:
            pr('      check: right spine (pixel %d) maps to x = %.4f arcsec (axis limit read as %.1f)' %
               (sp['x1'], axis_value(fx, sp['x1']), g['xlim_right']))
        mm = max(abs((fx['a'] + fx['b'] * v) - (fx['a_mm'] + fx['b_mm'] * v)) for v in (g['x_labels'][0], g['x_labels'][-1]))
        mmy = max(abs((fy['a'] + fy['b'] * v) - (fy['a_mm'] + fy['b_mm'] * v)) for v in (g['y_labels'][0], g['y_labels'][-1]))
        pr('      LS vs minimax calibration differ by <= %.3f px (x) and <= %.3f px (y) over the axis range' % (mm, mmy))
        pr('      mirrored top/right ticks identical to bottom/left ticks: %s' % mirror_ok)
        pr('      label cross-check: %d x-label glyph clusters (expect %d), max |centre - tick| = %.1f px; '
           '%d y-label clusters (expect %d, "0" skipped), label-minus-tick offset %.1f px (spread %.1f px)' %
           (chk['x_labels_found'], len(g['x_labels']), chk['x_label_dev_max'],
            chk['y_labels_found'], len(g['y_labels']) - 1, chk['y_label_offset_mean'], chk['y_label_offset_spread']))
    pr()

    # ---------------------------------------------------------------- 2. markers (templates, bars, matching)
    allowed = np.zeros((H, W), bool)               # panel interiors without the legend boxes
    for p, lg in zip(panels, legends):
        allowed[p['y0'] + 4:p['y1'] - 3, p['x0'] + 4:p['x1'] - 3] = True
        allowed[lg['y0'] - 3:lg['y1'] + 4, lg['x0'] - 3:lg['x1'] + 4] = False
    markers, T, FOR_P = locate_markers(im, lum, sc, panels, legends, allowed)

    pr('2. MARKER TEMPLATES (median of un-occluded instances, integer-lattice registration)')
    for cls in CLASSES:
        t = T[cls]
        pr('   %-5s %-6s seeds %2d, clean %2d, registration stable=%s, template soft-centroid offset (%+.3f,%+.3f) px, '
           'instance-vs-template mean |dev| %.2f-%.2f grey levels' %
           (cls, SHAPE_OF[cls], t['n_seed'], t['n_clean'], t['stable'], t['centroid'][0], t['centroid'][1],
            min(t['mean_abs_dev']), max(t['mean_abs_dev'])))
    pr()

    # ---------------------------------------------------------------- 3. conversion + table
    rows_out, counts = [], {}
    for gi, g in enumerate(GALAXIES):
        fx, fy = cals[gi]['fx'], cals[gi]['fy']
        for cls, line, nexp in g['lines']:
            pts = sorted([m for m in markers if m['gi'] == gi and m['cls'] == cls], key=lambda m: m['x'])
            counts[(g['name'], line)] = (len(pts), nexp)
            for k, m in enumerate(pts, 1):
                m['tag'] = '%s%d' % (TAG_OF[cls], k)
                m['radius'] = float(axis_value(fx, m['x']))
                m['v'] = float(axis_value(fy, m['y']))
                m['err_hi'] = float(axis_value(fy, m['cap_top'])) - m['v']
                m['err_lo'] = m['v'] - float(axis_value(fy, m['cap_bot']))
                # notes: only integer / coarse quantities, so the CSV is stable across JPEG decoders
                who_cov = ' + '.join(LINE_OF[c2] for c2, f in m['covered'].items() if f >= 0.01)
                pct = 5 * int(round(100.0 * m['hidden'] / 5.0))
                if m['clean']:
                    note = 'clean (no other colour within 12 px)'
                elif m['hidden'] >= 0.30:
                    note = ('PARTLY HIDDEN: about %d%% of the marker silhouette is covered by %s (marker or bar); '
                            'position from the visible edges by lattice template fit' % (pct, who_cov))
                elif m['hidden'] >= 0.03:
                    note = ('overlapped: about %d%% of the marker silhouette is covered by %s; lattice template fit '
                            'on the visible pixels' % (pct, who_cov))
                else:
                    note = 'complete (drawn on top or not overlapped); neighbour within 12 px: %s' % \
                           ' + '.join('%s %s' % (LINE_OF[c2], kind) for c2, kind in m['near'])
                m['notes'] = ('%s; caps rows %d/%d' % (note, m['cap_top'], m['cap_bot'])).replace(',', ' ')
                rows_out.append((g['name'], line, m))

    csv_path = os.path.join(args.outdir, CSV_NAME)
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['galaxy', 'line', 'radius_arcsec', 'vrot_kms', 'err_lo_kms', 'err_hi_kms',
                    'pixel_x', 'pixel_y', 'notes'])
        for gname, line, m in rows_out:
            w.writerow([gname, line, '%.4f' % m['radius'], '%.2f' % m['v'], '%.2f' % m['err_lo'],
                        '%.2f' % m['err_hi'], '%d' % m['x'], '%d' % m['y'], m['notes']])

    # ---------------------------------------------------------------- 4. QA numbers
    allm = [m for _, _, m in rows_out]
    pr('3. COUNTS (found / expected)')
    for (gname, line), (n, ne) in counts.items():
        pr('   %-10s %-8s %d / %d%s' % (gname, line, n, ne, '' if n == ne else '   <-- DIFFERS'))
    for gi, g in enumerate(GALAXIES):                 # stray detections in classes that should not occur in a panel
        have = {c for c, _, _ in g['lines']}
        for cls in CLASSES:
            if cls not in have:
                pr('   %-10s stray %-5s bars (class not in this panel): %d' %
                   (g['name'], cls, len(find_bars(sc, lum, panels[gi], legends[gi], cls))))
    pr()
    pr('4. MEAN OF THE DIGITISED V_rot OVER ALL POINTS OF EACH GALAXY')
    for g in GALAXIES:
        vs = np.array([m['v'] for gn, _, m in rows_out if gn == g['name']])
        pm, ps = PAPER_MEAN[g['name']]
        pr('   %-10s N=%2d  mean %.1f km/s (sample SD %.1f, s.e.m. %.1f)  | paper table <V_rot> = %.0f +- %.0f  '
           '-> difference %+.1f km/s (%.2f paper-sigma)' %
           (g['name'], len(vs), vs.mean(), vs.std(ddof=1), vs.std(ddof=1) / np.sqrt(len(vs)), pm, ps,
            vs.mean() - pm, (vs.mean() - pm) / ps))
    pr()
    pr('5. LATTICE / MATCH-QUALITY EVIDENCE')
    pr('   bar column == marker column for %d / %d markers' % (sum(m['bar_x'] == m['x'] for m in allm), len(allm)))
    subs = np.array([m['sub'] for m in allm if m['sub'] is not None])
    pr('   un-occluded markers (n=%d): measured soft-centroid offset from the integer lattice  '
       'x: mean %+.3f rms %.3f max %.3f px | y: mean %+.3f rms %.3f max %.3f px' %
       (len(subs), subs[:, 0].mean(), np.sqrt((subs[:, 0] ** 2).mean()), np.abs(subs[:, 0]).max(),
        subs[:, 1].mean(), np.sqrt((subs[:, 1] ** 2).mean()), np.abs(subs[:, 1]).max()))
    comp = [m for m in allm if m['hidden'] < 0.03 and m['blob'] is not None]
    pr('   template-free check, complete markers (n=%d): centroid of the opened own-colour fill blob vs the lattice position, '
       'max |offset| per class: %s px' %
       (len(comp), ', '.join('%s %.2f' % (c, max(max(abs(m['blob'][0]), abs(m['blob'][1])) for m in comp if m['cls'] == c))
                            for c in CLASSES)))
    pr('      (hard-threshold blob centroids are quantised / biased by up to ~0.5 px for the stars and the dark-green squares; '
       'a mis-placed match would show >= 1 px)')
    ratio_far = [m['match']['ssd_far'] / max(m['match']['ssd'], 1e-9) for m in allm]
    ratio_near = [m['match']['ssd_near'] / max(m['match']['ssd'], 1e-9) for m in allm]
    pr('   template-match sharpness: SSD(best distinct competitor)/SSD(best) >= %.0f ; SSD(+-1 px neighbour)/SSD(best) >= %.0f ; '
       'worst best-SSD %.0f (grey-level^2/px, truncated), smallest usable window fraction %.2f' %
       (min(ratio_far), min(ratio_near), max(m['match']['ssd'] for m in allm),
        min(m['match']['n_valid'] for m in allm) / (2 * RAD + 1) ** 2))
    pr('   cap peak / next-best row statistic: min over all %d caps = %.1f' %
       (2 * len(allm), min(min(m['cap_q']) for m in allm)))
    dm = np.array([0.5 * (m['cap_top'] + m['cap_bot']) - m['y'] for m in allm])
    n0 = int((np.abs(dm) < 1e-9).sum())
    pr('   error-bar symmetry: (cap-midpoint row - marker row): mean %+.2f +- %.2f px, SD %.2f px; %d of %d are exactly 0 and %d are +-0.5 px.' %
       (dm.mean(), dm.std(ddof=1) / np.sqrt(len(dm)), dm.std(ddof=1), n0, len(dm), int((np.abs(np.abs(dm) - 0.5) < 1e-9).sum())))
    pr('      Exactly symmetric bars + whole-pixel rounding of marker and both caps allow ONLY 0 (50%) or +-0.5 px (25% each), '
       'SD 0.353 px (Monte Carlo); +-1 px, which independent roundings would give in 17% of cases, is impossible.')
    for cls in CLASSES:
        dd = np.array([0.5 * (m['cap_top'] + m['cap_bot']) - m['y'] for m in allm if m['cls'] == cls])
        pr('      by class %-5s (%-6s) n=%2d: mean %+.2f px, s.e.m. %.2f px' %
           (cls, SHAPE_OF[cls], len(dd), dd.mean(), dd.std(ddof=1) / np.sqrt(len(dd))))
    pr('      largest |cap-midpoint - marker row| = %.1f px' % np.abs(dm).max())
    ds = np.array([m['err_hi'] - m['err_lo'] for m in allm])
    pr('   err_hi - err_lo: mean %+.2f km/s, SD %.2f km/s;  typical half-width %.1f km/s (min %.1f, max %.1f)' %
       (ds.mean(), ds.std(ddof=1), np.mean([0.5 * (m['err_hi'] + m['err_lo']) for m in allm]),
        min(min(m['err_hi'], m['err_lo']) for m in allm), max(max(m['err_hi'], m['err_lo']) for m in allm)))
    pr()
    pr('   per-point diagnostics (SSD = truncated template cost per usable pixel; far/near = SSD of the best competitor '
       '>=3 px away along the bar / of the best +-1 px neighbour, divided by the best SSD)')
    for gname, line, m in rows_out:
        mt = m['match']
        pr('      %-9s %-8s %-6s px(%4d,%3d) SSD %6.1f far x%5.1f near x%5.1f usable %3.0f%% silhouette covered %3.0f%%' %
           (gname, line, m['tag'], m['x'], m['y'], mt['ssd'], mt['ssd_far'] / mt['ssd'], mt['ssd_near'] / mt['ssd'],
            100.0 * mt['n_valid'] / (2 * RAD + 1) ** 2, 100.0 * m['hidden']))
    pr()
    pr('6. ROBUSTNESS: whole localisation (masks, templates, bars, matching) repeated under alternative settings')
    base = [(m['gi'], m['cls'], m['bar_x'], m['x'], m['y'], m['cap_top'], m['cap_bot']) for m in markers]
    for var in ROBUSTNESS_VARIANTS:
        with params(**var):
            mv, _, _ = locate_markers(im, lum, sc, panels, legends, allowed)
        alt = [(m['gi'], m['cls'], m['bar_x'], m['x'], m['y'], m['cap_top'], m['cap_bot']) for m in mv]
        if len(alt) != len(base):
            res = 'COUNT CHANGED (%d vs %d)' % (len(alt), len(base))
        else:
            changed = [(a[1], a[2], a[3:5], b[3:5]) for a, b in zip(base, alt) if a != b]
            res = ('all %d positions and cap rows unchanged' % len(base)) if not changed else str(changed)
        pr('   %-52s -> %s' % (', '.join('%s=%g' % kv for kv in var.items()), res))
    pr('   stress (outside the validity range, expected to degrade):')
    for var in STRESS_VARIANTS:
        label = ', '.join('%s=%g' % kv for kv in var.items())
        try:
            with params(**var):
                mv, _, _ = locate_markers(im, lum, sc, panels, legends, allowed)
            alt = [(m['gi'], m['cls'], m['bar_x'], m['x'], m['y'], m['cap_top'], m['cap_bot']) for m in mv]
            changed = [(a[1], a[2], 'moves %d,%d px' % (b[3] - a[3], b[4] - a[4])) for a, b in zip(base, alt) if a != b]
            res = ('unchanged' if not changed else '%d position(s) change: %s' % (len(changed), changed))
        except RuntimeError as e:
            res = 'localisation fails (%s)' % e
        pr('   %-52s -> %s' % (label, res))
    pr()
    pr('7. RING-RADIUS REGULARITY (consistency check of the x calibration; NOT applied to the CSV)')
    for gname, line, _ in [(g['name'], l, n) for g in GALAXIES for _, l, n in g['lines']]:
        rr = np.array([m['radius'] for gn, ln, m in rows_out if gn == gname and ln == line])
        A = np.column_stack([np.ones(len(rr)), np.arange(len(rr))])
        co = np.linalg.lstsq(A, rr, rcond=None)[0]
        res = rr - A @ co
        pr('   %-10s %-8s R_k = %.4f + k*%.4f arcsec (R_0/Delta = %.3f); rms residual %.5f arcsec' %
           (gname, line, co[0], co[1], co[0] / co[1], np.sqrt((res ** 2).mean())))
    pr()
    pr('8. ACCURACY ESTIMATE (1-sigma; intrinsic limit = whole-pixel quantisation of the raster)')
    for g, cal in zip(GALAXIES, cals):
        fx, fy = cal['fx'], cal['fy']
        xs = np.array([m['radius'] for gn, _, m in rows_out if gn == g['name']])
        vs = np.array([m['v'] for gn, _, m in rows_out if gn == g['name']])
        sx = np.sqrt(SIGMA_Q ** 2 + axis_sigma_pix(fx, xs) ** 2) / fx['b']
        sy = np.sqrt(SIGMA_Q ** 2 + axis_sigma_pix(fy, vs) ** 2) / abs(fy['b'])
        pr('   %-10s radius: marker rounding %.5f + calibration (mean) %.5f -> mean total %.5f arcsec; worst-case +-0.5 px '
           '+ cal. 1 sigma %.5f arcsec' % (g['name'], SIGMA_Q / fx['b'], np.mean(axis_sigma_pix(fx, xs)) / fx['b'],
                                           np.mean(sx), (0.5 + axis_sigma_pix(fx, xs).max()) / fx['b']))
        pr('   %-10s vrot  : marker rounding %.3f + calibration (mean) %.3f -> mean total %.3f km/s; worst-case %.3f km/s; '
           'error-bar ends (difference of two rows) %.3f km/s each' %
           (g['name'], SIGMA_Q / abs(fy['b']), np.mean(axis_sigma_pix(fy, vs)) / abs(fy['b']), np.mean(sy),
            (0.5 + axis_sigma_pix(fy, vs).max()) / abs(fy['b']), np.sqrt(2) * SIGMA_Q / abs(fy['b'])))
    pr()

    # ---------------------------------------------------------------- 5. overlay
    try:
        font = ImageFont.load_default(size=22)
    except TypeError:
        font = ImageFont.load_default()
    ov_path = os.path.join(args.outdir, OVERLAY_NAME)
    draw_overlay(im, allm, cals, panels, legends, ov_path, font)

    def sha(path):
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    pr('FILES  %s  sha256 %s' % (CSV_NAME, sha(csv_path)))
    pr('       %s  sha256 %s' % (OVERLAY_NAME, sha(ov_path)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
