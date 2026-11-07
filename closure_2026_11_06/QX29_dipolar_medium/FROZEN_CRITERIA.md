# QX29 frozen criteria: a gravitationally polarizable medium (dipolar class) as a cold dark energy sector

Frozen before any QX29 script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane.
Rules: ../SWARM_BRIEF.md. The sector is called the COLD DARK ENERGY sector with a dipole moment field.
- **Disclosure:** the owner's no-particle rule is relaxed for this TEST lane only. Nothing here is a particle claim,
  and the lane adopts nothing.
- No LCDM inputs.
- Prior work (qwen_claude_field_theory/papers_2026/LCDM_FRIED_CHICKEN, recipe25) is background only. None of its outputs
  are inputs here.

## a0 and the law (owner requirement, 11-06)

- a0 = kappa c sqrt(G rho_DE) on the framework's two footings only: canonical 9.3603e-11 m/s^2 and alt 1.1312e-10 m/s^2.
  The footings are never pooled.
- The law is used only in its own simple-mu form, g_N = g^2/(g + a0), so mu(x) = x/(1 + x) with x = g/a0.
- Standard MOND's a0 = 1.2e-10 is never used, and neither is any other interpolating function. That holds in calibration,
  in the known-answer checks and in the dipolar W.
- Check KA0 (below) FAILS the run if the string for 1.2e-10 appears as an a0 value in any QX29 script.

## The class (nonrelativistic static limit, as written for this lane)

- **Fields.** The medium has a monopole mass density sigma, which is cold and pressureless. Its dipole moment per unit
  mass is xi, and the polarization is Pi = sigma xi.
- **Field equation.** Poisson is div g = -4 pi G (rho_b + sigma - div Pi), with g the gravitational field.
- **Equilibrium of the dipoles.** The internal potential W(|Pi|) aligns Pi with g, and its equilibrium is
  dW/d|Pi| = |g|.
- **W, chosen by a rule fixed here.** W is the unique function for which spherical statics reproduce the law exactly,
  with the law applied to the full monopole source (rho_b + sigma). That requires 4 pi G Pi = (1 - mu) g = a0 g/(g + a0).
  With y = 4 pi G |Pi|/a0 < 1, this gives
  W(Pi) = (a0^2/(4 pi G)) [ -y - ln(1 - y) ].
  - The rule is derived, not fitted. It has no constant beyond a0.
  - Pi saturates at Pi_s = a0/(4 pi G).
  - Then div(mu g) = -4 pi G (rho_b + sigma): the static field is AQUAL with the law's mu, sourced by baryons plus the
    medium's monopole.
- **Monopole dynamics, as the class is written here.** The monopole obeys dv/dt = g. The dipole force (Pi.grad)g is
  smaller by about xi/r and is dropped in the dipole-continuum regime. So the monopole is cold dust:
  - it clusters on the linear web (T1);
  - it falls into every host whose turnaround sphere contains it.
  This reading of the BLT-type equations is stated, not certified. The relativistic BLT completion is not built here.

## Host rules for sigma (each graded as a separate candidate; none tuned to clusters)

