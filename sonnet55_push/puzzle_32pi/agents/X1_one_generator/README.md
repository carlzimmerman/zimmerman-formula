# Lane X1: is there ONE generating structure behind all the 32 pi's, and what would it say about the puzzle?

(c = G = 1 unless stated. Puzzle: Lambda = 32 pi a0^2, i.e. G rho_Lambda = 4 a0^2 (pi-free), a0 = (1/2) sqrt(G rho_Lambda), kappa = 1/2 FITTED. Variable held fixed: L (Lambda) unless stated.)

## Bottom line
1. **Verdict: NOTHING NEW on the factor (kappa = 1/2 stays FITTED); SHARP NO-GO (scoped) on two specific ideas: (i) a single generator of the '4's, (ii) a Noether-charge / Euler-unit origin of A Lambda = 32 pi^2.** Nothing here derives the 4 in G rho_Lambda = 4 a0^2; it is the only factor in the 28-row ledger whose origin is not a derivation.
2. **No single formula in D generates the 4's.** Recomputed for D = 4..8, the graviton's 4 (kappa_g^2 = 8 pi G x 4) and the Bekenstein-Hawking 4 (S = A/4G) are constant, the Tangherlini horizon (r_h kappa)^-2 is 4/(D-3)^2, the MacDowell-Mansouri algebra gives 2(D-2)(D-3); 5 of the 6 pairs of these D-lifts differ. The equality of the TT-graviton kinetic coefficient and the Euler coefficient, both 1/(64 pi G), is a **D = 4 accident of two different quarters** (1/4 from expanding sqrt(-g)R, D-independent; 1/4 = 1/(2(D-2)(D-3)) from the Euler algebra, and the identity R - 2 Lambda = (Euler - F^2)/norm exists only at D = 4).
3. **Candidate origins of the 4** (trace D, spin^2, polarisations^2, sphere/disc = 4 pi/pi, thermal 8 pi/2 pi, quadratic-EH 1/(1/4), Tangherlini, static-patch channels, GB-shift, response N^2): all give 4 at D = 4 by construction and 25 of 26 simple D-formulas that equal 4 at D = 4 are D-dependent (agreement at D = 4 is worthless). Under the premise that the puzzle's 4 is the graviton's 4, only the D-independent class {spin^2, 8 pi/2 pi, quadratic-EH, response N^2} survives: four different claims, identical D-lift, no mechanism, indistinguishable. 4 = D read on the TOTAL source predicts an evolving a0 (a0(2.5)/a0(0) = 2.31, versus 1.00 flat and 3.77 for a0 ~ H(z)).
4. **Noether/Euler link (task 3): no.** The Iyer-Wald charge of the static-patch Killing vector is Q(r) = -r^3/(2 G L^2) (r^2 for the area law); a quantity ~ r^n has pi-power n/2 at r = Z L/2, so no r^3 charge, Noether entropy or Euler number can be a rational multiple of pi^k there; with the Euler term the charge is (1 + 4 alpha/L^2) Q, an equation-of-motion-blind shift (it vanishes identically for the MacDowell-Mansouri alpha = -L^2/4). A Lambda = 32 pi^2 is exactly 'the a0-surface entropy is 16 pi/3 Euler units', a rewriting.
5. Side result (structural, not a derivation): A kappa^2 <= pi over all Kerr-Newman horizons, so kappa <= (1/2) sqrt(mean Gauss curvature): a0 = (1/2) sqrt(G rho_Lambda) is the supremum of kappa at K_bar = rho_Lambda. True for KN (D = 4), RN (D = 4,5,6), Myers-Perry single spin (D = 4,5); **false for Myers-Perry at D = 6, 7**. It relocates the puzzle to 'why K_bar = rho_Lambda, and why the supremum'.

