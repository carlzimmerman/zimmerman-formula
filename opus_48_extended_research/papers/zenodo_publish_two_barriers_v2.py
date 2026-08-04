#!/usr/bin/env python3
r"""zenodo_publish_two_barriers_v2.py -- NEW VERSION of DOI 10.5281/zenodo.21782600.

v2 corrects the SCOPE of one sentence in v1. v1 said the de Sitter-Unruh mechanism "returns Milgrom's coefficient
and cannot be made to yield a smaller one". That is true for inertia functionals of the local dS-Unruh
TEMPERATURE -- where a self-audit upgrades it from an assumption to a theorem -- but v1's response lane (the
functional of F(E) with a gap-dependent T_eff) was never computed, and the unscoped sentence claimed it was. v2
states the scoped claim, adds the rigidity theorem, and records the arithmetic of the remaining freedom, which
runs AGAINST this framework's own coefficient.

Reuses every guard from the v1 publisher (LOCAL-PRESENCE, NO-PLACEHOLDER, NO-EMAIL, SCRIPTS-PASS, NAME-EXACT,
METADATA-SANITY) by importing them, then adds two:

  V2-DIFF      the paper on disk must actually differ from v1 in the ways claimed -- it must carry the v2 banner
               AND must no longer carry v1's unscoped sentence. Refuses to mint a version that changes nothing.
  FILES-RESET  a Zenodo newversion draft inherits v1's files; every inherited file is DELETED before upload, so
               NAME-EXACT is a real check on this version's contents rather than on a union with v1's.

The token is read from .env and never printed.
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zenodo_publish_two_barriers as v1  # noqa: E402  (config + guards, single source of truth)

RECORD_ID = 21782600                       # the v1 record this versions
BANNER = "**v2 (2026-08-03), correction of scope.**"
V1_SENTENCE = "cannot be made to yield a smaller one"

META = copy.deepcopy(v1.META)
META["metadata"]["version"] = "v2"
META["metadata"]["description"] += (
    "<p><strong>v2 (2026-08-03), correction of scope.</strong> A self-audit "
    "(mi_orbital_q_selfaudit_2026.py, included) found that v1's statement that the mechanism &quot;cannot be "
    "made to yield a smaller&quot; coefficient over-reached its class. Within the class of inertia functionals "
    "of the local de Sitter-Unruh temperature the audit STRENGTHENS the result -- the Newtonian and deep-MOND "
    "limits jointly force the functional to be linear in T, and the 2 pi cancels in q, so q = 2 is not an "
    "artefact of the Unruh normalisation -- but functionals of the full response F(E), with the gap-dependent "
    "T_eff that this paper's own KMS result forces for every non-zero orbital frequency, were never computed "
    "and are not closed. v2 states the scoped claim. Against this framework's own interest, v2 also records "
    "where the remaining freedom would land: a non-cancelling 4 pi gives q = 0.15915, which is exactly Milgrom "
    "(2020)'s 1/2pi, while reaching q = 1/Z = 0.17275 requires dividing 2 by 2Z = 11.578 -- a factor carrying "
    "sqrt(pi), not the normalisation of any identifiable detector response. Neither the 30.6% shape systematic "
    "nor the orbital invariance of q is affected.</p>")


def main():
    tok = v1.token()

    # ---- V2-DIFF: refuse to mint a version that changes nothing ----------------------
    paper = open(os.path.join(v1.REPO, v1.PAPER), encoding="utf-8").read()
    if BANNER not in paper:
        sys.exit("ERROR V2-DIFF: the paper carries no v2 banner -- refusing to mint a version")
    if V1_SENTENCE in paper:
        sys.exit(f"ERROR V2-DIFF: v1's unscoped sentence {V1_SENTENCE!r} is still present -- "
                 "the correction was not applied")
    if "mi_orbital_q_selfaudit_2026.py" not in paper:
        sys.exit("ERROR V2-DIFF: the audit script is not cited in the paper -- refusing")
    print(f"V2-DIFF ok: banner present, v1 sentence removed, audit cited")

    # ---- every v1 guard, unchanged ----------------------------------------------------
    missing = [f for f in v1.FILES if not os.path.exists(os.path.join(v1.REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing: {missing}")
    print(f"LOCAL-PRESENCE ok: all {len(v1.FILES)} files present")

    for rel in v1.FILES:
        blob = open(os.path.join(v1.REPO, rel), "rb").read()
        hits = [p for p in v1.PLACEHOLDERS if p.encode() in blob]
        if hits:
            sys.exit(f"ERROR: {rel} contains placeholder text {hits} -- refusing")
        em = v1.EMAIL_RE.findall(blob)
        if em:
            sys.exit(f"ERROR: {rel} contains {len(em)} e-mail address(es) -- refusing (public-record rule)")
    print(f"NO-PLACEHOLDER ok; NO-EMAIL ok across all {len(v1.FILES)} files")

    import subprocess
    for rel in v1.RERUN:
        r = subprocess.run([sys.executable, os.path.join(v1.REPO, rel)],
                           capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            sys.exit(f"ERROR: {rel} exits {r.returncode} -- refusing to archive a failing script")
        tail = [l for l in r.stdout.splitlines() if "checks held" in l]
        print(f"SCRIPTS-PASS {os.path.basename(rel)}: {tail[-1].strip() if tail else 'exit 0'}")

    m = META["metadata"]
    if m.get("version") != "v2":
        sys.exit("ERROR: version string is not v2")
    if m.get("publication_type") != "preprint":
        sys.exit("ERROR: publication_type must be 'preprint'")
    for c in m["creators"]:
        if "@" in c["name"] or "@" in c.get("affiliation", ""):
            sys.exit("ERROR: e-mail in the creator block -- refusing")
    print(f"METADATA-SANITY ok: {m['creators'][0]['name']} / {m['creators'][0]['affiliation']}, v2, preprint")

    # ---- newversion draft ------------------------------------------------------------
    st, nv = v1.req("POST", f"{v1.BASE}/deposit/depositions/{RECORD_ID}/actions/newversion", tok)
    if st not in (200, 201):
        sys.exit(f"newversion failed [{st}]: {nv}")
    draft_url = nv["links"].get("latest_draft") or nv["links"].get("draft")
    did = int(str(draft_url).rstrip("/").rsplit("/", 1)[-1])
    st, dep = v1.req("GET", f"{v1.BASE}/deposit/depositions/{did}", tok)
    if st != 200:
        sys.exit(f"draft fetch failed [{st}]: {dep}")
    bucket = dep["links"]["bucket"]
    print(f"newversion draft {did} of record {RECORD_ID}")

    # ---- FILES-RESET: drop every inherited file so NAME-EXACT means this version -----
    for f in dep.get("files", []):
        st, _ = v1.req("DELETE", f"{v1.BASE}/deposit/depositions/{did}/files/{f['id']}", tok)
        if st not in (200, 204):
            sys.exit(f"ERROR FILES-RESET: could not delete inherited {f.get('filename')} [{st}]")
    st, dep = v1.req("GET", f"{v1.BASE}/deposit/depositions/{did}", tok)
    if dep.get("files"):
        sys.exit(f"ERROR FILES-RESET: {len(dep['files'])} inherited file(s) survive -- refusing")
    print("FILES-RESET ok: draft is empty, this version's contents are its own")

    for rel in v1.FILES:
        fn = os.path.basename(rel)
        with open(os.path.join(v1.REPO, rel), "rb") as fh:
            st, up = v1.req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
        print(f"  uploaded {fn}")

    st, chk = v1.req("GET", f"{v1.BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in v1.FILES)
    if got != want:
        sys.exit(f"ERROR NAME-EXACT: server has {got}, expected {want}")
    print(f"NAME-EXACT ok: {len(got)} files match")

    st, _ = v1.req("PUT", f"{v1.BASE}/deposit/depositions/{did}", tok, data=META)
    if st != 200:
        sys.exit(f"metadata failed [{st}]")
    print("metadata set (v2)")

    st, pub = v1.req("POST", f"{v1.BASE}/deposit/depositions/{did}/actions/publish", tok)
    if st not in (200, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    print(f"\n*** v2 PUBLISHED ***\n  version DOI : {pub.get('doi')}\n  concept DOI : "
          f"{pub.get('conceptdoi', '10.5281/zenodo.21782599')}\n  link        : "
          f"{pub.get('links', {}).get('record_html', '')}\n  draft id    : {did}")


if __name__ == "__main__":
    main()
