# Static sourced clock: exact second variation and a spatial constraint diagnostic

On arbitrary stationary zero-shift metrics, the **pure clock** quadratic action has no time derivatives, pointwise. Its remaining spatial tensor is explicitly computable and depends on the actual relative lapse normalization. On an admitted leading NR spherical source branch it can be elliptic or mixed-sign. This is a fixed-metric clock Hessian, not a metric/matter-constrained instability theorem, a ghost, or a removed clock degree.

## 1. Actual operator, hypotheses and variation convention

Use the parent's exchange-symmetric action

S_int=2Kχ_n a0²∫v M_eff(I),
I=H_projector^{μν}(a_g−a_hat)_μ(a_g−a_hat)_ν/a0²,
H_projector=(P_g+P_hat)/2,
v=(|g||hatg|)^(1/4), χ_n=(n−1)/[2(n−2)].

Both clocks remain timelike. Hold the two metrics and matter fields fixed for this calculation, with g=−N(x)²dt²+γ_ij(x)dx^i dx^j and hatg=−L(x)²dt²+hatγ_ij(x)dx^i dx^j, N,L>0. The shared clock is θ=t+επ(t,x); ε is the expansion parameter. All π jets are arbitrary at a point subject to small ε maintaining the timelike domain. The metrics need not be on shell for the coefficient identity. Sign statements below use a declared leading NR source solution, not arbitrary off-shell metric jets.

Write

G^{ij}=γ^{ij}, F^{ij}=hatγ^{ij}, H^{ij}=(G^{ij}+F^{ij})/2,
n_i=∂i lnN, h_i=∂i lnL, d_i=n_i−h_i,
D^{ij}=N²G^{ij}−L²F^{ij},
B^j=N²G^{jk}n_k−L²F^{jk}h_k,
π_i=∂iπ, π_it=∂i∂tπ.

All second coefficients below mean the coefficient of ε², so the second derivative with respect to ε is twice that coefficient. Let m=M_eff,I evaluated on I_0=H^{ij}d_i d_j/a0². The source envelope is differentiable at the background value; in the annulus used below I_0>0.

## 2. Full normalization, acceleration and projector jets

For the g metric the normalized clock lapse expands as

Nθ=N[1−επ_t+ε²(π_t²+N²G^{ij}π_iπ_j/2)].

Therefore

u_0=−N[1+ε²N²G^{ij}π_iπ_j/2],
u_i=−εNπ_i+ε²Nπ_tπ_i.

The acceleration identity a_μ=P_μ^ν∂ν lnNθ then gives

a_i=n_i−επ_it
  +ε²[π_tπ_it+π_iπ_tt+(1/2)∂i(N²G^{kl}π_kπ_l)+N²π_i G^{jk}n_jπ_k],

a_0=εN²G^{ij}n_iπ_j
  −ε²N²[G^{ij}π_iπ_jt+π_tG^{ij}n_iπ_j].

The hatted expressions replace N,G,n by L,F,h. The relative first spatial acceleration vanishes, but its first time covector component does not:

A_i=d_i+ε²[(1/2)∂i(D^{kl}π_kπ_l)+π_i B^jπ_j]+O(ε³),
A_0=ε B^jπ_j+ε²[−D^{ij}π_iπ_jt−π_t B^jπ_j]+O(ε³).

Projector components needed for the same order are

P_g^{00}=ε²G^{ij}π_iπ_j+O(ε³),
P_g^{0i}=−εG^{ij}π_j+ε²π_tG^{ij}π_j+O(ε³),
P_g^{ij}=G^{ij}+ε²N²(G^{ik}π_k)(G^{jl}π_l)+O(ε³).

These include the time projector and normalization terms. P^{00}A_0² starts at ε⁴, but P^{0i}A_0A_i already contributes at ε² and cannot be omitted.

## 3. Exact cancellation and remaining functional

The first invariant variation is zero. At second order the B terms from 2H^{ij}d_i A_j,2 and from 2P_avg^{0i},1 A_0,1 d_i cancel exactly. The full result is

a0² I_2=(H^{ij}d_i)∂j(D^{kl}π_kπ_l)
 +(1/2)[N²(G^{ij}d_iπ_j)²+L²(F^{ij}d_iπ_j)²].

No π_t, π_tt or π_it survives. This cancellation is pointwise, not an inference from a chosen time boundary or a stationary π ansatz. The measure has no θ dependence, and I_1=0 eliminates the M_eff,II term. Hence, for compact spatial variations,

S_θ,2=2Kχ_n∫dt d^nx C^{kl}(x)π_kπ_l,

C^{kl}=−D^{kl} ∂j[v m H^{ij}d_i]
 +(v m/2)[N²(G^{ik}d_i)(G^{jl}d_j)+L²(F^{ik}d_i)(F^{jl}d_j)].

