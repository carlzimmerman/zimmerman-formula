#!/usr/bin/env python3
"""EUC9 fetch: the co-added and the individual dither red-grism spectra of the lens object of every target system.

Frozen criteria: FROZEN_CRITERIA.md (bea4eacfa8) sections 1-2; fetch route: AMENDMENT_A0.md (82cf65da28) A0.1.
  targets = sample S, the truth lens and grade X systems whose lens object has a redshift interval and a spectrum
            passing the quality prerequisites (euc9_common.build)
  stage assoc  : objectid -> (path, hdu) from euclid.objectid_spectrafile_association_dr1 (TAP upload join)
  stage spectra: byte-range reads of the tile file; the object is located by OBJ_ID in the META headers; its
                 co-added table and every dither table are saved as <objectid>.npz
  stage verify : 20 objects at fixed positions of the target list are read again and compared (K5)
  --generic DIR: read the field objects in DIR (npz files from the per-object service) by range and compare (K5)

Public, anonymous, one request stream.  Everything goes under <data-dir>/nisp_spectra_dith/ (outside git).
The order is a fixed shuffle (sha256 of the identifier), so an interrupted run leaves a random subset of both sides.

Run:  python3 -I euc9_fetch.py --data-dir <dir with the ECLIPSE csv files and nisp_tables/> [--stage assoc|spectra|verify|all]
"""
import argparse, csv, hashlib, io, json, os, sys, time, warnings
import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc9_common as K

TAP = "https://irsa.ipac.caltech.edu/TAP/sync"
FILES = "https://irsa.ipac.caltech.edu/ibe/data/"
UA = {"User-Agent": "generic-client"}
PACE = 0.1
BLOCK = 2880
WIN = BLOCK * 182                      # 524,160 bytes per probe
RATE = [10400.0]                       # running estimate of bytes per HDU (updated from every object found)
HOST = {}
SES = requests.Session()

def card(blk, key):
    for i in range(0, len(blk), 80):
        c = blk[i:i + 80]
        if c[:8].strip() == key.encode(): return c[10:].split(b"/")[0].strip().strip(b"'").strip().decode()
        if c[:3] == b"END": break
    return None

def get_range(path, a, b, tries=5):
    """bytes a..b of a tile file; None beyond the end of the file"""
    url = HOST.get("base", FILES) + path; err = "?"
    for k in range(tries):
        time.sleep(PACE)
        try:
            r = SES.get(url, headers=dict(UA, Range="bytes=%d-%d" % (a, b)), timeout=120)
            if r.status_code == 206:
                if "base" not in HOST and r.url != url: HOST["base"] = r.url[:len(r.url) - len(path)]
                return r.content
            if r.status_code == 416: return None
            err = "HTTP %d" % r.status_code
            if r.status_code == 429: time.sleep(min(float(r.headers.get("Retry-After", 120) or 120), 900.0))
        except Exception as ex:
            err = type(ex).__name__
        time.sleep(4.0 * (k + 1))
    raise RuntimeError("range request failed: %s" % err)

def metas(buf, off0):
    out = []
    for i in range(0, len(buf) - BLOCK + 1, BLOCK):
        blk = buf[i:i + BLOCK]
        if blk[:8] == b"XTENSION" and b"_META" in blk[:960]:
            oid, nd = card(blk, "OBJ_ID"), card(blk, "N_DITH")
            if oid is not None: out.append((off0 + i, int(oid), int(nd or 0)))
    return out

PRIMARY = (b"SIMPLE  =                    T".ljust(80) + b"BITPIX  =                    8".ljust(80) + b"NAXIS   =                    0".ljust(80)
           + b"EXTEND  =                    T".ljust(80) + b"END".ljust(80)).ljust(BLOCK)

