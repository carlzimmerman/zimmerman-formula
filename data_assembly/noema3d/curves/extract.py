"""Raster digitisation of the NOEMA3D paper-1 kinematic-profile figure (PDF Fig. 5, page 15). One read per panel type (velocity, dispersion, normalised flux) for 10 galaxies.
Colours (RGB, measured from the figure): red (216,88,80), blue (72,128,184), green (80,168,80). Markers are found by morphological opening (lines are thinner than markers),
their centres refined by template fitting (circle, square or diamond of the size measured on isolated markers), y error bars by walking a thin strip along the marker column.
Model lines are traced from the colour mask with the markers and the legend removed; gaps (occlusion by markers or by the other line) are interpolated and flagged.
No acceleration, a0 or velocity ratio is computed here."""
import numpy as np, cv2, os, sys, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig_geometry import *
from scipy import ndimage as ndi
COLOURS = {"red": np.array([216, 88, 80]), "blue": np.array([72, 128, 184]), "green": np.array([80, 168, 80])}
def colour_mask(sub, name, tol=45):
    d = np.sqrt(((sub - COLOURS[name]) ** 2).sum(axis=2)); return d < tol
def tint_mask(sub, name, amin=0.30, tol=28):
    """pixels that are the colour blended with white (error bars may be drawn with alpha)"""
    c = COLOURS[name].astype(float); w = np.array([255., 255., 255.]); v = sub.astype(float) - w; cd = c - w
    a = (v * cd).sum(axis=2) / float(cd @ cd); res = np.sqrt(((v - a[..., None] * cd) ** 2).sum(axis=2))
    return (a > amin) & (a < 1.15) & (res < tol)
