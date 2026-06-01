# What real science is recoverable from the slop — an optimistic, rigorous sweep

**2026-06-01.** Four independent agents deep-mined the quarantined `ai_slop/` corpus
under one instruction: *don't reflexively dismiss — find what's genuinely valid, what's
sound-but-never-tested, and what's a reusable method, and say so clearly.* They
converged. The answer is **yes, there is recoverable science** — one sound physics
prediction and two reusable methods — and it is honestly much smaller than the program
claimed, but real.

---

## 1. The one recoverable PHYSICS prediction: evolving a₀(z) = a₀(0)·E(z)

This is the single survivor, and all three physics/theory agents land on it independently.

- **It is Z-independent.** Z cancels in the redshift ratio, so it stands even though the
  factor-of-2 in Z is hand-inserted, α⁻¹=4Z²+3 is a 2-integer fit, and "Z²=32π/3 = the
  η-invariant of T³/Z₂" is *false* — the rigorous spectral η-invariant is **exactly 0**
  (verified over 4,006,002 modes); Z² is a *definition* (the Friedmann 8×4π/3), not a
  topological derivation.
- **It is not numerology.** It rests on standard deep-MOND ($\sigma^4 = G M_{\rm bar}\,a_0$,
  McGaugh) plus the exact Friedmann scaling $\rho_c \propto E(z)^2$. The only physics input
  beyond textbook is "$a_0$ tracks the cosmic density" — which is **Milgrom's own
  conjecture**, not original here.
- **It is sharply falsifiable and untested in its clean regime.** The test
  (`highz_btfr_prediction.py`): a deep-MOND galaxy at redshift $z$ sits above the local
  baryonic Tully–Fisher relation by $\Delta\log\sigma = \tfrac14\log_{10}E(z)$ if $a_0$
  evolves, or *on* it if $a_0$ is constant (the null). The split is a few % at $z<2$ but
  **>2× at $z>10$**, so the test is only decisive in the deep-MOND $z>10$ regime.

**Honest current status (no spin):**
- $z<1$ and $z\sim4$–6 BTFR show ~no zero-point evolution → *mildly disfavors* evolving
  $a_0$, **but** those samples are massive disks at $g>a_0$ (Newtonian regime), where
  $a_0(z)$ barely enters — not a clean test (the regime trap).
- $z\sim6$ JADES dispersions: evolving $a_0$ has a ~6.5σ mean offset (poor; mass-dominated).
- $z>10$: the "GN-z11 exact match (0.018σ)" was an **artifact** (the factor-2 mass band is
  wider than the measurement; GN-z11 is AGN-contaminated). Genuinely **ambiguous /
  data-limited** — the open regime.

**Verdict:** a sound, Z-free, pre-registered, near-term-killable prediction — defend it as
that, not as a discovery. JWST-NIRSpec-IFU / ALMA [OIII]88µm dispersions of GLASS-z12 and
JADES-GS-z14-0 will settle it. (`highz_btfr_prediction.py`, `a0_evolution_pipeline.py`.)

## 2. Two recoverable METHODS (real, reusable — independent of Z²)

- **A blinded persistent-homology pipeline + an H1 death-radius dataset of real PDB
  proteins.** `…/validated_pipeline/03_strict_persistent_homology.py` runs `ripser` on
  real Cα coordinates, forbids fallbacks, and was deliberately run *blind* to Z²:
  3,385 H1 features (median 5.50 Å) scaling to 24,830 features over 25 sources (mean
  6.04 Å, 95% CI [6.02, 6.05]). It is a correct, reproducible structural measurement that
  a topologist could reuse as-is — and it **refutes** the Z² interpretation (the predicted
  9.14 Å / 5.79 Å are excluded; a random 2.78 Å constant fits better). Real method, real
  number, null result for Z².
- **The self-skepticism / honesty-classifier tooling.** The one asset the autonomous
  agents produced that works: a classifier that tagged 186 trivial + 262 phenomenological
  + 23 numerology + 31 suspicious out of 591 claims, and the von-Kármán-style "0.41 = 41/100,
  no physical connection — do not publish" rejection. Reusable for any constant-fitting
  program.

## 3. What is NOT recoverable (confirmed by all four agents AND the repo's own audits)

| claim | verdict |
|---|---|
| α⁻¹ = 4Z²+3, sin²θ_W=3/13, Ω_Λ=13/19, the ~53 "constants" | numerology — FDR: an arbitrary O(100) target is hit ≤0.004% **19.9%** of the time; several constants carry two incompatible formulas |
| 20.6 Gpc T³/Z₂ topology / η-invariant derivation | η-invariant is exactly 0; excluded by CMB matched circles; ghost "candidates" are SDSS aliasing artifacts (`reviews/ghost_quasar_sdss_live_check.py`) |
| r = 1/(2Z²) ≈ 0.0149 (tensor-to-scalar) | numerology — the Z₂-projection argument is wrong (both modes are Z₂-even); author's own file retracts it |
| cosmic birefringence β = 0 | rigorously derived but already at 4–6σ **tension** with data, and it's just the SM default |
| GW cross-polarization h_× = 0 | dead (same Z₂ error as r) |
| autonomous-agent "blind-test discoveries" | circular — answers fed in (`ground_truth_lookup.py.CONTAMINATED`); `empirical_value: 0, NO_DATA` |
| docking / therapeutic candidates | all `SIMULATED`/`MOCK` (Vina absent); no real hit |
| Z² protein "resonance", abiogenesis, Z² hurricane | refuted by the program's own real computations (PH 5.85 Å; eye/RMW falsified) |
| Riemann Hypothesis (H=xp) | dead — unequal deficiency indices, no boundary condition fixes it |

## 4. Bottom line

The optimistic search was warranted and the dismissiveness was not: **there is real,
recoverable science here — one sound, falsifiable, currently-untested prediction
(evolving $a_0$, in its clean $z>10$ regime) and two reusable methods (a blinded
persistent-homology pipeline + dataset, and the honesty classifier).** None of it
vindicates Z²=32π/3, the 137 retrodiction, the topology, or the cross-domain claims —
which the program's *own* audit files already retracted. The honest move forward is to
treat the evolving-$a_0$ prediction as a sharp pre-registered bet that JWST/ALMA can kill
or confirm within a couple of years, and to keep the two methods as tools.

*Scripts:* `highz_btfr_prediction.py`, `a0_evolution_pipeline.py`,
`schwarzschild_friedmann_core.py`, `coefficient_from_horizon_entropy.py`,
`reviews/ghost_quasar_sdss_live_check.py`. *Full audit:* `reviews/DATA_AUDIT.md`.
*Novelty calibration:* `NOVELTY.md`.
