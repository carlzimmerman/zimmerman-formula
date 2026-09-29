#!/usr/bin/env python3
"""
CFG57 gas source 1 -- digitise the deprojected density profiles of
Lakhchaura et al. 2018, MNRAS 481, 4472 (arXiv:1806.00455v2), Appendix
Figure A.2, for NGC 4486, NGC 5846, NGC 4374 and NGC 4649, straight from the
vector graphics of the arXiv PDF (PyMuPDF), with the Table 1 distances and the
validation checks V1-V4 described in README.md.

Run from anywhere:   python3 extract_lakhchaura.py
Needs:               raw/lakhchaura2018_1806.00455.pdf (git-ignored; sha256 checked)
Optional input:      fukazawa2006_table4.tsv (cross-source row V4 only;
                     made by transcribe_fukazawa.py)
Writes (next to this script):
  lakhchaura2018_ne_profiles.tsv   the digitised profiles (the deliverable)
  extract_lakhchaura.out           the full run log (calibrations, checks)

Method (the diteodoro2023_extraction precedent, made exact):
  * matplotlib draws each axes in one go: its white background rectangle,
    then its data, spines, tick marks and tick labels.  Every vector path and
    every text span therefore belongs to the axes whose background was drawn
    last before it (PDF drawing order, PyMuPDF 'seqno').  That ownership is
    used throughout, so neighbouring panels that share an edge cannot leak
    ticks, labels or points into each other;
  * a galaxy's panel is the axes that drew its name;
  * tick labels are read from the text layer with their font sizes (mathtext
    base "10" at the large size, the exponent at the small size; a minus sign
    is a small filled black bar between them, detected as a vector shape);
  * each tick label is paired with its own tick mark (a vector line on the
    spine) and log10(value) is fitted linearly in the tick-mark coordinate:
    the fit residual over all labelled ticks is the calibration residual;
  * panels without their own labels (shared axes) carry the same tick marks
    at the same places as the labelled panel of their column (x) or row (y);
    that identity is checked, not assumed;
  * a plotted point is the centre of its filled red marker; its error bars are
    the red stroked lines through that centre (x bars = the shell edges
    [r_in, r_out]; y bars = the density error).
No model is fitted and no model prediction or dynamics is computed here.
"""
import hashlib
import math
import os
import re

import fitz  # PyMuPDF
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "raw", "lakhchaura2018_1806.00455.pdf")
SHA256 = "706f479c54fa5757013d5e47706714cee7ce474c3ddb841395387f4bae3b88b0"
OUT_TSV = os.path.join(HERE, "lakhchaura2018_ne_profiles.tsv")
OUT_LOG = os.path.join(HERE, "extract_lakhchaura.out")
FUK_TSV = os.path.join(HERE, "fukazawa2006_table4.tsv")

TARGETS = ["NGC4486", "NGC5846", "NGC4374", "NGC4649"]
# 1-indexed PDF pages of the appendix figures (each runs over 3 pages)
FIG_PAGES = {"A.1": (17, 18, 19),   # kT (keV), linear y
             "A.2": (20, 21, 22),   # n (cm^-3)
             "A.3": (23, 24, 25),   # K (keV cm^2)
             "A.4": (26, 27, 28)}   # P (erg cm^-3)
TABLE1_PAGE = 3
FIG1_PAGE = 6
NE_OVER_N = 0.53        # paper Sec. 2.2.5: "n = ne + ni ... ne = 0.53n"
MU = 0.62               # paper footnote 4: rho = mu n m_p, mu = 0.62
KEV_ERG = 1.602176634e-9
M_P_G = 1.67262192e-24
MSUN_G = 1.98847e33
KPC_CM = 3.0856775814913673e21
ARCSEC = math.pi / 180.0 / 3600.0
ACIS_PIX_ARCSEC = 0.492
STATED_DIG_ERR_DEX = 0.001   # the stated digitisation error, per coordinate

RED = (1.0, 0.0, 0.0)
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

_log_lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log_lines.append(s)


def rgb3(c):
    return None if c is None else tuple(round(float(v), 3) for v in c)


