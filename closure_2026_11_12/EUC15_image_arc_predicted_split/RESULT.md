# EUC15 (IMAGE-ARC PREDICTED-SPLIT SOURCE REDSHIFTS): RESULT

2026-11-12. Criteria 176eefd3d1 (alone, before any VIS pixel of a lens or grade-X system other than the truth lens was
fetched). EUC14's rule is imported unchanged; the only new input is each system's arc, measured from its VIS image.

## Verdict: EARLY READING, NOT A GATE / EARLY READING, NOT A GATE (canonical / alt). EUC1-F is not graded.

**N(P) = 5** lenses with a certified source redshift; EUC1-F needs 10. That count decides the word. All checks pass
and both twins exit 1. The frozen fallback tier TB passes every gate (grade X 0 of 210, rotated 1, sign-flipped 1,
truth recovered); the primary tier TA fails three nulls (grade X 4 against 1.1, rotated 4 and sign-flipped 6 against
2.8). The four line-identity readings give the same word.

The image arcs triple the evaluable lenses against EUC14 (S 536 against 178), and at TB lenses now separate from
non-lenses (11 of 536 against 0 of 210). But only one lens in four has its brightest residual far enough along the
dispersion to predict a split, so P still falls short. κ = ½ FITTED. No outcome favours the framework.

## 1. Coverage and checks

| | usable spectrum | VIS box | image arc | median arc radius / θ_E | **evaluable** (half-split ≥ 30 Å) |
|---|---|---|---|---|---|
| S | 2,260 | 2,260 | 2,259 | 0.61 | **536** |
| X | 923 | 923 | 918 | 0.62 | **210** |
| P | 1,164 | 1,164 | 1,164 | 0.71 | **311** |

K1 −0.0185 / −0.0439; K2 +0.2314 / +0.2149; K5 20 of 20; K6 19,030 of 19,033; K7 S and X; C1 reproduced: all pass.
Injections into 300 evaluable S: I1 278 (92.7 %); I2 a centred line 1 (0.3 %); I3 the mirrored shifts 0.
**Twins:** newton exits 1 (anchor +0.330 / +0.330 against +0.231 / +0.215; P rose on both footings). nowindow exits 1:
(system, variant) pairs with a TA candidate before identity and guards rose from 106 to 437.

## 2. Gates

| Tier | P | S (rate) | X (limit) | rotated 90°, S (limit) | sign-flipped S | mirrored S | truth | |
|---|---|---|---|---|---|---|---|---|
| TA | 7 | 14 (2.6 %) | **4 (1.1): FAIL** | **4 (2.8): FAIL** | **6 (2.8): FAIL** | 6 | recovered | fails |
| TB | 5 | 11 (2.1 % [1.0, 3.6]) | 0 (1.0) | 1 (2.2) | 1 (2.2) | 0 | recovered | **all pass** |

