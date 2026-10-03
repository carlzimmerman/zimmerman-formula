# CFG320: gate G12 (radiative stability / naturalness, and Lorentz-violation leakage into matter) for the filtered C-H/K chassis. FROZEN CRITERIA

Lane CFG320. Written and committed before the lane script exists. Verdict words are the recipe's section 6 words only:
PASS, CONDITIONAL, FAIL (= KILL for this gate), OPEN. Standing rules: kappa = 1/2 is FITTED; no knob scans and no
fitting (alpha_c, c_2, xi, the cutoff are read from committed files or fixed here); nothing here says the theory is
closed; the cold mass the CMB needs is untouched and still required. A chassis result is not a result for candidate B.

## 0. What was read before freezing, and the not-blind statement

Read: recipe section 5 (G12: "is the screening relation technically stable or fine-tuned?") and the 2026-09-26 user
decisions; `closure_map/RECIPE_GATE_AUDIT_2026-10-03.md` (lane spec, item 1); L340 (window, P1); XC1 (strong-coupling
scale, its formula `k_sc = sqrt(alpha) M_P c_s^{-1/2}` for c_s > 1, M_P = 2.435e18 GeV reduced, A6-A8 MOND-vertex and
filter numbers); CFG291 and CFG318 READMEs/criteria.

Literature, through a summarising fetch tool on arXiv abstract pages and ar5iv HTML (no downloads). Every value below
is PROVISIONAL: the summariser is not the paper.
- Collins, Perez, Sudarsky, Urrutia & Vucetich 2004, PRL 93 191301 (gr-qc/0403053). Yukawa theory, one fermion loop
  in the scalar self-energy, the fermion propagator multiplied by a Lorentz-violating regulator f(|k|/Lambda),
  f(0) = 1, f(inf) = 0. LV coefficient xi = d^2 Pi_1/d(p^0)^2 + d^2 Pi_1/d(p^1)^2 at p = 0; result (their eq. A.2)
  xi = (g^2/6 pi^2) [1 + 2 Int_0^inf dx x f'(x)^2], independent of Lambda (percent-level LV for SM couplings).
- Pospelov & Shang 2012, PRD 85 105001 (arXiv:1010.5249). The SM coupled to a sector with anisotropic scaling above
  Lambda_HL through M_P-suppressed interactions: transmission of LV into the SM is protected by Lambda_HL^2/M_P^2.
  G_N = 1/(8 pi M_pl^2) (reduced). Their eq. 59 (as summarised): (delta c^2)_photon - (delta c^2)_scalar =
  -Lambda_HL^2/(12 pi^2 M_pl^2) (1 + ...) log(Lambda_UV^2/Lambda_HL^2) - ...; quoted sentence: "Given that various
  phenomenological constraints on dimension 4 LV operators are more stringent than 10^-20, one would need to have
  Lambda_HL <~ 10^10 GeV"; and that the most stringent dimension-4 speed differences are "at the level of 10^-23"
  (their ref. [11], not read).
- Klinkhamer & Schreck 2008, PRD 78 085026 (arXiv:0809.3217), eq. 16, 2 sigma: -9e-16 < kappa_tr < 6e-20 (isotropic
  photon-sector coefficient; vacuum Cherenkov from an Auger UHECR event, photon decay from HESS TeV photons).
- Recalled, not fetched (PROVISIONAL, reading only): Hohensee et al. 2009 PRL 102 170402 (LEP/Tevatron,
  |kappa_tr| ~ 1e-11); Liberati 2013 CQG 30 133001 (review); Iengo, Russo & Serone 2009 (LV percolation in
  Lifshitz-type theories); Blas, Pujolas & Sibiryakov 2010/2011 (khronometric model).

**Not blind.** Before this file I did, in scratch (not committed):
- the Collins control mechanics: a numerical one-loop integral (Euclidean, massive fermion m = 0.01 Lambda, two
  regulators f = e^{-x^2} and f = 1/(1 + x^4)) reproduces the Collins formula to 0.3% and 0.05%; at m = 0 the
  naive differentiation under the integral misses the "1" (an IR contact term), so the control is run massive;
- head power counting: delta alpha ~ c_2 Lambda^2/(16 pi^2 M_P^2) ~ 1e-23 at Lambda = 8.5e8 GeV (natural);
  Lambda_sc(corner) ranges ~8.5e8 GeV (alpha_c min, c_2 max) to ~3.5e12 GeV (alpha_c max, c_2 min); an O(1)-LV UV
  completion entering at 3.5e12 GeV gives delta ~ 1e-14, far above 6e-20; at 8.5e8 GeV it gives ~1e-20;
- the Pospelov-Shang threshold with their eq.-59 coefficient, reduced M_P and the log is ~4e8 GeV for 1e-20, not
  1e10; their 1e10 matches M = 1.22e19 GeV without the log. Reported as found (section 4, R2).
The decision rule below was written knowing these. The in-lane graviton-propagator LV measure (B1) has NOT been
computed yet.

## 1. Chassis, window, cutoffs (inputs)

I_CHK = I_CH + (c^3/16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], beta = 0, matter minimally coupled to g only
(recipe I2), the C-H sector filtered by S = exp((xi^2/2) Delta_h) with nu_mono. Window from
`real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json` P1: alpha_c in [9.624e-14, 3.2e-9],
c_2 in [7.2888e-3, 0.0667]; scored grid W = 9 x 9 log grid, corners included. xi floors 0.031 / 0.045 pc. Footings
a0 = 9.3619e-11 (canonical, kappa = 1/2 FITTED) and 1.1279e-10 (alt) m/s^2; a0 enters only part C.

Cutoffs. Primary: the point's own strong-coupling scale Lambda_sc(alpha_c, c_2) = sqrt(alpha_c) M_P c_s^{-1/2},
c_s^2 = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) (XC1 A2/A4; perturbative unitarity requires new physics at or below
it). Stated alternatives (reading): the window minimum 8.5e8 GeV at every point; M_P (no hierarchy).

