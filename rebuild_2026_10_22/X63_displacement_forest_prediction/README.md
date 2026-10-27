# X63_displacement_forest_prediction: what does X57's M6 (displacement) predict for the high-z Lyman-α forest?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (ddd98ade21, committed alone, before any script or number). One
amendment, A1 (`AMENDMENTS.md`, 4d8ac76f11): after the first run, the implementation check K4 was moved to fixed comoving
k. It cannot change a verdict. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is
a gravitating w ≈ 0 field component, not matter and not a particle. No fitting, no downloads. Not "theory closed".
Nothing here says the data favour the framework. Every number below is from `x63_m6_forest.out` /
`x63_m6_forest_results.json`.

## Verdict (frozen rule): **M6 PREDICTION COMPUTED; TESTABLE AT LEVEL X = 0.39 (ABOVE TYPICAL PER-BIN PRECISION, PROVISIONAL)**

- **Both footings give this verdict, with identical numbers.** X57's forest bound fixes the patches' point variance,
  f_V δ_b,in² = 0.2 σ²_ad(R_L, z = 3), on both footings. Only δ_b,in and F_b differ between them, and they cancel. So M6's
  forest signal carries no footing information. This holds by construction.
- **The record's forest gates do not exclude M6.** X22's `forest_class`, as X4 / X18 / X22 use it, gives **PASS** at the
  bound: the L346 bins sit at 1.014–1.155 (z = 3) and 1.008–1.088 (z = 2), all inside [0.8, 1.2].
- **At the bound, M6 predicts a large excess in the gas 1D power at z = 4.2–5.4.** It peaks at S = R − 1 = 0.26–0.39 near
  k ≈ 0.024–0.028 s/km (R_J = 0.1 Mpc/h). This is 3.9 × a PROVISIONAL 10 % high-resolution per-bin precision, and
  10 × a PROVISIONAL 3 % eBOSS / DESI precision.
- **The prediction is an upper envelope (ledger B3, B5, B6).** The linear, frozen, RSD-free proxy is generous to the
  signal, and the real patches are nonlinear (δ_b,in ≈ 4.3–5.2).

## Step 0 (stop rule): 25 / 25 reproduced (K0)

| item | value |
|---|---|
| X57 M6, canonical | δ_c,in −0.8035, δ_b,in +4.3101, f_V ≤ 0.1883, F_b,max 0.06038 (z = 3) / 0.10560 (z = 2) |
| X57 M6, alt | δ_c,in −0.9731, δ_b,in +5.2196, f_V ≤ 0.1608, F_b,max 0.04822 / 0.08434 |
| X57 recomputed | σ²_ad(R_L 0.4419 Mpc/h, z = 0) 10.597943 and both F_b,max values, relative deviation 0.0. CMB compensated 7.37e-6 |
| X22 forest | k5 4.6199 h/Mpc, T²_5.3keV 0.99519, α_NF 0.02991, λ_hm 0.4167 |
| L346 | bins 1.101–3.557 h/Mpc (six); bins and bands identical to X4 F0a (deviation 0.0) |
| L347 | R_J = 0.1 Mpc/h, read from its script |

## Model (frozen §1–3)

- **M6 as X57 defined it:** compensated patches, δ_c,in = −(1 − f_max) and δ_b,in = 5.364 (1 − f_max), with a frozen
  isocurvature gas mode.
- **Patches:** Poisson-placed top-hats of radius R_L = 0.442 Mpc/h, giving P_iso = f_V δ_b,in² V_p W²(kR_L).
- **Amplitude:** F_b = X57's F_b,max(z = 3). This gives f_V = 0.01137 (canonical) and 0.00775 (alt), far inside positivity,
  and A = 0.07637 (Mpc/h)³ on both footings.
- **Smoothed variance:** the smoothed isocurvature variance at R_L is 0.3238 × the point variance. So X57's bound, which
  compares the point variance with the adiabatic one, is tighter than the forest band. The N2 envelope saturates the band
  on the smoothed variance instead. It is ×3.088 larger and is reported only.
