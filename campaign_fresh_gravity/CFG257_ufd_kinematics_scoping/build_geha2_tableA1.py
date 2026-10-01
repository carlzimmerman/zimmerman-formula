#!/usr/bin/env python3
"""Transcribe Table A1 of Geha 2026, 'The Keck/DEIMOS Stellar Archive: II. Dynamical Masses and Metallicities for a Uniform Sample of Milky Way Satellites' (arXiv:2602.10202)
from the pdftotext output of the PDF.  usage: python3 build_geha2_tableA1.py <pdftotext -layout output>  -> geha2026_paperII_tableA1.csv
Columns follow the paper: (1) full name, (2) abbreviated name, (3)-(7) RA, Dec, distance, M_V, r_1/2 (arcmin) from Pace (2025), (8) type (G galaxy, GC globular cluster, U unknown),
(9) N_stars, (10)-(11) v_sys and error, (12)-(15) velocity dispersion sigma_sys and errors (lower, upper, 95th-percentile upper limit), (16)-(21) [Fe/H] columns.
-999 in the paper means 'not applicable': for the dispersion, eps_ll = eps_ul = -999 and sigma = -999 mean UNRESOLVED, with the 95% upper limit in eps_sigma95 (column 15, printed as the value in the sigma95 slot);
that convention is kept verbatim in the *_raw columns, and `sigma_resolved` / `sigma_ul95` are added."""
import re, sys, csv
txt = open(sys.argv[1], encoding="utf-8").read().splitlines()
i0 = next(i for i, l in enumerate(txt) if "Table A1. Derived Properties of Milky Way Satellites" in l); i1 = next(i for i, l in enumerate(txt) if i > i0 and l.strip().startswith("Note—Literature"))
num = re.compile(r"^-?\d+(\.\d+)?$")
rows = []
for l in txt[i0:i1]:
    t = l.split()
    while t and not num.match(t[-1]) and t[-1] not in ("G", "GC", "U"): t = t[:-1]     # stray margin words ('DEIMOS', 'Geha') after the last column
    if len(t) < 21 or not all(num.match(x) for x in t[-13:]) or t[-14] not in ("G", "GC", "U"): continue
    vals = t[-13:]; typ = t[-14]; r12, mv, dist, dec, ra = t[-15], t[-16], t[-17], t[-18], t[-19]
    if not all(num.match(x) for x in (r12, mv, dist, dec, ra)): continue
    abbr = t[-20]; full = " ".join(t[:-20])
    rows.append(dict(full_name=full, abbr=abbr, RA=ra, Dec=dec, dist_kpc=dist, M_V=mv, r12_arcmin=r12, type=typ, N_stars=vals[0], vsys=vals[1], e_vsys=vals[2], sigma_raw=vals[3], e_sigma_ll_raw=vals[4], e_sigma_ul_raw=vals[5], sigma95_raw=vals[6],
                     FeH=vals[7], e_FeH=vals[8], sigFeH=vals[9], e_sigFeH_ll=vals[10], e_sigFeH_ul=vals[11], sigFeH95=vals[12], source_line=" ".join(l.split())))
for r in rows:
    res = float(r["sigma_raw"]) != -999
    r["sigma_resolved"] = int(res); r["sigma_ul95"] = r["sigma95_raw"] if (not res and float(r["sigma95_raw"]) != -999) else ""
    r["sigma"] = r["sigma_raw"] if res else ""; r["e_sigma_ll"] = r["e_sigma_ll_raw"] if res else ""; r["e_sigma_ul"] = r["e_sigma_ul_raw"] if res else ""
fields = ["full_name", "abbr", "RA", "Dec", "dist_kpc", "M_V", "r12_arcmin", "type", "N_stars", "vsys", "e_vsys", "sigma_resolved", "sigma", "e_sigma_ll", "e_sigma_ul", "sigma_ul95", "sigma_raw", "e_sigma_ll_raw", "e_sigma_ul_raw", "sigma95_raw", "FeH", "e_FeH", "sigFeH", "e_sigFeH_ll", "e_sigFeH_ul", "sigFeH95", "source_line"]
with open("geha2026_paperII_tableA1.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print(len(rows), "rows written")
