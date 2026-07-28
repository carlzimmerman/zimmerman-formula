#!/usr/bin/env python3
"""Publish PAPER_ATOMOS_NULL.pdf to Zenodo (production).
Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- NEVER printed.
Usage: python zenodo_publish_atomos_null.py
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
PDF = "pdf/PAPER_ATOMOS_NULL.pdf"
META = "PAPER_ATOMOS_NULL.zenodo.json"
BASE = "https://zenodo.org/api"

def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")

def _parse(body):
    """Zenodo returns HTML on 5xx/gateway errors -- never let that raise."""
    try:
        return json.loads(body or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": body[:200]}

def req(method, url, tok, data=None, ctype="application/json", raw=None, tries=4):
    headers = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode(); headers["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw; headers["Content-Type"] = ctype
    else:
        body = None
    for attempt in range(tries):
        r = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(r, timeout=180) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, payload = e.code, _parse(e.read().decode())
        except Exception as e:            # socket timeout / reset
            st, payload = 599, {"_exc": repr(e)[:200]}
        # retry only on transient server-side failures; never on 4xx
        if st < 500 or attempt == tries - 1:
            return st, payload
        wait = 5 * (attempt + 1)
        print(f"  transient [{st}] on {method} -- retrying in {wait}s")
        time.sleep(wait)

def main():
    tok = token()
    meta = json.load(open(META))

    # 1) create deposition (or reuse an existing DRAFT id passed as argv[1])
    if len(sys.argv) > 1:
        st, dep = req("GET", f"{BASE}/deposit/depositions/{sys.argv[1]}", tok)
        if st != 200:
            sys.exit(f"reuse fetch failed [{st}]: {dep}")
        print(f"reusing draft deposition {sys.argv[1]}")
    else:
        st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={})
        if st not in (200, 201):
            sys.exit(f"create failed [{st}]: {dep}")
    dep_id = dep["id"]; bucket = dep["links"]["bucket"]
    print(f"deposition id = {dep_id}")

    # 2) upload the PDF into the bucket.
    # Zenodo can 504 on the PUT and still have stored the object, so never trust
    # the PUT status -- confirm from the server's own file list, by size.
    fn = os.path.basename(PDF)
    blob = open(PDF, "rb").read()
    want = len(blob)

    def landed():
        st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok)
        if st != 200:
            return None
        for f in d.get("files", []):
            if f.get("filename") == fn and f.get("filesize") == want:
                return True
        return False

    for attempt in range(1, 9):
        if landed():
            print(f"confirmed on server: {fn} ({want} bytes)")
            break
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=blob,
                     ctype="application/octet-stream", tries=1)
        if landed():
            print(f"uploaded {fn} ({want} bytes) [PUT returned {st}]")
            break
        # Zenodo reports a broken file-transfer backend as HTTP 400 with
        # "The file upload transfer failed, please try again." -- a RETRYABLE
        # server-side fault wearing a 4xx code. Log the message, not just the
        # status, or this is indistinguishable from a malformed request.
        msg = up.get("message") or up.get("_nonjson") or up.get("_exc") or ""
        wait = min(20 * attempt, 90)
        print(f"  upload attempt {attempt} not confirmed (PUT {st}: {msg[:80]}) -- retrying in {wait}s")
        time.sleep(wait)
    else:
        sys.exit("upload never confirmed after 8 attempts -- Zenodo degraded, rerun later "
                 f"with: python {os.path.basename(__file__)} {dep_id}")

    # 2b) refuse to publish a contaminated record. A 504 on an upload can still store
    # the object, so diagnostic probes may have landed invisibly. Delete anything
    # that is not the paper before this goes live.
    st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
    if st != 200:
        sys.exit(f"cannot verify file list before publish [{st}] -- refusing to publish blind")
    strays = [f for f in d.get("files", []) if f.get("filename") != fn]
    for s in strays:
        sid = s.get("id")
        dst, _ = req("DELETE", f"{BASE}/deposit/depositions/{dep_id}/files/{sid}", tok, tries=4)
        print(f"  removed stray file {s.get('filename')!r} [{dst}]")
    if strays:
        st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        names = [f.get("filename") for f in d.get("files", [])]
        if st != 200 or names != [fn]:
            sys.exit(f"stray files remain ({names}) -- refusing to publish")
    print(f"file list clean: {[f.get('filename') for f in d.get('files', [])]}")

    # 3) attach metadata (idempotent -- safe to retry)
    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": meta}, tries=6)
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")

    # 4) publish. IRREVERSIBLE, so it is never auto-retried: a 504 here may mean the
    # record went live without us seeing the response. Verify state, then decide.
    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok, tries=1)
    if st not in (200, 202):
        print(f"publish returned [{st}] -- verifying whether it went live anyway")
        vst, vd = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        if vst == 200 and vd.get("submitted"):
            pub = vd
            print("  it DID publish; the gateway just dropped the response")
        else:
            sys.exit(f"NOT published (state={vd.get('state')!r}). File is uploaded; rerun with: "
                     f"python {os.path.basename(__file__)} {dep_id}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    url = pub.get("links", {}).get("record_html") or pub.get("links", {}).get("latest_html", "?")
    print(f"PUBLISHED  DOI = {doi}  URL = {url}")

if __name__ == "__main__":
    main()
