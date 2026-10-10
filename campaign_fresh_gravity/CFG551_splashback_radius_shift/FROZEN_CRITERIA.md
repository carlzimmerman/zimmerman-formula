# CFG551 FROZEN CRITERIA: does the R5 drained shell push the inferred splashback radius outward, against published splashback measurements?

Committed alone, 2026-10-10, before any script of this lane exists, before any predicted splashback ratio is computed, and before any published splashback number is compiled from source text.
- **Read before this freeze:** the committed CFG546 record (README, criteria, `cfg546_lib.py`, `cfg546_forecast.py`, `cfg546_predict.py`, the forecast `.out` lines with the apparent r_sp shift, the predict JSON key layout), the CFG504 README and the key layout of `cfg504_calib_results.json` (S0 stacked ξ_hm per mass bin), the CFG544 README (edge softened outward by 25–55% in r_99), THEORY_v1 rule R5, the CFG526/530 profile builder (`Mesh.deposit` is CIC), and the file listing of `_external_data/cfg530_work` (the particle snapshots of the R5 runs exist; a 512³ alt R5 run finished 2026-10-10 04:18, with no profile built).
- **Not read before this freeze:** any published r_sp value, ratio or error bar. What was known going in was only the qualitative statement in the lane brief: galaxy-density r_sp around optically selected clusters came out ~10–20% smaller than ΛCDM simulations, and lensing r_sp was more consistent with ΛCDM.
- No downloads. κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are scored separately and never pooled. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing here may be read as "the data favour the framework".

## The idea
CFG546 found that the R5 engine predicts, around clusters, an excess of effective (lensing) density inside ~0.85 r_ta and a drained shell ~30% deep at 0.85–2 r_ta (512³; ×2.03 from 256³, not converged). By a LINEAR Fisher bias with a constructed DES-Y3-like covariance, a ΛCDM DK14 fit absorbing it would infer r_sp **+26 to +35% larger** than ΛCDM. Published splashback measurements find r_sp equal to or smaller than ΛCDM simulations. This lane (i) recomputes the shift by a full NONLINEAR DK14 fit done the way the observational papers do it, per sample mass and redshift, for lensing (ΔΣ, gravitating density) and for galaxy number density (Σ_g, tracer density), and (ii) confronts it with the published ratios.

## Task 1: the compilation (provisional)
- Sources: abstracts / HTML / arXiv listing text via web search and fetch only. Every number is labelled **PROVISIONAL** unless read from the paper's own text (abstract or body), in which case it is labelled **SOURCE TEXT**. A number from a search-engine summary only is **(U)** and enters no statistic.
- Per measurement record: reference, r_sp (or r_sp / r_200m), method (**L** = weak lensing ΔΣ; **G** = galaxy number density), selection (**SZX** = SZ- or X-ray-selected; **OPT** = optical richness-selected), z, mass (M_200m, converting if needed with colossus diemer19 c), the ΛCDM simulation expectation used, and the ratio data/ΛCDM with its error as quoted (or propagated from r_sp_data and r_sp_sim if only those are given; asymmetric errors kept).
- Classes: **L-SZX** (primary), **L-OPT**, **G-SZX**, **G-OPT** (selection caveat: projection / richness selection biases r_sp low by an amount the papers themselves estimate).
- **Overlap rule (frozen):** within one class, if two measurements use the same cluster catalogue (or one is a subset of the other), only the one with the smaller ratio error enters the class combination; the other is reported.

## Task 2: the frozen prediction
**ΛCDM reference profile per measurement:** the CFG546 DK14 fiducial (`cfg546_lib.fiducial`, imported unedited) at the sample's (M_200m, z): diemer19 c, Gao α, r_t = (1.9 − 0.18ν) r_200m, β 4, γ 6, b_e 1, s_e 1.5, ρ_s normalised to M_200m. Comoving h-units.

