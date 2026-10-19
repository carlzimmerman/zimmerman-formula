# Independent derivation of the continuation beyond FSP003

Saved before opening `chiral_zero_mode/` targets. After saving the base pretarget note, the coordinator identified the nearest ancestor: `qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md`, especially sections 4,6,7,9, and `qcd_prediction/coordinator/ZERO_MODE_QED_RAW.md`. Those prior files already derive the Haar/Dashen integral, axes, first charge response, measure cancellation, and exact-over-Gaussian assembly proposal. The base calculation is therefore **known after notation translation within the project**, not new work. No base finite grid will be repeated.

## Exact-over-Gaussian replacement

For x>0 and x+2y>0, the normalized Haar saddle factor is

`Z_G(x,y)=sqrt(2/pi) exp(x)/[sqrt(x)(x+2y)]`.

Its exact-over-Gaussian factor is `Q0=Z(x,y)/Z_G(x,y)`. If using only a charge difference relative to y=0, the normalization-independent replacement is

`Q_EM=(1+2y/x) Z(x,y)/Z(x,0)`.

Thus `Delta W_repl=Delta W_Haar-log(1+2y/x)`. The subtracted logarithm is independent of radius at fixed physical mass and charge because y/x is fixed. The replacement's direct charge-difference stress is consequently the same as the Haar coupling-difference stress. This is an exact algebraic assembly identity, already proposed in FSP003 section 9; evaluating it alone does not constitute a new physical calculation.

## First nonconstant-pion source contraction

Use the fixed decomposition `U(X)=U0 exp(i tau_j pi_j(X)/F)`, with `integral pi_j=0`, and the massless leading nonconstant pion covariance

`<pi_i(X) pi_j(X)>=delta_ij Gbar(X,X)`, `g=Gbar/F^2`.

The source action is integrated over the sphere. Its linear pion terms vanish because the nonconstant field has zero average. At first contraction order,

`<a0(U)>=a0(U0)[1-3g/2]`.

For the electromagnetic operator, the adjoint rotation of `exp(i tau.pi/F)` has expectation `I(1-4g)`: its quadratic term is `2(pi pi^T-pi^2 I)/F^2`, whose contraction is `-4g I`. It follows directly that

`<s(U)>=(1-4g)s(U0)+2g`.

Therefore the source-dependent partition factor, through this first pion contraction, is

`Z_1(x,y;g)=exp(-2yg) Z(x(1-3g/2), y(1-4g)) + O(g^2)`.

The exponential is essential. It depends on charge and radius even though it is independent of U0. Removing it without an explicit local counterterm changes the source response.

With `L=log Z`, write

`W_1=W_0+g T+O(g^2)`,

`T=2y+(3/2)x L_x+4y L_y=2y+(3/2)x<a0>-4y<s>`.

At this epsilon order the LO kinetic action is independent of the constant U0 by group invariance. The decomposition/collective Jacobian is also source independent when the same zero-average constraint and massless nonconstant covariance are used at every x,y. Their vacuum factors therefore cancel in the same-radius ratio at fixed x between y and zero. This cancellation does **not** remove the source-dependent `exp(-2yg)` factor, and does not compute dynamical photon effects.

## Matching subtraction needed with an existing full Gaussian determinant

At aligned `U0=I`, the same nonconstant source contraction is

`T_aligned=(3/2)x+2y`.

This equals the leading source expansion of the free nonconstant pion determinant:

`(VGbar/2)[M^2+2(M^2+2uC/F^2)] = g[(3/2)x+2y]`.

Hence an assembly that starts from a full Gaussian pion determinant and adds the exact-over-Gaussian constant replacement cannot then add all of gT again. In a common subtraction scheme the genuinely additional first mixed source correction is

`g[T-T_aligned]`.

For the normalized electromagnetic difference it is

`g{(3/2)x[<a0>_(x,y)-r(x)]-4y<s>_(x,y)}`.

The 2yg factor cancels the aligned electromagnetic tadpole only **after** this matching subtraction; it must not be silently dropped before matching. A full heat-subtracted determinant and a massless tadpole may use different finite local prescriptions, so their local matching terms must be translated before declaring a complete replacement formula. This is a necessary consistency obligation, not a claim that an arbitrary mixed-order assembly is complete.

## Curved tadpole, counterterms, and direct metric derivative

The massless prime coincident Green function is formally

`Gbar=(1/V) sum_(l>=1) d_l/[H^2 l(l+3)]`.

Removing l=0 changes the infrared part, not its ultraviolet coefficient. The minimal scalar diagonal heat term `R t/6` gives, in `d=4-2epsilon`,

`Gbar_div=R/(96pi^2 epsilon)`, `g_div=R/(96pi^2 epsilon F^2)`.

The finite part has a local scheme-dependent multiple of R and a fixed logarithmic residue. In an explicitly fixed-mu dimensional prescription it has the form

`g_ren=(H^2/F^2)[c_scheme+log(mu^2/H^2)/(8pi^2)]`

up to the precise chosen finite subtraction. Its metric derivative cannot treat g as constant or replace it by a scale-independent numerical shape factor without stating the renormalization choice. In particular `H d_H g=2g-H^2/(4pi^2F^2)` for that displayed convention at fixed mu and F.

If `W_corr=g T`, the direct partial metric response is

`rho_corr=[g D T-(H d_H g)T/4]/V`, `D=x d_x+y d_y`.

For coupling differences replace T by its same-radius difference. For matching to an existing full determinant use `T-T_aligned` before differentiating, in the same scheme.

The divergent/local orientation structures are precisely mass times R, electromagnetic orientation times R, and an electromagnetic U-independent curvature term. Their renormalized curvature LECs enter at the same epsilon order as the finite tadpole. A mass-curvature term can survive a charge difference because the tilted `<a0>` differs. No finite numerical choice of Gbar supplies these unknown matched coefficients.

Dynamical photon contractions, other same-order electromagnetic/chiral operators, and possible curvature contacts are omitted here. This is a **first nonconstant-pion source contribution**, not full NLO QCD+QED. The epsilon-regime and fixed-parameter/normalization caveats in the base pretarget note continue to apply; a fixed-positive-mass H->0 limit is not supplied.
