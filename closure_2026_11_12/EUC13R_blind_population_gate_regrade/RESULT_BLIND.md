# EUC13R (BLIND RE-GRADE OF EUC13): RESULT_BLIND

2026-11-12. Written before opening any EUC13 file other than FROZEN_CRITERIA.md. TEST lane. kappa = 1/2 FITTED; not
theory closed. Adopts nothing. Reading committed alone at 865ef2116c; code and runs at f02d4bda1d.

## Words (canonical / alt)

- **EUC13-P: NO VERDICT / NO VERDICT.** No member's upper bound is near 0.15; AGEL's and M3's lower bounds sit under 0.25.
- **f25: CEILING BROKEN / CEILING BROKEN.** Every surviving member's lower bound on f25 is >= 0.40 (lowest: M3 alt 0.407).

A population gate grades a modelled source population, not measured sources; it is weaker evidence than row-level
redshifts, and EUC1-F stays the gate that matters. These words are not a pass of anything. The blindness was
incomplete: EUC13's two words were in a commit subject in my start-up context (READING §0), and mine agree with them.

## Members (point, 95 % recentred interval; raw replicate percentiles in euc13r.json)

| member | b_med canonical | b_med alt | f25 canonical | f25 alt | median z_s on P |
|---|---|---|---|---|---|
| M1 AGEL DR2 (N 94, rule A1) | +0.237 [+0.215, +0.264] | +0.219 [+0.195, +0.246] | 0.477 [0.440, 0.515] | 0.449 [0.412, 0.492] | 2.06 |
| M2 SLF IV (N 51, rule S1) | +0.299 [+0.256, +0.341] | +0.282 [+0.231, +0.332] | 0.577 [0.516, 0.638] | 0.549 [0.477, 0.619] | 1.60 |
| M3 envelope (mu 10, full + sis) | [+0.210, +0.248] | [+0.192, +0.227] | [0.436, 0.495] | [0.407, 0.462] | 2.2-2.3 |

M3 per setting (b_med canonical / alt; only mu 10 survives validation, the rest are readings):
mu 3 full +0.302 / +0.286, sis +0.287 / +0.270; **mu 10 full +0.234 [+0.220, +0.248] / +0.214 [+0.202, +0.227], sis
+0.222 [+0.210, +0.234] / +0.204 [+0.192, +0.216]**; mu marginal full +0.277 / +0.259, sis +0.262 / +0.245.
B-fixed readings (full, mu marginal): b = 0: +0.274 / +0.257; b = 0.5: +0.281 / +0.263 (self-consistent +0.277 / +0.259).
Self-consistent B iteration, largest |Delta b| in the third iteration: 0.091 / 0.093 (mu 3), 0.024 / 0.025 (mu 10),
0.025 / 0.025 (mu marginal); not converged to better than that.

## Validation of M3 (sis weight)

- V1 (49 SLF IV systems with a source magnitude; observed median z_s 1.434): mu 3 mixture median 0.972, KS p 1.7e-8,
  FAIL; **mu 10 median 1.288, KS p 0.106, PASS**; mu marginal median 1.103, KS p 2.2e-4, FAIL.
