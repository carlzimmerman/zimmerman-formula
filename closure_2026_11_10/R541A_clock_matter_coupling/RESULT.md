# R541A RESULT: a clock-matter coupling does not fix the cold share; the induced density rides with the baryons. EXCLUDED / EXCLUDED (canonical / alt)

2026-11-10. Criteria `FROZEN_CRITERIA.md`, commit 96f38451fe, committed alone before any script or number. No amendment.
Adopts nothing. kappa = 1/2 FITTED; not theory closed. Cold dark energy is a field component, never a particle; none
was added. Footings graded separately; they differ only through R (5.410 / 5.412) and every row below is the same to
the digits shown.

## Label: EXCLUDED on both footings, for every coupling tested

The couplings -alpha rho_b f(Q) with f = Q - 1, (Q - 1)^2, ln Q, and beta (Q - 1) T, added to action (A):

1. They keep the shift symmetry: each depends on the clock only through Q, so the first integral survives with a
   free integration constant C. Nothing in the equations sets C.
2. Under "zero total charge" the coupling does induce clock charge, E = alpha f'(1) rho_b, but at linear order that
   charge is advected with the baryon velocity. It is not cold and not separate. The cold share is R_cold = 0 at every
   coupling value. The non-zero answer of a background-only reading, R = alpha/(1 - alpha), is that locked charge.
3. The only cold part is the free charge sigma = C, the same integration constant the record already fits. With C free
   the coupling fixes nothing: R = C / rho_b0 at any alpha (mutation, GA1).
4. Taking the naive background value alpha = 0.8440 anyway breaks GA3 by about 6.6e11 (MICROSCOPE) and 1.6e5 (Cassini).
   It also breaks GA4: the law's deep-regime amplitude drops to 0.156.

## Gate table (canonical / alt; identical to the digits shown)

| gate | (i-a) f = Q - 1 | (i-b) f = (Q - 1)^2 | (i-c) f = ln Q | (ii) beta (Q - 1) T |
|---|---|---|---|---|
| GA1 first integral | a^3 [M0 (Q-1) - alpha rho_b] = C, C free | (Q-1)(a^3 M0 - 2 alpha rho_b0) = C, C free | a^3 [M0 (Q-1) - alpha rho_b/Q] = C, C free | = (i-a) with alpha = beta (dust; radiation traceless) |
| GA1 R_cold under Z_can (C = 0) | 0 at all a in [1e-9, 1] | 0 (Q = 1 exactly) | 0 at all a | 0 |
| GA1 R_cold under Z_K (clock-own charge 0) | -alpha (negative) | 0 | -alpha | -beta |
| GA1 is Z forced? | no | no | no | no |
| GA2 induced density moves with | baryons (locked, exact at linear order) | nothing induced | baryons | baryons |
| GA2 cold share vs 5.41 | 0: FAIL (baryons-only, F1A +172,915.6 / +166,674.4 chi2) | 0: FAIL | 0: FAIL | 0: FAIL |
| GA3 eta(Ti,Pt) at alpha 0.8440 | 4.65e-3, x6.6e11 the 7.0e-15 line: FAIL | no alpha gives R; alpha <= 4.1e-4 from MICROSCOPE | as (i-a): FAIL | 0 (classical, couples to total mass) |
| GA3 Cassini gamma - 1 | 10.9, x1.6e5 the 6.7e-5 line: FAIL | - | FAIL | 10.8, x1.6e5: FAIL |
| GA4 a0_eff / a0 | 0.156 (line 0.90-1.10): FAIL | - | FAIL | FAIL |
| GA5 | PASS (densities +0.156 / +0.844 rho_b; inertia positive; constraint preserved to 7e-16) | FAIL at alpha 0.844: clock kinetic coefficient M0 - 2 alpha rho_b < 0 (ghost) before a = 5.4e-5 / 2.2e-6 / 4.3e-8 at mu_K 198 / 2.51e4 / 8.9e6 per Mpc | PASS | PASS |
| row label | EXCLUDED (GA2, GA3, GA4) | EXCLUDED (GA1/GA2: nothing induced) | EXCLUDED | EXCLUDED (GA2, GA3, GA4) |

## The derivation in plain steps

- **GA1** (`ga1_background.py`, `.out`): sympy minisuperspace L = L_grav + N a^3 G(Q, a), with
  G = M0 (Q - 1)^2/2 - rho_b (1 + alpha f(Q)) and M0 = mu_K^2/K.
  - The clock is cyclic in every case.
  - The first integral is a^3 G'(Q) = C and the density is rho_tot = Q G' - G (checked against dL/dN, residual 0).
  - Under C = 0, rho_tot - rho_b is 3e-5 rho_b at a = 1e-3 and 3e-14 rho_b today (mu_K 198). It grows like a^-6,
    stiff, never dust. The split is the clock's own +alpha rho_b plus an interaction term -alpha rho_b.