def interior(fr, m=3): xl, xr, yt, yb = fr; return xl + m, xr - m, yt + m, yb - m
SWATCH = {}
def legend_info(fr):
    """Legend groups 'Model' and 'Data': bounding boxes (image coordinates, swatches included) and entries (group, label, colour) with the colour read from the swatch left of each label."""
    x0, x1, y0, y1 = interior(fr); words = []
    im = Image.fromarray(A[y0:y1, x0:x1].astype("uint8")).convert("L"); im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    f = os.path.join(tempfile.gettempdir(), "noema_leg_%d.png" % os.getpid()); im.save(f)
    r = subprocess.run(["tesseract", f, "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout; os.remove(f)
    for line in r.splitlines()[1:]:
        p = line.split("\t")
        if len(p) < 12 or not p[11].strip(): continue
        words.append(dict(t=p[11].strip(), x0=x0 + int(p[6]) / 2, y0=y0 + int(p[7]) / 2, x1=x0 + (int(p[6]) + int(p[8])) / 2, y1=y0 + (int(p[7]) + int(p[9])) / 2))
    anchors = [w for w in words if w["t"] in ("Model", "Data")]
    boxes, entries = [], []
    for an in anchors:
        grp = [w for w in words if w is not an and w["t"] not in ("Model", "Data") and an["y0"] - 3 <= w["y0"] <= an["y0"] + 230 and an["x0"] - 120 <= w["x0"] <= an["x1"] + 260
               and (w["t"].startswith(("natural", "robust", "taper", "tappered", "uniform")) or "[model]" in w["t"] or "[data]" in w["t"])]
        if not grp: continue
        bx0 = min(min(w["x0"] for w in grp), an["x0"]) - 95; bx1 = max(max(w["x1"] for w in grp), an["x1"]) + 6; by0 = an["y0"] - 8; by1 = max(w["y1"] for w in grp) + 8
        boxes.append((int(max(bx0, x0)), int(min(bx1, x1)), int(max(by0, y0)), int(min(by1, y1))))
        for w in grp:
            if "[" in w["t"]: continue
            sw = A[int(w["y0"]):int(w["y1"]) + 1, int(w["x0"]) - 80:int(w["x0"]) - 8].reshape(-1, 3)
            best, bn = 0, None
            for cn, cv in COLOURS.items():
                n = int((np.sqrt(((sw - cv) ** 2).sum(axis=1)) < 45).sum())
                if n > best: best, bn = n, cn
            entries.append((an["t"], w["t"], bn, best))
            if an["t"] == "Data" and bn:                       # marker swatch of the Data legend: area of the largest own-colour component gives the marker size in this figure
                reg = A[int(w["y0"]) - 14:int(w["y1"]) + 15, int(w["x0"]) - 80:int(w["x0"]) - 8]
                mm = colour_mask(reg, bn, 45).astype(np.uint8); n_, lb_, st_, ce_ = cv2.connectedComponentsWithStats(mm)
                if n_ > 1: SWATCH[bn] = size_from_area(SHAPE[bn], float(st_[1:, cv2.CC_STAT_AREA].max()))
    return boxes, entries

SHAPE = {"red": "circle", "blue": "square", "green": "diamond"}
def disk(r): return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
def template(shape, size, cx, cy, H, W):
    yy, xx = np.mgrid[0:H, 0:W]; dx, dy = xx - cx, yy - cy
    if shape == "circle": return dx * dx + dy * dy <= size * size
    if shape == "square": return (np.abs(dx) <= size) & (np.abs(dy) <= size)
    return np.abs(dx) + np.abs(dy) <= size          # diamond: size = half diagonal
def size_from_area(shape, area):
    return float(np.sqrt(area / np.pi)) if shape == "circle" else (float(np.sqrt(area) / 2) if shape == "square" else float(np.sqrt(area / 2)))
def area_of(shape, size): return np.pi * size ** 2 if shape == "circle" else (4 * size ** 2 if shape == "square" else 2 * size ** 2)
def find_markers(sub, cname, excl, others, open_r=5, tol=45):
    """returns list of dict(cx, cy, area, partial, refined) in sub coordinates"""
    m = colour_mask(sub, cname, tol)
    for (a, b, c, d) in excl: m[c:d, a:b] = False
    o = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, disk(open_r))
    n, lab, st, cen = cv2.connectedComponentsWithStats(o, connectivity=8)
    comps = [(i, st[i, cv2.CC_STAT_AREA], cen[i]) for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 60]
    if not comps: return [], 0.0
    areas = np.array([c[1] for c in comps]); shape = SHAPE[cname]
    # full-marker area: upper quartile of component areas that are not merged (below 1.7 x median of the top half)
    top = np.sort(areas)[len(areas) // 2:]; full = float(np.median(top)); 
    if full > 1.6 * np.percentile(areas, 30) and len(areas) >= 4: full = float(np.percentile(areas, 60))
    size = size_from_area(shape, full); H, W = m.shape; out = []
    bg = (sub.min(axis=2) > 235); oth = np.zeros_like(bg)
    for on in others: oth |= colour_mask(sub, on, 45)
    for i, a, c in comps:
        k = max(1, int(round(a / full)))
        if a > 1.6 * full:                                       # merged markers of the same colour: split along the major axis by k-means on pixels
            ys, xs = np.where(lab == i); P = np.column_stack([xs, ys]).astype(np.float32)
            _, lb, cs = cv2.kmeans(P, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.1), 5, cv2.KMEANS_PP_CENTERS)
            for cc in cs: out.append(dict(cx=float(cc[0]), cy=float(cc[1]), area=a / k, partial=False, merged=True))
        else: out.append(dict(cx=float(c[0]), cy=float(c[1]), area=float(a), partial=bool(a < 0.82 * full), merged=False))
    win = int(size) + 2
    for mk in out:                                               # template refinement for every marker (own colour counts, background is penalised, other colours neutral)
        best = None
        for dy in np.arange(-win, win + 0.01, 1.0):
            for dx in np.arange(-win, win + 0.01, 1.0):
                cx, cy = mk["cx"] + dx, mk["cy"] + dy
                x0, x1, y0, y1 = int(cx - size - 3), int(cx + size + 4), int(cy - size - 3), int(cy + size + 4)
                if x0 < 0 or y0 < 0 or x1 > W or y1 > H: continue
                T = template(shape, size, cx - x0, cy - y0, y1 - y0, x1 - x0); sc = (m[y0:y1, x0:x1] & T).sum() - 2.0 * (bg[y0:y1, x0:x1] & T).sum() - 0.3 * (oth[y0:y1, x0:x1] & T).sum()
                if best is None or sc > best[0]: best = (sc, cx, cy)
        if best: mk["rx"], mk["ry"] = best[1], best[2]
        else: mk["rx"], mk["ry"] = mk["cx"], mk["cy"]
    return out, size

def scan_markers(sub, cname, size, excl, min_own=0.62, max_bg=0.03, tol=45):
    """Template scan: every centre where the marker template is >= min_own covered by the series colour and <= max_bg background.
    Occluded markers (drawn under another series) are found if at least min_own of the template is visible; others are missed and counted as such by the caller."""
    shape = SHAPE[cname]; size_full = size; size = max(size - 1.5, 3.0)          # scan with the inner template so anti-aliased edge pixels do not count as background
    own = colour_mask(sub, cname, tol).astype(np.float32)
    for (a, b, c, d) in excl: own[c:d, a:b] = 0
    bg = (sub.min(axis=2) > 225).astype(np.float32); r = int(np.ceil(size)) + 1; k = 2 * r + 1
    T = template(shape, size, r, r, k, k).astype(np.float32); nT = T.sum()
    fo = cv2.filter2D(own, -1, T, borderType=cv2.BORDER_CONSTANT); fb = cv2.filter2D(bg, -1, T, borderType=cv2.BORDER_CONSTANT)
    ok = (fo >= min_own * nT) & (fb <= max_bg * nT); H, W = own.shape
    ok[:r + 1, :] = False; ok[:, :r + 1] = False; ok[H - r - 1:, :] = False; ok[:, W - r - 1:] = False
    score = np.where(ok, fo - 3 * fb, -1e9); found = []; sc = score.copy()
    while True:
        i = np.unravel_index(np.argmax(sc), sc.shape)
        if sc[i] < 0: break
        y, x = i; region = (score[max(0, y - 1):y + 2, max(0, x - 1):x + 2] >= sc[i] - 2)
        ys, xs = np.mgrid[max(0, y - 1):y + 2, max(0, x - 1):x + 2]; cx = float(xs[region].mean()); cy = float(ys[region].mean())
        found.append(dict(rx=cx, ry=cy, vis=float(fo[y, x] / nT)))
        sc[max(0, y - int(1.7 * size)):y + int(1.7 * size) + 1, max(0, x - int(1.7 * size)):x + int(1.7 * size) + 1] = -1e9
    return sorted(found, key=lambda d: d["rx"])
def marker_size(sub, cname, excl):
    """size (radius / half-side / half-diagonal) from the areas of isolated, fully visible components after opening"""
    mk, size = find_markers(sub, cname, excl, [c for c in COLOURS if c != cname]); return size

def error_bar(sub, cname, cx, cy, size, tol=45):
    """vertical error-bar extent above and below a marker (sub coordinates, pixels), walking the strip cx-1..cx+1 over own-colour or tinted-own pixels; gaps up to 3 px are bridged"""
    own = colour_mask(sub, cname, tol) | tint_mask(sub, cname); H, W = own.shape; xs = slice(max(0, int(round(cx)) - 1), min(W, int(round(cx)) + 2))
    def walk(step):
        y = int(round(cy)) + step * int(np.ceil(size)); last = int(round(cy)) + step * int(np.ceil(size)); gap = 0
        while 0 <= y < H:
            if own[y, xs].any(): last = y; gap = 0
            else:
                gap += 1
                if gap > 3: break
            y += step
        return last
    up, dn = walk(-1), walk(+1); return float(up), float(dn)
def trace_line(sub, cname, footprints, excl, tol=45, min_run=3, max_run=90):
    """centre line of a thick model line: column runs (markers, legend and thin error bars removed), continuity tracking, gaps interpolated and flagged.
    Returns arrays x (px), y (px), flag (0 measured, 1 interpolated, 2 wide run)."""
    m = colour_mask(sub, cname, tol)
    for (a, b, c, d) in excl: m[c:d, a:b] = False
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)).astype(bool)          # drops 1-2 px error-bar strokes
    m &= ~footprints; H, W = m.shape; xs = []; ys = []; fl = []; prev = None
    for x in range(W):
        col = m[:, x].view(np.int8); d = np.diff(np.concatenate([[0], col, [0]])); s0 = np.where(d == 1)[0]; e0 = np.where(d == -1)[0]
        runs = [((a + b - 1) / 2.0, b - a) for a, b in zip(s0, e0) if b - a >= min_run]
        if not runs: continue
        if prev is None: c, t = max(runs, key=lambda r: r[1])
        else: c, t = min(runs, key=lambda r: abs(r[0] - prev))
        if prev is not None and abs(c - prev) > 160 and t < max_run: continue
        xs.append(x); ys.append(c); fl.append(2 if t > max_run else 0); prev = c
    return np.array(xs, float), np.array(ys, float), np.array(fl)
