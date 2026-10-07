# T6 deep-physics lane: families 215, 221, 263, 267, 269, 270 (extra-hard deep read)

Lane: `t6_deep_physics`. Criteria: `FROZEN_CRITERIA.md`. Working model: `WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md`.
Target: T = 1/sqrt(32 pi) = 0.0997356 (a0 = c^2 sqrt(Lambda/32 pi); kappa = 1/2 FITTED, stays fitted).
Screen: Q1 (derives a0?), Q2 (forced/chosen), Q3 (base rate p_base over F = {(p/q)pi^n, sqrt((p/q)pi^n): 1<=p,q<=12, n in -2..2}, distinct, N = 889; 1%-window share 0.0022).
Language: no "theory closed", no "data favour the framework", no DM particle. Both footings of a0 are IRRELEVANT here (no constant below lands near either footing; nothing below derives any acceleration).

All six families scored 0 in the abstract triage. Verdict of this deep read: **all six stay 0 as forcing results; zero constants land within 1% of T; the only structural material is analogy-grade (221 variational style, 267 settled/unsettled split, 269 gap mechanism, 215 continuum prescription).**

---

## Family 215 — Canonical O(3) continuum limit and exact O(4) mass asymptotics

Manuscripts read (pdftotext, full): `Exact-mass-asymptotics-for-the-two-dimensional-O4-lattice-model-October-5-2026/exact-mass-o4.pdf` (109 pp), `Sharp-mass-bounds-for-the-two-dimensional-O4-model-September-23-2026/paper.pdf`, `The-canonical-massive-continuum-limit-of-the-two-dimensional-O3-model-October-4-2026/massive-continuum-o3.pdf`, `An-Isolated-Particle-Pole-for-the-Two-Dimensional-O3-Spin-Field-October-4-2026/o3-particle-pole.pdf`.

**Main theorem (exact-mass-o4, Theorem 1.1, eq. 1.4).** For the nearest-neighbour O(4) model on the square lattice at inverse temperature beta, the full OS transfer gap (including rotation-invariant local-observable sectors, in units of one lattice time step):
  m_lat(beta) ~ 32 exp(pi/4 - 1/2) sqrt(beta) exp(-pi beta),  beta -> infinity.
The sharp-order bounds of the companion paper supply only existential c, C (mlat ~ c..C sqrt(beta) e^{-pi beta}), plus the all-temperature gap m_lat(beta) >= c exp{-pi beta - C(1+beta)log(2+beta)} > 0.

Extracted constants:
- C-A: amplitude A = 32 exp(pi/4 - 1/2) ~ 42.5669 (exact; the e makes it non-(p/q)pi^n).
- C-HMN: m/Lambda_MS = 32/(pi e) ~ 3.7470 (Hasenfratz-Maggiore-Niedermayer ratio, quoted p.4).
- C-flow: O(3) canonical continuum limit (massive-continuum-o3, eq. 1.4): beta_N = H + N/(2 pi) + O(log N) — the flow step 1/(2 pi).
- C-mix: mixing length X(beta) = C exp((4 pi - eta) beta) — exponent 4 pi (structural; xi ~ exp(2 pi beta) class).
- No 4 pi / 8 pi / 32 pi / 1/32 appears anywhere in the four manuscripts (grep-verified).

Screen: A miss 42582%, 32/(pi e) miss 3657%, 1/(2 pi) miss 59.6%, 2 pi miss 6200%, 4 pi miss 12500%. Q1 no, Q2 forced-within-O(n)-theory, Q3 p_base 0.089-0.994. Verdict: NOT APPLICABLE for every constant.

P1-P8 mapping: **P6 (the switch) — analogy-only.** The 2D O(n) model has NO phase transition: the gap is exponentially small but strictly positive at every beta, and the continuum limit exists for all beta -> infinity under a fixed canonical normalization (susceptibility + second-moment length). That is a smooth exponential crossover, not a threshold; the "canonical prescription" is a style match for how to *define* the interpolation, not a mechanism that produces a0. P1: DOES NOT APPLY (the amplitude is forced inside O(n) physics; nothing connects it to Lambda or G). P2, P5, P7, P8: DOES NOT APPLY.

## Family 221 — Mezard-Parisi formula for diluted spin glasses

