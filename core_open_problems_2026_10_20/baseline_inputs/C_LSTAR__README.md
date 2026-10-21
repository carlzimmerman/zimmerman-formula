# PARAMRED lane C (LSTAR): what is the stiffness length L*?

**Verdict. Part 1: CONSTRAINT TIGHTENED (the upper edge, previously only a grid edge, is now a number; approximation-conditional).
Part 2: NO REDUCTION (no derivation fixes L*).** kappa = 1/2 fitted; both footings never pooled; not "theory closed".

Files: `FROZEN_CRITERIA.md` (written first; addendum at the end), `lstar_constraints.py`, `lstar_constraints.out`,
`lstar_constraints_results.json`, `lstar_constraints_MUTATE.out`, `lstar_constraints_results_MUTATE.json`.
Run: one process, 7.6 s, 181 MB RSS (MUTATE 1.1 s, 140 MB). 8/8 controls pass; MUTATE (S = 1) finds no edge on either footing (bites).

## 1. Allowed interval (numbers from `lstar_constraints_results.json`)

| end | value | what sets it |
|---|---|---|
| lower | **5.650 pc** (the 5.754 pc of CFG691 is the next 0.01-dex grid point above it) | Saturn enclosed-mass gate, M_an = M (r/L*)^2 < 6.7e-11 Msun at 9.54 AU (CFG691 G-SS). Footing-free (the inner pull GM/L*^2 is a0-free) |
| upper | **2.04 kpc canonical / 2.14 kpc alt** | raw SPARC rms line 0.110 (CFG4 line), CFG691's own statistic scanned to 30 kpc (rms 0.1023 at 1 kpc, 0.1096 at 2.04 kpc, 0.2224 at 30 kpc; monotone, no later re-pass) |

Width 2.56 / 2.58 decades. The upper edge is **not** a bound from any other observable.

Lower-end gates, all on the record: Saturn 5.650 pc; 1 AU gate (3.66e-14 m/s^2) 1.951 pc; star halos (CFG694 G3 / CFG658 E3,
(1.08 pc / L*)^2 <= 0.155) 2.743 pc, conditional on the 1.08 pc truncation; Cassini Q2 (CFG770, Q2 ~ L*^-3, worst 3.47e-6 of the
ceiling at 5.75 pc) 0.087 pc. DR3 wide binaries (CFG658 E1): L* -> 0 gives gamma-hat 1.500, excluded at +7.73/+8.25 sigma; L* = 5.754 pc
gives 1.0162/1.0200 (-0.82/-0.83 sigma). No injection at 0 < L* < 5.754 pc exists, so DR3 gives no further bound. Sealed
predictions are L*-scalings, not bounds: CFG774 pull 4.22e-15 (5.75/L*)^2 m/s^2 (1.4e-19 at 1 kpc); CFG771 stress ~ L*^-2; CFG772 lab
null is L*-independent in the committed form. The CFG774 kill line 1e-13 maps to L* <= 1.18 pc, below the Saturn edge: a detection
kills the stiffened action, it does not select an L*.

**What the "> ~1 kpc" in THEORY_CANONICAL rests on.** It is CFG691's grid edge (1000 pc), reported there as "L*_max >= 1000 pc, a lower
bound, not a measured edge". CFG760 G3 incidentally computed rms 0.1718 at 9.55 kpc and 0.1609 at 7.59 kpc (fails), which already showed
a finite edge existed; this lane located it: 1.4-2.6 kpc across lines 0.105/0.110/0.115 and the two mass rules (5 of 6 edges found;
the sixth, line 0.105 with enclosed mass, lies below 1 kpc). So SPARC bounds L* above, at about 2 kpc, with a systematic of x1.4 to x2
from the screening approximation. At the edge the profiled Upsilon_disk is 0.47/0.44, below the CFG4 band: the CFG690 inheritance, not a pass.
Dwarfs are the lever: l_gamma = L*^2 / (2 r_M) grows as M^-1/2.

## 2. Gaia DR4 (2026-12-02) mapped onto the interval (formula of CFG740, error model of CFG816, s = 50 kAU = 0.2424 pc)
- A null at the registered precision (N = 1421 ... 1e5, sigma_tot 0.090 ... 0.023, floor 0.02) gives 2-sigma L* >= 0.41 ... 0.81 pc.
  **This is below the Saturn edge at every N: a null cannot move the lower edge.** To exceed it a null needs sigma < 4.6e-4 on
  gamma_v - 1, 43 x below the irreducible floor, at any N. (Using the 236 kAU bin at the same error would give 1.9-3.8 pc, an
  extrapolation outside the registered statistic, still below.)
