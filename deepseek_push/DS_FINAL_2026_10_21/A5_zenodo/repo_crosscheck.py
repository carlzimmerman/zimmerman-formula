#!/usr/bin/env python3
"""Cross-check every Zenodo record against the local repository.

Three probes per record, all fixed-string (no regex semantics from content):
  1. DOI probes       10.5281/zenodo.<id>  and bare  zenodo.<id>
  2. title shingles   two 4-word shingles from the title (content words only)
  3. number probes    up to 6 distinctive numbers taken from the abstract
                      (>=5 chars and containing '.' or an exponent)

Output _zenodo/repo_hits.json:
  {id: {"doi_hits": n, "doi_files": [...], "title_hits": n, "title_files": [...],
        "number_hits": {num: {"n": n, "files": [...]}}, "any": bool}}

Excludes deepseek_push/DS_FINAL_2026_10_21 (this lane) and VCS/venv/binary
paths.  Read-only: touches nothing outside the lane.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHE = os.path.join(HERE, "_zenodo")

EXCLUDES = [
    "!**/deepseek_push/DS_FINAL_2026_10_21/**",
    "!**/deepseek_push/FINAL_2026_10_21/**",
    "!**/_zenodo/**",
    "!.git/**", "!**/.venv*/**", "!**/venv*/**", "!**/__pycache__/**",
    "!**/node_modules/**", "!**/.ruff_cache/**", "!**/.research-cache/**",
    "!**/*.npz", "!**/*.npy", "!**/*.bin", "!**/*.pkl", "!**/*.h5",
    "!**/*.fits", "!**/*.png", "!**/*.jpg", "!**/*.jpeg", "!**/*.pdf",
    "!**/*.pt", "!**/*.gif", "!**/*.mp4", "!**/*.zip", "!**/*.gz",
]
GLOBS = ["*.md", "*.txt", "*.py", "*.json", "*.out", "*.tex", "*.csv",
         "*.yaml", "*.yml", "*.html", "*.lean", "*.sh", "*.log", "*.ipynb",
         "*.rst", "*.cff"]

STOP = set("the a an of for and to in on with from by as is are at into its "
           "this that these those what which why how we our you your".split())


def shingles(title, k=4):
    words = re.findall(r"[A-Za-z][A-Za-z0-9'\-]+", title.lower())
    words = [w for w in words if w not in STOP and len(w) > 2]
    out = []
    for i in range(0, max(1, len(words) - k + 1)):
        s = " ".join(words[i:i + k])
        if len(s) >= 18:
            out.append(s)
    # pick two spread across the title
    if not out:
        return []
    if len(out) == 1:
        return out
    return [out[0], out[len(out) // 2]]


NUMOK = re.compile(r"^[-+]?(\d+\.\d+|\d+(\.\d+)?[eE][-+]?\d+)")


def sig_digits(s):
    m = re.match(r"^[-+]?(\d+)(?:\.(\d+))?(?:[eE][-+]?\d+)?$", s.strip())
    if not m:
        return 0
    digits = (m.group(1) + (m.group(2) or "")).lstrip("0")
    return len(digits)


def number_probes(nums):
    """Keep only numbers distinctive enough that a repo hit means something.

    A raw 4-digit decimal such as 0.002 occurs 36k times in this repository and
    is evidence of nothing; require >= 3 significant digits and >= 5 chars, or
    an explicit exponent with a >= 3-digit mantissa.
    """
    out = []
    for n in nums:
        n = n.strip()
        if not NUMOK.match(n):
            continue
        sd = sig_digits(n)
        has_exp = "e-" in n.lower() or "e+" in n.lower()
        if has_exp and sd >= 3 and len(n) >= 7:
            out.append(n)
        elif (not has_exp) and sd >= 3 and len(n) >= 5:
            out.append(n)
    out = sorted(set(out), key=lambda s: (-len(s), s))
    return out[:6]


def rg_count(patterns, files_with_matches=False):
    """Return dict pattern -> (count, [files]) using one rg invocation."""
    pf = os.path.join(CACHE, "_pats.txt")
    with open(pf, "w") as f:
        for p in patterns:
            f.write(p.replace("\n", " ") + "\n")
    cmd = ["rg", "-F", "-f", pf, "--no-heading", "--with-filename",
           "--max-count", "200", "-o"]
    for e in EXCLUDES:
        cmd += ["-g", e]
    for g in GLOBS:
        cmd += ["-g", g]
    cmd += ["."]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    hits = {}
    for line in r.stdout.splitlines():
        # path:match
        if ":" not in line:
            continue
        path, _, match = line.rpartition(":")
        hits.setdefault(match, {"n": 0, "files": []})
        h = hits[match]
        h["n"] += 1
        if path not in h["files"] and len(h["files"]) < 8:
            h["files"].append(path)
    return hits


def main():
    recs = json.load(open(os.path.join(CACHE, "all_records.json")))
    ext = json.load(open(os.path.join(CACHE, "extract.json")))
    num_by_id = {o["id"]: o["numbers"] for o in ext}

    probe_map = {}   # pattern -> list of (id, kind)
    for r in recs:
        rid = r["id"]
        for p in (f"zenodo.{rid}", str(rid)):
            probe_map.setdefault(p, []).append((rid, "doi"))
        for s in shingles(r["title"]):
            probe_map.setdefault(s, []).append((rid, "title"))
        for n in number_probes(num_by_id.get(rid, [])):
            probe_map.setdefault(n, []).append((rid, "num"))

    print(f"records={len(recs)} probes={len(probe_map)}", flush=True)
    hits = rg_count(list(probe_map))
    print(f"probes_with_hits={len(hits)}", flush=True)

    out = {}
    for r in recs:
        rid = r["id"]
        row = {"doi_hits": 0, "doi_files": [], "title_hits": 0,
               "title_files": [], "number_hits": {}, "any": False}
        for pat, owners in probe_map.items():
            for (oid, kind) in owners:
                if oid != rid:
                    continue
                h = hits.get(pat)
                if not h:
                    continue
                if kind == "doi":
                    row["doi_hits"] += h["n"]
                    row["doi_files"] = sorted(set(row["doi_files"] + h["files"]))[:8]
                elif kind == "title":
                    row["title_hits"] += h["n"]
                    row["title_files"] = sorted(set(row["title_files"] + h["files"]))[:8]
                else:
                    row["number_hits"][pat] = {"n": h["n"], "files": h["files"][:4]}
                    ev = [f for f in h["files"]
                          if not re.search(r"/papers[^/]*/", f)
                          and not f.endswith((".tex", ".pdf", ".zenodo.json"))]
                    if ev and sum(1 for (o2, k2) in probe_map[pat] if k2 == "num") <= 2:
                        row.setdefault("evidence_hits", {})[pat] = ev[:4]
        row["any"] = bool(row["doi_hits"] or row["title_hits"] or row["number_hits"])
        out[str(rid)] = row

    with open(os.path.join(CACHE, "repo_hits.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    n_any = sum(1 for v in out.values() if v["any"])
    n_doi = sum(1 for v in out.values() if v["doi_hits"])
    n_title = sum(1 for v in out.values() if v["title_hits"])
    print(f"records_with_any_hit={n_any} with_doi={n_doi} with_title={n_title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
