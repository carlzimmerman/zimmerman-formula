"""CFG183 POST-COMPARISON (phase 2; written and run only AFTER my main, MUTATE 1-8, attacks, onset and mock runs were saved).
Opens CFG175's committed results JSON and .out/.py were read after those runs. Not part of any frozen result. Exit 0."""
import os, json, math
import numpy as np
import CFG183_common as C
from CFG183_common import pr

j175 = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity", "CFG175_t_law_a0z_results.json")))["numbers"]
mine = json.load(open(os.path.join(C.HERE, "CFG183_main_results.json")))
S, AS, K = C.load("inc_star_deg")
T = C.make_law("T")
LAWF = {"flat": (None, "flat"), "rival": (None, "H"), "T": (T, "H")}
pr("=== decision cells (mu = 0.67): |mine - CFG175| for D', sigma")
mx = 0
for s in (1.0, 0.0):
    for L in ("flat", "rival", "T"):
        law, wh = LAWF[L]; d, e = C.cell(S, AS, s, 0.67, law)[wh]
        t = j175["cell"]["%.2f|%s" % (s, L)]
        mx = max(mx, abs(d - t["d"]), abs(e - t["e"]))
        pr("  s=%.0f %-5s mine %+.5f +- %.5f | CFG175 %+.5f +- %.5f | diff %+.1e %+.1e" % (s, L, d, e, t["d"], t["e"], d - t["d"], e - t["e"]))
pr("  max |diff| decision cells: %.2e" % mx)
pr("=== the (s, mu) map: KURVS mu in {0.25,0.67,1.5,4}, KROSS mu=0.67, all six s, three laws")
mxd = mxe = 0; n = 0
for s in C.S_PUB:
    for nm, smp, mus in (("KURVS", S, (0.25, 0.67, 1.5, 4.0)), ("KROSS", K, (0.67,))):
        for mu in mus:
            t = j175["map"]["%s|%.2f|%s" % (nm, s, mu)]
            for L in ("flat", "rival", "T"):
                law, wh = LAWF[L]; d, e = C.cell(smp, AS, s, mu, law)[wh]
                mxd = max(mxd, abs(d - t[L]["d"])); mxe = max(mxe, abs(e - t[L]["e"])); n += 1
pr("  %d cells compared: max |dD'| %.2e, max |dsigma| %.2e" % (n, mxd, mxe))
pr("=== break-evens and intervals (both finite): relative differences")
worst = (0, None); nfin = 0; nonfin = []
mine_be = {"KURVS": mine["be_K"], "KROSS": mine["be_R"]}
for key, v in j175["breakevens"].items():
    nm, s, L = key.split("|"); i = C.S_PUB.index(float(s)); m = mine_be[nm][L][i]
    for lab, a, b in (("mu", v[0], m["mu"]), ("lo", v[1], m["lo"]), ("hi", v[2], m["hi"])):
        if a is None or b is None:
            if not (a is None and b is None): nonfin.append((key, lab, a, b))
            continue
        nfin += 1; r = abs(a - b) / max(abs(a), 1e-9)
        if r > worst[0]: worst = (r, (key, lab, a, b))
pr("  %d finite values compared; worst relative difference %.2e at %s" % (nfin, worst[0], worst[1]))
pr("  values finite in one and missing in the other (reporting convention, listed):")
for x in nonfin: pr("    ", x)
pr("=== s0 fit points")
for nm, smp in (("KURVS", S), ("KROSS", K)):
    for L in ("flat", "rival", "T"):
        law, wh = LAWF[L]
        v = C.s_root(lambda s: C.cell(smp, AS, s, 0.67, law)[wh])
        t = j175["s0"][nm][L]
        pr("  %s %-5s mine %s | CFG175 %s" % (nm, L, ("%.4f" % v) if isinstance(v, float) else v, ("%.4f" % t) if t is not None else "< 0"))
pr("=== status labels and summary")
mp = {"over": "over-predicts", "allowed": "gas-allowed", "excluded": "gas-excluded"}
bad = 0
for i, s in enumerate(C.S_PUB):
    for L in ("flat", "rival", "T"):
        a = mp[mine["stat"][L][i]]; b = j175["status"]["%.2f|%s" % (s, L)]; bad += a != b
pr("  status labels different: %d of 18" % bad)
pr("  summary equal (modulo the 'STRONGLY DISFAVOURED' suffix wording): %s" % (mine["sentence"] in j175["summary"] and mine["strong"] and "STRONGLY DISFAVOURED" in j175["summary"]))
pr("=== independence check on HOW the two pipelines differ (from the code, read after my runs):")
pr("  CFG175 exec's CFG141's own pipeline and re-implements P4 pooling/anchor in its own terms/DS/pooled functions; mine imports the CFG165 referee module (which itself matched CFG160 after the inc_star_deg column).")
pr("  Both use the same data files, CFG140 set-up choices and Kretschmer alpha (shared). Root-finder: theirs a 36-node log grid + brentq; mine 200 nodes + brentq.")
pr("  The 1-sigma interval convention (roots of D'(mu) = +-sigma(mu), sigma evaluated at the trial mu) is the same; where no break-even exists theirs still prints an upper edge, mine prints none.")