## 1. What I did (all scripts in this directory, each with a `.out`; all exit 0)
| script | content | pass (of which controls) |
|---|---|---|
| `x1_01_atoms.py` | independent recomputation of every atom: sphere volumes/Gaussian generator, Gauss flux, 3-d Fourier transform and heat-kernel form of 1/(4 pi r), trace-reversal factor in D = 4..7, TT quadratic EH action (D = 4, 5), Isaacson, time average, S^4/S^2xS^2 Euler constants and (2n)! Vol(S^2n) = 2 (4 pi)^n n! (n <= 8), explicit BPST instanton, Iyer-Wald charge, Smarr, S = A/4G, near-horizon period, free fall, FRW | 70/70 (10) |
| `x1_02_dlifts.py` | D-dependence for D = 4..8 of Omega_{D-2}, (D-2)/(D-3), G_N/G_E, TT quarter, Wald quarter (tensor contraction and Iyer-Wald charge), Tangherlini kappa r_h, FRW, GB-shift identity, static-patch stabiliser dimension, polarisation count, sphere/disc ratio | 41/41 (4) |
| `x1_03_ledger.py` | the ledger: 28 rows, values recomputed independently, decomposition product verified exactly, each decomposition mutated (must fail), non-uniqueness control, atom incidence, the TT/MM double role, one-graviton exchange route to kappa_g^2 in D = 4..8, D-lift slot comparison | 87/87 (32) |
| `x1_04_candidates_of_4.py` | ten pre-declared candidate origins of the 4, tests S1-S6, a0(z) readings, Kerr-Newman/RN/Myers-Perry extremality (Smarr-validated), decoy control | 24/24 (6) |
| `x1_05_noether_euler_static_patch.py` | Euclidean action = Euler term, Iyer-Wald charge in dS (r < L and r > L), pi-power table, 'one unit' solutions, E_GB tensor (finite differences), Q_alpha = (1 + 4 alpha/L^2) Q, MM charge zero, GB tensor vanishing in D = 4, a0 surface in Euler units | 24/24 (4) |
| `x1_06_mutation_runs.py` | 5 clean runs, then 22 mutants (one load-bearing constant or expectation changed in a temporary copy); a mutant counts as caught only if it prints a FAIL line and does not crash | 5/5 clean, 22/22 caught |

Total 246 checks (56 controls). One self-correction: my first mutant for the c7 candidate crashed the script (an assertion), which the tightened runner refused to count as a catch; I replaced it with a mutant that fails a real check. My first draft of the Myers-Perry test assumed the extremality holds for every D and scanned unphysical D = 4 spins (a > r_+); checking the formulas before running showed that both were wrong (section 4, S5), and the script now declares the D = 6, 7 failure as the expected outcome.

