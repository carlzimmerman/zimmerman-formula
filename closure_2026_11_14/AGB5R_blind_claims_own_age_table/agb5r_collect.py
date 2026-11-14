"""AGB5R collector, stage 1 (as frozen): applies the checks and the word L1. Writes agb5r_results.json, agb5r_collect.out."""
import os
import sys
import json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb5r_fit as F  # noqa: E402

LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s)


def load(m):
    with open(os.path.join(HERE, "agb5r_%s.json" % m)) as f:
        return json.load(f)


K1, KA, K3, K4, L1, REP, PP = (load(m) for m in ("K1", "KA", "K3", "K4", "L1", "REP", "PP"))
checks = {"K1": K1["pass"], "KA": KA["pass"], "K3": K3["pass"], "K4": K4["pass"]}
say("== AGB5R stage 1 (as frozen) ==")
for k, v in checks.items():
    say("check %s: %s" % (k, "PASS" if v else "FAIL"))
for nm in ("t1", "t2"):
    r = K4[nm]
    say("  K4 %s: shuffle mean %+.3f sA [%s], shuffle sd %.3f sA [%s], bootstrap sd %.3f sA [%s]" % (
        nm, r["shuffle_mean_over_sA"], r["pass_shuffle_mean"], r["shuffle_sd_over_sA"], r["pass_shuffle_sd"],
        r["boot_sd_over_sA"], r["pass_boot"]))
failed = [k for k, v in checks.items() if not v]
order = ["primary", "table1_alone", "table2_alone", "shared_dropped_t1", "t1_original_resid", "redshift_term", "structural"]
say("")
say("L1 rows (plain line, mass step free; the structural row uses the curvature error):")
for k in order:
    r = L1[k]
    say("  %-18s A = %+.4f +- %.4f  dchi2(A=0) %6.2f  dchi2(A=1) %6.2f  %s" % (k, r["A"], r["sA"], r["dchi2_A0"], r["dchi2_A1"], r["word"]))
reading = "%s / %s" % (L1["first_word"], L1["second_word"])
word = "NOT EVALUABLE (failed: %s)" % ", ".join(failed) if failed else reading
say("")
say("L1 WORD (as frozen): %s" % word)
if failed:
    say("L1 reading (numbers only, no word): %s" % reading)

# reading only: the same rows with each table's error scaled by sqrt(chi2/dof)
say("")
say("Reading only, not a word: plain rows with each table's sA scaled by sqrt(chi2/dof)")
scaled = {}
for k in order[:-1]:
    parts = L1[k]["parts"]
    c = F.combine([dict(A=p["A"], sA=p["sA_scaled"]) for p in parts])
    w, d0, d1 = F.w1_word(c["A"], c["sA"])
    scaled[k] = dict(A=c["A"], sA=c["sA"], dchi2_A0=d0, dchi2_A1=d1, word=w)
    say("  %-18s A = %+.4f +- %.4f  dchi2(A=0) %6.2f  dchi2(A=1) %6.2f  %s" % (k, c["A"], c["sA"], d0, d1, w))

# reported rows
say("")
say("Reported: plain, no step, combined on all rows (L0 / KA): A = %+.4f +- %.4f" % (KA["plain_comb"]["A"], KA["plain_comb"]["sA"]))
ns = F.combine([REP["t1_nostep_stepsample"], REP["t2_nostep_stepsample"]])
say("Reported: plain, no step, combined on the step sample: A = %+.4f +- %.4f" % (ns["A"], ns["sA"]))
for nm in ("t1", "t2", "t1orig"):
    s = REP[nm + "_step"]
    say("Reported: %s step g without age %+.4f +- %.4f, with age %+.4f +- %.4f" % (nm, s["g_no_age"], s["s_g_no_age"], s["g_with_age"], s["s_g_with_age"]))
    for Lv in (0, 1):
        r = REP["%s_inside_L%d" % (nm, Lv)]
        say("Reported: %s slope inside L=%d (n %d): A = %+.4f +- %.4f" % (nm, Lv, r["n"], r["A"], r["sA"]))
for sc in ("1.0", "0.5", "0.0"):
    for st in (0, 1):
        r = REP["struct_comb_scale%s_step%d" % (sc, st)]
        say("Reported: structural combined, sig_age x %s, step %d: A = %+.4f +- %.4f dchi2(0) %.2f dchi2(1) %.2f [%s]" % (
            sc, st, r["A"], r["sA"], r["dchi2_A0"], r["dchi2_A1"], r["word"]))
for k in ("union_t1age", "union_t2age", "t1_hosts", "t2_hosts"):
    for st in (0, 1):
        r = PP["%s_step%d" % (k, st)]
        say("Reported: Pantheon+ %-12s step %d n %d: A = %+.4f +- %.4f dchi2(0) %.2f dchi2(1) %.2f [%s]" % (
            k, st, r["n"], r["A"], r["sA"], r["dchi2_A0"], r["dchi2_A1"], r["word"]))

res = dict(checks=checks, failed=failed, L1_word=word, L1_reading=reading, L1=L1, scaled_reading=scaled,
           plain_nostep_comb_all=KA["plain_comb"], plain_nostep_comb_stepsample=ns)
with open(os.path.join(HERE, "agb5r_results.json"), "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
with open(os.path.join(HERE, "agb5r_collect.out"), "w") as f:
    f.write("\n".join(LINES) + "\n")
