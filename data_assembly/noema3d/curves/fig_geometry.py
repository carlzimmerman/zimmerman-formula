"""Geometry and axis calibration of the NOEMA3D paper-1 kinematic-profile figure (PDF Fig. 5, page 15, one raster image 3862x2376).
Panels: 10 galaxies (2 columns x 5 rows), 3 panels each (velocity, dispersion, normalised flux). Frames are found from the thin dark spines; ticks are found as short dark
segments just outside the frame; tick labels are read by tesseract (whitelist digits and minus) and the ticks are fitted linearly; residuals are reported."""
import numpy as np, subprocess, tempfile, os, re
from PIL import Image
IMG = os.environ.get("NOEMA_FIG", os.path.expanduser("~/new_physics/_external_data/noema3d/fig5_raw.png"))
A = np.array(Image.open(IMG).convert("RGB")).astype(int)
DARK = A.max(axis=2) < 160
ROWS = [(55, 416), (530, 891), (1005, 1366), (1480, 1841), (1955, 2316)]
COLS = [[(560, 935), (1011, 1405), (1486, 1876)], [(2535, 2910), (2998, 3381), (3457, 3851)]]
# order of galaxies (column-major: left column top to bottom, then right column), read from the figure's own labels
NAMES = [["G4_38065", "G4_20371", "GN4_24517", "GN4_32842", "G4_17555"], ["G4_38232", "G4_23011", "GN4_18574", "G4_24078", "G4_37375"]]
def frame(col, row, panel):
    """(x_left, x_right, y_top, y_bottom) of the axes frame. Rows are exact (same for every galaxy); the left and right spine columns are the columns whose dark fraction over the
    frame height is 1.0 within +-50 px of the row-0 estimate (the panel widths differ from galaxy to galaxy because the y-label widths differ)."""
    x0, x1 = COLS[col][panel]; y0, y1 = ROWS[row]
    def best(xa):
        c = [(DARK[y0 + 2:y1 - 1, x].mean(), x) for x in range(max(xa - 50, 0), min(xa + 51, DARK.shape[1]))]; m = max(f for f, _ in c)
        return min(x for f, x in c if f >= m - 0.01)
    return best(x0), best(x1), y0, y1
def clusters(idx):
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= 1: g[-1].append(i)
        else: g.append([i])
    return [float(np.mean(k)) for k in g]
def ticks(fr, side):
    xl, xr, yt, yb = fr
    if side == "bottom": m = DARK[yb + 2:yb + 6, xl:xr + 1].sum(axis=0) >= 3; return clusters(np.where(m)[0] + xl)
    if side == "top": m = DARK[yt - 6:yt - 2, xl:xr + 1].sum(axis=0) >= 3; return clusters(np.where(m)[0] + xl)
    if side == "left": m = DARK[yt:yb + 1, xl - 5:xl - 1].sum(axis=1) >= 3; return clusters(np.where(m)[0] + yt)
    if side == "right": m = DARK[yt:yb + 1, xr + 2:xr + 6].sum(axis=1) >= 3; return clusters(np.where(m)[0] + yt)
MINUS = {"\u2014": "-", "\u2212": "-", "\u2013": "-", "\u2012": "-", "_": "-", "~": "-"}
def ocr_tokens(box, psm=11):
    """numeric tokens with their centre in ORIGINAL pixel coordinates, from tesseract TSV"""
    box = (max(box[0], 0), max(box[1], 0), box[2], box[3])
    im = Image.fromarray(A[box[1]:box[3], box[0]:box[2]].astype("uint8")).convert("L"); im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    pad = Image.new("L", (im.width + 80, im.height + 80), 255); pad.paste(im, (40, 40))
    f = os.path.join(tempfile.gettempdir(), "noema_strip_%d.png" % os.getpid()); pad.save(f)
    r = subprocess.run(["tesseract", f, "-", "--psm", str(psm), "tsv"], capture_output=True, text=True).stdout; os.remove(f)
    out = []
    for line in r.splitlines()[1:]:
        p = line.split("\t")
        if len(p) < 12 or not p[11].strip(): continue
        t = "".join(MINUS.get(c, c) for c in p[11].strip())
        if re.fullmatch(r"-?\d+\.?\d*", t):
            cx = box[0] + (int(p[6]) + int(p[8]) / 2 - 40) / 3; cy = box[1] + (int(p[7]) + int(p[9]) / 2 - 40) / 3
            out.append((float(t), cx, cy))
    return out
