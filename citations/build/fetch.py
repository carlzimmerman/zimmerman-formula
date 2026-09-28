#!/usr/bin/env python3
"""Stage 2b: fetch and VERIFY the metadata of every work the index can point to.

Sources of works:
  * registry/*.yaml   (software, algorithms, datasets, concepts, eponyms): doi / arxiv / inspire ids, or
                       `classic:`/`software:` records for works that have no DOI (books, pre-DOI memoirs, code)
  * data/mentions     arXiv ids, DOIs and ADS bibcodes written in the scripts themselves
  * data/ay_resolution.json  the publications chosen for author-year citations

Every identifier is looked up in its authority (Crossref or DataCite for DOIs, arXiv, INSPIRE-HEP). A registry
identifier whose returned first author / year disagree with the expectation written next to it (the `cite:`
field or the trailing `# Author ... YEAR` comment) is flagged, never silently accepted.
Output: data/works_meta.json  {work_id: normalised metadata + verification record}
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apis  # noqa: E402
from common import DATA, REGISTRY, dump_json, is_own_author, load_json, norm_family, slugify  # noqa: E402

import yaml  # noqa: E402

TODAY = dt.date.today().isoformat()
BIB_J = {"ApJ": "Astrophysical Journal", "ApJL": "Astrophysical Journal Letters", "AJ": "Astronomical Journal",
         "MNRAS": "Monthly Notices of the Royal Astronomical Society", "A&A": "Astronomy and Astrophysics",
         "PASJ": "Publications of the Astronomical Society of Japan", "PASP": "Publications of the Astronomical Society of the Pacific"}


def wid_doi(d):
    return "doi:" + d.strip().lower()


def wid_arxiv(a):
    return "arxiv:" + re.sub(r"v\d+$", "", a.strip())


# ------------------------------------------------------------------ registry parsing
def registry_files():
    return sorted(REGISTRY.glob("*.yaml"))


def comment_expectations(path: Path) -> dict[str, str]:
    """Map identifier -> trailing comment text ('# Harris et al. 2020, Nature 585, 357')."""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\{\s*(doi|arxiv|inspire)\s*:\s*\"?([^\"}]+?)\"?\s*\}\s*#\s*(.+)$", line)
        if m:
            out[m.group(2).strip().lower()] = m.group(3).strip()
    return out


def iter_registry_works():
    """Yield (registry_file, entry_label, work_spec, expectation_text)."""
    for p in registry_files():
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        exp = comment_expectations(p)
        entries = data.items() if isinstance(data, dict) else enumerate(data)
        for key, ent in entries:
            if not isinstance(ent, dict):
                continue
            label = ent.get("label") or ent.get("concept") or str(key)
            for w in ent.get("works") or []:
                if not isinstance(w, dict):
                    continue
                ident = str(w.get("doi") or w.get("arxiv") or w.get("inspire") or "").lower()
                yield p.name, label, w, (w.get("cite") or exp.get(ident) or "")


def expectation(text: str):
    """(first-author family, year) parsed from 'Harris et al. 2020, ...' / 'Tully, R. B. & Fisher ...1977'."""
    if not text:
        return None, None
    t = re.sub(r"^(?:the\s+)?(?:[A-Z][\w-]*\s+)?[Cc]ollaboration[,:]?\s*", "", text.strip())
    m = re.match(r"([A-Z][A-Za-zÀ-ÿ'’\-]+(?:\s+(?:de|van|von|der|den|le|la|di|del|da|du)\s+[A-Z][\w'’-]+)?)", t)
    fam = m.group(1) if m else None
    y = re.search(r"\b(1[5-9]\d\d|20[0-2]\d)\b", t)
    return fam, int(y.group(1)) if y else None


# ------------------------------------------------------------------ authority lookups
def resolve_doi(doi: str):
    doi = doi.strip().lower().rstrip(".")
    r = None
    if not doi.startswith(("10.5281/", "10.25919/", "10.7935/", "10.17632/", "10.6084/", "10.48550/")):
        r = apis.crossref_doi(doi, fast=True)
    if r is None:
        r = apis.datacite_doi(doi)
    if r is None:
        r = apis.doiorg_csl(doi)
    return r


def resolve_arxiv(aid: str):
    aid = re.sub(r"v\d+$", "", aid.strip())
    got = apis.arxiv_ids([aid]).get(aid)
    if not got:
        return None, None
    if got.get("doi"):
        pub = resolve_doi(got["doi"])
        if pub and pub.get("title"):
            pub["arxiv"] = aid
            if not pub.get("year"):
                pub["year"] = got.get("year")
            if not pub.get("authors"):
                pub["authors"] = got.get("authors") or []
            if not pub.get("abstract"):
                pub["abstract"] = got.get("abstract")
            if len(pub.get("authors") or []) < len(got.get("authors") or []) and len(got["authors"]) > 3:
                pub["_arxiv_authors"] = got["authors"]      # publisher list truncated: keep the full list
            return wid_doi(pub["doi"]), pub
    return wid_arxiv(aid), got


def resolve_inspire(recid):
    r = apis.inspire_record(str(recid))
    if not r:
        return None, None
    if r.get("doi"):
        pub = resolve_doi(r["doi"])
        if pub and pub.get("title"):
            pub["inspire_id"] = str(recid)
            pub["arxiv"] = pub.get("arxiv") or r.get("arxiv")
            if len(pub.get("authors") or []) == 0:
                pub["authors"] = r["authors"]
            return wid_doi(pub["doi"]), pub
    if r.get("arxiv"):
        w, rec = resolve_arxiv(r["arxiv"])
        if rec:
            rec["inspire_id"] = str(recid)
            if not rec.get("container"):
                for k in ("container", "volume", "page", "year"):
                    rec[k] = rec.get(k) or r.get(k)
            return w, rec
    return f"inspire:{recid}", r


def resolve_bibcode(b: str):
    m = re.match(r"(\d{4})([A-Za-z&.]+?)\.*(\d+)[.L]*?([A-Z]?\d+)?\.*([A-Z])$", b)
    if not m:
        return None, None
    year, jour, vol, page, init = m.groups()
    jour = jour.strip(".")
    q = f"{BIB_J.get(jour, jour)} {vol} {page or ''} {year}"
    for r in apis.crossref_search(bibliographic=q, rows=5):
        if str(r.get("volume")) == vol and page and str(r.get("page") or "").split("-")[0].lstrip("L") == page.lstrip("L") \
                and r.get("year") and abs(int(r["year"]) - int(year)) <= 1:
            fam = apis.first_family(r)
            if fam and norm_family(fam)[:1] == init.lower():
                return wid_doi(r["doi"]), r
    return None, None


_PARTICLES = {"von", "van", "de", "der", "den", "du", "della", "del", "da", "di", "le", "la", "ten", "ter"}
_ORG_WORDS = ("team", "contributors", "developers", "collaboration", "research", "consortium", "group", "project")


def split_author_list(authors):
    """Registry author field (list or '; '-separated string) -> list of clean name strings, editors dropped."""
    items = authors if isinstance(authors, list) else re.split(r"\s*;\s*|\s+and\s+", str(authors or ""))
    out = []
    for a in items:
        a = re.sub(r"\([^)]*\)", " ", str(a))                                  # asides: (letters, ...), (Lord Rayleigh)
        a = re.sub(r",?\s*(?:compiled|edited|translated)\s+by\b.*$", "", a, flags=re.I)
        a = re.sub(r"\s+", " ", a).strip(" ,;")
        if not a or re.match(r"(?i)^(?:ed|eds|trans|transl)\.?\s", a):
            continue
        out.append(a)
    return out


def parse_person(a: str, organization: bool = False):
    if organization or any(w in a.lower() for w in _ORG_WORDS) or a.lower().startswith(("the ", "nous ")):
        return {"given": "", "family": "", "name": a, "orcid": None, "affiliation": None}
    if "," in a:
        fam, giv = [x.strip() for x in a.split(",", 1)]
    else:
        toks = a.split()
        i = len(toks) - 1
        while i > 0 and toks[i - 1].lower() in _PARTICLES:
            i -= 1
        giv, fam = " ".join(toks[:i]), " ".join(toks[i:])
    return {"given": giv, "family": fam, "orcid": None, "affiliation": None, "name": None}


def classic_record(spec: dict, kind: str):
    names = split_author_list(spec.get("authors"))
    authors = [parse_person(a, bool(spec.get("organization"))) for a in names]
    title = spec.get("title") or spec.get("software")
    first = authors[0]["family"] or authors[0]["name"] if authors else "anon"
    wid = f"{kind}:{slugify(first)}-{spec.get('year')}-{slugify(title or '')[:40]}"
    rec = apis.rec(kind, type="software" if kind == "software" else "classic", title=title, authors=authors,
                   year=spec.get("year"), container=spec.get("venue"), url=spec.get("url"))
    return wid, rec


def bad_names(authors):
    for a in authors:
        fam = (a.get("family") or "").strip()
        if a.get("name") and not fam:
            continue
        if not fam or "\ufffd" in fam + (a.get("given") or "") or len(fam.strip(".:")) <= 1 or fam in ("Jr", "Jr.", "Sr", "III"):
            return True
    return False


def needs_repair(rec):
    return ("\ufffd" in (rec.get("title") or "")) or not rec.get("title") or not rec.get("authors") or bad_names(rec["authors"])


# ------------------------------------------------------------------ main
def main():
    meta = {}
    checks = []                 # registry expectation mismatches
    ids = {"doi": set(), "arxiv": set(), "inspire": set(), "bibcode": set()}
    reg_specs = []
    for fname, label, spec, exp in iter_registry_works():
        reg_specs.append((fname, label, spec, exp))
        for k in ("doi", "arxiv", "inspire"):
            if spec.get(k):
                ids[k].add(str(spec[k]).strip())
    m = load_json(DATA / "mentions.json.gz")["mentions"]
    for r in m:
        if r["kind"] in ("doi", "arxiv", "bibcode"):
            ids[r["kind"]].add(r["key"])
    ayp = DATA / "ay_resolution.json.gz"
    ay = load_json(ayp) if ayp.exists() else {}
    for k, v in ay.items():
        used = {i for i in (v.get("assign") or {}).values() if i is not None}   # only candidates a script is credited with
        for i, c in enumerate(v.get("candidates", [])):
            if i not in used:
                continue
            if c.get("doi"):
                ids["doi"].add(c["doi"])
            elif c.get("arxiv"):
                ids["arxiv"].add(c["arxiv"])
            elif c.get("inspire_id"):
                ids["inspire"].add(c["inspire_id"])
        ch = v.get("choice")
        if isinstance(ch, dict):
            for kk in ("doi", "arxiv", "inspire"):
                if ch.get(kk):
                    ids[kk].add(str(ch[kk]))
    bibp = DATA / "bib_resolution.json.gz"
    if bibp.exists():
        for res in load_json(bibp)["by_text"].values():
            if res.get("doi"):
                ids["doi"].add(res["doi"])
            elif res.get("arxiv"):
                ids["arxiv"].add(res["arxiv"])
            elif res.get("inspire_id"):
                ids["inspire"].add(res["inspire_id"])
    # curated author-year decisions (registry/ay_overrides.yaml): identifiers, classic records, expectations
    ov_path = REGISTRY / "ay_overrides.yaml"
    overrides = (yaml.safe_load(ov_path.read_text(encoding="utf-8")) or {}) if ov_path.exists() else {}
    ov_specs = []
    for key, ch in overrides.items():
        if not isinstance(ch, dict):
            continue
        fam = key.split("|")[0]
        yr = int(re.sub(r"\D", "", key.split("|")[1])[:4]) if "|" in key else None
        for sp in [ch] + [v for v in (ch.get("files") or {}).values() if isinstance(v, dict)] + \
                [r for r in (ch.get("rules") or []) if isinstance(r, dict)]:
            if sp.get("classic"):
                ov_specs.append((key, {**sp["classic"], "classic": True}, fam, yr))
            else:
                for k in ("doi", "arxiv", "inspire"):
                    if sp.get(k):
                        ids[k].add(str(sp[k]).strip())
                        ov_specs.append((key, {k: sp[k]}, fam, yr))
    print({k: len(v) for k, v in ids.items()})
    alias = {}                  # raw identifier -> canonical work id

    def do_doi(d):
        r = resolve_doi(d)
        ok = r and (r.get("title") or r.get("authors") or r.get("source") == "doi.org")   # an empty title is fixable
        return ("doi", d, (wid_doi(r["doi"] or d), r) if ok else (None, None))

    def do_arx(a):
        return ("arxiv", a, resolve_arxiv(a))

    def do_ins(i):
        return ("inspire", i, resolve_inspire(i))

    def do_bib(b):
        return ("bibcode", b, resolve_bibcode(b))

    apis.arxiv_ids(sorted(re.sub(r"v\d+$", "", a.strip()) for a in ids["arxiv"]))   # warm the per-id cache, 50 ids per call
    jobs = [(do_doi, x) for x in sorted(ids["doi"])] + [(do_arx, x) for x in sorted(ids["arxiv"])] + \
           [(do_ins, x) for x in sorted(ids["inspire"])] + [(do_bib, x) for x in sorted(ids["bibcode"])]
    failures = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for i, (kind, raw, (wid, rec)) in enumerate(ex.map(lambda j: j[0](j[1]), jobs), 1):
            if wid and rec:
                rec.setdefault("verified_by", rec.get("source"))
                rec["verified_on"] = TODAY
                if wid not in meta or (meta[wid].get("source") != "crossref" and rec.get("source") == "crossref"):
                    old = meta.get(wid, {})
                    for f in ("arxiv", "inspire_id", "abstract", "_arxiv_authors"):
                        if old.get(f) and not rec.get(f):
                            rec[f] = old[f]
                    meta[wid] = rec
                else:
                    for f in ("arxiv", "inspire_id", "abstract", "_arxiv_authors"):
                        if rec.get(f) and not meta[wid].get(f):
                            meta[wid][f] = rec[f]
                alias[f"{kind}:{raw.lower() if kind == 'doi' else raw}"] = wid
            else:
                failures.append(f"{kind}:{raw}")
            if i % 200 == 0:
                print(f"  {i}/{len(jobs)} fetched; {len(failures)} unresolved", flush=True)
    # classic / software records and registry expectation checks
    for fname, label, spec, exp in reg_specs:
        if spec.get("classic") or spec.get("software"):
            wid, rec = classic_record(spec, "software" if spec.get("software") else "classic")
            rec["verified_by"] = "manual-record" + (" (url " + spec["url"] + ")" if spec.get("url") else "")
            rec["verified_on"] = TODAY
            meta.setdefault(wid, rec)
            continue
        for k in ("doi", "arxiv", "inspire"):
            if not spec.get(k):
                continue
            raw = str(spec[k]).strip()
            wid = alias.get(f"{k}:{raw.lower() if k == 'doi' else raw}")
            if not wid:
                checks.append({"registry": fname, "label": label, "id": f"{k}:{raw}", "problem": "not found in authority"})
                continue
            fam, yr = expectation(exp)
            rec = meta[wid]
            got_fam = apis.first_family(rec) or ((rec.get("authors") or [{}])[0].get("name") or "")
            prob = []
            if fam and got_fam and norm_family(fam) not in (norm_family(got_fam),) and \
                    not norm_family(got_fam).startswith(norm_family(fam)[:5]) and "ollaboration" not in got_fam:
                prob.append(f"first author {got_fam!r} != expected {fam!r}")
            if yr and rec.get("year") and abs(int(rec["year"]) - yr) > 1:
                prob.append(f"year {rec['year']} != expected {yr}")
            if prob:
                checks.append({"registry": fname, "label": label, "id": f"{k}:{raw}", "expected": exp,
                               "got": f"{got_fam} {rec.get('year')} {rec.get('title')}", "problem": "; ".join(prob)})
    # repair publisher records with broken names/titles from OpenAlex's copy (same DOI)
    repaired = 0
    for wid, rec in list(meta.items()):
        if not wid.startswith("doi:") or not needs_repair(rec):
            continue
        oa = apis.openalex_doi(wid[4:])
        if not oa or not oa.get("title"):
            continue
        fixed = False
        if ("\ufffd" in (rec.get("title") or "") or not rec.get("title")) and "\ufffd" not in oa["title"]:
            rec["title"] = oa["title"]
            fixed = True
        au, oau = rec.get("authors") or [], oa.get("authors") or []
        if oau and (not au or bad_names(au)) and not bad_names(oau) and (not au or len(oau) >= len(au)):
            rec["authors"] = oau
            fixed = True
        if fixed:
            rec["repaired_from"] = "openalex"
            repaired += 1
    print(f"records repaired from OpenAlex: {repaired}")
    for key, sp, fam, yr in ov_specs:
        if sp.get("classic"):
            wid, rec = classic_record(sp, "classic")
            rec["verified_by"] = "manual-record" + (" (url " + sp["url"] + ")" if sp.get("url") else "")
            rec["verified_on"] = TODAY
            meta.setdefault(wid, rec)
            got_fam = rec["authors"][0]["family"] if rec["authors"] else ""
        else:
            k = next(iter(sp))
            raw = str(sp[k]).strip()
            wid = alias.get(f"{k}:{raw.lower() if k == 'doi' else raw}")
            if not wid:
                checks.append({"registry": "ay_overrides.yaml", "label": key, "id": f"{k}:{raw}", "problem": "not found in authority"})
                continue
            rec = meta[wid]
            got_fam = apis.first_family(rec) or ((rec.get("authors") or [{}])[0].get("name") or "")
        prob = []
        nf = norm_family(got_fam)
        if fam and nf and fam != nf and not (len(fam) >= 4 and (nf.endswith(fam) or fam.endswith(nf) or nf.startswith(fam[:5]))) \
                and "ollaboration" not in got_fam and "group" not in got_fam.lower():
            prob.append(f"first author {got_fam!r} does not match the cited surname {fam!r}")
        if yr and rec.get("year") and abs(int(rec["year"]) - yr) > 1:
            prob.append(f"year {rec['year']} does not match the cited year {yr}")
        if prob:
            checks.append({"registry": "ay_overrides.yaml", "label": key, "id": str(sp), "problem": "; ".join(prob),
                           "got": f"{got_fam} {rec.get('year')} {rec.get('title')}"})
    # the repository author's own works are kept out of the index: store a stub (no names, no title), never the record
    for wid, rec in list(meta.items()):
        if any(is_own_author(a) for a in (rec.get("_arxiv_authors") or []) + (rec.get("authors") or [])):
            meta[wid] = {"own": True, "verified_by": rec.get("verified_by"), "year": rec.get("year")}
    dump_json({"meta": meta, "alias": alias, "failures": sorted(failures), "registry_checks": checks},
              DATA / "works_meta.json.gz", gz=True)
    src = collections.Counter(v.get("verified_by", "?").split(" ")[0] for v in meta.values())
    print(f"works with verified metadata: {len(meta)}  by source: {dict(src)}")
    print(f"identifiers that did not resolve: {len(failures)}")
    print(f"registry expectation problems: {len(checks)}")
    for c in checks[:80]:
        print("  CHECK", c)


if __name__ == "__main__":
    main()
