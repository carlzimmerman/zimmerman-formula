#!/usr/bin/env python3
"""A2 - atlas sufficiency for the volume-branch U-OUT door (V03c-derived).
Pre-registration: deepseek_push/Z2-WAVE_BRIEF.md (K1/K2/K3 fixed before any number).
Loaded inputs: V03b_trio_results.json (V03c 72-cell locked rerun, cells + decision tree),
N04_raw_cells.json (N04-record atlas raw cells). Matched-config z of dU = U_v03 - U_n04,
sigma = sqrt(se_U_block_v03^2 + se_U_block_n04^2) (independent MC runs).
Branches: K1 any |z|>=3 -> ATLAS-CONTESTED configs listed; K2 all |z|<3 -> ATLAS-RULE-ARTEFACT;
K3 disputed configs share one sign -> ATLAS-SHIFT. Missing field -> honest exit 1.
"""
import json, sys, math

V3 = "V03b_trio_results.json"
N4 = "N04_raw_cells.json"
RES = {"title": "A2 atlas sufficiency for the volume-branch U-OUT door",
       "inputs": [V3, N4], "pre_registration": "Z2-WAVE_BRIEF.md K1/K2/K3"}

def main():
    v3 = json.load(open(V3))
    n4 = json.load(open(N4))
    cells = v3["cells"]
    rows = v3["decision_tree"]["rows"]
    per_tag = []
    for r in rows:
        tag = r["tag"]
        if not tag.startswith("vt"):
            continue
        c = cells.get(tag)
        if c is None:
            RES["error"] = "missing V03 cell %s" % tag
            return 1
        n4tag = tag.replace("is", "iso") if tag.endswith("is") else tag
        a = n4.get(n4tag)
        if a is None:
            RES["error"] = "missing N04 atlas cell %s" % n4tag
            return 1
        u3, u4 = c["U"], a["U"]
        s3 = c.get("se_U_block", c.get("se_U"))
        s4 = a.get("se_U_block", a.get("se_U"))
        if s3 is None or s4 is None:
            RES["error"] = "missing se_U for %s" % tag
            return 1
        sig = math.sqrt(s3*s3 + s4*s4)
        z = (u3 - u4) / sig
        per_tag.append({"tag": tag, "n4_tag": n4tag, "tree": r["tree"],
                        "U_v03": u3, "U_n04": u4, "dU": u3-u4, "z_U": z,
                        "se_v03": s3, "se_n04": s4})
    contested = [p for p in per_tag if abs(p["z_U"]) >= 3.0]
    if contested:
        signs = set("+" if p["dU"] > 0 else "-" for p in contested)
        verdict = "ATLAS-SHIFT" if len(signs) == 1 and len(contested) < len(per_tag) else "ATLAS-CONTESTED"
        if len(signs) == 1 and len(contested) >= len(per_tag):
            verdict = "ATLAS-CONTESTED-SIGNED"
    else:
        verdict = "ATLAS-RULE-ARTEFACT"
    RES["per_tag"] = per_tag
    RES["n_volume_tags"] = len(per_tag)
    RES["contested"] = [p["tag"] for p in contested]
    RES["max_abs_z"] = max(abs(p["z_U"]) for p in per_tag)
    RES["verdict"] = verdict
    print(json.dumps(RES, indent=1))
    open("A2_atlas_sufficiency.json", "w").write(json.dumps(RES, indent=1))
    print("A2 COMPLETE verdict=%s contested=%d/%d max|z|=%.4f"
          % (verdict, len(contested), len(per_tag), RES["max_abs_z"]))
    return 0

if __name__ == "__main__":
    rc = main()
    print("EXIT %d" % rc)
    sys.exit(rc)
