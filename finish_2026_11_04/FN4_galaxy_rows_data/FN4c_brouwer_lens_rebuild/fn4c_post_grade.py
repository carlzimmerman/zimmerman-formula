#!/usr/bin/env python3
"""FN4c POST-RESULT stage-2 checks (written after fn4c_grade.py ran; no label changes; not in FROZEN_CRITERIA.md).

  B1  the frozen stage-2 MUTATE (lens masses x 2) did not bite (dZ -0.19 / -0.03): the graders bin lenses by mass, so a uniform
      shift mostly moves lenses between bins. This twin instead changes the model, as LE1's own MUTATE did: LE1's candidate
      rebuild_2026_10_22/LE1_lensing_estimator_audit/candidates/le1_law_x2.py (twice the law's g), on the rebuilt inventory.
  B2  the law on the V8 inventory (fn4c_post.py Q1: flux scale rebuilt from LePhare for every row; 259,166 lenses).
Reuses fn4c_grade.py's mirror builder and WLENS model by import; the child below is fn4c_grade.child with the candidate as a
parameter. Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I fn4c_post_grade.py -> fn4c_post_grade.out / .json.
kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.
"""
import importlib.util, json, math, os, subprocess, sys, types
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fn4c_grade as FG

LAWX2 = os.path.join(FG.RB, "LE1_lensing_estimator_audit", "candidates", "le1_law_x2.py")
LAW = os.path.join(FG.RQ3, "candidates", "law.py")


def child(cfg, cand_path):
    # identical to fn4c_grade.child except: the candidate file is a parameter and the output file name carries the run name
    src = open(os.path.join(HERE, "fn4c_grade.py")).read()
    i = src.index("def child(cfg):"); j = src.index("\ndef main():", i)
    body = src[i:j].replace("def child(cfg):", "def _child(cfg, CAND, TAGNAME):")
    body = body.replace('os.path.join(RQ3, "candidates", "law.py")', "CAND").replace('f"child_{cfg}.json"', 'f"postchild_{TAGNAME}.json"')
    assert body.count("CAND") == 2 and body.count("TAGNAME") == 2
    ns = dict(FG.__dict__); exec(compile(body, "fn4c_grade_child", "exec"), ns)
    ns["_child"](cfg, cand_path, sys.argv[4])


def main():
    OUT = []
    def P(*a):
        s_ = " ".join(str(x) for x in a); print(s_, flush=True); OUT.append(s_)
    P("FN4c POST-RESULT stage-2 checks (no label changes). kappa = 1/2 FITTED; not theory closed.")
    june = dict(np.load(os.path.join(FG.CRG, "inputs", "lensing", "lens_inventory.npz")))
    v8 = np.load(os.path.join(FG.CACHE, "fn4c_lenses_V8.npz"))
    FG.build_mirror("fn4c_V8", dict(logM=v8["logM"], z=v8["z"], WLENS=FG.wlens_model(june, v8["logM"], v8["z"])))
    runs = [("B1_fn4c_lawx2", "fn4c", LAWX2), ("B2_fn4c_V8_law", "fn4c_V8", LAW)]
    res = {}
    for name, cfg, cp in runs:
        r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "child", cfg, cp, name], capture_output=True, text=True, cwd=HERE)
        if r.returncode != 0:
            P(f"{name} FAILED: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'no stderr'}"); return 1
        res[name] = json.load(open(os.path.join(FG.CACHE, f"postchild_{name}.json")))
    base = json.load(open(os.path.join(HERE, "fn4c_grade.json")))["results"]["fn4c"]
    out = {}
    for foot in FG.FEET:
        b1 = res["B1_fn4c_lawx2"][foot]; b2 = res["B2_fn4c_V8_law"][foot]; o = base[foot]
        out[foot] = dict(B1_dZ_G1=b1["S0"]["Z"] - o["S0"]["Z"], B1_G1_chi2=b1["S0"]["chi2"], B1_G3_z=b1["G3"]["z"],
                         B2_G1_Z=b2["S0"]["Z"], B2_G3_z=b2["G3"]["z"], B2_A1_mean=b2["A1"]["mean"])
        P(f"[{foot}] B1 law x 2 on the rebuilt inventory: G1 chi2 {o['S0']['chi2']:.1f} -> {b1['S0']['chi2']:.1f} (dZ {out[foot]['B1_dZ_G1']:+.1f}), "
          f"G3 z {o['G3']['z']:+.2f} -> {b1['G3']['z']:+.2f} -> {'BITES' if abs(out[foot]['B1_dZ_G1']) > 1.0 else 'DOES NOT BITE'}")
        P(f"[{foot}] B2 law on the V8 inventory: G1 Z {b2['S0']['Z']:+.2f}, G3 z {b2['G3']['z']:+.2f}, A1 mean {b2['A1']['mean']:+.3f} dex "
          f"(primary inventory {o['S0']['Z']:+.2f}, {o['G3']['z']:+.2f}, {o['A1']['mean']:+.3f})")
    json.dump(dict(results=res, summary=out), open(os.path.join(HERE, "fn4c_post_grade.json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(HERE, "fn4c_post_grade.out"), "w").write("\n".join(OUT) + "\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 4 and sys.argv[1] == "child":
        child(sys.argv[2], sys.argv[3])
    else:
        sys.exit(main())
