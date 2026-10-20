"""CFG892 POST HOC (written after the graded run; NOT graded, does not change the class).
The graded run put Carina's Q95 (3.208 km/s, cell P4 f 0.7) only 0.013 km/s above its need (3.195), so 'reached' may be Monte-Carlo
noise of a max-over-15-cells 95th percentile.  This script: (1) lists Carina's 15 graded-cell 95th percentiles from cfg892_results.json;
(2) re-runs cfg892.py's own functions (extracted with ast, nothing re-implemented) for the main-run seed of Carina's most generous cell
and checks that it reproduces the committed value exactly; (3) repeats the 15 graded cells with 4 new seed sets (variant 200-203) and
reports the spread of the max-over-cells Q95 and how often it reaches the need; (4) pools the 5 seed sets at cells (P4, 0.7) and
(P3, 0.7) (R = 5000) for a lower-noise 95th percentile.  Canonical footing (the alt margin is 0.47 km/s).
Run: python3 cfg892_post.py -> cfg892_post.out, cfg892_post.json.  kappa = 1/2 FITTED; not theory closed."""
import os, ast, json, time, numpy as np
T0 = time.time(); HERE = os.path.dirname(os.path.abspath(__file__)); MAIN = os.path.join(HERE, "cfg892.py")
src = open(MAIN).read(); tree = ast.parse(src); body = []
for node in tree.body:
    if "K1 (binary fraction 0" in (ast.get_source_segment(src, node) or ""): break
    body.append(node)
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("measure", "run_cell", "needs", "classify"): body.append(node)
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("sq", "f_idx") for t in node.targets): body.append(node)
ns = {"__file__": MAIN, "__name__": "cfg892_subset"}
os.environ.pop("CFG892_MUTATE", None)
exec(compile(ast.Module(body=body, type_ignores=[]), "cfg892_subset", "exec"), ns)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
RES = json.load(open(os.path.join(HERE, "cfg892_results.json")))
d = ns["SYSD"]["Carina"]; sl = d["slaw"]["canonical"]; nd = ns["needs"](d, "canonical"); need = nd["need"]; sq = ns["sq"]
GK = [(p, f) for p in ("P1", "P2", "P3", "P4", "P5") for f in (0.3, 0.5, 0.7)]
P("CFG892 POST HOC (not graded): Monte-Carlo scatter of Carina's Q95, canonical footing")
P(f"  Carina |M| {len(d['M'])}, sigma_law {sl:.4f}, need {need:.4f} km/s")
cellq = {f"{p}|{f}": RES["cells"][f"Carina|canonical|{p}|{f}|0"]["ex_clean_q95"] for p, f in GK}
P("  (1) main-run 95th percentiles by cell: " + "  ".join(f"{k} {v:.3f}{'*' if v >= need else ''}" for k, v in cellq.items()) + "   (* = reaches the need)")
def q95(a): return float(np.quantile(sq(a["sc"] ** 2 - sl ** 2), 0.95))
a0 = ns["run_cell"](d, sl, 0.7, "P4", (d["si"], ns["POP_IDX"]["P4"], ns["f_idx"][0.7], 0, 0)); r0 = q95(a0)
ok = r0 == cellq["P4|0.7"]
P(f"  (2) reproduction of the main-run cell (P4, 0.7): {r0:.12f} vs committed {cellq['P4|0.7']:.12f} -> {'IDENTICAL' if ok else 'DIFFERENT'}")
POOL = {"P4|0.7": [a0["sc"]], "P3|0.7": [ns["run_cell"](d, sl, 0.7, "P3", (d["si"], ns["POP_IDX"]["P3"], ns["f_idx"][0.7], 0, 0))["sc"]]}
QS = []
for j in range(4):
    qs = {}
    for p, f in GK:
        a = ns["run_cell"](d, sl, f, p, (d["si"], ns["POP_IDX"][p], ns["f_idx"][f], 0, 200 + j)); qs[f"{p}|{f}"] = q95(a)
        if f"{p}|{f}" in POOL: POOL[f"{p}|{f}"].append(a["sc"])
    best = max(qs, key=qs.get); QS.append(dict(seed=200 + j, Q95=qs[best], cell=best, reached=qs[best] >= need, n_cells_reached=sum(v >= need for v in qs.values())))
    P(f"  (3) seed set {200 + j}: Q95 {qs[best]:.3f} ({best}), reached {qs[best] >= need}, cells reaching the need {QS[-1]['n_cells_reached']}/15   [{time.time() - T0:.0f} s]")
allq = [RES["per_dwarf"]["Carina|canonical"]["Q95"]] + [x["Q95"] for x in QS]
P(f"  max-over-cells Q95 over 5 seed sets (main + 4): {', '.join(f'{x:.3f}' for x in allq)}; mean {np.mean(allq):.3f}, sd {np.std(allq, ddof=1):.3f};"
  f" reached in {sum(x >= need for x in allq)}/5")
PL = {}
for k, v in POOL.items():
    sc = np.concatenate(v); ex = sq(sc ** 2 - sl ** 2); qq = float(np.quantile(ex, 0.95))
    bs = np.random.default_rng(892).integers(0, len(ex), (400, len(ex))); qb = np.quantile(ex[bs], 0.95, axis=1)
    PL[k] = dict(R=int(len(ex)), q95=qq, q95_boot_sd=float(np.std(qb)), P_sc_ge_obs=float(np.mean(sc >= nd["sig_obs"])), reached=qq >= need)
    P(f"  (4) pooled {k} (R {len(ex)}): 95th percentile {qq:.3f} +- {np.std(qb):.3f} (bootstrap) vs need {need:.3f} -> {'reached' if qq >= need else 'not reached'};"
      f" P(sigma_clean,sim >= sigma_obs {nd['sig_obs']:.3f}) = {PL[k]['P_sc_ge_obs']:.4f}")
P(f"  runtime {time.time() - T0:.0f} s")
json.dump(dict(lane="CFG892", post_hoc=True, need=need, sigma_law=sl, main_cells=cellq, reproduction_identical=bool(ok), seed_sets=QS,
               Q95_all=allq, pooled=PL), open(os.path.join(HERE, "cfg892_post.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
open(os.path.join(HERE, "cfg892_post.out"), "w").write("\n".join(OUT) + "\n")
