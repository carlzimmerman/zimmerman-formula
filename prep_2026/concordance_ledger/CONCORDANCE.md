# CONCORDANCE — one Planck-fixed acceleration, every independent band, every null
**Lane C combine.** 2026-07-16. All numbers below computed by `concordance.py` (exit 0) or the
lane scripts in this directory; frozen repo read-only; primary sources cited on every bound.

## THE HONEST CEILING (read this first)
This ledger demonstrates **consistency plus parameter economy — not proof, not validation.**
Its strongest true statement: one number derived from Planck's Λ with zero galaxy input,
`a0 = cH_Λ/Z = 9.355e-11 m/s²` (formal width <1%), sits **inside every independent positive band**
(gas kinematics; lensed photons; a shape-free global scaling) **with zero per-object freedom**,
while every high-precision null it must pass, it passes — two by computed suppression (~4 and ~7
orders), two by exact structure. What it does **not** do: the galaxy bands are wide
(baryon-budget and M/L systematics, stated as wide) and **cannot separate** 9.355e-11 from
1.131e-10 from the conventional fitted 1.2e-10 — joint Δχ² between all three candidates is
< 1 (computed below). The anchored values are distinguished by **provenance** (fixed before any
galaxy is looked at), not by a tighter posterior. ΛCDM fits the same positive probes **well**
with per-object halo freedom — the raw AIC/BIC on one dataset can favor it (computed below,
not hidden); what AIC/BIC on one dataset cannot price is that the framework's single number is
simultaneously hostage to four probe classes and four nulls. The Z in the anchor is fixed by
the dS-Unruh construction but its **value remains postulated** (κ-closure banked): the ledger
tests the number, not its pedigree. The wide-binary row is **pending** (Gaia DR4) and can still
hard-kill the premise. Fitted g† values are never compared across ν conventions; every fit here
uses the framework's own ν(y)=√(1+1/y).

![crossing figure](concordance_crossing.png)

## 1. Anchor (both footings, `anchor_planck_a0.py`)
| footing | a0 | width |
|---|---|---|
| CANONICAL ρ_DE/cH_Λ | (9.355 ± 0.090)e-11 m/s² | 0.96% (ρ-bracket 0.27–1.33%) |
| ALT ρ_total/cH0 | (1.1305 ± 0.0091)e-10 m/s² | 0.80% |

## 2. The crossing — joint consistency per footing
Bands (systematics envelopes): P1 kinematic [7.755e-11, 2.005e-10] · P2 photon
[7.234e-11, 3.283e-10] · P3 BTFR [8.686e-11, 1.549e-10]. One global Υ
must serve P1 and P3 simultaneously (co-movement enforced); P2 is independent (photons).

| candidate a0 | P1 | P2 | P3 | co-moving Υ* | P1 penalty @Υ* | P3 z @Υ* | joint χ² |
|---|---|---|---|---|---|---|---|
| CANONICAL cH_L/Z = 9.355e-11 | INSIDE | INSIDE | INSIDE | 0.80 | 0.09% | +0.19σ | 0.04 |
| ALT cH0/Z = 1.131e-10 | INSIDE | INSIDE | INSIDE | 0.66 | 0.39% | +0.01σ | 0.00 |
| conventional 1.2e-10 = 1.200e-10 | INSIDE | INSIDE | INSIDE | 0.61 | 1.52% | +0.07σ | 0.01 |

**Separation, stated honestly:** Δχ²(canonical−alt) = +0.04; Δχ²(canonical−conventional
1.2e-10) = +0.03. All three candidates thread all three bands; **the ledger cannot
separate them.** The distinguishing content of the anchored values is that they were **derived
from Planck's Λ before looking at any galaxy**. Stat-only lensing "rejects" *every* candidate —
canonical at +11.1σ from B21's cold-baryon budget and
+4.5σ from B21's own hot-CGM budget, conventional 1.2e-10 at
+8.2σ/+11.4σ —
which is exactly why the P2 band is a published-baryon-budget envelope, not an instrument limit.

