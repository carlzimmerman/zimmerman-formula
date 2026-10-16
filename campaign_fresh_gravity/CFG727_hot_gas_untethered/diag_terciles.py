"""Diagnostic (POST-HOC, not a verdict): CFG727 primary (s|canonical|P, also alt) eRASS1 band A by gas-mass tercile, with
CFG721's condensed and plain-law rows for comparison.  Reads stored work files only.  Run: python3 diag_terciles.py"""
import os
import numpy as np
LANES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
ER = list(np.load(os.path.join(EXT, "cfg727_work", "erass.npy"), allow_pickle=True))
D, E = d["D"], d["E"]; W = np.where(E > 0, 1 / E ** 2, 0); n = len(D)
order = np.argsort(d["ra"]); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
A_of = lambda sel, Pm: {b: (W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * Pm[sel][:, j]).sum() for b, j in BANDS.items()}
def jk(sel0, Pm):
    full = A_of(sel0, Pm); reps = [A_of(sel0 & (patch != p_), Pm) for p_ in range(30)]
    return {k: (full[k], np.sqrt(29 / 30 * np.sum((np.array([r[k] for r in reps]) - np.mean([r[k] for r in reps])) ** 2))) for k in full}
mg = d["mg"]; q = np.quantile(mg, [1 / 3, 2 / 3])
T = [mg <= q[0], (mg > q[0]) & (mg <= q[1]), mg > q[1]]
print(f"gas-mass terciles (log Mg): <= {np.log10(q[0]):.2f}, <= {np.log10(q[1]):.2f}, > ; n {[int(t.sum()) for t in T]}")
for lab, k in (("CFG727 P canonical", "s|canonical|P"), ("CFG727 P alt", "s|alt|P")):
    Pm = np.array([o[k]["base"] + o[k]["res"] for o in ER])
    print(f"\n{lab}:")
    for i, t in enumerate(T):
        A = jk(t, Pm)
        print(f"  tercile {i + 1}: MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f}  OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f}  INNER {A['INNER'][0]:.2f}")
Pl = d["PL"]
print("\nplain law (CFG687 PL):")
for i, t in enumerate(T):
    A = jk(t, Pl); print(f"  tercile {i + 1}: MID {A['MID'][0]:.2f}+-{A['MID'][1]:.2f}  OUTER {A['OUTER'][0]:.2f}+-{A['OUTER'][1]:.2f}")
