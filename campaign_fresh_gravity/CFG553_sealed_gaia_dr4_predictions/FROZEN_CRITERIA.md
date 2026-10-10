# CFG553 FROZEN CRITERIA: sealed (hash-committed) Milky Way predictions for Gaia DR4 (release 2026-12-02)

Written 2026-10-10 and committed alone, before any script for this lane exists and before any CFG553 number is
computed. Gaia DR4 data do not exist yet. Offline only: data already on disk; nothing is downloaded; nice -n 10,
<= 2 threads. κ = ½ is FITTED. Both footings, a0 = 9.36e-11 (canonical) and 1.13e-10 (alt) m/s², are computed and
reported separately and NEVER pooled. Kernel ν(y) = 1/(1 − exp(−√y)) (ν_mono). No EFE. The cold energy's MASS is still
required (no particle species is added). Not theory closed. Nothing here says the data favour the framework.

**Scope and separation from the wide-binary pre-registration.** The Gaia DR4 wide-binary test is already
pre-registered and FROZEN in `prep_2026/gaia_dr4_prep/` (PREREGISTRATION_DR4.md, its amendments and every
`*_HASH.txt`). This lane does NOT touch, amend or re-interpret any of those files and makes no wide-binary or s^TX
prediction. CFG553 is a separate, additional sealed set for five Milky Way observables (P1–P5 below). Like CFG571, the
sealed object is a results JSON whose SHA-256 is written into `PREDICTIONS_HASH.txt` and committed before release.
After the seal, none of CFG553's files are edited; any later change goes into a new, dated file.

## 0. What the record already says (read before freezing; disclosed)

