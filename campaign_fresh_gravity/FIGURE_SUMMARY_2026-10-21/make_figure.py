"""Summary figure of the framework's standing (working note, 2026-10-21).  PLOT ONLY.

Every plotted number is read from a committed file of the record (paths below, repo-relative).  The only computations
are (i) the SPARC radial-acceleration points, binned medians and the weighted rms, rebuilt with CFG695's exact recipe
(the CFG4 statistic) from the committed SPARC rotmod files, and (ii) unit conversions: ln -> dex (x / ln 10), a lensing
amplitude A -> log10 A, and the implied-a0 scale s* -> a0(z)/a0(footing) (x 9.3603e-11 / a0_footing).  Everything plotted
is written to plotted_numbers.json; figure_audit.py re-reads every source independently and checks it.

kappa = 1/2 is FITTED.  The two a0 footings (9.3603e-11 and 1.1312e-10 m s^-2) are drawn separately and never pooled.
"Cold energy" is not a particle species.  Not a closed theory.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 make_figure.py      (one core, ~0.3 GB, a few seconds)
"""
import glob
import json
import math
import os
import re

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
ROOT = os.path.dirname(CFG)
LN10 = math.log(10.0)

# ------------------------------------------------------------------------------------------------ sources (repo-relative)
SRC = {
    "sparc_dir": "real_research/data/sparc_data",
    "fp0": "real_research/derivation_chain_2026/FP0_core_postulates_results.json",
    "cfg695": "campaign_fresh_gravity/CFG695_saturating_vacuum/cfg695_results.json",
    "cfg919": "campaign_fresh_gravity/CFG919_pressure_support_selector/cfg919_results.json",
    "cfg933": "campaign_fresh_gravity/CFG933_udg_sealed_test/cfg933_results.json",
    "cfg687": "campaign_fresh_gravity/CFG687_erass1_shear_stack/cfg687_results.json",
    "cfg936": "campaign_fresh_gravity/CFG936_below_law_systems/cfg936_results.json",
    "cfg650": "campaign_fresh_gravity/CFG650_theory_v2_combined_pm/cfg650_native_results.json",
    "cfg650_crit": "campaign_fresh_gravity/CFG650_theory_v2_combined_pm/FROZEN_CRITERIA.md",
    "cfg654_NC1x": "campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC1x.json",
    "cfg654_NC2x": "campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC2x.json",
    "cfg909_T": "campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_T.json",
    "cfg909_NC1x": "campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC1x.json",
    "cfg909_NC2x": "campaign_fresh_gravity/CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC2x.json",
    "cfg689": "campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json",
    "chart_pts": "campaign_fresh_gravity/CHART_a0z_combined_2026-09-30/chart_a0z_points.csv",
    "chart_readme": "campaign_fresh_gravity/CHART_a0z_rar_z0_5_2026-10-01/README.md",
    "cfg303": "campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE_results.json",
    "cfg309": "campaign_fresh_gravity/CFG309_mightee_width_frame/cfg309_cfg301chain_FRAME_summary.json",
    "cfg301": "campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/cfg301_stageB_results.json",
    "cfg223": "campaign_fresh_gravity/CFG223_a0_over_cosmic_time/cfg223_results.json",
}
P = lambda k: os.path.join(ROOT, SRC[k])
J = lambda k: json.load(open(P(k)))

FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # the record's two footings (rounded), never pooled
ITEMS, TEXTS = {}, []


def rec(key, value, src, field, tol=1e-9):
    """register a plotted number (the audit re-derives every key from the source independently)"""
    ITEMS[key] = dict(value=float(value), source=SRC[src], field=field, tol=tol)
    return float(value)


# ================================================================================================ (a) SPARC RAR
fp0 = J("fp0")["numbers"]
A0_FP0 = {"canonical": float(fp0["a0_canonical"]), "alt": float(fp0["a0_rho_total"])}   # CFG695 used these (unrounded)
for f, k in (("canonical", "a0_canonical"), ("alt", "a0_rho_total")):
    rec(f"a.a0_fp0.{f}", A0_FP0[f], "fp0", f"numbers.{k} (used only to reproduce CFG695's rms; differs from the rounded footing by < 1e-15)", tol=0)
files = sorted(f for f in os.listdir(P("sparc_dir")) if f.endswith("_rotmod.dat"))
cols = [np.genfromtxt(os.path.join(P("sparc_dir"), f), comments="#") for f in files]
D = np.concatenate([c for c in cols if c.ndim == 2 and c.shape[1] >= 6])
R_m, Vo, eV, Vg, Vd, Vb = D[:, 0] * 3.0857e19, D[:, 1], D[:, 2], D[:, 3], D[:, 4], D[:, 5]
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
nu_simple = lambda y: 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))    # the law g_N = g^2/(g + a0), solved for g = nu g_N


def sparc_at(U):
    gb = (np.sign(Vg) * Vg ** 2 + U * Vd ** 2 + 1.4 * U * Vb ** 2) * 1e6 / R_m
    go = (Vo * 1e3) ** 2 / R_m
    ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vo > 0)
    w = 1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2
    return gb, go, ok, w


def rms_at(U, a0):
    gb, go, ok, w = sparc_at(U)
    r = np.log10(go[ok]) - np.log10(nu_simple(gb[ok] / a0) * gb[ok])
    return math.sqrt(np.sum(w[ok] * r ** 2) / np.sum(w[ok]))


