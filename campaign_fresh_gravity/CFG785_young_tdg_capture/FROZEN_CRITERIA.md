# CFG785 FROZEN CRITERIA: young tidal dwarfs. How full is their cold-energy halo? (no-capture vs law vs formation clock)

Committed alone, before any script. 2026-10-14. Block CFG780–789. Owner: "yeah do the young tidal dwarf galaxies rigorously".

## Seen before freezing (disclosed)
- CFG441 / CFG7: the six Lelli et al. 2015 young TDGs plus Arp 72c fit Newton (χ² 1.10 for 6; Arp 72c on the Newtonian
  side). The law + EFE gives χ² 34 (Δχ² +33 / +39).
- DF2/DF4 (old debris) lean Newtonian (CFG7 FG001).
- This lane is therefore a rigorous re-reading with systematics, scored against three DECLARED predictions. It is not a
  blind discovery.

## Predictions (fixed before any computation)
- **N (untether-on-unbinding, no capture; THEORY_PUSH B/C):** the debris forms moving through cold energy at rest and cannot
  capture it (no capture channel: CFG744, CFG760–762). f_fill = 0.
- **L (settled law):** f_fill = 1.
- **C (formation clock, CFG763):** f_fill = 1 − exp(−t/τ), where t is each TDG's age and τ ∈ [0.7, 3.5] Gyr. Report both
  ends.

## Model
- V_model² = V_N² + f · (V_law² − V_N²), with V_N² = G M_bar/R_out.
- V_law = the record's EFE column V_EFE1 (primary; nominal host). V_ISO1 (isolated) is reported. Columns V_EFE2/V_ISO2 give
  the alt footing.
- Arp 72c has no host compiled: its isolated law is computed from M_bar and R_out with ν_s.
- Data:
  - `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`: V_circ (pressure-corrected), e_V_circ, M_bar, e_M_bar, R_out.
  - `CFG441_old_tdgs_tidal_origin/data/tierB_arp72c.csv`: the asymmetric error symmetrised to 7.5 km/s (as CFG441 D2).
- Ages t = tmerg_over_torb × t_orb (Lelli columns); Arp 72c 0.32 Gyr.

## Likelihood and systematics
- Per galaxy, a Gaussian in V. The variance is e_V_circ² plus the propagated M_bar error: (∂V_model/∂M_bar · e_M_bar)².
- Joint f_fill is common to all 7, on a grid f ∈ [−0.5, 2], flat prior.
- **Systematics, each as a separate re-fit (reported; the verdict needs every one):**
  - **S1 inclination:** every i shifted by ±10° (V_circ ∝ 1/sin i).
  - **S2 molecular gas:** M_mol × 0.5 and × 2 (X_CO).
  - **S3 pressure support:** V_circ replaced by V_rot (no asymmetric-drift correction) and by V_rot² + 2σ_HI² (full
    isothermal correction).
  - **S4 drop-one:** jackknife over the 7 galaxies.

## Classes (primary: EFE law, canonical)
- **NO CAPTURE SUPPORTED** if the 95% upper limit on f_fill is < 0.25, and f = 1 is excluded at ≥ 3σ, under the primary
  AND every systematic variant.
- **LAW SUPPORTED** if f = 0 is excluded at ≥ 3σ and f = 1 lies inside 2σ.
- **CLOCK** if neither, and the C prediction (at either τ end) lies inside 2σ while f = 0 and f = 1 are outside 2σ.
- Otherwise **NOT DECIDED**.

## Controls
- K1: f = 0 reproduces CFG441/CFG7's Newton χ² for the six (1.095) to 0.02, using V_circ and V_N exactly as above.
- K2: f = 1 with V_EFE1 reproduces the record's law χ² for the six (10.55, most favourable host) to 0.1. If the record's
  10.55 used a different V column, report the mismatch.
- MUTATE (CFG785_MUTATE=1): replace V_circ by V_model(f = 1) exactly. The fit must return f̂ = 1.00 ± 0.02. This proves the
  method can find a full halo.

## Hand estimate
f̂ ≈ 0.0–0.2 with σ ≈ 0.15–0.3; f = 1 excluded at ~3–5σ under the primary. The pressure-support variant (S3) is the risk.
Expected: NO CAPTURE SUPPORTED, or NOT DECIDED if S3 widens the interval.

## Machine
Runs after T1x (tiny). κ fitted; not theory closed. A pass supports a postulate's prediction; it does not derive the
two-population rule.
