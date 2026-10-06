# Homogeneous Hamiltonian reduction and admitted constraint data

The declared regular two-lapse representative has two physical homogeneous configuration degrees of freedom on its rank3 patch, after the common time-reparametrization and algebraic auxiliary constraints are properly removed. Hessian rank3 does **not** itself imply a ghost: the critical tensor-mass-cancellation example admits real constraint data with positive reduced homogeneous kinetic. Conversely, the regular positive-slope tensor repair with eta=0 has two negative reduced homogeneous kinetic directions on an actual common de Sitter solution. These statements concern the specified smooth homogeneous model, not the original nonsmooth MOND auxiliary completion or all spatial helicities.

## Actual variables before gauge fixing

Start from the exact both-lapse action in ../REPORT.md, not fixed-lapse field equations. Set

`alpha=ln a`, `beta=ln b`, `r=ln(N/L)`, `ell=sqrt(NL)>0`,

so N=ell exp(r/2), L=ell exp(−r/2). The connection difference has u=dot r; dot ell cancels **before** any gauge choice. Each contraction S_A has inverse-common-lapse weight2 and the symmetric volume has weight1. With q=(alpha,beta,r), the complete homogeneous Lagrangian is

`L=(1/(2ell)) dot q^T G(q) dot q−ell U(q,T)`,

`U=Kchi_n a0^2(2A+lambda T^2) exp[n(alpha+beta)/2]`, `chi_n=(n−1)/[2(n−2)]`.

Here G is the exact three-velocity Hessian of the raw kinetic function F at ell=1. Explicitly, put a=exp alpha,b=exp beta,N=exp(r/2),L=exp(−r/2), h1=dot alpha,h2=dot beta,u=dot r into

`F=−Kn(n−1)[a^n h1^2/N+b^n h2^2/L]+K sqrt(NL)(ab)^(n/2)[−m Upsilon_sym+(xi J_sym+eta S3_sym)/2]`.

Then F=dot q^T G dot q/2. The prior raw S1..S5 formulas define every term; checks.py independently constructs them. Both lapses are retained: r is a dynamical candidate, ell is the common lapse. No dot T appears.

The action is the explicitly declared **regular linear** interaction M=−A+mz−lambda T^2/2, with constant m,xi,eta and geometric-mean volume f=1. It is an actual smooth covariant representative admitting all real invariant z, not a definition of the parent source kernel for negative z. A nonlinear or nonsmooth M can have different auxiliary equations and a different constraint algebra; these results cannot be transferred silently.

## Complete finite-dimensional Dirac algorithm on det G!=0

For positive ell and invertible G,

`p=G dot q/ell`, `p_ell=0`, `p_T=0`,

and the canonical Hamiltonian is

`Hcan=ell C`, `C=p^T G^−1 p/2+U`.

Add arbitrary primary multipliers mu_ell p_ell+mu_T p_T. Preservation of p_ell gives the Hamiltonian constraint C=0. Preservation of p_T gives U_T=0, hence T=0 for lambda>0,K>0,n>=3 and finite positive scale factors. Its bracket with p_T is nonzero because U_TT=2Kchi_n a0^2 lambda exp[n(alpha+beta)/2]>0. Preservation of that secondary fixes mu_T=0 on the surface. The pair p_T,T is second class; eliminating it leaves the ordinary canonical brackets on q,p.

After this elimination p_ell and C are first class. C has no ell, and {C,C}=0 identically; its preservation gives no tertiary constraint. Since the Legendre map in the three q velocities is invertible, it supplies no other primary constraint on this patch. The reduced count is

`(10−2*2−2)/2=2` physical homogeneous configuration degrees of freedom.

This is a full constraint algorithm for this finite-dimensional model. It is not the spatial field-theory Dirac algebra, and it does not cover the det G=0 surfaces. The common constraint cannot be dropped merely because ell may subsequently be chosen as1.

## Actual local on-shell admission

Fix ell=1 only after imposing C=0 and T=p_T=0. The Hamilton equations are

`dot q=G^−1 p`,
`dot p_i=dot q^T (partial_i G) dot q/2−partial_i U`.

On an open det G!=0 patch all coefficients are smooth. Finite initial q,p satisfying C=0 have an ordinary local ODE solution, and C is preserved because its Poisson bracket with itself vanishes. This is a local existence statement for a finite-dimensional smooth system, not a convergent-PDE or full-spatial well-posedness theorem.

This homogeneous isotropic restriction captures all equations for the declared covariant action in this symmetry sector: rotational invariance makes off-diagonal spatial and vector components vanish, each spatial diagonal equation is proportional to its scale variation, and the two lapse equations are represented by ell and r variation. Homogeneous T variation is also retained. Thus the constraint data below are not merely offshell Hessian examples. A fiducial coordinate spatial volume has been divided out; no claim of finite total energy on noncompact space is needed.

## Critical m=1/2, xi=3/8, eta=−xi: admitted patch

Take n=3,K=a0=1 and the position data alpha=0,beta=ln4,r=0, i.e. N=L=a=1,b=4. The exact kinetic matrix in (dot alpha,dot beta,dot r) is

`G=[[4041/256,−4143/16,45/16], [−4143/16,1755,45], [45/16,45,0]]`.

Its leading principal minors have signs +,−,− and its determinant is −14258025/128. The LDL pivots therefore have signs +,−,+: inertia is (two positive,one negative), not negative definite. U=16A at T=0.

