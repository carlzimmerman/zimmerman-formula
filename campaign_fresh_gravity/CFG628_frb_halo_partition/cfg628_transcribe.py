#!/usr/bin/env python3
"""CFG628 transcription (FROZEN_CRITERIA.md 'Data', C3).  Reads the arXiv LaTeX sources (data, never executed) and writes CSVs
into this lane folder.  Every row carries its source table.  Spot checks are printed.

Sources (outside the repo, under <repo parent>/_external_data/frb_tables/, or $CFG628_DATA):
  2402.00505/cobra_dr1.tex           Khrykin+24 FLIMFLAM DR1: Table 1 (tbl:tab_dr1), Table 3 (tbl:tab_dms), Table 5 (tbl:tab_results_priors)
  2409.16952/main.tex                Connor+25: the two FRB tables (DM_obs, DM_ex, z, DM_MW, survey)
  2408.02083/Tables/tab_frb.tex      Shannon+24 CRAFT/ICS: tab:frb_discoveries
Run: python3 -I cfg628_transcribe.py
"""
import csv
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("CFG628_DATA", HERE.parents[2] / "_external_data" / "frb_tables"))


def block(text, label):
    """the \\startdata ... \\enddata block of the deluxetable carrying \\label{label}."""
    i = text.index("\\label{%s}" % label)
    s = text.index("\\startdata", i)
    e = text.index("\\enddata", s)
    return text[s + len("\\startdata"):e]


def rows(blk):
    out = []
    for line in blk.split("\\\\"):
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        out.append([c.strip() for c in line.split("&")])
    return out


def num(s):
    s = s.replace("$", "").replace("{", "").replace("}", "").strip()
    return float(s)


def pm(s):
    m = re.match(r"\$?\s*([-\d.]+)\s*\\pm\s*([-\d.]+)\s*\$?", s.strip())
    return float(m.group(1)), float(m.group(2))