c695 = J("cfg695")["numbers"]["S2"]
RAR = {}
for f in FOOTS:
    scan = np.array([rms_at(U, A0_FP0[f]) for U in UPS])
    Ubest = float(UPS[int(np.argmin(scan))])
    RAR[f] = dict(U=Ubest, rms=float(scan.min()))
    rec(f"a.rms_text.{f}", round(c695[f]["rms"], 3), "cfg695", f"numbers.S2.{f}.rms (shown to 3 dp)", tol=0)
    rec(f"a.ups_disk.{f}", c695[f]["U"], "cfg695", f"numbers.S2.{f}.U", tol=0)
    ITEMS[f"a.rms_recomputed.{f}"] = dict(value=RAR[f]["rms"], source=SRC["cfg695"], field=f"numbers.S2.{f}.rms (recipe reproduced)", tol=1e-6)
    ITEMS[f"a.ups_recomputed.{f}"] = dict(value=Ubest, source=SRC["cfg695"], field=f"numbers.S2.{f}.U (recipe reproduced)", tol=0)

BINS = np.arange(-12.25, -8.24, 0.25)
binned = {}
for f in FOOTS:
    gb, go, ok, w = sparc_at(RAR[f]["U"])
    lx, ly = np.log10(gb[ok]), np.log10(go[ok])
    res = ly - np.log10(nu_simple(gb[ok] / A0_FP0[f]) * gb[ok])
    rows = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        m = (lx >= lo) & (lx < hi)
        if m.sum() < 10:
            continue
        rows.append(dict(x=float(np.median(lx[m])), y=float(np.median(ly[m])), y16=float(np.percentile(ly[m], 16)),
                         y84=float(np.percentile(ly[m], 84)), r=float(np.median(res[m])), r16=float(np.percentile(res[m], 16)),
                         r84=float(np.percentile(res[m], 84)), n=int(m.sum())))
    binned[f] = rows
    for i, b in enumerate(rows):
        for k in ("x", "y", "y16", "y84", "r", "r16", "r84", "n"):
            ITEMS[f"a.bin.{f}.{i}.{k}"] = dict(value=b[k], source=SRC["sparc_dir"], field=f"binned SPARC at Upsilon_disk {RAR[f]['U']:.2f}", tol=1e-9)
gb0, go0, ok0, _ = sparc_at(RAR["canonical"]["U"])
PTS_X, PTS_Y = np.log10(gb0[ok0]), np.log10(go0[ok0])
rec("a.n_files", len(files), "sparc_dir", "number of *_rotmod.dat files", tol=0)
rec("a.n_points", int(ok0.sum()), "sparc_dir", "points with g_bar > 0, g_obs > 0 at Upsilon_disk 0.60", tol=0)

# ================================================================================================ (b) the excess family
c919 = {f: J("cfg919")["byfoot"][f]["V0"]["class_summary"] for f in FOOTS}
c933 = J("cfg933")["byfoot"]
c687 = J("cfg687")["A"]
c936 = J("cfg936")
KEY687 = {"canonical": "canonical|b0.67|rc0.15|f0.20", "alt": "alt|b0.67|rc0.15|f0.20"}    # CFG687 primary bracket
EX = {}   # class -> footing -> (offset dex, error dex)
for f in FOOTS:
    for cls, tag in (("SL", "sparc_large"), ("SS", "sparc_small"), ("DW", "dsph")):
        EX.setdefault(tag, {})[f] = (rec(f"b.{tag}.{f}.dex", c919[f][cls]["E"] / LN10, "cfg919", f"byfoot.{f}.V0.class_summary.{cls}.E / ln10"),
                                     rec(f"b.{tag}.{f}.err", c919[f][cls]["se"] / LN10, "cfg919", f"byfoot.{f}.V0.class_summary.{cls}.se / ln10"))
    co = c933[f]["primary"]["samples"]["coma"]
    EX.setdefault("coma", {})[f] = (rec(f"b.coma.{f}.dex", co["mean_Eobs"] / LN10, "cfg933", f"byfoot.{f}.primary.samples.coma.mean_Eobs / ln10"),
                                    rec(f"b.coma.{f}.err", co["se_obs"] / LN10, "cfg933", f"byfoot.{f}.primary.samples.coma.se_obs / ln10"))
    for band, tag in (("MID", "core"), ("OUTER", "outskirt")):
        A, sA = c687[KEY687[f]][band]
        EX.setdefault(tag, {})[f] = (rec(f"b.{tag}.{f}.dex", math.log10(A), "cfg687", f"A.{KEY687[f]}.{band}[0] -> log10"),
                                     rec(f"b.{tag}.{f}.err", sA / (A * LN10), "cfg687", f"A.{KEY687[f]}.{band}: sigma_A/(A ln10)"))
    s1 = c936["S1"][f]
    EX.setdefault("tdg", {})[f] = (rec(f"b.tdg.{f}.dex", s1["mean"], "cfg936", f"S1.{f}.mean"),
                                   rec(f"b.tdg.{f}.err", s1["se"], "cfg936", f"S1.{f}.se"))
    lu = c936["routes"][f]["law"]["U"]["stats"]
    EX.setdefault("dfs", {})[f] = (rec(f"b.dfs.{f}.dex", lu["rbar"] / LN10, "cfg936", f"routes.{f}.law.U.stats.rbar / ln10"),
                                   rec(f"b.dfs.{f}.err", lu["se"] / LN10, "cfg936", f"routes.{f}.law.U.stats.se / ln10"))
