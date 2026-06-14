# SZ + the baryon census to the virial radius — is the missing mass missing BARYONS, and can we count them?

*2026-06-14. Modality sz_baryon_census. Carl's ask: pull the latest 2023–2026 SZ/kSZ/eROSITA census AND design the
concrete measurement — how much does measured η drop if the true baryon is counted to r200, and what precision does
SO/CMB-S4+eROSITA deliver, on what timeline? Both ways. Framework a0=9.36e-11 throughout; quarantine held.*

---

## 1. The latest census (2023–2026): the gas is being FOUND, but it sits OUTSIDE the virial radius

Three independent probes now agree, and all say the same radius-dependent thing:

| probe (year) | within R500 | within R_vir / R200m | where it reaches cosmic |
|---|---|---|---|
| **Hadzhiyska, Ferraro+ 2025** (kSZ ACT DR6 × DESI LRG/BGS, PRD `mdhz-fgj8`/2507.14136) | — | **f_gas ≈ 0.3 cosmic** for LRG groups (log M_h≈13.0–13.5) | **2–3 R_vir** ("recover all baryons") |
| **Roper, Cai, Peacock 2025** (kSZ ACT × DESI Legacy, 2510.12553) | — | **0.38 ± 0.11 × cosmic** within R_vir (low-mass 10^12.5–10^14); **massive groups = cosmic within R_vir** | well beyond R_vir |
| **eROSITA outskirts stack 2026** (680 clusters, 2509.25317 / A&A 2026) | **~65% cosmic** | **~80% (clumping-corr), ≳100% (uncorr)** at R200m | ~R200m (~4.5 Mpc, 2×R200m detected) |
| **DESI DR2 × ACT DR6 Part II 2026** (2604.19745) | — | BGS: **low** f_gas at R_vir (AGN); ELG: high; S/N up to 9 (BGS), 7.5 (ELG) | beyond R_vir |
| **X-COP** (Eckert+ 2019, the gas-complete anchor) | f_gas,500=0.141±0.005, +7% above universal | total f_b ≈ cosmic at R200 | R200 |

**Net:** The cluster missing-baryon problem is essentially SOLVED by 2024–2026 — the baryons are real and are being
counted — but they are **expelled by feedback to 1–3 virial radii**. Within R500 the gas is ~65% cosmic; within R_vir
~38–80% cosmic for groups (mass-dependent), reaching cosmic only at 2–3 R_vir. The cosmic baryon fraction is recovered
at the largest apertures; **the depletion within the virial radius is real and feedback-driven**, not a measurement gap.

## 2. HOW MUCH does η drop if the true baryon is counted to r200? (real eRASS1, framework a0, both readings)

η ≡ g_obs/(ν·g_bar), framework a0=9.36e-11, dS-Unruh ν, N=9830 clean eRASS1 (Bulbul+2024). **The answer depends on
WHICH radius you evaluate η at — and this is the load-bearing subtlety, reported both ways:**

**Reading A — η AT R500 (g_bar there depends ONLY on the WITHIN-R500 baryon):**
| within-R500 baryon | η_median |
|---|---|
| gas only (catalog) | 2.61 |
| gas + 0.2·gas stars (banked) | 2.37 |
| **65% cosmic gas + stars (eROSITA 2026 census)** | **1.99** |
| 100% cosmic crammed in R500 (counterfactual; census says NOT there) | 1.69 |

→ Counting the *expelled* gas to R200m does **NOT** lower g_bar at R500 — that gas is at r>R500 and contributes zero
to g_bar(R500). At R500 the honest census floor is **η≈1.7–2.0**. This is the deep-dive's crux (a), confirmed.

**Reading B — η AT the virial radius R200m (~2×R500), where the census IS near-cosmic:**
| baryon within R200m | η_median | note |
|---|---|---|
| 65% cosmic (R500 value, no climb) | 1.40 | |
| **80% cosmic (clumping-corrected eROSITA)** | **1.26** | the honest central census value |
| 100% cosmic (uncorrected) | 1.12 | upper bound |

The deep-MOND self-consistency check (NOT an assumption artifact): at R200m with cosmic baryon, MOND's *predicted*
boost ν = M_pred/M_bar ≈ **5.7**, while explaining the observed M_dyn from cosmic baryon needs 1/f_b = **6.4** →
η = 6.4/5.7 = **1.12**. **So η DOES fall toward ~1.1–1.3 at the virial radius when the enclosed baryon is near-cosmic.**

**This is genuine and must be stated as a real reducer — it is exactly the observed "central η high → ~1 at the
outskirts" shape (eRASS1, CLASH), not a manufactured cure.** But it does NOT reach 1: a residual **~10–30% survives at
R200m**, and the deficit is **concentrated centrally** — precisely where the census says the baryon is MOST depleted
(38% cosmic within R_vir for low-mass groups, Roper+2025) AND where MOND needs the LARGEST boost.

