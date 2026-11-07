# Independent audit: no Cantor part does not restore strong regularity

**Verdict: proved as the stated countertest of a regularity/flow
implication. It is not a native AC2q example or a PDE nonuniqueness
example.** Reviewed `pf15/REGULARITY_COUNTERTEST.md`, SHA256
`bdbdee4fbb775379377d61ef5aee86427436ca3bb1570648d2408e22326217a8`.
Independent delegated audit, 2026-11-06.

For y=x-c t and u=c+delta sqrt(|y|), the weak first derivatives are

    u_x=delta sign(y)/(2 sqrt(|y|)),    u_t=-c u_x

away from y=0. They are locally integrable across that line, but not
bounded. The function and its Burgers flux are continuous, so their
first distributional derivatives have no additional delta. Directly,

    u_t+(u^2/2)_x=(u-c)u_x=(delta^2/2)sign(y).

Thus u is locally W1,1 in spacetime and has neither jump nor Cantor
derivative part. It is not locally Lipschitz at the moving cusp. Its
bounded source is discontinuous in x, and Burgers is genuinely nonlinear.
The state can remain in a prescribed small compact neighborhood of a
nonzero subluminal c on a suitably small bounded region.

The characteristic ODE reduces exactly to y'=delta sqrt(|y|). The
displayed waiting curves, followed by delta^2(t-t_wait)^2/4, are C1
solutions through y=0, as is the curve staying at zero. This disproves
uniqueness of the classical pointwise characteristic curve under these
regularity hypotheses alone. It says nothing about uniqueness of an
almost-everywhere regular Lagrangian flow or of the PDE field itself.
No such stronger claim appears in the candidate.

Consequently even an SBV theorem, combined with zero jump part, would
not by itself recover the bounded derivatives required for the native
strong continuation/Riccati argument. Additional native estimates could
still rule out this type of behavior; the countertest does not assess
their existence. Its initial trace already has a cusp, so it also does
not demonstrate formation from smooth incoming data.

## Narrow source-theorem check

Independently opened [Ancona, Caravenna and Marson, *SBV regularity of
Entropy Solutions for Hyperbolic Systems of Balance Laws with General
Flux function*](https://arxiv.org/pdf/2409.06087), arXiv:2409.06087v4
(header September 1, 2025; internal date September 3, 2025). Theorem 7
on page 3 applies to the constructed small-TV vanishing-viscosity
solution, strict hyperbolicity and genuine nonlinearity, with source
assumption (G) on page 2. That assumption requires time continuity,
uniform Lipschitz control in x and state, and an integrable spatial
derivative envelope; Remark 1 discusses localization of the last
condition. The conclusion removes slice Cantor parts except possibly
at countably many times.

These are not verified native hypotheses: the Jacobian source is only
known to be bounded, a closed coupled source is not supplied, and the
native weak evolution has not been identified with that viscosity
construction. This exact theorem therefore cannot yet close the
native regularity argument. It is not evidence that no other theorem
or direct native estimate could do so. No full-text local cache or
source hash is claimed.

Actual source-note follow-up: read `pf15/SBV_THEOREM_CHECK.md`, SHA256
`7227470adafdd8a215ac7e1852658e6bf9c412b74c77c5bd787f48f33a7e1399`.
Its v4 metadata, Theorem 7/source-(G) extraction and unverified-native-
application verdict agree with the independent primary-PDF check above.
The main theorem is authenticated; its AC2q application is not established.
The additional older search hit is not used by this audit and was not
independently checked here.
