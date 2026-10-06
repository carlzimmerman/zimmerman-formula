# Finite local modulus prevents exact source-universal interpolation

## Scope and result
For the fixed-source nonrelativistic action in the frozen parent report, finite positive Z, m, κ and two distinct self-similar compact spherical masses cannot produce one exact physical constitutive function ν*(y) throughout both vacuum exteriors. This is an exact equation obstruction, even if ν* is not the original constant-T kernel. It does not exclude approximate universality, impose an observational bound, or determine a vacuum coefficient. The parent contraction condition supplies actual solutions; the obstruction also applies to any positive bounded radial solutions with T→T0 that exist outside that sufficient condition.

Let n≥3, Ω be the unit sphere area, ΔΦN=Ω Gnρ, rM=(GnM/a0)^(1/(n−1)), and κ=a0²/(2Ω Gn). The parent action gives

(-Δ+m²)(T−T0)=(κ/Z)q_T(y,T),
q=2∫_0^y t b(t)/(1+(t/T)²)dt, b(t)=√(1+1/t)−1,
ν(y,T)=1+b(y)/(1+(y/T)²).

The other potential equation is ΔΦ=div[ν(y,T)∇ΦN]. Regular spherical center boundary conditions remove the flux integration constant, hence the actual force is g=ν(y,T)gN. This retains the T-gradient term in the differential equation. Ordinary bodies are prescribed sources; this is not a proof of matter equilibrium or a relativistic completion.

## Exact two-body contradiction
Choose a normalized nonnegative compact radial profile f, Ω∫s^(n−1)f(s)ds=1, and ρM(r)=M rM^(−n)f(r/rM). Its enclosed fraction Ff(s) is independent of M, and

y(s)=Ff(s)/s^(n−1); in the exterior y=s^(−(n−1))>0.

At any common exterior s, exact universality g/gN=ν*(y) and
ν_T=2T y²b(y)/(T²+y²)²>0
force T1(s)=T2(s)=T(s). This inference needs the entire exterior interval, not finitely many measured accelerations. In scaled coordinates the two modulus equations are

−Z rM_i^(−2)Δ_sT+Zm²(T−T0)=κq_T(y(s),T).

Subtracting them for rM_1≠rM_2 gives Δ_sT=0. Radial harmonicity and T→T0 imply T=T0+D s^(2−n) outside the body. The remaining equation would require

Zm²D s^(2−n)=κq_T(s^(−(n−1)),T0+D s^(2−n)).

The parent bound q_T≤8y^(7/2)/(7T0³), valid for T≥T0, gives RHS=O(s^(−7(n−1)/2)). For merely positive bounded T approaching T0, use T≥T0/2 sufficiently far out and the same bound with T0/2. Multiplication by s^(n−2) therefore forces D=0, since 7(n−1)/2>n−2. Then the equation becomes 0=κq_T(y,T0), impossible for exterior y>0. This exterior-only argument covers hollow profiles and avoids assuming injectivity at the center where gN=0.

Alternatively, for a profile positive near the center and at all interior radii before its edge, equality extends by continuity through s=0. A regular bounded whole-space harmonic T approaching T0 is constant: its spherical mean about any point is constant in radius by the divergence theorem, and tends to T0. The same contradiction follows. Exterior harmonicity is sufficient and stronger in source coverage.

For the parent's actual Banach solutions, uniqueness and rotational invariance establish radiality. The sufficient contraction condition 3κπ/(2Zm²T0)<1 is independent of M. Thus this is a counterexample to exact kernel universality among existing solutions, not an existence failure.

## Quantitative first source-dependent force term in three dimensions
For each fixed body and fixed positive parameters, put λ=(m rM)^(−2) and y=(rM/r)² in its exterior. Direct expansion gives

q_T(y,T0)=T0^(−3)[(8/7)y^(7/2)−y^4+(4/9)y^(9/2)+O(y^(11/2))].

The actual finite-Z solution has

u=T−T0=κ/(Zm²T0³)[(8/7)y^(7/2)−y^4+(4/9+48λ)y^(9/2)+O(y^5)].

Here u is a modulus displacement, not the interpolation function ν. To justify the remainder, cut off the displayed trial series smoothly inside a large exterior radius. The radial identity Δr^(−j)=j(j−1)r^(−j−2) makes its massive-operator residual O(r^(−10)); 42 times 8/7 gives 48. The nonlinear forcing correction is O(y^7), since q_TT=O(y^(7/2)) and the parent solution u=O(y^(7/2)). The difference from the trial is the massive Green convolution of a bounded O(r^(−10)) residual plus a compact contribution. Splitting the convolution into |z|≤r/2 and its exponentially small complement gives O(r^(−10)). No expansion in 1/Z is used. This establishes the displayed asymptotic remainder for fixed parameters, rather than a uniform small-mass estimate.

Since ν_T=2T0^(−3)[y^(3/2)−y²+(1/2)y^(5/2)+O(y^(7/2))], the full physical extra force compared with the constant-T0 kernel is

δg=κa0/(Zm²T0^6)[(16/7)y^6−(30/7)y^(13/2)+(254/63+96λ)y^7+O(y^(15/2))].

The second-T-variation term is O(y^(19/2)), beyond these orders. The first explicitly source-dependent coefficient is 96λ in the force at order y^7 (order y^6 in g/gN). At the same exterior y, two bodies therefore satisfy

g1−g2=96κa0/(Zm²T0^6)(λ1−λ2)y^7+O(y^(15/2)).

In n=3, λ=a0/(m²GnM). The smaller mass has the larger correction at this order. The comparison is a far-field fixed-two-body limit requiring r≫body radius,m^(−1), y≪1 and u≪T0; it is not uniform as M→0. Profile-dependent exponentially decaying homogeneous contributions do not alter these power coefficients.

## Interpretation and next missing arrow
The local heavy-modulus approximation drops the radius-dependent Laplacian and solves Zm²u=κq_T(y,T0+u), allowing approximate universality. Finite gradients spoil exact universality at the identified order. This diagnostic is not an observed violation or a bound on Z or m. A finite window can hide the correction.

The source-dependent exterior function ν_M(y) is not one universal kernel whose vacuum moment can automatically be inserted into C=∫y(ν−1)dy. The constant-T0 moment remains a separately defined mathematical function of the parent kernel; deriving its cosmological meaning requires a new same-action covariant vacuum/source dictionary. There is no 32π selection here.

## Verification and provenance
checks.py uses exact rational symbolic identities for source scaling, exterior equations, radial powers, small-y coefficients and the physical force product. Three negative controls test dropping the radius-gradient term, treating a nonzero exterior harmonic displacement as a solution, and removing the actual mass-dependent force coefficient. The computation corroborates the proof's algebra; it is not a numerical PDE integration or a whole-class empirical test. Frozen input hashes and actual checkout HEAD are in provenance.json; current runner evidence is in RUNS.md. No external theorem is used beyond the explicitly derived radial harmonic and massive Green estimates; the parent report supplies the action, existence and its established tail.
