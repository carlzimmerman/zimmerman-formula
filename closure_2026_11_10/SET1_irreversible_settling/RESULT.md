# SET1 RESULT: irreversible settling of cold dark energy toward the law's halo (2026-11-10)

**Label, canonical / alt: STRUCTURE FAILS AT A1 / STRUCTURE FAILS AT A1.** The stop rule applies, so A2 to A5 and Part B
were not run. There is no disc reading (A2 not run).

- **Point mass: holds, exactly.** For a point mass the target pressure P = J(g) plus Poisson returns the law exactly,
  and the deep field is the isothermal halo sigma^2 = (1/2) sqrt(G M_b a0). The state is unique once the centre is
  regular (no cold point mass).
- **Extended spherical baryons: fails.** Put the law's own state into the Jeans equation with P = J(g). The force is
  off by exactly **a0 rho_b** (sympy, residual 0). So J(g) holds the law's halo only where there are no baryons.
- **Cored baryons (Plummer).** The static P = J(g) state needs negative cold density in the core, at every mass, with
  **rho_c(0) = -rho_b(0)/4 exactly**. The negative region reaches 0.57 to 0.63 R_50 and holds -0.9 to -2.7 % of M_b. So
  no f >= 0 static state exists.
- **Cusped baryons (Hernquist).** rho_c stays positive, but the field is the law of a smaller mass,
  M_eff = Int mu dM_b. That puts it 0.084 to 0.20 dex low far out (canonical; alt 0.092 to 0.22).
- **Against the SPARC line** (rms in g over 0.3 to 6 R_50; line 0.0660 / 0.0658):
  - Plummer fails at all four masses: 0.099 to 0.327 (canonical), 0.114 to 0.357 (alt).
  - Hernquist fails at log M_b 9.4: 0.154 / 0.169.
  - Hernquist at 10.45: 0.0660 against the 0.0660 line canonical (flagged by the script at full precision), 0.074 alt.
    Neither row is needed for the label.

**In plain words.** The candidate gives its settled medium an isotropic velocity spread that depends only on the local
field. The law's own stress (M5's, FB1's) is anisotropic, and its anisotropic part, Pi_rr - Pi_tt = -a0 g_N/(4 pi G)
(exact), has zero divergence only outside the baryons. An isotropic local spread therefore holds the law around a point
and nowhere inside a galaxy's own mass. That is the part of the halo inside SPARC's radii.

The repair that does hold a sphere (reading D, reported only) adds a radial column of baryons:
P_eq = J(g) + a0 Int_r^inf rho_b dr'. It is positive, but it is not local, and at R_50 the non-local piece is 0.34 to
0.68 of J. A disc has no such column and no isotropic version at all. That is A2's problem, reached earlier than
expected.

TEST lane, quarantined. Adopts nothing, relabels nothing, not registered. Footings never pooled. Cold dark energy is a
gravitating field component. f(x, v) describes the field's state; it adds no particle species. kappa = 1/2 FITTED; not
theory closed.

## What is put in by hand (from the criteria)

The law's function enters through the target f_law (through J), and tau's rule is a postulate. Even a pass would have
been an existence statement about an irreversible, charge-conserving joint, not a derivation of the law. Here the
existence fails first.

## A1a, exact (`set1_a1_sym.py` -> `set1_a1_sym.out` / `.json`; ALL PASS, exit 0)

| check | result |
|---|---|
| (i) Jeans with isotropic P = J(g) plus Poisson is equivalent to F(g) = 4 pi G rho_b, F = g'(2+u)/(1+u) + 2g/r | residual 0 |
| (i) the law is mu(u) F(g) = 4 pi G rho_b | residual 0 |
| (i) J'(g) = g / (4 pi G (1 + u)) | residual 0 |
| (ii) law state in Jeans with P = J: dJ/dr + rho_ph g = **a0 rho_b** | residual 0 |
| (ii) anisotropy of the field stress: g^2/(K(1+u)) = a0 g_N/K | residual 0 |
| (iii) point mass: dJ/dr + rho_ph g = 0 on the exact law | residual 0 |
| (iii) M_ph = M_b (sqrt(1 + 4x^2) - 1)/2 | residual 0 |
| (iii) deep field: sigma^2 -> (1/2) sqrt(G M_b a0), and rho_ph -> sigma^2/(2 pi G r^2); Newtonian side: sigma^2 -> G M_b/(2r) | exact limits 1/2, 1, 1 |
| (iv) uniqueness: off the baryons F = 0 is d(r^2 mu g)/dr = 0, a family r^2 mu g = C. At the centre r^2 g -> C, so C/G = M_b + m_c | regular centre: C = G M_b, unique. Otherwise each member carries a cold point mass m_c and its far field is the law for the wrong mass, M_b + m_c |
| (v) any cored profile: the centre is deep, g = c r with c = pi G rho_b(0), so rho_c(0) = -rho_b(0)/4 | exact (any mass) |
| (vi) deep-limit closed forms (KA3): Plummer g = (G M / 2 r b)[1 - (1 + r^2/b^2)^(-3/2)]; Hernquist g = G M (r + 2a)/(2a (r + a)^2), whose g' < 0 everywhere | residual 0 |

