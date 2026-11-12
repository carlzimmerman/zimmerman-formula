# EUC4 (WIDE LENSES): RESULT

2026-11-12. Criteria 3ef9630a69 (committed alone, before any script or number).

## Verdict: WIDE LENSES BREAK THE CEILING / WIDE LENSES BREAK THE CEILING (canonical / alt)

On 124 grade-B Euclid lenses with Einstein radius ≥ 1.7″, none of which EUC1's map used, 75.8 % [67.7, 83.1]
(canonical) and 70.2 % [62.1, 77.4] (alt) need more than 1.78 × their catalogued Salpeter stellar mass for law S to
make them **with the source at infinity**. The frozen line was 25 %. 99 % need more than Salpeter. The median lens
needs 2.3 × / 2.2 × Salpeter before any real source redshift is applied. Every robustness run keeps the word; the
mutation twin exits 1; both instrument checks pass.

EUC1's post hoc split is confirmed on an independent sample: **the law, acting on the lens galaxy's stars alone,
cannot make Euclid's wide-separation lenses, for any source redshift and any IMF up to 1.78 × Salpeter.**

κ = ½ FITTED. Footings never pooled. One-sided test: no outcome favours the framework.

## 1. Part A numbers (grade B, source at infinity, law S)

| Sample | N | f₂₅ canonical [95 %] | f₂₅ alt [95 %] | b_med canonical / alt | Word |
|---|---|---|---|---|---|
| **W_B: θ_E ≥ 1.7″ (primary)** | 124 | 0.758 [0.677, 0.831] | 0.702 [0.621, 0.774] | +0.364 / +0.343 | BREAK / BREAK |
| Secondary: 1.3″ ≤ θ_E < 1.7″ | 292 | 0.425 [0.370, 0.479] | 0.380 [0.329, 0.435] | +0.207 / +0.182 | BREAK / BREAK (secondary) |
| Complement: θ_E < 1.0″ | 2,045 | 0.092 [0.080, 0.105] | 0.082 [0.070, 0.093] | −0.101 / −0.127 | at the 10 % floor |

Law B supplies less and breaks harder (W_B: 0.831 / 0.798).

W_B medians: z_l = 0.43, θ_E = 1.99″, log M★ = 11.66, θ_E/θ_e = 0.98, n = 5.8. Against the whole sample these lenses
have 2.2 × the Einstein radius and only 0.24 dex more stars.