NEWTON = {}
for f in FOOTS:
    T = c936["routes"][f]["route_i"]["T"]["per_object"]
    U_ = c936["routes"][f]["route_i"]["U"]["per_object"]
    NEWTON.setdefault("tdg", {})[f] = rec(f"b.tdg.{f}.newton", np.mean([o["Delta_pred"] for o in T]), "cfg936",
                                          f"routes.{f}.route_i.T.per_object[*].Delta_pred, mean")
    NEWTON.setdefault("dfs", {})[f] = rec(f"b.dfs.{f}.newton", np.mean([o["E_pred"] for o in U_]) / LN10, "cfg936",
                                          f"routes.{f}.route_i.U.per_object[*].E_pred, mean / ln10")
SCAT = {f: rec(f"b.sparc_rms.{f}", c695[f]["rms"], "cfg695", f"numbers.S2.{f}.rms") for f in FOOTS}

# ================================================================================================ (c) cosmic shear
c650 = J("cfg650")["runs"]
RUNS = [("T1x", "canonical", "inherited", "cfg650", "L100_N1024_canonical", "cfg909_T"),
        ("T2x", "alt", "inherited", "cfg650", "L100_N1024_alt", "cfg909_T"),
        ("NC1x", "canonical", "native", "cfg654_NC1x", None, "cfg909_NC1x"),
        ("NC2x", "alt", "native", "cfg654_NC2x", None, "cfg909_NC2x")]
SH = {}
for name, foot, inp, src, runkey, s909 in RUNS:
    if runkey:
        K = c650[runkey]["surveys"]["KiDS"]
        dchi2, robust, cls = K["dchi2"], K["robust"], K["class"]
        fld = f"runs.{runkey}.surveys.KiDS"
    else:
        K = J(src)["surveys"]["KiDS"]
        dchi2, robust, cls = K["dchi2"], K["robust"], K["class"]
        fld = "surveys.KiDS"
    v909 = J(s909)["variants"]
    om = [v909[v]["results"][foot]["KiDS"]["dchi2"] for v in v909 if v.startswith("OM_") and not v.endswith("_resupport")]
    SH[name] = dict(foot=foot, inp=inp, cls=cls,
                    d=rec(f"c.{name}.dchi2", dchi2, src, f"{fld}.dchi2"),
                    rlo=rec(f"c.{name}.robust_min", min(robust.values()), src, f"{fld}.robust (min over {sorted(robust)})"),
                    rhi=rec(f"c.{name}.robust_max", max(robust.values()), src, f"{fld}.robust (max)"),
                    olo=rec(f"c.{name}.om_min", min(om), s909, f"variants.OM_*[primary kept set].results.{foot}.KiDS.dchi2 (min)"),
                    ohi=rec(f"c.{name}.om_max", max(om), s909, f"variants.OM_*[primary kept set].results.{foot}.KiDS.dchi2 (max)"))
DES_NC2X = rec("c.NC2x.des_dchi2", J("cfg654_NC2x")["surveys"]["DES"]["dchi2"], "cfg654_NC2x", "surveys.DES.dchi2")
CHI_NC1 = rec("c.NC1x.chi2_F", J("cfg654_NC1x")["surveys"]["KiDS"]["chi2_F"], "cfg654_NC1x", "surveys.KiDS.chi2_F")
CHI_NC2 = rec("c.NC2x.chi2_F", J("cfg654_NC2x")["surveys"]["KiDS"]["chi2_F"], "cfg654_NC2x", "surveys.KiDS.chi2_F")
CHI_S0 = rec("c.NCS0.chi2_S0", J("cfg654_NC2x")["surveys"]["KiDS"]["chi2_S0"], "cfg654_NC2x", "surveys.KiDS.chi2_S0")
NK = rec("c.native.N_kept", J("cfg654_NC2x")["surveys"]["KiDS"]["N_kept"], "cfg654_NC2x", "surveys.KiDS.N_kept", tol=0)
crit = open(P("cfg650_crit")).read()
TENSION = rec("c.tension_line", float(re.search(r"TENSION \(Δχ² ≥ (\d+)\)", crit).group(1)), "cfg650_crit", "Classes: TENSION (Δχ² ≥ 4)", tol=0)
EXCL = rec("c.excluded_line", float(re.search(r"EXCLUDED \(Δχ² ≥ (\d+)", crit).group(1)), "cfg650_crit", "Classes: EXCLUDED (Δχ² ≥ 9 ...)", tol=0)

# ================================================================================================ (d) a0 across redshift
c689 = J("cfg689")["BAO+SN"]
BAND = []
for z in ("1.0", "1.2", "1.5", "2.0", "2.33"):
    q = c689["P6"][z]["sqrtX_q"] if z == "2.0" else c689["P1"][z]["sqrtX_q"]
    where = f"BAO+SN.P6.{z}.sqrtX_q" if z == "2.0" else f"BAO+SN.P1.{z}.sqrtX_q"
    BAND.append((float(z), rec(f"d.band.{z}.q16", q[1], "cfg689", where + "[1]"), rec(f"d.band.{z}.q50", q[2], "cfg689", where + "[2]"),
                 rec(f"d.band.{z}.q84", q[3], "cfg689", where + "[3]")))
P6E = rec("d.p6_e20", c689["P6"]["2.5"]["DM14"]["e20_close"], "cfg689", "BAO+SN.P6.2.5.DM14.e20_close")
c223 = J("cfg223")["curves"]
ZC, HZ = np.array(c223["z"]), np.array(c223["H(z)"])
for zz in (1.0, 2.0, 3.0, 4.0, 5.0):
    rec(f"d.rival.{zz:.1f}", float(np.interp(zz, ZC, HZ)), "cfg223", f"curves['H(z)'] at z {zz}")