## A1b, numbers (`set1_a1_num.py` -> `set1_a1_num.out` / `.json`)

R_50 comes from SCS2's relation. The window is 0.3 to 6 R_50 and the residual is dex in g. The asymptotic offset is
0.5 log10(M_eff/M_b). "Negative region" is where rho_c < 0, in units of R_50.

| footing | log M_b | profile | rms | max | far-field offset | negative region | its mass / M_b | rho_c(0)/rho_b(0) | D: non-local / J at R_50 |
|---|---|---|---|---|---|---|---|---|---|
| canonical | 9.4 | Plummer | **0.327** | 0.404 | -0.292 | 0 to 0.62 | -0.025 | -0.25 | 0.67 |
| canonical | 9.4 | Hernquist | **0.154** | 0.188 | -0.204 | none | 0 | 0 | 0.42 |
| canonical | 10.45 | Plummer | **0.138** | 0.185 | -0.114 | 0 to 0.59 | -0.012 | -0.25 | 0.58 |
| canonical | 10.45 | Hernquist | 0.0660 (at the line) | 0.091 | -0.104 | none | 0 | 0 | 0.36 |
| canonical | 10.7 | Plummer | **0.114** | 0.154 | -0.093 | 0 to 0.58 | -0.010 | -0.25 | 0.56 |
| canonical | 10.7 | Hernquist | 0.056 | 0.079 | -0.092 | none | 0 | 0 | 0.35 |
| canonical | 10.9 | Plummer | **0.099** | 0.134 | -0.081 | 0 to 0.57 | -0.009 | -0.25 | 0.55 |
| canonical | 10.9 | Hernquist | 0.050 | 0.072 | -0.084 | none | 0 | 0 | 0.34 |
| alt | 9.4 | Plummer | **0.357** | 0.435 | -0.323 | 0 to 0.63 | -0.027 | -0.25 | 0.68 |
| alt | 9.4 | Hernquist | **0.169** | 0.205 | -0.221 | none | 0 | 0 | 0.42 |
| alt | 10.45 | Plummer | **0.156** | 0.209 | -0.130 | 0 to 0.59 | -0.014 | -0.25 | 0.59 |
| alt | 10.45 | Hernquist | **0.074** | 0.100 | -0.114 | none | 0 | 0 | 0.37 |
| alt | 10.7 | Plummer | **0.130** | 0.175 | -0.107 | 0 to 0.58 | -0.012 | -0.25 | 0.57 |
| alt | 10.7 | Hernquist | 0.063 | 0.087 | -0.100 | none | 0 | 0 | 0.35 |
| alt | 10.9 | Plummer | **0.114** | 0.154 | -0.093 | 0 to 0.58 | -0.010 | -0.25 | 0.56 |
| alt | 10.9 | Hernquist | 0.056 | 0.079 | -0.092 | none | 0 | 0 | 0.35 |

Bold = above the SPARC line. Every Plummer row also fails the frozen rho_c < 0 test, which on its own sets the label.

Checks:
- The Jeans form of rho_c and the Poisson form agree to 1e-9 or better in every row.
- The direct ODE with P = J returns the law around a point mass to 1e-9 dex over 0.3 to 30 r_M.

**A1 rule as frozen:** STRUCTURE FAILS AT A1 on both footings. On each footing all four Plummer masses fail both the
negative-density test and the line, and Hernquist fails the line at log M_b 9.4 (and, alt, at 10.45).

## A1c, reported (point mass; no label)

| x = r/r_M | sigma^2 / sqrt(G M_b a0) | d ln sigma^2 / d ln r | sigma^2 / v_c^2 | Knudsen sigma tau / r, eta 0.3 / 1 / 3 |
|---|---|---|---|---|
| 0.3 | 1.656 | -0.915 | 0.459 | 1.28 / 4.26 / 12.8 |
| 1 | 0.733 | -0.407 | 0.453 | 1.27 / 4.23 / 12.7 |
| 3 | 0.563 | -0.125 | 0.477 | 1.30 / 4.34 / 13.0 |
| 10 | 0.517 | -0.035 | 0.492 | 1.32 / 4.41 / 13.2 |

