# Algebraic conserved stress sources cannot independently weaken vacuum coupling

**Result.** On a connected open domain of symmetric stresses, any `C1` local Lorentz-covariant algebraic map `H(T,g)` which is symmetric and conserved for **every conserved stress first jet** has the form

`H_mu_nu = a T_mu_nu + b g_mu_nu`,

with constants `a,b`. At fixed theory parameters, the vacuum slope is `dH(-rho_E g)/d rho_E=-a g`; choosing `b` can cancel one vacuum height but does not change that coupling slope. This holds for every spacetime dimension `d>=2`, hence the requested `d>=3`. No invariant-polynomial ansatz or second differentiability is needed. It rules out replacing the vacuum's coupling by `G` while keeping the measured dust/Newton coupling `8piG`, within this source-only algebraic class. It is not a no-go for all modified gravity or all physical matter models.

A trace-compensating cosmological field cancels the attempted unequal trace coupling and restores the universal source plus an integration constant. That constant can absorb a vacuum shift if its boundary data are changed or left free; conservation does not fix it or determine a MOND scale.

## Scope and overlap

Requested/start base: `310f0d1a46ca858e9a63cf37f699f10baa07ad3d`; actual input/run revisions and hashes are recorded separately. The nearest `HORIZON_SHARING_RESULTS.md` obstructed a specific acceleration-dependent curvature lift by its nonexact Bianchi one-form. `galaxy_coefficient_bridge.py` compared bare and conditionally relaxed Newton calibrations. The previous `selection_2026_10_06/vacuum_constraint/REPORT.md` replaced gravitating vacuum shifts by a four-form sector. This report instead proves a **universal local algebraic source classification**, including nonlinear invariant maps, then calibrates its surviving coefficient operationally. It does not repeat an entropy/sphere-area explanation of pi.

Assumptions: (i) Levi-Civita metric; (ii) no extra tensor, preferred observer or separately tracked species input; (iii) no derivatives, curvature, history, nonlocal averages or explicit position dependence in `H`; (iv) symmetric `C1` output; (v) the admitted stresses fill a connected open subset of `Sym²`, and every first derivative compatible with `nabla_mu T^{mu nu}=0` is admitted there. Lorentz equivariance is imposed wherever the domain transforms into itself; an invariant connected domain suffices. Constants may depend on fixed theory parameters, not the local stress. Separate disconnected domains need not have the same constants.

The demand is about **all conserved stress jets**, not merely jets selected by the coupled Einstein equations or a particular restricted matter action. This quantifier is essential.

## 1. Complete proof of the first-jet classification

At a point choose normal coordinates and use contravariant symmetric tensors. Write `V=Sym²(R^d)` and `N=d(d+1)/2`. A first jet is a tuple `J=(S_0,...,S_{d-1})` with `S_mu in V`. Its divergence is the surjective linear map

`B(J)^nu = sum_mu (S_mu)^{mu nu}`.

Surjectivity follows by assigning any prescribed divergence to the row `(S_0)^{0nu}`, leaving the other tensors zero. Formal conserved jets are exactly `ker B`. They are not artificial algebraic states: in Minkowski space `T(x)=T_*+sum_mu x^mu S_mu` realizes each such jet as an exactly conserved local tensor field, remaining in the open domain near the origin.

Fix any stress `T_*` and set `A=DH(T_*) : V -> V`. The conservation hypothesis is

`B composed (Id tensor A)` vanishes on `ker B`.

Because `B` is surjective, there is a unique linear `L:R^d->R^d` such that

`B composed (Id tensor A) = L composed B`.

Indeed define `L(v)` using any jet with `B(J)=v`; two choices differ by an element of `ker B`, so the definition is well-defined and linear. This factorization does not assume Lorentz covariance or classify only a sample of jets.

Take a jet whose sole nonzero tensor is `S_mu=S`. The factorization gives, for **every** symmetric `S` and every row `mu`,

`(A(S))^{mu nu} = sum_e L^nu_e S^{mu e}`,

or in coordinate matrices `A(S)=S L^T`. Since the output is symmetric, `S L^T = L S` for every real symmetric `S`.

Taking the coordinate matrix `S=I` gives `L=L^T`. Consequently `L` commutes with every real symmetric matrix. Commuting with all diagonal matrices makes `L` diagonal; commuting with each elementary off-diagonal symmetric matrix makes every diagonal entry equal. Thus `L=a(T_*)I` and

`DH(T_*)=a(T_*) Id_V`.

The coordinate identity `S=I` here is an allowed contravariant symmetric tensor, **not** a claim that the Lorentz metric is Euclidean. Conservation was written with both stress indices raised, so no hidden metric-sign substitution occurs.

It remains to show that `a` is constant without assuming `H` is `C2`. Choose a coordinate box contained in the domain, with coordinates `t_1,...,t_N` on `V`. The off-diagonal derivative equations say each output coordinate `H_i` depends only on `t_i` in that box: `H_i=f_i(t_i)`. The diagonal derivatives say `f_i'(t_i)=a(T)` for every `i`. For `i!=j`, varying `t_i,t_j` independently forces both one-variable derivatives to be the same constant. Since `N>=2`, this shows that `a` is locally constant. A locally constant continuous function on a connected domain is constant. Integrating the derivative gives

