#!/usr/bin/env python3
"""EUC17R: blind re-grade of EUC17 (mask-aperture stellar mass, Euclid lens rows re-read).

Criteria: ../EUC17_mask_aperture_mass_reread/FROZEN_CRITERIA.md and AMENDMENT_A1.md, as read in READING.md (this
folder).  Per lens with a mask, f = euc1.M2D_frac(mask_radius, eclipse_effective_radius, eclipse_sersic_index) and
b_corr = b + log10 f.  Rows R1 (EUC1, P), R2 (EUC4, W_B), R3 (EUC1-F as EUC16 graded it); both footings, never pooled.

Run (from the repository root):
  python3 -I closure_2026_11_13/EUC17R_blind_mask_aperture_regrade/euc17r.py
  EUC17R_MUTATE=nomask python3 -I .../euc17r.py      (twin, must exit 1)
  EUC17R_MUTATE=invert python3 -I .../euc17r.py      (twin, must exit 1)

kappa = 1/2 FITTED.  Adopts nothing; no outcome is a pass of the lensing gate.
"""
import sys
sys.dont_write_bytecode = True
import csv, json, math, os, time

import numpy as np
from scipy.special import gammainc, gammaincinv, gamma as Gfun

for _v in ("EUC1_MUTATE", "EUC4_MUTATE"):
    os.environ.pop(_v, None)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
D_EUC1 = os.path.join(REPO, "closure_2026_11_12", "EUC1_eclipse_saturation_ceiling")
D_EUC4 = os.path.join(REPO, "closure_2026_11_12", "EUC4_wide_lenses")
D_EUC10 = os.path.join(REPO, "closure_2026_11_12", "EUC10_published_source_redshifts")
D_EUC16 = os.path.join(REPO, "closure_2026_11_13", "EUC16_better_arc_finder_source_redshifts")
D_EUC17 = os.path.join(REPO, "closure_2026_11_13", "EUC17_mask_aperture_mass_reread")
D_J0332 = os.path.join(REPO, "euclid_for_j0332_fit_2026_11_13", "inputs")
D_DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
sys.path.insert(0, D_EUC1)
sys.path.insert(0, D_EUC4)
import euc1 as E          # EUC1's machinery, imported, not edited
import euc4 as W4         # EUC4's word function, imported, not edited

MUT = (os.environ.get("EUC17R_MUTATE", "") or "").strip()
if MUT not in ("", "nomask", "invert"):
    sys.exit("unknown EUC17R_MUTATE")
TAG = "euc17r" + ("_MUTATE_" + MUT if MUT else "")
LAWKEYS = ("S_canonical", "S_alt", "B_canonical", "B_alt")
FOOTS = ("canonical", "alt")
NOMASK_MAX = 0.05
R3_HOLD, R3_FAIL, R3_NMIN = 0.15, 0.25, 10
COMMITTED = {"R1": {"canonical": "NO VERDICT", "alt": "NO VERDICT"},
             "R2": {"canonical": "WIDE LENSES BREAK THE CEILING", "alt": "WIDE LENSES BREAK THE CEILING"},
             "R3": {"canonical": "NO VERDICT", "alt": "NO VERDICT"}}
BIN_NAMES = {"W_B": "W_B: theta_E >= 1.7 arcsec (primary)", "SEC": "secondary: 1.3 <= theta_E < 1.7",
             "CMP": "complement: theta_E < 1.0"}

OUT = []
def P(s=""):
    print(s); OUT.append(s)

def fl(x):
    try: return float(x)
    except Exception: return float("nan")

# ================================================================== inputs
def load_inputs():
    rows, _ = E.load(D_DATA)
    E.OUT.clear()
    KEY = {r["id"]: r for r in rows}
    ORDER = {r["id"]: i for i, r in enumerate(rows)}
    Pm, _ = E.select(rows, ("A",))
    Bm, _ = E.select(rows, ("B",))
    bins = {"W_B": [r for r in Bm if r["tE"] >= 1.7], "SEC": [r for r in Bm if 1.3 <= r["tE"] < 1.7],
            "CMP": [r for r in Bm if r["tE"] < 1.0]}
    MASK, dup, tab_n = {}, 0, 0
    with open(os.path.join(D_EUC17, "euc17_masks.csv"), newline="") as f:
        for m in csv.DictReader(f):
            tab_n += 1
            if m["unique_identifier"] in MASK: dup += 1
            ok = m["http_status"].strip() == "200" and m["has_mask"].strip() == "1"
            rad = fl(m["mask_radius_arcsec"])
            if ok and np.isfinite(rad) and rad > 0:
                c0, c1 = fl(m["mask_centre_0"]), fl(m["mask_centre_1"])
                MASK[m["unique_identifier"]] = dict(rad=rad, c0=c0, c1=c1, off=float(math.hypot(c0, c1)) if np.isfinite(c0) and np.isfinite(c1) else 0.0)
    # committed per-lens files
    c1 = {r["unique_identifier"]: r for r in csv.DictReader(open(os.path.join(D_EUC1, "euc1_per_lens.csv"), newline=""))}
    c4 = {r["unique_identifier"]: r for r in csv.DictReader(open(os.path.join(D_EUC4, "euc4_per_lens.csv"), newline=""))}
    c16 = [r for r in csv.DictReader(open(os.path.join(D_EUC16, "euc16_sources.csv"), newline=""))
           if r["in_P"].strip() == "True" and r["class_TB"].strip() == "SECURE"]
    c10 = [r for r in csv.DictReader(open(os.path.join(D_EUC10, "euc10_per_lens.csv"), newline=""))
           if r["b_S_canonical"].strip() and r["b_S_alt"].strip()]
    ref = dict(euc1=json.load(open(os.path.join(D_EUC1, "euc1_results.json"))),
               euc4=json.load(open(os.path.join(D_EUC4, "euc4_results.json"))),
               euc16=json.load(open(os.path.join(D_EUC16, "euc16_results.json"))),
               euc10=json.load(open(os.path.join(D_EUC10, "euc10_results.json"))))
    return rows, KEY, ORDER, Pm, bins, MASK, dict(table_rows=tab_n, duplicates=dup), c1, c4, c16, c10, ref

