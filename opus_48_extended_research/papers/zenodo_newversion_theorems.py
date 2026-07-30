#!/usr/bin/env python3
"""Publish a NEW VERSION of the WB cubic gate-law record with the COMPLETE file set.

WHY THIS EXISTS. The first v3 attempt used a newversion script adapted from a PDF-only paper.
A Zenodo new-version draft starts as a copy of the previous record, and that script DELETES every
inherited file then uploads only the PDF. v2 carried 9 files -- the paper PDF, the markdown source,
and 7 reproducibility scripts that section 8 of the paper explicitly cites -- so v3 shipped with 1
file and silently dropped the reproducibility material. This script uploads the FULL set, including
the new v3 scripts, and VERIFIES the count before publishing.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_newversion_wb_cubic_full.py <record_id>
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
META = "MI_STRUCTURAL_THEOREMS.zenodo.json"
BASE = "https://zenodo.org/api"

# every file the record should carry: the paper, its source, and every script section 8 cites
FILES = [
    "opus_48_extended_research/papers/pdf/MI_STRUCTURAL_THEOREMS.pdf",
    "opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md",
    "real_research/reviews/mi_dcac_split_settled_2026.py",
    "real_research/reviews/mi_sign_from_perturbation_drift_2026.py",
    "real_research/reviews/mi_closure_vs_action_gap_2026.py",
    "real_research/reviews/mi_channelA_friedmann_2026.py",
    "real_research/reviews/mi_efe_derived_general_2026.py",
    "real_research/reviews/mi_growth_amplification_founded_2026.py",
    "real_research/reviews/mi_closure_fixed_by_rar_universality_2026.py",
    "real_research/reviews/mi_dsph_closure_test_real_data_2026.py",
    "real_research/data/dsph/mcconnachie2012_dsph.csv",
    "real_research/data/dsph/PROVENANCE.md",
    "reviews/mi_kappa_spectral_reduction_2026.py",
]


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: token not found")


def _parse(b):
    try:
        return json.loads(b or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": b[:200]}


def req(method, url, tok, data=None, raw=None, ctype="application/json", tries=4):
    h = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    elif raw is not None:
        body = raw; h["Content-Type"] = ctype
    else:
        body = None
    for i in range(tries):
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=180) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, pay = e.code, _parse(e.read().decode())
        except Exception as e:
            st, pay = 599, {"_exc": repr(e)[:200]}
        if st < 500 or i == tries - 1:
            return st, pay
        time.sleep(5 * (i + 1))


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: zenodo_newversion_wb_cubic_full.py <record_id>")
    rid = sys.argv[1]
    tok = token()

    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing to publish: {missing}")
    print(f"all {len(FILES)} files present locally")

    st, dep = req("POST", f"{BASE}/deposit/depositions/{rid}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {dep}")
    draft_url = dep["links"]["latest_draft"]
    st, draft = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {draft}")
    did, bucket = draft["id"], draft["links"]["bucket"]
    print(f"new draft id = {did}")

    # clear inherited files, then upload the full set
    for f in draft.get("files", []):
        req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f['id']}", tok)
    print(f"cleared {len(draft.get('files', []))} inherited file(s)")

    for rel in FILES:
        p = os.path.join(REPO, rel)
        fn = os.path.basename(p)
        with open(p, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(),
                         ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed for {fn} [{st}]: {up}")
        print(f"  uploaded {fn} ({up.get('size', '?')} B)")

    # VERIFY the count before publishing -- this is the guard the first attempt lacked
    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = [f.get("filename") for f in chk.get("files", [])]
    if st != 200 or len(got) != len(FILES):
        sys.exit(f"file-count check FAILED: expected {len(FILES)}, server has {len(got)}: {got}")
    print(f"verified {len(got)} files on the draft")

    meta = json.load(open(META))
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
    print(f"PUBLISHED  DOI = {doi}  URL = https://zenodo.org/record/{did}")
    cd = pub.get("conceptdoi") or pub.get("metadata", {}).get("conceptdoi")
    if cd:
        print(f"concept DOI (all versions) = {cd}")


if __name__ == "__main__":
    main()
