"""UD2: the a0 law on Malin 1 (FROZEN_CRITERIA.md + AMENDMENTS.md A1).

Rotation curve: Lelli, Fraternali & Sancisi 2010 Table 3 (typed below from the arXiv source). Baryon components: exact
path coordinates from the authors' vector EPS figures (inputs/*.eps, converted with gs -dSAFER -dEPSCrop to *.pdf).
Law: g = nu(g_b/a0) g_b, nu(y) = 1/2 + sqrt(1/4 + 1/y). Both footings, never pooled. kappa = 1/2 FITTED; not theory
closed. One galaxy excludes nothing.

usage: python3 ud2.py [law|MUTATE]   (MUTATE sets nu = 1; outputs go to ud2_MUTATE.*)
"""
import json, os, sys
import numpy as np
import fitz
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "law"
INP = os.path.join(HERE, "inputs")
CONV = 1e6 / 3.0857e19                        # (km/s)^2/kpc -> m/s^2
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
A0_PAPER = 3000.0                             # (km/s)^2/kpc, the paper's MOND a0 (K0b only)
I0, SIG_I = 38.0, 3.0
# Table 3 (Malin 1): ring radius kpc, V_c, sigma_Vc (km/s)
RT = np.array([12.5, 37.5, 62.5, 87.5]); VT = np.array([236.9, 216.2, 197.4, 214.1]); ET = np.array([9.4, 2.6, 4.7, 11.8])
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)


def nu(y):
    if MODE == "MUTATE":
        return np.ones_like(np.asarray(y, float))
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_std(y):                                # mu = x/sqrt(1+x^2) inverted; the paper's "standard" function (K0b)
    y = np.maximum(y, 1e-30); return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y ** 2))


def read(path):
    p = fitz.open(path)[0]; dr = []
    for d in p.get_drawings():
        pts = []
        for it in d["items"]:
            for q in it[1:]:
                if hasattr(q, "x"): pts.append((q.x, q.y))
        if pts:
            dr.append(dict(n=len(d["items"]), k="".join(i[0] for i in d["items"]), pts=np.array(pts),
                           col=tuple(round(c, 2) for c in d["color"]) if d.get("color") else None,
                           fill=tuple(round(c, 2) for c in d["fill"]) if d.get("fill") else None))
    words = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip(); x0, y0, x1, y1 = l["bbox"]
            words.append((t, 0.5 * (x0 + x1), 0.5 * (y0 + y1)))
    return dr, words


def axis(words, dr, vals, which, box, axis_line):
    """Tick label centres snapped to the nearest black-path vertex lying on the axis line (tol 0.6 pt)."""
    x0, x1, y0, y1 = box
    V = np.vstack([d["pts"] for d in dr if d["col"] == (0.0, 0.0, 0.0)])
    pairs = []
    for v in vals:
        c = [(x, y) for t, x, y in words if t == v and x0 <= x <= x1 and y0 <= y <= y1]
        if len(c) != 1: raise SystemExit(f"label {v!r}: {c}")
        x, y = c[0]
        if which == "x":
            on = V[np.abs(V[:, 1] - axis_line) < 0.6][:, 0]; cand = on[np.abs(on - x) < 4]
            pairs.append((float(v), cand[np.argmin(np.abs(cand - x))] if len(cand) else x))
        else:
            on = V[np.abs(V[:, 0] - axis_line) < 0.6][:, 1]; cand = on[np.abs(on - y) < 4]
            pairs.append((float(v), cand[np.argmin(np.abs(cand - y))] if len(cand) else y))
    v, c = np.array(pairs).T; m, b = np.polyfit(c, v, 1)
    return (lambda q: m * np.asarray(q) + b), float(np.max(np.abs(m * c + b - v)))


def curve(dr, col, n, xlim):
    c = [d for d in dr if d["col"] == col and d["n"] == n and xlim[0] <= d["pts"][:, 0].min() <= xlim[1]]
    if len(c) != 1: raise SystemExit(f"curve {col} n={n}: {len(c)}")
    return c[0]["pts"]


def dots(dr, xlim):
    c = [d["pts"].mean(axis=0) for d in dr if d["k"].startswith("cccc") and d["fill"] == (0.0, 0.0, 1.0)
         and xlim[0] <= d["pts"][:, 0].mean() <= xlim[1]]
    return np.array(sorted(tuple(q) for q in c))


def at(xpx, ypx, X, Y, R, ytop):
    r, v = X(xpx), Y(ypx); o = np.argsort(r)
    if np.any(np.interp(R, r[o], ypx[o]) <= ytop + 0.5): raise SystemExit("curve clipped at an evaluated radius")
    return np.interp(R, r[o], v[o])


def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))
def label(p): return "CONSISTENT" if p >= 0.05 else ("FAIL" if p < 0.01 else "TENSION")


def law_v(vb2, R, a0, ge=0.0):
    gN = vb2 / R * CONV
    if ge == 0.0: g = nu(gN / a0) * gN
    else: gt = gN + ge * a0; g = nu(gt / a0) * gt - nu(ge) * ge * a0
    return np.sqrt(np.maximum(g / CONV * R, 0))


