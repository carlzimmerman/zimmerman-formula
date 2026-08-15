#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t082_frozen_guard.py -- T082: Frozen-file guard.

Spec (verbatim from TASKS.md): "Script that hashes PREREGISTRATION_DR4.md + all
*_HASH.txt and fails if any differ from the committed digests. PASS: green run."

WHAT IT DOES
 - Frozen set = { prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md }
                 + every repo-wide file whose name matches *_HASH.txt
    (the 10 AMENDMENT*_HASH.txt amendment-chain digests). NOTE: FREEZE_HASHES.txt
    does NOT match the glob *_HASH.txt (it ends in "HASHES.txt"), so it is out of
    scope for this task as written.
 - For each frozen file: working_tree_sha256 vs COMMITTED_DIGEST, where
    COMMITTED_DIGEST = sha256( git show HEAD:<relpath> ).  A mismatch means a frozen
    artifact was edited on disk without being committed -> TAMPER -> FAIL.  A frozen
    file with no committed baseline (untracked / deleted at HEAD) -> FAIL: you cannot
    guard a frozen file that has no frozen reference.
 - Exit 0 (green = PASS) iff every frozen file matches its committed digest.
   Exit 1 otherwise, listing every offender.

WHY THIS CANNOT TRIVIALLY PASS (DEFICIT-risk mitigation)
 The dangerous failure mode for a guard is a FALSE PASS -- a guard that always goes
 green no matter what (e.g. comparing a file against a digest it recomputes on the
 spot, or comparing a file to itself).  Here the expected digest is read from the
 git-committed blob, an EXTERNAL frozen reference the script cannot regenerate without
 a `git commit`.  So tampering the working tree without committing is caught.

This is a tamper-evidence / integrity guard, NOT a physics claim.  It only READS the
frozen files and only READS git; it never writes or touches them.
"""
import sys, os, glob, hashlib, subprocess, datetime

RUNS = os.path.dirname(os.path.abspath(__file__))      # .../qwen_38_experiment/runs
EXPERIMENT = os.path.dirname(RUNS)                     # .../qwen_38_experiment
ROOT = os.path.dirname(EXPERIMENT)                     # repo root
REPORT = os.path.join(RUNS, "frozen_guard_report.txt")

PREREG = "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"   # the frozen pre-registration


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def committed_digest(relpath):
    """sha256 of the git-committed blob at HEAD for relpath; None if not committed."""
    try:
        p = subprocess.run(["git", "show", "HEAD:" + relpath], cwd=ROOT,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    return sha256_bytes(p.stdout)


def main():
    # ---- discover the frozen set ----
    frozen = [PREREG]
    for p in sorted(glob.glob(os.path.join(ROOT, "**", "*_HASH.txt"), recursive=True)):
        rp = os.path.relpath(p, ROOT)
        if rp not in frozen:
            frozen.append(rp)
    frozen = sorted(set(frozen))

    # ---- check each frozen file against its committed digest ----
    results = []   # (relpath, status, detail)
    for rp in frozen:
        abs_p = os.path.join(ROOT, rp)
        if not os.path.exists(abs_p):
            results.append((rp, "MISSING", "frozen file absent on disk"))
            continue
        cur = sha256_file(abs_p)
        committed = committed_digest(rp)
        if committed is None:
            results.append((rp, "NOT-COMMITTED",
                            "no HEAD baseline to compare against (cannot guard)"))
            continue
        if cur == committed:
            results.append((rp, "OK", cur[:16] + "..."))
        else:
            results.append((rp, "MISMATCH",
                            "working %s... != committed %s..." % (cur[:16], committed[:16])))

    offenders = [r for r in results if r[1] != "OK"]

    # ---- report ----
    lines = []
    lines.append("T082 FROZEN-FILE GUARD   %s" % datetime.date.today())
    lines.append("frozen set: %d file(s)   OK: %d   OFFENDERS: %d"
                 % (len(results), len(results) - len(offenders), len(offenders)))
    lines.append("=" * 78)
    for rp, status, detail in results:
        lines.append("%-11s %-46s %s" % (status, rp, detail))
    lines.append("=" * 78)
    if offenders:
        lines.append("VERDICT: FAIL -- %d frozen file(s) drifted from their committed digest"
                     % len(offenders))
    else:
        lines.append("VERDICT: PASS -- all %d frozen file(s) match their committed digests"
                     % len(results))
    with open(REPORT, "w") as f:
        f.write("\n".join(lines) + "\n")

    # ---- stdout summary ----
    print("T082 frozen-file guard: %d frozen file(s)" % len(results))
    for rp, status, detail in results:
        print("   %-11s %-46s %s" % (status, rp, detail))
    print("=" * 78)
    print("REPORT -> %s" % os.path.relpath(REPORT, ROOT))
    if offenders:
        print("FAIL: %d frozen file(s) differ from committed digest" % len(offenders))
        return 1
    print("PASS: all frozen files match committed digests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
