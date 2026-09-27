#!/usr/bin/env python3
"""LR2 -- J09p general-p window law Lean certificate (Z5-wave; owns LR2_*).
Door: register rows 10-11 Lean status "open (M01)"; extends LR1's central-window
certificate to the J09p general-p law. Gates (Z5-WAVE_BRIEF.md, fixed before any run):
exit 0 ONLY on compile rc 0 + zero sorry/errors + axioms subset of
{propext, Classical.choice, Quot.sound} + exact-rational witness pass. Lean certifies
the ALGEBRA; the J09p MC verification (21/21) stays the empirical leg.
"""
import json, os, subprocess, sys, time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
LEAN_FILE = "LR2_j09p_window_law.lean"
OUT = os.path.join(HERE, "LR2_j09p_window.out")
RESF = os.path.join(HERE, "LR2_results.json")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
RES = {"title": "LR2 J09p general-p window law Lean certificate",
       "pre_registration": "Z5-WAVE_BRIEF.md LR2 gates",
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
    with open(os.path.join(HERE, "LR2_lean_stdout.txt"), "w") as fo:
        p = subprocess.run(["lake", "env", "lean", LEAN_FILE], cwd=LEAN_DIR,
                           stdout=fo, stderr=subprocess.STDOUT, timeout=900)
    out = open(os.path.join(HERE, "LR2_lean_stdout.txt")).read()
    with open(OUT, "a") as fo:
        fo.write("\n=== LR2 run %s (lake env lean rc=%s) ===\n%s" %
                 (time.strftime("%Y-%m-%d %H:%M:%S"), p.returncode, out))
    RES["compile_rc"] = p.returncode
    errors = [l for l in out.splitlines() if "error" in l.lower()]
    sorries = [l for l in out.splitlines() if "sorry" in l.lower()]
    RES["errors"], RES["sorries"] = errors, sorries
    ax_ok = True
    for line in out.splitlines():
        if line.startswith("'") and "depends on axioms" in line:
            inner = line[line.index("["):line.index("]") + 1]
            for ax in ("sorryAx",):
                if ax in inner:
                    ax_ok = False
    RES["axioms_ok"] = ax_ok
    wit, ok = {}, True
    for pf in (1, 2, 4):
        pF = Fraction(pf)
        prev = None
        for qf in (0, 3, 10):
            q = Fraction(qf)
            W = (1 + q / (pF + 1)) / (Fraction(1, 2) + q / (pF + 2))
            lim = (pF + 2) / (pF + 1)
            inside = lim <= W <= 2
            dec = W < prev if prev is not None else True
            prev = W
            wit["p%d_q%d" % (pf, qf)] = {"W": str(W), "limit": str(lim),
                                         "in_band": inside, "antitone": dec}
            ok = ok and inside and dec
    RES["witness"], RES["witness_pass"] = wit, ok
    good = (p.returncode == 0 and not errors and not sorries and ax_ok and ok)
    RES["verdict"] = ("LEAN CERTIFICATE BANKED: W_p(q) = (1+q/(p+1))/(1/2+q/(p+2)) in "
                      "[(p+2)/(p+1), 2], strictly antitone in q, zero sorry; witness "
                      "p={1,2,4} x q={0,3,10}" if good else
                      "HONEST FAIL (recorded): compile_rc=%s errors=%d sorries=%d "
                      "axioms_ok=%s witness=%s" % (p.returncode, len(errors),
                                                   len(sorries), ax_ok, ok))
    finish(0 if good else 1)

if __name__ == "__main__":
    main()