Grade A, for reference (EUC1's map, the hypothesis): 0.62 for 1.7–2.5″, 0.90 above 2.5″. Wide lenses are 6.0 % of
grade A (192 of 3,192) and 4.2 % of grade B (124 of 2,981).

## 2. Checks

| Check | Result |
|---|---|
| E1 EUC1's primary numbers on P reproduced | 0.156 / 0.139 (pass) |
| E2 identifiers shared by grade A and grade B | 0 (pass) |
| MUTATE newton | f₂₅ on W_B 0.758 → 0.968 and 0.702 → 0.968; exit 1 |

## 3. Robustness (W_B, law S; f₂₅ canonical / alt)

| Run | N | f₂₅ | Word |
|---|---|---|---|
| R_e × 0.80 | 124 | 0.669 / 0.629 | BREAK |
| n = 4 | 124 | 0.766 / 0.718 | BREAK |
| SIE Einstein radius ≥ 1.7″ | 125 | 0.744 / 0.696 | BREAK |
| z_l < 1.0 | 118 | 0.763 / 0.703 | BREAK |
| r_max = 300 kpc | 124 | 0.766 / 0.718 | BREAK |
| threshold 1.5″ | 238 | 0.655 / 0.601 | BREAK |
| threshold 2.0″ | 59 | 0.831 / 0.814 | BREAK |

The lowest lower bound in the table is 0.534 (threshold 1.5″, alt), twice the line.

## 4. Part B (EXPLORATORY; no verdict): could group gas rescue the law?

316 wide lenses (192 grade A, 124 grade B). Stars plus a β = 2/3 gas body cut at 500 kpc; law S; the gas mass inside
500 kpc at which the law supplies the lens.

| Core radius | Source | Stars | Median gas mass needed (canonical / alt) | Gas / stars | Fraction above 4 × 10¹² M☉ |
|---|---|---|---|---|---|
| 30 kpc | infinity | Salpeter | 2.8 / 2.3 × 10¹³ M☉ | 52 / 46 | 0.98 / 0.96 |
| 30 kpc | infinity | 1.174 × | 2.3 / 1.9 × 10¹³ | 46 / 38 | 0.93 / 0.90 |
| 30 kpc | z_s = 3 | Salpeter | 4.5 / 4.0 × 10¹³ | 86 / 76 | 1.00 / 1.00 |
| 100 kpc | infinity | Salpeter | 6.9 / 5.9 × 10¹³ | 131 / 113 | 0.99 / 0.98 |
| 100 kpc | infinity | 1.174 × | 5.6 / 4.7 × 10¹³ | 112 / 93 | 0.96 / 0.93 |
| 100 kpc | z_s = 3 | Salpeter | 1.2 / 1.0 × 10¹⁴ | 222 / 195 | 1.00 / 1.00 |

X-ray groups with massive central galaxies hold about 1–4 × 10¹² M☉ of gas inside R₅₀₀ (quoted from memory of the
group scaling-relation literature; PROVISIONAL; orientation only). The law would need **10 to 30 times more**, the gas
content of a rich cluster, around galaxies whose lensing corresponds to a velocity dispersion near 270–310 km/s. With
a 100 kpc core and the source at infinity the medians inside R_E are: stars 482, projected gas 350–412, the law's
cold pull 646–707, needed 1,514 M☉ pc⁻². Extended gas adds little cold pull at 12 kpc, so it is an inefficient rescue.

Only 0.3–4 % of the wide lenses need no gas at all. The catalogue has no environment measure, so nothing here says
these lenses are or are not in groups. It says that if they are, ordinary group gas under the same law is not enough.

## 5. What this means

1. **A hypothesis from our own exploratory map was put to an independent sample and held.** It is adverse to
   "law + the lens galaxy's stars". It needs no source redshift and no IMF assumption below 1.78 × Salpeter.
2. **The Euclid lens population splits by Einstein radius.** Below 1″ (two thirds of the lenses) the fraction above the
   ceiling is at the contamination floor, 8–9 %: those lenses are not excluded without source redshifts, and EUC3 /
   EUC1-F will decide them. From 1.3″ up the ceiling is broken, 38–43 % then 70–76 %.
3. **The extra mass cannot be the law's own response to group gas.** Part B: short by a factor of 10–30. So the wide
   lenses need gravitating density beyond the law's saturating cold pull, inside about 12 kpc, in systems of group
   scale. EUC1's map sized it at +600 to +900 M☉ pc⁻² of mean surface density inside R_E (grade A, source at infinity).
4. **For the framework this is the cluster residual reaching down to galaxy-group lenses.** Assertion (O), "no second
   halo", holds here only if these systems are counted with the clusters, where the framework already carries a cold
   component beyond the law and has no constructed state for it (CLS1). EUC4 gives that missing state a number to
   meet at the small end: at least a few hundred M☉ pc⁻² inside 12 kpc around galaxies of log M★ ≈ 11.7.
5. **It does not test a₀, κ, or clusters proper**, and it says nothing about the two thirds of lenses below 1″.

## 6. Files

`euc4.py`, `euc4.out`, `euc4_results.json`, `euc4_per_lens.csv` (the 316 wide lenses),
`euc4_MUTATE_newton.out` / `_results.json` (exit 1). EUC1's code is imported from
`../EUC1_eclipse_saturation_ceiling/euc1.py`. Data as EUC1 (hash-checked on every run).
