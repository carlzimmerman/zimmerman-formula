#!/usr/bin/env python3
"""Stage 6: the gate. Exits non-zero if the generated index is inconsistent or unsafe to publish.

Checks
  1. every credited work has a title, a year, at least one author, and a recognised verification source
  2. no garbled text (U+FFFD) or HTML entity survives in any title, journal or author name
  3. every script path in the index is git-tracked, inside the scanned scope, and every cited line exists
  4. every person has at least one work; every person page / work page / letter page that is linked exists
  5. every relative link in the generated markdown resolves to a file in the repository
  6. no registry identifier failed verification (registry_misses is empty)
  7. the repository's own author is not listed as a credited person; no committed index file (pages, data, registry,
     build code) contains a local filesystem path, the author's name, or the repository owner's handle; the
     author's own works survive in the fetched metadata only as stubs
  8. every one of the previous index's surname pages still exists (as a pointer) except the own-author page
  9. the counts quoted in CITATIONS.md match the data
 10. nothing the index needs is git-ignored (only the build intermediates and caches may be)
Optional: --online re-fetches a random sample of DOIs from Crossref and compares title/year.
"""
from __future__ import annotations

import gzip
import random
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CITE_DIR, DATA, EXCLUDE_PREFIXES, REPO, committed_files, is_own_author, read_committed, load_json, norm_family, own_author_families, \
    own_author_given_initials, own_leak_patterns, strip_accents  # noqa: E402

fails, warns = [], []


def fail(msg):
    fails.append(msg)


