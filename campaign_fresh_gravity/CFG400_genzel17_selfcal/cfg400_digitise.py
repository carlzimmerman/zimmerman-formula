"""CFG400 digitiser: Genzel+2017 (arXiv:1703.04310) Figure 1 (PDF page 3), vector markers + error bars, axes calibrated per panel
from its own tick labels. Criteria: FROZEN_CRITERIA.md (1dccb3a0c). Output: cfg400_points.csv. Read-only on the PDF.
"""
import csv, json, math, os, sys
import numpy as np
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "arxiv_pdf", "1703.04310.pdf"))
p = fitz.open(PDF)[2]
W = p.get_text("words")
D = p.get_drawings()
import re
def num(s):
    s2 = s.replace("\u2013", "-").replace("\u2212", "-")
    return float(s2) if re.fullmatch(r"[+-]?\d+(\.\d+)?", s2) else None
words = [(0.5 * (w[0] + w[2]), 0.5 * (w[1] + w[3]), num(w[4]), w[4]) for w in W]
words = [w for w in words if w[2] is not None]
marks = [x for x in D if x["type"] in ("f", "fs") and 1.5 < x["rect"].width < 3 and 1.5 < x["rect"].height < 3]
segs = [x for x in D if x["type"] == "s"]
ids = {}
for w in W:
    if w[4] in ("01351", "15504", "43501", "6397", "406690", "400569") and w[0] < 200 and w[1] < 520:   # the left-column labels only (not the caption)
        ids[w[4]] = 0.5 * (w[1] + w[3])
GAL = {"01351": "COS4 01351", "15504": "D3a 15504", "43501": "GS4 43501", "6397": "D3a 6397", "406690": "zC 406690", "400569": "zC 400569"}

def panel(xlab_lo, xlab_hi, ycand):
    """y-axis labels: words in x window; returns groups of (y, value) clustered by y."""
    lab = sorted([(w[1], w[2], w[0]) for w in words if xlab_lo <= w[0] <= xlab_hi and w[2] in ycand], key=lambda t: t[0])
    groups, cur = [], []
    for t in lab:
        if cur and t[1] > cur[-1][1]:     # new panel: a gap, or the value jumps back up
            groups.append(cur); cur = []
        cur.append(t)
    if cur:
        groups.append(cur)
    return [g for g in groups if len(g) >= 3]

vel_groups = panel(258, 278, {-300, -200, -100, 0, 100, 200, 300})
dis_groups = panel(420, 434, {0, 50, 100, 150, 200})
out, report = [], []
for kind, groups, xr in (("v", vel_groups, (276, 350)), ("s", dis_groups, (432, 505))):
    for g in groups:
        ys = np.array([t[0] for t in g]); vs = np.array([t[1] for t in g])
        ay, by = np.polyfit(ys, vs, 1)                          # value = ay*y + by
        resid = np.max(np.abs(ay * ys + by - vs)) / (vs.max() - vs.min())
        ytop, ybot = ys.min() - 6, ys.max() + 6
        # x-axis arcsec labels: the row of small integers just below the panel bottom
        xl = [w for w in words if xr[0] <= w[0] <= xr[1] and ys.max() - 4 <= w[1] <= ys.max() + 14 and w[2] is not None and abs(w[2]) <= 3]
        if len(xl) < 3:
            continue
        xs = np.array([w[0] for w in xl]); xv = np.array([w[2] for w in xl])
        ax, bx = np.polyfit(xs, xv, 1)
        xres = np.max(np.abs(ax * xs + bx - xv)) / (xv.max() - xv.min())
        yc = 0.5 * (ytop + ybot)
        gid = min(ids, key=lambda k: abs(ids[k] - yc))
        n = 0
        for m in marks:
            cx, cy = 0.5 * (m["rect"].x0 + m["rect"].x1), 0.5 * (m["rect"].y0 + m["rect"].y1)
            if not (xr[0] <= cx <= xr[1] and ytop <= cy <= ybot):
                continue
            # error bar: vertical segment through the marker
            err = 0.0
            for s_ in segs:
                for it in s_["items"]:
                    if it[0] == "l":
                        a, b = it[1], it[2]
                        if abs(a.x - b.x) < 0.3 and abs(a.x - cx) < 0.6 and min(a.y, b.y) <= cy <= max(a.y, b.y):
                            err = max(err, abs(ay) * abs(a.y - b.y) / 2)
            out.append(dict(galaxy=GAL[gid], kind=kind, offset_arcsec=ax * cx + bx, value=ay * cy + by, err=err))
            n += 1
        report.append(dict(galaxy=GAL[gid], kind=kind, n=n, ytick_resid=resid, xtick_resid=xres, nyt=len(g), nxt=len(xl)))
for r in report:
    print(f"{r['galaxy']:11s} {r['kind']}: {r['n']:2d} points | y-ticks {r['nyt']} (resid {r['ytick_resid']:.4f}) x-ticks {r['nxt']} (resid {r['xtick_resid']:.4f})")
with open(os.path.join(HERE, "cfg400_points.csv"), "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=["galaxy", "kind", "offset_arcsec", "value", "err"]); wr.writeheader(); wr.writerows(out)
json.dump(report, open(os.path.join(HERE, "cfg400_digitise_report.json"), "w"), indent=1)
print(f"total points {len(out)} (markers on page {len(marks)})")
