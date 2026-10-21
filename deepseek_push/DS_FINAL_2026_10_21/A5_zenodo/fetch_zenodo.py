#!/usr/bin/env python3
"""Fetch all Zenodo records for creator "Zimmerman, Carl" and cache them.

Network is permitted only for zenodo.org.  Unauthenticated page size is capped
at 25, so we page.  Output: _zenodo/all_records.json (list, sorted by id) and
_zenodo/fetch_meta.json (counts, timestamps, per-page hashes).
"""
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://zenodo.org/api/records"
QUERY = 'creators.name:"Zimmerman, Carl"'
PAGE_SIZE = 25
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_zenodo")
UA = "a5-zenodo-lane/1.0 (research audit; contact: local)"


def get(url, retries=5):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8")), r.status
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 + 3 * attempt)
    raise RuntimeError(f"GET failed after {retries}: {url}: {last}")


def slim(h):
    m = h.get("metadata", {})
    creators = [c.get("name", "") for c in m.get("creators", [])]
    return {
        "id": h.get("id"),
        "doi": h.get("doi") or m.get("doi"),
        "conceptdoi": h.get("conceptdoi"),
        "date": m.get("publication_date"),
        "title": m.get("title"),
        "description": m.get("description", ""),
        "creators": creators,
        "resource_type": (m.get("resource_type") or {}).get("type"),
        "keywords": m.get("keywords", []),
        "version": m.get("version"),
        "related_identifiers": m.get("related_identifiers", []),
        "html": h.get("links", {}).get("self_html") or h.get("links", {}).get("html"),
        "updated": h.get("updated"),
    }


def main():
    os.makedirs(CACHE, exist_ok=True)
    records, pages = [], []
    page = 1
    total = None
    while True:
        url = (f"{BASE}?q={urllib.parse.quote(QUERY)}&sort=newest"
               f"&size={PAGE_SIZE}&page={page}")
        d, status = get(url)
        total = d["hits"]["total"]
        hits = d["hits"]["hits"]
        pages.append({"page": page, "status": status, "n": len(hits),
                      "total": total,
                      "sha256": hashlib.sha256(
                          json.dumps(hits, sort_keys=True).encode()).hexdigest()[:16]})
        records.extend(slim(h) for h in hits)
        print(f"page {page}: {len(hits)} records (total {total})", flush=True)
        if len(hits) < PAGE_SIZE or len(records) >= total:
            break
        page += 1
        time.sleep(0.4)

    # dedupe by id, keep order
    seen, uniq = set(), []
    for r in records:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        uniq.append(r)
    uniq.sort(key=lambda r: (r["date"] or "", r["id"] or 0))

    with open(os.path.join(CACHE, "all_records.json"), "w") as f:
        json.dump(uniq, f, indent=1, sort_keys=True)
    with open(os.path.join(CACHE, "fetch_meta.json"), "w") as f:
        json.dump({"query": QUERY, "api": BASE, "reported_total": total,
                   "fetched": len(records), "unique": len(uniq),
                   "pages": pages,
                   "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                  f, indent=1)
    print(f"DONE fetched={len(records)} unique={len(uniq)} reported_total={total}")
    return 0 if len(uniq) == total else 1


if __name__ == "__main__":
    sys.exit(main())
