"""Audit of summary_figure.png / .pdf (working note, 2026-10-21).

For every number make_figure.py registered as plotted (plotted_numbers.json), this script re-reads the committed source
file with its OWN extraction code (it does not import make_figure.py) and asserts equality within the stated tolerance.
It also: rebuilds the SPARC points, binned medians and the CFG695 weighted rms from the rotmod files; cross-checks the
plotted values against a second committed copy where the record has one (lane README tables, CFG922's K1 copy of CFG687,
cfg689_summary.md); checks the footer wording, the record's wording rules, the absence of personal names and home paths,
that every source is tracked and unmodified in git, and that PROVENANCE.md names each source with its commit hash.

Prints PASS/FAIL per item and a summary; writes figure_audit.out; exits 0 only if nothing fails.
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 figure_audit.py
"""
import codecs
import csv
import glob
import hashlib
import json
import math
import os
import re
import struct
import subprocess
import sys
import zlib

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LN10 = math.log(10.0)
OUT, NPASS, NFAIL = [], [0], [0]


def say(s=""):
    print(s)
    OUT.append(s)


def check(name, ok, detail=""):
    if ok:
        NPASS[0] += 1
    else:
        NFAIL[0] += 1
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    return ok


def R(rel):
    return os.path.join(ROOT, rel)


def L(rel):
    return json.load(open(R(rel)))


CF = "campaign_fresh_gravity/"
S = {
    "sparc": "real_research/data/sparc_data",
    "sparc_readme": "real_research/data/SPARC_table.README.md",
    "fp0": "real_research/derivation_chain_2026/FP0_core_postulates_results.json",
    "cfg695": CF + "CFG695_saturating_vacuum/cfg695_results.json",
    "cfg919": CF + "CFG919_pressure_support_selector/cfg919_results.json",
    "cfg919_readme": CF + "CFG919_pressure_support_selector/README.md",
    "cfg933": CF + "CFG933_udg_sealed_test/cfg933_results.json",
    "cfg933_readme": CF + "CFG933_udg_sealed_test/README.md",
    "cfg687": CF + "CFG687_erass1_shear_stack/cfg687_results.json",
    "cfg687_readme": CF + "CFG687_erass1_shear_stack/README.md",
    "cfg922_K": CF + "CFG922_cluster_core_baryon_recheck/cfg922_K.json",
    "cfg936": CF + "CFG936_below_law_systems/cfg936_results.json",
    "cfg936_readme": CF + "CFG936_below_law_systems/README.md",
    "cfg650": CF + "CFG650_theory_v2_combined_pm/cfg650_native_results.json",
    "cfg650_readme": CF + "CFG650_theory_v2_combined_pm/README.md",
    "cfg650_crit": CF + "CFG650_theory_v2_combined_pm/FROZEN_CRITERIA.md",
    "cfg654_NC1x": CF + "CFG654_independent_inputs/cfg654_native_results_NC1x.json",
    "cfg654_NC2x": CF + "CFG654_independent_inputs/cfg654_native_results_NC2x.json",
    "cfg654_readme": CF + "CFG654_independent_inputs/README.md",
    "cfg909_T": CF + "CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_T.json",
    "cfg909_NC1x": CF + "CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC1x.json",
    "cfg909_NC2x": CF + "CFG909_shear_score_lcdm_input_sensitivity/cfg909_results_NC2x.json",
    "cfg909_readme": CF + "CFG909_shear_score_lcdm_input_sensitivity/README.md",
    "cfg689": CF + "CFG689_native_ruler_bao/cfg689.json",
    "cfg689_summary": CF + "CFG689_native_ruler_bao/cfg689_summary.md",
    "chart_pts": CF + "CHART_a0z_combined_2026-09-30/chart_a0z_points.csv",
    "chart_readme": CF + "CHART_a0z_rar_z0_5_2026-10-01/README.md",
    "cfg303": CF + "CFG303_lcdm_free_inputs/cfg303_rc100_cristal_LCDMFREE_results.json",
    "cfg309": CF + "CFG309_mightee_width_frame/cfg309_cfg301chain_FRAME_summary.json",
    "cfg301": CF + "CFG301_mightee_hi_catalogue_width_chain/cfg301_stageB_results.json",
    "cfg223": CF + "CFG223_a0_over_cosmic_time/cfg223_results.json",
}
PN = json.load(open(os.path.join(HERE, "plotted_numbers.json")))
ITEMS = PN["items"]
EXP = {}          # key -> (expected value, source key)