| id | rule | status |
|---|---|---|
| A | "Weak clustering": sigma in hosts = the cosmic mean sector density RHO_D0 (QX10's value). The monopole adds nothing; the hosts see exactly the law (AQUAL) | the hypothesis of the dipolar literature; ASSUMED, not derived (it contradicts the dust dynamics above) |
| B1 | Captured cold dust: M_X(<r) = R M_b(<r), with R = 5.562 (QX12 iter_2's T1 amplitude). The medium traces the baryons, as in the QX12 / QX27 convention | derived amount (all dust inside r_ta); record profile convention |
| B2 | Captured cold dust in a self-similar cold-infall profile: rho_X ∝ r^-9/4 inside r_ta, so M_X(<r) = R M_b,tot (r/r_ta)^(3/4) for r < r_ta and R M_b,tot beyond. Here r_ta is QX10's rule and M_b,tot is the host's baryon total | derived amount; profile from Newtonian EdS secondary infall, not re-derived with the law on (disclosed) |
| Bcal | The B2 profile with amplitude f R. f is the largest value on a 61-point log grid 1e-4 to 1 at which C1 (SPARC G5 inner mass), C2 (KiDS) and G7 (dSphs) all pass, there and at every smaller grid value. Cold-dust capture has no scale, so the same f applies to every host, clusters and groups included | the most medium galaxies allow; f is fixed by galaxies only |
| C | The minimal medium: sigma(r) = |Pi(r)|/r, the least monopole that can carry the needed polarization with dipoles no longer than the radius (xi <= r). It is solved self-consistently with the law to r_ta, and M_X is held constant beyond r_ta | derived floor from the dipole-continuum condition |

Reported variants: B1 and B2 with f_cap R, using f_cap = 0.76 (QX10's convention).

The constants are a0 (the two footings), R = 5.562 (CMB-era cold component, QX12 iter_2 / QX15), f_cap = 0.76 (QX10)
and Bcal's f (galaxies only). No cluster or group number enters any constant. There is no knob scan on clusters.

## Gates (both footings separately; QX27's grader imported read-only, its retention function replaced by the QX29 host rule)

- **G1 SPARC.** QX8's exact-field grade (algebraic law plus QX8's per-point T from its saved parts), with g_X = G M_X(<r)/r^2
  added to g_bar.
  - Line (QX8): rms <= 0.110 and median U in [0.50, 0.80].
  - Hosts: exponential discs with M_b = 0.5 L[3.6] + 1.33 M_HI and R_opt = 3.2 Rdisk, as QX27.
  - C1 (QX10 line, G5 list), M_X(<R_opt)/M_b <= 0.3, is graded inside G1: G1 PASS needs both.
  - QX8's exact field is AQUAL with this mu, which is the class's own static field.
- **G2 KiDS isolated lenses.** QX10 / QX12 line: |mean shift| <= 0.05 dex, using QX27's calib C2 with the law base. This
  is a prediction for A, B1, B2 and C. For Bcal it is a calibration gate and is reported as such.
- **G3 X-ray ellipticals.** QX18's line on the absolute offset: |D| <= 0.15 dex, with D = mean log(M_obs/M_pred) at 2, 4
  and 8 Re.
- **G4 X-COP.** HO1 line: |mean| <= 0.05 and rms <= 0.10 dex on log(M_obs/M_law(M_b + M_X)). These are the QX12 iter_3 / A1
  hosts, as QX27 grades them.
- **G5 groups (Lovisari).** QX5's mean-band rule over the two stellar allowances. QX10's strict count is reported.
- **G6 growth and CMB-lensing shape.**
  - The monopole is pressureless dust from before recombination. On QX27's G6 line (QX3 iter2 growth ODE, PR4
    lensing, Delta chi^2 <= 4 against the cold reference) it is the cold reference, so Delta chi^2 = 0.
  - The polarization's linear-order effect is not derivable here. AQUAL about g = 0 is not linearizable, because
    mu ∝ |g|. G6 is therefore graded under QX3's assumption A-web (a0 does not enter at linear order).
  - Label: PASS [A-web CONDITIONAL]. The control run (the QX27 G6 machinery: cold limit sigma 0.01 km/s, and the
    medium smooth from z 1089) must show that the gate has power.
  - If CLASS or PR4 cannot run, G6 is NOT EVALUABLE and the missing input is stated.
- **G7 dSphs.** The 8 MW classical dSphs, QX27's hosts. Line: median shift <= 0.05 dex.
- **G8 Solar System / Cassini.** The class's static field is AQUAL with the law's mu; the medium adds no screening length.
  - Graded on the record: E2 R1 (PAPER58, AQUAL, law, no turn-off) Cassini Q2 over Hees at the four external fields, read
    from doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json, and the Saturn monopole anomaly
    delta g = g_law - g_N against 7.0e-15 m/s^2 (AX1's bound).
  - PASS needs Q2/Hees <= 1 at all four fields and Saturn <= 1.
  - Reported: a W with the high-g turn-off (E2 R1 66.3803 entry).
  - Reported: the local dipole length xi = Pi/sigma for each host rule, against 1 AU.
- **G9 Bullet Cluster offset.** NOT EVALUABLE unless a lensing-convergence map, gas maps and a 3D non-spherical merger solve
  for the medium (collisionless monopole plus AQUAL polarization) can be built in small compute. The missing inputs are
  stated. A qualitative statement is reported, not graded.
- **G10 dipole-continuum consistency (internal, like QX27's G8).** Pi = sigma xi is a valid continuum description only if
  xi = |Pi|/sigma <= r at the graded radii.
  - Graded radii: every KiDS lens radius, every galaxy's last SPARC point, the X-COP and group radii and the dSph r_half.
  - PASS if xi/r <= 1 at all of them.
  - C passes by construction (reported as such).
  - The maximum and the median of xi/r are reported.

## Labels

- Per candidate (A, B1, B2, Bcal, C), per gate, per footing: PASS / FAIL. G6 is PASS [A-web CONDITIONAL] or NOT EVALUABLE.
  G9 is NOT EVALUABLE unless built.
- **PASSES ALL (EVALUABLE)** only if one candidate passes G1-G5, G7, G8 and G10 on both footings, with G6 at least
  conditional. If G9 is not built, the label says so.
- Otherwise the class **FAILS**. For each candidate the README lists its failing gates and maps each failure to a triangle
  corner:
  - T1: G6.
  - T2: G1/C1, G2, G3, G7.
  - T3: G4, G5.
  - Solar System: G8.
  - Internal consistency: G10.

## Known answers (run before the candidate grades; written to the main output)

- **KA0.** No QX29 script contains the string for 1.2e-10 as an a0. The FAIL condition is a regex match of "1.2e-10",
  "1.20e-10" or "1.2*1e-10" in any QX29 .py file, built in code so that the check cannot match itself.
- **KA0b.** A0K[f] times the kpc-unit conversion equals 9.3603e-11 / 1.1312e-10 to 1e-4 relative. glaw obeys
  g_N = g^2/(g + a0) to 1e-10 over g/a0 in [1e-4, 1e4].
- **KA1 (the derived W).**
  - Root-solving dW/dPi = g for Pi and forming g_N = g - 4 pi G Pi returns g^2/(g + a0) to 1e-10 over g/a0 in [1e-4, 1e4].
  - A finite-difference dW/dPi equals g(Pi) to 1e-6.
  - 4 pi G Pi / a0 -> 1 at g/a0 = 1e4, to 1e-3.
- **KA2.** Candidate A's ellipticals D equals QX18's +0.210 / +0.189 within 1e-3.
- **KA3.** Candidate A's X-COP mean equals +0.4675 / +0.4345 within 2e-3.
- **KA4.** Candidate A's G1 equals QX8's 0.0560 @ 0.58 / 0.0558 @ 0.52 within 1e-4.
- **KA5.** The B1 machinery at amplitude 0 equals candidate A to 1e-6 on X-COP.
- **KA6.** The Saturn delta g computed here equals AX1's static "law" Saturn_dg to 1e-6 relative, if AX1's json is on
  disk; otherwise this is reported as not checked.
- **KA labels.** If a KA fails, it is reported, and the dependent gate is graded as computed, with the failure disclosed.

## MUTATE twins (separate outputs qx29_MUTATE.*)

- **M1, polarization off, pure cold mass (the required twin).** Newtonian g = g_N (mu = 1, W = 0) with the B2 medium at
  amplitude R. It must FAIL at least one of G1-G5 and G7 on both footings, or it does not bite.
- **M2, polarization off with candidate A.** Newtonian baryons only. It must fail G1 on both footings.
- **M3, B1 machinery at amplitude 0.** It must return candidate A's X-COP within 2e-3. This shows that the amplitude is
  what the cluster grade rests on.