- **GA2** (`ga2_perturbations.py`, `.out`): sympy expansion to second order in Newtonian gauge, followed by an
  integration by parts with baryon continuity:
  - L_c = alpha f'(1) m n [(v_b - v_K)^2/2 - v_b^2/2 + Phi] + total derivative, residual 0.
  - f''(1) first enters at fourth order.
  - The clock charge obeys d_t rho_K + div[rho_K v_K + E (v_b - v_K)] = 0. Hence sigma = rho_K - E moves with the
    clock frame, and E moves with the baryons.
  - The baryons' Euler equation is unchanged: inertia and weight are both m n.
  - A Fourier-mode toy (tight coupling plus gravity) confirms it. Under Z_can the free part stays 0.0000. Baryon
    evolution is identical to the uncoupled case (delta_b at the end: 0.8660 in both runs).
  - The cold share is therefore 0, which is the baryons-only case F1A rejects. If the co-moving density instead had to
    carry the whole 6.41 rho_b, the baryon load would be 541 % off against a ~1 % determination.
- **GA3 / GA4** (`ga3_ga4_static.py`, `.out`): standing clock, Q = 1/N. A body has inertia M and gravitational mass
  (1 - alpha b) M, with b = B m_N / M.
  - b from atomic masses: Ti 1.009113, Pt 1.008294, so Delta b = 8.19e-4. MICROSCOPE alloys TA6V / PtRh10:
    Delta b = 7.26e-4.
  - Coupling (ii) couples to -T, which integrates to M (von Laue), so it is composition-blind. The universal mismatch
    between light and orbits still gives gamma_eff - 1 = 2 beta/(1 - beta).
  - Law: v^4 = (1 - alpha) G_lab M a0 once a0 is read from G rho_DE = 3 H0^2 Omega_L / 8 pi, which is free of G.
- **GA5** (`ga5_signs.py`, `.out`): signs of the densities and of the inertia matrix.

## Checks run

- KA, passed:
  - alpha = 0 reproduces the record's first integral and rho_K = C/a^3 + K C^2/(2 mu_K^2 a^6) (True).
  - Acoustic frequency: 95.27 numeric against 95.28 textbook.
  - Fe-56 binding energy 8.7903 MeV; hydrogen b = 0.999456.
  - alpha = 0 gives eta = 0, gamma = 1 and a0_eff = a0.
  - Constraint preservation at alpha = 0.
- MU, every gate moved:
  - Free charge C = 5.41 rho_b0 returns R = 5.41 at any alpha.
  - sigma = R rho_b on top of Z_can returns R_cold = 5.410 and a growing cold mode.
  - Pt swapped for Be gives eta 1.37e-2.
  - alpha > 1 flips the baryon density sign (GA5 FAIL).
- Mutation deviation, disclosed: the criteria said "halve alpha: eta halves". In fact eta goes from 4.65e-3 to
  6.0e-4. It follows alpha Delta b / (1 - alpha b), which is linear only at small alpha.

## What was not checked, and weaknesses

- GA2 is Newtonian and sub-horizon, on a static background (Jeans swindle). No expansion, no Boltzmann code and no
  CAMB run. The locking identity is exact at linear order; higher orders in v_rel were not checked.
- GA3 assumes the clock stands still around the Earth and the Sun (rule 4). If the clock instead falls locally, the
  entrainment term gives preferred-frame effects of order alpha. Those were not computed.
- The coupling's effect on the polarization (P, W, gamma_L) sector of the static state was not derived. GA4 assumes
  the law sector is sourced by the active density (1 - alpha) rho_b.
- MICROSCOPE (Touboul et al. 2022, PRL 129, 121102) and Cassini (Bertotti et al. 2003, Nature 425, 374) were quoted
  from memory: PROVISIONAL. The atomic masses were typed in from memory, but the Fe-56 and hydrogen known-answer
  checks pass. The 1 % peaks width is a standard-model fit: indicative only.
- Coupling (ii) was taken classically. Composition dependence through the trace anomaly or other quantum corrections
  was ignored. It is not needed for the label, which rests on Cassini, GA2 and GA4.
- No full covariant stress tensor of the coupled theory was derived: minisuperspace plus Newtonian limit only.
- Under Z_can at small mu_K the clock's stiff a^-6 piece dominates the early universe. This is the record's known
  nucleosynthesis condition (mu_K >= 8.9e6 per Mpc) and was not graded here.
- "Zero total charge" is not even convention-free. Adding the total derivative eps J_B . d tau (lane R541D's term)
  shifts the canonical charge by eps n_B, which is why Z_can and Z_K differ.

## Files

`FROZEN_CRITERIA.md`, `ga1_background.py/.out`, `ga2_perturbations.py/.out`, `ga3_ga4_static.py/.out`, `ga5_signs.py/.out`.