**Framework profile:** Δρ_F = Δρ_ΛCDM × [1 + rel(r / r_ta(Δρ_ΛCDM, z))] (A = 1, the CFG546 construction), with
- **L (lensing):** rel = the CFG546 cluster templates of the gravitating density ρ_g (committed JSON, unedited): canonical primary = 512³ canonical; alt primary = 256³ alt × s_res (2.03); pure 256³ canonical / alt reported.
- **G (galaxy density):** rel_p = the same stacking (CFG546 `run()` statistic: S0 centres, S0 r_ta, x bins 0.1 to 4, ratio of stacked means) applied to the **particle density** ρ_p of the R5 run against the S0 particle density. Particles are the tracer (the baryon carriers, M_bret = f_ret F_B ρ_p); the cold energy's source term is not a tracer. ρ_p of the R5 runs is CIC-deposited here from the committed z = 0 snapshots (512³ canonical; 256³ canonical and alt; read-only). Alt primary = 256³ alt × s_res,p (least-squares scale of 512³ onto 256³ canonical over 0.2 ≤ x ≤ 3, the CFG546 construction). The 512³ alt particle template (run finished 2026-10-10) is reported only.
- Template handling as CFG546 (`cfg546_lib.Template`): zero for x < 0.2 and x > 4; lognormal r_ta smoothing σ_ln = 0.2.