import csv
cp = {r["object"]: r for r in csv.DictReader(open(P("chart_pts")))}
c303 = J("cfg303")
c303 = c303.get("numbers", c303)["points"]
c309 = J("cfg309")["frame"]
c301 = J("cfg301")["numbers"]["results"]
PTS = []   # (label, z_draw, s, lo68, hi68, lo95, hi95, upper_limit, marker)


def addpt(tag, label, z_true, z_draw, s, l68, h68, l95, h95, src, field, mk, ul=False):
    vals = dict(z=rec(f"d.pt.{tag}.z", z_true, src, field + " z"), s=rec(f"d.pt.{tag}.s", s, src, field + " s"),
                l68=rec(f"d.pt.{tag}.lo68", l68, src, field + " lo68"), h68=rec(f"d.pt.{tag}.hi68", h68, src, field + " hi68"),
                l95=rec(f"d.pt.{tag}.lo95", l95, src, field + " lo95"), h95=rec(f"d.pt.{tag}.hi95", h95, src, field + " hi95"))
    PTS.append(dict(tag=tag, label=label, zd=z_draw, ul=ul, mk=mk, **vals))


zm = float(np.median([c301[w]["z_med"] for w in ("W1", "W2", "W3")]))
q = c309["q_a0"]
addpt("meerkat", "MeerKAT HI", zm, zm, c309["s"], q[1] / 9.3603e-11, q[2] / 9.3603e-11, q[0] / 9.3603e-11, q[3] / 9.3603e-11, "cfg309",
      "frame (s; q_a0[1], q_a0[2] = 68%, q_a0[0], q_a0[3] = 95%, each / 9.3603e-11)", "D")
rec("d.pt.meerkat.z", zm, "cfg301", "numbers.results.W1/W2/W3.z_med, median")
for i, (qq, zd) in enumerate((("B Q1", None), ("B Q2", None), ("B Q3", None))):
    r = c303["RC100"][qq]
    addpt(f"rc100_q{i + 1}", "RC100", r["z_med"], r["z_med"], r["s"], r["lo68"], r["hi68"], r["lo95"], r["hi95"], "cfg303", f"points.RC100['{qq}']", "o")
r = c303["RC100"]["B Q4"]
addpt("rc100_q4", "RC100", r["z_med"], r["z_med"], r["hi95"], r["hi95"], r["hi95"], r["hi95"], r["hi95"], "cfg303", "points.RC100['B Q4'] (no root: 95% upper bound)", "o", ul=True)
rec("d.pt.rc100_q4.unbounded", float(r["unbounded"]), "cfg303", "points.RC100['B Q4'].unbounded", tol=0)
r = cp["ALESS_122.1"]
addpt("aless", "ALESS 122.1", float(r["z"]), float(r["z"]), float(r["s_star"]), float(r["stat68_lo"]), float(r["stat68_hi"]), float(r["stat95_lo"]),
      float(r["stat95_hi"]), "chart_pts", "row ALESS_122.1", "*")
r = cp["ALPINE6 pooled"]
addpt("alpine6", "ALPINE 6 (pooled)", float(r["z"]), float(r["z"]), float(r["s_star"]), float(r["stat68_lo"]), float(r["stat68_hi"]),
      float(r["stat95_lo"]), float(r["stat95_hi"]), "chart_pts", "row 'ALPINE6 pooled'", "s")
for tag, key, dz in (("cristal_re", "R_e native, six", -0.11), ("cristal_rout", "R_out native, six, outermost data marker (primary)", +0.11)):
    r = c303["CRISTAL"][key]
    addpt(tag, "CRISTAL 6", r["z_med"], r["z_med"] + dz, r["s"], r["lo68"], r["hi68"], r["lo95"], r["hi95"], "cfg303", f"points.CRISTAL['{key}']", "p")
NFLOOR = rec("d.n_floor", int(re.findall(r"floor count is now (\d+)", open(P("chart_readme")).read())[-1]), "chart_readme",
             "last 'The floor count is now N' (no-root galaxies on the 2026-10-01 chart)", tol=0)
FOOTFAC = {f: A0["canonical"] / A0[f] for f in FOOTS}       # s* is relative to the canonical footing; ratio to each footing's own a0

# ================================================================================================ figure
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "mathtext.fontset": "dejavusans",
    "font.size": 10, "axes.titlesize": 11.5, "axes.labelsize": 10.5, "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8, "axes.edgecolor": "#333333",
    "xtick.color": "#333333", "ytick.color": "#333333", "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.facecolor": "white",
    "figure.facecolor": "white", "axes.facecolor": "white", "legend.frameon": False, "legend.fontsize": 8.8,
})
COL = {"canonical": "#0072B2", "alt": "#D55E00"}            # Okabe-Ito blue / vermillion (colour-blind safe)
MFC = {"canonical": COL["canonical"], "alt": "white"}       # canonical filled, alt open
INK, GREY, LIGHT = "#1a1a1a", "#6b6b6b", "#d9d9d9"
GREEN, PURPLE = "#009E73", "#CC79A7"
FOOTLAB = {"canonical": "canonical  a$_0$ = 9.3603×10$^{-11}$ m s$^{-2}$", "alt": "alt  a$_0$ = 1.1312×10$^{-10}$ m s$^{-2}$"}

fig = plt.figure(figsize=(13.0, 11.0))
gs = GridSpec(2, 2, figure=fig, left=0.075, right=0.985, top=0.862, bottom=0.112, wspace=0.40, hspace=0.38,
              width_ratios=[1.0, 1.08])


