#!/usr/bin/env python3
# CRG1 COMPARE: sealed v1 against FG1's table, classes as frozen. Reads only; run from this folder.
import ast, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
SEAL = "da3c91046c6ac045aae63873365b4b01c0a77247b5efd1648fcff3d4740a9315"
J = lambda *p: json.load(open(os.path.join(RB, *p)))
raw = open(os.path.join(HERE, "v1", "crg1_results.json"), "rb").read()
assert hashlib.sha256(raw).hexdigest() == SEAL, "seal broken"
R = json.loads(raw)
H = J("FG1_final_grade", "fg1_harness_results.json")
F = J("FG1_final_grade", "fg1_results.json")
ZN = J("ZN4_cluster_resolution", "zn4_results.json")["runs"]
NR = J("NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")["runs"]
README = open(os.path.join(RB, "FG1_final_grade", "README.md")).read()
TOL = {"stat": (0.01, 0.03), "Z": (0.10, 0.30), "dchi2": (1.0, 3.0)}
NUM = r"[-+−]?\d+\.\d+"
rows = []


def num(s):
    return float(s.replace("−", "-"))


def cls(kind, a, b):
    d = abs(a - b); m, c = TOL[kind]
    return "MATCH" if d <= m else "CLOSE" if d <= c else "DISAGREE"


def add(cand, foot, line, item, kind, crg, fg1):
    rows.append(dict(cand=cand, foot=foot, line=line, item=item, kind=kind, crg=crg, fg1=fg1, d=crg - fg1, cls=cls(kind, crg, fg1)))


def flip(cand, foot, line, crg, fg1):
    rows.append(dict(cand=cand, foot=foot, line=line, item="PASS/FAIL", kind="status", crg=crg, fg1=fg1, d=None, cls="MATCH" if crg == fg1 else "DISAGREE"))


def md_tables():
    # FG1's three scorecard tables: canonical C1/C2, canonical C3/C4, alt C3/C4
    out = {}; sets = [("canonical", "C1", "C2"), ("canonical", "C3", "C4"), ("alt", "C3", "C4")]
    sec = README[README.index("## Scorecard"):]; blocks = re.findall(r"\| Line \|.*?\n((?:\|.*\n)+)", sec)
    for (foot, a, b), blk in zip(sets, blocks):
        for row in blk.splitlines()[1:]:
            c = [x.strip() for x in row.strip("|").split("|")]
            if len(c) != 3: continue
            ln = c[0].split()[0]
            out[(a, foot, ln)] = c[1]; out[(b, foot, ln)] = c[2]
    return out


