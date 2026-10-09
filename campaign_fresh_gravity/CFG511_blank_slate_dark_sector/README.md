# CFG511: a blank-slate look at dark energy and cold energy

**Bottom line.** The four fresh ontologies tested here fail in their simplest form, each for a specific, named reason:
- The cold energy cannot be the vacuum's response to bound or overdense regions. The CMB measures its smooth, mean density at z = 1100, to 1%,
  when nothing is bound (bound fraction ~10^-1989).
- It cannot be horizon information. The Hubble-radius version does not accelerate. The event-horizon version has the wrong w(z), 7-8 sigma
  from DESI.
- It cannot be one viscous medium. The friction that would make the acceleration also stops structure from growing.
- It cannot be one elastic medium with a single stiffness. The rigidity gives the cold energy a sound speed of order c and erases structure.

One variant is still standing: the elastic vacuum with its rigidity left free (a knob). In it, dark energy is the vacuum's tension and cold
energy is stored strain. It makes one prediction that two independent components do not make:

- **a0 follows the tension, -p_DE, not the energy density.** With DESI's w(z), a0 at z = 2.5 comes out at 1.02-1.15x its value today (DESI
  plus supernovae). The record's two-component law gives 0.78-0.83x. The gap is 0.09-0.17 dex, about the reach of the record's decisive
  a0(z = 2.5) test.

This variant also allows energy to pass from the relaxing tension into cold strain. DESI's growth data cannot see that (Delta chi^2 <= 0.25).

kappa = 1/2 is FITTED. The cold energy's mass is still required and its amount is still an input. No particle is proposed. Nothing here closes
the theory.

**Files and runs.**
- `FROZEN_CRITERIA.md` was committed alone first, in 930d9760a.
- Script: `cfg511_blank_slate.py`. It runs in about 36 s with `nice -n 15` and at most 4 processes.
- Main run: `cfg511.out` and `cfg511_results.json`. Exit 0; controls K1-K6 all pass.
- `CFG511_MUTATE=1` writes `cfg511_MUTATE.out` and `cfg511_results_MUTATE.json`. Exit 0. All three plants behave as frozen:
  - M1: a bound-phase whose bound fraction is 1 at all times reads CONSISTENT-BUT-EQUIVALENT.
  - M2: cold c_s^2 = 0.01 is EXCLUDED (Delta chi^2 +504).
  - M3: 1.5x clustering cold energy is EXCLUDED (Delta chi^2 +2590).
- **Data.** All already on disk; nothing was downloaded:
  - the DESI DR2 w0wa chains (DESI+CMB, +Pantheon+, +Union3, +DESY5);
  - the DESI DR1 f sigma8 ratios (L181, through CFG508);
  - CAMB;
  - CFG508's linear solver, imported read-only;
  - literature rows from the record's catalogue (`CFG1_evidence_audit.py`), marked LIT.

## STEP 1: what the data require (no model priors)

Status key:
- **M** = MEASURED: only FLRW kinematics or a direct observable is assumed.
- **I** = INFERRED: model-dependent; the model is named.
- **U** = UNKNOWN.

Ranges are 68%. Where four values are listed they come from the four chains, in this order: DESI+CMB / +Pantheon+ / +Union3 / +DESY5.

### Dark energy

| property | constraint | status | source |
|---|---|---|---|
| density vs time | rho_DE(z)/rho_DE(0): at z = 1, 1.22 / 0.98 / 1.07 / 1.02 (+-0.05-0.15); at z = 2.5, 0.53 / 0.68 / 0.61 / 0.64 (+-0.1). It rises to z ~ 0.5-1 and falls beyond | I (CPL) | S1 |
| equation of state | w0 = -0.41 / -0.84 / -0.67 / -0.75; wa = -1.75 / -0.61 / -1.08 / -0.85. w(0.5) = -1.00 / -1.04 / -1.03 / -1.04 (+-0.03): phantom near z ~ 0.5, above -1 today | I (CPL) | S1 |
| acceleration today | q0 = +0.10 [-0.13, +0.31] (DESI+CMB) / -0.37 +- 0.06 / -0.17 +- 0.10 / -0.27 +- 0.06 | M with SN; weak without | S1 |
| sound speed | not measurable while w ~ -1 | U | — |
| anisotropic stress | — | U | — |
| clustering | none detected; expected unobservable near w = -1 | U (smooth assumed) | — |
| interaction with ordinary matter | — | U | — |
| momentum / flows | no rest frame is measured | U | — |
| bound vs unbound regions | if a0 = kappa c sqrt(G rho_DE) holds locally, a0 being the same across SPARC (g-dagger 1.20e-10), MeerKAT (1.05e-10, CFG301) and the gas-point value (8.3e-11, PAPER43) means the local rho_DE equals the cosmic value within ~+-0.2 dex. This compares galaxy samples; it is not an environmental test | I (the bridge) | record |
| relation to a0 | a0 = kappa c sqrt(G rho_DE); kappa = 0.465 +- 0.076 (BTFR) or 0.55 +- 0.17 (distance-free); FITTED. a0(z) is calibration-limited | I (single epoch) | STANDING |
| exchange with cold energy | the background measures only the SUM of the two densities, so any exchange is degenerate with w(z) at background level. Growth: a full exchange split of DESI's w(z) shifts DESI f sigma8 by Delta chi^2 <= 0.25 | M (the degeneracy); exchange U | S6 |

