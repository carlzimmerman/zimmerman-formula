# Fractional certificate contract clarification

Independent reviewer `cassini_sign_route` identified a stale convention string
in `contract_monotonicity_fractional.json`. It was copied from the p=6 contract:

    z=(y/t)^6; s=(sqrt(1+4/y)-1)/2;
    F=1+exp(-z)*(s*s/(2*s+1)-6*z*s)

For the fractional theorem and its actual executable, the correct convention is

    p=63/10, t0=3163/2000, z=(y/t)^p;
    s=(sqrt(1+4/y)-1)/2;
    F=1+exp(-z)*(s*s/(2*s+1)-p*z*s).

The original contract's `assertion_tested` and `bounds`, both fractional proof
and executable, and the recorded result consistently use p=63/10 and
t0=3163/2000. The incorrect prose convention was not consumed as executable
input, but it is nevertheless a contract inconsistency and must not be
silently corrected after the run. The pinned contract, completed manifest and
original output remain unchanged.

The reviewer independently found the mathematical reduction and rational-bound
implementation sound. The fresh replay under
`../universal_length/fractional_review_contract.json` completed, and its
`../universal_length/fractional_review_001/manifest.json` validates against
the current inputs. The output exactly matches the original result, including
all 4,961 intervals and bound 12671/1000000. The independent analysis is in
`../universal_length/FRACTIONAL_REVIEW.md`, with verdict proved as written
for exact rational parameters. The old run remains a completed exact
computation with this disclosed stale convention string, not an entirely
consistent contract; cite the corrected replay for the accepted evidence.
This clarification does not change the computed rational lower bound, the
mathematical claim, any physical response parameter or an observational cut.
