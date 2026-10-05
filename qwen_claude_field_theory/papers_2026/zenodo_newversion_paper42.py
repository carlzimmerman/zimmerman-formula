#!/usr/bin/env python3
"""New version of PAPER42 on Zenodo (concept of record 23171066). Reads ZENODO_ACCESS_TOKEN from the owner's .env -- NEVER printed.
Creates a new-version draft, replaces its files with the current PDF/tex/figure, attaches the current .zenodo.json metadata, publishes (irreversible)."""
import json, os, sys, urllib.request, urllib.error
ENV = os.path.join(os.path.expanduser("~"), "new_physics", ".env")
BASE = "https://zenodo.org/api"; OLD = 23171066
FILES = ["PAPER42_mond_vacuum_dark_energy_2026.pdf", "PAPER42_mond_vacuum_dark_energy_2026.tex", "fig1_paper42_band.pdf"]
META = "PAPER42_mond_vacuum_dark_energy_2026.zenodo.json"
def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: token not found")
def req(method, url, tok, data=None, raw=None):
    h = {"Authorization": f"Bearer {tok}"}; body = None
    if data is not None: body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    elif raw is not None: body = raw; h["Content-Type"] = "application/octet-stream"
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            t = resp.read().decode(); return resp.status, (json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        t = e.read().decode(); return e.code, (json.loads(t) if t.strip().startswith("{") else {"raw": t[:300]})
tok = token()
st, nv = req("POST", f"{BASE}/deposit/depositions/{OLD}/actions/newversion", tok)
if st not in (200, 201): sys.exit(f"newversion failed [{st}]: {nv}")
draft_url = nv["links"]["latest_draft"]
st, d = req("GET", draft_url, tok)
if st != 200: sys.exit(f"draft fetch failed [{st}]: {d}")
did = d["id"]; bucket = d["links"]["bucket"]; print(f"new-version draft id = {did}")
for f in d.get("files", []):
    st, _ = req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f['id']}", tok); print(f"  removed old file {f['filename']} [{st}]")
for p in FILES:
    with open(p, "rb") as fh:
        st, up = req("PUT", f"{bucket}/{os.path.basename(p)}", tok, raw=fh.read())
    if st not in (200, 201): sys.exit(f"upload failed [{st}] {p}: {up}")
    print(f"  uploaded {p} ({up.get('size','?')} bytes)")
meta = json.load(open(META)); meta.setdefault("publication_date", d.get("metadata", {}).get("publication_date"))
st, md = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
if st not in (200, 201): sys.exit(f"metadata failed [{st}]: {md}")
st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok)
if st not in (200, 202): sys.exit(f"publish failed [{st}]: {pub}")
print(f"PUBLISHED [{st}]  DOI = {pub.get('doi')}  concept DOI = {pub.get('conceptdoi')}  URL = {pub.get('links', {}).get('record_html') or pub.get('links', {}).get('html')}")
