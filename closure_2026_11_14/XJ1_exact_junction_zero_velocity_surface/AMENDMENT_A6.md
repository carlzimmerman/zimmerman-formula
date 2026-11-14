# XJ1 AMENDMENT A6 (2026-11-14, written 13:47 EST by the clock): how far the integer can go before rotation curves are cut

Post hoc: written after both forest passes of build B were graded and RESULT.md was written. It adds one reported item.
It changes no case, gate, known answer, twin, bracket, label or lane word.

**Why.** RESULT.md section 6 says the integer k is a choice and that nothing was run for k = 4 and beyond. The forest
number falls as the settled radius shrinks in this lane (the first, second and third caustic read 3.94 / 5.37, 1.21 /
1.65 and 0.51 / 0.69), so the forest does not bound k from above; today's rotation curves do, because a caustic that
lies inside a galaxy's last measured point cuts its curve. This item finds where that happens.

**The added item (reported; no label; no forest run).**
- `xj1_shells45.py`: this lane's `xj1_shells.py` with the passage count carried to 5 (two more series columns, R_4 and
  R_5, defined as R_2 and R_3 are), all 12 of FLD1's masses on both footings, output in `shells45/`. Known answer: the
  first eight series columns equal this lane's stored shell runs (`shells/`) to 1e-9 relative, in all 24 runs.
- `xj1_contain45.py`: `xj1_contain.py` with R_4 and R_5 in place of R_2 and R_3: for each of SPARC's 175 galaxies
  the last measured radius against R_4 and R_5 at z = 0 and its own M_b (mass-to-light 0.5; brackets 0.3 and 0.8); the
  number beyond, the largest ratio and its galaxy.
- Not run: the forest, lensing or matter-level chains for k = 4 or 5. Nothing is claimed about them.

**Hand estimate (before any number of this item):** R_4 / R_fold about 0.44 and R_5 / R_fold about 0.38 at z = 0 (the
worst SPARC galaxy sits at 0.41 R_fold). No galaxy beyond R_4 at mass-to-light 0.5 (60 %); 1 to 5 galaxies beyond R_5
(70 %).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
