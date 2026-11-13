# EXR1R (BLIND RE-GRADE OF EXR1, WIDE-LENS X-RAY CUSP): PROTOCOL

2026-11-12. Committed alone, before any script of this lane exists and before any number of it is computed. A blind
re-grade; it does not relabel EXR1 and adopts nothing. κ = ½ FITTED. Footings (canonical a₀ = 9.3603e-11, alt
1.132e-10 m/s²) graded separately, never pooled. One-sided: no outcome favours the framework.

## What I read, and what I will not read until my numbers are committed

Read: EXR1's `FROZEN_CRITERIA.md` and `AMENDMENT_A1.md`; ESZ1's and EUC1's `FROZEN_CRITERIA.md`. Raw inputs: the two
ECLIPSE CSVs (`_external_data/euclid_dr1_eclipse/`), the AtomDB 3.1.3 line and coco files and the TM0 ARF/RMF of source
products 180135/00004 (`_external_data/exr1_erass1/`), `real_research/data/erass1cl_primary_v3.2.fits`, and the raw
service responses under `_external_data/exr1_erass1/fetch/{ul,nh,scs}/` with that folder's `MANIFEST.json` (request
URLs). I parse the raw responses myself and do not use the `*_table.csv` files in that folder (EXR1's parse).

Not read until my script and outputs are committed: EXR1's `RESULT.md`, scripts and outputs; ESZ1's, EUC4's and EUC8's
results, code and outputs; EUC1's code and outputs (I write my own lens model from EUC1's text); any EXR1 or ESZ1
memory entry; `git log`; the shared side-session notes about EXR1, EUC4 or EUC6.

## Seen before writing this note (disclosed)

- File names in EXR1's folder (`exr1.py`, `exr1_a1.py`, `exr1_fetch.py`, twins `inject`, `shift`, `newton`,
  `exr1_arrays.npz`, `exr1_per_lens.csv`). No file opened.
- The amendment's numbers: frozen-run null mean +1.61e-15 against a K8 limit of 1.33e-15, σ = 1.77e-15 (the null rms),
  all eight nulls positive; twin `shift` K7 stack 7.1 σ, recovery 4 of 60; twin `inject` σ 15.0e-15; a random 30″
  aperture holds a catalogued source 1.9 % of the time. So I know frozen K8 failed in EXR1's run.
- The raw cache's `fetch_log.txt` and manifests: S 6,173, W 316, positive-control clusters 3,730, K4 groups 39;
  16,161 upper-limit look-ups (= 6,173 S + 2,528 W shifts + 2 × 3,730 clusters); 355 N_HI positions (316 + 39);
  383 cones (60 clusters, 60 shifted clusters, 263 lenses at 0.55°).
