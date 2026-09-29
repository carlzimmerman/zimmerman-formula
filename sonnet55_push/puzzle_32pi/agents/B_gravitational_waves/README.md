# Lane B: gravitational waves and the graviton -- where 32 pi comes from, and whether the puzzle is a GW/graviton statement

(c = G = 1 unless stated; puzzle: Lambda = 32 pi a0^2, i.e. a0 = (1/2) sqrt(G rho_L), kappa = 1/2 FITTED.)

## Bottom line
1. **Verdict: SHARP NO-GO (scoped to the GW/graviton quantities listed below).** No gravitational-wave or graviton quantity gives a0 = (1/2) sqrt(G rho_L) with the 1/2 (or 32 pi) derived; every candidate needs the same inserted coefficient, an hbar (60 orders too small), or leaves its validity range. kappa = 1/2 stays FITTED.
2. **32 pi is exactly located, and it has nothing to do with Lambda.** In every GW/graviton place it is the normalisation of the graviton kinetic term: 32 pi = 8 pi x 4 (Isaacson: 4 = 1/(1/4), the second-order Ricci coefficient) = 16 pi x 2 (canonical) = 8 x 4 pi (one-graviton exchange: tensor structure x Poisson Green function). GW memory has no pi at all (4G/r = 16 pi G/(4 pi)).
3. **Sharp structural result (pi-class):** the puzzle needs a pi^(-1/2) in a0/(cH) = sqrt(3/(32 pi)). A graviton/GW quantity built with the canonical normalisation either (K) is a rational-dressed multiple of cH -- algebraic, e.g. the record's graviton-bath chain gives exactly a0 = cH/2 -- or (E) goes through the Isaacson energy and gives X^2 = 8 pi f, so it needs a GW energy fraction f = 1/(32 pi) (and that number is polarisation-state dependent: 1/(64 pi) for circular). Neither route can produce 1/2 without inserting a 1/pi.
4. **The one thing GW language does buy (a relocation, not a derivation):** a0 = (1/2) w h0 c with the 1/2 = the geodesic-deviation 1/2 (derived); so the puzzle is equivalent to "strain rate w h0 = vacuum free-fall rate sqrt(G rho_L)" (coefficient 1, pi-free). The 32 pi then appears only when that wave's energy is booked with the canonical Isaacson 1/(32 pi G). Why the coefficient is exactly 1 is not supplied.

## 1. Exact origin of 32 pi (`g01_origin_of_32pi.py`, 21/21 recomputed checks incl. 4 mutation controls, plus 4 bookkeeping lines)
Everything is recomputed with sympy from the metric (Ricci/Riemann of eta + eps h, truncated at O(eps^2)).
| where 32 pi appears | exact decomposition (verified) | check |
|---|---|---|
| canonical TT graviton, kappa_g^2 = 32 pi G | sqrt(-g)R at O(eps^2) = -(1/4) d_l h_ij d^l h_ij (up to a total derivative, Euler-operator test); (1/16 pi G)(1/4) = (1/2)/(32 pi G) | A1-A3, control C1 (1/3 rejected) |
| Isaacson t_mn = (1/32 pi G)<d_m h_ab d_n h_ab> | exact plane-wave Ricci: <R_uu^(2)> = -(1/4)<h'_ab h'_ab> (the 1/4 = 1/2 - 1/4 after averaging by parts), t = -(1/8 pi G)<G^(2)>, so 32 pi = 8 pi x 4; second route: canonical stress tensor of the quadratic action = 2 x 1/(64 pi G) | B1-B7, control C2 (1/16 pi G rejected) |
| flux c^3 w^2 h0^2/(32 pi G) | rho = w^2 (A^2+B^2)/(32 pi G) from <G^(2)_tt> (phase-independent); null (t_tz = -rho), traceless | B2-B4 |
| one-graviton exchange | V = -kappa^2 m1 m2/(32 pi r): 32 pi = 8 (vertices x de Donder tensor structure 1/2) x 4 pi (Fourier transform of 1/q^2); kappa^2 = 32 pi G gives Newton | E1-E3, control C4 (16 pi G gives G/2) |
| geodesic deviation | R_0x0x = -(1/2) d_t^2 h_xx, so a = (1/2) w^2 h r | D1 |
| **identity** | rho_GW = a_tid^2/(8 pi G) with a_tid = (1/2) w h0 (peak tidal acceleration at r = c/w): Isaacson = (Newtonian field-energy 1/8 pi G) x (geodesic 1/2)^2 | D2, control C3 |
| GW memory | 16 pi G/(4 pi) = 4G/r; linear memory (Favata review, arXiv:1003.3486 eq. 11) and nonlinear memory (its eq. 12, sourced by the same T^GW) carry no pi | F1-F4 |

So "8 pi G x polarisation/average factor 4" is right in the precise sense above. None of these is connected to Lambda: Lambda enters a GW quantity only through the frequency scale H or the energy fraction f.