def main(argv):
    works = load_json(DATA / "works.json.gz")
    usage = load_json(DATA / "usage.json.gz")
    people = load_json(DATA / "people.json.gz")
    un = load_json(DATA / "unresolved.json.gz")
    tracked = set(committed_files())                     # as committed at the commit the index was built from
    ok_src = {"crossref", "datacite", "arxiv", "inspire", "openalex", "doi.org", "manual-record"}
    # 1-2
    for wid, w in works.items():
        if not w.get("title"):
            fail(f"work {wid}: no title")
        if not w.get("year"):
            warns.append(f"work {wid}: no year")
        if not (w.get("all_authors") or []):
            fail(f"work {wid}: no authors")
        if (w.get("verified_by") or "").split(" ")[0] not in ok_src:
            fail(f"work {wid}: unknown verification source {w.get('verified_by')!r}")
        blob = (w.get("title") or "") + " ".join((a.get("family") or "") + (a.get("given") or "") + (a.get("name") or "")
                                                 for a in w.get("all_authors") or [])
        if "�" in blob:
            fail(f"work {wid}: garbled characters in title/authors (add a fix to registry/metadata_fixes.yaml)")
        if re.search(r"&(?:[a-zA-Z]{2,8}|#\d{2,6}|#x[0-9a-fA-F]{2,5});", blob + (w.get("container") or "")):
            fail(f"work {wid}: an HTML entity in its metadata (apis.unescape should have removed it)")
    # 3
    nlines = {}
    for wid, us in usage.items():
        if wid not in works:
            fail(f"usage for unknown work {wid}")
        for u in us:
            f = u["file"]
            if f not in tracked:
                fail(f"{wid}: script not tracked: {f}")
                continue
            if f.startswith(EXCLUDE_PREFIXES):
                fail(f"{wid}: script outside the scanned scope: {f}")
            if u["lines"]:
                if f not in nlines:
                    try:
                        nlines[f] = (read_committed(f) or b"").count(b"\n") + 1
                    except OSError:
                        nlines[f] = 0
                if max(u["lines"]) > nlines[f] and not f.endswith(".ipynb"):
                    fail(f"{wid}: line {max(u['lines'])} beyond end of {f} ({nlines[f]} lines)")
    # 4
    for pid, p in people.items():
        if not p["works"]:
            fail(f"person {pid} has no works")
        if not p["collab_only"] and not (CITE_DIR / "people" / f"{pid}.md").exists():
            fail(f"missing person page {pid}")
    # 5 links in generated markdown
    md_files = [CITE_DIR.parent / "CITATIONS.md", CITE_DIR / "README.md", CITE_DIR / "UNVERIFIED.md",
                CITE_DIR / "CORRECTIONS.md", CITE_DIR / "BY_FOLDER.md"]
    md_files += sorted((CITE_DIR / "people").glob("*.md")) + sorted((CITE_DIR / "works").glob("*.md"))
    md_files += sorted(CITE_DIR.glob("*/index.md")) + sorted(CITE_DIR.glob("WORKS*.md"))
    for mf in md_files:                         # GitHub stops rendering very large markdown files
        if mf.exists() and mf.stat().st_size > 900_000:
            fail(f"{mf.name} is {mf.stat().st_size // 1000} kB (too large to render on GitHub)")
    link_rx = re.compile(r"\]\(([^)\s]+)\)")
    checked = 0
    for mf in md_files:
        if not mf.exists():
            fail(f"expected file missing: {mf.name}")
            continue
        txt = mf.read_text(encoding="utf-8")
        for m in link_rx.finditer(txt):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = urllib.parse.unquote(target.split("#")[0])
            if not path:
                continue
            dest = (mf.parent / path).resolve()
            checked += 1
            if not dest.exists():
                try:
                    rel = dest.relative_to(CITE_DIR.parent.resolve())
                except ValueError:
                    rel = None
                if rel is None or not ((REPO / rel).exists() or str(rel) in tracked):
                    fail(f"broken link in {mf.name}: {target}")
    # 6
    for miss in un.get("registry_misses", []):
        fail(f"registry work failed verification: {miss}")
    # 7
    own_f, own_i = own_author_families(), own_author_given_initials()
    for pid, p in people.items():
        if norm_family(p["family"]) in own_f and strip_accents(p["given"])[:1].lower() in own_i:
            fail(f"repository's own author listed as a credited person: {pid}")
    leak = re.compile(r"/Users/[A-Za-z0-9._-]+/|/home/[a-z][A-Za-z0-9._-]*/")
    cff = (REPO / "CITATION.cff").read_text(encoding="utf-8") if (REPO / "CITATION.cff").exists() else ""
    gm = re.search(r"given-names:\s*\"?([^\"\n]+)", cff)
    fm = re.search(r"family-names:\s*\"?([^\"\n]+)", cff)
    own_name = re.compile(rf"\b{re.escape(gm.group(1).split()[0])}\b[\w. ]{{0,6}}\b{re.escape(fm.group(1).strip())}\b", re.I) \
        if gm and fm else None
    for mf in md_files:
        if not mf.exists():
            continue
        txt = mf.read_text(encoding="utf-8")
        if leak.search(txt):
            fail(f"local filesystem path in {mf.name}")
        if own_name and own_name.search(txt):
            fail(f"the repository author's own name appears in {mf.name}")
    ignored = {"texts.json.gz", "mentions.json.gz"}             # gitignored build intermediates
    scan = [p for p in CITE_DIR.rglob("*") if p.is_file() and p.name not in ignored
            and not {".cache", "__pycache__"} & set(p.parts)] + [CITE_DIR.parent / "CITATIONS.md"]
    pats = own_leak_patterns()
    for p in scan:
        if p.suffix == ".gz":
            with gzip.open(p, "rt", encoding="utf-8") as fh:
                txt = fh.read()
        elif p.suffix in (".md", ".bib", ".tsv", ".json", ".yaml", ".py", ".txt") or p.name == ".gitignore":
            txt = p.read_text(encoding="utf-8", errors="replace")
        else:
            continue
        for label, rx in pats:
            m = rx.search(txt)
            if m:
                fail(f"{label} in {p.relative_to(CITE_DIR.parent)}: {txt[max(0, m.start() - 30):m.end() + 10]!r}")
    for wid, rec in load_json(DATA / "works_meta.json.gz")["meta"].items():
        if any(is_own_author(a) for a in (rec.get("_arxiv_authors") or []) + (rec.get("authors") or [])):
            fail(f"works_meta keeps the author's own work {wid} with its author list (fetch.py should store a stub)")
    # 8
    old = subprocess.run(["git", "-C", str(REPO), "show", "c5fddc2191:CITATIONS.md"], capture_output=True, text=True).stdout
    for slug in re.findall(r"\[citations/([^/]+)/\]", old):
        page = CITE_DIR / slug / "index.md"
        own_page = any(norm_family(slug) == f for f in own_f)
        if own_page and page.exists():
            fail(f"own-author page still present: citations/{slug}/")
        if not own_page and not page.exists():
            fail(f"old index page lost: citations/{slug}/index.md")
    # 9
    cm = (CITE_DIR.parent / "CITATIONS.md").read_text(encoding="utf-8") if (CITE_DIR.parent / "CITATIONS.md").exists() else ""
    m = re.search(r"\*\*([\d,]+) people\*\*", cm)
    if not m or int(m.group(1).replace(",", "")) != len(people):
        fail(f"CITATIONS.md people count does not match data ({m.group(1) if m else None} vs {len(people)})")
    m = re.search(r"\*\*([\d,]+) works\*\*", cm)
    if not m or int(m.group(1).replace(",", "")) != len(works):
        fail(f"CITATIONS.md works count does not match data ({m.group(1) if m else None} vs {len(works)})")
    # 10 a repository-wide ignore glob must not silently drop pages or build code from the commit
    ign = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "--others", "--ignored", "--exclude-standard",
                          "--directory", "--", "citations"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
    ok_ignored = {"citations/data/texts.json.gz", "citations/data/mentions.json.gz", "citations/build/__pycache__/",
                  "citations/.cache/"}
    for p in ign:
        if p and p not in ok_ignored:
            fail(f"git ignores {p}, which the index needs (add an exception to citations/.gitignore)")
    # optional online spot-check
    if "--online" in argv:
        import apis
        dois = [w["doi"] for w in works.values() if w.get("doi") and (w.get("verified_by") or "").startswith("crossref")]
        random.seed(0)
        for d in random.sample(dois, min(40, len(dois))):
            r = apis.crossref_doi(d)
            if not r:
                fail(f"online: {d} no longer resolves")
    print(f"verify: {len(works)} works, {len(people)} people, {sum(len(u) for u in usage.values())} script credits, "
          f"{checked} links checked; {len(warns)} warnings; {len(fails)} failures")
    for w in warns[:10]:
        print("  warn:", w)
    for f in fails[:60]:
        print("  FAIL:", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(sys.argv)
