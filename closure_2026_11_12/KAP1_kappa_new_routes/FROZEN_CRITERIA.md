# KAP1 FROZEN CRITERIA: one more attempt to derive kappa, on routes the record has not closed (2026-11-12)

Committed alone, before any KAP1 script or KAP1 number exists. TEST lane. Adopts nothing.
kappa = 1/2 FITTED; not theory closed.

## 0. What is to be derived, and the targets (declared before any attempt)

The law: a0 = kappa c sqrt(G rho). Footings, never pooled (record, PAPER72 Section 2; FINAL-19 inputs H0 = 67.4 km/s/Mpc,
Omega_L = 0.685):
- canonical: rho = rho_Lambda = Omega_L rho_crit,0; a0 = 9.3603e-11 m/s^2 is kappa = 1/2 on rho_Lambda.
- alt: a0 = 1.1312e-10 m/s^2 is kappa = 1/2 on rho_crit,0, i.e. kappa = 0.6041 on rho_Lambda.

Distinct targets; a route declares ONE before it is computed and may not slide to another afterwards:
- T_can: kappa = 1/2 on rho_Lambda. T_alt: kappa = 1/2 on rho_crit,0 (0.6041 on rho_Lambda).
- T_lock: kappa = sqrt(2/(3 pi)) = 0.4607 on rho_Lambda (a0 = c H_Lambda / 2 pi).
- Kernel fits (SLK1, published SPARC relation): law S 1.128e-10 (0.6025 on rho_Lambda), slow tail 8.96e-11 (0.4786).

Kernel statement: law S (mu = x/(1+x)) and the slow tail (mu = 1 - 1/sqrt(1+2x)) both have mu -> x as x -> 0, so their
deep-field (baryonic Tully-Fisher, v^4 = G M a0) coefficient is the same a0; their fitted a0 differ through the transition
shape. Every route here speaks for the DEEP-FIELD coefficient, which is common to both kernels; a route that fixes a
transition-region quantity must say which kernel it uses.

Matching window, per footing: an exact (symbolic) route matches only if it equals its declared target exactly. A numerical
route matches if |log10(kappa_route / target)| <= 0.0178 dex (half the 0.0355 dex gap between 1/2 and 0.4607). A match is
necessary, never sufficient (section 2).

## 1. Closed routes (the do-not-repeat boundary), one line each with the reason

