# Exact source and input checks

Checked 2026-10-19. This lane uses the literature-check workflow only for its
two rearrangement arrows. No external result about two-fluid stellar
stability, a GP–Euler flow, or a particular stationary branch is imported.

Source: Almut Burchard, *A Short Course on Rearrangement Inequalities*, June
2009, copyright date 25 June 2009, 47-page author-hosted lecture notes:
[author PDF](https://www.math.utoronto.ca/almut/rearrange.pdf). The author's
[publication list](https://www.math.utoronto.ca/almut/publist.html) identifies
these notes. Exact source text was opened through the web tool; PDF pages
33 and 36 (printed numbering) contain the relevant theorems and their proofs.

Theorem 4.1 applies to nonnegative measurable functions vanishing at infinity
and increases their triple convolution integral after centered symmetric
rearrangement. Apply it separately to each density pair with kernel 1/|x|,
which is already symmetric decreasing; all required integrals are finite by
the potential bound derived in EQUILIBRIUM.md. This includes mutual gravity.
Theorem 4.7 applies to W1,p functions; p=2 and f=sqrt(rho_d) give the required
decrease of its gradient norm. Rearrangement preserves all density Lp integrals.
Neither theorem supplies uniqueness, gap positivity or a stability theorem.

Application verdict for these two arrows: verified. Authentication: primary
author-hosted PDF, matching title, author, date and theorem text. Extraction:
web PDF text and full theorem/proof context checked. Translation: scalar
sqrt-density is in H1; Newton kernel and both densities are nonnegative;
1/|x| has finite-volume positive superlevel sets and the integrals are finite.

Cache lookup by the exact URL identifier found no retained match. A temporary
direct PDF retrieval failed because the shell network has no DNS access.
No PDF hash is invented and no full source text is stored in this packet.
The source is accessible through the web tool; local PDF caching is unnecessary
for the checked arrow and would write outside this lane's allowed scope.

The scalar coefficient is inherited from the parent's fully matched daughter
projection, not rederived here. Its exact antecedent is
`sol61_push/particle_derivation_2026_10_18/micro_response/DERIVATION.md`, §1,
with `EXCHANGE_REVIEW.md`, and the pinned parent
`scalar_dipole_bridge_2026_10_19/virial_normalization/VIRIAL_NORMALIZATION.md`.
Parent artifact hashes are checked and recorded in ARTIFACTS.json. We do not
claim validity of that low-density elimination at arbitrary fluid density.
