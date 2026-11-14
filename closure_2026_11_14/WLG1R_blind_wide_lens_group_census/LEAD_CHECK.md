# WLG1R LEAD_CHECK: commit ids, the lead's re-run, and the comparison with WLG1

Written by the lead after `RESULT_BLIND.md` was committed (01fb260fda). Adopts nothing, relabels nothing, does not
edit the scorecard. kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed.

## Commits
Brief ec7fed6252 (alone, before the builder started); frozen criteria 8a730ebaa1 (alone); fetch script 5fb840fa9d;
main script f498060fc8 (before any graded run); outputs and result 01fb260fda. Every commit touches only this folder.

## Re-run
The lead re-ran `python3 -I -B wlg1r.py` from a copy with the repository's folders linked: `wlg1r.json` and
`wlg1r_per_lens.csv` byte-identical; same words printed.

## Blindness
The brief forbade WLG1's folder, the scorecard, paper drafts, XJ1R, EUC18, memory and git log outside this folder;
the builder reports opening none of them. WLG1's commit subjects carry no outcome word. No WLG1 number was sent to
the builder.

## Comparison with WLG1
- Words as frozen: WLG1 "WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, FRAGILE" (canonical) / "GROUPS TOO SLOW: ROW 40
  FAILS, FRAGILE" (alt). WLG1R "NOT EVALUABLE, BLIND" on both footings.
- The whole difference is the reading of KA-6 ("At least 90 % of W and C lenses have their own MER object ... with a
  photo-z row"). WLG1 pooled W and C: 520 / 565 = 0.920, pass. WLG1R graded each class: W 283 / 316 = 0.896, fail;
  C 0.952, pass. The frozen text allows both readings; neither build's reading is changed here. On the per-class
  reading WLG1's own data also fail KA-6 on W.
- Every graded number agrees: s 1.093 [1.061, 1.125] / 0.904 [0.878, 0.931]; r +0.023 [+0.008, +0.035]; the same
  brackets flip the words (no gas: SLOW on both; gas at ESZ1's 2-sigma limit: NO VERDICT / MIXED; sources at z_s 2:
  canonical short by +0.17). WLG1R's own twin TW-X0 (no cold share) bites.
- So the blind build confirms WLG1's arithmetic and its fragility, not its label. The canonical hit is NOT confirmed
  as a label and is not contradicted. It rests on one stacked gas value (ESZ1, 2.6 sigma, NO EXCESS DETECTED against
  controls) credited whole to every wide lens, with gas temperature unbracketed, and on sources beyond z_s about 3.8.
- What would decide row 40: per-lens group gas masses and certified source redshifts.
