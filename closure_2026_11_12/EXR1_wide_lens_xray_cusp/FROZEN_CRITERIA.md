# EXR1 (WIDE-LENS X-RAY CUSP): FROZEN CRITERIA

2026-11-12. Committed alone, before any script of this lane exists and before eRASS1 was read at the position of any
lens, control or shifted position. A test lane; it adopts nothing. κ = ½ FITTED. Footings (canonical a₀ = 9.3603e-11,
alt 1.132e-10 m/s²) graded separately, never pooled. One-sided: no outcome favours the framework. Cold dark energy is a
gravitating field component, never a particle.

## Question

ESZ1 stacked the ACT Compton-y map on Euclid's wide lenses (θ_E ≥ 1.7″). Hot gas bodies with a core (30 or 100 kpc)
that law S would need are excluded by their pressure; a body cusped on the lens (ρ ∝ r⁻², cut at 300 kpc; ESZ1's G2,
from EUC8's γ = 2 family) needs so little pressure that the y map has no power on it (word ONLY A CUSP IS LEFT). Its
reading: the cusp is an X-ray question. **Does eRASS1 see the X-rays that ESZ1's G2 gas must emit?** Part G grades
it. Part C compares wide lenses with matched small-separation lenses. Parts L and D report per-lens and physical
numbers.

## Data

- **Lenses:** ECLIPSE catalogue, EUC1's two frozen files and hashes; EUC1's `load`, `select`, `build`, `g_law`,
  cosmology `EUCLID`. Sample S = `select(rows, ("A", "B"))` with finite RA/Dec. W = S with θ_E ≥ 1.7″ (316).
- **G2 gas:** ESZ1's code imported unchanged (`solve_gas`, `gas_body`, `pressure`, `grid`, μ = 0.59, μ_e = 1.14):
  amplitude solved per lens so that stars plus gas under law S give π R_E² Σ_cr; hydrostatic in law S's own field
  with zero pressure at 300 kpc. kT(r) = μ m_p P(r)/ρ(r); n_e = ρ/(μ_e m_p); n_H = X ρ/m_p with X = 2/μ_e − 1.
- **eRASS1 (eROSITA-DE DR1):** (i) the upper-limit service (`/erodat/upperlimit/service_multi`, band 024 =
  0.2–2.3 keV, DR1_eRASS1): per position the counts C in an aperture of about 30″ (EEF 0.75), smooth-background
  counts B, source-map background, exposure T, UL_B, UL_S, de_sky (Tubín-Arenas et al. 2024); (ii) the Main catalogue
  cone search (`/erodat/catalogue/SCS`, DR1_Main, VERB 1); (iii) the eRASS1 cluster table already on disk
  (`real_research/data/erass1cl_primary_v3.2.fits`, sha256 recorded on first read); (iv) the TM0 ARF and RMF of
  source products 180135/00004 (a source 51° from the nearest ECLIPSE lens), sha256 recorded.
- **Plasma:** AtomDB 3.1.3 APEC CIE line and continuum tables (official CfA tarball, md5
  c6f13b893358cc17e35f22cb81a8490b), read directly (no pyatomdb), Anders & Grevesse (1989) abundances as tabulated;
  H and He at 1, elements Z ≥ 3 scaled by the metallicity; band emissivity interpolated linearly in log kT between
  tabulated temperatures. Emissivity per n_e n_H.
- **Absorption:** Morrison & McCammon (1983) Table 2 (checked against the scanned paper), on N_H = **2 × N_HI**
  (HI4PI, HEASARC nH tool, weighted average within 0.1°) at each lens. The factor 2 is the least-demanding setting
  (it covers molecular and ionised hydrogen generously); 1 × N_HI is a bracket.
- **Band conversion:** eRASS1 fluxes are absorbed 0.2–2.3 keV fluxes for a Γ = 2, N_H = 3e20 power law with
  ECF = 1.074e12 cm²/erg (instrument check K2). A model's **catalogue-equivalent flux** is
  F_cat = F_ref × CR_model / CR_ref, where CR is the count rate in channels 0.2–2.3 keV from folding through the ARF
  and RMF and "ref" is that power law with absorbed flux F_ref. Only the shape of the ARF enters.
- Fetches: one stream, at least 1 s between requests, generic client name, outside git under
  `_external_data/exr1_erass1/` with a manifest (URL, time, sha256).

## Prediction per lens (least-demanding setting, each footing)

Source at infinity (z_s = 1100), stars catalogued Salpeter × 10^0.10, zero edge pressure (ESZ1's least setting);
metallicity **Z = 0.1 Z☉** (AG89); N_H = 2 × N_HI; inner radius **r_in = R_E** (only gas at 3D radius r ≥ R_E
counts). Rest-frame spectrum ∫ n_e n_H ε(E, kT(r), Z) dV over shells, observed at z_l with D_L = D_A (1 + z_l)²,
absorbed, folded: P_i = F_cat of that gas. **Aperture factor** (least demanding): only gas at 3D radius
r ≤ 10″ × D_A counts, and its counts are taken at 2/3 of a point source's (a photon displaced by at most 10″ from the
aperture centre falls inside the 30″ aperture at least as often as a point source's fall inside 20″, taken here as
0.50 against 0.75). pred_i = (2/3) × F_cat(r_in ≤ r ≤ min(10″ D_A, 300 kpc)). Lenses where law S needs no gas have
pred_i = 0 and stay in the stack.

## Measurement

Per position: f = (C − B) / (0.75 T × 1.074e12), the net catalogue-equivalent flux in the aperture (B from the smooth
background map). Every per-lens value, measured and predicted, is clipped at **F_clip = 1e-12** erg/s/cm² (a bright
cluster or AGN in one aperture cannot carry the stack). **Tested set T:** W lenses with de_sky true and T > 0.
**Required N_T ≥ 100.** Stack = unweighted mean over T. **σ** = the larger of (a) the bootstrap standard deviation
over lenses (2,000 resamples, seed 20261112) and (b) the rms of 8 null stacks: the same lenses at 0.5° from their
positions at position angles 0°, 45°, …, 315° (true angle; PA 0° is +0.5° in Dec).

## Part G: words (per footing)

pred_min = mean of the clipped pred_i over T.

- **NO POWER**: pred_min < 3 σ.
- **EXCLUDED**: measured stack + 2σ < pred_min.
- **ALLOWED**: otherwise.

Lane word = that word, or **NOT EVALUABLE** if an instrument check fails or N_T < 100. Tag
**[BRACKET-DEPENDENT: list]** if it moves under any of: Z = 0 (H and He only); Z = 0.3; N_H = 1 × N_HI; point source
(all gas from r_in to 300 kpc, aperture factor 1); r_in = R_E/2; r_in = 1 kpc; grade A only; z_l ≤ 0.6 only.
Reported beside it: Z = 1.0, the central source case (z_s = max(2, z_l + 0.5)) and b★ = 0.

No word here is a pass. EXCLUDED says the hydrostatic r⁻² gas is not there at its least emission. Gas much cooler than
hydrostatic would emit below the band, so two factors are reported: f_M = √((measured + 2σ)/pred_min), the largest
fraction of the required gas mass the stack allows at the same profile and temperature; and f_T, the factor by which
kT(r) would have to fall (density fixed) for the predicted stack to drop to measured + 2σ.

## Part C: wide lenses against matched controls (word)

For each lens of T in identifier order, the lens of S with θ_E < 1.0″, de_sky and T > 0 nearest in
(Δz_l/0.05)² + (Δ log M★/0.1)², without replacement (ESZ1/EUC6 rule; ties to the lower identifier).
D_i = f(W_i) − f(C_i), clipped values; mean with a bootstrap 95 % interval (2,000 resamples, seed 20261112).
**Required N ≥ 100 pairs.** **WIDE LENSES ARE BRIGHTER IN X-RAYS** if the lower bound is above zero; otherwise **NO
EXCESS DETECTED** (upper bound reported).

## Part L: per lens (reported; no word)

Main catalogue sources within 30″ of each lens of T (count, catalogued fluxes); the same at the 8 shifted positions
(chance rate). Lenses with UL_B < pred_i (eRASS1's own 3σ bound below the least prediction); lenses where an empty
aperture (C = 0) would give a bound below pred_i (per-lens power).

## Part D: what it means (reported; no word)

Per footing: median required gas mass, kT at R_E, n_e at R_E, rest-frame band luminosity (all gas, and r ≥ R_E),
pred_i, and cooling time at R_E, t_cool = (3/2)(n_e + n_i) kT / (n_e n_H Λ_bol), Λ_bol from APEC over 0.001–20 keV at
Z = 0.1 and 0.3. The stack as a mean luminosity. Classes 1.3–1.7″, 1.0–1.3″, below 1.0″ (measured only).

## Instrument checks (all must pass)

- **K1 APEC reader:** Λ_bol(1 keV, Z = 0) = 8.917e-24 erg cm³/s within 2 %, and Λ_bol(0.12 keV) at Z = 1 over Z = 0
  = 30.1 within 5 % (pyatomdb 1.2.2 on AtomDB 3.1.3 as recorded by CFG581, 0.001–20 keV).
- **K2 band conversion:** the catalogue's band ECF ratios 0.2–0.5 / 0.5–1 / 1–2 keV to 0.2–2.3 keV
  (9.217e11, 1.359e12, 1.014e12 over 1.074e12) reproduced within 8 % for the absorbed Γ = 2, N_H = 3e20 power law.
- **K3 upper limits:** UL_B recomputed from (C, B, T) as the Kraft, Burrows & Nousek (1991) bound at 99.87 % over
  0.75 T × 1.074e12 agrees within 2 % at ≥ 99 % of the de_sky lens positions.
- **K4 known answers (eRASS1 groups):** the clusters with kT measured to 30 % (KT_H − KT_L < 0.3 KT) and z > 0.05
  (39 rows): APEC at their kT, Z = 0.3, z and 1 × N_HI. (a) CR500/F500 against the predicted catalogue-equivalent
  count rate per absorbed flux: median ratio 1 ± 0.10. (b) F500 × 4π D_L² / L500 (flat ΛCDM, H₀ 70, Ω_m 0.3) against
  the predicted absorbed-observed over rest-frame band ratio: median 1 ± 0.10. (c) Gas mass to flux: L500 over the
  least band luminosity MGAS500 can have inside R500 at kT (a uniform sphere): median between 1 and 30.
- **K5 luminosity integral:** a Newtonian r⁻² body at constant Λ against 4π n₀² r₀⁴ Λ (1/r_in − 1/r_t)(n_H/n_e),
  to 1e-4.
- **K6 ESZ1 reproduced:** on ESZ1's 237 W lenses, G2 far, b★ = +0.10, median gas mass, kT and n_e at R_E equal
  `esz1_results.json` to 0.1 % on both footings.
- **K7 positive control:** eRASS1 clusters with M500 ≥ 2e14 M☉ and 0.1 ≤ z ≤ 0.6 (ESZ1's K8 selection), de_sky:
  stacked aperture net flux positive at ≥ 5 σ; and of 60 of them drawn with seed 20261112, ≥ 90 % have a Main
  catalogue source within 60″.
- **K8 nulls:** the 8 null stacks of T: mean within 3σ/4 of zero, none beyond 3.5 σ.

## Mutation twins (each must exit 1; separate output names)

- `EXR1_MUTATE=inject`: pred_i (primary setting, canonical) added to every tested lens's measured value: the word
  must read ALLOWED on both footings.
- `EXR1_MUTATE=shift`: every lens and cluster moved +0.5° in Dec: K7 must fail.
- `EXR1_MUTATE=newton`: a₀ → 1e-30: pred_min must rise on both footings.

## Known before freezing (disclosed)

- ESZ1's results (above) and EUC1–EUC8's. Access checks, none at a lens, control or shifted position: a cone of 37
  Main-catalogue sources at (180°, −45°) gives ECF 1.074e12 for 0.2–2.3 keV and the band ECFs quoted in K2; folding
  the TM0 ARF/RMF of source 180135/00004 reproduces those band ratios within 3 % if the catalogue fluxes are absorbed
  and misses by 40 % if unabsorbed (so the absorbed convention is used); the upper-limit service at 97 positions near
  (185°, −45°): UL_B 5–6e-14 for empty apertures at 150–210 s, reproduced by hand at two of them (6.64 counts for
  C = 0). The cluster table: 39 groups in K4 (median z 0.07, kT 1.2 keV), CR500/F500 median 1.154e12 cm²/erg,
  F500 × 4πD_L²/L500 median 0.83. 263 of the 316 W lenses have Galactic longitude ≥ 180° (coordinates only).
- No prediction of this lane was computed before freezing; the hand estimate below is the only number.

## Hand estimate (before any number; unverified)

N_T ≈ 263. Per-lens background ≈ 0.8–1 count at T ≈ 150–200 s, so one count ≈ 7e-15 and σ ≈ 1e-15. G2 at 0.41 keV,
n_e 0.2 cm⁻³ at 12.6 kpc: emission measure from r ≥ R_E ≈ 2e67 cm⁻³; at Z = 0.1 a band emissivity near 5e-24 gives
L ≈ 1e44 erg/s, F ≈ 1.3e-13 at z 0.45, about 0.7 of that after absorption and the band conversion, and the aperture
factor about 0.55: pred_min ≈ 5e-14, some 50 σ. At Z = 0 (free-free and H/He recombination only) about 2e-14. The
wide lenses (massive ellipticals in groups) should show 2–5e-15. Expected: **EXCLUDED / EXCLUDED** at tens of σ,
also at Z = 0; Part C NO EXCESS DETECTED or a small excess; cooling time at R_E 10–30 Myr.

## Limits

Spherical; hydrostatic; single-phase gas in collisional ionisation equilibrium; photometric lens redshifts; no source
redshifts (the far case is the least mass). Gas far below its hydrostatic temperature emits below the band and is
not tested (f_T says how far). X-rays from the lens galaxy's AGN, its group or a lensed AGN add flux and work against
EXCLUDED. The aperture factor rests on a stated PSF bound, not on a fitted PSF. It tests no part of a₀ or κ.

## Compute and outputs

Light. Scripts `exr1_fetch.py` (network, cached) and `exr1.py` (offline grading). Outputs `exr1.out`,
`exr1_results.json`, one `.out` and `.json` per twin, `exr1_per_lens.csv`, `RESULT.md` (label first).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
