#!/usr/bin/env python3
"""EUC15 fetch: a 64 x 64-pixel (6.4 arcsec) box of Euclid's VIS mosaic around the lens object of every system with a
cached dither spectrum (EUC9's targets: sample S, grade X and the truth lens), for the image-arc procedure that EUC14
froze for the truth lens (euc14.truth_arc).

  stage tiles : ESA archive TAP, dr1.mosaic_product: the VIS background-subtracted mosaic of each MER tile involved.
  stage boxes : the mosaics are uncompressed float32 primary images in the public AWS Open Data bucket
                nasa-irsa-euclid-dr1 (the same files IRSA serves): per tile, the header (WCS); per system, 64 byte
                ranges of 256 bytes, one per row.  At most 8 parallel keep-alive connections, about 60 requests a
                second in all; on 429 / 5xx wait 150 s, stop if it persists.  Each box is written as a small FITS file
                with the WCS shifted, exactly like EUC14's truth-lens cutout.  Resumable; manifest with sha256.
                Hard cap on transfer (this lane's cap is 300 MB including an accidental 144 MB, see RESULT).

Run:  python3 -I euc15_fetch.py --data-dir <dir with nisp_spectra_dith/ and nisp_tables/> --stage tiles|boxes [--only truth|all]
"""
import argparse, csv, glob, hashlib, io, json, math, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ESA = "https://eas.esac.esa.int/tap-server/tap/sync"
S3 = "https://nasa-irsa-euclid-dr1.s3.amazonaws.com/"
UA = {"User-Agent": "generic-client"}
HALF = 32                                   # box = 2 * HALF pixels = 6.4 arcsec at 0.1 arcsec per pixel
WORKERS, RATE = 4, 60.0
BACKOFF, MAX_BACKOFFS = 150.0, 3
CAP_MB = 140.0
TRUTH_OID = 2754184908715026460

BYTES = [0]; LOCK = threading.Lock(); T_LAST = [0.0]
TL = threading.local()

def session():
    if not hasattr(TL, "s"): TL.s = requests.Session()
    return TL.s

def throttle():
    with LOCK:
        now = time.time(); wait = T_LAST[0] + 1.0 / RATE - now
        if wait > 0: time.sleep(wait)
        T_LAST[0] = max(now, T_LAST[0] + 1.0 / RATE)

def get_range(key, a, b):
    for k in range(MAX_BACKOFFS + 1):
        throttle()
        try:
            r = session().get(S3 + key, headers=dict(UA, Range="bytes=%d-%d" % (a, b)), timeout=20); code = r.status_code
        except Exception as ex:
            code = type(ex).__name__
        if code == 206 and len(r.content) == b - a + 1:
            with LOCK: BYTES[0] += len(r.content)
            return r.content
        if code == 200: raise SystemExit("server ignored the range: stopped")
        if k == MAX_BACKOFFS: break
        print("  S3 answered %s; waiting %.0f s" % (code, BACKOFF), flush=True); time.sleep(BACKOFF)
    raise SystemExit("S3 errors persist: stopped; resume later")

def esa(query):
    for k in range(4):
        time.sleep(2.0)
        try:
            r = requests.post(ESA, data=dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=query), headers=UA, timeout=600)
            if r.status_code == 200 and not r.text.lstrip().startswith("<"): return list(csv.DictReader(io.StringIO(r.text)))
        except Exception:
            pass
        time.sleep(20.0 * (k + 1))
    raise SystemExit("ESA query failed")

def targets(data_dir):
    """lens object id -> (ra, dec, tile) for every object with a cached dither spectrum"""
    oids = {int(f[:-4]) for f in os.listdir(os.path.join(data_dir, "nisp_spectra_dith")) if f.endswith(".npz") and not f.startswith("generic")}
    out = {}
    for fn in sorted(glob.glob(os.path.join(data_dir, "nisp_tables", "mer_*.csv"))):
        for r in csv.DictReader(open(fn)):
            o = int(r["object_id"])
            if o in oids and o not in out: out[o] = (float(r["ra"]), float(r["dec"]), int(r["tileid"]))
    return out