def full_b(sample):
    """A1 change 1: b at full precision with EUC1's own build / solve_b, source at z_s = 1100."""
    eng, z, RE, Re, n, lm = E.build(sample)
    Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
    return {law + "_" + nm: eng.solve_b(Mmin, a0, law) for law in ("S", "B") for nm, a0 in E.FOOT.items()}

# ================================================================== in-mask share
def f_lens(lid, KEY, MASK, cfg):
    m, r = MASK.get(lid), KEY.get(lid)
    if m is None or r is None: return float("nan")
    rad = m["rad"] + cfg.get("rad_sign", 0.0) * m["off"]
    if not rad > 0: return float("nan")
    te = r["te"] * cfg.get("re_scale", 1.0)
    n = cfg["n_fix"] if cfg.get("n_fix") else r["n"]
    return float(E.M2D_frac(rad, te, n))

# ================================================================== statistics (stream rules of READING.md section 3)
def _st(b, rng):
    return E.stats(np.asarray(b, float), rng if rng is not None else np.random.default_rng(E.SEED))

def r3_word(st):
    if st["N"] < R3_NMIN: return "NOT EVALUABLE"
    if st["b_med_hi"] <= R3_HOLD: return "LENS GATE HOLDS"
    if st["b_med_lo"] >= R3_FAIL: return "LENS GATE FAILS"
    return "NO VERDICT"

def block_R1(b, c3, c2, stream):
    """EUC1's order: primary S-can, S-alt, B-can, B-alt; then z_s = 3 and z_s ~ 2 (same four each, shared rng)."""
    rng = np.random.default_rng(E.SEED) if stream == "mirror" else None
    out = {}
    for k in LAWKEYS:
        st = _st(b[k], rng); st["word"] = E.word(st); out[k] = st
    for name, arr in (("C3", c3), ("C2", c2)):
        for k in LAWKEYS:
            if len(arr) == 0: continue
            if k == "S_alt":
                st = _st(arr, rng); st["would_be"] = E.word(st); out[name] = st
            elif stream == "mirror":
                _st(np.zeros(len(arr)), rng)          # stream advance only (EUC1's uncommitted calls)
    return out

def block_R2(bins_b, stream):
    """EUC4's order: W_B, secondary, complement; S-can, S-alt, B-can, B-alt each; shared rng."""
    rng = np.random.default_rng(E.SEED) if stream == "mirror" else None
    out = {}
    for nm in ("W_B", "SEC", "CMP"):
        out[nm] = {}
        for k in LAWKEYS:
            b = bins_b[nm][k]
            if len(b) == 0:
                out[nm][k] = dict(N=0, word="NOT EVALUABLE"); continue
            st = _st(b, rng); st["word"] = W4.word(st); out[nm][k] = st
    return out

def fresh_pair(bd):
    out = {}
    for nm in FOOTS:
        b = bd[nm]
        out[nm] = _st(b, None) if len(b) else dict(N=0)
    return out

# ================================================================== one full configuration
def run_config(D, cfg, mode, stream="mirror"):
    """mode: 'harness' (f = 1, all lenses), 'corr' (b + log f), 'invert' (b - log f). cfg: bracket options."""
    KEY, MASK = D["KEY"], D["MASK"]
    sign = -1.0 if mode == "invert" else 1.0
    res = dict(nomask={}, N_row={})

    def prep(ids, arrays, extra_keep=None):
        n_row = len(ids)
        f = np.array([f_lens(i, KEY, MASK, cfg) for i in ids], float)
        nom = ~np.isfinite(f)
        base = np.ones(n_row, bool) if extra_keep is None else extra_keep.copy()
        if cfg.get("drop_n"):
            base &= np.array([KEY[i]["n"] <= cfg["drop_n"] for i in ids], bool)
        share = float(np.sum(nom & base) / max(np.sum(base), 1))
        if mode == "harness":
            keep, ff = base, np.ones(n_row)
            share = 0.0
        elif mode == "unit":                                  # f = 1 on the lenses with a mask (same set as 'corr')
            keep, ff = base & ~nom, np.ones(n_row)
        elif cfg.get("keep_nomask"):
            keep, ff = base, np.where(nom, 1.0, f)
        else:
            keep, ff = base & ~nom, np.where(nom, 1.0, f)
        lf = np.log10(ff)
        outa = {k: (np.asarray(a, float) + sign * lf)[keep] for k, a in arrays.items()}
        return outa, share, int(np.sum(nom & base)), int(np.sum(base))

    # R1 and its conditional readings C3 / C2 (committed columns, A1 change 2)
    r1, sh, nn, nb = prep(D["P_ids"], D["bP"]); res["nomask"]["R1"], res["N_row"]["R1"] = (nn, sh), nb
    c3m, c2m = np.isfinite(D["c3"]), np.isfinite(D["c2"])
    c3, sh3, nn3, nb3 = prep(D["P_ids"], {"x": D["c3"]}, c3m); res["nomask"]["C3"], res["N_row"]["C3"] = (nn3, sh3), nb3
    c2, sh2, nn2, nb2 = prep(D["P_ids"], {"x": D["c2"]}, c2m); res["nomask"]["C2"], res["N_row"]["C2"] = (nn2, sh2), nb2
    res["R1"] = block_R1(r1, c3["x"], c2["x"], stream)
    # R2 and its bins
    bb = {}
    for nm in ("W_B", "SEC", "CMP"):
        bb[nm], shb, nnb, nbb = prep(D["bin_ids"][nm], D["bB"][nm]); res["nomask"][nm], res["N_row"][nm] = (nnb, shb), nbb
    res["R2"] = block_R2(bb, stream)
    # R3 (EUC16's certified lenses of P; committed columns; fresh rng per statistic)
    r3, sh, nn, nb = prep(D["r3_ids"], D["r3_b"]); res["nomask"]["R3"], res["N_row"]["R3"] = (nn, sh), nb
    res["R3"] = fresh_pair(r3)
    for nm in FOOTS:
        if res["R3"][nm]["N"]: res["R3"][nm]["word"] = r3_word(res["R3"][nm])
        else: res["R3"][nm]["word"] = "NOT EVALUABLE"
    # EUC10 reading (11 lenses) and its EUC1-F line (2 lenses of P)
    e10, sh, nn, nb = prep(D["e10_ids"], D["e10_b"]); res["nomask"]["E10"], res["N_row"]["E10"] = (nn, sh), nb
    res["E10"] = fresh_pair(e10)
    e10f, sh, nn, nb = prep(D["e10F_ids"], D["e10F_b"]); res["nomask"]["E10F"], res["N_row"]["E10F"] = (nn, sh), nb
    res["E10F"] = fresh_pair(e10f)
    for nm in FOOTS: res["E10F"][nm]["word"] = "NOT EVALUABLE" if res["E10F"][nm].get("N", 0) < R3_NMIN else r3_word(res["E10F"][nm])

    # words with the no-mask rule (rows and reported bins)
    def nm_ok(key): return res["nomask"][key][1] <= NOMASK_MAX
    W = {}
    for nm in FOOTS:
        W[("R1", nm)] = res["R1"]["S_" + nm]["word"] if nm_ok("R1") else "NOT EVALUABLE (no mask > 5 %)"
        W[("R2", nm)] = res["R2"]["W_B"]["S_" + nm]["word"] if nm_ok("W_B") else "NOT EVALUABLE (no mask > 5 %)"
        W[("R3", nm)] = res["R3"][nm]["word"] if nm_ok("R3") else "NOT EVALUABLE (no mask > 5 %)"
        for b_ in ("SEC", "CMP"):
            W[(b_, nm)] = res["R2"][b_]["S_" + nm]["word"] if nm_ok(b_) else "NOT EVALUABLE (no mask > 5 %)"
        W[("R1_lawB", nm)] = res["R1"]["B_" + nm]["word"] if nm_ok("R1") else "NOT EVALUABLE (no mask > 5 %)"
        W[("R2_lawB", nm)] = res["R2"]["W_B"]["B_" + nm]["word"] if nm_ok("W_B") else "NOT EVALUABLE (no mask > 5 %)"
    for c in ("C3", "C2"):
        W[(c, "alt")] = res["R1"][c]["would_be"] if (c in res["R1"] and nm_ok(c)) else "NOT EVALUABLE (no mask > 5 %)"
    res["words"] = {"%s|%s" % k: v for k, v in W.items()}
    return res

