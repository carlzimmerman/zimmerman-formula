#!/usr/bin/env python3
"""
arxiv_watch.py — daily arXiv scan for results bearing on the Zimmerman Theory of Gravity.

Stdlib only (urllib + xml.etree). No ai_slop dependency. This script ONLY fetches and
dedupes candidate papers; the VALIDATE/INVALIDATE assessment is done by Claude following
real_research/data_watch/ROUTINE.md.

It queries astro-ph.GA / astro-ph.CO / gr-qc for the framework's watch terms, keeps papers
submitted in the last N days, removes any already in seen.json, prints the new candidates
(Markdown by default, --json for machine output), and marks them seen.

Usage:
  python arxiv_watch.py                # last 2 days, mark seen, Markdown
  python arxiv_watch.py --days 7       # wider window (use once at setup to seed seen.json)
  python arxiv_watch.py --json         # JSON for programmatic use
  python arxiv_watch.py --no-mark      # dry run: do not update seen.json
"""
import argparse, json, os, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(HERE, "seen.json")
API = "http://export.arxiv.org/api/query"
CATS = ["astro-ph.GA", "astro-ph.CO", "gr-qc"]

# Watch terms — phrases bearing on the framework's pre-registered predictions (ROUTINE.md).
TERMS = [
    "radial acceleration relation", "baryonic Tully-Fisher", "Tully-Fisher relation",
    "MOND", "modified Newtonian dynamics", "modified inertia", "deep-MOND",
    "MOND acceleration scale", "external field effect", "emergent gravity",
    "wide binaries", "wide binary test", "MUSE-DARK", "dark energy equation of state",
    "w0waCDM", "evolving dark energy", "high-redshift rotation curves",
    # WATCHLIST entries 5-6: relativistic-MOND theory + the high-z / a0(z) telescopes
    "aether scalar tensor", "AeST", "Skordis", "relativistic MOND", "TeVeS",
    "weak lensing radial acceleration", "DESI DR3", "ELT HARMONI",
    "JWST rotation curve", "ALMA high-redshift kinematics", "galaxy cluster MOND residual",
]
ATOM = "{http://www.w3.org/2005/Atom}"


def build_query():
    cat = " OR ".join(f"cat:{c}" for c in CATS)
    terms = " OR ".join(f'all:"{t}"' for t in TERMS)
    return f"({cat}) AND ({terms})"


def fetch(max_results):
    params = {"search_query": build_query(), "sortBy": "submittedDate",
              "sortOrder": "descending", "start": 0, "max_results": max_results}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "zimmerman-data-watch/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall(ATOM + "entry"):
        idurl = (e.findtext(ATOM + "id", "") or "").strip()
        arxid = idurl.rsplit("/abs/", 1)[-1] if "/abs/" in idurl else idurl.rsplit("/", 1)[-1]
        out.append({
            "id": arxid,
            "title": " ".join((e.findtext(ATOM + "title", "") or "").split()),
            "authors": [a.findtext(ATOM + "name", "") for a in e.findall(ATOM + "author")],
            "abstract": " ".join((e.findtext(ATOM + "summary", "") or "").split()),
            "published": (e.findtext(ATOM + "published", "") or "")[:10],
            "link": idurl,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("--no-mark", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    seen = set()
    if os.path.exists(SEEN):
        try:
            seen = set(json.load(open(SEEN)))
        except Exception:
            seen = set()

    try:
        entries = parse(fetch(args.max))
    except Exception as ex:
        print(f"ERROR fetching/parsing arXiv: {ex}", file=sys.stderr)
        sys.exit(2)

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    new = []
    for e in entries:
        if e["id"] in seen:
            continue
        try:
            pub = datetime.fromisoformat(e["published"] + "T00:00:00+00:00")
        except Exception:
            pub = None
        if pub is not None and pub < cutoff:
            continue
        new.append(e)

    if not args.no_mark and new:
        seen |= {e["id"] for e in new}
        json.dump(sorted(seen), open(SEEN, "w"), indent=0)

    if args.json:
        print(json.dumps(new, indent=2))
        return

    today = datetime.now(timezone.utc).date()
    print(f"# arXiv data-watch — {len(new)} new candidate(s), last {args.days}d ({today})\n")
    if not new:
        print("_No new candidate papers._")
        return
    for e in new:
        au = ", ".join(e["authors"][:4]) + (" et al." if len(e["authors"]) > 4 else "")
        print(f"## {e['title']}")
        print(f"- **{e['id']}** · {au} · {e['published']} · {e['link']}\n")
        print(f"{e['abstract'][:900]}\n")


if __name__ == "__main__":
    main()
