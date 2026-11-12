#!/usr/bin/env python3
"""EUC3 fetch: Euclid DR1 MER, photo-z and red-grism redshift / line rows at the positions of ECLIPSE systems.

Frozen criteria: FROZEN_CRITERIA.md (commit bf72d787a8), sections 1 and 2.
  systems = every grade A/B key-catalogue row with an effective Einstein radius > 0, and every grade X object row
  part  first : EUC1's sample S, EUC2's three truth lenses and the grade X systems (everything the gates and the
                P and S readings need); part rest: the remaining grade A/B systems (the not-quality-cut set U)
  stage mer   : every MER object within 3.0 arcsec of each system position (the rule's aperture r_a <= 3.0 arcsec
                is applied by euc3.py, not here)
  stage tables: for every such MER object id, its rows in the photo-z, quality, galaxy-candidates (all ranks),
                line-features (rank 0, listed lines) and classification tables
  stage verify: three fixed id chunks of the candidates table are queried again and compared row for row (K5)

Public, anonymous IRSA TAP (sync).  One request stream, paced; positions and ids go up as a TAP_UPLOAD table.
Everything is written under <data-dir>/nisp_tables/ (outside git).  Resumable: finished chunks are skipped.

The service ends a synchronous job after about five minutes: 1,000 positions take about 220 s, 2,000 time out, so
positions go up 800 at a time.

Run:  python3 -I euc3_fetch.py --data-dir <dir with the two ECLIPSE csv files> --part first|rest [--stage mer|tables|verify|all]
"""
import argparse, csv, hashlib, io, json, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E

TAP = "https://irsa.ipac.caltech.edu/TAP/sync"
UA = {"User-Agent": "generic-client"}
PACE = 2.0
CONE_DEG = 3.0 / 3600.0
MER = "euclid_dr1_mer_catalogue_wide_survey"
T = dict(
    phz=("euclid_dr1_phz_photo_z_wide",
         "t.object_id, t.phz_median, t.phz_70_int_1, t.phz_70_int_2, t.phz_90_int_1, t.phz_90_int_2, t.phz_95_int_1, "
         "t.phz_95_int_2, t.phz_classification", ""),
    qual=("euclid_dr1_spectro_z_spe_quality_wide_survey",
          "t.object_id, t.spe_error_flag, t.spe_warning_flag, t.spe_gal_error_flag, t.spe_gal_warning_flag, t.spe_grism, "
          "t.spe_w_min, t.spe_w_max, t.spe_npix, t.spe_n_dith_max, t.spe_n_dith_med, t.spe_lsf_red, t.patch_id_list, "
          "t.calblock_id_list, t.cntr", ""),
    gal=("euclid_dr1_spectro_z_spe_galaxy_candidates_wide_survey",
         "t.object_id, t.spe_rank, t.spe_z, t.spe_z_err, t.spe_z_prob, t.spe_z_rel, t.spe_z_reduced_chi2, t.spe_subclass, "
         "t.spe_cont_snr, t.basic_download_data_oid, t.patch_id_list, t.calblock_id_list, t.cntr", ""),
    lines=("euclid_dr1_spectro_line_features_spe_line_features_wide_survey",
           "t.object_id, t.spe_rank, t.spe_line_name, t.spe_line_flag, t.spe_line_n_dith, t.spe_line_central_wl_gf, "
           "t.spe_line_flux_gf, t.spe_line_flux_err_gf, t.spe_line_snr_gf, t.spe_line_fwhm_gf, t.spe_line_qual_gf, "
           "t.spe_line_ew_gf, t.spe_line_flux_di, t.spe_line_snr_di, t.spe_line_qual_di, t.spe_line_aon, "
           "t.basic_download_data_oid, t.patch_id_list, t.calblock_id_list, t.cntr",
           " AND t.spe_rank = 0 AND t.spe_line_name IN ('Halpha', 'NII6585', 'SII6718', 'OIII5008', 'Hbeta', 'SIII9530', "
           "'SIII9068', 'OII3727', 'PaBeta', 'PaGamma')"),
    cls=("euclid_dr1_spectro_z_spe_classification_wide_survey",
         "t.object_id, t.spe_class, t.spe_gal_prob, t.spe_qso_prob, t.spe_star_prob", ""),
)
MER_COLS = ("m.object_id, m.ra, m.dec, m.point_like_prob, m.spurious_prob, m.kron_radius, m.flux_h_templfit, "
            "m.flux_vis_psf, m.flux_detection_total, m.vis_det, m.deblended_flag, m.parent_id, m.segmentation_area, "
            "m.semimajor_axis, m.tileid")

