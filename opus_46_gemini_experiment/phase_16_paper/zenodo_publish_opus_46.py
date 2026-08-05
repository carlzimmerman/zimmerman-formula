#!/usr/bin/env python3
"""Publish "Linear Response of the de Sitter Vacuum to Accelerated Matter" to Zenodo as a NEW record.

FIRST release -> POST /deposit/depositions to mint a new concept DOI. NOT a new version of any existing
record; do not point it at one.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
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
PAPER = "opus_46_gemini_experiment/phase_16_paper/linear_response_anti_mond_proof.md"

SCRIPTS = [
    "opus_46_gemini_experiment/phase_07_linear_response/retarded_susceptibility_deSitter.py",
]
FILES = [PAPER] + SCRIPTS
RERUN = SCRIPTS

PLACEHOLDERS = ("to be inserted", "TO BE INSERTED", "TBD", "INSERT_", "YOUR_EMAIL", "XXX")
EMAIL_RE = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

META = {
    "metadata": {
        "upload_type": "publication",
        "publication_type": "preprint",
        "title": ("Linear Response of the de Sitter Vacuum to Accelerated Matter: A Kubo-Formalism Proof "
                  "that MOND Requires Non-Equilibrium Physics"),
        "creators": [{"name": "Zimmerman, Carl P.", "affiliation": "Briar Creek Tech"}],
        "version": "v1",
        "language": "eng",
        "keywords": ["MOND", "modified inertia", "cosmological constant", "dark energy",
                     "acceleration scale", "de Sitter", "Kubo formalism", "linear response",
                     "Equation of State", "vacuum thermodynamics"],
        "description": (
            "<p>Recent attempts to derive Modified Newtonian Dynamics (MOND) and its characteristic "
            "acceleration scale a0 rely on the interaction between accelerated matter and the cosmological "
            "horizon. A persistent conjecture is that the vacuum response in de Sitter spacetime modifies "
            "inertia at low accelerations. In this work, we formalize this conjecture using Kubo linear "
            "response theory.</p>"
            "<p>We postulate that the modification to inertia is dictated by a causal memory kernel K(t), "
            "derived as the inverse Fourier transform of the retarded susceptibility of the de Sitter vacuum. "
            "By computing this susceptibility for a massive scalar field in the Bunch-Davies vacuum, we show "
            "exactly that the equilibrium de Sitter vacuum is thermodynamically passive (it satisfies the "
            "Kubo-Martin-Schwinger condition). Consequently, the spectral density is non-negative, and the "
            "resulting inertia correction is strictly positive. The linear response of the de Sitter vacuum "
            "therefore raises inertia, an \"anti-MOND\" effect.</p>"
            "<p>We conclude that any derivation of MOND from vacuum dynamics strictly forbids the use of "
            "dynamical memory kernels (influence functionals). Instead, we demonstrate that Modified Inertia "
            "must be formulated as a Category-2 thermodynamic Equation of State (EOS). By defining inertia "
            "as the excess response above the de Sitter thermal floor, the EOS approach bypasses the "
            "passivity wall entirely, yielding a causal, ghost-free relation that reproduces the exact "
            "MOND phenomenology without requiring non-equilibrium physics.</p>"
            "<p>All numerical claims are reproduced by the self-checking script included in this record, "
            "which evaluates the worldline Wightman function directly to extract the susceptibility and mass "
            "correction.</p>"
        ),
        "notes": ("Companion scripts are included and are self-verifying: they exit non-zero if any internal "
                  "check fails. Repository: https://github.com/carlzimmerman/zimmerman-formula"),
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
    dry = "--dry-run" in sys.argv

    missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
    if missing:
        sys.exit(f"ERROR: {len(missing)} file(s) missing, refusing: {missing}")
    print(f"LOCAL-PRESENCE ok: all {len(FILES)} files present")

    for rel in FILES:
        blob = open(os.path.join(REPO, rel), "rb").read()
        hits = [p for p in PLACEHOLDERS if p.encode() in blob]
        if hits:
            sys.exit(f"ERROR: {rel} still contains placeholder text {hits} -- refusing to mint a DOI")
        em = EMAIL_RE.findall(blob)
        if em:
            sys.exit(f"ERROR: {rel} contains {len(em)} e-mail address(es) -- refusing (public-record rule)")
    print(f"NO-PLACEHOLDER ok; NO-EMAIL ok across all {len(FILES)} files")

    for rel in RERUN:
        r = subprocess.run([sys.executable, os.path.join(REPO, rel)],
                           cwd=os.path.dirname(os.path.join(REPO, rel)),
                           capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr)
            sys.exit(f"ERROR: {rel} exits {r.returncode} -- refusing to archive a failing script")
        tail = [l for l in r.stdout.splitlines() if "checks held" in l]
        print(f"SCRIPTS-PASS {os.path.basename(rel)}: {tail[-1].strip() if tail else 'exit 0'}")

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

    if dry:
        print("\nDRY RUN: every local guard passed. Stopping before network call.")
        sys.exit(0)

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
