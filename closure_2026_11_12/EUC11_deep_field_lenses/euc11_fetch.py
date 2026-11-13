#!/usr/bin/env python3
"""EUC11 fetch: Euclid DR1 deep-field MER, photo-z and grism redshift / line rows for the Q1 lenses and their controls.

Frozen criteria: FROZEN_CRITERIA.md (commit 0a6088cd0a), sections 1 and 2.
  stage lens    : every deep MER object within 3.0 arcsec of each grade A/B Q1 lens; photo-z of those objects
  stage foot    : (amendment A1) deep MER objects within 30 arcsec of each lens, counted, to define the footprint
  stage cand    : control candidates 20-100 arcsec (amendment A2; frozen: 20-300) from each lens with a lens object, H flux within a factor 1.5,
                  spurious_prob < 0.2, point_like_prob < 0.5; six drawn per lens (seed 20261112); their photo-z;
                  up to three kept with |delta phz_median| <= 0.15
  stage ctrl    : every deep MER object within 3.0 arcsec of each control
  stage tables  : photo-z, quality, galaxy candidates (all ranks), good line rows (all ranks) and class of every
                  MER object found near a lens or a control
  stage verify  : one id chunk of the candidates table queried again and compared row for row (K4)

Public, anonymous IRSA TAP (sync), one paced request stream, through EUC3's helpers (imported, not edited).
Everything is written under <q1-dir>/deep_tables/ (outside git).  Resumable: finished chunks are skipped.

Run:  python3 -I euc11_fetch.py --q1-dir <dir with the Q1 lens csv files> [--stage lens|foot|cand|ctrl|tables|verify|all]
"""
import argparse, csv, hashlib, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC3_nisp_source_redshifts"))
import euc3_fetch as F

SEED = 20261112
MER = "euclid_dr1_mer_catalogue_deep_survey"
MER_COLS = ("m.object_id, m.ra, m.dec, m.point_like_prob, m.spurious_prob, m.kron_radius, m.flux_h_templfit, "
            "m.flux_vis_psf, m.flux_detection_total, m.vis_det, m.deblended_flag, m.parent_id, m.segmentation_area, "
            "m.semimajor_axis, m.tileid")
GOODQ = "(211, 212, 213, 251, 252, 253)"
T = dict(
    phz=("euclid_dr1_phz_photo_z_deep_survey", "t.object_id, t.phz_median, t.phz_70_int_1, t.phz_70_int_2, t.phz_classification", ""),
    qual=("euclid_dr1_spectro_z_spe_quality_deep",
          "t.object_id, t.spe_error_flag, t.spe_gal_error_flag, t.spe_grism, t.spe_w_min, t.spe_w_max, t.spe_npix, "
          "t.spe_n_dith_max, t.spe_n_dith_med, t.patch_id_list, t.calblock_id_list, t.cntr", ""),
    gal=("euclid_dr1_spectro_z_spe_galaxy_candidates_deep",
         "t.object_id, t.spe_rank, t.spe_z, t.spe_z_err, t.spe_z_prob, t.spe_z_rel, t.patch_id_list, t.calblock_id_list, t.cntr", ""),
    lines=("euclid_dr1_spectro_line_features_spe_line_features_deep",
           "t.object_id, t.spe_rank, t.spe_line_name, t.spe_line_central_wl_gf, t.spe_line_flux_gf, t.spe_line_snr_gf, "
           "t.spe_line_fwhm_gf, t.spe_line_qual_gf, t.patch_id_list, t.calblock_id_list, t.cntr",
           " AND t.spe_line_qual_gf IN %s AND t.spe_line_name IN ('Halpha', 'OIII5008', 'Hbeta', 'SII6718', 'SIII9530', "
           "'SIII9068', 'OII3727')" % GOODQ),
    cls=("euclid_dr1_spectro_z_spe_classification_deep", "t.object_id, t.spe_class", ""),
)

