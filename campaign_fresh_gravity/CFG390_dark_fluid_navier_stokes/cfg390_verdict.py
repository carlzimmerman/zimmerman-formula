"""CFG390 verdict from parts A and B (run cfg390_symbolic.py and cfg390_spherical.py first; same CFG390_MUTATE setting).
Frozen rule (FROZEN_CRITERIA.md section 5). Exit 0 only for the main run with every control passing as declared."""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG390_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
A = json.load(open(os.path.join(HERE, f"cfg390_symbolic_results{TAG}.json")))
B = json.load(open(os.path.join(HERE, f"cfg390_spherical_results{TAG}.json")))
ra, rb = A["results"], B["results"]
lines = []
def say(s=""): print(s); lines.append(s)
cons = ra["A1"] and ra["A2a"] and ra["A2"] and ra["A4"]
a_all = cons and ra["A3"] and ra["A5"]
mw = all(rb["MW_recovered"].values()); cl = all(rb["cluster_u500_ok"].values())
if not cons:
    v = "INCONSISTENT"
elif a_all and mw and cl:
    v = "CONSISTENT-AND-REPRODUCES"
else:
    v = "PARTIAL"
say("CFG390 verdict" + ("  (MUTATE: kappa_s = 0)" if MUTATE else ""))
say(f"  A1 mass {ra['A1']}; A2 exchange {ra['A2a']}, momentum up to declared sink {ra['A2']} (sink required {ra['sink_required']}); "
    f"A3 Galilean {ra['A3']}; A4 H-theorem {ra['A4']}; A5 rest state stationary {ra['A5']}")
say(f"  A1b proposed C anti-relaxes (fixed by R1): {ra['A1b_proposed_C_antirelaxes']}; A4b relaxation-time C violates H: {ra['A4b_relaxation_time_C_violates_H']}")
for f in ("canonical", "alt"):
    m, c = rb[f]["MW_primary"], rb[f]["cluster_primary"]
    say(f"  [{f}] MW primary: max|V/V_law - 1| = {m['max_dev']:.3f} (recovered {m['recovered']}); cluster primary u500 = {c['u500']:.3f}")
say(f"VERDICT: {v}")
ctrl = [c for c in A["checks"] + B["checks"] if not c["name"].startswith("A5 ")]
bad = [c["name"] for c in ctrl if not c["pass"]]
say(f"  controls/checks failing (excluding the scored A5 item): {bad if bad else 'none'}")
json.dump({"lane": "CFG390", "mutate": MUTATE, "verdict": v, "failing": bad}, open(os.path.join(HERE, f"cfg390_verdict{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg390_verdict{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(1 if (MUTATE or bad) else 0)
