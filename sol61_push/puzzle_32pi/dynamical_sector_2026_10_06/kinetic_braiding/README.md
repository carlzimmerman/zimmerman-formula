# Evidence handoff

Read [REPORT.md](REPORT.md) for exact hypotheses and unresolved implications; [REVIEW_ROLLING_KESSENCE.md](REVIEW_ROLLING_KESSENCE.md) is the independent current root-baseline review. No32π selector or full galaxy theory was found. The positive result is a classical covariant logarithmic vacuum map with full4D cosmological scalar constraint health; its minimally sourced leading force has the wrong MOND radial exponent.

`runs/main_a`: completed,71 assertions. `runs/control_mixing`, `control_canonical`, `control_mond`: expected failures, each at its designated false assertion. Allfour manifests passed the computation-audit validator. `preflight.json` is exploratory supplemental output, not the standard evidence record.

Reproduce with a fresh directory name:

    python3 run_checks.py --tag main_fresh
    python3 run_checks.py --tag control_fresh --control mond

Run from any directory; runner root resolves to this repository. The fixed runner interpreter is Python3.13, while mathematical execution uses `/usr/bin/python3` (3.9.6) and SymPy1.14.0. Manifests record actual executables, inputs, results, limits and exit status. `input_snapshot.json` supplements binary/file hashes and actual concurrent HEAD; it does not override manifests. Root-base metadata is not a substitute for exact input hashes.

Primary source versions: [Bernardo2101.00965v2](https://arxiv.org/pdf/2101.00965v2), [Kobayashi et al.1105.5723v2](https://arxiv.org/pdf/1105.5723v2). The latter uses equation numbering56–64 in this version. `sources.json` pins PDF and `pdftotext -layout` hashes. Fullcached PDFs/text are ignored locally; restore exact sources and match hashes before source-audit reruns. `make_provenance.py` creates a new current input snapshot/contract; do not run it to rewrite provenance for historical runs.
