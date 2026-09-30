"""CFG230 script G: class screening by the ranking rule FROZEN in section 6 (before any ranking). Prioritisation only, not a scoring.
MUTATE=M8 flips one label (C02 AeST, R05: M -> F[m])."""
import re
import CFG230_common as C
import CFG230_data as D

R = C.Run("CFG230_G_screening")
M = C.mode()
R.p(f"CFG230 G. repo=<repo> mode={M or 'main'}")
REQS = D.REQS
H = [r for i, r in enumerate(REQS) if not any(v[i] == "P" for v in D.MATRIX.values())]
theorem_core = [r for r in REQS if any(cl == "THEOREM" and lb for (_, cl, gr, lb) in D.SUB[r])]
R.p(f"  hard-core set H (from the frozen matrix) = {H}; theorem-core requirements = {theorem_core}")

def parse(cell):
    m = re.match(r"^(M|F|U|N)(?:\[(T|s|m)\])?$", cell)
    return m.group(1), m.group(2)

classes = {k: (n, dict(c)) for k, (n, c) in D.CLASSES.items()}
if M == "M8":
    classes["C02"][1]["R05"] = "F[m]"
def labels(cdict):
    return {r: parse(cdict.get(r, "U")) for r in REQS}
m_val = {"M": 1, "U": 0, "N": 0, "F": -1}

def score(lab, req_list, w=None):
    return sum(m_val[lab[r][0]] * (w.get(r, 1) if w else 1) for r in req_list)

def rank(cls, req_list, w=None):
    rows = []
    for k, (n, cd) in cls.items():
        lab = labels(cd)
        tierX = any(lab[r] == ("F", "T") for r in REQS)
        nF = sum(1 for r in REQS if lab[r][0] == "F"); nM = sum(1 for r in REQS if lab[r][0] == "M")
        rows.append(dict(id=k, name=n, tierX=tierX, S=score(lab, req_list, w), nF=nF, nM=nM, lab=lab))
    Y = sorted([r for r in rows if not r["tierX"]], key=lambda r: (-r["S"], r["nF"], -r["nM"], r["name"]))
    X = sorted([r for r in rows if r["tierX"]], key=lambda r: r["name"])
    return Y, X

Y, X = rank(classes, H)
R.p("\n== tier X (excluded by theorem: a cell F[T]): " + ", ".join(f"{r['id']} {r['name']}" for r in X))
R.p("\n== tier Y ranked by the frozen rule (S over H, then fewer F, more M, name)")
R.p("  rank  id   S   nF nM  class")
for i, r in enumerate(Y, 1):
    R.p(f"  {i:>3}   {r['id']}  {r['S']:>2}  {r['nF']:>2} {r['nM']:>2}  {r['name']}   M-cells: {[q for q in REQS if r['lab'][q][0]=='M']}  F-cells: {[q+'['+(r['lab'][q][1] or '')+']' for q in REQS if r['lab'][q][0]=='F']}")
R.res["tierY"] = [(r["id"], r["S"], r["nF"], r["nM"]) for r in Y]; R.res["tierX"] = [r["id"] for r in X]

# statements required by the rule (item 5)
allM = [r for r in Y if all(r["lab"][q][0] == "M" for q in H)]
noF = [r for r in Y if r["nF"] == 0]
R.p("\n== rule item 5")
R.p(f"  classes with M on every requirement of H: {[r['id'] for r in allM] or 'none'}")
R.p(f"  classes (tier Y) with no F on any requirement: {[(r['id'], r['name']) for r in noF]}")
if not allM:
    R.p("  STATEMENT: NO KNOWN CLASS MEETS ALL OF THESE (no class has M on every requirement of H; most cells are U because the requirements are about mechanisms, not class labels).")
if len(noF) == 1:
    R.p(f"  exactly one class has no F: {noF[0]['name']}; its U cells: {[q for q in REQS if noF[0]['lab'][q][0]=='U']}")
else:
    R.p(f"  the 'exactly one open class' branch of the rule is NOT triggered: {len(noF)} classes carry no F, all of them only because their cells are U (undecided by structure) or N; this does not isolate an open class.")
R.check("EXPECT", "hand expectation 6: the ranking is coarse (few distinct S values) and no class meets all of H", len({r["S"] for r in Y}) <= 4 and not allM, f"distinct S over tier Y: {sorted({r['S'] for r in Y}, reverse=True)}")

