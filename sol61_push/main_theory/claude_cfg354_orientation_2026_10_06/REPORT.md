# Building on CFG354: an affine-invariant orientation reader has a variational cost

The proposed third-derivative orientation rule reads `g/r` on every exact flat spherical jet and rejects ideal cylinders and planes. It removes CFG354 T3's uniform-external-acceleration tilt. However, this exact rule is discontinuous at otherwise smooth, positive-density jets. A smooth threshold function alone does not fix that defect. Away from the discontinuity, its source variation has a generic derivative-of-delta layer at a sharp edge, scaling as `1/w²`; CFG354's Hessian-only layer scales as `1/w`. These are explicit obstructions for this reader/action, not a no-go for every higher-derivative discriminator.

## Inspected Claude inputs and distinction from CFG355

The frozen CFG354 commit is `bd5ab6223de96b33d0a2419227ef6c5273f89151`. Actual inspected HEAD was `3f59dab1bec9d533a4dceed0f48c039ac05cce87`, including CFG354's results at67b8311c5 and CFG355's frozen rank-veto criteria. The current CFG354 Python source, README and frozen criteria are pinned in the authoritative run manifest. They define `psi=Phi_d/(4piG rhobar)`, `H=Hessian psi`, and T3 as the smaller Hessian eigenvalue transverse to **grad psi**. Source was read without importing/executing it. The new rule below uses derivatives of H instead of grad psi; it was not one of Claude's frozen/scored rules and inherits no host, growth, fidelity or data passes.

CFG355 changes the premise differently: T1 times a cold velocity-dispersion rank veto. That introduces genuine velocity/stream state and is outside a density-only discriminator. Its frozen criteria, inspected but not executed, are also pinned. Its exact-rank regularity obligation is discussed below; its numerical/data result was not available in the inspected commit and is not inferred here.

## Definition on a flat leaf

Put `Tijk=partial_i Hjk`, `vi=Tijj=partial_i Delta psi`, and `Mij=Tikl Tjkl`. If v is nonzero choose the unoriented axis `n=v/|v|` and read

`R(H,T)=min_{|e|=1,e perpendicular n} e^T H e`.

If v=0 but T is nonzero, take the maximal-eigenvalue eigenspace E of M, and minimize the same projected reader over all unit n in E. If T=0 use `lambda_min(H)`. Sign of n is immaterial. If dim E>=2 this minimization is simply `lambda_min(H)`: every unit e has a nonzero perpendicular vector in E. For dim E1 it is the ordinary transverse projection.

The construction is invariant under rotations and under `psi -> psi+C+B_i x_i`, since H and T are unchanged. This affine invariance statement concerns the intended Euclidean leaf model. A full curved-leaf covariant action must define covariant derivatives, commutator terms, metric variation and its boundary/mean constraints; these are not authenticated by the flat calculation. In the normalized psi convention H is dimensionless, T and v have inverse-length units, M inverse-length². No target coefficient or new physical scale is assigned.

## Exact spherical and translational controls

For a sphere with `g=psi'(r)`, `n=rhat`, `P=I−nn`,

`H=g' nn+(g/r)P`,

`T=g'' nnn+b[n_iPjk+n_jPik+n_kPij]`, `b=(g'−g/r)/r`.

Direct contraction gives

`v=(g''+2b)n`, `M=2b² I+g''² nn`.

If v!=0 its axis is radial. If v=0 and T!=0 then g''=−2b!=0 and M has a unique radial maximal axis. If T=0 then b=g''=0, so H is isotropic. All three branches therefore give exactly `R=g/r`, for arbitrary smooth spherical profiles at r>0. This includes points where the density gradient vanishes; using v alone would miss them.

For a cylinder let n be its transverse radial direction and t its transverse tangent, with z axial. Then `H=g' nn+(g/r)tt`, and the nonzero tensor entries in `(n,t,z)` are `Tnnn=g''` and the three permutations of `Tntt=b`. Hence

`v=(g''+b)n`, `M=diag(g''²+b²,2b²,0)`.

When v!=0 the axial zero lies in the projection, so R<=0 for a positive-source cylinder. When v=0 and T!=0, `g''=−b` and E is the full transverse plane, giving `R=lambda_min(H)<=0`. Uniform-density interior has T=0 and H=`diag(c,c,0)`, so R0. An exterior cylinder can give a **negative** reader rather than exactly zero; rejection at a positive threshold is the correct statement. Planes have `H=diag(psi'',0,0)`, `T111=psi'''`, so every branch again gives R<=0. FRW overdensity H=T0 gives R0.

