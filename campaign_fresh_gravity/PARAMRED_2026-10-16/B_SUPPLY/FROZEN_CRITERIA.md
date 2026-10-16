# PARAMRED lane B (SUPPLY): is Omega_c/Omega_b forced by the framework's own supply structure? FROZEN CRITERIA

Date 2026-10-16. Written BEFORE any script exists in this directory. Part 2 (the numeric predictions) is appended after the
prediction stage has run and BEFORE the comparison stage is run; Part 1 is never edited afterwards.

Settings (standing): kappa = 1/2 is FITTED. Footings a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2 are scored
separately and never pooled. Cold energy keeps its required mass; no particle species is added. This is not "theory closed".
Omega_c/Omega_b = 5.364 +- 0.065 (CMB pair; CFG642 row, THEORY_v3 section 2) is the measured target.

**Honesty about blinding.** The target value is stated in the lane brief and in the theory documents, so the author cannot
be blind to it. The protocol is therefore procedural: the code path of the prediction stage (`PREDICT`) uses no target
constant (the target is defined only in the compare section of the same script) and reads no file from the CFG721 ladder;
its numbers are frozen into Part 2 of this file; only then does `COMPARE` read the target.

## 0. Record check (done before proposing; these lines are NOT re-run)

- CFG642: formula search for 5.364 (Buckingham-pi monomials of G rho_b/H^2, a0/(cH), kappa, 11 geometric prefactors) is
  chance level. Any closure below that reduces to "a length c/H times a density equals a0/G" is inside that search space.
- CFG461/462/488: what sets the supply edge dynamically (settling temperature, khronon lapse, co-settling) -> no class
  passes, restatement only. The edge is a postulate (supply = x times catchment baryons), not a derived stopping point.
- CFG720/721 (H-OF, H-OF2): supply overflow (supply above what the tether holds) fails as the origin of the massive-system
  excess; the tethered phantom never reaches the cap a0/(pi G) for nu_s. CFG722/724: tether capacity <= a0/(pi G); a tethered
  core expels any excess over the law. CFG726: merger memory fails. CFG782: photo-evaporation selector DEAD; CFG784 not run.
- CFG423/424/518: mass-conserving edge; the supply edge is DEFINED by M_c(r_edge) = supply, i.e. it is built from x.

## 1. Notation (all derived from the record; nothing new is introduced)

- x = S/M_cat = Omega_c/Omega_b: supply per catchment baryon (the measured target).
- f_c = condensed fraction of catchment baryons (CFG652 catchment rule M_cat = M_src/0.10 in the CFG721 ladder, f_c = 0.10).
  sigma = S/M_src = x/f_c.
- Deep law (S2/S3): M_c(r) = r sqrt(M_src a0/G); supply edge r_s = (1 + sigma) r_M, r_M = sqrt(G M_src/a0) (Lean
  supply_radius_bound). Boost at the edge nu_edge = 1 + sigma.
- Tether capacity Sigma_cap = a0/(pi G) (CFG722/724), which is the y -> infinity supremum of (nu_s - 1) y a0/(pi G).
- Spherical turnaround at age t0: r_ta = (8 G M_ta t0^2/pi^2)^(1/3), M_ta = M_cat (1 + x) (cold energy gravitates).
- Zero-gravity (free-fall basin) surface of a halo of total mass M_tot in a dark-energy background:
  r_0^3 = G M_tot / H_L^2 (CFG693 basin = largest closed level surface of the free-fall potential).

## 2. The logical test applied to every closure (stated before computing)

For a universal x the tethered mass of a halo of source mass M is T(M; x) = min(x M_cat, cap(M)), with cap(M) the deep-law
capacity inside the basin (r_ta). Two regimes only:
- supply-limited (x < x_cap(M)): T = x M_cat identically. Any statement "tether holds the supply" is an identity in x.
- capacity-limited (x > x_cap(M)): T = cap(M), independent of x. The remainder is free cold energy (S4/overflow).
x enters a tether-derived relation only at the single boundary x = x_cap(M). Hence any closure built from what the tether
holds is either an identity (no prediction) or trades x for a reference mass M_ref (or a held fraction q*).
A second, independent argument (A0): Omega_c/Omega_b is already present at z ~ 1100 (CFG649: before any basin cold energy is
ordinary cold matter), and cold mass is conserved (S4 permanence), so late-time halo structure cannot determine it; a
late-time relation can only be a coincidence relation, not a derivation of an initial amount.

