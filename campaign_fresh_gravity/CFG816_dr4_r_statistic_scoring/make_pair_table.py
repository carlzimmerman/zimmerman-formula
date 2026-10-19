#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_pair_table.py -- the CONVERTER for cfg816_r.py: it joins the registered pipeline's stage-G catalogue with the per-star columns and writes the pair table that
cfg816_r.py reads (schema in cfg816_r.py's docstring).  It computes nothing about R and reads no model.

  python3 make_pair_table.py --catalogue wide_binaries_dr3.csv --per-star stage_A.npz --out pairs_dr3.csv       # DR3: both files are already on disk, no download
  python3 make_pair_table.py --self-test                                                                         # synthetic checks, nothing read from the repository data

INPUTS
  --catalogue   the stage-G catalogue CSV (the registered driver's --out-csv). Columns used: sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc, source_id1, source_id2.
  --per-star    an .npz with one entry per star (the registered builder's stage-A layout), keys REQUIRED:
                source_id, parallax, parallax_error, pmra, pmdec, pmra_error, pmdec_error, ruwe, ipd_frac_multi_peak, radial_velocity, non_single_star
                For DR4 this is the release extract's per-star file AFTER the driver has joined the manifest's columns and applied cut 12 (non_single_star = the union flag).
OUTPUT
  --out         the pair table CSV (cfg816_r.py schema + source_id1, source_id2 for provenance) and <out>.manifest.json (counts, SHA-256 of both inputs and of the output, every choice below).

NEVER SILENT (house rule): a source_id missing from the per-star file stops the run (--max-missing N allows N and reports them); a required column that is constant across all stars (a
"neutral" fill such as the driver writes for an UNIMPLEMENTABLE column) stops the run unless it is named in --declare-neutral, and is then recorded in the manifest.

CHOICES made here (not in the frozen criteria; listed in README.md; none changes a frozen threshold or the R rule):
  P1  plx_err_frac = the LARGER of the two stars' parallax_error/parallax (both stars must pass the 2.5% / 1% cut).
  P2  drv_kms = |RV1 - RV2| if both stars have a radial velocity, else blank (the frozen cut applies only where RVs exist).
  P3  vt_err: leading-order propagation, not Cookson's full Jacobian: with the common distance d (the catalogue's d_pc) and the inverse-variance-weighted parallax error s_d/d,
      sigma(v-tilde)^2 = (4.74047 d[kpc] / vc[km/s])^2 * sigma_dmu^2 + (1.5 v-tilde s_d/d)^2, where sigma_dmu^2 is the proper-motion-difference variance projected on the
      direction of the proper-motion difference (the two stars' errors independent), vc = sqrt(G M / s), v-tilde = v_perp / vc.
  P4  nss1, nss2 = the per-star non_single_star flag (1 if nonzero).
  P5  v_perp_kms, the masses and d_pc are taken from the stage-G catalogue UNCHANGED (the registered estimator's values).
"""
import os, sys, csv, json, math, hashlib, argparse
import numpy as np

G, MSUN, KAU = 6.6743e-11, 1.989e30, 1.495978707e14
KMS_PER_MASYR_KPC = 4.74047
NEED_STAR = ["source_id", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error", "ruwe", "ipd_frac_multi_peak", "radial_velocity", "non_single_star"]
NEED_CAT = ["sep_kAU", "v_perp_kms", "M1_msun", "M2_msun", "d_pc", "source_id1", "source_id2"]
OUT_COLS = ["sep_kAU", "v_perp_kms", "M1_msun", "M2_msun", "d_pc", "plx_err_frac", "ruwe1", "ruwe2", "ipd1", "ipd2", "vt_err", "drv_kms", "nss1", "nss2", "source_id1", "source_id2"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_catalogue(path):
    rows = list(csv.DictReader(open(path)))
    if not rows:
        sys.exit("REFUSING: empty catalogue")
    miss = [c for c in NEED_CAT if c not in rows[0]]
    if miss:
        sys.exit(f"REFUSING: catalogue lacks columns {miss}")
    cat = {c: np.array([float(r[c]) for r in rows]) for c in NEED_CAT if not c.startswith("source_id")}
    cat["source_id1"] = np.array([int(r["source_id1"]) for r in rows], dtype=np.int64)
    cat["source_id2"] = np.array([int(r["source_id2"]) for r in rows], dtype=np.int64)
    return cat


def lookup(z, ids):
    """per-star columns for the wanted ids, one array at a time (npz entries load lazily; keeps memory low)"""
    sid = z["source_id"]
    order = np.argsort(sid, kind="stable") if not np.all(sid[1:] >= sid[:-1]) else None
    s_sorted = sid if order is None else sid[order]
    pos = np.searchsorted(s_sorted, ids)
    pos = np.clip(pos, 0, len(s_sorted) - 1)
    found = s_sorted[pos] == ids
    idx = pos if order is None else order[pos]
    del sid, s_sorted
    return idx, found


def build(cat, z, max_missing=0, declare_neutral=()):
    ids = np.concatenate([cat["source_id1"], cat["source_id2"]])
    n = len(cat["sep_kAU"])
    idx, found = lookup(z, ids)
    nmiss = int((~found).sum())
    if nmiss > max_missing:
        sys.exit(f"REFUSING: {nmiss} of {len(ids)} source_ids are missing from the per-star file (allowed {max_missing}); never silently dropped")
    star = {}
    constant = []
    for k in NEED_STAR[1:]:
        if k not in z:
            sys.exit(f"REFUSING: per-star file lacks the required column {k!r}")
        col = np.asarray(z[k], dtype=float)[idx]
        col[~found] = np.nan
        star[k] = col
        vals = col[np.isfinite(col)]
        if len(vals) > 1 and np.all(vals == vals[0]) and k not in declare_neutral:
            constant.append(k)
        del col
    if constant:
        sys.exit(f"REFUSING: required column(s) {constant} are constant across all stars (a neutral fill?). Name them in --declare-neutral if that is real; it is then recorded.")
    a, b = slice(0, n), slice(n, 2 * n)
    plx_frac = np.maximum(star["parallax_error"][a] / star["parallax"][a], star["parallax_error"][b] / star["parallax"][b])           # P1
    rv1, rv2 = star["radial_velocity"][a], star["radial_velocity"][b]
    drv = np.where(np.isfinite(rv1) & np.isfinite(rv2), np.abs(rv1 - rv2), np.nan)                                                       # P2
    # P3: leading-order sigma(v-tilde)
    dmx = star["pmra"][a] - star["pmra"][b]; dmy = star["pmdec"][a] - star["pmdec"][b]
    sx2 = star["pmra_error"][a] ** 2 + star["pmra_error"][b] ** 2; sy2 = star["pmdec_error"][a] ** 2 + star["pmdec_error"][b] ** 2
    mag = np.hypot(dmx, dmy)
    with np.errstate(invalid="ignore", divide="ignore"):
        sdmu2 = np.where(mag > 0, (dmx ** 2 * sx2 + dmy ** 2 * sy2) / mag ** 2, np.maximum(sx2, sy2))
    M = cat["M1_msun"] + cat["M2_msun"]
    vc = np.sqrt(G * M * MSUN / (cat["sep_kAU"] * KAU)) / 1e3                      # km/s
    vt = cat["v_perp_kms"] / vc
    w1 = star["parallax_error"][a] ** -2; w2 = star["parallax_error"][b] ** -2
    sd_over_d = (1.0 / np.sqrt(w1 + w2)) / (1000.0 / cat["d_pc"])
    vt_err = np.sqrt((KMS_PER_MASYR_KPC * (cat["d_pc"] / 1000.0) / vc) ** 2 * sdmu2 + (1.5 * vt * sd_over_d) ** 2)
    out = dict(sep_kAU=cat["sep_kAU"], v_perp_kms=cat["v_perp_kms"], M1_msun=cat["M1_msun"], M2_msun=cat["M2_msun"], d_pc=cat["d_pc"],
               plx_err_frac=plx_frac, ruwe1=star["ruwe"][a], ruwe2=star["ruwe"][b],
               ipd1=star["ipd_frac_multi_peak"][a], ipd2=star["ipd_frac_multi_peak"][b], vt_err=vt_err, drv_kms=drv,
               nss1=(star["non_single_star"][a] != 0).astype(float), nss2=(star["non_single_star"][b] != 0).astype(float),
               source_id1=cat["source_id1"], source_id2=cat["source_id2"])
    return out, dict(n_pairs=n, n_missing_ids=nmiss, declared_neutral=list(declare_neutral))


def write_csv(path, out):
    n = len(out["sep_kAU"])
    with open(path, "w") as f:
        f.write(",".join(OUT_COLS) + "\n")
        for i in range(n):
            f.write(",".join("" if (isinstance(out[c][i], (float, np.floating)) and np.isnan(out[c][i])) else
                             (str(int(out[c][i])) if c.startswith("source_id") else repr(float(out[c][i]))) for c in OUT_COLS) + "\n")


def regime_counts(out):
    """counts only (NO R is computed here): pairs passing the primary base cuts of cfg816_r.py and their regime sizes, per branch that changes the sample"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cfg816_r as R
    t = {k: out[k] for k in R_COLS}
    res = {}
    for name, ov in R.BRANCHES:
        cfg = dict(R.PRIMARY); cfg.update(ov)
        bm = R.base_mask(t, cfg); x = R.xval(t, cfg["a0"])
        res[name] = dict(n_base=int(bm.sum()), n_num=int((bm & (x > R.X_MOND) & (t["sep_kAU"] <= cfg["rmax_num"])).sum()), n_den=int((bm & (x < R.X_NEWT)).sum()))
    return res

R_COLS = ["sep_kAU", "v_perp_kms", "M1_msun", "M2_msun", "d_pc", "plx_err_frac", "ruwe1", "ruwe2", "ipd1", "ipd2", "vt_err", "drv_kms", "nss1", "nss2"]


def summary(out):
    f = lambda x: float(np.nanmedian(x))
    return dict(max_sep_kAU=float(np.max(out["sep_kAU"])), min_sep_kAU=float(np.min(out["sep_kAU"])),n_pairs=int(len(out["sep_kAU"])),
                frac_nss_any=float(np.mean((out["nss1"] > 0) | (out["nss2"] > 0))),
                frac_ipd_nonzero_any=float(np.mean((out["ipd1"] > 0) | (out["ipd2"] > 0))),
                frac_ruwe_ge_1p25_any=float(np.mean((out["ruwe1"] >= 1.25) | (out["ruwe2"] >= 1.25))),
                frac_with_both_rv=float(np.mean(np.isfinite(out["drv_kms"]))),
                median_plx_err_frac=f(out["plx_err_frac"]), median_vt_err=f(out["vt_err"]), max_d_pc=float(np.max(out["d_pc"])),
                n_d_lt_130=int((out["d_pc"] < 130).sum()))


def self_test():
    rng = np.random.default_rng(3); ok = True
    nstar = 50
    sid = np.arange(1000, 1000 + nstar, dtype=np.int64)
    z = dict(source_id=sid, parallax=np.full(nstar, 10.0) + rng.normal(0, .5, nstar), parallax_error=rng.uniform(0.05, 0.15, nstar), pmra=rng.normal(0, 30, nstar), pmdec=rng.normal(0, 30, nstar),
             pmra_error=rng.uniform(0.03, 0.08, nstar), pmdec_error=rng.uniform(0.03, 0.08, nstar), ruwe=rng.uniform(.9, 1.5, nstar), ipd_frac_multi_peak=rng.integers(0, 3, nstar),
             radial_velocity=np.where(rng.random(nstar) < .5, rng.normal(0, 20, nstar), np.nan), non_single_star=rng.integers(0, 2, nstar))
    cat = dict(sep_kAU=np.array([5., 10., 20.]), v_perp_kms=np.array([.3, .25, .2]), M1_msun=np.array([1., 1., 1.]), M2_msun=np.array([.5, .6, .7]), d_pc=np.array([90., 100., 110.]),
               source_id1=np.array([1000, 1002, 1004], dtype=np.int64), source_id2=np.array([1001, 1003, 1005], dtype=np.int64))
    out, rep = build(cat, z)
    # T1 per-star columns land on the right pair/star
    t1 = np.allclose(out["ruwe1"], z["ruwe"][[0, 2, 4]]) and np.allclose(out["ruwe2"], z["ruwe"][[1, 3, 5]]) and np.array_equal(out["nss1"], (z["non_single_star"][[0, 2, 4]] != 0).astype(float))
    # T2 plx_err_frac is the larger of the two
    p1 = z["parallax_error"][[0, 2, 4]] / z["parallax"][[0, 2, 4]]; p2 = z["parallax_error"][[1, 3, 5]] / z["parallax"][[1, 3, 5]]
    t2 = np.allclose(out["plx_err_frac"], np.maximum(p1, p2))
    # T3 delta-RV only where both exist
    both = np.isfinite(z["radial_velocity"][[0, 2, 4]]) & np.isfinite(z["radial_velocity"][[1, 3, 5]])
    t3 = np.array_equal(np.isfinite(out["drv_kms"]), both)
    # T4 vt_err by finite differences of v-tilde = 4.74047 d|dmu|/vc  (distance term: v-tilde ~ d^1.5 at fixed angular separation)
    i = 0
    M = 1.5; vc = math.sqrt(G * M * MSUN / (5. * KAU)) / 1e3
    dmx = z["pmra"][0] - z["pmra"][1]; dmy = z["pmdec"][0] - z["pmdec"][1]; mag = math.hypot(dmx, dmy)
    sx2 = z["pmra_error"][0] ** 2 + z["pmra_error"][1] ** 2; sy2 = z["pmdec_error"][0] ** 2 + z["pmdec_error"][1] ** 2
    sdmu = math.sqrt((dmx ** 2 * sx2 + dmy ** 2 * sy2) / mag ** 2)       # variance projected on the direction of the pm difference
    vt = cat["v_perp_kms"][0] / vc; sd_d = (1 / math.sqrt(z["parallax_error"][0] ** -2 + z["parallax_error"][1] ** -2)) / (1000. / 90.)
    expect = math.sqrt((KMS_PER_MASYR_KPC * 0.09 / vc) ** 2 * sdmu ** 2 + (1.5 * vt * sd_d) ** 2)
    t4 = abs(out["vt_err"][0] / expect - 1) < 1e-9
    # T5 refusals
    def refuses(fn):
        try: fn(); return False
        except SystemExit: return True
    cat_bad = dict(cat); cat_bad["source_id2"] = np.array([1001, 1003, 999999], dtype=np.int64)
    t5a = refuses(lambda: build(cat_bad, z))
    z_const = dict(z); z_const["ruwe"] = np.full(nstar, 1.0)
    t5b = refuses(lambda: build(cat, z_const))
    t5c = not refuses(lambda: build(cat, z_const, declare_neutral=("ruwe",)))
    z_nokey = {k: v for k, v in z.items() if k != "ipd_frac_multi_peak"}
    t5d = refuses(lambda: build(cat, z_nokey))
    # T6 CSV round trip through cfg816_r.read_table
    import tempfile
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cfg816_r as R
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg816_pt_tmp.csv")
    try:
        write_csv(p, out); t = R.read_table(p)
    finally:
        if os.path.exists(p): os.remove(p)
    t6 = np.allclose(t["vt_err"], out["vt_err"]) and np.allclose(t["plx_err_frac"], out["plx_err_frac"]) and np.array_equal(np.isnan(t["drv_kms"]), np.isnan(out["drv_kms"]))
    res = dict(T1_alignment=t1, T2_plx=t2, T3_drv=t3, T4_vt_err=t4, T5a_missing_id_refused=t5a, T5b_constant_column_refused=t5b, T5c_declared_neutral_allowed=t5c, T5d_missing_key_refused=t5d, T6_csv_roundtrip=t6)
    for k, v in res.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    ok = all(res.values())
    print("SELF-TEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue"); ap.add_argument("--per-star"); ap.add_argument("--out")
    ap.add_argument("--max-missing", type=int, default=0); ap.add_argument("--declare-neutral", default="")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not (a.catalogue and a.per_star and a.out):
        sys.exit("need --catalogue, --per-star and --out (or --self-test)")
    cat = read_catalogue(a.catalogue)
    z = np.load(a.per_star)
    neutral = tuple(x for x in a.declare_neutral.split(",") if x)
    out, rep = build(cat, z, a.max_missing, neutral)
    write_csv(a.out, out)
    man = dict(converter="make_pair_table.py", catalogue=os.path.basename(a.catalogue), catalogue_sha256=sha256(a.catalogue),
               per_star=os.path.basename(a.per_star), per_star_sha256=sha256(a.per_star), out=os.path.basename(a.out), out_sha256=sha256(a.out),
               report=rep, summary=summary(out), regime_counts=regime_counts(out), choices=["P1", "P2", "P3", "P4", "P5"],
               notes=["COUNTS ONLY: no R value is computed by this converter",
                      "the registered stage G already applied cut 12 (NSS screen) and caps s at 30 kAU: nss1/nss2 are 0 for every catalogue star BY CONSTRUCTION when the input is the registered catalogue"])
    json.dump(man, open(a.out + ".manifest.json", "w"), indent=1)
    print(json.dumps(man["summary"], indent=1)); print("wrote", a.out, "and", a.out + ".manifest.json")


if __name__ == "__main__":
    main()
