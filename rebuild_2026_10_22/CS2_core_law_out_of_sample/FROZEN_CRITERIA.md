# CS2_core_law_out_of_sample — FROZEN CRITERIA (committed alone, with the assumption ledger, before any script or number)

Written 2026-10-27 at the owner's request: "Grade the CS1 law out of sample: frozen criteria first. Fix q and amplitude
from SPARC + Milky Way only, then predict X-COP, eRASS1 cells, groups, dwarfs, SLUGGS with no refit, both footings."

Standing caveats:
- κ = ½ is FITTED.
- The two footings are scored separately and never pooled.
- Route E: Newtonian gravity on baryons plus cold dark energy halos. Cold dark energy is a gravitating field component,
  never a particle.
- Not "theory closed". Nothing here says the data favour the framework or ΛCDM.

## 0. Law and calibration (once, printed before any other class is computed)

    log Σ₀ [M☉ pc⁻²] = A + q log(σ / 70.5 km/s)

**Calibration data.** CS1's committed per-system Burkert Σ₀ (`CS1_core_surface_density_atlas/cs1_atlas.csv`, 5ec516e163),
two-sided points only:
- SPARC (Υ profiled);
- the Milky Way.

**Fit method.** CS1's M1 maximum-likelihood fit, executed from CS1's source: intrinsic scatter free, σ_logΣ floored at
0.005.

**What is fixed by the calibration.**
- A, q and their errors are fixed once.
- Σ₀ is a₀-free, so A and q are the same for both footings.
- The footings enter only through the grading machinery.

No X-COP, eRASS1, group, dwarf or SLUGGS number is computed before (A, q) are printed.

## 1. Predictions, no refit

Σ_i = 10^A (σ_i/70.5)^q in every class.

The grading machinery is the record's, executed read-only. It is not CS1's per-system fits.