The derivative includes the spatial dependence of m, v and H. Dropping dm/dx would change the source result. With fixed stationary metrics the pure-clock canonical energy contribution is −L_θ,2, with tensor −C; that sign is not yet the physical constrained gravitational energy. The pure-clock Euler row is a spatial divergence equation, proportional to ∂k(C^{kl}∂lπ)=0. When C is definite it is elliptic in this frozen-metric block; mixed signature or zero eigenvalues have a different principal classification. Coupling to metric constraints can change the physical interpretation.

Matter minimally coupled to g or hatg has no direct θ variation at fixed metrics. This does not authorize freezing matter or ignoring its conservation laws in a coupled perturbation problem. Mixed metric–clock variations, induced metric/matter perturbations and lapse/shift constraint preservation have not been eliminated here. A pure-clock Hessian with no π_t² can still mix with metric velocities. Thus no degree count, temporal instability or ghost follows from this calculation alone.

## 4. Leading NR source branch: an exact local discriminator

In the weak stationary pressureless branch, N=1+φ, L=1+hatφ and γ_ij=(1−2φ/(n−2))δ_ij, with the hatted analogue. Consequently D^{ij}=4χ_n φ*δ^{ij}+higher weak-field terms, φ*=φ−hatφ, H^{ij}=δ^{ij}+higher terms. The leading pure-clock energy is

E_θ,2=2Kχ_n∫[4χ_n φ* div(m∇φ*)|∇π|²−m(∇φ*·∇π)²].

This result is not a function of the force alone: the relative potential value enters. Its constant cannot be discarded as a gauge of the full covariant two-metric action.

For a concrete admitted n=3 local source branch, choose the exact cubic envelope M_eff=−A+I/2−I^(3/2)/12 on the tested small-I range (a smooth high-I completion may be specified separately). Then m=1/2−x/8 and the actual spherical star-flux law is y=(1−2m)x=x²/4. Outside a compact spherical body of mass M, define rM²=G_N M/a0. The exterior leading NR solution has

d(r)=φ*'(r)=2a0 rM/r, x=2rM/r,
φ*(r)=2a0 rM ln(r/r_ref),
J(r)=div[m∇φ*]=d/(2r)>0.

The star flux r²(1−2m)d=a0 rM² is constant and equals G_N M. The total-potential derivative is (φ+hatφ)'=G_N M/r², while φ'=(1−m)d and hatφ'=−m d. Thus these are actual solutions of the declared leading NR radial equations, not an imposed MOND force inserted into a clock calculation. They are used on a bounded weak-field exterior annulus with x≤1 and small a0rM. No global logarithmic-asymptotic metric, source equilibrium or full covariant sourced solution is claimed.

Let l=ln(r/r_ref). The tangential and radial coefficients of E_θ,2, excluding its positive overall factor, are exactly

E_t=d²(2l), E_r=d²(2l−m).

For l<0 and m>0 both are negative; the frozen clock spatial row is definite and elliptic, albeit with a negative pure-clock canonical energy sign. With no time kinetic term that sign alone is not a ghost criterion. For 0<l<m/2 the radial coefficient is negative and the tangential one positive, giving a mixed-sign spatial principal row. For l>m/2 both are positive; l=0 and l=m/2 are degenerate boundaries. These signs are the leading NR diagnostic, not a full relativistic stability classification.

For example x=1/2 gives m=7/16. Then l=−1 is negative definite, l=1/8 is mixed-sign, and l=1 is positive definite. Strict signs persist in sufficiently weak metrics away from those transition boundaries, conditional on admitting full backgrounds with the same local limit. Changing r_ref leaves all leading radial source forces unchanged but changes this clock block. The NR source equations alone therefore do not determine its ellipticity class. Global relative-clock normalization, metric constraints and source/vacuum matching are the first missing physical implications.

This is not imported single-metric khronometric stability. Flanagan's narrow symmetric-background sufficient conditions concern a different action and dynamical system; the parent's authenticated primary-source discussion remains the relevant scope warning.

## 5. Evidence and boundaries

checks.py starts from normalized u and a=P∂lnNθ, with generic non-diagonal two-spatial-dimensional metric matrices and arbitrary metric-derivative/clock jets. It checks both normalization orders, spatial/time acceleration and projector jets, the full invariant second coefficient, all time-jet cancellations, and the actual n3 radial flux and m-gradient. The dimension-free index derivation above supplies the general-d claim; a finite matrix test is not extrapolated into a proof.

Three negative controls wrongly discard the time-projector cross, assert a positive time kinetic coefficient, or call the relative-potential shift a gauge of the clock Hessian. Current bounded manifests and their exact counts are in RUNS.json. This closes the pure-clock second-variation calculation while leaving the coupled physical source/constraint problem open. No 32pi selector, dark/cold identity, full clock removal or nonlinear health theorem is asserted.
