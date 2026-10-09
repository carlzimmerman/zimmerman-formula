# CFG572: GS4_24110's gas mass from PUBLIC data, tested against CFG571's frozen prediction

Criteria 9c60f25ad (committed alone, before any download). Predictions frozen earlier in CFG571 (259f7825c). GS4_24110 is ASPECS 1mm.C10. Run: `python3 cfg572_gas.py` (and `--mutate`, `--mutate1000`); chart: `python3 chart_cfg572.py` → `cfg572_gs4_24110_chart.png`.

## What was measured
| route | result | log M_gas |
|---|---|---|
| CO(4-3), public 2019.1.01528.S (2.2″ beam) | **0.621 ± 0.036 Jy km/s, 17σ** | 10.95 (r41 0.37); 10.78–11.12 for r41 0.55–0.25 |
| [CI](1-0), public 2019.1.01528.S (1.8″ beam) | 0.044 ± 0.039 Jy km/s, **not detected** | < 10.28 (X_CI 1.9e-5) / < 10.08 (3.0e-5), 3σ |
| dust, Boogaard+2020 L850 (literature) | 32.1e29 erg/s/Hz | 10.51 (α_CO 4.36) / 10.68 (Scoville 6.5), ± 0.2 |

**The gas tracers disagree by ~0.7 dex.** The CO(4-3) value sits above the [CI] limit, so either r41 is high (high excitation at z ≈ 2) or X_CI is higher than assumed. The dust value sits between the two. The gas amount is the weak link.

## Against the frozen predictions (Δ_v at R_e, canon footing; ± is 1σ)
| | dust gas, M★ 10.89 | dust gas, M★ 10.76 | CO(4-3) gas, M★ 10.89 |
|---|---|---|---|
| framework, a0 ∝ √ρ_DE | +0.11 ± 0.09, consistent | +0.03 ± 0.10, consistent | +0.30 ± 0.12, tension |
| framework, flat a0 | +0.13 ± 0.09, consistent | +0.05 ± 0.10, consistent | +0.32 ± 0.12, tension |
| a0 ∝ H(z) | **+0.37 ± 0.09, tension** | **+0.28 ± 0.10, tension** | +0.55 ± 0.12, tension |
| ΛCDM+fb RAR-equivalent | **+0.35 ± 0.09, tension** | **+0.26 ± 0.10, tension** | +0.53 ± 0.12, tension |
| Newton, no dark matter (reference) | −0.03 | −0.08 | +0.16 |

The alt footing gives the same pattern (+0.03 to +0.06 higher). Post-freeze branch, reported only: with Boogaard's M★ 10^11.1, every model is in tension on every route.

## What it means (one galaxy, a demonstration; no model is excluded)
- **Inside R_e, GS4_24110 is baryon-dominated:** stars plus dust-route gas account for about the whole rotation. That leaves almost no room for a boost.
- **The rivals' tension comes mostly from the stars.** For a0 ∝ H(z) and the ΛCDM-feedback RAR-equivalent scale, the stars alone already exceed what's allowed (CFG571 FLOOR), so the tension rests on M★, whose systematics are ~0.2 dex. The [CI] limit and the dust route agree.
- **The framework fits with the dust gas and the frozen stellar masses.** It doesn't fit with the CO(4-3) gas or with M★ 11.1. With those inputs, even plain Newton has too many baryons, which points to the inputs (conversion factors, M★, the pressure-corrected V_c) and not to any model.
- **ΛCDM itself is NOT tested.** A baryon-dominated inner disc at z ≈ 2 is allowed in ΛCDM (Genzel+2017-type discs). Only the RAR-equivalent scale from CFG565 is.
- Nothing here says the data favour the framework over ΛCDM.

## Controls
- C1 injection recovery: 0.90 ([CI]) and 0.83 (CO(4-3)), within 20%: PASS.
- C2 off-source apertures: PASS.
- C3 headers: PASS.
- **MUTATE (+2000 km/s):** CO(4-3) drops to −0.7σ → detected (exit 1). The [CI] window leaves the cube's band at +2000 km/s; the line isn't detected anyway.
- **Disclosed extra (`--mutate1000`):** also detected.
- **Departures:**
  - the Δ_v block, the Newtonian reference and Boogaard's M★ 11.1 branch were added to the script after the first gas numbers were printed (the comparison rules themselves are as frozen);
  - the MUTATE out-of-band guard was added after the first MUTATE crashed.
- **The CO(4-3) ring apertures are all negative** (−0.10 to 0.00). The noise may be underestimated, but 17σ survives any plausible inflation.

## Data
The cubes (2.3 GB, public product tars of MOUS uid://A001/X1465/X99e and X99a) were downloaded with the owner's yes and deleted after the run. Extracted spectra are in the results JSON. Boogaard+2020 TeX source: `data_assembly/gs4_24110_lit/`.

κ = ½ fitted; the cold mass is still required.
