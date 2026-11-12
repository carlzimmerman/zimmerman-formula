# PIK2 RESULT (blind): the gated dust term graded. CMB-ONLY / CMB-ONLY (canonical / alt)

Criteria 95edd35e0b (committed alone, before any script or number). Scripts and runs ccc4f4fc92. No amendment.
Written before PIK1's RESULT.md, its scripts, any correction notice, the Codex audit or the research_closure folder was
opened. TEST lane: adopts nothing, relabels nothing (PIK1's committed label is untouched), registers nothing. Footings
never pooled. kappa = 1/2 FITTED; not theory closed.

## Label

**CMB-ONLY / CMB-ONLY** at mu_K = 2.512e4 per Mpc (primary). The same label holds at 198.25 per Mpc and, reported, at
8.89e6 per Mpc. No (S, xi) opens a window on either footing. All known answers pass. Every mutation bites.

What CMB-ONLY means here, plainly:
- **Galaxies are passed only by shutting the gate everywhere the law is measured.** The galaxy side (rows 2, 5, 6, 7 and
  row 8 at galaxy radii) passes only for three gates: F2 = exp(-u^2), F3 = exp(-u^3) and the step. It needs a low
  threshold, xi <= 10^0.7 to 10^1.65 (Pi_c <= 5 to 45 rho_d0 c^2, rho_d0 = 2.27e-27 kg/m^3). At those thresholds u >= 10
  at every graded radius of every galaxy, group and cluster, so S is effectively zero there. The key "lifts" the galaxy
  bound by switching the dust off. It does not tune it.
- **X-COP has no value for any gate, at any threshold, at any of the three mu_K.** The best rms is 0.39 to 0.48 at the
  primary mu_K, against the line 0.10. At the galaxy-side thresholds X-COP sits at the plain law (+0.467 / +0.435 mean).
- **Where a gate puts group-sized dust into the groups, the gated term is unhealthy there by 13 to 18 orders of
  magnitude.** Groups pass only in narrow threshold bands. There row 8b reads S''(u) (rho_K1/rho_c)^2 / (mu Lstar)^2 =
  1e13 to 2e18 (line 1). Row 8a reads 1e3 to 1e9 (line 0.02).
- **Row 2 (VISIBLE for E1, P1, P2, P4, F2):** linear invisibility is not a property of the action. The four gates that
  are not flat at the origin (S''(0) > 0) fail linear health at every threshold on the grid at 2.512e4 and at 198.
- The window line is not met, so there is no hit to re-grade.

The decisive numbers (primary mu_K; canonical / alt):

| quantity | value |
|---|---|
| X-COP best rms over all gates and thresholds | 0.390 / 0.390 (gate P2, xi = 10^-1.25; line 0.10); no X-COP pass anywhere |
| row 8b where the groups pass (all gates but the step) | 1.2e13 to 2.4e18; row 8a there: 6e3 to 1.4e9 |
| highest threshold at which the galaxy side passes | F2 10^0.7 / 10^0.8, F3 10^0.95 / 10^1.1, step 10^1.55 / 10^1.65; X-COP phantom density there >= 769 / 856 rho_d0, so u >= 17 to 140 |

## Row 0: certified variation

All of row 0 passes (`pik2_row0.out`).
- **C0a: the gate's second-order action about FRW, in unitary gauge, three space dimensions, general S.** It is checked
  as an exact constant term on a 3-torus, with trigonometric lapse, spatial-metric and P^i perturbations and S symbolic
  to cubic order. The result equals the hand form exactly (difference 0):

      delta2 S_gate = Int a^3 [ -(s1/Pi_c) (F/Q)'(Qbar) P^i d_i dQ + (s2 / 2 Pi_c^2) (F/Q)(Qbar) (d_i P^i)^2 ]

  Here s1 = S'(0), s2 = S''(0) and (F/Q)'(Qbar) = rhobar_d/Qbar^2 exactly. **S'''(0) and every higher derivative drop
  out.** The tadpole vanishes because P^0 = 0 and the background F/Q is spatially constant.
- **C0a' (KA3):** Int sqrt(gamma)(F/Q) Pi = -Int sqrt(gamma) P^i d_i(F/Q), exact at orders eps^1, eps^2 and eps^3.
- **C0b:** the static weak-field Euler-Lagrange equations of the gate term, with lapse N = 1 + Phi, generic S and 3D P,
  equal the hand forms exactly:
  - lapse equation: d[N F(1/N)]/dN S;
  - P equation: -grad[N F(1/N) S'/Pi_c].
- **C2:** the energy density is (mu^2/2K)(Q^2 - 1) S, so the dust is rho_K = -mu_K^2 S Phi/(4 pi G).
- **C3:** Pi does not depend on the lapse.
- **The law shift.** In SI the law acts on Phi - c^2 Gm, with c^2 Gm = mu^2 Phi^2 S'(u)/(8 pi G rho_c). It is Newtonian:
  c cancels.
- **Out of scope, as frozen:** the full covariant stress tensor, the covariant khronon equation and the collapse.
- **Disclosed:** the first M-ID run did not bite C0a at eps^2. The chosen torus modes made the P.grad(sqrt gamma)
  overlap vanish by symmetry. A cos(x)/2 term was added to h_22, and both the primary and the mutant were re-run. The
  primary still passes; M-ID now fails C0a and C0a' (`pik2_row0*.out`).

## Row 2: linear visibility, health and growth about FRW

**(i) Visibility (from C0a).** The gate changes the linear equations about FRW iff S'(0) != 0 or S''(0) != 0.
- **VISIBLE:** E1, P1, P2, P4 and F2.
- **INVISIBLE at linear order:** F3 = exp(-u^3), R3 = 1/(1+u^3) and the step. Their S'(0) = S''(0) = 0. The step is
  invisible until a perturbation reaches u = 1, which is non-linear.

**(ii) Sub-horizon Newtonian reduction** (stated assumption; the algebra is certified in `pik2_row0.out`).
- W is taken as K P^2/2. That holds because the foliation's acceleration on linear scales is about 1e-25 m/s^2,
  far below a0.
- Integrating out P, Phi and Psi gives the charge equation
  `ddot delta + 2H dot delta = K rhobar_m delta - K rhobar_d k^2 delta / M`, with
  - `M = mu^2 + beta k^2`, `beta = (1 + e1)^2 / K_P`, `K_P = 1 - e2 k^2/K`;
  - `e1 = s1 rhobar_d/(Qbar^2 rho_c) = s1 (1+z)^3/xi`;
  - `e2/K = s2 (rhobar_d/rho_c)^2/(2 mu^2) - theta Lstar^2/2`, where theta = 1 on the Pi > 0 branch (gamma_L acts) and
    0 on the Pi < 0 branch.

**Finding beside the label (KA4, not graded).** Even with no gate (S = 1), the law's P sector is not negligible at
linear order. It is the A^2/2K term, so M = mu^2 + k^2. Then omega^2 = -K rhobar mu^2/(mu^2 + k^2): there is no Jeans
oscillation, only growth slowed above k ~ mu. Without P the record's n = 1 polytrope, omega^2 = K rhobar (k^2/mu^2 - 1),
comes back (KA4 passes both ways). The record's Jeans line (QX3, KD1 G9a) was computed without the P sector. For
k << mu the two agree.

**(iii) Health H2: K_P > 0 and M > 0 at every physical k in [1e-4, 1e6] per Mpc, z in [0, 3400], on both branches.**
- **E1, P1, P2, P4 (S''(0) > 0): fail at every one of the 281 thresholds, at 2.512e4 and at 198 per Mpc.**
  - K_P passes through zero at k_* = mu sqrt(2/s2) xi/(1+z)^3, and M < 0 beyond it. The khronon's kinetic coefficient
    turns negative (a ghost) and the growth rate rises with k without bound.
  - Example, E1 at xi = 1e3 and mu 2.512e4: unhealthy from z = 2.4 to 3400, at physical k >= 9.1e-4 per Mpc at z 3400.
    That is every comoving scale above 2.7e-7 per Mpc.
  - At 8.89e6 they pass only for xi >= 10^9.5 to 10^10.15. Those thresholds are far above every static row's densities,
    so the gate is shut in every system.
- **F2 (s2 = -2):** healthy everywhere (beta in (0, 1]).
- **F3, R3 and the step:** healthy (invisible).

**(iv) Growth G2, standing in for a CMB-lensing likelihood: |D_gate/D_ungated - 1| <= 0.01 at 0.01, 0.05 and 0.2 h/Mpc,
z 3400 to 0.**
- F2 passes at 2.512e4 and at 8.89e6 (ratio 1.0000).
- **At 198, F2 fails for xi < 10^11.2.** Its ratio at 0.2 h/Mpc is 0.372. The flat gate removes the P sector's softening
  (beta -> 0), so the polytrope's Jeans pressure returns at k ~ mu.
- E1 to P4 have no growth number where H2 fails. Their coefficient is singular along the history, which is flagged and
  not integrated.
- **Row 2 passes** for F2, F3, R3 and the step at 2.512e4. At 198 it passes for F3, R3 and the step, and for F2 only at
  xi >= 10^11.2.

**Reading.** PIK1's argument (the gate is invisible because Pi = 0 on FRW) holds only for the background. At linear order
the gate is visible whenever S'(0) or S''(0) is non-zero. Its strength e1 = s1 (1+z)^3/xi is about 1e5 to 1e9 at
recombination for any threshold the static rows could use (xi ~ 1 to 1e4). Only gates flat to second order are
invisible.

## Rows 3 to 8 (static), at the primary mu_K

The graded reading puts the dust on the law's dust-free phantom of the baryons and keeps the law unmodified (rows 8a and
K-SC check both). The proxy rows 5 and 6 compare the gated dust with MK1's ungated bound at every radius.

| gate | X-COP best rms (mean) | groups pass at log xi | SPARC / KiDS / Sun passes (of 281) | galaxy side passes for log xi | row 2 |
|---|---|---|---|---|---|
| E1 | 0.469 (+0.420) / 0.438 (+0.422) | 1.6-1.65 / 1.6-1.7 | 84/47/137 / 85/49/138 | (rows 5-7: <= 0.3 / 0.4) | FAIL (H2) |
| P1 | 2.616 (-2.512) / 2.570 (-2.464) | none | 0/0/122 / 0/0/123 | none | FAIL |
| P2 | 0.413 (+0.287) / 0.390 (+0.279) | -1.25 to -1.1 / -1.3 to -1.1 | 40/0/136 / 39/0/137 | none | FAIL |
| P4 | 0.442 (+0.355) / 0.415 (+0.349) | 0.9-1.0 / 0.9-1.0 | 75/31/146 / 75/32/147 | (rows 5-7: <= -0.5 / -0.45) | FAIL |
| F2 | 0.472 (+0.459) / 0.440 (+0.424) | 2.2-2.25 / 2.2-2.3 | 96/59/142 / 97/62/143 | **-2 to 0.7 / -2 to 0.8** | PASS |
| F3 | 0.475 (+0.466) / 0.443 (+0.432) | 2.4-2.45 / 2.4-2.5 | 100/64/143 / 101/66/144 | **-2 to 0.95 / -2 to 1.1** | PASS |
| R3 | 0.432 (+0.330) / 0.407 (+0.323) | 0.2-0.3 / 0.2-0.3 | 63/17/138 / 63/18/139 | none (row 8b at galaxy radii fails) | PASS |
| step | 0.476 (+0.467) / 0.444 (+0.435) | 2.7-2.8 / 2.75-2.85 | 107/72/146 / 108/74/147 | **-2 to 1.55 / -2 to 1.65** | PASS |

- **Rows 3-7 together pass nowhere**, so no K-SC re-run was triggered. Groups and X-COP never pass together.
- **X-COP's shape.** The best rms values sit 4 to 26 times above the line. At these mu_K the ungated dust in a cluster is
  about 1e-16 kg/m^3, against about 1e-24 needed. A gate must therefore sit near 1e-8 in clusters. Every graded family
  varies over orders of magnitude across 0.1-0.7 R500 at that level, so the dust lands at the wrong radii.
- **Densities probed** (phantom / rho_d0):
  - X-COP points 769-1.05e4 (canonical) and 856-1.18e4 (alt); groups 466-2.1e3.
  - Galaxies at 1-30 kpc: 2.2e3 (1e9 Msun at 30 kpc) to 3.2e6.
  - The Sun's 8 kpc: 1.9e5.
  - So a 1e9-1e10 galaxy at 30 kpc sits at cluster densities. The ordering is not clusters-low, galaxies-high at all
    radii.
- **Row 8 at the galaxy-side passes:** below both lines, because S, S' and S'' vanish (u >= 10). R3 never passes 8b at
  galaxy radii. Its tail S'' ~ 12 u^-5 times (rho_K1/rho_c)^2 ~ 1e20 exceeds (mu Lstar)^2 = 0.30 / 0.33.
- **The flat-gate family on halo backgrounds.** F2, F3 and R3 have S'' > 0 for u above 0.71, 0.87 and 0.79. Wherever
  such a gate is partly open in a halo, row 8b fails by 1e14 to 1e18. Flat gates are healthy on static backgrounds only
  where they are shut. This is a fixed-metric statement with gravity not coupled.

Secondary (198.25) and reported (8.89e6) mu_K give the same picture (`pik2_static.out`, `pik2_grade.out`). There is no
X-COP pass, and the galaxy side passes only for F3 and the step (plus F2 at 8.89e6), at low thresholds.

## Known answers (all pass)

| | what | value |
|---|---|---|
| KA1 | S = 1, X-COP: additive mean at 0.1; mean-zero mu (additive, action-exact) | +0.4644 / +0.4317; 1.778 / 1.736; 1.534 / 1.456 (MK1 1.53 / 1.46) |
| KA2 | mu_B1a from w(z 3400) = 0.01 | 198.254 / 198.245 |
| KA3 | identity of C0a' | exact (0 at eps^1-3) |
| KA4 | reduction: no P gives the polytrope; P and S = 1 give beta = 1 | exact |
| KA5 | phantom: finite difference / MK1 lib vs closed form; closed vs deep at x = 1e3 | 4.7e-10 / 4.6e-7; 1.2e-7 |
| KA6 | S -> 1 dust vs MK1/QX2 construction | 0 |
| KA7 | groups at mu 0 | [+0.196, +0.359] / [+0.158, +0.320] |
| KA8 | Saturn at 2.04e4; mu_7 | 7.52e-14; 6223.35 |
| KA9 | rho_d0 recomputed in SI from H0 and Omega_d; c^2 Gm by the energy-unit route | 2.27174e-27 / 2.27152e-27 kg/m^3 (rel 0); rel 0 |

## MUTATE (all bite)

- **M-S1** (S = 1): at 2.512e4 rows 5, 6 and 7 fail at every threshold, and X-COP's mean is -8.08. Bites.
- **M-SIGN** (S = exp(+u)): rows 5, 6 and 7 fail at every threshold at 2.512e4. Bites.
- **M-PIB** (u read from the baryon density): row 6 passes 0 times, against 47 / 49 for E1 and 59 / 62 for F2. The groups
  pass band moves (E1 log xi 0.65-0.9 against 1.6-1.65). Bites. Disclosed: the galaxies are point masses, so their
  baryon density outside the centre is zero and the gate is fully open there.
- **M-NOCAP** (rows 5 and 6 uncapped): row 6 passes drop from 47 to 31 (E1) and from 59 to 44 (F2). The F2 galaxy side
  shrinks to log xi <= 0.15. Bites. The label does not turn on the cap: F3 and the step still pass the galaxy side at low
  thresholds.
- **M-ID** (sqrt(gamma) dropped from Pi): C0a and C0a' fail. Bites (after the mode change disclosed in row 0).
- **M-S2** (sign of the s2 term flipped): E1 becomes healthy at every threshold and F2 unhealthy at every threshold
  (2.512e4). Bites.

## Disclosures and what was not computed

- **Not computed:**
  - a CMB-lensing likelihood (G2 is a growth-factor stand-in);
  - the full covariant equations;
  - SPARC and KiDS through MK1's own graders (rows 5 and 6 are a proxy inequality on point masses);
  - the gated term's back-reaction on the law, which is only bounded by row 8a, never solved;
  - non-spherical states, the collapse, and any Lean.
  - The step's surface (a delta function in S') is not graded in row 8.
- **Run history:**
  - The first row-2 run was stopped by hand, with no number used: integrating through singular coefficients was too
    slow. Histories with a sign change of M or K_P are now flagged as singular instead of integrated.
  - The static script gained a guard, log10 of max(ratio, 1e-300), after M-SIGN crashed on an infinite model. The
    primary run was repeated with the guard and its numbers are unchanged.
  - The baryon density for the growth background is omega_b = 0.02237. It enters a ratio only.
- **Blindness:** see READING in FROZEN_CRITERIA.md. Nothing further was seen before this file was committed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
