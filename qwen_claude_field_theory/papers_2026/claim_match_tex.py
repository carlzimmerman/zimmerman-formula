#!/usr/bin/env python3
"""claim_match_tex.py — does every number in a LaTeX paper match the committed output it rests on?

The LaTeX twin of project_atomos/CLAIM_MATCH.py (after Craig, arXiv:2610.09093 sec. 12, where formal statements
get a separate correspondence review). A paper's own <paper>_audit.py checks the numbers someone chose to tag;
this checks EVERY sentence or table row containing a digit (preamble, comments and the bibliography excepted):

  * each claim is keyed by a hash of its text;
  * <stem>.claim_review.json (next to the .tex) holds a verdict per claim and the source files that carry it,
    each with its sha256 at review time (paths relative to the repo root);
  * FAIL if a claim is unreviewed, its verdict is not MATCH or CONTEXT, or a cited source changed or vanished.

Verdicts: MATCH, CONTEXT (digits that are not results: dates, section numbers, DOIs, years, equation labels),
OVERSTATES, WRONG, UNSUPPORTED. The review records judgements; this script only enforces them.

Usage:  python3 claim_match_tex.py PAPER.tex             check (exit 0 iff all pass)
        python3 claim_match_tex.py PAPER.tex --packets   write <stem>.claim_packets.json for reviewers
        MUTATE=1 python3 claim_match_tex.py PAPER.tex    controls: an edited claim and a changed source must be caught
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def repo_root(p):
    out = subprocess.run(["git", "-C", str(p.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else p.parent


def file_sha(root, rel):
    q = root / rel
    return hashlib.sha256(q.read_bytes()).hexdigest()[:16] if q.is_file() else None


def claims(tex):
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    m = re.search(r"\\begin\{document\}", tex)
    body = tex[m.end():] if m else tex
    body = re.split(r"\\begin\{thebibliography\}|\\bibliography\{", body)[0]
    out, sec = [], "front"
    for block in re.split(r"\n\s*\n", body):
        sm = re.search(r"\\(?:sub)*section\*?\{([^}]*)\}", block)
        if sm:
            sec = sm.group(1)
        for row in re.split(r"\\\\", block):
            for s in re.split(r"(?<=[.;])\s+(?=[A-Z\\$(])", row):
                s = re.sub(r"\s+", " ", s).strip()
                plain = re.sub(r"\\(?:label|ref|eqref|cite[pt]?|includegraphics|section|subsection)\*?(\[[^]]*\])?\{[^}]*\}", "", s)
                if re.search(r"\d", plain) and len(plain) > 12:
                    out.append({"id": h(s), "section": sec, "text": s})
    return out


def check(cl, review, sha):
    problems = []
    for c in cl:
        r = review.get(c["id"])
        if r is None:
            problems.append(f"UNREVIEWED [{c['section'][:20]}]: {c['text'][:90]}")
            continue
        if r.get("verdict") not in ("MATCH", "CONTEXT"):
            problems.append(f"{r.get('verdict')} [{c['section'][:20]}]: {c['text'][:70]} -- {r.get('note', '')[:160]}")
        for s in r.get("sources", []):
            if sha(s["path"]) != s.get("sha"):
                problems.append(f"STALE: {c['id']} source {s['path']} changed or missing since review")
    return problems


def main():
    paper = Path(sys.argv[1]).resolve()
    root = repo_root(paper)
    rev_path = paper.with_suffix(".claim_review.json")
    cl = claims(paper.read_text())
    review = json.loads(rev_path.read_text())["claims"] if rev_path.exists() else {}
    sha = lambda rel: file_sha(root, rel)
    if "--packets" in sys.argv:
        out = paper.with_suffix(".claim_packets.json")
        out.write_text(json.dumps(cl, indent=1, ensure_ascii=False))
        print(f"{len(cl)} claims -> {out.name}")
        return 0
    if os.environ.get("MUTATE") == "1":
        reviewed = [c for c in cl if review.get(c["id"], {}).get("sources")]
        if not reviewed:
            print("MUTATE: no reviewed claim with sources; controls cannot run")
            return 1
        c0 = reviewed[0]
        edited = [dict(c, id=h(c["text"] + " (edited)")) if c is c0 else c for c in cl]
        c1 = any(p.startswith("UNREVIEWED") for p in check(edited, review, sha))
        src = review[c0["id"]]["sources"][0]["path"]
        c2 = any(p.startswith(f"STALE: {c0['id']}") for p in
                 check(cl, review, lambda p: "0" * 16 if p == src else sha(p)))
        print(f"MUTATE: edited claim caught: {c1}; changed source ({src}) caught: {c2}")
        print("MUTATE: controls PASS" if c1 and c2 else "MUTATE: controls FAIL")
        return 0 if c1 and c2 else 1
    problems = check(cl, review, sha)
    counts = {}
    for c in cl:
        v = review.get(c["id"], {}).get("verdict", "UNREVIEWED")
        counts[v] = counts.get(v, 0) + 1
    print(f"{paper.name}: {len(cl)} claims; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for p in problems:
        print("  " + p)
    print("CLAIM-MATCH: FAIL" if problems else "CLAIM-MATCH: PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
