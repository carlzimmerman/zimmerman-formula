# CFG390: a two-fluid "Navier-Stokes" system for the cold fluid. PARTIAL

Criteria: `FROZEN_CRITERIA.md`, committed alone first (246c8d697). kappa = 1/2 is FITTED. Both a0 footings are scored separately and never pooled. No new species: the cold fluid is the record's ~eV Bose field (CFG383/384), and its amount (5.364 per original baryon) is an input, not derived. This is not "theory closed".

Run: `python3 cfg390_symbolic.py; python3 cfg390_spherical.py; python3 cfg390_verdict.py`. Add `CFG390_MUTATE=1` (kappa_s = 0) for the `*_MUTATE` outputs. The verdict script carries the exit code: main rc 0, MUTATE rc 1. Run time is about 6 min at nice 15.

## The system (the owner's request, with the declared refinements)

- **Condensate (inviscid):** d_t v_s + v_s.grad v_s = -grad[Phi + g rho_s/m^2 + Q + kappa_s ln(rho_s/rho_ph)].
- **Normal (Navier-Stokes):** rho_n D v_n = -grad(rho_n sigma_n^2) - rho_n grad Phi + div(eta * traceless shear).
- **Conversion C** between the two components, exchanging momentum.
- **Gravity:** lap Phi = 4 pi G (rho_b + rho_s + rho_n). The phantom is the TARGET, not a source.

Refinements, all frozen before any script:
- **R1.** The proposed C = (rho_n - rho_n_eq)/tau ANTI-relaxes. The sign is flipped.
- **R2.** C takes the Onsager form L (mu_s - mu_n).
- **R3.** The normal free energy is referenced to the Bose critical density.
- **R4.** The settling energy is the generalised relative entropy.
- **R5.** Converted mass carries the donor's momentum.
- **R6.** The settling reaction goes to the khronon sink.

## Verdict: PARTIAL (both footings)

### (A) Symbolic, sympy, 1D slab with every term

| item | result |
|---|---|
| A1 mass | PASS |
| A1b as proposed, C anti-relaxes | confirmed. **Bug in the proposal, fixed by R1.** |
| A2 momentum | exchange terms cancel exactly. Every stress is a pure flux. **The settling term is NOT a flux**: momentum kappa_s rho_s grad ln rho_ph per unit volume needs the declared sink (CFG373/381, one coupling). PASS with the declared sink. |
| A3 Galilean invariance | PASS (residual 2e-16), provided the target moves with the baryons |
| A4 H-theorem | PASS as an identity: d_t e + div J = -(4/3) eta v_x^2 - L (mu_s - mu_n)^2 + C (1/2 - theta)(dv)^2 <= 0 |
| A4b | the task's relaxation-time C (sign-fixed, with CFG383's Bose rho_n_eq) is **not** compatible with an H-theorem. At rho_s = 0.1 rho_ph, rho_n = 0.9 rho_crit, F rises. Only the Onsager form is safe. |
| A4c | a moving target adds kappa_s (1 - rho_s/rho_ph) d_t rho_ph. This energy is exchanged with the sink and has no fixed sign. |
| A5 rest state | **FAIL.** At rho_s = rho_ph, v = 0 the condensate's acceleration is exactly -grad(Phi + h + Q). The true rest state is rho_s = rho_ph exp[(mu - Phi - h - Q)/kappa_s]. The law is held only if kappa_s >> the depth of the potential across the system. |

Conditions for A4:
- static baryons and target;
- eta >= 0 and L >= 0;
- the donor rule for exchanged momentum;
- uniform sigma_n, with heat going to a bath.

Sensitivity: dropping the viscous term breaks the A4 identity (max |EL| 1.4), so the test can fail.

### (B) Spherical end state

This uses the quasi-static relaxation limit (declared): uniform mu across both fluids, self-consistent Phi, and cold mass conserved inside the Lagrangian sphere.

| case | canonical | alt |
|---|---|---|
| **MW, primary kappa_s** (sqrt = lambda_382 x 200 km/s = 5.6 km/s), f_ret 0.18: max abs(V/V_law - 1), 10-100 kpc | **4.15** (not recovered) | **3.99** (not recovered) |
| MW, kappa_s bracket 300 / 1000 / 3000 km/s / infinity (reported) | 0.53 / 0.55 / 0.55 / 0.55 | 0.55 / 0.57 / 0.57 / 0.57 |
| MW, f_ret = 1, primary / infinity | 1.28 / 0.65 | 1.20 / 0.66 |
| **Cluster u500 = M_n/M_cold (<R500)**, primary kappa_s, m 0.8066 | **1.00** (passes >= 0.3) | **1.00** (passes) |
| cluster M(<R500)/M_law, primary | 0.275 | 0.247 |

**Two structural failures.**

1. **Collapse.** The kappa_s set by CFG382's rate equals lambda_382^2 = 7.8e-4 of V^2. That is far too weak to hold the condensate against gravity.
   - In the MW, the condensate collapses into the innermost cell (r_half <= 10 pc, the grid floor), and the rotation curve rises to about 5 times the law.
   - **The MUTATE run (kappa_s = 0) gives identical MW numbers.** At its frozen rate, the settling term does nothing.
