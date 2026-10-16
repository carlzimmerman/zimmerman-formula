# CFG806 FROZEN CRITERIA (DRAFT, not yet committed): scoring U4_27928 against the predictions frozen in CFG571

**Status: DRAFT written 2026-10-15. It becomes frozen only when it is committed alone, before any download.** After that, never edit it;
any change goes in a new dated file. The predictions are CFG571's (commit 259f7825c, `PREDICTIONS_HASH.txt` SHA-256
be27457db6bad870a734c52d2bad92c6669cde53ca7a81553e79154dbedc3714), unchanged. This file freezes only **how the data will be read and
scored**. κ = ½ is fitted, not derived. The cold mass is still required. Nothing here says the data favour the framework.

## 1. Target and data
- **Target:** U4_27928, KMOS3D catalogue z = 1.41933, log M* = 10.74, R_half = 0.49″ (CFG571 inputs, unchanged).
- **Data:** ALMA programme 2024.1.00100.L, CO(2-1), 0.07″, 6.3 h. Public date **2026-11-06** per CFG570's archive metadata (commit
  185251551); **not re-verified with the archive**. If the date slips, nothing below changes.
- **Access:** the cube is downloaded only on the owner's explicit yes, after the file size is stated. Take the archive's imaged cube. If none
  is provided, image the visibilities (CASA `tclean`, Briggs robust 0.5, channel width ≤ 20 km/s) and record that as a **departure**
  (section 8). The cube is deleted after the run and only derived products and their SHA-256 are kept.
- **Cosmology for angular size:** flat ΛCDM, H0 = 70, Ωm = 0.3, as in `cfg571_prereg.py` (angular size only; read-only import of its
  functions). R = 2R_e = 8.3 kpc is the frozen radius of the prediction.

## 2. What was predicted (CFG571; the prediction is conditional on the measured V_c at R = 2R_e)
Required total gas mass, log10 M_gas [M☉], gas disc R_g = R_d | 1.5 R_d. FLOOR means the stars alone already exceed the baryons the model
allows (a detected gas mass then counts against that model, subject to the 0.2 dex stellar-mass systematic).

| V_c [km/s] | footing | F-DESI | F-flat | R-H | L-fb (RAR-equivalent) |
|---|---|---|---|---|---|
| 150–200 | both | FLOOR | FLOOR | FLOOR | FLOOR |
| 225 | canon 9.36e-11 | 9.84 \| 9.95 | 9.75 \| 9.87 | FLOOR | FLOOR |
| 225 | alt 1.13e-10 | 9.46 \| 9.58 | 9.19 \| 9.31 | FLOOR | FLOOR |
| 250 | canon | 10.42 \| 10.54 | 10.40 \| 10.52 | 9.50 \| 9.62 | 9.93 \| 10.05 |
| 250 | alt | 10.34 \| 10.46 | 10.31 \| 10.43 | FLOOR | 9.50 \| 9.61 |
| 275 | canon | 10.69 \| 10.80 | 10.67 \| 10.79 | 10.34 \| 10.46 | 10.45 \| 10.57 |
| 275 | alt | 10.64 \| 10.76 | 10.62 \| 10.74 | 10.19 \| 10.31 | 10.34 \| 10.46 |
| 300 | canon | 10.86 \| 10.98 | 10.85 \| 10.97 | 10.64 \| 10.76 | 10.70 \| 10.82 |
| 300 | alt | 10.83 \| 10.95 | 10.82 \| 10.94 | 10.55 \| 10.67 | 10.64 \| 10.75 |