# --------------------------------------------------------------------------
# page model with drawing-order ownership
# --------------------------------------------------------------------------
class Page:
    def __init__(self, doc, pno):
        self.pno = pno
        self.page = doc[pno - 1]
        self.dr = self.page.get_drawings()
        white = [(g["seqno"], g["rect"]) for g in self.dr
                 if g["type"] == "f" and g.get("fill") == WHITE
                 and len(g["items"]) == 1 and g["items"][0][0] == "re"]
        # axes backgrounds: white rectangles containing no other white rectangle;
        # figure canvases: the ones that do
        self.frames = sorted((s, r) for s, r in white
                             if not any(o != r and r.contains(o) for _, o in white))
        self.canvases = [r for s, r in white if all(r != fr for _, fr in self.frames)]
        self.fseq = [s for s, _ in self.frames]

        # text spans (the text trace carries the drawing sequence number)
        self.spans = []
        for sp in self.page.get_texttrace():
            if tuple(round(v) for v in sp["dir"]) != (1, 0):
                continue                       # rotated axis titles are not tick labels
            t = "".join(chr(c[0]) for c in sp["chars"])
            self.spans.append(dict(t=t, size=sp["size"], bbox=fitz.Rect(sp["bbox"]),
                                   own=self.owner(sp["seqno"])))
        # mathtext minus signs: small filled black horizontal bars
        self.minus = [(g["rect"], self.owner(g["seqno"])) for g in self.dr
                      if g["type"] == "f" and g.get("fill") == BLACK
                      and g["rect"].width > 3 * g["rect"].height and g["rect"].height < 1.0]
        # black single-segment lines (tick marks and spines)
        self.blines = []
        for g in self.dr:
            if g["type"] in ("s", "fs") and g.get("color") == BLACK and len(g["items"]) == 1 \
                    and g["items"][0][0] == "l":
                p0, p1 = g["items"][0][1], g["items"][0][2]
                self.blines.append((p0.x, p0.y, p1.x, p1.y, self.owner(g["seqno"])))

    def owner(self, seqno):
        """Index of the axes that drew item `seqno` (None: figure level)."""
        k = None
        for i, s in enumerate(self.fseq):
            if s <= seqno:
                k = i
            else:
                break
        return k

    def rect(self, fi):
        return self.frames[fi][1]

    def frame_of_label(self, label):
        hits = [s for s in self.spans if s["t"].strip() == label]
        if len(hits) != 1 or hits[0]["own"] is None:
            return None
        fi = hits[0]["own"]
        c = (hits[0]["bbox"].tl + hits[0]["bbox"].br) / 2
        assert self.rect(fi).contains(c), "label drawn by an axes it does not sit in"
        return fi

    def axis_ticks(self, fi, side):
        """Tick marks drawn by axes fi on one spine: [(coordinate, length)].
        Inward (the appendix figures) or, if there are none, outward (Fig. 1)."""
        fr, tol = self.rect(fi), 0.05

        def collect(direction):
            out = []
            for x0, y0, x1, y1, own in self.blines:
                if own != fi:
                    continue
                if side == "bottom" and abs(x0 - x1) < 1e-3:
                    sgn = -1 if direction == "in" else 1
                    for ya, yb in ((y0, y1), (y1, y0)):
                        L = (yb - ya) * sgn
                        if abs(ya - fr.y1) < tol and 0.3 < L < 8 and fr.x0 - tol <= x0 <= fr.x1 + tol:
                            out.append((x0, L))
                if side == "left" and abs(y0 - y1) < 1e-3:
                    sgn = 1 if direction == "in" else -1
                    for xa, xb in ((x0, x1), (x1, x0)):
                        L = (xb - xa) * sgn
                        if abs(xa - fr.x0) < tol and 0.3 < L < 8 and fr.y0 - tol <= y0 <= fr.y1 + tol:
                            out.append((y0, L))
            return sorted(set(out))
        return collect("in") or collect("out")

    def tick_labels(self, fi, side, scale):
        """Tick labels drawn by axes fi below (x) / left of (y) its frame.
        Returns [(value, label centre along the axis, text)]."""
        fr = self.rect(fi)
        own = [s for s in self.spans if s["own"] == fi]
        if side == "bottom":
            cand = [s for s in own if fr.y1 - 2 < s["bbox"].y0 < fr.y1 + 12]
        else:
            cand = [s for s in own if fr.x0 - 45 < s["bbox"].x1 < fr.x0 + 0.5]
        nums = [s["size"] for s in cand if re.fullmatch(r"-?\d+(?:\.\d+)?", s["t"].strip())]
        lin_size = max(set(nums), key=nums.count) if nums else None
        labels, used = [], set()
        for i, s in enumerate(cand):
            if i in used:
                continue
            txt = s["t"].strip()
            if scale == "log":
                m = re.fullmatch(r"(?:(\d+(?:\.\d+)?)\s*×\s*)?10", txt)
                if not m:
                    continue
                # exponent: the smaller span right after the base, same line
                exps = [(j, e) for j, e in enumerate(cand)
                        if j != i and e["size"] < s["size"] - 0.5
                        and -0.5 < e["bbox"].x0 - s["bbox"].x1 < 6.0
                        and abs(e["bbox"].y0 - s["bbox"].y0) < 2.5]
                if len(exps) != 1:
                    continue
                j, e = exps[0]
                neg = any(o == fi and s["bbox"].x1 - 0.5 <= mr.x0 and mr.x1 <= e["bbox"].x0 + 0.5
                          and e["bbox"].y0 - 1 <= mr.y0 <= e["bbox"].y1 + 1 for mr, o in self.minus)
                k = int(e["t"].strip()) * (-1 if neg else 1)
                mant = float(m.group(1)) if m.group(1) else 1.0
                val = mant * 10.0 ** k
                bb = fitz.Rect(s["bbox"]) | e["bbox"]
                text = (m.group(1) + "x" if m.group(1) else "") + "10^" + str(k)
                used.add(j)
            else:
                if not re.fullmatch(r"-?\d+(?:\.\d+)?", txt) or abs(s["size"] - lin_size) > 0.01:
                    continue
                val, bb, text = float(txt), s["bbox"], txt
            c = (bb.x0 + bb.x1) / 2 if side == "bottom" else (bb.y0 + bb.y1) / 2
            labels.append((val, c, text))
        return labels


def calibrate(pg, fi, side, scale):
    """Pair axes fi's tick labels with its tick marks and fit
    f(value) = a + b * coordinate (f = log10 for a log axis).  The residual is
    per labelled tick, in dex (log axis) or axis units (linear)."""
    labels = pg.tick_labels(fi, side, scale)
    ticks = pg.axis_ticks(fi, side)
    if len(labels) < 2 or not ticks:
        return None
    Lmax = max(L for _, L in ticks)
    major = [t for t, L in ticks if L > 0.75 * Lmax]
    pairs = []
    for val, c, text in labels:
        # prefer a major tick; accept a labelled minor one (Fig. 1's 4x10^-1)
        tm = min(major, key=lambda q: abs(q - c))
        if abs(tm - c) < 1.5:
            t = tm
        else:
            ta = min((q for q, _ in ticks), key=lambda q: abs(q - c))
            if abs(ta - c) >= 1.5:
                continue
            t = ta
        pairs.append((val, t, c - t, text))
    if len(pairs) < 2:
        return None
    f = np.array([math.log10(v) if scale == "log" else v for v, _, _, _ in pairs])
    x = np.array([t for _, t, _, _ in pairs])
    b, a = np.polyfit(x, f, 1)
    resid = f - (a + b * x)
    return dict(a=a, b=b, resid=resid, pairs=pairs, scale=scale, side=side,
                ticks=[t for t, _ in ticks])


def to_value(cal, coord):
    v = cal["a"] + cal["b"] * coord
    return 10.0 ** v if cal["scale"] == "log" else v


def axis_cal_for(pg, fi, side, scale):
    """Axes fi's calibration from its own labels, else from the labelled axes
    of its column (x) / row (y), after checking that fi draws its tick marks
    at exactly the same places (a shared axis)."""
    own = calibrate(pg, fi, side, scale)
    if own is not None:
        own["source"] = "own labels"
        own["tick_mismatch_pt"] = 0.0
        return own
    fr = pg.rect(fi)
    if side == "bottom":
        mates = [j for j in range(len(pg.frames)) if j != fi
                 and abs(pg.rect(j).x0 - fr.x0) < 0.01 and abs(pg.rect(j).x1 - fr.x1) < 0.01]
    else:
        mates = [j for j in range(len(pg.frames)) if j != fi
                 and abs(pg.rect(j).y0 - fr.y0) < 0.01 and abs(pg.rect(j).y1 - fr.y1) < 0.01]
    mine = sorted(t for t, _ in pg.axis_ticks(fi, side))
    for j in mates:
        cal = calibrate(pg, j, side, scale)
        if cal is None:
            continue
        theirs = sorted(cal["ticks"])
        if len(mine) != len(theirs):
            continue
        cal["source"] = "labels of the %s axes at (%.1f, %.1f)" % (
            "column's labelled" if side == "bottom" else "row's labelled", pg.rect(j).x0, pg.rect(j).y0)
        cal["tick_mismatch_pt"] = max(abs(p - q) for p, q in zip(mine, theirs))
        return cal
    return None