| class | machinery | σ_i | halo normalisation (primary) |
|---|---|---|---|
| eRASS1 cells (X38's 15 keys, both h) | SC1 / OS1 `grade`, Σ scaled through its `age` factor | OS1: √(kT/0.6 m_p), tercile fill | OS1's: r₀ from Mfair at r_ta |
| groups (P4 T3, 63) | GR1 `grade_groups` (P4 estimator) | observed σ | GR1's: EM1 M200 relation |
| SLUGGS centrals (4) | GR1 `sluggs` (CFG528b machinery, JAM-analogue M★) | outer-bin σ_LOS | GR1's: EM1 M200 relation |
| dwarfs (X1's 89) | OS1 / CD1 cap rule with cap = 0.254484 · 2πG Σ_i | OS1: √(g_obs r₁₂/3) | none (the cap is the maximum pull) |
| X-COP (7 with stars; the matched-clumping lane's profiles) | new, below | V_c,HSE(R500)/√2 (CS1) | r₀ such that the Burkert cold mass at R500 equals the measured M_HSE − M_gas − M★ there |

**X-COP grade.**
- Predicted g = G(M_b + M_c,pred)/r² at 0.1, 0.2, 0.3, 0.5 and 0.7 R500, i.e. 35 points.
- Residual Δ = log g_obs − log g_pred.
- If the measured cold mass exceeds the Burkert maximum at R500, r₀ saturates at the peak (counted).

**Native variant (reported, no class).** Every mass rule is replaced by a native core-radius law,
log r₀ = c + p log(σ/70.5):
- fitted by ordinary least squares on the same SPARC + MW CS1 two-sided points, at the same calibration step;
- applied to eRASS1, groups, SLUGGS and X-COP, with no normalisation from any mass;
- eRASS1 halos keep X38's truncation at r_ta.

## 2. Classes per system class (per footing)

The comparator "OS1" is the same machinery at OS1's law, Σ_a₀ (σ/70.5)^q_f with q_f 0.892 / 0.748. It is computed in
this lane; K0 shows it equals the record.

| class | PASS | IMPROVES ON OS1 | FAILS |
|---|---|---|---|
| eRASS1 cells | all 15 keys have \|Z\| ≤ 2 in both h | no key that passes under OS1 fails, and the summed max-h \|Z\| over OS1's failing keys falls by ≥ 50% | otherwise |
| groups | P4 verdict CONSISTENT | not PASS, and \|mean\| ≤ \|mean_OS1\| − 0.020 dex | otherwise |
| SLUGGS | CFG528's `closes` | not PASS, \|mean\| ≤ 0.5 \|mean_OS1\|, and no reversal | otherwise |
| dwarfs | OS1's CONSISTENT (< 5% with z ≥ 2 and median S ≤ 1) | not PASS, and the fraction with z ≥ 2 falls by ≥ 50% from OS1's | otherwise |
| X-COP | \|mean Δ\| ≤ 0.05 dex and rms Δ ≤ 0.10 dex | not PASS, and \|mean Δ\| ≤ 0.5 \|mean Δ_OS1\| | otherwise |

**Figure of merit (FOM) per class, for the lane class:**

| class | FOM |
|---|---|
| eRASS1 | number of failing keys, then the summed failing \|Z\| as tie-break |
| groups | \|mean\| |
| SLUGGS | \|mean\| |
| dwarfs | fraction with z ≥ 2 |
| X-COP | \|mean Δ\| |

CS2 is **better** than OS1 in a class if its FOM ≤ 0.8 × OS1's (for eRASS1: fewer failing keys, or equal keys and
summed |Z| ≤ 0.8×). It is **worse** if its FOM ≥ 1.25 × OS1's (for eRASS1: more failing keys, or equal keys and
summed |Z| ≥ 1.25×).

**Lane class (per footing; the verdict needs both footings to agree, else UNDECIDED):**

| lane class | rule |
|---|---|
| CS2 PREDICTS ALL | all 5 classes PASS |
| CS2 BETTER THAN OS1 | not all PASS; better in ≥ 1 class and worse in none |
| CS2 TRADES | better in ≥ 1 class and worse in ≥ 1 |
| CS2 NO BETTER | better in none |

## 3. Checks

- **K0** At (A, q) = (log₁₀ Σ_a₀[foot], q_f[foot]) the machinery reproduces the record:
  - OS1's 15 eRASS1 cell predictions, both h, to 1e-6;
  - OS1's dwarf fraction and median S, to 1e-9;
  - GR1's group mean and Z, to 1e-9;
  - GR1's SLUGGS per-galaxy offsets, to 1e-9.
- **K0b** The GR1 namespace's own K0 checks (SPARC = X38 / OS1, groups = X40b, SLUGGS = CFG528b) all pass inside this
  run.
- **K1** The calibration reproduces CS1's inputs: 166 calibration points (165 SPARC + MW), and CS1's code is executed
  unchanged.
- **K2** The X-COP rows equal the matched-clumping lane's `targets.csv` g_obs to relative 1e-6.
- **K3** Peak RSS < 1 GB, one thread.

**MUTATE** (`CS2_MUTATE=1`, separate `_MUTATE` outputs):
- σ is permuted across the 166 calibration systems (seed 20261027), then recalibrated.
- The tooth **bites** if the recalibrated q is within 2σ of 0. Exit 1, as frozen.
- Reported in MUTATE: groups, dwarfs and X-COP graded at the mutated law.

## 4. Disclosed before freezing

- CS1 found SPARC alone gives q = 0.882 (s_int 0.249), and the MW sits +0.26 dex above the all-class law. So the
  calibrated q is expected near 0.85–0.9, with A near OS1's canonical amplitude plus ~0.1–0.2 dex.
- The groups' and SLUGGS' outcomes under OS1 are known: groups PASS (Z +1.94 / +1.85) and SLUGGS FAILS (+0.127). The
  eRASS1 cells under OS1 are 14/15, with INNER M-all over-predicted.
- No CS1 X-COP or eRASS1 Σ₀ enters the calibration or the grades.
