#!/usr/bin/env python3
"""Stage 5b: write the two entry documents from data/summary.json — CITATIONS.md (repository root) and
citations/README.md (method, scope, how to rebuild) — so every number in them comes from the data."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CITE_DIR, DATA, EXCLUDE_PREFIXES, REPO  # noqa: E402


def main():
    s = json.loads((DATA / "summary.json").read_text(encoding="utf-8"))
    n = lambda k: f"{s[k]:,}"  # noqa: E731
    top_w = "\n".join(f"| {i} | [{c}](citations/works/{slug}.md) — {t} | {k:,} |"
                      for i, (c, t, k, slug) in enumerate(s["top_works"][:25], 1))
    top_p = "\n".join(f"| [{d}](citations/people/{pid}.md) | {k:,} | {nw} |" for d, pid, k, nw in s["top_people"][:40])
    top_t = ", ".join(f"[{d}](citations/people/{pid}.md) ({k:,})" for d, pid, k, nw in s.get("top_tools", [])[:10])
    cit = f"""# Citations

Everyone whose published work — equations, models, methods, data or software — is used by the Python scripts in
this repository, tied to the exact, verified reference and to every script and line that uses it.

**{n('n_people')} people** · **{n('n_works')} works** · credited in **{n('n_scripts_credit')} scripts** (of
{n('n_scripts_scanned')} scanned) and **{n('n_papers_credit')} LaTeX paper files** · built {s['date']} from commit `{s['commit']}`

| | |
|---|---|
| [People A–Z](citations/people/README.md) | everyone credited — {n('n_people_pages')} with their own page, {n('n_collab_only')} as authors of large collaboration papers |
| [Works](citations/WORKS.md) | every verified reference, most-used first; each work's page lists every script and line |
| [REFERENCES.bib](citations/REFERENCES.bib) | BibTeX for all {n('n_works')} works |
| [By folder](citations/BY_FOLDER.md) | which works each top-level folder uses |
| [Could not verify](citations/UNVERIFIED.md) | {n('n_defects')} broken identifiers, {n('n_notfound_distinct')} script citations that match no publication, {n('n_ambiguous_distinct')} ambiguous ones, {n('n_bib_unresolved_distinct')} unmatched paper-bibliography entries |
| [Corrections](citations/CORRECTIONS.md) | what happened to each of the previous index's 182 names |
| [How it is built](citations/README.md) | scope, evidence, verification, and the one command that rebuilds and checks it |

## How a person gets credited

A script credits a work when it

1. **cites** it — an author–year reference, arXiv id, DOI or ADS bibcode in a comment, docstring or string;
2. **names** its equation, method or model — "Tully–Fisher", "NFW", "Gibbons–Hawking temperature", "AQUAL", "Nelder–Mead";
3. **uses its data** — SPARC, Planck 2018, DESI DR2, Gaia DR3, Pantheon+, eRASS1, CODATA, PDG …;
4. **imports its software** — NumPy, SciPy, SymPy, mpmath, Astropy, CLASS, CAMB …; or
5. **calls a routine that implements its algorithm** — `solve_ivp` (Dormand & Prince 1980), `brentq` (Brent 1973),
   `quad` (QUADPACK), `spearmanr` (Spearman 1904) …;

and the repository's LaTeX papers credit every work in their bibliographies (matched entry by entry).

Every work is checked against its publisher (Crossref / DataCite), arXiv or INSPIRE-HEP record before anyone is
credited; the people credited are that record's authors. References that cannot be verified are never credited —
they are listed in [Could not verify](citations/UNVERIFIED.md) with the script and line, because some of this
repository's scripts were machine-written and a few of their references are garbled or invented.

## Most-used works

| # | work | scripts |
|---:|---|---:|
{top_w}

[All {n('n_works')} works →](citations/WORKS.md)

## Most-credited people for the research itself

Counted over the files that cite their work, name their method or use their data (software and numerical-method
credits excluded; authors of large collaboration papers are listed A–Z instead).

| person | files | works |
|---|---:|---:|
{top_p}

Software and numerical methods are credited too — most widely: {top_t} …