- V2 NOT APPLIED: my own position match (2 arcsec) found 8 ECLIPSE lenses with a published source redshift (3 AGEL,
  2 SLF IV, 0 SLACS, plus EUC2's 3 pairs); 4 are evaluable (L000613, L004966, L013325, L016382). L012826 and L014688
  have no MER flux in the cached tables; L006816 is grade C, not in the key catalogue. Fewer than 5: not applied, so
  mu 10 survives on V1 alone (READING §3). EUC13's own V2 list (14 + 3) was not available to me.
- Surviving settings: mu10_full, mu10_sis. The magnification-bias setting (mu marginal) predicts sources too low in
  redshift for SLF IV's measured sources and drops.

## Known answers and checks (all pass)

KA1 SLACS (70 lenses): +0.0826 / +0.0693 (ref +0.082 / +0.070). KA2 P source-free, N 3,192 (10 removed by the Sersic-n
range): -0.0185 / -0.0439 (ref -0.019 / -0.044). KA3 direct-solve EUC10 recipe on my own parse: AGEL +0.2371 / +0.2189
(ref +0.238 / +0.220), SLF IV +0.2986 / +0.2817 (ref +0.298 / +0.282): all within 0.002, although my parsed samples are
N 94 and 51, not EUC10's 90 and 49 (none of my pre-declared rules gives 90 or 49). KA4 table vs direct: largest
|diff| 7e-5. KA5: max |Delta b| 8.5e-5 / 8.7e-5 on 300 pairs. KA6 COSMOS median lpzBEST at 23.5 < i < 24.5: 1.017
(82,414 galaxies). Analytic: point mass 1e-11; deep-regime point mass against adaptive quadrature 7e-15; PS projection
against direct line-of-sight integral 9e-9; PS against exact 2D Sersic light, 2.6 % at most (reported). Quadrature
240 vs 1200 nodes: 2e-13. No out-of-grid fallback was needed. Mutation twin (a0 = 1e-30): every member's b_med rises
on both footings (e.g. M1 +0.237 -> +0.346, M3 mu10 full +0.234 -> +0.349); exit 1.

## theta_E classes (b_med, point [interval], against EUC5's bands; not EUC5-F)

Classes hold 1,948 / 691 / 553 lenses (< 1.0, 1.0-1.3, >= 1.3 arcsec).

| member | < 1.0 | 1.0-1.3 | >= 1.3 |
|---|---|---|---|
| M1 can. | +0.166 [+0.139, +0.199] inside | +0.280 [+0.252, +0.308] inside | +0.448 [+0.420, +0.478] above |
| M2 can. | +0.232 [+0.187, +0.277] above | +0.333 [+0.289, +0.382] above | +0.493 [+0.454, +0.536] above |
| M3 mu10 full can. | +0.157 [+0.141, +0.173] inside | +0.275 [+0.253, +0.298] inside | +0.455 [+0.428, +0.487] above |
| M3 mu10 sis can. | +0.145 [+0.133, +0.160] inside | +0.267 [+0.245, +0.292] inside | +0.445 [+0.413, +0.476] above |
| M1 alt | +0.148 [+0.121, +0.175] inside | +0.262 [+0.233, +0.289] inside | +0.430 [+0.398, +0.465] above |
| M2 alt | +0.215 [+0.163, +0.274] above | +0.316 [+0.269, +0.363] inside | +0.474 [+0.432, +0.524] above |
| M3 mu10 full alt | +0.136 [+0.122, +0.153] inside | +0.257 [+0.231, +0.278] inside | +0.434 [+0.403, +0.467] above |
| M3 mu10 sis alt | +0.126 [+0.112, +0.140] inside | +0.247 [+0.222, +0.269] inside | +0.427 [+0.396, +0.456] above |

Wide lenses (>= 1.3 arcsec) sit above the sealed band in every member and footing, by 0.1-0.2 dex.

## Disclosed details

- Arc magnitudes: 3,021 of 3,192 P lenses have one (median m_arc 22.69, 16-84 % 21.54-23.55); 171 take donors.
- In the mu 3 settings one lens has an empty n(z | arc) over its support and is dropped from the median (3,191 kept).
- The reported "median_logB" in euc13r.json is nan: the own rows of donor lenses carry no m_arc and are never drawn;
  it does not enter any number above.
- Error realisations use symmetric half-widths for photo-z (70 % width / 2.08), mass, theta_E and theta_e; z floored
  at 0.05. My random streams differ from EUC13's; point estimates will differ at the 0.002-level from draw noise.
- Development: one crash (EUC2 pair L006816 absent from the key catalogue) fixed before any member or validation number was printed (only KA2/KA5 had printed);
  no setting, tolerance or rule was changed after a number was seen.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
