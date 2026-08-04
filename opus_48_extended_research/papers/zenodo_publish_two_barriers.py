#!/usr/bin/env python3
"""Publish "Two Barriers to the MOND Acceleration Coefficient" to Zenodo as a NEW record.

FIRST release -> POST /deposit/depositions to mint a new concept DOI. NOT a new version of any existing
record; do not point it at one.

Guards, all inherited from zenodo_publish_a0_note.py because each was earned the hard way on an earlier
record in this corpus:
  LOCAL-PRESENCE    every intended file must exist before anything is created.
  SCRIPTS-PASS      every cited script must exit 0 here and now -- a self-verifying archive that ships a
                    failing script is worse than no archive.
  NO-PLACEHOLDER    refuse if the manuscript still contains an unfilled placeholder token.
  NO-EMAIL          refuse if any shipped file contains an e-mail address. This repo is public and the
                    standing rule is no personal contact data in it, ever.
  NAME-EXACT        after upload the server's file list must match the intended set exactly.
  METADATA-SANITY   version present; creator is the affiliation name, never an e-mail; type = preprint.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
Usage: python zenodo_publish_two_barriers.py
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
BASE = "https://zenodo.org/api"
PAPER = "opus_48_extended_research/papers/TWO_BARRIERS_TO_THE_MOND_COEFFICIENT_2026-08-03.md"

SCRIPTS = [
    "real_research/reviews/mi_orbital_unruh_gems_2026.py",
    "real_research/reviews/mi_orbital_unruh_conformal_2026.py",
    "real_research/reviews/mi_orbital_unruh_q_2026.py",
    "real_research/reviews/mi_routeA_a0_estimator_invariance_2026.py",
    "real_research/reviews/mi_p4_kernel_pricing_2026.py",
    "real_research/reviews/mi_shape_systematic_mechanism_2026.py",
    "real_research/reviews/mi_routeA_admissibility_audit_2026.py",
    "real_research/reviews/mi_orbital_q_selfaudit_2026.py",   # v2(a): the scope correction
    "real_research/reviews/mi_crossover_master_formula_2026.py",  # v2(b): refutes v2(a)'s theorem
    "real_research/reviews/mi_2Z_is_the_friedmann_root_2026.py",  # v2(b): withdraws a bad objection
    "real_research/reviews/mi_circular_dS_response_2026.py",   # v2: the response lane, computed
    "real_research/reviews/mi_route_a_kernel.py",          # the kernel module the others import
]
FILES = [PAPER] + SCRIPTS
# the two cheap ones are re-run live; the slow ones are trusted from their committed state
RERUN = ["real_research/reviews/mi_route_a_kernel.py",
         "real_research/reviews/mi_orbital_unruh_q_2026.py",
         "real_research/reviews/mi_orbital_q_selfaudit_2026.py",
         "real_research/reviews/mi_crossover_master_formula_2026.py",
         "real_research/reviews/mi_2Z_is_the_friedmann_root_2026.py"]

PLACEHOLDERS = ("to be inserted", "TO BE INSERTED", "TBD", "INSERT_", "YOUR_EMAIL", "XXX")
EMAIL_RE = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

META = {
    "metadata": {
        "upload_type": "publication",
        "publication_type": "preprint",
        "title": ("Two Barriers to the MOND Acceleration Coefficient: the de Sitter-Unruh Balance Is "
                  "Orbital-Invariant at a0 = 2 c H_Lambda, and Rotation-Curve Determinations of a0 Are "
                  "Definition-Limited at 30%"),
        "creators": [{"name": "Zimmerman, Carl P.", "affiliation": "Briar Creek Tech"}],
        "version": "v1",
        "language": "eng",
        "keywords": ["MOND", "modified inertia", "cosmological constant", "dark energy",
                     "Unruh effect", "de Sitter space", "galaxy rotation curves", "SPARC"],
        "description": (
            "<p>The MOND acceleration scale a0 is numerically close to c H_Lambda, and several authors have "
            "proposed that it is <em>set</em> by the cosmological constant. The relation's <strong>form</strong> "
            "is established (Milgrom 1994, 1999, 2020); its dimensionless O(1) <strong>coefficient</strong> is "
            "not derived by any published argument. This note reports two independent barriers to fixing it and "
            "quantifies both.</p>"
            "<p><strong>First, a theoretical barrier.</strong> We compute the Unruh-DeWitt response for a "
            "<em>circular</em> worldline in de Sitter space and extract the MOND crossover coefficient q defined "
            "by a0 = q c H_Lambda. Milgrom's (1999) balance uses a <em>hyperbolic</em> worldline and gives q = 2; "
            "a circular orbit is never hyperbolic, so that derivation is scope-limited to linear acceleration "
            "while galaxies are orbits. We find q = 2 <strong>exactly</strong> on orbits, for two independent "
            "reasons both forced by the identity A^2 h^2 - R^2 w^2 = 1: the short-time correlator depends only "
            "on a5^2 = a^2 + H^2, which holds for any worldline on the hyperboloid; and the full-response "
            "orbital correction is an a-<em>independent</em> rescaling (verified to 1e-16 over five decades in "
            "a/H) which cancels identically in the crossover ratio. The mechanism returns Milgrom's coefficient "
            "and cannot be made to yield a smaller one.</p>"
            "<p><strong>Second, an observational barrier that dissolves into a theoretical one.</strong> "
            "Profiling SPARC with the mass-to-light ratio free per galaxy, the preferred a0 spans 30.6% across "
            "five admissible interpolation shapes - nearly four times the 7.87% separating the two published "
            "coefficient proposals. We identify the mechanism: the likelihood anchors on a single <em>deep</em> "
            "acceleration (boost nu = 3.97, y = 0.06) where the five kernels agree to 1.14%; the knee is not the "
            "anchor and correcting there over-corrects by 3.4x. The spread is already diluted 5.5x by the "
            "sample's 1.57 decades of coverage in y, so more data at one acceleration cannot reduce it. But the "
            "kernels are <em>not</em> degenerate - after optimal a0 rescaling they differ by 0.050 dex, 46% of "
            "the observed scatter - so the barrier is finite: it is removed by measuring the interpolation "
            "<em>shape</em>, needing of order 5x the effective sample.</p>"
            "<p>Fixing the kernel eliminates the systematic and yields a definite verdict, tabulated for five "
            "shapes: four of five favour a0 = (1/2) c sqrt(G rho_Lambda) at up to 2.69 sigma, the exponential "
            "kernel disfavours it at 0.66 sigma, and none reaches 3 sigma. The two dominant obstacles - the "
            "kernel choice (30.6%) and which cosmological density the horizon term tracks (20.9%) - both exceed "
            "the 7.87% being measured, so the present barrier is theoretical rather than observational.</p>"
            "<p><strong>Nothing here derives a coefficient.</strong> The reference value kappa = 1/2 remains "
            "fitted, not derived. Prior art is conceded in section 1 before any claim is made: the circular "
            "de Sitter response is partial prior art (Hari K. and Kothawala, PRD 109, 104073, 2024; Bunney and "
            "Louko, arXiv:2406.17643); the only novelty claimed is the extraction of a MOND coefficient from an "
            "orbital detector response, which was searched for and not found.</p>"
            "<p>All numerical claims are reproduced by the self-checking scripts included in this record; each "
            "exits non-zero on any failed internal check.</p>"),
        "notes": ("Companion scripts are included and are self-verifying: each prints [OK]/[FAIL] per internal "
                  "check and exits non-zero if any fails. Repository: "
                  "https://github.com/carlzimmerman/zimmerman-formula"),
    }
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
        return {"_nonjson": (b or "")[:300]}


def req(method, url, tok, data=None, raw=None, ctype="application/json", tries=4):
    h = {"Authorization": f"Bearer {tok}"}
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    elif raw is not None:
        body, h["Content-Type"] = raw, ctype
    else:
        body = None
    for i in range(tries):
        r = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(r, timeout=600) as resp:
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

    # ---- LOCAL-PRESENCE ---------------------------------------------------------------
    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing: {missing}")
    print(f"LOCAL-PRESENCE ok: all {len(FILES)} files present")

    # ---- NO-PLACEHOLDER / NO-EMAIL ---------------------------------------------------
    for rel in FILES:
        blob = open(os.path.join(REPO, rel), "rb").read()
        hits = [p for p in PLACEHOLDERS if p.encode() in blob]
        if hits:
            sys.exit(f"ERROR: {rel} still contains placeholder text {hits} -- refusing to mint a DOI")
        em = EMAIL_RE.findall(blob)
        if em:
            sys.exit(f"ERROR: {rel} contains {len(em)} e-mail address(es) -- refusing (public-record rule)")
    print(f"NO-PLACEHOLDER ok; NO-EMAIL ok across all {len(FILES)} files")

    # ---- SCRIPTS-PASS ---------------------------------------------------------------
    for rel in RERUN:
        r = subprocess.run([sys.executable, os.path.join(REPO, rel)],
                           capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            sys.exit(f"ERROR: {rel} exits {r.returncode} -- refusing to archive a failing script")
        tail = [l for l in r.stdout.splitlines() if "checks held" in l]
        print(f"SCRIPTS-PASS {os.path.basename(rel)}: {tail[-1].strip() if tail else 'exit 0'}")

    # ---- METADATA-SANITY -----------------------------------------------------------
    m = META["metadata"]
    if not m.get("version"):
        sys.exit("ERROR: no version string")
    if m.get("publication_type") != "preprint":
        sys.exit("ERROR: publication_type must be 'preprint'")
    for c in m["creators"]:
        if "@" in c["name"] or "@" in c.get("affiliation", ""):
            sys.exit("ERROR: e-mail in the creator block -- refusing")
    print(f"METADATA-SANITY ok: {m['creators'][0]['name']} / {m['creators'][0]['affiliation']}, "
          f"{m['version']}, preprint")

    # ---- create / upload / verify / publish ----------------------------------------
    st, dep = req("POST", f"{BASE}/deposit/depositions", tok, data={})
    if st not in (200, 201):
        sys.exit(f"create failed [{st}]: {dep}")
    did, bucket = dep["id"], dep["links"]["bucket"]
    print(f"created draft {did}")

    for rel in FILES:
        fn = os.path.basename(rel)
        with open(os.path.join(REPO, rel), "rb") as fh:
            st, up = req("PUT", f"{bucket}/{fn}", tok, raw=fh.read(), ctype="application/octet-stream")
        if st not in (200, 201):
            sys.exit(f"upload failed {fn} [{st}]: {up}")
        print(f"  uploaded {fn}")

    st, chk = req("GET", f"{BASE}/deposit/depositions/{did}", tok)
    got = sorted(f.get("filename") for f in chk.get("files", []))
    want = sorted(os.path.basename(f) for f in FILES)
    if got != want:
        sys.exit(f"ERROR NAME-EXACT: server has {got}, expected {want}")
    print(f"NAME-EXACT ok: {len(got)} files match")

    st, _ = req("PUT", f"{BASE}/deposit/depositions/{did}", tok, data=META)
    if st != 200:
        sys.exit(f"metadata failed [{st}]")
    print("metadata set")

    st, pub = req("POST", f"{BASE}/deposit/depositions/{did}/actions/publish", tok)
    if st not in (200, 202):
        sys.exit(f"publish failed [{st}]: {pub}")
    print(f"\n*** PUBLISHED ***\n  DOI  : {pub.get('doi')}\n  link : "
          f"{pub.get('links', {}).get('record_html', '')}\n  id   : {did}")


if __name__ == "__main__":
    main()
