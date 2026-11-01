#!/usr/bin/env python3
"""HL2 POST-RESULT, reported only, never graded: the source K1 dropped (Okabe+Martino), and what K1's width comes from. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); s = open(os.path.join(HERE, "hl2.py")).read(); s = s[:s.index("USE = [k for k in S if k not in DROP]")].replace("os.path.abspath(__file__)", repr(os.path.join(HERE, "hl2.py")))
exec(s); OUT.clear(); OUT.append("HL2 POST-RESULT, not graded")
def show(lab, srcs, keep=None):
    u = combine(srcs); x = np.array([v for k, v in u.items() if keep is None or k in keep]); g = float(np.median(x)); e = bs(x); P(f"{lab}: n {len(x)}, g {g:+.3f} +- {e:.3f}, mean {x.mean():+.3f}, rms {x.std():.3f}: would read {cl(g, e)}")
    return u
P("=== after K1's drop: reproduces hl2.out"); show("Mahdavi + Zhang", ["Mahdavi+13", "Zhang+10"])
P("=== Okabe+Martino"); O = show("Okabe+Martino alone", ["Okabe16+Martino14"]); A = show("all three sources", list(S)); show("Mahdavi + Okabe+Martino", ["Mahdavi+13", "Okabe16+Martino14"])
a = {q["n"]: q for q in S["Mahdavi+13"]}; b = {q["n"]: q for q in S["Okabe16+Martino14"]}; c = sorted(set(a) & set(b)); P(f"same {len(c)} clusters: Mahdavi g {np.median([math.log10(a[n]['mw'] / a[n]['mh']) for n in c]):+.3f}; Okabe+Martino g {np.median([math.log10(b[n]['mw'] / b[n]['mh']) for n in c]):+.3f}")
y = np.array([(math.log10(q["mg"] * 1.034 / q["mw"] / .15945), math.log10(q["mg"] * 1.034 / q["mh"] / .15945)) for q in S["Okabe16+Martino14"] if q["mg"] > 0]); P(f"Okabe+Martino f* 0.034, n {len(y)}: log Y_WL {np.median(y[:, 0]):+.3f} +- {bs(y[:, 0]):.3f}, log Y_hyd {np.median(y[:, 1]):+.3f} +- {bs(y[:, 1]):.3f}")
ch = [(ZO[k], MA[k]["r"], v(MA[k]["c"])) for k in MA if k in ZO and np.isfinite(v(MA[k]["c"]))]; xm = [(ZO[k], MA[k]["r"], v(MA[k]["x"])) for k in MA if k in ZO and np.isfinite(v(MA[k]["x"]))]
for lab, t in (("r500 vs Chandra M500", ch), ("r500 vs XMM M500", xm)): t = np.array(t); o, w = k1(t[:, 0], t[:, 1], t[:, 2]); P(f"K1 diagnosis, {lab}: n {len(t)}, offset {o:+.4f}, width {w:.4f}")
open(os.path.join(HERE, "hl2_post.out"), "w").write("\n".join(OUT) + "\n")
