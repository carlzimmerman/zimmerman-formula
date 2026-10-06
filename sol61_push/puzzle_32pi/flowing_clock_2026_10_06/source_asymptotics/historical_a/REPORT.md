# Nonzero flowing clock: sourced P2 exterior balance is possible at leading order

Base and observed initial HEAD:07fa64b44891fc87697f53f86812287946481586. This is an independent asymptotic calculation for the logarithmic KGB plus fixed-A acceleration response. It does not establish an exact spherical solution. Unlike the zero-flow obstruction and conserved expanding-dust control, a nonzero stationary radial clock flow can satisfy a formal mass-normalized MOND exterior balance. The cosmological matching and regular conserved-fluid interior remain unproved. No32π selection follows.

Use the actual covariant action/conventions in ../../dynamical_sector_2026_10_06/kinetic_braiding/REPORT.md: K_E=M>0, K=−c ln(X/Xref), G=−√2c/(3H*)X^−1/2, η=c/(3MH*²)=−z∈(0,1), minimal conserved matter, and Lresp=M Q(a), Q=a²−2W(a;A), A fixed positive. W_a=√(a²+A²/4)−A/2. Its exact vacuum-rescaling map survives this response because the normalized clock is invariant. The vacuum parameter is not reset by hand: U(N)=K(q²/(2N²))−ρ_v=−3MH*²+2c ln N on the selected rolling branch.

## Exact stationary identities before any weak-field approximation

In unitary coordinates φ=qt,
ds²=−N²dt²+B²(dr+Vdt)²+r²dΩ².
X=q²/(2N²), a=|N'|/(NB), and θ=−(Br²V)'/(NBr²). Take the N'>0 exterior branch below; signs must be changed appropriately when crossing N'=0. Removing the shift by a stationary time change gives F=N²−B²V²>0 and radial metric N²B²/F. The physical proper acceleration of stationary metric observers is F'/(2NB√F); it is not generically N'/(NB). A bound source stationary in the diagonal metric can have nonzero ADM momentum; a vacuum exterior avoids assuming that momentum away.

After the appropriate radial boundary terms, the stationary action density (without the common4π) is
L=M[N(B+1/B)+2rN'/B]−MrV²[B'/N+B N'/N²]
+NBr²U(N)−(2c/(3H*))Br²V N'/N+MNBr²Q(a).

The full vacuum momentum equation is
V(B'/B+N'/N)+ηH*rN'=0.
The response contains no V and cannot alter this exact equation. Nonzero flow is essential; V=0 on an interval would require N'=0.

The exact B equation divided by M is
N(1−B^−2)−2rN'/B²+(V²+2rVV')/N−2rV²N'/N²
−2ηH*r²V N'/N+Nr²U/M+Nr²[Q−aQ_a]=0.

The exact N equation divided by M is
B−B^−1+2rB'/B²+[(B+2rB')V²+2rBVV']/N²
+2ηH*(Br²V)'/N+Br²[U+2c]/M
+Br²[Q−aQ_a]−(r²Q_a)'=0.
A regular minimal fluid contributes its actual ADM energy, momentum and stress to these equations. In a vacuum exterior the displayed equations require no externally imposed source law. The source appears as a mass integration constant at leading order; identifying it with baryonic mass needs an interior calculation.

## Retained weak-field balances and physical force

Let N=1+n,B=1+b,V=−H*r+v, S=V²−H*²r², a≈n', and g≈a−S'/2, where g is the physical force with the background de Sitter contribution subtracted at this order. Keep the clock lapse gradient nonlinearity Q_a, the V² contribution and the linear-in-H* braiding contribution. Discard higher weak-potential products and H*²n terms only when small relative to the retained mass flux. Then the radial equation and lapse mass integral give
2b−2ra+(rS)'≈0, hence rg≈b+S/2,
r²[g−a+W_a(a)+ηH*v]≈m.
Here m is the exterior integration constant; for an admissible regular weak-source interior with no independent homogeneous mass/clock charge it should reduce to G_N,b M_source, G_N,b=1/(8πM). That identification is conditional here, not proved from exterior equations alone.

Combining the same radial identity with the momentum equation gives the useful necessary physical-force relation
r g'+2g≈ηH*r a/(−V).
This prevents borrowing a static a=g law while discarding the clock equation. In particular the mass integral alone is insufficient.

## Formal sourced P2 profile and flow dictated by the momentum equation