# ================================================================== check helpers
def cmp_stat(got, ref, tol_b, tol_frac, tol_bound=0.01, wkey="word", ref_word=None):
    """returns (ok, worst point diff, worst bound diff, notes)."""
    notes, okp = [], True
    if int(got["N"]) != int(ref["N"]): notes.append("N %d vs %d" % (got["N"], ref["N"])); okp = False
    dp, db = 0.0, 0.0
    for k in ("f25", "f0", "b_med"):
        if k not in ref: continue
        tol = tol_b if k == "b_med" else tol_frac
        d = abs(got[k] - ref[k]); dp = max(dp, d)
        if d > tol: okp = False; notes.append("%s %.6g vs %.6g" % (k, got[k], ref[k]))
        for s in ("_lo", "_hi"):
            d = abs(got[k + s] - ref[k + s]); db = max(db, d)
            if d > tol_bound: okp = False; notes.append("%s%s %.6g vs %.6g" % (k, s, got[k + s], ref[k + s]))
    rw = ref.get(wkey) if ref_word is None else ref_word
    if rw is not None and got.get(wkey) != rw: okp = False; notes.append("word %s vs %s" % (got.get(wkey), rw))
    return okp, dp, db, notes

def k0_compare(H, ref, Nc3, Nc2):
    """K0: harness (f = 1) against every committed statistic and word."""
    items = []
    e1, e4, e16, e10 = ref["euc1"], ref["euc4"], ref["euc16"], ref["euc10"]
    for k in LAWKEYS:
        items.append(("R1 %s" % k,) + cmp_stat(H["R1"][k], e1["primary"][k], 1e-9, 1e-9))
    for c, rk in (("C3", "R3_S_alt"), ("C2", "R2_S_alt")):
        refst = e1["conditional"][rk]
        items.append(("%s (EUC1 %s)" % (c, rk),) + cmp_stat(H["R1"][c], refst, 1e-4, 1.0 / refst["N"], wkey="would_be"))
    for nm in ("W_B", "SEC", "CMP"):
        for k in LAWKEYS:
            items.append(("R2 %s %s" % (nm, k),) + cmp_stat(H["R2"][nm][k], e4["partA"][BIN_NAMES[nm]][k], 1e-9, 1e-9))
    for nm in FOOTS:
        refst = e16["reading"]["P"]["S_" + nm]["true"]
        items.append(("R3 %s" % nm,) + cmp_stat(H["R3"][nm], refst, 1e-4, 1.0 / refst["N"], ref_word=e16["words"][nm]))
        refst = e10["readings"]["all matched with valid inputs, law S"][nm]
        items.append(("EUC10 reading %s" % nm,) + cmp_stat(H["E10"][nm], refst, 1e-4, 1.0 / refst["N"], wkey="__none__"))
        refst = e10["EUC1F"]["noprov"][nm]
        items.append(("EUC10 EUC1-F line %s" % nm,) + cmp_stat(H["E10F"][nm], refst, 1e-4, 1.0 / refst["N"]))
    return items

