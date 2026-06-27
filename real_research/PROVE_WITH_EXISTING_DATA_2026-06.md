# PROVE WITH EXISTING DATA — the honest two-tier map (2026-06-26)

**Assumption (granted, not re-litigated):** a₀ = c²√(Λ/32π) = 9.36e-11 m/s² and dS-Unruh
MODIFIED INERTIA correct. Question: what POSITIVE distinctive result is provable NOW, with data
already published/in-hand — no future survey?

**Verdict in one line:** With existing data the framework **decisively beats ΛCDM** (real, in-hand,
MOND-shared) — but **NOTHING in hand separates dS-Unruh MI from standard/metric MOND**. The one
MG-impossible lever (the σ-spread sign) is genuinely the right discriminator and is **buried below
existing precision, not absent** — it is an ELT-era (2032+) test. No manufactured win; no high-priesting
of the real ΛCDM chicken.

All scripts re-run this session, exit 0, real published numbers (no synthetic data):
- `opus_48_extended_research/reviews/sigma_spread/EXISTING_DATA_SIGN_PILOT_2026-06-26.py`
- `opus_48_extended_research/reviews/mine2_rar_universality_INHAND.py` (+ `mine2b`, `mine2c`)
- `opus_48_extended_research/reviews/a0z_desi.py`
- grounded in banked `CLUSTER_SIGMA_SPREAD_PREDICTION_2026-06-19.md`,
  `CLUSTER_SIGMA_SIGN_IS_MOND_SHARED_2026-06-15.md`, `SPARC_RAR_FOOTING_BOTHWAYS_2026-06-13.md`.

---

## TIER 1 — vs ΛCDM: PROVABLE NOW (real chicken, fully MOND-SHARED)

The MOND family already owns these; the framework inherits them. None is framework-distinctive.

### 1a. RAR tightness — YES, provable now (SPARC 175 RCs, Lelli+2016)
On the framework's OWN footing (Υ=0.70, dS-Unruh ν, a₀=9.36e-11), 2778 points / 151 galaxies:
- Global vertical scatter **0.142 dex**; free-optimal a₀=1.039e-10 → 9.36e-11 sits −9.9% below
  optimal with a penalty of only **+0.0009 dex (+0.67%)**. Reproduces SPARC_RAR_FOOTING_BOTHWAYS.
- Velocity-error budget alone ≈ 0.04 dex; full Li+2018 M/L+distance+inclination budget drives
  intrinsic scatter to **~0.057 dex, consistent with zero**.
- **One parameter reproduces 2778 points to ~0.057 dex intrinsic** — this is what ΛCDM
  galaxy-formation does NOT natively produce. The "25–62σ too tight" is the **model-comparison**
  number (RAR-vs-feature-rich-halo Bayesian odds, Li+2018), a real published vs-ΛCDM result.

**Both-ways corrections (do not re-cite the old numbers):**
- The banked "0.110 dex / beats reg-MOND" is **NOT reproduced** — it is 0.142 dex, and reg-MOND on
  McGaugh ν (Υ=0.50) gives 0.1408 dex: a **statistical WASH**. No robust scatter advantage for the
  framework footing over regular MOND. dS-Unruh ν vs McGaugh ν is only ~1–2% (0.1419 vs 0.1439 dex)
  — far below noise, NOT a vs-MOND discriminator.

### 1b. a₀ universality — DOWNGRADE a banked overclaim
- The per-galaxy a₀ fit is M/L-degenerate → spurious +0.130/121σ "flat" slope (an artifact).
- Done properly (5 shared-a₀ mass bins): a₀ **runs 8.7e-11 → 1.53e-10, factor 1.76**,
  constant-a₀ rejected at **χ²=2681/4dof**. a₀ is NOT measurably invariant across galaxy mass in a
  direct binned fit (high-mass bulge-dominated galaxies barely sample deep-MOND → a₀ poorly
  leveraged). **The "25–62σ too tight" must NOT be re-cited as clean a₀ universality** — it is a
  model-comparison σ, not an a₀-invariance σ.

