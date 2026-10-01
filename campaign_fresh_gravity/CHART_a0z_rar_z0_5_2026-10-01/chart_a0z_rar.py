"""a0 from z = 0 to 5.5, and the radial-acceleration relation at z ~ 2-5.  Chart 2026-10-01.

PLOT ONLY.  Every plotted number is read from a committed file:
  CHART_a0z_combined_2026-09-30/chart_a0z_points.csv  (implied-a0 points of CFG223 / CFG228 / CFG229, as committed)
  CFG223_a0_over_cosmic_time/cfg223_results.json       (the four laws' curves)
  CFG227_rar_z2_5/cfg227_points.csv                    (RAR points: Amvrosiadis class S, CRISTAL class L / D, RC100 z >= 2 class D)
  CFG228_alma_cubes/cfg228_score_results.json          (six ALPINE [CII] rotators + SPT0418-47: g_obs, g_bar, joint class bands)
  CFG229_class_m_gold/cfg229_score_results.json        (the seven class-M galaxies: g_obs, g_bar)
Nothing is fitted or estimated here.  The only computations are unit conversions, the RAR curves
g_obs = g_bar nu(g_bar/a0) with the record's nu_mono kernel, and the cosmic-age axis (flat LCDM, H0 = 67.4,
Om = 0.315; used for the top axis only).
Descriptive compilation; calibration-limited; not a verdict.  LambdaCDM has no a0: the purple curve is an
effective-a0 PROXY.  kappa = 1/2 is FITTED.
"""
import csv, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
OUT = []
def P(s=""):
    print(s); OUT.append(s)
CHECKS = []
def check(name, ok, val=""):
    CHECKS.append(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name} {val}")

A0 = 9.3603e-11            # canonical footing (m/s^2); every implied-a0 ratio in the record is in this unit
ALT = 1.1312e-10           # alternative footing
U = A0 / 1e-10             # ratio -> a0 in units of 1e-10 m/s^2

