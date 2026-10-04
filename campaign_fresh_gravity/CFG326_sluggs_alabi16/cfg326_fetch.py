#!/usr/bin/env python3
"""CFG326 capped, logged fetch helper (owner's yes in the orchestrator chat, 2026-10-03: "yeah download Alabi+16 too boss" --
ONLY Alabi et al. 2016, its arXiv source/HTML and its VizieR tables).  CLI:  python3 cfg326_fetch.py <label> <url> <relative-dest-name>

  * Hosts: VizieR/CDS and arXiv only.  Cumulative hard cap 20 MB (this lane); any single file > 10 MB is aborted (curl --max-filesize) and logged as SKIPPED.
  * Files land in ../_external_data/sluggs_tracers/ (outside the repo; path stored RELATIVE to the repo root).
  * One JSON line per fetch (label, url, bytes, sha256, UTC) in FETCH_MANIFEST_CFG326.jsonl and one row in FETCH_LOG_CFG326.md (lane dir).
  * Never executes anything it downloads.
"""
import sys, os, json, hashlib, subprocess, datetime, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EXT_REL = os.path.join("..", "_external_data", "sluggs_tracers")
EXT = os.path.normpath(os.path.join(REPO, EXT_REL))
MAN = os.path.join(HERE, "FETCH_MANIFEST_CFG326.jsonl")
LOG = os.path.join(HERE, "FETCH_LOG_CFG326.md")
CAP, FILECAP = 20_000_000, 10_000_000
HOSTS = {"vizier.cds.unistra.fr", "cdsarc.cds.unistra.fr", "cdsarc.u-strasbg.fr", "vizier.u-strasbg.fr", "arxiv.org", "export.arxiv.org"}
UA = "research-fetch/1.0 (scientific data retrieval for an open research repository)"


def used():
    if not os.path.exists(MAN):
        return 0
    return sum(json.loads(l).get("bytes", 0) for l in open(MAN) if l.strip())


def fetch(label, url, name):
    host = urllib.parse.urlparse(url).netloc
    if host not in HOSTS:
        raise SystemExit(f"REFUSED host {host}")
    u = used()
    if u >= CAP:
        raise SystemExit(f"REFUSED: cap reached ({u})")
    dest = os.path.join(EXT, name); os.makedirs(os.path.dirname(dest), exist_ok=True)
    lim = min(FILECAP, CAP - u)
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "300", "--max-filesize", str(lim), "-A", UA, "-o", dest, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    status = r.stdout.strip()
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if r.returncode != 0 or not os.path.exists(dest):
        rec = dict(label=label, url=url, file=None, bytes=0, sha256=None, utc=t, status=f"FAILED rc={r.returncode} http={status} {r.stderr.strip()[:120]}")
        if os.path.exists(dest):
            os.remove(dest)
    else:
        b = open(dest, "rb").read()
        rec = dict(label=label, url=url, file=os.path.join(EXT_REL, name), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), utc=t, status=f"http {status}")
    open(MAN, "a").write(json.dumps(rec) + "\n")
    new = not os.path.exists(LOG)
    with open(LOG, "a") as fh:
        if new:
            fh.write("# CFG326 fetch log (owner's yes 2026-10-03, Alabi+16 only; cap 20 MB, 10 MB per file; paths relative to the repo root)\n\n| UTC | label | url | file | bytes | sha256 | status |\n|---|---|---|---|---|---|---|\n")
        fh.write(f"| {t} | {label} | {url} | {rec['file']} | {rec['bytes']} | {rec['sha256']} | {rec['status']} |\n")
    print(json.dumps(rec))
    return rec


if __name__ == "__main__":
    fetch(sys.argv[1], sys.argv[2], sys.argv[3])
