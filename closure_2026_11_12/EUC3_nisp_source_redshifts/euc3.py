#!/usr/bin/env python3
"""EUC3 (NISP SOURCE REDSHIFTS).  Frozen criteria: FROZEN_CRITERIA.md (commit bf72d787a8).

Secure lensed-source redshifts for Euclid's strong lenses from Euclid's own DR1 red-grism redshift and line tables
(fetched by euc3_fetch.py), a purity null on the grade-X systems, a truth gate on EUC2's three DESI-confirmed pairs,
and EUC1's b at the true source redshift.  EUC1-F (EUC1 RESULT section 8) is applied exactly as frozen if N(P) >= 10.

Run:
  python3 -I euc3.py --data-dir <dir with the two ECLIPSE csv files and nisp_tables/>
  python3 -I euc3.py --data-dir <dir> --interim      (part "first" of the fetch only: S, truth lenses, X; outputs
                                                      under euc3_interim*, labelled; never the lane's result)
  EUC3_MUTATE=newton  python3 -I euc3.py --data-dir <dir>     (must exit 1)
  EUC3_MUTATE=noguard python3 -I euc3.py --data-dir <dir>     (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  One-sided: no outcome favours the framework.
"""
import argparse, csv, json, math, os, sys, time
import numpy as np
from scipy.stats import beta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

MUT = (os.environ.get("EUC3_MUTATE", "") or "").strip()
if MUT == "newton":
    E.FOOT = {k: 1.0e-30 for k in E.FOOT}
GUARD = MUT != "noguard"

# ------------------------------------------------------------------ frozen numbers (criteria sections 2-5)
HA, OIII = 6564.61, 5008.24
BANDS = (("[S III] 9533", 9533.2, 9533.2), ("He I 10833 / Pa gamma", 10833.3, 10941.1), ("Pa beta", 12821.6, 12821.6))
NPIX_MIN, NDITH_ABOVE = 300, 3
ZPROB_MIN, ZREL_ABOVE = 0.99, 0.05
ZMIN, ZMAX = 0.84, 1.88
QUAL_OK = (212, 252)
FLUX_MIN, FWHM_MAX = 2.0e-16, 180.0
TIERS = (("T5", 5.0), ("T8", 8.0))
DZ_ABOVE, PAD, AGREE = 0.15, 0.01, 0.02
R_EXTRA, R_CAP, LENS_SEP = 0.7, 3.0, 0.6
NULL_FRAC, COVER_MIN = 0.20, 0.30
F_HOLDS, F_FAILS, F_NMIN = 0.15, 0.25, 10
TRUTH = (("EUCL-DR1-L015763", 1.3657), ("EUCL-DR1-L012826", 1.1374), ("EUCL-DR1-L014688", 0.9926))
SECOND = ("OIII5008", "Hbeta", "SII6718", "SIII9530", "SIII9068", "OII3727")
ANCHOR = ("EUCL-DR1-L015763", 1.3657, (0.231, 0.215))

OUT = []
def P(s=""):
    print(s); OUT.append(s)
E.P = P

def fl(v):
    try: return float(v)
    except Exception: return float("nan")

def read_tab(tdir, key, parts):
    rows = []
    for fn in sorted(os.listdir(tdir)):
        if fn.endswith(".csv") and any(fn.startswith("%s_%s_" % (key, p)) for p in parts):
            with open(os.path.join(tdir, fn), newline="") as f:
                rows.extend(csv.DictReader(f))
    return rows

def by_obj(rows):
    d = {}
    for r in rows: d.setdefault(int(r["object_id"]), []).append(r)
    return d

def obskey(r): return (r.get("patch_id_list", ""), r.get("calblock_id_list", ""))

ANOM = dict(multi_spectra_objects=0, unpaired_quality=0, ambiguous_pair=0)
def pair(c, pool):
    """the row of another table that belongs to the same spectrum as candidate row c"""
    if not pool: return None
    if len(pool) == 1: return pool[0]
    m = [r for r in pool if obskey(r) == obskey(c)]
    if len(m) > 1: ANOM["ambiguous_pair"] += 1
    return m[0] if m else None

def judge(c, q, ha, zlo, zup, snr_min, guard=True):
    """the frozen rule on one spectrum's rank-0 galaxy solution -> (class, first cut failed)"""
    if q is None: return "fail", "no quality row"
    if not (fl(q["spe_npix"]) >= NPIX_MIN and fl(q["spe_n_dith_med"]) > NDITH_ABOVE and int(fl(q["spe_error_flag"])) == 0
            and int(fl(q["spe_gal_error_flag"])) == 0): return "fail", "Q1 spectrum"
    z = fl(c["spe_z"])
    if not (ZMIN < z < ZMAX): return "fail", "Q3 window"
    if not (fl(c["spe_z_prob"]) >= ZPROB_MIN and fl(c["spe_z_rel"]) > ZREL_ABOVE): return "fail", "Q2 solution"
    if ha is None: return "fail", "Q4 no Halpha row"
    if int(fl(ha["spe_line_qual_gf"])) not in QUAL_OK: return "fail", "Q4 quality flag"
    if not (fl(ha["spe_line_flux_gf"]) >= FLUX_MIN): return "fail", "Q4 flux"
    if not (0.0 < fl(ha["spe_line_fwhm_gf"]) <= FWHM_MAX): return "fail", "Q4 width"
    if not (fl(ha["spe_line_snr_gf"]) >= snr_min): return "fail", "Q4 S/N"
    if guard:
        if not (z >= zup + DZ_ABOVE): return "fail", "G1 not above the lens"
        for nm, l1, l2 in BANDS:
            if (1.0 + zlo) * l1 / HA - 1.0 - PAD <= z <= (1.0 + zup) * l2 / HA - 1.0 + PAD: return "ambig", "G2 " + nm
    return "secure", ""

