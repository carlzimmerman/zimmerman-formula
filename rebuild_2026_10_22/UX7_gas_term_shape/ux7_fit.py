#!/usr/bin/env python3
"""UX7 k on X-COP train, per footing, and X-COP rows, forms, rivals, controls. --mutate: k x 3. kappa = 1/2 FITTED; not theory closed."""
from ux7_common import *
MUT = "--mutate" in sys.argv; OUT = []; R = {}
def P(s): print(s, flush=True); OUT.append(str(s))
X, nm, M5, Mg5 = xcop_full(); j = X[:, 4].astype(int); tr = j % 2 == 0; ho = ~tr; P(f"X-COP {nm}; train {sorted(set(np.array(nm)[j[tr] if False else [q for q in sorted(set(j)) if q % 2 == 0]]))}; lines |mean| <= 0.05, rms <= 0.10")
def row(a0, form, k, pqt=None):
    d = lambda m: resid(X[m], M5[m], Mg5[m], a0, form, k, pqt); h, a, t = st(d(ho))[:2], st(d(tr | ho))[:2], st(d(tr))[:2]; return dict(k=k, train=t, hold=h, all=a, all_hse=float(a[0] - .12), xpass=bool(abs(h[0]) <= .05 and h[1] <= .10 and abs(a[0]) <= .05 and a[1] <= .10), hold_margin=float(max(abs(h[0]) - .05, h[1] - .10)), all_margin=float(max(abs(a[0]) - .05, a[1] - .10)))
for ft, a0 in A0S.items():
    R[ft] = {"forms": {}, "ctrl": []}; P(f"\n=== {ft}")
    for f in FORMS + RIV:
        k, b = fit(X[tr], M5[tr], Mg5[tr], a0, f); o = row(a0, f, k * (3 if MUT else 1)); o["at_bound"] = b; R[ft]["forms"][f] = o; P(f"{f} k {o['k']:.5g}{' AT BOUND' if b else ''}: train {o['train'][0]:+.3f},{o['train'][1]:.3f}; unseen {o['hold'][0]:+.3f},{o['hold'][1]:.3f}; all 7 {o['all'][0]:+.3f},{o['all'][1]:.3f}; HSE-0.12 {o['all_hse']:+.3f}; {'PASS' if o['xpass'] else 'FAIL'}; margin to line unseen {o['hold_margin']:+.3f}, all {o['all_margin']:+.3f}")
    if not MUT:
        for pqt in controls():
            k, b = fit(X[tr], M5[tr], Mg5[tr], a0, "P", pqt); o = row(a0, "P", k, pqt); o.update(pqt=pqt, at_bound=b); R[ft]["ctrl"].append(o)
        P(f"controls: X-COP pass {sum(o['xpass'] for o in R[ft]['ctrl'])} of 40; at bound {sum(o['at_bound'] for o in R[ft]['ctrl'])}")
T = "_MUTATE" if MUT else ""; json.dump(R, open(os.path.join(HERE, f"ux7_fit{T}.json"), "w"), indent=0); open(os.path.join(HERE, f"ux7_fit{T}.out"), "w").write("\n".join(OUT) + "\n")
if not MUT:
    u = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); d = max(abs(R[f]["forms"]["F0"]["k"] - u[f]) for f in u); P(f"K2 F0 fit vs ux3_kfit: max |d| {d:.1e}: {'PASS' if d <= 1e-5 else 'FAIL'}")
