#!/usr/bin/env python3
"""JNT1R, REPORTED ONLY (post hoc, not in READING.md's grade): do the class lines L1, L2, L3 hold for a LIGHTER reference
halo (A = 0.25 ... 1.5 x the record's share)? jnt1r.py's definitions are executed from its own source up to its
"known answers" marker (nothing written by that part).
  nice -n 19 python3 jnt1r_light.py -> jnt1r_light.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "jnt1r.py"); code = open(SRC).read()
NS = {"__file__": SRC, "__name__": "jnt1r_lib"}; _a = sys.argv; sys.argv = [SRC]
exec(compile(code[:code.index("# ---------------- known answers")], SRC, "exec"), NS); sys.argv = _a
np = NS["np"]; build_src = code[code.index("def build(ft"):code.index("def fmt_word")]; exec(compile(build_src, SRC, "exec"), NS)
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("JNT1R light-halo scan (REPORTED, post hoc). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
RES = {}
for ft in NS["FOOTS"]:
    D = NS["build"](ft); RES[ft] = {}
    for A in (0.25, 0.4, 0.5, 0.58, 0.75, 1.0, 1.25, 1.5):
        dd, ee, sh, she = [], [], [], []; s = [0.0, 0.0, 0.0]; sl = [0.0, 0.0, 0.0]
        for d in D:
            lg = NS["model_lg"](d, ft, "ref", A); st = NS["gal_stats"](d, lg, NS["IU"][0.50]); dd.append(st["d"]); ee.append(st["e"])
            if st["D"] is not None: sh.append(st["D"]); she.append(st["eD"])
            f = NS["gal_stats"](d, lg, NS["fit_U"](d, lg)); s[0] += f["chi2"]; s[1] += f["swr"]; s[2] += f["sw"]
            ll = NS["model_lg"](d, ft, "law", withT=True); fl = NS["gal_stats"](d, ll, NS["fit_U"](d, ll)); sl[0] += fl["chi2"]; sl[1] += fl["swr"]; sl[2] += fl["sw"]
        c1, c2 = NS["cls"](dd, ee), NS["cls"](sh, she); rms, mean, rl = math.sqrt(s[0] / s[2]), s[1] / s[2], math.sqrt(sl[0] / sl[2])
        l3 = bool(rms <= rl + 0.010 and abs(mean) <= 0.05)
        RES[ft][str(A)] = dict(L1=c1, L2=c2, L3=dict(rms=rms, mean=mean, law_rms=rl, line=l3))
        P(f"[{ft}] A {A:4.2f}: L1 off {c1['med']:+.4f} (3se {3 * c1['se']:.4f}) {'holds' if c1['line'] else 'FAILS'}; L2 shape {c2['med']:+.4f} (3se {3 * c2['se']:.4f}) {'holds' if c2['line'] else 'FAILS'}; "
          f"L3 fit-mode rms {rms:.4f} mean {mean:+.4f} vs law {rl:.4f} {'holds' if l3 else 'FAILS'}")
json.dump(RES, open(os.path.join(HERE, "jnt1r_light.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "jnt1r_light.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
