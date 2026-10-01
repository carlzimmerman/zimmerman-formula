#!/usr/bin/env python3
"""Transcribe Table A.1 of Arroyo-Polonio, Battaglia & Thomas 2026 (arXiv:2603.03129, A&A 708, A287) from the pdftotext output of the PDF.
usage: python3 build_arroyo_tableA1.py <pdftotext -layout output of the PDF>   -> arroyo_polonio2026_tableA1.csv
Each posterior is quoted by the paper as median +1sigma(+3sigma) / -1sigma(-3sigma); the 3-sigma values exist only for the corrected quantities."""
import re, sys, csv
txt = open(sys.argv[1], encoding="utf-8").read().splitlines()
i0 = next(i for i, l in enumerate(txt) if "Table A.1. Observed l.o.s." in l); i1 = next(i for i, l in enumerate(txt) if i > i0 and l.strip().startswith("Notes. Observed"))
names = ["Boo I", "Car II", "Cra II", "Eri III", "Hyd I", "Leo IV", "Leo V", "Ret II", "Sag II", "Seg 1", "Uni 1", "Wil 1"]
LVD = {"Boo I": "Bootes I", "Car II": "Carina II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V", "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}   # the 8 systems in the CFG28/29 sample; Cra II, Eri III, Sag II, Uni 1 are not in the LVD ultra-faint list
REFS = {1: "Koposov+2011", 2: "Li+2018", 3: "Caldwell+2017", 4: "Simon+2024", 5: "Koposov+2018", 6: "Jenkins+2021", 7: "Koposov+2015b", 8: "Longeard+2021", 9: "Simon+2011", 10: "Smith+2024", 11: "Willman+2011"}
block = {}; cur = None
for l in txt[i0:i1]:
    m = re.match(r"\s*(%s)\s+(\d+)\s" % "|".join(re.escape(n) for n in names), l)
    if m: cur = m.group(1); block[cur] = [l.strip()]; continue
    if cur and l.strip(): block[cur].append(l.strip())
M = "−"
tok = re.compile(r"(\d+\.\d+)\+(\d+\.\d+)(?:\(\+(\d+\.\d+)\))?\s*[%s-](\d+\.\d+)(?:\([%s-](\d+\.\d+)\))?" % (M, M))
rows = []
cols = ["a12_arcmin", "sig_lit", "sig_f0", "logM_f0", "sig_free", "logM_free", "sig_f07", "logM_f07", "logJ"]
for n in names:
    s = " ".join(block[n]); s = re.sub(r"\[[ab]\]", " [FN] ", s); m0 = re.match(r"%s\s+(\d+)\s" % re.escape(n), s); nst = int(m0.group(1)); body = s[m0.end():]
    toks = list(tok.finditer(body)); assert len(toks) == 9, (n, len(toks), body)
    r = dict(galaxy=n, lvd_name=LVD.get(n, ""), in_cfg28_29_sample=int(n in LVD), N_stars=nst)
    for c, t in zip(cols, toks):
        med, up1, up3, lo1, lo3 = t.groups()
        r.update({c: med, c + "_up1": up1, c + "_up3": up3 or "", c + "_lo1": lo1, c + "_lo3": lo3 or ""})
    tail = body[toks[-1].end():].split(); r["stars_type"] = next(x for x in body.split() if x in ("RGB", "MS")); refn = [int(x) for x in tail if x.isdigit()]; r["ref_number"] = refn[-1]; r["ref"] = REFS[refn[-1]]
    r["footnote_marker"] = "[a]" if "[a]" in " ".join(block[n]) else ("[b]" if "[b]" in " ".join(block[n]) else "")
    rows.append(r)
fields = ["galaxy", "lvd_name", "in_cfg28_29_sample", "N_stars", "stars_type", "ref_number", "ref", "footnote_marker"] + [k for c in cols for k in (c, c + "_up1", c + "_up3", c + "_lo1", c + "_lo3")]
with open("arroyo_polonio2026_tableA1.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print(len(rows), "rows written")