def T(ax, x, y, s, **kw):
    TEXTS.append(s)
    return ax.text(x, y, s, **kw)


def title(ax, s):
    TEXTS.append(s)
    ax.set_title(s, loc="left", fontweight="bold", pad=8)


# ------------------------------------------------------------------ (a)
sub = GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 0], height_ratios=[3.1, 1.0], hspace=0.07)
ax = fig.add_subplot(sub[0]); axr = fig.add_subplot(sub[1], sharex=ax)
ax.scatter(PTS_X, PTS_Y, s=3, color="#8c8c8c", alpha=0.22, lw=0, rasterized=True, zorder=1)
xx = np.linspace(-12.8, -7.7, 400)
ax.plot(xx, xx, color=INK, lw=1.0, ls=(0, (4, 3)), zorder=2)
for f, ls in (("canonical", "-"), ("alt", (0, (6, 2)))):
    gg = 10 ** xx
    ax.plot(xx, np.log10(nu_simple(gg / A0[f]) * gg), color=COL[f], lw=2.0, ls=ls, zorder=3)
for f, dx in (("canonical", -0.035), ("alt", +0.035)):
    b = binned[f]
    x_ = np.array([q_["x"] for q_ in b]) + dx
    y_ = np.array([q_["y"] for q_ in b])
    ax.errorbar(x_, y_, yerr=[y_ - np.array([q_["y16"] for q_ in b]), np.array([q_["y84"] for q_ in b]) - y_], fmt="o", ms=4.6,
                color=COL[f], mfc=MFC[f], mec=COL[f], mew=1.2, elinewidth=1.1, capsize=0, zorder=5)
    r_ = np.array([q_["r"] for q_ in b])
    axr.errorbar(x_, r_, yerr=[r_ - np.array([q_["r16"] for q_ in b]), np.array([q_["r84"] for q_ in b]) - r_], fmt="o", ms=4.2,
                 color=COL[f], mfc=MFC[f], mec=COL[f], mew=1.2, elinewidth=1.1, capsize=0, zorder=5)
ax.set_xlim(-12.62, -7.88); ax.set_ylim(-12.25, -7.55)
ax.set_ylabel(r"log$_{10}$ g$_{\rm obs}$  [m s$^{-2}$]")
plt.setp(ax.get_xticklabels(), visible=False)
title(ax, "(a)  Radial acceleration relation: SPARC, 175 discs")
T(ax, -11.62, -11.52, "1:1 (Newton)", fontsize=8.4, color=INK, rotation=45, rotation_mode="anchor", transform_rotates_text=True,
  ha="left", va="bottom")
T(ax, 0.022, 0.972, "law  g$_N$ = g$^2$/(g + a$_0$),  κ = ½ fitted\n"
  f"one global 3.6 μm M/L per footing (disc {c695['canonical']['U']:.2f} / {c695['alt']['U']:.2f}; bulge 1.4×)",
  fontsize=8.6, color=INK, ha="left", va="top", transform=ax.transAxes)
T(ax, 0.985, 0.022, f"weighted rms about the law (CFG695):\n{round(c695['canonical']['rms'], 3):.3f} dex canonical,  "
  f"{round(c695['alt']['rms'], 3):.3f} dex alt", fontsize=8.6, color=INK, ha="right", va="bottom", transform=ax.transAxes)
T(ax, 0.022, 0.62, f"grey: {int(ok0.sum())} points (disc M/L {RAR['canonical']['U']:.2f})\n"
  "markers: binned medians, bars 16–84%", fontsize=8.0, color=GREY, ha="left", va="top", transform=ax.transAxes)
axr.axhline(0, color=INK, lw=0.9)
for f in FOOTS:
    axr.axhspan(-SCAT[f], SCAT[f], color=COL[f], alpha=0.07, lw=0)
axr.set_ylim(-0.42, 0.42); axr.set_yticks([-0.3, 0, 0.3])
axr.set_ylabel("obs − law\n[dex]", fontsize=9.5)
axr.set_xlabel(r"log$_{10}$ g$_{\rm bar}$  [m s$^{-2}$]")
T(axr, 0.985, 0.88, "shaded: ± weighted rms", fontsize=7.8, color=GREY, ha="right", va="center", transform=axr.transAxes)

# ------------------------------------------------------------------ (b)
ax = fig.add_subplot(gs[0, 1])
ROWS = [  # (tag, label, group)
    ("sparc_large", "SPARC discs, large\nCFG919 class mean", "on"),
    ("sparc_small", "SPARC discs, small\nCFG919 class mean", "on"),
    ("outskirt", "eRASS1 cluster outskirts, 1.2–3 Mpc\nKiDS lensing, log$_{10}$A$_{\\rm OUTER}$ (CFG687)", "on"),
    ("core", "eRASS1 cluster cores, 0.5–1.2 Mpc\nKiDS lensing, log$_{10}$A$_{\\rm MID}$ (CFG687, CFG922)", "above"),
    ("coma", "Coma ultra-diffuse galaxies, N = 9\nCFG933", "above"),
    ("dsph", "Local Group dSphs, N = 83\n(MW, M31, field; CFG919)", "above"),
    ("tdg", "Tidal dwarf galaxies, N = 6\nCFG936", "below"),
    ("dfs", "NGC 1052-DF2 and -DF4\nCFG933 / CFG936", "below"),
]
ny = len(ROWS)
ypos = {tag: ny - 1 - i for i, (tag, _, _) in enumerate(ROWS)}
DY = {"canonical": +0.16, "alt": -0.16}
for g, (y0, y1), lab in (("on", (ypos["outskirt"] - 0.5, ypos["sparc_large"] + 0.5), "on the law"),
                         ("above", (ypos["dsph"] - 0.5, ypos["core"] + 0.5), "above the law"),
                         ("below", (ypos["dfs"] - 0.5, ypos["tdg"] + 0.5), "below the law, at Newton")):
    if g == "above":
        ax.axhspan(y0, y1, color="#f2f2f2", lw=0, zorder=0)
    T(ax, -1.30, y1 - 0.08, lab, ha="left", va="top", fontsize=8.6, color=GREY, style="italic")
