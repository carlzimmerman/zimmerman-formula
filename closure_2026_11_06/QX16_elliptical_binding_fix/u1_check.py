#!/usr/bin/env python3
"""QX16 U1: after the fix, 7 distinct ellipticals; Mtot(1e9 kpc) = Mvir (1e-3), Mbar(1e9) = ups_krou*LK (1e-6)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
Q5 = [a for a in sys.argv[1:] if not a.startswith("--")][0] if [a for a in sys.argv[1:] if not a.startswith("--")] else os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")
src = open(Q5).read(); i0 = src.index("def ellipticals():"); i1 = src.index("\ndef ", i0 + 5)
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")}
exec("import math, os\nimport numpy as np\nHERE=os.path.dirname(__file__); REPO=os.path.dirname(os.path.dirname(HERE)); DATA=os.path.join(REPO,'real_research','data')\n" + src[i0:i1], NS)
E = NS["ellipticals"]()
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
hdr = rows[0]; D = [dict(zip(hdr, r)) for r in rows[1:]]
A1 = "--A1" in sys.argv; out = []; ok = True
for e, d in zip(E, D):
    mt = e["Mtot"](float(d["Rvir_kpc"])) if A1 else e["Mtot"](1e9); mb = e["Mbar"](1e9); mv = float(d["Mvir_1e12"]) * 1e12; mk = float(d["ups_krou"]) * float(d["LK_1e11"]) * 1e11
    r1, r2 = abs(mt / mv - 1), abs(mb / mk - 1); ok &= (r1 <= 1e-3 and r2 <= 1e-6 and e["name"] == d["name"])
    out.append(dict(name=e["name"], Mtot_1e9=mt, Mvir=mv, rel_tot=r1, Mbar_1e9=mb, Mb_expected=mk, rel_bar=r2))
distinct = len({round(o["Mtot_1e9"], -6) for o in out}) == len(out); ok &= distinct
for o in out: print(f"{o['name']:8s} Mtot({'Rvir' if A1 else '1e9'}) {o['Mtot_1e9']:.4e} vs Mvir {o['Mvir']:.4e} ({o['rel_tot']:.1e}); Mbar {o['Mbar_1e9']:.4e} vs {o['Mb_expected']:.4e} ({o['rel_bar']:.1e})")
print(f"distinct: {distinct}; U1 {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
