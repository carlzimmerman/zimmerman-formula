#!/usr/bin/env python3
"""CLAIM_MATCH.py — does every number in PAPER_ATOMOS_NULL.md match the committed output it rests on?

The atomos analogue of ChainCert's statement match (zimmerman-formula, after Craig arXiv:2610.09093 sec. 12).
VERIFY_ALL.sh re-derives the machinery; it cannot tell whether the PAPER says what the outputs say. Here:

  1. every sentence/bullet of the paper that contains a digit (References excepted) is a claim, keyed by a hash of
     its text;
  2. each claim needs an entry in CLAIM_MATCH_REVIEW.json: a verdict and the committed source file(s) that carry it,
     each with the sha256 of the file at review time;
  3. FAIL if a claim has no entry, if its verdict is not MATCH or CONTEXT, or if a cited source file changed or
     vanished since review (stale) — so editing the paper or regenerating an output forces a re-review.

Verdicts: MATCH (the number is in the cited output, to the stated precision); CONTEXT (the digits are not a result:
a date, depth label, section number, DOI, citation year); OVERSTATES; WRONG; UNSUPPORTED (no committed output
carries it). The review records judgements; this script only enforces that they exist, are current, and pass.

Usage:  python3 CLAIM_MATCH.py            check (exit 0 iff all pass)
        python3 CLAIM_MATCH.py --packets  write CLAIM_MATCH_PACKETS.json for reviewers
        MUTATE=1 python3 CLAIM_MATCH.py   controls: an edited claim and a changed source must both be caught
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE / "PAPER_ATOMOS_NULL.md"
REVIEW = HERE / "CLAIM_MATCH_REVIEW.json"
PACKETS = HERE / "CLAIM_MATCH_PACKETS.json"
PASSING = {"MATCH", "CONTEXT"}


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def file_sha(p):
    q = HERE / p
    return hashlib.sha256(q.read_bytes()).hexdigest()[:16] if q.is_file() else None


def claims(text):
    out, sec = [], "front"
    for b in re.split(r"\n\s*\n", text):
        if b.startswith("#"):
            sec = b.split("\n")[0].lstrip("# ").strip()
            b = "\n".join(b.split("\n")[1:])
        if sec.startswith("References"):
            continue
        for s in re.split(r"(?<=[.;])\s+(?=[A-Z*(`|-])|\n(?=\s*[-*|] )", b):
            s = re.sub(r"\s+", " ", s).strip()
            if re.search(r"\d", s) and len(s) > 15:
                out.append({"id": h(s), "section": sec, "text": s})
    return out


def check(cl, review, sha=file_sha):
    problems = []
    for c in cl:
        r = review.get(c["id"])
        if r is None:
            problems.append(f"UNREVIEWED [{c['section'][:20]}]: {c['text'][:90]}")
            continue
        if r.get("verdict") not in PASSING:
            problems.append(f"{r.get('verdict')} [{c['section'][:20]}]: {c['text'][:70]} -- {r.get('note', '')}")
        for s in r.get("sources", []):
            if sha(s["path"]) != s.get("sha"):
                problems.append(f"STALE: {c['id']} source {s['path']} changed or missing since review")
    return problems


def main():
    cl = claims(PAPER.read_text())
    review = json.loads(REVIEW.read_text())["claims"] if REVIEW.exists() else {}
    if "--packets" in sys.argv:
        PACKETS.write_text(json.dumps(cl, indent=1, ensure_ascii=False))
        print(f"{len(cl)} claims -> {PACKETS.name}")
        return 0
    if os.environ.get("MUTATE") == "1":
        reviewed = [c for c in cl if c["id"] in review and review[c["id"]].get("sources")]
        if not reviewed:
            print("MUTATE: no reviewed claim with sources; controls cannot run")
            return 1
        c0 = reviewed[0]
        edited = [dict(c, id=h(c["text"] + " (edited)")) if c is c0 else c for c in cl]
        c1 = any(p.startswith("UNREVIEWED") for p in check(edited, review))
        src = review[c0["id"]]["sources"][0]["path"]
        c2 = any(p.startswith(f"STALE: {c0['id']}") for p in
                 check(cl, review, sha=lambda p: "0" * 16 if p == src else file_sha(p)))
        print(f"MUTATE: edited claim caught: {c1}; changed source ({src}) caught: {c2}")
        print("MUTATE: controls PASS" if c1 and c2 else "MUTATE: controls FAIL")
        return 0 if c1 and c2 else 1
    problems = check(cl, review)
    counts = {}
    for c in cl:
        v = review.get(c["id"], {}).get("verdict", "UNREVIEWED")
        counts[v] = counts.get(v, 0) + 1
    print(f"claims: {len(cl)}; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for p in problems:
        print("  " + p)
    print("CLAIM-MATCH: FAIL" if problems else "CLAIM-MATCH: PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
