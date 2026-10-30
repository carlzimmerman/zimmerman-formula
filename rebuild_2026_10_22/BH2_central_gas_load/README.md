# BH2_central_gas_load: how much central gas would black hole energy need, through gravity alone?

**Verdict as frozen: REACHES LIMIT AT LOAD 0.05 M200.** Criteria cda84a5392. All checks pass. This is an upper-bound test: it gives the load required, it does not show such a load existed.

| Best capped R | L 0.02 | L 0.05 | L 0.10 | LIMIT |
|---|---|---|---|---|
| 10¹⁴ | 0.802 | 0.814 | 0.792 | 0.845 |
| 10¹³ | 0.813 | 0.620 | 0.469 | 0.809 |

R = η/η_STATIC at 10 Gyr, same load. Every cell is in `bh2.out`.

**What it says.**
- BH1's miss was the gas supply. With enough gas at the centre, gravity alone softens these cusps within E_BH. UNCAPPED at L 0.10 gives R 0.481 (4.09 E_BH) and 0.469 (0.89 E_BH).
- Required load: 8.1× the closed box, 5×10¹² M☉ at 10¹⁴ and 5×10¹¹ M☉ at 10¹³, within a_s (15 kpc and 7 kpc), through all 10 Gyr. The 10¹³ miss at L 0.02 is 0.813 vs 0.809, within noise, and 10¹⁴ reaches at L 0.02, so about 0.02 may do.
- In this model's own hot gas, CL5's in-place cap at a_s is 2 M_g(<2.414 a_s) = 0.0047 M200 (derived by hand, not by the grader). The load is 4 to 11 times that.
- CLEAN is reached at 10¹³ (L 0.05) but **not at 10¹⁴** (best capped 0.792, energy cap binds). SH1's pass at R 0.685 is therefore still not supplied. Being at LIMIT corresponds to SH1's KNIFE EDGE region, R 0.817.

**Post-result control, not frozen (`bh2_ramp50.out`).** The 5 Myr ramp means about 20 000 km/s at 10¹⁴, so the eight main reaching and near cells were rerun with CL5's 50 Myr ramp. All are at LIMIT, R within 0.018 of the 5 Myr values (for example 14_L05_N3 0.797, 13_L05_N10 0.602). The ramp does not drive the result. Slower ramps were not tested.

**Limits on the result.**
- The load is not derived and its existence is untested. Whether clusters and groups ever held this much gas within a_s has not been checked against data.
- E_BH is a ceiling with coupling 1; every joule goes into lifting gas. No lower coupling was run on the load grid apart from MUTATE (ε 0.01, no change).
- ICs start in equilibrium at CE1's η with the load in place, so no contraction from the load is charged. A real load built up over time would first deepen the cusp. This favours softening.
- R is measured at x_c about 0.017 R200, targets come from x_c 0.001. Gas is prescribed, spherical, one seed. Inputs PROVISIONAL. Cluster η is ng 48 until A4.
- Nothing here changes SH1's MW and KiDS failures.

κ = ½ FITTED. Canonical and alt share these dynamics; footings are not pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component, never a particle.

Reproduce: `python3 bh2.py setup` (needs BH1's `ics_*`), `python3 bh2.py run NAME` for each of `bh2.py list`, `python3 bh2.py grade`; `bh2_ramp.py` likewise.
