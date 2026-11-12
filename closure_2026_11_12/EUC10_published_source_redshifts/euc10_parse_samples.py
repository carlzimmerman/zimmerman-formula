#!/usr/bin/env python3
"""EUC10: parse the imaging-selected lens samples with spectroscopic source redshifts (criteria 21578af22b, sec. 7)
from the publications' own LaTeX tables, read locally.  Output: one row per system with lens and source redshift.

  AGEL      : AGEL DR2 (Barone+2025, arXiv 2503.08041) tables/redshifts_part{1,2}.tex; primary source = suffix 'A';
              secure = source flag >= 2 (the paper's own comparison cut); deflector flag >= 2 or a literature value (^).
  SLF4_MUSE : DESI Strong Lens Foundry IV (arXiv 2509.18078) table of lenses with sources; Q_z = 1 (robust) or 2
              (probable) for both; primary source = 'Source' or 'Source A'; lens = 'Lens' or 'Lens 1'.
  SLF2_DESI : DESI Strong Lens Foundry II (arXiv 2509.18089) master table, 'Confirmed systems' block; first z_s.
  HSC_DESI1 : HSC lenses with DESI (arXiv 2505.16158) Table 1 (grade A, secure lens and source).
  SLF3_KECK : DESI Strong Lens Foundry III (arXiv 2509.18086) zs-results.txt; primary (bold) z_s.
Samples with fewer than 20 systems are listed but not used by Part B (frozen N >= 20).

  python3 -I euc10_parse_samples.py --lit <lit dir> --out euc10_partB_samples.csv
"""
import argparse, csv, os, re

def num(s):
    m = re.search(r"-?\d+\.\d+|-?\d+", s or "")
    return float(m.group(0)) if m else None

def clean(s):
    return (s.replace("\\phantom{$-$}", "").replace("$-$", "-").replace("$+$", "+").replace("−", "-")
             .replace("~", " ").replace("\\,", " ").strip())

def agel(lit):
    out = []
    for part in ("redshifts_part1.tex", "redshifts_part2.tex"):
        p = os.path.join(lit, "x", "2503.08041", "tables", part)
        for ln, line in enumerate(open(p, encoding="utf-8"), 1):
            if not line.startswith("AGEL"): continue
            f = [c.strip() for c in line.split("&")]
            name = f[0]
            if not name.endswith("A"): continue
            zs, qs, zd, qd = num(f[1]), num(f[2]), num(f[4]), num(f[5])
            lit_d = "\\^" in f[4]
            if zs is None or qs is None or qs < 2: continue
            if zd is None or not (lit_d or (qd is not None and qd >= 2)): continue
            out.append(dict(sample="AGEL", name=name, ra=num(f[9]), dec=num(f[10].replace("\\\\", "")), z_l=zd, z_s=zs,
                            q_s=qs, theta_E="", prov="2503.08041 tables/%s line %d" % (part, ln)))
    return out

def slf4(lit):
    p = os.path.join(lit, "x", "2509.18078", "main.tex")
    out, cur = [], None
    lines = open(p, encoding="utf-8").read().splitlines()
    for ln, line in enumerate(lines, 1):
        if line.strip().startswith("%"): continue
        f = [clean(c) for c in line.split("&")]
        if len(f) < 9: continue
        if f[0].startswith("DESI"):
            cur = dict(name=f[0].replace(" ", ""), lens=None, src=None, ln=ln)
            out.append(cur)
        if cur is None: continue
        role = f[1]
        z = num(f[4].split("\\pm")[0]); q = num(f[5])
        if z is None or q is None: continue
        if role in ("Lens", "Lens 1") and cur["lens"] is None:
            cur["lens"] = (z, q, num(f[2]), num(f[3]))
        elif role in ("Source", "Source A") and cur["src"] is None:
            cur["src"] = (z, q, ln)
    res = []
    for c in out:
        if c["lens"] and c["src"] and c["lens"][1] <= 2 and c["src"][1] <= 2:
            res.append(dict(sample="SLF4_MUSE", name=c["name"], ra=c["lens"][2], dec=c["lens"][3], z_l=c["lens"][0],
                            z_s=c["src"][0], q_s=c["src"][1], theta_E="", prov="2509.18078 main.tex line %d" % c["src"][2]))
    return res

def slf2(lit):
    p = os.path.join(lit, "x", "2509.18089", "tables", "master_table.tex")
    out, inblock = [], False
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        if "Confirmed systems (20)" in line: inblock = True; continue
        if inblock and "textbf" in line and "Known system" in line: break
        if not inblock or line.strip().startswith("%"): continue
        f = [clean(c) for c in line.split("&")]
        if len(f) < 7 or not f[0].startswith("DESI"): continue
        m = re.search(r"J(\d+\.\d+)([+-]\d+\.\d+)", f[0].replace(" ", ""))
        zd, zs = num(f[3]), num(f[4])
        if m and zd and zs:
            out.append(dict(sample="SLF2_DESI", name=f[0].split("$")[0].replace(" ", ""), ra=float(m.group(1)),
                            dec=float(m.group(2)), z_l=zd, z_s=zs, q_s="", theta_E="",
                            prov="2509.18089 tables/master_table.tex line %d" % ln))
    return out

def hsc1(lit):
    p = os.path.join(lit, "x", "2505.16158", "Table", "longtable_1.tex")
    out = []
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        f = [clean(c) for c in line.split("&")]
        if len(f) < 7 or f[3] != "A": continue
        zl, zs = num(f[4].split("\\pm")[0]), num(f[5].split("\\pm")[0])
        if zl and zs:
            out.append(dict(sample="HSC_DESI1", name=f[0], ra=num(f[1]), dec=num(f[2]), z_l=zl, z_s=zs, q_s="",
                            theta_E="", prov="2505.16158 Table/longtable_1.tex line %d" % ln))
    return out

def slf3(lit):
    p = os.path.join(lit, "x", "2509.18086", "zs-results.txt")
    out = []
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        f = [clean(c) for c in line.split("&")]
        if len(f) < 3 or not f[0].startswith("DESI"): continue
        m = re.search(r"J(\d+\.\d+)([+-]\d+\.\d+)", f[0].replace(" ", ""))
        zl = num(f[1]) if f[1] != "-" else None
        b = re.search(r"\\textbf\{([\d.]+)", f[2])
        if m and zl and b:
            out.append(dict(sample="SLF3_KECK", name=f[0].replace(" ", ""), ra=float(m.group(1)), dec=float(m.group(2)),
                            z_l=zl, z_s=float(b.group(1)), q_s="", theta_E="", prov="2509.18086 zs-results.txt line %d" % ln))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--lit", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = agel(a.lit) + slf4(a.lit) + slf2(a.lit) + hsc1(a.lit) + slf3(a.lit)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sample", "name", "ra", "dec", "z_l", "z_s", "q_s", "theta_E", "prov"])
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    for k, v in sorted(Counter(r["sample"] for r in rows).items()):
        print("%-10s N = %3d %s" % (k, v, "" if v >= 20 else "(fewer than 20: not used by Part B)"))

if __name__ == "__main__":
    main()
