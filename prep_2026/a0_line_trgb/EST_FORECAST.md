# EST_FORECAST — the TRGB lever on the a0-line (forecast lane)

**Verdict: TIGHTENS-BUT-NON-DIAGNOSTIC (both footings).**
The TRGB/Cepheid distance lever cuts the distance systematic ~3.5× as advertised, but once
the sample is gas-dominated the a0 budget is **floored by the global M/L (Υ), gas-calibration
and estimator-choice systematics** — *above* the error needed to separate the two footings at
2σ. So canonical (a₀ = cH_Λ/Z = 9.36e-11) and alt (cH₀/Z = 1.13e-10) stay **non-separated by
any number of TRGB gas dwarfs alone**. Distance is not the binding systematic here.

Reproduce: `python3 est_forecast.py` (exit 0) → `est_forecast_results.json`.
Machinery reused verbatim from `/prep_2026/a0_line/fire_common.py` (same cuts, iterated
model-based GLS — never observed-error weights, the guard that already caught the fake
3.3e-11 deficit). Both footings from `concordance_ledger/anchor_values.json`. Kernel credit:
ν=√(1+1/y) is Milgrom 1999 PLA 253:273 Eq 9; the framework's content is the coefficient
a₀=cH_Λ/Z. SPARC = Lelli-McGaugh-Schombert 2016; McGaugh+2016 g† = 1.2e-10 quoted for
comparison only.

---

## 0. Does the central STAY at the banked value, or MOVE? — it MOVES UP

Splitting the gas-dominated sample by SPARC distance flag is the honest first look:

| Ud | subsample | Ngal | N | GLS a₀ | median a₀ | tot |
|----|-----------|------|---|--------|-----------|-----|
| 0.7 | full gas (banked) | 49 | 310 | 1.181e-10 | 0.973e-10 | 1.90e-11 |
| 0.7 | **fD∈{2,3} TRGB** | 18 | 147 | **1.333e-10** | **1.273e-10** | 1.71e-11 |
| 0.7 | fD==1 Hubble-flow | 29 | 154 | 0.954e-10 | 0.805e-10 | 1.87e-11 |
| 0.5 | full gas | 62 | 426 | 1.363e-10 | 1.107e-10 | 2.17e-11 |
| 0.5 | **fD∈{2,3} TRGB** | 20 | 191 | **1.490e-10** | **1.426e-10** | 1.85e-11 |
| 0.5 | fD==1 Hubble-flow | 39 | 221 | 1.193e-10 | 0.971e-10 | 2.28e-11 |

The high-quality-distance subsample does **not** stay at the banked 1.181e-10 — it lands
**HIGHER** (1.27–1.49e-10 across estimators and Ud), a ~1.25–1.40× distance-flag split against
the Hubble-flow set. Read as tension: the TRGB GLS central is **+2.3σ (Ud=0.7) / +3.0σ (Ud=0.5)
above canonical**, +1.2σ / +1.9σ above alt; the median estimator agrees in sign (+2.0/+2.7σ vs
canonical). So the clean-distance subsample leans **AWAY from canonical, toward/above alt** —
the opposite of a canonical detection. (Whether this is TRGB-galaxies-are-different selection
or Hubble-flow-distance bias is not resolvable here; flagged both ways.)

---

## (a) FORECAST — error + Occam bans, central held at banked GLS (Ud=0.7)

**Realistic all-TRGB** (re-flag every gas dwarf to σ_lnD=0.05, recompute the full budget):

- sysD: 7.63e-12 → **2.18e-12** (~3.5× cut — the lever fires)
- tot: 1.903e-11 → **1.757e-11** (s_ln 0.161 → 0.149 — barely moves)

because the budget is now floored by **sysU=9.57e-12 (Υ=0.23), sysG=8.63e-12 (gas-cal 0.10),
sysEst=1.04e-11 (estimator spread)**. Distance is not the binding line once gas-dominated.

Occam bans (M0: a₀ fixed at the footing ± Planck anchor vs M1: a₀ free, log-flat), central held:

| scenario | s_ln | B(canon) | B(alt) |
|----------|------|----------|--------|
| banked baseline | 0.161 | +0.60 | +1.04 |
| **all-TRGB realistic** | 0.149 | **+0.56** | **+1.07** |
| idealized σ/2 | 0.081 | −0.44 | +1.29 |
| idealized σ/3 | 0.054 | **−2.45** | +1.39 |
| σ/3, central moved onto each prediction | 0.054 | +1.53 (canon@canon) | +1.53 (alt@alt) |

