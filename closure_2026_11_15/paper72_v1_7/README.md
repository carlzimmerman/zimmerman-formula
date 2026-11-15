# PAPER72 version 1.7: the script that wrote its edits

2026-11-15. Not a lane: it grades nothing, freezes nothing and relabels nothing.

- `apply_v1_7.py` applies the version 1.7 edits to the paper's TeX source and to its audit script, in place, each edit
  anchored on an exact string of the version 1.6 source. It refuses to run on a source that is already version 1.7.
- `audit_block_v1_7.py.txt` is the block of audit entries it inserts: one entry per quoted number or word, each naming
  the committed file and the literal that must be found there.

What version 1.7 folds in, all of 2026-11-15 and after version 1.6 was deposited (DOI 10.5281/zenodo.24246863):

- the bounded closure statement BCS1, adopted by the owner as the record's closure statement ("Yes, adopt it") and put
  into this deposit on his go ("Yes, include it"); a statement of where the form stands, not a pass;
- the Gaia DR4 pre-data record DR4REC1, deposited as a record of its own (DOI 10.5281/zenodo.24248715), summarised
  in the paper's new Section 13.2; its archive stays in that record and is not copied into this version's supplement;
- the owner decisions of the day on Gaia DR4, and the decision sheet DR4DS1 they answer;
- CQB1, the check of the sealed wide-binary prediction under the adopted stiffness (MARGIN HOLDS, UNCHANGED on both
  footings), with its Lean certificate;
- DP8, the wiring of those decisions into the release-day path, checked on DR3 only;
- the scorecard's update of that morning (rows 15, 16, 26, 31 and 39; no word and no count changed).

It folds in no new graded data row and changes no lane's label, no scorecard word and no count.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