# ---------------- load ----------------
pts = list(csv.DictReader(open(os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv"))))
J223 = json.load(open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_results.json")))
J228 = json.load(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_score_results.json")))
J229 = json.load(open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score_results.json")))
rar = list(csv.DictReader(open(os.path.join(CFG, "CFG227_rar_z2_5", "cfg227_points.csv"))))
cur = J223["curves"]; Zc = np.array(cur["z"])
byobj = {r["object"]: r for r in pts}
f = lambda r, k: float(r[k]) if r[k] not in ("", "nan") else np.nan

# ---------------- checks that tie the plotted numbers to their source files ----------------
P("chart_a0z_rar: plot only; checks tie plotted values to committed files")
check("ALESS 122.1 a0 in the points CSV equals CFG229 IMPL a0_imp",
      abs(f(byobj["ALESS_122.1"], "a0_1e-10_m_s2") * 1e-10 - J229["IMPL"]["ALESS_122.1"]["a0_imp"]) < 1e-14,
      f"{f(byobj['ALESS_122.1'], 'a0_1e-10_m_s2'):.4f}e-10")
check("ALPINE6 pooled a0 in the points CSV equals CFG228 IMPL a0_imp",
      abs(f(byobj["ALPINE6 pooled"], "a0_1e-10_m_s2") * 1e-10 - J228["IMPL"]["ALPINE6"]["a0_imp"]) < 1e-14,
      f"{f(byobj['ALPINE6 pooled'], 'a0_1e-10_m_s2'):.4f}e-10")
nr229 = sum(1 for s in J229["IMPL"] if s in J229["gid"] and not np.isfinite(J229["IMPL"][s]["a0_imp"]))
check("CFG229: six of seven class-M galaxies have no root", nr229 == 6, f"({nr229})")
nr228 = sum(1 for g in J228["gid"] if not np.isfinite(J228["IMPL"][g]["a0_imp"]))
check("CFG228: two of seven ALMA galaxies have no root", nr228 == 2, f"({nr228})")
ncl = sum(1 for r in rar if r["class"] == "L")
check("CFG227: twelve class-L CRISTAL rows (R_e 6 + R_out 6)", ncl == 12, f"({ncl})")
check("CFG223 curves: flat curve is identically 1", np.allclose(cur["FLAT"], 1.0))

MUTATE = os.environ.get("MUTATE") == "1"
if MUTATE:   # swap two plotted values: the tie-to-source checks must fail
    byobj["ALESS_122.1"]["a0_1e-10_m_s2"], byobj["ALPINE6 pooled"]["a0_1e-10_m_s2"] = \
        byobj["ALPINE6 pooled"]["a0_1e-10_m_s2"], byobj["ALESS_122.1"]["a0_1e-10_m_s2"]
    check("MUTATE: ALESS value still ties to CFG229 (must FAIL)",
          abs(f(byobj["ALESS_122.1"], "a0_1e-10_m_s2") * 1e-10 - J229["IMPL"]["ALESS_122.1"]["a0_imp"]) < 1e-14)

# ---------------- cosmic age (top axis only) ----------------
H0 = 67.4; Om = 0.315; HUB = 977.79 / H0     # Gyr
age = lambda z: HUB * quad(lambda zz: 1 / ((1 + zz) * np.sqrt(Om * (1 + zz) ** 3 + 1 - Om)), z, np.inf)[0]
from scipy.optimize import brentq
z_of_age = lambda t: brentq(lambda z: age(z) - t, 0, 50)

# ---------------- style ----------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#555", "axes.linewidth": 0.9,
                     "xtick.color": "#444", "ytick.color": "#444", "axes.labelcolor": "#222"})
INK = "#1d1d1f"
LAW = {"FLAT": "#111111", "H(z)": "#d1342f", "PROXY": "#7b3fbf", "M-DEC": "#1b9aaa"}
LANE = {"RC100": "#1f5aa6", "CRISTAL": "#e07b00", "M": "#8a5a00", "ALMA": "#2e8b3e", "S1": "#b0548f"}

fig = plt.figure(figsize=(17.5, 9.2), dpi=170)
gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1], wspace=0.17, left=0.055, right=0.985, top=0.77, bottom=0.215)
ax = fig.add_subplot(gs[0]); bx = fig.add_subplot(gs[1])

# =============== PANEL A: a0 against redshift ===============
YLO, YHI = 0.22, 30
ax.set_yscale("log"); ax.set_xlim(-0.1, 5.85); ax.set_ylim(YLO, YHI)
for x0, x1 in ((0.6, 2.6), (4.0, 5.85)):
    ax.axvspan(x0, x1, color="#f4f1ea", zorder=0, lw=0)
ax.text(1.6, 22, "cosmic noon", ha="center", color="#9a8f78", fontsize=9.5, style="italic")
ax.text(4.92, 22, "first billion-and-a-half years", ha="center", color="#9a8f78", fontsize=9.5, style="italic")

zz = Zc[Zc <= 5.85]
def curve(key, **kw):
    y = np.array(cur[key])[Zc <= 5.85] * U
    return ax.plot(zz, y, **kw)
curve("M-DEC", color=LAW["M-DEC"], lw=1.6, alpha=0.75, zorder=2)
curve("PROXY", color=LAW["PROXY"], lw=2.2, ls=(0, (4, 2)), zorder=2)
curve("H(z)", color=LAW["H(z)"], lw=2.6, zorder=2)
curve("FLAT", color=LAW["FLAT"], lw=2.6, zorder=3)
yH = np.interp(5.85, Zc, cur["H(z)"]) * U
ax.text(5.8, 11.2, r"$a_0 \propto H(z)$", color=LAW["H(z)"], fontsize=12, ha="right", fontweight="bold")
ax.text(3.55, 1.62, r"$\Lambda$CDM effective-$a_0$ proxy", color=LAW["PROXY"], fontsize=10.5, ha="left", fontweight="bold", rotation=14)
ax.text(3.3, 1.0, r"flat $a_0$", color=LAW["FLAT"], fontsize=12, ha="left", fontweight="bold", va="bottom")
ax.text(5.8, 0.50, r"$a_0 \propto \sqrt{\rho_{DE}}$ (DESI)", color=LAW["M-DEC"], fontsize=10, ha="right", va="top")

# z ~ 0: the two footings (quoted from the record)
ax.fill_between([-0.1, 0.1], A0 / 1e-10, ALT / 1e-10, color="#444", alpha=0.85, zorder=6, lw=0)
ax.annotate("local galaxies\n(SPARC, two footings)", xy=(0.1, 1.03), xytext=(0.32, 0.36), fontsize=9.5,
            color="#333", arrowprops=dict(arrowstyle="-", color="#777", lw=0.8))

def point(r, x, col, mk, size, label=None, hollow=False, sys_band=True):
    s, lo68, hi68, lo95, hi95 = (f(r, k) for k in ("s_star", "stat68_lo", "stat68_hi", "stat95_lo", "stat95_hi"))
    if sys_band and np.isfinite(f(r, "inner_lo")):
        ilo = max(f(r, "inner_lo"), YLO / U); ihi = min(f(r, "inner_hi"), YHI / U)
        ax.add_patch(plt.Rectangle((x - 0.055, ilo * U), 0.11, (ihi - ilo) * U, color=col, alpha=0.16, lw=0, zorder=3))
    ax.plot([x, x], [max(lo95, YLO / U) * U, min(hi95, YHI / U) * U], color=col, lw=1.1, zorder=4, solid_capstyle="butt")
    ax.plot([x, x], [lo68 * U, min(hi68, YHI / U) * U], color=col, lw=4.2, zorder=4, solid_capstyle="butt")
    ax.scatter([x], [s * U], marker=mk, s=size, zorder=6, edgecolor="white" if not hollow else col,
               facecolor=("white" if hollow else col), linewidth=1.6 if hollow else 1.0)
    if label:
        return x, s * U

# RC100 quartiles (class D: the narrowest bars in the record)
for q in ("Q1", "Q2", "Q3", "Q4"):
    r = byobj[f"RC100 corr {q}"]; point(r, f(r, "z"), LANE["RC100"], "o", 90)
ax.text(1.05, 6.3, "RC100: 100 massive discs,\nfour redshift quartiles", color=LANE["RC100"], fontsize=9.5, ha="center")

# class M: ALESS 122.1 (the only class-M galaxy with a root) + six with no root
r = byobj["ALESS_122.1"]; point(r, f(r, "z"), LANE["M"], "*", 330)
ax.annotate("ALESS 122.1\nbest gas calibration (class M)\none galaxy", xy=(f(r, "z") + 0.04, f(r, "s_star") * U),
            xytext=(2.35, 15.5), fontsize=9, color=LANE["M"], va="center",
            arrowprops=dict(arrowstyle="-", color=LANE["M"], lw=0.8))
nr = [(o, f(byobj[o], "z")) for o in ("ALPAKA15", "ALPAKA18", "ALPAKA19", "ALPAKA20", "ALPAKA22", "SINS_BX610")]
ax.scatter([z for _, z in nr], [0.255] * 6, marker="v", s=55, color=LANE["M"], zorder=6, edgecolor="white", lw=0.6)
ax.text(2.56, 0.315, "6 more class-M galaxies: no $a_0$ fits\n(baryons already exceed the dynamics)", fontsize=8.5,
        color=LANE["M"], ha="center", va="bottom")

# ALMA ALPINE rotators: individual (faint, no bars) + the pooled six (CFG228)
for o in ("CG32", "DC396844", "DC494057", "DC552206", "DC881725"):
    ax.scatter([f(byobj[o], "z")], [f(byobj[o], "s_star") * U], marker="s", s=26, color=LANE["ALMA"], alpha=0.40,
               zorder=5, lw=0)
r = byobj["ALPINE6 pooled"]; point(r, f(r, "z"), LANE["ALMA"], "s", 95, hollow=True)
ax.text(f(r, "z") - 0.08, 7.6, "ALMA [CII]\nrotators", color=LANE["ALMA"], fontsize=9, ha="right")

# CRISTAL independent route (class L) and fit route (class D, faint)
xs = {"CR R_e ind": 5.14, "CR R_out ind": 5.38, "CR R_e fit": 5.02, "CR R_out fit": 5.50}
for o in ("CR R_e fit", "CR R_out fit"):
    rr = byobj[o]
    ax.scatter([xs[o]], [f(rr, "s_star") * U], marker="o", s=40, facecolor="white", edgecolor=LANE["CRISTAL"], lw=1.2,
               zorder=5, alpha=0.9)
for o in ("CR R_e ind", "CR R_out ind"):
    point(byobj[o], xs[o], LANE["CRISTAL"], "s", 85)
ax.text(5.26, 0.265, "CRISTAL discs (z 4.4-5.7)", color=LANE["CRISTAL"], fontsize=9.5, ha="center", zorder=9,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))

ax.set_xlabel("redshift  z", fontsize=12.5)
ax.set_ylabel(r"$a_0$ implied by the rotation curves   [$10^{-10}$ m s$^{-2}$]", fontsize=12.5)
ax.set_yticks([0.3, 0.5, 1, 2, 3, 5, 10, 20]); ax.set_yticklabels(["0.3", "0.5", "1", "2", "3", "5", "10", "20"])
ax.grid(True, which="major", color="#e3e3e3", lw=0.7, zorder=0)
top = ax.secondary_xaxis("top", functions=(lambda z: z, lambda z: z))
ages = [13, 6, 3, 2, 1.5, 1.2, 1.0]
top.set_xticks([z_of_age(t) for t in ages]); top.set_xticklabels([f"{t:g}" for t in ages], fontsize=9.5, color="#666")
top.set_xlabel("age of the universe (Gyr)", fontsize=10, color="#666", labelpad=6)
ax.set_title("A   $a_0$ across cosmic time", loc="left", fontsize=14, fontweight="bold", color=INK, pad=46)

# =============== PANEL B: RAR at z ~ 2-5 ===============
bx.set_xscale("log"); bx.set_yscale("log")
gb = np.logspace(-10.85, -7.7, 400)
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / y)                   # nu_mono, the record's kernel
E = lambda z: np.interp(z, Zc, cur["H(z)"])                  # E(z) = H(z)/H0 from CFG223's curve
bx.fill_between(gb, 1e-12, gb, color="#efefef", zorder=0, lw=0)
bx.plot(gb, gb, color="#9a9a9a", lw=1.2, zorder=1)
bx.text(9e-9, 2.6e-10, "below the line:\nbaryons exceed\nthe dynamics,\nno $a_0$ can fit", fontsize=8.8, color="#888", ha="center", va="center")
bx.plot(gb, gb * nu(gb / A0), color=LAW["FLAT"], lw=2.6, zorder=2)
for z, ls in ((2.5, "-"), (5.0, (0, (4, 2)))):
    a = A0 * E(z); bx.plot(gb, gb * nu(gb / a), color=LAW["H(z)"], lw=2.0, ls=ls, zorder=2)
