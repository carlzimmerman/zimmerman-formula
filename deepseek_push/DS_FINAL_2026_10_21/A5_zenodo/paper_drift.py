#!/usr/bin/env python3
"""Map each Zenodo record to a repo paper (if any) and measure drift.

Mapping is by normalised title equality against every *.zenodo.json in
qwen_claude_field_theory/papers_2026 (metadata titles are the deposit titles).
For a mapped paper we report:
  - the .tex / .pdf mtime (repo copy date)
  - how many of the record's distinctive numbers appear in the .tex
  - whether the .tex carries the corrected wording or the withdrawn wording
    (only for the handful of phrases listed in KNOWN_WORDING)

Output: _zenodo/paper_map.json
"""
import glob
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHE = os.path.join(HERE, "_zenodo")
PAPERS = os.path.join(REPO, "qwen_claude_field_theory", "papers_2026")

# withdrawn wording -> corrected wording, for records whose Zenodo version
# carries an explicit correction notice.
KNOWN_WORDING = {
    "negative lensing trough": "saddle dip",
    "no negative lensing trough": "no saddle dip",
}


def texnorm(txt):
    """Approximate the plain-text form of a LaTeX source so that a number
    written as $9.3603\\times10^{-11}$ compares equal to '9.3603e-11'."""
    t = txt
    t = re.sub(r"\\times\s*10\^\{?([-+]?\d+)\}?", r"e\1", t)
    t = re.sub(r"10\^\{?([-+]?\d+)\}?", r"e\1", t)
    t = re.sub(r"\\(left|right|,|;|!| |quad|qquad)", " ", t)
    t = t.replace("$", "").replace("{", "").replace("}", "")
    t = t.replace("\\pm", "+-").replace("\\,", " ")
    t = re.sub(r"\s+", " ", t)
    return t


def norm_title(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = t.lower()
    t = re.sub(r"\(working note\)|\(version[^)]*\)|version \d+(\.\d+)?", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def main():
    recs = json.load(open(os.path.join(CACHE, "all_records.json")))
    ext = {str(o["id"]): o for o in json.load(open(os.path.join(CACHE, "extract.json")))}

    papers = {}
    for f in glob.glob(os.path.join(PAPERS, "*.zenodo.json")):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        md = d.get("metadata", d)
        title = md.get("title") or ""
        base = f[:-len(".zenodo.json")]
        papers[norm_title(title)] = {
            "meta_file": os.path.relpath(f, REPO),
            "base": base,
            "tex": base + ".tex",
            "pdf": base + ".pdf",
        }

    out = {}
    for r in recs:
        key = norm_title(r["title"])
        p = papers.get(key)
        row: dict = {"mapped": False}
        if p:
            row["mapped"] = True
            row["tex"] = os.path.relpath(p["tex"], REPO)
            row["tex_exists"] = os.path.exists(p["tex"])
            if row["tex_exists"]:
                row["tex_mtime"] = os.path.getmtime(p["tex"])
                txt = texnorm(open(p["tex"], errors="ignore").read())
                probes = [n for n in ext[str(r["id"])]["numbers"]
                          if len(n) >= 5 and ("." in n or "e-" in n.lower())]
                probes = sorted(set(probes), key=lambda s: -len(s))[:8]
                row["probe_total"] = len(probes)
                row["probe_present"] = sum(1 for n in probes if n in txt)
                missing = [n for n in probes if n not in txt]
                row["probes_missing"] = missing
                row["withdrawn_wording"] = [w for w in KNOWN_WORDING
                                            if w in txt.lower()]
                row["corrected_wording"] = [w for w in KNOWN_WORDING.values()
                                            if w in txt.lower()]
        out[str(r["id"])] = row

    json.dump(out, open(os.path.join(CACHE, "paper_map.json"), "w"), indent=1,
              sort_keys=True)
    m = sum(1 for v in out.values() if v["mapped"])
    t = sum(1 for v in out.values() if v.get("tex_exists"))
    stale = [k for k, v in out.items()
             if v.get("tex_exists") and v.get("probe_total")
             and v["probe_present"] < v["probe_total"]]
    print(f"records={len(out)} mapped={m} tex_found={t} with_missing_numbers={len(stale)}")
    for k in stale:
        v = out[k]
        print(f"  {k}: {v['probe_present']}/{v['probe_total']} present; missing={v['probes_missing'][:4]}")


if __name__ == "__main__":
    main()