### Cold energy

| property | constraint | status | source |
|---|---|---|---|
| density vs time | omega_c = 0.1196 / 0.1190 / 0.1193 / 0.1192 (+-0.0008), anchored at z ~ 1100. Omega_c,0 = 0.297 / 0.261 / 0.275 / 0.268. About 5.4x ordinary matter | M (CMB) + I (a^-3) | S2 |
| equation of state | dilutes like a^-3. With c_s^2 = 0, constant w_c: -0.011 < w_c < +0.018 (DESI f sigma8, Delta chi^2 = 4), or \|w_c\| < 0.0063 (5% sigma8). LIT GDM analyses are tighter (~1e-3; not recomputed) | I (linear GR) | S4 |
| sound speed | independent cold fluid: c_s^2 < 1e-6 (DESI f sigma8, Delta chi^2 = 4), < 2e-7 (5% sigma8). The Lyman-alpha forest (k ~ 1 h/Mpc, +-14%) is tighter | I (linear GR) | S3; A13 |
| anisotropic stress | no slip seen: CMB lensing A = 1.011 +- 0.028 (ACT 1.013 +- 0.023), and KiDS lensing RAR = dynamical RAR | I (GR lensing) | A11, A07a (LIT) |
| clustering | clusters on every probed scale: BAO / P(k) at ~150 Mpc, the forest at ~1 Mpc, galaxy halos, mergers | M (linear) / I (small scales) | A12a, A13 |
| interaction with ordinary matter | not dragged by the cluster gas: the Bullet lensing-gas offset is 8 sigma | M | A09c (Clowe+06) |
| self-interaction | sigma/m < 0.47 cm^2/g (Harvey+15) or ~2 cm^2/g (Wittman+18), contested; in non-particle terms, a column of ~1 g/cm^2 passes through itself without losing its momentum | M (bound; contested) | A09d |
| momentum / flows | keeps its momentum through cluster collisions (Bullet). Its velocities follow GR plus dust growth (DESI f sigma8 chi^2 = 4.56 for 6 points at Planck LCDM) | M / I | A09c; S3 |
| bound vs unbound regions | **present and smooth when nothing is bound.** At z = 1100 the bound fraction is 10^-1989 (M >= 1e3 Msun) and omega_c is measured to 1%. Bound fraction for M >= 1e3 Msun: 10^-3.5 at z = 30, 0.19 at z = 10, 0.88 at z = 0. The law's phantom arrangement is seen only in bound systems (record) | M (unbound presence) / I (the arrangement) | S5 |
| relation to a0 | in galaxies its distribution is fixed by the baryons and a0: RAR scatter 0.108 dex (SPARC). Its amount is not tied to a0 (CFG496: 0 of 15 clues) | M (RAR) / I | A03a; CFG496 |
| ratio to dark energy | rho_c/rho_DE changes ~8x by z = 1 and ~36x by z = 2: no fixed ratio | I (CPL) | CFG508 |

**What this means.** The data need two behaviours:
- smooth, accelerating, with a slowly changing density;
- pressureless (|w_c| ~< 1e-2, c_s^2 ~< 1e-6), collisionless at the Bullet level, keeping its momentum, already homogeneous and present at
  z = 1100, and arranged by the a0 law inside bound systems.

The only link between the two that has been measured is a0 (single epoch, kappa fitted).

## STEP 2 + 3: four fresh ontologies

### O1. Elastic vacuum: tension and strain

**What it says.** Spacetime is a medium. Dark energy is its isotropic tension (w = -1 while the tension holds). Cold energy is strain energy
stored in point-like strain centres, so it dilutes as a^-3.

**Q1a, one modulus.** This is the minimal form: one material constant sets both the tension and the rigidity. The strained part then has a
shear sound speed c_s^2 = rho_DE/rho_c, which is 2.6 today (capped at 1).
- Result: Delta chi^2 +416; sigma8 drops to 0.04x.
- **EXCLUDED.**

