#!/usr/bin/env python3
"""Publish the MNRAS submission (author's original version, tag mnras-v3.4) to Zenodo (production) as a preprint.
Gates: the PDF must be byte-identical to the one committed at tag mnras-v3.4 (the version submitted; never post a
refereed revision before acceptance), and paper_numbers.py must pass.
Reads ZENODO_ACCESS_TOKEN from the .env one directory above the repository -- NEVER printed.  The creator's ORCID is
read from the git-ignored author_private.tex if present (never committed).
Usage (run from qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/): python3 zenodo_publish_mnras_preprint.py
       on acceptance, a new version of the record: python3 zenodo_publish_mnras_preprint.py --newversion <record_id>
       check the gates without contacting Zenodo: python3 zenodo_publish_mnras_preprint.py --dry-run
       check the gates without contacting Zenodo: python3 zenodo_publish_mnras_preprint.py --dry-run
       (for the new version, update the PDF gate, the metadata description and add the journal DOI first)
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".env"))
PDF = "mnras_a0_lambda_v3.pdf"
META = "mnras_a0_lambda_v3.zenodo.json"
TAG = "mnras-v3.4"
REPO_PATH = "qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/" + PDF
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
    import subprocess, hashlib, re
    tagged = subprocess.run(["git", "show", f"{TAG}:{REPO_PATH}"], capture_output=True)
    if tagged.returncode != 0:
        sys.exit(f"ERROR: cannot read {REPO_PATH} at tag {TAG} -- not depositing")
    if hashlib.sha256(tagged.stdout).hexdigest() != hashlib.sha256(open(PDF, "rb").read()).hexdigest():
        sys.exit(f"ERROR: {PDF} differs from the submitted version at tag {TAG} -- not depositing")
    print(f"PDF is byte-identical to the submitted version (tag {TAG})")
    if subprocess.run([sys.executable, "paper_numbers.py"], capture_output=True).returncode != 0:
        sys.exit("ERROR: paper_numbers.py does not pass -- not depositing")
    print("paper_numbers.py passed (every quoted number re-derived)")
    tok = token()
    meta = json.load(open(META))
    meta = meta.get("metadata", meta)   # the series' .zenodo.json wraps the fields under "metadata"
    if os.path.exists("author_private.tex"):
        m = re.search(r"\\authororcid\}\{([0-9X-]{19})\}", open("author_private.tex").read())
        if m:
            meta["creators"][0]["orcid"] = m.group(1)
            print("creator ORCID attached from author_private.tex")
    if "--dry-run" in sys.argv:
        print(f"DRY RUN: gates pass; would deposit {PDF} as '{meta['title'][:60]}...' ({meta['publication_type']}) -- nothing sent")
        return
    if "--dry-run" in sys.argv:
        print(f"DRY RUN: gates pass; would deposit {PDF} as '{meta['title'][:60]}...' ({meta['publication_type']}) -- nothing sent")
        return
    if not all(meta.get(k) for k in ("title", "creators", "upload_type")):
        sys.exit("ERROR: metadata lacks title/creators/upload_type -- not depositing")

    # 1) create deposition, OR a new version of a published record (--newversion <record_id>), OR reuse a DRAFT id (argv[1])
    if "--newversion" in sys.argv:
        rid = sys.argv[sys.argv.index("--newversion") + 1]
        st, nv = req("POST", f"{BASE}/deposit/depositions/{rid}/actions/newversion", tok, tries=1)
        if st not in (200, 201):
            sys.exit(f"newversion failed [{st}]: {nv}")
        draft = nv["links"]["latest_draft"].rstrip("/").split("/")[-1]
        st, dep = req("GET", f"{BASE}/deposit/depositions/{draft}", tok, tries=6)
        if st != 200:
            sys.exit(f"cannot fetch new-version draft {draft} [{st}]")
        for f in dep.get("files", []):              # drop the files inherited from the previous version
            dst, _ = req("DELETE", f"{BASE}/deposit/depositions/{draft}/files/{f['id']}", tok, tries=4)
            print(f"  removed inherited {f.get('filename')!r} [{dst}]")
        st, dep = req("GET", f"{BASE}/deposit/depositions/{draft}", tok, tries=6)
        print(f"new-version draft {draft} of record {rid} (same concept DOI)")
    elif len(sys.argv) > 1:
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
    if md.get("metadata", {}).get("title") != meta["title"]:
        sys.exit("metadata PUT returned OK but the title did not stick -- refusing to publish")
    print("metadata attached (title confirmed on server)")

    # 4) publish. IRREVERSIBLE, so it is never auto-retried: a 504 here may mean the
    # record went live without us seeing the response. Verify state, then decide.
    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok, tries=1)
    if st not in (200, 202):
        print(f"publish returned [{st}]: {json.dumps(pub)[:600]} -- verifying whether it went live anyway")
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
