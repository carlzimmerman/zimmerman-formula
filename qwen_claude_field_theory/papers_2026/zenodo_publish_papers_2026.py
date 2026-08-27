#!/usr/bin/env python3
"""Create and publish the two 2026-08-27 Zenodo deposits (Paper 1: carrier no-gos + DW audit;
Paper 2: MMG conditional closure). Carries the earned guards:

  LOCAL-PRESENCE  every file must exist on disk before anything is created.
  SCRIPTS-GREEN   every included .py must exit 0 (120 s timeout each).
  NAME-EXACT      server file names must match the intended set exactly.
  METADATA-SANE   title, version, creators, license present and non-empty.
  NO-PII          markdown + metadata scanned for e-mails/phones; refuse on hit.
  DRY-RUN default -- pass --publish to actually create and publish.

Reads ZENODO_ACCESS_TOKEN from /Users/carlzimmerman/new_physics/.env -- never printed.
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

ENV = "/Users/carlzimmerman/new_physics/.env"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
PAP = "qwen_claude_field_theory/papers_2026"
CLO = "qwen_claude_field_theory/closure_2026"
FRC = "qwen_claude_field_theory/fried_chicken_exact_exponential_v2/scripts"
MMG = "openai_push/final_closure"
BASE = "https://zenodo.org/api"

DEPOSITS = [
    {
        "stem": "PAPER1_carrier_nogos_and_dw_audit",
        "meta": f"{PAP}/PAPER1_carrier_nogos_and_dw_audit.zenodo.json",
        "files": [
            f"{PAP}/PAPER1_carrier_nogos_and_dw_audit.md",
            f"{CLO}/sf40_general_F_hessian_nogo_2026.py",
            f"{CLO}/sf41_isolated_zero_dirac_2026.py",
            f"{CLO}/sf42_aux_legendre_dof_2026.py",
            f"{CLO}/sf42_flrw_expansion_hessian_2026.py",
            f"{CLO}/sf43_dw_localized_dof_ghost_2026.py",
            f"{CLO}/sf44_dw_physical_phase_space_2026.py",
            f"{FRC}/verify_stability_and_crossing.py",
        ],
    },
    {
        "stem": "PAPER2_mmg_conditional_closure",
        "meta": f"{PAP}/PAPER2_mmg_conditional_closure.zenodo.json",
        "files": [
            f"{PAP}/PAPER2_mmg_conditional_closure.md",
            "qwen_claude_field_theory/FINAL_THEORY_MMG_CONSOLIDATED_2026-08-27.md",
            f"{MMG}/run_all.sh",
            f"{MMG}/scripts/01_constitutive.py",
            f"{MMG}/scripts/02_newtonian_limit.py",
            f"{MMG}/scripts/03_dirac_matrix.py",
            f"{MMG}/scripts/04_rank_and_ellipticity.py",
            f"{MMG}/scripts/05_dof_count.py",
            f"{MMG}/scripts/06_constraint_preservation.py",
            f"{MMG}/scripts/07_tensor_sector.py",
            f"{MMG}/scripts/08_matter_consistency.py",
            f"{MMG}/scripts/09_legendre_check.py",
            f"{MMG}/scripts/12_falsification.py",
            f"{MMG}/scripts/13_kernel_swap_ellipticity.py",
        ],
    },
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")


def token():
    for line in open(ENV):
        if line.startswith("ZENODO_ACCESS_TOKEN"):
            return line.split("=", 1)[1].strip()
    sys.exit("FATAL: ZENODO_ACCESS_TOKEN not found in .env")


def api(tok, method, path, data=None, headers=None, raw=False):
    url = f"{BASE}{path}{'&' if '?' in path else '?'}access_token={tok}"
    body = data if raw else (json.dumps(data).encode() if data is not None else None)
    req = urllib.request.Request(url, data=body, method=method,
                                 headers=headers or {"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def guard(dep):
    ok = True
    for f in dep["files"] + [dep["meta"]]:
        p = os.path.join(REPO, f)
        if not os.path.exists(p):
            print(f"  [FAIL] missing: {f}"); ok = False
    if not ok:
        return False
    print("  [ok] LOCAL-PRESENCE")
    for f in dep["files"]:
        if f.endswith(".py"):
            r = subprocess.run([sys.executable, os.path.join(REPO, f)],
                               capture_output=True, timeout=120, cwd=REPO)
            if r.returncode != 0:
                print(f"  [FAIL] script red: {f}"); ok = False
    if not ok:
        return False
    print("  [ok] SCRIPTS-GREEN")
    meta = json.load(open(os.path.join(REPO, dep["meta"])))["metadata"]
    for k in ("title", "version", "creators", "license"):
        if not meta.get(k):
            print(f"  [FAIL] metadata field empty: {k}"); ok = False
    if ok:
        print("  [ok] METADATA-SANE")
    blob = json.dumps(meta) + "".join(
        open(os.path.join(REPO, f), errors="ignore").read()
        for f in dep["files"] if f.endswith(".md"))
    # allow the author-identifying repo URL; scan for emails/phones
    hits = [m for m in EMAIL_RE.findall(blob) if "noreply" not in m] + PHONE_RE.findall(blob)
    if hits:
        print(f"  [FAIL] NO-PII: {len(hits)} hit(s)"); ok = False
    else:
        print("  [ok] NO-PII")
    return ok


def publish(dep, tok):
    meta = json.load(open(os.path.join(REPO, dep["meta"])))
    d = api(tok, "POST", "/deposit/depositions", meta)
    dep_id, bucket = d["id"], d["links"]["bucket"]
    print(f"  created deposition {dep_id}")
    for f in dep["files"]:
        name = os.path.basename(f)
        with open(os.path.join(REPO, f), "rb") as fh:
            api(tok, "PUT", f"{bucket.replace(BASE,'')}/{name}", fh.read(),
                headers={"Content-Type": "application/octet-stream"}, raw=True)
        print(f"    uploaded {name}")
    server = {x["filename"] for x in api(tok, "GET", f"/deposit/depositions/{dep_id}")["files"]}
    want = {os.path.basename(f) for f in dep["files"]}
    if server != want:
        sys.exit(f"FATAL NAME-EXACT: server {server ^ want}")
    print("  [ok] NAME-EXACT")
    pub = api(tok, "POST", f"/deposit/depositions/{dep_id}/actions/publish")
    print(f"  PUBLISHED: doi={pub['doi']}  concept={pub.get('conceptdoi','')}")
    return pub["doi"]


if __name__ == "__main__":
    do_publish = "--publish" in sys.argv
    tok = token() if do_publish else None
    dois = []
    for dep in DEPOSITS:
        print(f"== {dep['stem']} ==")
        if not guard(dep):
            sys.exit(f"GUARDS FAILED for {dep['stem']} -- nothing created")
        if do_publish:
            dois.append((dep["stem"], publish(dep, tok)))
        else:
            print("  DRY-RUN ok (pass --publish to create+publish)")
    for stem, doi in dois:
        print(f"{stem}: {doi}")
