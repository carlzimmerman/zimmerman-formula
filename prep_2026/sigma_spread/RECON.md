# LANE R — Relational σ-spread: prediction re-derived + 2026 data recon (2026-07-16)

**Scripts (all exit 0, this directory):** `rederive_mi_spread.py` (+`.out`), `estimator_power.py` (+`.out`),
`census_verify.py` (+`.out`); touched data in `data/`. Frozen-repo sources read (read-only):
`opus_48_extended_research/reviews/CLUSTER_SIGMA_SPREAD_PREDICTION_2026-06-19.md`,
`GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md`, `sigma_predict/*.py`, `sigma_spread/*.py`
(incl. `EXISTING_DATA_SIGN_PILOT_2026-06-26.py`), `mi_kernel/kernel_constraints.py`.

## 1. The prediction, re-derived from the framework's own premises (not taken on faith)

Modified INERTIA is time-nonlocal: a member with internal frequency ω_in in a cluster field varying
at ω_ex feels A = a_in + a_ex·θ(y), y = ω_ex/ω_in (Milgrom 2022 PRD 106 064060 Eq.34-class);
boost B = 1/μ_fw(A/a0) with μ_fw the **exact inverse of the framework's own ν(y)=√(1+1/y)**
(verified <1e-12). σ ∝ √B. The observable is the pure relational ratio R(y)=σ(y)/σ_QS at **matched
momentary a_ex and matched internal baryons** — plungers (large y) shed adiabatic EFE loading → run
HOTTER than settled members at the same radius.

- **Reproduced banked numbers (canonical footing a0=9.36e-11, canonical member a_in=0.3a0, a_ex=2a0):**
  Milgrom-kernel band **6.4–12.0%** over y≤1.5 (fiducial rational θ: **10.4%**); at Milgrom's own
  y≤1 the core member drops to **3.9–6.5%** (banked correction reproduced); model-independent cone
  **4.59–17.61%** (exact banked values). Amplitude is **kernel-hostage** (θ(y) not derived; only the
  cone is dS-Unruh-constrained) — conceded at full weight.
- **Both footings:** alt a0=1.13e-10 moves the y≤1.5 band to 7.6–14.4% (band ends shift ~20%
  relative); the a_ex=a0 shell of a 1e15 M⊙ cluster sits at 1.22 Mpc (canonical) vs 1.11 Mpc (alt).
  The discriminator is **not footing-hostage**.
- **Radial structure:** the spread peaks at a_ex ≈ 0.3–0.4 a0 (outer MOND-transition shell,
  ~R500–R200: 11.6% even at y≤1) and dies toward the core — the anti-correlation with tidal heating
  is the CDM separator.
- **Orbit shape enters ONLY through y:** plunging radial orbits near pericenter reach y~1–2 for
  diffuse members (UDG σ~15/Re~3kpc: y≈2.0; dSph: y≈1.0), while dE (σ~50) reach only y≈0.3 and
  L* ellipticals y≈0.2 → predicted spreads UDG ~24%(at a_ex=a0)/dSph ~11% vs dE **0.7%** / L* **0.1%**.
  **The σ-measurable-by-survey members are adiabatic-dead by the same physics that creates the signal.**
- **WHAT IS EXACTLY ZERO IN MG (made precise + proven symbolically):** in ANY elliptic MG realization
  (AQUAL/QUMOND/AeST) the internal dynamics depends on the external field only through its **momentary**
  value, so at matched (a_ex, internal baryons): dσ_int/dy ≡ 0 for **symbolic arbitrary interpolation μ
  and any a0** (sympy, plus numeric a0×{0.5,1,2}). Precisely: **Var_y{E[ln σ_int | a_ex, baryons]} = 0**
  — the relational spread after controlling radius and mass. Only the y-dependence is MG-impossible
  (constant θ(0) is absorbable, Eq.35 trap).

## 2. The operational estimator (pre-registered form)

Per cluster: (i) FJ residual d_i = ln σ_i − ⟨ln σ|L,Re⟩; (ii) restrict to the R500–R200 shell;
(iii) infall proxy p_i from projected phase space (caustic membership + k_r), dilution D≈0.4;
(iv) statistic = slope b of d_i on p_i (and the excess-variance variant). **MI: b>0, Δ_obs =
D(1−ε_int)f; MG: b=0 exactly.** Null calibrated by shuffling p_i (preserves FJ scatter, noise,
radial trends). Confounds enter as: interlopers → pure dilution; **substructure → the one confound
that can fake b≠0 in MG** (shared infall history correlates σ-residual with PPS position) → must be
CUT (Dressler-Shectman), not shuffled; FJ intrinsic scatter → noise floor (dominates over ELT
measurement error); CDM tidal heating → same-signed but radially anti-correlated + cumulative +
strips (banked S1–S3) — a confound on the MI interpretation, separable by the radial profile of b.