## 3. Both ways — does the central residual survive in the NEWEST gas-complete data? YES.

- **Zhang/Kroupa et al. 2026 (2602.06082, 46 WINGS+2MASS clusters):** with a COMPLETE canonical baryon budget
  (ICM + stars + ICL + remnants), baryons = **52% of MOND dynamical mass → η≈1.9 persists**. Only the *contested*
  IGIMF route (extra stellar remnants) reaches 88% (η≈1.14). So even with the full canonical census the residual is real.
- **Pizzuti & Famaey 2025 (PRD `dccw-srks`/2410.02612, CLASH lensing):** the residual missing mass is **centrally
  concentrated** — missing/hot-gas density ratio ~10 inside a ~450 kpc core, exponential cut-off, dies faster than the
  gas outward. The found census baryons sit at >R500; the MOND residual sits at <450 kpc — **spatially disjoint**.
- **X-COP (gas-complete, near-cosmic at R500):** central residual ~2× is robust at R500 exactly where the gas budget
  is most complete. Completing the budget helps depleted groups, not the gas-complete cores.

So the SZ+kSZ census closing the cosmic missing-baryon problem **simultaneously closes the missing-baryon escape for
the cluster MOND deficit**: the baryons are real, located, collisional, and outside — the wrong place, behaviour, and
radius to be the central residual.

## 4. THE CONCRETE MEASUREMENT — can SZ+kSZ+eROSITA count the baryon to r200 and resolve η there?

**The test:** measure the stacked enclosed baryon f_b(<R200m) AND the lensing M_dyn(<R200m) for cluster/group bins,
form η(R200m), and ask whether it sits at 1.12 (residual survives) or 1.0 (closed). Deep-MOND error propagation:
η ∝ √(M_dyn/(f_b·R²)) ⇒ to separate 1.12 from 1.0 (a 12% gap, 2σ) needs **σ(η)/η < 6% ⇒ σ(f_b)/f_b < ~12%** on the
enclosed baryon at R200m (and matched-aperture lensing M_dyn to ~10%).

| era | enclosed-baryon precision at R200m | σ(η) | verdict |
|---|---|---|---|
| **NOW (2024–2026)** | eROSITA clumping syst. ~20%+ (1.5× factor); kSZ f_b,vir=0.38±0.11 = 29% | ~10–15% | **cannot yet separate 1.12 from 1.0** |
| **SO LAT (first light 2025; full 2028; survey →2034)** | kSZ gas profile ~2 dex better than ACT+BOSS; feedback efficiency to **2%**; 33,000 tSZ clusters; gas-profile shape to **few-%** | **~2–4%** | **DECISIVE — separates 1.12 vs 1.0 at >3σ** |
| **CMB-S4 (~2032+)** | **10–20%** on gas-density-profile SHAPE from kSZ×CMB-lensing with NO external data; few-% with eROSITA/DESI priors; relativistic-tSZ density via T_e | **few-%** | confirmatory, external-data-free |

Supporting current SZ profile work: SPT-3G/ACT DR6 tSZ pressure profiles now reach **R/R200m ≈ 1.1** (6σ pressure
deficit / accretion-shock feature, DES×SPT×ACT ~10^5 clusters); ACT DR6 SZ cluster catalog 2025 (2507.21459); SPT+Planck
hierarchical pressure profiles to >R500 (2025). So the *radial* tSZ+kSZ machinery to the virial radius already exists;
what SO/CMB-S4 add is the **precision** to pin the enclosed baryon (hence η) to a few percent.

**Mass-calibration is the second leg:** η needs M_dyn(<R200m). ACT DR6 CMB-lensing already calibrates stacked group
masses to ~0.1 dex (Hadzhiyska+2025); SO/CMB-S4 CMB-cluster-lensing + Rubin/Euclid weak lensing deliver matched-aperture
M_dyn to ~5–10% per bin. The cross-method WL-vs-hydrostatic ~110% offset (Li+2024) is the dominant *current* systematic
on absolute η — kSZ (density) + relativistic-tSZ (temperature) give a hydrostatic-independent gas mass, breaking it.

## 5. The framework-DISTINCTIVE test this modality enables (vs shared MOND)

The η(R200m)→~1 drop is a **MOND-shared** result (any constant-a0 MOND predicts the same outskirt convergence). The
framework's DISTINCTIVE content is the **density-law superset a0_local=(c/2)√(G·ρ_total)**: in the dense core ρ_total ≫
ρ_DE, so a0 is LOCALLY BOOSTED by √(ρ_local/ρ_DE) — **extra amplification exactly where η is largest (central)**.
Constant-a0 MOND predicts NO central a0-enhancement. So the **radial η(r) shape from SZ+kSZ+eROSITA is the discriminator**:
- **Confirms the framework** if the central η-excess (η~7–10 at 0.1R500 → ~1.2 at R200m) tracks the central density-a0
  boost with the SAME ρ_total↔a0 mapping that leaves the **tight galaxy RAR unsmeared** — i.e. a DERIVED smoothing scale
  that threads galaxies + cluster cores.
