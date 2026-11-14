#!/usr/bin/env python3
"""EUC21 collector.  Frozen criteria: FROZEN_CRITERIA.md (commit 33778cb9a6).

Reads runs/<mode>/ made by euc21_run.py; applies checks H0-H4 and the twin; applies ESZ1's own rules to the family
words (Y1) and to the Part C words (Y2) that the corrected run produced; sets labels; prints the readings.

  python3 -I euc21_collect.py --data-dir <dir with the two ECLIPSE csv files>

kappa = 1/2 FITTED.  Footings never pooled.  A re-read: adopts nothing; no outcome is a pass.
"""
import argparse, csv, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
SRC = os.path.join(D12, "ESZ1_wide_lens_gas_pressure")
TABLES = [os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
          os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
import euc1 as E          # noqa: E402
FOOT = ("canonical", "alt"); FAMS = ("B30", "B100", "G2")
TIMING = re.compile(r"\d+(\.\d+)? s\b|elapsed")
OUT = []
def P(s=""):
    print(s); OUT.append(s)
def rd(mode, name): return os.path.join(HERE, "runs", mode, name)
def jl(p): return json.load(open(p))

def lane(g, nm):
    """ESZ1 criteria Part G, the lane word of one footing from the family words of one stack (N >= 100)."""
    fw = {f: g["fam"]["%s|%s" % (nm, f)]["word"] for f in FAMS}
    if g["N"] < 100: return "NOT EVALUABLE"
    if all(fw[f] == "EXCLUDED" for f in FAMS): return "HOT GAS DOES NOT SUPPLY THE WIDE LENSES"
    if fw["B30"] == "EXCLUDED" and fw["B100"] == "EXCLUDED": return "ONLY A CUSP IS LEFT"
    if fw["B30"] == "ALLOWED" or fw["B100"] == "ALLOWED": return "HOT GAS NOT EXCLUDED"
    return "NO VERDICT"

def y1(d, nm):
    w = lane(d["partG"]["primary"], nm)
    moved = [b for b, g in d["partG"]["brackets"].items() if lane(g, nm) != w]
    return w + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and w != "NOT EVALUABLE" else "")

