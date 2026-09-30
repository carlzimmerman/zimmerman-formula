#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 (draft rev 2, NOT FILED): the controls L1-L8 of SEED_LABEL_DESIGN_FROZEN.md (a9f0290bb) for seed_label.py (NEW file).  Offline; DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_seed_label.py        (MUTATE=1: the stale target 1.137 is ADDED to the edge table in L7's 'correct' case -- L7 must FAIL)"""
import sys
sys.dont_write_bytecode = True
import copy, json, math, os, re, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import seed_label as SL

MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, RES = [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(s)


def K(name, ok, detail=""):
    RES[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


P("SEED LABEL: controls L1-L8 (DR3 numbers are code-path tests, never results)" + (f"; MUTATE = {MUT}" if MUT else ""))
# ---------------------------------------------------------------- L1 extraction
table = SL.extract_edge_table()
mod = SL._load_module(SL.PIPELINE)
text = SL.PIPELINE.read_text()
names = sorted(n for n in dir(mod) if SL.FAMILY_RE.match(n))
in_table = set(x["constant"] for f in ("canonical", "alt") for x in table["targets"][f]) | set(x["constant"] for x in table["hard_edges"]) | set(table["excluded"]) | {"KAPPA_WINDOW"}
vals_ok = all(abs(x["gamma"] - getattr(mod, x["constant"])) == 0 for f in ("canonical", "alt") for x in table["targets"][f]) and all(abs(x["gamma"] - getattr(mod, x["constant"])) == 0 for x in table["hard_edges"])
reasons_ok = all(v["reason"] in text or table["excluded"][n]["reason"] == "an uncertainty, not an edge" for n, v in table["excluded"].items())
tmpd = Path(tempfile.mkdtemp())
plant = tmpd / "pipeline_plant.py"
plant.write_text(text + "\nGAMMA_PLANT = 1.5\n")
try:
    SL.extract_edge_table(plant, expected_sha=None); raised1 = False
except ValueError:
    raised1 = True
plant2 = tmpd / "pipeline_nostale.py"
plant2.write_text(text.replace("STALE per Amdt 4(i)", "obsolete"))
try:
    SL.extract_edge_table(plant2, expected_sha=None); raised2 = False
except ValueError:
    raised2 = True
K("L1 the edge table's in-force entries equal the pipeline attributes, every GAMMA_* / NOVERDICT_* / KAPPA_* attribute is classified, GAMMA_MG 1.137 is excluded and in no target or edge list, the pipeline's sha256 is the frozen one, sigma_sys 0.02 is found in the text; "
  "a planted unclassified constant and a planted removal of a reason string both make the extraction raise",
  vals_ok and set(names) == in_table and "GAMMA_MG" in table["excluded"] and table["excluded"]["GAMMA_MG"]["value"] == 1.137 and not any(x["constant"] == "GAMMA_MG" for f in ("canonical", "alt") for x in table["targets"][f])
  and table["pipeline_sha256"] == SL.FROZEN_PIPELINE_SHA256 and table["sigma_sys"] == 0.02 and reasons_ok and raised1 and raised2,
  f"{len(names)} constants classified ({len(table['targets']['canonical'])} canonical targets, {len(table['targets']['alt'])} alt, {len(table['hard_edges'])} hard edges, {len(table['excluded'])} excluded, kappa window {table['stability']['kappa_window']}); planted constant raises {raised1}; planted reason removal raises {raised2}; not in code: {len(table['not_in_code'])} items")

# ---------------------------------------------------------------- L2 edges at a hand-computed sigma_tot
st = math.hypot(0.019, 0.02)
E = dict(SL.edges_for(table, "canonical", st))
hand = {"GAMMA_B_PRED - 3 sigma_tot": 0.9172, "GAMMA_B_PRED - 2 sigma_tot": 0.9448, "GAMMA_B_PRED + 2 sigma_tot": 1.0552, "GAMMA_B_PRED + 3 sigma_tot": 1.0828}
Ea = SL.edges_for(table, "alt", st)
K("L2 at sigma_fit 0.019 (sigma_tot 0.02759) the z-rule edges around 1.0000 are 0.9172, 0.9448, 1.0552, 1.0828 (by hand); each hard edge appears once per footing; 23 edges per footing",
  all(abs(E[k] - v) < 6e-5 for k, v in hand.items()) and all(sum(1 for n, _ in Ea if n == c) == 1 for c in ("GAMMA_A_FALSIFIED_BELOW", "GAMMA_B_KILL", "NOVERDICT_EDGE")) and len(E) == 23 and len(Ea) == 23,
  f"sigma_tot {st:.5f}; {len(E)} / {len(Ea)} edges; B - 3 sigma {E['GAMMA_B_PRED - 3 sigma_tot']:.4f}, B + 3 sigma {E['GAMMA_B_PRED + 3 sigma_tot']:.4f}")

# ---------------------------------------------------------------- L3 label, below/above counts, far from every edge
SF = 0.019
off = np.linspace(-0.004, 0.004, 60)                                                     # a planted spread of builds around the primary
def builds_around(primary, off):
    return np.concatenate([[primary], primary + off])
sbuild = float(np.std(builds_around(1.0, off), ddof=1))
width = max(sbuild, 0.3 * SF)
edge = 1.084                                                                              # GAMMA_B_KILL
prim = edge + 0.5 * width
g = builds_around(prim, off)
r = SL.label_report(g, SF, table, "canonical")
fl = {e["edge"]: e for e in r["flagged"]}
direct_below, direct_above = int((g < edge).sum()), int((g >= edge).sum())
scan = np.arange(0.85, 1.45, 0.0005)
stc = math.hypot(SF, 0.02)
far = [x for x in scan if min(abs(x - v) for _, v in SL.edges_for(table, "canonical", stc)) > 2 * width][0]
r_far = SL.label_report(builds_around(far, off), SF, table, "canonical")
K("L3 a primary 0.5 width from an edge is labelled 'seed-sensitive' with below/above counts equal to a direct count; a primary more than 2 widths from every edge is not labelled",
  r["label"] == "seed-sensitive" and "GAMMA_B_KILL" in fl and fl["GAMMA_B_KILL"]["builds_below"] == direct_below and fl["GAMMA_B_KILL"]["builds_at_or_above"] == direct_above and r_far["label"].startswith("not seed-sensitive"),
  f"sigma_build {sbuild:.5f}, width {width:.5f} (set by {r['width_governed_by']}); primary {prim:.4f}: edges within the width {[e['edge'] for e in r['flagged']]}; counts {fl['GAMMA_B_KILL']['builds_below']} below / {fl['GAMMA_B_KILL']['builds_at_or_above']} at or above (direct {direct_below} / {direct_above}); far primary {far:.4f}: {r_far['label']}")

# ---------------------------------------------------------------- L4 the width rule
small = builds_around(1.0, np.linspace(-0.001, 0.001, 60))
big = builds_around(1.0, np.linspace(-0.03, 0.03, 60))
sb_small, sb_big = float(np.std(small, ddof=1)), float(np.std(big, ddof=1))
pr = 1.084 + 0.010
rs = SL.label_report(builds_around(pr, np.linspace(-0.001, 0.001, 60)), SF, table, "canonical")
rb = SL.label_report(builds_around(pr, np.linspace(-0.03, 0.03, 60)), SF, table, "canonical")
K("L4 the width is max(sigma_build, 0.3 sigma_fit): with a small spread it is 0.3 sigma_fit (0.0057) and a primary 0.010 from the edge is not labelled; with a large spread it is sigma_build and the same offset is labelled",
  rs["width_governed_by"] == "0.3 sigma_fit" and abs(rs["width"] - 0.3 * SF) < 1e-12 and not any(e["edge"] == "GAMMA_B_KILL" for e in rs["flagged"]) and rb["width_governed_by"] == "sigma_build" and any(e["edge"] == "GAMMA_B_KILL" for e in rb["flagged"]),
  f"small spread: SD {sb_small:.5f}, width {rs['width']:.5f}, B_KILL flagged {any(e['edge'] == 'GAMMA_B_KILL' for e in rs['flagged'])}; large spread: SD {sb_big:.5f}, width {rb['width']:.5f}, B_KILL flagged {any(e['edge'] == 'GAMMA_B_KILL' for e in rb['flagged'])}")

# ---------------------------------------------------------------- L5 stability conditions
win = table["stability"]["kappa_window"]
st1 = SL.stability_report([1.02, 1.04, 1.051, 1.03, 1.06], win, {"R_chance<0.001": [0.2, 0.9, 1.1, 0.3, 0.4]})
st2 = SL.stability_report([1.01, 1.02, 1.03], win, {"R_chance<0.001": [0.2, -0.5, 0.3]})
K("L5 stability: kappa crossing 1.05 in some builds is labelled 'seed-sensitive' (2 fail, 3 pass), all inside is 'stable'; a ladder rung whose shift crosses 1 sigma_fit in some builds is labelled, one that never does is 'stable'",
  st1["kappa window"]["label"] == "seed-sensitive" and st1["kappa window"]["passes"] == 3 and st1["kappa window"]["fails"] == 2 and st1["ladder R_chance<0.001"]["label"] == "seed-sensitive" and st2["kappa window"]["label"] == "stable" and st2["ladder R_chance<0.001"]["label"] == "stable",
  f"{st1['kappa window']}; {st1['ladder R_chance<0.001']}; {st2['kappa window']['label']}, {st2['ladder R_chance<0.001']['label']}")

# ---------------------------------------------------------------- L6 K requirement
r9 = SL.label_report(builds_around(1.084, np.linspace(-0.004, 0.004, 9)), SF, table, "canonical")
r10 = SL.label_report(builds_around(1.084, np.linspace(-0.004, 0.004, 10)), SF, table, "canonical")
K("L6 fewer than 10 further G-only builds gives 'NOT APPLICABLE (K < 10)' and no label; with 10 the label applies", r9["label"] == "NOT APPLICABLE (K < 10)" and "flagged" not in r9 and r10["label"] != r9["label"] and "flagged" in r10, f"K = 9: {r9['label']}; K = 10: {r10['label']}")

# ---------------------------------------------------------------- L7 the label bites on the list (MUTATE adds the stale target to the 'correct' table)
stale = copy.deepcopy(table)
stale["hard_edges"].append(dict(constant="GAMMA_MG_STALE", name="stale target planted as a hard edge", gamma=1.137))
correct = stale if MUT == "1" else table
p7 = builds_around(1.137, np.linspace(-0.001, 0.001, 60))
a_ = SL.label_report(p7, SF, correct, "canonical")
b_ = SL.label_report(p7, SF, stale, "canonical")
K("L7 a primary at 1.137 is NOT labelled by the extracted table (the stale target is excluded) but IS labelled when the stale 1.137 is planted as an edge: the label bites on the list",
  a_["label"].startswith("not seed-sensitive") and b_["label"] == "seed-sensitive",
  f"extracted table: {a_['label']} (nearest edges within the width: {[e['edge'] for e in a_['flagged']]}); with the stale edge: {b_['label']} ({[e['edge'] for e in b_['flagged']]})")

# ---------------------------------------------------------------- L8 DR3 rehearsal on the 51-build G-only sweep (if present)
mg = HERE / "seed_sweep_manifest_g50_dr3.json"                                              # the committed copy; falls back to the extract directory (gitignored)
if not mg.exists():
    mg = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract" / "seed_sweep" / "seed_sweep_manifest_g50.json"
if mg.exists():
    Ms = json.load(open(HERE / "seed_sweep_streams_dr3.json"))["QS"]["ALL"]["per_footing"]
    pseudo = {"builds": [{"fit": {f: {"g": Ms[f]["gammas"][k], "s": Ms[f]["sigma_fits"][k]} for f in ("canonical", "alt")}} for k in range(10)]}
    pf = tmpd / "all_ten_manifest.json"
    pf.write_text(json.dumps(pseudo))
    rep = SL.evaluate_sweep(mg, pf, table)
    lines = SL.format_report(rep)
    (HERE / "seed_label_dr3_rehearsal.out").write_text("DR3 REHEARSAL of the seed-sensitivity label (code path only; never a result)\nG-only: " + str(mg.name) + "; full-rebuild values: the ten ALL-family builds of seed_sweep_streams_dr3.json\n" + "\n".join(lines) + "\n")
    json.dump(rep, open(HERE / "seed_label_dr3_rehearsal.json", "w"), indent=1, default=float)
    K("L8 DR3 rehearsal: the label report is produced from the 51-build G-only manifest with the ten all-stream builds beside, for both footings, with the stability conditions", set(rep["footings"]) == {"canonical", "alt"} and all("label" in rep["footings"][f] for f in rep["footings"]) and all("stability" in rep["footings"][f] for f in rep["footings"]),
      "; ".join(f"{f}: {rep['footings'][f]['label']} ({len(rep['footings'][f].get('flagged', []))} edges within the width)" for f in rep["footings"]))
    P("\n".join("    " + l for l in lines))
else:
    P("  [not run here] L8 DR3 rehearsal (needs the 51-build G-only manifest seed_sweep_manifest_g50.json)")
ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / f"test_seed_label{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"test_seed_label_results{SFX}.json").write_text(json.dumps(dict(results=RES, mutate=MUT, seconds=round(time.time() - T0, 1)), indent=1) + "\n")
sys.exit(0 if ok else 1)
