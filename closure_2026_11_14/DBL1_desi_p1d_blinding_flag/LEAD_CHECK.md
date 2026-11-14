# DBL1 LEAD CHECK (2026-11-14): commit ids, what the lead checked, and how far the verdict goes

Written by the lead session after the lane's files were committed. A look-up lane: not blind, not graded, relabels
nothing, computes no forest number. The agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| SCOPE.md with the verdict rule (alone, before any look-up) | 3845638958 | 4a68b7b980 |
| dbl1_file.py, dbl1_file.out, FILE_FACTS.md | 193403b853 | 7ad76835ed |
| SOURCES.md, fetch_log.md | 347e16d8ef | f0d5095705 |
| READING.md | 2fac9c278d | 24ebbb29ee |

## What the lead checked

- **The file script** re-run from a copy in a new folder at the same depth: its printed output is byte-identical to
  the committed `dbl1_file.out`. That output and `FILE_FACTS.md` hold the two on-disk facts the verdict leans on: the figure data
  `fig_8a_qmle.txt` are built from this table (its error over one plus its ratio equals E_PK / PLYA in every row), and
  the table has no seed, no amplitude keyword and no second copy of the power.
- **The archive's md5**, computed by the lead: 33d7fc21bfd3d745ed71a0bbe80ca433. It is the value the lane reports for
  the paper's release record.
- **The web calls**, listed by script: 5 searches and 29 page fetches, all to arXiv, the release record, the survey's
  documentation and public code repositories. No query or address carries anything about this repository, its owner
  or the machine. Nothing was saved to disk from the web.
- The scope and the verdict rule were committed nine minutes before the other files. The committed files hold no home
  path.

## How far the verdict goes

- **Established on disk:** the table the gate reads is the table the paper plots, and the archive is the one the
  paper's release record lists (by md5, with the record's value read through the fetch tool).
- **Established from sources read through a page-fetch tool** (so PROVISIONAL in the house sense until read by eye):
  the header keyword is a date label written by the continuum-fitting code, which changes no value; the survey's
  first-release blinding for the Lyman-alpha forest was applied to correlation functions, a step a one-dimensional
  power spectrum never passes through; the paper describes no blinding of this measurement.
- **Not found:** a sentence in a primary source saying the released table is unblinded, and the code that wrote the
  release file with the extension name `P1D_BLIND`.
- The lane's word is UNBLINDED: ESTABLISHED under the second clause of its frozen rule. The lead's reading: the flag
  raised in ABS1's lead check is answered as far as a look-up can answer it. The gate's data are the published
  measurement, and nothing found says the published measurement carries a blinding. One multiplicative factor applied
  to the data would leave no trace in the file, so this is not a proof; it rests on the documented meaning of the
  keyword.
- Consequence for the record: no rescaling of any forest number is indicated, and ABS1's fit word can be read as it
  stands.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