def y2(d):
    c0, c1 = d["partC"]["primary"]["word"], d["partC"]["cib"]["word"]
    return c0 + (" [BRACKET-DEPENDENT: CIB-deprojected map]" if c1 != c0 and c0 != "NOT EVALUABLE" else "")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    P("EUC21 (MASK-APERTURE STELLAR MASS, FOURTH RE-READ: THE GAS LANE ESZ1)   criteria 33778cb9a6")
    ref = jl(os.path.join(SRC, "esz1_results.json")); RES = dict(lane="EUC21", criteria_commit="33778cb9a6")
    modes = [m for m in ("primary", "F1a", "F1b", "invert") if os.path.exists(rd(m, "esz1_results.json"))]
    RUN = {m: jl(rd(m, "esz1_results.json")) for m in modes}
    P("\n[checks]")
    # H0
    det = {}
    for fn in ("esz1_results.json", "esz1_per_lens.csv", "esz1.out"):
        xa, xb = open(rd("f1", fn), "rb").read(), open(os.path.join(SRC, fn), "rb").read()
        if xa == xb: det[fn] = "identical"; continue
        la, lb = xa.decode("utf-8", "replace").splitlines(), xb.decode("utf-8", "replace").splitlines()
        d = [(x, y) for x, y in zip(la, lb) if x != y]
        det[fn] = ("identical but %d elapsed-time lines" % len(d)) if fn.endswith(".out") and len(la) == len(lb) and all(TIMING.search(x) and TIMING.search(y) for x, y in d) else "DIFFERS (%d lines)" % len(d)
    h0 = all(v.startswith("identical") for v in det.values())
    P("  %s H0  f = 1 with the substitution in place against ESZ1's committed files: %s" % ("PASS" if h0 else "FAIL", "; ".join("%s %s" % kv for kv in det.items())))
    # H1
    st = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--", "closure_2026_11_12/ESZ1_wide_lens_gas_pressure", "closure_2026_11_12/EUC1_eclipse_saturation_ceiling",
                         "closure_2026_11_12/EUC4_wide_lenses", "closure_2026_11_12/EUC8_wide_lens_residual_profile", "closure_2026_11_12/EUC5_dynamical_boost"],
                        capture_output=True, text=True).stdout.splitlines()
    st = [s for s in st if "__pycache__" not in s]; h1 = len(st) == 0
    P("  %s H1  source folders unchanged in git (bytecode caches aside): %d changed paths" % ("PASS" if h1 else "FAIL", len(st)))
    # H2
    fl = {m: sorted(k for k, v in RUN[m]["checks"].items() if not v["ok"]) for m in modes}
    h2 = all(fl.get(m) == ["K6", "K7"] for m in ("primary", "F1a", "F1b")) and all(len(RUN[m]["checks"]) == len(ref["checks"]) for m in ("primary", "F1a", "F1b") if m in RUN)
    P("  %s H2  under the correction exactly K6 and K7 fail: %s" % ("PASS" if h2 else "FAIL", "; ".join("%s %s" % (m, ",".join(fl[m])) for m in fl)))
    # H3
    R = {}
    for t in TABLES:
        for r in csv.DictReader(open(t, newline="")):
            if r["has_mask"] == "1": R[r["unique_identifier"]] = float(r["mask_radius_arcsec"])
    rows, _ = E.load(a.data_dir); E.OUT.clear(); byid = {r["id"]: r for r in rows}
    c = {r["unique_identifier"]: float(r["log_Mstar"]) for r in csv.DictReader(open(os.path.join(SRC, "esz1_per_lens.csv")))}
    n_ = {r["unique_identifier"]: float(r["log_Mstar"]) for r in csv.DictReader(open(rd("primary", "esz1_per_lens.csv")))} if "primary" in modes else {}
    worst, nchk = 0.0, 0
    for i, lm in n_.items():
        if i in c and i in R:
            lf = math.log10(float(E.M2D_frac(R[i], byid[i]["te"], byid[i]["n"]))); worst = max(worst, abs((lm - c[i]) + lf)); nchk += 1
    h3 = nchk > 0 and nchk == len(c) and worst <= 0.001
    P("  %s H3  per-lens log mass, corrected minus committed, equals -log10 f on %d of %d lenses: largest difference %.1e (1e-3)" % ("PASS" if h3 else "FAIL", nchk, len(c), worst))
    # H4
    def same(x, y): return abs(x - y) <= 1e-9 * max(abs(x), abs(y), 1e-30)
    h4 = "primary" in RUN and all(RUN[m]["partG"]["primary"]["N"] == ref["partG"]["primary"]["N"] and same(RUN[m]["partG"]["primary"]["meas"], ref["partG"]["primary"]["meas"])
                                   and same(RUN[m]["partG"]["primary"]["sigma"], ref["partG"]["primary"]["sigma"])
                                   and same(RUN[m]["partG"]["brackets"]["CIB-deprojected map"]["meas"], ref["partG"]["brackets"]["CIB-deprojected map"]["meas"]) for m in modes)
    g0 = ref["partG"]["primary"]
    P("  %s H4  the measured stack of the wide lenses is the committed one in every run: N %d, %+.3f +- %.3f (1e-6 arcmin^2)" % ("PASS" if h4 else "FAIL", g0["N"], 1e6 * g0["meas"], 1e6 * g0["sigma"]))
    # H5 rules reproduce the committed words
    h5 = all(y1(ref, nm) == ref["partG"]["word"][nm] for nm in FOOT) and y2(ref) == ref["partC"]["word"]
    P("  %s H5  ESZ1's rules applied to the committed family and Part C words return the committed words" % ("PASS" if h5 else "FAIL"))
    twc = open(rd("invert", "exit_code.txt")).read().strip() if os.path.exists(rd("invert", "exit_code.txt")) else "?"
    tw = "invert" in RUN and all(RUN["invert"]["partG"]["primary"]["fam"]["%s|B100" % nm]["pred_min"] > g0["fam"]["%s|B100" % nm]["pred_min"] for nm in FOOT) and twc == "1"
    P("  %s twin invert: the least predicted stack of B100 rises on both footings; driver exit %s" % ("PASS" if tw else "FAIL", twc))
    ok = h0 and h1 and h2 and h3 and h4 and h5
    RES["checks"] = dict(H0=h0, H0_detail=det, H1=h1, H2=h2, H2_failed=fl, H3=h3, H3_worst=worst, H4=h4, H5=h5, twin=tw, all=ok)

    P("\n[Part G, least predicted stack against the measurement (1e-6 arcmin^2): committed -> corrected (primary f)]")
    FAMT = {}
    if "primary" in RUN:
        for nm in FOOT:
            for f in FAMS:
                k = "%s|%s" % (nm, f); cc, nn = g0["fam"][k], RUN["primary"]["partG"]["primary"]["fam"][k]
                FAMT[k] = dict(committed=cc, corrected=nn, F1a=RUN["F1a"]["partG"]["primary"]["fam"][k] if "F1a" in RUN else None, F1b=RUN["F1b"]["partG"]["primary"]["fam"][k] if "F1b" in RUN else None)
                P("  %-9s %-4s pred_min %7.2f -> %7.2f   (pred - meas) / sigma %6.1f -> %6.1f   f_T %.3f -> %.3f   %s -> %s%s"
                  % (nm, f, 1e6 * cc["pred_min"], 1e6 * nn["pred_min"], cc["z_excl"], nn["z_excl"], cc["f_T"], nn["f_T"], cc["word"], nn["word"],
                     "   [F1a %.2f %s; F1b %.2f %s]" % (1e6 * FAMT[k]["F1a"]["pred_min"], FAMT[k]["F1a"]["word"], 1e6 * FAMT[k]["F1b"]["pred_min"], FAMT[k]["F1b"]["word"]) if FAMT[k]["F1a"] and FAMT[k]["F1b"] else ""))
    RES["families"] = FAMT
    P("\n[Part C, wide lenses minus matched controls (1e-6 arcmin^2): committed -> corrected]")
    PC = {}
    for key, lab in (("primary", "primary map"), ("cib", "CIB-deprojected map")):
        cc = ref["partC"][key]; s = "  %-20s N %d  %+.2f [%+.2f, %+.2f] %s" % (lab, cc["N"], 1e6 * cc["mean"], 1e6 * cc["lo"], 1e6 * cc["hi"], cc["word"])
        PC[key] = dict(committed=cc)
        for m in ("primary", "F1a", "F1b"):
            if m in RUN:
                nn = RUN[m]["partC"][key]; PC[key][m] = nn
                s += "  ->  %s: N %d  %+.2f [%+.2f, %+.2f] %s" % (m, nn["N"], 1e6 * nn["mean"], 1e6 * nn["lo"], 1e6 * nn["hi"], nn["word"])
        P(s)
    RES["partC"] = PC

    P("\n[labels]")
    LAB = {}
    for nm in FOOT:
        com = ref["partG"]["word"][nm]
        if not ok or "primary" not in RUN: LAB["Y1|" + nm] = dict(committed=com, corrected="NOT EVALUABLE"); P("  Y1 Part G lane word %-9s committed %s -> NOT EVALUABLE (a check failed)" % (nm, com)); continue
        w = y1(RUN["primary"], nm); other = [m for m in ("F1a", "F1b") if y1(RUN[m], nm) != w]
        LAB["Y1|" + nm] = dict(committed=com, corrected=w, change="UNCHANGED" if w == com else "CHANGED", stability="FRAGILE" if other else "ROBUST", brackets_with_other_word=other,
                               esz1_brackets={b: lane(g, nm) for b, g in RUN["primary"]["partG"]["brackets"].items()})
        P("  Y1 Part G lane word %-9s committed %s -> corrected %s: %s, %s%s" % (nm, com, w, LAB["Y1|" + nm]["change"], LAB["Y1|" + nm]["stability"], (" (" + ", ".join(other) + ")") if other else ""))
        P("       in ESZ1's five brackets: " + "; ".join("%s: %s" % kv for kv in LAB["Y1|" + nm]["esz1_brackets"].items()))
    com = ref["partC"]["word"]
    if not ok or "primary" not in RUN: LAB["Y2"] = dict(committed=com, corrected="NOT EVALUABLE"); P("  Y2 Part C word committed %s -> NOT EVALUABLE (a check failed)" % com)
    else:
        w = y2(RUN["primary"]); other = [m for m in ("F1a", "F1b") if y2(RUN[m]) != w]
        LAB["Y2"] = dict(committed=com, corrected=w, change="UNCHANGED" if w == com else "CHANGED", stability="FRAGILE" if other else "ROBUST", brackets_with_other_word=other)
        P("  Y2 Part C word      committed %s -> corrected %s: %s, %s%s" % (com, w, LAB["Y2"]["change"], LAB["Y2"]["stability"], (" (" + ", ".join(other) + ")") if other else ""))
    RES["labels"] = LAB
    P("\nchecks H0-H5 all pass: %s;  twin: %s" % (ok, "exits 1 and bites" if tw else "FAILED"))
    json.dump(RES, open(os.path.join(HERE, "euc21_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "euc21.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
