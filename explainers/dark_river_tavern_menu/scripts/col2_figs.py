"""Column 2 of the status board, "The excess family": one picture per tile, plus captions/col2.json.

Plot and read only. Every number comes from a committed lane file (paths below). Run from the menu folder:
    python3 -I scripts/col2_figs.py
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import menu_style as ms  # noqa: E402
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

R = ms.ROOT
RB = R / "rebuild_2026_10_22"
FOOT = {"canonical": "#26323a", "alt": "#8c6d46"}          # two footings, never pooled: two colours
FOOT_LAB = {"canonical": "canonical a0 9.3603e-11", "alt": "alt a0 1.1312e-10"}


def J(p):
    return json.load(open(R / p))


def commit(p):
    try:
        return subprocess.run(["git", "-C", str(R), "log", "-1", "--format=%h", "--", p],
                              capture_output=True, text=True).stdout.strip() or "uncommitted"
    except Exception:
        return "unknown"


def src(paths):
    return [{"path": p, "commit": commit(p)} for p in paths]


CAPS = []

# ----------------------------------------------------------------------------------------------------------------
# c2_01 dwarf satellites
# ----------------------------------------------------------------------------------------------------------------
P_S1 = "rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small_results.json"
P_S1C = "rebuild_2026_10_22/S1_v3_hosted_small/s1_per_system.csv"
P_U1 = "rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content_results.json"
s1 = J(P_S1)
u1 = J(P_U1)["numbers"]
sat = s1["satellites"]
steps = [("Newton\nbaryons", "S0 Newton (E3 g_bar)"),
         ("isolated\nAQUAL", "S2 AQUAL isolated L*0 E-W"),
         ("+ host\nfield", "S3 AQUAL + EFE (E_mid) L*0 E-W"),
         ("v3\nL* floor", "S4 v3: AQUAL + EFE + screening L*floor E-W"),
         ("v3\nL* 90 pc", "S4 v3: AQUAL + EFE + screening L*90 E-W")]
rows = list(csv.DictReader(open(R / P_S1C)))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})
x = np.arange(len(steps) + 1)
for j, ft in enumerate(["canonical", "alt"]):
    vals = [sat[f"{ft}|primary|{k}"]["Delta"] for _, k in steps]
    sds = [sat[f"{ft}|primary|{k}"]["sd"] for _, k in steps]
    b0 = u1["N5"]["satellites"][ft]["stats"]["B0"]
    vals.append(b0[0]); sds.append(b0[1])
    a1.errorbar(x + (j - 0.5) * 0.22, vals, yerr=sds, fmt="o", color=FOOT[ft], capsize=3, ms=6, label=FOOT_LAB[ft])
a1.axhline(0, color=ms.MODEL, lw=1.6)
a1.text(5.45, 0.06, "data = prediction", color=ms.MODEL, fontsize=8.5, ha="right")
a1.set_xticks(x)
a1.set_xticklabels([s[0] for s in steps] + ["U1 dust-\nfree (T3)"], fontsize=8.2)
a1.set_ylabel("median log10(g_obs / g_pred)  [dex]")
a1.set_ylim(-0.2, 2.4)
a1.axvspan(2.6, 5.4, color=ms.STATUS["FAIL"], alpha=0.06)
a1.text(2.65, 2.28, "v3 readings", color=ms.STATUS["FAIL"], fontsize=8.5)
a1.legend(loc="upper left", fontsize=8)
a1.set_title("45 / 46 satellites: gap after each step", fontsize=10, color=ms.INK)

for ft in ["canonical", "alt"]:
    rr = [r for r in rows if r["footing"] == ft]
    xe = np.array([float(r["x_e_mid"]) for r in rr])
    obs = np.array([float(r["log_gobs_gbar"]) for r in rr])
    pred = np.array([float(r["logG_v3_Lfloor"]) for r in rr])
    if ft == "canonical":
        a2.scatter(xe, obs, s=22, color=ms.DATA, label="observed boost g_obs/g_bar", zorder=3)
        a2.scatter(xe, pred, s=22, facecolors="none", edgecolors=ms.MODEL, label="v3 predicted boost (L* floor)",
                   zorder=3)
        for xx, o, p in zip(xe, obs, pred):
            a2.plot([xx, xx], [p, o], color=ms.MUTED, lw=0.5, zorder=1)
a2.set_xscale("log")
a2.set_xlabel("host field x_e = g_host / a0  (canonical)")
a2.set_ylabel("log10 boost over Newton")
a2.legend(loc="lower left", fontsize=8)
a2.set_title("per system (canonical): data sit above v3", fontsize=10, color=ms.INK)
v_c = sat["canonical|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]
v_a = sat["alt|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]
ms.finish(fig, "c2_01_dwarf_satellites", "FAIL", "Dwarf satellites vs the screened law",
          f"FAIL: +{v_c['Delta']:.2f} / +{v_a['Delta']:.2f} dex above v3 at the L* floor "
          f"({v_c['z']:.1f} / {v_a['z']:.1f} sd); dust-free (U1) +{u1['N5']['satellites']['canonical']['stats']['B0'][0]:.2f}"
          f" / +{u1['N5']['satellites']['alt']['stats']['B0'][0]:.2f}",
          "S1_v3_hosted_small (results json, s1_per_system.csv); U1_v3_dust_content N5")
CAPS.append({
    "slug": "c2_01_dwarf_satellites", "name": "Dwarf satellites vs screened law", "status": "FAIL",
    "data": "E3's clean primary sample of Milky Way / M31 dwarf satellites (45 canonical, 46 alt systems; Arroyo free-f "
            "binaries, Upsilon_V = 2, E-W estimator). Statistic: bootstrap median over systems of log10(g_obs/g_pred). "
            "v3 = stiffened AQUAL mu = x/(1+x) solved for each satellite as a Plummer sphere in its host's uniform field.",
    "picture": "Left: the median gap (dex) after each modelling step, both footings with bootstrap sd; the red line at 0 "
               "is 'data = prediction'. The shaded steps are v3 readings (L* floor, L* 90 pc) and U1's dust-free hosted "
               "case. Right: per satellite (canonical) the observed boost over Newton (dark dots) and v3's predicted "
               "boost (open red circles) against the host field x_e, joined by grey lines.",
    "why": "Isolated, the law leaves the satellites about +0.55 dex short; putting them in their host's field (the EFE "
           "that v3's AQUAL has) pulls the prediction toward Newton and the gap grows to +1.33 / +1.30 dex at the L* floor "
           "(9.0 / 8.8 sd), more at L* = 90 pc. The frozen FAIL line (gap >= 3 sd) is met on both footings, also for the "
           "worst-clean data. U1's theorem T3 says a hosted system that falls with its host carries no held dust, so the "
           "satellites would be dust-free and sit +2.00 / +1.99 dex above: STRUCTURAL. Each satellite is a spherical "
           "Plummer in a uniform field (no tides, no non-equilibrium).",
    "numbers": [
        {"what": "v3 gap at L* floor, canonical / alt (dex, sd)", "value": f"{v_c['Delta']:.3f} +- {v_c['sd']:.3f} / "
         f"{v_a['Delta']:.3f} +- {v_a['sd']:.3f}", "file": P_S1},
        {"what": "v3 gap at L* 90 pc, canonical / alt", "value":
         f"{sat['canonical|primary|S4 v3: AQUAL + EFE + screening L*90 E-W']['Delta']:.3f} / "
         f"{sat['alt|primary|S4 v3: AQUAL + EFE + screening L*90 E-W']['Delta']:.3f}", "file": P_S1},
        {"what": "isolated AQUAL (no field) gap, canonical / alt", "value":
         f"{sat['canonical|primary|S2 AQUAL isolated L*0 E-W']['Delta']:.3f} / "
         f"{sat['alt|primary|S2 AQUAL isolated L*0 E-W']['Delta']:.3f}", "file": P_S1},
        {"what": "U1 dust-free (B0) gap, canonical / alt", "value":
         f"{u1['N5']['satellites']['canonical']['stats']['B0'][0]:.3f} +- {u1['N5']['satellites']['canonical']['stats']['B0'][1]:.3f} / "
         f"{u1['N5']['satellites']['alt']['stats']['B0'][0]:.3f} +- {u1['N5']['satellites']['alt']['stats']['B0'][1]:.3f}",
         "file": P_U1},
    ],
    "sources": src([P_S1, P_S1C, P_U1, "rebuild_2026_10_22/S1_v3_hosted_small/README.md",
                    "rebuild_2026_10_22/U1_v3_dust_content/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c2_02 cluster cores
# ----------------------------------------------------------------------------------------------------------------
P_F1 = "rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores_results.json"
P_X11 = "rebuild_2026_10_22/X11_cross_shear_diagnosis/x11_analysis_results.json"
P_X13 = "rebuild_2026_10_22/X13_source_size_test/x13_analysis_results.json"
f1 = J(P_F1)
x11 = J(P_X11)
x13 = J(P_X13)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.3, 1]})
bins = ["INNER", "MID", "OUTER"]
cells = [("PRIMARY h0672", "primary h 0.672"), ("PRIMARY h0686", "primary h 0.686"),
         ("A1 PRIMARY h0672 boost clipped at 1", "boost fixed (A1) h 0.672")]
mk = ["o", "s", "^"]
for j, ft in enumerate(["canonical", "alt"]):
    for i, (key, lab) in enumerate(cells):
        A = [f1["rows"][key][ft][b][0] for b in bins]
        s = [f1["rows"][key][ft][b][1] for b in bins]
        off = (j * 3 + i - 2.5) * 0.09
        a1.errorbar(np.arange(3) + off, A, yerr=s, fmt=mk[i], color=FOOT[ft], ms=5, capsize=2,
                    label=f"{ft}: {lab}" if True else None, alpha=0.95 if i == 0 else 0.7)
fav = f1["favourable"]["h0672"]
for j, ft in enumerate(["canonical", "alt"]):
    A = [fav[ft]["A"][b][0] for b in bins]
    a1.plot(np.arange(3) + 0.33 + j * 0.06, A, "x", color=FOOT[ft], ms=7, mew=1.6)
a1.plot([], [], "x", color=ms.MUTED, label="corner most favourable to the law")
a1.axhline(1, color=ms.MODEL, lw=1.6)
a1.text(-0.45, 1.03, "law on baryons (A = 1)", color=ms.MODEL, fontsize=8.5, ha="left")
a1.set_xticks(range(3))
a1.set_xticklabels(["INNER", "MID (core)", "OUTER"])
a1.set_ylabel("A = measured ΔΣ / v3 law prediction")
a1.set_title(f"{f1['N']} eRASS1 clusters x raw KiDS shear", fontsize=10, color=ms.INK)
a1.legend(fontsize=6.6, loc="upper right", ncol=1)
a1.set_ylim(0.4, 3.6)

labs, zc, za = [], [], []
for lab, d, kc, ka in [("F1 primary\nh 0.672", f1["Z_primary"]["h0672"], "canonical", "alt"),
                       ("F1 primary\nh 0.686", f1["Z_primary"]["h0686"], "canonical", "alt")]:
    labs.append(lab); zc.append(d[kc]); za.append(d[ka])
for h in ["h0672", "h0686"]:
    labs.append(f"X11 all-source\nh 0.{h[2:]}"); zc.append(x11["Z_MID"][f"canonical|{h}"]); za.append(x11["Z_MID"][f"alt|{h}"])
for h in ["h0672", "h0686"]:
    labs.append(f"X13 size-corr.\nh 0.{h[2:]}"); zc.append(x13["Z_MID_corr"][f"canonical|{h}"]["Z"])
    za.append(x13["Z_MID_corr"][f"alt|{h}"]["Z"])
y = np.arange(len(labs))
a2.barh(y - 0.18, zc, height=0.34, color=FOOT["canonical"], label="canonical")
a2.barh(y + 0.18, za, height=0.34, color=FOOT["alt"], label="alt")
a2.axvline(3, color=ms.MODEL, ls="--", lw=1.2)
a2.text(3.05, len(labs) - 0.45, "3σ", color=ms.MODEL, fontsize=8.5)
a2.set_yticks(y); a2.set_yticklabels(labs, fontsize=7.6); a2.invert_yaxis()
a2.set_xlabel("Z of the MID (core) excess over v3's law")
a2.set_xlim(0, 8)
a2.legend(fontsize=8, loc="upper right")
a2.set_title("excess significance, every rebuild", fontsize=10, color=ms.INK)
pc = f1["rows"]["PRIMARY h0672"]["canonical"]["MID"]; pa = f1["rows"]["PRIMARY h0672"]["alt"]["MID"]
ms.finish(fig, "c2_02_cluster_cores", "FAIL", "Cluster cores (326 eRASS1)",
          f"FAIL: core shear x{pc[0]:.2f} / x{pa[0]:.2f} the law (h 0.672); "
          f"Z {min(zc + za):.1f}–{max(zc + za):.1f} across F1, X11, X13",
          "F1_cluster_cores, X11_cross_shear_diagnosis, X13_source_size_test (results json)")
CAPS.append({
    "slug": "c2_02_cluster_cores", "name": "Cluster cores (326 eRASS1)", "status": "FAIL",
    "data": "Stacked tangential shear (ΔΣ) of 326 eRASS1 clusters from raw KiDS sources (21.3 million rows), in INNER / "
            "MID / OUTER radial apertures. v3 prediction: AQUAL mu = x/(1+x) on the clusters' baryons (eRASS1 gas, "
            "stars), native h 0.672 and 0.686, catalogue miscentring. A = measured / predicted.",
    "picture": "Left: A in the three apertures for both footings (dark = canonical, brown = alt), three primary cells "
               "each with error bars; crosses are the corner most favourable to the law; red line A = 1 is the law's "
               "prediction. Right: the Z of the MID (core) excess in every rebuild (F1, X11 all sources, X13 corrected "
               "for the size-split selection), with the 3σ line.",
    "why": "The core (MID) shear sits 1.5–1.9 times above what the law gives on the clusters' baryons, at Z 4.1–6.2 on "
           "every rebuild and both footings, while OUTER is close to 1: a shape problem, not an amplitude knob. Even "
           "the corner most favourable to the law (stars f* 0.30, gas +1σ, deep-X-ray gas factor, X-COP shape) leaves "
           "MID 1.23–1.37 and pushes OUTER below 1. X13 showed X11's source-size trend was a shear selection of the "
           "split, so the excess stands. S4: no allowed μ_K (v3's dust mass term) fixes it; X9: MOG fails too. "
           "Inherited inputs: eRASS1 R500 and distances use flat ΛCDM (70, 0.3), bracketed in F1.",
    "numbers": [
        {"what": "A_MID primary h0672 canonical / alt", "value": f"{pc[0]:.3f} +- {pc[1]:.3f} / {pa[0]:.3f} +- {pa[1]:.3f}",
         "file": P_F1},
        {"what": "A_MID boost-fixed (A1) h0672 / h0686, canonical", "value":
         f"{f1['rows']['A1 PRIMARY h0672 boost clipped at 1']['canonical']['MID'][0]:.3f} / "
         f"{f1['rows']['A1 PRIMARY h0686 boost clipped at 1']['canonical']['MID'][0]:.3f}", "file": P_F1},
        {"what": "Z_MID F1 primary (canonical h0672, h0686; alt h0672, h0686)", "value":
         f"{f1['Z_primary']['h0672']['canonical']:.2f}, {f1['Z_primary']['h0686']['canonical']:.2f}; "
         f"{f1['Z_primary']['h0672']['alt']:.2f}, {f1['Z_primary']['h0686']['alt']:.2f}", "file": P_F1},
        {"what": "Z_MID X11 all-source", "value": ", ".join(f"{k} {v:.2f}" for k, v in x11["Z_MID"].items()), "file": P_X11},
        {"what": "Z_MID X13 selection-corrected", "value": ", ".join(f"{k} {v['Z']:.2f}" for k, v in x13["Z_MID_corr"].items()),
         "file": P_X13},
        {"what": "favourable corner A_MID / A_OUTER h0672 canonical", "value":
         f"{fav['canonical']['A']['MID'][0]:.3f} / {fav['canonical']['A']['OUTER'][0]:.3f}", "file": P_F1},
    ],
    "sources": src([P_F1, P_X11, P_X13, "rebuild_2026_10_22/F1_cluster_cores/README.md",
                    "rebuild_2026_10_22/S4_v3_muK_clusters/README.md", "rebuild_2026_10_22/X9_mog_stvg_check/README.md",
                    "rebuild_2026_10_22/X13_source_size_test/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c2_03 Coma UDGs
# ----------------------------------------------------------------------------------------------------------------
P_S1K = "rebuild_2026_10_22/S1_v3_hosted_small/s1_coma_per_galaxy.csv"
crow = list(csv.DictReader(open(R / P_S1K)))
coma = s1["coma"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.3, 1]})
cc = [r for r in crow if r["footing"] == "canonical"]
xi = np.arange(len(cc))
a1.errorbar(xi - 0.12, [float(r["E_old"]) for r in cc], yerr=[float(r["sE"]) for r in cc], fmt="o", mfc="white",
            color=ms.MUTED, capsize=2, label="vs isolated law (no host field)")
a1.errorbar(xi + 0.12, [float(r["E_v3_dmean"]) for r in cc], yerr=[float(r["sE"]) for r in cc], fmt="o",
            color=ms.DATA, capsize=2, label="vs v3 in Coma's field (mean 3-D distance)")
a1.axhline(0, color=ms.MODEL, lw=1.6)
a1.text(len(cc) - 0.6, 0.1, "data = prediction", color=ms.MODEL, fontsize=8.5, ha="right")
a1.set_xticks(xi)
a1.set_xticklabels([r["name"].replace("J1", "J1​")[:11] for r in cc], rotation=40, ha="right", fontsize=6.8)
a1.set_ylabel("E = 2 ln(σ_obs / σ_pred)")
a1.set_ylim(-1.2, 5.0)
a1.legend(fontsize=8, loc="upper left")
a1.set_title("9 admitted Coma UDGs, canonical footing", fontsize=10, color=ms.INK)

items = [("isolated\n(no field)", "isolated bound (x_e = 0) L*floor"), ("v3, field at\n3-D distance", "S4 v3 dmean L*floor E-W"),
         ("v3, field at\nprojected dist.", "S4 v3 dproj L*floor E-W"), ("v3, field ÷ 2\n(3-D dist.)", "v3 dmean L*floor field/2")]
y = np.arange(len(items) + 1)
for j, ft in enumerate(["canonical", "alt"]):
    zz = [coma[f"{ft}|{k}"]["z_sys"] for _, k in items] + [u1["N5"]["coma"][ft]["B0"]["z_sys"]]
    a2.barh(y + (j - 0.5) * 0.36, zz, height=0.34, color=FOOT[ft], label=ft)
a2.axvline(3, color=ms.MODEL, ls="--", lw=1.2)
a2.set_ylim(len(items) + 0.6, -0.9)
a2.set_xlim(0, 7.2)
a2.text(3.08, -0.6, "frozen FAIL line |z_sys| = 3", color=ms.MODEL, fontsize=8)
a2.set_yticks(y); a2.set_yticklabels([i[0] for i in items] + ["U1: dust-free\n(T3)"], fontsize=7.8)
a2.set_xlabel("z_sys of ⟨E⟩ (with systematics)")
a2.legend(fontsize=8, loc="upper right")
a2.set_title("significance, both footings", fontsize=10, color=ms.INK)
vc = coma["canonical|S4 v3 dmean L*floor E-W"]; va = coma["alt|S4 v3 dmean L*floor E-W"]
ms.finish(fig, "c2_03_coma_udgs", "FAIL", "Coma ultra-diffuse galaxies",
          f"FAIL: in Coma's field +{vc['meanE_dex']:.2f} / +{va['meanE_dex']:.2f} dex above v3, z_sys "
          f"{vc['z_sys']:.1f} / {va['z_sys']:.1f}; isolated only {coma['canonical|isolated bound (x_e = 0) L*floor']['z_sys']:.2f}"
          f" / {coma['alt|isolated bound (x_e = 0) L*floor']['z_sys']:.2f}",
          "S1_v3_hosted_small (results json, s1_coma_per_galaxy.csv); U1_v3_dust_content N5")
CAPS.append({
    "slug": "c2_03_coma_udgs", "name": "Coma ultra-diffuse galaxies", "status": "FAIL",
    "data": "CFG933's 9 admitted Coma ultra-diffuse galaxies (stellar velocity dispersions σ_obs, M★, R_e). Statistic "
            "E = 2 ln(σ_obs/σ_pred), unweighted mean ⟨E⟩, systematics from CFG948's recipe rerun on the v3 prediction. "
            "v3: stiffened AQUAL solved in Coma's measured hydrostatic field (β-model) at the mean 3-D and projected "
            "distances.",
    "picture": "Left: E per galaxy (canonical) with error bars, against the isolated law (open grey) and against v3 in "
               "Coma's field (dark); red line E = 0 is the prediction. Right: z_sys of ⟨E⟩ for each reading, both "
               "footings, with the frozen FAIL line at 3.",
    "why": "Isolated, the UDGs sit only 1.6 / 1.4σ above the law. But v3 has an external-field effect, and Coma's "
           "measured field (x_e ≈ 0.50–1.06 a0) pushes the prediction toward Newton, so all 9 sit above it: ⟨E⟩ +2.58 / "
           "+2.48 ln (+1.12 / +1.08 dex), z_sys 4.3 / 4.1, and still 3.4–3.6 with the field halved. Screening is "
           "irrelevant here. U1's theorem T3 (held dust is weightless in its host) makes it worse: +1.41 dex, z_sys 5.4. "
           "The fail assumes equilibrium in the current field; a UDG far out of equilibrium would escape it.",
    "numbers": [
        {"what": "⟨E⟩ v3 dmean canonical / alt (ln; dex)", "value": f"{vc['meanE']:.3f}; {vc['meanE_dex']:.3f} / "
         f"{va['meanE']:.3f}; {va['meanE_dex']:.3f}", "file": P_S1},
        {"what": "z_sys v3 dmean / dproj canonical", "value": f"{vc['z_sys']:.2f} / {coma['canonical|S4 v3 dproj L*floor E-W']['z_sys']:.2f}",
         "file": P_S1},
        {"what": "z_sys v3 dmean / dproj alt", "value": f"{va['z_sys']:.2f} / {coma['alt|S4 v3 dproj L*floor E-W']['z_sys']:.2f}",
         "file": P_S1},
        {"what": "z_sys isolated canonical / alt", "value": f"{coma['canonical|isolated bound (x_e = 0) L*floor']['z_sys']:.2f} / "
         f"{coma['alt|isolated bound (x_e = 0) L*floor']['z_sys']:.2f}", "file": P_S1},
        {"what": "U1 dust-free: dex, z_sys (both footings)", "value": f"{u1['N5']['coma']['canonical']['B0']['dex']:.3f}, "
         f"{u1['N5']['coma']['canonical']['B0']['z_sys']:.2f}", "file": P_U1},
    ],
    "sources": src([P_S1, P_S1K, P_U1, "rebuild_2026_10_22/S1_v3_hosted_small/README.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c2_04 red lenses
# ----------------------------------------------------------------------------------------------------------------
P_S2 = "rebuild_2026_10_22/S2_v3_lowg_lensing/s2_v3_lowg_lensing_results.json"
s2 = J(P_S2)
cb = s2["cells_brackets"]
fig, ax = plt.subplots(figsize=(10, 5.4))
readings = [("R0", "inventory\nbaryons only"), ("R1", "+0.123 dex\n(CFG667)"), ("R2", "+0.123 + IMF α–σ\n(CFG926 R5)")]
fields = [("zero", "no field", "o"), ("noclu", "primary field", "s"), ("maxclu", "max field", "^")]
for j, ft in enumerate(["canonical", "alt"]):
    for k, (fk, flab, m) in enumerate(fields):
        A = [cb[f"{ft}|central|{r}|{fk}|red"]["A"] for r, _ in readings]
        s = [cb[f"{ft}|central|{r}|{fk}|red"]["sA"] for r, _ in readings]
        off = (j * 3 + k - 2.5) * 0.08
        ax.errorbar(np.arange(3) + off, A, yerr=s, fmt=m, color=FOOT[ft], ms=6, capsize=2,
                    label=f"{ft}, {flab}", alpha=1 if k == 1 else 0.6)
blue_c = cb["canonical|central|R0|noclu|blue"]; blue_a = cb["alt|central|R0|noclu|blue"]
ax.axhline(1, color=ms.MODEL, lw=1.6)
ax.text(0.5, 0.985, "v3 prediction (A = 1)", color=ms.MODEL, fontsize=8.5, ha="center", va="top")
ax.set_xticks(range(3)); ax.set_xticklabels([r[1] for r in readings])
ax.set_xlim(-0.5, 2.5)
ax.set_ylabel("A = measured ΔΣ / v3 prediction (red lenses)")
ax.legend(fontsize=7.4, ncol=2, loc="upper right")
ax.text(-0.45, 0.78, f"for comparison, blue lenses at the primary field: A {blue_c['A']:.2f} / {blue_a['A']:.2f}",
        fontsize=8, color=ms.MUTED)
ax.set_ylim(0.75, 1.75)
r0c = cb["canonical|central|R0|noclu|red"]; r0a = cb["alt|central|R0|noclu|red"]
r2c = cb["canonical|central|R2|noclu|red"]; r2a = cb["alt|central|R2|noclu|red"]
ms.finish(fig, "c2_04_red_lenses", "COND", "Red (early-type) lenses",
          f"CONDITIONAL: inventory {r0c['A']:.2f} / {r0a['A']:.2f} short; with CFG667 + IMF α–σ "
          f"{r2c['A']:.2f} / {r2a['A']:.2f} (consistent)",
          "S2_v3_lowg_lensing/s2_v3_lowg_lensing_results.json (cells_brackets)")
CAPS.append({
    "slug": "c2_04_red_lenses", "name": "Red (early-type) lenses", "status": "COND",
    "data": "KiDS galaxy-galaxy lensing of the record's 181,477 isolated lenses (B21 points in CFG829's low-g window, "
            "g_bar 10^-13.3 to 10^-11.9 m/s², 6 points), split by colour. v3 is forward-modelled as 4GΔΣ of F2's AQUAL "
            "solution with inventory baryons, hot CGM 0.5 M★, and the host field at three levels. A = data / v3.",
    "picture": "Red-lens amplitude A for three baryon readings (inventory only; +0.123 dex from CFG667; +0.123 dex plus "
               "the IMF α–σ posit), at three host-field levels, both footings, with error bars. Red line A = 1 is v3. "
               "The blue-lens A at the primary field is quoted for comparison.",
    "why": "On the stellar inventory alone, red lenses lens 1.32 / 1.20 times more than v3 predicts (5.0σ canonical, "
           "3.5σ alt by the README), while blue lenses are consistent. The excess is removed only by two declared "
           "posits: CFG667's +0.123 dex extra baryons and a bottom-heavy IMF that scales with σ (CFG926), which bring "
           "A to 1.02 / 0.93. So the tile is conditional on those posits; with M★ −0.2 dex the red tile fails on "
           "canonical even with the IMF. The external field barely matters in this window except at the maximum "
           "field. The μ_K²ψ term is not included.",
    "numbers": [
        {"what": "red A, R0 inventory, primary field, canonical / alt", "value": f"{r0c['A']:.3f} +- {r0c['sA']:.3f} / "
         f"{r0a['A']:.3f} +- {r0a['sA']:.3f}", "file": P_S2},
        {"what": "red A, R1 (+0.123 dex), primary field, canonical / alt", "value":
         f"{cb['canonical|central|R1|noclu|red']['A']:.3f} / {cb['alt|central|R1|noclu|red']['A']:.3f}", "file": P_S2},
        {"what": "red A, R2 (+0.123 + IMF), primary field, canonical / alt", "value": f"{r2c['A']:.3f} +- {r2c['sA']:.3f} / "
         f"{r2a['A']:.3f} +- {r2a['sA']:.3f}", "file": P_S2},
        {"what": "blue A, R0, primary field, canonical / alt", "value": f"{blue_c['A']:.3f} / {blue_a['A']:.3f}", "file": P_S2},
        {"what": "red − blue split z, primary field, R0 → R2 (canonical)", "value":
         f"{s2['splits']['canonical|R0|noclu']:.2f} → {s2['splits']['canonical|R2|noclu']:.2f}", "file": P_S2},
    ],
    "sources": src([P_S2, "rebuild_2026_10_22/S2_v3_lowg_lensing/README.md",
                    "rebuild_2026_10_22/S2_v3_lowg_lensing/FROZEN_CRITERIA.md"]),
})

# ----------------------------------------------------------------------------------------------------------------
# c2_05 one selector
# ----------------------------------------------------------------------------------------------------------------
P_T1 = "rebuild_2026_10_22/T1_efe_strength/t1_efe_strength_results.json"
P_T1S = "rebuild_2026_10_22/T1_efe_strength/t1_stage_satcoma.json"
t1 = J(P_T1)
t1s = J(P_T1S)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})
ds = [("SAT", "dwarf satellites"), ("COMA", "Coma UDGs"), ("LENS-P2", "GAMA spec-isolated\nlensing (P2)"),
      ("GC", "outer globulars")]
for j, ft in enumerate(["canonical", "alt"]):
    cs = t1["curves_summary"][ft]
    for i, (k, lab) in enumerate(ds):
        for lo, hi in cs[k]["interval95"]:
            yy = i + (j - 0.5) * 0.3
            a1.plot([lo, hi], [yy, yy], color=FOOT[ft], lw=5, solid_capstyle="butt", alpha=0.85,
                    label=ft if i == 0 else None)
        a1.plot(cs[k]["eps_hat"], i + (j - 0.5) * 0.3, "o", color="white", mec=FOOT[ft], ms=6)
        if cs[k]["failed"]:
            a1.text(1.52, i + (j - 0.5) * 0.3, "fails at every ε", fontsize=7, color=ms.STATUS["FAIL"], va="center")
a1.axvline(1, color=ms.MODEL, lw=1.6)
a1.text(1.03, -0.75, "v3 (ε = 1)", color=ms.MODEL, fontsize=8.5, ha="left")
a1.axvline(0, color=ms.MUTED, lw=0.8, ls=":")
a1.set_yticks(range(len(ds))); a1.set_yticklabels([d[1] for d in ds], fontsize=8.5); a1.invert_yaxis()
a1.set_xlim(-0.05, 2.0); a1.set_ylim(len(ds) - 0.4, -1.0)
a1.set_xlabel("ε = multiplier on v3's host field (0 = no EFE, 1 = v3)")
a1.set_title("95 % interval of ε each dataset wants", fontsize=10, color=ms.INK)
a1.legend(fontsize=8, loc="lower right")

for ft in ["canonical", "alt"]:
    c = t1s["SAT"][ft]
    D = np.array(c["curves"]["primary_EW"]["Delta"]); sd = np.array(c["curves"]["primary_EW"]["sd"])
    a2.errorbar(c["eps"], D, yerr=sd, fmt="o-", color=FOOT[ft], ms=4, capsize=2, label=ft)
a2.axhline(0, color=ms.MODEL, lw=1.6)
a2.text(0.0, 0.04, "data = prediction", color=ms.MODEL, fontsize=8.5, ha="left")
a2.set_xlabel("ε")
a2.set_ylabel("satellites: median gap (dex), L* floor")
a2.set_ylim(-0.1, 1.7)
a2.legend(fontsize=8, loc="center right")
a2.set_title("weaker EFE does not rescue the satellites", fontsize=10, color=ms.INK)
comb_c = t1["combinations"]["canonical"]["V (primary)"]; comb_a = t1["combinations"]["alt"]["V (primary)"]
ms.finish(fig, "c2_05_one_selector", "OPEN", "One selector for the family",
          f"OPEN: one EFE strength does not fit (p {comb_c['p_PG']:.3f} / {comb_a['p_PG']:.3f}); "
          "Coma wants weak, P2 lensing strong; J1, K1, M2 selectors fail",
          "T1_efe_strength (results json, t1_stage_satcoma.json); J1, K1, M2 READMEs")
cc_ = t1["curves_summary"]["canonical"]; ca_ = t1["curves_summary"]["alt"]
CAPS.append({
    "slug": "c2_05_one_selector", "name": "One selector for the family", "status": "OPEN",
    "data": "T1 scales v3's host field by one diagnostic number ε (ε = 1 is v3, ε = 0 no external-field effect) and "
            "re-runs each member through its own lane's solver: S1's satellites and Coma UDGs, P2's GAMA spectroscopic "
            "isolated-galaxy lensing, D10's outer globulars. Selector lanes J1 (potential depth), K1 (braneworld Weyl "
            "fluid) and M2 (K1 + L* screening) are cited from their READMEs.",
    "picture": "Left: each dataset's 95 % interval in ε, both footings (open circle = best ε; 1.5 is the scan edge); "
               "the red line is v3 at ε = 1. Right: the satellites' median gap against ε for both footings; it never reaches the red zero "
               "line.",
    "why": "A single selector would have to explain why satellites, Coma UDGs and cluster cores sit above v3 while other "
           "systems do not. Measured as one EFE strength, the data disagree with each other: Coma wants ε ≤ 0.21 / 0.24, "
           "P2 lensing wants ε ≥ 0.67 / 0.81, and the satellites fail at every ε (still +0.91 / +0.89 dex at ε = 0). "
           "The one-ε consistency test gives p = 0.023 / 0.014, just above the frozen INCONSISTENT line (0.01). The "
           "potential-depth selector J1, the braneworld fluid K1 and its screened version M2 all fail their frozen "
           "rules. The family's membership still has to be re-derived after R1/R2/R6, so the tile stays open.",
    "numbers": [
        {"what": "Coma ε 95 % interval canonical / alt", "value": f"{cc_['COMA']['interval95']} / {ca_['COMA']['interval95']}",
         "file": P_T1},
        {"what": "P2 lensing ε 95 % interval canonical / alt", "value": f"{cc_['LENS-P2']['interval95']} / {ca_['LENS-P2']['interval95']}",
         "file": P_T1},
        {"what": "satellites ε 95 % interval and χ²_min canonical / alt", "value":
         f"{cc_['SAT']['interval95']}, {cc_['SAT']['chi2_min']:.1f} / {ca_['SAT']['interval95']}, {ca_['SAT']['chi2_min']:.1f}",
         "file": P_T1},
        {"what": "satellite gap at ε = 0, canonical / alt (dex)", "value":
         f"{t1s['SAT']['canonical']['curves']['primary_EW']['Delta'][0]:.3f} / {t1s['SAT']['alt']['curves']['primary_EW']['Delta'][0]:.3f}",
         "file": P_T1S},
        {"what": "primary set one-ε test χ²_PG, p canonical / alt", "value":
         f"{comb_c['chi2_PG']:.2f}, {comb_c['p_PG']:.4f} / {comb_a['chi2_PG']:.2f}, {comb_a['p_PG']:.4f}", "file": P_T1},
    ],
    "sources": src([P_T1, P_T1S, "rebuild_2026_10_22/T1_efe_strength/README.md",
                    "rebuild_2026_10_22/J1_potential_selector/README.md", "rebuild_2026_10_22/K1_braneworld_weyl/README.md",
                    "rebuild_2026_10_22/M2_cluster_compact/README.md"]),
})

out = HERE.parent / "captions"
out.mkdir(exist_ok=True)
json.dump(CAPS, open(out / "col2.json", "w"), indent=1, ensure_ascii=False)
print("wrote", len(CAPS), "figures and captions/col2.json")