def panel_points(pg, fi, color=RED):
    """Filled markers of `color` drawn by axes fi, with the stroked error-bar
    lines of the same colour (drawn by fi) that pass through each centre.
    Markers whose centre falls outside the frame were clipped away in the
    published figure; they are returned separately."""
    fr = pg.rect(fi)
    marks, hbars, vbars = [], [], []
    for g in pg.dr:
        if pg.owner(g["seqno"]) != fi:
            continue
        items = g["items"]
        if g["type"] == "fs" and g.get("fill") == color and len(items) >= 3:
            r = g["rect"]
            marks.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, r.width, r.height))
        elif g["type"] == "s" and g.get("color") == color and len(items) == 1 and items[0][0] == "l":
            p0, p1 = items[0][1], items[0][2]
            if abs(p0.y - p1.y) < 1e-4:
                hbars.append((min(p0.x, p1.x), max(p0.x, p1.x), p0.y))
            elif abs(p0.x - p1.x) < 1e-4:
                vbars.append((p0.x, min(p0.y, p1.y), max(p0.y, p1.y)))
    inside = [m for m in marks if fr.x0 <= m[0] <= fr.x1 and fr.y0 <= m[1] <= fr.y1]
    clipped = [m for m in marks if m not in inside]
    pts = []
    for mx, my, w, h in inside:
        hb = [b for b in hbars if abs(b[2] - my) < 2e-3 and b[0] - 1e-3 <= mx <= b[1] + 1e-3]
        vb = [b for b in vbars if abs(b[0] - mx) < 2e-3 and b[1] - 1e-3 <= my <= b[2] + 1e-3]
        pts.append(dict(x=mx, y=my, w=w, h=h, hbar=hb[0] if len(hb) == 1 else None,
                        vbar=vb[0] if len(vb) == 1 else None, n_hbar=len(hb), n_vbar=len(vb)))
    pts.sort(key=lambda p: p["x"])
    return pts, clipped, (len(hbars), len(vbars))


def extract_panel(doc, fig, label, yscale="log", verbose=True):
    """Find `label`'s panel among the pages of appendix figure `fig`, calibrate
    both axes and return its points in data units."""
    for pno in FIG_PAGES[fig]:
        pg = Page(doc, pno)
        fi = pg.frame_of_label(label)
        if fi is not None:
            break
    else:
        raise LookupError("panel %s not found in Fig. %s" % (label, fig))
    fr = pg.rect(fi)
    cx = axis_cal_for(pg, fi, "bottom", "log")
    cy = axis_cal_for(pg, fi, "left", yscale)
    if cx is None or cy is None:
        raise LookupError("calibration failed for %s Fig. %s" % (label, fig))
    pts, clipped, nbars = panel_points(pg, fi)
    canvas = [c for c in pg.canvases if c.contains(fr)]
    canvas = canvas[0] if canvas else None
    rows = []
    for p in pts:
        r, v = to_value(cx, p["x"]), to_value(cy, p["y"])
        r_in = r_out = v_lo = v_hi = float("nan")
        flags = []
        if p["hbar"]:
            r_in, r_out = to_value(cx, p["hbar"][0]), to_value(cx, p["hbar"][1])
            # matplotlib clips paths to the figure canvas: a shell edge at r = 0
            # (log -> -inf) ends at the canvas edge.  Such an edge is r_in = 0.
            if canvas is not None and p["hbar"][0] < canvas.x0 + 1.0:
                flags.append("x-bar reaches the canvas edge (%.1e kpc): r_in = 0" % r_in)
                r_in = 0.0
        if p["vbar"]:
            # PDF y grows downwards: the lower end of the bar is the larger y
            v_hi, v_lo = to_value(cy, p["vbar"][1]), to_value(cy, p["vbar"][2])
            if canvas is not None and p["vbar"][2] > canvas.y1 - 1.0:
                flags.append("lower y-bar reaches the canvas edge: lower end <= 0")
                v_lo = 0.0
        rows.append(dict(r=r, v=v, r_in=r_in, r_out=r_out, v_lo=v_lo, v_hi=v_hi, raw=p, flags=flags))
    info = dict(page=pg.pno, frame=fr, calx=cx, caly=cy, clipped=clipped, nbars=nbars,
                clipped_vals=[(to_value(cx, m[0]), to_value(cy, m[1])) for m in clipped])
    if verbose:
        log("  Fig. %s  %-8s page %d  axes frame (%.3f, %.3f)-(%.3f, %.3f): %d points inside the frame,"
            " %d clipped markers; red bar lines drawn: %d horizontal, %d vertical"
            % (fig, label, pg.pno, fr.x0, fr.y0, fr.x1, fr.y1, len(rows), len(clipped), nbars[0], nbars[1]))
        for nm, c in (("x", cx), ("y", cy)):
            unit = "dex" if c["scale"] == "log" else "axis units"
            log("     %s axis (%s) from %s; shared-tick mismatch %.1e pt; labelled ticks: %s"
                % (nm, c["scale"], c["source"], c["tick_mismatch_pt"], " ".join(t for *_, t in c["pairs"])))
            log("        log10(value) = %.6f %+.8f * coord; residual rms %.1e %s, max %.1e %s;"
                " label-to-tick offsets %s pt"
                % (c["a"], c["b"], float(np.sqrt(np.mean(c["resid"] ** 2))), unit,
                   float(np.max(np.abs(c["resid"]))), unit,
                   " ".join("%.2f" % o for _, _, o, _ in c["pairs"])))
    return rows, info