## 2. The puzzle in GW variables (`g02`, Q1)
- Isaacson identity => a0-wave (peak tidal acceleration a0 at its reduced wavelength) has w h0 = 2 a0 = sqrt(G rho_L) = 1/t_L and <hdot_ab hdot_ab> = G rho_L, i.e. rho_L = 32 pi rho_GW. Checked in Q1d/Q1e (unique root kappa = 1/2 at strain rate 1/t_L).
- Omega_GW = (w h0)^2/(12 H^2): pi cancels between Isaacson and Friedmann (Q1f). At w = H the a0-wave has h0 = 2/Z = 0.3455.
- The identity rho = a^2/(8 pi G) is for linear polarisation; for circular polarisation with the same peak tidal acceleration it is a^2/(4 pi G), so the "needed f" is 1/(32 pi) or 1/(64 pi) (Q1k, control C1b). The GW reading of 32 pi is not state-independent.
- For every natural radius r = lambdabar, lambda/2, lambda the exponent of pi in X^2 = 8 pi f (r/lambdabar)^2 is odd (1, 3, 3); the radius choice cannot reach pi^0 (Q1j). Only a sqrt(pi) length (a Gaussian volume/norm, cf. p09's nonlocal-filter loophole) could.

## 3. Candidates, pi-content pre-declared then checked (`g02_gw_candidates_pi_count.py`, 35/35)
Declared in the script header before any evaluation; a0 = X sqrt(G rho_L), target X^2 = 1/4 (pi^0).
| candidate | predicted | found | verdict |
|---|---|---|---|
| Q1 classical Isaacson background, energy f rho_L, peak tidal accel at lambdabar | X^2 = 8 pi f | X^2 = 8 pi f (pi^1); f = 1 gives X = 5.01; a0 needs f = 1/(32 pi) = 0.00995, i.e. Omega_GW = 0.0068 | needs a 1/pi energy fraction; f = 1/32 rejected (control) |
| Q1 data | -- | w = 1/3 background with that f is 1.9e3 above a generous N_eff allowance for w/H0 >~ 7e7 (inside the horizon at BBN); f = 1: > 1e5 | excluded in that window. **Window 10 < w/H0 < 1e8 NOT evaluated** (dark radiation of Omega = 0.007, not Lambda-like; no claim). At w = H: h0 = 0.35 (f = 1/32 pi) or 3.46 (f = 1) with no scale separation, outside Isaacson validity |
| Q2 memory kick of a burst carrying the Hubble-sphere energy | X^2 = eta^2 (8 pi/3), eta pi-free | Delta h_max = 2 (nonperturbative); eta = ratio of angular integrals over one sphere: rational for 6 random rational weights (pi cancels; control with pi in the weight is non-rational); a0 needs eta = 1/Z, eta^2 = 3/(32 pi) | not reachable with rational eta |
| Q3 de Sitter Bunch-Davies tensor amplitude | X^2 = (32/3) hbar G H^2 | P_T = 16 hbar G H^2/pi = 2 hbar H^2/(pi^2 M_p^2) reproduced from kappa_g^2 = 32 pi G; X ~ 3e-61; energy per e-fold/rho_L = (4/3) hbar G H^2/pi ~ 1e-122 | 60 orders short and hbar-dependent (a0 has no hbar) |
| Q5 EOS of a GW/graviton gas | (rho+p)/rho = D/(D-1) | exact for d = 2..6 (traceless null tensor, <n_i n_j> = delta_ij/d) | see section 5 |
| Q6 Hubble-frequency quanta filling the Hubble sphere | -- | N = 1/(2 G H^2) = S_dS/(2 pi) gives rho_L; classical amplitude h0 = 2 sqrt 3 | condensate reading consistent, amplitude O(1), no a0 |
Own error caught by the script (Q2c): my first hand estimate of the eta needed was 3/(16 pi); the check failed, and the correct value is 1/Z (a = eta H, a0 = H/Z).

## 4. The record's graviton-bath chain with the canonical graviton (`g03_graviton_bath_pi_class.py`, 14/14)
Chain from `real_research/reviews/mi_graviton_bath_ctp_2026.py` (its assumptions A1-A7 taken as given, NOT audited here): S_dS = pi/(G H^2), T = H/2pi, eps_1 = m <h^2>, eps_tot = S_dS eps_1, a0^2 = 3 eps_tot H^2, kappa^2 = 8 pi eps_tot. That lane found kappa = 0.500 / 1.447 / 2.047 for three normalisations and named the question "why eps_tot = 1/(32 pi)". Added here:
- With the canonical two-point function (32 pi G x <phi^2>, <phi^2> = T^2/12 thermal or (H/2pi)^2 per e-fold, both derived) and ANY rational dressing (m, polarisation count, rational knobs c1..c6): G, H **and pi all cancel**, eps_tot is rational (2m/3 thermal, 8m de Sitter), (a0/cH)^2 = 2 c1 c3 c4 c6 m/(3 c2^2), so a0/(cH) is algebraic and kappa^2 = 8 pi eps_tot is a rational multiple of pi (B3-B6). S_dS x <h_ij h_ij> = 4/3 (thermal), 16 (de Sitter): rational (B9).
- The puzzle needs eps_tot = 1/(32 pi), (a0/cH)^2 = 3/(32 pi): not rational; equivalently m = 3/(64 pi) (B7, B8). Transcendence of pi is used (Lindemann); sympy checks irrationality of the target.
- The record's m = 1/8 gives eps_tot = 1/12, kappa = sqrt(2 pi/3) = 1.447 and **a0 = cH/2 exactly** (Z = 2, not 5.789); two polarisations give 2.047 (B4, B5). The loose normalisation <h^2> = G T^2 reproduces kappa = 1/2 (control C1: the test detects it as non-rational) and differs from the canonical one by exactly 32 pi/12 = 8 pi/3 (C2): it is the canonical graviton with its 32 pi/12 removed.
- Loophole, reported not closed: with a pi-free mode count N = 1/(G H^2) (the "area in Planck units" convention, cf. arXiv:1701.08776, abstract only) kappa^2 = 16 m/3 is rational, m = 1/8 gives 2/3 and kappa = 1/2 needs m = 3/64. The pi obstruction is lifted but m is a free rational with no principle: not a no-go, not a derivation (C3).

## 5. Formulation 6 (memory moment M1 = (4/3) t_L, radiation enthalpy 4/3)
- The record's "memory" is the first moment of a time-nonlocal inertia kernel in its modified-inertia worldline action (`real_research/reviews/mi_N_count_and_kappa_iff_2026.py` Part C, Lean `REV_kappa_memory_moment_dimension`), not GW memory. GW memory (a DC strain offset) is sourced by dE/dt dOmega with 4G/r and has no Hubble time scale; I found no computed link between them.
- What GW physics does supply exactly: any GW/graviton gas has p = rho/d, (rho+p)/rho = D/(D-1), the record's "enthalpy premise" for every D (Q5), because the Isaacson tensor is null and traceless (g01 B3/B4). So IF M1/t_L = (rho+p)/rho then kappa = (2/3)/(4/3) = 1/2 for any null gas.
- What it does not supply: the premise M1/t_L = (rho+p)/rho itself, and the identification of t_L (the vacuum's free-fall time) with a GW gas: w_GW = 1/3 vs w_L = -1, and rho_GW = rho_L is excluded (Q1). The 4/3 and the t_L belong to different components.

## 6. Not established
- That no GW/graviton principle exists: I checked Isaacson/geodesic-deviation, memory, Bunch-Davies, the canonical graviton-bath chain, the GW-gas EOS and condensate counting; not nonlinear (h ~ 1) graviton dynamics, backreaction/loop effects, nonlocal filters, or the mode-counting variant of section 4 (C3).
- The record's A1-A7 (incoherent sum, a0^2 = 3 eps H^2, the accelerated-worldline projection) are used as stated, not derived; the class-K result holds for every rational choice of them, not for irrational ones.
- The 10 < w/H0 < 1e8 GW window (section 3) is not tested against data.
- The P_T formula is derived here from kappa_g^2 = 32 pi G and matches the standard tensor power; I did not re-read it in a source (arXiv:astro-ph/0210603 was opened at abstract level only and is not cited for it). arXiv:1701.08776 was read at abstract level only.
- Anything about why kappa = 1/2. kappa = 1/2 stays FITTED; "theory closed" is not claimed.

## 7. Verdict
**SHARP NO-GO**, scoped: in the GW/graviton sector the 32 pi is the canonical graviton normalisation, and no physical quantity there returns a0 = (1/2) sqrt(G rho_L) without inserting a 1/pi (energy route: f = 1/(32 pi); kinematic/bath route: algebraic multiples of cH only; memory route: rational eta cannot give eta^2 = 3/(32 pi)), an hbar (Bunch-Davies), or leaving the Isaacson regime. The constructive residue is the relocation in section 2: in GW variables the 1/2 is the derived geodesic-deviation 1/2 and the open coefficient is "w h0 t_L = 1".

## Scripts (all committed here; `run_all.sh` reruns them in ~2 min; sympy 1.13.1, mpmath 1.3.0, numpy 1.26.4)
| script | result |
|---|---|
| `g01_origin_of_32pi.py` (+ `.out`) | 21/21 checks incl. 4 mutation controls; 4/4 bookkeeping |
| `g02_gw_candidates_pi_count.py` (+ `.out`) | 35/35 incl. controls C1, C1b, C2, C2b |
| `g03_graviton_bath_pi_class.py` (+ `.out`) | 14/14 incl. sensitivity control C1 and variant C3 |
Process notes: the first g01 used exact sympy matrix inverses and was too slow (killed); it was rewritten with an O(eps^2)-truncated inverse, which is exact to the order needed. Pseudo-checks that are pure arithmetic restatements are labelled BOOK and counted separately. No other file in the repo was edited or committed.
