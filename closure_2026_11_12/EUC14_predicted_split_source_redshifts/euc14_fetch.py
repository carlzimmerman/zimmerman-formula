#!/usr/bin/env python3
"""EUC14 fetch: the inputs a predicted split needs, and the field calibrators that validate them.

  stage pa      : ESA Euclid archive TAP, dr1.raw_frame: position angle `pa` (and centre, time, observation) of every
                  NISP spectroscopic frame whose pointing id occurs in the dither cache (EUC9's nisp_spectra_dith/).
  stage calsel  : field calibrator pairs from ESA TAP (dr1 wide-survey grism quality, galaxy candidates and line
                  tables, MER positions, spectra_source): an object A with an extracted spectrum and a neighbour B within
                  0.8 to 2.5 arcsec whose own spectrum carries a strong, single-solution H-alpha line.  No object within
                  30 arcsec of any ECLIPSE system (lens of any grade or grade X) is used.
  stage calspec : the co-added and dither spectra of each calibrator A, by byte range from the tile file at IRSA (route
                  of EUC9 amendment A0), with a smaller probe window than EUC9's fetch.

Public, anonymous, one paced stream per host, generic client name.  Everything goes under <data-dir>/euc14/ (outside git).

Run:  python3 -I euc14_fetch.py --data-dir <dir with the ECLIPSE csv files and nisp_spectra_dith/> --stage pa|calsel|calspec
"""
import argparse, csv, io, json, math, os, sys, time
import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC9_grism_spectra_source_redshifts"))
import euc9_fetch as F9                                            # imported, not edited

ESA = "https://eas.esac.esa.int/tap-server/tap/sync"
UA = {"User-Agent": "generic-client"}
PACE_ESA = 2.0

def esa(query, tries=5, timeout=600):
    err = "?"
    for k in range(tries):
        time.sleep(PACE_ESA)
        try:
            r = requests.post(ESA, data=dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=query), headers=UA, timeout=timeout)
            if r.status_code == 200 and not r.text.lstrip().startswith("<"):
                return list(csv.DictReader(io.StringIO(r.text)))
            err = "HTTP %d: %s" % (r.status_code, r.text[:200].replace("\n", " "))
        except Exception as ex:
            err = type(ex).__name__
        print("  ESA query failed (%s); retry %d" % (err, k + 1), flush=True); time.sleep(15.0 * (k + 1))
    raise RuntimeError("ESA query failed: " + err)

