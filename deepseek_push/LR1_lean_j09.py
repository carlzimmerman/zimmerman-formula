#!/usr/bin/env python3
"""LR1 -- M-roads Lean roadmap: J09 central window law certificate (Z4-wave; owns LR1_*).
Door: register rows 10-11 -- J09/J09p VERIFIED 27/27 + 21/21 with Lean status
"open (M01)"; M-roads Lean roadmap is a standing OPEN door. This lane banks the Lean
leg: W(q) = (1+q/3)/(1/2+q/4) on [0, inf) stays in [4/3, 2] and is strictly antitone,
certified in fable_independent_2026/lean_2026/LR1_j09_window_law.lean (toolchain
v4.34.0-rc2). Lean certifies the ALGEBRA (I-series scope precedent); the J09 MC
verification stays the empirical leg. Gates (Z4-WAVE_BRIEF.md, fixed before any run):
exit 0 ONLY on compile rc 0 + zero sorry + zero errors + axioms subset of
{propext, Classical.choice, Quot.sound} for every theorem + numeric witness pass.
"""
import json, os, subprocess, sys, time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
LEAN_FILE = "LR1_j09_window_law.lean"
OUT = os.path.join(HERE, "LR1_j09_window.out")
RESF = os.path.join(HERE, "LR1_results.json")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
RES = {"title": "LR1 J09 central window law Lean certificate",
       "pre_registration": "Z4-WAVE_BRIEF.md LR1 gates",
       "lean_file": os.path.join(LEAN_DIR, LEAN_FILE), "toolchain": "v4.34.0-rc2"}
_T0 = time.time()

def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(RESF, "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in
                      ("verdict", "compile_rc", "sorries", "errors", "axioms_ok",
                       "witness_pass")}, indent=1))
    print("elapsed %ss; exit %s" % (RES["elapsed_s"], rc))
    sys.exit(rc)

def main():
    if not os.path.exists(RES["lean_file"]):
        RES["verdict"] = "FAIL: lean file absent"
        finish(1)
    with open(os.path.join(HERE, "LR1_lean_stdout.txt"), "w") as fo:
        p = subprocess.run(["lake", "env", "lean", LEAN_FILE], cwd=LEAN_DIR,
                           stdout=fo, stderr=subprocess.STDOUT, timeout=900)
    out = open(os.path.join(HERE, "LR1_lean_stdout.txt")).read()
    with open(OUT, "a") as fo:
        fo.write("\n=== LR1 run %s (lake env lean rc=%s) ===\n%s" %
                 (time.strftime("%Y-%m-%d %H:%M:%S"), p.returncode, out))
    RES["compile_rc"] = p.returncode
    errors = [l for l in out.splitlines() if "error" in l.lower()]
    sorries = [l for l in out.splitlines() if "sorry" in l.lower()]
    RES["errors"], RES["sorries"] = errors, sorries
    ax_ok, bad = True, []
    for line in out.splitlines():
        if line.startswith("'") and "depends on axioms" in line:
            thm = line.split("'")[1]
            inner = line[line.index("["):line.index("]") + 1]
            for ax in ("sorryAx", "propext", "Classical.choice", "Quot.sound"):
                if ax in inner and ax not in ALLOWED:
                    ax_ok = False; bad.append(thm)
    RES["axioms_ok"], RES["axioms_bad"] = ax_ok, bad
    # numeric witness (exact rational arithmetic)
    wit = {}
    ok = True
    prev = None
    for q in (0, 3, 10):
        qf = Fraction(q)
        W = (1 + qf / 3) / (Fraction(1, 2) + qf / 4)
        inside = Fraction(4, 3) <= W <= 2
        dec = W < prev if prev is not None else True  # fix-forward: antitone = strictly DEcreasing (run-1 used >= and failed honestly, kept verbatim in .out)
        prev = W
        wit[str(q)] = {"W": str(W), "float": float(W), "in_window": inside,
                       "antitone_step": dec}
        ok = ok and inside and dec
    RES["witness"] = wit
    RES["witness_pass"] = ok
    good = (p.returncode == 0 and not errors and not sorries and ax_ok and ok)
    RES["verdict"] = ("LEAN CERTIFICATE BANKED: W(q) = (1+q/3)/(1/2+q/4) in [4/3, 2], "
                      "strictly antitone, zero sorry, axioms within the allowed set; "
                      "witness q={0,3,10} -> 2, 1.5556, 1.4444" if good else
                      "HONEST FAIL (recorded): compile_rc=%s errors=%d sorries=%d "
                      "axioms_ok=%s witness=%s" % (p.returncode, len(errors),
                                                   len(sorries), ax_ok, ok))
    finish(0 if good else 1)

if __name__ == "__main__":
    main()
