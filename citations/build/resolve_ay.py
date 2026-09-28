#!/usr/bin/env python3
"""Stage 2a: resolve author-year citations ("Chae 2023", "Lelli, McGaugh & Schombert 2016") to real publications.

For every distinct (first-author, year, suffix) key found by extract.py:
  1. candidates come from identifiers written next to the citation (arXiv id / DOI in the same comment),
     from a Crossref reference-string match when a journal/volume/page follows the year, from INSPIRE-HEP
     (first-author search), from Crossref (author + year window + topic words) and, for recent years, arXiv;
  2. a candidate is ELIGIBLE only if its first author's family name matches and its year is within one year;
  3. eligible candidates are scored on cited co-authors (present / absent), journal-volume-page agreement,
     identifiers in the context, and topic overlap between the citing comment and the paper's title/abstract;
  4. the best candidate is accepted only if it clears a score floor AND beats the runner-up by a margin.
     Otherwise the key is recorded as AMBIGUOUS (candidates listed) or NOT FOUND (possible invented citation).

Curated decisions in registry/ay_overrides.yaml always win over the automatic choice.
Output: data/ay_resolution.json
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apis  # noqa: E402
from common import DATA, REGISTRY, dump_json, load_json, norm_family, own_author_families, scrub_text, strip_accents  # noqa: E402
from extract import ARXIV_NEW, ARXIV_OLD, DOI  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

STOPWORDS = set("""a about above after again against all also am an and any are as at be because been before being below
between both but by can could did do does doing down during each few for from further had has have having he her here
hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once
only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves
then there these they this those through to too under until up very was we were what when where which while who whom
why will with would you your yours yourself yourselves et al eq eqs equation fig figure table section sec paper using
used use value values data result results model models test tests gives given see also via per vs versus note notes
our new one two three first second third fit fitted fits from into onto upon within without between across among
here there where whether which while cited cite cites reference references ref refs ibid op cit arxiv doi http https www
org abs pdf com html pp vol no volume page pages journal apj mnras aj pasp prl prd jcap aa phys rev lett astron astrophys
nature science true false none print return def self import numpy scipy np sp float int str len range list dict set lane
gate stage step verdict pass fail kill killed record committed commit script scripts run runs sigma framework law laws
""".split())
YEAR_WORDS = re.compile(r"\b(1[6-9]\d\d|20[0-2]\d)[a-h]?\b")
JREF = re.compile(r"(?:ApJ[LS]?|AJ|MNRAS|A\s?&\s?A|PASP|PASJ|Nature(?:\s+Astronomy)?|Science|PRL|PRD|PRX|PRE|PRB|PRA|"
                  r"Phys\.?\s?Rev\.?\s?(?:Lett\.?|[A-EX])?|JCAP|JHEP|CQG|Class\.?\s?Quant\.?\s?Grav\.?|GRG|Gen\.?\s?Rel\.?"
                  r"(?:\s?Grav\.?)?|Living\s?Rev\.?\s?Rel(?:ativ(?:ity)?)?\.?|LRR|ARA\s?&\s?A|Rev\.?\s?Mod\.?\s?Phys\.?|RMP|"
                  r"Phys\.?\s?Rep(?:t|orts)?\.?|Phys\.?\s?Lett\.?\s?[AB]|PLB|Nucl\.?\s?Phys\.?\s?B|NPB|EPJ\s?C|Eur\.?\s?Phys\.?"
                  r"\s?J\.?\s?C|Universe|Galaxies|Icarus|Celest\.?\s?Mech\.?|Ann\.?\s?Phys\.?|Annals|Proc\.?\s?Roy\.?\s?Soc\.?|"
                  r"Phil\.?\s?Trans\.?|Z\.?\s?Phys\.?|JMP|J\.?\s?Math\.?\s?Phys\.?|CMP|Commun\.?\s?Math\.?\s?Phys\.?|AN|"
                  r"Astron\.?\s?Nachr\.?|PTEP|Prog\.?\s?Theor\.?\s?Phys\.?|Symmetry|Entropy|EPL|Found\.?\s?Phys\.?|IJMPD?|"
                  r"Int\.?\s?J\.?\s?Mod\.?\s?Phys\.?\s?[AD]?|J\.?\s?Atmos\.?\s?Sci\.?|QJRMS|Mon\.?\s?Wea(?:ther)?\.?\s?Rev\.?|"
                  r"Q\.?\s?J\.?\s?R\.?\s?Meteorol\.?\s?Soc\.?|J\.?\s?Fluid\s?Mech\.?|JFM|Biometrika|JASA|Ann\.?\s?Stat\.?|"
                  r"J\.?\s?Stat\.?|Nat\.?\s?Astron\.?|Nat\.?\s?Phys\.?|Sci\.?\s?Adv\.?|PNAS|ApSS|Ap\s?&\s?SS|RNAAS|OJAp|"
                  r"Astron\.?\s?J\.?|Astrophys\.?\s?J\.?(?:\s?Lett\.?|\s?Suppl\.?)?)\s*[,.]?\s*(\d{1,4})\s*[,:]?\s*"
                  r"(?:\(\d{4}\)\s*)?(?:no\.\s*\d+\s*,?\s*)?([A-Z]?\d{1,6}|L\d+)")


ACRONYMS = {
    "bimond": "bimetric mond", "qumond": "quasi-linear quasilinear mond", "aqual": "aquadratic lagrangian nonlinear",
    "raqual": "relativistic aquadratic", "teves": "tensor vector scalar", "aest": "aether scalar tensor",
    "rar": "radial acceleration relation", "btfr": "baryonic tully fisher relation", "tfr": "tully fisher relation",
    "efe": "external field effect", "mond": "modified newtonian dynamics mond", "nfw": "navarro frenk white halo",
    "lcdm": "cold dark matter lambda", "cdm": "cold dark matter", "bao": "baryon acoustic oscillation",
    "cmb": "cosmic microwave background", "sne": "supernovae", "snia": "type supernovae", "wb": "wide binary",
    "wbs": "wide binaries", "udg": "ultra diffuse galaxy", "udgs": "ultra diffuse galaxies", "tdg": "tidal dwarf",
    "dsph": "dwarf spheroidal", "dsphs": "dwarf spheroidal", "ufd": "ultra faint dwarf", "smhm": "stellar halo mass",
    "shmr": "stellar halo mass relation", "wl": "weak lensing", "ggl": "galaxy galaxy lensing", "xcop": "x-cop xmm cluster",
    "ppn": "post newtonian parametrized", "llr": "lunar laser ranging", "gw": "gravitational wave", "bbn": "nucleosynthesis",
    "mi": "modified inertia", "des": "dark energy survey", "kids": "kilo degree survey", "hsc": "hyper suprime cam",
    "sparc": "sparc spitzer rotation curves", "things": "things nearby galaxy survey", "rc": "rotation curve",
    "rcs": "rotation curves", "ism": "interstellar medium", "imf": "initial mass function", "hi": "neutral hydrogen",
}


def tokens(text: str) -> list[str]:
    t = strip_accents(text or "").lower()
    t = re.sub(r"\b(" + "|".join(ACRONYMS) + r")\b", lambda m: m.group(1) + " " + ACRONYMS[m.group(1)], t)
    t = re.sub(r"https?://\S+", " ", t)
    words = re.findall(r"[a-z][a-z\-]{2,}", t)
    out = []
    for w in words:
        w = w.strip("-")
        if len(w) < 4 or w in STOPWORDS:
            continue
        if w.endswith("ies"):
            w = w[:-3] + "y"
        elif w.endswith("s") and not w.endswith("ss") and len(w) > 4:
            w = w[:-1]
        out.append(w)
    return out


class KeyGroup:
    def __init__(self, first_norm, year, suffix):
        self.first_norm, self.year, self.suffix = first_norm, int(year), suffix
        self.forms = collections.Counter()
        self.co = collections.Counter()
        self.co_forms = {}
        self.etal = 0
        self.n = 0
        self.how = collections.Counter()
        self.files = collections.defaultdict(set)
        self.per_file = {}
        self.ctx = []
        self.raws = []

    @property
    def key(self):
        return f"{self.first_norm}|{self.year}{self.suffix}"

    @property
    def display(self):
        f = self.forms.most_common(1)[0][0]
        acc = [x for x, _ in self.forms.most_common() if strip_accents(x) != x]
        return acc[0] if acc and strip_accents(acc[0]) == strip_accents(f) else f


def load_groups():
    d = load_json(DATA / "mentions.json.gz")
    groups = {}
    for m in d["mentions"]:
        if m["kind"] != "ay":
            continue
        k = (norm_family(m["first"]), m["year"], m["suffix"])
        g = groups.get(k) or groups.setdefault(k, KeyGroup(*k))
        g.forms[m["first"]] += 1
        for c in m["coauthors"]:
            nc = norm_family(c)
            if nc and nc != k[0]:
                g.co[nc] += 1
                g.co_forms.setdefault(nc, c)
        g.etal += 1 if m["etal"] else 0
        g.n += 1
        g.how[m["how"]] += 1
        g.files[m["file"]].update(m["lines"])
        pf = g.per_file.setdefault(m["file"], {"ctx": [], "co": set(), "etal": False, "raws": []})
        pf["co"].update(n for n in (norm_family(c) for c in m["coauthors"]) if n and n != k[0])
        pf["etal"] = pf["etal"] or m["etal"]
        for c in m["ctx"]:
            if c not in pf["ctx"] and len(pf["ctx"]) < 6:
                pf["ctx"].append(c)
        if m["raw"] and m["raw"] not in pf["raws"]:
            pf["raws"].append(m["raw"])
        for c in m["ctx"]:
            if c not in g.ctx and len(g.ctx) < 14:
                g.ctx.append(c)
        if m["raw"] and m["raw"] not in g.raws and len(g.raws) < 14:
            g.raws.append(m["raw"])
    return groups


def idf_table(groups):
    df = collections.Counter()
    for g in groups.values():
        df.update(set(tokens(" ".join(g.ctx))))
    n = max(1, len(groups))
    return {w: math.log((n + 1) / (c + 0.5)) for w, c in df.items()}


def context_ids(g):
    arx, dois = set(), set()
    for c in g.ctx:
        for m in ARXIV_NEW.finditer(c):
            pre = c[max(0, m.start() - 12):m.start()].lower()
            if "arxiv" in m.group(0).lower() or "arxiv" in pre:
                arx.add(m.group(1))
        for m in ARXIV_OLD.finditer(c):
            arx.add(m.group(1))
        for m in DOI.finditer(c):
            dois.add(m.group(1).rstrip(".):]").lower())
    return arx, dois


def journal_refs(g):
    refs = []
    for c in g.ctx:
        for m in JREF.finditer(c):
            refs.append((m.group(0), m.group(1), m.group(2)))
    return refs


def family_ok(cand_family: str, key_norm: str) -> bool:
    f = norm_family(cand_family)
    if not f:
        return False
    if f == key_norm:
        return True
    if min(len(f), len(key_norm)) >= 4 and (f.endswith(key_norm) or key_norm.endswith(f)
                                             or f.startswith(key_norm) or key_norm.startswith(f)):
        return True
    # transliteration variants (Zeldovich/Zel'dovich, Ubler/Uebler) handled by norm_family; allow 1 edit for len>=6
    if len(f) >= 6 and len(key_norm) >= 6 and abs(len(f) - len(key_norm)) <= 1:
        return _lev1(f, key_norm)
    return False


def _lev1(a, b):
    if a == b:
        return True
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) <= 1
    if len(a) > len(b):
        a, b = b, a
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == a:
            return True
    return False


def gather(g):
    """Collect candidate records from every source for one key."""
    cands = []
    first = strip_accents(g.display)
    arx, dois = context_ids(g)
    if arx:
        for aid, r in apis.arxiv_ids(sorted(arx)).items():
            r["_ctx_id"] = True
            cands.append(r)
    for d in sorted(dois)[:6]:
        r = apis.crossref_doi(d) if not d.startswith("10.5281/") else apis.datacite_doi(d)
        if r:
            r["_ctx_id"] = True
            cands.append(r)
    for text, vol, page in journal_refs(g)[:3]:
        for r in apis.crossref_search(bibliographic=f"{first} {g.year} {text}", rows=5):
            r["_jref"] = (vol, page)
            cands.append(r)
    # INSPIRE: first-author search in a +-1 year window (with a co-author when one is cited)
    fa = first if " " not in first else f'"{first}"'
    q = f"fa {fa} and date {g.year - 1}->{g.year + 1}"
    top_co = [c for c, _ in g.co.most_common(1)]
    if top_co:
        cands += apis.inspire_search(q + f" and a {strip_accents(g.co_forms[top_co[0]])}", size=25)
    cands += apis.inspire_search(q, size=50)
    # Crossref: author + year window, ranked by topic words from the citing comments
    topic = " ".join(sorted(set(tokens(" ".join(g.ctx))), key=lambda w: -IDF.get(w, 0))[:12])
    author_q = " ".join([first] + [strip_accents(g.co_forms[c]) for c, _ in g.co.most_common(2)])
    cands += apis.crossref_search(bibliographic=topic or None, author=author_q, year=g.year, rows=25)
    if not any(family_ok(apis.first_family(c), g.first_norm) and c.get("year") and abs(c["year"] - g.year) <= 1
               for c in cands):
        cands += apis.crossref_search(bibliographic=f"{first} {g.year} {topic}", rows=25, year=g.year)
        if g.year >= 1992:
            last = strip_accents(g.display).split()[-1].replace("'", "")
            cands += apis.arxiv_search(f'au:{last} AND submittedDate:[{g.year - 1}01010000 TO {g.year + 1}12312359]',
                                       max_results=40)
    return cands


def merge_key(r):
    if r.get("doi"):
        return "doi:" + r["doi"].lower()
    if r.get("arxiv"):
        return "arxiv:" + r["arxiv"]
    return "t:" + re.sub(r"[^a-z0-9]", "", (r.get("title") or "").lower())[:80] + str(r.get("year"))


def merge_cands(cands):
    """Collapse duplicates (same DOI / arXiv id, or arXiv record whose DOI matches a Crossref record)."""
    by = {}
    arx2doi = {}
    for r in cands:
        if r.get("arxiv") and r.get("doi"):
            arx2doi[r["arxiv"]] = r["doi"].lower()
    for r in cands:
        k = merge_key(r)
        if k.startswith("arxiv:") and r["arxiv"] in arx2doi:
            k = "doi:" + arx2doi[r["arxiv"]]
        if k in by:
            base = by[k]
            for f in ("arxiv", "abstract", "citations", "inspire_id", "texkey", "container", "volume", "page"):
                if not base.get(f) and r.get(f):
                    base[f] = r[f]
            base["_ctx_id"] = base.get("_ctx_id") or r.get("_ctx_id")
            base["_jref"] = base.get("_jref") or r.get("_jref")
            base.setdefault("_sources", set()).add(r["source"])
            if r["source"] == "crossref" and base["source"] != "crossref":
                # prefer the publisher's own metadata as the base record
                keep = {f: base.get(f) for f in ("arxiv", "abstract", "inspire_id", "texkey", "_ctx_id", "_jref")}
                srcs = base["_sources"]
                base.clear()
                base.update(r)
                for f, v in keep.items():
                    if v and not base.get(f):
                        base[f] = v
                base["_sources"] = srcs
        else:
            r = dict(r)
            r["_sources"] = {r["source"]}
            by[k] = r
    return list(by.values())


ERRATUM = re.compile(r"^\s*(erratum|corrigendum|publisher'?s note|retraction|addendum|correction to|reply to|"
                     r"comment on|response to|author correction|editorial)", re.I)


def score(g, r, ctx_tokens):
    if ERRATUM.search(r.get("title") or "") and not re.search(r"errat|corrig|comment|reply", " ".join(g.ctx), re.I):
        return None
    fam = apis.first_family(r)
    if not family_ok(fam, g.first_norm):
        return None
    if not r.get("year"):
        return None
    dy = abs(int(r["year"]) - g.year)
    if dy > 1:
        return None
    s = 3.0 if dy == 0 else 0.8
    why = [f"year{'=' if dy == 0 else '±1'}"]
    fams = [norm_family(a.get("family") or a.get("name") or "") for a in r.get("authors") or []]
    cofams = set(fams[1:])
    cited = {c for c, n in g.co.items()}
    if cited:
        hit = {c for c in cited if any(c == f or (len(c) >= 4 and (f.endswith(c) or c.endswith(f))) for f in cofams)}
        miss = cited - hit
        s += 2.5 * len(hit) - 1.6 * len(miss)
        if hit:
            why.append(f"coauthors+{len(hit)}")
        if miss:
            why.append(f"coauthors-{len(miss)}")
    n_auth = len(fams)
    if g.etal >= max(1, g.n // 2) and n_auth <= 1:
        s -= 1.2
        why.append("etal-but-solo")
    if g.etal == 0 and not g.co and n_auth >= 3:
        s -= 0.6
        why.append("solo-cited-but-multi")
    if r.get("_ctx_id"):
        s += 6
        why.append("id-in-context")
    if r.get("_jref"):
        vol, page = r["_jref"]
        rv = str(r.get("volume") or "")
        rp = str(r.get("page") or "").split("-")[0]
        if vol and rv == vol:
            s += 2.5
            why.append("volume")
            if page and rp and (rp.lstrip("0") == page.lstrip("L0") or rp == page):
                s += 2.5
                why.append("page")
    title_t = set(tokens(r.get("title") or ""))
    abs_t = set(tokens(r.get("abstract") or "")) - title_t
    ov = sum(IDF.get(w, 0) for w in title_t & ctx_tokens) + 0.3 * sum(IDF.get(w, 0) for w in abs_t & ctx_tokens)
    topic = min(6.0, ov / 3.0)
    s += topic
    if topic > 0.3:
        why.append(f"topic{topic:.1f}")
    c = r.get("citations") or 0
    s += 0.3 * math.log10(1 + c)
    return s, why


def resolve(g, overrides):
    if g.key in overrides:
        return {"status": "override", "choice": overrides[g.key], "why": ["registry/ay_overrides.yaml"]}
    cands = merge_cands(gather(g))
    ctx_tokens = set(tokens(" ".join(g.ctx + g.raws)))
    scored = []
    for r in cands:
        sc = score(g, r, ctx_tokens)
        if sc:
            scored.append((sc[0], sc[1], r))
    scored.sort(key=lambda x: -x[0])
    scored = scored[:8]
    slim = [{"score": round(s, 2), "why": w, **{k: r.get(k) for k in ("doi", "arxiv", "title", "year", "container",
                                                                          "volume", "page", "citations", "inspire_id",
                                                                          "source")},
             "authors": [(a.get("family") or a.get("name") or "") for a in (r.get("authors") or [])][:6],
             "n_authors": len(r.get("authors") or [])} for s, w, r in scored]
    if not scored:
        return {"status": "not_found", "candidates": [], "n_raw_candidates": len(cands)}
    best = scored[0]
    second = scored[1][0] if len(scored) > 1 else None
    margin = best[0] - second if second is not None else 99
    strong = best[0] >= 6.0 or ("id-in-context" in best[1]) or ("page" in best[1])
    if (best[0] >= 4.0 and margin >= 1.2) or (strong and margin >= 0.6):
        status = "auto"
    else:
        status = "ambiguous"
    assign = assign_files(g, scored[:8], status)
    return {"status": status, "candidates": slim, "margin": round(margin, 2), "assign": assign}


def mention_score(g, pf, key_score, r):
    """Score one candidate against ONE file's own citing text (its co-authors, journal ref, ids, topic)."""
    ms = 0.35 * key_score
    if r.get("year") and int(r["year"]) != g.year:
        ms -= 2.0
    fams = [norm_family(a.get("family") or a.get("name") or "") for a in r.get("authors") or []]
    cofams = set(fams[1:])
    for c in pf["co"]:
        ok = any(c == f or (len(c) >= 4 and (f.endswith(c) or c.endswith(f))) for f in cofams)
        ms += 2.5 if ok else -1.6
    text = " ".join(pf["ctx"] + pf["raws"])
    arx, dois = set(), set()
    for m in ARXIV_NEW.finditer(text):
        arx.add(m.group(1))
    for m in ARXIV_OLD.finditer(text):
        arx.add(m.group(1))
    for m in DOI.finditer(text):
        dois.add(m.group(1).rstrip(".):]").lower())
    if (r.get("arxiv") and r["arxiv"] in arx) or (r.get("doi") and r["doi"] in dois):
        ms += 8
    for m in JREF.finditer(text):
        vol, page = m.group(1), m.group(2)
        if str(r.get("volume") or "") == vol:
            ms += 2.5
            rp = str(r.get("page") or "").split("-")[0]
            if rp and (rp.lstrip("0") == page.lstrip("L0") or rp == page):
                ms += 2.5
    ctx_t = set(tokens(text))
    title_t = set(tokens(r.get("title") or ""))
    abs_t = set(tokens(r.get("abstract") or "")) - title_t
    ov = sum(IDF.get(w, 0) for w in title_t & ctx_t) + 0.3 * sum(IDF.get(w, 0) for w in abs_t & ctx_t)
    ms += min(6.0, ov / 3.0)
    return ms


