#!/usr/bin/env python3
"""Logged, capped fetch helper for the 2026-10-01 owner-approved downloads (the owner's explicit yes in the calc chat).

Usage: python3 fetch_logged.py <label> <url> <dest_path> <cap_bytes> [--extract-dir DIR] [--resume]
  * HEAD first (reports the advertised size), refuses if the advertised size exceeds the hard cap, then GETs with curl --max-filesize.
  * Appends one JSON line to data_assembly/FETCH_MANIFEST_2026-10-01.jsonl (label, url, final url, dest, bytes, sha256, UTC time, http status, content-type)
    and one row to data_assembly/FETCH_LOG_2026-10-01.md.
  * Never executes anything it downloads; --extract-dir only untars/gunzips after listing the members and refusing absolute or '..' paths.
"""
import sys, os, json, hashlib, subprocess, time, tarfile, gzip, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(HERE, "FETCH_MANIFEST_2026-10-01.jsonl")
LOGMD = os.path.join(HERE, "FETCH_LOG_2026-10-01.md")
UA = "research-fetch/1.0 (scientific data retrieval for an open research repository)"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()


def head(url):
    r = subprocess.run(["curl", "-sIL", "--max-time", "40", "-A", UA, url], capture_output=True, text=True)
    blocks = [b for b in r.stdout.replace("\r", "").split("\n\n") if b.strip()]
    last = blocks[-1] if blocks else ""
    hdr = {}
    for ln in last.split("\n")[1:]:
        if ":" in ln:
            k, v = ln.split(":", 1); hdr[k.strip().lower()] = v.strip()
    status = last.split("\n")[0] if last else ""
    return status, hdr


def main():
    label, url, dest, cap = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    extract = None
    if "--extract-dir" in sys.argv:
        extract = sys.argv[sys.argv.index("--extract-dir") + 1]
    status, hdr = head(url)
    adv = int(hdr.get("content-length", "-1")) if hdr.get("content-length", "").isdigit() else -1
    print(f"[{label}] HEAD: {status}; content-type {hdr.get('content-type')}; advertised bytes {adv}; hard cap {cap}")
    if adv > cap:
        print(f"[{label}] REFUSED: advertised size {adv} exceeds the cap {cap}"); sys.exit(3)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    cmd = ["curl", "-sL", "--fail", "--max-time", "900", "--max-filesize", str(cap), "-A", UA, "-o", tmp, "-w", "%{http_code} %{url_effective}", url]
    if "--resume" in sys.argv and os.path.exists(tmp):
        cmd[1:1] = ["-C", "-"]                                              # resume a stalled partial download
        print(f"[{label}] resuming from {os.path.getsize(tmp)} bytes")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(tmp):
        print(f"[{label}] FETCH FAILED (curl rc {r.returncode}): {r.stderr.strip()[:200]}"); sys.exit(4)
    os.replace(tmp, dest)
    nbytes = os.path.getsize(dest); digest = sha256(dest)
    code, _, final = r.stdout.partition(" ")
    rec = dict(label=label, url=url, final_url=final, dest=dest.replace(os.path.dirname(HERE) + "/", "<repo-parent>/"), bytes=nbytes, sha256=digest, http=code, content_type=hdr.get("content-type"), advertised=adv, cap=cap,
               utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    with open(MAN, "a") as f:
        f.write(json.dumps(rec) + "\n")
    new = not os.path.exists(LOGMD)
    with open(LOGMD, "a") as f:
        if new:
            f.write("# Owner-approved downloads, 2026-10-01 (the owner's explicit yes in the calc chat)\n\nEach row: label, URL, bytes, sha256, destination. Nothing downloaded is executed. Caps are hard (curl --max-filesize).\n\n| label | URL | bytes | sha256 | destination |\n|---|---|---|---|---|\n")
        f.write(f"| {label} | {url} | {nbytes} | `{digest}` | `{rec['dest']}` |\n")
    print(f"[{label}] OK: {nbytes} bytes, sha256 {digest}")
    if extract:
        os.makedirs(extract, exist_ok=True)
        try:
            with tarfile.open(dest) as tf:
                names = tf.getnames()
                bad = [n for n in names if n.startswith("/") or ".." in n.split("/")]
                if bad:
                    print(f"[{label}] extraction REFUSED: unsafe member paths {bad[:3]}"); sys.exit(5)
                tf.extractall(extract)
            print(f"[{label}] extracted {len(names)} members to {extract}")
        except tarfile.ReadError:
            with gzip.open(dest, "rb") as g, open(os.path.join(extract, "main.tex"), "wb") as o:
                shutil.copyfileobj(g, o)
            print(f"[{label}] single gzip file extracted to {extract}/main.tex")


if __name__ == "__main__":
    main()
