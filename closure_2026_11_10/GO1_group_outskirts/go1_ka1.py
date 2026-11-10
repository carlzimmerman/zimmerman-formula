"""GO1 KA1 (FROZEN_CRITERIA.md): CFG686's esd() exec'd from its committed file vs GO1's copy (esd_x from go1_measure.py, run with
CFG686's physical edges, R500 = 1 Mpc so x = R) on 5 selected groups: identical DeltaSigma to 1e-10 relative; CFG686 SIS self-test.
python3 -I go1_ka1.py <kids column dir>. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG686_cluster_shear_vs_law", "cfg686_shear.py")
os.environ.pop("MUTATE", None); g = {"__file__": SRC, "__name__": "cfg686"}; sys.argv = [SRC, sys.argv[1]]
exec(open(SRC).read().split("# ---- measure ----")[0], g)
mine = open(os.path.join(HERE, "go1_measure.py")).read(); fsrc = mine[mine.index("def esd_x"):mine.index("# ---- y strips")]
g.update(NB=8, XMAX=3.0); exec(fsrc, g)                                   # g["EDGES"] is CFG686's physical edges (Mpc)
GRP = [(152.9, -1.2, 0.12), (180.3, 0.5, 0.08), (214.1, 1.1, 0.21), (5.2, -31.0, 0.15), (340.6, -29.5, 0.27)]
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "..", "_external_data", "cfg687_inputs", "erass1_main.tsv"))]
sel = []
for r in rows:
    try: ra, de, z, mg = float(r[1]), float(r[2]), float(r[3]), float(r[5])*1e11
    except Exception: continue
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and -35 < de < 3.5 and 0.05 <= z <= 0.30 and 1.35e12 <= mg <= 1.15e13: sel.append((ra, de, z))
worst = 0.0; used = 0
for ra, de, z in sel:
    a = g["esd"](ra, de, z); b = g["esd_x"](ra, de, z, 1.0)
    if a is None or b is None: continue
    d2 = b["numt"]/b["den"]/g["KG_PER_MSUN_PC2"]/(1 + g["M_BIAS"]); okb = np.isfinite(a[0]) & np.isfinite(d2)
    rel = np.max(np.abs(d2[okb] - a[0][okb])/np.maximum(np.abs(a[0][okb]), 1e-30)); worst = max(worst, rel); used += 1
    print(f"  ({ra:.3f}, {de:.3f}, z {z:.3f}) bins {okb.sum()}, max rel diff {rel:.2e}; den equal: {np.allclose(a[2], b['den'], rtol=1e-12)}")
    if used == 5: break
print(f"KA1 estimator copy vs CFG686 esd on {used} selected groups: max rel diff {worst:.2e} -> {'PASS' if worst < 1e-10 and used == 5 else 'FAIL'}")
