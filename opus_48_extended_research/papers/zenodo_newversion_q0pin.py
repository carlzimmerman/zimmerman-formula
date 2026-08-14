#!/usr/bin/env python3
"""Publish a NEW VERSION of the PINNING_Q0_IN_AEST record (rid 21935943).

Carries the guards the version-publishers earned the hard way, adapted for a first deposit:

  * LOCAL-PRESENCE  every file in the intended set must exist on disk before anything is created.
  * SCRIPTS-GREEN   every included .py must exit 0 when run, so no failing script ships as evidence.
  * NAME-EXACT      after upload, the server's file names must match the intended set exactly.
  * METADATA-SANE   title, version, creators and license must be present and non-empty.
  * NO-PII          the markdown and metadata are scanned for e-mail addresses and phone numbers;
                    the deposit is refused if any is found.
  * DRY-RUN default -- pass --publish to actually create and publish.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_newdeposit_rapidity_gap.py [--dry-run | --publish]
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
PAP = "opus_48_extended_research/papers"
RR = "real_research/reviews"
BASE = "https://zenodo.org/api"

STEM = "PINNING_Q0_IN_AEST"
RID = 21935943   # v7; v6 21855681, v5 21855374, v4 21855252, v3 21855217, v2 21855003, v1 21854915 (concept 21854914)
META_PATH = f"{PAP}/{STEM}.zenodo.json"

FILES = [
    f"{PAP}/{STEM}.md",
    "nbody_2026/stage58_x_to_q0_2026.py",
    "nbody_2026/stage58_ev_q0pin_lane_2026.py",
    "nbody_2026/stage56_xpin_verdict_2026.py",
    "nbody_2026/stage57_sz21_corrected_refile_2026.py",
    "nbody_2026/stage59_local_a0_verdict_2026.py",
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")


def _parse(b):
    try:
        return json.loads(b or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": (b or "")[:200]}


def req(method, url, tok, data=None, raw=None, ctype="application/json", tries=4):
    h = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw
        h["Content-Type"] = ctype
    else:
        body = None
    for i in range(tries):
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=240) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, pay = e.code, _parse(e.read().decode())
        except Exception as e:
            st, pay = 599, {"_exc": repr(e)[:200]}
        if st < 500 or i == tries - 1:
            return st, pay
        time.sleep(5 * (i + 1))


def guards():
    """Everything that must hold before a single byte is sent. Returns the metadata dict."""
    missing = [f for f in FILES + [META_PATH] if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} missing, refusing: {missing}")
    print(f"[guard] LOCAL-PRESENCE ok: {len(FILES)} files + metadata")

    meta = json.load(open(os.path.join(REPO, META_PATH)))
    meta = meta.get("metadata", meta)
    for k in ("title", "version", "creators", "license", "upload_type"):
        if not meta.get(k):
            sys.exit(f"ERROR: metadata field {k!r} missing or empty")
    if any("@" in json.dumps(c) for c in meta["creators"]):
        sys.exit("ERROR: an e-mail address appears in creators -- refusing")
    print(f"[guard] METADATA-SANE ok: {meta['title'][:60]!r} v{meta['version']}")

    md_files = [f for f in FILES if f.endswith(".md")]
    assert md_files, "no markdown in FILES -- the NO-PII scan needs one"
    blob = open(os.path.join(REPO, META_PATH)).read() + "".join(
        open(os.path.join(REPO, f), encoding="utf-8").read() for f in md_files)
    hits = EMAIL_RE.findall(blob) + PHONE_RE.findall(blob)
    if hits:
        sys.exit(f"ERROR: NO-PII guard tripped, {len(hits)} match(es): {sorted(set(hits))[:5]}")
    print("[guard] NO-PII ok: no e-mail or phone pattern in the paper or metadata")

    for rel in FILES:
        if not rel.endswith(".py"):
            continue
        p = os.path.join(REPO, rel)
        r = subprocess.run([sys.executable, p], cwd=REPO, capture_output=True, timeout=1800)
        tail = (r.stdout or b"").decode(errors="replace").strip().splitlines()[-1:] or [""]
        if r.returncode != 0:
            sys.exit(f"ERROR: SCRIPTS-GREEN failed for {rel} (exit {r.returncode}): {tail[0]}")
        print(f"[guard]   {os.path.basename(rel):48s} exit 0   {tail[0][:40]}")
    print("[guard] SCRIPTS-GREEN ok: every included script exits 0")
    return meta


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    if mode not in ("--dry-run", "--publish"):
        sys.exit("usage: python zenodo_newdeposit_rapidity_gap.py [--dry-run | --publish]")

    meta = guards()
    if mode == "--dry-run":
        print(f"\n[dry-run] all guards passed. Would create a NEW deposit with "
              f"{len(FILES)} files:")
        for f in FILES:
            print(f"    {os.path.basename(f)}")
        print("[dry-run] re-run with --publish to create and publish.")
        return 0

    tok = token()
    st, r = req("POST", f"{BASE}/deposit/depositions/{RID}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {r}")
    draft_url = r["links"].get("latest_draft") or r["links"].get("draft")
    st, d = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {d}")
    did, bucket = d["id"], d["links"]["bucket"]
    prev = str((d.get("metadata") or {}).get("version", ""))
    print(f"[pub] draft {did} from record {RID} (prev version {prev!r})")

    inherited = sorted(f.get("filename") for f in d.get("files", []))
    want_names = sorted(os.path.basename(f) for f in FILES)
    dropped = [n for n in inherited if n not in want_names]
    if dropped:
        sys.exit(f"ERROR: SUPERSET guard -- would DROP {dropped}")
    print(f"[pub] SUPERSET ok: all {len(inherited)} inherited files present in the new {len(FILES)}")
    for f in d.get("files", []):
        req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f.get('id')}", tok)
    if str(meta.get("version", "")) == prev:
        sys.exit(f"ERROR: version {prev!r} unchanged -- refusing")

    for rel in FILES:
        p = os.path.join(REPO, rel)
        fn = os.path.basename(p)
        with open(p, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(),
                         ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
    print(f"[pub] uploaded {len(FILES)}")

    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in FILES)
    if st != 200 or got != want:
        sys.exit(f"NAME-EXACT check FAILED\n  want {want}\n  got  {got}")
    print(f"[pub] verified {len(got)} files, names exact")

    st, md_ = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md_}")
    print("[pub] metadata attached")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok, tries=1)
    if st not in (200, 201, 202):
        st2, v = req("GET", f"{BASE}/deposit/depositions/{did}", tok, tries=6)
        if st2 == 200 and v.get("submitted"):
            pub = v
            print("[pub]   it DID publish; gateway dropped the response")
        else:
            sys.exit(f"publish failed [{st}]: {pub}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    cd = pub.get("conceptdoi") or pub.get("metadata", {}).get("conceptdoi", "?")
    print(f"[pub] PUBLISHED  version DOI {doi}  concept {cd}  files {len(got)}")
    print(f"[pub] https://zenodo.org/record/{did}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
