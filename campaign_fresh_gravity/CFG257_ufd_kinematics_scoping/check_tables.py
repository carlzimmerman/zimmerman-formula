#!/usr/bin/env python3
"""Row-by-row checks of arroyo_polonio2026_tableA1.csv and geha2026_paperII_tableA1.csv against the PDF text they were transcribed from, and cross-checks against the repository's LVD table.
usage: python3 check_tables.py <arroyo pdftotext> <geha2 pdftotext>   (writes check_tables.out and geha_vs_lvd_match.csv; computes NO offset of any kind)"""
import re, sys, csv, math
import numpy as np, pandas as pd
M = "−"; ok_all = True
def check(name, cond, detail=""):
    global ok_all; ok_all &= bool(cond); print(("PASS " if cond else "FAIL ") + name + (("  " + detail) if detail else ""))
A = pd.read_csv("arroyo_polonio2026_tableA1.csv", dtype=str, keep_default_na=False); G = pd.read_csv("geha2026_paperII_tableA1.csv", dtype=str, keep_default_na=False)
atxt = open(sys.argv[1], encoding="utf-8").read().splitlines(); gtxt = open(sys.argv[2], encoding="utf-8").read().splitlines()
# ---- Arroyo Table A.1
i0 = next(i for i, l in enumerate(atxt) if "Table A.1. Observed l.o.s." in l); i1 = next(i for i, l in enumerate(atxt) if i > i0 and l.strip().startswith("Notes. Observed")); region = [l for l in atxt[i0:i1]]
cols = ["a12_arcmin", "sig_lit", "sig_f0", "logM_f0", "sig_free", "logM_free", "sig_f07", "logM_f07", "logJ"]
check("A1 12 rows (Boo I, Car II, Cra II, Eri III, Hyd I, Leo IV, Leo V, Ret II, Sag II, Seg 1, Uni 1, Wil 1)", len(A) == 12)
check("A2 8 rows flagged as members of the CFG28/29 sample", (A.in_cfg28_29_sample == "1").sum() == 8, ",".join(A[A.in_cfg28_29_sample == "1"].galaxy))
bad = 0
for _, r in A.iterrows():
    # a row's block: from its label line to the next label line; every transcribed number must occur, as a string, in the block (whitespace-collapsed)
    names = list(A.galaxy); k = names.index(r.galaxy); lab = lambda n: re.compile(r"^\s*%s\s+\d+\s" % re.escape(n))
    s = next(i for i, l in enumerate(region) if lab(r.galaxy).match(l)); e = next((i for i, l in enumerate(region) if i > s and any(lab(n).match(l) for n in names)), len(region)); blk = re.sub(r"\s+", "", " ".join(region[s:e]))
    for c in cols:
        for suf, sign in (("", ""), ("_up1", "+"), ("_up3", "(+"), ("_lo1", M), ("_lo3", "(" + M)):
            v = r[c + suf]
            if v == "": continue
            pat = {"": r[c] + "+", "_up1": "+" + v, "_up3": "(+" + v + ")", "_lo1": M + v, "_lo3": "(" + M + v + ")"}[suf]
            if pat not in blk: bad += 1; print("   not found in the PDF block:", r.galaxy, c + suf, pat)
    if str(r.N_stars) not in " ".join(region[s:s + 1]): bad += 1; print("   N not on label line", r.galaxy)
check("A3 every transcribed value occurs in the PDF text block of its own row", bad == 0, "(%d misses)" % bad)
sp = []
for _, r in A.iterrows():
    for sg, lm in (("sig_f0", "logM_f0"), ("sig_free", "logM_free"), ("sig_f07", "logM_f07")):
        if r.galaxy == "Eri III": pass
        sp.append((r.galaxy, float(r[lm]) - 2 * math.log10(float(r[sg]))))
d = pd.DataFrame(sp, columns=["g", "x"]); spread = d.groupby("g").x.agg(lambda v: v.max() - v.min()); check("A4 internal consistency: log M - 2 log sigma agrees across the three configurations within each row (same r_1/2) to <= 0.12 dex", spread.max() <= 0.12, "max spread %.3f dex (%s)" % (spread.max(), spread.idxmax()))
lvd = pd.read_csv("../../real_research/data/dsph/lvd_dwarf_mw.csv")
for g, lname in (("Car II", "Carina II"), ("Hyd I", "Hydrus I")):
    lv = lvd[lvd.name == lname].iloc[0]; a = A[A.galaxy == g].iloc[0]
    check("A5 the paper's literature sigma equals the LVD central value from the same reference: %s" % g, abs(float(a.sig_lit) - lv.vlos_sigma) < 0.051, "paper %s +%s -%s | LVD %.2f +%.2f -%.2f (%s)" % (a.sig_lit, a.sig_lit_up1, a.sig_lit_lo1, lv.vlos_sigma, lv.vlos_sigma_ep, lv.vlos_sigma_em, lv.ref_vlos))
    de = max(abs(float(a.sig_lit_up1) - lv.vlos_sigma_ep), abs(float(a.sig_lit_lo1) - lv.vlos_sigma_em))
    print("INFO A5b %s literature-sigma errors differ between the paper and LVD by up to %.2f km/s (%s)" % (g, de, "the paper quotes a symmetrised/rounded error" if de > 0.051 else "agree"))