- A local Maxwellian is a stationary solution of the collisionless operator only where sigma^2 is uniform. Inside about
  3 r_M, sigma^2 varies, so even around a point mass f = f_law balances only at the level of the Jeans equation, not as a
  kinetic steady state.
- With tau = eta t_orb the Knudsen number is about 4.3 eta at every radius. The BGK steady state is therefore not close
  to f_law there, and its density was not computed.
- So even the point-mass "holds" is a Jeans-level statement. This item is reported, not graded.

## Known answers and MUTATE

| item | canonical | alt | line | result |
|---|---|---|---|---|
| KA1 point-mass M_ph closed form vs integral of rho_ph | 1.5e-7 | 1.5e-7 | 1e-6 | PASS |
| KA2 Newtonian limit (a0 x 1e-6), Plummer | 8.7e-6 | 1.1e-5 | 1e-4 | PASS |
| KA3 deep limit (a0 x 1e8), Plummer and Hernquist closed forms | 6.1e-8 | 5.1e-8 | 1e-4 | PASS |
| KA4 compact Plummer (b = 1e-4 r_M) = law at r >= 0.1 r_M | 9.6e-8 dex | 9.6e-8 dex | 1e-3 dex | PASS |
| M1 target spread doubled (P = 2J): point mass off the law | 0.516 dex | 0.516 dex | > line | BITES (exit 1) |
| M2 identity checked against 2 a0 rho_b | residual nonzero | | nonzero | BITES (exit 1) |
| M3 no target pressure (J = 0): point mass off the law | 1.48 dex | 1.48 dex | > line | BITES (exit 1) |

## Hand estimates against the outcome

- **Mine** (written in the criteria before any script): A1 fails on extended spheres.
  - Right: the a0 rho_b residual, the negative cored centre (I wrote g ~ pi G rho_b0 r, as found), and the label.
  - Too small: I guessed the Hernquist offsets at about -0.05 dex (10.9) and -0.13 to -0.17 dex (9.4). The far-field
    offsets are -0.084 and -0.20.
- **The closure chat's:** "A1 holds; A2 is where it most likely breaks (the law's exact stress is a field stress, not a
  pressure)." The reason is right, but the break comes one item earlier. The anisotropic part of the field stress
  already matters in a sphere wherever baryons sit, so an isotropic spread fails before discs enter.

## What this does and does not close

- **Closed:** a medium that settles irreversibly onto a target with a local, isotropic velocity spread J(g). That covers
  the candidate as written, for any tau rule, because the static state fails before any dynamics enter.
- **Not closed (not graded here):**
  - a target carrying the non-local baryon column (reading D);
  - an anisotropic positive spread tensor. The law's own anisotropic stress has negative radial tension in the deep
    field, so any positive tensor would have to differ from it and would not be local (M5 S2);
  - the dynamics: A3's energy sink, A4, and Part B's amount and reach.
- Any successor has to beat a0 rho_b inside the baryons with something that is still a velocity spread.
- What was not run: A2 (discs), A3 (H-theorem, removed energy against SMF1 / PAR1), A4 (expansion, TK1's edge), A5 (hot
  rule) and Part B (the collapse). The stop rule ends the lane at A1.

## Disclosures

- The first run of `set1_a1_sym.py` printed FAIL on one check. sympy did not reduce sqrt(u^2 + 4u + 4) to u + 2 for
  u > 0, so the expression was printed unsimplified, though it is zero. A first fix attempt garbled the expression. The
  checker now factors the radicand before taking the root. No criterion, line or physics changed, and the other checks
  gave the same output in all three runs.
- Before the first run of `set1_a1_num.py`, `np.trapz` was routed through a helper for portability.
- The Hernquist 10.45 canonical row prints as 0.0660 and was flagged above the 0.0660 line at full precision. It is
  not needed for the label.
- R_50 uses SCS2's Shen et al. relation, which SCS2 quoted from memory. It was read, not re-sourced. Spherical toy
  profiles stand in for galaxies, as the brief specified for A1.
- Compute: each script runs in under a few seconds, single thread, `nice -n 10`, while other lanes' jobs were running.

## Files and re-run

- `FROZEN_CRITERIA.md`, committed alone first.
- `python3 set1_a1_sym.py` (exit 0); `SET1_MUTATE=M2 python3 set1_a1_sym.py` (exit 1).
- `python3 set1_a1_num.py`; `SET1_MUTATE=M1|M3 python3 set1_a1_num.py` (exit 1 each).
- Outputs: `.out` / `.json`, with `_MUTATE_<arm>` for the MUTATE runs.

Commits (local / origin): criteria d6ebdb40dd / 459ba348fb.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