### 1c. EFE detection — YES provable now, MOND-shared + contested (Chae 2021, ~5σ)
- The framework's MI-EFE **reproduces** the Chae 2021 ~5σ RC downturn. The deep-MOND EFE suppression
  D = [√(g_N+g_ext)−√(g_ext)]/√g_N is **a₀-INDEPENDENT** (D=0.268 identically for 9.36e-11 and
  1.2e-10 at fixed g_ext/g_N) → the detected SHAPE is reproduced; the smaller a₀ shifts e_N up ~+28%,
  inside Chae's per-galaxy scatter.
- vs-ΛCDM this is **LCDM-impossible physics** (SEP forbids any RC downturn from a uniform external
  field) that the framework predicts — but it is MOND-shared and the detection is contested
  (Banik/Pittordis/Saad-Ting wide-binary nulls).

### 1d. a₀(z) / DESI DR2 — provable-now DETECTION that a₀ evolves, but NON-DIAGNOSTIC
- Framework a₀(z)=√(ρ_DE(z)/ρ_DE0) is parameter-free given w(z) (κ,c,Z,interp cancel).
- DESI DR2 rejects w=−1 (=constant a₀) at 2.8σ→4.2σ. On the framework's own reading that is a
  detection a₀ evolves. The distinctive **+6% bump sits algebraically at DESI's phantom crossing
  z≈0.405** (peak==crossing for any w0>−1,wa<0; a0z_desi.py: DESY5 +6.0%, Pantheon+ +3.6%).
- **Both-ways:** this is ΛCDM-degenerate and dissolves if w→−1. NON-DIAGNOSTIC now. Not a clean
  in-hand win; it is a hostage to the DESI w0wa result holding.

**TIER-1 net:** the framework beats ΛCDM on real, published, in-hand data (RAR tightness + EFE
detection). **Every one of these is MOND-shared** — none distinguishes the framework from MOND.

---

## TIER 2 — vs MOND (THE BIG ONE): is ANYTHING in hand distinctive? — NO

The ONLY MG-impossible, no-particle lever is the **σ-spread sign**: at matched cluster radius, a
member's internal σ vs its infall phase y=ω_ex/ω_in. MI (non-local in time) → plungers run hotter,
**dσ/dy > 0, +6–13%**. MG → **dσ/dy ≡ 0 EXACTLY** (machine-verified + symbolic theorem, any a₀, any
interpolation — depends only on momentary a_ext). CDM ≈ 0. This is the cleanest distinctive asset and
the right discriminator.

### The σ-spread PILOT on EXISTING UDG kinematics — NULL, below existing noise
Real published per-object samples: **Coma UDGs** (Gannon+ living catalogue, arXiv:2405.09104 — Y358,
DF44, DFX1, DF17/Yagi…) + **Hydra-I LEWIS-II** (Iodice/Buttitta 2025: UDG1,4,7,9,11,12). N=14 objects
with measured σ.

- Real per-object σ precision: **median 26%, range 9–47%** — 2.6× too coarse for the ~10% intrinsic
  per-object spread.
- After the projected-phase-space proxy dilution (×0.4): observed high-vs-low-infall spread only
  **~2.4–5.2%**, vs MG=exactly-0 theorem and CDM≈0.
- Power calc with the ACTUAL sample (N~6–14/cluster → 3–5 per infall bin): **sign significance
  0.1–0.4σ — indistinguishable from zero.** Did NOT manufacture even a 1σ hint.
- Optimistic full global stack N~100/bin (~200 infall-tagged UDGs — **does not exist in 2026**; the
  entire global UDG-σ sample is ~40 objects) reaches only **~1.3σ** at the optimistic 5% spread. 3σ
  needs ~5–10× the existing sample.
