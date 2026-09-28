"""Thin, cached, rate-limited clients for the public bibliographic APIs used to VERIFY every reference.

Crossref (DOIs, reference-string matching), arXiv (preprints), INSPIRE-HEP (physics/astro literature search),
DataCite (Zenodo and other DataCite DOIs), OpenAlex (fallback search). No API keys; no personal data is sent.
Responses are cached on disk (CITE_CACHE, default: citations/.cache/, git-ignored) so re-runs are offline.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from common import CITE_DIR, strip_accents

CACHE = Path(os.environ.get("CITE_CACHE", CITE_DIR / ".cache"))
UA = "zimmerman-formula-citation-index/1.0 (python-requests; research citation index)"
OFFLINE = os.environ.get("CITE_OFFLINE") == "1"

_locks = {k: threading.Lock() for k in ("crossref", "inspire", "arxiv", "datacite", "openalex")}
_last = {k: 0.0 for k in _locks}
_hold = {k: 0.0 for k in _locks}           # service-wide pause after a 429 (all threads wait)
_SERIAL = {"crossref"}                     # Crossref's public pool allows one request at a time
DEGRADED = {"count": 0}                    # requests that failed permanently (results may be incomplete)
FAILED_URLS = set()                        # URLs that failed (rate limit / server error), as opposed to a 404
_min_gap = {"crossref": 0.25, "inspire": 0.36, "arxiv": 3.1, "datacite": 0.2, "openalex": 0.15}
_session = requests.Session()
_session.headers.update({"User-Agent": UA})


def _cache_path(url: str) -> Path:
    h = hashlib.sha1(url.encode()).hexdigest()
    return CACHE / h[:2] / f"{h}.json"


def get(service: str, url: str, parse: str = "json", retries: int = 7):
    """GET with on-disk cache; returns parsed JSON (or text), or None on 404/persistent failure."""
    cp = _cache_path(url)
    if cp.exists():
        try:
            obj = json.loads(cp.read_text(encoding="utf-8"))
            return obj.get("body")
        except Exception:
            pass
    if OFFLINE:
        return None
    body = None
    for attempt in range(retries):
        serial = service in _SERIAL
        _locks[service].acquire()
        try:
            wait = max(_min_gap[service] - (time.time() - _last[service]), _hold[service] - time.time())
            if wait > 0:
                time.sleep(wait)
            _last[service] = time.time()
            if not serial:
                _locks[service].release()
            try:
                r = _session.get(url, timeout=(10, 30))
            except requests.RequestException:
                r = None
        finally:
            if serial:
                _locks[service].release()
        if r is None:
            time.sleep(2 * (attempt + 1))
            continue
        if r.status_code == 404:
            body = None
            break
        if r.status_code in (429, 500, 502, 503, 504):
            try:
                ra = float(r.headers.get("Retry-After", "0"))
            except ValueError:
                ra = 0.0
            pause = max(ra, 15.0 * (attempt + 1)) if r.status_code == 429 else 5.0 * (attempt + 1)
            _hold[service] = max(_hold[service], time.time() + pause)
            continue
        if r.status_code != 200:
            body = None
            break
        body = r.json() if parse == "json" else r.text
        break
    else:
        DEGRADED["count"] += 1
        FAILED_URLS.add(url)
        return None
    cp.parent.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps({"url": url, "body": body}), encoding="utf-8")
    return body


# ------------------------------------------------------------------ normalised record
def rec(source, **kw):
    base = {"source": source, "type": None, "title": None, "authors": [], "year": None, "container": None,
            "volume": None, "issue": None, "page": None, "doi": None, "arxiv": None, "url": None,
            "citations": None, "abstract": None, "collaboration": None, "publisher": None}
    base.update(kw)
    return base


def _person(given, family, orcid=None, affil=None, name=None):
    return {"given": (given or "").strip(), "family": (family or "").strip(), "orcid": orcid,
            "affiliation": affil, "name": name}


_PART = {"de", "van", "von", "der", "den", "du", "della", "del", "da", "di", "le", "la", "ten", "ter", "dos", "das"}


def _split_full(full: str):
    """'Milgrom, Mordehai' or 'Mordehai Milgrom' -> (given, family); keeps particles: 'Antonio De Felice' -> De Felice."""
    full = (full or "").replace("\xa0", " ").strip()
    if "," in full:
        fam, giv = full.split(",", 1)
        return giv.strip(), fam.strip()
    parts = full.split()
    if len(parts) == 1:
        return "", parts[0]
    i = len(parts) - 1
    while i > 1 and parts[i - 1].lower() in _PART:
        i -= 1
    return " ".join(parts[:i]), " ".join(parts[i:])


def doiorg_csl(doi: str):
    """Last-resort DOI check through doi.org content negotiation (works for JaLC, mEDRA and other agencies)."""
    url = f"https://doi.org/{urllib.parse.quote(doi, safe='/:;()')}"
    cp = _cache_path("csl:" + url)
    if cp.exists():
        body = json.loads(cp.read_text(encoding="utf-8")).get("body")
    else:
        if OFFLINE:
            return None
        try:
            r = _session.get(url, headers={"Accept": "application/vnd.citationstyles.csl+json"}, timeout=40,
                             allow_redirects=True)
            body = r.json() if r.status_code == 200 else None
        except Exception:
            return None
        cp.parent.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps({"url": url, "body": body}), encoding="utf-8")
    if not body or not isinstance(body, dict):
        return None
    authors = [_person(a.get("given"), a.get("family"), (a.get("ORCID") or "").rstrip("/").split("/")[-1] or None, None,
                       name=a.get("literal") if not a.get("family") else None) for a in body.get("author", []) or []]
    dp = (body.get("issued") or {}).get("date-parts") or [[None]]
    title = body.get("title")
    title = title[0] if isinstance(title, list) and title else title
    cont = body.get("container-title")
    cont = cont[0] if isinstance(cont, list) and cont else cont
    return rec("doi.org", type=body.get("type"), title=clean_title(title), authors=authors,
               year=dp[0][0] if dp and dp[0] else None, container=cont, volume=body.get("volume"),
               issue=body.get("issue"), page=body.get("page"), doi=(body.get("DOI") or doi).lower(),
               publisher=body.get("publisher"))


# ------------------------------------------------------------------ Crossref
CR_SELECT = "DOI,title,subtitle,author,issued,published-print,published-online,container-title,short-container-title,volume,issue,page,article-number,type,is-referenced-by-count,publisher,abstract"


def crossref_doi(doi: str, fast: bool = False):
    """Publisher metadata for a DOI. fast=True: while Crossref is throttling us, read OpenAlex's copy instead of waiting."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/:;()')}"
    if fast and not _cache_path(url).exists() and _hold["crossref"] > time.time():
        r = openalex_doi(doi)
        if r and r.get("title"):
            r["source"] = "openalex"
            return r
    body = get("crossref", url, retries=2 if fast else 7)
    if not body or "message" not in body:
        if url in FAILED_URLS:                  # Crossref throttled us: fall back to OpenAlex's copy of the record
            r = openalex_doi(doi)
            if r and r.get("title"):
                r["source"] = "openalex"
                return r
        return None
    return _cr_norm(body["message"])