Numbers seen before freezing (they shape the expectations, not the rules): CFG516 (K_z(R0, 1.1) on McMillan17 F0:
PD 90.0 / 94.8, RM-φ 70.3 / 71.6, RM-v 74.1 / 75.5, NFW 75.2, data 66.4 ± 2.2; SPARC edge-on ν_z² PD/RM ×1.60 [1.28–1.87]
HSB at 2 R_d, ×2.36 HSB at R_last, ×3.30–3.55 LSB); CFG532/532b (census V(20 kpc) RM-v 199.5 / 206.6, RM-φ 192.4 / 199.3
km/s; law slope 15–27.5 kpc −0.10 to −0.19; DR4 σ_slope 0.04–0.07 to separate from measured slopes; fitted-NFW on Ou+24
M200 5.7e11, c 18.3); CFG513 (spherical ρ_cold(R0) 0.0064 / 0.0073 M☉ pc⁻³; flat V_c,sph(100 kpc) 169 / 177 km/s for
f_ret 0.18; edge 287 / 261 kpc); CFG574 (outer-disc HI: PD vertical force ≈ 1.7× RM's).

## 1. Models (all on the same baryons; A = 1, nothing fitted for the framework)

Machinery is re-used read-only by execution of committed files, never edited: CFG514's axisymmetric finite-volume
solver and McMillan 2017 baryons; CFG516's `Base`, `build_PD`, `flux_mass`, `Mtab`, `rho_b2`, `rho_b3`; CFG532's `Mix`,
`v_model`, `b1mix`, `slope`, `fit_nfw` and its data loaders.

- **RM-v** (round cold-energy rule, in-plane-speed form): spherical cold energy with M_cold(<r) = r v_law²(r)/G − M_b(<r),
  v_law from the algebraic law on the in-plane Newtonian field (CFG516 §1).
- **RM-φ** (round rule, flux form): spherical cold energy with M_cold(<r) = the QUMOND phantom's Gauss-flux enclosed
  mass (CFG516 §1).
- **Rival PD:** the full QUMOND ν_mono field on the same baryons (the "phantom disc"), at each footing.
- **Rival NFW:** the same baryons (Newtonian) + a spherical NFW (M200, c free) fitted by CFG532's `fit_nfw` to
  **Ou+24 Table 1** (APOGEE DR17 + Gaia DR3; on disk; CFG532's error model stat ⊕ 3% inner / 15% R > 22 kpc). This is
  the "NFW fitted to DR3". It is refitted at every baryon variant. Variant (reported, no verdict): NFW fitted to
  Eilers+19 (CFG514/516 errors). The NFW is footing-independent.
- The census edge (f_ret 0.18; 287 / 261 kpc, CFG513) lies far outside every predicted radius (≤ 60 kpc) and is not
  applied; this is stated, not tested.

## 2. Baryons and the model band (declared now; never fitted)

- **Central:** B1 McMillan17 census (CFG532's stars + gas grid split; stars 5.43 ± 0.57e10).
- **Census band (primary, enters every verdict):** the stars scaled by s ∈ [1 − 0.57/5.43, 1 + 0.57/5.43] =
  [0.89503, 1.10497], gas held. Predictions are tabulated at five s values: s−, (s− + 1)/2, 1, (1 + s+)/2, s+. Between
  them the frozen post-DR4 code interpolates linearly in s.
- **Declared variants (reported as a wider envelope; no verdict input):** B2 L172 shapes 6.0e10, B2b 7.3e10, B3 short
  disc R_d 2.15 (CFG516's definitions).
- **Model coordinates:** Galactocentric R with R0 = 8.122 kpc (the CFG514/516 frame) for every prediction.

## 3. The predictions (each tabulated for RM-v, RM-φ, PD, NFW; both footings; all five s values; variants)

- **P1 vertical force** K_z(R, |z|) = ∂Φ/∂|z|, reported as K_z/(2πG) in M☉ pc⁻², at R = 5, 6, …, 16 kpc and
  |z| = 0.5, 1.1, 2.0 kpc (36 cells). Also the midplane vertical frequency ν_z² = K_z(R, 0.075 kpc)/0.075 kpc (CFG516's
  0.25 h_z convention with the thin disc's h_z = 0.3 kpc) and the ratios PD/RM.
- **P2 rotation curve** V_c(R) in the plane at R = 5, 6, …, 27 kpc (23 points), and the logarithmic slope dlnV/dlnR by
  CFG532's `slope` estimator on an even 0.5-kpc grid with equal fractional weights over 15–22 kpc and 15–27.5 kpc.
- **P3 local quantities at R0** (8.122 kpc, z = 0):
  - the local cold-energy (dark) density: RM = the spherical ρ_cold(r = R0) = (dM_cold/dr)/(4πr²); PD = the phantom
    density in the midplane cell interpolated to (R0, 0) and its spherical shell average; NFW = ρ_NFW(R0). In M☉ pc⁻³
    and GeV cm⁻³ (1 M☉ pc⁻³ = 37.97 GeV cm⁻³, computed from constants in the script);
  - K_z(R0, 1.1)/(2πG) and the true total column Σ(|z| < 1.1 kpc) = ∫ρ_tot dz (baryons + dark), and the dark column alone;
  - the total midplane density ρ_tot(R0, 0) (the Oort limit).
- **P4 vertical velocity dispersion (tracer-model conditional).** Declared tracer model, no knob: an isothermal tracer
  with an exponential vertical density ν(z) ∝ exp(−|z|/h) in the model's own K_z(R, z), vertical Jeans equation with
  the tilt term neglected: σ_z²(R, z = 0) = ∫₀^∞ e^(−z/h) K_z(R, z) dz. Two tracers, both the census model's own discs:
  thin h = 0.30 kpc and thick h = 0.90 kpc, at R = 5, 6, …, 16 kpc. If a DR4 tracer's measured h(R) differs from the
  declared h by more than 15%, the frozen script is re-run with the measured h as an input (not a knob) and only that
  re-run is scored; the sealed numbers then serve as reference.
- **P5 halo-tracer circular speed** V_c at R = 30, 40, 50, 60 kpc (in-plane, = spherical equivalent at these radii to
  < 1%, checked), and the mean over 30–60 kpc. Expected framework band from the record: 175–195 km/s (not a criterion).

## 4. Decision rules (frozen now; applied after DR4 to each prediction separately)

Each verdict is per prediction × footing × rule form (RM-v, RM-φ) × rival (PD, NFW). Footings and forms are never pooled.

**Measurement error budget.** σ_m = the DR4 analysis's statistical error ⊕ its own stated systematic budget. The
systematics in §5 are propagated as stated there.

**Scalar predictions** (P2 slopes, P3 quantities, P5 30–60 kpc mean, and K_z(R0, 1.1)): framework band F = the census
band [min, max over s ∈ [s−, s+]] at that footing and form; rival band R likewise. d(m, B) = 0 if m ∈ B, else the distance
from m to the nearest band edge in units of σ_m.
- **FRAMEWORK-SUPPORTED** (vs that rival): d(m, F) ≤ 2 and d(m, R) ≥ 3.
- **FRAMEWORK-EXCLUDED**: d(m, F) ≥ 3 and d(m, R) ≤ 2.
- **BOTH EXCLUDED** (counts as a framework fail on that prediction): d(m, F) ≥ 3 and d(m, R) ≥ 3.
- **NOT DIAGNOSTIC**: everything else (including both consistent).

**Vector predictions** (P1 36-cell grid, or whatever subset of cells DR4 measures; P2 V_c(R); P4 σ_z(R)): with the
analysis's covariance (if only per-point errors are published: diagonal plus each stated systematic as a fully
correlated rank-1 term), χ²_X(s) for model X with the declared per-point model floor added in quadrature (K_z 5% as
CFG514/516; V_c 2% as CFG514/516; σ_z 5%), minimised over s ∈ [s−, s+] (one s per model per prediction). p_X = χ² survival
at N points. "Consistent" = p ≥ 0.0455 (2σ); "excluded" = p < 0.0027 (3σ). The four labels follow the scalar rule with
"d ≤ 2" → consistent and "d ≥ 3" → excluded. Secondary label (reported, not a verdict): Δχ² = χ²_R,min − χ²_F,min; a
relative preference is named only if |Δχ²| ≥ 9.
- Joint P1 + P2 with one shared s is reported as a secondary.

**Robustness requirements (each must hold or the verdict becomes NOT DIAGNOSTIC, named by cause):**
- R0: the verdict is unchanged when the measured radii are rescaled to the model frame from the analysis's own R0 and
  from R0 ∈ {8.122, 8.178, 8.275, 8.34} kpc (CFG532 S3 convention, R_model = R_meas × 8.122 / R0_used).
- Distance scale: where two or more DR4 analyses of the same observable use independent distance calibrations, each is
  scored separately; the overall verdict is the common verdict, else NOT DIAGNOSTIC (distance-scale dependent).
- Tracer: P1/P4 verdicts must agree between at least two declared tracer populations when available (e.g. thin- vs
  thick-disc or two abundance-selected samples); else NOT DIAGNOSTIC (tracer dependent).

**Required DR4 precision (computed now, sealed).**
- Scalars: σ_req,F = |F_central − nearest edge of R| / 3 (the precision at which a framework-central truth would
  exclude the rival at 3σ); σ_req,R = |R_central − nearest edge of F| / 3 (the reverse). If the framework's central
  lies inside the rival band (or vice versa), the entry is NOT SEPARABLE at census.
- Vectors: the uniform fractional per-point measurement error f such that, for a framework-central truth (s = 1), the
  rival's minimum χ² over its census band (with the model floor added) reaches 9 above zero; "FLOOR-LIMITED" if
  f → 0 still gives < 9. Computed on the declared grid with independent per-point errors (stated assumption).

## 5. Systematics DR4 analyses must report, and how each is propagated

- **R0** (and its error): radii rescaled as in §4; R0 error propagated as a correlated shift of every R.
- **V_sun (U, V, W) and Z_sun:** propagated as a fully correlated fractional normalisation error on V_c (rank-1).
- **Distance scale** (parallax zero point, spectrophotometric calibration): the analysis's stated scale error enters as a
  correlated R stretch; independent calibrations are scored separately (§4).
- **Tracer selection:** population, vertical density profile h(R) (P4), asymmetric-drift and tilt terms (P1, P2).
- **K_z convention:** whether the published quantity is K_z itself, K_z/(2πG), or a true column Σ(|z| < z0); each is
  compared only with the matching sealed column (P1/P3 give K_z/(2πG) and the true column separately).
- **Non-equilibrium** (Gaia snail, Sgr, LMC, north–south asymmetry, warp/flare beyond 12 kpc): only through the
  analysis's own systematic budget; the model is static, axisymmetric and in equilibrium.

## 6. Controls (reported; a failure is disclosed, never dropped)

- **K1:** CFG516's K_z χ² on Bovy & Rix's 43 MAPs (B1 McMillan17, F0; PD, RM-φ, RM-v; both footings) reproduced to
  relative 1e-4 from `cfg516_mw_results.json`.
- **K2:** CFG532's census V(20 kpc) (RM-v, RM-φ; both footings) reproduced to relative 1e-4 from `cfg532_results.json`
  (expected 199.5 / 206.6 and 192.4 / 199.3 km/s), and its 6-point DR4 slope to 1e-4 absolute.
- **K3:** the Mix (stars + gas) K_z equals a single B1 Base's K_z to 0.5% at (R0, 1.1).
- **K4:** CFG532's fitted-NFW χ² on Ou+24 at census reproduced to relative 1e-3.
- **K5:** the Jeans integrator returns σ² = K h exactly (0.1%) for a uniform K_z.
- **K6:** P5 in-plane vs spherical-equivalent V_c agree to < 1% at 30–60 kpc.

## 7. MUTATE (load-bearing; `CFG553_MUTATE=1`, outputs `_MUTATE`, exit 1 = DETECTED)

Swap round ↔ disc: the framework's P1 predictions are replaced by the phantom disc's on the same baryons and footings.
DETECTED iff, for every footing × form: (a) the midplane ratio ν_z²(PD)/ν_z²(RM) at R = 16 kpc lies in CFG516's
×1.6–3.6 range, AND (b) the swapped K_z(R, 1.1) lies outside the RM census band at every R ≥ 8 kpc. If (a) fails but the
ratio is ≥ 1.28 (CFG516's lowest HSB percentile), it is reported as "DETECTED BELOW THE HEADLINE RANGE" and the exit
is 1 only if (b) holds; the Milky Way is an HSB disc and its ratio need not reach SPARC's median.

## 8. Sealing procedure

1. This file is committed alone ("CFG553: FROZEN CRITERIA --").
2. The script `cfg553_predict.py` writes `cfg553_predictions.json` (deterministic: no timestamps or run times inside),
   `cfg553_predict.out`, `PREDICTIONS.md`; the MUTATE writes `_MUTATE` outputs.
3. `PREDICTIONS_HASH.txt` holds `sha256sum cfg553_predictions.json`. Commit "CFG553 SEALED PREDICTIONS:". No push from
   this lane. After this commit the sealed files are never edited.