def clopper(k, n, a=0.05):
    lo = 0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k))
    return lo, hi

def f_word(st):
    if st["N"] < F_NMIN: return None
    if st["b_med_hi"] <= F_HOLDS: return "LENS GATE HOLDS"
    if st["b_med_lo"] >= F_FAILS: return "LENS GATE FAILS"
    return "NO VERDICT"

# ================================================================== main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--interim", action="store_true")
    a = ap.parse_args(); t0 = time.time()
    tdir = os.path.join(a.data_dir, "nisp_tables")
    parts = ("first",) if a.interim else ("first", "rest")
    tag = "euc3" + ("_interim" if a.interim else "") + ("_MUTATE_" + MUT if MUT else "")
    RES = dict(lane="EUC3", criteria_commit="bf72d787a8", mutate=MUT, footings=E.FOOT, interim=bool(a.interim))
    P("EUC3 (NISP SOURCE REDSHIFTS)%s%s" % ("   *** MUTATE = %s ***" % MUT if MUT else "",
      "   *** INTERIM: sample S, truth lenses and grade X only; the rest of the grade A/B systems not yet fetched ***" if a.interim else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e" % (E.FOOT["canonical"], E.FOOT["alt"]))

    # ---------------------------------------------------------------- catalogue
    P("\n[data]")
    rows, _ = E.load(a.data_dir)
    key = {r["id"]: r for r in rows}
    obj = {}
    with open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): obj[r["Unique_Identifier"]] = r
    Pm, _ = E.select(rows, ("A",)); Sm, _ = E.select(rows, ("A", "B"))
    Um = [r for r in rows if r["tE"] > 0 and r["te"] > 0 and 0.6 <= r["n"] <= 10.0 and r["z"] > 0 and r["lm"] > 0]
    inP, inS, inU = {r["id"] for r in Pm}, {r["id"] for r in Sm}, {r["id"] for r in Um}
    sysrow = {}
    with open(os.path.join(tdir, "systems.csv"), newline="") as f:
        for r in csv.DictReader(f): sysrow[int(r["sid"])] = r
    part_of = {r["unique_identifier"]: r["part"] for r in sysrow.values()}
    lens_ids = sorted(r["id"] for r in rows if r["tE"] > 0 and part_of[r["id"]] in parts)
    Um = [r for r in Um if part_of[r["id"]] in parts]; inU = {r["id"] for r in Um}
    x_ids = sorted(i for i, o in obj.items() if o["Expert_Grade"].strip() == "X")
    S_sorted = sorted(Sm, key=lambda r: r["id"])
    thE = {i: key[i]["tE"] for i in lens_ids}
    for j, i in enumerate(x_ids): thE[i] = S_sorted[(j * len(S_sorted)) // len(x_ids)]["tE"]
    P("  lens systems searched (grade A/B, theta_E > 0): %d;  P %d, S %d, U %d;  null systems (grade X): %d"
      % (len(lens_ids), len(Pm), len(Sm), len(Um), len(x_ids)))

    # ---------------------------------------------------------------- fetched tables
    mer = {}
    for r in read_tab(tdir, "mer", parts):
        s = sysrow[int(r["sid"])]
        ra0, de0 = float(s["ra"]), float(s["dec"])
        sep = 3600.0 * math.hypot((fl(r["ra"]) - ra0) * math.cos(math.radians(de0)), fl(r["dec"]) - de0)
        mer.setdefault(s["unique_identifier"], []).append(dict(oid=int(r["object_id"]), sep=sep, fh=fl(r["flux_h_templfit"])))
    qual, gal, lin = (by_obj(read_tab(tdir, k, parts)) for k in ("qual", "gal", "lines"))
    phz, cls = by_obj(read_tab(tdir, "phz", parts)), by_obj(read_tab(tdir, "cls", parts))
    P("  fetched: MER rows for %d systems; objects with a quality row %d, a galaxy solution %d, line rows %d, a photo-z %d"
      % (len(mer), len(qual), len(gal), len(lin), len(phz)))

    # ---------------------------------------------------------------- association, interval, rule
    def interval(lid, lens_oid):
        o = obj[lid]; zs = o["desi_deflector_specz"].strip()
        if zs and fl(zs) > 0: return fl(zs) - 0.01, fl(zs) + 0.01, "DESI"
        los, his, src = [], [], []
        k = key.get(lid)
        if k is not None and k["zlo"] > 0 and k["zhi"] > 0 and k["zhi"] >= k["zlo"]:
            los.append(k["zlo"]); his.append(k["zhi"]); src.append("ECLIPSE")
        for p in phz.get(lens_oid, []):
            lo, hi = fl(p["phz_70_int_1"]), fl(p["phz_70_int_2"])
            if np.isfinite(lo) and np.isfinite(hi) and lo >= 0 and hi > 0 and hi >= lo:
                los.append(lo); his.append(hi); src.append("PHZ")
        if not los: return None
        return min(los), max(his), "+".join(sorted(set(src)))

    def system(lid):
        """association and the rule for one system; classes per tier"""
        ra = min(thE[lid] + R_EXTRA, R_CAP)
        cnt = sorted([m for m in mer.get(lid, []) if m["sep"] <= ra], key=lambda m: m["sep"])
        d = dict(id=lid, r_a=ra, n_counted=len(cnt), lens_oid=None, evaluable=False, spectra=[], why="")
        if not cnt or cnt[0]["sep"] > LENS_SEP: d["why"] = "no lens object"; return d
        d["lens_oid"] = cnt[0]["oid"]; d["lens_fh"] = cnt[0]["fh"]
        iv = interval(lid, cnt[0]["oid"])
        if iv is None: d["why"] = "no redshift interval"; return d
        d["zlo"], d["zup"], d["zsrc"] = iv
        pz = phz.get(cnt[0]["oid"], [])
        d["lens_phz"] = fl(pz[0]["phz_median"]) if pz else float("nan")
        for m in cnt:
            c0 = [c for c in gal.get(m["oid"], []) if int(fl(c["spe_rank"])) == 0]
            if len(c0) > 1: ANOM["multi_spectra_objects"] += 1
            for c in c0:
                q = pair(c, qual.get(m["oid"], []))
                if q is None: ANOM["unpaired_quality"] += 1
                lr = [r for r in lin.get(m["oid"], []) if int(fl(r["spe_rank"])) == 0]
                if len(c0) > 1: lr = [r for r in lr if obskey(r) == obskey(c)]
                ln = {}
                for r in lr: ln.setdefault(r["spe_line_name"], r)
                ha = ln.get("Halpha")
                sp = dict(oid=m["oid"], sep=m["sep"], role="lens object" if m["oid"] == d["lens_oid"] else "neighbour",
                          z=fl(c["spe_z"]), zprob=fl(c["spe_z_prob"]), zrel=fl(c["spe_z_rel"]),
                          npix=fl(q["spe_npix"]) if q else float("nan"), ndith=fl(q["spe_n_dith_med"]) if q else float("nan"),
                          snr=fl(ha["spe_line_snr_gf"]) if ha else float("nan"), flux=fl(ha["spe_line_flux_gf"]) if ha else float("nan"),
                          fwhm=fl(ha["spe_line_fwhm_gf"]) if ha else float("nan"), qualf=int(fl(ha["spe_line_qual_gf"])) if ha else -1,
                          cls=(cls.get(m["oid"], [{}])[0].get("spe_class", "") or "").strip(),
                          second=[n for n in SECOND if n in ln and fl(ln[n]["spe_line_snr_gf"]) >= 3.0 and int(fl(ln[n]["spe_line_qual_gf"])) in QUAL_OK],
                          alt=sorted((int(fl(x["spe_rank"])), round(fl(x["spe_z"]), 4), round(fl(x["spe_z_prob"]), 3))
                                     for x in gal.get(m["oid"], []) if obskey(x) == obskey(c) and int(fl(x["spe_rank"])) > 0))
                sp["T0"] = judge(c, q, ha, d["zlo"], d["zup"], 0.0, GUARD)      # every cut except the S/N threshold (output only)
                sp["q1"] = sp["T0"][1] not in ("no quality row", "Q1 spectrum")
                for tn, sn in TIERS: sp[tn] = judge(c, q, ha, d["zlo"], d["zup"], sn, GUARD)
                d["spectra"].append(sp)
        d["evaluable"] = any(sp["q1"] for sp in d["spectra"])
        if not d["evaluable"]: d["why"] = "no spectrum passing Q1"
        for tn, _ in TIERS:
            sec = sorted([sp for sp in d["spectra"] if sp[tn][0] == "secure"], key=lambda s: -s["snr"])
            amb = sorted([sp for sp in d["spectra"] if sp[tn][0] == "ambig"], key=lambda s: -s["snr"])
            if sec and max(abs(s["z"] - sec[0]["z"]) for s in sec) <= AGREE: d[tn] = ("SECURE", sec[0], len(sec))
            elif sec: d[tn] = ("CONFLICT", sec[0], len(sec))
            elif amb and max(abs(s["z"] - amb[0]["z"]) for s in amb) <= AGREE: d[tn] = ("AMBIGUOUS-OWN", amb[0], len(amb))
            else: d[tn] = ("none", None, 0)
        return d

    SYS = {i: system(i) for i in lens_ids + x_ids}
    P("  pairing: objects with more than one spectrum %d; spectra without a quality row %d; ambiguous pairings %d"
      % (ANOM["multi_spectra_objects"], ANOM["unpaired_quality"], ANOM["ambiguous_pair"]))
    RES["pairing"] = dict(ANOM)

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok))
        P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    engP, zP, REP, _, _, _ = E.build(Pm)
    binf = {nm: E.run_b(engP, zP, REP, E.ZS_INF, a0, "S") for nm, a0 in E.FOOT.items()}
    k1 = (float(np.median(binf["canonical"])), float(np.median(binf["alt"])))
    k1ok = len(Pm) == 3192 and abs(k1[0] + 0.019) <= 0.001 and abs(k1[1] + 0.044) <= 0.001
    ck("K1", "EUC1 reproduced: N(P) = 3192, source-free b_med law S = -0.019 / -0.044 to 0.001", "N = %d, %+.4f / %+.4f" % (len(Pm), k1[0], k1[1]), k1ok or MUT == "newton")
    ar = key[ANCHOR[0]]; zsp = fl(obj[ANCHOR[0]]["desi_deflector_specz"])
    lma = ar["lm"] + 2.0 * math.log10(float(E.EUCLID.DL(zsp)) / float(E.EUCLID.DL(ar["z"])))
    enga, za, REa, _, _, _ = E.build([ar], z=np.array([zsp]), lm=np.array([lma]))
    anc = {nm: float(E.run_b(enga, za, REa, ANCHOR[1], a0, "S")[0]) for nm, a0 in E.FOOT.items()}
    k2ok = abs(anc["canonical"] - ANCHOR[2][0]) <= 0.002 and abs(anc["alt"] - ANCHOR[2][1]) <= 0.002
    ck("K2", "EUC2 anchor L015763 at z_l(DESI), z_s = 1.3657: b = +0.231 / +0.215 to 0.002", "%+.4f / %+.4f" % (anc["canonical"], anc["alt"]), k2ok or MUT == "newton")
    RES["anchor_b"] = anc
    k3 = {}
    for nm, ids in (("S", sorted(inS)), ("X", x_ids)):
        giv = [i for i in ids if obj[i]["MER_object_id"].strip()]
        hit = sum(1 for i in giv if SYS[i]["lens_oid"] is not None and SYS[i]["lens_oid"] == int(obj[i]["MER_object_id"]))
        k3[nm] = (hit, len(giv))
    ck("K3", "lens object found by position carries ECLIPSE's MER_object_id in >= 95 % (S; X)",
       "%d / %d = %.3f ; %d / %d = %.3f" % (k3["S"][0], k3["S"][1], k3["S"][0] / max(k3["S"][1], 1), k3["X"][0], k3["X"][1], k3["X"][0] / max(k3["X"][1], 1)),
       all(v[0] >= 0.95 * v[1] and v[1] > 0 for v in k3.values()))
    raS = float(np.median([SYS[i]["r_a"] for i in inS])); raX = float(np.median([SYS[i]["r_a"] for i in x_ids]))
    ck("K4", "median association radius of X within 2 % of S's", "S %.3f\", X %.3f\"" % (raS, raX), abs(raX / raS - 1.0) <= 0.02)
    try:
        need, nids, ver = [], 0, []
        for p in parts:
            man = json.load(open(os.path.join(tdir, "ids_manifest_%s.json" % p))); ver += json.load(open(os.path.join(tdir, "verify_%s.json" % p)))
            need += [("%s_%s_%06d.csv" % (k, p, c0)) for k in ("qual", "gal", "lines", "phz", "cls") for c0 in range(0, man["n_ids"], man["chunk"])]
            nids += man["n_ids"]
        miss = [f for f in need if not os.path.exists(os.path.join(tdir, f))]
        allm = {m["oid"] for v in mer.values() for m in v}
        nsys = sum(1 for r in sysrow.values() if r["part"] in parts)
        k5ok = not miss and len(ver) >= len(parts) and all(v["identical"] for v in ver) and len(allm) == nids
        k5v = ("%d systems queried, %d MER object ids (%d in the manifests), %d chunk files, missing %d; re-queried chunks identical: %s"
               % (nsys, len(allm), nids, len(need), len(miss), [v["identical"] for v in ver]))
    except Exception as ex:
        k5ok, k5v = False, "manifest or verify file unreadable (%s)" % type(ex).__name__
    ck("K5", "fetch complete; three id chunks re-queried return identical rows", k5v, k5ok)

    # ---------------------------------------------------------------- coverage, like for like
    P("\n[coverage, like for like]")
    COV = {}
    for nm, ids in (("P", sorted(inP)), ("S", sorted(inS)), ("U", sorted(inU)), ("all A/B", lens_ids), ("X", x_ids)):
        ev = [i for i in ids if SYS[i]["evaluable"]]
        why = {}
        for i in ids:
            if not SYS[i]["evaluable"]: why[SYS[i]["why"]] = why.get(SYS[i]["why"], 0) + 1
        fh = np.array([SYS[i].get("lens_fh", np.nan) for i in ev]); pzm = np.array([SYS[i].get("lens_phz", np.nan) for i in ev])
        COV[nm] = dict(N=len(ids), evaluable=len(ev), frac=len(ev) / max(len(ids), 1), not_evaluable=why,
                       lens_H_flux_uJy_med=float(np.nanmedian(fh)) if len(ev) else None, lens_phz_med=float(np.nanmedian(pzm)) if len(ev) else None,
                       n_counted_mean=float(np.mean([SYS[i]["n_counted"] for i in ids])))
        P("  %-8s N = %5d, evaluable %5d (%.3f); lens-object median H flux %.1f uJy, median pipeline photo-z %.3f; counted objects per system %.2f; not evaluable: %s"
          % (nm, len(ids), len(ev), COV[nm]["frac"], COV[nm]["lens_H_flux_uJy_med"] or float("nan"), COV[nm]["lens_phz_med"] or float("nan"), COV[nm]["n_counted_mean"], why))
    RES["coverage"] = COV
    cover_ok = COV["S"]["frac"] >= COVER_MIN and COV["X"]["frac"] >= COVER_MIN
    P("  coverage gate (>= %.0f %% of S and of X evaluable): %s" % (100 * COVER_MIN, "PASS" if cover_ok else "FAIL"))

    # cut-by-cut census of evaluable lens-object spectra (S and X), tier T5
    for nm, ids in (("S", sorted(inS)), ("X", x_ids)):
        cen = {}
        for i in ids:
            for sp in SYS[i]["spectra"]:
                k = sp["T5"][1] or "SECURE"; cen[k] = cen.get(k, 0) + 1
        P("  %s spectra by first cut failed (T5): %s" % (nm, dict(sorted(cen.items(), key=lambda kv: -kv[1]))))
        RES["census_" + nm] = cen

    # ---------------------------------------------------------------- gates per tier
    GATE = {}
    for tn, sn in TIERS:
        P("\n[tier %s: H-alpha S/N >= %.0f]" % (tn, sn))
        cnt = {}
        for nm, ids in (("P", sorted(inP)), ("S", sorted(inS)), ("U", sorted(inU)), ("all A/B", lens_ids), ("X", x_ids)):
            c = dict(E=sum(SYS[i]["evaluable"] for i in ids))
            for k in ("SECURE", "CONFLICT", "AMBIGUOUS-OWN"): c[k] = sum(1 for i in ids if SYS[i].get(tn, ("none",))[0] == k)
            cnt[nm] = c
            lo, hi = clopper(c["SECURE"], max(c["E"], 1))
            P("  %-8s evaluable %5d: SECURE %4d (rate %.4f [%.4f, %.4f]), CONFLICT %d, AMBIGUOUS-OWN %d"
              % (nm, c["E"], c["SECURE"], c["SECURE"] / max(c["E"], 1), lo, hi, c["CONFLICT"], c["AMBIGUOUS-OWN"]))
        lim = max(1.0, NULL_FRAC * cnt["S"]["SECURE"] * cnt["X"]["E"] / max(cnt["S"]["E"], 1))
        h2 = cnt["X"]["SECURE"] <= lim
        rX = cnt["X"]["SECURE"] / max(cnt["X"]["E"], 1)
        P("  H2 purity null: grade-X SECURE = %d against a limit of %.1f -> %s;  expected false among P / S: %.1f / %.1f (of %d / %d)"
          % (cnt["X"]["SECURE"], lim, "PASS" if h2 else "FAIL", rX * cnt["P"]["E"], rX * cnt["S"]["E"], cnt["P"]["SECURE"], cnt["S"]["SECURE"]))
        tr = []; h4 = True
        for lid, zt in TRUTH:
            d = SYS.get(lid)
            if d is None: tr.append(dict(id=lid, z_true=zt, outcome="not searched")); continue
            k, sp, _ = d.get(tn, ("none", None, 0))
            if k == "SECURE" and abs(sp["z"] - zt) <= AGREE: oc = "RECOVERED"
            elif k == "SECURE": oc = "CONTRADICTED"; h4 = False
            else: oc = "not found"
            det = [dict(role=s["role"], sep=round(s["sep"], 2), z=round(s["z"], 4), zprob=round(s["zprob"], 4), zrel=round(s["zrel"], 3), npix=s["npix"],
                        ndith=s["ndith"], snr=s["snr"], flux=s["flux"], fwhm=s["fwhm"], qual=s["qualf"], cls=s["cls"], cut=s[tn][1] or "SECURE", lower_ranks=s["alt"])
                   for s in d["spectra"]]
            tr.append(dict(id=lid, z_true=zt, outcome=oc, system_class=k, z_found=(sp["z"] if sp else None), why=d["why"],
                           interval=(d.get("zlo"), d.get("zup"), d.get("zsrc")), spectra=det))
            P("  H4 truth %s (z_s = %.4f): %s%s" % (lid, zt, oc, "" if oc == "RECOVERED" else "  [system class %s; %s]" % (k, d["why"] or "see spectra")))
            for s in det:
                P("       %-11s sep %.2f\": z0 = %.4f prob %.3f rel %.3f npix %.0f dith %.0f | Ha S/N %.1f flux %.2e fwhm %.0f qual %d | %s | first cut: %s | lower ranks %s"
                  % (s["role"], s["sep"], s["z"], s["zprob"], s["zrel"], s["npix"], s["ndith"], s["snr"], s["flux"], s["fwhm"], s["qual"], s["cls"], s["cut"], s["lower_ranks"]))
        nrec = sum(t["outcome"] == "RECOVERED" for t in tr)
        P("  H4 truth gate: %d of %d recovered, %d contradicted -> %s" % (nrec, len(TRUTH), sum(t["outcome"] == "CONTRADICTED" for t in tr), "PASS" if h4 else "FAIL"))
        GATE[tn] = dict(counts=cnt, H2_limit=lim, H2=bool(h2), H4=bool(h4), truth=tr, recovered=nrec, null_rate=rX)
    RES["gates"] = GATE

    # null hits, listed
    P("\n[grade-X null hits, listed (T5)]")
    NH = []
    for i in x_ids:
        k, sp, n = SYS[i].get("T5", ("none", None, 0))
        if k in ("SECURE", "CONFLICT"):
            d = SYS[i]
            NH.append(dict(id=i, cls=k, z_s=sp["z"], snr=sp["snr"], flux=sp["flux"], fwhm=sp["fwhm"], role=sp["role"], sep=sp["sep"], zlo=d["zlo"], zup=d["zup"],
                           lens_phz=d["lens_phz"], spe_class=sp["cls"], second="+".join(sp["second"]), T8=d["T8"][0]))
            P("  %s %-8s z = %.4f S/N %.1f flux %.2e fwhm %.0f | %s sep %.2f\" | interval [%.2f, %.2f] photo-z %.2f | class %s | second lines: %s | T8: %s"
              % (i, k, sp["z"], sp["snr"], sp["flux"], sp["fwhm"], sp["role"], sp["sep"], d["zlo"], d["zup"], d["lens_phz"], sp["cls"], "+".join(sp["second"]) or "none", d["T8"][0]))
    if not NH: P("  none")
    RES["null_hits"] = NH

    # ---------------------------------------------------------------- tier ladder
    allok = all(v["ok"] for v in CK.values())
    tier = None
    for tn, _ in TIERS:
        if GATE[tn]["H2"] and GATE[tn]["H4"]: tier = tn; break
    evaluable = allok and cover_ok and tier is not None
    P("\n[tier ladder]")
    P("  T5: H2 %s, H4 %s;  T8: H2 %s, H4 %s  ->  %s"
      % (*("PASS" if GATE[t][g] else "FAIL" for t in ("T5", "T8") for g in ("H2", "H4")),
         ("reading tier " + tier + (" (frozen fallback)" if tier == "T8" else "")) if tier else "no tier passes: NOT EVALUABLE"))
    rt = tier or "T5"       # a void reading is still printed, labelled, at T5

    # ---------------------------------------------------------------- reading
    P("\n[reading at tier %s%s: b at the true source redshift]" % (rt, "" if evaluable else ", VOID (the search is not evaluable)"))
    READ = {}
    def reading(name, sample, zs_of, zl_desi=False, note=""):
        sel = [r for r in sample if r["id"] in zs_of]
        zs = np.array([zs_of[r["id"]] for r in sel]); zl = E.arr(sel, "z") if sel else np.array([])
        lm = E.arr(sel, "lm") if sel else np.array([])
        if zl_desi and sel:
            zsp = np.array([r["zspec"] if np.isfinite(r["zspec"]) and r["zspec"] > 0 else r["z"] for r in sel])
            lm = lm + 2.0 * np.log10(E.EUCLID.DL(zsp) / E.EUCLID.DL(zl)); zl = zsp
        keep = zl < zs - 0.2
        dropped = int(np.sum(~keep)); sel = [r for r, k in zip(sel, keep) if k]; zs, zl, lm = zs[keep], zl[keep], lm[keep]
        out = dict(N=len(sel), dropped=dropped)
        if not sel:
            P("  %-22s N = 0%s%s" % (name, " (dropped %d with z_l >= z_s - 0.2)" % dropped if dropped else "", note)); READ[name] = out; return out
        eng, z, RE, _, _, _ = E.build(sel, z=zl, lm=lm)
        out["ids"] = [r["id"] for r in sel]; out["b"] = {}
        for law in ("S", "B"):
            for nm, a0 in E.FOOT.items():
                bt = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs), a0, law)
                bi = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, law)
                st, si = E.stats(bt), E.stats(bi)
                out["%s_%s" % (law, nm)] = dict(true=st, inf=si, cost_med=float(np.median(bt - bi)), n_above_025=int(np.sum(bt > 0.25)))
                out["b"]["%s_%s" % (law, nm)] = [float(x) for x in bt]; out["b"]["inf_%s_%s" % (law, nm)] = [float(x) for x in bi]
                if law == "S":
                    P("  %-22s law S %-9s N = %3d  b_med(true z_s) = %+.3f [%+.3f, %+.3f]   source-free b_med = %+.3f   n(b > 0.25) = %d%s%s"
                      % (name, nm, len(sel), st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], int(np.sum(bt > 0.25)),
                         "  (dropped %d)" % dropped if dropped else "", note))
        out["z_s_med"] = float(np.median(zs)); out["z_l_med"] = float(np.median(zl))
        READ[name] = out; return out

    def zs_map(tn, classes=("SECURE",), flt=None):
        m = {}
        for i in lens_ids:
            k, sp, _ = SYS[i].get(tn, ("none", None, 0))
            if k in classes and (flt is None or flt(SYS[i], sp)): m[i] = sp["z"]
        return m
    ZS = zs_map(rt)
    rP = reading("P", Pm, ZS); rS = reading("S", Sm, ZS); rU = reading("U", Um, ZS, note="   [not quality-cut]")
    for law in ("B",):
        for nm in E.FOOT:
            if rP["N"]:
                st = rP["%s_%s" % (law, nm)]["true"]
                P("  %-22s law B %-9s N = %3d  b_med(true z_s) = %+.3f [%+.3f, %+.3f]" % ("P", nm, rP["N"], st["b_med"], st["b_med_lo"], st["b_med_hi"]))

    P("\n[robustness, law S; reported, cannot change the word]")
    reading("1 P, DESI deflector z", Pm, ZS, zl_desi=True)
    reading("2 P, tier T8 only", Pm, zs_map("T8"))
    reading("3 P, two-line subset", Pm, zs_map(rt, flt=lambda d, sp: len(sp["second"]) > 0))
    reading("4 P, [O III] extreme", Pm, {i: ((1.0 + z) * HA / OIII - 1.0 if z > 1.29 else z) for i, z in ZS.items()})
    reading("5 P, + AMBIGUOUS-OWN", Pm, zs_map(rt, classes=("SECURE", "AMBIGUOUS-OWN")))
    reading("6 P, theta_E <= 2.5", [r for r in Pm if r["tE"] <= 2.5], ZS)
    reading("7 S, two-line subset", Sm, zs_map(rt, flt=lambda d, sp: len(sp["second"]) > 0))
    RES["reading"] = {k: {kk: vv for kk, vv in v.items() if kk != "b"} for k, v in READ.items()}

    # ---------------------------------------------------------------- per-lens table
    bP = {}
    for nm_, rr in (("U", rU),):
        if rr["N"]:
            for j, i in enumerate(rr["ids"]):
                bP[i] = {k: v[j] for k, v in rr["b"].items()}
    with open(os.devnull if MUT else os.path.join(HERE, tag + "_sources.csv"), "w", newline="") as f:      # twins write no tables
        w = csv.writer(f)
        w.writerow(["unique_identifier", "grade", "in_P", "in_S", "in_U", "class_T5", "class_T8", "z_l_catalogue", "z_lo", "z_up", "interval_source",
                    "z_s", "Ha_snr", "Ha_flux", "Ha_fwhm_A", "Ha_qual", "z_prob", "z_rel", "mer_object_id", "role", "sep_arcsec", "n_spectra_same_class",
                    "second_lines", "spe_class", "theta_E_arcsec", "b_S_canonical", "b_S_alt", "b_inf_S_canonical", "b_inf_S_alt"])
        nrow = 0
        for i in lens_ids:
            d = SYS[i]; k5, sp, n = d.get("T5", ("none", None, 0))
            if k5 == "none": continue
            b = bP.get(i, {}) if k5 == "SECURE" else {}
            w.writerow([i, key[i]["grade"], i in inP, i in inS, i in inU, k5, d["T8"][0], "%.3f" % key[i]["z"], "%.3f" % d["zlo"], "%.3f" % d["zup"], d["zsrc"],
                        "%.4f" % sp["z"], "%.2f" % sp["snr"], "%.3e" % sp["flux"], "%.1f" % sp["fwhm"], sp["qualf"], "%.4f" % sp["zprob"], "%.3f" % sp["zrel"],
                        sp["oid"], sp["role"], "%.2f" % sp["sep"], n, "+".join(sp["second"]), sp["cls"], "%.3f" % key[i]["tE"]] +
                       [("%.4f" % b[c]) if c in b else "" for c in ("S_canonical", "S_alt", "inf_S_canonical", "inf_S_alt")])
            nrow += 1
    P("\n  per-lens table: %s (%d lens systems with a T5 class)" % ("not written by a twin" if MUT else tag + "_sources.csv", nrow))
    # per-system table of every evaluable system (lenses and null), for the disclosed post hoc diagnostics; output only
    with open(os.devnull if MUT else os.path.join(HERE, tag + "_systems.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "grade", "in_P", "in_S", "in_U", "r_a_arcsec", "z_lo", "z_up", "interval_source", "lens_H_flux_uJy",
                    "lens_phz_median", "class_T5", "class_T8", "pass_all_but_snr_z", "pass_all_but_snr_snr", "pass_all_but_snr_role", "pass_all_but_snr_second"])
        for i in lens_ids + x_ids:
            d = SYS[i]
            if not d["evaluable"]: continue
            p0 = sorted([sp for sp in d["spectra"] if sp["T0"][0] == "secure"], key=lambda sp: -sp["snr"])
            w.writerow([i, obj[i]["Expert_Grade"].strip(), i in inP, i in inS, i in inU, "%.3f" % d["r_a"], "%.3f" % d["zlo"], "%.3f" % d["zup"], d["zsrc"],
                        "%.2f" % d["lens_fh"], "%.3f" % d["lens_phz"], d["T5"][0], d["T8"][0], ";".join("%.4f" % sp["z"] for sp in p0),
                        ";".join("%.2f" % sp["snr"] for sp in p0), ";".join(sp["role"] for sp in p0), ";".join("+".join(sp["second"]) or "-" for sp in p0)])
    if rP["N"]:
        P("  sample P per lens (law S): id, z_l, z_s, Ha S/N, role, theta_E, second lines, b canonical / alt (source-free alt)")
        for j in np.argsort([ZS[i] for i in rP["ids"]]):
            i = rP["ids"][j]; sp = SYS[i][rt][1]
            P("    %s %.3f %.4f %5.1f %-11s %.2f\" %-18s %+.3f / %+.3f  (%+.3f)" % (i, key[i]["z"], sp["z"], sp["snr"], sp["role"], key[i]["tE"],
              "+".join(sp["second"]) or "-", rP["b"]["S_canonical"][j], rP["b"]["S_alt"][j], rP["b"]["inf_S_alt"][j]))

    # ---------------------------------------------------------------- verdict
    P("\n[summary]")
    words = {}
    for nm in E.FOOT:
        if not evaluable: words[nm] = "NOT EVALUABLE"
        elif rP["N"] >= F_NMIN: words[nm] = f_word(rP["S_" + nm]["true"])
        else: words[nm] = "EARLY READING, NOT A GATE"
    verdict = "%s / %s" % (words["canonical"], words["alt"])
    P("  instrument checks: %s;  coverage: %s;  reading tier: %s" % ("all pass" if allok else "FAILED", "pass" if cover_ok else "FAIL", tier or "none"))
    P("  N(P) with a secure source redshift = %d (EUC1-F needs %d)" % (rP["N"], F_NMIN))
    P("  LANE WORD (canonical / alt): %s%s" % (verdict, (" [tier %s%s]" % (tier, ", frozen fallback" if tier == "T8" else "")) if evaluable else ""))
    P("  kappa = 1/2 FITTED. One-sided: no outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    RES.update(checks=CK, checks_all_pass=allok, coverage_ok=cover_ok, tier=tier, evaluable=bool(evaluable), verdict=verdict, N_P=rP["N"])

    code = 0 if evaluable else 3
    if MUT:
        try: ref = json.load(open(os.path.join(HERE, tag.split("_MUTATE_")[0] + "_results.json")))
        except Exception: ref = None
        bite = False
        if ref is None: P("\n[MUTATE %s] no reference results: cannot judge" % MUT)
        elif MUT == "newton":
            samp = next((s for s in ("P", "S", "U") if ref["reading"].get(s, {}).get("N", 0) >= 1 and READ.get(s, {}).get("N", 0) >= 1), None)
            up_a = all(anc[k] > ref["anchor_b"][k] for k in E.FOOT)
            up_s = samp is not None and all(READ[samp]["S_" + k]["true"]["b_med"] > ref["reading"][samp]["S_" + k]["true"]["b_med"] for k in E.FOOT)
            bite = up_a and (up_s or samp is None)
            P("\n[MUTATE newton] anchor b %+.3f / %+.3f (ref %+.3f / %+.3f); sample %s b_med %s (ref %s) -> %s"
              % (anc["canonical"], anc["alt"], ref["anchor_b"]["canonical"], ref["anchor_b"]["alt"], samp,
                 None if samp is None else "%+.3f / %+.3f" % tuple(READ[samp]["S_" + k]["true"]["b_med"] for k in E.FOOT),
                 None if samp is None else "%+.3f / %+.3f" % tuple(ref["reading"][samp]["S_" + k]["true"]["b_med"] for k in E.FOOT),
                 "rose on both footings, as required; exit 1" if bite else "DID NOT RISE"))
        elif MUT == "noguard":
            n0, n1 = ref["gates"]["T5"]["counts"]["X"]["SECURE"], GATE["T5"]["counts"]["X"]["SECURE"]
            bite = n1 > n0
            P("\n[MUTATE noguard] grade-X SECURE systems (T5): %d (ref %d); lens S: %d (ref %d) -> %s"
              % (n1, n0, GATE["T5"]["counts"]["S"]["SECURE"], ref["gates"]["T5"]["counts"]["S"]["SECURE"],
                 "the null count rose, as required; exit 1" if bite else "DID NOT RISE"))
        RES["mutate_bites"] = bool(bite); code = 1 if bite else 2
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)

if __name__ == "__main__":
    main()
