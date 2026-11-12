#!/usr/bin/env python3
"""EUC10: build the matched list of published lensed-source redshifts (criteria 21578af22b, sections 3 and 4).

Route R1 (NED): every NED object within 10" of an ECLIPSE position, typed G_Lens or Q_Lens, with a spectroscopic
redshift (zflag starting 'S') more than 0.05 above the lens reference redshift.  Untyped spectroscopic objects more than
0.1 above the lens reference are written as POINTERS only (not counted).
Routes R2/R3 (VizieR, literature): the hits of euc10_scan_lit.py were read by eye; every system that carries a source
redshift is entered below with file and line, and this script checks that the quoted value is on that line.
The shifted-position null is counted the same way (NED: second cone set; literature: the scan's shifted hits).

  python3 -I euc10_build_matches.py --data-dir <ECLIPSE dir> --ned-dir <dir with ned_cones_*.csv> --lit <lit dir>
Writes euc10_matches.csv, euc10_ned_rows.csv, euc10_ned_pointers.csv, euc10_null.json in this folder.
"""
import argparse, csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

R_NED = 10.0
SHIFT = 0.3

# ---- literature entries read from the scan hits (file relative to the lit dir, 1-based line, value text on that line)
# fields: eclipse_id, z_s, quality as published, z_l as published, source, file, line, text that must appear, table?, note
LIT = [
    ("EUCL-DR1-L000613", 2.478, "flag 3 (high)", 0.722, "AGEL DR2, Barone+2025 Table 3", "x/2503.08041/tables/redshifts_part1.tex", 53, "AGEL025052-552412A & 2.478 & 3.0", True, ""),
    ("EUCL-DR1-L000613", 2.478, "", 0.718, "AGEL environments (arXiv 2602.11068) table", "x/2602.11068/paper.txt", 973, "2.478", True, "second place"),
    ("EUCL-DR1-L004966", 0.920, "flag 2", 0.343, "AGEL DR2, Barone+2025 Table 3", "x/2503.08041/tables/redshifts_part1.tex", 64, "AGEL043806-322852A & 0.920 & 2.0", True, ""),
    ("EUCL-DR1-L004966", 0.92, "", 0.34, "AGEL environments (arXiv 2602.11068) table", "x/2602.11068/paper.txt", 1025, "0.92", True, "second place"),
    ("EUCL-DR1-L008070", 2.035, "flag 2", None, "AGEL DR2, Barone+2025 Table 3", "x/2503.08041/tables/redshifts_part1.tex", 58, "AGEL034131-513045A & 2.035 & 2.0", True, ""),
    ("EUCL-DR1-L016382", 2.344, "flag 2", 0.354, "AGEL DR2, Barone+2025 Table 3", "x/2503.08041/tables/redshifts_part1.tex", 65, "AGEL053724-464702A & 2.344 & 2.0", True, ""),
    ("EUCL-DR1-L016382", 2.344, "", 0.352, "AGEL environments (arXiv 2602.11068) table", "x/2602.11068/paper.txt", 968, "2.344", True, "second place"),
    ("EUCL-DR1-L001750", 1.43211, "Q_z 1 (Source A)", 0.4883, "DESI SLF IV (arXiv 2509.18078) Table of sources", "x/2509.18078/main.tex", 622, "1.43211", True, "seven-source group lens; first-listed source A"),
    ("EUCL-DR1-L001750", 0.962, "", 0.488, "AGEL environments (arXiv 2602.11068) table", "x/2602.11068/paper.txt", 1095, "0.962a", True, "a different source of the same system (paper: several sources)"),
    ("EUCL-DR1-L008608", 0.84611, "Q_z 1 (Source A)", 0.3011, "DESI SLF IV (arXiv 2509.18078) Table of sources", "x/2509.18078/main.tex", 614, "0.84611", True, "lens position 4.67\" from ECLIPSE"),
    ("EUCL-DR1-L013325", 1.44884, "Q_z 1", 0.44137, "DESI SLF IV (arXiv 2509.18078) Table of sources", "x/2509.18078/main.tex", 596, "1.44884", True, "single strong [O II] line"),
    ("EUCL-DR1-L015871", 1.17482, "Q_z 1", 0.62107, "DESI SLF IV (arXiv 2509.18078) Table of sources", "x/2509.18078/main.tex", 575, "1.17482", True, ""),
    ("EUCL-DR1-L014483", 0.620, "text: 'clearly resolved narrow emission lines'", None, "Lemon+2022 (Gaia IV, arXiv 2206.07714) sec. lensed galaxies, J0500-5534", "x/2206.07714/main.tex", 838, "0.620", False, "text, not a table"),
    ("EUCL-DR1-L015763", 1.366, "NISP, with DESI support", 0.235, "Bergamini+ (Euclid DR1) Table 1, PS1J1821+7130", "euclid_dr1_bergamini.txt", 268, "1.366", True, "EUC2 DESI fibre redshift 1.3657 is the second place"),
    ("EUCL-DR1-L017819", 1.21, "compiled (ref O08)", 0.320, "SuGOHI II (Wong+2018) VizieR J/ApJ/867/107/added, SDSSJ1524+4409", "vizier_J_ApJ_867_107_added.tsv", 106, "1.2100", True, "lensed quasar"),
]
# scan hits read and NOT entered (no source redshift on the matched row), for the record:
LIT_NO_ZS = ["L000188 AGEL184141+741405 (imaging list only)", "L000938 AGEL040823-532714 (deflector only)",
             "L000942 AGEL103255+751854 (imaging list only)", "L001663 AGEL032216-523440 (imaging list only)",
             "L001804 AGEL025029-410418 (imaging list only)", "L011324 AGEL035606-560729 (imaging list only)",
             "L012872 AGEL025220-473238 (deflector only)", "L013536 AGEL042816-321800 (imaging list only)",
             "L014638 AGEL041810-545735 (imaging list only)", "L023468 AGEL042225-403156 (imaging list only)",
             "L023359 DESI-064.8539-25.2245 (lens-only table)", "HSC/Shu+2022 and SuGOHI rows L001851 L003257 L010972 "
             "L012015 L013347 L013627 L014691 L015124 L024303 L026571 (lens redshift only, or the decimal position "
             "is > 5\" away)"]

