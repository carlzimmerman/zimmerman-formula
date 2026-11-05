"""UD1: the a0 law on AGC 114905 (FROZEN_CRITERIA.md + AMENDMENTS.md A1, A2).

Inputs are the authors' own vector figures from the arXiv sources (inputs/); points are read as exact path
coordinates, calibrated on the tick marks. Baryons are built from Mancera Pina+2024's published functional forms.
Law: g = nu(g_b/a0) g_b, nu(y) = 1/2 + sqrt(1/4 + 1/y). Both footings, never pooled. kappa = 1/2 FITTED; not theory
closed. One galaxy excludes nothing.

usage: python3 ud1.py [law|MUTATE]   (MUTATE sets nu = 1; outputs go to ud1_MUTATE.*)
"""
import json, os, sys
import numpy as np
import fitz
from scipy.special import ellipk
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else "law"
INP = os.path.join(HERE, "inputs")
G = 4.30091e-6                      # kpc (km/s)^2 / Msun
CONV = 1e6 / 3.0857e19              # (km/s)^2/kpc -> m/s^2
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10)
A0_PAPER = 1.2e-10                  # used only to reproduce the paper's plotted MOND curve (K0b, K0c)
I0, SIG_I, D0 = 31.0, 2.0, 78.7     # 2024 fiducial
OUT = []


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)


def nu(y):
    if MODE == "MUTATE":
        return np.ones_like(np.asarray(y, float))
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_paper(y):                    # Gentile+2008 form = this nu; never mutated (it reproduces the paper's figure)
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)


# ------------------------------------------------------------------ vector-figure reading
def drawings(path):
    p = fitz.open(path)[0]; out = []
    for d in p.get_drawings():
        pts = []
        for it in d["items"]:
            for q in it[1:]:
                if hasattr(q, "x"): pts.append((q.x, q.y))
                elif hasattr(q, "x0"): pts += [(q.x0, q.y0), (q.x1, q.y1)]
        out.append(dict(k="".join(i[0] for i in d["items"]), n=len(d["items"]), pts=np.array(pts),
                        col=tuple(round(c, 2) for c in d["color"]) if d.get("color") else None,
                        fill=tuple(round(c, 2) for c in d["fill"]) if d.get("fill") else None,
                        sop=d.get("stroke_opacity")))
    words = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip(); x0, y0, x1, y1 = l["bbox"]
            words.append((t, 0.5 * (x0 + x1), 0.5 * (y0 + y1)))
    return out, words


def axis(words, dr, vals, which, box):
    """Linear map from tick labels: label centre snapped to the nearest major tick mark (black 1-segment line)."""
    x0, x1, y0, y1 = box; pairs = []
    ticks = [d for d in dr if d["k"] == "l" and d["n"] == 1 and d["col"] == (0.0, 0.0, 0.0) and len(d["pts"]) == 2]
    for v in vals:
        cands = [(t, x, y) for t, x, y in words if t == v and x0 <= x <= x1 and y0 <= y <= y1]
        if len(cands) != 1: raise SystemExit(f"axis label {v!r} not unique in box: {cands}")
        _, x, y = cands[0]
        if which == "x":
            tx = [d["pts"][0, 0] for d in ticks if abs(d["pts"][0, 0] - d["pts"][1, 0]) < 1e-6 and abs(d["pts"][0, 0] - x) < 3]
            pairs.append((float(v), min(tx, key=lambda q: abs(q - x)) if tx else x))
        else:
            ty = [d["pts"][0, 1] for d in ticks if abs(d["pts"][0, 1] - d["pts"][1, 1]) < 1e-6 and abs(d["pts"][0, 1] - y) < 3]
            pairs.append((float(v), min(ty, key=lambda q: abs(q - y)) if ty else y))
    v, c = np.array(pairs).T; m, b = np.polyfit(c, v, 1)
    res = np.max(np.abs(m * c + b - v)); return (lambda q: m * np.asarray(q) + b), res


def markers(dr, fill, sop=1.0, xmin=-1e9, xmax=1e9):
    """Filled-circle markers ('cccc', 8 curves); returns centres. Legend marker dropped by the caller's x-window."""
    c = [d["pts"].mean(axis=0) for d in dr if d["k"].startswith("cccc") and d["fill"] == fill
         and (d["sop"] or 1.0) == sop and xmin < d["pts"][:, 0].mean() < xmax]
    return np.array(sorted([tuple(q) for q in c]))


