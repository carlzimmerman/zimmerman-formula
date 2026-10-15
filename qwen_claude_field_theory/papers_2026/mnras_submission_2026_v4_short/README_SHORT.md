# Short plain-language MNRAS manuscript (v4, 2026-10-15)

`mnras_a0_lambda_short.tex` / `.pdf` — "Crispy Fried Chicken Conjecture on Galaxy Dynamics", 5 pages including references (4.3 of text/tables + references).
It states the conjecture as (P1)/(P2) with refutation criteria (R1)/(R2), defines every symbol (Table 1) and ends with a claim-by-claim ledger (Table 2). It is the v3.4 paper (`../mnras_submission_2026_v3/`, MN-26-3158-P, rejected 2026-10-07) rewritten at about three pages of
text, every step of the algebra shown and every symbol explained in words.

**Why:** the editors' comment on MN-26-3158-P was that the paper "does not reach the standards of clarity, rigour and
logical argumentation", with "many sentences [having] no clear scientific meaning". This version keeps only the pieces that can be
stated and verified in a few lines: the unit argument for the form, the unit chain to 9.36e-11, the 1/Upsilon degeneracy, kappa
from three SPARC methods, the three redshift predictions, the error-amplification derivation, and the number of galaxies needed.

**Cut from v3.4 (still in the long version, Zenodo 10.5281/zenodo.23192441):** the error budget tables, the deep-regime
MIGHTEE-HI comparison, the RC100 stress tests, MUSE-DARK/KURVS/CRISTAL/ALESS 122.1, the NFW appendix, the repository index.

**Checks:** `python3 short_numbers.py` recomputes 52 checks (26 algebra: dimensional analysis, the unit chain, the series, the
amplification derivation re-solved numerically, the odds formulas by Monte Carlo and exact N-galaxy KL; 19 data: read from the
committed `../mnras_submission_2026_v3/paper_numbers.json`; 7 literature), verifies that each quoted phrase occurs in the .tex,
and fails if the .tex contains any number with two or more decimals that is not registered. `bash build.sh` runs figure -> numbers -> PDF.

**Not done / owner decisions:**
- The PDF carries the placeholder "address supplied at submission"; the e-mail goes in only through the v3 `make_upload_bundle.py`
  route (git-ignored). No upload bundle or cover letter was built for this version.
- Whether to send it to MNRAS at all: the 2026-10-07 decision said the editors could not give the manuscript any further consideration.
- One non-obvious claim to keep scoped: above delta_c = 0.058 dex the sample MEAN alone cannot reach 20:1, but the full
  likelihood (mean and spread) still can (52 galaxies at 0.07 dex); the text says both.
- Estimator A's "24 galaxies" is checked against `reproduce_outputs/estimator_A.out`, which is git-ignored (regenerate with v3 `reproduce_all.sh`).
