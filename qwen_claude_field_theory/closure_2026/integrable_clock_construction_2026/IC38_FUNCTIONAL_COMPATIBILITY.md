# IC38: a function-level second-preservation obligation

Base c23c1d7ec34f32b1c982648a27ae25ce88243115 plus the uncommitted IC37
derivation. Original full gravity goal OPEN. Carl Zimmerman's exponential
kernel, vacuum-scale relation and primordial-clock idea motivate this route.
The preceding vacuum-density answer supplied context, not construction progress.

## Bounded implementation plan

Continue inline under the user's standing autonomous research authorization.
Keep the same action, coefficient table, ordinary fluids and initial-data family.
Do not discard IC36/37 failures or substitute a different gravitational target.

1. In `test_ic38_functional_compatibility.py`, test exact compatible and
   incompatible operator pairs, a singular reduction, and nonzero highest-order
   coefficients. Use hand-solved scalar ODEs; observe missing implementation.
2. In `ic38_functional_compatibility.py`, eliminate the common second derivative,
   differentiate once, solve the actual two-by-two algebraic system, and test
   BOTH differential integrability residuals. Derive the generic identity in
   SymPy rather than assigning a desired determinant or residual.
3. Add optional coefficient export to `ic37_local_taylor.local_result` for this
   consumer. Apply the operator reduction to the actual same-action sources
   at 50/80-digit precision. Compare baseline and both IC37 selected branches.
4. Preserve exact identities separately from numerical Taylor evidence. Freeze
   inputs, run all new scripts and the relevant full closure regression suite,
   inspect provenance, self-review and commit/push only this work's files.

## Exact reduction, including a zero first-derivative coefficient

Assume real C2 coefficient/source functions on an open interval, c2 nowhere
zero, and seek a C2 common solution A=S_tt. Write

    c2 A'' + c1 A' + c0 A + f = 0,
    w2 A'' + w1 A' + w0 A + g = 0.

Here f and g are independently differentiated same-action sources. For a
finite multiplier, g=FW+eta exp(S) L with L=ell_tt; for an identically vanishing
unmultiplied residual, g=FW. A is not the action's mixing parameter A.

Put p=c0/c2, q=c1/c2, h=f/c2 and

    b0=w0-w2 p, b1=w1-w2 q, bF=g-w2 h,
    d0=b0'-b1 p, d1=b0+b1'-b1 q, dF=bF'-b1 h.

Every common solution obeys

    M (A,V)^T = -(bF,dF)^T,  V=A',
    M=[[b0,b1],[d0,d1]].

On an interval where det(M) is nonzero, let (Ahat,Vhat) denote this unique
algebraic candidate. A common solution exists there if and only if

    R1=Ahat'-Vhat=0,
    R2=Vhat'+p Ahat+q Vhat+h=0

as FUNCTIONS on that interval. Necessity follows by elimination and
differentiation. Sufficiency follows by substitution: R1 identifies Vhat
with Ahat', R2 is the first ODE and the first row of M recovers the second.
There is no division by b1; isolated or identically zero b1 is allowed.
If det(M)=0 this reduction is undecided, not a no-go or permission to divide.
The algebraic identities imply b0 R1+b1 R2=0. Keep both residuals: when b1=0,
R1 alone can vanish even for an incompatible pair (A''=0, A+x^2=0).

This is a direct elementary elimination proof, not an external theorem or a
novelty claim. It does not establish full Dirac closure or solve the field
theory. A finite Taylor computation of R1/R2 is not function-level existence.
The next constructive input is a bounded L and initial profiles satisfying
these residual equations with the first-preservation equations, not another
independent fit of the lapse's two integration constants.
