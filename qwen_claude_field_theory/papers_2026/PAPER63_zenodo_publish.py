#!/usr/bin/env python3
"""Publish PAPER63_where_cold_dark_energy_switches_on_2026.pdf to Zenodo (production). Run only after: build && PAPER63_audit.py exits 0.
The owner runs this ONCE. It is not run by the drafting session.
GUARD: main() first refuses while the TeX still carries a "% PENDING" placeholder (a lane result not yet folded in),
then runs PAPER63_audit.py and refuses to touch Zenodo unless it exits 0.
Reads ZENODO_ACCESS_TOKEN from the workspace .env two levels above this file -- NEVER printed.
Usage: python PAPER63_zenodo_publish.py --check              run both gates only; never reads the token or contacts Zenodo
       python PAPER63_zenodo_publish.py                      new record (v1/v2 flow)
       python PAPER63_zenodo_publish.py DRAFT_ID             resume an existing draft
       python PAPER63_zenodo_publish.py --newversion REC_ID [--meta FILE]
           new VERSION of published record REC_ID under the same concept DOI: the inherited
           files are removed from the draft before the new PDF is uploaded.
"""
import json, os, subprocess, sys, time, urllib.request, urllib.error

ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER63_where_cold_dark_energy_switches_on_2026.pdf")
META = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER63_where_cold_dark_energy_switches_on_2026.zenodo.json")
if "--meta" in sys.argv:
    META = sys.argv[sys.argv.index("--meta") + 1]
BASE = "https://zenodo.org/api"
AUDIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER63_audit.py")
TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER63_where_cold_dark_energy_switches_on_2026.tex")


def pending_gate():
    """Refuse to publish a draft that still carries a pending-lane placeholder."""
    left = [l.strip() for l in open(TEX, encoding="utf-8") if l.startswith("% PENDING")]
    if left:
        sys.exit(f"REFUSING TO PUBLISH: pending placeholders remain in the TeX: {left} -- fold the lane in, rebuild, re-audit")
    print("pending gate passed: no placeholder left")


def audit_gate():
    """Refuse to publish unless the paper's audit passes (exit 0) on the PDF that would be uploaded."""
    r = subprocess.run([sys.executable, AUDIT], capture_output=True, text=True, cwd=os.path.dirname(AUDIT))
    lines = r.stdout.strip().splitlines()
    last = lines[-1] if lines else "(no output)"
    if r.returncode != 0:
        sys.exit(f"REFUSING TO PUBLISH: {os.path.basename(AUDIT)} exited {r.returncode} -- {last}")
    print(f"audit gate passed: {last}")

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
    pending_gate()                         # never deposit a draft with an unfolded lane
    audit_gate()                           # never contact Zenodo unless the audit exits 0
    if "--check" in sys.argv:
        print("--check: gates passed; Zenodo not contacted, token not read")
        return
    tok = token()
    meta = json.load(open(META))
    meta = meta.get("metadata", meta)      # the .zenodo.json files wrap the fields in a top-level 'metadata' key

    # 1) create deposition, a new version of a published record, or reuse a DRAFT id
    if "--newversion" in sys.argv:
        rec = sys.argv[sys.argv.index("--newversion") + 1]
        st, nv = req("POST", f"{BASE}/deposit/depositions/{rec}/actions/newversion", tok, tries=1)
        if st not in (200, 201):
            sys.exit(f"newversion failed [{st}]: {nv}")
        draft_url = nv["links"]["latest_draft"]
        st, dep = req("GET", draft_url, tok, tries=6)
        if st != 200:
            sys.exit(f"cannot fetch new-version draft [{st}]: {dep}")
        print(f"new-version draft {dep['id']} of record {rec} -- rerun with this id if anything below fails")
        for f in dep.get("files", []):   # the inherited previous-version files
            dst, _ = req("DELETE", f"{BASE}/deposit/depositions/{dep['id']}/files/{f['id']}", tok, tries=4)
            print(f"  removed inherited file {f.get('filename')!r} [{dst}]")
        st, dep = req("GET", f"{BASE}/deposit/depositions/{dep['id']}", tok, tries=6)
        if st != 200 or dep.get("files"):
            sys.exit(f"inherited files remain ({[f.get('filename') for f in dep.get('files', [])]}) -- refusing to continue")
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
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