def errbars(dr, col, xs, sop=1.0):
    """Vertical error-bar stem per marker x: the no-fill 1-segment line of that colour at that x."""
    out = []
    for x in xs:
        st = [d for d in dr if d["k"] == "l" and d["n"] == 1 and d["col"] == col and d["fill"] is None
              and (d["sop"] or 1.0) == sop and len(d["pts"]) == 2
              and abs(d["pts"][0, 0] - x) < 0.05 and abs(d["pts"][1, 0] - x) < 0.05 and abs(d["pts"][0, 1] - d["pts"][1, 1]) > 0.5]
        if len(st) != 1: raise SystemExit(f"error bar at x={x}: {len(st)} candidates")
        out.append((st[0]["pts"][:, 1].min(), st[0]["pts"][:, 1].max()))
    return np.array(out)


def curve(dr, col, nmin, sop=1.0):
    c = [d for d in dr if d["col"] == col and d["n"] >= nmin and (d["sop"] or 1.0) == sop]
    if len(c) != 1: raise SystemExit(f"curve {col}: {len(c)} candidates")
    return c[0]["pts"]


# ------------------------------------------------------------------ baryons (Mancera Pina+2024 functional forms)
def as2kpc(D): return D * 1e3 * np.pi / 648000.0


def sig_star(R_as):   # Msun/pc^2, R in arcsec, at the authors' fiducial inclination
    c = [0.5576, -0.1126, 0.0085, -0.0002]
    return 3.6703 * np.exp(-R_as / 3.6155) * (1 + sum(ci * R_as ** (k + 1) for k, ci in enumerate(c)))


def sig_gas(R_as):
    return 3.953 * np.exp(-R_as / 0.676) * (1 + R_as / 375.220) ** 559.231


def vc2_thick(Rk, sigma_fn, vert, zscale, D, amax_as=80.0):
    """Midplane V^2 = R dPhi/dR of an axisymmetric disc, Sigma(a) [Msun/pc^2, a in arcsec] x h(z), by ring sums."""
    k = as2kpc(D)
    a = (np.arange(4000) + 0.5) * (amax_as / 4000.0) * k                  # kpc, midpoint grid
    da = a[1] - a[0]
    S = np.clip(sigma_fn(a / k), 0, None) * 1e6                           # Msun/kpc^2
    zmax = 8.0 * zscale; nz = 240
    z = (np.arange(nz) + 0.5) * (zmax / nz); dz = z[1] - z[0]
    if vert == "sech2": h = 1.0 / np.cosh(z / zscale) ** 2 / (2 * zscale)
    else: h = np.exp(-0.5 * (z / zscale) ** 2) / (np.sqrt(2 * np.pi) * zscale)
    h = h / (2 * np.sum(h) * dz)                                           # both sides, unit integral
    m = (2 * np.pi * a * S * da)[:, None] * (2 * h * dz)[None, :]         # Msun per (ring, |z| layer)

    def phi(R):
        s2 = (R + a[:, None]) ** 2 + z[None, :] ** 2; kk = np.clip(4 * a[:, None] * R / s2, 0, 1 - 1e-12)
        return -np.sum(2 * G * m / np.pi * ellipk(kk) / np.sqrt(s2))
    out = []
    for R in np.atleast_1d(Rk):
        e = 1e-3 * max(R, 0.05); out.append(R * (phi(R + e) - phi(R - e)) / (2 * e))
    return np.array(out), float(np.sum(m))


def zd_star(): return 0.196 * (2.80 / 1.678) ** 0.633                     # kpc (Bershady relation, R_e 2.80 kpc)


def baryons(Rk, D, i, mstar_scale=1.0):
    """V_*^2, V_gas^2 at kpc radii for distance D, inclination i (Sigma x cos i / cos i0, A2)."""
    f = np.cos(np.radians(i)) / np.cos(np.radians(I0))
    vs2, ms = vc2_thick(Rk, lambda q: mstar_scale * f * sig_star(q), "sech2", zd_star(), D)
    vg2, mg = vc2_thick(Rk, lambda q: f * sig_gas(q), "gauss", 1.3, D)
    return vs2, vg2, ms, mg


def law_v(vb2, R, a0, ge=0.0):
    gN = vb2 / R * CONV
    if ge == 0.0: g = nu(gN / a0) * gN
    else:
        gt = gN + ge * a0; g = nu(gt / a0) * gt - nu(ge) * ge * a0
    return np.sqrt(np.maximum(g / CONV * R, 0))


