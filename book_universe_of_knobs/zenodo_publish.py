#!/usr/bin/env python3
"""Publish universe_of_knobs.pdf to Zenodo, on the owner's request of 2026-11-05.
GUARD: every Zenodo step first rebuilds the book and runs book_audit.py, and refuses unless both pass.
Reads ZENODO_ACCESS_TOKEN from the workspace .env two levels above this folder; the token is NEVER printed.
Forces IPv4: IPv6 connections to Zenodo hang from this network.

Usage: python3 zenodo_publish.py --check      build and audit only; never reads the token or contacts Zenodo
       python3 zenodo_publish.py --reserve    create a draft, reserve its DOI, write zenodo_draft.json
       python3 zenodo_publish.py DRAFT_ID     upload the PDF to that draft, attach metadata, publish
                                              (refuses unless front.tex carries the reserved DOI)
"""
import json, os, re, socket, subprocess, sys, time, urllib.request, urllib.error

_orig = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, type=0, proto=0, flags=0: _orig(host, port, socket.AF_INET, type, proto, flags)

HERE = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(HERE, "..", "..", ".env")
PDF = os.path.join(HERE, "universe_of_knobs.pdf")
TEX = os.path.join(HERE, "universe_of_knobs.tex")
META = os.path.join(HERE, "universe_of_knobs.zenodo.json")
DRAFT = os.path.join(HERE, "zenodo_draft.json")
BASE = "https://zenodo.org/api"


def build_gate():
    r = subprocess.run(["tectonic", "-X", "compile", "--keep-logs", TEX], cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("REFUSING: the book did not build\n" + r.stderr[-800:])
    log = open(os.path.join(HERE, "universe_of_knobs.log"), errors="ignore").read()
    os.remove(os.path.join(HERE, "universe_of_knobs.log"))
    m = re.search(r"\((\d+) pages", log)
    pages = int(m.group(1)) if m else 0
    if pages < 150 or "Overfull \\hbox" in log:
        sys.exit(f"REFUSING: build check failed (pages {pages}, overfull lines present: {'Overfull' in log})")
    newest = max(os.path.getmtime(p) for p in
                 [os.path.join(HERE, f) for f in os.listdir(HERE) if f.endswith(".tex")] +
                 [os.path.join(HERE, "figures", f) for f in os.listdir(os.path.join(HERE, "figures"))])
    if os.path.getmtime(PDF) < newest:
        sys.exit("REFUSING: the PDF is older than its sources")
    print(f"build gate passed: {pages} pages, no overfull lines, PDF newer than every source")


def audit_gate():
    r = subprocess.run([sys.executable, os.path.join(HERE, "book_audit.py")], capture_output=True, text=True, cwd=HERE)
    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    if r.returncode != 0:
        sys.exit(f"REFUSING: book_audit.py exited {r.returncode}: {last}")
    print(f"audit gate passed: {last}")


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")


def _parse(body):
    try:
        return json.loads(body or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": body[:200]}


def req(method, url, tok, data=None, ctype="application/json", raw=None, tries=4):
    headers = {"Authorization": f"Bearer {tok}"}
    body = None
    if data is not None:
        body = json.dumps(data).encode(); headers["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw; headers["Content-Type"] = ctype
    for attempt in range(tries):
        r = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(r, timeout=180) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, payload = e.code, _parse(e.read().decode())
        except Exception as e:
            st, payload = 599, {"_exc": repr(e)[:200]}
        if st < 500 or attempt == tries - 1:
            return st, payload
        wait = 5 * (attempt + 1)
        print(f"  transient [{st}] on {method}, retrying in {wait}s")
        time.sleep(wait)


def reserve(tok):
    st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={})
    if st not in (200, 201):
        sys.exit(f"create failed [{st}]: {dep}")
    pre = dep.get("metadata", {}).get("prereserve_doi", {})
    if not pre.get("doi"):
        sys.exit(f"draft {dep['id']} created but no reserved DOI was returned: {dep.get('metadata')}")
    json.dump({"draft_id": dep["id"], "doi": pre["doi"], "recid": pre.get("recid")}, open(DRAFT, "w"), indent=2)
    print(f"draft {dep['id']} created; reserved DOI {pre['doi']} (written to zenodo_draft.json)")


def publish(tok, dep_id):
    reserved = json.load(open(DRAFT))["doi"]
    if reserved not in open(os.path.join(HERE, "front.tex")).read():
        sys.exit(f"REFUSING: front.tex does not carry the reserved DOI {reserved}")
    meta = json.load(open(META))["metadata"]
    st, dep = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok)
    if st != 200:
        sys.exit(f"cannot fetch draft {dep_id} [{st}]: {dep}")
    bucket = dep["links"]["bucket"]
    fn = os.path.basename(PDF); blob = open(PDF, "rb").read(); want = len(blob)

    def landed():
        s2, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok)
        return s2 == 200 and any(f.get("filename") == fn and f.get("filesize") == want for f in d.get("files", []))

    for attempt in range(1, 9):
        if landed():
            print(f"confirmed on server: {fn} ({want} bytes)"); break
        st, up = req("PUT", f"{bucket}/{fn}", tok, raw=blob, ctype="application/octet-stream", tries=1)
        if landed():
            print(f"uploaded {fn} ({want} bytes) [PUT returned {st}]"); break
        msg = up.get("message") or up.get("_nonjson") or up.get("_exc") or ""
        wait = min(20 * attempt, 90)
        print(f"  upload attempt {attempt} not confirmed (PUT {st}: {msg[:80]}), retrying in {wait}s")
        time.sleep(wait)
    else:
        sys.exit(f"upload never confirmed; rerun later with: python3 zenodo_publish.py {dep_id}")

    st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
    names = [f.get("filename") for f in d.get("files", [])]
    if st != 200 or names != [fn]:
        sys.exit(f"REFUSING: file list is not exactly the book ({names})")
    print(f"file list clean: {names}")

    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": meta}, tries=6)
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok, tries=1)
    if st not in (200, 202):
        print(f"publish returned [{st}], checking whether it went live anyway")
        vst, vd = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        if vst == 200 and vd.get("submitted"):
            pub = vd; print("  it did publish; the gateway dropped the response")
        else:
            sys.exit(f"NOT published (state={vd.get('state')!r}); rerun with: python3 zenodo_publish.py {dep_id}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    url = pub.get("links", {}).get("record_html") or pub.get("links", {}).get("html", "?")
    full = json.load(open(META))
    full["deposited"] = {"doi": doi, "url": url, "date": time.strftime("%Y-%m-%d"), "version": meta.get("version")}
    json.dump(full, open(META, "w"), indent=2, ensure_ascii=False)
    print(f"PUBLISHED  DOI = {doi}  URL = {url}")


def main():
    build_gate()
    audit_gate()
    if "--check" in sys.argv:
        print("--check: gates passed; Zenodo not contacted, token not read")
        return
    tok = token()
    if "--reserve" in sys.argv:
        reserve(tok)
    elif len(sys.argv) > 1 and sys.argv[1].isdigit():
        publish(tok, sys.argv[1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
