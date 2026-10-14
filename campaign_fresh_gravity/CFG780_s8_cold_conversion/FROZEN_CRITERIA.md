# CFG780 FROZEN CRITERIA: does converting cold energy into dark energy lower late growth, and what does raw KiDS say?

Committed alone, before any script or number. 2026-10-14. Block CFG780–789 (reserved in LEDGER in this commit).

## Question
CFG779 (FRBs) allows black-hole dark energy only if the converted mass is cold energy, not baryons. Astra's conserved MD14
history (cold-only partition) converts 10.6% of Ω_c by z = 0 (cold survival 0.894; Ξ fixed by H0, not by lensing).
- Less clustering matter at late times means less linear growth.
- How much does that lower P(k) at the KiDS redshifts, and does it improve or worsen the framework's raw KiDS fit?

## Declared calculation
- **G1, linear growth.** δ″ + (2 + dln H/dln a) δ′ − (3/2) Ω_cl(a) δ = 0 (primes = d/dln a). Ω_cl = clustering matter
  (baryons + surviving cold).
  - Conversion branch C: cold comoving density C(a) = C_i − D(a) with D from MD14 ψ (z_start 8). The amount is set so that
    C(1)/C_i = 0.894 (astra's cold-only number). Baryons are conserved. Vacuum V(a) = ρ_DE0 · F(a), with F the CFG775
    (1 + z)³-weighted production history, and V0 set by flatness today.
  - Reference R: no conversion, same baryons, C = C_i, constant Λ with the same H0 (flat).
  - Both start at z = 8 with identical δ (δ ∝ a in matter domination).
  - Output: g(z) = D_C(z)/D_R(z) at z = 0, 0.5, 1 (the scorer's nodes) and its effect on P: g².
  - Linear growth is applied to the framework's nonlinear P_grav as a multiplicative g(z)² (disclosed approximation;
    conversion inside halos is not modelled).
- **G2, raw KiDS-1000 rescore.** CFG650's own scorer (`cfg650_native.py`, the CFG592 machinery, unchanged) is run with the
  framework run's P_grav at each node multiplied by g(z)². The S0 control is unchanged.
  - Jobs: T12 (on disk) and T1x (when finished).
  - Report: absolute χ² and p (scaled vs unscaled), and Δχ² vs S0.
- **Brackets (reported):** half the amount (cold survival 0.947), and the proportional partition η = 5.364 (cold survival
  0.911; baryons 0.911, which CFG779 puts in tension).

## Classes (primary: T12 canonical, KiDS, IA on)
- IMPROVES if χ²_abs(scaled) − χ²_abs(unscaled) ≤ −4.
- WORSENS if ≥ +4.
- NEUTRAL otherwise.

## Controls
- K1: with zero conversion, g ≡ 1 to 1e-8 and the rescore reproduces CFG650's stored T12 χ² to 1e-6.
- K2: the reference growth D_R matches the scorer's own Dgrow(a) shape to 1% at z ≤ 1.

## MUTATE (CFG780_MUTATE=1)
Conversion ×3 (cold survival 0.68). The absolute χ² must move further than in the primary run, in the same direction.

## Hand estimate
- Removing ~10% of Ω_c over z ≈ 3 → 0 lowers D(0) by ~3–5%, so P by ~6–10%.
- T12's absolute χ² of 146 (p = 0.011) may fall, but the sign is uncertain because the S0-matched comparison also moves.

## Machine
Run ONLY after the relaunched T1x (14:32) finishes and is scored. 1 process, < 1.5 GB.

κ fitted; cold energy mass required; not theory closed. The conversion mechanism is not derived (CFG775/779).