In a region where V² derivative terms, cosmological terms, and higher weak-potential terms are small compared with the retained mass flux, g≈a and the integrated lapse equation reduces to
W_a(a)=m/r².
This is a derived vacuum mass balance, not an imposed acceleration law. Its positive inverse is
s=m/r²,
a(r)=√[s(s+A)].
At high s/A it approaches a≈m/r²+A/2; at low s/A it gives a≈√(mA)/r. The scalar/metric radial equation gives b≈ra. The nonzero momentum constraint then fixes, rather than permits choosing,
V≈−ηH*r a/[r a'+2a]=−ηH*r(1+s/A).
The identity r a'+2a=A s/a was derived from the exact inverse. The deep-MOND branch has V≈−ηH*r and b≈L=√(mA) constant. The interior high-force exterior has V≈−ηH*m/(A r); treating V as −ηH*r through that region is incorrect. In the formal deep branch, g has mass exponent1/2 and radius exponent−1, with acceleration scale A independent of m. This differs from the previous pure KGB Vainshtein force because the added acceleration response and nonzero stationary flow both enter the source constraints.

These profiles satisfy the leading mass/momentum/radial equations, not the exact equations above. Flow and its derivative are not negligible automatically. Necessary control scales include r_M=√(m/A), L=√(mA)≪1, r_cos=(m/H*²)^(1/3), r_flow~η²H*²m/A², and weak lapse drift |L ln(r/r_ref)|≪1. In a deep window require
r_M≪r≪r_cos, Ar≪1, |V|≪1.
The r_cos restriction suppresses H*²r against the much smaller mass term m/r², not merely against g. Ar≪1 suppresses post-Newton terms of order L²/r against m/r². In the high-force region also require r≫r_flow and m/r≪1. Existence of a deep overlap requires approximately L≪(A/H*)², with numerical constants depending on the chosen tolerance.

The matching deficit is visible already: outer rolling de Sitter needs V→−H*r, whereas this deep branch has V≈−ηH*r, η strictly below1 on the healthy cosmological interval. The neglected terms become important near r_cos and may change the branch, exclude it, or select additional integration data. Taking η=1 to remove the deficit is forbidden by the singular original KGB constraint boundary. No smooth global connection has been established. Clock/lapse additive data and exterior m remain boundary data until the complete source and asymptotic solution is solved.

## Independent zero-shift-charge check

Minimal matter does not inject scalar shift charge. Regular-center matching requires the conserved exterior quantity NBr² j^r_total to vanish, rather than treating it as a new freely chosen charge. Direct stationary scalar variation, performed before setting the perturbation to zero, gives
j^r_KGB=(2c/(3H*q))[N'/B²−3H*V−(V/N)(V'+(B'/B+2/r)V)],
j^r_response=M V/(qBr²)(r²Q_a)'.
For the latter identity, a stationary perturbation δφ=ψ(r) gives δa=(NVψ')'/(qNB), and its integrated response variation is −(M/q)NV(r²Q_a)'ψ'. This uses fixed A, N'>0 and the canonical-current sign j^r=−(1/√−g) times the stationary scalar Euler momentum.

In the leading P2 exterior (r²W_a)'=0, this current becomes
j^r_total≈(2M/q){ηH*a+V(a'+2a/r)−ηH*[3H*V+V(V'+2V/r)]}.
The first two terms cancel exactly for the momentum-determined flow above. This is an independent necessary zero-charge consistency check of the leading branch. The last small terms do not vanish identically for that profile and cannot be discarded in an exact zero-charge assertion: they require subleading corrections. Tiny terms in the gravitational balances can be loadbearing in the scalar equation. Exact scalar-charge, angular/Bianchi and regular-center matching have not been closed here.

## Evidence, controls, and first missing implication

checks.py derives the exact stationary Euler equations algebraically, checks the de Sitter vacuum, the weak physical-force identity, P2 inversion and forced flow, and samples bounded weak/deep windows with explicit omitted-term ratios. Negative controls impose zero flow, use the deep flow in the Newtonian transition, or treat clock acceleration as the exact physical force. Source dependence is not proved by samples: exponents come from the exact leading balance. Primary inputs are the previously version-verified KGB/Horndeski source records and the P2 operator declared by the project; this is an internal asymptotic derivation, not an external theorem or literature-wide novelty claim.

Strongest safe advance: the coupled leading vacuum equations admit a formal mass-normalized MOND exterior with nonzero clock flow; a zero-flow obstruction cannot rule out this branch. Smallest missing implication: construct an exact or controlled matched asymptotic solution of the same varied action, with regular conserved static-fluid interior (including its true ADM momentum), cosmological outer clock, and finite-gradient constraint health. Until then m cannot be asserted universally to equal the measured baryonic source mass, nor A to equal an observed a0. Even a successful construction would leave the separate A/H* selector problem open.