These are geometric controls, not phase-space ownership. Identical instantaneous density and its derivatives do not determine whether streams are approaching, departing or bound relative to a specified host. The independent bulk-phase audit is in `../claude_cfg355_bulk_phase_2026_10_06/REPORT.md`; no phase-information claim is added by this orientation rule.

## A compactly supported continuity counterexample

Take c>tau>0 and a smooth bump chi equal to1 on an open ball U. Perturb a uniform-cylinder potential by

`psi_epsilon=c(x²+y²)/2+epsilon z³ chi(x,y,z)/6`.

Inside U, at epsilon0, H=`diag(c,c,0)`, T0 and R0. For **every** nonzero epsilon, v=`epsilon ez`, and projection onto the xy plane gives R=c throughout U, even though `Hzz=epsilon z`. The perturbation tends to zero in every fixed finite smooth norm, has compact support, and its Poisson source perturbation integrates to zero. The total source stays positive in a sufficiently small ball; if a globally nonnegative total matter density is required, a finite background can cover the bounded compensating bump shell. The same example can be placed on a periodic leaf and its mean potential removed without changing H or T.

Choose the independent MOND-sector density B=Nsqrt(h)L_MOND supported in U and nonzero. Even replacing the sharp gate by a smooth function F with `F(c−tau)!=F(−tau)`, the reduced term `integral B F(R−tau)` has a finite nonzero jump as epsilon tends to zero. This is an action-level discontinuity on admissible small source perturbations, not just a pointwise ambiguity on a measure-zero surface. Therefore the proposed exact reader has no ordinary first variation on this domain. The M fallback at v0 does not cure the branch jump. One can smooth/blend the orientation selection, but its defining functions, scale/domain assumptions and full action reaction must then be supplied and retested.

## A restricted continuous-local-reader impossibility

There is also a precise limitation independent of this particular fallback. Assume a continuous local function F(H,T) is required to equal g/r on **every** spherical jet at **every** radius R>0, and to give a value <=0 on the positive uniform-cylinder jet `H=diag(c,c,0),T0`. Fix c>0. At a spherical point whose radial axis is z, choose

`g=cR`, `g'=0`, `g''=2c/R`.

Then H is exactly `diag(c,c,0)`, b=−c/R, v0, and every component of T tends to zero as R tends to infinity. These are smooth local spherical jets, for example supplied near R by `g_R(r)=cR[1+(r/R−1)²]`. Their required spherical response is c at every finite R. Continuity therefore forces F at the limiting cylinder jet to equal c, contradicting rejection. Consequently the all-radius, exact-sphere/ideal-cylinder specification cannot be implemented by a continuous local F(H,T).

This theorem is about the stated Euclidean all-radius jet specification. A finite weak-metric domain, an upper physical radius, a nonlocal orientation datum or an approximate spherical response changes its premises. It is **not** an all-physical-galaxy or all-third-derivative-reader no-go. The large-R jets need not lie in a chosen globally weak gravitational domain. Higher source/clock scales could restrict that domain, but must be declared; they are not automatically selected by this argument.

## Exact smooth-branch variation and a stronger sharp layer

On a v!=0 branch, suppose the projected smaller eigenvalue is simple, with minimizing unit vector e perpendicular n. The constrained eigenvalue equation is `H e=R e+mu n`, where `mu=n^T H e`. Differentiating its norm and orthogonality conditions gives

`delta R=e_i e_j delta Hij−2mu e·delta n`,

`delta n=(I−nn)delta v/|v|`, hence

`delta R=Pij delta Hij+A_i delta v_i`,

`Pij=e_i e_j`, `A_i=−2(n^T H e)e_i/|v|`.

Since `delta v_i=partial_i Delta delta psi`, the fixed-metric source-adjoint variation of `E=integral B F(R−tau)` is

`E_psi=partial_i partial_j[B F' Pij]−partial_i Delta[B F' Ai]`.

Under `Delta psi=delta`, eliminating the Poisson auxiliary on a flat periodic/decaying leaf gives, modulo the zero mode,

`E_delta=Delta^-1 partial_i partial_j[B F' Pij]−partial_i[B F' Ai]`.

Thus the third-derivative orientation piece has an **exact local order-one** source reaction. Its Fourier source symbol grows as |k|; unlike CFG354's Hessian Riesz symbol, it is not order0. No time derivatives of this auxiliary have been introduced, so this does not by itself establish an Ostrogradsky degree of freedom. It does establish a new spatial-regularity/force obligation. Actual lapse weight N is included in B; the previously audited weighted auxiliary adjoint changes lower terms/mean normalization, not this local derivative order. Metric and cold-state variations remain additional obligations.