## 3. The closures (hypotheses), equations, and what each predicts

- **C1** (cosmic-mean tether = supply). sum_halos w(M) T(M;x) = x sum w M_cat. Holds iff the weight w is supported on
  x <= x_cap(M): a one-sided bound, not an equality. For a delta weight at M_max it is x = x_cap(M_max). Needs a baryon
  weight w (a halo mass function: not framework-native here), so it is evaluated only at declared M_max.
- **C2a** (supply edge = turnaround basin edge, class M_ref): (1+sigma) r_M = r_ta  <=>  x = A(M)(1+x)^(1/3), with
  A(M) = sqrt(M_src a0/G) (8 G M_cat t0^2/pi^2)^(1/3)/M_cat. Same equation as C1 at M = M_ref (counted as a separate
  hypothesis, no new numbers). Predicts x_cap(M) ~ M^(-1/6).
- **C2b** (supply edge = zero-gravity basin edge): ((1+sigma) r_M)^3 H_L^2 = G M_src (1+sigma)  =>
  1 + sigma = a0^(3/4) / ((G M_src)^(1/4) H_L),  x = f_c sigma. Predicts x ~ M^(-1/4).
- **C3a** (capacity saturation by the catchment-averaged supply surface density at r_ta): x M_cat/(pi r_ta^2) = a0/(pi G)
  =>  x = a0 r_ta^2/(G M_cat), r_ta as above. Predicts x ~ M^(-1/3).