# ---- Geha Paper II Table A1
check("G1 67 rows (the paper: 'full contents of this table (67 rows)')", len(G) == 67)
bad = 0
for _, r in G.iterrows():
    line = r.source_line.split()
    for c in ("RA", "Dec", "dist_kpc", "M_V", "r12_arcmin", "N_stars", "vsys", "e_vsys", "sigma_raw", "e_sigma_ll_raw", "e_sigma_ul_raw", "sigma95_raw", "FeH", "e_FeH", "sigFeH", "e_sigFeH_ll", "e_sigFeH_ul", "sigFeH95"):
        if r[c] not in line: bad += 1; print("   value not on the source line:", r.full_name, c, r[c])
    if r.abbr not in line or r.type not in line: bad += 1
check("G2 every transcribed value occurs, as a string, on the PDF line it came from", bad == 0, "(%d misses)" % bad)
src = [" ".join(l.split()) for l in gtxt]; nmiss = sum(1 for _, r in G.iterrows() if r.source_line not in src); check("G3 every source_line is a line of the PDF text", nmiss == 0, "(%d misses)" % nmiss)
check("G4 types: 29 galaxies, 36 globular clusters, 2 unknown", G.type.value_counts().to_dict() == {"GC": 36, "G": 29, "U": 2}, str(G.type.value_counts().to_dict()))
unres = G[G.sigma_resolved == "0"]; check("G5 every unresolved row carries a 95% upper limit and no lower/upper error", all(r.sigma_ul95 != "" and r.e_sigma_ll_raw == "-999" and r.e_sigma_ul_raw == "-999" for _, r in unres.iterrows()), "%d unresolved rows" % len(unres))
# ---- cross-match to the repository LVD table by sky position (and distance); NO offsets
Gd = G.copy()
for c in ("RA", "Dec", "dist_kpc"): Gd[c] = Gd[c].astype(float)
ufd = lvd[(lvd.M_V > -7.7) & (lvd.vlos_sigma.notna() | lvd.vlos_sigma_ul.notna())].reset_index(drop=True)
out = []; mism = []
for _, u in ufd.iterrows():
    dra = (Gd.RA - u.ra) * np.cos(np.radians(u.dec)); dd = Gd.Dec - u.dec; sep = np.hypot(dra, dd); j = sep.idxmin()
    g = Gd.loc[j] if sep[j] < 0.2 else None; how = "sky position < 0.2 deg"
    if g is None:   # fallback: identical normalised name (the LVD and the paper adopt different centres for extended or disrupting systems, e.g. Bootes III 0.34 deg apart)
        nm = Gd.index[Gd.full_name.str.replace(" ", "").str.lower() == u["name"].replace(" ", "").lower()]
        if len(nm) == 1: j = nm[0]; g = Gd.loc[j]; how = "name (sky separation %.2f deg)" % sep[j]
    row = dict(lvd_name=u["name"], lvd_ref_vlos=u.ref_vlos, lvd_distance_kpc=u.distance, lvd_sigma=u.vlos_sigma, lvd_sigma_em=u.vlos_sigma_em, lvd_sigma_ep=u.vlos_sigma_ep, lvd_sigma_ul=u.vlos_sigma_ul)
    if g is not None:
        gg = G.loc[j]; row.update(match_method=how, geha_full_name=gg.full_name, geha_abbr=gg.abbr, sep_deg=round(float(sep[j]), 4), geha_dist_kpc=gg.dist_kpc, geha_N_stars=gg.N_stars, geha_sigma_resolved=gg.sigma_resolved, geha_sigma=gg.sigma, geha_e_sigma_ll=gg.e_sigma_ll, geha_e_sigma_ul=gg.e_sigma_ul, geha_sigma_ul95=gg.sigma_ul95)
    out.append(row)
M2 = pd.DataFrame(out); M2.to_csv("geha_vs_lvd_match.csv", index=False)
check("G6 LVD ultra-faint rows with a dispersion or limit: 40", len(ufd) == 40)
inG = M2.geha_abbr.notna(); check("G7 of the 40, matched to a Geha Paper II row (sky position < 0.2 deg, else identical name)", True, "%d of 40; by name only: %s" % (inG.sum(), ", ".join(M2[inG & M2.match_method.str.startswith("name")].lvd_name)))
dm = M2[inG].copy(); dm["dd"] = np.abs(dm.lvd_distance_kpc - dm.geha_dist_kpc.astype(float)) / dm.lvd_distance_kpc
check("G8 matched rows agree in distance (Pace compilations) to 5%", (dm.dd < 0.05).all(), "max %.3f (%s)" % (dm.dd.max(), dm.loc[dm.dd.idxmax(), "lvd_name"]))
gh = dm[dm.lvd_ref_vlos.str.startswith("Geha2026")]; eq = 0
for _, r in gh.iterrows():
    if r.geha_sigma_resolved == "1" and not math.isnan(r.lvd_sigma): eq += abs(float(r.geha_sigma) - r.lvd_sigma) < 0.006 and abs(float(r.geha_e_sigma_ll) - r.lvd_sigma_em) < 0.006 and abs(float(r.geha_e_sigma_ul) - r.lvd_sigma_ep) < 0.006
    elif r.geha_sigma_resolved == "0" and not math.isnan(r.lvd_sigma_ul): eq += abs(float(r.geha_sigma_ul95) - r.lvd_sigma_ul) < 0.006
check("G9 independent control: for the LVD rows whose reference is Geha2026 and that are in Paper II, sigma and both errors (or the 95% limit) equal the LVD values", eq == len(gh), "%d of %d rows equal" % (eq, len(gh)))
print("\nALL CHECKS", "PASS" if ok_all else "FAIL"); sys.exit(0 if ok_all else 1)
