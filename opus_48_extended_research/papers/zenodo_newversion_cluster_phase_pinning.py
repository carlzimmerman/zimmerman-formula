#!/usr/bin/env python3
"""Publish VERSION 2 of the cluster polytrope paper (v1 record 22242701) as a Zenodo NEW VERSION, two-phase so the
PDF carries its own v2 DOI:
  1) POST newversion on the v1 record -> draft -> read the draft's prereserved DOI;
  2) stamp that DOI into the paper's version line, rebuild the PDF;
  3) drop the inherited v1 file, upload the v2 PDF, NAME-EXACT check, attach metadata (version must differ), publish.
Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- NEVER printed.
Guards: version bump required; empty/non-JSON replies never crash a half-done draft; a dropped publish response is re-checked.
Usage: python3 zenodo_newversion_cluster_phase_pinning.py   (from papers/)
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
MD = "CLUSTER_PHASE_PINNING_POLYTROPE.md"
PDF = "pdf/CLUSTER_PHASE_PINNING_POLYTROPE.pdf"
META = "CLUSTER_PHASE_PINNING_POLYTROPE.zenodo.json"
BUILD = "build_cluster_phase_pinning_pdf.py"
BASE = "https://zenodo.org/api"
RID_V1 = 22242701

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
            txt = resp.read().decode(); st = resp.status
    except urllib.error.HTTPError as e:
        txt = e.read().decode(); st = e.code
    try:
        return st, (json.loads(txt) if txt.strip() else {})
    except ValueError:
        return st, {"_nonjson_body": txt[:300]}

def main():
    tok = token()
    meta = json.load(open(META))
    # 1) new version draft
    st, r = req("POST", f"{BASE}/deposit/depositions/{RID_V1}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {r}")
    draft_url = r["links"].get("latest_draft") or r["links"].get("draft")
    st, d = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {d}")
    did, bucket = d["id"], d["links"]["bucket"]
    prev = str((d.get("metadata") or {}).get("version", ""))
    doi = (d.get("metadata") or {}).get("prereserve_doi", {}).get("doi") or f"10.5281/zenodo.{did}"
    print(f"draft {did} from record {RID_V1} (prev version {prev!r}); reserved v2 DOI = {doi}")
    if str(meta.get("version", "")) == prev:
        sys.exit(f"ERROR: version {prev!r} unchanged -- refusing")
    # 2) stamp + rebuild
    s = open(MD).read()
    s2, n = re.subn(r"\*Version 2026-09-02 \(v2\) · DRAFT v2, not yet deposited\. ",
                    f"*Version 2026-09-02 (v2) · Zenodo [{doi}](https://doi.org/{doi}). ", s, count=1)
    if n != 1:
        sys.exit("ERROR: v2 draft version line not found/unique; not publishing")
    open(MD, "w").write(s2)
    subprocess.run([sys.executable, BUILD], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"stamped v2 DOI and rebuilt {PDF} ({os.path.getsize(PDF)} bytes)")
    # 3) replace the file
    for f in d.get("files", []):
        st, _ = req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f.get('id')}", tok)
        print(f"dropped inherited file {f.get('filename')} [{st}]")
    fn = os.path.basename(PDF)
    with open(PDF, "rb") as fh:
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
    if st not in (200, 201):
        sys.exit(f"upload failed [{st}]: {up}")
    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    if st != 200 or got != [fn]:
        sys.exit(f"NAME-EXACT check FAILED: got {got}")
    print(f"uploaded {fn} ({up.get('size', '?')} bytes); files on server: {got}")
    full = dict(meta); full["prereserve_doi"] = True
    st, md_ = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": full})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md_}")
    print(f"metadata attached (version {full['version']}, {len(full.get('keywords', []))} keywords)")
    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok)
    if st not in (200, 201, 202):
        st2, v = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
        if st2 == 200 and v.get("submitted"):
            pub = v; print("publish reply dropped by the gateway, but the record IS submitted")
        else:
            sys.exit(f"publish failed [{st}]: {pub}")
    doi_pub = pub.get("doi") or pub.get("metadata", {}).get("doi", doi)
    cd = pub.get("conceptdoi") or pub.get("metadata", {}).get("conceptdoi", "?")
    print(f"PUBLISHED  v2 DOI = {doi_pub}  concept DOI = {cd}  https://zenodo.org/record/{did}")

if __name__ == "__main__":
    main()