ax.axvline(0, color=INK, lw=1.0, zorder=1)
for tag in ("sparc_large", "sparc_small"):
    for f in FOOTS:
        ax.add_patch(Rectangle((-SCAT[f], ypos[tag] + DY[f] - 0.09), 2 * SCAT[f], 0.18, color=COL[f], alpha=0.13, lw=0, zorder=1))
for tag, _, _ in ROWS:
    for f in FOOTS:
        v, e = EX[tag][f]
        ax.errorbar([v], [ypos[tag] + DY[f]], xerr=[[e], [e]], fmt="o" if f == "canonical" else "s", ms=6.0, color=COL[f], mfc=MFC[f],
                    mec=COL[f], mew=1.4, elinewidth=1.5, capsize=2.5, zorder=4)
        if tag in NEWTON:
            ax.plot([NEWTON[tag][f]], [ypos[tag] + DY[f]], marker="|", ms=13, mew=2.0, color=INK, zorder=5)
ax.set_yticks([ypos[t] for t, _, _ in ROWS]); ax.set_yticklabels([lab for _, lab, _ in ROWS], fontsize=8.5, linespacing=1.15)
TEXTS.extend(lab for _, lab, _ in ROWS)
ax.set_ylim(-0.6, ny - 0.4)
ax.set_xlim(-1.32, 0.62)
ax.set_xlabel(r"offset from the law,  log$_{10}$(g$_{\rm obs}$ / g$_{\rm law}$)  [dex]")
title(ax, "(b)  The excess family: offset from the law by system class")
top = ax.secondary_xaxis("top", functions=(lambda d: 10 ** d, lambda r: np.log10(np.clip(r, 1e-6, None))))
top.set_xticks([0.1, 0.2, 0.5, 1, 2, 3]); top.set_xticklabels(["0.1", "0.2", "0.5", "1", "2", "3"], fontsize=8.5)
top.tick_params(axis="x", colors=GREY, length=3, pad=1.5); top.spines["top"].set_color(GREY)
top.set_xlabel("ratio  g$_{\\rm obs}$ / g$_{\\rm law}$", fontsize=8.2, color=GREY, labelpad=3)
TEXTS.append("ratio  g$_{\\rm obs}$ / g$_{\\rm law}$")
leg = [Line2D([], [], marker="|", ls="none", ms=11, mew=2.0, color=INK, label="zero cold energy (≈ Newton) expectation, CFG936"),
       Patch(color="#999999", alpha=0.35, lw=0, label="SPARC point scatter (± weighted rms, CFG695)")]
ax.legend(handles=leg, loc="lower right", bbox_to_anchor=(1.0, 0.075), fontsize=8.0, handlelength=1.4, frameon=True, facecolor="white",
          edgecolor="none", framealpha=1.0)
TEXTS.extend(h.get_label() for h in leg)
T(ax, 0.985, 0.018, "bars: ±1 s.e. of the class mean (record convention); EFE-free law", transform=ax.transAxes, fontsize=7.8, color=GREY,
  ha="right", va="bottom", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))

# ------------------------------------------------------------------ (c)
ax = fig.add_subplot(gs[1, 0])
order = ["T1x", "T2x", "NC1x", "NC2x"]
yc = {n: len(order) - 1 - i for i, n in enumerate(order)}
ax.axvspan(TENSION, 12, color="#efefef", lw=0, zorder=0)
ax.axvline(0, color=INK, lw=1.0, zorder=1)
ax.axvline(TENSION, color=INK, lw=1.3, ls=(0, (1, 2.2)), zorder=2)
ax.axvline(EXCL, color=GREY, lw=1.0, ls=(0, (5, 3)), zorder=2)
T(ax, TENSION + 0.35, 4.25, f"TENSION\nΔχ² ≥ {TENSION:.0f}", fontsize=8.4, color=INK, ha="left", va="center")
T(ax, EXCL + 0.35, 4.25, f"EXCLUDED\nΔχ² ≥ {EXCL:.0f}", fontsize=8.4, color=GREY, ha="left", va="center")
YL = {"T1x": "T1x · canonical · inherited ICs (CFG650)", "T2x": "T2x · alt · inherited ICs (CFG650)",
      "NC1x": "NC1x · canonical · native ICs (CFG654)", "NC2x": "NC2x · alt · native ICs (CFG654)"}
for n in order:
    s, f, y = SH[n], SH[n]["foot"], yc[n]
    T(ax, -17.2, y + 0.42, YL[n], fontsize=8.6, color=COL[f], fontweight="bold", ha="left", va="center")
    ax.plot([s["olo"], s["ohi"]], [y - 0.17] * 2, color=COL[f], lw=1.6, solid_capstyle="butt", zorder=3)
    ax.plot([s["olo"], s["ohi"]], [y - 0.17] * 2, ls="none", marker="|", ms=8, mew=1.6, color=COL[f], zorder=3)
    ax.plot([s["rlo"], s["rhi"]], [y + 0.08] * 2, color=COL[f], lw=7.5, alpha=0.38, solid_capstyle="butt", zorder=3)
    ax.plot([s["d"]], [y + 0.08], marker="o" if f == "canonical" else "s", ms=7.2, color=COL[f], mfc=MFC[f], mec=COL[f], mew=1.6, zorder=5)
    T(ax, s["rhi"] + 0.45, y + 0.08, f"{s['d']:.2f}".replace("-", "−"), fontsize=8.4, color=COL[f], ha="left", va="center")
