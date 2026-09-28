#!/usr/bin/env python3
"""Stage 1 of the citation-index build: pull every piece of attribution evidence out of the scanned scripts.

Evidence kinds written to data/mentions.json.gz (one record per file x kind x key, with line numbers):
  arxiv    arXiv identifier (new or old style) in a comment/docstring/string
  doi      DOI in a comment/docstring/string
  bibcode  ADS bibcode
  ay       author-year citation ("Lelli, McGaugh & Schombert 2016", "Chae et al. (2023)", "Milgrom+83")
  import   top-level module imported (AST; regex fallback)
  call     library function called, fully qualified through import aliases (e.g. scipy.integrate.solve_ivp)
  text     lower-cased prose (comments/docstrings/strings) and identifiers kept per file for the later
           dictionary match of named methods, datasets and collaborations (stored separately, not in mentions)

Only comments, docstrings and string literals are read for literature references, so code identifiers never
produce a "citation". Run from anywhere:  python3 citations/build/extract.py
"""
from __future__ import annotations

import ast
import collections
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, dump_json, head_commit, norm_family, prose_segments, read_source, tracked_files  # noqa: E402

# ------------------------------------------------------------------ identifier patterns
ARXIV_NEW = re.compile(r"(?<![\w./])(?:arXiv\s*[:/]?\s*|arxiv\.org/(?:abs|pdf)/)?"
                       r"((?:0[7-9]|1\d|2[0-6])(?:0[1-9]|1[0-2])\.\d{4,5})(v\d+)?(?![\d])", re.I)
ARXIV_OLD = re.compile(r"(?<![\w-])((?:astro-ph|gr-qc|hep-th|hep-ph|hep-ex|hep-lat|math-ph|nucl-th|nucl-ex|quant-ph|"
                       r"cond-mat(?:\.[a-z-]+)?|physics(?:\.[a-z-]+)?|math(?:\.[A-Z]{2})?|nlin(?:\.[A-Z]{2})?|q-bio)"
                       r"/\d{7})(v\d+)?(?!\d)")
DOI = re.compile(r"(?<![\w/])(10\.\d{4,9}/[^\s\"'<>,;\]}`]+)", re.I)
BIBCODE = re.compile(r"(?<![\w.])((?:1[6-9]\d\d|20[0-2]\d)[A-Za-z&][A-Za-z&.]{4}[\d.]{4}[A-Za-z.\d][\d.]{4}[A-Z])(?![\w.])")

# ------------------------------------------------------------------ author-year grammar
_UP = "A-ZÀ-ÖØ-ÞĀĂĄĆĈĊČĎĐĒĖĘĚĜĞĠĢĤĪĮİĴĶĹĻĽŁŃŅŇŌŐŒŔŖŘŚŜŞŠŢŤŪŮŰŲŴŶŸŹŻŽ"
_LO = "a-zß-öø-ÿāăąćĉċčďđēėęěĝğġģĥīįıĵķĺļľłńņňōőœŕŗřśŝşšţťūůűųŵŷźżž"
PART = r"(?:(?:[dD]e|[vV]an|von|[dD]er|den|[lL]e|[lL]a|[dD]i|[dD]el|[dD]a|dos|du|ten|ter|'t|[dD]es|[dD]ella|[dD]al|[eE]l)\s+)"
SUR = (rf"(?:{PART}{{0,3}})(?:[{_UP}](?:[{_LO}]|['’][{_UP}{_LO}])[{_LO}'’]*(?:[{_UP}][{_LO}]+)?"
       rf"(?:[-–][{_UP}][{_LO}'’]+(?:[{_UP}][{_LO}]+)?)*)")
INIT = rf"(?:(?:[{_UP}]\.\s?-?){{1,3}}\s*)"            # optional initials before a surname: "S. S. McGaugh"
AUTH = rf"(?:{INIT}?{SUR})"
ETAL = r"(?:\s*,?\s+et\.?\s*al\.?|\s*\+\s?)"
YEAR = r"(1[6-9]\d\d|20[0-2]\d)((?:[a-h](?![\w]))(?:\s*,\s*[a-h](?![\w]))*)?"
SEP = r"\s*[,(\[]?\s*"

