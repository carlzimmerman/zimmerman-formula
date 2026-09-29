# J -- emergent electromagnetism from a condensate (pre-registration)

Written 2026-09-28 BEFORE any of `j1_*.py` ... `j4_*.py` was run.
Target: alpha^-1 = 137.035999177, Thomson limit (q -> 0). Anything at another scale is stated with its scale.

## Honest disclosure of what was looked at before this file was written
* Read (full-text passages, via saved PDFs): Volovik, arXiv:0801.0724 (Table 1 and text: running couplings alpha_n^-1 ~ ln(E_P/E_IR), the IR cut-off may be
  the inverse Hubble radius; masses of fermions zero at the Fermi point; the Fermi-point count of 16 Weyl fermions per generation); Pace, Morampudi, Moessner,
  Laumann, arXiv:2009.04499 (emergent fine-structure constant of quantum spin ice, tunable 0..0.2 in their units alpha = e^2/(hbar c), microscopic a and g cancel).
* Abstract only: Levin & Wen cond-mat/0407140 (string-net photons), Bjorken hep-th/0111196 (photon as Goldstone boson of a fermion theory), Volovik gr-qc/0005091.
* Recalled from memory (not read here): the Fermi-point species count N_F and the 3He-A gap/Fermi-energy ratio; compact-U(1) Wilson-action critical coupling beta_c ~ 1.011
  (Arnold et al.); the two-loop QED beta function dalpha/dlnmu = (2 alpha^2/3pi)(1 + 3 alpha/(4 pi)); Bjorken/Eguchi compositeness condition 1/e^2(Lambda) = 0.
* Before writing this file I noticed BY HAND that ln(M_Planck^2/(hbar H)^2) is about 280 (so a Hubble-IR / Planck-UV log with N_eff of about 4.6 is in the neighbourhood of 137).
  The Hubble-IR table (J4c) is therefore a POST-OBSERVATION trial family, not a blind one. It is scored anyway, with its trial count, and it is declared now that it
  cannot count as a derivation whatever it returns (wrong scale for the Thomson limit; see J4c).
* Lanes A-G and AH1-AH6 were read at the level of their pre-registrations/summaries; nothing here redoes them. Lane C (P3) already gives the one-loop emergence formula
  1/alpha = (2/3pi) sum N_c q^2 ln(Lambda/m); J extends it to the condensed-matter constructions and to the FL1 order parameter.

## Question
In standard emergent-photon constructions, what microscopic quantities set the dimensionless coupling, and can the programme's FL1 order parameter
(one complex Schroedinger-Poisson field, kernel-invisible, neutral, mass m declared >= 2e-19 eV, amount free) supply the species count and cutoff so alpha is FORCED?

## Hypotheses and criteria (fixed now)
H1 (structure). For a photon that is purely induced (no bare Maxwell term) by charged Weyl/Dirac species with common velocity v and cutoff Lambda,
   (i) the induced action has eps = Z/v, 1/mu = Z v, so c_photon = v; (ii) alpha_eff = 3 pi /(N_eff ln(Lambda^2/mu^2)) with the microscopic charge e AND v cancelling exactly;
   (iii) the ONLY inputs are N_eff = sum N_c q^2 (charges in units of the holonomy quantum) and the scale ratio Lambda/mu.
   PASS iff sympy verifies (i)-(iii) as identities. MUTATE (argv `MUTATE`, exit 1): eps = Z v (wrong scaling) must break c_photon = v and the e-cancellation.
H2 (numerical check with a hard momentum cutoff, the condensed-matter regulator). Direct 3D interband polarization of a Dirac fermion with the projector-overlap formula
   (overlap formula itself checked against explicit 4x4 matrices): (a) the coefficient of ln Lambda^2 in eps equals 1/(12 pi^2) per unit charge^2 to 1e-3;
   (b) the finite constant differs between three declared schemes (hard cutoff on p; hard cutoff on |p+-q/2| symmetric; Pauli-Villars analytic), so the scheme-dependent
   shift of 1/alpha is (N_eff/3 pi) * Delta c. PASS for (a) iff the fit is within 1e-3; (b) is a REPORT of whether Delta c (N_eff/3pi) exceeds 1e-3*137.036 = 0.137
   for N_eff in {1, 8/3, 8}. Also report the precision budget for any Lambda/mu-law prediction of 1/alpha to 1e-3: needed dlnLambda, and the two-loop fractional shift 3alpha/(4pi).
   MUTATE (argv `MUTATE`, exit 1): overlap sign flipped (1 + ... instead of 1 - ...) must fail (a).