def crossref_search(bibliographic: str | None = None, author: str | None = None, year: int | None = None,
                    rows: int = 20, span: int = 1, fast: bool = False):
    q = {"rows": str(rows), "select": CR_SELECT}
    if fast and _hold["crossref"] > time.time() and bibliographic:
        q2 = dict(q)
        if author:
            q2["query.author"] = author
        q2["query.bibliographic"] = bibliographic[:400]
        if year:
            q2["filter"] = f"from-pub-date:{year - span},until-pub-date:{year + span}"
        if not _cache_path("https://api.crossref.org/works?" + urllib.parse.urlencode(q2)).exists():
            return openalex_search(bibliographic, year=year, per_page=min(rows, 25))
    if bibliographic:
        q["query.bibliographic"] = bibliographic[:400]
    if author:
        q["query.author"] = author
    if year:
        q["filter"] = f"from-pub-date:{year - span},until-pub-date:{year + span}"
    body = get("crossref", "https://api.crossref.org/works?" + urllib.parse.urlencode(q))
    if not body or "message" not in body:
        return []
    return [_cr_norm(it) for it in body["message"].get("items", [])]


def _cr_year(m):
    for k in ("issued", "published-print", "published-online"):
        dp = (m.get(k) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]:
            return int(dp[0][0])
    return None


