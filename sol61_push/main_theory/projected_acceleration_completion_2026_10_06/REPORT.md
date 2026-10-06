# Projected relative acceleration: a changed covariant operator

This construction avoids two specific problems of the earlier difference-connection interaction: its critical source slope does not cancel tensor derivatives, and the eliminated norm-cube interaction has a genuine C2 extension at zero. It does **not** establish a healthy scalar completion. In fact the shared clock cancels from the quadratic interaction at coincident metrics. No coefficient, including 32pi, is selected.

## 1. Actual action and domain

Use signature −+++ in d=n+1, n≥3, standard Einstein curvature sign and K=1/(16πG_EH)>0. The shared scalar θ has a timelike gradient for both metrics throughout the admitted patch. Define

X_g=−g^{μν}θ_μθ_ν>0, Nθ,g=X_g^(−1/2), u_gμ=−Nθ,g θ_μ,

P_g^{μν}=g^{μν}+u_g^μu_g^ν, a_gμ=u_g^ν∇^g_νu_gμ,

with corresponding hatted quantities. The new invariant is

Aμ=a_gμ−a_hatμ,
I=(P_g^{μν}+P_hat^{μν})AμAν/(2a0²).

Both projectors are positive semidefinite on covectors, with their common kernel spanned by dθ. Hence I≥0. The explicit exchange-symmetric action is

S=K∫[√−g R+√−hatg Rhat]+2Kχ_n a0²∫v M_eff(I)+S_m[g]+S_hat[hatg],

χ_n=(n−1)/[2(n−2)], v=(|g||hatg|)^(1/4).

Here a0 is inverse-length geometric acceleration (physical a0/c²); M_eff is a declared function on I≥0. This changes the covariant operator from the earlier averaged difference-connection scalar. It is not an assertion that the two theories agree dynamically. Exchange sends A→−A; monotone relabeling θ→f(θ) leaves u and a invariant. Matter is minimally coupled to its own metric and has no explicit θ coupling, so each matter stress obeys its own covariant conservation law on matter equations.

## 2. Exact ADM identity and variations

In θ=t coordinates write g with lapse N, spatial metric γ and shift S^i, and hatg with lapse L, spatial metric hatγ and shift R^i. Direct normalization gives u^μ=(1/N,−S^i/N), P^{00}=P^{0i}=0 and P^{ij}=γ^{ij}. The acceleration covector has

a_i=∂i lnN, a_0=S^i a_i.

The time covector component must not be discarded. It drops out of I because the projector has zero time row. Therefore exactly

I=H^{ij}∂i r∂j r/a0²,
H^{ij}=(γ^{ij}+hatγ^{ij})/2, r=ln(N/L).

There are no lapse or shift velocities, no shift dependence, and no spatial-metric velocities in this interaction. A naive Lorentz contraction of C*u*u is a different object and fails positivity even on homogeneous lapse histories.

Holding spatial metrics fixed, the interaction lapse Euler derivatives are

EL_N=Kχ_n/N [a0²v M_eff−4∂j(v m H^{ij}∂i r)],
EL_L=Kχ_n/L [a0²v M_eff+4∂j(v m H^{ij}∂i r)], m=M_eff,I.

The volume terms are essential. Spatial-metric variation also varies H and v; they cannot be omitted from full equations. Interaction shift variation is zero, leaving the Einstein momentum variation rows unchanged. This fact alone does not determine their preservation, the full Dirac classification, or scalar health.

For a covariant clock variation at fixed metrics,

δu_gμ=−Nθ,g P_gμ^ν ∂νδθ,
δa_gμ=δu_g^ν∇νu_gμ+u_g^ν∇νδu_gμ,
δP_g^{μν}=δu_g^μu_g^ν+u_g^μδu_g^ν,

δI=(δP_g+δP_hat)^{μν}AμAν/(2a0²)+2P_avg^{μν}AμδAν/a0².

Together with δθS_int=2Kχ_n a0²∫v m δI these specify the actual clock Euler equation after integration by parts, rather than treating θ as an imposed background. Diagonal diffeomorphism invariance implies that, on both metric and matter equations, the clock equation follows since dθ≠0; this Noether relation does not establish that the clock is nondynamical or healthy.

A useful direct static check: for zero-shift stationary metrics θ=t+π, δa_i=−∂i πdot for each metric, independently of its lapse and spatial metric. Thus δA_i=0. Also δP^{ij}=0 and A_0=0 on that background, so δI=0. The stationary clock choice is an admitted first-variation branch, not merely an externally fixed field.

## 3. Actual stationary source normalization

In the leading pressureless weak stationary branch N=1+φ, L=1+hatφ, the invariant becomes |∇φ*|²/a0², φ*=φ−hatφ. Explicit spatial-metric variations of the interaction are quadratic in weak gradients, not leading linear spatial Einstein forcing; the usual leading GR conformal spatial potentials are admitted. Cosmological curvature from the constant interaction is neglected only in this local NR limit.

With Ω_(n−1) the unit sphere area, the physical Newton coupling is

G_N=8π(n−2)G_EH/[(n−1)Ω_(n−1)].

Then 2Kχ_n=1/(2Ω_(n−1)G_N), and the reduced Lagrangian is

L_NR=−[(∇φ)²+(∇hatφ)²]/(2ΩG_N)+a0²M_eff(x²)/(2ΩG_N)−ρφ−hatρhatφ,
x=|∇φ*|/a0.

Its actual variations give

Δφ=ΩG_Nρ+div[m∇φ*],
Δhatφ=ΩG_Nhatρ−div[m∇φ*],
div[(1−2m)∇φ*]=ΩG_N(ρ−hatρ).