Manuscripts read: `The-Mezard-Parisi-formula-for-diluted-spin-glasses-September-23-2026/paper.pdf`, `All-temperature-pressure-for-orthogonally-invariant-Ising-spin-glasses-September-25-2026/paper.pdf` (sibling, same structure).

**Main theorem (MP paper, Theorem 1.1).** For Poisson-diluted even-arity Ising models in the Panchenko-Talagrand class (factorization + positivity, first-moment integrability), the limiting pressure equals the infimum over finite hierarchy depths k and hierarchical trial laws nu of the cavity functional: p = inf_k inf_nu P_k(nu). The orthogonally-invariant sibling: pressure = variational formula in the edge-extended R-transform of the spectral law; zero-field ground-state energy by T -> 0.

Extracted constants: **NONE.** All 18+14 occurrences of pi in both manuscripts are generic measure symbols (pi = product measure, pi = quotient map) or arcsin(argument) bounds. No sharp numeric constant appears in any theorem.

Screen: nothing to screen. Q1-Q3 moot.

P1-P8 mapping: **P2 — TOOL (style only, no constants attach).** The MP principle is a legitimate structural model for the settling problem: a free energy over order parameters whose unique minimiser realises the target distribution. It is exactly the right *shape* for "relax toward rho_ph": hierarchical cavity trial laws are the spin-glass analogue of radial density profiles, and inf-over-hierarchies is the analogue of the JKO/Wasserstein gradient-flow structure of T3. But the theorem FORCES nothing here: it proves an equality for a specific Hamiltonian class with a specific cavity functional; it provides no functional whose minimiser is rho_ph and no rate Gamma. Consistent with, not additive to, the T3 JKO reading. All other pieces: DOES NOT APPLY.

## Family 263 — Ionization and generalized ionization conjectures

Manuscripts read: `Uniform-excess-charge.../paper.pdf`, `Generalized-ionization-energies.../paper.pdf`, `Generalized-outer-electron-radii.../paper.pdf` (Continuum-Coulomb-hardness is QMA-hardness: no constants; checked).

**Main theorems.**
- (excess charge, Thm 1.1) For M nuclei of charges >= 1, total Z: strict binding E_n < E_{n-1} implies n <= Z + C M with C universal finite (existential; no value). (Thm 1.2) R(Psi_Z) = inf{r : exterior electron mass <= 1/2} satisfies c <= R <= C, universal c, C (existential); first ionization energy I_1(Z) similarly two-sided (Cor 1.3). The fixed fraction is **1/2** (expected half-electron).
- (ionization, Thm 1.1) I_m(Z)/m^{7/3} -> a_TF as m -> infinity and Z/m -> infinity; a_TF = (3/7) q^{-4/3} where q > 0 is the implicit charge of the unique classical solution of Delta F = 4 pi k (F-1)_+^{3/2}, k = (5 c_TF/3)^{-3/2} = 2^{3/2}/(3 pi^2), c_TF = (3/10)(3 pi^2)^{2/3} (exact, eq. 1.3).
- (radii, Thm 1.1) outer radius for expected exterior mass m: R_m ~ (81 pi^2/2)^{1/3} m^{-1/3} (exact; the one closed pi-constant in the family).

Extracted constants: 1/2; 3/7 (a_TF prefactor, PDE-coupled); k = 2^(3/2)/(3 pi^2) ~ 0.09552 — **closest of ALL 26 screened candidates to T: miss 4.22%, C/T = 0.9578, p_base = 0.0045 -> special flag per the literal criteria**; c_F = 4 pi k = 8 sqrt(2)/(3 pi) ~ 1.2005; c_TF ~ 2.8712; (81 pi^2/2)^{1/3} ~ 7.3647; universal C (existential).

Screen: k is derived within TF kinematics (Q2 forced-in-host), but Q1 fails: k is a density-of-states/kinetic coefficient with no Lambda, no G, no acceleration; the a0 identification is a free reading with no chain. Verdict NUMEROLOGY (miss <= 5% only after free choice of reading) — flagged special-but-not-FORCED, genuinely the only "near-hit" in the six families. All others: NOT APPLICABLE (miss 42%-7286%).

