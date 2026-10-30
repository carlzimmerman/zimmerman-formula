#!/usr/bin/env python3
"""CL5 Part B (see FROZEN_CRITERIA.md): X74 grader unchanged at the stipulated eta 21.2/14.3/14.3, via CE1's grade().
    python3 cl5_grade.py [--mutate]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CE = os.path.join(os.path.dirname(HERE), "CE1_converged_eta_grade", "ce1_grade.py"); T = open(CE).read()
T = T[:T.index("R0 = {}")].replace("HERE = os.path.dirname(os.path.abspath(__file__))", f"HERE = {HERE!r}", 1)
MUTATE = "--mutate" in sys.argv; argv0 = sys.argv; sys.argv = [CE]; NS = {"__file__": CE, "__name__": "ce1_ro"}; exec(compile(T, CE, "exec"), NS); sys.argv = argv0
grade, summ = NS["grade"], NS["summ"]; cf = lambda eta: 4 * (eta / 10.82) ** 0.8; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
TB = lambda a, b, c: {"1e+12": cf(a), "1e+13": cf(b), "1e+14": cf(c)}
P("CL5 Part B (see FROZEN_CRITERIA.md); stipulated target, not a prediction; kappa = 1/2 FITTED; not theory closed")
RES = {}
if MUTATE:
    b = json.load(open(os.path.join(HERE, "cl5_B_results.json")))["runs"]["0.034"]["canonical"]["sparc"]["A_c2b_refit"]["U"]; R = summ(grade("CL5_B_MUTATE", TB(10.6, 14.3, 14.3), "0.034"), "canonical")
    d = R["sparc"]["A_c2b_refit"]["U"] - b; P(f"MUTATE 1e12 eta x 0.5: canonical SPARC median Upsilon {d:+.3f} (must rise): {'PASS' if d > 0 else 'FAIL'}")
    open(os.path.join(HERE, "cl5_B_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if d > 0 else 1)
C1 = json.load(open(os.path.join(os.path.dirname(HERE), "CE1_converged_eta_grade", "ce1_results.json")))["runs"]["med_fs0.034"]; K = summ(grade("CL5_K4", C1["cf_table"], "0.034"), "canonical")
dk = max(abs(K["sparc"][t][q] - C1["canonical"]["sparc"][t][q]) for t in K["sparc"] for q in ("rms", "U")); RES["K4"] = dk == 0; P(f"K4 CE1 median table reproduces CE1's SPARC rms and Upsilon: max |d| {dk:.1e}: {'PASS' if dk == 0 else 'FAIL'}")
RES["runs"] = {}
for fs in ("0.034", "0.0615"):
    R = grade(f"CL5_B_fs{fs}", TB(21.2, 14.3, 14.3), fs); RES["runs"][fs] = {}
    for f in ("canonical", "alt"):
        s = summ(R, f); RES["runs"][fs][f] = s; ok = not s["failing"] and s["sparc_line"]
        P(f"  f* {fs} [{f}]: {'TARGET PASSES' if ok else 'TARGET BREAKS'}; SPARC {'PASS' if s['sparc_line'] else 'FAIL'} (U {s['sparc']['A_c2b_refit']['U']:.2f}/{s['sparc']['B_cfg886_bg']['U']:.2f}, rms {s['sparc']['A_c2b_refit']['rms']:.4f}); groups Z {s['groupsZ']:+.2f}, {s['verdict']}; failing: {s['failing']}")
json.dump(RES, open(os.path.join(HERE, "cl5_B_results.json"), "w"), indent=1, default=str); open(os.path.join(HERE, "cl5_B.out"), "w").write("\n".join(OUT) + "\n")
