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
| **Wide binaries** | **0%** velocity boost (Newtonian) | **+3–15%** boost (EFE-suppressed; ~3–5% derived end) at s≳7000 AU | a **robust velocity boost** survives triple-rejection | **pure Newtonian** at the framework's sensitivity | **Gaia DR4**, ~2026–27 | **NULL-INFORMATIVE / degeneracy-limited** (our WB program, 2026-06, real Gaia DR3): faithful replication → ~3σ deep excess, fully absorbable by separation-dependent contamination; boost↔contamination degenerate in the sky-projected observable, and the orbital-prior-sensitivity (WB-3b) **weakens both published σ's (Banik ~16–19σ N, Chae ~4–5σ M)**. Neither strike nor support; **DR4-gated**. See `reviews/public_data/WB_PROGRAM_SUMMARY.md` |
| **a₀(z) evolution** ⚠️(corrected) | apparent a₀ rises ∝E(z) *(ΛCDM-degenerate)* | **faithful a₀ ∝ √ρ_DE**: constant (w=−1) or mild decline (×0.96/0.81/0.70 at z=1/2/3 under DESI) | — *(degenerate; can't kill ΛCDM)* | a₀ **rises** ∝√ρ_total (z~3 BTFR offset **far above** z=0) | JWST+ALMA halo-free RCs + DESI DR3, ~2027 | **CONTESTED, leaning UNFAVOURABLE**: MUSE-DARK III ~30σ *apparent* rise refutes the canonical constant; framework survives only via the ΛCDM-apparent-a₀ degeneracy (cuts both ways); declining branch untested. Sign of z~3 offset decides — see `A0Z_MUSE_DARK_III_CONFRONTATION.md`. |
| **CMB 3rd peak** | fits (non-baryonic CDM) | pure baryonic MOND → 3rd peak **too low** | a CMB feature ΛCDM can't fit *(none known)* | **the 3rd peak** | Planck — **DONE** | **ΛCDM wins** (framework needs AeST + dark field) |
| **Galaxy clusters** | fits with DM | MOND under-predicts core mass **~2×** | — | **the ~2× residual** | eROSITA, lensing — **DONE** | **ΛCDM wins** (environmental-a₀ fix breaks the RAR) |
| **Dwarf σ via EFE** | σ independent of host | σ depends on host field (Crater II ~2 vs ΛCDM ~4) | σ **tracks the external field** | σ **independent** of host | spectroscopy — partial | **MOND win** (Crater II obs ~2.7) |

> **⚠️ a₀(z) row — corrected (2026-06-05) to the settled √ρ_DE reading.** The a₀(z) cells were written for the
> *superseded* "a₀ rises ∝ E(z)" reading. Per [`THE_DARK_ENERGY_TRACKING_READING.md`](THE_DARK_ENERGY_TRACKING_READING.md)
> and [`DOORS_FINAL_DISPOSITION.md`](DOORS_FINAL_DISPOSITION.md) (#2), the framework's **faithful** claim is a₀ ∝ √ρ_DE →
> **constant** (w=−1, the safe geometric core) or a **mild decline** (~0.70 at z=3 under DESI); the rising ∝E(z) form was
> the ρ_total/ρ_DE conflation. So the kill-condition **flips**: a measured *steep rise* (∝√ρ_total) falsifies the a₀↔Λ
> thesis; *constant* is safe; a *mild decline* is the distinctive (DESI-contingent) win. **Honest consequence:** the
> correction makes the a₀(z) test *softer and currently unfavourable* — the distinctive signal retreated from a bold ×4.6
> rise to a ~30% decline current data can't distinguish from constant, while MUSE-DARK III's ~30σ *apparent* rise leaves
> the front empirically **mute-to-unfavourable** (faithful √ρ_DE survives only via the ΛCDM-apparent-a₀ degeneracy; full
> grade in [`A0Z_MUSE_DARK_III_CONFRONTATION.md`](A0Z_MUSE_DARK_III_CONFRONTATION.md)). Only the **sign of the z~3 BTFR
> offset** (JWST/ALMA + DESI DR3, ~2027) cleanly probes the fundamental a₀(z).

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
- **a₀(z) rising ∝√ρ_total** — if halo-free high-z measurements show a₀ rising *steeply* as cH(z) (the
  matter-tracking ρ_total form, ×4.6 at z=3), the framework's a₀↔Λ thesis is falsified. *Constant* a₀ is **not**
  a kill — it is the safe w=−1 core; the distinctive **faithful** signal is a *mild decline* (~0.70 at z=3 under
  DESI). [Corrected 2026-06-05 — the older "constant a₀ kills it" was the superseded rising-reading inversion.]

## The honest asymmetry (the uncomfortable part)

| | tests | status |
|---|---|---|
| **Can kill ΛCDM** | EFE, wide-binary boost | **both UNCONFIRMED** (contested / split) — *no clean ΛCDM kill is in hand* |
| **Can kill the framework** | CMB, clusters, a₀(z) **rising** ∝√ρ_total, wide-binary null, **Cassini quadrupole** | **partly ALREADY realized** (CMB & clusters lost; a₀(z) **leaning UNFAVOURABLE** — MUSE-DARK III shows a ~30σ apparent rise; faithful √ρ_DE survives only via the ΛCDM-apparent-a₀ degeneracy → empirically *mute-to-unfavourable*). **NEW near-term pressure:** the Cassini Solar-System quadrupole excludes RAR-fitting modified-gravity interp functions at **3–15σ** (Desmond+2024 → 2026 update) — the framework inherits this via AeST and **cannot** invoke modified-inertia (it is modified gravity); escape = AeST `K(𝒬)` screening, *uncomputed*. The one kill-pressure that does **not** wait for z~3. See `CASSINI_QUADRUPOLE_CONSTRAINT.md`. |

**Read it straight: the framework currently carries *more* live falsification exposure than ΛCDM.** ΛCDM has
*lost nothing* it can't absorb (it owns the CMB and clusters; the galaxy RAR it fine-tunes), while the framework
has *standing losses* (CMB, clusters need an added field) and an a₀(z) front that is *contested, leaning
unfavourable* (the corrected row above — MUSE-DARK III's ~30σ apparent rise; the faithful √ρ_DE survives only via
the ΛCDM-apparent-a₀ degeneracy, so the front is empirically mute-to-unfavourable, not a clean win). That
is not a reason to abandon it — a falsifiable theory with standing risk is a *real* theory, not a fitted one — but
it is the true scoreboard.

## What flips it — the only path

The verdict moves **only** when a **ΛCDM-impossible signal is confirmed.** Concretely, in priority order:
1. **Independent confirmation of the EFE** (a second group, second method, reproducing Chae's environment-dependent
   rotation curves at ≥4σ). This is the single fastest, cleanest potential ΛCDM kill — it needs no new telescope,
   just rigorous independent analysis of existing/near-term RC samples.
2. **Gaia DR4 wide binaries** (~2026–27) with proper triple-rejection — settles the *foundation*. A confirmed
   boost validates the premise; a hard null at the framework's sensitivity falsifies it.
3. **Halo-free high-z a₀(z)** (JWST/ALMA + DESI DR3, ~2027) — settles the *distinctive* claim via the **sign of the
   z~3 BTFR offset**: faithful √ρ_DE declining (~0.70, *below* z=0) vs constant (1.0) vs the disfavored rising
   ∝√ρ_total (4.6, *far above*). The hard split is declining-vs-constant (~30%, needs N~30 discs); it can't
   separate the framework from ΛCDM.

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
