# CFG511 FROZEN CRITERIA: a blank-slate look at dark energy and cold energy

Committed alone, before any script was written and before any ontology number was computed.

## Purpose (owner, 2026-10-08)

Dark energy and the cold, lumpy energy are new kinds of stuff. This lane takes a fresh look without leaning on past work. It does not start
from particles, fields, black holes, LCDM's CDM or the record's earlier constructions. It starts from what the DATA require of the two dark
components (STEP 1). It then asks which new kinds of 'stuff' could have exactly those properties (STEP 2). Finally it checks each one (STEP 3).

Terms. "Dark energy" is the smooth component that drives acceleration. "Cold energy" is the lumpy component that gravitates, about 5.4x the
ordinary matter. The framework has one established bridge: a0 = kappa c sqrt(G rho_DE), with kappa = 1/2 FITTED (measured 0.465 +- 0.076 BTFR,
0.55 +- 0.17 distance-free). In galaxies the cold energy arranges itself into the law's phantom profile. Both footings (a0 = 9.3603e-11 and
1.1312e-10 m/s^2) are quoted and never pooled.

On-disk data only; nothing is downloaded:
- the DESI DR2 w0wa chains (DESI+CMB; +Pantheon+; +Union3; +DESY5);
- the DESI DR1 ShapeFit+BAO f sigma8 ratios as transcribed in L181 (used through CFG508's table);
- CAMB, for the Planck-2018 LCDM P_lin;
- CFG508's linear solver, imported read-only;
- committed record results and the record's literature catalogue (CFG1_evidence_audit: A09c Bullet, A09d Harvey, A11 CMB lensing, A13 forest,
  A16 GW speed, A03 RAR).
Literature numbers that are NOT recomputed here are flagged LIT.

## STEP 1 method: the data-only property list (fixed now)

For each component (DE = dark energy, CE = cold energy), one row per property:
1. energy density vs time;
2. pressure / equation of state;
3. sound speed;
4. anisotropic stress;
5. clustering, and on which scales;
6. interaction with ordinary matter;
7. self-interaction (Bullet);
8. momentum / flows;
9. response to bound vs unbound regions;
10. relation to a0;
11. energy exchange between the two.

Each row gets a value with its error bar (68% unless stated), a source, and one status:
- **MEASURED**: read from data with only FLRW kinematics or a direct observable (lensing-gas offset, a CMB-measured density) assumed.
- **INFERRED**: needs a model. Name it (CPL w0wa, linear perturbation theory with GR, the record's law, LIT bound under a particle model).
- **UNKNOWN**: no data constrain it at a level that matters.

Computed here (method fixed now; the numbers come from the script):
- **S1. rho_DE(z)/rho_DE(0)** at z = 0.5, 1, 1.5, 2, 2.5 from each DESI DR2 chain. CPL: f = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)). Weighted
  16/50/84 percentiles, first 30% of each chain dropped. Also: w(z = 0.5), Omega_DE, and q0 = Omega_m/2 + (1 + 3 w0) Omega_DE/2.
