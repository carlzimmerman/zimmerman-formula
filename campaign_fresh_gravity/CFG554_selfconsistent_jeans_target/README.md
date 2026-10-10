# CFG554: the self-consistent Jeans target of the velocity part, from a principle (no knobs)

**Result: the self-consistent target is NOT derived.**
- The principled route, maximum entropy at fixed density under the exact kinetic (tensor-Jeans) stationarity constraint,
  does produce a self-consistent target with no temperature inserted. It passes every MW check except overfill. It FAILS in
  the cluster cells.
- FIX-2's isotropic target follows from the same principle only if isotropy (equivalently, the scalar Euler-fluid
  hydrostatic constraint) is added, so it stays POSITED.
- FIX-2 itself is a valid metriplectic relaxation (M·δE = 0, dS ≥ 0 with the φ sink) and can be made to conserve angular
  momentum.

**Labels:**
- **As frozen: NO LABEL**, because control C6 fails (see the disclosures).
- **With C6 read at the grid's resolution:**
  - (a) INCONSISTENT;
  - (b) POSITED (metriplectic structure and angular momentum DERIVED, bench passes);
  - (c) INCONSISTENT.
- **Full-system Lyapunov: NOT ESTABLISHED** (every route).

κ = ½ is fitted. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The cold energy's mass is still required.
No dark-matter particle. This is not a closed theory.

Every number below is from `cfg554_results.json` or `cfg554_results_MUTATE.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (01ad75492).
- **Equations:** `VELOCITY_PART_v2.md`.
- **Script:** `cfg554.py`. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg554.py`, 4 processes, exit 0.
  `CFG554_MUTATE=1` exits 1, as designed: all teeth bite.
- **Bench:** CFG544's toy is imported unchanged. C5 reproduces CFG544's FIX-2 IC-C end states exactly (Δ = 0 in all 4 cells).
  C2 passes, and mass is exact in every run.

## The routes

**(a) Maximum entropy at fixed ρ_c, constrained by ∂_j Π_ij + ρ_c ∂_i Φ = 0 (Φ from real mass, G9).**
- sympy (S1a–e, all PASS):
  - the maximiser is a Gaussian with inverse covariance −2 sym ∇λ;
  - spherical: σ_r² = −1/(2λ′), σ_t² = −r/(2λ);
  - **it is isotropic iff the state is isothermal**;
  - SIS: σ² = V_f²/2 exactly;
  - the maximiser is unique;
  - the virial theorem makes an energy constraint redundant.
- The temperature profile is a Lagrange-multiplier field fixed by the Jeans constraint on the current density. It is solved
  every step by shooting, with no solver failure in any run.
- **MW (both footings): it works.**
  - G550 passes on IC-B and IC-C: |log X_J| ≤ 0.017, |D| ≤ 0.023.
  - Edge: +0.23 to +0.33, inside the allowances 0.355 / 0.433.
  - Energy is COMPATIBLE: IC-B net +0.220 / +0.245, IC-C whole-history +0.233 / +0.250 V_f² per M_cat.
  - Shell β −0.19 to −0.21; edge tangential (β −0.68 to −0.92).
- **Clusters (both footings): it fails.**
  - G550: log X_J = +0.119 / +0.119 (IC-B) and +0.103 / +0.104 (IC-C).
  - The halo spills: edge +1.80 / +1.92 (IC-B), r_99 = 6.0 / 6.8 r_*, 2–3% of the mass beyond r_ta.
  - Energy flows in: IC-B net −0.460 / −0.511, IC-C whole-history −0.073 / −0.090. NOT COMPATIBLE.
  - **Mechanism (verified from the final targets):** in the dilute outer tail, σ_t² = r/(2Λ) decays only logarithmically.
    Where it exceeds V_c²/2, the tensor-Jeans constraint keeps P falling more slowly than ρ, so σ_r² rises outward:
    2.7–7.1 V_f² at 2 r_*, against an isotropic Jeans value of 0.02–0.07. The relaxation heats the tail, particles leave,
    and the tail grows (r_99 rises steadily from 2.3 to 6.0 r_* in the second half of IC-B).
  - This is a property of the maximiser in a dilute, point-mass-dominated tail, not of the grid. The C6 grid error is ≤ 6%
    and cannot produce a factor of about 40.
  - At α = 2 the cluster cells pass G550 (log X_J +0.082 to +0.088).
- **Label: INCONSISTENT** (the derived target fails G550 in the clusters; energy too).

**(b) FIX-2 as metriplectic relaxation toward the instantaneous isotropic Jeans projection.**
- sympy S2 (all PASS):
  - with a state-dependent reference p*[ρ], M is symmetric PSD, M·δE = 0 with the partner, dS/dt is a sum of squares, and
    mass is exact;
  - the ρ-dependence of p* adds only a v-independent term (value T₀/Θ at equilibrium), so the equilibrium stays p_c = p*;
  - ∂KL/∂σ² = 0 at the match, so the position drift is unchanged on the velocity-equilibrium manifold.
- **Angular momentum (S3 + numeric): CONSERVED.**
  - Relax v_r about 0 (radial moves leave j unchanged) and v_t about the local mean, by momentum-conserving pairs with the
    partner. Then d⟨v_t⟩/dt = 0, and the stationary state is a Gaussian with free rotation.
  - Rotating-shell test: total J changes by 9.6e-16 (relative), against −98% under CFG544's operator.
  - The spherical bench has J ≡ 0, so it runs FIX-2 unchanged.
