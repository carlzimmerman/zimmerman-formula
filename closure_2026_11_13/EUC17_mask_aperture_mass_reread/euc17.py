#!/usr/bin/env python3
"""EUC17 (MASK-APERTURE STELLAR MASS, EUCLID LENS ROWS RE-READ).
Frozen criteria: FROZEN_CRITERIA.md (commit 8b31c449c9) with AMENDMENT_A1.md (commit e3db93ac26).

The ECLIPSE catalogue's stellar mass is the mass of the Sersic model inside the modelling circle (ECLIPSE-D
Sect. 3.1 / 3.2 / 6.1).  EUC1 and its children take it as the total of an infinite Sersic body.  Per lens
f = M2D_frac(mask radius, R_e, n) and b_corr = b + log10 f.  Rows R1 (EUC1), R2 (EUC4), R3 (EUC1-F as EUC16
graded it) are re-read with their own statistics, lines and words.

Run:
  python3 -I euc17.py --data-dir <dir with the two ECLIPSE csv files>
  EUC17_MUTATE=nomask python3 -I euc17.py --data-dir <dir>      (must exit 1)
  EUC17_MUTATE=invert python3 -I euc17.py --data-dir <dir>      (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  A re-read: adopts nothing; no outcome is a pass of the lensing gate.
"""
import argparse, csv, glob, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D12 = os.path.join(REPO, "closure_2026_11_12")
D13 = os.path.join(REPO, "closure_2026_11_13")
sys.path.insert(0, os.path.join(D12, "EUC1_eclipse_saturation_ceiling"))
sys.path.insert(0, os.path.join(D12, "EUC4_wide_lenses"))
import euc1 as E          # noqa: E402   (EUC1's own code: load, select, build, Engine, stats, word, M2D_frac)
import euc4 as W          # noqa: E402   (EUC4's word rule)

MUT = (os.environ.get("EUC17_MUTATE", "") or "").strip()
if MUT not in ("", "nomask", "invert"):
    sys.exit("unknown EUC17_MUTATE")
TAG = "euc17" + ("_MUTATE_" + MUT if MUT else "")
VARIANTS = ("primary", "F1a", "F1b", "F2", "F3a", "F3b", "F4", "F5")
VAR_TEXT = {"primary": "as frozen", "F1a": "f with R_e x 0.80", "F1b": "f with R_e x 1.25", "F2": "f with n = 4",
            "F3a": "mask radius + |mask centre|", "F3b": "mask radius - |mask centre|",
            "F4": "no-mask lenses kept at f = 1", "F5": "lenses with n > 9.5 dropped"}
G_HOLDS, G_FAILS = 0.15, 0.25          # EUC1-F lines (EUC1 RESULT section 8)
NOMASK_MAX = 0.05
F_EUC1 = os.path.join(D12, "EUC1_eclipse_saturation_ceiling")
F_EUC4 = os.path.join(D12, "EUC4_wide_lenses")
F_EUC10 = os.path.join(D12, "EUC10_published_source_redshifts")
F_EUC16 = os.path.join(D13, "EUC16_better_arc_finder_source_redshifts")

OUT = []
def P(s=""):
    print(s); OUT.append(s)

def fnum(v):
    try:
        return float(v)
    except Exception:
        return float("nan")

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def word_gate(st):
    if st["N"] < 10: return "NOT EVALUABLE"
    if st["b_med_hi"] <= G_HOLDS: return "LENS GATE HOLDS"
    if st["b_med_lo"] >= G_FAILS: return "LENS GATE FAILS"
    return "NO VERDICT"

# ------------------------------------------------------------------ masks and the in-mask share
def load_masks():
    M = {}
    for r in read_csv(os.path.join(HERE, "euc17_masks.csv")):
        ok = r["has_mask"] == "1"
        M[r["unique_identifier"]] = dict(
            ok=ok, R=fnum(r["mask_radius_arcsec"]) if ok else float("nan"),
            off=math.hypot(fnum(r["mask_centre_0"]), fnum(r["mask_centre_1"])) if ok else float("nan"))
    return M

def logf(ids, te, n, variant, M):
    """log10 of the in-mask share per lens for one variant; NaN = the lens is dropped in this variant."""
    te = np.asarray(te, float).copy(); n0 = np.asarray(n, float); n = n0.copy()
    if MUT == "nomask":
        return np.zeros(len(ids))
    R = np.array([M[i]["R"] if (i in M and M[i]["ok"]) else np.nan for i in ids], float)
    off = np.array([M[i]["off"] if (i in M and M[i]["ok"]) else np.nan for i in ids], float)
    if variant == "F1a": te *= 0.80
    if variant == "F1b": te *= 1.25
    if variant == "F2": n = np.full(len(ids), 4.0)
    if variant == "F3a": R = R + off
    if variant == "F3b": R = R - off
    good = np.isfinite(R) & (R > 0)
    lf = np.full(len(ids), np.nan)
    if good.any():
        lf[good] = np.log10(E.M2D_frac(R[good], te[good], n[good]))
    if variant == "F4": lf = np.where(np.isfinite(lf), lf, 0.0)
    if variant == "F5": lf[n0 > 9.5] = np.nan
    if MUT == "invert": lf = -lf
    return lf

