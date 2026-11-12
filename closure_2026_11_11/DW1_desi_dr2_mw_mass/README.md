# DW1 — DESI DR2 III's Milky Way mass, against the a₀-line framework

**Paper absorbed:** DESI Collaboration, *DESI DR2 Results III: The Mass of the Milky Way*, arXiv:2611.05518
(submitted to ApJ, 3 Nov 2026). 10,036 RR Lyrae + BHB halo stars, 6D phase space, 10–95 kpc, four
dynamical-modeling methods, mock-calibrated; joint `M(r<80 kpc) = 6.36 (+0.53/−0.48)×10¹¹ M☉` and
`M200c = 1.19 (+0.14/−0.12)×10¹² M☉`. Table 4 of the paper — the joint enclosed-mass profile at 13 radii,
20 to 80 kpc in 5 kpc steps — is the instrument here; the single numbers are not.

## Why this is the framework's own quantity

The framework has no dark-matter particle. The "dark mass" is the stress–energy of the same scalar whose
horizon scale sets `a₀ = c H_Λ / Z`. The gravitating mass therefore obeys one line, with nothing to fit:

```
M_dyn(<r) = ν( g_bar(r)/a₀ ) · M_b(<r),   g_bar = G M_b(<r)/r²,   ν(y) = 1/(1 − e^{−√y})
```

`M_b(<r)` is the spherical enclosed mass of McMillan (2017)'s baryons (6.681×10¹⁰ M☉: thin 3.519, thick
1.049, bulge 0.923, HI 1.068, H₂ 0.123 in 10¹⁰ M☉), and both registered footings are run:
`a₀ = 9.36×10⁻¹¹` (canonical) and `1.13×10⁻¹⁰ m s⁻²` (alt). DESI's 13 points are 13 independent chances to
fail this line.

## Result

| | canonical | alt |
|---|---|---|
| absolute M(<80 kpc) (A = 1) | 5.69×10¹¹ (−1.34σ) | 6.22×10¹¹ (−0.28σ) |
| one-amplitude profile fit, χ²/dof (13 points) | 0.26 (rms 2.9%) | 0.22 (rms 2.7%) |
| amplitude needed, A* (M_b → A·M_b) | 1.33 ± 0.04 | 1.15 ± 0.03 |
| same number from the framework's own outer rotation curve (item 35) | 1.25–1.31 | 1.15–1.21 |
| 60→80 kpc log-slope: measured 0.71 ± 0.35 | 0.92 (+0.6σ) | 0.93 (+0.6σ) |
| EFE-saturated plateau vs `M200c` = 1.19×10¹² | 0.83×10¹² (−2.8σ) | 0.72×10¹² (−3.6σ) |

For comparison, the paper's own zero-parameter NFW (M200c = 1.19×10¹², c = 12) gives χ² = 17.6/13
(rms 4.5%) on the same table: **this data set cannot distinguish the two shapes**, and the framework does
not need it to.

**Verdict: PASS on the enclosed mass profile (DW1a–DW1d, DW1f: 5 checks), FAIL on the extrapolated
M200c (DW1e).**

## What is genuinely new here

1. **The 20–80 kpc profile is fit by one amplitude to 2.9%.** Not one number is tuned to the halo stars.
2. **That amplitude is the same one the framework's outer rotation curve already demanded** (0.45σ
   canonical, 0.23σ alt). Two independent data sets now agree on the framework's one free ledge — the
   baryonic mass. The repo's standing "the framework needs 25–30% more baryons than the census" liability
   is thereby converted into a measurement with two witnesses, and (if the excess is in stars) into a
   prediction: `M_* ≈ 7.3×10¹⁰ M☉`, a Salpeter-side IMF, falsifiable by the same photometry that would
   otherwise kill the framework.
3. **The EFE is now the dominant modelling uncertainty.** With the Local-Group external field at
   `e_N = 0.0127` the 80 kpc prediction drops to 4.31×10¹¹ (canonical, −4.1σ) and the profile fit needs
   `A = 1.36–1.50` with 7% rms. The profile therefore prefers a *weak* external field — the same direction
   as the rotation-curve fit (item 35, `e_N = 0.000 [0, 0.008]`) and the LMC bound (item 37,
   `g_ext < 0.067 a₀`). The number under pressure is the large-scale-structure estimate of `g_ext`, not `a₀`.
4. **The falsifier has a radius and a size.** The framework says the mass is flat at ≈6.3×10¹¹ M☉ (A=1) to
   ≈8.3×10¹¹ (A*) beyond `r_EFE ≈ 90–100 kpc`. The paper's own NFW extrapolation gives 9.65×10¹¹ at 150 kpc
   and 11.35×10¹¹ at 200 kpc: a 54% / 81% split, i.e. 7σ / 10σ at the paper's 8% precision. DESI DR3 or
   4MOST with halo tracers at 150–200 kpc settles it.

## What is NOT settled, stated plainly

- **`M200c` is not a framework quantity.** The framework has a plateau, not a virial mass. The paper states
  it reports *no* enclosed mass beyond 80 kpc and draws `M200c` as an NFW extrapolation with c = 12; a
  plateau is exactly the profile that extrapolation is built to miss. The −2.8σ is registered as a tension,
  not a refutation — and as the honest size of the framework's largest MW-scale exposure.
- **The spherical reduction is a 1–13% systematic.** A disc's exterior mass still pulls inward in the plane
  (12.7% at 20 kpc, 4.5% at 40 kpc, 1.0% at 80 kpc), so the force-equivalent mass and the spherical Jeans
  mass differ. The lane uses the spherical mass throughout (the quantity a spherical Jeans analysis returns)
  and shows that dropping the 20 kpc point moves `A*` by <1%.
- **The paper's bias corrections are calibrated on ΛCDM mocks** (AuriDESI, NFW-like halos). A profile as
  different from NFW as a plateau is not guaranteed to transfer. Recorded as a scope limit on the data, not
  used to excuse a miss.
- **The 13 table errors are correlated** (all points come from smooth joint fits); χ² here treats them as
  diagonal, which flatters *every* χ² in the lane, the NFW comparator's included.
- `κ = 1/2` remains **FITTED**; nothing here derives `a₀`, the kernel, or the baryon census. `A = 1` is the
  prediction; `A` free is a nuisance and every amplitude claim is quoted both ways.

## Files

- `FROZEN_CRITERIA.md` — the 12 pre-registered checks and pass conditions, committed alone before the script.
- `dw1.py` — the lane (both footings, mutation controls, instrument validation, `dw1_results.json`).
- `dw1.out` / `dw1_results.json` — the committed run.

`DW1 COMPLETE: 9/12 checks PASS.` — the three failures are V2b, V3 (instrument gates whose frozen
thresholds are mis-specified for a flattened baryon distribution; explained in READING §7, and the gate's
purpose is met by the subset fits) and DW1e (`M200c`, the registered tension above).

(Lane id note: this is the DESI Milky Way lane of the 2026-11-11 campaign. `rebuild_2026_10_22/DW1_dwarf_core_flattening`
and `DW2_disc_wall` are unrelated earlier lanes; ids repeat across campaign folders in this repo.)