P1-P8 mapping: **P1 — DOES NOT APPLY** (no 4, no 1/(32 pi); the 4.2%-near TF constant k cannot be promoted without a derivation chain to a0). **P6 / galaxy floor ~0.1 (CFG370) — analogy-only at best**: the excess-charge theorem is a *ceiling* structure ("binding stops at Z + O(M)"), i.e. binding is capped by what the baryons can supply — the right shape for a supply-limited floor, but it bounds electron numbers in Coulomb systems, supplies no ~0.1 constant and no mass scale. P2, P3, P4, P5, P7, P8: DOES NOT APPLY.

## Family 267 — Positive-temperature BEC and exact quantum depletion

Manuscripts read: `Quantum-Depletion-and-Momentum-Distribution.../Quantum-Depletion-in-the-Dilute-Hard-Sphere-Bose-Gas.pdf`, `Quantum-Depletion-for-Fixed-Bounded-Repulsive-Potentials.../fixed-repulsion-quantum-depletion.pdf`, `Bose-Einstein-condensation-at-positive-temperature.../positive-temperature-hard-spheres.pdf`, `Ground-state-condensation.../paper.pdf`, `A-density-uniform-condensate-bound.../paper.pdf`.

**Main theorems.**
- (depletion, Thm 1.1 + Cor 1.2) Bogoliubov momentum measure: nu_Bog(dt) = (8 pi)^{3/2}/(2 pi)^3 g(t) dt, g(t) = (1/2)( (|t|^2+1)/sqrt(|t|^4 + 2|t|^2) - 1 ); total mass 8/(3 sqrt(pi)); depletion fraction 1 - B = 8/(3 sqrt(pi)) sqrt(rho a^3) + o(sqrt(rho a^3)) for density rho, exclusion distance a; momentum scale sqrt(8 pi rho a). Same coefficient in the fixed-repulsion paper (Thm 1.1). Thermodynamic limit at fixed density, then dilute limit; uniform over all ground states.
- (positive T, Thm 1.1) For each a > 0 there is rho*(a) > 0 such that for fixed small rho there is a fixed temperature T = T(a,rho) > 0 with liminf condensate fraction > 0. **Existential T; no exact T_c constant is given.**

Extracted constants: 8/(3 sqrt(pi)) ~ 1.5045 (matches the classic LHY 8/3 sqrt(n a^3/pi)); prefactor (8 pi)^{3/2}/(2 pi)^3 = 2 sqrt(2)/pi^{3/2} ~ 0.5072; momentum-scale coefficient sqrt(8 pi) ~ 5.0133; combo sweep (8/3)(1/sqrt(pi))^k for k = 2..6: 0.8488, 0.4790, 0.2702, 0.1524, 0.0860; resonance 1/(8 sqrt(2 pi)) = T/2 EXACTLY (C4a: |1/(8 sqrt(2 pi)) - T/2| < 1e-12).

Screen: closest combo (8/3)(1/sqrt(pi))^6 misses T by 13.8%; 1/(8 sqrt(2 pi)) is exactly T/2 (ratio 0.5, miss 50%) — a factor-2 numerology with NO derivation attaching it to a0 (the 8 in 1/(8 sqrt(2 pi)) is borrowed from the BEC momentum scale 8 pi by free choice). Q1 no for all; Q2 forced-within-Bogoliubov; Q3 p_base 0.0236-0.86. Verdict: NOT APPLICABLE / NUMEROLOGY-free null.

