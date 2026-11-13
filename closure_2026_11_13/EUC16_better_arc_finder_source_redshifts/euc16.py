#!/usr/bin/env python3
"""EUC16 (BETTER ARC FINDER, PREDICTED-SPLIT SOURCE REDSHIFTS).  Frozen criteria: FROZEN_CRITERIA.md.

EUC15's lane (euc15.py) copied with ONE change: every system's arc position comes from the frozen EUC16 finder
(euc16_arc.arc_euc16: lens light modelled about its own light centre in elliptical annuli; the peak of the smoothed
residual divided by sqrt(sky^2 + (0.03 x lens model)^2) between 0.5 and 1.5 theta_E; centroid within 0.3 arcsec)
instead of euc14.truth_arc.  EUC14's rule, tiers, gates, nulls (grade X, rotated 90 deg, sign-flipped, mirrored),
line-identity readings, checks and twins are imported or copied unchanged; the null limits scale with the new evaluable
counts by EUC14's formula.  Added: check K8 (the copied code with EUC15's finder reproduces EUC15), the fate of
EUC15's five certified lenses, the single-line count and a selection check.

Run:
  EUC16_FINDER=v1       python3 -I -B euc16.py --data-dir <dir>    (check K8: must reproduce EUC15; exit 0)
  python3 -I -B euc16.py --data-dir <dir>                           (the lane)
  EUC16_MUTATE=newton   python3 -I -B euc16.py --data-dir <dir>    (must exit 1)
  EUC16_MUTATE=nowindow python3 -I -B euc16.py --data-dir <dir>    (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  No outcome favours the framework.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC14_predicted_split_source_redshifts"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC9_grism_spectra_source_redshifts"))
EUC15_DIR = os.path.join(HERE, "..", "..", "closure_2026_11_12", "EUC15_image_arc_predicted_split")
import euc14 as L14                                          # EUC14's frozen rule and helpers (imported, not edited)
from euc14 import (K, C, GM, CAL, E, CONV, W_K, H_MIN, TIERS, NULL_FRAC, COVER_MIN, F_HOLDS, F_FAILS, F_NMIN, TRUTH_TOL,
                   INJ_N, INJ_SN, INJ_SEED, ANCHOR, IDENT, HA, DZ_ABOVE, SIG_ALL, clopper, search_arc, classify, truth_arc)
import euc16_arc as A                                        # the frozen EUC16 finder (image only)

MUT = (os.environ.get("EUC16_MUTATE", "") or "").strip()
FINDER = (os.environ.get("EUC16_FINDER", "") or "").strip()                  # "" = the frozen EUC16 finder; "v1" = EUC15's (check K8 only)
assert FINDER in ("", "v1") and MUT in ("", "newton", "nowindow") and not (FINDER and MUT)
FIVE = ("EUCL-DR1-L001890", "EUCL-DR1-L001520", "EUCL-DR1-L001449", "EUCL-DR1-L012745", "EUCL-DR1-L001971")   # EUC15's certified P
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
if MUT == "nowindow": L14.MUT = "anyk"                        # EUC14's own k-window removal (any |k| >= 0.3)
BOX_GOOD = 0.90                                              # a usable box: at least 90 % of its pixels finite and non-zero

OUT = []
def P(s=""):
    print(s); OUT.append(s)

def image_arc(path, ra0, de0, thE):
    """the frozen EUC16 finder on this system's box (EUC15's finder with EUC16_FINDER=v1); None if the box is not usable"""
    from astropy.io import fits
    img = fits.getdata(path)
    if np.mean(np.isfinite(img) & (img != 0)) < BOX_GOOD: return None
    if FINDER == "v1": a = truth_arc(path, ra0, de0, thE)
    else:
        im, E_, N_ = A.offsets(path, ra0, de0); a = A.arc_euc16(im, E_, N_, thE)
    return a if np.all(np.isfinite(a)) else None

# ------------------------------------------------------------------ main (EUC14's, with the arc input and the twin replaced)
def main():
    assert CONV is not None and W_K is not None, "convention and k window are frozen in the criteria"
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args(); t0 = time.time()
    sdir = os.path.join(a.data_dir, "nisp_spectra_dith"); odir = os.path.join(a.data_dir, "euc15")
    tag = "euc16" + ("_MUTATE_" + MUT if MUT else "") + ("_CHECK_v1" if FINDER == "v1" else "")
    RES = dict(lane="EUC16", mutate=MUT, finder=FINDER or "euc16", footings=E.FOOT, convention=CONV, w_k=W_K)
    P("EUC16 (BETTER ARC FINDER, PREDICTED-SPLIT SOURCE REDSHIFTS)%s%s" % ("   *** MUTATE = %s ***" % MUT if MUT else "",
      "   *** CHECK K8: EUC15's finder ***" if FINDER == "v1" else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e;  convention C0 = %.0f deg, tilt sign %+.0f;  k window 1 +- %.2f" % (E.FOOT["canonical"], E.FOOT["alt"], CONV[0], CONV[1], W_K))

    # ---------------------------------------------------------------- systems, arcs, spectra
    P("\n[data]")
    B = K.build(a.data_dir); SYS, key, obj, Pm, Sm = B["SYS"], B["key"], B["obj"], B["Pm"], B["Sm"]
    PA = GM.load_pa(a.data_dir)
    tdir = os.path.join(a.data_dir, "nisp_tables")
    sysrow = {int(r["sid"]): r for r in csv.DictReader(open(os.path.join(tdir, "systems.csv"), newline=""))}
    mer = {}
    for r in K.read_tab(tdir, "mer"): mer.setdefault(sysrow[int(r["sid"])]["unique_identifier"], []).append(r)
    ids = dict(P=sorted(B["inP"]), S=sorted(B["inS"]), X=B["x_ids"])
    D = {}
    for lid, d in SYS.items():
        d["spec_ok"] = False; d["evaluable"] = False; d["arcs"] = []
        if not d.get("target"): continue
        fn = os.path.join(sdir, "%d.npz" % d["oid"])
        if not os.path.exists(fn): d["why"] = "no spectrum"; continue
        rows = mer.get(lid, []); lo = [r for r in rows if int(r["object_id"]) == d["oid"]]
        if not lo: d["why"] = "lens object not in the table"; continue
        ra0, de0 = float(lo[0]["ra"]), float(lo[0]["dec"]); d["ra0"], d["de0"] = ra0, de0
        raw = dict(np.load(fn, allow_pickle=False))
        U = GM.dither_dirs(raw, PA, CONV, ra0, de0)
        dl = C.dithers(raw)
        okd = [i for i, x in enumerate(dl) if x is not None and np.isfinite(U[i, 0])]
        if not any(dl[i]["pos"] == C.POS[0] for i in okd) or not any(dl[i]["pos"] == C.POS[1] for i in okd):
            d["why"] = "no usable dither with a position angle in each grism position"; continue
        d["spec_ok"] = True
        bx = os.path.join(odir, "vis_boxes", "%d.fits" % d["oid"])                      # the arc: from the VIS box only
        d["box"] = os.path.exists(bx)
        arc = image_arc(bx, ra0, de0, d["thE"]) if d["box"] else None
        if arc is not None: d["arcs"] = [arc]
        D[lid] = (raw, dl, U)
    dt = SYS[K.TRUTH[0]]
    if dt.get("arcs"):
        P("  truth lens %s: arc from its VIS image at (east %+.2f, north %+.2f) arcsec, %.2f arcsec from the lens object (theta_E %.2f)"
          % (K.TRUTH[0], dt["arcs"][0][0], dt["arcs"][0][1], float(np.hypot(*dt["arcs"][0])), dt["thE"]))
    # per-arc searches: true prediction, sign-flipped residuals, arcs rotated by +90 deg, arcs mirrored
    def rot(o): return np.array([o[1], -o[0]])
    S_cache = {}
    for lid, (raw, dl, U) in D.items():
        d = SYS[lid]
        if not (d["inS"] or d["isX"] or lid == K.TRUTH[0]): continue
        S = C.sums(dl, SIG_ALL); dlf = [None if x is None else dict(x, r=-x["r"]) for x in dl]; Sf = C.sums(dlf, SIG_ALL)
        d["cache"] = {v: {} for v in ("true", "flip", "rot", "mirror")}
        for ai, off in enumerate(d["arcs"]):
            for v, (dd, SS, oo) in dict(true=(dl, S, off), flip=(dlf, Sf, off), rot=(dl, S, rot(off)), mirror=(dl, S, -off)).items():
                pr = GM.proj(U, oo); r_, u_ = search_arc(dd, SS, pr)
                d["cache"][v][ai] = (r_, u_, pr)
        d["usable_arc"] = {v: any(x[1] is not None and x[1]["ok"] for x in d["cache"][v].values()) for v in d["cache"]}
        d["evaluable"] = d["usable_arc"]["true"]
        S_cache[lid] = (S, Sf, dlf)
    # for the nowindow twin: (system, variant) pairs of S and X with a TA candidate before line identity and guards
    pre = {v: sum(1 for lid in D if (SYS[lid]["inS"] or SYS[lid]["isX"]) and "cache" in SYS[lid]
                  and any(x[0] is not None and x[0].get("TA") is not None for x in SYS[lid]["cache"][v].values())) for v in ("true", "flip", "rot", "mirror")}
    RES["pre_guard_TA"] = pre; RES["pre_guard_TA_total"] = int(sum(pre.values()))
    P("  pre-guard TA candidates (S and X; true / sign-flipped / rotated / mirrored): %s" % pre)
    COV = {}
    for nm in ("P", "S", "X"):
        n = len(ids[nm]); sp = sum(SYS[i]["spec_ok"] for i in ids[nm]); wa = sum(1 for i in ids[nm] if SYS[i]["spec_ok"] and SYS[i]["arcs"])
        ev = sum(SYS[i]["evaluable"] for i in ids[nm])
        COV[nm] = dict(N=n, spectrum=sp, with_arc=wa, evaluable=ev)
        bxn = sum(1 for i in ids[nm] if SYS[i]["spec_ok"] and SYS[i].get("box"))
        rr = [float(np.hypot(*SYS[i]["arcs"][0])) / SYS[i]["thE"] for i in ids[nm] if SYS[i]["spec_ok"] and SYS[i]["arcs"]]
        COV[nm] = dict(N=n, spectrum=sp, box=bxn, with_arc=wa, evaluable=ev, arc_r_over_thetaE_median=float(np.median(rr)) if rr else None)
        P("  %-2s N = %4d; usable spectrum with position angles %4d (%.3f); VIS box %4d; image arc %4d (median radius / theta_E %.2f); evaluable (predicted half-split >= %.0f A) %4d"
          % (nm, n, sp, sp / n, bxn, wa, COV[nm]["arc_r_over_thetaE_median"] or float("nan"), H_MIN, ev))
    cover_ok = COV["S"]["spectrum"] / COV["S"]["N"] >= COVER_MIN and COV["X"]["spectrum"] / COV["X"]["N"] >= COVER_MIN
    P("  coverage gate (>= %.0f %% of S and of X with a usable spectrum): %s" % (100 * COVER_MIN, "PASS" if cover_ok else "FAIL"))
    RES["coverage"] = COV

    def cls(lid, tier, v="true"):
        d = SYS[lid]
        if not d.get("usable_arc", {}).get(v): return "none", None
        ck = (tier, v)
        if ck not in d.setdefault("cls", {}):
            raw, dl, U = D[lid]; S, Sf, dlf = S_cache[lid]
            dd, SS = (dlf, Sf) if v == "flip" else (dl, S)
            arcs = d["arcs"] if v in ("true", "flip") else [rot(o) if v == "rot" else -o for o in d["arcs"]]
            d["cls"][ck] = classify(d, dd, SS, arcs, tier, d["cache"][v])
        return d["cls"][ck]

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
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
        ver = json.load(open(os.path.join(sdir, "verify.json"))); flog = json.load(open(os.path.join(sdir, "fetch_log.json")))
        miss = sum(1 for d in SYS.values() if d.get("target") and not os.path.exists(os.path.join(sdir, "%d.npz" % d["oid"])) and str(d["oid"]) not in flog)
        k5ok = miss == 0 and len(ver) >= 20 and all(v["identical"] for v in ver)
        k5v = "targets with neither a spectrum nor a recorded reason %d; EUC9's re-read check %d of %d identical" % (miss, sum(v["identical"] for v in ver), len(ver))
    except Exception as ex:
        k5ok, k5v = False, "unreadable (%s)" % type(ex).__name__
    ck("K5", "dither cache complete (EUC9's fetch) and re-read identical", k5v, k5ok)
    npa = sum(int(np.sum(np.isfinite(D[i][2][:, 0]))) for i in D); nd = sum(len(D[i][1]) for i in D)
    ck("K6", "position angle found for >= 95 % of the dithers of evaluable-spectrum systems", "%d of %d (%.3f)" % (npa, nd, npa / max(nd, 1)), npa >= 0.95 * nd)
    for nm in ("S", "X"):
        sp, bxn, wa = COV[nm]["spectrum"], COV[nm]["box"], COV[nm]["with_arc"]
        ck("K7" + nm, "VIS box for >= 95 %% of usable-spectrum %s systems, and a usable image arc for >= 90 %% of those" % nm,
           "box %d of %d, arc %d" % (bxn, sp, wa), bxn >= 0.95 * sp and wa >= 0.90 * bxn)
    if FINDER != "v1":
        try:
            k8 = json.load(open(os.path.join(HERE, "euc16_CHECK_v1_results.json")))
            ck("K8", "the copied lane code with EUC15's finder reproduces EUC15's coverage and gate counts exactly", k8["check_value"], k8["check_ok"])
        except Exception as ex:
            ck("K8", "the copied lane code with EUC15's finder reproduces EUC15's coverage and gate counts exactly", "no check output (%s)" % type(ex).__name__, False)
    cal = CAL.summary(a.data_dir)
    ck("C1", "field calibration reproduced: convention and k window as frozen, calibration passes",
       "convention %s, %d detections (next %d), median k %.3f, sigma %.3f, n %d" % (cal["convention"], cal["n_detected"], cal["next_detected"], cal["k_median"], cal["k_sigma"], cal["n_scale"]),
       cal["passes"] and tuple(cal["convention"]) == tuple(CONV) and abs(max(0.25, min(0.5, 2.0 * cal["k_sigma"])) - W_K) < 0.005)

    # injections into the dithers of S systems with a usable arc
    rng = np.random.default_rng(INJ_SEED)
    evS = [i for i in ids["S"] if SYS[i]["evaluable"]]
    pick = [evS[j] for j in rng.permutation(len(evS))[:INJ_N]]
    i1 = i2 = i3 = n_inj = 0
    for lid in pick:
        d = SYS[lid]; raw, dl, U = D[lid]
        ai = next(ai for ai, x in d["cache"]["true"].items() if x[1] is not None and x[1]["ok"]); pr = d["cache"]["true"][ai][2]
        b0, _ = search_arc(dl, S_cache[lid][0], pr)
        for _ in range(50):
            lam0 = float(rng.uniform(12300.0, 18700.0)); j = int(np.argmin(np.abs(C.LAM0 - lam0)))
            sc = C.scan(dl, S_cache[lid][0], pr, 16.0, kgrid=np.array([1.0, -1.0, 0.0]), lam0=np.array([C.LAM0[j]]))
            if np.all(sc["N"][:, 0] > 0): break
        else: continue
        lam0 = float(C.LAM0[j]); n_inj += 1
        def near(bb, tol): return bool(bb and bb.get("TA") and abs(bb["TA"]["lam0"] - lam0) <= tol)
        dq = C.dithers(C.inject(raw, pr, lam0, 1.0, 16.0, INJ_SN / math.sqrt(sc["N"][0, 0]))); q, _ = search_arc(dq, C.sums(dq, SIG_ALL), pr)
        i1 += near(q, C.DW)
        dq = C.dithers(C.inject(raw, pr, lam0, 0.0, 20.0, INJ_SN / math.sqrt(sc["N"][2, 0]))); q, _ = search_arc(dq, C.sums(dq, SIG_ALL), pr)
        i2 += near(q, 80.0) and not near(b0, 80.0)
        dq = C.dithers(C.inject(raw, pr, lam0, -1.0, 16.0, INJ_SN / math.sqrt(sc["N"][1, 0]))); q, _ = search_arc(dq, C.sums(dq, SIG_ALL), pr)
        i3 += near(q, C.DW) and not near(b0, C.DW)
    if MUT != "nowindow":
        ck("I1", "a line injected at the predicted shifts (S/N 12) returned at TA within 13.4 A in >= 70 %", "%d / %d = %.3f" % (i1, n_inj, i1 / max(n_inj, 1)), n_inj > 0 and i1 >= 0.70 * n_inj)
        ck("I2", "a centred line (S/N 12) returned at TA in <= 5 %", "%d / %d = %.3f" % (i2, n_inj, i2 / max(n_inj, 1)), n_inj > 0 and i2 <= 0.05 * n_inj)
        ck("I3", "a line at the mirrored shifts (S/N 12) returned at TA in <= 5 %", "%d / %d = %.3f" % (i3, n_inj, i3 / max(n_inj, 1)), n_inj > 0 and i3 <= 0.05 * n_inj)

    # ---------------------------------------------------------------- gates per tier
    GATE = {}
    def cnt(group, tier, v="true", c_="SECURE"): return sum(1 for i in group if SYS[i]["evaluable"] and cls(i, tier, v)[0] == c_)
    for tn, each, comb, dchi in TIERS:
        P("\n[tier %s: each grism position S/N >= %.1f, combined >= %.0f, over a centred line dchi2 >= %.0f; k within 1 +- %.2f]" % (tn, each, comb, dchi, W_K))
        c = {}
        for nm in ("P", "S", "X"):
            Ev = sum(SYS[i]["evaluable"] for i in ids[nm]); n = cnt(ids[nm], tn); lo, hi = clopper(n, Ev)
            byid = {}
            for i in ids[nm]:
                if SYS[i]["evaluable"] and cls(i, tn)[0] == "SECURE": byid[cls(i, tn)[1]["idc"]] = byid.get(cls(i, tn)[1]["idc"], 0) + 1
            c[nm] = dict(E=Ev, SECURE=n, by_identity=byid, AMBIG=cnt(ids[nm], tn, c_="AMBIGUOUS-OWN"), CONFLICT=cnt(ids[nm], tn, c_="CONFLICT"),
                         flip=cnt(ids[nm], tn, "flip"), rot=cnt(ids[nm], tn, "rot"), mirror=cnt(ids[nm], tn, "mirror"),
                         E_rot=sum(1 for i in ids[nm] if SYS[i].get("usable_arc", {}).get("rot")))
            P("  %-2s evaluable %4d: SECURE %3d (rate %.4f [%.4f, %.4f]) %s; AMBIGUOUS-OWN %d; CONFLICT %d | sign-flipped %d; rotated 90 deg %d (of %d); mirrored %d"
              % (nm, Ev, n, n / max(Ev, 1), lo, hi, byid, c[nm]["AMBIG"], c[nm]["CONFLICT"], c[nm]["flip"], c[nm]["rot"], c[nm]["E_rot"], c[nm]["mirror"]))
        lim = max(1.0, NULL_FRAC * c["S"]["SECURE"] * c["X"]["E"] / max(c["S"]["E"], 1)); h2 = c["X"]["SECURE"] <= lim
        lim3 = max(1.0, NULL_FRAC * c["S"]["SECURE"]); h3 = c["S"]["rot"] <= lim3
        h2b = c["S"]["flip"] <= lim3
        P("  H2  purity null: grade-X SECURE = %d against a limit of %.1f -> %s" % (c["X"]["SECURE"], lim, "PASS" if h2 else "FAIL"))
        P("  H3  scrambled prediction (arcs rotated by 90 deg): S SECURE = %d against a limit of %.1f -> %s" % (c["S"]["rot"], lim3, "PASS" if h3 else "FAIL"))
        P("  H2b sign-flipped residuals: S SECURE = %d against a limit of %.1f -> %s" % (c["S"]["flip"], lim3, "PASS" if h2b else "FAIL"))
        if dt.get("usable_arc", {}).get("true"):
            k_, info = cls(K.TRUTH[0], tn)
            h4 = k_ == "SECURE" and abs(info["z"] - K.TRUTH[1]) <= TRUTH_TOL
            best = dt["cache"]["true"][0][0]
            P("  H4  truth %s (z_s = %.4f): %s%s" % (K.TRUTH[0], K.TRUTH[1], "RECOVERED" if h4 else "NOT RECOVERED (class %s)" % k_,
              "" if not info else "  [midpoint %.1f A, z = %.4f as %s, k = %.2f (predicted half-split %.1f A), sigma %.0f, S/N %.1f (RGS000 %.1f, RGS180 %.1f), dchi2 over centred %.1f, support %s]"
              % (info["lam0"], info["z"], info["idc"], info["k"], info["h"], info["sig"], info["sn"], info["sn000"], info["sn180"], info["dchi"], info["sup"])))
        else:
            h4 = False; best = None
            P("  H4  truth %s: NOT EVALUABLE (%s)" % (K.TRUTH[0], "no usable arc" if dt.get("spec_ok") else dt.get("why", "no spectrum")))
        GATE[tn] = dict(counts=c, H2_limit=lim, H2=bool(h2), H3_limit=lim3, H3=bool(h3), H2b=bool(h2b), H4=bool(h4), passes=bool(h2 and h3 and h2b and h4))
    RES["gates"] = GATE

    P("\n[every SECURE system at TA: grade X and lenses]")
    NH = []
    for nm in ("X", "S"):
        for i in ids[nm]:
            k_, f = cls(i, "TA")
            if k_ != "SECURE": continue
            d = SYS[i]
            NH.append(dict(id=i, side=nm, inP=d["inP"], z=f["z"], idc=f["idc"], lam0=f["lam0"], k=f["k"], h=f["h"], sn=f["sn"], sn000=f["sn000"], sn180=f["sn180"],
                           dchi=f["dchi"], sup=f["sup"], thE=d["thE"], zup=d["zup"], arc=f["off"], TB=cls(i, "TB")[0]))
            P("  %s %s%s z = %.4f (%s) midpoint %.0f A, k %.2f, predicted half-split %.0f A, S/N %.1f (%.1f / %.1f), dchi2 %.1f | arc (E %+.2f, N %+.2f) | theta_E %.2f | z_up %.2f | support %s | TB %s"
              % (nm, i, " (P)" if d["inP"] else "", f["z"], f["idc"], f["lam0"], f["k"], f["h"], f["sn"], f["sn000"], f["sn180"], f["dchi"], f["off"][0], f["off"][1], d["thE"], d["zup"], f["sup"], NH[-1]["TB"]))
    RES["secure_list"] = NH

    # ---------------------------------------------------------------- ladder
    allok = all(v["ok"] for v in CK.values())
    tier = next((t[0] for t in TIERS if GATE[t[0]]["passes"]), None)
    evaluable = allok and cover_ok and tier is not None
    P("\n[ladder]")
    for t in TIERS: P("  %s  H2 %s, H3 %s, H2b %s, H4 %s" % (t[0], *("PASS" if GATE[t[0]][g] else "FAIL" for g in ("H2", "H3", "H2b", "H4"))))
    P("  -> " + (("reading tier " + tier + ("" if tier == "TA" else " (frozen fallback)")) if tier else "no tier passes: NOT EVALUABLE"))
    rt = tier or "TA"

    # ---------------------------------------------------------------- readings
    P("\n[readings on tier %s%s]" % (rt, "" if evaluable else ", VOID (the search is not evaluable)"))
    READ = {}
    def zmap(tn, ident=None, classes=("SECURE",), ids_ok=None):
        m = {}
        for i in ids["S"]:
            d = SYS[i]
            if not d["evaluable"] or cls(i, tn)[0] not in classes: continue
            f = cls(i, tn)[1]
            if ids_ok is not None and f["idc"] not in ids_ok: continue
            z = f["z"]
            if ident is not None and f["idc"] == "HA1":
                zx = (1.0 + z) * HA / ident - 1.0
                if zx >= d["zup"] + DZ_ABOVE: z = zx                            # an identity that puts the source at or below the lens is excluded
            m[i] = z
        return m
    def reading(name, sample, zs_of, desi=False, quiet=False):
        sel = [r for r in sample if r["id"] in zs_of]
        zs = np.array([zs_of[r["id"]] for r in sel]); zl = E.arr(sel, "z") if sel else np.array([]); lm = E.arr(sel, "lm") if sel else np.array([])
        if desi and sel:
            zsp = np.array([r["zspec"] if np.isfinite(r["zspec"]) and r["zspec"] > 0 else r["z"] for r in sel])
            lm = lm + 2.0 * np.log10(E.EUCLID.DL(zsp) / E.EUCLID.DL(zl)); zl = zsp
        keep = zl < zs - 0.2; dropped = int(np.sum(~keep))
        sel = [r for r, k_ in zip(sel, keep) if k_]; zs, zl, lm = zs[keep], zl[keep], lm[keep]
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
            if not sel: P("  %-34s N = 0%s" % (name, " (dropped %d)" % dropped if dropped else ""))
            else:
                for nm in E.FOOT:
                    st, si = out["S_" + nm]["true"], out["S_" + nm]["inf"]
                    P("  %-34s law S %-9s N = %3d  b_med = %+.3f [%+.3f, %+.3f]   source-free %+.3f%s"
                      % (name, nm, len(sel), st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], "  (dropped %d)" % dropped if dropped else ""))
        READ[name] = out; return out
    def f_word(rP_):
        w = {}
        for nm in E.FOOT:
            if rP_["N"] < F_NMIN: w[nm] = "EARLY READING, NOT A GATE"; continue
            st = rP_["S_" + nm]["true"]
            w[nm] = "LENS GATE HOLDS" if st["b_med_hi"] <= F_HOLDS else "LENS GATE FAILS" if st["b_med_lo"] >= F_FAILS else "NO VERDICT"
        return w
    ZS = zmap(rt)
    rP = reading("P", Pm, ZS); rS = reading("S", Sm, ZS)
    W = f_word(rP)
    WID = {}
    for nm_i, lam_i in IDENT:
        WID[nm_i] = f_word(reading("P [HA1 read as %s]" % nm_i, Pm, zmap(rt, lam_i), quiet=False))
    ident_dep = any(WID[k_] != W for k_ in WID)
    P("  line identity: HA1 lenses read as %s -> words %s" % (", ".join(n for n, _ in IDENT), "THE SAME" if not ident_dep else "DIFFERENT: %s" % json.dumps(WID)))
    nH = {k_: sum(1 for i in ZS if cls(i, rt)[1]["idc"] == k_) for k_ in ("HA1", "HA2", "O3")}
    P("  secure sample of S: N = %d (%s); median theta_E %.2f arcsec (sample P: %.2f); median z_s %.2f"
      % (len(ZS), nH, np.median([SYS[i]["thE"] for i in ZS]) if ZS else float("nan"), np.median(E.arr(Pm, "tE")), np.median(list(ZS.values())) if ZS else float("nan")))
    P("\n[robustness, law S; reported]")
    reading("1 P, two-line classes only", Pm, zmap(rt, ids_ok=("HA2", "O3")))
    reading("2 P, tier TB only", Pm, zmap("TB"))
    reading("3 P, + AMBIGUOUS-OWN", Pm, zmap(rt, classes=("SECURE", "AMBIGUOUS-OWN")))
    reading("4 P, DESI deflector z", Pm, ZS, desi=True)
    RES["reading"] = {k_: {kk: vv for kk, vv in v.items() if kk not in ("b", "ids")} for k_, v in READ.items()}

    # per-system table
    if not MUT and not FINDER:
        bS = {i: {k_: v[j] for k_, v in rS["b"].items()} for j, i in enumerate(rS["ids"])} if rS["N"] else {}
        with open(os.path.join(HERE, tag + "_sources.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["unique_identifier", "grade", "in_P", "in_S", "class_TA", "class_TB", "line", "z_s", "midpoint_A", "k", "predicted_half_split_A", "sigma_A",
                        "sn_combined", "sn_RGS000", "sn_RGS180", "dchi2_over_centred", "support", "own_line_band", "arc_east_arcsec", "arc_north_arcsec",
                        "theta_E_arcsec", "z_lo", "z_up", "mer_object_id", "b_S_canonical", "b_S_alt", "b_inf_S_canonical", "b_inf_S_alt"])
            for i in [K.TRUTH[0]] + ids["S"] + ids["X"]:
                d = SYS[i]
                if not d["evaluable"]: continue
                ka, f_ = cls(i, "TA")
                if ka == "none": continue
                b = bS.get(i, {}) if ka == "SECURE" else {}
                w.writerow([i, d["grade"], d["inP"], d["inS"], ka, cls(i, "TB")[0], f_["idc"], "%.4f" % f_["z"], "%.1f" % f_["lam0"], "%.2f" % f_["k"], "%.1f" % f_["h"],
                            "%.0f" % f_["sig"], "%.2f" % f_["sn"], "%.2f" % f_["sn000"], "%.2f" % f_["sn180"], "%.1f" % f_["dchi"], "; ".join(f_["sup"]), f_.get("own", ""),
                            "%.2f" % f_["off"][0], "%.2f" % f_["off"][1], "%.3f" % d["thE"], "%.3f" % d["zlo"], "%.3f" % d["zup"], d["oid"]]
                           + [("%.4f" % b[c_]) if c_ in b else "" for c_ in ("S_canonical", "S_alt", "inf_S_canonical", "inf_S_alt")])
    if rP["N"]:
        P("  sample P per lens (law S): id, z_l, z_s, line, k, predicted half-split arcsec, theta_E, S/N, support, b canonical / alt (source-free alt)")
        for j in np.argsort([ZS[i] for i in rP["ids"]]):
            i = rP["ids"][j]; f_ = cls(i, rt)[1]
            P("    %s %.3f %.4f %-3s %.2f %.2f %.2f %5.1f %-22s %+.3f / %+.3f  (%+.3f)" % (i, key[i]["z"], ZS[i], f_["idc"], f_["k"], f_["h"] / C.DISP, key[i]["tE"], f_["sn"],
              "; ".join(f_["sup"]) or "-", rP["b"]["S_canonical"][j], rP["b"]["S_alt"][j], rP["b"]["inf_S_alt"][j]))

    # ---------------------------------------------------------------- EUC16 additions (reported)
    P("\n[EUC15's five certified lenses of P under this finder]")
    FV = {}
    for i in FIVE:
        d = SYS[i]; arc = d["arcs"][0] if d.get("arcs") else None
        ka, fa = cls(i, "TA") if d["evaluable"] else ("not evaluable", None); kb, fb = cls(i, "TB") if d["evaluable"] else ("not evaluable", None)
        FV[i] = dict(arc=None if arc is None else [float(arc[0]), float(arc[1])], evaluable=bool(d["evaluable"]), TA=ka, TB=kb,
                     z=None if fb is None else fb["z"], k=None if fb is None else fb["k"])
        P("  %s arc %s; evaluable %s; TA %s; TB %s%s" % (i, "none" if arc is None else "(%+.2f, %+.2f)" % tuple(arc), d["evaluable"], ka, kb,
          "" if fb is None else "  [z %.4f %s, k %.2f, half-split %.0f A]" % (fb["z"], fb["idc"], fb["k"], fb["h"])))
    RES["euc15_five"] = FV
    nsingle = sum(1 for i in rP.get("ids", []) if cls(i, rt)[1]["idc"] == "HA1")
    P("\n[single lines] certified lenses of P resting on one line (HA1): %d of %d" % (nsingle, rP["N"]))
    RES["N_P_single_line"] = nsingle
    P("\n[selection check] source-free b (law S, z_s at infinity) of the certified lenses against all of P")
    SEL = {}
    if rP["N"]:
        allP = {nm: E.run_b(engP, zP, REP, E.ZS_INF, a0, "S") for nm, a0 in E.FOOT.items()}
        pid = [r["id"] for r in Pm]; pos = {i: j for j, i in enumerate(pid)}
        for nm in E.FOOT:
            bc = np.array(rP["b"]["inf_S_" + nm]); ba = np.asarray(allP[nm], float)
            pr_ = [float(np.mean(ba <= x)) for x in bc]
            SEL[nm] = dict(cert_median=float(np.median(bc)), P_median=float(np.median(ba)), cert_percentiles=pr_, cert_mean_percentile=float(np.mean(pr_)))
            P("  %-9s certified (N %d) median %+.3f; all P (N %d) median %+.3f; certified lenses' percentiles in P: %s (mean %.2f)"
              % (nm, len(bc), np.median(bc), len(ba), np.median(ba), " ".join("%.2f" % x for x in pr_), np.mean(pr_)))
        thc = [key[i]["tE"] for i in rP["ids"]]; zc = [key[i]["z"] for i in rP["ids"]]
        SEL["thetaE"] = dict(cert_median=float(np.median(thc)), P_median=float(np.median(E.arr(Pm, "tE"))))
        SEL["z_l"] = dict(cert_median=float(np.median(zc)), P_median=float(np.median(E.arr(Pm, "z"))))
        P("  theta_E median: certified %.2f, P %.2f;  z_l median: certified %.3f, P %.3f" % (np.median(thc), np.median(E.arr(Pm, "tE")), np.median(zc), np.median(E.arr(Pm, "z"))))
    RES["selection_check"] = SEL
    LOO = {}
    if rP["N"] >= 2:
        P("\n[leave-one-out, law S, P; reported, never the word] interval bounds with each certified lens dropped")
        for nm in E.FOOT:
            lo_, hi_ = [], []
            for i in rP["ids"]:
                r_ = reading("LOO", Pm, {k_: v_ for k_, v_ in ZS.items() if k_ != i}, quiet=True)
                lo_.append(r_["S_" + nm]["true"]["b_med_lo"]); hi_.append(r_["S_" + nm]["true"]["b_med_hi"])
            READ.pop("LOO", None)
            LOO[nm] = dict(lo_min=float(min(lo_)), lo_max=float(max(lo_)), hi_min=float(min(hi_)), hi_max=float(max(hi_)))
            P("  %-9s lower bound %+.3f to %+.3f; upper bound %+.3f to %+.3f" % (nm, min(lo_), max(lo_), min(hi_), max(hi_)))
    RES["leave_one_out"] = LOO

    # ---------------------------------------------------------------- verdict
    P("\n[summary]")
    P("  instrument checks: %s;  coverage: %s;  reading tier: %s" % ("all pass" if allok else "FAILED", "pass" if cover_ok else "FAIL", tier or "none"))
    if evaluable:
        wc, wa = W["canonical"], W["alt"]
        if ident_dep:
            wc = wc if wc.startswith("EARLY") else "NO VERDICT"; wa = wa if wa.startswith("EARLY") else "NO VERDICT"
        v1 = "%s / %s" % (wc, wa)
        P("  N(P) with a secure source redshift = %d (EUC1-F needs %d)" % (rP["N"], F_NMIN))
        P("  EUC1-F (canonical / alt): %s%s" % (v1, " (IDENTIFICATION-DEPENDENT: the words flip with the identity of single lines)" if ident_dep else ""))
    else:
        v1 = "NOT EVALUABLE / NOT EVALUABLE"
        P("  EUC1-F: not graded.  (N(P) with a line passing the rule: %d; void)" % rP["N"])
    P("  LANE WORD (canonical / alt): %s%s" % (v1, (" [tier %s%s]" % (tier, "" if tier == "TA" else ", frozen fallback")) if evaluable else ""))
    P("  kappa = 1/2 FITTED. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    RES.update(checks=CK, checks_all_pass=allok, coverage_ok=cover_ok, tier=tier, evaluable=bool(evaluable), verdict=v1, words=W, words_identity=WID,
               identification_dependent=bool(ident_dep), N_P=rP["N"], N_S=rS["N"])
    code = 0 if evaluable else 3
    if MUT:
        try: ref = json.load(open(os.path.join(HERE, "euc16_results.json")))
        except Exception: ref = None
        bite = False
        if ref is None: P("\n[MUTATE %s] no reference results: cannot judge" % MUT)
        elif MUT == "newton":
            samp = next((s for s in ("P", "S") if ref["reading"].get(s, {}).get("N", 0) >= 1 and READ.get(s, {}).get("N", 0) >= 1), None)
            up_a = all(anc[k_] > ref["anchor_b"][k_] for k_ in E.FOOT)
            up_s = samp is not None and all(READ[samp]["S_" + k_]["true"]["b_med"] > ref["reading"][samp]["S_" + k_]["true"]["b_med"] for k_ in E.FOOT)
            bite = up_a and (up_s or samp is None)
            P("\n[MUTATE newton] anchor b %+.3f / %+.3f (ref %+.3f / %+.3f); sample %s -> %s" % (anc["canonical"], anc["alt"], ref["anchor_b"]["canonical"], ref["anchor_b"]["alt"], samp,
              "rose on both footings, as required; exit 1" if bite else "DID NOT RISE"))
        elif MUT == "nowindow":
            n0, n1 = ref["pre_guard_TA_total"], RES["pre_guard_TA_total"]
            bite = n1 > n0
            P("\n[MUTATE nowindow] (system, variant) pairs of S and X with a TA candidate before identity and guards, k window removed: %d (ref %d) -> %s"
              % (n1, n0, "rose, as required; exit 1" if bite else "DID NOT RISE"))
        RES["mutate_bites"] = bool(bite); code = 1 if bite else 2
    if FINDER == "v1":                                                      # check K8 against EUC15's committed results
        ref = json.load(open(os.path.join(EUC15_DIR, "euc15_results.json")))
        same_cov = all(RES["coverage"][nm][k_] == ref["coverage"][nm][k_] for nm in ("P", "S", "X") for k_ in ("spectrum", "box", "with_arc", "evaluable"))
        same_g = all(GATE[t][g] == ref["gates"][t][g] for t in GATE for g in ("H2", "H3", "H2b", "H4")) and all(
            GATE[t]["counts"][nm][k_] == ref["gates"][t]["counts"][nm][k_] for t in GATE for nm in ("P", "S", "X") for k_ in ("E", "SECURE", "AMBIG", "CONFLICT", "flip", "rot", "mirror"))
        same_pre = RES["pre_guard_TA"] == ref["pre_guard_TA"] and RES["N_P"] == ref["N_P"] and RES["N_S"] == ref["N_S"]
        RES["check_ok"] = bool(same_cov and same_g and same_pre)
        RES["check_value"] = "coverage %s, gate counts %s, pre-guard and N(P), N(S) %s (EUC15: N(P) %d)" % (
            "same" if same_cov else "DIFFERENT", "same" if same_g else "DIFFERENT", "same" if same_pre else "DIFFERENT", ref["N_P"])
        P("\n[CHECK K8] EUC15's finder in this code: %s -> %s" % (RES["check_value"], "PASS" if RES["check_ok"] else "FAIL"))
        code = 0 if RES["check_ok"] else 4
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

if __name__ == "__main__":
    main()
