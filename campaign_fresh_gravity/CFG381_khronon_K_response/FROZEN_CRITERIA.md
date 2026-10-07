# CFG381 FROZEN CRITERIA: does the khronon equation produce K ~ Gamma/c when the cold fluid settles?

Committed alone, before any script. kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is still required and is kept. No knob scans. Never "theory closed". Owner (2026-10-06, chat "Nobel Prize and neutrinos"): "yeah". The orchestrator was told first; it reserves CFG375-380 for its agents.

**Question.** CFG373 G3: the khronon can absorb the settling reaction only through its K^2 (c_2) sector, and only if settling induces a congruence expansion K ~ Gamma/c. Derive the induced K from the chassis' own khronon equation.

## Method (declared)
- Action (CFG292 / L340): (c^3/16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], beta = 0, u_mu = d_mu tau / sqrt(g^{ab} d_a tau d_b tau),
  tau = t + chi.
- Weak-field metric ds^2 = (1 + 2 Phi) dt^2 - (1 - 2 Psi) dx^2 + 2 B_i dx^i dt (c = 1 in the derivation; restored in the
  numbers). Linear order in (Phi, Psi, B, chi):
  a_i = d_i(chi-dot + Phi); K = div B - lap chi + 3 Psi-dot (sign conventions stated in the script; the result is taken in
  magnitude).
- sympy: build the quadratic Lagrangian density, take the Euler-Lagrange equation for chi, and read off the quasi-static
  relation between K and the matter-driven potentials.
- **The induced K is evaluated for settling:** Phi-dot ~ Gamma Phi (the potential re-arranges on the settling timescale),
  with Phi = V^2 (V = 200 km/s), Gamma = 3.21 H_Lambda (CFG370-corrected) and 5.4 H_Lambda, over the L340 window
  alpha_c in (9.62e-14, 3.2e-9), c_2 in (7.29e-3, 0.0667).

## Test
R_K = K_induced/(Gamma/c).
- **PRODUCES:** R_K >= 0.1 somewhere in the window (within an order of magnitude; CFG373's c_2 channel had >= 240x margin).
- **DOES NOT PRODUCE:** R_K < 0.1 everywhere. Then the khronon cannot be the sink through its gravitational coupling. Report
  what a DIRECT fluid-khronon coupling (one new constant lambda_x) would need, and say that it adds a constant.

## Controls
- C1: the linearised a_i and K reproduce the standard Einstein-aether / khronometric weak-field forms. Check that chi = 0,
  B = 0, static: a = grad Phi and K = 3 Psi-dot.
- C2: alpha_c = 0 decouples chi from Phi (the derived equation must reduce to lap K = 0 for alpha_c = 0).
- MUTATE: alpha_c -> 1 (far outside the window). R_K must change by > 1e6, rc 1.

Local compute only. No downloads.
