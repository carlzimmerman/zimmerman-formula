#!/usr/bin/env python3
"""EUC11 (DEEP-FIELD LENSES).  Frozen criteria: FROZEN_CRITERIA.md (commit 0a6088cd0a); amendments A1 (63dbb33bb4, footprint),
A2 (650ed9e51b, control annulus 20-100 arcsec) and A3 (a42a20fbca, Part 2 on the lenses whose control candidates were fetched).

Part 1: EUC1's / EUC4's source-free ceiling test on the Q1 lenses of the Euclid Deep Fields (an independent sample).
Part 2: lensed-source redshifts from the DR1 deep grism tables by EUC3's rule, graded by a matched-control null.

Run:
  python3 -I euc11.py --q1-dir <dir with the Q1 lens csv files and deep_tables/> --eclipse-dir <dir with the ECLIPSE csv files and nisp_tables/>
  EUC11_MUTATE=newton  python3 -I euc11.py ...      (must exit 1)
  EUC11_MUTATE=noguard python3 -I euc11.py ...      (must exit 1)
"""
import argparse, collections, csv, hashlib, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
MUT = (os.environ.get("EUC11_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
GUARD = MUT != "noguard"
LHA = 6564.61
GOOD = {211, 212, 213, 251, 252, 253}
SECOND = ("OIII5008", "Hbeta", "SII6718", "SIII9530", "SIII9068", "OII3727")
OWN = ((9071.1, 9071.1), (9533.2, 9533.2), (10833.3, 10941.1), (12821.6, 12821.6))
SHA = {"q1_discovery_engine_lens_catalog.csv": "ee5e60cd507413eabf3da8ffa37a3c527212da00feb29083cf516a86d6f26877",
       "modeling_lens_mass.csv": "f2a52616a1ac65137b34abe0892d251e18e2c60e9a64c459914102f44ec49db5",
       "modeling_lens_sersic.csv": "c0b05783ecfdcb4068c3487db11c7eda18e070f8011726fc17d50a04aecd5dc2",
       "modeling_sersic_magnitude.csv": "7c7506af33f27d65cc618e998cbbb0868c36a106703f303d6b0b0a74240d94f2"}
F5 = {"below 1.0": ((-0.19, 0.22), (-0.19, 0.21)), "1.0 - 1.3": ((-0.05, 0.30), (-0.06, 0.34)), "1.3 and above": ((0.03, 0.32), (0.03, 0.31))}
MPC = 1.0e6 * E.PC
OUT = []
def P(s=""):
    print(s); OUT.append(s)
def fl(v):
    try: return float(v)
    except Exception: return float("nan")
def sep_arcsec(ra1, de1, ra2, de2):
    d1, d2 = math.radians(de1), math.radians(de2)
    x = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin(math.radians(ra2 - ra1) / 2) ** 2
    return math.degrees(2.0 * math.asin(min(1.0, math.sqrt(x)))) * 3600.0
def read_all(tdir, prefix):
    out = []
    for fn in sorted(os.listdir(tdir)):
        if fn.startswith(prefix + "_") and fn.endswith(".csv"):
            with open(os.path.join(tdir, fn), newline="") as f: out += list(csv.DictReader(f))
    return out
def obskey(r): return (r.get("patch_id_list", ""), r.get("calblock_id_list", ""))
def own_line(z, zlo, zup):
    return any((1.0 + zlo) * a / LHA - 1.0 - 0.01 <= z <= (1.0 + zup) * b / LHA - 1.0 + 0.01 for a, b in OWN)

class Spectra:
    def __init__(self, tdir):
        self.qual, self.gal, self.lines = (collections.defaultdict(list) for _ in range(3))
        for r in read_all(tdir, "qual_all"): self.qual[r["object_id"]].append(r)
        for r in read_all(tdir, "gal_all"): self.gal[r["object_id"]].append(r)
        for r in read_all(tdir, "lines_all"): self.lines[r["object_id"]].append(r)
        self.phz = {r["object_id"]: (fl(r["phz_median"]), fl(r["phz_70_int_1"]), fl(r["phz_70_int_2"])) for r in read_all(tdir, "phz_all")}
    def judge(self, ra0, de0, tE, objs, tier):
        """the frozen rule on one system.  objs: MER rows within 3 arcsec."""
        ra_ = min(tE + 0.7, 3.0); cnt = []
        for o in objs:
            d = sep_arcsec(ra0, de0, fl(o["ra"]), fl(o["dec"]))
            if d <= ra_: cnt.append((d, o))
        cnt.sort(key=lambda x: x[0])
        if not cnt or cnt[0][0] > 0.6: return dict(ev=False, why="no lens object")
        loid = cnt[0][1]["object_id"]; pz = self.phz.get(loid)
        if pz is None or not (np.isfinite(pz[1]) and np.isfinite(pz[2]) and pz[2] > 0): return dict(ev=False, why="no redshift interval", loid=loid)
        zlo, zup = pz[1], pz[2]; sec = []; anyspec = False; amb = 0
        for d, o in cnt:
            oid = o["object_id"]; Q = self.qual.get(oid, []); Gs = self.gal.get(oid, []); Ls = self.lines.get(oid, [])
            for q in Q:
                if not (fl(q["spe_npix"]) >= 300 and fl(q["spe_n_dith_med"]) > 3 and int(fl(q["spe_error_flag"])) == 0 and int(fl(q["spe_gal_error_flag"])) == 0): continue
                cs = [c for c in Gs if obskey(c) == obskey(q)] if len(Q) > 1 else Gs
                if cs: anyspec = True
                wmin, wmax = fl(q["spe_w_min"]), fl(q["spe_w_max"])
                for c in cs:
                    rk = int(fl(c["spe_rank"])); z = fl(c["spe_z"])
                    if tier == "A":
                        if rk != 0 or not (fl(c["spe_z_prob"]) >= 0.99 and fl(c["spe_z_rel"]) > 0.05): continue
                    elif rk > 4: continue
                    if not (wmin < LHA * (1.0 + z) < wmax): continue
                    lr = [l for l in Ls if int(fl(l["spe_rank"])) == rk and int(fl(l["spe_line_qual_gf"])) in GOOD and (len(Q) == 1 or obskey(l) == obskey(q))]
                    ha = [fl(l["spe_line_snr_gf"]) for l in lr if l["spe_line_name"] == "Halpha" and fl(l["spe_line_fwhm_gf"]) <= 180.0]
                    if not ha or max(ha) < 5.0: continue
                    two = any(l["spe_line_name"] in SECOND and fl(l["spe_line_snr_gf"]) >= 3.0 for l in lr)
                    if tier == "B" and not two: continue
                    if GUARD and not (z >= zup + 0.15): continue
                    if GUARD and own_line(z, zlo, zup): amb += 1; continue
                    sec.append((max(ha), z, oid == loid, rk, two, oid))
        if not anyspec: return dict(ev=False, why="no spectrum passing Q1", loid=loid)
        if not sec: return dict(ev=True, status="NONE", amb=amb, loid=loid, zl=pz[0], zlo=zlo, zup=zup)
        zs = [s[1] for s in sec]; best = max(sec)
        return dict(ev=True, status="SECURE" if max(zs) - min(zs) <= 0.02 else "CONFLICT", zs=best[1], snr=best[0], on_lens=bool(best[2]), rank=best[3],
                    two=bool(best[4]), oid=best[5], nsec=len(sec), amb=amb, loid=loid, zl=pz[0], zlo=zlo, zup=zup)

def eclipse_pipeline(edir):
    """lens object (nearest wide MER object within 0.6 arcsec), its H flux and pipeline photo-z, for every ECLIPSE system in EUC3's cache."""
    tdir = os.path.join(edir, "nisp_tables"); S = {r["sid"]: r for r in csv.DictReader(open(os.path.join(tdir, "systems.csv")))}
    best = {}
    for pre in ("mer_first", "mer_rest"):
        for m in read_all(tdir, pre):
            s = S.get(m["sid"])
            if s is None: continue
            d = sep_arcsec(fl(s["ra"]), fl(s["dec"]), fl(m["ra"]), fl(m["dec"]))
            if d <= 0.6 and (m["sid"] not in best or d < best[m["sid"]][0]): best[m["sid"]] = (d, m["object_id"], fl(m["flux_h_templfit"]))
    pz = {}
    for pre in ("phz_first", "phz_rest"):
        for r in read_all(tdir, pre): pz[r["object_id"]] = fl(r["phz_median"])
    out = {}
    for sid, (d, oid, fh) in best.items():
        z = pz.get(oid, float("nan"))
        if fh > 0 and z > 0: out[S[sid]["unique_identifier"]] = (fh, z)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--q1-dir", required=True); ap.add_argument("--eclipse-dir", required=True)
    a = ap.parse_args(); t0 = time.time(); tag = "euc11" + ("_MUTATE_" + MUT if MUT else ""); tdir = os.path.join(a.q1_dir, "deep_tables")
    P("EUC11 (DEEP-FIELD LENSES)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EUC11", criteria_commit="0a6088cd0a", amendments=dict(A1="63dbb33bb4", A2="650ed9e51b", A3="a42a20fbca"), mutate=MUT, footings=E.FOOT); CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-9s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    for fn, h in SHA.items():
        if E.sha256(os.path.join(a.q1_dir, fn)) != h: sys.exit("Q1 data hash mismatch: " + fn)
    P("  Q1 lens tables: four sha256 hashes match the frozen ones")

    # ---------------------------------------------------------------- Q1 systems
    cat = sorted([r for r in csv.DictReader(open(os.path.join(a.q1_dir, "q1_discovery_engine_lens_catalog.csv"), encoding="utf-8")) if r["grade"].strip() in ("A", "B")], key=lambda r: r["id_str"])
    mass = {r["id_str"]: fl(r["einstein_radius_effective_median_pdf"]) for r in csv.DictReader(open(os.path.join(a.q1_dir, "modeling_lens_mass.csv"), encoding="utf-8"))}
    ser = {r["id_str"]: (fl(r["effective_radius_median_pdf"]), fl(r["sersic_index_median_pdf"])) for r in csv.DictReader(open(os.path.join(a.q1_dir, "modeling_lens_sersic.csv"), encoding="utf-8"))}
    n30 = {int(r["sid"]): int(r["n_within_30arcsec"]) for r in csv.DictReader(open(os.path.join(tdir, "footprint_counts.csv")))}
    L = []
    for i, r in enumerate(cat):
        tE = mass.get(r["id_str"], float("nan")); Re, n = ser.get(r["id_str"], (float("nan"), float("nan")))
        L.append(dict(sid=i, id=r["id_str"], grade=r["grade"].strip(), ra=float(r["right_ascension"]), dec=float(r["declination"]), tE=tE, te=Re, n=n,
                      has_tE=bool(tE > 0), usable=bool(tE > 0 and Re > 0 and 0.6 <= n <= 10.0), inside=n30.get(i, 0) >= 5))
    mod = [l for l in L if l["has_tE"]]; unm = [l for l in L if not l["has_tE"]]
    for i, l in enumerate(unm): l["tE_ap"] = mod[int(i * len(mod) / len(unm))]["tE"]
    for l in mod: l["tE_ap"] = l["tE"]
    merL = collections.defaultdict(list)
    for m in read_all(tdir, "merL"): merL[int(m["sid"])].append(m)
    C = list(csv.DictReader(open(os.path.join(tdir, "systems_C.csv")))); merC = collections.defaultdict(list)
    for m in read_all(tdir, "merC"): merC[int(m["sid"])].append(m)
    SP = Spectra(tdir)
    covered = {int(r["sid"]) for r in csv.DictReader(open(os.path.join(tdir, "covered_lenses.csv")))}          # amendment A3
    P("\n[systems] Q1 grade A/B: %d (A %d, B %d); with a model Einstein radius %d; usable model %d; inside the DR1 deep catalogue (A1) %d; controls %d"
      % (len(L), sum(l["grade"] == "A" for l in L), sum(l["grade"] == "B" for l in L), len(mod), sum(l["usable"] for l in L), sum(l["inside"] for l in L), len(C)))

    # lens objects, H flux
    for l in L:
        best = None
        for m in merL.get(l["sid"], []):
            d = sep_arcsec(l["ra"], l["dec"], fl(m["ra"]), fl(m["dec"]))
            if d <= 0.6 and (best is None or d < best[0]): best = (d, m)
        l["lobj"] = best[1]["object_id"] if best else None; l["fh"] = fl(best[1]["flux_h_templfit"]) if best else float("nan")
        l["zp"] = SP.phz.get(l["lobj"], (float("nan"),) * 3)[0] if best else float("nan")

    # ---------------------------------------------------------------- checks
    P("\n[instrument checks]")
    k2f = np.mean([l["lobj"] is not None for l in L]); ins = [l for l in L if l["inside"]]; k2a = np.mean([l["lobj"] is not None for l in ins])
    ck("K2 frozen", "at least 90% of L have a lens object within 0.6 arcsec", "%.3f (%d of %d)" % (k2f, sum(l["lobj"] is not None for l in L), len(L)), k2f >= 0.90)
    ck("K2 (A1)", "of the lenses inside the DR1 deep catalogue, at least 90% have a lens object", "%.3f (%d of %d)" % (k2a, sum(l["lobj"] is not None for l in ins), len(ins)), k2a >= 0.90)
    Lc = {l["sid"]: l for l in L}; cl = [Lc[int(c["sid"])] for c in C]
    fr = np.median([fl(c["flux_h_templfit"]) for c in C]) / np.median([l["fh"] for l in cl]); dz = np.median([fl(c["phz_median"]) for c in C]) - np.median([l["zp"] for l in cl])
    ck("K3", "controls like the lenses: median H flux within 10%, median photo-z within 0.05", "flux ratio %.3f, photo-z difference %+.3f (%d controls of %d lenses)"
       % (fr, dz, len(C), len({c["sid"] for c in C})), abs(fr - 1.0) <= 0.10 and abs(dz) <= 0.05)
    ver = json.load(open(os.path.join(tdir, "verify.json"))); man = json.load(open(os.path.join(tdir, "ids_manifest.json")))
    ids = {m["object_id"] for v in list(merL.values()) + list(merC.values()) for m in v}
    ck("K4", "fetch complete: every counted object id queried; one chunk of the candidates table re-queried, identical",
       "%d ids (manifest %d); re-query %s (%d rows)" % (len(ids), man["n_ids"], "identical" if ver["identical"] else "DIFFERENT", ver["rows_again"]), ver["identical"] and man["n_ids"] == len(ids))

    rows, _ = E.load(a.eclipse_dir); E.OUT.clear()
    Pm, _ = E.select(rows, ("A",)); Sm, _ = E.select(rows, ("A", "B")); Bm, _ = E.select(rows, ("B",))
    pipe = eclipse_pipeline(a.eclipse_dir)
    def ell(fh, z): return np.log10(fh) + 2.0 * np.log10(E.EUCLID.DL(z) / MPC)
    tr = [r for r in Sm if r["id"] in pipe]; fh = np.array([pipe[r["id"]][0] for r in tr]); zp = np.array([pipe[r["id"]][1] for r in tr]); y = E.arr(tr, "lm")
    X = np.column_stack([np.ones(len(tr)), ell(fh, zp), zp]); coef, *_ = np.linalg.lstsq(X, y, rcond=None); resid = y - X @ coef
    def lm_pred(fh, z): return coef[0] + coef[1] * ell(np.asarray(fh, float), np.asarray(z, float)) + coef[2] * np.asarray(z, float)
    P("  mass predictor on ECLIPSE sample S (N = %d): log M* = %.3f + %.3f l + %.3f z;  residual scatter %.3f dex (median |residual| %.3f);  pipeline minus ECLIPSE photo-z: median %+.3f, scatter %.3f"
      % (len(tr), coef[0], coef[1], coef[2], np.std(resid), np.median(np.abs(resid)), np.median(zp - E.arr(tr, "z")), np.std(zp - E.arr(tr, "z"))))
    RES["mass_predictor"] = dict(N=len(tr), coef=[float(c) for c in coef], scatter=float(np.std(resid)))
    def src_free(sample, **kw):
        eng, z, RE, Re, n, lm = E.build(sample, **kw); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        return {nm: E.stats(eng.solve_b(Mmin, a0, "S")) for nm, a0 in E.FOOT.items()}, eng, z, RE
    if not MUT:
        st = src_free(Pm)[0]
        ck("K1", "EUC1 reproduced: N(P) = 3,192, source-free median b -0.019 / -0.044 (+-0.001)", "N = %d, %+.4f / %+.4f" % (len(Pm), st["canonical"]["b_med"], st["alt"]["b_med"]),
           len(Pm) == 3192 and abs(st["canonical"]["b_med"] + 0.019) <= 0.001 and abs(st["alt"]["b_med"] + 0.044) <= 0.001)
        def transfer(sample):
            sub = [r for r in sample if r["id"] in pipe]; f = np.array([pipe[r["id"]][0] for r in sub]); z = np.array([pipe[r["id"]][1] for r in sub])
            return src_free(sub, z=z, lm=lm_pred(f, z))[0], len(sub)
        tP, nP = transfer(Pm); tW, nW = transfer([r for r in Bm if r["tE"] >= 1.7])
        ok = (abs(tP["canonical"]["f25"] - 0.156) <= 0.03 and abs(tP["alt"]["f25"] - 0.139) <= 0.03 and abs(tP["canonical"]["b_med"] + 0.019) <= 0.03 and abs(tP["alt"]["b_med"] + 0.044) <= 0.03
              and abs(tW["canonical"]["f25"] - 0.758) <= 0.05 and abs(tW["alt"]["f25"] - 0.702) <= 0.05)
        ck("T1", "transfer: EUC1 / EUC4 numbers with pipeline photo-z and predicted mass (P: f25 0.156 / 0.139 +-0.03, b_med -0.019 / -0.044 +-0.03; wide B: f25 0.758 / 0.702 +-0.05)",
           "P (N = %d): f25 %.3f / %.3f, b_med %+.3f / %+.3f;  wide B (N = %d): f25 %.3f / %.3f"
           % (nP, tP["canonical"]["f25"], tP["alt"]["f25"], tP["canonical"]["b_med"], tP["alt"]["b_med"], nW, tW["canonical"]["f25"], tW["alt"]["f25"]), ok)
        RES["T1"] = dict(P={k: v for k, v in tP.items()}, wideB={k: v for k, v in tW.items()})
    RES["checks"] = CK
    t1ok = MUT or CK["T1"]["ok"]; core_ok = MUT or all(CK[k]["ok"] for k in ("K1", "K2 (A1)", "K3", "K4"))

    # ---------------------------------------------------------------- Part 1
    P("\n[Part 1: source-free ceiling on the Q1 lenses; law S, source at z = 1100; predicted masses, pipeline photo-z]")
    Q = [l for l in L if l["inside"] and l["usable"] and l["lobj"] is not None and l["zp"] > 0 and l["fh"] > 0]
    for l in Q: l["z"] = l["zp"]; l["lm"] = float(lm_pred(l["fh"], l["zp"]))
    tEq = np.array([l["tE"] for l in Q]); gA = np.array([l["grade"] == "A" for l in Q])
    P("  lenses with a usable model, a lens object, a photo-z and an H flux: %d (grade A %d, B %d); medians: z %.3f, theta_E %.2f\", R_e %.2f\", n %.1f, log M* %.2f"
      % (len(Q), int(gA.sum()), int((~gA).sum()), np.median([l["z"] for l in Q]), np.median(tEq), np.median([l["te"] for l in Q]), np.median([l["n"] for l in Q]), np.median([l["lm"] for l in Q])))
    eng, zq, REq, Req, nq, lmq = E.build(Q); Mmin = math.pi * REq ** 2 * E.EUCLID.sigcr(zq, E.ZS_INF)
    binf = {(law, nm): eng.solve_b(Mmin, a0, law) for law in ("S", "B") for nm, a0 in E.FOOT.items()}
    def wide_word(st):
        if st["N"] < 30: return "NOT EVALUABLE"
        if st["f25_lo"] >= 0.25: return "WIDE LENSES BREAK THE CEILING"
        if st["f25_hi"] <= 0.10: return "NOT CONFIRMED"
        return "NO VERDICT"
    P1 = {}; wA, wW = {}, {}
    for nm in E.FOOT:
        b = binf[("S", nm)]
        stA = E.stats(b[gA]); wA[nm] = E.word(stA) if t1ok else "NOT EVALUABLE"; P1["QA_" + nm] = stA
        P("  QA  grade A        %-9s %s  -> %s" % (nm, E.fmt(stA), wA[nm]))
        mW = tEq >= 1.7
        if mW.sum() >= 5:
            stW = E.stats(b[mW]); wW[nm] = wide_word(stW) if t1ok else "NOT EVALUABLE"; P1["QW_" + nm] = stW
            P("  QW  theta_E >= 1.7 %-9s %s  -> %s" % (nm, E.fmt(stW), wW[nm]))
        else:
            wW[nm] = "NOT EVALUABLE"; P("  QW  theta_E >= 1.7 %-9s N = %d  -> NOT EVALUABLE" % (nm, int(mW.sum())))
    P("  reported:")
    for lab, m in (("below 1.0", tEq < 1.0), ("1.0 - 1.3", (tEq >= 1.0) & (tEq < 1.3)), ("1.3 - 1.7", (tEq >= 1.3) & (tEq < 1.7)), ("1.7 and above", tEq >= 1.7), ("grade B", ~gA), ("all", np.ones(len(Q), bool))):
        if m.sum() < 5: P("    %-14s N = %d: too few" % (lab, int(m.sum()))); continue
        for nm in E.FOOT:
            st = E.stats(binf[("S", nm)][m]); P1["%s_%s" % (lab, nm)] = st; P("    %-14s %-9s %s" % (lab, nm, E.fmt(st)))
    for nm in E.FOOT:
        st = E.stats(binf[("B", nm)][gA]); P1["QA_lawB_" + nm] = st; P("    QA law B       %-9s %s" % (nm, E.fmt(st)))
    RES["part1"] = P1; RES["part1_words"] = dict(QA=wA, QW=wW)
    if MUT == "newton":
        ref = json.load(open(os.path.join(HERE, "euc11_results.json")))["part1"]
        up = all(P1["QA_" + nm]["f25"] > ref["QA_" + nm]["f25"] for nm in E.FOOT)
        P("\n[MUTATE newton] f25 on QA: %.3f / %.3f (ref %.3f / %.3f) -> %s" % (P1["QA_canonical"]["f25"], P1["QA_alt"]["f25"], ref["QA_canonical"]["f25"], ref["QA_alt"]["f25"],
          "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- Part 2: the search
    P("\n[Part 2: deep grism tables; EUC3's rule; the %d lenses with fetched control candidates (A3) against their matched controls]" % len(covered))
    TIER = {}
    for tier in ("A", "B"):
        JL = {l["sid"]: SP.judge(l["ra"], l["dec"], l["tE_ap"], merL.get(l["sid"], []), tier) for l in L if l["inside"] and l["sid"] in covered}
        JC = {int(c["cid"]): SP.judge(fl(c["ra"]), fl(c["dec"]), Lc[int(c["sid"])]["tE_ap"], merC.get(int(c["cid"]), []), tier) for c in C}
        EL = sum(j["ev"] for j in JL.values()); EC = sum(j["ev"] for j in JC.values())
        nL = sum(j.get("status") == "SECURE" for j in JL.values()); nC = sum(j.get("status") == "SECURE" for j in JC.values())
        lim = max(1.0, 0.20 * nL * EC / max(EL, 1)); cov = EL / max(len(JL), 1) >= 0.30 and EC / max(len(JC), 1) >= 0.30
        h2 = nC <= lim
        TIER[tier] = dict(JL=JL, JC=JC, EL=EL, EC=EC, nL=nL, nC=nC, lim=lim, cov=cov, h2=h2)
        why = collections.Counter(j.get("why") for j in JL.values() if not j["ev"])
        P("  tier %s: lenses %d, evaluable %d (%.3f); controls %d, evaluable %d (%.3f); not evaluable lenses: %s"
          % (tier, len(JL), EL, EL / max(len(JL), 1), len(JC), EC, EC / max(len(JC), 1), dict(why)))
        P("    SECURE: lenses %d (%.2f%%), controls %d (%.2f%%); CONFLICT %d / %d; own-line rejections %d / %d"
          % (nL, 100.0 * nL / max(EL, 1), nC, 100.0 * nC / max(EC, 1), sum(j.get("status") == "CONFLICT" for j in JL.values()), sum(j.get("status") == "CONFLICT" for j in JC.values()),
             sum(j.get("amb", 0) > 0 for j in JL.values()), sum(j.get("amb", 0) > 0 for j in JC.values())))
        P("    on the lens object / on another counted object: lenses %d / %d, controls %d / %d;  two-line: lenses %d, controls %d;  rank 0: lenses %d, controls %d"
          % (sum(j.get("status") == "SECURE" and j["on_lens"] for j in JL.values()), sum(j.get("status") == "SECURE" and not j["on_lens"] for j in JL.values()),
             sum(j.get("status") == "SECURE" and j["on_lens"] for j in JC.values()), sum(j.get("status") == "SECURE" and not j["on_lens"] for j in JC.values()),
             sum(j.get("status") == "SECURE" and j["two"] for j in JL.values()), sum(j.get("status") == "SECURE" and j["two"] for j in JC.values()),
             sum(j.get("status") == "SECURE" and j["rank"] == 0 for j in JL.values()), sum(j.get("status") == "SECURE" and j["rank"] == 0 for j in JC.values())))
        P("    coverage %s;  H2 purity null: controls SECURE = %d against a limit of %.1f -> %s;  expected false among the lenses' %d: %.1f"
          % ("PASS" if cov else "FAIL", nC, lim, "PASS" if h2 else "FAIL", nL, nC * EL / max(EC, 1)))
        RES["tier_" + tier] = dict(EL=EL, EC=EC, nL=nL, nC=nC, limit=lim, coverage=bool(cov), H2=bool(h2), N_L=len(JL), N_C=len(JC))
    force = "A" if (TIER["A"]["cov"] and TIER["A"]["h2"]) else "B" if (TIER["B"]["cov"] and TIER["B"]["h2"]) else None
    RES["tier_in_force"] = force
    P("  tier ladder: %s" % ("tier %s is in force%s" % (force, " (frozen fallback)" if force == "B" else "") if force else "no tier passes: Part 2 is NOT EVALUABLE"))
    if MUT == "noguard":
        ref = json.load(open(os.path.join(HERE, "euc11_results.json"))); tf = ref["tier_in_force"] or "A"
        up = TIER[tf]["nC"] > ref["tier_" + tf]["nC"]
        P("\n[MUTATE noguard] SECURE controls, tier %s: %d (ref %d) -> %s" % (tf, TIER[tf]["nC"], ref["tier_" + tf]["nC"], "rose, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- Part 2: the reading (void unless a tier is in force)
    qi = {l["sid"]: i for i, l in enumerate(Q)}; READ = {}
    for tier in ("A", "B"):
        T = TIER[tier]; hits = [(sid, j) for sid, j in sorted(T["JL"].items()) if j.get("status") == "SECURE" and sid in qi]
        keep = [(sid, j) for sid, j in hits if zq[qi[sid]] < j["zs"] - 0.2]
        lab = "tier %s%s" % (tier, "" if force == tier else " (VOID: not in force)")
        P("\n[reading, %s] SECURE lenses with a usable model and mass: %d; dropped for z_l >= z_s - 0.2: %d" % (lab, len(hits), len(hits) - len(keep)))
        if not keep: READ[tier] = dict(N=0); continue
        ii = np.array([qi[s] for s, _ in keep]); zs = np.array([j["zs"] for _, j in keep]); sub = [Q[i] for i in ii]
        e2, z2, RE2, _, _, _ = E.build(sub); row = dict(N=len(keep))
        for law in ("S", "B"):
            for nm, a0 in E.FOOT.items():
                b = e2.solve_b(math.pi * RE2 ** 2 * E.EUCLID.sigcr(z2, zs), a0, law); row["b_%s_%s" % (law, nm)] = [float(x) for x in b]
        gsub = np.array([l["grade"] == "A" for l in sub]); tsub = np.array([l["tE"] for l in sub])
        for nm in E.FOOT:
            b = np.array(row["b_S_" + nm])
            for sname, m in (("grade A", gsub), ("A and B", np.ones(len(sub), bool))):
                if m.sum() == 0: continue
                st = E.stats(b[m]) if m.sum() >= 2 else dict(N=int(m.sum()), b_med=float(np.median(b[m])), b_med_lo=float("nan"), b_med_hi=float("nan"))
                w = ""
                if sname == "grade A":
                    w = "EARLY READING, NOT A GATE" if st["N"] < 10 else "Q1 LENS GATE HOLDS" if st["b_med_hi"] <= 0.15 else "Q1 LENS GATE FAILS" if st["b_med_lo"] >= 0.25 else "NO VERDICT"
                    row["word_" + nm] = w
                P("  %-8s %-9s N = %3d  median b at the secure redshift %+.3f [%+.3f, %+.3f];  same lenses, source-free %+.3f   %s"
                  % (sname, nm, st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], np.median(binf[("S", nm)][ii][m]), w))
            for k, (lo, hi) in (("below 1.0", (0, 1.0)), ("1.0 - 1.3", (1.0, 1.3)), ("1.3 and above", (1.3, 99))):
                m = (tsub >= lo) & (tsub < hi)
                if m.sum() == 0: continue
                band = F5[k][0 if nm == "canonical" else 1]
                P("    theta_E %-13s %-9s N = %2d  median b %+.3f   (EUC5-F band %+.2f to %+.2f; different lenses, not EUC5-F's grade)" % (k, nm, int(m.sum()), np.median(b[m]), band[0], band[1]))
        READ[tier] = row
    RES["reading"] = READ

    # ---------------------------------------------------------------- tables
    with open(os.path.join(HERE, "euc11_part1_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id_str", "grade", "z_phot", "theta_E_arcsec", "R_e_arcsec", "sersic_n", "log_Mstar_predicted", "b_inf_S_canonical", "b_inf_S_alt"])
        for i, l in enumerate(Q): w.writerow([l["id"], l["grade"], "%.3f" % l["z"], "%.3f" % l["tE"], "%.3f" % l["te"], "%.2f" % l["n"], "%.3f" % l["lm"], "%.3f" % binf[("S", "canonical")][i], "%.3f" % binf[("S", "alt")][i]])
    with open(os.path.join(HERE, "euc11_sources.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["tier", "kind", "system", "grade", "z_lens_phot", "z_up", "z_secure", "halpha_snr", "rank", "two_line", "on_lens_object", "status"])
        for tier in ("A", "B"):
            for sid, j in sorted(TIER[tier]["JL"].items()):
                if j.get("status") in ("SECURE", "CONFLICT"): w.writerow([tier, "lens", Lc[sid]["id"], Lc[sid]["grade"], "%.3f" % j["zl"], "%.3f" % j["zup"], "%.4f" % j["zs"], "%.1f" % j["snr"], j["rank"], int(j["two"]), int(j["on_lens"]), j["status"]])
            for cid, j in sorted(TIER[tier]["JC"].items()):
                if j.get("status") in ("SECURE", "CONFLICT"): w.writerow([tier, "control", "C%05d" % cid, "", "%.3f" % j["zl"], "%.3f" % j["zup"], "%.4f" % j["zs"], "%.1f" % j["snr"], j["rank"], int(j["two"]), int(j["on_lens"]), j["status"]])
    frozen_ok = all(v["ok"] for k, v in CK.items() if k != "K2 (A1)")
    part2 = ("tier %s in force" % force) if (force and core_ok) else "NOT EVALUABLE"
    RES["words"] = dict(as_frozen="NOT EVALUABLE" if not frozen_ok else "see A1 words", part1_QA="%s / %s" % (wA["canonical"], wA["alt"]) if core_ok else "NOT EVALUABLE",
                        part1_QW="%s / %s" % (wW["canonical"], wW["alt"]) if core_ok else "NOT EVALUABLE", part2=part2)
    P("\n[summary]")
    P("  as frozen: %s" % ("NOT EVALUABLE (check K2 as frozen fails; see AMENDMENT_A1.md)" if not frozen_ok else "all frozen checks pass"))
    P("  under the amendments, instrument checks K1, K2 (A1), K3, K4: %s;  transfer check T1: %s" % ("all pass" if core_ok else "FAILED", "pass" if t1ok else "FAIL"))
    P("  under A1, Part 1 word QA (canonical / alt): %s" % RES["words"]["part1_QA"])
    P("  under A1, Part 1 word QW (canonical / alt): %s" % RES["words"]["part1_QW"])
    P("  under A1, A2 and A3, Part 2: %s" % part2)
    P("  kappa = 1/2 FITTED. A test lane; adopts nothing. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
