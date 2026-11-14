#!/usr/bin/env python3
"""EUC21R collector (blind re-grade of EUC21).  Applies ESZ1's word rules (re-implemented here, not imported) to the
runs written by euc21r_run.py, runs the frozen checks H0-H4 and the twin, and writes euc21r_results.json and
euc21r_collect.out.

  python3 -I euc21r_collect.py

kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import csv, json, math, os, re, sys
import numpy as np
from scipy.special import gammainc

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", ".."))
ESZ1_DIR = os.path.join(REPO, "closure_2026_11_12", "ESZ1_wide_lens_gas_pressure")
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
MASKS = [os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread", "euc17_masks.csv"),
         os.path.join(REPO, "closure_2026_11_14", "EUC19_grade_b_mask_table", "euc19_masks.csv")]
RUNS = os.path.join(HERE, "runs")
FAMS = ("B30", "B100", "G2")
FOOTS = ("canonical", "alt")
BRK = ("CIB-deprojected map", "theta_d 1.5 arcmin", "theta_d 3.0 arcmin", "grade A only", "z_l <= 0.6 only")
NE = "NOT EVALUABLE"
COMMITTED = {"Y1": {"canonical": "ONLY A CUSP IS LEFT", "alt": "ONLY A CUSP IS LEFT"},
             "Y2": {"canonical": "NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map]",
                    "alt": "NO EXCESS DETECTED [BRACKET-DEPENDENT: CIB-deprojected map]"}}
OUT = []
def P(s=""):
    print(s); OUT.append(s)


# ------------------------------------------------------------------ ESZ1's rules, written here
def fam_word(meas, sig, pmin):
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in (meas, sig, pmin)): return "NO POWER"
    if pmin < 3.0 * sig: return "NO POWER"
    if meas + 2.0 * sig < pmin: return "EXCLUDED"
    return "ALLOWED"

def lane_word(fw, n, ok):
    if not ok or n < 100: return NE
    if all(fw[f] == "EXCLUDED" for f in FAMS): return "HOT GAS DOES NOT SUPPLY THE WIDE LENSES"
    if fw["B30"] == "EXCLUDED" and fw["B100"] == "EXCLUDED": return "ONLY A CUSP IS LEFT"
    if fw["B30"] == "ALLOWED" or fw["B100"] == "ALLOWED": return "HOT GAS NOT EXCLUDED"
    return "NO VERDICT"

def fam_words(block, nm, recompute=False):
    if recompute:
        return {f: fam_word(block["meas"], block["sigma"], block["fam"]["%s|%s" % (nm, f)]["pred_min"]) for f in FAMS}
    return {f: block["fam"]["%s|%s" % (nm, f)]["word"] for f in FAMS}

def y1(res, ok):
    """Part G lane word per footing, with the bracket tag; input = the family words the run produced."""
    out, detail = {}, {}
    G0 = res["partG"]["primary"]
    for nm in FOOTS:
        fw = fam_words(G0, nm); base = lane_word(fw, G0["N"], ok); moved = []; bw = {}
        for k in BRK:
            b = res["partG"]["brackets"][k]; bw[k] = lane_word(fam_words(b, nm), b["N"], ok)
            if bw[k] != base: moved.append(k)
        out[nm] = base + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and base != NE else "")
        detail[nm] = dict(base=base, family_words=fw, bracket_words=bw,
                          family_words_recomputed_agree=all(fam_words(G0, nm, True) == fw for _ in [0]) and
                          all(fam_words(res["partG"]["brackets"][k], nm, True) == fam_words(res["partG"]["brackets"][k], nm) for k in BRK))
    return out, detail

def y2(res, ok):
    C0, C1 = res["partC"]["primary"], res["partC"]["cib"]
    if not ok: w = NE
    else: w = C0["word"] + (" [BRACKET-DEPENDENT: CIB-deprojected map]" if C1["word"] != C0["word"] and C0["word"] != NE else "")
    return {nm: w for nm in FOOTS}, dict(primary=C0, cib=C1)

def untag(w): return w.split(" [")[0]


# ------------------------------------------------------------------ own f, for H3
def b_ser(n):
    return 7.669249934 if n == 4.0 else 2.0 * n - 1.0 / 3.0 + 4.0 / (405.0 * n) + 46.0 / (25515.0 * n * n)
def share(R, Re, n):
    return float(gammainc(2.0 * n, b_ser(n) * (R / Re) ** (1.0 / n)))
def own_f(rescale):
    rad = {}
    for path in MASKS:
        for r in csv.DictReader(open(path, newline="")):
            try: R = float(r["mask_radius_arcsec"])
            except Exception: continue
            if r["has_mask"].strip() == "1" and math.isfinite(R) and R > 0 and r["unique_identifier"] not in rad:
                rad[r["unique_identifier"]] = R
    f = {}
    for r in csv.DictReader(open(os.path.join(DATA, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8")):
        uid = r["unique_identifier"]
        if uid not in rad: continue
        try: te, n = float(r["eclipse_effective_radius"]), float(r["eclipse_sersic_index"])
        except Exception: continue
        f[uid] = share(rad[uid], te * rescale, n)
    return f


def per_lens(path):
    return {r["unique_identifier"]: r for r in csv.DictReader(open(path, newline=""))}

def load_run(mode):
    d = os.path.join(RUNS, mode)
    out = dict(mode=mode, dir=d)
    for k, fn in (("res", "esz1_results.json"), ("drv", "driver.json")):
        p = os.path.join(d, fn); out[k] = json.load(open(p)) if os.path.exists(p) else None
    p = os.path.join(d, "esz1_per_lens.csv"); out["pl"] = per_lens(p) if os.path.exists(p) else None
    p = os.path.join(d, "esz1.out"); out["log"] = open(p).read() if os.path.exists(p) else None
    return out


def rel_eq(a, b, tol=1e-9):
    return a == b or (math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol * max(abs(a), abs(b)))

ELAPSED = re.compile(r"\(\s*\d+(\.\d+)?\s*s\)|run time|elapsed", re.I)


def main():
    R = dict(lane="EUC21R", criteria="closure_2026_11_14/EUC21_mask_mass_gas_lane_reread/FROZEN_CRITERIA.md")
    P("EUC21R COLLECTOR (blind re-grade of EUC21: ESZ1 on the mask-aperture stellar mass)")
    P("kappa = 1/2 FITTED; footings graded separately, never pooled.  Units: 1e-6 arcmin^2 (integrated y, 2' compensated aperture).")
    cres = json.load(open(os.path.join(ESZ1_DIR, "esz1_results.json")))
    cpl = per_lens(os.path.join(ESZ1_DIR, "esz1_per_lens.csv"))

    # ---------------------------------------------------------------- R0 rule self-test on the committed file
    P("\n[R0 rule self-test: these rules on ESZ1's committed results file]")
    w1, d1 = y1(cres, True); w2, _ = y2(cres, True)
    r0 = all(w1[nm] == cres["partG"]["word"][nm] for nm in FOOTS) and all(w2[nm] == cres["partC"]["word"] for nm in FOOTS) \
        and all(d1[nm]["family_words_recomputed_agree"] for nm in FOOTS)
    for nm in FOOTS:
        P("  %-9s Y1 %s (committed %s);  Y2 %s (committed %s)" % (nm, w1[nm], cres["partG"]["word"][nm], w2[nm], cres["partC"]["word"]))
    P("  R0 %s" % ("PASS" if r0 else "FAIL: the collector does not reproduce the committed words; nothing is graded"))
    R["R0"] = r0

    runs = {m: load_run(m) for m in ("harness", "corrected", "F1a", "F1b", "invert")}
    for m, r in runs.items():
        if r["drv"] is None: P("  run %s has no driver record" % m)

    # ---------------------------------------------------------------- H0 harness
    P("\n[H0 harness: f = 1 with the substitution in place]")
    h = runs["harness"]; H0 = dict()
    H0["source_exit_0"] = bool(h["drv"] and h["drv"].get("source_exit") == 0)
    H0["results_bytes_equal"] = open(os.path.join(ESZ1_DIR, "esz1_results.json"), "rb").read() == open(os.path.join(h["dir"], "esz1_results.json"), "rb").read() \
        if os.path.exists(os.path.join(h["dir"], "esz1_results.json")) else False
    H0["per_lens_bytes_equal"] = open(os.path.join(ESZ1_DIR, "esz1_per_lens.csv"), "rb").read() == open(os.path.join(h["dir"], "esz1_per_lens.csv"), "rb").read() \
        if os.path.exists(os.path.join(h["dir"], "esz1_per_lens.csv")) else False
    cl = open(os.path.join(ESZ1_DIR, "esz1.out")).read().split("\n"); hl = (h["log"] or "").split("\n")
    keep = lambda L: [x for x in L if not ELAPSED.search(x)]
    H0["log_lines_equal"] = keep(cl) == keep(hl); H0["log_lines_excluded_for_elapsed_time"] = len(cl) - len(keep(cl))
    so = open(os.path.join(h["dir"], "stdout.txt")).read().split("\n") if os.path.exists(os.path.join(h["dir"], "stdout.txt")) else []
    H0["stdout_equals_log"] = keep([x for x in so if x != ""]) == keep([x for x in cl if x != ""])
    if not H0["log_lines_equal"]:
        diffs = [(i, a, b) for i, (a, b) in enumerate(zip(keep(cl), keep(hl))) if a != b][:5]
        H0["first_log_differences"] = diffs
        for i, a, b in diffs: P("    line %d:\n      committed: %s\n      harness:   %s" % (i, a, b))
    H0["ok"] = H0["source_exit_0"] and H0["results_bytes_equal"] and H0["per_lens_bytes_equal"] and H0["log_lines_equal"]
    for k, v in H0.items(): P("  %-40s %s" % (k, v))
    R["H0"] = H0

    # ---------------------------------------------------------------- per corrected-type run: H1-H4
    fown = {m: own_f(s) for m, s in (("corrected", 1.0), ("F1a", 0.80), ("F1b", 1.25))}
    fown["invert"] = fown["corrected"]
    sgn = {"corrected": -1, "F1a": -1, "F1b": -1, "invert": +1}
    WORDS, CHK = {}, {}
    for m in ("harness", "corrected", "F1a", "F1b", "invert"):
        r = runs[m]; c = dict()
        c["H1"] = bool(r["drv"] and r["drv"].get("H1_ok"))
        if m == "harness":
            CHK[m] = c; continue
        res = r["res"]
        if res is None:
            c["error"] = "no results file"; CHK[m] = c; continue
        ck = res.get("checks", {})
        c["K_ok"] = {k: v["ok"] for k, v in ck.items()}
        c["H2"] = (set(ck) == {"K%d" % i for i in range(1, 10)} and not ck["K6"]["ok"] and not ck["K7"]["ok"]
                   and all(ck["K%d" % i]["ok"] for i in (1, 2, 3, 4, 5, 8, 9)))
        # H3
        worst, nlens, nmiss = 0.0, 0, 0
        for uid, row in r["pl"].items():
            fl = fown[m].get(uid)
            if fl is None or uid not in cpl: nmiss += 1; continue
            d = float(row["log_Mstar"]) - float(cpl[uid]["log_Mstar"]); want = sgn[m] * math.log10(fl)
            worst = max(worst, abs(d - want)); nlens += 1
        c["H3"] = bool(nmiss == 0 and nlens == len(cpl) and worst <= 0.001)
        c["H3_detail"] = dict(lenses=nlens, without_f=nmiss, worst_abs_diff=worst)
        # H4
        sw, cw = res["stack_W"], cres["stack_W"]; gp, cgp = res["partG"]["primary"], cres["partG"]["primary"]
        b, cb = res["partG"]["brackets"]["CIB-deprojected map"], cres["partG"]["brackets"]["CIB-deprojected map"]
        h4 = [sw["N"] == cw["N"], rel_eq(sw["mean"], cw["mean"]), rel_eq(sw["sigma"], cw["sigma"]),
              gp["N"] == cgp["N"], rel_eq(gp["meas"], cgp["meas"]), rel_eq(gp["sigma"], cgp["sigma"]),
              b["N"] == cb["N"], rel_eq(b["meas"], cb["meas"]), rel_eq(b["sigma"], cb["sigma"])]
        c["H4"] = all(h4)
        c["H4_detail"] = dict(primary=[sw["N"], sw["mean"], sw["sigma"]], cib=[b["N"], b["meas"], b["sigma"]],
                              max_rel=max(abs(x / y - 1.0) for x, y in ((sw["mean"], cw["mean"]), (sw["sigma"], cw["sigma"]), (b["meas"], cb["meas"]), (b["sigma"], cb["sigma"]))))
        c["driver"] = dict(source_exit=r["drv"].get("source_exit"), driver_exit=r["drv"].get("driver_exit"), S_without_mask=len(r["drv"].get("S_without_mask", [])),
                           S_bad_f=len(r["drv"].get("S_bad_f", [])), mask_conflicts=len(r["drv"]["mask_table"]["conflicts"]), substitution_count=r["drv"].get("substitution_count"))
        CHK[m] = c

    P("\n[H1 source folders untouched after every run; H2 right checks fail; H3 shift arrives; H4 measurement unmoved]")
    for m, c in CHK.items():
        P("  %-9s %s" % (m, json.dumps({k: v for k, v in c.items() if k not in ("K_ok",)}, default=str)))
    corr = CHK.get("corrected", {})
    H1all = all(CHK[m]["H1"] for m in CHK)
    ok_corr = bool(R["R0"] and H0["ok"] and H1all and corr.get("H2") and corr.get("H3") and corr.get("H4"))
    R["checks"] = CHK; R["H1_all_runs"] = H1all; R["checks_ok_for_words"] = ok_corr
    P("  H0 %s, H1 (all runs) %s, H2 %s, H3 %s, H4 %s  ->  checks for the words: %s"
      % (H0["ok"], H1all, corr.get("H2"), corr.get("H3"), corr.get("H4"), "PASS" if ok_corr else "FAIL (Y1, Y2 NOT EVALUABLE)"))

    # ---------------------------------------------------------------- words
    def okfor(m):
        c = CHK.get(m, {})
        return bool(R["R0"] and H0["ok"] and c.get("H1") and c.get("H2") and c.get("H3") and c.get("H4"))
    for m in ("corrected", "F1a", "F1b", "invert"):
        res = runs[m]["res"]
        if res is None: continue
        a, ad = y1(res, okfor(m)); b2, bd = y2(res, okfor(m))
        WORDS[m] = dict(Y1=a, Y1_detail=ad, Y2=b2, Y2_detail=bd, checks_ok=okfor(m))
    R["words"] = WORDS

    P("\n[Part G, corrected run (far source, b* = +0.10); committed in brackets]")
    rc = runs["corrected"]["res"]
    if rc:
        G0, C0 = rc["partG"]["primary"], cres["partG"]["primary"]
        P("  measured %+.3f +- %.3f (N = %d); committed %+.3f +- %.3f (N = %d)" % (1e6 * G0["meas"], 1e6 * G0["sigma"], G0["N"], 1e6 * C0["meas"], 1e6 * C0["sigma"], C0["N"]))
        for nm in FOOTS:
            for f in FAMS:
                a, b = G0["fam"]["%s|%s" % (nm, f)], C0["fam"]["%s|%s" % (nm, f)]
                P("  %-9s %-4s pred_min %9.3f (%9.3f)  (pred - meas)/sigma %7.2f (%7.2f)  f_T %.4f (%.4f)  -> %s (%s)"
                  % (nm, f, 1e6 * a["pred_min"], 1e6 * b["pred_min"], a["z_excl"], b["z_excl"], a["f_T"], b["f_T"], a["word"], b["word"]))
        P("  brackets, corrected run: lane word recomputed per footing (code's own word, which counts K6 and K7, in brackets)")
        for k in BRK:
            bb = rc["partG"]["brackets"][k]
            P("    %-22s N = %3d  %+7.3f +- %.3f  pred_min B30/B100/G2 canonical %8.3f / %8.3f / %7.3f, alt %8.3f / %8.3f / %7.3f  -> %s / %s  (%s / %s)"
              % (k, bb["N"], 1e6 * bb["meas"], 1e6 * bb["sigma"], *[1e6 * bb["fam"]["%s|%s" % (nm, f)]["pred_min"] for nm in FOOTS for f in FAMS],
                 WORDS["corrected"]["Y1_detail"]["canonical"]["bracket_words"][k], WORDS["corrected"]["Y1_detail"]["alt"]["bracket_words"][k], bb["word"]["canonical"], bb["word"]["alt"]))
        P("  code's own lane words (final gate counts K6, K7): %s / %s; Part C %s" % (rc["partG"]["word"]["canonical"], rc["partG"]["word"]["alt"], rc["partC"]["word"]))
        P("\n[log lines of the corrected run that carry the samples and the stack]")
        for x in runs["corrected"]["log"].split("\n"):
            if x.strip().startswith(("W (theta_E", "controls:", "W: N =", "coverage:", "S: lens", "PASS K", "FAIL K")): P("  | " + x.strip())
        P("\n[Part C, corrected run (committed in brackets)]")
        for k in ("primary", "cib"):
            a, b = rc["partC"][k], cres["partC"][k]
            P("  %-8s N = %d  mean %+.3f [%+.3f, %+.3f] -> %s   (%+.3f [%+.3f, %+.3f] -> %s)" % (k, a["N"], 1e6 * a["mean"], 1e6 * a["lo"], 1e6 * a["hi"], a["word"],
              1e6 * b["mean"], 1e6 * b["lo"], 1e6 * b["hi"], b["word"]))

    # ---------------------------------------------------------------- labels
    P("\n[LABELS, per row and footing]")
    LAB = {}
    for row in ("Y1", "Y2"):
        for nm in FOOTS:
            if "corrected" not in WORDS: continue
            w = WORDS["corrected"][row][nm]; com = COMMITTED[row][nm]
            br = {m: WORDS[m][row][nm] for m in ("F1a", "F1b") if m in WORDS}
            lab = dict(word=w, change="UNCHANGED" if w == com else "CHANGED",
                       untagged_change="UNCHANGED" if untag(w) == untag(com) else "CHANGED",
                       robustness=("ROBUSTNESS NOT EVALUABLE (a bracket run is missing)" if len(br) < 2 else
                                   "FRAGILE" if any(v != w for v in br.values()) else "ROBUST"),
                       F1a=br.get("F1a"), F1b=br.get("F1b"), committed=com)
            LAB["%s|%s" % (row, nm)] = lab
            P("  %s %-9s %s ; %s (untagged %s) ; %s   [F1a: %s | F1b: %s]" % (row, nm, w, lab["change"], lab["untagged_change"], lab["robustness"], lab["F1a"], lab["F1b"]))
    R["labels"] = LAB

    # ---------------------------------------------------------------- twin
    P("\n[twin invert: lm + log10 f]")
    tv = runs["invert"]["drv"] or {}
    R["twin"] = dict(bites=tv.get("twin_bites"), driver_exit=tv.get("driver_exit"), B100=tv.get("twin_B100_pred_min_now_vs_committed"))
    if isinstance(R["twin"]["B100"], dict) and "canonical" in R["twin"]["B100"]:
        P("  B100 pred_min now / committed: canonical %.3f / %.3f, alt %.3f / %.3f  -> %s, driver exit %s"
          % (*[1e6 * x for nm in FOOTS for x in R["twin"]["B100"][nm]], "BITES" if R["twin"]["bites"] else "DOES NOT BITE", R["twin"]["driver_exit"]))
    if "invert" in WORDS: P("  twin's words (not graded): Y1 %s / %s; Y2 %s" % (WORDS["invert"]["Y1"]["canonical"], WORDS["invert"]["Y1"]["alt"], WORDS["invert"]["Y2"]["canonical"]))
    for m in ("F1a", "F1b"):
        if m in WORDS: P("  bracket %s words: Y1 %s / %s; Y2 %s" % (m, WORDS[m]["Y1"]["canonical"], WORDS[m]["Y1"]["alt"], WORDS[m]["Y2"]["canonical"]))

    # ---------------------------------------------------------------- reported, no word
    P("\n[reported, no word: model table at theta_d = 2.0' (predicted stack; median gas mass; median kT), corrected (committed)]")
    if rc:
        for nm in FOOTS:
            for f in FAMS:
                for case in ("far", "central", "near"):
                    P("  %-9s %-4s %-7s " % (nm, f, case) + " | ".join("b* %+.2f: %8.2f (%8.2f) %.2e (%.2e) Msun %.2f (%.2f) keV" % (
                        bs, 1e6 * rc["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["stack"][0], 1e6 * cres["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["stack"][0],
                        rc["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["Mg_med"], cres["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["Mg_med"],
                        rc["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["kT_med"], cres["model"]["%s|%s|%s|%+.2f" % (nm, f, case, bs)]["kT_med"]) for bs in (-0.10, 0.0, 0.10)))
        P("\n[Part D as the corrected run's code prints it]")
        lg = runs["corrected"]["log"].split("\n"); i0 = [i for i, x in enumerate(lg) if x.startswith("[Part D")]
        if i0:
            for x in lg[i0[0]:]:
                if x.startswith("checks all pass"): break
                P("  | " + x)
        # -log10 f over S and W
        fc = fown["corrected"]; wl = [u for u, r in cpl.items() if r["is_W"] == "1"]; sl = list(cpl)
        for nm, ids in (("W (valid, theta_E >= 1.7)", wl), ("S (all in the per-lens file)", sl)):
            v = np.array([-math.log10(fc[u]) for u in ids if u in fc])
            P("  -log10 f over %s: N = %d, median %.4f, 16-84 %% [%.4f, %.4f], mean %.4f" % (nm, len(v), np.median(v), *np.percentile(v, [16, 84]), v.mean()))
            R.setdefault("minus_log10_f", {})[nm] = dict(N=int(len(v)), median=float(np.median(v)), p16=float(np.percentile(v, 16)), p84=float(np.percentile(v, 84)), mean=float(v.mean()))
        # controls under the correction
        cpl_c = runs["corrected"]["pl"]
        newc = {r["control_of"]: u for u, r in cpl_c.items() if r["control_of"]}; oldc = {r["control_of"]: u for u, r in cpl.items() if r["control_of"]}
        same = sum(1 for k in oldc if newc.get(k) == oldc[k])
        P("  controls: %d pairs now, %d before; %d of the wide lenses keep the same control" % (len(newc), len(oldc), same))
        R["controls_same"] = same; R["controls_now"] = len(newc)

    json.dump(R, open(os.path.join(HERE, "euc21r_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, "euc21r_collect.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
