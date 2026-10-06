# Both-lapse homogeneous constraint probe

The NR-invisible tensor mass repair generally introduces a relative-lapse velocity into the actual averaged-invariant minisuperspace action. Retaining the independently free invisible S3 term can cancel that velocity square on coincident metrics, but in the declared regular linear interaction family it generally reappears through a lapse/scale velocity mixing on arbitrarily nearby configurations. The only parameter choice removing all homogeneous relative-lapse velocity in this family cannot stabilize the regular positive-slope de Sitter tensor. This is a useful constraint-admission diagnostic, not a Dirac analysis, a full ghost theorem, or an exclusion of singular/extended completions.

## Raw action and explicit regular continuation

Retain both metrics before any gauge choice:

`g=(-N(t)^2,a(t)^2 delta_ij)`, `hat g=(-L(t)^2,b(t)^2 delta_ij)`, n>=3, N,L,a,b>0.

Use healthy conventional Einstein-Hilbert coefficient K>0 for each sector; this is the parent's minus-R convention translated to conventional curvature. Use geometric-mean volume

`v=sqrt(NL)(ab)^(n/2)`

and f(k)=1, a declared member of the symmetric-volume family. This precise volume is used in the nearby determinant. No factor inherited from the unsymmetrized literature action is substituted.

For the diagnostic take the **declared regular local linear continuation**

`M(z,T)=−A+mz−lambda T^2/2`, `z=−Upsilon_sym/(2chi_n a0^2)`, `chi_n=(n−1)/[2(n−2)]`,

and add `K v(xi J_sym+eta S3_sym)/2`. Here J=3S1−2S2−S4+S5; each invariant is averaged between g and hat g as in the preceding construction. The homogeneous kinetic Lagrangian, per coordinate spatial volume, is exactly

`Lkin=−Kn(n−1)[a^n h1^2/N+b^n h2^2/L]+K v[−m Upsilon_sym+(xi J_sym+eta S3_sym)/2]`,

with h1=dot a/a, h2=dot b/b. The remaining potential is `−2Kchi_n a0^2 A v−Kchi_n a0^2 lambda T^2 v`. It has no velocity and the auxiliary equation is T=0 for lambda>0. There is no dot T.

This chosen extension is a finite, explicit action-level probe of the continuation/constraint gap. It is **not** the actual eliminated auxiliary MOND kernel away from the vacuum: that kernel's negative-z definition and joint Hessian remain unknown. At exact coincidence the quadratic Hessian uses only a regular two-sided slope M_z(0,T0)=m, so the common result applies more widely than this particular linear representative. Away from coincidence the displayed exact formulas apply to this representative. For a nonlinear M the velocity Hessian also contains its second-derivative outer-product term; that must not be silently discarded on moving nearby backgrounds.

## Connection and five exact contractions

Define relative lapse rate u=dot N/N−dot L/L, spatial connection coefficient vC=a^2 h1/N^2−b^2 h2/L^2, and scale rate w=h1−h2. The nonzero difference connections are

`C^0_00=u`, `C^0_ij=vC delta_ij`, `C^i_0j=C^i_j0=w delta^i_j`.

Using one metric g for contractions gives exactly

`S1=−(u^2+n w^2)/N^2+2n vC w/a^2`,
`S2=(u+n w)(−u/N^2+n vC/a^2)`,
`S3=−N^2(−u/N^2+n vC/a^2)^2`,
`S4=−(u+n w)^2/N^2`,
`S5=−u^2/N^2−2n w^2/N^2−nN^2 vC^2/a^4`.

The hat contractions replace N,a by L,b while retaining these same u,vC,w; C is already the connection difference. Their exchange averages are the actual action invariants. They are even under exchanging metrics and changing C to minus C.

In particular

`Upsilon_g=n[(uw−w^2)/N^2−vC(u+(n−2)w)/a^2]`.

There is no u^2 in Upsilon, but a velocity linear in u can still give a nondegenerate mixed Hessian. “No lapse square” is not “no lapse momentum.” These formulas follow from raw traces, not a fixed-lapse reduction of the equations. The executable reconstructs all five by explicit index sums in n=3,4,5, with general-n closed expressions retained separately.

## Common FRW: relative lapse rank

At coincident positions N=L and a=b, but **before** identifying their velocities, vC=a^2w/N^2 and

`Upsilon_sym=−n(n−1)w^2/N^2`,
`J_sym=S3_sym=−(u−nw)^2/N^2`.

Set the common state N=L=a=b=1 only after this variation, and write hc=(h1+h2)/2, sigma=xi+eta. The frozen velocity quadratic form is

`Lkin=−2Kn(n−1)hc^2−Kn(n−1)(1/2−m)w^2−Ksigma(u−nw)^2/2`.

Thus the reduced Hessian in (hc,w,u) has determinant

`det Hred=4K^3 n^2(n−1)^2 sigma(2m−1)`.

Its ranks are: 3 for m!=1/2 and sigma!=0; 2 for m!=1/2,sigma=0; 2 for m=1/2,sigma!=0; 1 for m=1/2,sigma=0. These are exact algebraic ranks, not physical mode counts. The full velocity Hessian in (dot N,dot L,dot a,dot b,dot T) has the same rank: the transformation to (h1,h2,u) is surjective at positive N,L,a,b. It has a common-lapse velocity null vector (N,L,0,0,0) and the auxiliary null vector (0,0,0,0,1). These nulls are retained explicitly in the checks. Relative u is distinct from the common reparametrization lapse direction.

