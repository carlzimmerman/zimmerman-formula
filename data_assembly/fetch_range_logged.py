#!/usr/bin/env python3
"""Capped, logged HTTP range-request helper for the owner-approved MIGHTEE-HI DR1 probe (the owner's explicit yes in the calc chat, 2026-10-02: "probe, cap 10 GB").

Importable (fetch_range) and a CLI:  python3 fetch_range_logged.py <label> <url> <start> <end> [--dest PATH]
  * ONLY the host archive-gw-1.kat.ac.za (the SARAO public archive named in the approval) is allowed; any other host is refused.
  * A CUMULATIVE hard cap (data_assembly/mightee_probe_2026-10-02/LEDGER.json, default 10,000,000,000 bytes, listings and landing pages counted) is enforced before every request; a request that would pass it is refused.
  * Each request asks for bytes=start-end, insists on HTTP 206 (a 200 full-file answer is aborted by --max-filesize), logs one JSON line (label, url, range, bytes, sha256, UTC time, Content-Range) in FETCH_MANIFEST_MIGHTEE_PROBE_2026-10-02.jsonl
    and one row in FETCH_LOG_MIGHTEE_PROBE_2026-10-02.md, and updates the ledger.
  * Never executes anything it downloads.
"""
import sys, os, json, hashlib, subprocess, datetime, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join(HERE, "mightee_probe_2026-10-02")
LEDGER = os.path.join(PROBE, "LEDGER.json")
MAN = os.path.join(PROBE, "FETCH_MANIFEST_MIGHTEE_PROBE_2026-10-02.jsonl")
LOGMD = os.path.join(PROBE, "FETCH_LOG_MIGHTEE_PROBE_2026-10-02.md")
ALLOWED_HOSTS = {"archive-gw-1.kat.ac.za"}
UA = "research-fetch/1.0 (scientific data retrieval for an open research repository)"


def _ledger():
    return json.load(open(LEDGER))


def fetch_range(label, url, start, end, dest=None, log=True):
    """Return the bytes of [start, end] (inclusive) of `url`; refuse on a foreign host or the cumulative cap; log it."""
    host = urllib.parse.urlparse(url).netloc
    if host not in ALLOWED_HOSTS:
        raise SystemExit(f"REFUSED: host {host} is not in the approved list {sorted(ALLOWED_HOSTS)}")
    n = end - start + 1
    led = _ledger()
    if led["used"] + n > led["cap"]:
        raise SystemExit(f"REFUSED: {n} bytes would pass the cumulative hard cap ({led['used']} used of {led['cap']})")
    cmd = ["curl", "-sS", "-L", "--max-time", "900", "--max-filesize", str(n), "-A", UA, "-H", f"Range: bytes={start}-{end}", "-D", "-", "-o", "-", url]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"FETCH FAILED (curl rc {r.returncode}): {r.stderr.decode()[:200]}")
    raw = r.stdout
    # curl -D - prints header blocks (one per redirect) then the body; split on the last header block
    parts = raw.split(b"\r\n\r\n")
    hdr_blocks = []; i = 0
    while i < len(parts) and parts[i].startswith(b"HTTP/"):
        hdr_blocks.append(parts[i]); i += 1
    body = b"\r\n\r\n".join(parts[i:]) if i < len(parts) else b""
    last = hdr_blocks[-1].decode(errors="replace") if hdr_blocks else ""
    status = last.split("\r\n")[0] if last else ""
    if " 206" not in status:
        raise SystemExit(f"REFUSED: expected HTTP 206, got '{status}'")
    crange = ""
    for ln in last.split("\r\n"):
        if ln.lower().startswith("content-range:"): crange = ln.split(":", 1)[1].strip()
    got = len(body)
    if got > n:
        raise SystemExit(f"REFUSED: received {got} > requested {n} bytes")
    led = _ledger(); led["used"] += got; led["requests"] += 1
    json.dump(led, open(LEDGER, "w"), indent=1)
    if dest:
        os.makedirs(os.path.dirname(dest), exist_ok=True); open(dest, "wb").write(body)
    if log:
        rec = dict(label=label, url=url, range=[start, end], bytes=got, sha256=hashlib.sha256(body).hexdigest(), http=status, content_range=crange, utc=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), cumulative_used=led["used"])
        open(MAN, "a").write(json.dumps(rec) + "\n")
        if not os.path.exists(LOGMD):
            open(LOGMD, "w").write("# MIGHTEE-HI DR1 probe: range-request log (the owner's yes, 2026-10-02: probe, cap 10 GB)\n\n| label | url | range | bytes | sha256 | cumulative bytes used |\n|---|---|---|---|---|---|\n")
        open(LOGMD, "a").write(f"| {label} | {url.split('/data/')[-1] if '/data/' in url else url} | {start}-{end} | {got} | `{rec['sha256'][:16]}…` | {led['used']} |\n")
    return body


if __name__ == "__main__":
    label, url, start, end = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    dest = sys.argv[sys.argv.index("--dest") + 1] if "--dest" in sys.argv else None
    b = fetch_range(label, url, start, end, dest)
    print(f"[{label}] OK: {len(b)} bytes of [{start}, {end}]")
