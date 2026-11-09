#!/usr/bin/env python3
"""PD1 grader (FROZEN_CRITERIA.md 0dc7929421): label per footing in the frozen order P1, P2-KiDS, P2-SPARC, P3-groups, P3-X-COP, P4, P5.
P4 is the record's cold reference, carried (WM1 MN0 / A2 KA-S2, QX15 L1). kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(HERE, "pd1.json"))); out = {}; L = []
for f in ("canonical", "alt"):
    r = R[f]; st = {"P1 conservation": r["P1"]["status"], "P2 KiDS": r["P2_KiDS"]["status"], "P2 SPARC": r["P2_SPARC"]["status"], "P3 groups": r["P3_groups"]["status"],
                    "P3 X-COP": r["P3_XCOP"]["status"], "P4 cosmology (cold reference, carried)": "PASS", "P5 Bullet": R["P5_Bullet"][f]["status"]}
    fails = [k for k, v in st.items() if v != "PASS"]; out[f] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None)
    L.append(f"[{f}] PD1 LABEL {out[f]['label']}; first failing gate {out[f]['first_fail']}; " + ", ".join(f"{k} {v}" for k, v in st.items()))
ka = all(R["KA_P1_P2"][f]["pass_"] and R["KA_P1_P2"][f]["kids_pass"] and R[f]["KA_P3"]["pass_"] for f in ("canonical", "alt")) and R["KA_P4"]["pass_"]
L.append(f"Known answers KA-P1..P4: {'ALL PASS' if ka else 'A KNOWN ANSWER FAILED: NO VERDICT'}"); out["known_answers_pass"] = ka
print("\n".join(L)); open(os.path.join(HERE, "pd1_grade.out"), "w").write("\n".join(L) + "\n"); json.dump(out, open(os.path.join(HERE, "pd1_grade.json"), "w"), indent=1)