- **Bench: G550 passes in all 4 cells on IC-B and IC-C.**
  - Edge +0.22 to +0.45: PRESERVED.
  - Energy COMPATIBLE: IC-B net +0.249 / +0.273 / +0.283 / +0.305; IC-C whole-history +0.257 / +0.274 / +0.286 / +0.305.
- **Target:** the isotropic σ_J² is the maximiser only with an added isotropy constraint, or with the scalar
  (Euler-fluid) hydrostatic constraint in place of the exact Vlasov tensor moment (S1f).
- **Label: POSITED** (target), with structure and angular momentum derived.

**(c) Maximum entropy with the global (virial) constraint only, a single T_v.**
- G550 fails in cluster_can IC-C (steadiness, ΔD −0.054).
- Edge NOT PRESERVED: MW can IC-B +0.391 > 0.355; cluster can IC-B +0.549 > 0.545.
- It runs a large two-way throughput (drift −4.4 to −34 V_f² per M_cat, offset by relaxation), and its integrator error
  reaches 0.116.
- **Label: INCONSISTENT.** The local constraint is needed.

## Checks table (α = 1)

| | MW can | MW alt | cluster can | cluster alt |
|---|---|---|---|---|
| (a) G550 B / C | pass / pass | pass / pass | FAIL / FAIL | FAIL / FAIL |
| (a) edge B / C | +0.32 / +0.23 | +0.33 / +0.28 | **+1.80** / **+0.67** | **+1.92** / **+0.72** |
| (a) energy B net / C whole | +0.22 / +0.23 | +0.25 / +0.25 | **−0.46** / **−0.07** | **−0.51** / **−0.09** |
| (a) overfill P | 0.41 | 0.39 | 0.30 | 0.29 |
| (b) G550 B / C | pass / pass | pass / pass | pass / pass | pass / pass |
| (b) edge B / C | +0.22 / +0.22 | +0.24 / +0.26 | +0.43 / +0.38 | +0.45 / +0.41 |
| (b) overfill P | 0.43 | 0.43 | 0.34 | 0.30 |
| blow-ups (all routes) | none | none | none | none |

- **Overfill: NOT HANDLED in every route** (P = 0.29–0.45 > 0.2). It is a position-sector item, and the velocity target
  does not change it.
- **α robustness: FAILS for both (a) and (b).**
  - At α = 0.5 most runs are still evolving over the last 2 Gyr (|ΔD| 0.05–0.13): G550 fails in 6/8 run-cells for (a)
    and 7/8 for (b).
  - α = 2 passes everywhere for both.
  - New: FIX-2 is not α-robust either.
- **Lyapunov:** the largest rise of F along the runs is 0.011 F₀ (a), 0.009 (b) and 0.024 (c).
  - sympy: every candidate has a Vlasov rate first order in the bulk velocity, against O(α) dissipation. So dL/dt > 0 for
    some state when α < A/(2√(BC)): **NOT ESTABLISHED**.
  - S4: the route-(a) maximiser is not an exact Vlasov steady state (that needs ln f = −E/σ_r² − γL²).

## MUTATE (all bite, exit 1)

- **MT (route-a target ×2, IC-C):** fails G550 in all 4 cells (log X_J +0.22 to +0.32).
- **MJ (Jeans constraint removed, so the reference falls back to the law's phantom T_ph):** reproduces CFG550's failure.
  - MW: edge +0.47 / +0.52, log X_J +0.112 / +0.114.
  - Clusters blow up (T_ph diverges inside r_M).
- **MK (sink removed):**
  - sympy: w·δE = (v₁² − v₀²)/2 ≠ 0;
  - bench MW can: matter energy changes by +0.486 |E₀|, against an integrator error of 3.3e-4.

## Disclosures (dated 2026-10-10; the frozen text is not edited)

- **C6 fails as frozen.** The solver on a Gaussian in a harmonic field misses by 0.062 in σ_r² (σ_t² 0.014) at r ≤ 3.
  - Cause: the frozen piecewise-constant-density bins, where ρ falls by e^0.8 per bin near r = 3.
  - FIX-2's own isotropic formula on the same grid misses by 0.042. At r ≤ 1.5 the solver is within 0.0066.
  - Not a solver bug. Labels are given both as frozen (NO LABEL) and with C6 read at the grid's resolution, following the
    CFG544 C4 precedent.
  - No verdict hinges on it: route (a)'s cluster failure is a factor-of-40 effect in the tail.
- **A check-code fix was made before the full run.** The S1a "is Gaussian" comparison used log(exp(·)), which sympy left
  unsimplified for unsigned symbols, so the check reported a false negative. It now compares f directly. The maximiser
  printed was always the Gaussian. The C6 diagnostics (FIX-2's formula on the same grid, the r ≤ 1.5 bulk) were added
  post-freeze; no label depends on them.
- **Toy limits:** those of CFG544 (spherical; static baryons; 0.05 V_f seed; α = 1 O(1) FREE; isotropic-start inner boundary
  condition for the shooting at the innermost occupied bin).

## Plain reading

- A principle does yield a self-consistent Jeans target: maximum entropy at the current density, subject to the current
  density being stationary under the reversible flow. Its temperature is a multiplier field set by the current density's
  own Jeans balance. In MW-like systems it behaves like FIX-2 and passes.
- But the exact (tensor) form makes a dilute, point-mass-dominated tail radially hot. That spills cluster halos and pulls
  energy in.
- FIX-2's isotropic target, which works everywhere on the bench, needs isotropy added by hand (equivalently, a fluid rather
  than kinetic stationarity condition). So it stays POSITED. Its structure (metriplectic, energy-conserving with the φ sink,
  angular-momentum-conserving) is now derived.
- Overfill, α robustness at ×0.5, and a full-system Lyapunov function all remain open.
