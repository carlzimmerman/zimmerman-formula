#!/usr/bin/env python3
"""Stage 4: write the human-readable index from data/*.json.

  CITATIONS.md                       entry point (repository root)
  citations/README.md                how the index is built, scope, rebuild/verify
  citations/people/<A-Z>.md          everyone credited, A-Z (collaboration-only authors link to the paper)
  citations/people/<slug>.md         one page per person credited outside large collaborations
  citations/works/<slug>.md          one page per verified work: full reference, authors, every script + line
  citations/WORKS.md                 all works, most-used first
  citations/REFERENCES.bib           BibTeX for every work
  citations/UNVERIFIED.md            broken identifiers, citations matching no publication, ambiguous citations
  citations/BY_FOLDER.md             works used per top-level folder
  citations/<old-slug>/index.md      the previous index's 182 surname pages, now pointers into the new index
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CITE_DIR, DATA, REPO, head_commit, load_json, norm_family, slugify, strip_accents  # noqa: E402

TODAY = dt.date.today().isoformat()
KIND_ORDER = ["cited", "named", "data", "library", "algorithm", "paper"]
KIND_WORD = {"cited": "cited", "named": "named method/model", "data": "data used", "library": "library imported",
             "algorithm": "algorithm via library call", "paper": "cited in a paper"}
MAX_ROWS = 800


def q(path: str) -> str:
    return urllib.parse.quote(path)


def fam_of(a):
    return (a.get("family") or a.get("name") or "").strip()


def short_authors(authors, n_max=3):
    fams = []
    for a in authors or []:
        f = fam_of(a)
        if f:
            fams.append(f)
    if not fams:
        return "Anon."
    if len(fams) == 1:
        return fams[0]
    if len(fams) == 2:
        return f"{fams[0]} & {fams[1]}"
    if len(fams) <= n_max:
        return ", ".join(fams[:-1]) + f" & {fams[-1]}"
    return f"{fams[0]} et al."


def initials(given: str) -> str:
    out = []
    for t in re.split(r"[\s]+", given or ""):
        if not t:
            continue
        sub = [s for s in t.split("-") if s]
        out.append("-".join(s[0].upper() + "." for s in sub if s[0].isalpha()) if sub else "")
    return " ".join(o for o in out if o)


def full_reference(w, max_auth=12):
    au = w.get("all_authors") or []
    names = []
    for a in au[:max_auth]:
        if a.get("family"):
            names.append(f"{a['family']}, {initials(a.get('given', ''))}".strip().rstrip(","))
        elif a.get("name"):
            names.append(a["name"])
    if len(au) > max_auth:
        names.append(f"et al. ({len(au)} authors)")
    s = "; ".join(names) if names else "Anon."
    yr = w.get("year") or "n.d."
    s += f" ({yr}). "
    if w.get("title"):
        s += f"{w['title'].rstrip('.')}. "
    cont = w.get("container")
    if cont:
        s += f"*{cont}*"
        if w.get("volume"):
            s += f" {w['volume']}"
        if w.get("page"):
            s += f", {w['page']}"
        s += ". "
    ids = []
    if w.get("doi"):
        ids.append(f"[doi:{w['doi']}](https://doi.org/{w['doi']})")
    if w.get("arxiv"):
        ids.append(f"[arXiv:{w['arxiv']}](https://arxiv.org/abs/{w['arxiv']})")
    if w.get("inspire_id"):
        ids.append(f"[INSPIRE {w['inspire_id']}](https://inspirehep.net/literature/{w['inspire_id']})")
    if w.get("url") and not w.get("doi"):
        ids.append(f"[link]({w['url']})")
    return s + " ".join(ids)


def verified_text(w):
    vb = (w.get("verified_by") or "").split(" ")[0]
    return {"crossref": "Crossref (publisher record)", "datacite": "DataCite record", "arxiv": "arXiv record",
            "inspire": "INSPIRE-HEP record", "openalex": "OpenAlex copy of the publisher record",
            "doi.org": "DOI registration-agency record (doi.org)",
            "manual-record": "bibliographic record (no DOI exists; not machine-checkable)"}.get(vb, vb or "?")


def work_slugs(works):
    slugs, used = {}, set()
    for wid, w in sorted(works.items(), key=lambda kv: kv[0]):
        au = w.get("all_authors") or []
        f = next((fam_of(a) for a in au if fam_of(a)), "anon")
        base = slugify(f"{f}-{w.get('year') or 'nd'}-{(w.get('title') or wid)[:48]}")[:80].strip("-")
        s, k = base, 2
        while s in used:
            s, k = f"{base}-{k}", k + 1
        used.add(s)
        slugs[wid] = s
    return slugs


def bib_keys(works):
    groups = collections.defaultdict(list)
    for wid, w in works.items():
        au = w.get("all_authors") or []
        f = next((fam_of(a) for a in au if fam_of(a)), "Anon")
        f = re.sub(r"[^A-Za-z]", "", strip_accents(f)) or "Anon"
        groups[(f, w.get("year") or 0)].append(wid)
    keys = {}
    for (f, y), wids in groups.items():
        wids.sort(key=lambda x: (works[x].get("title") or "").lower())
        for i, wid in enumerate(wids):
            keys[wid] = f"{f}{y}" + ("" if len(wids) == 1 else "abcdefghijklmnopqrstuvwxyz"[i] if i < 26 else str(i))
    return keys


def a_is_org(au):
    return bool(au) and not au[0].get("family") and bool(au[0].get("name"))


def bibtex(wid, w, key):
    typ = w.get("type") or ""
    kind = "article"
    if typ in ("book", "monograph", "edited-book", "reference-book"):
        kind = "book"
    elif typ in ("book-chapter", "proceedings-article", "book-part"):
        kind = "incollection"
    elif typ in ("software", "Software") or wid.startswith("software:"):
        kind = "misc"
    elif typ in ("preprint", "posted-content", "Preprint") or (w.get("arxiv") and not w.get("container")):
        kind = "misc"
    elif wid.startswith("classic:"):
        kind = "book" if not re.search(r"\d", w.get("container") or "") else "misc"
    au = w.get("all_authors") or []
    names = []
    for a in au[:100]:
        if a.get("family"):
            names.append(f"{{{a['family']}}}, {a.get('given', '')}".strip().rstrip(","))
        elif a.get("name"):
            names.append("{" + a["name"] + "}")
    if len(au) > 100:
        names.append("others")
    esc = lambda s: str(s).replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")  # noqa: E731
    f = [f"  author = {{{' and '.join(names) or 'Anonymous'}}}"]
    if w.get("title"):
        f.append(f"  title = {{{{{esc(w['title'])}}}}}")
    if w.get("container"):
        f.append(f"  {'journal' if kind == 'article' else 'howpublished' if kind == 'misc' else 'booktitle' if kind == 'incollection' else 'publisher'}"
                 f" = {{{esc(w['container'])}}}")
    for k, bk in (("volume", "volume"), ("issue", "number"), ("page", "pages")):
        if w.get(k):
            f.append(f"  {bk} = {{{esc(w[k])}}}")
    if w.get("year"):
        f.append(f"  year = {{{w['year']}}}")
    if w.get("doi"):
        f.append(f"  doi = {{{w['doi']}}}")
    if w.get("arxiv"):
        f.append(f"  eprint = {{{w['arxiv']}}}")
        f.append("  archivePrefix = {arXiv}")
    if w.get("url") and not w.get("doi"):
        f.append(f"  url = {{{w['url']}}}")
    return f"@{kind}{{{key},\n" + ",\n".join(f) + "\n}\n"


def kinds_text(kinds):
    return ", ".join(KIND_WORD[k] for k in KIND_ORDER if k in kinds)


def main():
    works = load_json(DATA / "works.json.gz")
    usage = load_json(DATA / "usage.json.gz")
    people = load_json(DATA / "people.json.gz")
    un = load_json(DATA / "unresolved.json.gz")
    head = head_commit()[:10]
    wslug = work_slugs(works)
    bkeys = bib_keys(works)
    # people lookup per work (in author order)
    person_of = {}
    for pid, p in people.items():
        for wid in p["works"]:
            person_of.setdefault(wid, []).append(pid)
    out_people = CITE_DIR / "people"
    out_works = CITE_DIR / "works"
    for d in (out_people, out_works):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    all_files = {u["file"] for us in usage.values() for u in us}
    n_scripts_total = sum(1 for f in all_files if f.endswith((".py", ".ipynb")))
    n_papers_total = sum(1 for f in all_files if f.endswith((".tex", ".bib")))
    by_work_files = {wid: len(us) for wid, us in usage.items()}

    def cite_short(wid):
        w = works[wid]
        return f"{short_authors(w.get('all_authors'))} {w.get('year') or 'n.d.'}"

    # ---------------------------------------------------------------- work pages
    for wid, w in works.items():
        us = usage.get(wid, [])
        lines = [f"# {cite_short(wid)} — {w.get('title') or wid}", ""]
        lines.append(f"**Reference.** {full_reference(w, max_auth=30)}")
        lines.append("")
        lines.append(f"**BibTeX key:** `{bkeys[wid]}` (in [REFERENCES.bib](../REFERENCES.bib)) · **Verified against:** {verified_text(w)}, {w.get('verified_on', TODAY)}")
        lines.append("")
        au = w.get("all_authors") or []
        pids = {}
        for pid in person_of.get(wid, []):
            p = people[pid]
            pids[norm_family(p["family"]) + "|" + strip_accents(p["given"])[:1].lower()] = pid
        au_md = []
        for a in au:
            if a.get("family"):
                k = norm_family(a["family"]) + "|" + strip_accents(a.get("given") or "")[:1].lower()
                nm = f"{a.get('given', '')} {a['family']}".strip()
                au_md.append(f"[{nm}](../people/{pids[k]}.md)" if k in pids and not people[pids[k]]["collab_only"] else nm)
            elif a.get("name"):
                au_md.append(f"*{a['name']}*")
        lines.append(f"**Authors ({len(au)}):** " + ", ".join(au_md) if au_md else "**Authors:** (not listed in the record)")
        lines.append("")
        kinds = collections.Counter(k for u in us for k in u["kinds"])
        lines.append(f"## Used in {len(us)} script(s)")
        lines.append("")
        lines.append("How: " + ", ".join(f"{KIND_WORD[k]} in {kinds[k]}" for k in KIND_ORDER if kinds.get(k)) + ".")
        lines.append("")
        rows = sorted(us, key=lambda u: u["file"])
        if len(rows) > MAX_ROWS:
            tsv = out_works / f"{wslug[wid]}.tsv"
            tsv.write_text("script\thow\tlines\tvia\n" + "\n".join(
                f"{u['file']}\t{','.join(u['kinds'])}\t{' '.join(map(str, u['lines']))}\t{'; '.join(u['via'])}" for u in rows) + "\n",
                encoding="utf-8")
            by_dir = collections.Counter(u["file"].split("/")[0] for u in rows)
            lines.append(f"Too many scripts to list here; the complete list is in [{tsv.name}]({tsv.name}). By top-level folder:")
            lines.append("")
            lines.append("| folder | scripts |")
            lines.append("|---|---:|")
            for d, n in by_dir.most_common():
                lines.append(f"| `{d}/` | {n} |")
        else:
            lines.append("| script | how | lines |")
            lines.append("|---|---|---|")
            for u in rows:
                ln = u["lines"]
                first = f"#L{ln[0]}" if ln else ""
                lns = ", ".join(f"[{x}](../../{q(u['file'])}#L{x})" for x in ln[:8]) + (" …" if len(ln) > 8 else "")
                via = "; ".join(v for v in u["via"] if not v.startswith(("doi:", "arxiv:")))[:120]
                how = kinds_text(u["kinds"]) + (f" — {via}" if via and "cited" not in u["kinds"] else "")
                lines.append(f"| [`{u['file']}`](../../{q(u['file'])}{first}) | {how} | {lns} |")
        (out_works / f"{wslug[wid]}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- person pages (non-collaboration authors)
    def person_line(p):
        orcid = f" · ORCID [{p['orcid']}](https://orcid.org/{p['orcid']})" if p.get("orcid") else ""
        return orcid

    for pid, p in people.items():
        if p["collab_only"]:
            continue
        ws = sorted(p["works"], key=lambda w: -by_work_files.get(w, 0))
        lines = [f"# {p['display']}", ""]
        meta = [f"Credited in **{p['n_files']}** file(s) through **{len(ws)}** work(s)"
                + (f" ({p['n_files_research']} for the research itself, the rest as software or a numerical method)"
                   if p.get("n_files_research", p["n_files"]) != p["n_files"] else "")]
        if p.get("orcid"):
            meta.append(f"ORCID [{p['orcid']}](https://orcid.org/{p['orcid']})")
        if p.get("affiliations"):
            meta.append("affiliation on the cited work(s): " + "; ".join(a[:120] for a in p["affiliations"][:2]))
        lines.append(" · ".join(meta))
        lines.append("")
        lines.append("| work | used in | how |")
        lines.append("|---|---:|---|")
        for wid in ws:
            w = works[wid]
            kinds = collections.Counter(k for u in usage.get(wid, []) for k in u["kinds"])
            lines.append(f"| [{cite_short(wid)}](../works/{wslug[wid]}.md) — {(w.get('title') or '')[:110]} | "
                         f"{by_work_files.get(wid, 0)} | {kinds_text(kinds)} |")
        lines.append("")
        lines.append(f"[All people A–Z](README.md) · [How this index is built](../README.md)")
        (out_people / f"{pid}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- A-Z letter pages
    letters = collections.defaultdict(list)
    for pid, p in people.items():
        L = strip_accents(p["family"])[:1].upper()
        letters[L if L.isalpha() else "#"].append(p)
    idx = ["# People credited, A–Z", "",
           f"**{len(people):,} people** whose published work is used by the repository's scripts. "
           f"{sum(1 for p in people.values() if not p['collab_only']):,} have their own page; "
           f"{sum(1 for p in people.values() if p['collab_only']):,} are credited as authors of large collaboration "
           "papers (more than 40 authors) and link straight to that paper.", "",
           " · ".join(f"[{L}]({L if L != '#' else 'other'}.md) ({len(letters[L])})" for L in sorted(letters)), "",
           "[How this index is built](../README.md) · [All works](../WORKS.md)"]
    (out_people / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    for L, ps in letters.items():
        ps.sort(key=lambda p: p["sort"])
        lines = [f"# People — {L}", "", f"{len(ps)} people. [A–Z](README.md)", ""]
        for p in ps:
            ws = sorted(p["works"], key=lambda w: -by_work_files.get(w, 0))
            name = f"{p['family']}, {p['given']}".strip().rstrip(",")
            if p["collab_only"]:
                wl = ", ".join(f"[{cite_short(w)}](../works/{wslug[w]}.md)" for w in ws[:3])
                lines.append(f"- {name} — author of {wl}{' …' if len(ws) > 3 else ''} · {p['n_files']} scripts")
            else:
                lines.append(f"- [{name}]({p['id']}.md) — {len(ws)} work(s) · {p['n_files']} scripts")
        (out_people / f"{L if L != '#' else 'other'}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- WORKS.md, REFERENCES.bib
    order = sorted(works, key=lambda w: (-by_work_files.get(w, 0), cite_short(w)))
    PAGE = 1000
    n_pages = (len(order) + PAGE - 1) // PAGE
    page_name = lambda k: "WORKS.md" if k == 1 else f"WORKS-{k}.md"  # noqa: E731
    for k in range(1, n_pages + 1):
        chunk = order[(k - 1) * PAGE:k * PAGE]
        nav = " · ".join((f"**{j}**" if j == k else f"[{j}]({page_name(j)})") for j in range(1, n_pages + 1))
        lines = ["# Works used by the scripts" + (f" (page {k} of {n_pages})" if n_pages > 1 else ""), "",
                 f"**{len(works):,} verified works**, most-used first. Every entry was checked against its publisher / "
                 "arXiv / INSPIRE record (see *Verified against* on each page).", "", f"Pages: {nav}", "",
                 "| # | work | files | how |", "|---:|---|---:|---|"]
        for i, wid in enumerate(chunk, (k - 1) * PAGE + 1):
            w = works[wid]
            kinds = collections.Counter(kk for u in usage.get(wid, []) for kk in u["kinds"])
            lines.append(f"| {i} | [{cite_short(wid)}](works/{wslug[wid]}.md) — {(w.get('title') or '')[:90]} | "
                         f"{by_work_files.get(wid, 0)} | {kinds_text(kinds)} |")
        lines += ["", f"Pages: {nav}"]
        (CITE_DIR / page_name(k)).write_text("\n".join(lines) + "\n", encoding="utf-8")
    bib = [f"% REFERENCES.bib — every work credited by the citation index (generated {TODAY}, commit {head}).",
           "% Regenerate with: python3 citations/build/run_all.py", ""]
    for wid in sorted(works, key=lambda w: bkeys[w].lower()):
        bib.append(bibtex(wid, works[wid], bkeys[wid]))
    (CITE_DIR / "REFERENCES.bib").write_text("\n".join(bib), encoding="utf-8")

    # ---------------------------------------------------------------- BY_FOLDER.md
    per_dir = collections.defaultdict(collections.Counter)
    for wid, us in usage.items():
        for u in us:
            per_dir[u["file"].split("/")[0]][wid] += 1
    lines = ["# Works used, by top-level folder", "", "[Back to the index](../CITATIONS.md)", ""]
    for d in sorted(per_dir, key=lambda d: -sum(per_dir[d].values())):
        c = per_dir[d]
        lines.append(f"## `{d}/` — {len(c)} works")
        lines.append("")
        lines.append(", ".join(f"[{cite_short(w)}](works/{wslug[w]}.md) ({n})" for w, n in c.most_common(60))
                     + (" …" if len(c) > 60 else ""))
        lines.append("")
    (CITE_DIR / "BY_FOLDER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- UNVERIFIED.md
    unr = un["unresolved"]
    by_key = collections.defaultdict(list)
    for r in unr:
        by_key[(r["key"], r["status"])].append(r)
    lines = ["# References that could not be verified", "",
             "Everything here is written in a script but could not be tied to a real publication. It is **not** "
             "credited to anyone in the index. Each item is either a typo, a truncated or invented reference "
             "(some scripts were machine-written), or too vague to pin down. Fix the script, or add a decision to "
             "`citations/build/registry/ay_overrides.yaml`, then rebuild.", ""]
    lines.append(f"## 1. Identifiers that do not resolve ({len(un['defects'])})")
    lines.append("")
    lines.append("| script | identifier as written | problem |")
    lines.append("|---|---|---|")
    for d in sorted(un["defects"], key=lambda d: d["file"]):
        ln = d["lines"][0] if d["lines"] else None
        lines.append(f"| [`{d['file']}`](../{q(d['file'])}{'#L' + str(ln) if ln else ''}) | `{d['identifier']}` | {d['problem']} |")
    lines.append("")
    nf = {k: v for k, v in by_key.items() if k[1] in ("not_found", "error")}
    lines.append(f"## 2. Author–year citations that match no publication ({len(nf)} distinct, {sum(len(v) for v in nf.values())} places)")
    lines.append("")
    lines.append("First author + year searched in INSPIRE-HEP, Crossref and arXiv (±1 year); nothing matched.")
    lines.append("")
    lines.append("| citation as written | finding | where |")
    lines.append("|---|---|---|")
    for (key, st), rs in sorted(nf.items(), key=lambda kv: -len(kv[1])):
        raw = next((r["raw"] for r in rs if r.get("raw")), key).replace("|", "/").replace("\n", " ")
        note = (next((r.get("note") for r in rs if r.get("note")), None) or "no match found").replace("|", "/")
        where = ", ".join(f"[`{r['file']}`](../{q(r['file'])}{'#L' + str(r['lines'][0]) if r['lines'] else ''})" for r in rs[:4])
        lines.append(f"| {raw[:90]} | {note[:160]} | {where}{' …' if len(rs) > 4 else ''} |")
    lines.append("")
    amb = {k: v for k, v in by_key.items() if k[1] in ("ambiguous", "auto", "override-unresolvable", "pending")}
    lines.append(f"## 3. Author–year citations that match several publications ({len(amb)} distinct, {sum(len(v) for v in amb.values())} places)")
    lines.append("")
    lines.append("The script's own text does not say which paper is meant. The closest candidates are listed; add the "
                 "right one to `registry/ay_overrides.yaml` to credit it.")
    lines.append("")
    lines.append("| citation as written | candidates | where |")
    lines.append("|---|---|---|")
    for (key, st), rs in sorted(amb.items(), key=lambda kv: -len(kv[1])):
        raw = next((r["raw"] for r in rs if r.get("raw")), key).replace("|", "/").replace("\n", " ")
        cands = rs[0].get("candidates") or []
        cs = "; ".join(f"{(c.get('title') or '')[:60]} ({c.get('year')}, "
                       f"{'doi:' + c['doi'] if c.get('doi') else 'arXiv:' + str(c.get('arxiv'))})" for c in cands[:3])
        where = ", ".join(f"[`{r['file']}`](../{q(r['file'])}{'#L' + str(r['lines'][0]) if r['lines'] else ''})" for r in rs[:3])
        lines.append(f"| {raw[:70]} | {cs.replace('|', '/')} | {where}{' …' if len(rs) > 3 else ''} |")
    bu = un.get("bib_unresolved", [])
    by_txt = collections.defaultdict(list)
    for r in bu:
        by_txt[r["text"]].append(r)
    lines.append("")
    lines.append(f"## 4. Bibliography entries in the repository's LaTeX papers that match no publication ({len(by_txt)} distinct, {len(bu)} places)")
    lines.append("")
    lines.append("Matched against Crossref and INSPIRE-HEP on first author, year and (when written) volume; none agreed. "
                 "Many are books, theses or conference talks that those databases do not hold; some are garbled.")
    lines.append("")
    lines.append("| entry as written | where |")
    lines.append("|---|---|")
    for txt, rs in sorted(by_txt.items(), key=lambda kv: -len(kv[1])):
        where = ", ".join(f"[`{r['file']}`](../{q(r['file'])}#L{r['line']})" for r in rs[:3])
        lines.append(f"| {txt[:140].replace('|', '/')} | {where}{' …' if len(rs) > 3 else ''} |")
    mis = un.get("misnamed", [])
    lines.append("")
    lines.append(f"## 5. Citations resolved on review whose written author or year differs from the paper ({len(mis)})")
    lines.append("")
    lines.append("These ARE credited, to the paper named here. The citation text in the script names a different first "
                 "author or year: sometimes a genuine slip in the script (a senior author written as first author, a "
                 "wrong year), sometimes only the index's parser keying on a later author. The reviewer's note says which.")
    lines.append("")
    lines.append("| citation as written | credited paper | reviewer's note | where |")
    lines.append("|---|---|---|---|")
    for r in sorted(mis, key=lambda r: r["key"]):
        raw = (r["raws"][0] if r["raws"] else r["key"]).replace("|", "/").replace("\n", " ")[:70]
        where = ", ".join(f"[`{f}`](../{q(f)}{'#L' + str(l[0]) if l else ''})" for f, l in r["files"].items())
        lines.append(f"| {raw} | {(r['paper'] or '')[:110].replace('|', '/')} | {(r['note'] or '')[:220].replace('|', '/')} | {where} |")
    (CITE_DIR / "UNVERIFIED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- summary json for README / CITATIONS.md
    top_people = sorted((p for p in people.values() if not p["collab_only"]),
                        key=lambda p: (-p.get("n_files_research", 0), -p["n_files"]))[:60]
    top_tools = sorted((p for p in people.values() if not p["collab_only"] and p["n_files"] > p.get("n_files_research", 0)),
                       key=lambda p: -(p["n_files"] - p.get("n_files_research", 0)))[:12]
    summary = {"date": TODAY, "commit": head, "n_people": len(people),
               "n_people_pages": sum(1 for p in people.values() if not p["collab_only"]),
               "n_collab_only": sum(1 for p in people.values() if p["collab_only"]),
               "n_works": len(works), "n_scripts_credit": n_scripts_total, "n_papers_credit": n_papers_total,
               "n_bib_unresolved_distinct": len({r["text"] for r in un.get("bib_unresolved", [])}),
               "n_scripts_scanned": len(load_json(DATA / "texts.json.gz")),
               "n_unresolved_places": len(unr), "n_unresolved_distinct": len(by_key), "n_defects": len(un["defects"]),
               "n_notfound_distinct": len(nf), "n_ambiguous_distinct": len(amb),
               "n_orgs": len(un["orgs"]), "n_own_files": len(un.get("own_refs", {})), "top_works": [(cite_short(w), (works[w].get("title") or "")[:90],
                                                          by_work_files.get(w, 0), wslug[w]) for w in order[:40]],
               "top_people": [(p["display"], p["id"], p.get("n_files_research", 0), len(p["works"])) for p in top_people],
               "top_tools": [(p["display"], p["id"], p["n_files"], len(p["works"])) for p in top_tools]}
    (DATA / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if not k.startswith("top_")}, indent=1))


if __name__ == "__main__":
    main()
