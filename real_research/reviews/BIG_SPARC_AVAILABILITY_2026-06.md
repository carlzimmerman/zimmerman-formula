# BIG-SPARC availability check, and the honest state of the a₀ environmental fork

**C. Zimmerman, 2026-06-05.** *Task: download BIG-SPARC (~4000 galaxies) and push the cluster-vs-field a₀ null
from N=28 to hundreds. Disposition below is a **release-limited door**: BIG-SPARC is not public, so the
BIG-SPARC analysis is documented and stopped — but the current public-data state of the art and a computed
power forecast are reported, and a drop-in pipeline is staged for release day
(`predictions/project_bigsparc_a0_environment.py`).*

---

## One-paragraph verdict

**BIG-SPARC is not publicly available as of 2026-06-05**, so steps (2)–(3) of the task — fit a₀ on the
larger sample and cross-match a real group catalog — cannot be run on it, and per the task are documented
and stopped (no fabricated data). This is not a loss: on the **public 175-galaxy SPARC** the local-ρ fork
(`d log a₀ / d log ρ = +½`) is **already dead 13–35×** — the internal-density (SBeff) slope excludes +0.5 at
**13σ** (Q=1) and the continuous NED kNN-density slope excludes it at **~34σ** (122 galaxies over a 6.4-dex
density range, slope **−0.010 ± 0.015**, consistent with 0 at 0.6σ). The one genuinely **underpowered** piece
is the direct cluster/field contrast (Ursa Major, N=28, p≈0.6–0.9). That — not the dead +0.5 fork — is what
BIG-SPARC would fix: a real group-catalog cross-match would push N_cluster → hundreds and drop the minimum
detectable a₀ offset from ~0.05 dex (today, 0.8σ) to a few-σ measurement, i.e. it would test whether a₀ is
**exactly** environment-independent or carries a small residual trend. The pipeline to do that the day the
data drops is written and smoke-tested; today it runs only the (real, public-data) power forecast.

---

## 1 · The determination: BIG-SPARC is not public

| What was checked | Result (2026-06-05) |
|---|---|
| **arXiv:2411.13329** "BIG-SPARC: The new SPARC database" (Haubner, Lelli, et al., Nov 2024) — abstract **and** full HTML body | **Status/methods paper, not a data release.** Future tense throughout ("will provide … homogeneously derived HI rotation curves, surface brightness profiles, and mass models"). No data-availability section, no release date, no repository named. |
| **VizieR / CDS** for a BIG-SPARC catalog | None. (The only SPARC catalog is the original Lelli+2016, J/AJ/152/157.) |
| **Zenodo** | Only the original 175-galaxy SPARC rotation-curve record; no BIG-SPARC DOI. |
| **SPARC home (astroweb.cwru.edu/SPARC/, Case Western)** | Still the 175-galaxy database; TLS cert expired at check time, but mirrored listings show no BIG-SPARC product. |
| **ADS / literature follow-ups, 2025–2026** | No BIG-SPARC data-release paper. A Feb-2026 rotation-curve paper (arXiv:2602.24211) still uses "the SPARC sample of **175** galaxies" — the field has no larger public set to cite. |

**Conclusion:** ~19 months after the announcement, BIG-SPARC remains in preparation. The ~4000-galaxy HI
data cubes (APERTIF, ASKAP, ATCA, GMRT, MeerKAT, VLA, WSRT) + WISE photometry exist on the team's side, but
the homogeneous rotation curves / mass models / master table are **not downloadable**. Per the task
instruction ("if not yet public, document that and stop"), the BIG-SPARC line is **stopped here**.

## 2 · What BIG-SPARC would enable (the task's premise — and a correction)

The premise was: push the cluster-vs-field a₀ null from **N=28 → hundreds**, and bin by a continuous
external density instead of a single cluster flag. That premise is right about the *cluster contrast* but
needs one honest correction about the *headline fork*:

- The **+0.5 dex local-ρ fork is not a live question** on existing data — it is excluded at 13σ (internal
  density, clean Q=1 sample) and ~34σ (continuous NED density). BIG-SPARC would not "rescue" or first-settle
  this; it would make an already-decisive exclusion overwhelming.
- BIG-SPARC's **real** value is two-fold: (i) a **properly powered** direct cluster/group contrast (the SPARC
  N=28 gives only p≈0.6–0.9, blind to any offset below ~0.05 dex), and (ii) reach into the **subtle
  residual-trend regime** (≈0.01–0.05 dex) — where a weak EFE-like signature or a real systematic would live,
  if a₀ is environment-dependent at all below the cluster-contrast level.

## 3 · Current state of the art (computed on the public 175 sample, 2026-06-05)

All values recomputed today (`predictions/a0_environmental_fork_test.py`, `reviews/sparc_environment_a0_REAL.py`):

| Environmental lever | N | slope / offset | vs local-ρ (+0.5) | vs universal (0) |
|---|---|---|---|---|
| Internal density, SBeff, **Q=1** | 91 | slope **+0.031 ± 0.036** | **13.0σ excluded** | 0.9σ |
| Internal density, gas-dominated (M/L-free) | 61 | slope +0.040 ± 0.079 | 5.8σ excluded | 0.5σ |
| **Continuous NED kNN density**, 6.4-dex range | 122 | slope **−0.010 ± 0.015** | **~34σ excluded** | 0.6σ |
| Ursa-Major **cluster vs field** | 28 | offset **−0.025 dex**, p≈0.9, SE 0.067 | +0.5 excluded ~7.5σ | NULL (underpowered) |