For spherical/aligned fields with hatρ=0 and a regular source-selected flux, y=g_N/a0=(1−2m)x and g/a0=(1−m)x. This recovers the same **radial constitutive law** as the earlier symmetric source dictionary if the same M_eff is chosen. It does not recover nonspherical QUMOND: the weighted star field need not be curl free. The earlier external-field/multipole QUMOND observables cannot be transferred automatically.

For the displayed local deep example M_eff=−A+I/2−I^(3/2)/12+…, m=1/2−x/8+…, so y=x²/4+… and g/a0=x/2+…=√y+…. The cubic coefficient defines the operational a0 normalization. This local series is not a globally complete high-acceleration kernel. One may instead inherit an admitted positive-I envelope from the parent radial construction; its extra constitutive parameters remain inputs. Flowing clocks, nonstationary sources and generic metrics require the full varied equations, and their physical force must not be identified silently with clock acceleration.

## 4. Tensor and eliminated-action regularity tests

With homogeneous clock and spatially homogeneous lapses, ∂i r=0 and I=0 for arbitrary homogeneous scale factors. It remains zero for a pure TT spatial perturbation with homogeneous lapses. Thus the interaction contributes **no TT derivative block**, regardless of the critical value m(0)=1/2. At a coincident on-shell FRW vacuum the constant interaction's volume quadratic cancels the usual Einstein background curvature mass as in an ordinary cosmological constant. Geometric-mean and individual volume second variations agree for traceless TT perturbations at coincidence. Writing h=s+d/2, hat h=s−d/2 gives

S_TT²=K∫a^n [1/2 tr(sdot²−a^(−2)(∇s)²)+1/8 tr(ddot²−a^(−2)(∇d)²)].

Both tensor derivative coefficients are positive and propagation is luminal on the coincident metric. There is no inherited connection-invariant H*d*ddot term. This is a tensor statement, not whole-action health.

On compact patches of the common-timelike-clock domain, the ADM spatial matrix H is uniformly positive and has a smooth Cholesky factor. Hence I=||B||² with B a smooth function of field jets, and I^(3/2)=||B||³ is C2 at every zero. For a fixed positive matrix P the Hessian is

3√Q P+3(Pv)(Pv)^T/√Q, Q=v^TPv>0,

and its norm is O(|v|), extending to zero there. Smooth composition includes metric dependence. This avoids the nonzero-null obstruction of an indefinite quadratic form, where dQ≠0 on Q=0 and the corresponding |Q|^(3/2) Hessian diverges. It is not C3 in general, nor uniformly elliptic at zero: the cubic Hessian vanishes.

This regularity applies to the **eliminated envelope** chosen as M_eff. It does not regularize the original joint auxiliary function at T=0. The inherited stationary auxiliary solution T_min~I^(7/8)=||B||^(7/4) is C1 but not C2 at zero, and mixed/order-limit questions of an uneliminated action remain separate.

## 5. Sharp scalar limitation and vacuum coefficient

When g=hatg, a_g=a_hat for any clock θ. The interaction is exactly independent of θ on this coincidence slice. Around double Minkowski with θ=t+π and lapse perturbations ν,hatν,

δa_g,i=∂i(ν−πdot), δa_hat,i=∂i(hatν−πdot),
δA_i=∂i(ν−hatν).

The common-clock perturbation cancels from the entire quadratic interaction. The same cancellation holds on a common FRW background. Consequently this action supplies no positive quadratic clock kinetic coefficient there. It would be incorrect to infer full scalar health from its ADM absence of lapse velocities, or to import a single-metric khronon stability theorem. An extra nonlinear constraint could matter; a full scalar constraint/principal-symbol calculation and sourced foliation admission are the first missing physical implications. Extrinsic-curvature operators might change this result but would be additional operators with their own cosmological/source consequences.

For coincident vacuum, I=δI=0 and M_eff(0)=−A. The same action gives

Λ/a0²=χ_n A/2,
H²=χ_n a0² A/[n(n−1)].

The clock equation gives no condition fixing A on this branch. If UV normalization of the same inherited envelope sets A=2C_resp(λ), that conditional endpoint dictionary survives; it does not choose λ or C_resp. The new operator improves a specific tensor and regularity leaf while leaving both coefficient selection and complete scalar dynamics open.

## 6. Primary-source scope and computation

Blanchet–Marsat (2011), eqs 2.1–2.9 and 3.2–3.4, supply the single-metric normalized foliation acceleration and its ADM D_i lnN identity. Their stationary MOND limit (eqs 4.5–4.8) is known prior work, with independent low/high acceleration constants. Our two-metric relative-projector action is a changed operator, not their established theory. [Primary journal PDF](https://www2.iap.fr/users/blanchet/images/PhysRevD.84.044056.pdf).

Flanagan v3 (2023), Secs 3–4, derives the single-metric slow-motion limit and sufficient stationary deep-MOND khronon stability in spherical, cylindrical and planar settings, subject to the stated matter/background conditions. It also finds nonstationary clock corrections. These hypotheses do not cover the shared-clock relative interaction above. [Exact primary version](https://arxiv.org/pdf/2302.14846v3).

checks.py verifies exact ADM projectors/exchange, generic lapse EL, the displayed radial deep normalization, norm-cube derivatives, clock cancellation and positive EH relative TT coefficient. It does not simulate a sourced relativistic solution or prove scalar well-posedness. Three declared negative controls reject a naive indefinite C*u*u invariant, inherited critical tensor cancellation and an unjustified positive quadratic common-clock kinetic claim. Frozen standard manifests and authoritative counts are in RUNS.json; the report is an execution input, so run summaries are kept separately.