- **Adiabatic part:** X57's BBKS shape with σ₈ 0.82742 and X22's D(z), linear.
- **Gas filter:** exp(−k²R_J²) in power, with R_J = 0.1 Mpc/h (L347's value, PROVISIONAL). Variants 0.05 and 0.2 are
  reported.
- **1D projection:** up to k = 200 h/Mpc. The proxy ratio R = 1 + P1D_iso/P1D_ad.

## Prediction: S = R − 1 (both footings identical; R_J = 0.1 Mpc/h primary)

| z | k = 0.005 | 0.011 | 0.0207 | 0.0455 | 0.1 s/km | max S (at k, s/km) |
|---|---|---|---|---|---|---|
| 4.2 | +0.101 | +0.167 | +0.243 | +0.169 | +0.067 | **+0.261** (0.028) |
| 4.6 | +0.119 | +0.198 | +0.286 | +0.179 | +0.070 | **+0.302** (0.028) |
| 5.0 | +0.139 | +0.233 | +0.332 | +0.187 | +0.070 | **+0.346** (0.024) |
| 5.4 | +0.161 | +0.270 | +0.382 | +0.193 | +0.066 | **+0.395** (0.024) |
| 3.0 (reference) | +0.056 | +0.092 | +0.137 | +0.126 | +0.038 | +0.155 (0.033) |
| 2.0 (reference) | +0.030 | +0.048 | +0.073 | +0.082 | +0.014 | +0.089 (0.033) |

- **Dependence on R_J:** max S at z = 5.4 is +0.328 (R_J 0.05), +0.395 (0.1) and +0.481 (0.2). At z = 4.2 it is +0.218 /
  +0.261 / +0.319.
- **N2 envelope (reported only):** max S at z = 4.2–5.4 is +0.81 to +1.22 (R_J 0.1).
- **Growth toward high z:** at fixed comoving k, S grows exactly as 1/D². S(5.4)/S(4.2) = 1.5109 (K4, amended). At fixed
  s/km the growth is not uniform, because the same s/km maps to a different comoving k at each z.

**Testability (PROVISIONAL precisions, ledger B7; bins = this lane's 20 log points per z):**

| dataset class | bins | max S / σ_PROV | combined S/N | per-bin precision for combined 3σ |
|---|---|---|---|---|
| eBOSS / DESI (z ≤ 4.6, k ≤ 0.04 s/km), σ_PROV 0.03 | 28 | 0.302 / 0.03 = 10.1 | 37.6 | 0.38 |
| high resolution (z 4.2–5.4, k 0.005–0.1), σ_PROV 0.10 | 80 | 0.395 / 0.10 = 3.9 | 19.4 | 0.65 |

The qualifier is ABOVE at all three R_J values, so the result is not UNDECIDED. These S/N values ignore the
thermal-history nuisance (T₀, γ, pressure smoothing). That nuisance is degenerate with small-scale shape and would absorb
part of a scale-dependent excess. The S/N values are therefore optimistic.

## Do the record's forest gates bite on an excess?

- **Which gate pieces see an excess.** In X22's `forest_class`:
  - The upper edges of the L346 band bite on an excess: above 2.0 is FAIL, and above 1.2 blocks a PASS.
  - The other pieces bite only on a suppression: the k5 line (T²(k5) ≥ 0.9), the L319 strict line (T²(k5) ≥ 0.99519),
    and the lower edges (< 0.5 FAIL, < 0.8 no PASS).
  - So the gate constrains an excess only through the L346 bins at k 1.10–3.56 h/Mpc, and only at z = 3 and 2.
- **M6 at the bound:**
  - The bins are 1.014–1.155 (z = 3) and 1.008–1.088 (z = 2), so the gate PASSES.
  - T²(k5) proxy is 1.2065 (z = 3) and 1.1181 (z = 2). That is above the L319 line, which has no upper edge.
  - The N2 envelope's largest bin is 1.478, which would be UNDECIDED, not FAIL.
  - **The graded gates do not exclude M6, even at the envelope.**
- **Reported only, not graded (frozen §4):** L347's P1D line (|R − 1| ≤ 0.10 for k∥ 0.2–2 h/Mpc at z = 3, 2) is
  **exceeded**: M6 gives max |R − 1| = 0.1245. That line is the record's own flux-power gate. L347 itself was BORDERLINE
  (10.8 %, a 0.8-point miss it judged below its method's systematics). M6's 12.5 % sits beyond it, but this lane's proxy is linear,
  not FGPA.
- **Already measured at lower z?** Even at z = 3, M6's 1D signal (S up to 0.155 at k ≈ 0.03 s/km) is large next to the
  few-per-cent per-bin precision the record quotes for eBOSS / DESI. Whether existing z ≈ 3 measurements already exclude
  it depends on nuisance marginalisation, which this lane cannot do without data.

## Deciding datasets (reported only; each **needs an owner-approved download**; nothing was downloaded)

The redshift and k coverages below are from memory and are **PROVISIONAL**. The record holds citation stubs for Viel 2013,
Boera 2019 and Chabanier 2019 under `citations/works/`, but no transcribed P1D values.

1. **HIRES / MIKE P1D at z = 4.2, 4.6, 5.0, 5.4** (Viel et al. 2013, PRD 88, 043502). These are the grid's own redshifts,
   over k ≈ 0.005–0.1 s/km. M6 needs per-bin precision ≲ 0.13 near k ≈ 0.02–0.03 s/km for a ~2–3σ per-bin excess, or ≲ 0.65
   per bin over 80 bins for a combined 3σ.
2. **HIRES / UVES P1D at z 4.2–5.0** (Boera et al. 2019), to k ≈ 0.1–0.2 s/km. Same target.
3. **eBOSS DR14 P1D** (Chabanier et al. 2019): z ≤ 4.4, k ≤ 0.02 s/km. At z = 4.2 M6 gives S 0.10–0.24 there, and a few
   per cent per bin would show it.
4. **DESI DR1 P1D** (FFT and QMLE analyses): z up to ~4.6, k up to ~0.04 s/km. M6 gives S 0.10–0.30 at z 4.2–4.6.
5. **XQ-100 and KODIAQ / SQUAD P1D** (Iršič et al. 2017; Karaçaylı et al. 2022): z to ~4.2–4.6, k to ~0.06–0.1 s/km.
6. **Lower-z cross-check:** the same eBOSS / DESI samples at z ≈ 3. There M6 gives S up to 0.155.

What any of these must deliver: the high-z P1D with thermal nuisance marginalised, compared with an M6-free model whose
small-scale shape is fixed by z ≤ 3 data. The test is a scale-dependent excess that grows as 1/D² toward z = 5.4. M5 (an
object-keyed switch) predicts none.

## Checks

- **Main run: 7/7 PASS, exit 0.** Peak RSS 0.069 GB, one thread, under 0.1 s.
  - K0: Step 0, 25/25.
  - K1: the 1D projection against the analytic Gaussian, 1.1e-7.
  - K2: the M5 null gives R ≡ 1 exactly.
  - K3: sign and positivity.
  - K4 (A1): fixed comoving k, S(5.4)/S(4.2) = [D(4.2)/D(5.4)]², deviation 6.9e-12.
  - K5: units, k(0.01 s/km, z = 5) = 1.378961 h/Mpc.
  - K6: resources.
- **Frozen K4 at fixed s/km (reported):** deviation 1.0. This is the mis-specification disclosed in A1.
- **MUTATE (`X63_MUTATE=1`): exit 1, twin OK.** Exactly K0, K3 and K4 fail, as required; K1, K2, K5 and K6 pass.
  - m1 (sign flipped, patches enriched in cold dark energy): 1 + δ_b,in = −3.31 / −4.22, which is negative baryon density;
    S < 0. The gate then FAILS on L346 < 0.8 and the L319 line.
  - m2 (growing isocurvature mode): the 1/D² scaling is broken, deviation 0.338.
  - m3 (Step 0 target × 1.01): 24/25.

## Files

- `x63_m6_forest.py`: run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x63_m6_forest.py` (twin:
  `X63_MUTATE=1`).
- `x63_m6_forest.out`, `x63_m6_forest_results.json`: normal run.
- `x63_m6_forest_MUTATE.out`, `x63_m6_forest_results_MUTATE.json`: twin (control output, not physics).
