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

**Caveats:**
- The exponent on 1+z_f is assumed.
- The zooms stop at z_f and measure c_f there, so a factor for concentration growth after formation has no stated basis.
- A HIT would support the trend, not this reasoning.
