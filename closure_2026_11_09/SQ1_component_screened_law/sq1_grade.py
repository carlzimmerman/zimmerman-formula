#!/usr/bin/env python3
"""SQ1 grader (FROZEN_CRITERIA.md 7e8fa69c63): label per footing in the frozen order Q1, Q-KiDS, Q-SPARC, Q-groups, Q-X-COP, Q2, Q-web,
Q5 Bullet (Q3, Q4 reported; Cassini carried). Reading G graded; C reported. kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(HERE, "sq1.json"))); out = {}; L = []
for f in ("canonical", "alt"):
    r = R[f]; cg = json.load(open(os.path.join(HERE, "parts", f"cosmo_SQG_{f}.json"))); cc = json.load(open(os.path.join(HERE, "parts", f"cosmo_SQC_{f}.json")))
    web = "PASS" if all(cg[k]["status"] == "PASS" for k in ("G7bL", "G8", "CS")) else "FAIL"
    st = {"Q1 depletion dynamics": r["Q1"]["status"], "Q-KiDS (G)": r["KiDS"]["G"]["status"], "Q-SPARC (G)": r["SPARC"]["G"]["status"], "Q-groups": r["groups"]["status"], "Q-X-COP": r["XCOP"]["status"],
          "Q2 volume filling (C)": r["Q2"]["status"], "Q-web (G)": web, "Q5 Bullet": r["Bullet"]["status"], "Cassini (carried)": "PASS"}
    fails = [k for k, v in st.items() if v != "PASS"]
    out[f] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None,
                  web_G=dict(lensing=cg["G7bL"]["chi2"], forest=cg["G8"]["forest"]["dchi2"], fs8=[x["Rf"] for x in cg["G8"]["fsigma8"]["rows"]], S8=cg["CS"]["change"]),
                  web_C_reported=dict(lensing=cc["G7bL"]["chi2"], fs8=[x["Rf"] for x in cc["G8"]["fsigma8"]["rows"]], S8=cc["CS"]["change"], status="PASS" if all(cc[k]["status"] == "PASS" for k in ("G7bL", "G8", "CS")) else "FAIL"))
    L.append(f"[{f}] SQ1 LABEL {out[f]['label']}; first failing gate {out[f]['first_fail']}; " + ", ".join(f"{k} {v}" for k, v in st.items()))
print("\n".join(L)); open(os.path.join(HERE, "sq1_grade.out"), "w").write("\n".join(L) + "\n"); json.dump(out, open(os.path.join(HERE, "sq1_grade.json"), "w"), indent=1)