def _cr_norm(m):
    authors = []
    collab = None
    for a in m.get("author", []) or []:
        if a.get("family") or a.get("given"):
            orcid = a.get("ORCID")
            if orcid:
                orcid = orcid.rstrip("/").split("/")[-1]
            aff = "; ".join(x.get("name", "") for x in (a.get("affiliation") or []) if x.get("name")) or None
            authors.append(_person(a.get("given"), a.get("family"), orcid, aff))
        elif a.get("name"):
            collab = collab or a["name"]
            authors.append(_person(None, None, None, None, name=a["name"]))
    title = clean_title((m.get("title") or [None])[0])
    sub = clean_title((m.get("subtitle") or [None])[0])
    if title and sub and sub.lower() not in title.lower():
        title = f"{title}: {sub}" if not title.rstrip().endswith((":", ".", "?", "!")) else f"{title} {sub}"
    cont = (m.get("container-title") or [None])[0] or (m.get("short-container-title") or [None])[0]
    page = m.get("page") or m.get("article-number")
    abstract = m.get("abstract")
    if abstract:
        abstract = re.sub(r"<[^>]+>", " ", abstract)
    return rec("crossref", type=m.get("type"), title=title, authors=authors, year=_cr_year(m), container=cont,
               volume=m.get("volume"), issue=m.get("issue"), page=page, doi=(m.get("DOI") or "").lower() or None,
               citations=m.get("is-referenced-by-count"), abstract=abstract, collaboration=collab,
               publisher=m.get("publisher"))


# ------------------------------------------------------------------ DataCite (Zenodo etc.)
def datacite_doi(doi: str):
    body = get("datacite", f"https://api.datacite.org/dois/{urllib.parse.quote(doi, safe='/')}")
    if not body or "data" not in body:
        return None
    a = body["data"]["attributes"]
    authors = []
    for c in a.get("creators", []) or []:
        orcid = None
        for ni in c.get("nameIdentifiers", []) or []:
            if "orcid" in (ni.get("nameIdentifierScheme") or "").lower():
                orcid = (ni.get("nameIdentifier") or "").rstrip("/").split("/")[-1]
        if c.get("nameType") == "Organizational" or (not c.get("familyName") and not c.get("givenName")):
            authors.append(_person(None, None, orcid, None, name=c.get("name")))
        else:
            aff = "; ".join((x if isinstance(x, str) else x.get("name", "")) for x in (c.get("affiliation") or [])) or None
            authors.append(_person(c.get("givenName"), c.get("familyName"), orcid, aff))
    title = (a.get("titles") or [{}])[0].get("title")
    typ = (a.get("types") or {}).get("resourceTypeGeneral")
    return rec("datacite", type=typ, title=clean_title(title), authors=authors, year=a.get("publicationYear"),
               container=a.get("publisher") if isinstance(a.get("publisher"), str) else (a.get("publisher") or {}).get("name"),
               doi=doi.lower(), url=a.get("url"), publisher=a.get("publisher") if isinstance(a.get("publisher"), str) else None,
               version=a.get("version"))


# ------------------------------------------------------------------ arXiv
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def _id_cache(aid: str) -> Path:
    h = hashlib.sha1(("arxiv-id:" + aid).encode()).hexdigest()
    return CACHE / "arxiv_ids" / f"{h}.json"


