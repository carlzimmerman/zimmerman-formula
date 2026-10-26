#!/usr/bin/env python3
"""X48 regrade (FROZEN_CRITERIA section 3): X43's rule with eta(M) = (4/(3 B(1))) c_f(M)^(5/4) from the native c_f table
(x48_analyze_results.json; interpolated in lg M between measured masses, held flat outside). Writes x48_regrade[_TAG].out/json.

    python3 x48_regrade.py [--tag PROVISIONAL]
"""
import argparse, contextlib, io, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
ap = argparse.ArgumentParser(); ap.add_argument("--tag", default=""); ap.add_argument("--analysis", default="x48_analyze_results.json"); a = ap.parse_args(); TAG = f"_{a.tag}" if a.tag else ""
A = json.load(open(os.path.join(HERE, a.analysis)))
tab = {float(k): v for k, v in A["cf_by_mass"].items() if v is not None}
LM = np.array(sorted(math.log10(m) for m in tab)); CF = np.array([tab[10 ** l] if 10 ** l in tab else tab[min(tab, key=lambda m: abs(math.log10(m) - l))] for l in LM])
B1 = 3 * math.log(2) - math.pi / 2
def cf_of(M): return float(np.interp(math.log10(M), LM, CF))
def eta_of(M): return 4.0 / (3.0 * B1) * cf_of(M) ** 1.25
src = open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")).read()
old = 'sc = ETA_USE["v"] * sigma_coll(tag, M)[0] * MSUNE / PC2'; assert src.count(old) == 1
src = src.replace(old, 'sc = (ETA_FUN(M) if (ETA_FUN is not None and ETA_USE["v"] == ETA) else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2')
src = src.replace('f"x43_collapse_core{TAG}.out"', f'"x48_regrade_x43copy{TAG}.out"').replace('f"x43_collapse_core_results{TAG}.json"', f'"x48_regrade_x43copy{TAG}_results.json"')
src = src.replace('"x43_x30_machinery"', '"x48_x30_machinery"').replace("sys.exit(0 if n == len(checks) else 1)", "pass")
ns = {"__file__": os.path.join(HERE, "x43_copy.py"), "__name__": "x43_copy", "ETA_FUN": eta_of}
sys.argv = [ns["__file__"]]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(src, ns["__file__"], "exec"), ns)
R = ns["RES"]; OUT = [f"X48 regrade{(' [' + a.tag + ']') if a.tag else ''}: X43 rule with native c_f table {dict(zip([f'1e{l:.0f}' for l in LM], [round(c, 3) for c in CF]))} (flat outside)"]
OUT.append("eta at 1e12/1e13/1e14/1e15: " + ", ".join(f"{eta_of(10 ** l):.2f}" for l in (12, 13, 14, 15)) + "   (X43 constant 14.83)")
res = {}
for f in ("canonical", "alt"):
    F = R["footings"][f]; c0 = F["clusters"]["cells"]["h0672"]; sp = F["sparc"]["A_c2b_refit"]; gr = F["groups"]
    v = "NATIVE-CC PASSES" if not F["failing"] else "NATIVE-CC FAILS: " + ", ".join(F["failing"])
    res[f] = dict(verdict=v, sparc=dict(rms=sp["rms"], U=sp["U_median"], line=sp["line"]), groups=dict(Z=gr["Z"], verdict=gr["verdict"]),
                  keys={k: dict(pred=c0[k]["pred"], meas=c0[k]["meas"], Z=c0[k]["Z"]) for k in c0})
    OUT.append(f"[{f}] SPARC {sp['rms']:.4f}@{sp['U_median']:.2f} line {'PASS' if sp['line'] else 'FAIL'}; groups Z {gr['Z']:+.2f} {gr['verdict']}")
    OUT.append("   " + "; ".join(f"{k} {c0[k]['pred']:.2f}/{c0[k]['meas']:.2f} Z {c0[k]['Z']:+.2f}" for k in ("G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-M3", "G-IN-all")))
    OUT.append(f"   VERDICT [{f}]: {v}")
print("\n".join(OUT))
open(os.path.join(HERE, f"x48_regrade{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(table=dict(lgM=LM.tolist(), cf=CF.tolist()), footings=res), open(os.path.join(HERE, f"x48_regrade{TAG}.json"), "w"), indent=1, default=float)
try: os.remove(os.path.join(HERE, "x43_copy.py"))
except OSError: pass
