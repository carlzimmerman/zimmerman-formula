#!/usr/bin/env python3
"""EUC9 (GRISM SPECTRA SOURCE REDSHIFTS).  Frozen criteria: FROZEN_CRITERIA.md (commit bea4eacfa8);
pre-data amendment AMENDMENT_A0.md (commit 82cf65da28).

Mirrored line pairs in the co-added red-grism spectra of Euclid's lens objects (euc9_core.py), graded by a grade-X
purity null, a sign-flipped signal-free null, the truth lens, injections and twins.  Rungs: TA, TB (frozen class
SECURE), then TA-D, TB-D (class SECURE-D of the amendment: the pair must also pass the dither test).  If a rung
passes: EUC1-F exactly as frozen in EUC1 RESULT section 8, and EUC5-F exactly as sealed in EUC5 RESULT section 3c.

Run:
  python3 -I euc9.py --data-dir <dir with the ECLIPSE csv files, nisp_tables/ and nisp_spectra/>
  EUC9_MUTATE=newton python3 -I euc9.py --data-dir <dir>     (must exit 1)
  EUC9_MUTATE=single python3 -I euc9.py --data-dir <dir>     (must exit 1)
  python3 -I euc9.py --data-dir <dir> --a1                   POST HOC amendment A1 (AMENDMENT_A1.md, 25d7f82cc2): the
                                                             same rule on a re-co-addition of the dither spectra without
                                                             rejection, dither test required; outputs euc9_a1*; twins too

kappa = 1/2 FITTED.  Footings never pooled.  No outcome favours the framework.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.stats import beta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc9_common as K
import euc9_core as C
E = K.E

MUT = (os.environ.get("EUC9_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
SINGLE = MUT == "single"

DZ_ABOVE, PAD_A = 0.15, 66.0
BANDS = (("[S III] 9533", 9533.2, 9533.2), ("He I 10833 / Pa gamma", 10833.3, 10941.1), ("Pa beta", 12821.6, 12821.6))
WIN = dict(HA=(0.84, 1.88), O3=(1.41, 2.78))
NULL_FRAC, COVER_MIN = 0.20, 0.30
F_HOLDS, F_FAILS, F_NMIN = 0.15, 0.25, 10
TRUTH_TOL = 0.004
INJ_N, INJ_SN, INJ_SEED = 300, 12.0, 20261112
ANCHOR = ("EUCL-DR1-L015763", 1.3657, (0.231, 0.215))
CLASSES = (("below 1.0", 0.0, 1.0), ("1.0 to 1.3", 1.0, 1.3), ("1.3 and above", 1.3, 1e9))
BAND5 = dict(canonical=((-0.19, 0.22), (-0.05, 0.30), (0.03, 0.32)), alt=((-0.19, 0.21), (-0.06, 0.34), (0.03, 0.31)))
TIERS = [t[0] for t in C.TIERS]
RUNGS = TIERS + [t + "-D" for t in TIERS]
A1 = "--a1" in sys.argv
if A1: RUNGS = [t + "-D" for t in TIERS]
ND_MIN = 2 if A1 else C.NDITH_MIN
def label(r): return ("A1-" + r[:2]) if A1 else r
def ready(raw): return C.recoadd(raw) if A1 else C.prepare(raw)

OUT = []
def P(s=""):
    print(s); OUT.append(s)

def clopper(k, n, a=0.05):
    if n == 0: return 0.0, 1.0
    return (0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1))), (1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k)))

def classify(d, raw, p, tier, sign=1.0):
    """the frozen rule on one system's spectrum at one tier -> (class, info); info carries the dither test"""
    b = C.search(p, d["thE"], sign=sign, single_only=SINGLE, nd_min=ND_MIN)[tier]
    if b is None: return "none", None
    if SINGLE: idc, z, sup = "HA1", b["lam0"] / C.HA - 1.0, []
    else: idc, z, sup = C.identify(p, b, sign, joint=A1)
    info = dict(b, idc=idc, z=float(z), sup=sup, D=None if SINGLE else C.dither_test(raw, b, sign))
    lo, hi = WIN["O3" if idc == "O3" else "HA"]
    if not (lo < z < hi): return "none", info
    if not (z >= d["zup"] + DZ_ABOVE): return "none", info
    for nm, l1, l2 in BANDS:
        if (1.0 + d["zlo"]) * l1 - PAD_A <= b["lam0"] <= (1.0 + d["zup"]) * l2 + PAD_A:
            info["own"] = nm; return "AMBIGUOUS-OWN", info
    return "SECURE", info

def at(d, rung, flip=False):
    """(class, info) of a system on a rung; on a -D rung SECURE also needs the dither test (AMENDMENT A0.2)"""
    k, info = d[("flip_" if flip else "") + rung[:2]]
    if rung.endswith("-D") and k == "SECURE" and not (info["D"] and info["D"]["passes"]): return "none", info
    return k, info

def f_word(st):
    if st["N"] < F_NMIN: return None
    if st["b_med_hi"] <= F_HOLDS: return "LENS GATE HOLDS"
    if st["b_med_lo"] >= F_FAILS: return "LENS GATE FAILS"
    return "NO VERDICT"