# --------------------------------------------------------------------------
# Table 1 (PDF page 3): z, D, kT(10 kpc), LX(10 kpc), H-alpha class
# --------------------------------------------------------------------------
def parse_table1(doc):
    txt = doc[TABLE1_PAGE - 1].get_text()
    body = txt.split("Magnitude", 1)[1].split("* redshift-independent", 1)[0]
    names = list(re.finditer(r"^(3C \d+|IC \d+|NGC \d+)\s*$", body, flags=re.M))
    out = {}
    for i, m in enumerate(names):
        chunk = body[m.end(): names[i + 1].start() if i + 1 < len(names) else len(body)]
        toks = chunk.split()
        dtok = toks[1]
        pm = re.findall(r"(\d+\.\d+)±(\d+\.\d+)", chunk)
        cls = re.search(r"\n(N|NE|E|U)[\d,]*\n", chunk)
        out[m.group(1).replace(" ", "")] = dict(
            z=float(toks[0]), D=float(dtok.rstrip("∗")), D_flag=dtok.endswith("∗"), D_str=dtok,
            kT=float(pm[0][0]), kT_err=float(pm[0][1]), LX42=float(pm[1][0]), LX42_err=float(pm[1][1]),
            kT_str=pm[0][0], LX_str=pm[1][0], cls=cls.group(1) if cls else None,
            raw=" | ".join(chunk.strip().split("\n")[:4]))
    return out


def ang_diam_distance(z, H0=70.0, Om=0.3, OL=0.7):
    """Flat LCDM angular-diameter distance in Mpc (the paper's cosmology)."""
    zz = np.linspace(0.0, z, 2001)
    Dc = 299792.458 / H0 * np.trapz(1.0 / np.sqrt(Om * (1 + zz) ** 3 + OL), zz)
    return Dc / (1 + z)


# --------------------------------------------------------------------------
def main():
    log("extract_lakhchaura.py -- CFG57 gas source 1: Lakhchaura et al. 2018, MNRAS 481, 4472")
    h = hashlib.sha256(open(PDF, "rb").read()).hexdigest()
    log("PDF", os.path.relpath(PDF, HERE), "sha256", h, "match:", h == SHA256)
    if h != SHA256:
        raise SystemExit("sha256 mismatch -- wrong or modified PDF")
    log("PyMuPDF", getattr(fitz, "VersionBind", "?"), "| numpy", np.__version__)
    doc = fitz.open(PDF)

    # ---------------- Table 1 -------------------------------------------
    t1 = parse_table1(doc)
    log("\n[Table 1, PDF page %d] parsed %d galaxies" % (TABLE1_PAGE, len(t1)))
    kts = [v["kT"] for v in t1.values()]
    lxs = [v["LX42"] for v in t1.values()]
    log("  parse check against Sec. 3.1 ('0.47 keV to 1.64 keV'; 'from 2.3e40 to 2.5e42 erg/s'):"
        " kT %.2f-%.2f keV, LX %.2g-%.3g erg/s" % (min(kts), max(kts), min(lxs) * 1e42, max(lxs) * 1e42))
    cls_count = {c: sum(1 for v in t1.values() if v["cls"] == c) for c in ("N", "NE", "E", "U")}
    log("  H-alpha classes", cls_count, "(Sec. 2.1 text: N 20, NE 12, E 13, U 4)")
    for nm in TARGETS:
        v = t1[nm]
        log("  %-8s z=%.4f  D=%s Mpc  kT=%s keV  LX=%se42 erg/s  class %s   [raw text: %s]"
            % (nm, v["z"], v["D_str"], v["kT_str"], v["LX_str"], v["cls"], v["raw"]))

    # ---------------- Fig. A.2: the deliverable -------------------------
    log("\n[Fig. A.2] 'Deprojected density profiles': plotted quantity n = ne + ni (cm^-3), log-log")
    prof = {nm: extract_panel(doc, "A.2", nm) for nm in TARGETS}

    log("\n[Fig. A.2] per-point geometry checks")
    worst_cross = 0.0
    for nm in TARGETS:
        rows, info = prof[nm]
        bad = [i for i, r in enumerate(rows) if r["raw"]["n_hbar"] != 1 or r["raw"]["n_vbar"] != 1]
        mid = [abs(math.log10(r["r"] / (0.5 * (r["r_in"] + r["r_out"])))) for r in rows]
        gaps = [abs(math.log10(rows[i + 1]["r_in"] / rows[i]["r_out"])) for i in range(len(rows) - 1)]
        circ = max(abs(r["raw"]["w"] - r["raw"]["h"]) for r in rows)
        worst_cross = max([worst_cross] + [abs(r["raw"]["hbar"][2] - r["raw"]["y"]) for r in rows]
                          + [abs(r["raw"]["vbar"][0] - r["raw"]["x"]) for r in rows])
        log("  %-8s %2d points, each with exactly one x-bar and one y-bar: %s; bars not used by any point:"
            " %d h / %d v; plotted r = linear mid-shell (r_in+r_out)/2 to %.1e dex; shells contiguous"
            " (r_out[i] = r_in[i+1]) to %.1e dex; circular markers (w-h %.1e pt)"
            % (nm, len(rows), not bad, info["nbars"][0] - len(rows), info["nbars"][1] - len(rows),
               max(mid), max(gaps), circ))
        for i, r in enumerate(rows):
            for f in r["flags"]:
                log("     point %d (r = %.4g kpc): %s" % (i, r["r"], f))
            if r["raw"]["hbar"] and r["raw"]["hbar"][0] < info["frame"].x0 and not r["flags"]:
                log("     point %d: the inner shell edge lies left of the axis limit (hidden by the clip path,"
                    " present in the vector data): r_in = %.5f kpc" % (i, r["r_in"]))
            if r["raw"]["vbar"] and (r["raw"]["vbar"][1] < info["frame"].y0 or r["raw"]["vbar"][2] > info["frame"].y1):
                log("     point %d: its y-bar runs past the frame; the drawn ends are used" % i)
        if info["clipped"]:
            log("     clipped (invisible) markers drawn by this axes:", info["clipped_vals"])

    # the digitisation error budget
    rx = max(float(np.max(np.abs(prof[nm][1]["calx"]["resid"]))) for nm in TARGETS)
    ry = max(float(np.max(np.abs(prof[nm][1]["caly"]["resid"]))) for nm in TARGETS)
    sx = max(abs(prof[nm][1]["calx"]["b"]) for nm in TARGETS)
    sy = max(abs(prof[nm][1]["caly"]["b"]) for nm in TARGETS)
    mis = max(max(prof[nm][1]["calx"]["tick_mismatch_pt"], prof[nm][1]["caly"]["tick_mismatch_pt"]) for nm in TARGETS)
    log("\n[digitisation error] calibration residual max %.1e dex (x) / %.1e dex (y); shared-tick mismatch"
        " max %.1e pt; marker centre vs error-bar line max %.1e pt; 1e-3 pt of coordinate = %.1e dex (x) /"
        " %.1e dex (y)" % (rx, ry, mis, worst_cross, 1e-3 * sx, 1e-3 * sy))
    log("  internal error <= %.1e dex (x), <= %.1e dex (y); STATED digitisation error %.3f dex per coordinate"
        " (conservative; validated below)" % (rx + 1e-3 * sx, ry + 1e-3 * sy, STATED_DIG_ERR_DEX))

    write_tsv(t1, prof)
    distance_diagnostic(doc, t1)
    fig1 = validate_fig1(doc, t1)
    cross_figure(doc, prof)
    gas_mass_check(prof, fig1)
    fukazawa_row(prof, t1)

    with open(OUT_LOG, "w") as f:
        f.write("\n".join(_log_lines) + "\n")
    print("\nwrote", os.path.relpath(OUT_TSV, HERE), "and", os.path.relpath(OUT_LOG, HERE))