Truth lens L015763 (box identical to EUC14's cutout): arc (−1.10, −1.11)″, z_s 1.3649 (DESI 1.3657), k = 1.05,
S/N 51.6. This is necessary, not independent: EUC9's and EUC14's results were known.

At TB grade X gives 0 of 210 (95 % upper bound 1.7 %), against 2.1 % for lenses. At TA the four grade-X hits (all
single lines; two of them EUC14's L023203 and L026011) match the lens rate, and the rotated and sign-flipped nulls fail
too: TA's thresholds admit noise.

## 3. Certified at TB (each line on the predicted side in both grism positions; `figs/euc15_secure_*.png`)

| Lens | in P | line | z_s | k | half-split | S/N | z_l | b canonical / alt |
|---|---|---|---|---|---|---|---|---|
| L001890 | yes | Hα (one line) | 1.0363 | 1.20 | 1.31″ | 13.5 | 0.640 | +0.851 / +0.838 |
| L001520 | yes | Hα (one line) | 1.2292 | 1.00 | 0.69″ | 13.0 | 0.970 | +0.688 / +0.679 |
| L001449 | yes | Hα (one line) | 1.5782 | 1.25 | 0.90″ | 14.9 | 0.860 | +0.589 / +0.574 |
| L012745 | yes | [O III] + 4960 (5.5 σ) | 2.1855 | 1.05 | 2.63″ | 14.2 | 0.350 | +0.405 / +0.385 |
| L001971 | yes | [O III] + 4960 (8.3 σ) | 2.4677 | 0.90 | 0.79″ | 29.3 | 1.060 | +0.151 / +0.134 |

Also in S (grade B, not P): L011858 [O III] 2.5052; L012019 [O III] 2.6095; L013774 [O III] 2.0089; L014252 [O III]
1.5139; L004590 Hα 1.3914; L016686 Hα 1.6987. L001971 and L011858 repeat EUC14 from an independent arc input.
EUC14's L015301 is not certified here: its brightest residual is not its catalogued arc.

## 4. Early reading (not a gate)

| P, N = 5, law S | canonical | alt |
|---|---|---|
| single lines as Hα (primary) | +0.589 [+0.151, +0.851] | +0.574 [+0.134, +0.838] |
| single lines as [O III] 5008 | +0.405 [+0.151, +0.613] | +0.385 [+0.134, +0.596] |
| single lines as [O II] 3727 | +0.326 [+0.117, +0.511] | +0.304 [+0.097, +0.491] |

The [S III] reading equals Hα: it would put every single-line source below z_up + 0.15, so it is excluded.
S, N = 11: +0.405 [+0.061, +0.589] / +0.385 [+0.042, +0.574]. Source-free P: +0.145 / +0.117. Robustness rows:
two-line classes only (P, N = 2) +0.278 / +0.260; with AMBIGUOUS-OWN (P, N = 16) +0.322 [+0.160, +0.459] / +0.302
[+0.142, +0.444]. Five lenses make no gate. Three of five are single lines, and the interval moves by 0.26 between
identities.

## 5. What this means

1. **The geometry generalises.** An arc found blind in the image predicts the shift in both grism positions for 11
   lenses, and at TB, with every null clean, no grade-X system is certified. The prediction now carries information
   that a 1D spectrum alone (EUC9) did not.
2. **The binding limit is geometric, not purity.** 2,259 lenses have an image arc, but only 536 lie at least 0.67″
   along their field's dispersion. DR1 observes each field at nearly one roll angle, so an arc across the dispersion
   cannot be predicted. The circular lens model also puts the brightest residual near the inner edge of the annulus
   (median 0.61 θ_E), which shortens predicted splits.
3. **N(P) = 5; EUC1-F stays open; EUC1 stays NO VERDICT / NO VERDICT.** Reaching 10 needs about twice the evaluable
   P: later releases with more roll angles, or a better arc finder frozen in a new lane. Single-line identity would
   then decide much of the word. (The launching session's estimate, N(P) near 20, was high by a factor of 4.)

## 6. Disclosures

- Seen before freezing: EUC14 in full, including that its `anyk` twin exited 2 (criteria §6).
- **Network.** ESA TAP (mosaic list). One IRSA request testing multi-range support returned the whole mosaic: 144 MB,
  stopped by a timeout and deleted unopened. Boxes came from the public AWS Open Data bucket by single byte ranges:
  about 66 MB, so about 210 MB for the lane against a 300 MB cap. Hash manifest outside git.
- Fetch only (no pixel or rule touched): repeated read timeouts on eight connections, resumed with four; later stopped
  when the shared disk filled with other sessions' files, resumed at 6.5 GiB free; the 1,759 earlier boxes intact.

## 7. Files

`euc15_fetch.py`, `euc15.py` (imports `euc14.py`), `euc15_figs.py`; `euc15.out`, `euc15_results.json`,
`euc15_sources.csv`, `euc15_MUTATE_*`, `figs/euc15_secure_*.png`. Boxes outside git (`_external_data/.../euc15/`).
Commits (local / origin): criteria 176eefd3d1 / be6185dbb6; scripts and run b272af9768 / 7db33d8cda; result 076321f1fd / 7d77a8282c.

    python3 -I euc15.py --data-dir <dir>;  EUC15_MUTATE=newton|nowindow python3 -I euc15.py --data-dir <dir>  (twins exit 1)
