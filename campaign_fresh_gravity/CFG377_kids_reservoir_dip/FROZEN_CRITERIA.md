# CFG377: FROZEN CRITERIA -- does KiDS-1000 see CFG372's reservoir dip around isolated lenses?

Written 2026-10-06, before any script or number of this lane exists. Nothing below changes after a result is seen; any departure goes in the README as a disclosed departure.

## Question

CFG372 (post-freeze scorecard (ii)) predicts that the reservoir rule (the phantom's excess over the local cold share is drawn from a 3D Gaussian catchment of width R_c = 3 Mpc/h) lowers the enclosed lensing mass around an isolated lens by about -0.3% at 1 Mpc and -6.5% at 3 Mpc, relative to the bare law truncated at 0.4 r_ta. Is that dip consistent with, disfavoured by, or preferred by the KiDS-1000 isolated-lens excess surface density (ESD) already on disk? If the data do not reach the radii where the dip lives, say so and give a forecast.

## Data (on disk only; nothing is downloaded)

- **PRIMARY.** The June 2026 KiDS-1000 re-measurement of 181,477 isolated lenses (`real_research/data/lensing_rar/lr_lenses.npz`; isolation: no neighbour with M* > 0.1 M*_lens within 3 Mpc transverse and |Δχ| < 10 Mpc). Per-lens pair sums WG, WW per g_bar bin from `cfg110_perlens.npz`; 50 jackknife patch labels from `lr_esd_jackknife.npz`. ESD_k = Σ WG / Σ WW / KG, KG = Msun/(3.0857e16 m)², all lenses (both colour classes together), 15 g_bar bins logspace(1e-15, 5e-12) m/s². No m-bias correction (a common constant, as CFG100).
- **Covariance.** Leave-one-patch-out over the 50 patches, C = (N−1)/N Σ_p (D_(−p) − mean)(D_(−p) − mean)^T; Hartlap h = (50 − p − 2)/49 with p the number of bins used.
- **Radial range.** All 15 bins (the range the data cover). Each bin's radius is reported as the pair-weighted mean of R_ik = sqrt(G M_gal,i / g_k) (g_k = bin centre). The "dip bins" are the bins whose pair-weighted mean R ≥ 1 Mpc.
- **SECONDARY, scored the same way and reported:** (S1) the strictest isolation subset f30 (|Δχ| < 30 Mpc, 57,265 lenses, `cfg96_isoflags.npz`), its own jackknife; (S2) Brouwer+2021 Fig-3 lensing rotation curves (four stellar-mass bins, 15 radii 0.035–2.6 Mpc each, 60-vector, m-bias applied as the README prescribes, B21's own covariance file, no Hartlap since it is not a 50-patch jackknife; declared: B21's covariance is not this lane's jackknife).

## Models (nothing fitted; both a0 footings separately, never pooled: canonical 9.3603e-11, alt 1.1312e-10 m/s²; κ = ½ is FITTED upstream)

- **BARE.** CFG100's `v_law`, copied as source (no cross-lane import): point baryon M_gal plus dark mass M_gal (ν_mono(G M_gal/(r² a0)) − 1) out to r_e = 0.4 r_ta, frozen beyond; r_ta from CFG100's spherical-collapse solution at the lens z; flat ΛCDM background Ωm 0.3153, h 0.6736.
- **RES** = BARE − ΔΣ_G, where ΔΣ_G is the projected excess surface density of a deficit mass M_ex distributed as a 3D Gaussian of width σ = R_c = 3/h Mpc (h = 0.674, as CFG372) centred on the lens: Σ_G(R) = M_ex/(2πσ²) exp(−R²/2σ²), ΔΣ_G = M_ex (1 − exp(−R²/2σ²))/(πR²) − Σ_G(R). M_ex = max(M_d(r_e) − 5.364 M_gal, 0), with M_d(r_e) the BARE dark mass at r_e and 5.364 = CFG372's local cold share.
- **Stacking.** Per lens through grouped cells (0.01 dex in log M_gal × 0.03 in z, evaluated at cell means, as CFG100); within a bin, uniform in ln g, 6-point Gauss-Legendre; model stack per bin weighted by the data's own pair weights WW_ik. S2: lr lenses inside each B21 stellar-mass bin (log M* edges 8.5, 10.3, 10.6, 10.8, 11.0), equal weights, evaluated at the B21 radii.

## Statistics

- χ²_X = h r^T C^−1 r, r = data − model X. **Δχ² = χ²_RES − χ²_BARE**, per footing.
- **Detectability:** μ = m_RES − m_BARE; λ = μ^T h C^−1 μ (the non-centrality of the 1-dof dip-amplitude test). Power at 2σ and 3σ (two-sided) = Φ(√λ − k) + Φ(−√λ − k), k = 2, 3. Amplitude fit A-hat (data = BARE + A μ), σ_A = 1/√λ (reported).
- **Required precision:** the error scale factor s_k = √(λ / k²) for a k = 2, 3 σ expected detection (errors must be multiplied by s_k; lens-number factor 1/s_k² if shape-noise limited), and the fractional ΔΣ precision at the dip radius that this implies (reported with the fractional ΔΣ dip at R = 1, 2, 3 Mpc).

## Verdict (primary data, per footing)

1. If no bin has pair-weighted mean R ≥ 1 Mpc: **NOT TESTABLE** (forecast only).
2. Else Δχ² ≥ 4: **DISFAVOURED**; Δχ² ≤ −4: **FAVOURED-OVER-BARE**; otherwise **CONSISTENT**. A CONSISTENT result with λ < 1 carries the label "uninformative" (the data cannot tell the dip from zero at 1σ).
3. **2-halo guard.** Neither model has a two-halo or environment term; the outer bins of isolated-lens stacks do carry one (CFG96: the all-bin zero-model χ² falls 84.8 → 26.1 with stricter isolation). A DISFAVOURED or FAVOURED verdict is "ROBUST" only if (a) S1 (f30) gives |Δχ²| ≥ 4 with the same sign AND (b) the primary Δχ² with a profiled two-halo nuisance N_k = A × pair-weighted mean (R_ik / 1 Mpc)^−0.8 (A free, linear, profiled analytically in both models) also gives |Δχ²| ≥ 4 with the same sign. Otherwise it is reported as "NOT ROBUST (2-halo / isolation)".
4. S2 is reported, not used for the verdict.

## Controls (a failure invalidates the dependent number and is kept)

- **C1 data:** per-(patch) sums of the per-lens arrays, both classes, reproduce `lr_esd_jackknife.npz` (wgE, W summed over class) to relative 1e-9.
- **C2 projector:** ΔΣ_G (closed form) agrees with CFG100's shell projector applied to the Gaussian enclosed-mass profile to 1e-3 relative at R = 0.3, 1, 3 Mpc; point mass ΔΣ = M/(πR²) to 1e-12.
- **C3 reproduction of CFG372:** CFG372's own recipe (exp kernel, 11.806 ρ_m, z = 0) reproduces its printed enclosed-mass changes at 1 and 3 Mpc (−0.28/−6.62, −0.27/−6.45, −0.28/−6.68, −0.27/−6.54 %) to the displayed digits. The same table with this lane's RES recipe (ν_mono, CFG100 r_ta at z = 0.2) is reported beside it.
- **C4 grouping:** on 2,000 random lenses the grouped stacked μ agrees with the exact per-lens μ to 2% (max over the dip bins, relative to max |μ|).
- **MUTATE (CFG377_MUTATE=1, separate outputs `*_MUTATE.*`):** M_ex × 100. Required: |χ²_RES,MUTATE − χ²_RES| > 4 on the primary data for both footings. If not, the control failed and is reported as such.

## Wording

Never "theory closed" or "the data favour the framework". The cold fluid (no dark-matter particle) is still required; the reservoir is CFG366/372 bookkeeping, not a derived law. Light CPU: one niced process.
