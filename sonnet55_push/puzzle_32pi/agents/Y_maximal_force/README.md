# Lane Y (W14) -- maximal force F_max = c^4/4G, the vacuum tension, and the exact de Sitter C-metric: the rational-in-H branch

## Bottom line (verdict: SHARP NO-GO, scoped to the principles declared in `PREDECLARED.md`; kappa = 1/2 stays FITTED)
1. **No tension / string / maximal-force construction fixes a0/(cH) without a free parameter.** In the exact dS C-metric a0 := A (the 4D proper acceleration) is a free parameter of a two-parameter family (m A, A/H). Of nine declared principle-combinations the only interior fixed point (string force = vacuum force across the same horizon, at the extremal boundary) gives **A/H = 2.448** (a0 = 2.45 cH, Z = 0.41), not 1/6, 1/2 or 1/Z; every other combination is FAMILY, EMPTY or the endpoint A/H = infinity.
2. **The "6" in F_Lambda = 6 F_max (vacuum tension x horizon area, pi-free, hbar-free) is the Friedmann relation H^2 = 8 pi G rho/3 written as a force** (exact equivalence, script), and by dimensional analysis any force built from (c, G, Lambda) is a pure number times c^4/G. Verlinde's a0 = cH/6 is then F_max/(3 M_H) only with the mass 3 M_H = F_Lambda L/c^2 **inserted**: a0/(cH) = F_max/F_Lambda is a restatement. Of seven natural Lambda-defined masses only that one (built after I saw the target: void) gives 1/6; the rest give 1/2, 1/4, 1/4, 2/(3 pi), 1/(3 pi), 3 sqrt3/4.
3. **Verlinde's own 1/6 is (d-3)/((d-2)(d-1)) at d = 4** (also 1/6 at d = 5); the 8 pi G's of his eqs (1.5) and (1.6) cancel. It is not an F_max statement.
4. **New exact facts (scripts):** in the dS C-metric the acceleration horizon and the cosmological horizon are one horizon; T_bh > T_(acc/cosm) strictly except at extremality (so "T_acc = T_cosm" is not a condition); F_max saturation (27 m^2 A^2 = 1) leaves no static black hole at any finite Lambda; the **largest string force of a static black hole is F_max [1 - sin(th)/sin(2 pi/3 - th)], th = (pi - 2 arctan(A/H))/3** (exactly F_max/2 at A = H; about 0.77 (A/H) F_max for A << H, i.e. <= 0.12 F_max at A = H/6).
5. **A rational Z = 6 is a different law** (a0 = cH_Lambda/6): Lambda = 108 a0^2 (not 32 pi), G rho_Lambda = 4.297 a0^2, A_a0 Lambda = 108 pi (not 32 pi^2), kappa = 0.4824, Omega_Lambda 7.4% higher (0.973 vs 0.906 at the record a0). The data do not separate it (0.29 sigma); on the pure-Lambda footing 6 (+1.6 sigma) and 5.789 (+1.3 sigma) both sit above Z_Lambda = 4.9 +/- 0.6.

**Result counts.** 113/113 checks pass (29 + 24 + 23 + 23 + 14), 25 of them controls that must fail; all five scripts exit 0 (`./run_all.sh`, about 22 s). `PREDECLARED.md` sha256 = `77fd9f5398faa909f7328988f697379acbf98c44f984f6095a97df476d5cb9b7` (written before any script; every script re-checks it).

## 1. What was declared first (PREDECLARED.md, hashed)
Targets T6 (q = a0/(cH) = 1/6), T2 (1/2), TF (1/Z = sqrt(3/32 pi)); decoys 1/3, 1/4, 1/5, 1/7, 1/8, 1/9, 1/10, 1/12; hit = exact equality only. Success = a construction whose declared principles fix q with no free parameter and give a target. Identification of a0: F_max/M for the static bookkeeping masses; A (Dias-Lemos a_4 = A) for the C-metric; H = H_Lambda throughout (pure-Lambda construction, so the comparison footing is rho_Lambda).
Disclosure written in the file: I had read Dias-Lemos, Gibbons and Verlinde before declaring; and by hand I expected F_Lambda = 6 F_max, T_b = T_c only at degeneracy, and saturation + extremality to force H = 0. The mass entry M_e (vacuum in a horizon shell of thickness L) was added after I noticed M = 3 M_H gives 1/6 and is void as evidence.