The banked forecast — "at σ/3 with the GLS central unchanged, canonical → −2.45 bans;
onto the prediction → +1.5 bans" — is **reproduced exactly as arithmetic**. But its premise (a
3× *total*-error cut) is **NOT delivered by TRGB distances**: those cut only sysD, and the
realistic all-TRGB error lands at s_ln=0.149 with bans essentially unchanged from banked
(+0.56/+1.07). The σ/3 world additionally requires beating the global Υ + gas-cal + estimator
systematics — a different, harder lever than distance.

---

## (b) PROVE-BY-MOVING — the TRGB central is not an artifact

Monte-Carlo perturbing every TRGB galaxy's distance within its real 5% error (4000 draws;
D→D(1+δ) scales g_bar and g_obs identically by 1/(1+δ), i.e. slope a₀ → a₀/(1+δ)):

| Ud | Ngal | unperturbed a₀ | MC mean | MC std | jackknife spread | max 1-galaxy shift |
|----|------|----------------|---------|--------|------------------|--------------------|
| 0.7 | 18 | 1.333e-10 | 1.336e-10 | 2.06e-12 (1.5%) | 1.29–1.39e-10 | 7.8% |
| 0.5 | 20 | 1.490e-10 | 1.493e-10 | 2.31e-12 (1.5%) | 1.36–1.56e-10 | 9.0% |

The central is **stable**: MC scatter ~1.5% (consistent with √Σσ_lnD²/N shrinkage) and no single
galaxy moves it by more than ~8–9%. The high TRGB central is a property of the sample, not a
distance-error draw or a single outlier.

---

## (c) DECISIVE-N — how many TRGB gas dwarfs separate the footings at 2σ?

2σ separation needs σ_tot ≤ |Δ|/2 = |1.131−0.935|e-10 / 2 = **9.75e-12**.

Split the budget: **shrinkable** (stat, sysD, sysI, sysEst — per-galaxy / estimator noise,
∝√(N₀/N)) vs **floor** (sysU, sysG — global fully-correlated Υ and gas-cal offsets, do NOT
average down):

| Ud | N₀ | shrinkable(N₀) | global FLOOR | N_decisive |
|----|----|----------------|--------------|------------|
| 0.7 | 18 | 8.86e-12 | **1.46e-11** | **∞ (floor > target)** |
| 0.5 | 20 | 9.50e-12 | **1.58e-11** | **∞ (floor > target)** |

The floor already **exceeds** the 9.75e-12 target, so **no finite number of TRGB gas dwarfs
reaches 2σ separation.** The gate is the global M/L (Υ=0.23) + gas-cal (0.10) systematic —
which distance anchoring does not touch. (Floor-free, i.e. if the global M/L systematic
vanished, the naive stat+distance count would be N~15–19 — but that world requires an external
M/L prior or deeper gas-dominated points where φ→0, not more galaxies.) Symmetric in canonical
vs alt: the verdict is identical for both footings.

---

## Λ-inversion with the tightened a₀ (Λ = 3Z²a₀²/c⁴, Z=5.789)

Planck Λ = 1.089e-52 m⁻². Error doubles in log-Λ space (a₀²):

| a₀ input | Λ_pred | ratio/Planck | σ |
|----------|--------|--------------|---|
| banked GLS | 1.737e-52 | 1.59 | +1.45 |
| all-TRGB GLS (tightened error) | 1.737e-52 | 1.59 | +1.57 |
| TRGB-subsample GLS (moved central) | 2.212e-52 | 2.03 | +2.76 |

The all-TRGB error tightens the inversion only marginally (distance isn't the binding
systematic). Rotation-curve→Λ stays a factor ~1.6 of Planck across ~52 a-priori orders — a
**reframing** of the a₀≈cH_Λ/Z coincidence, not new cosmological data. If the *moved* TRGB
central (2.2e-52) is taken at face value the inversion overshoots Planck at +2.8σ — another
reading in which the clean-distance data does not favor the canonical footing. No "proves".

---

## Honest bottom line

- The distance lever works on **its own line** (sysD −3.5×) but is **not decisive**: the a0-line
  budget is floored by global M/L + gas-cal + estimator systematics above the footing-separation
  threshold. **UNDERPOWERED-BY-FLOOR, not by count.**
- The clean-distance subsample central **moves UP, away from canonical** (~2–3σ high) — so this
  lever gives **no support to canonical 9.36e-11**; if anything a mild upward lean, but within
  the honest error it is a lean, not a detection. Consistent with the banked "no usable footing
  lean, estimator-owned central" once the systematics floor is respected.
- To actually separate cH_Λ/Z from cH₀/Z you need to beat the **global M/L systematic** (external
  stellar-pop Υ priors or deep φ→0 gas-only points), plus the CCHP/EDD TRGB program or BIG-SPARC
  for the count — the distance flag alone is a ~3× sysD win, not the discriminator.
