# Route 2 — The CMB Third Peak Through AeST: Does Skordis Fit It, At What Cost To The Unification?

**Opus 4.8 (1M), 2026-06-15.** *Both-ways review. Credit the Skordis machinery; quantify the unification cost;
assess "fishy" rigorously. Coefficient quarantine held (a0/Z never asserted derived).*

> **One-line verdict:** AeST **does** fit the full Planck CMB angular power spectrum including the third
> acoustic peak (a genuine, first-of-its-kind achievement for relativistic MOND) — but it does so with a
> **free dust-amplitude integration constant I₀** that is **provably independent of a₀=c²√(Λ/32π)**. So the
> CMB is **NOT a falsification of a₀=√Λ and NOT a data artifact** — it is an honest **unification-economy
> cost**: "two dark sectors, one number" holds for {a₀ ↔ Λ = dark *energy*} but **fails at recombination**,
> where the dark-*matter*-like clustering the third peak requires is a separate, hand-tuned number.

---

## (i) DOES AeST REPRODUCE THE FULL CMB + THIRD PEAK? — YES (verified, primary source)

**The 2021 PRL headline is real.** Skordis & Zlosnik 2021 (*New Relativistic Theory for MOND*, PRL 127 161302,
arXiv:2007.00082) abstract, verbatim: *"demonstrate its agreement with the observed cosmic microwave background
and matter power spectra on linear cosmological scales."* Their Fig. compares ΛCDM and AeST TT/EE C_ℓ and P(k)
with residuals; the AeST curve tracks Planck through all the acoustic peaks, third peak included.

**The mechanism (verified in the paper itself):** AeST's shift-symmetric scalar φ behaves as **shift-symmetric
k-essence**. With the FLRW reduced action `S = (1/8πG̃)∫d⁴x Na³[−3H²/N² + K(Q̄)] + Sₘ` (their Eq. 3) and
`K = −2Λ + K₂(Q̄−Q₀)² + …` (their Eq. 4), the φ̄ equation integrates once to:

> **dK/dQ = I₀/a³**  (their Eq.)  ⟹  **Q = Q₀ + I₀/a³ + …**  ⟹  **ρ̄ = ρ̄₀/a³ + …**

