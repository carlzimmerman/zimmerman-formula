# CFG360 FROZEN CRITERIA: the baryon tie, i.e. can the cold amount be fixed by the baryon excess?

Committed alone, before any script. kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans. Never "theory closed". Owner scope (2026-10-06): "yes scope the baryon-tie lane".

**Question.** Gap 2 (CFG288 G-AMOUNT): the cold fluid's amount is a free number (misalignment amplitude, or shift charge C;
CFG288 A2 proves C is a free integration constant). Can one early process set BOTH the baryon excess and the cold
fluid's charge, so that the measured ratio follows from the framework rather than being fitted?

**Target (data, both quoted, never pooled).**
- CMB: R_CMB = omega_c / omega_b = 0.1200 / 0.02237 = 5.364 +- 0.065 (Planck 2018 TT,TE,EE+lowE+lensing; errors combined
  in quadrature, correlation ignored and disclosed).
- Clusters: R_cl = 5.73 +- 0.68 (L49 X1, a0-independent). Reported only; R_CMB is the scored target.

## The bookkeeping identity (stated before any mechanism)
For the CFG288 wave field (complex Phi, U(1) charge density n_c, nonrelativistic, one sign of charge):
rho_c = m n_c. Hence

    R = rho_c / rho_b = (m / m_p) (n_c / n_b) = (m / m_p) r,     r = charge per baryon.

Every candidate below must report m, r and R. A mechanism "ties" only if it fixes r (and m) from the action and the
framework's own constants {kappa, a0, H0, Lambda, G, hbar, c, m_p}; m_p enters only through n_b.

## Tests
**T0 (controls, must pass first).**
- T0a: reproduce R_CMB = 5.364 from the two quoted omegas.
- T0b: re-read the CFG288 wave-field mass window from CFG288's committed outputs (lower edge m >= 2e-20 eV, CFG345
  m >= 2.3e-20 eV). Do not hard-code the upper edge: read it or derive it from the classical-wave requirement
  (occupation >> 1 at the cluster/dwarf phase-space density). Report both edges and their source.
- T0c: reproduce A1 (dust before z_eq needs a potential >= 1.5e10 rho_Lambda) from CFG288.

**T1 (minimal tie, expected FAIL, declared now).** Equal charges, r = 1: m = R_CMB m_p = 5.03 GeV. Graded against the T0b
window and the no-particle rule. A 5 GeV quantum with occupation << 1 is a particle species (asymmetric dark matter), not
a classical fluid. Verdict: inside window, or outside.

**T2 (required charge per baryon).** Map the T0b window to r_req = R_CMB m_p / m (about 1e8 to 1e29 for the remembered
window; the script's number governs). Any mechanism must land r in that band.

**T3 (G9 gate: coupling route).** CFG329 G9 PASS: matter couples to g only. Classify each mechanism:
- (a) gravitational-only (production from curvature or the baryon-sourced field during an early epoch);
- (b) a shared conserved current (e.g. B - k Q_c conserved), which needs a non-gravitational baryon-to-Phi coupling. Then
  G9 must be re-run and the fifth-force/EP bounds (Eot-Wash, MICROSCOPE) applied at the implied coupling.
  A (b) mechanism that breaks G9 is NO-GO regardless of R.

**T4 (timing).** The fluid must exist at its full amount before z = 1e5 (CFG288: seeding at <= 1e4 EXCLUDED; 1e5
undecided) and must add no radiation at BBN (N_eff 2.99 +- 0.17, CFG254). The tie must operate at T > 1 MeV, before BBN.

**T5 (look-elsewhere control, mandatory for any numeric match).** If r or m is built from framework constants, enumerate
the grammar of the p60 machinery (products and powers of {kappa, 2, pi, a0, H0, rho_Lambda, G, hbar, c, m_p, M_Pl} up to
the same depth), count forms that land R within 1 sigma of 5.364, and report the base rate. A match counts only if the
chosen form's chance probability is < 1e-3 AND a mechanism (T3) produces that form. Otherwise: NUMEROLOGY, not a tie.

**MUTATE.** Re-run T2 and T5 with a planted target R = 3.00 +- 0.065. T5 must flag a comparable number of chance hits
(within a factor 3 of the real-target count), or the look-elsewhere machinery is not discriminating and the lane is void.

## Verdict classes (declared)
- **TIED:** a mechanism of class (a), or (b) passing G9, fixes r and m with ZERO new constants; R within 1 sigma of
  R_CMB; T4 passes; T5 chance < 1e-3. Then Omega_c h^2 leaves the parameter count.
- **CONDITIONAL:** as TIED but with exactly ONE declared new constant. Relocated, not reduced. Say so.
- **NO-GO:** every enumerated mechanism class fails T1-T4. Recorded as a design constraint on Gap 2.
- **OPEN:** a class cannot be decided with local compute. Name what would decide it.

## Scope limits
- Local compute only. No downloads (every input number is quoted above or in committed files).
- The cluster ratio R_cl is never pooled with R_CMB.
- CFG338/339/340 (cold share from pre-reionisation baryons, galaxy scale; withdrawn as a solution in CFG340) is a
  different question (local share, not the cosmic amount) and is cited, not reused.
- Wording rules: a T5-failing coincidence is reported as a coincidence. "Derived" only under TIED.
