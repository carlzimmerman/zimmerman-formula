#!/usr/bin/env python3
"""Publish new versions of the three remaining papers under the alpha>=2 kernel.

One parameterised script rather than three, so the guards cannot diverge between them. Carries every
guard the theorems-paper publication earned the hard way:

  * LOCAL-PRESENCE  every file in the intended set must exist on disk before anything is created.
  * PDF-FRESHNESS   the PDF must be newer than its markdown, or we would ship a stale paper under a
                    new version label.
  * SUPERSET        the new file set must contain every file the PREVIOUS version carried. This is the
                    guard whose absence cost the theorems record two files (PROVENANCE.md and the dSph
                    CSV) between v3 and v4 -- verifying the server against OUR list is not enough.
  * NAME-EXACT      after upload, the server's file names must match the intended set exactly.
  * VERSION-DISTINCT the metadata version must be non-empty and different from the previous version's.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_newversion_alpha2.py <desitter|wb|crispy>
"""
import json, os, sys, time, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
PAP = "opus_48_extended_research/papers"
BASE = "https://zenodo.org/api"

PAPERS = {
    "desitter": dict(
        rid=20721540, stem="DESITTER_GAUGE_MOND_SCALE",
        files=[f"{PAP}/DESITTER_GAUGE_MOND_SCALE.pdf",
               f"{PAP}/DESITTER_GAUGE_MOND_SCALE.md",
               f"{PAP}/DESITTER_GAUGE_MOND_SCALE.html",
               "real_research/reviews/mi_disformal_tail_freedom_2026.py",
               "real_research/reviews/mi_alpha2_migration_2026.py",
               "real_research/reviews/mi_alpha2_costs_the_kernel_derivation_2026.py",
               "real_research/reviews/mi_alpha1_solar_system_2026.py",
               "real_research/reviews/mi_theorem3_corrected_proof_2026.py"],
    ),
    "wb": dict(
        rid=21702746, stem="WB_CUBIC_GATE_LAW",
        files=[f"{PAP}/pdf/WB_CUBIC_GATE_LAW.pdf",
               f"{PAP}/WB_CUBIC_GATE_LAW.md",
               "real_research/reviews/count_wb_elbadry2021.py",
               "reviews/mi_bootstrap_circularity_2026.py",
               "real_research/reviews/mi_cmb_camb_run_2026.py",
               "real_research/reviews/mi_dcac_branch_settled_2026.py",
               "reviews/mi_kappa_spectral_reduction_2026.py",
               "real_research/reviews/mi_offcircular_closure_collapse_2026.py",
               "real_research/reviews/mi_omegac_anchor_2026.py",
               "reviews/mi_thermal_class_nogo_2026.py",
               "reviews/mi_three_classes_2026.py",
               "real_research/reviews/mi_wb_cubic_rise_2026.py",
               "real_research/reviews/mi_wb_dr3_feasibility_2026.py",
               "real_research/reviews/mi_wb_exponent_pipeline_2026.py",
               "real_research/reviews/mi_wb_gate_fork_2026.py",
               "real_research/reviews/mi_alpha2_migration_2026.py"],
    ),
    "crispy": dict(
        rid=21706870, stem="CRISPY_DARK_MATTER",
        files=[f"{PAP}/pdf/CRISPY_DARK_MATTER.pdf",
               f"{PAP}/CRISPY_DARK_MATTER.md",
               "real_research/reviews/mi_crispy_dark_matter_ledger_2026.py",
               "reviews/mi_kappa_spectral_reduction_2026.py",
               "real_research/reviews/mi_phantom_artifact_2026.py",
               "real_research/reviews/mi_phantom_prior_art_and_exclusivity_2026.py",
               "real_research/reviews/mi_alpha2_migration_2026.py"],
    ),
}


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
            with urllib.request.urlopen(r, timeout=240) as resp:
                return resp.status, _parse(resp.read().decode())
        except urllib.error.HTTPError as e:
            st, pay = e.code, _parse(e.read().decode())
        except Exception as e:
            st, pay = 599, {"_exc": repr(e)[:200]}
        if st < 500 or i == tries - 1:
            return st, pay
        time.sleep(5 * (i + 1))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in PAPERS:
        sys.exit(f"usage: python zenodo_newversion_alpha2.py <{'|'.join(PAPERS)}>")
    key = sys.argv[1]
    cfg = PAPERS[key]
    rid, stem, FILES = cfg["rid"], cfg["stem"], cfg["files"]
    META = f"{stem}.zenodo.json"
    tok = token()

    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} missing, refusing: {missing}")
    print(f"[{key}] all {len(FILES)} files present locally")

    pdf = os.path.join(REPO, FILES[0])
    md = os.path.join(REPO, FILES[1])
    if os.path.getmtime(pdf) < os.path.getmtime(md):
        sys.exit(f"ERROR: {stem}.pdf is OLDER than its markdown -- rebuild before publishing")
    print(f"[{key}] PDF newer than source")

    st, r = req("POST", f"{BASE}/deposit/depositions/{rid}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {r}")
    draft_url = r["links"].get("latest_draft") or r["links"].get("draft")
    st, d = req("GET", draft_url, tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {d}")
    did, bucket = d["id"], d["links"]["bucket"]
    prev_ver = str((d.get("metadata") or {}).get("version", ""))
    print(f"[{key}] draft {did} from record {rid} (prev version {prev_ver!r})")

    # SUPERSET guard
    inherited = sorted(f.get("filename") for f in d.get("files", []))
    want_names = sorted(os.path.basename(f) for f in FILES)
    dropped = [n for n in inherited if n not in want_names]
    if dropped:
        sys.exit(f"ERROR: would DROP {len(dropped)} inherited file(s), refusing: {dropped}")
    print(f"[{key}] superset OK: {len(inherited)} inherited all present in the new {len(FILES)}")

    for f in d.get("files", []):
        req("DELETE", f"{BASE}/deposit/depositions/{did}/files/{f.get('id')}", tok)
    print(f"[{key}] cleared {len(inherited)} inherited files")

    for rel in FILES:
        p = os.path.join(REPO, rel)
        fn = os.path.basename(p)
        with open(p, "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
    print(f"[{key}] uploaded {len(FILES)}")

    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    if st != 200 or got != want_names:
        sys.exit(f"NAME-EXACT check FAILED\n  want {want_names}\n  got  {got}")
    print(f"[{key}] verified {len(got)} files, names exact")

    meta = json.load(open(META))
    meta = meta.get("metadata", meta)
    new_ver = str(meta.get("version", ""))
    if not new_ver:
        sys.exit("ERROR: no version in metadata")
    if new_ver == prev_ver:
        sys.exit(f"ERROR: version {new_ver!r} identical to previous -- refusing")
    st, md_ = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data={"metadata": meta})
    if st not in (200, 201):
        sys.exit(f"metadata failed [{st}]: {md_}")
    print(f"[{key}] metadata attached ({prev_ver!r} -> {new_ver!r})")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok, tries=1)
    if st not in (200, 201, 202):
        st2, v = req("GET", f"{BASE}/deposit/depositions/{did}", tok, tries=6)
        if st2 == 200 and v.get("submitted"):
            pub = v
            print(f"[{key}]   it DID publish; gateway dropped the response")
        else:
            sys.exit(f"publish failed [{st}]: {pub}")
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "?")
    cd = pub.get("conceptdoi") or pub.get("metadata", {}).get("conceptdoi", "?")
    print(f"[{key}] PUBLISHED  version DOI {doi}  concept {cd}  files {len(got)}")
    print(f"[{key}] https://zenodo.org/record/{did}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
