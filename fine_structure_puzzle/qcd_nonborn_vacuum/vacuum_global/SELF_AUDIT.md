# Focused self-audit, FSP-009

Primary verdict: **conditional on a named input** for extraction of physical
A and A_u. The finite-regulator contact identities themselves are proved by
normalized differentiation. No full physical coefficient has been proved or
evaluated. This is self-review, not an independent audit.

The audited derivation hash is
32fde2450bd0dd3355d9d2cce6b4fa26c407f69301194f3ea47139d6e5056264;
the implementation hash is
809c9bd20d771767a300845881e3f00be2f1ff3554408ddd44270f48d3c12d5c.

| Obligation | Status | Evidence or surviving restriction |
|---|---|---|
| Metric sign, volume and area normalization | Passed | W_t=4Vrho, E=4Vrho_t; r^3 action gives -4Omega A r^3 |
| W_tt contact minus connected variance | Passed | Direct quotient differentiation, independently audited formal -logZ jets |
| Full E_u and reduced F formula | Passed | Differentiate the variance including X_u; centering-mean term has zero mean |
| Fourth cumulant in K_u | Passed | Set-partition cumulants compared to independent t^3u coefficient |
| Positive-measure charge bound | Passed with stated hypothesis | Cauchy-Schwarz; not claimed for a signed/complex measure |
| Source Rindler action dictionary | Passed in exact v2 text | eq24-27,34 and Sections II.2, III.B-C; acceleration is not EM alpha |
| Rindler global reflection derivative | Passed with stated domain | Symmetric boundaries and finite compact-link measure; no thermodynamic conclusion |
| Fixed renormalized metric derivative | Conditional physical implementation | Bare trajectory, measure Jacobians and absolute gravity terms must be matched |
| QCD continuum/contact limit | Conditional | No relevant curved ensemble supplied; no flat separated-insertion theorem substituted |
| H->0 coefficient and charge derivative | Conditional | q_t=o(H) and q_tu=o(H), or corresponding directly controlled limits |
| Global cancellation bound | Not addressed physically | No numerical mean, variance or mixed moment was invented |

The internal dependency graph is definitions -> normalized derivative identities
-> E/E_u formulas -> finite-H bounds. Extraction of A/A_u additionally needs
controlled continuum differentiation and the differentiated asymptotic leaf.
The primary source is needed only for the separate Rindler action application;
it is not a leaf proving the sphere bound.

The finite enumerator has exactly 16 deterministic fixtures, five states each;
the 12 monomial fixtures cover precisely six listed exponents and two
coefficients. The run checks 221 assertions, including 32 component
Cauchy-Schwarz bounds and 16 rational squared aggregate bounds. It does not
claim exhaustive QCD coverage. The formal jet algebra is truncated at t^3u,
which exactly contains all derivatives claimed, including K_u. Set partitions
of four entries are independently checked to have cardinality 15.

Proofread: DERIVATION.md and REPORT.md, self-review mode. Routine edits: none.
Mathematical-token changes: none. Unresolved issues: the named physical leaves
above, not local notation/typography errors. Validation: completed exact run
and v2 manifest validation. No older science or shared navigation was edited.
