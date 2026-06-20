#!/usr/bin/env python3
"""Publish WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.pdf to Zenodo (production).
Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- NEVER printed.
Usage: python zenodo_publish_skordis.py
"""
import json, os, sys, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
PDF = "pdf/WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.pdf"
META = "WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.zenodo.json"
BASE = "https://zenodo.org/api"

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

    # 2) upload the PDF into the bucket
    fn = os.path.basename(PDF)
    with open(PDF, "rb") as f:
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=f.read(), ctype="application/octet-stream")
    if st not in (200, 201):
        sys.exit(f"upload failed [{st}]: {up}")
    print(f"uploaded {fn} ({up.get('size','?')} bytes)")

    # 3) attach metadata
    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")

    # 4) publish (irreversible)
    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok)
    if st not in (200, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    url = pub.get("links", {}).get("record_html") or pub.get("links", {}).get("latest_html", "?")
    print(f"PUBLISHED [{st}]  DOI = {doi}  URL = {url}")

if __name__ == "__main__":
    main()
