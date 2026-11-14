#!/usr/bin/env python3
"""WLG1R fetch (FROZEN_CRITERIA.md, 8a730ebaa1): Euclid DR1 photo-z and physical parameters by object_id for every
object passing EUC6R's neighbour cut in EUC6R's 665 MER cones, plus the ECLIPSE MER object of every W, C and L lens
(added so KA-6 and Delta can be read even if a lens object fails the neighbour cut; disclosed in RESULT_BLIND.md).

One paced stream (>= 1.5 s between requests), at most 1,000 ids per request, retries after 10, 30, 90, 270 s, generic
client name, no personal details. Raw responses gzipped under _external_data/wlg1r_phz_by_id/ (untracked); manifest
wlg1r_fetch_manifest.csv (committed). Resumable.
  nice -n 19 python3 -I wlg1r_fetch.py ids     # verify cone hashes, list ids -> wlg1r_ids.txt (untracked helper)
  nice -n 19 python3 -I wlg1r_fetch.py fetch
TEST lane, blind re-grade. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import csv, gzip, hashlib, io, math, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CONES = os.path.join(REPO, "_external_data", "euclid_dr1_mer_cones_euc6r")
E6R = os.path.join(REPO, "closure_2026_11_12", "EUC6R_blind_regrade")
ECL = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
RAW = os.path.join(REPO, "_external_data", "wlg1r_phz_by_id")
MAN = os.path.join(HERE, "wlg1r_fetch_manifest.csv")
IDS = os.path.join(RAW, "wlg1r_ids.txt")
TAP = "https://eas.esac.esa.int/tap-server/tap/sync"
UA = "tap-client/1.0"
PACE = 1.5; RETRY = [10, 30, 90, 270]; BATCH = 1000
COLS = ("p.object_id, p.phz_median, p.phz_70_int, p.phz_flags, p.phz_classification, q.phz_pp_median_stellarmass, "
        "q.phz_pp_68_stellarmass, q.phz_pp_median_redshift, q.quality_flag")
FLUX_CUT, PLP_CUT, DQF_CUT = 5.75, 0.7, 4


def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return float("nan")


def cut_ok(o):
    return (fnum(o["flux_h_templfit"]) > FLUX_CUT and fnum(o["spurious_flag"]) == 0 and fnum(o["det_quality_flag"]) < DQF_CUT
            and fnum(o["point_like_prob"]) < PLP_CUT)


def build_ids():
    man = list(csv.DictReader(open(os.path.join(E6R, "euc6r_manifest.csv"), newline="")))
    if len(man) != 665: sys.exit(f"EUC6R manifest has {len(man)} rows, not 665")
    ids = set(); nbad = 0; ncut = 0
    for m in man:
        body = gzip.open(os.path.join(CONES, m["file"])).read()
        if hashlib.sha256(body).hexdigest() != m["sha256_raw"]: nbad += 1; continue
        for o in csv.DictReader(io.StringIO(body.decode())):
            if cut_ok(o): ids.add(int(o["object_id"])); ncut += 1
    if nbad: sys.exit(f"{nbad} cone files fail EUC6R's hash")
    tg = list(csv.DictReader(open(os.path.join(E6R, "euc6r_targets.csv"), newline="")))
    obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(ECL, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8"))}
    lens_ids = set()
    for t in tg:
        if t["kind"] in ("W", "C", "L"):
            v = obj[t["lens_id"]]["MER_object_id"].strip()
            if v: lens_ids.add(int(float(v)) if "e" in v.lower() else int(v))
    add = lens_ids - ids
    allids = sorted(ids | lens_ids)
    os.makedirs(RAW, exist_ok=True)
    open(IDS, "w").write("\n".join(str(i) for i in allids) + "\n")
    print(f"cones 665 hash-checked; cut rows {ncut}; distinct cut ids {len(ids)}; lens MER ids {len(lens_ids)} "
          f"({len(add)} not among the cut ids); total {len(allids)} -> {math.ceil(len(allids) / BATCH)} requests")


def tap(query, timeout=600):
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv", "MAXREC": "1000000", "QUERY": query}).encode()
    req = urllib.request.Request(TAP, data=data, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r: return r.read()


def fetch():
    allids = [int(x) for x in open(IDS).read().split()]
    batches = [allids[i:i + BATCH] for i in range(0, len(allids), BATCH)]
    man = {}
    if os.path.exists(MAN):
        for m in csv.DictReader(open(MAN, newline="")): man[m["batch"]] = m
    fields = ["batch", "file", "n_ids", "rows", "sha256_raw", "seconds", "utc", "first_id", "last_id"]
    for k, b in enumerate(batches):
        name = f"b{k:04d}"
        if name in man and os.path.exists(os.path.join(RAW, man[name]["file"])): continue
        q = (f"SELECT {COLS} FROM dr1.phz_photo_z_wide AS p LEFT JOIN dr1.phz_physical_parameters_wide AS q "
             f"ON p.object_id = q.object_id WHERE p.object_id IN ({', '.join(str(i) for i in b)})")
        last = None
        for t in range(len(RETRY) + 1):
            try:
                t0 = time.time(); body = tap(q); dt = time.time() - t0
                if not body[:200].decode("utf-8", "replace").startswith("object_id"): raise RuntimeError(body[:150])
                break
            except Exception as e:
                last = e; body = None
                if t < len(RETRY): print(f"  retry in {RETRY[t]} s: {str(e)[:100]}", flush=True); time.sleep(RETRY[t])
        if body is None: sys.exit(f"failed: {last}")
        fn = name + ".csv.gz"
        with gzip.open(os.path.join(RAW, fn), "wb") as f: f.write(body)
        man[name] = dict(batch=name, file=fn, n_ids=len(b), rows=body.decode().count("\n") - 1, sha256_raw=hashlib.sha256(body).hexdigest(),
                         seconds=f"{dt:.1f}", utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), first_id=b[0], last_id=b[-1])
        with open(MAN + ".tmp", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
            for kk in sorted(man): w.writerow(man[kk])
        os.replace(MAN + ".tmp", MAN)
        print(f"[{k + 1}/{len(batches)}] {name} ids {len(b)} rows {man[name]['rows']} {dt:.1f}s", flush=True)
        time.sleep(PACE)


if __name__ == "__main__":
    {"ids": build_ids, "fetch": fetch}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
