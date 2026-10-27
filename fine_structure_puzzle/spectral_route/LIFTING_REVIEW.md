# Focused independent review of the archive's hypothetical lifting ansatz

**Claim and verdict: proved as written for the displayed mathematical ansatz.** This covers the stationary point, second derivative, potential value, fixed-B sensitivity, arbitrary-target coefficient and constant-uplift statements in the “Executed bounded discriminator” section of `archive_audit/REPORT.md`. The ansatz is not thereby derived from Q3, and no physical electromagnetic coupling is identified.

Reviewed report SHA-256:
`0f3c67b7f1e6bbcc8c53da079997677fbeea0334282d053f360e99eece3f752d`.
Base Git revision `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty baseline.
Reviewed 2026-10-18 America/New_York / 2026-10-19 UTC.

## Fresh derivation from the potential

Take the report's exact domain: dimensionless \(t>0\), \(p>0\), \(M_0>0\), real \(A\), real \(B\ne0\), and

\[
V(t)=M_0^4t^p(A+B\log t).
\]

Set \(u=\log t\in\mathbb R\). The chain rule gives

\[
\frac{dV}{du}=M_0^4e^{pu}\bigl[p(A+Bu)+B\bigr],
\qquad \frac{d}{dt}=e^{-u}\frac{d}{du}.
\]

The positive exponential cannot vanish and \(pB\ne0\), so there is exactly one stationary point:

\[
u_*=-A/B-1/p,\qquad t_*=e^{-A/B-1/p}.
\]

At stationarity \(A+B\log t_*=-B/p\). Direct differentiation, before imposing that equation, gives

\[
V''(t)=M_0^4t^{p-2}
\{p(p-1)(A+B\log t)+(2p-1)B\}.
\]

Consequently,

\[
V''(t_*)=M_0^4pB t_*^{p-2},\qquad
V(t_*)=-\frac Bp M_0^4t_*^p.
\]

For \(B>0\) this is a strict minimum with negative potential; for \(B<0\) it is a strict maximum. A healthy scalar kinetic metric preserves this local mass-sign inference at an extremum. An AdS interpretation additionally uses the usual gravitational potential convention; the report explicitly keeps this a hypothetical ansatz rather than a completed Q3 calculation.

Using only the report's declared **tree-level** dictionary \(\alpha_{SU(2)}=t^2/\pi^2\),

\[
\frac{\partial\log\alpha_{SU(2),*}}{\partial A}
=2\frac{\partial u_*}{\partial A}=-\frac2B,
\]

holding \(B,p,M_0\) fixed. Conversely, for any prescribed positive \(t_0\),
\(A=-B\log t_0-B/p\) makes it stationary. Thus the finite coefficient is the residual datum in this ansatz. Adding a t-independent constant leaves the stationarity equation unchanged. The report correctly distinguishes physical matching freedom from a scheme redistribution with matched coefficients held consistent.

## Checks and limits

The dependency chain is the displayed potential and domain → change of variable → linear stationary equation → substitution → tree-level dictionary. No archive code or output was imported. `lifting_check.py` reconstructs this chain in exact SymPy algebra; `runs/lifting_review_001/manifest.json` is the authoritative current record. It has status **completed**, exit 0, seven checks, unchanged inputs, and passes the manifest validator with `--root`.

| Obligation | Verdict |
|---|---|
| Unique positive finite stationary point under stated restrictions | Passed. |
| Second derivative and vacuum energy coefficients/signs | Passed. |
| Sensitivity with fixed other coefficients | Passed. |
| Any positive target can be obtained by a finite A | Passed. |
| Constant uplift does not select t | Passed. |
| Does Q3 generate this potential and fix its finite coefficients? | Not claimed; not addressed. |
| Does a minimum in t prove stability of the full scalar spectrum? | Not claimed; not addressed. |
| Does the SU(2) tree dictionary determine alpha(0)? | Not claimed; not addressed. |

No actionable correction to the reviewed lifting formulas is needed. Independence is limited to a fresh algebraic reconstruction by a different delegated agent without importing the archive implementation; the report's displayed conclusions were visible, so this was not a blinded review. No whole-archive rerun was performed.