def f5_word(st, band):
    if st["N"] < F_NMIN: return "NOT GRADED"
    if st["b_med_lo"] > band[1]: return "LENSING EXCEEDS DYNAMICS"
    if st["b_med_hi"] < band[0]: return "LENSING BELOW DYNAMICS"
    return "LENSING EQUALS DYNAMICS"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--a1", action="store_true")
    a = ap.parse_args(); t0 = time.time()
    sdir = os.path.join(a.data_dir, "nisp_spectra_dith")
    tag = "euc9" + ("_a1" if A1 else "") + ("_MUTATE_" + MUT if MUT else "")
    RES = dict(lane="EUC9", criteria_commit="bea4eacfa8", amendment_a1=A1, mutate=MUT, footings=E.FOOT)
    P("EUC9 (GRISM SPECTRA SOURCE REDSHIFTS)%s%s" % ("   *** POST HOC AMENDMENT A1: re-co-added dither spectra, dither test required ***" if A1 else "",
      "   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e" % (E.FOOT["canonical"], E.FOOT["alt"]))

    # ---------------------------------------------------------------- systems and spectra
    P("\n[data]")
    B = K.build(a.data_dir); SYS, key, obj, Pm, Sm = B["SYS"], B["key"], B["obj"], B["Pm"], B["Sm"]
    try: flog = json.load(open(os.path.join(sdir, "fetch_log.json")))
    except Exception: flog = {}
    SPEC = {}; nofile = 0
    for lid, d in SYS.items():
        d["evaluable"] = False
        if not d.get("target"): continue
        fn = os.path.join(sdir, "%d.npz" % d["oid"])
        if not os.path.exists(fn):
            d["why"] = "no spectrum: " + flog.get(str(d["oid"]), "not fetched"); nofile += str(d["oid"]) not in flog; continue
        raw = dict(np.load(fn, allow_pickle=False)); p = ready(raw)
        if p is None: d["why"] = ("no usable dither in each grism position" if A1 else "spectrum off the common grid or under 100 good pixels"); continue
        d["evaluable"] = True; SPEC[lid] = (raw, p)
    ids = dict(P=sorted(B["inP"]), S=sorted(B["inS"]), X=B["x_ids"])
    P("  systems: S %d (P %d), X %d, truth lens %s;  targets %d;  spectra read %d" % (len(ids["S"]), len(ids["P"]), len(ids["X"]), K.TRUTH[0],
      sum(1 for d in SYS.values() if d.get("target")), len(SPEC)))
    COV = {}
    for nm in ("P", "S", "X"):
        ev = [i for i in ids[nm] if SYS[i]["evaluable"]]; why = {}
        for i in ids[nm]:
            if not SYS[i]["evaluable"]: why[SYS[i]["why"]] = why.get(SYS[i]["why"], 0) + 1
        COV[nm] = dict(N=len(ids[nm]), evaluable=len(ev), frac=len(ev) / len(ids[nm]), not_evaluable=why,
                       noise_rescale_med=float(np.median([SPEC[i][1]["k"] for i in ev])) if ev else None,
                       good_frac_med=float(np.median([SPEC[i][1]["good"].mean() for i in ev])) if ev else None)
        P("  %-2s N = %4d, evaluable %4d (%.3f); median noise rescale %.2f, median good-pixel fraction %.2f; not evaluable: %s"
          % (nm, len(ids[nm]), len(ev), COV[nm]["frac"], COV[nm]["noise_rescale_med"] or float("nan"), COV[nm]["good_frac_med"] or float("nan"), why))
    RES["coverage"] = COV
    cover_ok = COV["S"]["frac"] >= COVER_MIN and COV["X"]["frac"] >= COVER_MIN
    P("  coverage gate (>= %.0f %% of S and of X evaluable): %s" % (100 * COVER_MIN, "PASS" if cover_ok else "FAIL"))

    # ---------------------------------------------------------------- the search
    for lid, (raw, p) in SPEC.items():
        d = SYS[lid]
        for tn in TIERS:
            d[tn] = classify(d, raw, p, tn)
            d["flip_" + tn] = classify(d, raw, p, tn, sign=-1.0)

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok))
        P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    engP, zP, REP, _, _, _ = E.build(Pm)
    k1 = tuple(float(np.median(E.run_b(engP, zP, REP, E.ZS_INF, a0, "S"))) for a0 in (E.FOOT["canonical"], E.FOOT["alt"]))
    ck("K1", "EUC1 reproduced: N(P) = 3192, source-free b_med law S = -0.019 / -0.044 to 0.001", "N = %d, %+.4f / %+.4f" % (len(Pm), k1[0], k1[1]),
       (len(Pm) == 3192 and abs(k1[0] + 0.019) <= 0.001 and abs(k1[1] + 0.044) <= 0.001) or MUT == "newton")
    ar = key[ANCHOR[0]]; zsp = K.fl(obj[ANCHOR[0]]["desi_deflector_specz"])
    lma = ar["lm"] + 2.0 * math.log10(float(E.EUCLID.DL(zsp)) / float(E.EUCLID.DL(ar["z"])))
    enga, za, REa, _, _, _ = E.build([ar], z=np.array([zsp]), lm=np.array([lma]))
    anc = {nm: float(E.run_b(enga, za, REa, ANCHOR[1], a0, "S")[0]) for nm, a0 in E.FOOT.items()}
    ck("K2", "EUC2 anchor L015763 at z_l(DESI), z_s = 1.3657: b = +0.231 / +0.215 to 0.002", "%+.4f / %+.4f" % (anc["canonical"], anc["alt"]),
       (abs(anc["canonical"] - ANCHOR[2][0]) <= 0.002 and abs(anc["alt"] - ANCHOR[2][1]) <= 0.002) or MUT == "newton")
    RES["anchor_b"] = anc
    try:
        ver = json.load(open(os.path.join(sdir, "verify.json"))); gen = json.load(open(os.path.join(sdir, "generic_check.json")))
        k5ok = nofile == 0 and len(ver) >= 20 and all(v["identical"] for v in ver) and len(gen) >= 20 and all(g["ok"] for g in gen)
        k5v = "targets with neither a spectrum nor a recorded reason: %d; no spectrum (reason recorded): %d; read again identical: %d of %d; field objects identical to the per-object service: %d of %d" % (
            nofile, len(flog), sum(v["identical"] for v in ver), len(ver), sum(g["ok"] for g in gen), len(gen))
    except Exception as ex:
        k5ok, k5v = False, "verify file unreadable (%s)" % type(ex).__name__
    ck("K5", "fetch complete; 20 objects read again identical; range route equals the service", k5v, k5ok)

    # I1 / I2 injections into 300 S spectra
    rng = np.random.default_rng(INJ_SEED)
    evS = [i for i in ids["S"] if SYS[i]["evaluable"]]
    pick = [evS[j] for j in rng.choice(len(evS), size=min(INJ_N, len(evS)), replace=False)] if evS else []
    rec = tot = fal = tot2 = d3 = d4 = 0
    for lid in pick:
        raw, p = SPEC[lid]; d = SYS[lid]
        iv = np.where(p["good"], 1.0 / p["e"] ** 2, 0.0); N16 = C.G2[16.0] @ iv; N20 = C.G2[20.0] @ iv
        smax = C.DISP * (d["thE"] + C.S_EXTRA)
        for _ in range(50):
            lam0 = float(rng.uniform(12300.0, 18700.0)); s = float(rng.uniform(C.S_MIN + 1.0, max(smax - 1.0, C.S_MIN + 1.5)))
            px = [int(round((lam0 + o - C.W0) / C.DW)) for o in (-s, 0.0, s)]
            j = int(np.argmin(np.abs(C.CENT - lam0)))
            if N16[j] > 0 and N20[j] > 0 and all(p["good"][q] and p["nd"][q] >= ND_MIN for q in px): break
        else: continue
        F2 = INJ_SN * math.sqrt(2.0 / N16[j]); F1 = INJ_SN / math.sqrt(N20[j]); tot += 1; tot2 += 1
        b0 = C.search(p, d["thE"], nd_min=ND_MIN)["TA"]
        def near(bb, tol): return bool(bb and abs(bb["lam0"] - lam0) <= tol)
        if A1:                                                    # A1.3: everything is injected into the dithers and re-co-added
            q3 = C.inject_dithers(raw, lam0, s, 16.0, F2, True); bb = C.search(C.recoadd(q3), d["thE"], nd_min=ND_MIN)["TA"]
            rec += near(bb, C.DW); t = C.dither_test(q3, bb) if near(bb, C.DW) else None; d3 += bool(t and t["passes"])
            q1 = C.inject_dithers(raw, lam0, 0.0, 20.0, F1, False); bb = C.search(C.recoadd(q1), d["thE"], nd_min=ND_MIN)["TA"]
            t = C.dither_test(q1, bb) if (near(bb, 80.0) and not near(b0, 80.0)) else None; fal += bool(t and t["passes"])
            q4 = C.inject_dithers(raw, lam0, s, 16.0, F2, False); bb = C.search(C.recoadd(q4), d["thE"], nd_min=ND_MIN)["TA"]
            t = C.dither_test(q4, bb) if near(bb, C.DW) else None; d4 += bool(t and t["passes"])
            continue
        q = C.prepare(C.inject(raw, lam0, s, 16.0, F2)); bb = C.search(q, d["thE"])["TA"] if q else None
        rec += near(bb, C.DW)
        q = C.prepare(C.inject(raw, lam0, 0.0, 20.0, F1)); bb = C.search(q, d["thE"])["TA"] if q else None
        fal += bool(near(bb, 80.0) and not near(b0, 80.0))
        if SINGLE: continue
        for mirrored in (True, False):
            q3 = C.inject_dithers(raw, lam0, s, 16.0, F2, mirrored); p3 = C.prepare(q3)
            bb = C.search(p3, d["thE"])["TA"] if p3 else None
            t = C.dither_test(q3, bb) if near(bb, C.DW) else None
            if mirrored: d3 += bool(t and t["passes"])
            else: d4 += bool(t and t["passes"])
    if not SINGLE:
        ck("I1", "injected pairs (S/N 12) returned within 13.4 A in >= 70 %", "%d / %d = %.3f" % (rec, tot, rec / max(tot, 1)), tot > 0 and rec >= 0.70 * tot)
        ck("I2", "injected single centred lines (S/N 12) returned as %s in <= 5 %%" % ("SECURE-A1" if A1 else "a pair"), "%d / %d = %.3f" % (fal, tot2, fal / max(tot2, 1)), tot2 > 0 and fal <= 0.05 * tot2)
    i3ok = tot > 0 and d3 >= 0.60 * tot; i4ok = tot > 0 and d4 <= 0.05 * tot
    if not SINGLE:
        P("  %s I3  injected mirrored pairs pass the dither test in >= 60 %% : %d / %d = %.3f   [gates the -D rungs only]" % ("PASS" if i3ok else "FAIL", d3, tot, d3 / max(tot, 1)))
        P("  %s I4  injected true doublets pass the dither test in <= 5 %% : %d / %d = %.3f   [gates the -D rungs only]" % ("PASS" if i4ok else "FAIL", d4, tot, d4 / max(tot, 1)))
    RES["I3_I4"] = dict(I3=(d3, tot, bool(i3ok)), I4=(d4, tot, bool(i4ok)))

    # ---------------------------------------------------------------- gates per rung
    GATE = {}
    def cnt(group, rung, cls="SECURE", flip=False): return sum(1 for i in group if SYS[i]["evaluable"] and at(SYS[i], rung, flip)[0] == cls)
    for rung in RUNGS:
        each, comb, dchi = [t[1:] for t in C.TIERS if t[0] == rung[:2]][0]
        P("\n[rung %s: each component S/N >= %.1f, combined >= %.0f, pair over single dchi2 >= %.0f%s]" % (label(rung), each, comb, dchi,
          "; and the dither test" if rung.endswith("-D") else ""))
        c = {}
        for nm in ("P", "S", "X"):
            Ev = sum(SYS[i]["evaluable"] for i in ids[nm]); n = cnt(ids[nm], rung); lo, hi = clopper(n, Ev)
            byid = {}
            for i in ids[nm]:
                if SYS[i]["evaluable"] and at(SYS[i], rung)[0] == "SECURE": byid[at(SYS[i], rung)[1]["idc"]] = byid.get(at(SYS[i], rung)[1]["idc"], 0) + 1
            c[nm] = dict(E=Ev, SECURE=n, AMBIG=cnt(ids[nm], rung, "AMBIGUOUS-OWN"), flip=cnt(ids[nm], rung, flip=True), by_identity=byid,
                         pairs_any=sum(1 for i in ids[nm] if SYS[i]["evaluable"] and SYS[i][rung[:2]][1] is not None))
            P("  %-2s evaluable %4d: SECURE %3d (rate %.4f [%.4f, %.4f]) %s; AMBIGUOUS-OWN %d; any pair before guards %d; sign-flipped SECURE %d"
              % (nm, Ev, n, n / max(Ev, 1), lo, hi, byid, c[nm]["AMBIG"], c[nm]["pairs_any"], c[nm]["flip"]))
        lim = max(1.0, NULL_FRAC * c["S"]["SECURE"] * c["X"]["E"] / max(c["S"]["E"], 1)); h2 = c["X"]["SECURE"] <= lim
        limb = max(1.0, NULL_FRAC * c["S"]["SECURE"]); h2b = c["S"]["flip"] <= limb
        rX = c["X"]["SECURE"] / max(c["X"]["E"], 1)
        P("  H2  purity null: grade-X SECURE = %d against a limit of %.1f -> %s;  expected false among P / S: %.1f / %.1f (of %d / %d)"
          % (c["X"]["SECURE"], lim, "PASS" if h2 else "FAIL", rX * c["P"]["E"], rX * c["S"]["E"], c["P"]["SECURE"], c["S"]["SECURE"]))
        P("  H2b signal-free null: sign-flipped SECURE in S = %d against a limit of %.1f -> %s" % (c["S"]["flip"], limb, "PASS" if h2b else "FAIL"))
        dt = SYS[K.TRUTH[0]]
        if dt["evaluable"]:
            k, info = at(dt, rung)
            h4 = k == "SECURE" and abs(info["z"] - K.TRUTH[1]) <= TRUTH_TOL
            P("  H4  truth %s (z_s = %.4f): %s%s" % (K.TRUTH[0], K.TRUTH[1], "RECOVERED" if h4 else "NOT RECOVERED (class %s)" % k,
              "" if info is None else "  [midpoint %.1f A, z = %.4f as %s, half-split %.1f A = %.2f arcsec (theta_E %.2f), sigma %.0f, S/N %.1f + %.1f, ratio %.2f, dchi2 %.1f, support %s, dither test %s]"
              % (info["lam0"], info["z"], info["idc"], info["s"], info["s"] / C.DISP, dt["thE"], info["sig"], info.get("sn_b", 0), info.get("sn_r", 0), info.get("ratio", 0), info.get("dchi", 0), info["sup"],
                 "not possible" if not info["D"] else "D = %+.1f (%s; dithers %d + %d)" % (info["D"]["stat"], "passes" if info["D"]["passes"] else "fails", info["D"]["n000"], info["D"]["n180"]))))
        else:
            h4 = False; P("  H4  truth %s: NOT EVALUABLE (%s)" % (K.TRUTH[0], dt["why"]))
        extra = (i3ok and i4ok) if rung.endswith("-D") else True
        GATE[rung] = dict(counts=c, H2_limit=lim, H2=bool(h2), H2b_limit=limb, H2b=bool(h2b), H4=bool(h4), null_rate=rX, injections_ok=bool(extra),
                          passes=bool(h2 and h2b and h4 and extra))
    RES["gates"] = GATE

    P("\n[every pair passing the frozen rule at TA, with its dither test: grade X listed, lenses summarised]")
    NH = []
    for i in ids["X"]:
        if SYS[i]["evaluable"] and SYS[i]["TA"][0] == "SECURE":
            f = SYS[i]["TA"][1]; d = SYS[i]; D = f["D"]
            NH.append(dict(id=i, z=f["z"], idc=f["idc"], lam0=f["lam0"], s=f["s"], sn=f["sn"], ratio=f.get("ratio"), dchi=f.get("dchi"), zup=d["zup"], thE=d["thE"], TB=d["TB"][0],
                           D=None if not D else D["stat"], D_passes=bool(D and D["passes"])))
            P("  X %s z = %.4f (%s) midpoint %.0f A, half-split %.1f A, S/N %.1f, ratio %.2f, dchi2 %.1f | interval [%.2f, %.2f], theta_E given %.2f | support %s | TB: %s | dither test: %s"
              % (i, f["z"], f["idc"], f["lam0"], f["s"], f["sn"], f.get("ratio", 0), f.get("dchi", 0), d["zlo"], d["zup"], d["thE"], f["sup"], d["TB"][0],
                 "not possible" if not D else "D = %+.1f %s" % (D["stat"], "PASSES" if D["passes"] else "fails")))
    if not NH: P("  X: none")
    for nm in ("S", "X"):
        Ds = [SYS[i]["TA"][1]["D"] for i in ids[nm] if SYS[i]["evaluable"] and SYS[i]["TA"][0] == "SECURE"]
        st = np.array([abs(x["stat"]) for x in Ds if x])
        P("  %s: %d pairs; dither test possible %d; passes %d; median |D| %.1f" % (nm, len(Ds), len(st), sum(bool(x and x["passes"]) for x in Ds), np.median(st) if len(st) else float("nan")))
    RES["null_hits"] = NH

    # ---------------------------------------------------------------- ladder
    allok = all(v["ok"] for v in CK.values())
    tier = next((r for r in RUNGS if GATE[r]["passes"]), None)
    evaluable = allok and cover_ok and tier is not None
    P("\n[ladder]")
    for r in RUNGS:
        P("  %-5s H2 %s, H2b %s, H4 %s%s" % (label(r), *("PASS" if GATE[r][g] else "FAIL" for g in ("H2", "H2b", "H4")),
          ("" if not r.endswith("-D") else ", I3/I4 %s" % ("PASS" if GATE[r]["injections_ok"] else "FAIL"))))
    P("  -> " + (("reading rung " + label(tier) + (" (POST HOC, amendment A1)" if A1 else "" if tier == "TA" else " (frozen fallback)" if tier == "TB" else " (under pre-data amendment A0)")) if tier else "no rung passes: NOT EVALUABLE"))
    rt = tier or RUNGS[0]

    # ---------------------------------------------------------------- readings
    P("\n[readings on rung %s%s%s]" % (label(rt), ", POST HOC (A1): not the frozen gates' verdicts" if A1 else "", "" if evaluable else ", VOID (the search is not evaluable)"))
    def zmap(tn, classes=("SECURE",), ids_ok=None, o3=False):
        m = {}
        for i in ids["S"]:
            d = SYS[i]
            if not d["evaluable"] or at(d, tn)[0] not in classes: continue
            f = at(d, tn)[1]
            if ids_ok is not None and f["idc"] not in ids_ok: continue
            m[i] = (1.0 + f["z"]) * C.HA / C.O3B - 1.0 if (o3 and f["idc"] == "HA1") else f["z"]
        return m
    READ = {}
    def reading(name, sample, zs_of, desi=False, quiet=False):
        sel = [r for r in sample if r["id"] in zs_of]
        zs = np.array([zs_of[r["id"]] for r in sel]); zl = E.arr(sel, "z") if sel else np.array([]); lm = E.arr(sel, "lm") if sel else np.array([])
        if desi and sel:
            zsp = np.array([r["zspec"] if np.isfinite(r["zspec"]) and r["zspec"] > 0 else r["z"] for r in sel])
            lm = lm + 2.0 * np.log10(E.EUCLID.DL(zsp) / E.EUCLID.DL(zl)); zl = zsp
        keep = zl < zs - 0.2; dropped = int(np.sum(~keep))
        sel = [r for r, k in zip(sel, keep) if k]; zs, zl, lm = zs[keep], zl[keep], lm[keep]
        out = dict(N=len(sel), dropped=dropped, ids=[r["id"] for r in sel])
        if sel:
            eng, z, RE, _, _, _ = E.build(sel, z=zl, lm=lm); out["b"] = {}
            for law in ("S", "B"):
                for nm, a0 in E.FOOT.items():
                    bt = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs), a0, law)
                    bi = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, law)
                    out["%s_%s" % (law, nm)] = dict(true=E.stats(bt), inf=E.stats(bi))
                    out["b"]["%s_%s" % (law, nm)] = [float(x) for x in bt]; out["b"]["inf_%s_%s" % (law, nm)] = [float(x) for x in bi]
            out["thE_med"] = float(np.median(E.arr(sel, "tE"))); out["zs_med"] = float(np.median(zs))
        if not quiet:
            if not sel: P("  %-30s N = 0%s" % (name, " (dropped %d)" % dropped if dropped else ""))
            else:
                for nm in E.FOOT:
                    st, si = out["S_" + nm]["true"], out["S_" + nm]["inf"]
                    P("  %-30s law S %-9s N = %3d  b_med = %+.3f [%+.3f, %+.3f]   source-free %+.3f   n(b > 0.25) = %d%s"
                      % (name, nm, len(sel), st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], int(np.sum(np.array(out["b"]["S_" + nm]) > 0.25)),
                         "  (dropped %d)" % dropped if dropped else ""))
        READ[name] = out; return out

    def grade(zs_of, label, quiet=False):
        """EUC1-F on P and EUC5-F per class of S for one set of source redshifts"""
        w = dict(F1={}, F5={})
        rP = reading("P%s" % label, Pm, zs_of, quiet=quiet)
        for nm in E.FOOT: w["F1"][nm] = (f_word(rP["S_" + nm]["true"]) if rP["N"] >= F_NMIN else "EARLY READING, NOT A GATE")
        for ci, (cn, lo, hi) in enumerate(CLASSES):
            rc = reading("S, theta_E %s%s" % (cn, label), [r for r in Sm if lo <= r["tE"] < hi], zs_of, quiet=quiet)
            for nm in E.FOOT: w["F5"][cn + " | " + nm] = f5_word(rc["S_" + nm]["true"], BAND5[nm][ci]) if rc["N"] >= F_NMIN else "NOT GRADED"
        return w, rP
    ZS = zmap(rt)
    W, rP = grade(ZS, "")
    rS = reading("S", Sm, ZS)
    if rP["N"]:
        for nm in E.FOOT:
            st = rP["B_" + nm]["true"]; P("  %-30s law B %-9s N = %3d  b_med = %+.3f [%+.3f, %+.3f]" % ("P", nm, rP["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"]))
    Wo3, _ = grade(zmap(rt, o3=True), " [HA1 read as O III]", quiet=True)
    ident_dep = (W != Wo3)
    P("  line identity: with the HA1 lenses read at the [O III] redshift the words are %s" % ("THE SAME" if not ident_dep else "DIFFERENT: %s" % json.dumps(Wo3)))
    thP = np.median(E.arr(Pm, "tE")); nH = {k: sum(1 for i in ZS if at(SYS[i], rt)[1]["idc"] == k) for k in ("HA1", "HA2", "O3")}
    P("  secure sample of S: N = %d (%s); median theta_E %.2f arcsec (sample P: %.2f); median z_s %.2f"
      % (len(ZS), nH, np.median([SYS[i]["thE"] for i in ZS]) if ZS else float("nan"), thP, np.median(list(ZS.values())) if ZS else float("nan")))

    P("\n[robustness, law S; reported]")
    reading("1 P, HA1 at the [O III] redshift", Pm, zmap(rt, o3=True))
    reading("2 P, two-line classes only", Pm, zmap(rt, ids_ok=("HA2", "O3")))
    reading("3 P, tier TB only", Pm, zmap("TB-D" if rt.endswith("-D") else "TB"))
    reading("4 P, + AMBIGUOUS-OWN", Pm, zmap(rt, classes=("SECURE", "AMBIGUOUS-OWN")))
    reading("5 P, DESI deflector z", Pm, ZS, desi=True)
    reading("6 P, dither-confirmed only", Pm, zmap(rt[:2] + "-D"))
    reading("7 S, dither-confirmed only", Sm, zmap(rt[:2] + "-D"))
    RES["reading"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("b", "ids")} for k, v in READ.items()}

    # ---------------------------------------------------------------- per-lens table and figures
    bS = {i: {k: v[j] for k, v in rS["b"].items()} for j, i in enumerate(rS["ids"])} if rS["N"] else {}
    rows_out = []
    for i in [K.TRUTH[0]] + ids["S"] + ids["X"]:
        d = SYS[i]
        if not d["evaluable"] or d["TA"][1] is None or d["TA"][0] == "none": continue
        f = d["TA"][1]; b = bS.get(i, {}) if d["TA"][0] == "SECURE" else {}
        rows_out.append([i, d["grade"], d["inP"], d["inS"], d["TA"][0], d["TB"][0], f["idc"], "%.4f" % f["z"], "%.1f" % f["lam0"], "%.1f" % f["s"],
                         "%.2f" % (f["s"] / C.DISP), "%.0f" % f["sig"], "%.2f" % f.get("sn_b", 0), "%.2f" % f.get("sn_r", 0), "%.2f" % f.get("ratio", 0), "%.2f" % f["sn"],
                         "%.1f" % f.get("dchi", 0), "%.3e" % ((f.get("flux_b", 0) + f.get("flux_r", 0)) * 1e-16), "; ".join(f["sup"]), f.get("own", ""),
                         "" if not f.get("D") else "%.2f" % f["D"]["stat"], "" if not f.get("D") else f["D"]["passes"], "" if not f.get("D") else "%d+%d" % (f["D"]["n000"], f["D"]["n180"]), "%.3f" % d["thE"],
                         "%.3f" % d["zlo"], "%.3f" % d["zup"], d["zsrc"], d["oid"]] + [("%.4f" % b[c]) if c in b else "" for c in ("S_canonical", "S_alt", "inf_S_canonical", "inf_S_alt")])
    if not MUT:
        with open(os.path.join(HERE, tag + "_sources.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["unique_identifier", "grade", "in_P", "in_S", "class_TA", "class_TB", "line", "z_s", "midpoint_A", "half_split_A", "half_split_arcsec", "sigma_A",
                        "sn_blue", "sn_red", "flux_ratio_blue_red", "sn_combined", "dchi2_pair_over_single", "line_flux_cgs", "support", "own_line_band",
                        "dither_stat_D", "dither_test_passes", "dithers_RGS000+RGS180", "theta_E_arcsec", "z_lo", "z_up", "interval_source", "mer_object_id", "b_S_canonical", "b_S_alt", "b_inf_S_canonical", "b_inf_S_alt"])
            w.writerows(rows_out)
        P("\n  per-system table: %s_sources.csv (%d systems with a TA class before the dither test; grade X rows included and marked)" % (tag, len(rows_out)))
        try:
            import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
            fdir = "figs_a1" if A1 else "figs"; os.makedirs(os.path.join(HERE, fdir), exist_ok=True)
            show = [i for i in [K.TRUTH[0]] + ids["S"] + ids["X"] if SYS[i]["evaluable"] and SYS[i]["TA"][0] == "SECURE"]
            for pg in range(0, len(show), 8):
                chunk = show[pg:pg + 8]
                fig, ax = plt.subplots(len(chunk), 2, figsize=(11, 2.0 * len(chunk)), squeeze=False)
                for r_, i in enumerate(chunk):
                    raw, p = SPEC[i]; f = SYS[i]["TA"][1]; d = SYS[i]
                    err = np.where(p["good"], p["e"], np.nan); rr = np.where(p["good"], p["r"], np.nan)
                    mod = f["flux_b"] * C.template(f["lam0"] - f["s"], f["sig"])[0] + f["flux_r"] * C.template(f["lam0"] + f["s"], f["sig"])[0]
                    for c_, hw in enumerate((320.0, 4000.0)):
                        q = np.abs(C.WL - f["lam0"]) <= hw; axx = ax[r_, c_]
                        axx.fill_between(C.WL[q], -err[q], err[q], color="0.85", step="mid")
                        axx.step(C.WL[q], rr[q], where="mid", lw=0.8, color="k")
                        if c_ == 0:
                            axx.plot(C.WL[q], mod[q], color="0.4", lw=0.9)
                            for g, col in zip(C.POS, ("tab:blue", "tab:red")):           # mean residual of the dithers of each grism position
                                num = np.zeros(C.NPIX); den = np.zeros(C.NPIX)
                                for u in range(len(raw["DS"])):
                                    if str(raw["dpos"][u]).strip() != g: continue
                                    pu = C.prepare(dict(WAVELENGTH=raw["WAVELENGTH"], SIGNAL=raw["DS"][u], UNCERTAINTY=np.sqrt(np.clip(np.asarray(raw["DV"][u], float), 0, None)),
                                                        MASK=raw["DM"][u], NDITH=np.ones(C.NPIX, int)))
                                    if pu is None: continue
                                    wv = np.where(pu["good"], 1.0 / pu["e"] ** 2, 0.0); num += pu["r"] * wv; den += wv
                                axx.step(C.WL[q], np.where(den[q] > 0, num[q] / np.where(den[q] > 0, den[q], 1.0), np.nan), where="mid", lw=0.7, color=col, alpha=0.8)
                        for l in (f["lam0"] - f["s"], f["lam0"] + f["s"]): axx.axvline(l, color="r", lw=0.5, ls="--")
                        axx.axvline(f["lam0"], color="g", lw=0.5, ls=":"); axx.tick_params(labelsize=6)
                        axx.set_title(("%s (%s%s) z_s=%.4f %s split=%.0fA=%.2f\" thE=%.2f\" S/N %.1f+%.1f dchi2=%.0f D=%s   [black co-add; blue RGS000, red RGS180]" % (i[-7:], d["grade"],
                                       ", P" if d["inP"] else "", f["z"], f["idc"], f["s"], f["s"] / C.DISP, d["thE"], f["sn_b"], f["sn_r"], f["dchi"],
                                       "n/a" if not f["D"] else "%+.1f%s" % (f["D"]["stat"], " ok" if f["D"]["passes"] else ""))) if c_ == 0 else "whole spectrum (residual)", fontsize=6)
                fig.tight_layout(); fig.savefig(os.path.join(HERE, fdir, "ta_%02d.png" % (pg // 8)), dpi=70); plt.close(fig)
            P("  figures: %s/ta_*.png (%d pairs passing the rule at TA: truth lens, S, then grade X)" % (fdir, len(show)))
        except Exception as ex:
            P("  (figures skipped: %s)" % type(ex).__name__)
    if rP["N"]:
        P("  sample P per lens (law S): id, z_l, z_s, line, half-split arcsec, theta_E, S/N, support, b canonical / alt (source-free alt)")
        for j in np.argsort([ZS[i] for i in rP["ids"]]):
            i = rP["ids"][j]; f = at(SYS[i], rt)[1]
            P("    %s %.3f %.4f %-3s %.2f %.2f %5.1f %-22s %+.3f / %+.3f  (%+.3f)" % (i, key[i]["z"], ZS[i], f["idc"], f["s"] / C.DISP, key[i]["tE"], f["sn"],
              "; ".join(f["sup"]) or "-", rP["b"]["S_canonical"][j], rP["b"]["S_alt"][j], rP["b"]["inf_S_alt"][j]))

    # ---------------------------------------------------------------- verdict
    P("\n[summary]")
    P("  instrument checks: %s;  coverage: %s;  reading rung: %s" % ("all pass" if allok else "FAILED", "pass" if cover_ok else "FAIL", tier or "none"))
    if evaluable:
        v1 = "%s%s / %s" % ("POST HOC READING (A1): " if A1 else "", W["F1"]["canonical"], W["F1"]["alt"])
        P("  N(P) with a secure source redshift = %d (EUC1-F needs %d)" % (rP["N"], F_NMIN))
        P("  EUC1-F%s (canonical / alt): %s / %s%s" % (" under A1 (post hoc)" if A1 else "", W["F1"]["canonical"], W["F1"]["alt"], " (IDENTIFICATION-DEPENDENT)" if ident_dep else ""))
        for cn, _, _ in CLASSES:
            P("  EUC5-F%s, theta_E %-14s (canonical / alt): %s / %s   [N = %d]" % (" under A1 (post hoc)" if A1 else "", cn, W["F5"][cn + " | canonical"], W["F5"][cn + " | alt"], READ["S, theta_E %s" % cn]["N"]))
    else:
        v1 = "NOT EVALUABLE / NOT EVALUABLE"
        P("  EUC1-F: not graded.  EUC5-F: not graded.  (N(P) with a pair passing the rule: %d; void)" % rP["N"])
    P("  %s (canonical / alt): %s%s" % ("A1 WORD" if A1 else "LANE WORD", v1, (" [rung %s%s]" % (label(tier), "" if (A1 or tier == "TA") else ", frozen fallback" if tier == "TB" else ", under pre-data amendment A0")) if evaluable else ""))
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    RES.update(checks=CK, checks_all_pass=allok, coverage_ok=cover_ok, tier=tier, evaluable=bool(evaluable), verdict=v1, words=W, words_o3=Wo3,
               identification_dependent=bool(ident_dep), N_P=rP["N"])

    code = 0 if evaluable else 3
    if MUT:
        try: ref = json.load(open(os.path.join(HERE, tag.split("_MUTATE_")[0] + "_results.json")))
        except Exception: ref = None
        bite = False
        if ref is None: P("\n[MUTATE %s] no reference results: cannot judge" % MUT)
        elif MUT == "newton":
            samp = next((s for s in ("P", "S") if ref["reading"].get(s, {}).get("N", 0) >= 1 and READ.get(s, {}).get("N", 0) >= 1), None)
            up_a = all(anc[k] > ref["anchor_b"][k] for k in E.FOOT)
            up_s = samp is not None and all(READ[samp]["S_" + k]["true"]["b_med"] > ref["reading"][samp]["S_" + k]["true"]["b_med"] for k in E.FOOT)
            bite = up_a and (up_s or samp is None)
            P("\n[MUTATE newton] anchor b %+.3f / %+.3f (ref %+.3f / %+.3f); sample %s b_med %s (ref %s) -> %s"
              % (anc["canonical"], anc["alt"], ref["anchor_b"]["canonical"], ref["anchor_b"]["alt"], samp,
                 None if samp is None else "%+.3f / %+.3f" % tuple(READ[samp]["S_" + k]["true"]["b_med"] for k in E.FOOT),
                 None if samp is None else "%+.3f / %+.3f" % tuple(ref["reading"][samp]["S_" + k]["true"]["b_med"] for k in E.FOOT),
                 "rose on both footings, as required; exit 1" if bite else "DID NOT RISE"))
        elif MUT == "single":
            r0 = RUNGS[0]; n0, n1 = ref["gates"][r0]["counts"]["X"]["SECURE"], sum(1 for i in ids["X"] if SYS[i]["evaluable"] and SYS[i]["TA"][0] == "SECURE")
            m0, m1 = ref["gates"][r0]["counts"]["S"]["SECURE"], sum(1 for i in ids["S"] if SYS[i]["evaluable"] and SYS[i]["TA"][0] == "SECURE")
            bite = n1 > n0
            P("\n[MUTATE single] grade-X systems passing with the pair requirement removed (S/N >= 6): %d (ref %d); S: %d (ref %d) -> %s"
              % (n1, n0, m1, m0, "the null count rose, as required; exit 1" if bite else "DID NOT RISE"))
        RES["mutate_bites"] = bool(bite); code = 1 if bite else 2
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

if __name__ == "__main__":
    main()