- **S2. Cold amount.** omega_c (CMB-anchored) and Omega_c,0 from the chains: weighted percentiles of omch2 and omch2/h^2.
- **S3. Cold sound speed.** Use an INDEPENDENT cold fluid (w = 0, constant c_s^2) on the Planck LCDM background, with baryons as separate dust.
  CFG508's solver is used unchanged. Scan c_s^2 over 1e-9 ... 1e-2 (log grid, 22 points). Report two upper bounds:
  - (a) the smallest c_s^2 with Delta chi^2 >= 4 on the DESI DR1 ShapeFit+BAO f sigma8 ratios (baryon velocity tracer, as CFG508);
  - (b) the smallest c_s^2 at which sigma8 of total matter shifts by >= 5% (the record's CFG361 cut).
- **S4. Cold equation of state.** Constant w_c with c_s^2 = 0 (non-adiabatic). omega_c is held at its CMB value at z = 1090:
  rho_c = Omega_c a^-3 (1090 a)^{-3 w_c}. Flatness is kept by Omega_L = 1 - Omega_b - rho_c(1). Scan w_c in +-{1e-4 ... 3e-2} (12 magnitudes
  per sign). Report the same two bounds as S3. Radiation and the pre-z = 200 evolution are neglected (disclosed).
- **S5. Bound fraction f_bound(z)** at z = 1100, 30, 10, 3, 1, 0. Press-Schechter collapsed fraction erfc(1.686/(sqrt 2 sigma(M_min, z))) with the
  CAMB P_lin (kmax 5000 h/Mpc), for M_min = 1e3, 1e6, 1e9 Msun.
- **S6. Exchange.** The background measures only the SUM of the two dark densities. A split with exchange is defined by holding H(z) at the
  chain's CPL median, keeping the vacuum part at w = -1 exactly, and sending all of its density change into cold energy:
  rho_c,ex(a) = Omega_c a^-3 + (1 + w(a)) rho_DE,CPL(a).
  Growth uses a scale-independent linear ODE with created cold energy born unclustered (delta_c' = -theta_c - q delta_c,
  q = d ln rho_c/dN + 3). Two momentum choices are scored:
  - P-c: born at rest in the cold frame;
  - P-v: born at rest in the vacuum frame (extra -q theta_c).
  The score is chi^2 on the DESI DR1 f sigma8 ratios against Planck LCDM, compared with the non-interacting reading of the same chain median
  (smooth DE). Alcock-Paczynski / distance effects are ignored (as in CFG508, disclosed).

Not computed (status from the record or LIT, with source named): anisotropic stress (CMB lensing amplitude, KiDS lensing vs dynamical RAR),
self-interaction (A09c/A09d), the interaction with baryons, the GW speed, and the clustering scales (A12a, A13).

## STEP 2: the ontologies and their declared quantitative consequences

Each ontology states what DE and CE ARE. Its MINIMAL FORM may carry no constant beyond H2's: the DE history and the cold amount, plus kappa
for a0. Its consequences Q are declared now and computed with no knob tuned to data.

**H2 (reference).** Two independent components: smooth DE with the chain's CPL history, and pressureless cold energy (c_s^2 = 0, a^-3).
a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)).

**O1. Elastic vacuum ("tension and strain").** Spacetime is a medium.
- DE is its isotropic tension T (w = -1 while T is constant).
- CE is strain energy stored in it, held in point-like strain centres so that it dilutes as a^-3.

Declared consequences:
- **Q1a, one modulus** (the minimal form: one material constant sets both the tension and the rigidity, mu = T = rho_DE c^2). The strained
  component then carries a shear sound speed c_s^2 = rho_DE/rho_c. This is run in the S3 machinery with c_s^2(a) = rho_DE/rho_c(a), capped at 1
  (the cap and any superluminal epoch are disclosed).
