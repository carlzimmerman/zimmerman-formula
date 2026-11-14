# ABS1 LEAD CHECK (2026-11-14): commit ids, the lead's re-run, and two things the lead adds

Written by the lead session after the lane's result was committed. TEST lane, not blind; adopts nothing, relabels
nothing. The agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| frozen criteria (alone) | adefae297a | 63b408ab0e |
| scripts and run outputs | affd4d69ad | 363fa4898d |
| RESULT.md | 9a88a92edb | cac01b0dc8 |

## What the lead checked

- **Re-run.** `abs1.py` and `abs1_verify.py` copied into a new folder at the same depth and run from scratch (not
  committed, removed afterwards). `abs1.json`, `abs1.out`, `abs1_MUTATE.json` and `abs1_MUTATE.out` are byte-identical
  to the committed files. The verify script's printed output equals the committed `abs1_verify.out` line for line; the
  committed file has the closing house line appended.
- **Order.** The agent's tool calls were listed by script (50 calls, no web call, no forest field computed). The frozen
  criteria were written and committed before `abs1.py` existed. One inline query was run before the freeze, in the
  library's folder; the agent discloses it as printing the data's wavenumber range and the box's wavenumber grid, with
  no power values.
- **Units, read by the lead in the code.** The stored spectra are `mean(|FFT(dF)|^2) x dv / N` on wavenumbers
  `2 pi x frequency` in s/km, with `dF = F / <F> - 1` (`p1d` in `frz3r_core.py`, called by `flux_p1d` in
  `fwn1r_lib.py`). That is the usual one-dimensional power convention, the same as the data's, so the comparison is
  like for like in units and normalisation. The box is in real space with thermal broadening and no peculiar
  velocities.

## Two things the lead adds

1. **The data file carries a blinding flag that no lane has checked.** The table the gate reads from the DESI DR1 file
   is the extension named `P1D_BLIND`, and its header has `BLINDING = desi_y1`. No lane in the record states whether
   the values in the public file are unblinded. The archive the file came in is the paper's set of published figure
   data, which argues that these are the published values, but that is an argument, not a check. Until it is settled:
   - the fit word here (how far the model is from the data) cannot be read as final;
   - if a multiplicative blinding were still in the table, every gate number of the record would carry it squared,
     because the gate multiplies the data by the model ratio.
   A look-up lane (DBL1) is launched to settle it from the paper and the release notes.
2. **What the result means for the record, in the lead's words.** The gate applies the model's fractional change to
   the data's power. ABS1 shows the model's own power is not the data's (25 to 40 per cent low at z 2.2, where most of
   every forest number comes from), so applying the same fractional change to the model's power gives numbers 0.55 to
   0.76 times the stored ones. The lane cannot say which is right. So:
   - words far from the gate keep their word under either scale: every fail at D of about 9 or more, every hold at D
     of about 1.5 or less;
   - a label that is not already a hold and has D below about 7 can change: FWN2's f = 4 on alt and f = 4.5 on both
     footings in the blind-written build. The other scale only lowers the numbers, so no hold turns into a fail;
   - the interpolated ceiling on f moves from 4.12 to 4.59 (canonical) and from 3.99 to 4.42 (alt) under the other
     scale;
   - the record's frozen convention is the stored one, and nothing is relabelled. The moved readings are not passes.
   The misfit itself is what a 20 Mpc/h real-space box with fixed gas parameters is expected to give; it says nothing
   for or against any layout.

## Not covered

- Build A (FRZ6's and FWN1's boxes) was not read.
- Redshift space, a larger box, and the data's own systematics columns were not used.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