P1-P8 mapping: **P4 — TOOL-grade analogy (no constant)**. The condensate/depleted split is a genuine "settled/unsettled" partition mechanism: a macroscopic fraction in one mode + a small-parameter tail (sqrt(rho a^3)), i.e. an exact *two-component split set by one dimensionless parameter*. This is structurally the right object for "clusters hold their full cosmic share, ~half unsettled", but the split fraction here is density-dependent and tiny, not ~1/2 at R500, and no mapping of a^3 or rho onto cold-fluid parameters exists. **P3 (5.36) — DOES NOT APPLY** (no 5.36 anywhere; depletion 1.50, c_F 1.20, none near). **P6 — DOES NOT APPLY** ((T=0) depletion has no threshold; the positive-T theorem's T(a,rho) is existential and deliberately not a critical temperature). P1, P2, P5, P7, P8: DOES NOT APPLY.

## Family 269 — Uniform Laughlin gap and stability under bounded scalar disorder

Manuscripts read: `A-Fock-space-inequality-and-the-Laughlin-spectral-gap.../A-Fock-space-inequality....pdf`, `Uniform-Stability-of-the-Spherical-Laughlin-Gap.../uniform-stability-spherical-laughlin-gap.pdf` (verification folders present; results asserted).

**Main theorems.**
- (Fock-space, Thm 1.1) For the V1 interaction (coefficient one per pair projector) on the lowest-Landau-level Fock space of flux Q: H_Q^2 >= gamma H_Q for some fixed gamma > 1/25, all (N, Q) large; threshold Q_gamma existential. (Cor 1.2) At Laughlin filling (Q = 3(N-1), N >= N0): gap >= 1/25 (units: pair-projector energy). (Cor 6.3) charge gap Delta_N >= N/(25(N-1)) >= 1/25. **gamma* and N0 are existential; the only sharp constant is 1/25.**
- (stability, Thm 1.1) Under bounded scalar potentials phi with ||phi||_inf <= 1 and |lambda| <= lambda*: gap E1 - E0 >= Delta* > 0, unique ground state; lambda*, Delta*, N* existential.

Extracted constants: **1/25** ~ 0.04 (sharp, in the main corollary); filling fraction **1/3** (Q = 3(N-1)). Notably: 1/25 is within 0.53% of the F member 1/(8 pi) (C4b) — a numerology-level coincidence inside the null family, reported because the task demands every pi-containing/near constant be screened; it does not involve T.

Screen: 1/25 vs T: miss 59.9%, p_base 0.0877. 1/3 vs T: miss 234%. Q1 no; Q2 forced-within-theHamiltonian (the constant is genuinely proved, not chosen); Q3 fails to make it special. Verdict: NOT APPLICABLE.

P1-P8 mapping: **P6 — analogy-only (honest)**. The mechanism — an interaction that opens a spectral gap, stable as a *uniform* lower bound under bounded scalar disorder (robustness against the very perturbation class the phantom model worries about: environment potentials) — is exactly the *type* of guarantee the switch would want. But there is no interaction term of this kind in the framework (cold fluid couples only through gravity + one fluid-khronon constant, CFG381), and 1/25 does not touch T. The filling fraction 1/3 and exponent structure 1/3 resonate with family 374's sharp 1/3 stability exponent — **coincidence observation only, no derivation links them** (374 is L2/optimal-transport; 269 is quantum Hall). P1-by-analogy: 1/25 is a sharp constant with integer content (like 4, 1/32 would need to be) but it is 1/25, not 4 or 1/(32 pi); DOES NOT APPLY. P2, P3, P4 (no partition ratio), P5, P7, P8: DOES NOT APPLY.

## Family 270 — Threshold and positive-energy bound states of the BFSS matrix model

Manuscripts read: `The-unique-threshold-bound-state-of-the-SU-N-BFSS-model-September-24-2026/paper.pdf`, `Positive-eigenvalues-of-the-relative-SU-2-BFSS-Hamiltonian-October-5-2026/positive-eigenvalues-relative-su2-bfss.pdf`.

**Main theorems.** (a) (SU(N) paper, Thm 1.1) dim ker H_N = 1 for every N >= 2 (exactly one normalizable zero-energy state after CM removal; Spin(9)-invariant, even fermion grading). Supercharge normalization (1.1): Q_alpha = p... + (1/2) f^ABC x... (the 1/2 from gamma_i Clifford convention; coupling fixed at 1; color basis T_a = sigma_a/sqrt(2)). (b) (SU(2) paper, Thm 1.1) infinitely many positive eigenvalues tending to infinity with square-integrable eigenvectors.

Extracted constants: supercharge coefficient 1/2; kernel count 1. **No pi, no 4 pi, no 8 pi anywhere in the model normalization** (grep-verified: pi appears only as quotient-map symbols).

Screen: 1/2 miss 401%; 1 miss 903%. Verdict: NOT APPLICABLE.

P1-P8 mapping: **P6 / galaxy floor — DOES NOT APPLY except as the sharp-threshold archetype.** "Exactly one normalizable state at the bottom of the continuous spectrum" is a mathematically sharp *threshold property* (count, not scale), and the SU(2) companion shows the positive spectrum is unbounded — i.e. no gap scale exists in this model. There is no critical coupling (the coupling is fixed at 1 by convention), so there is no constant that could even be brought near a0. The structure cannot transfer: the framework's switch is a ratio g_N/a0, not a number of bound states. P1-P5, P7, P8: DOES NOT APPLY.

---

## Ranked screen table (all 26 screened constants, by miss)

| rank | fam | candidate | exact value | C/T | miss | p_base | Q1 | Q2 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 263 | TF density constant k = 2^(3/2)/(3 pi^2) | 0.095521 | 0.958 | 4.2% | 0.0045 | no | forced in TF | NUMEROLOGY (special flag) |
| 2 | 267 | (8/3)(1/sqrt(pi))^6 = 8/(3 pi^3) | 0.085973 | 0.862 | 13.8% | 0.024 | no | forced in Bogoliubov | NOT APPLICABLE |
| 3 | 267 | 1/(8 sqrt(2 pi)) | 0.049868 | 0.500 | 50.0% | 0.077 | no | borrowed factor-2 reading | NOT APPLICABLE |
| 4 | 267 | (8/3)(1/sqrt(pi))^5 | 0.152430 | 1.528 | 52.8% | 0.079 | no | forced in Bogoliubov | NOT APPLICABLE |
| 5 | 215 | 1/(2 pi) (O(3) flow step) | 0.159155 | 1.596 | 59.6% | 0.086 | no | forced in O(n) flow | NOT APPLICABLE |
| 6 | 269 | Laughlin gap 1/25 | 0.040000 | 0.401 | 59.9% | 0.088 | no | forced in V1 Hamiltonian | NOT APPLICABLE |
| 7 | 269 | 1/(8 pi) (F-member, near 1/25) | 0.039789 | 0.399 | 60.1% | 0.089 | no | F membership only | NOT APPLICABLE |
| 8 | 267 | (8/3)(1/sqrt(pi))^4 | 0.270189 | 2.709 | 170.9% | 0.187 | no | forced in Bogoliubov | NOT APPLICABLE |
| 9 | 269 | filling fraction 1/3 | 0.333333 | 3.342 | 234.2% | 0.227 | no | forced (Q=3(N-1)) | NOT APPLICABLE |
| 10 | 263 | 3/7 (a_TF prefactor) | 0.428571 | 4.297 | 329.7% | 0.291 | no | forced in TF | NOT APPLICABLE |
| 11 | 267 | (8/3)(1/sqrt(pi))^3 | 0.478962 | 4.802 | 380.2% | 0.314 | no | forced in Bogoliubov | NOT APPLICABLE |
| 12 | 263 | 1/2 (half-electron radius) | 0.500000 | 5.013 | 401.3% | 0.321 | no | defined, not derived | NOT APPLICABLE |
| 13 | 270 | 1/2 (supercharge coefficient) | 0.500000 | 5.013 | 401.3% | 0.321 | no | convention (Clifford) | NOT APPLICABLE |
| 14 | 267 | 2 sqrt(2)/pi^(3/2) (nu_Bog prefactor) | 0.507159 | 5.093 | 409.3% | 0.325 | no | forced in Bogoliubov | NOT APPLICABLE |
| 15 | 267 | (8/3)(1/sqrt(pi))^2 | 0.848826 | 8.511 | 751.1% | 0.453 | no | forced in Bogoliubov | NOT APPLICABLE |
| 16 | 270 | kernel count 1 | 1.000000 | 10.027 | 902.6% | 0.501 | no | theorem (count) | NOT APPLICABLE |
| 17 | 263 | c_F = 8 sqrt(2)/(3 pi) | 1.200314 | 12.036 | 1103.6% | 0.555 | no | forced in TF | NOT APPLICABLE |
| 18 | 267 | depletion 8/(3 sqrt(pi)) | 1.504507 | 15.085 | 1408.5% | 0.607 | no | forced in Bogoliubov | NOT APPLICABLE |
| 19 | 263 | c_TF = (3/10)(3 pi^2)^(2/3) | 2.871212 | 28.788 | 2778.9% | 0.763 | no | forced in TF | NOT APPLICABLE |
| 20 | 215 | 32/(pi e) (HMN ratio) | 3.747032 | 37.571 | 3657.1% | 0.816 | no | forced in O(4) S-matrix | NOT APPLICABLE |
| 21 | 267 | sqrt(8 pi) (momentum scale) | 5.013257 | 50.265 | 4926.5% | 0.861 | no | forced in Bogoliubov | NOT APPLICABLE |
| 22 | 215 | 2 pi (O(3) correlation exponent) | 6.283185 | 62.998 | 6199.9% | 0.889 | no | forced in O(n) flow | NOT APPLICABLE |
| 23 | 263 | (81 pi^2/2)^(1/3) (outer radius) | 7.364723 | 73.859 | 7285.9% | 0.901 | no | forced in TF tail | NOT APPLICABLE |
| 24 | 215 | 4 pi (mixing exponent) | 12.566371 | 125.997 | 12499.7% | 0.948 | no | forced in O(n) flow | NOT APPLICABLE |
| 25 | 215 | 32 exp(pi/4 - 1/2) (O(4) amplitude) | 42.566947 | 426.822 | 42582.2% | 0.989 | no | forced in O(4) exact asymptotics | NOT APPLICABLE |

Checks (t6_screen.py): C1a amplitude exact to 1e-12 (MUTATE-flippable), C1b depletion, C1c 1/25, C1d nu_Bog prefactor identity (8 pi)^{3/2}/(2 pi)^3 = 2 sqrt(2)/pi^{3/2}, C1e (81 pi^2/2)^{1/3}; C2 family F (889 forms, T not in F, 1%-window p = 0.0022 in record range); C3 no candidate within 1% of T; C4a 1/(8 sqrt(2 pi)) = T/2 exactly, C4b 1/25 within 1% of 1/(8 pi); C5 verdicts/special-flag logic, no FORCED; C6 closest candidate k in declared (3%, 7%) window. Normal: 15/15 PASS, rc 0. MUTATE (215 amplitude +1%): C1a FAILS as declared, 14/15, rc 1.

## P1-P8 verdict table

| piece | 215 | 221 | 263 | 267 | 269 | 270 |
|---|---|---|---|---|---|---|
| P1 (4 and 1/(32 pi)) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY (but k is a 4.2% near-miss, NUMEROLOGY) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |
| P2 (settling mechanism) | DOES NOT APPLY | TOOL (style: inf-over-hierarchies variational principle; consistent with T3 JKO) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |
| P3 (Omega_c/Omega_b = 5.36) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |
| P4 (settled/unsettled split) | DOES NOT APPLY | DOES NOT APPLY | analogy-only (binding ceiling) | analogy-only/Tool-grade (condensate vs depleted split) | DOES NOT APPLY | DOES NOT APPLY |
| P5 (MOND field equation) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |
| P6 (the switch) | analogy-only (smooth exponential crossover; canonical prescription style) | DOES NOT APPLY | analogy-only (binding threshold) | DOES NOT APPLY | analogy-only (spectral gap, disorder-stable) | DOES NOT APPLY (sharp count, no scale) |
| P7 (growth power) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |
| P8 (reframing) | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY | DOES NOT APPLY |

## Resonances worth a follow-up lane (all numerology-grade, none forced)

1. **263's TF kinetic constant k = 2^(3/2)/(3 pi^2) ~ 0.09552 vs T ~ 0.09974: miss 4.2%, p_base 0.0045** — the single genuinely-derived constant in the six families that lands within 5% of T with a low base rate. It is forced by TF kinematics (density-of-states of the Fermi packet), which has no Lambda, no G, no acceleration; promoting it would require a new derivation chain (Q1). Worth one focused lane ONLY to state the null cleanly: "TF k is 4.2% off a0's 32 pi footing with nothing attaching the two".
2. **1/(8 sqrt(2 pi)) = T/2 exactly** (an identity in F-adjacent forms, factor-2 off): the 8 and 2 pi are borrowable from the BEC momentum scale 8 pi rho a only by free choice — classic numerology, no derivation.
3. **1/25 within 0.53% of F member 1/(8 pi)** (269): inside-the-null coincidence, does not touch T.
4. **1/3 filling vs 374's 1/3 exponent**: coincidence observation only (different mathematics: Hall states vs optimal transport).

## Honest bottom line

**No family here tools any open piece P1-P8, and none FORCES anything.** All six stay at abstract-triage score 0 after the full-manuscript read. The deep read found exactly one near-numeric-event (TF k, 4.2% off T) and four structural analogies of style-grade only (221's variational principle for P2, 267's condensate/depleted two-component split for P4, 269's disorder-stable spectral gap and 215's canonical continuum prescription for P6). None supplies a constant, a derivation chain, or a mechanism that could be implemented in the working model; the cold fluid's mass remains required, kappa = 1/2 remains fitted, and nothing here is theory-closed.