## 2. What is computed

**(A) Technical naturalness of alpha_c and c_2.**
- A0 (symbolic) the enlarged symmetry: with alpha_c = c_2 = 0 the khronon drops out of the gravity + khronon action
  (the Stueckelberg-restored terms carry overall factors alpha_c, c_2), so the LV couplings are collectively
  protected; with matter coupled to g only, pure matter loops generate only diffeomorphism-invariant functionals of g
  and cannot generate alpha or c_2.
- A1 one-loop power counting, conservative generic mixing (c_2 may generate alpha): delta alpha, delta c_2 =
  N_g max(alpha_c, c_2) Lambda^2/(16 pi^2 M_P^2) with N_g = 10 (graviton + khronon multiplicity, generous).
  Matter-LV feedback into gravity: delta alpha_m = N_m delta_matter Lambda^2/(16 pi^2 M_P^2), N_m = 100.
- Criterion (per point): |delta alpha| <= alpha_c AND |delta c_2| <= c_2 at Lambda = Lambda_sc(point).

**(B) LV leakage into matter.**
- B0 the inputs lie in the committed window (alpha_c <= 3.2e-9 PPN; 1.5 c_2 <= 0.1 BBN, L340 P1). Load-bearing.
- B1 (sympy, in-lane) the linear scalar-sector source-source amplitude W(omega, k) of the chassis at beta = 0 in
  unitary gauge (N = 1 + Phi, N_i = d_i B, gamma_ij = (1 - 2 Psi) delta_ij, E = 0), sources T^{mu nu} conserved
  scalar-type (rho, sigma free). The tensor and vector sectors are identical to GR at beta = 0 (c_T = 1; K^2 and a.a
  contain no vector/tensor pieces), so all LV of the graviton propagator is in W. Euclidean (omega -> i omega_E),
  ratio R(theta) = W_chassis/W_GR with omega_E = Q cos theta, |k| = Q sin theta. LV measure (primary, what a loop
  integral weights): eps_LV = < |R - Rbar| >_w with weight sin^2 theta (the 4D Euclidean measure) and Rbar the weighted
  mean; reading: eps_max = max |R - Rbar|. Sampled densely, including tan theta down to 1e-2/c_s.
- B2 EFT leakage (Pospelov-Shang normalisation, conservative log): delta_EFT = eps_LV Lambda^2/(12 pi^2 M_P^2)
  ln(M_P^2/Lambda^2), at Lambda = Lambda_sc(point). Photon and electron coefficients are of the same order (universal
  gravitational coupling); delta_gamma-e is taken = delta_EFT.
- B3 worst-case UV piece (Collins / Pospelov-Shang): O(1) LV entering at Lambda_HL = Lambda_sc(point):
  delta_UV = Lambda_HL^2/(12 pi^2 M_P^2) ln(M_P^2/Lambda_HL^2). Also the hierarchy needed: Lambda_HL,max solving
  delta_UV = bound.
- Bound (load-bearing, PROVISIONAL): |delta| <= 6e-20 (Klinkhamer-Schreck upper side; the induced sign is not
  computed, so the stricter side is used). Readings: 9e-16 (their lower side), 1e-23 (PS's "most stringent", source
  unread), 1e-11 (LEP/Tevatron, recalled).

**(C) The heat filter and the kernel under loops (explicit power counting, both footings, both xi floors).**
- C-a filtered MOND-vertex loops: correction to the kernel coefficients <= g_max/(16 pi^2), g_max = (2/3e)/(xi k_M)^2
  (XC1 A8; k_M recomputed with the XC1 formula at the lowest k_M).
