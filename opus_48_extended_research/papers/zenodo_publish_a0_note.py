#!/usr/bin/env python3
"""Publish the a0 note to Zenodo as a NEW record (preprint of the PRD submission).

This is a FIRST release, so it uses POST /deposit/depositions to mint a new concept DOI. It is NOT a
new version of any existing record -- do not point it at one.

Guards, all of which have been earned the hard way on earlier records in this corpus:
  * LOCAL-PRESENCE   every intended file must exist before anything is created.
  * PDF-FRESHNESS    the PDF must be newer than the .tex, or a stale paper ships under a fresh DOI.
  * NAME-EXACT       after upload, the server's file list must match the intended set exactly.
  * METADATA-SANITY  a version string must be present, and the creator must be the affiliation name --
                     never a personal e-mail address.
  * NO-PLACEHOLDER   refuse if the PDF still contains an unfilled placeholder token.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_publish_a0_note.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
SUB = "opus_48_extended_research/papers/submission_aps"
META = os.path.join(REPO, "opus_48_extended_research/papers/A0_HALF_THE_DARK_ENERGY_RATE.zenodo.json")
BASE = "https://zenodo.org/api"

FILES = [
    f"{SUB}/a0_half_dark_energy_rate.pdf",
    f"{SUB}/a0_half_dark_energy_rate.tex",
    f"{SUB}/COVER_LETTER.md",
    "real_research/reviews/verify_a0_half_dark_energy_rate_2026.py",
    "real_research/reviews/verify_a0_half_dark_energy_rate_2026.out",
    "real_research/rar_framework_a0_mlfit.py",
]

PLACEHOLDERS = ("INSERT_CONTACT_EMAIL", "to be supplied", "TO BE SUPPLIED", "YOUR_EMAIL")


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")


def _parse(b):
    try:
        return json.loads(b or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": (b or "")[:300]}


def req(method, url, tok, data=None, raw=None, ctype="application/json", tries=4):
    h = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw
        h["Content-Type"] = ctype
    else:
        body = None
    for i in range(tries):
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=300) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, pay = e.code, _parse(e.read().decode())
        except Exception as e:
            st, pay = 599, {"_exc": repr(e)[:300]}
        if st < 500 or i == tries - 1:
            return st, pay
        time.sleep(5 * (i + 1))


def main():
    tok = token()

    # ---- LOCAL-PRESENCE ----------------------------------------------------------------
    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing: {missing}")
    print(f"all {len(FILES)} files present locally")

    # ---- PDF-FRESHNESS ----------------------------------------------------------------
    pdf = os.path.join(REPO, FILES[0])
    tex = os.path.join(REPO, FILES[1])
    if os.path.getmtime(pdf) < os.path.getmtime(tex):
        sys.exit("ERROR: the PDF is OLDER than the .tex -- rebuild with "
                 "'tectonic -X compile a0_half_dark_energy_rate.tex' before publishing")
    print("PDF is newer than its source")

    # ---- NO-PLACEHOLDER ---------------------------------------------------------------
    blob = open(pdf, "rb").read()
    hits = [p for p in PLACEHOLDERS if p.encode() in blob]
    if hits:
        sys.exit(f"ERROR: the PDF still contains unfilled placeholder text {hits} -- refusing to mint a DOI")
    print("no placeholder tokens in the PDF")

    # ---- METADATA-SANITY --------------------------------------------------------------
    meta = json.load(open(META))
    meta = meta.get("metadata", meta)
    if not str(meta.get("version", "")):
        sys.exit("ERROR: metadata carries no version string")
    for c in meta.get("creators", []):
        if "@" in c.get("name", "") or "@" in c.get("affiliation", ""):
            sys.exit("ERROR: an e-mail address appears in the creator block -- refusing")
    if meta.get("publication_type") != "preprint":
        sys.exit("ERROR: publication_type must be 'preprint' -- this is a submitted manuscript, not a "
                 "journal publication, and mislabelling it would misrepresent the record")
    print(f"metadata sane: version {meta['version']!r}, type preprint, "
          f"creator {meta['creators'][0]['name']!r}")

    # ---- create ------------------------------------------------------------------------
    st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={})
    if st not in (200, 201):
        sys.exit(f"create failed [{st}]: {dep}")
    did = dep["id"]
    bucket = dep["links"]["bucket"]
    print(f"created draft {did}")

    # ---- upload ------------------------------------------------------------------------
    for rel in FILES:
        p = os.path.join(REPO, rel)
        fn = os.path.basename(p)
        with open(p, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(),
                         ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
        print(f"  uploaded {fn}")

    # ---- NAME-EXACT --------------------------------------------------------------------
    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in FILES)
    if st != 200 or got != want:
        sys.exit(f"NAME-EXACT check FAILED\n  want {want}\n  got  {got}")
    print(f"verified {len(got)} files, names exact")

    # ---- metadata + publish ------------------------------------------------------------
    st, md = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md}")
    print("metadata attached")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok, tries=1)
    if st not in (200, 201, 202):
        st2, v = req("GET", f"{BASE}/deposit/depositions/{did}", tok, tries=6)
        if st2 == 200 and v.get("submitted"):
            pub = v
            print("  it DID publish; the gateway dropped the response")
        else:
            sys.exit(f"publish failed [{st}]: {pub}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    cd = pub.get("conceptdoi") or pub.get("metadata", {}).get("conceptdoi", "?")
    print(f"\nPUBLISHED as a PREPRINT")
    print(f"  version DOI : {doi}")
    print(f"  concept DOI : {cd}   (always resolves to the latest version)")
    print(f"  URL         : https://zenodo.org/record/{did}")
    print(f"  files       : {len(got)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
