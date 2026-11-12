#!/usr/bin/env python3
"""XF1 Stage B run list (FROZEN_CRITERIA.md 8b99d12c42): writes xf1_runlist.txt, one xf1_hydro.py argument line per run,
longest runs first. Every cell on both footings; UNIFORM and HEDGEHOG starts; the two V readings (vi 0/1, vi 1 = the 3D
speed is primary); coarse for every row, medium for the representative row (largest gpar) of B1/B2, for B3/B4/B5 as listed;
known-answer runs KB1 (reduced M 490 REFLECT, AC15's exact run), KB2 (HEDGEHOG, no wind), KB3 (UNIFORM, gravity off)."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "xf1_cells.json")))
FOOTS = ("canonical", "alt")
REP = {"B1": 0, "B2": 6, "B3": 0, "B4": 0, "B5": 0}            # representative rows: DFX1 (max gpar); Sextans (the dSph row where the linear static start is valid, gN/gext 0.011)
runs = {"kb": [], "medium": [], "coarse": []}


def add(k, **kw):
    s = " ".join(f"--{a} {v}" if v is not True else f"--{a}" for a, v in kw.items() if v is not None and v is not False)
    runs[k].append(s)


# known answers (short, first)
add("kb", cell="B5", foot="canonical", row=0, vi=1, bc="reflect", start="uniform", res="coarse", reduced=True, Mover=490)      # KB1 bitwise vs AC15
for res in ("coarse", "medium"):
    add("kb", cell="B1", foot="canonical", row=0, vi=1, start="uniform", res=res, nograv=True)                                 # KB3 galaxy grid
    add("kb", cell="B5", foot="canonical", row=0, vi=1, start="uniform", res=res, nograv=True, tend=50)                        # KB3 Sun grid (AC15 KA3)
    add("kb", cell="B1", foot="canonical", row=0, vi=1, start="hedgehog", res=res, nowind=True)                                # KB2 galaxy grid
add("kb", cell="B5", foot="canonical", row=0, vi=0, start="hedgehog", res="coarse", nowind=True, tend=50)                      # KB2 Sun (AC15 KA4)
add("kb", cell="B2", foot="canonical", row=REP["B2"], vi=1, start="hedgehog", res="coarse", nowind=True)
add("kb", cell="B1", foot="canonical", row=0, vi=1, start="hedgehog", res="coarse", nowind=True, hhstart="d10")                 # the record's static phantom under the kernel (reported)
# B3/B4 HEDGEHOG (and their holds) NOT RUN: the linear EFE phantom is outside its validity there (gN/gext > 1 at the readout)
for f in FOOTS:
    # B1, B2: every row at vi 1 both starts coarse; the representative row also at vi 0 (coarse) and on medium (both V, both starts)
    for cell in ("B1", "B2"):
        for i in range(len(C["cells"][f][cell]["rows"])):
            for start in ("uniform", "hedgehog"):
                add("coarse", cell=cell, foot=f, row=i, vi=1, start=start, res="coarse")
        for start in ("uniform", "hedgehog"):
            add("coarse", cell=cell, foot=f, row=REP[cell], vi=0, start=start, res="coarse")
            for vi in (0, 1):
                add("medium", cell=cell, foot=f, row=REP[cell], vi=vi, start=start, res="medium")
    # B3, B4 (report-only proxies): coarse both V both starts, medium UNIFORM vi 1
    for cell in ("B3", "B4"):
        for vi in (0, 1):
            add("coarse", cell=cell, foot=f, row=0, vi=vi, start="uniform", res="coarse", tend=30, rin=0.1)
        add("medium", cell=cell, foot=f, row=0, vi=1, start="uniform", res="medium", tend=30, rin=0.1)
    # B5 (AC15 architecture): both M, TRANSMIT uniform coarse + medium, hedgehog coarse; REFLECT uniform coarse at vi 1 (AC15's worst bracket)
    for vi in (0, 1):
        add("coarse", cell="B5", foot=f, row=0, vi=vi, start="uniform", res="coarse")
        add("coarse", cell="B5", foot=f, row=0, vi=vi, start="hedgehog", res="coarse")
        add("medium", cell="B5", foot=f, row=0, vi=vi, start="uniform", res="medium")
    add("coarse", cell="B5", foot=f, row=0, vi=1, bc="reflect", start="uniform", res="coarse")
lines = runs["kb"] + runs["medium"] + runs["coarse"]
open(os.path.join(HERE, "xf1_runlist.txt"), "w").write("\n".join(lines) + "\n")
print(len(runs["kb"]), "KB runs,", len(runs["medium"]), "medium,", len(runs["coarse"]), "coarse ->", len(lines), "runs")