def asym(s):
    m = re.search(r"([-\d.]+)\^\{\+([\d.]+)\}_\{-([\d.]+)\}", s)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def main():
    tex = (DATA / "2402.00505" / "cobra_dr1.tex").read_text()
    # ---- Khrykin+24 Table 1 + Table 3
    t1 = {r[0]: r for r in rows(block(tex, "tbl:tab_dr1"))}
    t3 = rows(block(tex, "tbl:tab_dms"))
    ff = []
    for r in t3:
        frb = r[0]
        a = t1[frb]
        dmi, sdmi = pm(r[2]); dmh, sdmh = pm(r[3]); dhh, sdhh = pm(r[4])
        ff.append(dict(frb=frb, ra_deg=num(a[1]), dec_deg=num(a[2]), z_t1=num(a[3]), dm_frb_t1=num(a[6]),
                       z=num(r[1]), dm_argo=dmi, s_argo=sdmi, dm_halos=dmh, s_halos=sdmh, dm_hosthalo=dhh, s_hosthalo=sdhh,
                       logM_hosthalo=num(r[5]), dm_mw=num(r[6]), dm_frb=num(r[7]),
                       source="Khrykin+24 (arXiv:2402.00505) Table 1 tbl:tab_dr1 + Table 3 tbl:tab_dms"))
    with open(HERE / "flimflam_dr1_sightlines.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ff[0].keys())); w.writeheader(); w.writerows(ff)
    # ---- Khrykin+24 Table 5 (published posteriors)
    t5 = rows(block(tex, "tbl:tab_results_priors"))
    cols = ["flat_fd_fiducial", "flat_fd_limited_fgas", "gauss_fd", "gauss_fd_limited_fgas"]
    names = ["f_igm", "f_gas", "DM_host_unk", "DM_host_mean"]
    res = []
    for nm, r in zip(names, t5):
        for c, cell in zip(cols, r[1:]):
            v, up, lo = asym(cell)
            res.append(dict(param=nm, prior=c, median=v, plus=up, minus=lo,
                            source="Khrykin+24 Table 5 tbl:tab_results_priors"))
    with open(HERE / "flimflam_dr1_published_posteriors.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
    # ---- Connor+25 FRB tables
    ctex = (DATA / "2409.16952" / "main.tex").read_text()
    con = []
    for k, m in enumerate(re.finditer(r"\\midrule(.*?)\\bottomrule", ctex, re.S)):
        for line in m.group(1).split("\\\\"):
            line = line.strip()
            if not line or line.startswith("%"):
                continue
            c = [x.strip() for x in line.split("&")]
            if len(c) != 6:
                continue
            zs = c[3]
            phot = "dagger" in zs
            con.append(dict(frb=c[0].replace("FRB", "").strip(), dm_obs=num(c[1]), dm_ex=num(c[2]),
                            z=float(re.sub(r"\$.*", "", zs)), z_photometric=int(phot), dm_mw=num(c[4]), survey=c[5],
                            source="Connor+25 (arXiv:2409.16952) table %d" % (k + 1)))
    with open(HERE / "connor25_frbs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(con[0].keys())); w.writeheader(); w.writerows(con)
    # ---- CRAFT/ICS tab_frb
    ttex = (DATA / "2408.02083" / "Tables" / "tab_frb.tex").read_text()
    craft = []
    for line in ttex.split("\\\\"):
        line = line.replace("\\hline", "").strip()
        if not re.match(r"\d{8}[A-Z]", line):
            continue
        c = [x.strip() for x in line.split("&")]
        if len(c) < 10:
            continue
        dm = float(re.sub(r"\(.*?\)", "", c[4]))
        try:
            z = float(c[6]); zflag = ""
        except ValueError:
            z = float("nan"); zflag = c[6]
        craft.append(dict(frb=c[0], nu_c_MHz=float(c[2]), dm=dm, dm_mw_ne2001=float(c[5]), z=z, z_flag=zflag,
                          source="Shannon+24 (arXiv:2408.02083) tab:frb_discoveries"))
    with open(HERE / "craft_ics_frbs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(craft[0].keys())); w.writeheader(); w.writerows(craft)

    # ---- C3 spot checks
    print("CFG628 transcription: FLIMFLAM %d sightlines, %d posterior cells, Connor %d FRBs, CRAFT %d FRBs"
          % (len(ff), len(res), len(con), len(craft)))
    cmap = {r["frb"]: r for r in con}
    kmap = {r["frb"]: r for r in craft}
    # naming differences (not corrected in the CSVs): Khrykin+24 Tables 1/3 write 20190608A and 20211127A; CRAFT, Connor+25 and the
    # FLIMFLAM data paper write 20190608B and 20211127I.  Connor+25 writes 20180924A for the ASKAP burst others call 20180924B.
    alias = {"20190608A": "20190608B", "20211127A": "20211127I"}
    calias = {"20180924B": "20180924A"}
    nflag = 0
    print("C3 cross-source DM / z (flag |dDM| > 1, |dz| > 0.001):")
    for r in ff:
        key = alias.get(r["frb"], r["frb"])
        line = ["%s T1 DM %.2f z %.4f | T3 DM %.2f z %.4f" % (r["frb"], r["dm_frb_t1"], r["z_t1"], r["dm_frb"], r["z"])]
        flags = []
        if abs(r["dm_frb_t1"] - r["dm_frb"]) > 1 or abs(r["z_t1"] - r["z"]) > 0.001: flags.append("T1-vs-T3")
        if key in kmap:
            k = kmap[key]; line.append("CRAFT DM %.2f z %.4f" % (k["dm"], k["z"]))
            if abs(k["dm"] - r["dm_frb"]) > 1: flags.append("CRAFT-DM")
            if abs(k["z"] - r["z"]) > 0.001: flags.append("CRAFT-z")
        else:
            line.append("CRAFT: absent"); flags.append("CRAFT-absent")
        ckey = calias.get(key, key)
        if ckey in cmap:
            c = cmap[ckey]; line.append("Connor DM %.2f z %.4f" % (c["dm_obs"], c["z"]))
            if abs(c["dm_obs"] - r["dm_frb"]) > 1: flags.append("Connor-DM")
            if abs(c["z"] - r["z"]) > 0.001: flags.append("Connor-z")
        else:
            line.append("Connor: absent"); flags.append("Connor-absent")
        nflag += len(flags)
        print("  " + " | ".join(line) + ("   FLAGS: " + ",".join(flags) if flags else ""))
    # Connor internal consistency: DM_ex = DM_obs - DM_MW
    bad = [r["frb"] for r in con if abs(r["dm_obs"] - r["dm_mw"] - r["dm_ex"]) > 0.15]
    print("C3 Connor DM_ex == DM_obs - DM_MW (|d| <= 0.15): %d of %d rows off: %s" % (len(bad), len(con), bad))
    # hand spot checks against the LaTeX strings
    spots = [("20191001A", "dm_halos", 360.7, "s_halos", 72.4), ("20200430A", "dm_argo", 116.1, "s_argo", 5.6),
             ("20200906A", "dm_hosthalo", 45.8, "s_hosthalo", 10.8)]
    fmap = {r["frb"]: r for r in ff}
    ok = all(abs(fmap[f_][a] - va) < 1e-9 and abs(fmap[f_][b] - vb) < 1e-9 for f_, a, va, b, vb in spots)
    print("C3 hand spot-check (3 Table 3 cells read by eye from cobra_dr1.tex):", "PASS" if ok else "FAIL")
    print("C3 flags total:", nflag)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
