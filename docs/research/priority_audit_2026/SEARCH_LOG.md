# Search scope and reproducibility notes

Review cutoff: 2026-09-09; retrieval sessions: 2026-09-09/10. This is a human-readable reconstruction of the principal search routes, not a claim to preserve every search-engine response or every exploratory query. Search rankings and live pages may change.

## Sources and strategies

1. **Repository-first chronology:** inspect status and recent history; follow earliest commits containing exact claims, not only present-day filenames. Compare root content, subsequent density correction, interpolation corrections, filtered action drafts and constraint-method citations.
2. **Exact/lexical discovery:** equation variants, author names, titles, unusual numerical coefficients and operator combinations.
3. **Independent semantic discovery:** SciSpace queries, then primary-paper verification. Duplicate index records and incorrect dates were not counted as independent papers.
4. **Citation/version tracing:** follow earlier arXiv versions and antecedents rather than assuming journal dates or new repository uploads date the original discovery.

Main discovery interfaces: web search; arXiv primary records and HTML/PDFs; journal/publisher pages; SciSpace; author-uploaded manuscripts; PhilPapers/PhilArchive, SSRN, Zenodo and viXra records. No exhaustive authenticated subscription citation-database export was performed.

## Exact representative queries executed by the lead

```text
"Zimmerman" "MOND" "2026" gravity -site:github.com
"Zimmerman" "rho" "a0" dark energy -site:github.com
"Carl Zimmerman" gravity -site:github.com
"Carl P. Zimmerman" MOND
"zimmerman-formula" -site:github.com
"Zimmerman" "gravity" "10.5281"
"9.36" "MOND" "2026"
"MOND" "2y" "lambda" "quadrupole" 2026
"MOND" "central tidal identity"
"MOND" "filtered" "2/9"
"MOND" "32 pi" "Lambda"
"MOND" "155" "four-form"
"MOND" "gravitational seesaw" "Planck"
"MOND" "half" "vacuum density"
"The Solar-Galactic External-field Boundary Problem"
"MOND" "5.79"
"MOND" "5.789"
"MOND" "5.7888"
"acceleration" "sqrt(8" "Zimmerman"
"MOND" "sqrt{8" "3"
"MOND" "32π/3"
"MOND" "sqrt(32" "3"
"acceleration scale" "5.79"
MOND epicyclic Lambert W acceleration scale inverse 2026
"MOND" "spectrometer" "orbital"
"MOND" "7" "96" "rotation"
"MOND" "cross-radius"
```

Name-only searches returned many irrelevant namesakes. A missing result is therefore weak negative evidence, not a verified citation count of zero. Formula fragments are poorly indexed and require notation-translated searches. Additional workstream-specific searches and exact primary references are recorded in the scale and relativistic appendices.

The targeted `5.79` search returned equation numbers, galaxy-fit table entries and unrelated quantities, as well as Carl's own repo. Those are not matches to a MOND normalization. The exact-symbol queries and common-normalization primary-paper comparisons were used to distinguish such false positives. No external exact fixed-Z match was authenticated.

SciSpace discovery questions included:

> Which papers published before September 10, 2026 propose history-dependent modified inertia, memory effects in dwarf galaxy MOND dynamics, or a cubic separation onset in Gaia wide-binary gravity tests, and which original papers first proposed these predictions?

The other SciSpace route sought papers first posted between March 9 and September 9 relating the MOND scale to vacuum/dark-energy density, the fixed-half relation, and citations to Carl Zimmerman. Its results included older works and duplicate DOI/arXiv records; all required independent checking.

## Primary-source checks by the lead

- Elit: SSRN exact-title/abstract result and author-mirrored manuscript; equations 8.5–8.13; PhilPapers version history. Text search for `Zimmerman` found no match in the available extracted manuscript. Version inconsistency and historical-PDF retrieval gaps retained in the report.
- Kovacs: viXra abstract/version record and PDF. Distinguish manuscript March date, citation metadata April 1 and submission history April 2. `Zimmerman` search of extracted PDF found no match.
- Saad–Ting: arXiv abstract and submission history, not treated as a result on Carl's specific theory.
- STF Cosmology: live author page including its status corrections, not treated as an authenticated exact-normalization predecessor.
- Distinctive repo expressions: PAPER4 central-tidal/frequency formulas and P17 compared as written, not inferred from generic MOND keywords.

## Access failures and bounded exclusions

| Target | Result | Consequence |
|---|---|---|
| SSRN direct Elit record | HTTP 403 on direct open; indexed author abstract available | Abstract supports architectural lead; not full historical-content authentication. |
| PhilArchive Elit v1/v2 | Cache miss / HTTP 403 | Cannot establish every current equation existed in first upload. |
| Several Carl Zenodo records/DOI routes | Failed access; network retry also timed out | Local deposit claims are not promoted to independently verified public priority. |
| `lightfluid.org/predictions.html` | Cache miss | Search snippet only; excluded from substantive priority verdict. |
| `MrJevrem/entropic-superfluid-gravity` | Live page unavailable | No inference from indexed wording alone. |

Other source-specific qualifications are in the appendices. Inaccessible is not nonexistent; uncited is not copied; a preprint is not automatically peer reviewed.

## Local commands and review verification

The timeline appendix records the exact commit hashes and path-sensitive history searches. Lead inspection included:

```bash
git status --short
git log -5 --format='%h %aI %s'
git remote -v
sed -n '1,110p' real_research/NOVELTY.md
sed -n '1,220p' qwen_claude_field_theory/papers_2026/PAPER4_filtered_action_2026.tex
git diff --check -- docs/research/priority_audit_2026
```

New audit documents were created using `apply_patch`. Initial `ls` checks returned exit 1 because the audit directory had not yet been created; these were discovery checks, not failed physics tests. No new computational physics script was created and no existing closure script was run for this literature task. No commit, push, public deposit or external author message was made.

Final document check: each of the ten new Markdown files was checked with `git diff --no-index --check /dev/null <file>`. Each returned exit 1 for the new-file difference and **no whitespace diagnostics**. This is recorded explicitly, not misreported as a zero-exit physics test. All ten files were present and nonempty. The prose/notation review corrected one primary-paper hyperlink in the new report; no mathematical tokens in the original research files were changed. Follow-up scope from Carl is captured in `CORE_AND_LIVE_CLAIMS.md` and the three `LIVE_*.md` appendices.

## Stop rule and unresolved work

This review stops after the main high-value claim families have been compared via independent routes. It does not keep expanding indefinitely to every speculative gravity webpage. The most useful remaining checks are exact archived public release dates for Carl's narrow results, first-version retrieval for the closest screened-action paper, and a source-level comparison if the user supplies a specific suspected match.