def votable(fields, rows):
    s = io.StringIO()
    s.write('<?xml version="1.0"?>\n<VOTABLE version="1.3" xmlns="http://www.ivoa.net/xml/VOTable/v1.3">\n<RESOURCE><TABLE>\n')
    for nm, dt in fields: s.write('<FIELD name="%s" datatype="%s"/>\n' % (nm, dt))
    s.write("<DATA><TABLEDATA>\n")
    for r in rows: s.write("<TR>" + "".join("<TD>%s</TD>" % v for v in r) + "</TR>\n")
    s.write("</TABLEDATA></DATA>\n</TABLE></RESOURCE>\n</VOTABLE>\n")
    return s.getvalue().encode()

def tap(query, upload=None, tries=6, timeout=900):
    """One paced request.  Returns (header, rows).  A non-CSV answer (a service error) is retried, then raised."""
    err = "?"
    for k in range(tries):
        time.sleep(PACE)
        try:
            t0 = time.time()
            if upload is None:
                r = requests.post(TAP, data=dict(QUERY=query, FORMAT="CSV"), headers=UA, timeout=timeout)
            else:
                r = requests.post(TAP, data=dict(QUERY=query, FORMAT="CSV", UPLOAD="up,param:tbl"),
                                  files=dict(tbl=("up.xml", upload, "application/x-votable+xml")), headers=UA, timeout=timeout)
            txt = r.text
            if r.status_code == 200 and not txt.lstrip().startswith("<"):
                rows = list(csv.reader(io.StringIO(txt)))
                return (rows[0] if rows else []), [x for x in rows[1:] if x], time.time() - t0
            err = "HTTP %d: %s" % (r.status_code, " ".join(txt.split())[:300])
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", 120) or 120)
                print("  429 from the service: waiting %.0f s" % wait, flush=True); time.sleep(min(wait, 900.0)); continue
        except Exception as ex:
            err = type(ex).__name__
        print("  request failed (%s); retry %d" % (err, k + 1), flush=True)
        time.sleep(20.0 * (k + 1))
    raise RuntimeError("request failed: %s" % err)

def save(path, header, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    os.replace(tmp, path)

def load_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]

TRUTH = ("EUCL-DR1-L015763", "EUCL-DR1-L012826", "EUCL-DR1-L014688")