def stage_tiles(data_dir, odir):
    T = targets(data_dir); tiles = sorted({v[2] for v in T.values()}); rows = []
    for i in range(0, len(tiles), 400):
        rows += esa("SELECT tile_index, file_name, file_path FROM dr1.mosaic_product WHERE instrument_name = 'VIS' AND filter_name = 'VIS' "
                    "AND product_type = 'DpdMerBksMosaic' AND tile_index IN (%s)" % ",".join(str(t) for t in tiles[i:i + 400]))
    per = {}
    for r in rows:
        if "BGSUB-MOSAIC-VIS" in r["file_name"]: per.setdefault(int(r["tile_index"]), set()).add(r["file_name"])
    with open(os.path.join(odir, "vis_tiles.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["tile", "file_name"])
        for t in tiles:
            for fn in sorted(per.get(t, [])): w.writerow([t, fn])
    print("tiles: %d needed, %d with one VIS mosaic, %d with several, %d with none" % (len(tiles), sum(len(per.get(t, [])) == 1 for t in tiles),
          sum(len(per.get(t, [])) > 1 for t in tiles), sum(t not in per for t in tiles)), flush=True)

def header(key):
    hdr = b""
    while True:
        hdr += get_range(key, len(hdr), len(hdr) + 2 * 2880 - 1)
        cards = [hdr[i:i + 80] for i in range(0, len(hdr), 80)]
        if any(c.startswith(b"END" + b" " * 77) for c in cards): break
        if len(hdr) > 20 * 2880: raise SystemExit("no END card")
    n = [c.startswith(b"END" + b" " * 77) for c in cards].index(True) + 1
    return hdr[:n * 80].decode("ascii"), int(math.ceil(n * 80 / 2880.0)) * 2880

def box(key, hstr, hlen, oid, ra, de, bdir):
    from astropy.io import fits
    from astropy.wcs import WCS
    h = fits.Header.fromstring(hstr); w = WCS(h)
    if h["BITPIX"] != -32 or h["NAXIS"] != 2: return "not a float32 image"
    x, y = w.all_world2pix(ra, de, 0); x0, y0 = int(round(float(x))) - HALF, int(round(float(y))) - HALF
    nx, ny = h["NAXIS1"], h["NAXIS2"]
    if x0 < 0 or y0 < 0 or x0 + 2 * HALF > nx or y0 + 2 * HALF > ny: return "box off the mosaic"
    img = np.zeros((2 * HALF, 2 * HALF), np.float32)
    for r in range(2 * HALF):
        a = hlen + 4 * ((y0 + r) * nx + x0)
        img[r] = np.frombuffer(get_range(key, a, a + 8 * HALF - 1), dtype=">f4")
    w2 = WCS(h); w2.wcs.crpix = [w2.wcs.crpix[0] - x0, w2.wcs.crpix[1] - y0]
    out = fits.PrimaryHDU(img, header=w2.to_header()); out.header["X0"] = x0; out.header["Y0"] = y0
    out.header["SRCFILE"] = key.split("/")[-1][:68]
    out.writeto(os.path.join(bdir, "%d.fits" % oid), overwrite=True)
    return None

def manifest(bdir, odir):
    m = {fn: hashlib.sha256(open(os.path.join(bdir, fn), "rb").read()).hexdigest() for fn in sorted(os.listdir(bdir)) if fn.endswith(".fits")}
    json.dump(m, open(os.path.join(odir, "manifest_boxes.json"), "w"), indent=0, sort_keys=True)

def stage_boxes(data_dir, odir, only):
    T = targets(data_dir); bdir = os.path.join(odir, "vis_boxes"); os.makedirs(bdir, exist_ok=True)
    tf = {}
    for r in csv.DictReader(open(os.path.join(odir, "vis_tiles.csv"))): tf.setdefault(int(r["tile"]), []).append(r["file_name"])
    if only == "truth": T = {k: v for k, v in T.items() if k == TRUTH_OID}
    logp = os.path.join(bdir, "fetch_log.json"); log = json.load(open(logp)) if os.path.exists(logp) else {}
    todo = [(o, v) for o, v in sorted(T.items(), key=lambda kv: (kv[1][2] or 0, kv[0])) if not os.path.exists(os.path.join(bdir, "%d.fits" % o)) and str(o) not in log]
    hdrs = {}; hlock = threading.Lock(); t0 = time.time(); done = [0]
    def key_of(tile):
        fns = tf.get(tile, [])                                    # several versions: the latest processing time in the name
        return None if not fns else "dr1/MER/%d/VIS/%s" % (tile, sorted(fns, key=lambda f: f.split("_")[-2])[-1])
    def work(item):
        o, (ra, de, tile) = item
        if BYTES[0] > CAP_MB * 1e6: return o, "transfer cap reached"
        key = key_of(tile)
        if key is None: return o, "no VIS mosaic for the tile"
        with hlock: hv = hdrs.get(key)
        if hv is None:
            hv = header(key)
            with hlock: hdrs[key] = hv
        why = box(key, hv[0], hv[1], o, ra, de, bdir)
        return o, why
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for o, why in ex.map(work, todo):
            if why: log[str(o)] = why
            done[0] += 1
            if done[0] % 200 == 0:
                json.dump(log, open(logp, "w"))
                print("  %5d of %d systems (%.2f s each); %.1f MB; reasons %d" % (done[0], len(todo), (time.time() - t0) / done[0], BYTES[0] / 1e6, len(log)), flush=True)
    json.dump(log, open(logp, "w")); manifest(bdir, odir)
    print("boxes: %d cached, %d with a reason, %.1f MB transferred this run" % (sum(fn.endswith(".fits") for fn in os.listdir(bdir)), len(log), BYTES[0] / 1e6), flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True)
    ap.add_argument("--stage", required=True, choices=("tiles", "boxes")); ap.add_argument("--only", default="all", choices=("all", "truth"))
    a = ap.parse_args()
    odir = os.path.join(a.data_dir, "euc15"); os.makedirs(odir, exist_ok=True)
    if a.stage == "tiles": stage_tiles(a.data_dir, odir)
    if a.stage == "boxes": stage_boxes(a.data_dir, odir, a.only)

if __name__ == "__main__":
    main()
