# Focused self-review

Primary verdict: conditional on named portal, analyticity and no-cancellation inputs. The positive finite-band contribution and the analytic rotational-invariant restriction follow under their stated hypotheses. A bound on the full renormalized quadratic coefficient or a numerical MOND/vacuum amplitude does not follow.

Scope reviewed: RESULT.md in the frozen lane 13dd783e9e, based on parent 2ce8f3c2b8. This is same-agent self-review, not independent verification. No executable computation was used or needed for the analytic controls.

## Dependency graph and obligations

| Arrow | Status | Evidence or restriction |
|---|---|---|
| Positive-norm state sum to scalar spectral weight | Passed | Official UCLA source section 6.2, (6.37)-(6.46); source result authenticated |
| Multi-operator positive matrix and null condition | Passed | Contracting with h reduces to absolute square of sum of matrix elements |
| Linear portal to negative quadratic cumulant | Passed | Expansion of minus log of partition function |
| Gapped finite band to positive local p^2 contribution | Passed | Geometric expansion for |p^2| < sigma_1; finite moments assumed |
| Finite-band positivity to total beta positivity | Failed if asserted | Arbitrary local subtraction/contact coefficient; explicitly not asserted |
| Small band correction to bound on R | Conditional | No cancellation, specified tolerance and source/force matching required |
| Analytic rotational invariant to even powers | Passed | Restriction to signed axis plus rotational invariance; n >= 2, reflection in n = 1 |
| Generic mass gap to analytic gradient-amplitude expansion | Not established | Regular analytic branch is an explicit extra hypothesis |
| Spectral positivity to vacuum selection | Not established | Independent identity-operator coefficient in fixed background |
| Full gravitational and sourced vacuum stability | Not addressed | Outside this fixed-background correlator calculation |

## Direct sign and null controls

Single positive-norm massive pole: rho_O(sigma) = F^2 delta(sigma-m^2), with m^2 > 0. Then

    Pi(p^2) = F^2/(m^2+p^2),
    Delta S^(2) = -g^2 F^2 chi^2/(2m^2)
                   + g^2 F^2 (partial_E chi)^2/(2m^4) + ... .

Thus Delta beta = g^2 F^2/m^4 is positive. Integrating out a Gaussian massive scalar with real linear mixing gives exactly this kernel, independently checking the cumulant sign. The accompanying negative mass-squared contribution makes clear why this control is not a complete stable long-range-force model. Switching g to zero kills both terms. Adding a local gradient coefficient -g^2 F^2/m^4 cancels the p^2 term but not the pole.

Two operators with equal matrix elements have a spectral matrix proportional to [[1,1],[1,1]]. The vector (1,-1) is null. It cancels their combined matrix element rather than adding a negative-probability physical state. Conversely independent nonzero diagonal spectral entries give no such nonzero null vector on their common support. This confirms why independent-species and general interacting-sector conclusions must be distinguished.

## Matching, units and observable control

For a dimension-four O in four dimensions: [g] = mass^-1, [rho_O] = mass^4, [I_B] = mass^2, [beta] = 1. With [lambda] = mass^-2 and [s] = mass^2, both Delta beta/(lambda s) and 4 pi G I_B a0/a_min are dimensionless. R and the bound epsilon a_min M_Pl/(I_B sqrt(e)) are also dimensionless.

A constant recanonicalization of chi rescales g, lambda and beta, but g^3/lambda and beta/(lambda s) are invariant. Thus the conditional inequality does not gain content from an arbitrary field normalization. If beta is small and positive at fixed source, the solved acceleration differs from the cubic prediction by about half the flux ratio at leading order. RESULT.md deliberately defines epsilon as a flux tolerance, not the exact acceleration error.

The analytic-origin argument applies to E(z) as a function of gradient components, not merely to momentum analyticity of a two-point function. These are separate assumptions; the report does not infer the former from the latter. A nonanalytic bare cubic is an immediate counterexample to any attempt to drop the analytic-microscopic/regular-branch hypotheses.

## Remaining gap and continuation

To turn this into genuine protection, construct a complete source portal and derive a Ward identity fixing its contact contributions against the dispersive term. For the surviving metric/vector-mixing route, the next calculation is the constrained matter-plus-metric response matrix after solving lapse/vector constraints, including local contact terms; scalar spectral positivity cannot be transferred blindly to constrained gravitational variables. This is open, not exhausted, and requires a specified covariant action and vacuum before a reliable loop calculation. To select R, that same construction must also connect the identity-operator coefficient V to the cubic response; none of the present source-correlator identities does that.

Proofreading self-review: new RESULT.md and this review only. Units, symbols, inequalities and exceptions checked; no mathematical-token corrections made after the derivation. No LaTeX build applies to these Markdown artifacts.
