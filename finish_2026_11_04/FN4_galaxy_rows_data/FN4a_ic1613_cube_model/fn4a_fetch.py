#!/usr/bin/env python3
"""FN4a fetch: exactly the files the owner approved on 2026-11-04 (relayed by the lead with names and sizes), nothing else.
Target: ../_external_data/fn4a_ic1613_2026_11/ beside the repository, a new empty folder.

Attempt 1 (logged in fn4a_fetch.json as 'attempt1'): a plain GET of ic1613_ubvcalib.txt on science.nrao.edu returned a
33,529-byte HTML page view (the site runs Plone), not the 1,881-byte file; the fetch stopped there as designed and the HTML
copy was deleted. Attempt 2 (this version), per the lead: for each file, candidate URLs on the same host are HEAD-checked
in order (the bare URL, then Plone's /@@download/file/<name>, /@@download/file, /at_download/file); the first whose
Content-Length equals the approved size and whose type is not HTML is fetched. A file is kept only if its bytes equal the
approved size; otherwise it is deleted and reported. A file with no such URL is not fetched and is reported.
Writes FETCH_LOG.md in the data folder and fn4a_fetch.json here (no local paths). Run: python3 -I fn4a_fetch.py
"""
import datetime, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DST = os.path.join(os.path.dirname(REPO), "_external_data", "fn4a_ic1613_2026_11")
HI = "http://things.cv.nrao.edu/littlethings/ic1613/HI/"
OPT = "https://science.nrao.edu/science/surveys/littlethings/data/ic1613/"
FILES = [(OPT, "ic1613_ubvcalib.txt", 1881), (OPT, "ic1613v.fits", 10082880), (OPT, "ic1613b.fits", 10082880),
         (HI, "IC1613_NA_X0_P_R.FITS", 16902720), (HI, "IC1613_NA_XMOM1.FITS", 16899840), (HI, "IC1613_NA_XMOM2.FITS", 16899840),
         (HI, "IC1613_NA_ICL001.FITS", 1801082880), (HI, "IC1613_R_ICL001.FITS", 1813118400)]
ATTEMPT1 = dict(file="ic1613_ubvcalib.txt", url=OPT + "ic1613_ubvcalib.txt", start_utc="2026-11-04T20:11:45Z", bytes=33529,
                content="text/html page view, not the file", action="deleted; fetch stopped")


def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def head(url):
    r = subprocess.run(["curl", "-sIL", "--max-time", "120", "-A", "Mozilla/5.0", url], capture_output=True, text=True)
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
log = []
for base, name, size in FILES:
    cands = [base + name] + ([base + name + "/@@download/file/" + name, base + name + "/@@download/file", base + name + "/at_download/file"] if base == OPT else [])
    tried = []; use = None
    for u in cands:
        s, t = head(u); tried.append(dict(url=u, head_size=s, type=t))
        if s == size and "html" not in t.lower(): use = u; break
    rec = dict(file=name, approved_bytes=size, head_tried=tried)
    if use is None:
        rec.update(fetched=False, reason="no URL on the approved host gives the approved size as a non-HTML file")
        log.append(rec); print(json.dumps(rec), flush=True); continue
    out = os.path.join(DST, name); t0 = now()
    r = subprocess.run(["curl", "-fsSL", "--retry", "3", "--max-time", "7200", "-A", "Mozilla/5.0", "-o", out, "-w", "%{url_effective} %{content_type}", use],
                       capture_output=True, text=True)
    t1 = now(); got = os.path.getsize(out) if os.path.exists(out) else -1
    rec.update(url=use, final_url_and_type=r.stdout.strip(), start_utc=t0, end_utc=t1, bytes=got, curl_rc=r.returncode)
    if got == size and r.returncode == 0:
        rec.update(fetched=True, sha256=sha256(out))
    else:
        if os.path.exists(out): os.remove(out)
        rec.update(fetched=False, reason=f"downloaded {got} B against approved {size} B; deleted")
    log.append(rec); print(json.dumps({k: v for k, v in rec.items() if k != "head_tried"}), flush=True)
ok = all(x["fetched"] for x in log)
json.dump(dict(target="../_external_data/fn4a_ic1613_2026_11/", attempt1=ATTEMPT1, files=log, all_fetched=ok),
          open(os.path.join(HERE, "fn4a_fetch.json"), "w"), indent=1)
with open(os.path.join(DST, "FETCH_LOG.md"), "w") as f:
    f.write("# FETCH_LOG (fn4a_ic1613_2026_11)\n\nOwner's approval 2026-11-04 (relayed by the lead with names and sizes), for lane FN4a "
            "(criteria a616530a1a). Exactly these files; the robust-weighting moment maps were not approved and were not fetched.\n\n"
            f"Attempt 1, {ATTEMPT1['start_utc']}: a plain GET of {ATTEMPT1['url']} returned a {ATTEMPT1['bytes']:,}-byte HTML page view "
            "(Plone), not the file. The fetch stopped; the HTML copy was deleted.\n\nAttempt 2:\n\n"
            "| file | URL used | UTC start | UTC end | bytes | sha256 |\n|---|---|---|---|---|---|\n")
    for x in log:
        if x["fetched"]:
            f.write(f"| {x['file']} | {x['url']} | {x['start_utc']} | {x['end_utc']} | {x['bytes']:,} | {x['sha256']} |\n")
        else:
            f.write(f"| {x['file']} | not fetched | | | | {x['reason']} |\n")
    f.write(f"\nEvery kept file equals its approved size. All approved files fetched: {ok}.\n")
sys.exit(0 if ok else 1)