## 2. Results

### Part S: static bookkeeping (`y01_static_bookkeeping.py`, 29/29)
- **S1.** F_Lambda = rho_L 4 pi L^2 = 3 c^4/(2G) = **6 F_max**, no Lambda left; (c, G, Lambda) have det = -2 (no dimensionless combination; control: adding hbar allows one); F_Lambda = 6 F_max <=> rho = 3 H^2 c^2/(8 pi G): Friedmann. Mutations rho = Lambda/4 pi (12), area 2 pi (3), F_max = c^4/2G (3) all fail to give 6. In D dimensions F_Lambda/(c^4/4G) is 6 pi L (D = 5), 40 pi L^2/3 (D = 6): the pure number exists only in D = 4 (consistent with Gibbons' remark that for n > 4 there is only a bound on F/D^(n-4)).
- **S2.** g_H = G M_H/L^2 = F_max/M_H = cH/2, M_H = rho_L (4 pi/3) L^3 (Schwarzschild mass of r_s = L); it is the trivial q = 1/2.
- **S3.** Mass menu, a0 = F_max/M, q = F_max/(M c H): M_a (Hubble-ball vacuum mass) 1/2; M_b (Komar mass of the dS horizon) 1/4; M_c (Nariai) 3 sqrt3/4; M_d (Lambda zero-force sphere at L) 1/4; **M_e = rho A_H L = F_Lambda L/c^2 = 3 M_H: 1/6 (void)**; M_f (rho x hemisphere of S^3, pi^2 L^3) 2/(3 pi), Z = 3 pi/2; M_g (full S^3) 1/(3 pi). Census: 4 of 7 rational, 2 target hits (M_a -> T2, M_e -> T6 void), 2 decoy hits (1/4 twice), TF never, 1/5 and 1/7 never. The 6 needs the mass as input; the mass with the c H-force property (m c H = F_Lambda) is again 3 M_H (D5 of y05).
- **S4 (Verlinde, arXiv 1611.02269, PDF opened).** From his (1.5)+(1.6): a_M/a0 = (d-3)/((d-2)(d-1)); pi and G cancel; d = 3..7: 0, 1/6, 1/6, 3/20, 2/15. It equals the horizon-force number (D-1)(D-2) only at d = 4.

### Part C: the exact dS C-metric (Dias-Lemos form, arXiv hep-th/0301046, PDF opened)
`y02_cmetric_exact.py` 24/24, `y03_cmetric_horizons.py` 23/23, `y04_principle_table.py` 23/23, `cmetric.py` (mpmath, 50 digits).
- **C0.** R_mu nu = Lambda g_mu nu holds identically (sympy) for F = -1/(ell^2 A^2) - 1 + y^2 - 2 m A y^3, G = 1 - x^2 - 2 m A x^3 (controls: wrong sign of the Lambda term and a wrong cubic both fail); m = 0 is de Sitter (Kretschmann 24/ell^4); a_4 = A exactly at m = 0, independent of ell (the 5D/embedding acceleration is sqrt(A^2 + H^2)).
- **C1.** Deficit at a pole 2 pi[1 - (kappa/2)|G'|] verified against proper circumference/radius; tension = deficit/(8 pi); G contains no ell, so **the string tension depends on s = m A only, not on Lambda**; mu -> mA at small s (F = M a). Regular at the north pole, the string on the south axis has tension mu(s) (strictly increasing, < 1/4).
- **C2 (P_none).** Both poles regular is impossible for m A != 0 (999 grid points: |G'(x_n)| > |G'(x_s)|); at m A = 0 a pure dS observer has arbitrary A. **EMPTY / q free.**
- **C3 (P_sat).** mu = 1/4 iff 27 s^2 = 1 (discriminant of G); with Lambda > 0 there is no static region there (F(-x) = -G - h^2 and max F = -h^2 < 0). **ENDPOINT q = infinity.**
- **C4 (P_ext).** Double root of F: 27 s^2 (1 + h^2) = 1, i.e. **27 m^2 A^2 = 1 - 9 m^2 Lambda** (Dias-Lemos' condition, reproduced independently). The extremal mass is R/(3 sqrt3), R = 1/sqrt(A^2 + H^2) (Nariai mass of the accelerated observer's horizon). Along it the largest string force is the closed form in bottom-line item 4 (checked to 3e-49); it tends to F_max only as A/H -> infinity. **FAMILY (curve).**
- **C5 (P_eq).** On 2301 grid points F has exactly two horizons in the physical range (Descartes: at most 2 positive roots of r f); |F'(y2)|/|F'(y3)| = (y2 - y1)/(y3 - y1) < 1 always, so the black-hole horizon is strictly hotter than the acceleration/cosmological one and equality is only extremality (both T = 0). m = 0 gives T = sqrt(A^2 + H^2)/2 pi. The brief's T_acc = T_cosm has no content (one horizon, as Dias-Lemos state). **Same set as C4.**
- **C6 (P_bal), my addition to the brief's list, declared before computing.** String force 4 mu F_max = vacuum force rho_L x Area of the SAME solution's horizon. Area formula checked against its limits: a = H^2 Area/(4 pi) = 1 at m = 0 and -> 1 - 4 mu as H -> 0 (a straight string through a dS horizon removes 4 mu of it). The balance is a curve in (s, h) from (mu = 3/14, H -> 0) to the extremal boundary: **FAMILY**. On the extremal boundary alone there is exactly one solution: **A/H = q* = 2.4481112533319394966, m A = 0.178160, string force 0.735089 F_max, FIXED-NON-TARGET.** It is not sqrt 6 = 2.44949 (difference 1.4e-3: control that a near-coincidence is not a hit). Mutations move it (deficit 4 pi G mu: 1.2577; rho = Lambda/4 pi: 4.7818).
- **Lambda = 0 control.** At h = 0 extremality and saturation coincide (27 s^2 = 1) and A is not constrained at all: the principles fix m A, never A alone.

| principle set | label | q = A/H |
|---|---|---|
| R1 (regular north pole, string south) | FAMILY | free |
| R1 + C2 (no string, no strut) | EMPTY (mA != 0) / free at mA = 0 | -- |
| R1 + C3 (F_max saturation) | ENDPOINT | infinity |
| R1 + C4 (extremal) | FAMILY (curve) | (0, infinity) |
| R1 + C3 + C4 | ENDPOINT | infinity |
| R1 + C5 (thermal equality) | = C4 | boundary only |
| R1 + C6 (force balance) | FAMILY (curve) | (2.448, infinity) |
| **R1 + C6 + C4** | **FIXED-NON-TARGET** | **2.44811** |
| R1 + C6 + C3 | EMPTY | -- |
Census of all 8 fixed outputs (7 masses + q*): T2 once (trivial), T6 once (void), TF never, decoy 1/4 twice, zero hits from the C-metric. **DERIVATION criterion not met.**
Structural corollary: every condition on (s, h) is algebraic, so an algebraic q can never be 1/Z = sqrt(3/32 pi) (Lindemann, imported); the family could in principle have hit 1/6 or 1/2, and does not.

### Part D: consequences of a rational Z (`y05_consequences_and_data.py`, 14/14; data quoted from lane V, not re-derived)
- Z = 6 vs Z = sqrt(32 pi/3) vs 2 pi: Lambda/a0^2 = 108 / 100.53 / 118.4; G rho_L/a0^2 = 4.297 / 4 / 4.712; A_a0 Lambda = 108 pi / 32 pi^2 / 12 pi^3 (so the Chern-Gauss-Bonnet coincidence and kappa = 1/2 belong to the framework only); Omega_Lambda coefficient Z^2 = 36 / 33.51 / 39.48, ratio 36/(32 pi/3) = 27/(8 pi) = 1.0743.
- a0 that reproduces Omega_Lambda = 0.685 at H0 = 67.4: 9.03e-11 (Z = 6) vs 9.36e-11 (framework). Predicted Omega_Lambda from the record a0 1.0766e-10: 0.906 (F, reproduces lane V) vs 0.973 (Z = 6); from the ensemble a0 1.097e-10: 0.940 vs 1.010.
- Offsets in sigma (ensemble E, 12.2%): rho_total footing F -0.25, V +0.04, M +0.42; **rho_Lambda footing (the natural one for a pure-Lambda construction) F +1.30, V +1.59, M +1.97**; with the record's 5.44%: rho_Lambda footing F +2.57, V +3.23. F vs V separate by 0.29 sigma: **not separable** (lane V: 1.8% total error needed).
- Against the data, only at the end: masses M_a (Z = 2) -7.4 sigma, Z = 4 -1.7 (rho_Lambda) / -3.3 (rho_total), the C-metric point q* (Z = 0.41) -20 sigma. Note M_f (Z = 3 pi/2 = 4.71) sits at -0.4 sigma on the rho_Lambda footing: one of seven declared masses falling within 0.4 sigma is a ~25% chance event for a 12% data scatter, it is a pi-branch (transcendental) reading with an inserted mass, and it counts as nothing.
- Evolution: a construction with H = H_Lambda gives a flat a0(z), the same as the framework; a Verlinde-type H0 footing would give a0 proportional to H(z). The rational coefficient does not change the flat-versus-H(z) question.

## 3. What is NOT established
- The identification a0 := A is a premise (exact for the origin at m = 0; for m != 0 the mass/acceleration of the black hole is ambiguous at O(1) near saturation: mu/(mA) goes from 1 to 3 sqrt3/4). Only the dimensionless A/H and the tension enter, not the mass, so the verdict does not depend on the mass definition, but a different identification of a0 (e.g. a horizon-averaged acceleration) was not tried. sqrt(A^2 + H^2) >= H cannot give q < 1.
- Only the uncharged, non-rotating dS C-metric with one string family (R1; the strut mirror R2 is not carried through); the thin-string tension = deficit/(8 pi) reading; no matter fields, no Kerr/charge, no Kastor-Traschen configuration (abstract seen via search only, not opened), no Podolsky-Griffiths (not opened), Anabalon et al. 1805.02687 (abstract page only, not used).
- That "principles are exhausted": nine combinations declared, including one of my own (P_bal); other principles (e.g. an extremum of the horizon area or entropy on the boundary curve) were not declared and not tried. The absence of an interior parameter-free point among them says nothing about principles I did not think of.
- q* itself is an output of an ad hoc balance; I do not claim it has any physical meaning beyond "the only fixed point of that balance", and it is 15-20 sigma from the data.
- The (r, theta) accelerating-black-hole parametrisation of the literature (a different mass parameter) was not used; no result depends on which mass parameter is called m.
- Gibbons's bound is used only through deficit = 8 pi G mu <= 2 pi.

## 4. Own errors, fixed openly
(1) First arXiv IDs recalled from memory pointed at other papers; the real IDs (hep-th/0301046 Dias-Lemos, hep-th/0210109 Gibbons) were found by search and opened before declaring. (2) y02: my first regularity mutation had a typo (2 kappa/4 = kappa/2, the original) and the control failed; corrected. (3) y03: the Dias-Lemos identity check had an extra factor 1/3 and failed; corrected (9 m^2 Lambda = 27 s^2 h^2). (4) y04: a bracket-free root-finder wandered to s > 1/sqrt27 (outside the family, where G has one real root) and returned a fake s for mu = 3/14; replaced by a bracketing solver plus an in-domain check. (5) I twice wrote vacuous `check(..., True)` lines and removed them. (6) The mutation "deficit 8 pi G mu -> 4 pi G mu" cannot move purely geometric outcomes (C3, C4); the README and script say so and the mutation is applied to S1 and C6, where it does move the result.

## 5. Sources actually opened
arXiv hep-th/0301046 (Dias, Lemos; dS C-metric, horizon coincidence, extremal condition, a_4 = A), arXiv hep-th/0210109 (Gibbons; F_max = c^4/4G, C-metric string bound, no n > 4 analogue), arXiv 1611.02269 (Verlinde; eqs 1.2-1.7, sections 4.2-4.3 for the origin of the (d-1) and (d-2)). Lane V's README for the data numbers.

## 6. Files and re-run
`PREDECLARED.md`, `PREDECLARED.sha256`, `common.py`, `cmetric.py`, `y01_static_bookkeeping.py`, `y02_cmetric_exact.py`, `y03_cmetric_horizons.py`, `y04_principle_table.py`, `y05_consequences_and_data.py` with `.out` and `y0*_results.json`, `run_all.sh` (needs sympy, mpmath). Run `./run_all.sh`; exit 0 = 113/113.