- The project memory index loaded into my context, which carries ESZ1's word (ONLY A CUSP IS LEFT; cored bodies
  excluded), and the task text (EUC4's finding; EXR1 landed with a frozen word and an amendment). No EXR1 word or number.
- File names in the shared notes folder (`EXR1_xray_cusp_done.md`, `EUC4R_…`, `EUC6R_…`, `EUC14_…`); none opened.

## How I resolve each ambiguity (fixed now)

1. **Lens model (EUC1 §3 from text).** Sample S: grades A, B; `lens_model_success`, `final_sample`,
   `large_system_warning == False` (object catalogue joined on identifier); θ_E (effective) > 0, R_e > 0,
   0.6 ≤ n ≤ 10, z_l > 0, log M★ > 0; finite key-catalogue `ra`, `dec`. W: θ_E ≥ 1.7″. Prugniel–Simien with
   p = 1 − 0.6097/n + 0.05463/n², b_n solved exactly from γ(2n, b) = Γ(2n)/2; M★(<r) by the regularised incomplete
   gamma. Flat ΛCDM H₀ 67.74, Ω_m 0.3089, distances by direct integration. Σ_cr,∞ at z_s = 1100. Law S
   g = ½ g_N (1 + √(1 + 4a₀/g_N)). M_2D(<R) = (R²/G) ∫ g dr/√(r² − R²) to r_max = 10⁶ kpc, in r = R cosh u,
   Gauss–Legendre split at 300 kpc. Constants: G 6.6743e-11, M☉ 1.98841e30 kg, kpc 3.0856776e19 m, m_p 1.67262e-27 kg.
2. **G2 gas.** ρ = A r⁻² for r < 300 kpc (no core), zero beyond; its Newtonian field adds to the stars'; law S acts on
   the sum; A solved (Brent) so that M_2D(<R_E) = π R_E² Σ_cr; A = 0 if the stars alone reach it. Hydrostatic:
   P(r) = ∫_r^{300} ρ g dr; kT = μ m_p P/ρ; μ 0.59, μ_e 1.14, X = 2/μ_e − 1, n_e n_H = X ρ²/(μ_e m_p²).
3. **Plasma.** Lines from the line file (E = 12.39842/λ keV) and continuum plus pseudo-continuum from the coco rows
   with rmJ = 0, integrated exactly as piecewise linear; tables taken as already carrying AG89 abundances (K1 tests
   this). H and He at 1, Z ≥ 3 times the metallicity. Spectra interpolated linearly in emissivity against log kT
   between the two bracketing tabulated temperatures, gas by gas along the radial grid.
4. **Flux.** Photon flux = photon luminosity × (1 + z)/(4π D_L²), D_L = D_A(1 + z)²; MM83 Table 2 coefficients
   (σ(1 keV) = 2.42e-22 cm²) at observed energy on a fine grid, before rebinning to the ARF grid; SPECRESP of the TM0
   ARF and the dense TM0 RMF; band channels are those whose midpoint lies in 0.2–2.3 keV. Reference: photon index 2,
   N_H 3e20, MM83, absorbed 0.2–2.3 keV energy flux. F_cat = F_ref CR_model/CR_ref. Radial grid: 400 log-spaced
   shells from r_in to r_out.
5. **N_HI.** The "Weighted average nH" line of each cached HEASARC response, matched to positions within 1″.
6. **Positions and matching.** Shifted positions on the sphere: 0.5° great-circle distance at true position angle
   (north through east). Cached upper limits matched to my positions within 1″; any position of mine not in the cache
   is fetched live in one paced stream (≥ 1 s apart, generic client name) and recorded. B = `Bkg_counts`,
   T = `Exposure`, C = `Count`.
7. **Valid position:** de_sky true and T > 0. Frozen null stack k: mean over T lenses whose shifted position k is
   valid. Rms of nulls about zero (frozen and A1); about their own mean (reading R).
8. **Clipping:** min(value, 1e-12) on every per-lens measured and predicted value (and on cluster values in K7);
   in twin `inject`, pred_i is added before clipping.
9. **Bootstrap:** `numpy.random.default_rng(20261112)`, 2,000 resamples, a fresh generator per statistic; Part C
   interval = 2.5 and 97.5 percentiles.
10. **K3:** all S positions that are valid; KBN (1991) posterior with flat prior on S ≥ 0, 99.87 %.
11. **K6** needs ESZ1's lens list and `esz1_results.json`, which I may not open blind. It is evaluated only after my
    outputs are committed, by a separate script that imports my solver unchanged; my blind words are recorded as
    conditional on K6, and a K6 failure would make them NOT EVALUABLE.
12. **K7:** M500 ≥ 2e14 M☉ (catalogue unit read from its header), 0.1 ≤ BEST_Z ≤ 0.6, valid; σ = bootstrap over
    clusters. The 60 are drawn by `default_rng(20261112).choice(n, 60, replace=False)` over the valid clusters sorted
    by DETUID; cones of mine not in the cache are fetched live (radius 60″).
13. **K8 under R:** "scatter half" = every null within 3.5 σ of the null mean (also reported against zero).
14. **A1:** lenses with fewer than 6 valid shifted positions are dropped from the A1 set; pred_min is the mean over the
    A1 set; null k for lens i uses lens i's other valid shifted positions.
15. **Part C, Part L, classes:** controls from S with θ_E < 1.0″, valid, nearest in (Δz/0.05)² + (Δlog M★/0.1)² with
    catalogued (unboosted) log M★, without replacement, T in identifier order, ties to the lower identifier. Chance
    rate in Part L from the cached 0.55° lens cones.
16. **f_T:** kT(r) divided by f for every lens; the smallest f > 1 on a grid where pred_min falls to measured + 2σ.
17. **Twins exit 1** when the mutation shows the frozen effect; 3 if it does not bite. Mine: `inject`, `shift`,
    `newton`, and the A1 `inject`, outputs `exr1r_MUTATE_<name>.*`.
18. **My own known answer for the flux chain** (independent of EXR1): pure-hydrogen free-free continuum at
    kT = 8.6 keV against the Rybicki–Lightman formula with a 1.2–1.3 Gaunt factor; MM83 at 1 keV; the absolute TM0
    ECF of the reference power law against the catalogue's 1.074e12 (reported, shape-only use stands).

Live check: about 20 cached upper-limit positions drawn with seed 20261112, re-queried in one POST.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