**Q1b, relaxing tension.** When the tension changes, the energy it releases becomes cold strain: rho_c = Omega_c a^-3 + (1 + w) rho_DE.
This uses no new constant.
- With the DESI chains, the cold energy today is 1.42-1.81x the CMB extrapolation (2.25x DESI+CMB only). The new energy is born uniform, so
  the clustered mass hardly moves.
- DESI f sigma8: Delta chi^2 = +0.11 to +0.25 (born at rest in the cold frame) and +0.03 to +0.06 (born at rest in the vacuum frame).
- Not excluded, and invisible to current growth data.

**Q1c, a0 set by the tension -p_DE.** a0(z)/a0(0) = sqrt(w rho_DE / (w0 rho_DE,0)).

| a0(z)/a0(0) | z = 1, O1 | z = 1, H2 | z = 2.5, O1 | z = 2.5, H2 |
|---|---|---|---|---|
| +Pantheon+ | 1.16 | 0.99 | 1.02 | 0.83 |
| +Union3 | 1.39 | 1.03 | 1.15 | 0.78 |
| +DESY5 | 1.26 | 1.01 | 1.07 | 0.80 |
| DESI+CMB | 1.94 | 1.11 | 1.46 | 0.73 |

H2 is the reference: two independent components.
- DESI's density decline at high z is offset by w < -1 there, so the tension stays near its present value at z ~ 2.5. This makes a0 nearly
  flat at z = 2.5 even though rho_DE evolves.
- It is not excluded, since a0(z) is calibration-limited on the record.
- It is fixed with no knob, and the gap from H2 is 0.09-0.17 dex.
- Separately, kappa on the tension footing would be kappa/sqrt(-w0), 1.09-1.22x for the SN chains. kappa is fitted, so this is no test.

**Verdict.** The minimal form (one modulus) is **EXCLUDED**.

The knob variant (rigidity mu free, c_s^2 = mu/rho_c < 1e-6) is **CONSISTENT-AND-DISTINCT**. Its distinct, checkable prediction is a0(z)
following -p_DE (Q1c). The test that separates it from H2 is a0 at z ~ 1 and z ~ 2.5 to 0.1 dex. Q1b's exchange stays below current
growth reach.

Honest reading: the sound-speed part of the variant only renames things (mu -> 0 is H2). Its content is Q1c, a different bridge, a0 proportional
to sqrt(G x tension), which equals the record's bridge exactly when w = -1.

### O2. Two-phase medium keyed by boundedness

**What it says.** One medium. It is the smooth tension outside bound regions, and it condenses into the cold phase inside them.

**Q2a.** The mean cold density follows the bound fraction. At z = 1100 that predicts omega_c of 10^-1989 times the measured value, even
counting every clump down to 1e3 Msun. The CMB measures the HOMOGENEOUS cold density (equality, the peak ratios) to 1%.
- **EXCLUDED.**

**Q2b.** If the cold phase forms in any overdense region instead, the comoving amount grows with the growth factor. That is 697x between
z = 1100 and today. The a^-3 dilution allows at most a 0.37 change in ln(amount) (S4).
- **EXCLUDED.**

**Verdict: EXCLUDED** (both forms).
- What survives is the record's own arrangement: cold energy present everywhere, with only its *arrangement* following the law in bound
  systems. That is the two-component picture plus the law, CONSISTENT-BUT-EQUIVALENT and not new.
- A version where the condensation happened once, early, and then persisted is also only a renaming of a pressureless component.

### O3. Horizon information

**What it says.** Dark energy is the information energy of the cosmic horizon (holographic). Cold energy is horizon information displaced by
matter (emergent apparent mass).

Per the record, the dS-Unruh argument is never cited for kappa; only this ontology's own numbers are used here.

- **Q3a, L = the Hubble radius.** q0 = +1/2, so there is no acceleration. That is 14.1 / 7.0 / 12.3 sigma from the SN chains (1.9 sigma for
  DESI+CMB alone). **EXCLUDED.**
- **Q3b, L = the event horizon, c_h = 1.** CPL (w0, wa) ~ (-0.91, +0.46): wa > 0, against DESI's wa < 0. That is 7.2 / 8.4 / 7.6 / 8.1 sigma.
  **EXCLUDED.** With c_h free, the best fits (c_h 0.56-0.78) are still 4.4-6.6 sigma away.