def cmp_stats(st, ref, tol_pt, tol_fr, tol_bd=0.01):
    bad = []
    if abs(st["b_med"] - ref["b_med"]) > tol_pt: bad.append("b_med %.3e" % abs(st["b_med"] - ref["b_med"]))
    for k in ("f25", "f0"):
        if abs(st[k] - ref[k]) > tol_fr: bad.append("%s %.3e" % (k, abs(st[k] - ref[k])))
    for k in ("f25_lo", "f25_hi", "f0_lo", "f0_hi", "b_med_lo", "b_med_hi"):
        if abs(st[k] - ref[k]) > tol_bd: bad.append("%s %.3e" % (k, abs(st[k] - ref[k])))
    if st["N"] != ref["N"]: bad.append("N %d vs %d" % (st["N"], ref["N"]))
    if "word" in ref and "word" in st and st["word"] != ref["word"]: bad.append("word %s vs %s" % (st["word"], ref["word"]))
    return bad

def fmt(st):
    return ("N=%5d  f25 = %.3f [%.3f, %.3f]  f0 = %.3f  b_med = %+.3f [%+.3f, %+.3f]"
            % (st["N"], st["f25"], st["f25_lo"], st["f25_hi"], st["f0"], st["b_med"], st["b_med_lo"], st["b_med_hi"]))

