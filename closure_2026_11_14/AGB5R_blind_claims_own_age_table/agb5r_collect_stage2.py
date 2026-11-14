"""AGB5R collector, stage 2 (AGB5 amendment 1): K1, KA, K3 as in stage 1; K4 amended; L1 on bootstrap errors.
Writes agb5r_results_stage2.json and agb5r_collect_stage2.out. Stage 1 files are not touched."""
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s)


def load(n):
    with open(os.path.join(HERE, n + ".json")) as f:
        return json.load(f)


K1, KA, K3, K4, L1 = (load("agb5r_" + m) for m in ("K1", "KA", "K3", "K4", "L1"))
K4B, LB = load("agb5r_K4_boot"), load("agb5r_L_boot")
checks = {"K1": K1["pass"], "KA": KA["pass"], "K3": K3["pass"], "K4 (amended)": K4B["pass"]}
say("== AGB5R stage 2 (AGB5 amendment 1: bootstrap errors, amended K4) ==")
for k, v in checks.items():
    say("check %s: %s" % (k, "PASS" if v else "FAIL"))
say("  (frozen K4, stage 1: %s)" % ("PASS" if K4["pass"] else "FAIL"))
for nm in ("t1", "t2"):
    r = K4B[nm]
    say("  K4 amended %s: bootstrap sd %.3f x stated [%s]; shuffle with signal removed sd %.3f x stated [%s] (mean %+.3f)" % (
        nm, r["boot_sd_over_sA"], r["pass_boot"], r["shuffle_removed_sd_over_sA"], r["pass_shuffle_removed"],
        r["shuffle_removed_mean_over_sA"]))
failed = [k for k, v in checks.items() if not v]
order = ["primary", "table1_alone", "table2_alone", "shared_dropped_t1", "t1_original_resid", "redshift_term", "structural"]
say("")
say("Per-table fits: stated error -> bootstrap error (seed 20261119, 400 resamples)")
for k, f in LB["fits"].items():
    say("  %-11s A %+.4f  %.4f -> %.4f (x %.3f)" % (k, f["A"], f["sA_stated"], f["sA_boot"], f["sA_boot"] / f["sA_stated"]))
say("")
say("L1 rows, stage 1 (stated errors) | stage 2 (bootstrap errors):")
for k in order:
    a, b = L1[k], LB[k]
    say("  %-18s A %+.4f +- %.4f d0 %6.2f d1 %5.2f %-28s | A %+.4f +- %.4f d0 %6.2f d1 %5.2f %s" % (
        k, a["A"], a["sA"], a["dchi2_A0"], a["dchi2_A1"], a["word"], b["A"], b["sA"], b["dchi2_A0"], b["dchi2_A1"], b["word"]))
reading = "%s / %s" % (LB["first_word"], LB["second_word"])
word = ("NOT EVALUABLE (failed: %s)" % ", ".join(failed)) if failed else reading
say("")
say("L1 WORD (amendment 1): %s (amendment 1)" % word)
say("L1 WORD (as frozen, stage 1): NOT EVALUABLE (failed: K4)" if not K4["pass"] else "")
res = dict(checks=checks, failed=failed, L1_word_amendment1=word + " (amendment 1)", L1_amendment1=LB, K4_amended=K4B)
with open(os.path.join(HERE, "agb5r_results_stage2.json"), "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
with open(os.path.join(HERE, "agb5r_collect_stage2.out"), "w") as f:
    f.write("\n".join(LINES) + "\n")
