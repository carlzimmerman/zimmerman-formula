# RF2_ic1613_inclination_footing: FROZEN CRITERIA (committed alone with ASSUMPTION_LEDGER.md, before any script or RF2 number)

Written 2026-10-31 under THEORY_PROGRESS_SUMMARY_2026-10-31.md section 3 and section 4 (RF2). κ = ½ FITTED. Footings graded
separately, never pooled. Not "theory closed". No download. **No new falsifier is frozen here; IN1's stands.**

**Disclosed first.** I have read IN1, IN2 and Taibi+24's section 6.2 and Table 1. So I already know: MUSE 36 ± 11 and
32 ± 11; ε 0.20 ± 0.05 with arccos(1 − ε) ≈ 37°; optical PA 90 ± 1 against HI PA 72 ± 2 (Oh+15 73.7); Lake & Skillman 38 ± 5, second-hand;
Read+16 39 ± 2 as adopted in Taibi's Table 1; Oh+15 48 ± 0 fixed. I have also looked by eye at the moment-0 panel of Oh+15's Fig. A.55
(about 3 by 3 inches, binary mask). I have computed no axis ratio from it.

## Question

How much of IN2's failure rests on the Read+16 stellar-kinematic inclination?

## (a) The law across i

IN1's model, unchanged: the law, IN1's masses, σ, r₁₂, HI V_rot, s (0.0792 σ tracer, 0.075 HI). i from 15° to 50° in 1° steps. E and Z for both tracers, q_σ
0.4, 0.6, 0.8, both footings. **Check against IN1's band** I_HI [18.5, 26.5] canonical, [18.0, 25.0] alt.
Verification of the fail (reported): the band if M★ = X1/LVD's 1.9e8 instead of LT's SED 2.88e7, and at s ± 0.01.

## (b) Rows: inclination estimates

| row | value | class | use |
|---|---|---|---|
| MUSE Read+16 formalism | 36 ± 11 | STELLAR-KINEMATIC, no mass model; assumes shared v_circ, exponential tracers. Comparator being replaced | MUSE row |
| MUSE Weijmans+08 formalism | 32 ± 11 | as above; core radius from HI | MUSE row |
| **Optical isophote** | ε 0.20 ± 0.05 (Higgs+21, via LVD and Taibi Table 1) | PHOTOMETRIC, no dynamics | **QUALIFYING** |
| **HI morphology** | measured here from Oh+15 Fig. A.55 panel (a), the moment-0 panel on disk | RENDERED MAP, no dynamics | **QUALIFYING** |
| Lake & Skillman 1989 | 38 ± 5, read only via Taibi+24 | HI, low resolution, PROVISIONAL (method mixes kinematics and isophote argument, paper unread) | **QUALIFYING**, flagged |
| Oh+15 tilted ring | 48 ("± 0": held fixed, no usable error) | HI KINEMATIC | central value only, no probability |
| Read+16 39 ± 2; 15° | mass-model fits with a halo | **ΛCDM-PROCESSED** | BRACKET, never counted |
| Collins & Read 2022 ~20° | set by requiring the BTFR | **CIRCULAR for this question** | BRACKET, never counted |
| TRGB geometry | not on disk | | row says NOT ON DISK |

**Optical isophote, forward model.** Prior flat in cos i, as Taibi's. Disc thin. Intrinsic oval e_int with the node at uniform angle
φ; apparent axis ratio from the singular values of diag(1, cos i) R(φ) diag(1, 1 − e_int). Likelihood N(ε; 0.20, 0.05). **PRIMARY e_int = 0.10**
(declared; dwarf discs are not circular, and the 18° PA offset above says this one is not a thin circular disc. Unsourced on disk, PROVISIONAL).
Reported: e_int 0, 0.05, 0.15, 0.20. Separately, for e_int = 0, intrinsic thickness q₀ 0, 0.2, 0.4, 0.6 by cos²i = ((1−ε)²−q₀²)/(1−q₀²). Central = posterior median; half-width = half the
16–84 % range.

**HI morphology, method.** Render panel (a) from the PDF's own raster (no rescale). Panel box from its frame. Mask = HI-coloured pixels. Remove pixels with fewer than 2 mask neighbours
(isolated specks). Take the largest connected body at 3-pixel dilation, and fill it. Second moments of the filled region: b/a = √(λ₂/λ₁), PA. ε_HI = 1 − b/a.
Error: pixel-block bootstrap (200 draws, seed 0) ⊕ half the spread across three variants (raw mask without fill; dilation 2; dilation 5). Same posterior machinery as the isophote, with e_int 0.10. The
footprint is a binary mask at about 72 ppi with holes; it may be cut by primary beam or S/N. **Check K4:** panel scale from axes gives a footprint diameter within a factor 2 of Oh+15's HI extent if on disk,
otherwise flagged. **Check K5:** the method recovers an injected ellipse b/a 0.80 at PA 70° on the panel grid within 0.02 and 3°.

## (c) Likelihood of IN1's band

For each row, P(i ∈ [18.5, 26.5]) (canonical; [18, 25] on alt): truncated normal on [0, 90] for quoted ± rows, posterior mass for the forward rows. Also the ratio of the row's density
at band centre 22.5° to its peak.

## Verdict (frozen)

Row **FAILS** iff its central value ≥ 30° (IN1's falsifier). Row **CONSISTENT** iff central value is inside the band. Otherwise **BETWEEN**. "Precise" = half-width ≤ 10°.
Only QUALIFYING rows, primary settings.

1. No precise qualifying row: **UNDETERMINED (no independent inclination better than ±10°)**.
2. Precise qualifying row(s), and every qualifying row FAILS: **FAILS under every halo-free inclination**.
3. No qualifying row FAILS, while a MUSE row does: **FAILS only under the MUSE kinematic value**.
4. Any other mix: **MIXED**, listing the rows. (Added; the summary lists three classes and does not cover this one.)

Per footing. **Word rule:** "FAILS" means IN1's frozen falsifier is met. It does not mean excluded. The band's probability under each row is always printed next to it, and at the largest e_int that keeps FAILS.
Answer the question directly: if the MUSE rows are removed, does the class change?

## Checks

- **K0:** IN1's HO3 −0.5352 and RT1 −0.5928 reproduce; **K1:** band reproduced for both footings at q 0.6.
- **K2:** forward model at e_int = 0 and σ_ε → 0.001 returns arccos(0.8) within 0.5°. **K3:** P(band) integrates to 1 over the full i range.
- **K4, K5:** above. **K6:** RSS < 1 GB.
- **Rerun** byte-identical. **MUTATE (`RF2_MUTATE=1`, separate outputs):** arcsin in place of arccos in the thin-disc row and sin/cos swapped in the projection; K2 must FAIL, exit 1.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf2_ic1613.py`.

Rule 7 applies. Nothing here says the data favour the framework.
