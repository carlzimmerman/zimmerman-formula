# CFG220 — FROZEN CRITERIA: the CRISTAL outer-radius decomposition on the INDEPENDENT baryon route (class A only), and the calibration that would reverse it

Written 2026-09-30 and committed BEFORE the independent-route numbers are computed. **κ = ½ is FITTED, not derived.** Both footings (9.36e-11 / 1.131e-10) and both kernels are carried. Author decompositions, not a direct a₀ measurement. Nothing here says the data favour a framework. What is already known and is NOT blind: CFG213's fit-route outer-radius block (12 discs: rival −0.283 [−0.350, −0.109] DISFAVOURED-under, flat +0.019 [−0.037, +0.225] at the table's R_out; −0.258 / +0.023 at the outermost marker) and its R_e route swap (both laws CONSISTENT). What is new and unread: the independent route at the outer radius on the six detections.

## Why
CFG219 (criteria e62ce4cff, lane b6d76ddb4) forecast that the radius reached separates the laws far better than R_e, and that a shared gas-calibration systematic is what limits the test. CFG213's outer-radius numbers use the authors' fitted M_bary (a 1-dex-wide Gaussian prior, fitted jointly with the halo), so they do not answer the independent-route question.

## Sample and inputs (all on disk)
- **S6 = CRISTAL-02, -03, -07a, -11, -19, -20**: the six with an SED M★ and a dust-DETECTED gas mass (data chat, 2ad335eea; the CRISTAL paper's f_molgas note lists 08, 12, 15, 23b as upper limits). **08, 12, 23b** (upper limits) enter only as one-sided bounds. 09 and 15 stay excluded as frozen in CFG213; 06b, 10a-E, 23c lack an M★ or a gas mass.
- From `data_assembly/arxiv_tables/cristal_vector/cristal_outer_summary.csv`, for `radius_definition` ∈ {`table_Rout`, `outermost_data_marker`}: R, V_bary, V_tot (model curves with the authors' pressure correction, extrapolated beyond the last marker). From the tables: z (z_cii), log M★, f_molgas, and M_fit = 10^logMtot (the fit's baryonic mass, as CFG213's route).

## Quantities
g_obs = V_tot²/R; g_bar,fit = V_bary²/R; route factor ρ = M_ind/M_fit with M_ind = M★/(1 − f_molgas); **g_bar,ind = ρ · g_bar,fit** (the baryon-curve shape is the fit's, only its normalisation changes); D_ind = g_obs/g_bar,ind; δ_L = log₁₀[ D_ind / ν(g_bar,ind / a₀,L(z)) ] with L ∈ {flat: a₀, rival: a₀ E(z), Ω_m 0.315}. Kernels **ν_mono** (primary) and P2; footings **canonical** (primary) and alt. The fit route on the same six discs is reported beside (ρ = 1).

## Statistic and verdict
Median δ over the six discs with a 95% galaxy-bootstrap CI (10,000 resamples, seed 220); verdict CONSISTENT / DISFAVOURED-over / DISFAVOURED-under as CFG213.
**Outcome class per cell:** FLAT-SUPPORTED (flat CONSISTENT and rival DISFAVOURED-under), RIVAL-SUPPORTED (rival CONSISTENT and flat DISFAVOURED-over), BOTH-CONSISTENT, BOTH-DISFAVOURED, OTHER. **Headline = the class at table_Rout, ν_mono, canonical, α as tabulated.** It is ROBUST if the class is identical in all eight cells (2 kernels × 2 footings × 2 radius definitions), else KERNEL/FOOTING/RADIUS-DEPENDENT. It is LOO-ROBUST if the headline class survives dropping any one disc.

## Calibration flip
A uniform gas-mass offset τ (dex) on all six detections: M_ind(τ) = M★ + M_gas 10^τ with M_gas = M★ f/(1 − f). For each law: **τ\*_L** = the τ at which the law's median δ is 0 (solved); **τ_flip** = the smallest |τ| at which the headline CLASS changes (the CI edge crossing 0 or a verdict changing), scanned on a 0.01 dex grid over [−1, +1]. The headline is **CALIBRATION-ROBUST** if the class is unchanged for every |τ| ≤ 0.25 dex (the CFG219 baseline for one sigma of the shared gas calibration), else **CALIBRATION-LIMITED**, and the distance to the flip is reported as |τ_flip|/0.25.

## Comparison with the forecast (CFG219)
The realised (median δ_flat, median δ_rival) at table_Rout, ν_mono, canonical, is reported beside CFG219's expected pooled shifts at R_out for six discs (flat true: (0, −0.33); rival true: (+0.30, 0)) and the CFG219 total scatter for N = 6, τ = 0.25 read from its results JSON; the distance to each truth in units of that scatter is reported as a description, not a test (CFG219 used a thin-disc model baryon curve, this lane the fit's).

## One-sided bounds
For 08, 12, 23b, δ_L computed with the table's f_molgas as if a value is a LOWER bound on the true δ (an upper limit on the gas caps g_bar, and δ falls as g_bar rises). Report each disc's bound and how many bounds lie above the six-disc median; a bound is never entered in a median.

## Controls (all must pass)
- **C1** with ρ = 1 and CFG213's twelve-disc outer-radius sample the medians equal CFG213's committed values (table_Rout: flat +0.019, rival −0.283; outermost marker: +0.023, −0.258) to 1e-3.
- **C2** ρ = 1 gives D_ind = D_fit exactly (synthetic rows with M_ind = M_fit, 1e-12).
- **C3** at the solved τ\*_L the law's median δ is 0 to 1e-9.
- **C4** for each upper-limit disc δ falls monotonically as the gas mass rises (so the bound direction is right).
- **MUTATE** (`MUTATE=1`, outputs `*_MUTATE`): D × 1.5 raises every median by log₁₀ 1.5 to 1e-9.

## Reporting rules
No sentence says the data favour the framework; n = 6 is small and the bootstrap sees only the disc-to-disc scatter, not the SED/f_molgas errors; the curves are model curves; the pressure treatment is the authors'; the outcome class is a description of these six discs, not a separation of laws unless ROBUST and CALIBRATION-ROBUST and LOO-ROBUST; first-run outputs are kept if a check implementation is fixed; outputs named by mode.
