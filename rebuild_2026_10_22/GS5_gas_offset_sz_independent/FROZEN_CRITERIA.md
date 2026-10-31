# GS5_gas_offset_sz_independent: FROZEN CRITERIA (committed alone, before any cross-match or number from it)

**Question.** ZN3's native cluster profile passes X-COP and 15 shear keys only if eRASS1's Mgas500 is raised by at least about +0.093 dex. SM1 says +0.111 (X-ray against X-ray, five clusters), RF3's hydrostatic-free version +0.092 ± 0.015. Does the thermal SZ signal, which measures the gas pressure integral, give the same offset? d is defined as the amount eRASS1's Mgas500 must be raised, at eRASS1's own R500.

**Disclosed.** ZN3 needs d high, so a high answer is one I'd welcome. Every correction that raises d is therefore reported on and off, and an ABOVE class must be read beside the selection bracket below. I have read ZN3, SM1, GS3, RF3's criteria and offset. I've inspected file headers and X-COP radial coverage only. Three older scripts use the PSZ2 file (`hunt_2026/h59*`, `CFG517`); I haven't read their results and take nothing from them. I expect route (a) to come out NOT POWERED on its systematics.

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. No downloads. No Λ-CDM input in a grade (ledger states the catalogues' own conventions).

**Two points about the brief, stated before any number.**
1. On the *same* clusters in X-COP and eRASS1, Y cancels from Q_E/Q_X, leaving Mgas × T against Mgas × T. That is SM1 again with T added, and carries no SZ information. So route (b) is a *population* comparison, with Y as a transfer standard between different clusters. The same-cluster set is used only for the T scale and for K3.
2. Only route (a) is free of every X-ray flux scale. Routes (b) and (d) are anchored on X-COP's XMM gas masses: they ask if eRASS1 sits low against X-COP without using any cluster observed by both for the gas, which is the quantity ZN3 needs, but they don't test XMM's absolute flux.

## Data
- PSZ2 union `real_research/data/psz2_union.tsv`: Y5R500 (10⁻³ arcmin²), e_Y5R500, MSZ, SNR, z, positions. Clusters with z > 0.
- eRASS1 `erass1cl_primary_v3.2.fits`: MGAS500, KT, R500, M500, F, BEST_Z, PCONT < 0.5, finite positive values. h 0.70, Ω_m 0.3 (GS3).
- X-COP, 12 clusters on disk: `*_fgas_profile.fits` gas, `*_hydro_mass.fits` M_FORW. **No temperature profile is on disk.** T_X comes from the hydrostatic inversion below.

## Quantities
- **Constant:** Y D_A² = C Mgas T, C = σ_T/(m_e c²)/(μ_e m_p), μ_e 1.17 (T the mass-weighted T inside the aperture, Y spherical in the same aperture).
- **Distance:** D_A at h 0.70, Ω_m 0.3, the convention in which the catalogues' Mgas and R500 were reported.
- **Y500** = Y5R500/1.79 (Planck's own GNFW shape), route (a) only.
- **X-COP P and T:** P_gas(r) = ∫_r^∞ ρ_g G M_FORW / r² dr, with ρ_g from the gas profile, gas and M_FORW extended past their last radius as power laws from the last 5 points. n_e kT = P_gas μ/μ_e with μ 0.6. kT_mw = (∫ n_e kT dV)/(N_e) inside R500. Because M_FORW is itself derived from X-COP's thermal pressure, this recovers that pressure. Thus K2 is partly self-referent: X-COP's outer pressure uses Planck's y map.
- **Match:** eRASS1 to PSZ2, mutual nearest, sep ≤ max(5′, 0.3 θ500) capped at 10′, |Δz| ≤ 0.02. X-COP to PSZ2 the same.

## Selection (rule fixed, numbers not seen)
- Cells: lg Mgas500 edges 13.0, 13.3, 13.6, 13.9, 14.3; z edges 0.03, 0.10, 0.15, 0.20, 0.25. Lensing keys' range is covered; z ≤ 0.25 limits the E(z) lever.
- f = (matched)/(all eRASS1) in the cell. Planck detection selects high Y at fixed Mgas, which would read as a **high** d. So a cell enters only if f ≥ 0.85 and n ≥ 5. Fewer than 30 clusters overall: NOT POWERED.
- **Selection bracket:** lower edge: unmatched clusters in those cells enter with Y = 0. Upper edge: matched only (the central). Half the range goes into the SE, the lower edge is always printed.

## Estimators (ratio of sums, frozen)
Averaging linear Y, not log Y, so noise at low S/N doesn't bias; ratio of sums, so noise in the denominator doesn't either. No S/N weights, since Planck's e_Y correlates with Y.
- **Eddington on Mgas:** selection is on measured Mgas. Each eRASS1 Mgas in a prediction is taken as Mg × 10^(β ln10 σ²), σ its catalogue error in dex, β = dlog N/dlog Mg from the eRASS1 parent counts over lg Mg ± 0.3. This raises d. Half of the on/off difference goes into the SE; both printed.
- **X-COP aperture:** X-COP's gas is read at R500 × 10^s, s = the signed median dlog R500 over SM1's 5 matches, recomputed here, so d is at eRASS1's radius as the line is.
- **(a) absolute:** d_a = log[ΣY500D² / Σ(C Mg T)] with T = KT × 10^δT, where δT = median log(T_X/KT) over the same-cluster set. SE adds a fixed systematic budget: Y5/Y500 ±0.03 dex, T weighting (spectral against mass-weighted) ±0.03, μ_e ±0.005, Planck Y calibration ±0.01. Also printed with raw KT, and against X-COP's own Q from K2.
- **(b) relative to X-COP, population:** d_b = log[ΣY/Σ(Mg KT 10^δT)]_E − log[ΣY/Σ(Mg T_X)]_X. δT's error included. Also printed with raw KT. eROSITA's T offset may grow with T, and the five are hot; printed by mass bin, and a limit.
- **(d) T dropped, Y as transfer:** Y D² E^(−2/3) = A Mg^α, α 5/3, with A from X-COP alone. d_d = (1/α) log[Σ Y D² E^(−2/3) / Σ A Mg^α]_E. **Assumes:** clusters of one Mgas have one Y whichever survey found them, that is same f_gas and same T at fixed Mgas in X-COP and eRASS1, self-similar slope and evolution, and no selection of X-COP on Y at fixed Mgas. X-COP is Planck-selected, so if that selection acts it lowers d_d; printed by a toy with scatter 0.1 dex.
- **E(z)** uses Ω_m 0.3, the catalogue convention, only in (d). z ≤ 0.15 subset printed, where the effect is under 0.02 dex.

**SE** = quadrature of: bootstrap (2000 draws, eRASS1 clusters, X-COP clusters and the same-cluster set each resampled; seed 5), selection half-range, Eddington half-difference, half-range over s ∈ {0, SM1 median, mean over the same-cluster set}, half-range over Ω_m ∈ {0.2, 0.4} with Mgas restated as D^2.5 and Y as D², plus for (d) half-ranges over α ∈ {1.4, 1.9} and E exponent ∈ {0, 2/3}, plus (a)'s budget.

## Two Y products
- **Primary: Y5R500**, Planck's marginal over size. Its size-flux degeneracy pushes it high where the size is poorly fixed, depending on θ500 and S/N, and X-COP's clusters are large on the sky, so the bias may differ between the samples. Printed: d by θ500 (< 10′, ≥ 10′) and by S/N (< 7, ≥ 7).
- **Secondary: Y(MSZ)** ∝ MSZ^1.79, read back through Planck's own relation with E^(2/3). This is the flux at the size fixed by Planck's Y–θ relation, so no size freedom, at the price of that relation's prior. Used in (d) only, normalised on X-COP as above so its constant drops out, and with the same SE rule.

## Verdict
Class of a route, in this order: **NOT POWERED** SE > 0.05; **NO OFFSET** |d| < 2 SE; **ABOVE THE LINE** d − SE ≥ +0.093; **BELOW** d + SE ≤ +0.093; else **ON THE LINE**.
- **Headline:** route (d), primary Y, in the qualified cells.
- **[T-DEPENDENT]** if a powered (a) or (b) differs in class from (d).
- **[Y-PRODUCT-DEPENDENT]** if (d) with Y(MSZ) differs in class.
- d by Mgas bin reported, each route; bins have no class of their own unless SE ≤ 0.05.
- If SE > 0.02, the README says so: the line needs about 0.02.

## Second route, consistency line only: NOT INDEPENDENT
The 15 keys' shear, same grader as ZN3 (`zn3_grade.py` path, `zn3_shapes.json`, mode fs, X-COP's path untouched), eRASS1's gas × 10^d at d ∈ {−0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25}, f★ 0.034 and 0.0615. Reported: Σ Z² against d per f★ and h, its minimum, Δχ² = 1 edges (Z's are correlated, so indicative), and the d range with all |Z| ≤ 2. **Limit stated now:** in this path M₂₀₀ comes from the baryons by fair share, so gas in the model moves with M₂₀₀; this isn't a zero-gas fit. It inverts the shear for one M₂₀₀ scale along that line, and the d found is the M₂₀₀ scale restated. The same shear graded ZN3, so this can't support ZN3. It takes no part in any class.

## Checks. Any failure: no verdict, except as stated
- **K1:** C at μ_e 1.148 reproduces the textbook 1.416e-19 Mpc²/(M☉ keV) within 0.5 %, and a uniform-sphere case Y = C Mg T computed by direct numerical integration of σ_T/(m_e c²) n_e kT dV matches within 0.5 %.
- **K2:** X-COP Planck Y500 against C Mg T_X (its inversion): |median log| ≤ 0.10 dex. A failure voids route (a) only, and is reported as a finding on the marginal Y; (b), (d) rest on relative Y and proceed, flagged.
- **K3:** match sanity: at least 10 of 12 X-COP clusters in PSZ2; median sep < 3′ in eRASS1 × PSZ2; catalogues rotated by RA +30°, +60°, +90° give false matches under 5 % of the true count; same-cluster set reproduces SM1's +0.111 within 0.005.
- **K4:** route 2 at d = +0.111 reproduces ZN3's Z's at f★ 0.034 within 1e-9 (route 2 only).
- **MUTATE:** Y shuffled among matched eRASS1 clusters: corr(log Y, log Mg) must fall from above 0.5 to |r| < 0.15, else the lane stops.