bx.legend(handles=[Line2D([], [], color=LAW["FLAT"], lw=2.6, label="z = 0 relation (flat $a_0$)"),
                   Line2D([], [], color=LAW["H(z)"], lw=2.0, label=r"$a_0\propto H(z)$ at z = 2.5"),
                   Line2D([], [], color=LAW["H(z)"], lw=2.0, ls=(0, (4, 2)), label=r"$a_0\propto H(z)$ at z = 5"),
                   Line2D([], [], color="#9a9a9a", lw=1.2, label="Newtonian, $g_{obs} = g_{bar}$")],
          loc="upper left", frameon=False, fontsize=9.5, handlelength=2.4)
def hband(x, y, lo, hi, col):
    bx.plot([lo, hi], [y, y], color=col, lw=3.2, alpha=0.30, zorder=3, solid_capstyle="butt")
for r in rar:   # class D (flagged, never scored): RC100 z >= 2 and CRISTAL fit route
    if r["class"] == "D":
        bx.scatter(float(r["g_bar"]), float(r["g_obs"]), s=9, color="#b9b9b9", zorder=2, lw=0)
for r in rar:
    if r["class"] == "S":
        hband(None, float(r["g_obs"]), float(r["g_bar_inner_minus"]), float(r["g_bar_inner_plus"]), LANE["S1"])
        bx.scatter(float(r["g_bar"]), float(r["g_obs"]), marker="D", s=46, color=LANE["S1"], edgecolor="white", lw=0.7, zorder=5)
    elif r["class"] == "L":
        hband(None, float(r["g_obs"]), float(r["g_bar_inner_minus"]), float(r["g_bar_inner_plus"]), LANE["CRISTAL"])
        bx.scatter(float(r["g_bar"]), float(r["g_obs"]), marker="s", s=52, color=LANE["CRISTAL"], edgecolor="white", lw=0.7, zorder=5)
