# CFG348: a switch that reads the baryonic specific energy instead of the expansion?

Criteria: `FROZEN_CRITERIA.md` (commit aac73537d, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; c_T = 1; beta = 0; the switch reads baryons only (MS1-MS5); no DM particle (the cold mass is still required).

**Verdict (frozen rule): NO-GO.** Every admissible route fails (a) and (b). The obstruction is structural, and the
Lean file certifies it (9 theorems). The energy reader does fix CFG347's fidelity problem: inside the saturated
interior a compression changes nothing. But it cannot be OFF on FRW. This is a scoped result, not a closure.

## The reader and the action
- On the khronon leaves (diff-safe, CFG329): eps_b = |v_b|^2/2 + U.
  - v_b is the baryon velocity relative to the leaf normal, which is the Hubble flow on FRW.
  - U is a leaf potential whose source has the leaf average subtracted.
  - The threshold is exactly 0.
- Slaved gate: L ⊃ B W(eps_b), with W = S(-eps_b/eps_on) and S = DE12's C-infinity step. The gate is ON at
  eps <= -eps_on and OFF at eps >= 0.
- Dynamical gate (CFG347 R3 structure): S = Int sqrt(-g)[ -(Z/2)(d sigma)^2 - (Z M^2/2) sigma^2 - C sigma eps_b ], with
  f = S(sigma) and eps_on = Z M^2/C.

## MS check on U (decides admissibility)
The chassis's auxiliary U is not baryonic. L340 H1 (record) gives U/psi_N = 1 as alpha_c -> 0, and psi_N is sourced
by all matter coupling to g, the cold carrier included (CFG329 G9). Reading it is MS1's curvature/matter door, which
leaks 0.06-2300x the carrier's gravity at region edges. **So the proposal as stated violates the record rule.**
Two admissible replacements are tested:
- **E1:** the baryonic potential, lap U_b = 4 pi G (rho_b - <rho_b>), MS1 door d.
- **E2:** the MOND-sector potential lap(Phi - v), which is baryons plus phantom with the carrier only as its mean
  (MS1 door c).

## Results (24 DE12 hosts, both footings)
| route | (a) FRW | (b) bound | (c) transition | constants | tier |
|---|---|---|---|---|---|
| E1, eps_on = a0 c/H0 | FAIL | FAIL (0/24 ON) | PASS | 0 | NO-GO |
| E1, eps_on,min | FAIL | FAIL | FAIL (ghost) | 1 | NO-GO |
| E2, eps_on = a0 c/H0 | FAIL | FAIL (0/24 ON) | PASS | 0 | NO-GO |
| E2, eps_on,min | FAIL (growth x9.5/x10.9) | FAIL (8/24 ON) | FAIL (ghost, min m/rho -0.13) | 1 | NO-GO |
| E3 dynamical, zero-constant | FAIL | FAIL (reach) | PASS | 0 | NO-GO |

- **(a) FRW.**
  - sympy: the flat-FRW shell energy is -k r^2/(2a^2) = 0. The Hubble flow is marginally bound, eps = 0 exactly,
    whatever Lambda is. With a zero threshold, FRW sits on the gate's edge, so there is no finite OFF neighbourhood
    (Lean E2c).
  - The linear wells are deep: sigma_Phi = 7.7e-6 c^2, that is (829 km/s)^2, with sigma_v = 445 km/s.
  - At the theory's own width the mean gate is 0.38, and L341's harness gives D/D_LCDM = 9.48 (canonical) / 10.89
    (alt).
  - The zero-constant width a0 c/H0 (about 0.2 c^2) gives growth = LCDM. It still fails the neighbourhood clause, and
    it is OFF in every galaxy.
- **(b) bound.**
  - E1 is negative in the inner hosts (eps_b/v_c^2 down to -0.22). It is positive at 30 kpc on 16/24 hosts
    (theorem: eps_b = g_N r (nu - 2)/2). MOND-supported orbits beyond 2 r_M exceed the baryons' Newtonian escape
    speed, so a purely baryonic energy calls them unbound (Lean E3, E3f).
  - E2 is ON statically. eps_ms(30 kpc) = -2.2 to -3.8 v_c^2, that is (160-820 km/s)^2.
  - E2 fidelity: with a per-host width (lenient, 24 constants, not scored) it passes 24/24, with |dW| = 0 and a
    gas-mode change of 0 (eps is conserved; W' = W'' = 0 in the saturated interior, Lean E5).
  - With the one universal width, only 8/24 hosts are ON at 30 kpc. The gas-mode change reaches 0.99, and |dW| is at
    most 0.02.
  - E3 zero-constant: CFG347's T7 does not depend on what the switch reads. ell/r_ta >= 267 (3H), 800 (H) and 7.8e3
    (a0/c).
- **(c) transition.**
  - A velocity-reading gate changes the inertia: m_par = rho + B(W' + W'' v^2) and m_perp = rho + B W' (sympy).
  - The theory therefore picks its own minimum width from no-ghost. The exact width is (105-484 km/s)^2 per host,
    2.6e-6 c^2 universal.
  - The frozen closed form, max[S' v_B^2, sqrt(S'') v_c v_B] = 2.44e-6 c^2, undershoots it and shows a ghost.
  - The exact value is a declared deviation, reported and not scored. It does not change any tier.
  - H2/H3: U enters only through the elliptic constraint (~k^-2), so the principal part is the gas's. This is an
    argument, not a computed symbol.
- **Switch width (E2, at eps_on,min):** ell_eps = eps_on/|d eps/dr| = 181 kpc to 4.0 Mpc (16/24 hosts cross inside
  r_ta). That exceeds the 100 kpc tolerance and reaches CFG337's C2 ell_min (183-378 kpc) only at its low end.

## The obstruction in one line
eps is additive and infrared: flat FRW is marginally bound (eps = 0 exactly), and linear wells, sigma_Phi = (829
km/s)^2, are deeper than the gate width the theory needs, (469-484 km/s)^2. That width is in turn deeper than the
shallowest host's |eps| at 30 kpc, (160 km/s)^2 (Lean E6). So a single width cannot hold the linear field OFF and
every host ON. A purely baryonic potential fails earlier: by the escape theorem, it calls MOND outskirts unbound.

## Constants
The zero-constant routes add 0 constants (eps_on = a0 c/H0, c_sigma = c, M a framework rate). The theory-width routes
add 1 (universal eps_on). Per-host widths would add 24 (not scored).

## Controls
- **C1:** CFG347's theta_b x = 0.285-6.6 (3H) and 32.7-154 (a0/c), reproduced.
- **C2:** in the GR limit the inertia is diag(rho, rho).
- **MUTATE (ON at eps <= 0):** the switch is ON on FRW. Growth is 28.79x / 33.93x (sigma_8 23.32 / 27.48), the chassis
  values. The run exits 1.

## Lean
`CFG348_energy_certificates.lean`: 9 theorems, no sorry, standard axioms only (rc 0; output in `.out`).
- E1 FRW shell identity;
- E2 / E2c zero threshold: no OFF neighbourhood;
- E3 / E3f baryonic escape;
- E4 no-ghost inequality;
- E5 saturated fidelity;
- E6 / E6g nested wells.

## Run
```
python3 campaign_fresh_gravity/CFG348_energy_reading_switch/cfg348_energy_switch.py > campaign_fresh_gravity/CFG348_energy_reading_switch/cfg348_energy_switch.out   # rc 0, ~3 s
CFG348_MUTATE=1 python3 campaign_fresh_gravity/CFG348_energy_reading_switch/cfg348_energy_switch.py > campaign_fresh_gravity/CFG348_energy_reading_switch/cfg348_energy_switch_MUTATE.out   # rc 1
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG348_energy_reading_switch/CFG348_energy_certificates.lean
```

**Scope:**
- quadratic level, quasi-static, on DE12's point-mass hosts;
- E2's U_ms uses CFG347's r_ta reference with Lambda omitted;
- the (a) growth uses a mean-field gate over a Gaussian linear (Phi, v) field with k >= 0.02 h/Mpc (lenient, since it
  underestimates sigma_Phi);
- the compression is worst-case (azimuthal plus MOND-amplified potential);
- a costed dynamical E3 (free c_sigma, M) was not run, because (a) fails for any width.
