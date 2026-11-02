#!/usr/bin/env python3
"""BF1 harvest: Stage 1 on full train, gates 3 and 4 on data the search never saw. Usage: bf1_read.py MODE. kappa = 1/2 FITTED; not theory closed."""
import json, os, pickle, sys
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else "real"]
import numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bf1.py")).read().split('if __name__ == "__main__"')[0])
W = os.path.join(HERE, "chunks", MODE + os.environ.get("BF1_SUF", "")); names = json.load(open(os.path.join(W, "names.json")))
hits = set()
for l in open(os.path.join(W, "hits.jsonl")):
    i, o, j, w = json.loads(l); hits.add((i, o, j, w))
print(f"{MODE}: complete {os.path.exists(os.path.join(W, 'COMPLETE'))}, prefilter hits {len(hits)}, leaves in L2 {len(names)}")
d0 = np.log10(ST[:, 1] / law(ST[:, 0], A0)); RT = np.sqrt((d0 ** 2).mean()); dh0 = np.log10(SH[:, 1] / law(SH[:, 0], A0)); RH = np.sqrt((dh0 ** 2).mean())
print(f"law SPARC rms train {RT:.4f} median {np.median(d0):+.4f}; holdout {RH:.4f} median {np.median(dh0):+.4f}; line {SF} x")
C_ = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb")); K = 3.0857e19; LT = []
for g in C_["lt"]:
    M = 10 ** g["logMb"]; R = g["R"] * K; LT.append((G * M * MS / R ** 2, (g["V"] * 1e3) ** 2 / R, R * A0 / C ** 2, max(0, 1 - g["Mstar"] / M), 0))
LT = np.array(LT); R1 = 1.496e11 * 9.58; SAT = np.array([[G * 1.989e30 / R1 ** 2, 1, R1 * A0 / C ** 2, 0, 0]])
def fin(v): return np.all(np.isfinite(v))
S1 = []; seen = set(); ST_, G3, G4 = 0, 0, 0
for i, o, j, w in sorted(hits, key=lambda t: len(names[t[0]]) + len(names[t[2]])):
    s = f"({names[i]}{o}{names[j]})"
    try: d = full(s, w, ST); dx = full(s, w, XT)
    except Exception: continue
    if not (fin(d) and fin(dx)): continue
    if abs(dx.mean()) > XM or np.sqrt((dx ** 2).mean()) > XR: continue
    r = np.sqrt((d ** 2).mean()); m = np.median(d)
    if r > SF * RT or abs(m) > SM: continue
    k = (w, round(float(r), 7), round(float(dx.mean()), 7))
    if k in seen: continue
    seen.add(k); ST_ += 1
    dh = full(s, w, SH); dxh = full(s, w, XH); rh = np.sqrt((dh ** 2).mean()); g3 = rh <= SF * RH and abs(np.median(dh)) <= SM and abs(dxh.mean()) <= XM and np.sqrt((dxh ** 2).mean()) <= XR
    e = full(s, w, LT); g4 = g3 and abs(np.median(e)) <= 0.10
    S1.append(dict(H=s, wrap=w, train_rms=float(r), train_med=float(m), xcop=float(dx.mean()), xcop_rms=float(np.sqrt((dx ** 2).mean())), hold_rms=float(rh), hold_med=float(np.median(dh)), xcop_hold=float(dxh.mean()), xcop_hold_rms=float(np.sqrt((dxh ** 2).mean())), LT=float(np.median(e)), g3=bool(g3), g4=bool(g4)))
    G3 += g3; G4 += g4
print(f"Stage 1 distinct {ST_}; gate 3 {G3}; gate 4 {G4}")
S1.sort(key=lambda a: (-a["g4"], -a["g3"], len(a["H"])))
for a in S1[:25]: print(f"W{a['wrap']} {a['H'][:70]:70s} train {a['train_rms']:.3f} {a['train_med']:+.3f} X {a['xcop']:+.3f},{a['xcop_rms']:.3f} | hold {a['hold_rms']:.3f} {a['hold_med']:+.3f} X {a['xcop_hold']:+.3f},{a['xcop_hold_rms']:.3f} LT {a['LT']:+.3f} {'G3' if a['g3'] else ''} {'G4' if a['g4'] else ''}")
json.dump(dict(mode=MODE, stage1=int(ST_), g3=int(G3), g4=int(G4), rows=S1[:2000]), open(os.path.join(HERE, f"bf1_{MODE}{os.environ.get('BF1_SUF', '')}_results.json"), "w"), indent=0)
