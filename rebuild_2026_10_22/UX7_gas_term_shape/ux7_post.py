#!/usr/bin/env python3
"""UX7 post-result diagnostics, no label: F1 X-COP at scanned k, per-key Z, k x 3 on F6 and F8, the one X-COP-passing control, K5 with gas's qd power, binomial bound. kappa = 1/2 FITTED; not theory closed."""
from ux7_common import *
from scipy.stats import beta
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
J = lambda n: json.load(open(os.path.join(HERE, n))); G = J("ux7_keys_g005_f034.json"); M = J("ux7_keys_MUTATE_g005_f034.json"); FI = J("ux7_fit.json"); RD = J("ux7_read.json"); X, nm, M5, Mg5 = xcop_full(); j = X[:, 4].astype(int); tr = j % 2 == 0
def zs(r, h="h0672"): return " ".join(f"{k.replace('G-', '')} {v:+.2f}" for k, v in r["Z"][h].items())
for f, a0 in A0S.items():
    for x in ("F0", "F1", "F3"):
        k0 = FI[f]["forms"][x]["k"]
        for m in (.85, 1., 1.15, 1.3):
            d = resid(X, M5, Mg5, a0, x, k0 * m); h = d[~tr]; r = G[f"R1|c0|{f}|{x}:{k0 * m:.8g}"]; P(f"{f} {x} k x{m}: keys {r['n']}, over 2 {','.join(q.replace('G-', '') for q in r['bad'])}; X-COP unseen {h.mean():+.3f},{np.sqrt((h * h).mean()):.3f}; all {d.mean():+.3f},{np.sqrt((d * d).mean()):.3f}; train {d[tr].mean():+.3f}")
        if x == "F1":
            for m in (1., 1.3): P(f"   Z h0672 x{m}: " + zs(G[f"R1|c0|{f}|{x}:{k0 * m:.8g}"])); P(f"   Z h0686 x{m}: " + zs(G[f"R1|c0|{f}|{x}:{k0 * m:.8g}"], "h0686"))
    for x in ("F6", "F8"):
        r = M[f"R1|c0|{f}|{x}:{3 * FI[f]['forms'][x]['k']:.8g}"]; o = FM = J("ux7_fit_MUTATE.json")[f]["forms"][x]; P(f"{f} {x} k x3 (MUTATE): keys {r['n']}, over 2 {r['bad']}; X-COP unseen {o['hold'][0]:+.3f},{o['hold'][1]:.3f}; {zs(r)}")
    C = RD["ctrl"][f]["rows"]; p = [c for c in C if c["x"]]; P(f"{f} controls passing X-COP: " + "; ".join(f"p {c['pqt'][0]:.2f} q {c['pqt'][1]:.2f} t {c['pqt'][2]:.2f}: keys {c['n']}, |Z| {c['w']:.2f}, joint {c['p']:.2g}" for c in p))
    n = RD["ctrl"][f]["frac_x"] * 40; P(f"{f} frozen fraction {n:.0f}/40, one-sided 95 % upper bound {beta.ppf(.95, n + 1, 40 - n):.3f}; F1 vs F0 worst |Z| {RD['rows'][f]['F1']['cells']['g005_f034']['w']:.2f} vs {RD['rows'][f]['F0']['cells']['g005_f034']['w']:.2f}")
K = J("ux7_keys_POST_k5.json"); a = K["R1|c0|canonical|R1G:10"]["Z"]["h0672"]; b = K["R1|c0|canonical|F0:10"]["Z"]["h0672"]; P(f"K5 diagnosis: R1 with M scaled qd^2.5 as gas, vs F0: max |dZ| {max(abs(a[q] - b[q]) for q in a):.4f}")
open(os.path.join(HERE, "ux7_post.out"), "w").write("\n".join(OUT) + "\n")