[All {n('n_people')} people →](citations/people/README.md)
"""
    (CITE_DIR.parent / "CITATIONS.md").write_text(cit, encoding="utf-8")
    excl = "\n".join(f"- `{p}`" for p in EXCLUDE_PREFIXES)
    readme = f"""# How the citation index is built

The index answers one question: **whose published work do this repository's Python scripts use?** It is generated
by the scripts in [`build/`](build/) and checked by [`build/verify.py`](build/verify.py); nothing in it is typed by hand
except the curated dictionaries in [`build/registry/`](build/registry/).

## Scope

Every committed `.py` and `.ipynb` file ({n('n_scripts_scanned')} files at commit `{s['commit']}`), and the
bibliographies of every committed `.tex` / `.bib` file, read as committed (never the working tree), except:

{excl}

`ai_slop/extended_research/` is excluded at the author's request (biology material). The vendored Hermes Agent
code is third-party software: it is credited as software (Nous Research), not scanned for references. Only
comments, docstrings and string literals are read for references, so a variable name never creates a citation.
Personal communications are never indexed.

## Evidence (per script, with line numbers)

| kind | what counts | where it is defined |
|---|---|---|
| cited | author–year reference, arXiv id, DOI or bibcode written in the script | read from the script |
| named method/model | an eponymous equation, method, profile, theory or theorem | `registry/eponyms.yaml`, `registry/concepts.yaml` |
| data used | a named data release, catalogue, survey, ephemeris or constants compilation | `registry/datasets.yaml` |
| library imported | a scientific library the script imports | `registry/software.yaml` |
| algorithm via library call | a numerical/statistical routine that implements someone's method | `registry/algorithms.yaml` |
| cited in a paper | an entry in the bibliography of one of the repository's LaTeX papers (`.tex` / `.bib`) | `build/resolve_bib.py` |

## Verification

* **Identifiers** (DOI, arXiv id, INSPIRE record) are fetched from Crossref / DataCite, arXiv and INSPIRE-HEP; the
  metadata shown (authors, title, journal, year) is the authority's, not typed by hand. Registry entries carry the
  expected first author and year, and a mismatch stops the build.
* **Author–year citations** are resolved by searching INSPIRE-HEP, Crossref and arXiv for the first author within
  ±1 year, then scoring the candidates on the co-authors named in the script, any journal/volume/page or identifier
  written next to it, and the topic words around it. A candidate is accepted only if it clears a score floor and
  beats the runner-up by a margin; the choice is made per script, because the same "Lelli 2016" can mean different
  papers in different scripts. Hand decisions go in `registry/ay_overrides.yaml`.
* **Works with no DOI** (pre-DOI books and memoirs, technical reports, software without a DOI) are recorded from
  their standard bibliographic data with a stable link and are marked as not machine-checkable.
* **Garbled publisher metadata** is corrected in `registry/metadata_fixes.yaml`; the build fails on any that remains.

## People

The people are the authors of the verified works. Records of the same person are merged by ORCID when the
publisher supplies one, otherwise by family name plus compatible given names and initials; different people with
the same surname (Li, Fisher, Brout, Rubin, Klein …) stay separate. Authors of papers with more than 40 authors
(Planck, DESI, Gaia, LIGO–Virgo–KAGRA …) are listed A–Z and link to that paper rather than having a page each.
The repository's own author (read from `CITATION.cff`) is not part of the index.

## Rebuild and check

```bash
python3 citations/build/run_all.py          # extract → resolve → fetch → index → render → verify
python3 citations/build/verify.py --online  # also re-fetch a sample of DOIs from Crossref
```

API responses are cached in `citations/.cache/` (not committed); a rebuild with a warm cache is offline. A fresh
build takes about an hour, almost all of it spent resolving author–year citations.

## Known limits

* A named method is credited when the script's prose or identifiers name it; code that implements a method without
  naming it is not detected.
* An author–year citation whose script gives no co-author, journal or topic clue can remain ambiguous; those are
  listed in [UNVERIFIED.md](UNVERIFIED.md) with their candidates rather than guessed.
* Person merging without ORCIDs can occasionally split one person into two entries or, more rarely, merge two people
  who share a surname and initials.
"""
    (CITE_DIR / "README.md").write_text(readme, encoding="utf-8")
    print("wrote CITATIONS.md and citations/README.md")


if __name__ == "__main__":
    main()
