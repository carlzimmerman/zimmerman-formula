# CFG349: a causal memory switch on the khronon clock (a ratchet along the baryon flow)

Criteria: `FROZEN_CRITERIA.md` (commit b6ae8e697, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; the switch reads baryons only (MS1-MS5); no DM particle (the cold mass is still required).

**Verdict (frozen rule): PARTIAL, LEGALITY FAIL.** (a) and (c) pass and (b) fails, with 0 new constants. Where the
ratchet has had time to act it is exactly what CFG347/348 lacked: OFF on FRW and in every linear parcel, it never
flickers, and it is strongly hyperbolic. It fails (b) as frozen on young, low-mass hosts, and no action for it is fully
legal. This is a scoped result, not a closure.

## The construction
- Ratchet: u_b.dm = (u_b.dT) Gamma_b H(-theta_b) (1 - m), where Gamma_b = sqrt(4 pi G rho_b) and H(0) = 1. It has no
  decay term. The MOND sector is multiplied by f(m) = m.
- It is first order along u_b and timed by the leaves, and it reads only the baryons (theta_b, rho_b).
- New constants: 0.
- Actions:
  - L-ord: S ⊃ Int sqrt(-g) { f(m) L_MOND + lambda [u_b.dm - (u_b.dT) Gamma_b H(-theta_b)(1 - m)] }.
  - L-CTP: the doubled-field action of CFG242 route A. Its physical limit is the ratchet with no lambda back-reaction.

## Legality (the named liability)
- **L1 EOM.** Both actions give a derivable EOM (sympy, parcel reduction).
- **L2 diff-safety.** Every term is a scalar on the leaves, so it is diff-safe (CFG329's method).
- **L3 energy.** Neither action is legal, for different reasons.
  - **L-ord:**
    - The energy is linear in lambda, so it is unbounded.
    - lambda obeys d/dt[lambda (1 - m)] = f'(m) L_M (1 - m). Unsourced, lambda = C/(1 - m), which diverges as the switch
      saturates. This is Liouville's theorem: an irreversible attractor needs an exponentially growing conjugate.
    - The parcel inertia picks up lambda Gamma (1 - m) S''/(w V)^2. Its sign is indefinite, and for the sharp H it is a
      delta function at theta_b = 0, which is exactly the static state.
  - **L-CTP:**
    - It is causal and ghost-free.
    - It does not conserve momentum: the static stress divergence has a residual F f'(x) wherever m varies.
    - Size relative to rho_b g at 30 kpc: 4e-7 to 0.80 today; 0.09 to 3.1 while the switch turns on.
  - This is CFG48's verdict again: stable, but not a legal local term.

## Results (24 DE12 hosts, both footings, r = 30 kpc)
- **(a) PASS.**
  - m = 0 exactly on FRW parcels with theta = 3H(1 + d), d >= -0.99 (a finite OFF neighbourhood; Lean R3).
  - Linear parcels with delta <= 0.1 have theta_b/3H >= 0.967.
  - Turnaround needs delta_lin = 1.062 for a sphere (sympy, theta = 0 at eta = pi) and 0.75-0.85 for a Zel'dovich sheet.
  - L341 gives D/D_LCDM = 1.00000000 and sigma_8 = 0.8101.
- **(b) FAIL.**
  - **B1 ON:** 18/24 hosts have m >= 0.9 under the frozen conservative exponent. m_cons ranges 0.475-0.999999. The
    lenient bracket (no duty factor, turnaround density) gives 0.9935-1.0, so the frozen failure is NOT ESTABLISHED as
    physical.
  - The failing hosts are z = 2.5 and 4 at M_b 1e10-1e11, plus 1e11 at z = 4. Their 30-kpc gas turned around too
    recently for e-folds of Gamma_b.
  - **B2 fidelity:** the worst case delta f = 1 - m gives a change of 2.5e-6 to 0.70; 16/24 hosts pass. The failures are
    the deficit 1 - m, not flicker.
  - **B3 no flicker:** across 10 compression cycles the maximum drop on the hosts is exactly 0. The frozen 1e-12 line
    FAILS on the probe shell at 2.9e-11, which is LSODA noise near m = 1. A labelled post-hoc exact-step update gives a
    drop of 0 (Lean R1).
  - On the probe shell, m(t_ff) = 0.89 and m reaches 0.99 at 3.0 t_ff.
  - Sensitivity (not scored): Gamma = H gives 0/24 ON (m 0.19-0.34), and Gamma = a0/c gives 0/24 ON (m 0.005-0.06).
    The framework's global rates are too slow; only the parcel's own rate works.
- **(c) PASS.**
  - The baryon inertia is rho (no ghost).
  - The principal symbol has speeds {0 (m, along u_b), 0, 0, +-c_s}, and 5/5 eigenvectors, so it is strongly
    hyperbolic. CFG242's BIMOND failure was weak hyperbolicity.
  - The H(-theta) source is bounded and so not principal.
  - The dust limit's Jordan block belongs to dust alone (1/2 eigenvectors); the ratchet adds none.
  - Hadamard: the maximum growth rate is at most 0.79 (Gamma_J + Gamma_b) for k in [1e-3, 1e3]/kpc.
- **Edge sharpness.** The edge sits at the turnaround shell, not inside discs.
  - On top-hat infall, m reaches 0.1 / 0.5 / 0.9 at R/R_ta = 0.99 / 0.62 / 0.03, and at t/t_ff = 0.14 / 0.73 / 1.0.
  - First infall to R_ta/2 gives m = 0.58.
  - The radial width (m from 0.5 to 0.9) is 104-1953 kpc, against r_ta of 177-3312 kpc.

## Ownership (reported)
- **Class A** (accreted top-level systems) keeps its own ON state, because the ratchet never decreases.
- **Class E** (formed embedded) inherits the host gas's m, so it is ON, not Newtonian. A parcel carries one history
  number, and both classes share it. So FG001's class E is NOT reproduced: this is CFG251's "inherit" reading (iii-a).
- Field baryons that never turned around keep m = 0. Ejected gas keeps its m.

## Controls
- **K1:** CFG242's latch E3 reproduces n(t_ff) = 0.7910 and min 0.1429 (recorded: 0.791 / 0.143). Its static decay
  time is sqrt(4 pi/3) = 2.047.
- **K2:** Gamma = 0 gives m = 0 for all time, which is Newtonian.
- **MUTATE (reversible memory):** it flickers. On the hosts the late mean m is 0.50 and the peak-to-peak swing is 0.81
  (the duty fixed point, Lean R8). B3 fails and the run exits 1.

## Lean
`CFG349_memory_certificates.lean` has 10 theorems, no sorry and standard axioms only (rc 0; output in `.out`):
- R1 ratchet monotone; R2 [0,1] invariance; R3 FRW-off invariance;
- R4 / R4b distinct characteristic roots and the acoustic factorisation; R5 kinetic positivity;
- R6 / R6b the L-ord partner identity and lambda's divergence;
- R7 fidelity bound; R8 reversible fixed point = duty.

## Run
```
python3 campaign_fresh_gravity/CFG349_khronon_memory_switch/cfg349_memory_switch.py > campaign_fresh_gravity/CFG349_khronon_memory_switch/cfg349_memory_switch.out              # rc 0, ~4 s
CFG349_MUTATE=1 python3 campaign_fresh_gravity/CFG349_khronon_memory_switch/cfg349_memory_switch.py > campaign_fresh_gravity/CFG349_khronon_memory_switch/cfg349_memory_switch_MUTATE.out   # rc 1
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG349_khronon_memory_switch/CFG349_memory_certificates.lean
```

**Scope:**
- quadratic and quasi-static analysis;
- the turnaround epoch comes from the spherical-collapse factors 44.4 / 5.55 (an approximation);
- DE12's gas traces the NFW host (no dissipation), which makes B1 conservative;
- the 1D Bianchi residual uses |L_M| ~ g_ph^2/(8 pi G);
- the L-ord inertia uses a smoothed H of width w (the sharp limit is the delta function).
