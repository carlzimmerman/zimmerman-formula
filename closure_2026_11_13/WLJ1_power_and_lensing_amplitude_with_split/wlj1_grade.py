#!/usr/bin/env python3
"""WLJ1 (FROZEN_CRITERIA.md, 03f9823de7; AMENDMENT_A1 if present) part 6: the labels of section 3, per gate, per f, per footing, for
REF, ADOPT and SPLIT, with FRAGILE (frozen brackets), EQUALS THE REFERENCE THERE, the twins and the known answers. Reads only this
lane's outputs. Writes wlj1_grade.json / .out and wlj1_grade_MUTATE.json / .out (the twins' bites).
  python3 -I -B wlj1_grade.py [--as-frozen]
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
import numpy as np
from scipy.stats import chi2 as CH
HERE = os.path.dirname(os.path.abspath(__file__))
ASF = "--as-frozen" in sys.argv
def J(n): return json.load(open(os.path.join(HERE, n)))
HM, HMM = J("wlj1_hm.json"), J("wlj1_hm_MUTATE.json"); C4, C4M = J("wlj1_c4.json"), J("wlj1_c4_MUTATE.json"); SH, SHM = J("wlj1_shear.json"), J("wlj1_shear_MUTATE.json")
KB = {(ft, g): J(os.path.join("parts", f"wlj1_kl1bx1_{ft}_{g}.json")) for ft in ("canonical", "alt") for g in ("legacy", "deskids", "polish")}
LW = {w: J(f"wlj1_lwb_{w}.json") for w in ("lwb1", "lwb1r")}
FOOTS = ("canonical", "alt"); GR = ["S1.25", "S2", "S3"]; ALLC = ["REF", "ADOPT", "S1.25", "S2", "S3", "Sinf"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
HOLD, FAIL, NOV = "ROW HOLDS WITH THE SPLIT", "ROW FAILS WITH THE SPLIT", "NO VERDICT"
def k5(d):
    return "EXCLUDED" if d >= 9 else ("TENSION" if d >= 4 else "CONSISTENT")
def map_c5(w): return HOLD if w == "CONSISTENT" else (FAIL if w == "EXCLUDED" else NOV)
def lab_p(p): return "CONSISTENT" if p >= 0.05 else ("TENSION" if p >= 0.0027 else "EXCLUDED AT 3 SIGMA")
def map_p4(w): return HOLD if w == "CONSISTENT" else (FAIL if w.startswith("EXCLUDED") else NOV)
def surv(g, p):
    if abs(g) <= 2 and p >= 0.05: return "CONSISTENT"
    if g > 2: return "GAP STAYS"
    if g < -2: return "OVERSHOOT"
    return "POOR FIT"
def overall(ws):
    if all(w == "CONSISTENT" for w in ws): return "AMPLITUDE CONSISTENT"
    bad = [w for w in ws if w in ("GAP STAYS", "OVERSHOOT")]
    if bad: return " / ".join(sorted(set(bad)))
    return "POOR FIT"
def map_amp(w): return HOLD if w == "AMPLITUDE CONSISTENT" else FAIL
def map_lwb(w): return HOLD if w == "AMPLITUDE CONSISTENT" else (FAIL if (w.startswith("GAP") or w.startswith("TENSION")) else NOV)

# ------------------------------------------------------------------ known answers per gate
KA = dict(hm=HM["KA_ok"], shear=SH["KA_ok"])
# C4's known answers per footing; AMENDMENT A1: KA-R's "exactly" read as |r_eff - 1| <= 1e-12 (floating-point rounding)
KA["C4"] = {ft: bool(all(v["pass_"] for k, v in C4["KA"].items() if k.endswith(ft) and not k.startswith("KA_R"))
                     and (C4["KA"][f"KA_R_{ft}"]["pass_"] if ASF else abs(C4["KA"][f"KA_R_{ft}"]["r_eff"] - 1) <= 1e-12)) for ft in FOOTS}
def _ka_use(g, k):
    # AMENDMENT A2: DES rows of KL1's frozen scan (group deskids) are reported, not gating; the polished DES known answer gates
    return ASF or not (g == "deskids" and k.endswith("|DES"))
KA["KL1"] = {ft: all(v["pass_"] for g in ("legacy", "deskids", "polish") for k, v in KB[(ft, g)]["KA"].items() if not k.startswith("GATE_BX1") and not k.startswith("C3b_BX1") and _ka_use(g, k)) for ft in FOOTS}
KA["BX1"] = {ft: all(v["pass_"] for g in ("legacy", "deskids", "polish") for k, v in KB[(ft, g)]["KA"].items() if (k.startswith("GATE_BX1") or k.startswith("C3b_BX1")) and _ka_use(g, k)) for ft in FOOTS}
KA["LWB1"], KA["LWB1R"] = LW["lwb1"]["KA_ok"], LW["lwb1r"]["KA_ok"]
TWB_BITES = HMM["TWB_bite"]["bites"]
P(f"WLJ1 grading ({'AS FROZEN' if ASF else 'with AMENDMENT A1 where it applies'}). Known answers: {KA}; TW-B bites: {TWB_BITES}")

# ------------------------------------------------------------------ statistics and words per gate, per case
def c4w(cs, ft, src=C4):
    r = src["rows"][f"{cs}|{ft}"]; return abs(r["held"]["r_eff"] - 1), ("PASS" if r["status"] == "PASS" else "FAIL"), (r.get("status_z_bracket"))
def gate_rows(ft):
    G = {}
    for cs in ALLC + ["TWB", "TWL"]:
        tw = cs in ("TWB", "TWL"); c4src = C4M if tw else C4; shs = SHM if tw else SH
        s4, w4, w4z = c4w(cs, ft, c4src)
        c5 = shs["C5"][f"{cs}|{ft}"]; c5z = shs["C5_zb"].get(f"{cs}|{ft}")
        p4 = shs["P4"][f"{cs}|{ft}"]; p4z = shs["P4_zb"].get(f"{cs}|{ft}")
        co1 = HOLD if (w4 == "PASS" and c5["label"] == "CONSISTENT") else (FAIL if (w4 == "FAIL" or c5["label"] == "EXCLUDED") else NOV)
        g = dict(C4=dict(s=s4, word=w4, mine=HOLD if w4 == "PASS" else FAIL, br={"z bracket": w4z} if w4z else {}),
                 C5=dict(s=c5["d_cold"], word=c5["label"], mine=map_c5(c5["label"]),
                         br=({"z bracket": c5z["label"]} if c5z else {})),
                 CO1=dict(s=c5["d_cold"], word="ROWS HOLD" if co1 == HOLD else ("FAIL" if co1 == FAIL else "NO VERDICT"), mine=co1, br={}),
                 P4=dict(s=p4["chi2_data"], word=p4["label"], mine=map_p4(p4["label"]), br=({"z bracket": p4z["label"]} if p4z else {})))
        if not tw and f"{cs}|{ft}" in SH["C5_brackets"]:
            for n, v in SH["C5_brackets"][f"{cs}|{ft}"].items(): g["C5"]["br"][n] = k5(v["d_cold"])
            for n, v in SH["P4_brackets"][f"{cs}|{ft}"].items(): g["P4"]["br"][n] = lab_p(v["p"])
        # CO1 rule brackets: C4's z bracket with C5's z bracket; C5's layout brackets with C4 PASS (C4 brackets not run: C4 is 1e-4 of its line)
        for n, w in g["C5"]["br"].items():
            c4b = w4z if n == "z bracket" else w4
            g["CO1"]["br"][n] = "ROWS HOLD" if (c4b == "PASS" and w == "CONSISTENT") else ("FAIL" if (c4b == "FAIL" or w == "EXCLUDED") else "NO VERDICT")
        # HLF1 Part A
        if not tw and f"{cs}|{ft}" in SH["HLF1"]:
            own5 = SH["HLF1"][f"{cs}|{ft}"]["label"]; own4 = "PASS" if (cs == "REF" or C4["rows"][f"own:{cs}|{ft}"]["status"] == "PASS") else "FAIL"
            own_co1 = "ROWS HOLD" if (own4 == "PASS" and own5 == "CONSISTENT") else ("FAIL" if (own4 == "FAIL" or own5 == "EXCLUDED") else "NO VERDICT")
            fres = None if cs == "REF" else HM["f_res"][ft][cs]["1.0"]["f_res"]
            if fres is not None and not (fres >= 0.5): hw, hm_ = "NOT RESOLVED", NOV
            elif own4 == w4 and own5 == c5["label"] and own_co1 == g["CO1"]["word"]: hw, hm_ = "ROWS HOLD WITH THE OWN LIST", HOLD
            else:
                order = {"ROWS HOLD": 0, "NO VERDICT": 1, "FAIL": 2}; worse = order[own_co1] > order[g["CO1"]["word"]]
                hw, hm_ = f"ROWS MOVE ({g['CO1']['word']} -> {own_co1})", (FAIL if worse else NOV)
            g["HLF1"] = dict(s=SH["HLF1"][f"{cs}|{ft}"]["d_cold"], word=hw + (" (trivial: no redistribution)" if cs == "REF" else ""), mine=hm_, br={}, f_res=fres)
        # KL1 and BX1
        for gate, pzk, c3k in (("KL1", "GATE", "C3b"), ("BX1", "GATE_BX1", "C3b_BX1")):
            try:
                lg = KB[(ft, "legacy")]["rows"][f"{pzk}|{cs}|Legacy"]; ds = KB[(ft, "polish")]["rows"][f"{pzk}|{cs}|DES"]; kd = KB[(ft, "deskids")]["rows"][f"{pzk}|{cs}|KiDS"]
            except KeyError: continue
            wl = surv(lg["gap_widths"], lg["at_target"]["p"]); c3 = KB[(ft, "legacy")]["rows"].get(f"{c3k}|{cs}|Legacy")
            if wl != "CONSISTENT" and c3 is not None: wl = surv(c3["gap_widths"], c3["at_target"]["p"])
            wd = surv(ds["gap_widths"], ds["p"]); ov = overall([wl, wd])
            ent = dict(s=max(lg["gap_widths"], ds["gap_widths"]), word=ov, mine=map_amp(ov), br={}, legacy=lg["gap_widths"], des=ds["gap_widths"], kids1000=kd["gap_widths"],
                       readings=dict(Legacy=wl, DES=wd, KiDS1000_reported=surv(kd["gap_widths"], kd["at_target"]["p"])))
            add_l = KB[(ft, "legacy")]["rows"].get(f"{pzk}|{cs}|additive|Legacy"); add_d = KB[(ft, "polish")]["rows"].get(f"{pzk}|{cs}|additive|DES")
            if add_l and add_d: ent["br"]["additive transfer"] = overall([surv(add_l["gap_widths"], add_l["at_target"]["p"]), surv(add_d["gap_widths"], add_d["p"])])
            if gate == "KL1":
                for e in ("R2", "R2b"):
                    el = KB[(ft, "legacy")]["rows"].get(f"GATE_{e}|{cs}|Legacy"); ed = KB[(ft, "deskids")]["rows"].get(f"GATE_{e}|{cs}|DES")
                    if el and ed: ent["br" if ASF else "reported"] = ent.get("br" if ASF else "reported", {}); ent["br" if ASF else "reported"][f"C0 edge {e}"] = overall([surv(el["gap_widths"], el["at_target"]["p"]), surv(ed["gap_widths"], ed["at_target"]["p"])])
            g[gate] = ent
        # LWB1 and LWB1R
        for gate, w, bk, gk in (("LWB1", "lwb1", "best_sigma8", "gap"), ("LWB1R", "lwb1r", "best", "gap")):
            r = LW[w]["rows"].get(f"{cs}|{ft}")
            if r is None: continue
            jw = r["primary"]["J"]["label"]; pims = [r["brackets"][f"pimax_{p}"]["J"]["label"] for p in (80, 100)]
            word = jw if all(x == jw for x in pims) else "NO VERDICT (J label changes with pi_max)"
            ent = dict(s=r["primary"]["J"][gk], word=word, mine=map_lwb(word), br={})
            for b, v in r["brackets"].items():
                if b in ("pimax_80", "pimax_100"): continue
                ent["br"][b] = v["J"]["label"]
            g[gate] = ent
        G[cs] = g
    return G
GATES = ["C4", "C5", "CO1", "HLF1", "P4", "KL1", "BX1", "LWB1", "LWB1R"]
LINES = dict(C4=lambda s: 0.0481 - s, C5=lambda s: 4 - s, CO1=lambda s: 4 - s, HLF1=lambda s: 4 - s,
             P4=lambda s: min(abs(s - CH.isf(0.0027, 104)), abs(s - CH.isf(0.05, 104))), KL1=lambda s: min(abs(2 - s), abs(s + 2)), BX1=lambda s: min(abs(2 - s), abs(s + 2)),
             LWB1=lambda s: min(abs(2 - s), abs(s + 2)), LWB1R=lambda s: min(abs(2 - s), abs(s + 2)))
GATEKA = dict(C4=lambda ft: KA["hm"] and KA["C4"][ft], C5=lambda ft: KA["hm"] and KA["shear"], CO1=lambda ft: KA["hm"] and KA["C4"][ft] and KA["shear"],
              HLF1=lambda ft: KA["hm"] and KA["C4"][ft] and KA["shear"], P4=lambda ft: KA["hm"] and KA["shear"], KL1=lambda ft: KA["hm"] and KA["KL1"][ft],
              BX1=lambda ft: KA["hm"] and KA["BX1"][ft], LWB1=lambda ft: KA["hm"] and KA["LWB1"], LWB1R=lambda ft: KA["hm"] and KA["LWB1R"])
FROZEN_NOTE = dict(CO1="[lane as frozen: NO VERDICT (CO1 M4 as written), cause independent of the layout]", HLF1="[lane as frozen: NO VERDICT (HLF1 MA1), cause independent of the layout]",
                   KL1="[lane as frozen: NO VERDICT (KL1 MC1), cause independent of the layout]", BX1="[lane as frozen: NO VERDICT (BX1 KA3, MB2), cause independent of the layout]",
                   LWB1="[lane as frozen: NO VERDICT (LWB1 KA1), cause independent of the layout]")
RES = dict(lane="WLJ1", criteria="03f9823de7", as_frozen=ASF, KA=KA, TWB_bites=TWB_BITES, gates={}, rows={}, twins={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUTR = dict(lane="WLJ1", TWB=HMM["TWB_bite"], TWL={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for ft in FOOTS:
    G = gate_rows(ft)
    for gate in GATES:
        if gate not in G["S2"]: continue
        ref, ad = G["REF"].get(gate), G["ADOPT"].get(gate)
        # TW-L bite on this gate
        sS, sR, sT = G["S2"][gate]["s"], ref["s"], G["TWL"][gate]["s"] if gate in G["TWL"] else None
        floor = 0.002 if gate in ("C5", "CO1", "P4", "KL1", "BX1", "LWB1", "LWB1R", "HLF1") else 1e-9
        if sT is None: twl = dict(applies=False)
        else:
            unseen = abs(sS - sR) <= floor
            twl = dict(s_S2=sS, s_REF=sR, s_TWL=sT, bites=bool(abs(sT - sS) >= 0.5 * abs(sS - sR)) and not unseen, unseen=bool(unseen))
        MUTR["TWL"][f"{gate}|{ft}"] = twl
        for cs in ALLC:
            e = G[cs].get(gate)
            if e is None: continue
            word = e["mine"]; notes = []
            if not GATEKA[gate](ft): word, notes = NOV, notes + ["a known answer guarding the gate fails"]
            if cs.startswith("S") and not TWB_BITES: word, notes = NOV, notes + ["TW-B does not bite"]
            if cs.startswith("S") and twl.get("applies", True) is not False and not twl.get("bites") and not twl.get("unseen"): word, notes = NOV, notes + ["TW-L does not bite on this gate"]
            flips = [b for b, w in e["br"].items() if w is not None and (map_c5(w) if gate == "C5" else map_p4(w) if gate == "P4" else (HOLD if w in ("ROWS HOLD", "PASS") else FAIL if w in ("FAIL",) else NOV) if gate in ("CO1", "C4")
                                                                         else map_amp(w) if gate in ("KL1", "BX1") else map_lwb(w)) != e["mine"]]
            D = LINES[gate](ref["s"])
            eq = bool(cs not in ("REF", "ADOPT") and e["mine"] == ref["mine"] and abs(e["s"] - ref["s"]) <= abs(e["s"] - ad["s"]) and abs(e["s"] - ref["s"]) <= 0.25 * D)
            if cs.startswith("S") and twl.get("unseen"): eq = True; notes.append("TW-L: the gate cannot see the layout at all")
            full = word + (f", FRAGILE ({', '.join(flips)})" if flips and word != NOV else "")
            if eq and word != NOV: full = f"EQUALS THE REFERENCE THERE ({full})"
            ent = dict(case=cs, gate=gate, foot=ft, s=e["s"], gate_word=e["word"], word=word, full=full, fragile=flips, equals_reference=eq, D=D,
                       differs_from_ADOPT=bool(word != (G["ADOPT"][gate]["mine"] if GATEKA[gate](ft) else NOV)), brackets=e["br"], notes=notes,
                       frozen_note=FROZEN_NOTE.get(gate), extra={k: v for k, v in e.items() if k in ("legacy", "des", "kids1000", "readings", "f_res", "reported")})
            ent["hit_needing_blind_regrade"] = bool(cs.startswith("S") and word == HOLD and ent["differs_from_ADOPT"])
            RES["gates"][f"{gate}|{cs}|{ft}"] = ent
    # row words
    for cs in ALLC:
        for row, gl in (("24", ["CO1", "HLF1"]), ("25", ["P4", "KL1", "BX1", "LWB1", "LWB1R"])):
            ws = [RES["gates"][f"{g}|{cs}|{ft}"]["word"] for g in gl if f"{g}|{cs}|{ft}" in RES["gates"]]
            rw = FAIL if FAIL in ws else (HOLD if ws and all(w == HOLD for w in ws) else NOV)
            RES["rows"][f"{row}|{cs}|{ft}"] = dict(word=rw, gates=dict(zip(gl, ws)))
for ft in FOOTS:
    P(f"\n=== {ft}")
    for gate in GATES:
        for cs in ALLC:
            e = RES["gates"].get(f"{gate}|{cs}|{ft}")
            if e is None: continue
            P(f"  {gate:6s} {cs:6s} s {e['s']:+.5g}  [{e['gate_word']}]  -> {e['full']}" + (" | differs from ADOPT" if e["differs_from_ADOPT"] else "") + (" | HIT: needs a blind re-grade" if e["hit_needing_blind_regrade"] else "")
              + (f" | notes {e['notes']}" if e["notes"] else "") + (f" | D {e['D']:.3g}" if cs not in ("REF", "ADOPT") else ""))
    for cs in ALLC:
        P(f"  ROW 24 {cs:6s}: {RES['rows'][f'24|{cs}|{ft}']['word']}   ROW 25 {cs:6s}: {RES['rows'][f'25|{cs}|{ft}']['word']}")
P(f"\nTW-L bites: " + "; ".join(f"{k} {'not run (no twin on this gate)' if v.get('applies') is False else ('bites' if v.get('bites') else ('unseen' if v.get('unseen') else 'DOES NOT BITE'))}" for k, v in MUTR["TWL"].items()))
tag = "_asfrozen" if ASF else ""
json.dump(RES, open(os.path.join(HERE, f"wlj1_grade{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wlj1_grade{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
if not ASF:
    json.dump(MUTR, open(os.path.join(HERE, "wlj1_grade_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "wlj1_grade_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TW-" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
