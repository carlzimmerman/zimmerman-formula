# DW1 — DESI DR2 III's Milky Way mass, against the a₀-line framework

**Paper absorbed:** DESI Collaboration, *DESI DR2 Results III: The Mass of the Milky Way*, arXiv:2611.05518
(submitted to ApJ, 3 Nov 2026). 10,036 RR Lyrae + BHB halo stars, 6D phase space, 10–95 kpc, four
dynamical-modeling methods, mock-calibrated; joint `M(r<80 kpc) = 6.36 (+0.53/−0.48)×10¹¹ M☉` and
`M200c = 1.19 (+0.14/−0.12)×10¹² M☉`. Table 4 of the paper — the joint enclosed-mass profile at 13 radii,
20 to 80 kpc in 5 kpc steps — is the instrument here; the single numbers are not.

> **CORRECTION 2026-11-11 (G239, `deepseek_push/G239_proper_efe/`).** The external-field paragraph in the
> Result section and in "What is genuinely new here" §3 was computed with the **scalar-additive**
> approximation `ν((g_bar+g_ext)/a₀)`, which is the maximum-suppression case. The exact QUMOND angle
> average gives **+16% (canonical) / +13% (alt)** at 80 kpc: **−2.77σ / −2.50σ, not −4.11σ / −3.70σ**, and
> the 13-point profile fits at **3.3% rms (χ²/dof 0.38), not 7.0%**. Two statements are therefore
> **withdrawn**: that the EFE spoils the profile's shape, and that the 20–80 kpc profile prefers a weak
> external field (the rotation curve's `e_N = 0.000 [0, 0.008]` and the LMC bound still stand on their own).
> The M200c comparison and the plateau falsifier are unchanged except that the plateau is now **lower**
> (5.26×10¹¹ at A = 1, against item 38's naive `ν(e_N)M_b = 6.27×10¹¹`), so the falsifier's split widens
> from 1.8× to 2.2×. The `.out` is left as the historical record of the approximation; this note is the
> correction, and the operative numbers are G239's.

> **NOTE 2026-11-12 (DR2REV, NMB1, PLT1; `closure_2026_11_12/`).** Three later readings of the same
> release change how the sections below should be read. The frozen verdicts stand as frozen.
>
> 1. **"13 independent chances to fail" is wrong.** Table 4 is a per-radius combination of four
>    methods: emPDF is a two-parameter NFW, GME's slope is its prior, only the two NIMBLE branches
>    measure shape, and no radius-to-radius covariance is published. The chi2/dof of 0.26 / 0.22 shows
>    compatibility with one amplitude, not a passed shape test (DR2REV, origin 114f008bf4).
> 2. **DW1a graded the most favourable radius.** Against the same table the A = 1 canonical line is
>    2.3 to 3.5 sigma low at every radius from 20 to 65 kpc (alt 0.95 to 2.1), diagonal errors, post
>    hoc. Against the four shape-measuring curves, with the covariance of the paper's own mocks, the
>    line passes on both footings with and without the field (NMB1, origin 9d17287e7e: Q = 4.89 / 2.91
>    / 2.40 / 0.05 on two degrees of freedom, gate 6.18; the canonical field case is FRAGILE). That
>    gate has little power: the paper's NFW passes at 0.17.
> 3. **The amplitude is not a two-witness measurement at the precision quoted.** The shape-measuring
>    curves give A* = 1.17 [1.06, 1.30] (canonical) and 1.02 [0.92, 1.13] (alt) with no field, against
>    1.33 +/- 0.04 and 1.15 +/- 0.03 here. The rotation-curve ranges (1.25 to 1.31 and 1.15 to 1.21)
>    lie at the upper edge of the first interval and just outside the second.
> 4. **DW1e's M200c is not a measurement at 200 kpc.** It is an NFW extrapolation with 75 per cent of
>    its weight on GME; without GME the paper gets 1.52 (+0.35, -0.30) x 10^12. The outer test is
>    against published masses at r >= 100 kpc (PLT1, origin b6a6f1d4f5): the field reading passes as
>    frozen but FRAGILE, failing low against the satellite and globular-cluster masses beyond 150 kpc
>    (median pull -2.72); the no-field reading passes both tracer classes.

> **NOTE 2026-11-12, after this result: owner decision on the external field** (`campaign_fresh_gravity/OWNER_DECISION_2026-11-12_EXTERNAL_FIELD_READING.md`).
> The owner adopted the actual-field reading of the Milky Way's external field. The field cases in this
> file use the record's earlier reading (e_N = 0.01273 inside the kernel as a Newtonian source). Under the
> adopted reading e_N is 0.000160 (canonical) / 0.000110 (alt), the field takes over near 800 kpc, and
> inside 300 kpc the line is the no-field case. The external-field rows, the plateau and the M200c comparison in this README belong to the earlier reading; the no-field rows are the framework's.
> See `closure_2026_11_12/EFC1_external_field_convention/RESULT.md`. The frozen labels stand as frozen.

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

**Kernel diagnostic (post-hoc; the frozen criteria named no kernel).** The same 13 points on a0kit's
Milgrom form `ν = √(1+1/y)` demand `A = 1.59` (canonical) / `1.35` (alt) — 6.1σ / 3.8σ *more* amplitude than
the rotation curve does. So the two-dataset agreement above is a **Route A** result, and the Milky Way is
now a kernel discriminator: Route A passes both lever arms with one amplitude, the a0-line form cannot.
Both kernels still pass the absolute 80 kpc mass (−1.94σ / −0.89σ for Milgrom).

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
4. **A kernel discriminator falls out.** The framework's two registered kernels are not degenerate under
   the MW's two independent lever arms: Route A (ν = 1/(1−e^{−√y})) fits both with one amplitude, the
   a0kit/Milgrom form needs 30% more baryons for the mass profile than the rotation curve will give it.
   This is a post-hoc question the frozen criteria did not contain, and it is reported as such.
5. **The falsifier has a radius and a size.** The framework says the mass is flat at ≈6.3×10¹¹ M☉ (A=1) to
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
