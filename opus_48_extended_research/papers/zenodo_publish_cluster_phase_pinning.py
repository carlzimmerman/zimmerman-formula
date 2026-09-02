#!/usr/bin/env python3
"""Publish CLUSTER_PHASE_PINNING_POLYTROPE.pdf to Zenodo (production), two-phase so the PDF carries its own DOI:
  1) create the deposition -> read the prereserved DOI;
  2) stamp that DOI into the paper's version line, rebuild the PDF;
  3) upload the PDF, attach metadata, publish (irreversible; HTTP 200/201/202 = success).
Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- NEVER printed.
Usage: python3 zenodo_publish_cluster_phase_pinning.py   (from papers/)
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
MD = "CLUSTER_PHASE_PINNING_POLYTROPE.md"
PDF = "pdf/CLUSTER_PHASE_PINNING_POLYTROPE.pdf"
META = "CLUSTER_PHASE_PINNING_POLYTROPE.zenodo.json"
BUILD = "build_cluster_phase_pinning_pdf.py"
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
    # 1) create deposition with a prereserved DOI
    st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={"metadata": {"prereserve_doi": True, "title": meta["title"], "upload_type": "publication", "publication_type": "preprint", "creators": meta["creators"], "description": meta["description"]}})
    if st not in (200, 201):
        sys.exit(f"create failed [{st}]: {dep}")
    dep_id = dep["id"]; bucket = dep["links"]["bucket"]
    doi = dep.get("metadata", {}).get("prereserve_doi", {}).get("doi") or f"10.5281/zenodo.{dep_id}"
    print(f"deposition id = {dep_id}; reserved DOI = {doi}")
    # 2) stamp the DOI into the paper and rebuild the PDF
    s = open(MD).read()
    new_line = f"*Version 2026-09-01 · Zenodo [{doi}](https://doi.org/{doi}). Companion to Zenodo [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562), two of whose statements this paper corrects (§7).*"
    s2, n = re.subn(r"\*Version 2026-09-01 · DRAFT, not yet deposited\. Companion to Zenodo \[10\.5281/zenodo\.20779562\]\(https://doi\.org/10\.5281/zenodo\.20779562\), two of whose statements this paper corrects \(§7\)\.\*", new_line, s)
    if n != 1:
        sys.exit("ERROR: version line not found/unique in the markdown; not publishing")
    open(MD, "w").write(s2)
    subprocess.run([sys.executable, BUILD], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"stamped DOI and rebuilt {PDF} ({os.path.getsize(PDF)} bytes)")
    # 3) upload, metadata, publish
    fn = os.path.basename(PDF)
    with open(PDF, "rb") as f:
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=f.read(), ctype="application/octet-stream")
    if st not in (200, 201):
        sys.exit(f"upload failed [{st}]: {up}")
    print(f"uploaded {fn} ({up.get('size','?')} bytes)")
    full = dict(meta); full["prereserve_doi"] = True
    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": full})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")
    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok)
    if st not in (200, 201, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    doi_pub = pub.get("doi") or pub.get("metadata", {}).get("doi", doi)
    url = pub.get("links", {}).get("record_html") or pub.get("links", {}).get("latest_html", f"https://doi.org/{doi_pub}")
    print(f"PUBLISHED [{st}]  DOI = {doi_pub}  URL = {url}")

if __name__ == "__main__":
    main()
