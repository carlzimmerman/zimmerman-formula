# Nonlinear static cutoff modulus: constructive existence and physical tail

For the declared nonrelativistic action and a quadratic modulus potential, a finite stiffness condition gives an actual nonlinear static solution, not only a formal large-stiffness expansion. The solution is unique in the positive bounded decaying class. Its modulus-only energy has a strictly positive Hessian, and its spherical physical force acquires the same leading algebraic tail at any finite stiffness admitted by the theorem. These results neither select the vacuum cutoff nor prove causal or full gravitational health.

## Raw action, domain and theorem

Read the frozen parent REPORT.md and ROOT_FORCE_TAIL.md. Let n≥3, Ω_(n−1) be the unit sphere area and ΔΦN=Ω_(n−1)G_nρ. Set

κ=a0²/(2Ω_(n−1)G_n)>0,
L=−[2∇Φ·∇ΦN−a0²Q(y²,T)]/(2Ω_(n−1)G_n)−ρΦ−Z|∇T|²/2−V(T),
y=|∇ΦN|/a0,
Q(y²,T)=y²+q(y,T),
q(y,T)=2∫0^y t b(t)/[1+(t/T)²]dt,
b(t)=√(1+1/t)−1,
V=V0+Zm²(T−T0)²/2.

Assume T0,Z,m>0 and a smooth nonnegative compact spherical source on R^n, with nonzero finite mass M. Newtonian y is bounded, continuous (locally Lipschitz), tends to zero and outside the body equals (rM/r)^(n−1), rM=(G_nM/a0)^(1/(n−1)). A finite smooth source is used for existence; a point-source self-energy is not needed. The density is prescribed: this boundary-value problem does not establish a self-gravitating matter equilibrium or a compact static dust body. The first two varied equations remain ΔΦN=Ω_(n−1)G_nρ and ΔΦ=div[ν(y,T)∇ΦN], ν=1+b(y)/[1+(y/T)²]. The modulus equation is

(−Δ+m²)u=(κ/Z)q_T(y,T0+u),  u=T−T0→0 at infinity.

**Theorem.** If

L*=3κπ/(2Zm²T0)<1,

there is a unique solution u in C0(R^n) with positive T, necessarily

0≤u≤B*=κπ/(2Zm²).

It is nonzero and strictly positive for a nontrivial source. It has local classical elliptic regularity and lies in H¹∩L¹. The modulus-only relative energy is strictly minimized by this solution on its nonnegative H¹ cone. The theorem does not assert uniqueness for arbitrary smaller stiffness, nor positivity of the full two-potential gravitational action.

Dimensions are consistent in every n: κ is energy/L^n, Z is energy/L^(n−2), m has inverse-length units, and B*,L* are dimensionless. The dimension dependence enters κ through sphere/G_n normalization, not the universal kernel inequalities below.

## Uniform bounds, independently derived

c_T(t,T)=∂T[ b(t)T²/(T²+t²) ]=2Tt² b(t)/(T²+t²)²>0.

Since b(t)=1/[t(√(1+1/t)+1)]≤1/(2t),

0<q_T(y,T)=2∫0^y t c_T dt
 ≤2T∫0∞t²/(T²+t²)²dt=π/2.

The upper bound is strict at finite positive y,T, but the non-strict uniform bound is convenient. Equivalently q_T≤2C′(T)≤π/2, C=∫y(ν−1)dy. This integral is a response convention, not a newly derived covariant vacuum stress.

The exact logarithmic derivative is

(∂T c_T)/c_T=(t²−3T²)/[T(T²+t²)]∈[−3/T,1/T].

Thus |q_TT|≤3q_T/T≤3π/(2T0) for T≥T0. A second endpoint bound uses b(t)≤t^−1/2:

q_T(y,T)≤8y^(7/2)/(7T0³),  T≥T0.

Consequently q_T is bounded by h(x)=min[π/2,8y(x)^(7/2)/(7T0³)], which lies in C0∩L¹∩L²: its exterior decay exponent k=7(n−1)/2 exceeds n because k−n=(5n−7)/2>0. There is no divergent center source for the smooth body.

## Constructive fixed point and uniqueness

For all n, use the positive massive Green function through its heat representation

G_m(x)=∫0∞e^(−m²s)(4πs)^(-n/2)e^(−|x|²/(4s))ds.

Gaussian integration gives ∫G_m=1/m², and distributionally (−Δ+m²)G_m=δ by integrating the heat equation in s. Define the closed complete C0 box 0≤u≤B* and

A[u]=(κ/Z)G_m*q_T(y,T0+u).

The source bound gives A[u]≥0 and ||A[u]||∞≤B*. Its forcing is continuous and tends to zero; convolution with the L¹ kernel maps C0 to C0, as follows by splitting its small tail and using uniform continuity. The mean-value bound gives

||A[u]−A[v]||∞≤L*||u−v||∞.

Starting u0=0, the Picard differences obey ||u_(j+1)−u_j||∞≤(L*)^j B*. The series converges uniformly to a fixed point, with certified abstract error ≤B*(L*)^j/(1−L*) after j iterations. This directly supplies the contraction existence proof without turning sampled iterations into a theorem. Any two box fixed points differ by at most L* times their difference, hence coincide. Strict positivity follows from the positive Green kernel and the source being positive on a set of nonzero volume.

A positive bounded classical solution with u→0 is automatically in this box. A negative minimum, if present, is attained since u→0 and satisfies (−Δ+m²)u≤m²u<0, contradicting the nonnegative source. A positive maximum satisfies (−Δ+m²)u≥m²u while the source is ≤κπ/(2Z), so u≤B*. Nonzero extrema are attained at finite points; weak solutions can be bootstrapped as below before this comparison. A bounded homogeneous C0 solution of the massive operator is zero by the same extremum argument, so a classical solution equals the Green convolution. This extends uniqueness from the chosen box to all positive bounded decaying classical solutions, under the strict stiffness condition only.