def read_axis(fr, side, tk):
    """assign OCR tokens to ticks by nearest position; returns (values per tick or None, list of unmatched tokens)"""
    xl, xr, yt, yb = fr
    box = {"bottom": (xl - 40, yb + 7, xr + 40, yb + 58), "top": (xl - 40, max(yt - 58, 0), xr + 40, yt - 7), "left": (xl - 130, yt - 20, xl - 7, yb + 20), "right": (xr + 7, yt - 20, xr + 130, yb + 20)}[side]
    toks = ocr_tokens(box); vals = [None] * len(tk); un = []
    for v, cx, cy in toks:
        pos = cx if side in ("bottom", "top") else cy
        j = int(np.argmin([abs(pos - t) for t in tk])) if tk else None
        tol = 22 if side in ("bottom", "top") else 14
        if j is not None and abs(pos - tk[j]) < tol and vals[j] is None: vals[j] = v
        else: un.append(v)
    return vals, un
def axis_cal(fr, side):
    """Calibration of one axis from the OCR tokens: token centre (snapped to a detected tick mark when one lies within 3 px) vs the printed value.
    OCR sometimes drops a decimal point (2.5 -> 25): each token may be v or v/10 and the line supported by most tokens is kept.
    Returns dict(poly, max_resid, n, n_tokens, n_snapped, span, pts, dropped) or None."""
    xl, xr, yt, yb = fr
    box = {"bottom": (xl - 40, yb + 7, xr + 40, yb + 58), "top": (xl - 40, max(yt - 40, 0), xr + 40, yt - 5), "left": (xl - 130, yt - 20, xl - 7, yb + 20)}[side]
    toks = max((ocr_tokens(box, psm) for psm in (11, 6)), key=len); tk = ticks(fr, side)
    pts = []
    for v, cx, cy in toks:
        pos = cx if side in ("bottom", "top") else cy
        snap = [t for t in tk if abs(t - pos) < 3]
        pts.append((snap[0] if snap else pos, v, bool(snap)))
    if len(pts) < 3: return None
    x = np.array([p[0] for p in pts]); y0 = np.array([p[1] for p in pts]); cand = [(v, v / 10.0) for v in y0]; best = None
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            if abs(x[i] - x[j]) < 10: continue
            for a in cand[i]:
                for b in cand[j]:
                    m = (b - a) / (x[j] - x[i]); c = a - m * x[i]; pred = m * x + c; tol = max(0.02 * abs(m) * (x.max() - x.min()), 1e-9)
                    pick = [min(cv, key=lambda q: abs(q - pr)) for cv, pr in zip(cand, pred)]
                    inl = np.array([abs(pk - pr) < tol for pk, pr in zip(pick, pred)])
                    ndiv = sum(1 for pk, v in zip(pick, y0) if abs(pk - v) > 1e-12 and abs(v) > 1e-12); sc = (int(inl.sum()), -ndiv, -float(np.sum(np.abs(np.array(pick)[inl] - pred[inl]))))
                    if best is None or sc > best[0]: best = (sc, np.array(pick), inl)
    if best is None or best[2].sum() < 3: return None
    y = best[1]; keep = best[2]; p = np.polyfit(x[keep], y[keep], 1); r = y - np.polyval(p, x)
    return dict(poly=p, max_resid=float(np.abs(r[keep]).max()), n=int(keep.sum()), n_tokens=len(pts), n_snapped=int(sum(q[2] for q in pts)), span=float(y[keep].max() - y[keep].min()),
                pts=[(float(a), float(b)) for a, b in zip(x[keep], y[keep])], dropped=[(float(a), float(b)) for a, b in zip(x[~keep], y0[~keep])])
