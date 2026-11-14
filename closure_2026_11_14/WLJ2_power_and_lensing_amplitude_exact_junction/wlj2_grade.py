#!/usr/bin/env python3
"""WLJ2 (FROZEN_CRITERIA.md, c3bc2d3871) part 6: the labels per gate, case and footing, the row words, and section 4's row-25 word
(RELIEVES / LEAVES UNCHANGED / WORSENS relative to REF). COPY of WLJ1's wlj1_grade.py (closure_2026_11_13/
WLJ1_power_and_lensing_amplitude_with_split/; its AMENDMENT A1 and A2 rules kept) with the case list, the twin case (Ec2; the S2
control's twins read from WLJ1's stored wlj1_grade_MUTATE.json), the words, a missing deskids group tolerated (criteria section 2,
item 6) and section 4's rule added. Reads only this lane's outputs and WLJ1's stored twin file.
  python3 -I -B wlj2_grade.py [--as-frozen]   -> wlj2_grade[_asfrozen].json / .out, wlj2_grade_MUTATE.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
import numpy as np
from scipy.stats import chi2 as CH
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ASF = "--as-frozen" in sys.argv
def J(n):
    p = os.path.join(HERE, n); return json.load(open(p)) if os.path.exists(p) else None
HM, HMM = J("wlj2_hm.json"), J("wlj2_hm_MUTATE.json"); C4, C4M = J("wlj2_c4.json"), J("wlj2_c4_MUTATE.json"); SH, SHM = J("wlj2_shear.json"), J("wlj2_shear_MUTATE.json")
KB = {(ft, g): (J(os.path.join("parts", f"wlj2_kl1bx1_{ft}_{g}.json")) or dict(rows={}, KA={}, missing=True)) for ft in ("canonical", "alt") for g in ("legacy", "deskids", "polish")}
LW = {w: J(f"wlj2_lwb_{w}.json") for w in ("lwb1", "lwb1r")}
W1M = json.load(open(os.path.join(REPO, "closure_2026_11_13", "WLJ1_power_and_lensing_amplitude_with_split", "wlj1_grade_MUTATE.json")))
FOOTS = ("canonical", "alt"); GRADED = ["Ec3", "Ec2", "E0.5", "E0.75", "E1"]; ALLC = ["REF", "ADOPT", "S2"] + GRADED + ["E2"]
CAND = ["S2"] + GRADED + ["E2"]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
HOLD, FAIL, NOV = "ROW HOLDS", "ROW FAILS", "NO VERDICT"
def suffix(cs): return " WITH THE SPLIT" if cs == "S2" else (" WITH THE EXACT JUNCTION" if cs.startswith("E") else "")
def k5(d): return "EXCLUDED" if d >= 9 else ("TENSION" if d >= 4 else "CONSISTENT")
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

# ------------------------------------------------------------------ known answers per gate (WLJ1's, plus this lane's)
KA = dict(hm=bool(HM["KA_ok"]), shear=bool(SH["KA_ok"]))
KA["C4"] = {ft: bool(all(v["pass_"] for k, v in C4["KA"].items() if k.endswith(ft) and not k.startswith("KA_R"))
                     and (C4["KA"][f"KA_R_{ft}"]["pass_"] if ASF else abs(C4["KA"][f"KA_R_{ft}"]["r_eff"] - 1) <= 1e-12)) for ft in FOOTS}
def _ka_use(g, k): return ASF or not (g == "deskids" and k.endswith("|DES"))          # WLJ1 A2
def _kx(ft, bx):
    out = []
    for g in ("legacy", "deskids", "polish"):
        for k, v in KB[(ft, g)].get("KA_X2", {}).items():
            if (k.startswith("GATE_BX1") or k.startswith("C3b_BX1")) == bx and _ka_use(g, k): out.append(v["pass_"])
    return out
KA["KL1"] = {ft: all([v["pass_"] for g in ("legacy", "deskids", "polish") for k, v in KB[(ft, g)]["KA"].items() if not k.startswith("GATE_BX1") and not k.startswith("C3b_BX1") and _ka_use(g, k)] + _kx(ft, False))
             and not KB[(ft, "legacy")].get("missing") and not KB[(ft, "polish")].get("missing") for ft in FOOTS}
KA["BX1"] = {ft: all([v["pass_"] for g in ("legacy", "deskids", "polish") for k, v in KB[(ft, g)]["KA"].items() if (k.startswith("GATE_BX1") or k.startswith("C3b_BX1")) and _ka_use(g, k)] + _kx(ft, True))
             and not KB[(ft, "legacy")].get("missing") and not KB[(ft, "polish")].get("missing") for ft in FOOTS}
KA["LWB1"] = bool(LW["lwb1"] and LW["lwb1"]["KA_ok"]); KA["LWB1R"] = bool(LW["lwb1r"] and LW["lwb1r"]["KA_ok"])
KA["deskids_present"] = {ft: not KB[(ft, "deskids")].get("missing") for ft in FOOTS}
TWB_E = HMM["TWB_bite"]["bites"]; TWB_S2 = W1M["TWB"]["bites"]
P(f"WLJ2 grading ({'AS FROZEN' if ASF else 'with WLJ1 AMENDMENT A1 / A2 where they apply'}). Known answers: {KA}; TW-B bites at Ec2: {TWB_E} (S2: WLJ1's stored {TWB_S2})")

# ------------------------------------------------------------------ statistics and words per gate, per case (WLJ1's gate_rows, copied)
def c4w(cs, ft, src):
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
                 C5=dict(s=c5["d_cold"], word=c5["label"], mine=map_c5(c5["label"]), br=({"z bracket": c5z["label"]} if c5z else {})),
                 CO1=dict(s=c5["d_cold"], word="ROWS HOLD" if co1 == HOLD else ("FAIL" if co1 == FAIL else "NO VERDICT"), mine=co1, br={}),
                 P4=dict(s=p4["chi2_data"], word=p4["label"], mine=map_p4(p4["label"]), br=({"z bracket": p4z["label"]} if p4z else {})))
        if not tw and f"{cs}|{ft}" in SH["C5_brackets"]:
            for n, v in SH["C5_brackets"][f"{cs}|{ft}"].items(): g["C5"]["br"][n] = k5(v["d_cold"])
            for n, v in SH["P4_brackets"][f"{cs}|{ft}"].items(): g["P4"]["br"][n] = lab_p(v["p"])
        for n, w in g["C5"]["br"].items():
            c4b = w4z if n == "z bracket" else w4
            g["CO1"]["br"][n] = "ROWS HOLD" if (c4b == "PASS" and w == "CONSISTENT") else ("FAIL" if (c4b == "FAIL" or w == "EXCLUDED") else "NO VERDICT")
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
        for gate, pzk, c3k in (("KL1", "GATE", "C3b"), ("BX1", "GATE_BX1", "C3b_BX1")):
            lg = KB[(ft, "legacy")]["rows"].get(f"{pzk}|{cs}|Legacy"); ds = KB[(ft, "polish")]["rows"].get(f"{pzk}|{cs}|DES"); kd = KB[(ft, "deskids")]["rows"].get(f"{pzk}|{cs}|KiDS")
            if lg is None or ds is None: continue
            wl = surv(lg["gap_widths"], lg["at_target"]["p"]); c3 = KB[(ft, "legacy")]["rows"].get(f"{c3k}|{cs}|Legacy")
            if wl != "CONSISTENT" and c3 is not None: wl = surv(c3["gap_widths"], c3["at_target"]["p"])
            wd = surv(ds["gap_widths"], ds["p"]); ov = overall([wl, wd])
            ent = dict(s=max(lg["gap_widths"], ds["gap_widths"]), word=ov, mine=map_amp(ov), br={}, legacy=lg["gap_widths"], des=ds["gap_widths"], kids1000=(kd["gap_widths"] if kd else None),
                       readings=dict(Legacy=wl, DES=wd, KiDS1000_reported=(surv(kd["gap_widths"], kd["at_target"]["p"]) if kd else "missing (deskids group not run)")))
            add_l = KB[(ft, "legacy")]["rows"].get(f"{pzk}|{cs}|additive|Legacy"); add_d = KB[(ft, "polish")]["rows"].get(f"{pzk}|{cs}|additive|DES")
            if add_l and add_d: ent["br"]["additive transfer"] = overall([surv(add_l["gap_widths"], add_l["at_target"]["p"]), surv(add_d["gap_widths"], add_d["p"])])
            if gate == "KL1":
                for e in ("R2", "R2b"):
                    el = KB[(ft, "legacy")]["rows"].get(f"GATE_{e}|{cs}|Legacy"); ed = KB[(ft, "deskids")]["rows"].get(f"GATE_{e}|{cs}|DES")
                    if el and ed: ent["br" if ASF else "reported"] = ent.get("br" if ASF else "reported", {}); ent["br" if ASF else "reported"][f"C0 edge {e}"] = overall([surv(el["gap_widths"], el["at_target"]["p"]), surv(ed["gap_widths"], ed["at_target"]["p"])])
            g[gate] = ent
        for gate, w, gk in (("LWB1", "lwb1", "gap"), ("LWB1R", "lwb1r", "gap")):
            r = LW[w]["rows"].get(f"{cs}|{ft}") if LW[w] else None
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
RES = dict(lane="WLJ2", criteria="c3bc2d3871", as_frozen=ASF, KA=KA, TWB_bites_Ec2=TWB_E, TWB_bites_S2_WLJ1=TWB_S2, gates={}, rows={}, row_summary={}, row25_rule={},
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
MUTR = dict(lane="WLJ2", TWB=HMM["TWB_bite"], TWL={}, TWL_T={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
GS = {}
for ft in FOOTS:
    G = gate_rows(ft); GS[ft] = G
    for gate in GATES:
        if gate not in G["Ec2"] or gate not in G["REF"]: continue
        ref, ad = G["REF"].get(gate), G["ADOPT"].get(gate)
        sS, sR, sT = G["Ec2"][gate]["s"], ref["s"], G["TWL"][gate]["s"] if gate in G["TWL"] else None
        floor = 0.002 if gate in ("C5", "CO1", "P4", "KL1", "BX1", "LWB1", "LWB1R", "HLF1") else 1e-9
        if sT is None: twl = dict(applies=False)
        else:
            unseen = abs(sS - sR) <= floor
            twl = dict(s_Ec2=sS, s_REF=sR, s_TWL=sT, bites=bool(abs(sT - sS) >= 0.5 * abs(sS - sR)) and not unseen, unseen=bool(unseen))
        MUTR["TWL"][f"{gate}|{ft}"] = twl
        for cs in ALLC:
            e = G[cs].get(gate)
            if e is None: continue
            word = e["mine"]; notes = []
            if not GATEKA[gate](ft): word, notes = NOV, notes + ["a known answer guarding the gate fails"]
            if cs == "S2":
                tws = W1M["TWL"].get(f"{gate}|{ft}", {})
                if not TWB_S2: word, notes = NOV, notes + ["TW-B does not bite (WLJ1)"]
                if tws.get("applies", True) is not False and not tws.get("bites") and not tws.get("unseen"): word, notes = NOV, notes + ["TW-L does not bite on this gate (WLJ1's stored twin)"]
                unseen_c = bool(tws.get("unseen"))
            elif cs in CAND:
                if not TWB_E: word, notes = NOV, notes + ["TW-B does not bite"]
                if twl.get("applies", True) is not False and not twl.get("bites") and not twl.get("unseen"): word, notes = NOV, notes + ["TW-L does not bite on this gate"]
                unseen_c = bool(twl.get("unseen"))
            else: unseen_c = False
            flips = [b for b, w in e["br"].items() if w is not None and (map_c5(w) if gate == "C5" else map_p4(w) if gate == "P4" else (HOLD if w in ("ROWS HOLD", "PASS") else FAIL if w in ("FAIL",) else NOV) if gate in ("CO1", "C4")
                                                                         else map_amp(w) if gate in ("KL1", "BX1") else map_lwb(w)) != e["mine"]]
            D = LINES[gate](ref["s"])
            eq = bool(cs not in ("REF", "ADOPT") and e["mine"] == ref["mine"] and abs(e["s"] - ref["s"]) <= abs(e["s"] - ad["s"]) and abs(e["s"] - ref["s"]) <= 0.25 * D)
            if cs in CAND and unseen_c: eq = True; notes.append("TW-L: the gate cannot see the layout at all")
            full = word + (suffix(cs) if word != NOV else "") + (f", FRAGILE ({', '.join(flips)})" if flips and word != NOV else "")
            if eq and word != NOV: full = f"EQUALS THE REFERENCE THERE ({full})"
            ent = dict(case=cs, gate=gate, foot=ft, s=e["s"], gate_word=e["word"], word=word, full=full, fragile=flips, equals_reference=eq, D=D,
                       differs_from_ADOPT=bool(word != (G["ADOPT"][gate]["mine"] if GATEKA[gate](ft) else NOV)), brackets=e["br"], notes=notes,
                       frozen_note=FROZEN_NOTE.get(gate), extra={k: v for k, v in e.items() if k in ("legacy", "des", "kids1000", "readings", "f_res", "reported")})
            ent["hit_needing_blind_regrade"] = bool(cs in CAND and word == HOLD and ent["differs_from_ADOPT"])
            RES["gates"][f"{gate}|{cs}|{ft}"] = ent
    for cs in ALLC:
        for row, gl in (("24", ["CO1", "HLF1"]), ("25", ["P4", "KL1", "BX1", "LWB1", "LWB1R"])):
            ws = [RES["gates"][f"{g}|{cs}|{ft}"]["word"] for g in gl if f"{g}|{cs}|{ft}" in RES["gates"]]
            missing = [g for g in gl if f"{g}|{cs}|{ft}" not in RES["gates"]]
            rw = FAIL if FAIL in ws else (HOLD if ws and not missing and all(w == HOLD for w in ws) else NOV)
            RES["rows"][f"{row}|{cs}|{ft}"] = dict(word=rw, full=rw + (suffix(cs) if rw != NOV else ""), gates=dict(zip([g for g in gl if g not in missing], ws)), missing=missing)
    for row in ("24", "25"):
        ws = [RES["rows"][f"{row}|{cs}|{ft}"]["full"] for cs in GRADED]
        RES["row_summary"][f"{row}|{ft}"] = ws[0] if all(w == ws[0] for w in ws) else "NOT RESOLVED (the word depends on the radius): " + "; ".join(f"{cs} {w}" for cs, w in zip(GRADED, ws))

# ------------------------------------------------------------------ section 4: the row-25 tension word
TDEF = [("T1", "KiDS-1000 raw pinned minus best (P4 scan)", 0.02, "P4"), ("T2", "KL1 DES polished g", 0.15, "KL1"), ("T3", "KL1 Legacy g", 0.05, "KL1"),
        ("T4", "BX1 DES polished g", 0.15, "BX1"), ("T5", "BX1 Legacy g", 0.05, "BX1"), ("T6", "LWB1 J g", 0.02, "LWB1"), ("T7", "LWB1R J g", 0.02, "LWB1R")]
def T(ti, cs, ft):
    try:
        if ti == "T1": return (SHM if cs in ("TWL", "TWB") else SH)["P4_scan"][f"{cs}|{ft}"]["pinned_minus_best_in_widths"]
        if ti in ("T2", "T4"): return KB[(ft, "polish")]["rows"][f"{'GATE' if ti == 'T2' else 'GATE_BX1'}|{cs}|DES"]["gap_widths"]
        if ti in ("T3", "T5"): return KB[(ft, "legacy")]["rows"][f"{'GATE' if ti == 'T3' else 'GATE_BX1'}|{cs}|Legacy"]["gap_widths"]
        if ti == "T6": return LW["lwb1"]["rows"][f"{cs}|{ft}"]["primary"]["J"]["gap"]
        if ti == "T7": return LW["lwb1r"]["rows"][f"{cs}|{ft}"]["primary"]["J"]["gap"]
    except (KeyError, TypeError): return None
for ft in FOOTS:
    used = {}
    for ti, nm, dl, gate in TDEF:
        r, e2, tw = T(ti, "REF", ft), T(ti, "Ec2", ft), T(ti, "TWL", ft)
        if r is None or e2 is None: used[ti] = dict(used=False, why="missing rows"); continue
        ka_ok = GATEKA[gate](ft)
        unseen = abs(e2 - r) <= dl
        bites = (tw is not None) and abs(tw - e2) >= 0.5 * abs(e2 - r)
        u = bool(ka_ok and (unseen or bites))
        why = [] if u else (["a known answer guarding the gate fails"] if not ka_ok else []) + ([] if (unseen or bites) else ["TW-L at Ec2 does not bite"])
        used[ti] = dict(used=u, why=why, T_REF=r, T_Ec2=e2, T_TWL=tw, unseen=bool(unseen), twl_bites=bool(bites))
        MUTR["TWL_T"][f"{ti}|{ft}"] = used[ti]
    words = {}
    for cs in ["ADOPT", "S2"] + GRADED + ["E2"]:
        dl_ = {}
        for ti, nm, dl, gate in TDEF:
            v, r = T(ti, cs, ft), T(ti, "REF", ft)
            dl_[ti] = None if (v is None or r is None) else v - r
        up = [ti for ti, nm, dl, gate in TDEF if used[ti]["used"] and dl_[ti] is not None and dl_[ti] > dl]
        dn = [ti for ti, nm, dl, gate in TDEF if used[ti]["used"] and dl_[ti] is not None and dl_[ti] < -dl]
        nused = [ti for ti, nm, dl, gate in TDEF if used[ti]["used"] and dl_[ti] is not None]
        if not nused or (cs in GRADED + ["E2"] and not TWB_E) or (cs == "S2" and not TWB_S2): w = "NO VERDICT"
        elif dn and not up: w = "RELIEVES"
        elif up and not dn: w = "WORSENS"
        elif not up and not dn: w = "LEAVES UNCHANGED"
        else: w = "NOT RESOLVED (mixed)"
        words[cs] = dict(word=w, delta=dl_, up=up, down=dn, used=nused)
    kaw = words["ADOPT"]["word"] == "WORSENS"
    gw = [words[cs]["word"] for cs in GRADED]
    summ = ("NO VERDICT (KA-W: ADOPT does not read WORSENS)" if not kaw else (gw[0] if all(w == gw[0] for w in gw) else "NOT RESOLVED (the word depends on the radius): " + "; ".join(f"{cs} {w}" for cs, w in zip(GRADED, gw))))
    RES["row25_rule"][ft] = dict(statistics=used, cases=words, KA_W=bool(kaw), summary=summ)

# ------------------------------------------------------------------ print
for ft in FOOTS:
    P(f"\n=== {ft}")
    P(f"  ROW 25 TENSION WORD (section 4): {RES['row25_rule'][ft]['summary']}   [KA-W ADOPT reads {RES['row25_rule'][ft]['cases']['ADOPT']['word']}]")
    for cs, v in RES["row25_rule"][ft]["cases"].items():
        P(f"    {cs:6s} {v['word']:22s} Delta vs REF: " + " ".join(f"{k} {('%+.3f' % d) if d is not None else '-'}" for k, d in v["delta"].items()) + f"  (used {v['used']})")
    P("    statistics: " + "; ".join(f"{k}: {'used' if v['used'] else 'NOT USED ' + str(v.get('why'))}" + (f" (REF {v['T_REF']:+.3f}, Ec2 {v['T_Ec2']:+.3f}, TWL {v['T_TWL']:+.3f})" if v.get('T_TWL') is not None else "") for k, v in RES["row25_rule"][ft]["statistics"].items()))
    P(f"  ROW 24 summary: {RES['row_summary']['24|' + ft]}")
    P(f"  ROW 25 summary: {RES['row_summary']['25|' + ft]}")
    for gate in GATES:
        for cs in ALLC:
            e = RES["gates"].get(f"{gate}|{cs}|{ft}")
            if e is None: continue
            P(f"  {gate:6s} {cs:6s} s {e['s']:+.5g}  [{e['gate_word']}]  -> {e['full']}" + (" | differs from ADOPT" if e["differs_from_ADOPT"] else "") + (" | HIT: needs a blind re-grade" if e["hit_needing_blind_regrade"] else "")
              + (f" | notes {e['notes']}" if e["notes"] else "") + (f" | D {e['D']:.3g}" if cs not in ("REF", "ADOPT") else ""))
    for cs in ALLC:
        P(f"  ROW 24 {cs:6s}: {RES['rows'][f'24|{cs}|{ft}']['full']}   ROW 25 {cs:6s}: {RES['rows'][f'25|{cs}|{ft}']['full']}" + (f" (missing gates {RES['rows'][f'25|{cs}|{ft}']['missing']})" if RES['rows'][f'25|{cs}|{ft}']['missing'] else ""))
P(f"\nTW-L bites (gates, at Ec2): " + "; ".join(f"{k} {'not run' if v.get('applies') is False else ('bites' if v.get('bites') else ('unseen' if v.get('unseen') else 'DOES NOT BITE'))}" for k, v in MUTR["TWL"].items()))
tag = "_asfrozen" if ASF else ""
json.dump(RES, open(os.path.join(HERE, f"wlj2_grade{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wlj2_grade{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
if not ASF:
    json.dump(MUTR, open(os.path.join(HERE, "wlj2_grade_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "wlj2_grade_MUTATE.out"), "w").write("\n".join(l for l in OUT if "TW-" in l or "TWL" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
