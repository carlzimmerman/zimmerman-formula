# Independent affine-conformal inverse point audit

2026-09-10. Verdict: **computationally verified only in a stated range**.
No sign, physical/Einstein-frame chart, action-chain-rule, or local on-shell
discrepancy was found at the five tested points. This is not an audit of the
full scan, radial continuation, mass universality, or physical nonlinear energy.

The requested base was `9a088d45c9c3349de154446aeee4500a84f31c9a`.
The actual run used dirty HEAD `3b41b064a2b686c1305179d4d875759f951645f2`;
the intervening HEAD commit concerns unrelated Fable L119 files. All eight
declared execution inputs were hash-stable throughout the run. No root input
or earlier extension artifact was edited by this audit.

## Claim and dependencies

The claim tested is local: the affine-conformal inverse's solved
\((X'',P_X,G_X,P_{XX},G_{XX})\) give the same vacuum EF KGB principal and
on-shell stress/current as an independently rebuilt calculation. The dependency
chain is

\[
 \text{prior covariant variation}
 \longrightarrow \text{independent 3-by-3 solve and real derivatives}
 \longrightarrow \text{verified EF dictionary}
 \longrightarrow \text{imported original KGB stress/principal}.
\]

The last expression is reused, not independently rederived here. The numerical
geometry differentiation and the 3-by-3 elimination do not call the root
coefficient solver. Only the final comparison calls `conformal_inverse.py`.

