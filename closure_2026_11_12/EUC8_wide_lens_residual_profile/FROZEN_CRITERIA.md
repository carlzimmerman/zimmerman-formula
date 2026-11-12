# EUC8 (WIDE-LENS RESIDUAL PROFILE): FROZEN CRITERIA

2026-11-12. Committed alone, before any script of this lane exists and before any number below is computed. A test
lane; it adopts nothing. κ = ½ FITTED. Footings (canonical a₀ = 9.3603e-11, alt 1.132e-10 m/s²) graded separately,
never pooled. One-sided: no outcome favours the framework.

## Question

EUC4 (confirmed blind by EUC4R) found that Euclid's wide-separation lenses need more projected mass than law S gives
the lens galaxy's stars. EUC6 found those lenses in richer environments; EUC5's reading is that their stars feel extra
mass too. The framework carries such a residual in clusters as cold dark energy but has no constructed state for it.

**What must the extra mass look like?** Part A states how much is needed, in physical units. Part B asks how
concentrated it is, by tying two apertures on the same galaxies: the Einstein radius (projected mass, ECLIPSE) and the
spectroscopic fibre (stellar velocity dispersion, EUC5's DESI fits).

## Data (all on disk; nothing new is fetched)

- ECLIPSE catalogue, the two files and hashes frozen in EUC1; EUC1's `load`, `select`, `build`, `Engine`, cosmology.
- EUC5's `euc5_a1_dispersions.csv` with the quality cuts of `euc5_a1.py` (55 lenses of sample S), and EUC5's Jeans
  code (`euc5.py`: `sersic_model`, `sigma_ap`, `ap_weight`), fibre radius 0.75″, seeing 1.1″.
- Dispersion scale: EUC5 §3b. Fitted dispersions are divided by 1.064; the scale interval [1.016, 1.141] widens every
  interval below. That calibration was post hoc in EUC5 (its mock gate failed). Every word of Part B is therefore
  conditional on it, and is a reading of 25 noisy spectra, not a gate on the law.
- SLACS table (`real_research/data/slacs_auger2009_lenses.tsv`), as in EUC5's check J3.

## Model

Spherical. Stars: Sérsic with the catalogue's n and R_e, Prugniel–Simien deprojection, mass = catalogued Salpeter mass
× 10^b★. Extra component X with enclosed mass M_X(<r). The Newtonian fields add and law S acts on the sum:
`g = law_S(g_N★ + g_NX)`. Projected mass inside R_E by EUC1's integral; fibre dispersion by EUC5's Jeans model with
the stars as tracer, isotropic (β = 0).

Families of X, one free amplitude each:

| Name | Enclosed mass |
|---|---|
| P | a point mass at the centre |
| T | tracks the stars (the stellar profile) |
| γ = 2.5, 2.0, 1.5, 1.0, 0 | power law ρ ∝ r^−γ cut at r_t = 300 kpc: M_X(<r) = M_t (min(r, r_t)/r_t)^(3−γ) |

γ = 2 is isothermal; γ = 0 is a uniform sphere (close to a mass sheet). For a lens, a family and a source redshift,
the amplitude is solved so that stars + X under law S give the lensing mass π R_E² Σ_cr(z_l, z_s); if the stars alone
already give it, the amplitude is zero.

Source cases (no lens here has a measured source redshift): **far** z_s = 1100 (the least mass lensing allows);
**central** z_s = max(2.0, z_l + 0.5); **near** z_s = z_l + 0.5.

Stellar normalisations b★ = −0.10, 0, +0.10 dex. Zero is the catalogue's Salpeter mass, which EUC5's small-separation
class supports (b_dyn −0.01 [−0.12, +0.16]); ±0.10 spans that interval's core and SLACS's +0.085.

## Part A: the requirement (reported; no word)

Sample W: grades A and B, θ_E ≥ 1.7″ (EUC6's wide sample, 316 lenses expected). Classes 1.3–1.7″, 1.0–1.3″ and below
1.0″ for comparison. For each class, at b★ = 0, law S, each footing, far and central cases: median and 16–84 % of

- the excess projected mass ΔM = π R_E² Σ_cr − M_law+stars(<R_E), in M☉ (zero where negative), and the fraction of
  lenses needing any;
- its mean surface density inside R_E, in M☉/pc² and in units of a₀/(2πG);
- its share of the lensing mass;
- for each family: the mass of X inside a sphere of radius R_E and inside 300 kpc, the latter also as a multiple of
  the catalogued stellar mass; the density of X at r = R_E as a multiple of the cosmic mean cold density
  5.41 Ω_b ρ_crit (1 + z)³ (5.41 is the record's cold share, free, not derived; Ω_b = 0.0488); and the
  pressure-to-density ratio w = V_c²/(γ c²) a fluid in hydrostatic balance with slope γ would need at R_E.

## Part B: how concentrated (words)

Sample D: the DESI-dispersion lenses with θ_E ≥ 1.3″ (25 expected). Required N ≥ 10.

Statistic for a family, source case and b★: `d = log10(σ_measured / σ_predicted)` per lens; the class median with a
bootstrap 95 % interval (2,000 resamples, EUC1's seed), widened below by log10(1.141/1.064) and above by
log10(1.064/1.016).

Family words, per footing:

- **TOO CONCENTRATED**: in the far case the widened upper bound of the median d is below zero, at all three b★. (The
  far case is the least mass; a nearer source only raises the prediction.)
- **TOO DIFFUSE**: in the near case the widened lower bound of the median d is above zero, at all three b★. (This one
  assumes sources are no nearer than z_l + 0.5 and stars no heavier than Salpeter + 0.10 dex.)
- **ALLOWED** otherwise.

Lane word, per footing:

- **NOT EVALUABLE**: an instrument check fails or N < 10.
- **RESIDUAL MUST BE CONCENTRATED**: γ = 0 is TOO DIFFUSE and some family is ALLOWED.
- **RESIDUAL MUST BE EXTENDED**: T is TOO CONCENTRATED and some family is ALLOWED.
- **SLOPE BRACKETED**: both of the above.
- **SLOPE NOT CONSTRAINED**: neither.
- **NO FAMILY FITS**: no family is ALLOWED.

Reported, no word: the slope γ̂ at which the class median d crosses zero (interpolated over the power-law families,
flagged if outside 0–2.5), with its bootstrap interval, for each source case at b★ = 0; the same for the other
Einstein-radius classes and for θ_E ≥ 1.7″; anisotropy β = ±0.2; r_t = 150 and 600 kpc; SLACS at its true source
redshifts (fibre 1.5″, seeing 1.5″, published dispersions); and the sensitivity of γ̂ on mocks (the 25 lenses'
structure and dispersion errors, an injected γ = 2 at the central case, 500 noise draws).

## Instrument checks (all must pass)

- K1 EUC4 reproduced: grade B, θ_E ≥ 1.7″, N = 124, f25 = 0.758 / 0.702 (±0.001).
- K2 two-component solver against EUC1's: for family T the solved amplitude equals 10^b∞ − 10^b★ to 1e-4 (relative)
  on every W lens that needs any.
- K3 projection, Newtonian limit: a point mass returns M to 1e-4; an isothermal field g = 2σ²/r returns
  (2σ²R/G)·arccos(R/r_max) to 1e-4.
- K4 EUC5's J3 through the new solver: SLACS, family T at the true source redshifts, alt footing, median predicted /
  measured dispersion within 0.005 of EUC5's value.
- K5 EUC5's class reading reproduced: θ_E ≥ 1.3″, N = 25, b_dyn = +0.200 canonical (±0.003) on the 1.064 scale.
- K6 injection: noise-free mocks with γ = 2 injected at the central case return γ̂ = 2.00 ± 0.02.

## Mutation twins

- `EUC8_MUTATE=sigup` (measured dispersions × 1.30): γ = 0 must read TOO DIFFUSE on both footings; exit 1.
- `EUC8_MUTATE=sigdown` (× 0.70): T must read TOO CONCENTRATED on both footings; exit 1.
- `EUC8_MUTATE=newton` (a₀ → 1e-30): the median far-case ΔM of W must rise on both footings; exit 1.

## Known before freezing (disclosed)

EUC4's and EUC6's results; EUC5's class readings (b_dyn +0.200 [+0.100, +0.249] ± 0.066 at θ_E ≥ 1.3″, against a
far-case lensing bound below it), so family T is expected to be ALLOWED at b★ = 0, and γ = 0 is expected to depend on
b★; EUC4 Part B's order of magnitude for an extended gas body (10¹³–10¹⁴ M☉). Not known: any dispersion predicted with
an extended component, any ΔM in physical units, γ̂, the words.

## Limits

Spherical; one profile family at a time; isotropic orbits in the word; the fibre and the Einstein radius are 2–3×
apart, so the lever arm is short; photometric stellar masses; no source redshifts. A slope read this way describes the
average of 25 lenses. It tests no part of a₀ or κ.

## Clarification C1 (committed separately, before any script of this lane exists and before any number)

Check K4 as written above compares a median that the two code paths define differently: EUC5's J3 lets the stellar
boost go below zero, while this lane's model sets the amplitude of X to zero when the stars alone give the lensing
mass. A quarter or so of SLACS lenses are expected to be in that case, so the two medians would differ for a reason
that is not a solver error. K4 is restated as a per-lens equivalence of the two code paths:

- **K4** SLACS, alt footing, family T at the true source redshifts, b★ = 0: on every lens whose amplitude is non-zero,
  this lane's predicted dispersion equals EUC5's `sig_of_B` evaluated at that lens's b_lens to 0.5 %. The number of
  such lenses must be at least 30. The full-sample median ratio (with the zero-amplitude lenses) is printed beside
  EUC5's 0.966 for information.

Also fixed here: the dispersion scale and its interval are read from `euc5_a2_scale.json` (1.0641 [1.0155, 1.1408]),
of which the figures above are the rounded values. Nothing else changes.
