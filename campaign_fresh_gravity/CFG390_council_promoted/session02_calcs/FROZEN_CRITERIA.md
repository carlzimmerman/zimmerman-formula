# Session 2 calcs: does the light-end soliton idea for the ultra-faints survive? FROZEN CRITERIA

Written before any script exists or any number below has been computed. κ = ½ fitted; both footings. No dark-matter particle is added: "the fluid" is the record's cold wave field (FL1 / CFG288 road W), and its amount is free.

## The idea under test (from Session 1)
At m = 2.0–4.4e-20 eV (CFG367's surviving light end), the fluid's de Broglie length inside an ultra-faint (σ ≈ 3–5 km/s) is 70–150 pc, larger than the galaxy. So the fluid cannot take the law's target shape there, and it sits in a ground-state soliton. Classical dwarfs (λ < r_half) can follow the target.

## C0. Literature kill test (read 2026-10-06, arXiv API abstract of 2203.05750; provisional per the WebFetch rule)
Dalal & Kravtsov 2022: m > 3e-19 eV at 99% from Segue 1 / Segue 2. **Assumptions stated in the abstract:** heating comes from wave-interference granules in *virialized* FDM halos; soliton heating is neglected; the bound is marginalized over the host halo's circular velocity.
- Frozen reading: the bound applies to the idea **if** the UFD's fluid is a virialized granular halo. It does **not** directly apply to a pure ground-state soliton, which has no granules. Whether the settled fluid is granular or ground-state depends on open piece 1 (the settling dynamics). The calcs below must say whether the idea needs the escape, and if so how large the soliton is relative to a granular halo.
- G0 (computed): at each UFD, the ambient Milky Way fluid's granule heating (Bar-Or, Fouvry & Tremaine 2019 effective mass m_eff = ρ (√π ħ/(mσ))³, Chandrasekhar heating dσ²/dt = 4√(2π) G² ρ m_eff lnΛ / σ, lnΛ = 3, factor-2 systematic declared) over 10 Gyr. PASS if Δσ² < 1 (km/s)² at every UFD. The MW fluid density is the deep-MOND isothermal phantom of 6e10 M☉ at the UFD's current D_gc (the record's MW baryons).

## Data
`real_research/data/dsph/lvd_dwarf_mw.csv` (Pace 2024 LVD, on disk), same cut as AUDIT_UFD: M_V > −7.7, r_half and distance present. Resolved σ only in T1–T3 (the 9 upper limits are reported, not fitted). M★ = 2 L_V. R_e = circularised r_half.

## T1. Scaling regression (the discriminant)
OLS of log σ = a + b log R_e + c log M★ on the resolved sample. Errors: 2000 bootstrap resamples over objects (seed 7), each with σ, R_e perturbed by their quoted errors.
Predictions (b, c):
- the law, deep MOND (UFDs sit at y = 7e-5 to 3e-3): (0, 0.25)
- soliton traced by the stars (soliton r_½ = stellar r_½ at fixed m): (−1, 0)
- stars deep inside a larger soliton core (harmonic, fixed ρ_c): (+1, 0)
- (reported only, not a gate) a cuspy ΛCDM halo family: b ≈ +0.5
Rule: a model is DISFAVOURED if its (b, c) lies at Mahalanobis distance > 3.44 (χ²₂, p = 0.003) from the fit under the bootstrap covariance. NON-DISCRIMINATING if the law and soliton-trace points are within 3.44 of each other in that metric, or the bootstrap σ_b > 0.5.

## T2. Implied field mass under "the stars trace the soliton"
Schive 2014 soliton, ρ(r) = ρ_c / [1 + 0.091 (r/r_c)²]⁸, ρ_c = 1.9 (m/1e-23 eV)⁻² (r_c/kpc)⁻⁴ M☉ pc⁻³. Plummer stars with projected half-light R_e. Global σ_los² = ⅓ ⟨G M(<r)/r⟩ over the stellar light (virial; infinite aperture, declared). Stellar self-gravity included. Trace: soliton 3-D half-mass radius = 1.305 R_e.
For each resolved UFD, solve for the m that reproduces σ_obs.
- PASS (idea alive on T2) if the median implied m lies in 2.0–4.4e-20 eV **and** at least half of the objects' 1σ ranges overlap that window.
- FAIL if the median lies outside 1.0–8.8e-20 eV (a factor 2 beyond the window).
- Otherwise MARGINAL. Report the scatter of log m against the scatter of the law's residual log(σ_obs/σ_law).

## T3. Free soliton at fixed m (reported only)
At m = 2e-20 and 4.4e-20, for each UFD solve for the r_c that gives σ_obs (any σ is reachable, so this is not a test). Report r_c, the soliton mass, the ratio of r_c to the de Broglie length, and the ratio of the soliton's mean density within R_e to the MW's mean enclosed density at D_gc (tidal survival needs ≳ 3; current D_gc, not pericentre, declared).

## Controls (all must pass in the main run)
- K1: sample = 31 resolved + 9 upper limits, as AUDIT_UFD.
- K2: virial σ code on a self-gravitating Plummer sphere reproduces σ_los² = πGM/(32 a) to 1e-3.
- K3: the soliton total mass reproduces M_s ≈ 2.2e8 (m/1e-22)⁻² (r_c/kpc)⁻¹ M☉ (Schive 2014) to 5%.
## MUTATE
Run with `--mutate`: ρ_c normalisation ×10. K3 must fail (exit 1). Outputs written to separate `_MUTATE` files.

---
## ADDENDUM F (frozen after the main run above, before any F number exists)
Main run: soliton-traced DISFAVOURED (T1), T2 FAIL (implied m 3.9e-21). The light-end soliton idea is dead. T1 left the law's *shape* allowed (Mahalanobis 1.88): the UFDs scale like the law with an offset.
**F. Fossil-phantom switch (zero new parameters).** Reading: a conserved fluid can only re-arrange to a new target where its de Broglie length is below the system's size. Where λ > the system, the fluid stays as the fossil of the target set by the baryons the galaxy had before it lost them.
- Per object: λ = 2πħ/(m σ_obs) (σ_ul for upper limits) against r_½ = (4/3) R_e. If λ > r_½, use M_init = R_ind × M_now (CFG317 leaky box, as in AUDIT_UFD §7); otherwise M_now. m = 2.0e-20 and 4.4e-20 eV.
- The law row is AUDIT_UFD's isolated estimator (exp kernel = ν_mono here), Υ_V = 2, Kaplan–Meier median over 31 + 9.
- Error: the audit's own scale, 0.325 / 3.77 = 0.086 dex (canonical), 0.304/3.55 = 0.086 (alt).
- PASS if |median| < 2 × 0.086 at the nominal yield (−0.2) on both footings; FAIL otherwise. Yields −0.5 / +0.1 reported as a bracket.
- The classical dwarfs must not switch (λ < r_½ for all 12); if any does, report its effect.

---
## ADDENDUM D (frozen before any D number exists): SPARC a₀ by distance method
At fixed Υ the inferred a₀ scales as D⁻² (g_bar is distance-free, g_obs ∝ D⁻¹, deep regime a₀ = g_obs²/g_bar). SPARC's Hubble-flow distances assume H₀ = 73.
- Data: CFG4_common.load_sparc() (175 rotmod + Lelli 2016c master table); f_D classes 1 Hubble flow, 2 TRGB, 3 Cepheid, 4 UMa cluster, 5 SNe. Q ≤ 2 (declared), all points with g_bar, g_obs > 0, CFG4's weights.
- Fit: ν_mono, one free a₀ per class (log-grid, weighted least squares on log g_obs − log ν g_bar), at (i) Υ_disk = 0.50 fixed, (ii) Υ_disk = the CFG4 all-sample profiled value fixed. Υ_bul = 1.4 Υ_disk.
- Errors: bootstrap resamples over galaxies within each class (seed 3): 500 for the two tested classes, 200 for the reported single classes. (Changed from 1000 before any output existed: the first launch timed out with no numbers written.)
- Test: Δ = log a₀(Hubble flow) − log a₀(ladder: TRGB + Cepheid + SNe combined). SIGNIFICANT if |Δ| > 3σ_Δ. A 9% H₀ shift equals 0.075 dex.
- Reported: per-class a₀, and the H₀ that would null Δ (H₀_null = 73 × 10^(−Δ/2); the frozen text had the sign wrong — a₀ ∝ D⁻² ∝ H₀² — fixed after the first run, disclosed).
- MUTATE (`--mutate`): multiply ladder distances by 1.2 before fitting (g_obs scaled by 1/1.2, gas and disc velocities² unchanged per D-scaling ... implemented as g_obs /1.2, g_bar unchanged). Δ must move by +2 log 1.2 = +0.158 within 0.02, else exit 1.

---
## ADDENDUM S (frozen before any S number exists): super spirals against the two retention levels
cm08's definition exactly: f = (M_dyn − M_law) / ((Ω_c/Ω_b) M_b), Ω_c/Ω_b = 0.1200/0.02237, at each galaxy's measured radius. M_dyn = v_obs² r / G; M_law from CFG56's own `pred(..., which="law")` (bulge + disc, Simard B/T), canonical and alt. CFG56's 23 Ogle+2019 discs, nine fastest reported separately.
- Levels from the record: galaxy ≈ 0.13 (non-central ETGs 0.13, MW 0.14, spirals ≤ 0.105); group/cluster ≈ 0.6 (centrals 0.64, groups 0.60, X-COP 0.576).
- Error per galaxy: v_obs error, plus 0.059 dex (CFG56's stellar-mass systematic) on M_b propagated; median with bootstrap over galaxies (seed 5, 2000).
- Reading (descriptive, like cm08): the nine fastest are "galaxy-level" if their median f is within 2σ of 0.13 and > 2σ from 0.6; "group-level" in the mirror case; "between" otherwise. Super spirals' virial temperatures (μ = 0.6, T = μ m_p V²/2k) are reported to place them against the step's 0.5–2.3e6 K.
- This is shared with ΛCDM (CFG68) and can only fail the temperature-keyed reading, never confirm the framework.
- MUTATE: M_law = M_b (no phantom): f must rise by > 0.1 (else exit 1 is NOT produced; the MUTATE check exits 1 when it detects the change, by convention).
