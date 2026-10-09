# CFG509 — FROZEN CRITERIA: is the KiDS early/late lensing split differential satellite leakage?

**Committed alone, after step 1's photometric companion counts (`cfg509_counts.py`; no shear value is read, only CFG502's per-lens pair weights as stack weights) and before any lensing re-score.**

> κ = ½ is FITTED. Both footings (9.3603e-11 and 1.1312e-10) are scored separately and never pooled. a₀ flat. The cold energy's mass is still required; no particle species is added. Nothing here will say the data favour the framework, and nothing says "theory closed".

## 0. Hypothesis and what is known before this freeze

- **Hypothesis H-SAT:** the re-measured early/late split (CFG95 / CFG505: K1 χ² 35.03/7, 4.40σ, M0 masses, both footings) is largely a selection effect. The "isolated" stack-P sample leaks satellites (CFG502: stack-weighted f_W ≈ 0.17), satellites are preferentially red, and a leaked satellite carries its host halo's off-centre ΔΣ. If the early class leaks more, its stacked signal is inflated.
- **Record numbers read before the freeze:** CFG505 R3 (CFG503's E, nlz, W10, Moster, colour-blind f_W(M*, z), added to both class models of the law): split + E on K1 35.58/7 (4.45σ) and on the inner 9 bins (bins 6–14, R ≤ 0.445 Mpc = 0.3/h) 50.31/9 (5.34σ), canonical, M0. CFG506 (a framework-native environment term) has frozen criteria only (27a6c64ee) and **no committed results**, so no framework-native E is available to this lane; this is stated, not substituted.
- **Step 1 results (model-independent, `cfg509_counts.out`).** More-massive pool companions within R_p < 0.5 Mpc, 10 < |Δχ| < 600 Mpc, minus the area-scaled 4–6 Mpc annulus (CFG502's arrays verbatim; C1 reproduces CFG502's all-lens ratio 0.845):

| class | N | excess per lens, stack-weighted (jk) | unweighted | halo-model pred_sat / pred_2h | λ = (meas − pred_2h)/pred_sat (jk) | f_leak = λ f_W (jk) |
|---|---|---|---|---|---|---|
| late | 93,398 | 0.248 ± 0.006 | 0.272 | 0.369 / 0.031 | **0.589 ± 0.017** | **0.113 ± 0.003** |
| early | 88,079 | 0.257 ± 0.005 | 0.270 | 0.226 / 0.018 | **1.057 ± 0.022** | **0.168 ± 0.004** |
| all | 181,477 | 0.254 ± 0.004 | 0.271 | 0.278 / 0.023 | 0.833 ± 0.016 | 0.143 ± 0.003 |

  - The **raw** per-lens excess is the same in both classes (+0.009 ± 0.007, 1.3σ). But early lenses are more massive, so fewer companions are *more* massive than them. **At matched log M\* and z** (16 cells, common weights) the early excess is **1.53×** the late excess (0.321 vs 0.210), and λ_early/λ_late = 1.75 (1.07 vs 0.61). In 16 of 16 cells the early λ exceeds the late λ (ratio 1.09–4.96).
  - So the counts **do** show differential leakage, without lensing: at fixed M\* and z, early lenses have about 1.5× as many more-massive neighbours within 0.5 Mpc. Converted with CFG502's halo model: f_leak = 0.168 (early) vs 0.113 (late), Δf = +0.055 ± 0.004 (13σ). The record's colour-blind E had the opposite sign (f_W 0.159 early vs 0.192 late, from mass alone).
  - **Conversion caveat (declared):** the count measures (leaked fraction) × (companions per leaked satellite). If early lenses at fixed M\* sit in more massive hosts rather than leaking more often, the count rises too; λ attributes all of it to the fraction. Either reading raises the early class's host lensing; the fraction reading is used.

## 1. Data and machinery (read-only)
- Stack P (181,477 lenses), M0 masses (LePhare + 0.15; the record), CFG505's re-staged per-lens sums (`cfg505_perlens_M0.npz` = `cfg110_perlens.npz`), 50 patches, jackknife covariance of D = ESD_early − ESD_late with Hartlap (NPAT − p − 2)/(NPAT − 1). The law model = CFG261's L-law cell tables (CFG505's prefix loader, verbatim), s = 1, canonical; alt via CFG261's spline at log s = log10(1.1312/0.93603). M2 masses (CFG505) reported.
- **Environment term per lens:** CFG503's `E_moster_nlz_W10` decomposed exactly as E = A + f_W B, with A = HOLE + b_c S2H_nlz (centrals' hole + two-halo) and B = (E − A)/f_W (the leaked-satellite host term per unit leaked fraction). Per lens, the class-dependent term is E_c = A + λ_c f_W B, mapped to g_bar bins with CFG505's `env_perlens` / `cfg495_lenslib.finish` and stacked with WW pair weights, exactly as CFG505 R3.

## 2. Leakage settings
- **L-none:** no environment term (E ≡ 0). The zero-leakage control; must reproduce CFG95/CFG505's split.
- **L-cb:** λ = 1 for both classes (CFG505 R3, colour-blind f_W). Must reproduce CFG505 R3.
- **L-f0:** λ = 0 (centrals' terms only). Reported.
- **L-meas (HEADLINE):** λ_late = 0.589, λ_early = 1.057 (stack-weighted class values above).
- **L-match (reported):** λ_late = 0.613, λ_early = 1.071 (matched cells). **L-unw (reported):** 0.523 / 1.071 (unweighted).
- **L-2sd (reported bracket, favourable to H-SAT):** λ_early + 2 jk SD, λ_late − 2 jk SD.
- **L-lit (reported cross-check, LCDM-CALIBRATED, flagged):** colour-dependent parent satellite fractions f_par,red/f_par,blue = r(M\*), r = 2.0 at log M\* ≤ 10.0, falling linearly to 1.4 at log M\* 11.0 (the trend of SDSS/COSMOS halo-occupation and lensing results, e.g. Mandelbaum+06, Zehavi+11, Tinker+13; **transcribed approximately from memory, not checked against the papers, no download**). The mixture is held to CFG503's f_par(M\*, z) with the red share q(M\*, z) of the ISO lenses; isolation survival uses CFG502's W10 P_s, P_c: f_W,c = f_par,c P_s/(f_par,c P_s + (1 − f_par,c) P_c); λ_c(M\*, z) = f_W,c / f_W.
- **Stripping (reported; CFG503's rule transferred to the law):** the leaked fraction λ_c f_W of each class takes the law's own profile truncated at r_t instead of 0.40 r_ta, with r_t/r_ta = 0.066 (CFG503 C8: median r_t 0.061 Mpc / r_ta 0.926 Mpc at log M\* 10.5, z 0.25), via CFG261's `cells(ls, tfac = 0.066)`. Stripping lowers the more-leaky class's own signal, i.e. it works against H-SAT.
- **Diagnostic (reported, no verdict):** the λ_early that would bring the K1 split below 2σ with λ_late at its measured value (scan λ_early 0–20), compared with the counts.

## 3. Bin sets
- **K1** (bins 8–14; the record's split definition; pair-weighted mean R ≤ 0.251 Mpc for M0) and **inner 9** (bins 6–14; R ≤ 0.445 Mpc = 0.3/h, Brouwer+21's trusted range). Both are "trusted". All 15 bins are reported per bin (D, model D, pull), **outer 6 bins never in a verdict** (CFG503's LCDM validation fails at 1–1.4 Mpc).

## 4. Verdict (frozen; per bin set, per footing)
- σ_res = two-sided normal equivalent of p(χ², dof) of the residual D − (law_early − law_late + E_early − E_late) under the setting.
- **SPLIT EXPLAINED:** with L-meas, σ_res < 2 on **both** footings, on K1 **and** on the inner 9; and the stripping variant also < 2 (else downgraded to PARTLY).
- **PARTLY:** not EXPLAINED, but σ_res drops by ≥ 1.0 relative to L-none on both footings on K1 (the record's split), while staying ≥ 2.
- **NOT EXPLAINED:** otherwise.
- The headline uses L-meas. L-match / L-unw / L-2sd / L-lit are reported; if any of them would change the verdict, that is stated next to the headline (no upgrade of the headline).

## 5. Controls (load-bearing)
- **C1:** L-none reproduces CFG505's M0 T1 split 35.025/7 (canonical, ±0.01) and 35.026 (alt, ±0.05) on K1.
- **C2:** L-cb reproduces CFG505 R3 (M0): K1 35.58 (±0.02) and inner 9 50.31 (±0.05), canonical.
- **C3:** the decomposition A + f_W B reproduces CFG503's E_moster_nlz_W10 table to 1e-9 relative (+1e3 Msun/Mpc² floor).
- **C4:** CFG261's `cells(0, tfac = 0.40)` built in this lane equals the cached base table at s = 1 exactly (machinery for the stripping variant).

## 6. MUTATE (`CFG509_MUTATE=1`, separate outputs)
- **MU1 (swap):** λ_early ↔ λ_late (early 0.589, late 1.057). It must NOT explain the split: σ_res(MU1) ≥ σ_res(L-meas) on both footings on K1 (the swapped leakage must not move the residual toward zero more than the measured one does).
- **MU0 (zero leakage):** L-none = C1 (35.03), and L-f0 reported.

## 7. Limits stated now
- The conversion count → fraction is CFG502's Moster halo model (LCDM-calibrated); host-mass vs fraction is degenerate in the counts.
- The host term B is CFG503's (NFW hosts, satellites distributed like the host, Tinker+05 ζ ξ_NL); stripping for the law is a single median r_t/r_ta.
- No KiDS × GAMA spectroscopic overlap, no MICE mock (need an owner go; not used).
- No framework-native E (CFG506 has no results).
