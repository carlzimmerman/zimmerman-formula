# How the citation index is built

The index answers one question: **whose published work do this repository's Python scripts use?** It is generated
by the scripts in [`build/`](build/) and checked by [`build/verify.py`](build/verify.py); nothing in it is typed by hand
except the curated dictionaries in [`build/registry/`](build/registry/).

## Scope

Every committed `.py` and `.ipynb` file (8,143 files at commit `27356de753`), and the
bibliographies of every committed `.tex` / `.bib` file, read as committed (never the working tree), except:

- `ai_slop/extended_research/`
- `ai_slop/TruthFlow/hermes_agent/`
- `ai_slop/HermesFlow/hermes_agent/`
- `citations/`

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