def chi2p(v, e, m): c = float(np.sum(((v - m) / e) ** 2)); return c, float(CHI2.sf(c, len(v)))


def label(p): return "CONSISTENT" if p >= 0.05 else ("FAIL" if p < 0.01 else "TENSION")


# ------------------------------------------------------------------ main
R = {}
P(f"UD1 AGC 114905, mode {MODE}. kappa = 1/2 FITTED; not theory closed; footings never pooled; one galaxy excludes nothing.")

# K0 unit test of the ring-sum potential: thin exponential disc vs Freeman
from scipy.special import i0 as I0f, i1 as I1f, k0 as K0f, k1 as K1f
Rd_t = 2.0; Dt = 10.0; kt = as2kpc(Dt); Mt = 1e9
sig_t = lambda q: Mt / (2 * np.pi * (Rd_t * 1e3) ** 2) * np.exp(-q * kt / Rd_t)
Rt = np.array([1.0, 2.0, 4.0, 8.0]); yv = Rt / (2 * Rd_t)
vfree = 2 * G * Mt / Rd_t * yv ** 2 * (I0f(yv) * K0f(yv) - I1f(yv) * K1f(yv))
vnum, _ = vc2_thick(Rt, sig_t, "gauss", 0.01, Dt, amax_as=40 * Rd_t / kt)
k0z = float(np.max(np.abs(np.sqrt(vnum / vfree) - 1)))
P(f"K0z ring-sum vs Freeman thin disc: max |dV/V| = {k0z:.4f} (line 0.01) -> {'PASS' if k0z < 0.01 else 'FAIL'}")
R["K0z"] = k0z

# ---- data: plot_mond.pdf (V_circ at i = 31, D = 78.7) and the paper's MOND curve
dr, w = drawings(os.path.join(INP, "plot_mond.pdf"))
X, rx = axis(w, dr, ["0", "2", "4", "6", "8", "10"], "x", (40, 470, 315, 330))
Y, ry = axis(w, dr, ["0", "20", "40", "60", "80"], "y", (30, 57, 20, 330))
GREY = (0.5, 0.5, 0.5)
mk = markers(dr, GREY, 1.0, xmin=90)
eb = errbars(dr, GREY, mk[:, 0])
Rk = X(mk[:, 0]); V = Y(mk[:, 1]); E = 0.5 * (Y(eb[:, 0]) - Y(eb[:, 1]))
mk12 = markers(dr, GREY, 0.4000000059604645, xmin=90)
V12 = Y(mk12[:, 1]) if len(mk12) else None
red = curve(dr, (1.0, 0.0, 0.0), 40, 1.0); red_R = X(red[:, 0]); red_V = Y(red[:, 1])
P(f"axis fit residual x {rx:.2e} kpc, y {ry:.2e} km/s")
for r, v, e in zip(Rk, V, E): P(f"  R {r:6.3f} kpc  V_circ {v:6.2f} +- {e:5.2f} km/s")
R["data2024"] = dict(R=Rk.tolist(), V=V.tolist(), E=E.tolist(), V_i12=None if V12 is None else V12.tolist())

# ---- V_rot from plot_kinematics.pdf right panel (top axis kpc)
drk, wk = drawings(os.path.join(INP, "plot_kinematics.pdf"))
Xk, rxk = axis(wk, drk, ["0.0", "2.5", "5.0", "7.5", "10.0"], "x", (640, 1000, 15, 45))
Yk, ryk = axis(wk, drk, ["0", "5", "10", "15", "20", "25", "30"], "y", (640, 664, 40, 360))
RED_K = (0.7, 0.13, 0.13)
mkc = markers(drk, GREY, 1.0, xmin=690); mkr = markers(drk, RED_K, 1.0, xmin=690)
mkc = mkc[Xk(mkc[:, 0]) > 1.0]; mkr = mkr[Xk(mkr[:, 0]) > 1.0]          # drop the legend marker (upper left)
Vc_k = Yk(mkc[:, 1]); Vr_k = Yk(mkr[:, 1]); Rk_k = Xk(mkc[:, 0])
P(f"kinematics panel: axis residual x {rxk:.2e}, y {ryk:.2e}; R {np.round(Rk_k,3).tolist()}")
P(f"  V_circ {np.round(Vc_k,2).tolist()}  V_rot {np.round(Vr_k,2).tolist()}")
dVc = float(np.max(np.abs(Vc_k - V)))
P(f"  cross-figure V_circ agreement: max |dV| = {dVc:.2f} km/s")
AD2 = Vc_k ** 2 - Vr_k ** 2
R["kin"] = dict(R=Rk_k.tolist(), Vc=Vc_k.tolist(), Vrot=Vr_k.tolist(), AD2=AD2.tolist(), dVc_max=dVc)

