"""EDG1 grader (criteria f57da1f35c, section 3). Usage: python3 edg1_grade.py [_MUTATE_MUn]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1] if len(sys.argv) > 1 else ""
R = json.load(open(os.path.join(HERE, f"edg1{tag}.json")))
OUT, G = [], {}
def say(s): print(s); OUT.append(s)
kas = {k: R[k]["pass_"] for k in ("KA1", "KA2", "KA3", "KA4")}
say(f"known answers: {kas}")
for foot, rows in R["F"].items():
    G[foot] = {}
    for rd in ("R5", "U"):
        if not all(kas.values()):
            lab = "NO VERDICT"
        else:
            e0 = R["E0"]["PASS"]
            e1 = all(rows[m][rd]["E1_pass"] for m in rows)
            # E2: (a) unstable (c_s^2 < 0), (b) no equilibrium (KA3), (d) no equilibrium (exact); (c) per mass
            e2c = all(rows[m][rd]["E2c"]["pass"] for m in rows)
            e2 = e2c or (R["E2b"]["equilibrium"] != "NONE")
            e3 = e2c and all(rows[m][rd]["E3"]["pass_"] for m in rows)
            lab = ("FAILS AT E0" if not e0 else "FAILS AT E1" if not e1 else "FAILS AT E2" if not e2
                   else "FAILS AT E3" if not e3 else "BRANCH LIVES AT STRUCTURE")
            G[foot][rd + "_gates"] = dict(E0=e0, E1=e1, E2=e2, E2c=e2c, E3=e3)
        G[foot][rd] = lab
        say(f"{foot} reading {rd}{' (graded)' if rd == 'R5' else ' (reported)'}: {lab}  {G[foot].get(rd + '_gates', '')}")
json.dump(G, open(os.path.join(HERE, f"edg1_grade{tag}.json"), "w"), indent=1)
open(os.path.join(HERE, f"edg1_grade{tag}.out"), "w").write("\n".join(OUT) + "\n")
