# CFG787 FROZEN CRITERIA: is surplus cold energy still expelled with angular momentum and gradual baryon loss?

Committed alone, before any script. 2026-10-14. Block CFG780–789.

## Question
CFG776 (radial shells, sudden loss) found surplus tethered cold energy expelled within 50–100 t0, overshooting into a
deficit. The conclusion "any core excess must be untethered" rests on that. Repeat it with two relaxations:
- **A, angular momentum.** Each shell gets specific angular momentum j_i = ε_i × r_i × V_c(r_i) at start, with V_c from
  baryons + start profile. ε_i is drawn uniform in [0, 1] (seed 787): an isotropic-like mix. Force: r̈ = −1/r² + m³-tether
  term (CFG747 exactly) + j²/r³.
- **B, gradual loss.** Baryon mass M_b(t) declines linearly from p to 1 over τ_loss ∈ {10, 50, 200} t0 instead of
  instantly.
- Grid: p ∈ {1.5, 3}. Combinations: (A only), (B only, each τ), (A + B, τ = 50).
- Snapshots of m(<r)/r at r = 2, 5, 8, 11, 25 r_M at t = 100, 200, 500, 1000, 2000.
- Integrator, N, DT, R0, core: as CFG776.

## Classes (per case, at t = 200 t0, r = 5–11 r_M)
- **EXPELLED** if the relic fraction is ≤ 0.2 at every r.
- **RETAINED** if ≥ 0.5 at r = 5 and 8.
- **PARTIAL** otherwise.
- **Lane verdict:** CFG776 ROBUST if every case is EXPELLED; QUALIFIED if any case is PARTIAL/RETAINED (name which).

## Controls
- K1: ε ≡ 0 with τ_loss = 0 reproduces CFG776's p = 1.5 / 3 tables to 0.01 at t = 100–2000.
- K2: energy is conserved (ΔE/E ≤ 1e-3) in the sudden case. Gradual cases do external work, so report the work instead.
- MUTATE (CFG787_MUTATE=1): no cubic push. The relic must be retained (as CFG776's MUTATE).

## Hand estimate
- Angular momentum adds a centrifugal barrier, so shells cannot fall in, but the cubic push still acts outward. Expect
  expulsion slower but still EXPELLED by 200 t0 at p = 3; p = 1.5 possibly PARTIAL.
- Gradual loss lets the profile track the law adiabatically, so less overshoot and EXPELLED.
- **Expected: ROBUST or QUALIFIED at p = 1.5 + angular momentum.**

## Machine
Run after T1x (~30–60 min, single thread). κ fitted; not theory closed.
