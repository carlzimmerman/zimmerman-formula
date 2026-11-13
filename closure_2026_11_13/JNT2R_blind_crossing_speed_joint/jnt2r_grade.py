#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): marks, twins, known answers and the label per footing (READING sections 5 to 7).
  python3 jnt2r_grade.py -> jnt2r_grade.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import jnt2r_common as JC
J = lambda n: json.load(open(os.path.join(HERE, n)))
HM, RC, LE, LT, CL, CT = J("jnt2r_hm.json"), J("jnt2r_rc.json"), J("jnt2r_lens.json"), J("jnt2r_lens_MUTATE.json"), J("jnt2r_clusters.json"), J("jnt2r_clusters_MUTATE.json")
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("JNT2R grade (READING 5abea0324b). Footings never pooled. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
FG = ("0.75", "1.00", "1.25", "1.50", "2.00", "3.00")
RES = dict(lane="JNT2R", reading="5abea0324b", foot={})
def gz(cfg): L_ = cfg["gate"]["lines"]; return [round(L_[k]["z"], 4) for k in ("G-K1 all", "G-K1 late", "G-K1 early", "G-K3 type difference")] + [round(L_["G-K2 all profile"]["chi2"], 4)]
for ft in ("canonical", "alt"):
    FO = J(f"jnt2r_forest_{ft}.json"); TW = {t: J(f"jnt2r_forest_{ft}_MUTATE_{t}.json")["TW"] for t in ("V", "N", "H", "D")}
    rc = RC["foot"][ft]; cl = CL["foot"][ft]; ct = CT["foot"][ft]
    def rows_for(mode):
        out = {}
        for f in FG:
            g1 = FO["cases"][f"{mode}_f{f}"]["dchi2"]; r = rc["runs"][f"{'P' if mode == 'P' else mode}|f{f}"] if mode != "B" else rc["runs"][f"B|f{f}"]
            lc = LE["cfg"][f"{ft}|{mode}_f{f}"]; c = cl[f"{mode}|f{f}"]
            out[f] = dict(
                G1=dict(pass_=g1 <= 4, val=round(g1, 4), trivial=g1 < 1, law_equal=all(v == 0 for v in FO["cases"][f"{mode}_f{f}"]["n_above"].values())),
                G2=dict(pass_=r["G2"]["pass_"], val=f"{r['G2']['covered']}/100 covered, {r['G2']['n_above']} above", trivial=False, law_equal=r["G2"]["n_above"] == 0, coverage=True),
                G3=dict(pass_=r["G3"]["pass_"], val=f"by ({r['G3']['by']}); above {r['G3a']['n_above']} (a) / {r['G3b']['n_above']} (b)", trivial=False,
                        law_equal=r["G3a"]["n_above"] == 0 and r["G3b"]["n_above"] == 0, coverage=r["G3"]["by"] == "a"),
                G4=dict(pass_=lc["gate"]["status"] == "PASS", val=gz(lc), trivial=LE["checks"].get(f"{ft}|P_f{f}", {}).get("trivial") if mode == "P" else None, law_equal=lc["nodes_above"] == 0),
                XCOP=dict(pass_=c["a_last_label"] == "CONSISTENT" and c["b_label"] == "CONSISTENT", val=f"(a) {c['a_last'][0]:.3f} {c['a_last_label']}; (b) " + " / ".join(f"{x:+.3f}" for x in c["b_bins"]),
                          trivial=len(c["xcop_below"]) == 0, law_equal=len(c["xcop_below"]) == c["n_xcop"], r500=c["a_R500_label"]),
                GROUPS=dict(pass_=c["c_label"] == "CONSISTENT", val=f"{c['c'][0]:.3f} [{c['c'][1]:.3f}, {c['c'][2]:.3f}]", trivial=len(c["groups_below"]) == 0,
                            law_equal=len(c["groups_below"]) == c["n_groups"], n_below=len(c["groups_below"])))
        return out
    rows = rows_for("P")
    # brackets: B everywhere it exists; M exists for rc and clusters only (forest and lenses have no measured speed: primary values)
    brkB = rows_for("B")
    brkM = {}
    for f in FG:
        r = rc["runs"][f"M|f{f}"]; c = cl[f"M|f{f}"]
        brkM[f] = dict(rows[f]); brkM[f]["G2"] = dict(pass_=r["G2"]["pass_"], val=f"{r['G2']['covered']}/100, {r['G2']['n_above']} above")
        brkM[f]["G3"] = dict(pass_=r["G3"]["pass_"], val=f"by ({r['G3']['by']})"); brkM[f]["XCOP"] = dict(pass_=c["a_last_label"] == "CONSISTENT" and c["b_label"] == "CONSISTENT", val=c["b_label"])
        brkM[f]["GROUPS"] = dict(pass_=c["c_label"] == "CONSISTENT", val=c["c_label"])
    # power (READING 5): (iii) same mark for reference (f 0), law everywhere (TW-N, f 1) and the joint at every grid f
    ref_mark = dict(G1=FO["cases"]["KA_0"]["dchi2"] <= 4, G2=False, G3=rc["G3_f0"]["pass_"], G4=LE["cfg"][f"{ft}|f0"]["gate"]["status"] == "PASS",
                    XCOP=(CL["foot"][ft]["reference"]["a_last_label"] == "CONSISTENT" and CL["foot"][ft]["reference"]["b_label"] == "CONSISTENT"),
                    GROUPS=CL["foot"][ft]["reference"]["c_label"] == "CONSISTENT")
    tn = ct["N|f1.00"]
    law_mark = dict(G1=TW["N"]["dchi2"] <= 4, G2=RC["foot"][ft]["runs"]["N|f1.00"]["G2"]["pass_"], G3=RC["foot"][ft]["runs"]["N|f1.00"]["G3"]["pass_"],
                    G4=LT["cfg"][f"{ft}|TWN_f1.00"]["gate"]["status"] == "PASS", XCOP=tn["a_last_label"] == "CONSISTENT" and tn["b_label"] == "CONSISTENT", GROUPS=tn["c_label"] == "CONSISTENT")
    power = {}
    for k in ref_mark:
        marks = {ref_mark[k], law_mark[k]} | {rows[f][k]["pass_"] for f in FG}
        power[k] = len(marks) > 1
    # carried NO POWER: none of the graded lines above is a carried statistic (G2 is coverage; SRJ3 / SRJ4 data rows are not graded here)
    window = [f for f in FG if all(rows[f][k]["pass_"] for k in rows[f] if power[k])]
    nontriv = {f: [k for k in rows[f] if power[k] and rows[f][k]["pass_"] and not rows[f][k].get("trivial")] for f in window}
    fails = {f: [k for k in rows[f] if power[k] and not rows[f][k]["pass_"]] for f in FG}
    window_nocov = [f for f in FG if all(rows[f][k]["pass_"] for k in rows[f] if power[k] and k != "G2")]   # reported only: the G2 coverage line set aside
    # checks and known answers
    ka = dict(KA1=round(JC.vstar(ft, 0)) == {"canonical": 669, "alt": 808}[ft], KA4_boundary=rc["KA4_vcl_vs_vf"] <= 1e-10, KA4_KA_M=HM["KA"]["C4_KA_M"]["pass_"],
              KA4_f0_hm=HM["KA"]["KA_0_hm"]["pass_"], KA4_f0_gate=FO["KA"]["KA_0_gate"]["pass_"], KA4_f0_G4=LE["checks"][f"{ft}|f0"]["pass_"], KA4_K1=cl["K1"]["pass_"],
              FRZ1_KA2=FO["KA"]["frz1_KA2"]["pass_"], FRZ1_KA3=FO["KA"]["frz1_KA3"]["pass_"], TWN_hm=HM["KA"]["TWN_hm_vs_FZS1"]["pass_"])
    # twins
    p1 = rows["1.00"]
    def mark_diff(t):
        d = []
        if TW[t]["mark_differs"] or TW[t]["moves"]: d.append("G1")
        r = RC["foot"][ft]["runs"][f"{t}|f1.00"]
        if r["G2"]["pass_"] != p1["G2"]["pass_"]: d.append("G2")
        if r["G3"]["pass_"] != p1["G3"]["pass_"]: d.append("G3")
        lt = LT["checks"][f"{ft}|TW{t}"]
        if lt["mark_differs"] or lt["moves"]: d.append("G4")
        c = ct[f"{t}|f1.00"]; pc = cl["P|f1.00"]
        if (c["b_label"] != pc["b_label"] or c["a_last_label"] != pc["a_last_label"] or max(abs(a - b) for a, b in zip(c["b_bins"], pc["b_bins"]) if a == a and b == b) > 0.05
                or abs(c["a_last"][0] - pc["a_last"][0]) > 0.05): d.append("XCOP")
        if c["c_label"] != pc["c_label"] or abs(c["c"][0] - pc["c"][0]) > 0.05: d.append("GROUPS")
        return d
    memdiff_V = (RC["foot"][ft]["runs"]["V|f1.00"]["G2"]["n_above"] != RC["foot"][ft]["runs"]["P|f1.00"]["G2"]["n_above"]) or any(not HM["member"][f"{ft}|{z}"]["P_equals_V"] for z in HM["z_bins"])
    tw = dict(
        TW_V=dict(reproduces=bool(TW["V"]["reproduces"] and rc["TWV_reproduces"] and LT["checks"][f"{ft}|TWV"]["reproduces"] and ct["TWV_reproduces_SRJ2"]), membership_differs=bool(memdiff_V), moves=mark_diff("V")),
        TW_N=dict(reproduces=bool(TW["N"]["reproduces"] and rc["TWN_reproduces"] and LT["checks"][f"{ft}|TWN"]["reproduces"] and ct["TWN_reproduces_SRJ1"]), moves=mark_diff("N")),
        TW_H=dict(moves=mark_diff("H")), TW_D=dict(moves=mark_diff("D")))
    tw["TW_V"]["bites"] = tw["TW_V"]["reproduces"] and tw["TW_V"]["membership_differs"]
    tw["TW_N"]["bites"] = tw["TW_N"]["reproduces"] and len(tw["TW_N"]["moves"]) > 0
    tw["TW_H"]["bites"] = len(tw["TW_H"]["moves"]) > 0; tw["TW_D"]["bites"] = len(tw["TW_D"]["moves"]) > 0
    ok = all(ka.values()) and all(v["bites"] for v in tw.values())
    if not ok: label = "NO VERDICT"
    elif window and any(nontriv[f] for f in window): label = f"JOINT COMPLETE ON POWERED ROWS [{', '.join(window)}]"
    elif window: label = "NO VERDICT (window passes only trivially)"
    else:
        always = [k for k in power if power[k] and all(not rows[f][k]["pass_"] for f in FG)]
        label = "JOINT FAILS ON " + ", ".join(f"{k} ({'coverage' if rows['1.00'][k].get('coverage') else 'data'})" for k in always) if always else "JOINT FAILS (no single f passes every powered row)"
    # fragile: bracket marks against the primary at every grid f; R500 aperture where XCOP passes
    frag = []
    for nm, B in (("B-meas", brkM), ("B-halo", brkB)):
        for f in FG:
            for k in rows[f]:
                if k in B[f] and B[f][k]["pass_"] != rows[f][k]["pass_"]: frag.append(f"{nm}: {k} at f {f}")
    if any(rows[f]["XCOP"]["pass_"] and rows[f]["XCOP"]["r500"] != "CONSISTENT" for f in FG): frag.append("X-COP R500 aperture bracket (inherited)")
    RES["foot"][ft] = dict(label=label, fragile=frag, window=window, window_without_G2=window_nocov, nontrivial_in_window=nontriv, fails_by_f=fails, power=power, ref_mark=ref_mark, law_mark=law_mark,
                           rows=rows, bracket_B_halo=brkB, bracket_M={f: {k: v["pass_"] for k, v in brkM[f].items()} for f in FG}, known_answers=ka, twins=tw)
    P(f"[{ft}] LABEL: {label}" + (f", FRAGILE ({'; '.join(frag)})" if frag else ""))
    P(f"[{ft}] power: {power}; reference marks {ref_mark}; law-everywhere marks {law_mark}")
    P(f"[{ft}] window {window}; without the G2 coverage line {window_nocov}; fails by f {fails}")
    for f in FG: P(f"[{ft}] f {f}: " + "; ".join(f"{k} {'P' if v['pass_'] else 'F'}{' TRIVIAL' if v.get('trivial') else ''}{' LAW-EQUAL' if v.get('law_equal') else ''} {v['val']}" for k, v in rows[f].items()))
    P(f"[{ft}] known answers {ka}")
    P(f"[{ft}] twins {tw}")
json.dump(RES, open(os.path.join(HERE, "jnt2r_grade.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, "jnt2r_grade.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
