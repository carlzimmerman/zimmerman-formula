#!/usr/bin/env python3
"""Add the blind re-grade FRZ6R to the FRZ6 Zenodo record as version 3 (a new version of record 24210556; production).

Owner's go: 2026-11-13 ("Yes, add v3"). Version 3 keeps the 25 files of version 2 exactly as deposited and adds FRZ6R's
brief, frozen criteria, amendment, result, scripts, graded outputs and a zip of its 192 part files.
Metadata: frz6z_v3.zenodo.json.

Usage:
  python3 -I -B frz6z_zenodo_v3.py --check     gates only; never reads the token, never contacts Zenodo
  python3 -I -B frz6z_zenodo_v3.py             new version, upload, publish (ONCE)
  python3 -I -B frz6z_zenodo_v3.py DRAFT_ID    resume an unpublished draft of the new version

Gates (always): every new file is tracked, equal to origin/main, free of home paths and banned names; no version 3
receipt exists yet. Before publishing, the draft must hold version 2's 25 files with the checksums of its receipt plus
the new files and nothing else. The token is read by the helper of PAPER72_zenodo_publish.py and never printed.
kappa = 1/2 FITTED; not theory closed.
"""
import hashlib, importlib.util, io, json, os, subprocess, sys, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
META = os.path.join(HERE, "frz6z_v3.zenodo.json")
RECEIPT = os.path.join(HERE, "frz6z_v3_deposit_receipt.json")
V2 = json.load(open(os.path.join(HERE, "frz6z_v2_deposit_receipt.json")))
REC = str(V2["record_id"])
R6 = "closure_2026_11_13/FRZ6R_blind_forest_flux_candidate/"
FILES = [(R6 + s, n) for s, n in (
    ("BRIEF.md", "FRZ6R_BRIEF.md"), ("FROZEN_CRITERIA.md", "FRZ6R_FROZEN_CRITERIA.md"),
    ("AMENDMENT_A1_2026-11-13.md", "FRZ6R_AMENDMENT_A1.md"), ("RESULT_BLIND.md", "FRZ6R_RESULT_BLIND.md"),
    ("frz6r_lib.py", "frz6r_lib.py"), ("frz6r_run.py", "frz6r_run.py"), ("frz6r_grade.py", "frz6r_grade.py"),
    ("run_all.sh", "frz6r_run_all.sh"), ("run_lane2.sh", "frz6r_run_lane2.sh"), ("run_resume.sh", "frz6r_run_resume.sh"),
    ("frz6r_grade.json", "frz6r_grade.json"), ("frz6r_grade.out", "frz6r_grade.out"),
    ("frz6r_grade_MUTATE.json", "frz6r_grade_MUTATE.json"), ("frz6r_grade_MUTATE.out", "frz6r_grade_MUTATE.out"))]
ZIPNAME = "FRZ6R_parts.zip"
BANNED = ("/" + "users/", "cold " + "dark matter", "cdm" + "-like")


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
        sys.exit("REFUSING: a version 3 receipt already exists")
    m = json.load(open(META))["metadata"]
    low = (m["title"] + " " + m["description"]).lower()
    if any(b in low for b in BANNED):
        sys.exit("REFUSING: banned name or home path in the metadata")
    blobs = [(name, checked(src)) for src, name in FILES]
    parts = sorted(p for p in git("ls-files", "--", R6 + "parts").stdout.split() if p.endswith(".json"))
    if len(parts) != 192:
        sys.exit(f"REFUSING: expected 192 tracked part files, found {len(parts)}")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in parts:
            zi = zipfile.ZipInfo("parts/" + os.path.basename(p), date_time=(2026, 11, 13, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
            z.writestr(zi, checked(p))
    blobs.append((ZIPNAME, buf.getvalue()))
    clash = sorted(set(n for n, _ in blobs) & set(V2["files"]))
    if clash:
        sys.exit(f"REFUSING: new file names clash with version 2's: {clash}")
    for name, blob in blobs:
        print(f"gate ok: {name}  {len(blob)} bytes  md5 {hashlib.md5(blob).hexdigest()}")
    print(f"{len(blobs)} new files, {sum(len(b) for _, b in blobs) / 1e6:.2f} MB; {len(V2['files'])} kept from version 2")
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

    want = {n: (v["bytes"], v["md5"]) for n, v in V2["files"].items()}
    want.update({n: (len(b), hashlib.md5(b).hexdigest()) for n, b in blobs})

    def have(fl):
        return {f.get("filename"): (f.get("filesize"), f.get("checksum", "").replace("md5:", "")) for f in fl}

    fl = listing()
    if fl is None:
        sys.exit(f"cannot list the draft -- draft {dep_id} left unpublished")
    h = have(fl)
    missing = [n for n in V2["files"] if h.get(n) != want[n]]
    if missing:
        sys.exit(f"version 2's files are not all inherited unchanged ({missing}) -- draft {dep_id} left unpublished")
    print(f"inherited unchanged: {len(V2['files'])} files of version 2")

    for name, blob in blobs:
        for attempt in range(1, 9):
            fl = listing()
            if fl is not None and have(fl).get(name) == want[name]:
                print(f"confirmed on server: {name} ({len(blob)} bytes)")
                break
            req("PUT", f"{bucket}/{name}", tok, raw=blob, ctype="application/octet-stream", tries=1)
            time.sleep(3 if len(blob) < 1e6 else 10)
        else:
            sys.exit(f"upload of {name} never confirmed -- rerun with: {os.path.basename(__file__)} {dep_id}")

    fl = listing()
    if fl is None or have(fl) != want:
        sys.exit(f"file list or checksums are not the expected {len(want)} -- refusing to publish; draft {dep_id} left unpublished")
    print(f"file list clean and checksums match ({len(want)} files)")

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
