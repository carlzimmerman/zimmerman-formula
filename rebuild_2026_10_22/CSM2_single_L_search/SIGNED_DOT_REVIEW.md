# Signed-map arithmetic checkpoint

The completed run is signed_dot_002_cached. All8 controls pass, covering7440
projection dot bounds (62nodes x4bins x15rows x2bounds). It propagates directed
mass-difference boxes through signed binary64 projection coefficients, inventory
weights, and an explicit anchored map. Its fixed-map score lower bound is
569.5321678519074. This is not a certified original-likelihood score.

Actual longdouble precision on this host is53 significant binary bits; the
unit-roundoff bound2^-50 is conservative. For n products/summands, the usual
absolute dot error is bounded by gamma_(2n) times the exact sum of absolute
products, plus underflow terms. A rounded nonnegative absolute sum yields its
upper enclosure by division by1-gamma_(2n). Directed50-digit arithmetic carries
this error budget, stacking, residual mapping and final score. The chosen
eta2^-1000 exceeds actual binary64 minimum normal2^-1022 by over four million;
this leaves ample slack for absolute subnormal errors and their amplification.
All intermediates checked by the run/review are finite.

The exact-dyadic review uses Fraction arithmetic on24 predeclared selected dots;
each exact dot is contained in its saved bound. It independently sums squares
of distances from the60 saved residual boxes using exact rationals, obtaining
a downward binary64 score floor569.5321678519072. All31 review controls pass.
Selected exact dots are a review of the exhaustive derived-error calculation,
not a claim of exact-dyadic recomputation of all7440 dots.

Q=P@W emitted NumPy matmul status warnings; stderr is preserved. The review
checks all saved coefficients/evidence finite. Q is treated as the resulting
fixed binary64 matrix. This stage does not certify that it is an exact
annihilator/whitener of the original covariance/template. Projection coefficient
construction and continuum column/branch enclosures are likewise still open.

The initial uncached attempt signed_dot_001 remains subject to its original
bounds and is excluded from publication while incomplete. Its inner loop
repeatedly decompresses NPZ members. The cached rerun changes only loading,
not arithmetic or criteria (SIGNED_DOT_CACHE_AMENDMENT.md). No native run or
follower was changed. Preserve the first attempt's eventual bounded outcome.
