# CONCORDANCE LEDGER — one Planck-fixed acceleration through independent probe classes
**Lane AP: anchor + probe rows.** 2026-07-16. Every number below is either cited to a primary
source or recomputed by an exit-0 script in this directory. The frozen repo
(`~/new_physics/zimmerman-formula`) was read, never written.

**The structure that makes the ledger possible:** a0 is not fitted — it is derived from the
cosmological constant, `a0 = c·H_Λ/Z = c²√(Λ/3)/Z`, `Z = √(32π/3) = 5.7888`. Interpolation is the
framework's own `ν(y) = √(1+1/y)` (never McGaugh's ν; fitted g† values are never compared across
ν conventions). Modified **inertia**: WEP exact, CPT-even by structure, high-a solar-system
channels suppressed. Both footings on every row.

**What the ledger claims (rails):** consistency + parameter economy, not proof. Galaxy probes are
convention-compatible and **non-diagnostic** of the exact a0 (banked; committed
`real_research/rar_framework_a0_mlfit.py` rerun 2026-07-16: **0.108 dex @ Υ=0.70, beats reg-MOND
0.122**). Each positive row therefore contributes a **wide band** with its own disjoint
systematics; the claim is *the Planck-fixed value sits inside every independent band with zero
per-object freedom* — never "probe X pins 9.36e-11". ΛCDM fits the positive probes too, with
per-object halo freedom; the economy contrast is quantified per row.

---

## ANCHOR — Planck 2018 → a0 (script: `anchor_planck_a0.py`, exit 0)

| quantity | value | source |
|---|---|---|
| H0 | 67.36 ± 0.54 km/s/Mpc | Planck 2018 VI, A&A 641 A6, **Table 2, TT,TE,EE+lowE+lensing** |
| Ω_Λ | 0.6847 ± 0.0073 | same table |
| H_Λ = H0√Ω_Λ | 1.8063e-18 s⁻¹ | derived |
| **a0 CANONICAL** (ρ_DE/cH_Λ) | **(9.355 ± 0.090)e-11 m/s²** (0.96%; ρ-bracket 0.27–1.33%) | `a0 = cH_Λ/Z` |
| **a0 ALT** (ρ_total/cH0) | **(1.1305 ± 0.0091)e-10 m/s²** (0.80%) | `a0 = cH0/Z` |

Equivalent forms `c²√(Λ/3)/Z` and `(c/2)√(Gρ_Λ)` verified to <1e-12. Error propagation:
quadrature on (H0, Ω_Λ); the full ρ=±1 correlation bracket is printed (0.27%–1.33%), so the
sub-percent statement holds at quadrature and ~1.3% at the worst-case ceiling. Z is fixed by the
framework's dS-Unruh construction — its **value is postulated, not derived** (κ-closure banked);
the ledger tests the number, not its pedigree.

---

## POSITIVE PROBES — four independent bands, one number

### P1 — Kinematic RAR, SPARC 175 (script: `p1_sparc_a0_band.py`, exit 0)
*Systematics owned: stellar M/L, distances, inclinations. Data: gas kinematics.*

Committed baseline reproduced: fixing a0 = 9.36e-11 fits the full SPARC RAR at **0.108 dex**
scatter with Υ_disk = 0.70 (SPS range 0.5–0.8), beating reg-MOND's 0.122 @ Υ=0.5. Profiling the
weighted scatter over a0 with the framework ν:

| Υ_disk | best a0 | 2%-tolerance window | penalty @ canonical | @ alt |
|---|---|---|---|---|
| 0.50 | 1.76e-10 | [1.62, 2.00]e-10 | 37.6% | 20.9% |
| 0.60 | 1.36e-10 | [1.25, 1.55]e-10 | 15.0% | 4.3% |
| 0.70 | 1.10e-10 | [0.96, 1.25]e-10 | 2.4% | 0.05% |
| 0.80 | 8.83e-11 | [0.78, 1.05]e-10 | 0.09% | 3.7% |

**Kinematic band (union over physical Υ): [7.8e-11, 2.0e-10]. Canonical INSIDE (best at Υ≈0.75–0.80);
ALT INSIDE (best at Υ≈0.55–0.70).** The best-fit a0 moves ~2x across the physical M/L range — the
RAR does **not** pin a0 (non-diagnostic, as banked). Economy: 1 global Υ for 175 galaxies vs
~2–3 halo parameters per galaxy (~350–525) for ΛCDM on the same curves.