def exp(key, value, src):
    EXP[key] = (float(value), src)


say("figure_audit: summary_figure (2026-10-21). Every plotted number is re-derived from its committed source.")
say(f"  plotted_numbers.json: {len(ITEMS)} registered numbers")

# ================================================================================================ (a) SPARC
say("\n(a) SPARC radial acceleration relation")
fp0 = L(S["fp0"])["numbers"]
A0F = {"canonical": float(fp0["a0_canonical"]), "alt": float(fp0["a0_rho_total"])}
A0R = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
for f, k in (("canonical", "a0_canonical"), ("alt", "a0_rho_total")):
    exp(f"a.a0_fp0.{f}", A0F[f], "fp0")
    check(f"FP0 {f} a0 equals the record's rounded footing {A0R[f]:.4e} to < 1e-15", abs(A0F[f] - A0R[f]) < 1e-15, f"{A0F[f]:.10e}")
files = sorted(glob.glob(os.path.join(R(S["sparc"]), "*_rotmod.dat")))
h = hashlib.sha256()
for fn in files:
    h.update(os.path.basename(fn).encode() + b"\0" + open(fn, "rb").read())
readme_sha = re.search(r"combined sha256 of the repo set is `([0-9a-f]{64})`", open(R(S["sparc_readme"])).read()).group(1)
check("SPARC rotmod set: 175 files whose combined sha256 equals the one recorded in SPARC_table.README.md", len(files) == 175 and
      h.hexdigest() == readme_sha, f"{len(files)} files, {h.hexdigest()[:16]}...")
src_mf = open(os.path.join(HERE, "make_figure.py"), encoding="utf-8").read()
check("make_figure.py never reads SPARC_table.txt (a saved 404 page, not data)", "SPARC_table" not in src_mf)
exp("a.n_files", len(files), "sparc")
blocks = [np.loadtxt(fn, comments="#", ndmin=2)[:, :6] for fn in files]
A = np.vstack(blocks)
Rk, Vobs, eVobs, Vgas, Vdisk, Vbul = (A[:, i] for i in range(6))


def rar(U):
    gbar = (np.abs(Vgas) * Vgas + U * Vdisk * Vdisk + 1.4 * U * Vbul * Vbul) * 1e6 / (Rk * 3.0857e19)
    gobs = (Vobs * 1e3) ** 2 / (Rk * 3.0857e19)
    good = (gbar > 0) & (gobs > 0) & np.isfinite(gbar) & np.isfinite(gobs) & (Vobs > 0)
    wt = (np.maximum(Vobs, 1.0) / np.maximum(eVobs, 1.0)) ** 2
    return gbar, gobs, good, wt


