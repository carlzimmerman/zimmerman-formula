#!/usr/bin/env python3
"""Combined a0(z) chart, 2026-09-30.  PLOT ONLY: it reads the committed results JSONs of CFG223 (the four laws' curves and the RC100 / CRISTAL points), CFG229 (the seven class-M galaxies) and CFG228 (the six ALPINE [CII]
rotators and SPT0418-47) and draws them on one set of axes.  No fit, no estimator, no new number: every plotted value is a key of one of the three JSONs (chart_a0z_points.csv lists them all), apart from
the trivial unit conversion to m/s^2 on the secondary axis and the quoted z ~ 0 footings.
Descriptive compilation; calibration-limited; not a verdict.  LambdaCDM has no a0: the purple curve is an effective-a0 PROXY.  kappa = 1/2 is FITTED.
Marker SHAPE = the gas class of the record: circle = class D (baryon masses fitted with the dynamics or a scaling prior: RC100, CRISTAL fit route), square = class S/L (one or two UN-optimised tracers: CRISTAL independent
route, ALPINE, SPT0418-47), star = class M (Dunne+22 per-galaxy optimised multi-tracer gas).  Statistical bars (68% thick, 95% thin, over the Monte Carlo or bootstrap draws that have a root) and systematic bars
(shaded, inner dark / outer light) are separate styles.
Run:  python3 campaign_fresh_gravity/CHART_a0z_combined_2026-09-30/chart_a0z_combined.py        (MUTATE=1: two plotted values are swapped and the tie-to-JSON check must trip; no figure written)"""
import os, sys, json, math, csv, textwrap
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.gridspec import GridSpec

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
MUT = os.environ.pop("MUTATE", "").strip() == "1"
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
J229 = json.load(open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score_results.json")))
J228 = json.load(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_score_results.json")))
OUT, CHK = [], []


def P(s=""):
    OUT.append(s); print(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


A0 = 9.3603e-11                      # canonical footing (CFG4_common.A0; the unit of every ratio here)
ALT = J228["alt_over_can"]           # 1.1312e-10 / 9.3603e-11, from the JSON
Q_NU, Q_P2 = 1.37e-10 / A0, 1.78e-10 / A0   # the record's SPARC best free fits at Upsilon = 0.50 (CFG4_README H2b, quoted; no SPARC analysis here)
cur = J223["curves"]; Z = np.array(cur["z"])
FLOOR, CEIL = 0.04, 30.0
COL = {"FLAT": "#222222", "PROXY": "#7b2cbf", "H(z)": "#d62828", "M-DEC": "#1b9aaa"}
C_RC, C_CR, C_M, C_AL = "#1d4e89", "#e07b00", "#8a5a00", "#2e7d32"
CLS = {"D": ("o", 9.5), "S/L": ("s", 9.0), "M": ("*", 17)}


# ------------------------------------------------------------------ the objects to plot (read from the JSONs only)
def band223(r, t):
    b = {float(k): v for k, v in r["bands"].items()}; nr = {float(k): v for k, v in r["band_noroot"].items()}
    return dict(lo=min(b[t], b[-t]), hi=max(b[t], b[-t]), noroot=bool(nr[t] or nr[-t]))


def band_lane(r, tag):
    m, p = r["corners"][f"joint -{tag}"], r["corners"][f"joint +{tag}"]
    have = [10 ** v[0] for v in (m, p) if not v[1]]
    return dict(lo=min(have), hi=max(have), noroot=bool(m[1] or p[1])) if have else dict(lo=None, hi=None, noroot=True)


OBJ = []
for r in J223["points"]:
    if not r["fig"]:
        continue
    col = C_RC if r["dataset"] == "RC100" else C_CR
    cls = "D" if (r["dataset"] == "RC100" or r["route"] == "fit") else "S/L"
    dx = {"CR R_e fit": -0.10, "CR R_out fit": -0.035, "CR R_e ind": 0.035, "CR R_out ind": 0.10}.get(r["short"], 0.0) * 1.6
    OBJ.append(dict(lane="CFG223", id=r["short"], cls=cls, col=col, z=r["z_med"], zdisp=r["z_med"] + dx, zspan=(r["z_min"], r["z_max"]) if r["dataset"] == "RC100" else None,
                    noroot=False, s=r["s"], st68=(r["lo68"], r["hi68"]), st95=(r["lo95"], r["hi95"]), open_low=r["unb_frac"] > 0.05,
                    inner=band223(r, 0.15), outer=band223(r, 0.30), bands_name="baryon mass +-0.15 / +-0.30 dex", n=r["n"]))


def lane_objs(J, lane, cls_of, col, zdisp):
    gid, zz = J["gid"], J["z"]
    for g, z in zip(gid, zz):
        r = J["IMPL"][g]; nr = bool(r["s0"][1]); q = r["stat"]["q"]
        o = dict(lane=lane, id=g, cls=cls_of(g), col=col, z=z, zdisp=zdisp.get(g, z), zspan=None, noroot=nr, s=None if nr else 10 ** r["s0"][0], open_low=False, n=1)
        if not nr:
            o.update(st68=(10 ** q[1], 10 ** q[3]), st95=(10 ** q[0], 10 ** q[4]), inner=band_lane(r, "inner"), outer=band_lane(r, "outer"), bands_name="joint class bands on gas and stars")
        OBJ.append(o)


ZD229 = {"ALESS_122.1": 2.10, "SINS_BX610": 2.18, "ALPAKA15": 2.33, "ALPAKA18": 2.43, "ALPAKA19": 2.53, "ALPAKA20": 2.63, "ALPAKA22": 2.93}
ZD228 = {"SPT0418-47": 4.20, "CG32": 4.33, "DC396844": 4.43, "VC5110377875": 4.52, "DC881725": 4.75, "DC552206": 5.55, "DC494057": 5.68}
lane_objs(J229, "CFG229", lambda g: "M", C_M, ZD229)
lane_objs(J228, "CFG228", lambda g: "S/L", C_AL, ZD228)
# the pooled ALPINE6 set (median rule), drawn as one more object beside the galaxies (same estimator as CFG223's sets)
rp = J228["IMPL"]["ALPINE6"]; qp = rp["stat"]["q"]; zg = sorted(z for g, z in zip(J228["gid"], J228["z"]) if g != "SPT0418-47")
OBJ.append(dict(lane="CFG228", id="ALPINE6 pooled", cls="S/L", col=C_AL, z=float(np.median(zg)), zdisp=4.64, zspan=(zg[0], zg[-1]), noroot=False, s=10 ** rp["s0"][0], st68=(10 ** qp[1], 10 ** qp[3]), st95=(10 ** qp[0], 10 ** qp[4]),
                open_low=False, inner=band_lane(rp, "inner"), outer=band_lane(rp, "outer"), bands_name="joint class bands on gas and stars", n=6, pooled=True))

P("CHART a0(z) combined -- plot only; reads cfg223_results.json, cfg229_score_results.json, cfg228_score_results.json (all committed); no new analysis")
P(f"unit: s = implied a0 / {A0:.4e} m/s^2 (canonical footing); alt footing = {ALT:.4f} x canonical; quoted z ~ 0 reference: canonical 1, alt {ALT:.3f}, SPARC best free fits at Upsilon = 0.50: nu_mono {Q_NU:.3f} (1.37e-10), P2 {Q_P2:.3f} (1.78e-10) [CFG4_README H2b, quoted]")
P(f"{'lane':7s} {'object':16s} {'class':4s} {'z':>7s} {'z shown':>8s} {'s*':>8s} {'a0 (1e-10)':>10s} {'68%':>17s} {'95%':>17s}  inner band          outer band")


def f2(v):
    return "-" if v is None else f"{v:.3g}"


for o in OBJ:
    if o["noroot"]:
        P(f"{o['lane']:7s} {o['id']:16s} {o['cls']:4s} {o['z']:7.3f} {o['zdisp']:8.3f}  NO ROOT (D <= 1: no a0 can make nu < 1)")
    else:
        ib, ob = o["inner"], o["outer"]
        P(f"{o['lane']:7s} {o['id']:16s} {o['cls']:4s} {o['z']:7.3f} {o['zdisp']:8.3f} {o['s']:8.3f} {o['s'] * A0 * 1e10:10.3f} {f2(o['st68'][0]):>8s}-{f2(o['st68'][1]):<8s} {f2(o['st95'][0]):>8s}-{f2(o['st95'][1]):<8s}  "
          f"{f2(ib['lo'])}-{f2(ib['hi'])}{' (no root at one corner)' if ib['noroot'] else ''}   {f2(ob['lo'])}-{f2(ob['hi'])}{' (no root at one corner)' if ob['noroot'] else ''}")

# ------------------------------------------------------------------ self-checks (they can fail; MUTATE=1 swaps two values and the tie-to-JSON check must trip)
P("\nCHECKS")
if MUT:
    i1 = next(i for i, o in enumerate(OBJ) if o["id"] == "CG32"); i2 = next(i for i, o in enumerate(OBJ) if o["id"] == "DC881725")
    OBJ[i1]["s"], OBJ[i2]["s"] = OBJ[i2]["s"], OBJ[i1]["s"]
    P("MUTATE = 1 (the plotted s* of CG32 and DC881725 swapped)")
by = {(o["lane"], o["id"]): o for o in OBJ}
tie = all(abs(by[("CFG228", g)]["s"] - 10 ** J228["IMPL"][g]["s0"][0]) < 1e-12 for g in J228["gid"] if not J228["IMPL"][g]["s0"][1])
check("every plotted CFG228 s* equals 10**s0 of its own JSON entry (tie to the JSON)", tie, tie != MUT)
check("CFG223: eight figure points (four RC100 z-quartiles, four CRISTAL)", sum(o["lane"] == "CFG223" for o in OBJ), sum(o["lane"] == "CFG223" for o in OBJ) == 8)
n229 = sum(o["lane"] == "CFG229" for o in OBJ); r229 = [o["id"] for o in OBJ if o["lane"] == "CFG229" and not o["noroot"]]
check("CFG229: seven class-M galaxies, six with no root, ALESS 122.1 the only one with a root (README bottom line 5)", f"{n229} objects, root: {r229}", n229 == 7 and r229 == ["ALESS_122.1"] and abs(by[("CFG229", "ALESS_122.1")]["s"] - 8.82) < 0.01)
r228 = [o["id"] for o in OBJ if o["lane"] == "CFG228" and not o["noroot"] and not o.get("pooled")]
want = dict(CG32=12.1, DC396844=6.77, DC494057=4.58, DC552206=2.02, DC881725=4.08)
hand = all(abs(by[("CFG228", g)]["s"] - v) / v < 0.005 for g, v in want.items())
check("CFG228: five galaxies with a root (s* 12.1, 6.77, 4.58, 2.02, 4.08 as in the README), VC5110377875 and SPT0418-47 without; ALPINE6 pooled 4.33", f"root: {r228}", hand and sorted(r228) == sorted(want) and abs(by[("CFG228", "ALPINE6 pooled")]["s"] - 4.33) < 0.01)
check("both lanes' results files are the real runs (mode = none)", f"{J229['mode']!r}, {J228['mode']!r}", J229["mode"] == "" and J228["mode"] == "")
check("the alt-footing ratio equals 1.1312e-10 / 9.3603e-11", f"{ALT:.5f}", abs(ALT - 1.1312e-10 / A0) < 1e-4)
check("every plotted displayed z lies within 0.20 of the true z (legibility nudges only)", f"max {max(abs(o['zdisp'] - o['z']) for o in OBJ):.3f}", max(abs(o['zdisp'] - o['z']) for o in OBJ) <= 0.20)
P(f"\n{sum(CHK)}/{len(CHK)} checks pass")
if MUT:
    open(os.path.join(HERE, "chart_a0z_combined_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)
if not all(CHK):
    open(os.path.join(HERE, "chart_a0z_combined_FAILED.out"), "w").write("\n".join(OUT) + "\n")
    raise SystemExit("a check failed; no figure written")

with open(os.path.join(HERE, "chart_a0z_points.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["lane", "object", "gas_class", "z", "z_shown", "no_root", "s_star", "a0_1e-10_m_s2", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi", "inner_lo", "inner_hi", "inner_noroot_corner", "outer_lo", "outer_hi", "outer_noroot_corner"])
    for o in OBJ:
        if o["noroot"]:
            w.writerow([o["lane"], o["id"], o["cls"], o["z"], o["zdisp"], 1] + [""] * 12)
        else:
            w.writerow([o["lane"], o["id"], o["cls"], o["z"], o["zdisp"], 0, o["s"], o["s"] * A0 * 1e10, o["st68"][0], o["st68"][1], o["st95"][0], o["st95"][1], o["inner"]["lo"], o["inner"]["hi"], int(o["inner"]["noroot"]),
                        o["outer"]["lo"], o["outer"]["hi"], int(o["outer"]["noroot"])])


# ------------------------------------------------------------------ drawing
def draw_curves(ax, zmax):
    sel = Z <= zmax + 1e-9
    lo = np.minimum.reduce([np.array(cur[f"DESI {k}"]) for k in J223["desi"]]); hi = np.maximum.reduce([np.array(cur[f"DESI {k}"]) for k in J223["desi"]])
    ax.fill_between(Z[sel], lo[sel], hi[sel], color=COL["M-DEC"], alpha=0.16, lw=0, zorder=1)
    for L, zc in (("FLAT", 99), ("PROXY", 5.0), ("H(z)", 99), ("M-DEC", 2.5)):
        y = np.array(cur[L]); a = Z <= zc + 1e-9; b = Z >= zc - 1e-9; lw = 2.4 if L != "FLAT" else 2.0
        ax.plot(Z[a & sel], y[a & sel], color=COL[L], lw=lw, zorder=3)
        if zc < 99:
            ax.plot(Z[b & sel], y[b & sel], color=COL[L], lw=lw, ls=(0, (1.2, 2.2)), zorder=3)


LOFF = {"CG32": (-5, 9, "right"), "DC396844": (7, 9, "left"), "ALPINE6 pooled": (-7, -17, "right"), "DC881725": (9, -3, "left"), "DC552206": (9, -4, "left"), "DC494057": (8, 7, "left"),
        "CR R_e fit": (-9, -14, "right"), "CR R_out fit": (-9, -13, "right"), "CR R_e ind": (8, 9, "left"), "CR R_out ind": (-9, -14, "right"), "ALESS_122.1": (11, 2, "left")}
BB = dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8)


def draw_obj(ax, o, floor, ceil, label=None, wide=True):
    x, c = o["zdisp"], o["col"]
    mk, ms = CLS[o["cls"]]
    if o["noroot"]:
        ax.plot([x], [floor * 1.12], marker="v", ms=9, color=c, mec="white", mew=0.8, ls="none", zorder=6)
        if label:
            ax.annotate(label, (x, floor * 1.12), textcoords="offset points", xytext=(0, 9), ha="center", va="bottom", rotation=90, fontsize=8, color=c, bbox=BB)
        return
    for bd, al, w in ((o["outer"], 0.12, 17), (o["inner"], 0.26, 9)):
        lo = floor if (bd["noroot"] or bd["lo"] is None) else max(bd["lo"], floor)
        ax.plot([x, x], [lo, min(bd["hi"] if bd["hi"] is not None else ceil, ceil)], color=c, alpha=al, lw=w, solid_capstyle="butt", zorder=2)
        if bd["noroot"]:
            ax.plot([x], [floor * 1.1], marker="v", ms=4.5 if w < 12 else 5.5, color=c, alpha=0.6 if w < 12 else 0.4, ls="none", zorder=2)
    if o["zspan"] is not None:
        ax.plot(list(o["zspan"]), [o["s"], o["s"]], color=c, lw=0.9, alpha=0.45, zorder=3)
    for (lo, hi), w in ((o["st95"], 1.1), (o["st68"], 3.6)):
        lo_d = floor if (o["open_low"] and w < 2) else max(lo, floor)
        ax.plot([x, x], [lo_d, min(hi, ceil)], color=c, lw=w, solid_capstyle="butt", zorder=4)
        if hi > ceil:
            ax.plot([x], [ceil / 1.07], marker="^", ms=5, color=c, ls="none", zorder=4)
        if lo < floor and not (o["open_low"] and w < 2):
            ax.plot([x], [floor * 1.07], marker="v", ms=5, color=c, ls="none", zorder=4)
        if o["open_low"] and w < 2:
            ax.plot([x], [floor * 1.07], marker="v", ms=5, color=c, ls="none", zorder=4)
    hollow = o.get("pooled", False)
    ax.plot([x], [o["s"]], marker=mk, ms=ms, mfc="white" if hollow else c, mec=c if hollow else "white", mew=2.0 if hollow else 1.0, ls="none", zorder=7)
    if label:
        dxp, dyp, ha = LOFF.get(o["id"], (9, 4, "left"))
        ax.annotate(label, (x, o["s"]), textcoords="offset points", xytext=(dxp, dyp), ha=ha, fontsize=8.3, color=c, zorder=9, bbox=BB)


def ticks(ax, vals):
    ax.set_yticks(vals); ax.set_yticklabels([str(v) for v in vals]); ax.minorticks_off()


fig = plt.figure(figsize=(18.5, 13.8))
gs = GridSpec(2, 2, figure=fig, width_ratios=[1.45, 1.0], wspace=0.14, hspace=0.26, left=0.06, right=0.94, top=0.93, bottom=0.40)
ax = fig.add_subplot(gs[:, 0]); bz1 = fig.add_subplot(gs[0, 1]); bz2 = fig.add_subplot(gs[1, 1])
SHORT = {"SINS_BX610": "BX610", "ALESS_122.1": "ALESS 122.1", "VC5110377875": "VC5110", "ALPINE6 pooled": "ALPINE6 pooled"}
names_on = {"CFG229", "CFG228"}
for a, (x0, x1), fl, zmax, name_it in ((ax, (0.0, 7.9), FLOOR, 6.0, False), (bz1, (0.5, 3.2), 0.1, 3.2, True), (bz2, (4.0, 5.95), 0.1, 6.0, True)):
    draw_curves(a, min(zmax, 6.0))
    for o in OBJ:
        if not (x0 - 0.2 <= o["zdisp"] <= x1 + 0.2):
            continue
        lab = None
        if name_it and o["lane"] in names_on:
            lab = SHORT.get(o["id"], o["id"])
        elif name_it and o["lane"] == "CFG223" and a is bz2:
            lab = {"CR R_e fit": "R_e (12)", "CR R_out fit": "R_out (6)", "CR R_e ind": "R_e ind. (6)", "CR R_out ind": "R_out ind. (6)"}.get(o["id"])
        draw_obj(a, o, fl, CEIL, label=lab)
    a.set_yscale("log"); a.set_ylim(fl, CEIL); a.set_xlim(x0, x1)
    a.grid(True, which="major", color="#bbbbbb", lw=0.6, alpha=0.6); a.tick_params(labelsize=11)
    a.set_xlabel("redshift z", fontsize=12)
    ticks(a, [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20] if a is ax else [0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
ax.set_ylabel(r"implied $a_0(z)\,/\,a_0(0)$   (ratio to the footing's local $a_0$ = 9.36e-11 m/s$^2$)", fontsize=12)
ax.set_title("full range", fontsize=12, loc="left"); bz1.set_title("zoom: RC100 and the class-M sample (z 0.5 to 3.2)", fontsize=11, loc="left"); bz2.set_title("zoom: CRISTAL and the ALMA sample (z 4.0 to 5.95)", fontsize=11, loc="left")
for a in (ax, bz1, bz2):
    sec = a.secondary_yaxis("right", functions=(lambda r: r * A0 * 1e10, lambda v: v / (A0 * 1e10)))
    sec.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20] if a is not ax else [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]); sec.set_yticklabels([f"{v:g}" for v in ([0.1, 0.2, 0.5, 1, 2, 5, 10, 20] if a is not ax else [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20])]); sec.tick_params(labelsize=9)
    sec.minorticks_off()
    if a is ax:
        sec.set_ylabel(r"$a_0$  [$10^{-10}$ m/s$^2$]", fontsize=10)
# the z ~ 0 footings (quoted from the record, no SPARC analysis here)
ax.add_patch(Rectangle((0.0, 1.0), 0.16, ALT - 1.0, facecolor="#8c8c8c", alpha=0.45, edgecolor="#555555", lw=0.8, zorder=5))
ax.plot([0.08], [Q_NU], marker="D", ms=6, color="#555555", mfc="white", mew=1.3, ls="none", zorder=5)
ax.plot([0.08], [Q_P2], marker="D", ms=6, color="#555555", mfc="white", mew=1.3, ls="none", zorder=5)
ax.text(0.03, 26, "z ~ 0 (record):\ngrey box = footings\n9.36e-11, 1.131e-10;\ndiamonds = SPARC\nbest free fit, Ups 0.5:\n1.37e-10 (nu_mono),\n1.78e-10 (P2)", fontsize=8.0, color="#444444", va="top", ha="left", zorder=8)
for L, lab in (("FLAT", "flat $a_0$"), ("PROXY", r"$\Lambda$CDM effective-$a_0$ proxy"), ("H(z)", r"$a_0\propto H(z)$"), ("M-DEC", r"$a_0\propto\sqrt{\rho_{DE}}$ (DESI CPL)")):
    ax.annotate(lab, xy=(6.0, cur[L][-1]), xytext=(6, 0), textcoords="offset points", ha="left", va="center", fontsize=10.5, color=COL[L], fontweight="bold")
for txt, xx, col in (("RC100 (class D)", 1.45, C_RC), ("class M (CFG229)\n6 of 7 no root", 2.6, C_M), ("ALMA (CFG228) and CRISTAL (CFG223)", 4.95, C_AL)):
    ax.text(xx, 1.012, txt, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=9.6, color=col, fontweight="bold")
W = lambda t: "\n".join(textwrap.wrap(t, 62))
handles = [Line2D([], [], color=COL["FLAT"], lw=2, label=r"flat $a_0$ (ratio 1)"),
           Line2D([], [], color=COL["PROXY"], lw=2.4, label=W(r"$\Lambda$CDM effective-$a_0$ PROXY (dotted above z = 5)")),
           Line2D([], [], color=COL["H(z)"], lw=2.4, label=r"$a_0\propto H(z)=E(z)$"),
           Line2D([], [], color=COL["M-DEC"], lw=2.4, label=W(r"$a_0\propto\sqrt{\rho_{DE}(z)}$, DESI DR2 CPL (dotted above z = 2.5; band = DESY5, Union3)")),
           Patch(facecolor="#8c8c8c", alpha=0.6, label=W("z ~ 0 footings 9.36e-11 / 1.131e-10 (grey box); diamonds: SPARC best free fits at Upsilon = 0.5 (record, CFG4 H2b)")),
           Line2D([], [], marker="o", color="#555555", ls="none", ms=8, label=W("circle = class D: baryon masses fitted with the dynamics or a scaling prior (RC100 corrected table, CRISTAL fit route)")),
           Line2D([], [], marker="s", color="#555555", ls="none", ms=8, label=W("square = class S/L: one or two un-optimised tracers (CRISTAL independent route, ALPINE [CII], SPT0418-47)")),
           Line2D([], [], marker="*", color="#555555", ls="none", ms=13, label=W("star = class M: Dunne+22 per-galaxy optimised multi-tracer gas (seven z >= 2 galaxies)")),
           Line2D([], [], marker="s", color=C_AL, mfc="white", mew=2.0, ls="none", ms=8, label=W("hollow square = ALPINE6 pooled (median rule over the six rotators)")),
           Line2D([], [], marker="v", color="#555555", ls="none", ms=8, label=W("triangle at the floor = no root (g_obs <= g_bar: no a0 can fit); up-triangle = bar clipped")),
           Line2D([], [], color="#555555", lw=3.6, label=W("statistical: thick = 68%, thin = 95% (draws that have a root)")),
           Patch(facecolor="#777777", alpha=0.3, label=W("systematic (shaded, inner dark / outer light): RC100 and CRISTAL baryon mass +-0.15 / +-0.30 dex; class M and ALMA the joint class bands on gas and stars")),
           Patch(facecolor=C_RC, label="RC100"), Patch(facecolor=C_CR, label="CRISTAL"), Patch(facecolor=C_M, label="class-M sample (CFG229)"), Patch(facecolor=C_AL, label="ALMA sample (CFG228)")]
leg = fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.04, 0.178), ncol=3, fontsize=9.0, frameon=False, columnspacing=1.5, labelspacing=0.55, handlelength=2.0)
cap = ["Descriptive compilation; not a verdict; calibration-limited.  LambdaCDM has no a0: purple is an effective-a0 PROXY.  kappa = 1/2 is FITTED, not derived.  No law is separated, preferred or disfavoured by this chart, and no point is a detection.",
       "CFG223 (criteria 1f243e9e9; figure 155eb31e6; robustness 009d7a888): RC100 four z-quartiles and CRISTAL, author decompositions, gas-route-limited (class D fit-route baryon masses carry the authors' priors).  "
       "CFG229 (criteria 5c131c037 + Addendum 1 7e3b14d20; blind pre-flight e3f30dee5; results 96293d60c): seven class-M galaxies, SIX WITH NO ROOT (D = g_obs/g_bar < 1: no a0 can fit, for any law); ALESS 122.1 alone has a root, s* 8.8 (a0 8.25e-10 m/s2), INFORMATIVE by the A3 rule but ONE dispersion-supported galaxy: statistical 68% x4.2 to x14.4, systematic envelope 3.7 to 17.9, its delta within 1.3 sigma of every law ('a0 cannot be calculated from these seven', CFG229).  "
       "CFG228 (criteria 71ec12282; Stage 1 0694d7fc1; blind pre-flight 0c4c5778d; Stage 3 bb2caa47d; scoring 6842ad597): six ALPINE [CII] rotators (our own rotation fit) and SPT0418-47, two un-optimised tracers; five with a root, two without; ALPINE6 pooled s* 4.33 (a0 4.05e-10 m/s2).",
       "The blind pre-flights of CFG228 and CFG229 said the samples CANNOT separate the laws at the declared bands (NOT POSSIBLE); the bars show why.  Every ALMA set is UNINFORMATIVE about a0 by the frozen rule (the pressure-term choice alone moves an ALPINE point from no root to s* ~ 12: CFG228 README).  "
       "The z ~ 0 footings and the SPARC Upsilon = 0.5 fits are quoted from the record (CFG4_README H2b).  Points are shifted in z by up to 0.2 for legibility (true z in chart_a0z_points.csv).  Plot only; no new analysis: chart_a0z_combined.py reads the three committed results JSONs."]
wrapped = []
for c in cap:
    wrapped += textwrap.wrap(c, 215) + [""]
fig.suptitle(r"a$_0$ over cosmic time: every implied-a$_0$ compilation in the record, against four laws", fontsize=15.5, x=0.06, ha="left", y=0.985)
fig.text(0.06, 0.006, "\n".join(wrapped).rstrip(), fontsize=9.0, va="bottom", ha="left", family="DejaVu Sans", linespacing=1.4)
out = os.path.join(HERE, "chart_a0z_combined_2026-09-30.png")
fig.savefig(out, dpi=140)
open(os.path.join(HERE, "chart_a0z_combined.out"), "w").write("\n".join(OUT) + "\n")
print("wrote", out)