# controls: labels from the door rows
R.p("\n== scored-door controls (labels from the matrix rows: P->M, p*->U, F->F[s], U->U, N->N; C15's R01 carries [T])")
ctrl = {}
for cid, (nm, row, extra) in D.CONTROLS.items():
    cd = {}
    for i, r in enumerate(REQS):
        code = D.MATRIX[row][i]
        cd[r] = {"P": "M", "p*": "U", "F": "F[s]", "U": "U", "N": "N"}[code]
    cd.update(extra)
    lab = labels(cd)
    tierX = any(lab[r] == ("F", "T") for r in REQS)
    ctrl[cid] = (nm, lab, tierX, score(lab, H))
    R.p(f"  {cid} {nm}: S(H) = {score(lab, H)}, F cells over H = {sum(1 for r in H if lab[r][0]=='F')}, tier {'X' if tierX else 'Y'}")
R.check("EXPECT", "controls reproduce their door rows: S(H) = -(number of F over H); C15 in tier X", all(ctrl[c][3] == -sum(1 for r in H if ctrl[c][1][r][0] == 'F') for c in ctrl) and ctrl["C15"][2], "")

# sensitivities (reported, not chosen among)
def order(Yl): return [r["id"] for r in Yl]
w2 = {r: 2 for r in theorem_core}
Ya, Xa = rank(classes, H, w2)
Yb, Xb = rank(classes, REQS)
base = order(Y)
R.p("\n== sensitivities (not chosen among)")
R.p(f"  base:                       {base}")
R.p(f"  THEOREM-core doubled:       {order(Ya)}  changes: {[c for c in base if base.index(c) != order(Ya).index(c)]}")
R.p(f"  all twelve requirements:    {order(Yb)}  changes: {[c for c in base if base.index(c) != order(Yb).index(c)]}")
R.res["sens_doubled"] = order(Ya); R.res["sens_all12"] = order(Yb); R.res["base_order"] = base
top3 = {"base": base[:3], "doubled": order(Ya)[:3], "all12": order(Yb)[:3]}
R.p(f"  top three under each weighting: {top3}")

if M == "M8":
    # baseline ranking without the flip
    classes0 = {k: (n, dict(c)) for k, (n, c) in D.CLASSES.items()}
    Y0, X0 = rank(classes0, H)
    r0 = order(Y0).index("C02") + 1; r1 = base.index("C02") + 1
    tier_same = [r["id"] for r in X0] == [r["id"] for r in X]
    R.p(f"  M8: C02 (AeST) R05 M -> F[m]: rank {r0} -> {r1}; tier X membership unchanged: {tier_same}")
    C.bite(R, r0 != r1, "AeST's rank changes when its one M cell is flipped")
# ---------------------------------------------------------------- Amendment 2: the record's galileon scripts (frozen 6.2 note on C13)
import subprocess, sys
R.p("\n== Amendment 2 (post-freeze): C13 labels after reading the record's galileon scaling scripts")
outs = []
for p_ in D.AMEND2_SOURCE:
    pr = subprocess.run([sys.executable, "-B", C.os.path.join(C.REPO, p_)], capture_output=True, text=True, cwd=C.HERE)
    outs.append(pr.stdout)
    R.p(f"  ran {p_.split('/')[-1]}: exit {pr.returncode}")
t1, t2 = outs
R.check("CITATION-AUDIT", "no single power n gives the MOND deep limit (mass exponent n=2, radius exponent n=3/2): mutually inconsistent", "MUTUALLY INCONSISTENT" in t1 and "n = [2]" in t1, "in-lane sympy (grade S), not refereed")
R.check("CITATION-AUDIT", "Galileon helicity-0 spherical scaling never gives r^-1 (n = 3/2 not an integer operator)", "NEVER gives r^-1" in t2 and "3/2" in t2)
R.check("CITATION-AUDIT", "regime inversion: nonlinearity acts near the source (screening inward), MOND needs it far away", "REGIME INVERSION" in t1 and "WRONG regime" in t1)
Ya2 = None
classes2 = {k: (n, dict(c)) for k, (n, c) in D.CLASSES.items()}
for k, ch in D.AMEND2_LABELS.items():
    classes2[k][1].update(ch)
Y2, X2 = rank(classes2, H)
R.p("  amended ranking (tier Y): " + str([(r["id"], r["S"]) for r in Y2]))
R.p(f"  C13 rank {order(Y).index('C13')+1} -> {order(Y2).index('C13')+1}; top three now {order(Y2)[:3]}")
R.p("  Amendment 2 cell: C13 R03 U -> F[s] (the no-go is about the deep-MOND SHAPE from one dominant Galileon term, in-lane sympy, not refereed). C13's R09 M (Vainshtein screening, MEMORY) stands and is the same mechanism that inverts the regime.")
R.res["amended_order"] = order(Y2); R.res["amended_C13_rank"] = order(Y2).index("C13") + 1
R.write()
