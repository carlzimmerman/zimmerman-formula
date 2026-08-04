#!/usr/bin/env python3
r"""zenodo_publish_two_barriers_v2.py -- NEW VERSION of DOI 10.5281/zenodo.21782600.

v2 carries TWO corrections, both narrowing a closure claim, both made on the day of v1's release. They ship as
one version because the first was superseded before it ever reached the record.

  (a) v1's unscoped no-go is WITHDRAWN. "Cannot be made to yield a smaller one" is a claim about ALL inertia
      functionals, but only functionals of the local dS-Unruh TEMPERATURE were examined.
  (b) The "rigidity theorem" that briefly replaced (a) is ALSO WITHDRAWN. It claimed the two MOND limits jointly
      force q = 2. They do not: the Newtonian limit constrains f as T -> infinity, the deep limit reads
      f'(T_GH), and nothing connects two different points on f. The correct statement is the closed form
      q = 2 c1p/f'(T_GH), so q = 2/r with r free -- and an explicit admissible f reaches q = 1/Z exactly.

Reuses every guard from the v1 publisher (LOCAL-PRESENCE, NO-PLACEHOLDER, NO-EMAIL, SCRIPTS-PASS, NAME-EXACT,
METADATA-SANITY) by importing them, then adds two:

  V2-DIFF      refuses to mint a version that changes nothing, and -- because correction (b) had to be applied in
               THREE places -- checks each withdrawn claim is absent from the paper AND from every archived
               script, not merely from the abstract. A withdrawal that survives in a companion script is not a
               withdrawal.
  FILES-RESET  a Zenodo newversion draft inherits v1's files; every inherited file is DELETED before upload, so
               NAME-EXACT is a real check on this version's contents rather than on a union with v1's.

  --dry-run    runs every guard above and stops before the first network call.

The token is read from .env and never printed.
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zenodo_publish_two_barriers as v1  # noqa: E402  (config + guards, single source of truth)

RECORD_ID = 21782600                       # the v1 record this versions

META = copy.deepcopy(v1.META)
META["metadata"]["version"] = "v2"
META["metadata"]["description"] += (
    "<p><strong>v2 (2026-08-03): two corrections, both narrowing a closure claim.</strong> Adversarial "
    "self-audit of v1 produced two successive retractions on the day of release, both in the same direction -- "
    "a door was claimed shut that was not. (a) v1 said the mechanism &quot;cannot be made to yield a "
    "smaller&quot; coefficient; that is a claim about ALL inertia functionals, but only functionals of the local "
    "de Sitter-Unruh TEMPERATURE were examined, and functionals of the full response F(E) -- where the paper's "
    "own KMS result forces T_eff to be gap-dependent for every nonzero orbital frequency -- were never computed "
    "(mi_orbital_q_selfaudit_2026.py). (b) The rigidity theorem that briefly replaced it is ALSO withdrawn: the "
    "Newtonian limit forces f to be asymptotically linear, but the deep limit reads f-prime AT THE FLOOR, and "
    "nothing connects two different points on f; the five functions tested were all scale-free, for which the "
    "two slopes coincide. The correct statement, derived in the new section 3.3, is the closed form "
    "q = 2 c1prime / f-prime(T_GH), so the temperature class is a ONE-PARAMETER family in "
    "r = f-prime(T_GH)/c1prime with q = 2/r. Milgrom (1999)'s f = T is the r = 1 member; Milgrom (2020)'s "
    "coefficient requires r = 4 pi EXACTLY; kappa = 1/2 requires r = 2Z = 8 sqrt(6 pi)/3 = 11.577620, and an "
    "explicit smooth, strictly increasing, asymptotically linear f delivering q = 1/Z exactly is given "
    "(mi_crossover_master_formula_2026.py, 14/14). The mechanism therefore does NOT fix the coefficient. It "
    "fixes the question: since the a0-line is identically Milgrom's balance with the floor at a0/2, the two "
    "apparent freedoms are one factor 2Z, and what is open is whether the de Sitter floor is c H_Lambda, fixed "
    "by the horizon, or (1/4) c sqrt(G rho_Lambda) -- a BARE sqrt(G rho) carrying no Friedmann 8pi/3. "
    "AGAINST THIS FRAMEWORK'S INTEREST: r is itself unfixed, so this is a reparametrisation and NOT a "
    "derivation of kappa; Milgrom (2020)'s r = 4 pi is exact and a horizon-area or solid-angle normalisation "
    "supplies 4 pi, though the converse objection does NOT hold, since 2Z = 4 sqrt(8 pi/3) makes its sqrt(pi) "
    "the FRIEDMANN factor's and an arithmetic-naturalness argument against 2Z would be spurious "
    "(mi_2Z_is_the_friedmann_root_2026.py, 8/8); the substantive objection is Deser and Levin's, that the horizon "
    "FIXES the floor at H, so H is mechanism-given and sqrt(G rho_Lambda) is a substitution for it, and nothing "
    "here defeats that; and whether an r = 2Z kernel survives the solar-system ephemeris bound and "
    "the 30.6% shape range is untested. What survives unchanged: the orbital invariance of q, the value q = 2 "
    "for Milgrom's own f = T, and the entire 30.6% shape systematic. kappa = 1/2 remains FITTED, NOT "
    "DERIVED.</p>")

BANNERS = ["**v2 (2026-08-03), two corrections, both narrowing a closure claim.**",
           "### 3.3 The crossover is a one-parameter family, not a fixed number (v2)"]
GONE = ["cannot be made to yield a smaller one",          # v1's unscoped no-go
        "THE TWO LIMITS TOGETHER FORCE f LINEAR"]         # v2(a)'s withdrawn theorem
NEEDED = ["mi_orbital_q_selfaudit_2026.py", "mi_crossover_master_formula_2026.py"]


def main():
    tok = v1.token()

    # ---- V2-DIFF: refuse to mint a version that changes nothing ----------------------
    paper = open(os.path.join(v1.REPO, v1.PAPER), encoding="utf-8").read()
    corpus = paper + "".join(open(os.path.join(v1.REPO, f), encoding="utf-8").read() for f in v1.SCRIPTS)
    for b in BANNERS:
        if b not in paper:
            sys.exit(f"ERROR V2-DIFF: the paper is missing {b!r} -- refusing to mint a version")
    for g in GONE:
        if g in corpus:
            sys.exit(f"ERROR V2-DIFF: withdrawn claim {g!r} still asserted somewhere in the record -- "
                     "the correction was not applied everywhere")
    for nd in NEEDED:
        if nd not in paper:
            sys.exit(f"ERROR V2-DIFF: {nd} is not cited in the paper -- refusing")
    print(f"V2-DIFF ok: {len(BANNERS)} banners present, {len(GONE)} withdrawn claims absent from paper AND all "
          f"{len(v1.SCRIPTS)} scripts, {len(NEEDED)} corrections cited")

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

    if "--dry-run" in sys.argv:
        print("\nDRY RUN: every local guard passed. Stopping before the first network call; nothing published.")
        return

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
