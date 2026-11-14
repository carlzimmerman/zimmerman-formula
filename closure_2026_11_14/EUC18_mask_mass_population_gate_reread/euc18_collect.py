#!/usr/bin/env python3
"""EUC18 collector.  Frozen criteria: FROZEN_CRITERIA.md (commit c8908592a4).

Reads the runs made by euc18_run.py (runs/<mode>/), applies checks H0-H3 and the twin, reads the words of Q1 (the
EUC13-P gate) and Q2 (the f25 statistic) from the gate block EUC13's own code wrote, sets the labels, and computes
the one wordless reading of section 5 (the share of the wide lenses' lensing mass still missing) with its check KW.

  python3 -I euc18_collect.py --data-dir <dir with the two ECLIPSE csv files>

kappa = 1/2 FITTED.  Footings never pooled.  A re-read: adopts nothing; no outcome is a pass of the lensing gate.
"""
import argparse, csv, json, math, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
SRC_DIR = os.path.join(D12, "EUC13_population_source_gate")
EUC17 = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread")
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402

FOOT = ("canonical", "alt")
EXPECT_FAIL = {"KA2", "KA3M1", "KA3M2"}
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def rd(mode, name):
    return os.path.join(HERE, "runs", mode, name)

def ka2(path):
    for line in open(path, encoding="utf-8"):
        m = re.search(r"KA2 .*: N = (\d+), ([+-]\d+\.\d+) / ([+-]\d+\.\d+)", line)
        if m: return int(m.group(1)), float(m.group(2)), float(m.group(3))
    return None

