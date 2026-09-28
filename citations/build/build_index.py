#!/usr/bin/env python3
"""Stage 3: assemble the index — which script uses which verified work, and which people wrote those works.

Evidence kinds (per script, with line numbers where they exist):
  cited      an author-year citation, arXiv id, DOI or bibcode written in a comment/docstring/string
  named      a named method/equation/model/theory (registry/eponyms.yaml, registry/concepts.yaml)
  data       a named data product (registry/datasets.yaml)
  library    an imported scientific library (registry/software.yaml)
  algorithm  a numerical/statistical method reached through a library call (registry/algorithms.yaml)
Works by the repository's own author (read from CITATION.cff) are counted but kept out of the people index.
Outputs: data/works.json, data/usage.json.gz, data/people.json, data/unresolved.json
"""
from __future__ import annotations

import bisect
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (DATA, REGISTRY, REPO, dump_json, load_json, norm_family, own_author_families, read_committed,  # noqa: E402
                    slugify, strip_accents)
from fetch import classic_record, wid_arxiv, wid_doi  # noqa: E402

import yaml  # noqa: E402

BIG_COLLAB = 40          # works with more authors than this credit their authors "through a collaboration paper"


# ------------------------------------------------------------------ registries
def load_yaml(name):
    p = REGISTRY / name
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or []) if p.exists() else []


def work_ids(spec, alias):
    """Registry work spec -> canonical work id (or None if it failed verification)."""
    if spec.get("classic") or spec.get("software"):
        return classic_record(spec, "software" if spec.get("software") else "classic")[0]
    for k in ("doi", "arxiv", "inspire"):
        if spec.get(k):
            raw = str(spec[k]).strip()
            return alias.get(f"{k}:{raw.lower() if k == 'doi' else raw}")
    return None


LIT = re.compile(r"[A-Za-zÀ-ÿ]{3,}")


def _split_top(rx: str):
    """Split a regex on '|' at nesting depth 0 (outside groups and character classes)."""
    parts, depth, cls, cur, i = [], 0, False, [], 0
    while i < len(rx):
        ch = rx[i]
        if ch == "\\" and i + 1 < len(rx):
            cur.append(rx[i:i + 2]); i += 2; continue
        if cls:
            cls = ch != "]"
        elif ch == "[":
            cls = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "|" and depth == 0:
            parts.append("".join(cur)); cur = []; i += 1; continue
        cur.append(ch); i += 1
    parts.append("".join(cur))
    return parts


def _branch_literal(rx: str):
    """Longest literal word that every match of this branch must contain (None if unsure)."""
    if re.search(r"\((?!\?[:=!<])", rx) is None and "(?:" not in rx:
        body = rx
    else:
        # a group with an internal alternation makes its content optional-ish: drop grouped parts
        body = re.sub(r"\((?:\?[:=!<]?)?[^()]*\|[^()]*\)[?*]?", " ", rx)
        body = re.sub(r"\((?:\?[:=!<]?)?[^()]*\)[?*]", " ", body)
    body = re.sub(r"\[[^\]]*\][?*]?", " ", body)                  # character classes
    body = re.sub(r"\\[bBsSdDwW]|\\.", " ", body)
    body = re.sub(r".[?*]", " ", body)                               # optional single chars
    body = re.sub(r"\{[^}]*\}|[()?*+.^$|]", " ", body)
    words = LIT.findall(body)
    return max(words, key=len) if words else None


def anchors_of(rx: str):
    """Literal words, one per top-level branch; a file must contain at least one for the regex to match.
    Returns (anchors, case_insensitive) or (None, False) when no safe prefilter exists."""
    ci = rx.startswith("(?i)")
    core = rx[4:] if ci else rx
    lits = []
    for br in _split_top(core):
        lit = _branch_literal(br)
        if not lit:
            return None, False
        lits.append(lit.lower() if ci else lit)
    return lits, ci


def anchor_of(rx: str):
    a, _ = anchors_of(rx)
    return a[0] if a and len(a) == 1 else None