def write_tsv(t1, prof):
    L = ["# Lakhchaura K., Werner N., Sun M., Canning R. E. A., Gaspari M., Allen S. W., Connor T., Donahue M.,"
         " Sarazin C., 2018, MNRAS 481, 4472, 'Thermodynamic properties, multiphase gas and AGN feedback in a large"
         " sample of giant ellipticals'",
         "# arXiv:1806.00455 (v2, 15 Oct 2018); source PDF raw/lakhchaura2018_1806.00455.pdf, sha256 " + SHA256,
         "# Source: Appendix Figure A.2 'Deprojected density profiles of the individual galaxies' (vector graphics);"
         " NGC4374, NGC4486, NGC4649 on PDF page 21, NGC5846 on PDF page 22 (1-indexed)",
         "# D_Mpc_paper: Table 1 (PDF page 3) 'mean redshift-independent distance (NED)'. The kpc radii were made"
         " with this D: every finite innermost shell edge in Fig. A.2 is a whole number of ACIS pixels (or 2.000"
         " arcsec) at the Table 1 D and not at the H0=70 redshift distance (extract_lakhchaura.out, distance diagnostic)",
         "# Extraction script: extract_lakhchaura.py (PyMuPDF %s); full run log: extract_lakhchaura.out"
         % getattr(fitz, "VersionBind", "?")]
    for nm in TARGETS:
        _, info = prof[nm]
        cx, cy = info["calx"], info["caly"]
        L.append("# axis calibration %s (page %d): x residual max %.1e dex over %d labelled ticks (%s; %s);"
                 " y residual max %.1e dex over %d labelled ticks (%s; %s); shared-tick mismatch x %.1e pt, y %.1e pt"
                 % (nm, info["page"], float(np.max(np.abs(cx["resid"]))), len(cx["pairs"]),
                    " ".join(t for *_, t in cx["pairs"]), cx["source"],
                    float(np.max(np.abs(cy["resid"]))), len(cy["pairs"]),
                    " ".join(t for *_, t in cy["pairs"]), cy["source"],
                    cx["tick_mismatch_pt"], cy["tick_mismatch_pt"]))
    L += ["# DIGITISATION ERROR: %.3f dex per coordinate (r and n), stated conservatively. Internal estimate"
          " < 1e-4 dex: the log-axis fits reproduce every labelled tick to < 1e-6 dex, a vector coordinate is exact"
          " to ~1e-3 pt (= 2e-5 dex in r, 3e-5 dex in n), marker centre = error-bar crossing to < 1e-3 pt."
          " Validation (README): V1 the same method on Fig. 1 returns the printed Table 1 kT and LX of all four"
          " galaxies to 1e-6; V2 shell by shell, P(Fig. A.4) = n(Fig. A.2) kT(Fig. A.1) x 1.6e-9 erg/keV and"
          " K(Fig. A.3) = kT (0.53 n)^(-2/3) to 1e-5; V3 the whole-shell gas mass reproduces the paper's Fig. 1"
          " Mgas(10 kpc) of all four galaxies to 0.23%%." % STATED_DIG_ERR_DEX,
          "# QUANTITY: Fig. A.2 plots the TOTAL particle density n = ne + ni (paper Sec. 2.2.5, eq. 1; confirmed by"
          " V2). ne_* = 0.53 * n_* (the paper's own conversion for a fully ionised 1/3-solar plasma, 'ne = 0.53n')."
          " n_* = the plotted values as digitised.",
          "# r_kpc: plotted radius = linear mid-point of the deprojection shell, (r_in + r_out)/2 (verified to < 1e-5"
          " dex). r_in_kpc, r_out_kpc: the x error-bar ends = the shell edges (r_in = 0: the bar reaches the figure"
          " edge, i.e. the innermost shell starts at the centre). ne_lo/ne_hi, n_lo/n_hi: the y error-bar ends as"
          " drawn (the paper does not state the confidence level). The paper assumes constant n in each shell.",
          "# NOTE (as plotted, not edited): the outermost shell sits above the trend for %s -- the usual"
          " outermost-shell deprojection effect; Sec. 2.2.3 warns the outermost annuli may include group/cluster"
          " emission." % "; ".join("%s x%.2f the previous point" % (nm, prof[nm][0][-1]["v"] / prof[nm][0][-2]["v"])
                                   for nm in TARGETS if prof[nm][0][-1]["v"] > 1.2 * prof[nm][0][-2]["v"]),
          "\t".join(["name", "D_Mpc_paper", "r_kpc", "ne_cm3", "ne_lo", "ne_hi",
                     "r_in_kpc", "r_out_kpc", "n_cm3", "n_lo", "n_hi"])]
    for nm in TARGETS:
        for r in prof[nm][0]:
            L.append("\t".join([nm, t1[nm]["D_str"], "%.5g" % r["r"],
                                "%.5g" % (NE_OVER_N * r["v"]), "%.5g" % (NE_OVER_N * r["v_lo"]),
                                "%.5g" % (NE_OVER_N * r["v_hi"]),
                                "%.5g" % r["r_in"], "%.5g" % r["r_out"],
                                "%.5g" % r["v"], "%.5g" % r["v_lo"], "%.5g" % r["v_hi"]]))
    with open(OUT_TSV, "w") as f:
        f.write("\n".join(L) + "\n")
    log("\n[TSV] %s: %d rows" % (os.path.basename(OUT_TSV), sum(len(prof[nm][0]) for nm in TARGETS)))
    for nm in TARGETS:
        rows = prof[nm][0]
        log("  %-8s outermost three points (r kpc, n cm^-3): %s; last/previous = %.2f"
            % (nm, ", ".join("(%.2f, %.3g)" % (r["r"], r["v"]) for r in rows[-3:]), rows[-1]["v"] / rows[-2]["v"]))
    for nm in TARGETS:
        rows = prof[nm][0]
        log("  %-8s D=%s Mpc  %2d points  r = %.3f-%.2f kpc (shell edges %.4g-%.2f kpc)  n = %.3g-%.3g,"
            " ne = %.3g-%.3g cm^-3" % (nm, t1[nm]["D_str"], len(rows), rows[0]["r"], rows[-1]["r"], rows[0]["r_in"],
                                        rows[-1]["r_out"], min(r["v"] for r in rows), max(r["v"] for r in rows),
                                        NE_OVER_N * min(r["v"] for r in rows), NE_OVER_N * max(r["v"] for r in rows)))