- **Kills the framework's distinctive angle** if (i) the central η-excess matches plain constant-a0 MOND with NO density
  boost needed (then a0_local>a0_field is superfluous), OR (ii) the ρ_total↔a0 mapping required to fit cluster cores
  smears the galaxy RAR beyond its observed ~0.13-dex tightness (the standing trap — no derived scale does both yet).
- **The a0_local>a0_field prediction is independently measurable:** stack η(r) in bins of LOCAL environmental density
  (cosmic-web node vs field) at fixed M_bar — the framework predicts a0, hence the deep-MOND amplitude, RISES with
  ρ_local. SO/CMB-S4 tSZ+kSZ × DESI/Rubin density fields can build exactly this stack by ~2030.

## Verdict (both ways)

**The missing mass is NOT missing baryons — over-determined by the 2023–2026 SZ/kSZ census — AND the census is now
precise enough to MEASURE η to the virial radius, with SO/CMB-S4 making the test DECISIVE.**
- *Carl's premise vindicated:* the within-R_vir baryon IS incomplete (38–80% cosmic, mass-dependent), the missing
  baryons ARE real, and counting them to R200m is a GENUINE reducer — η at the virial radius falls to **~1.12–1.26**,
  the observed central→outskirt shrinking shape, NOT a manufactured cure. Do NOT say "baryons are fully counted within
  R_vir" (false) or "the census doesn't move η" (false at R200m).
- *But refuted at the level that matters:* η at R500 floors at ~1.7–2.0 (expelled gas can't act there); a **central
  ~10–30% residual survives even at R200m**; with the COMPLETE canonical census (Zhang/Kroupa 2026) η≈1.9 persists
  (52% unexplained); the residual is central + collisionless (Famaey-Pizzuti core + Bullet JWST), disjoint from the
  outskirts census gas. The found baryons are the wrong place, radius, and behaviour to be the missing mass.
- *Framework-distinctive:* density-a0 predicts the central a0-boost matching the central η-excess — the ONE live
  discriminator — but rides on an underived smoothing scale and inherits the framework's +13% (lower a0) surcharge. The
  SZ+kSZ radial η(r) + density-binned a0-stack is the concrete test; SO (2028+) reaches the few-% baryon precision to
  resolve it at >3σ.

## Sources
- Hadzhiyska, Ferraro, Farren+ 2025, PRD `mdhz-fgj8` (arXiv:2507.14136) — kSZ+CMB-lensing; f_gas≈0.3 cosmic at R_vir
  for LRG groups; baryons recovered at 2–3 R_vir; TNG300 over-predicts by ≳4σ.
- Roper, Cai, Peacock 2025 (arXiv:2510.12553) — kSZ mass-dependence; f_b,vir = 0.38±0.11 cosmic (low-mass), cosmic for
  massive groups within R_vir.
- DESI DR2 × ACT DR6 Part II 2026 (arXiv:2604.19745) — BGS/ELG kSZ S/N≤9; low BGS f_gas at R_vir (AGN).
- eROSITA outskirts stacking 2026 (arXiv:2509.25317 / A&A 2026, 680 clusters) — ~65% cosmic by R500c, ~80% (clumping-
  corr)/≳100% (uncorr) at R200m; n_gas(R200m)=2.5e-5 cm⁻³, baryon overdensity 30, detected to 2×R200m.
- Eckert+ 2019 X-COP (A&A 621 A40) — f_gas,500=0.141±0.005, near-cosmic at R200 for massive relaxed clusters.
- Zhang, Zonoozi, Kroupa 2026 (arXiv:2602.06082, 46 WINGS+2MASS clusters) — canonical baryons = 52% of M_dyn(MOND)
  (η≈1.9 persists); IGIMF → 88% (contested).
- Pizzuti & Famaey 2025, PRD `dccw-srks` (arXiv:2410.02612) — CLASH lensing: central core ~450 kpc, ratio ~10,
  dark-follows-gas, dies faster than gas outward.
- Bullet JWST 2026 (arXiv:2605.10022) — residual centred on galaxies, collisionless.
- SO Collaboration 2025, JCAP 08 034 (arXiv:2503.00636) — enhanced LAT: 33,000 tSZ clusters, kSZ gas profile ~2 dex
  over ACT+BOSS, feedback efficiency 2%, σ(τ)=0.0035; first light 2025, full 2028, survey →2034.
- Hadzhiyska+ 2023, JCAP (arXiv:2208.07847) — CMB-S4 kSZ×CMB-lensing: 10–20% on gas-density-profile SHAPE, no external
  data; SO×unWISE 62σ.
- DES×SPT×ACT 2024 — tSZ pressure deficit at R/R200m≈1.1, 6σ, ~10^5 clusters.
- Bulbul+ 2024, A&A 685 A106 — eRASS1 catalog (on disk).