def q3(x):
    return [float(v) for v in np.percentile(x, [50, 16, 84])]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    P("EUC18 (MASK-APERTURE STELLAR MASS, SECOND RE-READ: THE POPULATION GATE)   criteria c8908592a4")
    RES = dict(lane="EUC18", criteria_commit="c8908592a4")
    ref = json.load(open(os.path.join(SRC_DIR, "euc13_results.json")))
    CK = {}
    def ck(name, what, ok, value=None):
        CK[name] = dict(what=what, ok=bool(ok), value=value)
        P("  %s %-3s %s" % ("PASS" if ok else "FAIL", name, what))

    P("\n[checks]")
    # H0 harness
    same_json = open(rd("f1", "euc13_results.json"), "rb").read() == open(os.path.join(SRC_DIR, "euc13_results.json"), "rb").read()
    same_csv = open(rd("f1", "euc13_per_lens.csv"), "rb").read() == open(os.path.join(SRC_DIR, "euc13_per_lens.csv"), "rb").read()
    la = open(rd("f1", "euc13.out"), encoding="utf-8").read().splitlines()
    lb = open(os.path.join(SRC_DIR, "euc13.out"), encoding="utf-8").read().splitlines()
    timing = re.compile(r"\d+(\.\d+)? s\b|elapsed")
    diff = [(x, y) for x, y in zip(la, lb) if x != y]
    out_ok = len(la) == len(lb) and all(timing.search(x) and timing.search(y) for x, y in diff)
    ck("H0", "f = 1 reproduces EUC13's committed outputs: results.json identical %s, per_lens.csv identical %s, euc13.out %d lines, "
             "%d differ, all of them elapsed-time lines %s" % (same_json, same_csv, len(la), len(diff), out_ok),
       same_json and same_csv and out_ok, dict(json=same_json, csv=same_csv, out_lines=len(la), out_diff=len(diff)))
    # H1 source folders untouched
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", "closure_2026_11_12/EUC13_population_source_gate",
                         "closure_2026_11_12/EUC1_eclipse_saturation_ceiling", "closure_2026_11_12/EUC10_published_source_redshifts"],
                        capture_output=True, text=True).stdout.splitlines()
    st = [s for s in st if "__pycache__" not in s]
    ck("H1", "source folders of EUC13, EUC1 and EUC10 unchanged in git (bytecode caches aside): %d changed paths" % len(st), len(st) == 0, st)
    # H2 the right checks fail; H3 the shift arrives
    modes = [m for m in ("primary", "F1a", "F1b") if os.path.exists(rd(m, "euc13_results.json"))]
    RUN = {m: json.load(open(rd(m, "euc13_results.json"))) for m in modes}
    h2 = {}
    for m in modes:
        failed = {k for k, v in RUN[m]["checks"].items() if not v["ok"]}
        h2[m] = dict(failed=sorted(failed), surviving_mu=RUN[m]["M3_surviving_mu"],
                     ok=failed == EXPECT_FAIL and RUN[m]["M3_surviving_mu"] == ref["M3_surviving_mu"]
                     and sorted(RUN[m]["members"]) == sorted(ref["members"]))
    ck("H2", "under the correction exactly KA2 and KA3 (M1, M2) fail and the surviving members are the committed ones: %s"
       % "; ".join("%s failed %s, M3 %s" % (m, ",".join(h2[m]["failed"]), ",".join(h2[m]["surviving_mu"])) for m in modes),
       len(modes) == 3 and all(v["ok"] for v in h2.values()), h2)
    e17 = json.load(open(os.path.join(EUC17, "euc17_A2_results.json")))["reread"]["primary"]["R1"]["stats"]
    k = ka2(rd("primary", "euc13.out")) if "primary" in modes else None
    ok3 = k is not None and k[0] == 3192 and all(abs(k[i + 1] - e17["S_" + nm]["b_med"]) <= 0.001 for i, nm in enumerate(FOOT))
    ck("H3", "source-free b_med on P under the correction %s against EUC17's %+.4f / %+.4f (0.001)"
       % ("%+.4f / %+.4f" % (k[1], k[2]) if k else "not found", e17["S_canonical"]["b_med"], e17["S_alt"]["b_med"]), ok3, k)
    # twin
    tw = json.load(open(rd("invert", "driver.json"))) if os.path.exists(rd("invert", "driver.json")) else None
    twc = open(rd("invert", "exit_code.txt")).read().strip() if os.path.exists(rd("invert", "exit_code.txt")) else "?"
    twin_ok = bool(tw and tw.get("twin_b_med_rises_for_every_member") and tw.get("twin_same_members") and twc == "1")
    P("  %s twin invert: every member's b_med rises on both footings; driver exit %s" % ("PASS" if twin_ok else "FAIL", twc))
    RES["twin_invert"] = dict(ok=twin_ok, exit=twc)
    checks_ok = all(CK[h]["ok"] for h in ("H0", "H1", "H2", "H3"))
    RES["checks"] = CK; RES["checks_all_pass"] = checks_ok

    # ---------------------------------------------------------------- members
    def mem(d, m, nm):
        x = d["members"][m][nm]
        return x["med"], x["f25"], x["z_s_median"]
    P("\n[members on P, law S: committed -> corrected (primary f); b_med and f25 with 95 % intervals]")
    MEM = {}
    for m in ref["members"]:
        for nm in FOOT:
            c = mem(ref, m, nm); row = dict(committed=dict(b_med=c[0], f25=c[1], z_s_median=c[2]))
            s = "  %-13s %-9s b_med %+.3f [%+.3f, %+.3f]  f25 %.3f [%.3f, %.3f]" % (m, nm, c[0]["point"], c[0]["lo"], c[0]["hi"], c[1]["point"], c[1]["lo"], c[1]["hi"])
            for md in modes:
                n_ = mem(RUN[md], m, nm); row[md] = dict(b_med=n_[0], f25=n_[1], z_s_median=n_[2])
            if "primary" in modes:
                n_ = mem(RUN["primary"], m, nm)
                s += "  ->  b_med %+.3f [%+.3f, %+.3f]  f25 %.3f [%.3f, %.3f]" % (n_[0]["point"], n_[0]["lo"], n_[0]["hi"], n_[1]["point"], n_[1]["lo"], n_[1]["hi"])
            MEM["%s|%s" % (m, nm)] = row; P(s)
    RES["members"] = MEM

    # ---------------------------------------------------------------- words and labels
    P("\n[gate block of EUC13's own code: intervals over surviving members (M3 = envelope)]")
    for md in ["committed"] + modes:
        d = ref if md == "committed" else RUN[md]
        for nm in FOOT:
            g = d["gate"][nm]
            P("  %-9s %-9s b_med %s | f25 %s  -> gate %s; f25 statistic %s"
              % (md, nm, "; ".join("%s [%+.3f, %+.3f]" % (mm, x["lo"], x["hi"]) for mm, x in zip(g["members"], g["b_med"])),
                 "; ".join("[%.3f, %.3f]" % (x["lo"], x["hi"]) for x in g["f25"]), g["word"], g["f25_word"]))
    P("\n[labels]")
    LAB = {}
    for row, key in (("Q1 EUC13-P gate", "word"), ("Q2 f25 statistic", "f25_word")):
        LAB[row] = {}
        for nm in FOOT:
            com = ref["gate"][nm][key]
            if not checks_ok or "primary" not in modes:
                LAB[row][nm] = dict(committed=com, corrected="NOT EVALUABLE", change="-", stability="-")
                P("  %-17s %-9s committed %s -> NOT EVALUABLE (a check failed)" % (row, nm, com)); continue
            w = RUN["primary"]["gate"][nm][key]
            other = [md for md in ("F1a", "F1b") if RUN[md]["gate"][nm][key] != w]
            LAB[row][nm] = dict(committed=com, corrected=w, change="UNCHANGED" if w == com else "CHANGED",
                                stability="FRAGILE" if other else "ROBUST", brackets_with_other_word=other)
            P("  %-17s %-9s committed %s -> corrected %s: %s, %s%s" % (row, nm, com, w, LAB[row][nm]["change"], LAB[row][nm]["stability"],
                                                                      (" (" + ", ".join(other) + ")") if other else ""))
    RES["labels"] = LAB
    RES["gate"] = {md: RUN[md]["gate"] for md in modes}
    RES["drivers"] = {md: json.load(open(rd(md, "driver.json"))) for md in ["f1"] + modes if os.path.exists(rd(md, "driver.json"))}

    # ---------------------------------------------------------------- class readings the source code prints
    P("\n[theta_E classes, b_med per member (reported): committed -> corrected]")
    if "primary" in modes:
        for cls in ("theta_E < 1.0", "1.0 - 1.3", "theta_E >= 1.3"):
            for nm in FOOT:
                parts = []
                for m in ref["members"]:
                    c = ref["members"][m][nm]["cls"].get(cls); n_ = RUN["primary"]["members"][m][nm]["cls"].get(cls)
                    if c and n_: parts.append("%s %+.3f -> %+.3f" % (m, c["point"], n_["point"]))
                P("  %-15s %-9s %s" % (cls, nm, "; ".join(parts)))

    # ---------------------------------------------------------------- section 5: W share (wordless, own check KW)
    P("\n[reading: share of the wide lenses' lensing lower bound that law S and the stars do not supply (class W, source at infinity)]")
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Sm, _ = E.select(rows, ("A", "B")); Wm = [r for r in Sm if r["tE"] >= 1.7]
    R = {r["unique_identifier"]: float(r["mask_radius_arcsec"]) for r in csv.DictReader(open(os.path.join(EUC17, "euc17_masks.csv"))) if r["has_mask"] == "1"}
    nomask = [r["id"] for r in Wm if r["id"] not in R]
    lf = np.array([math.log10(float(E.M2D_frac(R[r["id"]], r["te"], r["n"]))) if r["id"] in R else np.nan for r in Wm])
    e8 = json.load(open(os.path.join(D12, "EUC8_wide_lens_residual_profile", "euc8_results.json")))["partA"]
    WS = {}

    def share(lm):
        eng, z, RE, Re, n, _ = E.build(Wm, lm=lm)
        Mt = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF); out = {}
        for nm, a0 in E.FOOT.items():
            base = eng.M2D(1.0, a0, "S"); need = Mt > base; dM = np.where(need, Mt - base, 0.0)
            out[nm] = dict(N=len(Wm), frac_need=float(np.mean(need)), dM_Msun=q3(dM / E.MSUN), share=q3(dM / Mt))
        return out

    before = share(E.arr(Wm, "lm"))
    kw = max(max(abs(before[nm]["share"][0] / e8["W theta_E >= 1.7|%s|far" % nm]["share"][0] - 1.0),
                 abs(before[nm]["dM_Msun"][0] / e8["W theta_E >= 1.7|%s|far" % nm]["dM_Msun"][0] - 1.0)) for nm in FOOT)
    kw_ok = kw <= 0.01 and len(Wm) == e8["W theta_E >= 1.7|canonical|far"]["N"] and not nomask
    P("  %s KW  with f = 1 the medians reproduce EUC8's committed far-case values for W (N %d, %d without a mask): largest relative difference %.1e (1e-2)"
      % ("PASS" if kw_ok else "FAIL", len(Wm), len(nomask), kw))
    WS["KW"] = dict(ok=bool(kw_ok), err=float(kw))
    if kw_ok:
        after = share(E.arr(Wm, "lm") - lf)
        for nm in FOOT:
            b_, a_ = before[nm], after[nm]
            P("  %-9s share %.3f [%.3f, %.3f] -> %.3f [%.3f, %.3f];  excess mass %.2e -> %.2e Msun;  lenses needing more %.3f -> %.3f"
              % (nm, b_["share"][0], b_["share"][1], b_["share"][2], a_["share"][0], a_["share"][1], a_["share"][2],
                 b_["dM_Msun"][0], a_["dM_Msun"][0], b_["frac_need"], a_["frac_need"]))
        WS.update(before=before, after=after, median_correction_dex=float(np.median(-lf)))
        P("  median correction on W: %.3f dex" % np.median(-lf))
    else:
        P("  KW failed: the reading is not reported (Q1 and Q2 are unaffected).")
    RES["W_share"] = WS

    P("\nchecks H0-H3 all pass: %s;  twin: %s" % (checks_ok, "exits 1" if twin_ok else "FAILED"))
    json.dump(RES, open(os.path.join(HERE, "euc18_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "euc18.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if checks_ok else 2)


if __name__ == "__main__":
    main()
