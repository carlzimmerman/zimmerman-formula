#!/usr/bin/env python3
"""KL1 PART C grading (FROZEN_CRITERIA_PARTC.md 190161a7f7 section 6; AMENDMENT_C1 fe976ca7d3; AMENDMENT_C2 2fd0710da0).
Two readings, both printed, frozen first:
  frozen     NO VERDICT if a known answer guarding the gate fails or any MUTATE arm does not bite (MC1 does not: NO VERDICT).
  amended    (post hoc) DES read on the polished scan (AMENDMENT C3); C1 is a BRACKET, so the gate (C0 R1 + C2 AD) is guarded by MC0, MC2, MP5 and its known answers;
             KC1 on DES read with tolerance 0.2 (C2's diagnostic); MC1b guards the C1 bracket rows.
Per survey: CONSISTENT (|g| <= 2, p >= 0.05) / GAP STAYS (g > 2) / OVERSHOOT (g < -2) / POOR FIT (|g| <= 2, p < 0.05). C3b re-reads
Legacy if it lands outside CONSISTENT.

  python3 kl1c_grade.py     -> kl1c.json, kl1c.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
GC = json.load(open(os.path.join(HERE, "kl1c_gas.json"))); GM = json.load(open(os.path.join(HERE, "kl1c_gas_MUTATE.json"))); M1B = json.load(open(os.path.join(HERE, "kl1c_mc1b_MUTATE.json")))
IA = json.load(open(os.path.join(HERE, "kl1c_ia.json"))); DIAG = json.load(open(os.path.join(HERE, "parts", "kc1diag.json")))
POL = {ft: json.load(open(os.path.join(HERE, "parts", f"polish_{ft}.json"))) for ft in ("canonical", "alt")}      # AMENDMENT C3 (a5d8d7f322)
TAIL = "for form B with the neutrino floor, RB1's gas with the cold component's slow-loss response, the box's draw corrected (R1), the covariance at the model; gravity-only S0 box; inherited halo list"
def read(o):
    g, p = o["gap_widths"], o["at_target"]["p"]
    if g > 2: return "GAP STAYS"
    if g < -2: return "OVERSHOOT"
    return "CONSISTENT" if p >= 0.05 else "POOR FIT"
ORDER = {"CONSISTENT": 0, "POOR FIT": 1, "GAP STAYS": 2, "OVERSHOOT": 2}
def overall(ls):
    if "NO VERDICT" in ls: return "NO VERDICT"
    if all(x == "CONSISTENT" for x in ls): return "AMPLITUDE CONSISTENT"
    bad = sorted({x for x in ls if ORDER[x] == 2})
    return " and ".join(bad) if bad else "POOR FIT"
RES = dict(lane="KL1", part="C", criteria="190161a7f7", amendments=dict(C1="fe976ca7d3", C2="2fd0710da0", C3="a5d8d7f322"), polish={ft: POL[ft]["rows"] for ft in ("canonical", "alt")}, note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           C1_decision=GC["C1_conversion"]["primary"]["decision"], labels={}, rows={}, KA={}, MUTATE={})
for ft in FOOTS:
    L = json.load(open(os.path.join(HERE, "parts", f"partc_{ft}_legacy.json"))); DK = json.load(open(os.path.join(HERE, "parts", f"partc_{ft}_deskids.json")))
    rows = {**L["rows"], **DK["rows"]}
    kc1 = {sn: (L if sn == "Legacy" else DK)["KA"][f"KC1_{sn}"] for sn in ("Legacy", "DES", "KiDS")}
    ka = dict(KC1_Legacy=kc1["Legacy"]["pass_"], KC1_DES=kc1["DES"]["pass_"], KC1_KiDS=kc1["KiDS"]["pass_"], KC1_DES_under_C2=bool(abs(kc1["DES"]["d"]) <= 0.2 and DIAG["optimiser_floor_shown"]),
              KC2=DK["KA"]["KC2"]["pass_"], KC3=bool(all(v["KC3_pass"] for v in GC["KA"].values())), KC4=bool(all(v["KC4_pass"] for v in GC["KA"].values())),
              KC5_map=IA["KC5_map_pass"], KC5_cell=bool(L["KA"]["KC5b"]["pass_"] and DK["KA"]["KC5b"]["pass_"]))
    mu = dict(MC0=DK["MUTATE"]["MC0"]["bites"], MC1=GM["rows"][ft]["MC1"]["bites"], MC1b=M1B["rows"][ft]["bites"], MC2=GM["rows"][ft]["MC2"]["bites"], MP5=L["MUTATE"]["MP5"]["bites"])
    RES["KA"][ft] = ka; RES["MUTATE"][ft] = mu
    gate_ka = lambda sn, amended: ka["KC2"] and ka["KC3"] and (ka[f"KC1_{sn}"] or (amended and sn == "DES" and ka["KC1_DES_under_C2"]))
    lab = {}
    for rd in ("frozen", "amended"):
        per = {}
        for sn in ("Legacy", "DES", "KiDS"):
            o = rows[f"GATE|{sn}"]
            if rd == "amended" and sn == "DES":                          # C3: DES read on the polished scan
                q = POL[ft]["rows"]["GATE"]; o = dict(gap_widths=q["gap_widths"], at_target=dict(p=q["p"]))
            ok = gate_ka(sn, rd == "amended") and mu["MC0"] and mu["MC2"] and mu["MP5"] and (rd == "amended" or all(mu[k] for k in ("MC0", "MC1", "MC2", "MP5")))
            per[sn] = read(o) if ok else "NO VERDICT"
        c3 = rows["C3b_own_prior|Legacy"]; c3r = read(c3) if ka["KC5_map"] and ka["KC5_cell"] else "NO VERDICT"
        leg = per["Legacy"] if (per["Legacy"] == "NO VERDICT" or c3r == "CONSISTENT") else c3r
        lab[rd] = dict(Legacy=leg, Legacy_without_C3=per["Legacy"], C3b=c3r, DES=per["DES"], KiDS_1000_reported=per["KiDS"], overall=overall([leg, per["DES"]]))
    RES["labels"][ft] = lab
    keep = ("N", "target_sigma8", "label", "best_sigma8", "width", "gap_widths", "with_logdet")
    RES["rows"][ft] = {k: {**{kk: v[kk] for kk in keep if kk in v}, "chi2": v["at_target"]["chi2"], "p": v["at_target"]["p"], "A_i": v["at_target"].get("A_i"), "ia_pulls": v["at_target"].get("ia_pulls"),
                           "dz_pulls": v["at_target"].get("dz_pulls")} for k, v in rows.items()}
P("KL1 PART C: the remaining gap after the box's draw (C0), the cold component's response (C2), gas from the kSZ stack (C1, a BRACKET by the frozen rule) and Legacy's own alignment (C3).")
P(f"C1 conversion: f_a {GC['C1_conversion']['primary']['a']['f']:.3f} +- {GC['C1_conversion']['primary']['a']['sigma_f']:.3f}, f_b {GC['C1_conversion']['primary']['b']['f']:.3f} +- "
  f"{GC['C1_conversion']['primary']['b']['sigma_f']:.3f} -> {RES['C1_decision']}\n")
for ft in FOOTS:
    for rd, nm in (("frozen", "as frozen"), ("amended", "under AMENDMENTS C1 + C2 + C3, post hoc")):
        l = RES["labels"][ft][rd]
        P(f"[{ft}] PART C LABEL ({nm}): {l['overall']}  (Legacy {l['Legacy']}; DES Y3 {l['DES']}; C3b {l['C3b']}; KiDS-1000, reported, {l['KiDS_1000_reported']})")
    P("  known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in RES["KA"][ft].items()) + ";  MUTATE: " + ", ".join(f"{k} {'bites' if v else 'DOES NOT BITE'}" for k, v in RES["MUTATE"][ft].items()))
P("")
names = []
for k in RES["rows"]["canonical"]:
    n = k.split("|")[0]
    if n not in names: names.append(n)
for sn in ("Legacy", "DES", "KiDS"):
    P(f"{sn} (canonical | alt): chi2, p, label; best sigma8 +- width, gap (ln det)")
    for n in names:
        k = f"{n}|{sn}"
        if k not in RES["rows"]["canonical"]: continue
        cells = []
        for ft in FOOTS:
            o = RES["rows"][ft].get(k)
            if o is None: cells.append("-"); continue
            c = f"{o['target_sigma8']:.4f} chi2 {o['chi2']:.2f} p {o['p']:.4f} {o['label']}"
            if o.get("best_sigma8") is not None: c += f"; best {o['best_sigma8']:.4f}+-{o['width']:.4f} gap {o['gap_widths']:+.2f}"
            if o.get("with_logdet"): c += f" ({o['with_logdet']['gap_widths']:+.2f})"
            cells.append(c)
        P(f"  {n:18s} N {RES['rows']['canonical'][k].get('N', '-')}: " + " | ".join(cells))
    P("")
json.dump(RES, open(os.path.join(HERE, "kl1c.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1c.out"), "w").write("\n".join(OUT) + "\n")
