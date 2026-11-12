#!/usr/bin/env python3
"""EUC10 routes R2/R3, step 1: find every position written in the fetched literature (LaTeX sources, locally
extracted PDF text, VizieR tsv) and cross-match it to the ECLIPSE positions (criteria 21578af22b section 4).

Positions recognised per line:
  D  decimal pair in a name (DESI-ddd.dddd+dd.dddd, "DESI J..."), or two adjacent decimal columns (>= 3 decimals);
  S  sexagesimal name hhmmss[.s]+ddmmss[.s] (J, AGEL, PS1J, HSCJ, ... prefixes) and hh:mm:ss / dd:mm:ss columns;
  C  coarse name hhmm[.m]+ddmm (precision > 2 arcsec: PROVISIONAL, unique-in-box rule).
Hits within 5 arcsec (D, S) or inside the precision box (C) are written with file, line number and the line text.
The same scan is repeated with every ECLIPSE position moved +0.3 deg in declination (the frozen null).

  python3 -I euc10_scan_lit.py --lit <dir> --cat <ECLIPSE_object_catalogue.csv> --out <hits.csv>
"""
import argparse, csv, glob, math, os, re, sys
import numpy as np

R_FINE = 5.0
SHIFT = 0.3
DEC_PAIR = re.compile(r"(?<![\d.])(\d{1,3}\.\d{3,})\s*(?:&|\s|,|\|)\s*\$?([+\-−]?\s?\d{1,2}\.\d{3,})")
DESI = re.compile(r"DESI[\s~\-_]*J?(\d{1,3}\.\d{3,})\s*([+\-−]\d{1,2}\.\d{3,})")
SEXN = re.compile(r"(?<![\d.])(\d{2})(\d{2})(\d{2}(?:\.\d+)?)\s*([+\-−]|\$[+\-−]\$|\$\-\$)\s*(\d{2})(\d{2})(\d{2}(?:\.\d+)?)(?![\d])")
COARSE = re.compile(r"J(\d{2})(\d{2})(?:\.(\d))?\s*([+\-−]|\$[+\-−]\$)\s*(\d{2})(\d{2})(?![\d.])")
SEXC = re.compile(r"(\d{1,2})[:h ](\d{2})[:m ](\d{2}(?:\.\d+)?)s?\s*(?:&|\s)\s*\$?([+\-−])\$?\s?(\d{1,2})[:d° ](\d{2})[:m' ](\d{2}(?:\.\d+)?)")

def sgn(s): return -1.0 if ("-" in s or "−" in s) else 1.0

def positions(line):
    out = []
    # LaTeX / PDF sign forms: \phantom{$-$}, $-$, $+$, Unicode minus, double hyphen in names
    line = (line.replace("\\phantom{$-$}", "").replace("$-$", "-").replace("$+$", "+").replace("−", "-")
                .replace("--", "-").replace("\\,", "").replace("$", " "))
    for m in DESI.finditer(line):
        out.append(("D", float(m.group(1)), float(m.group(2).replace("−", "-")), 0.0))
    for m in SEXN.finditer(line):
        h, mi, s, sg, d, dm, ds = m.groups()
        if int(h) > 23 or int(mi) > 59 or int(dm) > 59 or float(s) >= 60 or float(ds) >= 60: continue
        ra = 15.0 * (int(h) + int(mi) / 60.0 + float(s) / 3600.0)
        de = sgn(sg) * (int(d) + int(dm) / 60.0 + float(ds) / 3600.0)
        # names are truncated: precision 1 time-second in RA (15") is never used; seconds digits give <= 1.5"/1" truncation
        prec = 0.0 if "." in s else 15.0 * math.cos(math.radians(de))
        out.append(("S", ra, de, prec))
    for m in SEXC.finditer(line):
        h, mi, s, sg, d, dm, ds = m.groups()
        if int(h) > 23 or int(mi) > 59 or int(dm) > 59: continue
        out.append(("S", 15.0 * (int(h) + int(mi) / 60.0 + float(s) / 3600.0),
                    sgn(sg) * (int(d) + int(dm) / 60.0 + float(ds) / 3600.0), 0.0))
    for m in COARSE.finditer(line):
        h, mi, tenth, sg, d, dm = m.groups()
        if int(h) > 23 or int(mi) > 59 or int(dm) > 59: continue
        ra = 15.0 * (int(h) + (int(mi) + (int(tenth) / 10.0 if tenth else 0.0)) / 60.0)
        de = sgn(sg) * (int(d) + int(dm) / 60.0)
        out.append(("C", ra, de, 60.0))
    for m in DEC_PAIR.finditer(line):
        ra, de = float(m.group(1)), float(m.group(2).replace("−", "-").replace(" ", ""))
        if 0.0 <= ra < 360.0 and -90.0 <= de <= 90.0:
            out.append(("D", ra, de, 0.0))
    return out

def unitvec(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)], -1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lit", required=True); ap.add_argument("--cat", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cat = list(csv.DictReader(open(a.cat, newline="", encoding="utf-8")))
    ids = [r["Unique_Identifier"] for r in cat]; grade = [r["Expert_Grade"] for r in cat]
    ra0 = np.array([float(r["RA_obj"]) for r in cat]); de0 = np.array([float(r["DEC_obj"]) for r in cat])
    files = sorted(set(glob.glob(os.path.join(a.lit, "x", "**", "*.tex"), recursive=True)
                       + glob.glob(os.path.join(a.lit, "x", "**", "*.txt"), recursive=True)
                       + glob.glob(os.path.join(a.lit, "*.txt")) + glob.glob(os.path.join(a.lit, "*.tsv"))))
    files = [f for f in files if os.path.basename(f) != "MANIFEST.txt"]
    rows = []
    for shift in (0.0, SHIFT):
        V = unitvec(ra0, np.clip(de0 + shift, -90, 90))
        n_pos = 0
        for f in files:
            rel = os.path.relpath(f, a.lit)
            for ln, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
                for kind, ra, de, prec in positions(line):
                    n_pos += 1
                    v = unitvec(ra, de)
                    sep = np.degrees(np.arccos(np.clip((V * v).sum(1), -1, 1))) * 3600.0
                    lim = R_FINE if prec == 0.0 else R_FINE + prec * 1.5
                    for j in np.where(sep <= lim)[0]:
                        rows.append(dict(shift=shift, file=rel, line=ln, kind=kind if prec == 0.0 else kind + "c",
                                         ra=round(ra, 6), dec=round(de, 6), sep_arcsec=round(float(sep[j]), 2),
                                         eclipse_id=ids[j], grade=grade[j], text=line.strip()[:400]))
        print("shift %.1f: %d positions read in %d files; %d hits" % (shift, n_pos, len(files), sum(1 for r in rows if r["shift"] == shift)))
    with open(a.out, "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0].keys()) if rows else ["shift"]); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    main()