`H(T)=a T+B_0`,

where `B_0` is a constant symmetric tensor. Lorentz equivariance of `H` then requires `B_0` to be Lorentz invariant; the invariant symmetric rank-two tensors are multiples of the metric, so `B_0=b g^{-1}` in raised notation. Lowering indices gives the asserted form.

Conversely this form is conserved whenever `T` is conserved, since `nabla g=0` and `a,b` are constants. The classification is therefore necessary and sufficient under these assumptions. In `d=1`, `N=1` and the integrability step fails: every conserved stress is locally constant, allowing arbitrary functions of its value.

## 2. Trace projectors and nonlinear invariant attempts

For the linear trace projector `H=T-(t/d)g`, where `t=trace T`, conservation gives

`nabla_mu H^{mu nu}=-(1/d)nabla^nu t`.

A smallest concrete witness is the static dust-density jet `partial_1 T^{00}=1`, with all other first derivatives zero in a normal frame. It is conserved, while `partial_1 t=-1`, so the output divergence in direction 1 is `+1/d`. This particular failure already occurs in an ordinary dust family, not only in general anisotropic stress.

More generally `H=A(t)T+B(t)g` has divergence

`A'(t) T^{mu nu} partial_mu t+B'(t) partial^nu t`.

Arbitrary conserved jets permit arbitrary trace gradients. At a generic anisotropic stress the two structures cannot cancel for all such gradients; the general proof above forces constant `A,B`. A nonlinear scalar invariant multiplying the metric also fails unless it is constant on the domain. Quadratic tensor maps such as `T g T` are not saved by Lorentz covariance. Exact controls supply conserved counterjets for `tT`, `trace[(gT)²]g`, and `TgT`, including a paired shear/density jet for the last case.

These failures are consequences of the quantified conservation condition, not evidence that invariant tensors themselves are ill-defined.

## 3. What a trace compensator actually restores

Consider the proposed Einstein equation

`G_mu_nu + Lambda(x) g_mu_nu = a T_mu_nu + b t(x) g_mu_nu`.

Contracted Bianchi and conservation of the same matter tensor require `partial_nu Lambda=b partial_nu t`. Hence on a connected spacetime region

`Lambda=b t+Lambda0`,

and substituting gives exactly

`G_mu_nu + Lambda0 g_mu_nu = a T_mu_nu`.

The apparent bare vacuum coefficient `a+d b` has disappeared as an independent physical coupling. Any nonlinear **pure metric** term `F(T)g`, for a differentiable Lorentz scalar `F`, is similarly removed by a compensator satisfying `Lambda=F(T)+Lambda0`.

If a compensator is specifically a function of trace and one instead writes `H=A(t)T+B(t)g`, its derivative must satisfy `A'T grad t+(B'-Lambda')grad t=0`. Generic stresses and arbitrary trace gradients require `A'=0` and `Lambda'=B'`; again the restored coupling is universal. This does not classify arbitrary compensators for arbitrary nonlinear tensor maps; such maps first require their divergence one-form to be exact, which is an additional integrability condition. A compensator may restrict allowed matter solutions rather than satisfy this condition identically.

For the trace-free geometric equation

`R_mu_nu-(R/d)g_mu_nu = a[T_mu_nu-(t/d)g_mu_nu]`,

Bianchi gives

`partial_nu[(d-2)R/2+a t]=0`.