- **Q3c, the emergent cold part.** It has no homogeneous mean at z = 1100 (same test as Q2a). **EXCLUDED.**
- **Q3d, a0 = c H0/6.** As a numerical coincidence: delta = 0.153 (canonical) / 0.036 (alt) / 0.095 (SPARC g-dagger), against the 0.01 needed
  to count as a match. Look-elsewhere p = 0.97-1.00. The scrambled-cosmology check is uninformative because the value does not depend on R,
  which counts as a fail. **NO MATCH, no weight.** Its distinct prediction, a0 proportional to H(z) (3.7-3.9x at z = 2.5), is the record's
  known rival, not a new one.

**Verdict: EXCLUDED.**

### O4. Viscous unified medium ("the friction of space")

**What it says.** One medium. Dark energy is its bulk-viscous resistance to expansion (Pi = -rho_Lambda c^2, so zeta = rho_Lambda c^2/(3H)).
Cold energy is the same medium's rest energy. The background is LCDM exactly.

**Q4a.** The same viscosity damps compressive flows at the rate Gamma/H = (Omega_Lambda/(3 Omega_c(a))) (k c/(aH))^2. Growth stalls from
z ~ 20 at k = 0.1 h/Mpc (a hand estimate, not computed by the script).
- Result: Delta chi^2 +240; sigma8 drops to 0.13x.
- **EXCLUDED.**

The variant where viscosity acts on the smooth part only is two components (CONSISTENT-BUT-EQUIVALENT).

**Verdict: EXCLUDED.**

### Summary

| ontology | dark energy is | cold energy is | minimal form | surviving variant | its distinct, checkable prediction |
|---|---|---|---|---|---|
| O1 elastic vacuum | vacuum tension | stored strain (point-like centres) | EXCLUDED (one modulus: c_s^2 ~ 1) | rigidity free: **CONSISTENT-AND-DISTINCT** | a0 follows -p_DE: a0(1)/a0(0) 1.16-1.39, a0(2.5)/a0(0) 1.02-1.15 (H2: 0.99-1.03, 0.78-0.83); tension-to-strain exchange below growth reach |
| O2 bound-keyed two-phase medium | outer phase | the bound / overdense phase | EXCLUDED (z = 1100 mean, 10^-1989; the overdensity form 697x) | only the record's arrangement (EQUIVALENT) | — |
| O3 horizon information | holographic horizon energy | displaced information | EXCLUDED (q0; DESI 7-8 sigma; z = 1100) | none | — (a0 proportional to H is the old rival) |
| O4 viscous medium | friction of expansion | the medium's rest energy | EXCLUDED (Delta chi^2 +240, sigma8 0.13x) | smooth-only viscosity (EQUIVALENT) | — |

## Controls, post-freeze notes and limits

**Controls.**
- K1: the growth ODE and the damped solver match CFG508's solver to 3e-7; LCDM chi^2 = 4.559 (L181: 4.56).
- K2: the exchange-split identity holds to 2e-16.
- K3: the per-chain a0(2.5) values reproduce CFG508's 0.827 / 0.782 / 0.798.
- K4: the HDE w0 identity holds exactly, and the direct event-horizon integral agrees to 1e-5.
- K5: CAMB sigma8 = 0.8228, and f_bound(z = 0, M >= 1e12 Msun) = 0.46.
- K6: the coincidence test fires on a planted exact form.

**Post-freeze notes, disclosed.**
- P1, two bugs caught by the controls before any verdict was used:
  - the damped (O4) solver was missing a Hubble-friction term (K1 failed at 5.2; fixed; O4 went from Delta chi^2 +33 to +240);
  - the CAMB sigma8 array was indexed wrongly (K5).
- P2: the frozen text did not say how to combine chains for Q3a. Exclusion is taken to need every SN-including chain at >= 3 sigma. The
  DESI+CMB chain alone puts q0 = +1/2 at 1.9 sigma (its CPL q0 is broad); this is reported.
- P3: K3 compares against CFG508's per-chain values, which covered only the three SN chains. DESI+CMB gives 0.729 and is reported.

**Limits.**
- CPL is a stand-in for w(z). The chains are treated as 2-D Gaussians in (w0, wa) for O3.
- Linear, sub-horizon theory throughout. Alcock-Paczynski and distance effects are ignored in the f sigma8 comparison.
- S4 ignores the evolution before z = 200 and radiation.
- S5 is a Press-Schechter estimate, with a power-law P(k) tail beyond k = 5000 h/Mpc. The z = 1100 verdict has thousands of decades of margin.
- The S3 and S4 bounds are the first grid point to cross.
- LIT rows are not recomputed.
- Q1c is untested on data. a0(z) at z ~ 1-2.5 is calibration-limited on the record.

**Standing.** kappa = 1/2 is FITTED. The cold energy's mass is still required and its amount is an input. No dark-matter particle is proposed.
This is not "theory closed".
