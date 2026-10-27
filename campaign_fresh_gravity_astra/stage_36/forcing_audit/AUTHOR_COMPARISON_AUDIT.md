# FGF049 narrow author comparison: actual forcing and weighted gradients

Normalized claim: for the unchanged C1,1 compressive family and fixed positive
Q/scale/isothermal-fluid coefficients, sufficiently large N cannot admit a
positive classical solution on the stated physical cone through
T_N=B_* L/(v0 N^4) while BOTH the force-impulse budget (F) and the one-sided
adverse-gradient budget (D) hold on that entire cone/time interval.

Primary verdict: **conditional on a named input** — (F),(D) for the actual
coupled branch. The author's implication from those hypotheses to its
conditional upper-time obstruction is correct in the reviewed scope. No
blocking identity, force-gate, or scope defect was found. This narrow audit
is not a second independent existence/restart theorem or an unconditional
upper-lifespan/classification result.

## Provenance and pinned statement

I first froze INDEPENDENT_DERIVATION.md at 2026-10-06T05:43:32.505105+00:00,
SHA256 9f82562aec3cc623265051df3e62349e40cca6c05f95546bafa71e6cc1918768.
That freeze precedes any new stage36 author, root, or reviewer proof/preview.
All nine old ancestry pins match; the disclosed old-source read-before-pin
chronology remains in the unchanged independent file. No root/stage36 proof
was read for this comparison.

After the coordinator supplied final pins, I checked these exact author bytes
before reading the RAW derivation (and only afterward read result/FREEZE):

- DERIVATION.md: 187330b696fa88fe9300e974d8870a053f524d25852ffda1957a6be649696f5e.
- result.json: 34f62b2da6894e06e47e62da0fb042dca88e91b97dcb395bd13633385a88bdde.
- FREEZE.json: 9bda782ede5ac04d7d5122c34b67c00ba83c0b9cd2909a229e4bf2785318b869.

They are under deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/
FGF-049/fgf049_run_001/. The ancillary FAILED_ESTIMATES.md was read after the
raw proof and its hash matched the result/FREEZE map on the final check.
No author REPORT.md was needed. All outputs are confined to forcing_audit.

The independent freeze derived a sufficient gate with both an integral bound
and a pointwise adverse-gradient bound. The author's future-tail construction
removes the pointwise requirement. That stronger step is explicitly a
POST-EXPOSURE audit, not something predicted in my independent freeze. The
independent file remains unchanged.

## Dependency graph

Exact fluid equations with c=cs>0 and actual g(t,x)
  -> pressure-retaining Riemann equations and weighted-gradient identities;
exact initial profile/hydrostatic balance
  -> positive weighted upper envelope O(omega) and one negative trigger;
(F) plus fixed-speed bounds and large-N buffer inequality
  -> backward-cone containment and persistence of the chosen plus ray;
(D) plus weighted envelope inequalities
  -> H<=h0+A omega t and a strictly positive budget-corrected compression;
future-tail derivative identity
  -> reciprocal contradiction before T_N.

FGF048 supplies actual short-interval bounds and the existing constructed
branch, but supplies neither (F),(D) nor all chart/endpoint margins on the
full comparison interval. The missing edge is analytic and remains open.
The full field/scale equations feed into that missing edge through n_x and
variable chart/scale terms, not through a static inverse source equation.

## Decisive independent checks

### 1. Weighted identities: passed

With q=log(n/nref), r=v+cq, s=v-cq, alpha=r_x, beta=s_x,
h=n^(-1/2), y=h alpha, zeta=h beta, direct differentiation gives

    D+alpha=-(alpha+beta)alpha/2-g_x,
    D-beta =-(alpha+beta)beta/2-g_x,
    D+h=h beta/2, D-h=h alpha/2,
    D+y=-y^2/(2h)-h g_x,
    D-zeta=-zeta^2/(2h)-h g_x,
    Dv h=(y+zeta)/4.

