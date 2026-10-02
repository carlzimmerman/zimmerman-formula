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
M262 = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG262_musedark_zthirds_by_route", "cfg262_points_stageB.csv"))) if r["reading"] == "bD"]
K261 = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG261_kids_absolute_a0_zthirds", "cfg261_points_stageB.csv"))) if r["set"] == "T"]
J255 = json.load(open(os.path.join(CFG, "CFG255_lensing_rar_zsplit", "cfg255_stageB_results.json")))["numbers"]
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
A272 = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG272_alpaka_five_discs", "cfg272_points_stageB.csv"))) if "pooled" not in r["object"] and r["s_star"] != "nan"]   # CFG272 d993f02dc
A270 = list(csv.DictReader(open(os.path.join(CFG, "CFG270_kmos3d_cube_fits", "cfg270_points_stageB.csv"))))   # CFG270 b2e86a913
A271 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG271_hz9_three_rings", "cfg271_points_stageB.csv")))}   # CFG271 a18b17d72
A277 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG277_roman_oliveira_four_discs", "cfg277_points_stageB.csv")))}   # CFG277 0f6c4cd58
A280 = list(csv.DictReader(open(os.path.join(CFG, "CFG280_sins_ao_published", "cfg280_points_stageB.csv"))))   # CFG280 396299a9f
M279 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG279_mightee_published_values", "cfg279_points.csv")))}   # CFG279 7cecb04bc
A275 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG275_pks0529_ci_rings", "cfg275_points_stageB.csv")))}   # CFG275 093132b4c
A276 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG276_gn20", "cfg276_points_stageB.csv")))}   # CFG276 231d32a8c
A278 = {r["object"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG278_lelli23_two_discs", "cfg278_points_stageB.csv")))}   # CFG278 9878bfcec
A273 = list(csv.DictReader(open(os.path.join(CFG, "CFG273_danhaive_gold41", "cfg273_points_stageB_relabelled.csv"))))   # CFG273 208944196 (relabelled: two ceiling rows)
A274 = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG274_amvrosiadis_eight_discs", "cfg274_points_stageB.csv"))) if "pooled" not in r["object"]]   # CFG274 255f07244
TODO = [  # (label, zmin, zmax, short note)       sources: CFG227 'Listed, no point' + CFG237 + CFG258 + L328
    ("ALPAKA 24 (1)", alp["24"], alp["24"], "no stellar mass"),
]

P("chart_a0z_one: plot only")
check("ALESS 122.1 plotted a0 equals CFG229 a0_imp", abs(f(pts["ALESS_122.1"], "a0_1e-10_m_s2") * 1e-10 - J229["IMPL"]["ALESS_122.1"]["a0_imp"]) < 1e-14)
check("ALPINE6 plotted a0 equals CFG228 a0_imp", abs(f(pts["ALPINE6 pooled"], "a0_1e-10_m_s2") * 1e-10 - J228["IMPL"]["ALPINE6"]["a0_imp"]) < 1e-14)
check("Danhaive gold: 41 discs at z 3.80-5.82", len(dan) == 41 and abs(min(dan) - 3.80) < 1e-6 and abs(max(dan) - 5.82) < 1e-6, f"({len(dan)}, {min(dan)}-{max(dan)})")
check("Roman-Oliveira with kinematics: 4", len(ro) == 4, f"({len(ro)}: {[i for i, _ in ro]})")
check("CFG270 KMOS3D: pooled PT1 (72 fits) <= 2.44 at z 2.228; 16 T1 fits at the floor (b2e86a913)", any(r["object"] == "KMOS3D pooled PT1" and abs(float(r["s_star"]) - 2.4413) < 1e-3 for r in A270) and sum(r["tier"] == "T1" and r["no_root"] == "1" for r in A270) == 16, f"({sum(r['tier'] == 'T1' and r['no_root'] == '1' for r in A270)} T1 floor)")
check("CFG271 HZ9: outer-ring stars-only upper bounds 14.85 (corpus M*) and 48.9 (Parlanti M*) (a18b17d72)", abs(float(A271["HZ9 [M103]"]["s_star"]) - 14.847) < 1e-2 and abs(float(A271["HZ9 [M986]"]["s_star"]) - 48.906) < 1e-2)
check("CFG277 Roman-Oliveira: J081740 [gas] and BRI1335-0417 [gas] no root; SGP pair vacuous (51, 28) (0f6c4cd58)", A277["J081740 [gas]"]["no_root"] == "1" and A277["BRI1335-0417 [gas]"]["no_root"] == "1" and round(float(A277["SGP38326-1 [gas]"]["s_star"])) == 51)
check("CFG280 SINS: PT2_new <= 9.09 (overlap-free); 7 stars-only floor galaxies without an RC100/KMOS3D match (396299a9f)", any(r["object"] == "SINS pooled PT2_new" and abs(float(r["s_star"]) - 9.0878) < 1e-3 for r in A280) and len([r for r in A280 if r["no_root"] == "1" and "[" not in r["object"] and r["rc100_match"] == "0" and r["kmos3d_match"] == "0"]) == 7)
check("CFG279 MIGHTEE-HI: published whole-sample a0 = 1.50e-10 at z 0.055 (7cecb04bc)", abs(float(M279["MIGHTEE-HI paper: whole sample, z-averaged"]["a0_1e-10_m_s2"]) - 1.50) < 1e-6)
check("CFG275 PKS 0529-549: chart row [CIG; CO] is a FLOOR (no root), 7 of 8 rows floor (093132b4c)", A275["PKS0529 [CIG; CO]"]["no_root"] == "1" and sum(r["no_root"] == "1" for r in A275.values()) == 7)
check("CFG276 GN20: frozen row [stars+RT; Re] is a floor but uninformative (D 0.90) (231d32a8c)", A276["GN20 [stars+RT; Re]"]["no_root"] == "1")
check("CFG278 Lelli+23: zC-400569 [stars+CO a=0.4] floor; zC-488879 [stars+CO a=0.4] <= 33.4 (9878bfcec)", A278["zC-400569 [stars+CO a=0.4]"]["no_root"] == "1" and abs(float(A278["zC-488879 [stars+CO a=0.4]"]["s_star"]) - 33.424) < 1e-2)
check("CFG273 Danhaive: 7 no root (relabelled file), pooled PALL <= 29.4 at z 4.17 (208944196)", sum(r["no_root"] == "1" for r in A273) == 7 and any("PALL" in r["object"] and abs(float(r["s_star"]) - 29.45) < 0.01 for r in A273), f"({sum(r['no_root'] == '1' for r in A273)} no root)")
check("CFG272 ALPAKA: 13 and 23 no root; 25 <= 3.30 and 28 <= 0.74 upper bounds; 24 no M* (d993f02dc)", sorted(r["object"].split()[1] for r in A272 if r["no_root"] == "1") == ["13", "23"] and sorted(round(float(r["s_star"]), 2) for r in A272 if r["no_root"] == "0") == [0.74, 3.3], f"({len(A272)} rows)")
check("CFG274 Amvrosiadis: 7 of 8 no root, ALESS 075.1 s* 6.89 (255f07244)", sum(r["no_root"] == "1" for r in A274) == 7 and any(r["no_root"] == "0" and abs(float(r["s_star"]) - 6.887) < 0.01 for r in A274), f"({sum(r['no_root'] == '1' for r in A274)} no root)")
nr = [o for o in ("ALPAKA15", "ALPAKA18", "ALPAKA19", "ALPAKA20", "ALPAKA22", "SINS_BX610", "VC5110377875", "SPT0418-47") if pts[o]["no_root"] == "1"]
check("DESI CPL curve is nearly flat: about 0.87 x local at z = 2", abs(np.interp(2.0, Zc, cur["M-DEC"]) - 0.87) < 0.01, f"({np.interp(2.0, Zc, cur['M-DEC']):.3f})")
check("SINS AO 35 and KMOS3D 192 cube products on disk", len(sins) == 35 and len(k3d) == 192, f"({len(sins)}, {len(k3d)})")
check("CFG261 class rows: late 1.67 / 0.68, early 2.48 / 4.12 (80fd3d666)", len(K261) == 4 and [round(float(r["s_star"]), 2) for r in K261] == [1.67, 0.68, 2.48, 4.12], f"({[round(float(r['s_star']), 2) for r in K261]})")
check("KiDS split: A = +0.060 +- 0.038 dex, FLAT +0.001, RIVAL +0.019 (CFG255 stage B)", abs(J255["A_data"] - 0.0595) < 1e-3 and abs(J255["sigma_A"] - 0.0383) < 1e-3, f"(A {J255['A_data']:.4f}, sigma {J255['sigma_A']:.4f})")
check("CFG262 bD rows: route i 1.22/3.05/4.53, ii 0.46/1.02/0.36, iii 1.58/3.32/1.71 (fb24a5922)", sorted(round(float(r["s_star"]), 2) for r in M262) == sorted([1.22, 3.05, 4.53, 0.46, 1.02, 0.36, 1.58, 3.32, 1.71]), f"({len(M262)} rows)")
check("eight calculated galaxies with no a0 solution (6 class M + 2 ALMA)", len(nr) == 8, f"({len(nr)})")
for lab, z0, z1, note in TODO: P(f"  no-a0-yet row: {lab:28s} z {z0:.2f}-{z1:.2f}  {note}")

# ---------------- style ----------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#555", "xtick.color": "#444", "ytick.color": "#444"})
INK, MUTED = "#16202c", "#6b7480"
LAW = {"FLAT": "#111111", "H(z)": "#d1342f", "PROXY": "#7b3fbf", "M-DEC": "#1b9aaa"}
COL = {"RC100": "#1f5aa6", "CRISTAL": "#e07b00", "M": "#8a5a00", "ALMA": "#2e8b3e"}

fig = plt.figure(figsize=(14, 10.2), dpi=170)
HS = 0.035 + 0.024 * max(len(TODO), 1)          # the strip shrinks as its rows are calculated
sx_bottom = 0.118
ax = fig.add_axes([0.075, sx_bottom + HS + 0.012, 0.885, 0.83 - (sx_bottom + HS + 0.012)])
sx = fig.add_axes([0.075, sx_bottom, 0.885, HS], sharex=ax)
XLO, XHI, YLO, YHI = -0.12, 6.0, 0.17, 30

# ---------------- main: calculated a0 ----------------
ax.set_yscale("log"); ax.set_xlim(XLO, XHI); ax.set_ylim(YLO, YHI)
for x0, x1, t in ((0.6, 2.6, "cosmic noon"), (4.0, 6.0, "first 1.5 billion years")):
    ax.axvspan(x0, x1, color="#eef1f5", zorder=0, lw=0); sx.axvspan(x0, x1, color="#eef1f5", zorder=0, lw=0)
    ax.text(1.05 if t == "cosmic noon" else (x0 + x1) / 2, 23, t, ha="center", color="#8a94a0", fontsize=10, style="italic")
ax.axhspan(YLO, 0.30, color="#f6f2ea", zorder=0, lw=0)
m = Zc <= XHI
lo_b = np.minimum(np.array(cur["DESI DESY5"]), np.array(cur["DESI Union3"]))[m] * U
hi_b = np.maximum(np.array(cur["DESI DESY5"]), np.array(cur["DESI Union3"]))[m] * U
ax.fill_between(Zc[m], lo_b, hi_b, color=LAW["M-DEC"], alpha=0.13, lw=0, zorder=1)
md = np.array(cur["M-DEC"])[m] * U; zz = Zc[m]
ax.plot(zz[zz <= 2.5], md[zz <= 2.5], color=LAW["M-DEC"], lw=2.2, zorder=2)
ax.plot(zz[zz >= 2.5], md[zz >= 2.5], color=LAW["M-DEC"], lw=2.2, ls=(0, (1.2, 2.2)), zorder=2)
ax.text(3.5, 0.53, r"$a_0 \propto \sqrt{\rho_{DE}}$ (DESI)", color=LAW["M-DEC"], fontsize=11, ha="right", fontweight="bold")
for k, kw in (("PROXY", dict(lw=2.2, ls=(0, (5, 3)))), ("H(z)", dict(lw=2.8)), ("FLAT", dict(lw=2.8))):
    ax.plot(Zc[m], np.array(cur[k])[m] * U, color=LAW[k], zorder=2, **kw)
ax.text(4.42, 7.9, r"$a_0$ grows with $H(z)$", color=LAW["H(z)"], fontsize=12.5, ha="right", fontweight="bold")
ax.text(5.95, 4.1, r"$\Lambda$CDM proxy", color=LAW["PROXY"], fontsize=11, ha="right", fontweight="bold")
ax.text(5.95, 1.0, r"constant $a_0$", color=LAW["FLAT"], fontsize=12.5, ha="right", fontweight="bold", va="bottom")
ax.fill_between([XLO, 0.08], U, ALT / 1e-10, color="#444", zorder=6, lw=0)
ax.text(-0.08, 0.60, "today\n(SPARC)", fontsize=9.5, color="#333", ha="left", va="center")
ax.plot([0.0, 0.0], [0.70, 0.90], color="#888", lw=0.8)

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
ax.text(1.38, 5.2, "RC100\n100 discs in 4 bins", color=COL["RC100"], fontsize=10, ha="center", fontweight="bold")
r = pts["ALESS_122.1"]; point(r, 2.13, COL["M"], "*", 360)
ax.annotate("ALESS 122.1\nbest gas data, 1 galaxy", xy=(2.08, f(r, "s_star") * U), xytext=(1.98, 14.5), fontsize=10, ha="right",
            color=COL["M"], fontweight="bold", va="center", arrowprops=dict(arrowstyle="-", color=COL["M"], lw=0.8))
r = pts["ALPINE6 pooled"]; point(r, 4.58, COL["ALMA"], "s", 110, hollow=True)
ax.text(4.46, 1.95, "6 ALMA rotators\n(pooled)", color=COL["ALMA"], fontsize=10, ha="right", va="center", fontweight="bold")
point(pts["CR R_e ind"], 5.12, COL["CRISTAL"], "s", 95); point(pts["CR R_out ind"], 5.36, COL["CRISTAL"], "s", 95)
ax.text(5.46, 2.0, "CRISTAL\n6 discs,\n2 radii", color=COL["CRISTAL"], fontsize=10, ha="left", va="center", fontweight="bold")
# calculated, no solution
NRX = {"SINS_BX610": 2.16, "ALPAKA15": 2.27, "ALPAKA18": 2.40, "ALPAKA19": 2.49, "ALPAKA20": 2.58, "ALPAKA22": 2.94,
       "SPT0418-47": 4.22, "VC5110377875": 4.52}
for o, x in NRX.items():
    ax.scatter([x], [0.215], marker="v", s=70, color=COL["M"] if not o.startswith(("SPT", "VC")) else COL["ALMA"], zorder=6, edgecolor="white", lw=0.6)
AMV = "#6c5b7b"
for r in A274:
    if r["no_root"] == "1":
        ax.scatter([f(r, "z")], [0.188], marker="v", s=60, color=AMV, zorder=6, edgecolor="white", lw=0.6)
    else:
        zz = f(r, "z"); ax.plot([zz, zz], [f(r, "stat68_lo") * U, f(r, "stat68_hi") * U], color=AMV, lw=3.2, zorder=5, solid_capstyle="butt")
        ax.scatter([zz], [f(r, "s_star") * U], marker="h", s=80, facecolor="white", edgecolor=AMV, linewidth=1.8, zorder=6)
        ax.text(zz + 0.08, f(r, "s_star") * U * 1.04, "ALESS 075.1 (Amvrosiadis)\nnear-Newtonian, ill-conditioned", color=AMV, fontsize=8.5, va="center")
ALP = "#6b7f2a"
for r in A272:
    zz = f(r, "z")
    if r["no_root"] == "1":
        ax.scatter([zz], [0.188], marker="v", s=60, color=ALP, zorder=6, edgecolor="white", lw=0.6)
    else:   # stars-only baryons are a LOWER limit, so s* is an UPPER bound; near-Newtonian and ill-conditioned
        sv = f(r, "s_star") * U
        ax.scatter([zz], [sv], marker="o", s=55, facecolor="white", edgecolor=ALP, linewidth=1.8, zorder=6)
        ax.annotate("", xy=(zz, sv / 1.9), xytext=(zz, sv), arrowprops=dict(arrowstyle="-|>", color=ALP, lw=1.6), zorder=6)
ax.text(3.36, 0.52 * 3.30 * U, "ALPAKA 25 / 28: upper\nbounds, ill-conditioned", color=ALP, fontsize=8.5, ha="center", va="top")
DAN = "#9c4a2f"
for r in A273:
    if r["no_root"] == "1" and "pooled" not in r["object"]:
        ax.scatter([f(r, "z")], [0.188], marker="v", s=60, color=DAN, zorder=6, edgecolor="white", lw=0.6)
pall = next(r for r in A273 if "PALL" in r["object"])   # stars-only baryons are a lower limit: the pooled s* is an UPPER bound
zp, sp = f(pall, "z"), f(pall, "s_star") * U
ax.scatter([zp], [sp], marker="o", s=55, facecolor="white", edgecolor=DAN, linewidth=1.8, zorder=6)
ax.annotate("", xy=(zp, sp / 2.3), xytext=(zp, sp), arrowprops=dict(arrowstyle="-|>", color=DAN, lw=1.6), zorder=6)
ax.text(zp + 0.07, sp / 1.75, "Danhaive 41: upper\nbound only (≤ 29×)", color=DAN, fontsize=8.5, ha="left", va="center")
K3 = "#3d5a80"
k3_floor = [r for r in A270 if r["tier"] == "T1" and r["no_root"] == "1"]
ax.scatter([2.35], [0.252], marker="v", s=70, color=K3, zorder=6, edgecolor="white", lw=0.6)
ax.text(2.40, 0.252, f"KMOS3D ×{len(k3_floor)}", color=K3, fontsize=8.5, va="center", fontweight="bold")
pt1 = next(r for r in A270 if r["object"] == "KMOS3D pooled PT1")   # stars only: an UPPER bound; exists only with the hand-added pressure term
zk, sk = 2.40, f(pt1, "s_star") * U
ax.plot([zk, zk], [f(pt1, "stat68_lo") * U, f(pt1, "stat68_hi") * U], color=K3, lw=3.2, zorder=5, solid_capstyle="butt")
ax.scatter([zk], [sk], marker="o", s=55, facecolor="white", edgecolor=K3, linewidth=1.8, zorder=6)
ax.annotate("", xy=(zk, sk / 1.9), xytext=(zk, sk), arrowprops=dict(arrowstyle="-|>", color=K3, lw=1.6), zorder=6)
ax.text(zk + 0.07, 1.12, "KMOS3D 72 fits: ≤ 2.4×", color=K3, fontsize=8.5, va="bottom", fontweight="bold")
HZC = "#5b4636"
hz = A271["HZ9 [M103]"]; zh, shz = 5.62, f(hz, "s_star") * U   # corpus M* branch; the Parlanti branch (<= 49) is off the top of the axis
ax.scatter([zh], [shz], marker="o", s=55, facecolor="white", edgecolor=HZC, linewidth=1.8, zorder=6)
ax.annotate("", xy=(zh, shz / 1.9), xytext=(zh, shz), arrowprops=dict(arrowstyle="-|>", color=HZC, lw=1.6), zorder=6)
ax.text(zh + 0.06, shz, "HZ9 ≤ 15×\n(≤ 49× alt M*)", color=HZC, fontsize=8, va="center", ha="left", clip_on=False)
ROC = "#2e7d6b"
ro_floor = [A277[k] for k in ("J081740 [gas]", "BRI1335-0417 [gas]")]   # primary CO-gas rows; SGP pair vacuous bounds not drawn
for r in ro_floor:
    ax.scatter([f(r, "z")], [0.252], marker="v", s=60, color=ROC, zorder=6, edgecolor="white", lw=0.6)
SNC = "#1f7a8c"
sins_floor = [r for r in A280 if r["no_root"] == "1" and "[" not in r["object"] and r["rc100_match"] == "0" and r["kmos3d_match"] == "0"]   # BX610 is CFG229's
ax.scatter([3.15], [0.252], marker="v", s=70, color=SNC, zorder=6, edgecolor="white", lw=0.6)
ax.text(3.20, 0.252, f"SINS ×{len(sins_floor)}", color=SNC, fontsize=8.5, va="center", fontweight="bold")
ptn = next(r for r in A280 if r["object"] == "SINS pooled PT2_new")   # overlap-free stars-only UPPER bound; nudged from z 2.257 to 1.88
zs, ss = 1.88, f(ptn, "s_star") * U
ax.scatter([zs], [ss], marker="o", s=55, facecolor="white", edgecolor=SNC, linewidth=1.8, zorder=6)
ax.annotate("", xy=(zs, ss / 1.9), xytext=(zs, ss), arrowprops=dict(arrowstyle="-|>", color=SNC, lw=1.6), zorder=6)
ax.text(zs - 0.06, ss, "SINS (z 2.26): ≤ 9×", color=SNC, fontsize=8.5, ha="right", va="center", fontweight="bold")
PKSC = "#bc6c25"
ax.scatter([2.61], [0.188], marker="v", s=60, color=PKSC, zorder=6, edgecolor="white", lw=0.6)   # PKS 0529-549, true z 2.5706, nudged clear of the Amvrosiadis row
ax.scatter([4.055], [0.252], marker="v", s=60, facecolor="white", edgecolor="#8a8a8a", lw=1.3, zorder=6)   # GN20: D 0.90, NOT informative; not counted
ax.text(4.08, 0.33, "GN20 · near-Newtonian,\nnot informative", color="#7a7a7a", fontsize=8, ha="left", va="bottom")
LLC = "#6a4c93"
ax.scatter([2.20], [0.252], marker="v", s=60, color=LLC, zorder=6, edgecolor="white", lw=0.6)   # zC-400569 (z 2.240), nudged clear of KMOS3D's marker
zl8 = A278["zC-488879 [stars+CO a=0.4]"]   # <= 33.4: off the top of the axis; a BARYON-LIMITED bound, not an a0 measurement
ax.annotate("", xy=(1.47, 18.5), xytext=(1.47, 28.5), arrowprops=dict(arrowstyle="-|>", color=LLC, lw=1.6), zorder=6)
ax.scatter([1.47], [28.5], marker="o", s=45, facecolor="white", edgecolor=LLC, linewidth=1.6, zorder=6, clip_on=False)
ax.text(1.40, 18.5, "zC-488879 (Lelli+23): ≤ 33×, baryon-limited\n(SED M* 4× below dynamical)", color=LLC, fontsize=8, ha="right", va="center")
N_NR = 2 + len(sins_floor) + len(ro_floor) + len(k3_floor) + 8 + sum(r["no_root"] == "1" for r in A274) + sum(r["no_root"] == "1" for r in A272) + sum(r["no_root"] == "1" and "pooled" not in r["object"] for r in A273)
ax.text(0.12, 0.222, f"calculated, but no $a_0$ fits ({N_NR} galaxies):\nthe stars + gas already exceed what the rotation needs  ▸",
        fontsize=9.5, color="#7a5a1a", va="center")
# MUSE-DARK (CFG262, fb24a5922): implied a0 in z-thirds BY BARYON ROUTE, reading bD (projected + asymmetric drift, CFG236's
# best-supported reading). Routes are separate series and are never pooled; all inputs are one DC14 fit plus an SED mass.
COL_MD = "#b0548f"
RSTY = {"i": dict(dx=-0.045, mk="^", ls="-", fc=COL_MD, lab="(i) fitted masses"),
        "ii": dict(dx=0.0, mk="s", ls=(0, (4, 2)), fc="white", lab="(ii) SED + H$_2$  (H$_2$-limited)"),
        "iii": dict(dx=0.045, mk="D", ls=(0, (1, 1.6)), fc="#e3b3d1", lab="(iii) SED stars")}
for rt, st in RSTY.items():
    rows = sorted([r for r in M262 if r["route"] == rt], key=lambda r: f(r, "z"))
    xs = [f(r, "z") + st["dx"] for r in rows]; ys = [f(r, "s_star") * U for r in rows]
    ax.plot(xs, ys, color=COL_MD, lw=1.1, ls=st["ls"], zorder=4, alpha=0.8)
    for r, xx, yy in zip(rows, xs, ys):
        if rt == "ii":
            lo, hi = max(f(r, "outer_lo"), 0.30 / U), f(r, "outer_hi")   # clipped at the floor zone
            ax.add_patch(plt.Rectangle((xx - 0.02, lo * U), 0.04, (hi - lo) * U, color=COL_MD, alpha=0.10, lw=0, zorder=3))
        ax.plot([xx, xx], [f(r, "stat68_lo") * U, f(r, "stat68_hi") * U], color=COL_MD, lw=2.6, zorder=5, solid_capstyle="butt")
        ax.scatter([xx], [yy], marker=st["mk"], s=46, facecolor=st["fc"], edgecolor=COL_MD, linewidth=1.4, zorder=6)
lx, ly = 2.72, 21.0
ax.text(lx - 0.05, ly * 1.22, "MUSE-DARK, by baryon route", color=COL_MD, fontsize=9.5, fontweight="bold", ha="left")
for k, (rt, st) in enumerate(RSTY.items()):
    yy = ly / (1.27 ** k)
    ax.plot([lx, lx + 0.14], [yy, yy], color=COL_MD, lw=1.1, ls=st["ls"])
    ax.scatter([lx + 0.07], [yy], marker=st["mk"], s=40, facecolor=st["fc"], edgecolor=COL_MD, linewidth=1.3, zorder=6)
    ax.text(lx + 0.2, yy, st["lab"], color=COL_MD, fontsize=9, va="center")
ax.text(lx - 0.05, ly / (1.27 ** 3), "route-dependent, not an independent $a_0$", color=COL_MD, fontsize=8.5, style="italic", va="center")
# KiDS lensing (CFG261, 80fd3d666): absolute implied-a0 levels in the CFG255 lens-z thirds, by colour class (the class rows
# T-*; the joint rows are never headlines, CFG261 README). M* zero point dominates (lever -1.1); classes disagree at the high-z third.
KCOL = "#2a6f97"
for r in K261:
    zx = f(r, "z") + (-0.02 if r["class"] == "late" else 0.02)
    early = r["class"] == "early"
    olo, ohi = f(r, "outer_lo"), f(r, "outer_hi"); ilo, ihi = f(r, "inner_lo"), f(r, "inner_hi")
    ax.add_patch(plt.Rectangle((zx - 0.025, olo * U), 0.05, (ohi - olo) * U, color=KCOL, alpha=0.08, lw=0, zorder=3))
    ax.add_patch(plt.Rectangle((zx - 0.025, ilo * U), 0.05, (ihi - ilo) * U, color=KCOL, alpha=0.16, lw=0, zorder=3))
    ax.plot([zx, zx], [f(r, "stat95_lo") * U, f(r, "stat95_hi") * U], color=KCOL, lw=1.2, zorder=4)
    ax.plot([zx, zx], [f(r, "stat68_lo") * U, f(r, "stat68_hi") * U], color=KCOL, lw=4.2, zorder=4, solid_capstyle="butt")
    ax.scatter([zx], [f(r, "s_star") * U], marker="D" if early else "o", s=60 if early else 70, zorder=6,
               facecolor="white" if early else KCOL, edgecolor=KCOL, linewidth=1.8 if early else 1.0)
ax.text(0.03, 13.5, "KiDS lensing", color=KCOL, fontsize=10, fontweight="bold", ha="left")
ax.text(0.03, 10.9, "◇ early-type lenses", color=KCOL, fontsize=9.5, ha="left")
ax.text(0.03, 8.9, "● late-type lenses", color=KCOL, fontsize=9.5, ha="left")
MGC = "#e76f51"   # MIGHTEE-HI (CFG279): the PAPER'S published fit level (exponential RAR, authors' M/L), not our estimator
mw = M279["MIGHTEE-HI paper: whole sample, z-averaged"]
ax.plot([f(mw, "z")] * 2, [f(mw, "stat95_lo") * U, f(mw, "stat95_hi") * U], color=MGC, lw=1.2, zorder=6)
ax.scatter([f(mw, "z")], [f(mw, "a0_1e-10_m_s2")], marker="o", s=60, color=MGC, edgecolor="white", lw=1.0, zorder=7)
ax.text(0.03, 7.1, "● MIGHTEE-HI (published fit)", color=MGC, fontsize=9.5, ha="left")
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
    right = not lab.startswith(("Danhaive", "GN20", "Roman", "HZ9"))
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
         "ΛCDM has no $a_0$ (purple is an effective-$a_0$ proxy); κ = ½ fitted.\nTeal: $a_0 \\propto \\sqrt{\\rho_{DE}}$ with the DESI DR2 CPL fit ($w_0, w_a$) = (-0.838, -0.62), dotted beyond z = 2.5; band = DESY5 and Union3.  Points nudged in z for legibility; plot only: chart_a0z_one.py.\nSources: CFG223, CFG227 + CFG237, CFG228, CFG229, CFG270–278, CFG280 (calculated); CFG261 KiDS, CFG262 MUSE-DARK, CFG279 MIGHTEE (low z); CFG197, CFG235, CFG258, L328 (no $a_0$ value).",
         fontsize=8.6, color="#7a828c")
fig.savefig(os.path.join(HERE, "chart_a0z_one_2026-10-01.png"), dpi=170)
P(f"{sum(CHECKS)}/{len(CHECKS)} checks pass; wrote chart_a0z_one_2026-10-01.png")
open(os.path.join(HERE, "chart_a0z_one_2026-10-01.out"), "w").write("\n".join(OUT) + "\n")
