#!/usr/bin/env python3
"""Deposit lane FRZ6's frozen criteria on Zenodo as a standalone record (production).

Owner's go: 2026-11-13 ("Deposit now"), for the title and description in frz6z.zenodo.json and exactly four files:
the frozen criteria, the completed-form statement of the candidate rule, and the two scripts that define the split.
The result of FRZ6 is to be added later as a NEW VERSION of the same record, on the same go, whatever the verdict.

Usage:
  python3 -I -B frz6z_zenodo_publish.py --check     gates only; never reads the token, never contacts Zenodo
  python3 -I -B frz6z_zenodo_publish.py             create, upload, publish, read back (ONCE)
  python3 -I -B frz6z_zenodo_publish.py DRAFT_ID    resume an unpublished draft

Gates (always): every file is tracked, equal to origin/main, free of home paths and banned names; the metadata has no
'deposited' block yet. The token is read by the helper of PAPER72_zenodo_publish.py from the workspace .env and is never
printed. kappa = 1/2 FITTED; not theory closed.
"""
import hashlib, importlib.util, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
META = os.path.join(HERE, "frz6z.zenodo.json")
C13 = "closure_2026_11_13/"
FILES = [  # (repo-relative source, name in the record)
    (C13 + "FRZ6_forest_flux_candidate_graded/FROZEN_CRITERIA.md", "FRZ6_FROZEN_CRITERIA.md"),
    (C13 + "CJ1_candidate_completion/COMPLETED_FORM.md", "CJ1_COMPLETED_FORM.md"),
    (C13 + "JNT2_crossing_speed_joint/jnt2_common.py", "jnt2_common.py"),
    (C13 + "JNT2_crossing_speed_joint/jnt2_hm.py", "jnt2_hm.py"),
]
BANNED = ("/" + "users/", "cold " + "dark matter", "cdm" + "-like")


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True)


def gates():
    meta = json.load(open(META))
    if "deposited" in meta:
        sys.exit("REFUSING: frz6z.zenodo.json already carries a 'deposited' block")
    m = meta["metadata"]
    for k in ("title", "description", "creators", "license", "upload_type"):
        if not m.get(k):
            sys.exit(f"REFUSING: metadata field {k} missing")
    low = (m["title"] + " " + m["description"]).lower()
    if any(b in low for b in BANNED):
        sys.exit("REFUSING: banned name or home path in the metadata")
    blobs = []
    for src, name in FILES:
        path = os.path.join(REPO, src)
        if git("ls-files", "--error-unmatch", "--", src).returncode != 0:
            sys.exit(f"REFUSING: {src} is not tracked")
        if git("diff", "--quiet", "origin/main", "--", src).returncode != 0:
            sys.exit(f"REFUSING: {src} differs from origin/main")
        blob = open(path, "rb").read()
        if any(b in blob.decode("utf-8").lower() for b in BANNED):
            sys.exit(f"REFUSING: banned name or home path in {src}")
        blobs.append((name, blob))
        print(f"gate ok: {name}  {len(blob)} bytes  sha256 {hashlib.sha256(blob).hexdigest()}")
    return m, blobs


def main():
    m, blobs = gates()
    if "--check" in sys.argv:
        print("--check: gates passed; Zenodo not contacted, token not read")
        return
    spec = importlib.util.spec_from_file_location(
        "p72pub", os.path.join(REPO, "qwen_claude_field_theory", "papers_2026", "PAPER72_zenodo_publish.py"))
    P = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, [sys.argv[0]]
    spec.loader.exec_module(P)
    sys.argv = argv
    req, BASE = P.req, P.BASE
    tok = P.token()

    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        st, dep = req("GET", f"{BASE}/deposit/depositions/{sys.argv[1]}", tok)
        if st != 200 or dep.get("submitted"):
            sys.exit(f"cannot reuse draft [{st}] submitted={dep.get('submitted')}")
    else:
        st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={})
        if st not in (200, 201):
            sys.exit(f"create failed [{st}]: {dep}")
    dep_id, bucket = dep["id"], dep["links"]["bucket"]
    print(f"deposition id = {dep_id} -- rerun with this id if anything below fails")

    def listing():
        st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        return d.get("files", []) if st == 200 else None

    for name, blob in blobs:
        for attempt in range(1, 7):
            fl = listing()
            if fl is not None and any(f.get("filename") == name and f.get("filesize") == len(blob) for f in fl):
                print(f"confirmed on server: {name} ({len(blob)} bytes)")
                break
            st, up = req("PUT", f"{bucket}/{name}", tok, raw=blob, ctype="application/octet-stream", tries=1)
            time.sleep(2)
        else:
            sys.exit(f"upload of {name} never confirmed -- rerun with: {os.path.basename(__file__)} {dep_id}")

    fl = listing()
    names = sorted(f.get("filename") for f in fl) if fl is not None else None
    if names != sorted(n for n, _ in blobs):
        sys.exit(f"file list is not the expected four ({names}) -- refusing to publish; draft {dep_id} left unpublished")
    md5 = {n: hashlib.md5(b).hexdigest() for n, b in blobs}
    bad = [f.get("filename") for f in fl if f.get("checksum", "").replace("md5:", "") != md5[f.get("filename")]]
    if bad:
        sys.exit(f"checksum mismatch on {bad} -- refusing to publish; draft {dep_id} left unpublished")
    print("file list clean and checksums match")

    st, md = req("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok, data={"metadata": m}, tries=6)
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md} -- draft {dep_id} left unpublished")
    print("metadata attached")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{dep_id}/actions/publish", tok, tries=1)
    if st not in (200, 202):
        vst, vd = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        if vst == 200 and vd.get("submitted"):
            pub = vd
        else:
            sys.exit(f"NOT published [{st}] (state={vd.get('state')!r}); rerun with: {os.path.basename(__file__)} {dep_id}")
    out = {
        "doi": pub.get("doi") or pub.get("metadata", {}).get("doi"),
        "conceptdoi": pub.get("conceptdoi"),
        "record_id": pub.get("record_id") or pub.get("id"),
        "deposition_id": dep_id,
        "url": pub.get("links", {}).get("record_html") or pub.get("links", {}).get("html"),
        "created": pub.get("created"),
        "files": {f.get("filename"): {"bytes": f.get("filesize"), "md5": f.get("checksum", "").replace("md5:", "")}
                  for f in pub.get("files", [])},
    }
    print("PUBLISHED " + json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "frz6z_deposit_receipt.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
