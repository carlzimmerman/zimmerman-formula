"""Diagnostic (POST-HOC, not a verdict): ACCEPT OUTER band A per cluster and leave-one-out, CFG815 profile P (s|canonical|EX)
vs the ALL control, from stored work files."""
import os, json, numpy as np
LANES = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
cls = json.load(open(os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_results.json")))["clusters"]
AC = list(np.load(os.path.join(EXT, "cfg815_work_P", "accept.npy"), allow_pickle=True))
D = np.nan_to_num(np.array([x["dsig"] for x in cls])); E = np.array([x["err"] for x in cls]); W = np.where(np.isfinite(E) & (E > 0), 1 / E ** 2, 0)
J = [6, 7]
A = lambda sel, Pm: (W[sel][:, J] * D[sel][:, J]).sum() / (W[sel][:, J] * Pm[sel][:, J]).sum()
for k in ("s|canonical|EX", "s|canonical|ALL"):
    Pm = np.array([o[k]["base"] + o[k]["res"] for o in AC]); n = len(cls); allm = np.ones(n, bool)
    print(f"\n{k}: OUTER all {A(allm, Pm):.2f}")
    for i in range(n):
        one = np.zeros(n, bool); one[i] = True; loo = allm.copy(); loo[i] = False
        print(f"  {cls[i]['name']:22s} z {cls[i]['z']:.2f}  own OUTER {A(one, Pm):.2f}  weight {W[i][J].sum() / W[:, J].sum():.2f}  LOO {A(loo, Pm):.2f}  f_eff {o_f if (o_f:=AC[i][k]['meta'].get('fret')) else 0:.2f}")