- **Q1b, relaxing tension.** If the tension changes (DESI's w != -1), the energy it releases becomes strain. That is exactly S6's exchange
  split. The verdict comes from S6 with no new constant.
- **Q1c.** a0 is set by the tension, i.e. by -p_DE, not by rho_DE: a0(z)/a0(0) = sqrt(w(z) rho_DE(z)/(w0 rho_DE(0))). Computed at z = 1 and 2.5
  from the chains and compared with H2.
- **Q1d, two moduli** (the rigidity mu is free). c_s^2 = mu/rho_c is bounded by S3. Since mu -> 0 reproduces H2, this variant is a knob variant.

**O2. Two-phase medium keyed by boundedness.** One medium.
- Outside bound regions it is the smooth tension (DE).
- Inside bound regions it condenses into the cold phase (CE = the vacuum's response inside bound systems).

Declared consequences:
- **Q2a.** The mean cold density follows the bound fraction: rho_c(z)/rho_c,H2(z) = f_bound(z)/f_bound(0). It is tested at z = 1100, where the CMB
  measures omega_c to 1% (the acoustic peaks and the equality epoch see the HOMOGENEOUS cold density).
- **Q2b, overdensity-keyed variant** (the cold phase forms in any overdense region, delta > 0). The mean is proportional to <max(delta, 0)> =
  sigma/sqrt(2 pi), so the amount grows with the linear growth factor. Tested as omega_c(today)/omega_c(1100) against the a^-3 dilution
  (S2 and S4).
- **Q2c.** DE converts into CE as structure forms: rho_DE(z) = rho_DE,0 + rho_c,0 (f_bound(0) - f_bound(z))/f_bound(0) ... reported only if Q2a
  is not excluded.

**O3. Horizon information.**
- DE is the information (entropy) energy of the cosmic horizon: holographic, rho_DE = 3 c_h^2 c^4/(8 pi G L^2).
- CE is the horizon information displaced by ordinary matter (emergent apparent mass).
- The record forbids citing dS-Unruh for kappa. This ontology is used for its own testable numbers only.

Declared consequences:
- **Q3a.** L = the Hubble radius. Then rho_DE = c_h^2 rho_crit and the DE dilutes like matter: q0 = +1/2 (no acceleration). Compared with q0
  from the chains.
- **Q3b.** L = the future event horizon, c_h = 1 (the saturated bound, the minimal form). Equations: dOmega_DE/dN =
  Omega_DE (1 - Omega_DE)(1 + 2 sqrt(Omega_DE)/c_h), w = -1/3 - 2 sqrt(Omega_DE)/(3 c_h). The resulting w(z) is fitted to CPL on 0 <= z <= 2.5 and
  compared with each chain as a 2-D Gaussian in (w0, wa) (CFG508's convention). The best c_h is reported as a knob variant.
- **Q3c.** The cold part is emergent from ordinary matter's displacement of horizon information. Like Q2a, it needs bound or static structure
  and has no homogeneous mean at z = 1100. Tested with S5.
- **Q3d.** The emergent scale is a0 = c H0/6 (the horizon reading's own number). As a numerical coincidence it must pass the anti-numerology
  test below. Its distinct consequence is a0(z) proportional to H(z): a0(1)/a0(0) and a0(2.5)/a0(0) from the chains, against H2.

**O4. Viscous unified medium ("the friction of space").** One medium.
- DE is its bulk-viscous pressure resisting expansion, Pi = -3 zeta H = -rho_Lambda c^2, so zeta = rho_Lambda c^2/(3H). There is no separate
  vacuum.
- CE is the same medium's rest energy (inertia rho_c). The background is identical to LCDM by construction.

Declared consequence:
- **Q4a.** The same viscosity acts on compressive perturbation flows. The Euler equation gains a damping -(Gamma/H) theta with
  Gamma/H = (Omega_Lambda/(3 Omega_c(a))) (k c/(a H))^2. This is computed on CFG508's k grid (scale-dependent ODE). Scored with the S3 bounds
  (f sigma8 Delta chi^2, sigma8 shift). The continuity-equation viscous term is O(1) not O(k^2) and is neglected (disclosed).
- **Q4b.** Viscosity acting on the smooth part only is two components. It is a knob variant, EQUIVALENT by construction.

## Classification rules (frozen)

Each ontology gets one verdict from its MINIMAL FORM. Knob variants are reported on separate lines.

1. **EXCLUDED** if any declared Q of the minimal form is off named data:
   - by >= 3 sigma (Gaussian data); or
   - by Delta chi^2 >= 9 against H2 on the 6 DESI f sigma8 points; or
   - by a factor >= 10 against a quantity measured to better than 10% (e.g. omega_c at z = 1100); or
   - by a sigma8 shift > 20% (the record's 5% cut is a gate, not data; > 20% is far outside CMB lensing A = 1.011 +- 0.028 and every S8
     survey, A12b).
   A physical pathology (superluminal or imaginary sound speed) is reported and counts against the form only if the data verdict also fails.
2. **CONSISTENT-AND-DISTINCT** if no Q of the minimal form is excluded AND at least one Q:
   - takes a fixed value (no knob) that differs from H2's value; and
   - is checkable by a named measurement.
   If such a Q sits 2-3 sigma (or 4 <= Delta chi^2 < 9) from current data, the label carries "(in tension)".
3. **CONSISTENT-BUT-EQUIVALENT** if every Q either equals H2's prediction or depends on a new free constant that can be set to reproduce H2
   exactly. Such an ontology only renames things, and the README says so.
4. A minimal form EXCLUDED with a surviving knob variant reads "minimal form EXCLUDED; knob variant CONSISTENT-BUT-EQUIVALENT" (or "-AND-DISTINCT"
   if the variant still fixes a distinct Q with its knob at the value the data require, and that Q differs from H2 at another epoch or scale).
5. A verdict is provisional on the on-disk data, CPL as a stand-in for w(z), linear theory, and kappa FITTED. Nothing here makes kappa derived,
   fixes the cold amount, or closes any theory.

## Anti-numerology control (CFG496 rules 3, 4 and MUTATE, applied unchanged)

Any numerical coincidence used to support an ontology (declared now: Q3d's a0 = c H0/6; any other that appears is added and reported) is
tested on both footings:
- **Match:** delta = |ln(v/X)| <= 0.01.
- **Look-elsewhere p:** v' = v x 10^U(-1, 1), 20,000 draws, seed 496, against CFG496's family F1 (1,053 forms) plus the ontology's own form.
  p = P(delta(v') <= delta(v)). It passes if p < 0.01.
- **Second check (scrambled cosmology):** 200 draws (seed 4960) of R' ~ U[3, 8], Omega_b fixed, flat, a0 footings held.
  - The coincidence passes only if it holds (delta <= 0.01) in < 5% of the draws while holding for the real cosmology.
  - A coincidence that does not depend on R' is uninformative under the scramble. It then cannot pass the second check (CFG496 rule 4: no
    second check = FAIL).
- **Outcome:** a coincidence that fails any step is labelled COINCIDENCE (or NO MATCH) and carries NO weight in any verdict.

## Controls (exit 0 only if all pass)

- **K1.** The scale-independent growth ODE (S6) reproduces CFG508's solver at c_s^2 = 0 (baryon velocity, z = 0, 0.5, 1.5) to 1e-3. Planck
  LCDM gives chi^2 = 4.56 +- 0.01 on the DESI table (L181 / CFG508 K4).
- **K2.** The exchange split reproduces the CPL total dark density to 1e-10 at all a (identity check).
- **K3.** The chain loader reproduces CFG508's a0(2.5)/a0(0) range 0.78-0.83 for the non-interacting reading (to +-0.01).
- **K4.** The HDE integrator reproduces w0 = -1/3 - 2 sqrt(Omega_DE0)/3 to 1e-6. Integrating the event horizon L directly from H(z) gives the
  same Omega_DE(z) to 1e-3.
- **K5.** CAMB sigma8 from the Planck set-up is within 0.80-0.83, and f_bound(z = 0, M >= 1e12 Msun) is within 0.1-0.6.
- **K6.** The anti-numerology family test fires on a planted exact form: v = (1/6) x 3 pi kappa Omega_m gives delta = 0 and p < 0.01.

## MUTATE (frozen; `CFG511_MUTATE=1`, separate outputs)

- **M1.** A planted "bound-phase" ontology with f_bound == 1 at all z (identical to dust) must come out NOT EXCLUDED by the Q2a test, and as
  CONSISTENT-BUT-EQUIVALENT.
- **M2.** A planted independent cold fluid with c_s^2 = 1e-2 must be EXCLUDED by the S3 rules.
- **M3.** A planted split whose clustering cold density is 1.5 x Omega_c a^-3 at all a must be EXCLUDED by the growth score. The vacuum part
  takes up the difference, so H(z) is unchanged; the created energy is born clustered (P-c with q = 0).

The MUTATE run exits 0 when M1-M3 come out as stated. If one fails, the test cannot discriminate and the lane is VOID in that part.

## Stated in advance (rough expectations, written before any computation; they may be wrong)

- O2 (bound-keyed) and O3's cold part are expected to fail at z = 1100, since nothing is bound then.
- O4 is expected to be over-damped and EXCLUDED.
- O1's one-modulus form is expected to be EXCLUDED. O1's relaxing-tension and tension-sets-a0 predictions are the most likely survivors.
- O3b (event horizon, c_h = 1) has wa > 0 in the literature, against DESI's wa < 0. Expected disfavoured.
- Most knob variants are expected to be CONSISTENT-BUT-EQUIVALENT (renamings).

kappa = 1/2 is FITTED. No dark-matter particle. The cold energy's mass is still required and its amount is an input. Never "theory closed".