## 2. The ledger (task 1)
Atoms (each recomputed in `x1_01`/`x1_02`; name: value, source; D-lift class):
`S2` 4 pi, solid angle (Gauss flux; 3-d Fourier transform of 1/q^2 = 1/(4 pi r); the same integral from the heat kernel; equal to 2 pi chi(S^2), 2-d Gauss-Bonnet) [D-dep, Omega_{D-2}];
`S3` 2 pi^2 and `S4` 8 pi^2/3 (angular integrals); `BIA` 2, weak-field G_00 = 2 Lap Phi, D-dim (D-2)/(D-3) [D-dep];
`VAR` 2, the 2 in T_mn = -(2/sqrt(-g)) dS_m/dg^mn (a scalar's T_00 is its energy density only with it) [D-indep];
`QEH` 1/4, the second-order coefficient of sqrt(-g)R for a TT wave (Euler-operator test; h_ij h_ij = 2 f^2) [D-indep, D = 4..8];
`CAN` 1/2 canonical normalisation, `VIR` 2 (wave energy = kinetic + gradient), `TTN` 2 (polarisation norm), `AVG` 1/2 (<cos^2>) [conventions/D-indep];
`PER` 2 pi, Euclidean regularity period 2 pi/kappa [D-indep]; `CHI2` 2, chi(S^2) = chi(S^4); `PF` 8 = 2^n n! (n = 2); `RAD16` 16, the BPST radial profile integral; `TRC` 1/4, SU(2) trace normalisation;
`ANG` pi/2, the free-fall quarter cycle; `F3` 1/3 = 1/dim SO(3); `MMQ` 1/4 = 1/(2(D-2)(D-3)) at D = 4; `HOR` 4 = (r_s kappa)^-2; `E8` = BIA x S2 = 8 pi; `FIT` 4 = 1/kappa^2 (the puzzle).

Rows (value = product of atoms; exact, sympy; every row's decomposition mutated once and rejected):
| id | quantity | value | atoms |
|---|---|---|---|
| R01 | Poisson/Gauss solid angle | 4 pi | S2 |
| R02 | Einstein 8 pi | 8 pi | BIA S2 |
| R03 | EH action 1/(16 pi G) | 1/(16 pi) | VAR^-1 BIA^-1 S2^-1 |
| R04 | TT graviton kinetic coeff. 1/(64 pi G) | 1/(64 pi) | VAR^-1 BIA^-1 S2^-1 QEH |
| R05 | graviton kappa_g^2 = 32 pi G (action route) | 32 pi | CAN VAR BIA S2 QEH^-1 |
| R05b | same, one-graviton exchange (source route) | 32 pi | VAR^2 BIA S2 |
| R06 | Isaacson 1/(32 pi G) | 1/(32 pi) | VIR VAR^-1 BIA^-1 S2^-1 QEH |
| R07 | GW flux coefficient rho/(omega^2 h0^2) | 1/(32 pi) | R06 x TTN AVG |
| R08 | MacDowell-Mansouri Euler coefficient L^2/(64 pi G) | 1/(64 pi) | VAR^-1 BIA^-1 S2^-1 MMQ |
| R09 | Chern-Gauss-Bonnet 32 pi^2 chi | 32 pi^2 | CHI2 S2^2 |
| R10 | same, Chern-Weil (2 pi)^2 x 2^n n! | 32 pi^2 | PER^2 PF |
| R11 | BPST instanton int F F~ | 32 pi^2 | S3 RAD16 |
| R12 | instanton action 8 pi^2/g^2 | 8 pi^2 | S3 RAD16 TRC |
| R13 | dS Euclidean action = c_E 32 pi^2 chi = pi L^2/G | pi | VAR^-1 BIA^-1 S2 MMQ CHI2^2 |
| R14 | MM coupling 1/g^2 = L^2/(16 pi hbar G) | 1/(16 pi) | VAR^-1 BIA^-1 S2^-1 |
| R15 | Bekenstein-Hawking quarter | 1/4 | PER E8^-1 |
| R16 | Hawking T = kappa/2 pi | 1/(2 pi) | PER^-1 |
| R17 | Komar / first-law 1/(8 pi G) | 1/(8 pi) | E8^-1 |
| R18 | Smarr M = kappa A/(4 pi G) | 1/(4 pi) | S2^-1 |
| R19 | Friedmann H^2 = (8 pi/3) G rho | 8 pi/3 | E8 F3 |
| R20 | free fall G rho t_ff^2 | 3 pi/32 | ANG^2 E8^-1 F3^-1 |
| R21 | dS horizon A Lambda | 12 pi | S2 F3^-1 |
| R22 | Nariai sphere A Lambda | 4 pi | S2 |
| R23 | Schwarzschild A kappa^2 | pi | S2 HOR^-1 |
| R24 | PUZZLE Lambda = 32 pi a0^2 | 32 pi | E8 FIT |
| R25 | PUZZLE A Lambda = 32 pi^2 (A = pi/a0^2) | 32 pi^2 | E8 S2 |
| R26 | PUZZLE G rho = 4 a0^2 | 4 | FIT |
| R27 | same 32 pi as (8 pi)^2/(2 pi) (not independent of R24) | 32 pi | E8^2 PER^-1 |

Verified relations among atoms (this is what the ledger can honestly say about 'one generator'):
- **All the pi's are one thing, and it is trivial:** every Omega_n, hence every 4 pi, 2 pi^2, 8 pi^2/3, is fixed by the Gaussian integral (Omega_n int r^n e^-r^2 dr = pi^((n+1)/2), checked n = 1..7). In D = 4, 4 pi = 2 pi chi(S^2) (the Poisson solid angle is the 2-d Gauss-Bonnet number, r-independent), and (4 pi)^n n! = (2n)! Vol(S^2n)/2 (n = 1..8), so the Chern-Weil form (2 pi)^n 2^n n! and the sphere-volume form of the Euler constant are one identity.
- E8 = BIA x S2 (8 pi = 2 x 4 pi) is a **D = 4 fact about how G is defined**: the force-law constant satisfies Omega_{D-2} G_N = 8 pi G_E (D-3)/(D-2), so G_N/G_E = 1, 8/(3 pi), 9/(4 pi), 32/(5 pi^2), 25/(4 pi^2) at D = 4..8.
- The powers of 2 are NOT one thing: 13 separately derived atoms (BIA, VAR, QEH, CAN, VIR, TTN, AVG, CHI2, PF, RAD16, TRC, MMQ, HOR) plus the fitted FIT. Verified ties between some: QEH = CAN/VAR (1/4 = (1/2)/2), so kappa_g^2 = 32 pi G is over-determined (action route CAN VAR BIA S2/QEH, exchange route VAR^2 BIA S2; T_mn P T_ab = (D-3)/(D-2) = 1/BIA, and both routes give kappa_g^2 = 32 pi G_E for D = 4..8); PER/E8 = 1/4 (the entropy quarter is the thermal period over the Einstein coupling, S = (2 pi/kappa) Q_H = A/4G); free fall t_ff = (pi/2)/H_F (a quarter Friedmann cycle).
- 32 pi has 5 exact decompositions over {2, 4 pi, 2 pi} with exponents in [-4,4] (2^4 (2 pi), 2^3 (4 pi), 2^2 (4 pi)^2/(2 pi), ...): matching a decomposition is bookkeeping; only the derivations above carry information about origin.
- Four families, by which atoms occur: **Gauss/Einstein** (E8 = 2 x solid angle: R02-R08, R14, R17-R19, R21-R25); **topological** ((4 pi)^n n!, S3 x 16: R09-R13); **thermal** (2 pi: R15-R16); **angle** (R20). The puzzle's AΛ = 32 pi^2 is E8 x S2, a product of two sphere integrals of different origin (Einstein 8 pi and horizon area); it equals the Euler number 32 pi^2 only when rho_Lambda r_s^2 = 1. The puzzle's own 32 pi = E8 x 4 shares its atoms with the graviton's 32 pi = E8 x 4, but the graviton's 4 is derived (QEH^-1 CAN VAR, or VAR^2) and the puzzle's is FIT.

## 3. D-lifts: why no single generator (task 1-2)
Computed for D = 4..8 (`x1_02`): Omega_{D-2} = 4 pi, 2 pi^2, 8 pi^2/3, pi^3, 16 pi^3/15; G_00/Lap Phi = 2, 3/2, 4/3, 5/4, 6/5; Friedmann G_00/H^2 = 3, 6, 10, 15, 21; and the 'extra 4' slots:

| slot | D=4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|
| graviton kappa_g^2/(8 pi G_E) (TT quarter, D = 4..8 by metric computation) and Bekenstein-Hawking 1/quarter (Wald contraction, Iyer-Wald charge, Tangherlini) | 4 | 4 | 4 | 4 | 4 |
| Tangherlini (r_h kappa)^-2 = 4/(D-3)^2 | 4 | 1 | 4/9 | 1/4 | 4/25 |
| MM/GB-shift 2(D-2)(D-3) | 4 | 12 | 24 | 40 | 60 |

A generator must be a formula in D; these differ (5 of 6 pairs; the graviton and entropy quarters agree with each other; my interpretation, not a check, is that both are 'EH-normalisation numbers' because sqrt(-g)R is linear in Riemann in every D). Caveat: this uses the premise that the puzzle's 4 shares an origin with the instance; the D-lifts are my generalisations (G_E convention; with a force-law or 4 pi-Poisson G_N the slots change, section 4). The D = 4 agreement of the slots is the agreement of things that are not the same thing.

**The double role of 1/(64 pi G) (as the brief asked):** TT kinetic (R04) and Euler (R08) are both 1/(64 pi G) x (1 or L^2) at D = 4 (V5: (R - 6k) = (E4(R) - E4(F))/(4k) on 300 random curvature tensors, alpha x 4k = 1 to 3e-12; on S^4 the on-shell action is exactly c_E x 32 pi^2 x chi = pi L^2/G, and lane A's 1/g^2 = 4 c_E = L^2/(16 pi hbar G) reproduces). They are different atoms (QEH vs MMQ): the TT value is 1/(64 pi) in every D, the Euler value is 1/(64 pi), 1/(192 pi), 1/(384 pi) at D = 4, 5, 6, and the Einstein-Lambda closure of the algebra (D(D-1)/2 = (D-1)(D-2)) holds only at D = 4. So 'the same 1/(64 pi G)' is a D = 4 coincidence, not a generator. Also, the entropy quarter equals 1/(BIA x chi(S^2)) = 1/(2 x 2) at D = 4 but that reading fails at D = 5 (chi(S^3) = 0) and D = 6 (3/8): PER/E8 is the D-independent one.

## 4. Candidate origins of the 4 and their second predictions (task 2)
Pre-declared in `x1_04` (the list itself was written knowing the target: it characterises, it does not measure a false-positive rate). D-lift N_c(D) for D = 4..8, and tests: S1 = equals the graviton/BH constant 4; S2 = equals the Tangherlini slot; S3 = equals the MM slot; S4 = a0(z); S5 = horizon-family extremality; S6 = S1 with G_N (force-law) instead of G_E.

| candidate | D-lift (D = 4,5,6,7,8) | S1 | S2 | S3 | verdict |
|---|---|---|---|---|---|
| c1 trace, 4 = D | 4,5,6,7,8 | fail | fail | fail | orphan at D != 4; on the TOTAL source (rho_m + 4 rho_Lambda) it predicts an evolving a0 (S4); on Lambda alone flat |
| c2 spin^2, s = 2 | 4,4,4,4,4 | pass | - | - | survives S1; no mechanism (spin enters no coefficient) |
| c3 polarisations^2 | 4,25,81,196,400 | fail | fail | fail | orphan |
| c4 sphere/disc 4 pi/pi | 4, 3 pi/2, 16/3, 15 pi/8, 32/5 | fail | fail | fail | S6: agrees with the G_N-slot at D = 4 and 5 only (Vol(B^3) = 2 pi (D-3)/(D-2), a coincidence), fails D >= 6; with a 4 pi-normalised Poisson constant only D = 4 |
| c5 thermal 8 pi/2 pi (the BH quarter) | 4 x5 | pass | - | - | survives S1 (D-independent in the Wald formula); the same atoms give T = kappa/2 pi and S = A/4 |
| c6 quadratic-EH 1/(1/4) | 4 x5 | pass | - | - | survives S1 (computed D = 4..8) |
| c7 Tangherlini (r_h kappa)^-2 | 4,1,4/9,1/4,4/25 | fail | pass (own) | fail | S5: see below |
| c8 static-patch channels 1 + dim SO(D-1) | 4,7,11,16,22 (stabiliser dimension verified numerically, D = 3..6) | fail | fail | fail | orphan; no coefficient in any action counts Killing generators |
| c9 GB-shift 2(D-2)(D-3) | 4,12,24,40,60 | fail | fail | pass (own) | MM closure exists only at D = 4 |
| c10 response N^2, N = 2 | 4 x5 | pass | - | - | survives S1; equals the record's d-lock (kappa = 1/2 in every d) |

- **Survivors under the one-generator premise: c2, c5, c6, c10** (the D-independent class). They are four structurally different claims with the same D-lift, silent on a0(z) (they fix the coefficient, not which density enters), so nothing here separates them. This class is exactly what the record's d-lock (Z_d^2 = 64 pi/(d(d-1)), N = 4 constant) assumes; agreement with it is consistency, not support.
- **S4 (a0(z), computed, flat LCDM Omega_m = 0.315):** a0(z)/a0(0) for 'Lambda only' = 1; for c1 read as the trace of the total source, |T| = rho_m + 4 rho_Lambda: 1.12, 1.31, 1.92, 2.31, 2.74 at z = 0.5, 1, 2, 2.5, 3; for a0 ~ H(z): 1.32, 1.79, 3.03, 3.77, 4.57. So the reading '4 = D' is not silent: on the total source it puts the framework on the evolving side of its own decisive test; on Lambda alone it is flat and gives no separation from any other candidate.
- **S5 (horizon extremality; c7 and the extremal reading of c4).** For Kerr-Newman, A kappa^2/pi = (r_+ - r_-)^2/(r_+^2 + a^2) <= 1 because (r_+^2 + a^2) - (r_+ - r_-)^2 = a^2 + r_-(2 r_+ - r_-) >= 0, equality iff a = 0 and r_- = 0 (Schwarzschild); 2e5 random KN horizons give max 0.9995. By 2-d Gauss-Bonnet the mean Gauss curvature is K_bar = 4 pi/A for any S^2 horizon, so **kappa <= (1/2) sqrt(K_bar)** and a0 = (1/2) sqrt(G rho_Lambda) is the supremum of kappa over KN horizons with K_bar = rho_Lambda. Reissner-Nordstrom: A kappa^(D-2) = Omega ((D-3)(1-q^2)/2)^(D-2), maximal at q = 0, D = 4, 5, 6. Myers-Perry single spin (kappa, A, Omega_H from the standard formulas, validated here by the Smarr relation for D = 4..7 and the Kerr/Tangherlini limits): maximal at a = 0 for D = 4, 5 (max 3.1416 = pi, 19.74 = 2 pi^2); **not for D = 6, 7** (the ultraspinning branch: max over tested spins 1.6e4 versus 133 at D = 6). So the 'sup kappa' reading is a D <= 5 statement; it relocates the puzzle to 'K_bar = rho_Lambda' (p04's formulation 3) and 'why the supremum'. I have not searched the literature to see whether A kappa^2 <= pi is already known.

## 5. MacDowell-Mansouri / Euler / Noether (task 3)
Computed in `x1_05` (variable held fixed: L; the a0-surface is the sphere r = Z L/2 = 2.894 L, which lies beyond the static patch r < L, in the region where xi = d_t is spacelike; the charge formula is analytic across it up to an orientation sign).
- **Euclidean action:** int_{S^4} E4 = 64 pi^2 = 32 pi^2 chi (chi = 2); c_E = L^2/(64 pi G); c_E x 32 pi^2 x 2 = pi L^2/G = S_dS = A_dS/4G; on-shell EH action -pi L^2/G. Verified.
- **Iyer-Wald charge** (computed from the metric): Q(r) = r^2 f'(r)/(4G) for any static f; Schwarzschild M/2 at every radius; dS: Q(r) = -r^3/(2 G L^2); at r = L, |Q| = kappa A/(8 pi G) = L/(2G) (kappa = 1/L), S = 2 pi Q/kappa = pi L^2/G. The Noether entropy S_N(r) = -pi r^3/(G L) versus the area law pi r^2/G: ratio r/L, equal only at r = L. The Euclidean EH action of the ball and the Euler-term action inside r (chi(r) = 2 (r/L)^3) are the same r^3 function. **Three normalisations of S_dS agree at r = L and disagree at r = Z L/2**: area 8 pi/3 = 8.38 S_dS, Noether 24.25 S_dS, chi(r) = Z^3/4 = 48.5.
- **pi-content (exact):** (Z/2)^n has pi-power n/2 (n = 0..5 computed). Only even-n quantities (area, curvature, A Lambda) can be rational x pi^k at the a0 radius; the Noether charge (needed 'unit' G|Q|/L = Z^3/16 = 12.124, pi^(3/2)), Noether entropy (pi Z^3/8 = 76.18, pi^(5/2)) and Euler number (Z^3/4 = 48.50, pi^(3/2)) cannot equal 1, 2, pi, 2 pi, 4 pi, 8 pi, 16 pi, 3 pi, 2 pi^2, 8 pi^2 or 32 pi^2 (checked; exact reason above). The r at which each equals a unit is (2u)^(1/3) L for the charge (1.26, 2.32, 2.93, 8.58 for u = 1, 2 pi, 4 pi, 32 pi^2; the near miss u = 4 pi gives 2.93 versus 2.89, a 1.2% coincidence excluded by the pi-power argument). Rescaling xi by Z^(+-1) (normalising to surface gravity a0) shifts the pi-power by 1/2, but that inserts a0, and S = 2 pi Q/kappa is normalisation-independent (pi^(5/2)).
- **Euler-term deformation (D = 4):** E_GB^{abcd} = 2R^{abcd} - 2(g^{ac}R^{bd} - ...) + R(g^{ac}g^{bd} - ...) verified by finite differences (D = 4, 5); on dS it is 2k(g g - g g); Q_alpha(r) = (1 + 4 alpha/L^2) Q_EH(r); dS horizon entropy A/4G + 4 pi alpha/G (Jacobson-Myers); MM/Kounterterm alpha = -L^2/4 gives **Q_MM(r) = 0 for every r and S_MM = 0**, consistent with F = 0 on S^4. The Gauss-Bonnet field-equation tensor vanishes identically in D = 4 (max 1.3e-11 over 30 random tensors; 1885 in D = 5, control), so alpha changes no classical equation. Hence an absolute condition 'Q(r_a0) = unit' is alpha-dependent while a0 = (1/2) sqrt(G rho) is an equation-of-motion statement: such a condition cannot be its origin. Only ratios of areas (G-free, alpha-free) can.
- **Is A Lambda = 32 pi^2 'Euler coefficient x A'?** S_{a0} = A_{a0}/(4G) = (8 pi/3) S_dS = (16 pi/3) x (c_E 32 pi^2) = (Z^2/2) instanton units (agrees with lane A). Not an integer, not a rational; the statement 'S_a0 = 16 pi/3 Euler units' is A Lambda = 32 pi^2 rewritten (checked), G- and L-free; it adds nothing.

## 6. What is NOT established
- That no single generator exists: only that the D-lifts of the listed instances are incompatible and that no D-dependent formula built from Omega_{D-2}, (D-2)/(D-3), (D-3)/2 reproduces them together. A D = 4-specific structure (self-dual/anti-self-dual SU(2) x SU(2) splitting behind the topological family) is not excluded by anything here.
- Which candidate origin, if any, the puzzle's 4 has. The four survivors are indistinguishable; c7 is consistent with itself only; nothing is tested against data except the a0(z) reading of c1.
- The premise itself (that the puzzle's 4 must have a D-lift equal to some slot's). The puzzle has no D != 4 completion in the record; 'failing' means inconsistency with another computed instance, not with data.
- Conventions: kappa_g^2 = 32 pi G is the tensor-canonical convention (16 pi with e_ij e_ij = 2 per polarisation, lane C); G_N is the force-law constant (Omega_{D-2} G_N rho = Lap Phi); lane F used a 4 pi-normalised Poisson constant (G_N' = 2(D-3)G_E/(D-2)), with which the c4 coincidence at D = 5 disappears (checked).
- Myers-Perry kappa and A are quoted from the standard literature and validated only by the Smarr identity (D = 4..7) and the Kerr/Tangherlini limits; the D = 6, 7 failure of extremality uses them and the single-spin family only. The Iyer-Wald general-D charge was computed for D = 4, 5, 6 (the D-dependence is the measure r^{D-2} Omega_{D-2}).
- Rows R01, R02, R16, R24-R27 take their values from definitions or from `x1_01` rather than re-deriving them in `x1_03`. Decompositions are labels backed by the derivations, not unique numerics (section 2).
- The a0(z) numbers assume flat LCDM (Omega_m = 0.315, radiation neglected) and use only the stated readings; they are consequences of those readings, not a claim that any data favour one.
- Not investigated: heat-kernel/Seeley-DeWitt as a common origin of (4 pi)^(D/2) in loops and the GB constant beyond the Gaussian remark; Lovelock/Chern-Simons gravity in D = 5, 7 as a MacDowell-Mansouri analogue; a two-parameter (alpha, a0) family.

## 7. Verdict and surviving second-prediction tests
**NOTHING NEW on the derivation; SHARP NO-GO (scoped) for (i) one D-formula generating the '4's, (ii) a Noether-charge or Euler-unit origin of A Lambda = 32 pi^2. kappa = 1/2 stays FITTED.** What the lens adds: the constants of the 32 pi family split into a Gauss/Einstein class (E8 = 2 x solid angle at D = 4 only), a topological class ((2n)! Vol(S^2n)/2), and thermal/angle factors; the puzzle's 4 is the one atom without a derivation; and the 'coincidences' the brief listed (1/(64 pi G) twice; 32 pi^2 = 2 (4 pi)^2 = 8 (2 pi)^2; S_dS = 2 instanton units) are D = 4 accidents of structurally different factors.
Surviving tests (none is runnable on existing data except the first, and the first is the record's own):
1. a0(z): flat (Lambda alone) versus evolving. A candidate that reads the 4 as a trace over the total source (c1) predicts a0(2.5)/a0(0) = 2.31; a0 ~ H predicts 3.77; the framework's law is 1.00.
2. Any D != 4 completion must state its N(D): constant 4 (the class {c2, c5, c6, c10}, the record's d-lock), 4/(D-3)^2 (horizon reading), 2(D-2)(D-3), ...; they differ from D = 5. No data.
3. Equation-of-motion invariance: any origin defined through an absolute Noether charge or entropy must fix the Euler coefficient alpha (MacDowell-Mansouri alpha = -L^2/4 makes every such charge vanish).
4. Horizon extremality ('a0 = sup kappa at K_bar = rho_Lambda'): passes KN, RN, MP D <= 5, fails MP D = 6, 7; a D-independent principle cannot rest on it.
Files: `x1_01`..`x1_06` (.py and .out), `x1_atoms.json`, `x1_dlifts.json`, `x1_ledger.json`.