AY_PATTERNS = [
    # A, B, C & D 2016  /  A, B and C (2016)
    ("list_and", re.compile(rf"({AUTH}(?:\s*,\s*{AUTH}){{1,6}}\s*,?\s*(?:&|and)\s*{AUTH}){SEP}{YEAR}(?![\d])")),
    # A & B 2016 / A and B (2016)
    ("two", re.compile(rf"({AUTH}\s*(?:&|and)\s*{AUTH}){ETAL}?{SEP}{YEAR}(?![\d])")),
    # A et al. 2016 / A+2016 / A+ 16
    ("etal", re.compile(rf"({AUTH}){ETAL}{SEP}{YEAR}(?![\d])")),
    ("plus2", re.compile(rf"({SUR})\+\s?(\d\d)([a-h])?(?![\w])")),
    # A, B, C 2016 (comma list, no conjunction)
    ("list", re.compile(rf"({AUTH}(?:\s*,\s*{AUTH}){{2,6}}){SEP}{YEAR}(?![\d])")),
    # A (2016) / A [2016]
    ("paren", re.compile(rf"({AUTH})\s*[(\[]\s*{YEAR}\s*[)\],;:]")),
    # A-B 2016 (hyphen pair; could be one double-barrelled name)
    # A 2016 / A, 2016 (weak: kept only if the surname is seen elsewhere in a strong form)
    ("bare", re.compile(rf"({AUTH}),?\s+{YEAR}(?![\d\w])")),
]
STRONG = {"list_and", "two", "etal", "plus2", "list", "paren"}

# capitalised words that are not surnames (sentence words, months, labels, instruments...)
NOT_NAMES = set("""
A An The This That These Those Its It Our Their His Her We You They I In On At Of From Since By To For Until Before After
During Circa Around About Above Below Between Through Under Over With Without Within Per Via Versus Vs And Or But If Then
Else When While Where Here There Now Note Notes Table Tables Figure Figures Fig Figs Eq Eqs Equation Equations Section
Sections Sec Secs Paper Papers Version Versions Release Releases Data Cycle Cycles Run Runs Lane Lanes Gate Gates Stage
Stages Step Steps Amendment Amendments Wave Waves Appendix Chapter Chap Part Parts Model Models Case Cases Test Tests Round
Rounds Phase Phases Batch Session Sessions Commit Commits Item Items Hunt Door Doors Route Routes Front Fronts Arm Arms
Branch Branches Level Levels Tier Tiers Grade Year Years Month Months Day Days Week Weeks Today Yesterday Tomorrow Date Dates
January February March April May June July August September October November December Jan Feb Mar Apr Jun Jul Aug Sep
Sept Oct Nov Dec Spring Summer Fall Autumn Winter Monday Tuesday Wednesday Thursday Friday Saturday Sunday Updated Created
Modified Copyright Python Numpy Scipy Sympy Julia Fortran Mathematica Matlab Lean Released Published Submitted Accepted
Draft Revised Retracted Withdrawn Deposit Deposited Registered Preregistered Frozen Final Initial Original Previous Next
Last First Second Third Fourth Fifth New Old Early Late Mid Total Mean Median Max Min Sum Average Number Count Rate Ratio
Value Values Result Results Output Outputs Input Inputs File Files Line Lines Page Pages Vol Volume Issue No Nr Num
Planck Gaia DESI Euclid SPARC JWST HST LIGO Virgo KAGRA LISA Rubin LSST SDSS BOSS KiDS DES HSC ACT SPT WMAP COBE Pantheon Union
SH0ES CODATA PDG IAU NASA ESA ESO CERN NIST JPL ALMA MUSE MaNGA SAMI WALLABY MeerKAT ALFALFA THINGS LITTLE SKA Chandra XMM
eROSITA eRASS Swift TESS Hipparcos HIPPARCOS APOGEE LAMOST GALAH RAVE Horizons INPOP EPM DE MICROSCOPE
Messenger Juno Voyager Pioneer Apollo Lunar Moon Sun Earth Mars Jupiter Saturn Mercury Venus Uranus Neptune Pluto
Solar Galaxy Galactic Milky Way Local Group Cluster Clusters Bullet Coma Virgo Fornax Perseus Abell
Figure Tab Theorem Lemma Proof Corollary Definition Proposition Conjecture Claim Remark Example Exercise Problem Problems
Question Questions Answer Answers Summary Conclusion Conclusions Introduction Abstract Methods Method Discussion Status
Verdict Verdicts Standing Record Records Ledger Book Books Edition Editions Chapter Journal Journals Preprint Preprints
Zenodo GitHub Git Arxiv ArXiv Google Scholar Wikipedia Science Nature Physics Astronomy Astrophysics Cosmology Universe
Monte Carlo Gaussian Bayesian Newtonian Keplerian Einsteinian Lagrangian Hamiltonian Riemannian Euclidean Cartesian
Figures Plot Plots Graph Graphs Sample Samples Catalog Catalogue Catalogs Survey Surveys Mission Missions Observatory
Telescope Instrument Collaboration Collaborations Consortium Team Group Groups Project Projects Program Programme
Workshop Conference Proceedings Meeting Talk Lecture Lectures Course Class School University Institute Department
Also Only Just Even Still Yet Already Ever Never Always Often Sometimes Usually Some Many Most More Less Few All Any Each
Every Both Either Neither Other Another Such Same Different Various Several Certain Main Key Core Base Full Partial Half
Double Single Triple Standard Classic Classical Modern Recent Current Future Past Present Previous Upcoming Expected
Observed Measured Predicted Derived Computed Estimated Fitted Adopted Assumed Used Given Using Based See Cf Compare Ref Refs
Reference References Source Sources Via Updated Update Fix Fixed Bug Added Removed Changed Todo TODO FIXME XXX NB PS
Earth-Moon Earth-Sun Solar-System Milky-Way Local-Group Standard-Model Monte-Carlo First-Principles Work-Order
Content-Type User-Agent License-Identifier Parity-Odd Odd-Parity Fine-Tuning No-Slip Non-Gaussianity Helvetica-Bold
Apple-Accelerate Phi-Psi Psi-Phi
""".split())