(Read from `cfg571_prereg_results.json`. The run recomputes exact values at the measured V_c with the CFG571 functions rather than
interpolating this table, which is a lookup guide only. At V_c = 225 the framework's requirement spans 9.19–9.95 across footings and gas
shapes. CFG571's README summary "9.2–9.8" understates the top end; the table governs.)

## 3. Measurements, in order (each gate is checked before the next step is read)
**G1, detection.** The CO(2-1) line is detected if the integrated flux in the moment-0 mask has S/N ≥ 5, with the centroid within 0.5″ of
the KMOS3D position and the line redshift within 0.002 of 1.4193. If G1 fails: report a 3σ upper limit on M_gas (section 3.4) and stop;
there is no kinematic test.

**3.1 Rotation speed.**
- Fit a thin-disc forward model to the cube with V(R) = V_f (2/π) arctan(R/R_t), centre, position angle, systemic velocity and V_f, R_t free.
- **Inclination (never pooled):** primary from the CO moment-0 axis ratio q with intrinsic thickness q0 = 0.2 (cos² i = (q² − q0²)/(1 − q0²));
  branch from the KMOS3D catalogue axis ratio. The branch is chosen before V_c is read, by the rule above, not by outcome.
- **Pressure support (never pooled):** primary P-B, V_c² = V_rot² + 2σ0²(R/R_d) with R_d = R_half/1.678 and σ0 the intrinsic dispersion from the same
  fit; branch P0, no correction. (The same two branches as CFG571's KURVS.)
- **V_c** is the model value at R = 8.3 kpc with its 1σ interval from the fit covariance. **G2:** if V_c is not constrained at R = 8.3 kpc (the
  cube's detected emission does not reach 6 kpc), report "radius not reached" and stop the kinematic test.

**3.2 Stars.** log M* = 10.74, a thin exponential (Freeman) disc, as CFG571. Stellar-mass systematic 0.2 dex, carried as an interval, not a branch.

**3.3 Gas.** M_gas = α_CO L′_CO(1-0). Primary α_CO = 4.36 (including helium) with r21 = 0.77; branch α_CO = 1.0. The total flux is the sum in the
moment-0 mask (≥ 2σ), checked against a circular 2″ aperture (they must agree within 20%, else reported as a flag). The gas-shape branches
are R_g = R_d (primary) and 1.5 R_d, as CFG571. Flux error: random-aperture rms ⊕ a systematic floor of 0.15 dex (α_CO, M*).

**3.4 Non-detection.** M_gas < 3σ upper limit; one-sided Δ_m.

## 4. Scoring (a single disc; a demonstration; no model is excluded)
- **Per model m, per footing, per gas-shape and pressure branch (never pooled):** Δ_m = log M_gas,meas − log M_gas,req,m(V_c), with the interval from
  the gas error and from V_c ± 1σ propagated through the exact CFG571 functions. FLOOR models get no Δ_m; they are reported as FLOOR with the
  stellar-mass interval.
- **TESTS NOTHING:** if the 1σ interval of V_c lies entirely below 200 km/s, every model is FLOOR. Report V_c and the gas mass and nothing else.
- **PARTIAL:** if the 1σ interval of V_c straddles 200 km/s, report Δ_m at both ends and label the result PARTIAL.
- **Reading, frozen in advance:**
  - A measured M_gas inside a model's required range at the measured V_c is **consistent** for that model on this disc.
  - A measured M_gas below a model's required range by more than 2σ_tot is **in tension**; above it by more than 2σ_tot is **in tension**
    (more gas than the model can have). σ_tot = interval from section 3 ⊕ 0.15 dex.
  - A model that is FLOOR at the measured V_c is **in tension** whenever gas is detected (G1 passed), because its stars alone already exceed the baryons it allows. The tension is reduced, and reported as such, if M* is taken 0.2 dex lower.
- **Not allowed:** pooling branches or footings, dropping the disc, choosing the branch after seeing Δ_m, or any exclusion statement.

## 5. Controls (fail = reported and kept; a failed control makes the run NOT DIAGNOSTIC)
- **C1 injection recovery:** inject a rotating disc of known V_c (200, 250 km/s) and known M_gas into off-source noise taken from the real cube (the
  same channels, shifted in position); recover V_c within 15% and the flux within 20%.
- **C2 off-source apertures:** the mean flux of 100 random apertures is consistent with zero and their rms matches the quoted noise within 20%.
- **C3 headers:** rest frequency 230.538 GHz, beam, channel width and the line redshift are consistent with the catalogue.
- **C4 Newtonian round trip:** with ν ≡ 1 the required baryonic velocity equals V_c to < 1e-6 (CFG571's C4, re-run).
- **MUTATE:** shift the velocity axis by +2000 km/s. The line leaves the mask, G1 fails, and the script must detect it (exit 1). The output carries the `_MUTATE` tag.

## 6. Scripts and outputs
`cfg806_u4.py` (with `--mutate`), `cfg806_u4.out`, `cfg806_u4_results.json`. The script imports `cfg571_prereg.py` read-only and contains no model
change.

## 7. Pre-data forecast (committed with the criteria)
The table in section 2 is the forecast. Which row applies depends only on the measured V_c; the run prints the row for the measured V_c.

## 8. Departure rule
Anything added or changed after the first measured number is printed (an imaging choice, a mask, a branch) is listed under "Departures" in
the README, with the reason, as CFG572 did. The comparison rules in sections 4 and 5 may not be changed.

## 9. Not claimed
No a0 measurement. One disc, a demonstration. κ = ½ is fitted; the cold mass is still required; "theory closed" is never said. These are
scoring rules for predictions made before the data, not results.