def distance_diagnostic(doc, t1):
    """Which distance turned arcsec into kpc?  Every Fig. A.2 panel's innermost
    shell edge, converted back to arcsec with (a) the Table 1 D and (b) the
    H0 = 70 angular-diameter distance of the Table 1 redshift."""
    log("\n[distance diagnostic] innermost shell edge of every Fig. A.2 panel, back in arcsec (ACIS pixel ="
        " 0.492\"), at D = Table 1 and at D = D_A(z; H0=70, Om=0.3)")
    res, zero = [], []
    for nm in sorted(t1):
        rows, _ = extract_panel(doc, "A.2", nm, verbose=False)
        r_in = rows[0]["r_in"]
        if r_in == 0.0:
            zero.append(nm)
            continue
        DT, DA = t1[nm]["D"], ang_diam_distance(t1[nm]["z"])
        res.append((nm, r_in, DT, DA, r_in / (DT * 1e3) / ARCSEC, r_in / (DA * 1e3) / ARCSEC))
    for nm, r_in, DT, DA, aT, aA in res:
        log("  %-8s r_in %.5f kpc | Table 1 D %6.2f Mpc: %.4f\" = %.3f px | D_A(z) %6.2f Mpc: %.4f\" = %.3f px%s"
            % (nm, r_in, DT, aT, aT / ACIS_PIX_ARCSEC, DA, aA, aA / ACIS_PIX_ARCSEC,
               "   <-- target" if nm in TARGETS else ""))
    pT = np.array([r[4] for r in res]) / ACIS_PIX_ARCSEC
    pA = np.array([r[5] for r in res]) / ACIS_PIX_ARCSEC
    offT = np.abs(pT - np.round(pT))
    offA = np.abs(pA - np.round(pA))
    arcT = np.array([abs(r[4] - round(r[4])) for r in res])
    log("  %d panels start at r = 0 (no central exclusion), incl. targets %s"
        % (len(zero), [z for z in zero if z in TARGETS]))
    log("  %d panels with a finite inner edge: at the Table 1 D, %d are within 0.01 px of a whole number of"
        " pixels (exceptions %s, within %.4f\" of a whole arcsec); at D_A(z), %d are within 0.01 px"
        " (median offset from a whole pixel %.3f px)"
        % (len(res), int(np.sum(offT < 0.01)), [r[0] for r, o in zip(res, offT) if o >= 0.01],
           max(arcT[offT >= 0.01]) if np.any(offT >= 0.01) else 0.0,
           int(np.sum(offA < 0.01)), float(np.median(offA))))
    log("  reading: the kpc radii were computed at the Table 1 distance (and so, the same pipeline, the"
        " densities via eq. 1); D_Mpc_paper = Table 1 D.")


# --------------------------------------------------------------------------
# V1 -- Figure 1 (page 6) against the printed Table 1 kT and LX
# --------------------------------------------------------------------------
CLASS_COLOUR = {"N": (1.0, 0.0, 0.0), "NE": (0.0, 0.502, 0.0), "E": (0.0, 0.0, 1.0),
                "U": (1.0, 0.647, 0.0)}


def fig1_points(pg, fi):
    """Data points of a Fig. 1 axes by class colour: the crossing of each
    marker's own x and y error bars (the legend box is excluded)."""
    fr = pg.rect(fi)
    own = [g for g in pg.dr if pg.owner(g["seqno"]) == fi]
    legend = [g["rect"] for g in own if g["type"] == "fs" and g.get("fill") == WHITE]
    out = []
    for cls, col in CLASS_COLOUR.items():
        marks, hb, vb = [], [], []
        for g in own:
            gc = rgb3(g.get("fill") if g["type"] == "fs" else g.get("color"))
            if gc != col:
                continue
            it = g["items"]
            if g["type"] == "fs" and 3 <= len(it) <= 12:
                r = g["rect"]
                if fr.contains(r) and not any(Lg.contains(r) for Lg in legend):
                    marks.append(r)
            elif g["type"] == "s" and len(it) == 1 and it[0][0] == "l":
                p0, p1 = it[0][1], it[0][2]
                if abs(p0.y - p1.y) < 1e-4:
                    hb.append((min(p0.x, p1.x), max(p0.x, p1.x), p0.y))
                elif abs(p0.x - p1.x) < 1e-4:
                    vb.append((p0.x, min(p0.y, p1.y), max(p0.y, p1.y)))
        for r in marks:
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            h = [b for b in hb if r.y0 <= b[2] <= r.y1 and b[0] - 1e-3 <= cx <= b[1] + 1e-3]
            v = [b for b in vb if r.x0 <= b[0] <= r.x1 and b[1] - 1e-3 <= cy <= b[2] + 1e-3]
            if h and v:
                h = min(h, key=lambda b: abs(b[2] - cy))
                v = min(v, key=lambda b: abs(b[0] - cx))
                out.append(dict(cls=cls, x=v[0], y=h[2], how="error-bar crossing"))
            else:
                out.append(dict(cls=cls, x=cx, y=cy, how="marker box centre"))
    return out