ax.plot([DES_NC2X], [yc["NC2x"] - 0.48], marker="D", ms=5.5, mfc="white", mec=INK, mew=1.2, ls="none", zorder=5)
T(ax, DES_NC2X - 0.5, yc["NC2x"] - 0.48, f"DES Y3 for NC2x (DES diagnostic only here): {DES_NC2X:.2f}".replace("-", "−"), fontsize=8.0,
  color=INK, ha="right", va="center")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_ylim(-1.55, 4.85); ax.set_xlim(-17.5, 11.5)
ax.set_xlabel("KiDS-1000 Δχ² = framework run − its matched Poisson control  (negative: framework fits better)", fontsize=9.6)
title(ax, "(c)  Cosmic shear, raw KiDS-1000 ξ$_\\pm$: all four runs CONSISTENT")
leg = [Line2D([], [], color="#777777", lw=7.5, alpha=0.38, label="robustness set (widen2, noIA, held, DESI / LOC)"),
       Line2D([], [], color="#777777", lw=1.6, marker="|", ms=8, mew=1.6, label="projection Ω$_m$ 0.2806–0.3308 (CFG909)"),
       Line2D([], [], color="#777777", marker="o", ls="none", ms=6.5, label="as scored (value printed)")]
ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0.0, 1.02), fontsize=8.0, handlelength=2.0, borderaxespad=0.2)
TEXTS.extend(h.get_label() for h in leg)
note = (f"lead is amplitude-driven; absolute χ² ≈ 145/{NK:.0f} for both native arms\n"
        f"(NC1x {CHI_NC1:.1f}, NC2x {CHI_NC2:.1f}; matched control {CHI_S0:.1f}): not a good absolute fit")
T(ax, 0.985, 0.025, note, transform=ax.transAxes, fontsize=8.0, color=INK, ha="right", va="bottom",
  bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=LIGHT, lw=0.8))

# ------------------------------------------------------------------ (d)
ax = fig.add_subplot(gs[1, 1])
ax.set_yscale("log")
YLO, YHI, YCLIP = 0.042, 70.0, 0.115
zc = ZC <= 5.75
ax.plot(ZC[zc], HZ[zc], color=PURPLE, lw=2.4, zorder=2)
ax.axhline(1.0, color=INK, lw=1.6, zorder=2)
zb = np.array([b[0] for b in BAND]); lo = np.array([b[1] for b in BAND]); md = np.array([b[2] for b in BAND]); hi = np.array([b[3] for b in BAND])
ax.fill_between(zb, lo, hi, color=GREEN, alpha=0.30, lw=0, zorder=1.5)
ax.plot(zb, md, color=GREEN, lw=1.6, zorder=2.5)
ax.fill_between([2.33, 2.5], [lo[-1]] * 2, [hi[-1]] * 2, color=GREEN, alpha=0.12, lw=0, zorder=1.5)
T(ax, 2.42, hi[-1] * 1.09, "extrap.", fontsize=7.6, color=GREEN, ha="center", va="bottom")
for p in PTS:
    for f in FOOTS:
        k = FOOTFAC[f]
        x = p["zd"] + (-0.045 if f == "canonical" else 0.045)
        if p["ul"]:
            ax.annotate("", xy=(x, p["s"] * k / 2.2), xytext=(x, p["s"] * k), arrowprops=dict(arrowstyle="-|>", color=COL[f], lw=1.3), zorder=5)
            ax.plot([x], [p["s"] * k], marker="_", ms=9, mew=2.0, color=COL[f], zorder=6)
            continue
        l95 = max(p["l95"] * k, YCLIP); l68 = max(p["l68"] * k, YCLIP)
        ax.plot([x, x], [l95, min(p["h95"] * k, YHI)], color=COL[f], lw=0.9, zorder=4)
        ax.plot([x, x], [l68, min(p["h68"] * k, YHI)], color=COL[f], lw=3.2, solid_capstyle="butt", zorder=4, alpha=0.9)
        if p["l95"] * k < YCLIP:     # no lower bound: the bar is open-ended downward
            ax.plot([x], [YCLIP], marker="v", ms=3.6, color=COL[f], zorder=4)
        ax.plot([x], [p["s"] * k], marker=p["mk"], ms=9.5 if p["mk"] == "*" else 6.2, color=COL[f], mfc=MFC[f], mec=COL[f], mew=1.3, zorder=6)
LBL = [("MeerKAT HI (z 0.07)", 0.0, 0.56, "left"), ("RC100, z bins\n0.81 / 1.36 / 2.01", 0.81, 4.4, "center"), ("RC100 Q4\n(z 2.26): no root", 2.38, 0.215, "left"),
       ("ALESS 122.1", 2.13, 17.5, "left"), ("ALPINE 6\npooled", 4.36, 2.3, "right"), ("CRISTAL 6\n(R$_e$, R$_{\\rm out}$)", 5.27, 26.0, "center")]
for s_, x_, y_, ha in LBL:
    T(ax, x_, y_, s_, fontsize=7.9, color=INK, ha=ha, va="center", linespacing=1.1)
