# X64_oblique_object_keys: no combined object variable separates the retaining classes from L* galaxies; on every candidate L* sits between the dwarfs and the clusters

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (ea43d24f22, committed alone; X63 id was taken, so X64).
`AMENDMENT_A1.md` covers implementation fixes in the step-0 and K3 check code only, made after the first run. κ = ½
FITTED. Footings never pooled. Cold dark energy is not matter. Environment variables are out of scope here; the peer
lane X62_environment_keyed_switch tests them. Not "theory closed". Nothing here says the data favour the framework.
Every number is in `x64_oblique_keys.out`, `_results.json` or `x64_classes.csv`.

**Question.** X58_object_keyed_switch needs a non-monotone pattern:
- dwarfs RETAIN (MW ultra-faints, bright M31, M31 others);
- L* galaxies are EXCLUDED (KiDS lenses, SPARC large, MW disc);
- groups and clusters T1–T3 RETAIN.

Does one oblique variable separate these, using X19's classes plus a KiDS lens class?

## Verdict (frozen): **NO OBLIQUE KEY**, on both footings

No candidate separates under the primary labelling, on either footing. The reported variants agree: strict or wide
labels, strict min–max intervals, host-inclusive Φ, lens radius fixed at 0.104 Mpc, and EM1 dwarf M200 all give none.

**The test had power.** Under exact enumeration, 2.5 % of the 120 random relabellings are separated by at least one
candidate (p_any = 0.0250 canonical, 0.0250 alt). The true labels are not among them.

## Per-candidate results (labelling P, 16–84 %, internal Φ)

Values are log₁₀ class medians on the canonical footing. Alt medians differ by at most 0.16 dex (largest on C4/C4L, through a₀); see the `.out`. "Overlap" is how far the
two groups' intervals cross, in dex (the gap would be negative), in the best direction.

| candidate (key type) | dwarfs (UFD / bright M31 / M31 oth.) | L* (SPARC large / MW / lenses) | groups / clusters T1–T3 | overlap canonical / alt | offenders at best threshold |
|---|---|---|---|---|---|
| C1 Q_b = ρ_b/σ³ (K1) | −4.4 / −5.7 / −4.8 | −9.2 / −8.2 / −11.1 | −12.8 / −13.3…−13.0 | 5.58 / 5.58 | all three L* |
| C1d Q_dyn (K1) | −2.3 / −4.0 / −2.9 | −8.4 / −7.8 / −9.9 | −11.4 / −11.9…−12.1 | 4.53 / 4.53 | all three L* |
| C2 σ²/\|Φ_int\| (K3) | +1.53 / +0.82 / +1.38 | +0.31 / −0.13 / +0.73 | +0.65 / +0.36, +0.08, −0.10 | 1.41 / 1.45 | all three L* |
| C3a t_cross/t_H (K2) | −2.8 / −2.3 / −2.7 | −1.8 / −2.45 / −1.2 | −0.6 / −1.1…−1.2 | 2.30 / 2.28 | all three L* |
| C3b t_relax/t_H (K1) | −0.45 / +1.7 / +0.25 | +6.6 / +6.4 / +7.6 | +9.1 / +9.6…+10.3 | 9.25 / 9.23 | all three L* |
| C4L (1/ν)Σ_b/Σ_a₀ = f(x) (K3) | −4.4 / −3.4 / −3.7 | −1.4 / +0.24 / −2.7 | −3.7 / −2.4…−1.4 | 2.95 / 2.95 | SPARC large, lenses |
| C5 dynamical age (K2) | +2.65 / +2.18 / +2.60 | +1.59 / +2.20 / +0.98 | +0.30 / +0.72…+0.78 | 2.15 / 2.15 | all three L* |
| C6 v_esc/v_c at r_a₀ (K3) | −0.70 / −0.54 / −0.59 | −0.23 / +0.09 / −0.46 | −0.60 / −0.15…−0.03 | **0.685 / 0.685** (closest) | SPARC large, lenses |
| C4 f_b Σ_b/Σ_a₀ (reported only, by construction) | −5.2 / −3.6 / −4.2 | −1.35 / +0.19 / −2.7 | −3.9 / −2.75…−1.8 | 2.54 / 2.58 | clusters T3, lenses |

Per-candidate chance rates p_k: 0.008 (Q_b), 0.017 (Q_dyn), 0 (σ²/Φ), 0 (t_cross), 0.008 (t_relax), 0 (C4L), 0
(age), 0.008 (C6), on both footings.

## Physical reading

1. **All the candidates are scale-ordered, so L* sits in the middle.**
   - Phase-space density, relaxation time, crossing time and dynamical age all run monotonically from dwarfs, through L*
     galaxies, to groups and clusters.
   - That is the same mass ordering X58 already excluded, seen through σ and r.
   - On these variables the three L* classes fall between the two retaining ends. That is why the offenders at the
     best threshold are "all three L*".
2. **The bound-region keys come closest, but they are not clean.**
   - C6 (v_esc/v_c at the a₀ radius) and C2 (σ²/|Φ|) are not monotone in mass.
   - On C6 the dwarfs (−0.54 to −0.70) and groups (−0.60) sit low and the clusters high (−0.03 to −0.15). The KiDS lenses
     (−0.46, range −0.68 to −0.27) fall among the dwarfs and groups, and SPARC large (−0.23) falls near the clusters.
   - So the overlap is still 0.685 dex.
3. **C4 does not help either.** f_b·Σ_b is reported only, because f_b is built from the observed dynamics that define
   the need. Even so it does not separate: clusters T3 and the lenses cross. Its E-free form C4L is a function of x
   alone, and x already fails (X19).
4. **The radius convention is not driving this.** Fixing the lens radius at 0.104 Mpc, or using min–max intervals,
   changes nothing.

**Step 4 (R1 / early capture) was not run.** No candidate separates, so there is no key to propagate (frozen).

## Step 0 and checks (7/7)

- **K0.** X19 executed read-only. It reproduces all 1596 cells of `x19_classes.csv` and X19's "NO LOW-DIMENSIONAL
  SELECTOR" with every per-variable status. This passes after A1's parser fixes.
- **K1.** Radius reconstruction: x round trip 6.7e-16; MW r = 8.122 kpc; clusters r = 548 kpc.
- **K2.** The label oracle separates on both footings.
- **K3.** Unit tests: margin 1.00; perfect-order p = 2/15.
- **K4.**
  - Lens lgM200 from EM1's R1 relation: 11.34 / 11.72 / 11.90 / 12.05, against X53's 11.35 / 11.72 / 11.90 / 12.05.
  - EPS z_f(10¹²) = 0.944, matching X59.
- **KL.** The labels used match §1 of the criteria.
- **K5.** 0.21 GB.

**MUTATE** (`X64_MUTATE=1`; labels UFD ↔ SPARC large and T3 ↔ lenses swapped): KL and K2 FAIL as required. Exit 1.

## What is left

Every single oblique object variable built from catalogue quantities now fails, as do all single and axis-aligned
variables (X19). Either the key is not an object property, or it needs the variables this lane left out:
- environment, in the peer lane X62_environment_keyed_switch;
- the retarded or nonlocal history, beyond a crossing-count proxy (X57's K2, left unbuilt as an action).
