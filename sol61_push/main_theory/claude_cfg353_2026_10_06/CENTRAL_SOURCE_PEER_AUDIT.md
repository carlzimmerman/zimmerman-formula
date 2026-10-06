# Independent central-source audit of stationary log KGB plus acceleration response

**Restricted verdict:** the proposed regular-center lapse/radial/momentum coefficients and discriminant are correct. They obstruct a C² regular stationary metric and clock with finite static Killing-perfect-fluid density, weak central lapse and sufficiently large positive ρ0+3p0 on the stated vacuum-normalized action. They do not exclude all time-dependent sources, singular density cusps, alternative clock/matter couplings or modified actions. A real quadratic root alone is not a sufficient interior solution.

The derivation below starts from the full unfixed-radius spherical ADM action and exact source variation in flowing_clock_2026_10_06/spherical_adm/REPORT.md (SHA256 b82447d4c3cf3031031229ed433b55fa924605da5855bda45fa1fabeb23cdddb) and derive.py (9d8f74353661ef964df32e02a488209e24ca8b40bec27e0b0f908dba0795f0c5). No cold/source-agent code was executed or modified. This is an independent reconstruction of the proposed equations, not adoption of a peer verdict.

## Matter signs and central coefficients

Write K_E=K>0, η=c/(3KH²)∈(0,1), b=2KηH, Veff=3KH², F=N²−B²V². The physical fluid is static along ∂t/√F, not the ADM normal when V≠0. Direct variation of (√−g/2)T^{μν}δg_{μν} gives, per 4π,

E_N,m=−Br²[(ρ+p)N²/F−p],
E_B,m=Nr²[p+(ρ+p)B²V²/F],
E_V,m=NB³r²(ρ+p)V/F.

Let N=N0(1+n2r²+o(r²)), B=1+b2r²+o(r²), V=N0 x r+o(r), ρ=ρ0+o(1), p=p0+o(1). Here N0>0, x=v1/N0, R=ρ0/K and P=p0/K. Assume the derivatives needed in the Euler coefficients have the corresponding regular-center limits. The matter contributions at orders r²,r²,r³ are respectively −ρ0, N0p0 and x(ρ0+p0).

The actual response is K U(a), U=a²−2W(a), with a=|N′|/(NB). Both uncut P2 and the cutoff kernels have U=a²+O(a³/A) as a→0. The leading derivative U_a=2a+O(a²/A), extended with its signed derivative when N′<0, makes the lapse term −K(r²U_a)′ contribute −12K n2 r². It cannot be dropped. The response's algebraic pressure is order r^4 in the radial equation, and its higher terms do not affect the leading coefficients. A cubic |a|³ term can produce nonanalytic higher radial orders; only the stated C² leading regularity is needed here, not a claim of an all-orders analytic series.

The lapse terms are: curvature 6Kb2r²; extrinsic flow 3Kx²r²; scalar bulk K[u0+6ηH²]r²; braid 6KηHx r², where u0=−3H²+6ηH² ln N0. The resulting equations are

2b2−4n2+3x²+u0=−P,
6b2−12n2+3x²+6ηHx+u0+6ηH²=R,
x[b2+n2−(R+P)/4]+ηH n2=0.

All N0 factors and source signs agree with the proposed raw equations. Pressure gradients are fixed at the next order by p′=−(ρ+p)F′/(2F); they do not change these leading finite-source coefficients.

## Necessary real-center bound and an additional momentum condition

Subtracting three times the radial equation from the lapse equation eliminates b2,n2 and gives

x²−ηHx−(1+η)H²+2ηH² ln N0+(R+3P)/6=0.

Its discriminant is

D=(η+2)²H²−8ηH² ln N0−(2/3)(R+3P).

Thus a necessary real-center condition is

ρ0+3p0 ≤ (3K H²/2)[(η+2)²−8η ln N0].

For N0≈1 the right side is of the cosmic density scale, independently of A or its UV cutoff. Ordinary matter with ρ0+3p0≫KH² fails that condition on this stationary regular branch. The negative-lapse logarithm could formally offset a large density, but requires ln N0 of order −(ρ0+3p0)/(12ηKH²), an extreme central redshift relative to the fixed cosmological clock normalization, not a weak-field star. It is not a free gauge reset: Veff already fixes the vacuum/q normalization and the outer normalized lapse.

The remaining momentum equation supplies the additional relation

(3x+ηH)n2=(3/2)ηH x(x+H).

For 0<η<1, x=−ηH/3 has a nonzero right side and cannot satisfy this regular coefficient system. Therefore D≥0 alone is insufficient; the full interior, pressure/EOS, physical metric, clock and boundary conditions remain necessary. Negative-pressure matter or a changed vacuum normalization changes the stated inequality's interpretation.

## Nonanalytic deep-MOND central lapse: no regular-metric cancellation of this power type

A uniform-density deep-MOND potential often behaves as r^{3/2}, with acceleration ∝√r. It is C¹ but not C² at the center. Such a formal lapse is outside the regular-clock series above. It must not be excluded merely by calling it nonanalytic: one should test whether the physical Killing metric could stay regular through flow cancellation.

There is a direct necessary test. Let the physical diagonal stationary metric have F=F0+O(r²), F0>0, and Dmetric=(NB)²/F=1+O(r²), with their derivatives O(r). Then J=NB=√(F Dmetric) obeys J′/J=O(r). For finite ρ+p the exact sourced momentum constraint is

2K V J′/J + b r N′ = r V Dmetric(ρ+p).

Suppose N=N0[1+αr^p+o(r^p)] for 1<p<2, α≠0, with the corresponding differentiated leading terms, and V→0 at the center. Since F0=N0² and B→1, regular F would require V²=2N0²αr^p+o(r^p). If α<0 it already gives no real V. If α>0, V∝r^{p/2}. Both terms containing V in the momentum equation are then O(r^{1+p/2}), while b rN′ has a nonzero r^p leading coefficient. Because p<1+p/2, cancellation is impossible for b>0. In particular p=3/2 cannot restore a C² regular physical metric by a V∝r^{3/4} cancellation.

This is a scoped power-law argument, not a theorem about every nonsmooth function. If the physical metric itself is allowed a nonregular central curvature, the source density/pressure is singular, the clock/matter has additional flux, or time dependence is retained, its assumptions fail. The clock expansion for the proposed cancellation also diverges as r^{p/2−1}. No health conclusion for such singular alternatives is supplied here.

## Independent exact controls

center_audit.py differentiates the complete areal action before substituting the central series, includes the physical fluid stress sources, and checks all three leading coefficients, the quadratic/discriminant normalization and remaining momentum condition. The negative control removes the acceleration quadratic term to test the omitted lapse contribution. The analytic derivation above is the proof; finite symbolic output only corroborates these stated coefficients. Fresh center_main_a passes the six exact checks. center_control_quadratic fails the lapse coefficient and resulting central quadratic elimination, as intended. Both manifests validate with current input/output hashes.