## 3. Null table — the framework must predict ~zero where the best instruments see zero
| null | framework prediction | measured bound (primary source) | margin (canon / alt) |
|---|---|---|---|
| **N1 ephemerides (Cassini Q2)** | MI l=2: 7.4e-34 / 1.1e-33 s^-2 (DC a0/2g absorbed into GM_sun) | Q2 2-sigma ceiling 5.2e-27 s^-2 (Park+ 2026 arXiv:2602.17884; DHF24 MNRAS 530,1781) | PASS 6.8 / 6.7 orders; MG-read of the SAME a0 = 3.3e-23 -> EXCLUDED 3.8 orders |
| **N2 LLR (mm ranging)** | observable MI channel (a0/2g)^2 = 3.0e-16 / 4.4e-16 (DC absorbed into GM_earth) | fractional sensitivity 2.6e-12 (APOLLO; Murphy 2013 RPP 76, 076901) | PASS 3.9 / 3.8 orders |
| **N3 MICROSCOPE WEP** | eta = 0 EXACTLY (universal inertia rescaling; no composition channel; footing-independent) | eta(Ti,Pt) = (-1.5 +/- 2.3)e-15 (Touboul+ 2022 PRL 129, 121102 final) | PASS: exact zero sits 0.65 sigma from the measurement at 1e-15 precision |
| **N4 CPT / photon k_AF** | k_AF = 0 EXACTLY (SME bridge: horizon induces CPT-EVEN s_munu only) | abs(k_AF) < 1e-44 GeV (Kostelecky-Russell RMP 83,11, 2023 tables) | PASS by structure; CPT-ODD sibling scale hbar*H = 1.19e-42 / 1.44e-42 GeV sits 119x / 144x ABOVE the bound -> that variant is DEAD |

## 4. Parameter economy on the SAME 175 SPARC curves (`concordance.py`, N = 3388 points)
Gaussian-error χ², AIC = χ²+2k, BIC = χ²+k·ln N (constant terms identical across models).
a0 is charged to the framework as **zero** fitted parameters because it is fixed externally by
the CMB; even charging it as one global parameter adds only +2 (AIC) / +8.1 (BIC) and
changes nothing below.

| model | k (free params) | χ² | χ²/N | AIC | BIC |
|---|---|---|---|---|---|
| framework, canon a0 (external) + 1 global U | 1 | 149286 | 44.06 | 149288 | 149294 |
| framework, alt a0 (external) + 1 global U | 1 | 139225 | 41.09 | 139227 | 139233 |
| framework, canon a0 + per-galaxy U | 175 | 67324 | 19.87 | 67674 | 68746 |
| LCDM NFW, U=0.5 + (V200,c) per galaxy | 350 | 17670 | 5.22 | 18370 | 20515 |
| LCDM NFW, (V200,c,U) per galaxy | 525 | 10356 | 3.06 | 11406 | 14623 |

Median per-galaxy reduced χ²: framework (0 free/galaxy) 10.19 · NFW U=0.5 1.27 ·
NFW free-U 1.07. In 9% of galaxies the zero-per-object-freedom framework
curve lands within 2× of that galaxy's own 3-parameter NFW χ².

**Stated exactly as it must be:** ΛCDM halo fits **fit well** — with 2–3 free parameters per
galaxy they reach lower total χ², and they win raw AIC/BIC on this dataset despite the penalty.
The economy contrast is **freedom count and predictivity**: 1 externally-fixed global number
(+ one global M/L convention) against 350–525 per-object parameters; the framework's number
must simultaneously survive the photon band, the BTFR, and four nulls — a cross-dataset rigidity
that single-dataset information criteria cannot price. That rigidity, not a χ² win, is the
ledger's content. χ² caveat, both directions: the framework row models **no per-galaxy nuisance
at all** — SPARC's own 10–30% distance and inclination uncertainties enter its χ² as unmodeled
error, while per-galaxy halo parameters partially absorb them; the like-for-like
single-statistic comparison remains the committed RAR row, **0.108 dex (framework, canonical a0,
one global Υ) vs 0.122 (reg-MOND)** on the same points.

## 5. The ledger read (no "validates/proves")
One CMB-fixed number, formal width <1%, threads three independent positive bands with disjoint
systematics (a fourth probe class, wide binaries, is pending) and passes every null — two by ~4–7 orders of computed suppression, two by
exact structure (η = 0 at 1e-15 precision; k_AF = 0 where the CPT-odd sibling scale is dead by
~2 orders). The bands are wide and say so; the galaxy probes cannot pick the exact value; the
wide-binary row can still kill the premise. **Consistency with economy, exposed to a live
falsifier — that is the whole claim.**

*Files: `concordance.py` (this combine, exit 0), `concordance_crossing.png` (money figure),
lane scripts `anchor_planck_a0.py`, `p1_sparc_a0_band.py`, `p2_lensing_a0_band.py`,
`p3_btfr_a0_band.py`, `p4_widebinary_status.py`, `nulls_n1_n4.py`, sidecars `*_band.json`,
row detail `LEDGER_ROWS.md`.*
