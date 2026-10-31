# RF4_lensing_native_template: two-halo UNSEPARABLE on KiDS and on kSZ. Inside 300 kpc route E's shortfall depends mostly on the gas and the arm: k = 3 is near the data, measured gas is about 2× short, and the no-floor rule reads like the law

Criteria and ledger: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (5632124ef4), committed alone before any script or number. Scripts: `rf4_clones.py`, `rf4_counts.py`, `rf4_far.py`, `rf4_grade.py`, `rf4_ksz.py`. Outputs: `rf4_grade.out`, `rf4_results.json`, `rf4_ksz.out`, `rf4_ksz.json`, `*_MUTATE*`. Scratch sums are rebuilt from fixed seeds and not committed.

## Verdict
**Two-halo UNSEPARABLE, both footings, frozen.** So the lensing grade is R ≤ 300 kpc only, no template. The template lines below are reported, not graded.

The template was built from the sample's own counts, with its amplitude from shear at 3–15 Mpc, and no P(k), σ₈ or growth factor. It failed two of six tests:

| test | result | line | |
|---|---|---|---|
| TS1 detection | a = 5.87 ± 0.95 (M☉/pc² per count/Mpc²), 6.2σ | ≥ 3σ | PASS |
| **TS2 one a for all mass bins** | 5.5 ± 0.9, 1.3 ± 4.3, −7.8 ± 18.8, 22.0 ± 4.6; p 0.003 | p ≥ 0.01 | **FAIL** |
| TS3 scale-independent bias | ρ 0.754 ± 0.026 | within 30 % | PASS |
| TS4 inner exclusion | 0.56σ | < 1σ | PASS |
| **TS5 nulls** | cross 0.44σ; shifted centres max \|z\| 7.0 | < 3 | **FAIL** |
| TS6 implied b_t | 3.94 (at the top of the frozen range) | 0.3–4 | PASS |

**TS5 is partly a test I wrote badly.** It reads E(R), and shifted centres land on a different mean density (offset −1.27 counts/Mpc²), which T doesn't see, since T subtracts a mean. I'd not lean on it. **TS2 is the real failure:** bin 4 sits 3.5σ above the pooled a. The sample's own L − R reported beside it says the same thing: S_strict 8.2 ± 0.9, S_x300 12.2 ± 1.3. A tracer property shouldn't depend on the lens sample. Two reasons are possible and I can't separate them: isolated lenses aren't linearly biased at these scales, or the far signal carries something besides this T.

**kSZ: also UNSEPARABLE.** A(1.8) is 0.59, 0.92, 0.89 at holes of 1, 0.5, 0.25 Mpc (limit 1σ, 0.135), with b/σ_b 0 at 1 Mpc. As expected in the criteria. Graded at θ ≤ 3′.

The verdicts below are not "the framework passes" or "the framework fails": nothing here replaces the ΛCDM-conditioned two-halo with a working clean one. Removing that template didn't change which arm leads. E at k = 3 reads OK on S_strict and S_x300, but only with c_f 4 and closure gas, and it read that way with the template too.

κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Graded: Δ_c = L − I_c, R ≤ 0.31 Mpc, no template, f = 0.28
A = data/model, SI3's estimator. Primary R2, f 0.28. Band: R0 or R2 with f 0, 0.12, 0.28, 0.49. Δχ² = χ²(arm) − χ²(law), same miscentring. D is the separation in σ. Shape p is after fitting one A.

**Canonical**