i.e. the scalar's cosmological energy density **redshifts as a⁻³ — pressureless dust** — exactly the
non-baryonic clustering component the acoustic peaks need. This dust outweighs baryons, provides the
gravitational driving that keeps odd/even peak heights balanced, and at recombination supplies an **effective
DM density that AeST sets equal to the ΛCDM value** (the paper's own comparison uses **Ω_ch² = 0.1202**). The
shift symmetry (the action is invariant under φ→φ+const) is what protects the a⁻³ scaling — it is the low-energy
limit of ghost condensation (their refs [52–54], [87]).

**Cross-confirmed in the follow-ups:**
- Durakovic & Skordis 2023 (arXiv:2312.00889), verbatim: *"AeST providing cosmological energy density scaling
  as (1+z)³ plus corrections … approximately that of dust … the cosmological dust density **Ω_AeST is set by
  the initial displacement of Q from Q₀**"* via `Q = Q₀ + I₀(1+z)³`.
- Reza/dynamical-systems papers (arXiv:2309.06232, 2308.00342): the scalar "evolves as in shift-symmetric
  k-essence … energy density similar to dust ∝(1+z)³ plus small decaying corrections"; "the first extension of
  GR that successfully fits the CMB angular and matter power spectra without a (particle) dark matter
  component."

**This is a big deal and must be credited.** Pre-2021, the standard MOND objection ("relativistic MOND can't
make the third peak") was a genuine kill. AeST retired it. The CMB does **not** falsify AeST.

## THE THIRD-PEAK NUMBER, RECOMPUTED ON REAL DATA (the obstruction it solves)

`real_research/reviews/cmb_third_peak_dm_mimic.py` (real CAMB 1.6.6, rerun this session) confirms WHY AeST needs
the dust — a **pure-baryon / pure-modified-inertia universe cannot make the third peak**:

| universe | P3/P2 | z_eq | reading |
|---|---|---|---|
| ΛCDM (Planck 2018) | **0.98** | 3407 | third peak nearly as high as second (observed) |
| pure-baryon (Ω_ch²→0) | **0.53** | 535 | radiation-dominated recomb → potentials decay → 3rd peak crushed |
| all-baryon (CDM→baryons) | **0.42** | 3408 | baryon loading 6× BBN → 3rd peak even lower |
| best baryon-only rescue (free h,nₛ,Ω_bh²) | **0.54** | — | cannot reach 0.98 by ANY tuning |

So the third-peak height is a **branch-independent** obstruction for any baryon-only force law: you need a
clustering field. **AeST's a⁻³ scalar IS that field** — that is exactly the success.

## (ii) THE COST — IS THE DUST DENSITY GIVEN BY a₀=Λ, OR AN INDEPENDENT THIRD NUMBER? → INDEPENDENT

**This is the load-bearing finding, and it is settled by the primary source, not inferred.**

The dust amplitude is `8πG̃ ρ̄₀ = Q₀ I₀` (Skordis-Zlosnik 2021, their Eq.). And **I₀ is a free initial
condition.** Their own words, verbatim:

> **"As the solution depends on the initial condition I₀, the density ρ̄ is not (classically) predicted."**

And the cosmological-constant piece too:

> **"The CC in this model remains a freely specifiable parameter, just as in the Λ-cold dark matter (ΛCDM)
> model."**

**The free-parameter ledger (verbatim, their text):** *"Cosmologically, the necessary additional free
parameters to ΛCDM are **λ_s, K_B, K₂ (or equivalently w₀) and Q₀**"* — plus the dust amplitude I₀. The MOND
scale a₀ enters **a different feature**: the small-acceleration limit of the free function, J(Y) ≈ a₀²·(…) (their
Eq. A.6, `J = −a₀²ln(1−√Y/a₀)` form). So:

- **a₀ ↔ Λ = dark ENERGY** is real unification — Λ appears in K as the `−2Λ` term and fixes the late-time
  acceleration; a₀=c²√(Λ/32π) ties the MOND scale to that same Λ. ✔ "Two faces of one geometry" — for the
  *dark-energy* face.
- **a₀ → the early DUST = dark MATTER mimic is NOT unification.** The dust is set by I₀ (initial condition) and
  Q₀ (a free K-expansion constant). Neither is a function of a₀ or Λ. The shift symmetry that makes the dust
  *exist* is structural, but its *amplitude* (≈Ω_dm) is hand-put.

**Quantified (this session's python):**
- a₀=c²√(Λ/32π)=9.36×10⁻¹¹ fixes ρ_DE(Λ) ⟹ **Ω_DE=0.685** (the unification a₀ DOES deliver).
- the CMB third peak needs ρ̄₀ ⟹ **Ω_dm≈0.265**, via the *independent* Q₀I₀.
- ρ_dm0/ρ_DE ≈ **0.39** — an O(1) "why-now" ratio that a₀=√Λ does **not** predict.

> **The headline "two dark sectors, one number" provably does NOT hold at the CMB.** At z=0 the unification is
> {a₀, dark energy} — two faces of Λ. At recombination the third peak demands a THIRD number, Ω_dm≈0.26 via I₀,
> that a₀=c²√(Λ/32π) does not give. AeST *fits* Planck; the *unification* is incomplete at recombination.

**Both-ways guard (do NOT over-claim the loss either):** this is **not** "the CMB kills a₀=√Λ." a₀ is **provably
absent from linear perturbation theory** — a force/inertia modification adds exactly 0 to the linear transfer
functions (confirmed by the banked CLASS Euler-hook run: the modified-inertia injection gives Δχ²≈0 for
flat/declining at the physically-correct bath acceleration; only *rising* a₀(z) dies). So the I₀ that the third
peak needs is an **integration constant orthogonal to a₀**, not a contradiction of it. Inflating this to "Planck
falsifies a₀=Λ" would be a manufactured loss in the other direction.

## (iii) IS THE CMB "FISHY"? — NO. (assessed rigorously, not dismissed)

Carl's "the data is fishy because everything else checks out" does **not** apply here, and the honest reason is
not high-priest hand-waving — it is the data quality:

- **Cosmic-variance-limited, not noise/foreground-limited.** Planck 2018 (overview paper, verbatim): *"the
  uncertainties of the TT spectrum are dominated by sampling variance, rather than by noise or foreground
  residuals, at all scales below about ℓ=1800."* The third peak (ℓ≈800) sits deep in the CV-limited band — you
  cannot make it go away with a better instrument or a foreground re-analysis.
- **18 detected peaks, 35 extrema, 106 high-S/N multipoles**, six-parameter ΛCDM fit good to **<1% on five of
  six parameters**. The third-peak height is not a marginal feature; it is one of the best-measured numbers in
  cosmology.
- **Independently confirmed** by WMAP (lower ℓ), ACT DR4/DR6 and SPT-3G (higher ℓ, different sky, different
  systematics) — the peak structure is not a Planck pipeline artifact.

**Verdict on fishy, both ways:** The CMB is the **opposite** of fishy — it is the most-scrutinized, most-robust
dataset in the field. *But* the "something is off" instinct is not crazy in general — it just lands on the
**wrong target here**. Where it has PARTIAL merit is the **clusters** loss (the WL-vs-hydrostatic ~110% mass
discrepancy is a real systematic that softens that loss); at the CMB there is no such softening to find. The
honest answer is: AeST **fits** Planck, so the real cost is the **unification economy** (the extra I₀/Q₀
parameters), not a data error and not a falsification of a₀=√Λ.

## CONCEDE / CREDIT LEDGER

| claim | grade |
|---|---|
| AeST reproduces full Planck CMB incl. 3rd peak + P(k) | **TRUE — credit it (genuine first for relativistic MOND)** |
| The 3rd peak needs a clustering field; baryon-only fails | TRUE (P3/P2: 0.42–0.54 vs Planck 0.98, real CAMB) |
| AeST's a⁻³ shift-symmetric scalar IS that clustering field | TRUE (Skordis-Zlosnik 2021, mechanism verified) |
| The dust amplitude (≈Ω_dm) is set by a₀=c²√(Λ/32π) | **FALSE — it is I₀, a free initial condition; "ρ̄ not (classically) predicted"** |
| "Two dark sectors, one number" holds at the CMB | **FALSE — needs a 3rd number (Ω_dm via I₀); unification fails at recombination** |
| The CMB falsifies a₀=√Λ | FALSE (a₀ absent from linear theory; both-ways guard) |
| Planck's 3rd peak is fishy / a data artifact | **FALSE — CV-limited, 18 peaks, multi-experiment confirmed** |

**Net standing of the loss:** UNCURED as a *unification* claim (the most honest framing), but **AeST FITS the
data** so it is a falsification of neither AeST nor a₀=√Λ. It is a unification-economy cost, paid in the
extra parameters {λ_s, K_B, K₂/w₀, Q₀, I₀} — most pointedly the dust amplitude I₀≈Ω_dm that a₀=Λ does not
predict. Concede it loudly; the honesty is what makes the a₀↔Λ (dark-energy) unification credible.