No force-time derivative is missing. The source is spatially differentiated
along flow-label identities; C1 g and C1 fluid variables suffice for the
stated characteristic proof. C1,1 initial joins never require pointwise f''.
The constants d_f=8/(3sqrt(3)), initial alpha/beta signs and trigger
w_c(0)>=b_* omega are correct. Pressure remains in r,s and speeds v+/-c.

### 2. Integrated adverse budget: passed, post-exposure stronger step

The envelope argument uses only K_N=sup(-g_x)_+. For
eta=min(A/2,b_*/2)/H_* and integral K_N<=eta omega, a proposed first contact
M=2A omega instead gives M<=1.5A omega, hence H<=h0+A omega t<=H_*.
The value of positive g_x is favorable; it need not be bounded for this step.

For the full hypothetical slab set F_tail=H_* integral_t^T_N K_N and
u=w_c-F_tail. Because u(0)>=b_*omega/2, direct differentiation yields

    u'=w_c'+H_* K_N
       >=w_c^2/(2h)+K_N(H_*-h)
       >=w_c^2/(2h).

Thus u is positive and nondecreasing, w_c=u+F_tail>=u, and

    u'>=u^2/[2(h0+A omega t)],
    1/u(t)<=2/(b_*omega)-log(1+A omega t/h0)/(2A omega).

At T_N the right side is -2/(b_*omega), since its logarithm equals 8A/b_*.
This is a strict contradiction. The sign of the future-tail subtraction is
correct. This proof does not replace a time integral by a pointwise bound,
and concentrated K_N peaks are allowed. Dependence on hypothetical future
values is legitimate in a proof that assumes a solution through T_N and
contradicts it; it would not justify values beyond an actual earlier endpoint.
The author states precisely that distinction.

### 3. Force and domain gates: passed conditional on (F)

From integral G_N<=Gamma V,
|v|+c<=(1+Gamma)V+cQ0+c<S_N. The strict speed bootstrap gives all backward
fluid/material rays their required cone containment. On the positive chart,
B_g=2g/sqrt(a^2+4g^2) lies in (0,1), so field speeds are bounded by
1/sqrt(tau) and sqrt(J/sigma), even without an N-independent lower B_g
margin. The vertical reconstruction speed is zero. The author's S_N includes
these speeds with a positive margin. The selected plus ray remains inside
K_t because ell+2S_N T_N<R. Since S_N=O(N), loss of width is O(N^-3).
These are valid physical-patch statements under (F), not an assertion that
the chart and solution automatically continue to T_N.

### 4. Actual source, density and scale derivatives: passed

The author retains all terms in

    D_i Z_i=H_i^0(Z)-(C/tau)n e_i,
    D_i Z_i,x=-(Dlambda_i.Z_x)Z_i,x
                   +DH_i^0.Z_x-(C/tau)e_i n_x,
    e=(1,1,0,0,0),
    2b g_x=R_+,x-R_-,x-2Hcal_chi k.

Differentiating n_t+v n_x=-n v_x gives
D_v n_x=-2v_x n_x-n v_xx, and differentiating D_v q=-v_x gives
D_v q_x=-v_x q_x-v_xx, with a.e./weak second derivatives at the joins.
The author's (5.6) is a conservative integrating-factor consequence.
The n_x terms in the two potential modes are equal at the same point, but
their characteristic integrals use different paths; subtraction supplies no
free cancellation estimate. The term 2Hcal_chi k is necessary and present.

The exact source sign relation is B_g g_x=Cn+tau p_t-B_chi k. Positive n
does not imply g_x>=0 because the p_t and scale terms have no proved sign.
The full scale source T-U_s', a=a_ref exp chi, and W_g=B,T=-W_chi are all
preserved. This agrees with the frozen primitive-derivative check
 g_tt=(B_xx-Cn_x)/tau, including all B_chi derivatives. No static source
inversion, pressureless substitution, or coefficient retuning appears.

### 5. FGF048 coverage and exact gap: passed as a limitation

