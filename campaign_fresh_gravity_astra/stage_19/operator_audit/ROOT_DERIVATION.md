# Uniform pressure ambiguity under a bounded response perturbation

Root derivation fixed before reading new FGF031 author/auditor outputs.
This is a finite response-model theorem. It authenticates no actual error
budget, pressure datum, covariance or gravitational source correction.

Let U in R^(15x15) be the pinned invertible old response, c its added column,
H=[U,c], and target t=Lx for p=(x,s), with zero target coefficient for s.
Entries in the saved binary64 array are interpreted as exact rationals for
computing the constants. Subsequent E,e can be arbitrary real perturbations.
All bounds below use the SAME declared pressure units and row normalization.
Define induced matrix infinity norm as max row sum of absolute entries,
vector infinity norm as max absolute entry, and row 1-norm as sum absolute
entries. Entrywise bound alpha on E implies induced bound 15 alpha, not alpha.

Put w=U^-1 c, M=||U^-1||inf, W=||w||inf, r=L U^-1,
K=||r||1, mu=-Lw. For ||E||inf<=epsilon, ||e||inf<=eta and
M epsilon<1, the geometric inverse series proves U+E invertible. With
w_tilde=(U+E)^-1(c+e), the exact equation is

 (U+E)(w_tilde-w)=e-Ew.

Thus, uniformly for all admissible real E,e,

 delta = M(eta+epsilon W)/(1-M epsilon),
 ||w_tilde-w||inf<=delta.

Using (U+E)^-1=U^-1(I+EU^-1)^-1 and r gives the sharper target bound

 gamma=K(eta+epsilon W)/(1-M epsilon),
 |mu_tilde-mu|<=gamma, mu_tilde=-Lw_tilde.

The coarser ||L||1 delta bound is also valid. If gamma<|mu|, the target
response is nonzero for the entire error ball and has the same sign.
Therefore H_tilde=[U+E,c+e] has rank15, its null vector
v_tilde=(-w_tilde,1) has nonzero target, and target-augmented rank is16.
Invertibility alone would not prove target ambiguity; the second inequality
is necessary for this certificate. Failure of a sufficient bound proves
only that this certificate is inconclusive, not restored identification.

## Uniform strict synthetic witness

Choose a baseline p with sixteen strictly positive decreasing free pressure
coefficients and append the fixed endpoint p_16=0. Set
m=min_i(p_i-p_(i+1))>0, i=0,...,15. Let Z=max(1,W+delta), and choose

 h=m/(4Z)>0.

Append v_tilde,16=0. Every gap difference obeys
|v_tilde,i-v_tilde,i+1|<=2Z. Consequently p +/- h v_tilde has every gap
at least m/2>0, including the last free-node-to-zero gap. Both pressures
yield EXACTLY H_tilde p and their target separation is at least
2h(|mu|-gamma)>0. These are monotone piecewise-linear profiles in the
specified finite basis, not fitted observations or sharp feasible widths.
The shared step h is independent of E,e, but the vector and synthetic bins
generally depend on E,e. Do not claim those bins are the same across models.

## Stronger fixed-synthetic-data version: a separate conditional implication

One can retain the nominal synthetic bins d0=H p without pretending that
H_tilde p=d0. Keep s fixed to its baseline value s0 and adjust the old
coefficients by

 a=-(U+E)^-1(E x+e s0), p_bar=(x+a,s0).

Then H_tilde p_bar=d0 exactly. The uniform bound is

 A=M(epsilon ||x||inf+eta |s0|)/(1-M epsilon), ||a||inf<=A.

With appended a_15=0 and a_16=0, pressure gap changes are bounded by2A.
If 2A<m, define h0=(m-2A)/(4Z)>0. Then p_bar +/- h0 v_tilde have all
gaps at least (m-2A)/2>0, share the SAME nominal d0 for every E,e, and have
target separation >=2h0(|mu|-gamma)>0. Here E and e are the same for both
members of a pair; no distinct nuisance operator is assigned per profile.
This theorem needs the additional inequality 2A<m. Unless a computation
checks it, it is not claimed for the worker's selected numerical radius.
It still uses synthetic d0, not observed data or an observational confidence set.

## Controls and scope

Zero E,e gives w_tilde=w, mu_tilde=mu, original null direction and baseline.
The fixed-data baseline correction vanishes. A nonzero error radius requires
both M epsilon<1 and gamma<|mu|; fixed data also needs 2A<m. Missing the
factor15 when converting entrywise matrix errors, dropping the last pressure
gap, or keeping an uncorrected baseline while claiming fixed data are invalid.
A units change must transform U,c,L,p and error bounds together; an absolute
radius has meaning only in the saved response convention.

This proof relies solely on the finite U,c,L and explicitly strict baseline.
No new annuli or support extension, parameter sweep or response reconstruction
is required. One exact-arithmetic certificate of the constants and inequalities
is enough; stop this finite robustness route afterward. Actual calibration and
a scalar outer-pressure constraint sensitive to the mode remain separate gaps.
No acceleration or mass is computed. Later inference must supply pressure
conversion and density, then the proper MOND source inversion for the chosen
Q/RAR/registered M law with both a0 footings and separate vacuum/H histories.
No result transfers automatically to physical metric or theory closure.
