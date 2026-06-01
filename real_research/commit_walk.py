#!/usr/bin/env python3
"""
Walk EVERY commit in the repo, one by one, and classify it.
===========================================================

Carl asked for a commit-by-commit walk of the whole history. This processes all ~1669
commits (oldest -> newest) in a single git pass, classifies each by content, dates the
first appearance of each category, and writes a complete per-commit ledger to
COMMIT_LEDGER.csv. The substantive physics-claim commits (the ones whose MATH must be
checked) are flagged so they can be verified by hand -- they cluster in the early
"sound era" (before the 2026-03-26 numerology pivot found in COMMIT_WALK.md).

Run:  python real_research/commit_walk.py
"""

import csv
import os
import re
import subprocess
from collections import Counter, OrderedDict

PIVOT = "2026-03-26"   # the 'CUBE vertices' numerology pivot (ee1370d6)
OUT = os.path.join(os.path.dirname(__file__), "COMMIT_LEDGER.csv")


def get_commits():
    raw = subprocess.run(
        ["git", "log", "--reverse", "--numstat", "--date=short",
         "--format=@@C@@\t%H\t%ad\t%s"],
        capture_output=True, text=True).stdout
    commits, cur = [], None
    for line in raw.splitlines():
        if line.startswith("@@C@@"):
            if cur:
                commits.append(cur)
            _, h, d, s = line.split("\t", 3)
            cur = {"hash": h[:8], "date": d, "msg": s, "files": [], "add": 0, "del": 0}
        elif line.strip() and cur is not None and "\t" in line:
            p = line.split("\t")
            if len(p) == 3:
                a, r, f = p
                cur["files"].append(f)
                cur["add"] += int(a) if a.isdigit() else 0
                cur["del"] += int(r) if r.isdigit() else 0
    if cur:
        commits.append(cur)
    return commits


def classify(c):
    t = (c["msg"] + " " + " ".join(c["files"])).lower()
    if re.search(r"hermesflow|truthflow|olympusflow|metisflow|alpheus|cyllene|ergon|"
                 r"briareus|mnemosyne|aletheia|helicon|legomena|daemon|autonomous|"
                 r"blind_test|swarm|_outputs/|orchestrat", t):
        return "agent-infra"
    if re.search(r"biotech|protein|\bpdb\b|abiogen|docking|cftr|amyloid|\bdrug|chembl|"
                 r"prolactin|cas9|amp_design|alphafold|peptide|protogonos|resonance", t):
        return "biotech"
    if re.search(r"\b137\b|fine.?struct|alpha.?inv|alpha-1|sin2|weinberg|\bproton\b|"
                 r"mass.?ratio|pattern_search|phenomenolog|numerolog|53.?constant|"
                 r"60.?deriv|100.?deriv|standard.?model", t):
        return "numerology-constants"
    if re.search(r"\bcube\b|\bsphere\b|orbifold|topolog|32pi|\bz2\b|z\^2|z²|20\.6|"
                 r"entangle|eta.?invariant|holonom|wilson", t):
        return "numerology-geometry/topology"
    if re.search(r"meteorolog|hurricane|sunspot|weather|era5|venus|mars|exoplanet|"
                 r"ligo|nanograv|frb|parity|chirality|ghost|matched.?circle|4pcf|"
                 r"offensive", t):
        return "other-domain-tests"
    if re.search(r"\bmond\b|sparc|\ba0\b|rotation|\brar\b|tully|lensing|bullet|core.?cusp|"
                 r"cosmolog|hubble|\bh0\b|dark.?energy|critical.?density|zimmerman.?formula|"
                 r"acceleration.?scale|kinematic|jwst|btfr|dispersion", t):
        return "MOND-cosmology"
    if re.search(r"readme|honest|assessment|audit|cleanup|refactor|license|reorganiz|"
                 r"\.md|\.tex|guide|summary|report|disclaimer", t):
        return "docs/meta"
    return "other"


def is_claim(c, cat):
    """Heuristic: does this commit INTRODUCE a physics claim whose math should be checked?"""
    t = (c["msg"] + " " + " ".join(c["files"])).lower()
    new_theory = any(("core_theory" in f or "/papers/" in f or f.endswith(".tex"))
                     for f in c["files"])
    kw = re.search(r"deriv|formula|predict|proof|theorem|relation|derive|equation", t)
    return cat in ("MOND-cosmology",) and (new_theory or bool(kw))


def main():
    commits = get_commits()
    n = len(commits)
    print(f"walked {n} commits ({commits[0]['date']} -> {commits[-1]['date']})\n")

    # write full ledger
    with open(OUT, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["idx", "hash", "date", "era", "category", "claim", "+", "-", "n_files", "message"])
        for i, c in enumerate(commits, 1):
            cat = classify(c)
            era = "sound" if c["date"] < PIVOT else "sprawl"
            w.writerow([i, c["hash"], c["date"], era, cat, int(is_claim(c, cat)),
                        c["add"], c["del"], len(c["files"]), c["msg"][:90]])
    print(f"full per-commit ledger -> {os.path.relpath(OUT)}\n")

    # category x era table
    tab = Counter((("sound" if c["date"] < PIVOT else "sprawl"), classify(c)) for c in commits)
    cats = sorted({k[1] for k in tab})
    print(f"{'category':<32}{'sound':>8}{'sprawl':>8}{'total':>8}")
    for cat in cats:
        s, p = tab[("sound", cat)], tab[("sprawl", cat)]
        print(f"   {cat:<29}{s:>8}{p:>8}{s+p:>8}")
    print(f"   {'TOTAL':<29}{sum(1 for c in commits if c['date']<PIVOT):>8}"
          f"{sum(1 for c in commits if c['date']>=PIVOT):>8}{n:>8}")
    print()

    # first appearance of each category (the provenance timeline)
    first = OrderedDict()
    for i, c in enumerate(commits, 1):
        cat = classify(c)
        if cat not in first:
            first[cat] = (i, c["date"], c["hash"], c["msg"][:60])
    print("first appearance of each category (when it entered the repo):")
    for cat, (i, d, h, m) in sorted(first.items(), key=lambda kv: kv[1][0]):
        print(f"   #{i:<4} {d}  {h}  {cat:<28} {m}")
    print()

    # the substantive physics-claim commits to verify by hand
    claims = [(i, c) for i, c in enumerate(commits, 1) if is_claim(c, classify(c))]
    print(f"physics-claim commits to verify by hand: {len(claims)} "
          f"({sum(1 for i,c in claims if c['date']<PIVOT)} in the sound era)")
    for i, c in claims[:25]:
        print(f"   #{i:<4} {c['date']}  {c['hash']}  {c['msg'][:70]}")
    if len(claims) > 25:
        print(f"   ... and {len(claims)-25} more (see ledger)")


if __name__ == "__main__":
    main()