- C-b unfiltered operators generated by graviton loops from the unfiltered C-H quadratic term 2h(DU - a)^2:
  leading (dU)^4/(16 pi^2) relative to the Newtonian term M_P^2 (dU)^2, evaluated at the Sun's field at 0.1 AU (the
  hardest Solar-System point used), and relative to the tree MOND quartic (alpha_M^2/(16 pi^2 M_P^2)).
- C-c renormalisation of the filter scale: delta xi/xi <= max[Lambda^2/(16 pi^2 M_P^2), 1/(16 pi^2 M_P^2 xi^2)].
- Criterion: C-a, C-c <= 1e-2 relative AND C-b <= 1e-10 relative to the Newtonian term (the Solar System screening
  is not undone).

## 3. Decision rule (frozen)

- **OPEN:** a load-bearing control (section 4) fails.
- **PASS:** at every W point, (A) holds, delta_EFT <= 6e-20 and delta_UV <= 6e-20 (no hierarchy assumption beyond a
  UV completion entering at Lambda_sc), and (C) holds.
- **CONDITIONAL:** (A), delta_EFT and (C) hold at every W point (or on a stated sub-window), but delta_UV exceeds the
  bound at some points. The surviving statement is named: the sub-window where delta_UV <= 6e-20, and/or the
  Pospelov-Shang hierarchy M_* = Lambda_HL <= Lambda_HL,max (with Lambda_HL <= Lambda_sc). Non-empty survivor ->
  CONDITIONAL.
- **FAIL:** (A) fails at every W point at Lambda_sc, or delta_EFT exceeds the bound at every W point, or (C) fails
  (loops generate an unfiltered term that un-screens the Solar System).
- Readings (never change the verdict): Lambda = M_P and Lambda = 8.5e8 GeV numbers; eps_max in place of eps_LV
  (reported, including whether it would change the verdict); the weaker bounds.

## 4. Controls (each can fail)

Load-bearing:
- **K1 Collins et al. 2004 reproduced at its stated inputs:** Yukawa fermion loop, LV regulator on both propagators,
  m = 0.01 Lambda; xi/g^2 within 2% of (1/6 pi^2)[1 + 2 Int x f'^2] for f = e^{-x^2} and f = 1/(1 + x^4); and xi = 0
  for f = 1 at the integrand level (the LI regulator limit: d^2/dp4^2 - d^2/dp1^2 of the angular-averaged integrand
  integrates to 0 with a 4D-symmetric cutoff).
- **K2 GR control:** at alpha_c = c_2 = 0 the derived scalar-sector W equals the covariant amplitude
  [T^{mu nu} T_{mu nu} - T^2/2]/(k^2 - omega^2) for scalar-type conserved sources up to one constant (symbolic).
- **K3 zero-coupling limit:** alpha_c, c_2 -> 0 gives W_chassis -> W_GR (symbolic), eps_LV -> 0 numerically, and
  delta_EFT, delta alpha -> 0.
- **K4 static limit:** W_chassis/W_GR at omega = 0 is 1/(1 - alpha_c/2) (G_N, FP2 D1), symbolic.
- **K5 khronon pole:** the derived W has its pole at omega^2 = c_s^2 k^2 with L340/XC1's c_s^2.
- **K6 XC1 reproduced:** min Lambda_sc over the window = 8.5e8 GeV within 3%.
- **K7 numerics:** eps_LV stable to 1% when the theta sampling is doubled.

Reading: **R1** the Pospelov-Shang threshold with eq. 59's coefficient (reduced M_P, with and without the log, and
with M = 1.22e19 GeV) against their stated "Lambda_HL <~ 1e10 GeV"; **R2** reported as found (section 0).

**MUTATE** (`CFG320_MUTATE=1`, separate `_MUTATE` outputs): c_2 = 0.5 at every alpha_c. It must fail part B; the run
must exit rc = 1. Pre-registered expectation: B0 flags it (1.5 c_2 = 0.75 > 0.1, BBN). The leakage numbers
themselves will probably NOT flag c_2 = 0.5 (larger c_2 lowers Lambda_sc); that is reported as found, not hidden.

Every script prints check() rows and "N/M checks pass"; main and MUTATE outputs go to separate files.

## 5. What this lane cannot say

- Power counting: O(1) coefficients are not computed; no loop is evaluated in the gravity sector itself (B1 is the
  tree-level propagator that a loop would integrate). The log factor and N_g, N_m are conservative choices.
- The UV completion is unknown; B3 is a worst-case model of it, not a computation.
- The cosmological-constant problem (matter loops renormalising rho_vac ~ Lambda^4) is inherited from GR unchanged
  and is not addressed; nothing here derives a0 or the a0-Lambda relation (kappa = 1/2 is FITTED).
- One gate on one chassis. It is not "the theory works".