def write(path, rows, cols):
    with open(path + ".tmp", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    os.replace(path + ".tmp", path)

# ------------------------------------------------------------------ stage pa
PA_COLS = ["pointing_id", "observation_id", "grism_wheel_pos", "ra", "dec", "pa", "obs_time_mjd", "dither_observation", "stc_s"]

def stage_pa(data_dir, odir):
    sdir = os.path.join(data_dir, "nisp_spectra_dith")
    ptg = set()
    for fn in os.listdir(sdir):
        if fn.endswith(".npz"): ptg.update(int(x) for x in np.load(os.path.join(sdir, fn))["dptg"])
    lo, hi, step = min(ptg), max(ptg), 4000
    rows = []
    for a in range(lo - lo % step, hi + 1, step):
        q = ("SELECT %s FROM dr1.raw_frame WHERE instrument_name = 'NISP' AND technique = 'SPECTROIMAGE' AND pointing_id >= %d AND pointing_id < %d"
             % (", ".join(PA_COLS), a, a + step))
        got = esa(q); rows.extend(got); print("  pa: pointings %6d to %6d -> %d frames" % (a, a + step, len(got)), flush=True)
    write(os.path.join(odir, "pa_table.csv"), rows, PA_COLS)
    have = {int(r["pointing_id"]) for r in rows}
    print("pa stage: %d frames; pointings in the dither cache %d, with a frame %d" % (len(rows), len(ptg), len(ptg & have)), flush=True)

# ------------------------------------------------------------------ stage calsel
CAL_SEED, CAL_BOXES, CAL_SIDE = 20261112, 24, 0.25       # boxes of 0.25 x 0.25 deg (true angle) on random NISP pointings
B_SNR, B_FLUX, B_QUAL, B_FWHM = 8.0, 3.0e-16, ("212", "252"), 60.0
SEP_LO, SEP_HI, A_NDITH = 0.8, 2.5, 4
AVOID = 30.0                                              # arcsec from any ECLIPSE system (any grade, grade X included)
N_CAL = 160

def eclipse_positions(data_dir):
    pos = []
    with open(os.path.join(data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): pos.append((float(r["RA_obj"]), float(r["DEC_obj"])))
    with open(os.path.join(data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): pos.append((float(r["ra"]), float(r["dec"])))
    return np.array(pos)

def sep_arcsec(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    s = np.sin((de2 - de1) / 2) ** 2 + np.cos(de1) * np.cos(de2) * np.sin((ra2 - ra1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(s, 0, 1)))) * 3600.0

def stage_calsel(data_dir, odir):
    pa = list(csv.DictReader(open(os.path.join(odir, "pa_table.csv"))))
    cen = sorted({(round(float(r["ra"]), 3), round(float(r["dec"]), 3)) for r in pa if r["grism_wheel_pos"] in ("RGS000", "RGS180")})
    rng = np.random.default_rng(CAL_SEED); ecl = eclipse_positions(data_dir)
    boxes = []
    for j in rng.permutation(len(cen)):
        ra, de = cen[j]
        if abs(de) > 80: continue
        if any(sep_arcsec(ra, de, b[0], b[1])[()] < 3600.0 * 2 * CAL_SIDE for b in boxes): continue
        boxes.append((ra, de))
        if len(boxes) == CAL_BOXES: break
    srcs, ems = [], []
    if os.path.exists(os.path.join(odir, "cal_sources.csv")) and os.path.exists(os.path.join(odir, "cal_emitters.csv")):   # queried already
        srcs = list(csv.DictReader(open(os.path.join(odir, "cal_sources.csv")))); ems = list(csv.DictReader(open(os.path.join(odir, "cal_emitters.csv"))))
        boxes = []
    for k, (ra, de) in enumerate(boxes):
        dra = CAL_SIDE / 2 / math.cos(math.radians(de)); dde = CAL_SIDE / 2
        w = "s.ra_obj BETWEEN %.6f AND %.6f AND s.dec_obj BETWEEN %.6f AND %.6f" % (ra - dra, ra + dra, de - dde, de + dde)
        s = esa("SELECT s.source_id, s.ra_obj, s.dec_obj, s.file_name, s.hdu_index, s.dith_num FROM dr1.spectra_source_wide AS s WHERE " + w)
        e = esa("SELECT s.source_id, l.spe_line_central_wl_gf, l.spe_line_snr_gf, l.spe_line_flux_gf, l.spe_line_qual_gf, l.spe_line_fwhm_gf "
                "FROM dr1.spectra_source_wide AS s JOIN dr1.spectro_line_features_spe_line_features_wide_survey AS l ON l.object_id = s.source_id "
                "WHERE " + w + " AND l.spe_rank = 0 AND l.spe_line_name = 'Halpha' AND l.spe_line_snr_gf >= 5")
        for r in s: r["box"] = k
        srcs.extend(s); ems.extend(e)
        print("  box %2d at %.3f %+.3f: %d spectra, %d rank-0 H-alpha rows with S/N >= 5" % (k, ra, de, len(s), len(e)), flush=True)
    write(os.path.join(odir, "cal_sources.csv"), srcs, ["box", "source_id", "ra_obj", "dec_obj", "file_name", "hdu_index", "dith_num"])
    write(os.path.join(odir, "cal_emitters.csv"), ems, ["source_id", "spe_line_central_wl_gf", "spe_line_snr_gf", "spe_line_flux_gf", "spe_line_qual_gf", "spe_line_fwhm_gf"])
    # pairs: B a strong compact emitter, A another spectrum 0.8 to 2.5 arcsec away, neither near ECLIPSE
    em = {}
    for r in ems: em.setdefault(int(r["source_id"]), r)
    pos = {}
    for r in srcs: pos.setdefault(int(r["source_id"]), r)
    ids = np.array(sorted(pos)); ra = np.array([float(pos[i]["ra_obj"]) for i in ids]); de = np.array([float(pos[i]["dec_obj"]) for i in ids])
    pairs = []
    for b, r in em.items():
        if b not in pos: continue
        if not (float(r["spe_line_snr_gf"]) >= B_SNR and float(r["spe_line_flux_gf"]) >= B_FLUX and r["spe_line_qual_gf"] in B_QUAL
                and 0 < float(r["spe_line_fwhm_gf"]) <= B_FWHM): continue
        rb, db = float(pos[b]["ra_obj"]), float(pos[b]["dec_obj"])
        near = np.where(np.abs(de - db) < SEP_HI / 3600.0 * 1.2)[0]
        for j in near:
            a = int(ids[j])
            if a == b: continue
            s = float(sep_arcsec(rb, db, ra[j], de[j]))
            if not (SEP_LO <= s <= SEP_HI) or int(pos[a]["dith_num"]) < A_NDITH: continue
            if a in em and abs(float(em[a]["spe_line_central_wl_gf"]) - float(r["spe_line_central_wl_gf"])) < 200.0: continue
            if np.min(sep_arcsec(ra[j], de[j], ecl[:, 0], ecl[:, 1])) < AVOID: continue
            pairs.append(dict(a_id=a, b_id=b, sep=s, a_ra=ra[j], a_dec=de[j], b_ra=rb, b_dec=db, lam_b=float(r["spe_line_central_wl_gf"]),
                              snr_b=float(r["spe_line_snr_gf"]), flux_b=float(r["spe_line_flux_gf"]), fwhm_b=float(r["spe_line_fwhm_gf"]),
                              file_name=pos[a]["file_name"], hdu_index=int(pos[a]["hdu_index"]), dith_num=int(pos[a]["dith_num"]), box=pos[a]["box"]))
    # one pair per A (the strongest B); order by B's line S/N; keep the first N_CAL
    best = {}
    for p in pairs:
        if p["a_id"] not in best or p["snr_b"] > best[p["a_id"]]["snr_b"]: best[p["a_id"]] = p
    sel = sorted(best.values(), key=lambda p: -p["snr_b"])[:N_CAL]
    write(os.path.join(odir, "cal_pairs.csv"), sel, list(sel[0].keys()) if sel else ["a_id"])
    print("calsel: %d boxes queried now, %d spectra, %d emitters (S/N >= 5); pairs %d, distinct A %d, kept %d" % (len(boxes), len(srcs), len(em), len(pairs), len(best), len(sel)), flush=True)

# ------------------------------------------------------------------ stage calalign: pairs lying along a focal-plane axis
# Written after the first 72 calibrators of cal_pairs.csv showed B's line only where B lies almost exactly along the
# dispersion (the extraction is narrow across it).  Both focal-plane axes (pa and pa + 90) are accepted, so the four
# conventions stay on an equal footing.
AL_SNR, AL_FLUX, AL_CROSS = 6.0, 2.0e-16, 0.35

def stage_calalign(data_dir, odir):
    sys.path.insert(0, HERE)
    import euc14_core as C
    from matplotlib.path import Path
    fr = [r for r in csv.DictReader(open(os.path.join(odir, "pa_table.csv"))) if r["grism_wheel_pos"] in ("RGS000", "RGS180") and r["stc_s"]]
    FRA = np.array([float(r["ra"]) for r in fr]); FDE = np.array([float(r["dec"]) for r in fr]); FPA = np.array([float(r["pa"]) for r in fr])
    POLY = [[float(x) for x in r["stc_s"].replace('"', "").split()[2:]] for r in fr]
    def frames_pa(ra, de):
        d = np.hypot((FRA - ra) * math.cos(math.radians(de)), FDE - de); out = []
        for j in np.where(d < 0.6)[0]:
            p = POLY[j]; v = [C.tangent(p[2 * i], p[2 * i + 1], ra, de) for i in range(len(p) // 2)]
            if Path(v).contains_point((0.0, 0.0)): out.append(FPA[j])
        return out
    srcs = list(csv.DictReader(open(os.path.join(odir, "cal_sources.csv")))); ems = list(csv.DictReader(open(os.path.join(odir, "cal_emitters.csv"))))
    ecl = eclipse_positions(data_dir)
    em = {}
    for r in ems: em.setdefault(int(r["source_id"]), r)
    pos = {}
    for r in srcs: pos.setdefault(int(r["source_id"]), r)
    ids = np.array(sorted(pos)); ra = np.array([float(pos[i]["ra_obj"]) for i in ids]); de = np.array([float(pos[i]["dec_obj"]) for i in ids])
    first = {int(p["a_id"]) for p in csv.DictReader(open(os.path.join(odir, "cal_pairs.csv")))}
    best = {}
    for b, r in em.items():
        if b not in pos: continue
        if not (float(r["spe_line_snr_gf"]) >= AL_SNR and float(r["spe_line_flux_gf"]) >= AL_FLUX and r["spe_line_qual_gf"] in B_QUAL
                and 0 < float(r["spe_line_fwhm_gf"]) <= B_FWHM): continue
        rb, db = float(pos[b]["ra_obj"]), float(pos[b]["dec_obj"])
        for j in np.where(np.abs(de - db) < SEP_HI / 3600.0 * 1.2)[0]:
            a = int(ids[j])
            if a == b or a in first: continue
            s = float(sep_arcsec(rb, db, ra[j], de[j]))
            if not (SEP_LO <= s <= SEP_HI) or int(pos[a]["dith_num"]) < A_NDITH: continue
            if a in em and abs(float(em[a]["spe_line_central_wl_gf"]) - float(r["spe_line_central_wl_gf"])) < 200.0: continue
            if np.min(sep_arcsec(ra[j], de[j], ecl[:, 0], ecl[:, 1])) < AVOID: continue
            pas = frames_pa(ra[j], de[j])
            if not pas: continue
            pa = float(np.median(pas)); off = np.array([(rb - ra[j]) * math.cos(math.radians(db)) * 3600.0, (db - de[j]) * 3600.0])
            phi = math.degrees(math.atan2(off[0], off[1]))
            cross = min(abs(s * math.sin(math.radians(phi - pa))), abs(s * math.cos(math.radians(phi - pa))))
            if cross > AL_CROSS: continue
            p = dict(a_id=a, b_id=b, sep=s, a_ra=ra[j], a_dec=de[j], b_ra=rb, b_dec=db, lam_b=float(r["spe_line_central_wl_gf"]),
                     snr_b=float(r["spe_line_snr_gf"]), flux_b=float(r["spe_line_flux_gf"]), fwhm_b=float(r["spe_line_fwhm_gf"]),
                     file_name=pos[a]["file_name"], hdu_index=int(pos[a]["hdu_index"]), dith_num=int(pos[a]["dith_num"]), box=pos[a]["box"],
                     cross=cross, axis_pa=pa, n_frames=len(pas))
            if a not in best or p["snr_b"] > best[a]["snr_b"]: best[a] = p
    sel = sorted(best.values(), key=lambda p: -p["snr_b"])
    write(os.path.join(odir, "cal_pairs_aligned.csv"), sel, list(sel[0].keys()) if sel else ["a_id"])
    print("calalign: %d aligned pairs (cross offset <= %.2f arcsec to either focal-plane axis; B line S/N >= %.0f, flux >= %.1e)"
          % (len(sel), AL_CROSS, AL_SNR, AL_FLUX), flush=True)

# ------------------------------------------------------------------ stage calspec (IRSA tile files by byte range)
BYTES = [0]
PACE_IBE, BACKOFF, MAX_BACKOFFS = 1.0, 150.0, 3        # one stream, at most one request a second; >= 2 min after any 429 / 5xx

def polite_range(path, a, b, tries=None):
    """EUC9's byte-range request, paced at one a second; on 429 or 5xx (or a network error) wait 150 s, at most three
    times, then stop the stage (resume later; the fetch skips what is cached)"""
    url = F9.HOST.get("base", F9.FILES) + path
    for k in range(MAX_BACKOFFS + 1):
        time.sleep(PACE_IBE)
        try:
            r = F9.SES.get(url, headers=dict(UA, Range="bytes=%d-%d" % (a, b)), timeout=120)
            code = r.status_code
        except Exception as ex:
            code = type(ex).__name__
        if code == 206:
            if "base" not in F9.HOST and r.url != url: F9.HOST["base"] = r.url[:len(r.url) - len(path)]
            BYTES[0] += len(r.content); return r.content
        if code == 416: return None
        if k == MAX_BACKOFFS: break
        print("  IBE answered %s; waiting %.0f s" % (code, BACKOFF), flush=True); time.sleep(BACKOFF)
    raise SystemExit("IBE errors persist: stage stopped; resume later")
F9.get_range = polite_range                                          # replaces EUC9's faster retry loop for this lane

HDRS = []
def parse_object_ext(buf):
    """EUC9's parse_object plus each dither's contamination table and, for the first objects, every header card"""
    import warnings
    from astropy.io import fits
    o = F9_parse(buf)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        hl = fits.open(io.BytesIO(F9.PRIMARY + buf), memmap=False, ignore_missing_end=True, lazy_load_hdus=False)
        cont, seen_meta, hd = [], 0, []
        for h in hl[1:]:
            nm = h.header.get("EXTNAME", "")
            if nm.endswith("_META"):
                seen_meta += 1
                if seen_meta > 1: break
            if len(HDRS) < 3: hd.append(dict(extname=nm, cards=[str(c) for c in h.header.cards]))
            if "_DITH1D_" in nm and not nm.endswith("_SIGNAL") and h.data is not None:
                try: cont.append(np.array(h.data[h.data.columns.names[0]], np.float32))
                except Exception: cont.append(np.full(F9.BLOCK // 4, np.nan, np.float32))
        hl.close()
    if len(HDRS) < 3 and hd: HDRS.append(hd)
    o["DC"] = cont
    return o
F9_parse = F9.parse_object
F9.parse_object = parse_object_ext

def tile_path(fn):
    tile = fn.split("COMBSPEC_")[1].split("_")[0]
    return "euclid/dr1/SIR_COMBINED_SPECTRA/%s/%s" % (tile, fn)

def manifest(odir):
    """sha256 of every file this lane fetched (outside git)"""
    import hashlib
    m = {}
    for root in (odir, os.path.join(odir, "cal_spectra")):
        if not os.path.isdir(root): continue
        for fn in sorted(os.listdir(root)):
            fp = os.path.join(root, fn)
            if os.path.isfile(fp) and fn != "manifest.json":
                m[os.path.relpath(fp, odir)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    json.dump(m, open(os.path.join(odir, "manifest.json"), "w"), indent=0, sort_keys=True)
    print("manifest: %d files hashed" % len(m), flush=True)

def stage_calspec(odir, limit_mb=180.0):
    cdir = os.path.join(odir, "cal_spectra"); os.makedirs(cdir, exist_ok=True)
    pairs = list(csv.DictReader(open(os.path.join(odir, "cal_pairs_aligned.csv"))))      # the first list is not fetched further
    logp = os.path.join(cdir, "fetch_log.json"); log = json.load(open(logp)) if os.path.exists(logp) else {}
    try:
        _calspec_loop(pairs, cdir, log, logp)
    finally:
        json.dump(log, open(logp, "w"))
    if HDRS: json.dump(HDRS, open(os.path.join(cdir, "headers_first_objects.json"), "w"), indent=0)
    print("calspec: aligned list %d cached, %d failed, %.1f MB transferred this run" % (sum(os.path.exists(os.path.join(cdir, "%s.npz" % p["a_id"])) for p in pairs), len(log), BYTES[0] / 1e6), flush=True)
    manifest(odir)

def _calspec_loop(pairs, cdir, log, logp, limit_mb=180.0):
    t0 = time.time(); n = 0
    for p in sorted(pairs, key=lambda p: (p["file_name"], int(p["hdu_index"]))):
        oid = int(p["a_id"]); fn = os.path.join(cdir, "%d.npz" % oid)
        if os.path.exists(fn) or str(oid) in log: continue
        if BYTES[0] > limit_mb * 1e6: print("  transfer limit reached; stopping", flush=True); break
        try: o = F9.fetch_object(tile_path(p["file_name"]), int(p["hdu_index"]), oid)
        except RuntimeError as ex: o = str(ex)
        if isinstance(o, str): log[str(oid)] = o
        else:
            F9.save(fn, o)
            dc = o.get("DC") or []
            if dc:
                L = max(len(x) for x in dc); arr = np.full((len(dc), L), np.nan, np.float32)
                for i, x in enumerate(dc): arr[i, :len(x)] = x
                np.save(os.path.join(cdir, "%d_contam.npy" % oid), arr)
        n += 1
        if n % 20 == 0:
            json.dump(log, open(logp, "w")); print("  %4d objects (%.1f s each); %.1f MB transferred; failures %d" % (n, (time.time() - t0) / n, BYTES[0] / 1e6, len(log)), flush=True)

# ------------------------------------------------------------------ stage truthimg: one VIS cutout of the truth lens (opened only by euc14.py)
TRUTH_OBJ = (2754184908715026460, 275.41849084, 71.50264605)
TRUTH_MOSAIC = "euclid/dr1/MER/102162119/VIS/EUC_MER_BGSUB-MOSAIC-VIS_TILE102162119-E217F5_20250807T130651.965360Z_00.00.fits"

def stage_truthimg(odir, half=60):
    """the mosaic is an uncompressed float32 primary image: read its header, then the 2 * half rows of 2 * half pixels
    around the lens object, one byte range per row (IBE's cloud host refuses cutout parameters)"""
    from astropy.io import fits
    from astropy.wcs import WCS
    hdr = b""
    while b"END" + b" " * 77 not in [hdr[i:i + 80] for i in range(0, len(hdr), 80)]:
        blk = polite_range(TRUTH_MOSAIC, len(hdr), len(hdr) + 4 * 2880 - 1); hdr += blk
    n = [hdr[i:i + 80] for i in range(0, len(hdr), 80)].index(b"END" + b" " * 77) + 1
    hlen = int(math.ceil(n * 80 / 2880.0)) * 2880
    h = fits.Header.fromstring(hdr[:n * 80].decode("ascii"))
    assert h["BITPIX"] == -32 and h["NAXIS"] == 2
    x, y = WCS(h).all_world2pix(TRUTH_OBJ[1], TRUTH_OBJ[2], 0); x0, y0 = int(round(float(x))) - half, int(round(float(y))) - half
    nx = h["NAXIS1"]; img = np.zeros((2 * half, 2 * half), np.float32)
    for r in range(2 * half):
        a = hlen + 4 * ((y0 + r) * nx + x0)
        img[r] = np.frombuffer(polite_range(TRUTH_MOSAIC, a, a + 8 * half - 1), dtype=">f4")
    w = WCS(h); w.wcs.crpix = [w.wcs.crpix[0] - x0, w.wcs.crpix[1] - y0]
    out = fits.PrimaryHDU(img.astype(np.float32), header=w.to_header())
    out.header["SRCFILE"] = TRUTH_MOSAIC.split("/")[-1][:68]; out.header["X0"] = x0; out.header["Y0"] = y0
    out.writeto(os.path.join(odir, "truth_vis_cutout.fits"), overwrite=True)
    print("truthimg: %d x %d pixels around (%d, %d) of a %d x %d mosaic; %.1f kB transferred; saved (not opened)" % (2 * half, 2 * half, x0 + half, y0 + half,
          nx, h["NAXIS2"], BYTES[0] / 1e3), flush=True)
    manifest(odir)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True)
    ap.add_argument("--stage", required=True, choices=("pa", "calsel", "calalign", "calspec", "truthimg"))
    a = ap.parse_args()
    odir = os.path.join(a.data_dir, "euc14"); os.makedirs(odir, exist_ok=True)
    if a.stage == "pa": stage_pa(a.data_dir, odir)
    if a.stage == "calsel": stage_calsel(a.data_dir, odir)
    if a.stage == "calalign": stage_calalign(a.data_dir, odir)
    if a.stage == "calspec": stage_calspec(odir)
    if a.stage == "truthimg": stage_truthimg(odir)

if __name__ == "__main__":
    main()