# names that are both a person and a later mission/instrument: an "author" only while the person was publishing
PERSON_MAX_YEAR = {"Hubble": 1953, "Kepler": 1630, "Planck": 1947, "Fermi": 1954, "Herschel": 1871, "Spitzer": 1997,
                   "Einstein": 1955, "Newton": 1727, "Galileo": 1642, "Galilei": 1642, "Cassini": 1712, "Tycho": 1601,
                   "Brahe": 1601, "Chandrasekhar": 1995, "Compton": 1962, "Webb": 1992, "Roman": 1990, "Rubin": 2016,
                   "Euclid": 300, "Gaia": 0, "Hipparcos": 0, "Copernicus": 1543, "Huygens": 1695}

OWN_TAGS = re.compile(r"priv(?:ate|\.)?\s*comm|personal\s+comm", re.I)


def _split_authors(chunk: str) -> list[str]:
    chunk = re.sub(r"\s+et\.?\s*al\.?", "", chunk)
    chunk = chunk.replace("+", "")
    parts = re.split(r"\s*(?:,|&|\band\b)\s*", chunk)
    out = []
    for p in parts:
        p = re.sub(rf"^{INIT}", "", p.strip())
        if p:
            out.append(p.strip())
    return out


def _years(year: str, suf: str | None) -> list[tuple[str, str]]:
    if not suf:
        return [(year, "")]
    letters = re.findall(r"[a-h]", suf)
    return [(year, s) for s in letters] or [(year, "")]


