# PAPER72 version 1.6: the script that wrote its edits, and the scorecard as version 1.5 saw it

2026-11-15. Not a lane: it grades nothing, freezes nothing and relabels nothing.

- `apply_v1_6.py` applies the version 1.6 edits to the paper's TeX source and to its audit script, in place, each edit
  anchored on an exact string of the version 1.5 source. It refuses to run on a source that is already version 1.6.
  `audit_block_v1_6.py.txt` is the block of audit entries it inserts: one entry per quoted number or word, each naming
  the committed file and the literal that must be found there.
- `CJ1_SCORECARD_at_PAPER72_v1_5.md` is CJ1's scorecard as it stood when version 1.5 was deposited: the file
  `closure_2026_11_13/CJ1_candidate_completion/SCORECARD.md` at commit 1f4546aa80 (its thirteenth update, 2026-11-14
  16:15 EST; version 1.5's paper commit is from 16:25 EST), byte for byte, sha256
  5018f7352e14b84bbf44b97e36d3e5345c95dac8148c11eb141f5c8dd3c551f0. The paper's audit reads it for the two sentences of
  Section 9 that describe the scorecard of earlier versions (the list of fails at version 1.3, and row 24's placement at
  version 1.4), so that those quotations do not drift when the scorecard is updated. The live scorecard has since been
  updated three more times and by two notes; version 1.6's counts are the live ones.

What version 1.6 folds in: the blind lane XJ1R, XJ1's second build, BJ1's flux-level run, WLJ2, GAS2, ABS1, DBL1, the
lanes behind the scorecard's twelfth to sixteenth updates (EUC17R, EUC18, EUC20, EUC20R, EUC21, EUC21R, OTA1, RRL2,
RRL3R, WLG1, WLG1R), and Lean certificates for the algebra of those lanes. It changes no lane's label.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
