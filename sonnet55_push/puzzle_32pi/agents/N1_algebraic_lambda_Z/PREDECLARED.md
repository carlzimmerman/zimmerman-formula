# N1 pre-declaration (written and hashed BEFORE any script of this lane was run)

Units: c = G = 1 in derivations; L = c/H_Lambda = sqrt(3/Lambda); a0 = c H_Lambda / Z = 1/(Z L).
Nariai mass M_N = L/(3 sqrt 3). Z is the dimensionless ratio to be confronted with data.

## What I knew beforehand (disclosure)
- Lane V's table: Z_N = 3 sqrt 3 = 5.196 sits about +0.4 sigma on the Lambda footing, Z_F 1.3 sigma (ensemble E). Lane V declared N before its data statistics.
- Lane L/X3: at Nariai r_b = r_c = L/sqrt3; I expect (hand estimate, to be verified) that photon sphere 3M, zero-force radius (M L^2)^(1/3) also coincide there, so all "at the Nariai point" radii give Z = sqrt3, and only a radius L (pure-de-Sitter horizon, not a horizon of the M_N geometry) gives 3 sqrt3. I expect this to be the main finding. I have not computed the SdS marginally-stable-orbit number.

## Menu (formula declared; numbers not yet computed). Z = 1/(a0 L) for a0 = the listed acceleration.
Each line: id | acceleration | PHYSICAL PRINCIPLE that would make it the MOND scale | self-consistency test.
A1 | G M_N / L^2 (Newtonian field of the Nariai mass at r = L) | "the largest static mass a Lambda-universe can hold sources, at the de Sitter horizon distance, sets the smallest acceleration a bound system can have" | test: is r = L a point of the M_N geometry's static patch? (expected NO: f(L) < 0). Uses a chosen radius (pure-dS horizon).
A2 | G M_N / r_N^2, r_N = L/sqrt3 (Nariai horizon) | same principle, radius = the horizon of the M_N geometry itself | no chosen radius.
A3 | G M_N / r^2 at the Kottler cosmological horizon of the M_N geometry | same | coincidence with A2 to be verified.
A4 | G M_N / r_ph^2, r_ph = 3 G M_N/c^2 (photon sphere) | "acceleration at the light ring of the largest hole" | coincidence to be verified.
A5 | G M_N / r_0^2, r_0 = (M_N L^2)^(1/3) (zero-force radius) | "where Lambda repulsion balances the pull: the field at which gravity stops being the only force" | coincidence to be verified. (Equals Lambda-repulsion r_0/L^2.)
A6 | c^4/(4 G M_N) = Schwarzschild surface gravity of the Nariai mass (kappa_S) | "horizon surface gravity of the maximal hole" (flat-space formula, Lambda ignored) | mixes flat-space horizon with Lambda-bound mass.
A7 | G M_N / (6 G M_N)^2 (Newtonian field at the Schwarzschild ISCO of M_N) | "innermost orbit of the maximal hole" | Lambda ignored; inconsistent for M_N (no orbits at all at Nariai).
A8 | exact SdS: M_s = the largest mass with a stable circular timelike orbit; a = G M_s/r^2 at that critical orbit (coordinate-Newtonian), and the exact proper centripetal acceleration of that geodesic's static-frame equivalent is NOT used (geodesics have zero proper acceleration) | "largest mass that can carry a bound stable orbit: the bound-system existence threshold" | computed exactly; if no stable orbit exists for any M it is reported as such.
A9 | kappa_f at Nariai (f-normalised) | surface gravity of the degenerate horizon | expected 0, i.e. Z = infinity.
A10 | kappa_BH at Nariai (Bousso-Hawking normalised) = sqrt3 H | same, other normalisation | also equals 1/(Nariai dS2 radius) and (Lambda)^(1/2) c^2.
A11 | Lambda repulsion r/L^2 at r = L (pure dS, G M_Lambda(L)/L^2 with M_Lambda = (4 pi/3) rho_Lambda L^3) | vacuum mass inside the Hubble ball | Z = 1 (M_Lambda = L/2 gives 1/(2L): Z = 2 -- both evaluated; I do not know which is which until computed).
A12 | extremum of the static-observer proper acceleration a_s(r) = (M/r^2 - r/L^2)/sqrt f over r, M<M_N | "maximal force / tension point" | expected NO stationary point (monotone); if none, candidate removed, reported as a no.
Aliases by construction (same number by the algebra): recorded, not counted as independent.

## Decoys and controls (declared)
- Decoy family D1: a0 = c^2 sqrt(Lambda)/n, n = 6..12 (integers): these are pi-free algebraic multiples; counts how many "principle-free" integers fit.
- Decoy family D2: Monte Carlo menus of 12 Z values log-uniform in [0.5, 12]; false-match probability that at least one lies within the observed best |sigma| of the data.
- Decoy family D3: grammar decoys Z = p sqrt(q)/r, p,r in 1..6, q in {1,2,3,5,6,7}: fraction within +-x of data.
- Mutation: change the Nariai mass by a factor (e.g. use M_N/2): A1's Z must move accordingly and the check of Nariai-coincidence must FAIL.
## Data (from lane V, read not refit): a0 = 1.097e-10 +-12.2% (ensemble E); SPARC record 1.0766e-10 (5.44% crude, 16.1% with systematics); kernel values alpha1 1.083 / RAR 0.873 / simple 0.881 / standard 1.117 (e-10, 8.2% stat); H0 = 67.4, Omega_Lambda = 0.685 (Planck), H0 = 73 variant.
## Promotion rule (declared)
A candidate is promoted to "principle-consistent" only if (i) its principle is stated above, (ii) its geometry is self-consistent (radius belongs to the same solution), (iii) no chosen radius. A DERIVATION verdict additionally needs the principle to fix the coefficient and be about ordinary-galaxy acceleration; none is expected. Z is 'data-compatible' at |z| < 2.
