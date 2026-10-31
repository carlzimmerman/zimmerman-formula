# X80_low_mass_floor_emergence (QUEUED, BEFORE A5; criteria c1c6d82d69, AMENDMENT_A1)

**Question.** Does native collapse put cores on a₀/2πG at dwarf masses? If so, the floor of the route E core rule would
emerge rather than being put in by hand.

**Status.**
- **Owner's decision 10-30: X80 runs before A5** (`AMENDMENT_A1.md`). The 10¹⁰ / 10¹¹ zooms start when X74's post-A4 watcher logs
  "post-A4 regrades done". `watch_A4_then_X80_then_A5.sh` runs under nohup and checks every 10 min; its log is `watch_X80.log`. After
  "X80 done" it hands over to X48's A5 watcher. If the machine restarts or the run is preempted, re-run that script; it resumes.
- **Footprint:** 18 runs at ng 64 (about 2 GB each, from A4) and 6 at ng 48, all concurrent, about 42 GB, on 16 cores.
- The script is pre-built. **K1 PASS:** on the committed 10¹² ng 64 halos it reproduces X77's η 20.83 and gives
  ρ₀r₀ = 134.9 M☉/pc², which is R = 1.26 canonical / 1.05 alt.
- **Setup smoke:** ng 32 for 3 steps, in scratch only. z_f is 1.326 at 10¹⁰ and 1.137 at 10¹¹; the latter matches X43's
  table.

**Files:**
- `x80_floor.py`: X77's fit, executed from X77's source; outputs `x80_results.json` and `_MUTATE`.
- `run_low_mass.sh`: 24 preemptible runs.
- `watch_A4_then_X80_then_A5.sh`: the live watcher. `watch_A5_then_X80.sh`: superseded, kept for the record.
- `x80_converged.py`: AMENDMENT_A1's converged η and NF1's window. Its check on the committed 10¹² ng 64 runs gives 25.937 (K PASS); no low-mass number exists yet.
- `../NF1_no_floor_rule/nf1_native_read.py`: AMENDMENT_A1's native read of the no-floor rule. Its check, ρ₁₀ = ρ₁₁ = 1, reproduces NF1's N0, |d| 0.

**Caveats.**
- The zooms are Newtonian, with no a₀ in the dynamics.
- Emergence would be a native coincidence of scales, not a derivation.
- κ = ½ FITTED; not theory closed.

## Outside prediction to score (added 2026-10-30, before any low-mass number; reported, not graded)

Relayed by the owner from an external model. It does not change `FROZEN_CRITERIA.md`.

**Formula:** ρ₀r₀(M) = ρ₀r₀(10¹²) × [Σ_coll(M)/Σ_coll(10¹²)] × [(1+z_f(M))/(1+z_f(10¹²))]^(5/4), which assumes c_f ∝ 1+z_f.
Inputs: 134.9 M☉/pc² at 10¹²; z_f = 0.944 / 1.137 / 1.326; Σ_coll from X43's table, log-extrapolated to 10¹⁰ (X53).

| Mass (M☉) | c_f | ρ₀r₀ (M☉/pc²) | R canonical | R alt |
|---|---|---|---|---|
| 10¹¹ | 7.4 | 85 | 0.80 | 0.66 |
| 10¹⁰ | 8.1 | 53 | 0.50 | 0.41 |

**Scoring:** a HIT at a mass if the measured ρ₀r₀ lies within ±15 % of the formula, and separately for c_f-equivalent. These
are the formula's values, not the source's table, whose ρ₀r₀ column (96–101 and 68–76) used a fixed −0.125 dex per decade.

**Same formula as a converged-η ratio (Argon, relayed by the owner 10-30, before any low-mass number; reported, not graded):** ρ₁₁ = (2.137/1.944)^(5/4) = 1.126; ρ₁₀ = 1.251 at the setup smoke's z_f 1.326 (Argon used 1.330, which gives 1.254). HIT at a mass if the measured ratio lies within ±15 %. Argon's ρ₀r₀(10¹⁰) ≈ 70 M☉/pc² is total matter; the cold share SPARC grades is 59.

**Caveats:**
- The exponent on 1+z_f is assumed.
- The zooms stop at z_f and measure c_f there, so a factor for concentration growth after formation has no stated basis.
- A HIT would support the trend, not this reasoning.

## What-ifs at stated ratios (, 10-30; no low-mass zoom exists, so none of this is a measurement)

| ρ₁₀, ρ₁₁ | Υ (A/B) | rms (A/B) | SPARC line | S at V_flat 20–60 / 60–100 / 100–150 (ET1 69, 103, 143) | Υ in those bins |
|---|---|---|---|---|---|
| 1, 1 (NF1's N0) | 0.71 / 0.73 | 0.0678 / 0.0688 | pass | 47 / 69 / 94 | 1.20 / 1.10 / 0.84 |
| 1.1, 1.049 | 0.67 / 0.68 | 0.0672 / 0.0683 | pass | 52 / 73 / 98 | 1.20 / 1.03 / 0.81 |
| **1.254, 1.126 (Argon's)** | **0.62 / 0.63** | **0.0669 / 0.0679** | **pass** | 59 / 80 / 104 | 0.97 / 0.86 / 0.76 |
| 1.9, 1.378 | 0.49 / 0.51 | 0.0682 / 0.0693 | **fail, Υ 0.49 on A** | 88 / 105 / 122 | 0.30 / 0.48 / 0.61 |

So the upper cut of 1.9 sits right on the line's edge. The lower cut of 1.1 is not a line failure: the line passes down to ρ = 1. "N SHORT" means S falls below ET1 and ET2's intervals, with Υ above 1 in the smallest galaxies. It doesn't mean a floor is required.

## Can the converged η be tested with a smaller softening? Not at this N (, ; 10¹² only)
η_conv assumes each halo's NFW continues inside r_conv. On the committed ng 64 snapshots, recomputing r_conv with ε/2 or ε/4 moves the median x_c only from 0.0321 to 0.0296, because the relaxation limit sits just below 3ε. The expected rise in η is 3.4 %, against the 20 % between the cut and the converged value. A5 keeps ε and doesn't reach it either. A direct test needs far more particles than direct summation here allows. This is a rough estimate, since the snapshots evolved at ε. So the converged reads rest on that assumption, and the extrapolation is not closed.