# ------------------------------------------------------------------ K4: premise spot-check on FOR J0332
def k4(k4dir):
    from astropy.io import fits
    from scipy.special import gammaincinv, gammaln
    info = json.load(open(os.path.join(k4dir, "dataset", "info.json")))
    pix, R = float(info["pixel_scale"]), float(info["mask_radius"])
    c0, c1 = float(info["mask_centre"][0]), float(info["mask_centre"][1])
    mags = {r["waveband"]: r for r in read_csv(os.path.join(k4dir, "results", "magnitudes.csv"))}
    tiles = [p for p in glob.glob(os.path.join(k4dir, "dataset", "*.fits"))]
    par = json.load(open(os.path.join(k4dir, "results", "coolest_sersic.json")))["lensing_entities"][0]["light_model"][0]["parameters"]
    v = lambda k: float(par[k]["point_estimate"]["value"])
    rows = []
    with fits.open(os.path.join(k4dir, "results", "pre_psf.fits")) as pre, fits.open(tiles[0]) as hd:
        for band in sorted(mags):
            B = band.upper()
            a = np.array(pre[B + "_GALAXY_0"].data, float)
            zp = float(hd[B + "_BGSUB"].header["MAGZERO"]); conv = 3631.0e6 * 10.0 ** (-0.4 * zp)
            ny, nx = a.shape; yy, xx = np.indices(a.shape)
            X = (xx - 0.5 * (nx - 1)) * pix; Y = (yy - 0.5 * (ny - 1)) * pix
            best = None
            for sx, sy, tag in ((c1, -c0, "x=c1,y=-c0"), (c1, c0, "x=c1,y=c0"), (c0, c1, "x=c0,y=c1"), (c0, -c1, "x=c0,y=-c1")):
                circ = (X - sx) ** 2 + (Y - sy) ** 2 < R * R
                nout = int(np.count_nonzero(a[~circ]))
                if best is None or nout < best[0]: best = (nout, tag, float(a[circ].sum()))
            cat = float(mags[band]["lens_flux_max_lh"]); catmed = float(mags[band]["lens_flux"])
            rows.append(dict(band=band, magzero=zp, in_circle_microJy=best[2] * conv, whole_map_microJy=float(a.sum()) * conv,
                             nonzero_outside_circle=best[0], centre_convention=best[1], catalogue_max_lh_microJy=cat,
                             catalogue_median_microJy=catmed, ratio_max_lh=best[2] * conv / cat, ratio_median=best[2] * conv / catmed))
        zpv = float(hd["VIS_BGSUB"].header["MAGZERO"]); convv = 3631.0e6 * 10.0 ** (-0.4 * zpv)
    re_, n_, q_ = v("theta_eff"), v("n"), v("q")
    bn = float(gammaincinv(2.0 * n_, 0.5))
    tot = v("I_eff") / pix ** 2 * 2.0 * math.pi * re_ ** 2 * n_ * math.exp(bn + gammaln(2.0 * n_) - 2.0 * n_ * math.log(bn)) * convv
    vis = next(r for r in rows if r["band"] == "vis")
    out = dict(mask_radius=R, bands=rows, infinite_total_VIS_microJy_circularised=tot, infinite_total_VIS_microJy_major_axis=tot * q_,
               infinite_over_catalogue_circularised=tot / vis["catalogue_max_lh_microJy"],
               infinite_over_catalogue_major_axis=tot * q_ / vis["catalogue_max_lh_microJy"],
               shape=dict(theta_eff=re_, n=n_, q=q_))
    ok = abs(vis["ratio_max_lh"] - 1.0) <= 0.03 and out["infinite_over_catalogue_circularised"] > 1.10
    return ok, out

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--k4-dir", default=os.path.join(REPO, "euclid_for_j0332_fit_2026_11_13", "inputs"))
    a = ap.parse_args()
    t0 = time.time()
    P("EUC17 (MASK-APERTURE STELLAR MASS, EUCLID LENS ROWS RE-READ)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("criteria 8b31c449c9, amendment A1 e3db93ac26;  footings (m/s^2): canonical %.4e, alt %.4e" % (E.FOOT["canonical"], E.FOOT["alt"]))
    rows, _ = E.load(a.data_dir)
    for s in E.OUT: OUT.append(s)
    E.OUT.clear()
    byid = {r["id"]: r for r in rows}
    M = load_masks()
    RES = dict(lane="EUC17", criteria_commit="8b31c449c9", amendment_A1="e3db93ac26", mutate=MUT, footings=E.FOOT)
    CK = {}
    def ck(name, what, ok, value=None):
        CK[name] = dict(what=what, ok=bool(ok), value=value)
        P("  %s %-4s %s" % ("PASS" if ok else "FAIL", name, what))

    nm_all = sum(1 for m in M.values() if m["ok"])
    P("\n[masks] table rows %d; with a mask %d; without %d" % (len(M), nm_all, len(M) - nm_all))
    RES["masks"] = dict(rows=len(M), with_mask=nm_all)

    # ---------------------------------------------------------------- samples and full-precision boosts (A1 change 1)
    Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",))
    WB = [r for r in Bm if r["tE"] >= 1.7]
    SEC = [r for r in Bm if 1.3 <= r["tE"] < 1.7]
    CMP = [r for r in Bm if r["tE"] < 1.0]
    GROUPS = [("R1 P", Pm), ("R2 W_B", WB), ("EUC4 secondary", SEC), ("EUC4 complement", CMP)]
    EUC4_NAME = {"R2 W_B": "W_B: theta_E >= 1.7 arcsec (primary)", "EUC4 secondary": "secondary: 1.3 <= theta_E < 1.7",
                 "EUC4 complement": "complement: theta_E < 1.0"}
    KEYS = [(law, nm) for law in ("S", "B") for nm in E.FOOT]
    B = {}
    for gname, smp in GROUPS:
        eng, z, RE, Re, n, lm = E.build(smp)
        Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        B[gname] = dict(ids=[r["id"] for r in smp], te=E.arr(smp, "te"), n=E.arr(smp, "n"), tE=E.arr(smp, "tE"),
                        b={k: eng.solve_b(Mmin, E.FOOT[k[1]], k[0]) for k in KEYS})
    P("samples: P %d, W_B %d, secondary %d, complement %d" % (len(Pm), len(WB), len(SEC), len(CMP)))

    # ---------------------------------------------------------------- committed references
    ref1 = json.load(open(os.path.join(F_EUC1, "euc1_results.json")))
    ref4 = json.load(open(os.path.join(F_EUC4, "euc4_results.json")))
    ref16 = json.load(open(os.path.join(F_EUC16, "euc16_results.json")))
    ref10 = json.load(open(os.path.join(F_EUC10, "euc10_results.json")))

    # R3 lenses and the readings that use committed per-lens columns (A1 change 2)
    src = [r for r in read_csv(os.path.join(F_EUC16, "euc16_sources.csv"))
           if r["in_P"] == "True" and r["class_TB"] == "SECURE" and r["b_S_canonical"].strip()]
    R3 = dict(ids=[r["unique_identifier"] for r in src],
              b={"canonical": np.array([fnum(r["b_S_canonical"]) for r in src]), "alt": np.array([fnum(r["b_S_alt"]) for r in src])})
    R3["te"] = np.array([byid[i]["te"] for i in R3["ids"]]); R3["n"] = np.array([byid[i]["n"] for i in R3["ids"]])
    r10 = [r for r in read_csv(os.path.join(F_EUC10, "euc10_per_lens.csv")) if r["b_S_canonical"].strip()]
    R10 = dict(ids=[r["eclipse_id"] for r in r10],
               b={"canonical": np.array([fnum(r["b_S_canonical"]) for r in r10]), "alt": np.array([fnum(r["b_S_alt"]) for r in r10])})
    R10["te"] = np.array([byid[i]["te"] for i in R10["ids"]]); R10["n"] = np.array([byid[i]["n"] for i in R10["ids"]])
    c1 = {r["unique_identifier"]: r for r in read_csv(os.path.join(F_EUC1, "euc1_per_lens.csv"))}
    c4 = {r["unique_identifier"]: r for r in read_csv(os.path.join(F_EUC4, "euc4_per_lens.csv"))}
    COND = {rd: np.array([fnum(c1[i]["b_S_alt_" + rd]) for i in B["R1 P"]["ids"]]) for rd in ("R3", "R2")}

    # ---------------------------------------------------------------- checks
    P("\n[checks]")
    # K0: f = 1 reproduces every committed statistic and word
    k0bad = []
    rng = np.random.default_rng(E.SEED)
    for law, nm in KEYS:
        st = E.stats(B["R1 P"]["b"][(law, nm)], rng); st["word"] = E.word(st)
        bad = cmp_stats(st, ref1["primary"]["%s_%s" % (law, nm)], 1e-9, 1e-9)
        if bad: k0bad.append("R1 %s %s: %s" % (law, nm, "; ".join(bad)))
    rng = np.random.default_rng(E.SEED)
    for gname in ("R2 W_B", "EUC4 secondary", "EUC4 complement"):
        for law, nm in KEYS:
            st = E.stats(B[gname]["b"][(law, nm)], rng); st["word"] = W.word(st)
            bad = cmp_stats(st, ref4["partA"][EUC4_NAME[gname]]["%s_%s" % (law, nm)], 1e-9, 1e-9)
            if bad: k0bad.append("%s %s %s: %s" % (gname, law, nm, "; ".join(bad)))
    for nm in E.FOOT:
        st = E.stats(R3["b"][nm]); st["word"] = word_gate(st)
        bad = cmp_stats(st, ref16["reading"]["P"]["S_" + nm]["true"], 1e-4, 1.0 / max(st["N"], 1) + 1e-12)
        if bad: k0bad.append("R3 %s: %s" % (nm, "; ".join(bad)))
        st = E.stats(R10["b"][nm])
        bad = cmp_stats(st, ref10["readings"]["all matched with valid inputs, law S"][nm], 1e-4, 1.0 / max(st["N"], 1) + 1e-12)
        if bad: k0bad.append("EUC10 reading %s: %s" % (nm, "; ".join(bad)))
    for rd in ("R3", "R2"):
        bb = COND[rd][np.isfinite(COND[rd])]
        st = E.stats(bb); st["word"] = E.word(st)
        bad = cmp_stats(st, ref1["conditional"]["%s_S_alt" % rd], 1e-4, 1.0 / max(st["N"], 1) + 1e-12)
        if bad: k0bad.append("EUC1 conditional %s alt: %s" % (rd, "; ".join(bad)))
    ck("K0", "f = 1 reproduces every committed statistic and word (R1, R2, R3, EUC4 bins, EUC10 reading, EUC1 conditional)%s"
       % ("" if not k0bad else ": " + " | ".join(k0bad)), not k0bad, k0bad)
    w16 = [word_gate(dict(N=ref16["reading"]["P"]["S_" + nm]["true"]["N"], **{k: ref16["reading"]["P"]["S_" + nm]["true"][k] for k in ("b_med_lo", "b_med_hi")})) for nm in E.FOOT]
    P("       committed words: R1 %s / %s; R2 %s / %s; R3 %s / %s" % (
        ref1["primary"]["S_canonical"]["word"], ref1["primary"]["S_alt"]["word"],
        ref4["partA"][EUC4_NAME["R2 W_B"]]["S_canonical"]["word"], ref4["partA"][EUC4_NAME["R2 W_B"]]["S_alt"]["word"], w16[0], w16[1]))

    # K0b: full-precision boosts against the committed four-decimal files
    d1 = max(abs(B["R1 P"]["b"][(law, nm)][j] - fnum(c1[i]["b_%s_%s" % (law, nm)]))
             for law, nm in KEYS for j, i in enumerate(B["R1 P"]["ids"]))
    d4 = max(abs(B["R2 W_B"]["b"][("S", nm)][j] - fnum(c4[i]["b_inf_S_" + nm])) for nm in E.FOOT for j, i in enumerate(B["R2 W_B"]["ids"]))
    ck("K0b", "computed boosts equal the committed four-decimal values: max |diff| P %.1e, W_B %.1e (limit 6e-5)" % (d1, d4),
       d1 <= 6e-5 and d4 <= 6e-5, [float(d1), float(d4)])

    # K1: the share function
    e1 = max(abs(float(E.M2D_frac(1.0, 1.0, nn)) - 0.5) for nn in (1.0, 4.0, 8.0))
    b1 = float(E.b_ser(1.0))
    e2 = max(abs(float(E.M2D_frac(x, 1.0, 1.0)) - (1.0 - (1.0 + b1 * x) * math.exp(-b1 * x))) for x in (0.5, 2.0, 5.0))
    ck("K1", "M2D_frac(R_e) = 0.5 for n = 1, 4, 8: max err %.1e (1e-6); n = 1 closed form: max err %.1e (1e-8)" % (e1, e2),
       e1 <= 1e-6 and e2 <= 1e-8, [e1, e2])

    # K2: shift identity through EUC1's own solver on 20 lenses of P
    lfP = logf(B["R1 P"]["ids"], B["R1 P"]["te"], B["R1 P"]["n"], "primary", M)
    if MUT == "invert": lfP_true = -lfP
    else: lfP_true = lfP
    have = np.where(np.isfinite(lfP_true))[0]
    step = max(len(have) // 20, 1)
    pick = have[::step][:20]
    sub = [Pm[i] for i in pick]
    lm_new = E.arr(sub, "lm") - lfP_true[pick]
    eng, z, RE, Re, n, lm = E.build(sub, lm=lm_new)
    Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
    e = max(float(np.max(np.abs(eng.solve_b(Mmin, E.FOOT[nm], law) - (B["R1 P"]["b"][(law, nm)][pick] + lfP_true[pick])))) for law, nm in KEYS)
    ck("K2", "shift identity b(M*/f) = b + log10 f on %d lenses of P, laws S and B, both footings: max err %.1e (1e-6)" % (len(pick), e),
       e <= 1e-6 and len(pick) == 20, float(e))

    # K3: geometry
    allf, nsmall = [], 0
    for gname in ("R1 P", "R2 W_B"):
        g = B[gname]; lf = logf(g["ids"], g["te"], g["n"], "primary", M)
        if MUT == "invert": lf = -lf
        if MUT != "nomask":
            Rm = np.array([M[i]["R"] if (i in M and M[i]["ok"]) else np.nan for i in g["ids"]])
            nsmall += int(np.sum(Rm < g["tE"]))
        allf.append(10.0 ** lf[np.isfinite(lf)])
    allf = np.concatenate(allf)
    ok3 = bool(np.all(allf > 0.0) and np.all(allf <= 1.0 + 1e-12))
    ck("K3", "every mask radius > 0 and f in (0, 1]: f range %.4f to %.4f over %d lenses; mask radius < theta_E in %d lenses"
       % (allf.min(), allf.max(), len(allf), nsmall), ok3, dict(fmin=float(allf.min()), fmax=float(allf.max()), mask_lt_thetaE=nsmall))

    # K4: premise spot-check
    try:
        ok4, K4 = k4(a.k4_dir)
        vis = next(r for r in K4["bands"] if r["band"] == "vis")
        ck("K4", "FOR J0332 premise: in-mask sum of the released lens-light map / catalogue flux (VIS, max-lh) = %.4f (within 3 %%); "
                 "analytic infinite total / catalogue flux = %.3f (> 1.10)" % (vis["ratio_max_lh"], K4["infinite_over_catalogue_circularised"]), ok4, K4)
        for r in K4["bands"]:
            P("         %-8s in-mask %.4f uJy; catalogue max-lh %.4f (ratio %.4f), median %.4f (ratio %.4f); non-zero pixels outside the circle %d"
              % (r["band"], r["in_circle_microJy"], r["catalogue_max_lh_microJy"], r["ratio_max_lh"], r["catalogue_median_microJy"], r["ratio_median"], r["nonzero_outside_circle"]))
        P("         infinite total / catalogue if theta_eff were a major-axis radius: %.3f (reported; the released library's radius is circularised)"
          % K4["infinite_over_catalogue_major_axis"])
    except Exception as ex:
        ck("K4", "FOR J0332 premise spot-check could not run: %s" % type(ex).__name__, False)

    # K5: the two lenses with fractions from the other agent's work (reported)
    K5 = {}
    for i, other in (("EUCL-DR1-L014994", 0.804), ("EUCL-DR1-L015780", 0.587)):
        if i in M and M[i]["ok"] and i in byid:
            f = float(E.M2D_frac(M[i]["R"], byid[i]["te"], byid[i]["n"]))
            K5[i] = dict(mask_radius=M[i]["R"], theta_e=byid[i]["te"], n=byid[i]["n"], f=f, other_agent=other)
            P("  note K5   %s: mask %.3f arcsec, theta_e %.3f, n %.2f -> f = %.4f (other agent's elliptical best-fit value %.3f)"
              % (i, M[i]["R"], byid[i]["te"], byid[i]["n"], f, other))
    CK["K5"] = dict(what="reported, no threshold", ok=True, value=K5)
    checks_ok = all(c["ok"] for c in CK.values())
    RES["checks"] = CK; RES["checks_all_pass"] = checks_ok

    # ---------------------------------------------------------------- the re-read
    def reread(variant):
        out = {}
        # R1
        g = B["R1 P"]; lf = logf(g["ids"], g["te"], g["n"], variant, M); keep = np.isfinite(lf)
        rng = np.random.default_rng(E.SEED); r1 = {}
        for law, nm in KEYS:
            st = E.stats(g["b"][(law, nm)][keep] + lf[keep], rng); st["word"] = E.word(st)
            st["uncorrected_same_lenses"] = dict(f25=float(np.mean(g["b"][(law, nm)][keep] > E.B_STAR)), b_med=float(np.median(g["b"][(law, nm)][keep])))
            r1["%s_%s" % (law, nm)] = st
        out["R1"] = dict(stats=r1, N_all=len(keep), N_kept=int(keep.sum()), no_mask_frac=float(1.0 - keep.mean()))
        # R2 and EUC4's bins
        rng = np.random.default_rng(E.SEED)
        for gname in ("R2 W_B", "EUC4 secondary", "EUC4 complement"):
            g = B[gname]; lf = logf(g["ids"], g["te"], g["n"], variant, M); keep = np.isfinite(lf); rr = {}
            nomask = float(1.0 - keep.mean()) if len(keep) else 1.0
            for law, nm in KEYS:
                if keep.sum() == 0:
                    rr["%s_%s" % (law, nm)] = dict(N=0, word="NOT EVALUABLE")
                    continue
                st = E.stats(g["b"][(law, nm)][keep] + lf[keep], rng); st["word"] = W.word(st)
                st["uncorrected_same_lenses"] = dict(f25=float(np.mean(g["b"][(law, nm)][keep] > E.B_STAR)), b_med=float(np.median(g["b"][(law, nm)][keep])))
                rr["%s_%s" % (law, nm)] = st
            out[gname] = dict(stats=rr, N_all=len(keep), N_kept=int(keep.sum()), no_mask_frac=nomask)
        # R3 and the EUC10 reading
        for name, g, wf in (("R3", R3, word_gate), ("EUC10 reading", R10, None)):
            lf = logf(g["ids"], g["te"], g["n"], variant, M); keep = np.isfinite(lf); rr = {}
            for nm in E.FOOT:
                if keep.sum() == 0:
                    rr["S_" + nm] = dict(N=0, word="NOT EVALUABLE"); continue
                st = E.stats(g["b"][nm][keep] + lf[keep])
                if wf: st["word"] = wf(st)
                st["uncorrected_same_lenses"] = dict(f25=float(np.mean(g["b"][nm][keep] > E.B_STAR)), b_med=float(np.median(g["b"][nm][keep])))
                rr["S_" + nm] = st
            out[name] = dict(stats=rr, N_all=len(keep), N_kept=int(keep.sum()), no_mask_frac=float(1.0 - keep.mean()),
                             lenses=[dict(id=i, log10f=(float(l) if np.isfinite(l) else None)) for i, l in zip(g["ids"], lf)])
        # EUC1's conditional readings, alt footing (would-be words)
        g = B["R1 P"]; lf = logf(g["ids"], g["te"], g["n"], variant, M)
        for rd in ("R3", "R2"):
            keep = np.isfinite(lf) & np.isfinite(COND[rd])
            st = E.stats(COND[rd][keep] + lf[keep]); st["word"] = E.word(st)
            out["EUC1 conditional " + rd] = dict(stats={"S_alt": st}, N_kept=int(keep.sum()))
        # the 5 % rule
        for name in ("R1", "R2 W_B", "EUC4 secondary", "EUC4 complement", "R3"):
            if out[name]["no_mask_frac"] > NOMASK_MAX and variant != "F4":
                for k in out[name]["stats"]:
                    out[name]["stats"][k]["word_before_5pct_rule"] = out[name]["stats"][k].get("word")
                    out[name]["stats"][k]["word"] = "NOT EVALUABLE"
        return out

    ALL = {v: reread(v) for v in VARIANTS}
    PRI = ALL["primary"]
    RES["reread"] = ALL

    def line(name, key, st):
        if st.get("N", 0) == 0:
            P("  %-22s %-13s no lens with a mask -> %s" % (name, key, st["word"])); return
        P("  %-22s %-13s %s%s" % (name, key, fmt(st), ("   -> %s" % st["word"]) if "word" in st else ""))

    P("\n[re-read, corrected stellar mass, primary f]")
    for name in ("R1", "R2 W_B", "EUC4 secondary", "EUC4 complement"):
        P("  %s: lenses %d, with a mask %d (no mask %.1f %%)" % (name, PRI[name]["N_all"], PRI[name]["N_kept"], 100.0 * PRI[name]["no_mask_frac"]))
        for law, nm in KEYS: line(name, "law %s %s" % (law, nm), PRI[name]["stats"]["%s_%s" % (law, nm)])
    for name in ("R3", "EUC10 reading"):
        P("  %s: lenses %d, with a mask %d" % (name, PRI[name]["N_all"], PRI[name]["N_kept"]))
        for nm in E.FOOT: line(name, "law S %s" % nm, PRI[name]["stats"]["S_" + nm])
    for rd in ("R3", "R2"):
        line("EUC1 conditional " + rd, "law S alt", PRI["EUC1 conditional " + rd]["stats"]["S_alt"])

    # ---------------------------------------------------------------- labels
    COMMIT = {"R1": {nm: ref1["primary"]["S_" + nm]["word"] for nm in E.FOOT},
              "R2 W_B": {nm: ref4["partA"][EUC4_NAME["R2 W_B"]]["S_" + nm]["word"] for nm in E.FOOT},
              "R3": dict(zip(E.FOOT, w16))}
    COMSTAT = {"R1": {nm: ref1["primary"]["S_" + nm] for nm in E.FOOT},
               "R2 W_B": {nm: ref4["partA"][EUC4_NAME["R2 W_B"]]["S_" + nm] for nm in E.FOOT},
               "R3": {nm: ref16["reading"]["P"]["S_" + nm]["true"] for nm in E.FOOT}}
    P("\n[labels, law S]")
    LAB = {}
    for row in ("R1", "R2 W_B", "R3"):
        LAB[row] = {}
        for nm in E.FOOT:
            st = PRI[row]["stats"]["S_" + nm]; w = st["word"]
            diff = [v for v in VARIANTS[1:] if ALL[v][row]["stats"]["S_" + nm]["word"] != w]
            LAB[row][nm] = dict(committed=COMMIT[row][nm], corrected=w, change="UNCHANGED" if w == COMMIT[row][nm] else "CHANGED",
                                stability="FRAGILE" if diff else "ROBUST", brackets_with_other_word=diff)
            cs = COMSTAT[row][nm]
            if row == "R3":
                P("  %-7s %-9s committed %s (b_med %+.3f [%+.3f, %+.3f]) -> corrected %s (b_med %+.3f [%+.3f, %+.3f]): %s, %s%s"
                  % (row, nm, COMMIT[row][nm], cs["b_med"], cs["b_med_lo"], cs["b_med_hi"], w, st.get("b_med", float("nan")), st.get("b_med_lo", float("nan")),
                     st.get("b_med_hi", float("nan")), LAB[row][nm]["change"], LAB[row][nm]["stability"], (" (" + ", ".join(diff) + ")") if diff else ""))
            else:
                P("  %-7s %-9s committed %s (f25 %.3f [%.3f, %.3f]) -> corrected %s (f25 %.3f [%.3f, %.3f]): %s, %s%s"
                  % (row, nm, COMMIT[row][nm], cs["f25"], cs["f25_lo"], cs["f25_hi"], w, st.get("f25", float("nan")), st.get("f25_lo", float("nan")),
                     st.get("f25_hi", float("nan")), LAB[row][nm]["change"], LAB[row][nm]["stability"], (" (" + ", ".join(diff) + ")") if diff else ""))
    RES["labels"] = LAB

    P("\n[brackets, law S: R1 f25 | R2 f25 | R3 b_med, canonical / alt, with the word]")
    for v in VARIANTS:
        s = "  %-8s %-30s" % (v, VAR_TEXT[v])
        for row, key in (("R1", "f25"), ("R2 W_B", "f25"), ("R3", "b_med")):
            a_, b_ = ALL[v][row]["stats"]["S_canonical"], ALL[v][row]["stats"]["S_alt"]
            s += " | %s %+.3f / %+.3f (N %d) %s / %s" % (row, a_.get(key, float("nan")), b_.get(key, float("nan")), a_.get("N", 0), a_["word"], b_["word"])
        P(s)

    # ---------------------------------------------------------------- S1 and descriptive
    P("\n[S1: size of the correction, -log10 f, primary f]")
    S1 = {}
    g = B["R1 P"]; lf = logf(g["ids"], g["te"], g["n"], "primary", M)
    if MUT == "invert": lf = -lf
    def q3(x):
        x = x[np.isfinite(x)]
        return [float(v) for v in np.percentile(-x, [16, 50, 84])] if len(x) else [float("nan")] * 3
    S1["P all"] = dict(N=int(np.isfinite(lf).sum()), q=q3(lf))
    P("  P, all lenses (N %d): median %.3f dex [16-84 %%: %.3f, %.3f]" % (S1["P all"]["N"], S1["P all"]["q"][1], S1["P all"]["q"][0], S1["P all"]["q"][2]))
    for lo, hi in ((0.0, 1.0), (1.0, 1.3), (1.3, 1.7), (1.7, 99.0)):
        m = (g["tE"] >= lo) & (g["tE"] < hi)
        k = "P theta_E %.1f-%.1f" % (lo, hi); S1[k] = dict(N=int((m & np.isfinite(lf)).sum()), q=q3(lf[m]))
        P("  P, %.1f <= theta_E < %.1f arcsec (N %d): median %.3f dex [%.3f, %.3f]" % (lo, hi, S1[k]["N"], S1[k]["q"][1], S1[k]["q"][0], S1[k]["q"][2]))
    g4 = B["R2 W_B"]; lf4 = logf(g4["ids"], g4["te"], g4["n"], "primary", M)
    if MUT == "invert": lf4 = -lf4
    S1["W_B"] = dict(N=int(np.isfinite(lf4).sum()), q=q3(lf4))
    P("  W_B (N %d): median %.3f dex [%.3f, %.3f]" % (S1["W_B"]["N"], S1["W_B"]["q"][1], S1["W_B"]["q"][0], S1["W_B"]["q"][2]))
    S1["P frac above 0.10 dex"] = float(np.mean(-lf[np.isfinite(lf)] > 0.10)); S1["P frac above 0.20 dex"] = float(np.mean(-lf[np.isfinite(lf)] > 0.20))
    P("  P: share of lenses with a correction above 0.10 dex: %.3f; above 0.20 dex: %.3f" % (S1["P frac above 0.10 dex"], S1["P frac above 0.20 dex"]))
    P("  on the record (quoted, not recomputed): the catalogue masses are 0.23 dex above the Euclid pipeline's own (EUC1 criteria);")
    P("  EUC12: the uncorrected ECLIPSE scale agrees with Auger 2009 and DESI CIGALE to about 0.05 dex.")
    RES["S1"] = S1
    P("  R3 lenses, -log10 f: %s" % ", ".join("%s %.3f" % (d["id"][-7:], -d["log10f"]) if d["log10f"] is not None else "%s none" % d["id"][-7:] for d in PRI["R3"]["lenses"]))
    P("  EUC10 lenses, -log10 f: %s" % ", ".join("%s %.3f" % (d["id"][-7:], -d["log10f"]) if d["log10f"] is not None else "%s none" % d["id"][-7:] for d in PRI["EUC10 reading"]["lenses"]))

    # ---------------------------------------------------------------- twins
    code = 0
    if MUT == "nomask":
        back = all(PRI[row]["stats"]["S_" + nm]["word"] == COMMIT[row][nm] for row in COMMIT for nm in E.FOOT)
        P("\n[twin nomask] every committed word comes back with f = 1: %s" % ("YES" if back else "NO"))
        RES["twin_ok"] = bool(back); code = 1 if back else 3
    elif MUT == "invert":
        ok = True
        for row, key in (("R1", "f25"), ("R2 W_B", "f25"), ("R3", "b_med")):
            for nm in E.FOOT:
                st = PRI[row]["stats"]["S_" + nm]
                if st.get("N", 0) == 0: ok = False; continue
                ok = ok and st[key] >= st["uncorrected_same_lenses"][key] - 1e-12
        P("\n[twin invert] with the shift reversed f25 does not fall in R1, R2 and b_med does not fall in R3: %s" % ("YES" if ok else "NO"))
        RES["twin_ok"] = bool(ok); code = 1 if ok else 3
    else:
        if not checks_ok:
            P("\nA CHECK FAILED: the lane is NOT EVALUABLE."); code = 2
        with open(os.path.join(HERE, "euc17_per_lens.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["unique_identifier", "row", "theta_E_arcsec", "theta_e_arcsec", "sersic_n", "mask_radius_arcsec", "mask_centre_offset_arcsec",
                        "f_in_mask", "log10_f", "b_S_canonical", "b_S_alt", "b_corr_S_canonical", "b_corr_S_alt"])
            for gname, tagrow in (("R1 P", "P"), ("R2 W_B", "W_B")):
                g = B[gname]; lf = logf(g["ids"], g["te"], g["n"], "primary", M)
                for j, i in enumerate(g["ids"]):
                    has = np.isfinite(lf[j])
                    w.writerow([i, tagrow, "%.4f" % g["tE"][j], "%.4f" % g["te"][j], "%.3f" % g["n"][j],
                                "%.4f" % M[i]["R"] if has else "", "%.4f" % M[i]["off"] if has else "",
                                "%.5f" % 10.0 ** lf[j] if has else "", "%.5f" % lf[j] if has else "",
                                "%.4f" % g["b"][("S", "canonical")][j], "%.4f" % g["b"][("S", "alt")][j],
                                "%.4f" % (g["b"][("S", "canonical")][j] + lf[j]) if has else "", "%.4f" % (g["b"][("S", "alt")][j] + lf[j]) if has else ""])
    P("\nchecks all pass: %s;  elapsed %.0f s;  exit %d" % (checks_ok, time.time() - t0, code))
    with open(os.path.join(HERE, TAG + "_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    with open(os.path.join(HERE, TAG + ".out"), "w") as f:
        f.write("\n".join(OUT) + "\n")
    sys.exit(code)


if __name__ == "__main__":
    main()