def author_year_hits(text: str):
    """Yield (kind, authors[list], year, suffix, span, etal_flag) with longest-match-wins masking."""
    taken = [False] * (len(text) + 1)
    for kind, rx in AY_PATTERNS:
        for m in rx.finditer(text):
            s, e = m.span()
            if any(taken[s:e]):
                continue
            authors = _split_authors(m.group(1))
            if kind == "plus2":
                yy = int(m.group(2))
                year, suf = (f"20{yy:02d}" if yy <= 26 else f"19{yy:02d}"), (m.group(3) or "")
            else:
                year, suf = m.group(2), (m.group(3) or "")
            if not authors:
                continue
            first = authors[0]
            if first in NOT_NAMES or first.split()[-1] in NOT_NAMES or len(norm_family(first)) < 2:
                continue
            last = first.split()[-1]
            if last in PERSON_MAX_YEAR and int(year) > PERSON_MAX_YEAR[last]:
                continue
            etal = bool(re.search(r"et\.?\s*al|\+", m.group(0)))
            for y, sf in _years(year, suf):
                yield kind, authors, y, sf, (s, e), etal
            for i in range(s, e):
                taken[i] = True


CALL_MODULES = ("scipy", "numpy", "emcee", "sympy", "mpmath", "astropy", "sklearn", "statsmodels", "camb", "classy",
                "healpy", "dynesty", "corner", "galpy", "colossus", "pyccl", "lmfit", "networkx", "numba", "torch", "jax")


