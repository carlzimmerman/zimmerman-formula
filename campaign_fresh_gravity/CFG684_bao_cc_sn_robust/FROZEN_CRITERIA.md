# CFG684 — narrow the tracking band CMB-free: cosmic chronometers + alternative SN sets (FROZEN, before any number)

Block CFG680–689. Owner "both" (2026-10-12). CFG683: CMB-free, the rival a0 ∝ H(z) is pinned to ±1.5% but tracking a0 ∝ √ρ_DE is
Ω_m-degenerate (√X(2.33) 0–2.18). Goal: shrink that band with more raw, CMB-free expansion data, and check SN-set robustness.

## Data
- Cosmic chronometers (CC): Moresco et al. compilation of differential-age H(z) with the public systematic covariance
  (gitlab.com/mmoresco/CCcovariance; BC03 models as primary, M11 as alternative). Absolute H(z) in km/s/Mpc → H0 profiled freely
  (no H0 prior). If the full compilation table cannot be fetched from a primary source, the run uses only what the repository
  provides, says so, and the lane reports CC as NOT RUN.
- SN alternatives (shape only, M profiled): DES-SN5YR (des-science/DES-SN5YR, Hubble diagram + STAT+SYS cov) and Union3
  (binned μ + covariance, rubind/union3_release). Each REPLACES Pantheon+, never pooled with it (overlapping SNe).
- BAO, X(z) model, Ω_m grid, Hessian bands: CFG681/682/683 verbatim.

## Combinations (each reported)
BAO+PP (=CFG683 reference), BAO+CC, BAO+PP+CC, BAO+DES5+CC, BAO+U3+CC, BAO+DES5, BAO+U3.

## Outputs per combination
χ²(Ω_m) range on the grid (does CC break the dark degeneracy? Δχ²_max across 0.24–0.36), tracking √X(z*) band (CFG683 method),
rival E(z*) band, closest gap and e_3σ at z* = 1.0, 1.5, 2.33; Ω_m implied by flat a0 (CFG682 method, e = 0.02, z* 2.33).

## Decision rules
- DEGENERACY BROKEN by a combination if Δχ²_max over the grid ≥ 4 (Ω_m bounded at 2σ inside 0.24–0.36); else NOT BROKEN.
- ROBUST if the flat-a0 Ω_m from BAO+DES5(+CC) and BAO+U3(+CC) agree with BAO+PP(+CC) within 1σ (combined); else SN-SET-DEPENDENT.
- The best combination's e_3σ is the CMB-free target for CFG685.
- MUTATE: CC replaced by its own best-fit E(z) at the same errors → Δχ² against BAO+PP+CC must not exceed BAO+PP's own by > 1.
κ fitted; cold energy mass required; not theory closed.