# ---- baryons at fiducial
vs2, vg2, ms, mg = baryons(Rk, D0, I0)
vb2 = vs2 + vg2
P(f"baryons at D {D0}, i {I0}: M_* {ms:.3e} (paper 9e7 within 10.9 kpc), M_gas {mg:.3e} (paper 1.33 M_HI = {1.47e9-9e7:.3e})")
for r, a, b in zip(Rk, np.sqrt(vs2), np.sqrt(vg2)): P(f"  R {r:6.3f}  V_* {a:6.2f}  V_gas {b:6.2f}  V_bar {np.hypot(a,b):6.2f}")
R["baryons"] = dict(Mstar=ms, Mgas=mg, Vstar=np.sqrt(vs2).tolist(), Vgas=np.sqrt(vg2).tolist())

# ---- K0a: plotted baryon curves in plot_mm_noDM.pdf (D 80.27, i 35.86)
drn, wn = drawings(os.path.join(INP, "plot_mm_noDM.pdf"))
Xn, _ = axis(wn, drn, ["0", "2", "4", "6", "8", "10"], "x", (40, 470, 303, 320))
Yn, _ = axis(wn, drn, ["0", "10", "20", "30", "40", "50"], "y", (30, 58, 0, 320))
k0a = {}
for name, col, n in [("stars", (1.0, 0.55, 0.0), 25), ("gas", (0.12, 0.56, 1.0), 20), ("sum", (1.0, 0.0, 0.0), 30)]:
    c = curve(drn, col, n); rr = Xn(c[:, 0]); vv = Yn(c[:, 1]); sel = (rr > 0.5) & (rr < 10.5)
    rr, vv = rr[sel][::2], vv[sel][::2]
    a2, b2, _, _ = baryons(rr, 80.27, 35.86)
    mine = np.sqrt({"stars": a2, "gas": b2, "sum": a2 + b2}[name])
    dev = np.abs(mine / vv - 1); k0a[name] = float(np.median(dev)); k0a[name + "_max"] = float(np.max(dev))
P(f"K0a plotted baryons (D 80.27, i 35.86): median |dV/V| stars {k0a['stars']:.3f}, gas {k0a['gas']:.3f}, sum {k0a['sum']:.3f}"
  f" (max {k0a['stars_max']:.3f}/{k0a['gas_max']:.3f}/{k0a['sum_max']:.3f}); line 0.03 on the median -> "
  f"{'PASS' if max(k0a['stars'], k0a['gas'], k0a['sum']) < 0.03 else 'FAIL'}")
R["K0a"] = k0a

# ---- K0b: the paper's plotted MOND curve (a0 1.2e-10) from my baryons
sel = (red_R > 0.5) & (red_R < 10.5); rr, vv = red_R[sel][::2], red_V[sel][::2]
a2, b2, _, _ = baryons(rr, D0, I0)
gN = (a2 + b2) / rr * CONV; mine = np.sqrt(nu_paper(gN / A0_PAPER) * gN / CONV * rr)
k0b = float(np.median(np.abs(mine / vv - 1))); k0b_max = float(np.max(np.abs(mine / vv - 1)))
P(f"K0b paper's MOND curve: median |dV/V| {k0b:.3f} (max {k0b_max:.3f}); line 0.03 -> {'PASS' if k0b < 0.03 else 'FAIL'}")
R["K0b"] = dict(median=k0b, max=k0b_max)


def scan(a0, nu_f, variant):
    """chi2 vs inclination. frozen: V and E x sin i0/sin i, baryons fixed. paper: V_rot rescaled, AD kept, Sigma x cos i."""
    out = []
    for i in np.arange(5.0, 90.0001, 0.1):
        s = np.sin(np.radians(I0)) / np.sin(np.radians(i))
        if variant == "frozen":
            v, e, b2 = V * s, E * s, vb2
        else:
            vr = np.sqrt(np.maximum(V ** 2 - AD2, 0)) * s; v = np.sqrt(vr ** 2 + AD2); e = E * v / V
            b2 = vb2 * np.cos(np.radians(i)) / np.cos(np.radians(I0))   # Sigma x cos i / cos i0 is linear in V_b^2
        gN = b2 / Rk * CONV; m = np.sqrt(nu_f(gN / a0) * gN / CONV * Rk)
        out.append((round(i, 1),) + chi2p(v, e, m))
    return np.array(out)