1. dS-Unruh g_eff = sqrt(a^2 + c^2 H^2) - cH, Taylor 1/2: forces the temperature root a0 = 2 c H_Lambda, off by Z (KAPPA_ALL_DOORS F1).
2. Equipartition (1/2) k T_dS: hbar-laden, cancels classically (ALL_DOORS F1b).
3. SIS / virial / kinetic 1/2 (GF2, Q010): a ratio sigma^2/v^2, not the law's kappa (AUDIT_GF2; rules S7).
4. de Sitter surface gravity c^2/(2 R_dS): on the cH root, ratio 1/Z (ALL_DOORS F1d).
5. Ghost-freedom, unitarity, FDT: invariant under the overall normalisation (ALL_DOORS, prior routes).
6. Holography, CKN degree-of-freedom count: hbar-laden or tuned g_* (ALL_DOORS).
7. Topological eta, Hopf flux, lens/Seifert, Witten anomaly, framing, Chern-Simons level: phases mod Z or tuned (FIVE_HAIL_MARY).
8. Casimir / zeta(-1), Bousso-Polchinski flux: a horizon zero-point energy is part of rho_Lambda, double count (FIVE_HAIL_MARY).
9. Action classes P(X), nonlocal kernels, modified dispersion, spectral action, conical defects: free outside multiplier or wrong root (GATED_ACTION_BRUTEFORCE).
10. k01 zero mode: the primitive enters only through J', the vacuum constant is free (kimik3 KAPPA_VERDICT).
11. Mode / channel / photocount count, kappa = 1/n: occupation not derived (kimik3; H061; rules S7).
12. Einstein lengths: Hubble or de Sitter radius (1.447, 2.894), Poisson 4 pi G (1.772), uniform-sphere horizon J = 3/(8 pi) (KAPPA_CLOSURE section 1).
13. xi = 1, a length exactly c/sqrt(G rho): a posit, door X7 (KF1).
14. chi^2 portal kappa = 1/(2b), b = 1 is premise A; DU = 8 pi unset (KT2, KT3).
15. pi-free portals and the c-a0 census: 1/2 only in menus or posits (CFG911, CFG891).
16. KAPPA_DOORS D1-D5 and P4 (CFG897, 891, 900, 905, 904): closed.
17. K843 premise screen, 16 candidates (incl. Bekenstein bound vs S_BH -> J = 3/8 pi; gravito-electromagnetism): no survivor.
18. Switched vacuum constant (W4-24): eta = +1 needs kappa >= 5.2; CLOSURE.
19. Normalisation feedback, reciprocal sectors, curvature feedback (astra AZ18-AZ22): b, xi or the vacuum offset stay free.
20. Published dS-thermodynamic routes (Milgrom 1999/2020, Verlinde, Pikhitsa), eps_tot = 1/(32 pi), q-deformed mirror, GHY/bulk ratios (qwen T001-T009): none forced in window.
21. Clock-rate lock to the de Sitter KMS period (OUT-2): the postulate IS kappa^2 = 2/(3 pi) (audit A1: WRONG as a derivation).
22. Equality-fixed normalisation (OUT-3): K in [3/2, 3], 1/2 unreachable.
23. Scale-free boundary (normalisation continuous through the fold surface; OUT3_scale_free_boundary): fails on number, mass and epoch.
24. T*: a0 = c^2/(2 lambda), lambda = c/sqrt(G rho) is kappa = 1/2 restated; not a surface gravity, not a horizon (OUT-4).
25. Formation reading / dimensional uniqueness (FINAL6): form only; per-galaxy constructions give a0 ~ M^(1/3); its rho_Lambda selection does not hold (C3).
26. Formation-epoch matching (FINAL16): epoch menu 0.319 dex; equality was chosen.
27. Capacity of the law (FINAL-17): menu of 0.798 dex; "flat direction" reading wrong (a0 observable; A1, C3).
28. Fold charge matching M_ph(R_fold) = Q_fold (FINAL18): misses by 1.2-2.2 dex; no self-consistent root.
29. Deep-field column saturated at the vacuum stress rho_Lambda c^2 (FINAL-19): kappa = sqrt(2 pi).
30. Energy-density matching at g = a0 with a chosen convention (W_v, eps_tot; a0^2/(8 pi G) = rho c^2/(32 pi) <=> kappa = 1/2): rules S7, FINAL-19 Lean.
31. Global averages without the halo filling factor (k02): five orders short.
32. Unstiffened QUMOND / BIMOND vacuum class: excluded (Cassini, p58).
33. Komar / Tolman |rho + 3p| (0.707, MISS); Tolman 1/|1 + 3 w0| (menu on a measured w0).
34. Khronon universal horizon in Schwarzschild-de Sitter (Lambda cancels); finite-speed khronon (1/2 only at tuned n).
35. Brown-York / quasi-local field energy, 341 principles: 0 hits.
36. Vacuum Jeans, plasma, Debye scales: menu; the vacuum Jeans frequency is zero.
37. Horava-Lifshitz: Lambda free, no a0 scale.
38. Gauss-Bonnet integrals: 32 pi^2 is bookkeeping (p01).
39. Any c-free balance (rules S1, CFG893): gives a0 ~ G rho^(2/3) M^(1/3) or holds for every a0.
40. Standard-Model-constant routes: walled by standing rule unless a new forced kernel appears. Not entered here.
41. The cold share 5.41 (R541, R541A-E, OUT3_cosmic_share_fold): an integration constant; four couplings EXCLUDED, one TRADES.
42. Measurement as a route: 1/2 vs 0.4607 needs a0 to 2.8 %; floor about 9 %, best case about 5 % (KAPPA_CLOSURE section 2).