def arxiv_ids(ids: list[str]) -> dict[str, dict]:
    """Metadata for arXiv ids: per-id cache first, then batched API calls (50 ids per call)."""
    out, todo = {}, []
    for aid in sorted(set(ids)):
        cp = _id_cache(aid)
        if cp.exists():
            obj = json.loads(cp.read_text(encoding="utf-8"))
            if obj.get("rec"):
                out[aid] = obj["rec"]
        else:
            todo.append(aid)
    if OFFLINE:
        return out
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"id_list": ",".join(chunk), "max_results": str(len(chunk))})
        text = get("arxiv", url, parse="text")
        if text is None:
            continue
        got = _arxiv_parse(text)
        for aid in chunk:
            r = got.get(aid)
            cp = _id_cache(aid)
            cp.parent.mkdir(parents=True, exist_ok=True)
            cp.write_text(json.dumps({"id": aid, "rec": r}), encoding="utf-8")
            if r:
                out[aid] = r
    return out


def arxiv_search(query: str, max_results: int = 30):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": query, "max_results": str(max_results)})
    text = get("arxiv", url, parse="text")
    return list(_arxiv_parse(text).values()) if text else []


def _arxiv_parse(text: str) -> dict[str, dict]:
    out = {}
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return out
    for e in root.findall("a:entry", ATOM):
        idurl = (e.findtext("a:id", default="", namespaces=ATOM) or "").strip()
        m = re.search(r"abs/(.+?)(v\d+)?$", idurl)
        if not m:
            continue
        aid = m.group(1)
        title = re.sub(r"\s+", " ", e.findtext("a:title", default="", namespaces=ATOM) or "").strip()
        if title == "Error":
            continue
        authors = []
        for a in e.findall("a:author", ATOM):
            nm = (a.findtext("a:name", default="", namespaces=ATOM) or "").strip()
            g, f = _split_full(nm)
            authors.append(_person(g, f))
        published = e.findtext("a:published", default="", namespaces=ATOM) or ""
        doi = e.findtext("arxiv:doi", default=None, namespaces=ATOM)
        jref = e.findtext("arxiv:journal_ref", default=None, namespaces=ATOM)
        abstract = re.sub(r"\s+", " ", e.findtext("a:summary", default="", namespaces=ATOM) or "").strip()
        out[aid] = rec("arxiv", type="preprint", title=title, authors=authors,
                       year=int(published[:4]) if published[:4].isdigit() else None,
                       doi=doi.lower() if doi else None, arxiv=aid, journal_ref=jref, abstract=abstract)
    return out


# ------------------------------------------------------------------ INSPIRE-HEP
IN_FIELDS = ("titles.title,authors.full_name,authors.ids,authors.affiliations.value,publication_info,dois.value,"
             "arxiv_eprints.value,citation_count,earliest_date,preprint_date,abstracts.value,document_type,"
             "collaborations.value,texkeys,imprints.date,thesis_info.date")


def inspire_search(q: str, size: int = 25, sort: str = "mostcited"):
    url = "https://inspirehep.net/api/literature?" + urllib.parse.urlencode(
        {"q": q, "size": str(size), "sort": sort, "fields": IN_FIELDS})
    body = get("inspire", url)
    if not body:
        return []
    return [_in_norm(h.get("metadata", {}), h.get("id")) for h in body.get("hits", {}).get("hits", [])]


def inspire_record(recid: str):
    body = get("inspire", f"https://inspirehep.net/api/literature/{recid}?fields={IN_FIELDS}")
    return _in_norm(body.get("metadata", {}), recid) if body else None