Set v0=(1,1/4,0). Then v0^T G v0=−1023/256. For every A>0 choose

`dot q=t v0`, `t=sqrt(8192A/1023)`, `p=t G v0`.

The common lapse constraint is satisfied exactly:

`p^T G^−1 p/2+16A=−16A+16A=0`.

Both scale factors initially expand, dot r=0 initially, and alpha is monotone. There is no requirement that dot r remain0; its actual equation is evolved. G stays invertible for a sufficiently small time interval by continuity. The preceding ODE argument gives an actual local homogeneous solution for these data, for arbitrary positive A and lambda. This does not match a galaxy, a common vacuum at infinity, or the original auxiliary interpolation.

## Reduced kinetic: why rank3 alone is insufficient

For F=dot q^T G dot q/2<0,U>0, the lapse equation gives ell=sqrt(−F/U). Substitution produces the Jacobi action

`LJ=−2sqrt(−F U)`.

Its velocity Hessian is

`R=ell^−1 [G−(G dot q)(G dot q)^T/(dot q^T G dot q)]`.

It has the expected null direction dot q. Choose a monotone q coordinate as the internal time gauge and restrict this matrix to the two remaining velocities. The gauge is locally admissible when that coordinate's velocity is nonzero. By a basis containing dot q and Sylvester inertia, the restricted Hessian removes the negative direction of G when the constrained velocity is timelike. No extra constraints are being guessed from a Hessian sign.

At the critical admitted data, use alpha as clock. The ell=1 physical beta,r block is exactly

`[[3357498,231120],[231120,16875]]/341`,

with first principal minor positive and determinant 9505350/341>0. It is positive definite. Thus this critical rank3 homogeneous patch cannot be called a ghost just from the relative-lapse Hessian or rank restoration. This is a positive **homogeneous kinetic** result, not an assertion about the full spatial Hamiltonian, gradients, tensor degeneracy, nonlinear cutoff or observations.

## Regular tensor repair: two negative homogeneous kinetic directions

Now take n=3, m=xi=1/4, eta=0, K>0. On the exact coincident solution a=b=exp(Ht), N=L=1,T=0, the interaction connections vanish and

`H^2=a0^2 A/6` for A>0.

This is a common de Sitter solution of the declared action: the interaction correction and its first variation vanish at C=0, while the potential supplies the same vacuum term. Use tau=(alpha+beta)/2 as monotone internal clock, zeta=alpha−beta and r as the two remaining coordinates. At a=b=1 the unreduced kinetic is

`F=−12K dot tau^2−(3K/2)dot zeta^2−(K/8)(dot r−3dot zeta)^2`.

G is negative definite and invertible. The background dot tau=H satisfies F+U=−12KH^2+2Ka0^2A=0 exactly. Since its velocity has only a mean component and there are no kinetic mean-relative cross terms at coincidence, lapse elimination leaves the physical relative block

`K[[-21/4,3/4],[3/4,−1/4]]`.

Its first minor is negative and determinant is 3K^2/4>0. Both reduced homogeneous kinetic directions are negative. This is a genuine result **after** the common constraint and time gauge, in contrast to bare negative gravitational scale kinetic before reduction. The admitted de Sitter solution has a rank3 neighborhood, so no extra primary constraint can be assumed to remove these two directions there.

The same representative's TT mean kinetic is positive and its regular relative TT has the previously repaired positive kinetic/mass. The opposite sign in this homogeneous scalar sector exposes a material failure of treating that tensor repair as all-sector health. I do not infer a full finite-k ghost spectrum, a Hamiltonian unbounded on all constraint sheets, or a general BIMOND no-go from this restricted result. The internal-clock reduced Hamiltonian and allowed momenta can have further domain restrictions. At det G=0 or a nonmonotone clock this chart does not apply.

## Vacuum normalization and exact missing arrow

Both explicit cases admit constraint data for every A>0 and lambda>0; the constraint adjusts velocities or background H rather than selecting A. Lambda only fixes an algebraic auxiliary pair in this regular representative. No equation yields a distinguished lambda or32pi. If a separate source/vacuum endpoint convention fixes A in terms of an NR moment, that remains a separate conditional dictionary; this globally linear probe is not the parent's MOND source function.

The next physical implication is the full spatial primary/secondary constraints and principal scalar/vector spectrum for a fully specified source-compatible Lorentzian continuation. The critical representative supplies an actual homogeneous on-shell escape from the claim “rank3 automatically ghost,” but still has critical TT degeneracy. The regular eta=0 tensor repair fails the reduced homogeneous kinetic test. Other invisible counterterms and singular-rank branches require their own constraint reduction. No conclusion here is a32pi selector.

## Evidence

checks.py rebuilds the raw homogeneous kinetic function, verifies its common-lapse scaling and Legendre transform, auxiliary bracket, exact critical G/admitted constraint data, directly differentiates the Jacobi Hessian, and checks the actual regular de Sitter relative kinetic. Three controls assert rank3 implies negative critical kinetic, omit the common constraint in counting, or misclassify the regular repaired homogeneous kinetic as positive. The general constraint proof and smooth ODE admission are analytic; algebraic outputs are corroboration, not a spatial theorem or an integration certification. provenance.json records actual HEAD and input hashes; contract and fresh bounded run records pin the final evidence.
