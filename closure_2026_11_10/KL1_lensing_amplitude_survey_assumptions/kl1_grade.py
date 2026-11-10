#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef) grading: the frozen label rule (section 6) on parts/rows_<footing>.json, with every known
answer and MUTATE arm gathered. Per data set = the ALL row's label by CO2's lines; overall = the worse of KiDS-1000 and DES Y3;
NO VERDICT if a known answer guarding ALL fails or a MUTATE arm does not bite. Part A only: KiDS-1000 and DES Y3.

  python3 kl1_grade.py     -> kl1.json, kl1.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
J = {ft: json.load(open(os.path.join(HERE, "parts", f"rows_{ft}.json"))) for ft in FOOTS}
JM = {ft: json.load(open(os.path.join(HERE, "parts", f"rows_{ft}_MUTATE.json"))) for ft in FOOTS}
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); NUM = json.load(open(os.path.join(HERE, "kl1_nu_MUTATE.json")))
GAS = json.load(open(os.path.join(HERE, "kl1_gas.json"))); GASM = json.load(open(os.path.join(HERE, "kl1_gas_MUTATE.json")))
FIT = {ft: json.load(open(os.path.join(HERE, "parts", f"fit_nu_{ft}.json"))) for ft in FOOTS}
RANK = {"CONSISTENT": 0, "TENSION": 1, "EXCLUDED AT 3 SIGMA": 2}
OVR = {"CONSISTENT": "AMPLITUDE CONSISTENT WITH RAW LENSING", "TENSION": "TENSION", "EXCLUDED AT 3 SIGMA": "EXCLUDED", "NO VERDICT": "NO VERDICT"}
TAIL = "for form B with the neutrino floor, its own layout with RB1's gas, the covariance at the model; gravity-only S0 box; inherited halo list"
RES = dict(lane="KL1", criteria="99a42c78ef", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", scope="Part A: KiDS-1000 and DES Y3 only (Part B, KiDS-Legacy, waits on the owner's go)",
           KA={}, MUTATE={}, labels={}, rows={})
for ft in FOOTS:
    j, jm = J[ft], JM[ft]
    ka = dict(KA0=j["KA"]["KA0"]["pass_"], KA1_i=FIT[ft]["KA1_i"]["pass_"], KA1_ii=NU["KA"][ft]["pass_"], KA2_KiDS=j["KA"]["KA2"]["KiDS"]["pass_"],
              KA2_DES=j["KA"]["KA2"]["DES"]["pass_"], KA3=bool(GAS["KA"][ft]["KA3_i_pass"] and GAS["KA"][ft]["KA3_ii_pass"] and GAS["KA"][ft]["KA3_iii_pass"]), KA4=j["KA"]["KA4"]["pass_"])
    mu = dict(MA1=NUM["rows"][ft]["bites"], MA2_KiDS=jm["MUTATE"]["MA2"]["KiDS"]["bites"], MA2_DES=jm["MUTATE"]["MA2"]["DES"]["bites"],
              MA3=bool(GASM["rows"][ft]["bites_R"] and jm["MUTATE"]["MA3_chi2"]["bites"]), MP4=jm["MUTATE"]["MP4"]["KiDS"]["bites"])
    RES["KA"][ft] = ka; RES["MUTATE"][ft] = mu
    MA2B = json.load(open(os.path.join(HERE, "parts", "ma2b_MUTATE.json")))["rows"][ft]
    mu["MA2b_KiDS"] = MA2B["KiDS"]["bites"]; mu["MA2b_DES"] = MA2B["DES"]["bites"]
    def labels_for(reading):
        lab = {}
        for sn in ("KiDS", "DES"):
            ma2 = mu[f"MA2_{sn}"] if (reading == "frozen" or sn == "KiDS") else mu["MA2b_DES"]     # AMENDMENT A1 (post hoc): DES read by MA2b
            ok = all(ka[k] for k in ("KA0", "KA1_i", "KA1_ii", f"KA2_{sn}", "KA3", "KA4")) and ma2 and all(mu[k] for k in ("MA1", "MA3", "MP4"))
            a = j["rows"]["ALL"][sn]["at_target"]; lab[sn] = a["label"] if ok and not a.get("not_pd") else "NO VERDICT"
        worst = "NO VERDICT" if "NO VERDICT" in lab.values() else max(lab.values(), key=lambda x: RANK[x])
        return dict(KiDS_1000=lab["KiDS"], DES_Y3=lab["DES"], overall=OVR[worst], carries=TAIL, scope="KiDS-1000 and DES Y3 only")
    RES["labels"][ft] = dict(frozen=labels_for("frozen"), A1_post_hoc=labels_for("A1"))
    RES["rows"][ft] = {name: {sn: {k: v for k, v in o.items() if k in ("N", "target_sigma8", "label", "best_sigma8", "width", "gap_widths", "dchi2_target_vs_best", "with_logdet", "na")}
                              | ({"chi2": o["at_target"]["chi2"], "chi2_data": o["at_target"]["chi2_data"], "p": o["at_target"]["p"], "A_IA": o["at_target"]["A_IA"],
                                  "dz_pulls": o["at_target"].get("dz_pulls"), "eta": o["at_target"].get("eta"),
                                  "best_p": o.get("best", {}).get("p"), "best_dz_pulls": o.get("best", {}).get("dz_pulls")} if "at_target" in o else {})
                              for sn, o in r.items()} for name, r in j["rows"].items()}
P("KL1 Part A: which survey and comparison assumptions carry form B's weak-lensing amplitude gap. kappa = 1/2 FITTED; not theory closed.")
P("Part A scope: KiDS-1000 and DES Y3 as on disk. Part B (KiDS-Legacy, fetched on the owner's go) follows below.\n")
for ft in FOOTS:
    for rd in ("frozen", "A1_post_hoc"):
        L = RES["labels"][ft][rd]; P(f"[{ft}] PART A LABEL ({'as frozen' if rd == 'frozen' else 'under AMENDMENT A1, post hoc'}): KiDS-1000 {L['KiDS_1000']}; DES Y3 {L['DES_Y3']}; overall {L['overall']} ({L['scope']}; {TAIL})")
    P(f"  known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in RES["KA"][ft].items()) + ";  MUTATE: " + ", ".join(f"{k} {'bites' if v else 'DOES NOT BITE'}" for k, v in RES["MUTATE"][ft].items()))
P("")
names = list(J["canonical"]["rows"].keys())
for sn in ("KiDS", "DES"):
    P(f"{'KiDS-1000' if sn == 'KiDS' else 'DES Y3'} (canonical | alt): target sigma8, chi2, p, label; best sigma8 +- width, gap in widths")
    for name in names:
        cells = []
        for ft in FOOTS:
            o = RES["rows"][ft][name][sn]
            if "na" in o: cells.append("n/a"); continue
            c = f"{o['target_sigma8']:.4f} chi2 {o['chi2']:.2f} p {o['p']:.4f} {o['label']}"
            if o.get("best_sigma8") is not None: c += f"; best {o['best_sigma8']:.4f}+-{o['width']:.4f} gap {o['gap_widths']:+.2f}"
            if o.get("with_logdet"): c += f" (ln det: gap {o['with_logdet']['gap_widths']:+.2f})"
            cells.append(c)
        P(f"  {name:12s} N {RES['rows']['canonical'][name][sn].get('N', '-')}: " + " | ".join(cells))
    P("")

# ------------------------------------------------------------------ Part B (FROZEN_CRITERIA_PARTB.md d26939ed4f, AMENDMENT_PB1 7787483300)
if all(os.path.exists(os.path.join(HERE, "parts", f"partb_{ft}.json")) for ft in FOOTS):
    RES["partB"] = dict(scope="KiDS-Legacy (fetched on the owner's go) and DES Y3: the newest release of each survey on disk", labels={}, KB={}, MUTATE={}, rows={})
    P("PART B: KiDS-Legacy xi+- through the same machinery and gate (with DES Y3 from Part A).")
    for ft in FOOTS:
        b = json.load(open(os.path.join(HERE, "parts", f"partb_{ft}.json"))); bm = json.load(open(os.path.join(HERE, "parts", f"partb_{ft}_MUTATE.json")))
        kb = {k: v["pass_"] for k, v in b["KB"].items() if isinstance(v, dict) and "pass_" in v}
        mb = {k: v["bites"] for k, v in bm["arms"].items()}
        RES["partB"]["KB"][ft] = kb; RES["partB"]["MUTATE"][ft] = mb
        ka = RES["KA"][ft]; mu = RES["MUTATE"][ft]
        ok = all(kb.values()) and all(ka[k] for k in ("KA1_i", "KA1_ii", "KA3", "KA4")) and mb["MB1"] and mu["MA1"] and mu["MA3"]
        a = b["rows"]["BALL"]["at_target"]; leg = a["label"] if ok and not a.get("not_pd") else "NO VERDICT"
        RES["partB"]["labels"][ft] = {}
        for rd in ("frozen", "A1_post_hoc"):
            des = RES["labels"][ft][rd]["DES_Y3"]
            worst = "NO VERDICT" if "NO VERDICT" in (leg, des) else max((leg, des), key=lambda x: RANK[x])
            RES["partB"]["labels"][ft][rd] = dict(KiDS_Legacy=leg, DES_Y3=des, overall=OVR[worst], carries=TAIL,
                                                  MB2_note="MB2 does not bite (0.46 / 0.47 width against 0.5); by the frozen rule it guards no graded row; it removes the redshift-calibration attribution")
        RES["partB"]["rows"][ft] = {n: {k: v for k, v in o.items() if k in ("N", "target_sigma8", "label", "best_sigma8", "width", "gap_widths", "dchi2_target_vs_best", "with_logdet")}
                                    | {"chi2": o["at_target"]["chi2"], "chi2_data": o["at_target"]["chi2_data"], "p": o["at_target"]["p"], "dz_pulls": o["at_target"].get("dz_pulls")}
                                    for n, o in b["rows"].items()}
        RES["partB"]["rows"][ft]["KB4"] = b["KB"]["KB4"]; RES["partB"]["rows"][ft]["MB2"] = bm["arms"]["MB2"]
        for rd in ("frozen", "A1_post_hoc"):
            L = RES["partB"]["labels"][ft][rd]; P(f"[{ft}] PART B LABEL ({'as frozen' if rd == 'frozen' else 'under AMENDMENT A1, post hoc'}): KiDS-Legacy {L['KiDS_Legacy']}; DES Y3 {L['DES_Y3']}; overall {L['overall']} ({TAIL})")
        P("  known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in kb.items()) + ";  MUTATE: " + ", ".join(f"{k} {'bites' if v else 'DOES NOT BITE'}" for k, v in mb.items()))
        for n, o in RES["partB"]["rows"][ft].items():
            if n in ("KB4", "MB2"): continue
            s = f"  {n:10s} N {o['N']}: sigma8 {o['target_sigma8']:.4f} chi2 {o['chi2']:.2f} p {o['p']:.4f} {o['label']}"
            if o.get("best_sigma8") is not None: s += f"; best {o['best_sigma8']:.4f}+-{o['width']:.4f} gap {o['gap_widths']:+.2f}"
            if o.get("with_logdet"): s += f" (ln det: gap {o['with_logdet']['gap_widths']:+.2f})"
            P(s)
    P("")
json.dump(RES, open(os.path.join(HERE, "kl1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1.out"), "w").write("\n".join(OUT) + "\n")