All points have \(m=1\), \(q=-1\), \(X=1/2\),
\(\epsilon=10^{-6}\), positive \(p=\psi'\), and
\(U=p^2/B\). Physical radius is \(r\), not EF radius \(R\).
The action is the explicit-clock affine family in `REPORT.md`, with
\(F=(1+\sigma X)/2\), \(K=3F_X^2/(2F)\), physical minimal matter,
and no dark matter particles. The present evaluation is in vacuum outside
baryons, where the transformed matter source vanishes.

## Independent equations

Write \(z=X'\), \(a=g+2/r\), and impose \(B=1+2rg\). The radial
variation fixes

\[
 \mathcal P(y,X,z)
 =\frac{2F_Xza+3F_X^2z^2/(2F)}B=P(X).
\]

Its stable GR-connected quadratic root is exactly the root code's

\[
 z=\frac{BP}{F_X[a+\sqrt{a^2+3BP/(2F)}]}.
\]

The independent calculation obtains all partial derivatives of
\(\mathcal P\) by real `mpmath.diff`, including its full \(y\) dependence.
It solves directly for \((z',P_X,G_X)\), without the root's preliminary
elimination of \(z'\):

\[
 \begin{pmatrix}
 \mathcal P_z&-z&0\\
 -2K/B&1&-Q\\
 2F_X/B&0&2Xz/p
 \end{pmatrix}
 \begin{pmatrix}z'\\P_X\\G_X\end{pmatrix}
 =\begin{pmatrix}
 -\mathcal P_Xz-\mathcal P_y/r_y\\
 -F_X\mathcal R+K_Xz^2/B+2K(g-B'/(2B)+2/r)z/B\\
 2F\rho+P+Kz^2/B-2F_X(2/r-B'/(2B))z/B
 \end{pmatrix},
\]

where \(Q=2X(U/X-rg)/(pr)\) and
\(\mathcal R=\rho-p_r-2p_t\). Here \(\rho,p_r,p_t\) denote geometric
Einstein components, not freely selected matter. They are reconstructed by
direct high-precision differentiation of the target metric; \(p_r=0\)
identically. The second row is the **total** scalar current, including the
conformal sector; the third is the lapse equation after using that current.
These rows reproduce the root's reduced 2-by-2 system, including all signs.

With \(v=(y,X,U,P)\), the actual radial tangent is

\[
 v'=\left(r_y^{-1},z,-2g(2X+U)-2z,P_Xz\right).
\]

The independent curvatures are
\(P_{XX}=z^{-1}dP_X(v+tv')/dt|_0\) and the corresponding expression
for \(G_{XX}\), using real arbitrary-precision differentiation. They are
not independently assigned health controls. This is local derivative
consistency along one reconstructed action flow, not common-action matching
across different masses or a check of an integrated interval.

## EF checks and numerical results

The checked action transformation is

\[
 \chi=X/C,\quad C=1+\sigma X,\quad
 \widetilde P_\chi=P_X-2\sigma P/C,\quad
 \widetilde P_{\chi\chi}=C^2P_{XX}-2\sigma CP_X+2\sigma^2P,
\]
\[
 \widetilde G_\chi=CG_X,\qquad
 \widetilde G_{\chi\chi}=C^3G_{XX}+\sigma C^2G_X.
\]

The root's mixed Hessian sign agrees with \(q=-1\) in `EF_PRINCIPAL.md`.
The independent EF curvature calculation uses
\(R=\sqrt C\,r\), \(h=\sigma z/C\), \(D=1+rh/2\), and

\[
 h'=\sigma z'/C-h^2,\quad D'=h/2+rh'/2,
\]
\[
 \frac{\widetilde B_R}{\widetilde B}
 =\frac{B'/B-2D'/D}{\sqrt C D},\qquad
 \widetilde g_R
 =\frac{g'+h'/2-(g+h/2)(h/2+D'/D)}{CD^2}.
\]

It compares the original EF stress against all three diagonal Einstein
components and checks the off-diagonal stress and EF current. Thus the
principal is evaluated on tested on-shell vacuum jets, not just on a freely
selected Hessian. The angular equation is a consistency check, not an additional
independent matching freedom: radial preservation, total current, and lapse
closure already imply it in this restricted ansatz.

The five tuples below are \((y,\sigma,b,d)\), with
\(U=bXrg\), \(z=-dg\), and pressure fixed by the radial equation.
Every independent calculation uses 80 digits.

| Tuple | EF energy/cone flags | Relative EF stress residual |
|---|---|---:|
| (.1,.1,.25,1.5) | both pass | 1.99e-76 |
| (.1,.1,.25,.5) | both fail | 4.28e-76 |
| (1,.001,.75,1) | both fail | 1.10e-75 |
| (2,1,1.25,1.5) | both fail | 3.64e-77 |
| (20,.000001,.25,2) | both fail | 2.09e-71 |

Across these points, all root action-jet relative differences are below
\(9.53\times10^{-16}\) in the recorded one-library-thread run. Root and helper principal coefficients evaluated
at identical root input jets agree below \(1.14\times10^{-15}\).
The independently computed normalized current residual is below
\(2.79\times10^{-77}\). At the healthy seed it is
\(4.47\times10^{-78}\). Stored results retain the
actual values rather than interpreting tiny numerical signs as exact zero.

At the healthy seed,

\[
 P_X=9138.3310493591441,\quad
 P_{XX}=44498849990.493838,\quad
 G_X=-51.147576158675735,\quad
 G_{XX}=37852003.103373311,
\]
\[
 C_{00}=3.8396595889810893\times10^{10},\quad
 C_{01}=1.9422368791926485\times10^7,\quad
 C_{11}=-8579.477918413932,\quad C_{22}=-28280.801300310693.
\]

The strict-cone margin is \(3.8357742572749122\times10^{10}\).
The EF-frame labels and interpretation restrictions in `EF_PRINCIPAL.md`
remain essential; these coefficients do not certify the full physical
Hamiltonian under a derivative-dependent metric transformation.

There is a numerical caveat, not an identified algebraic defect. At the
\(y=20\) point, evaluating EF geometry with already-rounded root float jets
produces a normalized stress discrepancy \(2.584\times10^{-6}\).
The independent 80-digit geometry closes at \(2.09\times10^{-71}\), while
the root action derivatives agree to roughly 15 digits. Large geometric terms
cancel, so ordinary-precision reconstructed curvature does not support a claim
of uniformly near-machine-epsilon on-shell residuals. Near a health boundary,
coefficient signs must also be checked at increased precision.

## Restrictions and remaining obligations

| Obligation | Status |
|---|---|
| Total-current/lapse signs, radial preservation, action derivatives | Independently checked at five points |
| EF coordinate and action dictionary | Agrees with the separately verified helper |
| Same-action vacuum EF stress/current | All components tested locally |
| Regular algebraic/invertible chart | Recorded and tested at all five points |
| Full scan, integrated radial trajectories, or multi-mass matching | Not audited here |
| Matter principal/source, global boundaries, FLRW, full constrained energy/Dirac/Ward analysis | Not supplied by this audit |

The restricted branch needs \(F>0\), \(X>0\), \(U>0\), \(B>0\),
\(D>0\), \(\sigma\ne0\), \(z\ne0\),
\(\mathcal P_z\ne0\), positive quadratic discriminant, and a nonsingular
current/lapse solve. The field-map invertibility factor is
\(C-XC_X=1\), equivalently \(F-XF_X=1/2\); it does not replace the
coordinate or inverse-equation gates. The root's finite-result rejection and
solve errors are not a theorem extending the formulas to singular charts.
The \(\sigma=0\) KGB limit and turning points require another chart.

Under the previously stated regular invertible constrained-mode equivalence,
the model has the conditional two-tensor-plus-clock interpretation and the
same conformal photon null cone. Neither a scalar kinetic-rank argument nor
this finite computation is a full current Dirac or physical energy proof.
Transformed matter cannot be dropped inside baryons. No PPN parameter,
interior matching, novelty, or full-theory claim follows.

## Reproduction and provenance

From repository root, `python3 -B` on `extension/inverse_audit.py` executes
four tests and prints the five-point evidence. The formal bounded command is
recorded verbatim in `inverse_audit_run_001/manifest.json`, with output in
`results.json` and test log in `stderr.txt`. It exited 0 in 1.063159 seconds;
four tests passed. `validate_manifest.py --root` also exited 0 and confirmed
the stored hashes. The enforced run bounds were 60 seconds wall time,
45 seconds CPU time, 1 MiB logs, and a requested one-library-thread cap.

Key SHA-256 values:

- Audited root: `d8629d79b04cac4b60c24187134d23580c93314b6a687d4d8df2cc1551a720f5`
- Audit script: `18d734893513102d78ba67262d5b09dad70b83589d8de6887a5f217383487205`
- Results: `6579546a25708203194470f077dc2492d4e62c875cd4b7786ad1dce42890624b`

Computation-audit shaped the independent implementation and evidence bounds;
proof-audit separated verified dependencies from open obligations, and
proofread-math was used for the final equation/notation review. Only new
`extension/` audit files were added. No commits or pushes were made.