The coincident-FRW Hessian is independent of the common background H when its positions are frozen. Terms involving H and position perturbations matter for evolution but do not remove this principal velocity result. A positive xi with eta=0 introduces a negative u-square coefficient. The standard gravitational scale-factor kinetic is already negative before its constraints are applied, so neither that coefficient nor this rank by itself establishes a physical ghost.

## S3 cancellation, exact lapse-free choice, and nearby rank witness

Allow eta rather than falsely concluding from J alone. Exact homogeneous identities are

`partial_u(J_sym−S3_sym)=4 partial_u Upsilon_sym`,
`partial_u^2 J_sym=partial_u^2 S3_sym=−(1/N^2+1/L^2)`,

and

`partial_u Upsilon_sym=−n(L^2a^2−N^2b^2)(a^2 h1+b^2 h2)/(2L^2N^2a^2b^2)`.

To remove explicit u dependence on **all** homogeneous configurations in this constant-coefficient family one must first choose eta=−xi to remove u^2, then xi=m/2 to remove the remaining mixed coefficient. This conclusion concerns literal lapse independence, not every possible degenerate-Hessian or secondary-constraint mechanism. On conformally related positions L a=N b the mixed coefficient vanishes accidentally, so coincidence alone is not an adequate test.

For a precise nearby witness set n=3,K=1,N=L=a=1,b=1+epsilon and eta=−xi. In the (h1,h2,u) coordinate system the exact reduced determinant expands as

`det Hred=216(1−2m)(m−2xi)^2 epsilon^2+O(epsilon^3)`.

For 0<m<1/2 and xi!=m/2 it is nonzero for every sufficiently small nonzero epsilon. This is an arbitrarily-nearby off-shell rank witness, not an integrated solution. At m=xi=1/4,eta=−1/4,b=2 the determinant is exactly `243(96−59sqrt(2))/128`, also nonzero.

For a generic nonlinear regular M, the same nearby witness can be interpreted at **zero-velocity** homogeneous jets: C=0 for constant metric coefficients even when their ratios differ, so the M_zz gradient outer product vanishes and the velocity Hessian depends only on m. At moving off-coincident jets that extra contribution need not vanish, and the exact linear-family determinant cannot be exported without rederivation. Zero-velocity jets with the retained vacuum potential are not claimed on-shell cosmological backgrounds. Whether an admissible branch stays on a singular-rank surface requires the remaining constraints and evolution.

## Tension with the tensor repair, and exact remaining implication

The preceding independently reviewed tensor calculation gives kinetic K(1−2m)/8 and curvature coefficient `K[mn−xi(n+1)]H^2/2`. For a regular positive subcritical slope its stable tensor cone is

`xi>=mn/(n+1)>m/2` for n>=3,m>0.

Therefore literal homogeneous lapse independence (eta=−xi,xi=m/2) cannot lie in that cone. With xi=m/2 the curvature coefficient still has positive numerator m(n−1)/2 and gives a growing de Sitter relative tensor. If sigma!=0 a tensor-repair choice already has rank3 at coincidence. If sigma=0 it has the rank3 nearby witness above. The two-invisible-invariant **regular linear family** thus cannot simultaneously supply the tensor repair and an ordinary globally lapse-independent homogeneous action. This is more discriminating than a tensor mass inequality, but does not rule out constraint mechanisms requiring a full Dirac analysis, other operators, singular branches, changed invariant or a different completion.

At the actual critical slope m=1/2, relative tensor kinetic is still zero. The homogeneous ranks quoted above show that degeneracy patterns can differ between helicity sectors, but do not decide nonlinear elimination or strong coupling. No two-sided regular continuation of the auxiliary source branch has been constructed here.

The first missing implication is the actual primary/secondary constraint analysis and on-shell branch admission for the fully specified Lorentzian action. In particular, eliminating T is algebraic only on the declared regular representative; the source candidate's nonsmooth elimination cannot be inferred from it. No physical degree-of-freedom or ghost count is asserted. The additive vacuum offset and lambda remain independent; this probe supplies no32pi normalization.

## Evidence and reproducibility

checks.py verifies raw contractions, common and nearby Hessian determinants, the full five-coordinate nulls, retained S3 cancellation, and the incompatible lapse-free/tensor-repair choices. Controls incorrectly gauge-fix away the relative lapse Hessian, extrapolate coincident rank tuning globally, or equate the tensor stability threshold to the lapse-free choice. Exact algebra and the local determinant expansion support the declared claims; no integration or Hamiltonian reduction is hidden in the checks.

Preflight caught two implementation-only issues: a matrix zero was compared without simplifying its entries, and simultaneous parameter substitution retained an old xi in eta. Both were corrected before authoritative runs; no mathematical formula was changed. provenance.json pins actual input bytes/HEAD; SOURCES.md distinguishes the original published unsymmetrized critique from the present averaged action. REPORT is frozen as a run input; RUNS.json holds the authoritative counts/manifests separately.
