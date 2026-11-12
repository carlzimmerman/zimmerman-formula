#!/usr/bin/env python3
"""EUC10 (PUBLISHED SOURCE REDSHIFTS): grade EUC1-F and EUC5-F on source redshifts already published by others.
Frozen criteria: FROZEN_CRITERIA.md (commit 21578af22b).  EUC1's machinery is imported, not rewritten.

  python3 -I euc10.py --data-dir <dir with the two ECLIPSE csv files>
  EUC10_MUTATE=newton python3 -I euc10.py --data-dir <dir>      (must exit 1)

Inputs in this folder: euc10_matches.csv (matched published source redshifts, with provenance),
euc10_null.json (shifted-position null counts), euc10_partB_samples.csv (Part B samples).
kappa = 1/2 FITTED.  Footings never pooled.  One-sided: no outcome favours the framework.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

MUT = (os.environ.get("EUC10_MUTATE", "") or "").strip()
FOOT = dict(E.FOOT)
if MUT == "newton":
    FOOT = {k: 1.0e-30 for k in FOOT}
SEED = 20261112
HOLD, FAIL = 0.15, 0.25
BANDS = {"theta_E < 1.0": {"canonical": (-0.19, 0.22), "alt": (-0.19, 0.21)},
         "1.0 - 1.3": {"canonical": (-0.05, 0.30), "alt": (-0.06, 0.34)},
         "theta_E >= 1.3": {"canonical": (0.03, 0.32), "alt": (0.03, 0.31)}}
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def stats(b):
    return E.stats(np.asarray(b, float), np.random.default_rng(SEED))

def gate_word(st):
    if st["N"] < 10: return "NOT EVALUABLE"
    if st["b_med_hi"] <= HOLD: return "LENS GATE HOLDS"
    if st["b_med_lo"] >= FAIL: return "LENS GATE FAILS"
    return "NO VERDICT"

def band_word(st, band):
    if st["N"] < 10: return "NOT GRADED"
    if st["b_med_lo"] > band[1]: return "LENSING EXCEEDS DYNAMICS"
    if st["b_med_hi"] < band[0]: return "LENSING BELOW DYNAMICS"
    return "LENSING EQUALS DYNAMICS"

def fmtb(st):
    if st["N"] == 0: return "N = 0"
    return "N=%3d  b_med = %+.3f [%+.3f, %+.3f]  f25 = %.2f" % (st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], st["f25"])

def load_slacs():
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    L = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        r = l.split("\t")
        if len(r) < len(hdr): continue
        d = dict(zl=E.fl(r[col["zlens"]]), zs=E.fl(r[col["zsrc"]]), RE=E.fl(r[col["RE"]]), lME=E.fl(r[col["Mass"]]),
                 Fs=E.fl(r[col["Fs"]]), Fc=E.fl(r[col["Fc"]]), ReV=E.fl(r[col["Re(V)"]]))
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0: L.append(d)
    return L

def b_true(sel, zs, law="S", use_spec=False, guard=0.2):
    """b at the true source redshift for rows `sel` (EUC1 rows) with source redshifts zs; drop z_l >= z_s - guard."""
    zs = np.asarray(zs, float)
    zl = E.arr(sel, "z"); lm = E.arr(sel, "lm")
    if use_spec:
        zsp = np.array([r["zspec"] if np.isfinite(r["zspec"]) and r["zspec"] > 0 else np.nan for r in sel])
        has = np.isfinite(zsp)
        lm = np.where(has, lm + 2.0 * np.log10(E.EUCLID.DL(np.where(has, zsp, zl)) / E.EUCLID.DL(zl)), lm)
        zl = np.where(has, zsp, zl)
    keep = zl < zs - guard
    out = {"dropped": [r["id"] for r, k in zip(sel, keep) if not k]}
    sel2 = [r for r, k in zip(sel, keep) if k]
    if not sel2:
        return out, sel2, {nm: np.array([]) for nm in FOOT}
    eng, z, RE, _, _, _ = E.build(sel2, z=zl[keep], lm=lm[keep])
    bs = {nm: E.run_b(eng, z, RE, zs[keep], a0, law) for nm, a0 in FOOT.items()}
    return out, sel2, bs

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); args = ap.parse_args()
    t0 = time.time(); tag = "euc10" + ("_MUTATE_" + MUT if MUT else "")
    RES = dict(lane="EUC10", criteria_commit="21578af22b", mutate=MUT, footings=FOOT)
    P("EUC10 (PUBLISHED SOURCE REDSHIFTS)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e" % (FOOT["canonical"], FOOT["alt"]))
    P("\n[data]")
    rows, nobj = E.load(args.data_dir)
    Pm, _ = E.select(rows, ("A",)); Sm, _ = E.select(rows, ("A", "B"))
    byid = {r["id"]: r for r in rows}
    inP = {r["id"] for r in Pm}; inS = {r["id"] for r in Sm}
    valid = {r["id"] for r in rows if r["tE"] > 0 and r["te"] > 0 and 0.6 <= r["n"] <= 10 and r["z"] > 0 and r["lm"] > 0}
    P("  P = %d, S = %d (EUC1 select)" % (len(Pm), len(Sm)))

    # ------------------------------------------------------------ matches
    M = list(csv.DictReader(open(os.path.join(HERE, "euc10_matches.csv"), newline="")))
    used = [m for m in M if m["status"] == "USED"]
    P("  published source-redshift rows: %d; used %d (excluded %d: %s)"
      % (len(M), len(used), len(M) - len(used), "; ".join("%s %s" % (m["eclipse_id"], m["status"]) for m in M if m["status"] != "USED")))
    zs_of = {m["eclipse_id"]: float(m["z_s"]) for m in used}
    prov = {m["eclipse_id"]: m["provisional"] == "Y" for m in used}
    RES["matched"] = dict(all=len(used), in_key_valid=sum(1 for i in zs_of if i in valid),
                          S=sum(1 for i in zs_of if i in inS), P=sum(1 for i in zs_of if i in inP))
    P("  used, by set: all %d; with valid EUC1 inputs %d; in S %d; in P %d; PROVISIONAL %d"
      % (len(zs_of), RES["matched"]["in_key_valid"], RES["matched"]["S"], RES["matched"]["P"], sum(prov.values())))

    # ------------------------------------------------------------ checks
    P("\n[known answers and checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-4s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    if not MUT:
        engP, zP, REP, _, _, _ = E.build(Pm)
        k4 = [float(np.median(E.run_b(engP, zP, REP, E.ZS_INF, FOOT[nm], "S"))) for nm in ("canonical", "alt")]
        ck("KA4", "EUC1 reproduced: N(P) = 3192, source-free b_med -0.019 / -0.044 to 0.001", "N = %d, %+.4f / %+.4f" % (len(Pm), *k4),
           len(Pm) == 3192 and abs(k4[0] + 0.019) <= 0.001 and abs(k4[1] + 0.044) <= 0.001)
        SL = load_slacs()
        zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL])
        REs = np.array([d["RE"] for d in SL]) * E.KPC
        Res = np.array([d["ReV"] for d in SL]) * E.ARCSEC * E.AUGER.DA(zl)
        Ms = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(REs, Res, 4.0) * E.MSUN
        engS = E.Engine(REs, Res, np.full(len(SL), 4.0), Ms)
        k1 = [float(np.median(engS.solve_b(math.pi * REs ** 2 * E.AUGER.sigcr(zl, zs), FOOT[nm], "S"))) for nm in ("canonical", "alt")]
        ck("KA1", "SLACS through EUC1's K5 path: b_med +0.082 / +0.070 to 0.003 (N = %d)" % len(SL), "%+.4f / %+.4f" % tuple(k1),
           abs(k1[0] - 0.082) <= 0.003 and abs(k1[1] - 0.070) <= 0.003)
        ar = byid["EUCL-DR1-L015763"]; zsp = ar["zspec"]
        lma = ar["lm"] + 2.0 * math.log10(float(E.EUCLID.DL(zsp)) / float(E.EUCLID.DL(ar["z"])))
        enga, za, REa, _, _, _ = E.build([ar], z=np.array([zsp]), lm=np.array([lma]))
        anc = [float(E.run_b(enga, za, REa, 1.3657, FOOT[nm], "S")[0]) for nm in ("canonical", "alt")]
        ck("KA2", "L015763 at z_l(DESI), z_s = 1.3657: b = +0.231 / +0.215 to 0.002 (x %.2f / %.2f Salpeter)" % (10 ** anc[0], 10 ** anc[1]),
           "%+.4f / %+.4f" % tuple(anc), abs(anc[0] - 0.231) <= 0.002 and abs(anc[1] - 0.215) <= 0.002)
        got = [m for m in M if m["eclipse_id"] == "EUCL-DR1-L015763"]
        ck("KA3", "cross-match returns z_s ~ 1.366 for L015763 (Bergamini+ Table 1)",
           "; ".join("%s from %s" % (m["z_s"], m["source"]) for m in got) or "not found",
           any(abs(float(m["z_s"]) - 1.366) < 0.002 for m in got))
        NL = json.load(open(os.path.join(HERE, "euc10_null.json")))
        lim = max(2.0, 0.1 * NL["real_accepted"])
        ck("NULL", "shifted positions (+0.3 deg Dec): accepted <= max(2, 10%% of real %d) = %.1f" % (NL["real_accepted"], lim),
           "%d accepted (literature %d, NED %d)" % (NL["shifted_accepted"], NL["shifted_lit"], NL["shifted_ned"]), NL["shifted_accepted"] <= lim)

    # ------------------------------------------------------------ gates
    P("\n[EUC1-F: sample P, law S, true source redshift, z_l = ECLIPSE photo-z, drop z_l >= z_s - 0.2]")
    GATE = {}
    for lab, keepprov in (("without PROVISIONAL (the word)", False), ("with PROVISIONAL", True)):
        sel = [r for r in Pm if r["id"] in zs_of and (keepprov or not prov[r["id"]])]
        d, sel2, bs = b_true(sel, [zs_of[r["id"]] for r in sel])
        g = {}
        for nm in FOOT:
            st = stats(bs[nm]) if len(bs[nm]) else dict(N=0); st["word"] = gate_word(st) if st["N"] else "NOT EVALUABLE"
            st["ids"] = [r["id"] for r in sel2]; st["b"] = [float(x) for x in bs[nm]]; st["dropped"] = d["dropped"]; g[nm] = st
            P("  %-32s %-9s %s  dropped %d  -> %s" % (lab, nm, fmtb(st), len(d["dropped"]), st["word"]))
        GATE["noprov" if not keepprov else "withprov"] = g
    RES["EUC1F"] = GATE
    verdict = "%s / %s" % (GATE["noprov"]["canonical"]["word"], GATE["noprov"]["alt"]["word"])
    P("  EUC1-F (canonical / alt): %s" % verdict); RES["EUC1F_word"] = verdict

    P("\n[EUC5-F: sample S, law S, class medians by theta_E (effective Einstein radius)]")
    F5 = {}
    selS = [r for r in Sm if r["id"] in zs_of and not prov[r["id"]]]
    d, selS2, bS = b_true(selS, [zs_of[r["id"]] for r in selS])
    tE = E.arr(selS2, "tE") if selS2 else np.array([])
    for cls, m in (("theta_E < 1.0", tE < 1.0), ("1.0 - 1.3", (tE >= 1.0) & (tE < 1.3)), ("theta_E >= 1.3", tE >= 1.3)):
        for nm in FOOT:
            b = bS[nm][m] if len(tE) else np.array([])
            st = stats(b) if len(b) else dict(N=0)
            st["word"] = band_word(st, BANDS[cls][nm]) if st["N"] else "NOT GRADED"; F5["%s_%s" % (cls, nm)] = st
            P("  %-15s %-9s band [%+.2f, %+.2f]  %s  -> %s" % (cls, nm, *BANDS[cls][nm], fmtb(st), st["word"]))
    RES["EUC5F"] = F5

    # ------------------------------------------------------------ readings
    P("\n[readings, NOT gates]")
    RD = {}
    def reading(name, sel, law="S", use_spec=False, guard=0.2):
        d, sel2, bs = b_true(sel, [zs_of[r["id"]] for r in sel], law, use_spec, guard)
        RD[name] = {}
        for nm in FOOT:
            st = stats(bs[nm]) if len(bs[nm]) else dict(N=0); st["dropped"] = len(d["dropped"]); RD[name][nm] = st
            P("  %-44s %-9s %s  dropped %d" % (name, nm, fmtb(st), len(d["dropped"])))
        return sel2, bs
    allsel = [r for r in rows if r["id"] in zs_of and r["id"] in valid and not prov[r["id"]] and r["grade"] in ("A", "B")]
    reading("S (A+B, EUC1 cuts), law S", selS)
    am, abs_ = reading("all matched with valid inputs, law S", allsel)
    reading("S, law B", selS, law="B")
    reading("P at DESI deflector z (guard 0.05)", [r for r in Pm if r["id"] in zs_of and not prov[r["id"]]], use_spec=True, guard=0.05)
    reading("S at DESI deflector z (guard 0.05)", selS, use_spec=True, guard=0.05)
    RES["readings"] = RD

    P("\n[matched lenses against P: medians]")
    def med(sel, k): return float(np.median(E.arr(sel, k))) if sel else float("nan")
    cmp = {}
    for lab, sel in (("P (3192)", Pm), ("S matched", selS2), ("all matched valid", am)):
        if not sel: continue
        c = dict(N=len(sel), theta_E=med(sel, "tE"), z_l=med(sel, "z"), logM=med(sel, "lm"), n=med(sel, "n"),
                 tE_over_te=float(np.median(E.arr(sel, "tE") / E.arr(sel, "te"))))
        cmp[lab] = c
        P("  %-18s N=%4d theta_E %.2f\"  z_l %.3f  log M* %.2f  n %.2f  theta_E/theta_e %.2f" % (lab, c["N"], c["theta_E"], c["z_l"], c["logM"], c["n"], c["tE_over_te"]))
    RES["compare"] = cmp

    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc10_results.json")))
        key = "noprov" if ref["EUC1F"]["noprov"]["canonical"]["N"] else None
        if key:
            cur = {nm: GATE[key][nm]["b_med"] for nm in FOOT}; base = {nm: ref["EUC1F"][key][nm]["b_med"] for nm in FOOT}
        else:
            cur = {nm: RD["all matched with valid inputs, law S"][nm]["b_med"] for nm in FOOT}
            base = {nm: ref["readings"]["all matched with valid inputs, law S"][nm]["b_med"] for nm in FOOT}
        up = all(cur[nm] > base[nm] for nm in FOOT)
        P("\n[MUTATE %s] b_med %s: canonical %+.3f (ref %+.3f), alt %+.3f (ref %+.3f) -> %s"
          % (MUT, "P matched" if key else "all matched", cur["canonical"], base["canonical"], cur["alt"], base["alt"],
             "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        RES["mutate_rose"] = bool(up)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if up else 2)

    # ------------------------------------------------------------ Part B (NOT A GATE)
    P("\n[Part B: population reading, NOT A GATE, never EUC1-F: P with source redshifts drawn from published samples]")
    SB = list(csv.DictReader(open(os.path.join(HERE, "euc10_partB_samples.csv"), newline="")))
    engP, zP, REP, _, _, _ = E.build(Pm)
    PB = {}
    for samp in sorted(set(r["sample"] for r in SB)):
        rr = [r for r in SB if r["sample"] == samp]
        if len(rr) < 20:
            P("  %-10s N = %d < 20: not used" % (samp, len(rr))); continue
        zl_s = np.array([float(r["z_l"]) for r in rr]); zs_s = np.array([float(r["z_s"]) for r in rr])
        hasT = sum(1 for r in rr if r["theta_E"]) >= 0.8 * len(rr)
        rng = np.random.default_rng(SEED)
        nn = np.argsort(np.abs(zP[:, None] - zl_s[None, :]) / 0.1, axis=1)[:, :10]
        meds = {nm: [] for nm in FOOT}; ndrop = []
        for it in range(200):
            zs_d = np.full(len(Pm), np.nan)
            for t in range(20):
                need = ~np.isfinite(zs_d)
                if not need.any(): break
                pick = zs_s[nn[need, rng.integers(0, 10, need.sum())]]
                ok = pick > zP[need] + 0.2
                idx = np.where(need)[0][ok]; zs_d[idx] = pick[ok]
            keep = np.isfinite(zs_d); ndrop.append(int((~keep).sum()))
            for nm, a0 in FOOT.items():
                b = engP.solve_b(math.pi * REP ** 2 * E.EUCLID.sigcr(zP, np.where(keep, zs_d, zP + 5.0)), a0, "S")
                meds[nm].append(float(np.median(b[keep])))
        PB[samp] = dict(N=len(rr), matched_on="z_l and theta_E" if hasT else "z_l only", z_s_median=float(np.median(zs_s)),
                        z_l_median=float(np.median(zl_s)), dropped_mean=float(np.mean(ndrop)))
        for nm in FOOT:
            v = np.array(meds[nm]); PB[samp][nm] = dict(median=float(np.median(v)), lo=float(np.percentile(v, 2.5)), hi=float(np.percentile(v, 97.5)))
            P("  %-10s N=%3d (%s; sample median z_l %.2f, z_s %.2f)  %-9s b_med over 200 draws: %+.3f [%+.3f, %+.3f]  (P lenses dropped per draw %.1f)"
              % (samp, len(rr), PB[samp]["matched_on"], PB[samp]["z_l_median"], PB[samp]["z_s_median"], nm,
                 PB[samp][nm]["median"], PB[samp][nm]["lo"], PB[samp][nm]["hi"], PB[samp]["dropped_mean"]))
    for nm in FOOT:
        v = [PB[s][nm]["median"] for s in PB if not s.startswith("bracket_")]
        if v:
            P("  bracket across samples, %-9s: %+.3f to %+.3f" % (nm, min(v), max(v)))
            PB["bracket_" + nm] = [min(v), max(v)]
    RES["partB"] = PB

    # ------------------------------------------------------------ outputs
    with open(os.path.join(HERE, "euc10_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["eclipse_id", "grade", "in_P", "in_S", "z_l_photo", "z_l_desi", "z_s", "theta_E", "log_Mstar", "b_S_canonical", "b_S_alt", "provisional"])
        d, sel2, bs = b_true(allsel, [zs_of[r["id"]] for r in allsel])
        bid = {r["id"]: (bs["canonical"][i], bs["alt"][i]) for i, r in enumerate(sel2)}
        for i in sorted(zs_of):
            r = byid.get(i)
            if r is None:
                w.writerow([i, "", "", "", "", "", zs_of[i], "", "", "", "", "Y" if prov[i] else ""]); continue
            bb = bid.get(i)
            w.writerow([i, r["grade"], int(i in inP), int(i in inS), "%.3f" % r["z"] if r["z"] > 0 else "",
                        "%.4f" % r["zspec"] if np.isfinite(r["zspec"]) else "", zs_of[i], "%.3f" % r["tE"] if r["tE"] > 0 else "",
                        "%.3f" % r["lm"] if r["lm"] > 0 else "", "%.4f" % bb[0] if bb else "", "%.4f" % bb[1] if bb else "",
                        "Y" if prov[i] else ""])
    allok = all(v["ok"] for v in CK.values())
    RES["checks"] = CK; RES["checks_all_pass"] = allok
    P("\n[summary]")
    P("  checks: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  EUC1-F (canonical / alt): %s" % (verdict if allok else "NOT EVALUABLE"))
    P("  EUC5-F by class (canonical / alt): %s" % "; ".join("%s: %s / %s" % (c, F5[c + "_canonical"]["word"], F5[c + "_alt"]["word"]) for c in BANDS))
    P("  kappa = 1/2 FITTED. One-sided: no outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
