# DR2_noether_flux_contraction: FROZEN CRITERIA (committed alone, before any script or number)

kappa = 1/2 FITTED, unused here. Cold dark energy is a gravitating field component, no particle. Not theory closed. Nothing here says the data favour the framework. One thread, nice 15, minutes, no downloads, other lanes read only.

## Question
An outside text claims: in a shift-symmetric scalar-vector theory (AeST type), static spherical div J = 0 gives 4 pi r^2 J^r = Q0, fixed at turnaround, so baryons condensing centrally "mathematically forbid" Blumenthal pile-up while w ~ 0 clustering stays intact. Is that a valid derivation? The text is a claim under test, its reasoning is not adopted.

## Record check (done before this freeze)
No lane has tested this. Related, read only: X6 X-D1/X-D2 (the khronon's force relative to free fall is grad Xi; at Q = 1 it is mimetic, geodesic dust), X14 (single-stream caustics are generic), X17/the mu-pincer (pressure cannot keep the cold mass out of galaxies), C1 (AeST's static limit), O1 K9, X39 (Blumenthal code), LC1 (Blumenthal holds in live zooms, f_Q 0.872).

## Rule under test
L = P(X), X = -(1/2) g^{mn} d_m phi d_n phi, Q = sqrt(2X), matter coupled to g only. Dust limit: P = K(Q) with K = mu^2 (Q-1)^2 and Q -> 1 at fixed charge density (mu -> infinity). Static AeST: the record's C1 weak-field Lagrangian. No new number.

## Derivations and checks (sympy unless stated)
- S1 J^m = P_X d^m phi (sign fixed in the script), its covariant divergence in the general time-dependent spherical metric, and that the equation of motion is d_t(sqrt(-g) J^t) + d_r(sqrt(-g) J^r) = 0, which is continuity: 4 pi r^2 J^r(r,t) = -d_t N(<r,t) up to the metric factors, not a constant in general.
- S2 Static: sqrt(-g) J^r = C. A regular centre gives C = 0. Then chi' = 0 or P_X = 0.
- S3 Exact identity, general spherical metric: u^n nabla_n u_m = -h_m^n d_n ln Q or its correct sign (to be derived). The dust limit (Q -> 1 uniformly) gives geodesics. A static fluid in a gradient of Phi has Q e^{Phi} uniform, so it isn't in the dust limit.
- S4 C nonzero: steady flow, J^0 = C/(4 pi r^2 v(r)), with a sink at the centre.
- S5 Two different radial distributions with the same total charge and the same C = 0 solve the conservation law: charge conservation alone doesn't constrain the distribution of J^0.
- S6 On C1's AeST static Lagrangian: the chi equation, its flux with C = 0, and what it fixes (expected the algebraic law relation), and J^0.

## Numerics (Newtonian weak field, stated toy, no grade)
Start: NFW, M200 1e12 Msun, R200 200 kpc, c 10, softening 1 kpc. Baryons: LC1's disc, M_d 6.72e10 Msun, R_d 3.565 kpc as a spherical mass M_d[1 - a/sqrt(r^2+a^2)], a = R_d (as LC1's spherical(), whose a to be read from LC1; if different use LC1's), grown slowly.
- N1 Pressureless single-stream radial field (Hamilton-Jacobi plus continuity on a grid) against geodesic shells, before the first caustic: same velocity field; flux identity; first caustic time reported.
- N2 Self-gravitating shells on circular orbits, conserved charge, baryons grown slowly: Q(r) = M_cold,final(<r)/M_cold,initial(<r) at r/R_d = 1,2,3,4,6,8,10 against Blumenthal; the flux 4 pi r^2 J^r(r,t) measured at a fixed radius against -dN(<r)/dt.
- N2b Same on nearly radial orbits, the closest to the scalar's zero angular momentum (phase-mix, then grow).
- N3 Finite sound speed, static: the K above, n = dK/dQ, Q0 e^{-Phi} rule, self-gravitating, total charge fixed, polytrope radius set to R200 (no fitted scale), baryons added: sign of the central response.
- N4 Steelman: C nonzero sized to hold the flat-curve density of V = 220 km/s: required Mdot, and the mass delivered to the sink in 10 Gyr, as a multiple of M200.

## Labels
Failure tests, each either true or false from the above:
- F1 static regular centre forces C = 0 (no Q0 fixed at turnaround from the static equation).
- F2 conservation with fixed flux doesn't constrain the radial distribution of J^0 (S5).
- F3 strict dust limit is geodesic (S3), and static dust in a potential gradient doesn't exist.
- F4 N2: with charge conserved to <= 1e-10 per step or better, pile-up appears: mean (Q-1)/(Q_B-1) over r/R_d = 2,3,4 >= 0.8 (LC1's line).

- **ARGUMENT FAILS**: F1 or F2 true AND F3 AND F4 true. The lane stays a derivation note and nothing is graded.
- **ARGUMENT SURVIVES**: F1, F2 and F4 all false. Only then: an amendment freezes a stated profile and grades it on SPARC, 15 keys, X-COP, groups, LITTLE THINGS at the record's lines.
- **UNCLEAR**: anything else, saying which.
An escape other than the claimed one (finite sound speed, a sink) is reported as a separate finding, not as the claim surviving, and any new number it needs is named.

## Checks
- K1 My Blumenthal against X39's `contract` on the N2 setup, |d| <= 1e-6 on Q at the seven radii (read X39 by exec, no writes).
- K2 N2 with M_d = 0 stays at Q = 1 within 0.01. K3 Shell charge conserved at machine level. K4 flux identity residual <= 5 % of peak flux. K5 sympy residuals zero. Failed check: no verdict.
- MUTATE (separate outputs): (a) a sign flip in the S3 connection term must make the identity fail; (b) shells leak 1e-3 of their charge per step must fail K3 and K4.

## Disclosure and expectation
Not blind: Blumenthal's results, LC1, X6 and X14 are known. Expectation on record: ARGUMENT FAILS. Charge conservation is a premise of Blumenthal rather than an obstacle to it; a static regular centre has zero radial flux; the dust limit is geodesic; the only real difference is the fluid's zero angular momentum and caustics, plus a finite sound speed, which the mu-pincer already covers.
