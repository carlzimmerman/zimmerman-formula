#!/usr/bin/env python3
"""Create, publish, or issue a NEW VERSION of the 2026-09-06 Zenodo deposit for PAPER7 (the decisive a0(z) measurement).  DRY-RUN by default; --publish to create+publish.
Reads ZENODO_ACCESS_TOKEN from ~/new_physics/.env -- never printed.  Same guards and API calls as zenodo_publish_papers_2026.py."""
import os, sys, json, re, urllib.request
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); ENV = os.path.expanduser("~/new_physics/.env"); BASE = "https://zenodo.org/api"
DEP = dict(stem="PAPER7_a0z_decisive_measurement_2026", meta="qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.zenodo.json",
           files=["qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.pdf", "qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.tex"])
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}"); PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")
def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN"): return line.split("=", 1)[1].strip()
    sys.exit("FATAL: ZENODO_ACCESS_TOKEN not found in .env")
def api(tok, method, path, data=None, headers=None, raw=False):
    url = f"{BASE}{path}{'&' if '?' in path else '?'}access_token={tok}"
    body = data if raw else (json.dumps(data).encode() if data is not None else None)
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        body = r.read()
        return json.loads(body) if body else {}                     # DELETE returns 204 with an empty body
def guard(dep):
    ok = all(os.path.exists(os.path.join(REPO, f)) for f in dep["files"] + [dep["meta"]]); print(f"  [{'ok' if ok else 'FAIL'}] LOCAL-PRESENCE")
    meta = json.load(open(os.path.join(REPO, dep["meta"])))["metadata"]
    ok2 = all(meta.get(k) for k in ("title", "version", "creators", "license")); print(f"  [{'ok' if ok2 else 'FAIL'}] METADATA-SANE")
    blob = json.dumps(meta) + open(os.path.join(REPO, dep["files"][1]), errors="ignore").read()
    hits = [m for m in EMAIL_RE.findall(blob) if "noreply" not in m] + PHONE_RE.findall(blob); print(f"  [{'ok' if not hits else 'FAIL'}] NO-PII ({len(hits)})")
    return ok and ok2 and not hits
def newversion(dep, tok, rec_id):
    """Publish a NEW VERSION of an existing record: same concept DOI, new version DOI."""
    nv = api(tok, "POST", f"/deposit/depositions/{rec_id}/actions/newversion")
    draft = nv["links"]["latest_draft"].split("/")[-1]; print(f"  new-version draft {draft}")
    d = api(tok, "GET", f"/deposit/depositions/{draft}")
    for f in d.get("files", []):
        api(tok, "DELETE", f"/deposit/depositions/{draft}/files/{f['id']}"); print(f"    removed inherited {f['filename']}")
    d = api(tok, "GET", f"/deposit/depositions/{draft}"); bucket = d["links"]["bucket"]
    for f in dep["files"]:
        with open(os.path.join(REPO, f), "rb") as fh:
            api(tok, "PUT", f"{bucket.replace(BASE, '')}/{os.path.basename(f)}", fh.read(), headers={"Content-Type": "application/octet-stream"}, raw=True)
        print(f"    uploaded {os.path.basename(f)}")
    meta = json.load(open(os.path.join(REPO, dep["meta"])))
    api(tok, "PUT", f"/deposit/depositions/{draft}", meta)
    server = {x["filename"] for x in api(tok, "GET", f"/deposit/depositions/{draft}")["files"]}; want = {os.path.basename(f) for f in dep["files"]}
    if server != want: sys.exit(f"FATAL NAME-EXACT: {server ^ want}")
    pub = api(tok, "POST", f"/deposit/depositions/{draft}/actions/publish")
    print(f"  PUBLISHED v2: doi={pub['doi']}  concept={pub.get('conceptdoi', '')}"); return pub["doi"]

def publish(dep, tok):
    meta = json.load(open(os.path.join(REPO, dep["meta"]))); d = api(tok, "POST", "/deposit/depositions", meta); dep_id, bucket = d["id"], d["links"]["bucket"]
    print(f"  created deposition {dep_id}")
    for f in dep["files"]:
        with open(os.path.join(REPO, f), "rb") as fh: api(tok, "PUT", f"{bucket.replace(BASE, '')}/{os.path.basename(f)}", fh.read(), headers={"Content-Type": "application/octet-stream"}, raw=True)
        print(f"    uploaded {os.path.basename(f)}")
    server = {x["filename"] for x in api(tok, "GET", f"/deposit/depositions/{dep_id}")["files"]}; want = {os.path.basename(f) for f in dep["files"]}
    if server != want: sys.exit(f"FATAL NAME-EXACT: {server ^ want}")
    pub = api(tok, "POST", f"/deposit/depositions/{dep_id}/actions/publish"); print(f"  PUBLISHED: doi={pub['doi']}  concept={pub.get('conceptdoi', '')}"); return pub["doi"]
if __name__ == "__main__":
    print(f"== {DEP['stem']}")
    if not guard(DEP): sys.exit(1)
    if "--newversion" in sys.argv:
        rid = sys.argv[sys.argv.index("--newversion") + 1]; print("DOI:", newversion(DEP, token(), rid))
    elif "--publish" in sys.argv: print("DOI:", publish(DEP, token()))
    else: print("  DRY-RUN ok (pass --publish to create+publish, or --newversion <record_id>)")
