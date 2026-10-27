# Root transport calculation and acoustic-resonance check

Scope: exact identities along an already-existing classical solution, and an
initial-data obstruction to a global division estimate. No actual full-horizon
feedback bound or counterexample to compression. Inputs are FGF050's pinned
FGF049 DERIVATION (187330b696fa88fe9300e974d8870a053f524d25852ffda1957a6be649696f5e)
and unchanged data. This is coordinator work, not yet independent acceptance.

Chronology: root derived the continuity IBP privately before the author's
progress message reporting that same identity, but did not freeze it first.
The author's message was received before this file was written. Therefore
this file is NOT claimed as a blinded independent derivation of that identity.
The following acoustic-denominator and initial resonance check was reasoned
before that progress message and is documented here without a prior freeze.
The independent reviewer is not sent this file until its own freeze.

Let lambda be either actual Q characteristic speed (+b or -b),
b=sqrt(B_g/tau)>0, X'=lambda(t,X), and j'=lambda_x(t,X)j, j(0)=1.
All quantities in path integrals below are evaluated at (s,X(s)). For
xi=R_x, the differentiated exact Q mode obeys

  D_lambda xi+lambda_x xi=(H0)_x-(C/tau)n_x.

Thus the density term in j(t)xi(t) is -(C/tau)I, I=int_0^t j n_x ds.
This is a decomposition evaluated on the actual solution, not a decoupled
linear response: j, H0 and the remaining gradients also depend on that solution.
The two Q modes have different paths, Jacobians and scale contributions.

On a path segment where d=v-lambda is nonzero, continuity gives
D_lambda n=-d n_x-n v_x. Integration by parts gives exactly

  I=-[j n/d]_0^t-int_0^t j n D_v d/d^2 ds.               (1)

Indeed D_lambda(j/d)=j lambda_x/d-j D_lambda d/d^2;
its difference from j v_x/d is -j(D_lambda d+d d_x)/d^2.
Since D_lambda+d partial_x=D_v, this is the claimed integrand.
There is no estimate from finite mass alone: boundary traces and signed
weighted acceleration remain. Full momentum yields

  D_v d=-c^2 n_x/n-g-D_v lambda,
  int j(1-c^2/d^2)n_x=-[j n/d]+int j n(g+D_v lambda)/d^2. (2)

Pressure has not vanished. A replacement of the left weighted integral by
(1-c^2/d0^2)I is invalid when d varies.

A way to expose the actual acoustic denominators without dividing by d is
r=v+c log(n/nref), s=v-c log(n/nref). Along the field path,

  D_lambda r=-(d+c)r_x-g,
  D_lambda s=-(d-c)s_x-g.

Whenever d+c and d-c are nonzero,

  n_x=-n/(2c)[(D_lambda r+g)/(d+c)
                    -(D_lambda s+g)/(d-c)].           (3)

These are acoustic-relative speeds. They show why simply replacing the
continuity denominator by a momentum inversion does not remove every
resonance. Division by d=0 in (1) is an artifact of that chosen identity;
d^2=c^2 is the coupled fluid transport degeneracy in (3). Neither is a
singularity of the original PDE merely because a denominator vanishes.

For the inherited initial datum, a global acoustic-separation hypothesis is
already false for sufficiently large N. Take the positive-speed Q mode
lambda=b0(x). Let F_N(x)=V f((x-x*)/ell)-b0(x)-c on
[x*-ell,x*+ell]. It is continuous. At both endpoints F_N=-b0-c<0, while
F_N(x*)=V-b0(x*)-c>0 for large N. The intermediate value theorem gives at
least one zero in each half of the bump. At those actual initial points,
v0-b0=c, so the minus-fluid speed v0-c equals the positive Q speed b0.
All original state coefficients remain regular and positive there. No new
initial data, field freeze of the evolution, or pressureless approximation
was used for this initial-time statement. The roots lie inside K0 for the
same large-N support gate. This refutes ONLY uniform whole-cone separation
|v-lambda-c|>=delta>0 from the exact initial slice; it proves no instability
or failure of the desired adverse-gradient budget.

Negative control: for zero-velocity exact hydrostatics, D_v d=0 for the
stationary fields, so (1) reduces to I=-[j n/d]. The pressure and force cancel
in D_v v=0; no density-gradient source was dropped. Favorable g_x>=0 gives
zero adverse budget regardless of its positive size. The resonance test
cannot replace that sign-sensitive target by a bound on |g_x|.

Remaining implication: a proof based on (1) or (3) must either control the
regions containing the initial acoustic intersections without division, or
split their contributions with matched endpoint terms. Nonresonant interiors
alone do not bound the sup over the full FGF049 cone. The coupled full-time
chart and density-source estimates remain open. These identities hold for
each separately normalized/fixed-reference diagnostic Q branch; no transfer
to RAR, registered M, filtered MONO, metric/photon/2DOF or observations.
No mathematical executable computations were used.