T = md_tables()
status = lambda s: None if "NOT GRADED" in s else "PASS" in s[:12]
BG = ("A_c2b_refit", "B_cfg886_bg")
CELLS = [("C1", "canonical"), ("C2", "canonical"), ("C3", "canonical"), ("C4", "canonical"), ("C3", "alt"), ("C4", "alt")]
for c, fo in CELLS:
    r = R[c][fo]
    for ln, keys in [("S", None), ("Tl", "tilt"), ("LT", "median_E")]:
        txt = T[(c, fo, ln)]; v = [num(x) for x in re.findall(NUM, txt)]
        by = r[ln]["by_background"]
        if ln == "S":  # U a/b, rms a/b
            for i, b in enumerate(BG):
                add(c, fo, ln, f"Y {b[0]}", "stat", by[b]["Y_med"], v[i]); add(c, fo, ln, f"rms {b[0]}", "stat", by[b]["rms"], v[2 + i])
        else:
            for i, b in enumerate(BG): add(c, fo, ln, f"{keys} {b[0]}", "stat", by[b][keys], v[i])
        flip(c, fo, ln, r[ln]["passed"] if ln != "Tl" else r[ln].get("passed"), status(txt))
    # groups
    txt = T[(c, fo, "G")]
    if c != "C2":
        add(c, fo, "G", "Z", "Z", r["G"]["Z"], num(re.search(r"Z (" + NUM + ")", txt).group(1))); flip(c, fo, "G", r["G"]["passed"], status(txt))
    # keys
    txt = T[(c, fo, "K")]; kk = r["K"]
    flip(c, fo, "K", kk["passed"], status(txt))
    if c in ("C1", "C3"): src = {h: ZN["f* 0.034, gas +0.005"]["cells"][h] for h in ("h0672", "h0686")}; getz = lambda h, k: src[h][k]["Z"]
    elif c == "C2": src = NR["EM1|blum"]["keys"]["Z"]; getz = lambda h, k: src[h][k]
    else: src = None
    if src is not None:
        for h in ("h0672", "h0686"):
            for k, cell in kk["tables"][h].items(): add(c, fo, "K", f"{k} {h}", "Z", cell["Z"], getz(h, k))
    else:
        for k, cell in kk["tables"]["h0672"].items():
            if k in H[c][fo]["clusters"]: add(c, fo, "K", f"{k} h0672", "Z", cell["Z"], H[c][fo]["clusters"][k]["Z"])
    bad = set(re.findall(r"G-[A-Z]+-[A-Za-z0-9]+", txt.split("worst")[0]))
    rows.append(dict(cand=c, foot=fo, line="K", item="failing set", kind="set", crg=sorted(kk["failing"]), fg1=sorted(bad), d=None, cls="MATCH" if set(kk["failing"]) == bad else "DISAGREE"))
    # X-COP
    txt = T[(c, fo, "X")]
    if "NOT GRADED" not in txt:
        v = [num(x) for x in re.findall(NUM, txt)]; add(c, fo, "X", "mean", "stat", r["X"]["mean"], v[0]); add(c, fo, "X", "rms", "stat", r["X"]["rms"], v[1]); flip(c, fo, "X", r["X"]["passed"], status(txt))
    # lensing
    txt = T[(c, fo, "Ln")]
    if c == "C1":
        v = [num(x) for x in re.findall(NUM, txt)]; add(c, fo, "Ln", "dchi2(H2H-L2H)", "dchi2", r["Ln"]["D0"], v[0]); add(c, fo, "Ln", "dchi2 alt", "dchi2", r["Ln"]["alt_reported"]["D0"], v[1]); flip(c, fo, "Ln", r["Ln"]["passed"], status(txt))
    elif c != "C2":
        L = H[c][fo]["lensing"]; add(c, fo, "Ln", "ENV-L", "dchi2", r["Ln"]["d_ENV_L"], L["d_LF_L"]); add(c, fo, "Ln", "ENV-H", "dchi2", r["Ln"]["d_ENV_H"], L["d_LF_H"]); flip(c, fo, "Ln", r["Ln"]["passed"], status(txt))
    # dwarfs
    txt = T[(c, fo, "Dw")]
    if c != "C2":
        for name, z in re.findall(r"(MW ultra-faint|bright M31|M31 others|MW classical|LG field) (" + NUM + ")", txt):
            add(c, fo, "Dw", name, "Z", r["Dw"]["classes"][name]["Z"], num(z))
        flip(c, fo, "Dw", r["Dw"]["passed"], status(txt))

# gas-conditional input
g = R["C1"]["canonical"]["K"]["GAS_CONDITIONAL_input"]
# K4: Tier C sources exist and carry their values
miss = []
src = open(os.path.join(RB, "FG1_final_grade", "fg1_read.py")).read()
lits = ast.literal_eval(re.search(r"LITS = (\[.*?\])\nmiss4", src, re.S).group(1))
for p, l in lits:
    if l not in open(os.path.join(RB, p)).read(): miss.append((p, l))
paths = ["UR3_direct_weighing/ur3_mw.json", "UR3_direct_weighing/ur3_diskmass.json", "BS1_basin_switch/bs1_basin_switch_results.json", "RF2_ic1613_inclination_footing/rf2_ic1613_results.json", "FC1_cold_share_native_eta/x79_rule/x79_kids_grade_native.json"]
miss += [p for p in paths if not os.path.exists(os.path.join(RB, p))]

# bite: the classes must move on a planted error
assert cls("Z", 4.41, 4.41) == "MATCH" and cls("Z", 4.41, 4.0) == "DISAGREE" and cls("stat", .07, .09) == "CLOSE"

n = {k: sum(x["cls"] == k for x in rows) for k in ("MATCH", "CLOSE", "DISAGREE")}
out = dict(counts=n, gas_conditional_input=g, k4_missing=miss, k4_literals=len(lits), fg1_verdicts=F["verdicts"], rows=rows)
json.dump(out, open(os.path.join(HERE, "crg1_compare.json"), "w"), indent=0, sort_keys=True, default=str)
print("cells", len(rows), n, "K4 missing", miss, "of", len(lits), "literals +", len(paths), "files")
print("gas input:", json.dumps(g)[:200])
for x in rows:
    if x["cls"] != "MATCH":
        print(x["cls"], x["cand"], x["foot"], x["line"], x["item"], "CRG", x["crg"], "FG1", x["fg1"], "d", x["d"])
worst = {}
for x in rows:
    if x["d"] is not None:
        k = (x["kind"]); worst[k] = max(worst.get(k, 0), abs(x["d"]))
print("largest |d| by kind:", worst)
sys.exit(0)