2. **Proportional filling.** Even for stiff kappa_s (to infinity), the relative-entropy term fills the target in proportion: rho_s = A rho_ph with A = S/M_ph(<R_dom).
   - It does not fill from the inside out.
   - The MW gets A = 0.035-0.12 (R_dom = R_L, f_ret 1 and 0.18; 0.22-0.24 at R_L/2), so the median V over 10-100 kpc sits 42-50% below the law.
   - Control C2c: when the supply is set equal to M_ph(<R_dom), the law is reproduced to 1e-13. So the failure comes from the supply and the functional, not from the numerics.

**The cluster "pass" is hollow (read before citing).**
- u500 = 1 because the cold fluid at the primary kappa_s stays entirely in the normal (unsettled) phase. Its critical density at sigma = 1000 km/s is high enough to hold all of it.
- So M(<R500) is only 0.25-0.28 of the law's mass there.
- At stiff kappa_s (3000 km/s or infinity) u500 drops to 0, because the under-supplied condensate leaves mu - Phi far below zero.
- The quasi-static end state is not reached in the cluster:
  - the conversion time at R500 is 50-7000 ages;
  - the settling crossing time is 12 ages.

**Viscosity (role).** Lagrangian isothermal Navier-Stokes control, normal fluid only, cluster potential.
- Viscosity does **not** change the end state. V1: the eta_ref and 0.1 eta_ref runs end 0.2-0.3% from hydrostatic.
- F decreases monotonically (V2).
- Viscosity is the normal fluid's only relaxation channel. V3: without it, 92% of the peak kinetic energy is still present after 30 Gyr, against 4e-15 with eta_ref.
- **But the Knudsen number at the cluster's R500 is 51** at the Bullet-limit cross-section. There the normal component is collisionless, and the Navier-Stokes form is not valid. In the MW at 10 kpc, Kn = 2e-4, so it is valid.
- The condensate is inviscid. Its only dissipation is the conversion friction (or a khronon drag). Its relaxation rate is not derived here.

Controls C1 (target), C2a/b/c (solver), C3 (CFG383 u = 0.5 reproduced exactly), C4, and V1-V3 all pass. The MUTATE flips all pass as declared:
- the sink is no longer required;
- the MW is not recovered in any of 11 cells;
- the Thomas-Fermi core has r_half 0.01 kpc.

## What it means
- The two-fluid system is a **consistent dynamical frame** once refinements R1, R2 and R6 are in: mass, momentum up to one declared sink, Galilean invariance, and an H-theorem.
- As a mechanism for the law it fails in two declared ways:
  - **(i)** the rest state is not rho_ph in any gravitating host unless kappa_s >> V^2 (about (7 V)^2 or more for 5%), roughly 6e4 times CFG382's rate-matched value;
  - **(ii)** the relative-entropy potential cannot do inside-out, supply-limited filling, which is what working-model piece 4 assumes.
- A working settling functional would need two properties:
  - a target that already includes the force balance: Phi enters mu_s, so the target must be rho_ph exp((Phi + h)/kappa_s), which is hand-built;
  - a non-scale-free penalty that saturates at rho_ph.
- Neither is derived. The open pieces stay open: the settling force (CFG60), the rate, and the amount.

## Caveats and disclosures
- **Spherical, static baryons.** The MW is a spherical Hernquist model (a = 3 kpc); the cluster is Hernquist with a = 250 kpc. Temperature is uniform per host. The Lagrangian sphere is a closed box. The analytic nu kernel is used (it differs from the record's nu_mono by up to 2.4% near y ~ 10).
- **Bose closure.** The normal fluid is a classical Boltzmann gas capped at the Bose critical density, not the exact Bose g_{3/2} function. h and Q are negligible (Q/Delta Phi below 1e-42 in resolved cells).
- **Choices made at script time** (not in the criteria, disclosed):
  - The viscosity control's normal mass is 2.682e14 Msun (= 0.5 S).
  - Its eta = 0 run carries a weak von Neumann-Richtmyer artificial viscosity for shock capture, and V3 is scored with it.
  - The primary MW collapse is limited by the grid floor (10 pc). The true Thomas-Fermi core is about 15 pc or smaller (estimate).
- **Development bugs, fixed before the committed run:**
  - brentq rtol below the machine floor;
  - the first global viscous time-step limit was too slow;
  - an a-posteriori Q diagnostic that divided by underflowed densities, printing 1e248. It is now restricted to resolved cells.
- **Script exit codes.** The symbolic and spherical scripts do not set rc; `cfg390_verdict.py` carries rc (main 0, MUTATE 1).
- **The frozen kappa_s bracket never changes the verdict.** No kappa_s value is adopted. The "(7 V)^2" figure is an analytic estimate of what would be needed, not a fit.

Files:
- scripts: `cfg390_symbolic.py`, `cfg390_spherical.py`, `cfg390_verdict.py`;
- outputs: `*.out` and `*_results.json`, with `*_MUTATE` counterparts.