| arm | sample | A | band | Δχ² (band) | D | shape p | normalisation | shape |
|---|---|---|---|---|---|---|---|---|
| E, k = 3 | S10 | 1.20 ± 0.04 | 0.87–1.81 | −50.1 (−112.7, +24.2) | 5.8 | 0.118 | SHORT | ok |
| E, k = 3 | S_strict | 1.16 ± 0.11 | 0.84–1.74 | −13.3 (−25.4, +3.1) | 2.8 | 0.917 | OK | ok |
| E, k = 3 | S_x300 | 1.16 ± 0.11 | 0.84–1.74 | −17.3 (−29.9, −0.5) | 2.7 | 0.294 | OK | ok |
| E, k = 1 | S10 | 2.19 ± 0.08 | 1.58–3.75 | +188.4 (+151.2, +188.4) | 8.4 | < 0.001 | SHORT | MISFIT |
| E, k = 1 | S_strict | 2.14 ± 0.20 | 1.55–3.61 | +27.0 (+21.9, +27.0) | 3.2 | 0.432 | SHORT | ok |
| E, k = 1 | S_x300 | 2.22 ± 0.21 | 1.60–3.76 | +26.0 (+19.9, +26.0) | 2.9 | 0.183 | SHORT | ok |
| **N** | S10 | 1.45 ± 0.05 | 1.04–2.74 | +40.6 (+34.4, +77.5) | 5.6 | < 0.001 | SHORT | MISFIT |
| **N** | S_strict | 1.43 ± 0.13 | 1.03–2.66 | +2.2 (+0.8, +7.8) | 2.5 | 0.606 | SHORT | ok |
| **N** | S_x300 | 1.47 ± 0.14 | 1.06–2.79 | −2.4 (−2.4, +5.0) | 1.8 | 0.233 | SHORT | ok |
| **Z** | S10 | 1.80 ± 0.06 | 1.30–3.36 | +82.8 (+49.8, +119.9) | 5.2 | 0.025 | SHORT | ok |
| **Z** | S_strict | 1.78 ± 0.16 | 1.28–3.26 | +10.5 (+6.0, +16.1) | 1.9 | 0.871 | SHORT | ok |
| **Z** | S_x300 | 1.79 ± 0.17 | 1.29–3.34 | +8.9 (+4.3, +15.5) | 1.5 | 0.297 | SHORT | ok |
| law, k = 1 | S10 | 1.45 ± 0.05 | 1.05–2.39 | | | | SHORT | |
| law, k = 1 | S_strict | 1.46 ± 0.14 | 1.06–2.39 | | | | SHORT | |
| law, k = 1 | S_x300 | 1.48 ± 0.15 | 1.07–2.44 | | | | SHORT | |