H3 (does any construction select the ratio?). Constructions: (C-a) Fermi point/3He-A (ratio = E_UV/E_IR of the linear spectrum), (C-b) NJL/Bjorken compositeness with a 4-fermion gap equation,
   (C-c) BCS-type gap (Lambda/Delta = exp(1/N0V)), (C-d) compact-U(1) lattice (string-net/spin-ice type): alpha tunable 0..alpha_c.
   Test (numerical, for C-b, and analytic for C-c): the map from the microscopic dimensionless coupling (G Lambda^2 or N0 V) to 1/alpha_IR is continuous and surjective onto (0, infinity) --
   for a declared list of 10 target values of 1/alpha spanning 1..1e3 (including 137.036) a microscopic coupling exists in every case. Criterion "construction constrains alpha":
   some target is unreachable without an extra input. Declared expectation: NONE unreachable (alpha trades for the microscopic coupling). C-d is reported from the read paper (no computation).
   MUTATE (argv `MUTATE`, exit 1): NJL gap equation with a wrong sign inside the logarithm must fail the solve-and-substitute check.
H4 (can FL1 supply the count and cutoff?). Declared sub-questions:
   J4a species/charge: FL1's field content has N_charged = 0 (neutral, couples only to u). If instead its quanta carried charge fraction f of e, the condensate would Higgs the photon:
      m_gamma^2 = f^2 e^2 rho_d/m^2 (Heaviside-Lorentz, hbar=c=1). Criterion: compute m_gamma for f=1 at the cosmic-mean dark density and m = 2e-19 eV; compare to the photon-mass
      bound 1e-18 eV (recalled PDG-level bound, order of magnitude); report the maximum f allowed. If f=1 is excluded, a charged FL1 cannot be the photon's source.
   J4b cutoff window: FL1's energy scales are declared m in [2e-19, ~3] eV (F6 classicality edge), healing/Jeans scales below. Criterion: is any FL1 scale >= m_e (the Thomson-limit IR scale)?
      If not, FL1 cannot be the UV cutoff of the QED log. Also the decay constant f_theta^2 = rho/m^2 of the superfluid Goldstone (dual to a 2-form in 3+1): dimensionful, no alpha.
   J4c Hubble-IR table (post-observation family): alpha^-1 = (N_eff/3pi) ln(E_UV^2/E_IR^2) with E_UV in {M_Planck, M_reduced}, E_IR in {hbar H0, hbar H_Lambda = hbar H0 sqrt(Omega_L),
      rho_Lambda^(1/4)} and N_eff in {1, 8/3, 8, 16}: 2 x 3 x 4 = 24 scored trials. HIT iff within 1e-3 relative of 137.035999177. Also report (not scored) N_eff required per pair.
      Expected chance hits: 24 x 2e-3 / ln(1e3) = 6.9e-3. Whatever it returns, it is NOT a derivation: (a) it is post-observation, (b) at IR = Hubble it is alpha at the Hubble scale for
      massless charged species, not the Thomson limit, (c) N_eff is chosen from a list, (d) M_Pl vs M_red is an O(1) convention.
   J4d m-dependence: every dimensionless FL1 number (occupation per de Broglie cell N ~ m^-4, GDM q, f_theta/m) depends on the free m and amount. Criterion: verify the exponent
      symbolically; if it depends on free m it cannot be forced (no hit-test).
   MUTATE (argv `MUTATE`, exit 1): set the dark density to zero in J4a so the exclusion check must fail.
Total scored hit-tests: 24 (J4c) + 1 (J2 coefficient is a check, not a hit) = 24; chance hits expected 6.9e-3. H3's 10 targets are a surjectivity test, not hits.

