#!/usr/bin/env python3
"""Add lane FRZ6's result to its Zenodo record as a NEW VERSION of record 24208901 (production).

Owner's go: 2026-11-13 ("Deposit now": the frozen criteria today, the result as a new version whatever the verdict).
Version 2 keeps the four files of version 1 and adds RESULT.md, the amendment, the scripts, the graded outputs and a
zip of the part files. Metadata: frz6z_v2.zenodo.json.

Usage:
  python3 -I -B frz6z_zenodo_newversion.py --check     gates only; never reads the token, never contacts Zenodo
  python3 -I -B frz6z_zenodo_newversion.py             new version, upload, publish, read back (ONCE)
  python3 -I -B frz6z_zenodo_newversion.py DRAFT_ID    resume an unpublished draft of the new version

Gates (always): every file is tracked, equal to origin/main, free of home paths and banned names; no receipt for
version 2 exists yet. The token is read by the helper of PAPER72_zenodo_publish.py and never printed.
kappa = 1/2 FITTED; not theory closed.
"""
import hashlib, importlib.util, io, json, os, subprocess, sys, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
META = os.path.join(HERE, "frz6z_v2.zenodo.json")
RECEIPT = os.path.join(HERE, "frz6z_v2_deposit_receipt.json")
REC = "24208901"
C13 = "closure_2026_11_13/"
F6 = C13 + "FRZ6_forest_flux_candidate_graded/"
FILES = [  # (repo-relative source, name in the record); the first four are version 1's
    (F6 + "FROZEN_CRITERIA.md", "FRZ6_FROZEN_CRITERIA.md"),
    (C13 + "CJ1_candidate_completion/COMPLETED_FORM.md", "CJ1_COMPLETED_FORM.md"),
    (C13 + "JNT2_crossing_speed_joint/jnt2_common.py", "jnt2_common.py"),
    (C13 + "JNT2_crossing_speed_joint/jnt2_hm.py", "jnt2_hm.py"),
    (F6 + "RESULT.md", "FRZ6_RESULT.md"),
    (F6 + "AMENDMENT_A1.md", "FRZ6_AMENDMENT_A1.md"),
] + [(F6 + n, n) for n in (
    "frz6_tables.py", "frz6_run.py", "frz6_grade.py", "frz6_refit.py", "run_all.sh", "run_rest.sh",
    "frz6_grade_canonical.json", "frz6_grade_canonical.out", "frz6_grade_canonical_MUTATE.json",
    "frz6_grade_canonical_MUTATE.out", "frz6_grade_alt.json", "frz6_grade_alt.out", "frz6_grade_alt_MUTATE.json",
    "frz6_grade_alt_MUTATE.out", "frz6_refit_canonical.json", "frz6_refit_canonical.out", "frz6_refit_alt.json",
    "frz6_refit_alt.out")]
ZIPNAME = "FRZ6_parts.zip"
BANNED = ("/" + "users/", "cold " + "dark matter", "cdm" + "-like")
V1_KEEPS_COMPLETED_FORM = True  # version 1's copy of the completed form is kept as deposited (the repo copy moved on)


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True)


def checked(src):
    if git("ls-files", "--error-unmatch", "--", src).returncode != 0:
        sys.exit(f"REFUSING: {src} is not tracked")
    if git("diff", "--quiet", "origin/main", "--", src).returncode != 0:
        sys.exit(f"REFUSING: {src} differs from origin/main")
    blob = open(os.path.join(REPO, src), "rb").read()
    if any(b in blob.decode("utf-8", "replace").lower() for b in BANNED):
        sys.exit(f"REFUSING: banned name or home path in {src}")
    return blob


def gates():
    if os.path.exists(RECEIPT):
        sys.exit("REFUSING: a version 2 receipt already exists")
    m = json.load(open(META))["metadata"]
    low = (m["title"] + " " + m["description"]).lower()
    if any(b in low for b in BANNED):
        sys.exit("REFUSING: banned name or home path in the metadata")
    blobs = [(name, checked(src)) for src, name in FILES]
    parts = sorted(p for p in git("ls-files", "--", F6 + "parts").stdout.split() if p.endswith(".json"))
    if len(parts) != 44:
        sys.exit(f"REFUSING: expected 44 tracked part files, found {len(parts)}")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in parts:
            zi = zipfile.ZipInfo("parts/" + os.path.basename(p), date_time=(2026, 11, 13, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
            z.writestr(zi, checked(p))
    blobs.append((ZIPNAME, buf.getvalue()))
    for name, blob in blobs:
        print(f"gate ok: {name}  {len(blob)} bytes  sha256 {hashlib.sha256(blob).hexdigest()[:16]}  md5 {hashlib.md5(blob).hexdigest()}")
    print(f"{len(blobs)} files, {sum(len(b) for _, b in blobs) / 1e6:.2f} MB")
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
        st, nv = req("POST", f"{BASE}/deposit/depositions/{REC}/actions/newversion", tok, tries=1)
        if st not in (200, 201):
            sys.exit(f"newversion failed [{st}]: {nv}")
        st, dep = req("GET", nv["links"]["latest_draft"], tok, tries=6)
        if st != 200:
            sys.exit(f"cannot fetch the new-version draft [{st}]: {dep}")
    dep_id, bucket = dep["id"], dep["links"]["bucket"]
    print(f"new-version draft {dep_id} of record {REC} -- rerun with this id if anything below fails")

    def listing():
        st, d = req("GET", f"{BASE}/deposit/depositions/{dep_id}", tok, tries=6)
        return d.get("files", []) if st == 200 else None

    md5 = {n: hashlib.md5(b).hexdigest() for n, b in blobs}

    def ok(fl, name, blob):
        return any(f.get("filename") == name and f.get("filesize") == len(blob)
                   and f.get("checksum", "").replace("md5:", "") == md5[name] for f in fl)

    for name, blob in blobs:
        for attempt in range(1, 9):
            fl = listing()
            if fl is not None and ok(fl, name, blob):
                print(f"confirmed on server: {name} ({len(blob)} bytes)")
                break
            if fl is not None:   # an inherited file of the same name with other content must go first
                for f in fl:
                    if f.get("filename") == name:
                        req("DELETE", f"{BASE}/deposit/depositions/{dep_id}/files/{f['id']}", tok, tries=4)
            req("PUT", f"{bucket}/{name}", tok, raw=blob, ctype="application/octet-stream", tries=1)
            time.sleep(3 if len(blob) < 1e6 else 15)
        else:
            sys.exit(f"upload of {name} never confirmed -- rerun with: {os.path.basename(__file__)} {dep_id}")

    fl = listing()
    names = sorted(f.get("filename") for f in fl) if fl is not None else None
    if names != sorted(md5):
        sys.exit(f"file list is not the expected {len(md5)} ({names}) -- refusing to publish; draft {dep_id} left unpublished")
    if not all(ok(fl, n, b) for n, b in blobs):
        sys.exit(f"checksum mismatch -- refusing to publish; draft {dep_id} left unpublished")
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
        "created": pub.get("created"), "modified": pub.get("modified"),
        "files": {f.get("filename"): {"bytes": f.get("filesize"), "md5": f.get("checksum", "").replace("md5:", "")}
                  for f in pub.get("files", [])},
    }
    print("PUBLISHED " + json.dumps({k: v for k, v in out.items() if k != "files"}, indent=1))
    print(f"{len(out['files'])} files on the record")
    json.dump(out, open(RECEIPT, "w"), indent=1)


if __name__ == "__main__":
    main()