def nu_s(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


c695 = L(S["cfg695"])["numbers"]["S2"]
grid = [round(0.30 + 0.01 * i, 2) for i in range(91)]
own = {}
for f in ("canonical", "alt"):
    best = None
    for U in grid:
        gbar, gobs, good, wt = rar(U)
        res = np.log10(gobs[good]) - np.log10(nu_s(gbar[good] / A0F[f]) * gbar[good])
        r = math.sqrt(np.sum(wt[good] * res * res) / np.sum(wt[good]))
        if best is None or r < best[0]:
            best = (r, U)
    own[f] = best
    exp(f"a.rms_text.{f}", round(c695[f]["rms"], 3), "cfg695")
    exp(f"a.ups_disk.{f}", c695[f]["U"], "cfg695")
    exp(f"a.rms_recomputed.{f}", c695[f]["rms"], "cfg695")
    exp(f"a.ups_recomputed.{f}", c695[f]["U"], "cfg695")
    check(f"audit's own rebuild of CFG695's statistic ({f}) equals the committed rms and Upsilon", abs(best[0] - c695[f]["rms"]) < 1e-6 and
          best[1] == c695[f]["U"], f"{best[0]:.6f} @ {best[1]:.2f} vs {c695[f]['rms']:.6f} @ {c695[f]['U']:.2f}")
    check(f"audit rebuild equals make_figure's plotted rms ({f}) to 1e-12",
          abs(best[0] - ITEMS[f"a.rms_recomputed.{f}"]["value"]) < 1e-12)
edges = [-12.25 + 0.25 * i for i in range(17)]
for f in ("canonical", "alt"):
    gbar, gobs, good, wt = rar(own[f][1])
    x, y = np.log10(gbar[good]), np.log10(gobs[good])
    rr = y - np.log10(nu_s(gbar[good] / A0F[f]) * gbar[good])
    i = 0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (x >= lo) & (x < hi)
        if m.sum() < 10:
            continue
        for k, v in (("x", np.median(x[m])), ("y", np.median(y[m])), ("y16", np.percentile(y[m], 16)), ("y84", np.percentile(y[m], 84)),
                     ("r", np.median(rr[m])), ("r16", np.percentile(rr[m], 16)), ("r84", np.percentile(rr[m], 84)), ("n", m.sum())):
            exp(f"a.bin.{f}.{i}.{k}", v, "sparc")
        i += 1
gbar, gobs, good, wt = rar(own["canonical"][1])
exp("a.n_points", int(good.sum()), "sparc")
px, py = np.array(PN["sparc_points"]["logx"]), np.array(PN["sparc_points"]["logy"])
ok = px.size == good.sum() and np.max(np.abs(px - np.log10(gbar[good]))) < 1e-6 and np.max(np.abs(py - np.log10(gobs[good]))) < 1e-6
check("the plotted grey SPARC points equal the audit's rebuild (log g_bar, log g_obs) to 1e-6", ok, f"{px.size} points")

# ================================================================================================ (b) excess family
say("\n(b) the excess family")
c919 = L(S["cfg919"])["byfoot"]
c933 = L(S["cfg933"])["byfoot"]
c687 = L(S["cfg687"])["A"]
c922 = L(S["cfg922_K"])["K"]["K1"]
c936 = L(S["cfg936"])
for f in ("canonical", "alt"):
    cs = c919[f]["V0"]["class_summary"]
    for cls, tag in (("SL", "sparc_large"), ("SS", "sparc_small"), ("DW", "dsph")):
        exp(f"b.{tag}.{f}.dex", cs[cls]["dex"], "cfg919")          # the lane's own stored dex value
        exp(f"b.{tag}.{f}.err", cs[cls]["se"] / LN10, "cfg919")
    co = c933[f]["primary"]["samples"]["coma"]
    exp(f"b.coma.{f}.dex", co["mean_Eobs_dex"], "cfg933")
    exp(f"b.coma.{f}.err", co["se_obs"] / LN10, "cfg933")
    key = f"{f}|b0.67|rc0.15|f0.20"
    for band, tag in (("MID", "core"), ("OUTER", "outskirt")):
        a_, sa = c687[key][band]
        exp(f"b.{tag}.{f}.dex", math.log10(a_), "cfg687")
        exp(f"b.{tag}.{f}.err", sa / a_ / LN10, "cfg687")
        a2, sa2 = c922["A_can" if f == "canonical" else "A_alt"][band]
        check(f"CFG687 {band} amplitude ({f}) equals CFG922's K1 copy", abs(a_ - a2) < 1e-12 and abs(sa - sa2) < 1e-12, f"{a_:.4f} ± {sa:.4f}")
    exp(f"b.tdg.{f}.dex", c936["S1"][f]["mean"], "cfg936")
    exp(f"b.tdg.{f}.err", c936["S1"][f]["se"], "cfg936")
    law_u = c936["routes"][f]["law"]["U"]["stats"]
    exp(f"b.dfs.{f}.dex", law_u["rbar"] / LN10, "cfg936")
    exp(f"b.dfs.{f}.err", law_u["se"] / LN10, "cfg936")
    eo = [c936["K2"][f"DF{n}|{f}"]["E_obs"] for n in (2, 4)]
    check(f"DF2/DF4 class mean ({f}) equals the mean of CFG933's per-galaxy E_obs (CFG936 K2 copy)", abs(np.mean(eo) - law_u["rbar"]) < 1e-12)
    exp(f"b.tdg.{f}.newton", np.mean([o["Delta_pred"] for o in c936["routes"][f]["route_i"]["T"]["per_object"]]), "cfg936")
    exp(f"b.dfs.{f}.newton", np.mean([o["E_pred"] for o in c936["routes"][f]["route_i"]["U"]["per_object"]]) / LN10, "cfg936")
    exp(f"b.sparc_rms.{f}", c695[f]["rms"], "cfg695")
txt919, txt933, txt936, txt687 = (open(R(S[k]), encoding="utf-8").read() for k in ("cfg919_readme", "cfg933_readme", "cfg936_readme", "cfg687_readme"))
check("CFG919 README table carries the plotted dSph / SPARC class means (+0.372, +0.332, +0.059, +0.025, +0.001, -0.023 dex)",
      all(s in txt919 for s in ("(+0.372)", "(+0.332)", "(+0.059)", "(+0.025)", "(+0.001)", "(−0.023)")))
check("CFG933 README carries the plotted Coma means (+0.330 / +0.291 dex)", "(+0.330 dex)" in txt933 and "(+0.291 dex)" in txt933)
check("CFG936 README carries the plotted TDG means (-0.690 ± 0.078 / -0.728 ± 0.079 dex)",
      "−0.690 ± 0.078 dex" in txt936 and "−0.728 ± 0.079" in txt936)
check("CFG687 README carries A_MID 1.91 ± 0.12 / 1.75 ± 0.11 and A_OUTER 1.01 ± 0.09 / 0.93 ± 0.08",
      all(s in txt687 for s in ("1.91 ± 0.12", "1.75 ± 0.11", "1.01 ± 0.09", "0.93 ± 0.08")))

# ================================================================================================ (c) cosmic shear
say("\n(c) cosmic shear")
c650 = L(S["cfg650"])["runs"]
runs = {"T1x": ("canonical", c650["L100_N1024_canonical"]["surveys"]["KiDS"], "cfg650", "cfg909_T"),
        "T2x": ("alt", c650["L100_N1024_alt"]["surveys"]["KiDS"], "cfg650", "cfg909_T"),
        "NC1x": ("canonical", L(S["cfg654_NC1x"])["surveys"]["KiDS"], "cfg654_NC1x", "cfg909_NC1x"),
        "NC2x": ("alt", L(S["cfg654_NC2x"])["surveys"]["KiDS"], "cfg654_NC2x", "cfg909_NC2x")}
for n, (f, K, src, s9) in runs.items():
    rob = list(K["robust"].values())
    exp(f"c.{n}.dchi2", K["dchi2"], src)
    exp(f"c.{n}.robust_min", min(rob), src)
    exp(f"c.{n}.robust_max", max(rob), src)
    V = L(S[s9])["variants"]
    om = [V[v]["results"][f]["KiDS"]["dchi2"] for v in V if re.fullmatch(r"OM_[0-9.]+", v)]
    exp(f"c.{n}.om_min", min(om), s9)
    exp(f"c.{n}.om_max", max(om), s9)
    check(f"{n} KiDS class is CONSISTENT in its committed result ({f})", K["class"] == "CONSISTENT", K["class"])
    check(f"{n}: every CFG909 projection-Omega_m variant keeps CONSISTENT", all(V[v]["results"][f]["KiDS"]["class"] == "CONSISTENT"
                                                                              for v in V if v.startswith("OM_")))
n2 = L(S["cfg654_NC2x"])["surveys"]
exp("c.NC2x.des_dchi2", n2["DES"]["dchi2"], "cfg654_NC2x")
check("NC2x DES Y3 class is CONSISTENT (diagnostic)", n2["DES"]["class"] == "CONSISTENT" and not n2["DES"].get("T_OWN_failed", False))
exp("c.NC1x.chi2_F", L(S["cfg654_NC1x"])["surveys"]["KiDS"]["chi2_F"], "cfg654_NC1x")
exp("c.NC2x.chi2_F", n2["KiDS"]["chi2_F"], "cfg654_NC2x")
exp("c.NCS0.chi2_S0", n2["KiDS"]["chi2_S0"], "cfg654_NC2x")
exp("c.native.N_kept", n2["KiDS"]["N_kept"], "cfg654_NC2x")
check("NC1x and NC2x share the same matched control chi2 (NCS0)", abs(L(S["cfg654_NC1x"])["surveys"]["KiDS"]["chi2_S0"] - n2["KiDS"]["chi2_S0"]) < 1e-12)
crit = open(R(S["cfg650_crit"]), encoding="utf-8").read()
m_t = re.search(r"TENSION \(Δχ² ≥ (\d+)\)", crit)
m_e = re.search(r"EXCLUDED \(Δχ² ≥ (\d+) and robustness minimum ≥ (\d+)\)", crit)
exp("c.tension_line", float(m_t.group(1)), "cfg650_crit")
exp("c.excluded_line", float(m_e.group(1)), "cfg650_crit")
t650, t654, t909 = (open(R(S[k]), encoding="utf-8").read() for k in ("cfg650_readme", "cfg654_readme", "cfg909_readme"))
check("CFG650 README table carries T1x -7.70 and T2x -7.18 with their robustness members",
      "| canonical (T1x) | −7.70 | −4.6 / −11.0 / −6.7 / −5.4 |" in t650 and "| alt (T2x) | −7.18 | −4.3 / −10.2 / −6.1 / −5.1 |" in t650)
check("CFG654 README carries NC1x -10.08 (-6.13 / -13.78 / -8.75 / -12.74) and NC2x -9.39 (-5.69 / -12.85 / -7.99 / -11.86)",
      "**−10.08** | −6.13 / −13.78 / −8.75 / −12.74" in t654 and "**−9.39** | −5.69 / −12.85 / −7.99 / −11.86" in t654)
check("CFG654 README carries chi2 144.68 / 145.38 vs 154.76 on 108 points and DES -2.15 CONSISTENT",
      "144.68 / 108" in t654 and "145.38 / 108" in t654 and "154.76" in t654 and "| −2.15 |" in t654)
check("CFG909 README carries the projection-Omega_m extremes (T1x -0.94 / -11.93, T2x -0.92 / -11.09, NC1x -3.11 / -15.80, NC2x -2.93 / -14.69)",
      all(s in t909 for s in ("| −0.94 | −0.92 |", "| −11.93 | −11.09 |", "−3.11 / −6.86 / −9.58 / −10.97 / −15.80", "−2.93 / −6.40 / −8.93 / −10.22 / −14.69")))
check("plotted T2x lower Omega_m end (-0.915) is the primary kept-set value; README rounds it to -0.92 (re-derived set: -0.91)",
      abs(ITEMS["c.T2x.om_max"]["value"] - (-0.9153985333559547)) < 1e-12)

# ================================================================================================ (d) a0(z)
say("\n(d) a0 across redshift")
c689 = L(S["cfg689"])["BAO+SN"]
summ = open(R(S["cfg689_summary"]), encoding="utf-8").read()
for z in ("1.0", "1.2", "1.5", "2.33"):
    q = c689["P1"][z]["sqrtX_q"]
    exp(f"d.band.{z}.q16", q[1], "cfg689"); exp(f"d.band.{z}.q50", q[2], "cfg689"); exp(f"d.band.{z}.q84", q[3], "cfg689")
    check(f"cfg689_summary.md primary row z {z}: {q[2]:.3f} [{q[1]:.3f}, {q[3]:.3f}]", f"| {z} | {q[2]:.3f} [{q[1]:.3f}, {q[3]:.3f}] |" in summ)
q = c689["P6"]["2.0"]["sqrtX_q"]
exp("d.band.2.0.q16", q[1], "cfg689"); exp("d.band.2.0.q50", q[2], "cfg689"); exp("d.band.2.0.q84", q[3], "cfg689")
check("cfg689_summary.md P6 row z 2.0 band [0.561, 1.155]", f"| 2.0 | [{q[1]:.3f}, {q[3]:.3f}] |" in summ)
check("CFG689 z 2.0 band is interpolated, not extrapolated (P6 flag)", c689["P6"]["2.0"]["extrapolated"] is False)
e20 = c689["P6"]["2.5"]["DM14"]["e20_close"]
exp("d.p6_e20", e20, "cfg689")
check("P6 decisive error at z 2.5 is 0.100 dex in the summary (primary, TARGET HARDER)", "| 0.100 (TARGET HARDER) |" in summ and f"{e20:.3f}" == "0.100")
cur = L(S["cfg223"])["curves"]
for zz in (1.0, 2.0, 3.0, 4.0, 5.0):
    exp(f"d.rival.{zz:.1f}", float(np.interp(zz, cur["z"], cur["H(z)"])), "cfg223")
rows = {r["object"]: r for r in csv.DictReader(open(R(S["chart_pts"])))}
P303 = L(S["cfg303"]); P303 = P303.get("numbers", P303)["points"]


def pt(tag, src, z, s, l68, h68, l95, h95):
    for k, v in (("z", z), ("s", s), ("lo68", l68), ("hi68", h68), ("lo95", l95), ("hi95", h95)):
        exp(f"d.pt.{tag}.{k}", v, src)


fr = L(S["cfg309"])["frame"]
qa = fr["q_a0"]
pt("meerkat", "cfg309", 0.0, fr["s"], qa[1] / 9.3603e-11, qa[2] / 9.3603e-11, qa[0] / 9.3603e-11, qa[3] / 9.3603e-11)
r301 = L(S["cfg301"])["numbers"]["results"]
exp("d.pt.meerkat.z", sorted(r301[w]["z_med"] for w in ("W1", "W2", "W3"))[1], "cfg301")
check("CFG309 MeerKAT: s* x 9.3603e-11 equals its absolute a0 (1.311e-10)", abs(fr["s"] * 9.3603e-11 - fr["a0"]) < 1e-15)
for i in (1, 2, 3):
    r = P303["RC100"][f"B Q{i}"]
    pt(f"rc100_q{i}", "cfg303", r["z_med"], r["s"], r["lo68"], r["hi68"], r["lo95"], r["hi95"])
r = P303["RC100"]["B Q4"]
pt("rc100_q4", "cfg303", r["z_med"], r["hi95"], r["hi95"], r["hi95"], r["hi95"], r["hi95"])
exp("d.pt.rc100_q4.unbounded", float(r["unbounded"]), "cfg303")
check("RC100 Q4 has no root (drawn only as its 95% upper bound)", r["unbounded"] is True)
for tag, obj in (("aless", "ALESS_122.1"), ("alpine6", "ALPINE6 pooled")):
    r = rows[obj]
    pt(tag, "chart_pts", float(r["z"]), float(r["s_star"]), float(r["stat68_lo"]), float(r["stat68_hi"]), float(r["stat95_lo"]), float(r["stat95_hi"]))
    check(f"{obj}: chart row has a root and a0 = s* x 9.3603e-11", r["no_root"] == "0" and
          abs(float(r["s_star"]) * 0.93603 - float(r["a0_1e-10_m_s2"])) < 1e-9)
for tag, key in (("cristal_re", "R_e native, six"), ("cristal_rout", "R_out native, six, outermost data marker (primary)")):
    r = P303["CRISTAL"][key]
    pt(tag, "cfg303", r["z_med"], r["s"], r["lo68"], r["hi68"], r["lo95"], r["hi95"])
nf = [int(x) for x in re.findall(r"floor count is now (\d+)", open(R(S["chart_readme"]), encoding="utf-8").read())]
exp("d.n_floor", nf[-1], "chart_readme")
check("chart README: the last stated no-root (floor) count is 53", nf[-1] == 53, f"sequence ends {nf[-3:]}")

# ================================================================================================ every plotted number
say("\nEvery registered plotted number against its source")
check("every plotted number has an independent expectation, and vice versa", set(ITEMS) == set(EXP),
      f"only plotted: {sorted(set(ITEMS) - set(EXP))[:5]}; only expected: {sorted(set(EXP) - set(ITEMS))[:5]}")
for key in sorted(ITEMS):
    if key not in EXP:
        continue
    v, (e, src) = ITEMS[key]["value"], EXP[key]
    tol = max(ITEMS[key]["tol"], 1e-12 * max(1.0, abs(e)))
    check(f"{key} = {v:.6g}", abs(v - e) <= tol and ITEMS[key]["source"] == S[src], f"source {S[src]}; expected {e:.6g}")

# ================================================================================================ figure text and wording
say("\nFigure text, wording rules, names and paths")
FOOTER_REQUIRED = ("Working-note figure, 2026-10-21. AI-assisted research programme, not peer reviewed. κ = ½ fitted; two a0 footings never "
                   "pooled; cold energy is not a particle species. The framework is not a closed theory: the structure-formation engine has "
                   "no established physical parent and the excess family is unexplained.")
check("footer line is exactly the required text", PN["footer"] == FOOTER_REQUIRED)
alltext = "\n".join(PN["texts"])
check("the footer as drawn (line break -> space) equals the required text",
      any(t.replace("\n", " ") == FOOTER_REQUIRED for t in PN["texts"]))
check("panel (a) rms labels show 0.101 and 0.099 (CFG695 rounded)", "0.101 dex canonical" in alltext and "0.099 dex alt" in alltext)
check("panel (c) note quotes 145/108 and NC1x 144.7, NC2x 145.4, control 154.8",
      "145/108" in alltext and "NC1x 144.7" in alltext and "NC2x 145.4" in alltext and "154.8" in alltext and "amplitude-driven" in alltext)
check("panel (d) quotes the 53 no-root galaxies and the 0.10 dex target", "53 further galaxies" in alltext and "σ ≈ 0.10 dex" in alltext)
check("figure states κ = ½ fitted and footings never pooled", "κ = ½ fitted" in alltext and "never pooled" in alltext)
myfiles = [os.path.join(HERE, f) for f in ("make_figure.py", "figure_audit.py", "plotted_numbers.json", "PROVENANCE.md", "figure_caption.txt")]
texts = {os.path.basename(p): open(p, encoding="utf-8").read() for p in myfiles if os.path.exists(p)}
texts["figure"] = alltext
BAD = ["theory" + " closed", "data favour the" + " framework", "data favor the" + " framework", "κ = ½ " + "derived",
       "kappa = 1/2 " + "derived", "dark matter " + "particle"]
for name, t in texts.items():
    hits = [b for b in BAD if b.lower() in t.lower()]
    check(f"{name}: none of the forbidden phrases", not hits, ", ".join(hits))
NAMES = [codecs.decode(x, "rot13") for x in ("mvzzrezna", "pney mvz", "pneycmv")]      # name fragments, encoded so this file holds none
PATHS = ["/Us" + "ers/", "/ho" + "me/", "~" + "/"]
for name, t in texts.items():
    hits = [b for b in NAMES + PATHS if b.lower() in t.lower()]
    check(f"{name}: no personal names or home paths", not hits, ", ".join(hits))
check("caption names SPARC, eRASS1, KiDS-1000, DES Y3 and the panel (d) data", all(k in texts.get("figure_caption.txt", "") for k in
      ("SPARC", "eRASS1", "KiDS-1000", "DES Y3", "DESI", "RC100", "ALESS 122.1", "ALPINE", "CRISTAL", "MIGHTEE")))
ncap = len(re.findall(r"\S+", texts.get("figure_caption.txt", "")))
check("caption length is 120-180 words", 120 <= ncap <= 180, f"{ncap} words")
cap = texts.get("figure_caption.txt", "")
above = [EXP[f"b.{t}.{f}.dex"][0] for t in ("core", "coma", "dsph") for f in ("canonical", "alt")]
check("caption numbers match the record: 3389 points, rms 0.101 / 0.099, excess range 0.24-0.37 dex",
      f"{int(EXP['a.n_points'][0])} points" in cap and f"{round(c695['canonical']['rms'], 3):.3f} / {round(c695['alt']['rms'], 3):.3f} dex" in cap
      and f"{min(above):.2f}–{max(above):.2f} dex" in cap, f"range {min(above):.3f}-{max(above):.3f}")
e689 = L(S["cfg689"])["BAO+SN"]["P1"]
rel = [float(np.interp(float(z), cur["z"], cur["H(z)"])) / e689[z]["E_q"][2] - 1 for z in ("1.0", "1.2", "1.5", "2.33")]
check("PROVENANCE statement: CFG689's native E(z) is 0.6-1.7% below the plotted CFG223 rival at its nodes",
      0.0055 <= min(rel) and max(rel) < 0.0175, ", ".join(f"{x:+.4f}" for x in rel))

# ================================================================================================ output files
say("\nOutput files")
png = os.path.join(HERE, "summary_figure.png")
with open(png, "rb") as fh:
    head = fh.read(33)
w, hgt = struct.unpack(">II", head[16:24])
dpi_ok = False
data = open(png, "rb").read()
i = data.find(b"pHYs")
if i > 0:
    ppx = struct.unpack(">I", data[i + 4:i + 8])[0]
    dpi_ok = abs(ppx * 0.0254 - 300) < 0.5
check("summary_figure.png is a PNG at 300 dpi, 3900 x 3300 px", head[:8] == b"\x89PNG\r\n\x1a\n" and dpi_ok and (w, hgt) == (3900, 3300), f"{w} x {hgt}")
pdf = open(os.path.join(HERE, "summary_figure.pdf"), "rb").read()
check("summary_figure.pdf is a PDF with embedded TrueType fonts (vector text)", pdf[:5] == b"%PDF-" and b"/FontFile2" in pdf, f"{len(pdf)} bytes")
check("PDF metadata names no author", b"/Author" not in pdf)

# ================================================================================================ git: sources tracked and unmodified; provenance hashes
say("\nSources in git, and PROVENANCE.md")


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True).stdout.strip()


def spec(rel):   # pathspec for git; the CFG689 directory is addressed by a glob
    return rel.replace("CFG689_native_ruler_bao", "CFG689*") if "CFG689_" in rel else rel


used = sorted({it["source"] for it in ITEMS.values()})
prov = texts.get("PROVENANCE.md", "")
for rel in used:
    tracked = git("ls-files", "--", spec(rel))
    dirty = git("status", "--porcelain", "--", spec(rel))
    hsh = git("log", "-1", "--abbrev=10", "--format=%h", "--", spec(rel))
    check(f"{rel}: tracked, unmodified, commit {hsh}", bool(tracked) and not dirty)
    m = re.search(r"`" + re.escape(rel) + r"`\s*\|\s*`([0-9a-f]{7,40})`", prov)
    check(f"PROVENANCE.md lists {rel} with its commit hash", bool(m) and m.group(1).startswith(hsh[:7]) and hsh.startswith(m.group(1)[:10]),
          f"listed {m.group(1) if m else None}, git {hsh}")

say(f"\nSUMMARY: {NPASS[0]} PASS / {NFAIL[0]} FAIL")
open(os.path.join(HERE, "figure_audit.out"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
sys.exit(0 if NFAIL[0] == 0 else 1)