def assign_files(g, scored, key_status):
    """Pick, per citing file, which of the key's candidates that file means (keys can be mixed across files)."""
    out = {}
    for f, pf in g.per_file.items():
        sc = sorted(((mention_score(g, pf, s, r), i) for i, (s, w, r) in enumerate(scored)), reverse=True)
        best, bi = sc[0]
        second = sc[1][0] if len(sc) > 1 else -99
        if bi == 0 and key_status == "auto":
            out[f] = 0
        elif best - second >= 1.5 and best >= 3.0:
            out[f] = bi
        elif key_status == "auto" and bi != 0 and best - second < 1.5:
            out[f] = 0 if sc[0][1] == 0 or any(i == 0 and best - m < 1.5 for m, i in sc[:2]) else None
        else:
            out[f] = None
    return out


def load_overrides():
    p = REGISTRY / "ay_overrides.yaml"
    if not p.exists() or yaml is None:
        return {}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return {str(k): v for k, v in data.items()}


IDF = {}


def main(argv):
    global IDF
    groups = load_groups()
    IDF = idf_table(groups)
    overrides = load_overrides()
    own = own_author_families()
    missing = "--missing" in argv
    only = set(a for a in argv[1:] if not a.startswith("--"))
    pth0 = DATA / "ay_resolution.json.gz"
    have = set(load_json(pth0)) if (missing and pth0.exists()) else set()
    if missing:
        only = {g.key for g in groups.values()} - have
    todo = [g for g in groups.values() if g.key in only] if (only or missing) else list(groups.values())
    todo.sort(key=lambda g: -len(g.files))
    out = {}
    prev = {}
    pth = DATA / "ay_resolution.json.gz"
    if pth.exists() and (only or missing):
        prev = load_json(pth)

    def work(g):
        if g.first_norm in own:
            return g, {"status": "own", "candidates": []}
        try:
            return g, resolve(g, overrides)
        except Exception as e:  # keep going; record the failure
            return g, {"status": "error", "error": repr(e), "candidates": []}

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for i, (g, res) in enumerate(ex.map(work, todo), 1):
            res.update({"display": g.display, "year": g.year, "suffix": g.suffix, "n_files": len(g.files),
                        "coauthors": [g.co_forms[c] for c, _ in g.co.most_common(6)], "etal": g.etal, "n": g.n,
                        "how": dict(g.how), "raws": [scrub_text(r) for r in g.raws[:6]],
                        "files": {f: sorted(l) for f, l in sorted(g.files.items())}})
            out[g.key] = res
            if i % 100 == 0:
                c = collections.Counter(v["status"] for v in out.values())
                print(f"  {i}/{len(todo)} {dict(c)}", flush=True)
    if prev:
        prev.update(out)
        out = prev
    for v in out.values():                     # script context is used for scoring only; never stored
        v.pop("ctx", None)
        v["raws"] = [scrub_text(r) for r in v.get("raws") or []]
    dump_json(out, pth, gz=True)
    c = collections.Counter(v["status"] for v in out.values())
    print("status:", dict(c), "| API requests that failed permanently:", apis.DEGRADED["count"])


if __name__ == "__main__":
    main(sys.argv)
