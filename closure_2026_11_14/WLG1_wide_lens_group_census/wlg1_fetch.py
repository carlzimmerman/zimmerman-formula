#!/usr/bin/env python3
"""WLG1 fetch (FROZEN_CRITERIA.md section 2): Euclid DR1 photo-z and physical parameters, by object_id lists, for every
object passing EUC6R's neighbour cut in EUC6R's 665 MER cones, plus each lens's own MER object.

ESA Euclid archive TAP, anonymous, one stream, >= 1.5 s between requests, generic client name, retries 10/30/90/270 s.
Raw responses gzipped under _external_data/wlg1_phz_by_id/ (untracked); manifest wlg1_fetch_manifest.csv beside this file.
Resumable. Run:  nice -n 19 python3 -I wlg1_fetch.py
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import csv, gzip, hashlib, io, math, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CONES = os.path.join(REPO, "_external_data", "euclid_dr1_mer_cones_euc6r")
OUTD = os.path.join(REPO, "_external_data", "wlg1_phz_by_id")
TGT = os.path.join(REPO, "closure_2026_11_12", "EUC6R_blind_regrade", "euc6r_targets.csv")
MAN6 = os.path.join(REPO, "closure_2026_11_12", "EUC6R_blind_regrade", "euc6r_manifest.csv")
OBJ = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse", "ECLIPSE_object_catalogue.csv")
MAN = os.path.join(HERE, "wlg1_fetch_manifest.csv")
TAP = "https://eas.esac.esa.int/tap-server/tap/sync"
UA = "tap-client/1.0"
PACE, RETRY, CHUNK = 1.5, [10, 30, 90, 270], 1000
COLS = ("p.object_id, p.phz_median, p.phz_70_int, p.phz_flags, p.phz_classification, pp.phz_pp_median_stellarmass, "
        "pp.phz_pp_68_stellarmass, pp.phz_pp_median_redshift, pp.quality_flag")
FLUX_CUT, PLP_CUT, DQF_CUT = 5.75, 0.7, 4


def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return float("nan")


def sha256b(b): return hashlib.sha256(b).hexdigest()


def cut_ids(path):
    ids = []
    for o in csv.DictReader(io.StringIO(gzip.open(path, "rt").read())):
        fl, sp, dq, pl = (fnum(o[k]) for k in ("flux_h_templfit", "spurious_flag", "det_quality_flag", "point_like_prob"))
        if fl > FLUX_CUT and sp == 0 and dq < DQF_CUT and pl < PLP_CUT:
            ids.append(int(o["object_id"]))
    return ids


_last = [0.0]
def query(adql):
    for k in range(len(RETRY) + 1):
        dt = time.time() - _last[0]
        if dt < PACE: time.sleep(PACE - dt)
        _last[0] = time.time()
        try:
            r = requests.post(TAP, data=dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=adql),
                              headers={"User-Agent": UA}, timeout=280)
            if r.status_code == 200 and r.text.startswith("object_id"):
                return r.text
            msg = "HTTP %d %s" % (r.status_code, r.text[:120].replace("\n", " "))
        except Exception as e:
            msg = repr(e)[:160]
        if k < len(RETRY):
            print("   retry in %d s: %s" % (RETRY[k], msg), flush=True); time.sleep(RETRY[k])
    return None


def main():
    os.makedirs(OUTD, exist_ok=True)
    m6 = {r["target"]: r for r in csv.DictReader(open(MAN6, newline=""))}
    mer = {r["Unique_Identifier"]: r["MER_object_id"].strip() for r in csv.DictReader(open(OBJ, newline="", encoding="utf-8"))}
    T = list(csv.DictReader(open(TGT, newline="")))
    done = {}
    if os.path.exists(MAN):
        done = {r["target"]: r for r in csv.DictReader(open(MAN, newline=""))}
    t0 = time.time(); n_new = 0
    for i, t in enumerate(T):
        key = t["target"]
        if key in done: continue
        fpath = os.path.join(CONES, m6[key]["file"])
        raw = open(fpath, "rb").read()
        if sha256b(raw) != m6[key]["sha256_raw"] and sha256b(gzip.decompress(raw)) != m6[key]["sha256_raw"]:
            sys.exit("cone hash mismatch: " + key)
        ids = cut_ids(fpath)
        lm = mer.get(t["lens_id"], "")
        if t["kind"] in ("W", "C", "L") and lm:
            try:
                v = int(lm)
                if v not in ids: ids.append(v)
            except ValueError:
                pass
        ids = sorted(set(ids))
        parts = []; ok = True
        for j in range(0, len(ids), CHUNK):
            chunk = ids[j:j + CHUNK]
            adql = ("SELECT %s FROM dr1.phz_photo_z_wide AS p LEFT OUTER JOIN dr1.phz_physical_parameters_wide AS pp "
                    "ON p.object_id = pp.object_id WHERE p.object_id IN (%s)" % (COLS, ",".join(str(x) for x in chunk)))
            txt = query(adql)
            if txt is None: ok = False; break
            lines = txt.splitlines()
            parts.append(lines if not parts else lines[1:])
        if not ok:
            print("FAILED %s; continuing" % key, flush=True); continue
        body = ("\n".join(l for p in parts for l in p) + "\n").encode() if parts else b"object_id\n"
        name = key.replace(":", "_") + ".csv.gz"
        with open(os.path.join(OUTD, name), "wb") as f: f.write(gzip.compress(body, mtime=0))
        nrow = max(0, body.count(b"\n") - 1)
        new = not os.path.exists(MAN)
        with open(MAN, "a", newline="") as f:
            w = csv.writer(f)
            if new: w.writerow(["target", "file", "ids_sent", "rows", "sha256_raw", "utc"])
            w.writerow([key, name, len(ids), nrow, sha256b(body), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())])
        n_new += 1
        if n_new % 20 == 0:
            print("  %d / %d targets (%.0f s)" % (i + 1, len(T), time.time() - t0), flush=True)
    print("done (%.0f s); new %d" % (time.time() - t0, n_new), flush=True)


if __name__ == "__main__":
    main()
