# Signed-dot implementation amendment, before cached rerun

The initial bounded attempt remains under its original resource caps. Its
inner delta verification reads mass[lower/upper] from NpzFile four times per
coordinate:893048 whole-member decompressions. Inspection of installed NumPy
NpzFile.__getitem__ confirms it opens and reads the member afresh on every
access. This is an avoidable input-loading cost, not new physics arithmetic.

The cached implementation loads both arrays once. Arithmetic, criteria,
coverage, tolerances, controls and physical coefficients remain identical.
A fresh bounded output directory preserves the initial attempt and its outcome.
No native simulation or follower is stopped or changed. The initial attempt
will finish or hit its predeclared bound; this amendment does not restart it.