def _in_norm(md, recid=None):
    authors = []
    for a in md.get("authors", []) or []:
        g, f = _split_full(a.get("full_name", ""))
        orcid = None
        for i in a.get("ids", []) or []:
            if i.get("schema") == "ORCID":
                orcid = i.get("value")
        aff = "; ".join(x.get("value", "") for x in (a.get("affiliations") or []) if x.get("value")) or None
        authors.append(_person(g, f, orcid, aff))
    pubs = md.get("publication_info") or []
    pi = next((p for p in pubs if p.get("journal_title")), pubs[0] if pubs else {})
    year = pi.get("year")
    if not year:
        for k in ("earliest_date", "preprint_date"):
            if md.get(k):
                year = int(str(md[k])[:4])
                break
    if not year and md.get("imprints"):
        d = md["imprints"][0].get("date")
        year = int(str(d)[:4]) if d else None
    page = pi.get("artid") or (f"{pi.get('page_start')}" + (f"-{pi['page_end']}" if pi.get("page_end") else "")
                               if pi.get("page_start") else None)
    dois = [d.get("value", "").lower() for d in md.get("dois", []) or [] if d.get("value")]
    arx = [x.get("value") for x in md.get("arxiv_eprints", []) or [] if x.get("value")]
    collab = ", ".join(c.get("value") for c in md.get("collaborations", []) or [] if c.get("value")) or None
    return rec("inspire", type=",".join(md.get("document_type", []) or []) or None,
               title=clean_title(((md.get("titles") or [{}])[0]).get("title")), authors=authors, year=year,
               container=pi.get("journal_title"), volume=pi.get("journal_volume"), issue=pi.get("journal_issue"),
               page=page, doi=dois[0] if dois else None, arxiv=arx[0] if arx else None,
               citations=md.get("citation_count"), abstract=((md.get("abstracts") or [{}])[0]).get("value"),
               collaboration=collab, inspire_id=str(recid) if recid else None,
               texkey=(md.get("texkeys") or [None])[0])


# ------------------------------------------------------------------ OpenAlex
def openalex_search(search: str, year: int | None = None, per_page: int = 25):
    q = {"search": search[:300], "per-page": str(per_page)}
    if year:
        q["filter"] = f"publication_year:{year - 1}-{year + 1}"
    body = get("openalex", "https://api.openalex.org/works?" + urllib.parse.urlencode(q))
    if not body:
        return []
    return [_oa_norm(w) for w in body.get("results", [])]


def openalex_doi(doi: str):
    body = get("openalex", f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi, safe='/')}")
    return _oa_norm(body) if body else None


def _oa_norm(w):
    authors = []
    for au in w.get("authorships", []) or []:
        nm = (au.get("author") or {}).get("display_name") or au.get("raw_author_name") or ""
        g, f = _split_full(nm)
        orcid = (au.get("author") or {}).get("orcid")
        if orcid:
            orcid = orcid.rstrip("/").split("/")[-1]
        aff = "; ".join(i.get("display_name", "") for i in au.get("institutions", []) or [] if i.get("display_name")) or None
        authors.append(_person(g, f, orcid, aff))
    loc = w.get("primary_location") or {}
    src = (loc.get("source") or {}) if loc else {}
    bib = w.get("biblio") or {}
    doi = (w.get("doi") or "").replace("https://doi.org/", "").lower() or None
    page = bib.get("first_page") + (f"-{bib['last_page']}" if bib.get("last_page") else "") if bib.get("first_page") else None
    return rec("openalex", type=w.get("type"), title=clean_title(w.get("title") or w.get("display_name")), authors=authors,
               year=w.get("publication_year"), container=src.get("display_name"), volume=bib.get("volume"),
               issue=bib.get("issue"), page=page, doi=doi, citations=w.get("cited_by_count"),
               openalex_id=(w.get("id") or "").split("/")[-1] or None)


def clean_title(t):
    if not t:
        return t
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", t).strip()


def first_family(r) -> str:
    for a in r.get("authors") or []:
        if a.get("family"):
            return a["family"]
        if a.get("name"):
            return ""
    return ""


def fold(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", strip_accents(s or "").lower())