## Declared expected outcome
No forced principle. The induced-photon construction has a genuine forced BOUNDARY CONDITION (1/e^2 -> 0 at the compositeness cutoff; microscopic e and v drop out) but the low-energy alpha is
(N_eff/3pi) ln(Lambda^2/mu^2) + scheme constant: N_eff and Lambda/mu are microscopic inputs; every construction trades alpha for a microscopic coupling; FL1 is neutral (charge would Higgs the photon by ~30 orders),
sits entirely below m_e, and all its dimensionless numbers carry the free m. Precision 1e-3 is out of reach of any one-loop cutoff law because of scheme constants alone.

## Not tested
Non-perturbative emergence (string-net ground-state numerics; lattice QED beyond the read paper's numbers), emergent charged fermions from FL1 (would need new field content), any derivation of
fermion masses (walled), gravity-induced (Sakharov) relations between Lambda and G (parametric; C-lane P2/P3 territory), kappa (stays 1/2 FITTED).

## Amendments
(none yet)

## Results (appended after the runs; no criterion was changed; real runs exit 0, every MUTATE run exits 1)
Scripts/outputs: j1_induced_photon_structure, j2_hard_cutoff_polarization, j3_constructions_trading, j4_fl1_supply (each `.py`, `.out`, `_MUTATE.out`).
* H1 PASS (11 checks). Induced photon: eps = Z/v, 1/mu = Z v, c_photon = v; alpha_eff = 3 pi/(N_eff L) with e and v cancelling identically; with a bare term 1/alpha = 1/alpha_0 + N_eff L/(3 pi).
  Required log for 1/alpha = 137.036: ln(Lambda^2/mu^2) = 1291.5 (N_eff=1), 484.3 (8/3), 161.4 (8), i.e. Lambda/mu = 10^280, 10^105, 10^35.
* H2: (a) PASS, hard-cutoff numerical coefficient of ln Lambda^2 is 0.99999989 (target 1) from an independent 3D interband integral (overlap formula matches explicit 4x4 matrices to 2e-16).
  (b) c_hard = -0.2804 relative to Pauli-Villars; shift of 1/alpha = 0.030 / 0.079 / 0.238 for N_eff = 1 / 8/3 / 8 (budget 0.137: EXCEEDS only for N_eff=8); a factor-2 in the meaning of Lambda
  shifts 1/alpha by 0.147 / 0.392 / 1.177 (EXCEEDS for all). (c) two-loop fractional shift 3 alpha/(4 pi) = 1.74e-3 moves 1/alpha by 0.239 > 0.137: no one-loop cutoff law can reach 1e-3.
* H3: surjectivity 20/20 for NJL and 20/20 for BCS (10 targets x N_eff in {1,8}); criterion 'constructions constrain alpha' NOT met. 137.036 needs NJL coupling within 1.2e-68 of critical (N_eff=8; 1.6e-558 for N_eff=1)
  or BCS lambda = 0.0123 (N_eff=8; alpha = 3 pi lambda/(2 N_eff)). Lattice compact U(1): 1/137.036 is 9.3% of the recalled alpha_c(HL) = 0.0787: an interior point (inequality only).
* H4: J4a PASS: a charged FL1 gives m_gamma = 4.7e12 eV at m = 2e-19 eV, 4.7e30 above the 1e-18 eV bound; f_max = 2e-31 (so N_charged = 0). J4b PASS: largest FL1 scale (m ~ 3 eV) is 5.9e-6 m_e: no cutoff
  above m_e. J4c: 24 trials, 0 hits, chance expectation 0.0069; required N_eff = 4.60 (M_Pl, hbar H0), 4.60 (hbar H_Lambda), 9.12 (rho_L^1/4), 4.65-9.34 for M_red: non-integers, and wrong scale anyway.
  J4d PASS: N_cell ~ m^-4, f_theta ~ m^-1 (free m).
* Total scored hit-tests 24, hits 0, expected chance hits 6.9e-3. (The pre-registration line 'Total ... 24 + 1' counted J2's coefficient, which is a check, not a hit-test; the scored count is 24.)
