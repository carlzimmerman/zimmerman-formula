# The Falsification Matrix — Where Each Model Breaks, Where It Lives

**C. Zimmerman, June 2026.** *Sharpens `TESTABLE_PREDICTIONS.md` into decision criteria: for each test, the exact
outcome that **invalidates** one model and **validates** the other. Numbers verified in
`reviews/project_decision_matrix.py`. The organizing principle — and it is symmetric and fair:*

> **Only a ΛCDM-*impossible* signal can break ΛCDM. Only a MOND-*impossible* result can break the framework.**

Everything reduces to: which tests are which, what the kill-threshold is, and where the data currently lean.

---

## The decision table

| Test | ΛCDM predicts | Framework / MOND predicts | ⇒ KILLS ΛCDM if… | ⇒ KILLS framework if… | Instrument · timeline | Current lean |
|---|---|---|---|---|---|---|
| **External field effect** | **no** environmental dependence (shell theorem) | internal boost **collapses 10×→1** as external field rises | rotation-curve amplitude **declines with environment** | rotation curves **independent of environment** | galaxy RC samples; Chae method | **Chae 4–5σ — CONTESTED** |
| **Wide binaries** | **0%** velocity boost (Newtonian) | **+3–15%** boost (EFE-suppressed; ~3–5% derived end) at s≳7000 AU | a **robust velocity boost** survives triple-rejection | **pure Newtonian** at the framework's sensitivity | **Gaia DR4**, ~2026–27 | **SPLIT** (Banik 19σ N vs Chae 4σ M) |
| **a₀(z) evolution** | apparent a₀ also rises *(degenerate!)* | a₀ rises **exactly as E(z)** (×1.8/3.0/4.6 at z=1/2/3) | — *(degenerate; can't kill ΛCDM)* | a₀ **constant** (→std-MOND) or **falls** (→SIV) | JWST+ALMA halo-free RCs, ~3 yr | **UNFAVORABLE** (MUSE faster than E(z), McGaugh constant) |
| **CMB 3rd peak** | fits (non-baryonic CDM) | pure baryonic MOND → 3rd peak **too low** | a CMB feature ΛCDM can't fit *(none known)* | **the 3rd peak** | Planck — **DONE** | **ΛCDM wins** (framework needs AeST + dark field) |
| **Galaxy clusters** | fits with DM | MOND under-predicts core mass **~2×** | — | **the ~2× residual** | eROSITA, lensing — **DONE** | **ΛCDM wins** (environmental-a₀ fix breaks the RAR) |
| **Dwarf σ via EFE** | σ independent of host | σ depends on host field (Crater II ~2 vs ΛCDM ~4) | σ **tracks the external field** | σ **independent** of host | spectroscopy — partial | **MOND win** (Crater II obs ~2.7) |

## The two clean, mutually-exclusive verdicts

**Where ΛCDM can actually break (the only places):**
- **EFE** — ΛCDM *forbids* any dependence of internal dynamics on a uniform external field (shell theorem). MOND
  *requires* the boost to collapse from ~10× to ~1 as the external field grows past a₀. **Any robust detection of
  environment-dependent rotation curves is a ΛCDM kill.** Chae reports 4–5σ; it needs independent confirmation.
- **Wide binaries** — ΛCDM/Newton predict exactly **zero** boost; MOND predicts a (small, EFE-suppressed) boost at
  the geometric-mean MOND radius r_M = (8π/3)^{1/4}√(r_s R_H) ≈ 7000 AU. **A confirmed boost is a ΛCDM kill.**

**Where the framework can actually break:**
- **CMB 3rd peak & clusters** — *already realized.* Pure MOND loses both; the framework survives only by adding a
  relativistic completion (AeST) with a dark field — keeping the dark sector's economy *only* at galaxy scale.
- **Wide-binary null** — if Gaia DR4 confirms pure Newtonian even at the framework's ~3–15% sensitivity, the
  *premise* (local MOND, the deep-MOND sign at z=0) is locally falsified.
- **a₀(z) constant** — if halo-free high-z measurements show a₀ flat, the framework's *one original idea* dies
  (and standard MOND lives). This is currently the lean.

## The honest asymmetry (the uncomfortable part)

| | tests | status |
|---|---|---|
| **Can kill ΛCDM** | EFE, wide-binary boost | **both UNCONFIRMED** (contested / split) — *no clean ΛCDM kill is in hand* |
| **Can kill the framework** | CMB, clusters, a₀(z), wide-binary null | **partly ALREADY realized** (CMB & clusters lost; a₀(z) leaning unfavorable) |

**Read it straight: the framework currently carries *more* live falsification exposure than ΛCDM.** ΛCDM has
*lost nothing* it can't absorb (it owns the CMB and clusters; the galaxy RAR it fine-tunes), while the framework
has *standing losses* (CMB, clusters need an added field) and an *unfavorable lean* on its distinctive test. That
is not a reason to abandon it — a falsifiable theory with standing risk is a *real* theory, not a fitted one — but
it is the true scoreboard.

## What flips it — the only path

The verdict moves **only** when a **ΛCDM-impossible signal is confirmed.** Concretely, in priority order:
1. **Independent confirmation of the EFE** (a second group, second method, reproducing Chae's environment-dependent
   rotation curves at ≥4σ). This is the single fastest, cleanest potential ΛCDM kill — it needs no new telescope,
   just rigorous independent analysis of existing/near-term RC samples.
2. **Gaia DR4 wide binaries** (~2026–27) with proper triple-rejection — settles the *foundation*. A confirmed
   boost validates the premise; a hard null at the framework's sensitivity falsifies it.
3. **Halo-free high-z a₀(z)** (JWST+ALMA, ~3 yr) — settles the *distinctive* claim (framework E(z) vs constant vs
   SIV, ~10× apart at z=3), though it can't separate the framework from ΛCDM.

Until one of those lands, the honest verdict is fixed: **a real, falsifiable theory, strongest on galaxy scales,
carrying genuine standing risk, whose validation hinges entirely on a ΛCDM-impossible signal that is currently
contested or split — not won, and not lost.** Anyone claiming otherwise, in either direction, is ahead of the data.

---

## Extension — more discriminators (2026-06-04 deep dive), and two corrections to the above

A second literature sweep added tests that cut **both ways**, and flagged two places my matrix above was too strong.

### New ΛCDM-stressing tests (pro-MOND — but every one has a live escape)

| Test | ΛCDM | MOND | Tension | Escape route | Instrument |
|---|---|---|---|---|---|
| **Fast galactic bars** | DM halo drags bars slow (R>1.4) via dynamical friction | no halo → bars stay fast (R≈1) | **8σ** (Roshan+ 2021 vs EAGLE/TNG) | simulation numerics / resolution (Frankel+ 2022) | MaNGA/SAMI now |
| **El Gordo** (z=0.87, ~2×10¹⁵ M⊙, ~2500 km/s) | too massive/fast/early | natural (faster growth + boost) | **6.2σ** (Asencio+ 2023) | cluster mass/velocity systematics; rare-tail | JWST/Euclid 2024–28 |
| **KBC void + H₀** | local void too deep; growth too slow | deep voids natural; relieves H₀ tension | claimed **7σ** (Haslbauer+ 2020) | void depth/profile contested (likely shallower) | DESI/4MOST/Rubin 2026–30 |
| **Planes of satellites (M31, Cen A)** | isotropic accretion; planes rare | tidal-dwarf planes natural | co-rotation <1% of analogs | MW plane now *escapable* (transient, Sawala 2023); M31/Cen A harder | Gaia DR4, Rubin+Euclid |

**The genuine pattern worth seeing:** El Gordo, the KBC void, JWST early galaxies, *and* fast bars all probe the **same axis — faster early structure growth**, which is exactly what MOND predicts. Each has an individual escape, but they **point the same way**, and that coherence is a real (if soft) pro-MOND signal — more than the sum of four isolated anomalies.

### New robust ANTI-MOND tests (these deepen the framework's exposure)

| Test | Verdict |
|---|---|
| **Cluster RAR / residual mass** (Li+ 2024) | **Clean, against MOND** — cluster centrals follow an *offset* RAR; MOND still needs ~2× extra unseen mass. Sharpens the "clusters" row with 2024 RAR-framed data. |
| **Weak-lensing RAR early/late split** (Brouwer+ 2021) | **6σ, against *pure* MOND** — property-independent modified gravity *cannot* make the RAR depend on galaxy type; the split needs a baryonic (circumgalactic-gas) explanation. |

### Two corrections to my matrix above (honesty flags)

1. **The "CMB 3rd peak → ΛCDM wins" row was too strong.** Skordis–Złośnik **AeST** (2021, PRL) reproduces the
   acoustic peaks **and** keeps c_GW=c. Honest framing: *MOND-as-modified-gravity-alone loses the CMB, but
   covariant MOND fits it by adding a field that behaves dark-matter-like at early times* — which blurs the MOND/DM
   distinction rather than a clean ΛCDM win. (It's still a cost: the economy survives only at galaxy scale.)
2. **GW170817 killed *TeVeS*, not MOND.** The c_GW=c bound (10⁻¹⁵) falsified Bekenstein's TeVeS and its cousins,
   but AeST/RelMOND survives. So it's a clean kill of a *specific relativistic realization*, not of MOND broadly —
   and it's the template for what a real "kill" looks like.

### The deepened, honest asymmetry

The extension makes the asymmetry **sharper**, not softer: the robust **anti-MOND** results (cluster RAR, the
lensing early/late split, the standing CMB/cluster costs) are **more robust** than any single **pro-MOND** anomaly
(bars, El Gordo, void, planes — all "ΛCDM-stressed with a live escape"). So the framework's exposure is genuinely
**multi-front**. *But* the pro-MOND items share a coherent structure-growth axis, and the two clean ΛCDM-kill doors
(EFE, wide binaries) remain the decisive ones. Net: more tests on the board, the same verdict — **contested, the
framework carrying more standing risk, the kill-doors still unconfirmed** — now with a clearer map of exactly
where each model is pressed.