The record's register holds 847 rows; this list is by family, 42 lines.

## 2. Grading rule (frozen)

A route is DERIVED only if ALL hold:
(i) every postulate is written out and none is equivalent to the answer or to a restatement of it;
(ii) no fitted or observed number enters except G, c and the density the formula names;
(iii) it says which kernel it applies to, or fixes the kernel;
(iv) the algebra is checked independently: a sympy check, and a second derivation by a different path (here: an SI numeric
evaluation of the same chain, written separately in the same script);
(v) it yields at least one new consequence that could be tested.
Otherwise the label is one of: REDUCES TO A POSTULATE (name it), NUMEROLOGY (matches a number with no mechanism), CIRCULAR,
NOT DERIVED. A route that returns a mass- or epoch-dependent kappa is NOT DERIVED (a0 is universal to 0.041 dex). A route whose
output does not move when kappa is changed in its inputs (counterfactual, rules S2) cannot be DERIVED.

## 3. Routes to attempt (declared now; each uses an input the earlier attempts did not have)

- L1 (structural lemma, not a route): are the new inputs (COL1 collapse, FLD1 fold reach, FB1 static identities
  sigma^2 = (1/2) sqrt(G M a0) and J(g)) free of c? If so, by dimensional analysis over {G, rho, M_b, a0, t, r}, any
  condition built from them gives a0 independent of the condition or a0 = F G rho^(2/3) M_b^(1/3), never a universal kappa.
  Check: sympy nullspace of the dimension matrix.
- R1 fold-reach equality: postulate the law's MOND radius r_M = sqrt(G M_b/a0) equals the fold radius (FLD1 values, z = 0),
  and separately at the de Sitter limit R_fold = f R_max, R_max^3 = 3 M_b/(8 pi rho_Lambda). Target T_can.
- R2 fold ratio: kappa := R_fold/R_ta = 0.52 (FLD1, z = 0). Target T_can. Mechanism sought: none known before computing.
  Checks: epoch dependence (FLD1: 0.46 at z 1, 0.43-0.44 at z 2, 0.31-0.33 at z 4), dependence on a0 (FINAL18 table:
  R_fold 139.25 / 139.23 kpc canonical / alt), the uniform-sphere virial ratio R_vir/R_ta (sympy).
- R3 joint stress matching: at the fold the static halo's stress magnitude |Pi| = g^2/(8 pi G) (FB1 deep field) equals the
  vacuum's |p| = rho_Lambda c^2 (the falling clock as w = -1 cold dark energy). This is the only route here where c enters.
  Target T_can. Output: the universal g it fixes at the fold, the implied a0 per FLD1 mass, its mass slope.

Mutation twin (`KAP1_MUTATE=1`, separate outputs, exit non-zero if a control bites): R1 f -> 2f must move a0 by 1/4; R3
8 pi G -> 4 pi G must move a0 by 1/2; L1 with c added to the variable list must admit a universal group (c sqrt(G rho)).

Disclosed before freezing: numbers already read from the record (FLD1 table and fold ratios; FINAL18's R_fold per footing;
FB1 identities; SLK1 a0 fits). Hand estimates: L1 holds (all three inputs are Newtonian); R1 mass-dependent, NOT DERIVED;
R2 NUMEROLOGY (0.52 sits 0.017 dex from 1/2, inside the window, with no mechanism and epoch drift); R3 mass-dependent and
several dex off, NOT DERIVED. The lead's estimate, unverified: KAPPA NOT DERIVED.

Lane words: KAPPA DERIVED (route, kernel; awaits independent re-derivation; not closed) or KAPPA NOT DERIVED.