T(ax, 3.45, 6.3, "rival: a$_0 \\propto$ H(z)", fontsize=9.0, color=PURPLE, fontweight="bold", ha="center", va="bottom")
T(ax, 3.35, 1.07, "flat a$_0$ (constant ρ$_{\\rm DE}$)", fontsize=9.0, color=INK, fontweight="bold", ha="center", va="bottom")
T(ax, 2.62, 0.70, "framework's own\nBAO-ruler band, 68%\n(a$_0 \\propto \\sqrt{\\rho_{\\rm DE}(z)}$, CFG689)", fontsize=8.2, color=GREEN,
  fontweight="bold", ha="left", va="top")
ax.set_xlim(-0.12, 5.75); ax.set_ylim(YLO, YHI)
ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]); ax.set_yticklabels(["0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel("redshift  z")
ax.set_ylabel(r"a$_0$(z) / a$_0$(footing, today)")
title(ax, "(d)  a$_0$ across redshift: flat (framework) vs a$_0 \\propto$ H(z)")
T(ax, 0.015, 0.985, "Not decidable from today's data: no sample separates the two.\n"
  f"Decisive: one kinematic a$_0$ at z ≈ 2.5 with σ ≈ {P6E:.2f} dex (CFG689 P6).",
  transform=ax.transAxes, fontsize=8.2, color=INK, ha="left", va="top")
T(ax, 0.985, 0.012, f"bars: thick 68%, thin 95% statistical; baryon-mass systematics not drawn.  "
  f"{int(NFLOOR)} further galaxies at z ≈ 2–5:\nno a$_0$ solution (baryons ≥ dynamics), not drawn.  $\\blacktriangledown$ = no lower bound.",
  transform=ax.transAxes, fontsize=7.4, color=GREY, ha="right", va="bottom")

# ------------------------------------------------------------------ figure-level text
HEAD = "Where the framework stands: four views of the record (working-note figure)"
T(fig, 0.075, 0.966, HEAD, fontsize=15, fontweight="bold", color=INK, ha="left", va="center")
fl = [Line2D([], [], marker="o", ls="-", lw=1.6, ms=6.5, color=COL["canonical"], mfc=MFC["canonical"], label=FOOTLAB["canonical"]),
      Line2D([], [], marker="s", ls=(0, (6, 2)), lw=1.6, ms=6.5, color=COL["alt"], mfc=MFC["alt"], mec=COL["alt"], mew=1.4, label=FOOTLAB["alt"])]
fig.legend(handles=fl, loc="center left", bbox_to_anchor=(0.068, 0.930), ncol=2, fontsize=9.5, handlelength=2.6, columnspacing=2.2)
TEXTS.extend(FOOTLAB.values())
T(fig, 0.985, 0.930, "filled = canonical, open = alt  ·  two a$_0$ footings, never pooled  ·  κ = ½ fitted", fontsize=9.3, color=GREY,
  ha="right", va="center")
FOOTER = ("Working-note figure, 2026-10-21. AI-assisted research programme, not peer reviewed. κ = ½ fitted; two a0 footings never pooled; "
          "cold energy is not a particle species. The framework is not a closed theory: the structure-formation engine has no "
          "established physical parent and the excess family is unexplained.")
FOOTER_WRAPPED = FOOTER.replace("cold energy is not a particle species. ", "cold energy is not a particle species.\n")
T(fig, 0.075, 0.040, FOOTER_WRAPPED, fontsize=8.4, color="#404040", ha="left", va="center", linespacing=1.35)
SRCLINE = ("Data: SPARC; eRASS1 clusters × KiDS-1000 lensing; KiDS-1000 and DES Y3 cosmic shear; DESI BAO + Pantheon+ (CFG689); "
           "RC100, ALESS 122.1, ALPINE, CRISTAL, MIGHTEE-HI.  Sources and checks: PROVENANCE.md, figure_audit.py.")
T(fig, 0.075, 0.011, SRCLINE, fontsize=7.4, color=GREY, ha="left", va="center")

out_png, out_pdf = os.path.join(HERE, "summary_figure.png"), os.path.join(HERE, "summary_figure.pdf")
META = {"Title": "Framework standing summary (working note, 2026-10-21)", "Author": "", "Subject": "plot only; see PROVENANCE.md"}
fig.savefig(out_png, dpi=300, metadata={"Title": META["Title"]})
fig.savefig(out_pdf, metadata={"Title": META["Title"], "Subject": META["Subject"]})

json.dump(dict(items=ITEMS, texts=TEXTS, footer=FOOTER,
               sparc_points=dict(upsilon_disk=RAR["canonical"]["U"], logx=[round(v, 7) for v in PTS_X.tolist()],
                                 logy=[round(v, 7) for v in PTS_Y.tolist()]),
               files=dict(png="summary_figure.png", pdf="summary_figure.pdf", dpi=300)),
          open(os.path.join(HERE, "plotted_numbers.json"), "w"), indent=1, ensure_ascii=False)
print(f"wrote summary_figure.png / .pdf and plotted_numbers.json: {len(ITEMS)} registered numbers, {len(TEXTS)} text items")
print(f"SPARC rms reproduced: canonical {RAR['canonical']['rms']:.6f} @ {RAR['canonical']['U']:.2f} (CFG695 {c695['canonical']['rms']:.6f}); "
      f"alt {RAR['alt']['rms']:.6f} @ {RAR['alt']['U']:.2f} (CFG695 {c695['alt']['rms']:.6f})")
