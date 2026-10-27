"""IB1 part 2 RF: HG with the record's regression sigma fill for the 220 no-kT clusters (FROZEN_CRITERIA_RF.md, 9e54055970).
kappa = 1/2 FITTED; not theory closed.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ib1_rf.py [--mutate]
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, "ib1_hse_halo.py")).read().split("P(\"IB1 HG")[0])    # HG's model functions, verbatim
import numpy as np
TAG = "_MUTATE" if MUT else ""; OUT = []; RES = dict(frozen="9e54055970", mutate=MUT); checks = []
def P(s): OUT.append(s); print(s, flush=True)
HGJ = json.load(open(os.path.join(HERE, "ib1_hse_halo_results.json")))
MG = ("G-IN-Mall", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3")

def cells_all(foot):
    c = {}
    for hk in L.HK:
        V, _ = vectors(foot, hk); c[hk] = L.cells_from(foot, hk, V)[0]
    return c, {k: all(abs(c[h][k]["Z"]) <= 2 for h in L.HK) for k in c["h0672"]}

P("IB1 RF (HG + regression sigma fill)" + (" [MUTATE: slope -b]" if MUT else "") + "; kappa = 1/2 FITTED; not theory closed")
TERC = L.SIG_C.copy()
if not MUT:   # K0: tercile fill reproduces HG's committed cells
    d0 = 0.0
    for foot in L.FEET:
        c, _ = cells_all(foot)
        d0 = max(d0, max(abs(c[h][k]["pred"] - HGJ["footings"][foot]["cells"][h][k]["pred"]) for h in L.HK for k in c[h]))
    k0 = d0 < 1e-12; checks.append(("K0", k0)); P(f"K0 tercile fill vs HG committed cells: max |dpred| {d0:.1e}: {'PASS' if k0 else 'FAIL'}")

# the fill (IC1 D5's definition, verbatim arithmetic)
lm = np.log10(np.asarray(NX["MY"]["Mgas500"], float)); ls = np.log10(TERC)
A_ = np.c_[np.ones(L.OKK.sum()), lm[L.OKK]]; co = np.linalg.lstsq(A_, ls[L.OKK], rcond=None)[0]
if MUT: co = np.array([ls[L.OKK].mean() + co[1] * lm[L.OKK].mean(), -co[1]])
rms = float(np.std(ls[L.OKK] - (co[0] + co[1] * lm[L.OKK])))
k1 = round(float(co[1]), 3) == 0.139; checks.append(("K1", k1))
P(f"fit: log10 sigma = {co[0]:.4f} + {co[1]:.4f} log10 Mgas500 (n {int(L.OKK.sum())}, rms {rms:.3f} dex); K1 slope 0.139: {'PASS' if k1 else 'FAIL'}")
L.SIG_C[:] = TERC; L.SIG_C[~L.OKK] = 10 ** (co[0] + co[1] * lm[~L.OKK])
P(f"filled sigma (220): 5/50/95% {np.percentile(L.SIG_C[~L.OKK], [5, 50, 95]).round(0).tolist()} km/s (tercile fill: {sorted(set(np.round(TERC[~L.OKK]).tolist()))})")
RES["fit"] = dict(a=float(co[0]), b=float(co[1]), rms_dex=rms, n=int(L.OKK.sum()))

classes, cls15 = {}, {}
for foot in L.FEET:
    hg = HGJ["footings"][foot]; o1ok = L.OS1J["footings"][foot]["clusters"]["ok"]; o1c = L.OS1J["footings"][foot]["clusters"]["cells"]
    c, ok = cells_all(foot)
    P(f"\n=== [{foot}] cells (h 0.672 | h 0.686): Z (HG-tercile Z h 0.672)")
    for k in c["h0672"]:
        P(f"   {k:10s} meas {c['h0672'][k]['meas']:+.3f}+-{c['h0672'][k]['s']:.3f} pred {c['h0672'][k]['pred']:+.3f} Z {c['h0672'][k]['Z']:+.2f} | "
          f"{c['h0686'][k]['Z']:+.2f}  {'pass' if ok[k] else 'FAIL'}   (HG-tercile {hg['cells']['h0672'][k]['Z']:+.2f})")
    zm3 = max(abs(c[h]["G-OUT-M3"]["Z"]) for h in L.HK); zm3hg = max(abs(hg["cells"][h]["G-OUT-M3"]["Z"]) for h in L.HK)
    if all(ok[k] for k in MG): cl = "FILL-RESOLVED"
    elif zm3 < zm3hg and not [k for k in MG if hg["ok"][k] and not ok[k]]: cl = "PARTIAL"
    else: cl = "NOT RESOLVED"
    classes[foot] = cl
    zin = max(abs(c[h]["G-IN-Mall"]["Z"]) for h in L.HK); zin1 = max(abs(o1c[h]["G-IN-Mall"]["Z"]) for h in L.HK)
    nf = [k for k in ok if o1ok[k] and not ok[k]]
    c15 = "PASS" if all(ok.values()) else "IMPROVES" if (zin < zin1 and not nf) else "TRADES" if ((ok["G-IN-Mall"] or zin < zin1) and nf) else "FAILS"
    cls15[foot] = c15
    P(f"  MGAS cells: {', '.join(k + (' pass' if ok[k] else ' FAIL') for k in MG)}; G-OUT-M3 max|Z| {zm3:.2f} (HG-tercile {zm3hg:.2f})")
    P(f"  CLASS [{foot}]: {cl}   (reported 15-cell class: {c15}; OS1-passing cells failing: {nf or 'none'})")
    # reported: OUTER pred/meas split, canonical-style (h 0.672)
    hk = "h0672"; dd = L.DAT[hk]; WB = dd["W"] * dd["B"][None, :]; n = WB * (dd["D"] - NX["MY"]["leakP"][:, NX["HXI"][hk], 0])
    VC = L.DC[(foot, hk)]; V, _ = vectors(foot, hk); ob = NX["BANDS"]["OUTER"]; sp = {}
    for t in range(3):
        for lab, m in (("KT", L.OKK), ("fill", ~L.OKK)):
            s = (L.T3M == t) & m; sp[f"M{t+1} {lab}"] = float((V[s][:, ob].sum() / VC[s][:, ob].sum()) / (n[s][:, ob].sum() / VC[s][:, ob].sum()))
    P("  (reported) OUTER pred/meas h 0.672: " + "; ".join(f"{k} {v:.2f}" for k, v in sp.items()))
    RES[foot] = dict(cells=c, ok=ok, cls=cl, cls15=c15, zm3=zm3, new_fail_vs_OS1=nf, outer_split=sp)
k2 = rss() < 2.0; checks.append(("K2", k2))
v = classes["canonical"] if classes["canonical"] == classes["alt"] else "UNDECIDED"
v15 = cls15["canonical"] if cls15["canonical"] == cls15["alt"] else "UNDECIDED"
P(f"\nK2 peak RSS {rss():.2f} GB: {'PASS' if k2 else 'FAIL'}")
P(f"=== VERDICT (both footings): RF {v}   (reported 15-cell class: {v15}); checks " + ", ".join(f"{k} {'PASS' if x else 'FAIL'}" for k, x in checks))
RES.update(verdict=v, verdict15=v15, checks=dict(checks))
json.dump(RES, open(os.path.join(HERE, f"ib1_rf_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"ib1_rf{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(x for _, x in checks) else 1)
