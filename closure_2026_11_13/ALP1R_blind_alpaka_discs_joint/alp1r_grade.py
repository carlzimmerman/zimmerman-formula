#!/usr/bin/env python3
"""ALP1R twin bites and final labels (READING.md section 6), from alp1r.json and the two *_MUTATE_* outputs.
  python3 alp1r_grade.py -> alp1r_grade.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda n: json.load(open(os.path.join(HERE, n)))
M, TN, TD = L("alp1r.json"), L("alp1r_MUTATE_TWN.json"), L("alp1r_MUTATE_TWD.json")
def short(w): return w.split(" (")[0] if not w.startswith("NO VERDICT") else w
OUT, RES = [], dict(lane="ALP1R", part="grade", foot={})
for ft in ("canonical", "alt"):
    gm = M["foot"][ft]["main"]["groups"]["ABOVE"]; gn = TN["foot"][ft]["main"]["groups"]["ABOVE"]; gd = TD["foot"][ft]["main"]["groups"]["ABOVE"]
    t = gm["gate"]; qm, qn, qd = gm[t], gn[t], gd[t]
    main_span = abs(qm["chi2"] - qm["chi0"]); n_span = abs(qn["chi2"] - qn["chi0"])
    bite_N = bool((main_span > 4 * qm["s2"] and n_span < 1e-6) or short(gn["word"]) != short(gm["word"]))
    um = qm["bestA"] if 0 < qm["bestA"] < 6 and qm["i95"][1] >= 6 else qm["i95"][1]
    ud = qd["bestA"] if 0 < qd["bestA"] < 6 and qd["i95"][1] >= 6 else qd["i95"][1]
    ratio = ud / um if um > 0 else float("nan")
    bite_D = bool(short(gd["word"]) != short(gm["word"]) or (0.35 <= ratio <= 0.65))
    ka = all(v["pass_"] for v in M["KA"].values())
    lab0 = M["foot"][ft]["label_before_twins"]
    final = lab0 if (ka and bite_N and bite_D) else ("NO VERDICT (" + ", ".join(x for x, ok in (("a known answer fails", ka), ("TW-N does not bite", bite_N), ("TW-D does not bite", bite_D)) if not ok) + ")")
    RES["foot"][ft] = dict(gate=t, main_span=main_span, twn_span=n_span, four_s2=4 * qm["s2"], bite_N=bite_N, upper_main=um, upper_twd=ud, ratio=ratio, bite_D=bite_D,
                           known_answers=ka, reading_before_twins=lab0, label=final)
    OUT.append(f"[{ft}] gate {t}: TW-N main |chi2(2)-chi2(0)| {main_span:.2f} vs 4 s2 {4*qm['s2']:.2f}, TW-N span {n_span:.2e}, word {short(gn['word'])} -> bites {bite_N}")
    OUT.append(f"[{ft}] TW-D: upper A main {um:.3f} -> twin {ud:.3f} (ratio {ratio:.3f}; bite window 0.35-0.65), word {short(gd['word'])} -> bites {bite_D}")
    OUT.append(f"[{ft}] known answers pass: {ka}; reading before twins: {lab0}")
    OUT.append(f"[{ft}] LABEL AS FROZEN: {final}")
json.dump(RES, open(os.path.join(HERE, "alp1r_grade.json"), "w"), indent=1)
open(os.path.join(HERE, "alp1r_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
print("\n".join(OUT))