Regularity is not inferred from continuity of the forcing alone. The heat representation gives ∇G_m in L¹, using ||∇heat_s||₁≤√[n/(2s)] and integration in s. Thus u and ∇u are continuous. The composite q_T(|∇ΦN|/a0,T0+u) is locally C¹ even at Newtonian-field zeros: its y derivative vanishes there as y^(5/2), removing the norm cusp. Local second-derivative Green integrals can be defined by subtracting the forcing value at their singularity; the C¹ forcing makes the residual O(|x−x′|), which is locally integrable against the |x−x′|^−n kernel. This yields local C² regularity and the classical equation. For each integrable convolution kernel K, Cauchy–Schwarz and Fubini give ||K*f||₂≤||K||₁||f||₂. Applying this directly to the L² source with G_m and ∇G_m gives u∈H¹; positivity and the L¹ source bound give u∈L¹. These arguments require the smooth compact source assumption stated above.

## Modulus energy and exact scope of stability

Use the relative functional at fixed ΦN and fixed source,

Erel[u]=∫{ Z|∇u|²/2+Zm²u²/2−κ[q(y,T0+u)−q(y,T0)] }dx.

The subtraction is essential in n=3: the bare isolated MOND q term has a universal logarithmic IR divergence. It does not alter the field equation or Hessian. For u≥0, |q(T0+u)−q(T0)|≤h(x)u, so the H¹ solution has finite relative energy. Its weak first variation vanishes, and

δ²Erel[w,w]=Z∫|∇w|²+∫(Zm²−κq_TT)w²
 ≥Z∫|∇w|²+[Zm²−3κπ/(2T0)]∫w²>0

for any nonzero admissible H¹ perturbation on T≥T0. Integrating this Hessian along a segment establishes a strict global cone minimum, not merely a linear stability sign at one point. For positive-T finite-energy H¹ competitors below T0 on some set, clipping to T0 lowers their gradient and mass energy and also lowers −κ[q(T)−q(T0)] because q_T>0. Thus such competitors cannot improve on the cone minimum. This is reduced static modulus stability only. The QUMOND auxiliary gravitational variational block is not a positive full Hessian, and no covariant kinetic/causal theorem follows from this static stiffness.

## Nonperturbative massive tail and measured spherical force

Rotations of the fixed point solve the same equation because the source and Green kernel are spherical; uniqueness therefore makes u radial. The existence theorem gives u(r)→0 at fixed finite parameters. Therefore the exact nonlinear forcing has

q_T(y,T0+u)=8y^(7/2)/(7T0³)[1+o(1)]

at large r. Positivity and the massive Green convolution then imply

u_modulus(r)≡u(r)=8κ y^(7/2)/(7Zm²T0³)[1+o(1)].

A useful direct proof splits the convolution displacement |z| at √r. On the inner part y(r−z)/y(r)→1 uniformly and T(r−z)→T0, giving forcing ratio→1. On the outer part bounded forcing times the exponentially decaying kernel is negligible relative to r^−k. Exponential integrability follows already from the heat formula: for a<m/√n, ∫e^(a|z|)G_m(z)dz≤2^n/(m²−na²). Hence the convolution ratio tends to ∫G_m=1/m². Compact core sources do not remove the algebraic particular tail. This proof uses finite stiffness, not a 1/Z expansion, and retains only the leading asymptotic coefficient; no unjustified higher-order remainder is claimed.

For a regular compact spherical body, integrating the **actual varied** Phi equation gives

r^(n−1)[Φ′−ν(y,T(r))ΦN′]=constant=0.

The center flux vanishes, so the physical acceleration is exactly g=ν(y,T(r))gN. Spatial gradients of T have not been dropped: the differentiated flux includes ν_T T′ as required. Phi is globally a weak potential with continuous gradient; at a Newtonian-field zero the usual deep-MOND force may be only Hölder continuous, so a smooth global Phi is not asserted. In n=3 its potential grows logarithmically at infinity, with the usual additive gauge freedom.

Compare the same source at vacuum cutoff T0. Since ∂Tχ=2y^(3/2)/T0³[1+o(1)],

Δg=a0 y[χ(y,T0+u)−χ(y,T0)]
 =16κa0 y^6/(7Zm²T0^6)[1+o(1)]
 =8a0³ y^6/[7Ω_(n−1)G_nZm²T0^6][1+o(1)]>0.

Thus the modulus decays as r^−[7(n−1)/2] while the physical correction decays as r^−[6(n−1)], namely r^−7 and r^−12 in n=3. This strengthens the parent's leading-stiffness tail to a finite-stiffness result in the proven contraction regime. The correction remains subleading to deep MOND and supplies no selected a0, T0, V0 or 32π.

## Bounded evidence

checks.py verifies the exact global bounds, dimensions/normalizations, Green mass, derivative identity and physical flux reaction. A positive smooth compact radial test source is iterated at two finite grids as a reproducibility/control example only; its finite-domain quadrature is not a continuum PDE certificate. The analytic contraction proof supplies existence, uniqueness and its abstract error bound. Three controls claim arbitrary stiffness contraction, pure Yukawa tail, or omit the T-gradient reaction; they must fail. The script and parent scientific inputs are pinned in bounded standard-runner manifests. No peer/global files or git state are modified. Primary source anchors are the already authenticated parent NR action; no full relativistic result or novelty claim is imported.