**The fit (as the papers do it), noiseless ("Asimov"):**
- Model: DK14, Δρ = ρ_s exp{−(2/α)[(r/r_s)^α − 1]} [1 + (r/r_t)^β]^(−γ/β) + ρ̄_m b_e (r / 5 r_200m)^(−s_e). Free: ln ρ_s, ln r_s, ln α, ln r_t, ln β, ln γ, b_e, s_e. Gaussian priors (More+16 / Baxter+17 / Chang+18 practice): ln α ± 0.6 about the Gao value, ln β ± 0.2 about ln 4, ln γ ± 0.2 about ln 6.
- Observable: **L:** ΔΣ(R) (CFG546 `project`, line of sight ±40 h⁻¹ Mpc); **G:** Σ(R) = 2∫₀⁴⁰ Δρ dl (the projected galaxy surface-density shape; normalisation free through ρ_s, b_e).
- Data vector: 20 log bins over **0.2–10 h⁻¹ Mpc comoving (primary)**; per-bin fractional error **σ_bin = 0.05** (uncorrelated, in ln); residuals in ln.
- Fit by `scipy.optimize.least_squares` from the ΛCDM fiducial, then restarted from 2 perturbed starts (r_t × 1.3, s_e + 0.3; r_t × 0.77, s_e − 0.3); the lowest cost is kept.
- **r_sp** = the radius of the steepest logarithmic slope of ρ̄_m + Δρ_fit (3D), searched over 0.5 ≤ r / r_200m ≤ 3 on a fine grid with parabolic refinement. A minimum on the search boundary is flagged EDGE.
- **Predicted ratio** R_pred = r_sp(fit to framework profile) / r_sp(fit to ΛCDM fiducial profile), same pipeline.
- **Prediction error** σ_pred = |R(rel + σ_rel) − R(rel − σ_rel)| / 2 with σ_rel the committed CFG546 bootstrap error (and the particle template's own bootstrap error, 200 draws).
- **Declared variants (all reported; the verdict rule says which count):** (V1) 256³ templates both footings; (V2) CFG544 kinetic softening: template radial coordinate stretched outward, rel_soft(x) = rel(x / s), s = 1.25 and s = 1.55 (the CFG544 r_99 range; amplitude unchanged, mass not re-balanced, a crude stand-in disclosed as such); (V3) σ_bin 0.02 and 0.10; (V4) range 0.3–30 h⁻¹ Mpc; (V5, lensing only) weights from the CFG546 constructed covariance of a DES-Y3-like stack at the sample's (M, z); (V6, reported) the CFG495 proportional-draw template; (V7, reported) the "sim route": DK14 fitted directly to the CFG546 stacked S0 profile and to S0 × (1 + rel), x 0.2–3.95 r_ta.
- Every R_pred is computed per measurement (its own M_200m, z). Labels: **TEMPLATE MASS EXTRAPOLATED** if M_200m < 10^14 h⁻¹ M_sun (the cluster template is log M_ta ≥ 14.2); **z = 0 TEMPLATE** for z ≥ 0.5 (applied in units of r_ta(z)).

**Comparison statistic (frozen):**
- Per measurement: Z_i = (R_pred − R_obs) / √(σ_obs² + σ_pred²), σ_obs = the quoted error on the side facing the prediction.
- Per class and footing: inverse-variance combination Δ̄ = Σ w_i (R_pred,i − R_obs,i) / Σ w_i, w_i = 1/(σ_obs,i² + σ_pred,i²), Z_class = Δ̄ √(Σ w_i). Independence assumed after the overlap rule (disclosed).
- **Primary statistic:** Z_L-SZX on each footing. L-OPT, G-SZX, G-OPT reported separately; G-OPT carries the selection caveat and never enters a verdict.
- **Separation (data precision):** S = (R_pred,512 − 1) √(Σ w_i) over L-SZX: how many σ the data separate the framework prediction from ΛCDM.

## Verdict (frozen, on L-SZX; per footing, lane verdict needs both footings)
1. **NOT DIAGNOSTIC (no clean data)** if L-SZX is empty after the overlap rule.
2. **EXCLUDED** if Z_L-SZX ≥ 3 with the primary templates on both footings AND with V1 (256³) on both footings AND with V2 (s = 1.25 and 1.55) on both footings.
3. **TENSION (Z)** if Z_L-SZX ≥ 2 with the primary templates on both footings and with V1 on both footings (not EXCLUDED).
4. **NOT DIAGNOSTIC (template non-convergence)** if Z_L-SZX ≥ 2 with the primary templates on both footings but < 2 with V1 on either footing (the TENSION number at 512³ is stated).
5. **NOT DIAGNOSTIC (data precision)** if |Z_L-SZX| < 2 on both footings and S < 2 (the data cannot separate the prediction from ΛCDM at 2σ).
6. **CONSISTENT** if |Z_L-SZX| < 2 on both footings with the primary templates and with V1, and S ≥ 2.
7. Mixed footings → the weaker label of the two.
- **Labels (attached, never replace the verdict):** SELECTION-DOMINATED for the G-OPT class if its mean ratio differs from the G-SZX mean by more than the combined error (the known selection systematic dominates that class); NOT ROBUST if the per-footing verdict changes under V3, V4 or V5; FEW MEASUREMENTS if L-SZX has fewer than 3 entries.
- G-class sets get the same statistic and a reported label by the same rules, but they do not set the lane verdict.

## Task 3: controls and MUTATE
- **K-DEP (gate):** this lane's CIC deposit of the S0 512³ and 256³ particle snapshots reproduces the committed `cfg526_S0_L200_rhop.npy` to max |Δρ| ≤ 1e-4 (float32). Otherwise the G templates are not used.
- **K-S0 (gate), ΛCDM's own ratio from our S0 boxes:** the same DK14 pipeline (3D, σ_bin 0.05, 0.2–10 h⁻¹ Mpc, priors) fitted to the CFG504 S0 512³ stacked profiles ρ̄_m(1 + ξ_hm) of the resolved cluster bins R3 and R4 (boxes a and b) gives r_sp; the ratio to the colossus `more15` steepest-slope expectation at the bin's median M_200m (converted from the stored M_200c with diemer19 c), z = 0, must lie in 0.85–1.15 for every bin. The ratio to the DK14-fiducial r_sp at that mass is reported. (PM softening ~2 cells, r_sp ≈ 4–5 cells: a FAIL is diagnosed, not tuned.)
- **K-ROUTE (reported):** the sim-route ratio (V7) vs the analytic ratio for the 512³ canonical template.
- **MUTATE-0 (gate):** template set to zero → R_pred within 1 ± 0.01 for every measurement and both methods (fit starts from the perturbed points).
- **MUTATE-FULL (gate):** CFG546's own linear-bias calculation (its lib, its D1–D8 extended setups, its constructed covariances, R5_512 both footings) re-run here reproduces the committed `cfg546_forecast_results.json` `rsp_shift_frac` to |Δ| ≤ 0.005 (so +26 to +35% is reproduced). The nonlinear R_pred at the same (M, z) is reported beside it; a difference between linear and nonlinear is a finding, not a failure.
- **MUTATE-SHUF (gate):** the CFG546 shuffled-centre template (`cfg546_predict_MUTATE_results.json`, 512³ canonical clusters) gives |R_pred − 1| ≤ 0.05 for the L method at every measurement.
- Outputs of mutated runs go to `*_MUTATE.*`.

## Caveats stated before any number
- The templates are z = 0 products of 0.39 / 0.78 h⁻¹ Mpc PM meshes; the 512³ shell amplitude is 2.03× the 256³ one; no continuum value exists. CFG546's K3 (512³) found a template-shape systematic in projection.
- The DK14 fiducial stands in for each paper's ΛCDM simulation; papers matched their own simulations to their selection. R_pred is a ratio of two fits through the same pipeline, so the fiducial's absolute r_sp cancels to first order.
- The CFG544 softening is a crude declared stand-in (V2); a real kinetic profile does not exist.
- Asimov fits ignore miscentring, boost, photo-z dilution and the galaxy-selection projection effects the G-OPT papers discuss.
- Every compiled number is provisional until read from the paper's own text.