def import_map(tree: ast.AST) -> tuple[dict[str, str], set[str]]:
    """alias -> fully qualified name; plus set of top-level modules imported."""
    alias, tops = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                tops.add(a.name.split(".")[0])
                alias[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            tops.add(node.module.split(".")[0])
            for a in node.names:
                if a.name != "*":
                    alias[a.asname or a.name] = f"{node.module}.{a.name}"
    return alias, tops


def dotted(node: ast.AST) -> str | None:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def calls(tree: ast.AST, alias: dict[str, str]):
    """Yield (qualified_name, method_kwarg_or_None, line) for calls into scientific libraries."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        d = dotted(node.func)
        if not d:
            continue
        head, _, rest = d.partition(".")
        if head not in alias:
            continue
        q = alias[head] + ("." + rest if rest else "")
        if not q.startswith(CALL_MODULES):
            continue
        method = None
        for kw in node.keywords:
            if kw.arg in ("method", "algorithm", "kind", "sampler") and isinstance(kw.value, ast.Constant) \
                    and isinstance(kw.value.value, str):
                method = kw.value.value
        yield q, method, node.lineno


IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def scan_file(path: str):
    code, extra = read_source(path)
    if code is None:
        return None
    segs = prose_segments(code) + extra
    rec = collections.defaultdict(lambda: collections.defaultdict(list))   # kind -> key -> [lines]
    raw = {}                                                                 # (kind,key) -> sample text
    ctx = collections.defaultdict(list)                                      # (kind,key) -> context windows
    prose_parts, pc = [], False
    for ln, s in segs:
        if OWN_TAGS.search(s):
            pc = True
            continue          # personal-communication text is never indexed (standing directive)
        prose_parts.append((ln, s))
        for m in ARXIV_NEW.finditer(s):
            pre = s[max(0, m.start() - 12):m.start()].lower()
            if "arxiv" in m.group(0).lower() or "arxiv" in pre or "abs/" in pre:
                rec["arxiv"][m.group(1)].append(ln)
        for m in ARXIV_OLD.finditer(s):
            rec["arxiv"][m.group(1)].append(ln)
        for m in DOI.finditer(s):
            d = m.group(1).rstrip(".):]").rstrip(".")
            rec["doi"][d.lower()].append(ln)
        for m in BIBCODE.finditer(s):
            rec["bibcode"][m.group(1)].append(ln)
        for kind, authors, year, suf, (a, b), etal in author_year_hits(s):
            key = "|".join([norm_family(authors[0]), year + suf])
            full = "|".join([authors[0], year + suf, ";".join(authors[1:]), "etal" if etal else "", kind])
            rec["ay"][full].append(ln)
            if (("ay", full) not in raw):
                raw[("ay", full)] = s[a:b].strip()[:200]
            if len(ctx[("ay", full)]) < 4:
                ctx[("ay", full)].append(re.sub(r"\s+", " ", s[max(0, a - 220):min(len(s), b + 220)]).strip())
    imports, call_hits, idents = set(), [], set()
    try:
        tree = ast.parse(code)
        alias, imports = import_map(tree)
        for q, method, ln in calls(tree, alias):
            call_hits.append((q, method, ln))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                idents.add(node.name)
            elif isinstance(node, ast.Name):
                idents.add(node.id)
            elif isinstance(node, ast.Attribute):
                idents.add(node.attr)
            elif isinstance(node, ast.arg):
                idents.add(node.arg)
    except Exception:
        for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_]\w*)", code, re.M):
            imports.add(m.group(1))
        idents = set(IDENT.findall(code))
    for mod in imports:
        rec["import"][mod].append(0)
    for q, method, ln in call_hits:
        rec["call"][q + (f"[{method}]" if method else "")].append(ln)
    return {"rec": rec, "raw": raw, "ctx": ctx, "segs": prose_parts, "idents": sorted(idents),
            "pc": pc, "nlines": code.count("\n") + 1}


def not_citation_filter():
    """Author-year look-alikes that are not citations (registry/not_citations.yaml)."""
    p = Path(__file__).resolve().parent / "registry" / "not_citations.yaml"
    if not p.exists():
        return lambda path, first, key: False
    import yaml
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    storms = set(d.get("storm_names") or [])
    paths = tuple(d.get("storm_paths") or ())
    keys = set((d.get("keys") or {}).keys())
    return lambda path, first, key: key in keys or (first.split()[-1] in storms and path.startswith(paths))


def main() -> None:
    t0 = time.time()
    skip = not_citation_filter()
    files = tracked_files()
    mentions = []            # flat records
    texts = {}               # path -> {"prose": str, "idents": [...]}
    strong_surnames = collections.Counter()
    pc_files = []
    per_file = {}
    for i, path in enumerate(files):
        r = scan_file(path)
        if r is None:
            continue
        per_file[path] = r
        if r["pc"]:
            pc_files.append(path)
        for full in r["rec"].get("ay", {}):
            first, _, _, _, kind = full.split("|")
            if kind in STRONG:
                strong_surnames[norm_family(first)] += 1
    for path, r in per_file.items():
        for kind, keys in r["rec"].items():
            for key, lines in keys.items():
                if kind == "ay":
                    first, yr, co, etal, how = key.split("|")
                    if how == "bare" and strong_surnames[norm_family(first)] == 0:
                        continue          # weak "Word 2016" with a word never seen as an author elsewhere
                    if skip(path, first, f"{norm_family(first)}|{yr}"):
                        continue          # a hurricane name or other look-alike (registry/not_citations.yaml)
                    mentions.append({"file": path, "kind": "ay", "first": first, "year": yr[:4], "suffix": yr[4:],
                                     "coauthors": [c for c in co.split(";") if c], "etal": bool(etal), "how": how,
                                     "lines": sorted(set(lines)), "raw": r["raw"].get((kind, key), ""),
                                     "ctx": r["ctx"].get((kind, key), [])})
                else:
                    mentions.append({"file": path, "kind": kind, "key": key, "lines": sorted(set(l for l in lines if l))})
        texts[path] = {"segs": r["segs"], "idents": r["idents"], "nlines": r["nlines"]}
    meta = {"head": head_commit(), "n_files": len(per_file), "n_mentions": len(mentions),
            "personal_communication_segments_skipped_in": sorted(pc_files), "seconds": round(time.time() - t0, 1)}
    dump_json({"meta": meta, "mentions": mentions}, DATA / "mentions.json.gz", gz=True)
    dump_json(texts, DATA / "texts.json.gz", gz=True)
    kinds = collections.Counter(m["kind"] for m in mentions)
    print(f"scanned {len(per_file)} files in {meta['seconds']} s; mentions by kind: {dict(kinds)}")
    print(f"personal-communication segments skipped in {len(pc_files)} file(s)")


if __name__ == "__main__":
    main()