def sep_arcsec(ra1, de1, ra2, de2):
    d1, d2 = math.radians(de1), math.radians(de2)
    x = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin(math.radians(ra2 - ra1) / 2) ** 2
    return math.degrees(2.0 * math.asin(min(1.0, math.sqrt(x)))) * 3600.0

def lenses(q1_dir):
    rows = [r for r in csv.DictReader(open(os.path.join(q1_dir, "q1_discovery_engine_lens_catalog.csv"), encoding="utf-8")) if r["grade"].strip() in ("A", "B")]
    rows.sort(key=lambda r: r["id_str"])
    return [(i, r["id_str"], r["grade"].strip(), float(r["right_ascension"]), float(r["declination"])) for i, r in enumerate(rows)]

def cone(tdir, name, pos, chunk, radius_deg, cols=MER_COLS, extra="", fields=(("sid", "long"), ("sra", "double"), ("sdec", "double"))):
    """pos rows: (sid, ra, dec, ...extra upload columns).  One file per chunk."""
    for c0 in range(0, len(pos), chunk):
        path = os.path.join(tdir, "%s_%05d.csv" % (name, c0))
        if os.path.exists(path): continue
        up = F.votable(fields, [tuple(("%.8f" % v) if isinstance(v, float) else v for v in p) for p in pos[c0:c0 + chunk]])
        q = ("SELECT u.sid, %s FROM %s AS m, TAP_UPLOAD.up AS u WHERE CONTAINS(POINT('ICRS', m.ra, m.dec), "
             "CIRCLE('ICRS', u.sra, u.sdec, %.9f)) = 1%s" % (cols, MER, radius_deg, extra))
        h, rows, dt = F.tap(q, up)
        F.save(path, h, rows)
        print("  %s chunk %5d: %d positions -> %d rows (%.0f s)" % (name, c0, len(pos[c0:c0 + chunk]), len(rows), dt), flush=True)

def read_all(tdir, name):
    out, hdr = [], None
    for fn in sorted(os.listdir(tdir)):
        if fn.startswith(name + "_") and fn.endswith(".csv"):
            h, rows = F.load_csv(os.path.join(tdir, fn)); hdr = h; out += rows
    return hdr, out

def id_query(key, ids):
    tab, cols, extra = T[key]
    up = F.votable((("oid", "long"),), [(i,) for i in ids])
    return F.tap("SELECT %s FROM %s AS t, TAP_UPLOAD.up AS u WHERE t.object_id = u.oid%s" % (cols, tab, extra), up)

def tables(tdir, name, ids, keys, chunk):
    for key in keys:
        for c0 in range(0, len(ids), chunk):
            path = os.path.join(tdir, "%s_%s_%06d.csv" % (key, name, c0))
            if os.path.exists(path): continue
            h, rows, dt = id_query(key, ids[c0:c0 + chunk])
            F.save(path, h, rows)
            print("  %-5s %s chunk %6d: %d ids -> %d rows (%.0f s)" % (key, name, c0, len(ids[c0:c0 + chunk]), len(rows), dt), flush=True)

def lens_objects(tdir, L):
    """nearest deep MER object within 0.6 arcsec of each lens: sid -> (object_id, ra, dec, flux_h, sep)."""
    h, rows = read_all(tdir, "merL"); c = {k: i for i, k in enumerate(h)}; pos = {s[0]: (s[3], s[4]) for s in L}; best = {}
    for r in rows:
        sid = int(r[c["sid"]]); d = sep_arcsec(pos[sid][0], pos[sid][1], float(r[c["ra"]]), float(r[c["dec"]]))
        if d <= 0.6 and (sid not in best or d < best[sid][4]):
            best[sid] = (int(r[c["object_id"]]), float(r[c["ra"]]), float(r[c["dec"]]), float(r[c["flux_h_templfit"]] or "nan"), d)
    return best