class Matcher:
    def __init__(self, entries, kind, alias, source):
        self.items = []
        self.missing = []
        for e in entries:
            label = e.get("label") or e.get("concept")
            wids = [work_ids(w, alias) for w in e.get("works") or [] if isinstance(w, dict)]
            ok = [w for w in wids if w]
            if len(ok) < len(wids):
                self.missing.append((source, label, len(wids) - len(ok)))
            if not ok:
                continue
            pats = []
            for rx in e.get("patterns") or []:
                try:
                    pats.append((re.compile(rx), anchors_of(rx)))
                except re.error as err:
                    self.missing.append((source, label, f"bad regex {rx!r}: {err}"))
            ids = []
            for rx in e.get("ident") or []:
                try:
                    ids.append(re.compile(rx))
                except re.error as err:
                    self.missing.append((source, label, f"bad ident regex {rx!r}: {err}"))
            calls = []
            for rx in e.get("calls") or []:
                calls.append(re.compile(rx))
            self.items.append({"label": label, "works": ok, "pats": pats, "ident": ids, "calls": calls,
                               "kind": e.get("kind") or kind})


# ------------------------------------------------------------------ names and people
PARTS = {"de", "van", "von", "der", "den", "le", "la", "di", "del", "da", "dos", "du", "ten", "ter", "des", "della", "dal"}
NAME_FIX = {  # publisher-metadata quirks, keyed by (family, given-prefix)
    ("hamed", "nima"): ("Nima", "Arkani-Hamed"),
    ("lematre", ""): ("Georges", "Lemaître"),
}