# ---- K0c: paper's 'i ~ 12 deg' statement, paper-consistent variant, paper a0
sc = scan(A0_PAPER, nu_paper, "paper"); ib = float(sc[np.argmin(sc[:, 1]), 0])
P(f"K0c paper-consistent scan at a0 1.2e-10: best i = {ib:.1f} deg (paper: 12; line +-2) -> {'PASS' if abs(ib-12) <= 2 else 'FAIL'}")
if V12 is not None:
    s = np.sin(np.radians(I0)) / np.sin(np.radians(12.0))
    v12 = np.sqrt(np.maximum(V ** 2 - AD2, 0) * s ** 2 + AD2)
    P(f"  paper's plotted i=12 points {np.round(V12,2).tolist()} vs my rescaling {np.round(v12,2).tolist()}")
R["K0c"] = dict(i_best=ib)

# ---- grade, per footing
P("\n=== GRADE at published i0 = 31 deg, D 78.7 Mpc, published M* (law, nu = 1/2 + sqrt(1/4 + 1/y))" if MODE == "law" else "\n=== MUTATE nu = 1")
for f, a0 in FOOT.items():
    m = law_v(vb2, Rk, a0); c, p = chi2p(V, E, m)
    row = dict(a0=a0, Vlaw=m.tolist(), chi2=c, p=p, label=label(p))
    for sname, sc_ in [("Mstar_minus1s", 8 / 9), ("Mstar_plus1s", 10 / 9)]:
        a_, b_, _, _ = baryons(Rk, D0, I0, sc_); cc, pp = chi2p(V, E, law_v(a_ + b_, Rk, a0)); row[sname] = dict(chi2=cc, p=pp)
    sf = scan(a0, nu, "frozen"); ok = sf[sf[:, 2] >= 0.05, 0]
    ibf = float(sf[np.argmin(sf[:, 1]), 0]); lo, hi = I0 - 2 * SIG_I, I0 + 2 * SIG_I
    resc = (len(ok) > 0) and (ok.max() >= lo) and (ok.min() <= hi)
    row["scan_frozen"] = dict(i_best=ibf, chi2_best=float(sf[:, 1].min()), p_ok_range=[float(ok.min()), float(ok.max())] if len(ok) else None,
                              rescue="RESCUED WITHIN ERRORS" if resc else "NOT RESCUED",
                              sigma_from_i0=float((I0 - (ok.max() if len(ok) else ibf)) / SIG_I))
    sp = scan(a0, nu, "paper"); okp = sp[sp[:, 2] >= 0.05, 0]
    row["scan_paper_variant"] = dict(i_best=float(sp[np.argmin(sp[:, 1]), 0]),
                                     p_ok_range=[float(okp.min()), float(okp.max())] if len(okp) else None)
    row["EFE"] = {str(ge): dict(zip(("chi2", "p"), chi2p(V, E, law_v(vb2, Rk, a0, ge)))) for ge in (0.01, 0.03)}
    R[f] = row
    P(f"[{f}] a0 {a0:.4e}: V_law {np.round(m,2).tolist()}  chi2 {c:.1f}/5  p {p:.2e} -> {row['label']}")
    P(f"   M* -1s chi2 {row['Mstar_minus1s']['chi2']:.1f}, +1s {row['Mstar_plus1s']['chi2']:.1f}")
    P(f"   frozen scan: i_best {ibf:.1f}, p>=0.05 for i in {row['scan_frozen']['p_ok_range']} vs i0+-2s [{lo:.0f},{hi:.0f}] -> "
      f"{row['scan_frozen']['rescue']} ({row['scan_frozen']['sigma_from_i0']:.1f} sigma_i below i0)")
    P(f"   paper-variant scan (reported): i_best {row['scan_paper_variant']['i_best']:.1f}, p>=0.05 for {row['scan_paper_variant']['p_ok_range']}")
    P(f"   EFE (assumed, reported): ge 0.01 chi2 {row['EFE']['0.01']['chi2']:.1f}, ge 0.03 chi2 {row['EFE']['0.03']['chi2']:.1f}")