R = {}
P(f"UD2 Malin 1, mode {MODE}. kappa = 1/2 FITTED; not theory closed; footings never pooled; one galaxy excludes nothing.")
BLUE, GREEN, CYAN, ORANGE, BLACK = (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (1.0, 0.55, 0.0), (0.0, 0.0, 0.0)

# ---- DecoHL (primary components, HSB 3.3, LSB 0.9), Malin 1 = lower-left panel
dr, w = read(os.path.join(INP, "DecoHL.pdf"))
X, rx = axis(w, dr, ["0", "20", "40", "60", "80", "100"], "x", (40, 360, 465, 490), 465.0)
Y, ry = axis(w, dr, ["0", "50", "100", "150", "200", "250", "300"], "y", (20, 46, 245, 475), 50.4)
dd = dots(dr, (40, 360)); Rd, Vd = X(dd[:, 0]), Y(dd[:, 1])
k0a1 = float(np.max(np.abs(Vd - VT))); k0a1r = float(np.max(np.abs(Rd - RT)))
P(f"DecoHL axis residual x {rx:.2e} y {ry:.2e}; dots R {np.round(Rd,2).tolist()} V {np.round(Vd,1).tolist()}")
P(f"K0a DecoHL dots vs Table 3: max |dV| {k0a1:.2f} km/s, max |dR| {k0a1r:.2f} kpc (line 1 km/s) -> {'PASS' if k0a1 <= 1 else 'FAIL'}")
comp = {}
for name, col in [("gas", GREEN), ("lsb", CYAN), ("hsb", ORANGE), ("dm", BLACK), ("total", BLUE)]:
    c = curve(dr, col, 61, (40, 70)); comp[name] = at(c[:, 0], c[:, 1], X, Y, RT, 249.0)
for kk, vv in comp.items(): P(f"  {kk:5s} at Table radii: {np.round(vv,1).tolist()}")
R["decoHL"] = {k: v.tolist() for k, v in comp.items()}; R["K0a_decoHL"] = dict(dV=k0a1, dR=k0a1r)

# ---- Mond2comp (their MOND fit; components at HSB 3.7, LSB 0.5)
drm, wm = read(os.path.join(INP, "Mond2comp_malin1.pdf"))
Xm, rxm = axis(wm, drm, ["0", "20", "40", "60", "80", "100"], "x", (60, 660, 420, 455), 417.0)
Ym, rym = axis(wm, drm, ["0", "50", "100", "150", "200", "250"], "y", (30, 72, 70, 440), 83.2)
dm_ = dots(drm, (60, 700)); Rdm, Vdm = Xm(dm_[:, 0]), Ym(dm_[:, 1])
k0a2 = float(np.max(np.abs(Vdm - VT)))
P(f"Mond2comp axis residual x {rxm:.2e} y {rym:.2e}; dots V {np.round(Vdm,1).tolist()}")
P(f"K0a Mond2comp dots vs Table 3: max |dV| {k0a2:.2f} km/s (line 1) -> {'PASS' if k0a2 <= 1 else 'FAIL'}")
cm = {}
for name, col in [("gas", GREEN), ("lsb", CYAN), ("hsb", ORANGE), ("total", BLUE)]:
    c = curve(drm, col, 61, (95, 110)); cm[name] = c
# K0b: their MOND total from their components, standard mu, a0 3000 (km/s)^2/kpc, on a grid clear of the clip
rg = np.linspace(8.0, 95.0, 30)
comp_m = {k: at(cm[k][:, 0], cm[k][:, 1], Xm, Ym, rg, 39.0) for k in ("gas", "lsb", "hsb", "total")}
vb2g = comp_m["gas"] ** 2 + comp_m["lsb"] ** 2 + comp_m["hsb"] ** 2
mine = np.sqrt(nu_std(vb2g / rg / A0_PAPER) * vb2g)
k0b = float(np.median(np.abs(mine / comp_m["total"] - 1))); k0b_max = float(np.max(np.abs(mine / comp_m["total"] - 1)))
P(f"K0b paper's MOND fit from its components (standard mu, a0 3000): median |dV/V| {k0b:.4f} (max {k0b_max:.4f}); line 0.02 -> {'PASS' if k0b < 0.02 else 'FAIL'}")
gas_same = float(np.max(np.abs(at(cm["gas"][:, 0], cm["gas"][:, 1], Xm, Ym, RT, 39.0) - comp["gas"])))
P(f"  gas curve, two figures (M/L-free): max |dV| {gas_same:.2f} km/s at Table radii")
mondT = {k: at(cm[k][:, 0], cm[k][:, 1], Xm, Ym, RT, 39.0) for k in ("gas", "lsb", "hsb", "total")}
cpm, ppm = chi2p(VT, ET, mondT["total"])
P(f"  paper's MOND fit vs Table 3 (reported): {np.round(mondT['total'],1).tolist()} chi2 {cpm:.1f}/4 (HSB M/L fitted by the paper)")
R["K0b"] = dict(median=k0b, max=k0b_max, gas_two_figs=gas_same, paper_mond_chi2=cpm)
R["mond2comp"] = {k: v.tolist() for k, v in mondT.items()}

# ---- grade
vb2 = comp["gas"] ** 2 + comp["lsb"] ** 2 + comp["hsb"] ** 2
fh = comp["hsb"] ** 2 / vb2; outer = fh < 0.10
P(f"\nV_bar (DecoHL, HSB 3.3, LSB 0.9) at Table radii: {np.round(np.sqrt(vb2),1).tolist()}; HSB share of V_b^2 {np.round(fh,3).tolist()}")
gNa = vb2 / RT * CONV
P(f"g_N/a0 (canonical) at Table radii: {np.round(gNa/FOOT['canonical'],3).tolist()}")
P(f"outer-disc points (HSB < 10 % of V_b^2): {RT[outer].tolist()}")
P("\n=== GRADE at i0 = 38 deg, D_A 322 Mpc (published), M/L HSB 3.3, LSB 0.9" if MODE == "law" else "\n=== MUTATE nu = 1")
for f, a0 in FOOT.items():
    m = law_v(vb2, RT, a0); c, p = chi2p(VT, ET, m)
    row = dict(a0=a0, Vlaw=m.tolist(), chi2=c, p=p, label=label(p))
    if outer.sum():
        co, po = chi2p(VT[outer], ET[outer], m[outer]); row["outer"] = dict(chi2=co, p=po, n=int(outer.sum()), label=label(po))
    else:
        row["outer"] = None
    ends = {}
    for hn, hs in [("hsb_x0.5", 0.5), ("hsb_x2", 2.0)]:
        for ln, ls in [("lsb0.9", 1.0), ("lsb0.5", 0.5 / 0.9)]:
            vv = comp["gas"] ** 2 + ls * comp["lsb"] ** 2 + hs * comp["hsb"] ** 2
            ends[hn + "_" + ln] = chi2p(VT, ET, law_v(vv, RT, a0))[0]
    vv = mondT["gas"] ** 2 + mondT["lsb"] ** 2 + mondT["hsb"] ** 2
    ends["mond2comp_components_3.7_0.5"] = chi2p(VT, ET, law_v(vv, RT, a0))[0]
    row["ends_chi2"] = ends
    sc = []
    for i in np.arange(5.0, 90.0001, 0.1):
        s_ = np.sin(np.radians(I0)) / np.sin(np.radians(i)); sc.append((round(i, 1),) + chi2p(VT * s_, ET * s_, m))
    sc = np.array(sc); ok = sc[sc[:, 2] >= 0.05, 0]; lo, hi = I0 - 2 * SIG_I, I0 + 2 * SIG_I
    resc = len(ok) > 0 and ok.max() >= lo and ok.min() <= hi
    row["scan"] = dict(i_best=float(sc[np.argmin(sc[:, 1]), 0]), p_ok_range=[float(ok.min()), float(ok.max())] if len(ok) else None,
                       rescue="RESCUED WITHIN ERRORS" if resc else "NOT RESCUED")
    row["EFE"] = {str(ge): chi2p(VT, ET, law_v(vb2, RT, a0, ge))[0] for ge in (0.01, 0.03)}
    R[f] = row
    P(f"[{f}] a0 {a0:.4e}: V_law {np.round(m,1).tolist()} vs {VT.tolist()}  chi2 {c:.1f}/4 p {p:.2e} -> {row['label']}")
    if row["outer"]: P(f"   outer disc ({row['outer']['n']} pts): chi2 {row['outer']['chi2']:.1f} p {row['outer']['p']:.2e} -> {row['outer']['label']}")
    P(f"   M/L ends chi2: " + ", ".join(f"{k} {v:.1f}" for k, v in ends.items()))
    P(f"   scan: i_best {row['scan']['i_best']:.1f}, p>=0.05 for {row['scan']['p_ok_range']} vs [{lo:.0f},{hi:.0f}] -> {row['scan']['rescue']}")
    P(f"   EFE (assumed): ge 0.01 chi2 {row['EFE']['0.01']:.1f}, ge 0.03 chi2 {row['EFE']['0.03']:.1f}")
cN, pN = chi2p(VT, ET, np.sqrt(vb2)); R["newton_baryons"] = dict(chi2=cN, p=pN)
P(f"Newtonian baryons alone (reported): {np.round(np.sqrt(vb2),1).tolist()} chi2 {cN:.1f}/4")

src = open(os.path.abspath(__file__)).read()
bad = [w_ for w_ in ("curve_fit", "minimize(", "least_squares", "leastsq", "emcee") if w_ in src.replace('"curve_fit", "minimize(", "least_squares", "leastsq", "emcee"', "")]
P(f"K1 optimiser grep: {bad if bad else 'none'} -> {'PASS' if not bad else 'FAIL'}")
name = "ud2_MUTATE" if MODE == "MUTATE" else "ud2"
json.dump(R, open(os.path.join(HERE, name + ".json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
