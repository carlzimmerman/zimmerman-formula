#!/usr/bin/env python3
"""KL1R labels (FROZEN_CRITERIA.md 1792bd07ea section 3): reads parts/ (nu, gas, known, grade_*) and writes kl1r.json, kl1r.out.
Frozen reading first, the A1 reading beside it. kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); PT = os.path.join(HERE, "parts")
J = lambda n: json.load(open(os.path.join(PT, n)))
KN, GAS = J("known.json"), J("gas.json"); OUT = []
def P(s=""): print(s); OUT.append(s)
RANK = {"CONSISTENT": 0, "TENSION": 1, "EXCLUDED AT 3 SIGMA": 2}
NAME = {0: "AMPLITUDE CONSISTENT WITH RAW LENSING", 1: "TENSION", 2: "EXCLUDED"}
RES = dict(lane="KL1R", criteria="1792bd07ea", footings={}, note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
for ft in ("canonical", "alt"):
    NU = J(f"nu_{ft}.json"); g = {sv: J(f"grade_{sv}_{ft}.json") for sv in ("Legacy", "DES")}
    common = dict(KB1=KN["KB1"]["pass_"], KB2=KN["KB2"][ft]["pass_"], KA4=all(v["pass_"] for v in KN["KA4"].values()), KA1=bool(NU["KA1"]["i"]["pass_"] and NU["KA1"]["ii"]["pass_"]),
                  KA3=GAS["KA3"][ft]["pass_"], MA1=NU["MA1"]["bites"],
                  MA3=bool(GAS["MA3"][ft]["R_part_bites"] and g["Legacy"]["MUTATE"]["MA3_chi2"]["bites"]), MB1=g["Legacy"]["MUTATE"]["MB1_MP4"]["bites"])
    per = {}
    for sv in ("Legacy", "DES"):
        G = g[sv]; a = G["rows"]["ALL"]
        guards_frozen = dict(common, KA2=G["KA2"]["pass_"], MA2=G["MUTATE"]["MA2_halved"]["bites"], cov_pd=not a.get("not_pd", False))
        guards_A1 = dict(guards_frozen)
        if sv == "DES": guards_A1.pop("MA2"); guards_A1["MA2b"] = G["MUTATE"]["MA2b_doubled"]["bites"]
        lf = a["label"] if all(guards_frozen.values()) else "NO VERDICT"; la = a["label"] if all(guards_A1.values()) else "NO VERDICT"
        per[sv] = dict(ALL_label_raw=a["label"], p=a["p"], frozen=lf, A1=la, failed_guards_frozen=[k for k, v in guards_frozen.items() if not v],
                       failed_guards_A1=[k for k, v in guards_A1.items() if not v])
    def overall(key):
        ls = [per[sv][key] for sv in ("Legacy", "DES")]
        if "NO VERDICT" in ls: return "NO VERDICT"
        return NAME[max(RANK[x] for x in ls)]
    L = g["Legacy"]["rows"]
    against = dict(Legacy_ALL_tension_or_worse=L["ALL"]["label"] != "CONSISTENT", Legacy_gap_ALL_above_2=L["ALL"]["gap_widths"] > 2, Legacy_gap_X1_above_2=L["X1"]["gap_widths"] > 2,
                   MB1_not_biting=not common["MB1"])
    mb2 = g["Legacy"]["MUTATE"]["MB2"]
    RES["footings"][ft] = dict(frozen=overall("frozen"), A1=overall("A1"), per_survey=per, common_guards=common, counts_against=against, MB2_bites=mb2["bites"],
                               strict_MB2_reading=("NO VERDICT" if not mb2["bites"] else overall("frozen")), pinned_fit_flag=NU["flag_inadequate"])
    P(f"[{ft}] OVERALL Part B label: frozen {overall('frozen')}; under A1 {overall('A1')}")
    for sv in ("Legacy", "DES"):
        d = per[sv]; P(f"    {sv}: ALL p {d['p']:.3f} ({d['ALL_label_raw']}); frozen {d['frozen']} (failed guards {d['failed_guards_frozen']}); A1 {d['A1']} (failed {d['failed_guards_A1']})")
    P(f"    counts against form B: {against}; MB2 bites {mb2['bites']} (strict MB2 reading: {RES['footings'][ft]['strict_MB2_reading']}); neutrino-floor CMB cost {NU['cmb_cost']:+.2f} (flag {NU['flag_inadequate']})")
json.dump(RES, open(os.path.join(HERE, "kl1r.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1r.out"), "w").write("\n".join(OUT) + "\n")