for i, g in enumerate(J228["gid"]):
    lo, hi = J228["BANDS_GB"]["joint -inner"][i], J228["BANDS_GB"]["joint +inner"][i]
    hband(None, J228["GO"][i], lo, hi, LANE["ALMA"])
    bx.scatter(J228["GB"][i], J228["GO"][i], marker="s", s=58, facecolor="white", edgecolor=LANE["ALMA"], lw=1.8, zorder=6)
for i, g in enumerate(J229["gid"]):
    bx.scatter(J229["GB"][i], J229["GO"][i], marker="*", s=230 if g == "ALESS_122.1" else 150, color=LANE["M"],
               edgecolor="white", lw=0.7, zorder=7)
i = J229["gid"].index("ALESS_122.1")
bx.annotate("ALESS 122.1", xy=(J229["GB"][i], J229["GO"][i]), xytext=(1.6e-10, 2.1e-9), fontsize=9, color=LANE["M"],
            arrowprops=dict(arrowstyle="-", color=LANE["M"], lw=0.8))
bx.text(1.45e-8, 5.0e-9, "class-M\ndiscs", fontsize=8.8, color=LANE["M"], ha="center", va="bottom")
bx.set_xlim(1.2e-11, 2.5e-8); bx.set_ylim(4e-11, 2.5e-8)
bx.set_xlabel(r"$g_{\rm bar}$  from stars + gas   [m s$^{-2}$]", fontsize=12.5)
bx.set_ylabel(r"$g_{\rm obs} = V^2/r$   [m s$^{-2}$]", fontsize=12.5)
bx.grid(True, which="major", color="#e3e3e3", lw=0.7, zorder=0)
bx.set_title("B   The radial-acceleration relation at z ≈ 2-5.7", loc="left", fontsize=14, fontweight="bold", color=INK, pad=46)
bx.text(0.0, 1.095, "every z ≥ 2 galaxy in the record with stars, gas and a measured velocity", transform=bx.transAxes,
        fontsize=9.5, color="#666")
