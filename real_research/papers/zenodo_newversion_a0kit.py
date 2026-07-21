#!/usr/bin/env python3
"""Publish a NEW VERSION (v2) of the residual-doors paper (No Pump-Free Corner) on Zenodo.
Versions the existing record (concept DOI stays; a new version DOI is minted).
Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- NEVER printed.
Usage: python zenodo_newversion_nogo.py <existing_record_id>
       e.g. python zenodo_newversion_nogo.py 20949773
"""
import json, os, sys, urllib.request, urllib.error

ENV   = "/Users/carlzimmerman/new_physics/.env"
FILES = ["/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad/a0kit-1.0.1.zip"]
META  = "A0KIT_SOFTWARE.zenodo.json"
BASE  = "https://zenodo.org/api"

def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")

def req(method, url, tok, data=None, ctype="application/json", raw=None):
    headers = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode(); headers["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw; headers["Content-Type"] = ctype
    else:
        body = None
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python zenodo_newversion_nogo.py <existing_record_id>")
    rec = sys.argv[1]
    tok = token()
    meta = json.load(open(META))

    # 1. open a new version draft of the existing record
    st, dep = req("POST", f"{BASE}/deposit/depositions/{rec}/actions/newversion", tok)
    if st not in (200, 201): sys.exit(f"newversion failed [{st}]: {dep}")
    draft_url = dep["links"].get("latest_draft") or dep["links"].get("latest_draft_html")
    st, draft = req("GET", draft_url, tok)
    if st != 200: sys.exit(f"draft fetch failed [{st}]: {draft}")
    dep_id = draft["id"]; bucket = draft["links"]["bucket"]
    print(f"new-version draft id = {dep_id}")

    # 2. remove inherited files, then upload the fresh ones
    for f in draft.get("files", []):
        fid = f.get("id")
        if fid:
            req("DELETE", f"{BASE}/deposit/depositions/{dep_id}/files/{fid}", tok)
    for path in FILES:
        if not os.path.exists(path):
            print(f"  skip (missing): {path}"); continue
        fn = os.path.basename(path)
        with open(path, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
        if st not in (200, 201): sys.exit(f"upload failed [{st}] for {fn}: {up}")
        print(f"  uploaded {fn} ({up.get('size','?')} bytes)")

    # 3. metadata + publish
    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": meta})
    if st not in (200, 201): sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")
    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok)
    if st not in (200, 202): sys.exit(f"publish failed [{st}]: {pub}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    url = pub.get("links", {}).get("record_html") or pub.get("links", {}).get("latest_html", "?")
    conceptdoi = pub.get("conceptdoi", "?")
    print(f"PUBLISHED v2 [{st}]  version DOI = {doi}  concept DOI = {conceptdoi}  URL = {url}")

if __name__ == "__main__":
    main()
