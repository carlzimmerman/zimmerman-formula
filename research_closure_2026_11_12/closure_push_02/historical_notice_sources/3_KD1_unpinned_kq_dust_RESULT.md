# KD1: v3s's K(Q) dust with the amplitude unpinned. NO SETTING PASSES ALL GATES

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. This is a TEST lane that reopens a cold-dark-energy sector
(owner 11-04 rule). It is never called dark matter, and there is no particle. Criteria: FROZEN_CRITERIA.md
(6c7f83ed02), committed alone before any script. Script: kd1.py (one thread, 34 s). Outputs: kd1.json / kd1.out,
and the MUTATE twin's kd1_MUTATE.json / kd1_MUTATE.out. QX3 iter2, GB1 and QX15 are used read-only; none of their
files is edited.

**Label: FAIL. The one fixed setting passes the background and CMB lensing but fails G1 to G7. On both footings,
G1 SPARC, G2 X-COP, G3 groups, G4 ellipticals, G5 Coma UDGs, G6 dSph classes and G7 KiDS block it. At any value of
mu_K that galaxies allow, the background (B1a, B1b) and CMB lensing (G9a) block it instead.**

## Physics settled first (criteria section 1)

- **The static term does not depend on the amplitude.** The static weak-field dust is delta rho_K = -mu_K^2 psi/(4 pi G).
  I0 only sets the cosmic mean. So freeing I0 cannot move the galaxy or cluster side except through the captured
  mass.
- **How it clusters.** The sector is an n = 1 polytrope with a fixed physical Jeans wavenumber mu_K (QX3, Lean). It is
  an irrotational khronon-gradient fluid, so it has no rotational support and no coupling that ejects it. It falls
  into every well above the Jeans mass and settles in a central core of radius pi/mu_K or less. Every host retains
  it. At the fixed setting, the Jeans mass is 1e-6 Msun and the core is 0.35 pc. All 5,633 graded points sit in
  systems that captured.
- **The FRW solution is stiff before a^3 = w0** (Lean frw_dust: rho ∝ a^-3 (1 + w0/a^3), with w0 = I0/(4 mu_K^2)).
  This is new in KD1: BBN alone needs mu_K >= 8.9e6 Mpc^-1. That bound is 350 times stricter than CMB lensing's
  Jeans line.

## The fixed setting, and how it was fixed

| | canonical | alt |
|---|---|---|
| omega_d (the amplitude), fixed once from QX15's primary TT/TE/EE fit on the footing background (h 0.674) | 0.120940 | 0.120929 |
| I0 = 3 H0^2 Omega_d / c^2 | 4.037e-8 Mpc^-2 | 4.037e-8 Mpc^-2 |
| mu_B (B1a cold at z 3400: >= 198; B1b BBN: >= 8.89e6) | 8.890e6 Mpc^-1 | 8.889e6 Mpc^-1 |
| mu_J (CMB-lensing Jeans line, Delta chi^2 <= 4) | 2.51e4 Mpc^-1 | 2.51e4 Mpc^-1 |
| **mu_K* = max(mu_B, mu_J)**, the point most favourable to every static gate | **8.890e6 Mpc^-1** | **8.889e6 Mpc^-1** |
| captured fraction f_cap omega_d/omega_b | 4.111 | 4.112 |

## Gate x footing (at the fixed setting)