def parse_object(buf):
    """META + co-added table + dither tables of one object, from the bytes starting at its META header"""
    from astropy.io import fits
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        hl = fits.open(io.BytesIO(PRIMARY + buf), memmap=False, ignore_missing_end=True, lazy_load_hdus=False)
        out = dict(DS=[], DM=[], DV=[], dpos=[], dtilt=[], dptg=[], dlsf=[]); seen_meta = 0
        for h in hl[1:]:
            nm = h.header.get("EXTNAME", "")
            if nm.endswith("_META"):
                seen_meta += 1
                if seen_meta > 1: break
                out["oid"] = int(h.header["OBJ_ID"]); out["n_dith"] = int(h.header.get("N_DITH", 0))
            elif nm.endswith("_COMBINED1D_SIGNAL"):
                d = h.data
                out.update(WAVELENGTH=np.array(d["WAVELENGTH"], np.float32), SIGNAL=np.array(d["SIGNAL"], np.float32), MASK=np.array(d["MASK"], np.int32),
                           QUALITY=np.array(d["QUALITY"], np.float32), VAR=np.array(d["VAR"], np.float32), NDITH=np.array(d["NDITH"], np.int16),
                           lsf=float(h.header.get("LSF_SIG", np.nan)))
            elif "_DITH1D_" in nm and nm.endswith("_SIGNAL"):
                d = h.data
                out["DS"].append(np.array(d["SIGNAL"], np.float32)); out["DM"].append(np.array(d["MASK"], np.int32)); out["DV"].append(np.array(d["VAR"], np.float32))
                out["dpos"].append(str(h.header.get("GWA_POS", "")).strip()); out["dtilt"].append(float(h.header.get("GWA_TILT", np.nan)))
                out["dptg"].append(int(h.header.get("PTGID", -1))); out["dlsf"].append(float(h.header.get("LSF_SIG", np.nan)))
        hl.close()
    return out

