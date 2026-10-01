# Independent FGF031 uncertainty certificate plan

Auditor /root/metric_intake. Algebra derived from task031 and pinned stage15 target proof/code before reading any new worker or root code/proof. A worker message describing its own norm-based plan arrived after the auditor had independently reasoned the formulas below but before this filesystem freeze; that preview is disclosed and is not counted as independent numerical evidence. The auditor uses a sharper dual-row target bound and componentwise gap bounds; no new worker implementation or stage19 root proof has been inspected.

Let H=[U,c] be the saved 15x16 binary64 matrix interpreted entry-by-entry as exact rationals. U is 15x15. L has L5=-5,L6=+5 (zero-based), every other entry zero, and extended last coefficient zero. This is dp/d(r/R500) at radius1 between .9 and1.1; pressure coefficients are in keV/cm³. Offset, geometry, support through fixed endpoint6 and nodes remain as FGF029.

Compute q=-U^-1c, mu=Lq, a=||U^-1||infinity induced max row absolute sum, b=||q||infinity and R=||L U^-1||1. The vector norm is max absolute entry. For real perturbations ||E||infinity,induced<=delta and ||e||infinity<=delta, factor U+E=U(I+U^-1 E). If a delta<1, the Neumann inverse bound proves invertibility for EVERY allowed E. Put q' = -(U+E)^-1(c+e). Then

 q'-q=-(I+U^-1 E)^-1 U^-1(e+E q),
 eta = a delta(1+b)/(1-a delta),
 ||q'-q||infinity <= eta.

A separate dual-row identity gives the sharper target bound:

 L(q'-q)=-L U^-1[e+E q'],
 |L(q'-q)| <= R delta(1+b+eta)
                =R delta(1+b)/(1-a delta) = Btarget.

Assuming the computed exact mu>0, choose a positive radius no larger than

 delta_max=min{1/(4a), mu/[4R(1+b)]}.

Then a delta<=1/4 and Btarget<=mu/3, so every mu'>=2mu/3>0. The program will take a simple exact decimal radius by starting at1 and dividing by10 until it is <=delta_max; this is deterministic rounding of one proved sufficient threshold, not a response/model sweep. For separate radii replace delta(1+b) by epsilon_c+epsilon_U b. Entrywise |Eij|<=delta/15 is sufficient for the stated induced bound. Entrywise delta would not generally be the same ball: a full matrix of delta entries has induced norm15delta.

## Uniform strictly interior synthetic witnesses

Take the pinned rational baseline p_i=1e-5/(1+x_i)^2 at the sixteen free nodes x=(0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5); append p16=0 at fixed endpoint6. All sixteen differences m_i=p_i-p_(i+1) are positive. Define nominal v=(q,1), v16=0; perturbation bounds d_i=eta for i<15, d15=d16=0. Then

 |v'_i-v'_(i+1)| <= M_i=|v_i-v_(i+1)|+d_i+d_(i+1),
 t=(1/2) min_i m_i/M_i >0,
 p_plus/minus=p +/- t(q',1).

Every successive gap is >=m_i/2>0, including the last free node to the fixed zero endpoint. Hence the PL pressure is strictly decreasing and positive inside the support and zero only at the specified endpoint. The SAME step t works for all allowed errors, but the directions and resulting two profiles depend on E,e. Their exact noiseless bins agree for the SAME perturbed operator: [U+E,c+e]p_plus=[U+E,c+e]p_minus. Their target separation is >=2t(mu-Btarget)>0. This is a for-all-errors existence statement with a common step, not one fixed pair producing a common observed data vector for all operators. No data fit or positivity of all possible solutions is asserted.

## Implementation and controls fixed before code

Use an independent Fraction LU factorization and triangular solves from original NPZ values, not author outputs or a float inverse. Verify U*Uinv=I, nominal H*v=0, dual relation (L Uinv)U=L, mu against the pinned FGF029 exact result, actual nominal witness gaps/bin equality and target separation. Save load-bearing exact constants, chosen radius, gap bounds and witnesses. Include denominator-threshold rejection as inconclusive only, entrywise/induced mismatch, Llast cancellation mutant, and missing-last-gap trap. No error sampling, response-map rebuilding or calibrated instrument assumption.

This finite exact certificate is supported by the analytic norm inequalities for arbitrary REAL matrices in the declared ball. It does not certify that actual continuum/beam/geometry errors lie in that ball; two implementation agreement is not such an error budget. A real external pressure constraint sensitive to the surviving mode remains needed. No pressure-to-force/mass calculation is performed; both a0 normalizations, separate vacuum/H branches and Q/RAR/M remain distinct for any future conversion. Stop after this bounded certificate and audit; no further support or radius search is authorized.
