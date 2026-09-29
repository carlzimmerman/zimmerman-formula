"""CFG183 attack (d): dependence of the T amplitude on the flow-onset redshift. Exit 0."""
import os, json, math
import numpy as np
import CFG183_common as C
from CFG183_common import M, pr

S, AS, K = C.load("inc_star_deg")
ZONS = [None, 30, 20, 10, 7, 5]; OMS = [0.3111, 0.315]
pr("=== (d) flow-onset redshift grid for T:  f_T(z; z_on) = (t(z)-t(z_on))/(t0-t(z_on))")
rows = []; res = []
base = None
for Om in OMS:
    for zon in ZONS:
        law = C.make_law("T", Om=Om, zon=zon)
        dex = [float(np.log10(law(np.array([z]))[0])) for z in (0.85, 1.5, 2.5)]
        d1 = C.cell(S, AS, 1.0, 0.67, law)["H"]; d0 = C.cell(S, AS, 0.0, 0.67, law)["H"]
        bes = [C.breakeven(lambda m: C.cell(S, AS, s, m, law)["H"]) for s in C.S_PUB]
        st = [C.status(b) for b in bes]
        z0 = d0[0] / d0[1]
        surv = abs(z0) < 2 and bes[0]["mu"] is not None and bes[0]["lo"] <= 1.69 and bes[0]["hi"] >= 0.6
        r = dict(Om=Om, zon=("inf" if zon is None else zon), dex=dex, D1=d1, D0=d0, be0=C.fmt_be(bes[0]), be1=C.fmt_be(bes[1]), status=st, P0_survive=bool(surv),
                 sentence=C.headline_sentence({s: st[i] for i, s in enumerate(C.S_PUB)}))
        res.append(r)
        pr("  Om=%.4f z_on=%-4s dex(0.85/1.5/2.5)= %+.3f %+.3f %+.3f | D'(0.67,s=1) %+.3f+-%.3f  D'(s=0) %+.3f+-%.3f | mu_be s=0 %s ; s=1 %s | status %s | P0 survive %s" % (
            Om, r["zon"], *dex, *d1, *d0, r["be0"], r["be1"], "".join(x[0] for x in st), surv))
dex15 = [r["dex"][1] for r in res]
spread = max(dex15) - min(dex15)
ok_hi = all(r["status"][2:] == ["excluded"] * 4 for r in res)
ok_p0 = all(r["P0_survive"] for r in res)
pr("dex spread at z=1.5 over the grid: %.3f  (CFG181 found 0.105; my frozen line for ONSET-ROBUST is < 0.12)" % spread)
pr("dex range at z=1.5: min %.3f max %.3f" % (min(dex15), max(dex15)))
pr("s>=1.42 exclusions keep their labels in all cells: %s ; P0 survival in all cells: %s ; s=1 label 'excluded' in cells: %d of %d" % (ok_hi, ok_p0, sum(r["status"][1] == "excluded" for r in res), len(res)))
verdict = "ONSET-ROBUST" if (ok_hi and ok_p0 and spread < 0.12) else "ONSET-FRAGILE"
pr("VERDICT (frozen rule):", verdict)
ctl = [r for r in res if r["zon"] == "inf" and r["Om"] == 0.315][0]
pr("control: z_on = inf, Om = 0.315 row equals the main run: D'(s=1) %+.4f (main +0.3227), D'(s=0) %+.4f (main +0.0457)" % (ctl["D1"][0], ctl["D0"][0]))
pr("one-sidedness: max over the grid of D'_T(0.67,s=1) %+.3f, min %+.3f ; Big-Bang member is the least T-hostile: %s" % (
    max(r["D1"][0] for r in res), min(r["D1"][0] for r in res), all(r["D1"][0] >= ctl["D1"][0] - 1e-3 for r in res if r["Om"] == 0.315)))
json.dump(dict(rows=res, spread=spread, verdict=verdict), open(os.path.join(C.HERE, "CFG183_onset_d_results.json"), "w"), indent=1, default=lambda o: None if o is None else float(o))