Writing its constant as `d Lambda0` recovers `G+Lambda0 g=aT`. This reproduces the classical trace-free/unimodular integrability mechanism. Verified primary checks are [Ellis 1306.3021v3](https://arxiv.org/pdf/1306.3021v3), Sec. 3.1, Eqs. (14)–(16), and [Fiol–Garriga 0809.1371v3](https://arxiv.org/pdf/0809.1371v3), Secs. 1 and 4. Both keep matter conservation as a separate required ingredient in the trace-free formulation. No quantum equivalence or automatic boundary selection is invoked here.

For `T=tau-rho_E g`, the restored equation has geometric vacuum term `Lambda_eff=Lambda0+a rho_E`. A vacuum shift can be absorbed by changing the free integration constant, or can leave the trace-free equations unchanged if that constant is not independently fixed. At fixed reconstructed Einstein integration constant, its contribution retains coefficient `a`. These are different boundary prescriptions. Neither supplies a determined small vacuum density or galaxy acceleration scale.

## 4. Calibrating a against measured Newton G in dimension d

Now assume ordinary Einstein geometry with universal coupling `a=kappa_d`. Let `rho_m` be mass density in `d-1` spatial dimensions, `rho_E=rho_m c²`, and define measured `G_N` operationally by the isolated weak radial force

`g(r)=G_N M/r^(d-2)`.

For spacetime `d>=4`, the unit sphere has area

`Omega_(d-2)=2 pi^((d-1)/2)/Gamma((d-1)/2)`.

The Newtonian Gauss normalization is `laplacian Phi=Omega_(d-2) G_N rho_m`. It is a definition in force units, not a decision to call the action parameter Newton's constant.

Independently, trace reversal of `G=kappa_d T`, with static dust `T_00=rho_m c²`, `t=-rho_m c²`, gives

`R_00=kappa_d rho_m c² (d-3)/(d-2)`.

Since `R_00=laplacian Phi/c²` in the weak static limit,

`kappa_d = [(d-2)Omega_(d-2)/(d-3)] G_N/c⁴`.

The Tangherlini mass parameter confirms the same calibration. With the conventional Einstein–Hilbert parameter `G_EH` defined by `kappa_d=8pi G_EH/c⁴`,

`f(r)=1-mu/r^(d-3)`,

`mu=16pi G_EH M/[(d-2)Omega_(d-2)c²]`,

`Phi=-c² mu/[2r^(d-3)]`.

Differentiating this potential reproduces the Gauss result, giving

`G_N=8pi(d-3)G_EH/[(d-2)Omega_(d-2)]`.

Primary normalization checked against [Mougiakakos–Vanhove 2010.08882v2](https://arxiv.org/pdf/2010.08882v2), Sec. 5, Eq. (5.2) and footnote 7. That source uses **spatial** `d` and calls its Einstein–Hilbert parameter `G_N`; here `d` is **spacetime** dimension and the symbol `G_N` is reserved for the measured force coefficient. Translating both conventions matters. Our derivation is independent of the source's mass-symbol naming.

In four dimensions `Omega_2=4pi`, and the calibrated result is `kappa_4=8pi G_N/c⁴`. Thus for mass-equivalent vacuum density

`Lambda_vac=kappa_d rho_E=[(d-2)Omega_(d-2)/(d-3)] G_N rho_m/c²`.

The scalar curvature is `R=2d Lambda_eff/(d-2)`; `R`, geometric `Lambda`, energy density and mass density must not be interchanged. Units are consistent: `[G_N]=L^(d-1)/(mass time²)`, `[rho_m]=mass/L^(d-1)`, so `[G_N rho_m/c²]=L^-2`, whereas `kappa_d rho_E` has the same units. In particular changing dimension does not make `G_N rho_m` a curvature without the `c^-2` conversion.

The source classification remains valid in spacetime `d=3`, but the above force calibration does not: its pressureless `R_00` coefficient vanishes and the Tangherlini inverse-power potential degenerates. There is no division by `d-3` at that dimension. A Newtonian logarithmic-force theory in two spatial dimensions requires its own gravity prescription.

This calibrates an existing Einstein source coupling; it neither derives `a0` nor selects `Lambda c⁴/a0²`. Restoring `32pi` from an independently postulated acceleration-to-density relation would leave that relation as the missing dynamical premise.

## 5. Physical scope, evidence and checkpoint

An open strict energy-condition cone can satisfy the stress-value hypothesis; arbitrary sufficiently local jets can remain inside it near a point. However a given physical matter model may realize only a lower-dimensional stress-value manifold or fewer jets. A single perfect fluid, canonical scalar, fixed-trace radiation or vacuum sector is not automatically covered by the **full classification**. In particular a pure vacuum stress has constant density under conservation, so it admits no nonzero density first jets and cannot by itself enforce this theorem. A regular `C1` extension from a connected open matter domain to a vacuum boundary inherits the same coefficients by continuity. Disjoint or singular sector definitions evade that premise and must be assessed separately.

The trace-projector dust counterjet is stronger in physical scope than a generic invariant classification, but it does not show that every allowed first jet is realized by a single microscopic matter action. No claim of that realization is made.

`checks.py` constructs the exact divergence kernel and all linear `DH` conditions for `d=2,3,4,5`. The admissible derivative space has dimension one in each case, namely the identity map. It tests conserved nonlinear counterjets, the compensator and trace-free reconstruction, independent Poisson/Tangherlini calibration, and dimensional consistency; sphere areas are reported for `d=4..8`. The finite ranks corroborate the proof, not replace its all-dimension argument. Mutation intentionally accepts the trace projector and is required to fail. `runs/main_a` completes with all implemented assertions passing; `runs/control_a` exits 1 and rejects the trace projector in all four tested dimensions. Both standard runner manifests validate against current input and output hashes. They record actual revisions and limits. No failure was used as evidence for a successful assertion.

**Strongest implication:** a universal, local, symmetric, algebraic stress source with conserved matter cannot weaken vacuum coupling independently of the measured ordinary source coefficient. A trace compensation can relocate vacuum information into a free integration constant, but does not create a separately fixed small coupling. To escape, a proposal must supply extra fields/exchange, derivative or nonlocal terms, a genuinely restricted physical stress domain, or a specified boundary prescription. Each changes an explicit hypothesis and needs its own conserved action and measured-force dictionary; none is excluded globally by this theorem.