**Alt** (N and Z have no footing; only their Δχ² against alt's law moves)

| arm | sample | A | band | Δχ² (band) | D | shape p | normalisation |
|---|---|---|---|---|---|---|---|
| E, k = 3 | S10 | 1.14 ± 0.04 | 0.82–1.71 | −28.2 (−98.2, +51.5) | 5.9 | 0.041 | SHORT |
| E, k = 3 | S_strict | 1.10 ± 0.10 | 0.80–1.64 | −8.7 (−22.5, +8.9) | 2.7 | 0.879 | OK |
| E, k = 3 | S_x300 | 1.11 ± 0.11 | 0.80–1.66 | −13.2 (−27.0, +3.8) | 2.5 | 0.288 | OK |
| E, k = 1 | S10 | 2.10 ± 0.08 | 1.51–3.60 | +204.2 (+144.2, +207.2) | 9.8 | < 0.001 | SHORT |
| E, k = 1 | S_strict | 2.05 ± 0.19 | 1.48–3.46 | +29.7 (+21.3, +29.7) | 3.7 | 0.374 | SHORT |
| E, k = 1 | S_x300 | 2.13 ± 0.21 | 1.53–3.62 | +28.8 (+19.2, +28.8) | 3.4 | 0.166 | SHORT |
| N | S10 | 1.45 ± 0.05 | 1.04–2.74 | +65.9 (+46.5, +107.2) | 6.3 | < 0.001 | SHORT |
| N | S_strict | 1.43 ± 0.13 | 1.03–2.66 | +6.7 (+6.2, +12.8) | 2.6 | 0.606 | SHORT |
| N | S_x300 | 1.47 ± 0.14 | 1.06–2.79 | +2.7 (+0.3, +10.6) | 1.9 | 0.233 | SHORT |
| Z | S10 | 1.80 ± 0.06 | 1.30–3.36 | +108.0 (+50.2, +149.7) | 6.6 | 0.025 | SHORT |
| Z | S_strict | 1.78 ± 0.16 | 1.28–3.26 | +15.1 (+6.7, +21.2) | 2.5 | 0.871 | SHORT |
| Z | S_x300 | 1.79 ± 0.17 | 1.29–3.34 | +14.0 (+5.7, +21.2) | 2.1 | 0.297 | SHORT |
| law, k = 1 | S10 | 1.33 ± 0.05 | 0.96–2.18 | | | | SHORT |
| law, k = 1 | S_strict | 1.34 ± 0.13 | 0.97–2.18 | | | | SHORT at primary |
| law, k = 1 | S_x300 | 1.36 ± 0.14 | 0.98–2.23 | | | | SHORT at primary |

Normalisation labels are read at the primary point. The bands are wider than the errors, and the low edge is R2 with f = 0.

## Reading
- **Inner normalisation depends mostly on miscentring and the gas.** At f = 0.28 and σ_off 389 kpc, every arm and the law gain about 0.4 in A. The low edge of the band, R2 with f = 0, reaches about 1 for N and the law and 0.87 for E(3). f = 0.28 is another sample's number, applied to lenses selected as isolated, so it's probably high here. That's a limit on the primary point, and I froze it knowing the source.
- **The no-floor rule reads like the law here.** N's A matches the law's within errors on every sample, and it isn't separated from the law on S_strict or S_x300 (D below 3). It loses on S10 (Δχ² +40.6). N's shape misfits S10, and the law's χ² there has p below 0.001 too.
- **The native shape runs about 0.35 shorter than N inside 300 kpc** and isn't powered apart from the law past S10.
- **E at k = 3 is the closest to the data,** and it's the only arm that beats the law in this range on S10. But k = 3 is a gas assumption past R_vir (next section), and E carries c_f 4 EXTERNAL. At measured gas, k = 1, E is the worst.
- **Isolation doesn't change any arm's A inside 300 kpc.** S10, S_strict and S_x300 agree within errors, for all arms.
- **Catalogue noise:** with 8 clones on S10 and 16 on the two strict samples, Δχ² noise for N at R2 over all radii is ±13.3, ±5.2, ±3.6 (from two halves). That's 0.6–0.8× SI3's values on the same three samples.

## kSZ, graded: θ ≤ 3′, f = 0.28, σ_off 389 kpc
GH10's points. e includes the 10 % r uncertainty. Footings don't enter the gas.

| k | A | class | f 0.12 | f 0.49 | reported: all θ, no two-halo |
|---|---|---|---|---|---|
| 1 | 0.90 ± 0.22 | CONSISTENT | 0.74 CONSISTENT | 1.24 CONSISTENT | 0.81 ± 0.20 |
| 1.8 | 0.74 ± 0.16 | CONSISTENT | 0.63 BELOW | 0.96 CONSISTENT | 0.59 ± 0.14 BELOW |
| arms' k*, 1.88–2.39 | 0.74–0.76 ± 0.16 | CONSISTENT | 0.63–0.66 BELOW | 0.95 CONSISTENT | 0.59–0.61 BELOW |

- **A(1.8) BELOW holds only if a neighbour term is ignored and all θ are kept, or at low f.** GH11's "BELOW at realistic miscentring" softens to f-dependent at θ ≤ 3′.
- **k = 3 itself wasn't run in this lane** (frozen rows: 1, 1.8, k*). GH11's reading at f 0.24, all θ, is 0.61 ± 0.13 with mass 7.1e11 M☉, which credits neighbour signal to gas. So the gas that E(3) needs is neither supplied nor excluded here, and that is still the open question for E(3).

## Reported, not graded: the template lines
**TL1's stack, bins 3–4, free b ≥ 0 per bin, this lane's T in place of CFG805's.** "f 0" is the like-for-like comparison with TL1's 66.2 (law, k = 1) and 140.6 (route E, k = 3).

| | law, k = 1 | E, k = 1 | E, k = 3 | N, k = 1 | N, k = 3 | Z, k = 1 | Z, k = 3 |
|---|---|---|---|---|---|---|---|
| canonical, f 0 | 64.8 | 437.9 | 121.4 | 350.8 | 331.9 | 319.0 | 301.1 |
| alt, f 0 | 80.7 | 432.6 | 155.2 | 350.8 | 331.9 | 319.0 | 301.1 |
| canonical, f 0.28 | 136.6 | 562.7 | 117.0 | 453.3 | 433.7 | 455.2 | 436.4 |
| alt, f 0.28 | 115.2 | 552.8 | 115.7 | 453.3 | 433.7 | 455.2 | 436.4 |

- **Swapping CFG805's template for a data-built shape changes TL1's picture little:** 66 to 65, 141 to 121. The law's lead at measured gas stands on this harness.
- N and Z don't get better with more gas, unlike E. They use EM1's masses, so gas doesn't add cold mass. So neither arm ever gets close to E(3) or the law's k = 1 on this statistic. Their crossover k* at 2.2–2.4 comes from the law's getting worse, not from their improving.
- Crossover at f 0.28: E 2.02, N 2.38, Z 2.39 canonical; 1.88, 2.16, 2.17 alt.
- **The fixed-a lines** are in `rf4_results.json`, with a from a test that failed. Over all radii in S10 they read A_O1 about 3 for E(1) and N and A_O2 about 1.1, and shape p below 1e-25 for every arm. So on these lines most of the misfit is the 0.4–1.1 Mpc shortfall, and the S10 lead at those radii remains, as in SI3.

## GH1's matched hosts (template negligible, |a T| below 0.03σ of each bin's stacked mean; its a is −1.09, unreliable, and the term stays out)
20 points, 50–300 kpc. A_h is on the cold halo only. GH1's +0.17 is a log M200 shift, not the same operation.

| arm | canonical χ² | A_h | lg A_h, f 0.12–0.49 | f 0 lg A_h | alt χ² | alt A_h |
|---|---|---|---|---|---|---|
| E, k = 1 | 33.5 | 2.67 ± 0.58 | +0.33 to +0.59 | +0.27 | 33.0 | 2.55 ± 0.55 |
| E, k = 3 | 25.2 | 1.06 ± 0.23 | −0.07 to +0.19 | −0.13 | 25.4 | 0.99 ± 0.21 |
| N | 29.2 | 1.83 ± 0.39 | +0.17 to +0.42 | +0.10 | 29.2 | 1.83 ± 0.39 |
| Z | 31.5 | 2.11 ± 0.46 | +0.23 to +0.49 | +0.17 | 31.5 | 2.11 ± 0.46 |
| law | 27.9 | | | | 27.3 | |

- Every line has p above 0.01 at f 0.28. With f 0, law 27.2, N 25.6, Z 27.6, E(1) 29.2, E(3) 27.7. **This sample doesn't separate them,** as GH1 and GH2 said.
- The shape after fitting A_h is the same for all arms, χ² 24.7–25.8. So the differences are all normalisation.
- N's A_h at f 0 is within 1σ of 1.

## Checks
All K pass: K1 (TL1 numbers), K2 (old clones reproduce +56.55), K3 (lens/I weight in O2 1.016–1.045; cross null lowest p 0.023; halves lowest p 0.215), K4, K5, K6 (G09, GH1 stack, GH10 0.448, GH11 0.542), K7 (0.65 %), K8. **MUTATE bites:** TS1 falls to −0.51σ, χ² of E(1) over all radii on S10, no template, moves from 916.9 to 1166.1, UNSEPARABLE, exit 1.

## Disclosures: fixes after seeing a number
- **K4 first failed,** ratio 0.55 and then 0.585 ± 0.04. I first blamed pixel size and cut it from 0.04° to 0.01°. That moved it little. The real fault was my comparison: ring means against record cells, at different radii. Read at the record cells' radii, it's 0.938 ± 0.041. So the check's frozen limit is unchanged and its method changed after failure. a moved from 5.53 to 5.87 with the pixel change, and TS2 and TS5 failed in both runs.
- **K5 first failed** on inner quadrature, 0.40 against 0.01. Two trapezoid factors fixed it. No grade had been read through that operator.
- **Three crashes** (a namespace, a wrong r₀ bracket, an array shape). r₀ now uses X38's `solve_r0`, as FC1 does.
- The band on ≤ 300 kpc and `law_A_in` were added after seeing the first grades, since the criteria want a band and UNSEPARABLE moved the grade there. No frozen number changed.
- **A criteria wording mismatch:** "tracers with RA shifted" is implemented by shifting the lens centres in the real run, and the tracers in MUTATE.

## Limits
- **Linear bias is an assumption;** that's the piece TS2 doubts. A spectroscopic sample of this N with a measured matter reference would be the clean way, and none is on disk. Measuring b any other way needs a matter P(k) and growth, which needs RF5's native answer. No clean input here.
- **f = 0.28 and its band come from another sample's HOD fit;** G3C's own 0.282 in G09 agrees, but G3C's FoF was tuned on ΛCDM mocks, and neither is an isolated sample. Gaussian offset form assumed.
- **EM1's masses** came from NFW fits with Bullock c(M); they're used in N and Z. Most lenses sit below the 10¹² tag where Z is clamped (KN1), and N's rule below 10¹² is the X80 read.
- E(3)'s gas is a closure assumption past R_vir, and E carries c_f 4.
- Photo-z lenses, no m correction, no n(z), as in SI3. S10 is the record's reconstruction, ×1.15 against B21, and T is S10's applied to B21's stack.
- R2 is an open choice.

## Compute
One thread, `nice -n 15`, at most two lane processes, zooms running. Peak RSS 1.0 GB in clone measurement, 5.7 GB in far-range and counts stages and 1.5 GB in grading; no 1024³ run was live (`compute_queue/status.json`). Wall time about 2.5 hours.

κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
