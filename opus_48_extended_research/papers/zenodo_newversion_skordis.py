#!/usr/bin/env python3
"""Publish a NEW VERSION of the Skordis-Zlosnik paper to its existing Zenodo record.
Usage: python zenodo_newversion_skordis.py <existing_record_id>
Token from /Users/carlzimmerman/new_physics/.env (never printed)."""
import json, os, sys, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
PDF = "pdf/WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.pdf"
META = "WHY_SKORDIS_AND_ZLOSNIK_WERE_RIGHT.zenodo.json"
BASE = "https://zenodo.org/api"

def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: token not found")

def req(method, url, tok, data=None, raw=None, ctype="application/json"):
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
            return resp.status, (json.loads(resp.read().decode() or "{}"))
    except urllib.error.HTTPError as e:
        return e.code, (json.loads(e.read().decode() or "{}"))

def main():
    rid = sys.argv[1]
    tok = token()
    meta = json.load(open(META))

    # 1) new version -> draft
    st, r = req("POST", f"{BASE}/deposit/depositions/{rid}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {r}")
    draft_url = r["links"].get("latest_draft") or r["links"].get("draft")
    st, d = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {d}")
    did = d["id"]; bucket = d["links"]["bucket"]
    print(f"new draft id = {did}")

    # 2) delete inherited files
    for f in d.get("files", []):
        fid = f.get("id")
        st, _ = req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{fid}", tok)
        print(f"  deleted old file {f.get('filename','?')} [{st}]")

    # 3) upload new PDF
    fn = os.path.basename(PDF)
    with open(PDF, "rb") as fh:
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
    if st not in (200, 201):
        sys.exit(f"upload failed [{st}]: {up}")
    print(f"uploaded {fn} ({up.get('size','?')} bytes)")

    # 4) metadata
    st, md = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")

    # 5) publish
    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok)
    if st not in (200, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    print(f"PUBLISHED v2 [{st}]  DOI = {pub.get('doi','?')}  URL = {pub.get('links',{}).get('record_html','?')}")
    print(f"concept DOI (all versions) = {pub.get('conceptdoi', pub.get('metadata',{}).get('conceptdoi','?'))}")

if __name__ == "__main__":
    main()
