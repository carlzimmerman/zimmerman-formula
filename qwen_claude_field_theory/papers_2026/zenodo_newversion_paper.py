#!/usr/bin/env python3
"""Publish a NEW VERSION of an existing Zenodo record (same concept DOI). Production; publishing is irreversible.
Reads ZENODO_ACCESS_TOKEN from ~/new_physics/.env -- NEVER printed.

Usage: python zenodo_newversion_paper.py --from REC_ID --meta X.zenodo.json --date YYYY-MM-DD FILE [FILE ...]
       python zenodo_newversion_paper.py --draft DRAFT_ID --meta ... --date ... FILE ...   (resume a draft)

REC_ID must be the LATEST published version (the script checks). The inherited files are deleted from the draft,
the given files uploaded, and the server's file list must equal the given basenames, sizes included, before publish.
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = os.path.join(os.path.expanduser("~"), "new_physics", ".env")
BASE = "https://zenodo.org/api"


def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found")


def req(method, url, tok, data=None, raw=None, tries=4):
    h = {"Authorization": f"Bearer {tok}"}; body = None
    if data is not None: body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    elif raw is not None: body = raw; h["Content-Type"] = "application/octet-stream"
    for k in range(tries):
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=300) as resp:
                t = resp.read().decode(); return resp.status, (json.loads(t) if t.strip().startswith(("{", "[")) else {})
        except urllib.error.HTTPError as e:
            t = e.read().decode(); st, p = e.code, (json.loads(t) if t.strip().startswith("{") else {"raw": t[:200]})
        except Exception as e:
            st, p = 599, {"exc": repr(e)[:200]}
        if st < 500 or k == tries - 1:
            return st, p
        time.sleep(5 * (k + 1))


def main():
    meta_path, date = arg("--meta"), arg("--date")
    skip = {"--from", "--draft", "--meta", "--date"}
    files = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] not in skip]
    if not (meta_path and date and files):
        sys.exit(__doc__)
    for f in files:
        if not os.path.isfile(f): sys.exit(f"missing file {f}")
    meta = json.load(open(meta_path)); meta = meta.get("metadata", meta); meta["publication_date"] = date
    tok = token()
    if arg("--from"):
        rec = arg("--from")
        st, lat = req("GET", f"{BASE}/records/{rec}/versions/latest", tok, tries=6)
        if st != 200 or str(lat.get("id")) != str(rec):
            sys.exit(f"record {rec} is not the latest version (latest: {lat.get('id')}) [{st}] -- refusing")
        st, nv = req("POST", f"{BASE}/deposit/depositions/{rec}/actions/newversion", tok, tries=1)
        if st not in (200, 201): sys.exit(f"newversion failed [{st}]: {nv}")
        st, d = req("GET", nv["links"]["latest_draft"], tok, tries=6)
    else:
        st, d = req("GET", f"{BASE}/deposit/depositions/{arg('--draft')}", tok, tries=6)
    if st != 200: sys.exit(f"draft fetch failed [{st}]: {d}")
    did, bucket = d["id"], d["links"]["bucket"]
    print(f"draft {did} -- rerun with --draft {did} if anything below fails")
    for f in d.get("files", []):
        st, _ = req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f['id']}", tok)
        print(f"  removed inherited {f['filename']} [{st}]")
    for p in files:
        st, up = req("PUT", f"{bucket}/{os.path.basename(p)}", tok, raw=open(p, "rb").read(), tries=3)
        print(f"  upload {os.path.basename(p)} [{st}]")
    want = sorted((os.path.basename(p), os.path.getsize(p)) for p in files)
    st, d = req("GET", f"{BASE}/deposit/depositions/{did}", tok, tries=6)
    have = sorted((f["filename"], f["filesize"]) for f in d.get("files", []))
    if st != 200 or have != want:
        sys.exit(f"file list mismatch -- refusing to publish\n  want {want}\n  have {have}")
    print(f"file list verified: {[w[0] for w in want]}")
    st, md = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta}, tries=6)
    if st not in (200, 201): sys.exit(f"metadata failed [{st}]: {md}")
    if md.get("metadata", {}).get("version") != meta.get("version"):
        sys.exit("metadata did not stick on the server -- refusing to publish")
    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok, tries=1)
    if st not in (200, 202):
        st2, v = req("GET", f"{BASE}/deposit/depositions/{did}", tok, tries=6)
        if not v.get("submitted"): sys.exit(f"NOT published [{st}]; rerun with --draft {did}")
        pub = v
    print(f"PUBLISHED  DOI = {pub.get('doi')}  concept = {pub.get('conceptdoi')}  version = {pub.get('metadata', {}).get('version')}")


if __name__ == "__main__":
    main()
