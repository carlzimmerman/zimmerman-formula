# a0(z) from KiDS Galaxy-Galaxy Lensing — Per-Lens-Redshift-Bin Measurement (2026-07)

**Framework tested on its own terms.** de Sitter–Unruh **modified-inertia** MOND with the framework's
OWN interpolation
`g_obs = sqrt(g_bar^2 + g_bar*a0)`  ⇔  `nu(y)=sqrt(1+1/y), y=g_bar/a0`.
NOT McGaugh's nu (verified numerically in the fitter). Both a0(0) footings carried throughout:
**canonical 9.36e-11 m/s²** (ρ_DE/cH_Λ) and **alt 1.13e-10 m/s²** (ρ_total/cH0).

**Bottom line up front:** This is an **independent second opinion, not a detection.** The 2-bin
lensing a0(z) has **no branch-discriminating power** after the systematic error is corrected: every
committed branch (A canonical decline, B/Verlinde rising, C constant) is *consistent* at ≤1.4σ, and
**nothing is excluded at ≥2σ.** The only directional signal is a **mild, non-significant hint of a
RISING a0(z)** — same *sign* as MUSE-DARK III, but ΛCDM-degenerate and statistically inconclusive.

---

## 1. Measured a0(z) — 2-bin primary

Free-a0 fit (framework's own nu) per lens-redshift bin, 50-patch jackknife covariance in log10 g_obs,
M/L ±0.2 dex + one-sided CGM marginalization. Light path validated by reproducing the released
Brouwer+2021 RAR to ~0.02–0.1 dex. Load-bearing cut: **REL g_bar > 1e-13** (isolation-clean, 7 pts/bin).

| bin  | z range     | z_eff  | N_lens | a0_fit (m/s²) | stat (dex) | syst band (m/s²)          | χ²/npt |
|------|-------------|--------|--------|---------------|------------|---------------------------|--------|
| low  | 0.10–0.308  | 0.2357 | 90,739 | 2.187e-10     | ±0.041     | 1.083e-10 … 3.475e-10     | 8.7/7  |
| high | 0.308–0.50  | 0.3723 | 90,738 | 2.864e-10     | ±0.044     | 1.433e-10 … 4.540e-10     | 11.5/7 |

Extended cut (g>1e-14, 11 pts): 2.216e-10 → 3.652e-10, but the high bin's χ²=23.1/11 flags mild
model-misfit and the deepest bins carry the isolation/extrapolation systematic — so the REL cut is
load-bearing.

**a0 RATIO / slope (patch-consistent jackknife, REL cut):**
- ratio a0(high)/a0(low) = **1.309 ± 0.210** (stat)
- d ln a0 / dz = **+1.972 ± 1.159** per unit z (stat)  — Δ⟨z⟩ = 0.1367

### 3-bin case: BLOCKER (not fabricated)
The committed accumulator `agentZ_stack.npz` is **2-way in lens-z** (CZ ∈ {0,1}, split at global median
0.307855). A clean 3-bin a0(z) requires the 16 GB KiDS source re-stack (`agentZ_second_variable.py
--stage stack` with a 3-way iz digitize at z-edges [0.2, 0.35]) — the hours-long path, not run. The
3-bin result is reported **UNAVAILABLE**; no 3-bin a0 is fabricated.

---

## 2. Systematic error correction (adversarial-verifier reconciliation)

Three independent verifiers (systematics, statistics, fidelity) reproduced every number and flagged one
**real over-claim on error precision** (no verdict flips). Reconciled and corrected here:

**The slope error was reported stat-only.** The confront script asserted the ~0.25-dex CGM/M-L
systematic is "largely z-common so it cancels in the ratio." **That is false: the two z-bins are not
mass-matched.** The r<20 magnitude limit selects more massive galaxies at higher z:

- **Δ logM = 0.465 dex** (mean logM 10.214 low → 10.679 high) — *verified directly from the lens
  catalog `lr_lenses.npz`.*

A mass(=z)-correlated baryon term (CGM cold-gas fraction f_cold≈0.55 low vs 0.21 high →
differential 0.108 dex in log10(1+f_cold)) scales the two bins' g_bar differently and does **NOT**
cancel in the ratio. At a 50% CGM-model amplitude uncertainty this adds **0.906/z in quadrature**:

| quantity                 | stat-only | **stat + differential-CGM syst (corrected)** |
|--------------------------|-----------|----------------------------------------------|
| slope error d ln a0/dz   | 1.159/z   | **1.471/z**                                  |
| ratio error              | ~16%      | ~20%                                         |

(A more conservative *generic* independent-fraction f≈0.2–0.3 of the full 0.25-dex band brackets
1.7–2.1/z; the physically-modeled CGM-differential 1.47/z is adopted as load-bearing.)

The correction is **one-sided** — widening the error only shrinks every branch's significance. Since
all branches were already <2σ, **nothing that was consistent becomes excluded and no detection is
created.** The result is *more* null than the stat-only version, not less.

Photo-z: lens z is `zphot_ANNz2` (photometric); for KiDS-bright σ_z≈0.018–0.02 the regression dilution
of the true z-separation is ~5–6%, sub-dominant to the ~59–74% slope error and non-flipping.

---

## 3. Confrontation — per-branch verdict (AFTER corrections)

Load-bearing test is the **footing- and baryon-shift-invariant slope** (test III). Measured
**+1.972 ± 1.471/z (corrected)** vs each committed branch:

| Branch                              | pred slope /z | pred ratio | stat-only σ | **corrected σ** | verdict          |
|-------------------------------------|---------------|------------|-------------|-----------------|------------------|
| **A** canonical √ρ_DE (+6% bump)    | +0.056        | 1.008      | 1.65        | **1.30**        | consistent / **UNDETERMINED** |
| **C** constant w=−1                 | +0.000        | 1.000      | 1.70        | **1.34**        | consistent / **UNDETERMINED** |
| **B** rising √ρ_total = E(z)        | +0.580        | 1.083      | 1.20        | **0.95**        | consistent (not excluded) |
| **Verlinde** a0∝cH∝E(z) (=B shape)  | +0.580        | 1.083      | 1.20        | **0.95**        | consistent (not excluded) |

- **Branch A vs C is UNDETERMINED — NOT a win.** Their predicted slopes differ by only ~0.06/z, far
  below the 1.47/z measured error. The framework's own +6% non-monotonic bump (Branch A) is **below
  precision**; we can neither confirm nor refute A vs C. Stated plainly, as forecast.
- **The steeply-rising B/Verlinde branch is the real result** and it is **NOT excluded** (0.95σ) —
  in fact the *data slope is steeper than every branch*, so B/Verlinde sits *closer* to the data
  (0.95σ) than flat/declining A/C (1.30–1.34σ). Contrary to the pre-registered forecast that the +8%
  B/Verlinde rise over this z-pair would be resolvable at 1–3σ, **this specific 2-bin pair
  (Δ⟨z⟩=0.137, ratio error ~20%) does not resolve it.** No branch is killed.
- **Nothing is excluded at ≥2σ.** All four branches are "consistent."

### Absolute-level test (I) — syst-dominated, NON-diagnostic at both footings
| footing            | Branch A | Branch B/Verlinde | Branch C |
|--------------------|----------|-------------------|----------|
| canonical 9.36e-11 | χ²=5.15 (1.77σ) | 4.00 (1.49σ) | 5.78 (1.91σ) |
| alt 1.13e-10       | χ²=3.31 (1.44σ) | 2.40 (1.03σ) | 3.81 (1.44σ) |

All consistent (<2σ) at both footings; **neither footing is confirmed nor refuted.** The measured
~2–3e-10 per bin must **NOT** be read as "a0 is ~2.4× canonical" — the deep-MOND degeneracy
a0_hat(δ)=a0_hat(0)·10^−δ means the M/L + one-sided CGM window swamps the absolute level.

**Correction (fidelity verifier):** Do **not** state "a +0.35 dex shift lands 9.36e-11 exactly." The
fitter's actual one-sided syst band floors at **1.083e-10 (low) / 1.433e-10 (high) — both ABOVE
canonical.** Reaching 9.36e-11 needs a +0.37 dex shift, +0.07 dex *beyond* the +0.30 dex CGM prior
the fitter explored. Honest statement: **canonical is at the edge of / just outside the coded
systematic prior, not comfortably inside it.** The absolute test is not load-bearing (syst-dominated);
the footing-invariant slope carries the verdict and is independent of this.

---

## 4. MUSE-DARK III (Ciocan+2026) cross-check

MUSE-DARK III measures a0 **RISING** (~2.4e-10 at z~1, +1.59/z), contradicting the framework's
*canonical DECLINE*. This lensing a0(z) is an **independent second opinion** on that exact tension:

- **Sign agrees:** the lensing slope (+1.97/z) and MUSE (+1.59/z) are both **positive/rising**, and
  fully compatible within the 1.47/z lensing error.
- **But statistically inconclusive:** the lensing rise is significant at only ~1.3σ (corrected), not a
  detection. Like MUSE it is **ΛCDM-degenerate** (deep-MOND a0–baryon degeneracy + one-sided CGM).
- **Net:** lensing **corroborates the SIGN** of MUSE's rise **without confirming it**, and does **NOT**
  falsify the framework's canonical flat/mild-decline claim (Branch A/C stays consistent at 1.30σ).
  The rising-a0 tension flagged by MUSE is **echoed but not resolved.**

---

## 5. Honest caveats (verifier-surfaced)

1. **Systematics degeneracy (dominant).** Absolute a0 is degenerate with the coherent baryon/M-L scale
   (deep-MOND). Only the ratio/slope is diagnostic, and even that carries a *differential* (non-cancelling)
   CGM term because the bins are not mass-matched (Δ logM=0.47 dex) — corrected into the 1.47/z error above.
2. **Photo-z smearing.** ANNz2 photometric lens z dilutes the true z-separation by ~5–6% (sub-dominant).
3. **N-per-bin / Δ⟨z⟩.** Only 2 bins, Δ⟨z⟩=0.137, ~90.7k lenses each, 7 RAR points/bin. The z-lever is
   too short to separate branches; more z-bins / combined surveys (DES, LSST, Euclid ×spec-z) are needed.
4. **3-bin blocker.** Genuinely unavailable without the 16 GB re-stack; reported as blocker, not faked.

---

## 6. Reproduce (every number is script-backed, exit 0)

```
cd /Users/carlzimmerman/new_physics/zimmerman-formula
python3 real_research/reviews/lensing_rar/lr_a0z_zbin_measure.py     # measurement (exit 0)
python3 real_research/reviews/lensing_rar/lr_a0z_zbin_confront.py    # confrontation (exit 0)
```

- **Measurement:** `real_research/reviews/lensing_rar/lr_a0z_zbin_measure.py`
  (reuses `real_research/reviews/confront_lensing_rar.py::fit_a0`, framework nu `gobs_fw`; accumulator
  `data/lensing_rar/agentZ_stack.npz`, keys wgE/W; light path validated vs Brouwer+2021).
- **Confrontation:** `real_research/reviews/lensing_rar/lr_a0z_zbin_confront.py`
  (branch shapes from `real_research/a0z_clean_ledger.py`: m_framework=A, m_rising_cH=B/Verlinde,
  m_constant=C; both footings).
- **Corrected slope error (1.47/z):** differential-CGM inflation from Δ logM=0.465 dex (verified from
  `data/lensing_rar/lr_lenses.npz`), f_cold 0.55→0.21, 50% amplitude uncertainty → +0.906/z in
  quadrature with the 1.159/z jackknife stat.

**Committed 2026-07-06** (local only, no push) — a verified null belongs in the self-verifying repo.

---

## 7. Verdict

**Publishable only as an independent NULL / second-opinion note — not a detection.** The 2-bin KiDS
lensing a0(z) neither confirms nor excludes any branch: the framework's canonical declining/flat
a0(z) (A/C) is **alive and undetermined**, the disfavored rising rival (B/Verlinde) is **alive and
un-excluded**, and the sole directional signal is a **1.3σ non-significant rising hint** whose *sign*
matches MUSE-DARK III. **No deficit manufactured against the framework; no win manufactured for it.**
Both footings carried; neither confirmed nor refuted.

**Single biggest caveat:** the load-bearing slope error is now systematics-limited, not
statistics-limited — the differential CGM/M-L baryon term (from the unavoidable 0.47-dex mass mismatch
between z-bins) inflates it to ≥1.47/z, which is what kills all discriminating power. Closing the gap
requires mass-matched z-bins (or a joint baryon-marginalized fit) and a longer z-lever, not just more
lenses.