**Power (two-bin, 3σ vs MG=0, honest noise = meas ⊕ s_FJ):** the banked "N~100–180 (ELT)" is
recovered only as the upper-band/no-interloper measurement-only corner (N≈134–165). With the honest
FJ floor s_FJ≈0.15: fiducial ELT **N≈903**; best realistic corner (f=13%, s_FJ=0.08) **N≈270**;
today's 20–40% errors **N≈1,850–8,700**. The banked feasibility was optimistic ×2–5 — the binding
noise at ELT is intrinsic M-σ scatter, not the instrument.

## 3. The 2026 public-data census (every catalog actually touched; `census_verify.py` re-runs it)

**Load-bearing correction to the tasking premise: DESI DR2 public spectroscopy does NOT exist as of
2026-07-16.** `data.desi.lbl.gov/public/dr2/` → **HTTP 401** (collaboration-only); the official
releases page lists only EDR (2023) and **DR1 (2025-03-19, 18.7M spectra)**; the public index HTML
carries the dr2 entry **commented out** (staged, not live). The 2026 re-scope therefore runs on DR1.

| # | Catalog (touched how) | N_clusters | Members | Velocity quantity + precision | Carrier σ? |
|---|---|---|---|---|---|
| 1 | **DESI DR1 gfinder VAC** (remote FITS headers + 30MB head parsed) | 99.6M groups; ≥1,273 w/ RICH≥100, ≥7,274 w/ RICH≥50 (head; photo+spec mix) | 134.7M links | member v_los ~10–30 km/s (Redrock) | **NO** |
| 2 | **DESI DR1 extragalactic-dwarfs VAC** (header + 18.8k-row head) | — | 647,241 dwarfs, cols Z/MU_R/SHAPE_R/LOGM | redshifts only | **NO** |
| 3 | **HeCS** Rines+2013 (VizieR full download) | 58 | 22,680 z's; median 173 members/cluster (61–461) | e_cz median 36 km/s | NO |
| 4 | **HeCS-SZ** Rines+2016 (full download) | 123 | +11,585 z's | same | NO |
| 5 | **HeCS-omnibus** Sohn+2020 (full download) | **227** | **52,415 members** (median 180, max 1209); N200 sum 22,091 | caustic membership, σ_cl, R200 | BCG σ only (adiabatic-dead) |
| 6 | **GalWCat19** Abdullah+2020 (full download) | 1,800 | 34,471 | SDSS z's | NO |
| 7 | **CAIRNS** Rines+2003 (full download) | 9 | 19,796 | deep infall-region z's | NO |
| 8 | **Sohn+2017 A2029** member-σ (full download) | 1 | 982 rows, 924 with internal σ, median err 20% | reliable σ only ≳60 km/s | dE/E only → f~0.7% → N~10^5: **dead route** |
| 9 | **Gannon+2024 living UDG catalog** (github, full download) | ~10 hosts | **38 UDGs; 24 with stellar σ (23 cluster/group)**, median err 24% (6–46%) | the actual carriers | **YES — the entire reservoir** |

Survey-resolution wall (arithmetic in `estimator_power.py`): instrumental σ floor DESI 23–64 km/s,
SDSS ~64, MUSE ~42 vs carriers at 8–20 km/s → no survey spectrograph can measure carrier internal σ;
ELT-HARMONI (~7 km/s floor) is the first that can, ~2032.

## 4. Verdict (both ways, firewalled)

- **STILL UNDERPOWERED — quantified:** need ~270–900 infall-tagged, outer-shell, undisrupted
  diffuse carriers with ≲10% internal-σ errors (or ~1,850–8,700 at today's 20–40%); the entire 2026
  public reservoir is **23 cluster/group UDGs with stellar σ at ~24% median error**, not infall-tagged.
  Gap: **×15–60 in N at a precision tier that does not exist before ELT (~2032); ×~100+ today.**
  Any firing on the 23 in-hand objects is **EXPLORATORY/FIREWALLED** (cannot support or kill) — the
  pre-derived power analysis says ~0.2–0.6σ, consistent with the banked 2026-06-26 pilot.
- **What genuinely improved (credited at full weight):** the phase-tagging side is now solved and
  free — HeCS-omnibus (227 clusters/52k members with caustics), GalWCat19, CAIRNS, and DESI DR1's
  gfinder (≥10³ rich clusters) + the 647k-dwarf VAC (carrier identification at survey scale). When
  ELT-class carrier σ's arrive, targets can be pre-tagged from public data with D possibly 0.4→0.6
  (N×0.45). A concrete NOW-item: cross-match the DESI dwarf VAC (MU_R>24 tail, ~30k LSB dwarfs)
  against HeCS-omnibus/gfinder clusters to build the pre-registered ELT target list.
- **What got harder (conceded at full weight):** the honest FJ-scatter floor raises the banked
  ELT-era N by ×2–5; substructure is the one MG-null-breaking confound and requires an explicit cut.
- **Unchanged assets:** MG=0 is a theorem (symbolic, any a0, any interpolation, both footings);
  sign (plungers hotter) and radial anti-correlation vs tides are kernel-independent; the amplitude
  band 6–13% (cone 5–18%) is kernel-hostage as banked.
