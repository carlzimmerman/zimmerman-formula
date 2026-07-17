# POWER — cluster-member EFE relational σ-spread on REAL survey data (2026-07-17)

**Lane:** power analysis on existing data. **Script:** `power.py` (+`.out`, exit 0, numpy-only, both
footings). **Estimator:** the SAME frozen pooled cluster-centered OLS slope of the FJ residual on the
infall-phase proxy as the banked carrier lane (`../sigma_spread/POWER_cluster_efe_channel.md` E1–E9);
calibrated here, never fired on real σ-vs-infall data (specs only).

## The question this lane answers (distinct from the banked UDG/ELT carrier lane)

The banked lane found the **diffuse-UDG carrier** route needs ELT (~2032). This lane asks whether the
**survey-measurable** regimes bite NOW: (a) a single rich cluster (Coma ~1000+ members), (b) a stacked
SDSS sample (redMaPPer/Yang × single-fiber σ, N~1e4–1e5), plus MaNGA/SAMI IFU.

## The physics that sets per-member amplitude (the kernel, physically anchored)

The relational spread `f` depends on the member's **dimensionless depth** `a_in/a0`, with
`a_in ≈ σ²/R_e` (a0 cancels in `f` — footing only remaps which physical (σ,R_e) lands at a given depth):

| a_in/a0 | f (spread) | physical member |
|---|---|---|
| 0.05 | 23% | UDG σ~20, R_e~3 kpc (ELT-only) |
| 0.15 | 20% | diffuse dSph σ~22, R_e~1.2 |
| 0.5 | 12% | MaNGA-reachable dE σ~50, R_e~2 |
| 1.0 | 7% | SDSS-floor dE σ~90, R_e~2.5 |
| 3.0 | 1.9% | SDSS mid-E σ~150, R_e~3 |
| 10 | 0.3% | SDSS bright E σ~230, R_e~4 |

`f` drops **~50×** from the deep-MOND carriers to the survey-bright members. The measurable-by-survey
members are the shallow ones; the deep ones (large f) are faint/diffuse. **That anti-correlation is
the whole power problem** — but N also differs by ~100× across the ladder, so both must be weighed.

## Confirmed real-data specs (web search 2026-07-17 + banked census)

- **SDSS single-fiber veldisp:** instrumental floor 69 km/s, resolution ~90 km/s → σ<~90–100 km/s
  **unreliable** (sdss3.org; Sohn+2017; Zahid+2016). The σ-complete cluster-member sample is therefore
  **dominated by bright/mid ellipticals (σ~120–300)** — the low-f end of the ladder. N ~ O(1e5) across
  redMaPPer (~26k clusters) / Yang groups × SDSS spectroscopy.
- **MaNGA DR17:** ~10,000 galaxies; IFU LSF gives reliable astrophysical σ **down to ~20 km/s**
  (Law+2021) — reaches genuine signal depth. Cluster/group members ~O(1e3); diffuse dE/dwarf ~few
  hundred–1e3. **SAMI** ~3,000 galaxies incl. 8 clusters (Owers+2017): same IFU depth.
- **Coma:** deep dwarf spectroscopy (MUSE/Subaru) reaches σ~15–40; diffuse members with internal σ ~
  few hundred.
- **Phase tagging (free, public):** HeCS-omnibus 227 clusters/52k caustic members; GalWCat19;
  Rhee+2017 PPS infall diagram; Oman+2013.

## Results (both footings; full grid in `power.out`)

**The compensation question — does N~1e5 beat tiny f?** VDF-weighted population MC (Choi+2007 σ-function
truncated to σ>90 + size-σ relation): ~24–35% of σ-complete members fall in the diffuse a_in<1.5a0 tail
carrying ⟨f⟩~3–4%, so **statistically the SDSS stack is OVER-powered: z ~ 8 (canonical) / 10 (alt) at
N=1e5.** The N *does* compensate statistically. But the detected quantity is a **slope of amplitude
D·⟨f⟩ ~ 1.2–1.4% in ln σ.**

**Why that z is a mirage — the signal-to-systematic ratio (the real wall for the stack):**