def validate_fig1(doc, t1):
    log("\n[V1] method validation: the same machinery on Fig. 1 (PDF page %d), whose plotted coordinates are"
        " printed in Table 1 (kT and LX within 10 kpc)" % FIG1_PAGE)
    pg = Page(doc, FIG1_PAGE)
    words = pg.page.get_text("words")
    panels = {}
    for fi in range(len(pg.frames)):
        fr = pg.rect(fi)
        t = " ".join(w[4] for w in words if fr.x0 - 40 < w[0] < fr.x0 and fr.y0 < w[1] < fr.y1)
        key = ("LX" if "ergs" in t else "Mgas" if "solar" in t else "fgas" if "gas" in t else "YX")
        panels[key] = fi
    out = {}
    for key in ("LX", "Mgas"):
        fi = panels[key]
        fr = pg.rect(fi)
        cx = calibrate(pg, fi, "bottom", "log")
        cy = calibrate(pg, fi, "left", "log")
        pts = fig1_points(pg, fi)
        for p in pts:
            p["X"], p["Y"] = to_value(cx, p["x"]), to_value(cy, p["y"])
        log("  axes %-4s (%.1f,%.1f)-(%.1f,%.1f): %d points %s (%d located by their error-bar crossing);"
            " x ticks %s (residual max %.1e dex); y ticks %s (residual max %.1e dex)"
            % (key, fr.x0, fr.y0, fr.x1, fr.y1, len(pts),
               {c: sum(1 for p in pts if p["cls"] == c) for c in CLASS_COLOUR},
               sum(1 for p in pts if p["how"] == "error-bar crossing"),
               " ".join(t for *_, t in cx["pairs"]), float(np.max(np.abs(cx["resid"]))),
               " ".join(t for *_, t in cy["pairs"]), float(np.max(np.abs(cy["resid"])))))
        out[key] = dict(pts=pts, calx=cx, caly=cy)
    # each Table 1 galaxy -> its LX-panel point (same colour, nearest in log kT, log LX)
    lx = out["LX"]["pts"]
    match, dev = {}, []
    for nm, v in sorted(t1.items()):
        cand = [p for p in lx if p["cls"] == v["cls"]]
        d = [math.hypot(math.log10(p["X"] / v["kT"]), math.log10(p["Y"] / (v["LX42"] * 1e42))) for p in cand]
        order = np.argsort(d)
        p = cand[int(order[0])]
        match[nm] = p
        rT, rL = p["X"] / v["kT"], p["Y"] / (v["LX42"] * 1e42)
        # printed rounding half-steps
        hT = 0.5 * 10 ** (-len(v["kT_str"].split(".")[1])) / v["kT"]
        hL = 0.5 * 10 ** (-len(v["LX_str"].split(".")[1])) / v["LX42"]
        dev.append((nm, rT, rL, max(abs(rT - 1) / hT, abs(rL - 1) / hL)))
        if nm in TARGETS:
            log("  %-8s printed kT %s keV, LX %se42 erg/s | digitised kT %.4f keV (ratio %.5f), LX %.4fe42"
                " (ratio %.5f) | next-nearest same-colour point %.3f dex away"
                % (nm, v["kT_str"], v["LX_str"], p["X"], rT, p["Y"] / 1e42, rL,
                   d[int(order[1])] if len(d) > 1 else float("nan")))
    ids = [id(p) for p in match.values()]
    ok = [x for x in dev if x[3] <= 1.0]
    log("  all %d galaxies (one-to-one match: %s): %d/%d digitised (kT, LX) round to the printed values;"
        " the exceptions are:" % (len(dev), len(set(ids)) == len(ids), len(ok), len(dev)))
    for nm, rT, rL, w in dev:
        if w > 1.0:
            p = match[nm]
            log("     %-8s printed kT %s, LX %s | plotted kT %.4f, LX %.4f (a table-vs-figure difference in the"
                " paper: the plotted value is a round number)" % (nm, t1[nm]["kT_str"], t1[nm]["LX_str"],
                                                                 p["X"], p["Y"] / 1e42))
    tgt = [x for x in dev if x[0] in TARGETS]
    log("  V1 RESULT (four targets): max |digitised/printed - 1| = %.2e (kT), %.2e (LX); criterion 10%%: %s"
        % (max(abs(x[1] - 1) for x in tgt), max(abs(x[2] - 1) for x in tgt),
           "PASS" if all(abs(x[1] - 1) < 0.1 and abs(x[2] - 1) < 0.1 for x in tgt) else "FAIL"))
    out["match"] = match
    return out


# --------------------------------------------------------------------------
# V2 -- per-shell identities between Figs. A.1, A.2, A.3, A.4
# --------------------------------------------------------------------------
def cross_figure(doc, prof):
    log("\n[V2] cross-figure identities per shell (Sec. 2.2.5: P = n kT, K = kT ne^(-2/3), ne = 0.53 n);"
        " every panel digitised independently with the same machinery; shells matched by plotted radius")
    for nm in TARGETS:
        rows_n, _ = prof[nm]
        other = {}
        for fig, sc in (("A.1", "linear"), ("A.3", "log"), ("A.4", "log")):
            other[fig] = extract_panel(doc, fig, nm, yscale=sc, verbose=False)
        rp, rk, rk_ne, nmatch = [], [], [], 0
        for a in rows_n:
            m = {}
            for fig in other:
                c = [b for b in other[fig][0] if abs(math.log10(b["r"] / a["r"])) < 1e-3]
                m[fig] = c[0] if len(c) == 1 else None
            if all(m.values()):
                nmatch += 1
                T = m["A.1"]["v"]
                rp.append(m["A.4"]["v"] / (a["v"] * T * KEV_ERG))
                rk.append(m["A.3"]["v"] / (T * (NE_OVER_N * a["v"]) ** (-2.0 / 3.0)))
                rk_ne.append(m["A.3"]["v"] / (T * a["v"] ** (-2.0 / 3.0)))
        rp, rk, rk_ne = np.array(rp), np.array(rk), np.array(rk_ne)
        cal = [other[f][1][k] for f in other for k in ("calx", "caly")]
        clip = {f: len(other[f][1]["clipped"]) for f in other}
        log("  %-8s A.2 shells %d; matched in A.1/A.3/A.4: %d (points inside frames: %s; clipped markers: %s);"
            " calibration residual max %.1e dex (log axes), %.1e keV (A.1 linear y)"
            % (nm, len(rows_n), nmatch, {f: len(other[f][0]) for f in other}, clip,
               max(float(np.max(np.abs(c["resid"]))) for c in cal if c["scale"] == "log"),
               float(np.max(np.abs(other["A.1"][1]["caly"]["resid"])))))
        if nmatch == 0:
            continue
        log("     P / (n kT x 1.602e-9 erg/keV)   : median %.5f, range %.5f-%.5f"
            "  [1.6/1.602177 = %.5f: the paper used 1 keV = 1.6e-9 erg]"
            % (np.median(rp), rp.min(), rp.max(), 1.6 / 1.602176634))
        log("     K / (kT (0.53 n)^(-2/3))        : median %.5f, range %.5f-%.5f  (n = total density, ne = 0.53 n)"
            % (np.median(rk), rk.min(), rk.max()))
        log("     K / (kT n^(-2/3)) [n taken as ne]: median %.4f  (would be 1 if the plotted n were ne)"
            % np.median(rk_ne))


