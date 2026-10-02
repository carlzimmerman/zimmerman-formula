#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cfg290_reference_check.py -- CFG290 referee: compare every DOI-bearing entry of the v3 references.bib against Crossref's
metadata (title, journal, volume, first page, year, first author), and every eprint-only entry against the arXiv API
(title, first author, and whether arXiv records a journal reference / DOI, i.e. whether a published version should be cited).
Reads small JSON/Atom responses only (no files are saved apart from this script's .out and _results.json).
Usage: python3 cfg290_reference_check.py      (needs network; prints one line per entry)
"""
import os, re, json, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(HERE, "..", "..", "qwen_claude_field_theory", "papers_2026", "mnras_submission_2026_v3", "references.bib")
txt = open(BIB).read()
entries = re.findall(r"@(\w+)\{([^,]+),(.*?)\}\s*(?=@|\Z)", txt, flags=re.S)
def field(body, name):
    m = re.search(r"\b" + name + r"\s*=\s*\{", body)
    if m:                                    # brace-matched value (author lists nest braces two deep, e.g. {Macci{\`o}})
        i, depth = m.end(), 1
        while depth and i < len(body):
            depth += {"{": 1, "}": -1}.get(body[i], 0); i += 1
        return body[m.end():i - 1]
    m = re.search(name + r"\s*=\s*([0-9]+)", body)
    return m.group(1) if m else None
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cfg290-referee-check (mailto:none)"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read()
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())
RES = []
for typ, key, body in entries:
    doi, eprint = field(body, "doi"), field(body, "eprint")
    vol, pages, year = field(body, "volume"), field(body, "pages"), field(body, "year")
    a1 = re.search(r"\{([^{}]+)\}", field(body, "author") or "")       # the first braced family name, e.g. {Klinkhamer}
    a1 = a1.group(1) if a1 else "NO-AUTHOR-PARSED"
    row = dict(key=key, doi=doi, eprint=eprint, bib=dict(volume=vol, pages=pages, year=year, first_author=a1))
    try:
        if doi and not doi.startswith("10.5281/zenodo"):
            d = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
            cr_page = (d.get("page") or d.get("article-number") or "")
            cr_year = (d.get("issued", {}).get("date-parts") or [[None]])[0][0]
            cr_a1 = (d.get("author") or [{}])[0].get("family", "")
            ok_vol = str(d.get("volume")) == str(vol)
            ok_page = norm(str(pages).split("-")[0]) == norm(cr_page.split("-")[0]) or norm(str(pages)) in norm(cr_page)
            ok_year = str(cr_year) == str(year)
            ok_a1 = norm(cr_a1)[:5] in norm(a1) or norm(a1)[:5] in norm(cr_a1)
            row.update(source="crossref", title=(d.get("title") or [""])[0][:90], journal=(d.get("container-title") or [""])[0],
                       volume=d.get("volume"), page=cr_page, year=cr_year, first_author=cr_a1, ok=dict(volume=ok_vol, page=ok_page, year=ok_year, author=ok_a1))
        elif doi and doi.startswith("10.5281/zenodo"):
            d = json.loads(get("https://zenodo.org/api/records/" + doi.split(".")[-1]))
            row.update(source="zenodo", title=d.get("metadata", {}).get("title", "")[:110], year=d.get("metadata", {}).get("publication_date"),
                       version=d.get("metadata", {}).get("version"), ok=dict(resolves=True))
        elif eprint:
            aid = eprint.replace("arXiv:", "")
            x = ET.fromstring(get("http://export.arxiv.org/api/query?id_list=" + aid))
            ns = {"a": "http://www.w3.org/2005/Atom", "ar": "http://arxiv.org/schemas/atom"}
            e = x.find("a:entry", ns)
            title = " ".join((e.findtext("a:title", "", ns) or "").split())
            jref = e.findtext("ar:journal_ref", "", ns); adoi = e.findtext("ar:doi", "", ns)
            fa = (e.find("a:author", ns).findtext("a:name", "", ns) if e.find("a:author", ns) is not None else "")
            row.update(source="arxiv", title=title[:110], first_author=fa, journal_ref=jref, arxiv_doi=adoi,
                       ok=dict(author=norm(a1)[:5] in norm(fa), published_version_exists=bool(jref or adoi)))
        else:
            row.update(source="none", ok=dict(no_identifier=True))
    except Exception as ex:
        row.update(source="error", error=str(ex)[:120])
    RES.append(row)
    flag = "" if row.get("ok") and all(v for k, v in row["ok"].items() if k != "published_version_exists") else "  <-- CHECK"
    if row.get("ok", {}).get("published_version_exists"): flag += "  <-- arXiv lists a journal version"
    print(f"{key:20s} {row.get('source',''):8s} {json.dumps(row.get('ok'))} | {row.get('title','')[:70]} | "
          f"{row.get('journal', row.get('journal_ref',''))} {row.get('volume','')} {row.get('page','')} {row.get('year','')} {row.get('arxiv_doi','')}{flag}", flush=True)
    time.sleep(0.4)
json.dump(RES, open(os.path.join(HERE, "cfg290_reference_check_results.json"), "w"), indent=1, default=str)
print(f"\n{len(RES)} entries checked; wrote cfg290_reference_check_results.json")
