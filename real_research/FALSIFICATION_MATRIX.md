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