# --------------------------------------------------------------------------
# V3 -- Mgas(<10 kpc) of Fig. 1 against the digitised shells
# --------------------------------------------------------------------------
def gas_mass_check(prof, fig1):
    log("\n[V3] gas mass inside 10 kpc: Fig. 1 upper right (the paper: 'Mgas(r) = int 4 pi r^2 mu m_H n dr',"
        " mu = 0.62) vs the digitised Fig. A.2 profile; the paper does not state its integration scheme")
    # The two panels draw each class's points in the same order (checked: the x sequences agree to
    # < 1e-6 for every class), so a galaxy's Mgas point is the one at the same place in its class's
    # drawing sequence as its LX point.  (x alone is ambiguous: NGC 4374 and NGC 4636 are both
    # 'NE' at kT = 0.68 keV.)
    seq = {}
    for key in ("LX", "Mgas"):
        for c in CLASS_COLOUR:
            seq[key, c] = [p for p in fig1[key]["pts"] if p["cls"] == c]
    same = max(max(abs(a["X"] / b["X"] - 1) for a, b in zip(seq["LX", c], seq["Mgas", c]))
               for c in CLASS_COLOUR if len(seq["LX", c]) == len(seq["Mgas", c]))
    log("  drawing-order check: per class, LX-panel and Mgas-panel x sequences agree to %.1e" % same)
    for nm in TARGETS:
        p_lx = fig1["match"][nm]
        k = [i for i, q in enumerate(seq["LX", p_lx["cls"]]) if q is p_lx][0]
        p = seq["Mgas", p_lx["cls"]][k]
        twins = [q for q in seq["Mgas", p_lx["cls"]] if q is not p and abs(q["X"] / p["X"] - 1) < 1e-4]
        dx = [(abs(p["X"] / p_lx["X"] - 1), k)]
        rows, _ = prof[nm]
        rho = [MU * M_P_G * r["v"] for r in rows]
        # (a) constant n in each shell (the deprojection's own assumption), shells cut at 10 kpc
        Ma = sum(4 / 3 * math.pi * ((min(r["r_out"], 10.0) * KPC_CM) ** 3 - (r["r_in"] * KPC_CM) ** 3) * d
                 for r, d in zip(rows, rho) if r["r_in"] < 10.0) / MSUN_G
        # (b) log-log interpolation through the plotted (mid-shell) points to 10 kpc, constant inside the first
        rr = np.logspace(-4, 1, 20001)
        dens = 10 ** np.interp(np.log10(rr), np.log10([r["r"] for r in rows]), np.log10(rho))
        Mb = float(np.trapz(4 * math.pi * (rr * KPC_CM) ** 2 * dens, rr * KPC_CM)) / MSUN_G
        # (c) whole shells, up to and including the shell that contains r = 10 kpc
        st = [r for r in rows if r["r_in"] < 10.0 <= r["r_out"]][0]
        Mc = sum(4 / 3 * math.pi * ((r["r_out"] * KPC_CM) ** 3 - (r["r_in"] * KPC_CM) ** 3) * d
                 for r, d in zip(rows, rho) if r["r_in"] < 10.0) / MSUN_G
        log("  %-8s Fig. 1 Mgas point #%d of class %s: kT %.4f keV (= its LX point to %.0e%s), Mgas = %.4g Msun"
            " | (a) shells cut at 10 kpc: %.4g, ratio %.3f | (b) log-log through the plotted points to 10 kpc:"
            " %.4g, ratio %.3f | (c) whole shells through the one containing 10 kpc (%.2f-%.2f kpc): %.4g,"
            " ratio %.4f"
            % (nm, k + 1, p_lx["cls"], p["X"], dx[0][0],
               "; same-x twin in this class: Mgas %s, resolved by drawing order"
               % ", ".join("%.4g" % q["Y"] for q in twins) if twins else "",
               p["Y"], Ma, Ma / p["Y"], Mb, Mb / p["Y"], st["r_in"], st["r_out"], Mc, Mc / p["Y"]))
    log("  reading: scheme (c) -- found after (a) and (b) fell 7-18% short -- reproduces the paper's own plotted"
        " gas masses for all four galaxies; Fig. 1's 'Mgas (10 kpc)' is the gas inside the outer edge of the shell"
        " containing 10 kpc, and the digitised densities carry the paper's scale")


# --------------------------------------------------------------------------
# V4 -- a different paper's ne(10 kpc) (cross-source, not a digitisation check)
# --------------------------------------------------------------------------
def fukazawa_row(prof, t1):
    if not os.path.exists(FUK_TSV):
        log("\n[V4] skipped (fukazawa2006_table4.tsv not present; run transcribe_fukazawa.py first)")
        return
    rows_f = [ln.rstrip("\n").split("\t") for ln in open(FUK_TSV) if not ln.startswith("#")]
    hdr, data = rows_f[0], {r[0]: r for r in rows_f[1:]}
    iD, iN = hdr.index("D_Mpc"), hdr.index("ne10_1e-3cm3")
    log("\n[V4] cross-source (NOT a digitisation check): ne at 10 kpc, Lakhchaura 0.53 n (log-log interpolated)"
        " vs Fukazawa+2006 Table 4, with Lakhchaura moved to Fukazawa's distance (r ~ D, ne ~ D^-1/2)")
    for nm in TARGETS:
        if nm not in data or data[nm][iN] in ("", "nan", "---"):
            log("  %-8s not in Fukazawa+2006 Table 4" % nm)
            continue
        DF, DL = float(data[nm][iD]), t1[nm]["D"]
        rows = prof[nm][0]
        lr = np.log10([r["r"] * DF / DL for r in rows])
        lne = np.log10([NE_OVER_N * r["v"] * (DF / DL) ** -0.5 for r in rows])
        ne10 = 10 ** np.interp(1.0, lr, lne)
        nf = float(data[nm][iN]) * 1e-3
        log("  %-8s D %.2f -> %.1f Mpc: Lakhchaura ne(10 kpc) = %.3e; Fukazawa %.3e cm^-3; ratio %.2f"
            " (had n been taken as ne: %.2f)" % (nm, DL, DF, ne10, nf, ne10 / nf, ne10 / NE_OVER_N / nf))


if __name__ == "__main__":
    main()