def fetch_object(path, hdu, oid, max_probe=14):
    """locate the object by OBJ_ID and return its parsed tables, or a string saying why not"""
    guess = RATE[0] * hdu; lo = hi = None; sign = 1
    for it in range(max_probe):
        a = max(0, (int(guess) // BLOCK) * BLOCK - WIN // 2)
        buf = get_range(path, a, a + WIN - 1)
        if buf is None:                                        # beyond the end of the file
            hi = (a, None); guess = (lo[0] + a) / 2.0 if lo else a * 0.6; continue
        ms = metas(buf, a)
        if not ms: guess = a + WIN + WIN // 2; continue
        if len(ms) > 1 and ms[-1][1] != ms[0][1]: sign = 1 if ms[-1][1] > ms[0][1] else -1
        hit = [m for m in ms if m[1] == oid]
        if hit:
            off, _, nd = hit[0]
            if nd == 0: return "the tile file has no dither for this object"
            need = BLOCK + 17280 + nd * 23040 + BLOCK
            seg = buf[off - a: off - a + need]
            if len(seg) < need:
                more = get_range(path, off, off + need - 1); seg = more if more is not None else seg
            o = parse_object(seg)
            if o.get("oid") != oid or "SIGNAL" not in o: return "object tables not parsed"
            RATE.append(off / float(hdu)); RATE[0] = float(np.median(RATE[-20:]))
            o["probes"] = it + 1
            return o
        if (oid - ms[0][1]) * sign < 0: hi = (ms[0][0], ms[0][1])
        elif (oid - ms[-1][1]) * sign > 0: lo = (ms[-1][0], ms[-1][1])
        else: return "OBJ_ID not present where the file's order puts it"
        if lo and hi and hi[1] is not None:
            f = (oid - lo[1]) / float(hi[1] - lo[1]); f = min(max(f, 0.1), 0.9)
            guess = lo[0] + f * (hi[0] - lo[0])
            if hi[0] - lo[0] <= WIN: guess = (lo[0] + hi[0]) / 2.0
        else:
            slope = (ms[-1][0] - ms[0][0]) / float(ms[-1][1] - ms[0][1]) if len(ms) > 1 and ms[-1][1] != ms[0][1] else 0.0
            anc = lo if lo else hi
            step = slope * (oid - anc[1]) if slope else (WIN if lo else -WIN)
            if hi and hi[1] is None and lo: guess = (lo[0] + hi[0]) / 2.0
            else: guess = max(0.0, anc[0] + 1.2 * step + (WIN // 4 if lo else -WIN // 4))
    return "not located in %d probes" % max_probe

def save(fn, o):
    np.savez_compressed(fn, WAVELENGTH=o["WAVELENGTH"], SIGNAL=o["SIGNAL"], MASK=o["MASK"], QUALITY=o["QUALITY"], VAR=o["VAR"], NDITH=o["NDITH"],
                        UNCERTAINTY=np.sqrt(np.clip(o["VAR"], 0, None)).astype(np.float32), lsf=o["lsf"], n_dith=o["n_dith"],
                        DS=np.array(o["DS"], np.float32).reshape(len(o["DS"]), -1), DM=np.array(o["DM"], np.int32).reshape(len(o["DM"]), -1),
                        DV=np.array(o["DV"], np.float32).reshape(len(o["DV"]), -1), dpos=np.array(o["dpos"]), dtilt=np.array(o["dtilt"]), dptg=np.array(o["dptg"]),
                        dlsf=np.array(o["dlsf"]))

def votable_ids(ids):
    s = io.StringIO()
    s.write('<?xml version="1.0"?>\n<VOTABLE version="1.3" xmlns="http://www.ivoa.net/xml/VOTable/v1.3">\n<RESOURCE><TABLE>\n'
            '<FIELD name="oid" datatype="long"/>\n<DATA><TABLEDATA>\n')
    for i in ids: s.write("<TR><TD>%d</TD></TR>\n" % i)
    s.write("</TABLEDATA></DATA>\n</TABLE></RESOURCE>\n</VOTABLE>\n")
    return s.getvalue().encode()

def query_assoc(ids, chunk=2000):
    out = []
    for c0 in range(0, len(ids), chunk):
        for k in range(6):
            time.sleep(2.0); t0 = time.time()
            try:
                r = requests.post(TAP, data=dict(QUERY="SELECT t.objectid, t.tileid, t.path, t.hdu FROM euclid.objectid_spectrafile_association_dr1 AS t, "
                                                 "TAP_UPLOAD.up AS u WHERE t.objectid = u.oid", FORMAT="CSV", UPLOAD="up,param:tbl"),
                                  files=dict(tbl=("up.xml", votable_ids(ids[c0:c0 + chunk]), "application/x-votable+xml")), headers=UA, timeout=900)
                if r.status_code == 200 and not r.text.lstrip().startswith("<"):
                    rows = [x for x in csv.reader(io.StringIO(r.text))][1:]
                    out.extend(x for x in rows if x); print("  assoc chunk %5d: %d ids -> %d rows (%.0f s)" % (c0, len(ids[c0:c0 + chunk]), len(rows), time.time() - t0), flush=True)
                    break
                err = "HTTP %d" % r.status_code
            except Exception as ex:
                err = type(ex).__name__
            print("  assoc request failed (%s); retry %d" % (err, k + 1), flush=True); time.sleep(20.0 * (k + 1))
        else:
            raise RuntimeError("association query failed")
    return out

def assoc(path):
    a = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f): a.setdefault(int(r["objectid"]), []).append((r["path"], int(r["hdu"])))
    return {k: sorted(v) for k, v in a.items()}

def write_assoc(path, rows):
    with open(path + ".tmp", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["objectid", "tileid", "path", "hdu"]); w.writerows(rows)
    os.replace(path + ".tmp", path)

COLS = ("WAVELENGTH", "SIGNAL", "MASK", "QUALITY", "VAR", "NDITH")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True)
    ap.add_argument("--stage", default="all", choices=("assoc", "spectra", "verify", "all"))
    ap.add_argument("--generic", default="")
    a = ap.parse_args()
    sdir = os.path.join(a.data_dir, "nisp_spectra_dith"); os.makedirs(sdir, exist_ok=True)
    if a.generic:                                                   # field objects: range route against the per-object service
        gids = sorted(int(f[:-4]) for f in os.listdir(a.generic) if f.endswith(".npz"))
        gp = os.path.join(sdir, "generic_assoc.csv")
        if not os.path.exists(gp): write_assoc(gp, query_assoc(gids))
        A = assoc(gp); res = []; t0 = time.time()
        for oid in gids:
            if oid not in A: continue
            o = fetch_object(A[oid][0][0], A[oid][0][1], oid)
            if isinstance(o, str): res.append(dict(oid=oid, ok=False, why=o)); continue
            c = np.load(os.path.join(a.generic, "%d.npz" % oid))
            same = all(np.array_equal(np.asarray(o[k], float), np.asarray(c[k], float), equal_nan=True) for k in COLS)
            unc = bool(np.allclose(np.sqrt(np.clip(o["VAR"], 0, None)), np.asarray(c["UNCERTAINTY"], float), rtol=1e-5, atol=1e-9))
            res.append(dict(oid=oid, ok=bool(same and unc), probes=o["probes"], n_dith=len(o["DS"]), pos=sorted(set(o["dpos"]))))
            save(os.path.join(sdir, "generic_%d.npz" % oid), o)
        json.dump(res, open(os.path.join(sdir, "generic_check.json"), "w"), indent=1)
        print("field objects read by range: %d; identical to the per-object service: %d; mean probes %.1f; %.1f s each"
              % (len(res), sum(r["ok"] for r in res), np.mean([r.get("probes", 0) for r in res]), (time.time() - t0) / max(len(res), 1)), flush=True)
        return
    B = K.build(a.data_dir)
    tg = sorted((d for d in B["SYS"].values() if d.get("target")), key=lambda d: hashlib.sha256(d["id"].encode()).hexdigest())
    tg.sort(key=lambda d: d["id"] != K.TRUTH[0])                       # the truth lens first
    ids = sorted({d["oid"] for d in tg})
    print("targets: %d systems (S %d, X %d, truth %d); %d lens objects" % (len(tg), sum(d["inS"] for d in tg), sum(d["isX"] for d in tg),
          sum(d["id"] == K.TRUTH[0] for d in tg), len(ids)), flush=True)
    ap_ = os.path.join(sdir, "spec_assoc.csv")
    if a.stage in ("assoc", "all") and not os.path.exists(ap_): write_assoc(ap_, query_assoc(ids))
    A = assoc(ap_)
    print("objects with an association row: %d of %d (more than one row: %d)" % (sum(i in A for i in ids), len(ids), sum(len(A.get(i, [])) > 1 for i in ids)), flush=True)
    logp = os.path.join(sdir, "fetch_log.json")
    log = json.load(open(logp)) if os.path.exists(logp) else {}
    if a.stage in ("spectra", "all"):
        t0 = time.time(); n = 0; probes = 0
        for d in tg:
            oid = d["oid"]; fn = os.path.join(sdir, "%d.npz" % oid)
            if os.path.exists(fn) or str(oid) in log: continue
            if oid not in A: log[str(oid)] = "no association row"; continue
            try: o = fetch_object(A[oid][0][0], A[oid][0][1], oid)
            except RuntimeError as ex: o = str(ex)
            if isinstance(o, str): log[str(oid)] = o
            else: save(fn, o); probes += o["probes"]
            n += 1
            if n % 100 == 0:
                json.dump(log, open(logp, "w")); print("  %5d objects this run (%.2f s each, %.2f probes each); without a spectrum so far %d" % (n, (time.time() - t0) / n, probes / max(n - 0, 1), len(log)), flush=True)
        json.dump(log, open(logp, "w"))
        print("spectra stage done: %d cached, %d without a spectrum" % (sum(os.path.exists(os.path.join(sdir, "%d.npz" % d["oid"])) for d in tg), len(log)), flush=True)
    if a.stage in ("verify", "all"):
        have = [d for d in tg if os.path.exists(os.path.join(sdir, "%d.npz" % d["oid"]))]
        out = []
        for d in have[::max(len(have) // 20, 1)][:20]:
            o = fetch_object(A[d["oid"]][0][0], A[d["oid"]][0][1], d["oid"]); c = np.load(os.path.join(sdir, "%d.npz" % d["oid"]))
            same = (not isinstance(o, str)) and all(np.array_equal(o[k], c[k], equal_nan=True) for k in COLS) and np.array_equal(np.array(o["DS"]).reshape(c["DS"].shape), c["DS"], equal_nan=True)
            out.append(dict(oid=d["oid"], identical=bool(same)))
        json.dump(out, open(os.path.join(sdir, "verify.json"), "w"), indent=1)
        print("verify: %d of %d read again identical" % (sum(o["identical"] for o in out), len(out)), flush=True)
    print("fetch done", flush=True)

if __name__ == "__main__":
    main()