# ---- Newtonian baryons, reported (also the MUTATE comparison)
cN, pN = chi2p(V, E, np.sqrt(vb2)); R["newton_baryons"] = dict(chi2=cN, p=pN)
P(f"Newtonian baryons alone at i0 (reported): chi2 {cN:.1f}/5 p {pN:.2e}")

# ---- secondary: 2022 figure (i0 32 +- 3, D 76), baryons from 2024 forms (A1); never pooled
d2, w2 = drawings(os.path.join(INP, "vcvdisp_fixed.pdf"))
X2, _ = axis(w2, d2, ["0", "2", "4", "6", "8", "10"], "x", (40, 470, 303, 320))
Y2, _ = axis(w2, d2, ["0", "5", "10", "15", "20", "25", "30"], "y", (30, 53, 0, 320))
S9 = 0.8999999761581421
m2 = markers(d2, GREY, S9, xmin=0); m2 = m2[X2(m2[:, 0]) > 0.3]
def has_stem(x):
    return any(d["k"] == "l" and d["n"] == 1 and d["col"] == GREY and d["fill"] is None and (d["sop"] or 1.0) == S9
               and len(d["pts"]) == 2 and abs(d["pts"][0, 0] - x) < 0.05 and abs(d["pts"][0, 1] - d["pts"][1, 1]) > 0.5 for d in d2)
m2 = m2[[has_stem(x) for x, _ in m2]]                                         # the legend marker has no error bar
e2 = errbars(d2, GREY, m2[:, 0], S9)
R2, V2, E2 = X2(m2[:, 0]), Y2(m2[:, 1]), 0.5 * (Y2(e2[:, 0]) - Y2(e2[:, 1]))
I2, SI2 = 32.0, 3.0
a_, b_, _, _ = baryons(R2 * D0 / 76.0, D0, I0)                               # Sigma(arcsec) fixed: build at the 2024 D, rescale
vb2_2 = (a_ + b_) * (76.0 / D0) * np.cos(np.radians(I2)) / np.cos(np.radians(I0))
P("\n=== SECONDARY 2022 (i0 32 +- 3, D 76 Mpc; V_c errors include the inclination MC per the paper; baryons from 2024 forms)")
for r, v, e in zip(R2, V2, E2): P(f"  R {r:6.3f} kpc  V_c {v:6.2f} +- {e:5.2f}")
R["sec2022"] = dict(R=R2.tolist(), V=V2.tolist(), E=E2.tolist())
for f, a0 in FOOT.items():
    m = law_v(vb2_2, R2, a0); c, p = chi2p(V2, E2, m)
    sc2 = []
    for i in np.arange(5.0, 90.0001, 0.1):
        s_ = np.sin(np.radians(I2)) / np.sin(np.radians(i)); sc2.append((round(i, 1),) + chi2p(V2 * s_, E2 * s_, m))
    sc2 = np.array(sc2); ok = sc2[sc2[:, 2] >= 0.05, 0]
    resc = (len(ok) > 0) and ok.max() >= I2 - 2 * SI2 and ok.min() <= I2 + 2 * SI2
    R["sec2022"][f] = dict(chi2=c, p=p, label=label(p), p_ok_range=[float(ok.min()), float(ok.max())] if len(ok) else None,
                           rescue="RESCUED WITHIN ERRORS" if resc else "NOT RESCUED")
    P(f"[{f}] chi2 {c:.1f}/{len(V2)} p {p:.2e} -> {label(p)}; frozen scan p>=0.05 for {R['sec2022'][f]['p_ok_range']} vs [{I2-2*SI2:.0f},{I2+2*SI2:.0f}] -> {R['sec2022'][f]['rescue']}")

# ---- K1: no fitted M/L, a0 or distance (grep this file for optimisers)
src = open(os.path.abspath(__file__)).read()
bad = [w_ for w_ in ("curve_fit", "minimize(", "least_squares", "leastsq", "emcee") if w_ in src.replace('"curve_fit", "minimize(", "least_squares", "leastsq", "emcee"', "")]
P(f"K1 optimiser grep: {bad if bad else 'none'} -> {'PASS' if not bad else 'FAIL'}")

name = "ud1_MUTATE" if MODE == "MUTATE" else "ud1"
json.dump(R, open(os.path.join(HERE, name + ".json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
