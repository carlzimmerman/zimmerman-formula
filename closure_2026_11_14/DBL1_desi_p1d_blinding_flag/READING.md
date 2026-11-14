# DBL1 reading

## Verdict: UNBLINDED: ESTABLISHED (by the second clause of the frozen rule)

The frozen rule (SCOPE.md) allows ESTABLISHED when "the keyword's meaning is documented and consistent with that, and
no file fact contradicts it". That is the clause met here. No primary source says in one sentence "the released table
is unblinded"; the call rests on the following.

1. **The keyword's meaning is documented in code (SEEN IN TEXT, S4).** In the continuum fitter that makes the deltas
   for this measurement (QSOnic), `BLINDING = "desi_y1"` is a label set only from the date of the newest observation
   in the quasar catalogue (before 2022-08-01 gives "desi_y1"). Its only effects are to rename the delta column to
   `DELTA_BLIND` and to write the `BLINDING` header keyword. The estimator (lyspeq) reads `DELTA` and `DELTA_BLIND`
   the same way (S5). The file's spelling `desi_y1`, with an underscore, is QSOnic's spelling.
2. **The DESI DR1 Lyman-alpha blinding acted on correlation functions, not on deltas (SEEN IN TEXT, S7).** The DR1
   BAO paper blinded "the measured correlation functions" with an additive BAO-shift template that picca applied
   whenever it computed a correlation function. A one-dimensional power spectrum made from the deltas does not go
   through that step. The public DR1 deltas themselves keep the name `DELTA_BLIND` with the keyword documented as
   "none" (S6), so the "BLIND" in a name is a label, not a state.
3. **The archive is the paper's published data release, and the table is what the paper plots.** The archive's
   checksum equals that of Zenodo record 10.5281/zenodo.16943723, the paper's "Supplementary material" (S3), which
   the paper names as holding "All data points shown in the figures" (S1). The Figure 8 data are built from exactly
   this table's PLYA and E_PK (fractional errors equal to 3e-17 in all 195 rows; FILE_FACTS.md).
4. **The paper describes no blinding of the P1D values and no unblinding step** (PROVISIONAL negative, S1); it calls
   the measurement "cosmologically blind" in the sense that it precedes cosmological inference. The companion FFT
   paper uses "blind" only for systematics tests (S2).
5. **No file fact contradicts it.** No column, keyword or extension holds a second version of the power, a seed, an
   amplitude or a date (FILE_FACTS.md).

## What is missing (said plainly)

- The code that wrote this release file (its `P1D_BLIND` extension name, its `BLINDING` keyword, `PSMOOTH`,
  `E_SYST`, `SYSTEMATICS`) was not found. lyspeq names its own output `P1D`; picca's `postproc_pk1d.py` sets no such
  name. So that the keyword in this file is the label carried over from the deltas is inferred from the matching
  string, not read in the writer's code.
- The QSOnic source read is the current master branch, not a tagged DR1 version.
- That the paper describes no value-level blinding, and that QSOnic changes no value by the label, are negatives
  reported by the fetch tool after reading the whole text; they are PROVISIONAL.
- Item 3 (an independent number) was not done: the paper's text gives the eBOSS excess only as a 5 to 15 per cent
  range, no single power value at a stated z and k was seen, and the eBOSS table is not on disk. Nothing in this lane
  tests the table's overall amplitude against an outside measurement. Figure 9's DESI-to-eBOSS excess (about 13 per
  cent at the lowest k, falling to about 0 to 1 per cent near k = 0.01 s/km) sits inside the paper's quoted range,
  but it is a figure file of the same release, not an independent number.
- Verdict probability against the frozen hand estimate (UNBLINDED: ESTABLISHED 0.55): the call is made, but it rests
  on documented meaning plus the release's identity, not on a sentence that names the table unblinded. A reader who
  sets the bar at such a sentence would read NOT ESTABLISHED, with the missing item being that sentence or the
  writer's code.

## What it means for the record's forest numbers

The record's forest gate reads `PLYA` from this table. On this reading the values are the published DR1 measurement,
the same numbers the paper plots and fits, and the `BLINDING` keyword and `P1D_BLIND` name do not signal a factor
hidden in the data, so no forest number of the record needs rescaling for blinding. What stays open is the general
point that the gate's amplitude has not been tied in this lane to an outside survey; this lane computes no forest
number and relabels nothing.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
