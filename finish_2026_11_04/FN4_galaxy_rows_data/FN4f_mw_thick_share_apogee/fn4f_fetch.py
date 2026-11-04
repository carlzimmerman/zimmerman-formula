#!/usr/bin/env python3
"""FN4f fetch: exactly the two APOGEE DR17 files the owner approved on 2026-11-04 (relayed by the lead with names and sizes).
No selection function, nothing else. Target: ../_external_data/apogee_dr17_2026_11/ beside the repository, a new empty folder.
Each file is HEAD-checked first; a Content-Length that differs from the approved size stops before any download. A file is
kept only if its bytes equal the approved size. Writes FETCH_LOG.md in the data folder and fn4f_fetch.json here (no local
paths). Run: python3 -I fn4f_fetch.py
"""
import datetime, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DST = os.path.join(os.path.dirname(REPO), "_external_data", "apogee_dr17_2026_11")
FILES = [("https://data.sdss.org/sas/dr17/env/APOGEE_ASTRO_NN/", "apogee_astroNN-DR17.fits", 647328960),
         ("https://data.sdss.org/sas/dr17/apogee/spectro/aspcap/dr17/synspec_rev1/", "allStar-dr17-synspec_rev1.fits", 3970621440)]


def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def head(url):
    r = subprocess.run(["curl", "-sIL", "--max-time", "120", url], capture_output=True, text=True)
    size = None; ctype = ""
    for l in r.stdout.splitlines():
        k = l.lower()
        if k.startswith("content-length:"): size = int(l.split(":", 1)[1])
        if k.startswith("content-type:"): ctype = l.split(":", 1)[1].strip()
    return size, ctype


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()


if os.path.exists(DST) and os.listdir(DST):
    sys.exit("target folder is not empty; stopping")
os.makedirs(DST, exist_ok=True)
heads = []
for base, name, size in FILES:
    s, t = head(base + name); heads.append(dict(file=name, head_size=s, type=t))
    if s != size or "html" in t.lower():
        json.dump(dict(stopped=True, heads=heads), open(os.path.join(HERE, "fn4f_fetch.json"), "w"), indent=1)
        sys.exit(f"HEAD for {name}: {s} B, {t}; approved {size} B. Stopping before any download")
log = []
for base, name, size in FILES:
    url = base + name; out = os.path.join(DST, name); t0 = now()
    r = subprocess.run(["curl", "-fsSL", "--retry", "3", "--max-time", "14400", "-o", out, "-w", "%{url_effective} %{content_type}", url], capture_output=True, text=True)
    t1 = now(); got = os.path.getsize(out) if os.path.exists(out) else -1
    rec = dict(file=name, url=url, final_url_and_type=r.stdout.strip(), start_utc=t0, end_utc=t1, bytes=got, approved_bytes=size, curl_rc=r.returncode)
    if got == size and r.returncode == 0: rec.update(fetched=True, sha256=sha256(out))
    else:
        if os.path.exists(out): os.remove(out)
        rec.update(fetched=False, reason=f"downloaded {got} B against approved {size} B; deleted")
    log.append(rec); print(json.dumps(rec), flush=True)
    if not rec["fetched"]: break
ok = len(log) == len(FILES) and all(x["fetched"] for x in log)
json.dump(dict(target="../_external_data/apogee_dr17_2026_11/", heads=heads, files=log, all_fetched=ok), open(os.path.join(HERE, "fn4f_fetch.json"), "w"), indent=1)
with open(os.path.join(DST, "FETCH_LOG.md"), "w") as f:
    f.write("# FETCH_LOG (apogee_dr17_2026_11)\n\nOwner's approval 2026-11-04 (relayed by the lead with names and sizes), for lane FN4f. "
            "Exactly these two files; APOGEE's selection function was not approved and was not fetched.\n\n"
            "| file | URL | UTC start | UTC end | bytes | sha256 |\n|---|---|---|---|---|---|\n")
    for x in log:
        f.write(f"| {x['file']} | {x['url']} | {x['start_utc']} | {x['end_utc']} | {x['bytes']:,} | {x.get('sha256', x.get('reason'))} |\n")
    f.write(f"\nAll approved files fetched at their approved sizes: {ok}.\n")
sys.exit(0 if ok else 1)