def systems(data_dir):
    """Every grade A/B key row with theta_E > 0 and every grade X object row: (index, identifier, grade, ra, dec, part).
    Part 'first' = sample S, the truth lenses and grade X; part 'rest' = the other grade A/B systems."""
    rows, _ = E.load(data_dir)
    first = {r["id"] for r in E.select(rows, ("A", "B"))[0]} | set(TRUTH)
    obj = {}
    with open(os.path.join(data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): obj[r["Unique_Identifier"]] = r
    out = []
    for r in rows:
        if r["tE"] > 0: out.append((r["id"], r["grade"], float(obj[r["id"]]["RA_obj"]), float(obj[r["id"]]["DEC_obj"])))
    for lid, o in obj.items():
        if o["Expert_Grade"].strip() == "X": out.append((lid, "X", float(o["RA_obj"]), float(o["DEC_obj"])))
    out = sorted(o + ("first" if (o[1] == "X" or o[0] in first) else "rest",) for o in out)
    out.sort(key=lambda o: (o[4] != "first", o[0]))
    return [(i,) + s for i, s in enumerate(out)]

def stage_mer(tdir, sysl, chunk, part):
    for c0 in range(0, len(sysl), chunk):
        path = os.path.join(tdir, "mer_%s_%05d.csv" % (part, c0))
        if os.path.exists(path): continue
        blk = sysl[c0:c0 + chunk]
        up = votable((("sid", "long"), ("sra", "double"), ("sdec", "double")), [(s[0], "%.8f" % s[3], "%.8f" % s[4]) for s in blk])
        q = ("SELECT u.sid, %s FROM %s AS m, TAP_UPLOAD.up AS u WHERE CONTAINS(POINT('ICRS', m.ra, m.dec), "
             "CIRCLE('ICRS', u.sra, u.sdec, %.9f)) = 1" % (MER_COLS, MER, CONE_DEG))
        h, rows, dt = tap(q, up)
        save(path, h, rows)
        print("  mer chunk %5d: %d systems -> %d MER rows (%.0f s)" % (c0, len(blk), len(rows), dt), flush=True)

def mer_ids(tdir, part):
    ids = set()
    for fn in sorted(os.listdir(tdir)):
        if fn.startswith("mer_%s_" % part) and fn.endswith(".csv"):
            h, rows = load_csv(os.path.join(tdir, fn)); j = h.index("object_id")
            ids.update(int(r[j]) for r in rows)
    return sorted(ids)

def id_query(key, ids):
    tab, cols, extra = T[key]
    up = votable((("oid", "long"),), [(i,) for i in ids])
    return tap("SELECT %s FROM %s AS t, TAP_UPLOAD.up AS u WHERE t.object_id = u.oid%s" % (cols, tab, extra), up)

def stage_tables(tdir, ids, chunk, part):
    json.dump(dict(n_ids=len(ids), chunk=chunk, sha=hashlib.sha256(",".join(map(str, ids)).encode()).hexdigest()),
              open(os.path.join(tdir, "ids_manifest_%s.json" % part), "w"))
    for key in ("qual", "gal", "lines", "phz", "cls"):
        for c0 in range(0, len(ids), chunk):
            path = os.path.join(tdir, "%s_%s_%06d.csv" % (key, part, c0))
            if os.path.exists(path): continue
            h, rows, dt = id_query(key, ids[c0:c0 + chunk])
            save(path, h, rows)
            print("  %-5s chunk %6d: %d ids -> %d rows (%.0f s)" % (key, c0, len(ids[c0:c0 + chunk]), len(rows), dt), flush=True)

def stage_verify(tdir, ids, chunk, part):
    starts = list(range(0, len(ids), chunk)); pick = sorted({starts[0], starts[len(starts) // 2], starts[-1]})
    out = []
    for c0 in pick:
        h0, r0 = load_csv(os.path.join(tdir, "gal_%s_%06d.csv" % (part, c0)))
        h, rows, dt = id_query("gal", ids[c0:c0 + chunk])
        same = (h == h0) and sorted(map(tuple, rows)) == sorted(map(tuple, r0))
        out.append(dict(chunk=c0, rows_cached=len(r0), rows_again=len(rows), identical=bool(same)))
        print("  verify gal chunk %6d: cached %d rows, again %d rows -> %s (%.0f s)" % (c0, len(r0), len(rows), "identical" if same else "DIFFERENT", dt), flush=True)
    json.dump(out, open(os.path.join(tdir, "verify_%s.json" % part), "w"), indent=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--part", required=True, choices=("first", "rest"))
    ap.add_argument("--stage", default="all", choices=("mer", "tables", "verify", "all"))
    ap.add_argument("--sys-chunk", type=int, default=800)
    ap.add_argument("--id-chunk", type=int, default=2000)
    a = ap.parse_args()
    tdir = os.path.join(a.data_dir, "nisp_tables"); os.makedirs(tdir, exist_ok=True)
    allsys = systems(a.data_dir)
    save(os.path.join(tdir, "systems.csv"), ["sid", "unique_identifier", "grade", "ra", "dec", "part"], allsys)
    sysl = [s for s in allsys if s[5] == a.part]
    print("systems: %d (grade A/B with theta_E > 0: %d, grade X: %d); part %s: %d"
          % (len(allsys), sum(s[2] != "X" for s in allsys), sum(s[2] == "X" for s in allsys), a.part, len(sysl)), flush=True)
    if a.stage in ("mer", "all"): stage_mer(tdir, sysl, a.sys_chunk, a.part)
    ids = mer_ids(tdir, a.part)
    if a.part == "rest":
        done = set(mer_ids(tdir, "first")); ids = [i for i in ids if i not in done]
    print("MER objects within 3.0 arcsec of a system of part %s (not already fetched): %d" % (a.part, len(ids)), flush=True)
    if a.stage in ("tables", "all"): stage_tables(tdir, ids, a.id_chunk, a.part)
    if a.stage in ("verify", "all"): stage_verify(tdir, ids, a.id_chunk, a.part)
    print("fetch done (part %s)" % a.part, flush=True)

if __name__ == "__main__":
    main()
