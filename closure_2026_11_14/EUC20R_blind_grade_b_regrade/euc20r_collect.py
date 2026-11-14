#!/usr/bin/env python3
"""EUC20R collector: checks H0-H4, the three rows' words and labels, the readings (READING.md sections 3-5).

  python3 -I -B euc20r_collect.py                         -> euc20r_results.json, euc20r.out
  EUC20R_MUTATE=invert python3 -I -B euc20r_collect.py    -> euc20r_MUTATE_invert.json / .out; exits 1 if the twin fires
Reads only this lane's runs/ and the committed (HEAD) files of the source lanes.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import builtins, csv, io, json, math, os, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc20r_common as C

MUT = (os.environ.get("EUC20R_MUTATE", "") or "").strip()
RUNS = os.path.join(HERE, "runs")
FOOTS = ("canonical", "alt")
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def head(relpath):
    r = subprocess.run(["git", "show", "HEAD:" + relpath], cwd=C.REPO, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout

def jload(p):
    with builtins.open(p) as f:
        return json.load(f)

ELAPSED = re.compile(r"elapsed|\(\d+ s\)")
COMMITTED = {"euc8": ("EUC8", ["euc8.out", "euc8_results.json", "euc8_per_lens.csv", "euc8_wide_per_lens.csv"]),
             "euc5a1": ("EUC5", ["euc5_a1.out", "euc5_a1_results.json", "euc5_a1_per_lens.csv"]),
             "lnj1": ("LNJ1", ["lnj1.out", "lnj1.json", "lnj1_per_lens.csv", "lnj1_MUTATE_TWH.json", "lnj1_MUTATE_TWH.out",
                               "lnj1_MUTATE_TWD.json", "lnj1_MUTATE_TWD.out", "lnj1_MUTATE_TWSH.json", "lnj1_MUTATE_TWSH.out"])}

def committed(lane, fn):
    key, _ = COMMITTED[lane]
    return head(C.rel(os.path.join(C.DIRS[key], fn)))

# ------------------------------------------------------------------ words
def euc8_word(fw, nD):
    if nD < 10: return "NOT EVALUABLE"
    anyok = any(v == "ALLOWED" for v in fw.values()); dif0 = fw["0.0"] == "TOO DIFFUSE"; conT = fw["T"] == "TOO CONCENTRATED"
    if not anyok: return "NO FAMILY FITS"
    if dif0 and conT: return "SLOPE BRACKETED"
    if dif0: return "RESIDUAL MUST BE CONCENTRATED"
    if conT: return "RESIDUAL MUST BE EXTENDED"
    return "SLOPE NOT CONSTRAINED"

def lnj1_word(F):
    prim = F["configs"]["primary"]["final_word"]
    flips = [k for k, v in F["bracket_words"].items() if v != prim]
    return prim + (", FRAGILE" if flips else ""), prim, flips

def euc8_nD(d):
    with builtins.open(os.path.join(d, "euc8_per_lens.csv")) as f:
        rows = list(csv.DictReader(f))
    return sum(float(r["theta_E_arcsec"]) >= 1.3 for r in rows), [r["unique_identifier"] for r in rows if float(r["theta_E_arcsec"]) >= 1.3], [r["unique_identifier"] for r in rows]

# ------------------------------------------------------------------ H0
def h0_route(lane):
    d = os.path.join(RUNS, "f1", lane)
    rep = {}
    _, files = COMMITTED[lane]
    drv = jload(os.path.join(d, "driver.json"))
    written = sorted({os.path.basename(w["written"]) for w in drv["writes"]})
    for fn in sorted(set(files) | set(written)):
        ref = committed(lane, fn); p = os.path.join(d, fn)
        if ref is None or not os.path.exists(p):
            rep[fn] = dict(ok=False, why="missing committed" if ref is None else "not written"); continue
        new = builtins.open(p, "rb").read()
        if fn.endswith(".out"):
            a = [l for l in ref.decode().splitlines() if not ELAPSED.search(l)]
            b = [l for l in new.decode().splitlines() if not ELAPSED.search(l)]
            diff = [i for i in range(max(len(a), len(b))) if (a[i] if i < len(a) else None) != (b[i] if i < len(b) else None)]
            rep[fn] = dict(ok=not diff, lines_compared=len(a), lines_differing=len(diff), first=diff[:3])
        else:
            rep[fn] = dict(ok=new == ref, bytes=len(new))
    return rep, all(v["ok"] for v in rep.values()), drv

def h0_euc4():
    ref = json.loads(head(C.rel(os.path.join(C.DIRS["EUC4"], "euc4_results.json"))))["partA"]
    got = jload(os.path.join(RUNS, "f1", "euc4_bins.json"))["bins"]
    worst_pt, worst_bd, words_ok, n = 0.0, 0.0, True, 0
    for b in ref:
        for k in ("S_canonical", "S_alt", "B_canonical", "B_alt"):
            r, g = ref[b][k], got[b][k]
            for q in ("N", "f25", "f0", "b_med"):
                worst_pt = max(worst_pt, abs(r[q] - g[q])); n += 1
            for q in ("f25_lo", "f25_hi", "f0_lo", "f0_hi", "b_med_lo", "b_med_hi"):
                worst_bd = max(worst_bd, abs(r[q] - g[q]))
            words_ok &= r["word"] == g["word"]
    ok = worst_pt <= 1e-9 and worst_bd <= 0.01 and words_ok
    return dict(points_compared=n, max_point_diff=worst_pt, max_bound_diff=worst_bd, words_identical=words_ok, ok=ok), ok

# ------------------------------------------------------------------ main collector
def main():
    os.chdir(C.REPO)
    masks, minfo = C.load_masks()
    h1 = jload(os.path.join(RUNS, "h1_log.json")) if os.path.exists(os.path.join(RUNS, "h1_log.json")) else []
    if MUT == "invert":
        return twin(h1)
    RES = dict(lane="EUC20R", reading_commit="025dc97b73", criteria="closure_2026_11_14/EUC20_mask_mass_grade_b_reread/FROZEN_CRITERIA.md",
               footings=C.FOOT, mask_tables=minfo, note="blind re-grade; adopts nothing; kappa = 1/2 FITTED; not theory closed")
    P("EUC20R (BLIND RE-GRADE OF EUC20): mask-aperture stellar mass, the grade-B lanes. kappa = 1/2 FITTED; not theory closed.")
    P("mask union: %s" % ", ".join("%s rows %d, with mask %d" % (k, v["rows"], v["with_mask"]) for k, v in minfo.items()))

    # ---------------- H1
    h1_bad = [r for r in h1 if r["porcelain"].strip()]
    h1_ok = bool(h1) and not h1_bad
    RES["H1"] = dict(runs=len(h1), dirty=h1_bad, ok=h1_ok)
    P("\n[H1 source folders untouched] %d runs checked; dirty after: %s -> %s" % (len(h1), [r["run"] for r in h1_bad] or "none", "PASS" if h1_ok else "FAIL"))

    # ---------------- H0
    P("\n[H0 harness, f = 1]")
    H0 = {}
    for lane in ("euc8", "euc5a1", "lnj1"):
        rep, ok, drv = h0_route(lane); H0[lane] = dict(files=rep, ok=ok, exit_code=drv["exit_code"], loader_wrapped=drv.get("loader_wrapped"), substitution_count=drv.get("substitution_count"))
        P("  %-7s %s  (exit %s)" % (lane, "; ".join("%s %s" % (fn, "identical" if v["ok"] else "DIFFERS %s" % {k: v[k] for k in v if k != "ok"}) for fn, v in rep.items()), drv["exit_code"]))
    e4, ok4 = h0_euc4(); H0["euc4_bins"] = e4
    P("  euc4    bins: %d point statistics, max diff %.1e (<= 1e-9); bounds max diff %.1e (<= 0.01); words identical %s -> %s"
      % (e4["points_compared"], e4["max_point_diff"], e4["max_bound_diff"], e4["words_identical"], "PASS" if ok4 else "FAIL"))
    # words rebuilt at f = 1 equal the committed words
    r8 = jload(os.path.join(RUNS, "f1", "euc8", "euc8_results.json")); nD1, Dids, D55 = euc8_nD(os.path.join(RUNS, "f1", "euc8"))
    w8 = {ft: euc8_word(r8["family_words"][ft], nD1) for ft in FOOTS}
    ok8w = all(w8[ft] == "SLOPE NOT CONSTRAINED" for ft in FOOTS)
    rl = jload(os.path.join(RUNS, "f1", "lnj1", "lnj1.json"))
    wl = {ft: lnj1_word(rl["foot"][ft])[0] for ft in FOOTS}
    okLw = wl["canonical"] == "NO POWER, FRAGILE" and wl["alt"] == "NO POWER" and all(wl[ft] == rl["foot"][ft]["word"] for ft in FOOTS)
    H0["euc8"]["word_rebuilt"] = w8; H0["euc8"]["ok"] &= ok8w
    H0["lnj1"]["word_rebuilt"] = wl; H0["lnj1"]["ok"] &= okLw
    P("  rebuilt words at f = 1: G2 %s / %s (%s); G3 %s / %s (%s)" % (w8["canonical"], w8["alt"], "matches" if ok8w else "DIFFERS", wl["canonical"], wl["alt"], "matches" if okLw else "DIFFERS"))
    H0["euc4_bins"]["ok"] = ok4
    RES["H0"] = H0

    # ---------------- H2, H3 (primary run); bracket runs reported
    P("\n[H2 the right checks fail, H3 the shift arrives]")
    H2 = {}
    for mode in ("primary", "F1a", "F1b"):
        c8 = jload(os.path.join(RUNS, mode, "euc8", "euc8_results.json"))["checks"]
        fail8 = sorted(k for k, v in c8.items() if not v["ok"])
        cl = jload(os.path.join(RUNS, mode, "lnj1", "lnj1.json"))["known_answers"]
        failL = sorted(k for k, v in cl.items() if isinstance(v, dict) and "pass_" in v and not v["pass_"])
        H2[mode] = dict(euc8_failing=fail8, euc8_ok=fail8 == ["K1", "K5"], lnj1_failing=failL, lnj1_ok=failL == ["KA1", "KA2"],
                        euc8_K1=c8["K1"]["value"], lnj1_KA1=cl["KA1"]["value"], lnj1_KA2=cl["KA2"]["value"])
    ra1c = json.loads(head(C.rel(os.path.join(C.DIRS["EUC5"], "euc5_a1_results.json"))))
    ra1p = jload(os.path.join(RUNS, "primary", "euc5a1", "euc5_a1_results.json"))
    a1_ok = (ra1p["F1_pass"] == ra1c["F1_pass"] and ra1p["F2"] == ra1c["F2"] and ra1p["N_P"] == ra1c["N_P"] and ra1p["N_S"] == ra1c["N_S"]
             and ra1p["evaluable"] == ra1c["evaluable"])
    H2["primary"]["euc5a1_ok"] = bool(a1_ok)
    H2["primary"]["euc5a1_state"] = dict(F1_pass=ra1p["F1_pass"], N_P=ra1p["N_P"], N_S=ra1p["N_S"], evaluable=ra1p["evaluable"], F2_unchanged=ra1p["F2"] == ra1c["F2"])
    for mode in ("primary", "F1a", "F1b"):
        h = H2[mode]
        P("  %-7s EUC8 failing %s (%s); LNJ1 failing %s (%s)%s" % (mode, h["euc8_failing"], "as required" if h["euc8_ok"] else "NOT as required",
          h["lnj1_failing"], "as required" if h["lnj1_ok"] else "NOT as required",
          ("; EUC5 A1 states unchanged (F1 %s, N(P) %d, N(S) %d): %s" % ("pass" if ra1p["F1_pass"] else "FAIL", ra1p["N_P"], ra1p["N_S"], "yes" if a1_ok else "NO")) if mode == "primary" else ""))
    m = re.findall(r"(\d+\.\d+)", H2["primary"]["euc8_K1"])
    k1v = [float(x) for x in m[-2:]] if len(m) >= 2 else [float("nan")] * 2
    h3_ok = abs(k1v[0] - 0.444) <= 0.001 + 1e-12 and abs(k1v[1] - 0.379) <= 0.001 + 1e-12
    RES["H2"] = H2; RES["H3"] = dict(K1_line=H2["primary"]["euc8_K1"], values=k1v, ok=bool(h3_ok))
    P("  H3 EUC8 K1 under the correction: %s -> 0.444 / 0.379 to 0.001: %s" % (H2["primary"]["euc8_K1"], "PASS" if h3_ok else "FAIL"))

    # ---------------- H4
    P("\n[H4 mask coverage]")
    cov = jload(os.path.join(RUNS, "coverage.json"))
    def cv(ids):
        miss = [i for i in ids if i not in masks]; return dict(N=len(ids), without=len(miss), frac_without=len(miss) / len(ids) if ids else float("nan"), ids_without=miss)
    H4 = dict(G1=dict(N=cov["secondary"]["N"], without=cov["secondary"]["without"], frac_without=cov["secondary"]["frac_without"]),
              G2_D=cv(Dids), G2_all55=cv(D55), G3_S=dict(N=cov["S"]["N"], without=cov["S"]["without"], frac_without=cov["S"]["frac_without"]),
              complement=dict(N=cov["complement"]["N"], without=cov["complement"]["without"]), W_B=dict(N=cov["W_B"]["N"], without=cov["W_B"]["without"]),
              P=dict(N=cov["P"]["N"], without=cov["P"]["without"]), grade_B=dict(N=cov["grade_B"]["N"], without=cov["grade_B"]["without"]))
    a1ids = [r["unique_identifier"] for r in csv.DictReader(builtins.open(os.path.join(RUNS, "primary", "euc5a1", "euc5_a1_per_lens.csv")))]
    H4["EUC5_A1_55"] = cv(a1ids)
    for k in ("G1", "G2_D", "G3_S"):
        H4[k]["ok"] = bool(H4[k]["frac_without"] <= 0.05)
    RES["H4"] = H4
    for k, v in H4.items():
        P("  %-12s N %5d, without a mask %d%s" % (k, v["N"], v["without"], (" (%.2f %%) -> %s" % (100 * v["frac_without"], "within 5 %" if v["ok"] else "OVER 5 % -> NOT EVALUABLE")) if "ok" in v else ""))

    # ---------------- rows
    P("\n[rows: corrected word; UNCHANGED / CHANGED; FRAGILE / ROBUST from F1a (R_e x 0.80 in f) and F1b (R_e x 1.25)]")
    ref4 = json.loads(head(C.rel(os.path.join(C.DIRS["EUC4"], "euc4_results.json"))))["partA"]
    SEC = "secondary: 1.3 <= theta_E < 1.7"
    bins = {m_: jload(os.path.join(RUNS, m_, "euc4_bins.json"))["bins"] for m_ in C.MODES}
    rows = {}
    g1_valid = H0["euc4_bins"]["ok"] and h1_ok and H4["G1"]["ok"]
    g2_valid = H0["euc8"]["ok"] and h1_ok and H2["primary"]["euc8_ok"] and h3_ok and H4["G2_D"]["ok"]
    g3_valid = H0["lnj1"]["ok"] and h1_ok and H2["primary"]["lnj1_ok"] and H4["G3_S"]["ok"]
    for ft in FOOTS:
        k = "S_" + ft
        w = {m_: bins[m_][SEC][k]["word"] for m_ in ("primary", "F1a", "F1b")}
        rows["G1|" + ft] = dict(committed=ref4[SEC][k]["word"], word=w["primary"] if g1_valid else "NOT EVALUABLE", F1a=w["F1a"], F1b=w["F1b"],
                                 valid=g1_valid, stat=bins["primary"][SEC][k], stat_F1a=bins["F1a"][SEC][k], stat_F1b=bins["F1b"][SEC][k])
        w8m = {}
        for m_ in ("primary", "F1a", "F1b"):
            rr = jload(os.path.join(RUNS, m_, "euc8", "euc8_results.json")); nD, _, _ = euc8_nD(os.path.join(RUNS, m_, "euc8"))
            w8m[m_] = euc8_word(rr["family_words"][ft], nD)
            if m_ == "primary": fw8 = rr["family_words"][ft]; nDp = nD; src8 = rr["verdict"]
        rows["G2|" + ft] = dict(committed="SLOPE NOT CONSTRAINED", word=w8m["primary"] if g2_valid else "NOT EVALUABLE", F1a=w8m["F1a"], F1b=w8m["F1b"],
                                 valid=g2_valid, family_words=fw8, N_D=nDp, source_printed_word=src8)
        wlm = {}
        for m_ in ("primary", "F1a", "F1b"):
            rr = jload(os.path.join(RUNS, m_, "lnj1", "lnj1.json")); wlm[m_] = lnj1_word(rr["foot"][ft])
            if m_ == "primary": FL = rr["foot"][ft]
        rows["G3|" + ft] = dict(committed=("NO POWER, FRAGILE" if ft == "canonical" else "NO POWER"), word=wlm["primary"][0] if g3_valid else "NOT EVALUABLE",
                                 F1a=wlm["F1a"][0], F1b=wlm["F1b"][0], valid=g3_valid, primary_final=wlm["primary"][1], lnj1_flips=wlm["primary"][2],
                                 primary_raw=FL["primary_raw"], primary_detail=FL["primary_detail"], bracket_words=FL["bracket_words"],
                                 source_printed_word=FL["word"], N_above=FL["configs"]["primary"]["main"]["N_above"],
                                 gates=FL["configs"]["primary"]["gates"])
    for key, r in rows.items():
        r["change"] = "UNCHANGED" if r["word"] == r["committed"] else "CHANGED"
        r["fragility"] = "FRAGILE" if (r["F1a"] != r["word"] or r["F1b"] != r["word"]) and r["valid"] else ("ROBUST" if r["valid"] else "-")
        P("  %s %-9s %-40s %-9s %-8s (committed %s; F1a %s; F1b %s)" % (key.split("|")[0], key.split("|")[1], r["word"], r["change"], r["fragility"], r["committed"], r["F1a"], r["F1b"]))
    RES["rows"] = rows

    # ---------------- numbers behind the rows
    P("\n[G1 EUC4 secondary bin (292 grade-B lenses, 1.3 <= theta_E < 1.7), source at infinity; f25 law S]")
    for m_ in ("f1", "primary", "F1a", "F1b"):
        for ft in FOOTS:
            s = bins[m_][SEC]["S_" + ft]
            P("  %-7s %-9s f25 %.3f [%.3f, %.3f]  b_med %+.3f [%+.3f, %+.3f]  -> %s" % (m_, ft, s["f25"], s["f25_lo"], s["f25_hi"], s["b_med"], s["b_med_lo"], s["b_med_hi"], s["word"]))
    mlf = bins["primary"][SEC]["minus_logf"]
    P("  correction -log10 f on the secondary bin (primary share): median %.3f dex, 16-84 %% %.3f to %.3f" % (mlf["median"], mlf["p16"], mlf["p84"]))
    P("  law B beside: " + "; ".join("%s f25 %.3f [%.3f, %.3f] %s" % (ft, bins["primary"][SEC]["B_" + ft]["f25"], bins["primary"][SEC]["B_" + ft]["f25_lo"], bins["primary"][SEC]["B_" + ft]["f25_hi"], bins["primary"][SEC]["B_" + ft]["word"]) for ft in FOOTS))
    P("\n[reported, no word: EUC4's other bins under the correction, law S]")
    for b in ("complement: theta_E < 1.0", "W_B: theta_E >= 1.7 arcsec (primary)"):
        for ft in FOOTS:
            s = bins["primary"][b]["S_" + ft]; c = ref4[b]["S_" + ft]
            P("  %-38s %-9s f25 %.3f [%.3f, %.3f] b_med %+.3f  would-be %s  (committed f25 %.3f, %s)" % (b, ft, s["f25"], s["f25_lo"], s["f25_hi"], s["b_med"], s["word"], c["f25"], c["word"]))
        mlf = bins["primary"][b]["minus_logf"]
        P("  %-38s correction -log10 f: median %.3f dex, 16-84 %% %.3f to %.3f" % ("", mlf["median"], mlf["p16"], mlf["p84"]))
    RES["euc4_bins"] = {m_: bins[m_] for m_ in ("primary", "F1a", "F1b")}

    P("\n[G2 EUC8 Part B family words under the correction (sample D: N %d)]" % rows["G2|canonical"]["N_D"])
    r8p = jload(os.path.join(RUNS, "primary", "euc8", "euc8_results.json")); r8c = json.loads(committed("euc8", "euc8_results.json"))
    for ft in FOOTS:
        P("  %-9s %s" % (ft, ", ".join("%s %s" % (f, r8p["family_words"][ft][f]) for f in ("P", "T", "2.5", "2.0", "1.5", "1.0", "0.0"))))
        P("  %-9s committed: %s" % ("", ", ".join("%s %s" % (f, r8c["family_words"][ft][f]) for f in ("P", "T", "2.5", "2.0", "1.5", "1.0", "0.0"))))
        for f in ("T", "0.0"):
            st = r8p["partB"]["%s|%s" % (ft, f)]["stats"]
            P("    family %-4s d at b* = 0: far %+.3f [%+.3f, %+.3f], near %+.3f [%+.3f, %+.3f]; far upper at b* -0.1/0/+0.1: %+.3f / %+.3f / %+.3f; near lower: %+.3f / %+.3f / %+.3f"
              % (f, st["+0.00|far"]["med"], st["+0.00|far"]["lo_w"], st["+0.00|far"]["hi_w"], st["+0.00|near"]["med"], st["+0.00|near"]["lo_w"], st["+0.00|near"]["hi_w"],
                 st["-0.10|far"]["hi_w"], st["+0.00|far"]["hi_w"], st["+0.10|far"]["hi_w"], st["-0.10|near"]["lo_w"], st["+0.00|near"]["lo_w"], st["+0.10|near"]["lo_w"]))
        gh = r8p.get("gamma_hat", {}).get("theta_E >= 1.3 (D)|" + ft)
        if gh: P("    gamma-hat (D, b* = 0): far %s [%s, %s], central %s [%s, %s], near %s [%s, %s]" % tuple(x for c in ("far", "central", "near") for x in (gh[c]["gamma"], gh[c]["lo"], gh[c]["hi"])))
    P("  source script's own printed lane word under the correction: %s (its checks K1 / K5 fail by design; not this row's word)" % r8p["verdict"])

    P("\n[reported, no word: EUC8 Part A, law S, b_star = 0: fraction needing extra mass; median excess mass [16-84 %]; median share of the lensing mass]")
    PA = {}
    for cn in ("W theta_E >= 1.7", "1.3 - 1.7", "1.0 - 1.3", "below 1.0"):
        for ft in FOOTS:
            for case in ("far", "central"):
                k = "%s|%s|%s" % (cn, ft, case); a, c = r8p["partA"][k], r8c["partA"][k]
                PA[k] = dict(N=a["N"], frac_need=a["frac_need"], dM=a["dM_Msun"], share=a["share"], committed=dict(frac_need=c["frac_need"], dM=c["dM_Msun"], share=c["share"]))
                P("  %-17s %-9s %-7s N %4d  need %.3f (was %.3f)  excess %.2e [%.2e, %.2e] (was %.2e)  share %.3f (was %.3f)"
                  % (cn, ft, case, a["N"], a["frac_need"], c["frac_need"], a["dM_Msun"][0], a["dM_Msun"][1], a["dM_Msun"][2], c["dM_Msun"][0], a["share"][0], c["share"][0]))
    RES["euc8_partA"] = PA

    P("\n[reported, no word: EUC5 under amendment A1, law S, raw | F1-corrected; word stays NOT EVALUABLE (F1 gate)]")
    A1 = {}
    for smp in ("P", "S"):
        for ft in FOOTS:
            k = "%s_S_%s" % (smp, ft); a, c = ra1p[k], ra1c[k]
            A1[k] = dict(raw=a["raw"]["b_med"], corrected=a["corrected"]["b_med"], raw_committed=c["raw"]["b_med"], corrected_committed=c["corrected"]["b_med"],
                         raw_ci=[a["raw"]["b_med_lo"], a["raw"]["b_med_hi"]])
            P("  %s %-9s N %2d  b_dyn raw %+.3f [%+.3f, %+.3f] (was %+.3f) | corrected %+.3f (was %+.3f)" % (smp, ft, a["raw"]["N"], a["raw"]["b_med"], a["raw"]["b_med_lo"], a["raw"]["b_med_hi"], c["raw"]["b_med"], a["corrected"]["b_med"], c["corrected"]["b_med"]))
    for k, v in ra1p["by_thetaE"].items():
        c = ra1c["by_thetaE"][k]
        P("  theta_E %-9s N %2d  b_dyn raw %+.3f / corrected %+.3f, b_inf %+.3f (alt)   [was %+.3f / %+.3f, %+.3f]" % (k, v["N"], v["raw"], v["corr"], v["binf"], c["raw"], c["corr"], c["binf"]))
    for ft in FOOTS:
        for lab in ("raw", "corrected"):
            k = "dyn_minus_binf_%s_%s" % (ft, lab); v, c = ra1p[k], ra1c[k]
            P("  %-9s %-9s median (b_dyn - b_inf) %+.3f [%+.3f, %+.3f], below the lensing bound %.3f   [was %+.3f, %.3f]" % (ft, lab, v["med"], v["lo"], v["hi"], v["below"], c["med"], c["below"]))
    A1["by_thetaE"] = ra1p["by_thetaE"]; A1["dyn_minus_binf"] = {k: ra1p[k] for k in ra1p if k.startswith("dyn_minus_binf")}
    RES["euc5_a1"] = A1

    P("\n[reported, no word: LNJ1 under the correction]")
    for ft in FOOTS:
        r = rows["G3|" + ft]
        P("  %-9s primary raw %s (%s); after its twin gates %s; N(s >= 1) %d; gates %s; bracket words %s; its own printed WORD %s"
          % (ft, r["primary_raw"], r["primary_detail"], r["primary_final"], r["N_above"], r["gates"], r["bracket_words"], r["source_printed_word"]))

    P("\n[reported, no word: EUC6 pairs under the correction]")
    E6 = {}
    for m_ in ("primary", "F1a", "F1b"):
        e = jload(os.path.join(RUNS, m_, "euc6_reading.json")); E6[m_] = e
        P("  %-7s pairs %d (lenses with a mask %d of %d); median d log M* wide - control: corrected %+.4f [%+.4f, %+.4f], catalogued %+.4f; median -log10 f: wide %.3f, control %.3f"
          % (m_, e["pairs"], e["with_mask"], e["lenses"], e["median_dlm_corrected"], e["dlm_corr_lo"], e["dlm_corr_hi"], e["median_dlm_catalogued"], e["median_minus_logf_W"], e["median_minus_logf_C"]))
        P("  %-7s controls' richness-mass slope %.2f [%.2f, %.2f] galaxies per dex (catalogued mass %.2f); worth %+.2f [%+.2f, %+.2f] galaxies = %.0f %% of EUC6's +3.38; one-third line 1.13 -> %s"
          % ("", e["slope_controls_corrected"], e["slope_lo"], e["slope_hi"], e["slope_controls_catalogued"], e["worth"], e["worth_lo"], e["worth_hi"], 100 * e["share_of_excess"],
             "EUC6 NEEDS A RE-MATCHED CONTROL SET" if e["needs_rematch"] else "below the line"))
    P("  EUC6 pair rebuild harness: %s" % E6["primary"]["harness"])
    RES["euc6"] = E6

    allvalid = all(r["valid"] for r in rows.values())
    P("\n[summary] (blind; labels per row and footing)")
    for g in ("G1", "G2", "G3"):
        P("  %s  canonical: %s, %s, %s   |   alt: %s, %s, %s" % (g, *[rows[g + "|canonical"][k] for k in ("word", "change", "fragility")], *[rows[g + "|alt"][k] for k in ("word", "change", "fragility")]))
    P("  checks: H0 %s; H1 %s; H2 %s; H3 %s; H4 %s" % ("pass" if all(H0[k]["ok"] for k in H0) else "FAIL", "pass" if h1_ok else "FAIL",
      "pass" if (H2["primary"]["euc8_ok"] and H2["primary"]["lnj1_ok"] and H2["primary"]["euc5a1_ok"]) else "FAIL", "pass" if h3_ok else "FAIL",
      "pass" if all(H4[k]["ok"] for k in ("G1", "G2_D", "G3_S")) else "FAIL"))
    P("  No outcome is a pass of the lensing gate. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
    RES["all_rows_valid"] = allvalid
    with builtins.open(os.path.join(HERE, "euc20r_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=float)
    with builtins.open(os.path.join(HERE, "euc20r.out"), "w") as f:
        f.write("\n".join(OUT) + "\n")
    sys.exit(0)


def twin(h1):
    P("EUC20R TWIN (mode invert: lm + log10 f; exact shift b - log10 f). Must fire on every item; exit 1.")
    T = {}
    r8i = jload(os.path.join(RUNS, "invert", "euc8", "euc8_results.json")); r8c = json.loads(committed("euc8", "euc8_results.json"))
    for ft in FOOTS:
        k = "W theta_E >= 1.7|%s|far" % ft
        T["euc8_W_far_excess_" + ft] = dict(got=r8i["partA"][k]["dM_Msun"][0], committed=r8c["partA"][k]["dM_Msun"][0])
        T["euc8_W_far_excess_" + ft]["ok"] = T["euc8_W_far_excess_" + ft]["got"] > T["euc8_W_far_excess_" + ft]["committed"]
    a1i = jload(os.path.join(RUNS, "invert", "euc5a1", "euc5_a1_results.json")); a1c = json.loads(committed("euc5a1", "euc5_a1_results.json"))
    for smp in ("P", "S"):
        for ft in FOOTS:
            k = "%s_S_%s" % (smp, ft)
            T["euc5a1_bdyn_raw_" + k] = dict(got=a1i[k]["raw"]["b_med"], committed=a1c[k]["raw"]["b_med"])
            T["euc5a1_bdyn_raw_" + k]["ok"] = T["euc5a1_bdyn_raw_" + k]["got"] > T["euc5a1_bdyn_raw_" + k]["committed"]
    b4 = jload(os.path.join(RUNS, "invert", "euc4_bins.json"))["bins"]; r4 = json.loads(head(C.rel(os.path.join(C.DIRS["EUC4"], "euc4_results.json"))))["partA"]
    SEC = "secondary: 1.3 <= theta_E < 1.7"
    for ft in FOOTS:
        T["G1_f25_" + ft] = dict(got=b4[SEC]["S_" + ft]["f25"], committed=r4[SEC]["S_" + ft]["f25"])
        T["G1_f25_" + ft]["ok"] = T["G1_f25_" + ft]["got"] >= T["G1_f25_" + ft]["committed"]
    h1_ok = bool(h1) and not [r for r in h1 if r["porcelain"].strip()]
    for k, v in T.items():
        P("  %-34s %.6g against committed %.6g -> %s" % (k, v["got"], v["committed"], "as required" if v["ok"] else "DID NOT FIRE"))
    fired = all(v["ok"] for v in T.values())
    P("  source folders untouched after every run: %s" % ("yes" if h1_ok else "NO"))
    P("  twin %s; exit %d. kappa = 1/2 FITTED; not theory closed." % ("fired on every item" if fired else "DID NOT FIRE", 1 if fired else 2))
    with builtins.open(os.path.join(HERE, "euc20r_MUTATE_invert.json"), "w") as f:
        json.dump(dict(items=T, fired=fired, h1_ok=h1_ok), f, indent=1)
    with builtins.open(os.path.join(HERE, "euc20r_MUTATE_invert.out"), "w") as f:
        f.write("\n".join(OUT) + "\n")
    sys.exit(1 if fired else 2)


if __name__ == "__main__":
    main()