- **MUSE-HFF cannot help:** the diffuse 8–20 km/s carriers sit below its integrated-light σ floor; it
  resolves only bright ellipticals — the Faber-Jackson WRONG sample (sign flips +, the banked
  CLUSTER_SIGMA_SIGN_IS_MOND_SHARED trap).

### Why it is buried (three independent walls, all checked vs real 2026 numbers)
1. Per-object σ precision 16–47% vs the ~10% needed.
2. Sample size ~6–14/cluster vs the ~200 infall-tagged needed for 3σ.
3. Infall-proxy dilution (×0.4).
The irreducible anti-correlation: ~1–2 km/s resolved-STAR σ exists only for D<~5–20 Mpc Local-Group
dSph, while the infall-phase cluster population lives at Coma/Hydra (~100 Mpc) where stars are
unresolved → integrated-light σ at 16–45%. **Distance and precision are anti-correlated exactly where
the signal lives.**

### The other in-hand vs-MOND probes are a₀-degenerate, not just noisy
- **EFE (Chae/Gaia DR3 wide binaries):** MI-EFE (γ_g~1.05–1.10) vs MG-EFE (~1.13) differ by Δγ_g~0.11
  = **0.53σ** of Chae's error, AND a constant θ0 is **EXACTLY a₀-degenerate** (MI(θ0=k)≡MG(a₀/k)) —
  even a perfect single-external-field measurement cannot separate them. The framework's a₀ predicts
  γ_g BELOW Chae 2023's 1.49 (consistent with the Saad-Ting skeptic camp) — **so Chae 1.49 must NOT
  be cited as support** (that would be a manufactured win).

**TIER-2 net: NO provable-now framework-vs-MOND result.** The σ-spread is the real distinctive lever,
the sign is the right discriminator, the MG=0 theorem is verified — but existing data give an
**upper-limit / proof-of-concept only**. No positive distinctive σ-spread result is provable now.

---

## NEXT STEP TO SHARPEN (the only thing that flips Tier 2)
The σ-spread needs **resolved-star σ (~0.5–2.6 km/s on σ~8–20 km/s)** on ~100–200 infall-tagged
diffuse UDG/dSph members in the outer MOND-transition shell (a_ext~a₀, ~R500–R200, where the carrier
signal lives and tides are 2–3 orders quieter). Timeline: NOW (2026–27) recast LEWIS Hydra-I + Coma
KCWI → upper-limit/method-paper ONLY; 2028–32 dedicated VLT-MUSE/Keck-KCWI N~100–200 → conditional ~3σ
IF θ(y) is upper-band; 2032+ ELT-HARMONI/MOSAIC → definitive 3–5σ vs MG.

---

## WHAT TO TELL CARL (both ways, no manufactured win)
- **TODAY, vs ΛCDM:** you win, for real, on data already published — RAR tightness (one parameter,
  ~0.057 dex intrinsic, SPARC 175) and the ~5σ EFE detection (LCDM-impossible SEP-violating physics).
  Cite these as the in-hand chicken — but say plainly they are **MOND-shared**, not yours alone.
- **Correct two banked numbers when you cite them:** RAR scatter is 0.142 dex (not 0.110) and ties
  reg-MOND — no robust advantage; and a₀ is NOT measurably invariant across galaxy mass in a direct
  binned fit (factor-1.76, χ²=2681/4dof) — the "25–62σ" is a model-comparison σ, not a₀ universality.
- **TODAY, vs MOND:** nothing in hand separates dS-Unruh MI from standard/metric MOND. The σ-spread
  sign is genuinely your one MG-impossible, no-particle lever and the MG=0 theorem is verified — but
  with the real 2026 UDG samples it sits at 0.1–0.4σ (best-case stack ~1.3σ, and that sample does not
  exist). It is an **ELT-era (2032+) prediction-table asset**, not a provable-now win.
- **Don't:** cite Chae 1.49 as support (your a₀ predicts lower), present the a₀(z) bump as a clean win
  (NON-DIAGNOSTIC, dissolves if w→−1), or present RAR/a₀-universality as framework-distinctive.