ax.text(0.0, 1.095, "implied $a_0$ per sample; bars: thick 68 %, thin 95 % statistical; shaded: baryon-mass calibration band",
        transform=ax.transAxes, fontsize=9.5, color="#666")

# =============== shared legend + title + footer ===============
H = [Line2D([], [], color=LANE["RC100"], marker="o", ls="", ms=8, label="RC100 discs, z 0.6-2.5 (masses fitted, class D)"),
     Line2D([], [], color=LANE["M"], marker="*", ls="", ms=13, label="multi-tracer gas, Dunne+22 (class M, z 2.0-2.9)"),
     Line2D([], [], color=LANE["ALMA"], marker="s", ls="", ms=8, mfc="white", mew=1.8, label="ALPINE [CII] rotators, our cube fits (class S/L)"),
     Line2D([], [], color=LANE["CRISTAL"], marker="s", ls="", ms=8, label="CRISTAL, independent masses (class L)"),
     Line2D([], [], color=LANE["S1"], marker="D", ls="", ms=7, label="Amvrosiadis+25 sub-mm discs (class S)"),
     Line2D([], [], color="#b9b9b9", marker="o", ls="", ms=5, label="fit-route masses (class D, not scored)")]
fig.legend(handles=H, loc="lower center", ncol=3, frameon=False, fontsize=10, bbox_to_anchor=(0.52, 0.05),
           columnspacing=2.2, handletextpad=0.5)
fig.text(0.055, 0.955, "Is $a_0$ the same in the early universe?  What our best high-redshift galaxies can and cannot say",
         fontsize=18, fontweight="bold", color=INK)
fig.text(0.055, 0.88, "At the calibration bands the record declares, no sample here separates a constant $a_0$ from $a_0 \\propto H(z)$.\n"
         "Gas masses at z > 1 are uncertain by 0.2-0.7 dex, and a 0.05 dex baryon-mass error moves the implied $a_0$ by ×1.5-1.8.",
         fontsize=11.5, color="#444")
fig.text(0.055, 0.008, "Descriptive compilation, not a verdict; no law is separated or preferred.  ΛCDM has no $a_0$: purple is an "
         "effective-$a_0$ proxy.  κ = ½ is fitted.\nSources: CFG223, CFG227 (+ CFG237 corrections), CFG228, CFG229; "
         "plot only (chart_a0z_rar.py).  CRISTAL points nudged in z by ≤ 0.24 for legibility.",
         fontsize=8.6, color="#777")

name = "chart_a0z_rar_2026-10-01" + ("_MUTATE" if MUTATE else "")
fig.savefig(os.path.join(HERE, name + ".png"), dpi=170)
P(f"{sum(CHECKS)}/{len(CHECKS)} checks pass; wrote {name}.png")
open(os.path.join(HERE, name.replace("chart_", "chart_") + ".out"), "w").write("\n".join(OUT) + "\n")
