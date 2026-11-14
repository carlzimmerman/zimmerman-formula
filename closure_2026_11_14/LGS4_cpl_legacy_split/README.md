# LGS4 — the legacy supernova split in a two-parameter (w0, wa) fit

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (local 7b1ba21241). A re-read of public data with a public fitting form.
It adopts nothing, edits no ledger and grades nothing in the framework.

## Result
- **As frozen: NOT EVALUABLE AS FROZEN.** The chain gate G0 failed (local 6d106b236c). The fault was in this lane's
  sampler, not in the data: see "Two design errors" below.
- **Post hoc, sampler repaired, every rule and threshold unchanged: THE SPLIT CANNOT TELL.** Both gates pass. Dropping
  the 197 legacy supernovae does not show whether the two-parameter preference is a signal seen with less data or a
  signal the legacy set made. Three numbers lean toward "less data"; none reaches the bar set in advance.

The question: arXiv:2610.23657 (Table 3) reports the preference for w(a) = w0 + wa (1 − a) over constant dark energy
falling from 3.36σ to 2.13σ when the legacy set is dropped from DES-SN5YR Dovekie (+ DESI DR2 BAO + 15 chronometers +
a compressed CMB summary + BBN). Reading A: the fit sits in the same place and only the errors grow. Reading B: the
legacy set is offset from the DES sample and pulled the fit.

## Numbers (post hoc run; `lgs4_posthoc_collect.out`, `lgs4_posthoc_p1_rank1.out`)
Harness H1, this lane's independent code against the paper's "DES + legacy" row: PASS, every mean within 0.10 of the
paper's sd (Ω_m 0.3145 ± 0.0053, w0 −0.800 ± 0.056, wa −0.772 ± 0.221, H0 67.36 ± 0.54). The paper's other two rows
are reproduced as closely (context, no gate): DES only w0 −0.837 ± 0.093, wa −0.658 ± 0.302; free legacy offset
0.0128 ± 0.0214 mag against the paper's 0.013 ± 0.021.

| rule | number | label |
|---|---|---|
| P1 centre shift, two-dimensional | C_des_only − C_full is singular (eigenvalues −5.5e-5 and +4.8e-2) | NOT EVALUABLE |
| P1 one-direction version (post hoc) | shift 0.120 along (−0.34, +0.94), sd 0.219: 0.55σ, p 0.58 (Laplace: 0.65σ) | no frozen label |
| P2 distance from constant dark energy | full 3.42σ (Δχ² 14.74); des_only 2.18σ (7.08); rand197 3.47σ (15.12) | des_only 2 TO 3 SIGMA |
| P3 offset or w(z), full sample | χ²: constant 1666.86; constant + offset 1659.16; CPL 1652.12; CPL + offset 1651.70. G = 7.04; ΔAIC +5.04, ΔBIC −0.48 | CANNOT TELL |
| P4 size control | rand197 3.47σ against 3.42σ; centre moves 0.09 sd | CONTROL QUIET |
| P5 offset wanted by constant dark energy | +0.034 ± 0.012 mag, 2.78σ | OFFSET HINTED |
| P5 offset wanted by CPL | +0.013 ± 0.021 mag, 0.65σ | NO OFFSET |

P2 context (no label). DES-only keeps 0.57 of the information along the full-sample offset from w = −1. If the
full-sample signal is real, the DES-only χ² gain should average 9.3 (2.59σ), with a spread of 5.8; if the legacy set
made it, 2.0. Observed 7.08. A gain this low or lower has probability 0.41 under A; one this high or higher has
probability 0.029 under B.

P3 context (no label; these move with the prior widths). Laplace evidence ratios with the paper's priors, ln B:
CPL against constant dark energy +1.61 on the full sample (paper +1.70), −1.67 on DES only (paper −1.79), −1.50 with
the offset free in both (paper −1.39). CPL with no offset against constant dark energy with an offset: +1.95, which the
paper does not print.