CYR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
               ["a", "b", "v", "g", "d", "e", "yo", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya"]))


def translit(s):
    if not any("\u0400" <= ch <= "\u04ff" for ch in s):
        return s
    out = []
    for ch in s:
        lo = ch.lower()
        t = CYR.get(lo, ch)
        out.append(t.capitalize() if ch != lo and t else t)
    return "".join(out)


def smart_case(name):
    """'HOYLE' -> 'Hoyle', 'DE LAURENTIS' -> 'De Laurentis', 'CLERK-MAXWELL' -> 'Clerk-Maxwell', 'MCGAUGH' -> 'McGaugh'."""
    if not name or not name.isupper() or len(name) <= 1:
        return name
    def cap(w):
        w = w.lower()
        if w.startswith("mc") and len(w) > 2:
            return "Mc" + w[2:].capitalize()
        if w.startswith("o'") and len(w) > 2:
            return "O'" + w[2:].capitalize()
        return w.capitalize()
    return " ".join("-".join(cap(p) for p in w.split("-")) for w in name.split(" "))


def clean_person(a):
    given = re.sub(r"\s+", " ", (a.get("given") or "").replace("\xa0", " ")).strip()
    family = re.sub(r"\s+", " ", (a.get("family") or "").replace("\xa0", " ")).strip().strip(",")
    given, family = translit(given), smart_case(translit(family))
    gt = given.split()
    moved = []
    while gt and gt[-1].lower() in PARTS:                  # 'W. J. G. de' + 'Blok'; 'Arjen van der' + 'Wel'
        moved.insert(0, gt.pop())
    if moved:
        prefix = " ".join(moved)
        given = " ".join(gt)
        if not family.lower().startswith(prefix.lower() + " "):
            family = f"{prefix} {family}"
    if given.isupper() and len(given) > 3:
        given = smart_case(given)
    if family in ("Jr", "Jr.", "Sr", "Sr.", "II", "III") and len(given.split()) >= 2:
        toks = given.split()                                   # 'Clifford M. Will' + 'Jr' -> family Will
        given, family = " ".join(toks[:-1]), toks[-1]
    if len(family.strip(".")) == 1 and given and len(given.split()[-1].strip(".")) > 1:
        toks = given.split()                                   # 'Gothai' + 'L' -> 'L. Gothai'
        given, family = " ".join(toks[:-1] + [family]), toks[-1]
    if not family and given:
        given, family = "", given
    if family and not given and " " in family:
        toks = family.split(" ")
        i = len(toks) - 1
        while i > 0 and toks[i - 1].lower() in PARTS:
            i -= 1
        given, family = " ".join(toks[:i]), " ".join(toks[i:])
    m = re.match(r"^((?:[A-Z]\.\s?-?)+)\s*(.+)$", family)
    if m and not given:
        given, family = m.group(1).strip(), m.group(2)
    fx = NAME_FIX.get((norm_family(family), strip_accents(given).lower().split(" ")[0] if given else ""))
    if fx is None:
        fx = NAME_FIX.get((norm_family(family), ""))
    if fx:
        given, family = fx[0] or given, fx[1]
    if given.lower().startswith("nima arkani") and family.lower() == "hamed":
        given, family = "Nima", "Arkani-Hamed"
    return given, family


def given_tokens(given: str):
    g = strip_accents(given).replace("-", " ").replace(".", ". ")
    toks = [t for t in re.split(r"\s+", g) if t]
    first = None
    inits = []
    for t in toks:
        t0 = t.strip(".,")
        if not t0:
            continue
        inits.append(t0[0].lower())
        if first is None and len(t0) > 1 and not t.endswith(".") and t0.isalpha() and not t0.isupper():
            first = t0.lower()
    return first, "".join(inits)


def compatible(a, b):
    (fa, ia), (fb, ib) = a, b
    if not ia or not ib:
        return True
    if ia[0] != ib[0]:
        return False
    if fa and fb and fa != fb and not (fa.startswith(fb) or fb.startswith(fa)):
        return False
    if len(ia) > 1 and len(ib) > 1 and ia[:2] != ib[:2]:
        return False
    return True


def build_people(works, own_fams, own_init):
    inst = collections.defaultdict(list)       # norm family -> list of instances
    orgs = collections.defaultdict(set)
    own_works = set()
    for wid, w in sorted(works.items()):          # sorted: clustering and page names must not depend on run order
        if w.get("own"):                       # stub written by fetch.py for the repository author's own works
            own_works.add(wid)
            continue
        authors = w.get("_arxiv_authors") if w.get("_arxiv_authors") and len(w["_arxiv_authors"]) > len(w.get("authors") or []) \
            else w.get("authors") or []
        for i, a in enumerate(authors):
            if a.get("name") and not a.get("family"):
                orgs[a["name"]].add(wid)
                continue
            full = f"{a.get('given') or ''} {a.get('family') or ''}".strip()
            if re.search(r"(?i)\b(collaboration|consortium|team|group|survey|project)\b", full) or not re.search(r"[A-Za-zÀ-ÿ\u0400-\u04ff]{2}", full):
                if re.search(r"[A-Za-z]{3}", full):
                    orgs[full].add(wid)
                continue
            given, family = clean_person(a)
            nf = norm_family(family)
            if not nf:
                continue
            if nf in own_fams and (not given or strip_accents(given)[:1].lower() in own_init):
                own_works.add(wid)
                continue
            inst[nf].append({"wid": wid, "pos": i, "given": given, "family": family, "orcid": a.get("orcid"),
                             "aff": a.get("affiliation"), "tok": given_tokens(given)})
    people = {}
    for nf, lst in sorted(inst.items()):
        clusters = []
        by_orcid = {}
        for x in lst:
            if x["orcid"]:
                c = by_orcid.get(x["orcid"])
                if c is None:
                    c = {"members": [], "orcids": {x["orcid"]}, "full": set(), "inits": set()}
                    by_orcid[x["orcid"]] = c
                    clusters.append(c)
                c["members"].append(x)
        for c in clusters:
            for x in c["members"]:
                if x["tok"][0]:
                    c["full"].add(x["tok"][0])
                c["inits"].add(x["tok"][1])
        # full-first-name instances without ORCID
        rest = [x for x in lst if not x["orcid"]]
        for x in sorted(rest, key=lambda x: (x["tok"][0] is None, -len(x["tok"][1]), x["wid"], x["pos"])):
            cands = [c for c in clusters if any(compatible(x["tok"], m["tok"]) for m in c["members"])
                     and all(compatible(x["tok"], m["tok"]) for m in c["members"] if m["tok"][0])]
            if x["tok"][0]:
                exact = [c for c in cands if x["tok"][0] in c["full"]]
                pick = exact[0] if len(exact) == 1 else (cands[0] if len(cands) == 1 and not cands[0]["full"] else None)
                if pick is None and len(exact) > 1:
                    pick = max(exact, key=lambda c: len(c["members"]))
            else:
                pick = cands[0] if len(cands) == 1 else None
                if pick is None and len(cands) > 1:
                    # initials only and several compatible people: attach only if one clearly dominates
                    cands.sort(key=lambda c: -len(c["members"]))
                    if len(cands[0]["members"]) >= 3 * len(cands[1]["members"]):
                        pick = cands[0]
            if pick is None:
                pick = {"members": [], "orcids": set(), "full": set(), "inits": set()}
                clusters.append(pick)
            pick["members"].append(x)
            if x["tok"][0]:
                pick["full"].add(x["tok"][0])
            pick["inits"].add(x["tok"][1])
        for c in clusters:
            ms = c["members"]
            fam_forms = collections.Counter(m["family"] for m in ms)
            fam = max(fam_forms, key=lambda f: (not f.isupper(), strip_accents(f) != f, fam_forms[f], len(f)))
            giv = max((m["given"] for m in ms), key=lambda g: (given_tokens(g)[0] is not None, len(g.replace(".", ""))))
            display = f"{giv} {fam}".strip()
            wids = sorted({m["wid"] for m in ms})
            affs = collections.Counter(m["aff"] for m in ms if m["aff"])
            pid = slugify(f"{fam}-{giv}") if giv else slugify(fam)
            base, k = pid, 2
            while pid in people:
                pid, k = f"{base}-{k}", k + 1
            people[pid] = {"id": pid, "display": display, "given": giv, "family": fam, "sort": f"{strip_accents(fam).lower()} {strip_accents(giv).lower()}",
                           "orcid": sorted(c["orcids"])[0] if c["orcids"] else None,
                           "works": wids, "affiliations": [a for a, _ in affs.most_common(3)]}
    return people, {k: sorted(v) for k, v in orgs.items()}, own_works


_file_lines = {}


def window_text(path, lines, pad=4):
    """The script's own text around the cited lines (for override rules)."""
    if path not in _file_lines:
        try:
            _file_lines[path] = (read_committed(path) or b"").decode("utf-8", "replace").splitlines()
        except OSError:
            _file_lines[path] = []
    src = _file_lines[path]
    if not lines:
        return "\n".join(src[:80])
    out = []
    for ln in lines:
        out.extend(src[max(0, ln - 1 - pad):ln + pad])
    return "\n".join(out)


# ------------------------------------------------------------------ main
def main():
    wm = load_json(DATA / "works_meta.json.gz")
    meta, alias = wm["meta"], wm["alias"]
    fixes = load_yaml("metadata_fixes.yaml") or {}
    for wid, fx in (fixes.items() if isinstance(fixes, dict) else []):
        if wid in meta:
            for k, v in fx.items():
                if k == "authors":
                    meta[wid]["authors"] = [{"given": a.get("given", ""), "family": a.get("family", ""), "orcid": a.get("orcid"),
                                             "affiliation": None, "name": a.get("name")} for a in v]
                    meta[wid].pop("_arxiv_authors", None)
                else:
                    meta[wid][k] = v
            meta[wid]["metadata_fixed"] = sorted(fx)
    mentions = load_json(DATA / "mentions.json.gz")
    texts = load_json(DATA / "texts.json.gz")
    ay = load_json(DATA / "ay_resolution.json.gz") if (DATA / "ay_resolution.json.gz").exists() else {}
    overrides = load_yaml("ay_overrides.yaml") or {}
    for key, ch in (overrides.items() if isinstance(overrides, dict) else []):
        if isinstance(ch, dict):                       # curated decisions win over the automatic resolution
            prev = ay.get(key, {})
            ay[key] = {**prev, "status": "override", "choice": ch}
    own_fams = own_author_families()
    from common import own_author_given_initials
    own_init = own_author_given_initials()

    software = load_yaml("software.yaml")
    sw_map = collections.defaultdict(list)
    vendored = []
    for key, e in (software.items() if isinstance(software, dict) else []):
        wids = [work_ids(w, alias) for w in e.get("works") or []]
        for mod in e.get("modules") or []:
            sw_map[mod].append((e.get("label") or key, [w for w in wids if w]))
        if e.get("vendored"):
            vendored.append({"label": e.get("label"), "path": e["vendored"], "works": [w for w in wids if w]})
    algos = Matcher(load_yaml("algorithms.yaml"), "algorithm", alias, "algorithms.yaml")
    dsets = Matcher(load_yaml("datasets.yaml"), "data", alias, "datasets.yaml")
    concepts = Matcher(load_yaml("concepts.yaml"), "named", alias, "concepts.yaml")
    epon = Matcher(load_yaml("eponyms.yaml"), "named", alias, "eponyms.yaml")
    text_matchers = [dsets, concepts, epon]

    usage = collections.defaultdict(lambda: collections.defaultdict(lambda: {"kinds": set(), "lines": set(), "via": set()}))
    unresolved = []
    defects = []
    own_refs = collections.defaultdict(set)

    def add(wid, f, kind, lines, via):
        u = usage[wid][f]
        u["kinds"].add(kind)
        u["lines"].update(l for l in lines if l)
        if via:
            u["via"].add(via)

    # 1) identifiers written in the scripts (checked against any author named on the same line)
    named_on_line = collections.defaultdict(set)          # (file, line) -> author surnames cited there
    raw_named = collections.defaultdict(set)              # same, as written (lower case, accents stripped)
    ids_on_line = collections.Counter()                   # (file, line) -> identifiers written there
    for m in mentions["mentions"]:
        if m["kind"] == "ay":
            for ln in m["lines"]:
                named_on_line[(m["file"], ln)].add(norm_family(m["first"]))
                raw_named[(m["file"], ln)].add(strip_accents(m["first"]).lower())
        elif m["kind"] in ("arxiv", "doi"):
            for ln in m["lines"]:
                ids_on_line[(m["file"], ln)] += 1

    def is_own(wid):
        if meta.get(wid, {}).get("own"):
            return True
        au = meta.get(wid, {}).get("_arxiv_authors") or meta.get(wid, {}).get("authors") or []
        return any(norm_family(a.get("family") or "") in own_fams for a in au)

    def author_mismatch(wid, f, lines):
        """Only an unambiguous pairing is checked: one identifier and one cited surname on the same line."""
        if not lines or wid not in meta or is_own(wid):
            return None
        pairs = [(named_on_line.get((f, ln), set()), ids_on_line[(f, ln)]) for ln in lines]
        if not all(len(nm) == 1 and n_ids == 1 for nm, n_ids in pairs):
            return None
        named = set().union(*[nm for nm, _ in pairs])
        # the named author must precede the identifier in the same clause (no ';' between, within 160 characters)
        raw_id = str(meta[wid].get("arxiv") or "").split("v")[0]
        line_txt = strip_accents(window_text(f, lines[:1], pad=0)).lower()
        idpos = -1
        for cand in (raw_id, (meta[wid].get("doi") or "")):
            if cand and cand.lower() in line_txt:
                idpos = line_txt.index(cand.lower())
                break
        if idpos < 0:
            return None
        paired = False
        for n in raw_named.get((f, lines[0]), set()):
            for mt in re.finditer(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", line_txt[:idpos]):
                j = mt.start()
                if idpos - j < 160 and ";" not in line_txt[j:idpos]:
                    paired = True
        if not paired:
            return None
        au = meta[wid].get("_arxiv_authors") or meta[wid].get("authors") or []
        fams = {norm_family(a.get("family") or a.get("name") or "") for a in au}
        for n in named:
            if any(n == x or (len(n) >= 4 and (x.endswith(n) or n.endswith(x))) for x in fams if x):
                return None
        first = next((a.get("family") or a.get("name") for a in au if a.get("family") or a.get("name")), "?")
        return f"the identifier's paper is by {first} et al., but the comment names {', '.join(sorted(named))}"

    for m in mentions["mentions"]:
        k = m["kind"]
        if k in ("arxiv", "doi", "bibcode"):
            raw = m["key"]
            wid = alias.get(f"{k}:{raw.lower() if k == 'doi' else raw}")
            mm = author_mismatch(wid, m["file"], m["lines"]) if wid else None
            if wid and mm:
                defects.append({"file": m["file"], "lines": m["lines"], "identifier": f"{k}:{raw}", "problem": mm})
            elif wid:
                add(wid, m["file"], "cited", m["lines"], f"{k}:{raw}")
            else:
                defects.append({"file": m["file"], "lines": m["lines"], "identifier": f"{k}:{raw}",
                                "problem": "does not resolve at its registry (typo, truncated or invented)"})
        elif k == "import":
            for label, wids in sw_map.get(m["key"], []):
                for wid in wids:
                    add(wid, m["file"], "library", [], label)
        elif k == "call":
            for it in algos.items:
                if any(rx.search(m["key"]) for rx in it["calls"]):
                    for wid in it["works"]:
                        add(wid, m["file"], "algorithm", m["lines"], it["label"])
    # 2) author-year citations
    ay_files = collections.defaultdict(list)
    for m in mentions["mentions"]:
        if m["kind"] == "ay":
            ay_files[(norm_family(m["first"]), m["year"] + m["suffix"])].append(m)
    for (nf, ys), ms in ay_files.items():
        key = f"{nf}|{ys}"
        res = ay.get(key)
        if res is None:
            for m in ms:
                unresolved.append({"key": key, "file": m["file"], "lines": m["lines"], "raw": m["raw"], "status": "pending"})
            continue
        st = res["status"]
        if st == "own":
            for m in ms:
                own_refs[m["file"]].add(key)
            continue
        cands = res.get("candidates") or []
        for m in ms:
            idx = None
            if st == "override":
                ch = res.get("choice") if isinstance(res.get("choice"), dict) else {}
                spec = ch.get("files", {}).get(m["file"]) if isinstance(ch.get("files"), dict) else None
                if not isinstance(spec, dict) and ch.get("rules"):
                    near = window_text(m["file"], m["lines"])
                    spec = next((r for r in ch["rules"] if re.search(r["if"], near)), None)
                spec = spec if isinstance(spec, dict) else ch
                wid = None
                if not spec.get("unresolvable"):
                    if spec.get("classic"):
                        wid = work_ids({**spec["classic"], "classic": True}, alias)
                    else:
                        wid = work_ids({k: spec[k] for k in ("doi", "arxiv", "inspire") if spec.get(k)}, alias)
                if wid and wid in meta:
                    add(wid, m["file"], "cited", m["lines"], m["raw"] or key)
                else:
                    unresolved.append({"key": key, "file": m["file"], "lines": m["lines"], "raw": m["raw"],
                                       "status": "not_found" if spec.get("unresolvable") else "override-unresolvable",
                                       "note": spec.get("note") or ch.get("note"), "candidates": cands[:3]})
                continue
            idx = (res.get("assign") or {}).get(m["file"])
            if st in ("auto", "ambiguous") and idx is not None and idx < len(cands):
                c = cands[idx]
                wid = alias.get(f"doi:{c['doi'].lower()}") if c.get("doi") else alias.get(f"arxiv:{c.get('arxiv')}")
                if wid:
                    add(wid, m["file"], "cited", m["lines"], m["raw"] or key)
                    continue
            unresolved.append({"key": key, "file": m["file"], "lines": m["lines"], "raw": m["raw"], "status": st,
                               "candidates": cands[:3]})
    # 2b) bibliographies of the repository's LaTeX papers
    bib_unresolved = []
    bibp = DATA / "bib_resolution.json.gz"
    if bibp.exists():
        br = load_json(bibp)
        for e in br["entries"]:
            res = br["by_text"].get(e["text"])
            if not res or res.get("status") in ("own",):
                continue
            st = res.get("status")
            wid = None
            if st in ("crossref", "inspire", "id"):
                if res.get("doi"):
                    wid = alias.get(f"doi:{res['doi'].lower()}")
                if not wid and res.get("arxiv"):
                    wid = alias.get(f"arxiv:{res['arxiv']}")
                if not wid and res.get("inspire_id"):
                    wid = alias.get(f"inspire:{res['inspire_id']}")
            if st == "id" and res.get("check") is False:
                defects.append({"file": e["file"], "lines": [e["line"]], "identifier": (f"doi:{res['doi']}" if res.get("doi") else f"arxiv:{res.get('arxiv')}"),
                                "problem": "identifier in this bibliography entry points to a paper by a different first author or year"})
                continue
            if wid and wid in meta:
                add(wid, e["file"], "paper", [e["line"]], e["key"])
            elif st in ("not_found", "unparsed", "error"):
                bib_unresolved.append({"file": e["file"], "line": e["line"], "key": e["key"], "text": e["text"][:240], "status": st})
    # 2c) known author-list errors in the scripts' citation text (registry/known_defects.yaml)
    kd = [(re.compile(d["pattern"]), d["problem"]) for d in (load_yaml("known_defects.yaml") or [])]
    for f, t in texts.items():
        for ln, seg in t["segs"]:
            for rx, prob in kd:
                mt = rx.search(seg)
                if mt:
                    defects.append({"file": f, "lines": [ln + seg[:mt.start()].count("\n")],
                                    "identifier": mt.group(0)[:60], "problem": prob})
    # 3) named methods / concepts / data products in prose, and identifiers in code
    for f, t in texts.items():
        segs = t["segs"]
        if not segs:
            joined, starts, lines = "", [0], [0]
        else:
            starts, lines, parts, pos = [], [], [], 0
            for ln, s in segs:
                starts.append(pos)
                lines.append(ln)
                parts.append(s)
                pos += len(s) + 1
            joined = "\n".join(parts)
        idents = "\n".join(t["idents"]).lower()
        joined_lc = joined.lower()
        for mt in text_matchers:
            for it in mt.items:
                hit_lines = set()
                for rx, (ancs, ci) in it["pats"]:
                    if ancs is not None and not any(a in (joined_lc if ci else joined) for a in ancs):
                        continue
                    for mm in rx.finditer(joined):
                        j = bisect.bisect_right(starts, mm.start()) - 1          # segment holding the match
                        hit_lines.add(lines[j] + joined[starts[j]:mm.start()].count("\n"))
                ident_hit = any(rx.search(idents) for rx in it["ident"]) if it["ident"] else False
                if hit_lines or ident_hit:
                    for wid in it["works"]:
                        add(wid, f, it["kind"], sorted(hit_lines), it["label"])
    # own works cited by identifier (Zenodo DOIs etc.) are separated below via the people pass
    works = {wid: meta[wid] for wid in usage if wid in meta}
    people, orgs, own_works = build_people(works, own_fams, own_init)
    for wid in own_works:
        for f in usage.get(wid, {}):
            own_refs[f].add(wid)
    # serialise
    usage_out = {}
    for wid, per in usage.items():
        if wid in own_works or wid not in meta:
            continue
        usage_out[wid] = [{"file": f, "kinds": sorted(u["kinds"]), "lines": sorted(u["lines"])[:50],
                           "via": sorted(u["via"])[:6]} for f, u in sorted(per.items())]
    def norm_authors(au):
        out = []
        for a in au or []:
            if a.get("name") and not a.get("family"):
                out.append({"name": a["name"], "given": "", "family": "", "orcid": a.get("orcid")})
                continue
            full = f"{a.get('given') or ''} {a.get('family') or ''}".strip()
            if re.search(r"(?i)\b(collaboration|consortium|team)\b", full):
                out.append({"name": full, "given": "", "family": "", "orcid": None})
                continue
            if not re.search(r"[A-Za-zÀ-ÿ\u0400-\u04ff]{2}", full):
                continue
            g, f = clean_person(a)
            out.append({"given": g, "family": f, "orcid": a.get("orcid"), "affiliation": a.get("affiliation")})
        return out

    works_out = {}
    for wid, w in works.items():
        if wid in own_works:
            continue
        files = usage_out.get(wid, [])
        kinds = collections.Counter(k for u in files for k in u["kinds"])
        works_out[wid] = {**{k: v for k, v in w.items() if not k.startswith("_") and k != "abstract"},
                          "n_authors": len(w.get("_arxiv_authors") or w.get("authors") or []),
                          "all_authors": norm_authors(w.get("_arxiv_authors") if w.get("_arxiv_authors") and
                                                      len(w["_arxiv_authors"]) > len(w.get("authors") or []) else w.get("authors")),
                          "n_files": len(files), "kinds": dict(kinds)}
        works_out[wid].pop("authors", None)
    TOOL = {"library", "algorithm"}
    for p in people.values():
        p["works"] = [w for w in p["works"] if w in works_out]
        fs, fs_sci = set(), set()
        for w in p["works"]:
            for u in usage_out.get(w, []):
                fs.add(u["file"])
                if set(u["kinds"]) - TOOL:
                    fs_sci.add(u["file"])
        p["n_files"] = len(fs)
        p["n_files_research"] = len(fs_sci)
        p["collab_only"] = all(works_out[w]["n_authors"] > BIG_COLLAB for w in p["works"]) if p["works"] else False
    people = {k: v for k, v in people.items() if v["works"]}
    dump_json(works_out, DATA / "works.json.gz", gz=True)
    dump_json(usage_out, DATA / "usage.json.gz", gz=True)
    dump_json(people, DATA / "people.json.gz", gz=True)
    # citations resolved by review whose written author/year differs from the paper's (script error or parse artifact)
    misnamed = []
    for chk in wm.get("registry_checks", []):
        if chk.get("registry") != "ay_overrides.yaml" or "does not match" not in chk.get("problem", ""):
            continue
        key = chk["label"]
        ch = overrides.get(key) if isinstance(overrides, dict) else None
        res = ay.get(key, {})
        misnamed.append({"key": key, "problem": chk["problem"], "paper": chk.get("got"),
                         "note": (ch or {}).get("note"), "files": {f: l[:3] for f, l in list((res.get("files") or {}).items())[:4]},
                         "raws": (res.get("raws") or [])[:2]})
    dump_json({"unresolved": unresolved, "defects": defects, "bib_unresolved": bib_unresolved, "misnamed": misnamed,
               "orgs": orgs, "vendored": vendored,
               "own_refs": {f: sorted(v) for f, v in own_refs.items()},
               "registry_misses": algos.missing + dsets.missing + concepts.missing + epon.missing},
              DATA / "unresolved.json.gz", gz=True)
    n_scripts = len({u["file"] for us in usage_out.values() for u in us})
    print(f"works credited: {len(works_out)}; people: {len(people)} "
          f"({sum(1 for p in people.values() if p['collab_only'])} only via collaboration papers); "
          f"organisations: {len(orgs)}; scripts with at least one credit: {n_scripts}")
    print(f"unresolved author-year mentions: {len(unresolved)}; broken identifiers: {len(defects)}; "
          f"files citing own works: {len(own_refs)}; registry misses: {len(algos.missing + dsets.missing + concepts.missing + epon.missing)}")


if __name__ == "__main__":
    main()