The accepted short-time control gives n=O(1), q_x=O(N^3), first fluid
derivatives O(N^4), total derivative-Lipschitz norm O(N^7), bounded fields,
|g-g0|=O(N^-4), and |g_x-g0_x|=O(N^-1), on kappa/omega only. Thus the
short-time integrals of |g| and (-g_x)_+ are O(N^-4). Their small consumption
relative to the proposed O(N) and O(N^4) budgets is not a bound on the rest.
The bootstrap requires small kappa and its derivative-Lipschitz estimates
are consequences of that same short-time closure. Replacing kappa by B_*
is circular. The author accurately marks full-time (F),(D) and compact chart
control as unproved. An uncontrolled bound is not a stable counterexample.

### 6. Endpoint and restart scope: passed within narrow review

The author distinguishes full-slab obstruction from classification. Its
separate sufficient gate assumes compact state, n and g positivity margins,
bounded chi, full first derivatives and a buffered domain. Under those
assumptions (6.1) is linear in H_f+H_z, with constants allowed to depend on
fixed N and the compact state set, so the displayed higher-norm implication
is consistent with the pinned coupled structure. Nothing in (F),(D) alone
supplies the missing g/B_g or complete scale-state margins. The author does
not inherit FGF046's first-gradient classification. This review checks the
force/regularity hypotheses and the displayed implication's scope, not a
second full local existence, domain gluing or restart construction.

### 7. Energy and hydrostatic control: passed

Full fluid+interaction exchange is +np. The Q field supplies -np-Tw/C,
and the scale supplies +Tw/C. Thus E_t+F_x=0 with both flux terms
-(pB+Jwk)/C and all kinetic, W, scale-gradient and U_s contributions.
For moving endpoints the Reynolds terms are b'E(b)-a'E(a); on the inward
cone they equal -S_N[E(a)+E(b)]. No conserved shrinking-cone energy or
small-energy gradient estimate is claimed. Initial kinetic excess is
O(V^2 ell)=O(N^-1), while |v_x(0)|=d_f v0 N^4/L.
The zero-velocity hydrostatic tuple solves all four equations and has zero
flux. Its gradient values alpha=-g0/c,beta=g0/c do not satisfy the order-omega
compressive trigger. No false instability of this control is inferred.

## Obligation matrix and precise disposition

| Obligation | Disposition |
| --- | --- |
| Raw statement/task and author pins | Passed, exact bytes checked |
| Actual weighted identities and original C1,1 data | Passed |
| Integrated-budget correction and contradiction | Passed as conditional theorem |
| Full upper-interval budgets for actual family | Conditional, unproved |
| n_x feedback and all scale source terms | Passed |
| FGF048 is only a short lower-time estimate | Passed |
| Physical cone/characteristic containment | Passed under (F) and stated threshold |
| Positive complete chart margin to endpoint | Conditional, unproved |
| Endpoint first-gradient classification | Not asserted; not established |
| Full existence/restart theorem independently re-audited | Out of scope |
| Full energy and moving-boundary control | Passed |
| Separate laws, normalizations and histories | Passed |

The two dimensional a_ref values 9.3619e-11 and 1.1279e-10 remain separate
backgrounds. Constant vacuum, each frozen a0E(z) with
E(z)^2=.315(1+z)^3+.685, and an evolving protocol remain different branches;
the latter requires work and is excluded from fixed-reference conservation.
Q is distinct from RAR, registered M and filtered MONO. Diagnostic chi adds
a degree of freedom and establishes no physical vacuum completion, metric/
photon/two-DOF result, criterion B, calibrated cluster evidence, cosmology,
historical novelty or theory closure.

Strongest safe statement: the conditional full-cone upper-time obstruction
is accepted in this narrow audit; actual-family upper time and endpoint
classification remain open. The cheapest meaningful next analytic check is
the signed/two-path evolving-density feedback bound on the remaining interval,
with the same chart/physical-domain conditions. Repeating FGF048's short-time
bootstrap does not settle it.

Proofread: this comparison and its matching audit metadata. Routine edits:
none needed after final read. Mathematical-token changes to source: none.
Unresolved issues: full-time feedback and chart gates, explicitly mathematical
and not proofreading errors. Validation: exact input/artifact SHA256 and JSON
structure; no mathematical executable computations, literature or services.
