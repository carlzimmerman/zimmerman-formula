#!/usr/bin/env python3
r"""zenodo_publish_what_can_fix.py -- FIRST release of a NEW record (new concept DOI).

Mints a new concept DOI for WHAT_CAN_FIX_THE_MOND_COEFFICIENT_2026-08-04.md. This is NOT a new version of
10.5281/zenodo.21782600; NEW-RECORD asserts that below so the two cannot be confused.

Guards (the six from the two-barriers publisher, imported so there is one source of truth, plus three):
  LOCAL-PRESENCE   every cited file exists
  NO-PLACEHOLDER   no TBD / INSERT_ / XXX style stubs anywhere in the record
  NO-EMAIL         no e-mail address in any archived file (public-record rule)
  SCRIPTS-PASS     EVERY cited script is re-run here and now and must exit 0 -- a self-verifying archive
  NAME-EXACT       the server's file list matches ours exactly before publish
  METADATA-SANITY  version string, preprint type, no address in the creator block
  NEW-RECORD       refuses to run if the target looks like a version of an existing deposition
  OVERLAP-DECLARED the paper must contain the overlap statement, because three scripts are shared with the
                   companion record and a reader must be told which sections are new
  FITTED-STATED    the paper must say kappa = 1/2 is fitted and not derived. A record that omits this is not
                   publishable under the project's own standing rule, so it is a guard and not a courtesy.

The token is read from .env and never printed.

  --dry-run   runs every guard and stops before the first network call.
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zenodo_publish_two_barriers as tb  # noqa: E402  (token, req, PLACEHOLDERS, EMAIL_RE, BASE, REPO)

PAPER = "opus_48_extended_research/papers/WHAT_CAN_FIX_THE_MOND_COEFFICIENT_2026-08-04.md"
SCRIPTS = [
    "real_research/reviews/mi_crossover_master_formula_2026.py",
    "real_research/reviews/mi_2Z_is_the_friedmann_root_2026.py",
    "real_research/reviews/mi_circular_dS_response_2026.py",
    "real_research/reviews/mi_zeropoint_interference_audit_2026.py",
    "real_research/reviews/mi_local_floor_target_2026.py",
    "real_research/reviews/mi_scalar_condensate_proposal_audit_2026.py",
]
FILES = [PAPER] + SCRIPTS
COMPANION = "10.5281/zenodo.21782600"

META = {
    "metadata": {
        "upload_type": "publication",
        "publication_type": "preprint",
        "title": ("What Can and Cannot Fix the MOND Acceleration Coefficient: a Relabelling Theorem, Three "
                  "Failed Derivations, and a Redshift Discriminant"),
        "creators": [{"name": "Zimmerman, Carl P.", "affiliation": "Briar Creek Tech"}],
        "version": "v1",
        "language": "eng",
        "keywords": ["MOND", "modified inertia", "cosmological constant", "dark energy",
                     "acceleration scale", "de Sitter", "Unruh effect", "ghost condensate",
                     "galaxy rotation curves", "a0"],
        "related_identifiers": [
            {"identifier": COMPANION, "relation": "isSupplementTo", "scheme": "doi"},
        ],
        "description": (
            "<p>The MOND acceleration scale is numerically close to c H_Lambda, and the proposal that it is SET by "
            "the cosmological constant dates to Milgrom (1994, 1999). The relation's FORM is established; its "
            "dimensionless O(1) COEFFICIENT is not derived by any published argument, and the live proposals "
            "differ: Milgrom (1999) gives a0 = 2 c H_Lambda, Milgrom (2020) gives kappa = 1/2pi, and this author "
            "has used a0 = (1/2) c sqrt(G rho_Lambda), i.e. a0 = c H_Lambda / Z with Z = 2 sqrt(8 pi/3). That "
            "last value is FITTED, NOT DERIVED, and nothing in this paper changes that.</p>"
            "<p>This paper is about what could change it. We prove a RELABELLING THEOREM: because "
            "Lambda = 8 pi G rho_Lambda/c^2 identically, G rho_Lambda and c^2 Lambda are the SAME scale up to the "
            "pure number 8 pi, so any combination of the two returns that scale times a power of 8 pi and cannot "
            "select a coefficient or exclude c H_Lambda. We then audit three constructions of the kind that "
            "naturally suggest themselves. All three fail: one on dimensions (its geometric mean is a "
            "frequency-squared, not an acceleration, and the charitable repair overshoots by exactly (8 pi)^(1/4)); "
            "one because its free parameter is merely relocated (for any inertia functional of the local de "
            "Sitter-Unruh temperature the crossover is q = 2 c1prime / f-prime(T_GH) = 2/r with r free, so an "
            "explicit admissible functional reaches kappa = 1/2 but only by trading one fitted number for "
            "another); and one on a sign that makes its central invariant imaginary in any homogeneous vacuum. "
            "Two of the three additionally attach their coefficient to a0 rather than to the FLOOR a0/2 that "
            "Milgrom's balance actually contains; having committed the same error ourselves, we record it as a "
            "systematic hazard.</p>"
            "<p>Three results are constructive. (i) The theorem does NOT exclude a single-scale derivation: "
            "sqrt(G rho_Lambda) is pi-free while sqrt(8 pi G rho_Lambda/3) is not, so a construction taking "
            "rho_Lambda as its only input is untouched by the theorem and would automatically exclude c H_Lambda, "
            "being unable to manufacture the Friedmann 8 pi/3. (ii) No standard local rate supplies the required "
            "factor 1/4: over seven candidates the closest is sqrt(G rho/4 pi) at 12.84% away, wider than the "
            "7.87% separating the two published coefficients, so there is no near miss. Since kappa is fitted, "
            "searching constructions until one reproduces 1/4 is reverse-engineering a fit, and any candidate must "
            "make an independent prediction. (iii) The choice of floor is OBSERVATIONALLY DECIDABLE and needs no "
            "new mechanism: a local response to the vacuum DENSITY gives a0 proportional to sqrt(rho_DE), exactly "
            "constant for w = -1 and blind to matter, whereas a horizon floor tracks c H(z) = c H_0 E(z), rising "
            "to 1.78, 3.01 and 4.54 times its present value at z = 1, 2, 3. The local reading is therefore the "
            "MORE falsifiable of the two, because it forbids the rising branch the horizon reading permits.</p>"
            "<p>A by-product worth separating from the negative results: the detector-response calculation "
            "reproduces Deser and Levin's temperature sqrt(a^2+H^2)/2pi to 1e-15 to 1e-17 across three radii from "
            "a computed Unruh-DeWitt response on a non-rotating worldline, so the temperature Milgrom's balance "
            "POSITS is here obtained rather than assumed. Rotation breaks the KMS condition only at order "
            "(v/c)^2, falling short of the freedom needed for kappa = 1/2 by a factor 1.2e7, which makes the "
            "response route a null for the coefficient.</p>"
            "<p>PRIOR ART, which the coefficient question does not displace: Milgrom 1994 Ann. Phys. 229, 384 "
            "section II eq. 3 writes a_lambda = c^2 sqrt(Lambda/3); the interpolating function nu = sqrt(1+1/y) "
            "and the temperature balance are Milgrom 1999 Phys. Lett. A 253, 273 eqs. 6-9, who fixes the "
            "coefficient at 2 c H_Lambda; the five-acceleration construction is Deser and Levin 1997 CQG 14, "
            "L163; the exponential kernel is McGaugh 2008 ApJ 683, 137 eq. 11a; kappa = 1/2pi is Milgrom 2020. "
            "None of the FORM is claimed here.</p>"
            "<p>All numerical and symbolic claims are reproduced by the self-checking scripts included in this "
            "record; each prints per-check results and exits non-zero if any internal check fails. Three of the "
            "six scripts, and the closed form of section 4, are shared with the companion record "
            "10.5281/zenodo.21782600; the paper declares the overlap and states which sections are new.</p>"),
        "notes": ("Companion scripts are included and self-verifying: each prints [OK]/[FAIL] per internal check "
                  "and exits non-zero if any fails. Overlap with 10.5281/zenodo.21782600 is declared in the "
                  "paper's section 10. Repository: https://github.com/carlzimmerman/zimmerman-formula"),
    }
}

BANNED = ("gemini", "chatgpt", "openai", "google", "anthropic", "claude", "e-mail from", "wrote to me")


def main():
    tok = tb.token()
    dry = "--dry-run" in sys.argv

    # ---- NEW-RECORD ------------------------------------------------------------------
    if any(a.isdigit() for a in sys.argv[1:]) or "--newversion" in sys.argv:
        sys.exit("ERROR NEW-RECORD: this script mints a NEW concept DOI and takes no record id. To version the "
                 f"companion record {COMPANION}, use zenodo_publish_two_barriers_v2.py")
    print(f"NEW-RECORD ok: minting a new concept DOI; {COMPANION} is linked as a related identifier, not versioned")

    # ---- LOCAL-PRESENCE --------------------------------------------------------------
    missing = [f for f in FILES if not os.path.exists(os.path.join(tb.REPO, f))]
    if missing:
        sys.exit(f"ERROR LOCAL-PRESENCE: {len(missing)} file(s) missing: {missing}")
    print(f"LOCAL-PRESENCE ok: all {len(FILES)} files present")

    # ---- NO-PLACEHOLDER / NO-EMAIL ---------------------------------------------------
    for rel in FILES:
        blob = open(os.path.join(tb.REPO, rel), "rb").read()
        hits = [p for p in tb.PLACEHOLDERS if p.encode() in blob]
        if hits:
            sys.exit(f"ERROR NO-PLACEHOLDER: {rel} contains {hits} -- refusing to mint a DOI")
        em = tb.EMAIL_RE.findall(blob)
        if em:
            sys.exit(f"ERROR NO-EMAIL: {rel} contains {len(em)} e-mail address(es) -- refusing (public-record rule)")
    print(f"NO-PLACEHOLDER ok; NO-EMAIL ok across all {len(FILES)} files")

    # ---- OVERLAP-DECLARED / FITTED-STATED / no third-party attribution ---------------
    paper = open(os.path.join(tb.REPO, PAPER), encoding="utf-8").read()
    if "Overlap declaration" not in paper or COMPANION not in paper:
        sys.exit("ERROR OVERLAP-DECLARED: the paper must declare its overlap with the companion record by DOI")
    print(f"OVERLAP-DECLARED ok: overlap with {COMPANION} stated in the paper")
    if "fitted, not derived" not in paper.lower():
        sys.exit("ERROR FITTED-STATED: the paper must state that kappa = 1/2 is fitted and not derived")
    print("FITTED-STATED ok: the paper states kappa = 1/2 is fitted, not derived")
    low = paper.lower()
    named = [b for b in BANNED if b in low]
    if named:
        sys.exit(f"ERROR: the paper names {named} -- the audited constructions must be assessed on their merits "
                 "without attributing them to any person, product or private correspondence")
    print("NO-ATTRIBUTION ok: the audited constructions are described without naming any third party")

    # ---- SCRIPTS-PASS: every one, live ------------------------------------------------
    for rel in SCRIPTS:
        r = subprocess.run([sys.executable, os.path.join(tb.REPO, rel)],
                           capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            sys.exit(f"ERROR SCRIPTS-PASS: {rel} exits {r.returncode} -- refusing to archive a failing script")
        tail = [l for l in r.stdout.splitlines() if "checks held" in l]
        print(f"SCRIPTS-PASS {os.path.basename(rel)}: {tail[-1].strip() if tail else 'exit 0'}")

    # ---- METADATA-SANITY -------------------------------------------------------------
    m = META["metadata"]
    if not m.get("version") or m.get("publication_type") != "preprint":
        sys.exit("ERROR METADATA-SANITY: version string missing or publication_type is not 'preprint'")
    for cr in m["creators"]:
        if "@" in cr["name"] or "@" in cr.get("affiliation", ""):
            sys.exit("ERROR METADATA-SANITY: e-mail in the creator block -- refusing")
    print(f"METADATA-SANITY ok: {m['creators'][0]['name']} / {m['creators'][0]['affiliation']}, "
          f"{m['version']}, preprint")

    if dry:
        print("\nDRY RUN: every local guard passed. Stopping before the first network call; nothing published.")
        return

    # ---- create / upload / verify / publish ------------------------------------------
    st, dep = tb.req("POST", f"{tb.BASE}/deposit/depositions", tok, data={})
    if st not in (200, 201):
        sys.exit(f"create failed [{st}]: {dep}")
    did, bucket = dep["id"], dep["links"]["bucket"]
    print(f"created draft {did}")

    for rel in FILES:
        fn = os.path.basename(rel)
        with open(os.path.join(tb.REPO, rel), "rb") as fh:
            st, up = tb.req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
        print(f"  uploaded {fn}")

    st, chk = tb.req("GET", f"{tb.BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in FILES)
    if got != want:
        sys.exit(f"ERROR NAME-EXACT: server has {got}, expected {want}")
    print(f"NAME-EXACT ok: {len(got)} files match")

    st, _ = tb.req("PUT", f"{tb.BASE}/deposit/depositions/{did}", tok, data=META)
    if st != 200:
        sys.exit(f"metadata failed [{st}]")
    print("metadata set")

    st, pub = tb.req("POST", f"{tb.BASE}/deposit/depositions/{did}/actions/publish", tok)
    if st not in (200, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    print(f"\n*** PUBLISHED ***\n  version DOI : {pub.get('doi')}\n  concept DOI : "
          f"{pub.get('conceptdoi', '')}\n  link        : "
          f"{pub.get('links', {}).get('record_html', '')}\n  id          : {did}")


if __name__ == "__main__":
    main()