def unit(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], -1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--ned-dir", required=True); ap.add_argument("--lit", required=True)
    a = ap.parse_args()
    cat = list(csv.DictReader(open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8")))
    rows, _ = E.load(a.data_dir)
    key = {r["id"]: r for r in rows}
    ids = [r["Unique_Identifier"] for r in cat]
    ra0 = np.array([float(r["RA_obj"]) for r in cat]); de0 = np.array([float(r["DEC_obj"]) for r in cat])
    def zref(i):
        r = key.get(i)
        o = cat[ids.index(i)]
        if o["desi_deflector_specz"].strip(): return float(o["desi_deflector_specz"]), "DESI"
        if r is not None and r["z"] > 0: return r["z"], "photo-z"
        return None, "none"

    # ------------------------------------------------ NED
    ned_acc, ned_ptr, nulls = {}, [], {}
    for shift in (0.0, SHIFT):
        V = unit(ra0, np.clip(de0 + shift, -90, 90))
        p = os.path.join(a.ned_dir, "ned_cones_shift%.1f.csv" % shift)
        src_rows = [dict(r, svc="NED") for r in csv.DictReader(open(p, newline="", encoding="utf-8"))]
        # R1b SIMBAD (CfA mirror): the whole list of lensed-type objects with a redshift, matched here at the same
        # positions and radius.  Lensed-image types LeG/LeI/LeQ count; quality E (uncertain) does not;
        # gLe/gLS (the lens / the system) are pointers only.
        sp = os.path.join(a.ned_dir, "simbad_lens_types_with_z.csv")
        for r in csv.DictReader(open(sp, newline="", encoding="utf-8")):
            if not (r["ra"] and r["dec"] and r["rvz_redshift"]): continue
            ok = r["rvz_qual"] in ("A", "B", "C", "D")
            src_rows.append(dict(svc="SIMBAD", prefname=r["main_id"], ra=r["ra"], dec=r["dec"], z=r["rvz_redshift"],
                                 zflag=("S" if ok else "X") + "-qual" + r["rvz_qual"], z_bibcode=r["rvz_bibcode"],
                                 prefphytype={"LeG": "G_Lens", "LeI": "G_Lens", "LeQ": "Q_Lens"}.get(r["otype"], r["otype"])))
        acc, nrow = [], 0
        for r in src_rows:
            nrow += 1
            if not r["z"] or not r["zflag"].startswith("S"): continue
            v = unit(float(r["ra"]), float(r["dec"]))
            sep = np.degrees(np.arccos(np.clip((V * v).sum(1), -1, 1))) * 3600.0
            j = int(np.argmin(sep))
            if sep[j] > R_NED: continue
            i = ids[j]; z = float(r["z"]); zl, zlsrc = zref(i)
            typed = r["prefphytype"] in ("G_Lens", "Q_Lens")
            rec = dict(shift=shift, svc=r["svc"], eclipse_id=i, grade=cat[j]["Expert_Grade"], prefname=r["prefname"], type=r["prefphytype"],
                       z=z, zflag=r["zflag"], z_bibcode=r["z_bibcode"], sep_arcsec=round(float(sep[j]), 2),
                       z_lens_ref=zl if zl is not None else "", z_lens_ref_from=zlsrc)
            if typed and (zl is None or z > zl + 0.05):
                acc.append(rec)
            elif (not typed) and zl is not None and z > zl + 0.1:
                rec["role"] = "POINTER"; ned_ptr.append(rec)
        nulls[shift] = acc
        print("NED+SIMBAD shift %.1f: %d rows read; %d lens-typed spectroscopic objects above the lens, on %d lenses; pointers %d"
              % (shift, nrow, len(acc), len(set(x["eclipse_id"] for x in acc)), sum(1 for x in ned_ptr if x["shift"] == shift)))
    for x in nulls[0.0]:
        ned_acc.setdefault(x["eclipse_id"], []).append(x)
    with open(os.path.join(HERE, "euc10_ned_rows.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(nulls[0.0][0].keys()) if nulls[0.0] else ["shift"]); w.writeheader()
        for s in (0.0, SHIFT): w.writerows(nulls[s])
    with open(os.path.join(HERE, "euc10_ned_pointers.csv"), "w", newline="") as f:
        if ned_ptr:
            w = csv.DictWriter(f, fieldnames=list(ned_ptr[0].keys())); w.writeheader(); w.writerows(ned_ptr)

    # ------------------------------------------------ literature (verify every quoted line)
    lit_by = {}
    for (i, zs, q, zl, src, fil, ln, txt, table, note) in LIT:
        line = open(os.path.join(a.lit, fil), encoding="utf-8", errors="replace").read().split("\n")[ln - 1]
        if txt not in line:
            sys.exit("literature entry %s: '%s' not found on %s line %d" % (i, txt, fil, ln))
        lit_by.setdefault(i, []).append(dict(z_s=zs, quality=q, z_l_pub=zl, source=src, where="%s:%d" % (fil, ln), table=table, note=note))
    hits = list(csv.DictReader(open(os.path.join(HERE, "euc10_lit_hits.csv"), newline="")))
    lit_null_ids = sorted(set(h["eclipse_id"] for h in hits if h["shift"] == "0.3"))

    # ------------------------------------------------ merge per lens
    out = []
    for i in sorted(set(lit_by) | set(ned_acc)):
        L = lit_by.get(i, []); N = ned_acc.get(i, [])
        prim = [x for x in L if x["note"] != "second place" and "a different source" not in x["note"]]
        cand = []
        for x in L:
            cand.append(("LIT", x["z_s"], x))
        nz = sorted(set(round(x["z"], 4) for x in N))
        if prim:
            zs = prim[0]["z_s"]; src = prim[0]["source"]; where = prim[0]["where"]; q = prim[0]["quality"]; table = prim[0]["table"]
        else:
            zs = min(nz); src = "; ".join(sorted(set("%s %s" % (x["svc"], x["z_bibcode"]) for x in N if round(x["z"], 4) == zs)))
            where = ", ".join("%s: %s" % (x["svc"], x["prefname"]) for x in N if round(x["z"], 4) == zs); q = ", ".join(sorted(set(x["zflag"] for x in N))); table = True
        allv = [x["z_s"] for x in L] + nz
        conflict = (max(allv) - min(allv)) > 0.02
        agree = set(("LIT", x["source"]) for x in L if abs(x["z_s"] - zs) <= 0.02) | set((x["svc"], x["z_bibcode"]) for x in N if abs(x["z"] - zs) <= 0.02)
        two = len(agree) >= 2 or i == "EUCL-DR1-L015763"   # L015763: EUC2's DESI fibre redshift 1.3657 is the second place
        prov = "N" if (table or two) else "Y"
        status = "EXCLUDED: values differ by more than 0.02 (%s)" % ", ".join("%.4g" % v for v in sorted(set(allv))) if conflict else "USED"
        zl_ref, zl_from = zref(i)
        if zl_ref is not None and zs <= zl_ref + 0.05:
            status = "EXCLUDED: not above the lens"
        r = key.get(i)
        out.append(dict(eclipse_id=i, grade=cat[ids.index(i)]["Expert_Grade"], z_s=zs, quality=q, source=src, where=where,
                        all_values=";".join("%.5g" % v for v in allv), second_place="Y" if two else "N", provisional=prov,
                        status=status, in_key=int(r is not None), z_l_photo="%.3f" % r["z"] if r and r["z"] > 0 else "",
                        z_l_desi=cat[ids.index(i)]["desi_deflector_specz"],
                        large_system=cat[ids.index(i)]["large_system_warning"],
                        ned_names=";".join(sorted(set("%s:%s %.4f %s" % (x["svc"], x["prefname"], x["z"], x["z_bibcode"]) for x in N))),
                        lit_where=";".join(x["where"] for x in L), note=";".join(x["note"] for x in L if x["note"])))
    with open(os.path.join(HERE, "euc10_matches.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    real = sum(1 for o in out if o["status"] == "USED")
    null = dict(real_accepted=real, shifted_ned=len(set(x["eclipse_id"] for x in nulls[SHIFT])),
                shifted_lit=0, shifted_lit_scan_hits_coarse=lit_null_ids,
                note="literature shifted hits are coarse-name matches whose rows carry a decimal position > 5\" away; none carries a source redshift")
    null["shifted_accepted"] = null["shifted_ned"] + null["shifted_lit"]
    json.dump(null, open(os.path.join(HERE, "euc10_null.json"), "w"), indent=1)
    print("matched lenses: %d rows, %d USED; null (shifted): %d" % (len(out), real, null["shifted_accepted"]))
    for o in out:
        print("  %s %s z_s %.4f %-9s prov %s 2nd %s large %s | %s | %s" % (o["eclipse_id"], o["grade"], o["z_s"], o["status"][:9], o["provisional"],
              o["second_place"], o["large_system"], o["source"][:60], o["all_values"]))
    print("literature hits without a source redshift:", "; ".join(LIT_NO_ZS))

if __name__ == "__main__":
    main()