The naive fixed-M/L SBeff slope (+0.18) is a demonstrated **M/L / data-quality artifact**: it collapses to
r≈0.07 (p=0.6) when restricted to gas-dominated points, and its strength tracks the assumed M/L — the
fingerprint of an artifact, not physics. No real a₀–density correlation survives artifact control. (Consistent
with Li, McGaugh, Lelli et al. 2018, A&A 615 A3: "no credible indication of variation in the critical
acceleration scale" — the novelty here is the **environmental** axis they did not test.)

## 4 · Power forecast — what a BIG-SPARC-sized N actually buys

Scaled from the measured public-data anchors (`SE(slope)=0.015` at N=122; cluster-offset `SE=0.067` at
N_cluster=20), assuming the same a₀ scatter and density range — **conservative**, since BIG-SPARC's larger
volume widens the density lever. Full table from `project_bigsparc_a0_environment.py`:

| BIG-SPARC N | SE(slope) | min slope detectable @3σ | +0.5 fork excluded at |
|---|---|---|---|
| 500 | 0.0076 | 0.023 | 66σ |
| 1000 | 0.0053 | 0.016 | 94σ |
| 2000 | 0.0038 | 0.011 | 132σ |
| 4000 | 0.0027 | 0.008 | 187σ |

| N_cluster (real group catalog) | SE(offset) | detect +0.5 dex | detect **+0.05 dex** |
|---|---|---|---|
| 20 (SPARC/UMa today) | 0.067 | 8σ | 0.8σ |
| 100 | 0.030 | 17σ | 1.7σ |
| 300 | 0.017 | 29σ | **2.9σ** |
| 800 | 0.011 | 48σ | **4.8σ** |

**Reading:** the +0.5 exclusion sails past overkill (≈100–190σ). The meaningful gain is the bottom-right
column — a real **+0.05 dex** environmental offset goes from invisible (0.8σ) to a 3–5σ measurement, and the
minimum detectable continuous trend drops from ~0.05 dex to ~0.01 dex. That is the science BIG-SPARC uniquely
unlocks: not the dead fork, but the existence (or firm absence) of a *small* environmental dependence.

## 5 · Disposition and what is staged

- **Door status: BLOCKED — release-limited, documented, stopped.** Same category as the z≈3 deep-MOND
  evolution test (telescope-limited): a valid "cannot run yet," not a failure. Note BIG-SPARC is a **z≈0**
  sample, so it sharpens *universality* (a₀ the same across today's density field) but still does **not**
  deliver *causal proof* (a₀ tracking ρ as ρ **changes** with cosmic time) — that remains the z≈3 door.
- **Staged for release day:** `predictions/project_bigsparc_a0_environment.py` — generalizes the audited a₀
  fit to the BIG-SPARC schema, cross-matches an **external** group/cluster catalog (Tempel+2017 FoF groups,
  VizieR J/A+A/602/A100, *or* the 2M++ density field, Lavaux & Hudson 2011) for a physical ρ_env, and reports
  the slope `d log a₀ / d log ρ_env` and the cluster/field offset with the full artifact-control battery
  (gas-dominated, Q-cut, M/L variation). It is data-gated: with no BIG-SPARC on disk it runs only the §4
  forecast and exits — it fabricates no galaxies. The live path is smoke-tested end-to-end on synthetic input.
- **No circularity:** a₀ is fit from each galaxy's own deep-MOND points; the density axis comes from an
  external catalog (group multiplicity / 2M++ / kNN of independent positions), never from a₀.

## 6 · Honest grading (value-coincidence vs universality vs causal)

- **Value-coincidence (unchanged):** a₀ ≈ (c/2)√(G ρ_Λ) holds to ~20%. Neither this test nor BIG-SPARC moves it.
- **Universality evidence (strengthened, already strong):** a₀ is uniform across a 6.4-dex local-density range
  and a real cluster/field split — its source is a **cosmic** field (ρ_Λ reading), not the local ambient
  density. The +½ local-ρ fork is excluded 13–35× today; BIG-SPARC would make this overwhelming and probe the
  ~0.01–0.05 dex residual regime.
- **Causal proof (still out of reach):** showing a₀ *tracks* ρ as ρ changes needs the z≈3 evolution
  `a₀(z)=cH(z)/Z`. BIG-SPARC is z≈0 and **cannot** supply it. That door stays telescope-limited.

**Grade:** environmental fork → **NULL for the local-ρ fork, decisive universality/consistency evidence for
the cosmic-ρ_Λ reading.** BIG-SPARC is not required to reach that verdict; it is the instrument that would
refine it from "the +0.5 fork is dead" to "a₀ is environment-independent to ~0.01 dex, with a powered cluster
contrast." Staged and ready; blocked only by the data release.

---

### Sources
- Haubner, Lelli, et al. (2024), *BIG-SPARC: The new SPARC database*, [arXiv:2411.13329](https://arxiv.org/abs/2411.13329).
- Lelli, McGaugh & Schombert (2016), *SPARC: Mass Models for 175 Disk Galaxies…*, AJ 152, 157; data at astroweb.cwru.edu/SPARC/.
- Li, McGaugh, Lelli, et al. (2018), A&A 615, A3 — a₀ universality across SPARC.
- Tempel et al. (2017), A&A 602, A100 — SDSS DR12 FoF group catalog ([VizieR J/A+A/602/A100](https://vizier.cds.unistra.fr/viz-bin/VizieR?-source=J/A+A/602/A100)).
- Lavaux & Hudson (2011), MNRAS 416, 2840 — the 2M++ density field.