Let s be proper normal distance to a regular gate surface, `R−tau=kappa s+O(s²)`, kappa>0. With a sharp step, the orientation term contains

`−[B A·ns/kappa] delta'(s)`

plus delta and less singular terms. For a width-w Gaussian approximation to delta(s), its derivative has exact maximum `sqrt(2/e)/(sqrt(pi) w²)`. If A·ns!=0, this matter-potential layer is unbounded as1/w². The Hessian-only reaction can have an order1/w layer and cannot cancel this higher-order distribution generically. Vanishing A·ns removes this leading term but does not prove complete regularity.

## Explicit constant external-tide witness

In local dimensionless units choose `psi_sphere=r³/3`, point `(0,0,1)`, and a constant trace-free tide with `Hxx=-.1`, `Hyy=.1`, `Hxz=.2`. This tide has zero T and zero source trace. At that point

`H=[[.9,0,.2],[0,1.1,0],[.2,0,2]]`, `v=4ez`, `e=ex`, `R=.9`,

`A=-.1 ex`, `grad R=(-.4,0,1)`, `A·grad R=.04`.

The angular derivative −.4 is the rotation of the radial projection plane under the fixed external tide. Setting the threshold to this local reader value locates a regular edge with nonzero A·normal. The witness is unaffected by adding any uniform gradient to psi. It shows that affine invariance does not remove the sharp reaction caused by a tide. It is a local action-variation witness, not a fitted cosmological host profile.

For B1 the frozen leading orientation layer peaks are1.66876,6.67505,26.70022,106.80087 at widths .1,.05,.025,.0125: halving width multiplies the peak by4. The derivative formula is also checked against independent finite differences of the projected eigenvalue, which give −.1 for variation of vx. The layer numbers implement the exact local leading distribution; they are not an integration of a complete galaxy force equation.

## CFG355 exact-rank obligation, kept separate from its scored experiment

Its frozen `V=1−[rank sigma_c==2]` reads extra cold-state information, and therefore does not fall under the density-only restriction. But exact rank is discontinuous: `sigma_epsilon=diag(1,1,epsilon²)` has V0 at epsilon0 and V1 for every nonzero epsilon. This can be realized by adding an arbitrarily small out-of-plane stream-velocity component while retaining positive stream weights. A smoothed T1 gate alone does not regularize that rank jump.

The frozen identities `sigma adj(sigma)=det(sigma)I` and the rank1 polynomial identity are valid, and exact rank is unchanged by invertible congruence. They explain why **metric-congruence tangent variations** can have zero rank-switch stress. They do not establish differentiability under independent cold stream/weight variations. In particular, pulling `delta(det sigma)` back through stream velocities at a rank2 state gives a determinant proportional to epsilon²; the zero is not a regular level set, so the ordinary distribution chain rule cannot be assumed. Rank-preserving metric stress is not the entire Vlasov/action reaction.

The numerical rank tolerance in the frozen criteria needs its actual definition and smoothing interpretation. Numerical rank is generally not invariant under unrestricted invertible congruences with badly conditioned factors; exact rank is. A continuous state gate could replace the exact veto, but its velocity-scale threshold, response width and reactions would be new mathematical/physical inputs. This note does not prejudge CFG355's scored results and does not duplicate its run. The root's separate fixed-host bulk-phase construction asks a different question: even all central moments can miss coherent motion relative to a fixed host.

## Evidence and remaining implication

Authoritative `runs/main_d` passes39 checks. Three deliberate negative controls fail respectively the old gradient affine-invariance claim, the false continuity claim, and the false bounded-layer claim; all four current manifests validate. Exact symbolic tensor contractions and analytic variation/layer proofs provide the universal implications; finite tests do not substitute for them. No Claude script was executed or changed.

Historical a failed before a result because SymPy arrays do not expose subs; b failed because initialized zero entries were Python integers. Exact historical source copies and raw logs are retained. c was a successful narrower pre-limit run. The authoritative d run adds the declared all-radius controls; current script/contract hashes supersede c. The original a contract also misstated NumPy version; current contract records measured1.26.2. Historical records are not advertised as fresh current evidence.

The next substantive implication is a **continuous** orientation/state gate with declared domain/scale assumptions and its full sourced variational reaction. Smoothing only the final step leaves the explicit orientation discontinuity. Smoothing the selector might repair it, but exact all-radius sphere recognition versus cylinder rejection must then be weakened or supplemented by nonlocal/domain information, and the spatial order-one reaction must be controlled. Geometry remains a classifier rather than a substitute for phase-space binding/turnaround information.