| Gate | canonical | alt |
|---|---|---|
| B1a cold at z 3400 (w <= 0.01) | PASS (w 5.0e-12) | PASS (5.0e-12) |
| B1b BBN stiff phase (<= 0.067 of radiation) | PASS (at the line by construction) | PASS |
| G9a CMB-lensing shape (chi^2 <= 18.48; Jeans Delta chi^2 <= 4) | PASS: chi^2 8.56, Delta chi^2 0.00 | PASS: 8.56, 0.00 |
| G9b growth (label from G9a's window, as QX3 ruled; no separate dataset) | PASS | PASS |
| G1 SPARC | **FAIL**: Z -0.719, rms 0.817 (line 0.146) | **FAIL**: Z -0.735, rms 0.828 (line 0.143) |
| G2 X-COP | **FAIL**: mean -0.703, rms 0.803 (plain law was +0.468) | **FAIL**: -0.714, 0.810 |
| G3 groups | **FAIL**: 1/20 and 0/20 (medians -0.19 / -0.38) | **FAIL**: 1/20 and 0/20 |
| G4 ellipticals | **FAIL**: -0.465 | **FAIL**: -0.475 |
| G5 Coma UDGs | **FAIL**: +0.601 (+2.29 sigma_U) | **FAIL**: +0.561 (+2.14 sigma_U) |
| G6 dSph classes (median minus the SPARC anchor) | **FAIL**: bright M31 +0.42, MW classical +0.43, LG field +0.25; no CI contains 0 | **FAIL**: +0.40, +0.41, +0.23 |
| G7 KiDS split | **FAIL**: R +0.158 (+2.46 sigma). The same b in both colours moves nothing | **FAIL**: same |
| G8 Solar System | PASS: 0.211 (no ambient dust at the Sun) | PASS: 0.190 |

- The static rows keep the same status at 10 x mu* and at 100 x mu* (monotonicity, P5).
- Cassini was not graded. The linear near-field term (mu* r)^2/2 at the Cassini radius would be 8.5e-8. It is zero
  in model P, which has no ambient dust at the Sun.

**Converse reading, at mu_K values galaxies allow (both footings, numbers canonical):**

| mu_K (Mpc^-1) | w(z 3400) | BBN stiff/radiation | G9a Delta chi^2 |
|---|---|---|---|
| 0.1 (S4 isolated-galaxy guard) | 1.0, FAIL | 5.3e14, FAIL | 312, FAIL |
| 79.43 (QX3 capture bound) | 0.059, FAIL | 8.4e8, FAIL | 857, FAIL |

**Where it blocks, and by how much.** The CMB and BBN need mu_K >= 8.9e6 Mpc^-1. Galaxies need mu_K <= 0.1 (S4) to
79 (QX3). That is a gap of at least 1.1e5 in mu_K. QX3 put the gap at 500; KD1 widens it through the BBN stiff
phase.

## Diagnostic (reported, not graded): the step decides it whatever the amplitude

Suppose a uniform extra baryon-mass fraction f is added at every point (b = 1 + f). SPARC allows f <= 0.33
(canonical) or 0.19 (alt). The hot classes need:

| | X-COP | groups f*0 / f*1 | ellipticals | bright M31 | MW classical | Coma UDGs |
|---|---|---|---|---|---|---|
| canonical | 4.18 | 3.46 / 1.23 | 0.86 | 1.68 | 1.82 | 86 |
| alt | 3.78 | 2.86 / 0.93 | 0.77 | 1.27 | 1.41 | 78 |

- Cosmic capture gives 4.11 to every class alike. That is close to what X-COP needs, and 13 to 21 times what SPARC
  allows.
- The step needs a sector that discs exclude and hot systems keep. A universally captured, retained, irrotational
  sector has no such switch, so no value of I0 serves both, even with the CMB set aside.
- The fixed setting also over-shoots X-COP (-0.70). The polytrope core puts all the dust at the centre, not on the
  measured radii.
- The UDGs would need f ~ 80, which is beyond any cosmic share.

## Known answers and MUTATE (all PASS; nothing was graded until they did)

- KA1: GB1's L0 class means, max |d| 4.3e-7 / 4.5e-7 against a line of 1e-6. UDG |d| <= 2.2e-16.
- KA2: KD with I0 = 0 equals gb1.json's L0 numbers on G1-G8, |d| = 0, both footings.
- KA3: QX3 iter2, corner (0.0215, 65, 0.95):
  - chi^2 8.570836 against 8.570881;
  - Delta chi^2 above mu = 1e4 matches exactly;
  - mu_min = 25118.86, which matches.
- KA4: QX3 g3 mu_max = 79.43, which matches.
- MUTATE (I0 -> 0): G9a chi^2 888.5 / 888.5 against a line of 18.48 (1483 with A_s fixed), so it FAILS on both
  footings. Its static rows equal L0. **The test bites.**

## Assumptions and limits

- Capture uses model P (QX3 G3): f_cap 0.76 (X22), and the core is not compressed by baryons, which is generous.
  - If the fluid multi-streamed after shell crossing, the dust would not sit in a core. That is beyond the fluid
    description, and AC14's fold is NO VERDICT. Its profile would be extended instead.
  - That cannot rescue the result. The uniform-f diagnostic shows SPARC tolerates at most 0.33, against a cosmic
    share of 4.1.
- The B1b line (Delta N_eff <= 0.5) is declared in KD1, and mu_B scales as line^-1/2. Even mu_J alone (2.5e4) sits
  316 to 2.5e5 times above the galaxy bounds.
- The CMB lensing shape is linear CLASS at L <= 400 with A_s refit, as in QX3. The A_s fixed at QX15's primary value
  also passes as a reported reading (chi^2 9.73 / 9.71). No LCDM parameter values were used: the background is
  QX15's footing fit.
- KiDS assumes all lens baryons are enclosed at R >= 0.1 Mpc (declared, P4).
- Growth (G9b) has no separate dataset here.
- Post-freeze disclosure: the first full run printed the core radius scaled by 1e9 instead of 1e6 (353 pc instead
  of 0.353 pc). It was a print line only. It was fixed, the run repeated, and every graded number is unchanged.

Kappa = 1/2 FITTED; not theory closed.