- A detection b = R - 1 maps to L* = s / sqrt(2b): b = 0.003 -> 3.1 pc, 0.01 -> 1.71 pc, 0.05 -> 0.77 pc, 0.15 -> 0.44 pc: all below
  the Saturn edge. So a boost bigger than 9.2e-4 at 50 kAU is incompatible with the stiffened action at ANY allowed L*; it kills it (CFG816's
  rule: R - 1 >= 0.01 at 3 sigma). The zone b in (9.2e-4, ~0.07) is untestable at DR4.
- Consequence: **DR4 cannot tighten or fix L*. It can only kill the construction.**

## 3. Part 2: is L* tied to anything? No.
- **D-A (theorem).** Only G carries kg, so a combination G^a a0^b that is a length needs a = 0, then seconds force b = 0. No length from {G, a0}.
  The static action's single new dimensionful constant is its own.
- **D-B (scale).** With c, the only length is c^2/a0 = 9.60e26 m = 3.11e10 pc (canonical; 2.57e10 pc alt), 1.5e7 x the SPARC edge. A tie needs a
  dimensionless number of 1e-7 to 1e-10; kappa, Omega_c/Omega_b, Omega_Lambda are O(1). Not a search; no combination was tuned.
- **D-C (c_P).** c_P = sqrt(gamma/I), gamma = 2 pi G L*^2. For an independent light field I is a second free constant: no tie. For the
  identification P = -rho_c xi (I = 1/rho_c) there IS one, c_P = L* sqrt(2 pi G rho_c), and CFG744/CFG699 tested it at L* = 5.754 pc only.
  With CFG744's own law (t ~ L*^-2) relaxation within 4.6 Gyr needs L* >= 188-13,723 pc (canonical) / 159-11,628 pc (alt), all twelve cases: the top
  exceeds the SPARC edge, so the branch is closed over the whole window. **Caveat:** at those L* the law's s0 falls to 5.0-5.8, below its
  fitted range (10-80), and the necessary-only one-crossing bound opens at 3-800 pc, inside the window. The closure over the window rests on the
  s0^(3/2) law extrapolated, as CFG744's own did.
- **D-D (gap).** The vacuum has no mass term (CFG694 G1); the gap belongs to a background and L* is its unit of length. CFG760 G3 (P-wave export) needs
  L*_all = 9.55 / 7.59 kpc, above the SPARC edge: closed over the window (5 of 8 cases open by 1 kpc; the record needs all).
- Capacity a0/(pi G) is a surface density, and the S4 selector (CFG782, DEAD) contains no L*.

## 4. What pins L*
L* is an inequality with a data-set upper edge, not a derived parameter. **Lower end:** a tighter bound on the anomalous enclosed mass or a
direct detection of the constant sunward pull GM/L*^2 (4.2e-15 m/s^2 at 5.65 pc, 1.4e-19 at 1 kpc; CFG774). L*_min ~ B^-1/2: probing 100 pc
needs a bound 313 x tighter than 6.7e-11 Msun, 1 kpc needs 3.1e4 x. **Upper end:** an extended-source solution of the stiff equation (not on the
record) scored on dwarfs; UFDs are the pc-scale lever (generic, unscored: S = 0.58 at 1e3 Msun, r_h = 30 pc, L* = 5.754 pc; 3.7e-5 at 1 kpc).
No single measurement fixes both.

## Not verified / disclosures
- The SPARC upper edge uses CFG691's point-mass screening of extended systems, at exactly the radii where l_gamma ~ galaxy size; the 0.110 line is a
  campaign threshold, not a confidence interval; the Saturn input (6.7e-11 Msun) is a 2013 number, newer ephemeris bounds are not on the record.
- UFD, CFG720 (merger lag at the L* ~ 1 kpc corner) and MW external-field effects are unscored.
- The first run exceeded the RSS limit (467 MB); rerun at 181 MB. See the addendum in `FROZEN_CRITERIA.md`.
- Hypotheses tried: 8.
