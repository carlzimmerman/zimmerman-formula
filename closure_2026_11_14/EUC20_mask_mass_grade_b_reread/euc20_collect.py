#!/usr/bin/env python3
"""EUC20 collector.  Frozen criteria: FROZEN_CRITERIA.md (commit cbd14e4ca4).

Reads runs/<lane>/<mode>/ made by euc20_run.py and euc20_bins_results.json made by euc20_bins.py; applies checks
H0-H4 and the twins per source lane; reads the words of G2 (EUC8) and G3 (LNJ1); sets labels; prints the readings.

  python3 -I euc20_collect.py

kappa = 1/2 FITTED.  Footings never pooled.  A re-read: adopts nothing; no outcome is a pass of the lensing gate.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12"); D13 = os.path.join(REPO, "closure_2026_11_13")
SRC = {"euc8": os.path.join(D12, "EUC8_wide_lens_residual_profile"), "euc5a1": os.path.join(D12, "EUC5_dynamical_boost"),
       "lnj1": os.path.join(D13, "LNJ1_joint_switch_on_euclid_lenses")}
FOOT = ("canonical", "alt")
TIMING = re.compile(r"\d+(\.\d+)? s\b|elapsed")
OUT = []
def P(s=""):
    print(s); OUT.append(s)
def rd(lane, mode, name=""): return os.path.join(HERE, "runs", lane, mode, name)
def jl(p): return json.load(open(p))

def h0(lane):
    """f = 1 outputs against the committed files of the same name."""
    drv = jl(rd(lane, "f1", "driver.json")); res = {}
    for fn in drv["redirected_files"]:
        a, b = rd(lane, "f1", fn), os.path.join(SRC[lane], fn)
        if not os.path.exists(b): res[fn] = "no committed file"; continue
        xa, xb = open(a, "rb").read(), open(b, "rb").read()
        if xa == xb: res[fn] = "identical"; continue
        if fn.endswith(".out"):
            la, lb = xa.decode("utf-8", "replace").splitlines(), xb.decode("utf-8", "replace").splitlines()
            d = [(x, y) for x, y in zip(la, lb) if x != y]
            res[fn] = "identical but %d elapsed-time lines" % len(d) if len(la) == len(lb) and all(TIMING.search(x) and TIMING.search(y) for x, y in d) else "DIFFERS"
        else:
            res[fn] = "DIFFERS"
    ok = bool(res) and all(v.startswith("identical") for v in res.values())
    return ok, res


def main():
    P("EUC20 (MASK-APERTURE STELLAR MASS, THIRD RE-READ: THE GRADE-B LANES)   criteria cbd14e4ca4")
    RES = dict(lane="EUC20", criteria_commit="cbd14e4ca4")
    OK = {}
    P("\n[checks]")
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--"] + [os.path.relpath(p, REPO) for p in SRC.values()] +
                        ["closure_2026_11_12/EUC1_eclipse_saturation_ceiling", "closure_2026_11_12/EUC4_wide_lenses", "closure_2026_11_12/EUC6_wide_lens_environment"],
                        capture_output=True, text=True).stdout.splitlines()
    st = [s for s in st if "__pycache__" not in s]
    h1 = len(st) == 0
    P("  %s H1  source folders unchanged in git (bytecode caches aside): %d changed paths" % ("PASS" if h1 else "FAIL", len(st)))
    RES["H1"] = dict(ok=h1, paths=st)
    for lane in ("euc8", "euc5a1", "lnj1"):
        ok0, det = h0(lane)
        P("  %s H0  %-6s f = 1 against the committed files: %s" % ("PASS" if ok0 else "FAIL", lane, "; ".join("%s %s" % kv for kv in sorted(det.items()))))
        drv = {m: jl(rd(lane, m, "driver.json")) for m in ("f1", "primary", "F1a", "F1b", "invert") if os.path.exists(rd(lane, m, "driver.json"))}
        P("       H4  %-6s lenses of sample S without a mask: %d of %d; median log10 f on S (primary) %.3f"
          % (lane, drv["primary"]["S_without_mask"], drv["primary"]["S"], drv["primary"]["median_log10f_S"]))
        OK[lane] = dict(H0=ok0, H0_detail=det, drivers=drv)

    # ---------------------------------------------------------------- EUC8
    ref8 = jl(os.path.join(SRC["euc8"], "euc8_results.json"))
    R8 = {m: jl(rd("euc8", m, "euc8_results.json")) for m in ("primary", "F1a", "F1b", "invert") if os.path.exists(rd("euc8", m, "euc8_results.json"))}
    f8 = {m: sorted(k for k, v in R8[m]["checks"].items() if not v["ok"]) for m in R8}
    h2_8 = all(f8.get(m) == ["K1", "K5"] for m in ("primary", "F1a", "F1b"))
    P("  %s H2  euc8   under the correction exactly K1 and K5 fail: %s" % ("PASS" if h2_8 else "FAIL", "; ".join("%s %s" % (m, ",".join(f8[m])) for m in f8)))
    e17 = jl(os.path.join(D13, "EUC17_mask_aperture_mass_reread", "euc17_A2_results.json"))["reread"]["primary"]["R2 W_B"]["stats"]
    k1 = None
    for line in open(rd("euc8", "primary", "euc8.out"), encoding="utf-8"):
        m = re.search(r"K1 .*: N = (\d+), (\d\.\d+) / (\d\.\d+)", line)
        if m: k1 = (int(m.group(1)), float(m.group(2)), float(m.group(3)))
    h3 = k1 is not None and k1[0] == 124 and abs(k1[1] - e17["S_canonical"]["f25"]) <= 0.001 and abs(k1[2] - e17["S_alt"]["f25"]) <= 0.001
    P("  %s H3  euc8   K1 prints W_B f25 %s under the correction; EUC17's corrected values %.3f / %.3f"
      % ("PASS" if h3 else "FAIL", "%.3f / %.3f" % (k1[1], k1[2]) if k1 else "not found", e17["S_canonical"]["f25"], e17["S_alt"]["f25"]))
    wkey = lambda nm: "W theta_E >= 1.7|%s|far" % nm
    tw8 = "invert" in R8 and all(R8["invert"]["partA"][wkey(nm)]["dM_Msun"][0] > ref8["partA"][wkey(nm)]["dM_Msun"][0] for nm in FOOT)
    P("  %s twin euc8   invert: the far-case excess mass of class W rises on both footings" % ("PASS" if tw8 else "FAIL"))
    ok8 = OK["euc8"]["H0"] and h1 and h2_8 and h3
    OK["euc8"].update(H2=h2_8, H3=h3, twin=tw8, all=ok8)

    # ---------------------------------------------------------------- EUC5 A1
    ref5 = jl(os.path.join(SRC["euc5a1"], "euc5_a1_results.json"))
    R5 = {m: jl(rd("euc5a1", m, "euc5_a1_results.json")) for m in ("primary", "F1a", "F1b", "invert") if os.path.exists(rd("euc5a1", m, "euc5_a1_results.json"))}
    h2_5 = all(R5[m]["F1_pass"] == ref5["F1_pass"] and R5[m]["F2"] == ref5["F2"] and R5[m]["evaluable"] == ref5["evaluable"]
               and R5[m]["N_S"] == ref5["N_S"] and R5[m]["N_P"] == ref5["N_P"] for m in ("primary", "F1a", "F1b") if m in R5) and "primary" in R5
    P("  %s H2  euc5a1 the validation gates and sample sizes keep their committed state (F1 pass %s, evaluable %s, N %d / %d)"
      % ("PASS" if h2_5 else "FAIL", ref5["F1_pass"], ref5["evaluable"], ref5["N_S"], ref5["N_P"]))
    tw5 = "invert" in R5 and all(R5["invert"]["S_S_" + nm]["raw"]["b_med"] > ref5["S_S_" + nm]["raw"]["b_med"] for nm in FOOT)
    P("  %s twin euc5a1 invert: the sample median b_dyn rises on both footings" % ("PASS" if tw5 else "FAIL"))
    ok5 = OK["euc5a1"]["H0"] and h1 and h2_5
    OK["euc5a1"].update(H2=h2_5, twin=tw5, all=ok5)

    # ---------------------------------------------------------------- LNJ1
    refL = jl(os.path.join(SRC["lnj1"], "lnj1.json"))
    RL = {m: jl(rd("lnj1", m, "lnj1.json")) for m in ("primary", "F1a", "F1b") if os.path.exists(rd("lnj1", m, "lnj1.json"))}
    def ka_failed(d): return sorted(k for k, v in d["known_answers"].items() if isinstance(v, dict) and v.get("pass_") is False)
    h2_L = len(RL) == 3 and all(ka_failed(RL[m]) == ["KA1", "KA2"] for m in RL)
    P("  %s H2  lnj1   under the correction exactly KA-1 and KA-2 fail: %s" % ("PASS" if h2_L else "FAIL", "; ".join("%s %s" % (m, ",".join(ka_failed(RL[m]))) for m in RL) or "no run"))
    okL = OK["lnj1"]["H0"] and h1 and h2_L
    OK["lnj1"].update(H2=h2_L, all=okL)
    RES["checks"] = {k: {kk: vv for kk, vv in v.items() if kk != "drivers"} for k, v in OK.items()}

    # ---------------------------------------------------------------- G1 (from the bins script)
    bins = jl(os.path.join(HERE, "euc20_bins_results.json"))
    twb = os.path.exists(os.path.join(HERE, "euc20_bins_MUTATE_invert_results.json")) and jl(os.path.join(HERE, "euc20_bins_MUTATE_invert_results.json")).get("twin_ok")
    P("  %s H0  bins   (from euc20_bins.py);  twin invert: %s" % ("PASS" if bins["H0"] else "FAIL", "PASS" if twb else "FAIL"))

    P("\n[labels, law S]")
    LAB = {}
    for nm in FOOT:
        g = bins["labels_G1"][nm]
        LAB["G1|" + nm] = g
        P("  G1 EUC4 secondary bin %-9s committed %s -> corrected %s: %s, %s%s" % (nm, g["committed"], g["corrected"], g["change"], g["stability"],
                                                                                 (" (" + ", ".join(g["brackets_with_other_word"]) + ")") if g["brackets_with_other_word"] else ""))
    com8 = ref8["verdict"].split(" / ")

    def lane8(fam):
        """EUC8 criteria Part B, the lane word from the family words.  EUC8's own `verdict` field is gated by its
        checks and reads NOT EVALUABLE under the correction (K1 and K5 assert uncorrected numbers, check H2), so
        the frozen rule is applied here to the family words the corrected run produced.  (The first collector
        run read the gated field by mistake; its output is kept as euc20_firstrun.out.)"""
        allowed = any(v == "ALLOWED" for v in fam.values())
        diffuse, conc = fam.get("0.0") == "TOO DIFFUSE", fam.get("T") == "TOO CONCENTRATED"
        if not allowed: return "NO FAMILY FITS"
        if diffuse and conc: return "SLOPE BRACKETED"
        if diffuse: return "RESIDUAL MUST BE CONCENTRATED"
        if conc: return "RESIDUAL MUST BE EXTENDED"
        return "SLOPE NOT CONSTRAINED"

    rule_ok = all(lane8(ref8["family_words"][nm]) == com8[i] for i, nm in enumerate(FOOT))
    P("  %s H5  euc8   the lane-word rule applied to the committed family words returns the committed lane word" % ("PASS" if rule_ok else "FAIL"))
    ok8 = ok8 and rule_ok
    for i, nm in enumerate(FOOT):
        if not ok8: LAB["G2|" + nm] = dict(committed=com8[i], corrected="NOT EVALUABLE"); P("  G2 EUC8 lane word      %-9s committed %s -> NOT EVALUABLE (a check failed)" % (nm, com8[i])); continue
        w = lane8(R8["primary"]["family_words"][nm]); other = [m for m in ("F1a", "F1b") if lane8(R8[m]["family_words"][nm]) != w]
        fam_c, fam_n = ref8["family_words"][nm], R8["primary"]["family_words"][nm]
        famdiff = {k: (fam_c[k], fam_n[k]) for k in fam_c if fam_c[k] != fam_n.get(k)}
        LAB["G2|" + nm] = dict(committed=com8[i], corrected=w, change="UNCHANGED" if w == com8[i] else "CHANGED", stability="FRAGILE" if other else "ROBUST",
                               brackets_with_other_word=other, family_words=fam_n, family_words_changed=famdiff)
        P("  G2 EUC8 lane word      %-9s committed %s -> corrected %s: %s, %s%s" % (nm, com8[i], w, LAB["G2|" + nm]["change"], LAB["G2|" + nm]["stability"],
                                                                                 (" (" + ", ".join(other) + ")") if other else ""))
        P("       family words: %s%s" % ("; ".join("%s %s" % kv for kv in fam_n.items()),
                                          ("   CHANGED: " + "; ".join("%s %s -> %s" % (k, v[0], v[1]) for k, v in famdiff.items())) if famdiff else "   (all as committed)"))
    for nm in FOOT:
        com = refL["foot"][nm]["word"]
        if not okL: LAB["G3|" + nm] = dict(committed=com, corrected="NOT EVALUABLE"); P("  G3 LNJ1 word           %-9s committed %s -> NOT EVALUABLE (a check failed)" % (nm, com)); continue
        wd = lambda d: d["foot"][nm]["primary_raw"] + (", FRAGILE" if d["foot"][nm]["flips"] else "")
        w = wd(RL["primary"]); other = [m for m in ("F1a", "F1b") if wd(RL[m]) != w]
        LAB["G3|" + nm] = dict(committed=com, corrected=w, change="UNCHANGED" if w == com else "CHANGED", stability="FRAGILE" if other else "ROBUST",
                               brackets_with_other_word=other, detail=RL["primary"]["foot"][nm]["primary_detail"], bracket_words=RL["primary"]["foot"][nm]["bracket_words"])
        cr, pr = refL["foot"][nm], RL["primary"]["foot"][nm]
        P("  G3 LNJ1 word           %-9s committed %s -> corrected %s: %s, %s%s   (%s; lenses above the boundary, model rule: P %s -> %s, grade B %s -> %s)"
          % (nm, com, w, LAB["G3|" + nm]["change"], LAB["G3|" + nm]["stability"], (" (" + ", ".join(other) + ")") if other else "", pr["primary_detail"],
             cr["P_only"].get("N_above"), pr["P_only"].get("N_above"), cr["B_only"].get("N_above"), pr["B_only"].get("N_above")))
    RES["labels"] = LAB

    # ---------------------------------------------------------------- readings
    P("\n[reading: EUC8 Part A, share of the lensing mass not supplied by law S and the stars, median [16-84 %]: committed -> corrected]")
    PA = {}
    if ok8:
        for case in ("far", "central"):
            for nm in FOOT:
                for cls in ("W theta_E >= 1.7", "1.3 - 1.7", "1.0 - 1.3", "below 1.0"):
                    k = "%s|%s|%s" % (cls, nm, case); c, n_ = ref8["partA"][k], R8["primary"]["partA"][k]
                    PA[k] = dict(committed=dict(share=c["share"], dM=c["dM_Msun"], need=c["frac_need"]), corrected=dict(share=n_["share"], dM=n_["dM_Msun"], need=n_["frac_need"]))
                    P("  %-8s %-9s %-17s N %4d  share %.3f [%.3f, %.3f] -> %.3f [%.3f, %.3f];  excess %.2e -> %.2e Msun;  lenses needing more %.3f -> %.3f"
                      % (case, nm, cls, c["N"], c["share"][0], c["share"][1], c["share"][2], n_["share"][0], n_["share"][1], n_["share"][2],
                         c["dM_Msun"][0], n_["dM_Msun"][0], c["frac_need"], n_["frac_need"]))
    RES["EUC8_partA"] = PA
    P("\n[reading: EUC5 under A1 (word NOT EVALUABLE on its dispersion-recovery gate, before and after)]")
    if ok5:
        for nm in FOOT:
            c, n_ = ref5["S_S_" + nm]["raw"], R5["primary"]["S_S_" + nm]["raw"]; cp, np_ = ref5["P_S_" + nm]["raw"], R5["primary"]["P_S_" + nm]["raw"]
            dc, dn = ref5["dyn_minus_binf_%s_raw" % nm], R5["primary"]["dyn_minus_binf_%s_raw" % nm]
            P("  %-9s b_dyn median, raw: sample S (N %d) %+.3f -> %+.3f; sample P (N %d) %+.3f -> %+.3f;  dynamics minus lensing bound %+.3f [%+.3f, %+.3f] -> %+.3f [%+.3f, %+.3f]"
              % (nm, c["N"], c["b_med"], n_["b_med"], cp["N"], cp["b_med"], np_["b_med"], dc["med"], dc["lo"], dc["hi"], dn["med"], dn["lo"], dn["hi"]))
        P("  by Einstein radius (alt, raw b_dyn; source-free lensing bound): " + "; ".join(
            "%s N %d: %+.3f -> %+.3f (bound %+.3f -> %+.3f)" % (k, v["N"], v["raw"], R5["primary"]["by_thetaE"][k]["raw"], v["binf"], R5["primary"]["by_thetaE"][k]["binf"])
            for k, v in ref5["by_thetaE"].items()))
        RES["EUC5_A1"] = dict(committed={k: ref5[k] for k in ref5 if k.startswith(("S_S_", "P_S_", "dyn_minus", "by_thetaE"))},
                              corrected={k: R5["primary"][k] for k in R5["primary"] if k.startswith(("S_S_", "P_S_", "dyn_minus", "by_thetaE"))})
    if "EUC6_reading" in bins:
        e = bins["EUC6_reading"]
        P("\n[reading: EUC6, from euc20_bins.py]")
        P("  %d pairs; wide minus control log mass: catalogue %+.3f -> corrected %+.3f dex [%+.3f, %+.3f]; controls' richness-mass slope %+.2f per dex [%+.2f, %+.2f];"
          % (e["pairs"], e["mass_diff_catalogue"], e["mass_diff_corrected"], e["mass_diff_ci"][0], e["mass_diff_ci"][1], e["slope"], e["slope_ci"][0], e["slope_ci"][1]))
        P("  worth %+.2f galaxies [%+.2f, %+.2f] against EUC6's paired excess of %+.2f" % (e["worth"], e["worth_ci"][0], e["worth_ci"][1], e["median_D"]))
    allok = ok8 and ok5 and okL and bins["H0"]
    P("\nchecks: euc8 %s, euc5a1 %s, lnj1 %s, bins %s;  twins: euc8 %s, euc5a1 %s, bins %s"
      % (ok8, ok5, okL, bins["H0"], "exit 1 and bite" if tw8 else "FAILED", "exit 1 and bite" if tw5 else "FAILED", "exits 1" if twb else "FAILED"))
    RES["all_checks_pass"] = bool(allok)
    json.dump(RES, open(os.path.join(HERE, "euc20_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "euc20.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 2)


if __name__ == "__main__":
    main()
