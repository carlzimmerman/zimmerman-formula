#!/usr/bin/env python3
"""BX1 grading (FROZEN_CRITERIA.md 21e1c07e9a sections 7-8; AMENDMENT_A1.md 4af7a4b905, post hoc), from bx1_ka.json and
parts/bx1_<footing>_<legacy|deskids|polish>.json.
Per survey and footing: g = (target - best) / width; CONSISTENT (|g| <= 2, p >= 0.05) / GAP STAYS (g > 2) / OVERSHOOT (g < -2) /
POOR FIT (|g| <= 2, p < 0.05). Legacy and KiDS-1000 on KL1's frozen scan; DES Y3 on AMENDMENT C3's polished scan. C3b re-reads
Legacy if it lands outside CONSISTENT. Overall (Legacy + DES Y3).
  FROZEN   graded splice pair A (512^3); NO VERDICT if KA1-KA5 fail or MB1 / MB2 does not bite (KA3 fails, MB2 does not bite).
           The pair-A readings are printed beside the withheld label.
  A1       KA3 (a') replaces KA3, MB2' replaces MB2; graded splice = mean of the 512^3 pairs A + B, sigma_g = max(|g_A - g_B| / 2,
           |g_A256 - g_B256| / 2). Until 512^3 pair B exists: the INTERIM reading on pair A with sigma_g = |g_A256 - g_B256| / sqrt(2).
[INSIDE SPLICE NOISE] if |g - 2| < 2 sigma_g (never changes a label).
  python3 bx1_grade.py     -> bx1.json, bx1.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); FOOTS = ("canonical", "alt"); SNS = ("Legacy", "DES", "KiDS"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
KAJ = json.load(open(os.path.join(HERE, "bx1_ka.json"))); KA_, MU_ = KAJ["KA"], KAJ["MUTATE"]
def part(ft, g): return json.load(open(os.path.join(HERE, "parts", f"bx1_{ft}_{g}.json")))
def read(g, p):
    if g > 2: return "GAP STAYS"
    if g < -2: return "OVERSHOOT"
    return "CONSISTENT" if p >= 0.05 else "POOR FIT"
ORDER = {"CONSISTENT": 0, "POOR FIT": 1, "GAP STAYS": 2, "OVERSHOOT": 2}
def overall(ls):
    if "NO VERDICT" in ls: return "NO VERDICT"
    if all(x == "CONSISTENT" for x in ls): return "AMPLITUDE CONSISTENT"
    bad = sorted({x for x in ls if ORDER[x] == 2}); return " and ".join(bad) if bad else "POOR FIT"
def ok(d, k): return bool(d.get(k, {}).get("pass_", False))
sim = dict(KA1=ok(KA_, "KA1"), KA2=ok(KA_, "KA2"), KA2_pA=ok(KA_, "KA2_pA"), KA2_pAi=ok(KA_, "KA2_pAi"))
RES = dict(lane="BX1", criteria="21e1c07e9a", amendment_A1="4af7a4b905 (post hoc)", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", labels={}, rows={}, KA={}, MUTATE={})
for ft in FOOTS:
    L, D, Q = part(ft, "legacy"), part(ft, "deskids"), part(ft, "polish")
    ka = dict(sim, KA4_Legacy=ok(L["KA"], "KA4_Legacy"), KA4_DES=ok(D["KA"], "KA4_DES"), KA4_KiDS=ok(D["KA"], "KA4_KiDS"), KA5=ok(L["KA"], "KA5"))
    rows = {"Legacy": {k.split("|")[0]: (v["gap_widths"], v["at_target"]["p"], v["best_sigma8"], v["width"]) for k, v in L["rows"].items() if "gap_widths" in v},
            "DES": {k.split("|")[0]: (v["gap_widths"], v["p"], v["best_sigma8"], v["width"]) for k, v in Q["rows"].items()},
            "KiDS": {k.split("|")[0]: (v["gap_widths"], v["at_target"]["p"], v["best_sigma8"], v["width"]) for k, v in D["rows"].items() if k.endswith("|KiDS") and "gap_widths" in v},
            "DES_frozen_scan": {k.split("|")[0]: (v["gap_widths"], v["at_target"]["p"], v["best_sigma8"], v["width"]) for k, v in D["rows"].items() if k.endswith("|DES") and "gap_widths" in v}}
    lnd = {sn: X["rows"].get(f"GATE_BX1|{sn}", {}).get("with_logdet", {}).get("gap_widths") for sn, X in (("Legacy", L), ("DES", D), ("KiDS", D))}
    mb1 = {sn: rows[sn]["GATE_BX1"][0] - rows[sn]["MB1_x09"][0] for sn in ("Legacy", "DES")}; mb1_b = bool(all(v >= 0.3 for v in mb1.values()))
    def labels(gate, ka_ok, sig):
        per = {sn: (read(*rows[sn][gate][:2]) if ka_ok else "NO VERDICT") for sn in SNS}
        c3 = (read(*rows["Legacy"]["C3b_BX1"][:2]) if ka_ok else "NO VERDICT") if gate == "GATE_BX1" else "not run on this splice"
        leg = per["Legacy"] if (per["Legacy"] == "NO VERDICT" or c3 in ("CONSISTENT", "not run on this splice")) else c3
        tags = {sn: ("[INSIDE SPLICE NOISE]" if sn in sig and abs(rows[sn][gate][0] - 2) < 2 * sig[sn] else "") for sn in SNS}
        return dict(overall=overall([leg, per["DES"]]), Legacy=leg, Legacy_without_C3b=per["Legacy"], C3b=c3, DES=per["DES"], KiDS_1000_reported=per["KiDS"], tags=tags, sigma_g=sig)
    s256 = {sn: abs(rows[sn]["REP_A256"][0] - rows[sn]["REP_B256"][0]) for sn in SNS if "REP_A256" in rows[sn] and "REP_B256" in rows[sn]}
    frozen_ok = all(ka.values()) and ok(KA_, "KA3") and mb1_b and MU_.get("MB2", {}).get("bites", False)
    lab = dict(frozen=labels("GATE_BX1", frozen_ok, {sn: v / math.sqrt(2) for sn, v in s256.items()}))
    lab["frozen"]["pair_A_reading_if_not_withheld"] = labels("GATE_BX1", True, {sn: v / math.sqrt(2) for sn, v in s256.items()})
    a1_ok = all(ka.values()) and ok(KA_, "KA3a_A1") and mb1_b and MU_.get("MB2_A1", {}).get("bites", False)
    have_B = all("REP_B" in rows[sn] and "REP_AB" in rows[sn] for sn in SNS)
    if have_B:
        sig = {sn: max(abs(rows[sn]["GATE_BX1"][0] - rows[sn]["REP_B"][0]) / 2, s256.get(sn, 0) / 2) for sn in SNS}
        lab["A1"] = dict(labels("REP_AB", a1_ok, sig), splice="mean of 512^3 pairs A + B (graded)")
    else:
        lab["A1_interim"] = dict(labels("GATE_BX1", a1_ok, {sn: v / math.sqrt(2) for sn, v in s256.items()}),
                                 splice="512^3 pair A only; A1's graded A + B mean pending (512^3 pair B not finished)")
    RES["labels"][ft] = lab; RES["KA"][ft] = dict(ka, KA3_frozen=ok(KA_, "KA3"), KA3a_A1=ok(KA_, "KA3a_A1"))
    RES["MUTATE"][ft] = dict(MB1_drop=mb1, MB1=mb1_b, MB2_frozen=MU_.get("MB2", {}).get("bites", False), MB2_A1=MU_.get("MB2_A1", {}).get("bites", False))
    RES["rows"][ft] = dict(rows=rows, ln_det_gap_GATE_BX1=lnd, sigma_256_pair_diff=s256)
P("BX1: KL1 Part C's gate (C2 slow-loss response, covariance at the model) with the fixed-amplitude paired 200 Mpc/h S0 splice below k 0.5 in place of R1.")
for ft in FOOTS:
    for key, nm in (("frozen", "AS FROZEN"), ("A1", "UNDER AMENDMENT A1 (post hoc)"), ("A1_interim", "UNDER AMENDMENT A1 (post hoc), INTERIM on pair A")):
        if key not in RES["labels"][ft]: continue
        l = RES["labels"][ft][key]
        P(f"[{ft}] {nm}: {l['overall']}  (KiDS-Legacy {l['Legacy']} {l['tags']['Legacy']}; DES Y3 {l['DES']} {l['tags']['DES']}; C3b {l['C3b']}; KiDS-1000, reported, {l['KiDS_1000_reported']} {l['tags']['KiDS']})"
          + (f"  [{l['splice']}]" if "splice" in l else ""))
        if key == "frozen":
            q = l["pair_A_reading_if_not_withheld"]
            P(f"      the withheld pair-A gate reads: Legacy {q['Legacy']}, DES Y3 {q['DES']}, KiDS-1000 {q['KiDS_1000_reported']} -> {q['overall']}")
        P("      sigma_g: " + ", ".join(f"{k} {v:.2f}" for k, v in l["sigma_g"].items()))
    P("  known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in RES["KA"][ft].items()) + ";  MUTATE: MB1 drop " +
      ", ".join(f"{k} {v:.2f}" for k, v in RES["MUTATE"][ft]["MB1_drop"].items()) + f" -> {'bites' if RES['MUTATE'][ft]['MB1'] else 'DOES NOT BITE'}; "
      f"MB2 frozen {'bites' if RES['MUTATE'][ft]['MB2_frozen'] else 'DOES NOT BITE'}, MB2' (A1) {'bites' if RES['MUTATE'][ft]['MB2_A1'] else 'DOES NOT BITE'}")
P("")
for sn in ("Legacy", "DES", "DES_frozen_scan", "KiDS"):
    P(f"{sn} (canonical | alt): gap in widths (p at the target; best sigma8 +- width)")
    for n in RES["rows"]["canonical"]["rows"][sn]:
        P(f"  {n:12s} " + " | ".join((lambda o: f"{o[0]:+.2f} (p {o[1]:.3f}; {o[2]:.4f} +- {o[3]:.4f})")(RES["rows"][ft]["rows"][sn][n]) if n in RES["rows"][ft]["rows"][sn] else "-" for ft in FOOTS))
P("ln det gaps, GATE_BX1 (frozen scans): " + "; ".join(f"{ft} " + ", ".join(f"{sn} {v:+.2f}" for sn, v in RES["rows"][ft]["ln_det_gap_GATE_BX1"].items() if v is not None) for ft in FOOTS))
json.dump(RES, open(os.path.join(HERE, "bx1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "bx1.out"), "w").write("\n".join(OUT) + "\n")
