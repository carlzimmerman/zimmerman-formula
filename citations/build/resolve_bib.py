#!/usr/bin/env python3
"""Stage 2c: the repository's LaTeX papers — resolve every bibliography entry to a verified publication.

Reads every tracked .tex (\\bibitem blocks) and .bib (@entries) file in scope, cleans each reference to plain text,
and resolves it: an identifier written in the entry (DOI / arXiv) wins; otherwise Crossref's reference matcher is
asked, and a hit is accepted only if its first author matches the entry's first surname, its year is within one
year, and any volume/page written in the entry agrees; INSPIRE-HEP is the fallback. Entries that match nothing are
reported, never credited. Output: data/bib_resolution.json.gz
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apis  # noqa: E402
from common import DATA, EXCLUDE_PREFIXES, REPO, committed_files, dump_json, load_json, mentions_own_repository, norm_family, \
    own_author_families, own_author_given_initials, read_committed, scrub_text, strip_accents  # noqa: E402
from extract import ARXIV_NEW, ARXIV_OLD, DOI  # noqa: E402

ACC = {r'\"a': "ä", r'\"o': "ö", r'\"u': "ü", r"\'e": "é", r"\'a": "á", r"\'i": "í", r"\'o": "ó", r"\`e": "è",
       r"\^o": "ô", r"\c{c}": "ç", r"\l": "ł", r"\L": "Ł", r"\o": "ø", r"\ss": "ß", r"\v{s}": "š", r"\v{c}": "č",
       r"\~n": "ñ", r"\'c": "ć", r"\.z": "ż", r"\'n": "ń", r"\'s": "ś"}


def tex_files():
    return [p for p in committed_files((".tex", ".bib")) if not p.startswith(EXCLUDE_PREFIXES)]


def detex(s: str) -> str:
    s = s.replace("{", "").replace("}", "") if False else s
    for k, v in ACC.items():
        s = s.replace("{" + k + "}", v).replace(k, v)
    s = re.sub(r"\\(?:textit|textbf|emph|it|bf|em|rm|sc|textsc|mathrm|url|href)\s*", "", s)
    s = re.sub(r"\\newblock|\\bibinfo\{[^}]*\}|\\bibfield\{[^}]*\}", " ", s)
    s = s.replace("~", " ").replace(r"\&", "&").replace("--", "–")
    s = re.sub(r"\\[ ,;:!]", " ", s)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_tex(path: str, text: str):
    items = []
    for m in re.finditer(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}(.*?)(?=\\bibitem|\\end\{thebibliography\}|\Z)", text, re.S):
        line = text.count("\n", 0, m.start()) + 1
        raw = m.group(2)
        items.append({"file": path, "line": line, "key": m.group(1), "raw": raw[:1200], "text": detex(raw)[:600]})
    return items


def parse_bib(path: str, text: str):
    items = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, re.S):
        typ, key, body = m.group(1).lower(), m.group(2), m.group(3)
        if typ in ("comment", "string", "preamble"):
            continue
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}|\"[^\"]*\"|\d+)", body):
            fields[fm.group(1).lower()] = fm.group(2).strip("{}\"")
        au = fields.get("author", "")
        first = au.split(" and ")[0] if au else ""
        first_fam = first.split(",")[0].strip() if "," in first else (first.split()[-1] if first.split() else "")
        text_ = detex(f"{au}. {fields.get('year', '')}. {fields.get('title', '')}. {fields.get('journal', '')} "
                      f"{fields.get('volume', '')} {fields.get('pages', '')}")
        line = text.count("\n", 0, m.start()) + 1
        items.append({"file": path, "line": line, "key": key, "raw": body[:1200], "text": text_[:600],
                      "bib": {k: detex(v) for k, v in fields.items()}, "first": detex(first_fam)})
    return items


YEAR = re.compile(r"\b(1[6-9]\d\d|20[0-2]\d)[a-z]?\b")
SURNAME = re.compile(r"([A-ZÀ-ÖØ-ÞŁŻŠŽČ][\w'’À-ÿłżšžčćńś\-]+(?:\s+(?:de|van|von|der|den|le|la|di|del|da)\s+[A-Z][\w'’\-]+)?)")


def first_surname(it):
    if it.get("first"):
        return it["first"]
    t = it["text"]
    t = re.sub(r"^(?:[A-Z]\.\s*-?){1,3}\s*", "", t)          # "M. Milgrom, ..." -> "Milgrom, ..."
    m = SURNAME.match(t)
    return m.group(1) if m else None


def own_initial(it):
    """The first author's first initial when the entry writes one ("C. P. Surname" / "Surname, C." / "Surname C."),
    else None."""
    t = it["text"]
    m = re.match(r"^\s*([A-Z])\.", t) or re.match(r"^\s*[^\W\d_][\w'’-]+,?\s+([A-Z])\.?(?:\s|,|$)", t)
    return m.group(1).lower() if m else None


def vol_page(t):
    m = re.search(r"\b(\d{1,4})\s*[,:]\s*(?:no\.\s*\d+\s*,\s*)?([A-Z]?\d{1,6})\b", t)
    return (m.group(1), m.group(2)) if m else (None, None)


JUNK_DOI = re.compile(r"\.sm\d+$|/fig-\d+$|/table-\d+$|-rc\d+$|-ac\d+$|-cc\d+$|^10\.7554/elife\.\d+\.\d+$|pamphlet", re.I)


def accept(r, fam, year, vol, page):
    if not r or not r.get("title") or not r.get("authors"):
        return False                                   # a match must name its authors (rejects figures, SI, reviews)
    if r.get("doi") and JUNK_DOI.search(r["doi"]) and not r["doi"].startswith("10.1103/"):
        return False
    got = norm_family(apis.first_family(r) or "")
    want = norm_family(fam or "")
    if not got:
        org = ((r.get("authors") or [{}])[0].get("name") or "")
        if not (want and want in norm_family(org)):
            return False
    elif want and got != want and not (len(want) >= 4 and (got.endswith(want) or want.endswith(got))):
        org = ((r.get("authors") or [{}])[0].get("name") or "").lower()
        if not org or want not in norm_family(org):
            return False
    if year and r.get("year") and abs(int(r["year"]) - year) > 1:
        return False
    if vol and r.get("volume") and str(r["volume"]) != vol:
        return False
    return True


IDS = re.compile(r"(?:arXiv:?\s*)?\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}|10\.\d{4,9}/\S+|https?://\S+", re.I)
COLLAB = re.compile(r"^\s*(?:The\s+)?([A-Z][\w/+-]*(?:\s+[A-Z][\w/+-]*)?)\s+[Cc]ollaboration|^\s*(?:The\s+)?[A-Z]{2,}[\w/+-]*\s+(?:Team|Consortium)")


def entry_year(t: str):
    clean = IDS.sub(" ", t)
    m = re.search(r"\((1[6-9]\d\d|20[0-2]\d)[a-z]?\)", clean) or YEAR.search(clean)
    return int(m.group(1)) if m else None


def resolve(it):
    t = it["text"]
    raw = it["raw"]
    fam = None if COLLAB.search(t) else first_surname(it)
    year = entry_year(t)
    if it.get("bib", {}).get("year", "").isdigit():
        year = int(it["bib"]["year"])
    vol, page = vol_page(t)
    ids = []
    for m in DOI.finditer(raw):
        ids.append(("doi", m.group(1).rstrip(".):]}").lower()))
    if it.get("bib", {}).get("doi"):
        ids.append(("doi", it["bib"]["doi"].lower()))
    for m in ARXIV_NEW.finditer(raw):
        ids.append(("arxiv", m.group(1)))
    for m in ARXIV_OLD.finditer(raw):
        ids.append(("arxiv", m.group(1)))
    if it.get("bib", {}).get("eprint"):
        ids.append(("arxiv", it["bib"]["eprint"]))
    for k, v in ids:
        if k == "doi":
            r = apis.crossref_doi(v) or apis.datacite_doi(v)
            if r and r.get("title"):
                return {"status": "id", "doi": v, "check": accept(r, fam, year, None, None)}
        else:
            got = apis.arxiv_ids([v]).get(v)
            if got:
                return {"status": "id", "arxiv": v, "doi": got.get("doi"), "check": accept(got, fam, year, None, None)}
    if not year or (not fam and not COLLAB.search(t)):
        return {"status": "unparsed"}
    for r in apis.crossref_search(bibliographic=t[:350], rows=5, fast=True):
        if accept(r, fam, year, vol, page):
            return {"status": "crossref", "doi": r["doi"], "title": r.get("title"), "year": r.get("year")}
    if not fam:
        return {"status": "not_found", "first": None, "year": year}
    q = f'fa "{strip_accents(fam)}" and date {year - 1}->{year + 1}'
    title_words = set(w.lower() for w in re.findall(r"[A-Za-z]{5,}", t))
    best, best_ov = None, 0
    for r in apis.inspire_search(q, size=25):
        if not accept(r, fam, year, vol, page):
            continue
        if vol and page and str(r.get("volume")) == vol and str(r.get("page") or "").split("-")[0].lstrip("L") == page.lstrip("L"):
            return {"status": "inspire", "doi": r.get("doi"), "arxiv": r.get("arxiv"), "inspire_id": r.get("inspire_id"),
                    "title": r.get("title"), "year": r.get("year")}
        ov = len(title_words & set(w.lower() for w in re.findall(r"[A-Za-z]{5,}", r.get("title") or "")))
        if ov > best_ov:
            best, best_ov = r, ov
    if best and best_ov >= 2:
        return {"status": "inspire", "doi": best.get("doi"), "arxiv": best.get("arxiv"), "inspire_id": best.get("inspire_id"),
                "title": best.get("title"), "year": best.get("year")}
    return {"status": "not_found", "first": fam, "year": year}


def main():
    own = own_author_families()
    items = []
    for p in tex_files():
        raw = read_committed(p)
        if raw is None:
            continue
        text = raw.decode("utf-8", "replace")
        items += parse_bib(p, text) if p.endswith(".bib") else parse_tex(p, text)
    # the author's own works (and references to this repository) are kept out of the data: only a hash is stored
    own_init = own_author_given_initials()
    for it in items:
        fam = first_surname(it)
        ini = own_initial(it)
        if (fam and norm_family(fam) in own and (ini is None or ini in own_init)) or mentions_own_repository(it["text"]):
            it["text"] = "[own work] " + hashlib.sha1(it["text"].encode("utf-8")).hexdigest()[:12]
            it["own"] = True
        else:
            it["text"] = scrub_text(it["text"])
    # de-duplicate identical reference texts across files (versions of the same paper)
    uniq = {}
    for it in items:
        uniq.setdefault(it["text"], it)
    prev_p = DATA / "bib_resolution.json.gz"
    prev = load_json(prev_p) if prev_p.exists() else {}
    todo = [it for t, it in uniq.items() if t not in prev.get("by_text", {})]
    print(f"{len(items)} bibliography entries in {len({i['file'] for i in items})} files; {len(uniq)} distinct; {len(todo)} to resolve")
    by_text = dict(prev.get("by_text", {}))

    def work(it):
        if it.get("own"):
            return it["text"], {"status": "own"}
        try:
            return it["text"], resolve(it)
        except Exception as e:  # keep going
            return it["text"], {"status": "error", "error": repr(e)}

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(work, it) for it in todo]
        for i, fut in enumerate(cf.as_completed(futs), 1):
            t, res = fut.result()
            by_text[t] = res
            if i % 100 == 0:
                print(f"  {i}/{len(todo)} {dict(collections.Counter(v['status'] for v in by_text.values()))}", flush=True)
                dump_json({"by_text": by_text, "entries": []}, prev_p, gz=True)      # checkpoint (entries rewritten at the end)
    by_text = {t: v for t, v in by_text.items() if t in uniq}          # drop entries no longer in any paper
    entries = [{"file": it["file"], "line": it["line"], "key": it["key"], "text": it["text"]} for it in items]
    dump_json({"by_text": by_text, "entries": entries}, prev_p, gz=True)
    print("status:", dict(collections.Counter(by_text[e["text"]]["status"] for e in items if e["text"] in by_text)),
          "| API requests that failed permanently:", apis.DEGRADED["count"])


if __name__ == "__main__":
    main()
