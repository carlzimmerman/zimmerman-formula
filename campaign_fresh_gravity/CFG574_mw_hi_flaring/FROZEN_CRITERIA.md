# CFG574 FROZEN CRITERIA — Milky Way HI flaring: round rule (RM) vs phantom disc (PD)

(owner chat 10-09, "yes do the milky way test"). Committed alone before any script.

Question: CFG516 predicts HI layers 26–89% thicker under the round enclosed-mass rule (RM) than under the full
QUMOND phantom disc (PD), at fixed gas dispersion. Does the measured Milky Way HI flaring prefer either?

Data (fetched from the source TeX, arXiv:0804.4831, Kalberla & Dedes 2008, Sect. on flaring): HI half width at
half maximum h(R) = 0.15 exp((R - R_sun)/9.8) kpc, R_sun = 8.5 kpc, stated as a good approximation to the
observed flaring for 5 ≲ R ≲ 35 kpc (azimuthal average; the disc is warped and lopsided beyond 15 kpc).
No error bars are given; the fit is used as the data curve.

Models (re-using CFG514/516 code by execution, not editing): baryons B1 (McMillan17 = CFG514's rho_baryon);
kernel ν_mono; κ = ½ fitted; both footings 9.36e-11 / 1.13e-10, never pooled; A = 1 (F0).
 RM-φ and RM-v exactly as CFG516; PD = full QUMOND grid field as CFG516.
 PRIMARY gas: the baryon model's HI component is given the OBSERVED flaring thickness (sech² layer with
 HWHM = h(R) above), so gas self-gravity is consistent with the data. VARIANT: McMillan's fixed 85 pc HI layer.
HI layer: isothermal hydrostatic equilibrium in each model's total potential at fixed R,
 ρ(z) ∝ exp(-[Φ(R,z) - Φ(R,0)]/σ²), Φ from integrating K_z; model HWHM read off ρ(z).
 σ is ONE constant per model and footing, fitted (least squares in ln h) over the scoring range.

Scoring range R = 10–30 kpc, 1 kpc steps (21 points).
 Per model: rms_ln = rms of ln(h_model/h_obs) at the fitted σ; R0_model = exponential scale length from a
 straight-line fit of ln h_model vs R over the same range (data: 9.8 kpc).
 A model is CONSISTENT iff rms_ln ≤ 0.15 AND 7.8 ≤ R0_model ≤ 11.8 kpc (±20%).
Verdict per footing: ROUND FAVOURED if both RM-φ and RM-v are consistent and PD is not; PD FAVOURED if PD is
 consistent and neither RM is; NOT DIAGNOSTIC if all are consistent or none is. Overall verdict requires the
 same call on both footings; otherwise SPLIT (reported as such).
Report only (not a gate): fitted σ per model. A value outside 5–15 km/s is flagged IMPLAUSIBLE (band
 recalled, PROVISIONAL); a pass at an implausible σ is reported as such and cannot be called a win.
Controls: C1 grid baryon mass reproduces CFG514's 6.64e10 to 2% with the modified HI layer swapped back;
 C2 Newtonian baryons only (no cold part) must give R0 or rms far outside the band (no-dark-component control);
 C3 the HWHM extractor recovers a known sech² HWHM to 1%.
MUTATE (CFG574_MUTATE=1): RM's cold mass in a q = 0.3 homeoid (CFG516's MUTATE). It must NOT be consistent
 wherever RM-φ is consistent; if RM-φ is not consistent anywhere, the MUTATE must move rms_ln or R0 toward PD.
Disclosed limits: azimuthal-average data; warp and lopsidedness; single-phase isothermal gas; A = 1 only;
 κ fitted; cold energy's mass still required; not theory closed.