# ================================================================== K4 (FOR J0332, own code)
def k4_check():
    from astropy.io import fits
    info = json.load(open(os.path.join(D_J0332, "dataset", "info.json")))
    rad = float(info["mask_radius"]); my, mx = (float(v) for v in info["mask_centre"]); ps = float(info["pixel_scale"])
    tile = "Tile102034383RA0532498193624DECNEG0359643115588"
    with fits.open(os.path.join(D_J0332, "dataset", tile + ".fits")) as h:
        hv = h["VIS_BGSUB"].header; zp = float(hv["MAGZERO"]); bunit = str(hv.get("BUNIT", "")).strip()
    with fits.open(os.path.join(D_J0332, "results", "pre_psf.fits")) as h:
        img = np.array(h["VIS_GALAXY_0"].data, dtype=float)
    rec = json.load(open(os.path.join(D_J0332, "portal_lens_record.json")))
    ly, lx = float(rec["master"]["lens_light_centre_0"]), float(rec["master"]["lens_light_centre_1"])
    vis = [m for m in csv.DictReader(open(os.path.join(D_J0332, "results", "magnitudes.csv"), newline="")) if m["waveband"].strip() == "vis"][0]
    Fcat, Fmed = float(vis["lens_flux_max_lh"]), float(vis["lens_flux"])
    ny, nx = img.shape
    jj, ii = np.meshgrid(np.arange(nx), np.arange(ny))
    X = (jj - (nx - 1) / 2.0) * ps
    Yraw = (ii - (ny - 1) / 2.0) * ps
    ipk, jpk = np.unravel_index(int(np.argmax(img)), img.shape)
    sgn = 1.0 if np.sign(Yraw[ipk, jpk]) == np.sign(ly) else -1.0
    conv = 10.0 ** (-0.4 * (zp - 23.9))                     # ADU/s -> microJy (AB)
    def inside(s): return (X - mx) ** 2 + (s * Yraw - my) ** 2 <= rad * rad
    ins = inside(sgn); S_map = float(img[ins].sum()); S_other = float(img[inside(-sgn)].sum())
    F_map = S_map * conv
    # analytic Sersic (released VIS Sersic fit, coolest_sersic.json, galaxy_0)
    cs = json.load(open(os.path.join(D_J0332, "results", "coolest_sersic.json")))
    ent = [e for e in cs["lensing_entities"] if e.get("name") == "galaxy_0"][0]
    lp = ent["light_model"][0]["parameters"]
    pv = {k: float(lp[k]["point_estimate"]["value"]) for k in ("I_eff", "theta_eff", "n", "q", "phi", "center_x", "center_y")}
    n, q, th, I0 = pv["n"], pv["q"], pv["theta_eff"], pv["I_eff"]
    bn = float(E.b_ser(n))
    def model(rconv, phi_deg, s):
        yN = -(s * Yraw)                                     # pipeline +y south -> COOLEST +y north
        dx, dy = X - pv["center_x"], yN - pv["center_y"]
        a = math.radians(phi_deg)
        u = dx * math.cos(a) + dy * math.sin(a); v = -dx * math.sin(a) + dy * math.cos(a)
        r = np.sqrt(q * u * u + v * v / q) if rconv == "intermediate" else np.sqrt(u * u + v * v / (q * q))
        return I0 * np.exp(-bn * ((r / th) ** (1.0 / n) - 1.0))
    combos = []
    for rconv in ("intermediate", "major"):
        for unit in ("per_pixel", "per_arcsec2"):
            pix = model(rconv, pv["phi"], sgn) * (1.0 if unit == "per_pixel" else ps * ps)
            pix90 = model(rconv, pv["phi"] + 90.0, sgn) * (1.0 if unit == "per_pixel" else ps * ps)
            S_mod = float(pix[ins].sum()); S_mod90 = float(pix90[ins].sum())
            T_area = 2.0 * math.pi * I0 * th * th * n * math.exp(bn) * bn ** (-2.0 * n) * Gfun(2.0 * n) * (1.0 if rconv == "intermediate" else q)
            T_img = T_area / (ps * ps) if unit == "per_pixel" else T_area
            combos.append(dict(rconv=rconv, unit=unit, S_model_inmask=S_mod, S_model_inmask_phi90=S_mod90,
                               match=S_mod / S_map, T_img=T_img, T_uJy=T_img * conv, model_inmask_share=S_mod / T_img))
    best = min(combos, key=lambda c: abs(math.log(c["match"])))
    a_dev = F_map / Fcat - 1.0
    T = best["T_uJy"]
    ok_a = abs(a_dev) <= 0.03
    ok_b = T > 1.10 * Fcat
    contradicted = abs(T / Fcat - 1.0) < abs(a_dev)
    return dict(mask_radius=rad, mask_centre_yx=[my, mx], pixel_scale=ps, zero_point=zp, bunit=bunit,
                peak_pixel=[int(ipk), int(jpk)], row_sign=sgn, peak_x_arcsec=float(X[ipk, jpk]), lens_light_centre_yx=[ly, lx],
                n_pix_inside=int(ins.sum()), S_map_ADU_s=S_map, S_map_other_orientation=S_other, F_map_uJy=F_map,
                F_map_other_orientation_uJy=S_other * conv, F_cat_max_lh_uJy=Fcat, F_cat_median_uJy=Fmed,
                test_a_dev=a_dev, test_a_dev_median=F_map / Fmed - 1.0, sersic=pv, b_n=bn, combos=combos, chosen=best,
                T_over_Fcat=T / Fcat, ok_a=bool(ok_a), ok_b=bool(ok_b), contradicted=bool(contradicted),
                ok=bool(ok_a and ok_b and not contradicted))