## What this says
- An independent implementation reproduces the paper's three CPL rows to a tenth of their errors. Its numbers stand.
- **The centre does not move.** Without the legacy set the fit shifts by about half of the scatter expected from
  losing those supernovae (0.55σ). The legacy set adds information along one direction in the (w0, wa) plane only.
- **The drop in significance is about what lost data alone would give.** 3.42σ should fall to about 2.6σ if the signal
  is real; it falls to 2.18σ.
- **Inside constant dark energy the legacy set is offset from DES by 0.034 ± 0.012 mag (2.8σ); inside CPL by
  0.013 ± 0.021 (0.65σ).** The same mismatch can be written as an offset or as w(z).
- **The data do not choose between them by the bar set here.** CPL without an offset fits better than constant dark
  energy with one by Δχ² 7.0 for one more parameter: ahead by 5.0 on AIC, behind by 0.5 on BIC.
- A random drop of 197 DES supernovae changes nothing, so the effect is tied to the legacy set and not to sample size.

## What it does not say
- Not which supernova sample is right, and not whether dark energy evolves. Three numbers lean toward reading A
  (the shift, the P2 probabilities 0.41 against 0.029, the AIC), and none is decisive.
- Nothing about the framework. Every ingredient beyond the raw distances is the paper's: the CPL form, standard
  pre-recombination physics, the compressed CMB summary, the BBN prior. No a0 enters.
- Nothing about Pantheon+ or Union3. LGS3 found no such effect there.
- The paper's statement that the preference is not significant without the legacy set is unchanged: 2.18σ here.

## Two design errors in this lane (recorded, fixed forward)
1. **Sampler.** `lgs4_run.py` took the proposal from a numerical Hessian with fixed steps per parameter. Along the
   w0–wa degeneracy that Hessian was not positive definite in all four CPL runs; the chains fell back to a diagonal
   proposal, accepted 1.7 % of steps, and two missed R − 1 < 0.01 (max 0.0208). `lgs4_posthoc_run.py` takes the
   proposal from the frozen run's own chain covariance and the Hessian in whitened coordinates. Acceptance is then
   0.23 to 0.32 and max R − 1 is 0.0008. The χ² minima are identical in both runs (to 1e-9), so P2, P3 and P5 did
   not move.
2. **Rule P1.** The criteria asked for a two-dimensional shift statistic with covariance C_des_only − C_full. That
   matrix has rank one here, because the legacy set adds a single number (the low-redshift level against DES), so it
   cannot be inverted. The one-direction version is reported post hoc and carries no frozen label. With P3 at
   CANNOT TELL the reading is the same whatever P1 says.

## The guess
Written in the criteria before the run: P1 CONSISTENT, P2 2 TO 3 SIGMA, P3 CANNOT TELL (G near 6 to 7), P4 CONTROL
QUIET, P5 OFFSET HINTED / NO OFFSET, reading THE SPLIT CANNOT TELL. It held for P2 to P5 and the reading (G = 7.04).
It missed that P1 could not be evaluated as written. The paper's rows are public, so the lane was not blind to its
likely outcome; what it adds is the shift statistic, the offset-against-w(z) comparison and the size control.

## Files
- `lgs4_like.py`, `lgs4_fit.py`, `lgs4_run.py`, `lgs4_collect.py`: committed with the criteria.
- `lgs4_prefreeze_checks.*`: checks made before freezing, none fitting a supernova sample.
- `lgs4_<sample>_<model>.*`, `lgs4_collect.out`, `lgs4_results.json`: the frozen run (failed G0; no weight).
- `lgs4_posthoc_run.py`, `lgs4_posthoc_collect.py` (the frozen collector with three file names substituted),
  `lgs4_posthoc_<sample>_<model>.*`, `lgs4_posthoc_collect.out`, `lgs4_posthoc_results.json`: the repaired run.
- `lgs4_posthoc_p1_rank1.*`: the one-direction version of P1.
- Thinned chains are kept outside the repo (`_external_data/lgs4_work`).

kappa = 1/2 FITTED; not theory closed.