- **C3b** (capacity saturation by the cosmic baryon column): rho_b ell = a0/(pi G) with ell = c/H_f (radius, "R") or
  2c/H_f (diameter, "D"), H_f = sqrt(8 pi/3) a0/(kappa c) (the footing's own Hubble rate; canonical: H_Lambda, alt: H0).
  x_pred = (a0/(pi G))/(rho_b ell). Mass-independent. This lies inside the CFG642 search space (a0/(cH) times density ratios);
  it is evaluated only because the brief asks for it, and an O(1) agreement here would be a coincidence relation (A0).
- **C4** (S4 population fractions close the budget). x M_cat = T + F_merger + F_evap. Every term of the pure partition is
  proportional to the supply except T = min(x M_cat, cap), so the partition fixes the FREE FRACTION F(M; x) = max(0, 1 -
  x_cap(M)/x), not x. A closure needs F_S4 and M_typ from outside (merger statistics; CFG782 DEAD, CFG784 not run, CFG726
  FAIL). No numeric prediction is possible on the record; the script reports the implied F(M) only.

## 4. Declared system classes (reference masses) and native scales

Declared source-mass grid, log10(M_src/Msun) = 9, 10, 11, 12, 13, 14, 15 (the CFG721 ladder points). Native (x-free) mass
scales: M_H = c^3/(2 G H_f) (horizon mass) and M_a = c^4/(G a0). They are the only reference masses the framework itself
supplies; the closures are also evaluated there (extrapolation, labelled).

Inputs used by the prediction stage (measured cosmology or census conventions, all already on the record): G, c, Msun, a0
(two footings), kappa = 1/2, t0 = 13.8 Gyr, f_c = 0.10, omega_b = 0.02237, rho_crit/h^2 = 1.87847e-26 kg m^-3,
Omega_Lambda = 0.685 (alt footing only, to convert H0 to H_Lambda).

## 5. Decision rules (frozen)

Target T = 5.364, sigma_T = 0.065; window W = 2 sigma_T = 0.130.
Per-trial chance probability (log-uniform prior on [1, 10], the CFG642 convention): p1 = (2W/T)/ln 10 = 0.0211.
Look-elsewhere: p_LE = 1 - (1 - p1)^N, N = number of distinct numeric predictions made (per footing). Trial count is also
reported as the number of hypotheses (7: C1, C2a, C2b, C3a, C3b-R, C3b-D, C4).

A closure is **REDUCTION DERIVED** only if ALL of:
- (R0) its prediction does not depend on a free reference mass: max/min of x over the declared grid <= 1 + 2 sigma_T/T = 1.0242,
  or M_ref is fixed by a rule that does not use x (the native masses are the only such rule; they must then hit the window);
- (R1) the prediction (written in Part 2 first) lies within W of T for BOTH footings (a ratio is footing independent);
- (R2) the mutated version (below) misses;
- (R3) p_LE < 0.05.
**CONSTRAINT TIGHTENED**: a closure turns an input into a one-sided bound that excludes values not already excluded on the
record. **NO REDUCTION**: otherwise, with the failing criterion named for each closure.

## 6. Controls

- N1 (implementation check, COMPARE stage): the analytic capacity ratio must reproduce the CFG721 ladder's mass trend
  (slope d ln(cap/supply)/d log10 M within 1% of -1/6 ln 10) and put the overflow onset (cap/supply = 1 at x = 5.364) within
  0.25 dex of the ledger's log M_b,OF = 13.03 / 13.05. Failure invalidates the numbers.
- MUTATE: quantity swaps that change a closure's number by an O(1) factor: C3b with rho_m for rho_b; C3b with ell = 3c/H_f;
  C2b with H_0-like rate H_f in place of H_L; C2a and C3a with f_c = 0.90 (the other CFG652 catchment branch) and t0 -> 2 t0.
  For the mass-dependent families the report is the implied crossing mass M*(closure) of x_pred(M) = T, before and after the
  mutation: if a mutant still crosses T at some mass, the hit carries no information. A closure is non-diagnostic if its
  mutants hit at the same rate as the unmutated one.
- The crossing masses M* are POST-HOC (they use the target) and are labelled so.

## 7. What would decide it (stated now)

An independent measurement of sigma = S/M_src per halo from the finite outer edge r_s = (1+sigma) r_M of isolated-galaxy
lensing profiles (S3 / THEORY_v3 section 6). That tests the identification of the cosmic ratio with the per-halo supply
(x = f_c sigma); it does not by itself derive x.

---

# PART 2: FROZEN NUMERIC PREDICTIONS (appended after the PREDICT stage ran, BEFORE the COMPARE stage was run)

Source: `B_predictions.json` (sha256 prefix 5a70edb004e62411), `B_predict.out`. Compute gate was clear (no matching process; chain log tail
showed only rc lines). Units: x = Omega_c/Omega_b-equivalent supply per catchment baryon. Grid = log10(M_src/Msun).

| closure (footing) | 9 | 10 | 11 | 12 | 13 | 14 | 15 | slope dlnx/dlnM | max/min |
|---|---|---|---|---|---|---|---|---|---|
| C1 = C2a, edge at r_ta (canonical) | 62.31 | 35.25 | 20.03 | 11.46 | 6.632 | 3.897 | 2.336 | -0.238 | 26.67 |
| C1 = C2a (alt) | 71.75 | 40.56 | 23.02 | 13.14 | 7.581 | 4.436 | 2.645 | -0.239 | 27.13 |
| C2b, edge at zero-g surface (canonical) | 87.13 | 48.95 | 27.49 | 15.41 | 8.623 | 4.805 | 2.659 | -0.252 | 32.77 |
| C2b (alt) | 100.4 | 56.43 | 31.69 | 17.78 | 9.952 | 5.553 | 3.079 | -0.252 | 32.62 |
| C3a, catchment surface density (canonical) | 1.46e10 | 1.46e9 | 1.46e8 | 1.46e7 | 1.46e6 | 1.46e5 | 1.461e4 | -1.000 | 1.0e6 |
| C3a (alt) | 2.578e10 | 2.578e9 | 2.578e8 | 2.578e7 | 2.578e6 | 2.578e5 | 2.578e4 | -1.000 | 1.0e6 |

Mass-free: C3b-R (ell = c/H_f): canonical 6.405, alt 9.354. C3b-D (ell = 2c/H_f): canonical 3.202, alt 4.677.
Native masses (M_H = 5.616e22 / 4.647e22 Msun, M_a = 6.502e23 / 5.380e23 Msun, canonical / alt): C2a 0.082 / 0.054 (can),
0.093 / 0.061 (alt); C2b negative (edge inside r_M); C3a 0.067 / 0.029 (can), 0.087 / 0.037 (alt).
C4: no numeric prediction (needs F_S4 and M_typ; not on the record).
C1 as a bound: no overflow up to M_max requires x <= x_cap(M_max): canonical 6.632 / 3.897 / 2.336 for log M_max = 13 / 14 / 15.
N distinct predictions per footing = 29; hypotheses = 7.

**Reading written before COMPARE.** By the frozen rules: R0 fails for C2a, C2b, C3a (max/min 26.7, 32.8, 1e6 against the
limit 1.0242; this is a property of the slopes, independent of the absolute normalisation). C3b is mass-free but its two
footings differ by 46% (R) and 46% (D), so R1 (both footings in the window) cannot hold for either option. All native-mass
rows are far from the window. Expected overall: NO REDUCTION.

**Known risk to control N1, recorded before COMPARE.** The analytic turnaround here is spherical, Einstein-de-Sitter
(no Lambda term); the CFG721 PM ladder's r_ta is smaller (by hand, about 12% at M_src = 1e11), which moves the analytic
onset mass (cap/supply = 1 at x = 5.364) to about 13.4 against the ledger's 13.03, i.e. beyond the frozen 0.25 dex tolerance,
because the onset mass is amplified 6x by the -1/6 slope. I keep the frozen rule: if N1 fails it is reported as FAILED, the
absolute C2a and C3a numbers are then labelled normalisation-uncertain, and only the slope-based verdict (R0) is carried.
A ladder-normalised variant of C2a is added in COMPARE as POST-HOC and circular at its calibration mass.

---

# PART 3: OUTCOME NOTES (appended after COMPARE; Parts 1 and 2 above were not edited after their dates)

Files: `paramred_b_supply.py`, `B_predictions.json`, `B_predict.out`, `B_results.json`, `B_compare.out`,
`B_results_MUTATE.json`, `B_compare_MUTATE.out`. All margins below are read from those JSON files.

**Verdict by the frozen rules: NO REDUCTION.** Trial count: 7 hypotheses, 29 distinct predictions per footing; per-trial
chance p1 = 0.0211, look-elsewhere p_LE = 0.460 (N = 29), 0.472 (N = 30 with the post-hoc reading below).

| closure | R0 (mass-independent) | R1 (both footings in +-0.130) | failing reason |
|---|---|---|---|
| C1 (cosmic-mean tether = supply) | n/a | n/a | identity below the overflow onset; above it x drops out. Equality only at one boundary mass. Bound: x <= x_cap(M_max) |
| C2a (edge = turnaround basin edge) | FAIL (max/min 26.7 / 27.1) | FAIL | x_cap ~ M^-0.24 (analytic slope -1/6 on the cap/supply ratio; ledger -0.3834/dex vs analytic -0.3838/dex) |
| C2b (edge = zero-gravity surface) | FAIL (32.8 / 32.6) | FAIL | x ~ M^-0.25 |
| C3a (catchment surface density at r_ta vs a0/(pi G)) | FAIL (1e6) | FAIL | capacity never binds at halo scales: x_pred 1e4 to 1e10 |
| C3b-R (cosmic baryon column over c/H_f) | pass | FAIL: 6.405 (+19.4%) canonical, 9.354 (+74%) alt | footing dependent (x ~ a0^2); fails the window; lies inside the CFG642 monomial family |
| C3b-D (column over 2c/H_f) | pass | FAIL: 3.202 (-40%), 4.677 (-13%) | same |
| C4 (S4 populations close the budget) | n/a | n/a | the partition fixes the free fraction F(M) = 1 - x_cap/x, not x; F_S4 and M_typ are not on the record |

Native-mass rule: C2a/C2b/C3a at M_H and M_a give x = 0.03 to 0.09 or negative. No x-free mass reaches the window.
MUTATE (`B_compare_MUTATE.out`): O(1) swaps (f_c 0.10 -> 0.90, t0 -> 2 t0, zero-g from source mass only) move the
crossing mass M* of a mass-dependent closure by 1.0 to 3.8 dex and every mutant still crosses 5.364 somewhere: a hit at some
mass carries no information. The mass-free C3b mutants (rho_m for rho_b, ell = 3c/H_f) all miss (1.0, 2.1).

**Control N1: slope PASS, onset FAIL (disclosed).** Analytic slope -0.3838/dex vs ledger -0.3834/dex (PASS). The analytic
overflow onset is log M = 13.39 (canonical) and 13.64 (alt) against the ledger's 13.03 / 13.05: beyond the frozen 0.25 dex
tolerance, as anticipated in Part 2. The absolute C2a/C3a numbers are therefore normalisation-uncertain (about 16-20%); the
verdict rests on R0, which depends only on the slope. The ladder-normalised variant (POST-HOC, circular at its calibration
mass) has max/min 26.0 / 26.5, so it fails R0 identically. The script exits 1 for this reason.

**What the record forbids (the logical point).** The ladder arithmetic itself (cap/supply from 4.78 at 1e9 to 0.48 at 1e15,
supply = 5.364 x catchment, canonical) shows x enters a tether-derived relation only at the boundary mass M_OF(x) = 10^13.03.
Below it the tether holds the supply identically; above it the tether holds cap(M) regardless of x and the rest is free
cold energy. So a closure that asks the tether to hold the supply cannot fix x, whether or not overflow feeds cores
(CFG721 says it does not): a pure-tether closure is excluded, and what survives is a trade of x for a reference mass M_ref
or a held fraction q* (the implied F(M) at x = 5.364 is 0 up to 1e13, 0.20 / 0.38 / 0.52 / 0.63 at 10^13.5 / 14 / 14.5 / 15,
canonical ladder; consistent in sign with the record's core excess, but not a derivation). Causal argument A0 applies too.

**POST-HOC observation (noticed after COMPARE; NOT a closure; not counted as a pass).** C3b-R canonical (6.405) is close to
Omega_m/Omega_b = 6.364. Read as "the TOTAL matter column rho_m c/H_L equals the capacity a0/(pi G)" it gives Omega_c/Omega_b =
5.405 (0.63 sigma from 5.364). Algebraically this is Omega_m/Omega_Lambda = kappa sqrt(8/(3 pi)) = 0.4607 for kappa = 1/2,
i.e. a tie between kappa and the matter fraction, not between Omega_c and Omega_b (Omega_b drops out of the relation; it
re-enters only through the final subtraction). Caveats, all from `B_results.json` key `total_matter_reading_POSTHOC`:
R_m = 0.998 with Omega_m = 0.315 but 0.919 with Omega_m = 0.2975 (DESI DR2 BAO-alone value quoted in CFG642's criteria);
R_m = 0.684 in the alt footing (the same reading predicts 8.35, +46 sigma); the identification (total matter, which is not
the tethered cold column) is not what the capacity statement says; it is the CFG642 family (a0/(cH) x density ratio x a
geometric prefactor) with a "+1"; and I tried 30 numbers (p_LE 0.47). It is recorded only so that it is not rediscovered as a
derivation. If one assumed it, it would imply kappa = 0.499 +- 0.016 (Planck-like Omega_m) or 0.460 (DESI-BAO Omega_m):
hand-off to the kappa lane, not a result of this lane.

**What would decide it.** An independent per-halo S/M_src from the finite outer edge r_s = (1+sigma) r_M of isolated-galaxy
lensing profiles (census prediction sigma = x/f_c = 53.6 for f_c = 0.10), and the Nov-Dec 2026 sealed data for the a0 branch.
Neither derives x; both test the identification of the cosmic ratio with the per-halo supply.
