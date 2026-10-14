# CFG776 FROZEN CRITERIA: the frozen relic (H-FR). Systems that lost condensed baryons keep cold energy tethered at their peak

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

Owner: "we overlooked something that can explain it ... using our latest work".

Seen before freezing (disclosed):
- CFG747/748 tables. Excess cold energy is expelled; the inner halo returns to the law by t ≈ 2000 t0.
- CFG669: KiDS early-type excess +0.280 ± 0.083 (Ks).
- AUDIT_UFD: MW UFDs +0.325 dex in σ, 3.8σ.
- CFG721: free fraction 0 for galaxies.
- The hand reasoning in chat: UFD clocks are fast, so a relic is erased there; early-type clocks are slow, so it survives.

## Hypothesis H-FR
- Cold energy is tethered to condensed baryons (T12 rule). The record has no export channel (CFG760–762).
- When a system's condensed mass falls from a peak p·M_now to M_now (gas heated or expelled at quenching), the cold energy
  tethered at the peak is released. It is NOT removed: it then evolves under the framework's own collisionless dynamics
  (CFG747: critical tether cancels self-gravity, cubic push u²/a0, baryons now M_now).
- **What survives at time τ after the loss is the prediction.** No relaxation time is put in by hand.

## Calculation (declared)
- **D1, dynamics (units G = a0 = M_now = 1).** CFG747's integrator and settings: N = 4000 shells, DT = 0.005, core 0.5 inside
  r_min = 0.5, R0 = 50.
  - Start at rest with the law profile of the peak mass: m(r) = √p (r − 0.5) + 0.5 shape, scaled, out to R0.
  - Sudden loss (the conservative case).
  - Peak values p ∈ {1.5, 2, 3}.
  - Snapshots of m(<r)/r at r = 2, 5, 8, 11, 25 r_M at t = 50, 100, 150, 200, 300, 500, 1000, 2000, 3000.
  - Relic fraction f(r, t) = (m/r − 1)/(√p − 1).
- **D2, physical clocks.**
  - t0 = √(r_M/a0), r_M = √(G M_now/a0), both footings.
  - Early types: M_b = 10^10.5, 10^11, 10^11.5 M☉; loss lookback τ_q = 8, 10 Gyr (z_q ≈ 1, 1.7); n = τ_q/t0.
  - KiDS radii R = 50, 70.7, 100 kpc, expressed in units of r_M.
  - MW UFDs: M = 10³–10⁵ M☉, τ = 13 Gyr, r_h/r_M ≈ 10–30.
- **D3, peak ratio from measured gas fractions.**
  - p = (1 + μ_gas(z_q, M*))/(1 − 0.1): stellar mass loss after quenching ~10%.
  - μ_gas from the Tacconi et al. (2018) main-sequence scaling,
    log μ = 0.12 − 3.62 (log(1 + z) − 0.66)² − 0.35 (log M* − 10.7).
  - **The coefficients are quoted from memory and are UNVERIFIED (provisional).** p is also bracketed {1.5, 2, 3}.
- **D4, KiDS prediction.**
  - Excess Δ = mean over the three K radii of log10[M_relic(<R)/M_law(<R)], with M = M_b + m_cold. The enclosed-mass ratio
    is a proxy for the ESD ratio (disclosed approximation).
  - Late types are unchanged (p = 1).
  - Predicted early − late = −0.027 (the CFG658 law value) + Δ.

## Tests
- **T1 (early types, headline):** the predicted excess at the primary p (Tacconi, z_q = 1.5, M* = 10^10.8) and τ_q = 10 Gyr
  lies within 2σ of +0.280 ± 0.083, on at least one footing. PASS / FAIL.
- **T2 (UFD erasure, consistency):** at n = 13 Gyr / t0(UFD), with n capped at the simulated 3000 when larger (disclosed),
  the relic fraction at 25 r_M is ≤ 0.1. If so, H-FR cannot explain the UFDs and predicts their offset unchanged; that
  failure stands.
- **T3 (SPARC guard):** discs keep their gas (p = 1), so there is no change by construction. Reported, not tested.
- **K1:** the p = 1 run reproduces CFG747's law control (m/r within 1% at all radii and times).
- **K2:** energy conservation ΔE/E ≤ 1e-3 for every run.

## MUTATE (CFG776_MUTATE=1)
M1: no cubic push (CFG747's MUTATE force). The relic must then NOT be expelled: m/r stays far from the law and the
expulsion picture fails. This tests that erasure is the push's work.

## Hand estimate (before any script)
- Early-type t0 ≈ 48–85 Myr ⇒ n ≈ 120–210, before CFG747's relaxation (~1000–2000 t0). Most of the relic survives at
  5–11 r_M.
- p ≈ 1.8–2.1 ⇒ Δ ≈ +0.10–0.15 ⇒ predicted +0.07–0.12, against +0.28 ± 0.083 ⇒ **T1 borderline FAIL (Z ≈ 2–2.5)**.
- T2: UFD n ≫ 3000 ⇒ relic erased ⇒ UFDs unexplained.

## Disclosures fixed now
- Radial shells, sudden loss, deep-regime units (the inner baryon structure is a point mass).
- Projection is approximated by enclosed mass.
- Tacconi coefficients are from memory.
- κ fitted; cold energy mass required; not theory closed.