# ================================================================== main
def main():
    t0 = time.time()
    P("EUC17R (BLIND RE-GRADE OF EUC17: MASK-APERTURE STELLAR MASS)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("criteria: EUC17 FROZEN_CRITERIA.md + AMENDMENT_A1.md, read in READING.md.  kappa = 1/2 FITTED.")
    P("footings (m/s^2): canonical %.4e, alt %.4e; never pooled" % (E.FOOT["canonical"], E.FOOT["alt"]))
    rows, KEY, ORDER, Pm, bins, MASK, tabinfo, c1, c4, c16, c10, ref = load_inputs()
    P("\n[data]")
    P("  catalogue rows (key joined to object) %d; P = %d; grade-B bins: W_B %d, secondary %d, complement %d"
      % (len(rows), len(Pm), len(bins["W_B"]), len(bins["SEC"]), len(bins["CMP"])))
    P("  mask table: %d lines, %d duplicate identifiers, %d lenses with a usable mask" % (tabinfo["table_rows"], tabinfo["duplicates"], len(MASK)))

    # ------------------------------------------------ full-precision b (A1 change 1)
    bP = full_b(Pm)
    bB = {nm: full_b(bins[nm]) for nm in bins}
    P_ids = [r["id"] for r in Pm]
    c3 = np.array([fl(c1[i]["b_S_alt_R3"]) if i in c1 else float("nan") for i in P_ids])
    c2 = np.array([fl(c1[i]["b_S_alt_R2"]) if i in c1 else float("nan") for i in P_ids])
    r3_rows = sorted(c16, key=lambda r: ORDER.get(r["unique_identifier"], 10 ** 9))
    r3_ids = [r["unique_identifier"] for r in r3_rows]
    r3_b = {nm: np.array([fl(r["b_S_" + nm]) for r in r3_rows]) for nm in FOOTS}
    e10_rows = sorted(c10, key=lambda r: ORDER.get(r["eclipse_id"], 10 ** 9))
    e10_ids = [r["eclipse_id"] for r in e10_rows]
    e10_b = {nm: np.array([fl(r["b_S_" + nm]) for r in e10_rows]) for nm in FOOTS}
    e10F_ids = list(ref["euc10"]["EUC1F"]["noprov"]["canonical"]["ids"])
    e10F_rows = {r["eclipse_id"]: r for r in e10_rows}
    e10F_b = {nm: np.array([fl(e10F_rows[i]["b_S_" + nm]) for i in e10F_ids]) for nm in FOOTS}
    D = dict(KEY=KEY, MASK=MASK, P_ids=P_ids, bP=bP, c3=c3, c2=c2, bin_ids={nm: [r["id"] for r in bins[nm]] for nm in bins},
             bB=bB, r3_ids=r3_ids, r3_b=r3_b, e10_ids=e10_ids, e10_b=e10_b, e10F_ids=e10F_ids, e10F_b=e10F_b)
    RES = dict(lane="EUC17R", mutate=MUT, footings=E.FOOT, n=dict(P=len(Pm), **{k: len(v) for k, v in bins.items()},
               R3=len(r3_ids), E10=len(e10_ids), E10F=len(e10F_ids), C3=int(np.isfinite(c3).sum()), C2=int(np.isfinite(c2).sum())))
    P("  R3 lenses (in_P, class_TB SECURE): %d; EUC10 reading lenses: %d; its EUC1-F line: %d (%s)"
      % (len(r3_ids), len(e10_ids), len(e10F_ids), ", ".join(e10F_ids)))
    P("  C3 (z_s = 3) lenses with a committed value: %d; C2 (z_s ~ 2): %d" % (RES["n"]["C3"], RES["n"]["C2"]))

    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok))
        P("  %s %-4s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))

    # ------------------------------------------------ twins
    if MUT:
        P("\n[twin %s]" % MUT)
        if MUT == "nomask":
            H = run_config(D, {}, "harness")
            back, diffs = True, []
            refw = dict(H["words"])
            want = {("R1", nm): COMMITTED["R1"][nm] for nm in FOOTS}
            want.update({("R2", nm): COMMITTED["R2"][nm] for nm in FOOTS}); want.update({("R3", nm): COMMITTED["R3"][nm] for nm in FOOTS})
            for nm in FOOTS:
                want[("R1_lawB", nm)] = ref["euc1"]["primary"]["B_" + nm]["word"]
                want[("R2_lawB", nm)] = ref["euc4"]["partA"][BIN_NAMES["W_B"]]["B_" + nm]["word"]
                for b_ in ("SEC", "CMP"): want[(b_, nm)] = ref["euc4"]["partA"][BIN_NAMES[b_]]["S_" + nm]["word"]
            want[("C3", "alt")] = ref["euc1"]["conditional"]["R3_S_alt"]["would_be"]
            want[("C2", "alt")] = ref["euc1"]["conditional"]["R2_S_alt"]["would_be"]
            for k, w in want.items():
                g = refw["%s|%s" % k]
                P("  %-12s %-9s committed %-30s f = 1 gives %-30s %s" % (k[0], k[1], w, g, "same" if g == w else "DIFFERENT"))
                if g != w: back = False; diffs.append(k)
            P("  every committed word comes back with f = 1: %s -> exit %d" % ("YES" if back else "NO", 1 if back else 2))
            RES["twin_ok"] = back; RES["words"] = refw
            code = 1 if back else 2
        else:
            C = run_config(D, {}, "invert"); U = run_config(D, {}, "unit")
            ok = True
            for nm in FOOTS:
                for row, got, comm, u in (("R1 f25", C["R1"]["S_" + nm]["f25"], ref["euc1"]["primary"]["S_" + nm]["f25"], U["R1"]["S_" + nm]["f25"]),
                                          ("R2 f25", C["R2"]["W_B"]["S_" + nm]["f25"], ref["euc4"]["partA"][BIN_NAMES["W_B"]]["S_" + nm]["f25"], U["R2"]["W_B"]["S_" + nm]["f25"]),
                                          ("R3 b_med", C["R3"][nm]["b_med"], ref["euc16"]["reading"]["P"]["S_" + nm]["true"]["b_med"], U["R3"][nm]["b_med"])):
                    fell = got < comm
                    ok &= not fell
                    P("  %-9s %-9s inverted %+.4f  committed %+.4f  -> %-12s (f = 1 on the same lenses with a mask: %+.4f, %s)"
                      % (row, nm, got, comm, "FELL" if fell else "did not fall", u, "fell" if got < u else "did not fall"))
            P("  f25 (R1, R2) and b_med (R3) do not fall on either footing: %s -> exit %d" % ("YES" if ok else "NO", 1 if ok else 2))
            RES["twin_ok"] = bool(ok); RES["words"] = C["words"]
            code = 1 if ok else 2
        json.dump(RES, open(os.path.join(HERE, TAG + "_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(code)

    # ------------------------------------------------ checks
    P("\n[checks]")
    H = run_config(D, {}, "harness", "mirror")
    items = k0_compare(H, ref, RES["n"]["C3"], RES["n"]["C2"])
    k0ok = all(it[1] for it in items)
    for it in items:
        P("       K0 %-30s %s  point diff max %.2e, bound diff max %.2e%s" % (it[0], "ok  " if it[1] else "FAIL", it[2], it[3], ("  [" + "; ".join(it[4]) + "]") if it[4] else ""))
    ck("K0", "harness f = 1, stream as the source lanes called it: every committed statistic and word", "%d of %d items within tolerance" % (sum(it[1] for it in items), len(items)), k0ok)
    Hf = run_config(D, {}, "harness", "fresh")
    itf = k0_compare(Hf, ref, RES["n"]["C3"], RES["n"]["C2"])
    k0f = all(it[1] for it in itf)
    for it in itf:
        if not it[1]: P("       K0-fresh %-24s FAIL  point %.2e, bound %.2e  [%s]" % (it[0], it[2], it[3], "; ".join(it[4])))
    P("  info K0-fresh (a new generator for every statistic, same lens order): %d of %d items within tolerance -> %s"
      % (sum(it[1] for it in itf), len(itf), "would pass" if k0f else "WOULD FAIL"))
    RES["K0_items"] = [dict(name=it[0], ok=bool(it[1]), dpoint=it[2], dbound=it[3], notes=it[4]) for it in items]
    RES["K0_fresh_items"] = [dict(name=it[0], ok=bool(it[1]), dpoint=it[2], dbound=it[3], notes=it[4]) for it in itf]
    RES["K0_fresh_ok"] = bool(k0f)

    # K0b
    worst, nbad, ncmp = 0.0, 0, 0
    for i, lid in enumerate(P_ids):
        for k in LAWKEYS:
            d = abs(bP[k][i] - fl(c1[lid]["b_" + k])); worst = max(worst, d); ncmp += 1; nbad += d > 6e-5
    worst4, nbad4, ncmp4 = 0.0, 0, 0
    WB_ids = D["bin_ids"]["W_B"]
    for i, lid in enumerate(WB_ids):
        for nm in FOOTS:
            if lid not in c4: nbad4 += 1; continue
            d = abs(bB["W_B"]["S_" + nm][i] - fl(c4[lid]["b_inf_S_" + nm])); worst4 = max(worst4, d); ncmp4 += 1; nbad4 += d > 6e-5
    nB4 = sum(1 for r in c4.values() if r["grade"] == "B")
    ck("K0b", "recomputed b vs committed 4-decimal values to 6e-5 (R1: S,B x 2 footings; R2: law S x 2)",
       "R1 max %.2e over %d (%d beyond); R2 max %.2e over %d (%d beyond); committed grade-B rows %d, W_B %d"
       % (worst, ncmp, nbad, worst4, ncmp4, nbad4, nB4, len(WB_ids)), nbad == 0 and nbad4 == 0 and nB4 == len(WB_ids))

    # K1
    e1 = max(abs(float(E.M2D_frac(1.0, 1.0, nn)) - 0.5) for nn in (1.0, 4.0, 8.0))
    b1 = float(E.b_ser(1.0)); b1x = float(gammaincinv(2.0, 0.5))
    e2 = max(abs(float(E.M2D_frac(x, 1.0, 1.0)) - (1.0 - (1.0 + b1 * x) * math.exp(-b1 * x))) for x in (0.5, 2.0, 5.0))
    e2x = max(abs(float(E.M2D_frac(x, 1.0, 1.0)) - (1.0 - (1.0 + b1x * x) * math.exp(-b1x * x))) for x in (0.5, 2.0, 5.0))
    ck("K1", "M2D_frac(Re,Re,n)=0.5 to 1e-6 (n=1,4,8); n=1 form with the function's b1 to 1e-8",
       "%.2e ; %.2e   (info: with the exact b1 = %.8f instead of %.8f: %.2e)" % (e1, e2, b1x, b1, e2x), e1 <= 1e-6 and e2 <= 1e-8)

    # K2
    Pmask = [(i, r) for i, r in enumerate(Pm) if r["id"] in MASK]
    step = max(len(Pmask) // 20, 1); pick = Pmask[::step][:20]
    sub = [r for _, r in pick]; idx = np.array([i for i, _ in pick])
    fsub = np.array([f_lens(r["id"], KEY, MASK, {}) for r in sub])
    eng, z, RE, _, _, _ = E.build(sub, lm=E.arr(sub, "lm") - np.log10(fsub))
    Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
    dk2 = 0.0
    for law in ("S", "B"):
        for nm, a0 in E.FOOT.items():
            dk2 = max(dk2, float(np.max(np.abs(eng.solve_b(Mmin, a0, law) - (bP[law + "_" + nm][idx] + np.log10(fsub))))))
    ck("K2", "EUC1's solver with M*/f returns b + log10 f to 1e-6 on %d lenses of P (every %d-th with a mask)" % (len(sub), step),
       "max %.2e" % dk2, dk2 <= 1e-6 and len(sub) == 20)

    # K3
    union = {}
    for lab, ids in (("R1", P_ids), ("W_B", D["bin_ids"]["W_B"]), ("SEC", D["bin_ids"]["SEC"]), ("CMP", D["bin_ids"]["CMP"]),
                     ("R3", r3_ids), ("E10", e10_ids)):
        for i in ids: union.setdefault(i, []).append(lab)
    fall = {i: f_lens(i, KEY, MASK, {}) for i in union}
    withm = [i for i in union if i in MASK]
    bad = [i for i in withm if not (MASK[i]["rad"] > 0 and 0.0 < fall[i] <= 1.0)]
    small = {lab: sum(1 for i in withm if lab in union[i] and MASK[i]["rad"] < KEY[i]["tE"]) for lab in ("R1", "W_B", "SEC", "CMP", "R3", "E10")}
    small_all = sum(1 for i in withm if MASK[i]["rad"] < KEY[i]["tE"])
    ck("K3", "every lens with a mask: radius > 0 and f in (0, 1]", "%d lenses with a mask, %d bad; mask radius < theta_E: %d (%s)"
       % (len(withm), len(bad), small_all, ", ".join("%s %d" % kv for kv in small.items())), len(bad) == 0)

    # K4
    try:
        K4 = k4_check()
        ch = K4["chosen"]
        P("       K4 map pre_psf VIS_GALAXY_0, %s, ZP %.2f AB; mask r = %.3f\" centre (y, x) = (%+.2f, %+.2f)\"; %d pixels inside"
          % (K4["bunit"], K4["zero_point"], K4["mask_radius"], K4["mask_centre_yx"][0], K4["mask_centre_yx"][1], K4["n_pix_inside"]))
        P("       K4 orientation: brightest pixel %s, row sign %+d (lens light centre y = %+.3f, x = %+.3f; peak x = %+.2f)"
          % (K4["peak_pixel"], K4["row_sign"], K4["lens_light_centre_yx"][0], K4["lens_light_centre_yx"][1], K4["peak_x_arcsec"]))
        P("       K4 (a) in-mask map sum %.4f uJy (other orientation %.4f) vs catalogue lens_flux_max_lh %.4f uJy: %+.2f %% (vs median lens_flux %.4f: %+.2f %%)"
          % (K4["F_map_uJy"], K4["F_map_other_orientation_uJy"], K4["F_cat_max_lh_uJy"], 100 * K4["test_a_dev"], K4["F_cat_median_uJy"], 100 * K4["test_a_dev_median"]))
        for c in K4["combos"]:
            P("       K4 Sersic convention %-12s %-11s in-mask model / map %.4f (phi+90: %.4f); infinite total %.4f uJy; in-mask share of model %.4f%s"
              % (c["rconv"], c["unit"], c["match"], c["S_model_inmask_phi90"] / K4["S_map_ADU_s"], c["T_uJy"], c["model_inmask_share"], "   <- chosen" if c is ch else ""))
        P("       K4 (b) infinite Sersic total / catalogue flux = %.4f (must exceed 1.10); premise contradicted: %s"
          % (K4["T_over_Fcat"], "YES" if K4["contradicted"] else "no"))
        ck("K4", "FOR J0332: in-mask map sum = catalogue VIS flux to 3 %; infinite Sersic total > 1.10 x catalogue flux",
           "(a) %+.2f %% %s; (b) x %.3f %s" % (100 * K4["test_a_dev"], "ok" if K4["ok_a"] else "FAIL", K4["T_over_Fcat"], "ok" if K4["ok_b"] else "FAIL"), K4["ok"])
    except Exception as ex:                                   # a check that cannot run is a failed check
        K4 = dict(error=repr(ex)); ck("K4", "FOR J0332 premise spot-check", "could not run: %r" % ex, False)
    RES["K4"] = K4

    # K5
    k5 = {i: f_lens(i, KEY, MASK, {}) for i in ("EUCL-DR1-L014994", "EUCL-DR1-L015780")}
    P("  info K5   f (circular, catalogue R_e and n, centred): L014994 (FOR J0332) %.4f vs 0.804; L015780 %.4f vs 0.587"
      % (k5["EUCL-DR1-L014994"], k5["EUCL-DR1-L015780"]))
    RES["K5"] = k5
    allok = all(v["ok"] for v in CK.values())
    RES["checks"] = CK; RES["checks_all_pass"] = bool(allok)

    # ------------------------------------------------ primary corrected run
    P("\n[masks per row: no-mask count / row lenses (share); rule: > 5 % -> NOT EVALUABLE]")
    C = run_config(D, {}, "corr")
    for key in ("R1", "C3", "C2", "W_B", "SEC", "CMP", "R3", "E10", "E10F"):
        nn, sh = C["nomask"][key]
        P("  %-5s %4d / %5d  (%.2f %%)%s" % (key, nn, C["N_row"][key], 100 * sh, "   -> NOT EVALUABLE" if sh > NOMASK_MAX else ""))
    RES["nomask"] = {k: dict(count=v[0], share=v[1], N_row=C["N_row"][k]) for k, v in C["nomask"].items()}

    def fmt(st): return E.fmt(st) if st.get("N", 0) else "N = 0"
    P("\n[primary: corrected boost b + log10 f, lenses with a mask%s]" % ("" if allok else "; a check FAILED, so every word below is WOULD-BE"))
    for nm in FOOTS:
        P("  R1 law S %-9s %s -> %s" % (nm, fmt(C["R1"]["S_" + nm]), C["words"]["R1|" + nm]))
    for nm in FOOTS:
        P("  R2 law S %-9s %s -> %s" % (nm, fmt(C["R2"]["W_B"]["S_" + nm]), C["words"]["R2|" + nm]))
    for nm in FOOTS:
        st = C["R3"][nm]
        P("  R3 law S %-9s N=%3d  b_med = %+.4f [%+.4f, %+.4f]  f25 = %.3f -> %s" % (nm, st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], st["f25"], C["words"]["R3|" + nm]))
    P("\n[reported beside the rows, no word]")
    for nm in FOOTS:
        P("  R1 law B %-9s %s   (EUC1 word rule: %s)" % (nm, fmt(C["R1"]["B_" + nm]), C["words"]["R1_lawB|" + nm]))
    for nm in FOOTS:
        P("  R2 law B %-9s %s   (EUC4 word rule: %s)" % (nm, fmt(C["R2"]["W_B"]["B_" + nm]), C["words"]["R2_lawB|" + nm]))
    for b_ in ("SEC", "CMP"):
        for k in LAWKEYS:
            st = C["R2"][b_][k]
            P("  %-10s law %s %-9s %s   secondary word: %s" % (b_, k[0], k[2:], fmt(st), C["words"]["%s|%s" % (b_, k[2:])] if k[0] == "S" else st.get("word", "")))
    for c in ("C3", "C2"):
        if c in C["R1"]:
            P("  %s (EUC1 conditional, z_s %s) law S alt %s   would-be: %s" % (c, "= 3" if c == "C3" else "~ 2", fmt(C["R1"][c]), C["words"][c + "|alt"]))
    for nm in FOOTS:
        st = C["E10"][nm]
        P("  EUC10 reading %-9s N=%3d  b_med = %+.4f [%+.4f, %+.4f]  f25 = %.3f [%.3f, %.3f]" % (nm, st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], st["f25"], st["f25_lo"], st["f25_hi"]))
    for nm in FOOTS:
        st = C["E10F"][nm]
        P("  EUC10 EUC1-F line %-9s N=%d  b_med = %+.4f [%+.4f, %+.4f] -> %s" % (nm, st["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"], st["word"]))

    # ------------------------------------------------ brackets
    BR = [("F1a R_e x 0.80", {"re_scale": 0.80}), ("F1b R_e x 1.25", {"re_scale": 1.25}), ("F2 n = 4", {"n_fix": 4.0}),
          ("F3a r + |c|", {"rad_sign": 1.0}), ("F3b r - |c|", {"rad_sign": -1.0}), ("F4 no-mask kept, f = 1", {"keep_nomask": True}),
          ("F5 n > 9.5 dropped", {"drop_n": 9.5})]
    P("\n[brackets: corrected word per row and footing (law S); they set FRAGILE / ROBUST only]")
    P("  %-24s %-34s %-34s %-34s" % ("bracket", "R1 can / alt", "R2 can / alt", "R3 can / alt"))
    BRES = {}
    for name, cfg in BR:
        Bc = run_config(D, cfg, "corr")
        BRES[name] = dict(words=Bc["words"], stats={
            "R1": {nm: {k: Bc["R1"]["S_" + nm][k] for k in ("N", "f25", "f25_lo", "f25_hi", "b_med")} for nm in FOOTS},
            "R2": {nm: {k: Bc["R2"]["W_B"]["S_" + nm].get(k) for k in ("N", "f25", "f25_lo", "f25_hi", "b_med")} for nm in FOOTS},
            "R3": {nm: {k: Bc["R3"][nm].get(k) for k in ("N", "b_med", "b_med_lo", "b_med_hi")} for nm in FOOTS}})
        P("  %-24s %-34s %-34s %-34s" % (name, *["%s / %s" % (Bc["words"][r + "|canonical"][:16], Bc["words"][r + "|alt"][:16]) for r in ("R1", "R2", "R3")]))
        for r in ("R1", "R2"):
            s = BRES[name]["stats"][r]
            P("      %s f25 %.3f [%.3f, %.3f] / %.3f [%.3f, %.3f]  (N %d)" % (r, s["canonical"]["f25"], s["canonical"]["f25_lo"], s["canonical"]["f25_hi"], s["alt"]["f25"], s["alt"]["f25_lo"], s["alt"]["f25_hi"], s["alt"]["N"]))
        s = BRES[name]["stats"]["R3"]
        P("      R3 b_med %+.3f [%+.3f, %+.3f] / %+.3f [%+.3f, %+.3f]  (N %d)" % (s["canonical"]["b_med"], s["canonical"]["b_med_lo"], s["canonical"]["b_med_hi"], s["alt"]["b_med"], s["alt"]["b_med_lo"], s["alt"]["b_med_hi"], s["alt"]["N"]))
    RES["brackets"] = BRES

    # ------------------------------------------------ labels
    P("\n[labels per row and footing%s]" % ("" if allok else ": LANE NOT EVALUABLE (a check failed); labels below are WOULD-BE"))
    LAB = {}
    for r in ("R1", "R2", "R3"):
        for nm in FOOTS:
            w = C["words"]["%s|%s" % (r, nm)]
            ch = "UNCHANGED" if w == COMMITTED[r][nm] else "CHANGED"
            diff = [b for b in BRES if BRES[b]["words"]["%s|%s" % (r, nm)] != w]
            fr = "FRAGILE" if diff else "ROBUST"
            LAB["%s|%s" % (r, nm)] = dict(word=w if allok else "NOT EVALUABLE", would_be=w, committed=COMMITTED[r][nm], change=ch, fragility=fr, brackets_differing=diff)
            P("  %s %-9s %-34s %-9s %-7s (committed %s)%s" % (r, nm, (w if allok else "NOT EVALUABLE [would-be: %s]" % w), ch, fr, COMMITTED[r][nm],
                                                          ("  differing: " + ", ".join(diff)) if diff else ""))
    RES["labels"] = LAB
    RES["primary"] = dict(words=C["words"], R1=C["R1"], R2=C["R2"], R3=C["R3"], E10=C["E10"], E10F=C["E10F"])

    # ------------------------------------------------ S1 plausibility
    P("\n[S1 plausibility: -log10 f on P (lenses with a mask), by theta_E class]")
    tE = np.array([KEY[i]["tE"] for i in P_ids]); fP = np.array([fall[i] for i in P_ids]); has = np.isfinite(fP)
    S1 = {}
    for lab, m in (("< 1.0", tE < 1.0), ("1.0-1.3", (tE >= 1.0) & (tE < 1.3)), ("1.3-1.7", (tE >= 1.3) & (tE < 1.7)), (">= 1.7", tE >= 1.7), ("all P", np.ones(len(tE), bool))):
        x = -np.log10(fP[m & has])
        q16, q50, q84 = (float(v) for v in np.percentile(x, [16, 50, 84]))
        S1[lab] = dict(N=int(x.size), median=q50, p16=q16, p84=q84)
        P("  theta_E %-8s N=%5d  median %.4f dex  [16-84 %%: %.4f, %.4f]" % (lab, x.size, q50, q16, q84))
    P("  on the record: catalogue masses 0.23 dex above the Euclid pipeline's (EUC1); uncorrected ECLIPSE scale agrees with")
    P("  Auger 2009 and DESI CIGALE to ~0.05 dex (EUC12).  Median correction on P %.4f dex: %s" % (S1["all P"]["median"],
      "ABOVE 0.05 dex -> the corrected scale would sit above the total-magnitude scales beyond their present agreement; a reason to doubt the extrapolated wings"
      if S1["all P"]["median"] > 0.05 else "within 0.05 dex"))
    RES["S1"] = S1

    # ------------------------------------------------ per-lens f table
    with open(os.path.join(HERE, "euc17r_f.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["unique_identifier", "rows", "mask_radius_arcsec", "mask_offset_arcsec", "theta_E_arcsec", "theta_e_arcsec", "sersic_n", "f_in_mask"])
        for i in sorted(union, key=lambda x: ORDER.get(x, 10 ** 9)):
            m = MASK.get(i); r = KEY[i]
            w.writerow([i, "+".join(union[i]), "%.4f" % m["rad"] if m else "", "%.4f" % m["off"] if m else "", "%.4f" % r["tE"], "%.4f" % r["te"], "%.3f" % r["n"],
                        "%.6f" % fall[i] if np.isfinite(fall[i]) else ""])

    P("\n[summary]")
    P("  checks K0 (mirrored stream), K0b, K1, K2, K3, K4: %s" % ("all pass" if allok else "FAILED: " + ", ".join(k for k, v in CK.items() if not v["ok"]) + " -> LANE NOT EVALUABLE"))
    P("  K0 under a fresh generator per statistic (info): %s" % ("would pass" if k0f else "would FAIL"))
    for r in ("R1", "R2", "R3"):
        P("  %s: %s / %s" % (r, *["%s (%s, %s)" % (LAB["%s|%s" % (r, nm)]["word"] if allok else "NOT EVALUABLE [would-be %s]" % LAB["%s|%s" % (r, nm)]["would_be"],
                                                 LAB["%s|%s" % (r, nm)]["change"], LAB["%s|%s" % (r, nm)]["fragility"]) for nm in FOOTS]))
    P("  kappa = 1/2 FITTED. No row is a pass of the lensing gate; a CHANGED row is a hit awaiting a blind re-grade.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, TAG + "_results.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