def phz_of(tdir, name):
    h, rows = read_all(tdir, "phz_" + name); c = {k: i for i, k in enumerate(h)}; out = {}
    for r in rows:
        try: out[int(r[c["object_id"]])] = float(r[c["phz_median"]])
        except ValueError: pass
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--q1-dir", required=True)
    ap.add_argument("--stage", default="all", choices=("lens", "foot", "cand", "ctrl", "tables", "verify", "all"))
    ap.add_argument("--cand-chunk", type=int, default=40); ap.add_argument("--cand-covered", default="", help="amendment A3: index ranges of lens positions already fetched, e.g. 0-140,160-220"); ap.add_argument("--id-chunk", type=int, default=2000)
    a = ap.parse_args(); tdir = os.path.join(a.q1_dir, "deep_tables"); os.makedirs(tdir, exist_ok=True)
    L = lenses(a.q1_dir); print("Q1 grade A/B lens systems: %d" % len(L), flush=True)
    F.save(os.path.join(tdir, "systems_L.csv"), ["sid", "id_str", "grade", "ra", "dec"], L)

    if a.stage in ("lens", "all"):
        cone(tdir, "merL", [(s[0], s[3], s[4]) for s in L], 600, 3.0 / 3600.0)
        h, rows = read_all(tdir, "merL"); ids = sorted({int(r[h.index("object_id")]) for r in rows})
        tables(tdir, "L", ids, ("phz",), a.id_chunk)
    if a.stage in ("foot", "all"):
        # amendment A1: footprint = at least 5 deep MER objects within 30 arcsec (plain cone query, counted here)
        cone(tdir, "foot", [(s[0], s[3], s[4]) for s in L], 30, 30.0 / 3600.0, cols="m.object_id")
        h, rows = read_all(tdir, "foot"); n = {}
        for r in rows: n[int(r[0])] = n.get(int(r[0]), 0) + 1
        F.save(os.path.join(tdir, "footprint_counts.csv"), ["sid", "n_within_30arcsec"], [(s[0], n.get(s[0], 0)) for s in L])
        print("lenses with >= 5 deep MER objects within 30 arcsec: %d of %d (1-4 objects: %d)"
              % (sum(1 for s in L if n.get(s[0], 0) >= 5), len(L), sum(1 for s in L if 0 < n.get(s[0], 0) < 5)), flush=True)
    lo = lens_objects(tdir, L); pzL = phz_of(tdir, "L")
    print("lenses with a lens object within 0.6 arcsec: %d of %d; of those with a photo-z and an H flux: %d"
          % (len(lo), len(L), sum(1 for s, v in lo.items() if v[0] in pzL and pzL[v[0]] > 0 and v[3] > 0)), flush=True)

    if a.stage in ("cand", "all"):
        pos = [(sid, v[1], v[2], v[3] / 1.5, v[3] * 1.5) for sid, v in sorted(lo.items()) if v[3] > 0 and v[0] in pzL and pzL[v[0]] > 0]
        if a.cand_covered:
            # amendment A3: no further candidate requests; use the chunks on disk and record which lens positions they cover
            cov = [pos[i][0] for r0, r1 in (tuple(int(x) for x in rng_.split("-")) for rng_ in a.cand_covered.split(",")) for i in range(r0, min(r1, len(pos)))]
            F.save(os.path.join(tdir, "covered_lenses.csv"), ["sid"], [(c,) for c in cov])
            print("amendment A3: control candidates on disk cover %d of %d lens positions" % (len(cov), len(pos)), flush=True)
            pos = []
        cone(tdir, "cand", pos, a.cand_chunk, 100.0 / 3600.0,                      # amendment A2: 100 arcsec, not 300
             cols="m.object_id, m.ra, m.dec, m.flux_h_templfit, m.point_like_prob, m.spurious_prob",
             extra=" AND m.flux_h_templfit > u.flo AND m.flux_h_templfit < u.fhi AND m.spurious_prob < 0.2 AND m.point_like_prob < 0.5",
             fields=(("sid", "long"), ("sra", "double"), ("sdec", "double"), ("flo", "double"), ("fhi", "double")))
        h, rows = read_all(tdir, "cand"); c = {k: i for i, k in enumerate(h)}; per = {}
        for r in rows:
            sid = int(r[c["sid"]]); d = sep_arcsec(lo[sid][1], lo[sid][2], float(r[c["ra"]]), float(r[c["dec"]]))
            if a.cand_covered and sid not in set(cov): continue
            if 20.0 <= d <= 100.0: per.setdefault(sid, []).append((int(r[c["object_id"]]), float(r[c["ra"]]), float(r[c["dec"]]), float(r[c["flux_h_templfit"]])))
        rng = np.random.default_rng(SEED); draw = []
        for sid in sorted(per):
            cands = sorted(set(per[sid])); k = min(6, len(cands))
            for j, i in enumerate(rng.choice(len(cands), size=k, replace=False)): draw.append((sid, j) + cands[int(i)])
        F.save(os.path.join(tdir, "controls_drawn.csv"), ["sid", "draw", "object_id", "ra", "dec", "flux_h_templfit"], draw)
        print("control candidates in the annulus: %d for %d lenses (median %d per lens); drawn %d"
              % (sum(len(v) for v in per.values()), len(per), int(np.median([len(v) for v in per.values()])) if per else 0, len(draw)), flush=True)
        tables(tdir, "D", sorted({d[2] for d in draw}), ("phz",), a.id_chunk)
        pzD = phz_of(tdir, "D"); kept = []; n = {}
        for d in draw:
            sid = d[0]; z = pzD.get(d[2], float("nan"))
            if n.get(sid, 0) < 3 and z > 0 and abs(z - pzL[lo[sid][0]]) <= 0.15:
                kept.append((len(kept), sid, d[2], d[3], d[4], d[5], z)); n[sid] = n.get(sid, 0) + 1
        F.save(os.path.join(tdir, "systems_C.csv"), ["cid", "sid", "object_id", "ra", "dec", "flux_h_templfit", "phz_median"], kept)
        print("controls kept: %d for %d lenses" % (len(kept), len(n)), flush=True)

    if a.stage in ("ctrl", "all"):
        h, C = F.load_csv(os.path.join(tdir, "systems_C.csv"))
        cone(tdir, "merC", [(int(r[0]), float(r[3]), float(r[4])) for r in C], 600, 3.0 / 3600.0)

    ids = sorted({int(r[h.index("object_id")]) for nm in ("merL", "merC") for h, rows in [read_all(tdir, nm)] if h for r in rows})
    print("MER objects within 3.0 arcsec of a lens or a control: %d" % len(ids), flush=True)
    if a.stage in ("tables", "all"):
        json.dump(dict(n_ids=len(ids), sha=hashlib.sha256(",".join(map(str, ids)).encode()).hexdigest()), open(os.path.join(tdir, "ids_manifest.json"), "w"))
        tables(tdir, "all", ids, ("qual", "gal", "lines", "phz", "cls"), a.id_chunk)
    if a.stage in ("verify", "all"):
        h0, r0 = F.load_csv(os.path.join(tdir, "gal_all_%06d.csv" % 0))
        h, rows, dt = id_query("gal", ids[:a.id_chunk]); same = (h == h0) and sorted(map(tuple, rows)) == sorted(map(tuple, r0))
        json.dump(dict(rows_cached=len(r0), rows_again=len(rows), identical=bool(same)), open(os.path.join(tdir, "verify.json"), "w"))
        print("  verify gal chunk 0: cached %d rows, again %d rows -> %s (%.0f s)" % (len(r0), len(rows), "identical" if same else "DIFFERENT", dt), flush=True)
    print("fetch done (stage %s)" % a.stage, flush=True)

if __name__ == "__main__":
    main()
