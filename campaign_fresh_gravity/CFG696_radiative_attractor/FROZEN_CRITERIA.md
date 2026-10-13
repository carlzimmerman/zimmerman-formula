# CFG696 — does the polarization field relax onto the law's profile by radiating? (M1a + M2b; frozen criteria)

Block CFG690–699. Written 2026-10-13, before any CFG696 script or number. Committed alone. κ = ½ fitted; both footings, never
pooled; the cold energy's mass is required; no particle species; not theory closed.

## Why
CFG694/695 give one action whose static solution is the law (with stiffness, saturation and free-fall basins). CFG679 still
lacks:
- **M1a:** the profile must be an attractor from non-law initial states, with no law quantity as input;
- **M2b:** the exchanged energy must go to a named field of the same action.

The action has a kinetic term (I/2)|Ṗ|² and a convex static energy (CFG692 T2, CFG695 S1). The candidate mechanism is
**radiation of P waves to infinity**. The same field P carries the energy away; the dissipation is not added by hand.

## The dynamical problem (point mass, CFG691's universal units)
Spherical, fixed baryons (a point mass), P = p(r,t) r̂. Units: r in ℓ_γ, p in B/ℓ_γ, t in ℓ_γ/c_P with c_P = √(γ/I).
- Equation: q_tt = L[q] − q|q| + 1/s², with L[q] = q″ + 2q′/s − 2q/s². With v = s q:
  v_tt = v″ − 2v/s² − v|v|/s + 1/s.
- Regularity: v(0) = 0.
- Outgoing boundary at s = S = 200: (v − v_∞)_t + (v − v_∞)_s = 0, with v_∞ = 1 − 1/s (the static asymptote).
- The cubic W is used: saturation is negligible wherever u ≪ a₀, and the point-mass problem is the screened/transition regime
  (CFG695 S3). Disclosed as a limit.
- **The equation contains no law quantity:** baryons enter only through 1/s² (Gauss), which satisfies R0's "no target in" for
  the dynamics.

## Tests
- **A1. Attractor.** Initial states: (i) v = 0 (no polarization, no cold mass); (ii) 2× the static solution; (iii) 0.5× the
  static solution; (iv) v = 1 − e^{−s} (wrong shape); all with v_t = 0.
  - Evolve to t = 2000 (10 crossing times of the domain).
  - **PASS iff, for every initial state, max |q − q_static|/q_static over s ∈ [0.1, 50] at t = 2000 is ≤ 1%, and it decreases
    over the last half of the run.**
  - q_static is CFG691's BVP profile (control K1: the static limit of this code's spatial operator reproduces it to ≤ 1e-3).
- **A2. Energy ledger (M2b).**
  - Energy inside the domain: E(t) = ∫[½v_t² + ½(v_s)² + v²/s² + v³/(3s) − v/s] ds. This is the (v, s) form of the action's
    energy; its exact form is derived in the script and checked to conserve with a reflecting boundary (control K2).
  - **PASS iff E(0) − E(t) equals the time-integrated outgoing flux through s = S to within 1%**, for every initial state: the
    lost energy is carried out by P waves.
- **A3 (reported). Where the cold mass comes from.** The bound charge inside s, M_c(<s) ∝ s² q (surface flux). For initial
  state (i), report M_c(<50) at t = 0, 500, 1000, 2000, and the flux of P at the outer boundary. The ledger: halo mass appears as
  the outgoing front carries the compensating charge outward.
- **A4 (reported). Timescale.** In physical units the relaxation time is t_relax = (relaxation time in code units) × ℓ_γ/c_P.
  Report it for a 10¹⁰ M☉ galaxy and for the Sun at L* = 5.75 pc, for c_P = c and c_P = 10⁻³c. I is a constant not fixed by any
  gate so far: state it as such.

## Verdict
- **M1a PASS and M2b PASS** iff A1 and A2 pass. Then the mechanism is: the vacuum's polarization relaxes onto the law's profile
  by radiating P waves, and the cold mass is the bound charge left behind.
- Still open, whatever the verdict:
  - non-spherical, moving baryons;
  - the basin reading as an action (B1);
  - the relativistic completion;
  - C3, D2 and clusters not re-scored;
  - I (or c_P) a second constant unless tied to c.

## MUTATE (`CFG696_MUTATE=1`, exit 1 iff both bite)
- **M1:** reflecting outer boundary (v fixed at S). No radiation: A1 must FAIL, since the energy cannot leave.
- **M2:** the radiation flux omitted from the balance. A2 must FAIL.
