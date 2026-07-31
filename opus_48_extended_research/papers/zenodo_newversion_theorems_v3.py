#!/usr/bin/env python3
"""Publish v3 of the structural-theorems record as a NEW VERSION of the existing concept record.

WHY A SEPARATE SCRIPT. zenodo_publish_theorems.py does POST /deposit/depositions, i.e. it creates a
BRAND NEW record with its own concept DOI. That is correct for a first release and WRONG for v3: it
would orphan v2 and leave readers of the v2 DOI with no pointer to the corrected version. v3 must be a
new VERSION of concept 21707844, so the versioned-DOI chain resolves and "latest" moves.

AND IT KEEPS THAT SCRIPT'S FILE-SET GUARD, which exists because an earlier new-version attempt on a
sibling record deleted every inherited file and uploaded only the PDF, silently dropping the
reproducibility scripts the paper's own section 11 cites. A Zenodo new-version draft starts as a copy of
the previous record, so the inherited files must be deleted and the FULL set re-uploaded, then counted
against the server before publishing.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_newversion_theorems_v3.py <v2_record_id>
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
META = "MI_STRUCTURAL_THEOREMS.zenodo.json"
BASE = "https://zenodo.org/api"

# Every file the record should carry: the paper, its source, and every script section 11 cites.
FILES = [
    "opus_48_extended_research/papers/pdf/MI_STRUCTURAL_THEOREMS.pdf",
    "opus_48_extended_research/papers/MI_STRUCTURAL_THEOREMS.md",
    # v1-v2 reproducibility set
    "real_research/reviews/mi_dcac_split_settled_2026.py",
    "real_research/reviews/mi_sign_from_perturbation_drift_2026.py",
    "real_research/reviews/mi_closure_vs_action_gap_2026.py",
    "real_research/reviews/mi_channelA_friedmann_2026.py",
    "real_research/reviews/mi_efe_derived_general_2026.py",
    "real_research/reviews/mi_growth_amplification_founded_2026.py",
    "real_research/reviews/mi_closure_fixed_by_rar_universality_2026.py",
    "real_research/reviews/mi_dsph_closure_test_real_data_2026.py",
    "reviews/mi_kappa_spectral_reduction_2026.py",
    # the real-catalogue data behind section 9.1, and its extraction record
    "real_research/data/dsph/mcconnachie2012_dsph.csv",
    "real_research/data/dsph/PROVENANCE.md",
    # NEW IN v3
    "real_research/reviews/mi_structural_theorems_v3_numbers_2026.py",
    "real_research/reviews/mi_disformal_tail_freedom_2026.py",
    "real_research/reviews/mi_alpha2_migration_2026.py",
]


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("ERROR: ZENODO_ACCESS_TOKEN not found in .env")


def _parse(b):
    try:
        return json.loads(b or "{}")
    except json.JSONDecodeError:
        return {"_nonjson": (b or "")[:200]}


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
        sys.exit("usage: python zenodo_newversion_theorems_v3.py <v2_record_id>")
    rid = sys.argv[1]
    tok = token()

    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing to publish: {missing}")
    print(f"all {len(FILES)} files present locally")

    # sanity: the PDF must actually contain v3 content, or we would ship a stale paper under a v3 label
    pdf = os.path.join(REPO, FILES[0])
    md = os.path.join(REPO, FILES[1])
    if os.path.getmtime(pdf) < os.path.getmtime(md):
        sys.exit("ERROR: the PDF is OLDER than the markdown -- rebuild it before publishing")
    print("PDF is newer than its source")

    # 1) open a new version draft off the existing record
    st, r = req("POST", f"{BASE}/deposit/depositions/{rid}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {r}")
    draft_url = r["links"].get("latest_draft") or r["links"].get("draft")
    if not draft_url:
        sys.exit(f"no draft link returned: {r.get('links')}")
    st, d = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {d}")
    did, bucket = d["id"], d["links"]["bucket"]
    print(f"new-version draft id = {did}  (from record {rid})")

    # 1b) *** THE GUARD THAT WAS MISSING IN v3 AND COST TWO FILES. ***
    # v3 verified the server against OUR list but never checked OUR list against the PREVIOUS
    # version's. It therefore silently dropped PROVENANCE.md and mcconnachie2012_dsph.csv -- the data
    # and extraction record behind section 9.1 -- reproducing, in a new form, exactly the regression
    # this script's file-set check was written to prevent. A new version must be a SUPERSET.
    inherited = sorted(f.get("filename") for f in d.get("files", []))
    want_names = sorted(os.path.basename(f) for f in FILES)
    dropped = [n for n in inherited if n not in want_names]
    if dropped:
        sys.exit(f"ERROR: this would DROP {len(dropped)} file(s) the previous version carried, "
                 f"refusing to publish: {dropped}\n  (a new version must be a superset; add them to "
                 f"FILES or state explicitly why they are being removed)")
    print(f"superset check OK: all {len(inherited)} inherited files are in the new set of {len(FILES)}")

    # 2) delete every inherited file, so the set is exactly what we intend
    for f in d.get("files", []):
        fid = f.get("id")
        st, _ = req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{fid}", tok)
        print(f"  removed inherited {f.get('filename')} [{st}]")

    # 3) upload the full set
    for rel in FILES:
        p = os.path.join(REPO, rel)
        fn = os.path.basename(p)
        with open(p, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(),
                         ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed for {fn} [{st}]: {up}")
        print(f"  uploaded {fn} ({up.get('size', '?')} B)")

    # 4) VERIFY the count against the server before publishing
    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in FILES)
    if st != 200 or got != want:
        sys.exit(f"file-set check FAILED.\n  expected {len(want)}: {want}\n  server has {len(got)}: {got}")
    print(f"verified {len(got)} files on the draft, names match exactly")

    # 5) metadata
    meta = json.load(open(META))
    meta = meta.get("metadata", meta)
    prev_ver = str((d.get("metadata") or {}).get("version", ""))
    new_ver = str(meta.get("version", ""))
    if not new_ver:
        sys.exit("ERROR: metadata carries no version string -- refusing")
    if new_ver == prev_ver:
        sys.exit(f"ERROR: metadata version {new_ver!r} is IDENTICAL to the previous version's -- a new "
                 f"version must be labelled distinctly. Refusing.")
    st, md_ = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md_}")
    print(f"metadata attached (version = {meta['version']})")

    # 6) publish
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
    print(f"\nPUBLISHED v3")
    print(f"  version DOI : {doi}")
    print(f"  concept DOI : {cd}   (always resolves to the latest version)")
    print(f"  URL         : https://zenodo.org/record/{did}")
    print(f"  files       : {len(got)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
