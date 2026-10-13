# CFG696: the polarization field relaxes onto the law's profile by radiating

**Label: M1a PASS (attractor), M2b PASS (energy ledger).** Four non-law initial states, including no polarization at all, all
relax to the law's profile within 0.06–0.12%. The energy they lose equals the energy carried out by P waves to 0.02–0.2%. With
a reflecting boundary (no radiation) nothing relaxes. Point mass, spherical, fixed baryons.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (30a4ff252), 2026-10-13.
- **Script:** `cfg696.py`, one process, about 40 s, exit 0 → `cfg696.out`, `cfg696_results.json`. `CFG696_MUTATE=1` exits 1 (both
  teeth bite).
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".

## The equation
v_tt = v″ − 2v/s² − v|v|/s + 1/s (v = s q; CFG691 units), with a regular origin and an outgoing boundary at s = 200.
- Baryons enter only through 1/s² (Gauss).
- **No law quantity is in the dynamics** (R0's "no target in" holds for the mechanism).
- The energy is the one this Lagrangian implies; dE/dt = v_s v_t at the boundary exactly.

## Results

| initial state | max \|q − q_static\|/q_static on [0.1, 50], t = 500 / 1000 / 2000 | energy lost | energy radiated | mismatch |
|---|---|---|---|---|
| (i) zero (no cold mass) | 5.1e-2 / 3.0e-3 / **1.2e-3** | 2.99995 | 2.99909 | 2.9e-4 |
| (ii) 2× static | 8.9e-2 / 3.0e-3 / **1.2e-3** | 5.34164 | 5.34074 | 1.7e-4 |
| (iii) 0.5× static | 2.1e-2 / 1.5e-3 / **5.8e-4** | 0.89634 | 0.89612 | 2.5e-4 |
| (iv) 1 − e^{−s} | 4.1e-3 / 3.0e-3 / **1.2e-3** | 0.38727 | 0.38647 | 2.1e-3 |

- **Bound charge (the cold mass) inside s = 50**, starting from zero: 0 → 51.5 (t = 500) → 49.02 → 48.99 (static 48.99).
- **K1:** CFG691's static profile is reproduced; the discrete residual is 4e-6.
- **MUTATE M1 (reflecting boundary):** errors stay at 14–60% at t = 2000 and keep oscillating. Relaxation needs radiation.
- **MUTATE M2:** dropping the flux breaks the ledger. Both bite.

## Reading: the mechanism
1. **How the cold mass gets into the law's profile.** The vacuum's polarization field P is driven by the baryons' Gauss field.
   Any departure from the static profile is carried away as outgoing P waves. Because the static energy is convex (CFG692,
   CFG695), the field settles onto its unique minimum, which is the law's profile. The cold mass is the bound charge ∇·P that
   this leaves behind.
2. **Where the exchanged energy goes.** Into P radiation, the same field of the same action. No friction is added by hand, and
   no second field is needed.
3. **Gravity and lensing are consistent.** The bound charge sits in the one Poisson equation (CFG692/694). The mass that settles
   is the mass that lenses.
4. **No target is copied in.** Unlike the record's class-A settling (CFG638, which relaxes toward ρ_ph taken from the law), this
   dynamics contains only the action's terms and Gauss's law.

## Limits (stated once)
- Spherical, fixed point-mass baryons, cubic W. The saturating W (CFG695) only matters where u ~ a₀, which is not exercised here.
  Moving baryons, mergers and non-spherical systems are not run.
- The error floor stops at about 1e-3: it rises slightly from 8.8e-4 (t = 1500) to 1.2e-3 (t = 2000). This is disclosed as a
  numerical floor (grid ds = 0.02, approximate absorbing boundary). The frozen test (t = 2000 vs t = 1000) passes.
- **Timescale.** The relaxed region grows at c_P = √(γ/I), so a region of size r settles in about r/c_P. For a 10 kpc galaxy
  that is about 3×10⁴ yr at c_P = c, or 3×10⁷ yr at 10⁻³c. (The A4 lines in the .out quote code time × ℓ_γ, which is the time to
  settle about 50 ℓ_γ, not a whole galaxy.)
- I (or c_P) is a constant not yet fixed by any gate; c_P = c would make it free.
- In the MUTATE run the "radiated" column is a boundary-node artifact (the fixed node jumps at the first step). M2 sets the flux
  to zero regardless.
- **Still open:**
  - the free-fall basin reading as an action term (B1);
  - the relativistic completion (Φ = Ψ);
  - the C3, D2 and cluster gates, which were not re-scored;
  - κ fitted.