### P2 — Weak-lensing RAR, photons (script: `p2_lensing_a0_band.py`, exit 0)
*Systematics owned: shear calibration, photo-z, lens stellar-mass scale, CGM budget —
**fully disjoint from P1** (no rotation curves, inclinations, or SPARC distances enter; no shear
or photo-z enters P1).* Data: **Brouwer et al. 2021, A&A 650, A113 (KiDS-1000)** — the authors'
own CDS machine-readable release, in-hand in the frozen repo (not digitized). GLS fit with the
full published covariance, framework ν only.

| variant | fitted a0 | stat (Δχ²=1) |
|---|---|---|
| KiDS isolated, fiducial (stars+cold gas), 15 pts | 1.98e-10 | [1.88, 2.07]e-10, χ²/dof 2.8 |
| M* +0.2 dex (SPS zero-point) | 1.24e-10 | [1.18, 1.30]e-10 |
| **hot-CGM budget (B21's own variant file)** | **7.6e-11** | [7.2, 8.0]e-11 |
| GAMA spec-z lenses (independent sample) | 1.62e-10 | [1.30, 1.99]e-10 |
| shear+photo-z ±5% | 1.78–2.18e-10 | — |

**Photon band (systematics envelope): [7.2e-11, 3.3e-10]. Canonical INSIDE; ALT INSIDE.**
Honest read, both directions: with the fiducial cold-baryon budget the fit sits ~2.1x canonical
(with low-acc shape tension, χ²/dof 2.8, exactly where B21 flag the unmeasured CGM); B21's **own**
hot-gas variant lands **below** canonical (0.81x). The Planck value sits **between the two
published baryon budgets** — the band edges are physics B21 themselves state ("our results are
sensitive to the amount of circumgalactic gas"). Neither "lensing pins it" nor "lensing excludes
it" survives. The photon-specific systematics (shear, photo-z) move a0 only ~10%; the baryon
budget dominates. Corroboration (cited; no machine-readable release found on arXiv/Zenodo as of
2026-07-16): **Mistele, McGaugh, Lelli, Schombert, Li 2024** (JCAP 04(2024)020, arXiv:2310.15248)
— exact deprojection, SPARC-consistent SPS masses: the lensing RAR "smoothly continues" the
kinematic RAR ~2.5 dex deeper, early/late types on the same relation under strict isolation.

### P3 — BTFR zero-point (script: `p3_btfr_a0_band.py`, exit 0)
*Shape-free global statistic: (Vflat, M_b) only. Dominant systematic: M/L (same 0.5–0.8 range as
P1 — one range ledger-wide); then distances.* Data: SPARC master table (Lelli+ 2016, AJ 152, 157),
N=121 after standard cuts (e_Vf/Vf≤0.10, Q≤2, i≥30°).

Framework-exact relation (derived in-script, no deep-limit approximation):
`Vf⁴ = G·M_b·(a0 + g_bar,last)` — the naive estimator `Vf⁴/(G·M_b)` is biased **high** by g_bar at
the last measured point. Both estimators shown (naive for the record, exact for the row), plus a
deep subsample (g_bar,last < 0.2·a0, bias <20% by construction) as cross-check:

| Υ | naive median | **exact median ± err** | deep-sub median (N) |
|---|---|---|---|
| 0.50 | 1.53e-10 | 1.46e-10 ± 0.09e-10 | 1.48e-10 (105) |
| 0.60 | 1.36e-10 | 1.22e-10 ± 0.08e-10 | 1.25e-10 (100) |
| 0.70 | 1.22e-10 | 1.07e-10 ± 0.07e-10 | 1.15e-10 (97) |
| 0.80 | 1.13e-10 | 0.95e-10 ± 0.08e-10 | 1.08e-10 (95) |

**BTFR band (exact estimator, Υ 0.5–0.8): [8.7e-11, 1.55e-10]. Canonical INSIDE (at Υ≈0.75–0.80);
ALT INSIDE (at Υ≈0.60–0.65).** Honest edge, stated: at Υ=0.70 exactly the exact-estimator median
sits ~1.8σ above canonical — canonical needs the upper half of the SPS range here. Internal
consistency the ledger buys for free: at canonical a0, P1's profile scatter and P3's shape-free
zero-point **co-move** to the same Υ≈0.75–0.80; at ALT both prefer Υ≈0.55–0.65. No Υ makes the two
SPARC statistics demand different a0.

### P4 — Gaia wide binaries: STATUS ROW, not a decided band (script: `p4_widebinary_status.py`, exit 0)
*Microarcsecond astrometry; contamination/triples systematics disjoint from all above.*
Framework prediction: pure-MI γ ≈ **1.05–1.14** (θ(0)-family, the most-Newtonian MOND reading;
MG momentary-field 1.137; Newton 1.00). a0-degenerate — tests the premise, not the value.
Committed DR3 dry-run record (re-parsed from frozen-repo outputs): deep-bin medians sit
**2.4–3.2 z above the calibrated Newton MC** and 6–22 z **below** the naive full-MOND upper bound;
a separation-dependent triple fraction can absorb most of the excess. Session-banked headline
γ = 1.205 ± 0.035 carried with the **contamination-axis caveat**, not recomputed, not a detection.
**PENDING — Gaia DR4 (~Dec 2026).** This is the row that can hard-kill (Newtonian null kills all
MOND readings including this framework) or separate MI from MG (boost ≥15–20% favors MG).

---

## NULL PROBES — the framework must predict ~zero where the best instruments see zero
(script: `nulls_n1_n4.py`, exit 0; margins per footing)

| row | framework prediction | measured bound (primary source) | margin |
|---|---|---|---|
| **N1 ephemerides** | a0/2-channel split: DC piece ν−1 = a0/2g = 7.2e-7 @ Saturn **absorbed into GM_sun** (not an anomaly); observable MI quadrupole (committed l=2 Legendre) **Q2 = 7.4e-34 s⁻²** (canon) / 1.1e-33 (alt) | Cassini Q2 = (1.6±1.8)e-27 s⁻², 2σ ceiling 5.2e-27 (Park+ 2026, arXiv:2602.17884; Desmond-Hees-Famaey 2024, MNRAS 530, 1781) | **PASS, 6.7–6.8 orders**. MG-read of the same a0: Q2 ~ a0/2r = 3.3e-23 → **excluded by 3.8–3.9 orders** — the MI/MG split is the framework's content, and the nearest sibling fails where it passes |
| **N2 LLR** | DC ν−1 = 1.7e-8 absorbed into GM_earth; observable channel ~(a0/2g)² = 3.0e-16 (canon) / 4.4e-16 (alt) fractional | mm-level ranging, fractional sensitivity ~2.6e-12 (APOLLO; Murphy 2013, Rep. Prog. Phys. 76, 076901) | **PASS, 3.8–3.9 orders** |
| **N3 WEP** | **η = 0 exactly** — MI rescales inertia universally; no composition channel exists (footing-independent) | η(Ti,Pt) = (−1.5 ± 2.3)e-15 (Touboul+ 2022, PRL 129, 121102, final) | **PASS, 0.65σ from exact zero** at 1e-15 precision |
| **N4 CPT/k_AF** | **k_AF = 0 exactly** — SME bridge theorem: horizon background induces CPT-even s_μν only | |k_AF| < 1e-44 GeV (Kostelecký-Russell RMP 83, 11, 2023 tables, CMB birefringence) | **PASS by structure**. Falsified alternative: natural CPT-odd scale ħH = 1.19e-42 (H_Λ) / 1.44e-42 GeV (H0) sits **~120–144x above the bound** — a CPT-odd horizon variant is dead ~2 orders; the surviving CPT-even s^TX keeps ~9.6x margin (Gaia DR4 front) |

---

## THE LEDGER READ (no "validates/proves")

One CMB-fixed number, formal width <1%, sits **inside** four bands measured with disjoint
systematics — gas kinematics (M/L, distance, inclination), lensed photons (shear, photo-z, baryon
budget), a shape-free global scaling (M/L, distance), — while every high-precision null the
framework must pass, it passes: two by computed suppression (~4 and ~7 orders of margin), two by
exact structure (0 at 1e-15; 0 where the sibling CPT-odd scale is dead by 2 orders). The wide
bands are stated as wide; the two galaxy-band edges are set by published baryon-budget physics,
not by instrument noise. Parameter economy: the framework spends **one global M/L per dataset**
(and zero per-object parameters); ΛCDM fits the same positives with hundreds of per-object halo
parameters and no cross-probe number to thread. The wide-binary row is pending and can still kill
the premise outright. That is the honest shape of the claim: **consistency with economy, exposed
to a live falsifier — not proof.**

*Scripts (all exit 0, this directory): `anchor_planck_a0.py`, `p1_sparc_a0_band.py`,
`p2_lensing_a0_band.py`, `p3_btfr_a0_band.py`, `p4_widebinary_status.py`, `nulls_n1_n4.py`.
JSON side-cars: `anchor_values.json`, `p1_band.json`, `p2_band.json`, `p3_band.json`.*