| route | D·f (signal) | σ-sys floor | C6 confound | signal vs floor |
|---|---|---|---|---|
| SDSS stack (bright/mid E) | ~1.2% | 1–5% (single-fiber aperture/S–N/z) | 2–8% | **BURIED / MARGINAL** |
| MaNGA/SAMI diffuse dE cut | ~4.4% | 0.3–1% (IFU resolved) | 2–8% | **CLEARS the σ-sys floor** |
| Coma/nearby deep diffuse | ~5.9% | 0.3–1% | 2–8% | **CLEARS** |

The SDSS stack is **systematics-limited, not statistics-limited** — a *new* failure mode versus the
banked carrier lane (which is statistics-limited). Its ~1% signal sits inside the single-fiber σ
systematic floor AND below the same-signed, phase-correlated C6 tidal/environmental confound (2–8%,
`../sigma_spread/MG_ZERO.md`). Beating it needs **sub-0.5% σ control + the radial-profile separator**,
not more galaxies. The single-fiber σ<90 km/s reliability wall also bars the high-f diffuse members
from the stack in the first place.

**Head-to-head (the tasked comparison):** the two routes fail for **opposite** reasons —

- **(a) Single rich cluster (Coma):** only ~300–400 diffuse deep-σ members → **z ~ 2.0–2.5** (fails on
  **statistics/N**). Best used as the cleanest single testbed; stacking Coma+Virgo+Fornax+A2029 with
  IFU/deep dwarf σ reaches z~3.7–4.0 at N~1e3.
- **(b) Stacked SDSS:** z≫3 statistically but fails on **systematics** (above).

**The one 2026-existing route that can give an exploratory hint:** the **MaNGA/SAMI IFU diffuse-member
cut**. IFU reaches σ~20–50 (real depth, f~10–14%) at resolved errors whose ~0.3–1% systematic floor the
~4% signal clears. The wall is **N**: only ~few hundred–1e3 diffuse cluster members with IFU σ + phase
tags → **z ~ 2.7–2.9 (canonical/alt), EXPLORATORY/hint-grade**, single-survey systematics; can neither
confirm nor kill. Both footings within ~10% (alt needs ×0.8 the N — **not footing-hostage**).

## VERDICT

- **POWERED NOW (clean detection)? NO on all existing data.** SDSS stack: systematics-limited (~1%
  signal under a 1–5% σ-sys + 2–8% confound floor). Coma single: statistics-limited (z~2–2.5).
- **NEAREST BITE-NOW:** a **MaNGA/SAMI + SAMI-cluster IFU diffuse-dE reanalysis** at HeCS/GalWCat19/
  Rhee-2017 phase tags → an **exploratory ~2–3.5σ** probe (hint-grade, firewalled).
- **What a clean detection needs:** EITHER (i) ELT-HARMONI diffuse-UDG carrier σ (~2032; banked carrier
  lane), OR (ii) a dedicated **wide nearby-cluster IFU dwarf survey** (~1e3–1e4 diffuse members,
  resolved σ, sub-percent systematics). The binding resource is **systematic σ control**, which a
  stacked SDSS sample cannot buy with N.

## Scope / caveats (carried at full weight)

- **MI-CLASS-GENERIC, not framework-specific:** discriminates MI-class (any history-dependent inertia,
  incl. Milgrom 2503.07106 no-EFE MI) vs MG(=0). NOT this-framework vs Milgrom's MI.
- **MG=0** stays a theorem for the sourced-field WEP class (any a0, any interpolation, both footings,
  off-adiabatic; `../sigma_spread/MG_ZERO.md`). Only the y-dependence is MG-impossible; a constant EFE
  boost is absorbable.
- **Amplitude kernel-hostage:** 6–13% fiducial (cone 4–15%); **a0 value + sign s=−1 are postulates**.
  Existence + sign + MG=0 are theorem-grade; the amplitude is a band.
- **Both footings shown throughout** (identical at fixed depth; alt needs ×0.8 the N).

**Credit:** Milgrom 1983 (MOND) / 1999 PLA 253:273 (ν-kernel wellhead) / 2022 PRD 106 064060 (MOND as
modified inertia). Cluster kinematics: Rhee+2017, Oman+2013, Sohn+2017/2020, Choi+2007, Owers+2017,
Law+2021.
