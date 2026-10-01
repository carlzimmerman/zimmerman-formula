"""ONE chart: a0 across cosmic time -- what has been calculated, what was calculated and has no solution, and the
data sets in hand that have no a0 value yet.  Chart 2026-10-01 (companion to chart_a0z_rar.py).

PLOT ONLY.  Calculated points come from the committed CHART_a0z_combined_2026-09-30/chart_a0z_points.csv (tied to
the CFG223 / CFG228 / CFG229 results JSONs; checked below), the laws from CFG223's cfg223_results.json.  The
"no a0 value yet" rows read their redshifts and counts from the data files on disk; what each one lacks and what was
done with it is quoted from the lane READMEs (CFG197, CFG227 + CFG237 correction, CFG235, CFG258, L328).
Descriptive compilation; calibration-limited; not a verdict.  LambdaCDM has no a0: purple is an effective-a0 PROXY.
kappa = 1/2 is FITTED.
"""
import csv, json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); ROOT = os.path.dirname(CFG)
TAB = os.path.join(ROOT, "data_assembly", "arxiv_tables")
OUT, CHECKS = [], []
def P(s=""): print(s); OUT.append(s)
def check(name, ok, val=""): CHECKS.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name} {val}")

A0, ALT = 9.3603e-11, 1.1312e-10
U = A0 / 1e-10
pts = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv")))}
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
J228 = json.load(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_score_results.json")))
J229 = json.load(open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score_results.json")))
rar = list(csv.DictReader(open(os.path.join(CFG, "CFG227_rar_z2_5", "cfg227_points.csv"))))
cur = J223["curves"]; Zc = np.array(cur["z"])
f = lambda r, k: float(r[k]) if r[k] not in ("", "nan") else np.nan

# ---------------- the "no a0 value yet" rows: z and counts read from files ----------------
dan = [float(r["z"]) for r in csv.DictReader(open(os.path.join(TAB, "danhaive2025_gold.csv")))]
ro_kin = {r[next(iter(r))] for r in csv.DictReader(open(os.path.join(TAB, "romanoliveira2023_kinematics.csv")))}
ro = [(r["id"], float(r["z"])) for r in csv.DictReader(open(os.path.join(TAB, "romanoliveira2023_sample.csv"))) if r["id"] in ro_kin]
alp = {r["id"]: float(r["z"]) for r in csv.DictReader(open(os.path.join(TAB, "alpaka1_digitised", "alpaka1_outer_summary.csv")))}
alp_none = [alp[i] for i in ("13", "23", "24", "25", "28")]          # CFG237: no class-M gas mass on disk
DA = os.path.join(ROOT, "data_assembly")   # data-front cube products (50d8c274e SINS, ff6633985 KMOS3D): no a0 computed there
sins = [float(r["z"]) for r in csv.DictReader(open(os.path.join(DA, "sins_cubes", "sins_ao_per_galaxy_AMEND1.csv")))]
k3d = [float(r["Z"]) for r in csv.DictReader(open(os.path.join(DA, "kmos3d_cubes", "k3d_fits_main_final_flags.csv")))]
amv = [float(r["z"]) for r in rar if r["class"] == "S" and r["id"] != "122.1"]   # 122.1 has a class-M a0 (CFG229)
TODO = [  # (label, zmin, zmax, short note)       sources: CFG227 'Listed, no point' + CFG237 + CFG258 + L328
    ("MIGHTEE-HI survey", 0.02, 0.09, "mock forecast only"),
    (f"SINS AO cubes ({len(sins)})", min(sins), max(sins), "curves extracted; method failed validation"),
    (f"KMOS3D cubes ({len(k3d)})", min(k3d), max(k3d), "curves fitted; no baryons attached"),
    (f"Amvrosiadis+25 ({len(amv)})", min(amv), max(amv), "baryons exceed rotation in most"),
    (f"ALPAKA ({len(alp_none)})", min(alp_none), max(alp_none), "no multi-tracer gas"),
    ("Lelli+23 (1)", 2.24, 2.24, "mean speed only"),
    ("PKS 0529-549 (1)", 2.57, 2.57, "no radius / stellar mass"),
    (f"Danhaive+25 ({len(dan)})", min(dan), max(dan), "no gas mass"),
    ("GN20 (1)", 4.05, 4.05, "no radius / stellar mass"),
    (f"Roman-Oliveira+23 ({len(ro)})", min(z for _, z in ro), max(z for _, z in ro), "no stellar mass"),
    ("HZ9 (1)", 5.54, 5.54, "curve on disk, never run"),
]

P("chart_a0z_one: plot only")
check("ALESS 122.1 plotted a0 equals CFG229 a0_imp", abs(f(pts["ALESS_122.1"], "a0_1e-10_m_s2") * 1e-10 - J229["IMPL"]["ALESS_122.1"]["a0_imp"]) < 1e-14)
check("ALPINE6 plotted a0 equals CFG228 a0_imp", abs(f(pts["ALPINE6 pooled"], "a0_1e-10_m_s2") * 1e-10 - J228["IMPL"]["ALPINE6"]["a0_imp"]) < 1e-14)
check("Danhaive gold: 41 discs at z 3.80-5.82", len(dan) == 41 and abs(min(dan) - 3.80) < 1e-6 and abs(max(dan) - 5.82) < 1e-6, f"({len(dan)}, {min(dan)}-{max(dan)})")
check("Roman-Oliveira with kinematics: 4", len(ro) == 4, f"({len(ro)}: {[i for i, _ in ro]})")
check("Amvrosiadis without an a0: 8", len(amv) == 8, f"({len(amv)})")
nr = [o for o in ("ALPAKA15", "ALPAKA18", "ALPAKA19", "ALPAKA20", "ALPAKA22", "SINS_BX610", "VC5110377875", "SPT0418-47") if pts[o]["no_root"] == "1"]
check("DESI CPL curve is nearly flat: about 0.87 x local at z = 2", abs(np.interp(2.0, Zc, cur["M-DEC"]) - 0.87) < 0.01, f"({np.interp(2.0, Zc, cur['M-DEC']):.3f})")
check("SINS AO 35 and KMOS3D 192 cube products on disk", len(sins) == 35 and len(k3d) == 192, f"({len(sins)}, {len(k3d)})")
check("eight calculated galaxies with no a0 solution (6 class M + 2 ALMA)", len(nr) == 8, f"({len(nr)})")
for lab, z0, z1, note in TODO: P(f"  no-a0-yet row: {lab:28s} z {z0:.2f}-{z1:.2f}  {note}")

# ---------------- style ----------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#555", "xtick.color": "#444", "ytick.color": "#444"})
INK, MUTED = "#16202c", "#6b7480"
LAW = {"FLAT": "#111111", "H(z)": "#d1342f", "PROXY": "#7b3fbf", "M-DEC": "#1b9aaa"}
COL = {"RC100": "#1f5aa6", "CRISTAL": "#e07b00", "M": "#8a5a00", "ALMA": "#2e8b3e"}

fig = plt.figure(figsize=(14, 10.2), dpi=170)
ax = fig.add_axes([0.075, 0.33, 0.885, 0.50])
sx = fig.add_axes([0.075, 0.118, 0.885, 0.215], sharex=ax)
XLO, XHI, YLO, YHI = -0.12, 6.0, 0.17, 30

# ---------------- main: calculated a0 ----------------
ax.set_yscale("log"); ax.set_xlim(XLO, XHI); ax.set_ylim(YLO, YHI)
for x0, x1, t in ((0.6, 2.6, "cosmic noon"), (4.0, 6.0, "first 1.5 billion years")):
    ax.axvspan(x0, x1, color="#eef1f5", zorder=0, lw=0); sx.axvspan(x0, x1, color="#eef1f5", zorder=0, lw=0)
    ax.text((x0 + x1) / 2, 23, t, ha="center", color="#8a94a0", fontsize=10, style="italic")
ax.axhspan(YLO, 0.30, color="#f6f2ea", zorder=0, lw=0)
m = Zc <= XHI
lo_b = np.minimum(np.array(cur["DESI DESY5"]), np.array(cur["DESI Union3"]))[m] * U
hi_b = np.maximum(np.array(cur["DESI DESY5"]), np.array(cur["DESI Union3"]))[m] * U
ax.fill_between(Zc[m], lo_b, hi_b, color=LAW["M-DEC"], alpha=0.13, lw=0, zorder=1)
md = np.array(cur["M-DEC"])[m] * U; zz = Zc[m]
ax.plot(zz[zz <= 2.5], md[zz <= 2.5], color=LAW["M-DEC"], lw=2.2, zorder=2)
ax.plot(zz[zz >= 2.5], md[zz >= 2.5], color=LAW["M-DEC"], lw=2.2, ls=(0, (1.2, 2.2)), zorder=2)
ax.text(2.95, 0.53, r"$a_0 \propto \sqrt{\rho_{DE}}$ (DESI dark energy)", color=LAW["M-DEC"], fontsize=11, ha="left", fontweight="bold")
for k, kw in (("PROXY", dict(lw=2.2, ls=(0, (5, 3)))), ("H(z)", dict(lw=2.8)), ("FLAT", dict(lw=2.8))):
    ax.plot(Zc[m], np.array(cur[k])[m] * U, color=LAW[k], zorder=2, **kw)
ax.text(5.95, 10.6, r"$a_0$ grows with $H(z)$", color=LAW["H(z)"], fontsize=12.5, ha="right", fontweight="bold")
ax.text(5.95, 4.1, r"$\Lambda$CDM proxy", color=LAW["PROXY"], fontsize=11, ha="right", fontweight="bold")
ax.text(5.95, 1.0, r"constant $a_0$", color=LAW["FLAT"], fontsize=12.5, ha="right", fontweight="bold", va="bottom")
ax.fill_between([XLO, 0.08], U, ALT / 1e-10, color="#444", zorder=6, lw=0)
ax.annotate("today (SPARC)", xy=(0.08, 1.06), xytext=(0.28, 2.6), fontsize=10, color="#333",
            arrowprops=dict(arrowstyle="-", color="#888", lw=0.8))

def point(r, x, col, mk, size, hollow=False):
    s, lo68, hi68, lo95, hi95, ilo, ihi = (f(r, k) for k in ("s_star", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi", "inner_lo", "inner_hi"))
    ilo = max(ilo, YLO / U); ihi = min(ihi, YHI / U)
    ax.add_patch(plt.Rectangle((x - 0.06, ilo * U), 0.12, (ihi - ilo) * U, color=col, alpha=0.15, lw=0, zorder=3))
    ax.plot([x, x], [max(lo95, YLO / U) * U, min(hi95, YHI / U) * U], color=col, lw=1.2, zorder=4)
    ax.plot([x, x], [lo68 * U, min(hi68, YHI / U) * U], color=col, lw=4.6, zorder=4, solid_capstyle="butt")
    ax.scatter([x], [s * U], marker=mk, s=size, zorder=6, facecolor="white" if hollow else col,
               edgecolor=col if hollow else "white", linewidth=1.8 if hollow else 1.0)
for q in ("Q1", "Q2", "Q3", "Q4"):
    r = pts[f"RC100 corr {q}"]; point(r, f(r, "z"), COL["RC100"], "o", 95)
ax.text(1.05, 5.6, "RC100\n100 discs in 4 bins", color=COL["RC100"], fontsize=10, ha="center", fontweight="bold")
r = pts["ALESS_122.1"]; point(r, 2.13, COL["M"], "*", 360)
ax.annotate("ALESS 122.1\nbest gas data, 1 galaxy", xy=(2.18, f(r, "s_star") * U), xytext=(2.45, 15.5), fontsize=10,
            color=COL["M"], fontweight="bold", va="center", arrowprops=dict(arrowstyle="-", color=COL["M"], lw=0.8))
r = pts["ALPINE6 pooled"]; point(r, 4.58, COL["ALMA"], "s", 110, hollow=True)
ax.text(4.46, 6.6, "6 ALMA rotators\n(pooled)", color=COL["ALMA"], fontsize=10, ha="right", fontweight="bold")
point(pts["CR R_e ind"], 5.12, COL["CRISTAL"], "s", 95); point(pts["CR R_out ind"], 5.36, COL["CRISTAL"], "s", 95)
ax.text(5.46, 2.0, "CRISTAL\n6 discs,\n2 radii", color=COL["CRISTAL"], fontsize=10, ha="left", va="center", fontweight="bold")
# calculated, no solution
NRX = {"SINS_BX610": 2.16, "ALPAKA15": 2.27, "ALPAKA18": 2.40, "ALPAKA19": 2.49, "ALPAKA20": 2.58, "ALPAKA22": 2.94,
       "SPT0418-47": 4.22, "VC5110377875": 4.52}
for o, x in NRX.items():
    ax.scatter([x], [0.215], marker="v", s=70, color=COL["M"] if not o.startswith(("SPT", "VC")) else COL["ALMA"], zorder=6, edgecolor="white", lw=0.6)
ax.text(0.12, 0.222, "calculated, but no $a_0$ fits (8 galaxies):\nthe stars + gas already exceed what the rotation needs  ▸",
        fontsize=9.5, color="#7a5a1a", va="center")
ax.set_ylabel(r"$a_0$ implied by the rotation   [$10^{-10}$ m s$^{-2}$]", fontsize=12)
ax.set_yticks([0.3, 0.5, 1, 2, 3, 5, 10, 20]); ax.set_yticklabels(["0.3", "0.5", "1", "2", "3", "5", "10", "20"])
ax.grid(True, which="major", axis="y", color="#e4e7eb", lw=0.7, zorder=0)
plt.setp(ax.get_xticklabels(), visible=False); ax.tick_params(axis="x", length=0)
HUB = 977.79 / 67.4
age = lambda z: HUB * quad(lambda zz: 1 / ((1 + zz) * np.sqrt(0.315 * (1 + zz) ** 3 + 0.685)), z, np.inf)[0]
ages = [13, 6, 3, 2, 1.5, 1.2, 1.0]
top = ax.secondary_xaxis("top"); top.set_xticks([brentq(lambda z: age(z) - t, 0, 50) for t in ages])
top.set_xticklabels([f"{t:g}" for t in ages], fontsize=9.5, color=MUTED)
top.set_xlabel("age of the universe (billion years)", fontsize=10, color=MUTED, labelpad=6)
ax.text(0.008, 0.975, "a₀ CALCULATED", transform=ax.transAxes, fontsize=10.5, color=INK, fontweight="bold", ha="left", va="top")

# ---------------- strip: data in hand, no a0 value yet ----------------
sx.set_ylim(len(TODO) - 0.4, -0.8); sx.set_yticks([]); sx.spines["left"].set_visible(False)
sx.spines["top"].set_visible(True); sx.spines["top"].set_color("#bbb"); sx.spines["top"].set_linestyle((0, (3, 3)))
for i, (lab, z0, z1, note) in enumerate(TODO):
    if z1 - z0 > 0.04:
        sx.add_patch(plt.Rectangle((z0, i - 0.27), z1 - z0, 0.54, fill=False, ec=INK, lw=1.2, ls=(0, (3, 2)), zorder=3))
    else:
        sx.scatter([z0], [i], s=60, facecolor="white", edgecolor=INK, lw=1.2, linestyle=(0, (2, 1.5)), zorder=3)
    right = not lab.startswith(("Amvrosiadis", "Danhaive", "GN20", "Roman", "HZ9"))
    xp = z1 + 0.07 if right else z0 - 0.07
    t = sx.text(xp, i, lab, ha="left" if right else "right", va="center", fontsize=9.8, color=INK, fontweight="bold")
    tb = t.get_window_extent(fig.canvas.get_renderer()); inv = sx.transData.inverted()
    xa = inv.transform((tb.x1, 0))[0] + 0.03 if right else inv.transform((tb.x0, 0))[0] - 0.03
    sx.text(xa, i, ("· " + note) if right else (note + " ·"), ha="left" if right else "right", va="center", fontsize=9, color=MUTED)
sx.text(0.995, 0.975, "DATA IN HAND, NO a₀ VALUE YET", transform=sx.transAxes, fontsize=10.5, color=INK, fontweight="bold", ha="right", va="top")
sx.set_xlabel("redshift  z", fontsize=12)
sx.set_xticks(range(7)); sx.grid(True, axis="x", color="#e4e7eb", lw=0.7, zorder=0)
for x in range(7): ax.axvline(x, color="#e4e7eb", lw=0.7, zorder=0)

# ---------------- headline ----------------
fig.text(0.075, 0.955, "Is $a_0$ constant across 12 billion years?  Not decidable from today's data",
         fontsize=19, fontweight="bold", color=INK)
fig.text(0.075, 0.905, "None of these samples can separate a constant $a_0$ from one that grows with $H(z)$: at z > 1 the gas masses are uncertain by 0.2-0.7 dex,\n"
         "and a 0.05 dex error in the baryon mass moves the implied $a_0$ by ×1.5-1.8.  The dashed sets at the bottom are data in hand with no $a_0$ value yet.",
         fontsize=11.5, color="#3d4651", va="center")
fig.text(0.075, 0.004, "Bars: thick 68 %, thin 95 % statistical; shaded: baryon-mass calibration band.  Descriptive compilation, not a verdict; "
         "ΛCDM has no $a_0$ (purple is an effective-$a_0$ proxy); κ = ½ fitted.\nTeal: $a_0 \\propto \\sqrt{\\rho_{DE}}$ with the DESI DR2 CPL fit ($w_0, w_a$) = (-0.838, -0.62), dotted beyond z = 2.5; band = DESY5 and Union3.\nSources: CFG223, CFG227 + CFG237, CFG228, CFG229 (calculated); "
         "CFG197, CFG235, CFG258, L328 (tests that gave no $a_0$ value).  Some points nudged in z for legibility.  Plot only: chart_a0z_one.py.",
         fontsize=8.6, color="#7a828c")
fig.savefig(os.path.join(HERE, "chart_a0z_one_2026-10-01.png"), dpi=170)
P(f"{sum(CHECKS)}/{len(CHECKS)} checks pass; wrote chart_a0z_one_2026-10-01.png")
open(os.path.join(HERE, "chart_a0z_one_2026-10-01.out"), "w").write("\n".join(OUT) + "\n")
