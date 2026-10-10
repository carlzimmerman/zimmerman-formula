# CFG584 FROZEN CRITERIA — does the law's outer residual grow with baryonic mass? (independent confirmation in WALLABY)

(owner chat 10-09, "run the mass trend test"). Committed alone before any slope is computed on WALLABY.

Origin (post hoc, so SPARC is the DISCOVERY sample, not evidence): CFG583 saw a positive mass coefficient
b ≈ +0.06–0.07 dex per dex of M_b in SPARC's outer residual in every cell. Related record: CFG534 SPARC early-type
outer excess +0.071 (survives free M/L, CFG537 B); CFG531 KiDS deficit grows with M*.
CONFIRMATORY sample: WALLABY DR2 kinematic discs exactly as CFG537 Part A built them (87 non-SPARC galaxies,
CFG445 baryon model, Υ_K 0.6, outer band R ≥ 3 R_d, ≥ 2 rings), obtained by executing cfg537_wallaby.py unedited up to
its forecast exit (no CFG537 output files written).
Statistic: OLS slope s of Δ_out on log M_b (equal weights), per footing; bootstrap SE (2000 resamples, seed 584).
 H1 (one-sided): s > 0.
POWER FORECAST (computed and printed BEFORE the WALLABY slope, from SPARC's residual scatter about its own fit and
 WALLABY's log M_b spread): expected Z for s = 0.065. If P(Z ≥ 2) < 0.5 the lane is labelled LOW POWER whatever happens.
Verdict: CONFIRMED iff s > 0 with Z = s/SE ≥ 2 on BOTH footings; CONTRADICTED iff s < 0 with Z ≤ −2 on both;
 NOT CONFIRMED otherwise (with LOW POWER label if the forecast says so).
Reported: the slope with an early-type indicator (T ≤ 3) as a covariate (does mass survive type?); the SPARC slope
 on CFG537's identical Δ_out statistic (discovery sample); f_gas as a covariate.
Controls: C1 the executed CFG537 functions reproduce CFG537's WALLABY outer mean Δ_out (+0.026 / +0.029) to 0.002;
 C2 N ≥ 60 galaxies with a valid outer residual.
MUTATE (CFG584_MUTATE=1): inject +0.10 dex per dex (log M_b − 10) into WALLABY Δ_out; must be CONFIRMED.
κ = ½ fitted; footings never pooled; Υ fixed (a mass-dependent Υ error is the main alternative to a true trend, as
 in CFG537 B); cold energy's mass required; not theory closed.
