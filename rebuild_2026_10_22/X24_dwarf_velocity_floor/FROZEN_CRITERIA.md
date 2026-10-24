# X24_dwarf_velocity_floor — FROZEN CRITERIA (committed alone, before any script; POST-HOC on disclosed data, see §6)

**Question.** (a) Is the hosted-dwarf extra over the isolated law (X19's blocking classes) a property of being hosted, or
of low stellar mass? (b) Does one velocity floor c₀ fix all of it, with c₀ calibrated on isolated LG field dwarfs only and
then predicting the hosted dwarfs out of sample? The floor is σ² = σ_iso² + c₀².

Standing rules: κ = ½ FITTED. Footings canonical / alt, never pooled. No DM particle (c₀ is read as the cold-energy
medium's velocity floor; the mechanism is not derived here). One new constant c₀, calibrated on a class that is NOT
graded. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Data (read-only)

X1 `x1_per_system.csv` per footing:
- E = `Delta[iso AQUAL L*0]`, s = its sdMC (B_iso).
- E-W estimator, so E = log₁₀(σ_c²/σ_iso²), with σ_c the binary-corrected σ (X1's rule).
- Classes: `LG field` (13, calibration only); `MW ultra-faint` (31), `bright M31` (25), `M31 others` (5) (graded, H);
  `MW classical` (8, graded, reported class).
- Crater II, Antlia II, CVn I, Sagittarius, and the M31 dEs are reported individually.
- σ_iso = σ_c · 10^(−E/2), where σ_c = `sigma` × b and b is X1's binary ratio (free-f where matched; the median ratio for
  unmatched M_V > −7.7; else 1).

## 2. Test A — host or mass (verdict-bearing for question (a))

- Overlap window: log M★ ∈ [5.4, 6.8], the field class's low-mass range.
- Compare median E of the hosted systems (H ∪ MW classical) inside the window with the field systems inside it.
- Report the difference D, its bootstrap sd (10 000, seed 20261024, E_i ~ N(E_i, s_i)), and Z_D.
- Also: Spearman ρ(E, log M★) for the field class alone (13), with a permutation p (20 000).
- **HOST-DRIVEN** if Z_D ≥ 2 on both footings.
- **MASS-DRIVEN** if |Z_D| < 1 on both footings AND the field ρ < 0 with p < 0.05 on both.
- Otherwise **MIXED**.

## 3. Test B — one velocity floor (verdict-bearing for question (b))

- Model: E_pred = log₁₀(1 + c₀²/σ_iso²).
- c₀ per footing = the minimiser of Σ_field ((E − E_pred)/s)² over the 13 field dwarfs (bounded scalar search, 0–20 km/s),
  with its 68 % profile interval (Δχ² = 1).
- Graded, out of sample, per class of H and MW classical: median residual R = E − E_pred, bootstrap sd, Z_R; and
  χ²/N (floor) vs χ²/N (law, c₀ = 0).
- **FLOOR REPRODUCES THE DWARFS** if |Z_R| < 2 for all three H classes on both footings AND χ²_floor < χ²_law on H.
- **FLOOR PARTIAL** if χ²_floor < χ²_law on H but some H class has |Z_R| ≥ 2.
- **FLOOR FAILS** otherwise.
- Reported, no weight:
  - the floor's effect on TDGs, DF2/DF4, Crater II and Antlia II (it can only raise E_pred; their E is ≤ 0);
  - its effect on SPARC, where V ≫ c₀ gives ΔE ≈ c₀²/(V²/2) / ln 10 at the median V;
  - the floor fitted on H instead (in-sample, as a consistency read).

## 4. Checks (all must pass; `--mutate` must fail K0)

- **K0:** plain medians of E per H class equal X19's printed values (+0.596 / +0.220 / +0.777 canonical; +0.539 / +0.185 /
  +0.697 alt) to 0.005. The field class has N = 13.
- **K1:** σ_iso round trip: E recomputed from σ_c and σ_iso to 1e-12.
- **K2:** positive control. Synthetic E from the model at c₀ = 4 km/s plus N(0, s) noise; the calibration recovers c₀
  within its interval.
- **K3:** peak RSS < 1 GB.
- **MUTATE:** E taken from the AQUAL + EFE column; K0 must fail.

## 5. What a pass would and would not mean

A pass means the dwarf rows need one velocity floor, not a host selector, and X19's hosted classes stop being an
argument for a host-keyed mechanism. It would not derive c₀, would not touch clusters, growth or the MW disc, and would
leave the below-law rows (TDGs, DF2/DF4, Crater II) unexplained, with possibly worse agreement there.

## 6. Disclosure (post-hoc)

Before freezing, the per-system E, log M★ and HI of the 13 field dwarfs and the 8 MW classical dSphs were printed in this
session. The hosted class medians are known from X19. The calibration is on the field class, so c₀ is not tuned to the
graded classes, but the idea came from looking at these numbers. Treat any pass as a lead, not a confirmation; the
independent confirmation is new dwarf kinematics.
